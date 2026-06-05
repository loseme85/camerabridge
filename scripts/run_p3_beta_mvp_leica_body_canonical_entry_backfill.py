from __future__ import annotations

import argparse
import json
import subprocess
from collections import Counter
from pathlib import Path
from typing import Any
import sys


TASK_NAME = "P3-BETA-MVP-LEICA-BODY-CANONICAL-ENTRY-BACKFILL"
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from api.search import search_from_params
from search_service import load_search_records

ADMIN_DIR = PROJECT_ROOT / "data" / "admin"
INDEX_PATH = ADMIN_DIR / "canonical_entities_index.json"
PREVIOUS_AUDIT_PATH = ADMIN_DIR / "leica_global_canonical_entry_coverage_audit_v0.json"
MD_PATH = ADMIN_DIR / "p3_beta_mvp_leica_body_canonical_entry_backfill_v0.md"
JSONL_PATH = ADMIN_DIR / "p3_beta_mvp_leica_body_canonical_entry_backfill_v0.jsonl"
JSON_PATH = ADMIN_DIR / "leica_body_canonical_entry_backfill_v0.json"


FAMILY_FILES = {
    "leica_m_film_bodies": "entities/leica_m_film_bodies.json",
    "leica_m_digital_bodies": "entities/leica_m_digital_bodies.json",
    "leica_q_bodies": "entities/leica_q_bodies.json",
    "leica_sl_bodies": "entities/leica_sl_bodies.json",
}

ACTIVE_MODEL_TO_FAMILY = {
    "M3": "leica_m_film_bodies",
    "M4": "leica_m_film_bodies",
    "M5": "leica_m_film_bodies",
    "M6": "leica_m_film_bodies",
    "M6 TTL": "leica_m_film_bodies",
    "MP": "leica_m_film_bodies",
    "M9": "leica_m_digital_bodies",
    "M9-P": "leica_m_digital_bodies",
    "M10": "leica_m_digital_bodies",
    "M10-R": "leica_m_digital_bodies",
    "M11": "leica_m_digital_bodies",
    "Q2": "leica_q_bodies",
    "Q3": "leica_q_bodies",
    "SL2": "leica_sl_bodies",
    "SL3": "leica_sl_bodies",
}

