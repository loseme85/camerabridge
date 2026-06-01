# P3-THIRD-PARTY-SOURCE-SELECTOR-AUDIT

## 1. 작업명
- P3-THIRD-PARTY-SOURCE-SELECTOR-AUDIT

## 2. 작업 목적
- Sigma 14-24 L/DG DN/Art family가 현재 raw snapshot에 없는 이유를 source / crawler selector 관점에서 read-only로 분리

## 3. 실행 entrypoint
- `api.search.endpoint_response`
- `api.search.search_from_params`
- `search_service.load_and_search`

## 4. 조사한 파일/경로
- `/Users/changdaepark/Desktop/LEICA SEARCH/data/raw/results.json`
- `/Users/changdaepark/Desktop/LEICA SEARCH/data/normalized/normalized_latest.json`
- `/Users/changdaepark/Desktop/LEICA SEARCH/data/derived/results_search_index_v1.json`
- `/Users/changdaepark/Desktop/LEICA SEARCH/final_resolution_pipeline.py`
- `/Users/changdaepark/Desktop/LEICA SEARCH/scripts/regenerate_outputs_from_raw.py`
- `/Users/changdaepark/Desktop/LEICA SEARCH/api/search.py`
- `/Users/changdaepark/Desktop/LEICA SEARCH/crawler/logs/crawl_log.txt`
- `/Users/changdaepark/Desktop/LEICA SEARCH/crawler/sessions/crawl_sessions.json`
- `/Users/changdaepark/Desktop/LEICA SEARCH/crawl_sessions.json`
- archived raw snapshots: `/Users/changdaepark/Desktop/LEICA SEARCH/data/raw/raw_*.json`

## 5. source/crawler 구조 요약
- 이 workspace snapshot 안에서는 crawler adapter/source selector implementation 자체는 노출되지 않고, downstream artifacts와 session/log 위주로 남아 있음
- 확인된 local crawl artifacts는 `crawler/logs/crawl_log.txt`, `crawler/sessions/crawl_sessions.json`, top-level `crawl_sessions.json`
- raw -> normalized -> search index bridge는 `final_resolution_pipeline.py` / `scripts/regenerate_outputs_from_raw.py` 경로로 확인됨
- crawl log 기준 현재 visible selector scope는 적어도 일부 source에서 `category_page` 중심으로 보임

## 6. target Sigma 14-24 query 결과
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

## 7. coverage scan 결과
- `sigma 14-24`: raw=0, normalized=0, index=0 -> direct sigma 14-24 family absent across current raw / normalized / search index; archived raw snapshots also show zero direct hits
- `시그마 14-24`: raw=0, normalized=0, index=0 -> direct sigma 14-24 family absent across current raw / normalized / search index; archived raw snapshots also show zero direct hits
- `14-24`: raw=4, normalized=7, index=3 -> generic 14-24 exists, but current hits are Leica-side rather than Sigma 14-24
- `dg dn`: raw=13, normalized=13, index=13 -> third-party L-mount related tokens exist, so the gap is not global third-party L-mount absence
- `art`: raw=5, normalized=5, index=5 -> third-party L-mount related tokens exist, so the gap is not global third-party L-mount absence
- `아트`: raw=5, normalized=5, index=5 -> third-party L-mount related tokens exist, so the gap is not global third-party L-mount absence
- `l mount`: raw=12, normalized=42, index=12 -> third-party L-mount related tokens exist, so the gap is not global third-party L-mount absence
- `l-mount`: raw=12, normalized=42, index=12 -> third-party L-mount related tokens exist, so the gap is not global third-party L-mount absence
- `l마운트`: raw=12, normalized=42, index=12 -> third-party L-mount related tokens exist, so the gap is not global third-party L-mount absence
- `sl 마운트`: raw=8, normalized=8, index=8 -> third-party L-mount related tokens exist, so the gap is not global third-party L-mount absence
- `wide zoom`: raw=0, normalized=0, index=0 -> no direct signal in current snapshot
- `광각 줌`: raw=0, normalized=0, index=0 -> no direct signal in current snapshot
- `2.8`: raw=2, normalized=2, index=395 -> keyword appears in current snapshot

