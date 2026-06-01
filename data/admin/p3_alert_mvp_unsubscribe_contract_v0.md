# P3-ALERT-MVP-UNSUBSCRIBE-CONTRACT

## 작업 목적
- unsubscribe / pause / resume / delete / manage alert / privacy delete의 상태 전환과 suppression 정책을 contract로 정의한다.

## 구현 요약
- rendered email footer 링크 기준으로 unsubscribe/manage 요청 preview를 생성했다.
- single unsubscribe, unsubscribe all, pause/resume, delete, invalid/expired token, privacy delete를 분리했다.
- post-unsubscribe delivery skip preview를 추가했다.

## 결과 분포
- all_alerts_unsubscribed: 1
- already_unsubscribed: 1
- deleted: 1
- expired_token: 1
- invalid_token: 1
- manage_view_allowed: 1
- paused: 1
- privacy_delete_requested: 1
- resumed: 1
- unsubscribed: 4

## Suppression 분포
- privacy_delete: 1
- unsubscribe: 4
- unsubscribe_all: 1

## 수정 파일 목록
- alert_unsubscribe_contract.py
- scripts/run_p3_alert_mvp_unsubscribe_contract.py
- tests/test_alert_mvp_unsubscribe_contract.py
- data/admin/p3_alert_mvp_unsubscribe_contract_v0.md
- data/admin/p3_alert_mvp_unsubscribe_contract_v0.jsonl
- data/admin/alert_mvp_unsubscribe_contract_v0.json

## 수정하지 않은 파일/영역
- production search/parser/resolver/crawler code
- output JSON / taxonomy seed / canonical index / raw data / search index

## 다음 backlog 후보
- P3-ALERT-MVP-NO-RESULT-UI-CONTRACT
- P3-ALERT-MVP-DELIVERY-QUEUE-SCHEMA
- P3-ALERT-MVP-EMAIL-PROVIDER-ADAPTER-CONTRACT
- P3-ALERT-MVP-PREFERENCE-CENTER-CONTRACT
- P3-THIRD-PARTY-SOURCE-LIST-EXPANSION-IMPLEMENTATION
