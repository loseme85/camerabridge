# P3-UNSUBSCRIBE-MANAGE-ENDPOINT-IMPLEMENTATION

## 1. 작업명
P3-UNSUBSCRIBE-MANAGE-ENDPOINT-IMPLEMENTATION

## 2. 작업 목적
unsubscribe/manage token contract를 실제 HTTP 없이 local endpoint preview 코드로 옮기고, token validation부터 preference/storage/delivery effect까지 안전하게 이어지는 preview 경계를 고정한다.

## 3. 구현 요약
- token_hash 기반 request preview를 처리하는 provider-neutral local endpoint preview를 구현했다.
- raw token/email/url/provider payload를 차단하고, valid/expired/invalid/replay/scope mismatch/suppressed/privacy delete pending 경로를 분기했다.
- preference/subscription/unsubscribe/suppression/delivery effect를 local repository preview에 저장하고 provider webhook preview도 suppression/unsubscribe effect로 연결했다.

## 4. endpoint implementation scope
- 포함: local request validation, token store preview, manage/unsubscribe action mapping, storage effect preview, delivery queue effect preview, provider webhook preview mapping.
- 제외: actual HTTP endpoint, frontend/manage page, auth/session, DB connection, provider send, webhook runtime.

## 5. unsubscribe_manage_endpoint.py public API
- create_unsubscribe_manage_endpoint_policy
- create_token_store_preview
- validate_endpoint_request
- enforce_endpoint_privacy_policy
- validate_token_hash
- mark_token_used
- map_manage_action_to_preference_update
- apply_manage_action_preview
- apply_unsubscribe_action_preview
- apply_provider_webhook_unsubscribe_preview
- create_endpoint_response_preview
- process_endpoint_request_preview
- process_unsubscribe_manage_scenarios
- export_unsubscribe_manage_endpoint_preview

## 6. endpoint policy
- endpoint_mode = local_preview
- actual_http_endpoint_enabled = False
- frontend_page_enabled = False
- auth_session_enabled = False
- db_connection_enabled = False
- provider_send_enabled = False
- webhook_endpoint_enabled = False

## 7. token store / token validation 결과
- token store count = 14
- used token count = 3
- token validation status counts = {'accepted_preview': 12, 'rejected_expired_token': 1, 'rejected_invalid_token': 2, 'rejected_scope_mismatch': 1, 'noop_no_change': 1, 'rejected_suppressed': 1, 'rejected_privacy_delete_pending': 1, 'blocked_policy_violation': 1}

## 8. request validation / privacy enforcement 결과
- raw_token_present/raw_email_present/raw_url_present/provider_payload_present 모두 false expectation으로 고정했다.
- raw-like key가 들어오면 blocked_policy_violation으로 차단한다.
- missing token_hash는 request validation이 아니라 token validation에서 rejected_invalid_token으로 처리한다.

## 9. manage action 결과
- pause_subscription: queued jobs require pre-dispatch check
- resume_subscription: future jobs allowed
- convert_immediate_to_digest: digest_jobs_only
- update_price_condition: max_price update preview persisted
- opt_out_price_drop / opt_out_source_gap: future jobs blocked preview
- view_preferences: safe summary only, no raw identity leak

## 10. unsubscribe action 결과
- single_subscription: subscription unsubscribed, matching queued job cancelled, unsubscribe_event created, token marked used
- all_alerts: global_unsubscribe_active true, active subscriptions unsubscribed, queued jobs cancelled
- provider_complaint: suppression_event created, future jobs blocked
- provider_unsubscribe: unsubscribe effect mapped by scope

## 11. provider webhook mapping 결과
- complaint -> suppression_event
- bounce -> suppression_event
- unsubscribe -> unsubscribe_event path
- duplicate provider webhook -> noop_duplicate

## 12. persistent storage 연동 결과
- domain counts = {'source_state': 0, 'crawl_snapshot': 0, 'listing_observation': 0, 'scheduler_decision': 0, 'crawl_job': 0, 'live_adapter_handoff': 0, 'watch_target': 0, 'alert_subscription': 12, 'preference_profile': 10, 'preference_update_event': 6, 'delivery_queue_job': 5, 'rendered_email_template': 0, 'provider_request_event': 0, 'provider_result_event': 0, 'webhook_event': 2, 'unsubscribe_event': 3, 'suppression_event': 1, 'audit_log_event': 10}
- transition_log_count = 0
- privacy_event_log_count = 0

