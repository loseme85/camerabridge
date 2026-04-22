from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from query_parser import parse_query
from query_resolver import rank_listings, score_listing


def _record(final_output: dict, override_applied: bool = False, index: int = 1) -> dict:
    return {
        "record_index": index,
        "raw_item": {
            "site": "test",
            "상품명": final_output.get("title_raw", ""),
            "링크": "https://example.invalid/item",
        },
        "classifier_output": {
            "brand": "Unknown",
            "mount": "Unknown",
            "category": "Lens",
            "label": "Lens",
            "model_canonical": None,
            "variant": [],
            "focal_length": None,
        },
        "final_output": final_output,
        "override_applied": override_applied,
        "audit_trail": [],
    }


SUMMILUX_35 = _record(
    {
        "brand": "Leica",
        "mount": "M",
        "category": "Lens",
        "label": "M Lens",
        "model_raw": "Summilux",
        "model_canonical": "Summilux-M",
        "variant": ["ASPH", "AA"],
        "focal_length": "35",
        "title_raw": "Leica M 35mm Summilux ASPH AA",
        "source": "test",
        "source_url": "https://example.invalid/summilux-35-aa",
    }
)


MP3_SILVER = _record(
    {
        "brand": "Leica",
        "mount": "M",
        "category": "Body",
        "label": "M Body",
        "model_raw": None,
        "model_canonical": "MP3",
        "variant": ["Silver"],
        "focal_length": None,
        "title_raw": "[위탁] MP3 (Silver)",
        "source": "trusted",
        "source_url": "https://example.invalid/mp3-silver",
    },
    override_applied=True,
)


CM_BODY = _record(
    {
        "brand": "Leica",
        "mount": "PNS",
        "category": "Body",
        "label": "PNS Body",
        "model_raw": "CM",
        "model_canonical": "CM",
        "variant": [],
        "focal_length": None,
        "title_raw": "LEICA CM sn.2950",
        "source": "trusted",
        "source_url": "https://example.invalid/cm",
    },
    index=3,
)


M6_BODY = _record(
    {
        "brand": "Leica",
        "mount": "M",
        "category": "Body",
        "label": "M Body",
        "model_raw": "M6",
        "model_canonical": "M6",
        "variant": [],
        "focal_length": None,
        "title_raw": "Leica M6 TTL 0.72 Body",
        "source": "test",
        "source_url": "https://example.invalid/m6",
    },
    index=16,
)


M6_ACCESSORY = _record(
    {
        "brand": "Leica",
        "mount": "M",
        "category": "Accessory",
        "label": "Accessory",
        "model_raw": None,
        "model_canonical": None,
        "variant": [],
        "focal_length": None,
        "accessory_type": "case",
        "title_raw": "Leica M6 Leather Case",
        "source": "test",
        "source_url": "https://example.invalid/m6-case",
    },
    index=17,
)


Q3_BODY = _record(
    {
        "brand": "Leica",
        "mount": "Q",
        "system": "Q",
        "category": "Body",
        "label": "Q Body",
        "model_raw": "Q3",
        "model_canonical": "Q3",
        "variant": [],
        "focal_length": None,
        "title_raw": "Leica Q3 Digital Camera",
        "source": "test",
        "source_url": "https://example.invalid/q3",
    },
    index=18,
)


Q3_ACCESSORY = _record(
    {
        "brand": "Leica",
        "mount": "Q",
        "system": "Q",
        "category": "Accessory",
        "label": "Accessory",
        "model_raw": None,
        "model_canonical": None,
        "variant": [],
        "focal_length": None,
        "accessory_type": "case",
        "title_raw": "Leica Q3 Half Case",
        "source": "test",
        "source_url": "https://example.invalid/q3-case",
    },
    index=19,
)


R8_BODY = _record(
    {
        "brand": "Leica",
        "mount": "R",
        "category": "Body",
        "label": "R Body",
        "model_raw": "R8",
        "model_canonical": "R8",
        "variant": [],
        "focal_length": None,
        "title_raw": "Leica R8 Body Black",
        "source": "test",
        "source_url": "https://example.invalid/r8",
    },
    index=20,
)


BARNACK_IIIF_BODY = _record(
    {
        "brand": "Leica",
        "mount": "L",
        "category": "Body",
        "label": "L Body",
        "model_raw": "IIIf",
        "model_canonical": "IIIf",
        "variant": [],
        "focal_length": None,
        "title_raw": "Leica IIIf Body",
        "source": "test",
        "source_url": "https://example.invalid/iiif",
    },
    index=21,
)


