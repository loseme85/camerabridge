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
    assert ranked["results"][1]["score"] == 40.0
    assert ranked["results"][1]["match_quality"] == "weak"


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
    test_ambiguous_query_keeps_warnings()
    test_rank_listings_orders_by_score()
    test_strong_structured_match_ranks_above_mount_only_weak_match()
    test_mount_system_mismatch_is_capped()
    test_aperture_hint_breaks_focal_mount_tie()
    test_brand_unspecified_query_uses_soft_preference_for_strong_ties()
    test_explicit_brand_query_does_not_add_implicit_preference()
    test_implicit_preference_does_not_promote_weak_result()
    print("test_query_resolver: ok")
