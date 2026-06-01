# P3-MODEL-MARKET-PAGE-FRONTEND-CONTRACT

## 1. 작업명
P3-MODEL-MARKET-PAGE-FRONTEND-CONTRACT

## 2. 작업 목적
MarketPageDataBundle을 어떤 섹션, 상태, 문구, CTA 규칙으로 보여줄지 정의하는 frontend UX contract를 만든다.

## 3. 구현 요약
- exact model / rare variant / source-gap / broad query / unsafe boundary / unsupported 상태를 분리했다.
- active vs sold separation, related-not-substitute, accessory-not-model, selected source coverage disclosure를 UI 카피와 섹션 규칙으로 고정했다.
- 실제 frontend/API/DB/calculator는 만들지 않았다.

## 4. Model Market Page Frontend contract scope
- 포함: state, section, copy, CTA, disclosure, mobile/desktop layout contract.
- 제외: React component, HTML/CSS, API route, DB query, price guide calculator, archive builder.

## 5. frontend policy
- contract_only = True
- frontend_implementation_enabled = False
- react_component_enabled = False
- api_route_enabled = False
- db_query_enabled = False
- price_calculation_enabled = False

## 6. frontend states
- exact_model_full_market_page: exact_model_bundle_ready
- exact_rare_variant_limited_market_page: exact_rare_variant_bundle_ready
- source_gap_market_page: source_gap_bundle
- broad_query_refinement_page: broad_query_refinement_required
- unsafe_boundary_conflict_page: unsafe_boundary_conflict
- model_not_supported_page: model_not_supported
- active_only_no_price_guide_page: active_reference_only
- archive_only_no_active_page: archive_only_bundle_ready
- insufficient_sold_history_page: insufficient_sold_history
- loading_skeleton: loading_skeleton
- error_safe_fallback: error_safe_fallback

## 7. layout section map
- top_nav_placeholder: mobile=1 desktop=1
- hero_summary: mobile=1 desktop=1
- market_status_card: mobile=2 desktop=2
- price_guide_summary_card: mobile=3 desktop=2
- active_listings_lane: mobile=5 desktop=3
- sold_confirmed_lane: mobile=6 desktop=4
- sold_likely_lane: mobile=7 desktop=5
- expired_removed_lane: mobile=8 desktop=6
- source_gap_notice: mobile=3 desktop=3
- related_not_substitute_lane: mobile=8 desktop=7
- accessory_lane: mobile=9 desktop=8
- source_coverage_panel: mobile=7 desktop=9
- confidence_disclosure_panel: mobile=9 desktop=10
- alert_cta_panel: mobile=4 desktop=5
- target_price_watch_panel: mobile=4 desktop=4
- variant_boundary_warning_panel: mobile=8 desktop=8
- compatibility_warning_panel: mobile=9 desktop=9
- market_signal_panel: mobile=10 desktop=7
- monetization_placeholder_panel: mobile=10 desktop=11
- legal_disclaimer_footer: mobile=10 desktop=12

## 8. hero summary contract
- display_name_en = Leica Noctilux-M 50mm f/0.95 ASPH
- confidence_badge = High-confidence model page
- caution_line_en = Active listings and sold history are separated.

## 9. price guide widget contract
- full_price_guide_candidate: confidence=High confidence CTA_allowed=True
- limited_price_guide: confidence=Medium confidence CTA_allowed=True
- insufficient_sold_history: confidence=Insufficient data CTA_allowed=True
- active_reference_only: confidence=Active reference only CTA_allowed=True
- source_gap_no_price_guide: confidence=Source gap CTA_allowed=False
- unsafe_boundary_no_price_guide: confidence=Boundary conflict CTA_allowed=False
- model_not_supported_no_price_guide: confidence=Review required CTA_allowed=False