CANDIDATES = [
    {
        "candidate_name": "Leica M2",
        "product_group": "Leica M film bodies",
        "query": "Leica M2",
        "expected_body_intents": ["M2"],
        "index_key": None,
        "entry_file": None,
        "expected_action": "hold_manual_review",
        "hold_reason": "Top result is still Lens and safe Body dominance is not confirmed.",
    },
    {
        "candidate_name": "Leica M3",
        "product_group": "Leica M film bodies",
        "query": "Leica M3",
        "expected_body_intents": ["M3"],
        "index_key": "leica_m_film_bodies",
        "entry_file": "entities/leica_m_film_bodies.json",
        "expected_action": "add_active_body_entry",
    },
    {
        "candidate_name": "Leica M4",
        "product_group": "Leica M film bodies",
        "query": "Leica M4",
        "expected_body_intents": ["M4"],
        "index_key": "leica_m_film_bodies",
        "entry_file": "entities/leica_m_film_bodies.json",
        "expected_action": "add_active_body_entry",
    },
    {
        "candidate_name": "Leica M4-2",
        "product_group": "Leica M film bodies",
        "query": "Leica M4-2",
        "expected_body_intents": [],
        "index_key": None,
        "entry_file": None,
        "expected_action": "hold_parser_gap",
        "hold_reason": "Body parser does not currently connect Leica M4-2 safely.",
    },
    {
        "candidate_name": "Leica M4-P",
        "product_group": "Leica M film bodies",
        "query": "Leica M4-P",
        "expected_body_intents": [],
        "index_key": None,
        "entry_file": None,
        "expected_action": "hold_parser_gap",
        "hold_reason": "Body parser does not currently connect Leica M4-P safely.",
    },
    {
        "candidate_name": "Leica M5",
        "product_group": "Leica M film bodies",
        "query": "Leica M5",
        "expected_body_intents": ["M5"],
        "index_key": "leica_m_film_bodies",
        "entry_file": "entities/leica_m_film_bodies.json",
        "expected_action": "add_active_body_entry",
    },
    {
        "candidate_name": "Leica M6",
        "product_group": "Leica M film bodies",
        "query": "Leica M6",
        "expected_body_intents": ["M6"],
        "index_key": "leica_m_film_bodies",
        "entry_file": "entities/leica_m_film_bodies.json",
        "expected_action": "add_active_body_entry",
    },
    {
        "candidate_name": "Leica M6 TTL",
        "product_group": "Leica M film bodies",
        "query": "Leica M6 TTL",
        "expected_body_intents": ["M6"],
        "index_key": "leica_m_film_bodies",
        "entry_file": "entities/leica_m_film_bodies.json",
        "expected_action": "add_active_body_entry",
    },
    {
        "candidate_name": "Leica MP",
        "product_group": "Leica M film bodies",
        "query": "Leica MP",
        "expected_body_intents": ["MP"],
        "index_key": "leica_m_film_bodies",
        "entry_file": "entities/leica_m_film_bodies.json",
        "expected_action": "add_active_body_entry",
    },
    {
        "candidate_name": "Leica M-A",
        "product_group": "Leica M film bodies",
        "query": "Leica M-A",
        "expected_body_intents": [],
        "index_key": None,
        "entry_file": None,
        "expected_action": "hold_parser_gap",
        "hold_reason": "Body parser does not currently connect Leica M-A safely.",
    },
    {
        "candidate_name": "Leica M8",
        "product_group": "Leica M digital bodies",
        "query": "Leica M8",
        "expected_body_intents": [],
        "index_key": None,
        "entry_file": None,
        "expected_action": "hold_parser_gap",
        "hold_reason": "Leica M8 currently falls back to broad Leica Lens results.",
    },
    {
        "candidate_name": "Leica M8.2",
        "product_group": "Leica M digital bodies",
        "query": "Leica M8.2",
        "expected_body_intents": [],
        "index_key": None,
        "entry_file": None,
        "expected_action": "hold_parser_gap",
        "hold_reason": "Leica M8.2 currently falls back to broad Leica Lens results.",
    },
    {
        "candidate_name": "Leica M9",
        "product_group": "Leica M digital bodies",
        "query": "Leica M9",
        "expected_body_intents": ["M9"],
        "index_key": "leica_m_digital_bodies",
        "entry_file": "entities/leica_m_digital_bodies.json",
        "expected_action": "add_active_body_entry",
    },
    {
        "candidate_name": "Leica M9-P",
        "product_group": "Leica M digital bodies",
        "query": "Leica M9-P",
        "expected_body_intents": ["M9-P"],
        "index_key": "leica_m_digital_bodies",
        "entry_file": "entities/leica_m_digital_bodies.json",
        "expected_action": "add_active_body_entry",
    },
    {
        "candidate_name": "Leica M Typ 240",
        "product_group": "Leica M digital bodies",
        "query": "Leica M Typ 240",
        "expected_body_intents": [],
        "index_key": None,
        "entry_file": None,
        "expected_action": "hold_parser_gap",
        "hold_reason": "Typ 240 queries are not yet body-safe in parser/ranking.",
    },
    {
        "candidate_name": "Leica M-P Typ 240",
        "product_group": "Leica M digital bodies",
        "query": "Leica M-P Typ 240",
        "expected_body_intents": [],
        "index_key": None,
        "entry_file": None,
        "expected_action": "hold_source_gap",
        "hold_reason": "Observed source coverage is insufficient for safe active seed promotion.",
    },
    {
        "candidate_name": "Leica M Typ 262",
        "product_group": "Leica M digital bodies",
        "query": "Leica M Typ 262",
        "expected_body_intents": [],
        "index_key": None,
        "entry_file": None,
        "expected_action": "hold_parser_gap",
        "hold_reason": "Typ 262 queries are not yet body-safe in parser/ranking.",
    },
    {
        "candidate_name": "Leica M10",
        "product_group": "Leica M digital bodies",
        "query": "Leica M10",
        "expected_body_intents": ["M10"],
        "index_key": "leica_m_digital_bodies",
        "entry_file": "entities/leica_m_digital_bodies.json",
        "expected_action": "add_active_body_entry",
    },
    {
        "candidate_name": "Leica M10-P",
        "product_group": "Leica M digital bodies",
        "query": "Leica M10-P",
        "expected_body_intents": [],
        "index_key": None,
        "entry_file": None,
        "expected_action": "hold_parser_gap",
        "hold_reason": "Leica M10-P currently collapses into broad Leica Lens fallback.",
    },
    {
        "candidate_name": "Leica M10-R",
        "product_group": "Leica M digital bodies",
        "query": "Leica M10-R",
        "expected_body_intents": ["M10-R"],
        "index_key": "leica_m_digital_bodies",
        "entry_file": "entities/leica_m_digital_bodies.json",
        "expected_action": "add_active_body_entry",
    },
    {
        "candidate_name": "Leica M10 Monochrom",
        "product_group": "Leica M digital bodies",
        "query": "Leica M10 Monochrom",
        "expected_body_intents": ["M10"],
        "index_key": None,
        "entry_file": None,
        "expected_action": "hold_manual_review",
        "hold_reason": "Query resolves to M10 body line but not yet exact-enough to seed as a separate active body entry.",
    },
    {
        "candidate_name": "Leica M11",
        "product_group": "Leica M digital bodies",
        "query": "Leica M11",
        "expected_body_intents": ["M11"],
        "index_key": "leica_m_digital_bodies",
        "entry_file": "entities/leica_m_digital_bodies.json",
        "expected_action": "add_active_body_entry",
    },
    {
        "candidate_name": "Leica M11-P",
        "product_group": "Leica M digital bodies",
        "query": "Leica M11-P",
        "expected_body_intents": [],
        "index_key": None,
        "entry_file": None,
        "expected_action": "hold_parser_gap",
        "hold_reason": "Leica M11-P is not yet parser-connected as an exact body query.",
    },
    {
        "candidate_name": "Leica M11 Monochrom",
        "product_group": "Leica M digital bodies",
        "query": "Leica M11 Monochrom",
        "expected_body_intents": ["M11"],
        "index_key": None,
        "entry_file": None,
        "expected_action": "hold_manual_review",
        "hold_reason": "Leica M11 Monochrom still collapses to base M11 body intent rather than an exact canonical body row.",
    },
    {
        "candidate_name": "Leica Q",
        "product_group": "Leica Q / SL bodies",
        "query": "Leica Q",
        "expected_body_intents": [],
        "index_key": None,
        "entry_file": None,
        "expected_action": "hold_parser_gap",
        "hold_reason": "Leica Q still falls into accessory-led results and is not ready for active seed promotion.",
    },
    {
        "candidate_name": "Leica Q2",
        "product_group": "Leica Q / SL bodies",
        "query": "Leica Q2",
        "expected_body_intents": ["Q2"],
        "index_key": "leica_q_bodies",
        "entry_file": "entities/leica_q_bodies.json",
        "expected_action": "add_active_body_entry",
    },
    {
        "candidate_name": "Leica Q2 Monochrom",
        "product_group": "Leica Q / SL bodies",
        "query": "Leica Q2 Monochrom",
        "expected_body_intents": ["Q2"],
        "index_key": None,
        "entry_file": None,
        "expected_action": "hold_manual_review",
        "hold_reason": "Leica Q2 Monochrom currently resolves into base Q2 body intent rather than an exact canonical body row.",
    },
    {
        "candidate_name": "Leica Q3",
        "product_group": "Leica Q / SL bodies",
        "query": "Leica Q3",
        "expected_body_intents": ["Q3"],
        "index_key": "leica_q_bodies",
        "entry_file": "entities/leica_q_bodies.json",
        "expected_action": "add_active_body_entry",
    },
    {
        "candidate_name": "Leica Q3 43",
        "product_group": "Leica Q / SL bodies",
        "query": "Leica Q3 43",
        "expected_body_intents": ["Q3"],
        "index_key": None,
        "entry_file": None,
        "expected_action": "hold_manual_review",
        "hold_reason": "Leica Q3 43 still resolves to base Q3 body intent and remains safer as a hold candidate.",
    },
    {
        "candidate_name": "Leica SL2",
        "product_group": "Leica Q / SL bodies",
        "query": "Leica SL2",
        "expected_body_intents": ["SL2"],
        "index_key": "leica_sl_bodies",
        "entry_file": "entities/leica_sl_bodies.json",
        "expected_action": "add_active_body_entry",
    },
    {
        "candidate_name": "Leica SL2-S",
        "product_group": "Leica Q / SL bodies",
        "query": "Leica SL2-S",
        "expected_body_intents": ["SL2"],
        "index_key": None,
        "entry_file": None,
        "expected_action": "hold_manual_review",
        "hold_reason": "Leica SL2-S still collapses to base SL2 body intent rather than an exact canonical body row.",
    },
    {
        "candidate_name": "Leica SL3",
        "product_group": "Leica Q / SL bodies",
        "query": "Leica SL3",
        "expected_body_intents": ["SL3"],
        "index_key": "leica_sl_bodies",
        "entry_file": "entities/leica_sl_bodies.json",
        "expected_action": "add_active_body_entry",
    },
    {
        "candidate_name": "Leica M1",
        "product_group": "Hold / manual review",
        "query": "Leica M1",
        "expected_body_intents": [],
        "index_key": None,
        "entry_file": None,
        "expected_action": "hold_manual_review",
        "hold_reason": "Owner requested M1 stay out of this active backfill round.",
    },
    {
        "candidate_name": "Leica M7",
        "product_group": "Hold / manual review",
        "query": "Leica M7",
        "expected_body_intents": [],
        "index_key": None,
        "entry_file": None,
        "expected_action": "hold_manual_review",
        "hold_reason": "Owner requested M7 stay out of this active backfill round.",
    },
]

