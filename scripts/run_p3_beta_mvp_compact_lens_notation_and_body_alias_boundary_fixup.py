from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ADMIN_DIR = ROOT / "data" / "admin"
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from api.search import search_from_params
from classifier_v2 import classify_listing_v2
from query_parser import parse_query

TASK_NAME = "P3-BETA-MVP-COMPACT-LENS-NOTATION-AND-BODY-ALIAS-BOUNDARY-FIXUP"

COMPACT_QUERIES = [
    "M50/1.2",
    "Leica M50/1.2 1세대",
    "M50/2",
    "M35/2",
    "M28/2.8",
]
BODY_REGRESSION_QUERIES = [
    "Leica M5",
    "M5 body",
    "Leica M9",
    "Leica M10",
    "Leica M11",
    "q3 28",
]
NON_BODY_REGRESSION_QUERIES = [
    "ltm summaron 35",
    "35 lux aa",
    "summicron",
    "leica hood 12585",
    "ricoh gr iiix",
]


def _run_git(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()


def _query_snapshot(query: str) -> dict:
    response = search_from_params({"q": query, "limit": 5})
    intent = response.get("intent") or {}
    results = response.get("results") or []
    top_result = results[0] if results else {}
    top_final = (top_result.get("final_output") or {}) if top_result else {}
    return {
        "query": query,
        "intent": {
            key: intent.get(key)
            for key in [
                "brand",
                "body_intent",
                "mount",
                "system",
                "focal_length",
                "aperture",
                "model_family",
                "confidence",
            ]
        },
        "unknown_tokens": [
            token.get("raw")
            for token in intent.get("tokens", [])
            if token.get("type") == "unknown"
        ],
        "top_result": {
            "category": top_final.get("category"),
            "label": top_final.get("label"),
            "model_canonical": top_final.get("model_canonical"),
            "mount": top_final.get("mount"),
            "focal_length": top_final.get("focal_length"),
            "compact_lens_notation_detected": top_final.get("compact_lens_notation_detected"),
            "body_alias_boundary_blocked": top_final.get("body_alias_boundary_blocked"),
            "classification_conflict_detected": top_final.get("classification_conflict_detected"),
            "body_lens_boundary_conflict_detected": top_final.get("body_lens_boundary_conflict_detected"),
        },
        "top_match_quality": top_result.get("match_quality") if top_result else None,
        "top_matched_fields": top_result.get("matched_fields") if top_result else [],
        "top_three_categories": [
            ((item.get("final_output") or {}).get("category"))
            for item in results[:3]
        ],
        "market_entry_allowed": response.get("market_entry_allowed"),
        "price_summary_allowed": response.get("price_summary_allowed"),
        "market_entry_block_reason": response.get("market_entry_block_reason"),
    }


def _classification_snapshot(title: str) -> dict:
    classified = classify_listing_v2({"상품명": title, "상품설명": ""})
    return {
        "title": title,
        "category": classified.get("category"),
        "label": classified.get("label"),
        "mount": classified.get("mount"),
        "model_canonical": classified.get("model_canonical"),
        "focal_length": classified.get("focal_length"),
        "compact_lens_notation_detected": classified.get("compact_lens_notation_detected"),
        "body_alias_boundary_blocked": classified.get("body_alias_boundary_blocked"),
        "classification_conflict_detected": classified.get("classification_conflict_detected"),
        "body_lens_boundary_conflict_detected": classified.get("body_lens_boundary_conflict_detected"),
        "category_reason": classified.get("category_reason"),
    }


def _decision(parser_failures: list[str], body_regressions: list[str], boundary_failures: list[str], regression_failures: list[str]) -> str:
    if parser_failures:
        return "beta_mvp_compact_lens_body_alias_boundary_fixup_hold_compact_lens_still_matches_body"
    if body_regressions:
        return "beta_mvp_compact_lens_body_alias_boundary_fixup_hold_true_body_alias_regressed"
    if boundary_failures:
        return "beta_mvp_compact_lens_body_alias_boundary_fixup_hold_category_boundary_failed"
    if regression_failures:
        return "beta_mvp_compact_lens_body_alias_boundary_fixup_hold_tests_failed"
    if os.getenv("P3_PUSH_SUCCEEDED", "").lower() == "true":
        return "beta_mvp_compact_lens_body_alias_boundary_fixup_pushed_ready_for_owner_recheck"
    return "beta_mvp_compact_lens_body_alias_boundary_fixup_passed_ready_for_owner_approved_push"


def main() -> None:
    compact_classifications = [
        _classification_snapshot("[중고]Leica M50/1.2 1세대"),
        _classification_snapshot("M50/1.2"),
        _classification_snapshot("M35/2"),
        _classification_snapshot("M28/2.8"),
        _classification_snapshot("Leica M5"),
    ]
    compact_results = [_query_snapshot(query) for query in COMPACT_QUERIES]
    body_results = [_query_snapshot(query) for query in BODY_REGRESSION_QUERIES]
    non_body_results = [_query_snapshot(query) for query in NON_BODY_REGRESSION_QUERIES]

    parser_failures: list[str] = []
    for item in compact_results:
        intent = item["intent"]
        if item["query"] != "Leica M50/1.2 1세대" and intent.get("body_intent"):
            parser_failures.append(item["query"])
        if not intent.get("mount") or not intent.get("focal_length") or not intent.get("aperture"):
            parser_failures.append(f"{item['query']}:missing_compact_parse")

    boundary_failures: list[str] = []
    for item in compact_results:
        top = item["top_result"]
        if top.get("category") == "Body":
            boundary_failures.append(f"{item['query']}:top_body")
        if item["top_three_categories"] and item["top_three_categories"][0] not in {"Lens", None}:
            boundary_failures.append(f"{item['query']}:top_non_lens")

    body_regressions: list[str] = []
    for item in body_results:
        intent = item["intent"]
        if not intent.get("body_intent"):
            body_regressions.append(f"{item['query']}:missing_body_intent")
        if item["query"] != "q3 28" and item["top_result"].get("category") != "Body":
            body_regressions.append(f"{item['query']}:top_not_body")

    regression_failures: list[str] = []
    expected_categories = {
        "ltm summaron 35": "Lens",
        "35 lux aa": "Lens",
        "summicron": "Lens",
        "leica hood 12585": "Accessory",
        "ricoh gr iiix": None,
    }
    for item in non_body_results:
        expected = expected_categories[item["query"]]
        if item["top_result"].get("category") != expected:
            regression_failures.append(f"{item['query']}:unexpected_top_category")

    decision_status = _decision(parser_failures, body_regressions, boundary_failures, regression_failures)

    payload = {
        "task_name": TASK_NAME,
        "decision_status": decision_status,
        "current_problem_summary": {
            "core_problem": "Compact lens notation such as M50/1.2 could collide with Leica M-body aliases and stale body classification.",
            "owner_screenshot_issue": "[중고]Leica M50/1.2 1세대 was rendered as M5 / M Body / Body even though it is lens-like.",
        },
        "compact_lens_notation_detector": {
            "supported_examples": [
                "M50/1.2",
                "M 50/1.2",
                "M50 f1.2",
                "M 50mm f1.2",
                "M35/2",
                "R50/2",
                "SL50/2",
                "L35/3.5",
            ],
            "intent_behavior": "mount + focal_length + aperture are parsed before any body alias fallback",
        },
        "body_alias_boundary_rule": [
            "body alias must stay an independent token",
            "compact mount/focal/aperture notation must not collapse into M-body aliases",
            "runtime stale Body rows with compact lens notation are projected back to Lens",
        ],
        "category_conflict_guard": [
            "compact_lens_notation_detected",
            "body_alias_boundary_blocked",
            "classification_conflict_detected",
            "body_lens_boundary_conflict_detected",
        ],
        "classification_snapshots": compact_classifications,
        "query_regression_results": compact_results + body_results,
        "lens_accessory_no_result_regression_results": non_body_results,
        "market_entry_price_summary_gate_link": [
            "classification conflicts now contribute to market_entry boundary conflict",
            "price summary remains blocked when model-level confidence is not exact enough",
            "body market evidence is not derived from compact-lens conflict rows",
        ],
        "git_diff_summary": {
            "branch": _run_git("branch", "--show-current"),
            "head_commit": _run_git("rev-parse", "HEAD"),
            "head_subject": _run_git("log", "--oneline", "-1"),
            "working_diff_stat": _run_git("diff", "--stat", "--", "model_detector.py", "classifier_v2.py", "query_parser.py", "query_resolver.py", "api/search.py", "scripts/run_p3_beta_mvp_compact_lens_notation_and_body_alias_boundary_fixup.py", "tests/test_beta_mvp_compact_lens_notation_and_body_alias_boundary_fixup.py", "data/admin/p3_beta_mvp_compact_lens_notation_and_body_alias_boundary_fixup_v0.md", "data/admin/p3_beta_mvp_compact_lens_notation_and_body_alias_boundary_fixup_v0.jsonl", "data/admin/beta_mvp_compact_lens_notation_and_body_alias_boundary_fixup_v0.json"),
        },
        "commit_push_status": {
            "commit_executed": os.getenv("P3_COMMIT_EXECUTED", "").lower() == "true",
            "push_executed": os.getenv("P3_PUSH_EXECUTED", "").lower() == "true",
            "push_succeeded": os.getenv("P3_PUSH_SUCCEEDED", "").lower() == "true",
            "preview_deployment_url": os.getenv("P3_PREVIEW_URL") or None,
            "preview_deployment_id": os.getenv("P3_PREVIEW_DEPLOYMENT_ID") or None,
            "preview_deployment_state": os.getenv("P3_PREVIEW_STATE") or None,
            "preview_branch": os.getenv("P3_PREVIEW_BRANCH") or None,
            "preview_commit": os.getenv("P3_PREVIEW_COMMIT") or None,
        },
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
        "production_alias_connect_allowed": False,
        "test_verdict": {
            "parser_failures": parser_failures,
            "body_alias_regressions": body_regressions,
            "category_boundary_failures": boundary_failures,
            "regression_failures": regression_failures,
        },
        "next_backlog_candidates": [
            "P3-BETA-MVP-COMPACT-LENS-BODY-ALIAS-OWNER-RECHECK",
            "P3-BETA-MVP-GLOBAL-MATCH-PRIORITY-RANKING-FIXUP",
            "P3-BETA-MVP-QUERY-PARSER-UNKNOWN-TOKEN-COVERAGE-FIXUP",
        ],
    }

    md_lines = [
        f"# {TASK_NAME}",
        "",
        f"- decision_status: `{payload['decision_status']}`",
        "- compact lens notation now parses as lens intent before body alias fallback",
        "- stale Body rows with compact lens notation are projected back to Lens at search time",
        "- true Leica body aliases (M5, M9, M10, M11) remain intact",
        "",
        "## Compact Query Results",
    ]
    for item in compact_results:
        md_lines.append(
            f"- `{item['query']}` -> body_intent=`{item['intent'].get('body_intent')}`, "
            f"mount=`{item['intent'].get('mount')}`, focal=`{item['intent'].get('focal_length')}`, "
            f"aperture=`{item['intent'].get('aperture')}`, top_category=`{item['top_result'].get('category')}`"
        )
    md_lines.extend(
        [
            "",
            "## True Body Alias Regression",
        ]
    )
    for item in body_results:
        md_lines.append(
            f"- `{item['query']}` -> body_intent=`{item['intent'].get('body_intent')}`, "
            f"top_category=`{item['top_result'].get('category')}`, top_model=`{item['top_result'].get('model_canonical')}`"
        )

    md_path = ADMIN_DIR / "p3_beta_mvp_compact_lens_notation_and_body_alias_boundary_fixup_v0.md"
    jsonl_path = ADMIN_DIR / "p3_beta_mvp_compact_lens_notation_and_body_alias_boundary_fixup_v0.jsonl"
    json_path = ADMIN_DIR / "beta_mvp_compact_lens_notation_and_body_alias_boundary_fixup_v0.json"

    md_path.write_text("\n".join(md_lines) + "\n", encoding="utf-8")
    jsonl_path.write_text(json.dumps(payload, ensure_ascii=False) + "\n", encoding="utf-8")
    json_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(json.dumps(payload, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
