# P3-EXPIRED-SOLD-LISTING-ARCHIVE-CONTRACT

## 1. 작업명
P3-EXPIRED-SOLD-LISTING-ARCHIVE-CONTRACT

## 2. 작업 목적
Camera Bridge의 sold / expired / removed listing archive를 위한 data contract, classification policy, retention policy, confidence policy, source signal policy, Model Market Page 연동 boundary를 고정한다.

## 3. 구현 요약
- sold / expired / removed / source-gap / duplicate / relist 상태를 구분하는 archive contract를 정의했다.
- source signal별 sold-overclaim 방지 규칙과 price-guide 입력 자격을 분리했다.
- 실제 archive builder / DB / crawler / price guide calculator는 구현하지 않았다.

## 4. Expired/Sold Archive contract scope
- 포함: listing identity, status classification, source signal policy, source-specific policy, price snapshot, confidence/retention/privacy, Model Market Page integration, price guide dependency, duplicate/relist/merge policy, monetization placeholder.
- 제외: archive builder, DB schema/migration, sold detector runtime, price guide calculator, frontend/API, crawler/search runtime 변경.

## 5. archive policy
- contract_only = True
- archive_builder_enabled = False
- db_enabled = False
- api_enabled = False
- frontend_enabled = False
- price_guide_calculation_enabled = False
- sold_detection_runtime_enabled = False

## 6. archive listing identity contract
- identity count = 6
- archive_listing::noctilux_50_095_map_camera: model=leica_noctilux_m_50_095_asph confidence=high
- archive_listing::35_lux_aa_fujiya: model=leica_summilux_m_35_asph_aa confidence=high
- archive_listing::sigma_14_24_l_source_gap: model=sigma_14_24_dg_dn_art_l_mount confidence=medium
- archive_listing::apo_vario_elmarit_sl_boundary_conflict: model=leica_apo_vario_elmarit_sl_90_280_28_4 confidence=low
- archive_listing::leica_m6_accessory_removed: model=leica_m6 confidence=high
- archive_listing::unseeded_review_case: model=review_pending_model confidence=low

## 7. archive status classification
- active_observed: lane=active_verified_listings price_guide_eligible=False
- price_changed: lane=price_changed price_guide_eligible=False
- sold_confirmed: lane=sold_confirmed price_guide_eligible=True
- sold_likely: lane=sold_likely price_guide_eligible=True
- expired_removed: lane=expired_removed price_guide_eligible=False
- removed_unknown: lane=expired_removed price_guide_eligible=False
- relisted: lane=expired_removed price_guide_eligible=False
- duplicate_merged: lane=expired_removed price_guide_eligible=False
- source_gap_unobserved: lane=source_gap_watch price_guide_eligible=False
- manual_review_required: lane=active_uncertain_review price_guide_eligible=False
- unsafe_boundary_conflict: lane=related_but_not_substitute price_guide_eligible=False

## 8. source sold/expired signal policy
- explicit_sold_badge: maps_to=sold_confirmed price_guide_eligible=True
- sold_page_status: maps_to=sold_confirmed price_guide_eligible=True
- out_of_stock_badge: maps_to=sold_likely price_guide_eligible=False
- removed_404: maps_to=expired_removed price_guide_eligible=False
- removed_410: maps_to=expired_removed price_guide_eligible=False
- redirect_to_search: maps_to=removed_unknown price_guide_eligible=False
- listing_missing_from_index: maps_to=expired_removed price_guide_eligible=False
- price_disappeared: maps_to=price_changed price_guide_eligible=False
- add_to_cart_disabled: maps_to=sold_likely price_guide_eligible=False
- dealer_marked_reserved: maps_to=sold_likely price_guide_eligible=False
- dealer_marked_hold: maps_to=manual_review_required price_guide_eligible=False
- dealer_marked_sold: maps_to=sold_confirmed price_guide_eligible=True
- page_content_changed: maps_to=active_observed price_guide_eligible=False
- anti_bot_blocked: maps_to=source_gap_unobserved price_guide_eligible=False
- source_fetch_failed: maps_to=source_gap_unobserved price_guide_eligible=False
- source_selector_gap: maps_to=source_gap_unobserved price_guide_eligible=False

## 9. source-specific archive policy
- Map Camera: support=selected_supported sold_confirmed_allowed=True
- Fujiya Camera: support=selected_supported sold_confirmed_allowed=True
- Leica Store Miami: support=selected_supported sold_confirmed_allowed=True
- Ffordes: support=selected_supported sold_confirmed_allowed=True
- MPB US: support=selected_supported sold_confirmed_allowed=True
- KEH: support=review_required sold_confirmed_allowed=False
- MPB UK/EU: support=review_required sold_confirmed_allowed=False
- Mercari Japan: support=blocked_anti_bot_risk sold_confirmed_allowed=False
- Korean Sources: support=review_required sold_confirmed_allowed=False

## 10. price snapshot contract
- listed_price: archive=archive_listing::noctilux_50_095_map_camera price_guide_eligible=False
- sale_price_confirmed: archive=archive_listing::noctilux_50_095_map_camera price_guide_eligible=True
- asking_price: archive=archive_listing::35_lux_aa_fujiya price_guide_eligible=False
- price_on_application: archive=archive_listing::apo_vario_elmarit_sl_boundary_conflict price_guide_eligible=False
- unknown_price: archive=archive_listing::sigma_14_24_l_source_gap price_guide_eligible=False
- removed_before_price_capture: archive=archive_listing::leica_m6_accessory_removed price_guide_eligible=False

## 11. confidence policy
- archive_high_confidence: High-confidence archive
- archive_medium_confidence: Medium-confidence archive
- archive_low_confidence: Low-confidence archive
- archive_manual_review_required: Manual review required
- archive_not_price_guide_eligible: Not price-guide eligible
- archive_source_gap: Source gap
- archive_unsafe_boundary_conflict: Unsafe boundary conflict

