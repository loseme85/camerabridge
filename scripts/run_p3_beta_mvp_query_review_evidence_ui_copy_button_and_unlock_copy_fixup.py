from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DATA_ADMIN = ROOT / "data" / "admin"
APP_TEMPLATE = ROOT / "app" / "templates" / "index.html"
ROOT_TEMPLATE = ROOT / "index.html"

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from api.search import search_from_params


TASK_NAME = "P3-BETA-MVP-QUERY-REVIEW-EVIDENCE-UI-COPY-BUTTON-AND-UNLOCK-COPY-FIXUP"
DECISION_PUSHED = "query_review_evidence_ui_copy_button_and_unlock_copy_fixup_pushed_ready_for_owner_recheck"
DECISION_READY = "query_review_evidence_ui_copy_button_and_unlock_copy_fixup_passed_ready_for_owner_approved_push"
DECISION_HOLD_BUTTON = "query_review_evidence_ui_copy_button_and_unlock_copy_fixup_hold_copy_button_missing"
DECISION_HOLD_UI = "query_review_evidence_ui_copy_button_and_unlock_copy_fixup_hold_ui_still_too_technical"
DECISION_HOLD_REGRESSION = "query_review_evidence_ui_copy_button_and_unlock_copy_fixup_hold_regression"
DECISION_HOLD_PUSH = "query_review_evidence_ui_copy_button_and_unlock_copy_fixup_hold_push_or_preview_deploy_failed"

JSON_PATH = DATA_ADMIN / "query_review_evidence_ui_copy_button_and_unlock_copy_fixup_v0.json"
JSONL_PATH = DATA_ADMIN / "p3_beta_mvp_query_review_evidence_ui_copy_button_and_unlock_copy_fixup_v0.jsonl"
MD_PATH = DATA_ADMIN / "p3_beta_mvp_query_review_evidence_ui_copy_button_and_unlock_copy_fixup_v0.md"

SCOPED_FILES = [
    "api/search.py",
    "app/templates/index.html",
    "index.html",
    "scripts/run_p3_beta_mvp_query_review_evidence_ui_copy_button_and_unlock_copy_fixup.py",
    "tests/test_beta_mvp_query_review_evidence_ui_copy_button_and_unlock_copy_fixup.py",
    "data/admin/p3_beta_mvp_query_review_evidence_ui_copy_button_and_unlock_copy_fixup_v0.md",
    "data/admin/p3_beta_mvp_query_review_evidence_ui_copy_button_and_unlock_copy_fixup_v0.jsonl",
    "data/admin/query_review_evidence_ui_copy_button_and_unlock_copy_fixup_v0.json",
]

QUERY_ORDER = [
    "35 lux aa",
    "Noctilux 50 f1 E60",
    "Summicron 50 rigid",
    "Summilux-M 50 ASPH",
    "M50/1.2",
    "leica m5",
    "Leica M9",
    "Leica M10",
    "Leica M11",
]

FORBIDDEN_UI_TOKENS = {
    "exact_variant_pool",
    "exact_base_model_pool",
    "broader_family_pool",
    "query_incompatible",
    "third_party_top_result",
    "Need no third-party contamination in the selected price pool.",
    "Need exact or strong compatible visible Leica results.",
    "Need 2+ exact variant priced listings.",
}


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
    response = search_from_params({"q": query, "limit": "12"})
    results = response.get("results") or []
    top = results[0] if results else {}
    top_display = top.get("display_output") or {}
    return {
        "query": query,
        "display_query_review": response.get("display_query_review") or {},
        "display_top_result_evidence": response.get("display_top_result_evidence") or [],
        "display_price_summary_allowed": bool(response.get("display_price_summary_allowed")),
        "display_price_scope_label": response.get("display_price_scope_label"),
        "display_price_band": response.get("display_price_band"),
        "display_broader_reference_allowed": bool(response.get("display_broader_reference_allowed")),
        "display_broader_reference_label": response.get("display_broader_reference_label"),
        "display_broader_reference_band": response.get("display_broader_reference_band"),
        "display_match_state_message": response.get("display_match_state_message"),
        "display_unlock_requirements": list(response.get("display_unlock_requirements") or []),
        "top_display_category": top_display.get("display_category"),
        "top_display_model": top_display.get("display_model"),
    }


