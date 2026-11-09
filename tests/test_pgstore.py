import json

import pgstore


def test_disabled_without_url(monkeypatch):
    monkeypatch.delenv("DATABASE_URL", raising=False)
    monkeypatch.delenv("POSTGRES_URL", raising=False)
    assert not pgstore.enabled()


def test_usage_goes_to_db_when_connected(monkeypatch):
    calls = []
    monkeypatch.setenv("DATABASE_URL", "postgresql://u:p@ep-x.neon.tech/db?sslmode=require")
    monkeypatch.setattr(pgstore, "_SCHEMA_READY", True)
    monkeypatch.setattr(pgstore, "sql", lambda q, params=None, timeout=8.0: calls.append((q, params)) or [])
    from api import usage
    status, payload = usage.handle({"sid": "dbtest12345", "page": "/"}, "KR", "", "Mozilla/5.0", "1.2.3.4", "Asia/Seoul")
    assert status == 200 and payload["ok"]
    q, params = calls[-1]
    assert q.startswith("INSERT INTO usage_events") and json.loads(params[1])["page"] == "/"


def test_owner_page_reads_from_db(monkeypatch):
    monkeypatch.setenv("DATABASE_URL", "postgresql://u:p@ep-x.neon.tech/db")
    monkeypatch.setattr(pgstore, "_SCHEMA_READY", True)
    rows = [{"entry": json.dumps({"sid": "a1b2c3d4", "part": 1, "created_at": "2026-11-08T10:00:00+09:00", "page": "/", "searches": [], "clicks": []})}]
    monkeypatch.setattr(pgstore, "sql", lambda q, params=None, timeout=8.0: rows if "usage_events" in q else [])
    from api import owner_usage
    entries, feedback, cut = owner_usage.load(7)
    assert entries[0]["sid"] == "a1b2c3d4" and feedback == [] and cut is False


def test_feedback_limit_counts_from_db(monkeypatch):
    monkeypatch.setenv("DATABASE_URL", "postgresql://u:p@ep-x.neon.tech/db")
    monkeypatch.setattr(pgstore, "_SCHEMA_READY", True)
    monkeypatch.setattr(pgstore, "sql", lambda q, params=None, timeout=8.0: [{"n": 5}] if "count" in q else [])
    from api import feedback
    status, payload = feedback.handle({"message": "hello there", "elapsed_ms": 5000}, {})
    assert status == 429 and payload["error"] == "limit"
