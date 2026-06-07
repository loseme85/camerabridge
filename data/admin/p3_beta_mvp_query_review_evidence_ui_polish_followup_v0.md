# P3-BETA-MVP-QUERY-REVIEW-EVIDENCE-UI-POLISH-FOLLOWUP

## 1. 작업명
- `P3-BETA-MVP-QUERY-REVIEW-EVIDENCE-UI-POLISH-FOLLOWUP`

## 2. owner recheck 결과 요약
- Logic stayed conservative, but Query review still exposed too many internal/debug terms for external tester review.

## 3. UI polish 필요 이유
- Translate evidence pools, unlock reasons, and top result roles into tester-facing language without loosening any pricing or routing guard.

## 4. Query review 기본/상세 모드 설계
- 기본 모드: 검색어 / 해석된 target / 가격 상태 / 이유 / evidence summary / unlock condition / top evidence
- 상세 모드: title / source / price / result role / price usage / exclusion reason

## 5. 사용자용 copy 변환표
- exact_variant_pool -> Used for exact price
- exact_base_model_pool -> Same base model evidence
- broader_family_pool -> Broader reference only
- excluded_pool -> Not used for price

## 6. result role label 변환표
- Exact variant -> Exact variant
- Exact base model -> Same base model
- Broader family -> Broader reference
- Third-party top result -> Third-party or adjacent result
- Query incompatible -> Not compatible with this query

## 7. price usage label 변환표
- Used for exact price
- Used for same base model price
- Used as broader reference
- Not used — Price outlier
- Not used — Duplicate listing
- Not used — Different model
- Not used — Third-party item
- Not used — Accessory, not camera/lens

## 8. 35 lux aa 결과
- `35 lux aa`: Reference price only. / AA-specific price evidence is not enough yet.

## 9. Noctilux 50 f1 E60 결과
- `Noctilux 50 f1 E60`: Reference price only. / E60-specific price evidence is not enough yet.

## 10. Summicron 50 rigid 결과
- `Summicron 50 rigid`: Exact price is available. / Clean exact variant price evidence

## 11. Summilux-M 50 ASPH 결과
- `Summilux-M 50 ASPH`: Reference price only. / Top visible results include third-party or adjacent items.

## 12. Leica M5 / M50/1.2 body-lens boundary 결과
- `leica m5`: Body market summary is available. / Clean same-model price evidence
- `M50/1.2`: Reference price only. / Only broader reference pricing is safe for this query right now.

## 13. dev token 노출 여부
- []

## 14. external tester safe copy guard
- copy summary excludes raw URLs, raw HTML, private contact data, and internal-only identifiers.

## 15. git diff 요약
- branch = beta-ui-redesign-controlled-preview
- head = f6fcf81bd83d9c2ec60f411e3c3387559946033a
- subject = polish: simplify query review evidence UI
- files = api/search.py, app/templates/index.html, index.html

## 16. commit/push 수행 여부
- commit_executed = False
- push_executed = False
- push_succeeded = False

## 17. preview deployment URL
- not recorded

## 18. production/public/access guard
- production_launch_go = False
- production_alias_connect_allowed = False
- public_unrestricted_access_enabled = False
- external_tester_access_enabled = False
- invite_sent_count = 0
- provider_send_count = 0
- webhook_call_count = 0
- production_DB_write_count = 0
- access_activation_performed = False
- main_direct_push_executed = False
- production_promote_executed = False
- tester_link_send_allowed = False
- raw_identity_recorded = False
- raw_contact_recorded = False
- external_link_sent = False
- fake_fill_added = False

## 19. 테스트 결과
- ui_still_too_technical = []
- price_projection_regressed = []
- body_lens_regression = []

## 20. production alias 연결 가능 여부
- `production_alias_connect_allowed = false`

## 21. 다음 backlog 후보
- P3-BETA-MVP-QUERY-REVIEW-EVIDENCE-UI-POLISH-OWNER-RECHECK
- P3-BETA-MVP-LOCKED-ENTRY-AND-PRICE-UNLOCK-AUDIT
- P3-BETA-MVP-LENS-VARIANT-TOKEN-PARSER-COVERAGE-FIXUP
- P3-BETA-MVP-LENS-BOUNDARY-CONFLICT-RESOLUTION-FIXUP
