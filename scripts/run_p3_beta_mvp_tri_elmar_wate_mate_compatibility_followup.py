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


TASK_NAME = "P3-BETA-MVP-TRI-ELMAR-WATE-MATE-COMPATIBILITY-FOLLOWUP"
DECISION_PUSHED = "tri_elmar_wate_mate_compatibility_followup_pushed_ready_for_owner_recheck"
DECISION_READY = "tri_elmar_wate_mate_compatibility_followup_passed_ready_for_owner_approved_push"
DECISION_HOLD_CROSS = "tri_elmar_wate_mate_compatibility_followup_hold_cross_boundary_regression"
DECISION_HOLD_GENERIC = "tri_elmar_wate_mate_compatibility_followup_hold_generic_tri_elmar_regression"
DECISION_HOLD_ACCESSORY = "tri_elmar_wate_mate_compatibility_followup_hold_accessory_finder_regression"
DECISION_HOLD_PRICE = "tri_elmar_wate_mate_compatibility_followup_hold_price_unlock_regression"
DECISION_HOLD_BODY = "tri_elmar_wate_mate_compatibility_followup_hold_body_lens_regression"

JSON_PATH = DATA_ADMIN / "tri_elmar_wate_mate_compatibility_followup_v0.json"
JSONL_PATH = DATA_ADMIN / "p3_beta_mvp_tri_elmar_wate_mate_compatibility_followup_v0.jsonl"
MD_PATH = DATA_ADMIN / "p3_beta_mvp_tri_elmar_wate_mate_compatibility_followup_v0.md"

QUERY_ORDER = [
    "wate",
    "tri-elmar 16-18-21",
    "16 18 21 tri elmar",
    "16-18-21 wate",
    "mate",
    "tri-elmar 28-35-50",
    "28 35 50 tri elmar",
    "28-35-50 mate",
    "tri-elmar",
    "35 lux fle",
    "Summilux-M 50 ASPH",
    "APO-Summicron-SL 90",
    "Leica M10",
]

BAD_COPY = {
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
        "top_result_compatibility": response.get("top_result_compatibility"),
        "boundary_conflict_detected": bool(response.get("boundary_conflict_detected")),
        "copy_summary_text": review.get("copy_summary_text"),
        "display_top_result_evidence": response.get("display_top_result_evidence") or [],
    }


def collect_git_summary() -> dict[str, Any]:
    scoped = [
        "api/search.py",
        "scripts/run_p3_beta_mvp_tri_elmar_wate_mate_compatibility_followup.py",
        "tests/test_beta_mvp_tri_elmar_wate_mate_compatibility_followup.py",
        "data/admin/p3_beta_mvp_tri_elmar_wate_mate_compatibility_followup_v0.md",
        "data/admin/p3_beta_mvp_tri_elmar_wate_mate_compatibility_followup_v0.jsonl",
        "data/admin/tri_elmar_wate_mate_compatibility_followup_v0.json",
    ]
    return {
        "branch": run_git("branch", "--show-current"),
        "head_commit": run_git("rev-parse", "HEAD"),
        "head_subject": run_git("log", "-1", "--pretty=%s"),
        "working_diff_stat": run_git("diff", "--stat", "--", *scoped),
        "working_diff_files": [line for line in run_git("diff", "--name-only", "--", *scoped).splitlines() if line],
    }


def _contains_bad_copy(row: dict[str, Any]) -> bool:
    text = json.dumps(row, ensure_ascii=False)
    return any(token in text for token in BAD_COPY)


def _find_titles(row: dict[str, Any], needle: str) -> list[dict[str, Any]]:
    lowered = needle.lower()
    return [
        item
        for item in row.get("display_top_result_evidence") or []
        if lowered in str(item.get("title") or "").lower()
    ]


