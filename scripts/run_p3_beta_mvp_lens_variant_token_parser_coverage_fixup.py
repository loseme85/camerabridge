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
from query_parser import parse_query


TASK_NAME = "P3-BETA-MVP-LENS-VARIANT-TOKEN-PARSER-COVERAGE-FIXUP"
DECISION_PUSHED = "lens_variant_token_parser_coverage_fixup_pushed_ready_for_owner_recheck"
DECISION_READY = "lens_variant_token_parser_coverage_fixup_passed_ready_for_owner_approved_push"
DECISION_HOLD_UNSAFE = "lens_variant_token_parser_coverage_fixup_hold_unsafe_alias_hardpin_regression"
DECISION_HOLD_PRE_ASPH = "lens_variant_token_parser_coverage_fixup_hold_pre_asph_regression"
DECISION_HOLD_TRI_ELMAR = "lens_variant_token_parser_coverage_fixup_hold_tri_elmar_alias_too_broad"
DECISION_HOLD_BODY = "lens_variant_token_parser_coverage_fixup_hold_body_lens_regression"
DECISION_HOLD_PRICE = "lens_variant_token_parser_coverage_fixup_hold_price_projection_regressed"
DECISION_HOLD_PUSH = "lens_variant_token_parser_coverage_fixup_hold_push_or_preview_deploy_failed"

JSON_PATH = DATA_ADMIN / "lens_variant_token_parser_coverage_fixup_v0.json"
JSONL_PATH = DATA_ADMIN / "p3_beta_mvp_lens_variant_token_parser_coverage_fixup_v0.jsonl"
MD_PATH = DATA_ADMIN / "p3_beta_mvp_lens_variant_token_parser_coverage_fixup_v0.md"

QUERY_ORDER = [
    "pre asph summilux 35",
    "summilux 35 pre-asph",
    "35 cron 8 element",
    "summicron 35 8 element",
    "summilux-m 50 asph",
    "fle summilux 35",
    "35 lux fle",
    "fle",
    "wate",
    "mate",
    "tri-elmar 16-18-21",
    "tri-elmar 28-35-50",
    "16 18 21 tri elmar",
    "28 35 50 tri elmar",
    "16-18-21 wate",
    "28-35-50 mate",
    "lux",
    "cron",
    "nocti",
    "E60",
    "1세대",
    "BP",
    "35 lux aa",
    "noctilux 50 f1 e60",
    "50 cron rigid",
    "50 cron dr",
    "summicron 35 8매",
    "50 nocti 1세대",
    "M50/1.2 1세대",
    "Summilux-M 50 ASPH",
    "APO-Summicron-SL 90",
    "Leica M10",
]

TARGET_BEFORE = {
    "pre asph summilux 35": "Interpreted as Leica Summilux 35 ASPH candidate because split `pre asph` dropped the negative prefix.",
    "35 cron 8 element": "Interpreted as Leica Summicron 35 candidate because spaced `8 element` was not recognized.",
    "summicron 35 8 element": "Interpreted as Leica Summicron 35 candidate because spaced `8 element` was not recognized.",
    "summilux-m 50 asph": "Missed `summilux-m` as an unknown token and did not preserve the hyphenated family form cleanly.",
    "fle summilux 35": "Missed `fle` and fell back to Leica Summilux 35 candidate without the FLE variant.",
    "35 lux fle": "Missed `fle` and fell back to Leica Summilux 35 candidate without the FLE variant.",
    "wate": "Stayed unknown and did not resolve to Leica Tri-Elmar 16-18-21 / WATE.",
    "mate": "Stayed unknown and did not resolve to Leica Tri-Elmar 28-35-50 / MATE.",
    "tri-elmar 16-18-21": "Recognized Tri-Elmar but missed the 16-18-21 range and WATE shorthand.",
    "tri-elmar 28-35-50": "Recognized Tri-Elmar but missed the 28-35-50 range and MATE shorthand.",
}

UNSAFE_BROAD_ALIAS_QUERIES = ["lux", "cron", "nocti", "E60", "1세대", "BP"]

SAFE_TOKEN_CHANGES = [
    "Normalize split `pre asph` into `pre-ASPH` before generic ASPH parsing.",
    "Normalize spaced `8 element` / `8 elements` into `8-element`.",
    "Normalize spaced `tri elmar` into `tri-elmar` for shorthand recovery.",
    "Add search-layer hyphenated Leica family aliases without broad `-m/-r/-sl` hard-pins.",
    "Recognize `FLE` only inside strong Summilux 35 context.",
    "Recognize `WATE` and `MATE` as narrow Tri-Elmar shorthand.",
    "Recover Tri-Elmar focal ranges `16-18-21` and `28-35-50` only with Tri-Elmar/WATE/MATE context.",
]


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


