from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


GAP_JSON_PATH = ROOT / "data/admin/beta_ui_deployment_gap_closure_v0.json"
PREP_JSON_PATH = ROOT / "data/admin/beta_ui_deployment_prep_and_safe_redeploy_check_v0.json"
IMPLEMENTATION_JSON_PATH = ROOT / "data/admin/beta_landing_search_ui_reference_redesign_implementation_v0.json"
SMOKE_JSON_PATH = ROOT / "data/admin/beta_share_link_runtime_smoke_recheck_v0.json"
LIVE_PARITY_JSON_PATH = ROOT / "data/admin/beta_ui_live_deployment_parity_and_share_link_verification_v0.json"

MD_PATH = ROOT / "data/admin/p3_beta_ui_manual_commit_push_and_deploy_handoff_v0.md"
JSONL_PATH = ROOT / "data/admin/p3_beta_ui_manual_commit_push_and_deploy_handoff_v0.jsonl"
JSON_PATH = ROOT / "data/admin/beta_ui_manual_commit_push_and_deploy_handoff_v0.json"

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
    "data/admin/p3_beta_ui_deployment_gap_closure_v0.md",
    "data/admin/p3_beta_ui_deployment_gap_closure_v0.jsonl",
    "data/admin/beta_ui_deployment_gap_closure_v0.json",
    "data/admin/beta_ui_deployment_gap_closure_ui_diff_v0.patch",
]

OPTIONAL_INCLUDE_FILES = [
    "data/admin/p3_beta_share_link_runtime_smoke_recheck_v0.md",
    "data/admin/p3_beta_share_link_runtime_smoke_recheck_v0.jsonl",
    "data/admin/beta_share_link_runtime_smoke_recheck_v0.json",
    "data/admin/p3_beta_ui_live_deployment_parity_and_share_link_verification_v0.md",
    "data/admin/p3_beta_ui_live_deployment_parity_and_share_link_verification_v0.jsonl",
    "data/admin/beta_ui_live_deployment_parity_and_share_link_verification_v0.json",
]

EXCLUDE_FILES = [
    "data/private/*",
    ".env",
    "raw identity files",
    "private email/contact/token/provider payload",
    "temporary cache files",
    "browser screenshots unless explicitly needed",
    "accidental large crawl output not intended for this UI commit",
    "unrelated untracked files",
    "any local secret/config file",
]

MANUAL_COMMAND_SEQUENCE = [
    "git status --short",
    "git branch --show-current",
    "git rev-parse HEAD",
    "git rev-parse origin/main",
    "test -f data/admin/beta_ui_deployment_gap_closure_ui_diff_v0.patch",
    "git diff -- app/app.py app/templates/index.html index.html > data/admin/manual_pre_commit_ui_diff_check.patch",
    "git checkout -b beta-ui-redesign-controlled-preview",
    "git add app/app.py app/templates/index.html index.html",
    "git add beta_landing_search_ui_reference_redesign_implementation.py",
    "git add scripts/run_p3_beta_landing_search_ui_reference_redesign_implementation.py",
    "git add tests/test_beta_landing_search_ui_reference_redesign_implementation.py",
    "git add data/admin/p3_beta_landing_search_ui_reference_redesign_implementation_v0.md",
    "git add data/admin/p3_beta_landing_search_ui_reference_redesign_implementation_v0.jsonl",
    "git add data/admin/beta_landing_search_ui_reference_redesign_implementation_v0.json",
    "git add data/admin/p3_beta_ui_deployment_prep_and_safe_redeploy_check_v0.md",
    "git add data/admin/p3_beta_ui_deployment_prep_and_safe_redeploy_check_v0.jsonl",
    "git add data/admin/beta_ui_deployment_prep_and_safe_redeploy_check_v0.json",
    "git add data/admin/p3_beta_ui_deployment_gap_closure_v0.md",
    "git add data/admin/p3_beta_ui_deployment_gap_closure_v0.jsonl",
    "git add data/admin/beta_ui_deployment_gap_closure_v0.json",
    "git add data/admin/beta_ui_deployment_gap_closure_ui_diff_v0.patch",
    "git status --short",
    "python3 tests/test_beta_landing_search_ui_reference_redesign_implementation.py",
    "python3 tests/test_beta_share_link_runtime_smoke_recheck.py",
    "python3 tests/test_beta_ui_live_deployment_parity_and_share_link_verification.py",
    "python3 tests/test_beta_ui_deployment_prep_and_safe_redeploy_check.py",
    "python3 tests/test_beta_ui_deployment_gap_closure.py",
    "python3 golden_set.py",
    'git commit -m "feat: apply beta landing and search UI redesign for controlled preview"',
    "git fetch origin",
    "git rebase origin/main",
    "python3 tests/test_beta_landing_search_ui_reference_redesign_implementation.py",
    "python3 golden_set.py",
    "git status --short",
    "git push origin beta-ui-redesign-controlled-preview",
]