HOOD_ACCESSORY = _record(
    {
        "brand": "Leica",
        "mount": "Unknown",
        "category": "Accessory",
        "label": "Accessory",
        "model_raw": None,
        "model_canonical": None,
        "variant": [],
        "focal_length": None,
        "accessory_type": "hood",
        "title_raw": "Leica 12475 Hood Black for M 50mm F1.2 Noctilux ASPH",
        "source": "test",
        "source_url": "https://example.invalid/hood-12475",
    },
    index=4,
)


HOOD_CODE_ACCESSORY = _record(
    {
        "brand": "Leica",
        "mount": "Unknown",
        "category": "Accessory",
        "label": "Accessory",
        "model_raw": None,
        "model_canonical": None,
        "variant": [],
        "focal_length": None,
        "accessory_type": "hood",
        "title_raw": "LEICA 12586 50mm F1.4 Hood",
        "source": "test",
        "source_url": "https://example.invalid/hood-12586",
    },
    index=5,
)


HOOD_BUNDLE_LENS = _record(
    {
        "brand": "Zeiss",
        "mount": "M",
        "category": "Lens",
        "label": "3rd Party M Lens",
        "model_raw": "Biogon",
        "model_canonical": "Biogon",
        "variant": [],
        "focal_length": "21",
        "title_raw": "Zeiss 21mm F2.8 ZM + Hood - Silver",
        "source": "test",
        "source_url": "https://example.invalid/zeiss-21-bundle",
    },
    index=6,
)


FILTER_ACCESSORY = _record(
    {
        "brand": "Leica",
        "mount": "Unknown",
        "category": "Accessory",
        "label": "Accessory",
        "model_raw": None,
        "model_canonical": None,
        "variant": [],
        "focal_length": None,
        "accessory_type": "filter",
        "title_raw": "[위탁] Leica UVa E39 & Skylight E39",
        "source": "test",
        "source_url": "https://example.invalid/filter-e39",
    },
    index=7,
)


FILTER_A36_ACCESSORY = _record(
    {
        "brand": "Leica",
        "mount": "Unknown",
        "category": "Accessory",
        "label": "Accessory",
        "model_raw": None,
        "model_canonical": None,
        "variant": [],
        "focal_length": None,
        "accessory_type": "filter",
        "title_raw": "LEICA A36 Orange",
        "source": "test",
        "source_url": "https://example.invalid/filter-a36-orange",
    },
    index=8,
)


FILTER_BUNDLE_LENS = _record(
    {
        "brand": "Leica",
        "mount": "M",
        "category": "Lens",
        "label": "M Lens",
        "model_raw": "Summilux",
        "model_canonical": "Summilux-M",
        "variant": [],
        "focal_length": "35",
        "title_raw": "Used Leica Summilux-M 35mm f/1.4 ASPH FLE, silver - UVa Filter",
        "source": "test",
        "source_url": "https://example.invalid/summilux-filter-bundle",
    },
    index=9,
)


ADAPTER_ACCESSORY = _record(
    {
        "brand": "Leica",
        "mount": "Unknown",
        "category": "Accessory",
        "label": "Accessory",
        "model_raw": None,
        "model_canonical": None,
        "variant": [],
        "focal_length": None,
        "accessory_type": "adapter",
        "title_raw": "Leica M-Adapter-L Black",
        "source": "test",
        "source_url": "https://example.invalid/adapter-m-l",
    },
    index=11,
)


ADAPTOR_ACCESSORY = _record(
    {
        "brand": "Other",
        "mount": "Unknown",
        "category": "Accessory",
        "label": "Accessory",
        "model_raw": None,
        "model_canonical": None,
        "variant": [],
        "focal_length": None,
        "accessory_type": "adapter",
        "title_raw": "Amadeo adaptor for Contax RF to Leica M",
        "source": "test",
        "source_url": "https://example.invalid/adaptor-contax-m",
    },
    index=12,
)


ADAPTER_MACRO_ACCESSORY = _record(
    {
        "brand": "Leica",
        "mount": "Unknown",
        "category": "Accessory",
        "label": "Accessory",
        "model_raw": None,
        "model_canonical": None,
        "variant": [],
        "focal_length": None,
        "accessory_type": "adapter",
        "title_raw": "[위탁] Macro Adapter M",
        "source": "test",
        "source_url": "https://example.invalid/macro-adapter-m",
    },
    index=15,
)


