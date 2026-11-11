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
    # 같은 sid가 자정을 넘어도 하나. 서로 다른 브라우저는 같은 IP여도 별개.
    assert summarize([event(), event(day="2026-11-12")])["visits"] == 1
    assert summarize([event(vid=None), event(sid="oldtab02", vid=None)])["visits"] == 1


def test_history_does_not_use_dashboard_date_or_row_limit(monkeypatch):
    calls = []
    monkeypatch.setattr(pgstore, "_SCHEMA_READY", True)
    def sql(query, params=None):
        calls.append((query, params))
        return [{"vid": BROWSER, "visits": "5", "first_seen": "2026-10-01T12:00:00+09:00",
                 "last_seen": "2026-11-11T12:00:00+09:00"}]
    monkeypatch.setattr(pgstore, "sql", sql)
    monkeypatch.setattr(pgstore, "enabled", lambda: True)
    history = owner_usage.load_browser_history([event()])
    assert history[BROWSER]["visits"] == 5
    query, params = calls[0]
    assert "COUNT(DISTINCT entry->>'sid')" in query and "LIMIT" not in query
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
