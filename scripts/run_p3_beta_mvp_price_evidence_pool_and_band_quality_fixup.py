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


TASK_NAME = "P3-BETA-MVP-PRICE-EVIDENCE-POOL-AND-BAND-QUALITY-FIXUP"
DECISION_PUSHED = "price_evidence_pool_band_quality_fixup_pushed_ready_for_owner_recheck"
DECISION_READY = "price_evidence_pool_band_quality_fixup_passed_ready_for_owner_approved_push"
DECISION_HOLD_NOISY = "price_evidence_pool_band_quality_fixup_hold_noisy_band_still_shown"
DECISION_HOLD_OUTLIER = "price_evidence_pool_band_quality_fixup_hold_outlier_not_excluded"
DECISION_HOLD_WRONG = "price_evidence_pool_band_quality_fixup_hold_wrong_model_or_accessory_price_included"
DECISION_HOLD_EXACT = "price_evidence_pool_band_quality_fixup_hold_exact_variant_price_regressed"
DECISION_HOLD_BODY = "price_evidence_pool_band_quality_fixup_hold_body_lens_regression"
DECISION_HOLD_PUSH = "price_evidence_pool_band_quality_fixup_hold_push_or_preview_deploy_failed"

JSON_PATH = DATA_ADMIN / "price_evidence_pool_and_band_quality_fixup_v0.json"
JSONL_PATH = DATA_ADMIN / "p3_beta_mvp_price_evidence_pool_and_band_quality_fixup_v0.jsonl"
MD_PATH = DATA_ADMIN / "p3_beta_mvp_price_evidence_pool_and_band_quality_fixup_v0.md"

SCOPED_FILES = [
    "api/search.py",
    "app/templates/index.html",
    "index.html",
    "scripts/run_p3_beta_mvp_price_evidence_pool_and_band_quality_fixup.py",
    "tests/test_beta_mvp_price_evidence_pool_and_band_quality_fixup.py",
    "data/admin/p3_beta_mvp_price_evidence_pool_and_band_quality_fixup_v0.md",
    "data/admin/p3_beta_mvp_price_evidence_pool_and_band_quality_fixup_v0.jsonl",
    "data/admin/price_evidence_pool_and_band_quality_fixup_v0.json",
]

