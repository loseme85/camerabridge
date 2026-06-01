# P3-ALERT-MVP-SIGNUP-FLOW

## 1. 작업명
- P3-ALERT-MVP-SIGNUP-FLOW

## 2. 작업 목적
- watchlist item status와 current search/no-result 상태를 연결해 MVP signup CTA policy와 payload preview contract를 정의

## 3. 구현 요약
- `alert_signup_contract.py`에 signup flow enum/dataclass를 추가
- script는 watchlist contract를 읽고 scenario query에 대해 CTA decision / payload preview / scenario validation artifact를 생성
- production search behavior와 runtime 저장소는 변경하지 않음

## 4. signup contract 요약
- entry_point: `['search_results_page', 'no_result_page', 'watchlist_detail', 'source_gap_page', 'refinement_page', 'admin_preview']`
- cta_type: `['alert_signup', 'source_gap_alert_signup', 'price_watch_signup', 'availability_watch_signup', 'refinement_required', 'source_expansion_waitlist', 'manual_review_unavailable', 'excluded_too_broad', 'unavailable_for_mvp']`
- eligibility: `['eligible', 'eligible_no_result', 'eligible_waitlist', 'needs_refinement', 'needs_manual_review', 'needs_source_expansion', 'excluded']`
- block_reason: `['too_broad_query', 'manual_review_required', 'source_expansion_required', 'taxonomy_audit_required', 'body_intent_not_launch_safe', 'missing_canonical_query', 'unsupported_watchlist_status', 'excluded_for_mvp', 'none']`

## 5. CTA policy 요약
- `include` -> cta=`alert_signup` / eligibility=`eligible` / block=`none`
- `include_as_source_gap_alert` -> cta=`source_gap_alert_signup` / eligibility=`eligible_no_result` / block=`none`
- `needs_source_expansion` -> cta=`source_expansion_waitlist` / eligibility=`eligible_waitlist` / block=`source_expansion_required`
- `needs_manual_review` -> cta=`manual_review_unavailable` / eligibility=`needs_manual_review` / block=`manual_review_required`
- `refinement_required` -> cta=`refinement_required` / eligibility=`needs_refinement` / block=`too_broad_query`
- `exclude_too_broad` -> cta=`excluded_too_broad` / eligibility=`excluded` / block=`too_broad_query`
- `exclude_for_mvp` -> cta=`unavailable_for_mvp` / eligibility=`excluded` / block=`excluded_for_mvp`

## 6. signup eligibility 요약
- decision count: `32`
- cta distribution: `{'alert_signup': 10, 'source_gap_alert_signup': 5, 'source_expansion_waitlist': 2, 'manual_review_unavailable': 4, 'excluded_too_broad': 5, 'refinement_required': 6}`
- eligibility distribution: `{'eligible': 10, 'eligible_no_result': 5, 'eligible_waitlist': 2, 'needs_manual_review': 4, 'excluded': 5, 'needs_refinement': 6}`

## 7. signup payload schema 요약
- payload preview count: `21`
- required payload fields include watchlist id, canonical query, user query, alert intent, trigger policy, source priority hint, CTA type, eligibility, and readiness flags

## 8. normal include signup 결과
- `summilux m 35` -> cta=`alert_signup` / eligibility=`eligible` / status=`pass`
- `35 lux aa` -> cta=`alert_signup` / eligibility=`eligible` / status=`pass`
- `summilux m 50` -> cta=`alert_signup` / eligibility=`eligible` / status=`pass`
- `noctilux m 50 0.95` -> cta=`alert_signup` / eligibility=`eligible` / status=`pass`
- `apo summicron m 90` -> cta=`alert_signup` / eligibility=`eligible` / status=`pass`
- `m6` -> cta=`alert_signup` / eligibility=`eligible` / status=`pass`
- `mp` -> cta=`alert_signup` / eligibility=`eligible` / status=`pass`
- `r 180 apo telyt` -> cta=`alert_signup` / eligibility=`eligible` / status=`pass`
- `sigma 24-70 l` -> cta=`alert_signup` / eligibility=`eligible` / status=`pass`
- `lumix 24-105` -> cta=`alert_signup` / eligibility=`eligible` / status=`pass`

