# P3-MODEL-MARKET-PAGE-BETA-SMOKE-TEST

## 1. 작업명
P3-MODEL-MARKET-PAGE-BETA-SMOKE-TEST

## 2. 작업 목적
runbook의 smoke test plan을 local preview 기준으로 실행해 limited private beta open 직전 검증 artifact를 만든다.

## 3. 진행률
- 기준: P3 Market Intelligence / Model Market Page limited private beta operational-readiness
- 시작 전: 약 99.5%
- 이번 라운드 완료 후: 약 99.8%
- 증가분: +0.3%p

## 4. 구현 요약
- runbook smoke plan과 public route preview를 연결해 local smoke artifact를 생성했다.
- allowed route는 예상 상태로 열리는지, blocked route는 market page로 열리지 않는지, raw/SEO/CTA/robots/structured-data guard가 유지되는지 확인했다.
- smoke test 결과로 limited private beta open recommendation만 계산했고, production launch go는 하지 않았다.

## 5. Smoke test scope
- 포함: route preview, response safety, SEO claim scanner, robots matrix, CTA aggregate-only, structured data disabled, analytics safety, rollback simulation, feedback capture readiness
- 제외: actual deployment, actual API/frontend/DB wiring, actual CTA send, production launch decision

## 6. policy
- smoke_test_only = True
- actual_deployment_enabled = False
- actual_cta_send_enabled = False
- production_launch_enabled = False
- numeric_price_display_enabled = False
- structured_data_enabled = False

## 7. runbook smoke plan baseline
- baseline_count = 16
- fallback_used = False
- exact_noctilux_route_loads: exact Noctilux route
- rare_variant_route_loads: 35 lux AA route
- source_gap_route_loads: Sigma source-gap route
- broad_query_refines: broad Summicron query
- unsafe_boundary_hidden: unsafe boundary route
- unsupported_fallback: unsupported route
- privacy_fail_close: privacy blocked route
- db_unavailable_safe_fallback: DB unavailable route
- seo_claim_scanner: SEO prohibited claim scanner
- raw_field_injection_block: injected raw field block
- cta_aggregate_only: CTA aggregate-only/no send
- robots_by_route_state: robots policy by route state
- structured_data_disabled: structured data disabled
- analytics_safe_fields: analytics safe fields only
- rollback_trigger_simulation: rollback trigger simulation
- feedback_capture_ready: feedback capture ready

## 8. smoke test cases
- case_count = 19
- A: route / /camera-bridge/models/leica-noctilux-m-50mm-f095-asph
- B: route / /camera-bridge/models/leica-summilux-m-35mm-f14-asph-aa
- C: route / /camera-bridge/source-gap/sigma-14-24mm-dg-dn-art-l-mount
- D: route / /camera-bridge/search/summicron
- E: route / /camera-bridge/market/sl-14-24-vs-sigma-14-24-boundary
- F: route / /camera-bridge/unsupported/unknown-rare-lens
- G: route / /camera-bridge/models/leica-noctilux-m-50mm-f095-asph-privacy-blocked
- H: route / /camera-bridge/models/leica-noctilux-m-50mm-f095-asph-db-unavailable
- I: route / stale + active-only + archive-only route checks
- J: response_safety / raw/email/provider injection block
- K: seo / SEO prohibited claim injection
- L: robots / robots matrix check
- M: cta / CTA aggregate-only check
- N: structured_data / structured data disabled
- O: analytics / analytics safe fields
- P: rollback / rollback trigger simulation
- Q: feedback / feedback capture ready