## 8. positive third-party comparison 결과
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

## 9. positive source examples
- `Sigma 24-70mm f/2.8 DG DN Art L-mount` -> source=`라이카스토어 충무로`, title=`[중고] Sigma 24-70/2.8 (SL 마운트)`, brand=`3rd Party`, mount=`SL`, price=`950,000원`, status=`sold_confirmed`
- `Sigma 30mm f/1.4 DC DN L-mount` -> source=`사진집`, title=`Sigma L 30mm f1.4 DC DN Black for CL, TL2, etc`, brand=`3rd Party`, mount=`SL`, price=`350,000원`, status=`asking`
- `Panasonic Lumix S 24-105mm f/4 L-mount` -> source=`라이카스토어 충무로`, title=`[중고] 파나소닉 24-105 L 마운트`, brand=`Unknown`, mount=`SL`, price=`980,000원`, status=`sold_confirmed`

## 10. source별 audit summary
- `장씨카메라` (used camera dealer) -> third_party_l_mount_hits=1, sigma_hits=1, panasonic_lumix_hits=0, has_sigma_24_70=False, has_sigma_30mm=False, has_panasonic_24_105=False, has_sigma_14_24=False, selector_scope=category_page, suspected_gap=selector_miss_possible, status=selector_audit_needed
- `라이카스토어 충무로` (Leica-specialized dealer) -> third_party_l_mount_hits=21, sigma_hits=24, panasonic_lumix_hits=3, has_sigma_24_70=True, has_sigma_30mm=False, has_panasonic_24_105=True, has_sigma_14_24=False, selector_scope=category_page, suspected_gap=selector_miss_possible, status=selector_audit_needed
- `사진집` (used camera dealer) -> third_party_l_mount_hits=3, sigma_hits=3, panasonic_lumix_hits=1, has_sigma_24_70=False, has_sigma_30mm=True, has_panasonic_24_105=False, has_sigma_14_24=False, selector_scope=category_page, suspected_gap=selector_miss_possible, status=selector_audit_needed
- `Ffordes (영국)` (used camera dealer) -> third_party_l_mount_hits=12, sigma_hits=10, panasonic_lumix_hits=6, has_sigma_24_70=False, has_sigma_30mm=False, has_panasonic_24_105=False, has_sigma_14_24=False, selector_scope=unknown, suspected_gap=selector_miss_possible, status=selector_audit_needed
- `Leica Store Miami` (Leica-specialized dealer) -> third_party_l_mount_hits=0, sigma_hits=0, panasonic_lumix_hits=0, has_sigma_24_70=False, has_sigma_30mm=False, has_panasonic_24_105=False, has_sigma_14_24=False, selector_scope=unknown, suspected_gap=source_list_gap_possible, status=source_list_followup_needed
- `기타무라 (일본)` (used camera dealer) -> third_party_l_mount_hits=0, sigma_hits=0, panasonic_lumix_hits=0, has_sigma_24_70=False, has_sigma_30mm=False, has_panasonic_24_105=False, has_sigma_14_24=False, selector_scope=unknown, suspected_gap=none, status=observation_only

## 11. suspected gap 분류
- source audit status 분포: {'source_gap_confirmed': 13, 'pass': 11, 'guardrail_pass': 24, 'selector_audit_needed': 4, 'source_list_followup_needed': 1, 'observation_only': 1}
- source suspected_gap 분포: {'selector_miss_possible': 4, 'source_list_gap_possible': 1, 'none': 1}
- current snapshot + normalized + search index + archived raw 관점에서는 `Sigma 14-24` direct inventory absence가 가장 강하게 확인됨
- 다만 third-party L-mount positives가 이미 들어오는 source가 있고 local crawl log가 category-page 중심이라, wide zoom / DG DN Art coverage에 대한 `selector_miss_possible`도 배제할 수 없음
- current source set이 Leica-specialized dealer 비중이 높은 편이라 `source_list_gap_possible`도 후속 후보로 남음

