# P3 SL Zoom Query Recall v0

- 작업명: `P3-SL-ZOOM-QUERY-RECALL`

## 1. 작업 목적

- `sl 24-90`, `sl 14-24`, `sl 16-35`, `sl 90-280` 같은 Leica SL zoom shorthand query의 recall / ranking을 search-layer에서 좁게 복구한다.
- classifier나 taxonomy를 건드리지 않고 query parser / query resolver / ranking 층에서 해결한다.
- 목표는:
  - Leica SL zoom shorthand query가 Leica SL zoom row를 top1으로 가져오게 하는 것
  - Body / Accessory / SL prime / broad lens / third-party L-mount query를 오염시키지 않는 것

## 2. 수정 전 문제 요약

`SEARCH-RELIABILITY-SMOKE-V1` 기준으로 SL zoom shorthand는 category 자체는 Lens로 유지되지만 family recall이 약했다.

- `sl 24-90`
  - top1이 `Sigma L 30mm f1.4 DC DN...`
- `sl 14-24`
  - Leica SL 14-24 후보가 있어도 unrelated L-mount row가 먼저 끼어듦
- `sl 16-35`
  - exact range row가 있어도 family/model signal이 약한 stale row라 ranking이 불안정
- `sl 90-280`
  - Leica 후보는 있었지만 stale family/mount 표현이 섞여 있어 query recall 품질이 낮음

원인은 크게 두 가지였다.

1. parser가 `sl + exact zoom range`를 structured focal range intent로 만들지 못했다.  
2. resolver는 stored `focal_length`가 비어 있는 stale SL zoom row의 title-range를 충분히 읽지 못했다.

## 3. search index 내 관련 Leica SL zoom 후보 존재 여부

이번 라운드에서 search index를 먼저 확인한 결과, target 네 query 모두 관련 Leica SL zoom 후보가 존재했다.

- `sl 24-90`
  - `Leica SL 24-90mm f2.8-4 Vario-Elmarit Black`
  - `[위탁] SL 24-90/2.8-4 Vario Elmar ASPH (Black)`
- `sl 14-24`
  - `[중고] SL 14-24/2.8 Vario Elmarit ASPH (Black)`
- `sl 16-35`
  - `[중고] SL 16-35/3.5-4.5 Super Vario Elmar ASPH (Black)`
  - `LEICA SL2 16-35mm F3.5-4.5 ASPH ...`
- `sl 90-280`
  - `[중고] SL APO Vario Elmarit 90-280 f/2.8-4`
  - `[중고] SL 90-280/2.8-4 APO Vario Elmarit ASPH (Black)`

즉 이번 문제는 source/index coverage 부족이 아니라 query intent / ranking 문제였다.

## 4. 수정 파일 목록

- [query_parser.py](/Users/changdaepark/Desktop/LEICA%20SEARCH/query_parser.py)
- [query_resolver.py](/Users/changdaepark/Desktop/LEICA%20SEARCH/query_resolver.py)
- [test_sl_zoom_query_recall.py](/Users/changdaepark/Desktop/LEICA%20SEARCH/tests/test_sl_zoom_query_recall.py)

핵심 수정:

- `query_parser.py`
  - `sl 24-90`, `sl 14-24`, `sl 16-35`, `sl 90-280`를 narrow SL zoom range hint로 파싱
  - `SL` token이 있고, exact zoom range가 있으며, accessory/body/lens-family blocker가 없는 경우에만 적용
  - broad `24-90`, broad `16-35`, broad `sl` 자체는 열지 않음

- `query_resolver.py`
  - zoom range를 title text에서도 exact range로 읽도록 강화
  - obvious stale SL zoom row를 search-time only로 `SL Lens / SL / expected zoom family` projection
  - 그래서 stored model/focal field가 약해도 exact Leica SL zoom title이 top ranking에서 살아남게 함

## 5. target SL zoom query before / after

| query | before top1 | before category | after top1 | after category | after label | after mount | after model | status | note |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `sl 24-90` | `Sigma L 30mm f1.4 DC DN Black for CL, TL2, etc` | `Lens` | `Leica SL 24-90mm f2.8-4 Vario-Elmarit Black` | `Lens` | `SL Lens` | `SL` | `Vario-Elmarit-SL` | `pass` | SL zoom shorthand now ranks Leica SL zoom family first |
| `sl 14-24` | `Sigma L 30mm f1.4 DC DN Black for CL, TL2, etc` | `Lens` | `[중고] SL 14-24/2.8 Vario Elmarit ASPH (Black)` | `Lens` | `SL Lens` | `SL` | `Super-Vario-Elmarit-SL` | `pass` | SL zoom shorthand now ranks Leica SL zoom family first |
| `sl 16-35` | `Sigma L 30mm f1.4 DC DN Black for CL, TL2, etc` | `Lens` | `LEICA SL2 16-35mm F3.5-4.5 ASPH ...` | `Lens` | `SL Lens` | `SL` | `Super-Vario-Elmar-SL` | `pass` | SL zoom shorthand now ranks Leica SL zoom family first |
| `sl 90-280` | `Sigma L 30mm f1.4 DC DN Black for CL, TL2, etc` | `Lens` | `[중고] SL APO Vario Elmarit 90-280 f/2.8-4` | `Lens` | `SL Lens` | `SL` | `APO-Vario-Elmarit-SL` | `pass` | SL zoom shorthand now ranks Leica SL zoom family first |

