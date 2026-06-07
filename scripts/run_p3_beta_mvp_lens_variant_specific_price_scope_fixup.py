from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DATA_ADMIN = ROOT / "data" / "admin"

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from api.search import search_from_params

TASK_NAME = "P3-BETA-MVP-LENS-VARIANT-SPECIFIC-PRICE-SCOPE-FIXUP"
DECISION_PUSHED = "lens_variant_specific_price_scope_fixup_pushed_ready_for_owner_recheck"
DECISION_READY = "lens_variant_specific_price_scope_fixup_passed_ready_for_owner_approved_push"
DECISION_HOLD_UNSAFE = "lens_variant_specific_price_scope_fixup_hold_unsafe_broader_family_price_as_exact"
DECISION_HOLD_READY = "lens_variant_specific_price_scope_fixup_hold_exact_variant_ready_regressed"
DECISION_HOLD_BOUNDARY = "lens_variant_specific_price_scope_fixup_hold_boundary_conflict_price_opened"
DECISION_HOLD_BODY = "lens_variant_specific_price_scope_fixup_hold_body_lens_regression"
DECISION_HOLD_PUSH = "lens_variant_specific_price_scope_fixup_hold_push_or_preview_deploy_failed"

JSON_PATH = DATA_ADMIN / "lens_variant_specific_price_scope_fixup_v0.json"
JSONL_PATH = DATA_ADMIN / "p3_beta_mvp_lens_variant_specific_price_scope_fixup_v0.jsonl"
MD_PATH = DATA_ADMIN / "p3_beta_mvp_lens_variant_specific_price_scope_fixup_v0.md"

SCOPED_FILES = [
    "api/search.py",
    "app/templates/index.html",
    "index.html",
    "scripts/run_p3_beta_mvp_lens_variant_specific_price_scope_fixup.py",
    "tests/test_beta_mvp_lens_variant_specific_price_scope_fixup.py",
    "data/admin/p3_beta_mvp_lens_variant_specific_price_scope_fixup_v0.md",
    "data/admin/p3_beta_mvp_lens_variant_specific_price_scope_fixup_v0.jsonl",
    "data/admin/lens_variant_specific_price_scope_fixup_v0.json",
]

EXACT_VARIANT_READY = [
    "Summicron 35 8-element",
    "Summicron 50 rigid",
]

SEARCH_CONFIDENCE_MISMATCH = [
    "Summilux-M 50 ASPH",
]

VARIANT_DATA_LIMITED = [
    "Leica Summilux-M 50mm f1.4 3세대",
    "Summilux-M 50 pre-ASPH",
    "35 lux aa",
    "Noctilux 50 f1 E60",
]
PROMOTED_EXACT_VARIANT = ["Summilux 50 3rd generation"]

BROADER_FAMILY_ONLY = [
    "Noctilux 50 0.95",
    "Summaron 35 2.8",
]

BOUNDARY_LOCKED = [
    "Summicron-M 35 ASPH",
    "APO-Summicron-SL 90",
]

REGRESSION_QUERIES = [
    "ltm summaron 35",
    "Elmarit-R 28",
    "M50/1.2",
    "Leica M9",
    "Leica M10",
    "Leica M11",
]

ALL_QUERIES = SEARCH_CONFIDENCE_MISMATCH + EXACT_VARIANT_READY + PROMOTED_EXACT_VARIANT + VARIANT_DATA_LIMITED + BROADER_FAMILY_ONLY + BOUNDARY_LOCKED + REGRESSION_QUERIES


