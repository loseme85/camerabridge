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


def test_render_counts_visits_by_country():
    from api import owner_usage as ou
    entries = [{"sid": "a1b2c3d4", "part": 1, "created_at": "2026-10-29T10:00:00+09:00", "country": "JP", "searches": [{"q": "m6"}], "clicks": []},
               {"sid": "z9y8x7w6", "part": 1, "created_at": "2026-10-29T11:00:00+09:00", "searches": [{"q": "m3"}], "clicks": []}]
    page = ou.render(entries, [], 1, False)
    assert "나라별 방문" in page and "🇯🇵 일본" in page and "기록 전" in page


def test_model_page_visits_show_source_and_landing():
    from api import owner_usage as ou
    landing = "/?utm_source=model_page&utm_content=m6"
    entries = [{"sid": "m0d3lp4g", "part": 1, "created_at": "2026-10-29T19:00:00+09:00", "referrer": None, "landing": landing,
                "searches": [{"q": "m6"}], "clicks": []}]
    page = ou.render(entries, [], 1, False)
    assert "카메라브릿지 모델 페이지" in page and "utm_content=m6" in page


def test_referrer_groups_and_details():
    from api import owner_usage as ou
    assert ou._ref_name("www.google.co.kr") == "구글 검색"
    assert ou._ref_name("m.search.naver.com") == "네이버"
    assert ou._ref_name("www.reddit.com/r/Leica/comments/abc") == "레딧"
    assert ou._ref_name("t.co") == "X(트위터)" and ou._ref_name("www.tistory.com") == "www.tistory.com"
    assert ou._ref_detail("www.google.com") == "구글 검색"
    assert ou._ref_detail("www.reddit.com/r/Leica/comments/abc") == "www.reddit.com/r/Leica/comments/abc"


def test_browse_only_visits_are_counted_with_pages():
    from api import owner_usage as ou
    entries = [
        {"sid": "v1s1t0nly", "part": 1, "created_at": "2026-11-07T10:00:00+09:00", "page": "/ko/leica/m6/",
         "referrer": "www.google.com", "landing": "/ko/leica/m6/", "searches": [], "clicks": [{"host": "ffordes.com", "s": 20}]},
        {"sid": "v1s1t0nly", "part": 2, "created_at": "2026-11-07T10:01:00+09:00", "page": "/",
         "referrer": "www.google.com", "landing": "/ko/leica/m6/", "searches": [{"q": "m6", "s": 40}], "clicks": []},
        {"sid": "r3dd1tv1", "part": 1, "created_at": "2026-11-07T11:00:00+09:00", "page": "/",
         "referrer": "www.reddit.com/r/Leica/comments/abc", "landing": "/", "searches": [], "clicks": []},
    ]
    v = next(v for v in ou.visits(entries) if v["referrer"] == "www.google.com")
    assert [k for k, _ in v["steps"]] == ["페이지", "페이지", "클릭", "검색"]
    page = ou.render(entries, [], 1, False)
    assert "www.reddit.com/r/Leica/comments/abc" in page and "구글 검색" in page and "/ko/leica/m6/" in page
    from scripts import usage_report
    r = usage_report.summarize(entries)
    assert r["visits"] == 2 and r["visits_with_activity"] == 1


def test_search_via_and_day_view():
    import datetime as dt
    from api import owner_usage as ou
    from api import usage
    from scripts import usage_report
    today = dt.datetime.now(ou.KST).date().isoformat()
    entries = [{"sid": "typ3dv1s1t", "part": 1, "created_at": f"{today}T10:00:00+09:00", "page": "/", "referrer": "www.reddit.com/r/Leica/comments/x",
                "searches": [{"q": "Leica M6", "via": "pick", "typed": "m6 ttl", "results": 5, "active": 3, "s": 4},
                             {"q": "noctilux", "via": "typed", "results": 9, "active": 2, "s": 30},
                             {"q": "Leica M3", "via": "link", "results": 4, "active": 4, "s": 50}], "clicks": []}]
    r = usage_report.summarize(entries)
    assert dict(r["typed_queries"]) == {"m6 ttl": 1, "noctilux": 1}
    assert dict(r["opened_models"]) == {"Leica M3": 1}
    week = ou.render(entries, [], 7, False)
    assert f"?date={today}" in week and "날짜별" in week and "손님이 직접 친 검색어" in week
    day = ou.render(entries, [], 7, False, today)
    assert "◀ 전날" in day and "“m6 ttl” 치고" in day and "링크로 열림" in day
    kept = usage.clean({"sid": "abcd1234efgh", "searches": [{"q": "m6", "via": "hack", "typed": "x"}]})
    assert "via" not in kept["searches"][0]


def test_same_ip_same_day_counts_once(monkeypatch):
    import sys
    import types
    from api import usage, owner_usage as ou
    from scripts import usage_report
    saved = []
    monkeypatch.setenv("USAGE_SALT", "s3cret")
    monkeypatch.setitem(sys.modules, "vercel", types.SimpleNamespace(blob=types.SimpleNamespace(put=lambda path, data, **kw: saved.append(data))))
    usage.handle({"sid": "tab0ne1234", "page": "/"}, "KR", "", "Mozilla/5.0", "1.2.3.4, 10.0.0.1")
    usage.handle({"sid": "tabtw05678", "page": "/ko/leica/m6/"}, "KR", "", "Mozilla/5.0", "1.2.3.4")
    import json
    a, b = (json.loads(x) for x in saved)
    assert a["vtag"] == b["vtag"] and "1.2.3.4" not in saved[0].decode()
    assert usage.visitor_tag("1.2.3.4", "2026-11-07") != usage.visitor_tag("1.2.3.4", "2026-11-08")
    r = usage_report.summarize([a, b])
    assert r["visits"] == 1
    assert len(ou.visits([a, b])) == 1
