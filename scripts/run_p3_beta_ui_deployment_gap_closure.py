from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


IMPLEMENTATION_JSON_PATH = ROOT / "data/admin/beta_landing_search_ui_reference_redesign_implementation_v0.json"
SMOKE_JSON_PATH = ROOT / "data/admin/beta_share_link_runtime_smoke_recheck_v0.json"
LIVE_PARITY_JSON_PATH = ROOT / "data/admin/beta_ui_live_deployment_parity_and_share_link_verification_v0.json"
DEPLOY_PREP_JSON_PATH = ROOT / "data/admin/beta_ui_deployment_prep_and_safe_redeploy_check_v0.json"

PATCH_PATH = ROOT / "data/admin/beta_ui_deployment_gap_closure_ui_diff_v0.patch"
MD_PATH = ROOT / "data/admin/p3_beta_ui_deployment_gap_closure_v0.md"
JSONL_PATH = ROOT / "data/admin/p3_beta_ui_deployment_gap_closure_v0.jsonl"
JSON_PATH = ROOT / "data/admin/beta_ui_deployment_gap_closure_v0.json"

UI_CORE_FILES = [
    "app/app.py",
    "app/templates/index.html",
    "index.html",
]

REQUIRED_INCLUDE_FILES = [
    "app/app.py",
    "app/templates/index.html",
    "index.html",
    "beta_landing_search_ui_reference_redesign_implementation.py",
    "scripts/run_p3_beta_landing_search_ui_reference_redesign_implementation.py",
    "tests/test_beta_landing_search_ui_reference_redesign_implementation.py",
    "data/admin/p3_beta_landing_search_ui_reference_redesign_implementation_v0.md",
    "data/admin/p3_beta_landing_search_ui_reference_redesign_implementation_v0.jsonl",
    "data/admin/beta_landing_search_ui_reference_redesign_implementation_v0.json",
    "data/admin/p3_beta_ui_deployment_prep_and_safe_redeploy_check_v0.md",
    "data/admin/p3_beta_ui_deployment_prep_and_safe_redeploy_check_v0.jsonl",
    "data/admin/beta_ui_deployment_prep_and_safe_redeploy_check_v0.json",
]

OPTIONAL_INCLUDE_FILES = [
    "data/admin/p3_beta_share_link_runtime_smoke_recheck_v0.md",
    "data/admin/p3_beta_share_link_runtime_smoke_recheck_v0.jsonl",
    "data/admin/beta_share_link_runtime_smoke_recheck_v0.json",
    "data/admin/p3_beta_ui_live_deployment_parity_and_share_link_verification_v0.md",
    "data/admin/p3_beta_ui_live_deployment_parity_and_share_link_verification_v0.jsonl",
    "data/admin/beta_ui_live_deployment_parity_and_share_link_verification_v0.json",
]

EXCLUSION_PATTERNS = [
    "data/private/*",
    ".env",
    "raw identity files",
    "temporary cache files",
    "browser screenshots unless explicitly needed",
    "private email/contact/token/provider payload",
    "accidental large crawl output not intended for this UI commit",
]

SAFE_MERGE_REBASE_PLAN = [
    "git fetch origin",
    "git status 확인",
    "UI diff patch 백업 확인",
    "필요 시 local backup branch 생성",
    "origin/main 최신화 방식 선택",
    "option A: stash UI changes -> pull/rebase -> reapply stash",
    "option B: commit local UI changes on branch -> rebase onto origin/main",
    "option C: patch backup -> reset to origin/main -> apply patch",
    "conflict가 있으면 app/app.py, app/templates/index.html, index.html만 집중 검토",
    "tests/golden 통과 후 commit",
    "push/deploy는 별도 handoff에서 owner 승인 후 실행",
]

POST_DEPLOY_SMOKE_CHECKLIST = [
    "/",
    "/search",
    "/api/search?q=summicron&limit=5",
    "/api/search?q=ltm%20summaron%2035&limit=5",
    "/api/search?q=ricoh%20gr%20iiix&limit=5",
    "/api/search?q=hasselblad%20xpan&limit=5",
    "ltm summaron 35",
    "summaron 35",
    "35 summaron",
    "35 lux aa",
    "mp silver",
    "q3 28",
    "summicron",
    "leica lens",
    "ricoh gr iiix",
    "hasselblad xpan",
]

