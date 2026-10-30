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


def test_summilux_r50_generations_do_not_overlap() -> None:
    sx = "leica:lens:summilux-r:50"
    cases = {
        "Leica Summilux-R 50mm/F1.4 E55 Ver.II V2 Safari 11776": "v1",  # 해외 Ver.II = 1세대 후기
        "Leica 50mm f1.4 Summilux-R (Type I v2) (3-Cam) (11776)": "v1",
        "Leica Summilux-R 50mm F1.4 N 3-CAM": "v1",
        "LEICA 50mm F1.4 SUMMILUX-R sn.3290": "v1",
        "LEICA 50mm F1.4 ROM SUMMILUX-R sn.3729": "v1",
        "[중고] R 50/1.4 Summilux E60 ROM (Black)": "v2",
        "LEICA 50mm F1.4 E60 ROM SUMMILUX-R sn.3798": "v2",
        "LEICA 50mm F1.4 SUMMILUX-R sn.3775": "unspecified",
    }
    for title, gen in cases.items():
        kids = [i for i in match_entities(_record(title, mount="R")) if i.startswith(sx + ":")]
        assert kids == [f"{sx}:{gen}"], (title, kids)
    cheap = _record("Leica R 50mm f1.4 Summilux Black", mount="R")
    cheap["final_output"].update({"parsed_price_numeric": 1_000_000, "currency": "KRW"})
    assert f"{sx}:v1" in match_entities(cheap)


def test_summicron_28_asph_three_versions() -> None:
    sc = "leica:lens:summicron-m:28:asph"
    cases = {
        "Leica Summicron-M 28mm/F2.0 ASPH Black Lens Yr.2001 Germany 11604": "v1",
        "LEICA 28mm F2 ASPH (6bit) SUMMICRON-M sn.4075": "v1",
        "[위탁] M 28/2 Summicron ASPH NEW (Black)": "v2",
        "LEICA 28mm F2 ASPH II SUMMICRON-M sn.4922": "v2",
        "SUMMICRON-M 28 mm f/2 ASPH ( 2016-ACTU )": "v2",
        "Leica 28mm F2 Asph M Black (11672)": "v2",
        "SUMMICRON-M 28 mm f/2 ASPH. close focus (2024-ACTU)": "v3",
        "Brand New Leica Summicron-M 28mm/F2.0 E46 Asph.11618 Black Lens Germany 11618": "v3",
        "LEICA 28mm F2 ASPH SUMMICRON-M MATT BLACK PAINT FINISH sn.4792": "unspecified",
    }
    for title, gen in cases.items():
        kids = [i for i in match_entities(_record(title)) if i.startswith(sc + ":")]
        assert kids == [f"{sc}:{gen}"], (title, kids)
    assert "leica:lens:summicron-m:28:safari" in match_entities(_record("[중고] M 28/2 Safari Summicron"))
    assert not any(i.startswith(sc + ":") for i in match_entities(_record("[중고] M 28/2 Safari Summicron")))


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


def test_top20_collector_terms_find_their_models() -> None:
    """프리미엄 빈티지 수요 가설 TOP 20(2026-10-08)의 검색어가 맞는 모델로."""
    catalog = json.loads((ROOT / "data/config/entity_catalog_v1.json").read_text(encoding="utf-8"))
    s = Suggester(catalog["entities"])
    top = lambda q: s.suggest(q, 1)[0]["id"]
    for q in ("king of bokeh", "kob", "35 크론 v4", "35 cron v4"):
        assert top(q) == "leica:lens:summicron-m:35:v4", q
    for q in ("35 cron v1", "35 크론 1세대", "6군8매"):
        assert top(q) == "leica:lens:summicron-m:35:v1-8element", q
    assert top("elmarit 28 v1") == "leica:lens:elmarit-m:28:v1"
    assert top("m3 싱글스트로크") == "leica:body:m3:single-stroke"
    assert top("35lux aspherical") == "leica:lens:summilux-m:35:aa"
    # 붙여 쓴 '50lux'를 '35lux'로 고쳐 읽지 않음
    assert top("50lux pre asph") == "leica:lens:summilux-m:50"
    assert all("summilux-m:35" not in e["id"] for e in s.suggest("50lux pre asph", 5))


