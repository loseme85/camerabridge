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


TASK_NAME = "P3-BETA-MVP-MODEL-MARKET-ENTRY-UI-COPY-PROJECTION-FIXUP"
DECISION_PUSHED = "model_market_entry_ui_copy_projection_fixup_pushed_ready_for_owner_recheck"
DECISION_READY = "model_market_entry_ui_copy_projection_fixup_passed_ready_for_owner_approved_push"
DECISION_HOLD_UI = "model_market_entry_ui_copy_projection_fixup_hold_ui_still_too_technical"
DECISION_HOLD_QUERY_REVIEW = "model_market_entry_ui_copy_projection_fixup_hold_query_review_regression"
DECISION_HOLD_PRICE = "model_market_entry_ui_copy_projection_fixup_hold_price_projection_regressed"
DECISION_HOLD_BODY = "model_market_entry_ui_copy_projection_fixup_hold_body_lens_regression"
DECISION_HOLD_PUSH = "model_market_entry_ui_copy_projection_fixup_hold_push_or_preview_deploy_failed"

JSON_PATH = DATA_ADMIN / "model_market_entry_ui_copy_projection_fixup_v0.json"
JSONL_PATH = DATA_ADMIN / "p3_beta_mvp_model_market_entry_ui_copy_projection_fixup_v0.jsonl"
MD_PATH = DATA_ADMIN / "p3_beta_mvp_model_market_entry_ui_copy_projection_fixup_v0.md"

QUERY_ORDER = [
    "35 lux aa",
    "Noctilux 50 f1 E60",
    "Summicron 50 rigid",
    "Summilux-M 50 ASPH",
    "M50/1.2",
    "Leica M50/1.2 1세대",
    "leica m5",
    "Leica M6",
    "Leica M9",
    "Leica M10",
    "Leica M11",
    "APO-Summicron-SL 90",
]

FORBIDDEN_MARKET_ENTRY_SNIPPETS = {
    "display_price_band_source || 'locked'} / excluded",
    "display_price_band_source || 'locked'} / cleaned",
    "unlockRequirements.slice(0, 2).join(' / ')",
    "Need cleaner exact evidence",
}
FORBIDDEN_USER_TOKENS = {
    "undefined",
    "exact_variant / cleaned",
    "exact_base_model / cleaned",
    "broader_family / cleaned",
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


def _read_render_market_entry_snippet() -> str:
    text = APP_TEMPLATE.read_text(encoding="utf-8")
    start = text.find("function renderMarketEntry(results, uiHints){")
    end = text.find("function renderCard(result){")
    if start == -1 or end == -1:
        return text
    return text[start:end]


def _market_entry_label(response: dict[str, Any]) -> str:
    review = response.get("display_query_review") or {}
    category = str(review.get("category") or "").lower()
    if category == "body":
        return "Body market summary"
    if response.get("display_price_summary_allowed"):
        source = str(response.get("display_price_band_source") or "")
        if source == "exact_variant":
            return "Exact price"
        if source == "exact_base_model":
            return "Same model price"
    if response.get("display_broader_reference_allowed"):
        return "Reference price only"
    return "Price locked"


def _market_entry_value(response: dict[str, Any]) -> str:
    if response.get("display_price_summary_allowed"):
        return str(response.get("display_price_band") or "Not enough evidence yet.")
    if response.get("display_broader_reference_allowed"):
        return str(response.get("display_broader_reference_band") or "Not enough evidence yet.")
    return "Not enough evidence yet."


def build_row(query: str) -> dict[str, Any]:
    response = search_from_params({"q": query, "limit": "12"})
    review = response.get("display_query_review") or {}
    results = response.get("results") or []
    top = results[0] if results else {}
    display = top.get("display_output") or {}
    top_evidence = response.get("display_top_result_evidence") or []
    return {
        "query": query,
        "category": display.get("display_category"),
        "display_model": display.get("display_model"),
        "interpreted_target": review.get("interpreted_target"),
        "price_status": review.get("price_status"),
        "why": review.get("why"),
        "market_entry_label": _market_entry_label(response),
        "market_entry_value": _market_entry_value(response),
        "display_price_summary_allowed": bool(response.get("display_price_summary_allowed")),
        "display_broader_reference_allowed": bool(response.get("display_broader_reference_allowed")),
        "display_broader_reference_label": response.get("display_broader_reference_label"),
        "display_broader_reference_band": response.get("display_broader_reference_band"),
        "display_unlock_requirements": list(response.get("display_unlock_requirements") or []),
        "display_query_review": review,
        "display_top_result_evidence": top_evidence,
    }


def collect_git_summary() -> dict[str, Any]:
    scoped = [
        "app/templates/index.html",
        "index.html",
        "scripts/run_p3_beta_mvp_model_market_entry_ui_copy_projection_fixup.py",
        "tests/test_beta_mvp_model_market_entry_ui_copy_projection_fixup.py",
        "data/admin/p3_beta_mvp_model_market_entry_ui_copy_projection_fixup_v0.md",
        "data/admin/p3_beta_mvp_model_market_entry_ui_copy_projection_fixup_v0.jsonl",
        "data/admin/model_market_entry_ui_copy_projection_fixup_v0.json",
    ]
    return {
        "branch": run_git("branch", "--show-current"),
        "head_commit": run_git("rev-parse", "HEAD"),
        "head_subject": run_git("log", "-1", "--pretty=%s"),
        "working_diff_stat": run_git("diff", "--stat", "--", *scoped),
        "working_diff_files": [line for line in run_git("diff", "--name-only", "--", *scoped).splitlines() if line],
    }


def classify(rows: list[dict[str, Any]]) -> tuple[list[str], list[str], list[str]]:
    ui_still_too_technical: list[str] = []
    query_review_regressions: list[str] = []
    price_projection_regressions: list[str] = []
    body_lens_regressions: list[str] = []

    snippet = _read_render_market_entry_snippet()
    if any(token in snippet for token in FORBIDDEN_MARKET_ENTRY_SNIPPETS):
        ui_still_too_technical.append("renderMarketEntry")

    template_text = APP_TEMPLATE.read_text(encoding="utf-8") + "\n" + ROOT_TEMPLATE.read_text(encoding="utf-8")
    if "Copy summary" not in template_text or "data-copy-query-review" not in template_text:
        query_review_regressions.append("copy_summary_button")

    for row in rows:
        joined = " | ".join(
            [
                str(row.get("market_entry_label") or ""),
                str(row.get("market_entry_value") or ""),
                str(row.get("why") or ""),
                " ".join(row.get("display_unlock_requirements") or []),
                str((row.get("display_query_review") or {}).get("copy_summary_text") or ""),
            ]
        )
        if any(token in joined for token in FORBIDDEN_USER_TOKENS):
            ui_still_too_technical.append(row["query"])

        if row["query"] in {"M50/1.2", "Leica M50/1.2 1세대"} and row["category"] == "Body":
            body_lens_regressions.append(row["query"])
        if row["query"] in {"leica m5", "Leica M6", "Leica M9", "Leica M10", "Leica M11"} and row["category"] != "Body":
            body_lens_regressions.append(row["query"])

        if row["query"] == "35 lux aa" and row["market_entry_label"] not in {"Reference price only", "Price locked"}:
            price_projection_regressions.append(row["query"])
        if row["query"] == "Summicron 50 rigid" and row["market_entry_label"] != "Exact price":
            price_projection_regressions.append(row["query"])
        if row["query"] == "leica m5" and row["market_entry_label"] != "Body market summary":
            price_projection_regressions.append(row["query"])

    return (
        sorted(set(ui_still_too_technical)),
        sorted(set(query_review_regressions)),
        sorted(set(price_projection_regressions)),
        sorted(set(body_lens_regressions)),
    )


def build_payload(push_context: dict[str, Any] | None = None) -> dict[str, Any]:
    rows = [build_row(query) for query in QUERY_ORDER]
    ui_still_too_technical, query_review_regressions, price_projection_regressions, body_lens_regressions = classify(rows)

    decision_status = DECISION_READY
    if ui_still_too_technical:
        decision_status = DECISION_HOLD_UI
    elif query_review_regressions:
        decision_status = DECISION_HOLD_QUERY_REVIEW
    elif price_projection_regressions:
        decision_status = DECISION_HOLD_PRICE
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
    ):
        decision_status = DECISION_PUSHED

    return {
        "task_name": TASK_NAME,
        "decision_status": decision_status,
        "query_count": len(rows),
        "rows": rows,
        "ui_still_too_technical_rows": ui_still_too_technical,
        "query_review_regressions": query_review_regressions,
        "price_projection_regressions": price_projection_regressions,
        "body_lens_regressions": body_lens_regressions,
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
    }


