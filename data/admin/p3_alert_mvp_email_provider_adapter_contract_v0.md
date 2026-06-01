# P3-ALERT-MVP-EMAIL-PROVIDER-ADAPTER-CONTRACT

## 작업 목적
- queue job을 실제 provider 호출 전 단계의 provider-neutral request/result/webhook preview로 정의한다.

## 구현 요약
- queued job만 provider send request preview를 생성한다.
- skipped/inactive/suppressed/fake-fill/permanent-failure queue row는 provider request를 만들지 않는다.
- provider별 full payload 대신 mapping preview만 남기고, provider_send_enabled는 false로 유지한다.

## Provider Request 분포
- prepared_preview: 10

## Skipped Provider Request 분포
- blocked_inactive: 3
- blocked_missing_required_context: 5
- blocked_suppressed: 1

## 수정 파일 목록
- alert_email_provider_adapter_contract.py
- scripts/run_p3_alert_mvp_email_provider_adapter_contract.py
- tests/test_alert_mvp_email_provider_adapter_contract.py
- data/admin/p3_alert_mvp_email_provider_adapter_contract_v0.md
- data/admin/p3_alert_mvp_email_provider_adapter_contract_v0.jsonl
- data/admin/alert_mvp_email_provider_adapter_contract_v0.json

## 수정하지 않은 파일/영역
- production search/parser/resolver/crawler code
- output JSON / taxonomy seed / canonical index / raw data / search index
