from __future__ import annotations

import json
import re
from pathlib import Path

from entity_catalog import Suggester, load_catalog, match_entities

ROOT = Path(__file__).resolve().parents[1]


def _record(title: str, category: str = "Lens", mount: str | None = "M") -> dict:
    return {"final_output": {"title_raw": title, "category": category, "mount": mount}}


def test_listing_links_to_exact_model_and_parent() -> None:
    ids = match_entities(_record("[중고] M 35/1.4 Summilux ASPH 6bit FLE2 (Black)"))
    assert "leica:lens:summilux-m:35:asph-fle2" in ids
    assert "leica:lens:summilux-m:35" in ids
    assert "leica:lens:summilux-m:35:asph-fle" not in ids


def test_noctilux_is_not_summilux_and_copies_are_excluded() -> None:
    assert "leica:lens:summilux-m:50:asph" not in match_entities(_record("[중고] M 50/0.95 Noctilux ASPH 6bit (Black)"))
    assert match_entities(_record("Leeworks M 50mm f1.1 Noctilux M Silver")) == []
    assert "leica:lens:noctilux-m:50:f1.0" in match_entities(_record("LEICA 50mm F1.0 NOCTILUX-M sn.3220"))


def test_noctilux_f1_generations() -> None:
    nx = "leica:lens:noctilux-m:50:f1.0"
    cases = {
        "[중고] M 50/1.0 Noctilux 2세대 E58 (Black)": "v2-e58",
        "LEICA 50mm F1 NOCTILUX E58 sn.2854": "v2-e58",
        "[중고] M 50/1.0 Noctilux 3세대 E60 (Black)": "v3-e60",
        "[중고] M 50/1.0 Noctilux 4세대 6bit (Black)": "v4-builtin-hood",
        "LEICA 50mm F1.0 NOCTILUX-M sn.3928": "v4-builtin-hood",
        "LEICA 50mm F1.0 NOCTILUX-M sn.3442": "unspecified",  # 3세대·4세대 경계 시리얼은 미표기
        "[중고] M50/1 Noctilux (Black)": "unspecified",
    }
    for title, gen in cases.items():
        ids = match_entities(_record(title))
        assert f"{nx}:{gen}" in ids and nx in ids, title
        assert len([i for i in ids if i.startswith(nx + ":")]) == 1, title


def test_noctilux_generation_markers_from_foreign_dealers() -> None:
    nx = "leica:lens:noctilux-m:50:f1.0"
    cases = {
        "LEITZ Leica Noctilux-M 50mm/F1.0 E60 II Lens Yr.1982 Canada": "v3-e60",
        "Leica 50mm f1 Noctilux-M (Type III) (11821)": "v3-e60",
        "Leica Noctilux-M 50mm/F1.0 E60 V4 Ver.IV Lens Yr.1996 Canada 11822": "v4-builtin-hood",
        "Leica Noctilux M 50mm/F1.0 E58 Ver.I V1 boxed": "v2-e58",
    }
    for title, gen in cases.items():
        assert f"{nx}:{gen}" in match_entities(_record(title)), title


def test_noctilux_f12_original_by_marker_and_price() -> None:
    orig, asph = "leica:lens:noctilux:50:f1.2-original", "leica:lens:noctilux-m:50:f1.2-asph"

    def rec(title, price=None, currency="KRW", category="Lens"):
        r = _record(title, category)
        r["final_output"].update({"parsed_price_numeric": price, "currency": currency})
        return r

    assert orig in match_entities(rec("[중고]Leica M50/1.2 1세대 Noctilux", 33_000_000, category="Body"))
    assert orig in match_entities(rec("[중고] M 50/2 Noctilux Original (Black)"))
    # 표기 없는 f/1.2: 2,000만 원 미만이면 복각, 이상이거나 가격 없으면 오리지널
    ids = match_entities(rec("[중고] M50/1.2 Noctilux (Black)", 8_380_000))
    assert asph in ids and orig not in ids
    assert orig in match_entities(rec("Leica Noctilux-M 50mm F1.2", 3_916_000, "JPY"))
    assert orig in match_entities(rec("LEICA 50mm F1.2 NOCTILUX sn.2556"))
    # 표기가 있으면 가격과 상관없이 표기대로
    assert orig in match_entities(rec("[위탁] M50/1.2 Noctilux 오리지널 1세대 (Black)", 15_000_000))


