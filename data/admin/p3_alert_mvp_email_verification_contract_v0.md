# P3-ALERT-MVP-EMAIL-VERIFICATION-CONTRACT

## 작업 목적
- signup/storage preview를 바탕으로 email verification lifecycle과 activation policy를 contract로 정의한다.

## 구현 요약
- raw email, raw token 없이 verification preview / activation preview / blocked-not-verifiable preview를 생성했다.
- resend cooldown, resend max, attempt max, token expiry, existing active reuse 정책을 artifact로 고정했다.

## Email Verification Contract 요약
- token ttl: 24h
- max attempts: 5
- resend cooldown: 600s
- resend max per 24h: 3
- resend 시 token_hash를 rotate하고 이전 token은 revoked로 간주한다.

## Token Lifecycle Policy
- create -> pending/active
- verify success -> verified/used + subscription active
- expired -> expired/expired
- invalid token -> pending 유지 + attempt 증가
- max attempts 도달 -> failed/invalid
- resend after cooldown -> pending 유지 + token rotate

## Verification Preview 분포
- total: 17
- normal_alert: 10
- source_expansion_waitlist: 2
- source_gap_alert: 5

## Activation Result 분포
- total: 18
- noop_existing_active: 1
- verified_and_activated: 15
- verified_waitlist_activated: 2

## Blocked Signup 차단 요약
- total: 15
- blocked_manual_review: 4
- blocked_refinement_required: 6
- blocked_too_broad: 5

## Scenario Validation 분포
- blocked_not_verifiable: 11
- expired_token: 1
- invalid_token: 1
- normal_alert_verification_success: 7
- resend_after_cooldown: 1
- resend_before_cooldown: 1
- source_expansion_waitlist_verification_success: 2
- source_gap_alert_verification_success: 3
- too_many_attempts: 1

## Privacy Check
- raw email absent
- raw token absent
- token_hash present

## Dedupe / Reuse Policy
- same dedupe_key active subscription exists -> existing subscription reused
- duplicate verified signup does not create another active subscription

## 수정 파일 목록
- alert_verification_contract.py
- scripts/run_p3_alert_mvp_email_verification_contract.py
- tests/test_alert_mvp_email_verification_contract.py
- data/admin/p3_alert_mvp_email_verification_contract_v0.md
- data/admin/p3_alert_mvp_email_verification_contract_v0.jsonl
- data/admin/alert_mvp_email_verification_contract_v0.json

## 수정하지 않은 파일/영역
- production search/parser/resolver/crawler code
- output JSON / taxonomy seed / canonical index / raw data / search index

## 다음 backlog 후보
- P3-ALERT-MVP-DELIVERY-SIMULATION
- P3-ALERT-MVP-NO-RESULT-UI-CONTRACT
- P3-ALERT-MVP-UNSUBSCRIBE-CONTRACT
- P3-ALERT-MVP-EMAIL-TEMPLATE-CONTRACT
- P3-THIRD-PARTY-SOURCE-LIST-EXPANSION-IMPLEMENTATION
