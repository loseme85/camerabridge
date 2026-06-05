"""
api/search.py
=============
Thin HTTP endpoint for the search service.

Responsibilities:
  - Parse and validate endpoint query parameters.
  - Call search_service with the requested pagination/filter/sort options.
  - Serialize the search_service.v1 response for Vercel serverless use.

Non-responsibilities:
  - Do not classify listings.
  - Do not parse search aliases directly.
  - Do not rank listings directly.
  - Do not apply or infer trusted metadata overrides.
"""

from __future__ import annotations

import json
import re
import sys
from http.server import BaseHTTPRequestHandler
from json import JSONDecodeError
from pathlib import Path
from typing import Any, Callable, Mapping, Optional
from urllib.parse import parse_qs, urlparse


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


ERROR_SCHEMA_VERSION = "search_service.error.v1"
ALLOWED_CATEGORIES = {"Lens", "Body", "Accessory"}
DEFAULT_MAX_LIMIT = 100
DEFAULT_SUPPORTED_SORTS = {
    "relevance",
    "price_asc",
    "price_desc",
    "title",
    "source",
    "condition",
    "newest",
}
ALLOWED_SOLD_QUALITIES = {
    "asking",
    "sold",
    "sold_confirmed",
    "sold_likely",
    "unknown",
    "ended_unsold",
}
_RUNTIME_CACHE: dict[str, Any] | None = None


class SearchEndpointError(ValueError):
    def __init__(
        self,
        code: str,
        message: str,
        status: int = 400,
        details: Optional[dict[str, Any]] = None,
    ) -> None:
        super().__init__(message)
        self.code = code
        self.message = message
        self.status = status
        self.details = details or {}


def error_payload(
    code: str,
    message: str,
    status: int,
    details: Optional[dict[str, Any]] = None,
) -> dict[str, Any]:
    payload = {
        "schema_version": ERROR_SCHEMA_VERSION,
        "status": status,
        "error": {
            "code": code,
            "message": message,
        },
    }
    if details:
        payload["error"]["details"] = details
    return payload


def _load_runtime_dependencies() -> dict[str, Any]:
    global _RUNTIME_CACHE
    if _RUNTIME_CACHE is not None:
        return _RUNTIME_CACHE

    from search_index import DEFAULT_SEARCH_INDEX_PATH  # noqa: WPS433
    from search_service import MAX_LIMIT, SUPPORTED_SORTS, load_and_search, search_records  # noqa: WPS433
    from search_ui_hints import build_query_ui_hints  # noqa: WPS433

    _RUNTIME_CACHE = {
        "default_search_index_path": DEFAULT_SEARCH_INDEX_PATH,
        "max_limit": MAX_LIMIT,
        "supported_sorts": SUPPORTED_SORTS,
        "load_and_search": load_and_search,
        "search_records": search_records,
        "build_query_ui_hints": build_query_ui_hints,
    }
    return _RUNTIME_CACHE


def _candidate_index_paths(default_path: str | Path) -> list[Path]:
    default = Path(default_path)
    candidates = [
        default,
        PROJECT_ROOT / "data/derived/results_search_index_v1.json",
        Path.cwd() / "data/derived/results_search_index_v1.json",
        Path(__file__).resolve().parent.parent / "data/derived/results_search_index_v1.json",
    ]
    output: list[Path] = []
    seen: set[str] = set()
    for candidate in candidates:
        resolved = str(candidate.resolve())
        if resolved in seen:
            continue
        seen.add(resolved)
        output.append(candidate)
    return output


def _resolve_search_index_path(path: str | Path | None) -> Path:
    runtime = _load_runtime_dependencies()
    default_path = runtime["default_search_index_path"]
    requested = Path(path) if path is not None else Path(default_path)
    if requested.exists():
        return requested

    for candidate in _candidate_index_paths(default_path):
        if candidate.exists():
            return candidate

    raise FileNotFoundError(
        "No search index file found in runtime candidate paths: "
        + ", ".join(str(candidate) for candidate in _candidate_index_paths(default_path))
    )


def _first(params: Mapping[str, Any], key: str) -> Optional[Any]:
    value = params.get(key)
    if isinstance(value, list):
        return value[0] if value else None
    return value


def _normalize_params(params: Mapping[str, Any]) -> dict[str, Any]:
    return {key: _first(params, key) for key in params}


def _normalize_text(value: Any) -> str:
    return " ".join(str(value or "").strip().lower().split())


