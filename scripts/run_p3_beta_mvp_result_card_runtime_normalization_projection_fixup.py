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

TASK_NAME = "P3-BETA-MVP-RESULT-CARD-RUNTIME-NORMALIZATION-PROJECTION-FIXUP"
TARGET_TITLE = "[중고]Leica M50/1.2 1세대"
SCRIPT_NAME = "run_p3_beta_mvp_result_card_runtime_normalization_projection_fixup.py"
TEST_NAME = "test_beta_mvp_result_card_runtime_normalization_projection_fixup.py"
MD_PATH = ADMIN_DIR / "p3_beta_mvp_result_card_runtime_normalization_projection_fixup_v0.md"
JSONL_PATH = ADMIN_DIR / "p3_beta_mvp_result_card_runtime_normalization_projection_fixup_v0.jsonl"
JSON_PATH = ADMIN_DIR / "beta_mvp_result_card_runtime_normalization_projection_fixup_v0.json"


QUERY_GROUPS = {
    "compact_lens": [
        TARGET_TITLE,
        "M50/1.2",
        "Leica M50/1.2 1세대",
        "M35/2",
        "M28/2.8",
    ],
    "body_regression": [
        "Leica M5",
        "M5 body",
        "Leica M9",
        "Leica M10",
        "Leica M11",
        "q3 28",
    ],
    "non_body_regression": [
        "ltm summaron 35",
        "35 lux aa",
        "summicron",
        "leica hood 12585",
        "ricoh gr iiix",
    ],
}


def _run_git(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()


def _query_response(query: str, limit: int = 100) -> dict:
    return search_from_params({"q": query, "limit": str(limit)})


def _find_title_result(response: dict, title: str = TARGET_TITLE) -> tuple[int | None, dict | None]:
    for idx, result in enumerate(response.get("results") or [], 1):
        if (result.get("title") or "") == title:
            return idx, result
    return None, None


def _compact_result(result: dict | None) -> dict | None:
    if not result:
        return None
    final = result.get("final_output") or {}
    display = result.get("display_output") or {}
    return {
        "title": result.get("title"),
        "match_quality": result.get("match_quality"),
        "matched_fields": result.get("matched_fields"),
        "warnings": result.get("warnings"),
        "final_output": {
            key: final.get(key)
            for key in [
                "category",
                "label",
                "model_canonical",
                "mount",
                "focal_length",
                "compact_lens_notation_detected",
                "body_alias_boundary_blocked",
                "classification_conflict_detected",
                "body_lens_boundary_conflict_detected",
                "stale_body_normalization_detected",
            ]
        },
        "display_output": display,
    }


def _response_snapshot(query: str, limit: int = 100) -> dict:
    response = _query_response(query, limit=limit)
    intent = response.get("intent") or {}
    idx, title_result = _find_title_result(response)
    top = (response.get("results") or [None])[0]
    top_final = (top or {}).get("final_output") or {}
    top_display = (top or {}).get("display_output") or {}
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
        "top_result": {
            "title": (top or {}).get("title"),
            "final_category": top_final.get("category"),
            "final_model": top_final.get("model_canonical"),
            "display_category": top_display.get("display_category"),
            "display_model": top_display.get("display_model"),
            "display_family": top_display.get("display_family"),
            "display_mount": top_display.get("display_mount"),
            "display_focal_length": top_display.get("display_focal_length"),
            "display_aperture": top_display.get("display_aperture"),
            "result_card_confidence_state": top_display.get("result_card_confidence_state"),
        },
        "top_three_categories": [
            ((item.get("display_output") or {}).get("display_category") or (item.get("final_output") or {}).get("category"))
            for item in (response.get("results") or [])[:3]
        ],
        "title_result_index": idx,
        "title_result": _compact_result(title_result),
        "market_entry_allowed": response.get("market_entry_allowed"),
        "market_entry_block_reason": response.get("market_entry_block_reason"),
        "price_summary_allowed": response.get("price_summary_allowed"),
        "total_ranked": response.get("total_ranked"),
    }


