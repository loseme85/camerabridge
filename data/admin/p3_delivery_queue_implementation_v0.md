# P3-DELIVERY-QUEUE-IMPLEMENTATION

## 1. 작업 목적
- fast alert queue candidate를 delivery queue preview job으로 옮기고, dedupe / pre-dispatch / retry / expiry / cancellation / provider-dispatch preview를 순수 구현으로 고정한다.

## 2. 구현 요약
- `delivery_queue.py`에 queue candidate 검증, dedupe, job 생성, pre-dispatch guard, retry schedule, expiry, cancellation, provider dispatch preview를 구현했다.
- 실제 provider send / worker / DB queue는 만들지 않고 preview shape만 생성한다.

## 3. delivery_queue.py public API
- `build_delivery_dedupe_key`
- `create_delivery_job`
- `enqueue_delivery_candidates`
- `evaluate_pre_dispatch_guard`
- `compute_retry_schedule`
- `apply_delivery_attempt_result`
- `expire_delivery_jobs`
- `cancel_jobs_for_preference_update`
- `create_provider_dispatch_preview`
- `process_delivery_queue_batch`

## 4. fast alert queue candidate input compatibility
- fast alert implementation artifact queue candidate rows를 fixture로 재사용했다.
- 입력 호환 검증 대상 수: `17`

## 5. delivery job schema
- delivery jobs: `15`
- event counts: `{'rare_new_listing': 7, 'price_drop': 2, 'source_gap_resolved': 2, 'source_expansion_available': 2, 'conditional_rare_match': 1, 'smart_deal_match': 1}`

## 6. dedupe / idempotency 결과
- skipped duplicates: `1`
- duplicate scenario: `35 lux aa` repeated candidate -> `skipped_duplicate`

## 7. pre-dispatch guard 결과
- blocked guard counts: `{'blocked_unverified': 1, 'blocked_suppressed': 1, 'blocked_global_unsubscribe': 1, 'blocked_subscription_paused': 1, 'blocked_subscription_deleted': 1, 'blocked_trigger_disabled': 3}`
- allowed previews: `7`

## 8. retry policy 결과
- retryable failure -> `retry_scheduled`
- permanent failure -> `failed_permanent`

## 9. expiry / cancellation 결과
- expired jobs: `1`
- cancelled jobs after global unsubscribe preview: `1`

## 10. provider dispatch preview 결과
- provider previews: `7`
- provider send enabled: `false`
- provider message id stored: `false`

## 11. rare / price drop / source-gap / source-expansion / conditional rare / smart deal job 결과
- ready for dispatch preview: `7`

## 12. unverified / suppressed / global unsubscribe / paused / deleted / trigger disabled 결과
- blocked or suppressed jobs: `8`

## 13. raw URL/email/provider payload guard 결과
- policy violations: `1`
- all queue jobs raw-email/raw-url/provider-payload false 유지

## 14. provider adapter compatibility
- delivery jobs compatible count: `15/15`

## 15. output JSON / production code 수정 여부
- 허용된 implementation / test / artifact 파일만 수정했다.
- production crawler / search / parser / resolver / classifier / frontend / provider send path는 수정하지 않았다.

## 16. 테스트 결과
- scenario validations: `20/20`
- implementation checks: `5/5`
- jsonl validation: `True`

## 17. 남은 위험
- 실제 provider send, persistent queue storage, worker locking, concurrency dedupe는 아직 preview 범위 밖이다.

## 18. 다음 backlog 후보
- `P3-EMAIL-PROVIDER-ADAPTER-IMPLEMENTATION`
- `P3-ALERT-MVP-PREFERENCE-CENTER-IMPLEMENTATION`
- `P3-SOURCE-CHANGE-DETECTION-LIVE-ADAPTER-CONTRACT`
- `P3-CRAWL-FRESHNESS-SCHEDULER-CRON-CONTRACT`
- `P3-WATCH-BRIDGE-MARKET-SCOUT-CONTRACT`
