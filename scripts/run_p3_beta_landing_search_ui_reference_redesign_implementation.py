from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import beta_landing_search_ui_reference_redesign_implementation as implementation


MD_PATH = ROOT / "data/admin/p3_beta_landing_search_ui_reference_redesign_implementation_v0.md"
JSONL_PATH = ROOT / "data/admin/p3_beta_landing_search_ui_reference_redesign_implementation_v0.jsonl"
JSON_PATH = ROOT / "data/admin/beta_landing_search_ui_reference_redesign_implementation_v0.json"


def _write_json(path: Path, payload: dict) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _write_jsonl(path: Path, rows: list[dict]) -> None:
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")


def _build_report(results: dict, exported: dict) -> str:
    evidence = results["evidence"]
    frontend = results["frontend_files"]
    landing = results["landing_page_implementation"]
    home = results["search_home_implementation"]
    search_results = results["search_results_implementation"]
    states = results["search_state_implementation"]
    market = results["model_market_entry_implementation"]
    archive = results["archive_sold_reference_implementation"]
    alert = results["alert_cta_implementation"]
    runtime = results["runtime_error_fallback_implementation"]
    first_use = results["external_tester_first_use_notice_implementation"]
    forbidden = results["forbidden_claims_check"]
    smoke = results["query_smoke"]
    handoff = results["implementation_handoff"]
    scenario_rows = results["scenario_rows"]
    pass_count = sum(1 for row in scenario_rows if row["status"] == "passed")
    policy = results["policy"]

    lines = [
        "# P3-BETA-LANDING-AND-SEARCH-UI-REFERENCE-REDESIGN-IMPLEMENTATION",
        "",
        "## 1. 작업명",
        results["task_name"],
        "",
        "## 2. 작업 목적",
        "Contract에서 정의한 beta-facing landing/search 방향을 실제 UI에 반영하고, 외부 테스터 첫인상에서 신뢰감 있는 market intelligence tool로 보이게 만든다.",
        "",
        "## 3. 현재 판정",
        "- P3-BETA-LANDING-AND-SEARCH-UI-REFERENCE-REDESIGN-CONTRACT는 정상 완료 상태를 evidence로 로드했다.",
        f"- decision_status = {results['decision']['decision_status']}",
        "- external tester outreach / access activation / production launch는 이번 라운드에서도 하지 않았다.",
        "",
        "## 진행률/상태",
        f"- Limited External Beta 진행률 = 약 {policy['progress_limited_external_beta_progress_percentage_estimate']}%",
        f"- beta landing/search UI reference redesign contract = {evidence['contract_status']}",
        f"- external_tester_access_enabled = {policy['external_tester_access_enabled']}",
        f"- invite_sent_count = {policy['invite_sent_count']}",
        f"- production_launch_go = {policy['production_launch_go']}",
        f"- public_unrestricted_access_enabled = {policy['public_unrestricted_access_enabled']}",
        "",
        "## 4. 구현 요약",
        "- beta landing hero, search home, result workspace, state cards, market entry, archive section, and first-use notice를 새 구조로 반영했다.",
        "- broad query refinement UI를 backend ui_hints와 frontend 안전 fallback 양쪽으로 지원했다.",
        "- runtime failure 시 raw server error 대신 안전한 fallback card를 보여주도록 프론트엔드 copy를 고정했다.",
        "",
        "## 5. 실제 수정한 frontend 파일",
    ]
    for path in frontend["modified_frontend_files"]:
        lines.append(f"- {path}")
    lines.extend(
        [
            "",
            "## 6. UI reference mix 반영 내용",
            "- Classic.com 60%: market summary, model-market entry, structured metric cards",
            "- WatchCharts 25%: confidence-oriented copy, clean data cards, restrained summary strip",
            "- HifiShark 10%: multi-source listing utility and archive reference framing",
            "- Chrono24 5%: calm trust/safety wording without dealer-verification claims",
            "",
            "## 7. landing page 구현 내용",
            f"- hero_headline_present = {landing['hero_headline_present']}",
            f"- subheadline_present = {landing['subheadline_present']}",
            f"- trust_notice_present = {landing['trust_notice_present']}",
            f"- beta_notice_present = {landing['beta_notice_present']}",
            f"- no_personal_data_notice_present = {landing['no_personal_data_notice_present']}",
            f"- feedback_notice_present = {landing['feedback_notice_present']}",
            "",
            "## 8. search home 구현 내용",
            f"- large_search_box_present = {home['large_search_box_present']}",
            f"- example_query_chip_count = {home['example_query_chip_count']}",
            f"- no_fake_fill_principle_present = {home['no_fake_fill_principle_present']}",
            f"- source_coverage_notice_present = {home['source_coverage_notice_present']}",
            f"- quiet_alert_cta_present = {home['quiet_alert_cta_present']}",
            "",
            "## 9. search results 구현 내용",
            f"- listing_title_present = {search_results['listing_title_present']}",
            f"- price_present = {search_results['price_present']}",
            f"- source_present = {search_results['source_present']}",
            f"- status_badges_present = {search_results['status_badges_present']}",
            f"- confidence_fields_present = {search_results['confidence_fields_present']}",
            f"- source_coverage_present = {search_results['source_coverage_present']}",
            "",
            "## 10. no-result/source-gap 구현 내용",
            f"- no_result_copy_present = {states['no_result_copy_present']}",
            f"- source_gap_copy_present = {states['source_gap_copy_present']}",
            f"- source_gap_not_absence_copy_present = {states['source_gap_not_absence_copy_present']}",
            "",
            "## 11. broad query refinement 구현 내용",
            f"- broad_query_refinement_present = {states['broad_query_refinement_present']}",
            "- frontend local fallback also covers representative broad queries such as `leica lens` when backend ui_hints are not explicit.",
            "",
            "## 12. model market entry 구현 내용",
            f"- section_present = {market['section_present']}",
            f"- active_listings_present = {market['active_listings_present']}",
            f"- sold_confirmed_present = {market['sold_confirmed_present']}",
            f"- sold_likely_present = {market['sold_likely_present']}",
            f"- indicative_price_band_present = {market['indicative_price_band_present']}",
            "",
            "## 13. archive/sold reference entry 구현 내용",
            f"- section_present = {archive['section_present']}",
            f"- observed_price_present = {archive['observed_price_present']}",
            f"- confidence_caution_present = {archive['confidence_caution_present']}",
            f"- no_overstatement_copy_present = {archive['no_overstatement_copy_present']}",
            "",
            "## 14. alert CTA 구현 내용",
            f"- exact_model_alert_present = {alert['exact_model_alert_present']}",
            f"- verified_listing_alert_present = {alert['verified_listing_alert_present']}",
            f"- market_change_alert_present = {alert['market_change_alert_present']}",
            f"- broad_query_alert_requires_refinement = {alert['broad_query_alert_requires_refinement']}",
            "",
            "## 15. runtime error fallback 구현 내용",
            f"- safe_fallback_copy_present = {runtime['safe_fallback_copy_present']}",
            f"- raw_server_error_copy_absent = {runtime['raw_server_error_copy_absent']}",
            f"- frontend_logs_error_to_console = {runtime['frontend_logs_error_to_console']}",
            "",
            "## 16. external tester first-use notice 구현 내용",
            f"- section_present = {first_use['section_present']}",
            f"- private_beta_notice_present = {first_use['private_beta_notice_present']}",
            f"- incomplete_data_notice_present = {first_use['incomplete_data_notice_present']}",
            f"- no_guaranteed_valuation_present = {first_use['no_guaranteed_valuation_present']}",
            f"- no_personal_data_needed_present = {first_use['no_personal_data_needed_present']}",
            "",
            "## 17. forbidden claims 방지 확인",
            f"- all_forbidden_claims_absent = {forbidden['all_forbidden_claims_absent']}",
            f"- present_forbidden_claims = {forbidden['present_forbidden_claims']}",
            "",
            "## 18. production/public/access guard",
            f"- production_launch_go = {policy['production_launch_go']}",
            f"- public_unrestricted_access_enabled = {policy['public_unrestricted_access_enabled']}",
            f"- external_tester_access_enabled = {policy['external_tester_access_enabled']}",
            f"- invite_sent_count = {policy['invite_sent_count']}",
            "",
            "## 19. search/classifier/taxonomy 미수정 확인",
        ]
    )
    for path in exported["artifact_json"]["guard_not_modified_paths"]:
        lines.append(f"- guarded untouched path = {path}")
    lines.extend(
        [
            "",
            "## 20. query smoke 결과",
        ]
    )
    for row in smoke["queries"]:
        lines.append(
            f"- {row['query']} | status={row['status_code']} | total_ranked={row['total_ranked']} | ui_state={row['ui_state']} | ambiguity={row['ui_hint_ambiguity_type']}"
        )
    lines.extend(
        [
            "",
            "## 21. 테스트 결과",
            "- `package.json`이 없어 `npm test`, `npm run lint`, `npm run build`는 실행 대상이 아니었다.",
            "",
            "## 22. 생성 보고서 경로",
            f"- {MD_PATH}",
            f"- {JSONL_PATH}",
            f"- {JSON_PATH}",
            "",
            "## 23. 다음 backlog 후보",
        ]
    )
    for item in handoff["required_next_rounds"]:
        lines.append(f"- {item}")
    for item in handoff["optional_next_rounds"]:
        lines.append(f"- {item}")
    lines.extend(
        [
            "",
            "## scenario validation",
            f"- passed = {pass_count}/{len(scenario_rows)}",
        ]
    )
    for row in scenario_rows:
        lines.append(f"- {row['scenario_id']}. {row['scenario']} = {row['status']}")
    return "\n".join(lines) + "\n"


def main() -> None:
    results = implementation.process_beta_landing_search_ui_reference_redesign_implementation()
    exported = implementation.export_beta_landing_search_ui_reference_redesign_implementation(results)
    report = _build_report(results, exported)
    _write_json(JSON_PATH, exported["artifact_json"])
    _write_jsonl(JSONL_PATH, exported["jsonl_rows"])
    MD_PATH.write_text(report, encoding="utf-8")
    print(results["decision"]["decision_status"])


if __name__ == "__main__":
    main()
