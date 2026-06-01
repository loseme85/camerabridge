# P3-BROAD-ALIAS-CONTROL

## 1. 작업 목적

- broad Leica family alias query인 `summicron`, `summilux`, `leica summicron`, `leica summilux`가 Accessory / Body / SL zoom top1으로 무너지는 문제를 search-layer에서 좁게 보정했다.
- classifier, taxonomy seed, canonical index, output JSON은 수정하지 않았다.
- 이번 라운드의 목표는 broad alias를 특정 seed family로 hard-pin하는 것이 아니라, broad family query를 Lens 중심으로 되돌리고 non-lens top1을 억제하는 것이다.

## 2. 수정 전 문제 요약

- `summicron`
  - before top1: `신품 호환 Leica 14043 Hood Cover for M 35mm f2 Summicron, M 28mm f2.8 Elmarit`
  - before final: `Accessory / Accessory / M / Summicron`
- `summilux`
  - before top1: `Leica Ollux / 12522H Hood Black for M 35mm Summilux 1st`
  - before final: `Accessory / Accessory / M / Summilux`
- `leica summicron`
  - before top1: `신품 호환 Leica 14043 Hood Cover for M 35mm f2 Summicron, M 28mm f2.8 Elmarit`
  - before final: `Accessory / Accessory / M / Summicron`
- `leica summilux`
  - before top1: `Leica Ollux / 12522H Hood Black for M 35mm Summilux 1st`
  - before final: `Accessory / Accessory / M / Summilux`

원인:

- broad alias query는 `model_family`만 맞으면 100점 tie가 많이 생겼다.
- search index 안에는 실제 Lens 후보가 충분히 있었지만, Accessory row도 `model_canonical=Summicron` / `Summilux` 또는 title text hit를 가져서 top1을 먹을 수 있었다.
- broad alias query는 mount/focal/system/body/accessory intent가 없어서 ranking tie-break가 record order에 과하게 기대고 있었다.

## 3. search index 내 broad alias 후보 존재 여부

- `summicron`
  - 후보 존재: 예
  - count: `1231`
  - category 분포: `Lens 1207 / Accessory 8 / Body 16`
  - mount 분포: `M 1068 / SL 113 / L 35 / R 14 / Compact 1`
- `summilux`
  - 후보 존재: 예
  - count: `937`
  - category 분포: `Lens 921 / Accessory 8 / Body 8`
  - mount 분포: `M 870 / SL 33 / R 31 / L 3`

즉 이번 건은 source/index coverage 부족이 아니라, broad family alias query에서 non-lens top1을 충분히 눌러주지 못한 search ranking 문제였다.

## 4. 수정 파일 목록

- [query_resolver.py](/Users/changdaepark/Desktop/LEICA%20SEARCH/query_resolver.py)
- [test_broad_alias_control.py](/Users/changdaepark/Desktop/LEICA%20SEARCH/tests/test_broad_alias_control.py)

## 5. 수정하지 않은 파일 / 영역

- [classifier_v2.py](/Users/changdaepark/Desktop/LEICA%20SEARCH/classifier_v2.py)
- [model_detector.py](/Users/changdaepark/Desktop/LEICA%20SEARCH/model_detector.py)
- [normalization_admin.py](/Users/changdaepark/Desktop/LEICA%20SEARCH/normalization_admin.py)
- [normalized_latest.json](/Users/changdaepark/Desktop/LEICA%20SEARCH/data/normalized/normalized_latest.json)
- [sold_items.json](/Users/changdaepark/Desktop/LEICA%20SEARCH/data/sold_items.json)
- [results.json](/Users/changdaepark/Desktop/LEICA%20SEARCH/results.json)
- `data/admin/entities/*.json`
- [canonical_entities_index.json](/Users/changdaepark/Desktop/LEICA%20SEARCH/data/admin/canonical_entities_index.json)
- [canonical_seed_status.md](/Users/changdaepark/Desktop/LEICA%20SEARCH/data/admin/canonical_seed_status.md)

## 6. target broad alias query before / after

| query | before top1 | before final | after top1 | after final | status | note |
| --- | --- | --- | --- | --- | --- | --- |
| `summicron` | `신품 호환 Leica 14043 Hood Cover for M 35mm f2 Summicron, M 28mm f2.8 Elmarit` | `Accessory / Accessory / M / Summicron` | `Leica L 50mm f2 Summicron Silver` | `Lens / L Lens / L / Summicron` | `weak_pass` | non-lens top1 해소. 여전히 broad query라 mount/focal ambiguity는 남음 |
| `summilux` | `Leica Ollux / 12522H Hood Black for M 35mm Summilux 1st` | `Accessory / Accessory / M / Summilux` | `[중고] L 50/1.4 Summilux 4세대 (Silver)` | `Lens / L Lens / L / Summilux` | `weak_pass` | non-lens top1 해소. 특정 family hard-pin은 하지 않음 |
| `leica summicron` | `신품 호환 Leica 14043 Hood Cover for M 35mm f2 Summicron, M 28mm f2.8 Elmarit` | `Accessory / Accessory / M / Summicron` | `Leica L 50mm f2 Summicron Silver` | `Lens / L Lens / L / Summicron` | `weak_pass` | Leica brand signal 포함 broad query도 Lens 우선 회복 |
| `leica summilux` | `Leica Ollux / 12522H Hood Black for M 35mm Summilux 1st` | `Accessory / Accessory / M / Summilux` | `[중고] L 50/1.4 Summilux 4세대 (Silver)` | `Lens / L Lens / L / Summilux` | `weak_pass` | Leica brand signal 포함 broad query도 Lens 우선 회복 |

