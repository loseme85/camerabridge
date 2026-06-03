from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "scripts"
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import run_p3_beta_share_link_runtime_server_error_fixup as fixup


_CACHED_RESULT: dict | None = None


def _result() -> dict:
    global _CACHED_RESULT
    if _CACHED_RESULT is None:
        _CACHED_RESULT = fixup.process()
    return _CACHED_RESULT


def test_module_imports() -> None:
    assert fixup.__name__ == "run_p3_beta_share_link_runtime_server_error_fixup"


def test_triage_evidence_loaded() -> None:
    row = fixup.load_previous_triage_summary()
    assert row["triage_status"] == "beta_share_link_runtime_server_error_triage_completed_ready_for_fixup"


def test_modified_files_are_scoped() -> None:
    row = fixup.inspect_modified_files()
    assert row["modified_files"] == ["vercel.json", "api/search.py"]
    assert row["search_ranking_related_files_changed"] is False


def test_search_rewrite_added() -> None:
    row = fixup.inspect_search_route_fix()
    assert row["search_rewrite_added"] is True
    assert row["search_rewrite_destination"] == "/app/templates/index.html"


def test_api_runtime_safety_added() -> None:
    row = fixup.inspect_api_runtime_fix()
    assert row["lazy_runtime_dependencies_added"] is True
    assert row["resolved_index_path_helper_added"] is True
    assert row["bootstrap_error_json_added"] is True
    assert row["handler_last_boundary_added"] is True


def test_data_index_path_check() -> None:
    row = fixup.inspect_data_index_path()
    assert row["index_exists"] is True
    assert row["candidate_path_resolution_added"] is True


def test_local_route_smoke_passes() -> None:
    row = fixup.run_local_route_smoke()
    assert row["all_200"] is True
    assert row["api_all_json_200"] is True
    assert len(row["checks"]) == 6


def test_local_search_route_200() -> None:
    row = fixup.run_local_route_smoke()
    search_row = next(item for item in row["checks"] if item["path"] == "/search")
    assert search_row["status_code"] == 200


def test_local_api_queries_200_json() -> None:
    row = fixup.run_local_route_smoke()
    api_rows = [item for item in row["checks"] if item["path"].startswith("/api/")]
    assert all(item["status_code"] == 200 for item in api_rows)
    assert all("application/json" in item["content_type"] for item in api_rows)


def test_raw_server_error_absent_locally() -> None:
    local = fixup.run_local_route_smoke()
    row = fixup.evaluate_raw_server_error_boundary(local)
    assert row["raw_server_error_absent"] is True


def test_fake_fill_absent() -> None:
    local = fixup.run_local_route_smoke()
    row = fixup.evaluate_fake_fill(local)
    assert row["fake_fill_detected"] is False
    assert row["no_result_checks"]["/api/search?q=ricoh%20gr%20iiix&limit=5"]["result_count"] == 0
    assert row["no_result_checks"]["/api/search?q=hasselblad%20xpan&limit=5"]["result_count"] == 0


def test_forbidden_claims_absent() -> None:
    row = fixup.evaluate_forbidden_claims()
    assert row["forbidden_claims_absent"] is True


def test_guard_false() -> None:
    row = fixup.evaluate_guard()
    assert row["production_launch_go"] is False
    assert row["tester_link_send_allowed"] is False
    assert row["fake_fill_added"] is False


def test_validation_results_recorded() -> None:
    row = fixup.record_validation_results()
    assert row["all_passed"] is True
    assert len(row["commands"]) == 6


def test_result_is_ready_for_owner_approved_preview_recheck() -> None:
    row = _result()["fixup_result"]
    assert row["decision_status"] == "beta_share_link_runtime_server_error_fixup_ready_for_owner_approved_commit_push_preview_recheck"


def test_scenario_rows_present() -> None:
    rows = _result()["scenario_rows"]
    assert len(rows) == 15
    assert all(row["status"] == "passed" for row in rows)


def test_export_contains_expected_files() -> None:
    exported = fixup.export_results(_result())
    modified_files = set(exported["artifact_json"]["modified_files"])
    expected = {
        "vercel.json",
        "api/search.py",
        "scripts/run_p3_beta_share_link_runtime_server_error_fixup.py",
        "tests/test_beta_share_link_runtime_server_error_fixup.py",
        "data/admin/p3_beta_share_link_runtime_server_error_fixup_v0.md",
        "data/admin/p3_beta_share_link_runtime_server_error_fixup_v0.jsonl",
        "data/admin/beta_share_link_runtime_server_error_fixup_v0.json",
    }
    assert modified_files == expected


def test_jsonl_contains_required_row_types() -> None:
    exported = fixup.export_results(_result())
    row_types = {row["row_type"] for row in exported["jsonl_rows"]}
    required = {
        "beta_share_link_runtime_server_error_fixup_policy",
        "previous_triage_summary",
        "modified_files_inspection",
        "search_route_fix",
        "api_runtime_fix",
        "data_index_path_check",
        "local_route_smoke",
        "raw_server_error_boundary_check",
        "fake_fill_check",
        "forbidden_claim_check",
        "validation_results",
        "production_public_access_guard",
        "fixup_result",
        "scenario_validation",
        "progress_report",
        "summary",
    }
    assert required <= row_types


def test_report_contains_required_sections() -> None:
    exported = fixup.export_results(_result())
    report = fixup.build_report(_result(), exported)
    assert "## 6. /search route fix 내용" in report
    assert "## 14. commit/push/deploy 필요 여부" in report


def test_source_files_exist() -> None:
    assert fixup.TRIAGE_MD_PATH.exists()
    assert fixup.TRIAGE_JSON_PATH.exists()
    assert fixup.PREVIEW_CHECK_MD_PATH.exists()
    assert fixup.PREVIEW_CHECK_JSON_PATH.exists()


def test_golden_set_present() -> None:
    assert (ROOT / "golden_set.py").exists()


def main() -> None:
    tests = [value for name, value in sorted(globals().items()) if name.startswith("test_") and callable(value)]
    for func in tests:
        func()
    print(f"ok ({len(tests)} tests)")


if __name__ == "__main__":
    main()
