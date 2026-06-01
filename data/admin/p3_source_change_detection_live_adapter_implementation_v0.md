# P3-SOURCE-CHANGE-DETECTION-LIVE-ADAPTER-IMPLEMENTATION

## 1. 작업명
P3-SOURCE-CHANGE-DETECTION-LIVE-ADAPTER-IMPLEMENTATION

## 2. 작업 목적
source_change_detection_live_adapter_contract.py의 raw fetch/listing -> adapted snapshot/listing mapping 규칙을 provider-neutral local adapter 코드로 옮긴다.

## 3. 구현 요약
- raw fetch/listing preview를 검증하고 privacy guard를 적용한 뒤 adapted snapshot/listing row로 변환했다.
- adapted output을 local repository preview에 저장하고 source_change_detection.py compare/create_change_set까지 연결했다.
- 실제 live crawl 없이도 anti-bot, parse_failed, missing identity, duplicate raw rows, unchanged/price-change/sold-change 흐름을 검증했다.

## 4. Live Adapter Implementation Scope
- local preview only
- no live crawl
- no production crawler integration
- no DB connection

## 5. Public API
- `create_live_adapter_policy`
- `validate_raw_fetch`
- `validate_raw_listing`
- `enforce_raw_input_privacy`
- `normalize_text_for_fingerprint`
- `build_safe_fingerprint`
- `build_listing_url_fingerprint`
- `build_normalized_title_fingerprint`
- `build_price_fingerprint`
- `build_seller_or_dealer_fingerprint`
- `build_condition_hint_fingerprint`
- `map_availability_status`
- `map_price_preview`
- `map_source_published_at`
- `adapt_raw_listing_to_listing_row`
- `dedupe_adapted_listing_rows`
- `build_adapter_page_hash`
- `adapt_raw_fetch_to_source_snapshot`
- `persist_adapted_snapshot_and_listings`
- `create_source_change_detection_input`
- `run_source_change_detection_from_adapted_input`
- `process_raw_source_batch`
- `process_adapter_scenarios`

## 6. Raw Fetch/Listing Validation 결과
- adapted_source_snapshot rows = `15`
- adapted_listing_row rows = `13`
- missing identity rows are rejected before source_change pass-through.

## 7. Privacy Enforcement 결과
- storage raw flags: email=`False` url=`False` html=`False` payload=`False`
- raw source/listing/image URL and raw HTML keys are blocked.

## 8. Fingerprint/Page Hash 결과
- listing_url/title/price/seller/condition/image fingerprints are deterministic.
- page hash is built from sorted stable listing fingerprints, so order-only changes do not move it.

## 9. Availability/Price/Date Mapping 결과
- EN/KO/JP availability text maps into available/reserved/sold/unavailable/unknown.
- numeric price, POA/ASK, and KRW/JPY/USD/GBP/EUR preview flows are handled.
- source_published_at stays null when the source did not provide it.

## 10. Adapted Listing Row / Source Snapshot 결과
- adapted rows remain source_change_detection.py compatible preview rows.
- blocked or failed fetches still yield safe snapshot metadata, but do not pass listing rows forward.

## 11. Duplicate Raw Listing 처리 결과
- duplicate raw rows are deduped before source_change_detection and before storage persistence.

## 12. Persistent Storage 연동 결과
- adapted snapshots go through persistent_alert_storage.create_source_snapshot_pair.
- adapted listing rows go through persistent_alert_storage.upsert_listing_observation.

## 13. source_change_detection.py 연동 결과
- unchanged short-circuit verified with matching page hashes.
- price_changed and availability_changed/sold paths verified across snapshots.

## 14. Scenario Validation 결과
- scenario_validation_rows = `15`

## 15. Raw URL/HTML/Image URL/Privacy Guard
- adapted snapshot/listing outputs always keep raw_url_present=false and raw_html_present=false.
- storage export also keeps all raw flags false.

## 16. Output JSON / Production Code 미수정 여부
- 이번 라운드는 local adapter preview + artifact 생성만 포함한다.
- production crawler/search/parser/resolver/classifier/cron/DB/provider/frontend 코드는 수정하지 않는다.

## 17. 테스트 결과
- implementation tests, runner, JSONL validation, and golden_set expected to pass

## 18. 남은 위험
- source-specific selector robustness는 아직 fixture 수준이다.
- live adapter concurrency/fetch retry는 cron/runtime 구현 단계에서 다시 붙여야 한다.

## 19. 다음 Backlog 후보
- P3-CRAWL-FRESHNESS-SCHEDULER-CRON-IMPLEMENTATION
- P3-UNSUBSCRIBE-MANAGE-ENDPOINT-CONTRACT
- P3-EMAIL-PROVIDER-SEND-ENABLEMENT-CONTRACT
- P3-PRIVATE-BETA-RUNBOOK
- P3-ALERT-MVP-LANDING-PAGE-COPY-IMPLEMENTATION