def _family_root(value: Any) -> str:
    text = _normalize_text(value)
    if "apo-summicron" in text or ("apo" in text and "summicron" in text):
        return "APO-Summicron"
    if "summicron" in text:
        return "Summicron"
    if "summilux" in text:
        return "Summilux"
    if "noctilux" in text:
        return "Noctilux"
    if "elmarit" in text:
        return "Elmarit"
    if "summaron" in text:
        return "Summaron"
    if "elmar" in text:
        return "Elmar"
    if "summarit" in text:
        return "Summarit"
    if "q3" in text:
        return "Q3"
    if "mp" in text:
        return "MP"
    return ""


def _unknown_tokens(intent: Mapping[str, Any]) -> list[str]:
    return [str(token.get("raw") or "") for token in intent.get("tokens", []) if token.get("type") == "unknown"]


def _dangerous_unknown_family_tokens(intent: Mapping[str, Any]) -> list[str]:
    pattern = re.compile(
        r"(?:^|[-])(?:apo|summicron|summilux|noctilux|elmarit|summaron|elmar|summarit)(?:-[a-z0-9]+)*$"
    )
    return [token for token in _unknown_tokens(intent) if pattern.search(token)]


def _explicit_query_mount(query: str, intent: Mapping[str, Any]) -> str | None:
    if intent.get("mount"):
        return str(intent.get("mount"))
    lowered = _normalize_text(query)
    token_set = set(re.findall(r"[a-z0-9./-]+", lowered))
    if any(token in {"ltm", "l39", "m39", "screw"} for token in token_set):
        return "L"
    if any(token == "sl" or token.endswith("-sl") for token in token_set):
        return "SL"
    if any(token == "r" or token.endswith("-r") for token in token_set):
        return "R"
    if any(token == "m" or token.endswith("-m") for token in token_set):
        return "M"
    return None


def _explicit_query_family(query: str, intent: Mapping[str, Any]) -> str:
    lowered = _normalize_text(query)
    query_mount = _explicit_query_mount(query, intent)

    if "apo-summicron" in lowered or re.search(r"\bapo\s+\d{2,3}\s+summicron\b|\bapo\s+summicron\b", lowered):
        return "APO-Summicron"

    parsed_family = str(intent.get("model_family") or "")
    if parsed_family:
        if parsed_family == "Summicron" and query_mount == "M":
            return "Summicron-M"
        if parsed_family == "Summicron" and query_mount == "R":
            return "Summicron-R"
        if parsed_family == "Summicron" and query_mount == "SL":
            return "Summicron-SL"
        if parsed_family == "Summilux" and query_mount == "M":
            return "Summilux-M"
        if parsed_family == "Elmarit" and query_mount == "M":
            return "Elmarit-M"
        if parsed_family == "Elmarit" and query_mount == "R":
            return "Elmarit-R"
        return parsed_family

    if "summicron" in lowered:
        if query_mount == "M":
            return "Summicron-M"
        if query_mount == "R":
            return "Summicron-R"
        if query_mount == "SL":
            return "Summicron-SL"
        return "Summicron"
    if "summilux" in lowered or re.search(r"\blux\b", lowered):
        return "Summilux-M" if query_mount == "M" else "Summilux"
    if "noctilux" in lowered or re.search(r"\bnocti\b|\bnoct\b", lowered):
        return "Noctilux-M" if query_mount == "M" else "Noctilux"
    if "elmarit" in lowered:
        if query_mount == "M":
            return "Elmarit-M"
        if query_mount == "R":
            return "Elmarit-R"
        return "Elmarit"
    if "summaron" in lowered:
        return "Summaron"
    return ""


def _parsed_category(intent: Mapping[str, Any]) -> str | None:
    if intent.get("accessory_intent"):
        return "Accessory"
    if intent.get("body_intent"):
        return "Body"
    if intent.get("model_family") or intent.get("focal_length") or intent.get("variant") or intent.get("mount"):
        return "Lens"
    return None


def _is_weak_only_fallback(quality: Mapping[str, Any]) -> bool:
    return (
        int(quality.get("strong_result_count") or 0) == 0
        and int(quality.get("medium_result_count") or 0) == 0
        and int(quality.get("weak_result_count") or 0) > 0
    ) or quality.get("fallback_reason") == "no_strong_results_weak_matches_included"


def _result_field(result: Mapping[str, Any], name: str) -> Any:
    return (result.get("final_output") or {}).get(name)


