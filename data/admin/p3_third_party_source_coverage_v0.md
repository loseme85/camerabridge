# P3-THIRD-PARTY-SOURCE-COVERAGE

## 1. 작업 목적
- third-party L-mount no-result가 parser/ranking miss가 아니라 실제 source coverage gap인지 pipeline 단위로 분리
- fake fill 없이 no-result + alert/signup 정책이 맞는지 확인

## 2. 실행 entrypoint
- `api.search.endpoint_response`
- `api.search.search_from_params`
- `search_service.load_and_search`
- `data/derived/results_search_index_v1.json`

## 3. 조사 범위
- checked_at: `2026-05-27`
- 총 query 수: `48`
- group counts: `{'target_source_gap': 13, 'positive_third_party_comparison': 11, 'leica_sl_guardrail': 8, 'accessory_body_guardrail': 8, 'broad_ui_guardrail': 8}`
- status counts: `{'source_coverage_gap': 4, 'needs_source_followup': 9, 'pass': 11, 'guardrail_pass': 24}`
- cause counts: `{'source_coverage_gap': 13, 'no_result_policy_ok': 27, 'ui_alert_policy_ok': 8}`

## 4. source/index/normalized/raw 확인 경로
- search index: `/Users/changdaepark/Desktop/LEICA SEARCH/data/derived/results_search_index_v1.json`
- normalized: `/Users/changdaepark/Desktop/LEICA SEARCH/data/normalized/normalized_latest.json`
- raw: `/Users/changdaepark/Desktop/LEICA SEARCH/data/raw/results.json`

## 5. target no-result query 결과
- `sigma 14-24 l` -> result_count=`0` / ui_hints=`source_coverage_gap`:`no_result_alert_signup` / status=`source_coverage_gap` / notes=coverage gap confirmed across search index / normalized / raw; ui alert policy attached
- `sigma 14-24 l mount` -> result_count=`0` / ui_hints=`source_coverage_gap`:`no_result_alert_signup` / status=`source_coverage_gap` / notes=coverage gap confirmed across search index / normalized / raw; ui alert policy attached
- `sigma 14-24 dg dn` -> result_count=`0` / ui_hints=`source_coverage_gap`:`no_result_alert_signup` / status=`source_coverage_gap` / notes=coverage gap confirmed across search index / normalized / raw; ui alert policy attached
- `sigma 14-24 dg dn art` -> result_count=`0` / ui_hints=`source_coverage_gap`:`no_result_alert_signup` / status=`source_coverage_gap` / notes=coverage gap confirmed across search index / normalized / raw; ui alert policy attached
- `sigma 14-24 l-mount` -> result_count=`0` / ui_hints=`none`:`no_disambiguation_needed` / status=`needs_source_followup` / notes=coverage gap confirmed across search index / normalized / raw; current ui alert policy does not yet cover this alias variant
- `sigma 14-24 l마운트` -> result_count=`0` / ui_hints=`none`:`no_disambiguation_needed` / status=`needs_source_followup` / notes=coverage gap confirmed across search index / normalized / raw; current ui alert policy does not yet cover this alias variant
- `시그마 14-24 l` -> result_count=`0` / ui_hints=`none`:`no_disambiguation_needed` / status=`needs_source_followup` / notes=coverage gap confirmed across search index / normalized / raw; current ui alert policy does not yet cover this alias variant
- `시그마 14-24 l마운트` -> result_count=`0` / ui_hints=`none`:`no_disambiguation_needed` / status=`needs_source_followup` / notes=coverage gap confirmed across search index / normalized / raw; current ui alert policy does not yet cover this alias variant
- `시그마 14-24 dg dn` -> result_count=`0` / ui_hints=`none`:`no_disambiguation_needed` / status=`needs_source_followup` / notes=coverage gap confirmed across search index / normalized / raw; current ui alert policy does not yet cover this alias variant
- `시그마 14-24 아트` -> result_count=`0` / ui_hints=`none`:`no_disambiguation_needed` / status=`needs_source_followup` / notes=coverage gap confirmed across search index / normalized / raw; current ui alert policy does not yet cover this alias variant
- `sigma 14-24 art l mount` -> result_count=`0` / ui_hints=`none`:`no_disambiguation_needed` / status=`needs_source_followup` / notes=coverage gap confirmed across search index / normalized / raw; current ui alert policy does not yet cover this alias variant
- `sigma 14-24 f2.8 dg dn` -> result_count=`0` / ui_hints=`none`:`no_disambiguation_needed` / status=`needs_source_followup` / notes=coverage gap confirmed across search index / normalized / raw; current ui alert policy does not yet cover this alias variant
- `sigma 14-24 f2.8 l` -> result_count=`0` / ui_hints=`none`:`no_disambiguation_needed` / status=`needs_source_followup` / notes=coverage gap confirmed across search index / normalized / raw; current ui alert policy does not yet cover this alias variant

