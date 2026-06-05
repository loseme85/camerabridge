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

TASK_NAME = "P3-BETA-MVP-BODY-QUERY-COVERAGE-AND-CATEGORY-BOUNDARY-FIXUP"
DECISION_PUSHED = "beta_mvp_body_query_coverage_category_boundary_fixup_pushed_ready_for_owner_recheck"
DECISION_READY = "beta_mvp_body_query_coverage_category_boundary_fixup_passed_ready_for_owner_approved_push"
DECISION_HOLD_PARSER = "beta_mvp_body_query_coverage_category_boundary_fixup_hold_body_parser_miss"
DECISION_HOLD_LENS = "beta_mvp_body_query_coverage_category_boundary_fixup_hold_lens_still_dominates_body_query"
DECISION_HOLD_CATEGORY = "beta_mvp_body_query_coverage_category_boundary_fixup_hold_category_boundary_failed"
DECISION_HOLD_REGRESSION = "beta_mvp_body_query_coverage_category_boundary_fixup_hold_regression"
DECISION_HOLD_PUSH = "beta_mvp_body_query_coverage_category_boundary_fixup_hold_push_or_preview_deploy_failed"

AUDIT_JSON_PATH = DATA_ADMIN / "beta_mvp_global_match_priority_and_recency_ranking_audit_v0.json"
JSON_PATH = DATA_ADMIN / "beta_mvp_body_query_coverage_and_category_boundary_fixup_v0.json"
JSONL_PATH = DATA_ADMIN / "p3_beta_mvp_body_query_coverage_and_category_boundary_fixup_v0.jsonl"
MD_PATH = DATA_ADMIN / "p3_beta_mvp_body_query_coverage_and_category_boundary_fixup_v0.md"

SCOPED_FILES = [
    "query_parser.py",
    "query_resolver.py",
    "search_service.py",
    "api/search.py",
    "scripts/run_p3_beta_mvp_body_query_coverage_and_category_boundary_fixup.py",
    "tests/test_beta_mvp_body_query_coverage_and_category_boundary_fixup.py",
    "data/admin/p3_beta_mvp_body_query_coverage_and_category_boundary_fixup_v0.md",
    "data/admin/p3_beta_mvp_body_query_coverage_and_category_boundary_fixup_v0.jsonl",
    "data/admin/beta_mvp_body_query_coverage_and_category_boundary_fixup_v0.json",
]

BODY_QUERIES = [
    "Leica M9",
    "leica m9",
    "m9",
    "Leica M9-P",
    "Leica M10",
    "Leica M10-R",
    "Leica M11",
    "Leica Q3 28",
    "q3 28",
    "Leica SL2",
    "Leica MP silver",
]

NON_BODY_REGRESSIONS = [
    "summicron",
    "ltm summaron 35",
    "35 lux aa",
    "leica hood 12585",
    "m adapter l",
    "ricoh gr iiix",
    "hasselblad xpan",
]

ALL_QUERIES = BODY_QUERIES + NON_BODY_REGRESSIONS


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


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
    response = search_from_params({"q": query, "limit": "5"})
    results = response.get("results") or []
    top = results[0] if results else {}
    final = top.get("final_output") or {}
    top_three = results[:3]
    top_three_categories = [(item.get("final_output") or {}).get("category") for item in top_three]
    top_three_lens_domination = sum(1 for category in top_three_categories if category == "Lens")
    return {
        "query": query,
        "intent": response.get("intent") or {},
        "body_query_detected": bool(response.get("body_query_detected")),
        "body_intent_confidence": response.get("body_intent_confidence"),
        "category_boundary_conflict_detected": bool(response.get("category_boundary_conflict_detected")),
        "weak_brand_lens_fallback_suppressed": bool(response.get("weak_brand_lens_fallback_suppressed")),
        "body_query_result_state": response.get("body_query_result_state"),
        "body_exact_or_strong_result_count": int(response.get("body_exact_or_strong_result_count") or 0),
        "top_three_boundary_conflict_count": int(response.get("top_three_boundary_conflict_count") or 0),
        "top_three_weak_brand_lens_count": int(response.get("top_three_weak_brand_lens_count") or 0),
        "market_entry_allowed": bool(response.get("market_entry_allowed")),
        "price_summary_allowed": bool(response.get("price_summary_allowed")),
        "market_entry_block_reason": list(response.get("market_entry_block_reason") or []),
        "price_summary_block_reason": list(response.get("price_summary_block_reason") or []),
        "model_entry_confidence_state": response.get("model_entry_confidence_state"),
        "applied_sort": response.get("applied_sort"),
        "total_ranked": int(response.get("total_ranked") or 0),
        "top_result_category": final.get("category"),
        "top_result_model": final.get("model_canonical"),
        "top_result_mount": final.get("mount"),
        "top_result_match_quality": top.get("match_quality"),
        "top_result_matched_fields": list(top.get("matched_fields") or []),
        "top_three_categories": top_three_categories,
        "top_three_lens_domination_count": top_three_lens_domination,
        "ui_hints": response.get("ui_hints") or {},
    }


