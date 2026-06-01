# P3-MODEL-MARKET-PAGE-DATA-ADAPTER-DB-INTEGRATION-CONTRACT

## 1. 작업명
P3-MODEL-MARKET-PAGE-DATA-ADAPTER-DB-INTEGRATION-CONTRACT

## 2. 작업 목적
Model Market Page Data Adapter가 local preview에서 DB-backed read adapter로 넘어갈 때의 safe read boundary를 계약으로 정의한다.

## 3. 진행률
- 기준: P3 Market Intelligence / Model Market Page preview stack
- 시작 전: 약 78%
- 이번 라운드 완료 후: 약 83%
- 증가분: +5%p

## 4. 구현 요약
- DB domain, read model, safe/blocked field, join, freshness, lineage, price-guide input, CTA aggregate, fallback 경계를 정의했다.
- raw URL/HTML/email/provider payload/webhook body가 public Market Page read model로 흐르지 않도록 고정했다.
- 실제 DB connection/query/migration/ORM 구현은 만들지 않았다.

## 5. DB integration contract scope
- 포함: read-only projection boundary, join keys, privacy boundary, fallback contract, progress report.
- 제외: DB schema/migration, DB query, ORM, API/frontend implementation, production adapter runtime.

## 6. policy
- contract_only = True
- actual_db_enabled = False
- db_query_enabled = False
- db_migration_enabled = False
- production_adapter_enabled = False
- public_page_safe_fields_only = True

## 7. DB domain contract
- canonical_model_domain: read_mode=projection_only / public_safe=True
- listing_observation_domain: read_mode=projection_only / public_safe=True
- source_change_detection_domain: read_mode=projection_only / public_safe=True
- archive_listing_domain: read_mode=projection_only / public_safe=True
- archive_price_snapshot_domain: read_mode=projection_only / public_safe=True
- archive_lineage_domain: read_mode=projection_only / public_safe=True
- price_guide_input_domain: read_mode=projection_only / public_safe=True
- source_coverage_domain: read_mode=projection_only / public_safe=True
- source_freshness_domain: read_mode=projection_only / public_safe=True
- alert_watch_target_domain: read_mode=aggregate_only / public_safe=True
- preference_profile_domain: read_mode=aggregate_only / public_safe=True
- delivery_safety_domain: read_mode=aggregate_only / public_safe=True
- manual_review_domain: read_mode=projection_only / public_safe=True
- frontend_state_cache_domain: read_mode=projection_only / public_safe=True

## 8. read model contract
- market_page_model_identity_read: sources=canonical_model_domain -> model_identity_summary
- active_listing_lane_read: sources=listing_observation_domain, source_change_detection_domain -> active_listing_lanes
- archive_lane_read: sources=archive_listing_domain, archive_price_snapshot_domain, archive_lineage_domain -> archive_listing_lanes
- price_guide_input_read: sources=price_guide_input_domain, archive_lineage_domain, source_freshness_domain -> price_guide_input_bundle
- source_coverage_read: sources=source_coverage_domain -> source_coverage_summary
- source_freshness_read: sources=source_freshness_domain, source_change_detection_domain -> source_freshness_summary
- lineage_exclusion_read: sources=archive_lineage_domain -> lineage_exclusion_summary
- confidence_state_read: sources=frontend_state_cache_domain, price_guide_input_domain -> confidence_state
- cta_eligibility_read: sources=alert_watch_target_domain, preference_profile_domain, delivery_safety_domain -> alert_cta_eligibility
- frontend_state_read: sources=frontend_state_cache_domain -> frontend_state
- error_fallback_read: sources=frontend_state_cache_domain, manual_review_domain -> error_fallback_state

## 9. safe / blocked field policy
- safe_field_count = 34
- blocked_field_count = 21

## 10. join contract
- join::canonical_to_listing: keys=canonical_model_id / blocked=raw_url, email
- join::canonical_to_archive: keys=canonical_model_id / blocked=raw_url, email
- join::archive_to_price: keys=archive_record_id / blocked=raw_url, raw_html
- join::archive_to_lineage: keys=archive_record_id, lineage_key / blocked=raw_url, email
- join::source_to_coverage: keys=source_id / blocked=raw_url, email
- join::source_to_freshness: keys=source_id / blocked=raw_url, email
- join::canonical_to_price_guide: keys=canonical_model_id / blocked=raw_url, email
- join::canonical_to_frontend_state: keys=canonical_model_id / blocked=raw_url, email
- join::canonical_to_alert_aggregate: keys=canonical_model_id, watch_target_id_hash / blocked=email, recipient_email
- join::canonical_to_manual_review: keys=canonical_model_id / blocked=raw_url, email