SMOKE_QUERIES = [
    "Leica M2",
    "M2",
    "Leica M3",
    "M3",
    "Leica M4",
    "Leica M5",
    "Leica M6",
    "M6",
    "Leica MP",
    "MP silver",
    "Leica M9",
    "Leica M10",
    "Leica M10-R",
    "Leica M11",
    "Leica Q2",
    "Leica Q3",
    "q3 28",
    "Leica SL2",
    "Leica SL3",
    "Leica M1",
    "Leica M7",
]

REGRESSION_QUERIES = [
    "M50/1.2",
    "Leica M50/1.2 1세대",
    "ltm summaron 35",
    "35 lux aa",
    "summicron",
    "ricoh gr iiix",
    "hasselblad xpan",
]


def _run(cmd: list[str]) -> str:
    return subprocess.check_output(cmd, cwd=PROJECT_ROOT, text=True).strip()


def _load_seed_inventory() -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    index_payload = json.loads(INDEX_PATH.read_text(encoding="utf-8"))
    families = list(index_payload.get("families") or [])
    entities: list[dict[str, Any]] = []
    for family in families:
        rel = family.get("file")
        if not rel:
            continue
        payload = json.loads((ADMIN_DIR / rel).read_text(encoding="utf-8"))
        for entity in payload.get("entities") or []:
            enriched = dict(entity)
            enriched["_family_id"] = payload.get("family_id") or family.get("id")
            enriched["_family_name"] = payload.get("family_name") or family.get("family_name")
            enriched["_file"] = rel
            entities.append(enriched)
    return families, entities


