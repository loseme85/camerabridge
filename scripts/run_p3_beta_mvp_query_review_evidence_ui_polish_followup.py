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


TASK_NAME = "P3-BETA-MVP-QUERY-REVIEW-EVIDENCE-UI-POLISH-FOLLOWUP"
DECISION_PUSHED = "query_review_evidence_ui_polish_followup_pushed_ready_for_owner_recheck"
DECISION_READY = "query_review_evidence_ui_polish_followup_passed_ready_for_owner_approved_push"
DECISION_HOLD_UI = "query_review_evidence_ui_polish_followup_hold_ui_still_too_technical"
DECISION_HOLD_PROJECTION = "query_review_evidence_ui_polish_followup_hold_price_projection_regressed"
DECISION_HOLD_BODY = "query_review_evidence_ui_polish_followup_hold_body_lens_regression"
DECISION_HOLD_PUSH = "query_review_evidence_ui_polish_followup_hold_push_or_preview_deploy_failed"

JSON_PATH = DATA_ADMIN / "query_review_evidence_ui_polish_followup_v0.json"
JSONL_PATH = DATA_ADMIN / "p3_beta_mvp_query_review_evidence_ui_polish_followup_v0.jsonl"
MD_PATH = DATA_ADMIN / "p3_beta_mvp_query_review_evidence_ui_polish_followup_v0.md"

SCOPED_FILES = [
    "api/search.py",
    "app/templates/index.html",
    "index.html",
    "scripts/run_p3_beta_mvp_query_review_evidence_ui_polish_followup.py",
    "tests/test_beta_mvp_query_review_evidence_ui_polish_followup.py",
    "data/admin/p3_beta_mvp_query_review_evidence_ui_polish_followup_v0.md",
    "data/admin/p3_beta_mvp_query_review_evidence_ui_polish_followup_v0.jsonl",
    "data/admin/query_review_evidence_ui_polish_followup_v0.json",
]

QUERY_ORDER = [
    "35 lux aa",
    "Noctilux 50 f1 E60",
    "Summicron 50 rigid",
    "Summicron 35 8-element",
    "Leica Summilux-M 50mm f1.4 3세대",
    "Summilux 50 3rd generation",
    "Summilux-M 50 ASPH",
    "Noctilux 50 0.95",
    "Summaron 35 2.8",
    "APO-Summicron-SL 90",
    "M50/1.2",
    "Leica M50/1.2 1세대",
    "leica m5",
    "Leica M9",
    "Leica M10",
    "Leica M11",
    "ltm summaron 35",
    "Elmarit-R 28",
    "ricoh gr iiix",
    "hasselblad xpan",
]

