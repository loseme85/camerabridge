# P3-ALERT-MVP-LANDING-PAGE-COPY-IMPLEMENTATION

## 1. 작업명
P3-ALERT-MVP-LANDING-PAGE-COPY-IMPLEMENTATION

## 2. 작업 목적
Camera Bridge Alert MVP의 landing page / waitlist / signup / trust / limitation / FAQ copy를 beta-safe하게 구현한다.

## 3. 구현 요약
- EN/KO landing copy package, CTA, FAQ, source coverage, beta notice, disclaimer, A/B variants를 artifact로 구현했다.
- real-email/private-beta readiness를 과장하지 않도록 claim safety checker를 함께 붙였다.

## 4. Landing Page Copy Implementation Scope
- copy artifact only
- no frontend page
- no signup form
- no auth/email/provider runtime

## 5. Copy Policy
- real-email / real-time / guaranteed / all-sources / official-affiliation overclaim blocked
- waitlist / preview-only / no-fake-fill / source limitation disclosure required

## 6. Landing Page Section Map
- section rows = `26`
- hero/problem/promise/how_it_works/beta_status/rare_watch_examples/no_fake_fill/source_coverage/early_access_waitlist/trust_privacy/manage_unsubscribe/FAQ/final_CTA

## 7. English Copy Package
- English hero rows = `1`
- Stop refreshing dealer sites framing
- waitlist/private beta preparation wording

## 8. Korean Copy Package
- Korean hero rows = `1`
- 희귀 라이카 매물 / 프라이빗 베타 준비 / 대기 신청 wording

## 9. CTA Variants
- CTA rows = `8`
- early access / beta access / watch this search / request a source

## 10. No Fake-Fill / No Adjacent Substitution Messaging
- exact match discipline and refinement-first behavior are explained in user language

## 11. Beta Status / Limitation Disclosure
- beta status notice rows = `2`
- real-email alerts are not enabled for all users yet

## 12. Source Coverage Disclosure
- source coverage notice rows = `2`
- selected sources disclosed; blocked/review sources disclosed

## 13. FAQ Package
- FAQ rows = `24`
- marketplace/affiliation/email status/broad query/source coverage/unsubscribe/privacy/source request included

## 14. Privacy / Unsubscribe / Manage Copy
- verification, manage, pause/unsubscribe, and privacy-delete direction are mentioned without overexposing internal implementation

## 15. No Affiliation / Source Disclaimer
- disclaimer rows = `4`
- Leica non-affiliation and source volatility disclaimers included in EN/KO

## 16. Copy Variants
- variant rows = `5`
- accuracy-first / collector-pain / rare-alert waitlist / Korean localized / founder-direct

## 17. Claim Safety Checker 결과
- claim safety rows = `35`
- prohibited English and Korean overclaims are blocked

## 18. Scenario Validation 결과
- scenario rows = `15`
- failed scenarios = `[]`

## 19. Real Email / Production Claim Guard
- no claim that real email is already active for all users
- no claim of all-source monitoring, guaranteed accuracy, official Leica affiliation, or instant delivery

## 20. Output JSON / Production Code 미수정 여부
- artifact-only copy implementation
- no frontend/auth/provider/crawler/search production files modified

## 21. 테스트 결과
- copy tests, runner, JSONL validation, and golden_set expected to pass

## 22. 남은 위험
- eventual frontend implementation will still need visual hierarchy, copy density tuning, and legal/compliance review before user-facing launch.
- beta-state wording should be revisited whenever send/runtime status changes.

## 23. 다음 Backlog 후보
- P3-PERSISTENT-ALERT-STORAGE-DB-ADAPTER-CONTRACT
- P3-UNSUBSCRIBE-MANAGE-ENDPOINT-IMPLEMENTATION
- P3-EMAIL-PROVIDER-SEND-ENABLEMENT-IMPLEMENTATION
- P3-PRIVATE-BETA-ADMIN-QUEUE-CONTRACT
- P3-ALERT-MVP-LANDING-PAGE-FRONTEND-CONTRACT