def _result_family_conflict(expected_family: str, top_result: Mapping[str, Any]) -> bool:
    if not expected_family:
        return False
    top_family = str(_result_field(top_result, "model_canonical") or _result_field(top_result, "model_raw") or "")
    top_root = _family_root(top_family)
    expected_root = _family_root(expected_family)
    if expected_root == "APO-Summicron":
        return top_root != "APO-Summicron"
    if expected_root == "Summicron":
        return top_root != "Summicron"
    if expected_root and top_root and expected_root != top_root:
        return True
    return False


def _result_mount_conflict(expected_mount: str | None, top_result: Mapping[str, Any]) -> bool:
    if not expected_mount:
        return False
    return str(_result_field(top_result, "mount") or "") != expected_mount


def _result_category_conflict(expected_category: str | None, top_result: Mapping[str, Any]) -> bool:
    if not expected_category:
        return False
    return str(_result_field(top_result, "category") or "") != expected_category


def _result_variant_conflict(intent: Mapping[str, Any], top_result: Mapping[str, Any]) -> bool:
    expected_variants = [str(item) for item in intent.get("variant") or [] if item]
    if not expected_variants:
        return False
    matched = set(top_result.get("matched_fields") or [])
    if "variant" in matched:
        return False
    top_variants = {str(item).lower() for item in (_result_field(top_result, "variant") or []) if item}
    return not all(str(item).lower() in top_variants for item in expected_variants)


def _exact_model_like_match(intent: Mapping[str, Any], top_result: Mapping[str, Any], expected_mount: str | None) -> bool:
    matched = set(top_result.get("matched_fields") or [])
    if intent.get("body_intent"):
        if "body_intent" not in matched:
            return False
        if intent.get("focal_length") and "focal_length" not in matched:
            return False
        if expected_mount and "mount" not in matched and "system" not in matched:
            return False
        return True
    if "model_family" not in matched or "focal_length" not in matched:
        return False
    if expected_mount and "mount" not in matched:
        return False
    if intent.get("variant") and "variant" not in matched:
        return False
    return True


def _result_matches_query_summary_scope(
    result: Mapping[str, Any],
    intent: Mapping[str, Any],
    query: str,
    expected_family: str,
    expected_mount: str | None,
) -> bool:
    final = result.get("final_output") or {}
    if intent.get("body_intent"):
        expected_body = _normalize_text(intent.get("body_intent"))
        result_body = _normalize_text(final.get("model_canonical") or final.get("model_raw") or final.get("label"))
        if expected_body and expected_body not in result_body:
            return False
    else:
        if str(final.get("category") or "") != "Lens":
            return False
        if expected_family and _result_family_conflict(expected_family, result):
            return False
        if expected_mount and str(final.get("mount") or "") != expected_mount:
            return False
        expected_focal = str(intent.get("focal_length") or "")
        if expected_focal and str(final.get("focal_length") or "") != expected_focal:
            return False
        if _result_variant_conflict(intent, result):
            return False
    return True


def _build_market_counts(results: list[Mapping[str, Any]]) -> dict[str, int]:
    counts = {"asking": 0, "sold_confirmed": 0, "sold_likely": 0, "expired_removed": 0, "archive": 0}
    for result in results:
        sold_quality = _normalize_text(_result_field(result, "sold_quality"))
        if sold_quality == "asking":
            counts["asking"] += 1
        elif sold_quality == "sold_confirmed":
            counts["sold_confirmed"] += 1
        elif sold_quality == "sold_likely":
            counts["sold_likely"] += 1
        elif sold_quality in {"expired", "removed", "ended_unsold"}:
            counts["expired_removed"] += 1
        if sold_quality and sold_quality != "asking":
            counts["archive"] += 1
    return counts


def _parse_price_number(value: Any) -> float | None:
    text = str(value or "")
    digits = re.findall(r"\d+(?:\.\d+)?", text.replace(",", ""))
    if not digits:
        return None
    try:
        return float(digits[0])
    except ValueError:
        return None


def _format_price_band(results: list[Mapping[str, Any]]) -> str:
    priced = []
    for result in results:
        numeric = _parse_price_number(result.get("price"))
        if numeric is None:
            continue
        priced.append((numeric, str(result.get("currency") or "")))
    if not priced:
        return "Not enough exact confidence for price summary"
    currencies = sorted({currency or "Unknown" for _, currency in priced})
    if len(currencies) != 1:
        return "Mixed currencies"
    values = [value for value, _ in priced]
    currency = currencies[0]
    formatter = lambda num: f"{num:,.0f}"
    return f"{currency} {formatter(min(values))} - {formatter(max(values))}"