def test_generation_candidates_listed_under_parent_in_order() -> None:
    import json
    from pathlib import Path

    from entity_catalog import Suggester

    catalog = json.loads((Path(__file__).resolve().parents[1] / "data/config/entity_catalog_v1.json").read_text(encoding="utf-8"))
    names = [e["id"].rsplit(":", 1)[-1] for e in Suggester(catalog["entities"]).suggest("nocti 1.0")[:5]]
    assert names == ["f1.0", "v2-e58", "v3-e60", "v4-builtin-hood", "unspecified"]


def test_korean_shop_body_misfiled_as_lens_still_links_but_accessories_do_not() -> None:
    assert "leica:body:m7" in match_entities(_record("[중고] M7 0.72 (Black)", category="Lens"))
    assert match_entities(_record("[중고] JNK M7 케이스 (Brown)", category="Accessory")) == []
    assert "leica:body:m10" not in match_entities(_record("[중고] Leica M10 하프케이스 (Black)", category="Body"))


def test_edition_numbers_are_not_focal_lengths() -> None:
    ids = match_entities(_record("LEICA 35mm F2 ASPH SUMMICRON-M sn.4618 (33/50)"))
    assert "leica:lens:summicron-m:35:asph" in ids
    assert "leica:lens:summicron-m:50:current" not in ids


def _suggester() -> Suggester:
    summary = ROOT / "data" / "derived" / "entity_summary_v1.json"
    return Suggester(json.loads(summary.read_text(encoding="utf-8"))["entities"])


def test_suggest_understands_shorthand_korean_typos_and_units() -> None:
    s = _suggester()
    assert s.suggest("m6 ttl 0.72", 1)[0]["id"] == "leica:body:m6:ttl"
    assert s.suggest("주미룩스 35 fle", 1)[0]["id"] == "leica:lens:summilux-m:35:asph-fle"
    assert s.suggest("notilux 0.95", 1)[0]["id"] == "leica:lens:noctilux-m:50:f0.95"
    assert s.suggest("summicron 90mm", 1)[0]["id"] == "leica:lens:summicron-m:90"
    assert s.suggest("엠6", 1)[0]["id"] == "leica:body:m6"


def test_suggest_does_not_fill_nonexistent_models() -> None:
    s = _suggester()
    assert s.suggest("summilux 135", 3) == []
    assert s.suggest("24 cron", 3) == []
    assert s.suggest("summicron sl 24", 3) == []


def test_catalog_entities_have_aliases_and_rules() -> None:
    catalog = load_catalog()
    for entity in catalog["entities"].values():
        assert entity["aliases"], entity["id"]
        assert entity["match"] or entity["children"] or entity.get("feature"), entity["id"]


def test_summilux_35_korean_generation_numbers() -> None:
    sl = "leica:lens:summilux-m:35"
    assert f"{sl}:aa" in match_entities(_record("[중고] M 35/1.4 Summilux 3세대 (2매) (Black)"))
    assert f"{sl}:asph-1994" in match_entities(_record("[위탁] M 35/1.4 Summilux 4세대 (Black)"))
    ids = match_entities(_record("[중고] M 35/1.4 Summilux 4세대 (Titan)"))
    assert f"{sl}:titan" in ids and f"{sl}:asph-1994" not in ids


