# P3-MODEL-MARKET-PAGE-DATA-ADAPTER-CONTRACT

## 1. 작업명
P3-MODEL-MARKET-PAGE-DATA-ADAPTER-CONTRACT

## 2. 작업 목적
source_change_detection, persistent storage, archive contract, price guide contract, model market page contract를 연결하는 Model Market Page Data Adapter boundary를 고정한다.

## 3. 구현 요약
- canonical resolution, listing/archive mapping, price guide input bundle, lane assembly, source coverage, CTA eligibility, empty/confidence state를 묶는 data adapter contract를 정의했다.
- broad query, source-gap, accessory, adjacent-family conflict, duplicate/relist를 page data assembly 단계에서도 안전하게 차단했다.
- 실제 adapter/query/API/frontend/calculator는 구현하지 않았다.

## 4. Model Market Page Data Adapter contract scope
- 포함: data input boundary, canonical resolution, listing/archive mapping, lane/source/signal/bundle assembly, empty/confidence/CTA/freshness/privacy contract.
- 제외: adapter implementation, DB query, API response, frontend props, price guide calculator, archive builder.

## 5. data adapter policy
- contract_only = True
- adapter_implementation_enabled = False
- db_query_enabled = False
- api_enabled = False
- frontend_props_enabled = False
- price_guide_calculation_enabled = False

## 6. data input contract
- canonical_model_identity: sections=hero_summary, market_status, data_confidence
- listing_observation: sections=active_listings, price_trend
- source_snapshot: sections=source_coverage, market_status
- source_change_candidate: sections=active_listings, empty_or_source_gap_state
- archive_listing_record: sections=sold_expired_history, price_guide_summary
- archive_price_snapshot: sections=price_guide_summary, price_trend
- price_guide_policy: sections=price_guide_summary, price_trend, target_price_watch_cta
- alert_watch_target: sections=market_alert_cta, target_price_watch_cta
- source_coverage_state: sections=source_coverage, empty_or_source_gap_state
- manual_review_state: sections=active_uncertain_review, variant_and_boundary_notes

## 7. canonical model resolution contract
- Leica Noctilux-M 50 0.95: status=exact_canonical_model page=True fast_alert=True
- 35 lux aa: status=refined_variant_required page=True fast_alert=False
- summicron: status=broad_query_refinement_required page=False fast_alert=False
- Sigma 14-24 L: status=source_gap_known page=True fast_alert=False
- SL 90-280 / R 105-280 ambiguous: status=unsafe_boundary_conflict page=False fast_alert=False
- unknown unseeded model: status=model_not_supported page=False fast_alert=False

## 8. listing observation mapping
- new_listing_candidate: lane=active_verified_listings review=False
- price_changed: lane=price_changed review=False
- availability_changed: lane=active_verified_listings review=False
- removed_or_sold_candidate: lane=sold_likely review=True
- duplicate_candidate: lane=active_uncertain_review review=True
- source_gap_resolved_candidate: lane=source_gap_watch review=True
- source_expansion_candidate: lane=source_gap_watch review=True
- low_confidence_candidate: lane=active_uncertain_review review=True
- manual_review_required: lane=active_uncertain_review review=True
- skipped_anti_bot_guard: lane=source_gap_watch review=True

## 9. archive input mapping
- sold_confirmed: lane=sold_confirmed strong_input=True
- sold_likely: lane=sold_likely strong_input=False
- expired_removed: lane=expired_removed strong_input=False
- removed_unknown: lane=active_uncertain_review strong_input=False
- relisted: lane=expired_removed strong_input=False
- duplicate_merged: lane=active_uncertain_review strong_input=False
- source_gap_unobserved: lane=source_gap_watch strong_input=False
- manual_review_required: lane=active_uncertain_review strong_input=False
- unsafe_boundary_conflict: lane=related_but_not_substitute strong_input=False