## 13. delivery queue effect 결과
- queued_jobs_should_be_cancelled
- queued_jobs_require_pre_dispatch_check
- digest_jobs_only
- global_unsubscribe_block
- suppression_block

## 14. endpoint response preview 결과
- accepted/unsubscribed/paused/resumed/digest/expired/not verified 메시지를 safe preview 형태로 생성한다.
- invalid token과 missing token은 같은 user-visible message를 반환한다.
- Korean safe message summary examples:
  - 이 알림 수신이 해지되었습니다.
  - 전체 알림 수신이 해지되었습니다.
  - 이 알림이 일시정지되었습니다.
  - 설정이 업데이트되었습니다.
  - 링크가 만료되었습니다.
  - 요청을 확인할 수 없습니다.

## 15. security / no enumeration 결과
- invalid token과 missing token은 동일한 safe message를 반환한다.
- response에는 raw email/token/url/provider payload를 노출하지 않는다.
- suppressed/privacy delete 상태도 내부 세부를 과도하게 노출하지 않는다.

## 16. scenario validation 결과
- pass = 20/20
- single_alert_unsubscribe: passed (accepted_preview)
- global_unsubscribe: passed (accepted_preview)
- pause_subscription_manage: passed (accepted_preview)
- resume_subscription_manage: passed (accepted_preview)
- convert_digest: passed (accepted_preview)
- update_price_condition: passed (accepted_preview)
- opt_out_price_drop: passed (accepted_preview)
- opt_out_source_gap: passed (accepted_preview)
- expired_token: passed (rejected_expired_token)
- invalid_tampered_token: passed (rejected_invalid_token)
- scope_mismatch: passed (rejected_scope_mismatch)
- replayed_unsubscribe_token: passed (noop_no_change)
- suppressed_profile: passed (rejected_suppressed)
- privacy_delete_pending: passed (rejected_privacy_delete_pending)
- raw_policy_violation: passed (blocked_policy_violation)
- provider_complaint_webhook: passed (accepted_preview)
- provider_unsubscribe_webhook: passed (accepted_preview)
- manage_view_preferences: passed (accepted_preview)
- provider_duplicate_webhook: passed (accepted_preview)
- security_no_enumeration: passed (rejected_invalid_token)

## 17. raw token/email/url/provider payload guard
- raw_token_present = False
- raw_email_present = False
- raw_url_present = False
- provider_payload_present = False

## 18. actual HTTP/frontend/auth/DB 미구현 guard
- actual HTTP endpoint 구현 없음
- frontend/manage page 구현 없음
- auth/session 구현 없음
- DB connection/migration/runtime 구현 없음
- provider send/webhook runtime 구현 없음

## 19. output JSON / production code 미수정 여부
- 이번 라운드는 local endpoint preview implementation과 artifact 생성만 포함한다.
- production crawler/search/parser/resolver/classifier/frontend/auth/provider runtime은 수정하지 않는다.

## 20. 테스트 결과
- scenario validation rows generated
- JSONL/JSON artifact export ready

## 21. 남은 위험
- actual HTTP boundary, auth/session, token issuance runtime, DB persistence, webhook signature verification은 아직 구현 대상이 아니다.
- provider send enablement 및 actual unsubscribe endpoint runtime과 결합되기 전까지는 preview-only 상태다.

## 22. 다음 backlog 후보
- P3-EMAIL-PROVIDER-SEND-ENABLEMENT-IMPLEMENTATION
- P3-PRIVATE-BETA-ADMIN-QUEUE-CONTRACT
- P3-ALERT-MVP-LANDING-PAGE-FRONTEND-CONTRACT
- P3-PERSISTENT-ALERT-STORAGE-DB-ADAPTER-IMPLEMENTATION
- P3-UNSUBSCRIBE-MANAGE-ENDPOINT-FRONTEND-CONTRACT