def test_price_relevant_variants_are_separate_models():
    def leaf(title, category="Body"):
        return {i for i in match_entities(_record(title, category=category, mount=None))}
    q3m = leaf("Leica Q3 Monochrom")
    assert "leica:body:q3-monochrom" in q3m and "leica:body:q3" not in q3m
    ttl_ti = leaf("LEICA M6 TTL Titan sn.2754", "Body")
    assert "leica:body:m6:ttl-titan" in ttl_ti and "leica:body:m6:ttl" not in ttl_ti and "leica:body:m6:titan" not in ttl_ti
    assert "leica:body:m6:titan" in leaf("[중고] M6 non ttl (Titan)")
    mp_bp = leaf("신품 Leica MP Blackpaint x0.72")
    assert "leica:body:mp-film:black-paint" in mp_bp and "leica:body:mp-film:standard" not in mp_bp
    assert "leica:body:sl3:reporter" in leaf("Leica SL3 Reporter Body [10662]")
    lux = match_entities(_record("Leica Summilux-M 50mm f1.4 ASPH. Safari [11736]"))
    assert "leica:lens:summilux-m:50:asph-safari" in lux and "leica:lens:summilux-m:50:asph" not in lux
    cron = match_entities(_record("LEICA 35mm F2 ASPH SUMMICRON-M Black paint sn.4000"))
    assert "leica:lens:summicron-m:35:asph-black-paint" in cron and "leica:lens:summicron-m:35:asph" not in cron
    apo = match_entities(_record("Leica APO-Summicron M 50mm F2.0 ASPH.LHSA Silver"))
    assert "leica:lens:apo-summicron-m:50:lhsa" in apo and "leica:lens:summicron-m:50:current" not in apo


def test_suggest_by_leica_product_code() -> None:
    # 2026-10 레딧 피드백: "11873으로 검색하면 아무것도 안 나온다"
    s = _suggester()
    assert s.suggest("11873", 1)[0]["id"] == "leica:lens:summilux-m:35:aa"
    assert s.suggest("leica 11874", 1)[0]["id"] == "leica:lens:summilux-m:35:asph-1994"
    assert s.suggest("20200", 1)[0]["id"] == "leica:body:m11:standard"
    # 앞부분만 같은 번호는 후보가 아님: 초점거리 검색이 바디 번호(10043 R4, 10502 M5)로 새지 않게
    ids = {e["id"] for e in s.suggest("100", 12) + s.suggest("105", 12)}
    assert not ids & {"leica:body:r4", "leica:body:m5:standard", "leica:body:m4-2:standard"}
    assert s.suggest("1187", 3) == []
    # 라이카가 다시 쓴 번호: 두 제품 모두 후보
    ids = {e["id"] for e in s.suggest("11135", 5)}
    assert {"leica:lens:elmarit-m:21:asph", "leica:lens:hektor:135"} <= ids


def test_listing_with_only_product_code_links_to_model() -> None:
    assert "leica:lens:summilux-m:35:asph-fle" in match_entities(_record("Leica 35mm F1.4 Asph M Black 6bit (11663)"))
    assert "leica:body:m6:classic" in match_entities(_record("Leica M6 (0.72x) (Silver, 10414)", category="Body"))
    # 후드·호환품 매물은 번호가 있어도 본품에 연결하지 않음
    assert match_entities(_record("Leica Lens Hood for 11663 Black", category="Accessory")) == []


def test_product_codes_point_to_existing_entities() -> None:
    catalog = load_catalog()
    for number, entity_ids in catalog["codes"].items():
        assert (len(number) == 5 and number.isdigit()) or re.fullmatch(r"[a-z]{5}( [a-z]{1,2})?", number), number
        assert all(entity_id in catalog["entities"] for entity_id in entity_ids), number


def test_search_by_body_feature() -> None:
    # 2026-10 레딧 피드백: "28mm 프레임라인, TTL 같은 사양으로 찾고 싶다"
    s = _suggester()
    assert s.suggest("28mm frameline", 1)[0]["id"] == "leica:feature:frameline-28"
    assert s.suggest("28mm 프레임라인", 1)[0]["id"] == "leica:feature:frameline-28"
    assert s.suggest("ttl", 1)[0]["id"] == "leica:feature:ttl-flash"
    assert s.suggest("노출계 없는", 1)[0]["id"] == "leica:feature:no-meter"
    assert s.suggest("28", 1)[0]["id"].startswith("leica:lens:")  # 숫자만 치면 여전히 28mm 렌즈가 먼저
    assert s.suggest("m6 ttl 0.72", 1)[0]["id"] == "leica:body:m6:ttl"