## 10. price guide input bundle contract
- pg_bundle::noctilux_095: sold_confirmed=5 excluded=duplicate_merged, source_gap_unobserved
- pg_bundle::35_lux_aa: sold_confirmed=2 excluded=regular_35_lux_variant
- pg_bundle::sigma_14_24_l: sold_confirmed=0 excluded=source_gap_unobserved, unsafe_boundary_conflict, leica_sl_14_24_related

## 11. market page lane assembly
- active_verified_listings: exact_required=True blocked=accessory_listing, related_but_not_substitute, source_gap_unobserved
- active_uncertain_review: exact_required=False blocked=sold_confirmed_archive
- sold_confirmed: exact_required=True blocked=active_observed, removed_unknown
- sold_likely: exact_required=True blocked=active_observed, source_gap_unobserved
- expired_removed: exact_required=True blocked=active_observed
- price_changed: exact_required=True blocked=source_gap_unobserved
- source_gap_watch: exact_required=False blocked=sold_confirmed_archive
- related_but_not_substitute: exact_required=False blocked=active_verified_listings
- accessory_compatible_not_model: exact_required=False blocked=active_verified_listings, sold_confirmed
- dealer_lead_candidate: exact_required=False blocked=active_verified_listings

## 12. source coverage assembly
- Map Camera: coverage=selected_supported fast_alert=True
- Fujiya Camera: coverage=selected_supported fast_alert=True
- Leica Store Miami: coverage=selected_supported fast_alert=True
- Ffordes: coverage=selected_supported fast_alert=True
- MPB US: coverage=selected_supported fast_alert=True
- KEH: coverage=review_required fast_alert=False
- MPB UK/EU: coverage=review_required fast_alert=False
- Mercari Japan: coverage=blocked_anti_bot_risk fast_alert=False
- Korean Sources: coverage=review_required fast_alert=False

## 13. market signal input bundle
- rarity_signal: future_placeholder=False
- liquidity_signal: future_placeholder=False
- price_volatility_signal: future_placeholder=False
- source_gap_signal: future_placeholder=False
- archive_depth_signal: future_placeholder=False
- demand_watch_signal: future_placeholder=True
- target_price_signal: future_placeholder=False
- smart_deal_signal: future_placeholder=True
- dealer_visibility_signal: future_placeholder=True
- confidence_signal: future_placeholder=False

## 14. empty / confidence state contract
- empty::no_active_exact_listings: No exact active listings found yet.
- empty::source_gap_known: This looks like a source coverage gap, not a confirmed absence.
- empty::insufficient_sold_history: Not enough confirmed sold listings yet.
- empty::active_only_no_price_guide: Active asking prices are shown separately from sold prices.
- empty::broad_query_needs_refinement: This query is broad. Refine the model before creating a fast alert.
- empty::model_not_seeded_or_not_supported: This page is not ready for this model yet.
- empty::source_coverage_not_ready: This model has limited source coverage.
- empty::unsafe_boundary_conflict: This page is not safe for a model-level summary yet.
- empty::archive_only_no_active: We have historical traces, but no active exact listing right now.
- confidence::high_confidence_market_page: High confidence market page
- confidence::medium_confidence_market_page: Medium confidence market page
- confidence::low_confidence_review_required: Review required
- confidence::insufficient_data: Insufficient data
- confidence::source_gap: Source gap
- confidence::broad_query_refinement_required: Refinement required
- confidence::unsafe_boundary_conflict: Boundary conflict
- confidence::active_reference_only: Active reference only

## 15. CTA eligibility contract
- watch_this_model: allowed_when=exact_model_page future=False
- watch_this_exact_variant: allowed_when=exact_rare_variant future=False
- rare_new_listing_alert: allowed_when=exact_model_or_variant future=False
- source_gap_alert: allowed_when=source_gap_known future=False
- target_price_watch: allowed_when=exact_model_or_variant_with_confidence_or_caution future=False
- smart_deal_alert: allowed_when=future_placeholder future=True
- request_source: allowed_when=source_gap_or_coverage_limited future=False
- export_price_data: allowed_when=future_placeholder future=True
- dealer_visibility_request: allowed_when=future_placeholder future=True

