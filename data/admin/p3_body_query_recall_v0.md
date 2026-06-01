# P3 Body Query Recall v0

- 작업명: `P3-BODY-QUERY-RECALL`

## 1. 목적

- `SEARCH-RELIABILITY-SMOKE-V1`에서 드러난 body query `wrong_category`를 검색층에서 좁게 복구한다.
- 이번 라운드는 classifier 수정이 아니라 query parser / resolver / ranking 보정 라운드다.
- 목표 query:
  - `leica sl2`
  - `leica sl3`
  - `leica m10 body`

## 2. 수정 전 문제 요약 / 원인 분석

이번 문제는 classifier보다 검색층 쪽이 더 컸다.

- search index 안에는 body 후보가 이미 있었다.
  - `M10` body row는 실제 `Body / M Body / M / M10`로 존재했다.
  - `SL2`, `SL3`는 stored search index 안에서 `Leica SL2 Black`, `Leica SL3 Black` title이 존재했지만 stale `Lens / SL Lens / SL / None` 상태였다.
- query resolver는 기존에 `leica iiif`, `barnack iiif`, `leica q2` 같은 body query는 처리했지만, `sl2`, `sl3`, `m10 body`는 explicit body intent로 구조화하지 못했다.
- ranking에서는 explicit body intent가 생겨도 unrelated Body row에 broad bonus를 주는 경로가 있어, 정확한 model match보다 무관한 body row가 먼저 나올 수 있었다.

정리하면 원인은 세 갈래였다.

1. `SL2 / SL3 / M10 body` query가 body intent로 파싱되지 않음  
2. body ranking이 exact model match보다 broad body category에 너무 관대했음  
3. `SL2 / SL3`는 stored search index가 stale lens label이라 search-time projection이 필요했음

## 3. 수정 파일 목록 / 수정 내용

수정 파일:

- [query_parser.py](/Users/changdaepark/Desktop/LEICA%20SEARCH/query_parser.py)
- [query_resolver.py](/Users/changdaepark/Desktop/LEICA%20SEARCH/query_resolver.py)
- [test_search_body_query_recall.py](/Users/changdaepark/Desktop/LEICA%20SEARCH/tests/test_search_body_query_recall.py)

핵심 수정:

- `query_parser.py`
  - `leica sl2`, `leica sl3`를 narrow explicit body intent로 파싱
  - `m10`은 query 안에 `body`가 있을 때만 `M10` body intent로 파싱
  - `battery`, `hood`, `adapter`, `strap` 같은 accessory blocker가 있으면 body intent를 만들지 않음
  - `summicron`, `summilux`, `apo`, `vario` 같은 lens blocker가 있으면 body intent를 만들지 않음

- `query_resolver.py`
  - explicit body query에서 obvious body-like stale rows (`Leica SL2 Black`, `Leica SL3 Black`)를 search-time only로 `Body` projection
  - unrelated body rows에 주던 broad body bonus 제거
  - exact model/text match가 없는 body row는 더 이상 `SL2 / SL3 / M10 body` query를 가로채지 못함

## 4. Before / After 결과

