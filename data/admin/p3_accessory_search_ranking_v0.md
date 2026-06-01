# P3 Accessory Search Ranking v0

- 작업명: `P3-ACCESSORY-SEARCH-RANKING`

## 1. 작업 목적

- `sl3 battery`, `leica m strap`처럼 accessory intent가 명확한 query에서 search recall / ranking을 좁게 보정한다.
- classifier나 taxonomy를 건드리지 않고 query parser / query resolver / ranking 층에서 해결한다.
- 목표는 두 가지다.
  - accessory query가 Body / Lens로 오염되지 않도록 유지
  - accessory 후보가 실제 index 안에 있을 때 lens/body row보다 위로 오르게 하기

## 2. 수정 전 문제 요약

직전 상태에서 두 target query는 아래처럼 약했다.

- `sl3 battery`
  - `no_result / weak_pass`
  - Body 오염은 없었지만 accessory recall이 거의 없었다.
- `leica m strap`
  - top1이 `Lens / M Lens / M`
  - strap accessory 후보가 있어도 lens row가 먼저 왔다.

이번 라운드에서 먼저 search index를 확인한 결과:

- `sl3 battery` 관련 accessory 후보는 실제로 존재했다.
  - `Leica Q3, SL3 Battery [BP-SCL6]`
  - `[중고] Q3,SL3 배터리 (BP-SCL6)`
  - `[위탁] Q3,SL3 배터리 (BP-SCL6)`
- 다만 `battery` 텍스트가 들어간 non-battery accessory도 있었다.
  - `Jnk SL2 Case [Black / Battery Door Type]`

- `leica m strap` 관련 accessory 후보도 실제로 존재했다.
  - `[중고] Leica M11 strap (Cognac)`
  - `[중고] Leica M11 Neck strap (Cognac)`
  - `Used Leica Carrying Strap for SL or S-System - Elk Leather`

즉 이번 문제는 source/index coverage 부족이 아니라,
accessory intent parsing과 ranking 우선순위가 약한 쪽에 가까웠다.

## 3. 수정 파일 목록

- [query_parser.py](/Users/changdaepark/Desktop/LEICA%20SEARCH/query_parser.py)
- [query_resolver.py](/Users/changdaepark/Desktop/LEICA%20SEARCH/query_resolver.py)
- [test_accessory_search_ranking.py](/Users/changdaepark/Desktop/LEICA%20SEARCH/tests/test_accessory_search_ranking.py)

핵심 수정:

- `query_parser.py`
  - `battery`, `배터리`, `BP-SCL*` query를 accessory intent `battery`로 파싱
  - `strap`, `hand strap`, `neck strap`, `shoulder strap`, `스트랩` query를 accessory intent `strap`로 파싱
  - accessory query 안의 `sl2/sl3`는 Body intent가 아니라 **accessory compatibility mount hint**로만 `SL`을 부여

- `query_resolver.py`
  - accessory query에서 `accessory_type` exact match는 강하게 유지
  - 반대로 accessory_type이 다른데 title text에만 accessory token이 들어간 경우에는 점수를 낮춤
  - 그래서 `battery door case`가 실제 `battery` row를 이기는 현상을 막음

## 4. target query before / after

| query | before top1 | before category | after top1 | after category | after label | after mount | after model | status | note |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `sl3 battery` | - | - | `[중고] Q3,SL3 배터리 (BP-SCL6)` | `Accessory` | `Accessory` | `SL` | `Q3` | `pass` | accessory query now ranks battery accessory above body/lens and above battery-door case |
| `leica m strap` | `Leica M 50mm f2.8 Elmar Black` | `Lens` | `[중고] Leica M11 strap (Cognac)` | `Accessory` | `Accessory` | `M` | `M11` | `pass` | strap accessory now outranks lens rows |

상세 row 기록은 [p3_accessory_search_ranking_v0.jsonl](/Users/changdaepark/Desktop/LEICA%20SEARCH/data/admin/p3_accessory_search_ranking_v0.jsonl)에 남겼다.

