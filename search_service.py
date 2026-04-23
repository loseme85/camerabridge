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

from query_parser import parse_query
from query_resolver import DEFAULT_MIN_SCORE, DEFAULT_RESOLVED_PATH, load_resolved_records, rank_listings
from search_response import format_search_response, summarize_result_quality
from search_index import DEFAULT_SEARCH_INDEX_PATH, load_search_index


SEARCH_SERVICE_SCHEMA_VERSION = "search_service.v1"
DEFAULT_LIMIT = 20
MAX_LIMIT = 100
CANDIDATE_MIN_BROAD_RECORDS = 120
CANDIDATE_MAX_RECORDS = 900
ACCESSORY_CANDIDATE_MAX_RECORDS = 260
ACCESSORY_CANDIDATE_BROAD_RECORDS = 120
FILTER_DETAIL_CANDIDATE_MAX_RECORDS = 140
FILTER_DETAIL_CANDIDATE_BROAD_RECORDS = 40
BODY_CANDIDATE_MAX_RECORDS = 260
BODY_CANDIDATE_BROAD_RECORDS = 80
SUPPORTED_SORTS = {
    "relevance",
    "price_asc",
    "price_desc",
    "title",
    "source",
    "condition",
    "newest",
}

QUALITY_RANKS = {
    "none": 0,
    "weak": 1,
    "medium": 2,
    "strong": 3,
}


def _normalize_text(value: Any) -> str:
    return re.sub(r"\s+", " ", str(value or "").strip().lower())


def _normalize_search_text(value: Any) -> str:
    text = str(value or "").lower()
    text = text.replace("㎜", "mm").replace("ｍｍ", "mm")
    text = re.sub(r"[^a-z0-9가-힣]+", " ", text)
    return re.sub(r"\s+", " ", text).strip()


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


def _price_value(final: dict[str, Any]) -> Optional[float]:
    numeric = final.get("parsed_price_numeric")
    if isinstance(numeric, (int, float)):
        return float(numeric)
    return parse_price_number(final.get("price_raw"))


def _source_record_by_index(records: list[dict[str, Any]]) -> dict[int, dict[str, Any]]:
    output = {}
    for record in records:
        index = record.get("record_index")
        if isinstance(index, int):
            output[index] = record
    return output


def _final_output(record: dict[str, Any]) -> dict[str, Any]:
    final = record.get("final_output")
    return final if isinstance(final, dict) else record


def _search_fields(record: dict[str, Any]) -> dict[str, Any]:
    fields = record.get("search_fields")
    return fields if isinstance(fields, dict) else {}


def _search_field_tokens(record: dict[str, Any], field_name: str) -> set[str]:
    value = _search_fields(record).get(field_name)
    if isinstance(value, list):
        return {_normalize_search_text(item) for item in value if item}
    return set()


def _candidate_search_text(record: dict[str, Any]) -> str:
    search_fields = _search_fields(record)
    searchable_text = search_fields.get("searchable_text")
    if isinstance(searchable_text, str) and searchable_text:
        return searchable_text

    final = _final_output(record)
    raw = record.get("raw_item") if isinstance(record.get("raw_item"), dict) else {}
    parts = [
        final.get("model_canonical"),
        final.get("model_raw"),
        final.get("label"),
        final.get("title_raw"),
        final.get("normalized_name"),
        final.get("normalized_title"),
        raw.get("상품명"),
        raw.get("label"),
        " ".join(str(item) for item in _as_list(final.get("variant"))),
    ]
    return _normalize_search_text(" ".join(str(part) for part in parts if part))


def _contains_word(text: str, value: Any) -> bool:
    return _contains_normalized_word(text, _normalize_search_text(value))


def _contains_normalized_word(text: str, needle: str) -> bool:
    if not needle:
        return False
    if " " not in needle and needle in set(text.split()):
        return True
    return bool(re.search(rf"\b{re.escape(needle)}\b", text))


def _aperture_from_intent(intent: dict[str, Any]) -> str:
    aperture = str(intent.get("aperture") or "")
    if aperture:
        return aperture
    for token in intent.get("tokens", []):
        if token.get("type") in {"aperture", "aperture_hint"}:
            return str(token.get("value") or "")
    return ""


