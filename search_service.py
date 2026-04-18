"""
search_service.py
=================
Endpoint-friendly search service layer.

Responsibilities:
  - Apply pagination, filters, and sort to query_resolver results.
  - Return API/UI-ready response shape through search_response formatting.

Non-responsibilities:
  - Do not classify listings.
  - Do not parse aliases directly.
  - Do not apply or infer trusted metadata overrides.
  - Do not import classifier_v2.py.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any, Optional

from query_resolver import DEFAULT_RESOLVED_PATH, load_resolved_records, rank_listings
from search_response import format_search_response


SEARCH_SERVICE_SCHEMA_VERSION = "search_service.v1"
DEFAULT_LIMIT = 20
MAX_LIMIT = 100
SUPPORTED_SORTS = {
    "relevance",
    "price_asc",
    "price_desc",
    "title",
    "source",
    "condition",
    "newest",
}


def _normalize_text(value: Any) -> str:
    return re.sub(r"\s+", " ", str(value or "").strip().lower())


def _as_list(value: Any) -> list[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


def parse_price_number(value: Any) -> Optional[float]:
    """Parse a raw listing price into a same-currency numeric value."""
    text = str(value or "")
    if not text or any(keyword in text for keyword in ["문의", "ASK", "Ask", "상담"]):
        return None
    digits = re.findall(r"\d+(?:\.\d+)?", text.replace(",", ""))
    if not digits:
        return None
    try:
        return float("".join(digits[:1]))
    except ValueError:
        return None


def _filter_values_match(actual: Any, expected: Any) -> bool:
    expected_values = {_normalize_text(item) for item in _as_list(expected)}
    if not expected_values:
        return True
    actual_values = {_normalize_text(item) for item in _as_list(actual)}
    return bool(actual_values & expected_values)


def _sold_quality_matches(actual: Any, expected: Any) -> bool:
    expected_values = {_normalize_text(item) for item in _as_list(expected)}
    actual_norm = _normalize_text(actual or "unknown")
    if not expected_values:
        return True

    for expected_norm in expected_values:
        if expected_norm == "sold" and actual_norm.startswith("sold"):
            return True
        if expected_norm == "unknown" and actual_norm in {"", "unknown", "none"}:
            return True
        if actual_norm == expected_norm:
            return True
    return False


def _listing_system(result: dict[str, Any], source_record: Optional[dict[str, Any]]) -> Any:
    final = result.get("final_output") or {}
    if final.get("system"):
        return final.get("system")
    if isinstance(source_record, dict):
        raw = source_record.get("raw_item") or {}
        return raw.get("system")
    return None


def _source_record_by_index(records: list[dict[str, Any]]) -> dict[int, dict[str, Any]]:
    output = {}
    for record in records:
        index = record.get("record_index")
        if isinstance(index, int):
            output[index] = record
    return output


def _matches_filters(
    result: dict[str, Any],
    filters: dict[str, Any],
    source_record: Optional[dict[str, Any]] = None,
) -> bool:
    final = result.get("final_output") or {}

    if "sold_quality" in filters and not _sold_quality_matches(final.get("sold_quality"), filters["sold_quality"]):
        return False
    if "category" in filters and not _filter_values_match(final.get("category"), filters["category"]):
        return False
    if "brand" in filters and not _filter_values_match(final.get("brand"), filters["brand"]):
        return False
    if "mount" in filters and not _filter_values_match(final.get("mount"), filters["mount"]):
        return False
    if "system" in filters and not _filter_values_match(_listing_system(result, source_record), filters["system"]):
        return False
    if "used_override" in filters and bool(result.get("used_override")) is not bool(filters["used_override"]):
        return False
    if "source" in filters and not _filter_values_match(result.get("source") or final.get("source"), filters["source"]):
        return False

    price = parse_price_number(final.get("price_raw"))
    if filters.get("price_min") is not None:
        if price is None or price < float(filters["price_min"]):
            return False
    if filters.get("price_max") is not None:
        if price is None or price > float(filters["price_max"]):
            return False

    return True


def apply_filters(
    ranked_results: list[dict[str, Any]],
    filters: Optional[dict[str, Any]] = None,
    records: Optional[list[dict[str, Any]]] = None,
) -> list[dict[str, Any]]:
    filters = filters or {}
    if not filters:
        return ranked_results

    source_records = _source_record_by_index(records or [])
    return [
        result
        for result in ranked_results
        if _matches_filters(
            result,
            filters,
            source_record=source_records.get(result.get("record_index")),
        )
    ]


def _sort_key_price(result: dict[str, Any]) -> tuple[int, float]:
    price = parse_price_number((result.get("final_output") or {}).get("price_raw"))
    if price is None:
        return (1, 0.0)
    return (0, price)


def _sort_key_text(result: dict[str, Any], field_name: str) -> str:
    final = result.get("final_output") or {}
    if field_name == "title":
        return _normalize_text(result.get("title_raw") or final.get("title_raw"))
    return _normalize_text(result.get(field_name) or final.get(field_name))


def _sort_key_newest(result: dict[str, Any]) -> str:
    final = result.get("final_output") or {}
    return str(final.get("crawl_time") or final.get("first_seen") or "")


def apply_sort(
    ranked_results: list[dict[str, Any]],
    sort: str = "relevance",
) -> tuple[list[dict[str, Any]], str, list[str]]:
    warnings: list[str] = []
    sort_name = sort or "relevance"
    if sort_name not in SUPPORTED_SORTS:
        warnings.append(f"unsupported_sort:{sort_name}")
        sort_name = "relevance"

    if sort_name == "relevance":
        return ranked_results, sort_name, warnings
    if sort_name == "price_asc":
        return sorted(ranked_results, key=_sort_key_price), sort_name, warnings
    if sort_name == "price_desc":
        return sorted(
            ranked_results,
            key=lambda result: (
                _sort_key_price(result)[0],
                -_sort_key_price(result)[1],
            ),
        ), sort_name, warnings
    if sort_name == "title":
        return sorted(ranked_results, key=lambda result: _sort_key_text(result, "title")), sort_name, warnings
    if sort_name == "source":
        return sorted(ranked_results, key=lambda result: _sort_key_text(result, "source")), sort_name, warnings
    if sort_name == "condition":
        return sorted(ranked_results, key=lambda result: _sort_key_text(result, "condition_raw")), sort_name, warnings
    if sort_name == "newest":
        return sorted(ranked_results, key=_sort_key_newest, reverse=True), sort_name, warnings

    return ranked_results, "relevance", warnings


def _normalize_pagination(limit: int = DEFAULT_LIMIT, offset: int = 0) -> tuple[int, int, list[str]]:
    warnings = []
    try:
        normalized_limit = int(limit)
    except (TypeError, ValueError):
        normalized_limit = DEFAULT_LIMIT
        warnings.append("invalid_limit_defaulted")

    try:
        normalized_offset = int(offset)
    except (TypeError, ValueError):
        normalized_offset = 0
        warnings.append("invalid_offset_defaulted")

    if normalized_limit < 1:
        normalized_limit = DEFAULT_LIMIT
        warnings.append("invalid_limit_defaulted")
    if normalized_limit > MAX_LIMIT:
        normalized_limit = MAX_LIMIT
        warnings.append("limit_capped")
    if normalized_offset < 0:
        normalized_offset = 0
        warnings.append("invalid_offset_defaulted")

    return normalized_limit, normalized_offset, warnings


def paginate_results(
    results: list[dict[str, Any]],
    limit: int = DEFAULT_LIMIT,
    offset: int = 0,
) -> tuple[list[dict[str, Any]], dict[str, Any], list[str]]:
    normalized_limit, normalized_offset, warnings = _normalize_pagination(limit, offset)
    total = len(results)
    if normalized_offset >= total and total > 0:
        warnings.append("offset_out_of_range")

    page = results[normalized_offset:normalized_offset + normalized_limit]
    next_offset = normalized_offset + normalized_limit
    has_more = next_offset < total
    pagination = {
        "limit": normalized_limit,
        "offset": normalized_offset,
        "result_count": len(page),
        "total_ranked": total,
        "has_more": has_more,
        "next_offset": next_offset if has_more else None,
    }
    return page, pagination, warnings


def search_records(
    query: str,
    records: list[dict[str, Any]],
    limit: int = DEFAULT_LIMIT,
    offset: int = 0,
    filters: Optional[dict[str, Any]] = None,
    sort: str = "relevance",
    include_debug: bool = False,
    min_score: float = 1.0,
) -> dict[str, Any]:
    ranked_payload = rank_listings(
        query,
        records,
        limit=len(records),
        min_score=min_score,
    )
    ranked_results = ranked_payload["results"]
    total_before_filters = len(ranked_results)
    filtered_results = apply_filters(ranked_results, filters=filters, records=records)
    sorted_results, applied_sort, sort_warnings = apply_sort(filtered_results, sort=sort)
    paginated_results, pagination, pagination_warnings = paginate_results(
        sorted_results,
        limit=limit,
        offset=offset,
    )

    response = format_search_response(
        {
            "intent": ranked_payload["intent"],
            "results": paginated_results,
            "total_ranked": len(sorted_results),
        },
        records=records,
        include_debug=include_debug,
    )
    response["schema_version"] = SEARCH_SERVICE_SCHEMA_VERSION
    response["total_before_filters"] = total_before_filters
    response["total_ranked"] = len(sorted_results)
    response["result_count"] = len(response["results"])
    response["pagination"] = pagination
    response["applied_filters"] = filters or {}
    response["applied_sort"] = applied_sort
    response["warnings"] = list(response.get("warnings") or []) + sort_warnings + pagination_warnings
    return response


def load_and_search(
    query: str,
    path: str | Path = DEFAULT_RESOLVED_PATH,
    limit: int = DEFAULT_LIMIT,
    offset: int = 0,
    filters: Optional[dict[str, Any]] = None,
    sort: str = "relevance",
    include_debug: bool = False,
    min_score: float = 1.0,
) -> dict[str, Any]:
    records = load_resolved_records(path)
    return search_records(
        query=query,
        records=records,
        limit=limit,
        offset=offset,
        filters=filters,
        sort=sort,
        include_debug=include_debug,
        min_score=min_score,
    )


def run_service_demo(path: str | Path = DEFAULT_RESOLVED_PATH) -> dict[str, Any]:
    records = load_resolved_records(path)
    return {
        "basic_mp3_silver": search_records("mp3 silver", records, limit=2),
        "filter_q3_28_body_asking": search_records(
            "q3 28",
            records,
            limit=2,
            filters={"category": "Body", "sold_quality": "asking"},
        ),
        "sort_ltm_summaron_35_price_asc": search_records(
            "ltm summaron 35",
            records,
            limit=2,
            filters={"brand": "Leica", "category": "Lens", "mount": "L"},
            sort="price_asc",
            min_score=80,
        ),
        "pagination_35lux_aa": search_records(
            "35lux aa",
            records,
            limit=2,
            offset=2,
        ),
    }


if __name__ == "__main__":
    print(json.dumps(run_service_demo(), ensure_ascii=False, indent=2))
