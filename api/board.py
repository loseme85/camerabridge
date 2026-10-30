"""게시판 (전 세계 이용자 커뮤니티): 글 목록·읽기·쓰기·댓글·지우기·신고 + 운영자 관리 화면.

회원 가입 없음: 닉네임 + 글 비밀번호(복원할 수 없는 해시로 저장)로 쓰고, 같은 비밀번호로 지운다.
저장 위치: Vercel Blob (private), 의견 보내기와 같은 스토어
  board/posts/<글id>~<분류>~<접속지태그>.json            보이는 글
  board/comments/<글id>/<댓글id>~<접속지태그>.json        보이는 댓글
  board/held/…                                            신고 HIDE_REPORTS명 이상 → 자동으로 가림 (운영자가 확인 뒤 되살리거나 지움)
  board/removed/…                                         지운 글·댓글 (REMOVED_DAYS일 보관 뒤 운영자가 비움)
  board/reports/<글id>[~<댓글id>]/<접속지태그>.json        신고
스팸 막기: 숨은 입력칸, 창을 연 지 3초 안에 보내면 거절, 같은 접속지(IP 해시, 날마다 바뀜) 하루 글 POST_LIMIT·댓글 COMMENT_LIMIT건, 링크 MAX_LINKS개까지.
운영자 관리: /owner/board (cb_owner 쿠키 = OWNER_DASHBOARD_KEY, /owner/usage?key=… 로 한 번 들어가면 생김)
"""
from __future__ import annotations

import datetime as dt
import hashlib
import hmac
import html
import json
import os
import re
import secrets
from concurrent.futures import ThreadPoolExecutor
from http.cookies import SimpleCookie
from http.server import BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse

import requests

KST = dt.timezone(dt.timedelta(hours=9))
CATEGORIES = ("free", "question", "review", "site")  # 자유 · 질문 · 정보·후기 · 사이트 의견
PAGE_SIZE = 20
TITLE_LEN, BODY_LEN, COMMENT_LEN, NICK_LEN, PW_LEN = (2, 80), (5, 5000), (1, 1000), (1, 20), (4, 40)
POST_LIMIT, COMMENT_LIMIT = 5, 30
MAX_LINKS = 3
MIN_ELAPSED_MS = 3000
HIDE_REPORTS = 3
REMOVED_DAYS = 30
COOKIE = "cb_owner"
LINK = re.compile(r"https?://|www\.", re.I)
ID = re.compile(r"^\d{14}-[0-9a-f]{6}$")
STAMP = re.compile(r"(\d{14})-[0-9a-f]{6}")


# ── 공통 ──
def _client_ip(headers) -> str:
    forwarded = headers.get("x-forwarded-for") or headers.get("x-real-ip") or ""
    return forwarded.split(",")[0].strip()


def _tag(headers, day: str) -> str:
    """접속지 태그: 날마다 바뀌는 소금을 섞은 IP 해시 (IP 자체는 남기지 않음)."""
    salt = os.environ.get("FEEDBACK_SALT", "camerabridge")
    return hashlib.sha256(f"{salt}:board:{day}:{_client_ip(headers)}".encode()).hexdigest()[:12]


def _hash_pw(password: str, salt: str) -> str:
    return hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), 120_000).hex()


def _clean(text, limit: int) -> str:
    text = re.sub(r"[\u0000-\u0008\u000b\u000c\u000e-\u001f\u007f]", "", str(text or ""))
    text = re.sub(r"[ \t]+\n", "\n", text.replace("\r\n", "\n")).strip()
    return re.sub(r"\n{4,}", "\n\n\n", text)[:limit + 1]


def _now():
    now = dt.datetime.now(KST)
    return now, now.strftime("%Y%m%d%H%M%S"), now.strftime("%Y-%m-%d")


def _new_id(stamp: str) -> str:
    return f"{stamp}-{secrets.token_hex(3)}"


def _blob():
    from vercel import blob  # noqa: WPS433 (함수가 불릴 때만)
    return blob


def _names(blob, prefix: str) -> list:
    try:
        return list(blob.iter_objects(prefix=prefix))
    except Exception:  # noqa: BLE001
        return []


def _read(blob, item) -> dict | None:
    try:
        return json.loads(blob.get(item.url if hasattr(item, "url") else item, access="private", use_cache=False).content)
    except Exception:  # noqa: BLE001
        return None