## 9. source-gap no-result signup 결과
- `sigma 14-24 l` -> cta=`source_gap_alert_signup` / eligibility=`eligible_no_result` / fake_fill=`False` / status=`pass`
- `sigma 14-24 l mount` -> cta=`source_gap_alert_signup` / eligibility=`eligible_no_result` / fake_fill=`False` / status=`pass`
- `sigma 14-24 dg dn` -> cta=`source_gap_alert_signup` / eligibility=`eligible_no_result` / fake_fill=`False` / status=`pass`
- `시그마 14-24 l` -> cta=`source_gap_alert_signup` / eligibility=`eligible_no_result` / fake_fill=`False` / status=`pass`
- `시그마 14-24 아트` -> cta=`source_gap_alert_signup` / eligibility=`eligible_no_result` / fake_fill=`False` / status=`pass`

## 10. needs-source-expansion waitlist 결과
- `sigma 28-70 dg dn l` -> cta=`source_expansion_waitlist` / eligibility=`eligible_waitlist` / block=`source_expansion_required`
- `sigma 28-105 dg dn l` -> cta=`source_expansion_waitlist` / eligibility=`eligible_waitlist` / block=`source_expansion_required`

## 11. manual-review block 결과
- `leica m-a` -> cta=`manual_review_unavailable` / eligibility=`needs_manual_review` / block=`body_intent_not_launch_safe`
- `leica m10 monochrom` -> cta=`manual_review_unavailable` / eligibility=`needs_manual_review` / block=`body_intent_not_launch_safe`
- `leica m10-r` -> cta=`manual_review_unavailable` / eligibility=`needs_manual_review` / block=`body_intent_not_launch_safe`
- `leica m11 monochrom` -> cta=`manual_review_unavailable` / eligibility=`needs_manual_review` / block=`body_intent_not_launch_safe`

## 12. broad query refinement/exclusion 결과
- `summicron` -> cta=`excluded_too_broad` / eligibility=`excluded` / block=`too_broad_query`
- `summilux` -> cta=`excluded_too_broad` / eligibility=`excluded` / block=`too_broad_query`
- `cron` -> cta=`refinement_required` / eligibility=`needs_refinement` / block=`too_broad_query`
- `lux` -> cta=`refinement_required` / eligibility=`needs_refinement` / block=`too_broad_query`
- `50 cron` -> cta=`refinement_required` / eligibility=`needs_refinement` / block=`too_broad_query`
- `35 lux` -> cta=`refinement_required` / eligibility=`needs_refinement` / block=`too_broad_query`
- `leica r` -> cta=`refinement_required` / eligibility=`needs_refinement` / block=`too_broad_query`
- `leica cap` -> cta=`refinement_required` / eligibility=`needs_refinement` / block=`too_broad_query`
- `leica lens` -> cta=`excluded_too_broad` / eligibility=`excluded` / block=`too_broad_query`
- `leica m` -> cta=`excluded_too_broad` / eligibility=`excluded` / block=`too_broad_query`
- `leica sl` -> cta=`excluded_too_broad` / eligibility=`excluded` / block=`too_broad_query`