ADAPTER_BUNDLE_LENS = _record(
    {
        "brand": "Zeiss",
        "mount": "M",
        "category": "Lens",
        "label": "3rd Party M Lens",
        "model_raw": "Sonnar",
        "model_canonical": "Sonnar",
        "variant": [],
        "focal_length": "50",
        "title_raw": "Carl Zeiss C 50mm F1.5 Sonnar + Amadeo adaptor",
        "source": "test",
        "source_url": "https://example.invalid/zeiss-50-adaptor-bundle",
    },
    index=13,
)


ADAPTER_BUNDLE_BODY = _record(
    {
        "brand": "Leica",
        "mount": "M",
        "category": "Body",
        "label": "M Body",
        "model_raw": "M10",
        "model_canonical": "M10",
        "variant": [],
        "focal_length": None,
        "title_raw": "Leica M10 Body with M-L Adapter",
        "source": "test",
        "source_url": "https://example.invalid/m10-adapter-bundle",
    },
    index=14,
)


E39_HOOD_ACCESSORY = _record(
    {
        "brand": "Other",
        "mount": "Unknown",
        "category": "Accessory",
        "label": "Accessory",
        "model_raw": None,
        "model_canonical": None,
        "variant": [],
        "focal_length": None,
        "accessory_type": "hood",
        "title_raw": "Overgaard Ventilated Lens Hood Black for 35mm, 28mm [e39]",
        "source": "test",
        "source_url": "https://example.invalid/hood-e39",
    },
    index=10,
)


def test_exact_family_and_focal_match_scores_high() -> None:
    result = score_listing(parse_query("35 summilux"), SUMMILUX_35)
    assert result["score"] >= 95
    assert result["match_quality"] == "medium"
    assert "model_family" in result["matched_fields"]
    assert "focal_length" in result["matched_fields"]


def test_alias_expanded_family_match_scores_high() -> None:
    result = score_listing(parse_query("35lux"), SUMMILUX_35)
    assert result["score"] >= 90
    model_items = [item for item in result["score_breakdown"] if item["field"] == "model_family"]
    assert model_items[0]["match_type"] == "alias_expanded"


def test_variant_hit_contributes_to_score() -> None:
    result = score_listing(parse_query("35lux aa"), SUMMILUX_35)
    assert result["score"] >= 90
    assert result["match_quality"] == "strong"
    assert "variant" in result["matched_fields"]


def test_override_listing_matches_on_final_output() -> None:
    result = score_listing(parse_query("mp3 silver"), MP3_SILVER)
    assert result["score"] == 100
    assert result["match_quality"] == "strong"
    assert result["used_override"] is True
    assert result["final_output"]["model_canonical"] == "MP3"


def test_short_cm_alias_matches_leica_cm_body() -> None:
    generic_leica = _record(
        {
            "brand": "Leica",
            "mount": "M",
            "category": "Lens",
            "label": "M Lens",
            "model_canonical": "Summilux-M",
            "variant": [],
            "focal_length": "50",
            "title_raw": "Leica M 50mm Summilux",
        },
        index=1,
    )
    ranked = rank_listings("leica cm", [generic_leica, CM_BODY], limit=2, min_score=1)

    assert ranked["intent"]["model_family"] == "CM"
    assert ranked["intent"]["system"] == "PNS"
    assert ranked["results"][0]["final_output"]["model_canonical"] == "CM"
    assert ranked["results"][0]["match_quality"] == "medium"


def test_body_shorthand_prefers_body_over_accessory() -> None:
    ranked = rank_listings("m6", [M6_ACCESSORY, M6_BODY, SUMMILUX_35], limit=3, min_score=1)

    assert ranked["intent"]["body_intent"] == "M6"
    assert ranked["intent"]["mount"] == "M"
    assert ranked["results"][0]["final_output"]["category"] == "Body"
    assert ranked["results"][0]["final_output"]["model_canonical"] == "M6"
    assert ranked["results"][0]["match_quality"] == "strong"
    assert any(result["final_output"]["category"] == "Accessory" for result in ranked["results"])
    accessory = next(result for result in ranked["results"] if result["final_output"]["category"] == "Accessory")
    assert accessory["match_quality"] == "weak"


def test_q3_bare_body_query_prefers_body_but_keeps_accessory_visible() -> None:
    ranked = rank_listings("q3", [Q3_ACCESSORY, Q3_BODY], limit=2, min_score=1)

    assert ranked["intent"]["body_intent"] == "Q3"
    assert ranked["intent"]["system"] == "Q"
    assert ranked["results"][0]["final_output"]["category"] == "Body"
    assert ranked["results"][0]["final_output"]["model_canonical"] == "Q3"
    assert ranked["results"][0]["match_quality"] == "strong"
    assert ranked["results"][1]["final_output"]["category"] == "Accessory"


