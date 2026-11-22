import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from cafe24_dedupe import dedupe_by_product_no  # noqa: E402

BASE = "https://leica-storebando.co.kr/product/x/{no}/category/{cat}/display/1/"


def item(no, cat, sold=False, reserved=False):
    return {"링크": BASE.format(no=no, cat=cat), "품절": sold, "예약중": reserved}


def test_same_product_in_two_categories_is_kept_once_with_first_link():
    out = dedupe_by_product_no([item(1, 442), item(2, 442), item(1, 436)])
    assert [r["링크"] for r in out] == [BASE.format(no=1, cat=442), BASE.format(no=2, cat=442)]


def test_active_in_either_category_means_active():
    out = dedupe_by_product_no([item(1, 442, sold=True), item(1, 436, sold=False, reserved=True)])
    assert len(out) == 1 and out[0]["품절"] is False and out[0]["예약중"] is True


def test_links_without_product_number_are_kept():
    rows = [{"링크": "https://a/x"}, {"링크": "https://a/y"}]
    assert dedupe_by_product_no(rows) == rows


def test_primary_category_link_wins_even_if_it_comes_second():
    out = dedupe_by_product_no([item(1, 436), item(1, 442)])
    assert len(out) == 1 and out[0]["링크"] == BASE.format(no=1, cat=442)


def test_merge_source_quietly_cleans_old_duplicate_records():
    sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "app"))
    import crawl_engine as ce

    site = "라이카스토어 충무로"
    prev = [dict(item(n, c), site=site, 상품명=f"p{n}", 가격="1", first_seen="2026-11-01 00:00:00") for n in range(1, 40) for c in (442, 436)]
    run = {"site": site, "ok": True, "coverage": "active_zone",
           "rows": [dict(item(n, c), site=site, 상품명=f"p{n}", 가격="1") for n in range(1, 40) for c in (442, 436)]}
    merged, events, stat = ce.merge_source(prev, run, "2026-11-22 12:00:00")
    assert len(merged) == 39
    assert all("/category/442/" in r["링크"] for r in merged)
    assert not events and stat["status"] == "ok"
