# P3-EXPIRED-SOLD-LISTING-ARCHIVE-IMPLEMENTATION

## 1. 작업명
P3-EXPIRED-SOLD-LISTING-ARCHIVE-IMPLEMENTATION

## 2. 작업 목적
Expired/Sold Listing Archive contract를 local preview 코드로 내려 source signal, archive status, price-guide eligibility, lineage, model summary를 검증한다.

## 3. 구현 요약
- fixture listing/source signal/price input을 기반으로 archive record preview를 생성했다.
- anti-bot/fetch fail/selector gap/404/remove를 sold_confirmed로 올리지 않도록 코드에서 차단했다.
- duplicate/relist/cross-source duplicate를 lineage로 묶어 double count를 막았다.

## 4. Expired/Sold Archive implementation scope
- 포함: privacy guard, identity, signal classification, status classification, price snapshot preview, confidence, price-guide eligibility, lineage, summary.
- 제외: DB query, crawler runtime, sold detector runtime, price guide calculator, frontend/API.

## 5. expired_sold_listing_archive.py public API
- create_archive_policy
- create_archive_fixture_inputs
- enforce_archive_privacy
- create_archive_listing_identity
- classify_source_signal
- classify_archive_status
- create_archive_price_snapshot
- evaluate_archive_confidence
- evaluate_price_guide_eligibility
- resolve_duplicate_relist_lineage
- create_archive_record_preview
- create_archive_summary_for_model
- create_model_market_page_archive_lane_summary
- create_price_guide_archive_input_summary
- process_expired_sold_archive_scenarios
- export_expired_sold_archive_preview

## 6. archive policy
- implementation_mode = local_preview
- local_preview_enabled = True
- production_archive_builder_enabled = False
- db_query_enabled = False
- crawler_runtime_enabled = False
- price_guide_calculation_enabled = False

## 7. fixture input summary
- source_policies = 9
- signal_templates = 16
- price_inputs = 9
- input_listings = 29

## 8. privacy / raw data guard 결과
- blocked_privacy_record = listing::raw_policy_violation
- privacy_status = blocked_policy_violation

## 9. archive listing identity 결과
- listing::noct_explicit_sold_badge: archive::map_camera::map-noct-sold-001 / confidence=high
- listing::noct_dealer_marked_sold: archive::leica_store_miami::lsm-noct-sold-002 / confidence=high
- listing::keh_explicit_sold_review: archive::keh::keh-noct-sold-003 / confidence=high
- listing::noct_reserved: archive::mpb_us::mpb-noct-reserved-004 / confidence=high
- listing::noct_hold: archive::mpb_us::mpb-noct-hold-005 / confidence=high
- listing::noct_out_of_stock: archive::mpb_us::mpb-noct-oos-006 / confidence=high

## 10. source signal classification 결과
- listing::noct_explicit_sold_badge: explicit_sold_badge->sold_confirmed
- listing::noct_dealer_marked_sold: dealer_marked_sold->sold_confirmed
- listing::keh_explicit_sold_review: dealer_marked_sold->sold_confirmed
- listing::noct_reserved: dealer_marked_reserved->sold_likely
- listing::noct_hold: dealer_marked_hold->manual_review_required
- listing::noct_out_of_stock: out_of_stock_badge->sold_likely
- listing::noct_cart_disabled: add_to_cart_disabled->sold_likely
- listing::noct_404: removed_404->expired_removed

## 11. archive status classification 결과
- listing::noct_explicit_sold_badge: sold_confirmed / lane=sold_confirmed
- listing::noct_dealer_marked_sold: sold_confirmed / lane=sold_confirmed
- listing::keh_explicit_sold_review: manual_review_required / lane=active_uncertain_review
- listing::noct_reserved: sold_likely / lane=sold_likely
- listing::noct_hold: manual_review_required / lane=active_uncertain_review
- listing::noct_out_of_stock: sold_likely / lane=sold_likely
- listing::noct_cart_disabled: sold_likely / lane=sold_likely
- listing::noct_404: expired_removed / lane=expired_removed
- listing::noct_410: expired_removed / lane=expired_removed
- listing::noct_redirect_removed_unknown: removed_unknown / lane=active_uncertain_review
- listing::noct_missing_from_index: expired_removed / lane=expired_removed
- listing::noct_active_price_changed: price_changed / lane=active_uncertain_review