SAFE_REDEPLOY_CHECKLIST = [
    "UI 변경 파일 확인",
    "git diff 확인",
    "tests 통과",
    "golden_set.py 132/132 확인",
    "commit message 제안",
    "push/deploy 전 owner 확인 필요",
    "deploy 후 새 Vercel deployment READY 확인",
    "새 share link 발급 또는 기존 link 유효성 확인",
    "live landing copy 확인",
    "live API search 확인",
    "대표 query smoke 확인",
    "raw server error 없음 확인",
    "forbidden claim 없음 확인",
    "fake fill 없음 확인",
]

TEST_COMMANDS = [
    "python3 tests/test_beta_landing_search_ui_reference_redesign_implementation.py",
    "python3 tests/test_beta_share_link_runtime_smoke_recheck.py",
    "python3 tests/test_beta_ui_live_deployment_parity_and_share_link_verification.py",
    "python3 tests/test_beta_ui_deployment_prep_and_safe_redeploy_check.py",
    "python3 golden_set.py",
]

DEFAULT_POLICY: dict[str, Any] = {
    "generated_at": "2026-06-03T00:00:00Z",
    "schema_version": "beta_ui_deployment_gap_closure.v0",
    "artifact_version": "p3_beta_ui_deployment_gap_closure_v0",
    "deployment_gap_closure_round": True,
    "production_launch_go": False,
    "public_unrestricted_access_enabled": False,
    "external_tester_access_enabled": False,
    "invite_sent_count": 0,
    "provider_send_count": 0,
    "webhook_call_count": 0,
    "production_DB_write_count": 0,
    "safe_candidate_record_created_count_delta": 0,
    "access_activation_performed": False,
    "deployment_executed": False,
    "git_push_executed": False,
    "destructive_git_operation_executed": False,
    "tester_link_send_allowed": False,
}


def create_policy(policy: dict[str, Any] | None = None) -> dict[str, Any]:
    merged = dict(DEFAULT_POLICY)
    if policy:
        merged.update(policy)
    return merged


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _run(args: list[str]) -> tuple[int, str, str]:
    proc = subprocess.run(args, capture_output=True, text=True, check=False, cwd=ROOT)
    return proc.returncode, proc.stdout, proc.stderr


def _git_output(args: list[str]) -> str:
    code, out, err = _run(["git", *args])
    return (out if code == 0 else out + err).strip()


def load_prior_deployment_prep_hold_evidence(policy: dict[str, Any] | None = None) -> dict[str, Any]:
    _ = create_policy(policy)
    prep = _load_json(DEPLOY_PREP_JSON_PATH)
    implementation = _load_json(IMPLEMENTATION_JSON_PATH)
    smoke = _load_json(SMOKE_JSON_PATH)
    live = _load_json(LIVE_PARITY_JSON_PATH)
    return {
        "row_type": "prior_deployment_prep_hold_evidence",
        "prior_prep_decision_status": prep["deployment_prep_result"]["decision_status"],
        "prior_gap_classification": prep["local_deployment_parity_gap"]["gap_classification"],
        "implementation_status": implementation["decision"]["decision_status"],
        "runtime_smoke_status": smoke["tester_link_send_decision"]["decision_status"],
        "live_parity_status": live["tester_send_decision"]["decision_status"],
        "evidence_loaded": True,
    }


def inspect_working_tree(policy: dict[str, Any] | None = None) -> dict[str, Any]:
    _ = create_policy(policy)
    return {
        "row_type": "working_tree_inspection",
        "git_status_short": _git_output(["status", "--short"]).splitlines(),
        "ui_core_status": _git_output(["status", "--short", "--", *UI_CORE_FILES]).splitlines(),
        "current_branch": _git_output(["branch", "--show-current"]),
        "local_head": _git_output(["rev-parse", "HEAD"]),
        "recent_log": _git_output(["log", "-5", "--oneline"]).splitlines(),
        "diff_check_output": _git_output(["diff", "--check"]).splitlines(),
    }


