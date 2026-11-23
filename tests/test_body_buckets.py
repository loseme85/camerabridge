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
    assert _leaf("Leica M3 Gold Limited 15 DS")[0] == ["leica:body:m3:rare"]  # 골드는 시제품·희귀 갈래
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


def test_barnack_buckets() -> None:
    # 바르낙 (2026-11-21): 단일 모델 → 전체 + 스탠다드 + 갈래
    assert _leaf("Leica IIIf Midland Ontario Outfit 10000 Body")[0] == ["leica:body:iiif:canada"]
    assert _leaf("Leica III BLACK/NICKEL Body")[0] == ["leica:body:iii:black-nickel"]
    assert _leaf("Leica IIIf Red Dial w/ Self Timer Body")[0] == ["leica:body:iiif:standard"]  # 레드 다이얼은 값 차이 없음(데이터 1.1배)
    assert _leaf("Leica IIIc Rideau Rouge")[0] == ["leica:body:iiic:rare"]
    assert _leaf("Leica A型 Old Elmar付 Gold (後塗り) 8千台")[0] == ["leica:body:i:repaint"]  # 나중에 칠한 금색 = 리페인트


def test_barnack_conversion_goes_to_current_model() -> None:
    assert _leaf("Leica I Umbau zu III mit Nickel Elamr 50mm f/3.5")[0] == ["leica:body:iii:converted"]
    assert _leaf("Leica IIIc body, war-time, converted to IIIf")[0] == ["leica:body:iiif:converted"]
    assert _leaf("Leica IF upgrade to IIIF Selftimer")[0] == ["leica:body:iiif:converted"]
    assert _leaf("Leica IIIC Umbau IIIF III F Shark Skin Summitar Leitz 50mm")[0] == ["leica:body:iiif:converted"]


def test_barnack_same_place_prefers_specific_model() -> None:
    assert _leaf("Leica III F Body")[0] == ["leica:body:iiif:standard"]  # 판매자의 'III F' = IIIf
    assert _leaf("Leica I c")[0] == ["leica:body:ic:standard"]
    assert _leaf("Linhof Technorama 612 PC II Body")[0] == []  # 다른 브랜드


def test_review_bucket_has_no_model_page() -> None:
    import importlib.util
    from pathlib import Path
    spec = importlib.util.spec_from_file_location("bmp", Path(__file__).resolve().parents[1] / "scripts/build_model_pages.py")
    bmp = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(bmp)
    ents = [{"id": "leica:body:m4:review", "kind": "Body", "active_count": 9, "listing_count": 9, "parent": "leica:body:m4"},
            {"id": "leica:body:m4", "kind": "Body", "active_count": 40, "listing_count": 40, "children": ["leica:body:m4:review"]}]
    picked = {e["id"] for e in bmp.pick_entities(ents, {"leica:body:m4:review"})}
    assert "leica:body:m4:review" not in picked and "leica:body:m4" in picked  # 이미 공개된 적 있어도 다시 만들지 않음


def _leaf_desc(title: str, desc: str, tags: list[str] | None = None) -> tuple[list[str], dict]:
    record = _body(title)
    record["raw_item"] = {"상품명": title, "매장정보": {"desc": desc, "tags": tags or []}}
    annotate_records([record])
    catalog = load_catalog()
    leaves = [e for e in record["entity_ids"] if not catalog["entities"][e].get("children") and not catalog["entities"][e].get("feature")]
    return leaves, record["final_output"]


def test_description_only_repaint_and_defect() -> None:
    leaves, final = _leaf_desc("Leica M2 #941805", "Kanto repaint & CLA. Great shooter.")
    assert leaves == ["leica:body:m2:repaint"] and "desc:repaint" in final["bucket"]["reason"]
    leaves, final = _leaf_desc("Leica IIIc chrome", "Being sold as is for parts. Body does not work.")
    assert final.get("entity_note") == "defect"


def test_description_false_alarms_are_ignored() -> None:
    for desc in ["There are no dents nor major defects.", "Ship to Canada then to the US.", "Body (Black), gold contacts, prototype history.",
                 "Handgrip does not work with M240.", "The sticker is not repainted."]:
        leaves, final = _leaf_desc("Leica M2 chrome", desc)
        assert leaves == ["leica:body:m2"] or leaves == ["leica:body:m2:standard"], (desc, leaves)
        assert final.get("entity_note") != "defect"


def test_m6_ttl_japan_limited_is_its_own_bucket() -> None:
    """사장님 2026-11-22: 진짜 Japan Limited 0.58은 일반 일본 내수 M6 TTL과 따로. '0.58'만 쓴 매물은 단정하지 않음"""
    assert _leaf("Leica M6 TTL Japan Limited 0.58")[0] == ["leica:body:m6:ttl-japan-limited"]
    assert _leaf("Leica M6 TTL ジャパンリミテッド 0.58")[0] == ["leica:body:m6:ttl-japan-limited"]
    assert _leaf("Leica M6 TTL 0.58 Body Black")[0] == ["leica:body:m6:ttl"]
    assert _leaf("[위탁] M6 TTL 0.85 'Japan' (Black)")[0] == ["leica:body:m6:ttl"]


def test_m11p_kevlar_edition_is_its_own_bucket() -> None:
    """사장님 2026-11-22: 뉴욕 Meatpacking 전용 M11-P Kevlar Edition은 일반 M11-P와 따로"""
    assert _leaf("Leica M11-P Kevlar Edition")[0] == ["leica:body:m11-p:kevlar"]
    assert _leaf("Leica M11-P ケブラー")[0] == ["leica:body:m11-p:kevlar"]
    assert _leaf("Leica M11-P Black")[0] == ["leica:body:m11-p:standard"]


def test_m240_100_years_edition_is_its_own_bucket() -> None:
    """사장님 2026-11-22: 2014 M (Typ 240) 100주년 기념판은 일반 M240과 따로. 'M Edition 100' 세트와는 다른 물건"""
    assert _leaf("Leica M 240 100 Jahre demo model + doos")[0] == ["leica:body:m240:100-years"]
    assert _leaf("Leica M (Typ 240) 100 Years Anniversary Edition")[0] == ["leica:body:m240:100-years"]
    assert _leaf("Leica M (Typ 240) Black")[0] == ["leica:body:m240:standard"]
    assert "leica:body:m240:100-years" not in _leaf("Leica M Edition 100 Set M-A Monochrom 240 100 years")[0]


def test_r_bodies_get_buckets_and_r_lens_is_not_r4() -> None:
    # 2026-11-23 ④ 넓히기: 라이카플렉스·R 바디도 갈래. 블랙페인트는 크롬보다 훨씬 비쌈, 'R 4,0/21'은 R4 바디가 아니라 렌즈
    assert _leaf("Leicaflex SL black paint Body")[0] == ["leica:body:leicaflex-sl:black-paint"]
    assert _leaf("Leicaflex Mark II Black Paint Film SLR Camera")[0] == ["leica:body:leicaflex:black-paint"]
    assert _leaf("Leica R4 Body")[0] == ["leica:body:r4:standard"]
    assert _leaf("Leica R4 Gold set 10051 Body")[0] == ["leica:body:r4:rare"]
    assert _leaf("Leica R3 Safari Body")[0] == ["leica:body:r3:safari"]  # 기존 사파리 갈래가 먼저
    assert "leica:body:r4:standard" not in _leaf("Leica R 4,0/21")[0]