def test_feature_groups_follow_body_specs() -> None:
    def ids(title):
        return match_entities(_record(title, category="Body", mount="M"))
    assert "leica:feature:frameline-28" in ids("Leica M6 0.72 Black")
    assert "leica:feature:frameline-28" not in ids("Leica M6 TTL 0.85 Black")  # 0.85 파인더엔 28mm 프레임 없음
    assert "leica:feature:frameline-28" not in ids("Leica M3 Double Stroke")
    assert "leica:feature:ttl-flash" in ids("Leica M7 0.72 Silver")
    assert "leica:feature:ttl-flash" not in ids("Leica MP 0.72 Black Paint")
    assert "leica:feature:mechanical" not in ids("Leica M7 0.72 Silver")
    assert "leica:feature:no-meter" in ids("Leica M-A Typ 127 Silver")


def test_suggest_by_leitz_code_word() -> None:
    s = _suggester()
    assert s.suggest("SOOIC", 1)[0]["id"] == "leica:lens:summicron:50:collapsible"
    assert s.suggest("sooic-m", 1)[0]["id"] == "leica:lens:summicron:50:collapsible"
    assert s.suggest("SUMMITAR", 1)[0]["id"] == "leica:lens:summitar:50"  # 이름 검색은 그대로
    assert s.suggest("SOORE", 1)[0]["id"] == "leica:lens:summitar:50"


def test_military_and_special_bodies_are_separate() -> None:
    def ids(title):
        return match_entities(_record(title, category="Body", mount=None))
    luft = ids("Leica IIIc Luftwaffen-Eigentum Fl.Nr 38079")
    assert "leica:body:barnack-military" in luft and "leica:body:iiic" not in luft
    assert "leica:body:iiic" in ids("Leica IIIc chrome")
    assert "leica:body:iiig-swedish" in ids("Leica IIIg Swedish Army three crowns")
    ke = ids("Leica KE-7A US Army")
    assert "leica:body:ke-7a" in ke and "leica:body:m4:standard" not in ke
    assert "leica:body:c2-zoom" in ids("Leica C2-Zoom")
    assert "leica:body:c-series" not in ids("Leica C2-Zoom")
    assert "leica:body:digilux-2" in ids("Leica Digilux 2")
    assert "leica:body:d-lux-1" in ids("Leica D-Lux 1")


def test_lens_bundled_with_hood_still_links() -> None:
    # 'with hood'는 렌즈 매물 (후드 단품은 그대로 제외)
    assert "leica:lens:summarex:85" in match_entities(_record("Leica Summarex L39 85mm/F1.5 with hood", mount=None))
    assert match_entities(_record("Leica 12585 Metal Hood for Summaron M 35 / 50mm", category="Accessory")) == []


def test_r_lenses_from_hong_kong_titles() -> None:
    assert "leica:lens:telyt-r:long" in match_entities(_record("LEITZ Leica Telyt-R 250mm/F4.0 Ver.II V2 Lens", mount="R"))
    assert "leica:lens:mr-telyt-r:500" in match_entities(_record("LEITZ Leica MR-Telyt-R 500mm/F8.0 Lens Yr.1981", mount="R"))
    assert "leica:lens:elmarit-r:100" in match_entities(_record("LEITZ Leica Macro-Elmar-R 100mm/F4.0 Lens Yr.1980", mount="R"))
    assert "leica:lens:summicron:50:collapsible" in match_entities(_record("LEITZ Leica Summicron L39 50mm/F2.0 Silver Lens Yr.1955 LTM", mount=None))
