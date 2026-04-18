from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from search_response import build_search_response


def _record(final_output: dict, override_applied: bool = False) -> dict:
    return {
        "record_index": 7 if override_applied else 3,
        "raw_item": {
            "site": final_output.get("source"),
            "상품명": final_output.get("title_raw"),
            "링크": final_output.get("source_url"),
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


SUMMILUX_35 = _record(
    {
        "source": "test",
        "source_url": "https://example.invalid/summilux-35-aa",
        "title_raw": "Leica M 35mm Summilux ASPH AA",
        "price_raw": "7,300,000원",
        "currency": "KRW",
        "image_url": "https://example.invalid/summilux.jpg",
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
    }
)


MP3_SILVER = _record(
    {
        "source": "trusted",
        "source_url": "https://example.invalid/mp3-silver",
        "title_raw": "[위탁] MP3 (Silver)",
        "price_raw": "20,500,000원",
        "currency": "KRW",
        "image_url": "https://example.invalid/mp3.jpg",
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


def test_response_has_required_top_level_fields() -> None:
    response = build_search_response("35lux aa", [SUMMILUX_35], limit=1)
    assert response["schema_version"] == "search_response.v1"
    assert response["query"] == "35lux aa"
    assert "intent" in response
    assert "results" in response
    assert response["result_count"] == 1


def test_result_has_required_public_fields() -> None:
    response = build_search_response("35lux aa", [SUMMILUX_35], limit=1)
    result = response["results"][0]
    for field_name in [
        "score",
        "title",
        "price",
        "source",
        "source_url",
        "final_output",
        "used_override",
        "match_quality",
        "matched_fields",
        "score_breakdown",
        "warnings",
    ]:
        assert field_name in result
    assert result["final_output"]["model_canonical"] == "Summilux-M"
    assert result["match_quality"] == "strong"


def test_used_override_is_visible() -> None:
    response = build_search_response("mp3 silver", [MP3_SILVER], limit=1)
    result = response["results"][0]
    assert result["used_override"] is True
    assert result["final_output"]["model_canonical"] == "MP3"


def test_matched_fields_and_score_breakdown_are_included() -> None:
    response = build_search_response("35lux aa", [SUMMILUX_35], limit=1)
    result = response["results"][0]
    assert "model_family" in result["matched_fields"]
    assert any(item["field"] == "model_family" for item in result["score_breakdown"])


def test_empty_results_add_response_warning() -> None:
    response = build_search_response("35lux aa", [], limit=5)
    assert response["result_count"] == 0
    assert response["results"] == []
    assert "no_results" in response["warnings"]


def test_ambiguous_query_preserves_parser_warning() -> None:
    response = build_search_response("nice camera", [SUMMILUX_35], limit=5)
    assert response["result_count"] == 0
    assert "no_structured_search_intent" in response["warnings"]
    assert "no_results" in response["warnings"]


def test_debug_mode_can_expose_classifier_and_audit() -> None:
    response = build_search_response("mp3 silver", [MP3_SILVER], limit=1, include_debug=True)
    debug = response["results"][0]["debug"]
    assert debug["match_quality_rank"] == 3
    assert debug["classifier_output"]["brand"] == "Unknown"
    assert debug["audit_trail"][0]["changed_fields"]["mount"]["after"] == "M"


if __name__ == "__main__":
    test_response_has_required_top_level_fields()
    test_result_has_required_public_fields()
    test_used_override_is_visible()
    test_matched_fields_and_score_breakdown_are_included()
    test_empty_results_add_response_warning()
    test_ambiguous_query_preserves_parser_warning()
    test_debug_mode_can_expose_classifier_and_audit()
    print("test_search_response: ok")
