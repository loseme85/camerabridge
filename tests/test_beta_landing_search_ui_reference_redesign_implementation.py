from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import beta_landing_search_ui_reference_redesign_implementation as implementation
from scripts.run_p3_beta_landing_search_ui_reference_redesign_implementation import _build_report


_CACHED_RESULT: dict | None = None


def _result() -> dict:
    global _CACHED_RESULT
    if _CACHED_RESULT is None:
        _CACHED_RESULT = implementation.process_beta_landing_search_ui_reference_redesign_implementation()
    return _CACHED_RESULT


def test_module_imports() -> None:
    assert implementation.__name__ == "beta_landing_search_ui_reference_redesign_implementation"


def test_policy_ui_facing_only_and_guards_disabled() -> None:
    policy = implementation.create_beta_landing_search_ui_reference_redesign_implementation_policy()
    assert policy["ui_implementation_in_this_round"] is True
    assert policy["candidate_access_code_modification_allowed"] is False
    assert policy["search_ranking_code_modification_allowed"] is False
    assert policy["classifier_taxonomy_modification_allowed"] is False


def test_contract_evidence_loaded() -> None:
    row = implementation.load_beta_landing_search_ui_reference_redesign_implementation_evidence()
    assert row["contract_status"] == "beta_landing_search_ui_reference_redesign_contract_ready_for_implementation"
    assert row["contract_ready_for_implementation"] is True


def test_frontend_files_present_and_identical() -> None:
    row = implementation.inspect_frontend_files()
    assert row["app_template_exists"] is True
    assert row["root_index_exists"] is True
    assert row["app_and_root_index_identical"] is True
    assert row["existing_search_api_connection_preserved"] is True


def test_landing_page_hero_and_notices_present() -> None:
    row = implementation.define_landing_page_implementation()
    assert row["hero_headline_present"] is True
    assert row["trust_notice_present"] is True
    assert row["beta_notice_present"] is True
    assert row["no_personal_data_notice_present"] is True


def test_search_home_is_implemented() -> None:
    row = implementation.define_search_home_implementation()
    assert row["large_search_box_present"] is True
    assert row["example_query_chip_count"] >= 6
    assert row["no_fake_fill_principle_present"] is True


def test_search_results_support_confidence_source_and_status_fields() -> None:
    row = implementation.define_search_results_implementation()
    assert row["status_badges_present"] is True
    assert row["confidence_fields_present"] is True
    assert row["source_coverage_present"] is True


def test_state_cards_present() -> None:
    row = implementation.define_search_state_implementation()
    assert row["no_result_copy_present"] is True
    assert row["source_gap_copy_present"] is True
    assert row["broad_query_refinement_present"] is True
    assert row["runtime_error_fallback_present"] is True


def test_model_market_entry_present() -> None:
    row = implementation.define_model_market_entry_implementation()
    assert row["section_present"] is True
    assert row["indicative_price_band_present"] is True


def test_archive_sold_reference_entry_present() -> None:
    row = implementation.define_archive_sold_reference_implementation()
    assert row["section_present"] is True
    assert row["no_overstatement_copy_present"] is True


def test_alert_cta_present() -> None:
    row = implementation.define_alert_cta_implementation()
    assert row["exact_model_alert_present"] is True
    assert row["market_change_alert_present"] is True


def test_runtime_error_fallback_prevents_raw_server_error_copy() -> None:
    row = implementation.define_runtime_error_fallback_implementation()
    assert row["safe_fallback_copy_present"] is True
    assert row["raw_server_error_copy_absent"] is True


def test_external_tester_first_use_notice_present() -> None:
    row = implementation.define_external_tester_first_use_notice_implementation()
    assert row["section_present"] is True
    assert row["do_not_paste_private_details_present"] is True


def test_forbidden_claims_absent() -> None:
    row = implementation.define_forbidden_claims_check()
    assert row["all_forbidden_claims_absent"] is True
    assert row["present_forbidden_claims"] == []


def test_query_smoke_is_recorded() -> None:
    row = implementation.record_query_smoke_results()
    assert row["query_count"] == 10
    assert row["all_status_ok"] is True


def test_query_smoke_broad_and_empty_states_are_honest() -> None:
    smoke = implementation.record_query_smoke_results()["queries"]
    by_query = {row["query"]: row for row in smoke}
    assert by_query["summicron"]["ui_state"] == "broad_query_refinement"
    assert by_query["leica lens"]["ui_state"] == "broad_query_refinement"
    assert by_query["ricoh gr iiix"]["ui_state"] == "no_result"


