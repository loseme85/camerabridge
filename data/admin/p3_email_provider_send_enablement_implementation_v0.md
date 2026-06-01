# P3-EMAIL-PROVIDER-SEND-ENABLEMENT-IMPLEMENTATION

## 1. 작업명
P3-EMAIL-PROVIDER-SEND-ENABLEMENT-IMPLEMENTATION

## 2. 작업 목적
email provider send enablement contract의 phase/gate/pre-dispatch/provider boundary 규칙을 local safety gate implementation으로 옮긴다.

## 3. 구현 요약
- delivery_queue_job, rendered template, preference/subscription 상태를 받아 send enablement decision을 생성하는 local preview 코드를 구현했다.
- verified/suppressed/global unsubscribe/privacy delete/template/idempotency/rate-limit/provider readiness를 gate로 평가한다.
- provider_send_enabled_allowed, provider_payload_allowed, actual_provider_call_allowed는 이번 라운드에서 모두 false로 유지한다.

## 4. send enablement implementation scope
- 포함: policy, phase matrix, input validation, privacy enforcement, gate evaluation, provider readiness, request boundary, decision persistence preview.
- 제외: actual provider SDK/API call, payload generation, webhook endpoint, DB runtime, frontend/auth.

## 5. email_provider_send_enablement.py public API
- create_send_enablement_policy
- build_send_phase_matrix
- evaluate_send_phase
- validate_send_enablement_input
- enforce_send_privacy_policy
- run_pre_dispatch_safety_check
- evaluate_verified_email_gate
- evaluate_subscription_gate
- evaluate_unsubscribe_manage_gate
- evaluate_suppression_gate
- evaluate_template_safety_gate
- evaluate_provider_readiness_gate
- evaluate_idempotency_gate
- evaluate_rate_limit_gate
- create_provider_send_request_boundary
- create_send_enablement_decision
- persist_send_enablement_preview
- process_send_enablement_batch
- process_send_enablement_scenarios
- export_send_enablement_preview

## 6. send enablement policy
- implementation_mode = local_preview
- provider_send_enabled_default = False
- actual_send_allowed = False
- provider_sdk_call_allowed = False
- provider_payload_generation_allowed = False
- webhook_endpoint_enabled = False

## 7. phase matrix 결과
- preview_only: allowed_preview
- provider_payload_preview: blocked_missing_payload_boundary_implementation
- sandbox_send_preview: blocked_provider_not_ready
- internal_real_send_limited: blocked_provider_not_ready
- private_beta_real_send: blocked_missing_runtime_dependencies
- public_beta_send: blocked
- production_send: blocked

## 8. input/context validation 결과
- delivery_job/context/requested_phase required field를 검증한다.
- raw email/payload/webhook body 또는 raw-like key가 있으면 blocked_policy_violation.

## 9. privacy enforcement 결과
- raw_email_present=true 차단
- provider_payload_present=true 차단
- raw_webhook_body_present=true 차단
- safe refs만 boundary에 남긴다.

## 10. pre-dispatch safety check 결과
- allowed_preview
- blocked_unverified
- blocked_paused
- blocked_global_unsubscribe
- blocked_suppressed
- blocked_privacy_delete
- blocked_missing_unsubscribe_endpoint
- blocked_template_unsafe
- blocked_template_not_rendered
- blocked_duplicate_send
- blocked_rate_limited
- blocked_provider_not_ready

## 11. gate evaluation 결과
- verified/subscription/unsubscribe-manage/suppression/template/provider/idempotency/rate-limit/privacy/monitoring/domain/webhook gate를 개별 평가한다.

## 12. provider readiness 결과
- provider_neutral = ready_for_preview_only
- resend/sendgrid/aws_ses = blocked_provider_not_ready until credentials/domain/webhook/signature readiness

## 13. provider send request boundary 결과
- recipient_ref / recipient_email_hash / template_ref / body_template_ref / placeholder ref만 포함한다.
- raw email/provider payload/provider_message_id raw value는 포함하지 않는다.

