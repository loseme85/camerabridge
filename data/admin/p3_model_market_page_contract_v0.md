# P3-MODEL-MARKET-PAGE-CONTRACT

## 1. 작업명
P3-MODEL-MARKET-PAGE-CONTRACT

## 2. 작업 목적
Camera Bridge의 Model Market Page를 search result page가 아니라 model-level market intelligence page로 정의하기 위한 data/UX/safety contract를 고정한다.

## 3. 구현 요약
- canonical model identity, page section map, listing lanes, price summary placeholder, market signals, alert CTA, source coverage, variant boundary warning, confidence/empty state, monetization hook을 contract로 정의했다.
- no fake-fill, adjacent-family substitution 금지, broad query refinement, source-gap honesty를 contract 핵심 규칙으로 넣었다.
- 실제 frontend/API/DB/price guide/archive는 구현하지 않았다.

## 4. Model Market Page contract scope
- 포함: product/data/UX section contract, lane contract, signal/CTA/source coverage/empty state contract, scenario validation.
- 제외: frontend implementation, API route, DB schema, price guide calculator, sold archive builder, crawler/search/index changes.

## 5. policy
- contract_only = True
- frontend_enabled = False
- api_enabled = False
- db_enabled = False
- live_crawl_enabled = False
- price_guide_calculation_enabled = False
- sold_archive_enabled = False

## 6. model identity contract
- identity count = 6
- Leica Noctilux-M 50mm f/0.95 ASPH
- Leica Summilux-M 35mm f/1.4 ASPH AA
- Leica M6
- Leica APO-Summicron-M 50mm f/2 ASPH
- Leica APO-Vario-Elmarit-SL 90-280mm f/2.8-4
- Sigma 14-24mm DG DN Art L-mount

## 7. page section map
- section count = 17
- hero_summary (priority 1)
- market_status (priority 2)
- active_listings (priority 3)
- sold_expired_history (priority 4)
- price_guide_summary (priority 5)
- price_trend (priority 6)
- source_coverage (priority 7)
- market_alert_cta (priority 8)
- target_price_watch_cta (priority 9)
- variant_and_boundary_notes (priority 10)
- compatibility_or_accessory_notes (priority 11)
- dealer_source_visibility (priority 12)
- data_confidence (priority 13)
- empty_or_source_gap_state (priority 14)
- related_models (priority 15)
- monetization_hooks (priority 16)
- legal_disclaimer (priority 17)

## 8. listing lanes
- active_verified_listings: exact_required=True fake_fill_allowed=False
- active_uncertain_review: exact_required=True fake_fill_allowed=False
- sold_confirmed: exact_required=True fake_fill_allowed=False
- sold_likely: exact_required=True fake_fill_allowed=False
- expired_removed: exact_required=True fake_fill_allowed=False
- price_changed: exact_required=True fake_fill_allowed=False
- source_gap_watch: exact_required=True fake_fill_allowed=False
- related_but_not_substitute: exact_required=False fake_fill_allowed=False
- accessory_compatible_not_model: exact_required=False fake_fill_allowed=False
- dealer_lead_candidate: exact_required=False fake_fill_allowed=False

## 9. price guide summary contract
- active/sold/expired를 구분한다.
- sold_confirmed와 sold_likely를 나눈다.
- archive가 없으면 insufficient data 또는 active-only caution을 표시한다.

## 10. market signals
- rarity_signal: Rare-watch candidate
- liquidity_signal: Liquidity estimate
- price_volatility_signal: Price volatility
- source_gap_signal: Source-gap
- demand_watch_signal: Demand watch
- target_price_signal: Target price watch
- dealer_visibility_signal: Dealer visibility
- archive_depth_signal: Archive depth

## 11. alert CTA contract
- watch_this_model: beta_status=preview_only requires_refinement=False
- watch_this_exact_variant: beta_status=preview_only requires_refinement=False
- target_price_alert: beta_status=preview_only requires_refinement=False
- source_gap_alert: beta_status=preview_only requires_refinement=False
- rare_new_listing_alert: beta_status=preview_only requires_refinement=True
- smart_deal_alert: beta_status=preview_only requires_refinement=True
- request_source: beta_status=preview_only requires_refinement=False
- request_dealer_visibility: beta_status=future_placeholder requires_refinement=False
- export_price_data: beta_status=future_placeholder requires_refinement=False

## 12. source coverage contract
- Map Camera: coverage=selected_active fast_alert=True
- Fujiya Camera: coverage=selected_active fast_alert=True
- Leica Store Miami: coverage=selected_active fast_alert=True
- Ffordes: coverage=selected_active fast_alert=True
- MPB US: coverage=selected_active fast_alert=True
- KEH: coverage=review_required fast_alert=False
- MPB UK/EU: coverage=review_required fast_alert=False
- Mercari Japan: coverage=blocked fast_alert=False
- Korean Sources: coverage=review_required fast_alert=False