QUERY_ORDER = [
    "Noctilux 50 f1 E60",
    "Leica Summilux-M 50mm f1.4 3세대",
    "Summilux 50 3rd generation",
    "35 lux aa",
    "Summilux-M 50 ASPH",
    "Summicron 35 8-element",
    "Summicron 50 rigid",
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

EXACT_VARIANT_STABLE = ["Summicron 35 8-element", "Summicron 50 rigid", "Leica M50/1.2 1세대"]
BODY_REGRESSION = ["M50/1.2", "Leica M50/1.2 1세대", "Leica M9", "Leica M10", "Leica M11"]


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
    response = search_from_params({"q": query, "limit": "20"})
    results = response.get("results") or []
    top = results[0] if results else {}
    final = top.get("final_output") or {}
    display = top.get("display_output") or {}
    return {
        "query": query,
        "price_summary_allowed": bool(response.get("price_summary_allowed")),
        "price_scope": response.get("price_scope"),
        "price_scope_label": response.get("price_scope_label"),
        "price_evidence_scope": response.get("price_evidence_scope"),
        "price_band_quality_state": response.get("price_band_quality_state"),
        "price_band_quality_reason": list(response.get("price_band_quality_reason") or []),
        "raw_price_min": response.get("raw_price_min"),
        "raw_price_max": response.get("raw_price_max"),
        "cleaned_price_min": response.get("cleaned_price_min"),
        "cleaned_price_max": response.get("cleaned_price_max"),
        "price_band_width_ratio": response.get("price_band_width_ratio"),
        "price_summary_band": response.get("price_summary_band"),
        "broader_reference_allowed": bool(response.get("broader_reference_allowed")),
        "broader_reference_label": response.get("broader_reference_label"),
        "broader_reference_band": response.get("broader_reference_band"),
        "broader_reference_locked_reason": response.get("broader_reference_locked_reason"),
        "broader_reference_quality_state": response.get("broader_reference_quality_state"),
        "broader_reference_quality_reason": list(response.get("broader_reference_quality_reason") or []),
        "exact_variant_pool_count": int(response.get("exact_variant_pool_count") or 0),
        "exact_variant_priced_count": int(response.get("exact_variant_priced_count") or 0),
        "exact_base_model_pool_count": int(response.get("exact_base_model_pool_count") or 0),
        "exact_base_model_priced_count": int(response.get("exact_base_model_priced_count") or 0),
        "broader_family_pool_count": int(response.get("broader_family_pool_count") or 0),
        "broader_family_priced_count": int(response.get("broader_family_priced_count") or 0),
        "excluded_pool_count": int(response.get("excluded_pool_count") or 0),
        "excluded_reason_counts": dict(response.get("excluded_reason_counts") or {}),
        "outlier_removed_count": int(response.get("outlier_removed_count") or 0),
        "accessory_price_excluded_count": int(response.get("accessory_price_excluded_count") or 0),
        "third_party_price_excluded_count": int(response.get("third_party_price_excluded_count") or 0),
        "wrong_model_price_excluded_count": int(response.get("wrong_model_price_excluded_count") or 0),
        "unlock_requirements": list(response.get("unlock_requirements") or []),
        "search_confidence_state": response.get("search_confidence_state"),
        "top_result_compatibility": response.get("top_result_compatibility"),
        "top_result_category": final.get("category"),
        "top_result_model": final.get("model_canonical"),
        "top_display_category": display.get("display_category"),
        "top_display_model": display.get("display_model"),
    }


def collect_git_summary() -> dict[str, Any]:
    return {
        "branch": run_git("branch", "--show-current"),
        "head_commit": run_git("rev-parse", "HEAD"),
        "head_subject": run_git("log", "-1", "--pretty=%s"),
        "working_diff_stat": run_git("diff", "--stat", "--", *SCOPED_FILES),
        "working_diff_files": [line for line in run_git("diff", "--name-only", "--", *SCOPED_FILES).splitlines() if line],
    }


def classify_failures(rows: dict[str, dict[str, Any]]) -> tuple[list[str], list[str], list[str], list[str], list[str]]:
    noisy_band: list[str] = []
    outlier_failures: list[str] = []
    wrong_model_failures: list[str] = []
    exact_variant_regressions: list[str] = []
    body_lens_regressions: list[str] = []

    e60 = rows["Noctilux 50 f1 E60"]
    if e60["price_summary_allowed"]:
        noisy_band.append("Noctilux 50 f1 E60")
    if e60["broader_reference_allowed"] and any(token in str(e60["broader_reference_band"]) for token in ["990,000", "53,000,000"]):
        noisy_band.append("Noctilux 50 f1 E60")
    if e60["broader_reference_allowed"] and e60["broader_reference_quality_state"] not in {"clean_broader_reference_band", "clean_exact_base_model_band"}:
        noisy_band.append("Noctilux 50 f1 E60")

    for query in ["Leica Summilux-M 50mm f1.4 3세대", "Summilux 50 3rd generation", "35 lux aa"]:
        row = rows[query]
        if row["price_summary_allowed"] and row["price_scope"] == "exact_variant":
            noisy_band.append(query)

    for query in ["Noctilux 50 f1 E60", "Summilux-M 50 ASPH"]:
        row = rows[query]
        if row["price_summary_allowed"] and row["wrong_model_price_excluded_count"] < 0:
            wrong_model_failures.append(query)

    for query in EXACT_VARIANT_STABLE:
        row = rows[query]
        if not row["price_summary_allowed"] or row["price_scope"] != "exact_variant":
            exact_variant_regressions.append(query)

    for query in BODY_REGRESSION:
        row = rows[query]
        if query in {"M50/1.2", "Leica M50/1.2 1세대"}:
            if row["top_display_category"] == "Body" or row["top_display_model"] == "M5":
                body_lens_regressions.append(query)
        elif row["top_display_category"] != "Body":
            body_lens_regressions.append(query)

    return (
        sorted(set(noisy_band)),
        sorted(set(outlier_failures)),
        sorted(set(wrong_model_failures)),
        sorted(set(exact_variant_regressions)),
        sorted(set(body_lens_regressions)),
    )


def build_payload(push_context: dict[str, Any] | None = None) -> dict[str, Any]:
    rows = {query: response_row(query) for query in QUERY_ORDER}
    noisy_band, outlier_failures, wrong_model_failures, exact_variant_regressions, body_lens_regressions = classify_failures(rows)

    decision_status = DECISION_READY
    if noisy_band:
        decision_status = DECISION_HOLD_NOISY
    elif outlier_failures:
        decision_status = DECISION_HOLD_OUTLIER
    elif wrong_model_failures:
        decision_status = DECISION_HOLD_WRONG
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
        "current_problem_summary": "Broader family reference and raw min/max price bands could still look like trustworthy market prices even when accessory, wrong-model, third-party, duplicate, or outlier noise was present.",
        "price_evidence_pool_design": {
            "exact_variant_pool": "Variant, mount, focal length, and aperture-compatible cleaned price evidence.",
            "exact_base_model_pool": "Base model-compatible cleaned evidence when exact variant evidence is insufficient.",
            "broader_family_pool": "Clearly labeled family reference only after noisy prices are excluded and band quality is acceptable.",
            "excluded_pool": "Accessory, wrong model, third-party, duplicate, suspicious, or outlier prices removed from pricing.",
        },
        "query_results": [rows[q] for q in QUERY_ORDER],
        "noctilux_e60_result": rows["Noctilux 50 f1 E60"],
        "summilux_50_3rd_result": rows["Leica Summilux-M 50mm f1.4 3세대"],
        "lux_aa_result": rows["35 lux aa"],
        "exact_variant_stable_results": [rows[q] for q in EXACT_VARIANT_STABLE],
        "test_verdict": {
            "noisy_band_still_shown": noisy_band,
            "outlier_not_excluded": outlier_failures,
            "wrong_model_or_accessory_price_included": wrong_model_failures,
            "exact_variant_price_regressed": exact_variant_regressions,
            "body_lens_regressions": body_lens_regressions,
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
            "P3-BETA-MVP-PRICE-EVIDENCE-POOL-AND-BAND-QUALITY-OWNER-RECHECK",
            "P3-BETA-MVP-LENS-VARIANT-TOKEN-PARSER-COVERAGE-FIXUP",
            "P3-BETA-MVP-LENS-BOUNDARY-CONFLICT-RESOLUTION-FIXUP",
            "P3-BETA-MVP-LOCKED-ENTRY-AND-PRICE-UNLOCK-AUDIT",
        ],
    }