## 16. market page data bundle contract
- page_bundle::leica_noctilux_50_095: status=exact_model_bundle_ready display=full_price_guide
- page_bundle::sigma_14_24_l: status=source_gap_bundle display=source_gap_no_price_guide

## 17. freshness policy
- price_guide_freshness_window=sold_data_warning_after_180d
- source_coverage_stale_after_days=30

## 18. privacy / raw data guard
- forbidden=raw_url, raw_html, raw_email, raw_seller_personal_info, raw_provider_payload, raw_webhook_body
- allowed=source_id, source_name, source_listing_id, listing_url_fingerprint, title_fingerprint, normalized_title_fingerprint, image_fingerprint_placeholder, safe_external_link_placeholder_ref

## 19. scenario validation 결과
- pass = 21/21
- A. exact_noctilux_market_page_bundle: passed (exact_bundle_safe)
- B. 35_lux_aa_exact_rare_variant: passed (exact_variant_required)
- C. broad_summicron_query: passed (broad_query_refinement_required)
- D. sigma_14_24_l_source_gap: passed (source_gap_bundle)
- E. active_listing_high_confidence: passed (active_verified_listings_lane)
- F. active_listing_low_confidence: passed (active_uncertain_review_lane)
- G. sold_confirmed_archive_input: passed (sold_confirmed_strong_input)
- H. sold_likely_archive_input: passed (sold_likely_weak_only)
- I. expired_removed_input: passed (expired_removed_no_median)
- J. removed_unknown_input: passed (review_or_hidden_no_price_guide)
- K. anti_bot_skipped_source: passed (source_gap_fetch_issue_only)
- L. duplicate_relisted_lineage: passed (no_double_count)
- M. accessory_listing: passed (accessory_lane_only)
- N. unsafe_boundary_conflict: passed (related_or_blocked)
- O. source_coverage_limited: passed (coverage_disclosed)
- P. active_only_no_sold_data: passed (active_reference_only)
- Q. sold_data_stale: passed (stale_data_warning)
- R. target_price_watch: passed (exact_with_confidence_or_caution)
- S. smart_deal_placeholder: passed (future_placeholder_only)
- T. public_bundle_privacy: passed (raw_flags_false)
- U. model_market_page_integration: passed (bundle_sections_present)

## 20. no fake-fill / source-gap / broad refinement / boundary guard
- broad query는 direct page/fast alert로 보내지 않는다.
- source-gap은 source-gap lane과 empty state로만 표현한다.
- adjacent-family substitution은 data assembly 단계에서 막는다.
- accessory는 active/sold model lane에 섞지 않는다.

## 21. actual adapter/DB/API/frontend/calculator 미구현 guard
- adapter implementation 없음
- DB query 없음
- API response 없음
- frontend props 없음
- price guide calculator 없음

## 22. output JSON / production code 미수정 여부
- 이번 라운드는 contract artifact만 생성한다.
- canonical index, taxonomy seed, raw data, search index, output JSON production surface는 수정하지 않는다.

## 23. 테스트 결과
- scenario validation rows generated
- JSONL/JSON artifact export ready

## 24. 남은 위험
- 실제 adapter 구현 시 query performance, lineage joins, freshness aggregation은 후속 round가 필요하다.
- CTA/runtime gating은 implementation phase에서 unsubscribe/send/verification runtime과 다시 연결해야 한다.

## 25. 다음 backlog 후보
- P3-MODEL-MARKET-PAGE-DATA-ADAPTER-IMPLEMENTATION
- P3-MODEL-MARKET-PAGE-FRONTEND-CONTRACT
- P3-EXPIRED-SOLD-LISTING-ARCHIVE-IMPLEMENTATION
- P3-PRICE-GUIDE-MARKET-INTELLIGENCE-IMPLEMENTATION
- P3-DEALER-LEAD-SIGNAL-CONTRACT
