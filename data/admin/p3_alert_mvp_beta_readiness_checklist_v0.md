# P3-ALERT-MVP-BETA-READINESS-CHECKLIST

## 1. 작업명
P3-ALERT-MVP-BETA-READINESS-CHECKLIST

## 2. 작업 목적
현재까지 구현된 alert MVP 모듈과 contract artifact를 기준으로 internal dry-run 가능 범위, preview-only 범위, real beta blocker를 구분한다.

## 3. 구현 요약
- implementation artifact와 supporting contract artifact를 읽어 readiness matrix를 계산했다.
- module readiness, pipeline linkage, guardrail coverage, preview-only blockers, beta phase decision을 분리했다.
- readiness를 과장하지 않고 provider send/live crawl/persistence/auth/frontend gap을 blocker로 고정했다.

## 4. 현재 MVP 구현 상태 요약
- audited implementation modules: 7
- audited pipeline linkages: 6
- audited guardrails: 13
- preview-only blockers: 20

## 5. Module Readiness Matrix
- crawl_freshness_scheduler.py: ready_for_internal_dry_run | phase=internal_fixture_dry_run | scenarios=18 | preview_only=True | blockers=1
- source_change_detection.py: ready_for_internal_dry_run | phase=local_end_to_end_preview | scenarios=14 | preview_only=True | blockers=1
- fast_alert_path.py: ready_for_internal_dry_run | phase=local_end_to_end_preview | scenarios=22 | preview_only=True | blockers=1
- delivery_queue.py: ready_for_preview_beta | phase=private_beta_preview_only | scenarios=20 | preview_only=True | blockers=2
- email_template.py: ready_for_preview_beta | phase=private_beta_preview_only | scenarios=11 | preview_only=True | blockers=1
- email_provider_adapter.py: ready_for_preview_beta | phase=private_beta_preview_only | scenarios=21 | preview_only=True | blockers=2
- alert_preference_center.py: ready_for_preview_beta | phase=private_beta_preview_only | scenarios=19 | preview_only=True | blockers=1

## 6. Pipeline Linkage Matrix
- crawl_freshness_scheduler.py -> source_change_detection.py: compatible_preview_with_adapter_gap | missing_adapter=True | preview_only=True
- source_change_detection.py -> fast_alert_path.py: compatible_preview | missing_adapter=False | preview_only=True
- fast_alert_path.py -> delivery_queue.py: compatible_preview | missing_adapter=False | preview_only=True
- delivery_queue.py -> email_template.py: compatible_preview | missing_adapter=False | preview_only=True
- delivery_queue.py -> email_provider_adapter.py: compatible_preview | missing_adapter=False | preview_only=True
- alert_preference_center.py -> fast_alert_path.py + delivery_queue.py: compatible_preview | missing_adapter=False | preview_only=True

## 7. Guardrail Readiness Matrix
- no fake-fill: ready_for_internal_dry_run | covered_by=source_change_detection.py + fast_alert_path.py + email_template.py | evidence=source_gap_fake_fill_blocked
- no adjacent family substitution: ready_for_internal_dry_run | covered_by=source_change_detection.py | evidence=source_gap_fake_fill_blocked
- broad query refinement only: ready_for_internal_dry_run | covered_by=crawl_freshness_scheduler.py + fast_alert_path.py | evidence=broad_query_blocked
- manual-review target not fast-path: ready_for_internal_dry_run | covered_by=source_change_detection.py + fast_alert_path.py | evidence=manual_review_blocked
- source-gap exact only: ready_for_internal_dry_run | covered_by=source_change_detection.py + fast_alert_path.py | evidence=source_gap_exact
- duplicate blocked: ready_for_internal_dry_run | covered_by=source_change_detection.py + fast_alert_path.py + delivery_queue.py | evidence=duplicate_blocked
- sold/removed blocked: ready_for_internal_dry_run | covered_by=source_change_detection.py + fast_alert_path.py | evidence=sold_removed_blocked
- anti-bot/source-health guard: ready_for_internal_dry_run | covered_by=crawl_freshness_scheduler.py + source_change_detection.py + fast_alert_path.py | evidence=anti_bot_high_risk
- unverified subscription blocked: ready_for_internal_dry_run | covered_by=fast_alert_path.py + delivery_queue.py + alert_preference_center.py | evidence=pending_unverified_immediate_enable
- suppressed/global unsubscribe blocked: ready_for_internal_dry_run | covered_by=fast_alert_path.py + delivery_queue.py + alert_preference_center.py | evidence=global_unsubscribe
- high-risk source cannot bypass via preference: ready_for_internal_dry_run | covered_by=alert_preference_center.py | evidence=high_risk_source_immediate_request
- common watch digest-only unless smart condition: ready_for_internal_dry_run | covered_by=crawl_freshness_scheduler.py + fast_alert_path.py | evidence=common_watch_digest_only
- raw email/url/provider payload not emitted: ready_for_internal_dry_run | covered_by=fast_alert_path.py + delivery_queue.py + email_template.py + email_provider_adapter.py + alert_preference_center.py | evidence=privacy_guard_cross_artifacts

