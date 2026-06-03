from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "scripts"
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import run_p3_beta_ui_manual_commit_push_and_deploy_handoff as handoff


_CACHED_RESULT: dict | None = None


def _result() -> dict:
    global _CACHED_RESULT
    if _CACHED_RESULT is None:
        _CACHED_RESULT = handoff.process()
    return _CACHED_RESULT


def test_module_imports() -> None:
    assert handoff.__name__ == "run_p3_beta_ui_manual_commit_push_and_deploy_handoff"


def test_deployment_gap_closure_evidence_loaded() -> None:
    row = handoff.load_previous_evidence_summary()
    assert row["evidence_loaded"] is True
    assert row["gap_closure_status"] == "beta_ui_deployment_gap_closure_ready_for_manual_commit_push_deploy_handoff"


def test_git_baseline_recorded() -> None:
    row = handoff.record_git_baseline()
    assert row["branch"] in {"main", "beta-ui-redesign-controlled-preview"}
    assert row["local_head"]
    assert row["origin_main_head"]


def test_commit_inclusion_plan_finalized() -> None:
    row = handoff.finalize_commit_inclusion_plan()
    assert row["commit_scope_clear"] is True
    assert "app/app.py" in row["required_include_files"]
    assert "data/admin/beta_ui_deployment_gap_closure_ui_diff_v0.patch" in row["required_include_files"]


def test_commit_exclusion_plan_finalized() -> None:
    row = handoff.finalize_commit_exclusion_plan()
    assert "data/private/*" in row["exclude_files_or_patterns"]
    assert row["exclude_unrelated_untracked_files"] is True


def test_private_secret_risk_checked() -> None:
    row = handoff.check_private_secret_risk()
    assert row["private_secret_risk_level"] == "low"
    assert row["risky_files"] == []


def test_manual_command_sequence_produced() -> None:
    row = handoff.produce_manual_command_sequence()
    assert row["recommended_option"] == "option_b_feature_branch_commit_then_rebase"
    assert "git checkout -b beta-ui-redesign-controlled-preview" in row["commands"]
    assert row["commands_executed_in_this_round"] is False


def test_recommended_branch_strategy_defined() -> None:
    row = handoff.define_recommended_branch_strategy()
    assert row["recommended_strategy"] == "feature_branch_then_rebase_onto_origin_main"


def test_owner_approval_gate_defined() -> None:
    row = handoff.define_owner_approval_gate()
    assert row["approval_required_before_git_commit"] is True
    assert row["approval_required_before_git_push"] is True
    assert row["approval_required_before_vercel_deploy"] is True


def test_deploy_strategy_options_defined() -> None:
    row = handoff.define_deploy_strategy_options()
    assert len(row["options"]) == 3
    assert row["recommended_primary_option"] == "deploy_strategy_pr_merge"


def test_post_deploy_smoke_checklist_produced() -> None:
    row = handoff.define_post_deploy_smoke_checklist()
    assert row["item_count"] >= 20
    assert "Vercel deployment state = READY" in row["items"]


def test_no_git_commit_push_or_deploy_executed() -> None:
    row = handoff.evaluate_guard()
    assert row["git_commit_executed"] is False
    assert row["git_push_executed"] is False
    assert row["deployment_executed"] is False


def test_production_public_access_guard_false() -> None:
    row = handoff.evaluate_guard()
    assert row["production_launch_go"] is False
    assert row["public_unrestricted_access_enabled"] is False
    assert row["external_tester_access_enabled"] is False


def test_decision_ready_for_owner_approved_execution() -> None:
    row = _result()["manual_handoff_result"]
    assert row["decision_status"] == "beta_ui_manual_commit_push_deploy_handoff_ready_for_owner_approved_execution"
    assert row["tester_link_send_allowed"] is False


def test_scenario_rows_present() -> None:
    rows = _result()["scenario_rows"]
    assert len(rows) == 15
    assert all(row["status"] == "passed" for row in rows)


def test_export_contains_expected_files() -> None:
    exported = handoff.export_results(_result())
    modified_files = set(exported["artifact_json"]["modified_files"])
    expected = {
        "scripts/run_p3_beta_ui_manual_commit_push_and_deploy_handoff.py",
        "tests/test_beta_ui_manual_commit_push_and_deploy_handoff.py",
        "data/admin/p3_beta_ui_manual_commit_push_and_deploy_handoff_v0.md",
        "data/admin/p3_beta_ui_manual_commit_push_and_deploy_handoff_v0.jsonl",
        "data/admin/beta_ui_manual_commit_push_and_deploy_handoff_v0.json",
    }
    assert modified_files == expected


def test_jsonl_contains_required_row_types() -> None:
    exported = handoff.export_results(_result())
    row_types = {row["row_type"] for row in exported["jsonl_rows"]}
    required = {
        "beta_ui_manual_commit_push_and_deploy_handoff_policy",
        "previous_evidence_summary",
        "git_baseline",
        "commit_inclusion_plan",
        "commit_exclusion_plan",
        "private_secret_risk_check",
        "manual_command_sequence",
        "recommended_branch_strategy",
        "owner_approval_gate",
        "deploy_strategy_options",
        "post_deploy_smoke_checklist",
        "production_public_access_guard",
        "manual_handoff_result",
        "scenario_validation",
        "progress_report",
        "summary",
    }
    assert required <= row_types


def test_report_contains_required_sections() -> None:
    exported = handoff.export_results(_result())
    report = handoff.build_report(_result(), exported)
    assert "## 8. manual command sequence" in report
    assert "## 12. post-deploy smoke checklist" in report
    assert "## 17. 다음 backlog 후보" in report


def test_patch_reference_exists() -> None:
    assert (ROOT / "data/admin/beta_ui_deployment_gap_closure_ui_diff_v0.patch").exists()


def test_golden_set_present() -> None:
    assert (ROOT / "golden_set.py").exists()


def main() -> None:
    tests = [value for name, value in sorted(globals().items()) if name.startswith("test_") and callable(value)]
    for func in tests:
        func()
    print(f"ok ({len(tests)} tests)")


if __name__ == "__main__":
    main()
