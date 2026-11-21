"""M 바디 갈래 정하기 (body_buckets.py, 2026-11-21 분류 설계 시범) — 사장님이 짚은 실제 매물 제목으로."""
from __future__ import annotations

from body_buckets import review_outliers, traits_of
from entity_catalog import _with_parents, annotate_records, load_catalog, record_title


def _body(title: str, price: float | None = None) -> dict:
    final = {"title_raw": title, "category": "Body", "mount": "M", "sold_quality": "asking"}
    if price:
        final.update(parsed_price_numeric=price, currency="USD")
    return {"final_output": final}


def _leaf(title: str) -> tuple[list[str], dict]:
    record = _body(title)
    annotate_records([record])
    catalog = load_catalog()
    leaves = [e for e in record["entity_ids"] if not catalog["entities"][e].get("children") and not catalog["entities"][e].get("feature")]
    return leaves, record["final_output"]


def test_unknown_variants_leave_standard() -> None:
    assert _leaf("Leica M2-M M2M Rangefinder Only 276 Made")[0] == ["leica:body:m2:m2-m"]
    assert _leaf("Leica M2 chrome ELC - full CLA Body")[0] == ["leica:body:m2:canada"]
    assert _leaf("Leica M3 Black Repaint [Shueido Camera Repaint]")[0] == ["leica:body:m3:repaint"]
    assert _leaf("Leica M2 black nachlackiert")[0] == ["leica:body:m2:repaint"]  # 독일어 '재도장'
    assert _leaf("Leica M7 - Shueido Repaint / 0.72")[0] == ["leica:body:m7:repaint"]
    assert _leaf("Leica M3 Body (カナダ)")[0] == ["leica:body:m3:canada"]


def test_custom_leather_is_not_repaint() -> None:
    assert _leaf("Leica M3 Double Stroke (Silver- Chrome) (Green Custom Leather)")[0] == ["leica:body:m3:double-stroke"]


def test_major_bucket_wins_when_two_variants() -> None:
    # 블랙페인트가 대분류 (2026-11-21 사장님): 블랙페인트 + 버튼 리와인드 → 블랙페인트 하나
    assert _leaf("Leica M2 black paint Button Rewind Body")[0] == ["leica:body:m2:black-paint"]


def test_two_models_keep_first_and_prototype_is_rare() -> None:
    leaves, final = _leaf("Leica M6A M6 A (M7 Prototype) Black Rangefinder Rare")
    assert leaves == ["leica:body:m6:rare"]  # M6 클래식·M7 두 곳에 붙던 것
    assert final["bucket"]["reason"].startswith("conflict:")


def test_unmapped_edition_goes_to_review_not_standard() -> None:
    assert _leaf("Leica M-P(Typ240)サファリ Body")[0] == ["leica:body:m-p240:review"]
    assert _leaf("Leica M3 Gold Limited 15 DS")[0] == ["leica:body:m3:review"]
    assert _leaf("Leica M4 50周年 BlackChrome Body 038-I")[0] == ["leica:body:m4:50-jahre"]  # 일본어 '周年'도 50주년 갈래로


def test_defect_is_marked_and_left_out_of_graph() -> None:
    for title in ("Leica M3 Bastelobjekt craft object for parts", "Leica M9 Corroded Sensor (As-is) Body",
                  "Parts - Leica M6 Classic in Original Zinc Finish", "Fotocamera analogica Leica M4 -leggi"):
        assert _leaf(title)[1].get("entity_note") == "defect", title
    assert _leaf("Leica M3 DS full CLA")[1].get("entity_note") is None
    assert "defect" not in traits_of("Leica M6 TTL 0.72 serviced")


def test_price_outlier_without_trait_goes_to_review() -> None:
    catalog = load_catalog()
    records = [_body("Leica M2 chrome", 1700 + i * 10) for i in range(8)] + [_body("Leica M2 chrome body", 8000)]
    annotate_records(records)
    moved = review_outliers(records, lambda r: r["final_output"].get("parsed_price_numeric"), catalog, _with_parents, record_title)
    assert moved == 1
    assert "leica:body:m2:review" in records[-1]["entity_ids"] and "leica:body:m2:standard" not in records[-1]["entity_ids"]
    assert records[-1]["final_output"]["bucket"]["reason"].startswith("price:")
    assert all("leica:body:m2:standard" in r["entity_ids"] for r in records[:-1])