def test_r_body_and_barnack_shorthand_rank_body_first() -> None:
    r_ranked = rank_listings("r8", [SUMMILUX_35, R8_BODY], limit=2, min_score=1)
    barnack_ranked = rank_listings("barnack", [SUMMILUX_35, BARNACK_IIIF_BODY], limit=2, min_score=1)
    iiif_ranked = rank_listings("iiif", [SUMMILUX_35, BARNACK_IIIF_BODY], limit=2, min_score=1)

    assert r_ranked["intent"]["body_intent"] == "R8"
    assert r_ranked["results"][0]["final_output"]["model_canonical"] == "R8"
    assert r_ranked["results"][0]["match_quality"] == "strong"
    assert barnack_ranked["intent"]["body_intent"] == "Barnack"
    assert barnack_ranked["results"][0]["final_output"]["category"] == "Body"
    assert iiif_ranked["intent"]["body_intent"] == "IIIf"
    assert iiif_ranked["results"][0]["final_output"]["model_canonical"] == "IIIf"


def test_body_intent_does_not_disturb_non_body_queries() -> None:
    lens = rank_listings("35lux aa", [Q3_BODY, SUMMILUX_35], limit=2, min_score=1)
    hood = rank_listings("leica hood", [Q3_BODY, HOOD_ACCESSORY], limit=2, min_score=1)
    adapter = rank_listings("adapter", [Q3_BODY, ADAPTER_ACCESSORY], limit=2, min_score=1)

    assert lens["intent"].get("body_intent") is None
    assert lens["results"][0]["final_output"]["category"] == "Lens"
    assert hood["intent"].get("body_intent") is None
    assert hood["results"][0]["final_output"]["accessory_type"] == "hood"
    assert adapter["intent"].get("body_intent") is None
    assert adapter["results"][0]["final_output"]["accessory_type"] == "adapter"


def test_hood_accessory_intent_prefers_accessory_over_broad_lens() -> None:
    ranked = rank_listings("leica hood", [SUMMILUX_35, HOOD_ACCESSORY], limit=2, min_score=1)

    assert ranked["intent"]["accessory_intent"] == "hood"
    assert ranked["results"][0]["final_output"]["category"] == "Accessory"
    assert ranked["results"][0]["match_quality"] == "medium"
    assert ranked["results"][1]["final_output"]["category"] == "Lens"
    assert "accessory_intent_non_accessory_listing" in ranked["results"][1]["warnings"]


def test_hood_accessory_code_ranks_exact_hood_first() -> None:
    ranked = rank_listings("12586 hood", [HOOD_ACCESSORY, HOOD_CODE_ACCESSORY, SUMMILUX_35], limit=3, min_score=1)

    assert ranked["intent"]["accessory_code"] == "12586"
    assert ranked["results"][0]["final_output"]["title_raw"] == "LEICA 12586 50mm F1.4 Hood"
    assert ranked["results"][0]["match_quality"] == "strong"
    assert "accessory_code" in ranked["results"][0]["matched_fields"]


def test_hood_intent_keeps_lens_bundle_visible_but_lower() -> None:
    ranked = rank_listings("zeiss 21mm f2.8 zm hood", [HOOD_ACCESSORY, HOOD_BUNDLE_LENS], limit=2, min_score=1)

    assert any(result["final_output"]["category"] == "Lens" for result in ranked["results"])
    bundle = next(result for result in ranked["results"] if result["final_output"]["category"] == "Lens")
    assert bundle["final_output"]["title_raw"] == "Zeiss 21mm F2.8 ZM + Hood - Silver"
    assert "accessory_intent" in bundle["matched_fields"]
    assert any(item["match_type"] == "bundle_text_hint" for item in bundle["score_breakdown"] if item["field"] == "accessory_intent")


def test_filter_accessory_intent_prefers_filter_over_broad_lens() -> None:
    ranked = rank_listings("uv filter", [SUMMILUX_35, FILTER_ACCESSORY], limit=2, min_score=1)

    assert ranked["intent"]["accessory_intent"] == "filter"
    assert ranked["results"][0]["final_output"]["category"] == "Accessory"
    assert ranked["results"][0]["final_output"]["accessory_type"] == "filter"
    assert ranked["results"][0]["match_quality"] == "medium"
    assert all(result["final_output"]["category"] == "Accessory" for result in ranked["results"])