def classify(rows: dict[str, dict[str, Any]]) -> tuple[list[str], list[str], list[str], list[str], list[str], dict[str, Any]]:
    cross_boundary_regressions: list[str] = []
    generic_regressions: list[str] = []
    accessory_regressions: list[str] = []
    price_unlock_regressions: list[str] = []
    body_lens_regressions: list[str] = []

    for query in ["wate", "tri-elmar 16-18-21", "16 18 21 tri elmar", "16-18-21 wate", "mate", "tri-elmar 28-35-50", "28 35 50 tri elmar", "28-35-50 mate", "35 lux fle", "Summilux-M 50 ASPH", "APO-Summicron-SL 90"]:
        if rows[query]["body_or_lens_path"] != "Lens":
            body_lens_regressions.append(query)
    if rows["Leica M10"]["body_or_lens_path"] != "Body":
        body_lens_regressions.append("Leica M10")

    for query in ["wate", "tri-elmar 16-18-21", "16 18 21 tri elmar", "16-18-21 wate"]:
        row = rows[query]
        mate_rows = _find_titles(row, "28-35-50")
        if any(item.get("compatibility_label") in {"Exact variant", "Exact base model", "Broader family"} for item in mate_rows):
            cross_boundary_regressions.append(query)
        if row["display_price_summary_allowed"]:
            price_unlock_regressions.append(query)

    for query in ["mate", "tri-elmar 28-35-50", "28 35 50 tri elmar", "28-35-50 mate"]:
        row = rows[query]
        wate_rows = _find_titles(row, "16-18-21")
        if any(item.get("compatibility_label") in {"Exact variant", "Exact base model", "Broader family"} for item in wate_rows):
            cross_boundary_regressions.append(query)
        if row["display_price_summary_allowed"]:
            price_unlock_regressions.append(query)

    for query in ["wate", "tri-elmar 16-18-21", "mate", "tri-elmar 28-35-50"]:
        row = rows[query]
        tri_rows = [item for item in row["display_top_result_evidence"] if "tri-elmar" in str(item.get("title") or "").lower()]
        compatible_rows = [item for item in tri_rows if item.get("compatibility_label") == "Exact base model"]
        if not compatible_rows:
            cross_boundary_regressions.append(query)

    generic = rows["tri-elmar"]
    if "WATE" in generic["interpreted_target"] or "MATE" in generic["interpreted_target"]:
        generic_regressions.append("tri-elmar")
    if generic["display_price_summary_allowed"]:
        price_unlock_regressions.append("tri-elmar")

    for query in ["wate", "tri-elmar 16-18-21", "mate", "tri-elmar 28-35-50", "tri-elmar"]:
        row = rows[query]
        for item in row["display_top_result_evidence"]:
            title = str(item.get("title") or "").lower()
            if "finder" in title or "frankenfinder" in title:
                if item.get("used_for_price"):
                    accessory_regressions.append(query)
                if item.get("compatibility_label") == "Exact variant":
                    accessory_regressions.append(query)

    if str(rows["Leica M10"].get("display_price_band") or "").startswith("KRW 80,000 -"):
        body_lens_regressions.append("Leica M10 noisy band")

    summary = {
        "wate_before": {
            "issue": "Compatible 16-18-21 Tri-Elmar rows could show up as not compatible with this query.",
        },
        "wate_after": {
            "interpreted_target": rows["wate"]["interpreted_target"],
            "price_status": rows["wate"]["price_status"],
            "top_rows": rows["wate"]["display_top_result_evidence"][:5],
        },
        "mate_before": {
            "issue": "Compatible 28-35-50 Tri-Elmar rows could show up as boundary conflict instead of same-base evidence.",
        },
        "mate_after": {
            "interpreted_target": rows["mate"]["interpreted_target"],
            "price_status": rows["mate"]["price_status"],
            "top_rows": rows["mate"]["display_top_result_evidence"][:5],
        },
        "tri_elmar_16_18_21_after": rows["tri-elmar 16-18-21"]["display_top_result_evidence"][:5],
        "tri_elmar_28_35_50_after": rows["tri-elmar 28-35-50"]["display_top_result_evidence"][:5],
        "bad_copy_regressions": [query for query, row in rows.items() if _contains_bad_copy(row)],
    }
    return (
        sorted(set(cross_boundary_regressions)),
        sorted(set(generic_regressions)),
        sorted(set(accessory_regressions)),
        sorted(set(price_unlock_regressions)),
        sorted(set(body_lens_regressions)),
        summary,
    )


