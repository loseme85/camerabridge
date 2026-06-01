# P3-PERSISTENT-ALERT-STORAGE-IMPLEMENTATION

## 1. 작업명
P3-PERSISTENT-ALERT-STORAGE-IMPLEMENTATION

## 2. 작업 목적
persistent_alert_storage_contract.py의 schema/lifecycle/idempotency/privacy 규칙을 provider-neutral local repository preview 코드로 옮긴다.

## 3. 구현 요약
- 18개 storage domain을 가진 in-memory preview repository를 구현했다.
- raw email/url/html/provider payload/webhook body 저장 금지와 strict validation을 공통 경계로 고정했다.
- snapshot/listing/subscription/delivery/provider/webhook/suppression/privacy delete 흐름을 deterministic scenario batch로 검증했다.

## 4. Persistent Storage Implementation Scope
- provider-neutral local repository preview
- no DB migration
- no DB connection
- no ORM production runtime

## 5. Storage Repository API
- `create_empty_storage`
- `validate_storage_record`
- `enforce_storage_privacy_policy`
- `compute_storage_id`
- `compute_idempotency_key`
- `compute_dedupe_key`
- `upsert_record`
- `get_record`
- `list_records`
- `transition_record_status`
- `create_source_snapshot_pair`
- `upsert_listing_observation`
- `enqueue_crawl_job`
- `apply_preference_update_event`
- `enqueue_delivery_job`
- `apply_provider_result_event`
- `apply_webhook_event`
- `apply_global_unsubscribe`
- `apply_privacy_delete_preview`
- `export_storage_preview`
- `process_storage_scenario_batch`

## 6. Storage Policy / In-Memory Store Shape
- storage_mode = `in_memory_preview`
- domain_count = `18`
- production_persistence_enabled = `False`
- db_migration_enabled = `False`

## 7. Privacy Enforcement 결과
- policy_violation_count = `1`
- raw-like keys or raw flags set to true are blocked before persistence.

## 8. Domain Validation 결과
- persisted_record_rows = `28`
- scenario_validation_rows = `14`

## 9. Idempotency / Dedupe 결과
- crawl job duplicate returns existing record by idempotency key.
- listing observation reuses the same observation record across snapshots.
- webhook duplicate is ignored through idempotency/dedupe indexes.

## 10. Snapshot Persistence 결과
- previous_snapshot_id/current_snapshot_id linkage stored.
- source_state current/previous pointers and last_page_hash update.

## 11. Listing Observation Persistence 결과
- first_seen_at stays stable.
- last_seen_at advances on repeated observations.
- sold/unavailable transitions remain representable.

## 12. Source State / Cooldown Persistence 결과
- failed fetch increments failure_count and sets source cooldown.
- anti-bot result sets anti_bot_cooldown_until.

## 13. Crawl Job Persistence 결과
- queued jobs persist with deterministic idempotency and dedupe keys.
- retry_count/next_retry_at fields stay compatible with later worker-backed implementation.

## 14. Subscription / Preference Persistence 결과
- pause/resume events update subscription_status and log transitions.
- global_unsubscribe_active and suppressed flags persist at profile level.

## 15. Delivery Queue Persistence 결과
- unverified immediate delivery stays blocked_pre_dispatch.
- failed_retryable increments retry_count and schedules next_retry_at.

## 16. Provider/Webhook/Suppression Persistence 결과
- provider bounce/complaint creates suppression_event.
- duplicate webhook does not double-apply delivery status updates.

## 17. Privacy Delete Preview 결과
- email_encrypted_ref is redacted.
- subscriptions are deleted and queued jobs cancelled.

## 18. Storage Export Summary
- beta_readiness_effect = `local_repository_preview`
- transition_log_count = `3`
- privacy_event_log_count = `2`

## 19. Raw Email/URL/HTML/Provider Payload Guard
- raw_email_present = `False`
- raw_url_present = `False`
- raw_html_present = `False`
- provider_payload_present = `False`

## 20. Output JSON / Production Code 미수정 여부
- 이번 라운드는 local repository preview + artifact 생성만 포함한다.
- production DB/runtime/auth/provider/webhook/crawler/frontend 코드는 수정하지 않는다.

## 21. 테스트 결과
- scenario batch and JSONL validation pass expected
- dedicated implementation tests cover persistence transitions and privacy guards

## 22. 남은 위험
- 아직 actual DB transaction/concurrency/locking은 없다.
- timestamp conflict resolution과 long-lived retention cleanup은 future DB implementation에서 다시 다뤄야 한다.

## 23. 다음 Backlog 후보
- P3-SOURCE-CHANGE-DETECTION-LIVE-ADAPTER-IMPLEMENTATION
- P3-CRAWL-FRESHNESS-SCHEDULER-CRON-IMPLEMENTATION
- P3-UNSUBSCRIBE-MANAGE-ENDPOINT-CONTRACT
- P3-EMAIL-PROVIDER-SEND-ENABLEMENT-CONTRACT
- P3-PRIVATE-BETA-RUNBOOK
