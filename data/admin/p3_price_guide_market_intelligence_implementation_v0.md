# P3-PRICE-GUIDE-MARKET-INTELLIGENCE-IMPLEMENTATION

## 1. 작업명
P3-PRICE-GUIDE-MARKET-INTELLIGENCE-IMPLEMENTATION

## 2. 작업 목적
Price Guide / Market Intelligence contract를 local preview implementation으로 내려 archive strong/weak/excluded input 위에서 preview state와 signal을 산출한다.

## 3. 진행률
- 기준: P3 Market Intelligence / Model Market Page preview stack
- 시작 전: 약 72%
- 이번 라운드 완료 후: 약 78%
- 증가분: +6%p

## 4. 구현 요약
- archive preview 결과를 strong/weak/active/archive-depth/source-gap/excluded input으로 다시 분류했다.
- sample threshold, source mix, stale warning, overlay, confidence, display state, widget summary를 preview-only로 생성했다.
- numeric price calculation은 하지 않고 sample/count/confidence/source-mix disclosure만 남겼다.

## 5. Price Guide / Market Intelligence implementation scope
- 포함: price guide input classification, input set, threshold, source mix, staleness, overlay, confidence, display, signal, target price, widget summary.
- 제외: production calculator, DB/API, frontend component, archive builder, crawler runtime.

## 6. price_guide_market_intelligence.py public API
- create_price_guide_policy
- create_price_guide_fixture_inputs
- enforce_price_guide_privacy
- classify_price_guide_input
- build_price_guide_input_set
- evaluate_sample_threshold
- evaluate_source_mix
- evaluate_staleness
- evaluate_condition_variant_overlay
- determine_price_guide_confidence
- determine_price_guide_display_state
- build_price_metric_preview
- build_market_intelligence_signal_preview
- build_target_price_watch_preview
- build_smart_deal_placeholder
- create_price_guide_preview_for_model
- create_model_market_page_price_widget_summary
- process_price_guide_market_intelligence_scenarios
- export_price_guide_market_intelligence_preview

## 7. price guide policy
- implementation_mode = local_preview
- local_preview_enabled = True
- production_price_guide_enabled = False
- calculator_enabled = False
- db_query_enabled = False
- numeric_price_calculation_enabled = False

## 8. fixture input summary
- model_fixtures = 11
- archive_record_source = 29
- progress_after = 78%

## 9. privacy / raw data guard 결과
- fixture::noctilux_full: privacy_safe
- fixture::35lux_aa: privacy_safe
- fixture::sigma_source_gap: privacy_safe
- fixture::active_only_noctilux: privacy_safe
- fixture::expired_only_model: privacy_safe
- fixture::unsafe_boundary_conflict: privacy_safe
- fixture::broad_summicron: privacy_safe
- fixture::stale_sold_data: privacy_safe
- fixture::single_source_dominance: privacy_safe
- fixture::duplicate_relisted_excluded: privacy_safe
- fixture::privacy_violation: blocked_policy_violation

## 10. input classification 결과
- fixture::noctilux_full: strong=4 weak=3 excluded=3
- fixture::35lux_aa: strong=1 weak=0 excluded=1
- fixture::sigma_source_gap: strong=0 weak=0 excluded=1
- fixture::active_only_noctilux: strong=0 weak=0 excluded=0
- fixture::expired_only_model: strong=0 weak=0 excluded=0
- fixture::unsafe_boundary_conflict: strong=0 weak=0 excluded=1
- fixture::broad_summicron: strong=0 weak=0 excluded=1
- fixture::stale_sold_data: strong=4 weak=0 excluded=0
- fixture::single_source_dominance: strong=5 weak=0 excluded=0
- fixture::duplicate_relisted_excluded: strong=0 weak=0 excluded=5

