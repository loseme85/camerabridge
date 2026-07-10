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

M6_CLASSIC = _record(
    5,
    {
        "source": "Body dealer",
        "source_url": "https://example.invalid/m6-classic",
        "title_raw": "Leica M6 Classic Silver x0.72 [Big Logo]",
        "price_raw": "4,100,000원",
        "currency": "KRW",
        "condition_raw": "92%",
        "brand": "Leica",
        "mount": "M",
        "category": "Body",
        "label": "M Body",
        "model_raw": "M6",
        "model_canonical": "M6",
        "variant": [],
        "focal_length": None,
        "sold_quality": "asking",
    },
)

M6_TTL = _record(
    6,
    {
        "source": "Body dealer",
        "source_url": "https://example.invalid/m6-ttl",
        "title_raw": "Leica M6 TTL Silver 0.72x",
        "price_raw": "4,900,000원",
        "currency": "KRW",
        "condition_raw": "93%",
        "brand": "Leica",
        "mount": "M",
        "category": "Body",
        "label": "M Body",
        "model_raw": "M6",
        "model_canonical": "M6",
        "variant": [],
        "focal_length": None,
        "sold_quality": "asking",
    },
)

TYPE_IV_A = _record(
    7,
    {
        "source": "Lens dealer",
        "source_url": "https://example.invalid/type-iv-a",
        "title_raw": "Leica 50mm f2 Summicron-M (Type IV) (Black, 11819)",
        "price_raw": "2,900,000원",
        "currency": "KRW",
        "condition_raw": "94%",
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

TYPE_IV_B = _record(
    8,
    {
        "source": "Lens dealer",
        "source_url": "https://example.invalid/type-iv-b",
        "title_raw": "Leica 50mm Summicron-M Type IV Black",
        "price_raw": "3,100,000원",
        "currency": "KRW",
        "condition_raw": "95%",
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

M10_BODY = _record(
    9,
    {
        "source": "Body dealer",
        "source_url": "https://example.invalid/m10",
        "title_raw": "Leica M10 Silver",
        "price_raw": "5,800,000원",
        "currency": "KRW",
        "condition_raw": "93%",
        "brand": "Leica",
        "mount": "M",
        "category": "Body",
        "label": "M Body",
        "model_raw": "M10",
        "model_canonical": "M10",
        "variant": [],
        "focal_length": None,
        "sold_quality": "asking",
    },
)

M10_P_A = _record(
    10,
    {
        "source": "Body dealer",
        "source_url": "https://example.invalid/m10p-a",
        "title_raw": "LEICA M10-P sn.5506",
        "price_raw": "6,000,000원",
        "currency": "KRW",
        "condition_raw": "95%",
        "brand": "Leica",
        "mount": "M",
        "category": "Body",
        "label": "M Body",
        "model_raw": "M10-P",
        "model_canonical": "M10-P",
        "variant": [],
        "focal_length": None,
        "sold_quality": "asking",
    },
)

M10_P_B = _record(
    11,
    {
        "source": "Body dealer",
        "source_url": "https://example.invalid/m10p-b",
        "title_raw": "LEICA M10-P sn.5488",
        "price_raw": "7,200,000원",
        "currency": "KRW",
        "condition_raw": "94%",
        "brand": "Leica",
        "mount": "M",
        "category": "Body",
        "label": "M Body",
        "model_raw": "M10-P",
        "model_canonical": "M10-P",
        "variant": [],
        "focal_length": None,
        "sold_quality": "asking",
    },
)

M10_ACCESSORY = _record(
    12,
    {
        "source": "Accessory dealer",
        "source_url": "https://example.invalid/m10-holster",
        "title_raw": "[중고] Leica M10 홀스터",
        "price_raw": "120,000원",
        "currency": "KRW",
        "condition_raw": "used",
        "brand": "Leica",
        "mount": "M",
        "category": "Accessory",
        "label": "Accessory",
        "model_raw": "M10",
        "model_canonical": "M10",
        "variant": [],
        "focal_length": None,
        "sold_quality": "asking",
    },
)

GENERATION_RECORDS = RECORDS + [
    M6_CLASSIC,
    M6_TTL,
    TYPE_IV_A,
    TYPE_IV_B,
    M10_BODY,
    M10_P_A,
    M10_P_B,
    M10_ACCESSORY,
]


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


def test_broad_parent_generation_gate_syncs_top_level_and_market_entry_policy() -> None:
    status, response = endpoint_response({"q": "Leica M6", "limit": "12"}, records=GENERATION_RECORDS)
    assert status == 200
    assert response["price_summary_allowed"] is False
    assert response["price_scope"] == "generation_disambiguation_required"
    assert response["display_price_summary_allowed"] is False
    assert response["display_price_band"] == "Generation selection needed"
    assert response["market_entry_policy"]["price_summary_allowed"] is False
    assert response["market_entry_policy"]["price_scope"] == "generation_disambiguation_required"
    assert response["market_entry_policy"]["display_price_summary_allowed"] is False
    assert response["market_entry_policy"]["display_price_band"] == "Generation selection needed"
    assert response["market_entry_policy"]["display_query_review"]["interpreted_target"] == "Leica M6"
    assert sum(1 for item in response["results"] if item.get("used_for_price")) == 0


def test_exact_generation_syncs_generation_label_and_band_without_broad_reference_fallback() -> None:
    status, response = endpoint_response({"q": "Leica 50mm Summicron-M Type IV", "limit": "12"}, records=GENERATION_RECORDS)
    assert status == 200
    assert response["price_scope"] == "exact_generation"
    assert response["display_price_summary_allowed"] is True
    assert response["query_entry_label"] == "Leica 50mm Summicron-M Type IV"
    assert response["market_entry_title"] == "Leica 50mm Summicron-M Type IV"
    assert response["market_entry_policy"]["market_entry_title"] == "Leica 50mm Summicron-M Type IV"
    assert response["display_broader_reference_allowed"] is False
    assert response["market_entry_policy"]["display_broader_reference_allowed"] is False
    assert response["display_price_band_source"] == "exact_generation"
    assert response["display_price_band"].startswith("KRW ")


def test_broad_generation_query_projects_reference_only_labels() -> None:
    status, response = endpoint_response({"q": "Leica M6", "limit": "12"}, records=GENERATION_RECORDS)
    assert status == 200
    assert response["price_summary_allowed"] is False
    assert response["price_scope"] == "generation_disambiguation_required"
    assert sum(1 for item in response["results"] if item.get("used_for_price")) == 0
    labels = [str(item.get("price_usage_label") or "") for item in response["results"]]
    assert "Used for same base model price" not in labels
    assert "Reference only — generation selection needed" in labels


def test_broad_m10_generation_query_keeps_accessories_out_of_price_use() -> None:
    status, response = endpoint_response({"q": "Leica M10", "limit": "12"}, records=GENERATION_RECORDS)
    assert status == 200
    assert response["price_summary_allowed"] is False
    assert response["price_scope"] == "generation_disambiguation_required"
    assert sum(1 for item in response["results"] if item.get("used_for_price")) == 0
    accessory_rows = [item for item in response["results"] if "홀스터" in str(item.get("title", ""))]
    assert accessory_rows
    assert all(item.get("used_for_price") is False for item in accessory_rows)
    assert all(
        str(item.get("price_usage_label") or "") in {
            "Not used for price — generation selection needed",
            "Not used — Accessory, not camera/lens",
        }
        for item in accessory_rows
    )


def test_exact_m10_p_rows_use_exact_generation_labels_when_summary_is_available() -> None:
    status, response = endpoint_response({"q": "Leica M10-P", "limit": "12"}, records=GENERATION_RECORDS)
    assert status == 200
    assert response["price_scope"] == "exact_generation"
    assert response["display_price_summary_allowed"] is True
    exact_rows = [item for item in response["results"] if "M10-P" in str(item.get("title", ""))]
    assert exact_rows
    assert any(str(item.get("price_usage_label") or "") == "Used for exact-generation price" for item in exact_rows)
    assert all(
        str(item.get("price_usage_label") or "") != "Exact generation match visible, but not enough to unlock price yet"
        for item in exact_rows
        if item.get("used_for_price")
    )


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
