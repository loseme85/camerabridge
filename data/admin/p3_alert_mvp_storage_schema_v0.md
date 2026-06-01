# P3-ALERT-MVP-STORAGE-SCHEMA

## 1. 작업명
- P3-ALERT-MVP-STORAGE-SCHEMA

## 2. 작업 목적
- signup payload를 실제 DB 구현 전에 저장 가능한 schema contract와 preview record로 변환

## 3. 구현 요약
- `alert_storage_contract.py`에 signup/subscription/verification/event/notification/suppression schema dataclass와 enum을 추가
- signup flow artifact를 입력으로 읽어 signup/verification/subscription preview와 blocked preview를 생성
- 실제 DB migration, email 저장, token 저장은 하지 않음

## 4. storage contract 요약
- signup_storage_status: `['accepted_pending_verification', 'accepted_no_result_pending_verification', 'waitlist_pending_verification', 'blocked_manual_review', 'blocked_refinement_required', 'blocked_too_broad', 'blocked_unavailable_for_mvp']`
- subscription_status: `['pending_email_verification', 'active', 'paused', 'unsubscribed', 'suppressed', 'expired', 'deleted']`
- verification_status: `['not_started', 'pending', 'verified', 'expired', 'failed', 'cancelled']`
- subscription_type: `['normal_alert', 'source_gap_alert', 'source_expansion_waitlist', 'price_watch_later', 'manual_review_block', 'refinement_block']`
- dedupe_scope: `['email_watchlist', 'email_query', 'email_query_filters', 'email_source_gap']`

## 5. storage entity/table summary
- signup_record_preview count: `17`
- verification_record_preview count: `17`
- subscription_record_preview count: `17`
- blocked_signup_preview count: `15`

## 6. signup status -> storage status mapping
- `alert_signup` -> `accepted_pending_verification` -> `normal_alert`
- `source_gap_alert_signup` -> `accepted_no_result_pending_verification` -> `source_gap_alert`
- `source_expansion_waitlist` -> `waitlist_pending_verification` -> `source_expansion_waitlist`
- `manual_review_unavailable` -> `blocked_manual_review`
- `refinement_required` -> `blocked_refinement_required`
- `excluded_too_broad` -> `blocked_too_broad`
- `unavailable_for_mvp` -> `blocked_unavailable_for_mvp`

## 7. dedupe key policy
- normal alert: `hash(email_hash + watchlist_id + canonical_query + selected_filters)`
- source gap alert: `hash(email_hash + watchlist_id + canonical_query + source_gap_related)`
- source expansion waitlist: `hash(email_hash + canonical_query + subscription_type)`
- blocked / refinement / manual-review: subscription은 생성하지 않고 blocked preview만 남김

## 8. privacy/minimal PII policy
- raw email은 artifact에 저장하지 않음
- `email_hash`와 `email_encrypted_ref` preview만 둠
- `email_domain`은 `example.com` placeholder만 사용
- verification token raw value는 저장하지 않고 `token_hash`만 둠

## 9. storage preview count / distribution
- signup_storage_status distribution: `{'accepted_pending_verification': 10, 'accepted_no_result_pending_verification': 5, 'waitlist_pending_verification': 2, 'blocked_manual_review': 4, 'blocked_too_broad': 5, 'blocked_refinement_required': 6}`
- subscription_type distribution: `{'normal_alert': 10, 'source_gap_alert': 5, 'source_expansion_waitlist': 2, 'manual_review_block': 4, 'refinement_block': 11}`

## 10. normal include storage 결과
- `summilux m 35` -> signup=`accepted_pending_verification` / sub=`normal_alert` / created=`True`
- `35 lux aa` -> signup=`accepted_pending_verification` / sub=`normal_alert` / created=`True`
- `m6` -> signup=`accepted_pending_verification` / sub=`normal_alert` / created=`True`
- `mp` -> signup=`accepted_pending_verification` / sub=`normal_alert` / created=`True`
- `r 180 apo telyt` -> signup=`accepted_pending_verification` / sub=`normal_alert` / created=`True`
- `sigma 24-70 l` -> signup=`accepted_pending_verification` / sub=`normal_alert` / created=`True`
- `lumix 24-105` -> signup=`accepted_pending_verification` / sub=`normal_alert` / created=`True`

