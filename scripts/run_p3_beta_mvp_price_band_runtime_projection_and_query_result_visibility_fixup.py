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


TASK_NAME = "P3-BETA-MVP-PRICE-BAND-RUNTIME-PROJECTION-AND-QUERY-RESULT-VISIBILITY-FIXUP"
DECISION_PUSHED = "price_band_runtime_projection_query_result_visibility_fixup_pushed_ready_for_owner_recheck"
DECISION_READY = "price_band_runtime_projection_query_result_visibility_fixup_passed_ready_for_owner_approved_push"
DECISION_HOLD_BROADER = "price_band_runtime_projection_query_result_visibility_fixup_hold_disallowed_broader_reference_visible"
DECISION_HOLD_MISMATCH = "price_band_runtime_projection_query_result_visibility_fixup_hold_band_projection_mismatch"
DECISION_HOLD_PANEL = "price_band_runtime_projection_query_result_visibility_fixup_hold_query_result_panel_missing"
DECISION_HOLD_DEV = "price_band_runtime_projection_query_result_visibility_fixup_hold_dev_token_visible"
DECISION_HOLD_EXACT = "price_band_runtime_projection_query_result_visibility_fixup_hold_exact_variant_price_regressed"
DECISION_HOLD_BODY = "price_band_runtime_projection_query_result_visibility_fixup_hold_body_lens_regression"
DECISION_HOLD_PUSH = "price_band_runtime_projection_query_result_visibility_fixup_hold_push_or_preview_deploy_failed"

JSON_PATH = DATA_ADMIN / "price_band_runtime_projection_and_query_result_visibility_fixup_v0.json"
JSONL_PATH = DATA_ADMIN / "p3_beta_mvp_price_band_runtime_projection_and_query_result_visibility_fixup_v0.jsonl"
MD_PATH = DATA_ADMIN / "p3_beta_mvp_price_band_runtime_projection_and_query_result_visibility_fixup_v0.md"