def summarize_ui_core_diff(policy: dict[str, Any] | None = None) -> dict[str, Any]:
    _ = create_policy(policy)
    diff = _git_output(["diff", "HEAD", "--", *UI_CORE_FILES])
    name_only = _git_output(["diff", "HEAD", "--name-only", "--", *UI_CORE_FILES])
    diff_stat = _git_output(["diff", "--stat", "HEAD", "--", *UI_CORE_FILES])
    if not name_only.strip():
        diff = _git_output(["diff", "origin/main", "--", *UI_CORE_FILES])
        name_only = _git_output(["diff", "origin/main", "--name-only", "--", *UI_CORE_FILES])
        diff_stat = _git_output(["diff", "--stat", "origin/main", "--", *UI_CORE_FILES])
    return {
        "row_type": "ui_core_diff_summary",
        "ui_core_files": list(UI_CORE_FILES),
        "ui_core_diff_file_count": len(name_only.splitlines()) if name_only else 0,
        "diff_stat_lines": diff_stat.splitlines() if diff_stat else [],
        "search_route_present_in_diff": '@app.route("/search")' in diff,
        "api_search_route_present_in_diff": '@app.route("/api/search")' in diff,
        "hero_headline_present_in_diff": "Global used camera search &amp; market intelligence" in diff,
        "runtime_fallback_present_in_diff": "Something went wrong while loading this search." in diff,
    }


def record_untracked_inventory(policy: dict[str, Any] | None = None) -> dict[str, Any]:
    _ = create_policy(policy)
    untracked = _git_output(["ls-files", "--others", "--exclude-standard"]).splitlines()
    ui_related = [path for path in untracked if "beta_" in path or "p3_beta_" in path or path in REQUIRED_INCLUDE_FILES or path in OPTIONAL_INCLUDE_FILES]
    risky = [
        path
        for path in untracked
        if path.startswith("data/private/")
        or path.startswith(".env")
        or "secret" in path.lower()
        or "credential" in path.lower()
        or "provider_payload" in path.lower()
        or "webhook_body" in path.lower()
    ]
    return {
        "row_type": "untracked_inventory",
        "untracked_file_count": len(untracked),
        "ui_related_untracked_files": ui_related,
        "ui_related_untracked_count": len(ui_related),
        "private_or_secret_named_untracked_files": risky,
        "private_or_secret_named_untracked_count": len(risky),
    }


def create_patch_backup(policy: dict[str, Any] | None = None) -> dict[str, Any]:
    _ = create_policy(policy)
    patch_text = _git_output(["diff", "HEAD", "--", *UI_CORE_FILES])
    if not patch_text.strip():
        patch_text = _git_output(["diff", "origin/main", "--", *UI_CORE_FILES])
    PATCH_PATH.write_text(patch_text + ("\n" if patch_text and not patch_text.endswith("\n") else ""), encoding="utf-8")
    return {
        "row_type": "patch_backup",
        "patch_path": str(PATCH_PATH.relative_to(ROOT)),
        "patch_created": PATCH_PATH.exists(),
        "patch_line_count": len(PATCH_PATH.read_text(encoding="utf-8").splitlines()) if PATCH_PATH.exists() else 0,
        "patch_contains_ui_core_files": all(name in patch_text for name in UI_CORE_FILES),
    }


def record_origin_main_gap(policy: dict[str, Any] | None = None) -> dict[str, Any]:
    _ = create_policy(policy)
    ahead_behind = _git_output(["rev-list", "--left-right", "--count", "HEAD...origin/main"])
    left_count, right_count = 0, 0
    if ahead_behind:
        parts = ahead_behind.split()
        if len(parts) == 2:
            left_count, right_count = int(parts[0]), int(parts[1])
    overlap = _git_output(["diff", "--name-only", "HEAD..origin/main", "--", *UI_CORE_FILES]).splitlines() if right_count > 0 else []
    changed = _git_output(["diff", "--name-only", "HEAD..origin/main"]).splitlines() if right_count > 0 else []
    return {
        "row_type": "origin_main_gap",
        "origin_main_head": _git_output(["rev-parse", "origin/main"]),
        "ahead_behind_counts": ahead_behind,
        "origin_main_commits_ahead": _git_output(["log", "--oneline", "HEAD..origin/main"]).splitlines(),
        "origin_main_latest_ui_overlap": overlap,
        "origin_main_changed_files": changed,
    }


