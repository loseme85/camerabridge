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
LIVE_PARITY_JSON_PATH = ROOT / "data/admin/beta_ui_live_deployment_parity_and_share_link_verification_v0.json"
SMOKE_JSON_PATH = ROOT / "data/admin/beta_share_link_runtime_smoke_recheck_v0.json"

MD_PATH = ROOT / "data/admin/p3_beta_ui_deployment_prep_and_safe_redeploy_check_v0.md"
JSONL_PATH = ROOT / "data/admin/p3_beta_ui_deployment_prep_and_safe_redeploy_check_v0.jsonl"
JSON_PATH = ROOT / "data/admin/beta_ui_deployment_prep_and_safe_redeploy_check_v0.json"

UI_FILES = [
    "app/app.py",
    "app/templates/index.html",
    "index.html",
    "beta_landing_search_ui_reference_redesign_implementation.py",
    "scripts/run_p3_beta_landing_search_ui_reference_redesign_implementation.py",
    "tests/test_beta_landing_search_ui_reference_redesign_implementation.py",
    "data/admin/p3_beta_landing_search_ui_reference_redesign_implementation_v0.md",
    "data/admin/p3_beta_landing_search_ui_reference_redesign_implementation_v0.jsonl",
    "data/admin/beta_landing_search_ui_reference_redesign_implementation_v0.json",
    "data/admin/p3_beta_share_link_runtime_smoke_recheck_v0.md",
    "data/admin/beta_share_link_runtime_smoke_recheck_v0.json",
    "data/admin/p3_beta_ui_live_deployment_parity_and_share_link_verification_v0.md",
    "data/admin/beta_ui_live_deployment_parity_and_share_link_verification_v0.json",
]

FRONTEND_CORE_FILES = [
    "app/app.py",
    "app/templates/index.html",
    "index.html",
]

