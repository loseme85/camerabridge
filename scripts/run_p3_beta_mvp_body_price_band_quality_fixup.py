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


TASK_NAME = "P3-BETA-MVP-BODY-PRICE-BAND-QUALITY-FIXUP"
DECISION_PUSHED = "body_price_band_quality_fixup_pushed_ready_for_owner_recheck"
DECISION_READY = "body_price_band_quality_fixup_passed_ready_for_owner_approved_push"
DECISION_HOLD_M10 = "body_price_band_quality_fixup_hold_m10_band_still_noisy"
DECISION_HOLD_BODY = "body_price_band_quality_fixup_hold_body_lens_regression"
DECISION_HOLD_UI = "body_price_band_quality_fixup_hold_ui_copy_regression"
DECISION_HOLD_PRICE = "body_price_band_quality_fixup_hold_price_projection_regressed"
DECISION_HOLD_PUSH = "body_price_band_quality_fixup_hold_push_or_preview_deploy_failed"

JSON_PATH = DATA_ADMIN / "body_price_band_quality_fixup_v0.json"
JSONL_PATH = DATA_ADMIN / "p3_beta_mvp_body_price_band_quality_fixup_v0.jsonl"
MD_PATH = DATA_ADMIN / "p3_beta_mvp_body_price_band_quality_fixup_v0.md"

QUERY_ORDER = [
    "Leica M10",
    "leica m5",
    "Leica M6",
    "Leica M9",
    "Leica M11",
    "35 lux aa",
    "Noctilux 50 f1 E60",
    "Summicron 50 rigid",
    "M50/1.2",
    "Leica M50/1.2 1세대",
    "APO-Summicron-SL 90",
]

ACCESSORY_LABEL = "Accessory, not camera/lens"
VARIANT_LABEL = "Variant boundary"


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
    response = search_from_params({"q": query, "limit": "20"})
    results = response.get("results") or []
    top = results[0] if results else {}
    display = top.get("display_output") or {}
    review = response.get("display_query_review") or {}
    evidence = response.get("display_top_result_evidence") or []
    return {
        "query": query,
        "category": display.get("display_category"),
        "display_model": display.get("display_model"),
        "interpreted_target": review.get("interpreted_target"),
        "market_entry_label": "Body market summary" if display.get("display_category") == "Body" and response.get("display_price_summary_allowed") else (
            "Reference price only" if response.get("display_broader_reference_allowed") else "Price locked"
        ),
        "market_entry_value": response.get("display_price_band") if response.get("display_price_summary_allowed") else (response.get("display_broader_reference_band") or "Not enough evidence yet."),
        "price_status": review.get("price_status"),
        "why": review.get("why"),
        "display_price_summary_allowed": bool(response.get("display_price_summary_allowed")),
        "display_broader_reference_allowed": bool(response.get("display_broader_reference_allowed")),
        "display_price_scope_label": response.get("display_price_scope_label"),
        "display_price_band": response.get("display_price_band"),
        "display_broader_reference_band": response.get("display_broader_reference_band"),
        "display_unlock_requirements": list(response.get("display_unlock_requirements") or []),
        "excluded_reason_counts": dict(response.get("excluded_reason_counts") or {}),
        "display_query_review": review,
        "display_top_result_evidence": evidence,
    }


def collect_git_summary() -> dict[str, Any]:
    scoped = [
        "api/search.py",
        "scripts/run_p3_beta_mvp_body_price_band_quality_fixup.py",
        "tests/test_beta_mvp_body_price_band_quality_fixup.py",
        "data/admin/p3_beta_mvp_body_price_band_quality_fixup_v0.md",
        "data/admin/p3_beta_mvp_body_price_band_quality_fixup_v0.jsonl",
        "data/admin/body_price_band_quality_fixup_v0.json",
    ]
    return {
        "branch": run_git("branch", "--show-current"),
        "head_commit": run_git("rev-parse", "HEAD"),
        "head_subject": run_git("log", "-1", "--pretty=%s"),
        "working_diff_stat": run_git("diff", "--stat", "--", *scoped),
        "working_diff_files": [line for line in run_git("diff", "--name-only", "--", *scoped).splitlines() if line],
    }