## 8. Preview-Only Blocker Matrix
- actual live crawl: severity=blocker | preview_only_gap | next=P3-SOURCE-CHANGE-DETECTION-LIVE-ADAPTER-CONTRACT
- source selector production adapter: severity=high | preview_only_gap | next=P3-SOURCE-CHANGE-DETECTION-LIVE-ADAPTER-CONTRACT
- persistent crawl snapshot storage: severity=high | preview_only_gap | next=P3-PERSISTENT-ALERT-STORAGE-IMPLEMENTATION-CONTRACT
- scheduler cron / GitHub Actions integration: severity=high | preview_only_gap | next=P3-CRAWL-FRESHNESS-SCHEDULER-CRON-CONTRACT
- persistent subscription storage: severity=blocker | preview_only_gap | next=P3-PERSISTENT-ALERT-STORAGE-IMPLEMENTATION-CONTRACT
- persistent delivery queue: severity=blocker | preview_only_gap | next=P3-PERSISTENT-ALERT-STORAGE-IMPLEMENTATION-CONTRACT
- worker locking / concurrency dedupe: severity=high | preview_only_gap | next=P3-PERSISTENT-ALERT-STORAGE-IMPLEMENTATION-CONTRACT
- actual email provider SDK/API send: severity=blocker | preview_only_gap | next=P3-EMAIL-PROVIDER-SEND-ENABLEMENT-CONTRACT
- real provider payload generation: severity=high | preview_only_gap | next=P3-EMAIL-PROVIDER-SEND-ENABLEMENT-CONTRACT
- webhook endpoint: severity=high | preview_only_gap | next=P3-EMAIL-PROVIDER-SEND-ENABLEMENT-CONTRACT
- webhook signature verification: severity=high | preview_only_gap | next=P3-EMAIL-PROVIDER-SEND-ENABLEMENT-CONTRACT
- persistent webhook dedupe: severity=medium | preview_only_gap | next=P3-PERSISTENT-ALERT-STORAGE-IMPLEMENTATION-CONTRACT
- auth/session/manage link token: severity=blocker | preview_only_gap | next=P3-UNSUBSCRIBE-MANAGE-ENDPOINT-CONTRACT
- actual unsubscribe/manage endpoint: severity=blocker | preview_only_gap | next=P3-UNSUBSCRIBE-MANAGE-ENDPOINT-CONTRACT
- landing/signup frontend: severity=medium | preview_only_gap | next=P3-ALERT-MVP-LANDING-PAGE-COPY-IMPLEMENTATION
- admin review UI: severity=medium | preview_only_gap | next=P3-PRIVATE-BETA-RUNBOOK
- monitoring/alert logs: severity=blocker | preview_only_gap | next=P3-PRIVATE-BETA-RUNBOOK
- compliance/privacy policy copy: severity=high | preview_only_gap | next=P3-PRIVATE-BETA-RUNBOOK
- domain/email deliverability setup: severity=high | preview_only_gap | next=P3-EMAIL-PROVIDER-SEND-ENABLEMENT-CONTRACT
- rate limits/source TOS review: severity=blocker | preview_only_gap | next=P3-PRIVATE-BETA-RUNBOOK