def run_git(*args: str) -> str:
    try:
        completed = subprocess.run(
            ["git", *args],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
    except subprocess.CalledProcessError as exc:
        return (exc.stdout or exc.stderr or "").strip()
    return completed.stdout.strip()


def build_commit_push_context_from_env() -> dict[str, Any]:
    return {
        "commit_executed": os.environ.get("P3_COMMIT_EXECUTED", "false").lower() == "true",
        "push_executed": os.environ.get("P3_PUSH_EXECUTED", "false").lower() == "true",
        "push_succeeded": os.environ.get("P3_PUSH_SUCCEEDED", "false").lower() == "true",
        "preview_deployment_url": os.environ.get("P3_PREVIEW_URL"),
        "preview_deployment_id": os.environ.get("P3_PREVIEW_DEPLOYMENT_ID"),
        "preview_deployment_state": os.environ.get("P3_PREVIEW_STATE"),
        "preview_branch": os.environ.get("P3_PREVIEW_BRANCH"),
        "preview_commit": os.environ.get("P3_PREVIEW_COMMIT"),
    }


def response_row(query: str) -> dict[str, Any]:
    response = search_from_params({"q": query, "limit": "10"})
    results = response.get("results") or []
    top = results[0] if results else {}
    final = top.get("final_output") or {}
    display = top.get("display_output") or {}
    return {
        "query": query,
        "market_entry_allowed": bool(response.get("market_entry_allowed")),
        "price_summary_allowed": bool(response.get("price_summary_allowed")),
        "price_scope": response.get("price_scope"),
        "price_scope_label": response.get("price_scope_label"),
        "price_scope_confidence_state": response.get("price_scope_confidence_state"),
        "price_summary_band": response.get("price_summary_band"),
        "broader_reference_allowed": bool(response.get("broader_reference_allowed")),
        "broader_reference_label": response.get("broader_reference_label"),
        "broader_reference_band": response.get("broader_reference_band"),
        "variant_tokens_detected": list(response.get("variant_tokens_detected") or []),
        "exact_variant_result_count": int(response.get("exact_variant_result_count") or 0),
        "exact_variant_priced_count": int(response.get("exact_variant_priced_count") or 0),
        "exact_base_model_result_count": int(response.get("exact_base_model_result_count") or 0),
        "exact_base_model_priced_count": int(response.get("exact_base_model_priced_count") or 0),
        "broader_family_result_count": int(response.get("broader_family_result_count") or 0),
        "broader_family_priced_count": int(response.get("broader_family_priced_count") or 0),
        "price_summary_block_reason": list(response.get("price_summary_block_reason") or []),
        "current_ui_label_safe": bool(response.get("current_ui_label_safe")),
        "top_result_category": final.get("category"),
        "top_display_category": display.get("display_category"),
        "top_result_model": final.get("model_canonical"),
        "top_display_model": display.get("display_model"),
        "total_ranked": int(response.get("total_ranked") or 0),
    }


def classify_failures(rows: dict[str, dict[str, Any]]) -> tuple[list[str], list[str], list[str], list[str]]:
    unsafe: list[str] = []
    ready_regressions: list[str] = []
    boundary_failures: list[str] = []
    body_lens_regressions: list[str] = []

    for query in EXACT_VARIANT_READY:
        row = rows[query]
        if not row["price_summary_allowed"] or row["price_scope"] != "exact_variant":
            ready_regressions.append(query)
        if row["price_scope_label"] != "Exact variant price":
            ready_regressions.append(query)

    for query in SEARCH_CONFIDENCE_MISMATCH:
        row = rows[query]
        if row["price_summary_allowed"]:
            unsafe.append(query)
        if row["price_scope_label"] != "Price summary locked":
            unsafe.append(query)

    for query in VARIANT_DATA_LIMITED:
        row = rows[query]
        if row["price_summary_allowed"]:
            unsafe.append(query)
        if row["price_scope_label"] not in {"Exact variant price data limited", "Price summary locked"}:
            unsafe.append(query)
        if not row["current_ui_label_safe"]:
            unsafe.append(query)

    promoted = rows["Summilux 50 3rd generation"]
    if not promoted["price_summary_allowed"] or promoted["price_scope"] != "exact_variant":
        ready_regressions.append("Summilux 50 3rd generation")

    for query in BROADER_FAMILY_ONLY:
        row = rows[query]
        if row["price_summary_allowed"]:
            unsafe.append(query)
        if row["price_scope_label"] not in {"Broader family reference", "Price summary locked"}:
            unsafe.append(query)
        if row["broader_reference_allowed"] and row["broader_reference_label"] not in {"Broader family reference", "Exact base model reference"}:
            unsafe.append(query)

    for query in BOUNDARY_LOCKED:
        row = rows[query]
        if row["price_summary_allowed"] or row["price_scope"] != "blocked_boundary_conflict":
            boundary_failures.append(query)

    m5012 = rows["M50/1.2"]
    if m5012["top_display_category"] == "Body" or m5012["top_display_model"] == "M5":
        body_lens_regressions.append("M50/1.2")

    for query in ["Leica M9", "Leica M10", "Leica M11"]:
        row = rows[query]
        if row["top_display_category"] != "Body":
            body_lens_regressions.append(query)

    for query in ["ltm summaron 35", "Elmarit-R 28"]:
        row = rows[query]
        if not row["price_summary_allowed"] or row["price_scope"] != "exact_base_model":
            body_lens_regressions.append(query)

    return (
        sorted(set(unsafe)),
        sorted(set(ready_regressions)),
        sorted(set(boundary_failures)),
        sorted(set(body_lens_regressions)),
    )


def collect_git_summary() -> dict[str, Any]:
    return {
        "branch": run_git("branch", "--show-current"),
        "head_commit": run_git("rev-parse", "HEAD"),
        "head_subject": run_git("log", "-1", "--pretty=%s"),
        "working_diff_stat": run_git("diff", "--stat", "--", *SCOPED_FILES),
        "working_diff_files": [line for line in run_git("diff", "--name-only", "--", *SCOPED_FILES).splitlines() if line],
    }


def build_payload(push_context: dict[str, Any] | None = None) -> dict[str, Any]:
    rows = {query: response_row(query) for query in ALL_QUERIES}
    unsafe, ready_regressions, boundary_failures, body_lens_regressions = classify_failures(rows)

    decision_status = DECISION_READY
    if unsafe:
        decision_status = DECISION_HOLD_UNSAFE
    elif ready_regressions:
        decision_status = DECISION_HOLD_READY
    elif boundary_failures:
        decision_status = DECISION_HOLD_BOUNDARY
    elif body_lens_regressions:
        decision_status = DECISION_HOLD_BODY

    push_context = push_context or build_commit_push_context_from_env()
    if push_context.get("push_executed") and not push_context.get("push_succeeded"):
        decision_status = DECISION_HOLD_PUSH
    elif (
        decision_status == DECISION_READY
        and push_context.get("commit_executed")
        and push_context.get("push_executed")
        and push_context.get("push_succeeded")
        and push_context.get("preview_deployment_url")
    ):
        decision_status = DECISION_PUSHED

    guards = {
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
    }

    return {
        "task_name": TASK_NAME,
        "decision_status": decision_status,
        "previous_audit_summary": {
            "decision_status": "lens_variant_specific_price_scope_policy_audit_completed_ready_for_fixup",
            "exact_variant_ready_queries": EXACT_VARIANT_READY,
            "search_confidence_mismatch_queries": SEARCH_CONFIDENCE_MISMATCH,
            "exact_variant_data_limited_queries": VARIANT_DATA_LIMITED,
            "broader_family_only_queries": BROADER_FAMILY_ONLY,
            "blocked_boundary_conflict_queries": BOUNDARY_LOCKED,
        },
        "implemented_price_scope_contract": {
            "entry_scope_values": ["parent_model", "lens_family", "exact_variant", "hold_conflict"],
            "price_scope_values": [
                "exact_variant",
                "exact_base_model",
                "broader_model_family",
                "insufficient_exact_data",
                "blocked_boundary_conflict",
                "blocked_weak_only",
            ],
            "price_scope_labels": [
                "Exact variant price",
                "Exact base model price",
                "Broader family reference",
                "Exact variant price data limited",
                "Price summary locked",
            ],
        },
        "query_results": [rows[q] for q in ALL_QUERIES],
        "exact_variant_ready_results": [rows[q] for q in EXACT_VARIANT_READY],
        "exact_variant_data_limited_results": [rows[q] for q in VARIANT_DATA_LIMITED],
        "broader_family_reference_results": [rows[q] for q in BROADER_FAMILY_ONLY],
        "boundary_conflict_results": [rows[q] for q in BOUNDARY_LOCKED],
        "body_lens_regression_results": [rows[q] for q in REGRESSION_QUERIES],
        "ui_copy_labels": [
            "Exact variant price",
            "Exact base model price",
            "Broader family reference",
            "Exact variant price data limited",
            "Price summary locked",
        ],
        "test_verdict": {
            "unsafe_broader_family_price_as_exact": unsafe,
            "exact_variant_ready_regressions": ready_regressions,
            "boundary_conflict_price_opened": boundary_failures,
            "body_lens_regressions": body_lens_regressions,
        },
        "git_diff_summary": collect_git_summary(),
        "commit_push_context": push_context,
        "preview_deployment_url": push_context.get("preview_deployment_url"),
        "preview_deployment_id": push_context.get("preview_deployment_id"),
        "preview_deployment_state": push_context.get("preview_deployment_state"),
        "preview_branch": push_context.get("preview_branch"),
        "preview_commit": push_context.get("preview_commit"),
        "guards": guards,
        "production_alias_connect_allowed": False,
        "next_backlog_candidates": [
            "P3-BETA-MVP-LENS-VARIANT-SPECIFIC-PRICE-SCOPE-OWNER-RECHECK",
            "P3-BETA-MVP-LENS-VARIANT-TOKEN-PARSER-COVERAGE-FIXUP",
            "P3-BETA-MVP-LENS-MODEL-DETAIL-PAGE-PROFILE-SCHEMA-CONTRACT",
            "P3-BETA-MVP-LEICA-LENS-CANONICAL-ENTRY-COVERAGE-FOLLOWUP",
        ],
    }


def write_artifacts(payload: dict[str, Any]) -> None:
    JSON_PATH.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    JSONL_PATH.write_text(json.dumps(payload, ensure_ascii=False) + "\n", encoding="utf-8")

    lines = [
        f"# {TASK_NAME}",
        "",
        f"- decision_status: `{payload['decision_status']}`",
        "- previous audit: `lens_variant_specific_price_scope_policy_audit_completed_ready_for_fixup`",
        f"- preview_deployment_url: `{payload.get('preview_deployment_url')}`",
        f"- preview_deployment_state: `{payload.get('preview_deployment_state')}`",
        f"- preview_commit: `{payload.get('preview_commit')}`",
        "",
        "## Exact Variant Ready",
    ]
    for row in payload["exact_variant_ready_results"]:
        lines.append(
            f"- `{row['query']}` -> `{row['price_scope_label']}` / allowed={row['price_summary_allowed']} / band={row['price_summary_band']}"
        )
    lines.extend(["", "## Exact Variant Data Limited"])
    for row in payload["exact_variant_data_limited_results"]:
        lines.append(
            f"- `{row['query']}` -> `{row['price_scope_label']}` / broader_reference={row['broader_reference_allowed']} / band={row['broader_reference_band']}"
        )
    lines.extend(["", "## Broader Family Reference"])
    for row in payload["broader_family_reference_results"]:
        lines.append(
            f"- `{row['query']}` -> `{row['price_scope_label']}` / broader_reference={row['broader_reference_allowed']}"
        )
    lines.extend(["", "## Boundary Conflict"])
    for row in payload["boundary_conflict_results"]:
        lines.append(
            f"- `{row['query']}` -> `{row['price_scope_label']}` / allowed={row['price_summary_allowed']}"
        )
    lines.extend(
        [
            "",
            "## Body/Lens Regression",
        ]
    )
    for row in payload["body_lens_regression_results"]:
        lines.append(
            f"- `{row['query']}` -> display_category={row['top_display_category']} / price_scope={row['price_scope']}"
        )
    MD_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    payload = build_payload()
    write_artifacts(payload)
    print(json.dumps({"decision_status": payload["decision_status"]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