def build_payload(push_context: dict[str, Any] | None = None) -> dict[str, Any]:
    rows = {query: build_row(query) for query in QUERY_ORDER}
    (
        cross_boundary_regressions,
        generic_regressions,
        accessory_regressions,
        price_unlock_regressions,
        body_lens_regressions,
        summary,
    ) = classify(rows)

    decision_status = DECISION_READY
    if body_lens_regressions:
        decision_status = DECISION_HOLD_BODY
    elif price_unlock_regressions:
        decision_status = DECISION_HOLD_PRICE
    elif accessory_regressions:
        decision_status = DECISION_HOLD_ACCESSORY
    elif generic_regressions:
        decision_status = DECISION_HOLD_GENERIC
    elif cross_boundary_regressions:
        decision_status = DECISION_HOLD_CROSS

    push_context = push_context or build_commit_push_context_from_env()
    if (
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
        "tri_elmar_summary": summary,
        "cross_boundary_regressions": cross_boundary_regressions,
        "generic_tri_elmar_regressions": generic_regressions,
        "accessory_finder_regressions": accessory_regressions,
        "price_unlock_regressions": price_unlock_regressions,
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
    summary = payload["tri_elmar_summary"]
    lines = [
        f"# {payload['task_name']}",
        "",
        "## 1. 작업명",
        f"- `{payload['task_name']}`",
        "",
        "## 2. exact compatibility logic changed",
        "- Tri-Elmar WATE / MATE rows can now inherit compatible same-base usage labels even when they stay visible-only for pricing.",
        "- WATE queries accept 16-18-21 Tri-Elmar-M rows as compatible same-base/reference evidence.",
        "- MATE queries accept 28-35-50 Tri-Elmar-M rows as compatible same-base/reference evidence.",
        "- WATE vs MATE cross-boundary separation remains intact.",
        "",
        "## 3. before / after for `wate`",
        f"- before issue = {summary['wate_before']['issue']}",
        f"- after interpreted_target = {summary['wate_after']['interpreted_target']}",
        f"- after price_status = {summary['wate_after']['price_status']}",
        "",
        "## 4. before / after for `mate`",
        f"- before issue = {summary['mate_before']['issue']}",
        f"- after interpreted_target = {summary['mate_after']['interpreted_target']}",
        f"- after price_status = {summary['mate_after']['price_status']}",
        "",
        "## 5. before / after for `tri-elmar 16-18-21`",
    ]
    for item in summary["tri_elmar_16_18_21_after"][:3]:
        lines.append(f"- {item['title']} -> {item['compatibility_label']} / {item['price_usage_label']}")
    lines.extend(
        [
            "",
            "## 6. before / after for `tri-elmar 28-35-50`",
        ]
    )
    for item in summary["tri_elmar_28_35_50_after"][:3]:
        lines.append(f"- {item['title']} -> {item['compatibility_label']} / {item['price_usage_label']}")
    lines.extend(
        [
            "",
            "## 7. cross-boundary guard status",
            f"- cross_boundary_regressions = {payload['cross_boundary_regressions'] or 'none'}",
            "",
            "## 8. generic `tri-elmar` ambiguity guard status",
            f"- generic_tri_elmar_regressions = {payload['generic_tri_elmar_regressions'] or 'none'}",
            "",
            "## 9. accessory / finder guard status",
            f"- accessory_finder_regressions = {payload['accessory_finder_regressions'] or 'none'}",
            "",
            "## 10. price / routing / UI guard",
            f"- price_unlock_regressions = {payload['price_unlock_regressions'] or 'none'}",
            f"- body_lens_regressions = {payload['body_lens_regressions'] or 'none'}",
            f"- technical_copy_regressions = {summary['bad_copy_regressions'] or 'none'}",
            "",
            "## 11. decision_status",
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
