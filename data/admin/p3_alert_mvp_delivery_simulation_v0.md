# P3-ALERT-MVP-DELIVERY-SIMULATION

## 작업 목적
- active subscription과 mock event를 매칭해 notification candidate/skip decision을 contract로 고정한다.

## 구현 요약
- active subscription preview를 verification/storage artifact에서 읽어 delivery target으로 만들었다.
- new_listing / source_gap_resolved / source_expansion_available / price_drop mock event를 정의했다.
- duplicate, inactive, suppressed, fake-fill, trigger-not-enabled 케이스를 분리했다.

## Delivery Contract 요약
- provider_send_enabled: False
- source_gap_listing_id_required: False
- medium_confidence_allowed_for_mvp: True

## Active Subscription / Mock Event
- active subscriptions: 16
- mock events: 12

## Notification Decision 분포
- queue_notification_preview: 10
- skip_duplicate: 2
- skip_no_match: 2
- skip_subscription_inactive: 3
- skip_suppressed: 1
- skip_trigger_not_enabled: 1

## Scenario Validation 분포
- duplicate_skip: 2
- fake_fill_guard: 2
- inactive_or_suppressed_skip: 4
- normal_new_listing_success: 5
- price_drop: 2
- source_expansion_waitlist: 2
- source_gap_resolved_success: 2

## Privacy / Provider Send
- raw email absent
- provider_message_id empty preview only
- no actual email send path

## 수정 파일 목록
- alert_delivery_contract.py
- scripts/run_p3_alert_mvp_delivery_simulation.py
- tests/test_alert_mvp_delivery_simulation.py
- data/admin/p3_alert_mvp_delivery_simulation_v0.md
- data/admin/p3_alert_mvp_delivery_simulation_v0.jsonl
- data/admin/alert_mvp_delivery_simulation_v0.json

## 수정하지 않은 파일/영역
- production search/parser/resolver/crawler code
- output JSON / taxonomy seed / canonical index / raw data / search index

## 다음 backlog 후보
- P3-ALERT-MVP-EMAIL-TEMPLATE-CONTRACT
- P3-ALERT-MVP-UNSUBSCRIBE-CONTRACT
- P3-ALERT-MVP-NO-RESULT-UI-CONTRACT
- P3-ALERT-MVP-DELIVERY-QUEUE-SCHEMA
- P3-THIRD-PARTY-SOURCE-LIST-EXPANSION-IMPLEMENTATION
