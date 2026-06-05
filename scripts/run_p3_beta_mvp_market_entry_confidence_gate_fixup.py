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

TASK_NAME = "P3-BETA-MVP-MARKET-ENTRY-CONFIDENCE-GATE-FIXUP"
DECISION_PUSHED = "beta_mvp_market_entry_confidence_gate_fixup_pushed_ready_for_owner_recheck"
DECISION_READY = "beta_mvp_market_entry_confidence_gate_fixup_passed_ready_for_owner_approved_push"
DECISION_HOLD_GATE = "beta_mvp_market_entry_confidence_gate_fixup_hold_gate_incomplete"
DECISION_HOLD_MARKET = "beta_mvp_market_entry_confidence_gate_fixup_hold_wrong_market_entry_still_renders"
DECISION_HOLD_PRICE = "beta_mvp_market_entry_confidence_gate_fixup_hold_price_summary_unsafe"
DECISION_HOLD_REGRESSION = "beta_mvp_market_entry_confidence_gate_fixup_hold_regression"
DECISION_HOLD_PUSH = "beta_mvp_market_entry_confidence_gate_fixup_hold_push_or_preview_deploy_failed"

AUDIT_JSON_PATH = DATA_ADMIN / "beta_mvp_lens_family_boundary_and_market_entry_anchor_audit_v0.json"
JSON_PATH = DATA_ADMIN / "beta_mvp_market_entry_confidence_gate_fixup_v0.json"
JSONL_PATH = DATA_ADMIN / "p3_beta_mvp_market_entry_confidence_gate_fixup_v0.jsonl"
MD_PATH = DATA_ADMIN / "p3_beta_mvp_market_entry_confidence_gate_fixup_v0.md"

APP_HTML_PATH = ROOT / "app" / "templates" / "index.html"
ROOT_HTML_PATH = ROOT / "index.html"

SCOPED_FILES = [
    "api/search.py",
    "search_ui_hints.py",
    "app/templates/index.html",
    "index.html",
    "scripts/run_p3_beta_mvp_market_entry_confidence_gate_fixup.py",
    "tests/test_beta_mvp_market_entry_confidence_gate_fixup.py",
    "data/admin/p3_beta_mvp_market_entry_confidence_gate_fixup_v0.md",
    "data/admin/p3_beta_mvp_market_entry_confidence_gate_fixup_v0.jsonl",
    "data/admin/beta_mvp_market_entry_confidence_gate_fixup_v0.json",
]

BLOCKING_QUERIES = [
    "Summicron-M 35 ASPH",
    "Leica M 35mm f2 Summicron ASPH",
    "35 Summicron-M ASPH",
    "APO-Summicron-M 35 ASPH",
    "apo 35 summicron",
    "APO-Summicron-SL 50",
    "APO-Summicron-SL 90",
    "Summicron-M 50",
    "summicron",
    "leica lens",
]

REGRESSION_QUERIES = [
    "ltm summaron 35",
    "35 lux aa",
    "q3 28",
    "ricoh gr iiix",
    "hasselblad xpan",
]

ALL_QUERIES = BLOCKING_QUERIES + REGRESSION_QUERIES


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
    ui_hints = response.get("ui_hints") or {}
    return {
        "query": query,
        "market_entry_allowed": bool(response.get("market_entry_allowed")),
        "market_entry_block_reason": list(response.get("market_entry_block_reason") or []),
        "price_summary_allowed": bool(response.get("price_summary_allowed")),
        "price_summary_block_reason": list(response.get("price_summary_block_reason") or []),
        "model_entry_confidence_state": response.get("model_entry_confidence_state"),
        "boundary_conflict_detected": bool(response.get("boundary_conflict_detected")),
        "dangerous_unknown_family_token_detected": bool(
            response.get("dangerous_unknown_family_token_detected")
        ),
        "dangerous_unknown_family_tokens": list(response.get("dangerous_unknown_family_tokens") or []),
        "weak_only_fallback_detected": bool(response.get("weak_only_fallback_detected")),
        "status": 200,
        "ui_state": (
            "broad_query_refinement_rendered"
            if ui_hints.get("needs_disambiguation")
            else "no_result_card_rendered"
            if not results
            else "search_results_rendered"
        ),
        "total_ranked": int(response.get("total_ranked") or 0),
        "top_result_model": final.get("model_canonical"),
        "top_result_mount": final.get("mount"),
        "top_result_category": final.get("category"),
        "top_result_match_quality": top.get("match_quality"),
        "top_result_matched_fields": list(top.get("matched_fields") or []),
        "market_entry_title": response.get("market_entry_title"),
        "price_summary_band": response.get("price_summary_band"),
        "needs_disambiguation": bool(ui_hints.get("needs_disambiguation")),
        "ambiguity_type": ui_hints.get("ambiguity_type"),
        "expected_query_family": response.get("expected_query_family"),
        "expected_query_mount": response.get("expected_query_mount"),
    }


