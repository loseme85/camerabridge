# P3-BETA-SHARE-LINK-RUNTIME-SERVER-ERROR-FIXUP

## 1. 작업명
- `P3-BETA-SHARE-LINK-RUNTIME-SERVER-ERROR-FIXUP`

## 2. 현재 판정
- `decision_status = beta_share_link_runtime_server_error_fixup_ready_for_owner_approved_commit_push_preview_recheck`

## 3. 목적
- preview triage에서 확인된 `/search` 404와 `/api/search` bootstrap/runtime 취약 지점을 최소 수정으로 보완

## 4. previous triage summary
- triage status = `beta_share_link_runtime_server_error_triage_completed_ready_for_fixup`
- search route issue = `true`
- api auth gate issue = `true`
- api runtime 500 issue = `true`

## 5. 수정한 파일
- `vercel.json`
- `api/search.py`
- `scripts/run_p3_beta_share_link_runtime_server_error_fixup.py`
- `tests/test_beta_share_link_runtime_server_error_fixup.py`
- `data/admin/p3_beta_share_link_runtime_server_error_fixup_v0.md`
- `data/admin/p3_beta_share_link_runtime_server_error_fixup_v0.jsonl`
- `data/admin/beta_share_link_runtime_server_error_fixup_v0.json`

## 6. /search route fix 내용
- `vercel.json`에 `/search` rewrite를 추가
- destination = `/app/templates/index.html`
- preview의 `/`와 동일한 beta landing/search surface로 연결되도록 준비

## 7. /api/search runtime fix 내용
- `api/search.py`의 search runtime imports를 lazy load로 이동
- `_resolve_search_index_path()` 추가로 runtime candidate path resolution 보강
- `search_runtime_bootstrap_failed` JSON error 경계 추가
- `search_handler_failed` ultra-last handler boundary 추가

## 8. data/index path check
- index path = `data/derived/results_search_index_v1.json`
- exists = `true`
- size bytes = `11811593`
- cwd only assumption removed = `true`

## 9. local route/API smoke 결과
- `/` -> `200` / `text/html; charset=utf-8` / raw_error=`false`
- `/search` -> `200` / `text/html; charset=utf-8` / raw_error=`false`
- `/api/search?q=summicron&limit=5` -> `200` / `application/json` / raw_error=`false`
- `/api/search?q=ltm%20summaron%2035&limit=5` -> `200` / `application/json` / raw_error=`false`
- `/api/search?q=ricoh%20gr%20iiix&limit=5` -> `200` / `application/json` / raw_error=`false`
- `/api/search?q=hasselblad%20xpan&limit=5` -> `200` / `application/json` / raw_error=`false`

## 10. raw server error 방지 확인
- raw server error absent locally = `true`

## 11. fake fill 방지 확인
- fake fill detected = `false`
- `ricoh gr iiix` total/result = `0` / `0`
- `hasselblad xpan` total/result = `0` / `0`

## 12. production/public/access guard
- production_launch_go = `false`
- public_unrestricted_access_enabled = `false`
- external_tester_access_enabled = `false`
- tester_link_send_allowed = `false`

## 13. 테스트 결과
- `python3 tests/test_beta_share_link_runtime_server_error_fixup.py` -> `passed` / ok (21 tests)
- `python3 scripts/run_p3_beta_share_link_runtime_server_error_fixup.py` -> `passed` / decision emitted
- `python3 tests/test_beta_landing_search_ui_reference_redesign_implementation.py` -> `passed` / ok (27 tests)
- `python3 tests/test_beta_share_link_runtime_smoke_recheck.py` -> `passed` / ok (22 tests)
- `python3 tests/test_beta_ui_preview_deployment_and_share_link_check.py` -> `passed` / ok (20 tests)
- `python3 golden_set.py` -> `passed` / 132/132

## 14. commit/push/deploy 필요 여부
- `commit_push_deploy_required = true`
- 이번 라운드에서는 실행하지 않았고, 다음 round에서 owner-approved preview recheck용으로 올려야 합니다.

## 15. tester link send 가능 여부
- `tester_link_send_allowed = false`
- preview 재배포와 share-link smoke recheck 전에는 여전히 금지입니다.

## 16. 다음 backlog 후보
- `P3-BETA-SHARE-LINK-RUNTIME-SERVER-ERROR-FIXUP-COMMIT-PUSH-AND-PREVIEW-RECHECK`
