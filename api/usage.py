"""사용 기록: 방문 한 번에 한 묶음(검색어·고른 모델·결과 수·판매처 클릭) → 비공개 Vercel Blob.

저장 위치: Neon Postgres usage_events (DATABASE_URL 있을 때, pgstore.py) · 없으면 Blob usage/YYYY-MM-DD/HHMMSS-<세션>-<n>.json
남기는 나라: Vercel이 붙여 주는 접속 나라 코드(x-vercel-ip-country, 예: KR)만. 남기지 않는 것: IP, 이메일, 쿠키. 세션 ID는 브라우저 탭마다 새로 만드는 무작위 값.
보내는 곳: 첫 화면(beta.html)과 모델 시세 페이지(track.js). 같은 탭이면 한 방문(sid)으로 묶이고, 페이지마다 첫 묶음은 검색·클릭이 없어도 보냄(어디서 왔는지 남기려고).
같은 사람 하루 한 번: IP를 그날 날짜·비밀 소금과 섞은 해시(vtag, 12자)만 남김. IP 자체는 저장 안 하고, 날이 바뀌면 값도 바뀌어 날끼리 이어 볼 수 없음. 새 기록은 브라우저 저장소의 무작위 vid로 날짜를 넘어 연결(생성 후 1년), 로그인 정보와 연결하지 않음.
들어온 곳(referrer): 바깥 사이트의 도메인+경로(?·# 뒤는 버림, 예: www.reddit.com/r/Leica/comments/abc). 로봇(user-agent)은 기록 안 함.
사장님 브라우저는 빼기: /owner/usage 를 열면 /api/usage 에만 가는 표시 쿠키(cb_skip_usage=1)가 생기고, 그 쿠키가 오면 기록하지 않음.
Blob 무료 한도(쓰기 월 2,000회)를 아끼려고 화면이 방문당 최대 3번만 보낸다. 끄기: USAGE_LOG_DISABLED=1
요약: python3 scripts/usage_report.py
"""
from __future__ import annotations

import datetime as dt
import hashlib
import json
import os
import re
import sys
from http.server import BaseHTTPRequestHandler
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

KST = dt.timezone(dt.timedelta(hours=9))
BROWSER_ID = re.compile(r"^[a-f0-9]{32}$")
SID = re.compile(r"^[a-z0-9]{8,24}$")
COUNTRY = re.compile(r"^[A-Z]{2}$")
MAX_SEARCHES = 40
MAX_CLICKS = 40
TZ = re.compile(r"^[A-Za-z]+(?:/[A-Za-z0-9_+\-]+){1,2}$")
VIA = {"typed", "pick", "chip", "link", "other"}
BOT = re.compile(r"bot|crawl|spider|slurp|headless|lighthouse|preview|python|curl|wget", re.I)


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
        one = {
            "q": _text(item.get("q"), 120),
            "entity": _text(item.get("entity"), 120),
            "results": _int(item.get("results")),
            "active": _int(item.get("active")),
            "s": _int(item.get("s")),  # 방문 시작 뒤 몇 초
        }
        if item.get("via") in VIA:  # 어떻게 찾았나: typed·pick·chip·link·other
            one["via"] = item["via"]
        if _text(item.get("typed"), 120):  # pick 일 때 고르기 전에 친 글자
            one["typed"] = _text(item.get("typed"), 120)
        searches.append(one)
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
    page = _text(body.get("page"), 200)
    if not searches and not clicks and not page:
        return None
    return {
        "sid": body["sid"],
        "vid": body.get("vid") if isinstance(body.get("vid"), str) and BROWSER_ID.fullmatch(body["vid"]) else None,
        "part": _int(body.get("part")) or 1,
        "locale": _text(body.get("locale"), 12),
        "currency": _text(body.get("currency"), 8),
        "page": page,                                  # 이 묶음을 보낸 페이지 경로 (예: /ko/leica/m6/)
        "referrer": _text(body.get("referrer"), 160),  # 도메인+경로 (예: www.reddit.com/r/Leica/comments/abc)
        "landing": _text(body.get("landing"), 200),   # 경로와 utm만
        "mobile": bool(body.get("mobile")),
        "duration_s": _int(body.get("duration_s")),
        "scroll": min(100, _int(body.get("scroll")) or 0),  # 얼마나 내려 봤나 % (2026-11-08)
        "searches": searches,
        "clicks": clicks,
    }


def visitor_tag(ip: str, day: str) -> str | None:
    """같은 IP·같은 날 → 같은 값. 소금은 비밀값(USAGE_SALT, 없으면 Blob 토큰)이라 IP를 거꾸로 맞혀 볼 수 없음."""
    ip = str(ip or "").split(",")[0].strip()
    if not ip:
        return None
    salt = os.environ.get("USAGE_SALT") or os.environ.get("BLOB_READ_WRITE_TOKEN") or "camerabridge-usage"
    return hashlib.sha256(f"{salt}:{day}:{ip}".encode()).hexdigest()[:12]


def handle(body: dict, country: str | None = None, cookie: str | None = None, agent: str | None = None,
           ip: str | None = None, timezone: str | None = None) -> tuple[int, dict]:
    if os.environ.get("USAGE_LOG_DISABLED") == "1":
        return 200, {"ok": True}
    if agent and BOT.search(agent):  # 검색엔진 로봇이 페이지를 그리다 보낸 것
        return 200, {"ok": True, "skipped": True}
    if "cb_skip_usage=1" in (cookie or ""):  # 사장님 브라우저 (/owner/usage 를 연 적 있음) → 기록 안 함
        return 200, {"ok": True, "skipped": True}
    entry = clean(body)
    if entry is None:
        return 400, {"ok": False}
    country = str(country or "").strip().upper()
    if COUNTRY.match(country):
        entry["country"] = country
    timezone = str(timezone or "").strip()
    if TZ.match(timezone):  # 접속한 곳의 시간대 (Vercel x-vercel-ip-timezone, 예: America/New_York) → 방문 현황에서 현지 시각으로
        entry["tz"] = timezone
    now = dt.datetime.now(KST)
    entry["created_at"] = now.isoformat(timespec="seconds")
    tag = visitor_tag(ip, f"{now:%Y-%m-%d}")
    if tag:
        entry["vtag"] = tag
    import pgstore  # noqa: WPS433
    try:
        if pgstore.enabled():  # Neon Postgres (2026-11 Blob 무료 한도 초과 뒤)
            pgstore.add_usage(entry)
        else:
            from vercel import blob  # noqa: WPS433 (함수가 불릴 때만)
            path = f"usage/{now:%Y-%m-%d}/{now:%H%M%S}-{entry['sid']}-{entry['part']}.json"
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
        status, payload = handle(body, self.headers.get("x-vercel-ip-country"), self.headers.get("cookie"),
                                 self.headers.get("user-agent"),
                                 self.headers.get("x-forwarded-for") or self.headers.get("x-real-ip"),
                                 self.headers.get("x-vercel-ip-timezone"))
        return self._send(status, payload)

    def do_GET(self):  # noqa: N802
        # 첫 화면 언어 권유용: 접속 나라 코드만 돌려줌 (기록하지 않음, 사람마다 달라 캐시 안 함)
        if "geo" in (self.path.split("?", 1)[1] if "?" in self.path else ""):
            country = str(self.headers.get("x-vercel-ip-country") or "").upper()[:2]
            return self._send(200, {"ok": True, "country": country or None})
        return self._send(405, {"ok": False})
