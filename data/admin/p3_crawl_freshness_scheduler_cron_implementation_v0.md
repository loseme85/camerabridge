# P3-CRAWL-FRESHNESS-SCHEDULER-CRON-IMPLEMENTATION

## 1. 작업명
P3-CRAWL-FRESHNESS-SCHEDULER-CRON-IMPLEMENTATION

## 2. 작업 목적
crawl_freshness_scheduler_cron_contract.py의 scheduler decision -> cron tick -> due decision -> execution plan -> crawl job -> live adapter handoff 규칙을 provider-neutral local orchestrator preview 코드로 옮긴다.

## 3. 구현 요약
- scheduler decision validation, due 판단, budget/priority/cooldown/concurrency/adapter readiness skip, selected/skipped job preview, live adapter handoff, local storage persistence, local adapter run, source_change_detection 연결을 구현했다.
- 모든 흐름은 preview_only/dry_run으로 고정했고 actual cron/live crawl/DB/provider send는 수행하지 않는다.

## 4. Cron Implementation Scope
- provider-neutral local orchestrator preview
- no actual cron/GitHub Actions config change
- no actual live crawl
- no DB connection or production persistence runtime

## 5. crawl_freshness_scheduler_cron.py Public API
- `create_cron_orchestrator_policy`
- `validate_scheduler_decision_input`
- `create_cron_tick_preview`
- `compute_due_decision`
- `apply_interval_band_policy`
- `apply_budget_priority_policy`
- `apply_cooldown_policy`
- `apply_concurrency_policy`
- `apply_adapter_readiness_policy`
- `create_crawl_job_preview`
- `create_skipped_job_preview`
- `create_live_adapter_handoff_preview`
- `build_crawl_execution_plan`
- `persist_cron_execution_plan`
- `run_selected_job_local_preview`
- `process_cron_tick_batch`
- `process_cron_scenarios`

## 6. Scheduler Decision Validation 결과
- scheduler_decision_input rows = `16`
- preview_only=true, supported interval band/crawl intent, required fields, and broad/manual/anti-bot guards are checked.

## 7. Cron Tick / Due Decision 결과
- cron_tick_preview rows = `12`
- due_decision rows = `16`
- due_now, skipped_budget, skipped_cooldown, skipped_concurrency, skipped_adapter_not_ready, skipped_anti_bot, skipped_broad_query, skipped_manual_review_only, skipped_paused are covered.

## 8. Interval / Budget / Priority 결과
- selected jobs = `7`
- skipped jobs = `9`
- source-gap and rare jobs are chosen before common digest jobs under shared budget.

## 9. Cooldown / Concurrency 결과
- cooldown rows = `16`
- concurrency rows = `16`
- seeded source cooldown and duplicate in-flight crawl job both force safe skips.

## 10. Adapter Readiness / Anti-Bot / Broad-Manual Skip 결과
- needs_selector_audit sources are skipped_adapter_not_ready.
- blocked_by_anti_bot sources are skipped_anti_bot.
- broad refinement and manual review targets never create live adapter handoffs.

## 11. Execution Plan / Crawl Job Preview 결과
- execution_plan rows = `12`
- selected jobs remain preview-only and dry-run only.

## 12. Live Adapter Handoff 결과
- handoff rows = `7`
- only selected jobs create handoffs, and all handoffs stay raw-URL safe.

## 13. Persistent Storage 연동 결과
- scheduler_decision, crawl_job, live_adapter_handoff rows are persisted into the local repository preview.
- aggregated domain counts = `{'source_state': 7, 'crawl_snapshot': 6, 'listing_observation': 6, 'scheduler_decision': 16, 'crawl_job': 16, 'live_adapter_handoff': 7, 'watch_target': 0, 'alert_subscription': 0, 'preference_profile': 0, 'preference_update_event': 0, 'delivery_queue_job': 0, 'rendered_email_template': 0, 'provider_request_event': 0, 'provider_result_event': 0, 'webhook_event': 0, 'unsubscribe_event': 0, 'suppression_event': 0, 'audit_log_event': 0}`

## 14. source_change_detection_live_adapter.py 연동 결과
- local adapter run rows = `7`
- selected jobs call the local adapter preview with raw fixture inputs only.

## 15. source_change_detection.py 연동 결과
- source_change_detection_run_result rows = `7`
- adapted snapshot/listing output continues into source_change_detection preview only.

## 16. Scenario Validation 결과
- scenario_validation rows = `16`
- failed scenarios = `[]`

## 17. Preview-Only / No Actual Crawl Guard
- preview_only = `True`
- dry_run = `True`
- actual_cron_enabled = `False`
- actual_live_crawl_enabled = `False`

## 18. Raw URL/HTML/Privacy Guard
- raw_email_present = `False`
- raw_url_present = `False`
- raw_html_present = `False`
- provider_payload_present = `False`

## 19. Output JSON / Production Code 미수정 여부
- 이번 라운드는 local orchestrator preview + artifact 생성만 포함한다.
- actual cron/config, crawler, DB, provider, frontend, auth, search/parser/resolver/classifier production 코드는 수정하지 않는다.

## 20. 테스트 결과
- implementation tests, runner, JSONL validation, and golden_set expected to pass

## 21. 남은 위험
- cron/runtime concurrency locking은 아직 preview store 수준이다.
- source-specific live fetch retry/backoff orchestration은 future runtime implementation에서 더 세밀해져야 한다.

## 22. 다음 Backlog 후보
- P3-UNSUBSCRIBE-MANAGE-ENDPOINT-CONTRACT
- P3-EMAIL-PROVIDER-SEND-ENABLEMENT-CONTRACT
- P3-PRIVATE-BETA-RUNBOOK
- P3-ALERT-MVP-LANDING-PAGE-COPY-IMPLEMENTATION
- P3-PERSISTENT-ALERT-STORAGE-DB-ADAPTER-CONTRACT
