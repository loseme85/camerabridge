# P3-EXPIRED-SOLD-LISTING-ARCHIVE-DB-INTEGRATION-CONTRACT

## 1. 작업명
P3-EXPIRED-SOLD-LISTING-ARCHIVE-DB-INTEGRATION-CONTRACT

## 2. 작업 목적
Expired/Sold Listing Archive가 local preview에서 DB-backed archive projection으로 넘어갈 때의 safe read boundary를 계약으로 정의한다.

## 3. 진행률
- 기준: P3 Market Intelligence / Model Market Page preview-to-DB readiness
- 시작 전: 약 83%
- 이번 라운드 완료 후: 약 87%
- 증가분: +4%p

## 4. 구현 요약
- archive record projection, source signal history, status transition, price snapshot, lineage materialization, fetch history, repeated observation, price guide handoff 경계를 정의했다.
- raw URL/HTML/email/provider payload/raw fetch response/raw selector output이 public archive/read model로 흐르지 않도록 막았다.
- 실제 DB connection/query/migration/ORM/archive builder 구현은 만들지 않았다.

## 5. Archive DB integration contract scope
- 포함: archive safe projection boundary, signal/fetch/status/lineage contract, price guide projection handoff, Market Page lane projection, privacy boundary, fallback, progress report.
- 제외: DB schema/migration, DB query, DB connection, ORM, archive builder runtime, API/frontend implementation.

## 6. policy
- contract_only = True
- actual_db_enabled = False
- db_query_enabled = False
- db_migration_enabled = False
- archive_builder_enabled = False
- public_page_safe_fields_only = True

## 7. archive DB domain contract
- archive_record_domain: read_mode=projection_only / public_safe=True / public_projection=True
- archive_identity_domain: read_mode=projection_only / public_safe=True / public_projection=True
- source_signal_history_domain: read_mode=projection_only / public_safe=True / public_projection=True
- source_fetch_history_domain: read_mode=projection_only / public_safe=True / public_projection=True
- archive_status_transition_domain: read_mode=projection_only / public_safe=True / public_projection=True
- archive_price_snapshot_domain: read_mode=projection_only / public_safe=True / public_projection=True
- archive_lineage_domain: read_mode=projection_only / public_safe=True / public_projection=True
- archive_manual_review_domain: read_mode=projection_only / public_safe=True / public_projection=True
- archive_source_policy_domain: read_mode=projection_only / public_safe=True / public_projection=True
- archive_privacy_filter_domain: read_mode=projection_only / public_safe=True / public_projection=True
- price_guide_projection_domain: read_mode=projection_only / public_safe=True / public_projection=True
- market_page_archive_lane_projection_domain: read_mode=projection_only / public_safe=True / public_projection=True
- source_gap_projection_domain: read_mode=projection_only / public_safe=True / public_projection=True
- raw_source_snapshot_domain: read_mode=blocked / public_safe=False / public_projection=False

## 8. archive record projection contract
- archive_record_safe_projection: allowed=25 / blocked=13

## 9. source signal history contract
- explicit_sold_badge: candidate=sold_confirmed_candidate / source_gap_only=False
- sold_page_status: candidate=sold_confirmed_candidate / source_gap_only=False
- dealer_marked_sold: candidate=sold_confirmed_candidate / source_gap_only=False
- dealer_marked_reserved: candidate=sold_likely_candidate / source_gap_only=False
- dealer_marked_hold: candidate=manual_review_or_sold_likely / source_gap_only=False
- out_of_stock_badge: candidate=sold_likely_candidate / source_gap_only=False
- add_to_cart_disabled: candidate=sold_likely_candidate / source_gap_only=False
- removed_404: candidate=expired_removed_candidate / source_gap_only=False
- removed_410: candidate=expired_removed_candidate / source_gap_only=False
- redirect_to_search: candidate=removed_unknown_candidate / source_gap_only=False
- listing_missing_from_index: candidate=expired_removed_candidate / source_gap_only=False
- price_disappeared: candidate=price_changed_candidate / source_gap_only=False
- page_content_changed: candidate=active_observed_candidate / source_gap_only=False
- anti_bot_blocked: candidate=source_gap_only / source_gap_only=True
- source_fetch_failed: candidate=source_gap_only / source_gap_only=True
- source_selector_gap: candidate=source_gap_only / source_gap_only=True