## 9. route smoke result
- A: pass / {'route_state': 'exact_model_public_market_page', 'status_code_preview': 200, 'robots_hint': 'index,follow', 'page_status': 'exact_model_bundle_ready', 'visible_cta_ids': ['watch_this_model', 'rare_new_listing_alert', 'target_price_watch'], 'price_widget_state': 'full_price_guide_candidate'}
- B: pass / {'route_state': 'exact_rare_variant_public_market_page', 'status_code_preview': 200, 'robots_hint': 'index,follow', 'page_status': 'rare_variant_limited', 'visible_cta_ids': ['watch_this_exact_variant', 'rare_new_listing_alert', 'target_price_watch'], 'price_widget_state': 'insufficient_sold_history'}
- C: pass / {'route_state': 'source_gap_public_page', 'status_code_preview': 200, 'robots_hint': 'noindex,follow', 'page_status': 'source_gap', 'visible_cta_ids': ['source_gap_alert', 'request_source'], 'price_widget_state': 'source_gap_no_price_guide'}
- D: pass / {'route_state': 'broad_query_refinement_route', 'status_code_preview': 302, 'robots_hint': 'noindex,follow', 'page_status': 'refinement_required', 'visible_cta_ids': [], 'price_widget_state': 'refinement_required'}
- E: pass / {'route_state': 'unsafe_boundary_review_route', 'status_code_preview': 200, 'robots_hint': 'noindex,follow', 'page_status': 'unsafe_boundary', 'visible_cta_ids': [], 'price_widget_state': 'unsafe_boundary_no_price_guide'}
- F: pass / {'route_state': 'unsupported_model_route', 'status_code_preview': 404, 'robots_hint': 'noindex,follow', 'page_status': 'unsupported', 'visible_cta_ids': [], 'price_widget_state': 'model_not_supported_no_price_guide'}
- G: pass / {'route_state': 'privacy_blocked_route', 'status_code_preview': 403, 'robots_hint': 'noindex,nofollow', 'page_status': 'privacy_blocked', 'visible_cta_ids': [], 'price_widget_state': 'model_not_supported_no_price_guide'}
- H: pass / {'route_state': 'db_unavailable_safe_route', 'status_code_preview': 503, 'robots_hint': 'noindex,nofollow', 'page_status': 'db_unavailable', 'visible_cta_ids': [], 'price_widget_state': 'model_not_supported_no_price_guide'}
- I: warning / {'stale_warning': True, 'active_only_numeric_price': False, 'archive_only_active_count': 0}

## 10. response safety smoke result
- J: pass / {'first_blocked_fields': ['listing_url', 'raw_html', 'raw_url'], 'second_blocked_fields': ['provider_payload', 'user_email', 'webhook_body'], 'fail_closed': True}

## 11. SEO smoke result
- K: pass / {'seo_status': 'blocked_policy_violation', 'blocked_claims': ['all sources', 'guaranteed price', 'investment advice', 'official leica']}

## 12. robots smoke result
- L: pass / matrix_match=True

## 13. CTA smoke result
- M: pass / send_disabled=True

## 14. structured data smoke result
- N: pass / {'structured_data_enabled': False, 'structured_data_status': 'blocked_policy_violation', 'price_values_present': False, 'raw_links_present': False, 'seller_info_present': False}

## 15. analytics smoke result
- O: pass / {'event_name': 'model_page_view', 'route_state': 'exact_model_public_market_page', 'canonical_model_id': 'leica_noctilux_m_50_095_asph', 'model_slug': 'leica-noctilux-m-50mm-f095-asph', 'raw_url_present': False, 'raw_email_present': False, 'provider_payload_present': False, 'session_id_present': False}

## 16. rollback simulation result
- P: pass / action_generated=True

## 17. feedback capture check
- Q: pass / feedback_ready=True

## 18. smoke test summary
- total_tests = 17
- pass_count = 16
- warning_count = 1
- fail_count = 0
- blocked_count = 0
- blocker_fail_count = 0
- rollback_trigger_count = 0

## 19. limited beta open recommendation
- recommendation = limited_private_beta_open_recommended
- limited_beta_open_allowed = True
- production_launch_go = False
- actual_cta_send_enabled = False
- numeric_price_display_enabled = False
- structured_data_enabled = False

## 20. production launch 미승인 guard
- smoke test pass는 production go가 아니다.
- recommendation은 limited private beta open recommendation에만 쓴다.

## 21. actual deployment/API/frontend/DB 미구현 guard
- actual deployment 없음
- actual route/API/frontend runtime 추가 구현 없음
- actual DB production wiring 없음
- actual CTA send runtime 없음

## 22. output JSON / production code 미수정 여부
- 이번 라운드는 smoke test artifact만 생성한다.
- production runtime surface, taxonomy seed, canonical index, raw data, search index, output JSON production surface는 수정하지 않는다.

## 23. 테스트 결과
- scenario_pass = 19/19
- jsonl_row_count = 78

## 24. 남은 위험
- CTA send runtime은 여전히 disabled 상태라 별도 verification check가 필요하다.
- actual production DB wiring과 archive DB implementation은 아직 smoke test 범위 밖이다.
- limited beta open 전 operator signoff와 runbook preflight는 여전히 필요하다.

## 25. 다음 backlog 후보
- P3-EXPIRED-SOLD-LISTING-ARCHIVE-DB-IMPLEMENTATION
- P3-PRIVATE-BETA-FEEDBACK-TRIAGE-CONTRACT
- P3-CTA-EMAIL-VERIFICATION-RUNTIME-CHECK
- P3-DEALER-LEAD-SIGNAL-CONTRACT
- P3-LIMITED-BETA-OPEN-CANDIDATE-HANDOFF

