# P3-PRIVATE-BETA-MARKET-PAGE-RUNBOOK

## 1. 작업명
P3-PRIVATE-BETA-MARKET-PAGE-RUNBOOK

## 2. 작업 목적
limited private beta를 실제로 열기 전 운영자가 따라야 할 절차, preflight, smoke test, rollback, monitoring, incident response, release checklist를 정리한다.

## 3. 진행률
- 기준: P3 Market Intelligence / Model Market Page private-beta operational-readiness
- 시작 전: 약 99%
- 이번 라운드 완료 후: 약 99.5%
- 증가분: +0.5%p

## 4. 구현 요약
- limited private beta를 안전하게 운영하기 위한 역할, 허용 범위, 운영 전 점검표, 모니터링, 롤백 절차를 runbook artifact로 고정했다.
- previous readiness recheck의 conditional_go_limited_private_beta 결과를 운영 절차로 연결했다.
- 실제 deployment나 feature enablement는 하지 않고, 운영 기준과 즉시 조치 규칙만 문서화했다.

## 5. Runbook scope
- 포함: operator roles, release scope, preflight, allowed route matrix, disabled feature matrix, smoke test, monitoring, rollback, incident response, feedback, post-beta review criteria, go/no-go checklist
- 제외: actual deployment, actual route/API/frontend/DB implementation, actual CTA send, production launch decision

## 6. policy
- runbook_only = True
- actual_deployment_enabled = False
- production_launch_enabled = False
- CTA_send_enabled = False
- numeric_price_display_enabled = False
- structured_data_enabled = False
- limited_private_beta_only = True

## 7. beta operator roles
- role_count = 7
- beta_owner: can_approve_go=True, can_trigger_rollback=False
- release_operator: can_approve_go=False, can_trigger_rollback=False
- QA_operator: can_approve_go=False, can_trigger_rollback=False
- data_safety_reviewer: can_approve_go=False, can_trigger_rollback=True
- SEO_safety_reviewer: can_approve_go=False, can_trigger_rollback=True
- rollback_owner: can_approve_go=False, can_trigger_rollback=True
- user_feedback_owner: can_approve_go=False, can_trigger_rollback=False

## 8. beta release scope
- scope_count = 13
- leica_noctilux_m_50_095_asph: allowed=True / route_state=exact_model_public_market_page
- leica_summilux_m_35_asph_aa: allowed=True / route_state=exact_rare_variant_public_market_page
- sigma_14_24_dg_dn_art_l_mount_source_gap: allowed=True / route_state=source_gap_public_page
- active_only_noctilux_route: allowed=True / route_state=active_only_public_page
- archive_only_noctilux_route: allowed=True / route_state=archive_only_public_page
- stale_noctilux_route: allowed=True / route_state=stale_data_safe_route
- leica_m6_future_candidate: allowed=False / route_state=exact_model_public_market_page
- apo_summicron_m_50_future_candidate: allowed=False / route_state=exact_model_public_market_page
- broad_summicron_market_page: allowed=False / route_state=broad_query_refinement_route
- unsafe_boundary_price_page: allowed=False / route_state=unsafe_boundary_review_route
- unsupported_model_market_page: allowed=False / route_state=unsupported_model_route
- privacy_blocked_market_page: allowed=False / route_state=privacy_blocked_route
- db_unavailable_market_page: allowed=False / route_state=db_unavailable_safe_route

## 9. preflight checklist
- preflight_check_count = 20
- readiness_recheck_decision: failure_action=hold_for_fix / owner=beta_owner
- open_launch_blockers_zero: failure_action=hold_for_fix / owner=beta_owner
- warning_list_acknowledged: failure_action=hold_for_fix / owner=beta_owner
- allowed_model_list_confirmed: failure_action=hold_for_fix / owner=release_operator
- blocked_route_list_confirmed: failure_action=hold_for_fix / owner=release_operator
- cta_send_disabled: failure_action=hold_for_fix / owner=data_safety_reviewer
- numeric_price_disabled: failure_action=hold_for_fix / owner=beta_owner
- structured_data_disabled: failure_action=hold_for_fix / owner=SEO_safety_reviewer
- source_gap_noindex: failure_action=hold_for_fix / owner=SEO_safety_reviewer
- broad_refinement_only: failure_action=hold_for_fix / owner=SEO_safety_reviewer
- unsafe_boundary_hidden: failure_action=hold_for_fix / owner=data_safety_reviewer
- raw_response_check_passed: failure_action=rollback / owner=data_safety_reviewer
- seo_claim_check_passed: failure_action=rollback / owner=SEO_safety_reviewer
- robots_policy_check_passed: failure_action=hold_for_fix / owner=SEO_safety_reviewer
- privacy_fail_close_passed: failure_action=rollback / owner=data_safety_reviewer
- db_unavailable_safe_fallback_passed: failure_action=hold_for_fix / owner=data_safety_reviewer
- rollback_owner_assigned: failure_action=hold_for_fix / owner=beta_owner
- smoke_test_scheduled: failure_action=hold_for_smoke_test / owner=QA_operator
- feedback_channel_ready: failure_action=hold_for_fix / owner=user_feedback_owner
- incident_log_ready: failure_action=hold_for_fix / owner=QA_operator

