"""딜러(매장) 로그인: 계정·비밀번호·로그인 쿠키.

계정: 비공개 Vercel Blob dealer/accounts.json (저장소에는 안 남김). 사장님이 /owner/dealers 에서 만든다.
  {"accounts": {"<아이디>": {"name", "stores": [수집 매장 이름], "country", "lang", "pw", "pv", "disabled", "admin", "created_at", "last_login"}}}
  pw = pbkdf2_sha256$반복$소금$해시. pv = 비밀번호 바꿀 때마다 1씩 올림 (옛 로그인 쿠키를 끊음)
  admin = 사장님 계정: 모든 매장을 골라 볼 수 있음
  stores가 비고 country만 있으면 수집 매장이 없는 딜러 (개인·온라인 판매 — 사장님 본인 등). 모든 매장이 경쟁 매장
로그인 쿠키 cb_dealer: <아이디>.<pv>.<만료 시각>.<서명>. 서명 비밀 값은 환경 변수 DEALER_SESSION_SECRET (32자 이상).
"""
from __future__ import annotations

import base64
import datetime as dt
import hashlib
import hmac
import json
import os
import re
import secrets
import time

KST = dt.timezone(dt.timedelta(hours=9))
COOKIE = "cb_dealer"
SESSION_DAYS = 30
ACCOUNTS_PATH = "dealer/accounts.json"
PBKDF2_ROUNDS = 240_000
ID_RE = re.compile(r"^[a-z0-9][a-z0-9_-]{2,31}$")
MIN_PASSWORD = 10
CACHE_SECONDS = 60
LOCK_AFTER = 5         # 연속 실패 이만큼이면
LOCK_SECONDS = 600     # 이만큼 막음 (함수 인스턴스마다)

_cache: dict = {"at": 0.0, "data": None}
_fails: dict[str, list[float]] = {}


# ── 비밀번호 ──
def hash_password(password: str, *, rounds: int = PBKDF2_ROUNDS) -> str:
    salt = secrets.token_bytes(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, rounds)
    return f"pbkdf2_sha256${rounds}${base64.b64encode(salt).decode()}${base64.b64encode(digest).decode()}"


def check_password(password: str, stored: str) -> bool:
    try:
        algo, rounds, salt, digest = stored.split("$")
        if algo != "pbkdf2_sha256":
            return False
        got = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), base64.b64decode(salt), int(rounds))
        return hmac.compare_digest(got, base64.b64decode(digest))
    except (ValueError, TypeError):
        return False


def new_password() -> str:
    """사장님이 딜러에게 전할 임시 비밀번호. 헷갈리는 글자(0 O 1 l I)는 뺌."""
    alphabet = "abcdefghjkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ23456789"
    return "".join(secrets.choice(alphabet) for _ in range(12))


# ── 로그인 쿠키 ──
def _secret() -> bytes | None:
    value = os.environ.get("DEALER_SESSION_SECRET", "")
    return value.encode() if len(value) >= 32 else None


def _sign(payload: str) -> str:
    return hmac.new(_secret(), payload.encode(), hashlib.sha256).hexdigest()[:32]


def make_session(account_id: str, pv: int, *, now: float | None = None) -> str | None:
    if not _secret():
        return None
    exp = int((now or time.time()) + SESSION_DAYS * 86400)
    payload = f"{account_id}.{pv}.{exp}"
    return f"{payload}.{_sign(payload)}"


def read_session(value: str, *, now: float | None = None) -> tuple[str, int] | None:
    """쿠키가 맞으면 (아이디, pv). 서명·만료만 본다 — 계정이 살아 있는지는 current_account 가 본다."""
    if not value or not _secret():
        return None
    parts = value.split(".")
    if len(parts) != 4:
        return None
    account_id, pv, exp, sig = parts
    if not hmac.compare_digest(sig, _sign(f"{account_id}.{pv}.{exp}")):
        return None
    try:
        if int(exp) < (now or time.time()):
            return None
        return account_id, int(pv)
    except ValueError:
        return None


def session_cookie(value: str) -> str:
    return f"{COOKIE}={value}; Path=/dealer; Max-Age={SESSION_DAYS * 86400}; HttpOnly; Secure; SameSite=Lax"


def clear_cookie() -> str:
    return f"{COOKIE}=; Path=/dealer; Max-Age=0; HttpOnly; Secure; SameSite=Lax"


# ── 계정 저장 (Blob) ──
def _blob():
    from vercel import blob  # noqa: WPS433 (함수가 불릴 때만)
    return blob


