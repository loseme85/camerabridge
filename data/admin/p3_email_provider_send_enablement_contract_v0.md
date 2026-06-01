# P3-EMAIL-PROVIDER-SEND-ENABLEMENT-CONTRACT

## 1. 작업명
P3-EMAIL-PROVIDER-SEND-ENABLEMENT-CONTRACT

## 2. 작업 목적
preview-only email provider adapter를 실제 send로 전환하기 전에 필요한 gate, boundary, safety policy, webhook/storage 연결 조건을 contract로 정의한다.

## 3. 구현 요약
- provider send enablement policy, phases, gates, pre-dispatch safety checks, provider boundaries, credential/domain/webhook readiness, idempotency/rate-limit policy, and send decisions를 contract로 정리했다.
- 현재 상태에서 provider_send_enabled=true를 허용하지 않고, private beta/public/prod send readiness도 명확히 blocked로 남겼다.

## 4. Send Enablement Contract Scope
- contract only
- no actual provider SDK call
- no actual provider payload generation
- no actual webhook endpoint implementation

## 5. Send Enablement Policy
- provider_send_enabled_default=false
- actual_send_allowed_in_this_round=false
- raw email/provider payload/webhook body storage disallowed

## 6. Send Enablement Phases
- phase rows = `7`
- preview_only/provider_payload_preview/sandbox/internal/private/public/production phases included

## 7. Send Enablement Gates
- gate rows = `16`
- verified/suppression/unsubscribe/template/provider/rate/webhook/monitoring/privacy gates included

## 8. Pre-Dispatch Safety Check
- pre_dispatch rows = `18`
- blocks unverified/paused/global unsubscribe/suppressed/privacy delete/template unsafe/duplicate/rate/provider-not-ready/policy violation

## 9. Provider Send Request Boundary
- recipient_ref/email_hash/encrypted_ref boundary only
- no raw email persistence
- no provider payload persistence

## 10. Provider Credential/Domain Readiness
- provider_neutral is preview-only
- resend/sendgrid/aws_ses remain blocked until credentials/domain/webhooks are configured

## 11. Provider Payload Boundary
- payload generation stays runtime-only-later
- payload storage/logging forbidden
- provider_message_id storage is not allowed as raw value in this contract

## 12. Idempotency / Duplicate Send Policy
- delivery_job_id + provider_type + template_ref basis
- duplicate send -> blocked_duplicate_send

## 13. Rate Limit / Quota Policy
- provider-specific minute/hour/day preview limits defined
- internal real send would start with very low quotas

## 14. Webhook Readiness
- bounce/complaint/unsubscribe webhook readiness required before any real send phase
- raw webhook body storage remains forbidden

## 15. Delivery Queue / Storage Compatibility
- delivery_queue_job/provider_request_event/provider_result_event/webhook_event/unsubscribe_event/suppression_event/audit_log_event compatibility defined through safe refs

## 16. Scenario Validation 결과
- scenario rows = `18`
- failed scenarios = `[]`

## 17. Raw Email/Provider Payload/Webhook Body Guard
- raw email/provider payload/webhook body are blocked from persistence across the contract surface

## 18. Output JSON / Production Code 미수정 여부
- 이번 라운드는 contract artifact만 생성한다.
- actual provider send/webhook/DB/auth/frontend/crawler production 코드는 수정하지 않는다.

## 19. 테스트 결과
- contract tests, runner, JSONL validation, and golden_set expected to pass

## 20. 남은 위험
- actual provider credential bootstrap, secret handling, payload redaction in runtime logs, and webhook signature enforcement are still implementation backlog items.
- compliance copy and monitoring thresholds still need operational runbook work before any real send phase.

## 21. 다음 Backlog 후보
- P3-PRIVATE-BETA-RUNBOOK
- P3-ALERT-MVP-LANDING-PAGE-COPY-IMPLEMENTATION
- P3-PERSISTENT-ALERT-STORAGE-DB-ADAPTER-CONTRACT
- P3-UNSUBSCRIBE-MANAGE-ENDPOINT-IMPLEMENTATION
- P3-EMAIL-PROVIDER-SEND-ENABLEMENT-IMPLEMENTATION