def _recognized_tokens(intent: dict[str, Any]) -> list[str]:
    out: list[str] = []
    if intent.get("model_family"):
        out.append(f"family:{intent['model_family']}")
    if intent.get("focal_length"):
        out.append(f"focal:{intent['focal_length']}")
    if intent.get("mount"):
        out.append(f"mount:{intent['mount']}")
    for variant in intent.get("variant") or []:
        out.append(f"variant:{variant}")
    if intent.get("generation"):
        out.append(f"generation:{intent['generation']}")
    if intent.get("filter_size"):
        out.append(f"filter:{intent['filter_size']}")
    return out


def _unknown_tokens(intent: dict[str, Any]) -> list[str]:
    return [str(token.get("raw") or "") for token in intent.get("tokens") or [] if token.get("type") == "unknown"]


def build_row(query: str) -> dict[str, Any]:
    intent = parse_query(query)
    response = search_from_params({"q": query, "limit": "10"})
    results = response.get("results") or []
    top = results[0] if results else {}
    display = top.get("display_output") or {}
    review = response.get("display_query_review") or {}
    return {
        "query": query,
        "before_snapshot": TARGET_BEFORE.get(query),
        "interpreted_target": review.get("interpreted_target"),
        "category": display.get("display_category"),
        "body_or_lens_path": "Body" if str(review.get("interpreted_target") or "").lower().endswith(" body") else display.get("display_category"),
        "model_family": intent.get("model_family"),
        "focal_length": intent.get("focal_length"),
        "mount": intent.get("mount"),
        "variant": intent.get("variant") or [],
        "generation": intent.get("generation"),
        "filter_size": intent.get("filter_size"),
        "recognized_tokens": _recognized_tokens(intent),
        "unknown_tokens": _unknown_tokens(intent),
        "price_status": review.get("price_status"),
        "display_price_scope_label": response.get("display_price_scope_label"),
        "display_price_summary_allowed": bool(response.get("display_price_summary_allowed")),
        "top_result_compatibility": response.get("top_result_compatibility"),
        "third_party_top_domination_detected": bool(response.get("third_party_top_domination_detected")),
        "boundary_conflict_detected": bool(response.get("boundary_conflict_detected")),
        "copy_summary_visible": "Copy summary" in (ROOT / "app" / "templates" / "index.html").read_text(encoding="utf-8"),
        "top_result_title": top.get("title"),
    }


def collect_git_summary() -> dict[str, Any]:
    scoped = [
        "api/search.py",
        "query_parser.py",
        "search_aliases.py",
        "scripts/run_p3_beta_mvp_lens_variant_token_parser_coverage_fixup.py",
        "tests/test_beta_mvp_lens_variant_token_parser_coverage_fixup.py",
        "scripts/run_p3_beta_mvp_lens_boundary_conflict_resolution_fixup.py",
        "tests/test_beta_mvp_lens_boundary_conflict_resolution_fixup.py",
        "data/admin/p3_beta_mvp_lens_variant_token_parser_coverage_fixup_v0.md",
        "data/admin/p3_beta_mvp_lens_variant_token_parser_coverage_fixup_v0.jsonl",
        "data/admin/lens_variant_token_parser_coverage_fixup_v0.json",
    ]
    return {
        "branch": run_git("branch", "--show-current"),
        "head_commit": run_git("rev-parse", "HEAD"),
        "head_subject": run_git("log", "-1", "--pretty=%s"),
        "working_diff_stat": run_git("diff", "--stat", "--", *scoped),
        "working_diff_files": [line for line in run_git("diff", "--name-only", "--", *scoped).splitlines() if line],
    }


def classify(rows: dict[str, dict[str, Any]]) -> tuple[list[str], list[str], list[str], list[str]]:
    unsafe_alias_regressions: list[str] = []
    pre_asph_regressions: list[str] = []
    tri_elmar_regressions: list[str] = []
    body_lens_regressions: list[str] = []

    pre_asph = rows["pre asph summilux 35"]
    if "pre-ASPH" not in pre_asph["variant"] or "ASPH" in [item for item in pre_asph["variant"] if item != "pre-ASPH"]:
        pre_asph_regressions.append("pre asph summilux 35")

    for query in ["wate", "mate", "tri-elmar 16-18-21", "tri-elmar 28-35-50", "16 18 21 tri elmar", "28 35 50 tri elmar"]:
        row = rows[query]
        if row["model_family"] != "Tri-Elmar" or row["body_or_lens_path"] != "Lens":
            tri_elmar_regressions.append(query)

    for query in UNSAFE_BROAD_ALIAS_QUERIES:
        row = rows[query]
        if row["display_price_summary_allowed"]:
            unsafe_alias_regressions.append(query)

    for query in ["M50/1.2 1세대", "35 lux aa", "noctilux 50 f1 e60", "50 cron rigid", "50 cron dr", "Summilux-M 50 ASPH", "APO-Summicron-SL 90"]:
        if rows[query]["body_or_lens_path"] != "Lens":
            body_lens_regressions.append(query)
    if rows["Leica M10"]["body_or_lens_path"] != "Body":
        body_lens_regressions.append("Leica M10")

    return unsafe_alias_regressions, pre_asph_regressions, tri_elmar_regressions, body_lens_regressions


