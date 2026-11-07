from api import usage
from scripts import usage_report


def test_clean_rejects_bad_session_and_empty_visits():
    assert usage.clean({"sid": "x", "searches": [{"q": "m6"}]}) is None
    assert usage.clean({"sid": "abcd1234efgh", "searches": [], "clicks": []}) is None


def test_clean_trims_and_keeps_only_known_fields():
    entry = usage.clean({
        "sid": "abcd1234efgh", "ip": "1.2.3.4", "email": "a@b.c",
        "searches": [{"q": "  leica   m6 ", "entity": "m6", "results": "12", "active": 3, "s": 5, "extra": 1}, {"q": ""}],
        "clicks": [{"host": "www.kitamura.jp", "s": 9}],
        "referrer": "www.reddit.com",
    })
    assert entry["searches"] == [{"q": "leica m6", "entity": "m6", "results": 12, "active": 3, "s": 5}]
    assert entry["clicks"][0]["host"] == "www.kitamura.jp"
    assert "ip" not in entry and "email" not in entry


def test_summarize_counts_zero_results_and_referrers():
    entries = [
        {"sid": "a", "part": 1, "referrer": "www.reddit.com", "searches": [{"q": "Steel Rim", "results": 0}], "clicks": []},
        {"sid": "a", "part": 2, "referrer": "www.reddit.com", "searches": [{"q": "m6", "entity": "m6", "results": 5, "active": 0}], "clicks": [{"host": "ffordes.com"}]},
        {"sid": "b", "part": 1, "referrer": None, "searches": [{"q": "steel  rim", "results": 0}], "clicks": []},
    ]
    report = usage_report.summarize(entries)
    assert report["visits_with_activity"] == 2
    assert report["visits_with_click"] == 1
    assert report["zero_result_queries"] == [("steel rim", 2)]
    assert report["no_active_queries"] == [("m6", 1)]
    assert dict(report["referrers"])["www.reddit.com"] == 1


def test_handle_keeps_only_country_code(monkeypatch):
    import sys
    import types
    import api.usage as usage
    saved = {}
    fake = types.SimpleNamespace(put=lambda path, data, **kw: saved.update(data=data))
    monkeypatch.setitem(sys.modules, "vercel", types.SimpleNamespace(blob=fake))
    body = {"sid": "abcdefgh12", "searches": [{"q": "m6"}]}
    assert usage.handle(dict(body), "kr")[1]["ok"]
    assert b'"country": "KR"' in saved["data"]
    usage.handle(dict(body), "1.2.3.4")
    assert b"country" not in saved["data"]


def test_owner_browser_is_not_logged(monkeypatch):
    import sys
    import types
    import api.usage as usage
    saved = []
    fake = types.SimpleNamespace(put=lambda path, data, **kw: saved.append(path))
    monkeypatch.setitem(sys.modules, "vercel", types.SimpleNamespace(blob=fake))
    body = {"sid": "abcdefgh12", "searches": [{"q": "m6"}]}
    assert usage.handle(dict(body), "KR", "cb_skip_usage=1")[1]["skipped"]
    assert saved == []
    usage.handle(dict(body), "KR", "other=1")
    assert len(saved) == 1


def test_owner_usage_page_marks_browser_to_skip():
    import api.owner_usage as owner
    assert "Path=/api/usage" in owner.SKIP_USAGE_COOKIE and owner.SKIP_USAGE_COOKIE.startswith("cb_skip_usage=1")


def test_browse_only_visit_with_page_is_kept_and_bots_skipped(monkeypatch):
    import sys
    import types
    entry = usage.clean({"sid": "abcd1234efgh", "page": "/ko/leica/m6/", "referrer": "www.reddit.com/r/Leica/comments/abc"})
    assert entry["page"] == "/ko/leica/m6/" and entry["referrer"].endswith("/comments/abc")
    saved = []
    monkeypatch.setitem(sys.modules, "vercel", types.SimpleNamespace(blob=types.SimpleNamespace(put=lambda path, data, **kw: saved.append(path))))
    body = {"sid": "abcdefgh12", "page": "/"}
    assert usage.handle(dict(body), "KR", "", "Mozilla/5.0 (compatible; Googlebot/2.1)")[1]["skipped"]
    assert saved == []
    usage.handle(dict(body), "KR", "", "Mozilla/5.0 (iPhone)")
    assert len(saved) == 1