def render_markdown(payload: dict[str, Any]) -> str:
    lines = [
        f"# {payload['task_name']}",
        "",
        "## 1. 작업명",
        f"- `{payload['task_name']}`",
        "",
        "## 2. exact copy changes",
        "- Model Market Entry now uses `Exact price`, `Same model price`, `Reference price only`, `Price locked`, and `Body market summary` instead of raw scope text.",
        "- Unlock requirements now reuse the same human wording already used in Query review and render as list-style text instead of slash-joined debug text.",
        "- Price evidence now shows the human summary sentence from the evidence pool summary instead of raw internal scope tokens.",
        "",
        "## 3. per-query status",
    ]
    for row in payload["rows"]:
        lines.extend(
            [
                f"### {row['query']}",
                f"- category = {row['category']}",
                f"- interpreted_target = {row['interpreted_target']}",
                f"- market_entry_label = {row['market_entry_label']}",
                f"- market_entry_value = {row['market_entry_value']}",
                f"- price_status = {row['price_status']}",
                f"- why = {row['why']}",
            ]
        )
    lines.extend(
        [
            "",
            "## 4. regression status",
            f"- ui_still_too_technical = {payload['ui_still_too_technical_rows']}",
            f"- query_review_regressions = {payload['query_review_regressions']}",
            f"- price_projection_regressions = {payload['price_projection_regressions']}",
            f"- body_lens_regressions = {payload['body_lens_regressions']}",
            "",
            "## 5. preview / push context",
            f"- preview_url = {payload['commit_push_context'].get('preview_deployment_url') or 'not recorded'}",
            f"- commit_executed = {payload['commit_push_context']['commit_executed']}",
            f"- push_executed = {payload['commit_push_context']['push_executed']}",
            f"- push_succeeded = {payload['commit_push_context']['push_succeeded']}",
        ]
    )
    return "\n".join(lines) + "\n"


def write_artifacts(payload: dict[str, Any]) -> None:
    JSON_PATH.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    JSONL_PATH.write_text(
        "\n".join(json.dumps(row, ensure_ascii=False) for row in payload["rows"]) + "\n",
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