## 11. price guide input set 결과
- fixture::noctilux_full: strong=4 weak=3 active=1 archive=2 gap=0
- fixture::35lux_aa: strong=1 weak=0 active=0 archive=0 gap=0
- fixture::sigma_source_gap: strong=0 weak=0 active=0 archive=0 gap=4
- fixture::active_only_noctilux: strong=0 weak=0 active=1 archive=0 gap=0
- fixture::expired_only_model: strong=0 weak=0 active=0 archive=3 gap=0
- fixture::unsafe_boundary_conflict: strong=0 weak=0 active=0 archive=0 gap=0
- fixture::broad_summicron: strong=0 weak=0 active=0 archive=0 gap=0
- fixture::stale_sold_data: strong=4 weak=0 active=0 archive=0 gap=0
- fixture::single_source_dominance: strong=5 weak=0 active=0 archive=0 gap=0
- fixture::duplicate_relisted_excluded: strong=0 weak=0 active=0 archive=0 gap=0

## 12. sample threshold 결과
- fixture::noctilux_full: median=True high=True rare_exception=False
- fixture::35lux_aa: median=False high=False rare_exception=True
- fixture::sigma_source_gap: median=False high=False rare_exception=False
- fixture::active_only_noctilux: median=False high=False rare_exception=False
- fixture::expired_only_model: median=False high=False rare_exception=False
- fixture::unsafe_boundary_conflict: median=False high=False rare_exception=False
- fixture::broad_summicron: median=False high=False rare_exception=False
- fixture::stale_sold_data: median=True high=True rare_exception=False
- fixture::single_source_dominance: median=True high=True rare_exception=False
- fixture::duplicate_relisted_excluded: median=False high=False rare_exception=False

## 13. source mix 결과
- fixture::noctilux_full: sources=3 dominant=Map Camera share=0.5
- fixture::35lux_aa: sources=1 dominant=Fujiya Camera share=1.0
- fixture::sigma_source_gap: sources=0 dominant=none share=0.0
- fixture::active_only_noctilux: sources=0 dominant=none share=0.0
- fixture::expired_only_model: sources=0 dominant=none share=0.0
- fixture::unsafe_boundary_conflict: sources=0 dominant=none share=0.0
- fixture::broad_summicron: sources=0 dominant=none share=0.0
- fixture::stale_sold_data: sources=3 dominant=Map Camera share=0.5
- fixture::single_source_dominance: sources=2 dominant=Map Camera share=0.8
- fixture::duplicate_relisted_excluded: sources=0 dominant=none share=0.0

## 14. stale data 결과
- fixture::noctilux_full: stale=False severity=none
- fixture::35lux_aa: stale=False severity=none
- fixture::sigma_source_gap: stale=False severity=none
- fixture::active_only_noctilux: stale=False severity=none
- fixture::expired_only_model: stale=False severity=none
- fixture::unsafe_boundary_conflict: stale=False severity=none
- fixture::broad_summicron: stale=False severity=none
- fixture::stale_sold_data: stale=True severity=medium
- fixture::single_source_dominance: stale=False severity=none
- fixture::duplicate_relisted_excluded: stale=False severity=none

## 15. condition / variant overlay 결과
- fixture::noctilux_full: rare_no_merge=False mount_conflict=False condition_missing=False
- fixture::35lux_aa: rare_no_merge=True mount_conflict=False condition_missing=True
- fixture::sigma_source_gap: rare_no_merge=False mount_conflict=True condition_missing=True
- fixture::active_only_noctilux: rare_no_merge=False mount_conflict=False condition_missing=True
- fixture::expired_only_model: rare_no_merge=False mount_conflict=False condition_missing=True
- fixture::unsafe_boundary_conflict: rare_no_merge=False mount_conflict=True condition_missing=True
- fixture::broad_summicron: rare_no_merge=False mount_conflict=True condition_missing=True
- fixture::stale_sold_data: rare_no_merge=False mount_conflict=False condition_missing=False
- fixture::single_source_dominance: rare_no_merge=False mount_conflict=False condition_missing=False
- fixture::duplicate_relisted_excluded: rare_no_merge=False mount_conflict=False condition_missing=True

