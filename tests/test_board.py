import importlib.util
import json
import sys
import types
from pathlib import Path

_spec = importlib.util.spec_from_file_location("board_api", Path(__file__).resolve().parents[1] / "api" / "board.py")
board = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(board)


class FakeBlob:
    def __init__(self):
        self.store = {}

    def iter_objects(self, prefix=None, **_):
        return [types.SimpleNamespace(pathname=k, url=k) for k in sorted(self.store) if k.startswith(prefix or "")]

    def get(self, url, access="public", use_cache=True):
        assert access == "private"
        return types.SimpleNamespace(content=json.dumps(self.store[url]).encode())

    def put(self, path, body, access="public", content_type=None, overwrite=False):
        assert access == "private"
        self.store[path] = json.loads(body)

    def delete(self, urls):
        for url in [urls] if isinstance(urls, str) else urls:
            self.store.pop(url, None)


def _setup(monkeypatch):
    fake = FakeBlob()
    vercel_mod = types.ModuleType("vercel")
    vercel_mod.blob = fake
    monkeypatch.setitem(sys.modules, "vercel", vercel_mod)
    sent = []
    monkeypatch.setattr(board, "_notify", lambda text: sent.append(text))
    monkeypatch.setenv("DEALER_SESSION_SECRET", "s" * 40)
    monkeypatch.setenv("GOOGLE_CLIENT_ID", "cid.apps.googleusercontent.com")
    monkeypatch.setattr(board, "verify_google", lambda credential: {"tok-a": "sub-a", "tok-b": "sub-b"}.get(credential))
    return fake, sent


def _join(credential: str, nick: str) -> str:
    """구글 로그인 → 쿠키에서 회원 id → 닉네임 정하기."""
    status, out, session = board.login({"credential": credential})
    assert status == 200
    member_id = board.member_from_cookie(session)
    assert board.set_nick({"nick": nick}, member_id)[0] == 200
    return member_id


def _ip(n: int) -> dict:
    return {"x-forwarded-for": f"203.0.113.{n}"}


POST = {"action": "post", "category": "question", "title": "M6 셔터 소리", "body": "M6 셔터 소리가 원래 이런가요?", "elapsed_ms": 5000, "locale": "ko"}


def test_google_member_posts_and_comments_without_password(monkeypatch):
    fake, sent = _setup(monkeypatch)
    a = _join("tok-a", "필름러")
    b = _join("tok-b", "라이카")
    status, out = board.create_post(POST, a)
    assert status == 200
    post_id = out["id"]
    assert board.create_comment({"post_id": post_id, "body": "네 원래 그래요", "elapsed_ms": 4000}, b)[0] == 200
    listed = board.list_posts()
    assert listed["total"] == 1 and listed["posts"][0]["comments"] == 1 and listed["posts"][0]["nick"] == "필름러"
    status, read = board.read_post(post_id, a)
    assert read["post"].get("mine") is True and "mine" not in read["comments"][0]
    dump = json.dumps(read, ensure_ascii=False) + json.dumps(listed, ensure_ascii=False)
    assert a not in dump and "sub-a" not in dump  # 회원 id·구글 번호는 밖으로 안 나감
    assert "sub-a" not in json.dumps(fake.store)  # 구글 번호 자체는 저장 안 함 (해시만)
    assert len(sent) == 1


def test_login_needed_and_nick_needed(monkeypatch):
    _setup(monkeypatch)
    assert board.create_post(POST, None) == (401, {"ok": False, "error": "login"})
    assert board.login({"credential": "forged"})[0] == 401
    status, out, session = board.login({"credential": "tok-a"})
    member_id = board.member_from_cookie(session)
    assert out["member"]["nick"] is None
    assert board.create_post(POST, member_id)[1]["error"] == "nick"  # 닉네임 먼저
    assert board.set_nick({"nick": ""}, member_id)[0] == 400
    assert board.me(member_id)["member"] == {"nick": None} and board.me(None)["client_id"] == "cid.apps.googleusercontent.com"


def test_session_cookie_is_signed_and_expires(monkeypatch):
    _setup(monkeypatch)
    value = board.session_value("a" * 20, now=1_000)
    assert board.member_from_cookie(value, now=2_000) == "a" * 20
    assert board.member_from_cookie(value, now=1_000 + 91 * 86400) is None  # 90일 뒤 만료
    assert board.member_from_cookie(value.replace("a" * 20, "b" * 20), now=2_000) is None  # 서명 위조
    monkeypatch.delenv("DEALER_SESSION_SECRET")
    assert board.member_from_cookie(value, now=2_000) is None and board.login({"credential": "tok-a"})[0] == 503


def test_bad_input_and_daily_limit(monkeypatch):
    fake, _ = _setup(monkeypatch)
    a = _join("tok-a", "필름러")
    assert board.create_post({**POST, "website": "spam"}, a) == (200, {"ok": True})
    assert board.create_post({**POST, "elapsed_ms": 500}, a)[0] == 429
    assert board.create_post({**POST, "category": "sale"}, a)[1]["error"] == "category"
    assert board.create_post({**POST, "title": "x"}, a)[1]["error"] == "title"
    assert board.create_post({**POST, "body": "a http://x.co b http://y.co c http://z.co d http://w.co"}, a)[1]["error"] == "links"
    for _ in range(board.POST_LIMIT):
        assert board.create_post(POST, a)[0] == 200
    assert board.create_post(POST, a)[1]["error"] == "limit"
    assert board.create_post(POST, _join("tok-b", "다른사람"))[0] == 200  # 회원마다 따로 셈


def test_only_author_deletes(monkeypatch):
    fake, _ = _setup(monkeypatch)
    a, b = _join("tok-a", "필름러"), _join("tok-b", "라이카")
    post_id = board.create_post(POST, a)[1]["id"]
    board.create_comment({"post_id": post_id, "body": "댓글", "elapsed_ms": 4000}, b)
    assert board.delete_entry({"post_id": post_id}, b)[0] == 403
    assert board.delete_entry({"post_id": post_id}, None)[0] == 403
    assert board.delete_entry({"post_id": post_id}, a)[0] == 200
    assert board.list_posts()["total"] == 0 and board.read_post(post_id)[0] == 404
    assert all(k.startswith(("board/removed/", "board/members/")) for k in fake.store)


def test_three_reports_hide_post_until_owner_restores(monkeypatch):
    fake, _ = _setup(monkeypatch)
    post_id = board.create_post(POST, _join("tok-a", "필름러"))[1]["id"]
    assert board.report({"post_id": post_id, "reason": "광고"}, _ip(5))[1]["hidden"] is False
    board.report({"post_id": post_id}, _ip(5))  # 같은 접속지는 한 번으로
    assert board.report({"post_id": post_id}, _ip(6))[1]["hidden"] is False
    assert board.report({"post_id": post_id}, _ip(7))[1]["hidden"] is True
    assert board.list_posts()["total"] == 0
    (held,) = [k for k in fake.store if k.startswith("board/held/")]
    board.owner_action({"action": "restore", "path": held})
    assert board.list_posts()["total"] == 1


def test_owner_needs_key(monkeypatch):
    monkeypatch.setenv("OWNER_DASHBOARD_KEY", "k" * 20)
    assert board.authorized("k" * 20) and not board.authorized("") and not board.authorized("nope")
    monkeypatch.setenv("OWNER_DASHBOARD_KEY", "short")
    assert not board.authorized("short")
