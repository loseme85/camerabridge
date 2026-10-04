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