## 10. listing lane view contract
- active_verified_listings: price_policy=active_asking_only
- active_uncertain_review: price_policy=hidden_or_cautious
- sold_confirmed: price_policy=sold_history_placeholder_only
- sold_likely: price_policy=caution_only
- expired_removed: price_policy=not_sold_price
- price_changed: price_policy=active_reference_only
- source_gap_watch: price_policy=no_price
- related_but_not_substitute: price_policy=context_only
- accessory_compatible_not_model: price_policy=accessory_only

## 11. source coverage view contract
- selected_sources = Map Camera, Fujiya Camera, Leica Store Miami, Ffordes, MPB US
- review_required_sources = KEH, MPB UK/EU, Korean Sources
- blocked_sources = Mercari Japan
- all_source_claim_present = False

## 12. confidence disclosure contract
- High confidence / 고신뢰
- Medium confidence / 중간 신뢰
- Review required / 검토 필요
- Insufficient data / 데이터 부족
- Source gap / 소스 공백
- Boundary conflict / 경계 충돌
- Active reference only / 활성 시세 참고 전용

## 13. alert CTA view contract
- watch_this_model: future=False visible_when=exact_model_full_market_page, archive_only_no_active_page
- watch_this_exact_variant: future=False visible_when=exact_rare_variant_limited_market_page
- rare_new_listing_alert: future=False visible_when=exact_model_full_market_page, exact_rare_variant_limited_market_page
- source_gap_alert: future=False visible_when=source_gap_market_page
- target_price_watch: future=False visible_when=exact_model_full_market_page, active_only_no_price_guide_page
- request_source: future=False visible_when=source_gap_market_page
- smart_deal_alert_future: future=True visible_when=exact_model_full_market_page
- export_price_data_future: future=True visible_when=exact_model_full_market_page, insufficient_sold_history_page
- dealer_visibility_future: future=True visible_when=exact_model_full_market_page

## 14. boundary / compatibility warning view contract
- exact_variant_required: Leica Summilux-M 35mm f/1.4 ASPH AA
- adjacent_family_not_substitute: Leica Noctilux-M 50mm f/0.95 vs f/1.0 / f/1.2
- broad_query_refinement_required: Summicron / Summilux / Leica M
- accessory_not_model_listing: hood / cap / case
- mount_conflict_warning: M / R / SL mount conflict
- active_vs_sold_price_warning: active vs sold
- condition_overlay_warning: mint / user / CLA / haze
- special_edition_overlay_warning: black / chrome / safari / titanium
- source_gap_not_absence_warning: Sigma 14-24 L vs Leica SL 14-24

## 15. empty state view contract
- no_active_exact_listings: No exact active listings found yet.
- source_gap_known: This looks like a source coverage gap.
- insufficient_sold_history: Not enough confirmed sold listings yet.
- active_only_no_price_guide: Active asking prices are shown separately.
- broad_query_needs_refinement: Refine this query before opening a model page.
- model_not_seeded_or_not_supported: This model is not supported yet.
- source_coverage_not_ready: Source coverage is not ready for this preview.
- unsafe_boundary_conflict: This target has a boundary conflict.
- archive_only_no_active: No exact active listings are visible right now.
- no_sold_confirmed_history: No confirmed sold history yet.

## 16. mobile / desktop layout contract
- mobile priority = hero_summary, market_status_card, price_guide_summary_card or source_gap_notice, alert_cta_panel, active_listings_lane, sold_confirmed_lane / sold_likely_lane / expired_removed_lane, source_coverage_panel, variant_boundary_warning_panel, confidence_disclosure_panel, legal_disclaimer_footer
- desktop main column = hero_summary, market_status_card, active_listings_lane, sold_confirmed_lane, sold_likely_lane, expired_removed_lane, related_not_substitute_lane, accessory_lane
- desktop sticky column = price_guide_summary_card, alert_cta_panel, target_price_watch_panel, source_coverage_panel, confidence_disclosure_panel