def build_market_entry_policy(query: str, response: Mapping[str, Any], ui_hints: Mapping[str, Any]) -> dict[str, Any]:
    intent = response.get("intent") or {}
    results = list(response.get("results") or [])
    quality = response.get("result_quality_summary") or {}
    top_result = results[0] if results else {}
    expected_mount = _explicit_query_mount(query, intent)
    expected_family = _explicit_query_family(query, intent)
    expected_category = _parsed_category(intent)
    dangerous_unknown = _dangerous_unknown_family_tokens(intent)
    weak_only_fallback = _is_weak_only_fallback(quality)

    boundary_reasons: list[str] = []
    if _result_family_conflict(expected_family, top_result):
        boundary_reasons.append("family_conflict")
    if _result_mount_conflict(expected_mount, top_result):
        boundary_reasons.append("mount_conflict")
    if _result_category_conflict(expected_category, top_result):
        boundary_reasons.append("category_conflict")
    if _result_variant_conflict(intent, top_result):
        boundary_reasons.append("variant_conflict")

    boundary_conflict_detected = bool(boundary_reasons)
    confidence = float(intent.get("confidence") or 0.0)
    required_confidence = 0.55 if intent.get("body_intent") else 0.60
    exact_model_like_match = _exact_model_like_match(intent, top_result, expected_mount)

    market_entry_block_reason: list[str] = []
    if not results:
        market_entry_block_reason.append("no_results")
    if int(quality.get("strong_result_count") or 0) <= 0:
        market_entry_block_reason.append("no_strong_results")
    if weak_only_fallback:
        market_entry_block_reason.append("weak_only_fallback")
    if confidence < required_confidence:
        market_entry_block_reason.append("low_query_intent_confidence")
    if dangerous_unknown:
        market_entry_block_reason.append("dangerous_unknown_family_token")
    if ui_hints.get("needs_disambiguation"):
        market_entry_block_reason.append("broad_query_refinement_required")
    if boundary_conflict_detected:
        market_entry_block_reason.extend(boundary_reasons)
    if top_result and top_result.get("match_quality") != "strong":
        market_entry_block_reason.append("top_result_not_strong")
    if not exact_model_like_match:
        market_entry_block_reason.append("exact_model_like_match_missing")

    market_entry_allowed = not market_entry_block_reason

    compatible_results = [
        result
        for result in results
        if _result_matches_query_summary_scope(result, intent, query, expected_family, expected_mount)
    ]
    compatible_counts = _build_market_counts(compatible_results)
    price_summary_block_reason: list[str] = []
    if not market_entry_allowed:
        price_summary_block_reason.append("market_entry_not_allowed")
    if not exact_model_like_match:
        price_summary_block_reason.append("exact_model_like_match_missing")
    if not compatible_results:
        price_summary_block_reason.append("no_query_compatible_results")
    if not any(_parse_price_number(result.get("price")) is not None for result in compatible_results):
        price_summary_block_reason.append("no_query_compatible_priced_results")

    price_summary_allowed = not price_summary_block_reason

    if market_entry_allowed:
        confidence_state = "exact_model_confident"
    elif dangerous_unknown:
        confidence_state = "locked_dangerous_unknown_family_token"
    elif weak_only_fallback:
        confidence_state = "locked_weak_only_fallback"
    elif ui_hints.get("needs_disambiguation"):
        confidence_state = "locked_broad_query_refinement"
    elif boundary_conflict_detected:
        confidence_state = "locked_boundary_conflict"
    elif confidence < 0.60:
        confidence_state = "locked_low_query_intent_confidence"
    else:
        confidence_state = "locked_market_entry_confidence"

    market_entry_title = None
    if market_entry_allowed and top_result:
        market_entry_title = _result_field(top_result, "model_canonical") or top_result.get("title")

    return {
        "market_entry_allowed": market_entry_allowed,
        "market_entry_block_reason": market_entry_block_reason,
        "price_summary_allowed": price_summary_allowed,
        "price_summary_block_reason": price_summary_block_reason,
        "model_entry_confidence_state": confidence_state,
        "boundary_conflict_detected": boundary_conflict_detected,
        "dangerous_unknown_family_token_detected": bool(dangerous_unknown),
        "dangerous_unknown_family_tokens": dangerous_unknown,
        "weak_only_fallback_detected": weak_only_fallback,
        "exact_model_like_match_detected": exact_model_like_match,
        "market_entry_title": market_entry_title,
        "compatible_result_count": len(compatible_results),
        "market_entry_metrics": compatible_counts,
        "price_summary_band": _format_price_band(compatible_results) if price_summary_allowed else "Not enough exact confidence for price summary",
        "expected_query_family": expected_family or None,
        "expected_query_mount": expected_mount,
        "required_query_confidence": required_confidence,
    }


