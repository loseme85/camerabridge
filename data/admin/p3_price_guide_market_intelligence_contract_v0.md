# P3-PRICE-GUIDE-MARKET-INTELLIGENCE-CONTRACT

## 1. 작업명
P3-PRICE-GUIDE-MARKET-INTELLIGENCE-CONTRACT

## 2. 작업 목적
Camera Bridge의 모델별 Price Guide / Market Intelligence를 위한 data contract, calculation boundary, confidence policy, display policy, sample threshold, trend policy, condition/variant overlay policy, monetization placeholder를 고정한다.

## 3. 구현 요약
- sold-confirmed 중심의 price guide input boundary와 active/expired/source-gap exclusion rule을 contract로 정의했다.
- confidence, sample threshold, source mix, condition/variant overlay, target price / smart deal placeholder 정책을 묶었다.
- 실제 calculator, DB, frontend/API, archive builder는 구현하지 않았다.

## 4. Price Guide / Market Intelligence contract scope
- 포함: model scope, input eligibility, sample threshold, metric contract, confidence/trend/display policy, condition/variant overlay, market-intelligence signals, target-price/smart-deal policy, monetization placeholder.
- 제외: actual calculator, DB schema/migration, frontend/API, archive builder, crawler/search runtime 변경.

## 5. price guide policy
- contract_only = True
- calculator_enabled = False
- db_enabled = False
- api_enabled = False
- frontend_enabled = False
- archive_builder_enabled = False
- active_asking_price_median_allowed = False

## 6. model identity / scope
- Leica Noctilux-M 50mm f/0.95 ASPH: scope=exact_model_only excluded=Leica Noctilux-M 50mm f/1.0, Leica Noctilux-M 50mm f/1.2
- Leica Summilux-M 35mm f/1.4 ASPH AA: scope=exact_rare_variant_only excluded=Leica Summilux-M 35mm f/1.4 ASPH FLE, Leica Summilux-R 35mm
- Leica M6: scope=family_with_condition_overlay excluded=Leica MP, Leica M-A, Leica M7
- Leica APO-Summicron-M 50mm f/2 ASPH: scope=exact_model_only excluded=Leica Summicron-M 50mm f/2, Leica APO-Summicron-SL 50mm
- Sigma 14-24mm DG DN Art L-mount: scope=exact_model_only excluded=Leica Super-Vario-Elmarit-SL 14-24mm, Sigma 24-70 DG DN Art L-mount

## 7. input eligibility policy
- sold_confirmed: median=True trend=True rarity=True
- sold_likely: median=False trend=True rarity=True
- active_observed: median=False trend=True rarity=True
- active_asking_price: median=False trend=True rarity=False
- price_changed: median=False trend=True rarity=False
- expired_removed: median=False trend=False rarity=True
- removed_unknown: median=False trend=False rarity=False
- source_gap_unobserved: median=False trend=False rarity=False
- manual_review_required: median=False trend=False rarity=False
- unsafe_boundary_conflict: median=False trend=False rarity=False
- duplicate_merged: median=False trend=False rarity=False
- relisted: median=False trend=False rarity=False

## 8. sample threshold policy
- sold_confirmed_for_median=3
- minimum_sources_for_high_confidence=2
- maximum_single_source_dominance=0.8

## 9. metric contract
- sold_median_price: allowed=sold_confirmed blocked=active_asking_price, expired_removed, removed_unknown, source_gap_unobserved
- sold_low_price: allowed=sold_confirmed blocked=active_asking_price, expired_removed, removed_unknown
- sold_high_price: allowed=sold_confirmed blocked=active_asking_price, expired_removed, removed_unknown
- sold_range: allowed=sold_confirmed blocked=active_asking_price, source_gap_unobserved
- active_asking_low: allowed=active_asking_price blocked=sold_confirmed
- active_asking_median_reference: allowed=active_asking_price blocked=sold_confirmed
- active_asking_high: allowed=active_asking_price blocked=sold_confirmed
- price_trend_direction: allowed=sold_confirmed, sold_likely, price_changed blocked=source_gap_unobserved, unsafe_boundary_conflict
- price_volatility: allowed=sold_confirmed, sold_likely, price_changed blocked=source_gap_unobserved, removed_unknown
- liquidity_estimate: allowed=sold_confirmed, sold_likely, expired_removed blocked=source_gap_unobserved, unsafe_boundary_conflict
- rarity_estimate: allowed=sold_confirmed, expired_removed, source_gap_unobserved blocked=unsafe_boundary_conflict
- archive_depth: allowed=sold_confirmed, sold_likely, expired_removed blocked=source_gap_unobserved
- source_mix: allowed=sold_confirmed, sold_likely, active_asking_price blocked=source_gap_unobserved
- last_seen_price: allowed=sold_confirmed, active_asking_price blocked=source_gap_unobserved
- target_price_distance: allowed=sold_confirmed, active_asking_price blocked=source_gap_unobserved, unsafe_boundary_conflict
- smart_deal_candidate_score: allowed=sold_confirmed, active_asking_price blocked=source_gap_unobserved, unsafe_boundary_conflict

## 10. confidence policy
- price_guide_high_confidence: High confidence
- price_guide_medium_confidence: Medium confidence
- price_guide_low_confidence: Low confidence
- insufficient_data: Insufficient data
- active_only_reference: Active-only reference
- source_gap_only: Source-gap only
- manual_review_required: Manual review required
- unsafe_boundary_conflict: Unsafe boundary conflict