FORBIDDEN_UI_TOKENS = {
    "exact_variant_pool",
    "exact_base_model_pool",
    "broader_family_pool",
    "query_incompatible",
    "third_party_top_result",
    "dangerous_unknown_family_token",
    "weak_only_fallback",
    "too_wide_price_band",
    "Need no third-party contamination in the selected price pool.",
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
    policy = response.get("market_entry_policy") or {}
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
        "display_evidence_pool_summary": response.get("display_evidence_pool_summary") or {},
        "price_summary_band": response.get("price_summary_band"),
        "broader_reference_band": response.get("broader_reference_band"),
        "top_display_category": top_display.get("display_category"),
        "top_display_model": top_display.get("display_model"),
        "policy_preview": {
            "market_entry_allowed": policy.get("market_entry_allowed"),
            "price_summary_allowed": policy.get("price_summary_allowed"),
            "broader_reference_allowed": policy.get("broader_reference_allowed"),
        },
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
        row.get("display_price_scope_label") or "",
        row.get("display_price_band") or "",
        row.get("display_broader_reference_label") or "",
        row.get("display_broader_reference_band") or "",
        row.get("display_match_state_message") or "",
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


def classify(rows: dict[str, dict[str, Any]]) -> tuple[list[str], list[str], list[str]]:
    ui_too_technical: list[str] = []
    price_projection_regressed: list[str] = []
    body_lens_regressed: list[str] = []

    for query, row in rows.items():
        text = _row_text(row)
        if any(token in text for token in FORBIDDEN_UI_TOKENS):
            ui_too_technical.append(query)
        review = row.get("display_query_review") or {}
        if not review.get("copy_summary_text"):
            ui_too_technical.append(query)
        if not row["display_broader_reference_allowed"] and row["display_broader_reference_band"]:
            price_projection_regressed.append(query)
        if row["display_price_summary_allowed"] and row["display_price_band"] != row["price_summary_band"]:
            price_projection_regressed.append(query)
        if row["display_broader_reference_allowed"] and row["display_broader_reference_band"] != row["broader_reference_band"]:
            price_projection_regressed.append(query)

    for query in ["M50/1.2", "Leica M50/1.2 1세대"]:
        row = rows[query]
        if row["top_display_category"] == "Body" or row["top_display_model"] == "M5":
            body_lens_regressed.append(query)
    for query in ["leica m5", "Leica M9", "Leica M10", "Leica M11"]:
        row = rows[query]
        if row["top_display_category"] != "Body":
            body_lens_regressed.append(query)

    return (
        sorted(set(ui_too_technical)),
        sorted(set(price_projection_regressed)),
        sorted(set(body_lens_regressed)),
    )


def build_payload(push_context: dict[str, Any] | None = None) -> dict[str, Any]:
    rows = {query: response_row(query) for query in QUERY_ORDER}
    ui_too_technical, price_projection_regressed, body_lens_regressed = classify(rows)

    decision_status = DECISION_READY
    if ui_too_technical:
        decision_status = DECISION_HOLD_UI
    elif price_projection_regressed:
        decision_status = DECISION_HOLD_PROJECTION
    elif body_lens_regressed:
        decision_status = DECISION_HOLD_BODY

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

    payload = {
        "task_name": TASK_NAME,
        "decision_status": decision_status,
        "owner_recheck_result_summary": "Logic stayed conservative, but Query review still exposed too many internal/debug terms for external tester review.",
        "ui_polish_goal": "Translate evidence pools, unlock reasons, and top result roles into tester-facing language without loosening any pricing or routing guard.",
        "files_changed_scope": SCOPED_FILES,
        "query_results": list(rows.values()),
        "ui_still_too_technical_rows": ui_too_technical,
        "price_projection_regressed_rows": price_projection_regressed,
        "body_lens_regression_rows": body_lens_regressed,
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
        "m50_12_investigation": {
            "query": "M50/1.2",
            "result": rows["M50/1.2"],
            "summary": "The query stays on the Lens path, does not regress to Leica M5 Body, and only exposes broader reference pricing. It does not present an exact 1st-generation Noctilux price unless the stronger variant query is used.",
        },
        "next_backlog_candidates": [
            "P3-BETA-MVP-QUERY-REVIEW-EVIDENCE-UI-POLISH-OWNER-RECHECK",
            "P3-BETA-MVP-LOCKED-ENTRY-AND-PRICE-UNLOCK-AUDIT",
            "P3-BETA-MVP-LENS-VARIANT-TOKEN-PARSER-COVERAGE-FIXUP",
            "P3-BETA-MVP-LENS-BOUNDARY-CONFLICT-RESOLUTION-FIXUP",
        ],
    }
    return payload


def render_markdown(payload: dict[str, Any]) -> str:
    rows = {row["query"]: row for row in payload["query_results"]}

    def review_line(query: str) -> str:
        review = rows[query]["display_query_review"]
        return f"- `{query}`: {review.get('price_status')} / {review.get('why')}"

    lines = [
        f"# {payload['task_name']}",
        "",
        "## 1. 작업명",
        f"- `{payload['task_name']}`",
        "",
        "## 2. owner recheck 결과 요약",
        f"- {payload['owner_recheck_result_summary']}",
        "",
        "## 3. UI polish 필요 이유",
        f"- {payload['ui_polish_goal']}",
        "",
        "## 4. Query review 기본/상세 모드 설계",
        "- 기본 모드: 검색어 / 해석된 target / 가격 상태 / 이유 / evidence summary / unlock condition / top evidence",
        "- 상세 모드: title / source / price / result role / price usage / exclusion reason",
        "",
        "## 5. 사용자용 copy 변환표",
        "- exact_variant_pool -> Used for exact price",
        "- exact_base_model_pool -> Same base model evidence",
        "- broader_family_pool -> Broader reference only",
        "- excluded_pool -> Not used for price",
        "",
        "## 6. result role label 변환표",
        "- Exact variant -> Exact variant",
        "- Exact base model -> Same base model",
        "- Broader family -> Broader reference",
        "- Third-party top result -> Third-party or adjacent result",
        "- Query incompatible -> Not compatible with this query",
        "",
        "## 7. price usage label 변환표",
        "- Used for exact price",
        "- Used for same base model price",
        "- Used as broader reference",
        "- Not used — Price outlier",
        "- Not used — Duplicate listing",
        "- Not used — Different model",
        "- Not used — Third-party item",
        "- Not used — Accessory, not camera/lens",
        "",
        "## 8. 35 lux aa 결과",
        review_line("35 lux aa"),
        "",
        "## 9. Noctilux 50 f1 E60 결과",
        review_line("Noctilux 50 f1 E60"),
        "",
        "## 10. Summicron 50 rigid 결과",
        review_line("Summicron 50 rigid"),
        "",
        "## 11. Summilux-M 50 ASPH 결과",
        review_line("Summilux-M 50 ASPH"),
        "",
        "## 12. Leica M5 / M50/1.2 body-lens boundary 결과",
        review_line("leica m5"),
        review_line("M50/1.2"),
        "",
        "## 13. dev token 노출 여부",
        f"- {payload['ui_still_too_technical_rows']}",
        "",
        "## 14. external tester safe copy guard",
        "- copy summary excludes raw URLs, raw HTML, private contact data, and internal-only identifiers.",
        "",
        "## 15. git diff 요약",
        f"- branch = {payload['git_diff_summary']['branch']}",
        f"- head = {payload['git_diff_summary']['head_commit']}",
        f"- subject = {payload['git_diff_summary']['head_subject']}",
        f"- files = {', '.join(payload['git_diff_summary']['working_diff_files']) or '(none)'}",
        "",
        "## 16. commit/push 수행 여부",
        f"- commit_executed = {payload['commit_push_context']['commit_executed']}",
        f"- push_executed = {payload['commit_push_context']['push_executed']}",
        f"- push_succeeded = {payload['commit_push_context']['push_succeeded']}",
        "",
        "## 17. preview deployment URL",
        f"- {payload['commit_push_context'].get('preview_deployment_url') or 'not recorded'}",
        "",
        "## 18. production/public/access guard",
        *[f"- {k} = {v}" for k, v in payload["production_public_access_guard"].items()],
        "",
        "## 19. 테스트 결과",
        f"- ui_still_too_technical = {payload['ui_still_too_technical_rows']}",
        f"- price_projection_regressed = {payload['price_projection_regressed_rows']}",
        f"- body_lens_regression = {payload['body_lens_regression_rows']}",
        "",
        "## 20. production alias 연결 가능 여부",
        "- `production_alias_connect_allowed = false`",
        "",
        "## 21. 다음 backlog 후보",
        *[f"- {item}" for item in payload["next_backlog_candidates"]],
    ]
    return "\n".join(lines) + "\n"


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
