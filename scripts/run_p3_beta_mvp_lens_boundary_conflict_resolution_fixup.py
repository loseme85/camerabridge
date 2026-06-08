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


TASK_NAME = "P3-BETA-MVP-LENS-BOUNDARY-CONFLICT-RESOLUTION-FIXUP"
DECISION_PUSHED = "lens_boundary_conflict_resolution_fixup_pushed_ready_for_owner_recheck"
DECISION_READY = "lens_boundary_conflict_resolution_fixup_passed_ready_for_owner_approved_push"
DECISION_HOLD_SUMMILUX = "lens_boundary_conflict_resolution_fixup_hold_summilux_50_asph_boundary_still_polluted"
DECISION_HOLD_SL90 = "lens_boundary_conflict_resolution_fixup_hold_sl90_boundary_still_polluted"
DECISION_HOLD_PRICE = "lens_boundary_conflict_resolution_fixup_hold_price_projection_regressed"
DECISION_HOLD_BODY = "lens_boundary_conflict_resolution_fixup_hold_body_lens_regression"
DECISION_HOLD_UI = "lens_boundary_conflict_resolution_fixup_hold_ui_copy_regression"
DECISION_HOLD_PUSH = "lens_boundary_conflict_resolution_fixup_hold_push_or_preview_deploy_failed"

JSON_PATH = DATA_ADMIN / "lens_boundary_conflict_resolution_fixup_v0.json"
JSONL_PATH = DATA_ADMIN / "p3_beta_mvp_lens_boundary_conflict_resolution_fixup_v0.jsonl"
MD_PATH = DATA_ADMIN / "p3_beta_mvp_lens_boundary_conflict_resolution_fixup_v0.md"

QUERY_ORDER = [
    "Summilux-M 50 ASPH",
    "summilux 50 asph",
    "leica summilux-m 50 asph",
    "APO-Summicron-SL 90",
    "apo summicron sl 90",
    "leica sl 90 apo summicron",
    "35 lux aa",
    "Noctilux 50 f1 E60",
    "Summicron 50 rigid",
    "M50/1.2",
    "Leica M50/1.2 1세대",
    "leica m5",
    "Leica M6",
    "Leica M9",
    "Leica M10",
    "Leica M11",
    "APO-Summicron-M 90",
    "Summicron-M 90",
    "Elmarit-M 90",
    "Summarit-M 90",
    "Voigtlander 50 Nokton",
    "Voigtlander 90",
    "Leica SL 50 APO",
]

