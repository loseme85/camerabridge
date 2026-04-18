"""
search_response.py
==================
API/UI response formatting layer.

Responsibilities:
  - Convert query_resolver ranking output into a lightweight external schema.
  - Keep final_output as the user-facing classified source of truth.
  - Expose debug/audit details only when requested.

Non-responsibilities:
  - Do not classify listings.
  - Do not parse search aliases.
  - Do not apply trusted metadata overrides.
  - Do not import classifier_v2.py.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Optional

from query_resolver import (
    DEFAULT_MIN_SCORE,
    DEFAULT_RESOLVED_PATH,
    load_resolved_records,
    rank_listings,
)


SEARCH_RESPONSE_SCHEMA_VERSION = "search_response.v1"

FINAL_OUTPUT_FIELDS = [
    "brand",
    "mount",
    "category",
    "label",
    "model_raw",
    "model_canonical",
    "variant",
    "focal_length",
    "accessory_type",
    "compatible_mounts",
    "compatible_systems",
    "sold_quality",
]


def _compact_final_output(final_output: dict[str, Any]) -> dict[str, Any]:
    return {
        field_name: final_output.get(field_name)
        for field_name in FINAL_OUTPUT_FIELDS
        if field_name in final_output
    }


def _record_by_index(records: list[dict[str, Any]]) -> dict[int, dict[str, Any]]:
    indexed = {}
    for record in records:
        index = record.get("record_index")
        if isinstance(index, int):
            indexed[index] = record
    return indexed


def format_search_result(
    ranked_result: dict[str, Any],
    source_record: Optional[dict[str, Any]] = None,
    include_debug: bool = False,
) -> dict[str, Any]:
    """
    Convert one query_resolver result into an API/UI-safe result object.

    The default response intentionally avoids exposing full raw/classifier
    records. Debug mode can include classifier_output and audit_trail for QA.
    """
    final_output = ranked_result.get("final_output") or {}
    result = {
        "score": ranked_result.get("score"),
        "title": ranked_result.get("title_raw") or final_output.get("title_raw"),
        "price": final_output.get("price_raw"),
        "currency": final_output.get("currency"),
        "source": ranked_result.get("source") or final_output.get("source"),
        "source_url": ranked_result.get("source_url") or final_output.get("source_url"),
        "image_url": final_output.get("image_url"),
        "condition": final_output.get("condition_raw"),
        "final_output": _compact_final_output(final_output),
        "used_override": bool(ranked_result.get("used_override")),
        "match_quality": ranked_result.get("match_quality"),
        "matched_fields": list(ranked_result.get("matched_fields") or []),
        "score_breakdown": list(ranked_result.get("score_breakdown") or []),
        "warnings": list(ranked_result.get("warnings") or []),
    }

    if include_debug:
        result["debug"] = {
            "record_index": ranked_result.get("record_index"),
            "raw_score": ranked_result.get("raw_score"),
            "possible_score": ranked_result.get("possible_score"),
            "match_quality_rank": ranked_result.get("match_quality_rank"),
            "mismatch_reasons": list(ranked_result.get("mismatch_reasons") or []),
            "classifier_output": (
                source_record.get("classifier_output")
                if isinstance(source_record, dict)
                else None
            ),
            "audit_trail": (
                source_record.get("audit_trail")
                if isinstance(source_record, dict)
                else None
            ),
        }

    return result


def format_search_response(
    ranked_payload: dict[str, Any],
    records: Optional[list[dict[str, Any]]] = None,
    include_debug: bool = False,
) -> dict[str, Any]:
    intent = ranked_payload.get("intent") or {}
    ranked_results = ranked_payload.get("results") or []
    record_index = _record_by_index(records or [])
    response_warnings = list(intent.get("warnings") or [])

    if not ranked_results:
        response_warnings.append("no_results")

    results = []
    for ranked_result in ranked_results:
        source_record = record_index.get(ranked_result.get("record_index"))
        results.append(
            format_search_result(
                ranked_result,
                source_record=source_record,
                include_debug=include_debug,
            )
        )

    return {
        "schema_version": SEARCH_RESPONSE_SCHEMA_VERSION,
        "query": intent.get("original_query"),
        "intent": intent,
        "result_count": len(results),
        "total_ranked": ranked_payload.get("total_ranked", len(results)),
        "warnings": response_warnings,
        "results": results,
    }


def build_search_response(
    query: str,
    records: list[dict[str, Any]],
    limit: int = 10,
    min_score: float = DEFAULT_MIN_SCORE,
    include_debug: bool = False,
) -> dict[str, Any]:
    ranked = rank_listings(query, records, limit=limit, min_score=min_score)
    return format_search_response(
        ranked,
        records=records,
        include_debug=include_debug,
    )


def load_and_build_search_response(
    query: str,
    path: str | Path = DEFAULT_RESOLVED_PATH,
    limit: int = 10,
    min_score: float = DEFAULT_MIN_SCORE,
    include_debug: bool = False,
) -> dict[str, Any]:
    records = load_resolved_records(path)
    return build_search_response(
        query=query,
        records=records,
        limit=limit,
        min_score=min_score,
        include_debug=include_debug,
    )


def run_response_demo(
    queries: Optional[list[str]] = None,
    path: str | Path = DEFAULT_RESOLVED_PATH,
    limit: int = 2,
) -> list[dict[str, Any]]:
    demo_queries = queries or [
        "35lux aa",
        "mp3 silver",
        "q3 28",
        "ltm summaron 35",
    ]
    records = load_resolved_records(path)
    return [
        build_search_response(query, records, limit=limit, min_score=25)
        for query in demo_queries
    ]


if __name__ == "__main__":
    print(json.dumps(run_response_demo(), ensure_ascii=False, indent=2))