def test_king_of_bokeh_listing_is_summicron_35_v4() -> None:
    ids = match_entities(_record('Leica 35mm f/2 SUMMICRON-M "KING OF BOKEH"'))
    assert "leica:lens:summicron-m:35:v4" in ids
    assert "leica:lens:summicron-m:35:unspecified" not in ids


def test_summicron_50_first_second_not_current_generation() -> None:
    # 한국·일본 매장의 '2nd'는 1969년형(서양 3세대), 서양 매장의 2nd는 리지드 — 셈법이 달라 4·5세대(현행)에도, 특정 세대에도 붙이지 않음
    cur = "leica:lens:summicron-m:50:current"
    gen12 = "leica:lens:summicron:50:gen12-unspecified"
    for title in ("LEICA 50mm F2 (2nd) SUMMICRON sn.2445", "[중고] M 50/2 Summicron 2세대 (Black)",
                  "Leica Summicron M 50/2 (2nd)", "Leica Summicron-M 50mm f2.0 2nd"):
        ids = match_entities(_record(title))
        assert cur not in ids and gen12 in ids and "leica:lens:summicron:50" in ids
    assert "leica:lens:summicron:50:rigid-late" in match_entities(_record("Leica Summicron 50mm f2 Rigid 2nd"))
    assert gen12 not in match_entities(_record("Leica Summicron 50mm f2 Rigid 2nd"))
    assert cur in match_entities(_record("Leica Summicron-M 50mm f2 4th Black"))


def test_cl_film_and_digital_by_marker_and_price() -> None:
    film, digital, f50 = "leica:body:cl-film", "leica:body:cl-digital:standard", "leica:body:cl-film-50-jahre"

    def rec(title, price=None, currency="KRW", category="Lens"):
        r = _record(title, category, None)
        r["final_output"].update({"parsed_price_numeric": price, "currency": currency})
        return r

    # 표기가 있으면 표기대로
    assert film in match_entities(rec("Leitz MINOLTA CL Body", 121_000, "JPY", "Body"))
    assert film in match_entities(rec("Leica CL film Body", 7_995, "DKK", "Body"))
    assert match_entities(rec("Leica CL 50주년기념 serviced.노출계정상", 1_280_000))[:1] == [f50]
    assert digital not in match_entities(rec("Leica CL 50주년기념 serviced.노출계정상", 1_280_000))
    assert digital in match_entities(rec("Leica 19301 CL black Body", 1_800, "EUR", "Body"))
    # 표기 없는 CL: 170만 원 미만은 필름, 이상이거나 가격 없으면 디지털
    for title, price, cur in (("Leica CL Body", 108_600, "JPY"), ("Leica CL (10700)", 624, "EUR"), ("LEICA CL sn.1409", 1_000_000, "KRW")):
        ids = match_entities(rec(title, price, cur))
        assert film in ids and digital not in ids, title
    for title, price in (("[중고] CL (Silver)", 2_480_000), ("Leica CL black", 2_300_000), ("LEICA CL sn.5352", None)):
        ids = match_entities(rec(title, price))
        assert digital in ids and film not in ids, title


def test_macro_elmar_100_bellows_head_is_its_own_model() -> None:
    head, r_lens = "leica:lens:macro-elmar:100:bellows", "leica:lens:elmarit-r:100"
    ids = match_entities(_record("Leica Leitz Macro-Elmar 100mm f4, lens head for bellows", mount=None))
    assert head in ids and r_lens not in ids
    ids = match_entities(_record("Leica Macro-Elmar 100/4(for bellows)", mount=None))
    assert head in ids and r_lens not in ids
    assert r_lens in match_entities(_record("Leica R Macro-Elmar 100mm F4 3CAM", mount="R"))


