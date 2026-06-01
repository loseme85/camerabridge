# P3-THIRD-PARTY-SOURCE-COVERAGE-IMPLEMENTATION

## 1. 작업명
- P3-THIRD-PARTY-SOURCE-COVERAGE-IMPLEMENTATION

## 2. 작업 목적
- Sigma 14-24 source-gap alias variants에도 same no-result alert/signup metadata를 source-neutral하게 확장

## 3. 구현 요약
- `search_ui_hints.py`에서 Sigma 14-24 source-gap alias matcher를 확장
- results가 비어 있을 때만 `source_coverage_gap / no_result_alert_signup`를 반환
- ranking / result order / filtering은 변경하지 않음

## 4. 수정 파일 목록
- `search_ui_hints.py`
- `tests/test_third_party_source_coverage_implementation.py`
- `scripts/run_p3_third_party_source_coverage_implementation.py`
- `data/admin/p3_third_party_source_coverage_implementation_v0.md`
- `data/admin/p3_third_party_source_coverage_implementation_v0.jsonl`

## 5. 수정하지 않은 파일/영역
- `classifier_v2.py`
- `model_detector.py`
- `query_parser.py`
- `query_resolver.py`
- `search_service.py`
- `api/search.py`
- output JSON / taxonomy seed / canonical index / raw data / search index

## 6. response metadata 변경 요약
- canonical 4종뿐 아니라 Korean / l-mount / l마운트 / f2.8 / art variants도 no-result source gap hints를 받음

## 7. canonical Sigma 14-24 query 결과
- `sigma 14-24 l` -> count=`0` / hint=`source_coverage_gap`:`no_result_alert_signup` / status=`pass`
- `sigma 14-24 l mount` -> count=`0` / hint=`source_coverage_gap`:`no_result_alert_signup` / status=`pass`
- `sigma 14-24 dg dn` -> count=`0` / hint=`source_coverage_gap`:`no_result_alert_signup` / status=`pass`
- `sigma 14-24 dg dn art` -> count=`0` / hint=`source_coverage_gap`:`no_result_alert_signup` / status=`pass`

## 8. alias Sigma 14-24 query 결과
- `sigma 14-24 l-mount` -> count=`0` / hint=`source_coverage_gap`:`no_result_alert_signup` / status=`pass`
- `sigma 14-24 l마운트` -> count=`0` / hint=`source_coverage_gap`:`no_result_alert_signup` / status=`pass`
- `시그마 14-24 l` -> count=`0` / hint=`source_coverage_gap`:`no_result_alert_signup` / status=`pass`
- `시그마 14-24 l마운트` -> count=`0` / hint=`source_coverage_gap`:`no_result_alert_signup` / status=`pass`
- `시그마 14-24 dg dn` -> count=`0` / hint=`source_coverage_gap`:`no_result_alert_signup` / status=`pass`
- `시그마 14-24 아트` -> count=`0` / hint=`source_coverage_gap`:`no_result_alert_signup` / status=`pass`
- `sigma 14-24 art l mount` -> count=`0` / hint=`source_coverage_gap`:`no_result_alert_signup` / status=`pass`
- `sigma 14-24 f2.8 dg dn` -> count=`0` / hint=`source_coverage_gap`:`no_result_alert_signup` / status=`pass`
- `sigma 14-24 f2.8 l` -> count=`0` / hint=`source_coverage_gap`:`no_result_alert_signup` / status=`pass`

## 9. fake fill 방지 확인
- fake_fill_detected rows: `0`

## 10. overreach 방지 확인
- `sigma 24-70 l` -> `none` / top1=`Lens`:`[중고] Sigma 24-70/2.8 (SL 마운트)` / status=`guardrail_pass`
- `sigma 24-70 dg dn` -> `none` / top1=`Lens`:`[중고] Sigma 24-70/2.8 (SL 마운트)` / status=`guardrail_pass`
- `sigma l 30mm` -> `none` / top1=`Lens`:`Sigma L 30mm f1.4 DC DN Black for CL, TL2, etc` / status=`guardrail_pass`
- `sigma 30mm l` -> `none` / top1=`Lens`:`Sigma L 30mm f1.4 DC DN Black for CL, TL2, etc` / status=`guardrail_pass`
- `panasonic 24-105 l` -> `none` / top1=`Lens`:`[중고] 파나소닉 24-105 L 마운트` / status=`guardrail_pass`
- `lumix 24-105` -> `none` / top1=`Lens`:`[중고] 파나소닉 24-105 L 마운트` / status=`guardrail_pass`
- `sigma 14mm l` -> `none` / top1=`Lens`:`Laowa M 14mm f4 FF II Silver` / status=`guardrail_pass`
- `sigma 24mm l` -> `none` / top1=`Lens`:`Leica R 24mm f2.8 Elmarit Black` / status=`guardrail_pass`
- `sigma 14-24 canon` -> `none` / top1=``:`` / status=`guardrail_pass`
- `sigma 14-24 nikon` -> `none` / top1=``:`` / status=`guardrail_pass`