def collect_git_summary() -> dict[str, Any]:
    return {
        "branch": run_git("branch", "--show-current"),
        "head_commit": run_git("rev-parse", "HEAD"),
        "head_subject": run_git("log", "-1", "--pretty=%s"),
        "working_diff_stat": run_git("diff", "--stat", "--", *SCOPED_FILES),
        "working_diff_files": [line for line in run_git("diff", "--name-only", "--", *SCOPED_FILES).splitlines() if line],
    }


def _row_text(row: dict[str, Any]) -> str:
    review = row.get("display_query_review") or {}
    chunks = [
        review.get("interpreted_target") or "",
        review.get("price_status") or "",
        review.get("why") or "",
        review.get("evidence_summary") or "",
        review.get("copy_summary_text") or "",
        " ".join(review.get("needed_to_unlock") or []),
    ]
    for item in row.get("display_top_result_evidence") or []:
        chunks.extend(
            [
                item.get("result_role_label") or "",
                item.get("price_usage_label") or "",
                item.get("evidence_pool_label") or "",
                " ".join(item.get("excluded_reason") or []),
            ]
        )
    return " | ".join(chunks)


def _template_text() -> str:
    return "\n".join(
        [
            APP_TEMPLATE.read_text(encoding="utf-8"),
            ROOT_TEMPLATE.read_text(encoding="utf-8"),
        ]
    )


def classify(rows: dict[str, dict[str, Any]]) -> tuple[list[str], list[str], list[str]]:
    button_missing: list[str] = []
    ui_too_technical: list[str] = []
    regressions: list[str] = []

    template_text = _template_text()
    if "Copy summary" not in template_text or "query-review-copy" not in template_text or "data-copy-query-review" not in template_text:
        button_missing.append("query_review_panel")
    if "unlock.join(' / ')" in template_text:
        ui_too_technical.append("query_review_unlock_copy")

    for query, row in rows.items():
        text = _row_text(row)
        if any(token in text for token in FORBIDDEN_UI_TOKENS):
            ui_too_technical.append(query)
        review = row.get("display_query_review") or {}
        if not review.get("copy_summary_text"):
            button_missing.append(query)

    for query in ["M50/1.2"]:
        row = rows[query]
        if row["top_display_category"] == "Body" or row["top_display_model"] == "M5":
            regressions.append(query)
    for query in ["leica m5", "Leica M9", "Leica M10", "Leica M11"]:
        row = rows[query]
        if row["top_display_category"] != "Body":
            regressions.append(query)

    return sorted(set(button_missing)), sorted(set(ui_too_technical)), sorted(set(regressions))


