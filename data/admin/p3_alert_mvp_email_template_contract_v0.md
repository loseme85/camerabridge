# P3-ALERT-MVP-EMAIL-TEMPLATE-CONTRACT

## 작업 목적
- queue_notification_preview 후보에 대해 이메일 템플릿 구조와 문구 원칙을 contract로 정의한다.

## 구현 요약
- queued decision만 rendered preview를 만들고 skipped/fake-fill은 no-email preview로 분리했다.
- source-gap resolved와 실제 new listing을 문구상 명확히 분리했다.

## Template Type별 Preview 분포
- normal_new_listing: 5
- price_drop: 1
- source_expansion_available: 2
- source_gap_new_listing: 1
- source_gap_resolved: 1

## Skipped / No Email 분포
- blocked_fake_fill: 2
- skipped_no_email: 7

## 문구 원칙
- 한국어 기본
- 짧고 신뢰감 있게
- 과장 표현 금지
- source-gap resolved는 실제 매물 발견처럼 쓰지 않음
- source expansion available도 실제 매물 발견처럼 쓰지 않음

## 수정 파일 목록
- alert_email_template_contract.py
- scripts/run_p3_alert_mvp_email_template_contract.py
- tests/test_alert_mvp_email_template_contract.py
- data/admin/p3_alert_mvp_email_template_contract_v0.md
- data/admin/p3_alert_mvp_email_template_contract_v0.jsonl
- data/admin/alert_mvp_email_template_contract_v0.json

## 수정하지 않은 파일/영역
- production search/parser/resolver/crawler code
- output JSON / taxonomy seed / canonical index / raw data / search index

## 다음 backlog 후보
- P3-ALERT-MVP-UNSUBSCRIBE-CONTRACT
- P3-ALERT-MVP-NO-RESULT-UI-CONTRACT
- P3-ALERT-MVP-DELIVERY-QUEUE-SCHEMA
- P3-ALERT-MVP-EMAIL-PROVIDER-ADAPTER-CONTRACT
- P3-THIRD-PARTY-SOURCE-LIST-EXPANSION-IMPLEMENTATION