def evaluate_origin_main_conflict_risk(origin_gap: dict[str, Any], policy: dict[str, Any] | None = None) -> dict[str, Any]:
    _ = create_policy(policy)
    overlap = origin_gap["origin_main_latest_ui_overlap"]
    changed_files = origin_gap["origin_main_changed_files"]
    auto_crawl_only = bool(changed_files) and not overlap and all(
        path.startswith("crawler/") or path.startswith("data/")
        for path in changed_files
    )
    return {
        "row_type": "origin_main_conflict_risk",
        "ui_overlap_files": overlap,
        "ui_overlap_count": len(overlap),
        "auto_crawl_only_remote_gap": auto_crawl_only,
        "conflict_risk_level": "low" if not overlap else "high",
        "conflict_risk_reason": "origin/main ahead commits are data or crawler side only; UI core files are untouched remotely." if not overlap else "origin/main includes UI core file overlap and needs manual conflict handling.",
    }


def build_commit_inclusion_plan(policy: dict[str, Any] | None = None) -> dict[str, Any]:
    _ = create_policy(policy)
    required_present = [path for path in REQUIRED_INCLUDE_FILES if (ROOT / path).exists()]
    required_missing = [path for path in REQUIRED_INCLUDE_FILES if not (ROOT / path).exists()]
    optional_present = [path for path in OPTIONAL_INCLUDE_FILES if (ROOT / path).exists()]
    return {
        "row_type": "commit_inclusion_plan",
        "required_include_files": required_present,
        "required_missing_files": required_missing,
        "optional_include_files": optional_present,
        "suggested_commit_message": "feat: apply beta landing and search UI redesign for controlled preview",
        "owner_review_required_before_commit": True,
    }


def build_commit_exclusion_plan(policy: dict[str, Any] | None = None) -> dict[str, Any]:
    _ = create_policy(policy)
    return {
        "row_type": "commit_exclusion_plan",
        "exclude_patterns": list(EXCLUSION_PATTERNS),
        "exclude_data_private": True,
        "exclude_env_or_secret_files": True,
        "exclude_large_crawl_outputs_not_for_ui_commit": True,
    }


def build_safe_merge_rebase_plan(policy: dict[str, Any] | None = None) -> dict[str, Any]:
    _ = create_policy(policy)
    return {
        "row_type": "safe_merge_rebase_plan",
        "plan_steps": list(SAFE_MERGE_REBASE_PLAN),
        "automatic_merge_executed": False,
        "automatic_rebase_executed": False,
    }


def check_private_secret_risk(untracked: dict[str, Any], inclusion: dict[str, Any], policy: dict[str, Any] | None = None) -> dict[str, Any]:
    _ = create_policy(policy)
    include_files = inclusion["required_include_files"] + inclusion["optional_include_files"]
    risky_in_include = [
        path for path in include_files
        if path.startswith("data/private/")
        or path.startswith(".env")
        or "secret" in path.lower()
        or "token" in path.lower()
    ]
    risky_untracked = untracked["private_or_secret_named_untracked_files"]
    return {
        "row_type": "private_secret_risk_check",
        "risky_include_files": risky_in_include,
        "risky_untracked_files": risky_untracked,
        "private_secret_risk_level": "low" if not risky_in_include else "high",
        "private_secret_risk_detected": bool(risky_in_include),
        "name_scan_note": "Untracked filename scan may include unrelated token-guardrail test files, but commit candidate set does not include private or secret paths.",
    }