## 12. fake fill 방지 확인
- target Sigma 14-24 queries는 전부 result_count=0 유지
- Leica SL 14-24 / Sigma 24-70 / Sigma 30mm로 채워지는 케이스 없음

## 13. broad ui_hints guardrail 결과
- `summicron` -> `broad_family_alias` / `refinement_chips` / status=guardrail_pass
- `summilux` -> `broad_family_alias` / `refinement_chips` / status=guardrail_pass
- `cron` -> `short_alias_bare` / `family_selector` / status=guardrail_pass
- `lux` -> `short_alias_bare` / `family_selector` / status=guardrail_pass
- `50 cron` -> `focal_short_alias` / `mount_selector` / status=guardrail_pass
- `leica r` -> `broad_mount_alias` / `family_selector` / status=guardrail_pass
- `r apo` -> `broad_mount_alias` / `family_selector` / status=guardrail_pass
- `leica cap` -> `broad_accessory_alias` / `accessory_subtype_selector` / status=guardrail_pass

## 14. Leica SL guardrail 결과
- `sl 14-24` -> `[중고] SL 14-24/2.8 Vario Elmarit ASPH (Black)` / mount=SL / status=guardrail_pass
- `sl 24-90` -> `Leica SL 24-90mm f2.8-4 Vario-Elmarit Black` / mount=SL / status=guardrail_pass
- `sl 16-35` -> `[중고] SL 16-35/3.5-4.5 Super Vario Elmar ASPH (Black)` / mount=SL / status=guardrail_pass
- `sl 90-280` -> `[중고] SL APO Vario Elmarit 90-280 f/2.8-4` / mount=SL / status=guardrail_pass
- `summicron sl 35` -> `신품 Leica SL 35mm f2 Summicron ASPH Black` / mount=SL / status=guardrail_pass
- `sl 50 summicron` -> `Leica SL 50mm f2 APO-Summicron ASPH Black` / mount=SL / status=guardrail_pass
- `leica sl2` -> `Leica SL2 Black` / mount=SL / status=guardrail_pass
- `leica sl3` -> `Leica SL3 Black` / mount=SL / status=guardrail_pass

## 15. output JSON / taxonomy seed / production code 미수정 여부
- production code 수정 없음
- crawler selector 수정 없음
- output JSON / taxonomy seed / canonical index / raw data / search index write 없음

## 16. 테스트 결과
- 이 스크립트 실행 후 별도 regression/test block에서 검증

## 17. source-neutral follow-up proposal
- `P3-THIRD-PARTY-SOURCE-SELECTOR-IMPLEMENTATION`: site-specific 예외 없이 third-party L-mount wide zoom category/search coverage를 source adapter contract 기준으로 점검
- `P3-THIRD-PARTY-SOURCE-LIST-EXPANSION`: Leica-specialized dealer 중심 source mix를 broader used-camera / L-mount inventory source로 확장 검토
- category-page only ingestion이 보이는 source는 wide zoom / DG DN Art naming coverage 점검
- keyword seed hard-code보다 source adapter capability matrix와 audit checklist를 먼저 정리

## 18. 다음 backlog 후보
- `P3-THIRD-PARTY-SOURCE-SELECTOR-IMPLEMENTATION`
- `P3-THIRD-PARTY-SOURCE-LIST-EXPANSION`
- `P3-DIVERSITY-AWARE-RANKING`
- `P3-ACCESSORY-SUBTYPE-PRECISION`
- `P3-R-LENS-TAXONOMY-AUDIT`
- `P3-SL-ZOOM-FAMILY-TAXONOMY-AUDIT`

## Appendix
- archived raw snapshots scanned: `30` files
- archived direct Sigma 14-24 hits: `0`
- archived Sigma 14-24 samples: `[]`