## 7. observation-only query 결과

| query | after top1 | after final | status | note |
| --- | --- | --- | --- | --- |
| `cron` | `Leica R 50mm f2 Summicron Black` | `Lens / R Lens / R / Summicron-R` | `observation_only` | 여전히 short risky shorthand. 이번 라운드에서 hard-pin 조정은 하지 않음 |
| `lux` | `Leica M 28mm f1.4 Summilux ASPH 6bit Black` | `Lens / M Lens / M / Summilux-M` | `observation_only` | 여전히 short risky shorthand. 이번 라운드에서 broad control만 적용하지 않음 |

## 8. specific lens guardrail 결과

- 유지됨:
  - `summicron sl 35` -> `Lens / SL Lens / SL / Summicron-SL`
  - `Leica 35mm F2 AsphSummicron SL` -> `Lens / SL Lens / SL / Summicron-SL`
  - `apo summicron sl 35` -> `Lens / SL Lens / SL / Summicron-SL`
  - `sl 35 summicron` -> `Lens / SL Lens / SL / Summicron-SL`
  - `sl 50 summicron` -> `Lens / SL Lens / SL / APO-Summicron`
  - `sl 75 summicron` -> `Lens / SL Lens / SL / APO-Summicron`
  - `sl 90 summicron` -> `Lens / SL Lens / SL / APO-Summicron`
  - `35 lux` -> `Lens / M Lens / M / Summilux-M`
  - `50 lux` -> `Lens / M Lens / M / Summilux-M`

메모:

- 이번 broad alias control은 `summicron` / `summilux` / `leica summicron` / `leica summilux`에만 적용된다.
- `35 lux`, `50 lux`처럼 focal이 붙은 shorthand는 broad alias로 취급하지 않았다.

## 9. SL zoom guardrail 결과

- 유지됨:
  - `sl 24-90` -> `Lens / SL Lens / SL / Vario-Elmarit-SL`
  - `sl 14-24` -> `Lens / SL Lens / SL / Super-Vario-Elmarit-SL`
  - `sl 16-35` -> `Lens / SL Lens / SL / Super-Vario-Elmar-SL`
  - `sl 90-280` -> `Lens / SL Lens / SL / APO-Vario-Elmarit-SL`

이번 broad alias 보정이 SL zoom recall을 방해하지 않음을 확인했다.

## 10. body guardrail 결과

- 유지됨:
  - `leica sl2` -> `Body / SL Body / SL / SL2`
  - `leica sl3` -> `Body / SL Body / SL / SL3`
  - `leica m10 body` -> `Body / M Body / M / M10`
  - `leica iiif` -> `Body / L Body / L / IIIf`
  - `barnack iiif` -> `Body / L Body / L / IIIf`
  - `leica q2` -> `Body / Leica Body / Q / Q2`

## 11. accessory guardrail 결과

- 유지됨:
  - `sl3 battery` -> `Accessory / Accessory / SL / Q3`
  - `leica m strap` -> `Accessory / Accessory / M / M11`
  - `leica hood 12585` -> `Accessory / Accessory / M`
  - `hood 12549` -> `Accessory / Accessory / M / Elmar`
  - `m adapter l` -> `Accessory / Accessory / M`

## 12. third-party L-mount guardrail 결과

- 유지됨:
  - `sigma l 30mm` -> `Lens / SL Lens / SL / brand=3rd Party`
  - `sigma 30mm l` -> `Lens / SL Lens / SL / brand=3rd Party`
- no-result 유지:
  - `sigma 24-70 l`
  - `sigma 14-24 l`
  - `panasonic 24-105 l`
  - `lumix 24-105`

이번 라운드에서는 위 no-result를 억지로 Leica Summicron/Summilux로 채우지 않았다.

## 13. 수정 내용 요약

- broad Leica family alias query helper를 `query_resolver.py`에 추가했다.
- 적용 범위는 매우 좁다:
  - `summicron`
  - `summilux`
  - `leica summicron`
  - `leica summilux`
- 이 broad alias query에 한해:
  - `Accessory` / `Body` top1 후보가 family text만으로 점수를 먹는 경우 score cap을 걸어 Lens row보다 뒤로 보낸다.
  - `SL Lens`라도 zoom-like `Vario` 계열이면 broad family alias query에서 top1을 먹지 못하게 score cap을 건다.
- 하지 않은 것:
  - broad alias를 특정 mount/focal/family로 hard-pin하지 않음
  - `cron` / `lux` 단독 query는 그대로 observation-only
  - classifier / taxonomy / output JSON 수정 없음

## 14. 테스트 결과

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

## 15. 남은 위험

- `summicron`, `summilux` broad query는 now lens-first지만 여전히 `weak_pass` 성격이다.
- broad family query를 더 자연스럽게 만들려면:
  - diversity-aware ranking
  - mount/focal distribution control
  - broad query explanation / ambiguity UI
  가 필요할 수 있다.
- `cron`, `lux`는 여전히 위험 shorthand라 별도 정책이 필요하다.

## 16. 다음 backlog 후보

- `P3-QUERY-RANKING`
- `P3-NO-RESULT-RECALL`
- `P3-R-LENS-QUERY-RECALL`
- `P3-ACCESSORY-TAXONOMY-COVERAGE`
- `P3-SL-ZOOM-FAMILY-TAXONOMY-AUDIT`
- `P3-THIRD-PARTY-L-MOUNT-RECALL`
