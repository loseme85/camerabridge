from __future__ import annotations

import json
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
        assert entity["match"] or entity["children"], entity["id"]


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


def test_listing_with_only_product_code_links_to_model() -> None:
    assert "leica:lens:summilux-m:35:asph-fle" in match_entities(_record("Leica 35mm F1.4 Asph M Black 6bit (11663)"))
    assert "leica:body:m6:classic" in match_entities(_record("Leica M6 (0.72x) (Silver, 10414)", category="Body"))
    # 후드·호환품 매물은 번호가 있어도 본품에 연결하지 않음
    assert match_entities(_record("Leica Lens Hood for 11663 Black", category="Accessory")) == []


def test_product_codes_point_to_existing_entities() -> None:
    catalog = load_catalog()
    for number, entity_id in catalog["codes"].items():
        assert len(number) == 5 and number.isdigit(), number
        assert entity_id in catalog["entities"], entity_id