def _parse_bool(value: Any, key: str) -> bool:
    if isinstance(value, bool):
        return value
    text = str(value).strip().lower()
    if text in {"1", "true", "yes", "y", "on"}:
        return True
    if text in {"0", "false", "no", "n", "off"}:
        return False
    raise SearchEndpointError(
        f"invalid_{key}",
        f"{key} must be true or false",
        details={"value": value},
    )


def _parse_int(value: Any, key: str, minimum: int, maximum: Optional[int] = None) -> int:
    try:
        parsed = int(str(value).strip())
    except (TypeError, ValueError):
        raise SearchEndpointError(
            f"invalid_{key}",
            f"{key} must be an integer",
            details={"value": value},
        )

    if parsed < minimum:
        raise SearchEndpointError(
            f"invalid_{key}",
            f"{key} must be greater than or equal to {minimum}",
            details={"value": value},
        )
    if maximum is not None and parsed > maximum:
        raise SearchEndpointError(
            f"invalid_{key}",
            f"{key} must be less than or equal to {maximum}",
            details={"value": value, "maximum": maximum},
        )
    return parsed


def _parse_float(value: Any, key: str) -> float:
    try:
        return float(str(value).strip())
    except (TypeError, ValueError):
        raise SearchEndpointError(
            f"invalid_{key}",
            f"{key} must be a number",
            details={"value": value},
        )


def parse_search_params(params: Mapping[str, Any]) -> dict[str, Any]:
    normalized = _normalize_params(params)
    query = str(normalized.get("q") or "").strip()
    if not query:
        raise SearchEndpointError("missing_query", "q query parameter is required")

    runtime = _load_runtime_dependencies()
    max_limit = int(runtime.get("max_limit") or DEFAULT_MAX_LIMIT)
    supported_sorts = set(runtime.get("supported_sorts") or DEFAULT_SUPPORTED_SORTS)

    limit = _parse_int(normalized.get("limit", 20), "limit", minimum=1, maximum=max_limit)
    offset = _parse_int(normalized.get("offset", 0), "offset", minimum=0)
    sort = str(normalized.get("sort") or "relevance").strip()
    if sort not in supported_sorts:
        raise SearchEndpointError(
            "invalid_sort",
            "sort is not supported",
            details={"value": sort, "allowed": sorted(supported_sorts)},
        )

    include_debug = False
    if normalized.get("include_debug") is not None:
        include_debug = _parse_bool(normalized["include_debug"], "include_debug")

    strong_only = False
    if normalized.get("strong_only") is not None:
        strong_only = _parse_bool(normalized["strong_only"], "strong_only")

    min_score = None
    if normalized.get("min_score") is not None and str(normalized.get("min_score")).strip():
        min_score = _parse_float(normalized["min_score"], "min_score")
        if min_score < 0 or min_score > 100:
            raise SearchEndpointError(
                "invalid_min_score",
                "min_score must be between 0 and 100",
                details={"value": normalized["min_score"]},
            )

    filters: dict[str, Any] = {}
    category = normalized.get("category")
    if category is not None:
        category_text = str(category).strip()
        if category_text not in ALLOWED_CATEGORIES:
            raise SearchEndpointError(
                "invalid_category",
                "category must be Lens, Body, or Accessory",
                details={"value": category, "allowed": sorted(ALLOWED_CATEGORIES)},
            )
        filters["category"] = category_text

    sold_quality = normalized.get("sold_quality")
    if sold_quality is not None:
        sold_quality_text = str(sold_quality).strip()
        if sold_quality_text not in ALLOWED_SOLD_QUALITIES:
            raise SearchEndpointError(
                "invalid_sold_quality",
                "sold_quality is not supported",
                details={"value": sold_quality, "allowed": sorted(ALLOWED_SOLD_QUALITIES)},
            )
        filters["sold_quality"] = sold_quality_text

    used_override = normalized.get("used_override")
    if used_override is not None:
        filters["used_override"] = _parse_bool(used_override, "used_override")

    for key in ["brand", "mount", "system", "source"]:
        value = normalized.get(key)
        if value is not None and str(value).strip():
            filters[key] = str(value).strip()

    for key in ["price_min", "price_max"]:
        value = normalized.get(key)
        if value is not None and str(value).strip():
            filters[key] = _parse_float(value, key)

    if (
        filters.get("price_min") is not None
        and filters.get("price_max") is not None
        and filters["price_min"] > filters["price_max"]
    ):
        raise SearchEndpointError(
            "invalid_price_range",
            "price_min must be less than or equal to price_max",
            details={"price_min": filters["price_min"], "price_max": filters["price_max"]},
        )

    return {
        "query": query,
        "limit": limit,
        "offset": offset,
        "sort": sort,
        "filters": filters,
        "include_debug": include_debug,
        "min_score": min_score,
        "strong_only": strong_only,
    }