def _candidate_anchor_query(intent: dict[str, Any]) -> dict[str, Any]:
    aperture = _aperture_from_intent(intent)
    return {
        "model_family": _normalize_search_text(intent.get("model_family")),
        "focal_length": str(intent.get("focal_length") or ""),
        "focal_length_norm": _normalize_search_text(intent.get("focal_length")),
        "mount": _normalize_search_text(intent.get("mount")),
        "system": _normalize_search_text(intent.get("system")),
        "body_intent": _normalize_search_text(intent.get("body_intent")),
        "variant": [_normalize_search_text(item) for item in intent.get("variant") or [] if item],
        "generation": _normalize_search_text(intent.get("generation")),
        "filter_size": _normalize_search_text(intent.get("filter_size")),
        "optical_formula": _normalize_search_text(intent.get("optical_formula")),
        "aperture": aperture,
        "aperture_norm": _normalize_search_text(aperture),
        "accessory_intent": _normalize_search_text(intent.get("accessory_intent")),
        "accessory_code": _normalize_search_text(intent.get("accessory_code")),
        "filter_details": _filter_detail_values(intent),
    }


def _filter_detail_values(intent: dict[str, Any]) -> list[str]:
    if _normalize_search_text(intent.get("accessory_intent")) != "filter":
        return []

    values: list[str] = []
    for token in intent.get("tokens", []):
        if token.get("type") not in {"filter_kind", "filter_brand", "filter_color"}:
            continue
        for value in [token.get("value"), token.get("raw")]:
            value_norm = _normalize_search_text(value)
            if value_norm and value_norm not in values:
                values.append(value_norm)
    return values


def _record_has_precomputed_search_fields(record: dict[str, Any]) -> bool:
    fields = _search_fields(record)
    return bool(fields.get("searchable_text"))


def _search_field_value(record: dict[str, Any], field_name: str) -> str:
    value = _search_fields(record).get(field_name)
    return value if isinstance(value, str) else ""


def _contains_precomputed_token(record: dict[str, Any], field_name: str, value: str) -> bool:
    if not value:
        return False
    return value in _search_field_tokens(record, field_name)


def _candidate_focal_match(anchor_query: dict[str, Any], record: dict[str, Any], final: dict[str, Any], text: str) -> bool:
    focal = str(anchor_query.get("focal_length") or "")
    if not focal:
        return False
    focal_norm = str(anchor_query.get("focal_length_norm") or _normalize_search_text(focal))
    if _search_field_value(record, "focal_token") == focal_norm:
        return True
    listing_focal = final.get("focal_length")
    if listing_focal:
        if _normalize_search_text(listing_focal) == focal_norm:
            return True
        if focal in re.findall(r"\d{2,3}", str(listing_focal)):
            return True
    return bool(re.search(rf"\b{re.escape(focal)}\s*(mm|/)\b", text))


def _candidate_aperture_match(anchor_query: dict[str, Any], record: dict[str, Any], text: str) -> bool:
    aperture = str(anchor_query.get("aperture") or "")
    if not aperture:
        return False
    if _contains_precomputed_token(record, "aperture_tokens", str(anchor_query.get("aperture_norm") or aperture)):
        return True
    parts = aperture.split(".")
    if len(parts) == 1:
        pattern = rf"\bf\s*{re.escape(parts[0])}\b"
    else:
        pattern = rf"\bf\s*{re.escape(parts[0])}\s+{re.escape(parts[1])}\b"
    return bool(re.search(pattern, text))