def _read_many(blob, items) -> list:
    with ThreadPoolExecutor(max_workers=8) as pool:
        return list(pool.map(lambda item: _read(blob, item), items))


def _put(blob, path: str, entry: dict) -> None:
    blob.put(path, json.dumps(entry, ensure_ascii=False).encode("utf-8"), access="private",
             content_type="application/json", overwrite=True)


def _move(blob, item, to_prefix: str, entry: dict | None = None) -> None:
    """글·댓글을 다른 칸(held/removed/posts)으로 옮김: 새 자리에 쓰고 옛 자리를 지움."""
    entry = entry if entry is not None else _read(blob, item)
    rest = item.pathname.split("/", 2)[2]
    _put(blob, f"board/{to_prefix}/{rest}", entry or {})
    blob.delete(item.url)


def _notify(text: str) -> None:
    token, chat = os.environ.get("TELEGRAM_BOT_TOKEN"), os.environ.get("TELEGRAM_CHAT_ID")
    if not token or not chat:
        return
    try:
        requests.post(f"https://api.telegram.org/bot{token}/sendMessage",
                      json={"chat_id": chat, "text": text[:4000], "disable_web_page_preview": True}, timeout=8)
    except requests.RequestException:
        pass


def _public(entry: dict) -> dict:
    return {k: entry.get(k) for k in ("id", "post_id", "category", "title", "body", "nick", "created_at", "locale")
            if entry.get(k) is not None}


def _check_human(body: dict) -> tuple[int, dict] | None:
    if str(body.get("website") or "").strip():  # 숨은 칸: 사람은 비워 둠
        return 200, {"ok": True}
    try:
        elapsed = int(body.get("elapsed_ms") or 0)
    except (TypeError, ValueError):
        elapsed = 0
    if elapsed < MIN_ELAPSED_MS:
        return 429, {"ok": False, "error": "too_fast"}
    return None


def _author(body: dict) -> tuple[str, str] | tuple[None, str]:
    nick = _clean(body.get("nick"), NICK_LEN[1]).replace("\n", " ")
    password = str(body.get("password") or "")
    if not (NICK_LEN[0] <= len(nick) <= NICK_LEN[1]):
        return None, "nick"
    if not (PW_LEN[0] <= len(password) <= PW_LEN[1]):
        return None, "password"
    return nick, password


def _find_post(blob, post_id: str, where: str = "posts"):
    if not ID.match(post_id or ""):
        return None
    items = _names(blob, f"board/{where}/{post_id}~")
    return items[0] if items else None