## 14. idempotency / duplicate send 결과
- key basis = delivery_job_id + provider_type + template_ref
- duplicate send -> blocked_duplicate_send

## 15. rate limit / quota 결과
- provider_neutral은 preview decision count 중심
- exceeded/limited는 blocked_rate_limited 또는 delayed_retry_preview reason으로 차단

## 16. storage/delivery compatibility 결과
- allowed_preview_count = 3
- blocked_count = 20
- storage domain counts = {'source_state': 0, 'crawl_snapshot': 0, 'listing_observation': 0, 'scheduler_decision': 0, 'crawl_job': 0, 'live_adapter_handoff': 0, 'watch_target': 0, 'alert_subscription': 7, 'preference_profile': 6, 'preference_update_event': 0, 'delivery_queue_job': 7, 'rendered_email_template': 7, 'provider_request_event': 1, 'provider_result_event': 0, 'webhook_event': 0, 'unsubscribe_event': 0, 'suppression_event': 0, 'audit_log_event': 3}

## 17. send enablement decision 결과
- real send phases에서도 provider_send_enabled_allowed=false 유지
- actual_provider_call_allowed=false 유지
- next_required_action에 credential/domain/webhook/runtime blockers를 구체적으로 남긴다.

## 18. scenario validation 결과
- pass = 21/21
- preview_only_provider_neutral: passed (allowed_preview)
- unsubscribe_endpoint_missing: passed (blocked_missing_unsubscribe_endpoint)
- unverified_email: passed (blocked_unverified)
- paused_subscription: passed (blocked_paused)
- global_unsubscribe: passed (blocked_global_unsubscribe)
- suppressed_profile: passed (blocked_suppressed)
- privacy_delete_requested: passed (blocked_privacy_delete)
- template_unsafe_claim: passed (blocked_template_unsafe)
- template_not_rendered: passed (blocked_template_not_rendered)
- duplicate_delivery_job_send: passed (blocked_duplicate_send)
- rate_limit_hit: passed (blocked_rate_limited)
- provider_credentials_missing_resend: passed (blocked_provider_not_ready)
- provider_credentials_missing_sendgrid: passed (blocked_provider_not_ready)
- provider_credentials_missing_aws_ses: passed (blocked_provider_not_ready)
- webhook_not_ready: passed (blocked_provider_not_ready)
- internal_real_send_limited_requested: passed (blocked_provider_not_ready)
- private_beta_real_send_readiness: passed (blocked_provider_not_ready)
- raw_policy_violation: passed (blocked_policy_violation)
- provider_request_boundary_privacy: passed (allowed_preview)
- suppression_from_prior_unsubscribe_manage: passed (blocked_suppressed)
- batch_mixed_decisions: passed (batch_blocked_real_send)

## 19. raw email/provider payload/webhook body guard
- raw_email_present = False
- provider_payload_present = False
- raw_webhook_body_present = False

## 20. actual provider send/webhook/DB 미구현 guard
- actual provider send 없음
- provider SDK/API call 없음
- provider payload generation 없음
- webhook endpoint/runtime 없음
- DB connection/migration/runtime 없음

## 21. output JSON / production code 미수정 여부
- local preview implementation과 artifact만 생성했다.
- production crawler/search/parser/resolver/classifier/frontend/auth/provider runtime은 수정하지 않는다.

## 22. 테스트 결과
- scenario validation rows generated
- JSONL/JSON artifact export ready

## 23. 남은 위험
- actual send runtime, webhook signature runtime, DB adapter/runtime, unsubscribe endpoint runtime과 붙기 전까지는 preview-only이다.

## 24. 다음 backlog 후보
- P3-PRIVATE-BETA-ADMIN-QUEUE-CONTRACT
- P3-ALERT-MVP-LANDING-PAGE-FRONTEND-CONTRACT
- P3-PERSISTENT-ALERT-STORAGE-DB-ADAPTER-IMPLEMENTATION
- P3-UNSUBSCRIBE-MANAGE-ENDPOINT-FRONTEND-CONTRACT
- P3-EMAIL-PROVIDER-SEND-RUNTIME-CONTRACT