def test_elmar_50_f28_old_and_elmar_m_split() -> None:
    old, new, unspec = (f"leica:lens:elmar-m:50:f2.8:{k}" for k in ("v1", "elmar-m", "unspecified"))
    for title in ("Leitz 5cm f2.8 Elmar, screw mount", "Leitz 50mm f2.8 Elmar, M", "LEICA 50mm F2.8 ELMAR sn.1625",
                  "LEITZ Leica Elmar M 50mm/F2.8 Ver.I Silver Lens Yr.1959 Germany", "Leica Elmar-M 50mm F2.8 Old Collapsible"):
        assert old in match_entities(_record(title, mount=None)), title
    for title in ("Leica 50mm F2.8 M Black (11831)", "LEICA 50mm F2.8 ELMAR-M sn.3911", "ELMAR-M 50 mm f/2.8 (1994-2007)",
                  "LEICA M-System MP + 50mmF2.8 ELMAR-M sn.2939"):  # sn.2939는 바디 번호
        assert new in match_entities(_record(title, mount=None)), title
    ids = match_entities(_record("Leica 50mm F2.8 Elmar", mount=None))
    assert unspec in ids and "leica:lens:elmar-m:50:f2.8" in ids
    assert not any("elmar-m:50" in i for i in match_entities(_record("Leitz 50mm f3.5 Elmar", mount=None)))


def test_accessories_for_a_lens_are_not_the_lens() -> None:
    for title in ("Leitz 'VTOOX' aperture setting ring for 50mm f2.8 Elmar", "Leitz 14071 short focusing mount for 135mm f4 Elmar",
                  "Leica 12549 Elmar-M 50mm f2.8용)", "LEICA Visoflex EVF2 - Electronic Viewfinder for Leica M (Typ 240)",
                  "Leica (14021) SVOOP Film Take-Up Spool for Barnack LTM I II IIIc IIIf",
                  "Leitz HEBOO Slow Speed Shutter Release for Leica Standard and II"):
        assert match_entities(_record(title, mount=None)) == [], title
    # 렌즈에 부속품이 딸린 매물은 그대로 렌즈
    assert "leica:lens:elmar:65" in match_entities(_record("Leitz 65mm f3.5 Elmar + 16464 universal focusing mount", mount=None))