| query | group | before top1 title | before category | before label | before mount | before model | after top1 title | after category | after label | after mount | after model | status | note |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `leica sl2` | Target Body Queries | `Leica M 50mm f2.8 Elmar Black` | `Lens` | `M Lens` | `M` | `Elmar` | `Leica SL2 Black` | `Body` | `SL Body` | `SL` | `SL2` | `pass` | body recall restored on search path |
| `leica sl3` | Target Body Queries | `Leica M 50mm f2.8 Elmar Black` | `Lens` | `M Lens` | `M` | `Elmar` | `Leica SL3 Black` | `Body` | `SL Body` | `SL` | `SL3` | `pass` | body recall restored on search path |
| `leica m10 body` | Target Body Queries | `Leica M 50mm f2.8 Elmar Black` | `Lens` | `M Lens` | `M` | `Elmar` | `[위탁] M10 Monochrom 'Leitz Wetzlar' Edition` | `Body` | `M Body` | `M` | `M10` | `pass` | body recall restored on search path |
| `leica iiif` | Existing Body Pass Queries | `Leica Barnack IIIF Silver` | `Body` | `L Body` | `L` | `IIIf` | `Leica Barnack IIIF Silver` | `Body` | `L Body` | `L` | `IIIf` | `pass` | existing body pass preserved |
| `barnack iiif` | Existing Body Pass Queries | `Leica Barnack IIIF Silver` | `Body` | `L Body` | `L` | `IIIf` | `Leica Barnack IIIF Silver` | `Body` | `L Body` | `L` | `IIIf` | `pass` | existing body pass preserved |
| `leica q2` | Existing Body Pass Queries | `Leica Q2 007 Edition` | `Body` | `Leica Body` | `Q` | `Q2` | `Leica Q2 007 Edition` | `Body` | `Leica Body` | `Q` | `Q2` | `pass` | existing body pass preserved |
| `summicron sl 35` | Lens Guardrail Queries | `신품 Leica SL 35mm f2 Summicron ASPH Black` | `Lens` | `SL Lens` | `SL` | `Summicron-SL` | `신품 Leica SL 35mm f2 Summicron ASPH Black` | `Lens` | `SL Lens` | `SL` | `Summicron-SL` | `pass` | body fix did not contaminate lens query |
| `Leica 35mm F2 AsphSummicron SL` | Lens Guardrail Queries | `신품 Leica SL 35mm f2 Summicron ASPH Black` | `Lens` | `SL Lens` | `SL` | `Summicron-SL` | `신품 Leica SL 35mm f2 Summicron ASPH Black` | `Lens` | `SL Lens` | `SL` | `Summicron-SL` | `pass` | body fix did not contaminate lens query |
| `apo summicron sl 35` | Lens Guardrail Queries | `신품 Leica SL 35mm f2 Summicron ASPH Black` | `Lens` | `SL Lens` | `SL` | `Summicron-SL` | `신품 Leica SL 35mm f2 Summicron ASPH Black` | `Lens` | `SL Lens` | `SL` | `Summicron-SL` | `weak_pass` | body-safe, but APO family ranking is still weak |
| `sl 24-90` | Lens Guardrail Queries | `Sigma L 30mm f1.4 DC DN Black for CL, TL2, etc` | `Lens` | `SL Lens` | `SL` | - | `Sigma L 30mm f1.4 DC DN Black for CL, TL2, etc` | `Lens` | `SL Lens` | `SL` | - | `weak_pass` | body-safe, but SL zoom family recall remains weak |
| `sl3 battery` | Accessory Guardrail Queries | - | - | - | - | - | - | - | - | - | - | `weak_pass` | still no-result; body contamination avoided but accessory recall remains weak |
| `leica hood 12585` | Accessory Guardrail Queries | `Leica 12585 Hood for M-50mm, 35mm` | `Accessory` | `Accessory` | `M` | - | `Leica 12585 Hood for M-50mm, 35mm` | `Accessory` | `Accessory` | `M` | - | `pass` | body fix did not contaminate accessory query |
| `hood 12549` | Accessory Guardrail Queries | `Leica 12549 Hood Silver [for M 50mm f2.8 Elmar]` | `Accessory` | `Accessory` | `M` | `Elmar` | `Leica 12549 Hood Silver [for M 50mm f2.8 Elmar]` | `Accessory` | `Accessory` | `M` | `Elmar` | `pass` | body fix did not contaminate accessory query |
| `m adapter l` | Accessory Guardrail Queries | `Leica M-L adapter Black` | `Accessory` | `Accessory` | `M` | - | `Leica M-L adapter Black` | `Accessory` | `Accessory` | `M` | - | `pass` | body fix did not contaminate accessory query |
| `leica m strap` | Accessory Guardrail Queries | `Leica M 50mm f2.8 Elmar Black` | `Lens` | `M Lens` | `M` | `Elmar` | `Leica M 50mm f2.8 Elmar Black` | `Lens` | `M Lens` | `M` | `Elmar` | `weak_pass` | still ranks lens above strap accessory; body contamination avoided |