## 17. copy contract
- active_vs_sold_separation: Active asking prices are shown separately from sold prices.
- insufficient_sold_history: Not enough confirmed sold listings yet.
- source_gap_explanation: This looks like a source coverage gap, not a confirmed absence.
- broad_query_refinement: This query is broad. Refine the model before creating a fast alert.
- related_not_substitute: We found related items, but they are not substitutes for this model.
- accessory_not_model_listing: Compatible accessory, not the model listing itself.
- selected_source_coverage: Selected source coverage is shown separately from review-required and blocked sources.
- no_affiliation_disclaimer: Camera Bridge is not affiliated with Leica Camera AG.
- beta_preview_status: Preview beta: some sections are placeholders or limited summaries.
- future_placeholder_disclosure: Some features shown here are future placeholders only.

## 18. legal / disclaimer contract
- required_points_en = 7
- required_points_ko = 7

## 19. claim safety check 결과
- blocked_claim_count = 14
- en: all sources -> blocked
- en: guaranteed price -> blocked
- en: real-time all dealer alerts -> blocked
- en: official leica -> blocked
- en: 100% accurate -> blocked
- en: investment advice -> blocked
- en: best deal guaranteed -> blocked
- ko: 모든 사이트 -> blocked
- ko: 최저가 보장 -> blocked
- ko: 실시간 전체 알림 -> blocked
- ko: 공식 라이카 -> blocked
- ko: 100% 정확 -> blocked
- ko: 투자 조언 -> blocked
- ko: 무조건 좋은 딜 -> blocked

## 20. scenario validation 결과
- pass = 21/21
- A. Noctilux exact full page: passed
- B. 35 lux AA limited rare variant page: passed
- C. Sigma 14-24 L source-gap page: passed
- D. broad Summicron refinement page: passed
- E. unsafe boundary conflict page: passed
- F. active-only no sold history: passed
- G. archive-only no active: passed
- H. sold_likely lane: passed
- I. expired_removed lane: passed
- J. accessory lane: passed
- K. related-not-substitute lane: passed
- L. source coverage limited: passed
- M. confidence disclosure: passed
- N. target price watch CTA: passed
- O. future placeholders: passed
- P. mobile layout priority: passed
- Q. desktop layout priority: passed
- R. copy safety: passed
- S. legal disclaimer: passed
- T. source-gap not absence: passed
- U. raw data display guard: passed

## 21. no fake-fill / source-gap / active-vs-sold UI guard
- related lane은 substitute가 아니라 context로만 표시한다.
- accessory lane은 model listing과 섞지 않는다.
- source-gap은 부재 확정이 아니라 coverage gap으로 표현한다.
- active asking reference와 sold history를 분리 표시한다.
- broad query에는 fast alert CTA를 노출하지 않는다.

## 22. actual frontend/API/DB/calculator 미구현 guard
- React component 없음
- HTML/CSS page 없음
- API route 없음
- DB query 없음
- price guide calculator 없음
- archive builder 없음

## 23. output JSON / production code 미수정 여부
- 이번 라운드는 contract artifact 생성만 포함한다.
- production crawler/search/parser/resolver/classifier/frontend runtime은 수정하지 않는다.

## 24. 테스트 결과
- runner and contract tests executed locally.

## 25. 남은 위험
- 실제 구현 라운드에서는 copy density, card hierarchy, CTA disable state, responsive truncation을 다시 검증해야 한다.
- 실제 frontend 연결 시 data-adapter bundle state names과 UI state names이 drift하지 않도록 묶는 단계가 필요하다.

## 26. 다음 backlog 후보
- P3-MODEL-MARKET-PAGE-FRONTEND-IMPLEMENTATION
- P3-EXPIRED-SOLD-LISTING-ARCHIVE-IMPLEMENTATION
- P3-PRICE-GUIDE-MARKET-INTELLIGENCE-IMPLEMENTATION
- P3-MODEL-MARKET-PAGE-DATA-ADAPTER-DB-INTEGRATION-CONTRACT
- P3-DEALER-LEAD-SIGNAL-CONTRACT

