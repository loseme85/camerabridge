# P3-PRIVATE-BETA-RUNBOOK

## 1. 작업명
P3-PRIVATE-BETA-RUNBOOK

## 2. 작업 목적
Camera Bridge Alert MVP를 private beta로 운영하기 전에 필요한 phase, gate, 절차, 롤백 기준, incident 대응, monitoring, manual review, privacy/compliance 체크를 runbook contract로 고정한다.

## 3. 구현 요약
- preview-only beta와 real-email beta를 분리한 phase/runbook을 정의했다.
- send enablement, unsubscribe/manage, storage, cron, live adapter readiness를 운영 관점의 gate/checklist/go-no-go로 연결했다.
- real-email beta는 blocked로 유지하고, 운영자가 무엇을 먼저 갖춰야 하는지 명확히 적었다.

## 4. Private Beta Runbook Scope
- runbook/operations contract only
- no actual beta launch
- no actual provider send / webhook / DB / cron enablement

## 5. Beta Phases
- phase rows = `8`
- internal_fixture_dry_run / local_end_to_end_preview / preview_only_private_beta are preview-safe phases
- provider_payload_preview and every real-email phase remain blocked

## 6. Readiness Gates
- gate rows = `20`
- storage/db/cron/adapter/provider/unsubscribe/privacy/monitoring/rollback/rate-limit gates included

## 7. Launch Checklist
- checklist rows = `14`
- source/crawl/detection/queue/template/provider/privacy/manual-review/rollback readiness categories included

## 8. Go/No-Go Decision Matrix
- decision rows = `8`
- preview_only_private_beta = go_with_limits
- private_beta_real_email = blocked

## 9. Operational Procedures
- procedure rows = `27`
- daily review, source health, skip review, fake-fill guard, queue review, unsubscribe/suppression review, privacy delete review, weekly go/no-go review included

## 10. Rollback Criteria
- rollback rows = `12`
- unsubscribe/suppression/privacy/fake-fill/duplicate send/provider complaint/manual backlog triggers included

## 11. Incident Response
- incident rows = `13`
- raw leak, duplicate send, unsubscribe/suppression failure, fake-fill, source crawl blocked, provider complaints, storage corruption, queue stuck included

## 12. Monitoring Metrics
- metric rows = `20`
- crawl/parse/queue/unsubscribe/suppression/privacy/provider block/latency metrics included

## 13. Manual Review/Admin Queue Policy
- manual review queue rows = `11`
- manual-review/fake-fill/broad-query/raw-policy/provider-not-ready/user-complaint/privacy-delete queues included

## 14. Privacy/Compliance Checks
- privacy rows = `15`
- raw email/url/provider payload/webhook body prohibited
- token hash only, unsubscribe/manage link, privacy delete, suppression, disclaimers, no account enumeration included

## 15. Source/Watch Target Beta Limits
- source limit rows = `9`
- watch target limit rows = `6`
- only Map Camera / Fujiya / Leica Store Miami / Ffordes / MPB US are allowed preview sources by default
- broad/manual/anti-bot unsafe paths remain blocked or review-only

## 16. Scenario Validation 결과
- scenario rows = `16`
- failed scenarios = `[]`

## 17. Real Send / Actual Cron / DB 미구현 Guard
- real send stays disabled
- actual cron stays disabled
- actual DB stays disabled

## 18. Output JSON / Production Code 미수정 여부
- 이번 라운드는 runbook artifact만 생성한다.
- provider/frontend/auth/DB/cron/crawler production 코드는 수정하지 않는다.

## 19. 테스트 결과
- runbook tests, runner, JSONL validation, and golden_set expected to pass

## 20. 남은 위험
- real-email beta readiness still depends on DB adapter, unsubscribe/manage implementation, provider send enablement implementation, webhook runtime, monitoring implementation, and compliance signoff.
- preview-only beta still needs disciplined manual review and source/watch scope control.

## 21. 다음 Backlog 후보
- P3-ALERT-MVP-LANDING-PAGE-COPY-IMPLEMENTATION
- P3-PERSISTENT-ALERT-STORAGE-DB-ADAPTER-CONTRACT
- P3-UNSUBSCRIBE-MANAGE-ENDPOINT-IMPLEMENTATION
- P3-EMAIL-PROVIDER-SEND-ENABLEMENT-IMPLEMENTATION
- P3-PRIVATE-BETA-ADMIN-QUEUE-CONTRACT
