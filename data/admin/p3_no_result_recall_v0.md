# P3-NO-RESULT-RECALL

## 1. 작업 목적

- third-party L-mount query의 `no result` 원인을 search-layer / search index / normalized / raw 층으로 분리한다.
- 후보가 실제로 있는 경우에만 search-layer에서 좁게 recall을 복구한다.
- 후보가 없는 경우에는 fake result를 만들지 않고 coverage issue로 남긴다.

## 2. 수정 전 문제 요약

대상 query 네 건은 모두 `no result`였다.

- `sigma 24-70 l`
- `sigma 14-24 l`
- `panasonic 24-105 l`
- `lumix 24-105`

수정 전 공통 원인:

- parser가 `sigma / panasonic / lumix + exact focal range + L signal`을 structured intent로 해석하지 못했다.
- query intent는 모두 `unknown token` 위주였고, `no_structured_search_intent` 경고가 붙었다.
- 따라서 후보가 실제로 있어도 resolver/ranking이 recall을 회복하지 못했다.

## 3. target query before 결과

| query | before top1 | before status | note |
| --- | --- | --- | --- |
| `sigma 24-70 l` | 없음 | `no_result` | 후보는 존재했지만 parser가 구조화 실패 |
| `sigma 14-24 l` | 없음 | `no_result` | 후보 자체가 없음 |
| `panasonic 24-105 l` | 없음 | `no_result` | 후보는 존재했지만 parser가 구조화 실패 |
| `lumix 24-105` | 없음 | `no_result` | 후보는 존재했지만 parser가 구조화 실패 |

## 4. search index / normalized / raw 후보 존재 여부

| query | search index | normalized_latest | raw results | representative candidate |
| --- | --- | --- | --- | --- |
| `sigma 24-70 l` | 있음 | 있음 | 있음 | `[중고] Sigma 24-70/2.8 (SL 마운트)` |
| `sigma 14-24 l` | 없음 | 없음 | 없음 | - |
| `panasonic 24-105 l` | 있음 | 있음 | 있음 | `[중고] 파나소닉 24-105 L 마운트` |
| `lumix 24-105` | 있음 | 있음 | 있음 | `[중고] 파나소닉 24-105 L 마운트` |

해석:

- `sigma 24-70 l`, `panasonic 24-105 l`, `lumix 24-105`는 coverage 부족이 아니라 parser/search-layer 문제였다.
- `sigma 14-24 l`는 search index, normalized, raw 어디에도 후보가 없어서 source/raw coverage 이슈로 보는 편이 맞다.

## 5. 원인 분류

- `sigma 24-70 l`
  - `cause = parser_issue`
- `sigma 14-24 l`
  - `cause = raw_source_coverage_issue`
- `panasonic 24-105 l`
  - `cause = parser_issue`
- `lumix 24-105`
  - `cause = parser_issue`

## 6. 수정 파일 목록

- [query_parser.py](/Users/changdaepark/Desktop/LEICA%20SEARCH/query_parser.py)
- [query_resolver.py](/Users/changdaepark/Desktop/LEICA%20SEARCH/query_resolver.py)
- [test_no_result_recall.py](/Users/changdaepark/Desktop/LEICA%20SEARCH/tests/test_no_result_recall.py)

## 7. 수정하지 않은 파일 / 영역

- [classifier_v2.py](/Users/changdaepark/Desktop/LEICA%20SEARCH/classifier_v2.py)
- [model_detector.py](/Users/changdaepark/Desktop/LEICA%20SEARCH/model_detector.py)
- [normalization_admin.py](/Users/changdaepark/Desktop/LEICA%20SEARCH/normalization_admin.py)
- [normalized_latest.json](/Users/changdaepark/Desktop/LEICA%20SEARCH/data/normalized/normalized_latest.json)
- [sold_items.json](/Users/changdaepark/Desktop/LEICA%20SEARCH/data/sold_items.json)
- [results.json](/Users/changdaepark/Desktop/LEICA%20SEARCH/results.json)
- `data/admin/entities/*.json`
- [canonical_entities_index.json](/Users/changdaepark/Desktop/LEICA%20SEARCH/data/admin/canonical_entities_index.json)
- [canonical_seed_status.md](/Users/changdaepark/Desktop/LEICA%20SEARCH/data/admin/canonical_seed_status.md)

## 8. target query after 결과

| query | after top1 | after final | status | note |
| --- | --- | --- | --- | --- |
| `sigma 24-70 l` | `[중고] Sigma 24-70/2.8 (SL 마운트)` | `Lens / SL Lens / SL / brand=3rd Party` | `pass` | exact candidate 복구 |
| `sigma 14-24 l` | 없음 | - | `needs_source_or_index_followup` | 후보 부재. fake result 없음 |
| `panasonic 24-105 l` | `[중고] 파나소닉 24-105 L 마운트` | `Lens / SL Lens / SL / brand=Unknown` | `weak_pass` | 후보 복구. brand field는 아직 Unknown |
| `lumix 24-105` | `[중고] 파나소닉 24-105 L 마운트` | `Lens / SL Lens / SL / brand=Unknown` | `weak_pass` | Lumix/Panasonic family alias로 한국어 title 회수 |

