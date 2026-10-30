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
    return fake, sent


def _ip(n: int) -> dict:
    return {"x-forwarded-for": f"203.0.113.{n}"}


POST = {"action": "post", "category": "question", "title": "M6 셔터 소리", "body": "M6 셔터 소리가 원래 이런가요?",
        "nick": "필름러", "password": "pass1234", "elapsed_ms": 5000, "locale": "ko"}


def test_post_list_read_comment_without_account(monkeypatch):
    fake, sent = _setup(monkeypatch)
    status, out = board.create_post(POST, _ip(1))
    assert status == 200 and out["ok"]
    post_id = out["id"]
    assert board.create_comment({"post_id": post_id, "body": "네 원래 그래요", "nick": "라이카", "password": "abcd",
                                 "elapsed_ms": 4000}, _ip(2))[0] == 200
    listed = board.list_posts()
    assert listed["total"] == 1 and listed["posts"][0]["comments"] == 1 and "body" not in listed["posts"][0]
    assert board.list_posts("free")["total"] == 0 and board.list_posts("question")["total"] == 1
    status, read = board.read_post(post_id)
    assert status == 200 and read["post"]["title"] == "M6 셔터 소리" and read["comments"][0]["nick"] == "라이카"
    dump = json.dumps(read, ensure_ascii=False)
    assert "pass1234" not in json.dumps(fake.store) and '"pw"' not in dump and '"salt"' not in dump  # 비밀번호·해시는 밖으로 안 나감
    assert "203.0.113" not in json.dumps(fake.store)  # IP는 저장하지 않음
    assert len(sent) == 1


def test_bots_bad_input_and_daily_limit(monkeypatch):
    fake, _ = _setup(monkeypatch)
    assert board.create_post({**POST, "website": "spam"}, _ip(1)) == (200, {"ok": True})
    assert board.create_post({**POST, "elapsed_ms": 500}, _ip(1))[0] == 429
    assert board.create_post({**POST, "category": "sale"}, _ip(1))[1]["error"] == "category"
    assert board.create_post({**POST, "title": "x"}, _ip(1))[1]["error"] == "title"
    assert board.create_post({**POST, "password": "12"}, _ip(1))[1]["error"] == "password"
    assert board.create_post({**POST, "body": "a http://x.co b http://y.co c http://z.co d http://w.co"}, _ip(1))[1]["error"] == "links"
    assert fake.store == {}
    for _ in range(board.POST_LIMIT):
        assert board.create_post(POST, _ip(1))[0] == 200
    assert board.create_post(POST, _ip(1))[1]["error"] == "limit"
    assert board.create_post(POST, _ip(9))[0] == 200  # 다른 접속지는 따로 셈


def test_author_deletes_with_password(monkeypatch):
    fake, _ = _setup(monkeypatch)
    post_id = board.create_post(POST, _ip(1))[1]["id"]
    board.create_comment({"post_id": post_id, "body": "댓글", "nick": "a", "password": "abcd", "elapsed_ms": 4000}, _ip(2))
    assert board.delete_entry({"post_id": post_id, "password": "wrong-pw"})[0] == 403
    assert board.delete_entry({"post_id": post_id, "password": "pass1234"})[0] == 200
    assert board.list_posts()["total"] == 0 and board.read_post(post_id)[0] == 404
    assert all(k.startswith("board/removed/") for k in fake.store)  # 글·댓글 모두 지운 칸으로 (운영자 30일 보관)


def test_three_reports_hide_post_until_owner_restores(monkeypatch):
    fake, sent = _setup(monkeypatch)
    post_id = board.create_post(POST, _ip(1))[1]["id"]
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