def _decision(
    stale_display_failures: list[str],
    body_regressions: list[str],
    display_truth_failures: list[str],
    regression_failures: list[str],
) -> str:
    if stale_display_failures:
        return "beta_mvp_result_card_runtime_projection_fixup_hold_result_card_still_shows_m5_body"
    if body_regressions:
        return "beta_mvp_result_card_runtime_projection_fixup_hold_true_body_alias_regressed"
    if display_truth_failures:
        return "beta_mvp_result_card_runtime_projection_fixup_hold_stale_final_output_display_truth"
    if regression_failures:
        return "beta_mvp_result_card_runtime_projection_fixup_hold_tests_failed"
    if os.getenv("P3_PUSH_SUCCEEDED", "").lower() == "true":
        return "beta_mvp_result_card_runtime_projection_fixup_pushed_ready_for_owner_recheck"
    return "beta_mvp_result_card_runtime_projection_fixup_passed_ready_for_owner_approved_push"


def _git_diff_stat() -> str:
    files = [
        "search_service.py",
        "search_ui_hints.py",
        "query_parser.py",
        "query_resolver.py",
        "model_detector.py",
        "classifier_v2.py",
        "api/search.py",
        "search_response.py",
        "app/templates/index.html",
        "index.html",
        f"scripts/{SCRIPT_NAME}",
        f"tests/{TEST_NAME}",
        "data/admin/p3_beta_mvp_result_card_runtime_normalization_projection_fixup_v0.md",
        "data/admin/p3_beta_mvp_result_card_runtime_normalization_projection_fixup_v0.jsonl",
        "data/admin/beta_mvp_result_card_runtime_normalization_projection_fixup_v0.json",
    ]
    return _run_git("diff", "--stat", "--", *files)