def test_a36_filter_intent_ranks_a36_filter_first() -> None:
    ranked = rank_listings("a36 orange", [SUMMILUX_35, FILTER_ACCESSORY, FILTER_A36_ACCESSORY], limit=3, min_score=1)

    assert ranked["intent"]["accessory_intent"] == "filter"
    assert ranked["intent"]["filter_size"] == "A36"
    assert ranked["results"][0]["final_output"]["title_raw"] == "LEICA A36 Orange"
    assert "filter_size" in ranked["results"][0]["matched_fields"]


def test_filter_thread_does_not_promote_non_filter_accessory_above_filter() -> None:
    ranked = rank_listings("e39 filter", [E39_HOOD_ACCESSORY, FILTER_ACCESSORY], limit=2, min_score=1)

    assert ranked["intent"]["accessory_intent"] == "filter"
    assert ranked["intent"]["filter_size"] == "E39"
    assert ranked["results"][0]["final_output"]["accessory_type"] == "filter"
    assert ranked["results"][1]["final_output"]["accessory_type"] == "hood"


def test_filter_intent_keeps_lens_bundle_visible_but_lower_than_filter() -> None:
    ranked = rank_listings("summilux uva filter", [FILTER_ACCESSORY, FILTER_BUNDLE_LENS], limit=2, min_score=1)

    assert any(result["final_output"]["category"] == "Accessory" for result in ranked["results"])
    assert any(result["final_output"]["category"] == "Lens" for result in ranked["results"])
    bundle = next(result for result in ranked["results"] if result["final_output"]["category"] == "Lens")
    assert bundle["final_output"]["title_raw"] == "Used Leica Summilux-M 35mm f/1.4 ASPH FLE, silver - UVa Filter"
    assert "accessory_intent" in bundle["matched_fields"]
    assert any(item["match_type"] == "bundle_text_hint" for item in bundle["score_breakdown"] if item["field"] == "accessory_intent")


def test_adapter_accessory_intent_prefers_adapter_over_broad_lens() -> None:
    ranked = rank_listings("adapter", [SUMMILUX_35, ADAPTER_ACCESSORY], limit=2, min_score=1)

    assert ranked["intent"]["accessory_intent"] == "adapter"
    assert ranked["results"][0]["final_output"]["category"] == "Accessory"
    assert ranked["results"][0]["final_output"]["accessory_type"] == "adapter"
    assert ranked["results"][0]["match_quality"] == "strong"
    assert all(result["final_output"]["category"] == "Accessory" for result in ranked["results"])


def test_adaptor_variant_parses_and_matches_adapter_type() -> None:
    ranked = rank_listings("adaptor", [ADAPTER_ACCESSORY, ADAPTOR_ACCESSORY], limit=2, min_score=1)

    assert ranked["intent"]["accessory_intent"] == "adapter"
    assert ranked["results"][0]["final_output"]["category"] == "Accessory"
    assert ranked["results"][0]["final_output"]["accessory_type"] == "adapter"
    assert any(result["final_output"]["title_raw"] == "Amadeo adaptor for Contax RF to Leica M" for result in ranked["results"])


def test_adapter_intent_does_not_treat_compatibility_mount_as_listing_mount() -> None:
    ranked = rank_listings("m to l adapter", [SUMMILUX_35, ADAPTER_ACCESSORY], limit=2, min_score=1)

    assert ranked["intent"]["accessory_intent"] == "adapter"
    assert ranked["intent"]["mount"] is None
    assert ranked["results"][0]["final_output"]["category"] == "Accessory"
    assert ranked["results"][0]["score"] == 100.0


def test_macro_adapter_detail_ranks_macro_adapter_first() -> None:
    ranked = rank_listings("macro adapter m", [ADAPTER_ACCESSORY, ADAPTER_MACRO_ACCESSORY], limit=2, min_score=1)

    assert ranked["intent"]["accessory_intent"] == "adapter"
    assert ranked["intent"]["mount"] is None
    assert ranked["results"][0]["final_output"]["title_raw"] == "[위탁] Macro Adapter M"
    assert "adapter_detail" in ranked["results"][0]["matched_fields"]


def test_adapter_intent_keeps_lens_and_body_bundles_visible_but_lower() -> None:
    ranked = rank_listings(
        "zeiss 50mm f1.5 sonnar adapter",
        [ADAPTER_ACCESSORY, ADAPTER_BUNDLE_LENS, ADAPTER_BUNDLE_BODY],
        limit=3,
        min_score=1,
    )

    assert any(result["final_output"]["category"] == "Accessory" for result in ranked["results"])
    assert any(result["final_output"]["category"] == "Lens" for result in ranked["results"])
    bundle = next(result for result in ranked["results"] if result["final_output"]["category"] == "Lens")
    assert bundle["final_output"]["title_raw"] == "Carl Zeiss C 50mm F1.5 Sonnar + Amadeo adaptor"
    assert "accessory_intent" in bundle["matched_fields"]
    assert any(item["match_type"] == "bundle_text_hint" for item in bundle["score_breakdown"] if item["field"] == "accessory_intent")

    body_bundle = score_listing(parse_query("leica m adapter"), ADAPTER_BUNDLE_BODY)
    assert body_bundle["final_output"]["category"] == "Body"
    assert "accessory_intent" in body_bundle["matched_fields"]