def classify(rows: dict[str, dict[str, Any]]) -> tuple[list[str], list[str], list[str], dict[str, Any]]:
    m10 = rows["Leica M10"]
    ui_copy_regressions: list[str] = []
    price_projection_regressions: list[str] = []
    body_lens_regressions: list[str] = []

    if m10["category"] != "Body":
        body_lens_regressions.append("Leica M10")
    if m10["market_entry_value"] == "KRW 80,000 - 7,200,000":
        price_projection_regressions.append("Leica M10")
    if str(m10.get("display_price_band") or "").startswith("KRW 80,000 -"):
        price_projection_regressions.append("Leica M10")

    m10_accessories_used = []
    m10_variant_rows = []
    for item in m10["display_top_result_evidence"]:
        title = str(item.get("title") or "")
        usage = str(item.get("price_usage_label") or "")
        excluded = list(item.get("excluded_reason") or [])
        if any(token in title for token in ["홀스터", "하프케이스", "케이스", "핸드그립", "Holster", "Case", "Handgrip"]):
            if usage.startswith("Used for"):
                m10_accessories_used.append(title)
        if "Monochrom" in title or "Leitz Wetzlar" in title or "Reporter" in title or "Safari" in title:
            m10_variant_rows.append({"title": title, "usage": usage, "excluded_reason": excluded})

    if m10_accessories_used:
        price_projection_regressions.append("Leica M10")

    if any("undefined" in " | ".join([
        str(row.get("market_entry_label") or ""),
        str(row.get("market_entry_value") or ""),
        str(row.get("why") or ""),
        str((row.get("display_query_review") or {}).get("copy_summary_text") or ""),
    ]) for row in rows.values()):
        ui_copy_regressions.append("undefined")

    for query in ["leica m5", "Leica M6", "Leica M9", "Leica M11"]:
        if rows[query]["category"] != "Body":
            body_lens_regressions.append(query)
    for query in ["35 lux aa", "Noctilux 50 f1 E60", "Summicron 50 rigid", "M50/1.2", "Leica M50/1.2 1세대", "APO-Summicron-SL 90"]:
        if rows[query]["category"] != "Lens":
            body_lens_regressions.append(query)

    investigation = {
        "before_market_entry_value": "KRW 80,000 - 7,200,000",
        "after_market_entry_value": m10["market_entry_value"],
        "after_price_status": m10["price_status"],
        "after_why": m10["why"],
        "accessory_excluded_count": m10["excluded_reason_counts"].get("accessory", 0),
        "variant_boundary_excluded_count": m10["excluded_reason_counts"].get("variant_boundary", 0),
        "m10_accessories_used_for_price": m10_accessories_used,
        "m10_variant_rows": m10_variant_rows,
    }
    return (
        sorted(set(ui_copy_regressions)),
        sorted(set(price_projection_regressions)),
        sorted(set(body_lens_regressions)),
        investigation,
    )


def build_payload(push_context: dict[str, Any] | None = None) -> dict[str, Any]:
    rows = {query: build_row(query) for query in QUERY_ORDER}
    ui_copy_regressions, price_projection_regressions, body_lens_regressions, investigation = classify(rows)

    decision_status = DECISION_READY
    if ui_copy_regressions:
        decision_status = DECISION_HOLD_UI
    elif body_lens_regressions:
        decision_status = DECISION_HOLD_BODY
    elif price_projection_regressions:
        decision_status = DECISION_HOLD_M10

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
        "leica_m10_investigation": investigation,
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
    inv = payload["leica_m10_investigation"]
    lines = [
        f"# {payload['task_name']}",
        "",
        "## 1. 작업명",
        f"- `{payload['task_name']}`",
        "",
        "## 2. exact body price quality rules added",
        "- Accessory-like body titles are excluded from body price evidence even if a stale normalized row still says Body.",
        "- Adjacent body variants and special editions such as Monochrom / Reporter / Safari / Leitz Wetzlar / limited editions are excluded from generic base-body pricing as variant boundary rows unless the query explicitly asks for them.",
        "- Body base-model price now respects the same cleaned-band quality gate before it can open.",
        "",
        "## 3. Leica M10 before / after",
        f"- before = {inv['before_market_entry_value']}",
        f"- after = {inv['after_market_entry_value']}",
        f"- after price status = {inv['after_price_status']}",
        f"- after why = {inv['after_why']}",
        "",
        "## 4. M10 accessory / variant handling",
        f"- accessory_excluded_count = {inv['accessory_excluded_count']}",
        f"- variant_boundary_excluded_count = {inv['variant_boundary_excluded_count']}",
        f"- accessories_used_for_price = {inv['m10_accessories_used_for_price']}",
        f"- adjacent_variant_rows = {inv['m10_variant_rows']}",
        "",
        "## 5. regression status",
        f"- ui_copy_regressions = {payload['ui_copy_regressions']}",
        f"- price_projection_regressions = {payload['price_projection_regressions']}",
        f"- body_lens_regressions = {payload['body_lens_regressions']}",
        "",
        "## 6. query summary",
    ]
    for row in payload["rows"]:
        lines.extend(
            [
                f"### {row['query']}",
                f"- category = {row['category']}",
                f"- interpreted_target = {row['interpreted_target']}",
                f"- market_entry_value = {row['market_entry_value']}",
                f"- price_status = {row['price_status']}",
                f"- why = {row['why']}",
                f"- excluded_reason_counts = {row['excluded_reason_counts']}",
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