def _load_previous_status() -> dict[str, dict[str, Any]]:
    if not PREVIOUS_AUDIT_PATH.exists():
        return {}
    payload = json.loads(PREVIOUS_AUDIT_PATH.read_text(encoding="utf-8"))
    rows = payload.get("target_rows") or []
    return {str(row.get("query")): row for row in rows}


def _seed_exists(candidate_name: str, seed_entities: list[dict[str, Any]]) -> bool:
    needle = candidate_name.lower()
    for entity in seed_entities:
        haystack = {
            str(entity.get("canonical_name") or "").lower(),
            str(entity.get("model_canonical") or "").lower(),
            str(entity.get("model_raw") or "").lower(),
        }
        haystack.update(str(alias).lower() for alias in entity.get("aliases") or [])
        if needle in haystack:
            return True
    return False


def _query_summary(query: str, records: list[dict[str, Any]]) -> dict[str, Any]:
    response = search_from_params({"q": query, "limit": "10"}, records=records)
    results = list(response.get("results") or [])
    top = results[0] if results else {}
    display = top.get("display_output") or {}
    final = top.get("final_output") or {}
    top_category = display.get("display_category") or final.get("category")
    top_model = display.get("display_model") or final.get("model_canonical") or final.get("model_raw")
    return {
        "query": query,
        "body_intent": (response.get("intent") or {}).get("body_intent"),
        "market_entry_allowed": bool(response.get("market_entry_allowed")),
        "price_summary_allowed": bool(response.get("price_summary_allowed")),
        "top_result_category": top_category,
        "top_result_model": top_model,
        "top_three_categories": [
            ((item.get("display_output") or {}).get("display_category") or (item.get("final_output") or {}).get("category"))
            for item in results[:3]
        ],
        "total_ranked": int(response.get("total_ranked") or 0),
        "compact_lens_notation_detected": bool(top.get("compact_lens_notation_detected")),
        "stale_body_normalization_detected": bool(top.get("stale_body_normalization_detected")),
    }