DEPLOY_STRATEGY_OPTIONS = [
    {
        "option_id": "deploy_strategy_pr_merge",
        "label": "PR/merge 방식",
        "recommended": True,
        "reason": "auto crawl commits가 main을 계속 전진시키므로 reviewable branch와 merge 지점이 명확한 방식이 가장 안전하다.",
    },
    {
        "option_id": "deploy_strategy_main_direct_push",
        "label": "main 직접 push",
        "recommended": False,
        "reason": "UI 변경 범위를 빠르게 올릴 수 있지만 auto crawl 흐름과 섞일 때 추적성과 review 안정성이 떨어진다.",
    },
    {
        "option_id": "deploy_strategy_preview_then_promote",
        "label": "preview deployment 확인 후 production 반영",
        "recommended": True,
        "reason": "새 landing/search UI와 runtime fallback을 live와 최대한 비슷한 조건에서 먼저 검증할 수 있다.",
    },
]

POST_DEPLOY_SMOKE_CHECKLIST = [
    "Vercel deployment state = READY",
    "최신 deployment commit이 UI commit 포함",
    "share/access link 유효",
    "/ landing 200",
    "/search 200",
    "/api/search?q=summicron&limit=5 200",
    "/api/search?q=ltm%20summaron%2035&limit=5 200",
    "/api/search?q=ricoh%20gr%20iiix&limit=5 200",
    "/api/search?q=hasselblad%20xpan&limit=5 200",
    "Global used camera search & market intelligence 존재",
    "Independent project 존재",
    "Not affiliated with Leica, dealers, or marketplaces 존재",
    "Prices are references, not guaranteed valuations 존재",
    "A server error has occurred 부재",
    "official Leica service 부재",
    "guaranteed valuation 부재",
    "guaranteed lowest price 부재",
    "complete global coverage 부재",
    "confirmed absence 부재",
    "all listings real-time 부재",
    "dealer verified 부재",
    "public launch ready 부재",
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

DEFAULT_POLICY: dict[str, Any] = {
    "generated_at": "2026-06-03T00:00:00Z",
    "schema_version": "beta_ui_manual_commit_push_and_deploy_handoff.v0",
    "artifact_version": "p3_beta_ui_manual_commit_push_and_deploy_handoff_v0",
    "manual_handoff_round": True,
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
    "git_commit_executed": False,
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


def _git_output(args: list[str]) -> str:
    proc = subprocess.run(["git", *args], capture_output=True, text=True, check=False, cwd=ROOT)
    return (proc.stdout if proc.returncode == 0 else proc.stdout + proc.stderr).strip()


def load_previous_evidence_summary(policy: dict[str, Any] | None = None) -> dict[str, Any]:
    _ = create_policy(policy)
    gap = _load_json(GAP_JSON_PATH)
    prep = _load_json(PREP_JSON_PATH)
    implementation = _load_json(IMPLEMENTATION_JSON_PATH)
    smoke = _load_json(SMOKE_JSON_PATH)
    live = _load_json(LIVE_PARITY_JSON_PATH)
    return {
        "row_type": "previous_evidence_summary",
        "gap_closure_status": gap["deployment_gap_closure_result"]["decision_status"],
        "patch_path": gap["patch_backup"]["patch_path"],
        "patch_created": gap["patch_backup"]["patch_created"],
        "patch_line_count": gap["patch_backup"]["patch_line_count"],
        "prep_status": prep["deployment_prep_result"]["decision_status"],
        "implementation_status": implementation["decision"]["decision_status"],
        "runtime_smoke_status": smoke["tester_link_send_decision"]["decision_status"],
        "live_parity_status": live["tester_send_decision"]["decision_status"],
        "evidence_loaded": True,
    }


def record_git_baseline(policy: dict[str, Any] | None = None) -> dict[str, Any]:
    _ = create_policy(policy)
    return {
        "row_type": "git_baseline",
        "branch": _git_output(["branch", "--show-current"]),
        "local_head": _git_output(["rev-parse", "HEAD"]),
        "origin_main_head": _git_output(["rev-parse", "origin/main"]),
        "ahead_behind_counts": _git_output(["rev-list", "--left-right", "--count", "HEAD...origin/main"]),
        "origin_main_commits_ahead": _git_output(["log", "--oneline", "HEAD..origin/main"]).splitlines(),
        "ui_core_status": _git_output(["status", "--short", "--", "app/app.py", "app/templates/index.html", "index.html"]).splitlines(),
    }


def finalize_commit_inclusion_plan(policy: dict[str, Any] | None = None) -> dict[str, Any]:
    _ = create_policy(policy)
    required_present = [path for path in REQUIRED_INCLUDE_FILES if (ROOT / path).exists()]
    optional_present = [path for path in OPTIONAL_INCLUDE_FILES if (ROOT / path).exists()]
    missing_required = [path for path in REQUIRED_INCLUDE_FILES if not (ROOT / path).exists()]
    return {
        "row_type": "commit_inclusion_plan",
        "required_include_files": required_present,
        "optional_include_files": optional_present,
        "missing_required_files": missing_required,
        "commit_scope_clear": not missing_required,
    }


def finalize_commit_exclusion_plan(policy: dict[str, Any] | None = None) -> dict[str, Any]:
    _ = create_policy(policy)
    return {
        "row_type": "commit_exclusion_plan",
        "exclude_files_or_patterns": list(EXCLUDE_FILES),
        "exclude_unrelated_untracked_files": True,
        "exclude_private_and_secret_files": True,
    }


def check_private_secret_risk(policy: dict[str, Any] | None = None) -> dict[str, Any]:
    _ = create_policy(policy)
    include_files = REQUIRED_INCLUDE_FILES + OPTIONAL_INCLUDE_FILES
    risky = [
        path for path in include_files
        if path.startswith("data/private/")
        or path.startswith(".env")
        or "secret" in path.lower()
        or "token" in path.lower()
        or "provider" in path.lower() and "beta_ui" not in path.lower()
    ]
    return {
        "row_type": "private_secret_risk_check",
        "private_secret_risk_level": "low" if not risky else "high",
        "risky_files": risky,
        "risk_summary": "Commit candidate set does not include data/private, env, raw identity, or provider payload files." if not risky else "Commit candidate set includes risky secret-like paths and needs fixup.",
    }


def produce_manual_command_sequence(policy: dict[str, Any] | None = None) -> dict[str, Any]:
    _ = create_policy(policy)
    return {
        "row_type": "manual_command_sequence",
        "recommended_option": "option_b_feature_branch_commit_then_rebase",
        "commands": list(MANUAL_COMMAND_SEQUENCE),
        "commands_executed_in_this_round": False,
    }


def define_recommended_branch_strategy(policy: dict[str, Any] | None = None) -> dict[str, Any]:
    _ = create_policy(policy)
    return {
        "row_type": "recommended_branch_strategy",
        "recommended_branch_name": "beta-ui-redesign-controlled-preview",
        "recommended_strategy": "feature_branch_then_rebase_onto_origin_main",
        "reason": "auto crawl commits가 main을 계속 업데이트하므로 feature branch에서 먼저 UI scope를 고정한 뒤 rebase하는 방식이 가장 명확하다.",
    }


def define_owner_approval_gate(policy: dict[str, Any] | None = None) -> dict[str, Any]:
    _ = create_policy(policy)
    return {
        "row_type": "owner_approval_gate",
        "approval_required_before_git_commit": True,
        "approval_required_before_git_push": True,
        "approval_required_before_vercel_deploy": True,
        "approval_checkpoints": [
            "patch backup 존재 확인",
            "commit include/exclude 범위 최종 확인",
            "tests + golden 재통과 확인",
            "branch/deploy strategy 선택 확인",
        ],
    }


def define_deploy_strategy_options(policy: dict[str, Any] | None = None) -> dict[str, Any]:
    _ = create_policy(policy)
    return {
        "row_type": "deploy_strategy_options",
        "options": DEPLOY_STRATEGY_OPTIONS,
        "recommended_primary_option": "deploy_strategy_pr_merge",
        "recommended_secondary_option": "deploy_strategy_preview_then_promote",
    }


def define_post_deploy_smoke_checklist(policy: dict[str, Any] | None = None) -> dict[str, Any]:
    _ = create_policy(policy)
    return {
        "row_type": "post_deploy_smoke_checklist",
        "items": list(POST_DEPLOY_SMOKE_CHECKLIST),
        "item_count": len(POST_DEPLOY_SMOKE_CHECKLIST),
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
        "git_commit_executed": merged["git_commit_executed"],
        "destructive_git_operation_executed": merged["destructive_git_operation_executed"],
        "tester_link_send_allowed": merged["tester_link_send_allowed"],
    }


def determine_result(
    evidence: dict[str, Any],
    inclusion: dict[str, Any],
    private_secret: dict[str, Any],
    guard: dict[str, Any],
    policy: dict[str, Any] | None = None,
) -> dict[str, Any]:
    _ = create_policy(policy)
    if private_secret["private_secret_risk_level"] == "high":
        decision = "beta_ui_manual_commit_push_deploy_handoff_hold_private_or_secret_risk"
    elif not inclusion["commit_scope_clear"]:
        decision = "beta_ui_manual_commit_push_deploy_handoff_hold_commit_scope_unclear"
    elif not evidence["patch_created"]:
        decision = "beta_ui_manual_commit_push_deploy_handoff_hold_command_risk"
    else:
        decision = "beta_ui_manual_commit_push_deploy_handoff_ready_for_owner_approved_execution"
    return {
        "row_type": "manual_handoff_result",
        "decision_status": decision,
        "tester_link_send_allowed": guard["tester_link_send_allowed"],
        "next_execution_round": "P3-BETA-UI-OWNER-APPROVED-COMMIT-PUSH-DEPLOY-EXECUTION" if decision == "beta_ui_manual_commit_push_deploy_handoff_ready_for_owner_approved_execution" else "P3-BETA-UI-MANUAL-COMMIT-PUSH-DEPLOY-HANDOFF-FIXUP",
    }


def build_scenarios(results: dict[str, Any]) -> list[dict[str, Any]]:
    scenarios = [
        ("A", "deployment gap closure evidence loaded", results["previous_evidence_summary"]["evidence_loaded"]),
        ("B", "patch backup evidence loaded", results["previous_evidence_summary"]["patch_created"]),
        ("C", "commit inclusion plan finalized", results["commit_inclusion_plan"]["commit_scope_clear"]),
        ("D", "commit exclusion plan finalized", bool(results["commit_exclusion_plan"]["exclude_files_or_patterns"])),
        ("E", "private/secret risk checked", results["private_secret_risk_check"]["private_secret_risk_level"] in {"low", "high"}),
        ("F", "manual command sequence produced", len(results["manual_command_sequence"]["commands"]) > 10),
        ("G", "owner approval gate defined", results["owner_approval_gate"]["approval_required_before_git_commit"]),
        ("H", "deploy strategy options defined", len(results["deploy_strategy_options"]["options"]) == 3),
        ("I", "post-deploy smoke checklist produced", results["post_deploy_smoke_checklist"]["item_count"] >= 20),
        ("J", "no git commit executed", not results["production_public_access_guard"]["git_commit_executed"]),
        ("K", "no git push executed", not results["production_public_access_guard"]["git_push_executed"]),
        ("L", "no Vercel deploy executed", not results["production_public_access_guard"]["deployment_executed"]),
        ("M", "production/public/access guard remains false", not results["production_public_access_guard"]["production_launch_go"] and not results["production_public_access_guard"]["public_unrestricted_access_enabled"] and not results["production_public_access_guard"]["external_tester_access_enabled"]),
        ("N", "tester link send remains false", not results["manual_handoff_result"]["tester_link_send_allowed"]),
        ("O", "next execution round defined", bool(results["manual_handoff_result"]["next_execution_round"])),
    ]
    return [
        {"row_type": "scenario_validation", "scenario_id": sid, "scenario": name, "status": "passed" if passed else "failed"}
        for sid, name, passed in scenarios
    ]


def build_report(results: dict[str, Any], exported: dict[str, Any]) -> str:
    prev = results["previous_evidence_summary"]
    baseline = results["git_baseline"]
    inclusion = results["commit_inclusion_plan"]
    exclusion = results["commit_exclusion_plan"]
    private = results["private_secret_risk_check"]
    commands = results["manual_command_sequence"]
    branch = results["recommended_branch_strategy"]
    owner = results["owner_approval_gate"]
    deploy = results["deploy_strategy_options"]
    smoke = results["post_deploy_smoke_checklist"]
    guard = results["production_public_access_guard"]
    decision = results["manual_handoff_result"]
    scenarios = results["scenario_rows"]
    return "\n".join([
        "# P3-BETA-UI-MANUAL-COMMIT-PUSH-AND-DEPLOY-HANDOFF",
        "",
        "## 1. 작업명",
        "- P3-BETA-UI-MANUAL-COMMIT-PUSH-AND-DEPLOY-HANDOFF",
        "",
        "## 2. 현재 판정",
        f"- decision_status = {decision['decision_status']}",
        "",
        "## 3. 목적",
        "- 새 UI 변경을 실제 main/deploy 라인에 올리기 위한 수동 실행 절차를 owner가 그대로 따라갈 수 있게 정리한다.",
        "",
        "## 4. previous evidence summary",
        f"- gap_closure_status = {prev['gap_closure_status']}",
        f"- patch_path = {prev['patch_path']}",
        f"- patch_created = {prev['patch_created']}",
        f"- patch_line_count = {prev['patch_line_count']}",
        f"- prep_status = {prev['prep_status']}",
        "",
        "## 5. commit inclusion plan",
        f"- required_include_files = {inclusion['required_include_files']}",
        f"- optional_include_files = {inclusion['optional_include_files']}",
        f"- missing_required_files = {inclusion['missing_required_files']}",
        "",
        "## 6. commit exclusion plan",
        f"- exclude_files_or_patterns = {exclusion['exclude_files_or_patterns']}",
        "",
        "## 7. private/secret risk check",
        f"- private_secret_risk_level = {private['private_secret_risk_level']}",
        f"- risky_files = {private['risky_files']}",
        f"- risk_summary = {private['risk_summary']}",
        "",
        "## 8. manual command sequence",
        *[f"- {cmd}" for cmd in commands["commands"]],
        "",
        "## 9. recommended branch strategy",
        f"- recommended_branch_name = {branch['recommended_branch_name']}",
        f"- recommended_strategy = {branch['recommended_strategy']}",
        f"- reason = {branch['reason']}",
        "",
        "## 10. owner approval gate",
        f"- approval_required_before_git_commit = {owner['approval_required_before_git_commit']}",
        f"- approval_required_before_git_push = {owner['approval_required_before_git_push']}",
        f"- approval_required_before_vercel_deploy = {owner['approval_required_before_vercel_deploy']}",
        *[f"- {item}" for item in owner["approval_checkpoints"]],
        "",
        "## 11. deploy strategy options",
        *[f"- {opt['label']} | recommended={opt['recommended']} | {opt['reason']}" for opt in deploy["options"]],
        "",
        "## 12. post-deploy smoke checklist",
        *[f"- {item}" for item in smoke["items"]],
        "",
        "## 13. production/public/access guard",
        f"- production_launch_go = {guard['production_launch_go']}",
        f"- public_unrestricted_access_enabled = {guard['public_unrestricted_access_enabled']}",
        f"- external_tester_access_enabled = {guard['external_tester_access_enabled']}",
        f"- git_commit_executed = {guard['git_commit_executed']}",
        f"- git_push_executed = {guard['git_push_executed']}",
        f"- deployment_executed = {guard['deployment_executed']}",
        "",
        "## 14. 수정 파일 목록",
        *[f"- {path}" for path in exported["artifact_json"]["modified_files"]],
        "",
        "## 15. 테스트 결과",
        f"- scenario_validation = {sum(1 for row in scenarios if row['status'] == 'passed')}/{len(scenarios)} passed",
        "",
        "## 16. tester link send 가능 여부",
        f"- tester_link_send_allowed = {decision['tester_link_send_allowed']}",
        "",
        "## 17. 다음 backlog 후보",
        f"- {decision['next_execution_round']}",
        "",
        "## Git Baseline",
        f"- branch = {baseline['branch']}",
        f"- local_head = {baseline['local_head']}",
        f"- origin_main_head = {baseline['origin_main_head']}",
        f"- ahead_behind_counts = {baseline['ahead_behind_counts']}",
        f"- origin_main_commits_ahead = {baseline['origin_main_commits_ahead']}",
        f"- ui_core_status = {baseline['ui_core_status']}",
        "",
    ])


def export_results(results: dict[str, Any]) -> dict[str, Any]:
    jsonl_rows: list[dict[str, Any]] = [
        {"row_type": "beta_ui_manual_commit_push_and_deploy_handoff_policy", **results["policy"]},
        results["previous_evidence_summary"],
        results["git_baseline"],
        results["commit_inclusion_plan"],
        results["commit_exclusion_plan"],
        results["private_secret_risk_check"],
        results["manual_command_sequence"],
        results["recommended_branch_strategy"],
        results["owner_approval_gate"],
        results["deploy_strategy_options"],
        results["post_deploy_smoke_checklist"],
        results["production_public_access_guard"],
        results["manual_handoff_result"],
        *results["scenario_rows"],
        {"row_type": "progress_report", "limited_external_beta_progress_percent": 88, "current_stage": "beta_ui_manual_commit_push_and_deploy_handoff", "tester_link_send_allowed": False},
        {"row_type": "summary", "decision_status": results["manual_handoff_result"]["decision_status"], "next_execution_round": results["manual_handoff_result"]["next_execution_round"]},
    ]
    artifact_json = {
        "task_name": "P3-BETA-UI-MANUAL-COMMIT-PUSH-AND-DEPLOY-HANDOFF",
        "artifact_version": "p3_beta_ui_manual_commit_push_and_deploy_handoff_v0",
        "schema_version": "beta_ui_manual_commit_push_and_deploy_handoff.v0",
        "generated_at": results["policy"]["generated_at"],
        "policy": results["policy"],
        "previous_evidence_summary": results["previous_evidence_summary"],
        "git_baseline": results["git_baseline"],
        "commit_inclusion_plan": results["commit_inclusion_plan"],
        "commit_exclusion_plan": results["commit_exclusion_plan"],
        "private_secret_risk_check": results["private_secret_risk_check"],
        "manual_command_sequence": results["manual_command_sequence"],
        "recommended_branch_strategy": results["recommended_branch_strategy"],
        "owner_approval_gate": results["owner_approval_gate"],
        "deploy_strategy_options": results["deploy_strategy_options"],
        "post_deploy_smoke_checklist": results["post_deploy_smoke_checklist"],
        "production_public_access_guard": results["production_public_access_guard"],
        "manual_handoff_result": results["manual_handoff_result"],
        "scenario_validation": results["scenario_rows"],
        "modified_files": [
            "scripts/run_p3_beta_ui_manual_commit_push_and_deploy_handoff.py",
            "tests/test_beta_ui_manual_commit_push_and_deploy_handoff.py",
            "data/admin/p3_beta_ui_manual_commit_push_and_deploy_handoff_v0.md",
            "data/admin/p3_beta_ui_manual_commit_push_and_deploy_handoff_v0.jsonl",
            "data/admin/beta_ui_manual_commit_push_and_deploy_handoff_v0.json",
        ],
    }
    return {"jsonl_rows": jsonl_rows, "artifact_json": artifact_json}


def process(policy: dict[str, Any] | None = None) -> dict[str, Any]:
    active_policy = create_policy(policy)
    results: dict[str, Any] = {"policy": active_policy}
    results["previous_evidence_summary"] = load_previous_evidence_summary(active_policy)
    results["git_baseline"] = record_git_baseline(active_policy)
    results["commit_inclusion_plan"] = finalize_commit_inclusion_plan(active_policy)
    results["commit_exclusion_plan"] = finalize_commit_exclusion_plan(active_policy)
    results["private_secret_risk_check"] = check_private_secret_risk(active_policy)
    results["manual_command_sequence"] = produce_manual_command_sequence(active_policy)
    results["recommended_branch_strategy"] = define_recommended_branch_strategy(active_policy)
    results["owner_approval_gate"] = define_owner_approval_gate(active_policy)
    results["deploy_strategy_options"] = define_deploy_strategy_options(active_policy)
    results["post_deploy_smoke_checklist"] = define_post_deploy_smoke_checklist(active_policy)
    results["production_public_access_guard"] = evaluate_guard(active_policy)
    results["manual_handoff_result"] = determine_result(
        results["previous_evidence_summary"],
        results["commit_inclusion_plan"],
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
        "decision_status": results["manual_handoff_result"]["decision_status"],
        "recommended_strategy": results["recommended_branch_strategy"]["recommended_strategy"],
        "tester_link_send_allowed": results["manual_handoff_result"]["tester_link_send_allowed"],
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
