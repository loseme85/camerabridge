# P3-THIRD-PARTY-BRAND-CANONICALIZATION

## 1. 작업 목적

- Panasonic / Lumix / 파나소닉 / 루믹스 계열 third-party L-mount row가 왜 `brand=Unknown` 또는 raw `brand=Other`로 남는지 분리한다.
- 기존 third-party brand convention을 확인하고, 가능한 경우 기존 bucket `3rd Party`로 좁게 canonicalize한다.
- output JSON / taxonomy seed는 수정하지 않는다.

## 2. 수정 전 문제 요약

- `panasonic 24-105 l`, `lumix 24-105`, `panasonic lumix 24-105`, `lumix s 24-105`, `lumix 24-105 f4`는 useful recall이 가능했지만 stored search result brand가 `Unknown`으로 남아 있었다.
- raw `results.json`에서는 같은 row가 `brand=Other`로 남아 있었다.
- Sigma 계열은 이미 `brand=3rd Party`로 안정적이었기 때문에 Panasonic/Lumix만 중앙 brand 감지가 비어 있는지 확인할 필요가 있었다.

## 3. brand schema / existing convention 확인 결과

- `classifier_v2.py`의 `VALID_BRANDS`에는 `Sigma`, `Panasonic`이 보이지만, 실제 `detect_brand()`의 canonical output convention은 third-party maker를 개별 brand가 아니라 `3rd Party` bucket으로 묶는 쪽에 가깝다.
- 현재 classifier smoke 기준: Sigma / TTArtisan / Voigtlander / Lumix / Panasonic L-mount title은 모두 `brand=3rd Party`가 가장 일관된 convention이다.
- 따라서 이번 라운드에서도 `Panasonic` 같은 새 brand schema를 열지 않고 기존 `3rd Party` convention을 따랐다.

## 4. Panasonic/Lumix row의 raw / normalized / search index brand 상태

- raw `results.json`: `[중고] 파나소닉 24-105 L 마운트` -> `brand=Other`
- `data/normalized/normalized_latest.json`: same row -> `brand=Unknown`
- `data/derived/results_search_index_v1.json`: same row -> `brand=Unknown`
- current code direct classifier: same row -> `brand=3rd Party`
- current search response: stale compact row를 search-time projection으로 `brand=3rd Party`로 노출

## 5. 원인 분류

- `brand_detector_gap`: Korean Panasonic/Lumix tokens (`파나소닉`, `루믹스`)가 central `detect_brand()`의 third-party list에 없어서 current classifier가 `Unknown`으로 떨어지고 있었다.
- `normalization_stale_output` / `search_index_stale_output`: stored normalized/search index는 이전 output이어서 여전히 `Unknown`을 들고 있다.
- `schema_limitation`: 이번 라운드에서는 개별 brand schema를 열지 않고 기존 `3rd Party` bucket을 유지했다.

## 6. 수정 파일 목록

- `classifier_v2.py`
- `query_resolver.py`
- `tests/test_third_party_brand_canonicalization.py`

## 7. 수정하지 않은 파일 / 영역

- `model_detector.py` 수정 없음
- taxonomy seed / canonical index 수정 없음
- `data/normalized/normalized_latest.json` 수정 없음
- `data/sold_items.json` 수정 없음
- `results.json` 수정 없음
- search index write 없음

## 8. target query before / after

| query | before brand | after brand | top1 title | status | note |
|---|---|---|---|---|---|
| panasonic 24-105 l | Unknown | 3rd Party | [중고] 파나소닉 24-105 L 마운트 | pass | Stored raw/normalized/search-index brand is still Other/Unknown, but current classifier + search-time projection now expose 3rd Party. |
| lumix 24-105 | Unknown | 3rd Party | [중고] 파나소닉 24-105 L 마운트 | pass | Useful Panasonic row remains top1 and now projects to 3rd Party under current code. |
| panasonic lumix 24-105 | no result | 3rd Party | [중고] 파나소닉 24-105 L 마운트 | pass | Dual-brand wording now keeps useful recall and projects the stale row to 3rd Party. |
| lumix s 24-105 | Unknown | 3rd Party | [중고] 파나소닉 24-105 L 마운트 | pass | Current classifier convention is 3rd Party, not a new Panasonic/Lumix schema value. |
| lumix 24-105 f4 | no result | 3rd Party | [중고] 파나소닉 24-105 L 마운트 | pass | Candidate narrowing recovery stays intact and the stale stored row now projects to 3rd Party. |