## 10. archive status transition contract
- active_observed -> price_changed: triggers=price_disappeared, page_content_changed
- active_observed -> sold_confirmed: triggers=explicit_sold_badge, sold_page_status, dealer_marked_sold
- active_observed -> sold_likely: triggers=dealer_marked_reserved, dealer_marked_hold, out_of_stock_badge, add_to_cart_disabled
- active_observed -> expired_removed: triggers=removed_404, removed_410, listing_missing_from_index
- active_observed -> removed_unknown: triggers=redirect_to_search
- active_observed -> source_gap_unobserved: triggers=anti_bot_blocked, source_fetch_failed, source_selector_gap
- any -> manual_review_required: triggers=low_model_confidence, review_required_source
- any -> unsafe_boundary_conflict: triggers=adjacent_family_conflict
- duplicate_candidate -> duplicate_merged: triggers=same_source_listing_id, same_url_fingerprint
- relist_candidate -> relisted: triggers=relist_identity_match

## 11. price snapshot projection contract
- archive_price_snapshot_safe_projection: price_types=sale_price_confirmed, listed_price, asking_price, price_on_application, unknown_price, removed_before_price_capture

## 12. lineage materialization contract
- same_listing_lineage: double_count_allowed=False / sample_policy=dedup_to_one_sample
- likely_same_listing_lineage: double_count_allowed=False / sample_policy=dedup_to_one_sample
- duplicate_merged: double_count_allowed=False / sample_policy=exclude_secondary_records
- relisted_link_previous_lineage: double_count_allowed=False / sample_policy=count_once_per_lineage
- cross_source_duplicate_review_only: double_count_allowed=False / sample_policy=exclude_until_verified
- no_lineage_match: double_count_allowed=True / sample_policy=count_once

## 13. source fetch history / repeated observation contract
- source_fetch_outcome_count = 11
- repeated_observation_default: never_creates=sold_confirmed

## 14. price guide projection contract
- sold_confirmed_strong_projection: statuses=sold_confirmed
- sold_likely_weak_projection: statuses=sold_likely
- active_reference_projection: statuses=active_observed, price_changed
- archive_depth_projection: statuses=expired_removed
- source_gap_projection: statuses=source_gap_unobserved
- excluded_projection: statuses=removed_unknown, duplicate_merged, relisted, manual_review_required, unsafe_boundary_conflict, accessory_archive_only, adjacent_family_excluded

## 15. Market Page archive lane projection contract
- sold_confirmed: statuses=sold_confirmed / caution=False
- sold_likely: statuses=sold_likely / caution=True
- expired_removed: statuses=expired_removed / caution=True
- active_uncertain_review: statuses=active_observed, price_changed, manual_review_required, removed_unknown, relisted / caution=True
- source_gap_watch: statuses=source_gap_unobserved / caution=True
- related_but_not_substitute: statuses=unsafe_boundary_conflict, adjacent_family_excluded / caution=True
- accessory_compatible_not_model: statuses=accessory_archive_only / caution=True

## 16. privacy boundary contract
- raw_url_block: projection_invalid -> archive_record_public_projection_blocked
- raw_html_block: projection_invalid -> archive_record_public_projection_blocked
- raw_email_block: projection_invalid -> archive_record_public_projection_blocked
- provider_payload_block: projection_invalid -> archive_record_public_projection_blocked
- raw_fetch_response_block: projection_invalid -> price_guide_projection_blocked
- raw_selector_output_block: projection_invalid -> market_page_lane_blocked
- token_block: projection_invalid -> archive_record_public_projection_blocked
- raw_join_key_block: projection_invalid -> market_page_lane_blocked
- public_projection_safe_fields_only: policy_violation_logged -> archive_record_public_projection_blocked