## 12. price snapshot preview 결과
- listing::noct_explicit_sold_badge: sale_price_confirmed / amount_present=True
- listing::noct_dealer_marked_sold: sale_price_confirmed / amount_present=True
- listing::keh_explicit_sold_review: sale_price_confirmed / amount_present=True
- listing::noct_reserved: asking_price / amount_present=True
- listing::noct_hold: asking_price / amount_present=True
- listing::noct_out_of_stock: listed_price / amount_present=True
- listing::noct_cart_disabled: listed_price / amount_present=True
- listing::noct_404: removed_before_price_capture / amount_present=False
- listing::noct_410: removed_before_price_capture / amount_present=False
- listing::noct_redirect_removed_unknown: unknown_price / amount_present=False
- listing::noct_missing_from_index: removed_before_price_capture / amount_present=False
- listing::noct_active_price_changed: listed_price / amount_present=True

## 13. confidence evaluation 결과
- listing::noct_explicit_sold_badge: archive_high_confidence
- listing::noct_dealer_marked_sold: archive_high_confidence
- listing::keh_explicit_sold_review: archive_manual_review_required
- listing::noct_reserved: archive_medium_confidence
- listing::noct_hold: archive_manual_review_required
- listing::noct_out_of_stock: archive_medium_confidence
- listing::noct_cart_disabled: archive_medium_confidence
- listing::noct_404: archive_medium_confidence
- listing::noct_410: archive_medium_confidence
- listing::noct_redirect_removed_unknown: archive_manual_review_required
- listing::noct_missing_from_index: archive_medium_confidence
- listing::noct_active_price_changed: archive_medium_confidence

## 14. price guide eligibility 결과
- listing::noct_explicit_sold_badge: strength=strong / exclusion=
- listing::noct_dealer_marked_sold: strength=strong / exclusion=
- listing::keh_explicit_sold_review: strength=excluded / exclusion=not_price_guide_eligible
- listing::noct_reserved: strength=weak / exclusion=sold_likely_not_median_eligible
- listing::noct_hold: strength=excluded / exclusion=not_price_guide_eligible
- listing::noct_out_of_stock: strength=weak / exclusion=sold_likely_not_median_eligible
- listing::noct_cart_disabled: strength=weak / exclusion=sold_likely_not_median_eligible
- listing::noct_404: strength=excluded / exclusion=expired_removed_not_median_eligible
- listing::noct_410: strength=excluded / exclusion=expired_removed_not_median_eligible
- listing::noct_redirect_removed_unknown: strength=excluded / exclusion=removed_unknown_not_price_guide_eligible
- listing::noct_missing_from_index: strength=excluded / exclusion=expired_removed_not_median_eligible
- listing::noct_active_price_changed: strength=active_reference / exclusion=active_asking_not_sold_median

## 15. duplicate / relist lineage 결과
- listing::duplicate_same_source_id_primary: same_listing_lineage / key=sourceid::map_camera::map-noct-dup-019
- listing::duplicate_same_source_id_secondary: duplicate_merged / key=sourceid::map_camera::map-noct-dup-019
- listing::duplicate_same_url_primary: likely_same_listing_lineage / key=urlfp::fujiya_camera::urlfp_fuji_dup_021
- listing::duplicate_same_url_secondary: duplicate_merged / key=urlfp::fujiya_camera::urlfp_fuji_dup_021
- listing::relisted_same_source_identity: relisted_link_previous_lineage / key=lineage::map_noct_relist_prev
- listing::cross_source_duplicate_map: review_only_no_auto_merge / key=crosssource::crossdup::noct::1
- listing::cross_source_duplicate_fuji: review_only_no_auto_merge / key=crosssource::crossdup::noct::1

## 16. archive record preview 결과
- record_count = 29
- blocked_count = 1