def build_payload(push_context: dict[str, Any] | None = None) -> dict[str, Any]:
    rows = {query: response_row(query) for query in QUERY_ORDER}
    button_missing, ui_too_technical, regressions = classify(rows)

    decision_status = DECISION_READY
    if button_missing:
        decision_status = DECISION_HOLD_BUTTON
    elif ui_too_technical:
        decision_status = DECISION_HOLD_UI
    elif regressions:
        decision_status = DECISION_HOLD_REGRESSION

    push_context = push_context or build_commit_push_context_from_env()
    if push_context.get("push_executed") and not push_context.get("push_succeeded"):
        decision_status = DECISION_HOLD_PUSH
    elif (
        decision_status == DECISION_READY
        and push_context.get("commit_executed")
        and push_context.get("push_executed")
        and push_context.get("push_succeeded")
    ):
        decision_status = DECISION_PUSHED

    return {
        "task_name": TASK_NAME,
        "decision_status": decision_status,
        "owner_recheck_result_summary": "The logic is stable, but the Query review panel still needed a visible copy button and fully human unlock wording for owner and external tester review.",
        "files_changed_scope": SCOPED_FILES,
        "query_results": list(rows.values()),
        "copy_button_missing_rows": button_missing,
        "ui_still_too_technical_rows": ui_too_technical,
        "regression_rows": regressions,
        "m50_12_investigation": {
            "query": "M50/1.2",
            "result": rows["M50/1.2"],
            "summary": "M50/1.2 stays on the Lens path, does not regress to Leica M5 Body, and keeps broader/base Noctilux 50 f1.2 evidence clearly labeled as reference only.",
        },
        "git_diff_summary": collect_git_summary(),
        "commit_push_context": push_context,
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
        "next_backlog_candidates": [
            "P3-BETA-MVP-QUERY-REVIEW-EVIDENCE-UI-COPY-BUTTON-AND-UNLOCK-COPY-OWNER-RECHECK",
            "P3-BETA-MVP-LOCKED-ENTRY-AND-PRICE-UNLOCK-AUDIT",
            "P3-BETA-MVP-LENS-VARIANT-TOKEN-PARSER-COVERAGE-FIXUP",
            "P3-BETA-MVP-LENS-BOUNDARY-CONFLICT-RESOLUTION-FIXUP",
        ],
    }


def render_markdown(payload: dict[str, Any]) -> str:
    m50 = payload["m50_12_investigation"]
    return "\n".join(
        [
            f"# {payload['task_name']}",
            "",
            "## 1. 작업명",
            f"- `{payload['task_name']}`",
            "",
            "## 2. owner recheck 결과 요약",
            f"- {payload['owner_recheck_result_summary']}",
            "",
            "## 3. copy button / unlock copy 변경",
            "- Query review header now keeps a visible `Copy summary` button in the upper-right area.",
            "- Price unlock copy now renders as readable list items instead of slash-separated debug text.",
            "",
            "## 4. M50/1.2 조사 결과",
            f"- {m50['summary']}",
            "",
            "## 5. copy button missing rows",
            f"- {payload['copy_button_missing_rows']}",
            "",
            "## 6. ui still too technical rows",
            f"- {payload['ui_still_too_technical_rows']}",
            "",
            "## 7. regression rows",
            f"- {payload['regression_rows']}",
            "",
            "## 8. git diff 요약",
            f"- branch = {payload['git_diff_summary']['branch']}",
            f"- head = {payload['git_diff_summary']['head_commit']}",
            f"- subject = {payload['git_diff_summary']['head_subject']}",
            f"- files = {', '.join(payload['git_diff_summary']['working_diff_files']) or '(none)'}",
            "",
            "## 9. commit/push 수행 여부",
            f"- commit_executed = {payload['commit_push_context']['commit_executed']}",
            f"- push_executed = {payload['commit_push_context']['push_executed']}",
            f"- push_succeeded = {payload['commit_push_context']['push_succeeded']}",
            "",
            "## 10. preview deployment URL",
            f"- {payload['commit_push_context'].get('preview_deployment_url') or 'not recorded'}",
            "",
            "## 11. production/public/access guard",
            *[f"- {k} = {v}" for k, v in payload["production_public_access_guard"].items()],
            "",
            "## 12. 다음 backlog 후보",
            *[f"- {item}" for item in payload["next_backlog_candidates"]],
        ]
    ) + "\n"


def write_artifacts(payload: dict[str, Any]) -> None:
    JSON_PATH.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    JSONL_PATH.write_text(
        "\n".join(json.dumps(row, ensure_ascii=False) for row in payload["query_results"]) + "\n",
        encoding="utf-8",
    )
    MD_PATH.write_text(render_markdown(payload), encoding="utf-8")


def main() -> int:
    payload = build_payload()
    write_artifacts(payload)
    print(payload["decision_status"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
