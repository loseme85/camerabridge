# P3-SOURCE-CHANGE-DETECTION-CONTRACT

## 1. 작업명
- P3-SOURCE-CHANGE-DETECTION-CONTRACT

## 2. 작업 목적
- freshness scheduler가 정한 crawl 시점 이후, source snapshot을 비교해 무엇이 실제로 바뀌었는지 domain-neutral core contract로 정의한다.

## 3. 구현 요약
- source snapshot, listing fingerprint, change set, listing change candidate, downstream route preview를 분리했다.
- page hash short-circuit, duplicate guard, source-gap fake-fill block, anti-bot/source health block을 preview artifact로 고정했다.

## 4. source change detection contract 요약
- source snapshot rows: 14
- listing fingerprint rows: 15
- change set rows: 14
- listing change candidate rows: 12

## 5. source snapshot schema
- snapshot_id / source_id / snapshot_type / page_hash / previous_snapshot_id / detail_crawl_allowed / fetch_status 포함
- same page hash면 detail crawl 생략 가능

## 6. listing fingerprint schema
- listing_url_fingerprint / source_listing_id / normalized_title_fingerprint / price_fingerprint / availability_status 포함
- raw URL 대신 fingerprint만 사용

## 7. change set schema
- source_change_status와 new/updated/price_changed/removed/duplicate/manual_review count를 함께 기록

## 8. listing change candidate schema
- change_confidence / price_change_percent / availability_transition / detection_delay_estimate_minutes / downstream_route / fake_fill_detected 포함

## 9. source-gap resolution policy
- exact resolution candidate rows: 1
- Sigma 14-24 L exact candidate만 resolution review 또는 fast alert candidate로 연결

## 10. source-expansion policy
- source expansion candidate rows: 1
- source expansion은 source_expansion_review로 우선 라우팅

## 11. duplicate detection policy
- duplicate detection rows: 1
- duplicate candidate는 ignore_duplicate로 내려가며 new listing으로 승격하지 않음

## 12. removed/sold detection policy
- removed/sold detection rows: 2
- sold/removed candidate는 alert send path가 아니라 price guide/history 경로로 이동

## 13. timestamp / metric policy
- source_published_at, first_seen_at, last_seen_at, candidate_created_at, detection_delay_estimate_minutes 포함

## 14. downstream routing policy
- candidate distribution: {'new_listing_candidate': 2, 'price_changed': 1, 'availability_changed': 1, 'duplicate_candidate': 1, 'source_gap_resolved_candidate': 1, 'low_confidence_candidate': 3, 'source_expansion_candidate': 1, 'manual_review_required': 1, 'removed_or_sold_candidate': 1}
- high confidence rare listing -> fast_alert_path_candidate
- broad/manual-review/fake-fill -> full_normalization_queue or manual_review_queue

## 15. unchanged / new / price-change / sold scenario 결과
- unchanged source page -> ignore_unchanged, detail_crawl_allowed=false
- 35 lux aa / Noctilux 50 0.95 -> new_listing_candidate, fast path eligible
- Summilux-M 35 price drop -> price_changed
- M6 sold / APO-Telyt-R 180 removed -> fast path false

## 16. source-gap exact / fake-fill blocked 결과
- Sigma 14-24 L exact candidate -> source_gap_resolved_candidate
- Leica SL 14-24 / Sigma 24-70 adjacent candidates -> fake_fill_detected=true

## 17. broad/manual-review 제외 결과
- summicron broad query -> low_confidence_candidate, no direct fast path
- Leica M10-R -> manual_review_required, manual_review_queue

## 18. anti-bot/source health guard 결과
- Mercari Japan preview -> skipped_anti_bot_guard, detail_crawl_allowed=false

## 19. output JSON / production code 미수정 여부
- production crawler/search/parser/resolver/classifier code는 수정하지 않았다.

## 20. 테스트 결과
- script, tests, jsonl validation, py_compile, golden_set 기준으로 검증

## 21. 남은 위험
- cross-source duplicate는 이번 라운드에서 preview만 정의했고 실구현은 후속 backlog
- source_published_at 부재 source에서는 detection delay precision이 낮을 수 있음

## 22. 다음 backlog 후보
- P3-FAST-ALERT-PATH-CONTRACT
- P3-SOURCE-CHANGE-DETECTION-IMPLEMENTATION
- P3-CRAWL-FRESHNESS-SCHEDULER-IMPLEMENTATION
- P3-ALERT-MVP-PREFERENCE-CENTER-CONTRACT
- P3-WATCH-BRIDGE-MARKET-SCOUT-CONTRACT