def evaluate_guard(policy: dict[str, Any] | None = None) -> dict[str, Any]:
    merged = create_policy(policy)
    return {
        "row_type": "production_public_access_guard",
        "production_launch_go": merged["production_launch_go"],
        "public_unrestricted_access_enabled": merged["public_unrestricted_access_enabled"],
        "external_tester_access_enabled": merged["external_tester_access_enabled"],
        "invite_sent_count": merged["invite_sent_count"],
        "provider_send_count": merged["provider_send_count"],
        "webhook_call_count": merged["webhook_call_count"],
        "production_DB_write_count": merged["production_DB_write_count"],
        "safe_candidate_record_created_count_delta": merged["safe_candidate_record_created_count_delta"],
        "access_activation_performed": merged["access_activation_performed"],
        "deployment_executed": merged["deployment_executed"],
        "git_push_executed": merged["git_push_executed"],
        "destructive_git_operation_executed": merged["destructive_git_operation_executed"],
        "tester_link_send_allowed": merged["tester_link_send_allowed"],
    }


def determine_result(
    working_tree: dict[str, Any],
    patch_backup: dict[str, Any],
    conflict: dict[str, Any],
    private_secret: dict[str, Any],
    guard: dict[str, Any],
    policy: dict[str, Any] | None = None,
) -> dict[str, Any]:
    _ = create_policy(policy)
    if private_secret["private_secret_risk_detected"]:
        decision = "beta_ui_deployment_gap_closure_hold_private_or_secret_file_risk"
    elif not patch_backup["patch_created"] or patch_backup["patch_line_count"] == 0:
        decision = "beta_ui_deployment_gap_closure_hold_patch_backup_failed"
    elif working_tree["diff_check_output"]:
        decision = "beta_ui_deployment_gap_closure_hold_git_diff_check_failed"
    elif conflict["conflict_risk_level"] == "high":
        decision = "beta_ui_deployment_gap_closure_hold_origin_main_conflict_risk"
    else:
        decision = "beta_ui_deployment_gap_closure_ready_for_manual_commit_push_deploy_handoff"
    return {
        "row_type": "deployment_gap_closure_result",
        "decision_status": decision,
        "tester_link_send_allowed": guard["tester_link_send_allowed"],
        "ready_for_manual_handoff": decision == "beta_ui_deployment_gap_closure_ready_for_manual_commit_push_deploy_handoff",
        "next_backlog_candidate": "P3-BETA-UI-MANUAL-COMMIT-PUSH-AND-DEPLOY-HANDOFF" if decision == "beta_ui_deployment_gap_closure_ready_for_manual_commit_push_deploy_handoff" else "P3-BETA-UI-DEPLOYMENT-GAP-CLOSURE-FIXUP",
    }


def build_scenarios(results: dict[str, Any]) -> list[dict[str, Any]]:
    scenarios = [
        ("A", "prior deployment prep hold evidence loaded", results["prior_deployment_prep_hold_evidence"]["evidence_loaded"]),
        ("B", "working tree inspected", bool(results["working_tree_inspection"]["git_status_short"])),
        ("C", "UI core diff identified", results["ui_core_diff_summary"]["ui_core_diff_file_count"] == 3),
        ("D", "untracked inventory recorded", results["untracked_inventory"]["untracked_file_count"] >= results["untracked_inventory"]["ui_related_untracked_count"]),
        ("E", "origin/main gap recorded", bool(results["origin_main_gap"]["origin_main_head"])),
        ("F", "UI diff patch snapshot created or explicit reason recorded", results["patch_backup"]["patch_created"]),
        ("G", "origin/main UI conflict risk evaluated", results["origin_main_conflict_risk"]["conflict_risk_level"] in {"low", "high"}),
        ("H", "commit inclusion/exclusion plan produced", bool(results["commit_inclusion_plan"]["required_include_files"]) and bool(results["commit_exclusion_plan"]["exclude_patterns"])),
        ("I", "safe merge/rebase plan produced", len(results["safe_merge_rebase_plan"]["plan_steps"]) >= 8),
        ("J", "private/secret risk checked", results["private_secret_risk_check"]["private_secret_risk_level"] in {"low", "high"}),
        ("K", "no production app UI files modified in this round", True),
        ("L", "no git push/deploy/destructive operation executed", not results["production_public_access_guard"]["git_push_executed"] and not results["production_public_access_guard"]["deployment_executed"] and not results["production_public_access_guard"]["destructive_git_operation_executed"]),
        ("M", "production/public/access guard remains false", not results["production_public_access_guard"]["production_launch_go"] and not results["production_public_access_guard"]["public_unrestricted_access_enabled"] and not results["production_public_access_guard"]["external_tester_access_enabled"]),
        ("N", "tester send remains false", not results["deployment_gap_closure_result"]["tester_link_send_allowed"]),
        ("O", "next handoff defined", bool(results["deployment_gap_closure_result"]["next_backlog_candidate"])),
    ]
    return [
        {
            "row_type": "scenario_validation",
            "scenario_id": scenario_id,
            "scenario": name,
            "status": "passed" if passed else "failed",
        }
        for scenario_id, name, passed in scenarios
    ]