def _build_markdown(payload: dict) -> str:
    lines = [
        f"# {payload['task_name']}",
        "",
        f"- decision_status: `{payload['decision_status']}`",
        "",
        "## Owner recheck failure summary",
        f"- {payload['owner_recheck_failure_summary']}",
        "",
        "## Screenshot issue summary",
        f"- {payload['screenshot_issue_summary']}",
        "",
        "## Root cause hypothesis",
    ]
    lines.extend(f"- {item}" for item in payload["root_cause_hypothesis"])
    lines.extend(
        [
            "",
            "## Safe display projection design",
        ]
    )
    lines.extend(f"- {item}" for item in payload["safe_display_projection_design"])
    lines.extend(
        [
            "",
            "## Stale final_output conflict guard",
        ]
    )
    lines.extend(f"- {item}" for item in payload["stale_final_output_conflict_guard"])
    lines.extend(
        [
            "",
            "## Result card UI changes",
        ]
    )
    lines.extend(f"- {item}" for item in payload["result_card_ui_changes"])
    lines.extend(
        [
            "",
            "## Market entry / price summary gate connection",
        ]
    )
    lines.extend(f"- {item}" for item in payload["market_entry_price_summary_gate_link"])
    lines.extend(
        [
            "",
            "## Query regression highlights",
        ]
    )
    for item in payload["query_regression_results"]:
        lines.append(
            f"- `{item['query']}`: top=`{item['top_result']['display_category'] or item['top_result']['final_category']}` "
            f"title_row_index=`{item['title_result_index']}`"
        )
    lines.extend(
        [
            "",
            "## Git diff summary",
            f"- branch: `{payload['git_diff_summary']['branch']}`",
            f"- head_commit: `{payload['git_diff_summary']['head_commit']}`",
            f"- head_subject: `{payload['git_diff_summary']['head_subject']}`",
            f"- diff_stat: `{payload['git_diff_summary']['working_diff_stat']}`",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> None:
    compact_results = [_response_snapshot(query) for query in QUERY_GROUPS["compact_lens"]]
    body_results = [_response_snapshot(query) for query in QUERY_GROUPS["body_regression"]]
    non_body_results = [_response_snapshot(query) for query in QUERY_GROUPS["non_body_regression"]]

    stale_display_failures: list[str] = []
    for item in compact_results:
        title_result = item["title_result"]
        if item["query"] == TARGET_TITLE and not title_result:
            stale_display_failures.append("owner_target_row_missing")
            continue
        if not title_result:
            continue
        display = title_result["display_output"]
        if display.get("display_model") == "M5" or display.get("display_category") == "Body":
            stale_display_failures.append(f"{item['query']}:still_shows_body")
        if not display.get("compact_lens_notation_detected"):
            stale_display_failures.append(f"{item['query']}:missing_compact_flag")

    display_truth_failures: list[str] = []
    m5_query = next(item for item in body_results if item["query"] == "Leica M5")
    stale_row = m5_query["title_result"]
    if stale_row:
        display = stale_row["display_output"]
        if display.get("display_category") != "Lens":
            display_truth_failures.append("leica_m5_query_title_row_not_projected_to_lens")
        if display.get("display_model") == "M5":
            display_truth_failures.append("leica_m5_query_title_row_model_still_m5")
        if not display.get("stale_normalization_detected"):
            display_truth_failures.append("leica_m5_query_title_row_missing_stale_flag")

    body_regressions: list[str] = []
    for item in body_results:
        top = item["top_result"]
        if item["query"] != "q3 28" and item["intent"].get("body_intent") is None:
            body_regressions.append(f"{item['query']}:missing_body_intent")
        if top["display_category"] != "Body":
            body_regressions.append(f"{item['query']}:top_not_body")

    regression_failures: list[str] = []
    expected = {
        "ltm summaron 35": "Lens",
        "35 lux aa": "Lens",
        "summicron": "Lens",
        "leica hood 12585": "Accessory",
        "ricoh gr iiix": None,
    }
    for item in non_body_results:
        if item["top_result"]["display_category"] != expected[item["query"]]:
            regression_failures.append(f"{item['query']}:unexpected_display_category")

    decision_status = _decision(
        stale_display_failures,
        body_regressions,
        display_truth_failures,
        regression_failures,
    )

    payload = {
        "task_name": TASK_NAME,
        "decision_status": decision_status,
        "owner_recheck_failure_summary": "Owner preview still showed [중고]Leica M50/1.2 1세대 as Detected model=M5 / Family=M Body / Category=Body after the compact-lens boundary fix.",
        "screenshot_issue_summary": "The result card was still reading stale normalized Body metadata even though title-level compact lens notation indicates an M-mount 50mm f/1.2 lens.",
        "root_cause_hypothesis": [
            "stale final_output rows in the existing search index still contain Body/M5 metadata",
            "runtime compact-lens projection previously missed slash notation when it read normalized title text only",
            "result card UI was reading raw final_output fields directly instead of a safer display projection layer",
        ],
        "safe_display_projection_design": [
            "add display_output to each API result",
            "prefer display_category/display_model/display_family/display_mount/display_focal_length/display_aperture for UI",
            "when compact lens notation conflicts with stale Body output, project the card to Lens and blank unsafe body model claims",
        ],
        "stale_final_output_conflict_guard": [
            "compact_lens_notation_detected",
            "body_alias_boundary_blocked",
            "classification_conflict_detected",
            "stale_body_normalization_detected",
            "result_card_confidence_state",
        ],
        "result_card_ui_changes": [
            "result cards now read display_output instead of raw final_output for Detected model / Family / Mount / Category",
            "compact lens conflicts show Runtime projection and Lens notation detected badges",
            "focal length and aperture are shown on the card when compact notation can safely provide them",
        ],
        "market_entry_price_summary_gate_link": [
            "classification or stale-normalization conflict now contributes to market entry blocking",
            "summary-scope checks now honor display-safe category/mount/focal fields",
            "the stale M50/1.2 row cannot be used as Body evidence for M5 market entry or price summary",
        ],
        "query_regression_results": compact_results + body_results,
        "lens_accessory_no_result_regression_results": non_body_results,
        "true_body_alias_maintained": [
            {
                "query": item["query"],
                "body_intent": item["intent"].get("body_intent"),
                "top_display_category": item["top_result"]["display_category"],
                "top_display_model": item["top_result"]["display_model"],
            }
            for item in body_results
        ],
        "git_diff_summary": {
            "branch": _run_git("branch", "--show-current"),
            "head_commit": _run_git("rev-parse", "HEAD"),
            "head_subject": _run_git("log", "--oneline", "-1"),
            "working_diff_stat": _git_diff_stat(),
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
            "stale_display_failures": stale_display_failures,
            "true_body_alias_regressions": body_regressions,
            "stale_display_truth_failures": display_truth_failures,
            "regression_failures": regression_failures,
        },
        "next_backlog_candidates": [
            "P3-BETA-MVP-RESULT-CARD-RUNTIME-PROJECTION-OWNER-RECHECK",
            "P3-BETA-MVP-GLOBAL-MATCH-PRIORITY-RANKING-FIXUP",
            "P3-BETA-MVP-QUERY-PARSER-UNKNOWN-TOKEN-COVERAGE-FIXUP",
        ],
    }

    ADMIN_DIR.mkdir(parents=True, exist_ok=True)
    JSON_PATH.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    JSONL_PATH.write_text(json.dumps(payload, ensure_ascii=False) + "\n", encoding="utf-8")
    MD_PATH.write_text(_build_markdown(payload), encoding="utf-8")
    print(json.dumps(payload, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
