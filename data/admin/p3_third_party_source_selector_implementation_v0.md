# P3-THIRD-PARTY-SOURCE-SELECTOR-IMPLEMENTATION

## 1. 작업명
- P3-THIRD-PARTY-SOURCE-SELECTOR-IMPLEMENTATION

## 2. 작업 목적
- live crawl이나 crawler production code 수정 없이, source-neutral capability contract와 source capability matrix를 구현

## 3. 구현 요약
- `source_coverage_contract.py`를 추가해 token family / enum / source capability builder를 순수 모듈로 분리
- `scripts/run_p3_third_party_source_selector_implementation.py`가 raw / normalized / search index / crawl log를 read-only로 읽어 matrix와 report를 생성
- ranking, parser, resolver, ui_hints production behavior는 변경하지 않음

## 4. source-neutral contract 요약
- source_type enum: ['leica_specialized_dealer', 'used_camera_dealer', 'marketplace', 'unknown']
- selector_scope enum: ['category_page', 'search_page', 'brand_page', 'keyword_seed', 'unknown']
- suspected_gap enum: ['none', 'true_source_inventory_absent', 'selector_miss_possible', 'source_list_gap_possible', 'keyword_filter_gap_possible', 'pagination_gap_possible', 'status_page_gap_possible', 'insufficient_evidence']
- brand tokens: {'sigma': ('sigma', '시그마'), 'panasonic': ('panasonic', '파나소닉'), 'lumix': ('lumix', '루믹스')}
- L-mount tokens: ['l mount', 'l-mount', 'l마운트', 'sl 마운트', 'sl mount', 'l 마운트']
- third-party family tokens: ['dg dn', 'dgdn', 'art', '아트', 'contemporary', 's pro']
- wide zoom tokens: ['14-24', '16-28', '17-28', '20-60', '24-70', '28-70', '28-105']

## 5. source capability matrix 요약
- source status 분포: {'selector_followup_needed': 4, 'source_list_followup_needed': 1, 'insufficient_evidence': 1}
- source suspected_gap 분포: {'selector_miss_possible': 4, 'source_list_gap_possible': 1, 'insufficient_evidence': 1}
- `장씨카메라` -> type=`unknown`, scope=`category_page`, third_party_l_mount_hits=1, sigma_hits=1, panasonic_lumix_hits=0, dg_dn_hits=0, art_hits=1, wide_zoom_hits=0, has_sigma_24_70=False, has_sigma_30mm=False, has_panasonic_24_105=False, has_sigma_14_24=False, suspected_gap=selector_miss_possible, status=selector_followup_needed
- `라이카스토어 충무로` -> type=`leica_specialized_dealer`, scope=`category_page`, third_party_l_mount_hits=21, sigma_hits=24, panasonic_lumix_hits=3, dg_dn_hits=6, art_hits=2, wide_zoom_hits=7, has_sigma_24_70=True, has_sigma_30mm=False, has_panasonic_24_105=True, has_sigma_14_24=False, suspected_gap=selector_miss_possible, status=selector_followup_needed
- `사진집` -> type=`unknown`, scope=`category_page`, third_party_l_mount_hits=3, sigma_hits=3, panasonic_lumix_hits=1, dg_dn_hits=0, art_hits=0, wide_zoom_hits=0, has_sigma_24_70=False, has_sigma_30mm=True, has_panasonic_24_105=False, has_sigma_14_24=False, suspected_gap=selector_miss_possible, status=selector_followup_needed
- `Ffordes (영국)` -> type=`unknown`, scope=`category_page`, third_party_l_mount_hits=11, sigma_hits=10, panasonic_lumix_hits=6, dg_dn_hits=7, art_hits=2, wide_zoom_hits=1, has_sigma_24_70=False, has_sigma_30mm=False, has_panasonic_24_105=False, has_sigma_14_24=False, suspected_gap=selector_miss_possible, status=selector_followup_needed
- `Leica Store Miami` -> type=`leica_specialized_dealer`, scope=`category_page`, third_party_l_mount_hits=0, sigma_hits=0, panasonic_lumix_hits=0, dg_dn_hits=0, art_hits=0, wide_zoom_hits=0, has_sigma_24_70=False, has_sigma_30mm=False, has_panasonic_24_105=False, has_sigma_14_24=False, suspected_gap=source_list_gap_possible, status=source_list_followup_needed
- `기타무라 (일본)` -> type=`unknown`, scope=`category_page`, third_party_l_mount_hits=0, sigma_hits=0, panasonic_lumix_hits=0, dg_dn_hits=0, art_hits=0, wide_zoom_hits=0, has_sigma_24_70=False, has_sigma_30mm=False, has_panasonic_24_105=False, has_sigma_14_24=False, suspected_gap=insufficient_evidence, status=insufficient_evidence

