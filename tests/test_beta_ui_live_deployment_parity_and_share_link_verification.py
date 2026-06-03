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

import run_p3_beta_ui_live_deployment_parity_and_share_link_verification as verification


_CACHED_RESULT: dict | None = None


def _result() -> dict:
    global _CACHED_RESULT
    if _CACHED_RESULT is None:
        _CACHED_RESULT = verification.process_verification()
    return _CACHED_RESULT


def test_module_imports() -> None:
    assert verification.__name__ == "run_p3_beta_ui_live_deployment_parity_and_share_link_verification"


def test_prior_ui_implementation_evidence_loaded() -> None:
    row = verification.load_prior_ui_implementation_evidence()
    assert row["ready_for_runtime_triage_or_smoke"] is True


def test_prior_runtime_smoke_evidence_loaded() -> None:
    row = verification.load_prior_runtime_smoke_evidence()
    assert row["prior_query_smoke_count"] == 10


def test_local_git_deployment_metadata_evaluated() -> None:
    row = verification.collect_local_git_and_deployment_metadata()
    assert row["local_git_head"] != "unavailable"
    assert row["local_git_branch"] in {"main", "beta-ui-redesign-controlled-preview"}


def test_ui_implementation_parity_evaluated() -> None:
    row = verification.evaluate_ui_implementation_deployment_parity()
    assert row["local_frontend_files_match"] is True
    assert row["ui_implementation_deployed_to_live"] in {"unknown_not_verified", "deployed", "not_deployed"}


def test_live_share_landing_verification_attempted() -> None:
    row = verification.attempt_live_share_landing_verification()
    assert row["landing_live_status"] in {"verified", "not_verified", "not_verified_due_resolution_or_network_limit"}


def test_live_share_api_verification_attempted() -> None:
    row = verification.attempt_live_share_api_verification()
    assert row["live_api_total_probe_count"] == 4


def test_live_query_smoke_recorded() -> None:
    rows = verification.evaluate_live_query_smoke()
    assert len(rows) == 10


def test_required_copy_present_if_live_verified() -> None:
    landing = verification.attempt_live_share_landing_verification()
    row = verification.evaluate_required_copy_presence(landing)
    if landing["landing_live_verified"]:
        assert row["required_copy_present_count"] == 5
    else:
        assert row["live_verified"] is False


def test_forbidden_copy_absent_if_live_verified() -> None:
    landing = verification.attempt_live_share_landing_verification()
    row = verification.evaluate_forbidden_copy_absence(landing)
    if landing["landing_live_verified"]:
        assert row["forbidden_copy_absent"] is True


def test_raw_server_error_absent_if_live_verified() -> None:
    landing = verification.attempt_live_share_landing_verification()
    live_api = verification.attempt_live_share_api_verification()
    row = verification.evaluate_raw_server_error_exposure(landing, live_api)
    assert row["raw_server_error_visible_on_live"] is False


def test_fake_fill_absence_logic() -> None:
    rows = verification.evaluate_live_query_smoke()
    row = verification.evaluate_fake_fill_absence(rows)
    assert row["fake_fill_absent"] is True
    assert set(row["target_queries"]) == {"ricoh gr iiix", "hasselblad xpan"}


def test_production_public_access_guard_false() -> None:
    row = verification.evaluate_guard()
    assert row["production_launch_go"] is False
    assert row["public_unrestricted_access_enabled"] is False
    assert row["external_tester_access_enabled"] is False


def test_no_production_code_modified_flag() -> None:
    policy = verification.create_policy()
    assert policy["production_code_modified"] is False
    assert policy["automatic_deployment_execution"] is False


def test_tester_send_decision_honest() -> None:
    row = _result()["tester_send_decision"]
    assert row["decision_status"] in {
        "beta_ui_live_deployment_parity_and_share_link_verification_passed_ready_for_controlled_tester_preview",
        "beta_ui_live_deployment_parity_hold_ui_implementation_not_deployed",
        "beta_ui_live_deployment_parity_hold_live_share_link_not_verified",
        "beta_ui_live_deployment_parity_hold_runtime_server_error_reproduced",
        "beta_ui_live_deployment_parity_hold_forbidden_claim_or_raw_error",
        "beta_ui_live_deployment_parity_rollback_required",
    }


def test_current_environment_expected_hold_or_pass() -> None:
    assert _result()["tester_send_decision"]["decision_status"] in {
        "beta_ui_live_deployment_parity_and_share_link_verification_passed_ready_for_controlled_tester_preview",
        "beta_ui_live_deployment_parity_hold_live_share_link_not_verified",
    }


def test_scenario_rows_present() -> None:
    rows = _result()["scenario_rows"]
    assert len(rows) == 15
    assert all(row["status"] == "passed" for row in rows)


def test_export_contains_expected_files() -> None:
    exported = verification.export_results(_result())
    modified_files = set(exported["artifact_json"]["modified_files"])
    expected = {
        "scripts/run_p3_beta_ui_live_deployment_parity_and_share_link_verification.py",
        "tests/test_beta_ui_live_deployment_parity_and_share_link_verification.py",
        "data/admin/p3_beta_ui_live_deployment_parity_and_share_link_verification_v0.md",
        "data/admin/p3_beta_ui_live_deployment_parity_and_share_link_verification_v0.jsonl",
        "data/admin/beta_ui_live_deployment_parity_and_share_link_verification_v0.json",
    }
    assert modified_files == expected


def test_json_jsonl_validation_basics() -> None:
    exported = verification.export_results(_result())
    row_types = {row["row_type"] for row in exported["jsonl_rows"]}
    required = {
        "beta_ui_live_deployment_parity_and_share_link_verification_policy",
        "prior_ui_implementation_evidence",
        "prior_runtime_smoke_evidence",
        "local_git_and_deployment_metadata",
        "ui_implementation_deployment_parity",
        "live_share_landing_verification",
        "live_share_api_verification",
        "live_query_smoke_result",
        "required_copy_presence",
        "forbidden_copy_absence",
        "raw_server_error_exposure",
        "fake_fill_absence",
        "production_public_access_guard",
        "tester_send_decision",
        "scenario_validation",
        "progress_report",
        "summary",
    }
    assert required <= row_types


def test_report_contains_required_sections() -> None:
    exported = verification.export_results(_result())
    report = verification.build_report(_result(), exported)
    assert "## 8. live/share link 검증 가능 여부" in report
    assert "## 19. tester link send 가능 여부" in report


def test_no_raw_server_error_or_forbidden_claims_in_artifact_logic() -> None:
    exported = verification.export_results(_result())
    blob = json.dumps(exported["artifact_json"], ensure_ascii=False) + json.dumps(exported["jsonl_rows"], ensure_ascii=False)
    assert "A server error has occurred" not in blob


def test_golden_set_file_present() -> None:
    assert (ROOT / "golden_set.py").exists()


def main() -> None:
    tests = [value for name, value in sorted(globals().items()) if name.startswith("test_") and callable(value)]
    for func in tests:
        func()
    print(f"ok ({len(tests)} tests)")


if __name__ == "__main__":
    main()