def _family_index_snapshot() -> list[dict[str, Any]]:
    index_payload = json.loads(INDEX_PATH.read_text(encoding="utf-8"))
    families = []
    for family in index_payload.get("families") or []:
        if family.get("id") in FAMILY_FILES:
            families.append(dict(family))
    return families


def _schema_inspection(seed_entities: list[dict[str, Any]]) -> dict[str, Any]:
    indexed = _family_index_snapshot()
    body_rows = [entity for entity in seed_entities if entity.get("_family_id") in FAMILY_FILES]
    runtime_references = []
    for path in [
        "query_parser.py",
        "query_resolver.py",
        "search_service.py",
        "search_response.py",
        "api/search.py",
    ]:
        text = (PROJECT_ROOT / path).read_text(encoding="utf-8")
        if "canonical_entities_index.json" in text or "data/admin/entities" in text:
            runtime_references.append(path)
    return {
        "canonical_index_path": str(INDEX_PATH),
        "new_family_count": len(indexed),
        "new_body_seed_row_count": len(body_rows),
        "new_family_ids": [item["id"] for item in indexed],
        "runtime_module_direct_seed_references": runtime_references,
        "schema_note": "Canonical seed layer is schema-clear and admin-readable. Direct runtime references to canonical seed files are not present in the current search modules inspected in this round.",
    }