def _candidate_accessory_intent_match(anchor_query: dict[str, Any], final: dict[str, Any], text: str) -> bool:
    accessory_intent = str(anchor_query.get("accessory_intent") or "")
    if not accessory_intent:
        return False

    category = _normalize_search_text(final.get("category"))
    accessory_type = _normalize_search_text(final.get("accessory_type"))
    if accessory_intent == "hood":
        has_hood_text = bool(re.search(r"\bhood\b|후드", text))
        if category == "accessory" and (accessory_type == "hood" or has_hood_text):
            return True
        # Keep lens bundles such as "Zeiss 21mm + Hood" eligible, but let the
        # resolver keep them behind standalone accessory records.
        return has_hood_text

    if accessory_intent == "finder":
        has_finder_text = bool(re.search(r"\b(?:finder|viewfinder|brightline|external|visoflex)\b|파인더", text))
        if category == "accessory" and (accessory_type == "finder" or has_finder_text):
            return True
        # Keep lens/body bundles such as "Tri-Elmar + Finder set" eligible,
        # while the resolver keeps them behind standalone finder accessories.
        return has_finder_text

    return category == "accessory" and accessory_type == accessory_intent


def _candidate_accessory_code_match(anchor_query: dict[str, Any], text: str) -> bool:
    code = str(anchor_query.get("accessory_code") or "")
    return bool(code and _contains_normalized_word(text, code))


def _candidate_filter_detail_match(anchor_query: dict[str, Any], record: dict[str, Any], text: str) -> bool:
    details = anchor_query.get("filter_details") or []
    if not details:
        return False

    token_fields = [
        _search_field_tokens(record, "tokens"),
        _search_field_tokens(record, "normalized_title_tokens"),
        _search_field_tokens(record, "model_tokens"),
        _search_field_tokens(record, "variant_tokens"),
    ]
    for detail in details:
        if any(detail in tokens for tokens in token_fields):
            return True
        if _contains_normalized_word(text, detail):
            return True
    return False


def _candidate_body_intent_text_hit(body_intent: str, text: str) -> bool:
    body_norm = _normalize_search_text(body_intent)
    if not body_norm:
        return False
    if body_norm == "barnack":
        return bool(
            re.search(
                r"\bbarnack\b|\bleica\s+i{1,3}[cfg]?\b|\biii[cfg]\b|\biiif\b|\biiig\b|\biiic\b",
                text,
            )
        )
    return _contains_normalized_word(text, body_norm)


def _candidate_body_intent_match(anchor_query: dict[str, Any], final: dict[str, Any], text: str) -> str:
    body_intent = str(anchor_query.get("body_intent") or "")
    if not body_intent:
        return ""

    body_norm = _normalize_search_text(body_intent)
    category = _normalize_search_text(final.get("category"))
    model_values = [
        _normalize_search_text(final.get("model_canonical")),
        _normalize_search_text(final.get("model_raw")),
        _normalize_search_text(final.get("label")),
    ]
    model_hit = body_norm in model_values
    text_hit = _candidate_body_intent_text_hit(body_intent, text)

    if category == "body" and (model_hit or text_hit):
        return "body_exact"
    if text_hit:
        return "body_text_hint"
    return ""


def _candidate_system(record: dict[str, Any], final: dict[str, Any]) -> str:
    raw = record.get("raw_item") if isinstance(record.get("raw_item"), dict) else {}
    return str(final.get("system") or raw.get("system") or "")


