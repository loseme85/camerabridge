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
PRICE_EVIDENCE_SCAN_LIMIT = 60
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
    display = result.get("display_output") or {}
    display_map = {
        "category": "display_category",
        "label": "display_family",
        "model_canonical": "display_model",
        "model_raw": "display_model",
        "mount": "display_mount",
        "focal_length": "display_focal_length",
    }
    display_name = display_map.get(name)
    if display_name and display.get(display_name) not in {None, ""}:
        return display.get(display_name)
    return (result.get("final_output") or {}).get(name)


def _as_list(value: Any) -> list[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


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


def _result_matches_expected_family(expected_family: str, result: Mapping[str, Any]) -> bool:
    if not expected_family:
        return True
    expected_root = _family_root(expected_family)
    candidate_text = _normalize_text(
        _result_field(result, "model_canonical")
        or _result_field(result, "model_raw")
        or _result_field(result, "label")
        or result.get("title")
    )
    result_root = _family_root(candidate_text)
    if expected_root:
        if result_root:
            return result_root == expected_root
        return expected_root.lower() in candidate_text
    return _normalize_text(expected_family) in candidate_text


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


def _result_classification_conflict(top_result: Mapping[str, Any]) -> bool:
    display = top_result.get("display_output") or {}
    final = top_result.get("final_output") or {}
    return bool(
        display.get("classification_conflict_detected")
        or display.get("stale_normalization_detected")
        or
        final.get("classification_conflict_detected")
        or final.get("body_lens_boundary_conflict_detected")
        or final.get("stale_body_normalization_detected")
    )


def _result_text_blob(result: Mapping[str, Any]) -> str:
    parts = [
        result.get("title"),
        _result_field(result, "model_canonical"),
        _result_field(result, "model_raw"),
        _result_field(result, "label"),
        " ".join(str(item) for item in _as_list(_result_field(result, "variant")) if item),
        _result_field(result, "mount"),
        _result_field(result, "focal_length"),
    ]
    return _normalize_text(" ".join(str(item) for item in parts if item))


def _result_brand(result: Mapping[str, Any]) -> str:
    return str((result.get("final_output") or {}).get("brand") or "")


def _query_aperture_hint(query: str) -> str | None:
    lowered = _normalize_text(query)
    match = re.search(r"(?:f\s*|/)(0?\.\d+|\d+(?:\.\d+)?)\b", lowered)
    if match:
        return match.group(1)
    trailing = re.search(r"\b\d{2,3}\s+(0?\.\d+)\b", lowered)
    if trailing:
        return trailing.group(1)
    return None


def _query_variant_signals(intent: Mapping[str, Any]) -> list[dict[str, str]]:
    signals: list[dict[str, str]] = []
    for variant in intent.get("variant") or []:
        value = str(variant or "").strip()
        if value:
            signals.append({"kind": "variant", "value": value})
    generation = str(intent.get("generation") or "").strip()
    if generation:
        signals.append({"kind": "generation", "value": generation})
    filter_size = str(intent.get("filter_size") or "").strip()
    if filter_size:
        signals.append({"kind": "filter_size", "value": filter_size})
    optical_formula = str(intent.get("optical_formula") or "").strip()
    if optical_formula:
        signals.append({"kind": "optical_formula", "value": optical_formula})
    return signals


def _signal_patterns(kind: str, value: str) -> list[str]:
    lowered = _normalize_text(value)
    if kind == "generation":
        mapping = {
            "1st": ["1st", "first generation", "1세대", "v1", "version 1"],
            "2nd": ["2nd", "second generation", "2세대", "v2", "version 2"],
            "3rd": ["3rd", "third generation", "3세대", "v3", "version 3"],
            "4th": ["4th", "fourth generation", "4세대", "v4", "version 4"],
        }
        return mapping.get(lowered, [lowered])
    if kind == "filter_size":
        return [lowered]
    if kind == "optical_formula":
        if lowered == "8-element":
            return ["8-element", "8 element", "6군8매", "8매"]
        if lowered == "6-element":
            return ["6-element", "6 element", "6매"]
        return [lowered]
    variant_map = {
        "asph": ["asph", "aspherical"],
        "pre-asph": ["pre-asph", "pre asph", "preasph"],
        "apo": ["apo"],
        "aa": [" aa ", "double aspherical"],
        "8-element": ["8-element", "8 element", "6군8매", "8매"],
        "6-element": ["6-element", "6 element", "6매"],
        "rigid": ["rigid"],
        "dr": [" dr ", "dual range"],
        "collapsible": ["collapsible"],
        "steel rim": ["steel rim"],
        "reissue": ["reissue", "복각"],
        "close focus": ["close focus"],
        "floating element": ["floating element", "fle"],
    }
    patterns = variant_map.get(lowered)
    if patterns:
        return patterns
    return [lowered]


def _result_matches_signal(result: Mapping[str, Any], signal: Mapping[str, str]) -> bool:
    text = f" {_result_text_blob(result)} "
    value = str(signal.get("value") or "")
    kind = str(signal.get("kind") or "")
    if kind == "filter_size":
        return value.lower() in text
    for pattern in _signal_patterns(kind, value):
        normalized = _normalize_text(pattern)
        if normalized and normalized in text:
            return True
    return False


def _result_matches_base_model_scope(
    result: Mapping[str, Any],
    intent: Mapping[str, Any],
    expected_family: str,
    expected_mount: str | None,
) -> bool:
    if _result_classification_conflict(result):
        return False
    if intent.get("body_intent"):
        expected_body = _normalize_text(intent.get("body_intent"))
        result_body = _normalize_text(
            _result_field(result, "model_canonical") or _result_field(result, "model_raw") or _result_field(result, "label")
        )
        if str(_result_field(result, "category") or "") != "Body":
            return False
        if expected_body and expected_body not in result_body:
            return False
        return True

    if str(_result_field(result, "category") or "") != "Lens":
        return False
    if not _result_matches_expected_family(expected_family, result):
        return False
    if expected_mount and str(_result_field(result, "mount") or "") != expected_mount:
        return False
    expected_focal = str(intent.get("focal_length") or "")
    if expected_focal and str(_result_field(result, "focal_length") or "") != expected_focal:
        return False
    return True


def _result_matches_exact_variant_scope(
    result: Mapping[str, Any],
    intent: Mapping[str, Any],
    expected_family: str,
    expected_mount: str | None,
    signals: list[dict[str, str]],
) -> bool:
    if not _result_matches_base_model_scope(result, intent, expected_family, expected_mount):
        return False
    return all(_result_matches_signal(result, signal) for signal in signals)


def _result_matches_broader_family_scope(
    result: Mapping[str, Any],
    intent: Mapping[str, Any],
    expected_family: str,
    expected_mount: str | None,
) -> bool:
    if str(_result_field(result, "category") or "") != "Lens":
        return False
    if _result_classification_conflict(result):
        return False
    if expected_mount and str(_result_field(result, "mount") or "") != expected_mount:
        return False
    expected_root = _family_root(expected_family or intent.get("model_family") or "")
    result_root = _family_root(_result_field(result, "model_canonical") or _result_field(result, "model_raw") or "")
    if expected_root and result_root and expected_root != result_root:
        return False
    expected_focal = str(intent.get("focal_length") or "")
    if expected_focal and str(_result_field(result, "focal_length") or "") != expected_focal:
        return False
    return True


def _priced_results(results: list[Mapping[str, Any]]) -> list[Mapping[str, Any]]:
    return [result for result in results if _parse_price_number(result.get("price")) is not None]


def _strong_results(results: list[Mapping[str, Any]]) -> list[Mapping[str, Any]]:
    return [result for result in results if str(result.get("match_quality") or "") == "strong"]


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
    if not _result_matches_base_model_scope(result, intent, expected_family, expected_mount):
        return False
    if not intent.get("body_intent") and _result_variant_conflict(intent, result):
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


PRICE_ACCESSORY_KEYWORDS = {
    "hood",
    "cap",
    "case",
    "box",
    "filter",
    "finder",
    "adapter",
    "strap",
    "pouch",
    "protector",
    "handgrip",
    "thumb support",
    "base plate",
}
PRICE_REPAIR_KEYWORDS = {
    "repair",
    "parts",
    "for parts",
    "junk",
    "고장",
    "부품",
    "수리",
}
PRICE_RENTAL_KEYWORDS = {
    "deposit",
    "예약금",
    "rental",
    "렌탈",
}
THIRD_PARTY_PRICE_KEYWORDS = {
    "voigtlander",
    "nokton",
    "zeiss",
    "ttartisan",
    "7artisans",
    "light lens lab",
    "canon",
    "nikon",
    "sigma",
    "panasonic",
    "lumix",
    "leeworks",
    "thypoch",
    "laowa",
    "konica",
    "cooke",
}
PRICE_ALLOWED_SOLD_QUALITIES = {"asking", "sold_confirmed", "sold_likely", "sold", "unknown"}


def _result_title(result: Mapping[str, Any]) -> str:
    return str(result.get("title") or "")


def _result_currency(result: Mapping[str, Any]) -> str:
    return str(result.get("currency") or "")


def _contains_keyword(text: str, keywords: set[str]) -> bool:
    lowered = f" {_normalize_text(text)} "
    return any(f" {keyword} " in lowered for keyword in keywords)


def _query_aperture_value(intent: Mapping[str, Any], query: str) -> float | None:
    raw = str(intent.get("aperture") or _query_aperture_hint(query) or "").strip()
    if not raw:
        return None
    try:
        return float(raw)
    except ValueError:
        return None


def _extract_aperture_values(text: str) -> list[float]:
    values: list[float] = []
    for match in re.findall(r"(?:f\s*/?\s*|/)(0?\.\d+|\d+(?:\.\d+)?)\b", text.lower()):
        try:
            values.append(float(match))
        except ValueError:
            continue
    return values


def _result_matches_aperture_value(result: Mapping[str, Any], query_aperture: float | None) -> bool:
    if query_aperture is None:
        return True
    text = _result_text_blob(result)
    candidates = _extract_aperture_values(text)
    if not candidates:
        return False
    return any(abs(candidate - query_aperture) <= 0.11 for candidate in candidates)


def _normalize_dedupe_title(text: str) -> str:
    normalized = _normalize_text(text)
    normalized = re.sub(r"\bsn\.?\s*\d+\b", "", normalized)
    normalized = re.sub(r"\s+", " ", normalized).strip()
    return normalized


def _percentile(values: list[float], percentile: float) -> float:
    if not values:
        return 0.0
    ordered = sorted(values)
    if len(ordered) == 1:
        return ordered[0]
    index = (len(ordered) - 1) * percentile
    lower = int(index)
    upper = min(lower + 1, len(ordered) - 1)
    weight = index - lower
    return ordered[lower] * (1 - weight) + ordered[upper] * weight


def _pool_width_ratio(results: list[Mapping[str, Any]]) -> float | None:
    values = sorted(
        numeric
        for numeric in (_parse_price_number(result.get("price")) for result in results)
        if numeric is not None and numeric > 0
    )
    if not values:
        return None
    low = min(values)
    high = max(values)
    if low <= 0:
        return None
    return high / low


def _price_band_from_cleaned_results(results: list[Mapping[str, Any]]) -> dict[str, Any]:
    priced: list[tuple[float, str]] = []
    for result in results:
        numeric = _parse_price_number(result.get("price"))
        if numeric is None:
            continue
        priced.append((numeric, _result_currency(result)))
    if not priced:
        return {
            "band": "Not enough exact confidence for price summary",
            "raw_price_min": None,
            "raw_price_max": None,
            "currency": None,
        }
    currencies = sorted({currency or "Unknown" for _, currency in priced})
    values = [value for value, _ in priced]
    if len(currencies) != 1:
        return {
            "band": "Mixed currencies",
            "raw_price_min": min(values),
            "raw_price_max": max(values),
            "currency": None,
        }
    currency = currencies[0]
    formatter = lambda num: f"{num:,.0f}"
    return {
        "band": f"{currency} {formatter(min(values))} - {formatter(max(values))}",
        "raw_price_min": min(values),
        "raw_price_max": max(values),
        "currency": currency,
    }


def _humanize_policy_reason(reason: str) -> str:
    mapping = {
        "no_exact_or_strong_visible_results": "No exact strong visible listings yet.",
        "weak_only_fallback": "Results are visible, but not strong enough for model-level pricing.",
        "third_party_top_domination": "Top visible results are third-party or adjacent items.",
        "too_wide_price_band": "Reference prices are too spread out to show safely.",
        "too_noisy_broader_reference": "Broader family reference is too noisy to show safely.",
        "exact_model_like_match_missing": "Exact model evidence is missing from visible results.",
        "dangerous_unknown_family_token": "Query includes a model-like token that needs verification.",
        "boundary_conflict": "This query still conflicts across family, mount, or variant boundaries.",
        "search_aligned_exact_or_strong_visible": "Exact or strong compatible listings are visible.",
        "no_results": "No visible results are available yet.",
        "family_conflict": "Visible results do not stay inside the requested lens family.",
        "mount_conflict": "Visible results do not stay inside the requested mount.",
        "category_conflict": "Visible results do not stay inside the requested category.",
        "variant_conflict": "Visible results do not stay inside the requested variant.",
        "classification_conflict": "A listing-level classification conflict needs review first.",
        "market_entry_not_allowed": "Model-level summary is still locked for this query.",
        "insufficient_exact_variant_priced_results": "Exact variant price data is still limited.",
        "no_query_compatible_results": "No compatible visible results are ready for pricing.",
        "no_query_compatible_priced_results": "No compatible priced results are ready for pricing.",
        "aperture_only_scope_requires_broader_reference": "This query is only safe for broader family reference right now.",
        "not_enough_clean_priced_evidence": "Not enough clean priced listings are available yet.",
        "no_clean_priced_evidence": "Clean priced evidence is not available yet.",
        "accessory_contaminated": "Accessory prices are contaminating this reference pool.",
        "third_party_contaminated": "Third-party prices are contaminating this reference pool.",
        "wrong_model_contaminated": "Wrong-model prices are contaminating this reference pool.",
        "outlier_contaminated": "Outlier prices are contaminating this reference pool.",
        "locked_boundary_conflict": "Price summary is locked until boundary conflicts are resolved.",
        "locked_weak_only": "Price summary is locked until stronger visible results appear.",
    }
    return mapping.get(reason, reason.replace("_", " ").capitalize())


def _humanize_quality_state(state: str) -> str:
    mapping = {
        "clean_exact_variant_band": "Clean exact variant band",
        "clean_exact_base_model_band": "Clean exact base model band",
        "clean_broader_reference_band": "Clean broader family reference",
        "insufficient_priced_evidence": "Exact price data limited",
        "too_noisy_broader_reference": "Broader family reference is too noisy",
        "too_wide_price_band": "Reference prices are too spread out to show safely",
        "outlier_contaminated": "Outlier contamination detected",
        "accessory_contaminated": "Accessory contamination detected",
        "third_party_contaminated": "Third-party contamination detected",
        "wrong_model_contaminated": "Wrong-model contamination detected",
        "locked_boundary_conflict": "Price summary locked by boundary conflict",
        "locked_weak_only": "Price summary locked by weak fallback",
    }
    return mapping.get(state, state.replace("_", " ").capitalize())


def _result_signature(result: Mapping[str, Any]) -> tuple[str, str, str, str]:
    return (
        _normalize_dedupe_title(_result_title(result)),
        str(_parse_price_number(result.get("price")) or ""),
        _result_currency(result),
        _normalize_text(result.get("source")),
    )


def _build_interpreted_target(
    query: str,
    intent: Mapping[str, Any],
    expected_family: str,
    expected_mount: str | None,
    variant_signals: list[dict[str, str]],
    price_scope_label: str,
) -> str:
    if intent.get("body_intent"):
        parts = [str(intent.get("body_intent"))]
        if str(intent.get("brand") or ""):
            parts.insert(0, str(intent.get("brand")))
        return " ".join(part for part in parts if part)

    family = expected_family or str(intent.get("model_family") or "Lens candidate")
    focal = str(intent.get("focal_length") or "").strip()
    aperture = str(intent.get("aperture") or _query_aperture_hint(query) or "").strip()
    variant_text = ", ".join(str(signal.get("value") or "") for signal in variant_signals if signal.get("value"))
    parts = [family]
    if expected_mount:
        parts.append(expected_mount)
    if focal:
        parts.append(f"{focal}mm")
    if aperture:
        parts.append(f"f{aperture}")
    if variant_text:
        parts.append(variant_text)
    parts.append(f"candidate ({price_scope_label})")
    return " / ".join(part for part in parts if part)


def _result_matches_price_base_model_scope(
    result: Mapping[str, Any],
    intent: Mapping[str, Any],
    expected_family: str,
    expected_mount: str | None,
    query_aperture: float | None,
) -> bool:
    if not _result_matches_base_model_scope(result, intent, expected_family, expected_mount):
        return False
    return _result_matches_aperture_value(result, query_aperture)


def _result_matches_price_exact_variant_scope(
    result: Mapping[str, Any],
    intent: Mapping[str, Any],
    expected_family: str,
    expected_mount: str | None,
    signals: list[dict[str, str]],
    query_aperture: float | None,
) -> bool:
    if not _result_matches_price_base_model_scope(result, intent, expected_family, expected_mount, query_aperture):
        return False
    return all(_result_matches_signal(result, signal) for signal in signals)


def _result_matches_price_broader_family_scope(
    result: Mapping[str, Any],
    intent: Mapping[str, Any],
    expected_family: str,
    expected_mount: str | None,
    query_aperture: float | None,
) -> bool:
    if not _result_matches_broader_family_scope(result, intent, expected_family, expected_mount):
        return False
    return _result_matches_aperture_value(result, query_aperture)


def _build_price_evidence_pool(
    results: list[Mapping[str, Any]],
    *,
    pool_scope: str,
    query: str,
    intent: Mapping[str, Any],
    expected_family: str,
    expected_mount: str | None,
    variant_signals: list[dict[str, str]],
    query_aperture: float | None,
) -> dict[str, Any]:
    query_brand = _normalize_text(intent.get("brand"))
    raw_pool = list(results)
    raw_priced = [result for result in raw_pool if _parse_price_number(result.get("price")) is not None]

    kept: list[Mapping[str, Any]] = []
    excluded: list[dict[str, Any]] = []
    excluded_reason_counts: dict[str, int] = {}

    for result in raw_priced:
        reasons: list[str] = []
        title = _result_title(result)
        title_blob = _normalize_text(title)
        category = str(_result_field(result, "category") or "")
        sold_quality = _normalize_text(_result_field(result, "sold_quality"))

        if category == "Accessory" or _contains_keyword(title, PRICE_ACCESSORY_KEYWORDS):
            reasons.append("accessory")
        if _contains_keyword(title, PRICE_REPAIR_KEYWORDS):
            reasons.append("repair_or_parts")
        if _contains_keyword(title, PRICE_RENTAL_KEYWORDS):
            reasons.append("deposit_or_rental")
        if query_brand == "leica" and _contains_keyword(title, THIRD_PARTY_PRICE_KEYWORDS):
            reasons.append("third_party")
        if sold_quality and sold_quality not in PRICE_ALLOWED_SOLD_QUALITIES:
            reasons.append("sold_status_incompatible")
        if category not in {"Lens", "Body"}:
            reasons.append("category_mismatch")
        if _result_classification_conflict(result):
            reasons.append("classification_conflict")

        scope_match = True
        if pool_scope == "exact_variant":
            scope_match = _result_matches_price_exact_variant_scope(
                result,
                intent,
                expected_family,
                expected_mount,
                variant_signals,
                query_aperture,
            )
        elif pool_scope == "exact_base_model":
            scope_match = _result_matches_price_base_model_scope(
                result,
                intent,
                expected_family,
                expected_mount,
                query_aperture,
            )
        elif pool_scope == "broader_model_family":
            scope_match = _result_matches_price_broader_family_scope(
                result,
                intent,
                expected_family,
                expected_mount,
                query_aperture,
            )
        if not scope_match:
            reasons.append("wrong_model")

        if reasons:
            for reason in reasons:
                excluded_reason_counts[reason] = excluded_reason_counts.get(reason, 0) + 1
            excluded.append({"result": result, "reasons": reasons})
            continue
        kept.append(result)

    deduped: list[Mapping[str, Any]] = []
    seen_keys: set[tuple[str, str, str]] = set()
    duplicate_removed_count = 0
    for result in kept:
        key = (
            _normalize_dedupe_title(_result_title(result)),
            str(_parse_price_number(result.get("price")) or ""),
            _result_currency(result),
        )
        if key in seen_keys:
            duplicate_removed_count += 1
            excluded_reason_counts["duplicate"] = excluded_reason_counts.get("duplicate", 0) + 1
            excluded.append({"result": result, "reasons": ["duplicate"]})
            continue
        seen_keys.add(key)
        deduped.append(result)

    outlier_removed_count = 0
    cleaned = list(deduped)
    values = sorted(
        numeric
        for numeric in (_parse_price_number(result.get("price")) for result in deduped)
        if numeric is not None
    )
    if len(values) >= 4:
        q1 = _percentile(values, 0.25)
        q3 = _percentile(values, 0.75)
        iqr = q3 - q1
        lower = max(0.0, q1 - 1.5 * iqr)
        upper = q3 + 1.5 * iqr
        trimmed: list[Mapping[str, Any]] = []
        for result in cleaned:
            numeric = _parse_price_number(result.get("price"))
            if numeric is None:
                continue
            if numeric < lower or numeric > upper:
                outlier_removed_count += 1
                excluded_reason_counts["outlier"] = excluded_reason_counts.get("outlier", 0) + 1
                excluded.append({"result": result, "reasons": ["outlier"]})
                continue
            trimmed.append(result)
        cleaned = trimmed

    raw_band = _price_band_from_cleaned_results(raw_priced)
    cleaned_band = _price_band_from_cleaned_results(cleaned)
    width_ratio = _pool_width_ratio(cleaned)

    thresholds = {
        "exact_variant": {"min_count": 2, "max_ratio": 3.0, "clean_state": "clean_exact_variant_band"},
        "exact_base_model": {"min_count": 2, "max_ratio": 4.0, "clean_state": "clean_exact_base_model_band"},
        "broader_model_family": {"min_count": 3, "max_ratio": 2.0, "clean_state": "clean_broader_reference_band"},
    }
    threshold = thresholds[pool_scope]

    quality_reasons: list[str] = []
    if not cleaned:
        if excluded_reason_counts.get("accessory"):
            quality_state = "accessory_contaminated"
        elif excluded_reason_counts.get("third_party"):
            quality_state = "third_party_contaminated"
        elif excluded_reason_counts.get("wrong_model"):
            quality_state = "wrong_model_contaminated"
        else:
            quality_state = "insufficient_priced_evidence"
        quality_reasons.append("no_clean_priced_evidence")
    elif len(cleaned) < threshold["min_count"]:
        quality_state = "insufficient_priced_evidence"
        quality_reasons.append("not_enough_clean_priced_evidence")
    elif width_ratio is not None and width_ratio > threshold["max_ratio"]:
        quality_state = "too_noisy_broader_reference" if pool_scope == "broader_model_family" else "too_wide_price_band"
        quality_reasons.append("cleaned_price_band_too_wide")
    else:
        quality_state = threshold["clean_state"]
        if outlier_removed_count:
            quality_reasons.append("outliers_removed")
        if duplicate_removed_count:
            quality_reasons.append("duplicates_removed")

    return {
        "pool_scope": pool_scope,
        "raw_results": raw_pool,
        "raw_priced_results": raw_priced,
        "cleaned_results": cleaned,
        "excluded": excluded,
        "raw_pool_count": len(raw_pool),
        "priced_count": len(raw_priced),
        "cleaned_pool_count": len(cleaned),
        "excluded_pool_count": len(excluded),
        "excluded_reason_counts": excluded_reason_counts,
        "raw_price_min": raw_band["raw_price_min"],
        "raw_price_max": raw_band["raw_price_max"],
        "cleaned_price_min": cleaned_band["raw_price_min"],
        "cleaned_price_max": cleaned_band["raw_price_max"],
        "cleaned_band": cleaned_band["band"],
        "price_band_width_ratio": width_ratio,
        "price_band_quality_state": quality_state,
        "price_band_quality_reason": quality_reasons,
        "outlier_removed_count": outlier_removed_count,
        "duplicate_removed_count": duplicate_removed_count,
        "accessory_price_excluded_count": excluded_reason_counts.get("accessory", 0),
        "third_party_price_excluded_count": excluded_reason_counts.get("third_party", 0),
        "wrong_model_price_excluded_count": excluded_reason_counts.get("wrong_model", 0),
    }


def build_market_entry_policy(
    query: str,
    response: Mapping[str, Any],
    ui_hints: Mapping[str, Any],
    evidence_response: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    intent = response.get("intent") or {}
    results = list(response.get("results") or [])
    evidence_results = list((evidence_response or response).get("results") or results)
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
    if _result_classification_conflict(top_result):
        boundary_reasons.append("classification_conflict")

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
    variant_signals = _query_variant_signals(intent)
    query_aperture = _query_aperture_value(intent, query)
    visible_exact_base_model_results = [
        result
        for result in results
        if _result_matches_base_model_scope(result, intent, expected_family, expected_mount)
    ]
    visible_broader_family_results = [
        result
        for result in results
        if _result_matches_broader_family_scope(result, intent, expected_family, expected_mount)
    ]
    visible_exact_variant_results = [
        result
        for result in results
        if variant_signals and _result_matches_exact_variant_scope(result, intent, expected_family, expected_mount, variant_signals)
    ]
    exact_base_model_results = [
        result
        for result in evidence_results
        if _result_matches_base_model_scope(result, intent, expected_family, expected_mount)
    ]
    broader_family_results = [
        result
        for result in evidence_results
        if _result_matches_broader_family_scope(result, intent, expected_family, expected_mount)
    ]
    exact_variant_results = [
        result
        for result in evidence_results
        if variant_signals and _result_matches_exact_variant_scope(result, intent, expected_family, expected_mount, variant_signals)
    ]

    exact_variant_pool = _build_price_evidence_pool(
        exact_variant_results,
        pool_scope="exact_variant",
        query=query,
        intent=intent,
        expected_family=expected_family,
        expected_mount=expected_mount,
        variant_signals=variant_signals,
        query_aperture=query_aperture,
    )
    exact_base_model_pool = _build_price_evidence_pool(
        exact_base_model_results,
        pool_scope="exact_base_model",
        query=query,
        intent=intent,
        expected_family=expected_family,
        expected_mount=expected_mount,
        variant_signals=variant_signals,
        query_aperture=query_aperture,
    )
    broader_family_pool = _build_price_evidence_pool(
        broader_family_results,
        pool_scope="broader_model_family",
        query=query,
        intent=intent,
        expected_family=expected_family,
        expected_mount=expected_mount,
        variant_signals=variant_signals,
        query_aperture=query_aperture,
    )

    exact_variant_priced = list(exact_variant_pool["cleaned_results"])
    exact_base_model_priced = list(exact_base_model_pool["cleaned_results"])
    broader_family_priced = list(broader_family_pool["cleaned_results"])
    exact_variant_strong_visible = _strong_results(visible_exact_variant_results)
    exact_base_model_strong_visible = _strong_results(visible_exact_base_model_results)
    aperture_hint = _query_aperture_hint(query)
    aperture_only_variant = (
        not intent.get("body_intent")
        and not variant_signals
        and bool(intent.get("aperture") or aperture_hint)
        and bool(expected_family)
        and bool(intent.get("focal_length"))
    )
    exact_or_strong_visible_result_count = len(exact_variant_strong_visible if variant_signals else exact_base_model_strong_visible)
    third_party_top_domination_detected = bool(
        expected_category == "Lens"
        and str(intent.get("brand") or "").lower() == "leica"
        and top_result
        and _result_brand(top_result)
        and _result_brand(top_result).lower() != "leica"
    )

    if not top_result:
        top_result_compatibility = "no_results"
    elif boundary_conflict_detected:
        top_result_compatibility = "boundary_conflict"
    elif third_party_top_domination_detected:
        top_result_compatibility = "third_party_top_domination"
    elif variant_signals and _result_matches_exact_variant_scope(top_result, intent, expected_family, expected_mount, variant_signals):
        top_result_compatibility = "exact_variant_strong" if str(top_result.get("match_quality") or "") == "strong" else "exact_variant_weak"
    elif _result_matches_base_model_scope(top_result, intent, expected_family, expected_mount):
        top_result_compatibility = "exact_base_model_strong" if str(top_result.get("match_quality") or "") == "strong" else "exact_base_model_weak"
    elif _result_matches_broader_family_scope(top_result, intent, expected_family, expected_mount):
        top_result_compatibility = "broader_family_only"
    else:
        top_result_compatibility = "query_incompatible"

    price_scope_search_alignment_reason: list[str] = []
    if weak_only_fallback:
        price_scope_search_alignment_reason.append("weak_only_fallback")
    if boundary_conflict_detected:
        price_scope_search_alignment_reason.append("boundary_conflict")
    if third_party_top_domination_detected:
        price_scope_search_alignment_reason.append("third_party_top_domination")
    if exact_or_strong_visible_result_count <= 0:
        price_scope_search_alignment_reason.append("no_exact_or_strong_visible_results")

    price_scope_search_aligned = not price_scope_search_alignment_reason
    if not results:
        search_confidence_state = "no_results"
    elif boundary_conflict_detected:
        search_confidence_state = "boundary_conflict"
    elif weak_only_fallback:
        search_confidence_state = "weak_only_fallback"
    elif third_party_top_domination_detected:
        search_confidence_state = "third_party_top_domination"
    elif exact_or_strong_visible_result_count <= 0:
        search_confidence_state = "no_exact_or_strong_visible_results"
    else:
        search_confidence_state = "search_aligned_exact_or_strong_visible"

    price_summary_block_reason: list[str] = []
    broader_reference_allowed = False
    broader_reference_label = None
    broader_reference_band = None
    broader_reference_locked_reason: str | None = None
    broader_reference_quality_state = None
    broader_reference_quality_reason: list[str] = []
    broader_reference_source_scope: str | None = None
    broader_reference_pool_count = 0
    broader_reference_excluded_pool_count = 0
    broader_reference_outlier_removed_count = 0
    entry_scope = "parent_model" if market_entry_allowed else "hold_conflict"
    price_scope = "insufficient_exact_data"
    price_scope_label = "Price summary locked"
    price_scope_confidence_state = "price_scope_locked"
    price_evidence_scope = "insufficient_exact_data"
    price_band_quality_state = "insufficient_priced_evidence"
    price_band_quality_reason: list[str] = []
    raw_price_min = None
    raw_price_max = None
    cleaned_price_min = None
    cleaned_price_max = None
    price_band_width_ratio = None
    excluded_pool_count = 0
    excluded_reason_counts: dict[str, int] = {}
    outlier_removed_count = 0
    accessory_price_excluded_count = 0
    third_party_price_excluded_count = 0
    wrong_model_price_excluded_count = 0
    unlock_requirements: list[str] = []

    if intent.get("body_intent"):
        if not market_entry_allowed:
            price_summary_block_reason.append("market_entry_not_allowed")
        if not exact_model_like_match:
            price_summary_block_reason.append("exact_model_like_match_missing")
        if not compatible_results:
            price_summary_block_reason.append("no_query_compatible_results")
        if not exact_base_model_priced:
            price_summary_block_reason.append("no_query_compatible_priced_results")
        price_summary_allowed = not price_summary_block_reason
        if price_summary_allowed:
            price_scope = "exact_base_model"
            price_scope_label = "Exact base model price"
            price_scope_confidence_state = "exact_base_model_ready"
            price_evidence_scope = "exact_base_model"
            price_band_quality_state = "clean_exact_base_model_band"
        elif boundary_conflict_detected:
            price_scope = "blocked_boundary_conflict"
            price_scope_label = "Price summary locked"
            price_scope_confidence_state = "boundary_conflict_locked"
            price_evidence_scope = "blocked_boundary_conflict"
            price_band_quality_state = "locked_boundary_conflict"
        elif weak_only_fallback:
            price_scope = "blocked_weak_only"
            price_scope_label = "Price summary locked"
            price_scope_confidence_state = "weak_only_locked"
            price_evidence_scope = "blocked_weak_only"
            price_band_quality_state = "locked_weak_only"
        else:
            price_scope = "insufficient_exact_data"
            price_scope_label = "Price summary locked"
            price_scope_confidence_state = "body_price_scope_locked"
            price_evidence_scope = "insufficient_exact_data"
    elif boundary_conflict_detected:
        price_summary_allowed = False
        price_summary_block_reason.append("boundary_conflict")
        price_scope = "blocked_boundary_conflict"
        price_scope_label = "Price summary locked"
        price_scope_confidence_state = "boundary_conflict_locked"
        price_evidence_scope = "blocked_boundary_conflict"
        price_band_quality_state = "locked_boundary_conflict"
    elif variant_signals:
        entry_scope = "exact_variant" if market_entry_allowed else entry_scope
        price_evidence_scope = "exact_variant"
        if (
            len(exact_variant_priced) >= 2
            and price_scope_search_aligned
            and exact_variant_pool["price_band_quality_state"] == "clean_exact_variant_band"
        ):
            price_summary_allowed = True
            price_scope = "exact_variant"
            price_scope_label = "Exact variant price"
            price_scope_confidence_state = "exact_variant_ready_search_aligned"
        else:
            price_summary_allowed = False
            if weak_only_fallback:
                price_scope = "blocked_weak_only"
                price_scope_label = "Price summary locked"
                price_scope_confidence_state = "exact_variant_search_mismatch"
            elif third_party_top_domination_detected or exact_or_strong_visible_result_count <= 0:
                price_scope = "blocked_weak_only"
                price_scope_label = "Price summary locked"
                price_scope_confidence_state = "exact_variant_search_mismatch"
            else:
                price_scope = "insufficient_exact_data"
                price_scope_label = "Exact variant price data limited"
                price_scope_confidence_state = "exact_variant_data_limited"
            if len(exact_variant_priced) < 2:
                price_summary_block_reason.append("insufficient_exact_variant_priced_results")
            if exact_variant_pool["price_band_quality_state"] not in {"clean_exact_variant_band", "insufficient_priced_evidence"}:
                price_summary_block_reason.append(exact_variant_pool["price_band_quality_state"])
            price_summary_block_reason.extend(
                reason
                for reason in price_scope_search_alignment_reason
                if reason not in price_summary_block_reason
            )
            reference_pool = exact_base_model_pool if exact_base_model_priced else broader_family_pool
            if reference_pool["cleaned_results"]:
                broader_reference_quality_state = str(reference_pool["price_band_quality_state"] or "")
                broader_reference_quality_reason = list(reference_pool["price_band_quality_reason"] or [])
                broader_reference_source_scope = "exact_base_model_pool" if reference_pool is exact_base_model_pool else "broader_family_pool"
                broader_reference_pool_count = int(reference_pool["cleaned_pool_count"])
                broader_reference_excluded_pool_count = int(reference_pool["excluded_pool_count"])
                broader_reference_outlier_removed_count = int(reference_pool["outlier_removed_count"])
                if reference_pool["price_band_quality_state"] == "clean_broader_reference_band":
                    broader_reference_allowed = True
                    broader_reference_label = "Broader family reference"
                    broader_reference_band = reference_pool["cleaned_band"]
                elif reference_pool["price_band_quality_state"] == "clean_exact_base_model_band":
                    broader_reference_allowed = True
                    broader_reference_label = "Exact base model reference"
                    broader_reference_band = reference_pool["cleaned_band"]
                else:
                    broader_reference_allowed = False
                    broader_reference_locked_reason = reference_pool["price_band_quality_state"]
    elif weak_only_fallback:
        price_summary_allowed = False
        price_summary_block_reason.append("weak_only_fallback")
        price_scope = "blocked_weak_only"
        price_scope_label = "Price summary locked"
        price_scope_confidence_state = "weak_only_locked"
        price_evidence_scope = "blocked_weak_only"
        price_band_quality_state = "locked_weak_only"
    elif aperture_only_variant:
        price_summary_allowed = False
        price_scope = "broader_model_family"
        price_scope_label = "Broader family reference"
        price_scope_confidence_state = "broader_family_reference_only"
        price_summary_block_reason.append("aperture_only_scope_requires_broader_reference")
        price_evidence_scope = "broader_model_family"
        broader_reference_quality_state = str(broader_family_pool["price_band_quality_state"] or "")
        broader_reference_quality_reason = list(broader_family_pool["price_band_quality_reason"] or [])
        broader_reference_source_scope = "broader_family_pool"
        broader_reference_pool_count = int(broader_family_pool["cleaned_pool_count"])
        broader_reference_excluded_pool_count = int(broader_family_pool["excluded_pool_count"])
        broader_reference_outlier_removed_count = int(broader_family_pool["outlier_removed_count"])
        if broader_family_priced and broader_family_pool["price_band_quality_state"] == "clean_broader_reference_band":
            broader_reference_allowed = True
            broader_reference_label = "Broader family reference"
            broader_reference_band = broader_family_pool["cleaned_band"]
        elif broader_family_pool["cleaned_results"]:
            broader_reference_locked_reason = broader_family_pool["price_band_quality_state"]
    else:
        price_evidence_scope = "exact_base_model"
        if not market_entry_allowed:
            price_summary_block_reason.append("market_entry_not_allowed")
        if not visible_exact_base_model_results:
            price_summary_block_reason.append("no_query_compatible_results")
        if not exact_base_model_priced:
            price_summary_block_reason.append("no_query_compatible_priced_results")
        if (
            exact_base_model_priced
            and exact_base_model_pool["price_band_quality_state"] != "clean_exact_base_model_band"
        ):
            price_summary_block_reason.append(exact_base_model_pool["price_band_quality_state"])
        price_summary_allowed = not price_summary_block_reason
        if price_summary_allowed:
            price_scope = "exact_base_model"
            price_scope_label = "Exact base model price"
            price_scope_confidence_state = "exact_base_model_ready"
        elif broader_family_priced and broader_family_pool["price_band_quality_state"] == "clean_broader_reference_band":
            price_scope = "broader_model_family"
            price_scope_label = "Broader family reference"
            price_scope_confidence_state = "broader_family_reference_only"
            broader_reference_quality_state = str(broader_family_pool["price_band_quality_state"] or "")
            broader_reference_quality_reason = list(broader_family_pool["price_band_quality_reason"] or [])
            broader_reference_source_scope = "broader_family_pool"
            broader_reference_pool_count = int(broader_family_pool["cleaned_pool_count"])
            broader_reference_excluded_pool_count = int(broader_family_pool["excluded_pool_count"])
            broader_reference_outlier_removed_count = int(broader_family_pool["outlier_removed_count"])
            broader_reference_allowed = True
            broader_reference_label = "Broader family reference"
            broader_reference_band = broader_family_pool["cleaned_band"]
        elif broader_family_pool["cleaned_results"]:
            price_scope = "insufficient_exact_data"
            price_scope_label = "Price summary locked"
            price_scope_confidence_state = "price_scope_locked"
            broader_reference_quality_state = str(broader_family_pool["price_band_quality_state"] or "")
            broader_reference_quality_reason = list(broader_family_pool["price_band_quality_reason"] or [])
            broader_reference_source_scope = "broader_family_pool"
            broader_reference_pool_count = int(broader_family_pool["cleaned_pool_count"])
            broader_reference_excluded_pool_count = int(broader_family_pool["excluded_pool_count"])
            broader_reference_outlier_removed_count = int(broader_family_pool["outlier_removed_count"])
            broader_reference_locked_reason = broader_family_pool["price_band_quality_state"]
        else:
            price_scope = "insufficient_exact_data"
            price_scope_label = "Price summary locked"
            price_scope_confidence_state = "price_scope_locked"

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

    current_ui_label_safe = bool(
        (price_summary_allowed and price_scope_label in {"Exact variant price", "Exact base model price"})
        or (not price_summary_allowed and price_scope_label in {"Exact variant price data limited", "Broader family reference", "Price summary locked"})
    )

    selected_pool = exact_variant_pool
    if price_evidence_scope == "exact_base_model":
        selected_pool = exact_base_model_pool
    elif price_evidence_scope == "broader_model_family":
        selected_pool = broader_family_pool
    elif price_scope == "broader_model_family" and broader_family_pool["cleaned_results"]:
        selected_pool = broader_family_pool

    price_band_quality_state = str(selected_pool["price_band_quality_state"])
    price_band_quality_reason = list(selected_pool["price_band_quality_reason"])
    raw_price_min = selected_pool["raw_price_min"]
    raw_price_max = selected_pool["raw_price_max"]
    cleaned_price_min = selected_pool["cleaned_price_min"]
    cleaned_price_max = selected_pool["cleaned_price_max"]
    price_band_width_ratio = selected_pool["price_band_width_ratio"]
    excluded_pool_count = int(selected_pool["excluded_pool_count"])
    excluded_reason_counts = dict(selected_pool["excluded_reason_counts"])
    outlier_removed_count = int(selected_pool["outlier_removed_count"])
    accessory_price_excluded_count = int(selected_pool["accessory_price_excluded_count"])
    third_party_price_excluded_count = int(selected_pool["third_party_price_excluded_count"])
    wrong_model_price_excluded_count = int(selected_pool["wrong_model_price_excluded_count"])

    if variant_signals and len(exact_variant_priced) < 2:
        unlock_requirements.append("Need 2+ exact variant priced listings.")
    if variant_signals and not exact_or_strong_visible_result_count:
        unlock_requirements.append("Need exact or strong compatible visible Leica results.")
    if excluded_reason_counts.get("accessory"):
        unlock_requirements.append("Need no accessory contamination in the selected price pool.")
    if excluded_reason_counts.get("third_party"):
        unlock_requirements.append("Need no third-party contamination in the selected price pool.")
    if price_band_quality_state in {"too_wide_price_band", "too_noisy_broader_reference"}:
        unlock_requirements.append("Need cleaned price band within an acceptable width.")
    if boundary_conflict_detected:
        unlock_requirements.append("Need no boundary conflict between family, mount, and variant.")

    exact_variant_signatures = {_result_signature(result) for result in exact_variant_pool["cleaned_results"]}
    exact_base_signatures = {_result_signature(result) for result in exact_base_model_pool["cleaned_results"]}
    broader_signatures = {_result_signature(result) for result in broader_family_pool["cleaned_results"]}

    excluded_reason_by_signature: dict[tuple[str, str, str, str], list[str]] = {}
    for pool in (exact_variant_pool, exact_base_model_pool, broader_family_pool):
        for excluded_item in pool.get("excluded", []) if isinstance(pool.get("excluded"), list) else []:
            result = excluded_item.get("result") or {}
            excluded_reason_by_signature[_result_signature(result)] = list(excluded_item.get("reasons") or [])

    top_result_evidence = []
    for result in results[:5]:
        signature = _result_signature(result)
        excluded_reasons = excluded_reason_by_signature.get(signature, [])
        if signature in exact_variant_signatures:
            evidence_pool = "exact_variant_pool"
            used_for_price = price_summary_allowed and price_scope == "exact_variant"
        elif signature in exact_base_signatures:
            evidence_pool = "exact_base_model_pool"
            used_for_price = price_summary_allowed and price_scope == "exact_base_model"
        elif signature in broader_signatures:
            evidence_pool = "broader_family_pool"
            used_for_price = bool(broader_reference_allowed)
        else:
            evidence_pool = "excluded_pool" if excluded_reasons else "visible_only"
            used_for_price = False

        if boundary_conflict_detected:
            compatibility_label = "Boundary conflict"
        elif third_party_top_domination_detected and result is top_result:
            compatibility_label = "Third-party top result"
        elif variant_signals and _result_matches_exact_variant_scope(result, intent, expected_family, expected_mount, variant_signals):
            compatibility_label = "Exact variant"
        elif _result_matches_base_model_scope(result, intent, expected_family, expected_mount):
            compatibility_label = "Exact base model"
        elif _result_matches_broader_family_scope(result, intent, expected_family, expected_mount):
            compatibility_label = "Broader family"
        else:
            compatibility_label = "Query incompatible"

        top_result_evidence.append(
            {
                "title": _result_title(result),
                "source": str(result.get("source") or ""),
                "price": str(result.get("price") or ""),
                "compatibility_label": compatibility_label,
                "evidence_pool": evidence_pool,
                "used_for_price": used_for_price,
                "excluded_reason": [_humanize_policy_reason(reason) for reason in excluded_reasons],
                "display_category": str(_result_field(result, "category") or ""),
                "display_model": str(_result_field(result, "model_canonical") or _result_field(result, "model_raw") or ""),
            }
        )

    display_price_summary_allowed = bool(price_summary_allowed)
    display_price_scope_label = price_scope_label
    display_price_band = price_summary_band = (
        exact_variant_pool["cleaned_band"]
        if price_summary_allowed and price_scope == "exact_variant"
        else exact_base_model_pool["cleaned_band"]
        if price_summary_allowed
        else "Exact variant price data limited"
        if price_scope == "insufficient_exact_data"
        else "Price summary locked"
    )
    display_price_band_source = price_evidence_scope
    display_broader_reference_allowed = bool(broader_reference_allowed)
    display_broader_reference_label = broader_reference_label
    display_broader_reference_band = broader_reference_band if broader_reference_allowed else None
    display_broader_reference_locked_reason = (
        _humanize_policy_reason(broader_reference_locked_reason) if broader_reference_locked_reason else None
    )
    display_price_band_quality_state = _humanize_quality_state(price_band_quality_state)
    display_unlock_requirements = unlock_requirements
    display_evidence_pool_summary = {
        "exact_variant_pool_count": int(exact_variant_pool["cleaned_pool_count"]),
        "exact_base_model_pool_count": int(exact_base_model_pool["cleaned_pool_count"]),
        "broader_family_pool_count": int(broader_family_pool["cleaned_pool_count"]),
        "excluded_pool_count": excluded_pool_count,
        "outlier_removed_count": outlier_removed_count,
        "broader_reference_allowed": broader_reference_allowed,
        "price_band_quality_state": display_price_band_quality_state,
    }
    display_match_state_message = _humanize_policy_reason(
        alignmentReasons[0] if (alignmentReasons := price_scope_search_alignment_reason) else search_confidence_state
    )
    display_query_review = {
        "query": query,
        "interpreted_target": _build_interpreted_target(
            query,
            intent,
            expected_family,
            expected_mount,
            variant_signals,
            price_scope_label,
        ),
        "category": expected_category or ("Body" if intent.get("body_intent") else "Lens"),
        "match_state": display_match_state_message,
        "price_status": price_scope_label,
    }

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
        "entry_scope": entry_scope,
        "price_evidence_scope": price_evidence_scope,
        "price_scope": price_scope,
        "price_scope_label": price_scope_label,
        "price_scope_confidence_state": price_scope_confidence_state,
        "search_confidence_state": search_confidence_state,
        "top_result_compatibility": top_result_compatibility,
        "exact_or_strong_visible_result_count": exact_or_strong_visible_result_count,
        "third_party_top_domination_detected": third_party_top_domination_detected,
        "price_scope_search_aligned": price_scope_search_aligned,
        "price_scope_search_alignment_reason": price_scope_search_alignment_reason,
        "variant_tokens_detected": [signal["value"] for signal in variant_signals],
        "exact_variant_result_count": len(exact_variant_results),
        "exact_variant_pool_count": int(exact_variant_pool["cleaned_pool_count"]),
        "exact_variant_priced_count": len(exact_variant_priced),
        "exact_base_model_result_count": len(exact_base_model_results),
        "exact_base_model_pool_count": int(exact_base_model_pool["cleaned_pool_count"]),
        "exact_base_model_priced_count": len(exact_base_model_priced),
        "broader_family_result_count": len(broader_family_results),
        "broader_family_pool_count": int(broader_family_pool["cleaned_pool_count"]),
        "broader_family_priced_count": len(broader_family_priced),
        "excluded_pool_count": excluded_pool_count,
        "excluded_reason_counts": excluded_reason_counts,
        "raw_price_min": raw_price_min,
        "raw_price_max": raw_price_max,
        "cleaned_price_min": cleaned_price_min,
        "cleaned_price_max": cleaned_price_max,
        "price_band_width_ratio": price_band_width_ratio,
        "price_band_quality_state": price_band_quality_state,
        "price_band_quality_reason": price_band_quality_reason,
        "outlier_removed_count": outlier_removed_count,
        "accessory_price_excluded_count": accessory_price_excluded_count,
        "third_party_price_excluded_count": third_party_price_excluded_count,
        "wrong_model_price_excluded_count": wrong_model_price_excluded_count,
        "broader_reference_allowed": broader_reference_allowed,
        "broader_reference_label": broader_reference_label,
        "broader_reference_band": broader_reference_band,
        "broader_reference_locked_reason": broader_reference_locked_reason,
        "broader_reference_quality_state": broader_reference_quality_state,
        "broader_reference_quality_reason": broader_reference_quality_reason,
        "broader_reference_source_scope": broader_reference_source_scope,
        "broader_reference_pool_count": broader_reference_pool_count,
        "broader_reference_excluded_pool_count": broader_reference_excluded_pool_count,
        "broader_reference_outlier_removed_count": broader_reference_outlier_removed_count,
        "unlock_requirements": unlock_requirements,
        "display_price_summary_allowed": display_price_summary_allowed,
        "display_price_scope_label": display_price_scope_label,
        "display_price_band": display_price_band,
        "display_price_band_source": display_price_band_source,
        "display_broader_reference_allowed": display_broader_reference_allowed,
        "display_broader_reference_label": display_broader_reference_label,
        "display_broader_reference_band": display_broader_reference_band,
        "display_broader_reference_locked_reason": display_broader_reference_locked_reason,
        "display_price_band_quality_state": display_price_band_quality_state,
        "display_unlock_requirements": display_unlock_requirements,
        "display_evidence_pool_summary": display_evidence_pool_summary,
        "display_top_result_evidence": top_result_evidence,
        "display_match_state_message": display_match_state_message,
        "display_query_review": display_query_review,
        "current_ui_label_safe": current_ui_label_safe,
        "price_summary_band": price_summary_band,
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
    evidence_limit = min(int(runtime.get("max_limit") or DEFAULT_MAX_LIMIT), max(parsed["limit"], PRICE_EVIDENCE_SCAN_LIMIT))

    def build_evidence_response() -> dict[str, Any] | None:
        if evidence_limit <= parsed["limit"] and parsed["offset"] == 0:
            return None
        kwargs = dict(
            query=parsed["query"],
            limit=evidence_limit,
            offset=0,
            filters=parsed["filters"],
            sort=parsed["sort"],
            include_debug=parsed["include_debug"],
            strong_only=parsed["strong_only"],
        )
        if parsed["min_score"] is not None:
            kwargs["min_score"] = parsed["min_score"]
        if records is not None:
            return search_records(records=records, **kwargs)
        return load_and_search(path=_resolve_search_index_path(path), **kwargs)

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
        evidence_response = build_evidence_response()
        response["market_entry_policy"] = build_market_entry_policy(
            parsed["query"],
            response,
            response["ui_hints"],
            evidence_response=evidence_response,
        )
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
    evidence_response = build_evidence_response()
    response["market_entry_policy"] = build_market_entry_policy(
        parsed["query"],
        response,
        response["ui_hints"],
        evidence_response=evidence_response,
    )
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