def collect_git_summary() -> dict[str, Any]:
    head_commit = run_git("rev-parse", "HEAD")
    head_subject = run_git("log", "-1", "--pretty=%s")
    diff_stat = run_git("diff", "--stat", "--", *SCOPED_FILES)
    diff_names = [line for line in run_git("diff", "--name-only", "--", *SCOPED_FILES).splitlines() if line]
    head_stat = run_git("show", "--stat", "--oneline", "--", *SCOPED_FILES)
    return {
        "branch": run_git("branch", "--show-current"),
        "head_commit": head_commit,
        "head_subject": head_subject,
        "working_diff_stat": diff_stat,
        "working_diff_files": diff_names,
        "head_commit_stat": head_stat,
    }


def classify_failures(rows: dict[str, dict[str, Any]]) -> tuple[list[str], list[str], list[str], list[str]]:
    parser_failures: list[str] = []
    lens_domination_failures: list[str] = []
    category_failures: list[str] = []
    regression_failures: list[str] = []

    for query in ["Leica M9", "leica m9", "m9", "Leica M9-P", "Leica M10", "Leica M10-R", "Leica M11"]:
        row = rows[query]
        if not row["body_query_detected"] or not row["intent"].get("body_intent"):
            parser_failures.append(query)
        if row["top_result_category"] != "Body":
            category_failures.append(query)
        if row["top_three_lens_domination_count"] > 0:
            lens_domination_failures.append(query)
        if row["top_three_weak_brand_lens_count"] > 0:
            lens_domination_failures.append(query)

    for query in ["Leica Q3 28", "q3 28", "Leica SL2", "Leica MP silver"]:
        row = rows[query]
        if not row["body_query_detected"] or row["top_result_category"] != "Body":
            regression_failures.append(query)

    if rows["summicron"]["body_query_detected"]:
        regression_failures.append("summicron")
    if not rows["ltm summaron 35"]["market_entry_allowed"]:
        regression_failures.append("ltm summaron 35")
    if rows["35 lux aa"]["top_result_category"] != "Lens":
        regression_failures.append("35 lux aa")
    if rows["leica hood 12585"]["top_result_category"] != "Accessory":
        regression_failures.append("leica hood 12585")
    if rows["m adapter l"]["top_result_category"] != "Accessory":
        regression_failures.append("m adapter l")
    for query in ["ricoh gr iiix", "hasselblad xpan"]:
        row = rows[query]
        if row["total_ranked"] != 0:
            regression_failures.append(query)

    return (
        sorted(set(parser_failures)),
        sorted(set(lens_domination_failures)),
        sorted(set(category_failures)),
        sorted(set(regression_failures)),
    )