def test_m6_special_editions_are_split_from_classic_and_ttl() -> None:
    def m6(title: str) -> list[str]:
        return [i for i in match_entities(_record(title, "Body")) if i.startswith("leica:body:m6:")]
    assert m6("LEICA M6 PANDA sn.1773") == ["leica:body:m6:panda"]
    assert m6("LEICA M6 PANDA 'sh' 125th ANNIVERSARY 106/125") == ["leica:body:m6:siber-hegner"]
    assert m6('[중고] M6 "Colombo 92" -200대한정-') == ["leica:body:m6:columbus"]
    assert m6("LEICA M6 chrome Gold Dragon Edition, 1995") == ["leica:body:m6:gold-dragon"]
    assert m6("Leica M 6 플라티늄 (75주년)") == ["leica:body:m6:platinum"]
    assert m6("Leica M6 LEITZ WETZLAR刻印 Silver") == ["leica:body:m6:leitz-wetzlar"]
    assert m6("Leica 【世界300台 Limited品】M6 TTL 0.85 GreenPaint 10478") == ["leica:body:m6:ttl-green"]
    assert m6("Leica M6 TTL Olive Green x0.85 [Custom]") == ["leica:body:m6:ttl"]  # 개인 도색은 그린페인트 한정판이 아님
    assert m6("LEICA M6 TTL 0.85 NSH black paint finish SH124/400 sn.2680") == ["leica:body:m6:ttl-nsh"]
    assert m6("Leica M6 TTL 0.85 Øresundsbron Black Paint set with Summilux-M 50mm f1.4 10492") == ["leica:body:m6:ttl-oresund"]
    assert m6("Leica M6 “Royal-Photo Austria” Black chromium") == ["leica:body:m6:royal-foto"]
    assert m6("LEICA M6 ROYAL CENTENARY 1994 043/100") == ["leica:body:m6:royal"]
    assert m6("Leica M6 with 35mm f2 Summicron-M Danish Royal Wedding (028/200)") == ["leica:body:m6:royal-wedding"]
    assert m6('Leica M6 "EIN STÜCK Leica" + 35mm f1.4 - 306/996') == ["leica:body:m6:ein-stueck"]
    assert m6("LEICA M6 TTL the last 999 sn.2756") == ["leica:body:m6:last-999"]
    assert m6("LEICA M6 TTL ICS Black paint sn.2555") == ["leica:body:m6:ttl-ics"]
    assert m6("Black Paint Leica M6 TTL 0.85 Dragon 2000") == ["leica:body:m6:ttl-dragon"]
    assert m6("LEICA M6 black paint") == ["leica:body:m6:classic"]
    assert m6("Leica M6 Safari 타조 custom 0.85") == ["leica:body:m6:classic"]  # 개인 도색은 한정판이 아님
    assert m6("Leica MP 0.72 Black Paint w/ M6 Dial FIRST BATCH") == []
    assert m6("[중고] M6 CLASSIC") == ["leica:body:m6:classic"]
    assert m6("Leica M6 TTL 0.72 Black") == ["leica:body:m6:ttl"]


def test_m6_editions_are_flagged_for_the_version_bar() -> None:
    entities = load_catalog()["entities"]
    assert entities["leica:body:m6:titan"].get("edition") and entities["leica:body:m6:ttl-millennium"].get("edition")
    assert not any(entities[f"leica:body:m6:{k}"].get("edition") for k in ("classic", "ttl", "leitz-wetzlar", "panda"))