# ── 읽기 ──
def list_posts(category: str = "", page: int = 1) -> dict:
    blob = _blob()
    items = [i for i in _names(blob, "board/posts/") if not category or f"~{category}~" in i.pathname]
    items.sort(key=lambda i: i.pathname, reverse=True)
    pages = max(1, -(-len(items) // PAGE_SIZE))
    page = max(1, min(page, pages))
    chosen = items[(page - 1) * PAGE_SIZE: page * PAGE_SIZE]
    counts: dict[str, int] = {}
    for item in _names(blob, "board/comments/"):
        post_id = item.pathname.split("/")[2]
        counts[post_id] = counts.get(post_id, 0) + 1
    posts = []
    for entry in _read_many(blob, chosen):
        if entry:
            row = _public(entry)
            row.pop("body", None)
            row["comments"] = counts.get(entry["id"], 0)
            posts.append(row)
    return {"ok": True, "posts": posts, "page": page, "pages": pages, "total": len(items)}


def read_post(post_id: str) -> tuple[int, dict]:
    blob = _blob()
    item = _find_post(blob, post_id)
    entry = _read(blob, item) if item else None
    if not entry:
        return 404, {"ok": False, "error": "not_found"}
    comment_items = sorted(_names(blob, f"board/comments/{post_id}/"), key=lambda i: i.pathname)
    comments = [_public(c) for c in _read_many(blob, comment_items) if c]
    return 200, {"ok": True, "post": _public(entry), "comments": comments}


# ── 쓰기 ──
def create_post(body: dict, headers) -> tuple[int, dict]:
    blocked = _check_human(body)
    if blocked:
        return blocked
    category = str(body.get("category") or "")
    if category not in CATEGORIES:
        return 400, {"ok": False, "error": "category"}
    title = _clean(body.get("title"), TITLE_LEN[1]).replace("\n", " ")
    text = _clean(body.get("body"), BODY_LEN[1])
    if not (TITLE_LEN[0] <= len(title) <= TITLE_LEN[1]):
        return 400, {"ok": False, "error": "title"}
    if not (BODY_LEN[0] <= len(text) <= BODY_LEN[1]):
        return 400, {"ok": False, "error": "body"}
    if len(LINK.findall(title + " " + text)) > MAX_LINKS:
        return 400, {"ok": False, "error": "links"}
    nick, password = _author(body)
    if not nick:
        return 400, {"ok": False, "error": password}
    blob = _blob()
    now, stamp, day = _now()
    tag = _tag(headers, day)
    today = stamp[:8]
    mine = [i for i in _names(blob, f"board/posts/{today}") + _names(blob, f"board/held/{today}") if i.pathname.endswith(f"~{tag}.json")]
    if len(mine) >= POST_LIMIT:
        return 429, {"ok": False, "error": "limit"}
    salt = secrets.token_hex(8)
    entry = {"id": _new_id(stamp), "created_at": now.isoformat(timespec="seconds"), "category": category, "title": title,
             "body": text, "nick": nick, "salt": salt, "pw": _hash_pw(password, salt), "locale": str(body.get("locale") or "")[:12] or None}
    _put(blob, f"board/posts/{entry['id']}~{category}~{tag}.json", entry)
    _notify(f"📝 게시판 새 글 ({category})\n\n{title}\n{text[:500]}\n\n— {nick}\nhttps://camerabridge.io/#board/{entry['id']}")
    return 200, {"ok": True, "id": entry["id"]}


def create_comment(body: dict, headers) -> tuple[int, dict]:
    blocked = _check_human(body)
    if blocked:
        return blocked
    post_id = str(body.get("post_id") or "")
    text = _clean(body.get("body"), COMMENT_LEN[1])
    if not (COMMENT_LEN[0] <= len(text) <= COMMENT_LEN[1]):
        return 400, {"ok": False, "error": "body"}
    if len(LINK.findall(text)) > MAX_LINKS:
        return 400, {"ok": False, "error": "links"}
    nick, password = _author(body)
    if not nick:
        return 400, {"ok": False, "error": password}
    blob = _blob()
    if not _find_post(blob, post_id):
        return 404, {"ok": False, "error": "not_found"}
    now, stamp, day = _now()
    tag = _tag(headers, day)
    today = stamp[:8]
    mine = [i for i in _names(blob, "board/comments/") if i.pathname.split("/")[-1].startswith(today) and i.pathname.endswith(f"~{tag}.json")]
    if len(mine) >= COMMENT_LIMIT:
        return 429, {"ok": False, "error": "limit"}
    salt = secrets.token_hex(8)
    entry = {"id": _new_id(stamp), "post_id": post_id, "created_at": now.isoformat(timespec="seconds"), "body": text,
             "nick": nick, "salt": salt, "pw": _hash_pw(password, salt)}
    _put(blob, f"board/comments/{post_id}/{entry['id']}~{tag}.json", entry)
    return 200, {"ok": True, "id": entry["id"]}


def _target(blob, post_id: str, comment_id: str = ""):
    if comment_id:
        if not ID.match(comment_id or "") or not ID.match(post_id or ""):
            return None
        items = _names(blob, f"board/comments/{post_id}/{comment_id}~")
        return items[0] if items else None
    return _find_post(blob, post_id)


def delete_entry(body: dict) -> tuple[int, dict]:
    """글쓴이가 비밀번호로 지움 → board/removed 로 옮김 (댓글도 같이)."""
    blob = _blob()
    post_id, comment_id = str(body.get("post_id") or ""), str(body.get("comment_id") or "")
    item = _target(blob, post_id, comment_id)
    entry = _read(blob, item) if item else None
    if not entry:
        return 404, {"ok": False, "error": "not_found"}
    if not hmac.compare_digest(_hash_pw(str(body.get("password") or ""), entry.get("salt", "")), entry.get("pw", "")):
        return 403, {"ok": False, "error": "password"}
    _move(blob, item, "removed", {**entry, "removed_at": _now()[0].isoformat(timespec="seconds"), "removed_by": "author"})
    if not comment_id:
        for comment in _names(blob, f"board/comments/{post_id}/"):
            _move(blob, comment, "removed")
    return 200, {"ok": True}


def report(body: dict, headers) -> tuple[int, dict]:
    """신고: 같은 접속지는 한 번만. HIDE_REPORTS명이 신고하면 board/held 로 옮겨 가림."""
    blob = _blob()
    post_id, comment_id = str(body.get("post_id") or ""), str(body.get("comment_id") or "")
    item = _target(blob, post_id, comment_id)
    if not item:
        return 404, {"ok": False, "error": "not_found"}
    _, _, day = _now()
    key = f"{post_id}~{comment_id}" if comment_id else post_id
    reason = _clean(body.get("reason"), 200)
    _put(blob, f"board/reports/{key}/{_tag(headers, day)}.json", {"reason": reason, "day": day})
    count = len(_names(blob, f"board/reports/{key}/"))
    hidden = count >= HIDE_REPORTS
    if hidden:
        _move(blob, item, "held")
    _notify(f"🚩 게시판 신고 {count}건{' → 자동으로 가림' if hidden else ''}\n{item.pathname}\n{reason}\nhttps://camerabridge.io/owner/board")
    return 200, {"ok": True, "hidden": hidden}


# ── 운영자 ──
def authorized(cookie_value: str) -> bool:
    expected = os.environ.get("OWNER_DASHBOARD_KEY", "")
    return len(expected) >= 16 and bool(cookie_value) and hmac.compare_digest(cookie_value, expected)


def owner_action(form: dict) -> None:
    """hold(가리기) · restore(되살리기) · remove(지우기) · purge(지운 지 REMOVED_DAYS일 지난 것 비우기)."""
    blob = _blob()
    action, path = form.get("action", ""), form.get("path", "")
    if action == "purge":  # 지운 날 기준이 아니라 글·댓글을 쓴 날 기준 (지운 날은 파일 안에만 있음)
        cutoff = (dt.datetime.now(KST) - dt.timedelta(days=REMOVED_DAYS)).strftime("%Y%m%d")
        old = [i.url for i in _names(blob, "board/removed/") if (STAMP.findall(i.pathname) or ["99999999"])[-1][:8] < cutoff]
        if old:
            blob.delete(old)
        return
    if not path.startswith(("board/posts/", "board/comments/", "board/held/")):
        return
    items = [i for i in _names(blob, path) if i.pathname == path]
    if not items:
        return
    is_comment = "/" in path.split("/", 2)[2]  # 댓글은 <글id>/<댓글id>, 글은 <글id>~…
    to = {"hold": "held", "remove": "removed", "restore": "comments" if is_comment else "posts"}.get(action)
    if to:
        _move(blob, items[0], to)


def owner_page() -> str:
    blob = _blob()
    held = sorted(_names(blob, "board/held/"), key=lambda i: i.pathname, reverse=True)[:50]
    recent = sorted(_names(blob, "board/posts/"), key=lambda i: i.pathname, reverse=True)[:30]
    comments = sorted(_names(blob, "board/comments/"), key=lambda i: i.pathname.split("/")[-1], reverse=True)[:30]
    reports: dict[str, int] = {}
    for item in _names(blob, "board/reports/"):
        reports[item.pathname.split("/")[2]] = reports.get(item.pathname.split("/")[2], 0) + 1

    def rows(items, buttons):
        entries = _read_many(blob, items)
        out = []
        for item, entry in zip(items, entries):
            entry = entry or {}
            key = f"{entry.get('post_id')}~{entry.get('id')}" if entry.get("post_id") else entry.get("id", "")
            forms = "".join(f'<form method="post"><input type="hidden" name="action" value="{a}"><input type="hidden" name="path" value="{html.escape(item.pathname)}"><button>{label}</button></form>'
                            for a, label in buttons)
            out.append(f"<tr><td>{html.escape(entry.get('created_at', '')[:16])}</td><td>{html.escape(entry.get('nick', ''))}</td>"
                       f"<td><b>{html.escape(entry.get('title', ''))}</b> {html.escape((entry.get('body') or '')[:300])}</td>"
                       f"<td>{reports.get(key, 0)}</td><td class=act>{forms}</td></tr>")
        return "".join(out) or '<tr><td colspan=5>없음</td></tr>'

    head = "<tr><th>시각</th><th>닉네임</th><th>내용</th><th>신고</th><th></th></tr>"
    return ("<!doctype html><html lang=ko><meta charset=utf-8><meta name=robots content=noindex><title>게시판 관리</title>"
            "<style>body{font:14px/1.5 -apple-system,sans-serif;margin:24px;color:#16181a}table{border-collapse:collapse;width:100%;margin-bottom:28px}"
            "td,th{border-bottom:1px solid #ddd;padding:6px 8px;text-align:left;vertical-align:top}.act form{display:inline}button{margin-right:4px}</style>"
            "<h1>게시판 관리</h1><p>신고 3명이면 자동으로 가려져 아래 '가려진 글'에 옵니다. 지운 글은 30일 보관 뒤 비웁니다.</p>"
            f"<h2>가려진 글·댓글 ({len(held)})</h2><table>{head}{rows(held, [('restore', '되살리기'), ('remove', '지우기')])}</table>"
            f"<h2>최근 글</h2><table>{head}{rows(recent, [('hold', '가리기'), ('remove', '지우기')])}</table>"
            f"<h2>최근 댓글</h2><table>{head}{rows(comments, [('hold', '가리기'), ('remove', '지우기')])}</table>"
            '<form method="post"><input type="hidden" name="action" value="purge"><button>지운 지 30일 지난 것 비우기</button></form>')


class handler(BaseHTTPRequestHandler):
    def _send(self, status: int, payload, content_type: str = "application/json", cache: str = "no-store", extra: dict | None = None) -> None:
        body = payload if isinstance(payload, bytes) else (payload.encode() if isinstance(payload, str) else json.dumps(payload, ensure_ascii=False).encode())
        self.send_response(status)
        self.send_header("content-type", content_type)
        self.send_header("cache-control", cache)
        for name, value in (extra or {}).items():
            self.send_header(name, value)
        self.end_headers()
        self.wfile.write(body)

    def _query(self) -> dict:
        return {k: v[0] for k, v in parse_qs(urlparse(self.path).query).items()}

    def _owner(self) -> bool:
        cookie = SimpleCookie(self.headers.get("cookie") or "")
        return authorized(cookie[COOKIE].value if COOKIE in cookie else "")

    def do_GET(self):  # noqa: N802
        query = self._query()
        try:
            if query.get("r") == "owner":
                if not self._owner():
                    return self._send(401, "<!doctype html><meta charset=utf-8><p>권한이 없습니다. /owner/usage?key=… 로 먼저 들어가 주세요.</p>", "text/html; charset=utf-8")
                return self._send(200, owner_page(), "text/html; charset=utf-8", extra={"x-robots-tag": "noindex, nofollow"})
            if query.get("id"):
                status, payload = read_post(query["id"])
                return self._send(status, payload, cache="public, s-maxage=15, stale-while-revalidate=60")
            try:
                page = int(query.get("page") or 1)
            except ValueError:
                page = 1
            category = query.get("category") if query.get("category") in CATEGORIES else ""
            return self._send(200, list_posts(category, page), cache="public, s-maxage=15, stale-while-revalidate=60")
        except Exception:  # noqa: BLE001
            return self._send(503, {"ok": False, "error": "unavailable"})

    def do_POST(self):  # noqa: N802
        length = min(int(self.headers.get("content-length") or 0), 32_000)
        raw = self.rfile.read(length) or b""
        query = self._query()
        try:
            if query.get("r") == "owner":
                if not self._owner():
                    return self._send(401, "권한이 없습니다.", "text/plain; charset=utf-8")
                owner_action({k: v[0] for k, v in parse_qs(raw.decode()).items()})
                return self._send(303, b"", "text/plain", extra={"location": "/owner/board"})
            try:
                body = json.loads(raw or b"{}")
            except ValueError:
                return self._send(400, {"ok": False, "error": "bad_json"})
            if not isinstance(body, dict):
                return self._send(400, {"ok": False, "error": "bad_request"})
            action = body.get("action")
            if action == "post":
                status, payload = create_post(body, self.headers)
            elif action == "comment":
                status, payload = create_comment(body, self.headers)
            elif action == "delete":
                status, payload = delete_entry(body)
            elif action == "report":
                status, payload = report(body, self.headers)
            else:
                status, payload = 400, {"ok": False, "error": "action"}
            return self._send(status, payload)
        except Exception:  # noqa: BLE001
            return self._send(503, {"ok": False, "error": "unavailable"})