## 11. source-gap storage 결과
- `sigma 14-24 l` -> signup=`accepted_no_result_pending_verification` / sub=`source_gap_alert` / created=`True`
- `sigma 14-24 dg dn` -> signup=`accepted_no_result_pending_verification` / sub=`source_gap_alert` / created=`True`
- `시그마 14-24 아트` -> signup=`accepted_no_result_pending_verification` / sub=`source_gap_alert` / created=`True`

## 12. waitlist storage 결과
- `sigma 28-70 dg dn l` -> signup=`waitlist_pending_verification` / sub=`source_expansion_waitlist` / created=`True`
- `sigma 28-105 dg dn l` -> signup=`waitlist_pending_verification` / sub=`source_expansion_waitlist` / created=`True`

## 13. blocked signup 결과
- `leica m-a` -> signup=`blocked_manual_review` / created=`False` / block=`body_intent_not_launch_safe`
- `leica m10 monochrom` -> signup=`blocked_manual_review` / created=`False` / block=`body_intent_not_launch_safe`
- `leica m10-r` -> signup=`blocked_manual_review` / created=`False` / block=`body_intent_not_launch_safe`
- `leica m11 monochrom` -> signup=`blocked_manual_review` / created=`False` / block=`body_intent_not_launch_safe`
- `summicron` -> signup=`blocked_too_broad` / created=`False` / block=`too_broad_query`
- `summilux` -> signup=`blocked_too_broad` / created=`False` / block=`too_broad_query`
- `cron` -> signup=`blocked_refinement_required` / created=`False` / block=`too_broad_query`
- `lux` -> signup=`blocked_refinement_required` / created=`False` / block=`too_broad_query`
- `50 cron` -> signup=`blocked_refinement_required` / created=`False` / block=`too_broad_query`
- `leica r` -> signup=`blocked_refinement_required` / created=`False` / block=`too_broad_query`
- `leica lens` -> signup=`blocked_too_broad` / created=`False` / block=`too_broad_query`
- `leica m` -> signup=`blocked_too_broad` / created=`False` / block=`too_broad_query`
- `leica sl` -> signup=`blocked_too_broad` / created=`False` / block=`too_broad_query`

## 14. event / notification / suppression future schema
- `alert_events`: future matching engine output preview included
- `alert_notification_logs`: future delivery trace preview included
- `alert_suppression_records`: unsubscribe/bounce/privacy suppression preview included

## 15. 수정 파일 목록
- `alert_storage_contract.py`
- `scripts/run_p3_alert_mvp_storage_schema.py`
- `tests/test_alert_mvp_storage_schema.py`
- `data/admin/p3_alert_mvp_storage_schema_v0.md`
- `data/admin/p3_alert_mvp_storage_schema_v0.jsonl`
- `data/admin/alert_mvp_storage_schema_v0.json`

## 16. 수정하지 않은 파일/영역
- production search code
- crawler production code
- output JSON / taxonomy seed / canonical index / raw data / search index

## 17. 테스트 결과
- script run / JSONL validation / storage schema JSON validation / py_compile / golden set recorded separately

## 18. 남은 위험
- verification lifecycle와 resend/rate-limit policy는 아직 contract 수준
- waitlist subscription을 `active`와 별도 status로 둘지 여부는 실제 DB 설계 단계에서 다시 판단 필요
- unsubscribe token rotation / privacy delete workflow는 후속 contract로 분리하는 편이 좋음

## 19. 다음 backlog 후보
- `P3-ALERT-MVP-EMAIL-VERIFICATION-CONTRACT`
- `P3-ALERT-MVP-DELIVERY-SIMULATION`
- `P3-ALERT-MVP-NO-RESULT-UI-CONTRACT`
- `P3-ALERT-MVP-UNSUBSCRIBE-CONTRACT`
- `P3-THIRD-PARTY-SOURCE-LIST-EXPANSION-IMPLEMENTATION`