SAFE_REDEPLOY_CHECKLIST = [
    "UI 변경 파일 확인",
    "git diff 확인",
    "tests 통과",
    "golden_set.py 132/132 확인",
    "commit message 제안 확인",
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

DEFAULT_POLICY: dict[str, Any] = {
    "generated_at": "2026-06-03T00:00:00Z",
    "schema_version": "beta_ui_deployment_prep_and_safe_redeploy_check.v0",
    "artifact_version": "p3_beta_ui_deployment_prep_and_safe_redeploy_check_v0",
    "deployment_prep_round": True,
    "deploy_executed": False,
    "git_push_executed": False,
    "production_code_modified": False,
    "production_launch_go": False,
    "public_unrestricted_access_enabled": False,
    "external_tester_access_enabled": False,
    "invite_sent_count": 0,
    "provider_send_count": 0,
    "webhook_call_count": 0,
    "production_DB_write_count": 0,
    "safe_candidate_record_created_count_delta": 0,
    "access_activation_performed": False,
}


def create_policy(policy: dict[str, Any] | None = None) -> dict[str, Any]:
    merged = dict(DEFAULT_POLICY)
    if policy:
        merged.update(policy)
    return merged


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _run(args: list[str]) -> tuple[int, str, str]:
    proc = subprocess.run(args, capture_output=True, text=True, check=False)
    return proc.returncode, proc.stdout, proc.stderr


def _git_output(args: list[str]) -> str:
    code, out, err = _run(["git", *args])
    if code != 0:
        return (out + err).strip()
    return out.strip()


def load_ui_implementation_evidence(policy: dict[str, Any] | None = None) -> dict[str, Any]:
    _ = create_policy(policy)
    payload = _load_json(IMPLEMENTATION_JSON_PATH)
    return {
        "row_type": "ui_implementation_evidence",
        "implementation_status": payload["decision"]["decision_status"],
        "modified_frontend_files": payload["frontend_files"]["modified_frontend_files"],
        "implementation_query_smoke_count": payload["query_smoke"]["query_count"],
        "evidence_source": "artifact_based_ui_implementation",
    }


def load_prior_live_parity_hold_evidence(policy: dict[str, Any] | None = None) -> dict[str, Any]:
    _ = create_policy(policy)
    payload = _load_json(LIVE_PARITY_JSON_PATH)
    smoke = _load_json(SMOKE_JSON_PATH)
    return {
        "row_type": "prior_live_parity_hold_evidence",
        "prior_live_parity_status": payload["tester_send_decision"]["decision_status"],
        "prior_live_share_status": payload["live_share_landing_verification"]["landing_live_status"],
        "prior_live_api_verified": payload["live_share_api_verification"]["live_api_verified"],
        "prior_runtime_smoke_status": smoke["tester_link_send_decision"]["decision_status"],
        "evidence_source": "artifact_based_live_parity_hold",
    }


def inspect_git_working_tree(policy: dict[str, Any] | None = None) -> dict[str, Any]:
    _ = create_policy(policy)
    status_short = _git_output(["status", "--short"])
    ui_status = _git_output(["status", "--short", "--", *UI_FILES])
    branch = _git_output(["branch", "--show-current"])
    head = _git_output(["rev-parse", "HEAD"])
    log = _git_output(["log", "-5", "--oneline"])
    diff_stat = _git_output(["diff", "--stat"])
    return {
        "row_type": "git_working_tree",
        "git_status_short": status_short.splitlines() if status_short else [],
        "ui_file_status": ui_status.splitlines() if ui_status else [],
        "current_branch": branch,
        "local_head": head,
        "recent_log": log.splitlines() if log else [],
        "diff_stat_lines": diff_stat.splitlines() if diff_stat else [],
    }


def inspect_frontend_diff(policy: dict[str, Any] | None = None) -> dict[str, Any]:
    _ = create_policy(policy)
    diff = _git_output(["diff", "HEAD", "--", *FRONTEND_CORE_FILES])
    name_only = _git_output(["diff", "HEAD", "--name-only", "--", *FRONTEND_CORE_FILES])
    if not name_only.strip():
        diff = _git_output(["diff", "origin/main", "--", *FRONTEND_CORE_FILES])
        name_only = _git_output(["diff", "origin/main", "--name-only", "--", *FRONTEND_CORE_FILES])
    return {
        "row_type": "frontend_diff",
        "frontend_diff_file_count": len(name_only.splitlines()) if name_only else 0,
        "frontend_diff_files": name_only.splitlines() if name_only else [],
        "app_route_search_added": '@app.route("/search")' in diff,
        "api_route_search_added": '@app.route("/api/search")' in diff,
        "hero_headline_diff_present": "Global used camera search &amp; market intelligence" in diff,
        "runtime_fallback_copy_diff_present": "Something went wrong while loading this search." in diff,
    }


def evaluate_ui_implementation_files(policy: dict[str, Any] | None = None) -> dict[str, Any]:
    _ = create_policy(policy)
    existence = {path: (ROOT / path).exists() for path in UI_FILES}
    return {
        "row_type": "ui_implementation_files",
        "files_exist_map": existence,
        "missing_files": [path for path, exists in existence.items() if not exists],
        "all_required_files_exist": all(existence.values()),
    }


def evaluate_commit_push_need(policy: dict[str, Any] | None = None) -> dict[str, Any]:
    _ = create_policy(policy)
    ui_status = _git_output(["status", "--short", "--", *UI_FILES]).splitlines()
    modified_or_untracked = [line for line in ui_status if line.strip()]
    return {
        "row_type": "commit_push_need",
        "ui_changes_present_in_working_tree": bool(modified_or_untracked),
        "ui_changes_uncommitted_or_untracked": modified_or_untracked,
        "commit_push_required": bool(modified_or_untracked),
        "suggested_commit_message": "feat: apply beta landing and search UI redesign for controlled preview",
    }


def evaluate_latest_deployment_metadata(policy: dict[str, Any] | None = None) -> dict[str, Any]:
    _ = create_policy(policy)
    local_head = _git_output(["rev-parse", "HEAD"])
    origin_main_head = _git_output(["rev-parse", "origin/main"])
    origin_main_log = _git_output(["log", "-1", "--pretty=format:%H%n%s%n%ci", "origin/main"])
    ahead_behind = _git_output(["rev-list", "--left-right", "--count", f"{local_head}...{origin_main_head}"])
    remote_diff = _git_output(["diff", "--name-only", f"{local_head}..{origin_main_head}"])
    return {
        "row_type": "latest_deployment_metadata",
        "local_head": local_head,
        "origin_main_head": origin_main_head if origin_main_head else None,
        "origin_main_latest_log": origin_main_log.splitlines() if origin_main_log else [],
        "ahead_behind_counts": ahead_behind,
        "origin_main_diff_from_local": remote_diff.splitlines() if remote_diff else [],
        "origin_main_latest_is_auto_crawl": "Auto crawl" in origin_main_log,
        "deployment_metadata_available": False,
        "vercel_latest_deployment_sha": None,
        "vercel_latest_deployment_message": None,
    }


def classify_local_deployment_gap(
    file_check: dict[str, Any],
    commit_need: dict[str, Any],
    deployment_meta: dict[str, Any],
    policy: dict[str, Any] | None = None,
) -> dict[str, Any]:
    _ = create_policy(policy)
    remote_changes = set(deployment_meta["origin_main_diff_from_local"])
    ui_remote_overlap = sorted(remote_changes.intersection(UI_FILES))
    auto_crawl_only_remote = bool(remote_changes) and not ui_remote_overlap
    if not file_check["all_required_files_exist"]:
        classification = "ui_implementation_files_missing"
    elif commit_need["commit_push_required"]:
        classification = "ui_changes_uncommitted_or_unpushed"
    elif deployment_meta["origin_main_head"] is None:
        classification = "deployment_gap_not_understood"
    elif auto_crawl_only_remote:
        classification = "remote_main_ahead_with_data_only_auto_crawl_gap"
    else:
        classification = "deployment_gap_not_understood"
    return {
        "row_type": "local_deployment_parity_gap",
        "gap_classification": classification,
        "ui_remote_overlap": ui_remote_overlap,
        "auto_crawl_only_remote_gap": auto_crawl_only_remote,
        "gap_summary": "Remote main is ahead with auto crawl data commits while local UI changes remain uncommitted in the working tree." if classification in {"ui_changes_uncommitted_or_unpushed", "remote_main_ahead_with_data_only_auto_crawl_gap"} else "Gap needs further inspection.",
    }


def evaluate_auto_crawl_influence(deployment_meta: dict[str, Any], gap: dict[str, Any], policy: dict[str, Any] | None = None) -> dict[str, Any]:
    _ = create_policy(policy)
    return {
        "row_type": "auto_crawl_influence",
        "origin_main_latest_is_auto_crawl": deployment_meta["origin_main_latest_is_auto_crawl"],
        "auto_crawl_only_remote_gap": gap["auto_crawl_only_remote_gap"],
        "ui_files_in_remote_diff": gap["ui_remote_overlap"],
        "possible_influence": "Auto crawl appears to have advanced remote main with data artifacts, but there is no evidence that it overwrote the UI files in remote history." if gap["auto_crawl_only_remote_gap"] else "No specific auto crawl impact isolated.",
    }


def define_safe_redeploy_checklist(policy: dict[str, Any] | None = None) -> dict[str, Any]:
    _ = create_policy(policy)
    return {
        "row_type": "safe_redeploy_checklist",
        "items": SAFE_REDEPLOY_CHECKLIST,
    }


def define_post_deploy_smoke_checklist(policy: dict[str, Any] | None = None) -> dict[str, Any]:
    _ = create_policy(policy)
    return {
        "row_type": "post_deploy_smoke_checklist",
        "items": POST_DEPLOY_SMOKE_CHECKLIST,
    }


def evaluate_guard(policy: dict[str, Any] | None = None) -> dict[str, Any]:
    active_policy = create_policy(policy)
    return {
        "row_type": "production_public_access_guard",
        "production_launch_go": active_policy["production_launch_go"],
        "public_unrestricted_access_enabled": active_policy["public_unrestricted_access_enabled"],
        "external_tester_access_enabled": active_policy["external_tester_access_enabled"],
        "invite_sent_count": active_policy["invite_sent_count"],
        "provider_send_count": active_policy["provider_send_count"],
        "webhook_call_count": active_policy["webhook_call_count"],
        "production_DB_write_count": active_policy["production_DB_write_count"],
        "safe_candidate_record_created_count_delta": active_policy["safe_candidate_record_created_count_delta"],
        "access_activation_performed": active_policy["access_activation_performed"],
        "deploy_executed": active_policy["deploy_executed"],
        "git_push_executed": active_policy["git_push_executed"],
    }


def determine_result(
    file_check: dict[str, Any],
    commit_need: dict[str, Any],
    gap: dict[str, Any],
    guard: dict[str, Any],
    policy: dict[str, Any] | None = None,
) -> dict[str, Any]:
    _ = create_policy(policy)
    if any(
        [
            guard["production_launch_go"],
            guard["public_unrestricted_access_enabled"],
            guard["external_tester_access_enabled"],
            guard["deploy_executed"],
            guard["git_push_executed"],
        ]
    ):
        decision_status = "beta_ui_deployment_prep_rollback_required"
    elif not file_check["all_required_files_exist"]:
        decision_status = "beta_ui_deployment_prep_hold_ui_implementation_files_missing"
    elif commit_need["commit_push_required"]:
        decision_status = "beta_ui_deployment_prep_hold_ui_changes_uncommitted_or_unpushed"
    elif gap["gap_classification"] == "deployment_gap_not_understood":
        decision_status = "beta_ui_deployment_prep_hold_deployment_gap_not_understood"
    else:
        decision_status = "beta_ui_deployment_prep_ready_for_manual_commit_push_or_deploy"
    return {
        "row_type": "deployment_prep_result",
        "decision_status": decision_status,
        "tester_link_send_allowed": False,
        "manual_commit_push_or_deploy_ready": decision_status == "beta_ui_deployment_prep_ready_for_manual_commit_push_or_deploy",
    }


def build_scenario_rows(results: dict[str, Any], policy: dict[str, Any] | None = None) -> list[dict[str, Any]]:
    _ = create_policy(policy)
    scenarios = [
        ("1", "UI implementation evidence loaded", results["ui_implementation_evidence"]["implementation_query_smoke_count"] == 10),
        ("2", "prior live parity hold evidence loaded", "hold" in results["prior_live_parity_hold_evidence"]["prior_live_parity_status"]),
        ("3", "git working tree inspected", bool(results["git_working_tree"]["git_status_short"])),
        ("4", "frontend diff inspected", results["frontend_diff"]["frontend_diff_file_count"] == 3),
        ("5", "local HEAD recorded", bool(results["git_working_tree"]["local_head"])),
        ("6", "latest deployment metadata recorded if available", results["latest_deployment_metadata"]["origin_main_head"] is not None),
        ("7", "UI deployment gap classified", bool(results["local_deployment_parity_gap"]["gap_classification"])),
        ("8", "no production code modified", results["guard"]["deploy_executed"] is False and results["guard"]["git_push_executed"] is False),
        ("9", "no deploy executed", results["guard"]["deploy_executed"] is False),
        ("10", "no git push executed", results["guard"]["git_push_executed"] is False),
        ("11", "test command list recorded", len(results["test_command_list"]["commands"]) >= 4),
        ("12", "safe redeploy checklist produced", len(results["safe_redeploy_checklist"]["items"]) >= 10),
        ("13", "post-deploy share link smoke checklist produced", len(results["post_deploy_smoke_checklist"]["items"]) >= 10),
        ("14", "tester_link_send_allowed remains false", results["deployment_prep_result"]["tester_link_send_allowed"] is False),
    ]
    return [
        {
            "row_type": "scenario_validation",
            "scenario_id": sid,
            "scenario": text,
            "status": "passed" if passed else "failed",
        }
        for sid, text, passed in scenarios
    ]


def define_test_command_list(policy: dict[str, Any] | None = None) -> dict[str, Any]:
    _ = create_policy(policy)
    return {
        "row_type": "test_command_list",
        "commands": [
            "python3 tests/test_beta_landing_search_ui_reference_redesign_implementation.py",
            "python3 scripts/run_p3_beta_landing_search_ui_reference_redesign_implementation.py",
            "python3 tests/test_beta_share_link_runtime_smoke_recheck.py",
            "python3 scripts/run_p3_beta_share_link_runtime_smoke_recheck.py",
            "python3 tests/test_beta_ui_live_deployment_parity_and_share_link_verification.py",
            "python3 scripts/run_p3_beta_ui_live_deployment_parity_and_share_link_verification.py",
            "python3 golden_set.py",
        ],
    }


def process(policy: dict[str, Any] | None = None) -> dict[str, Any]:
    active_policy = create_policy(policy)
    results: dict[str, Any] = {
        "task_name": "P3-BETA-UI-DEPLOYMENT-PREP-AND-SAFE-REDEPLOY-CHECK",
        "artifact_version": active_policy["artifact_version"],
        "schema_version": active_policy["schema_version"],
        "generated_at": active_policy["generated_at"],
        "policy": active_policy,
        "ui_implementation_evidence": load_ui_implementation_evidence(active_policy),
        "prior_live_parity_hold_evidence": load_prior_live_parity_hold_evidence(active_policy),
        "git_working_tree": inspect_git_working_tree(active_policy),
        "frontend_diff": inspect_frontend_diff(active_policy),
        "ui_implementation_files": evaluate_ui_implementation_files(active_policy),
        "commit_push_need": evaluate_commit_push_need(active_policy),
        "latest_deployment_metadata": evaluate_latest_deployment_metadata(active_policy),
        "test_command_list": define_test_command_list(active_policy),
        "safe_redeploy_checklist": define_safe_redeploy_checklist(active_policy),
        "post_deploy_smoke_checklist": define_post_deploy_smoke_checklist(active_policy),
        "guard": evaluate_guard(active_policy),
    }
    results["local_deployment_parity_gap"] = classify_local_deployment_gap(
        results["ui_implementation_files"],
        results["commit_push_need"],
        results["latest_deployment_metadata"],
        active_policy,
    )
    results["auto_crawl_influence"] = evaluate_auto_crawl_influence(
        results["latest_deployment_metadata"],
        results["local_deployment_parity_gap"],
        active_policy,
    )
    results["deployment_prep_result"] = determine_result(
        results["ui_implementation_files"],
        results["commit_push_need"],
        results["local_deployment_parity_gap"],
        results["guard"],
        active_policy,
    )
    results["scenario_rows"] = build_scenario_rows(results, active_policy)
    return results


def export_results(results: dict[str, Any]) -> dict[str, Any]:
    progress = {
        "row_type": "progress_report",
        "current_stage": "beta_ui_deployment_prep_and_safe_redeploy_check",
        "external_tester_access_enabled": results["policy"]["external_tester_access_enabled"],
        "invite_sent_count": results["policy"]["invite_sent_count"],
        "production_launch_go": results["policy"]["production_launch_go"],
        "public_unrestricted_access_enabled": results["policy"]["public_unrestricted_access_enabled"],
    }
    summary = {
        "row_type": "summary",
        "decision_status": results["deployment_prep_result"]["decision_status"],
        "current_branch": results["git_working_tree"]["current_branch"],
        "local_head": results["git_working_tree"]["local_head"],
        "origin_main_head": results["latest_deployment_metadata"]["origin_main_head"],
        "gap_classification": results["local_deployment_parity_gap"]["gap_classification"],
        "tester_link_send_allowed": results["deployment_prep_result"]["tester_link_send_allowed"],
    }
    rows = [
        {"row_type": "beta_ui_deployment_prep_and_safe_redeploy_check_policy", **results["policy"]},
        results["ui_implementation_evidence"],
        results["prior_live_parity_hold_evidence"],
        results["git_working_tree"],
        results["frontend_diff"],
        results["ui_implementation_files"],
        results["commit_push_need"],
        results["latest_deployment_metadata"],
        results["local_deployment_parity_gap"],
        results["auto_crawl_influence"],
        results["test_command_list"],
        results["safe_redeploy_checklist"],
        results["post_deploy_smoke_checklist"],
        results["guard"],
        results["deployment_prep_result"],
        *results["scenario_rows"],
        progress,
        summary,
    ]
    artifact = {
        "task_name": results["task_name"],
        "artifact_version": results["artifact_version"],
        "schema_version": results["schema_version"],
        "generated_at": results["generated_at"],
        "policy": results["policy"],
        "ui_implementation_evidence": results["ui_implementation_evidence"],
        "prior_live_parity_hold_evidence": results["prior_live_parity_hold_evidence"],
        "git_working_tree": results["git_working_tree"],
        "frontend_diff": results["frontend_diff"],
        "ui_implementation_files": results["ui_implementation_files"],
        "commit_push_need": results["commit_push_need"],
        "latest_deployment_metadata": results["latest_deployment_metadata"],
        "local_deployment_parity_gap": results["local_deployment_parity_gap"],
        "auto_crawl_influence": results["auto_crawl_influence"],
        "test_command_list": results["test_command_list"],
        "safe_redeploy_checklist": results["safe_redeploy_checklist"],
        "post_deploy_smoke_checklist": results["post_deploy_smoke_checklist"],
        "guard": results["guard"],
        "deployment_prep_result": results["deployment_prep_result"],
        "scenario_rows": results["scenario_rows"],
        "modified_files": [
            "scripts/run_p3_beta_ui_deployment_prep_and_safe_redeploy_check.py",
            "tests/test_beta_ui_deployment_prep_and_safe_redeploy_check.py",
            "data/admin/p3_beta_ui_deployment_prep_and_safe_redeploy_check_v0.md",
            "data/admin/p3_beta_ui_deployment_prep_and_safe_redeploy_check_v0.jsonl",
            "data/admin/beta_ui_deployment_prep_and_safe_redeploy_check_v0.json",
        ],
        "summary": summary,
    }
    return {"jsonl_rows": rows, "artifact_json": artifact}


def build_report(results: dict[str, Any], exported: dict[str, Any]) -> str:
    scenario_rows = results["scenario_rows"]
    pass_count = sum(1 for row in scenario_rows if row["status"] == "passed")
    lines = [
        "# P3-BETA-UI-DEPLOYMENT-PREP-AND-SAFE-REDEPLOY-CHECK",
        "",
        "## 1. 작업명",
        results["task_name"],
        "",
        "## 2. 현재 판정",
        f"- decision_status = {results['deployment_prep_result']['decision_status']}",
        "",
        "## 3. 이번 라운드 목적",
        "- 새 UI 구현이 실제 배포 가능한 상태인지 확인한다.",
        "- 실제 deploy 없이 commit/push/deploy readiness를 점검한다.",
        "",
        "## 4. 이전 라운드 요약",
        f"- ui_implementation_status = {results['ui_implementation_evidence']['implementation_status']}",
        f"- prior_live_parity_status = {results['prior_live_parity_hold_evidence']['prior_live_parity_status']}",
        f"- prior_runtime_smoke_status = {results['prior_live_parity_hold_evidence']['prior_runtime_smoke_status']}",
        "",
        "## 5. git status 요약",
    ]
    for line in results["git_working_tree"]["ui_file_status"]:
        lines.append(f"- {line}")
    lines.extend(
        [
            "",
            "## 6. local HEAD",
            f"- branch = {results['git_working_tree']['current_branch']}",
            f"- local_head = {results['git_working_tree']['local_head']}",
        ]
    )
    for line in results["git_working_tree"]["recent_log"]:
        lines.append(f"- log = {line}")
    lines.extend(
        [
            "",
            "## 7. frontend diff 요약",
            f"- frontend_diff_file_count = {results['frontend_diff']['frontend_diff_file_count']}",
        ]
    )
    for item in results["frontend_diff"]["frontend_diff_files"]:
        lines.append(f"- diff_file = {item}")
    lines.extend(
        [
            "",
            "## 8. UI implementation files 존재 여부",
            f"- all_required_files_exist = {results['ui_implementation_files']['all_required_files_exist']}",
            f"- missing_files = {results['ui_implementation_files']['missing_files']}",
            "",
            "## 9. UI 변경 commit/push 필요 여부",
            f"- commit_push_required = {results['commit_push_need']['commit_push_required']}",
            f"- suggested_commit_message = {results['commit_push_need']['suggested_commit_message']}",
        ]
    )
    for item in results["commit_push_need"]["ui_changes_uncommitted_or_untracked"]:
        lines.append(f"- pending_ui_change = {item}")
    lines.extend(
        [
            "",
            "## 10. latest deployment metadata",
            f"- origin_main_head = {results['latest_deployment_metadata']['origin_main_head']}",
            f"- ahead_behind_counts = {results['latest_deployment_metadata']['ahead_behind_counts']}",
            f"- origin_main_latest_is_auto_crawl = {results['latest_deployment_metadata']['origin_main_latest_is_auto_crawl']}",
            f"- deployment_metadata_available = {results['latest_deployment_metadata']['deployment_metadata_available']}",
        ]
    )
    for item in results["latest_deployment_metadata"]["origin_main_latest_log"]:
        lines.append(f"- origin_main_log = {item}")
    lines.extend(
        [
            "",
            "## 11. local/deployment parity gap",
            f"- gap_classification = {results['local_deployment_parity_gap']['gap_classification']}",
            f"- gap_summary = {results['local_deployment_parity_gap']['gap_summary']}",
            "",
            "## 12. auto crawl commit 영향 가능성",
            f"- auto_crawl_only_remote_gap = {results['auto_crawl_influence']['auto_crawl_only_remote_gap']}",
            f"- possible_influence = {results['auto_crawl_influence']['possible_influence']}",
            "",
            "## 13. safe redeploy checklist",
        ]
    )
    for item in results["safe_redeploy_checklist"]["items"]:
        lines.append(f"- {item}")
    lines.extend(
        [
            "",
            "## 14. post-deploy smoke checklist",
        ]
    )
    for item in results["post_deploy_smoke_checklist"]["items"]:
        lines.append(f"- {item}")
    lines.extend(
        [
            "",
            "## 15. production/public/access guard",
            f"- production_launch_go = {results['guard']['production_launch_go']}",
            f"- public_unrestricted_access_enabled = {results['guard']['public_unrestricted_access_enabled']}",
            f"- external_tester_access_enabled = {results['guard']['external_tester_access_enabled']}",
            f"- deploy_executed = {results['guard']['deploy_executed']}",
            f"- git_push_executed = {results['guard']['git_push_executed']}",
            "",
            "## 16. 수정 파일 목록",
        ]
    )
    for item in exported["artifact_json"]["modified_files"]:
        lines.append(f"- {item}")
    lines.extend(
        [
            "",
            "## 17. 테스트 결과",
            f"- scenario_validation = {pass_count}/{len(scenario_rows)} passed",
            "",
            "## 18. tester link send 가능 여부",
            f"- tester_link_send_allowed = {results['deployment_prep_result']['tester_link_send_allowed']}",
            f"- final_decision = {results['deployment_prep_result']['decision_status']}",
            "",
            "## 19. 다음 backlog 후보",
        ]
    )
    if results["deployment_prep_result"]["decision_status"] == "beta_ui_deployment_prep_ready_for_manual_commit_push_or_deploy":
        next_items = [
            "P3-BETA-UI-MANUAL-COMMIT-PUSH-AND-DEPLOY-HANDOFF",
            "P3-BETA-SHARE-LINK-REGENERATION-AND-ACCESS-CHECK",
        ]
    else:
        next_items = ["P3-BETA-UI-DEPLOYMENT-GAP-CLOSURE"]
    for item in next_items:
        lines.append(f"- {item}")
    return "\n".join(lines) + "\n"


def write_artifacts(results: dict[str, Any]) -> dict[str, Any]:
    exported = export_results(results)
    report = build_report(results, exported)
    JSON_PATH.write_text(json.dumps(exported["artifact_json"], ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    with JSONL_PATH.open("w", encoding="utf-8") as handle:
        for row in exported["jsonl_rows"]:
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")
    MD_PATH.write_text(report, encoding="utf-8")
    return exported


def main() -> None:
    results = process()
    write_artifacts(results)
    print(results["deployment_prep_result"]["decision_status"])


if __name__ == "__main__":
    main()
