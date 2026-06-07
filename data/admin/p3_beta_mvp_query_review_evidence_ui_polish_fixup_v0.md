# P3-BETA-MVP-QUERY-REVIEW-EVIDENCE-UI-POLISH-FIXUP

## 1. 작업명
- `P3-BETA-MVP-QUERY-REVIEW-EVIDENCE-UI-POLISH-FIXUP`

## 2. owner recheck 결과 요약
- Previous runtime projection fix passed functionally, but Query review still read like an owner-debug surface instead of external tester copy.

## 3. UI polish 필요 이유
- The panel now needs to explain search interpretation, price status, and evidence use without exposing internal pool names or debug tokens.

## 4. Query review 기본/상세 모드 설계
- 기본: 검색어 / 해석된 target / 가격 상태 / 이유 / evidence / unlock requirement / top evidence
- 상세: 증거 행별 title / source / price / result role / price usage / exclusion reason

## 5. 사용자용 copy 변환표
- `no_exact_or_strong_visible_results` -> No exact strong visible listings yet.
- `weak_only_fallback` -> Results are visible, but not strong enough for model-level pricing.
- `third_party_top_domination` -> Top visible results include third-party or adjacent items.
- `too_wide_price_band` -> Reference prices are too spread out to show safely.
- `dangerous_unknown_family_token` -> Query includes a model-like term that needs verification.

## 6. result role label 변환표
- `Exact variant` -> Exact variant match
- `Exact base model` -> Same base model
- `Broader family` -> Broader family reference
- `Third-party top result` -> Third-party result
- `Query incompatible` -> Not compatible with this query

## 7. price usage label 변환표
- `exact_variant_pool` -> Used for exact price
- `exact_base_model_pool` -> Used for same-model price
- `broader_family_pool` -> Used as reference
- `excluded:outlier` -> Not used — Price outlier
- `excluded:wrong_model` -> Not used — Wrong model
- `excluded:duplicate` -> Not used — Duplicate listing
- `excluded:accessory` -> Not used — Accessory or part
- `excluded:third_party` -> Not used — Third-party item

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
- `M50/1.2`: Reference price only. / Exact or strong compatible listings are visible.

## 13. dev token 노출 여부
- visible rows = []

## 14. external tester safe copy guard
- forbidden phrases are blocked from display summary checks

## 15. git diff 요약
- branch = beta-ui-redesign-controlled-preview
- head = 48a8394506c27e37c311baa9d928a6f040628183
- subject = fix: align price band projection and show query result evidence
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
- dev_token_visible = []
- query_review_too_technical = []
- price_state_copy_confusing = []
- price_projection_regressed = []
- body_lens_regression = []

## 20. production alias 연결 가능 여부
- `production_alias_connect_allowed = false`

## 21. 다음 backlog 후보
- P3-BETA-MVP-QUERY-REVIEW-EVIDENCE-UI-POLISH-OWNER-RECHECK
- P3-BETA-MVP-LOCKED-ENTRY-AND-PRICE-UNLOCK-AUDIT
- P3-BETA-MVP-LENS-VARIANT-TOKEN-PARSER-COVERAGE-FIXUP
- P3-BETA-MVP-LENS-BOUNDARY-CONFLICT-RESOLUTION-FIXUP