상세 per-query 기록은 [p3_body_query_recall_v0.jsonl](/Users/changdaepark/Desktop/LEICA%20SEARCH/data/admin/p3_body_query_recall_v0.jsonl)에 남겼다.

## 5. Guardrail 결과

### Lens guardrail

- `summicron sl 35`
- `Leica 35mm F2 AsphSummicron SL`
- `apo summicron sl 35`
- `sl 24-90`
- `sl 14-24`
- `sl 16-35`
- `sl 90-280`
- `35 lux`
- `50 lux`

결론:

- 이번 body recall 보정 이후에도 body contamination은 발생하지 않았다.
- 다만 `apo summicron sl 35`, `sl 24-90`, `sl 14-24`, `sl 16-35`, `sl 90-280`는 여전히 family ranking / recall 후속이 남는다.

### Accessory guardrail

- `leica hood 12585`
- `hood 12549`
- `m adapter l`

는 그대로 Accessory 유지.

- `sl3 battery`
- `leica m strap`

은 여전히 accessory recall / ranking 후속이 남지만, 이번 라운드 이후 Body로 오염되지는 않았다.

### Existing body pass guardrail

- `leica iiif`
- `barnack iiif`
- `leica q2`

는 기존 pass 상태를 그대로 유지했다.

## 6. 수정하지 않은 파일 / 영역

이번 라운드에서 아래는 수정하지 않았다.

- [classifier_v2.py](/Users/changdaepark/Desktop/LEICA%20SEARCH/classifier_v2.py)
- [model_detector.py](/Users/changdaepark/Desktop/LEICA%20SEARCH/model_detector.py)
- [normalization_admin.py](/Users/changdaepark/Desktop/LEICA%20SEARCH/normalization_admin.py)
- [normalized_latest.json](/Users/changdaepark/Desktop/LEICA%20SEARCH/data/normalized/normalized_latest.json)
- [sold_items.json](/Users/changdaepark/Desktop/LEICA%20SEARCH/data/sold_items.json)
- [results.json](/Users/changdaepark/Desktop/LEICA%20SEARCH/results.json)
- root `results.json` write pass 없음
- `data/admin/entities/*.json`
- [canonical_entities_index.json](/Users/changdaepark/Desktop/LEICA%20SEARCH/data/admin/canonical_entities_index.json)
- [canonical_seed_status.md](/Users/changdaepark/Desktop/LEICA%20SEARCH/data/admin/canonical_seed_status.md)

## 7. 남은 후속

이번 라운드에서 일부러 고치지 않은 backlog:

- `P3-query-ranking`
  - `apo summicron sl 35`
  - `sl 24-90`
  - `sl 14-24`
  - `sl 16-35`
  - `sl 90-280`

- `P3-accessory-search-ranking`
  - `sl3 battery`
  - `leica m strap`

- `P3-broad-alias-control`
- `P3-R-lens-query-recall`
- `P3-no-result-recall`

이번 라운드에서는 `SL zoom family recall`, `broad alias control`, `accessory ranking`, `R lens recall`은 건드리지 않았다.

## 8. 결론

이번 라운드의 핵심 목표였던 body query recall은 좁게 안정화됐다.

- `leica sl2` -> `Body / SL Body / SL / SL2`
- `leica sl3` -> `Body / SL Body / SL / SL3`
- `leica m10 body` -> `Body / M Body / M / M10`

그리고 중요한 guardrail도 지켜졌다.

- Barnack / Q body query 유지
- SL lens query body contamination 없음
- accessory query body contamination 없음

다음 추천 backlog는 두 갈래다.

1. `P3-query-ranking`  
   SL zoom / APO-SL 35 family ranking 약점 정리

2. `P3-accessory-search-ranking`  
   `sl3 battery`, `leica m strap`처럼 accessory recall이 아직 약한 query 정리
