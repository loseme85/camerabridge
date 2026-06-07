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

TASK_NAME = "P3-BETA-MVP-LENS-PRICE-SCOPE-SEARCH-CONFIDENCE-ALIGNMENT-FIXUP"
DECISION_PUSHED = "lens_price_scope_search_confidence_alignment_fixup_pushed_ready_for_owner_recheck"
DECISION_READY = "lens_price_scope_search_confidence_alignment_fixup_passed_ready_for_owner_approved_push"
DECISION_HOLD_EXACT_ON_WEAK = "lens_price_scope_search_confidence_alignment_fixup_hold_exact_price_opens_on_weak_fallback"
DECISION_HOLD_READY = "lens_price_scope_search_confidence_alignment_fixup_hold_exact_variant_ready_regressed"
DECISION_HOLD_BOUNDARY = "lens_price_scope_search_confidence_alignment_fixup_hold_boundary_conflict_price_opened"
DECISION_HOLD_BODY = "lens_price_scope_search_confidence_alignment_fixup_hold_body_lens_regression"
DECISION_HOLD_PUSH = "lens_price_scope_search_confidence_alignment_fixup_hold_push_or_preview_deploy_failed"

JSON_PATH = DATA_ADMIN / "lens_price_scope_search_confidence_alignment_fixup_v0.json"
JSONL_PATH = DATA_ADMIN / "p3_beta_mvp_lens_price_scope_search_confidence_alignment_fixup_v0.jsonl"
MD_PATH = DATA_ADMIN / "p3_beta_mvp_lens_price_scope_search_confidence_alignment_fixup_v0.md"

SCOPED_FILES = [
    "api/search.py",
    "app/templates/index.html",
    "index.html",
    "scripts/run_p3_beta_mvp_lens_price_scope_search_confidence_alignment_fixup.py",
    "tests/test_beta_mvp_lens_price_scope_search_confidence_alignment_fixup.py",
    "tests/test_beta_mvp_lens_variant_specific_price_scope_fixup.py",
    "data/admin/p3_beta_mvp_lens_price_scope_search_confidence_alignment_fixup_v0.md",
    "data/admin/p3_beta_mvp_lens_price_scope_search_confidence_alignment_fixup_v0.jsonl",
    "data/admin/lens_price_scope_search_confidence_alignment_fixup_v0.json",
]

SEARCH_CONFIDENCE_MISMATCH = ["Summilux-M 50 ASPH"]
EXACT_VARIANT_READY = ["Summicron 35 8-element", "Summicron 50 rigid"]
VARIANT_DATA_LIMITED = [
    "Leica Summilux-M 50mm f1.4 3세대",
    "35 lux aa",
    "Noctilux 50 f1 E60",
]
PROMOTED_EXACT_VARIANT = ["Summilux 50 3rd generation"]
BOUNDARY_LOCKED = ["APO-Summicron-SL 90"]
REGRESSIONS = ["M50/1.2", "Leica M9", "Leica M10", "Leica M11", "ltm summaron 35"]
ALL_QUERIES = SEARCH_CONFIDENCE_MISMATCH + EXACT_VARIANT_READY + PROMOTED_EXACT_VARIANT + VARIANT_DATA_LIMITED + BOUNDARY_LOCKED + REGRESSIONS


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
        "search_confidence_state": response.get("search_confidence_state"),
        "top_result_compatibility": response.get("top_result_compatibility"),
        "exact_or_strong_visible_result_count": int(response.get("exact_or_strong_visible_result_count") or 0),
        "weak_only_fallback_detected": bool(response.get("weak_only_fallback_detected")),
        "third_party_top_domination_detected": bool(response.get("third_party_top_domination_detected")),
        "price_scope_search_aligned": bool(response.get("price_scope_search_aligned")),
        "price_scope_search_alignment_reason": list(response.get("price_scope_search_alignment_reason") or []),
        "price_summary_block_reason": list(response.get("price_summary_block_reason") or []),
        "price_summary_band": response.get("price_summary_band"),
        "broader_reference_allowed": bool(response.get("broader_reference_allowed")),
        "broader_reference_label": response.get("broader_reference_label"),
        "broader_reference_band": response.get("broader_reference_band"),
        "exact_variant_priced_count": int(response.get("exact_variant_priced_count") or 0),
        "top_result_category": final.get("category"),
        "top_result_model": final.get("model_canonical"),
        "top_display_category": display.get("display_category"),
        "top_display_model": display.get("display_model"),
    }