def _candidate_anchor_matches(
    intent: dict[str, Any],
    record: dict[str, Any],
    anchor_query: Optional[dict[str, Any]] = None,
) -> set[str]:
    anchor_query = anchor_query or _candidate_anchor_query(intent)
    final = _final_output(record)
    text = _candidate_search_text(record)
    matches: set[str] = set()

    model_family = anchor_query.get("model_family")
    model_text = _search_field_value(record, "model_text")
    if model_family and (
        _contains_normalized_word(model_text, model_family)
        or _contains_normalized_word(text, model_family)
    ):
        matches.add("model_family")

    if _candidate_focal_match(anchor_query, record, final, text):
        matches.add("focal_length")

    body_match = _candidate_body_intent_match(anchor_query, final, text)
    if body_match == "body_exact":
        matches.add("body_intent")
    elif body_match == "body_text_hint":
        matches.add("body_text_hint")

    query_mount = anchor_query.get("mount")
    if query_mount and query_mount == (_search_field_value(record, "mount_token") or _normalize_search_text(final.get("mount"))):
        matches.add("mount")

    query_system = anchor_query.get("system")
    if query_system:
        system_values = {
            _search_field_value(record, "mount_token") or _normalize_search_text(final.get("mount")),
            _search_field_value(record, "system_token") or _normalize_search_text(_candidate_system(record, final)),
        }
        if query_system in system_values:
            matches.add("system")

    listing_variant_tokens = _search_field_tokens(record, "variant_tokens")
    for variant_norm in anchor_query.get("variant") or []:
        listing_variants = listing_variant_tokens or {_normalize_search_text(item) for item in _as_list(final.get("variant"))}
        if variant_norm in listing_variants or _contains_normalized_word(text, variant_norm):
            matches.add("variant")
            break

    if anchor_query.get("generation") and _contains_normalized_word(text, anchor_query["generation"]):
        matches.add("generation")

    if anchor_query.get("filter_size") and _contains_normalized_word(text, anchor_query["filter_size"]):
        matches.add("filter_size")

    if _candidate_filter_detail_match(anchor_query, record, text):
        matches.add("filter_detail")

    if anchor_query.get("optical_formula"):
        formula_norm = anchor_query["optical_formula"]
        if formula_norm in text or "8 element" in text or "8매" in text:
            matches.add("optical_formula")

    if _candidate_aperture_match(anchor_query, record, text):
        matches.add("aperture")

    if _candidate_accessory_intent_match(anchor_query, final, text):
        matches.add("accessory_intent")

    if _candidate_accessory_code_match(anchor_query, text):
        matches.add("accessory_code")

    return matches


def _candidate_anchor_fields(intent: dict[str, Any]) -> set[str]:
    fields = {
        field
        for field in [
            "model_family",
            "body_intent",
            "focal_length",
            "mount",
            "system",
            "generation",
            "filter_size",
            "optical_formula",
            "accessory_intent",
            "accessory_code",
        ]
        if intent.get(field)
    }
    if intent.get("variant"):
        fields.add("variant")
    if intent.get("aperture") or any(token.get("type") in {"aperture", "aperture_hint"} for token in intent.get("tokens", [])):
        fields.add("aperture")
    if _filter_detail_values(intent):
        fields.add("filter_detail")
    return fields


def _accessory_anchor_active(intent: dict[str, Any]) -> bool:
    return bool(intent.get("accessory_intent") or intent.get("accessory_code"))


def _body_anchor_active(intent: dict[str, Any]) -> bool:
    return bool(intent.get("body_intent"))


def _filter_detail_anchor_active(intent: dict[str, Any]) -> bool:
    lens_like_anchor = bool(intent.get("model_family") or intent.get("focal_length") or _aperture_from_intent(intent))
    return (
        _normalize_search_text(intent.get("accessory_intent")) == "filter"
        and bool(intent.get("filter_size") or _filter_detail_values(intent))
        and not lens_like_anchor
    )