## 16. confidence 결과
- fixture::noctilux_full: price_guide_high_confidence
- fixture::35lux_aa: price_guide_low_confidence
- fixture::sigma_source_gap: source_gap_only
- fixture::active_only_noctilux: active_only_reference
- fixture::expired_only_model: insufficient_data
- fixture::unsafe_boundary_conflict: unsafe_boundary_conflict
- fixture::broad_summicron: broad_query_refinement_required
- fixture::stale_sold_data: price_guide_medium_confidence
- fixture::single_source_dominance: price_guide_medium_confidence
- fixture::duplicate_relisted_excluded: insufficient_data

## 17. display state 결과
- fixture::noctilux_full: full_price_guide_candidate / numeric_allowed=False
- fixture::35lux_aa: insufficient_sold_history / numeric_allowed=False
- fixture::sigma_source_gap: source_gap_no_price_guide / numeric_allowed=False
- fixture::active_only_noctilux: active_reference_only / numeric_allowed=False
- fixture::expired_only_model: limited_price_guide / numeric_allowed=False
- fixture::unsafe_boundary_conflict: unsafe_boundary_no_price_guide / numeric_allowed=False
- fixture::broad_summicron: broad_query_refinement_required / numeric_allowed=False
- fixture::stale_sold_data: full_price_guide_candidate / numeric_allowed=False
- fixture::single_source_dominance: full_price_guide_candidate / numeric_allowed=False
- fixture::duplicate_relisted_excluded: limited_price_guide / numeric_allowed=False

## 18. price metric preview 결과
- fixture::noctilux_full: visible=sold_median_price, sold_range, price_trend_direction, archive_depth, source_mix
- fixture::35lux_aa: visible=archive_depth, source_mix
- fixture::sigma_source_gap: visible=source_mix
- fixture::active_only_noctilux: visible=active_asking_median_reference, source_mix
- fixture::expired_only_model: visible=archive_depth, source_mix
- fixture::unsafe_boundary_conflict: visible=
- fixture::broad_summicron: visible=
- fixture::stale_sold_data: visible=sold_median_price, sold_range, price_trend_direction, archive_depth, source_mix
- fixture::single_source_dominance: visible=sold_median_price, sold_range, price_trend_direction, archive_depth, source_mix
- fixture::duplicate_relisted_excluded: visible=archive_depth, source_mix

## 19. market intelligence signal 결과
- fixture::noctilux_full: visible=rarity_signal, liquidity_signal, price_volatility_signal, archive_depth_signal, target_price_signal, confidence_signal
- fixture::35lux_aa: visible=rarity_signal, liquidity_signal, archive_depth_signal, target_price_signal, confidence_signal
- fixture::sigma_source_gap: visible=source_gap_signal, confidence_signal
- fixture::active_only_noctilux: visible=target_price_signal, confidence_signal
- fixture::expired_only_model: visible=rarity_signal, archive_depth_signal, confidence_signal
- fixture::unsafe_boundary_conflict: visible=confidence_signal
- fixture::broad_summicron: visible=confidence_signal
- fixture::stale_sold_data: visible=rarity_signal, liquidity_signal, price_volatility_signal, archive_depth_signal, target_price_signal, confidence_signal
- fixture::single_source_dominance: visible=rarity_signal, liquidity_signal, price_volatility_signal, archive_depth_signal, target_price_signal, confidence_signal
- fixture::duplicate_relisted_excluded: visible=confidence_signal

## 20. target price / smart deal 결과
- fixture::noctilux_full: target_watch=True smart_deal_future=True
- fixture::35lux_aa: target_watch=True smart_deal_future=True
- fixture::sigma_source_gap: target_watch=False smart_deal_future=True
- fixture::active_only_noctilux: target_watch=True smart_deal_future=True
- fixture::expired_only_model: target_watch=True smart_deal_future=True
- fixture::unsafe_boundary_conflict: target_watch=False smart_deal_future=True
- fixture::broad_summicron: target_watch=False smart_deal_future=True
- fixture::stale_sold_data: target_watch=True smart_deal_future=True
- fixture::single_source_dominance: target_watch=True smart_deal_future=True
- fixture::duplicate_relisted_excluded: target_watch=True smart_deal_future=True

