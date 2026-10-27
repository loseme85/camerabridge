import json
import time

import pytest

import dealer_portal as portal
from api import dealer, owner_dealers


class FakeBlob:
    """vercel.blob 대신 메모리에 저장."""

    class NotFound(Exception):
        pass

    def __init__(self):
        self.files = {}

    def get(self, path, access="public", use_cache=True):
        if path not in self.files:
            raise type("BlobNotFoundError", (Exception,), {})()
        return type("R", (), {"content": self.files[path]})()

    def put(self, path, body, access="public", content_type=None, overwrite=False):
        self.files[path] = body


@pytest.fixture
def blob(monkeypatch):
    fake = FakeBlob()
    monkeypatch.setattr(portal, "_blob", lambda: fake)
    monkeypatch.setattr(portal, "PBKDF2_ROUNDS", 1000)
    monkeypatch.setenv("DEALER_SESSION_SECRET", "s" * 40)
    portal._cache.update(at=0.0, data=None)
    portal._fails.clear()
    return fake


def test_password_hash_roundtrip():
    stored = portal.hash_password("correct horse", rounds=1000)
    assert portal.check_password("correct horse", stored)
    assert not portal.check_password("wrong horse", stored)
    assert not portal.check_password("x", "garbage")
    assert len(portal.new_password()) == 12


def test_session_needs_secret_and_rejects_tampering(monkeypatch):
    monkeypatch.delenv("DEALER_SESSION_SECRET", raising=False)
    assert portal.make_session("shop", 0) is None
    monkeypatch.setenv("DEALER_SESSION_SECRET", "short")
    assert portal.make_session("shop", 0) is None
    monkeypatch.setenv("DEALER_SESSION_SECRET", "s" * 40)
    value = portal.make_session("shop", 3)
    assert portal.read_session(value) == ("shop", 3)
    assert portal.read_session(value.replace("shop", "other")) is None
    assert portal.read_session(value, now=time.time() + 31 * 86400) is None
    monkeypatch.setenv("DEALER_SESSION_SECRET", "t" * 40)
    assert portal.read_session(value) is None


def test_create_login_and_disable(blob):
    password = portal.create_account("chungmuro", name="라이카스토어 충무로", stores=["라이카스토어 충무로"], country="KR", lang="ko")
    saved = json.loads(blob.files[portal.ACCOUNTS_PATH])["accounts"]["chungmuro"]
    assert password not in json.dumps(saved) and saved["pw"].startswith("pbkdf2_sha256$")

    assert portal.login("chungmuro", "nope") == "wrong"
    value, account = portal.login("ChungMuro ", password)
    assert account["stores"] == ["라이카스토어 충무로"]
    assert portal.current_account(value)[0] == "chungmuro"

    portal.set_disabled("chungmuro", True)
    assert portal.current_account(value) is None
    assert portal.login("chungmuro", password) == "wrong"


def test_password_change_ends_old_sessions(blob):
    password = portal.create_account("ffordes", name="Ffordes", stores=["Ffordes (영국)"], country="GB", lang="en")
    old, _ = portal.login("ffordes", password)
    assert portal.change_password("ffordes", password, "short") == "short"
    assert portal.change_password("ffordes", "wrong", "a-long-new-password") == "wrong"
    new, _ = portal.change_password("ffordes", password, "a-long-new-password")
    assert portal.current_account(old) is None
    assert portal.current_account(new)[0] == "ffordes"
    assert portal.login("ffordes", "a-long-new-password") != "wrong"


def test_lock_after_repeated_failures(blob):
    portal.create_account("shop1", name="", stores=["사진집"], country="KR", lang="ko")
    for _ in range(portal.LOCK_AFTER):
        assert portal.login("shop1", "bad") == "wrong"
    assert portal.login("shop1", "anything") == "locked"


def test_create_account_validation(blob):
    with pytest.raises(ValueError, match="id"):
        portal.create_account("A B", name="", stores=["사진집"], country="KR", lang="ko")
    with pytest.raises(ValueError, match="stores"):
        portal.create_account("nostore", name="", stores=[], country="KR", lang="ko")
    portal.create_account("dup", name="", stores=["사진집"], country="KR", lang="ko")
    with pytest.raises(ValueError, match="exists"):
        portal.create_account("dup", name="", stores=["사진집"], country="KR", lang="ko")
    assert "pw" not in portal.public_account("dup", json.loads(blob.files[portal.ACCOUNTS_PATH])["accounts"]["dup"])


def test_app_page_embeds_account_without_secrets(tmp_path, monkeypatch):
    page = tmp_path / "dealer.html"
    page.write_text("<body><!--ME--></body>")
    monkeypatch.setattr(dealer, "PAGE", page)
    html = dealer.app_page("shop", {"name": "</script><b>", "stores": ["사진집"], "pw": "pbkdf2_sha256$1$a$b", "pv": 2}).decode()
    assert "pbkdf2" not in html and "</script><b>" not in html
    me = json.loads(html.split("window.ME = ")[1].split(";</script>")[0])
    assert me == {"id": "shop", "name": "</script><b>", "stores": ["사진집"], "country": None, "lang": None, "admin": False}


def test_pick_lang_and_login_page_escapes():
    assert dealer.pick_lang("de", "ko-KR") == "de"
    assert dealer.pick_lang(None, "ja-JP,ja;q=0.9") == "ja"
    assert dealer.pick_lang(None, "zh-TW") == "zh-Hant"
    assert dealer.pick_lang(None, "zh-CN") == "zh-Hans"
    assert dealer.pick_lang(None, "") == "en"
    page = dealer.login_page("ko", "wrong", '"><script>')
    assert "<script>" not in page and "아이디나 비밀번호가 맞지 않습니다" in page
    for lang in dealer.LANGS:
        assert set(dealer.T[lang]) == set(dealer.T["en"])


def test_owner_create_shows_password_once(blob):
    sites = {"라이카스토어 충무로": {"country": "KR", "act": 10}, "Ffordes (영국)": {"country": "GB", "act": 5}}
    notice, error = owner_dealers.handle_post({"do": ["create"], "id": ["ffordes"], "name": ["Ffordes"], "stores": ["Ffordes (영국)", "없는 매장"]}, sites)
    assert not error and "임시 비밀번호" in notice
    account = json.loads(blob.files[portal.ACCOUNTS_PATH])["accounts"]["ffordes"]
    assert account["stores"] == ["Ffordes (영국)"] and account["country"] == "GB" and account["lang"] == "en"
    page = owner_dealers.render(portal.load_accounts()["accounts"], sites)
    assert "ffordes" in page and "pbkdf2" not in page
    _, error = owner_dealers.handle_post({"do": ["reset"], "id": ["nobody"]}, sites)
    assert error == owner_dealers.ERRORS["missing"]