## 11. read adapter boundary
- 1. resolve canonical model target: query target -> canonical resolution state
- 2. fetch safe model identity projection: canonical_model_id -> model identity projection
- 3. fetch active listing lane projection: canonical_model_id -> active listing lane rows
- 4. fetch archive lane projection: canonical_model_id -> archive lane rows
- 5. fetch price guide input projection: canonical_model_id -> strong/weak/excluded projections
- 6. fetch source coverage/freshness projection: source_id set -> coverage + freshness rows
- 7. fetch manual review/boundary state projection: canonical_model_id -> manual review state
- 8. fetch CTA eligibility aggregate: canonical_model_id -> CTA aggregate
- 9. assemble MarketPageDataBundle: safe projections -> bundle contract object
- 10. map to frontend view model: MarketPageDataBundle -> frontend view model

## 12. freshness / staleness contract
- stale_warning_days=180 / source_coverage_stale_after_days=30

## 13. lineage / duplicate exclusion contract
- same_listing_lineage: double_count_allowed=False
- likely_same_listing_lineage: double_count_allowed=False
- review_only_no_auto_merge: double_count_allowed=False

## 14. price guide DB input contract
- sold_confirmed_strong_input_projection: statuses=sold_confirmed
- sold_likely_weak_input_projection: statuses=sold_likely
- active_reference_projection: statuses=active_observed, price_changed
- archive_depth_projection: statuses=expired_removed
- source_gap_projection: statuses=source_gap_unobserved
- excluded_input_projection: statuses=removed_unknown, manual_review_required, unsafe_boundary_conflict

## 15. CTA / alert DB boundary
- watch_this_model: read_mode=aggregate_only
- watch_this_exact_variant: read_mode=aggregate_only
- target_price_watch: read_mode=aggregate_only
- smart_deal_alert: read_mode=future_placeholder_only
- source_gap_alert: read_mode=aggregate_only

## 16. error / fallback contract
- db_projection_unavailable: safe_empty_state
- source_freshness_unavailable: stale_or_unknown_warning
- archive_projection_unavailable: hide_archive_lane
- price_guide_projection_unavailable: hide_price_guide
- manual_review_projection_unavailable: unsafe_boundary_fallback
- privacy_filter_failed: blocked_or_safe_fallback
- lineage_join_failed: reduce_confidence_or_hide_price_guide
- stale_data_fallback: show_stale_warning
- safe_empty_state: safe_empty_state

## 17. privacy boundary check 결과
- raw_url_block: blocked
- raw_email_block: blocked
- provider_payload_block: blocked
- raw_html_block: blocked
- raw_join_block: blocked

## 18. scenario validation 결과
- pass = 21/21
- A. exact Noctilux DB-backed read plan: passed
- B. 35 lux AA rare variant DB plan: passed
- C. Sigma source-gap DB plan: passed
- D. broad Summicron DB plan: passed
- E. unsafe boundary DB plan: passed
- F. raw URL field attempted: passed
- G. raw email/user field attempted: passed
- H. lineage join missing: passed
- I. source freshness missing: passed
- J. duplicate/relist records: passed
- K. active asking projection: passed
- L. sold likely projection: passed
- M. expired removed projection: passed
- N. source gap projection: passed
- O. CTA aggregate projection: passed
- P. privacy filter failure: passed
- Q. stale price guide projection: passed
- R. source coverage selected/review/blocked: passed
- S. frontend state read: passed
- T. DB unavailable fallback: passed
- U. progress report: passed

## 19. no fake-fill / source-gap / raw-data / duplicate guard 결과
- source-gap은 safe fallback에서도 fake result로 채우지 않는다.
- broad query는 direct market page / fast alert read path로 보내지 않는다.
- raw URL/email 기반 join을 금지한다.
- lineage join은 double count 방지에 필수다.

## 20. actual DB/API/frontend/query 미구현 guard
- DB connection 없음
- DB query 없음
- DB migration 없음
- ORM model 없음
- API/frontend 구현 없음

## 21. output JSON / production code 미수정 여부
- 이번 라운드는 contract artifact만 생성한다.
- production runtime surface는 수정하지 않는다.

## 22. 테스트 결과
- contract_check_count = 4

## 23. 남은 위험
- 다음 DB integration implementation 단계에서는 실제 projection naming, lineage materialization, freshness cache invalidation이 더 구체화되어야 한다.
- public route 단계에서는 frontend state drift check를 실제 runtime contract로 다시 확인해야 한다.

## 24. 다음 backlog 후보
- P3-EXPIRED-SOLD-LISTING-ARCHIVE-DB-INTEGRATION-CONTRACT
- P3-MODEL-MARKET-PAGE-PUBLIC-ROUTE-CONTRACT
- P3-DEALER-LEAD-SIGNAL-CONTRACT
- P3-PRIVATE-BETA-MARKET-PAGE-READINESS-CHECKLIST
- P3-MARKET-PAGE-DB-READ-ADAPTER-IMPLEMENTATION

