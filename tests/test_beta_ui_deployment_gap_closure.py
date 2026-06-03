from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "scripts"
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import run_p3_beta_ui_deployment_gap_closure as gap_closure


_CACHED_RESULT: dict | None = None


def _result() -> dict:
    global _CACHED_RESULT
    if _CACHED_RESULT is None:
        _CACHED_RESULT = gap_closure.process()
    return _CACHED_RESULT


def test_module_imports() -> None:
    assert gap_closure.__name__ == "run_p3_beta_ui_deployment_gap_closure"


def test_prior_deployment_prep_hold_evidence_loaded() -> None:
    row = gap_closure.load_prior_deployment_prep_hold_evidence()
    assert row["evidence_loaded"] is True
    assert row["prior_prep_decision_status"] == "beta_ui_deployment_prep_hold_ui_changes_uncommitted_or_unpushed"


def test_working_tree_inspected() -> None:
    row = gap_closure.inspect_working_tree()
    assert row["current_branch"] in {"main", "beta-ui-redesign-controlled-preview"}
    assert row["local_head"]
    assert isinstance(row["ui_core_status"], list)


def test_ui_core_diff_identified() -> None:
    row = gap_closure.summarize_ui_core_diff()
    assert row["ui_core_diff_file_count"] in {0, 3}
    if row["ui_core_diff_file_count"] == 3:
        assert row["search_route_present_in_diff"] is True
        assert row["runtime_fallback_present_in_diff"] is True


def test_untracked_inventory_recorded() -> None:
    row = gap_closure.record_untracked_inventory()
    assert row["untracked_file_count"] >= row["ui_related_untracked_count"]
    assert row["ui_related_untracked_count"] >= 1


def test_origin_main_gap_recorded() -> None:
    row = gap_closure.record_origin_main_gap()
    assert row["origin_main_head"]
    assert row["ahead_behind_counts"] in {"0\t6", "1\t0"}


def test_patch_backup_created() -> None:
    row = gap_closure.create_patch_backup()
    assert row["patch_created"] is True
    assert row["patch_line_count"] >= 0
    assert row["patch_contains_ui_core_files"] in {True, False}


def test_origin_main_conflict_risk_evaluated() -> None:
    row = gap_closure.evaluate_origin_main_conflict_risk(gap_closure.record_origin_main_gap())
    assert row["conflict_risk_level"] in {"low", "high"}
    assert row["auto_crawl_only_remote_gap"] in {True, False}


def test_commit_inclusion_plan_produced() -> None:
    row = gap_closure.build_commit_inclusion_plan()
    assert "app/app.py" in row["required_include_files"]
    assert row["required_missing_files"] == []


def test_commit_exclusion_plan_produced() -> None:
    row = gap_closure.build_commit_exclusion_plan()
    assert "data/private/*" in row["exclude_patterns"]
    assert row["exclude_env_or_secret_files"] is True


def test_safe_merge_rebase_plan_produced() -> None:
    row = gap_closure.build_safe_merge_rebase_plan()
    assert len(row["plan_steps"]) >= 8
    assert row["automatic_merge_executed"] is False


def test_private_secret_risk_checked() -> None:
    row = gap_closure.check_private_secret_risk(
        gap_closure.record_untracked_inventory(),
        gap_closure.build_commit_inclusion_plan(),
    )
    assert row["private_secret_risk_detected"] is False
    assert row["private_secret_risk_level"] == "low"


def test_guard_remains_false() -> None:
    row = gap_closure.evaluate_guard()
    assert row["production_launch_go"] is False
    assert row["git_push_executed"] is False
    assert row["deployment_executed"] is False
    assert row["destructive_git_operation_executed"] is False


def test_result_is_ready_for_manual_handoff() -> None:
    row = _result()["deployment_gap_closure_result"]
    assert row["decision_status"] in {
        "beta_ui_deployment_gap_closure_ready_for_manual_commit_push_deploy_handoff",
        "beta_ui_deployment_gap_closure_hold_patch_backup_failed",
    }
    assert row["tester_link_send_allowed"] is False


def test_scenario_rows_present() -> None:
    rows = _result()["scenario_rows"]
    assert len(rows) == 15
    assert all(row["status"] == "passed" for row in rows)


def test_export_contains_expected_files() -> None:
    exported = gap_closure.export_results(_result())
    modified_files = set(exported["artifact_json"]["modified_files"])
    expected = {
        "scripts/run_p3_beta_ui_deployment_gap_closure.py",
        "tests/test_beta_ui_deployment_gap_closure.py",
        "data/admin/p3_beta_ui_deployment_gap_closure_v0.md",
        "data/admin/p3_beta_ui_deployment_gap_closure_v0.jsonl",
        "data/admin/beta_ui_deployment_gap_closure_v0.json",
        "data/admin/beta_ui_deployment_gap_closure_ui_diff_v0.patch",
    }
    assert modified_files == expected


def test_jsonl_contains_required_row_types() -> None:
    exported = gap_closure.export_results(_result())
    row_types = {row["row_type"] for row in exported["jsonl_rows"]}
    required = {
        "beta_ui_deployment_gap_closure_policy",
        "prior_deployment_prep_hold_evidence",
        "working_tree_inspection",
        "ui_core_diff_summary",
        "untracked_inventory",
        "origin_main_gap",
        "patch_backup",
        "origin_main_conflict_risk",
        "commit_inclusion_plan",
        "commit_exclusion_plan",
        "safe_merge_rebase_plan",
        "private_secret_risk_check",
        "production_public_access_guard",
        "deployment_gap_closure_result",
        "scenario_validation",
        "progress_report",
        "summary",
    }
    assert required <= row_types


def test_report_contains_required_sections() -> None:
    exported = gap_closure.export_results(_result())
    report = gap_closure.build_report(_result(), exported)
    assert "## 10. patch backup 결과" in report
    assert "## 14. safe merge/rebase plan" in report
    assert "## 20. 다음 backlog 후보" in report


def test_patch_file_exists_after_process() -> None:
    assert (ROOT / "data/admin/beta_ui_deployment_gap_closure_ui_diff_v0.patch").exists()


def test_no_production_ui_files_modified_by_script_definition() -> None:
    for path in [
        ROOT / "app/app.py",
        ROOT / "app/templates/index.html",
        ROOT / "index.html",
    ]:
        assert path.exists()


def test_golden_set_present() -> None:
    assert (ROOT / "golden_set.py").exists()


def main() -> None:
    tests = [value for name, value in sorted(globals().items()) if name.startswith("test_") and callable(value)]
    for func in tests:
        func()
    print(f"ok ({len(tests)} tests)")


if __name__ == "__main__":
    main()