## 6. positive comparison query 결과
- `sigma 24-70 l` -> `Lens` / `3rd Party` / `SL` / `[중고] Sigma 24-70/2.8 (SL 마운트)` / sites=['라이카스토어 충무로'] / status=`pass`
- `sigma 24-70 l mount` -> `Lens` / `3rd Party` / `SL` / `[중고] Sigma 24-70/2.8 (SL 마운트)` / sites=['라이카스토어 충무로'] / status=`pass`
- `sigma 24-70 dg dn` -> `Lens` / `3rd Party` / `SL` / `[중고] Sigma 24-70/2.8 (SL 마운트)` / sites=[] / status=`pass`
- `sigma 24-70 dg dn art` -> `Lens` / `3rd Party` / `SL` / `[중고] Sigma 24-70/2.8 (SL 마운트)` / sites=[] / status=`pass`
- `sigma l 30mm` -> `Lens` / `3rd Party` / `SL` / `Sigma L 30mm f1.4 DC DN Black for CL, TL2, etc` / sites=['사진집'] / status=`pass`
- `sigma 30mm l` -> `Lens` / `3rd Party` / `SL` / `Sigma L 30mm f1.4 DC DN Black for CL, TL2, etc` / sites=['사진집'] / status=`pass`
- `panasonic 24-105 l` -> `Lens` / `3rd Party` / `SL` / `[중고] 파나소닉 24-105 L 마운트` / sites=['라이카스토어 충무로'] / status=`pass`
- `lumix 24-105` -> `Lens` / `3rd Party` / `SL` / `[중고] 파나소닉 24-105 L 마운트` / sites=['라이카스토어 충무로'] / status=`pass`
- `panasonic lumix 24-105` -> `Lens` / `3rd Party` / `SL` / `[중고] 파나소닉 24-105 L 마운트` / sites=['라이카스토어 충무로'] / status=`pass`
- `lumix s 24-105` -> `Lens` / `3rd Party` / `SL` / `[중고] 파나소닉 24-105 L 마운트` / sites=[] / status=`pass`
- `lumix 24-105 f4` -> `Lens` / `3rd Party` / `SL` / `[중고] 파나소닉 24-105 L 마운트` / sites=[] / status=`pass`

## 7. Leica SL guardrail 결과
- `sl 14-24` -> `Lens` / `SL` / `Super-Vario-Elmarit-SL` / status=`guardrail_pass`
- `sl 24-90` -> `Lens` / `SL` / `Vario-Elmarit-SL` / status=`guardrail_pass`
- `sl 16-35` -> `Lens` / `SL` / `Super-Vario-Elmar-SL` / status=`guardrail_pass`
- `sl 90-280` -> `Lens` / `SL` / `APO-Vario-Elmarit-SL` / status=`guardrail_pass`
- `summicron sl 35` -> `Lens` / `SL` / `Summicron-SL` / status=`guardrail_pass`
- `sl 50 summicron` -> `Lens` / `SL` / `APO-Summicron` / status=`guardrail_pass`
- `leica sl2` -> `Body` / `SL` / `SL2` / status=`guardrail_pass`
- `leica sl3` -> `Body` / `SL` / `SL3` / status=`guardrail_pass`