def test_generation_counts_differ_by_country_and_steel_rim_reissue_without_label() -> None:
    def lens(title: str, prefix: str) -> list[str]:
        return sorted(i for i in match_entities(_record(title, "Lens")) if i.startswith(prefix) and i.count(":") >= 4)  # 부모 칸 제외
    sr = "leica:lens:summilux-m:35:"
    # 복각 표기가 없어도 11301·2022·오리지널 근거 없는 'Summilux-M … steel rim'은 복각
    assert lens("Leica Summilux 35mm f1.4 Steel Rim (11301)", sr) == [sr + "steel-rim-reissue"]
    assert lens("LEICA 35mm F1.4 steel rim SUMMILUX-M sn.4836", sr) == [sr + "steel-rim-reissue"]
    assert lens("Leica 35mm f1.4 Summilux-M Steel Rim", sr) == [sr + "steel-rim-reissue"]
    assert lens("Leica Summilux-M 35mm f1.4 M3 Steel Rim With Goggles 11870", sr) == [sr + "v1-steel-rim"]
    assert lens('Leica Summilux-M 35mm f1.4 "Original Steel Rim 1960"', sr) == [sr + "v1-steel-rim"]
    assert lens("LEICA 35mm F1.4 steel rim SUMMILUX sn.1765", sr) == [sr + "v1-steel-rim"]
    # 'V2'·'Ver.2'·'第2世代'는 세대 칸에만 (미표기 칸에 같이 들어가지 않음)
    assert lens("Leica Summilux-M 35mm f1.4 V2 Infinity Lock 11870", sr) == [sr + "v2"]
    assert lens("LEICA 35mm F1.4 Ver.2 infinity Lock SUMMILUX sn.2347", sr) == [sr + "v2"]
    lux = "leica:lens:summilux-m:50:"
    # 해외 'Type III'(11868·11856)는 E46 후드 내장 = 한국 4세대, 한국 '5th'는 ASPH
    assert lens("Leica 50mm f1.4 Summilux-M (Type III) (Black, 11868)", lux) == [lux + "v4"]
    assert lens("Leica Summilux 50mm f1.4 Silver 5th", lux) == [lux + "asph"]
    assert lens("Leica Summilux M 50/1.4 (第2世代)", lux) == [lux + "v2"]
    # 주미크론 50: 해외·일본 세대 표기는 현행(4·5세대)이 아님
    sc50 = "leica:lens:summicron"
    assert lens("Leica 50mm f2 Summicron (Type II) (Silver, SOOIC-MS / SOSIC / 11118)", sc50) == ["leica:lens:summicron:50:gen12-unspecified"]
    assert lens("Leica Summicron-M 50mm f2.0 Version III", sc50) == ["leica:lens:summicron:50:v3"]
    assert lens("Leica Summicron M 50/2 第3世代", sc50) == ["leica:lens:summicron:50:v3"]
    assert lens("Leica SUMMICRON-M 50mm F2.0(VER.4)", sc50) == ["leica:lens:summicron-m:50:current"]
    # 주미크론 35: 7매를 '4th'로 쓰는 매장 → 매수가 이김
    sc35 = "leica:lens:summicron-m:35:"
    assert lens("LEICA 35mm F2 (4th) 7 element SUMMICRON-M sn.3554", sc35) == [sc35 + "v3"]
    assert lens("Leica SUMMICRON M 35mm F2.0 ver.4", sc35) == [sc35 + "v4"]
    assert lens("Leica SUMMICRON-M 35mm F2.0(VER.1)", sc35) == [sc35 + "v1-8element"]
    assert lens("Leica Elmarit-M 28/2.8 第2世代 Late E48", "leica:lens:elmarit-m:28") == ["leica:lens:elmarit-m:28:v2"]


def _priced(title: str, krw: float) -> dict:
    record = _record(title)
    record["entity_ids"] = match_entities(record)
    record["_v"] = krw
    return record


def test_price_band_decides_original_or_reissue_only_when_title_is_silent() -> None:
    from entity_catalog import infer_by_price
    orig, re_ = "leica:lens:summilux-m:35:v1-steel-rim", "leica:lens:summilux-m:35:steel-rim-reissue"
    records = [_priced("Leica Summilux 35mm f1.4 Steel Rim M3 11870", v) for v in (9_000_000, 14_000_000, 20_000_000)]
    records += [_priced("Leica Summilux 35mm f1.4 Steel Rim Reissue 11301", v) for v in (4_500_000, 5_000_000, 5_500_000)]
    silent_cheap = _priced("[중고] M 35/1.4 Summilux 스틸림 (Silver)", 5_100_000)
    silent_between = _priced("[위탁] M 35/1.4 Summilux 스틸림 (Black)", 7_000_000)  # 어느 가격대에도 안 들어감 → 그대로
    cheap_but_marked = _priced("Leica Summilux 35mm f1.4 Steel Rim M3 goggles", 5_000_000)  # 제목 근거가 이김
    records += [silent_cheap, silent_between, cheap_but_marked]
    assert orig in silent_cheap["entity_ids"]
    assert infer_by_price(records, lambda r: r["_v"]) == 1
    assert re_ in silent_cheap["entity_ids"] and orig not in silent_cheap["entity_ids"]
    assert "leica:lens:summilux-m:35" in silent_cheap["entity_ids"]  # 부모는 그대로
    assert silent_cheap["final_output"]["entity_note"] == "price_inferred"
    assert orig in silent_between["entity_ids"] and "entity_note" not in silent_between["final_output"]
    assert orig in cheap_but_marked["entity_ids"]