def test_non_filter_query_keeps_existing_lens_ranking() -> None:
    ranked = rank_listings("35lux aa", [FILTER_ACCESSORY, SUMMILUX_35], limit=2, min_score=1)

    assert ranked["intent"]["accessory_intent"] is None
    assert ranked["results"][0]["final_output"]["category"] == "Lens"
    assert ranked["results"][0]["final_output"]["model_canonical"] == "Summilux-M"


def test_ambiguous_query_keeps_warnings() -> None:
    result = score_listing(parse_query("nice camera"), SUMMILUX_35)
    assert result["score"] == 0
    assert "ambiguous_query:no_structured_constraints" in result["warnings"]
    assert any(warning.startswith("unparsed_tokens:") for warning in result["warnings"])


def test_rank_listings_orders_by_score() -> None:
    summicron_50 = _record(
        {
            "brand": "Leica",
            "mount": "M",
            "category": "Lens",
            "label": "M Lens",
            "model_raw": "Summicron",
            "model_canonical": "Summicron-M",
            "variant": [],
            "focal_length": "50",
            "title_raw": "Leica M 50mm Summicron",
        }
    )
    ranked = rank_listings("35lux aa", [summicron_50, SUMMILUX_35], limit=2)
    assert ranked["results"][0]["final_output"]["model_canonical"] == "Summilux-M"


def test_strong_structured_match_ranks_above_mount_only_weak_match() -> None:
    summaron_l_35 = _record(
        {
            "brand": "Leica",
            "mount": "L",
            "category": "Lens",
            "label": "L Lens",
            "model_raw": "Summaron",
            "model_canonical": "Summaron",
            "variant": [],
            "focal_length": "35",
            "title_raw": "L 35mm Summaron f2.8",
        },
        index=2,
    )
    l_body_mount_only = _record(
        {
            "brand": "Leica",
            "mount": "L",
            "category": "Body",
            "label": "L Body",
            "model_raw": "If",
            "model_canonical": "If",
            "variant": [],
            "focal_length": None,
            "title_raw": "Leica IF Red Scale + 50mm F2.8",
        },
        index=1,
    )
    ranked = rank_listings("ltm summaron 35", [l_body_mount_only, summaron_l_35], limit=2, min_score=1)
    assert ranked["results"][0]["final_output"]["model_canonical"] == "Summaron"
    assert ranked["results"][0]["match_quality"] == "strong"
    assert ranked["results"][1]["match_quality"] == "weak"
    assert "weak_match" in ranked["results"][1]["warnings"]


def test_mount_system_mismatch_is_capped() -> None:
    m_lens = _record(
        {
            "brand": "Leica",
            "mount": "M",
            "category": "Lens",
            "label": "M Lens",
            "model_canonical": "Summilux-M",
            "variant": [],
            "focal_length": "28",
            "title_raw": "Leica M 28mm Summilux",
        }
    )
    q_body = _record(
        {
            "brand": "Leica",
            "mount": "Q",
            "category": "Body",
            "label": "Q Body",
            "model_canonical": "Q3",
            "variant": [],
            "focal_length": None,
            "title_raw": "Leica Q3 28mm",
        }
    )
    ranked = rank_listings("q3 28", [m_lens, q_body], limit=2)
    assert ranked["results"][0]["final_output"]["mount"] == "Q"
    assert ranked["results"][1]["score"] <= 40.0
    assert ranked["results"][1]["match_quality"] == "weak"
    assert "body_intent_non_body_listing" in ranked["results"][1]["warnings"]


