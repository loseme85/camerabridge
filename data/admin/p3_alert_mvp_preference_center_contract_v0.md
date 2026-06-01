# P3-ALERT-MVP-PREFERENCE-CENTER-CONTRACT

## 1. 작업명
- P3-ALERT-MVP-PREFERENCE-CENTER-CONTRACT

## 2. 작업 목적
- 사용자가 알림 강도, 빈도, 조건, source, source-gap/source-expansion 상태를 직접 조정할 수 있는 preference center contract를 정의한다.

## 3. 구현 요약
- preference profile, subscription preference, condition/source/digest/source-gap preference, update request/result, access policy를 분리했다.
- update 결과가 fast alert path와 delivery queue에 어떤 영향을 주는지 preview로 고정했다.

## 4. preference center contract 요약
- preference profile rows: 2
- subscription preference rows: 10
- update result rows: 15

## 5. preference profile schema
- email_hash / email_encrypted_ref placeholder만 사용하고 raw email은 금지

## 6. subscription preference schema
- active/paused/pending/suppressed/deleted 상태와 immediate/digest/source-gap/source-expansion 선호를 분리

## 7. condition/source/digest/source-gap preference schema
- max_price / min_price_drop_percent / domestic_only / source_allowlist / digest frequency / fake-fill-forbidden source-gap policy를 포함

## 8. update request/result schema
- update_status, fast_alert_effect, delivery_queue_effect, suppression_effect, requires_reverification 포함

## 9. access policy
- manage link token / verified session later / unsubscribe token preview 제공, raw token 저장 없음

## 10. active/pause/resume 결과
- 35 lux aa active immediate 유지
- Noctilux pause -> future fast alerts blocked
- resume -> future jobs allowed

## 11. common watch digest 결과
- Lumix 24-105 / SL 24-90 generic -> daily digest 전환 가능

## 12. conditional rare / price-drop preference 결과
- Q2 under target price -> max_price condition fast alert 반영
- Summilux-M 35 -> price_drop opt-in + threshold 유지

## 13. source-gap / source-expansion preference 결과
- Sigma 14-24 L -> fake_fill_allowed=false, exact source-gap only
- Sigma 28-70 DG DN L -> source_expansion_available 중심 관리

## 14. global unsubscribe / suppressed / unverified 결과
- global unsubscribe -> queued_jobs_should_be_cancelled
- suppressed -> rejected_suppressed
- pending verification -> requires_verification

## 15. source allowlist / high-risk source guard 결과
- Map Camera / Fujiya allowlist 예시 포함
- Mercari request가 있어도 anti-bot/source-health guard는 유지

## 16. fast alert / delivery queue 영향 결과
- allow_future_fast_alerts / block_future_fast_alerts / convert_to_digest / price_drop_only / source_gap_only 를 명시

## 17. privacy guard 결과
- raw email 없음, raw token 없음, encrypted ref placeholder만 사용

## 18. output JSON / production code 미수정 여부
- production frontend/auth/db/provider/crawler/search code는 수정하지 않았다.

## 19. 테스트 결과
- script, tests, jsonl validation, py_compile, golden_set 기준으로 검증

## 20. 남은 위험
- 실제 UI와 auth/session layer가 붙을 때 token/session access policy를 더 세밀하게 맞춰야 함

## 21. 다음 backlog 후보
- P3-ALERT-MVP-PREFERENCE-CENTER-IMPLEMENTATION
- P3-FAST-ALERT-PATH-IMPLEMENTATION
- P3-SOURCE-CHANGE-DETECTION-IMPLEMENTATION
- P3-ALERT-MVP-LANDING-PAGE-COPY-CONTRACT
- P3-WATCH-BRIDGE-MARKET-SCOUT-CONTRACT
