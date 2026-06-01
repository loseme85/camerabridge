# P3-PERSISTENT-ALERT-STORAGE-DB-ADAPTER-CONTRACT

## 1. 작업명
P3-PERSISTENT-ALERT-STORAGE-DB-ADAPTER-CONTRACT

## 2. 작업 목적
persistent_alert_storage.py의 local repository preview를 실제 DB adapter로 옮기기 전에 필요한 schema mapping, transaction, locking, idempotency, retention, privacy delete, migration boundary를 contract로 정의한다.

## 3. 구현 요약
- 18개 local domain을 DB entity boundary로 매핑했다.
- adapter 후보, field guard, index/unique/FK, transaction, locking, retention/privacy delete, readiness/migration preview를 contract로 정리했다.
- 실제 DB 연결, migration, ORM 모델 생성은 하지 않았다.

## 4. DB Adapter Contract Scope
- contract only
- no actual DB connection
- no migration generation
- no ORM/model generation

## 5. DB Adapter Policy
- actual_db_enabled=false
- db_connection_allowed=false
- migration_generation_allowed=false
- raw email/url/html/provider payload/webhook body storage disallowed

## 6. DB Adapter Candidates
- candidate rows = `4`
- in_memory_preview / sqlite_local_beta / postgres / supabase_postgres included

## 7. Local Domain -> DB Entity Mapping
- entity mapping rows = `18`
- all 18 local domains mapped to DB entities

## 8. Field Mapping / Raw Data Guard
- db field rows = `262`
- policy violation rows = `9`
- no raw_email/raw_url/raw_html/provider_payload/webhook_body columns allowed

## 9. Index / Unique Constraint Policy
- index rows = `13`
- unique rows = `9`
- idempotency/dedupe/crawl interval/webhook uniqueness included

## 10. Foreign Key / Relationship Policy
- foreign key rows = `12`
- relationship policy is defined without generating SQL

## 11. Transaction Boundary
- transaction rows = `7`
- snapshot/crawl/delivery/provider/webhook/unsubscribe/privacy delete transactions included

## 12. Locking / Concurrency Policy
- locking rows = `6`
- crawl/delivery/webhook/privacy/subscription/source locks included

## 13. Idempotency / Dedupe Persistence
- idempotency rows = `6`
- listing/crawl/delivery/provider/webhook/unsubscribe dedupe boundaries included

## 14. Privacy Delete / Retention Policy
- retention rows = `11`
- privacy delete rows = `1`
- email_encrypted_ref redaction, subscription delete, queued job cancellation, future job block included

## 15. DB Readiness / Blocker Matrix
- readiness rows = `5`
- private real-email beta remains blocked until actual DB adapter implementation and related gates pass

## 16. Migration Plan Preview
- migration rows = `7`
- schema_draft/local_sqlite_trial/postgres_schema_contract/db_adapter_implementation/migration_dry_run/private_beta_db_enablement/production_migration_candidate included

## 17. Scenario Validation 결과
- scenario rows = `15`
- failed scenarios = `[]`

## 18. Actual DB / Migration 미구현 Guard
- no DB connection
- no migration files
- no SQL generation

## 19. Output JSON / Production Code 미수정 여부
- 이번 라운드는 contract artifact만 생성한다.
- production persistence runtime, worker runtime, provider send, webhook, frontend, crawler production 코드는 수정하지 않는다.

## 20. 테스트 결과
- contract tests, runner, JSONL validation, and golden_set expected to pass

## 21. 남은 위험
- actual lock semantics, isolation guarantees, RLS/auth boundaries, and migration rollback drills still need implementation-phase validation.
- sqlite and supabase suitability depend on later operational/security decisions.

## 22. 다음 Backlog 후보
- P3-UNSUBSCRIBE-MANAGE-ENDPOINT-IMPLEMENTATION
- P3-EMAIL-PROVIDER-SEND-ENABLEMENT-IMPLEMENTATION
- P3-PRIVATE-BETA-ADMIN-QUEUE-CONTRACT
- P3-ALERT-MVP-LANDING-PAGE-FRONTEND-CONTRACT
- P3-PERSISTENT-ALERT-STORAGE-DB-ADAPTER-IMPLEMENTATION