## 9. direct brand detector / classifier check 결과

- `[중고] 파나소닉 24-105 L 마운트` -> `brand=3rd Party`, `mount=SL`, `category=Lens`, `label=SL Lens`, `reason=['3rd_party_first_token:파나소닉']`
- `Panasonic Lumix S Pro 24-105mm f4 Macro OIS` -> `brand=3rd Party`, `mount=SL`, `category=Lens`, `label=SL Lens`, `reason=['3rd_party_first_token:panasonic']`
- `lumix s 24-105 f4 macro o.i.s.` -> `brand=3rd Party`, `mount=SL`, `category=Lens`, `label=SL Lens`, `reason=['3rd_party_first_token:lumix']`
- `파나소닉 루믹스 24-105 L 마운트` -> `brand=3rd Party`, `mount=SL`, `category=Lens`, `label=SL Lens`, `reason=['3rd_party_first_token:파나소닉']`
- `[중고] Sigma 24-70/2.8 (SL 마운트)` -> `brand=3rd Party`, `mount=SL`, `category=Lens`, `label=SL Lens`, `reason=['3rd_party_first_token:sigma']`
- `Sigma L 30mm f1.4 DC DN Black for CL, TL2, etc` -> `brand=3rd Party`, `mount=SL`, `category=Lens`, `label=SL Lens`, `reason=['3rd_party_first_token:sigma']`

## 10. Sigma guardrail 결과

- `sigma 24-70 l`, `sigma 24-70 l mount`, `sigma 24-70 dg dn`, `sigma 24-70 dg dn art`, `sigma l 30mm`, `sigma 30mm l` 모두 `brand=3rd Party` 유지
- `sigma 14-24 l`는 여전히 no-result 유지; fake result 없음

## 11. Leica SL zoom guardrail 결과

- `sl 24-90`, `sl 14-24`, `sl 16-35`, `sl 90-280` 모두 Leica SL zoom top1 유지

## 12. Leica L / SL prime guardrail 결과

- `Leica L 50mm Summicron`, `summicron sl 35`, `Leica 35mm F2 AsphSummicron SL`, `apo summicron sl 35`, `sl 35/50/75/90 summicron`, `35 lux`, `50 lux` 모두 Leica lens 유지

## 13. broad alias / body / accessory guardrail 결과

- broad alias: `summicron`, `summilux`, `leica summicron`, `leica summilux`는 Lens-first 유지; `cron`, `lux`는 observation-only 성격 유지
- body: `leica sl2`, `leica sl3`, `leica m10 body`, `leica iiif`, `barnack iiif`, `leica q2` 유지
- accessory: `sl3 battery`, `leica m strap`, `leica hood 12585`, `hood 12549`, `m adapter l` 유지

## 14. observation query 결과

- `panasonic`, `lumix`, `파나소닉`, `루믹스`, `panasonic l mount`, `lumix l mount`는 모두 no-result 유지
- 이번 라운드에서는 broad Panasonic/Lumix recall을 억지로 열지 않았다.

## 15. output JSON / taxonomy seed 미수정 여부

- output JSON write 없음
- `results.json` / `normalized_latest.json` / `sold_items.json` 수정 없음
- taxonomy seed / canonical entity / index 수정 없음

## 16. 테스트 결과

- 신규 `tests/test_third_party_brand_canonicalization.py` 통과
- 기존 third-party / search-layer / classifier guardrail 테스트 통과
- `golden_set.py` = `132/132` 유지

## 17. 남은 위험

- stored raw/normalized/search-index brand는 아직 `Other` / `Unknown`이라 regeneration 없이는 파일 자체는 바뀌지 않는다.
- `sigma 14-24`는 여전히 source coverage가 없어서 no-result가 맞다.
- Panasonic/Lumix broad brand query는 이번 라운드 범위상 열지 않았다.

## 18. 다음 backlog 후보

- `P3-R-LENS-QUERY-RECALL`
- `P3-QUERY-RANKING`
- `P3-ACCESSORY-TAXONOMY-COVERAGE`
- `P3-SL-ZOOM-FAMILY-TAXONOMY-AUDIT`
- `P3-CRON-LUX-SHORT-ALIAS-POLICY`
- `P3-THIRD-PARTY-SOURCE-COVERAGE`

## 19. 상태 분포

- `guardrail_pass`: `38`
- `observation_only`: `6`
- `pass`: `5`