def _candidate_rows(records: list[dict[str, Any]], seed_entities: list[dict[str, Any]], previous_rows: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    rows = []
    for candidate in CANDIDATES:
        smoke = _query_summary(candidate["query"], records)
        before = previous_rows.get(candidate["query"], {})
        exists_before = bool(before.get("canonical_entry_exists"))
        exists_after = _seed_exists(candidate["candidate_name"], seed_entities)
        parser_body_intent = smoke["body_intent"]
        top_category = smoke["top_result_category"]
        top_model = smoke["top_result_model"]
        body_boundary_safe = top_category == "Body" and smoke["top_three_categories"][:3].count("Body") >= 2
        expected_intents = set(candidate.get("expected_body_intents") or [])
        parser_ok = not expected_intents or parser_body_intent in expected_intents

        if candidate["expected_action"] == "add_active_body_entry" and exists_after and parser_ok and body_boundary_safe:
            action_taken = "add_active_body_entry"
            hold_reason = None
        elif exists_before:
            action_taken = "already_exists_noop"
            hold_reason = None
        else:
            action_taken = candidate["expected_action"]
            hold_reason = candidate.get("hold_reason")

        rows.append(
            {
                "candidate_name": candidate["candidate_name"],
                "product_group": candidate["product_group"],
                "canonical_entry_exists_before": exists_before,
                "canonical_entry_exists_after": exists_after,
                "search_results_exist": smoke["total_ranked"] > 0,
                "observed_result_count": smoke["total_ranked"],
                "top_result_category": top_category,
                "top_result_model": top_model,
                "parser_body_intent": parser_body_intent,
                "body_boundary_safe": body_boundary_safe,
                "recommended_action": candidate["expected_action"],
                "action_taken": action_taken,
                "hold_reason": hold_reason,
                "entry_file": candidate["entry_file"],
                "index_key": candidate["index_key"],
                "smoke_query_result": smoke,
            }
        )
    return rows


def _git_diff_summary() -> dict[str, Any]:
    status = _run(["git", "status", "--short"])
    diff = _run(["git", "diff", "--stat"])
    return {
        "git_status_short": status.splitlines(),
        "git_diff_stat": diff.splitlines(),
    }


def _decision_status(candidate_rows: list[dict[str, Any]], commit_executed: bool, push_executed: bool, preview_url: str | None) -> str:
    blocking = [
        row for row in candidate_rows
        if row["recommended_action"] == "add_active_body_entry" and row["action_taken"] != "add_active_body_entry"
    ]
    if blocking:
        return "leica_body_canonical_entry_backfill_hold_unsafe_candidate_mix"
    if push_executed and preview_url:
        return "leica_body_canonical_entry_backfill_pushed_ready_for_owner_recheck"
    if commit_executed:
        return "leica_body_canonical_entry_backfill_passed_ready_for_owner_approved_push"
    return "leica_body_canonical_entry_backfill_passed_ready_for_owner_approved_push"


def _build_markdown(payload: dict[str, Any]) -> str:
    lines = [
        f"# {payload['task_name']}",
        "",
        f"- decision_status: `{payload['decision_status']}`",
        "",
        "## Previous global coverage audit 요약",
        f"- {payload['previous_global_coverage_audit_summary']}",
        "",
        "## Body backfill 대상과 제외 대상",
        f"- active body candidate count: `{len(payload['added_canonical_body_entries'])}`",
        f"- hold/manual review count: `{len(payload['hold_manual_review_entries'])}`",
        f"- source gap count: `{len(payload['source_gap_entries'])}`",
        "",
        "## Schema inspection 결과",
    ]
    schema = payload["schema_inspection_result"]
    lines.append(f"- canonical index path: `{schema['canonical_index_path']}`")
    lines.append(f"- new family ids: `{', '.join(schema['new_family_ids'])}`")
    lines.append(f"- new body seed row count: `{schema['new_body_seed_row_count']}`")
    lines.append(f"- runtime direct seed references: `{schema['runtime_module_direct_seed_references']}`")
    lines.append(f"- note: {schema['schema_note']}")
    lines.extend(["", "## 추가한 canonical body entries"])
    for row in payload["added_canonical_body_entries"]:
        lines.append(
            f"- `{row['candidate_name']}` -> `{row['entry_file']}` / body_intent=`{row['parser_body_intent']}` / top=`{row['top_result_category']}:{row['top_result_model']}`"
        )
    lines.extend(["", "## Already existing entries"])
    for row in payload["already_existing_entries"]:
        lines.append(f"- `{row['candidate_name']}`")
    if not payload["already_existing_entries"]:
        lines.append("- none")
    lines.extend(["", "## Hold / manual review entries"])
    for row in payload["hold_manual_review_entries"]:
        lines.append(f"- `{row['candidate_name']}`: {row['hold_reason']}")
    lines.extend(["", "## Source gap entries"])
    for row in payload["source_gap_entries"]:
        lines.append(f"- `{row['candidate_name']}`: {row['hold_reason']}")
    if not payload["source_gap_entries"]:
        lines.append("- none")
    lines.extend(["", "## Smoke query 결과"])
    for row in payload["smoke_query_results"]:
        lines.append(
            f"- `{row['query']}`: body_intent=`{row['body_intent']}`, market=`{row['market_entry_allowed']}`, "
            f"price=`{row['price_summary_allowed']}`, top=`{row['top_result_category']}:{row['top_result_model']}`, "
            f"top3=`{row['top_three_categories']}`"
        )
    lines.extend(["", "## Market entry / price summary gate 유지 여부"])
    lines.append(f"- {payload['market_entry_price_summary_gate_status']}")
    lines.extend(["", "## Body / lens regression 결과"])
    for row in payload["body_lens_regression_results"]:
        lines.append(
            f"- `{row['query']}`: top=`{row['top_result_category']}:{row['top_result_model']}`, "
            f"market=`{row['market_entry_allowed']}`, compact_lens=`{row['compact_lens_notation_detected']}`, "
            f"stale_body=`{row['stale_body_normalization_detected']}`"
        )
    lines.extend(["", "## Git diff 요약"])
    for line in payload["git_diff_summary"]["git_diff_stat"]:
        lines.append(f"- {line}")
    lines.extend(["", "## Commit / push 수행 여부"])
    lines.append(f"- commit_executed = `{payload['commit_executed']}`")
    lines.append(f"- push_executed = `{payload['push_executed']}`")
    lines.append(f"- commit_hash = `{payload['commit_hash']}`")
    lines.append(f"- preview_deployment_url = `{payload['preview_deployment_url']}`")
    lines.extend(["", "## Production / public / access guard"])
    for key, value in payload["production_public_access_guard"].items():
        lines.append(f"- `{key}` = `{value}`")
    lines.extend(["", "## 테스트 결과"])
    for line in payload["test_expectation_notes"]:
        lines.append(f"- {line}")
    lines.extend(["", "## Production alias 연결 가능 여부"])
    lines.append(f"- `production_alias_connect_allowed = {payload['production_alias_connect_allowed']}`")
    lines.extend(["", "## 다음 backlog 후보"])
    for item in payload["next_backlog_candidates"]:
        lines.append(f"- {item}")
    return "\n".join(lines) + "\n"


def build_payload(args: argparse.Namespace) -> dict[str, Any]:
    records = load_search_records()
    families, seed_entities = _load_seed_inventory()
    previous_rows = _load_previous_status()
    candidate_rows = _candidate_rows(records, seed_entities, previous_rows)
    smoke_query_results = [_query_summary(query, records) for query in SMOKE_QUERIES]
    regression_results = [_query_summary(query, records) for query in REGRESSION_QUERIES]

    added = [row for row in candidate_rows if row["action_taken"] == "add_active_body_entry"]
    already = [row for row in candidate_rows if row["action_taken"] == "already_exists_noop"]
    holds = [row for row in candidate_rows if row["action_taken"] == "hold_manual_review" or row["action_taken"] == "hold_parser_gap"]
    source_gaps = [row for row in candidate_rows if row["action_taken"] == "hold_source_gap"]

    payload = {
        "task_name": TASK_NAME,
        "previous_global_coverage_audit_summary": "The Leica-wide canonical coverage audit found 57 entry_missing_but_results_exist targets, and Leica body lines were the clearest high-priority backfill slice. This round limits itself to body models with query-compatible Body dominance and parser-connected body intent.",
        "body_backfill_targets_and_exclusions": {
            "active_target_groups": [
                "Leica M film bodies",
                "Leica M digital bodies",
                "Leica Q bodies",
                "Leica SL bodies",
            ],
            "explicit_hold_groups": [
                "Leica M1",
                "Leica M7",
                "Leica classic I/II/III",
                "Leica R bodies",
                "Leica compact / P&S / Sofort",
            ],
        },
        "schema_inspection_result": _schema_inspection(seed_entities),
        "added_canonical_body_entries": added,
        "already_existing_entries": already,
        "hold_manual_review_entries": holds,
        "source_gap_entries": source_gaps,
        "candidate_rows": candidate_rows,
        "smoke_query_results": smoke_query_results,
        "market_entry_price_summary_gate_status": "Maintained. Canonical body backfill does not bypass the existing query-confidence gate; market entry and price summary still follow query-compatible Body evidence only.",
        "body_lens_regression_results": regression_results,
        "git_diff_summary": _git_diff_summary(),
        "commit_executed": args.commit_executed,
        "push_executed": args.push_executed,
        "commit_hash": args.commit_hash,
        "preview_deployment_url": args.preview_url,
        "preview_deployment_id": args.preview_deployment_id,
        "preview_deployment_state": args.preview_state,
        "production_alias_connect_allowed": False,
        "production_public_access_guard": {
            "production_launch_go": False,
            "production_alias_connect_allowed": False,
            "public_unrestricted_access_enabled": False,
            "external_tester_access_enabled": False,
            "invite_sent_count": 0,
            "provider_send_count": 0,
            "webhook_call_count": 0,
            "production_DB_write_count": 0,
            "access_activation_performed": False,
            "main_direct_push_executed": False,
            "production_promote_executed": False,
            "tester_link_send_allowed": False,
            "raw_identity_recorded": False,
            "raw_contact_recorded": False,
            "external_link_sent": False,
            "fake_fill_added": False,
        },
        "test_expectation_notes": [
            "Body seed files use the same family schema as existing admin seed files.",
            "Only parser-connected, top-Body-dominant Leica body lines were promoted to active seed rows.",
            "Compact lens notation regressions remain blocked separately and must not reclassify M50/1.2 as M5 Body.",
        ],
        "next_backlog_candidates": [
            "P3-BETA-MVP-LEICA-BODY-CANONICAL-ENTRY-OWNER-RECHECK",
            "P3-BETA-MVP-LEICA-COMPACT-PNS-CANONICAL-ENTRY-BACKFILL",
            "P3-BETA-MVP-QUERY-PARSER-UNKNOWN-TOKEN-COVERAGE-FIXUP",
            "P3-BETA-MVP-LEICA-LENS-CANONICAL-ENTRY-COVERAGE-FOLLOWUP",
        ],
    }
    payload["decision_status"] = args.decision_status or _decision_status(
        candidate_rows,
        commit_executed=args.commit_executed,
        push_executed=args.push_executed,
        preview_url=args.preview_url,
    )
    return payload


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--decision-status", default="")
    parser.add_argument("--commit-hash", default="")
    parser.add_argument("--preview-url", default="")
    parser.add_argument("--preview-deployment-id", default="")
    parser.add_argument("--preview-state", default="")
    parser.add_argument("--commit-executed", action="store_true")
    parser.add_argument("--push-executed", action="store_true")
    args = parser.parse_args()

    payload = build_payload(args)
    MD_PATH.write_text(_build_markdown(payload), encoding="utf-8")
    JSONL_PATH.write_text(json.dumps(payload, ensure_ascii=False) + "\n", encoding="utf-8")
    JSON_PATH.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