## 6. target Sigma 14-24 결과
- `sigma 14-24 l` -> result_count=0, ui_hints=source_coverage_gap/no_result_alert_signup, status=source_gap_confirmed
- `sigma 14-24 l mount` -> result_count=0, ui_hints=source_coverage_gap/no_result_alert_signup, status=source_gap_confirmed
- `sigma 14-24 l-mount` -> result_count=0, ui_hints=source_coverage_gap/no_result_alert_signup, status=source_gap_confirmed
- `sigma 14-24 l마운트` -> result_count=0, ui_hints=source_coverage_gap/no_result_alert_signup, status=source_gap_confirmed
- `sigma 14-24 dg dn` -> result_count=0, ui_hints=source_coverage_gap/no_result_alert_signup, status=source_gap_confirmed
- `sigma 14-24 dg dn art` -> result_count=0, ui_hints=source_coverage_gap/no_result_alert_signup, status=source_gap_confirmed
- `sigma 14-24 art l mount` -> result_count=0, ui_hints=source_coverage_gap/no_result_alert_signup, status=source_gap_confirmed
- `sigma 14-24 f2.8 dg dn` -> result_count=0, ui_hints=source_coverage_gap/no_result_alert_signup, status=source_gap_confirmed
- `sigma 14-24 f2.8 l` -> result_count=0, ui_hints=source_coverage_gap/no_result_alert_signup, status=source_gap_confirmed
- `시그마 14-24 l` -> result_count=0, ui_hints=source_coverage_gap/no_result_alert_signup, status=source_gap_confirmed
- `시그마 14-24 l마운트` -> result_count=0, ui_hints=source_coverage_gap/no_result_alert_signup, status=source_gap_confirmed
- `시그마 14-24 dg dn` -> result_count=0, ui_hints=source_coverage_gap/no_result_alert_signup, status=source_gap_confirmed
- `시그마 14-24 아트` -> result_count=0, ui_hints=source_coverage_gap/no_result_alert_signup, status=source_gap_confirmed
- `sigma 24-70 l` -> result_count=3, ui_hints=none/no_disambiguation_needed, status=pass
- `sigma 24-70 l mount` -> result_count=3, ui_hints=none/no_disambiguation_needed, status=pass
- `sigma 24-70 dg dn` -> result_count=3, ui_hints=none/no_disambiguation_needed, status=pass
- `sigma 24-70 dg dn art` -> result_count=3, ui_hints=none/no_disambiguation_needed, status=pass
- `sigma l 30mm` -> result_count=3, ui_hints=none/no_disambiguation_needed, status=pass
- `sigma 30mm l` -> result_count=3, ui_hints=none/no_disambiguation_needed, status=pass
- `panasonic 24-105 l` -> result_count=1, ui_hints=none/no_disambiguation_needed, status=pass
- `lumix 24-105` -> result_count=1, ui_hints=none/no_disambiguation_needed, status=pass
- `panasonic lumix 24-105` -> result_count=1, ui_hints=none/no_disambiguation_needed, status=pass
- `lumix s 24-105` -> result_count=1, ui_hints=none/no_disambiguation_needed, status=pass
- `lumix 24-105 f4` -> result_count=1, ui_hints=none/no_disambiguation_needed, status=pass

## 7. positive third-party comparison 결과
- `sigma 24-70 l` -> `[중고] Sigma 24-70/2.8 (SL 마운트)` / brand=3rd Party / mount=SL / source=라이카스토어 충무로 / status=pass
- `sigma 24-70 l mount` -> `[중고] Sigma 24-70/2.8 (SL 마운트)` / brand=3rd Party / mount=SL / source=라이카스토어 충무로 / status=pass
- `sigma 24-70 dg dn` -> `[중고] Sigma 24-70/2.8 (SL 마운트)` / brand=3rd Party / mount=SL / source=라이카스토어 충무로 / status=pass
- `sigma 24-70 dg dn art` -> `[중고] Sigma 24-70/2.8 (SL 마운트)` / brand=3rd Party / mount=SL / source=라이카스토어 충무로 / status=pass
- `sigma l 30mm` -> `Sigma L 30mm f1.4 DC DN Black for CL, TL2, etc` / brand=3rd Party / mount=SL / source=사진집 / status=pass
- `sigma 30mm l` -> `Sigma L 30mm f1.4 DC DN Black for CL, TL2, etc` / brand=3rd Party / mount=SL / source=사진집 / status=pass
- `panasonic 24-105 l` -> `[중고] 파나소닉 24-105 L 마운트` / brand=3rd Party / mount=SL / source=라이카스토어 충무로 / status=pass
- `lumix 24-105` -> `[중고] 파나소닉 24-105 L 마운트` / brand=3rd Party / mount=SL / source=라이카스토어 충무로 / status=pass
- `panasonic lumix 24-105` -> `[중고] 파나소닉 24-105 L 마운트` / brand=3rd Party / mount=SL / source=라이카스토어 충무로 / status=pass
- `lumix s 24-105` -> `[중고] 파나소닉 24-105 L 마운트` / brand=3rd Party / mount=SL / source=라이카스토어 충무로 / status=pass
- `lumix 24-105 f4` -> `[중고] 파나소닉 24-105 L 마운트` / brand=3rd Party / mount=SL / source=라이카스토어 충무로 / status=pass