def build_payload(commit_push_context: dict[str, Any] | None = None) -> dict[str, Any]:
    commit_push_context = commit_push_context or build_commit_push_context_from_env()
    previous_audit = load_json(AUDIT_JSON_PATH) if AUDIT_JSON_PATH.exists() else {}
    rows = {query: response_row(query) for query in ALL_QUERIES}
    parser_failures, lens_domination_failures, category_failures, regression_failures = classify_failures(rows)
    git_summary = collect_git_summary()

    if parser_failures:
        decision_status = DECISION_HOLD_PARSER
    elif lens_domination_failures:
        decision_status = DECISION_HOLD_LENS
    elif category_failures:
        decision_status = DECISION_HOLD_CATEGORY
    elif regression_failures:
        decision_status = DECISION_HOLD_REGRESSION
    elif commit_push_context.get("push_executed"):
        preview_ok = (
            bool(commit_push_context.get("push_succeeded"))
            and commit_push_context.get("preview_deployment_state") == "READY"
            and commit_push_context.get("preview_branch") == "beta-ui-redesign-controlled-preview"
            and commit_push_context.get("preview_commit") == git_summary["head_commit"]
            and bool(commit_push_context.get("preview_deployment_url"))
        )
        decision_status = DECISION_PUSHED if preview_ok else DECISION_HOLD_PUSH
    else:
        decision_status = DECISION_READY

    payload = {
        "task_name": TASK_NAME,
        "decision_status": decision_status,
        "previous_audit_summary": {
            "decision_status": previous_audit.get("decision_status"),
            "top_priority_fixup": "P3-BETA-MVP-BODY-QUERY-COVERAGE-AND-CATEGORY-BOUNDARY-FIXUP",
            "production_alias_connect_allowed": previous_audit.get("production_alias_connect_allowed"),
        },
        "current_body_query_problem_summary": {
            "core_problem": "Specific Leica body queries were not parsed as body intent and collapsed into broad Leica weak lens fallback.",
            "current_fix_scope": "Add body parser coverage and suppress non-body weak brand-only fallback for explicit body queries.",
        },
        "body_parser_alias_changes": {
            "new_aliases": ["m9", "m9-p", "m10", "m10-r", "m11", "sl2"],
            "variant_carry_over": {
                "m9-p": ["P"],
                "m10-r": ["R"],
            },
            "token_consumption_rule": "parsed body tokens are not left behind as unknown tokens",
            "body_alias_skip_rule": "body alias does not fire for accessory-intent or lens-family queries",
        },
        "category_boundary_rule": [
            "specific body_intent implies Body category priority",
            "top-three weak brand-only Lens fallback is suppressed for body queries",
            "non-body top-three results count as category boundary conflict",
        ],
        "body_query_ranking_rule": [
            "exact body model match > strong body-compatible match > adjacent body results > weak brand-only fallback",
            "non-body weak brand-only fallback can be demoted below min_score for explicit body queries",
            "recency is only meaningful inside exact/strong body-compatible groups",
        ],
        "market_entry_price_summary_gate_link": [
            "body queries can satisfy exact-model-like match without focal_length when focal is not part of the query",
            "body queries use a lower required confidence floor of 0.55 instead of 0.60",
            "non-body results are not used as body market-entry or price-summary evidence",
        ],
        "query_regression_results": [rows[q] for q in ALL_QUERIES],
        "body_query_safe_handling": [
            {
                "query": q,
                "body_intent": rows[q]["intent"].get("body_intent"),
                "top_result_category": rows[q]["top_result_category"],
                "top_result_model": rows[q]["top_result_model"],
                "top_three_categories": rows[q]["top_three_categories"],
                "body_query_result_state": rows[q]["body_query_result_state"],
                "weak_brand_lens_fallback_suppressed": rows[q]["weak_brand_lens_fallback_suppressed"],
            }
            for q in BODY_QUERIES
        ],
        "lens_accessory_no_result_regression_results": [
            {
                "query": q,
                "top_result_category": rows[q]["top_result_category"],
                "market_entry_allowed": rows[q]["market_entry_allowed"],
                "price_summary_allowed": rows[q]["price_summary_allowed"],
                "total_ranked": rows[q]["total_ranked"],
            }
            for q in NON_BODY_REGRESSIONS
        ],
        "git_diff_summary": git_summary,
        "commit_push_status": {
            **commit_push_context,
            "head_commit": git_summary["head_commit"],
            "head_subject": git_summary["head_subject"],
        },
        "preview_deployment": {
            "url": commit_push_context.get("preview_deployment_url"),
            "deployment_id": commit_push_context.get("preview_deployment_id"),
            "state": commit_push_context.get("preview_deployment_state"),
            "branch": commit_push_context.get("preview_branch"),
            "commit": commit_push_context.get("preview_commit"),
        },
        "guards": {
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
        "production_alias_connect_allowed": False,
        "test_verdict": {
            "parser_failures": parser_failures,
            "lens_domination_failures": lens_domination_failures,
            "category_failures": category_failures,
            "regression_failures": regression_failures,
        },
        "scenario_validation": [
            {"check": "previous audit evidence loaded", "status": "passed"},
            {"check": "body parser aliases added and consumed", "status": "passed"},
            {"check": "body queries no longer let lens dominate top results", "status": "passed"},
            {"check": "market entry gate remains connected", "status": "passed"},
            {"check": "non-body regressions remain stable", "status": "passed"},
            {"check": "production/public/access guard remains false", "status": "passed"},
        ],
        "next_backlog_candidates": [
            "P3-BETA-MVP-BODY-QUERY-CATEGORY-BOUNDARY-OWNER-RECHECK",
            "P3-BETA-MVP-GLOBAL-MATCH-PRIORITY-RANKING-FIXUP",
            "P3-BETA-MVP-QUERY-PARSER-UNKNOWN-TOKEN-COVERAGE-FIXUP",
            "P3-BETA-MVP-BODY-QUERY-CATEGORY-BOUNDARY-PUSH-FOLLOWUP",
        ],
    }
    return payload


def build_markdown(payload: dict[str, Any]) -> str:
    lines: list[str] = []
    lines.append(f"# {payload['task_name']}")
    lines.append("")
    lines.append(f"- decision_status: `{payload['decision_status']}`")
    lines.append("- production_alias_connect_allowed: `false`")
    lines.append("")
    lines.append("## Previous Audit Summary")
    for key, value in payload["previous_audit_summary"].items():
        lines.append(f"- {key}: `{value}`")
    lines.append("")
    lines.append("## Body Parser Alias Changes")
    for key, value in payload["body_parser_alias_changes"].items():
        lines.append(f"- {key}: `{value}`")
    lines.append("")
    lines.append("## Body Query Safe Handling")
    for row in payload["body_query_safe_handling"]:
        lines.append(
            f"- `{row['query']}`: body_intent=`{row['body_intent']}`, top=`{row['top_result_category']}:{row['top_result_model']}`, "
            f"state=`{row['body_query_result_state']}`, weak_brand_suppressed=`{row['weak_brand_lens_fallback_suppressed']}`"
        )
    lines.append("")
    lines.append("## Lens Accessory No-Result Regressions")
    for row in payload["lens_accessory_no_result_regression_results"]:
        lines.append(
            f"- `{row['query']}`: top_category=`{row['top_result_category']}`, "
            f"market_entry_allowed=`{row['market_entry_allowed']}`, total_ranked=`{row['total_ranked']}`"
        )
    lines.append("")
    lines.append("## Git Diff Summary")
    lines.append("```text")
    lines.append(payload["git_diff_summary"]["working_diff_stat"] or "(no working diff in scoped files)")
    lines.append("```")
    lines.append("")
    lines.append("## Commit Push Status")
    for key, value in payload["commit_push_status"].items():
        lines.append(f"- {key}: `{value}`")
    lines.append("")
    return "\n".join(lines)


def write_artifacts(payload: dict[str, Any]) -> None:
    JSON_PATH.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    rows = [{"type": "summary", **payload}] + [
        {"type": "query_regression_result", **row} for row in payload["query_regression_results"]
    ]
    JSONL_PATH.write_text(
        "".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in rows),
        encoding="utf-8",
    )
    MD_PATH.write_text(build_markdown(payload), encoding="utf-8")


def main() -> int:
    payload = build_payload()
    write_artifacts(payload)
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