## 21. Model Market Page price widget summary 결과
- fixture::noctilux_full: full_price_guide_candidate / High confidence / Confirmed sold samples: 4
- fixture::35lux_aa: insufficient_sold_history / Low confidence / Confirmed sold samples: 1
- fixture::sigma_source_gap: source_gap_no_price_guide / Source gap / Confirmed sold samples: 0
- fixture::active_only_noctilux: active_reference_only / Active reference only / Confirmed sold samples: 0
- fixture::expired_only_model: limited_price_guide / Insufficient data / Confirmed sold samples: 0
- fixture::unsafe_boundary_conflict: unsafe_boundary_no_price_guide / Boundary conflict / Confirmed sold samples: 0
- fixture::broad_summicron: broad_query_refinement_required / Refinement required / Confirmed sold samples: 0
- fixture::stale_sold_data: full_price_guide_candidate / Medium confidence / Confirmed sold samples: 4
- fixture::single_source_dominance: full_price_guide_candidate / Medium confidence / Confirmed sold samples: 5
- fixture::duplicate_relisted_excluded: limited_price_guide / Insufficient data / Confirmed sold samples: 0

## 22. scenario validation 결과
- pass = 23/23
- A. Noctilux enough strong input: passed
- B. Noctilux weak supplement: passed
- C. 35 lux AA insufficient samples: passed
- D. Sigma source-gap: passed
- E. active-only model: passed
- F. expired-only model: passed
- G. unsafe boundary conflict: passed
- H. broad query: passed
- I. stale sold data: passed
- J. single-source dominance: passed
- K. duplicate/relisted excluded: passed
- L. sold_likely only: passed
- M. active asking below reference: passed
- N. source mix disclosure: passed
- O. condition overlay missing: passed
- P. boxed/special edition overlay: passed
- Q. Noctilux 0.95 vs f/1.0: passed
- R. Summicron M/R/SL boundary: passed
- S. smart deal placeholder: passed
- T. paid CSV/API placeholder: passed
- U. privacy violation: passed
- V. Model Market Page widget summary: passed
- W. batch price guide preview: passed

## 23. active/sold/source-gap/boundary/duplicate guard 결과
- active asking은 sold median처럼 취급하지 않는다.
- source-gap으로 price guide를 만들지 않는다.
- adjacent family와 rare variant를 샘플 부족하다고 합치지 않는다.
- duplicate/relist는 double count하지 않는다.
- sold_likely는 weak supplement일 뿐 median input이 아니다.

## 24. actual DB/API/frontend/calculator/archive 미구현 guard
- production price guide calculator 없음
- DB query 없음
- API response 없음
- frontend component 없음
- archive builder 없음

## 25. output JSON / production code 미수정 여부
- 이번 라운드는 local preview implementation + artifact 생성만 포함한다.
- production runtime surface는 수정하지 않는다.

## 26. 테스트 결과
- batch_summary = {"preview_count": 11, "blocked_count": 1, "full_candidate_count": 3, "source_gap_count": 1}

## 27. 남은 위험
- 다음 implementation 단계에서는 실제 numeric price calculator와 sample window 정의가 더 정교해져야 한다.
- DB integration 단계에서 archive lineage exclusion과 source freshness wiring이 필요하다.

## 28. 다음 backlog 후보
- P3-MODEL-MARKET-PAGE-DATA-ADAPTER-DB-INTEGRATION-CONTRACT
- P3-EXPIRED-SOLD-LISTING-ARCHIVE-DB-INTEGRATION-CONTRACT
- P3-MODEL-MARKET-PAGE-PUBLIC-ROUTE-CONTRACT
- P3-DEALER-LEAD-SIGNAL-CONTRACT
- P3-PRIVATE-BETA-MARKET-PAGE-READINESS-CHECKLIST

