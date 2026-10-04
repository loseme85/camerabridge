"""의견 보내기: 화면의 '의견 보내기' → 비공개 저장(Vercel Blob, private) + 텔레그램 알림.

저장 위치: Blob 스토어 camerabridge-feedback 의 feedback/YYYY-MM-DD/… .json (비공개, 저장소에는 안 남김)
나중에 공개 목록으로: 사장님이 고른 의견만 따로 공개 파일로 내보냄 (status/public 칸).
스팸 막기: 숨은 입력칸(봇만 채움), 창을 연 지 1.5초 안에 보내면 거절, 같은 접속지(IP 해시) 하루 5건까지.
"""
from __future__ import annotations

import datetime as dt
import hashlib
import json
import os
import re
import secrets
from http.server import BaseHTTPRequestHandler

import requests

MAX_LEN = 2000
MIN_LEN = 5
DAILY_LIMIT = 5
EMAIL = re.compile(r"^[^@\s]{1,64}@[^@\s]{1,190}\.[^@\s]{2,24}$")
KST = dt.timezone(dt.timedelta(hours=9))


def _client_ip(headers) -> str:
    forwarded = headers.get("x-forwarded-for") or headers.get("x-real-ip") or ""
    return forwarded.split(",")[0].strip()


def _ip_tag(ip: str, day: str) -> str:
    # 날마다 바뀌는 소금을 섞어 IP 자체는 남기지 않음
    salt = os.environ.get("FEEDBACK_SALT", "camerabridge")
    return hashlib.sha256(f"{salt}:{day}:{ip}".encode()).hexdigest()[:12]


def _notify(entry: dict) -> None:
    token, chat = os.environ.get("TELEGRAM_BOT_TOKEN"), os.environ.get("TELEGRAM_CHAT_ID")
    if not token or not chat:
        return
    lines = [f"💬 Camera Bridge 의견 ({entry.get('locale') or '-'})", "", entry["message"], ""]
    if entry.get("email"):
        lines.append(f"✉️ {entry['email']}")
    if entry.get("entity"):
        lines.append(f"📷 {entry['entity']}")
    if entry.get("page"):
        lines.append(f"🔗 {entry['page']}")
    try:
        requests.post(f"https://api.telegram.org/bot{token}/sendMessage",
                      json={"chat_id": chat, "text": "\n".join(lines)[:4000], "disable_web_page_preview": True},
                      timeout=8)
    except requests.RequestException:
        pass


def handle(body: dict, headers) -> tuple[int, dict]:
    if not isinstance(body, dict):
        return 400, {"ok": False, "error": "bad_request"}
    if str(body.get("website") or "").strip():  # 숨은 칸: 사람은 비워 둠
        return 200, {"ok": True}
    try:
        elapsed = int(body.get("elapsed_ms") or 0)
    except (TypeError, ValueError):
        elapsed = 0
    if elapsed < 1500:
        return 429, {"ok": False, "error": "too_fast"}
    message = re.sub(r"\s+\n", "\n", str(body.get("message") or "")).strip()
    if not (MIN_LEN <= len(message) <= MAX_LEN):
        return 400, {"ok": False, "error": "length"}
    email = str(body.get("email") or "").strip()[:254]
    if email and not EMAIL.match(email):
        return 400, {"ok": False, "error": "email"}

    from vercel import blob  # noqa: WPS433 (함수가 불릴 때만)

    now = dt.datetime.now(KST)
    day = now.strftime("%Y-%m-%d")
    tag = _ip_tag(_client_ip(headers), day)
    prefix = f"feedback/{day}/"
    try:
        listed = blob.list_objects(prefix=prefix, limit=1000)
        names = [item.pathname for item in (getattr(listed, "blobs", None) or [])]
    except Exception:  # noqa: BLE001
        names = []
    if sum(1 for name in names if f"-{tag}-" in name) >= DAILY_LIMIT:
        return 429, {"ok": False, "error": "limit"}

    entry = {
        "id": f"{now.strftime('%Y%m%d%H%M%S')}-{secrets.token_hex(3)}",
        "created_at": now.isoformat(timespec="seconds"),
        "message": message,
        "email": email or None,
        "locale": str(body.get("locale") or "")[:12] or None,
        "page": str(body.get("page") or "")[:300] or None,
        "entity": str(body.get("entity") or "")[:120] or None,
        "status": "new",      # new → 검토 → 개발 중 → 완료 (공개 목록으로 옮길 때)
        "public": False,      # 사장님이 고른 의견만 공개
    }
    try:
        blob.put(f"{prefix}{now.strftime('%H%M%S')}-{tag}-{secrets.token_hex(4)}.json",
                 json.dumps(entry, ensure_ascii=False).encode("utf-8"),
                 access="private", content_type="application/json")
    except Exception:  # noqa: BLE001
        _notify({**entry, "message": entry["message"] + "\n\n(⚠️ 저장 실패 — 이 알림이 유일한 기록)"})
        return 200, {"ok": True}
    _notify(entry)
    return 200, {"ok": True}


class handler(BaseHTTPRequestHandler):
    def _send(self, status: int, payload: dict) -> None:
        body = json.dumps(payload).encode()
        self.send_response(status)
        self.send_header("content-type", "application/json")
        self.send_header("cache-control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def do_POST(self):  # noqa: N802
        length = min(int(self.headers.get("content-length") or 0), 16_000)
        try:
            body = json.loads(self.rfile.read(length) or b"{}")
        except ValueError:
            return self._send(400, {"ok": False, "error": "bad_json"})
        status, payload = handle(body, self.headers)
        return self._send(status, payload)

    def do_GET(self):  # noqa: N802
        return self._send(405, {"ok": False})
