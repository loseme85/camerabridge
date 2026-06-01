# P3-ALERT-MVP-NO-RESULT-UI-CONTRACT

## 작업 목적
- no-result / broad / manual-review / source-gap 상황에서 사용자에게 보여줄 empty-state와 CTA를 contract로 정의한다.

## 구현 요약
- source-gap은 alert signup, source-expansion은 waitlist, broad query는 refinement, manual-review는 blocked notice로 분리했다.
- 모든 preview에서 fake result 생성과 adjacent family substitution을 금지했다.

## No-Result State 분포
- broad_query_excluded: 5
- broad_query_refinement_required: 6
- manual_review_required: 4
- source_expansion_needed: 2
- source_gap_alertable: 3
- true_no_result: 2

## CTA 분포
- choose_mount_or_family: 8
- contact_or_feedback: 4
- join_source_expansion_waitlist: 2
- notify_when_source_gap_resolved: 3
- refine_query: 3
- view_related_searches: 2

## 수정 파일 목록
- alert_no_result_ui_contract.py
- scripts/run_p3_alert_mvp_no_result_ui_contract.py
- tests/test_alert_mvp_no_result_ui_contract.py
- data/admin/p3_alert_mvp_no_result_ui_contract_v0.md
- data/admin/p3_alert_mvp_no_result_ui_contract_v0.jsonl
- data/admin/alert_mvp_no_result_ui_contract_v0.json

## 수정하지 않은 파일/영역
- production search/parser/resolver/crawler code
- output JSON / taxonomy seed / canonical index / raw data / search index

## 다음 backlog 후보
- P3-ALERT-MVP-DELIVERY-QUEUE-SCHEMA
- P3-ALERT-MVP-EMAIL-PROVIDER-ADAPTER-CONTRACT
- P3-ALERT-MVP-PREFERENCE-CENTER-CONTRACT
- P3-ALERT-MVP-LANDING-PAGE-COPY-CONTRACT
- P3-THIRD-PARTY-SOURCE-LIST-EXPANSION-IMPLEMENTATION