def test_implementation_handoff_defined() -> None:
    row = implementation.define_implementation_handoff()
    assert row["implementation_ready_for_runtime_triage_or_smoke"] is True
    assert "P3-BETA-SHARE-LINK-RUNTIME-SERVER-ERROR-TRIAGE" in row["required_next_rounds"]


def test_scenario_validation_passes() -> None:
    rows = _result()["scenario_rows"]
    assert len(rows) == 20
    assert all(row["status"] == "passed" for row in rows)


def test_decision_status_ready_for_runtime_triage_or_smoke() -> None:
    assert _result()["decision"]["decision_status"] == "beta_landing_search_ui_reference_redesign_implementation_ready_for_runtime_triage_or_smoke"


def test_production_public_access_guard_remains_false() -> None:
    policy = _result()["policy"]
    assert policy["production_launch_go"] is False
    assert policy["public_unrestricted_access_enabled"] is False
    assert policy["external_tester_access_enabled"] is False
    assert policy["invite_sent_count"] == 0


def test_export_contains_expected_modified_files() -> None:
    exported = implementation.export_beta_landing_search_ui_reference_redesign_implementation(_result())
    modified_files = set(exported["artifact_json"]["modified_files"])
    expected = {
        "app/app.py",
        "app/templates/index.html",
        "index.html",
        "beta_landing_search_ui_reference_redesign_implementation.py",
        "scripts/run_p3_beta_landing_search_ui_reference_redesign_implementation.py",
        "tests/test_beta_landing_search_ui_reference_redesign_implementation.py",
        "data/admin/p3_beta_landing_search_ui_reference_redesign_implementation_v0.md",
        "data/admin/p3_beta_landing_search_ui_reference_redesign_implementation_v0.jsonl",
        "data/admin/beta_landing_search_ui_reference_redesign_implementation_v0.json",
    }
    assert modified_files == expected


def test_report_contains_required_sections() -> None:
    exported = implementation.export_beta_landing_search_ui_reference_redesign_implementation(_result())
    report = _build_report(_result(), exported)
    assert "## 진행률/상태" in report
    assert "## 20. query smoke 결과" in report
    assert "runtime error fallback" in report.lower()


def test_json_jsonl_validation_basics() -> None:
    exported = implementation.export_beta_landing_search_ui_reference_redesign_implementation(_result())
    row_types = {row["row_type"] for row in exported["jsonl_rows"]}
    required = {
        "beta_landing_search_ui_reference_redesign_implementation_policy",
        "beta_landing_search_ui_reference_redesign_implementation_evidence",
        "frontend_files",
        "ui_reference_mix_applied",
        "landing_page_implementation",
        "search_home_implementation",
        "search_results_implementation",
        "search_state_implementation",
        "model_market_entry_implementation",
        "archive_sold_reference_implementation",
        "alert_cta_implementation",
        "runtime_error_fallback_implementation",
        "external_tester_first_use_notice_implementation",
        "forbidden_claims_check",
        "query_smoke",
        "implementation_handoff",
        "scenario_validation",
        "implementation_result",
        "progress_report",
        "summary",
    }
    assert required <= row_types


def test_no_raw_server_error_or_raw_identity_in_artifacts() -> None:
    exported = implementation.export_beta_landing_search_ui_reference_redesign_implementation(_result())
    blob = json.dumps(exported["artifact_json"], ensure_ascii=False) + json.dumps(exported["jsonl_rows"], ensure_ascii=False)
    assert "A server error has occurred" not in blob
    assert "raw_email" not in blob
    assert "data/private/" not in blob


def test_existing_search_ui_contract_stays_satisfied() -> None:
    import test_search_ui

    test_search_ui.test_index_calls_search_endpoint()
    test_search_ui.test_required_ui_controls_exist()
    test_search_ui.test_quality_summary_message_is_consumed_from_api()


def test_package_json_absent_is_expected() -> None:
    assert not (ROOT / "package.json").exists()


def test_golden_set_file_present() -> None:
    assert (ROOT / "golden_set.py").exists()


def main() -> None:
    tests = [value for name, value in sorted(globals().items()) if name.startswith("test_") and callable(value)]
    for func in tests:
        func()
    print(f"ok ({len(tests)} tests)")


if __name__ == "__main__":
    main()
