# P3-ALERT-MVP-DELIVERY-QUEUE-SCHEMA

## 작업 목적
- delivery simulation에서 queue 가능하다고 판정된 notification candidate를 provider 발송 전 queue job schema로 정리한다.

## 구현 요약
- rendered email preview가 있는 queued decision만 queue job으로 만든다.
- duplicate / suppressed / inactive / fake-fill / trigger-not-enabled는 skipped preview로 분리한다.
- retry, expiry, pre-dispatch suppression을 preview row로 따로 기록한다.

## Queued Job 분포
- email_notification: 6
- price_drop_notification: 1
- source_expansion_update: 2
- source_gap_update: 1

## Skipped Preview 분포
- cancelled: 2
- failed_permanent: 1
- skipped_duplicate: 2
- skipped_inactive: 3
- skipped_suppressed: 1

## 수정 파일 목록
- alert_delivery_queue_contract.py
- scripts/run_p3_alert_mvp_delivery_queue_schema.py
- tests/test_alert_mvp_delivery_queue_schema.py
- data/admin/p3_alert_mvp_delivery_queue_schema_v0.md
- data/admin/p3_alert_mvp_delivery_queue_schema_v0.jsonl
- data/admin/alert_mvp_delivery_queue_schema_v0.json

## 수정하지 않은 파일/영역
- production search/parser/resolver/crawler code
- output JSON / taxonomy seed / canonical index / raw data / search index
