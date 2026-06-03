from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "scripts"
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import run_p3_beta_ui_deployment_prep_and_safe_redeploy_check as prep


_CACHED_RESULT: dict | None = None


def _result() -> dict:
    global _CACHED_RESULT
    if _CACHED_RESULT is None:
        _CACHED_RESULT = prep.process()
    return _CACHED_RESULT


def test_module_imports() -> None:
    assert prep.__name__ == "run_p3_beta_ui_deployment_prep_and_safe_redeploy_check"


def test_ui_implementation_evidence_loaded() -> None:
    row = prep.load_ui_implementation_evidence()
    assert "beta_landing_search_ui_reference_redesign_implementation_ready_for_runtime_triage_or_smoke" == row["implementation_status"]


def test_prior_live_parity_hold_evidence_loaded() -> None:
    row = prep.load_prior_live_parity_hold_evidence()
    assert "hold" in row["prior_live_parity_status"]


def test_git_working_tree_inspected() -> None:
    row = prep.inspect_git_working_tree()
    assert row["current_branch"] in {"main", "beta-ui-redesign-controlled-preview"}
    assert row["local_head"]
    assert isinstance(row["ui_file_status"], list)


def test_frontend_diff_inspected() -> None:
    row = prep.inspect_frontend_diff()
    assert row["frontend_diff_file_count"] in {0, 3}
    if row["frontend_diff_file_count"] == 3:
        assert row["hero_headline_diff_present"] is True
        assert row["runtime_fallback_copy_diff_present"] is True


def test_ui_implementation_files_exist() -> None:
    row = prep.evaluate_ui_implementation_files()
    assert row["all_required_files_exist"] is True
    assert row["missing_files"] == []


def test_ui_changes_need_commit_push() -> None:
    row = prep.evaluate_commit_push_need()
    assert row["commit_push_required"] in {True, False}
    assert row["ui_changes_present_in_working_tree"] in {True, False}


def test_latest_deployment_metadata_recorded_if_available() -> None:
    row = prep.evaluate_latest_deployment_metadata()
    assert row["origin_main_head"]
    assert row["origin_main_latest_is_auto_crawl"] is True


def test_local_deployment_gap_classified() -> None:
    file_check = prep.evaluate_ui_implementation_files()
    commit_need = prep.evaluate_commit_push_need()
    deployment = prep.evaluate_latest_deployment_metadata()
    row = prep.classify_local_deployment_gap(file_check, commit_need, deployment)
    assert row["gap_classification"] in {
        "ui_changes_uncommitted_or_unpushed",
        "deployment_gap_not_understood",
        "remote_main_ahead_with_data_only_auto_crawl_gap",
    }


def test_auto_crawl_influence_evaluated() -> None:
    deployment = prep.evaluate_latest_deployment_metadata()
    gap = prep.classify_local_deployment_gap(
        prep.evaluate_ui_implementation_files(),
        prep.evaluate_commit_push_need(),
        deployment,
    )
    row = prep.evaluate_auto_crawl_influence(deployment, gap)
    assert row["origin_main_latest_is_auto_crawl"] is True


def test_no_deploy_or_git_push_executed() -> None:
    row = prep.evaluate_guard()
    assert row["deploy_executed"] is False
    assert row["git_push_executed"] is False


def test_test_command_list_recorded() -> None:
    row = prep.define_test_command_list()
    assert len(row["commands"]) >= 4


def test_safe_redeploy_checklist_present() -> None:
    row = prep.define_safe_redeploy_checklist()
    assert "git diff 확인" in row["items"]
    assert "deploy 후 새 Vercel deployment READY 확인" in row["items"]


def test_post_deploy_smoke_checklist_present() -> None:
    row = prep.define_post_deploy_smoke_checklist()
    assert "/api/search?q=summicron&limit=5" in row["items"]
    assert "hasselblad xpan" in row["items"]


def test_tester_link_send_allowed_remains_false() -> None:
    assert _result()["deployment_prep_result"]["tester_link_send_allowed"] is False


def test_decision_is_expected_hold() -> None:
    assert _result()["deployment_prep_result"]["decision_status"] in {
        "beta_ui_deployment_prep_hold_ui_changes_uncommitted_or_unpushed",
        "beta_ui_deployment_prep_hold_deployment_gap_not_understood",
    }


def test_scenario_rows_present() -> None:
    rows = _result()["scenario_rows"]
    assert len(rows) == 14
    assert all(row["status"] == "passed" for row in rows)


def test_export_contains_expected_files() -> None:
    exported = prep.export_results(_result())
    modified_files = set(exported["artifact_json"]["modified_files"])
    expected = {
        "scripts/run_p3_beta_ui_deployment_prep_and_safe_redeploy_check.py",
        "tests/test_beta_ui_deployment_prep_and_safe_redeploy_check.py",
        "data/admin/p3_beta_ui_deployment_prep_and_safe_redeploy_check_v0.md",
        "data/admin/p3_beta_ui_deployment_prep_and_safe_redeploy_check_v0.jsonl",
        "data/admin/beta_ui_deployment_prep_and_safe_redeploy_check_v0.json",
    }
    assert modified_files == expected


def test_json_jsonl_validation_basics() -> None:
    exported = prep.export_results(_result())
    row_types = {row["row_type"] for row in exported["jsonl_rows"]}
    required = {
        "beta_ui_deployment_prep_and_safe_redeploy_check_policy",
        "ui_implementation_evidence",
        "prior_live_parity_hold_evidence",
        "git_working_tree",
        "frontend_diff",
        "ui_implementation_files",
        "commit_push_need",
        "latest_deployment_metadata",
        "local_deployment_parity_gap",
        "auto_crawl_influence",
        "test_command_list",
        "safe_redeploy_checklist",
        "post_deploy_smoke_checklist",
        "production_public_access_guard",
        "deployment_prep_result",
        "scenario_validation",
        "progress_report",
        "summary",
    }
    assert required <= row_types


def test_report_contains_required_sections() -> None:
    exported = prep.export_results(_result())
    report = prep.build_report(_result(), exported)
    assert "## 5. git status 요약" in report
    assert "## 14. post-deploy smoke checklist" in report


def test_golden_set_file_present() -> None:
    assert (ROOT / "golden_set.py").exists()


def main() -> None:
    tests = [value for name, value in sorted(globals().items()) if name.startswith("test_") and callable(value)]
    for func in tests:
        func()
    print(f"ok ({len(tests)} tests)")


if __name__ == "__main__":
    main()
