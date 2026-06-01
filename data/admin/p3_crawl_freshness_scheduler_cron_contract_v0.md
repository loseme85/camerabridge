# P3-CRAWL-FRESHNESS-SCHEDULER-CRON-CONTRACT

## 1. 작업명
P3-CRAWL-FRESHNESS-SCHEDULER-CRON-CONTRACT

## 2. 작업 목적
scheduler decision을 cron/orchestrator가 읽는 due decision, execution plan, crawl job preview, live adapter handoff preview로 변환하는 contract를 정의한다.

## 3. 구현 요약
- scheduler decision input / cron tick / due decision / execution plan / crawl job / live adapter handoff schema를 정의했다.
- budget, cooldown, retry/backoff, concurrency, preview-only safety 규칙을 분리했다.
- rare/source-gap 우선, broad/manual/anti-bot/adapter-not-ready skip 경로를 scenario로 고정했다.

## 4. Cron/Orchestrator Contract Scope
- contract only
- no actual cron config change
- no live crawl execution
- no production crawler integration

## 5. Scheduler Decision Input Schema
- scheduler_decision_id, source_id, watch_target_id, interval_band, crawl_intent, priority_score, next_due_at, downstream_expected_consumer 등을 포함한다.

## 6. Cron Tick / Due Decision Schema
- cron tick은 due 판단과 plan 생성만 수행한다.
- due status는 due_now / not_due_yet / paused / cooldown / budget / concurrency / source_health / anti_bot / adapter_not_ready / broad_query / manual_review skip을 포함한다.

## 7. Interval Band Policy
- very_fast=10, fast=45, normal=240, slow=960, paused=null
- degraded health는 very_fast를 fast로 낮출 수 있다.
- anti-bot high/blocked는 paused/skip이다.

## 8. Execution Plan / Crawl Job Preview Schema
- selected jobs: 5
- skipped jobs: 9
- crawl job preview는 source_url_fingerprint만 유지하고 raw URL은 유지하지 않는다.

## 9. Budget / Priority Policy
- rare/source-gap 먼저, common/digest는 budget pressure에서 먼저 skip한다.

## 10. Cooldown / Retry / Backoff Policy
- source cooldown, watch-target cooldown, failed fetch cooldown, anti-bot cooldown을 분리했다.
- first failure 30m, repeated failure 120m, anti-bot 24h backoff preview를 정의했다.

## 11. Concurrency / Dedupe Policy
- same source + watch target + interval window duplicate 금지
- same source max concurrent jobs 제한
- deterministic dedupe_key / idempotency_key 사용

## 12. Live Adapter Handoff Schema
- selected crawl job only handoff 생성
- adapter readiness and fetch_mode가 handoff에 같이 전달된다.

## 13. Scenario Validation 결과
- 35lux_map_due: due=due_now | job=selected_for_preview_execution | status=pass
- nocti_fujiya_due: due=due_now | job=selected_for_preview_execution | status=pass
- m6_leica_store_due: due=due_now | job=selected_for_preview_execution | status=pass
- sigma1424_map_source_gap: due=due_now | job=selected_for_preview_execution | status=pass
- sigma1424_keh_selector_audit: due=skipped_adapter_not_ready | job=skipped | status=pass
- lumix_mpb_digest: due=due_now | job=skipped | status=pass
- sl2490_digest: due=due_now | job=skipped | status=pass
- broad_summicron: due=skipped_broad_query | job=skipped | status=pass
- manual_review_m10r: due=skipped_manual_review_only | job=skipped | status=pass
- mercari_nocti_anti_bot: due=skipped_anti_bot | job=skipped | status=pass
- degraded_source_nocti: due=due_now | job=selected_for_preview_execution | status=pass
- cooldown_lumix: due=skipped_cooldown | job=skipped | status=pass
- concurrency_35lux_duplicate: due=skipped_concurrency | job=skipped | status=pass
- paused_watch: due=skipped_paused | job=skipped | status=pass

## 14. Preview-Only / No Actual Crawl Guard
- preview_only=true, dry_run=true를 유지한다.
- execution plan은 생성되지만 actual crawl은 수행하지 않는다.

## 15. Raw URL / HTML / Privacy Guard
- raw_url_present=false
- raw_html_storage_allowed=false
- raw_image_url_storage_allowed=false

## 16. Output JSON / Production Code 미수정 여부
- contract artifact only; no cron, GitHub Actions, crawler, frontend, auth, provider code was modified.

## 17. 테스트 결과
- schema, due decision, budget selection, anti-bot, adapter readiness, broad/manual, cooldown, concurrency, preview-only guard를 검증했다.

## 18. 남은 위험
- 실제 cron orchestration, persistence, in-flight state, retry history, and live adapter integration remain outside this contract round.

## 19. 다음 Backlog 후보
- P3-PERSISTENT-ALERT-STORAGE-IMPLEMENTATION-CONTRACT
- P3-SOURCE-CHANGE-DETECTION-LIVE-ADAPTER-IMPLEMENTATION
- P3-CRAWL-FRESHNESS-SCHEDULER-CRON-IMPLEMENTATION
- P3-ALERT-MVP-LANDING-PAGE-COPY-IMPLEMENTATION
- P3-PRIVATE-BETA-RUNBOOK
