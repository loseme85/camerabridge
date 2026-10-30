"""게시판 (전 세계 이용자 커뮤니티): 글 목록·읽기·쓰기·댓글·지우기·신고 + 운영자 관리 화면.

회원: 구글 로그인 (Google Identity Services ID 토큰 → tokeninfo로 확인). 구글 이메일·이름·사진은 저장하지 않고,
  구글 계정 고유번호(sub)를 비밀 값과 섞은 해시(회원 id)와 닉네임만 board/members/<회원id>.json 에 저장.
  로그인 유지: cb_member 쿠키 <회원id>.<만료>.<서명> (서명 비밀 = BOARD_SESSION_SECRET, 없으면 DEALER_SESSION_SECRET에서 용도를 나눠 만듦)
  환경 변수 GOOGLE_CLIENT_ID (구글 클라우드의 웹 OAuth 클라이언트 ID, 공개 값) 가 있어야 로그인 버튼이 나옴.
저장 위치: Vercel Blob (private), 의견 보내기와 같은 스토어
  board/posts/<글id>~<분류>~<회원id>.json                보이는 글
  board/comments/<글id>/<댓글id>~<회원id>.json            보이는 댓글
  board/held/…                                            신고 HIDE_REPORTS명 이상 → 자동으로 가림 (운영자가 확인 뒤 되살리거나 지움)
  board/removed/…                                         지운 글·댓글 (REMOVED_DAYS일 보관 뒤 운영자가 비움)
  board/reports/<글id>[~<댓글id>]/<접속지태그>.json        신고
스팸 막기: 로그인한 회원만 쓰기, 숨은 입력칸, 쓰기 시작한 지 1.5초 안에 보내면 거절, 회원당 하루 글 POST_LIMIT·댓글 COMMENT_LIMIT건, 링크 MAX_LINKS개까지.
신고는 로그인 없이도 가능 (같은 접속지는 한 번, 접속지 = 날마다 바뀌는 IP 해시).
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
TITLE_LEN, BODY_LEN, COMMENT_LEN, NICK_LEN = (2, 80), (5, 5000), (1, 1000), (1, 20)
POST_LIMIT, COMMENT_LIMIT = 5, 30
MAX_LINKS = 3
MIN_ELAPSED_MS = 1500
HIDE_REPORTS = 3
REMOVED_DAYS = 30
COOKIE = "cb_owner"
MEMBER_COOKIE = "cb_member"
SESSION_DAYS = 90
GOOGLE_ISSUERS = ("accounts.google.com", "https://accounts.google.com")
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


# ── 회원 (구글 로그인) ──
def _secret() -> bytes | None:
    value = os.environ.get("BOARD_SESSION_SECRET") or os.environ.get("DEALER_SESSION_SECRET", "")
    return hashlib.sha256(b"board-session:" + value.encode()).digest() if len(value) >= 32 else None


def _sign(payload: str, secret: bytes) -> str:
    return hmac.new(secret, payload.encode(), hashlib.sha256).hexdigest()[:32]


def session_value(member_id: str, now: float | None = None) -> str:
    secret = _secret()
    expires = int((now or dt.datetime.now().timestamp()) + SESSION_DAYS * 86400)
    payload = f"{member_id}.{expires}"
    return f"{payload}.{_sign(payload, secret)}"


def member_from_cookie(value: str, now: float | None = None) -> str | None:
    secret = _secret()
    parts = str(value or "").split(".")
    if not secret or len(parts) != 3 or not re.fullmatch(r"[0-9a-f]{20}", parts[0]) or not parts[1].isdigit():
        return None
    if int(parts[1]) < (now or dt.datetime.now().timestamp()):
        return None
    return parts[0] if hmac.compare_digest(_sign(f"{parts[0]}.{parts[1]}", secret), parts[2]) else None


def verify_google(credential: str) -> str | None:
    """구글 ID 토큰을 구글 tokeninfo로 확인 → 계정 고유번호(sub). 우리 클라이언트 ID로 발급된 토큰만."""
    client_id = os.environ.get("GOOGLE_CLIENT_ID", "")
    if not client_id or not credential or len(credential) > 4096:
        return None
    try:
        info = requests.get("https://oauth2.googleapis.com/tokeninfo", params={"id_token": credential}, timeout=8).json()
    except (requests.RequestException, ValueError):
        return None
    if info.get("aud") != client_id or info.get("iss") not in GOOGLE_ISSUERS or not info.get("sub"):
        return None
    if int(info.get("exp") or 0) < dt.datetime.now().timestamp():
        return None
    return str(info["sub"])


def _member_id(sub: str) -> str:
    return hmac.new(_secret(), f"google:{sub}".encode(), hashlib.sha256).hexdigest()[:20]


def _member(blob, member_id: str | None) -> dict | None:
    return _read(blob, f"board/members/{member_id}.json") if member_id else None


def login(body: dict) -> tuple[int, dict, str | None]:
    if not _secret():
        return 503, {"ok": False, "error": "unavailable"}, None
    sub = verify_google(str(body.get("credential") or ""))
    if not sub:
        return 401, {"ok": False, "error": "login"}, None
    member_id = _member_id(sub)
    blob = _blob()
    member = _member(blob, member_id)
    if not member:
        member = {"id": member_id, "nick": None, "created_at": _now()[0].isoformat(timespec="seconds")}
        _put(blob, f"board/members/{member_id}.json", member)
    return 200, {"ok": True, "member": {"nick": member.get("nick")}}, session_value(member_id)


def set_nick(body: dict, member_id: str | None) -> tuple[int, dict]:
    blob = _blob()
    member = _member(blob, member_id)
    if not member:
        return 401, {"ok": False, "error": "login"}
    nick = _clean(body.get("nick"), NICK_LEN[1]).replace("\n", " ")
    if not (NICK_LEN[0] <= len(nick) <= NICK_LEN[1]):
        return 400, {"ok": False, "error": "nick"}
    _put(blob, f"board/members/{member_id}.json", {**member, "nick": nick})
    return 200, {"ok": True, "member": {"nick": nick}}


def me(member_id: str | None) -> dict:
    member = _member(_blob(), member_id) if member_id else None
    return {"ok": True, "client_id": os.environ.get("GOOGLE_CLIENT_ID") or None,
            "member": {"nick": member.get("nick")} if member else None}


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


def _public(entry: dict, member_id: str | None = None) -> dict:
    """밖으로 보내는 칸만 (회원 id는 내보내지 않고, 내 글인지만 mine으로)."""
    row = {k: entry.get(k) for k in ("id", "post_id", "category", "title", "body", "nick", "created_at", "locale")
           if entry.get(k) is not None}
    if member_id and entry.get("member") == member_id:
        row["mine"] = True
    return row


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


def _writer(blob, member_id: str | None) -> tuple[dict | None, str]:
    member = _member(blob, member_id)
    if not member:
        return None, "login"
    if not member.get("nick"):
        return None, "nick"
    return member, ""


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


def read_post(post_id: str, member_id: str | None = None) -> tuple[int, dict]:
    blob = _blob()
    item = _find_post(blob, post_id)
    entry = _read(blob, item) if item else None
    if not entry:
        return 404, {"ok": False, "error": "not_found"}
    comment_items = sorted(_names(blob, f"board/comments/{post_id}/"), key=lambda i: i.pathname)
    comments = [_public(c, member_id) for c in _read_many(blob, comment_items) if c]
    return 200, {"ok": True, "post": _public(entry, member_id), "comments": comments}


# ── 쓰기 ──
def create_post(body: dict, member_id: str | None) -> tuple[int, dict]:
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
    blob = _blob()
    member, error = _writer(blob, member_id)
    if not member:
        return 401 if error == "login" else 400, {"ok": False, "error": error}
    now, stamp, _ = _now()
    today = stamp[:8]
    mine = [i for i in _names(blob, f"board/posts/{today}") + _names(blob, f"board/held/{today}") if i.pathname.endswith(f"~{member_id}.json")]
    if len(mine) >= POST_LIMIT:
        return 429, {"ok": False, "error": "limit"}
    entry = {"id": _new_id(stamp), "created_at": now.isoformat(timespec="seconds"), "category": category, "title": title,
             "body": text, "nick": member["nick"], "member": member_id, "locale": str(body.get("locale") or "")[:12] or None}
    _put(blob, f"board/posts/{entry['id']}~{category}~{member_id}.json", entry)
    _notify(f"📝 게시판 새 글 ({category})\n\n{title}\n{text[:500]}\n\n— {member['nick']}\nhttps://camerabridge.io/#board/{entry['id']}")
    return 200, {"ok": True, "id": entry["id"]}


def create_comment(body: dict, member_id: str | None) -> tuple[int, dict]:
    blocked = _check_human(body)
    if blocked:
        return blocked
    post_id = str(body.get("post_id") or "")
    text = _clean(body.get("body"), COMMENT_LEN[1])
    if not (COMMENT_LEN[0] <= len(text) <= COMMENT_LEN[1]):
        return 400, {"ok": False, "error": "body"}
    if len(LINK.findall(text)) > MAX_LINKS:
        return 400, {"ok": False, "error": "links"}
    blob = _blob()
    member, error = _writer(blob, member_id)
    if not member:
        return 401 if error == "login" else 400, {"ok": False, "error": error}
    if not _find_post(blob, post_id):
        return 404, {"ok": False, "error": "not_found"}
    now, stamp, _ = _now()
    today = stamp[:8]
    mine = [i for i in _names(blob, "board/comments/") if i.pathname.split("/")[-1].startswith(today) and i.pathname.endswith(f"~{member_id}.json")]
    if len(mine) >= COMMENT_LIMIT:
        return 429, {"ok": False, "error": "limit"}
    entry = {"id": _new_id(stamp), "post_id": post_id, "created_at": now.isoformat(timespec="seconds"), "body": text,
             "nick": member["nick"], "member": member_id, "locale": str(body.get("locale") or "")[:12] or None}
    _put(blob, f"board/comments/{post_id}/{entry['id']}~{member_id}.json", entry)
    return 200, {"ok": True, "id": entry["id"]}


def _target(blob, post_id: str, comment_id: str = ""):
    if comment_id:
        if not ID.match(comment_id or "") or not ID.match(post_id or ""):
            return None
        items = _names(blob, f"board/comments/{post_id}/{comment_id}~")
        return items[0] if items else None
    return _find_post(blob, post_id)


def delete_entry(body: dict, member_id: str | None) -> tuple[int, dict]:
    """글쓴이(로그인한 그 회원)가 지움 → board/removed 로 옮김 (글이면 댓글도 같이)."""
    blob = _blob()
    post_id, comment_id = str(body.get("post_id") or ""), str(body.get("comment_id") or "")
    item = _target(blob, post_id, comment_id)
    entry = _read(blob, item) if item else None
    if not entry:
        return 404, {"ok": False, "error": "not_found"}
    if not member_id or not hmac.compare_digest(str(entry.get("member") or ""), member_id):
        return 403, {"ok": False, "error": "not_yours"}
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

    def _cookie(self, name: str) -> str:
        cookie = SimpleCookie(self.headers.get("cookie") or "")
        return cookie[name].value if name in cookie else ""

    def _owner(self) -> bool:
        return authorized(self._cookie(COOKIE))

    def _member_id(self) -> str | None:
        return member_from_cookie(self._cookie(MEMBER_COOKIE))

    def do_GET(self):  # noqa: N802
        query = self._query()
        try:
            if query.get("r") == "owner":
                if not self._owner():
                    return self._send(401, "<!doctype html><meta charset=utf-8><p>권한이 없습니다. /owner/usage?key=… 로 먼저 들어가 주세요.</p>", "text/html; charset=utf-8")
                return self._send(200, owner_page(), "text/html; charset=utf-8", extra={"x-robots-tag": "noindex, nofollow"})
            if query.get("r") == "me":
                return self._send(200, me(self._member_id()))
            if query.get("id"):  # 내 글 표시(mine) 때문에 캐시하지 않음
                status, payload = read_post(query["id"], self._member_id())
                return self._send(status, payload)
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
            member_id = self._member_id()
            if action == "login":
                status, payload, session = login(body)
                cookie = (f"{MEMBER_COOKIE}={session}; Path=/api/board; Max-Age={SESSION_DAYS * 86400}; HttpOnly; Secure; SameSite=Lax"
                          if session else None)
                return self._send(status, payload, extra={"set-cookie": cookie} if cookie else None)
            if action == "logout":
                return self._send(200, {"ok": True}, extra={"set-cookie": f"{MEMBER_COOKIE}=; Path=/api/board; Max-Age=0; HttpOnly; Secure; SameSite=Lax"})
            if action == "nick":
                status, payload = set_nick(body, member_id)
            elif action == "post":
                status, payload = create_post(body, member_id)
            elif action == "comment":
                status, payload = create_comment(body, member_id)
            elif action == "delete":
                status, payload = delete_entry(body, member_id)
            elif action == "report":
                status, payload = report(body, self.headers)
            else:
                status, payload = 400, {"ok": False, "error": "action"}
            return self._send(status, payload)
        except Exception:  # noqa: BLE001
            return self._send(503, {"ok": False, "error": "unavailable"})