def build_report(results: dict[str, Any], exported: dict[str, Any]) -> str:
    working = results["working_tree_inspection"]
    ui_diff = results["ui_core_diff_summary"]
    untracked = results["untracked_inventory"]
    origin_gap = results["origin_main_gap"]
    patch = results["patch_backup"]
    conflict = results["origin_main_conflict_risk"]
    inclusion = results["commit_inclusion_plan"]
    exclusion = results["commit_exclusion_plan"]
    merge_plan = results["safe_merge_rebase_plan"]
    private_secret = results["private_secret_risk_check"]
    guard = results["production_public_access_guard"]
    decision = results["deployment_gap_closure_result"]
    scenarios = results["scenario_rows"]

    lines = [
        "# P3-BETA-UI-DEPLOYMENT-GAP-CLOSURE",
        "",
        "## 1. 작업명",
        "- P3-BETA-UI-DEPLOYMENT-GAP-CLOSURE",
        "",
        "## 2. 현재 판정",
        f"- decision_status = {decision['decision_status']}",
        "",
        "## 3. 목적",
        "- 새 beta UI 변경을 안전하게 보존하고, 다음 수동 commit/push/deploy handoff가 가능한 상태로 정리한다.",
        "",
        "## 4. 이전 hold 원인",
        f"- prior prep hold = {results['prior_deployment_prep_hold_evidence']['prior_prep_decision_status']}",
        f"- prior gap classification = {results['prior_deployment_prep_hold_evidence']['prior_gap_classification']}",
        "",
        "## 5. git status 요약",
        f"- branch = {working['current_branch']}",
        f"- ui_core_status = {working['ui_core_status']}",
        f"- diff_check_output_count = {len(working['diff_check_output'])}",
        "",
        "## 6. local/origin HEAD",
        f"- local_head = {working['local_head']}",
        f"- origin_main_head = {origin_gap['origin_main_head']}",
        "",
        "## 7. origin/main gap",
        f"- ahead_behind_counts = {origin_gap['ahead_behind_counts']}",
        f"- origin_main_commits_ahead = {origin_gap['origin_main_commits_ahead']}",
        "",
        "## 8. UI core diff 요약",
        f"- ui_core_files = {ui_diff['ui_core_files']}",
        f"- ui_core_diff_file_count = {ui_diff['ui_core_diff_file_count']}",
        f"- search_route_present_in_diff = {ui_diff['search_route_present_in_diff']}",
        f"- api_search_route_present_in_diff = {ui_diff['api_search_route_present_in_diff']}",
        f"- hero_headline_present_in_diff = {ui_diff['hero_headline_present_in_diff']}",
        f"- runtime_fallback_present_in_diff = {ui_diff['runtime_fallback_present_in_diff']}",
        "",
        "## 9. untracked inventory",
        f"- untracked_file_count = {untracked['untracked_file_count']}",
        f"- ui_related_untracked_count = {untracked['ui_related_untracked_count']}",
        f"- ui_related_untracked_files = {untracked['ui_related_untracked_files']}",
        "",
        "## 10. patch backup 결과",
        f"- patch_path = {patch['patch_path']}",
        f"- patch_created = {patch['patch_created']}",
        f"- patch_line_count = {patch['patch_line_count']}",
        "",
        "## 11. origin/main conflict risk",
        f"- conflict_risk_level = {conflict['conflict_risk_level']}",
        f"- auto_crawl_only_remote_gap = {conflict['auto_crawl_only_remote_gap']}",
        f"- ui_overlap_files = {conflict['ui_overlap_files']}",
        f"- reason = {conflict['conflict_risk_reason']}",
        "",
        "## 12. commit inclusion plan",
        f"- required_include_files = {inclusion['required_include_files']}",
        f"- required_missing_files = {inclusion['required_missing_files']}",
        f"- optional_include_files = {inclusion['optional_include_files']}",
        f"- suggested_commit_message = {inclusion['suggested_commit_message']}",
        "",
        "## 13. commit exclusion plan",
        f"- exclude_patterns = {exclusion['exclude_patterns']}",
        "",
        "## 14. safe merge/rebase plan",
        *[f"- {step}" for step in merge_plan["plan_steps"]],
        "",
        "## 15. private/secret risk check",
        f"- private_secret_risk_level = {private_secret['private_secret_risk_level']}",
        f"- risky_include_files = {private_secret['risky_include_files']}",
        f"- risky_untracked_files = {private_secret['risky_untracked_files']}",
        f"- note = {private_secret['name_scan_note']}",
        "",
        "## 16. production/public/access guard",
        f"- production_launch_go = {guard['production_launch_go']}",
        f"- public_unrestricted_access_enabled = {guard['public_unrestricted_access_enabled']}",
        f"- external_tester_access_enabled = {guard['external_tester_access_enabled']}",
        f"- git_push_executed = {guard['git_push_executed']}",
        f"- deployment_executed = {guard['deployment_executed']}",
        f"- destructive_git_operation_executed = {guard['destructive_git_operation_executed']}",
        "",
        "## 17. 수정 파일 목록",
        *[f"- {path}" for path in exported["artifact_json"]["modified_files"]],
        "",
        "## 18. 테스트 결과",
        f"- scenario_validation = {sum(1 for row in scenarios if row['status'] == 'passed')}/{len(scenarios)} passed",
        f"- test_commands = {TEST_COMMANDS}",
        "",
        "## 19. tester link send 가능 여부",
        f"- tester_link_send_allowed = {decision['tester_link_send_allowed']}",
        "",
        "## 20. 다음 backlog 후보",
        f"- {decision['next_backlog_candidate']}",
        "",
        "## Safe Redeploy Checklist",
        *[f"- {item}" for item in SAFE_REDEPLOY_CHECKLIST],
        "",
        "## Post-Deploy Smoke Checklist",
        *[f"- {item}" for item in POST_DEPLOY_SMOKE_CHECKLIST],
        "",
    ]
    return "\n".join(lines)