## 12. retention policy
- active_snapshot_history: 30-90d
- price_snapshot_history: 365d+
- sold_confirmed_archive: long_term
- sold_likely_archive: long_term_with_caution
- expired_removed_archive: long_term
- removed_unknown_archive: 90-180d_or_review_limited
- duplicate_merge_records: 365d
- source_fetch_failure_records: 7-30d
- manual_review_records: until_resolved_plus_audit_window
- audit_log_records: 365d

## 13. privacy / raw data guard
- forbidden=raw_listing_url, raw_url, raw_html, raw_image_binary, raw_seller_personal_info, raw_email, raw_provider_payload, raw_webhook_body
- allowed=listing_url_fingerprint, source_listing_id, title_fingerprint, normalized_title_fingerprint, image_fingerprint_placeholder, source_id, source_name, safe_external_link_placeholder_ref

## 14. Model Market Page integration
- integration::sold_confirmed: section=sold_expired_history lane=sold_confirmed
- integration::sold_likely: section=sold_expired_history lane=sold_likely
- integration::expired_removed: section=sold_expired_history lane=expired_removed
- integration::removed_unknown: section=sold_expired_history lane=active_uncertain_review
- integration::price_changed: section=price_trend lane=price_changed
- integration::source_gap: section=empty_or_source_gap_state lane=source_gap_watch
- integration::boundary_conflict: section=variant_and_boundary_notes lane=related_but_not_substitute

## 15. price guide dependency
- sold_confirmed: median=True trend=True
- sold_likely: median=False trend=True
- expired_removed: median=False trend=False
- removed_unknown: median=False trend=False
- active_observed: median=False trend=True
- price_changed: median=False trend=True
- source_gap_unobserved: median=False trend=False

## 16. duplicate / relist / merge policy
- lineage_same_source_listing_id: decision=same_listing_lineage double_count_allowed=False
- lineage_same_source_url_fingerprint: decision=likely_same_listing_lineage double_count_allowed=False
- possible_duplicate_title_price_image: decision=possible_duplicate_manual_review double_count_allowed=False
- relisted_same_source_identity: decision=relisted_link_previous_lineage double_count_allowed=False
- cross_source_duplicate_review_only: decision=review_only_no_auto_merge double_count_allowed=False

## 17. monetization hooks
- sold_archive_access: future_placeholder
- price_history_pro: future_placeholder
- model_market_page_pro: future_placeholder
- CSV_export_placeholder: future_placeholder
- API_access_placeholder: future_placeholder
- dealer_visibility_placeholder: future_placeholder
- WTB_RFQ_placeholder: future_placeholder
- source_reliability_report_placeholder: future_placeholder

## 18. scenario validation 결과
- pass = 18/18
- A. explicit_sold_badge: passed (sold_confirmed)
- B. reserved_or_hold_item: passed (sold_likely_or_manual_review_required)
- C. 404_disappeared_listing: passed (expired_removed_or_removed_unknown)
- D. anti_bot_blocked_source: passed (source_gap_or_fetch_issue)
- E. source_selector_gap: passed (source_gap_unobserved)
- F. active_price_changed: passed (price_changed)
- G. active_only_no_sold_history: passed (active_reference_only)
- H. sold_confirmed_low_model_confidence: passed (archive_manual_review_required)
- I. adjacent_family_conflict: passed (unsafe_boundary_conflict)
- J. accessory_listing_removed: passed (accessory_lane_only)
- K. duplicate_listing_same_source_id: passed (duplicate_merged)
- L. relisted_same_item: passed (relisted_lineage)
- M. sold_likely_with_price: passed (weak_price_input_with_caution)
- N. removed_unknown: passed (not_price_guide_eligible)
- O. raw_url_html_violation: passed (blocked_policy_violation)
- P. model_market_page_integration: passed (correct_lane_mapping)
- Q. price_guide_sample_threshold: passed (insufficient_data)
- R. paid_export_placeholder: passed (future_placeholder_only)

## 19. no fake-fill / source-gap / sold-overclaim guard
- anti-bot blocked / fetch failed / selector gap은 sold로 분류하지 않는다.
- 404 / removed는 sold_confirmed로 올리지 않는다.
- active asking price는 sold median에 섞지 않는다.
- accessory listing은 model sold history에 섞지 않는다.
- adjacent-family substitution은 허용하지 않는다.

## 20. actual DB/crawler/archive/price-guide 미구현 guard
- archive builder 없음
- DB schema/migration 없음
- crawler/search/parser/resolver/classifier runtime 수정 없음
- price guide calculator 없음
- frontend/API route 없음

## 21. output JSON / production code 미수정 여부
- 이번 라운드는 contract artifact만 생성한다.
- raw data / search index / canonical index / output JSON production surface는 수정하지 않는다.

## 22. 테스트 결과
- scenario validation rows generated
- JSONL/JSON artifact export ready

## 23. 남은 위험
- source별 sold signal 신뢰도는 실제 selector/runtime 검증 전까지 가설 단계다.
- price guide sample threshold와 duplicate/relist linkage는 후속 implementation round가 필요하다.

## 24. 다음 backlog 후보
- P3-PRICE-GUIDE-MARKET-INTELLIGENCE-CONTRACT
- P3-EXPIRED-SOLD-LISTING-ARCHIVE-IMPLEMENTATION
- P3-MODEL-MARKET-PAGE-DATA-ADAPTER-CONTRACT
- P3-MODEL-MARKET-PAGE-FRONTEND-CONTRACT
- P3-DEALER-LEAD-SIGNAL-CONTRACT