## 11. trend policy
- trend_up: inputs=sold_confirmed, sold_likely, price_changed
- trend_down: inputs=sold_confirmed, sold_likely, price_changed
- trend_flat: inputs=sold_confirmed, sold_likely
- trend_volatile: inputs=sold_confirmed, sold_likely, price_changed
- trend_insufficient_data: inputs=sold_confirmed
- trend_active_only_reference: inputs=active_asking_price, price_changed

## 12. display policy
- full_price_guide: Enough confirmed sold history to show a guide.
- limited_price_guide: We have some history, but not enough for a strong median.
- active_reference_only: This page shows active asking references only.
- insufficient_sold_history: This page is not ready for a price guide yet.
- source_gap_no_price_guide: This looks like a source coverage gap, not a market price guide.
- broad_query_refinement_required: This query is broad and needs refinement.
- unsafe_boundary_conflict: This page is not safe for a price guide yet.
- model_not_supported: This page is not ready for a price guide yet.

## 13. condition / variant overlay policy
- condition::mint: caution=True
- condition::near_mint: caution=True
- condition::user: caution=True
- condition::boxed: caution=True
- variant::variant_35_lux_aa: merge_allowed=False
- variant::variant_noctilux_095: merge_allowed=False
- variant::variant_summicron_mounts: merge_allowed=False
- variant::variant_sigma_vs_leica_1424: merge_allowed=False
- variant::variant_boxed_special_edition: merge_allowed=True

## 14. market intelligence signals
- rarity_signal: display=visible_with_caution
- liquidity_signal: display=visible_with_caution
- price_volatility_signal: display=visible_with_caution
- source_gap_signal: display=visible_source_gap_state
- archive_depth_signal: display=visible_with_caution
- demand_watch_signal: display=future_placeholder
- target_price_signal: display=visible_if_target_price_watch_ready
- smart_deal_signal: display=future_placeholder
- dealer_visibility_signal: display=future_placeholder
- confidence_signal: display=always_visible

## 15. target price / smart deal policy
- target_price_watch_allowed=True requires_exact_model_or_variant=True
- smart_deal_enabled=False future_placeholder=True

## 16. monetization hooks
- pro_price_history: future_placeholder
- price_guide_pro: future_placeholder
- CSV_export_placeholder: future_placeholder
- API_access_placeholder: future_placeholder
- target_price_watch: future_placeholder
- smart_deal_alert: future_placeholder
- dealer_visibility_placeholder: future_placeholder
- buyer_intent_signal_placeholder: future_placeholder
- source_reliability_report_placeholder: future_placeholder

## 17. benchmark mapping
- WatchCharts: price history, trend confidence, Pro / CSV / API placeholder
- CLASSIC.COM: model market summary, market trend, value estimate framing
- Reverb / PriceCharting / WorthPoint: sold-based price guide, archive dependency
- HiFi Shark: active vs expired history separation, multi-source archive context
- Keepa: price / availability history UX, trend caution
- StockX: target price watch, buyer intent placeholder

## 18. scenario validation 결과
- pass = 20/20
- A. sold_confirmed_enough_for_median: passed (price_guide_high_confidence)
- B. sold_confirmed_too_few: passed (insufficient_data_or_limited_price_guide)
- C. sold_likely_only: passed (no_median_weak_support_only)
- D. active_only_market: passed (active_reference_only)
- E. expired_removed_only: passed (archive_depth_only_no_median)
- F. source_gap_only: passed (source_gap_no_price_guide)
- G. unsafe_boundary_conflict: passed (unsafe_boundary_conflict)
- H. 35_lux_aa_vs_regular: passed (variant_boundary_prevents_merge)
- I. noctilux_095_vs_f1_0: passed (adjacent_family_excluded)
- J. active_asking_below_sold_median: passed (target_price_distance_possible_only)
- K. single_source_dominance: passed (confidence_not_high)
- L. stale_sold_data: passed (stale_data_warning)
- M. duplicate_merged_records: passed (no_double_count)
- N. relisted_item: passed (lineage_aware_count)
- O. condition_overlay_missing: passed (price_spread_caution)
- P. boxed_special_edition_overlay: passed (overlay_warning_no_separate_median_without_samples)
- Q. broad_query: passed (broad_query_refinement_required)
- R. unseeded_model: passed (model_not_supported_or_review_required)
- S. paid_csv_api_placeholder: passed (future_placeholder_only)
- T. model_market_page_integration: passed (price_guide_summary_display_state_returned)

## 19. active price / sold price / source-gap / boundary guard
- active asking price는 sold median에 섞지 않는다.
- sold_likely only로 median을 만들지 않는다.
- source-gap으로 price guide를 만들지 않는다.
- adjacent family와 rare variant를 샘플 부족하다고 합치지 않는다.

## 20. actual calculator/DB/frontend/API 미구현 guard
- actual price guide calculator 없음
- DB schema/migration 없음
- frontend/API route 없음
- archive builder 없음

## 21. output JSON / production code 미수정 여부
- 이번 라운드는 contract artifact만 생성한다.
- canonical index, raw data, search index, output JSON production surface는 수정하지 않는다.

## 22. 테스트 결과
- scenario validation rows generated
- JSONL/JSON artifact export ready

## 23. 남은 위험
- 실제 sample aggregation, condition normalization, time-window logic는 후속 implementation round가 필요하다.
- smart deal과 buyer intent signal은 placeholder 수준이다.

## 24. 다음 backlog 후보
- P3-MODEL-MARKET-PAGE-DATA-ADAPTER-CONTRACT
- P3-MODEL-MARKET-PAGE-FRONTEND-CONTRACT
- P3-EXPIRED-SOLD-LISTING-ARCHIVE-IMPLEMENTATION
- P3-PRICE-GUIDE-MARKET-INTELLIGENCE-IMPLEMENTATION
- P3-DEALER-LEAD-SIGNAL-CONTRACT