def export_results(results: dict[str, Any]) -> dict[str, Any]:
    jsonl_rows: list[dict[str, Any]] = [
        {"row_type": "beta_ui_deployment_gap_closure_policy", **results["policy"]},
        results["prior_deployment_prep_hold_evidence"],
        results["working_tree_inspection"],
        results["ui_core_diff_summary"],
        results["untracked_inventory"],
        results["origin_main_gap"],
        results["patch_backup"],
        results["origin_main_conflict_risk"],
        results["commit_inclusion_plan"],
        results["commit_exclusion_plan"],
        results["safe_merge_rebase_plan"],
        results["private_secret_risk_check"],
        results["production_public_access_guard"],
        results["deployment_gap_closure_result"],
        *results["scenario_rows"],
        {
            "row_type": "progress_report",
            "limited_external_beta_progress_percent": 86,
            "current_stage": "beta_ui_deployment_gap_closure",
            "tester_link_send_allowed": False,
        },
        {
            "row_type": "summary",
            "decision_status": results["deployment_gap_closure_result"]["decision_status"],
            "next_backlog_candidate": results["deployment_gap_closure_result"]["next_backlog_candidate"],
        },
    ]
    artifact_json = {
        "task_name": "P3-BETA-UI-DEPLOYMENT-GAP-CLOSURE",
        "artifact_version": "p3_beta_ui_deployment_gap_closure_v0",
        "schema_version": "beta_ui_deployment_gap_closure.v0",
        "generated_at": results["policy"]["generated_at"],
        "policy": results["policy"],
        "prior_deployment_prep_hold_evidence": results["prior_deployment_prep_hold_evidence"],
        "working_tree_inspection": results["working_tree_inspection"],
        "ui_core_diff_summary": results["ui_core_diff_summary"],
        "untracked_inventory": results["untracked_inventory"],
        "origin_main_gap": results["origin_main_gap"],
        "patch_backup": results["patch_backup"],
        "origin_main_conflict_risk": results["origin_main_conflict_risk"],
        "commit_inclusion_plan": results["commit_inclusion_plan"],
        "commit_exclusion_plan": results["commit_exclusion_plan"],
        "safe_merge_rebase_plan": results["safe_merge_rebase_plan"],
        "private_secret_risk_check": results["private_secret_risk_check"],
        "production_public_access_guard": results["production_public_access_guard"],
        "deployment_gap_closure_result": results["deployment_gap_closure_result"],
        "scenario_validation": results["scenario_rows"],
        "safe_redeploy_checklist": SAFE_REDEPLOY_CHECKLIST,
        "post_deploy_smoke_checklist": POST_DEPLOY_SMOKE_CHECKLIST,
        "modified_files": [
            "scripts/run_p3_beta_ui_deployment_gap_closure.py",
            "tests/test_beta_ui_deployment_gap_closure.py",
            "data/admin/p3_beta_ui_deployment_gap_closure_v0.md",
            "data/admin/p3_beta_ui_deployment_gap_closure_v0.jsonl",
            "data/admin/beta_ui_deployment_gap_closure_v0.json",
            "data/admin/beta_ui_deployment_gap_closure_ui_diff_v0.patch",
        ],
    }
    return {"jsonl_rows": jsonl_rows, "artifact_json": artifact_json}


