from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from search_index import clear_search_index_cache, write_search_index
from search_service import load_and_search, search_records


def _record(index: int, final_output: dict, override_applied: bool = False) -> dict:
    return {
        "record_index": index,
        "raw_item": {
            "site": final_output.get("source"),
            "상품명": final_output.get("title_raw"),
            "링크": final_output.get("source_url"),
            "system": final_output.get("system"),
        },
        "classifier_output": {
            "brand": "Unknown",
            "mount": "Unknown",
            "category": "Lens",
            "label": "Lens",
            "model_canonical": None,
        },
        "final_output": final_output,
        "override_applied": override_applied,
        "audit_trail": [
            {"changed_fields": {"mount": {"before": "Unknown", "after": "M"}}}
        ] if override_applied else [],
    }


SUMMILUX_HIGH = _record(
    1,
    {
        "source": "A dealer",
        "source_url": "https://example.invalid/high",
        "title_raw": "Leica M 35mm Summilux ASPH AA",
        "price_raw": "7,300,000원",
        "currency": "KRW",
        "condition_raw": "98%",
        "brand": "Leica",
        "mount": "M",
        "category": "Lens",
        "label": "M Lens",
        "model_raw": "Summilux",
        "model_canonical": "Summilux-M",
        "variant": ["ASPH", "AA"],
        "focal_length": "35",
        "sold_quality": "asking",
    },
)

SUMMILUX_LOW = _record(
    2,
    {
        "source": "B dealer",
        "source_url": "https://example.invalid/low",
        "title_raw": "Leica M 35mm Summilux ASPH AA",
        "price_raw": "6,100,000원",
        "currency": "KRW",
        "condition_raw": "95%",
        "brand": "Leica",
        "mount": "M",
        "category": "Lens",
        "label": "M Lens",
        "model_raw": "Summilux",
        "model_canonical": "Summilux-M",
        "variant": ["ASPH", "AA"],
        "focal_length": "35",
        "sold_quality": "sold_confirmed",
    },
)

SUMMICRON_50 = _record(
    3,
    {
        "source": "C dealer",
        "source_url": "https://example.invalid/cron",
        "title_raw": "Leica M 50mm Summicron",
        "price_raw": "2,000,000원",
        "currency": "KRW",
        "condition_raw": "90%",
        "brand": "Leica",
        "mount": "M",
        "category": "Lens",
        "label": "M Lens",
        "model_raw": "Summicron",
        "model_canonical": "Summicron-M",
        "variant": [],
        "focal_length": "50",
        "sold_quality": "asking",
    },
)

MP3_SILVER = _record(
    4,
    {
        "source": "Trusted dealer",
        "source_url": "https://example.invalid/mp3",
        "title_raw": "[위탁] MP3 (Silver)",
        "price_raw": "20,500,000원",
        "currency": "KRW",
        "condition_raw": "93%",
        "brand": "Leica",
        "mount": "M",
        "category": "Body",
        "label": "M Body",
        "model_raw": None,
        "model_canonical": "MP3",
        "variant": ["Silver"],
        "focal_length": None,
        "sold_quality": "asking",
    },
    override_applied=True,
)

SUMMARON_L_35 = _record(
    5,
    {
        "source": "L dealer",
        "source_url": "https://example.invalid/summaron",
        "title_raw": "L 35mm Summaron f2.8",
        "price_raw": "900,000원",
        "currency": "KRW",
        "condition_raw": "92%",
        "brand": "Leica",
        "mount": "L",
        "category": "Lens",
        "label": "L Lens",
        "model_raw": "Summaron",
        "model_canonical": "Summaron",
        "variant": [],
        "focal_length": "35",
        "sold_quality": "asking",
    },
)

L_BODY_WEAK_LOW_PRICE = _record(
    6,
    {
        "source": "Cheap dealer",
        "source_url": "https://example.invalid/l-body",
        "title_raw": "Leica IF Red Scale + 50mm F2.8",
        "price_raw": "100,000원",
        "currency": "KRW",
        "condition_raw": "Used",
        "brand": "Leica",
        "mount": "L",
        "category": "Body",
        "label": "L Body",
        "model_raw": "If",
        "model_canonical": "If",
        "variant": [],
        "focal_length": None,
        "sold_quality": "asking",
    },
)


def test_pagination_fields_and_next_offset() -> None:
    response = search_records("35lux aa", [SUMMILUX_HIGH, SUMMILUX_LOW, SUMMICRON_50], limit=1)
    assert response["pagination"]["limit"] == 1
    assert response["pagination"]["offset"] == 0
    assert response["pagination"]["has_more"] is True
    assert response["pagination"]["next_offset"] == 1
    assert response["result_count"] == 1


def test_offset_pagination_returns_second_page() -> None:
    response = search_records("35lux aa", [SUMMILUX_HIGH, SUMMILUX_LOW], limit=1, offset=1)
    assert response["pagination"]["offset"] == 1
    assert response["result_count"] == 1
    assert response["pagination"]["has_more"] is False


def test_sold_quality_category_brand_filters() -> None:
    response = search_records(
        "35lux aa",
        [SUMMILUX_HIGH, SUMMILUX_LOW, MP3_SILVER],
        filters={"sold_quality": "asking", "category": "Lens", "brand": "Leica"},
    )
    assert response["result_count"] == 1
    assert response["results"][0]["source_url"] == "https://example.invalid/high"


def test_relevance_default_sort_is_preserved() -> None:
    response = search_records("35lux aa", [SUMMICRON_50, SUMMILUX_HIGH], limit=2)
    assert response["applied_sort"] == "relevance"
    assert response["results"][0]["final_output"]["model_canonical"] == "Summilux-M"
    assert response["results"][0]["match_quality"] == "strong"


