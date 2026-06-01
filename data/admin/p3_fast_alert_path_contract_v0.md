# P3-FAST-ALERT-PATH-CONTRACT

## 1. 작업명
- P3-FAST-ALERT-PATH-CONTRACT

## 2. 작업 목적
- source change detection 후보 중 즉시 delivery queue preview로 올릴 수 있는 것만 선별하는 core fast alert gate를 정의한다.

## 3. 구현 요약
- fast alert input -> lightweight normalization -> watchlist match -> condition match -> confidence guard -> queue/blocked preview 흐름을 분리했다.
- fake fill, broad query, manual review, duplicate, sold/removed, unverified, suppressed, source health block을 즉시 queue 전에 막았다.

## 4. fast alert path contract 요약
- input candidate rows: 22
- queue candidate rows: 7
- blocked candidate rows: 15

## 5. input candidate schema
- source change candidate id, watch_target_class, downstream_route_from_change_detection, duplicate/false_positive risk, source health를 포함

## 6. lightweight normalization schema
- fast path용 lightweight normalization confidence와 full normalization fallback 여부를 기록

## 7. watchlist match schema
- verified/active/pending subscription count와 trigger_type, digest/source-gap/conditional-rare flag 포함

## 8. condition match schema
- conditional rare용 price/overlay/source-region/availability condition result를 분리

## 9. confidence guard schema
- fake_fill_detected, duplicate_risk_score, false_positive_risk_score, source_health_blocked 기준으로 최종 gate를 둠

## 10. queue candidate schema
- delivery_queue_compatible/provider_adapter_compatible preview, dedupe_key_preview, alert_pipeline_delay_minutes 포함

## 11. blocked candidate schema
- block_reason과 downstream_route_after_block을 별도로 남겨 fast path 탈락 이후 경로를 고정

## 12. route policy
- queue event distribution: {'rare_new_listing': 2, 'price_drop': 1, 'source_gap_resolved': 1, 'source_expansion_available': 1, 'conditional_rare_match': 1, 'smart_deal_match': 1}
- blocked reason distribution: {'sold_or_removed': 2, 'duplicate_listing': 1, 'fake_fill_detected': 2, 'condition_not_met': 3, 'broad_query_refinement_required': 3, 'manual_review_required': 1, 'anti_bot_guard': 1, 'missing_verified_subscription': 1, 'email_suppressed': 1}

## 13. true rare / price drop 결과
- 35 lux aa / Noctilux 50 0.95 -> eligible_immediate, urgent rare_new_listing
- Summilux-M 35 price drop -> eligible_price_drop_opt_in, high price_drop

## 14. source-gap exact / fake-fill blocked 결과
- Sigma 14-24 exact -> eligible_source_gap_exact, high source_gap_resolved
- Leica SL 14-24 / Sigma 24-70 adjacent candidates -> blocked fake_fill_detected

## 15. conditional rare 결과
- Q2 under target price / Summicron-M 50 boxed under price -> eligible_after_condition_match
- Q2 above target price -> blocked condition_not_met

## 16. common watch / digest 결과
- Lumix 24-105 / SL 24-90 generic -> no urgent queue, digest_later

## 17. broad/manual-review 제외 결과
- summicron / summilux / leica m -> broad_query_refinement_required
- Leica M10-R -> manual_review_required

## 18. sold/duplicate/source-health block 결과
- M6 sold / APO-Telyt-R 180 removed -> sold_or_removed
- duplicate listing -> ignore_duplicate
- Mercari Japan high risk source -> anti_bot_guard

## 19. subscription/suppression guard 결과
- pending-only subscription -> missing_verified_subscription
- suppressed recipient -> email_suppressed

## 20. latency metric 결과
- detection delay / fast path processing delay / alert pipeline delay preview 포함

## 21. delivery queue/provider adapter compatibility
- queue candidate preview는 delivery queue/provider adapter contract에 맞는 shape만 만든다.

## 22. output JSON / production code 미수정 여부
- production crawler/search/parser/resolver/classifier/frontend/provider send path는 수정하지 않았다.

## 23. 테스트 결과
- script, tests, jsonl validation, py_compile, golden_set 기준으로 검증

## 24. 남은 위험
- common watch의 smart deal threshold는 이후 implementation round에서 더 정교한 calibration 필요
- source_expansion_available를 immediate path로 볼지 여부는 vertical별 정책 확장 여지가 있음

## 25. 다음 backlog 후보
- P3-FAST-ALERT-PATH-IMPLEMENTATION
- P3-SOURCE-CHANGE-DETECTION-IMPLEMENTATION
- P3-CRAWL-FRESHNESS-SCHEDULER-IMPLEMENTATION
- P3-ALERT-MVP-PREFERENCE-CENTER-CONTRACT
- P3-WATCH-BRIDGE-MARKET-SCOUT-CONTRACT