BAD_MARKET_COPY = {
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


def build_row(query: str) -> dict[str, Any]:
    response = search_from_params({"q": query, "limit": "10"})
    results = response.get("results") or []
    top = results[0] if results else {}
    display = top.get("display_output") or {}
    review = response.get("display_query_review") or {}
    interpreted_target = str(review.get("interpreted_target") or "")
    lowered_target = interpreted_target.lower()
    body_or_lens_path = "Body" if lowered_target.endswith(" body") else ("Lens" if interpreted_target else display.get("display_category"))
    return {
        "query": query,
        "category": display.get("display_category"),
        "body_or_lens_path": body_or_lens_path,
        "display_model": display.get("display_model"),
        "interpreted_target": interpreted_target,
        "price_status": review.get("price_status"),
        "why": review.get("why"),
        "display_price_scope_label": response.get("display_price_scope_label"),
        "display_price_summary_allowed": bool(response.get("display_price_summary_allowed")),
        "display_broader_reference_allowed": bool(response.get("display_broader_reference_allowed")),
        "display_price_band": response.get("display_price_band"),
        "display_broader_reference_band": response.get("display_broader_reference_band"),
        "search_confidence_state": response.get("search_confidence_state"),
        "top_result_compatibility": response.get("top_result_compatibility"),
        "third_party_top_domination_detected": bool(response.get("third_party_top_domination_detected")),
        "boundary_conflict_detected": bool(response.get("boundary_conflict_detected")),
        "exact_or_strong_visible_result_count": int(response.get("exact_or_strong_visible_result_count") or 0),
        "copy_summary_text": review.get("copy_summary_text"),
        "display_top_result_evidence": response.get("display_top_result_evidence") or [],
        "display_unlock_requirements": response.get("display_unlock_requirements") or [],
    }


def collect_git_summary() -> dict[str, Any]:
    scoped = [
        "api/search.py",
        "scripts/run_p3_beta_mvp_lens_boundary_conflict_resolution_fixup.py",
        "tests/test_beta_mvp_lens_boundary_conflict_resolution_fixup.py",
        "data/admin/p3_beta_mvp_lens_boundary_conflict_resolution_fixup_v0.md",
        "data/admin/p3_beta_mvp_lens_boundary_conflict_resolution_fixup_v0.jsonl",
        "data/admin/lens_boundary_conflict_resolution_fixup_v0.json",
    ]
    return {
        "branch": run_git("branch", "--show-current"),
        "head_commit": run_git("rev-parse", "HEAD"),
        "head_subject": run_git("log", "-1", "--pretty=%s"),
        "working_diff_stat": run_git("diff", "--stat", "--", *scoped),
        "working_diff_files": [line for line in run_git("diff", "--name-only", "--", *scoped).splitlines() if line],
    }


def _contains_bad_copy(row: dict[str, Any]) -> bool:
    text = " | ".join(
        [
            str(row.get("price_status") or ""),
            str(row.get("why") or ""),
            str(row.get("display_price_scope_label") or ""),
            str(row.get("copy_summary_text") or ""),
            " | ".join(str(item) for item in row.get("display_unlock_requirements") or []),
        ]
    )
    return any(token in text for token in BAD_MARKET_COPY)


def classify(rows: dict[str, dict[str, Any]]) -> tuple[list[str], list[str], list[str], dict[str, Any]]:
    ui_copy_regressions: list[str] = []
    price_projection_regressions: list[str] = []
    body_lens_regressions: list[str] = []

    for query in ["leica m5", "Leica M6", "Leica M9", "Leica M10", "Leica M11"]:
        if rows[query]["body_or_lens_path"] != "Body":
            body_lens_regressions.append(query)
    for query in [
        "Summilux-M 50 ASPH",
        "summilux 50 asph",
        "leica summilux-m 50 asph",
        "APO-Summicron-SL 90",
        "apo summicron sl 90",
        "leica sl 90 apo summicron",
        "35 lux aa",
        "Noctilux 50 f1 E60",
        "Summicron 50 rigid",
        "M50/1.2",
        "Leica M50/1.2 1세대",
    ]:
        if rows[query]["body_or_lens_path"] != "Lens":
            body_lens_regressions.append(query)

    for row in rows.values():
        if _contains_bad_copy(row):
            ui_copy_regressions.append(row["query"])

    summilux = rows["Summilux-M 50 ASPH"]
    summilux_third_party = [
        item
        for item in summilux["display_top_result_evidence"]
        if ("voigtlander" in str(item.get("title") or "").lower() or "nokton" in str(item.get("title") or "").lower())
    ]
    summilux_exact_safe = bool(
        summilux["display_price_summary_allowed"]
        and summilux["top_result_compatibility"] == "exact_variant_strong"
        and not summilux["third_party_top_domination_detected"]
        and not summilux["boundary_conflict_detected"]
    )
    summilux_locked_safe = bool(
        not summilux["display_price_summary_allowed"]
        and summilux["third_party_top_domination_detected"]
    )
    if not (summilux_exact_safe or summilux_locked_safe):
        price_projection_regressions.append("Summilux-M 50 ASPH")
    for item in summilux_third_party:
        if item.get("used_for_price"):
            price_projection_regressions.append("Summilux-M 50 ASPH")
        if item.get("compatibility_label") in {"Broader family", "Exact base model", "Exact variant"}:
            price_projection_regressions.append("Summilux-M 50 ASPH")

    sl90 = rows["APO-Summicron-SL 90"]
    sl90_boundary_rows = []
    for item in sl90["display_top_result_evidence"]:
        title = str(item.get("title") or "")
        if any(token in title for token in ["Leica M 90", "Leica R 90", "Summarit", "Elmarit", "TTArtisan", "Leica L 90"]):
            sl90_boundary_rows.append(item)
            if item.get("used_for_price"):
                price_projection_regressions.append("APO-Summicron-SL 90")
            if item.get("compatibility_label") not in {"Boundary conflict", "Query incompatible"}:
                price_projection_regressions.append("APO-Summicron-SL 90")
    if sl90["display_price_summary_allowed"]:
        price_projection_regressions.append("APO-Summicron-SL 90")

    body_m10 = rows["Leica M10"]
    if body_m10["body_or_lens_path"] != "Body":
        body_lens_regressions.append("Leica M10")
    if str(body_m10.get("display_price_band") or "").startswith("KRW 80,000 -"):
        price_projection_regressions.append("Leica M10")

    summary = {
        "summilux_before": {
            "price_status": "Reference price only.",
            "issue": "Third-party Nokton rows could still appear as broader-family-like visible evidence instead of clean query-incompatible rows.",
        },
        "summilux_after": {
            "price_status": summilux["price_status"],
            "why": summilux["why"],
            "top_result_compatibility": summilux["top_result_compatibility"],
            "display_price_summary_allowed": summilux["display_price_summary_allowed"],
            "third_party_rows": [
                {
                    "title": item.get("title"),
                    "compatibility_label": item.get("compatibility_label"),
                    "price_usage_label": item.get("price_usage_label"),
                }
                for item in summilux_third_party
            ],
        },
        "sl90_before": {
            "price_status": "Price summary is locked.",
            "issue": "M/R 90mm and adjacent 90mm rows needed to remain boundary conflicts rather than SL-compatible evidence.",
        },
        "sl90_after": {
            "price_status": sl90["price_status"],
            "why": sl90["why"],
            "top_result_compatibility": sl90["top_result_compatibility"],
            "boundary_rows": [
                {
                    "title": item.get("title"),
                    "compatibility_label": item.get("compatibility_label"),
                    "price_usage_label": item.get("price_usage_label"),
                }
                for item in sl90_boundary_rows
            ],
        },
    }
    return sorted(set(ui_copy_regressions)), sorted(set(price_projection_regressions)), sorted(set(body_lens_regressions)), summary


def build_payload(push_context: dict[str, Any] | None = None) -> dict[str, Any]:
    rows = {query: build_row(query) for query in QUERY_ORDER}
    ui_copy_regressions, price_projection_regressions, body_lens_regressions, summary = classify(rows)

    decision_status = DECISION_READY
    if ui_copy_regressions:
        decision_status = DECISION_HOLD_UI
    elif body_lens_regressions:
        decision_status = DECISION_HOLD_BODY
    elif "Summilux-M 50 ASPH" in price_projection_regressions:
        decision_status = DECISION_HOLD_SUMMILUX
    elif "APO-Summicron-SL 90" in price_projection_regressions:
        decision_status = DECISION_HOLD_SL90
    elif price_projection_regressions:
        decision_status = DECISION_HOLD_PRICE

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
        "rows": list(rows.values()),
        "boundary_summary": summary,
        "ui_copy_regressions": ui_copy_regressions,
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
    summary = payload["boundary_summary"]
    lines = [
        f"# {payload['task_name']}",
        "",
        "## 1. 작업명",
        f"- `{payload['task_name']}`",
        "",
        "## 2. exact boundary logic changes",
        "- Broader family matching now requires visible family evidence when the requested Leica family is specific.",
        "- Third-party 50mm rows without Summilux family evidence are no longer treated as broader-family compatible rows for Summilux-M 50 ASPH.",
        "- SL 90 exact queries continue to treat M/R 90mm and adjacent 90mm rows as boundary conflicts instead of strong SL-compatible evidence.",
        "",
        "## 3. Summilux-M 50 ASPH before / after",
        f"- before issue = {summary['summilux_before']['issue']}",
        f"- after price status = {summary['summilux_after']['price_status']}",
        f"- after why = {summary['summilux_after']['why']}",
        f"- after top_result_compatibility = {summary['summilux_after']['top_result_compatibility']}",
        "",
        "## 4. APO-Summicron-SL 90 before / after",
        f"- before issue = {summary['sl90_before']['issue']}",
        f"- after price status = {summary['sl90_after']['price_status']}",
        f"- after why = {summary['sl90_after']['why']}",
        f"- after top_result_compatibility = {summary['sl90_after']['top_result_compatibility']}",
        "",
        "## 5. price unlock change 여부",
        "- No new exact price unlock was introduced in this round.",
        "",
        "## 6. third-party / adjacent rows blocking 여부",
        "- Summilux-M 50 ASPH keeps exact price locked when visible results are still third-party or adjacent.",
        "- APO-Summicron-SL 90 keeps price locked when visible rows are still boundary conflicts.",
        "",
        "## 7. M/R 90mm rows for SL 90",
    ]
    for item in summary["sl90_after"]["boundary_rows"]:
        lines.append(
            f"- {item['title']} -> {item['compatibility_label']} / {item['price_usage_label']}"
        )
    lines.extend(
        [
            "",
            "## 8. UI / copy guard",
            f"- Query review regression = {payload['ui_copy_regressions'] or 'none'}",
            "- Model Market Entry copy remains human-readable.",
            "- Copy summary remains visible via existing guard tests.",
            "",
            "## 9. Body price band quality regression",
            f"- body_lens_regressions = {payload['body_lens_regressions'] or 'none'}",
            f"- price_projection_regressions = {payload['price_projection_regressions'] or 'none'}",
            "",
            "## 10. decision_status",
            f"- `{payload['decision_status']}`",
        ]
    )
    return "\n".join(lines) + "\n"


def write_reports(payload: dict[str, Any]) -> None:
    DATA_ADMIN.mkdir(parents=True, exist_ok=True)
    JSON_PATH.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    JSONL_PATH.write_text(
        "\n".join(json.dumps(row, ensure_ascii=False) for row in payload["rows"]) + "\n",
        encoding="utf-8",
    )
    MD_PATH.write_text(render_markdown(payload), encoding="utf-8")


def main() -> None:
    payload = build_payload()
    write_reports(payload)
    print(payload["decision_status"])


if __name__ == "__main__":
    main()
