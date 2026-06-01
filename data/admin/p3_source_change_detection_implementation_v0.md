# P3-SOURCE-CHANGE-DETECTION-IMPLEMENTATION

## 작업 목적
- source snapshot diff를 순수 함수 모듈로 구현
- page hash short-circuit, listing fingerprint comparison, source-gap fake-fill guard를 deterministic하게 검증

## 구현 요약
- `source_change_detection.py`는 snapshot/listing rows만 받아 change set과 listing candidates를 생성합니다.
- live crawl, provider send, production crawler/search 변경 없이 synthetic fixture 기반으로 동작을 검증했습니다.

## source_change_detection.py public API
- `build_page_hash`
- `build_listing_fingerprint`
- `compare_source_snapshots`
- `detect_listing_changes`
- `classify_listing_change`
- `detect_duplicates`
- `route_change_candidate`
- `detect_source_gap_resolution`
- `create_change_set`

## page hash short-circuit 결과
- unchanged scenario: `Map Camera`
- detail comparison skipped
- downstream candidates: `0`

## listing fingerprint comparison 결과
- source listing id
- listing url fingerprint
- title/seller/price similarity fallback
- duplicate-like relist detection included

## new / price / sold / removed scenario 결과
- true rare new listing: `35 lux aa`, `noctilux m 50 0.95`
- price changed: `summilux m 35`
- sold: `m6`
- removed: `r 180 apo telyt`

## duplicate detection 결과
- duplicate relist is downgraded to `duplicate_candidate`
- downstream route: `ignore_duplicate`

## source-gap exact / fake-fill blocked 결과
- exact: `sigma 14-24 l` -> `source_gap_resolved_candidate`
- fake fill: `Leica SL 14-24`, `Sigma 24-70` -> manual review, no fast path

## source-expansion 결과
- `sigma 28-70 dg dn l` -> `source_expansion_candidate`

## broad/manual-review guard 결과
- `summicron` -> refinement/full normalization path
- `leica m10-r` -> `manual_review_required`

## anti-bot/source health guard 결과
- `Mercari Japan` high risk snapshot blocks detail crawl

## downstream route / fast alert compatibility
- candidate fields align with fast alert input mapping
- route counts: `{'new_listing_candidate': 2, 'price_changed': 1, 'availability_changed': 1, 'removed_or_sold_candidate': 1, 'duplicate_candidate': 1, 'source_gap_resolved_candidate': 1, 'low_confidence_candidate': 3, 'source_expansion_candidate': 1, 'manual_review_required': 1}`

## raw URL/privacy guard
- output candidates store `raw_url_present=false`
- fixture rows include only fingerprint previews

## 테스트 결과
- scenario validations passed: `14/14`
- jsonl rows: `109`