def load_accounts(*, fresh: bool = False) -> dict:
    if not fresh and _cache["data"] is not None and time.time() - _cache["at"] < CACHE_SECONDS:
        return _cache["data"]
    try:
        result = _blob().get(ACCOUNTS_PATH, access="private", use_cache=False)
        data = json.loads(result.content)
    except Exception as error:  # noqa: BLE001
        if type(error).__name__ != "BlobNotFoundError":
            raise
        data = {"accounts": {}}
    data.setdefault("accounts", {})
    _cache.update(at=time.time(), data=data)
    return data


def save_accounts(data: dict) -> None:
    _blob().put(ACCOUNTS_PATH, json.dumps(data, ensure_ascii=False, indent=1).encode("utf-8"),
                access="private", content_type="application/json", overwrite=True)
    _cache.update(at=time.time(), data=data)


def current_account(cookie_value: str) -> tuple[str, dict] | None:
    session = read_session(cookie_value)
    if not session:
        return None
    account_id, pv = session
    account = load_accounts()["accounts"].get(account_id)
    if not account or account.get("disabled") or int(account.get("pv", 0)) != pv:
        return None
    return account_id, account


# ── 로그인 ──
def locked(account_id: str, *, now: float | None = None) -> bool:
    now = now or time.time()
    recent = [t for t in _fails.get(account_id, []) if now - t < LOCK_SECONDS]
    _fails[account_id] = recent
    return len(recent) >= LOCK_AFTER


def login(account_id: str, password: str) -> tuple[str, dict] | str:
    """맞으면 (쿠키 값, 계정), 틀리면 오류 코드 문자열."""
    account_id = (account_id or "").strip().lower()
    if not ID_RE.match(account_id) or not password:
        return "wrong"
    if locked(account_id):
        return "locked"
    data = load_accounts(fresh=True)
    account = data["accounts"].get(account_id)
    if not account or account.get("disabled") or not check_password(password, account.get("pw", "")):
        _fails.setdefault(account_id, []).append(time.time())
        return "wrong"
    _fails.pop(account_id, None)
    value = make_session(account_id, int(account.get("pv", 0)))
    if not value:
        return "setup"
    account["last_login"] = dt.datetime.now(KST).isoformat(timespec="minutes")
    try:
        save_accounts(data)
    except Exception:  # noqa: BLE001 (마지막 로그인 기록 실패는 로그인을 막지 않음)
        pass
    return value, account


def change_password(account_id: str, current: str, new: str) -> tuple[str, dict] | str:
    if len(new or "") < MIN_PASSWORD:
        return "short"
    data = load_accounts(fresh=True)
    account = data["accounts"].get(account_id)
    if not account or not check_password(current or "", account.get("pw", "")):
        return "wrong"
    account["pw"] = hash_password(new)
    account["pv"] = int(account.get("pv", 0)) + 1
    save_accounts(data)
    value = make_session(account_id, account["pv"])
    return (value, account) if value else "setup"


# ── 사장님 관리 화면에서 쓰는 것 ──
def create_account(account_id: str, *, name: str, stores: list[str], country: str, lang: str, admin: bool = False) -> str:
    """새 계정을 만들고 임시 비밀번호를 돌려준다. 같은 아이디가 있으면 ValueError."""
    account_id = (account_id or "").strip().lower()
    if not ID_RE.match(account_id):
        raise ValueError("id")
    data = load_accounts(fresh=True)
    if account_id in data["accounts"]:
        raise ValueError("exists")
    if not stores and not admin and not country:
        raise ValueError("stores")
    password = new_password()
    data["accounts"][account_id] = {
        "name": name.strip()[:60] or account_id, "stores": stores, "country": country or None, "lang": lang or None,
        "admin": bool(admin), "pw": hash_password(password), "pv": 0, "disabled": False,
        "created_at": dt.datetime.now(KST).isoformat(timespec="minutes"), "last_login": None,
    }
    save_accounts(data)
    return password


def reset_password(account_id: str) -> str:
    data = load_accounts(fresh=True)
    account = data["accounts"][account_id]
    password = new_password()
    account["pw"] = hash_password(password)
    account["pv"] = int(account.get("pv", 0)) + 1
    save_accounts(data)
    return password


def set_disabled(account_id: str, disabled: bool) -> None:
    data = load_accounts(fresh=True)
    data["accounts"][account_id]["disabled"] = bool(disabled)
    if disabled:
        data["accounts"][account_id]["pv"] = int(data["accounts"][account_id].get("pv", 0)) + 1
    save_accounts(data)


def public_account(account_id: str, account: dict) -> dict:
    """화면에 내려보내는 계정 정보 (비밀번호 해시 빼고)."""
    return {"id": account_id, "name": account.get("name"), "stores": account.get("stores") or [],
            "country": account.get("country"), "lang": account.get("lang"), "admin": bool(account.get("admin"))}