def test_price_sort_ascending() -> None:
    response = search_records("35lux aa", [SUMMILUX_HIGH, SUMMILUX_LOW], limit=2, sort="price_asc")
    assert response["applied_sort"] == "price_asc"
    assert response["results"][0]["price"] == "6,100,000원"


def test_default_min_score_filters_mount_only_weak_matches() -> None:
    response = search_records(
        "ltm summaron 35",
        [L_BODY_WEAK_LOW_PRICE],
        filters={"brand": "Leica", "mount": "L"},
    )
    assert response["total_ranked"] == 0
    assert response["result_count"] == 0
    assert response["applied_quality_filter"]["min_score"] == 25.0


def test_price_sort_keeps_strong_match_above_cheap_weak_match() -> None:
    response = search_records(
        "ltm summaron 35",
        [L_BODY_WEAK_LOW_PRICE, SUMMARON_L_35],
        sort="price_asc",
        min_score=1,
    )
    assert response["results"][0]["final_output"]["model_canonical"] == "Summaron"
    assert response["results"][0]["match_quality"] == "strong"
    assert response["results"][1]["match_quality"] == "weak"


def test_quality_summary_keeps_weak_as_broader_matches_after_strong() -> None:
    response = search_records(
        "ltm summaron 35",
        [L_BODY_WEAK_LOW_PRICE, SUMMARON_L_35],
        min_score=1,
    )
    summary = response["result_quality_summary"]

    assert summary["strong_result_count"] == 1
    assert summary["weak_result_count"] == 1
    assert summary["fallback_applied"] is False
    assert summary["fallback_reason"] == "strong_results_first_broader_matches_available"
    assert "Broader matches" in summary["display_message"]


def test_quality_summary_marks_fallback_when_no_strong_results() -> None:
    response = search_records(
        "ltm summaron 35",
        [L_BODY_WEAK_LOW_PRICE],
        min_score=1,
    )
    summary = response["result_quality_summary"]

    assert summary["strong_result_count"] == 0
    assert summary["weak_result_count"] == 1
    assert summary["fallback_applied"] is True
    assert summary["fallback_reason"] == "no_strong_results_weak_matches_included"


def test_strong_only_filters_medium_and_weak_matches() -> None:
    response = search_records(
        "ltm summaron 35",
        [L_BODY_WEAK_LOW_PRICE, SUMMARON_L_35],
        strong_only=True,
        min_score=1,
    )
    assert response["result_count"] == 1
    assert response["results"][0]["match_quality"] == "strong"
    assert response["applied_quality_filter"]["strong_only"] is True
    assert response["result_quality_summary"]["fallback_applied"] is False
    assert response["result_quality_summary"]["fallback_reason"] == "strong_only_enabled"


def test_debug_hidden_by_default() -> None:
    response = search_records("mp3 silver", [MP3_SILVER], limit=1)
    assert "debug" not in response["results"][0]


def test_debug_visible_when_requested() -> None:
    response = search_records("mp3 silver", [MP3_SILVER], limit=1, include_debug=True)
    assert response["results"][0]["debug"]["classifier_output"]["brand"] == "Unknown"
    assert response["results"][0]["debug"]["audit_trail"][0]["changed_fields"]["mount"]["after"] == "M"


def test_empty_result_response() -> None:
    response = search_records("35lux aa", [], limit=5)
    assert response["total_ranked"] == 0
    assert response["result_count"] == 0
    assert response["pagination"]["has_more"] is False
    assert "no_results" in response["warnings"]
    assert response["result_quality_summary"]["fallback_applied"] is False
    assert response["result_quality_summary"]["fallback_reason"] == "no_results"


def test_out_of_range_offset_warning() -> None:
    response = search_records("35lux aa", [SUMMILUX_HIGH], limit=5, offset=99)
    assert response["result_count"] == 0
    assert "offset_out_of_range" in response["warnings"]


def test_load_and_search_uses_compact_index_cache_without_changing_results() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        resolved_path = tmp_path / "resolved.json"
        output_path = tmp_path / "search_index.json"
        resolved_path.write_text(json.dumps([SUMMILUX_HIGH], ensure_ascii=False), encoding="utf-8")
        write_search_index(resolved_path, output_path)

        clear_search_index_cache(output_path)
        cached = load_and_search("35lux aa", path=output_path, limit=1)
        uncached = load_and_search("35lux aa", path=output_path, limit=1, use_cache=False)

        assert cached["result_count"] == uncached["result_count"] == 1
        assert cached["results"][0]["final_output"] == uncached["results"][0]["final_output"]
        assert cached["results"][0]["match_quality"] == "strong"


if __name__ == "__main__":
    test_pagination_fields_and_next_offset()
    test_offset_pagination_returns_second_page()
    test_sold_quality_category_brand_filters()
    test_relevance_default_sort_is_preserved()
    test_price_sort_ascending()
    test_default_min_score_filters_mount_only_weak_matches()
    test_price_sort_keeps_strong_match_above_cheap_weak_match()
    test_quality_summary_keeps_weak_as_broader_matches_after_strong()
    test_quality_summary_marks_fallback_when_no_strong_results()
    test_strong_only_filters_medium_and_weak_matches()
    test_debug_hidden_by_default()
    test_debug_visible_when_requested()
    test_empty_result_response()
    test_out_of_range_offset_warning()
    test_load_and_search_uses_compact_index_cache_without_changing_results()
    print("test_search_service: ok")