## 13. variant / boundary warning
- exact_variant_required: Leica Summilux-M 35mm f/1.4 ASPH AA
- adjacent_family_not_substitute: Sigma 14-24 L vs Leica SL 14-24
- broad_alias_requires_refinement: Summicron
- accessory_compatibility_not_listing: Leica hood/cap/case
- mount_conflict_warning: Summicron-M vs Summicron-R vs Summicron-SL
- sold_price_not_active_price: Sold vs active
- condition_overlay_warning: boxed / mint / CLA / special finish
- boxed_or_special_edition_overlay: MP3 LHSA / boxed Summicron
- adjacent_family_conflict: APO-Vario-Elmarit-SL 90-280 vs Vario-Elmar-R 105-280

## 14. confidence / empty state policy
- high_confidence_market_page: High-confidence market page.
- medium_confidence_market_page: Medium-confidence market page.
- low_confidence_review_required: Low confidence, review required.
- insufficient_data: Insufficient data.
- source_gap: Source-gap known.
- broad_query_refinement_required: This query is broad. Refine the model first.
- unsafe_boundary_conflict: Boundary conflict detected.
- empty::no_active_exact_listings: No exact active listings found yet.
- empty::source_gap_known: This looks like a source coverage gap, not a confirmed absence.
- empty::insufficient_sold_history: We do not have enough sold history to summarize the market yet.
- empty::active_only_no_price_guide: Active listings are visible, but we are not treating them as a complete market price.
- empty::broad_query_needs_refinement: This query is broad. Refine the model before creating a fast alert.
- empty::model_not_seeded_or_not_supported: This model is not ready for a market page yet.
- empty::source_coverage_not_ready: Source coverage is still limited for this model.

## 15. monetization hooks
- market_alert_signup: active_preview
- target_price_watch: active_preview
- pro_price_history: future_placeholder
- csv_export_placeholder: future_placeholder
- api_access_placeholder: future_placeholder
- dealer_lead_placeholder: future_placeholder
- WTB_RFQ_placeholder: future_placeholder
- source_visibility_placeholder: future_placeholder

## 16. benchmark mapping
- CLASSIC.COM: market_status, market_alert_cta, dealer_source_visibility
- WatchCharts: price_guide_summary, price_trend, csv_export_placeholder
- HiFi Shark: active_listings, source_coverage, sold_expired_history
- Keepa: market_status, price_trend
- PriceCharting / WorthPoint / Reverb: sold_expired_history, price_guide_summary
- PCPartPicker: compatibility_or_accessory_notes, variant_and_boundary_notes
- ILS / Automa / Radwell: dealer_source_visibility, WTB_RFQ_placeholder
- StockX: target_price_watch_cta, demand_watch_signal

## 17. scenario validation 결과
- pass = 16/16
- exact_leica_lens_market_page: passed (high_confidence_market_page)
- 35_lux_aa_rare_variant: passed (exact_variant_required)
- broad_summicron_query: passed (broad_query_refinement_required)
- source_gap_sigma_14_24_l: passed (source_gap)
- accessory_compatibility: passed (accessory_lane_only)
- sold_only_history: passed (sold_expired_lane_visible)
- active_only_no_sold_data: passed (active_only_caution)
- adjacent_family_conflict: passed (boundary_warning)
- source_coverage_limited: passed (selected_sources_disclosed)
- target_price_watch: passed (conditional_alert_cta)
- dealer_visibility_placeholder: passed (future_placeholder)
- paid_price_data_placeholder: passed (future_placeholder)
- confidence_insufficient: passed (insufficient_data)
- model_not_seeded: passed (review_required)
- expired_listing_archive_placeholder: passed (archive_placeholder_only)
- price_guide_future_dependency: passed (calculator_not_enabled)

## 18. no fake-fill / source-gap / broad refinement guard
- exact active lane에는 fake-fill이 허용되지 않는다.
- adjacent-family substitution은 허용되지 않는다.
- broad query는 direct market page fast path가 아니라 refinement가 필요하다.
- source-gap은 honest source-gap state로 표시한다.

## 19. actual frontend/DB/search/crawler 미구현 guard
- frontend page 없음
- API route 없음
- DB schema/migration 없음
- price guide calculator 없음
- sold/expired archive builder 없음
- crawler/search/parser/resolver/classifier runtime 수정 없음

## 20. output JSON / production code 미수정 여부
- 이번 라운드는 contract artifact만 생성한다.
- canonical seed/index/raw/search index/output JSON은 수정하지 않는다.

## 21. 테스트 결과
- scenario validation rows generated
- JSONL/JSON artifact export ready

## 22. 남은 위험
- actual model-market data adapter, sold archive, price guide, frontend state는 후속 round가 필요하다.

## 23. 다음 backlog 후보
- P3-EXPIRED-SOLD-LISTING-ARCHIVE-CONTRACT
- P3-PRICE-GUIDE-MARKET-INTELLIGENCE-CONTRACT
- P3-MODEL-MARKET-PAGE-FRONTEND-CONTRACT
- P3-MODEL-MARKET-PAGE-DATA-ADAPTER-CONTRACT
- P3-DEALER-LEAD-SIGNAL-CONTRACT