상세 per-query 기록은 [p3_sl_zoom_query_recall_v0.jsonl](/Users/changdaepark/Desktop/LEICA%20SEARCH/data/admin/p3_sl_zoom_query_recall_v0.jsonl)에 남겼다.

## 6. body guardrail 결과

이번 SL zoom recall 보정 이후에도 body query는 그대로 유지됐다.

- `leica sl2` -> `Body / SL Body / SL / SL2`
- `leica sl3` -> `Body / SL Body / SL / SL3`
- `leica m10 body` -> `Body / M Body / M / M10`
- `leica iiif` -> `Body / L Body / L / IIIf`
- `barnack iiif` -> `Body / L Body / L / IIIf`
- `leica q2` -> `Body / Leica Body / Q / Q2`

## 7. accessory guardrail 결과

직전 accessory ranking 복구도 유지됐다.

- `sl3 battery` -> `Accessory / Accessory / SL / Q3`
- `leica m strap` -> `Accessory / Accessory / M / M11`
- `leica hood 12585` -> Accessory 유지
- `hood 12549` -> Accessory 유지
- `m adapter l` -> Accessory 유지

즉 `SL` token이 들어간 accessory query도 이번 zoom 보정으로 Lens로 오염되지 않았다.

## 8. SL prime lens guardrail 결과

SL prime query는 zoom으로 오염되지 않았다.

- `summicron sl 35` -> `Lens / SL Lens / SL / Summicron-SL`
- `Leica 35mm F2 AsphSummicron SL` -> `Lens / SL Lens / SL / Summicron-SL`
- `apo summicron sl 35` -> `Lens / SL Lens / SL / Summicron-SL`
- `sl 35 summicron` -> `Lens / SL Lens / SL / Summicron-SL`
- `sl 50 summicron` -> `Lens / SL Lens / SL / APO-Summicron 50`
- `sl 75 summicron` -> `Lens / SL Lens / SL / APO-Summicron 75`
- `sl 90 summicron` -> `Lens / SL Lens / SL / APO-Summicron 90`

## 9. broad lens / third-party L-mount guardrail 결과

### Broad lens guardrail

- `35 lux`, `50 lux`는 계속 M lens 쪽 유지
- `summicron`, `summilux`는 여전히 broad query지만 SL zoom으로 hard-pin되지는 않음

### Third-party / L-mount guardrail

- `sigma l 30mm`
- `sigma 30mm l`

는 그대로 Sigma row가 유지됐다.

또한:

- `sigma 24-70 l`
- `sigma 14-24 l`
- `panasonic 24-105 l`
- `lumix 24-105`

는 이번 수정으로 Leica SL zoom으로 오염되지 않았다. 현재 search path에서는 여전히 no-result지만, 그것은 별도 recall backlog다.

## 10. 수정하지 않은 파일 / 영역

이번 라운드에서 아래는 수정하지 않았다.

- [classifier_v2.py](/Users/changdaepark/Desktop/LEICA%20SEARCH/classifier_v2.py)
- [model_detector.py](/Users/changdaepark/Desktop/LEICA%20SEARCH/model_detector.py)
- [normalized_latest.json](/Users/changdaepark/Desktop/LEICA%20SEARCH/data/normalized/normalized_latest.json)
- [sold_items.json](/Users/changdaepark/Desktop/LEICA%20SEARCH/data/sold_items.json)
- [results.json](/Users/changdaepark/Desktop/LEICA%20SEARCH/results.json)
- `data/admin/entities/*.json`
- [canonical_entities_index.json](/Users/changdaepark/Desktop/LEICA%20SEARCH/data/admin/canonical_entities_index.json)
- [canonical_seed_status.md](/Users/changdaepark/Desktop/LEICA%20SEARCH/data/admin/canonical_seed_status.md)
- taxonomy seed / canonical entity layer 전체

root `results.json` write pass도 이번 라운드에서는 수행하지 않았다.

## 11. 테스트 결과

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

## 12. 남은 위험

- `apo summicron sl 35`는 여전히 APO family ranking이 약하다.
- broad `summicron`, `summilux`는 이번 라운드에서 zoom hard-pin은 막았지만, broad alias control 자체는 별도 backlog다.
- `sigma 24-70 l`, `panasonic 24-105 l`, `lumix 24-105`는 third-party no-result recall이 남아 있다.
- 이번 수정은 Leica SL zoom shorthand recall을 복구한 것이지, Leica SL zoom taxonomy 전체를 확장한 것은 아니다.

## 13. 다음 backlog 후보

- `P3-QUERY-RANKING`
- `P3-BROAD-ALIAS-CONTROL`
- `P3-NO-RESULT-RECALL`
- `P3-R-LENS-QUERY-RECALL`
- `P3-ACCESSORY-TAXONOMY-COVERAGE`
- `P3-SL-ZOOM-FAMILY-TAXONOMY-AUDIT`

## 14. 결론

이번 라운드는 Leica SL zoom shorthand 4개를 search-layer에서 좁게 복구했다.

- `sl 24-90`
- `sl 14-24`
- `sl 16-35`
- `sl 90-280`

모두 이제 Leica SL zoom row가 top1으로 올라온다.

그리고 중요한 guardrail도 유지됐다.

- body query 유지
- accessory query 유지
- SL prime query zoom contamination 없음
- broad lens query hard-pin 없음
- third-party L-mount query Leica contamination 없음

즉 이번 라운드는 classifier나 output JSON을 건드리지 않고,
SL zoom shorthand recall만 search-layer에서 안정화한 작업으로 정리할 수 있다.
