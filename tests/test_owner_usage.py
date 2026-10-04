from api import owner_usage

ENTRIES = [
    {"sid": "a", "part": 1, "created_at": "2026-10-05T10:00:00+09:00", "referrer": "www.reddit.com", "locale": "en", "mobile": True,
     "duration_s": 40, "searches": [{"q": "leica m6", "entity": "leica:body:m6", "results": 12, "active": 3, "s": 3}], "clicks": []},
    {"sid": "a", "part": 2, "created_at": "2026-10-05T10:01:00+09:00", "referrer": "www.reddit.com", "locale": "en", "mobile": True,
     "duration_s": 75, "searches": [], "clicks": [{"host": "www.ffordes.com", "s": 70}]},
    {"sid": "b", "part": 1, "created_at": "2026-10-05T11:00:00+09:00", "referrer": None, "locale": "ko", "mobile": False,
     "duration_s": 20, "searches": [{"q": "<script>x</script>", "results": 0, "s": 5}], "clicks": []},
]


def test_authorized_needs_long_key(monkeypatch):
    monkeypatch.setenv("OWNER_DASHBOARD_KEY", "short")
    assert not owner_usage.authorized("short", "")
    monkeypatch.setenv("OWNER_DASHBOARD_KEY", "x" * 32)
    assert owner_usage.authorized("", "x" * 32)
    assert not owner_usage.authorized("wrong", "")
    monkeypatch.delenv("OWNER_DASHBOARD_KEY")
    assert not owner_usage.authorized("", "")


def test_visits_group_parts_in_order():
    visits = owner_usage.visits(ENTRIES)
    a = next(v for v in visits if v["referrer"] == "www.reddit.com")
    assert [kind for kind, _ in a["steps"]] == ["검색", "클릭"]
    assert a["duration_s"] == 75


def test_render_escapes_queries_and_names_referrers():
    page = owner_usage.render(ENTRIES, [{"created_at": "2026-10-05T12:00:00+09:00", "message": "<b>hi</b>"}], 7, False)
    assert "<script>x</script>" not in page and "&lt;script&gt;" in page
    assert "레딧" in page and "결과 없음" in page and "&lt;b&gt;hi" in page
