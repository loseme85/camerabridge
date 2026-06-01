# P3-PERSISTENT-ALERT-STORAGE-IMPLEMENTATION-CONTRACT

## 1. 작업명
P3-PERSISTENT-ALERT-STORAGE-IMPLEMENTATION-CONTRACT

## 2. 작업 목적
Alert MVP가 반복 실행과 preview/private beta로 넘어가기 위해 어떤 상태를 어떤 privacy boundary로 저장해야 하는지 정의한다.

## 3. 구현 요약
- persistent storage domain matrix를 만들고 entity schema/field/index/lifecycle/privacy/idempotency/transition rule을 정의했다.
- raw email/url/html/provider payload/webhook body 저장 금지 정책을 모든 domain에 공통으로 고정했다.
- storage 부재가 어떤 beta blocker로 이어지는지도 domain 단위로 연결했다.

## 4. Persistent Storage Contract Scope
- contract only
- no actual DB migration
- no ORM/model implementation
- no persistence runtime implementation

## 5. Storage Domain Matrix
- source_state: owner=crawl_freshness_scheduler.py + source_change_detection.py | preview_beta=True | real_email_beta=True
- crawl_snapshot: owner=source_change_detection.py | preview_beta=True | real_email_beta=True
- listing_observation: owner=source_change_detection.py + fast_alert_path.py | preview_beta=True | real_email_beta=True
- scheduler_decision: owner=crawl_freshness_scheduler.py | preview_beta=True | real_email_beta=True
- crawl_job: owner=crawl_freshness_scheduler_cron_contract.py | preview_beta=True | real_email_beta=True
- live_adapter_handoff: owner=source_change_detection_live_adapter_contract.py | preview_beta=True | real_email_beta=True
- watch_target: owner=alert_watchlist_contract.py | preview_beta=True | real_email_beta=True
- alert_subscription: owner=alert_preference_center.py | preview_beta=True | real_email_beta=True
- preference_profile: owner=alert_preference_center.py | preview_beta=True | real_email_beta=True
- preference_update_event: owner=alert_preference_center.py | preview_beta=True | real_email_beta=True
- delivery_queue.py: owner=delivery_queue.py | preview_beta=True | real_email_beta=True
- email_template.py: owner=email_template.py | preview_beta=True | real_email_beta=True
- email_provider_adapter.py: owner=email_provider_adapter.py | preview_beta=True | real_email_beta=True
- email_provider_adapter.py: owner=email_provider_adapter.py | preview_beta=True | real_email_beta=True
- webhook_event: owner=email_provider_adapter.py | preview_beta=False | real_email_beta=True
- alert_unsubscribe_contract.py: owner=alert_unsubscribe_contract.py | preview_beta=True | real_email_beta=True
- suppression_event: owner=delivery_queue.py + email_provider_adapter.py | preview_beta=True | real_email_beta=True
- audit_log_event: owner=beta_ops | preview_beta=True | real_email_beta=True

## 6. Common Field / Privacy Policy
- common fields include id, domain_pack_id, created_at, updated_at, record_status, schema_version, source_component, idempotency_key, dedupe_key.
- raw_email_present/raw_url_present/raw_html_present/provider_payload_present must stay false.

## 7. source_state / crawl_snapshot / listing_observation schema
- source_state stores health, anti-bot, cooldown, and snapshot pointers.
- crawl_snapshot stores page_hash and previous_snapshot_id without raw HTML.
- listing_observation stores first_seen/last_seen and fingerprint-safe listing history.

## 8. scheduler_decision / crawl_job schema
- scheduler_decision stores next_due_at and interval state.
- crawl_job stores scheduled_for, retry_count, next_retry_at, cooldown_applied, and live_adapter_handoff linkage.

## 9. watch_target / subscription / preference schema
- watch_target stores canonical query and blocking flags for broad/manual/source-gap exact-only.
- alert_subscription stores pending/active/paused/unsubscribed/suppressed/deleted lifecycle.
- preference_profile stores email_hash/email_encrypted_ref plus global_unsubscribe/suppression/privacy_delete state.

## 10. delivery_queue / email_template / provider event schema
- delivery_queue_job stores dedupe/retry/expiry state.
- rendered_email_template stores safe preview refs only.
- provider_request/result event stores traceability without raw provider payload.

## 11. webhook / unsubscribe / suppression schema
- webhook_event stores deduped provider event metadata only.
- unsubscribe_event stores scope and queued-job cancellation effect.
- suppression_event stores bounce/complaint/unsubscribe enforcement state.