## 8. source별 capability summary
- `Sigma 24-70` source example -> source=`라이카스토어 충무로`, title=`[중고] Sigma 24-70/2.8 (SL 마운트)`, brand=`3rd Party`, mount=`SL`
- `Sigma 30mm` source example -> source=`사진집`, title=`Sigma L 30mm f1.4 DC DN Black for CL, TL2, etc`, brand=`3rd Party`, mount=`SL`
- `Panasonic/Lumix 24-105` source example -> source=`라이카스토어 충무로`, title=`[중고] 파나소닉 24-105 L 마운트`, brand=`Unknown`, mount=`SL`

## 9. suspected gap 분류
- dataset-level direct Sigma 14-24 inventory는 current raw / normalized / search index / archived raw에서 계속 0
- positive third-party L-mount signals가 있는 source는 `selector_miss_possible`로, third-party signal이 거의 없는 Leica-specialized source는 `source_list_gap_possible` 또는 `insufficient_evidence`로 보수적으로 분류

## 10. overreach/fake fill 방지 확인
- Sigma 14-24 target queries는 전부 result_count=0 유지
- Canon/Nikon Sigma 14-24, Sigma 14mm, Sigma 24mm는 Sigma 14-24 L-mount gap intent로 오분류하지 않음
- positive Sigma 24-70 / Sigma 30mm / Panasonic 24-105는 source gap으로 떨어지지 않음

## 11. broad ui_hints guardrail 결과
- `summicron` -> `broad_family_alias` / `refinement_chips` / status=guardrail_pass
- `summilux` -> `broad_family_alias` / `refinement_chips` / status=guardrail_pass
- `cron` -> `short_alias_bare` / `family_selector` / status=guardrail_pass
- `lux` -> `short_alias_bare` / `family_selector` / status=guardrail_pass
- `50 cron` -> `focal_short_alias` / `mount_selector` / status=guardrail_pass
- `leica r` -> `broad_mount_alias` / `family_selector` / status=guardrail_pass
- `r apo` -> `broad_mount_alias` / `family_selector` / status=guardrail_pass
- `leica cap` -> `broad_accessory_alias` / `accessory_subtype_selector` / status=guardrail_pass

## 12. Leica SL guardrail 결과
- `sl 14-24` -> `[중고] SL 14-24/2.8 Vario Elmarit ASPH (Black)` / mount=SL / status=guardrail_pass
- `sl 24-90` -> `Leica SL 24-90mm f2.8-4 Vario-Elmarit Black` / mount=SL / status=guardrail_pass
- `sl 16-35` -> `[중고] SL 16-35/3.5-4.5 Super Vario Elmar ASPH (Black)` / mount=SL / status=guardrail_pass
- `sl 90-280` -> `[중고] SL APO Vario Elmarit 90-280 f/2.8-4` / mount=SL / status=guardrail_pass
- `summicron sl 35` -> `신품 Leica SL 35mm f2 Summicron ASPH Black` / mount=SL / status=guardrail_pass
- `sl 50 summicron` -> `Leica SL 50mm f2 APO-Summicron ASPH Black` / mount=SL / status=guardrail_pass
- `leica sl2` -> `Leica SL2 Black` / mount=SL / status=guardrail_pass
- `leica sl3` -> `Leica SL3 Black` / mount=SL / status=guardrail_pass

## 13. 수정 파일 목록
- `source_coverage_contract.py`
- `scripts/run_p3_third_party_source_selector_implementation.py`
- `tests/test_third_party_source_selector_implementation.py`
- `data/admin/p3_third_party_source_selector_implementation_v0.md`
- `data/admin/p3_third_party_source_selector_implementation_v0.jsonl`
- `data/admin/source_capability_matrix_v0.json`

## 14. 수정하지 않은 파일/영역
- `classifier_v2.py`
- `model_detector.py`
- `query_parser.py`
- `query_resolver.py`
- `search_service.py`
- `search_ui_hints.py`
- `api/search.py`
- crawler selector production code
- output JSON / taxonomy seed / canonical index / raw data / search index

## 15. output JSON / taxonomy seed / raw/search index 미수정 여부
- 미수정

## 16. 테스트 결과
- script/test execution results are recorded after validation

## 17. 남은 위험
- local snapshot에는 crawler implementation이 없어 selector_scope는 source-specific trace가 아니라 global crawl-log inference 수준임
- `selector_miss_possible`는 positive signals 기반의 보수적 추정이며, live crawl 없이 확정 claim은 아님

## 18. 다음 backlog 후보
- `P3-THIRD-PARTY-SOURCE-LIST-EXPANSION`
- `P3-THIRD-PARTY-SOURCE-CAPABILITY-DASHBOARD`
- `P3-DIVERSITY-AWARE-RANKING`
- `P3-ACCESSORY-SUBTYPE-PRECISION`
- `P3-R-LENS-TAXONOMY-AUDIT`
- `P3-SL-ZOOM-FAMILY-TAXONOMY-AUDIT`

## Appendix
- contract checks: 8
- coverage scans: 13
- source rows: 6