## 8. accessory/body guardrail 결과
- `sl3 battery` -> `Accessory` / `[중고] Q3,SL3 배터리 (BP-SCL6)` / status=`guardrail_pass`
- `leica handgrip` -> `Accessory` / `Leica CL handgrip Black` / status=`guardrail_pass`
- `leica charger` -> `Accessory` / `[중고] Leica Q3 Drop XL Wireless Charger` / status=`guardrail_pass`
- `leica cap` -> `Accessory` / `[중고] Leitz Lens Cap E52.5` / status=`guardrail_pass`
- `leica filter` -> `Accessory` / `Leica E82 UVa II Black` / status=`guardrail_pass`
- `leica m strap` -> `Accessory` / `[중고] Leica M11 strap (Cognac)` / status=`guardrail_pass`
- `leica q2` -> `Body` / `Leica Q2 007 Edition` / status=`guardrail_pass`
- `leica m10 body` -> `Body` / `[위탁] M10 Monochrom 'Leitz Wetzlar' Edition` / status=`guardrail_pass`

## 9. broad query ui_hints guardrail 결과
- `summicron` -> `broad_family_alias` / `refinement_chips` / top1=`Lens`:`Leica L 50mm f2 Summicron Silver` / status=`guardrail_pass`
- `summilux` -> `broad_family_alias` / `refinement_chips` / top1=`Lens`:`[중고] L 50/1.4 Summilux 4세대 (Silver)` / status=`guardrail_pass`
- `cron` -> `short_alias_bare` / `family_selector` / top1=`Lens`:`Leica R 50mm f2 Summicron Black` / status=`guardrail_pass`
- `lux` -> `short_alias_bare` / `family_selector` / top1=`Lens`:`Leica M 28mm f1.4 Summilux ASPH 6bit Black` / status=`guardrail_pass`
- `50 cron` -> `focal_short_alias` / `mount_selector` / top1=`Lens`:`Leica R 50mm f2 Summicron Black` / status=`guardrail_pass`
- `leica r` -> `broad_mount_alias` / `family_selector` / top1=`Lens`:`Leica R 50mm f2 Summicron Black` / status=`guardrail_pass`
- `r apo` -> `broad_mount_alias` / `family_selector` / top1=`Lens`:`Leica R 50mm f2 Summicron Black` / status=`guardrail_pass`
- `leica cap` -> `broad_accessory_alias` / `accessory_subtype_selector` / top1=`Accessory`:`[중고] Leitz Lens Cap E52.5` / status=`guardrail_pass`

## 10. search index coverage 결과
- `sigma 14-24` -> search_index=`0` / sample=[]
- `시그마 14-24` -> search_index=`0` / sample=[]
- `14-24` -> search_index=`1` / sample=['[중고] SL 14-24/2.8 Vario Elmarit ASPH (Black)']
- `dg dn` -> search_index=`8` / sample=['[위탁] Sigma 28-105mm f/2.8 DG DN ART', '[중고] Sigma 24/1.4 DG DN Art']
- `art` -> search_index=`8` / sample=['Leica R 180mm f2.8 APO-Elmart Rom Black', 'Barton1972 Leather Neck Strap Whip Black Gray']
- `l mount` -> search_index=`8` / sample=['[중고] Sigma 35/1.4 DG DN (SL 마운트)', '[중고] Sigma 70/2.8 DG Macro (SL 마운트)']
- `l마운트` -> search_index=`8` / sample=['[중고] Sigma 35/1.4 DG DN (SL 마운트)', '[중고] Sigma 70/2.8 DG Macro (SL 마운트)']
- `sl 마운트` -> search_index=`5` / sample=['[중고] Sigma 35/1.4 DG DN (SL 마운트)', '[중고] Sigma 70/2.8 DG Macro (SL 마운트)']