def narrow_candidate_records(
    intent: dict[str, Any],
    records: list[dict[str, Any]],
    max_records: int = CANDIDATE_MAX_RECORDS,
    min_broad_records: int = CANDIDATE_MIN_BROAD_RECORDS,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    """
    Reduce expensive resolver scoring to likely candidates.

    The resolver still owns scoring and match quality. This helper only builds a
    cheap candidate pool from already-classified compact fields.
    """
    input_count = len(records)
    anchor_fields = _candidate_anchor_fields(intent)
    accessory_anchor_active = _accessory_anchor_active(intent)
    stats = {
        "applied": False,
        "input_record_count": input_count,
        "scored_record_count": input_count,
        "anchor_fields": sorted(anchor_fields),
        "strong_candidate_count": 0,
        "broad_candidate_count": 0,
        "precomputed_field_record_count": 0,
        "accessory_intent_applied": False,
        "accessory_code_applied": False,
        "filter_intent_applied": False,
        "filter_detail_applied": False,
        "body_intent_applied": False,
        "body_family_applied": False,
    }
    if input_count <= max_records or not anchor_fields:
        return records, stats

    anchor_query = _candidate_anchor_query(intent)
    strong: list[tuple[int, int, dict[str, Any]]] = []
    broad: list[tuple[int, int, dict[str, Any]]] = []
    precomputed_count = 0
    for position, record in enumerate(records):
        if _record_has_precomputed_search_fields(record):
            precomputed_count += 1
        matches = _candidate_anchor_matches(intent, record, anchor_query=anchor_query)
        match_count = len(matches)
        if match_count >= 2:
            strong.append((-match_count, position, record))
        elif match_count == 1:
            broad.append((-match_count, position, record))

    if not strong and not (accessory_anchor_active and broad):
        stats["precomputed_field_record_count"] = precomputed_count
        return records, stats

    strong.sort()
    broad.sort()
    filter_detail_active = _filter_detail_anchor_active(intent)
    body_anchor_active = _body_anchor_active(intent)
    if filter_detail_active:
        candidate_max = FILTER_DETAIL_CANDIDATE_MAX_RECORDS
        candidate_broad_records = FILTER_DETAIL_CANDIDATE_BROAD_RECORDS
    elif accessory_anchor_active:
        candidate_max = ACCESSORY_CANDIDATE_MAX_RECORDS
        candidate_broad_records = ACCESSORY_CANDIDATE_BROAD_RECORDS
    elif body_anchor_active:
        candidate_max = BODY_CANDIDATE_MAX_RECORDS
        candidate_broad_records = BODY_CANDIDATE_BROAD_RECORDS
    else:
        candidate_max = max_records
        candidate_broad_records = min_broad_records

    if accessory_anchor_active and not strong and broad:
        selected = [item[2] for item in broad[:candidate_max]]
    else:
        strong_limit = candidate_max
        if body_anchor_active and broad:
            strong_limit = max(candidate_max - min(candidate_broad_records, len(broad)), 0)
        selected = [item[2] for item in strong[:strong_limit]]
        remaining_slots = candidate_max - len(selected)
        broad_limit = min(candidate_broad_records, remaining_slots) if remaining_slots > 0 else 0
        selected.extend(item[2] for item in broad[:broad_limit])

    if not selected or len(selected) >= input_count:
        return records, stats

    stats.update(
        {
            "applied": True,
            "scored_record_count": len(selected),
            "strong_candidate_count": len(strong),
            "broad_candidate_count": len(broad),
            "precomputed_field_record_count": precomputed_count,
            "accessory_intent_applied": bool(intent.get("accessory_intent")),
            "accessory_code_applied": bool(intent.get("accessory_code")),
            "filter_intent_applied": _normalize_search_text(intent.get("accessory_intent")) == "filter",
            "filter_detail_applied": filter_detail_active,
            "body_intent_applied": body_anchor_active,
            "body_family_applied": body_anchor_active and bool(intent.get("mount") or intent.get("system")),
        }
    )
    return selected, stats


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

    price = _price_value(final)
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


def apply_quality_filter(
    ranked_results: list[dict[str, Any]],
    strong_only: bool = False,
) -> list[dict[str, Any]]:
    if not strong_only:
        return ranked_results
    return [
        result
        for result in ranked_results
        if result.get("match_quality") == "strong"
    ]


def _quality_rank(result: dict[str, Any]) -> int:
    value = result.get("match_quality_rank")
    if isinstance(value, int):
        return value
    return QUALITY_RANKS.get(str(result.get("match_quality") or "none"), 0)


def _sort_key_price(result: dict[str, Any]) -> tuple[int, float]:
    price = _price_value(result.get("final_output") or {})
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
        return sorted(
            ranked_results,
            key=lambda result: (
                -_quality_rank(result),
                _sort_key_price(result)[0],
                _sort_key_price(result)[1],
                -float(result.get("score") or 0),
            ),
        ), sort_name, warnings
    if sort_name == "price_desc":
        return sorted(
            ranked_results,
            key=lambda result: (
                -_quality_rank(result),
                _sort_key_price(result)[0],
                -_sort_key_price(result)[1],
                -float(result.get("score") or 0),
            ),
        ), sort_name, warnings
    if sort_name == "title":
        return sorted(ranked_results, key=lambda result: (-_quality_rank(result), _sort_key_text(result, "title"))), sort_name, warnings
    if sort_name == "source":
        return sorted(ranked_results, key=lambda result: (-_quality_rank(result), _sort_key_text(result, "source"))), sort_name, warnings
    if sort_name == "condition":
        return sorted(ranked_results, key=lambda result: (-_quality_rank(result), _sort_key_text(result, "condition_raw"))), sort_name, warnings
    if sort_name == "newest":
        return sorted(ranked_results, key=lambda result: (_quality_rank(result), _sort_key_newest(result)), reverse=True), sort_name, warnings

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
    min_score: float = DEFAULT_MIN_SCORE,
    strong_only: bool = False,
    use_candidate_narrowing: bool = True,
) -> dict[str, Any]:
    intent = parse_query(query)
    candidate_records, candidate_stats = (
        narrow_candidate_records(intent, records)
        if use_candidate_narrowing
        else (
            records,
            {
                "applied": False,
                "input_record_count": len(records),
                "scored_record_count": len(records),
                "anchor_fields": sorted(_candidate_anchor_fields(intent)),
                "strong_candidate_count": 0,
                "broad_candidate_count": 0,
                "precomputed_field_record_count": 0,
            },
        )
    )
    ranked_payload = rank_listings(
        intent,
        candidate_records,
        limit=len(candidate_records),
        min_score=min_score,
    )
    ranked_results = ranked_payload["results"]
    total_before_filters = len(ranked_results)
    quality_filtered_results = apply_quality_filter(ranked_results, strong_only=strong_only)
    filtered_results = apply_filters(quality_filtered_results, filters=filters, records=candidate_records)
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
        records=candidate_records,
        include_debug=include_debug,
    )
    response["schema_version"] = SEARCH_SERVICE_SCHEMA_VERSION
    response["total_before_filters"] = total_before_filters
    response["total_ranked"] = len(sorted_results)
    response["result_count"] = len(response["results"])
    response["pagination"] = pagination
    response["applied_filters"] = filters or {}
    response["applied_sort"] = applied_sort
    response["applied_quality_filter"] = {"min_score": min_score, "strong_only": strong_only}
    response["candidate_narrowing"] = candidate_stats
    response["result_quality_summary"] = summarize_result_quality(
        sorted_results,
        strong_only=strong_only,
    )
    response["warnings"] = list(response.get("warnings") or []) + sort_warnings + pagination_warnings
    return response


