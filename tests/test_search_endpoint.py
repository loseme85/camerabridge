from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from api.search import endpoint_response, parse_search_params


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


SUMMILUX_35 = _record(
    1,
    {
        "source": "A dealer",
        "source_url": "https://example.invalid/summilux-high",
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
        "source_url": "https://example.invalid/summilux-low",
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
        "sold_quality": "asking",
    },
)

MP3_SILVER = _record(
    3,
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

Q3_BODY = _record(
    4,
    {
        "source": "Q dealer",
        "source_url": "https://example.invalid/q3",
        "title_raw": "[중고] Q3 28mm",
        "price_raw": "7,900,000원",
        "currency": "KRW",
        "condition_raw": "97%",
        "brand": "Leica",
        "mount": "Q",
        "category": "Body",
        "label": "Q Body",
        "model_raw": "Q3",
        "model_canonical": "Q3",
        "variant": [],
        "focal_length": "28",
        "sold_quality": "asking",
    },
)

RECORDS = [SUMMILUX_35, SUMMILUX_LOW, MP3_SILVER, Q3_BODY]


def test_parse_required_and_optional_params() -> None:
    parsed = parse_search_params({
        "q": ["35lux aa"],
        "limit": ["2"],
        "offset": ["1"],
        "sort": ["price_asc"],
        "category": ["Lens"],
        "include_debug": ["true"],
        "min_score": ["42.5"],
        "strong_only": ["true"],
    })
    assert parsed["query"] == "35lux aa"
    assert parsed["limit"] == 2
    assert parsed["offset"] == 1
    assert parsed["sort"] == "price_asc"
    assert parsed["filters"]["category"] == "Lens"
    assert parsed["include_debug"] is True
    assert parsed["min_score"] == 42.5
    assert parsed["strong_only"] is True


def test_endpoint_response_has_service_schema_fields() -> None:
    status, response = endpoint_response({"q": "mp3 silver", "limit": "1"}, records=RECORDS)
    assert status == 200
    assert response["schema_version"] == "search_service.v1"
    assert response["query"] == "mp3 silver"
    assert "intent" in response
    assert "pagination" in response
    assert response["results"][0]["used_override"] is True


def test_debug_toggle_hides_and_shows_classifier_output() -> None:
    status, hidden = endpoint_response({"q": "mp3 silver", "limit": "1"}, records=RECORDS)
    assert status == 200
    assert "debug" not in hidden["results"][0]

    status, debug = endpoint_response(
        {"q": "mp3 silver", "limit": "1", "include_debug": "true"},
        records=RECORDS,
    )
    assert status == 200
    assert debug["results"][0]["debug"]["classifier_output"]["brand"] == "Unknown"


def test_pagination_filter_and_sort_are_connected() -> None:
    status, response = endpoint_response(
        {
            "q": "35lux aa",
            "limit": "1",
            "offset": "1",
            "category": "Lens",
            "brand": "Leica",
            "sort": "price_asc",
        },
        records=RECORDS,
    )
    assert status == 200
    assert response["pagination"]["offset"] == 1
    assert response["applied_filters"]["category"] == "Lens"
    assert response["applied_sort"] == "price_asc"
    assert response["results"][0]["price"] == "7,300,000원"


def test_quality_options_are_connected() -> None:
    status, response = endpoint_response(
        {"q": "q3 28", "strong_only": "true", "min_score": "1"},
        records=RECORDS,
    )
    assert status == 200
    assert response["applied_quality_filter"]["strong_only"] is True
    assert response["applied_quality_filter"]["min_score"] == 1.0
    assert response["result_count"] == 1
    assert response["results"][0]["final_output"]["category"] == "Body"
    assert response["results"][0]["match_quality"] == "strong"


def test_empty_result_is_success_with_no_results_warning() -> None:
    status, response = endpoint_response({"q": "nocti e60", "category": "Accessory"}, records=RECORDS)
    assert status == 200
    assert response["result_count"] == 0
    assert "no_results" in response["warnings"]


def test_missing_query_returns_400() -> None:
    status, response = endpoint_response({}, records=RECORDS)
    assert status == 400
    assert response["schema_version"] == "search_service.error.v1"
    assert response["error"]["code"] == "missing_query"


def test_invalid_params_return_400() -> None:
    status, response = endpoint_response({"q": "q3 28", "limit": "0"}, records=RECORDS)
    assert status == 400
    assert response["error"]["code"] == "invalid_limit"

    status, response = endpoint_response({"q": "q3 28", "category": "Camera"}, records=RECORDS)
    assert status == 400
    assert response["error"]["code"] == "invalid_category"

    status, response = endpoint_response({"q": "q3 28", "price_min": "expensive"}, records=RECORDS)
    assert status == 400
    assert response["error"]["code"] == "invalid_price_min"

    status, response = endpoint_response({"q": "q3 28", "min_score": "101"}, records=RECORDS)
    assert status == 400
    assert response["error"]["code"] == "invalid_min_score"


def test_data_file_missing_returns_503() -> None:
    missing = Path(__file__).resolve().parents[1] / "data/derived/does_not_exist.json"
    status, response = endpoint_response({"q": "q3 28"}, path=missing)
    assert status == 503
    assert response["error"]["code"] == "data_file_missing"


if __name__ == "__main__":
    test_parse_required_and_optional_params()
    test_endpoint_response_has_service_schema_fields()
    test_debug_toggle_hides_and_shows_classifier_output()
    test_pagination_filter_and_sort_are_connected()
    test_quality_options_are_connected()
    test_empty_result_is_success_with_no_results_warning()
    test_missing_query_returns_400()
    test_invalid_params_return_400()
    test_data_file_missing_returns_503()
    print("test_search_endpoint: ok")