## 12. Retention / Deletion Policy
- source_state: retention=active + 180d history | delete=upsert latest state, archive old versions
- crawl_snapshot: retention=30-90d by source tier | delete=expire old snapshots after retention
- listing_observation: retention=365d | delete=retain for price guide and dedupe
- scheduler_decision: retention=30d | delete=expire old decisions
- crawl_job: retention=90-180d | delete=retain retry/audit history
- live_adapter_handoff: retention=30-90d | delete=expire after crawl lineage closes

## 13. Idempotency / Dedupe Policy
- crawl_job: source + watch_target + interval window
- listing_observation: source identity + fingerprint-safe fields
- delivery_queue_job: subscription + listing_fingerprint + delivery_event_type
- provider_request_event: delivery_job_id + provider_type + template_ref
- webhook_event: provider event fingerprint + delivery_job_id

## 14. State Transition Rules
- crawl_job: queued -> running -> succeeded/failed/skipped/cancelled/expired
- subscription: pending -> active -> paused/unsubscribed/deleted/suppressed
- delivery_queue_job: queued -> ready -> dispatched_preview -> accepted/delivered/failed/suppressed/cancelled

## 15. Beta Blocker Mapping
- crawl_snapshot: phase=private_beta_preview_only | severity=high | component=source_change_detection.py
- listing_observation: phase=private_beta_preview_only | severity=high | component=source_change_detection.py + fast_alert_path.py
- listing_observation: phase=private_beta_preview_only | severity=high | component=source_change_detection.py + delivery_queue.py
- alert_subscription: phase=private_beta_preview_only | severity=blocker | component=alert_preference_center.py
- preference_profile: phase=private_beta_preview_only | severity=blocker | component=alert_preference_center.py + delivery_queue.py
- delivery_queue_job: phase=private_beta_with_real_email | severity=blocker | component=delivery_queue.py
- delivery_queue_job: phase=private_beta_with_real_email | severity=high | component=delivery_queue.py + email_provider_adapter.py
- webhook_event: phase=private_beta_with_real_email | severity=high | component=email_provider_adapter.py
- unsubscribe_event: phase=private_beta_with_real_email | severity=blocker | component=alert_unsubscribe_contract.py + delivery_queue.py
- suppression_event: phase=private_beta_with_real_email | severity=blocker | component=delivery_queue.py + email_provider_adapter.py
- preference_profile: phase=public_beta | severity=high | component=beta_ops
- audit_log_event: phase=public_beta | severity=high | component=beta_ops

## 16. Scenario Validation 결과
- source_snapshot_pair_persistence: status=pass | notes=previous/current snapshot linkage exists for cross-tick diffing
- listing_first_seen_last_seen: status=pass | notes=listing observation keeps first_seen and last_seen
- duplicate_listing_observation: status=pass | notes=listing observation idempotency/dedupe basis defined
- crawl_job_idempotency: status=pass | notes=crawl job duplicate prevention across same interval window defined
- source_cooldown_persistence: status=pass | notes=source_state stores anti-bot and source cooldown
- subscription_active_pause_unsubscribe_persistence: status=pass | notes=subscription lifecycle state persists
- global_unsubscribe: status=pass | notes=global unsubscribe and queue cancellation state persist
- unverified_subscription: status=pass | notes=pending verification state can persist
- delivery_queue_retry: status=pass | notes=delivery queue retry state persists
- provider_bounce_complaint: status=pass | notes=bounce/complaint can create suppression_event and block future jobs
- webhook_dedupe: status=pass | notes=webhook dedupe key/idempotency policy defined
- privacy_delete: status=pass | notes=privacy delete state and encrypted ref removal boundary defined
- raw_policy_guard: status=pass | notes=all privacy policies disallow raw email/url/html/provider payload storage
- public_beta_blocker: status=pass | notes=beta blocker mapping includes storage-driven public/private beta blockers

## 17. Raw Email/URL/HTML/Provider Payload Guard
- raw email 저장 금지
- raw source/listing/image URL 저장 금지
- raw HTML 저장 금지
- raw provider payload / raw webhook body 저장 금지

## 18. Output JSON / Production Code 미수정 여부
- contract artifact only; no DB, auth, crawler, webhook, provider, frontend runtime code modified.

## 19. 테스트 결과
- domain/schema/privacy/idempotency/transition/blocker/scenario checks included.

## 20. 남은 위험
- Postgres/Supabase/SQLite 실제 구현 선택, migration strategy, retention enforcement, privacy delete executor는 다음 라운드 과제다.

## 21. 다음 Backlog 후보
- P3-SOURCE-CHANGE-DETECTION-LIVE-ADAPTER-IMPLEMENTATION
- P3-CRAWL-FRESHNESS-SCHEDULER-CRON-IMPLEMENTATION
- P3-PERSISTENT-ALERT-STORAGE-IMPLEMENTATION
- P3-UNSUBSCRIBE-MANAGE-ENDPOINT-CONTRACT
- P3-PRIVATE-BETA-RUNBOOK
