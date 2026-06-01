# P3-MODEL-MARKET-PAGE-PUBLIC-ROUTE-CONTRACT

## 1. 작업명
P3-MODEL-MARKET-PAGE-PUBLIC-ROUTE-CONTRACT

## 2. 작업 목적
Model Market Page를 public route로 열기 전에 route boundary, route state, SEO/meta safety, response safety, noindex/fallback policy를 계약으로 정의한다.

## 3. 진행률
- 기준: P3 Market Intelligence / Model Market Page preview-to-public-route readiness
- 시작 전: 약 87%
- 이번 라운드 완료 후: 약 91%
- 증가분: +4%p

## 4. 구현 요약
- public route path/state, slug resolution, public response safety, SEO/meta safety, indexing/robots, CTA exposure, fallback, analytics 경계를 정의했다.
- broad query는 refine route로, unsafe boundary는 review-safe/noindex route로, source-gap은 honest gap route로 고정했다.
- 실제 route/API/frontend/SEO runtime은 만들지 않았다.

## 5. Public Route contract scope
- 포함: route pattern/state, slug resolution, response safety, SEO/meta safety, indexing, CTA route contract, fallback, analytics, progress report.
- 제외: actual Next.js route, actual API response, DB query, server handler, SEO runtime, frontend page/component.

## 6. policy
- contract_only = True
- actual_route_enabled = False
- api_route_enabled = False
- frontend_page_enabled = False
- db_query_enabled = False
- seo_runtime_enabled = False
- production_route_enabled = False

## 7. route pattern contract
- /camera-bridge/models/:model_slug: allowed=exact_model_public_market_page, exact_rare_variant_public_market_page, active_only_public_page, archive_only_public_page, insufficient_sold_history_public_page
- /camera-bridge/market/:model_slug: allowed=exact_model_public_market_page, exact_rare_variant_public_market_page, source_gap_public_page, active_only_public_page, archive_only_public_page, insufficient_sold_history_public_page
- /camera-bridge/search/:query: allowed=broad_query_refinement_route
- /camera-bridge/source-gap/:model_slug: allowed=source_gap_public_page
- /camera-bridge/unsupported/:slug: allowed=unsupported_model_route
- /camera-bridge/refine/:query: allowed=broad_query_refinement_route

## 8. route state contract
- exact_model_public_market_page: index=True / noindex=False / price_widget=True
- exact_rare_variant_public_market_page: index=True / noindex=False / price_widget=True
- source_gap_public_page: index=False / noindex=True / price_widget=False
- active_only_public_page: index=True / noindex=False / price_widget=True
- archive_only_public_page: index=True / noindex=False / price_widget=False
- insufficient_sold_history_public_page: index=True / noindex=False / price_widget=True
- broad_query_refinement_route: index=False / noindex=True / price_widget=False
- unsafe_boundary_review_route: index=False / noindex=True / price_widget=False
- unsupported_model_route: index=False / noindex=True / price_widget=False
- privacy_blocked_route: index=False / noindex=True / price_widget=False
- db_unavailable_safe_route: index=False / noindex=True / price_widget=False
- stale_data_safe_route: index=True / noindex=False / price_widget=True
- error_safe_fallback_route: index=False / noindex=True / price_widget=False

## 9. slug / canonical resolution contract
- exact slug -> exact_model_public_market_page / redirect=None
- exact rare variant slug -> exact_rare_variant_public_market_page / redirect=None
- source-gap slug -> source_gap_public_page / redirect=None
- broad query -> broad_query_refinement_route / redirect=/camera-bridge/refine/:query
- unsafe boundary -> unsafe_boundary_review_route / redirect=None
- unsupported -> unsupported_model_route / redirect=/camera-bridge/unsupported/:slug
- slug mismatch -> exact_model_public_market_page / redirect=canonical_redirect
- slug conflict -> error_safe_fallback_route / redirect=None
- unknown slug -> unsupported_model_route / redirect=/camera-bridge/unsupported/:slug

## 10. public response safety contract
- market_page_public_response_safe_fields: allowed=24 / blocked=20

## 11. SEO / metadata contract
- exact_model_public_market_page: robots=index,follow / structured_data_allowed=False
- source_gap_public_page: robots=noindex,follow / structured_data_allowed=False
- broad_query_refinement_route: robots=noindex,follow / structured_data_allowed=False
- unsafe_boundary_review_route: robots=noindex,follow / structured_data_allowed=False
- unsupported_model_route: robots=noindex,follow / structured_data_allowed=False

## 12. indexing / robots contract
- index_allowed: states=exact_model_public_market_page, exact_rare_variant_public_market_page, active_only_public_page, archive_only_public_page, insufficient_sold_history_public_page
- noindex_source_gap_optional: states=source_gap_public_page
- noindex_required_broad: states=broad_query_refinement_route
- noindex_required_unsafe_boundary: states=unsafe_boundary_review_route
- noindex_required_unsupported: states=unsupported_model_route
- noindex_required_privacy_blocked: states=privacy_blocked_route
- noindex_required_db_unavailable: states=db_unavailable_safe_route, error_safe_fallback_route
- stale_but_index_allowed_with_warning: states=stale_data_safe_route