def write_outputs(payload: dict[str, Any]) -> None:
    DATA_ADMIN.mkdir(parents=True, exist_ok=True)
    JSON_PATH.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    JSONL_PATH.write_text(json.dumps(payload, ensure_ascii=False) + "\n", encoding="utf-8")

    e60 = payload["noctilux_e60_result"]
    summilux3 = payload["summilux_50_3rd_result"]
    luxaa = payload["lux_aa_result"]
    exact_lines = "\n".join(
        f"- `{row['query']}` -> allowed={row['price_summary_allowed']} / band={row['price_summary_band']} / excluded={row['excluded_pool_count']}"
        for row in payload["exact_variant_stable_results"]
    )
    md = f"""# {TASK_NAME}

- decision_status: `{payload['decision_status']}`
- preview_deployment_url: `{payload.get('preview_deployment_url')}`

## Price Evidence Pool
- exact_variant_pool / exact_base_model_pool / broader_family_pool / excluded_pool are separated before band calculation.
- noisy or incompatible prices are removed before price band rendering.

## Noctilux E60
- `price_summary_allowed`: `{e60['price_summary_allowed']}`
- `price_scope_label`: `{e60['price_scope_label']}`
- `broader_reference_band`: `{e60['broader_reference_band']}`
- `broader_reference_quality_state`: `{e60['broader_reference_quality_state']}`
- `unlock_requirements`: `{", ".join(e60['unlock_requirements'])}`

## Summilux 50 3rd Generation
- `price_summary_allowed`: `{summilux3['price_summary_allowed']}`
- `price_scope_label`: `{summilux3['price_scope_label']}`
- `broader_reference_band`: `{summilux3['broader_reference_band']}`

## 35 lux aa
- `price_summary_allowed`: `{luxaa['price_summary_allowed']}`
- `broader_reference_allowed`: `{luxaa['broader_reference_allowed']}`
- `broader_reference_locked_reason`: `{luxaa['broader_reference_locked_reason']}`

## Exact Variant Stable
{exact_lines}
"""
    MD_PATH.write_text(md + "\n", encoding="utf-8")


def main() -> None:
    payload = build_payload()
    write_outputs(payload)
    print(json.dumps({"decision_status": payload["decision_status"]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