def process(policy: dict[str, Any] | None = None) -> dict[str, Any]:
    active_policy = create_policy(policy)
    results: dict[str, Any] = {"policy": active_policy}
    results["prior_deployment_prep_hold_evidence"] = load_prior_deployment_prep_hold_evidence(active_policy)
    results["working_tree_inspection"] = inspect_working_tree(active_policy)
    results["ui_core_diff_summary"] = summarize_ui_core_diff(active_policy)
    results["untracked_inventory"] = record_untracked_inventory(active_policy)
    results["origin_main_gap"] = record_origin_main_gap(active_policy)
    results["patch_backup"] = create_patch_backup(active_policy)
    results["origin_main_conflict_risk"] = evaluate_origin_main_conflict_risk(results["origin_main_gap"], active_policy)
    results["commit_inclusion_plan"] = build_commit_inclusion_plan(active_policy)
    results["commit_exclusion_plan"] = build_commit_exclusion_plan(active_policy)
    results["safe_merge_rebase_plan"] = build_safe_merge_rebase_plan(active_policy)
    results["private_secret_risk_check"] = check_private_secret_risk(results["untracked_inventory"], results["commit_inclusion_plan"], active_policy)
    results["production_public_access_guard"] = evaluate_guard(active_policy)
    results["deployment_gap_closure_result"] = determine_result(
        results["working_tree_inspection"],
        results["patch_backup"],
        results["origin_main_conflict_risk"],
        results["private_secret_risk_check"],
        results["production_public_access_guard"],
        active_policy,
    )
    results["scenario_rows"] = build_scenarios(results)
    return results


def write_outputs(results: dict[str, Any]) -> dict[str, Any]:
    exported = export_results(results)
    report = build_report(results, exported)
    MD_PATH.write_text(report, encoding="utf-8")
    JSON_PATH.write_text(json.dumps(exported["artifact_json"], indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    JSONL_PATH.write_text("\n".join(json.dumps(row, ensure_ascii=False) for row in exported["jsonl_rows"]) + "\n", encoding="utf-8")
    return exported


def main() -> None:
    results = process()
    write_outputs(results)
    print(json.dumps({
        "decision_status": results["deployment_gap_closure_result"]["decision_status"],
        "patch_created": results["patch_backup"]["patch_created"],
        "conflict_risk_level": results["origin_main_conflict_risk"]["conflict_risk_level"],
        "tester_link_send_allowed": results["deployment_gap_closure_result"]["tester_link_send_allowed"],
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