## 13. CTA route contract
- watch_this_model: aggregate_only=True / future=False
- watch_this_exact_variant: aggregate_only=True / future=False
- rare_new_listing_alert: aggregate_only=True / future=False
- source_gap_alert: aggregate_only=True / future=False
- request_source: aggregate_only=True / future=False
- target_price_watch: aggregate_only=True / future=False
- smart_deal_future: aggregate_only=True / future=True
- export_price_data_future: aggregate_only=True / future=True
- dealer_visibility_future: aggregate_only=True / future=True

## 14. fallback / error route contract
- route_not_found: unsupported_model_fallback
- slug_conflict: error_safe_fallback_route
- canonical_resolution_failed: unsupported_model_fallback
- db_projection_unavailable: db_unavailable_safe_route
- frontend_state_unavailable: error_safe_fallback_route
- privacy_filter_failed: privacy_blocked_route
- source_gap_fallback: source_gap_public_page
- unsafe_boundary_fallback: unsafe_boundary_review_route
- safe_empty_market_page: safe_empty_market_page
- unsupported_model_fallback: unsupported_model_route

## 15. analytics / event contract
- model_page_view: allowed=model_slug, canonical_model_id, route_state
- source_gap_page_view: allowed=model_slug, canonical_model_id, route_state
- refinement_page_view: allowed=model_slug, route_state
- watch_cta_click: allowed=canonical_model_id, route_state
- target_price_cta_click: allowed=canonical_model_id, route_state
- source_gap_cta_click: allowed=canonical_model_id, route_state
- unsafe_boundary_view: allowed=canonical_model_id, route_state
- unsupported_model_view: allowed=model_slug, route_state
- route_privacy_block: allowed=route_state
- route_fallback: allowed=route_state, canonical_model_id

## 16. privacy response check 결과
- raw_url_response_block: blocked
- raw_html_response_block: blocked
- raw_email_response_block: blocked
- user_email_response_block: blocked
- provider_payload_response_block: blocked
- webhook_body_response_block: blocked
- raw_fetch_response_block: blocked
- raw_selector_output_block: blocked
- public_response_safe_fields_only: enforced

## 17. SEO claim safety check 결과
- blocked_claim_count = 17
- all sources: blocked
- guaranteed price: blocked
- official leica: blocked
- 100% accurate: blocked
- best deal guaranteed: blocked
- real-time all dealer alerts: blocked
- investment advice: blocked
- confirmed absence: blocked
- confirmed sold price: blocked
- 모든 사이트: blocked

## 18. scenario validation 결과
- pass = 26/26
- A. exact Noctilux public route: passed
- B. 35 lux AA rare variant route: passed
- C. Sigma source-gap route: passed
- D. broad Summicron query: passed
- E. unsafe boundary conflict: passed
- F. unsupported model: passed
- G. active-only page: passed
- H. archive-only page: passed
- I. insufficient sold history: passed
- J. stale data page: passed
- K. privacy blocked response: passed
- L. raw URL attempted in response: passed
- M. user email attempted in response: passed
- N. provider payload attempted in response: passed
- O. slug mismatch: passed
- P. slug conflict: passed
- Q. DB unavailable: passed
- R. frontend state unavailable: passed
- S. SEO exact page: passed
- T. SEO source-gap page: passed
- U. SEO unsafe/broad/unsupported: passed
- V. CTA aggregate safety: passed
- W. analytics safety: passed
- X. structured data safety: passed
- Y. public response safe fields: passed
- Z. progress report: passed

## 19. no fake-fill / source-gap / raw-data / SEO overclaim guard 결과
- broad query는 direct public market page가 아니라 refinement route로 보낸다.
- source-gap은 confirmed absence가 아니라 coverage gap으로만 표현한다.
- unsafe boundary에서는 public price widget과 CTA를 열지 않는다.
- public response와 analytics에서 raw URL/HTML/email/provider payload를 차단한다.
- SEO/meta copy에서 all sources / guaranteed / official / investment advice 계열 표현을 차단한다.

## 20. actual route/API/frontend/DB 미구현 guard
- actual Next.js route 없음
- actual API endpoint 없음
- actual server handler 없음
- actual DB query 없음
- actual SEO runtime 없음
- actual frontend page/component 없음

## 21. output JSON / production code 미수정 여부
- 이번 라운드는 contract artifact만 생성한다.
- production runtime surface, taxonomy seed, canonical index, raw data, search index, output JSON production surface는 수정하지 않는다.

## 22. 테스트 결과
- contract_check_count = 5

## 23. 남은 위험
- 다음 public-route implementation 단계에서는 canonical redirect precedence, robots header/runtime wiring, CTA aggregate hydration이 실제 runtime과 어긋나지 않도록 다시 검증해야 한다.
- structured data는 현재 보수적으로 닫혀 있으므로, 추후 노출 시에도 price/raw link/user data가 새지 않도록 별도 구현 검토가 필요하다.

## 24. 다음 backlog 후보
- P3-DEALER-LEAD-SIGNAL-CONTRACT
- P3-PRIVATE-BETA-MARKET-PAGE-READINESS-CHECKLIST
- P3-MARKET-PAGE-DB-READ-ADAPTER-IMPLEMENTATION
- P3-EXPIRED-SOLD-LISTING-ARCHIVE-DB-IMPLEMENTATION
- P3-MODEL-MARKET-PAGE-PUBLIC-ROUTE-IMPLEMENTATION