## 10. allowed route matrix
- route_state_count = 13
- exact_model_public_market_page: beta_allowed=True / robots=index,follow / CTA=visible_candidate_send_disabled
- exact_rare_variant_public_market_page: beta_allowed=True / robots=index,follow / CTA=visible_candidate_send_disabled
- source_gap_public_page: beta_allowed=True / robots=noindex,follow / CTA=source_gap_candidate_only_send_disabled
- active_only_public_page: beta_allowed=True / robots=index,follow / CTA=visible_candidate_send_disabled
- archive_only_public_page: beta_allowed=True / robots=index,follow / CTA=visible_candidate_send_disabled
- insufficient_sold_history_public_page: beta_allowed=True / robots=index,follow / CTA=visible_candidate_send_disabled
- stale_data_safe_route: beta_allowed=True / robots=index,follow / CTA=visible_candidate_send_disabled
- broad_query_refinement_route: beta_allowed=False / robots=noindex,follow / CTA=no_fast_alert
- unsafe_boundary_review_route: beta_allowed=False / robots=noindex,follow / CTA=disabled
- unsupported_model_route: beta_allowed=False / robots=noindex,follow / CTA=disabled
- privacy_blocked_route: beta_allowed=False / robots=noindex,nofollow / CTA=disabled
- db_unavailable_safe_route: beta_allowed=False / robots=noindex,nofollow / CTA=disabled
- error_safe_fallback_route: beta_allowed=False / robots=noindex,nofollow / CTA=disabled

## 11. disabled feature matrix
- disabled_feature_count = 11
- numeric_price_display: disabled_for_beta=True
- structured_data: disabled_for_beta=True
- CTA_email_send: disabled_for_beta=True
- smart_deal: disabled_for_beta=True
- CSV_export: disabled_for_beta=True
- dealer_visibility: disabled_for_beta=True
- unsupported_market_page: disabled_for_beta=True
- broad_query_market_page: disabled_for_beta=True
- unsafe_boundary_price_page: disabled_for_beta=True
- raw_listing_links: disabled_for_beta=True
- user_specific_public_response: disabled_for_beta=True

## 12. smoke test plan
- smoke_test_count = 16
- exact_noctilux_route_loads: blocker_if_failed=True
- rare_variant_route_loads: blocker_if_failed=True
- source_gap_route_loads: blocker_if_failed=True
- broad_query_refines: blocker_if_failed=True
- unsafe_boundary_hidden: blocker_if_failed=True
- unsupported_fallback: blocker_if_failed=True
- privacy_fail_close: blocker_if_failed=True
- db_unavailable_safe_fallback: blocker_if_failed=True
- seo_claim_scanner: blocker_if_failed=True
- raw_field_injection_block: blocker_if_failed=True
- cta_aggregate_only: blocker_if_failed=True
- robots_by_route_state: blocker_if_failed=True
- structured_data_disabled: blocker_if_failed=True
- analytics_safe_fields: blocker_if_failed=True
- rollback_trigger_simulation: blocker_if_failed=True
- feedback_capture_ready: blocker_if_failed=False

## 13. monitoring plan
- monitoring_signal_count = 15
- public_response_blocked_policy_violation_count: threshold=>=1
- raw_field_leak_attempt_count: threshold=>=1
- source_gap_page_view_count: threshold=trend spike
- source_gap_overclaim_incident_count: threshold=>=1
- broad_refinement_route_count: threshold=unexpected drop
- unsafe_boundary_route_count: threshold=unexpected spike
- SEO_claim_violation_count: threshold=>=1
- CTA_click_visible_candidate_count: threshold=trend spike
- CTA_send_attempt_count: threshold=>=1
- DB_unavailable_fallback_count: threshold=sustained increase
- privacy_block_count: threshold=unexpected spike
- rollback_trigger_count: threshold=>=1 live incident
- user_feedback_count: threshold=spike
- false_positive_report_count: threshold=>=1 severe report
- false_negative_report_count: threshold=>=1 severe report