def classify_failures(rows: dict[str, dict[str, Any]]) -> tuple[list[str], list[str], list[str]]:
    market_failures: list[str] = []
    price_failures: list[str] = []
    regression_failures: list[str] = []

    for query in BLOCKING_QUERIES:
        row = rows[query]
        if row["market_entry_allowed"]:
            market_failures.append(query)
        if row["price_summary_allowed"]:
            price_failures.append(query)

    for query in ["Summicron-M 35 ASPH", "Leica M 35mm f2 Summicron ASPH", "35 Summicron-M ASPH"]:
        row = rows[query]
        if row["top_result_model"] == "APO-Summicron" and row["market_entry_allowed"]:
            market_failures.append(query)

    for query, forbidden_model in {
        "APO-Summicron-SL 50": "Elmar",
        "APO-Summicron-SL 90": "Summarit-M",
        "Summicron-M 50": "Elmar",
    }.items():
        row = rows[query]
        if row["top_result_model"] == forbidden_model and row["market_entry_allowed"]:
            market_failures.append(query)

    strong_regression = rows["ltm summaron 35"]
    if not strong_regression["market_entry_allowed"] or not strong_regression["price_summary_allowed"]:
        regression_failures.append("ltm summaron 35")

    lux_aa = rows["35 lux aa"]
    if not lux_aa["market_entry_allowed"]:
        regression_failures.append("35 lux aa")

    q3 = rows["q3 28"]
    if not q3["market_entry_allowed"] or q3["top_result_category"] != "Body":
        regression_failures.append("q3 28")

    for query in ["ricoh gr iiix", "hasselblad xpan"]:
        row = rows[query]
        if row["market_entry_allowed"] or row["price_summary_allowed"] or row["total_ranked"] != 0:
            regression_failures.append(query)

    return sorted(set(market_failures)), sorted(set(price_failures)), sorted(set(regression_failures))


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


def ui_copy_changes() -> list[dict[str, str]]:
    html = APP_HTML_PATH.read_text(encoding="utf-8")
    root_html = ROOT_HTML_PATH.read_text(encoding="utf-8")
    items = [
        {
            "change": "locked_market_entry_copy",
            "copy": "Exact model summary is locked until confidence is high enough.",
        },
        {
            "change": "locked_price_summary_copy",
            "copy": "Not enough exact confidence for price summary",
        },
        {
            "change": "refine_cta_copy",
            "copy": "Refine this search",
        },
        {
            "change": "confidence_gate_badge",
            "copy": "Confidence gate active",
        },
    ]
    for item in items:
        item["present_in_app_template"] = str(item["copy"] in html).lower()
        item["present_in_root_html"] = str(item["copy"] in root_html).lower()
    return items


def scenario_validation(rows: dict[str, dict[str, Any]], decision_status: str) -> list[dict[str, Any]]:
    validations = [
        ("previous audit evidence loaded", AUDIT_JSON_PATH.exists()),
        ("gate fields populated in response", all("market_entry_allowed" in row for row in rows.values())),
        (
            "blocking queries do not allow unsafe market entry",
            all(not rows[q]["market_entry_allowed"] for q in BLOCKING_QUERIES),
        ),
        (
            "blocking queries do not allow unsafe price summary",
            all(not rows[q]["price_summary_allowed"] for q in BLOCKING_QUERIES),
        ),
        (
            "broad query guidance preserved",
            rows["summicron"]["needs_disambiguation"] and rows["leica lens"]["needs_disambiguation"],
        ),
        (
            "safe query regression path preserved",
            rows["ltm summaron 35"]["market_entry_allowed"] and rows["35 lux aa"]["market_entry_allowed"],
        ),
        (
            "no-result queries stay locked without fake fill",
            rows["ricoh gr iiix"]["total_ranked"] == 0 and rows["hasselblad xpan"]["total_ranked"] == 0,
        ),
        (
            "decision status recorded",
            decision_status
            in {
                DECISION_PUSHED,
                DECISION_READY,
                DECISION_HOLD_GATE,
                DECISION_HOLD_MARKET,
                DECISION_HOLD_PRICE,
                DECISION_HOLD_REGRESSION,
                DECISION_HOLD_PUSH,
            },
        ),
    ]
    return [
        {"check": label, "status": "passed" if passed else "failed"}
        for label, passed in validations
    ]


