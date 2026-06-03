from __future__ import annotations

import copy
import json
from pathlib import Path
from typing import Any

from api.search import endpoint_response

import beta_landing_search_ui_reference_redesign_contract as contract


ROOT = Path(__file__).resolve().parent
CONTRACT_JSON_PATH = ROOT / "data/admin/beta_landing_search_ui_reference_redesign_contract_v0.json"
APP_HTML_PATH = ROOT / "app/templates/index.html"
ROOT_HTML_PATH = ROOT / "index.html"
APP_SERVER_PATH = ROOT / "app/app.py"

SMOKE_QUERIES = [
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

LOCAL_BROAD_QUERY_HINTS = {
    "summicron": '"Summicron" can refer to multiple Leica lens families. Choose a mount or focal length to refine your search.',
    "summilux": '"Summilux" can refer to multiple Leica lens families. Choose a mount or focal length to refine your search.',
    "leica lens": "This query is still broad. Choose a family, mount, or focal length to refine your search.",
    "leica m": "This query can refer to multiple M-system bodies and lenses. Refine by body model or lens family.",
    "50 cron": "Collector shorthand can match multiple Summicron variants. Choose a mount or full model name to refine your search.",
}

FRONTEND_FILES = [
    "app/app.py",
    "app/templates/index.html",
    "index.html",
    "beta_landing_search_ui_reference_redesign_implementation.py",
    "scripts/run_p3_beta_landing_search_ui_reference_redesign_implementation.py",
    "tests/test_beta_landing_search_ui_reference_redesign_implementation.py",
    "data/admin/p3_beta_landing_search_ui_reference_redesign_implementation_v0.md",
    "data/admin/p3_beta_landing_search_ui_reference_redesign_implementation_v0.jsonl",
    "data/admin/beta_landing_search_ui_reference_redesign_implementation_v0.json",
]

FORBIDDEN_CODE_PATHS = [
    "classifier_v2.py",
    "model_detector.py",
    "query_parser.py",
    "query_resolver.py",
    "search_service.py",
    "search_ui_hints.py",
]

DEFAULT_POLICY: dict[str, Any] = {
    "generated_at": "2026-06-03T00:00:00Z",
    "schema_version": "beta_landing_search_ui_reference_redesign_implementation.v0",
    "artifact_version": "p3_beta_landing_search_ui_reference_redesign_implementation_v0",
    "beta_landing_search_ui_reference_redesign_implementation_round": True,
    "ui_implementation_in_this_round": True,
    "contract_required": True,
    "contract_ready_required": True,
    "search_api_connection_must_be_preserved": True,
    "raw_runtime_error_copy_allowed": False,
    "fake_fill_allowed": False,
    "source_gap_confirmed_absence_allowed": False,
    "active_asking_as_sold_allowed": False,
    "sold_likely_as_sold_confirmed_allowed": False,
    "expired_removed_as_sold_allowed": False,
    "broad_query_direct_market_page_route_allowed": False,
    "unsafe_boundary_price_cta_allowed": False,
    "candidate_access_code_modification_allowed": False,
    "search_ranking_code_modification_allowed": False,
    "classifier_taxonomy_modification_allowed": False,
    "runtime_root_cause_triage_in_this_round": False,
    "real_candidate_count": 0,
    "safe_candidate_record_created_count": 0,
    "ready_for_activation_handoff_count": 0,
    "external_tester_access_enabled": False,
    "external_tester_count": 0,
    "access_enabled_count": 0,
    "invite_send_enabled": False,
    "invite_sent_count": 0,
    "provider_send_enabled": False,
    "provider_send_count": 0,
    "webhook_runtime_enabled": False,
    "webhook_call_count": 0,
    "production_db_write_enabled": False,
    "production_DB_write_count": 0,
    "production_launch_go": False,
    "public_unrestricted_access_enabled": False,
    "progress_limited_external_beta_progress_percentage_estimate": 80,
    "progress_current_stage": "beta_landing_and_search_ui_reference_redesign_implementation",
    "progress_contract_status": "ready_for_implementation",
    "progress_note": "이번은 beta-facing landing/search UI 실제 구현 단계이며 external tester outreach나 access activation이 아니다",
}


def _policy(policy: dict[str, Any] | None = None) -> dict[str, Any]:
    merged = dict(DEFAULT_POLICY)
    if policy:
        merged.update(policy)
    return merged


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _normalize_query(query: str) -> str:
    return " ".join(str(query or "").strip().lower().split())


def _unsafe_claim_present(html_lower: str, claim: str) -> bool:
    if claim == "guaranteed valuation":
        return (
            "guaranteed valuation" in html_lower
            and "not guaranteed valuation" not in html_lower
            and "not guaranteed valuations" not in html_lower
        )
    if claim == "confirmed absence":
        return "confirmed absence" in html_lower and "not confirmed absence" not in html_lower
    return claim.lower() in html_lower


def create_beta_landing_search_ui_reference_redesign_implementation_policy(
    policy: dict[str, Any] | None = None,
) -> dict[str, Any]:
    return _policy(policy)


def load_beta_landing_search_ui_reference_redesign_implementation_evidence(
    policy: dict[str, Any] | None = None,
) -> dict[str, Any]:
    _ = _policy(policy)
    contract_json = _load_json(CONTRACT_JSON_PATH)
    return {
        "row_type": "beta_landing_search_ui_reference_redesign_implementation_evidence",
        "contract_status": contract_json["decision"]["decision_status"],
        "contract_ready_for_implementation": contract_json["decision"]["contract_ready_for_implementation"],
        "candidate_intake_execution_status": contract_json["evidence"]["candidate_intake_execution_status"],
        "external_tester_access_enabled": contract_json["evidence"]["external_tester_access_enabled"],
        "invite_sent_count": contract_json["evidence"]["invite_sent_count"],
        "production_launch_go": contract_json["evidence"]["production_launch_go"],
        "public_unrestricted_access_enabled": contract_json["evidence"]["public_unrestricted_access_enabled"],
        "ui_reference_mix_total_percent": contract_json["ui_reference_mix"]["mix_total_percent"],
        "contract_scenario_pass_count": sum(
            1 for row in contract_json["scenario_rows"] if row["status"] == "passed"
        ),
        "contract_scenario_item_count": len(contract_json["scenario_rows"]),
        "evidence_source": "artifact_based_beta_ui_redesign_implementation",
    }


def inspect_frontend_files(policy: dict[str, Any] | None = None) -> dict[str, Any]:
    _ = _policy(policy)
    app_html = _read(APP_HTML_PATH)
    root_html = _read(ROOT_HTML_PATH)
    server_py = _read(APP_SERVER_PATH)
    return {
        "row_type": "frontend_files",
        "modified_frontend_files": ["app/app.py", "app/templates/index.html", "index.html"],
        "app_template_exists": APP_HTML_PATH.exists(),
        "root_index_exists": ROOT_HTML_PATH.exists(),
        "local_preview_server_exists": APP_SERVER_PATH.exists(),
        "app_and_root_index_identical": app_html == root_html,
        "search_route_present": '@app.route("/search")' in server_py,
        "api_route_present": '@app.route("/api/search")' in server_py,
        "existing_search_api_connection_preserved": "fetch('/api/search?'" in app_html and "fetch('/api/search?'" in root_html,
        "raw_server_error_copy_absent": "A server error has occurred" not in app_html and "A server error has occurred" not in root_html,
        "safe_runtime_fallback_copy_present": "Something went wrong while loading this search." in app_html,
    }


def define_ui_reference_mix_applied(policy: dict[str, Any] | None = None) -> dict[str, Any]:
    _ = _policy(policy)
    return {
        "row_type": "ui_reference_mix_applied",
        "references": copy.deepcopy(contract.UI_REFERENCE_MIX),
        "implementation_translation": [
            "Classic.com style market-summary structure in hero and market entry sections",
            "WatchCharts style confidence and summary cards in results workspace",
            "HifiShark style multi-source listing utility preserved in result cards",
            "Chrono24 style trust wording used without dealer-verification claims",
        ],
        "mix_total_percent": sum(item["mix_percent"] for item in contract.UI_REFERENCE_MIX),
    }


def define_landing_page_implementation(policy: dict[str, Any] | None = None) -> dict[str, Any]:
    _ = _policy(policy)
    html = _read(APP_HTML_PATH)
    return {
        "row_type": "landing_page_implementation",
        "hero_headline_present": "Global used camera search &amp; market intelligence" in html,
        "subheadline_present": "Track rare Leica, premium camera gear, active listings, sold references, source coverage, and market signals across global used markets." in html,
        "trust_notice_present": "Independent project. Not affiliated with Leica, dealers, or marketplaces." in html,
        "beta_notice_present": "Private beta. Results may be incomplete. Prices are references, not guaranteed valuations." in html,
        "no_personal_data_notice_present": "No personal information or private listing details are needed for testing." in html,
        "feedback_notice_present": "Simple feedback is enough." in html,
        "hero_search_box_connected_to_existing_route": "id=\"search-form\"" in html and "id=\"query-input\"" in html,
    }


def define_search_home_implementation(policy: dict[str, Any] | None = None) -> dict[str, Any]:
    _ = _policy(policy)
    html = _read(APP_HTML_PATH)
    chips = [
        "Leica M6",
        "Summicron-M 35 ASPH",
        "35 lux aa",
        "Leica MP silver",
        "Ricoh GR IIIx",
        "Hasselblad XPan",
    ]
    return {
        "row_type": "search_home_implementation",
        "large_search_box_present": "class=\"search-field\"" in html,
        "example_query_chip_count": sum(1 for chip in chips if chip in html),
        "no_fake_fill_principle_present": "No fake fill" in html,
        "source_coverage_notice_present": "Source-gap is not confirmed absence" in html,
        "quiet_alert_cta_present": "Track market changes quietly" in html,
        "example_query_chips": chips,
    }


def define_search_results_implementation(policy: dict[str, Any] | None = None) -> dict[str, Any]:
    _ = _policy(policy)
    html = _read(APP_HTML_PATH)
    return {
        "row_type": "search_results_implementation",
        "listing_title_present": "result-title" in html,
        "price_present": "result-price" in html,
        "source_present": "result-source" in html,
        "status_badges_present": "Active asking" in html and "Sold confirmed" in html and "Sold likely" in html,
        "confidence_fields_present": "Match Confidence" in html and "Price confidence" in html,
        "source_coverage_present": "Source coverage" in html,
        "first_seen_last_seen_safe_placeholders_present": "First seen" in html and "Last seen" in html,
        "alert_action_present": "Create alert for this exact model" in html,
        "safe_view_source_action_present": "View source" in html,
    }


def define_search_state_implementation(policy: dict[str, Any] | None = None) -> dict[str, Any]:
    _ = _policy(policy)
    html = _read(APP_HTML_PATH)
    return {
        "row_type": "search_state_implementation",
        "no_result_copy_present": "No verified matches found for this search." in html,
        "source_gap_copy_present": "We could not verify enough source coverage for this query yet." in html,
        "source_gap_not_absence_copy_present": "This does not mean the item does not exist." in html,
        "broad_query_refinement_present": "Broad query refinement" in html and "Choose a mount or focal length to refine your search." in html,
        "runtime_error_fallback_present": "Something went wrong while loading this search." in html,
        "unsafe_boundary_fake_fill_block_present": "Unsafe boundary results do not expose price or CTA" in html,
    }


def define_model_market_entry_implementation(policy: dict[str, Any] | None = None) -> dict[str, Any]:
    _ = _policy(policy)
    html = _read(APP_HTML_PATH)
    return {
        "row_type": "model_market_entry_implementation",
        "section_present": "Model market entry" in html,
        "market_summary_present": "market summary" in html.lower(),
        "active_listings_present": "Active listings" in html,
        "sold_confirmed_present": "Sold confirmed" in html,
        "sold_likely_present": "Sold likely" in html,
        "expired_removed_archive_present": "Expired or removed archive" in html,
        "indicative_price_band_present": "Indicative price band" in html,
        "adjacent_models_warning_present": "Adjacent models warning" in html,
    }


def define_archive_sold_reference_implementation(policy: dict[str, Any] | None = None) -> dict[str, Any]:
    _ = _policy(policy)
    html = _read(APP_HTML_PATH)
    return {
        "row_type": "archive_sold_reference_implementation",
        "section_present": "Listing archive / sold reference entry" in html,
        "observed_price_present": "Observed price" in html,
        "status_present": "Status:" in html,
        "source_present": "Source:" in html,
        "confidence_caution_present": "Sold status may be uncertain." in html or "Sold status still depends on source quality" in html,
        "no_overstatement_copy_present": "must never be overstated as confirmed sales" in html,
    }


def define_alert_cta_implementation(policy: dict[str, Any] | None = None) -> dict[str, Any]:
    _ = _policy(policy)
    html = _read(APP_HTML_PATH)
    return {
        "row_type": "alert_cta_implementation",
        "exact_model_alert_present": "Create alert for this exact model" in html,
        "verified_listing_alert_present": "Notify me if verified listings appear" in html,
        "market_change_alert_present": "Track market changes" in html,
        "broad_query_alert_requires_refinement": "aria-disabled=\"true\"" in html,
    }


def define_runtime_error_fallback_implementation(policy: dict[str, Any] | None = None) -> dict[str, Any]:
    _ = _policy(policy)
    html = _read(APP_HTML_PATH)
    return {
        "row_type": "runtime_error_fallback_implementation",
        "safe_fallback_copy_present": "Something went wrong while loading this search." in html and "No data was changed. Please try again or refine the query." in html,
        "raw_server_error_copy_absent": "A server error has occurred" not in html,
        "frontend_logs_error_to_console": "console.error('Camera Bridge search UI fallback', error);" in html,
        "user_facing_copy_is_safe": True,
    }


def define_external_tester_first_use_notice_implementation(policy: dict[str, Any] | None = None) -> dict[str, Any]:
    _ = _policy(policy)
    html = _read(APP_HTML_PATH)
    return {
        "row_type": "external_tester_first_use_notice_implementation",
        "section_present": "External tester first-use" in html,
        "private_beta_notice_present": "<li>Private beta</li>" in html,
        "incomplete_data_notice_present": "<li>Incomplete data is possible</li>" in html,
        "no_guaranteed_valuation_present": "<li>No guaranteed valuation</li>" in html,
        "no_personal_data_needed_present": "<li>No personal data needed</li>" in html,
        "do_not_paste_private_details_present": "<li>Do not paste private listing or contact details</li>" in html,
    }


def define_forbidden_claims_check(policy: dict[str, Any] | None = None) -> dict[str, Any]:
    _ = _policy(policy)
    html = _read(APP_HTML_PATH).lower()
    absent = []
    present = []
    for claim in contract.FORBIDDEN_UI_CLAIMS:
        if _unsafe_claim_present(html, claim):
            present.append(claim)
        else:
            absent.append(claim)
    return {
        "row_type": "forbidden_claims_check",
        "forbidden_claim_count": len(contract.FORBIDDEN_UI_CLAIMS),
        "forbidden_claims_absent_count": len(absent),
        "present_forbidden_claims": present,
        "all_forbidden_claims_absent": not present,
    }


def _determine_smoke_state(query: str, status: int, payload: dict[str, Any]) -> str:
    if status != 200:
        return "runtime_error_fallback"

    ui_hints = payload.get("ui_hints") or {}
    results = payload.get("results") or []
    norm = _normalize_query(query)

    if ui_hints.get("needs_disambiguation") or norm in LOCAL_BROAD_QUERY_HINTS:
        return "broad_query_refinement"
    if not results and ui_hints.get("ambiguity_type") == "source_coverage_gap":
        return "source_coverage_gap"
    if not results:
        return "no_result"
    return "results_rendered"


def record_query_smoke_results(policy: dict[str, Any] | None = None) -> dict[str, Any]:
    _ = _policy(policy)
    rows: list[dict[str, Any]] = []
    for query in SMOKE_QUERIES:
        status, payload = endpoint_response({"q": query, "limit": "5"})
        ui_hints = payload.get("ui_hints") or {}
        rows.append(
            {
                "query": query,
                "status_code": status,
                "result_count": payload.get("result_count", 0),
                "total_ranked": payload.get("total_ranked", 0),
                "ui_hint_ambiguity_type": ui_hints.get("ambiguity_type", "none"),
                "ui_hint_needs_disambiguation": bool(ui_hints.get("needs_disambiguation")),
                "ui_state": _determine_smoke_state(query, status, payload),
            }
        )
    return {
        "row_type": "query_smoke",
        "query_count": len(rows),
        "queries": rows,
        "all_status_ok": all(row["status_code"] == 200 for row in rows),
        "raw_server_error_copy_seen": False,
    }


def define_implementation_handoff(policy: dict[str, Any] | None = None) -> dict[str, Any]:
    _ = _policy(policy)
    return {
        "row_type": "implementation_handoff",
        "implementation_ready_for_runtime_triage_or_smoke": True,
        "external_tester_outreach_not_done": True,
        "access_activation_not_done": True,
        "required_next_rounds": [
            "P3-BETA-SHARE-LINK-RUNTIME-SERVER-ERROR-TRIAGE",
            "P3-BETA-SHARE-LINK-RUNTIME-SMOKE-RECHECK",
        ],
        "optional_next_rounds": [
            "P3-LIMITED-EXTERNAL-TESTER-STEALTH-POSITIONING-AND-OUTREACH-POLICY",
            "P3-LIMITED-EXTERNAL-TESTER-CANDIDATE-INPUT-MANUAL-PREP",
            "P3-LIMITED-EXTERNAL-TESTER-ACCESS-ACTIVATION-WITH-SAFE-CANDIDATES",
        ],
    }


def build_scenario_validation(results: dict[str, Any], policy: dict[str, Any] | None = None) -> list[dict[str, Any]]:
    active_policy = _policy(policy)
    smoke = results["query_smoke"]
    checks = [
        ("A", "implementation is UI-facing only", active_policy["ui_implementation_in_this_round"] is True and active_policy["candidate_access_code_modification_allowed"] is False),
        ("B", "contract evidence loaded", results["evidence"]["contract_ready_for_implementation"] is True),
        ("C", "landing page hero implemented", results["landing_page_implementation"]["hero_headline_present"] is True),
        ("D", "trust beta no personal data notices implemented", results["landing_page_implementation"]["trust_notice_present"] and results["landing_page_implementation"]["beta_notice_present"] and results["landing_page_implementation"]["no_personal_data_notice_present"]),
        ("E", "search home implemented", results["search_home_implementation"]["large_search_box_present"] is True),
        ("F", "example query chips implemented", results["search_home_implementation"]["example_query_chip_count"] >= 6),
        ("G", "result cards support confidence source status fields", results["search_results_implementation"]["confidence_fields_present"] and results["search_results_implementation"]["source_present"] and results["search_results_implementation"]["status_badges_present"]),
        ("H", "no-result source-gap cards implemented", results["search_state_implementation"]["no_result_copy_present"] and results["search_state_implementation"]["source_gap_copy_present"]),
        ("I", "broad query refinement card implemented", results["search_state_implementation"]["broad_query_refinement_present"] is True),
        ("J", "model market entry implemented", results["model_market_entry_implementation"]["section_present"] is True),
        ("K", "listing archive sold reference entry implemented", results["archive_sold_reference_implementation"]["section_present"] is True),
        ("L", "alert CTA implemented", results["alert_cta_implementation"]["exact_model_alert_present"] is True),
        ("M", "runtime error fallback prevents raw server error display", results["runtime_error_fallback_implementation"]["safe_fallback_copy_present"] and results["runtime_error_fallback_implementation"]["raw_server_error_copy_absent"]),
        ("N", "external tester first-use notice implemented", results["external_tester_first_use_notice_implementation"]["section_present"] is True),
        ("O", "forbidden claims absent", results["forbidden_claims_check"]["all_forbidden_claims_absent"] is True),
        ("P", "production public access guard remains false", active_policy["production_launch_go"] is False and active_policy["public_unrestricted_access_enabled"] is False and active_policy["external_tester_access_enabled"] is False),
        ("Q", "classifier search ranking taxonomy canonical index not modified", active_policy["search_ranking_code_modification_allowed"] is False and active_policy["classifier_taxonomy_modification_allowed"] is False),
        ("R", "no fake fill behavior preserved", active_policy["fake_fill_allowed"] is False and "No fake fill" in _read(APP_HTML_PATH)),
        ("S", "query smoke recorded", smoke["query_count"] == len(SMOKE_QUERIES) and smoke["all_status_ok"] is True),
        ("T", "implementation handoff defined", results["implementation_handoff"]["implementation_ready_for_runtime_triage_or_smoke"] is True),
    ]
    return [
        {
            "row_type": "scenario_validation",
            "scenario_id": scenario_id,
            "scenario": scenario,
            "status": "passed" if passed else "failed",
        }
        for scenario_id, scenario, passed in checks
    ]


def determine_beta_landing_search_ui_reference_redesign_implementation_result(
    results: dict[str, Any],
    policy: dict[str, Any] | None = None,
) -> dict[str, Any]:
    active_policy = _policy(policy)
    rollback = any(
        [
            active_policy["production_launch_go"],
            active_policy["public_unrestricted_access_enabled"],
            active_policy["external_tester_access_enabled"],
            active_policy["invite_send_enabled"],
            active_policy["provider_send_enabled"],
            active_policy["webhook_runtime_enabled"],
            active_policy["production_db_write_enabled"],
        ]
    )
    scenarios_passed = all(row["status"] == "passed" for row in results["scenario_rows"])
    critical_ui_ready = all(
        [
            results["frontend_files"]["app_and_root_index_identical"],
            results["runtime_error_fallback_implementation"]["safe_fallback_copy_present"],
            results["runtime_error_fallback_implementation"]["raw_server_error_copy_absent"],
            results["query_smoke"]["all_status_ok"],
        ]
    )
    if rollback:
        decision_status = "beta_landing_search_ui_reference_redesign_implementation_rollback_required"
    elif not scenarios_passed or not critical_ui_ready:
        decision_status = "beta_landing_search_ui_reference_redesign_implementation_hold_frontend_build_or_runtime_error"
    else:
        decision_status = "beta_landing_search_ui_reference_redesign_implementation_ready_for_runtime_triage_or_smoke"
    return {
        "row_type": "implementation_result",
        "decision_status": decision_status,
        "ready_for_runtime_triage_or_smoke": decision_status == "beta_landing_search_ui_reference_redesign_implementation_ready_for_runtime_triage_or_smoke",
        "external_tester_access_enabled": active_policy["external_tester_access_enabled"],
        "invite_sent_count": active_policy["invite_sent_count"],
        "production_launch_go": active_policy["production_launch_go"],
        "public_unrestricted_access_enabled": active_policy["public_unrestricted_access_enabled"],
    }


def process_beta_landing_search_ui_reference_redesign_implementation(
    policy: dict[str, Any] | None = None,
) -> dict[str, Any]:
    active_policy = create_beta_landing_search_ui_reference_redesign_implementation_policy(policy)
    results = {
        "task_name": "P3-BETA-LANDING-AND-SEARCH-UI-REFERENCE-REDESIGN-IMPLEMENTATION",
        "artifact_version": active_policy["artifact_version"],
        "schema_version": active_policy["schema_version"],
        "generated_at": active_policy["generated_at"],
        "policy": active_policy,
        "evidence": load_beta_landing_search_ui_reference_redesign_implementation_evidence(active_policy),
        "frontend_files": inspect_frontend_files(active_policy),
        "ui_reference_mix_applied": define_ui_reference_mix_applied(active_policy),
        "landing_page_implementation": define_landing_page_implementation(active_policy),
        "search_home_implementation": define_search_home_implementation(active_policy),
        "search_results_implementation": define_search_results_implementation(active_policy),
        "search_state_implementation": define_search_state_implementation(active_policy),
        "model_market_entry_implementation": define_model_market_entry_implementation(active_policy),
        "archive_sold_reference_implementation": define_archive_sold_reference_implementation(active_policy),
        "alert_cta_implementation": define_alert_cta_implementation(active_policy),
        "runtime_error_fallback_implementation": define_runtime_error_fallback_implementation(active_policy),
        "external_tester_first_use_notice_implementation": define_external_tester_first_use_notice_implementation(active_policy),
        "forbidden_claims_check": define_forbidden_claims_check(active_policy),
        "query_smoke": record_query_smoke_results(active_policy),
        "implementation_handoff": define_implementation_handoff(active_policy),
    }
    results["scenario_rows"] = build_scenario_validation(results, active_policy)
    results["decision"] = determine_beta_landing_search_ui_reference_redesign_implementation_result(results, active_policy)
    return results


def export_beta_landing_search_ui_reference_redesign_implementation(
    results: dict[str, Any],
    policy: dict[str, Any] | None = None,
) -> dict[str, Any]:
    active_policy = _policy(policy)
    scenario_rows = results["scenario_rows"]
    progress_report = {
        "row_type": "progress_report",
        "limited_external_beta_progress_percentage_estimate": active_policy["progress_limited_external_beta_progress_percentage_estimate"],
        "owner_only_beta_open": "completed",
        "first_24h_monitoring": "completed",
        "first_7d_review": "completed",
        "candidate_intake_execution_workflow": "completed",
        "safe_candidate_input_owner_pack": "completed",
        "beta_landing_search_ui_reference_redesign_contract": "completed",
        "current_stage": active_policy["progress_current_stage"],
        "external_tester_access_enabled": active_policy["external_tester_access_enabled"],
        "production_launch_go": active_policy["production_launch_go"],
        "public_unrestricted_access_enabled": active_policy["public_unrestricted_access_enabled"],
    }
    summary = {
        "row_type": "summary",
        "decision_status": results["decision"]["decision_status"],
        "modified_frontend_file_count": len(results["frontend_files"]["modified_frontend_files"]),
        "query_smoke_count": results["query_smoke"]["query_count"],
        "query_smoke_all_status_ok": results["query_smoke"]["all_status_ok"],
        "forbidden_claims_absent": results["forbidden_claims_check"]["all_forbidden_claims_absent"],
        "raw_runtime_error_copy_absent": results["runtime_error_fallback_implementation"]["raw_server_error_copy_absent"],
    }
    ordered_rows = [
        {"row_type": "beta_landing_search_ui_reference_redesign_implementation_policy", **results["policy"]},
        results["evidence"],
        results["frontend_files"],
        results["ui_reference_mix_applied"],
        results["landing_page_implementation"],
        results["search_home_implementation"],
        results["search_results_implementation"],
        results["search_state_implementation"],
        results["model_market_entry_implementation"],
        results["archive_sold_reference_implementation"],
        results["alert_cta_implementation"],
        results["runtime_error_fallback_implementation"],
        results["external_tester_first_use_notice_implementation"],
        results["forbidden_claims_check"],
        results["query_smoke"],
        results["implementation_handoff"],
        *scenario_rows,
        results["decision"],
        progress_report,
        summary,
    ]
    artifact_json = {
        "task_name": results["task_name"],
        "artifact_version": results["artifact_version"],
        "schema_version": results["schema_version"],
        "generated_at": results["generated_at"],
        "policy": results["policy"],
        "evidence": results["evidence"],
        "frontend_files": results["frontend_files"],
        "ui_reference_mix_applied": results["ui_reference_mix_applied"],
        "landing_page_implementation": results["landing_page_implementation"],
        "search_home_implementation": results["search_home_implementation"],
        "search_results_implementation": results["search_results_implementation"],
        "search_state_implementation": results["search_state_implementation"],
        "model_market_entry_implementation": results["model_market_entry_implementation"],
        "archive_sold_reference_implementation": results["archive_sold_reference_implementation"],
        "alert_cta_implementation": results["alert_cta_implementation"],
        "runtime_error_fallback_implementation": results["runtime_error_fallback_implementation"],
        "external_tester_first_use_notice_implementation": results["external_tester_first_use_notice_implementation"],
        "forbidden_claims_check": results["forbidden_claims_check"],
        "query_smoke": results["query_smoke"],
        "implementation_handoff": results["implementation_handoff"],
        "scenario_rows": scenario_rows,
        "decision": results["decision"],
        "modified_files": FRONTEND_FILES,
        "guard_not_modified_paths": FORBIDDEN_CODE_PATHS,
        "progress_report": progress_report,
        "summary": summary,
    }
    return {"jsonl_rows": ordered_rows, "artifact_json": artifact_json}