## 14. rollback plan
- rollback_condition_count = 11
- raw_field_leak: severity=P0 / owner=rollback_owner
- source_gap_overclaim: severity=P1 / owner=rollback_owner
- seo_prohibited_claim: severity=P1 / owner=rollback_owner
- cta_email_exposure: severity=P0 / owner=rollback_owner
- fake_fill_route: severity=P1 / owner=rollback_owner
- price_overclaim: severity=P1 / owner=rollback_owner
- duplicate_sample_inflation: severity=P1 / owner=rollback_owner
- db_fallback_fake_listing: severity=P1 / owner=rollback_owner
- privacy_failure_not_blocked: severity=P0 / owner=rollback_owner
- unsafe_boundary_price_cta_exposure: severity=P1 / owner=rollback_owner
- broad_query_direct_market_page_exposure: severity=P1 / owner=rollback_owner

## 15. incident response plan
- incident_step_count = 8
- P0: raw data leak / rollback_required=True
- P0: CTA/user email leak / rollback_required=True
- P1: fake-fill / source-gap overclaim / rollback_required=True
- P1: SEO prohibited claim indexed / rollback_required=True
- P1: unsafe boundary price/CTA exposed / rollback_required=True
- P2: stale/freshness warning missing / rollback_required=False
- P2: route fallback mismatch / rollback_required=False
- P3: copy/UI issue / rollback_required=False

## 16. beta feedback plan
- feedback_category_count = 9
- wrong_model_match: owner=user_feedback_owner
- missing_source: owner=user_feedback_owner
- source_gap_confusing: owner=user_feedback_owner
- price_confidence_confusing: owner=user_feedback_owner
- alert_cta_confusing: owner=user_feedback_owner
- page_copy_unclear: owner=user_feedback_owner
- route_seo_issue: owner=SEO_safety_reviewer
- mobile_layout_issue: owner=QA_operator
- trust_disclaimer_issue: owner=beta_owner

## 17. post-beta review criteria
- promotion_criteria_count = 11
- hold_criteria_count = 7

## 18. operator go/no-go checklist
- decision_options = limited_private_beta_open, hold_for_smoke_test, hold_for_fix, rollback
- all preflight required checks pass -> limited_private_beta_open
- smoke test not run -> hold_for_smoke_test
- any rollback condition active -> rollback
- any blocker open -> hold_for_fix
- warnings alone do not block if disclosures exist

## 19. scenario validation 결과
- pass = 15/15
- A. policy forbids actual deployment: passed
- B. operator roles exist: passed
- C. release scope matches recheck: passed
- D. blocked routes remain blocked: passed
- E. preflight checklist complete: passed
- F. disabled features complete: passed
- G. smoke test plan complete: passed
- H. monitoring plan complete: passed
- I. rollback plan complete: passed
- J. incident response levels complete: passed
- K. feedback plan complete: passed
- L. post-beta criteria complete: passed
- M. operator go/no-go checklist works: passed
- N. production launch guard: passed
- O. progress report: passed

## 20. production launch 미승인 guard
- 이번 runbook은 limited private beta 운영 문서다.
- production launch go를 선언하지 않는다.

## 21. actual route/API/frontend/DB 미구현 guard
- actual beta deployment 없음
- actual route/page/component 추가 구현 없음
- actual API response/runtime 없음
- actual DB query/runtime wiring 없음
- actual CTA send runtime 없음

## 22. output JSON / production code 미수정 여부
- 이번 라운드는 runbook artifact만 생성한다.
- production runtime surface, taxonomy seed, canonical index, raw data, search index, output JSON production surface는 수정하지 않는다.

## 23. 테스트 결과
- scenario_pass = 15/15
- jsonl_row_count = 143

## 24. 남은 위험
- smoke test 실행 전에는 open으로 간주하지 않는다.
- CTA send와 production DB wiring은 여전히 별도 runtime 검증이 필요하다.
- archive DB implementation pending 상태는 운영 범위를 제한하는 경고로 남아 있다.

## 25. 다음 backlog 후보
- P3-MODEL-MARKET-PAGE-BETA-SMOKE-TEST
- P3-EXPIRED-SOLD-LISTING-ARCHIVE-DB-IMPLEMENTATION
- P3-DEALER-LEAD-SIGNAL-CONTRACT
- P3-CTA-EMAIL-VERIFICATION-RUNTIME-CHECK
- P3-PRIVATE-BETA-FEEDBACK-TRIAGE-CONTRACT