## 17. model archive summary 결과
- noctilux sold_confirmed_count = 8
- noctilux sold_likely_count = 3
- noctilux expired_removed_count = 4
- noctilux price_guide_strong_input_count = 4

## 18. Market Page archive lane summary 결과
- leica_noctilux_m_50_095_asph: sold_confirmed=8, sold_likely=3, expired_removed=3, active_uncertain_review=6, source_gap_watch=0, related_but_not_substitute=0, accessory_compatible_not_model=1
- sigma_14_24_dg_dn_art_l_mount: sold_confirmed=0, sold_likely=0, expired_removed=0, active_uncertain_review=0, source_gap_watch=4, related_but_not_substitute=1, accessory_compatible_not_model=0
- leica_summilux_m_35_asph_aa: sold_confirmed=1, sold_likely=0, expired_removed=0, active_uncertain_review=0, source_gap_watch=0, related_but_not_substitute=1, accessory_compatible_not_model=0

## 19. Price Guide archive input summary 결과
- leica_noctilux_m_50_095_asph: strong=4 weak=3 excluded=13
- sigma_14_24_dg_dn_art_l_mount: strong=0 weak=0 excluded=5
- leica_summilux_m_35_asph_aa: strong=1 weak=0 excluded=1

## 20. scenario validation 결과
- pass = 28/28
- A. explicit sold badge: passed
- B. dealer marked sold: passed
- C. reserved / hold item: passed
- D. out of stock / add to cart disabled: passed
- E. 404 / 410 disappeared listing: passed
- F. redirect to search: passed
- G. listing missing from index: passed
- H. anti-bot blocked: passed
- I. source fetch failed: passed
- J. source selector gap: passed
- K. active price changed: passed
- L. sold confirmed low model confidence: passed
- M. adjacent family conflict: passed
- N. accessory listing removed: passed
- O. duplicate same source_listing_id: passed
- P. duplicate same URL fingerprint: passed
- Q. relisted same source identity: passed
- R. cross-source duplicate: passed
- S. sold likely with price: passed
- T. expired removed with price: passed
- U. removed unknown with price: passed
- V. raw URL/html/email violation: passed
- W. source-specific reliability: passed
- X. model archive summary: passed
- Y. Market Page lane summary: passed
- Z. price guide input summary: passed
- AA. privacy output: passed
- AB. batch archive preview: passed

## 21. sold-overclaim / source-gap / duplicate / boundary guard 결과
- anti-bot / fetch fail / selector gap은 source_gap_unobserved로만 남긴다.
- 404 / 410 / redirect / missing index는 sold_confirmed로 올리지 않는다.
- active asking price는 sold median input으로 쓰지 않는다.
- duplicate / relist / cross-source duplicate는 double count를 막는다.

## 22. actual DB/crawler/price-guide/frontend 미구현 guard
- DB schema/migration 없음
- DB query 없음
- crawler runtime 없음
- sold detector runtime 없음
- price guide calculator 없음
- frontend/API route 없음

## 23. output JSON / production code 미수정 여부
- 이번 라운드는 local preview archive implementation + artifact 생성만 포함한다.
- production crawler/search/frontend/API/DB runtime은 수정하지 않는다.

## 24. 테스트 결과
- batch_summary = {"record_count": 29, "privacy_blocked_count": 1, "strong_input_count": 5, "weak_input_count": 3}

## 25. 남은 위험
- 실제 DB-backed archive 단계에서는 source fetch history, repeated observation window, record merge audit trail이 더 정교해져야 한다.
- price guide implementation 단계에서는 archive lineage exclusion과 sample threshold가 다시 연결되어야 한다.

## 26. 다음 backlog 후보
- P3-PRICE-GUIDE-MARKET-INTELLIGENCE-IMPLEMENTATION
- P3-MODEL-MARKET-PAGE-DATA-ADAPTER-DB-INTEGRATION-CONTRACT
- P3-MODEL-MARKET-PAGE-PUBLIC-ROUTE-CONTRACT
- P3-EXPIRED-SOLD-LISTING-ARCHIVE-DB-INTEGRATION-CONTRACT
- P3-DEALER-LEAD-SIGNAL-CONTRACT

