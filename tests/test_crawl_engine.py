import importlib.util
from pathlib import Path

# app/ 을 sys.path에 넣으면 'import app'이 app/app.py로 잡혀 다른 테스트가 깨짐 → 파일 경로로 불러옴
_spec = importlib.util.spec_from_file_location("crawl_engine", Path(__file__).resolve().parents[1] / "app" / "crawl_engine.py")
ce = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(ce)

T0 = "2026-10-04 09:17:00"
T1 = "2026-10-04 11:17:00"


def _row(n, sold=False, price="1,000,000원", site="장씨카메라", **extra):
    return {"site": site, "링크": f"https://x/{n}", "상품명": f"item {n}", "가격": price, "통화": "KRW", "품절": sold, **extra}


def _run(rows, coverage="active_zone", ok=True, site="장씨카메라"):
    return {"site": site, "ok": ok, "rows": rows, "coverage": coverage}


def _prev(active=12, sold=30):
    return [_row(i, first_seen=T0) for i in range(active)] + [_row(100 + i, sold=True, first_seen=T0, sold_at=T0) for i in range(sold)]


def test_active_zone_keeps_unvisited_sold_archive_and_records_only_changes():
    prev = _prev()
    cur = [_row(i) for i in range(12)] + [_row(999)]  # 신규 1, 판매완료 기록은 안 읽음
    merged, events, stat = ce.merge_source(prev, _run(cur), T1)
    assert stat["status"] == "ok" and len(merged) == 43
    assert [e["type"] for e in events] == ["new"]
    assert next(r for r in merged if r["링크"] == "https://x/0")["first_seen"] == T0
    assert next(r for r in merged if r["링크"] == "https://x/999")["first_seen"] == T1
    assert all("crawl_time" not in r for r in merged)


def test_active_item_that_left_active_zone_becomes_sold_with_time_to_sell():
    prev = _prev()
    cur = [_row(i) for i in range(1, 12)]  # 0번이 판매 중 구간에서 빠짐
    merged, events, _ = ce.merge_source(prev, _run(cur), T1)
    gone = next(r for r in merged if r["링크"] == "https://x/0")
    assert gone["품절"] is True and gone["sold_at"] == T1
    assert events[0]["type"] == "sold" and events[0]["hours_to_sell"] == 2.0


def test_price_change_and_in_place_sold_are_events():
    prev = _prev()
    cur = [_row(0, price="900,000원"), _row(1, sold=True)] + [_row(i) for i in range(2, 12)]
    _, events, _ = ce.merge_source(prev, _run(cur), T1)
    assert sorted(e["type"] for e in events) == ["price", "sold"]
    assert next(e for e in events if e["type"] == "price")["prev_price"] == "1,000,000원"


def test_sudden_drop_keeps_previous_data():
    prev = _prev()
    merged, events, stat = ce.merge_source(prev, _run([_row(i) for i in range(5)]), T1)
    assert stat["status"] == "suspect" and merged == prev and events == []


def test_failed_run_keeps_previous_data():
    prev = _prev()
    merged, events, stat = ce.merge_source(prev, _run([], ok=False), T1)
    assert stat["status"] == "failed" and merged == prev and events == []


def test_full_sweep_waits_one_run_before_marking_gone():
    prev = [_row(i, site="Ffordes", first_seen=T0) for i in range(20)]
    cur = [_row(i, site="Ffordes") for i in range(1, 20)]
    merged, events, _ = ce.merge_source(prev, _run(cur, "full", site="Ffordes"), T1)
    kept = next(r for r in merged if r["링크"] == "https://x/0")
    assert kept["missing_runs"] == 1 and events == []
    merged2, events2, _ = ce.merge_source(merged, _run(cur, "full", site="Ffordes"), "2026-10-04 13:17:00")
    assert all(r["링크"] != "https://x/0" for r in merged2)
    assert [e["type"] for e in events2] == ["gone"]


def test_relisted_item_comes_back_to_sale():
    prev = _prev()
    cur = [_row(i) for i in range(12)] + [_row(100)]
    merged, events, _ = ce.merge_source(prev, _run(cur), T1)
    back = next(r for r in merged if r["링크"] == "https://x/100")
    assert back["품절"] is False and "sold_at" not in back
    assert [e["type"] for e in events] == ["relist"]


def test_full_sweep_schedule():
    fresh = {"장씨카메라": {"last_full": "2026-10-03 10:00:00"}}
    assert ce.needs_full_sweep("장씨카메라", fresh, "2026-10-04 11:00:00")
    assert not ce.needs_full_sweep("장씨카메라", fresh, "2026-10-03 20:00:00")
    assert ce.needs_full_sweep("새 사이트", fresh, T1)


def test_incremental_crawl_stops_after_active_zone():
    pages = {1: [("a1", False), ("a2", False)], 2: [("a3", False), ("s1", True)], 3: [("s2", True), ("s3", True)],
             4: [("s4", True)], 5: [("s5", True)], 6: [("s6", True)]}

    def html(n):
        lis = "".join(f'<li><a href="/p/{k}"><span class="name">{k}</span></a>{"품절" if sold else ""} 1,000원</li>'
                      for k, sold in pages.get(n, []))
        return f'<ul class="prdList">{lis}</ul>'

    class Resp:
        def __init__(self, text):
            self.text = text

        def raise_for_status(self):
            pass

    requested = []

    class Sess:
        headers = {}

        def get(self, url, timeout):
            n = int(url.rsplit("page=", 1)[1])
            requested.append(n)
            return Resp(html(n))

    site = {"name": "테스트", "base": "https://t", "categories": ["https://t/list?c=1"], "통화": "KRW", "active_first": True}
    known = {f"https://t/p/{k}" for k in ("s2", "s3", "s4", "s5", "s6")}
    run = ce.crawl_cafe24_http(site, known, False, lambda n: True, lambda raw, base: raw, lambda p: p, session=Sess(), workers=1)
    assert run["ok"] and run["coverage"] == "active_zone"
    assert max(requested) == 4  # 3·4페이지가 '판매 중 0 + 전부 아는 매물' → 멈춤
    full = ce.crawl_cafe24_http(site, known, True, lambda n: True, lambda raw, base: raw, lambda p: p, session=Sess(), workers=1)
    assert full["coverage"] == "full" and len(full["rows"]) == 9


def test_order_is_stable_when_site_reorders():
    prev = [_row(i, site="Kitamura", first_seen=T0) for i in range(15)]
    cur = [_row(i, site="Kitamura") for i in reversed(range(15))] + [_row(99, site="Kitamura")]
    merged, _, _ = ce.merge_source(prev, _run(cur, "full", site="Kitamura"), T1)
    assert [r["링크"] for r in merged] == ["https://x/99"] + [r["링크"] for r in prev]