## 17. fallback / error contract
- archive_projection_unavailable: safe_archive_empty_state
- signal_history_unavailable: manual_review_or_unknown
- price_snapshot_unavailable: keep_status_but_hide_strong_input
- lineage_materialization_unavailable: reduce_confidence_or_hide_price_guide
- source_fetch_history_unavailable: stale_or_unknown_fetch_history
- privacy_filter_failed: archive_record_public_projection_blocked
- source_policy_unavailable: manual_review_required
- stale_or_unknown_fetch_history: stale_or_unknown_fetch_history
- safe_archive_empty_state: safe_archive_empty_state

## 18. privacy boundary check 결과
- raw_url_block: blocked
- raw_html_block: blocked
- raw_email_block: blocked
- provider_payload_block: blocked
- raw_fetch_response_block: blocked
- raw_selector_output_block: blocked
- token_block: blocked
- raw_join_key_block: blocked
- public_projection_safe_fields_only: enforced

## 19. scenario validation 결과
- pass = 26/26
- A. reliable explicit sold DB projection: passed
- B. review-required source sold signal: passed
- C. 404/410 projection: passed
- D. redirect removed unknown: passed
- E. anti-bot blocked: passed
- F. fetch failed / selector gap: passed
- G. active price changed: passed
- H. duplicate same source_listing_id: passed
- I. duplicate same URL fingerprint: passed
- J. relisted same source identity: passed
- K. cross-source duplicate: passed
- L. accessory removed: passed
- M. adjacent family conflict: passed
- N. raw URL in archive projection: passed
- O. raw HTML/fetch response: passed
- P. raw email/provider payload: passed
- Q. raw URL/email join key: passed
- R. source policy unavailable: passed
- S. lineage unavailable: passed
- T. price snapshot unavailable: passed
- U. repeated observation strengthens expired removed: passed
- V. source fetch history unavailable: passed
- W. price guide projection summary: passed
- X. Market Page archive lane projection: passed
- Y. fallback safe archive empty state: passed
- Z. progress report: passed

## 20. sold-overclaim / source-gap / duplicate / raw-data guard 결과
- anti-bot / fetch fail / selector gap은 sold/expired가 아니라 source-gap projection으로만 남긴다.
- 404 / 410 / redirect / active price changed는 sold_confirmed로 전이되지 않는다.
- duplicate / relist / cross-source duplicate는 lineage materialization으로 double count를 막는다.
- adjacent family와 accessory는 target model sold history와 price guide strong input에서 분리한다.
- raw URL / HTML / email / provider payload / raw fetch response / raw selector output은 public projection에서 차단한다.

## 21. actual DB/API/frontend/query 미구현 guard
- actual DB connection 없음
- actual DB query 없음
- actual DB migration 없음
- actual ORM model 없음
- actual archive builder runtime 없음
- actual API/frontend 구현 없음

## 22. output JSON / production code 미수정 여부
- 이번 라운드는 contract artifact만 생성한다.
- production crawler/search/runtime, taxonomy seed, canonical index, raw data, search index, output JSON production surface는 수정하지 않는다.

## 23. 테스트 결과
- contract_check_count = 5

## 24. 남은 위험
- 다음 DB implementation 단계에서는 실제 projection naming, transition event materialization, lineage refresh timing을 더 구체화해야 한다.
- source policy snapshot과 fetch history retention window가 runtime에서 얼마나 신선하게 유지되는지 별도 contract/implementation 검증이 필요하다.

## 25. 다음 backlog 후보
- P3-MODEL-MARKET-PAGE-PUBLIC-ROUTE-CONTRACT
- P3-DEALER-LEAD-SIGNAL-CONTRACT
- P3-PRIVATE-BETA-MARKET-PAGE-READINESS-CHECKLIST
- P3-MARKET-PAGE-DB-READ-ADAPTER-IMPLEMENTATION
- P3-EXPIRED-SOLD-LISTING-ARCHIVE-DB-IMPLEMENTATION