## 11. normalized coverage 결과
- `sigma 14-24` -> normalized=`0`
- `시그마 14-24` -> normalized=`0`
- `14-24` -> normalized=`1`
- `dg dn` -> normalized=`8`
- `art` -> normalized=`8`
- `l mount` -> normalized=`8`
- `l마운트` -> normalized=`8`
- `sl 마운트` -> normalized=`5`

## 12. raw/source coverage 결과
- `sigma 14-24` -> raw=`0` / conclusion=sigma 14-24 family direct coverage
- `시그마 14-24` -> raw=`0` / conclusion=korean sigma 14-24 direct coverage
- `14-24` -> raw=`1` / conclusion=generic 14-24 coverage; may be Leica SL 14-24
- `dg dn` -> raw=`8` / conclusion=third-party dg dn coverage
- `art` -> raw=`8` / conclusion=art keyword is broad and noisy
- `l mount` -> raw=`8` / conclusion=third-party l-mount coverage
- `l마운트` -> raw=`8` / conclusion=korean l-mount alias coverage
- `sl 마운트` -> raw=`5` / conclusion=shop-side sl-mount phrasing coverage

## 13. 원인 분류
- canonical English `sigma 14-24` 4종은 `source_coverage_gap + ui_alert_policy_ok`
- extended alias variants (`l-mount`, `l마운트`, Korean sigma, f2.8/art variants)는 `source_coverage_gap` 자체는 같지만 current `ui_hints` contract가 아직 canonical 4종에만 붙음
- `sigma 24-70`, `sigma 30mm`, `panasonic/lumix 24-105`는 parser/ranking 문제가 아니라 실제 raw/index/source에 후보가 있는 comparison group

## 14. fake fill 방지 확인
- target no-result query 전부 result_count=0 유지
- `sigma 14-24`가 Leica SL 14-24나 Sigma 24-70/30mm로 채워지는 케이스 없음

## 15. no-result alert/signup UI 연결 여부
- exact supported queries:
  - `sigma 14-24 l`
  - `sigma 14-24 l mount`
  - `sigma 14-24 dg dn`
  - `sigma 14-24 dg dn art`
  -> `ui_hints.ambiguity_type = source_coverage_gap`, `recommended_ui_pattern = no_result_alert_signup`
- alias variants currently fall back to `none / no_disambiguation_needed`; this is a metadata coverage gap, not a ranking/source misclassification

## 16. source/crawler follow-up 후보
- current positive third-party hits are concentrated in sites such as `라이카스토어 충무로` and `사진집`
- source-side follow-up should inspect whether Sigma 14-24 L listings are absent from crawled source inventory or missed by site-specific crawler selectors
- candidate backlog themes:
  - site selector audit for Sigma DG DN Art wide zoom rows
  - source list expansion for third-party L-mount dealers
  - alias coverage for Korean / l-mount variant alert metadata

## 17. 수정 파일 목록
- `scripts/run_p3_third_party_source_coverage.py`
- `data/admin/p3_third_party_source_coverage_v0.md`
- `data/admin/p3_third_party_source_coverage_v0.jsonl`

## 18. 수정하지 않은 파일/영역
- `classifier_v2.py`
- `model_detector.py`
- `query_parser.py`
- `query_resolver.py`
- `search_service.py`
- `search_ui_hints.py`
- `api/search.py`
- output JSON / taxonomy seed / canonical index / raw data / search index

## 19. output JSON / taxonomy seed / production code 미수정 여부
- output JSON 미수정
- taxonomy seed / canonical index 미수정
- production search code 미수정

## 20. 다음 backlog 후보
- `P3-THIRD-PARTY-SOURCE-COVERAGE-IMPLEMENTATION`
- `P3-DIVERSITY-AWARE-RANKING`
- `P3-ACCESSORY-SUBTYPE-PRECISION`
- `P3-R-LENS-TAXONOMY-AUDIT`
- `P3-SL-ZOOM-FAMILY-TAXONOMY-AUDIT`
