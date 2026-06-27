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
import os
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

    from search_index import DEFAULT_SEARCH_INDEX_PATH, load_search_index_metadata  # noqa: WPS433
    from search_service import MAX_LIMIT, SUPPORTED_SORTS, load_and_search, search_records  # noqa: WPS433
    from search_ui_hints import build_query_ui_hints  # noqa: WPS433

    _RUNTIME_CACHE = {
        "default_search_index_path": DEFAULT_SEARCH_INDEX_PATH,
        "load_search_index_metadata": load_search_index_metadata,
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


# Read-only runtime index metadata for QA/preview verification.
def _build_index_meta(index_path: Path | None, request_query: str) -> dict[str, Any]:
    meta = {
        "index_path": str(index_path.resolve()) if index_path is not None else None,
        "index_generated_at": None,
        "index_record_count": None,
        "index_source_path": None,
        "deployment_commit": os.environ.get("VERCEL_GIT_COMMIT_SHA") or os.environ.get("GITHUB_SHA"),
        "api_runtime": "python-search-endpoint",
        "request_query": request_query,
    }
    if index_path is None:
        return meta

    runtime = _load_runtime_dependencies()
    index_metadata = runtime["load_search_index_metadata"](index_path)
    meta.update({
        "index_generated_at": index_metadata.get("generated_at"),
        "index_record_count": index_metadata.get("record_count"),
        "index_source_path": index_metadata.get("source_path"),
    })
    return meta


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
    if "tri-elmar" in text or "trielmar" in text:
        return "Tri-Elmar"
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
    lowered = re.sub(r"\b(?:summilux|summicron|noctilux|elmarit)-m\b", lambda m: m.group(0).split("-")[0], lowered)
    token_set = set(re.findall(r"[a-z0-9./-]+", lowered))
    if any(token in {"ltm", "l39", "m39", "screw"} for token in token_set):
        return "L"
    if "sl" in token_set:
        return "SL"
    if "r" in token_set:
        return "R"
    if "m" in token_set:
        return "M"
    return None


def _explicit_query_family(query: str, intent: Mapping[str, Any]) -> str:
    lowered = _normalize_text(query)
    lowered = re.sub(r"\b(?:summilux|summicron|noctilux|elmarit)-m\b", lambda m: m.group(0).split("-")[0], lowered)
    query_mount = _explicit_query_mount(query, intent)
    parsed_family = str(intent.get("model_family") or "")

    if parsed_family in {
        "APO-Summicron-SL",
        "APO-Summicron-M",
        "Vario-Elmarit-SL",
        "Vario-Elmar-R",
        "Vario-Elmarit-R",
    }:
        return parsed_family

    if "apo-summicron" in lowered or re.search(r"\bapo\s+\d{2,3}\s+summicron\b|\bapo\s+summicron\b", lowered):
        return "APO-Summicron"

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
    expected_variant_values = {item.strip().upper() for item in expected_variants if item}
    if (
        _result_is_summilux_35_context(top_result)
        and "FLE2" in expected_variant_values
        and _result_has_fle1_only_signal(top_result)
    ):
        return False
    if _tri_elmar_range_matches_query(intent, top_result):
        return False
    expected_family = _explicit_query_family(str(intent.get("original_query") or ""), intent)
    expected_mount = _explicit_query_mount(str(intent.get("original_query") or ""), intent)
    signals = _query_variant_signals(intent)
    if signals and _result_matches_exact_variant_scope(top_result, intent, expected_family, expected_mount, signals):
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


def _result_is_summilux_35_context(result: Mapping[str, Any]) -> bool:
    if str(_result_field(result, "category") or "") != "Lens":
        return False
    candidate_family = (
        _result_field(result, "model_canonical")
        or _result_field(result, "model_raw")
        or _result_field(result, "label")
        or result.get("title")
    )
    if _family_root(candidate_family) != "Summilux":
        return False
    focal = str(_result_field(result, "focal_length") or "").strip()
    if focal != "35":
        return False
    mount = str(_result_field(result, "mount") or "").strip()
    if mount and mount not in {"M", "Unknown"}:
        return False
    return True


def _result_is_summicron_50_family_context(result: Mapping[str, Any]) -> bool:
    if str(_result_field(result, "category") or "") != "Lens":
        return False
    candidate_family = (
        _result_field(result, "model_canonical")
        or _result_field(result, "model_raw")
        or _result_field(result, "label")
        or result.get("title")
    )
    if _family_root(candidate_family) != "Summicron":
        return False
    focal = str(_result_field(result, "focal_length") or "").strip()
    if focal != "50":
        return False
    return True


def _result_is_summicron_50_context(result: Mapping[str, Any]) -> bool:
    if not _result_is_summicron_50_family_context(result):
        return False
    mount = str(_result_field(result, "mount") or "").strip()
    if mount and mount not in {"M", "Unknown"}:
        return False
    return True


def _result_has_summicron_50_dr_signal(result: Mapping[str, Any]) -> bool:
    if not _result_is_summicron_50_context(result):
        return False
    text = f" {_result_text_blob(result)} "
    return any(pattern in text for pattern in (" dr ", " dual range ", " dual-range ", " dualrange "))


def _result_has_summicron_50_rigid_signal(result: Mapping[str, Any]) -> bool:
    if not _result_is_summicron_50_context(result):
        return False
    return _result_matches_signal(result, {"kind": "variant", "value": "Rigid"})


def _result_has_summicron_50_collapsible_signal(result: Mapping[str, Any]) -> bool:
    if not _result_is_summicron_50_context(result):
        return False
    return _result_matches_signal(result, {"kind": "variant", "value": "Collapsible"})


def _result_has_summicron_50_apo_signal(result: Mapping[str, Any]) -> bool:
    candidate_family = (
        _result_field(result, "model_canonical")
        or _result_field(result, "model_raw")
        or _result_field(result, "label")
        or result.get("title")
    )
    if _family_root(candidate_family) == "APO-Summicron":
        return True
    text = f" {_result_text_blob(result)} "
    return " apo " in text


def _result_has_summicron_50_ltm_signal(result: Mapping[str, Any]) -> bool:
    text = f" {_result_text_blob(result)} "
    return any(pattern in text for pattern in (" ltm ", " m39 ", " screw mount "))


def _result_has_summicron_50_m_side_signal(result: Mapping[str, Any]) -> bool:
    if not _result_is_summicron_50_family_context(result):
        return False
    row_mount = str(_result_field(result, "mount") or "").strip()
    if row_mount == "M":
        return True
    text = f" {_result_text_blob(result)} "
    return any(pattern in text for pattern in (" leica m 50", " m 50/2 ", " m 50mm ", " m50/2 "))


def _result_has_summicron_50_l_side_signal(result: Mapping[str, Any]) -> bool:
    if not _result_is_summicron_50_family_context(result):
        return False
    row_mount = str(_result_field(result, "mount") or "").strip()
    if row_mount == "L":
        return True
    if _result_has_summicron_50_ltm_signal(result):
        return True
    text = f" {_result_text_blob(result)} "
    return any(pattern in text for pattern in (" leica l 50", " l 50/2 ", " l 50mm ", " l50/2 "))


def _result_has_fle_signal(result: Mapping[str, Any]) -> bool:
    text = f" {_result_text_blob(result)} "
    return _result_has_fle2_signal(result) or any(pattern in text for pattern in (" fle ", " floating element "))


def _result_has_fle2_signal(result: Mapping[str, Any]) -> bool:
    text = f" {_result_text_blob(result)} "
    return any(pattern in text for pattern in (" fle ii ", " fle2 ", " fle 2 ", " close focus ", " close-focus "))


def _result_has_fle1_only_signal(result: Mapping[str, Any]) -> bool:
    return _result_has_fle_signal(result) and not _result_has_fle2_signal(result)


def _result_has_summilux_35_aa_signal(result: Mapping[str, Any]) -> bool:
    if not _result_is_summilux_35_context(result):
        return False
    if _result_has_fle_signal(result):
        return False
    text = f" {_result_text_blob(result)} "
    return any(pattern in text for pattern in (" aa ", " double aspherical ", " aspherical ", "2매"))


def _result_has_summilux_35_aa_third_gen_2mae_signal(result: Mapping[str, Any]) -> bool:
    if not _result_has_summilux_35_aa_signal(result):
        return False
    text = f" {_result_text_blob(result)} "
    return "2매" in text and (" 3세대 " in text or " v3 " in text or " version 3 " in text)


def _result_has_summilux_35_second_or_pre_asph_signal(result: Mapping[str, Any]) -> bool:
    if not _result_is_summilux_35_context(result):
        return False
    if (
        _result_has_fle_signal(result)
        or _result_has_summilux_35_aa_signal(result)
        or _result_has_steel_rim_signal(result)
        or _result_has_reissue_signal(result)
    ):
        return False
    text = f" {_result_text_blob(result)} "
    return any(pattern in text for pattern in (" 2nd ", " second generation ", " 2세대 ", " v2 ", " version 2 ", " pre-asph ", " pre asph ", " preasph "))


def _result_has_summilux_35_asph_family_signal(result: Mapping[str, Any]) -> bool:
    if not _result_is_summilux_35_context(result):
        return False
    if (
        _result_has_fle_signal(result)
        or _result_has_summilux_35_aa_signal(result)
        or _result_has_steel_rim_signal(result)
        or _result_has_reissue_signal(result)
    ):
        return False
    text = f" {_result_text_blob(result)} "
    return " asph " in text


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
    if not signals:
        family = str(intent.get("model_family") or "").strip()
        mount = str(intent.get("mount") or "").strip()
        focal = str(intent.get("focal_length") or "").strip()
        if family == "APO-Summicron-SL" and mount == "SL" and focal in {"35", "50", "75", "90"}:
            signals.append({"kind": "variant", "value": "ASPH"})
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


def _is_explicit_summicron_50_dr_query(intent: Mapping[str, Any]) -> bool:
    if _family_root(intent.get("model_family") or "") != "Summicron":
        return False
    if str(intent.get("focal_length") or "").strip() != "50":
        return False
    variant_values = _query_variant_values(intent)
    return "DUAL RANGE" in variant_values


def _is_explicit_summicron_50_hood_query(intent: Mapping[str, Any]) -> bool:
    if _normalize_text(intent.get("accessory_intent")) != "hood":
        return False
    if _family_root(intent.get("model_family") or "") != "Summicron":
        return False
    if str(intent.get("focal_length") or "").strip() != "50":
        return False
    return True


def _query_variant_values(intent: Mapping[str, Any]) -> set[str]:
    return {
        str(signal.get("value") or "").strip().upper()
        for signal in _query_variant_signals(intent)
        if str(signal.get("kind") or "") == "variant" and str(signal.get("value") or "").strip()
    }


def _is_explicit_summilux_35_fle_query(intent: Mapping[str, Any]) -> bool:
    if _family_root(intent.get("model_family") or "") != "Summilux":
        return False
    if str(intent.get("focal_length") or "").strip() != "35":
        return False
    variant_values = _query_variant_values(intent)
    return "FLE" in variant_values and "FLE2" not in variant_values


def _is_explicit_summilux_35_fle2_query(intent: Mapping[str, Any]) -> bool:
    if _family_root(intent.get("model_family") or "") != "Summilux":
        return False
    if str(intent.get("focal_length") or "").strip() != "35":
        return False
    variant_values = {
        str(signal.get("value") or "").strip().upper()
        for signal in _query_variant_signals(intent)
        if str(signal.get("kind") or "") == "variant" and str(signal.get("value") or "").strip()
    }
    return "FLE2" in variant_values


def _is_mount_unspecified_summicron_50_rigid_query(intent: Mapping[str, Any], expected_mount: str | None) -> bool:
    if expected_mount is not None:
        return False
    if _family_root(intent.get("model_family") or "") != "Summicron":
        return False
    if str(intent.get("focal_length") or "").strip() != "50":
        return False
    variant_values = {
        str(signal.get("value") or "").strip().upper()
        for signal in _query_variant_signals(intent)
        if str(signal.get("kind") or "") == "variant" and str(signal.get("value") or "").strip()
    }
    return "RIGID" in variant_values


def _is_broad_summilux_m_35_query(intent: Mapping[str, Any], expected_mount: str | None) -> bool:
    if _family_root(intent.get("model_family") or "") != "Summilux":
        return False
    if str(intent.get("focal_length") or "").strip() != "35":
        return False
    mount = str(expected_mount or intent.get("mount") or "").strip()
    if mount != "M":
        return False
    if _query_variant_values(intent):
        return False
    if str(intent.get("generation") or "").strip():
        return False
    if str(intent.get("filter_size") or "").strip():
        return False
    if str(intent.get("optical_formula") or "").strip():
        return False
    return True


def _summilux_35_variant_family_key(result: Mapping[str, Any]) -> str | None:
    if not _result_is_summilux_35_context(result):
        return None
    if _result_has_summilux_35_aa_signal(result):
        return "aa"
    if _result_has_steel_rim_signal(result) or _result_has_reissue_signal(result):
        return "steel_rim_family"
    if _result_has_fle2_signal(result):
        return "fle2"
    if _result_has_fle1_only_signal(result):
        return "fle"
    if _result_has_summilux_35_asph_family_signal(result):
        return "asph"
    if _result_has_summilux_35_second_or_pre_asph_signal(result):
        return "second_or_pre_asph"
    return None


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
        "fle2": ["fle2", "fle ii", "fle 2", "close focus", "close-focus"],
        "dual range": [" dr ", " dual range ", " dual-range ", " dualrange "],
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


def _result_has_steel_rim_signal(result: Mapping[str, Any]) -> bool:
    text = f" {_result_text_blob(result)} "
    return bool(re.search(r"\bsteel\s+rim\b|\bsteel-rim\b|스틸림", text))


def _result_has_reissue_signal(result: Mapping[str, Any]) -> bool:
    text = f" {_result_text_blob(result)} "
    return bool(re.search(r"\breissue\b|복각", text))


def _tri_elmar_mount_compatible_from_text(result: Mapping[str, Any], expected_mount: str | None, expected_family: str) -> bool:
    if expected_mount != "M" or _family_root(expected_family) != "Tri-Elmar":
        return False
    text = _result_text_blob(result)
    return "tri-elmar-m" in text or " tri-elmar m " in f" {text} "


def _tri_elmar_range_matches_query(intent: Mapping[str, Any], result: Mapping[str, Any]) -> bool:
    if _family_root(intent.get("model_family") or "") != "Tri-Elmar":
        return False
    expected_focal = str(intent.get("focal_length") or "")
    if expected_focal not in {"16-18-21", "28-35-50"}:
        return False
    result_focal = str(_result_field(result, "focal_length") or "")
    if result_focal == expected_focal:
        return True
    text = f" {_result_text_blob(result)} "
    return expected_focal in text or expected_focal.replace("-", " ") in text


def _result_matches_signal(result: Mapping[str, Any], signal: Mapping[str, str]) -> bool:
    text = f" {_result_text_blob(result)} "
    value = str(signal.get("value") or "")
    kind = str(signal.get("kind") or "")
    if kind == "variant" and _normalize_text(value) == "aa" and _result_has_summilux_35_aa_signal(result):
        return True
    if kind == "variant" and _normalize_text(value) == "steel rim":
        return _result_has_steel_rim_signal(result) and not _result_has_reissue_signal(result)
    if kind == "variant" and _normalize_text(value) == "reissue":
        return _result_has_reissue_signal(result)
    if kind == "variant" and _normalize_text(value) == "dual range":
        return _result_has_summicron_50_dr_signal(result)
    if kind == "variant" and _normalize_text(value) == "fle2":
        return _result_has_fle2_signal(result)
    if kind == "variant" and _normalize_text(value) == "fle":
        return _result_has_fle_signal(result)
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
    if expected_mount:
        result_mount = str(_result_field(result, "mount") or "")
        if result_mount != expected_mount and not (
            result_mount in {"", "Unknown"} and _tri_elmar_mount_compatible_from_text(result, expected_mount, expected_family)
        ):
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
    variant_values = {
        str(signal.get("value") or "").strip().upper()
        for signal in signals
        if str(signal.get("kind") or "") == "variant" and str(signal.get("value") or "").strip()
    }
    if (
        _family_root(expected_family or intent.get("model_family") or "") == "Summilux"
        and str(intent.get("focal_length") or "") == "35"
        and expected_mount in {None, "M"}
        and "ASPH" in variant_values
        and "AA" not in variant_values
        and _result_has_summilux_35_aa_signal(result)
    ):
        return False
    if (
        _family_root(expected_family or intent.get("model_family") or "") == "Summilux"
        and str(intent.get("focal_length") or "") == "35"
        and expected_mount in {None, "M"}
        and "ASPH" in variant_values
        and "FLE" not in variant_values
        and _result_has_fle_signal(result)
    ):
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
    if expected_mount:
        result_mount = str(_result_field(result, "mount") or "")
        if result_mount != expected_mount and not (
            result_mount in {"", "Unknown"} and _tri_elmar_mount_compatible_from_text(result, expected_mount, expected_family)
        ):
            return False
    expected_root = _family_root(expected_family or intent.get("model_family") or "")
    candidate_text = _normalize_text(
        _result_field(result, "model_canonical")
        or _result_field(result, "model_raw")
        or _result_field(result, "label")
        or result.get("title")
    )
    result_root = _family_root(candidate_text)
    if expected_root and result_root and expected_root != result_root:
        return False
    if expected_root and not result_root and expected_root.lower() not in candidate_text:
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
    "half case",
    "box",
    "filter",
    "finder",
    "adapter",
    "strap",
    "pouch",
    "holster",
    "grip",
    "thumb rest",
    "battery",
    "charger",
    "cover",
    "protector",
    "handgrip",
    "thumb support",
    "base plate",
    "홀스터",
    "케이스",
    "하프케이스",
    "하프 케이스",
    "파우치",
    "스트랩",
    "배터리",
    "충전기",
    "그립",
    "핸드그립",
    "프로텍터",
    "커버",
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


def _contains_normalized_word(text: str, needle: str) -> bool:
    haystack = f" {_normalize_text(text)} "
    target = _normalize_text(needle)
    if not target:
        return False
    return f" {target} " in haystack


def _body_variant_tokens(body_intent: str) -> set[str]:
    body = _normalize_text(body_intent)
    tokens: set[str] = set()
    if body == "m6":
        tokens.update({"ttl"})
    if body in {"m9", "m10", "m11"}:
        base = body
        tokens.update(
            {
                f"{base}-p",
                f"{base} p",
                f"{base}-r",
                f"{base} r",
                f"{base}-d",
                f"{base} d",
                "monochrom",
                "reporter",
                "safari",
                "leitz wetzlar",
                "edition",
                "limited edition",
            }
        )
    return tokens


def _body_query_has_explicit_bundle_signal(query: str, intent: Mapping[str, Any]) -> bool:
    if not intent.get("body_intent"):
        return False
    normalized = f" {_normalize_text(query)} "
    if not normalized.strip():
        return False
    if any(pattern in normalized for pattern in (" lens kit ", " body lens kit ", " bundle ", " body+lens ")):
        return True
    if " body + lens " in normalized or " body+lens " in normalized:
        return True
    if " kit " in normalized:
        return True
    lens_or_accessory_context = bool(
        re.search(
            r"\b(lens|accessories|accessory|hood|adapter|summicron|summilux|noctilux|elmarit|elmar|summaron|apo-summicron)\b",
            normalized,
        )
    )
    if " with " in normalized and lens_or_accessory_context:
        return True
    if " set " in normalized and lens_or_accessory_context:
        return True
    return False


def _body_query_has_explicit_accessory_signal(query: str, intent: Mapping[str, Any]) -> bool:
    if not intent.get("body_intent"):
        return False
    normalized = f" {_normalize_text(query)} "
    if not normalized.strip():
        return False
    accessory_patterns = (
        " screen protector ",
        " protector ",
        " half case ",
        " handgrip ",
        " thumb grip ",
        " thumb support ",
        " grip ",
        " holster ",
        " strap ",
        " cover ",
        " charger ",
        " battery ",
        " case ",
    )
    return any(pattern in normalized for pattern in accessory_patterns)


def _body_query_has_monochrom_signal(query: str, intent: Mapping[str, Any]) -> bool:
    if not intent.get("body_intent"):
        return False
    normalized = f" {_normalize_text(query)} "
    if not normalized.strip():
        return False
    return " monochrom " in normalized or " m10m " in normalized


def _result_has_monochrom_signal(result: Mapping[str, Any]) -> bool:
    text = _result_text_blob(result)
    if " monochrom " in text or " m10m " in text:
        return True
    result_variants = {_normalize_text(item) for item in _as_list(_result_field(result, "variant")) if item}
    return "monochrom" in result_variants or "m10m" in result_variants


def _body_price_variant_boundary(
    result: Mapping[str, Any],
    query: str,
    intent: Mapping[str, Any],
) -> bool:
    body_intent = str(intent.get("body_intent") or "").strip()
    if not body_intent:
        return False
    query_text = f" {_normalize_text(query)} "
    result_text = f" {_result_text_blob(result)} "
    result_variants = {_normalize_text(item) for item in _as_list(_result_field(result, "variant")) if item}

    for token in _body_variant_tokens(body_intent):
        normalized = _normalize_text(token)
        if not normalized:
            continue
        if normalized in result_variants:
            if f" {normalized} " not in query_text:
                return True
            continue
        if f" {normalized} " in result_text and f" {normalized} " not in query_text:
            return True
    return False


def _summicron_50_dr_ranking_bucket(
    result: Mapping[str, Any],
    intent: Mapping[str, Any],
    expected_family: str,
    expected_mount: str | None,
    signals: list[dict[str, str]],
) -> int:
    row_mount = str(_result_field(result, "mount") or "").strip()
    row_boundary_conflict = (
        _result_family_conflict(expected_family, result)
        or _result_mount_conflict(expected_mount, result)
        or _result_category_conflict(_parsed_category(intent), result)
        or _result_variant_conflict(intent, result)
        or _result_classification_conflict(result)
    )
    dr_signal = _result_has_summicron_50_dr_signal(result)
    rigid_signal = _result_has_summicron_50_rigid_signal(result)
    collapsible_signal = _result_has_summicron_50_collapsible_signal(result)
    apo_signal = _result_has_summicron_50_apo_signal(result)
    ltm_signal = _result_has_summicron_50_ltm_signal(result)
    exact_variant = _result_matches_exact_variant_scope(result, intent, expected_family, expected_mount, signals)
    exact_base = _result_matches_base_model_scope(result, intent, expected_family, expected_mount)

    if exact_variant and dr_signal and row_mount in {"", "Unknown", "M"} and not ltm_signal:
        return 0
    if dr_signal and row_mount in {"", "Unknown", "M"} and not ltm_signal and not row_boundary_conflict:
        return 1
    if exact_base and row_mount in {"", "Unknown", "M"} and not dr_signal and not rigid_signal and not apo_signal and not collapsible_signal and not ltm_signal:
        return 2
    if exact_base and row_mount in {"", "Unknown", "M"} and not ltm_signal:
        return 3
    if ltm_signal or row_mount in {"L", "R", "SL"}:
        return 5
    if row_boundary_conflict or apo_signal or rigid_signal or collapsible_signal:
        return 4
    return 6


def _is_explicit_generic_lens_query(query: str, intent: Mapping[str, Any]) -> bool:
    if intent.get("accessory_intent") or intent.get("body_intent"):
        return False
    normalized_query = f" {_normalize_text(query)} "
    if " lens " not in normalized_query:
        return False
    if re.search(r"\b(?:hood|cap|filter|adapter|finder|case|battery|charger|strap)\b", normalized_query):
        return False
    return True


def _generic_lens_query_ranking_bucket(result: Mapping[str, Any], intent: Mapping[str, Any]) -> tuple[int, int]:
    category = str(_result_field(result, "category") or "").strip()
    title = _normalize_text(result.get("title") or "")
    row_focal = str(_result_field(result, "focal_length") or "").strip()
    query_focal = str(intent.get("focal_length") or "").strip()
    accessory_like = category == "Accessory" or _contains_keyword(title, PRICE_ACCESSORY_KEYWORDS)
    focal_bucket = 0 if (not query_focal or row_focal == query_focal) else 1

    if category == "Lens" and not accessory_like:
        return (0, focal_bucket)
    if category == "Lens":
        return (1, focal_bucket)
    if accessory_like:
        return (3, focal_bucket)
    return (2, focal_bucket)


def _hood_query_ranking_bucket(
    result: Mapping[str, Any],
    intent: Mapping[str, Any],
    expected_family: str,
) -> tuple[int, int, int, int]:
    category = str(_result_field(result, "category") or "").strip()
    accessory_type = _normalize_text((result.get("final_output") or {}).get("accessory_type"))
    text = _result_text_blob(result)
    accessory_code = _normalize_text(intent.get("accessory_code"))
    family_root = _family_root(expected_family)
    focal = _normalize_text(intent.get("focal_length"))
    aperture = _normalize_text(intent.get("aperture"))

    is_accessory = category == "Accessory"
    has_hood_text = bool(re.search(r"\bhood\b|후드", text))
    exact_code_hit = bool(accessory_code and _contains_normalized_word(text, accessory_code))
    family_hit = bool(family_root and family_root.lower() in text)
    focal_hit = bool(focal and _contains_normalized_word(text, focal))
    aperture_hit = bool(aperture and (_contains_normalized_word(text, aperture) or _contains_normalized_word(text, f"f{aperture}")))
    compatibility_hits = int(family_hit) + int(focal_hit) + int(aperture_hit)

    if exact_code_hit and is_accessory and (accessory_type == "hood" or has_hood_text):
        return (0, 0, -compatibility_hits, 0)
    if is_accessory and (accessory_type == "hood" or has_hood_text) and compatibility_hits:
        return (1, 0, -compatibility_hits, 0)
    if is_accessory and (accessory_type == "hood" or has_hood_text):
        return (2, 0, -compatibility_hits, 0)
    if exact_code_hit and has_hood_text:
        return (3, 0, -compatibility_hits, 0)
    if has_hood_text and compatibility_hits:
        return (4, 0, -compatibility_hits, 0)
    if has_hood_text:
        return (5, 0, -compatibility_hits, 0)
    if is_accessory:
        return (6, 0, -compatibility_hits, 0)
    if category == "Lens":
        return (8, 0, -compatibility_hits, 0)
    return (7, 0, -compatibility_hits, 0)


def _summilux_35_fle_ranking_bucket(
    result: Mapping[str, Any],
    intent: Mapping[str, Any],
    expected_family: str,
    expected_mount: str | None,
    signals: list[dict[str, str]],
) -> int:
    row_boundary_conflict = (
        _result_family_conflict(expected_family, result)
        or _result_mount_conflict(expected_mount, result)
        or _result_category_conflict(_parsed_category(intent), result)
        or _result_classification_conflict(result)
    )
    exact_variant = _result_matches_exact_variant_scope(result, intent, expected_family, expected_mount, signals)
    exact_base = _result_matches_base_model_scope(result, intent, expected_family, expected_mount)
    fle1_signal = _result_has_fle1_only_signal(result)
    fle2_signal = _result_has_fle2_signal(result)
    aa_signal = _result_has_summilux_35_aa_signal(result)
    steel_rim_signal = _result_has_steel_rim_signal(result)
    reissue_signal = _result_has_reissue_signal(result)

    if exact_variant and fle1_signal:
        return 0
    if fle1_signal and not row_boundary_conflict:
        return 1
    if exact_variant and fle2_signal:
        return 2
    if fle2_signal and not row_boundary_conflict:
        return 3
    if exact_base and not fle1_signal and not fle2_signal and not aa_signal and not steel_rim_signal and not reissue_signal:
        return 4
    if aa_signal or steel_rim_signal or reissue_signal:
        return 5
    if row_boundary_conflict:
        return 6
    return 7


def _summilux_35_fle2_ranking_bucket(
    result: Mapping[str, Any],
    intent: Mapping[str, Any],
    expected_family: str,
    expected_mount: str | None,
    signals: list[dict[str, str]],
) -> int:
    row_boundary_conflict = (
        _result_family_conflict(expected_family, result)
        or _result_mount_conflict(expected_mount, result)
        or _result_category_conflict(_parsed_category(intent), result)
        or _result_classification_conflict(result)
    )
    exact_variant = _result_matches_exact_variant_scope(result, intent, expected_family, expected_mount, signals)
    exact_base = _result_matches_base_model_scope(result, intent, expected_family, expected_mount)
    fle1_signal = _result_has_fle1_only_signal(result)
    fle2_signal = _result_has_fle2_signal(result)
    aa_signal = _result_has_summilux_35_aa_signal(result)
    steel_rim_signal = _result_has_steel_rim_signal(result)
    reissue_signal = _result_has_reissue_signal(result)

    if exact_variant and fle2_signal:
        return 0
    if fle2_signal and not row_boundary_conflict:
        return 1
    if exact_variant and fle1_signal:
        return 2
    if fle1_signal and not row_boundary_conflict:
        return 3
    if aa_signal or steel_rim_signal or reissue_signal:
        return 5
    if exact_base and not fle1_signal and not fle2_signal:
        return 4
    if row_boundary_conflict:
        return 6
    return 7


def _rerank_results_for_query_context(query: str, response: Mapping[str, Any], sort: str) -> list[dict[str, Any]]:
    results = list(response.get("results") or [])
    if sort != "relevance" or not results:
        return results
    intent = response.get("intent") or {}
    if _is_explicit_summicron_50_dr_query(intent):
        expected_family = _explicit_query_family(query, intent)
        expected_mount = _explicit_query_mount(query, intent)
        signals = _query_variant_signals(intent)
        ranked = sorted(
            enumerate(results),
            key=lambda pair: (
                _summicron_50_dr_ranking_bucket(pair[1], intent, expected_family, expected_mount, signals),
                pair[0],
            ),
        )
        return [result for _, result in ranked]
    if _is_explicit_summilux_35_fle_query(intent):
        expected_family = _explicit_query_family(query, intent)
        expected_mount = _explicit_query_mount(query, intent)
        signals = _query_variant_signals(intent)
        ranked = sorted(
            enumerate(results),
            key=lambda pair: (
                _summilux_35_fle_ranking_bucket(pair[1], intent, expected_family, expected_mount, signals),
                pair[0],
            ),
        )
        return [result for _, result in ranked]
    if _is_explicit_summilux_35_fle2_query(intent):
        expected_family = _explicit_query_family(query, intent)
        expected_mount = _explicit_query_mount(query, intent)
        signals = _query_variant_signals(intent)
        ranked = sorted(
            enumerate(results),
            key=lambda pair: (
                _summilux_35_fle2_ranking_bucket(pair[1], intent, expected_family, expected_mount, signals),
                pair[0],
            ),
        )
        return [result for _, result in ranked]
    if str(intent.get("accessory_intent") or "") == "hood":
        expected_family = _explicit_query_family(query, intent)
        ranked = sorted(
            enumerate(results),
            key=lambda pair: (
                *_hood_query_ranking_bucket(pair[1], intent, expected_family),
                pair[0],
            ),
        )
        return [result for _, result in ranked]
    if _is_explicit_generic_lens_query(query, intent):
        ranked = sorted(
            enumerate(results),
            key=lambda pair: (
                *_generic_lens_query_ranking_bucket(pair[1], intent),
                pair[0],
            ),
        )
        return [result for _, result in ranked]
    return results


def _build_summicron_50_hood_supplement_query(intent: Mapping[str, Any]) -> str:
    mount = _normalize_text(intent.get("mount"))
    if mount == "m":
        return "Leica M 50mm hood"
    return "Leica 50mm hood"


def _hood_like_supplement_results(results: list[Mapping[str, Any]]) -> list[dict[str, Any]]:
    filtered: list[dict[str, Any]] = []
    for result in results:
        category = str(_result_field(result, "category") or "").strip()
        accessory_type = _normalize_text((result.get("final_output") or {}).get("accessory_type"))
        text = _result_text_blob(result)
        if category == "Accessory" and (accessory_type == "hood" or re.search(r"\bhood\b|후드", text)):
            filtered.append(dict(result))
            continue
        if re.search(r"\bhood\b|후드|\bshade\b|lens shade|vented hood|round hood", text):
            filtered.append(dict(result))
    return filtered


def _merge_unique_results(
    base_results: list[Mapping[str, Any]],
    supplemental_results: list[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    merged: list[dict[str, Any]] = [dict(result) for result in base_results]
    seen = {_result_signature(result) for result in base_results}
    for result in supplemental_results:
        signature = _result_signature(result)
        if signature in seen:
            continue
        merged.append(dict(result))
        seen.add(signature)
    return merged


def _promote_expanded_results_for_query_context(
    query: str,
    response: dict[str, Any],
    evidence_response: Mapping[str, Any] | None,
    *,
    sort: str,
    limit: int,
    offset: int,
) -> None:
    if sort != "relevance" or not evidence_response:
        return
    intent = response.get("intent") or {}
    if not _is_explicit_summicron_50_dr_query(intent):
        return
    expanded_results = list(evidence_response.get("results") or [])
    if not expanded_results:
        return
    promoted_results = expanded_results[offset : offset + limit]
    if not promoted_results:
        return
    response["results"] = promoted_results
    response["result_count"] = len(promoted_results)


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
        "mixed_fle_generation": "FLE and FLE II / FLE2 listings are mixed, so exact price stays locked.",
        "mixed_rigid_mounts": "M-side and LTM/M39-side rigid listings are mixed, so exact price stays locked.",
        "mixed_broad_summilux_35_variants": "Summilux-M 35 broad results mix materially different variants, so exact price stays locked.",
        "outlier_contaminated": "Outlier prices are contaminating this reference pool.",
        "locked_boundary_conflict": "Price summary is locked until boundary conflicts are resolved.",
        "locked_weak_only": "Price summary is locked until stronger visible results appear.",
    }
    return mapping.get(reason, reason.replace("_", " ").capitalize())


def _humanize_quality_state(state: str) -> str:
    mapping = {
        "clean_exact_variant_band": "Clean exact variant price evidence",
        "clean_exact_base_model_band": "Clean same-model price evidence",
        "clean_broader_reference_band": "Clean reference price evidence",
        "insufficient_priced_evidence": "Exact variant price data is limited",
        "too_noisy_broader_reference": "Broader family reference is too noisy",
        "too_wide_price_band": "Reference prices are too spread out to show safely",
        "outlier_contaminated": "Outlier contamination detected",
        "accessory_contaminated": "Accessory contamination detected",
        "third_party_contaminated": "Third-party contamination detected",
        "wrong_model_contaminated": "Wrong-model contamination detected",
        "mixed_fle_generation_locked": "Mixed FLE / FLE2 exact evidence",
        "mixed_rigid_mounts_locked": "Mixed M / LTM-M39 rigid exact evidence",
        "mixed_summilux_35_variants_locked": "Mixed Summilux-M 35 exact evidence",
        "locked_boundary_conflict": "Price summary locked by boundary conflict",
        "locked_weak_only": "Price summary locked by weak fallback",
    }
    return mapping.get(state, state.replace("_", " ").capitalize())


def _humanize_result_role(label: str) -> str:
    mapping = {
        "Exact variant": "Exact variant",
        "Exact base model": "Same base model",
        "Broader family": "Broader reference",
        "Third-party top result": "Third-party or adjacent result",
        "Boundary conflict": "Boundary conflict",
        "Query incompatible": "Not compatible with this query",
    }
    return mapping.get(label, label or "Visible result")


def _humanize_evidence_pool(pool_name: str) -> str:
    mapping = {
        "exact_variant_pool": "Used for exact price",
        "exact_base_model_pool": "Same base model evidence",
        "broader_family_pool": "Broader reference only",
        "excluded_pool": "Not used for price",
        "visible_only": "Not used for price",
    }
    return mapping.get(pool_name, pool_name.replace("_", " ").capitalize())


def _humanize_excluded_reason(reason: str) -> str:
    mapping = {
        "accessory": "Accessory, not camera/lens",
        "repair_or_parts": "Accessory, not camera/lens",
        "deposit_or_rental": "Deposit or rental listing",
        "third_party": "Third-party item",
        "sold_status_incompatible": "Current sale status is not used for this price view",
        "category_mismatch": "Not compatible with this query",
        "classification_conflict": "Classification needs review",
        "wrong_model": "Different model",
        "mount_mismatch": "Wrong mount",
        "focal_mismatch": "Wrong focal length",
        "aperture_mismatch": "Wrong aperture",
        "variant_mismatch": "Wrong variant",
        "variant_boundary": "Variant boundary",
        "body_lens_boundary_conflict": "Not compatible with this query",
        "duplicate": "Duplicate listing",
        "outlier": "Price outlier",
        "source_gap": "Current source coverage is not enough yet",
    }
    return mapping.get(reason, _humanize_policy_reason(reason))


def _build_price_usage_label(
    used_for_price: bool,
    evidence_pool: str,
    excluded_reasons: list[str],
) -> str:
    if used_for_price:
        if evidence_pool == "exact_variant_pool":
            return "Used for exact price"
        if evidence_pool == "exact_base_model_pool":
            return "Used for same base model price"
        return "Used as broader reference"
    if excluded_reasons:
        return f"Not used — {excluded_reasons[0]}"
    if evidence_pool == "exact_variant_pool":
        return "Exact match visible, but not enough to unlock price yet"
    if evidence_pool == "exact_base_model_pool":
        return "Same base model result is visible, but not used as exact price"
    if evidence_pool == "broader_family_pool":
        return "Shown as broader reference only"
    if evidence_pool == "visible_only":
        return "Not used — not compatible with this query"
    return "Visible, but not used for pricing"


def _humanize_unlock_requirement(requirement: str) -> str:
    mapping = {
        "Need 2+ exact variant priced listings.": "Price stays locked until at least 2 exact variant listings have reliable prices.",
        "Need exact or strong compatible visible Leica results.": "Price stays locked until the visible search results strongly match this Leica item.",
        "Need no third-party contamination in the selected price pool.": "Price stays locked because the selected evidence still includes third-party or adjacent items.",
        "Need cleaned price band within an acceptable width.": "Price stays locked until the remaining price range is narrow enough to show safely.",
        "Need no accessory contamination in the selected price pool.": "Price stays locked because accessory or part listings are still mixed into the evidence.",
        "Need no wrong-model contamination in the selected price pool.": "Price stays locked because different models are still mixed into the evidence.",
        "Need no mixed FLE and FLE2 listings in the exact price pool.": "Price stays locked because FLE and FLE II / FLE2 evidence are still mixed together.",
        "Need no mixed Summilux-M 35 variant families in the exact price pool.": "Price stays locked because broad Summilux-M 35 evidence still mixes materially different variants.",
        "Need 1+ sold confirmed or sold likely record.": "Price stays limited until at least one sold-like reference is available.",
    }
    if requirement in mapping:
        return mapping[requirement]
    if requirement.startswith("Need "):
        return f"Price stays locked until {requirement[5:].rstrip('.').lower()}."
    return requirement


def _summarize_evidence_pool_counts(
    *,
    variant_label: str | None,
    exact_variant_count: int,
    exact_base_count: int,
    broader_count: int,
    excluded_count: int,
) -> str:
    pieces: list[str] = []
    if variant_label:
        pieces.append(f"{exact_variant_count} exact {variant_label} listing{'s' if exact_variant_count != 1 else ''}")
    pieces.append(f"{exact_base_count} same-base listing{'s' if exact_base_count != 1 else ''}")
    if broader_count:
        pieces.append(f"{broader_count} broader reference{'s' if broader_count != 1 else ''}")
    sentence = "Price evidence found: " + ", ".join(pieces) + "."
    sentence += f" Excluded from price: {excluded_count} listing{'s' if excluded_count != 1 else ''}."
    return sentence


def _build_price_status_message(
    *,
    expected_category: str,
    price_summary_allowed: bool,
    price_scope: str,
    broader_reference_allowed: bool,
    market_entry_allowed: bool,
) -> str:
    if expected_category == "Body":
        if price_summary_allowed:
            return "Body market summary is available."
        if broader_reference_allowed:
            return "Reference price only."
        return "Price summary is locked."
    if price_summary_allowed:
        if price_scope == "exact_variant":
            return "Exact price is available."
        if price_scope == "exact_base_model":
            return "Same-model price is available."
    if broader_reference_allowed:
        return "Reference price only."
    if price_scope in {"insufficient_exact_data", "blocked_weak_only", "blocked_boundary_conflict"}:
        return "Price summary is locked."
    return "Exact variant price data is limited."


def _build_query_review_why(
    *,
    price_summary_allowed: bool,
    broader_reference_allowed: bool,
    display_match_state_message: str,
    display_price_band_quality_state: str,
    variant_signals: list[dict[str, str]],
    price_scope: str,
    search_confidence_state: str,
    third_party_top_domination_detected: bool,
    exact_variant_pool_count: int,
) -> str:
    if price_summary_allowed:
        return display_price_band_quality_state or "Clean exact price evidence is available."
    if variant_signals and (price_scope == "insufficient_exact_data" or exact_variant_pool_count <= 1):
        variant_name = " / ".join(str(signal.get("value") or "").strip() for signal in variant_signals if signal.get("value"))
        if variant_name:
            return f"{variant_name}-specific price evidence is not enough yet."
    if search_confidence_state == "weak_only_fallback" and third_party_top_domination_detected:
        return "Top visible results include third-party or adjacent items."
    if search_confidence_state == "weak_only_fallback":
        return "Results are visible, but not strong enough for model-level pricing."
    if broader_reference_allowed and price_scope == "broader_model_family":
        return "Only broader reference pricing is safe for this query right now."
    if broader_reference_allowed and price_scope == "exact_base_model":
        return "Same base model listings are visible, but exact variant pricing is still locked."
    if broader_reference_allowed:
        return display_match_state_message or "Reference prices are shown separately."
    return display_match_state_message or "Price summary is locked."


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
) -> str:
    if intent.get("body_intent"):
        parts = [str(intent.get("brand") or "").strip(), str(intent.get("body_intent") or "").strip(), "body"]
        return " ".join(part for part in parts if part)

    accessory_intent = str(intent.get("accessory_intent") or "").strip()
    if accessory_intent:
        brand = str(intent.get("brand") or "").strip()
        accessory_code = str(intent.get("accessory_code") or "").strip().upper()
        family = expected_family or str(intent.get("model_family") or "").strip()
        focal = str(intent.get("focal_length") or "").strip()
        aperture = str(intent.get("aperture") or _query_aperture_hint(query) or "").strip()
        parts: list[str] = [brand] if brand else []
        if accessory_code:
            parts.append(accessory_code)
        else:
            family_text = family.strip()
            if family_text and family_text.lower() != "lens":
                if expected_mount and expected_mount not in family_text:
                    family_text = f"{family_text}-{expected_mount}"
                if brand and brand.lower() in family_text.lower():
                    parts = []
                parts.append(family_text)
                if focal:
                    parts.append(focal)
            elif focal:
                parts.append(focal)
            if aperture:
                parts.append(f"f{aperture}")
        parts.append(accessory_intent)
        return " ".join(part for part in parts if part).strip() + " candidate"

    family = expected_family or str(intent.get("model_family") or "Lens")
    brand = str(intent.get("brand") or "").strip()
    focal = str(intent.get("focal_length") or "").strip()
    aperture = str(intent.get("aperture") or _query_aperture_hint(query) or "").strip()
    variant_values = [str(signal.get("value") or "").strip() for signal in variant_signals if signal.get("value")]
    family_text = family
    if family_text.lower() == "lens":
        mount_text = f"{expected_mount}-mount " if expected_mount else ""
        parts = [brand, f"{mount_text}lens".strip()]
        if focal:
            parts.append(f"{focal}")
        if aperture:
            parts.append(f"f{aperture}")
        if variant_values:
            parts.append(" / ".join(variant_values))
        return " ".join(part for part in parts if part).strip() + " candidate"
    if expected_mount and expected_mount not in family_text:
        family_text = f"{family_text}-{expected_mount}"
    if brand and brand.lower() not in family_text.lower():
        family_text = f"{brand} {family_text}"
    parts = [family_text]
    if focal:
        parts.append(f"{focal}")
    if aperture:
        parts.append(f"f{aperture}")
    if variant_values:
        parts.append(" / ".join(variant_values))
    return " ".join(part for part in parts if part).strip() + " candidate"


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
    variant_values = {
        str(signal.get("value") or "").strip().upper()
        for signal in variant_signals
        if str(signal.get("kind") or "") == "variant" and str(signal.get("value") or "").strip()
    }
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
        if intent.get("body_intent") and _body_price_variant_boundary(result, query, intent):
            reasons.append("variant_boundary")
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
        if (
            pool_scope == "exact_variant"
            and "AA" in variant_values
            and _result_has_summilux_35_aa_third_gen_2mae_signal(result)
            and sold_quality == "asking"
        ):
            reasons.append("outlier")

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
    variant_values = {
        str(signal.get("value") or "").strip().upper()
        for signal in variant_signals
        if str(signal.get("kind") or "") == "variant" and str(signal.get("value") or "").strip()
    }
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
    mixed_summilux_35_fle_generations_detected = bool(
        _family_root(expected_family or intent.get("model_family") or "") == "Summilux"
        and str(intent.get("focal_length") or "") == "35"
        and expected_mount in {None, "M"}
        and "FLE" in variant_values
        and "FLE2" not in variant_values
        and any(_result_has_fle1_only_signal(result) for result in exact_variant_results)
        and any(_result_has_fle2_signal(result) for result in exact_variant_results)
    )
    mixed_summicron_50_rigid_mounts_detected = bool(
        _is_mount_unspecified_summicron_50_rigid_query(intent, expected_mount)
        and any(_result_has_summicron_50_m_side_signal(result) for result in exact_variant_results)
        and any(_result_has_summicron_50_l_side_signal(result) for result in exact_variant_results)
    )

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
    mixed_broad_summilux_35_variants_detected = bool(
        _is_broad_summilux_m_35_query(intent, expected_mount)
        and len(
            {
                family_key
                for family_key in (_summilux_35_variant_family_key(result) for result in exact_base_model_priced)
                if family_key
            }
        )
        >= 2
    )
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
    explicit_body_bundle_query = _body_query_has_explicit_bundle_signal(query, intent)
    explicit_body_accessory_query = _body_query_has_explicit_accessory_signal(query, intent)
    monochrom_body_query = _body_query_has_monochrom_signal(query, intent)

    if monochrom_body_query:
        visible_exact_base_model_results = [
            result for result in visible_exact_base_model_results if _result_has_monochrom_signal(result)
        ]
        exact_base_model_results = [
            result for result in exact_base_model_results if _result_has_monochrom_signal(result)
        ]
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
        exact_base_model_priced = list(exact_base_model_pool["cleaned_results"])
        exact_base_model_strong_visible = _strong_results(visible_exact_base_model_results)
        exact_or_strong_visible_result_count = len(exact_variant_strong_visible if variant_signals else exact_base_model_strong_visible)

    if intent.get("body_intent"):
        if explicit_body_bundle_query:
            price_summary_block_reason.append("explicit_body_bundle_query")
        if explicit_body_accessory_query:
            price_summary_block_reason.append("explicit_body_accessory_query")
        if not market_entry_allowed:
            price_summary_block_reason.append("market_entry_not_allowed")
        if not exact_model_like_match:
            price_summary_block_reason.append("exact_model_like_match_missing")
        if not compatible_results:
            price_summary_block_reason.append("no_query_compatible_results")
        if not exact_base_model_priced:
            price_summary_block_reason.append("no_query_compatible_priced_results")
        if exact_base_model_priced and exact_base_model_pool["price_band_quality_state"] != "clean_exact_base_model_band":
            price_summary_block_reason.append(exact_base_model_pool["price_band_quality_state"])
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
            and not mixed_summilux_35_fle_generations_detected
            and not mixed_summicron_50_rigid_mounts_detected
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
            if mixed_summilux_35_fle_generations_detected:
                price_summary_block_reason.append("mixed_fle_generation")
            if mixed_summicron_50_rigid_mounts_detected:
                price_summary_block_reason.append("mixed_rigid_mounts")
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
        if mixed_broad_summilux_35_variants_detected:
            price_summary_block_reason.append("mixed_broad_summilux_35_variants")
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
    if mixed_summilux_35_fle_generations_detected and not price_summary_allowed:
        price_band_quality_state = "mixed_fle_generation_locked"
        price_band_quality_reason = ["mixed_fle_generation"]
    if mixed_summicron_50_rigid_mounts_detected and not price_summary_allowed:
        price_band_quality_state = "mixed_rigid_mounts_locked"
        price_band_quality_reason = ["mixed_rigid_mounts"]
    if mixed_broad_summilux_35_variants_detected and not price_summary_allowed:
        price_band_quality_state = "mixed_summilux_35_variants_locked"
        price_band_quality_reason = ["mixed_broad_summilux_35_variants"]

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
    if mixed_summilux_35_fle_generations_detected:
        unlock_requirements.append("Need no mixed FLE and FLE2 listings in the exact price pool.")
    if mixed_summicron_50_rigid_mounts_detected:
        unlock_requirements.append("Need no mixed M-side and LTM/M39-side rigid listings in the exact price pool.")
    if mixed_broad_summilux_35_variants_detected:
        unlock_requirements.append("Need no mixed Summilux-M 35 variant families in the exact price pool.")
    if boundary_conflict_detected:
        unlock_requirements.append("Need no boundary conflict between family, mount, and variant.")
    if price_summary_allowed:
        unlock_requirements = []

    exact_variant_signatures = {_result_signature(result) for result in exact_variant_pool["cleaned_results"]}
    exact_base_signatures = {_result_signature(result) for result in exact_base_model_pool["cleaned_results"]}
    broader_signatures = {_result_signature(result) for result in broader_family_pool["cleaned_results"]}

    excluded_reason_by_signature: dict[tuple[str, str, str, str], list[str]] = {}
    for pool in (exact_variant_pool, exact_base_model_pool, broader_family_pool):
        for excluded_item in pool.get("excluded", []) if isinstance(pool.get("excluded"), list) else []:
            result = excluded_item.get("result") or {}
            excluded_reason_by_signature[_result_signature(result)] = list(excluded_item.get("reasons") or [])

    def _build_visible_result_evidence(projection_results: list[Mapping[str, Any]]) -> list[dict[str, Any]]:
        evidence_items = []
        seen_projection_signatures: set[tuple[str, str, str, str]] = set()
        explicit_fle2_projection_query = "FLE2" in variant_values
        for index, result in enumerate(projection_results):
            signature = _result_signature(result)
            if signature in exact_variant_signatures:
                evidence_pool = "exact_variant_pool"
                used_for_price = price_summary_allowed and price_scope == "exact_variant"
                excluded_reasons = []
            elif signature in exact_base_signatures:
                evidence_pool = "exact_base_model_pool"
                used_for_price = price_summary_allowed and price_scope == "exact_base_model"
                excluded_reasons = []
            elif signature in broader_signatures:
                evidence_pool = "broader_family_pool"
                used_for_price = bool(broader_reference_allowed)
                excluded_reasons = []
            else:
                excluded_reasons = excluded_reason_by_signature.get(signature, [])
                evidence_pool = "excluded_pool" if excluded_reasons else "visible_only"
                used_for_price = False
            if excluded_reasons:
                used_for_price = False
                evidence_pool = "excluded_pool"

            row_boundary_conflict = (
                _result_family_conflict(expected_family, result)
                or _result_mount_conflict(expected_mount, result)
                or _result_category_conflict(expected_category, result)
                or _result_variant_conflict(intent, result)
                or _result_classification_conflict(result)
            )

            if row_boundary_conflict:
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

            if (
                explicit_fle2_projection_query
                and compatibility_label == "Exact base model"
                and _result_has_fle2_signal(result)
                and not excluded_reasons
            ):
                compatibility_label = "Exact variant"
                if evidence_pool == "exact_base_model_pool":
                    evidence_pool = "exact_variant_pool"
                    used_for_price = False

            if evidence_pool == "visible_only" and not excluded_reasons:
                if compatibility_label == "Exact variant":
                    evidence_pool = "exact_variant_pool"
                elif compatibility_label == "Exact base model":
                    evidence_pool = "exact_base_model_pool"
                elif compatibility_label == "Broader family":
                    evidence_pool = "broader_family_pool"

            if signature in seen_projection_signatures and evidence_pool != "excluded_pool":
                excluded_reasons = ["duplicate"]
                used_for_price = False
                evidence_pool = "excluded_pool"
            seen_projection_signatures.add(signature)

            display_role = _humanize_result_role(compatibility_label)
            display_excluded_reason = [_humanize_excluded_reason(reason) for reason in excluded_reasons]
            display_price_usage = _build_price_usage_label(
                used_for_price,
                evidence_pool,
                display_excluded_reason,
            )
            price_number = _parse_price_number(result.get("price"))
            if (
                explicit_fle2_projection_query
                and compatibility_label == "Exact variant"
                and evidence_pool == "exact_base_model_pool"
                and not used_for_price
                and not display_excluded_reason
                and price_number is not None
            ):
                display_price_usage = "Exact variant match visible, but not selected for exact price"
            if price_number is None:
                used_for_price = False
                display_price_usage = "No usable price"

            evidence_items.append(
                {
                    "result_index": index,
                    "evidence_signature": "||".join(signature),
                    "title": _result_title(result),
                    "source": str(result.get("source") or ""),
                    "price": str(result.get("price") or ""),
                    "currency": _result_currency(result),
                    "compatibility_label": compatibility_label,
                    "result_role_label": display_role,
                    "evidence_pool": evidence_pool,
                    "evidence_pool_label": _humanize_evidence_pool(evidence_pool),
                    "used_for_price": used_for_price,
                    "price_usage_label": display_price_usage,
                    "excluded_reason": display_excluded_reason,
                    "display_category": str(_result_field(result, "category") or ""),
                    "display_model": str(_result_field(result, "model_canonical") or _result_field(result, "model_raw") or ""),
                }
            )
        return evidence_items

    visible_result_evidence = _build_visible_result_evidence(results)
    top_result_evidence = list(visible_result_evidence[:5])

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
    display_unlock_requirements = [_humanize_unlock_requirement(item) for item in unlock_requirements]
    variant_label = "variant"
    if variant_signals:
        variant_values = [str(signal.get("value") or "").strip() for signal in variant_signals if signal.get("value")]
        if variant_values:
            variant_label = " / ".join(variant_values)
    display_evidence_pool_summary = {
        "exact_variant_pool_count": int(exact_variant_pool["cleaned_pool_count"]),
        "exact_base_model_pool_count": int(exact_base_model_pool["cleaned_pool_count"]),
        "broader_family_pool_count": int(broader_family_pool["cleaned_pool_count"]),
        "excluded_pool_count": excluded_pool_count,
        "outlier_removed_count": outlier_removed_count,
        "broader_reference_allowed": broader_reference_allowed,
        "price_band_quality_state": display_price_band_quality_state,
        "summary_line": _summarize_evidence_pool_counts(
            variant_label=variant_label if variant_signals else None,
            exact_variant_count=int(exact_variant_pool["cleaned_pool_count"]),
            exact_base_count=int(exact_base_model_pool["cleaned_pool_count"]),
            broader_count=int(broader_family_pool["cleaned_pool_count"]),
            excluded_count=excluded_pool_count,
        ),
        "exact_variant_label": (
            f"Exact {variant_label} evidence: {int(exact_variant_pool['cleaned_pool_count'])}"
            if variant_signals
            else None
        ),
        "same_model_label": f"Same base model evidence: {int(exact_base_model_pool['cleaned_pool_count'])}",
        "reference_label": f"Reference evidence: {int(broader_family_pool['cleaned_pool_count'])}",
        "excluded_label": f"Excluded from price: {excluded_pool_count}",
    }
    display_match_state_message = _humanize_policy_reason(
        alignmentReasons[0] if (alignmentReasons := price_scope_search_alignment_reason) else search_confidence_state
    )
    review_price_status = _build_price_status_message(
        expected_category=expected_category or ("Body" if intent.get("body_intent") else "Lens"),
        price_summary_allowed=bool(price_summary_allowed),
        price_scope=price_scope,
        broader_reference_allowed=bool(broader_reference_allowed),
        market_entry_allowed=bool(market_entry_allowed),
    )
    review_why = _build_query_review_why(
        price_summary_allowed=bool(price_summary_allowed),
        broader_reference_allowed=bool(broader_reference_allowed),
        display_match_state_message=display_match_state_message,
        display_price_band_quality_state=display_price_band_quality_state,
        variant_signals=variant_signals,
        price_scope=price_scope,
        search_confidence_state=search_confidence_state,
        third_party_top_domination_detected=bool(third_party_top_domination_detected),
        exact_variant_pool_count=int(exact_variant_pool["cleaned_pool_count"]),
    )
    display_query_review = {
        "query": query,
        "interpreted_target": _build_interpreted_target(
            query,
            intent,
            expected_family,
            expected_mount,
            variant_signals,
        ),
        "category": expected_category or ("Body" if intent.get("body_intent") else "Lens"),
        "match_state": display_match_state_message,
        "price_status": review_price_status,
        "why": review_why,
        "evidence_summary": display_evidence_pool_summary["summary_line"],
        "evidence_cards": [
            item
            for item in [
                display_evidence_pool_summary["exact_variant_label"],
                display_evidence_pool_summary["same_model_label"],
                display_evidence_pool_summary["reference_label"],
                display_evidence_pool_summary["excluded_label"],
            ]
            if item
        ],
        "needed_to_unlock": list(display_unlock_requirements),
        "details_toggle_label": "Show evidence details",
        "details_toggle_hide_label": "Hide evidence details",
        "copy_button_label": "Copy summary",
    }

    top_summary_lines = []
    for index, item in enumerate(top_result_evidence[:3], start=1):
        parts = [f"{index}. {item['title']}"]
        if item.get("result_role_label"):
            parts.append(item["result_role_label"])
        if item.get("price_usage_label"):
            parts.append(item["price_usage_label"])
        top_summary_lines.append(" — ".join(parts))
    copy_summary_lines = [
        "Query review",
        f"You searched: {query}",
        f"Interpreted as: {display_query_review['interpreted_target']}",
        f"Category: {display_query_review['category']}",
        f"Match status: {display_query_review['match_state']}",
        f"Price status: {display_query_review['price_status']}",
        f"Why: {display_query_review['why']}",
        f"Evidence: {display_query_review['evidence_summary']}",
    ]
    if display_query_review["needed_to_unlock"]:
        copy_summary_lines.append("Price stays locked until:")
        copy_summary_lines.extend(
            f"- {item}" for item in display_query_review["needed_to_unlock"]
        )
    if top_summary_lines:
        copy_summary_lines.append("Top visible evidence:")
        copy_summary_lines.extend(top_summary_lines)
    display_query_review["copy_summary_text"] = "\n".join(copy_summary_lines)

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
        "display_visible_result_evidence": visible_result_evidence,
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
    resolved_path = _resolve_search_index_path(path) if (records is None or path is not None) else None
    response_meta = _build_index_meta(resolved_path, parsed["query"])

    def maybe_supplement_summicron_50_hood_results(
        response: dict[str, Any],
        evidence_response: dict[str, Any] | None,
    ) -> None:
        if parsed["sort"] != "relevance" or parsed["offset"] != 0:
            return
        intent = response.get("intent") or {}
        if not _is_explicit_summicron_50_hood_query(intent):
            return
        supplement_query = _build_summicron_50_hood_supplement_query(intent)
        kwargs = dict(
            query=supplement_query,
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
            supplemental_response = search_records(records=records, **kwargs)
        else:
            supplemental_response = load_and_search(path=resolved_path, **kwargs)
        supplemental_rows = _hood_like_supplement_results(list(supplemental_response.get("results") or []))
        if not supplemental_rows:
            return

        response_merged = _merge_unique_results(list(response.get("results") or []), supplemental_rows)
        reranked_response = _rerank_results_for_query_context(
            parsed["query"],
            {**response, "results": response_merged},
            parsed["sort"],
        )
        response["results"] = reranked_response[: parsed["limit"]]
        response["result_count"] = len(response["results"])

        if evidence_response is not None:
            evidence_merged = _merge_unique_results(list(evidence_response.get("results") or []), supplemental_rows)
            evidence_response["results"] = _rerank_results_for_query_context(
                parsed["query"],
                {**evidence_response, "results": evidence_merged},
                parsed["sort"],
            )[:evidence_limit]
            evidence_response["result_count"] = len(evidence_response["results"])

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
            evidence_response = search_records(records=records, **kwargs)
        else:
            evidence_response = load_and_search(path=resolved_path, **kwargs)
        evidence_response["results"] = _rerank_results_for_query_context(parsed["query"], evidence_response, parsed["sort"])
        return evidence_response

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
        response["results"] = _rerank_results_for_query_context(parsed["query"], response, parsed["sort"])
        evidence_response = build_evidence_response()
        maybe_supplement_summicron_50_hood_results(response, evidence_response)
        _promote_expanded_results_for_query_context(
            parsed["query"],
            response,
            evidence_response,
            sort=parsed["sort"],
            limit=parsed["limit"],
            offset=parsed["offset"],
        )
        response["ui_hints"] = build_query_ui_hints(parsed["query"], response.get("results"))
        response["market_entry_policy"] = build_market_entry_policy(
            parsed["query"],
            response,
            response["ui_hints"],
            evidence_response=evidence_response,
        )
        response.update(response["market_entry_policy"])
        response["meta"] = response_meta
        return response

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
    response["results"] = _rerank_results_for_query_context(parsed["query"], response, parsed["sort"])
    evidence_response = build_evidence_response()
    maybe_supplement_summicron_50_hood_results(response, evidence_response)
    _promote_expanded_results_for_query_context(
        parsed["query"],
        response,
        evidence_response,
        sort=parsed["sort"],
        limit=parsed["limit"],
        offset=parsed["offset"],
    )
    response["ui_hints"] = build_query_ui_hints(parsed["query"], response.get("results"))
    response["market_entry_policy"] = build_market_entry_policy(
        parsed["query"],
        response,
        response["ui_hints"],
        evidence_response=evidence_response,
    )
    response.update(response["market_entry_policy"])
    response["meta"] = response_meta
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
