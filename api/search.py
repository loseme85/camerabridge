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
import sys
from http.server import BaseHTTPRequestHandler
from json import JSONDecodeError
from pathlib import Path
from typing import Any, Mapping, Optional
from urllib.parse import parse_qs, urlparse


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from search_index import DEFAULT_SEARCH_INDEX_PATH  # noqa: E402
from search_service import (  # noqa: E402
    MAX_LIMIT,
    SUPPORTED_SORTS,
    load_and_search,
    search_records,
)


ERROR_SCHEMA_VERSION = "search_service.error.v1"
ALLOWED_CATEGORIES = {"Lens", "Body", "Accessory"}
ALLOWED_SOLD_QUALITIES = {
    "asking",
    "sold",
    "sold_confirmed",
    "sold_likely",
    "unknown",
    "ended_unsold",
}


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


def _first(params: Mapping[str, Any], key: str) -> Optional[Any]:
    value = params.get(key)
    if isinstance(value, list):
        return value[0] if value else None
    return value


def _normalize_params(params: Mapping[str, Any]) -> dict[str, Any]:
    return {key: _first(params, key) for key in params}


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

    limit = _parse_int(normalized.get("limit", 20), "limit", minimum=1, maximum=MAX_LIMIT)
    offset = _parse_int(normalized.get("offset", 0), "offset", minimum=0)
    sort = str(normalized.get("sort") or "relevance").strip()
    if sort not in SUPPORTED_SORTS:
        raise SearchEndpointError(
            "invalid_sort",
            "sort is not supported",
            details={"value": sort, "allowed": sorted(SUPPORTED_SORTS)},
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
    path: str | Path = DEFAULT_SEARCH_INDEX_PATH,
) -> dict[str, Any]:
    parsed = parse_search_params(params)
    if records is not None:
        return search_records(
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

    return load_and_search(
        query=parsed["query"],
        path=path,
        limit=parsed["limit"],
        offset=parsed["offset"],
        filters=parsed["filters"],
        sort=parsed["sort"],
        include_debug=parsed["include_debug"],
        strong_only=parsed["strong_only"],
        **({"min_score": parsed["min_score"]} if parsed["min_score"] is not None else {}),
    )


def endpoint_response(
    params: Mapping[str, Any],
    records: Optional[list[dict[str, Any]]] = None,
    path: str | Path = DEFAULT_SEARCH_INDEX_PATH,
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
        status, payload = endpoint_response(_query_params_from_path(self.path))
        self._write_json(status, payload)

    def do_OPTIONS(self) -> None:
        self.send_response(204)
        self.send_header("Access-Control-Allow-Methods", "GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
