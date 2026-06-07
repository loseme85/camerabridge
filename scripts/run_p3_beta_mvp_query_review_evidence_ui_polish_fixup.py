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


TASK_NAME = "P3-BETA-MVP-QUERY-REVIEW-EVIDENCE-UI-POLISH-FIXUP"
DECISION_PUSHED = "query_review_evidence_ui_polish_fixup_pushed_ready_for_owner_recheck"
DECISION_READY = "query_review_evidence_ui_polish_fixup_passed_ready_for_owner_approved_push"
DECISION_HOLD_DEV = "query_review_evidence_ui_polish_fixup_hold_dev_token_visible"
DECISION_HOLD_TECHNICAL = "query_review_evidence_ui_polish_fixup_hold_query_review_too_technical"
DECISION_HOLD_COPY = "query_review_evidence_ui_polish_fixup_hold_price_state_copy_confusing"
DECISION_HOLD_PROJECTION = "query_review_evidence_ui_polish_fixup_hold_price_projection_regressed"
DECISION_HOLD_BODY = "query_review_evidence_ui_polish_fixup_hold_body_lens_regression"
DECISION_HOLD_TESTS = "query_review_evidence_ui_polish_fixup_hold_tests_failed"
DECISION_HOLD_PUSH = "query_review_evidence_ui_polish_fixup_hold_push_or_preview_deploy_failed"

JSON_PATH = DATA_ADMIN / "query_review_evidence_ui_polish_fixup_v0.json"
JSONL_PATH = DATA_ADMIN / "p3_beta_mvp_query_review_evidence_ui_polish_fixup_v0.jsonl"
MD_PATH = DATA_ADMIN / "p3_beta_mvp_query_review_evidence_ui_polish_fixup_v0.md"