def test_aperture_hint_breaks_focal_mount_tie() -> None:
    m_21_f14 = _record(
        {
            "brand": "Leica",
            "mount": "M",
            "category": "Lens",
            "label": "M Lens",
            "model_canonical": "Summilux-M",
            "variant": [],
            "focal_length": "21",
            "title_raw": "Leica M 21mm f1.4 Summilux",
        }
    )
    m_21_f28 = _record(
        {
            "brand": "Leica",
            "mount": "M",
            "category": "Lens",
            "label": "M Lens",
            "model_canonical": "Elmarit-M",
            "variant": [],
            "focal_length": "21",
            "title_raw": "Leica M 21mm f2.8 Elmarit",
        }
    )
    ranked = rank_listings("m 21/2.8", [m_21_f14, m_21_f28], limit=2)
    assert ranked["results"][0]["final_output"]["model_canonical"] == "Elmarit-M"
    assert "aperture_hint" in ranked["results"][0]["matched_fields"]


def test_standalone_aperture_ranks_exact_aperture_above_broad_fallback() -> None:
    m_50_f12 = _record(
        {
            "brand": "Leica",
            "mount": "M",
            "category": "Lens",
            "label": "M Lens",
            "model_canonical": "Noctilux",
            "variant": ["f1.2"],
            "focal_length": "50",
            "title_raw": "Leica M 50mm f1.2 Noctilux 1st Black",
        },
        index=2,
    )
    m_50_f14 = _record(
        {
            "brand": "Leica",
            "mount": "M",
            "category": "Lens",
            "label": "M Lens",
            "model_canonical": "Summilux-M",
            "variant": ["f1.4"],
            "focal_length": "50",
            "title_raw": "Leica M 50mm f1.4 Summilux",
        },
        index=1,
    )
    ranked = rank_listings("leica 50mm 1.2 m", [m_50_f14, m_50_f12], limit=2, min_score=1)

    assert ranked["intent"]["aperture"] == "1.2"
    assert ranked["results"][0]["final_output"]["model_canonical"] == "Noctilux"
    assert ranked["results"][0]["match_quality"] == "strong"
    assert ranked["results"][1]["score"] == 72.0
    assert ranked["results"][1]["match_quality"] == "weak"
    assert "essential_constraint_mismatch:aperture" in ranked["results"][1]["warnings"]


def test_prefixed_aperture_and_generation_find_exact_first_version() -> None:
    noctilux_first = _record(
        {
            "brand": "Leica",
            "mount": "M",
            "category": "Lens",
            "label": "M Lens",
            "model_canonical": "Noctilux",
            "variant": ["f1.2", "v1"],
            "focal_length": "50",
            "title_raw": "Leica M 50mm f1.2 Noctilux 1st Black",
        },
        index=1,
    )
    summilux_first = _record(
        {
            "brand": "Leica",
            "mount": "M",
            "category": "Lens",
            "label": "M Lens",
            "model_canonical": "Summilux-M",
            "variant": ["f1.4", "v1"],
            "focal_length": "50",
            "title_raw": "Leica M 50mm f1.4 Summilux 1st",
        },
        index=2,
    )
    ranked = rank_listings("leica 50mm f1.2 1st", [summilux_first, noctilux_first], limit=2, min_score=1)

    assert ranked["results"][0]["final_output"]["model_canonical"] == "Noctilux"
    assert ranked["results"][0]["match_quality"] == "strong"
    assert ranked["results"][1]["match_quality"] == "weak"


def test_brand_unspecified_query_uses_soft_preference_for_strong_ties() -> None:
    zeiss_21 = _record(
        {
            "brand": "Zeiss",
            "mount": "M",
            "category": "Lens",
            "label": "M Lens",
            "model_canonical": "Biogon",
            "variant": [],
            "focal_length": "21",
            "title_raw": "Zeiss M 21mm f2.8 Biogon ZM",
        },
        index=1,
    )
    leica_21 = _record(
        {
            "brand": "Leica",
            "mount": "M",
            "category": "Lens",
            "label": "M Lens",
            "model_canonical": "Elmarit-M",
            "variant": [],
            "focal_length": "21",
            "title_raw": "Leica M 21mm f2.8 Elmarit-M",
        },
        index=2,
    )
    voigtlander_21 = _record(
        {
            "brand": "Voigtlander",
            "mount": "M",
            "category": "Lens",
            "label": "M Lens",
            "model_canonical": "Color-Skopar",
            "variant": [],
            "focal_length": "21",
            "title_raw": "Voigtlander M 21mm f2.8 Color-Skopar",
        },
        index=3,
    )
    ranked = rank_listings("m 21/2.8", [zeiss_21, leica_21, voigtlander_21], limit=3)

    assert [result["match_quality"] for result in ranked["results"]] == ["strong", "strong", "strong"]
    assert ranked["results"][0]["final_output"]["brand"] == "Leica"
    assert ranked["results"][0]["score"] == 100.0
    assert ranked["results"][0]["implicit_brand_preference_score"] > ranked["results"][1]["implicit_brand_preference_score"]
    assert "listing_brand_matches_default:Leica" in ranked["results"][0]["implicit_brand_preference_reasons"]


