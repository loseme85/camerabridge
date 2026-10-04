"""사용 기록: 방문 한 번에 한 묶음(검색어·고른 모델·결과 수·판매처 클릭) → 비공개 Vercel Blob.

저장 위치: usage/YYYY-MM-DD/HHMMSS-<세션>-<n>.json (비공개, 저장소에는 안 남김)
남기지 않는 것: IP, 이메일, 쿠키. 세션 ID는 브라우저 탭마다 새로 만드는 무작위 값.
Blob 무료 한도(쓰기 월 2,000회)를 아끼려고 화면이 방문당 최대 3번만 보낸다. 끄기: USAGE_LOG_DISABLED=1
요약: python3 scripts/usage_report.py
"""
from __future__ import annotations

import datetime as dt
import json
import os
import re
from http.server import BaseHTTPRequestHandler

KST = dt.timezone(dt.timedelta(hours=9))
SID = re.compile(r"^[a-z0-9]{8,24}$")
MAX_SEARCHES = 40
MAX_CLICKS = 40


def _text(value, limit: int) -> str | None:
    text = re.sub(r"\s+", " ", str(value or "")).strip()[:limit]
    return text or None


def _int(value) -> int | None:
    try:
        return max(0, min(int(value), 1_000_000))
    except (TypeError, ValueError):
        return None


def clean(body: dict) -> dict | None:
    if not isinstance(body, dict) or not SID.match(str(body.get("sid") or "")):
        return None
    searches = []
    for item in (body.get("searches") or [])[:MAX_SEARCHES]:
        if not isinstance(item, dict) or not _text(item.get("q"), 120):
            continue
        searches.append({
            "q": _text(item.get("q"), 120),
            "entity": _text(item.get("entity"), 120),
            "results": _int(item.get("results")),
            "active": _int(item.get("active")),
            "s": _int(item.get("s")),  # 방문 시작 뒤 몇 초
        })
    clicks = []
    for item in (body.get("clicks") or [])[:MAX_CLICKS]:
        if not isinstance(item, dict) or not _text(item.get("host"), 80):
            continue
        clicks.append({
            "host": _text(item.get("host"), 80),
            "entity": _text(item.get("entity"), 120),
            "q": _text(item.get("q"), 120),
            "s": _int(item.get("s")),
        })
    if not searches and not clicks:
        return None
    return {
        "sid": body["sid"],
        "part": _int(body.get("part")) or 1,
        "locale": _text(body.get("locale"), 12),
        "currency": _text(body.get("currency"), 8),
        "referrer": _text(body.get("referrer"), 80),  # 호스트만 (예: www.reddit.com)
        "landing": _text(body.get("landing"), 200),   # 경로와 utm만
        "mobile": bool(body.get("mobile")),
        "duration_s": _int(body.get("duration_s")),
        "searches": searches,
        "clicks": clicks,
    }


def handle(body: dict) -> tuple[int, dict]:
    if os.environ.get("USAGE_LOG_DISABLED") == "1":
        return 200, {"ok": True}
    entry = clean(body)
    if entry is None:
        return 400, {"ok": False}
    from vercel import blob  # noqa: WPS433 (함수가 불릴 때만)

    now = dt.datetime.now(KST)
    entry["created_at"] = now.isoformat(timespec="seconds")
    path = f"usage/{now:%Y-%m-%d}/{now:%H%M%S}-{entry['sid']}-{entry['part']}.json"
    try:
        blob.put(path, json.dumps(entry, ensure_ascii=False).encode("utf-8"),
                 access="private", content_type="application/json")
    except Exception:  # noqa: BLE001 (기록 실패는 사용자에게 알리지 않음)
        return 200, {"ok": False}
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
        length = min(int(self.headers.get("content-length") or 0), 32_000)
        try:
            body = json.loads(self.rfile.read(length) or b"{}")
        except ValueError:
            return self._send(400, {"ok": False})
        status, payload = handle(body)
        return self._send(status, payload)

    def do_GET(self):  # noqa: N802
        return self._send(405, {"ok": False})