def load_and_search(
    query: str,
    path: str | Path = DEFAULT_SEARCH_INDEX_PATH,
    limit: int = DEFAULT_LIMIT,
    offset: int = 0,
    filters: Optional[dict[str, Any]] = None,
    sort: str = "relevance",
    include_debug: bool = False,
    min_score: float = DEFAULT_MIN_SCORE,
    strong_only: bool = False,
    use_cache: bool = True,
    use_candidate_narrowing: bool = True,
) -> dict[str, Any]:
    records = load_search_records(path=path, include_debug=include_debug, use_cache=use_cache)
    return search_records(
        query=query,
        records=records,
        limit=limit,
        offset=offset,
        filters=filters,
        sort=sort,
        include_debug=include_debug,
        min_score=min_score,
        strong_only=strong_only,
        use_candidate_narrowing=use_candidate_narrowing,
    )


def load_search_records(
    path: str | Path = DEFAULT_SEARCH_INDEX_PATH,
    include_debug: bool = False,
    use_cache: bool = True,
) -> list[dict[str, Any]]:
    """
    Load compact records for normal search and full resolved records for debug.

    The compact index is the production default. If it has not been generated
    yet, local development falls back to the full resolved file without changing
    search semantics.
    """
    data_path = Path(path)
    if include_debug and data_path == DEFAULT_SEARCH_INDEX_PATH and DEFAULT_RESOLVED_PATH.exists():
        return load_resolved_records(DEFAULT_RESOLVED_PATH)
    try:
        return load_search_index(data_path, use_cache=use_cache)
    except FileNotFoundError:
        if data_path == DEFAULT_SEARCH_INDEX_PATH:
            return load_resolved_records(DEFAULT_RESOLVED_PATH)
        raise


def run_service_demo(path: str | Path = DEFAULT_SEARCH_INDEX_PATH) -> dict[str, Any]:
    records = load_search_records(path)
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