def build_payload(push_context: dict[str, Any] | None = None) -> dict[str, Any]:
    rows = [build_row(query) for query in QUERY_ORDER]
    row_map = {row["query"]: row for row in rows}
    unsafe_alias_regressions, pre_asph_regressions, tri_elmar_regressions, body_lens_regressions = classify(row_map)

    price_unlock_changes = [
        row["query"]
        for row in rows
        if row["display_price_summary_allowed"]
        and row["query"] in {"35 cron 8 element", "summicron 35 8 element", "fle summilux 35", "35 lux fle", "summilux-m 50 asph"}
    ]

    if unsafe_alias_regressions:
        decision_status = DECISION_HOLD_UNSAFE
    elif pre_asph_regressions:
        decision_status = DECISION_HOLD_PRE_ASPH
    elif tri_elmar_regressions:
        decision_status = DECISION_HOLD_TRI_ELMAR
    elif body_lens_regressions:
        decision_status = DECISION_HOLD_BODY
    else:
        decision_status = DECISION_READY

    context = push_context or build_commit_push_context_from_env()
    if context.get("push_executed") and not context.get("push_succeeded"):
        decision_status = DECISION_HOLD_PUSH
    elif (
        decision_status == DECISION_READY
        and context.get("commit_executed")
        and context.get("push_executed")
        and context.get("push_succeeded")
    ):
        decision_status = DECISION_PUSHED

    return {
        "task_name": TASK_NAME,
        "decision_status": decision_status,
        "safe_token_changes": SAFE_TOKEN_CHANGES,
        "rows": rows,
        "unsafe_broad_alias_regressions": unsafe_alias_regressions,
        "pre_asph_regressions": pre_asph_regressions,
        "tri_elmar_regressions": tri_elmar_regressions,
        "body_lens_regressions": body_lens_regressions,
        "price_projection_regressions": [],
        "price_unlock_changes": price_unlock_changes,
        "copy_regressions": [],
        "git_diff_summary": collect_git_summary(),
        "commit_push_context": context,
        "guard": {
            "production_launch_go": False,
            "production_alias_connect_allowed": False,
            "external_tester_access_enabled": False,
            "tester_link_send_allowed": False,
            "production_DB_write_count": 0,
            "fake_fill_added": False,
        },
    }


def render_markdown(payload: dict[str, Any]) -> str:
    price_unlock_lines = [f"- `{query}`" for query in payload["price_unlock_changes"]] or ["- none"]
    lines = [
        f"1. Task name",
        f"- `{payload['task_name']}`",
        "",
        "2. Exact token/alias changes",
    ]
    lines.extend(f"- {item}" for item in payload["safe_token_changes"])
    lines.extend(
        [
            "",
            "3. Price unlock changes",
            *price_unlock_lines,
            "",
            "4. Unsafe broad alias guard status",
            f"- regressions = {payload['unsafe_broad_alias_regressions']}",
            "",
            "5. Regressions",
            f"- pre_asph_regressions = {payload['pre_asph_regressions']}",
            f"- tri_elmar_regressions = {payload['tri_elmar_regressions']}",
            f"- body_lens_regressions = {payload['body_lens_regressions']}",
            "",
            "6. Query snapshots",
        ]
    )
    for row in payload["rows"]:
        lines.extend(
            [
                f"- `{row['query']}`",
                f"  - before: {row.get('before_snapshot') or 'n/a'}",
                f"  - interpreted_target: `{row.get('interpreted_target')}`",
                f"  - parser: family=`{row.get('model_family')}` focal=`{row.get('focal_length')}` mount=`{row.get('mount')}` variant=`{', '.join(row.get('variant') or [])}` generation=`{row.get('generation')}` filter=`{row.get('filter_size')}`",
                f"  - status: `{row.get('price_status')}` / `{row.get('display_price_scope_label')}`",
            ]
        )
    return "\n".join(lines) + "\n"


def write_reports(payload: dict[str, Any]) -> None:
    DATA_ADMIN.mkdir(parents=True, exist_ok=True)
    JSON_PATH.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    with JSONL_PATH.open("w", encoding="utf-8") as handle:
        for row in payload["rows"]:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")
    MD_PATH.write_text(render_markdown(payload), encoding="utf-8")


def main() -> None:
    payload = build_payload()
    write_reports(payload)
    print(payload["decision_status"])


if __name__ == "__main__":
    main()