def build_payload(commit_push_context: dict[str, Any] | None = None) -> dict[str, Any]:
    commit_push_context = commit_push_context or build_commit_push_context_from_env()
    previous_audit = load_json(AUDIT_JSON_PATH) if AUDIT_JSON_PATH.exists() else {}
    rows = {query: response_row(query) for query in ALL_QUERIES}
    market_failures, price_failures, regression_failures = classify_failures(rows)
    git_summary = collect_git_summary()

    if market_failures:
        decision_status = DECISION_HOLD_MARKET
    elif price_failures:
        decision_status = DECISION_HOLD_PRICE
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
            "production_alias_connect_allowed": previous_audit.get("production_alias_connect_allowed"),
            "problem_summary": "query parser unknown token + weak-only fallback + first-result market entry anchoring",
        },
        "current_problem_summary": {
            "representative_failures": [
                "Summicron-M 35 ASPH -> APO-Summicron first result",
                "Leica M 35mm f2 Summicron ASPH -> APO-Summicron first result",
                "APO-Summicron-SL 50 -> Elmar first result",
                "Summicron-M 50 -> Elmar first result",
                "summicron / leica lens broad queries need market entry and price summary block",
            ],
        },
        "implemented_gate_fields": [
            "market_entry_allowed",
            "market_entry_block_reason",
            "price_summary_allowed",
            "price_summary_block_reason",
            "model_entry_confidence_state",
            "boundary_conflict_detected",
            "dangerous_unknown_family_token_detected",
            "weak_only_fallback_detected",
        ],
        "market_entry_allowed_rules": [
            "strong_result_count > 0",
            "not weak-only fallback",
            "no dangerous unknown family token",
            "not broad query refinement state",
            "query intent confidence >= 0.60",
            "no family/mount/category/variant boundary conflict",
            "top result must be strong",
            "exact-model-like match must exist",
        ],
        "price_summary_allowed_rules": [
            "market_entry_allowed = true",
            "exact-model-like match exists",
            "query-compatible results exist",
            "query-compatible priced results exist",
            "weak-only fallback prices are excluded",
        ],
        "query_regression_results": [rows[q] for q in ALL_QUERIES],
        "blocking_query_safe_handling": [
            {
                "query": q,
                "market_entry_allowed": rows[q]["market_entry_allowed"],
                "price_summary_allowed": rows[q]["price_summary_allowed"],
                "market_entry_block_reason": rows[q]["market_entry_block_reason"],
            }
            for q in BLOCKING_QUERIES
        ],
        "safe_hold_query_regression_results": [
            {
                "query": q,
                "market_entry_allowed": rows[q]["market_entry_allowed"],
                "price_summary_allowed": rows[q]["price_summary_allowed"],
                "ui_state": rows[q]["ui_state"],
                "total_ranked": rows[q]["total_ranked"],
            }
            for q in REGRESSION_QUERIES
        ],
        "ui_copy_changes": ui_copy_changes(),
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
            "market_failures": market_failures,
            "price_failures": price_failures,
            "regression_failures": regression_failures,
        },
        "scenario_validation": scenario_validation(rows, decision_status),
        "next_backlog_candidates": [
            "P3-BETA-MVP-MARKET-ENTRY-CONFIDENCE-GATE-OWNER-RECHECK",
            "P3-BETA-MVP-QUERY-PARSER-UNKNOWN-TOKEN-COVERAGE-FIXUP",
            "P3-BETA-MVP-MARKET-ENTRY-CONFIDENCE-GATE-PUSH-FOLLOWUP",
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
    lines.append("## Implemented Gate Fields")
    for item in payload["implemented_gate_fields"]:
        lines.append(f"- `{item}`")
    lines.append("")
    lines.append("## Market Entry Allowed Rules")
    for item in payload["market_entry_allowed_rules"]:
        lines.append(f"- {item}")
    lines.append("")
    lines.append("## Price Summary Allowed Rules")
    for item in payload["price_summary_allowed_rules"]:
        lines.append(f"- {item}")
    lines.append("")
    lines.append("## Query Regression Results")
    for row in payload["query_regression_results"]:
        lines.append(
            f"- `{row['query']}`: market_entry_allowed=`{row['market_entry_allowed']}`, "
            f"price_summary_allowed=`{row['price_summary_allowed']}`, "
            f"state=`{row['model_entry_confidence_state']}`, top=`{row['top_result_model']}`"
        )
    lines.append("")
    lines.append("## UI Copy Changes")
    for item in payload["ui_copy_changes"]:
        lines.append(f"- `{item['change']}`: `{item['copy']}`")
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
    lines.append("## Preview Deployment")
    for key, value in payload["preview_deployment"].items():
        lines.append(f"- {key}: `{value}`")
    lines.append("")
    lines.append("## Guards")
    for key, value in payload["guards"].items():
        lines.append(f"- {key}: `{value}`")
    lines.append("")
    lines.append("## Next Backlog Candidates")
    for item in payload["next_backlog_candidates"]:
        lines.append(f"- `{item}`")
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