def test_far_too_cheap_listing_is_flagged_and_left_out_of_market_price() -> None:
    from entity_catalog import flag_too_cheap
    records = [_priced("Leica Summicron-M 50mm f2 Silver", v) for v in (2_000_000, 2_200_000, 2_400_000, 2_300_000, 2_100_000)]
    manual = _priced("Leica Summicron-M 50mm f2 Instructions", 15_000)
    records.append(manual)
    flagged = flag_too_cheap(records, lambda r: r["_v"])
    assert flagged == {id(manual)} and manual["final_output"]["entity_note"] == "too_cheap"


# 분류 오류 케이스 (2026-10-30): 렌즈 표기 속 숫자·'…용'·렌즈 세대 표기를 바디로 읽던 매물
BODY_MISREAD_CASES = [
    # (케이스, 제목, 분류, 연결되면 안 되는 바디)
    ("조리개 숫자", "Leica Summaron M3.5/3.5", "Lens", "leica:body:m3:standard"),
    ("캠 수", "Leica 75-200 Vario-Elmarit-R 3 Cam", "Lens", "leica:body:r3:standard"),
    ("렌즈 세대", "Leica 9cm f4 Elmar (Type II, Collapsible) (ILNOO / 11631 / 11131)", "Lens", "leica:body:ii"),
    ("렌즈 세대", "Leica 9cm f4 Elmar (Type III) (11830)", "Lens", "leica:body:iii"),
    ("…용 렌즈", "Leica Summaron-M 35mm f2.8 for Leica M3", "Body", "leica:body:m3:standard"),
    ("…용 렌즈", "Leica Telyt-R 400mm/F6.8 Leicaflex 11960", "Body", "leica:body:leicaflex"),
    ("…용 액세서리", "Leica Handgriff schwarz für M11", "Body", "leica:body:m11:standard"),
    ("…용 액세서리", "LEICA Barnack VIT for IIIg", "Body", "leica:body:iiig"),
    ("이름 뒤 소수점", "Leica M 8.2 Silver", "Body", "leica:body:m8"),
]


def test_lens_notation_and_for_words_are_not_read_as_bodies() -> None:
    for case, title, category, body in BODY_MISREAD_CASES:
        ids = match_entities(_record(title, category))
        assert not any(i == body or i.startswith(body + ":") for i in ids), (case, title, ids)
    assert "leica:lens:summaron:35:f2.8" in match_entities(_record("Leica Summaron-M 35mm f2.8 for Leica M3", "Body"))  # 바디로 분류돼도 렌즈로
    # 바디 이름이 먼저 나오면 그대로 바디 (렌즈 뒤 기념판 이름도 읽음)
    assert "leica:body:m3:standard" in match_entities(_record("LEICA M3 50mm F2 SUMMICRON sn.1139", "Body"))
    assert "leica:body:m6:ttl-millennium" in match_entities(_record("LEICA M6 TTL 0.72 35mm 50mm black paint Millennium 3 piece", "Body"))
    assert match_entities(_record("[중고] Q3 43mm", "Body", None)) == ["leica:body:q3-43"]  # 렌즈 일체형은 렌즈 표기가 이름의 일부


def test_body_with_lens_is_a_set_but_fixed_lens_camera_is_not() -> None:
    from entity_catalog import is_set
    def rec(title: str, category: str = "Body", mount: str | None = "M") -> dict:
        r = _record(title, category, mount)
        r["entity_ids"] = match_entities(r)
        return r
    assert is_set(rec("LEICA M3 50mm F2 SUMMICRON sn.1139"))
    assert is_set(rec("Leica IIIf + Elmar 3.5 / 50mm lens", mount=None))
    assert not is_set(rec("Leica M6 .72mm Black Chrome"))
    assert not is_set(rec("Leica R3 Electronic Black 35mm SLR Film Body", mount="R"))
    assert not is_set(rec("[중고] Q3 43mm", mount=None))
    assert not is_set(rec("Leica Minilux Zoom Vario-Elmar 35-70mm silber", mount=None))