## 9. Beta Phase Decision
- internal_fixture_dry_run: allowed_now=True | status=ready_for_internal_dry_run | blockers=0
- local_end_to_end_preview: allowed_now=True | status=ready_for_preview_beta | blockers=0
- private_beta_preview_only: allowed_now=True | status=ready_for_preview_beta | blockers=6
- private_beta_with_real_email: allowed_now=False | status=blocked_for_real_beta | blockers=18
- public_beta: allowed_now=False | status=blocked_for_real_beta | blockers=20
- production: allowed_now=False | status=blocked_for_real_beta | blockers=20

## 10. Internal Dry-Run 가능 여부
- 가능. Synthetic fixture 기반 full preview pipeline dry-run은 현재 artifact 기준으로 지원된다.

## 11. Private Beta With Real Email Blocker
- blocked. provider_send_enabled=false, real provider send 미구현, unsubscribe/manage endpoint 부재, persistence/auth/compliance gap이 남아 있다.

## 12. Public Beta Blocker
- blocked. live crawl, persistent queue/storage, monitoring/logging, webhook verification, source TOS/rate-limit review가 모두 필요하다.

## 13. Privacy / No-Fake / Source-Gap / Broad / Manual-Review Guard 결과
- privacy guard passed=True
- fake-fill blocked: yes
- broad query direct alert blocked: yes
- manual-review fast-path blocked: yes
- source-gap exact-only preserved: yes

## 14. 다음 Milestone 우선순위
- 1. P3-SOURCE-CHANGE-DETECTION-LIVE-ADAPTER-CONTRACT: Live crawl and source adapter is the first hard blocker for anything beyond fixtures.
- 2. P3-CRAWL-FRESHNESS-SCHEDULER-CRON-CONTRACT: Scheduler logic needs a recurring orchestrator boundary next.
- 3. P3-PERSISTENT-ALERT-STORAGE-IMPLEMENTATION-CONTRACT: Persistent subscription, snapshot, queue, and webhook state becomes the next major beta gap.
- 4. P3-ALERT-MVP-LANDING-PAGE-COPY-IMPLEMENTATION: Preview-only beta can benefit from a real operator-facing signup surface.
- 5. P3-EMAIL-PROVIDER-SEND-ENABLEMENT-CONTRACT: Real email beta stays blocked until actual provider send and payload boundaries exist.
- 6. P3-UNSUBSCRIBE-MANAGE-ENDPOINT-CONTRACT: Real beta requires secure manage/unsubscribe endpoints.
- 7. P3-PRIVATE-BETA-RUNBOOK: Operational runbook, monitoring, TOS review, and beta ops need to be written down before exposure.

## 15. Output JSON / Production Code 미수정 여부
- 이번 라운드는 audit/checklist artifact만 생성했다.
- production crawler/search/frontend/auth/provider send/DB/cron code는 수정하지 않았다.

## 16. 테스트 결과
- module import / artifact load / readiness matrix / phase decision / blocker coverage 검증 포함

## 17. 남은 위험
- preview-only artifact를 real beta readiness로 오인하면 안 된다.
- persistence, live adapter, auth/manage endpoint, compliance, deliverability가 남아 있다.

## 18. 다음 Backlog 후보
- P3-SOURCE-CHANGE-DETECTION-LIVE-ADAPTER-CONTRACT
- P3-CRAWL-FRESHNESS-SCHEDULER-CRON-CONTRACT
- P3-PERSISTENT-ALERT-STORAGE-IMPLEMENTATION-CONTRACT
- P3-ALERT-MVP-LANDING-PAGE-COPY-IMPLEMENTATION
- P3-PRIVATE-BETA-RUNBOOK