def test_explicit_brand_query_does_not_add_implicit_preference() -> None:
    zeiss_21 = _record(
        {
            "brand": "Zeiss",
            "mount": "M",
            "category": "Lens",
            "label": "M Lens",
            "model_canonical": "Biogon",
            "variant": [],
            "focal_length": "21",
            "title_raw": "Zeiss M 21mm f2.8 Biogon ZM",
        },
        index=1,
    )
    leica_21 = _record(
        {
            "brand": "Leica",
            "mount": "M",
            "category": "Lens",
            "label": "M Lens",
            "model_canonical": "Elmarit-M",
            "variant": [],
            "focal_length": "21",
            "title_raw": "Leica M 21mm f2.8 Elmarit-M",
        },
        index=2,
    )
    ranked = rank_listings("leica m 21/2.8", [zeiss_21, leica_21], limit=2, min_score=1)

    assert ranked["results"][0]["final_output"]["brand"] == "Leica"
    assert all(result["implicit_brand_preference_score"] == 0.0 for result in ranked["results"])
    assert "hard_constraint_mismatch:brand" in ranked["results"][1]["warnings"]


def test_implicit_preference_does_not_promote_weak_result() -> None:
    leica_mount_only = _record(
        {
            "brand": "Leica",
            "mount": "M",
            "category": "Body",
            "label": "M Body",
            "model_canonical": "M3",
            "variant": [],
            "focal_length": None,
            "title_raw": "Leica M3 Body",
        },
        index=1,
    )
    zeiss_21 = _record(
        {
            "brand": "Zeiss",
            "mount": "M",
            "category": "Lens",
            "label": "M Lens",
            "model_canonical": "Biogon",
            "variant": [],
            "focal_length": "21",
            "title_raw": "Zeiss M 21mm f2.8 Biogon ZM",
        },
        index=2,
    )
    ranked = rank_listings("m 21/2.8", [leica_mount_only, zeiss_21], limit=2, min_score=1)

    assert ranked["results"][0]["final_output"]["brand"] == "Zeiss"
    assert ranked["results"][0]["match_quality"] == "strong"
    assert ranked["results"][1]["match_quality"] == "weak"
    assert ranked["results"][1]["implicit_brand_preference_score"] == 0.0


if __name__ == "__main__":
    test_exact_family_and_focal_match_scores_high()
    test_alias_expanded_family_match_scores_high()
    test_variant_hit_contributes_to_score()
    test_override_listing_matches_on_final_output()
    test_short_cm_alias_matches_leica_cm_body()
    test_body_shorthand_prefers_body_over_accessory()
    test_q3_bare_body_query_prefers_body_but_keeps_accessory_visible()
    test_r_body_and_barnack_shorthand_rank_body_first()
    test_body_intent_does_not_disturb_non_body_queries()
    test_hood_accessory_intent_prefers_accessory_over_broad_lens()
    test_hood_accessory_code_ranks_exact_hood_first()
    test_hood_intent_keeps_lens_bundle_visible_but_lower()
    test_filter_accessory_intent_prefers_filter_over_broad_lens()
    test_a36_filter_intent_ranks_a36_filter_first()
    test_filter_thread_does_not_promote_non_filter_accessory_above_filter()
    test_filter_intent_keeps_lens_bundle_visible_but_lower_than_filter()
    test_adapter_accessory_intent_prefers_adapter_over_broad_lens()
    test_adaptor_variant_parses_and_matches_adapter_type()
    test_adapter_intent_does_not_treat_compatibility_mount_as_listing_mount()
    test_macro_adapter_detail_ranks_macro_adapter_first()
    test_adapter_intent_keeps_lens_and_body_bundles_visible_but_lower()
    test_non_filter_query_keeps_existing_lens_ranking()
    test_ambiguous_query_keeps_warnings()
    test_rank_listings_orders_by_score()
    test_strong_structured_match_ranks_above_mount_only_weak_match()
    test_mount_system_mismatch_is_capped()
    test_aperture_hint_breaks_focal_mount_tie()
    test_standalone_aperture_ranks_exact_aperture_above_broad_fallback()
    test_prefixed_aperture_and_generation_find_exact_first_version()
    test_brand_unspecified_query_uses_soft_preference_for_strong_ties()
    test_explicit_brand_query_does_not_add_implicit_preference()
    test_implicit_preference_does_not_promote_weak_result()
    print("test_query_resolver: ok")