## 5. preserved accessory query 결과

- `leica hood 12585` -> `Accessory / Accessory / M`
- `hood 12549` -> `Accessory / Accessory / M`
- `m adapter l` -> `Accessory / Accessory / M`

기존 Accessory-first query는 모두 유지됐다.

## 6. body guardrail 결과

이번 accessory ranking 보정 이후에도 body query는 유지됐다.

- `leica sl2` -> `Body / SL Body / SL / SL2`
- `leica sl3` -> `Body / SL Body / SL / SL3`
- `leica m10 body` -> `Body / M Body / M / M10`
- `leica iiif` -> `Body / L Body / L / IIIf`
- `barnack iiif` -> `Body / L Body / L / IIIf`
- `leica q2` -> `Body / Leica Body / Q / Q2`

즉 `sl3 battery`가 `SL3` 토큰을 갖고 있어도 Body로 오염되지는 않았다.

## 7. lens guardrail 결과

이번 라운드 이후에도 lens query는 Accessory로 오염되지 않았다.

- `summicron sl 35` -> Lens 유지
- `Leica 35mm F2 AsphSummicron SL` -> Lens 유지
- `apo summicron sl 35` -> Lens 유지
- `sl 24-90` -> Lens 유지
- `sl 14-24` -> Lens 유지
- `sl 16-35` -> Lens 유지
- `sl 90-280` -> Lens 유지
- `35 lux` -> Lens 유지
- `50 lux` -> Lens 유지

다만 아래는 기존 약점이 그대로 남아 있다.

- `apo summicron sl 35` APO family ranking 약점
- `sl 24-90`, `sl 14-24`, `sl 16-35`, `sl 90-280` zoom family recall 약점

이건 이번 accessory 라운드 범위 밖이다.

## 8. 수정하지 않은 파일 / 영역

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

## 9. 테스트 결과

- `python3 tests/test_accessory_search_ranking.py` = `ok`
- `python3 tests/test_search_body_query_recall.py` = `ok`
- `python3 tests/test_accessory_token_guardrail.py` = `ok`
- `python3 tests/test_accessory_category.py` = `ok`
- `python3 tests/test_sl_string_drift.py` = `ok`
- `python3 tests/test_sl_zoom_classification.py` = `ok`
- `python3 tests/test_body_classification.py` = `ok`
- `python3 tests/test_r_tele_classification.py` = `ok`
- `python3 tests/test_normalization_admin.py` = `ok`

## 10. 남은 위험

- `sl3 battery`는 이제 accessory recall이 살아났지만, top candidate가 `Q3,SL3` shared battery라 exact body compatibility ranking은 더 다듬을 여지가 있다.
- `leica m strap`은 top1이 accessory로 올라왔지만, `M11 strap`이 generic `Leica M strap` query의 첫 결과인 점은 accessory ranking 품질 관점에서 추가 검토 여지가 있다.
- `BP-SCL5`처럼 code-only accessory query는 이번에 함께 좋아졌지만, broader battery coverage는 아직 별도 점검이 필요하다.

## 11. 다음 backlog 후보

- `P3-QUERY-RANKING`
- `P3-SL-ZOOM-QUERY-RECALL`
- `P3-BROAD-ALIAS-CONTROL`
- `P3-NO-RESULT-RECALL`
- `P3-R-LENS-QUERY-RECALL`
- `P3-ACCESSORY-TAXONOMY-COVERAGE`

## 12. 결론

이번 라운드는 accessory query 두 건을 search-layer에서 좁게 복구했다.

- `sl3 battery`는 이제 Accessory row가 top1이다.
- `leica m strap`도 이제 Accessory row가 top1이다.

그리고 중요한 guardrail도 유지했다.

- preserved accessory query 유지
- body query recall 유지
- lens query accessory contamination 없음

즉 이번 라운드는 classifier나 taxonomy를 건드리지 않고,
search ranking만으로 accessory intent query의 실사용 품질을 한 단계 올린 라운드로 정리할 수 있다.
