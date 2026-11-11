"""브라우저 재방문: 수집·중복 전송·과거 이력·기존 기록·집계 장애 회귀 검사."""
import json

import pgstore
from api import owner_usage, usage
from scripts.usage_report import summarize

BROWSER = "a" * 32
OTHER = "b" * 32


def event(sid="visit001", vid=BROWSER, day="2026-11-11", **extra):
    return {"sid": sid, "vid": vid, "created_at": f"{day}T12:00:00+09:00", "page": "/",
            "part": 1, "vtag": "same-network", "searches": [], "clicks": [], **extra}


def test_validated_browser_id_reaches_storage_without_raw_ip(monkeypatch):
    saved = []
    monkeypatch.setattr(pgstore, "enabled", lambda: True)
    monkeypatch.setattr(pgstore, "add_usage", saved.append)
    assert usage.handle(event(), ip="1.2.3.4")[1]["ok"]
    assert saved[0]["vid"] == BROWSER
    assert "1.2.3.4" not in json.dumps(saved)
    for invalid in ["<script>", "a" * 31, "a" * 33, "a" * 32 + "\n", [BROWSER], 1, None]:
        assert usage.clean(event(vid=invalid))["vid"] is None
    assert usage.handle(event(), cookie="cb_skip_usage=1")[1]["skipped"]
    assert usage.handle(event(), agent="Googlebot")[1]["skipped"]
    assert len(saved) == 1


def test_visits_distinguish_browsers_and_sessions_but_not_repeat_events():
    rows = [event(), event(part=2, page="/ko/leica/m6/"), event(),
            event(sid="visit002", day="2026-11-12"), event(vid=OTHER)]
    assert summarize(rows)["visits"] == 3
    visits = owner_usage.visits(rows)
    assert len(visits) == 3 and {v["vid"] for v in visits} == {BROWSER, OTHER}
    # 같은 탭도 30분 이상 비면 새 방문. 서로 다른 브라우저는 같은 IP여도 별개.
    assert summarize([event(), event(day="2026-11-12")])["visits"] == 2
    assert summarize([event(vid=None), event(sid="oldtab02", vid=None)])["visits"] == 1


def test_history_does_not_use_dashboard_date_or_row_limit(monkeypatch):
    calls = []
    monkeypatch.setattr(pgstore, "_SCHEMA_READY", True)
    def sql(query, params=None):
        calls.append((query, params))
        return [{"vid": BROWSER, "first_seen": f"{day}T12:00:00+09:00",
                 "last_seen": f"{day}T12:00:00+09:00"}
                for day in ("2026-10-01", "2026-10-11", "2026-10-21", "2026-11-01", "2026-11-11")]
    monkeypatch.setattr(pgstore, "sql", sql)
    monkeypatch.setattr(pgstore, "enabled", lambda: True)
    history = owner_usage.load_browser_history([event()])
    assert history[BROWSER]["visits"] == 5
    query, params = calls[0]
    assert "LAG(" in query and "INTERVAL '30 minutes'" in query and "LIMIT" not in query
    assert params == [[BROWSER]] and "- 364" in query
    page = owner_usage.render([event()], [], 1, False, "2026-11-11", history)
    assert "누적 5회" in page and "첫 방문 2026-10-01" in page and "최근 방문 2026-11-11" in page
    assert "브라우저 aaaaaaaa" in page and "최근 365일" in page


def test_missing_identity_and_history_failure_are_not_claimed_first_visits(monkeypatch):
    page = owner_usage.render([event(vid=None)], [], 7, False)
    assert "재방문 식별 없음" in page and "누적 1회" not in page
    monkeypatch.setattr(pgstore, "enabled", lambda: False)
    assert owner_usage.load_browser_history([event()]) is None
    monkeypatch.setattr(pgstore, "enabled", lambda: True)
    def failed(_):
        raise OSError("database unavailable")
    monkeypatch.setattr(pgstore, "browser_history", failed)
    assert owner_usage.load_browser_history([event()]) is None
    page = owner_usage.render([event()], [], 7, False)
    assert "누적 집계 확인 불가" in page and "누적 1회" not in page
    assert owner_usage.load_browser_history([event(vid=None)]) == {}


def test_simultaneous_tabs_and_reload_are_one_visit():
    rows = [event(sid=f"tab0000{i}", part=i + 1) for i in range(4)]
    assert summarize(rows)["visits"] == 1
    assert len(owner_usage.visits(rows)) == 1
    assert len({e["sid"] for e in rows}) == 4  # 원본 기록은 바꾸지 않음


def test_thirty_minute_gap_is_between_records_not_fixed_time_buckets():
    rows = [event(sid=f"tab{i:05d}", created_at=f"2026-11-11T{time}+09:00")
            for i, time in enumerate(("12:00:00", "12:29:00", "12:58:00", "13:28:00"))]
    assert summarize(rows)["visits"] == 2  # 29분씩 이어진 앞의 세 기록은 한 방문
    assert len(owner_usage.visits(list(reversed(rows)))) == 2
    assert summarize([event(), event(vid=OTHER)])["visits"] == 2


def test_session_continues_across_midnight_and_offsets():
    rows = [event(created_at="2026-11-11T23:59:00+09:00"),
            event(sid="newtab02", created_at="2026-11-12T00:01:00+09:00"),
            event(sid="newtab03", created_at="2026-11-11T15:02:00Z")]
    assert summarize(rows)["visits"] == 1


def test_full_history_keeps_session_together_when_filter_hides_middle_record():
    from scripts.usage_report import group_visits, visitor_key
    spans = [{"first_seen": "2026-11-11T12:00:00+09:00", "last_seen": "2026-11-11T13:00:00+09:00"}]
    history = {BROWSER: {"visits": 1, **spans[0], "sessions": spans}}
    # 12:20·12:40 중간 기록이 조회 상한으로 빠져도 전체 이력의 구간을 사용.
    rows = [event(), event(sid="tab00002", created_at="2026-11-11T13:00:00+09:00")]
    grouped = group_visits(rows, history)
    assert len({visitor_key(e) for e in grouped}) == 1
    assert summarize(grouped)["visits"] == 1
    assert len(owner_usage.visits(grouped)) == 1


def test_browser_first_and_last_are_shown_once_in_separate_table():
    rows = [event(), event(sid="tab00002", created_at="2026-11-11T14:00:00+09:00")]
    spans = [{"first_seen": e["created_at"], "last_seen": e["created_at"]} for e in rows]
    history = {BROWSER: {"visits": 2, "first_seen": spans[0]["first_seen"],
                         "last_seen": spans[-1]["last_seen"], "sessions": spans}}
    page = owner_usage.render(rows, [], 1, False, history=history)
    assert page.count("누적 2회") == 1
    assert page.count("첫 방문 2026-11-11") == 1
    assert page.count("최근 방문 2026-11-11") == 1
    assert page.count(f'href="#browser-{BROWSER}"') == 2
    assert "한 브라우저 = 한 줄" in page
