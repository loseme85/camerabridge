# P3-ALERT-MVP-PREFERENCE-CENTER-IMPLEMENTATION

## 1. 작업 목적
- preference center contract를 순수 상태 전이 함수로 옮겨 subscription/preference 업데이트와 downstream effect를 deterministic하게 계산한다.

## 2. 구현 요약
- `alert_preference_center.py`에 snapshot build, update request 생성, subscription state transition, condition/source/source-gap/source-expansion update, global unsubscribe, fast alert effect, delivery queue effect 계산을 구현했다.

## 3. alert_preference_center.py public API
- `validate_preference_profile`
- `validate_subscription_preference`
- `build_preference_snapshot`
- `create_preference_update_request`
- `apply_preference_update`
- `update_subscription_frequency`
- `update_condition_preferences`
- `update_source_preferences`
- `update_source_gap_preference`
- `apply_global_unsubscribe`
- `compute_fast_alert_effect`
- `compute_delivery_queue_effect`
- `process_preference_update_batch`

## 4. preference snapshot schema
- fixture snapshots: `3`

## 5. update request/result schema
- update results: `19`
- update status counts: `{'accepted_preview': 13, 'rejected_invalid_state': 2, 'rejected_suppressed': 1, 'requires_verification': 1, 'rejected_invalid_action': 1, 'blocked_policy_violation': 1}`

## 6. subscription state transition 결과
- transitions: `5`

## 7. frequency/digest transition 결과
- digest conversion scenarios included for `lumix 24-105` and `sl 24-90 generic`

## 8. condition preference update 결과
- condition rows: `2`

## 9. source preference update 결과
- source filter rows: `2`

## 10. source-gap/source-expansion preference 결과
- source-gap rows: `2`
- source-expansion rows: `1`

## 11. suppression/verification/global unsubscribe guard 결과
- suppression guard rows: `2`
- verification guard rows: `1`

## 12. delivery queue effect compatibility
- delivery queue effect rows: `13`

## 13. raw email/token/provider payload guard
- policy violation rows: `2`

## 14. output JSON / production code 미수정 여부
- 허용된 implementation / test / artifact 파일만 수정했다.

## 15. 테스트 결과
- scenario validations: `19/19`
- implementation checks: `5/5`
- jsonl validation: `True`
