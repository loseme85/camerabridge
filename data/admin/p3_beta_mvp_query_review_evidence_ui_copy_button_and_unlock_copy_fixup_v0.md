# P3-BETA-MVP-QUERY-REVIEW-EVIDENCE-UI-COPY-BUTTON-AND-UNLOCK-COPY-FIXUP

## 1. 작업명
- `P3-BETA-MVP-QUERY-REVIEW-EVIDENCE-UI-COPY-BUTTON-AND-UNLOCK-COPY-FIXUP`

## 2. owner recheck 결과 요약
- The logic is stable, but the Query review panel still needed a visible copy button and fully human unlock wording for owner and external tester review.

## 3. copy button / unlock copy 변경
- Query review header now keeps a visible `Copy summary` button in the upper-right area.
- Price unlock copy now renders as readable list items instead of slash-separated debug text.

## 4. M50/1.2 조사 결과
- M50/1.2 stays on the Lens path, does not regress to Leica M5 Body, and keeps broader/base Noctilux 50 f1.2 evidence clearly labeled as reference only.

## 5. copy button missing rows
- []

## 6. ui still too technical rows
- []

## 7. regression rows
- []

## 8. git diff 요약
- branch = beta-ui-redesign-controlled-preview
- head = 4cb3392507f62c375beb50f6fd0d6e95f031efcd
- subject = polish: simplify query review evidence UI followup
- files = api/search.py, app/templates/index.html, index.html

## 9. commit/push 수행 여부
- commit_executed = False
- push_executed = False
- push_succeeded = False

## 10. preview deployment URL
- not recorded

## 11. production/public/access guard
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

## 12. 다음 backlog 후보
- P3-BETA-MVP-QUERY-REVIEW-EVIDENCE-UI-COPY-BUTTON-AND-UNLOCK-COPY-OWNER-RECHECK
- P3-BETA-MVP-LOCKED-ENTRY-AND-PRICE-UNLOCK-AUDIT
- P3-BETA-MVP-LENS-VARIANT-TOKEN-PARSER-COVERAGE-FIXUP
- P3-BETA-MVP-LENS-BOUNDARY-CONFLICT-RESOLUTION-FIXUP