## 11. positive third-party guardrail 결과
- `sigma 24-70 l` -> `Lens` / `3rd Party` / `SL` / status=`guardrail_pass`
- `sigma 24-70 dg dn` -> `Lens` / `3rd Party` / `SL` / status=`guardrail_pass`
- `sigma l 30mm` -> `Lens` / `3rd Party` / `SL` / status=`guardrail_pass`
- `sigma 30mm l` -> `Lens` / `3rd Party` / `SL` / status=`guardrail_pass`
- `panasonic 24-105 l` -> `Lens` / `3rd Party` / `SL` / status=`guardrail_pass`
- `lumix 24-105` -> `Lens` / `3rd Party` / `SL` / status=`guardrail_pass`

## 12. Leica SL guardrail 결과
- `sl 14-24` -> `Lens` / `SL` / `Super-Vario-Elmarit-SL` / status=`guardrail_pass`
- `sl 24-90` -> `Lens` / `SL` / `Vario-Elmarit-SL` / status=`guardrail_pass`
- `sl 16-35` -> `Lens` / `SL` / `Super-Vario-Elmar-SL` / status=`guardrail_pass`
- `sl 90-280` -> `Lens` / `SL` / `APO-Vario-Elmarit-SL` / status=`guardrail_pass`
- `summicron sl 35` -> `Lens` / `SL` / `Summicron-SL` / status=`guardrail_pass`
- `sl 50 summicron` -> `Lens` / `SL` / `APO-Summicron` / status=`guardrail_pass`
- `leica sl2` -> `Body` / `SL` / `SL2` / status=`guardrail_pass`
- `leica sl3` -> `Body` / `SL` / `SL3` / status=`guardrail_pass`

## 13. accessory/body guardrail 결과
- `sl3 battery` -> `Accessory` / `[중고] Q3,SL3 배터리 (BP-SCL6)` / status=`guardrail_pass`
- `leica handgrip` -> `Accessory` / `Leica CL handgrip Black` / status=`guardrail_pass`
- `leica charger` -> `Accessory` / `[중고] Leica Q3 Drop XL Wireless Charger` / status=`guardrail_pass`
- `leica cap` -> `Accessory` / `[중고] Leitz Lens Cap E52.5` / status=`guardrail_pass`
- `leica filter` -> `Accessory` / `Leica E82 UVa II Black` / status=`guardrail_pass`
- `leica m strap` -> `Accessory` / `[중고] Leica M11 strap (Cognac)` / status=`guardrail_pass`
- `leica q2` -> `Body` / `Leica Q2 007 Edition` / status=`guardrail_pass`
- `leica m10 body` -> `Body` / `[위탁] M10 Monochrom 'Leitz Wetzlar' Edition` / status=`guardrail_pass`

## 14. broad ui_hints guardrail 결과
- `summicron` -> `broad_family_alias` / `refinement_chips` / status=`guardrail_pass`
- `summilux` -> `broad_family_alias` / `refinement_chips` / status=`guardrail_pass`
- `cron` -> `short_alias_bare` / `family_selector` / status=`guardrail_pass`
- `lux` -> `short_alias_bare` / `family_selector` / status=`guardrail_pass`
- `50 cron` -> `focal_short_alias` / `mount_selector` / status=`guardrail_pass`
- `leica r` -> `broad_mount_alias` / `family_selector` / status=`guardrail_pass`
- `r apo` -> `broad_mount_alias` / `family_selector` / status=`guardrail_pass`
- `leica cap` -> `broad_accessory_alias` / `accessory_subtype_selector` / status=`guardrail_pass`

## 15. fallback behavior
- `random unrelated query` -> `none` / `no_disambiguation_needed` / status=`fallback_pass`

## 16. output JSON / taxonomy seed / production ranking 미수정 여부
- output JSON 미수정
- taxonomy seed / canonical index 미수정
- production ranking / result order 미수정

## 17. 테스트 결과
- status counts: `{'pass': 13, 'guardrail_pass': 34, 'fallback_pass': 1}`

## 18. 남은 위험
- 현재 alias matcher는 Sigma 14-24 L/DG DN/Art source gap family에만 좁게 열려 있다.
- Canon/Nikon/other mount broad variants는 intentionally source gap으로 강제 분류하지 않는다.

## 19. 다음 backlog 후보
- `P3-THIRD-PARTY-SOURCE-SELECTOR-AUDIT`
- `P3-DIVERSITY-AWARE-RANKING`
- `P3-ACCESSORY-SUBTYPE-PRECISION`
- `P3-R-LENS-TAXONOMY-AUDIT`
- `P3-SL-ZOOM-FAMILY-TAXONOMY-AUDIT`