## 13. source priority hint 연결 요약
- `rare_leica_lens_summilux_m_35_asph` -> source_priority_hint=`['라이카스토어 충무로', 'Map Camera', 'Fujiya Camera', 'Lemonsha', 'Leica Store Miami', 'Ffordes', 'Red Dot Cameras', 'Meister Camera']`
- `rare_leica_lens_summilux_m_35_aa` -> source_priority_hint=`['라이카스토어 충무로', 'Map Camera', 'Fujiya Camera', 'Lemonsha', 'Leica Store Miami', 'Ffordes', 'Red Dot Cameras', 'Meister Camera']`
- `rare_leica_lens_summilux_m_50` -> source_priority_hint=`['라이카스토어 충무로', 'Map Camera', 'Fujiya Camera', 'Lemonsha', 'Leica Store Miami', 'Ffordes', 'Red Dot Cameras', 'Meister Camera']`
- `rare_leica_lens_noctilux_m_50_095` -> source_priority_hint=`['라이카스토어 충무로', 'Map Camera', 'Fujiya Camera', 'Lemonsha', 'Leica Store Miami', 'Ffordes', 'Red Dot Cameras', 'Meister Camera']`
- `rare_leica_lens_apo_summicron_m_90` -> source_priority_hint=`['라이카스토어 충무로', 'Map Camera', 'Fujiya Camera', 'Lemonsha', 'Leica Store Miami', 'Ffordes', 'Red Dot Cameras', 'Meister Camera']`
- `rare_leica_body_m6` -> source_priority_hint=`['라이카스토어 충무로', 'Map Camera', 'Fujiya Camera', 'Lemonsha', 'Leica Store Miami', 'Ffordes', 'Red Dot Cameras', 'Meister Camera']`
- `rare_leica_body_mp` -> source_priority_hint=`['라이카스토어 충무로', 'Map Camera', 'Fujiya Camera', 'Lemonsha', 'Leica Store Miami', 'Ffordes', 'Red Dot Cameras', 'Meister Camera']`
- `leica_r_rare_apo_telyt_r_180_34` -> source_priority_hint=`['라이카스토어 충무로', 'Map Camera', 'Fujiya Camera', 'Lemonsha', 'Leica Store Miami', 'Ffordes', 'Red Dot Cameras', 'Meister Camera']`
- `third_party_l_mount_sigma_24_70_dg_dn_art` -> source_priority_hint=`['라이카스토어 충무로', '사진집', 'Map Camera', 'Kitamura', 'Fujiya Camera', 'Camera no Naniwa', 'KEH', 'MPB US']`
- `third_party_l_mount_lumix_s_24_105_f4` -> source_priority_hint=`['장씨카메라', '라이카스토어 충무로', '사진집', 'Ffordes (영국)', 'Map Camera', 'Kitamura']`
- `third_party_l_mount_sigma_14_24_dg_dn_art` -> source_priority_hint=`['Map Camera', 'Fujiya Camera', 'KEH', 'MPB US', 'MPB UK/EU']`
- `third_party_l_mount_sigma_14_24_dg_dn_art` -> source_priority_hint=`['Map Camera', 'Fujiya Camera', 'KEH', 'MPB US', 'MPB UK/EU']`
- `third_party_l_mount_sigma_14_24_dg_dn_art` -> source_priority_hint=`['Map Camera', 'Fujiya Camera', 'KEH', 'MPB US', 'MPB UK/EU']`
- `third_party_l_mount_sigma_14_24_dg_dn_art` -> source_priority_hint=`['Map Camera', 'Fujiya Camera', 'KEH', 'MPB US', 'MPB UK/EU']`
- `third_party_l_mount_sigma_14_24_dg_dn_art` -> source_priority_hint=`['Map Camera', 'Fujiya Camera', 'KEH', 'MPB US', 'MPB UK/EU']`
- `third_party_l_mount_sigma_28_70_dg_dn` -> source_priority_hint=`['Map Camera', 'Fujiya Camera', 'KEH', 'MPB US', 'MPB UK/EU']`

## 14. fake fill 방지 확인
- `sigma 14-24` source-gap scenario는 결과를 억지로 채우지 않고 `source_gap_alert_signup`으로만 연결해야 함
- source-gap scenarios with fake_fill_detected=true: `0`

## 15. 수정 파일 목록
- `alert_signup_contract.py`
- `scripts/run_p3_alert_mvp_signup_flow.py`
- `tests/test_alert_mvp_signup_flow.py`
- `data/admin/p3_alert_mvp_signup_flow_v0.md`
- `data/admin/p3_alert_mvp_signup_flow_v0.jsonl`
- `data/admin/alert_mvp_signup_flow_v0.json`

## 16. 수정하지 않은 파일/영역
- production search code
- crawler production code
- output JSON / taxonomy seed / canonical index / raw data / search index

## 17. 테스트 결과
- script run / JSONL validation / signup flow JSON validation / py_compile / golden set recorded separately

## 18. 남은 위험
- body manual-review items는 watchlist는 정의돼 있어도 launch-safe signup으로 열면 안 됨
- third-party L-mount 중 `28-70`, `28-105`는 source expansion 전까지 waitlist 이상으로 올리기 어려움
- broad query는 refinement UI contract가 실제 화면에 붙기 전까지 product UX가 다소 거칠 수 있음

## 19. 다음 backlog 후보
- `P3-ALERT-MVP-STORAGE-SCHEMA`
- `P3-ALERT-MVP-DELIVERY-SIMULATION`
- `P3-ALERT-MVP-EMAIL-VERIFICATION-CONTRACT`
- `P3-ALERT-MVP-NO-RESULT-UI-CONTRACT`
- `P3-THIRD-PARTY-SOURCE-LIST-EXPANSION-IMPLEMENTATION`
