import importlib.util
import json
import sys
import types
from pathlib import Path

_spec = importlib.util.spec_from_file_location("feedback_api", Path(__file__).resolve().parents[1] / "api" / "feedback.py")
fb = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(fb)


class FakeBlob:
    def __init__(self):
        self.store = {}

    def list_objects(self, prefix=None, limit=None):
        items = [types.SimpleNamespace(pathname=k) for k in self.store if k.startswith(prefix or "")]
        return types.SimpleNamespace(blobs=items)

    def put(self, path, body, access="public", content_type=None):
        assert access == "private"
        self.store[path] = json.loads(body)


def _setup(monkeypatch):
    fake = FakeBlob()
    vercel_mod = types.ModuleType("vercel")
    vercel_mod.blob = fake
    monkeypatch.setitem(sys.modules, "vercel", vercel_mod)
    sent = []
    monkeypatch.setattr(fb, "_notify", lambda entry: sent.append(entry))
    return fake, sent


HEADERS = {"x-forwarded-for": "203.0.113.7"}


def test_valid_feedback_is_stored_privately_and_notified(monkeypatch):
    fake, sent = _setup(monkeypatch)
    status, out = fb.handle({"message": "시세 알림 기능이 있으면 좋겠어요", "email": "a@b.co", "locale": "ko", "elapsed_ms": 4000}, HEADERS)
    assert status == 200 and out["ok"]
    (entry,) = fake.store.values()
    assert entry["message"].startswith("시세") and entry["public"] is False and entry["status"] == "new"
    assert "203.0.113.7" not in json.dumps(fake.store)  # IP는 저장하지 않음
    assert len(sent) == 1


def test_bots_and_bad_input_are_rejected(monkeypatch):
    fake, sent = _setup(monkeypatch)
    assert fb.handle({"message": "hello there", "website": "spam", "elapsed_ms": 5000}, HEADERS) == (200, {"ok": True})
    assert fb.handle({"message": "hello there", "elapsed_ms": 200}, HEADERS)[0] == 429
    assert fb.handle({"message": "hi", "elapsed_ms": 5000}, HEADERS)[0] == 400
    assert fb.handle({"message": "hello there", "email": "nope", "elapsed_ms": 5000}, HEADERS)[0] == 400
    assert fake.store == {} and sent == []


def test_daily_limit_per_visitor(monkeypatch):
    fake, _ = _setup(monkeypatch)
    for _ in range(fb.DAILY_LIMIT):
        assert fb.handle({"message": "idea number", "elapsed_ms": 3000}, HEADERS)[0] == 200
    assert fb.handle({"message": "one more idea", "elapsed_ms": 3000}, HEADERS)[0] == 429
    assert fb.handle({"message": "other person", "elapsed_ms": 3000}, {"x-forwarded-for": "198.51.100.2"})[0] == 200