SCOPED_FILES = [
    "api/search.py",
    "app/templates/index.html",
    "index.html",
    "scripts/run_p3_beta_mvp_price_band_runtime_projection_and_query_result_visibility_fixup.py",
    "tests/test_beta_mvp_price_band_runtime_projection_and_query_result_visibility_fixup.py",
    "data/admin/p3_beta_mvp_price_band_runtime_projection_and_query_result_visibility_fixup_v0.md",
    "data/admin/p3_beta_mvp_price_band_runtime_projection_and_query_result_visibility_fixup_v0.jsonl",
    "data/admin/price_band_runtime_projection_and_query_result_visibility_fixup_v0.json",
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
        "market_entry_allowed": bool(response.get("market_entry_allowed")),
        "price_summary_allowed": bool(response.get("price_summary_allowed")),
        "broader_reference_allowed": bool(response.get("broader_reference_allowed")),
        "broader_reference_label": response.get("broader_reference_label"),
        "broader_reference_band": response.get("broader_reference_band"),
        "broader_reference_locked_reason": response.get("broader_reference_locked_reason"),
        "broader_reference_quality_state": response.get("broader_reference_quality_state"),
        "broader_reference_quality_reason": list(response.get("broader_reference_quality_reason") or []),
        "broader_reference_source_scope": response.get("broader_reference_source_scope"),
        "price_summary_band": response.get("price_summary_band"),
        "price_scope": response.get("price_scope"),
        "price_scope_label": response.get("price_scope_label"),
        "display_price_summary_allowed": bool(response.get("display_price_summary_allowed")),
        "display_price_scope_label": response.get("display_price_scope_label"),
        "display_price_band": response.get("display_price_band"),
        "display_price_band_source": response.get("display_price_band_source"),
        "display_broader_reference_allowed": bool(response.get("display_broader_reference_allowed")),
        "display_broader_reference_label": response.get("display_broader_reference_label"),
        "display_broader_reference_band": response.get("display_broader_reference_band"),
        "display_broader_reference_locked_reason": response.get("display_broader_reference_locked_reason"),
        "display_price_band_quality_state": response.get("display_price_band_quality_state"),
        "display_unlock_requirements": list(response.get("display_unlock_requirements") or []),
        "display_match_state_message": response.get("display_match_state_message"),
        "display_query_review": response.get("display_query_review"),
        "display_top_result_evidence": response.get("display_top_result_evidence") or [],
        "display_top_result_evidence_count": len(response.get("display_top_result_evidence") or []),
        "display_evidence_pool_summary": response.get("display_evidence_pool_summary"),
        "top_display_category": top_display.get("display_category"),
        "top_display_model": top_display.get("display_model"),
        "top_display_family": top_display.get("display_family"),
        "top_result_title": top.get("title"),
        "top_result_source": top.get("source"),
        "top_result_price": top.get("price"),
        "top_result_evidence_preview": (response.get("display_top_result_evidence") or [])[:3],
        "policy_preview": {
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


def dev_token_visible(row: dict[str, Any]) -> bool:
    values = [
        row.get("display_price_scope_label") or "",
        row.get("display_price_band") or "",
        row.get("display_broader_reference_locked_reason") or "",
        row.get("display_match_state_message") or "",
        (row.get("display_query_review") or {}).get("match_state") or "",
        (row.get("display_query_review") or {}).get("price_status") or "",
    ]
    values.extend(" ".join(item.get("excluded_reason") or []) for item in row.get("display_top_result_evidence") or [])
    text = " | ".join(values)
    return any(token in text for token in DEV_TOKENS)


def classify_failures(rows: dict[str, dict[str, Any]]) -> tuple[list[str], list[str], list[str], list[str], list[str]]:
    disallowed_broader_reference_visible: list[str] = []
    band_projection_mismatch: list[str] = []
    query_result_panel_missing: list[str] = []
    dev_token_rows: list[str] = []
    exact_variant_regressions: list[str] = []
    body_lens_regressions: list[str] = []

    for query, row in rows.items():
        if not row["display_query_review"]:
            query_result_panel_missing.append(query)
        elif row["top_result_title"] and row["display_top_result_evidence_count"] <= 0:
            query_result_panel_missing.append(query)
        if dev_token_visible(row):
            dev_token_rows.append(query)
        if not row["display_broader_reference_allowed"] and row["display_broader_reference_band"]:
            disallowed_broader_reference_visible.append(query)
        if row["display_price_summary_allowed"] and row["display_price_band"] != row["price_summary_band"]:
            band_projection_mismatch.append(query)
        if row["display_broader_reference_allowed"] and row["display_broader_reference_band"] != row["broader_reference_band"]:
            band_projection_mismatch.append(query)

    for query in ["Summicron 50 rigid", "Summicron 35 8-element"]:
        row = rows[query]
        if not row["display_price_summary_allowed"] or row["display_price_scope_label"] != "Exact variant price":
            exact_variant_regressions.append(query)

    for query in ["M50/1.2", "Leica M50/1.2 1세대"]:
        row = rows[query]
        if row["top_display_category"] == "Body" or row["top_display_model"] == "M5":
            body_lens_regressions.append(query)

    for query in ["Leica M9", "Leica M10", "Leica M11"]:
        row = rows[query]
        if row["top_display_category"] != "Body":
            body_lens_regressions.append(query)

    return (
        sorted(set(disallowed_broader_reference_visible)),
        sorted(set(band_projection_mismatch)),
        sorted(set(query_result_panel_missing)),
        sorted(set(dev_token_rows)),
        sorted(set(exact_variant_regressions)),
        sorted(set(body_lens_regressions)),
    )


def build_payload(push_context: dict[str, Any] | None = None) -> dict[str, Any]:
    rows = {query: response_row(query) for query in QUERY_ORDER}
    (
        disallowed_broader_reference_visible,
        band_projection_mismatch,
        query_result_panel_missing,
        dev_token_rows,
        exact_variant_regressions,
        body_lens_regressions,
    ) = classify_failures(rows)

    decision_status = DECISION_READY
    if disallowed_broader_reference_visible:
        decision_status = DECISION_HOLD_BROADER
    elif band_projection_mismatch:
        decision_status = DECISION_HOLD_MISMATCH
    elif query_result_panel_missing:
        decision_status = DECISION_HOLD_PANEL
    elif dev_token_rows:
        decision_status = DECISION_HOLD_DEV
    elif exact_variant_regressions:
        decision_status = DECISION_HOLD_EXACT
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

    guards = {
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
    }

    return {
        "task_name": TASK_NAME,
        "decision_status": decision_status,
        "owner_recheck_hold_reason": "Runtime UI projection did not consistently use the same cleaned price band fields as the API/report, and owner review lacked a one-screen query/result evidence view.",
        "unified_display_field_design": {
            "display_price_summary_allowed": "Single UI truth for exact/base price visibility.",
            "display_price_band": "Canonical cleaned band shown in the price card.",
            "display_broader_reference_band": "Canonical cleaned reference band shown only when allowed.",
            "display_top_result_evidence": "Top visible result evidence rows for owner review.",
            "display_query_review": "User-facing interpretation summary for the query.",
        },
        "query_results": [rows[q] for q in QUERY_ORDER],
        "lux_aa_result": rows["35 lux aa"],
        "noctilux_e60_result": rows["Noctilux 50 f1 E60"],
        "summicron_rigid_result": rows["Summicron 50 rigid"],
        "test_verdict": {
            "disallowed_broader_reference_visible": disallowed_broader_reference_visible,
            "band_projection_mismatch": band_projection_mismatch,
            "query_result_panel_missing": query_result_panel_missing,
            "dev_token_visible": dev_token_rows,
            "exact_variant_price_regressed": exact_variant_regressions,
            "body_lens_regression": body_lens_regressions,
        },
        "git_diff_summary": collect_git_summary(),
        "commit_push_context": push_context,
        "preview_deployment_url": push_context.get("preview_deployment_url"),
        "preview_deployment_id": push_context.get("preview_deployment_id"),
        "preview_deployment_state": push_context.get("preview_deployment_state"),
        "preview_branch": push_context.get("preview_branch"),
        "preview_commit": push_context.get("preview_commit"),
        "guards": guards,
        "production_alias_connect_allowed": False,
        "next_backlog_candidates": [
            "P3-BETA-MVP-PRICE-BAND-RUNTIME-PROJECTION-AND-QUERY-RESULT-VISIBILITY-OWNER-RECHECK",
            "P3-BETA-MVP-LENS-VARIANT-TOKEN-PARSER-COVERAGE-FIXUP",
            "P3-BETA-MVP-LENS-BOUNDARY-CONFLICT-RESOLUTION-FIXUP",
            "P3-BETA-MVP-LOCKED-ENTRY-AND-PRICE-UNLOCK-AUDIT",
        ],
    }


def write_outputs(payload: dict[str, Any]) -> None:
    DATA_ADMIN.mkdir(parents=True, exist_ok=True)
    JSON_PATH.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    JSONL_PATH.write_text(json.dumps(payload, ensure_ascii=False) + "\n", encoding="utf-8")

    lux_aa = payload["lux_aa_result"]
    e60 = payload["noctilux_e60_result"]
    rigid = payload["summicron_rigid_result"]
    md = f"""# {TASK_NAME}

- decision_status: `{payload['decision_status']}`
- preview_deployment_url: `{payload.get('preview_deployment_url')}`

## Owner Recheck Hold
- runtime price band projection and UI display were not reliably aligned before this fix.
- query/result evidence needed to be visible in one place for owner review.

## 35 lux aa
- `display_price_summary_allowed`: `{lux_aa['display_price_summary_allowed']}`
- `display_broader_reference_allowed`: `{lux_aa['display_broader_reference_allowed']}`
- `display_broader_reference_label`: `{lux_aa['display_broader_reference_label']}`
- `display_broader_reference_band`: `{lux_aa['display_broader_reference_band']}`
- `broader_reference_quality_state`: `{lux_aa['broader_reference_quality_state']}`

## Noctilux 50 f1 E60
- `display_price_band`: `{e60['display_price_band']}`
- `display_broader_reference_band`: `{e60['display_broader_reference_band']}`
- `display_match_state_message`: `{e60['display_match_state_message']}`

## Summicron 50 rigid
- `display_price_band`: `{rigid['display_price_band']}`
- `price_summary_band`: `{rigid['price_summary_band']}`
- `display_top_result_evidence_count`: `{rigid['display_top_result_evidence_count']}`

## Verdict
- disallowed broader reference visible: `{payload['test_verdict']['disallowed_broader_reference_visible']}`
- band projection mismatch: `{payload['test_verdict']['band_projection_mismatch']}`
- query result panel missing: `{payload['test_verdict']['query_result_panel_missing']}`
- dev token visible: `{payload['test_verdict']['dev_token_visible']}`
"""
    MD_PATH.write_text(md + "\n", encoding="utf-8")


def main() -> None:
    payload = build_payload()
    write_outputs(payload)
    print(json.dumps(payload, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