## 9. 수정 내용 요약

- query parser에 narrow third-party L-mount hint를 추가했다.
- 활성 조건은 매우 좁다:
  - brand token: `sigma` / `panasonic` / `lumix`
  - exact range: `24-70` / `14-24` / `24-105`
  - L-mount signal:
    - `l`
    - `l mount`
    - `l-mount`
    - `sl 마운트`
    - `dg dn`
    - `lumix s`
  - `lumix 24-105`는 observation query이지만 Lumix/Panasonic family alias로 허용
- resolver에는 third-party L-mount control을 추가했다.
  - exact brand-family text + exact focal range + `SL` lens 조건을 만족하지 않으면 score cap을 걸어 fake result를 막는다.
  - 그래서 `sigma 14-24 l`는 Sigma 30mm 같은 unrelated row로 채워지지 않고 no-result로 유지된다.

## 10. third-party pass guardrail 결과

- 유지됨:
  - `sigma l 30mm` -> `Lens / SL Lens / SL / brand=3rd Party`
  - `sigma 30mm l` -> `Lens / SL Lens / SL / brand=3rd Party`

## 11. Leica SL zoom guardrail 결과

- 유지됨:
  - `sl 24-90` -> `Lens / SL Lens / SL / Vario-Elmarit-SL`
  - `sl 14-24` -> `Lens / SL Lens / SL / Super-Vario-Elmarit-SL`
  - `sl 16-35` -> `Lens / SL Lens / SL / Super-Vario-Elmar-SL`
  - `sl 90-280` -> `Lens / SL Lens / SL / APO-Vario-Elmarit-SL`

이번 third-party recall 보정이 Leica SL zoom query를 third-party로 오염시키지 않았다.

## 12. broad alias guardrail 결과

- 유지됨:
  - `summicron` -> Lens-first
  - `summilux` -> Lens-first
  - `leica summicron` -> Lens-first
  - `leica summilux` -> Lens-first
  - `cron`, `lux` -> observation-only 성격 유지

## 13. body guardrail 결과

- 유지됨:
  - `leica sl2` -> `Body / SL Body / SL / SL2`
  - `leica sl3` -> `Body / SL Body / SL / SL3`
  - `leica m10 body` -> `Body / M Body / M / M10`
  - `leica iiif` / `barnack iiif` / `leica q2` -> 기존 Body 유지

## 14. accessory guardrail 결과

- 유지됨:
  - `sl3 battery` -> `Accessory / Accessory / SL / Q3`
  - `leica m strap` -> `Accessory / Accessory / M / M11`
  - `leica hood 12585` / `hood 12549` / `m adapter l` -> Accessory 유지

## 15. specific Leica lens guardrail 결과

- 유지됨:
  - `summicron sl 35`
  - `Leica 35mm F2 AsphSummicron SL`
  - `apo summicron sl 35`
  - `35 lux`
  - `50 lux`

모두 Leica Lens 상태 유지.

## 16. 테스트 결과

- `python3 tests/test_no_result_recall.py` = `ok`
- `python3 tests/test_broad_alias_control.py` = `ok`
- `python3 tests/test_sl_zoom_query_recall.py` = `ok`
- `python3 tests/test_accessory_search_ranking.py` = `ok`
- `python3 tests/test_search_body_query_recall.py` = `ok`
- `python3 tests/test_accessory_token_guardrail.py` = `ok`
- `python3 tests/test_accessory_category.py` = `ok`
- `python3 tests/test_sl_string_drift.py` = `ok`
- `python3 tests/test_sl_zoom_classification.py` = `ok`
- `python3 tests/test_body_classification.py` = `ok`
- `python3 tests/test_r_tele_classification.py` = `ok`
- `python3 tests/test_normalization_admin.py` = `ok`
- `python3 -m py_compile classifier_v2.py model_detector.py normalization_admin.py golden_set.py tests/test_normalization_admin.py query_parser.py query_resolver.py search_service.py api/search.py` = `ok`
- `python3 golden_set.py` = `132/132`

## 17. 남은 위험

- `panasonic 24-105 l`, `lumix 24-105`는 useful result를 찾았지만 row의 `brand` field가 `Unknown`이다.
  - 검색 UX는 개선됐지만 taxonomy/normalization 품질 관점에서는 아직 weak point다.
- `sigma 14-24 l`는 candidate가 전혀 없어서 ranking으로 해결할 수 없다.
- `third-party L-mount`는 brand canonicalization과 source coverage가 아직 uneven하다.

## 18. 다음 backlog 후보

- `P3-THIRD-PARTY-L-MOUNT-RECALL`
- `P3-QUERY-RANKING`
- `P3-R-LENS-QUERY-RECALL`
- `P3-ACCESSORY-TAXONOMY-COVERAGE`
- `P3-SL-ZOOM-FAMILY-TAXONOMY-AUDIT`
- `P3-CRON-LUX-SHORT-ALIAS-POLICY`