SCOPED_FILES = [
    "api/search.py",
    "app/templates/index.html",
    "index.html",
    "tests/test_beta_mvp_query_review_evidence_ui_polish_fixup.py",
    "scripts/run_p3_beta_mvp_query_review_evidence_ui_polish_fixup.py",
    "data/admin/p3_beta_mvp_query_review_evidence_ui_polish_fixup_v0.md",
    "data/admin/p3_beta_mvp_query_review_evidence_ui_polish_fixup_v0.jsonl",
    "data/admin/query_review_evidence_ui_polish_fixup_v0.json",
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

DEV_TOKENS = {
    "dangerous_unknown_family_token",
    "exact_model_like_match_missing",
    "no_exact_or_strong_visible_results",
    "weak_only_fallback",
    "third_party_top_domination",
    "too_wide_price_band",
}

TECHNICAL_TOKENS = {
    "exact_variant_pool",
    "exact_base_model_pool",
    "broader_family_pool",
    "query_incompatible",
    "Used for exact_variant_pool",
}

SAFE_COPY_FORBIDDEN = {
    "guaranteed valuation",
    "official leica value",
    "market price guaranteed",
    "investment recommendation",
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
        "display_top_result_evidence_count": len(response.get("display_top_result_evidence") or []),
        "display_evidence_pool_summary": response.get("display_evidence_pool_summary") or {},
        "display_price_summary_allowed": bool(response.get("display_price_summary_allowed")),
        "display_price_scope_label": response.get("display_price_scope_label"),
        "display_price_band": response.get("display_price_band"),
        "display_broader_reference_allowed": bool(response.get("display_broader_reference_allowed")),
        "display_broader_reference_label": response.get("display_broader_reference_label"),
        "display_broader_reference_band": response.get("display_broader_reference_band"),
        "display_broader_reference_locked_reason": response.get("display_broader_reference_locked_reason"),
        "display_price_band_quality_state": response.get("display_price_band_quality_state"),
        "display_unlock_requirements": list(response.get("display_unlock_requirements") or []),
        "display_match_state_message": response.get("display_match_state_message"),
        "price_summary_band": response.get("price_summary_band"),
        "broader_reference_band": response.get("broader_reference_band"),
        "top_display_category": top_display.get("display_category"),
        "top_display_model": top_display.get("display_model"),
        "top_result_title": top.get("title"),
        "top_result_source": top.get("source"),
        "top_result_price": top.get("price"),
        "top_result_evidence_preview": (response.get("display_top_result_evidence") or [])[:3],
        "policy_preview": {
            "market_entry_allowed": policy.get("market_entry_allowed"),
            "price_summary_allowed": policy.get("price_summary_allowed"),
            "broader_reference_allowed": policy.get("broader_reference_allowed"),
            "display_broader_reference_band": policy.get("display_broader_reference_band"),
            "display_price_band": policy.get("display_price_band"),
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


def _joined_user_facing_text(row: dict[str, Any]) -> str:
    values = [
        row.get("display_price_scope_label") or "",
        row.get("display_price_band") or "",
        row.get("display_broader_reference_label") or "",
        row.get("display_broader_reference_band") or "",
        row.get("display_broader_reference_locked_reason") or "",
        row.get("display_match_state_message") or "",
        (row.get("display_query_review") or {}).get("interpreted_target") or "",
        (row.get("display_query_review") or {}).get("price_status") or "",
        (row.get("display_query_review") or {}).get("why") or "",
        (row.get("display_query_review") or {}).get("evidence_summary") or "",
    ]
    for item in row.get("display_top_result_evidence") or []:
        values.extend(
            [
                item.get("result_role_label") or "",
                item.get("price_usage_label") or "",
                " ".join(item.get("excluded_reason") or []),
                item.get("evidence_pool_label") or "",
            ]
        )
    return " | ".join(values)


def classify_failures(rows: dict[str, dict[str, Any]]) -> tuple[list[str], list[str], list[str], list[str], list[str]]:
    dev_token_rows: list[str] = []
    technical_rows: list[str] = []
    confusing_copy_rows: list[str] = []
    price_projection_rows: list[str] = []
    body_lens_regressions: list[str] = []

    for query, row in rows.items():
        text = _joined_user_facing_text(row)
        if any(token in text for token in DEV_TOKENS):
            dev_token_rows.append(query)
        if any(token in text for token in TECHNICAL_TOKENS):
            technical_rows.append(query)
        if any(token in text.lower() for token in SAFE_COPY_FORBIDDEN):
            technical_rows.append(query)
        review = row.get("display_query_review") or {}
        if not review:
            technical_rows.append(query)
        if (
            not row["display_price_summary_allowed"]
            and (
                review.get("price_status") == "Exact price is available."
                or "Clean exact variant price evidence" in (review.get("why") or "")
            )
        ):
            confusing_copy_rows.append(query)
        if not row["display_broader_reference_allowed"] and row["display_broader_reference_band"]:
            price_projection_rows.append(query)
        if row["display_price_summary_allowed"] and row["display_price_band"] != row["price_summary_band"]:
            price_projection_rows.append(query)
        if row["display_broader_reference_allowed"] and row["display_broader_reference_band"] != row["broader_reference_band"]:
            price_projection_rows.append(query)

    for query in ["M50/1.2", "Leica M50/1.2 1세대"]:
        row = rows[query]
        if row["top_display_category"] == "Body" or row["top_display_model"] == "M5":
            body_lens_regressions.append(query)

    for query in ["leica m5", "Leica M9", "Leica M10", "Leica M11"]:
        row = rows[query]
        if row["top_display_category"] != "Body":
            body_lens_regressions.append(query)

    return (
        sorted(set(dev_token_rows)),
        sorted(set(technical_rows)),
        sorted(set(confusing_copy_rows)),
        sorted(set(price_projection_rows)),
        sorted(set(body_lens_regressions)),
    )


def build_payload(push_context: dict[str, Any] | None = None) -> dict[str, Any]:
    rows = {query: response_row(query) for query in QUERY_ORDER}
    (
        dev_token_rows,
        technical_rows,
        confusing_copy_rows,
        price_projection_rows,
        body_lens_regressions,
    ) = classify_failures(rows)

    decision_status = DECISION_READY
    if dev_token_rows:
        decision_status = DECISION_HOLD_DEV
    elif technical_rows:
        decision_status = DECISION_HOLD_TECHNICAL
    elif confusing_copy_rows:
        decision_status = DECISION_HOLD_COPY
    elif price_projection_rows:
        decision_status = DECISION_HOLD_PROJECTION
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

    payload = {
        "task_name": TASK_NAME,
        "decision_status": decision_status,
        "owner_recheck_summary": "Previous runtime projection fix passed functionally, but Query review still read like an owner-debug surface instead of external tester copy.",
        "ui_polish_why": "The panel now needs to explain search interpretation, price status, and evidence use without exposing internal pool names or debug tokens.",
        "query_review_design": {
            "default_mode": [
                "You searched",
                "Interpreted as",
                "Price status",
                "Why",
                "Evidence",
                "Needed to unlock",
                "Top evidence",
            ],
            "detail_mode": [
                "Show evidence details",
                "Result title",
                "Source name",
                "Price",
                "Result role",
                "Price usage",
                "Exclusion reason",
            ],
        },
        "copy_conversion_table": {
            "no_exact_or_strong_visible_results": "No exact strong visible listings yet.",
            "weak_only_fallback": "Results are visible, but not strong enough for model-level pricing.",
            "third_party_top_domination": "Top visible results include third-party or adjacent items.",
            "too_wide_price_band": "Reference prices are too spread out to show safely.",
            "dangerous_unknown_family_token": "Query includes a model-like term that needs verification.",
        },
        "result_role_labels": {
            "Exact variant": "Exact variant match",
            "Exact base model": "Same base model",
            "Broader family": "Broader family reference",
            "Third-party top result": "Third-party result",
            "Query incompatible": "Not compatible with this query",
        },
        "price_usage_labels": {
            "exact_variant_pool": "Used for exact price",
            "exact_base_model_pool": "Used for same-model price",
            "broader_family_pool": "Used as reference",
            "excluded:outlier": "Not used — Price outlier",
            "excluded:wrong_model": "Not used — Wrong model",
            "excluded:duplicate": "Not used — Duplicate listing",
            "excluded:accessory": "Not used — Accessory or part",
            "excluded:third_party": "Not used — Third-party item",
        },
        "query_results": list(rows.values()),
        "dev_token_visible_rows": dev_token_rows,
        "query_review_too_technical_rows": technical_rows,
        "price_state_copy_confusing_rows": confusing_copy_rows,
        "price_projection_regressed_rows": price_projection_rows,
        "body_lens_regression_rows": body_lens_regressions,
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
        "test_verdict": {
            "dev_token_visible": dev_token_rows,
            "query_review_too_technical": technical_rows,
            "price_state_copy_confusing": confusing_copy_rows,
            "price_projection_regressed": price_projection_rows,
            "body_lens_regression": body_lens_regressions,
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
    def line_for(query: str) -> str:
        row = rows[query]
        review = row.get("display_query_review") or {}
        return f"- `{query}`: {review.get('price_status')} / {review.get('why')}"

    lines = [
        f"# {payload['task_name']}",
        "",
        "## 1. 작업명",
        f"- `{payload['task_name']}`",
        "",
        "## 2. owner recheck 결과 요약",
        f"- {payload['owner_recheck_summary']}",
        "",
        "## 3. UI polish 필요 이유",
        f"- {payload['ui_polish_why']}",
        "",
        "## 4. Query review 기본/상세 모드 설계",
        "- 기본: 검색어 / 해석된 target / 가격 상태 / 이유 / evidence / unlock requirement / top evidence",
        "- 상세: 증거 행별 title / source / price / result role / price usage / exclusion reason",
        "",
        "## 5. 사용자용 copy 변환표",
        *[f"- `{k}` -> {v}" for k, v in payload["copy_conversion_table"].items()],
        "",
        "## 6. result role label 변환표",
        *[f"- `{k}` -> {v}" for k, v in payload["result_role_labels"].items()],
        "",
        "## 7. price usage label 변환표",
        *[f"- `{k}` -> {v}" for k, v in payload["price_usage_labels"].items()],
        "",
        "## 8. 35 lux aa 결과",
        line_for("35 lux aa"),
        "",
        "## 9. Noctilux 50 f1 E60 결과",
        line_for("Noctilux 50 f1 E60"),
        "",
        "## 10. Summicron 50 rigid 결과",
        line_for("Summicron 50 rigid"),
        "",
        "## 11. Summilux-M 50 ASPH 결과",
        line_for("Summilux-M 50 ASPH"),
        "",
        "## 12. Leica M5 / M50/1.2 body-lens boundary 결과",
        line_for("leica m5"),
        line_for("M50/1.2"),
        "",
        "## 13. dev token 노출 여부",
        f"- visible rows = {payload['dev_token_visible_rows']}",
        "",
        "## 14. external tester safe copy guard",
        "- forbidden phrases are blocked from display summary checks",
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
        *[f"- {k} = {v}" for k, v in payload["test_verdict"].items()],
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
