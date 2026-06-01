# P3-UNSUBSCRIBE-MANAGE-ENDPOINT-CONTRACT

## 1. 작업명
P3-UNSUBSCRIBE-MANAGE-ENDPOINT-CONTRACT

## 2. 작업 목적
manage/unsubscribe link가 가져야 할 token, request/response, preference/storage/delivery effect contract를 정의한다.

## 3. 구현 요약
- token hash only policy, endpoint request/response schema, token validation, preference center compatibility, storage effect, delivery queue effect, provider webhook mapping을 contract로 정리했다.
- 실제 HTTP endpoint/frontend/auth/DB/provider send 없이 boundary와 effect만 정의했다.

## 4. Unsubscribe/Manage Endpoint Contract Scope
- endpoint boundary only
- no actual HTTP endpoint
- no actual frontend/manage page
- no actual auth/session or DB connection

## 5. Token Policy / Token Schema
- token_preview rows = `18`
- token_validation_result rows = `18`
- raw token is never stored; token_hash only.

## 6. Manage Endpoint Request/Response Schema
- actions include pause/resume/digest conversion/price condition/source filters/price drop/source-gap/unsubscribe/privacy delete/view preferences.

## 7. Unsubscribe Endpoint Request/Response Schema
- scopes include single_subscription/all_alerts/digest_only/source_gap_only/provider_complaint/provider_unsubscribe.

## 8. Token Validation Rules
- valid/expired/invalid/revoked/already_used/scope mismatch/suppressed/privacy delete pending are covered.

## 9. Preference Center Compatibility
- endpoint actions map into alert_preference_center.py action previews and downstream fast/delivery effects.

## 10. Persistent Storage Effect
- affected domains preview: preference_profile, alert_subscription, preference_update_event, unsubscribe_event, suppression_event, delivery_queue_job, audit_log_event.

## 11. Delivery Queue Effect
- queue effects preview: no_effect, future_jobs_blocked, queued_jobs_should_be_cancelled, queued_jobs_require_pre_dispatch_check, digest_jobs_only, global_unsubscribe_block.

## 12. Email Template/Provider Compatibility
- placeholder refs only: `{{MANAGE_ALERT_URL}}`, `{{UNSUBSCRIBE_URL}}`.
- provider complaint/bounce/unsubscribe preview events map to suppression or unsubscribe effects.

## 13. Security/Abuse Guard
- endpoint_security_check rows = `18`
- replay/scope/expiry/no enumeration/raw token guard are required.

## 14. Provider Webhook Mapping
- provider_webhook_mapping_preview rows = `3`

## 15. Scenario Validation 결과
- scenario_validation rows = `18`
- failed scenarios = `[]`

## 16. Raw Token/Email/URL/Provider Payload Guard
- raw token/email/url/provider payload are disallowed across request/response/token preview shapes.

## 17. Output JSON / Production Code 미수정 여부
- 이번 라운드는 contract artifact만 생성한다.
- actual endpoint/frontend/auth/DB/provider/webhook/crawler production 코드는 수정하지 않는다.

## 18. 테스트 결과
- contract tests, runner, JSONL validation, and golden_set expected to pass

## 19. 남은 위험
- actual token issuance/rotation and signature verification runtime은 다음 implementation 라운드에서 구체화되어야 한다.
- global unsubscribe confirmation UX와 provider webhook trust boundary는 endpoint implementation에서 다시 고정해야 한다.

## 20. 다음 Backlog 후보
- P3-EMAIL-PROVIDER-SEND-ENABLEMENT-CONTRACT
- P3-PRIVATE-BETA-RUNBOOK
- P3-ALERT-MVP-LANDING-PAGE-COPY-IMPLEMENTATION
- P3-PERSISTENT-ALERT-STORAGE-DB-ADAPTER-CONTRACT
- P3-UNSUBSCRIBE-MANAGE-ENDPOINT-IMPLEMENTATION