def search_from_params(
    params: Mapping[str, Any],
    records: Optional[list[dict[str, Any]]] = None,
    path: str | Path | None = None,
) -> dict[str, Any]:
    runtime = _load_runtime_dependencies()
    search_records: Callable[..., dict[str, Any]] = runtime["search_records"]
    load_and_search: Callable[..., dict[str, Any]] = runtime["load_and_search"]
    build_query_ui_hints: Callable[..., dict[str, Any]] = runtime["build_query_ui_hints"]
    parsed = parse_search_params(params)
    if records is not None:
        response = search_records(
            query=parsed["query"],
            records=records,
            limit=parsed["limit"],
            offset=parsed["offset"],
            filters=parsed["filters"],
            sort=parsed["sort"],
            include_debug=parsed["include_debug"],
            strong_only=parsed["strong_only"],
            **({"min_score": parsed["min_score"]} if parsed["min_score"] is not None else {}),
        )
        response["ui_hints"] = build_query_ui_hints(parsed["query"], response.get("results"))
        response["market_entry_policy"] = build_market_entry_policy(parsed["query"], response, response["ui_hints"])
        response.update(response["market_entry_policy"])
        return response

    resolved_path = _resolve_search_index_path(path)
    response = load_and_search(
        query=parsed["query"],
        path=resolved_path,
        limit=parsed["limit"],
        offset=parsed["offset"],
        filters=parsed["filters"],
        sort=parsed["sort"],
        include_debug=parsed["include_debug"],
        strong_only=parsed["strong_only"],
        **({"min_score": parsed["min_score"]} if parsed["min_score"] is not None else {}),
    )
    response["ui_hints"] = build_query_ui_hints(parsed["query"], response.get("results"))
    response["market_entry_policy"] = build_market_entry_policy(parsed["query"], response, response["ui_hints"])
    response.update(response["market_entry_policy"])
    return response


def endpoint_response(
    params: Mapping[str, Any],
    records: Optional[list[dict[str, Any]]] = None,
    path: str | Path | None = None,
) -> tuple[int, dict[str, Any]]:
    try:
        return 200, search_from_params(params, records=records, path=path)
    except SearchEndpointError as exc:
        return exc.status, error_payload(exc.code, exc.message, exc.status, exc.details)
    except FileNotFoundError as exc:
        return 503, error_payload(
            "data_file_missing",
            "search data file was not found",
            503,
            {"path": str(getattr(exc, "filename", "") or path)},
        )
    except JSONDecodeError as exc:
        return 503, error_payload(
            "search_data_load_failed",
            "search data file is not valid JSON",
            503,
            {"message": str(exc)},
        )
    except ImportError as exc:
        return 503, error_payload(
            "search_runtime_bootstrap_failed",
            "search runtime dependencies could not be loaded",
            503,
            {"message": str(exc)},
        )
    except Exception as exc:  # pragma: no cover - final HTTP boundary guard
        return 500, error_payload(
            "search_endpoint_failed",
            "search endpoint failed",
            500,
            {"message": str(exc)},
        )


def _query_params_from_path(path: str) -> dict[str, list[str]]:
    return parse_qs(urlparse(path).query, keep_blank_values=True)


class handler(BaseHTTPRequestHandler):
    def _write_json(self, status: int, payload: dict[str, Any]) -> None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:
        try:
            status, payload = endpoint_response(_query_params_from_path(self.path))
        except Exception as exc:  # pragma: no cover - ultra-last serverless boundary
            status = 500
            payload = error_payload(
                "search_handler_failed",
                "search handler failed",
                500,
                {"message": str(exc)},
            )
        self._write_json(status, payload)

    def do_OPTIONS(self) -> None:
        self.send_response(204)
        self.send_header("Access-Control-Allow-Methods", "GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