def classify_failures(rows: dict[str, dict[str, Any]]) -> tuple[list[str], list[str], list[str], list[str]]:
    exact_on_weak: list[str] = []
    ready_regressions: list[str] = []
    boundary_failures: list[str] = []
    body_lens_regressions: list[str] = []

    row = rows["Summilux-M 50 ASPH"]
    if row["price_summary_allowed"] or row["price_scope_label"] == "Exact variant price":
        exact_on_weak.append("Summilux-M 50 ASPH")
    if row["search_confidence_state"] != "weak_only_fallback":
        exact_on_weak.append("Summilux-M 50 ASPH")
    if row["price_scope_search_aligned"]:
        exact_on_weak.append("Summilux-M 50 ASPH")

    for query in EXACT_VARIANT_READY:
        item = rows[query]
        if not item["price_summary_allowed"] or item["price_scope"] != "exact_variant":
            ready_regressions.append(query)
        if item["top_result_compatibility"] != "exact_variant_strong":
            ready_regressions.append(query)

    promoted = rows["Summilux 50 3rd generation"]
    if not promoted["price_summary_allowed"] or promoted["price_scope"] != "exact_variant":
        ready_regressions.append("Summilux 50 3rd generation")

    for query in BOUNDARY_LOCKED:
        item = rows[query]
        if item["price_summary_allowed"] or item["price_scope"] != "blocked_boundary_conflict":
            boundary_failures.append(query)

    for query in ["M50/1.2"]:
        item = rows[query]
        if item["top_display_category"] == "Body" or item["top_display_model"] == "M5":
            body_lens_regressions.append(query)

    for query in ["Leica M9", "Leica M10", "Leica M11"]:
        item = rows[query]
        if item["top_display_category"] != "Body":
            body_lens_regressions.append(query)

    if rows["ltm summaron 35"]["price_scope"] != "exact_base_model" or not rows["ltm summaron 35"]["price_summary_allowed"]:
        body_lens_regressions.append("ltm summaron 35")

    return (
        sorted(set(exact_on_weak)),
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
    exact_on_weak, ready_regressions, boundary_failures, body_lens_regressions = classify_failures(rows)

    decision_status = DECISION_READY
    if exact_on_weak:
        decision_status = DECISION_HOLD_EXACT_ON_WEAK
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
        "owner_recheck_hold_reason": "Summilux-M 50 ASPH exposed exact variant price while visible search results stayed weak-only and third-party-dominated.",
        "query_results": [rows[q] for q in ALL_QUERIES],
        "search_confidence_alignment_policy": {
            "requires_not_weak_only": True,
            "requires_exact_or_strong_visible_result": True,
            "blocks_third_party_top_domination": True,
            "blocks_boundary_conflict": True,
            "requires_exact_variant_priced_evidence_for_variant_queries": True,
            "allows_broader_reference_only_when_clearly_labeled": True,
        },
        "exact_variant_ready_results": [rows[q] for q in EXACT_VARIANT_READY],
        "search_confidence_mismatch_results": [rows[q] for q in SEARCH_CONFIDENCE_MISMATCH],
        "exact_variant_data_limited_results": [rows[q] for q in VARIANT_DATA_LIMITED],
        "boundary_conflict_results": [rows[q] for q in BOUNDARY_LOCKED],
        "body_lens_regression_results": [rows[q] for q in REGRESSIONS],
        "stale_market_entry_confidence_test_alignment": {
            "updated_prior_price_scope_fixup_script": True,
            "updated_prior_price_scope_fixup_test": True,
            "reason": "Summilux-M 50 ASPH is no longer treated as exact-variant-ready when visible search confidence is weak-only.",
        },
        "test_verdict": {
            "exact_price_opens_on_weak_fallback": exact_on_weak,
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
            "P3-BETA-MVP-LENS-PRICE-SCOPE-SEARCH-CONFIDENCE-ALIGNMENT-OWNER-RECHECK",
            "P3-BETA-MVP-STALE-MARKET-ENTRY-CONFIDENCE-TEST-ALIGNMENT",
            "P3-BETA-MVP-LENS-VARIANT-TOKEN-PARSER-COVERAGE-FIXUP",
        ],
    }


def write_artifacts(payload: dict[str, Any]) -> None:
    JSON_PATH.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    JSONL_PATH.write_text(json.dumps(payload, ensure_ascii=False) + "\n", encoding="utf-8")
    lines = [
        f"# {TASK_NAME}",
        "",
        f"- decision_status: `{payload['decision_status']}`",
        f"- owner_recheck_hold_reason: {payload['owner_recheck_hold_reason']}",
        f"- preview_deployment_url: `{payload.get('preview_deployment_url')}`",
        "",
        "## Search Confidence Mismatch",
    ]
    for row in payload["search_confidence_mismatch_results"]:
        lines.append(
            f"- `{row['query']}` -> allowed={row['price_summary_allowed']} / scope={row['price_scope']} / search_confidence={row['search_confidence_state']} / top={row['top_result_compatibility']}"
        )
    lines.extend(["", "## Exact Variant Ready"])
    for row in payload["exact_variant_ready_results"]:
        lines.append(
            f"- `{row['query']}` -> allowed={row['price_summary_allowed']} / scope={row['price_scope']} / top={row['top_result_compatibility']}"
        )
    lines.extend(["", "## Exact Variant Data Limited"])
    for row in payload["exact_variant_data_limited_results"]:
        lines.append(
            f"- `{row['query']}` -> label={row['price_scope_label']} / broader_reference={row['broader_reference_allowed']}"
        )
    MD_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    payload = build_payload()
    write_artifacts(payload)
    print(json.dumps({"decision_status": payload["decision_status"]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
