# Post-P1 Output Regeneration v0

## 1. 목적

- P1 처리 이후 저장 산출물에 남아 있는 stale output을 current classifier 기준으로 갱신할 수 있는지 확인했다.
- 이번 라운드는 수동 hot patch가 아니라 **공식 pipeline 재생성 가능 여부 점검**과 **실행 제약 기록** 라운드다.
- 결론부터 말하면, 이번 repo 상태에서는 세 대상 파일을 **허용 범위 안에서 공식 로컬 재생성 경로만으로 안전하게 다시 쓰는 엔트리포인트를 확인하지 못했다.**

## 2. 재생성 대상

| 파일 | 재생성 가능 여부 | 사용한 script / command | 변경 여부 | 사유 |
| --- | --- | --- | --- | --- |
| `results.json` | 보류 | 실행 안 함 | 변경 없음 | current codebase에서 root `results.json`를 직접 쓰는 공식 writer를 확인하지 못했다. `app/test.py`는 완료 로그에서 `results.json`을 언급하지만 실제 write 확인 경로는 `data/raw/results.json`였다. |
| `data/normalized/normalized_latest.json` | 보류 | 실행 안 함 | 변경 없음 | `app/test.py`의 `crawl_all()` 안에서 공식 writer를 확인했지만, live crawl과 함께 `data/raw/raw_*.json`, `data/raw/results.json`, `data/normalized/normalized_*.json`, `data/derived/*`, `crawler/sessions/crawl_sessions.json`까지 함께 갱신한다. 이번 라운드 허용 범위를 넘는다. |
| `data/sold_items.json` | 보류 | 실행 안 함 | 변경 없음 | `app/test.py`의 crawl-bound sold tracking 안에서만 공식 writer를 확인했다. local cached raw data만 받아 sold lane만 재생성하는 별도 공식 엔트리포인트는 찾지 못했다. |

## 3. 사용한 pipeline / command

이번 라운드에서는 **inspection만 수행했고 regeneration command는 실행하지 않았다.**

확인에 사용한 명령:

- `rg -n "normalized_latest|sold_items|results.json|data/raw/results.json|final_resolution_pipeline|classify_listing_v2" /Users/changdaepark/Desktop/LEICA SEARCH`
- `sed -n '2750,2915p' /Users/changdaepark/Desktop/LEICA SEARCH/app/test.py`
- `sed -n '2960,3325p' /Users/changdaepark/Desktop/LEICA SEARCH/app/test.py`
- `sed -n '1,260p' /Users/changdaepark/Desktop/LEICA SEARCH/final_resolution_pipeline.py`
- `ls -la /Users/changdaepark/Desktop/LEICA SEARCH/data/raw`
- `ls -la /Users/changdaepark/Desktop/LEICA SEARCH/data/normalized`

확인 결과:

- `app/test.py`의 `crawl_all()`이 `data/normalized/normalized_latest.json`, `data/sold_items.json`, `data/raw/results.json`를 갱신하는 **공식 메인 경로**다.
- 하지만 이 경로는 live crawl, raw snapshot 생성, derived 산출물 갱신, 세션 로그 갱신을 동반한다.
- `final_resolution_pipeline.py`는 `data/raw/results.json`을 입력으로 `data/derived/results_classified_v2.json`, `data/derived/results_resolved_v2.json`, search index를 생성하는 **후처리 경로**이며, 이번 라운드 대상 파일 셋은 직접 쓰지 않는다.
- root `results.json`에 대해서는 현재 코드에서 명시적인 official writer를 찾지 못했다.

## 4. 재생성 전후 대표 title 검증

아래 표의 `after` 값은 **current production classifier 기준 기대 출력**이다. 이번 라운드에서는 공식 regeneration command를 실행하지 않았으므로, 저장 파일의 실제 값은 그대로 남아 있다.

| title | source file | before category | before label | before mount | after category | after label | after mount | after model_canonical | status | note |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `Used Leica Summicron-SL 35mm f/2 ASPH` | `data/normalized/normalized_latest.json` | `Accessory` | `-` | `Accessory` | `Lens` | `SL Lens` | `SL` | `Summicron-SL` | `not_regenerated_still_stale` | normalized_latest/results remain stale Accessory; sold_items is already Lens. |
| `Used Leica APO-Summicron-SL 50mm f/2 ASPH` | `data/sold_items.json` | `Accessory` | `-` | `SL` | `Lens` | `SL Lens` | `SL` | `APO-Summicron` | `not_regenerated_still_stale` | Current classifier keeps the title in Lens lane; stale sold output still marks it as Accessory. |
| `Leica 35mm F2 AsphSummicron SL` | `data/normalized/normalized_latest.json` | `Accessory` | `-` | `Accessory` | `Lens` | `M Lens` | `M` | `Summicron-M` | `not_regenerated_still_stale` | Accessory drift is gone, but current classifier still leaves SL title on M mount/model. |
| `[중고] SL 14-24/2.8 Vario Elmarit ASPH (Black)` | `data/normalized/normalized_latest.json` | `Lens` | `24mm Elmarit ASPH` | `M` | `Lens` | `SL Lens` | `SL` | `Super-Vario-Elmarit-SL` | `not_regenerated_still_stale` | Stored output still shows M-prime collapse; current classifier restores SL zoom family recall. |
| `[중고] SL 16-35/3.5-4.5 Super Vario Elmar ASPH (Black)` | `data/normalized/normalized_latest.json` | `Lens` | `Vario-SL` | `M` | `Lens` | `SL Lens` | `SL` | `Super-Vario-Elmar-SL` | `not_regenerated_still_stale` | results.json still contains a stronger M-prime collapse variant; current classifier is correct. |
| `[위탁] SL 24-90/2.8-4 Vario Elmar ASPH (Black)` | `data/normalized/normalized_latest.json` | `Lens` | `24mm Elmar-M` | `SL` | `Lens` | `SL Lens` | `SL` | `Vario-Elmarit-SL` | `not_regenerated_still_stale` | Current classifier preserves SL standard zoom recall; stored labels remain stale. |
| `[중고] SL APO Vario Elmarit 90-280 f/2.8-4` | `data/normalized/normalized_latest.json` | `Lens` | `Elmarit` | `M` | `Lens` | `SL Lens` | `SL` | `APO-Vario-Elmarit-SL` | `not_regenerated_still_stale` | Stored rows still show generic label and M drift; current classifier is already correct. |
| `Leica SL2 Black` | `data/normalized/normalized_latest.json` | `Lens` | `Leica SL2` | `SL` | `Body` | `SL Body` | `SL` | `SL2` | `not_regenerated_still_stale` | normalized_latest, results, and sold_items still show stale Lens rows; current classifier now returns Body. |
| `Leica SL3 Black` | `data/normalized/normalized_latest.json` | `Lens` | `Leica SL3` | `SL` | `Body` | `SL Body` | `SL` | `SL3` | `not_regenerated_still_stale` | normalized_latest and results remain stale Lens rows; current classifier now returns Body. |
| `Leica Barnack IIIF Silver` | `data/normalized/normalized_latest.json` | `Lens` | `Leica Barnack` | `L` | `Body` | `L Body` | `L` | `IIIf` | `not_regenerated_still_stale` | Current classifier already classifies Barnack IIIF as Body; stored rows are stale. |
| `Leica Barnack IIIg Silver` | `data/normalized/normalized_latest.json` | `Lens` | `Leica Barnack` | `L` | `Body` | `L Body` | `L` | `IIIg` | `not_regenerated_still_stale` | Current classifier already classifies Barnack IIIg as Body; stored rows are stale. |
| `Leica R 180mm f3.4 APO-Telyt Black` | `data/normalized/normalized_latest.json` | `Lens` | `180mm APO-Telyt` | `M` | `Lens` | `R Lens` | `R` | `APO-Telyt-R` | `not_regenerated_still_stale` | results.json still has blank label + M drift; current classifier returns R Lens. |
| `LEICA 180mm F3.4 APO-TELYT-R` | `current_classifier_only` | `-` | `-` | `-` | `Lens` | `R Lens` | `R` | `APO-Telyt-R` | `not_found_in_stored_outputs` | Representative R tele title was not found in stored datasets but current classifier output is correct. |
| `[위탁] R 180/3.4 APO-Telyt (Black)` | `current_classifier_only` | `-` | `-` | `-` | `Lens` | `R Lens` | `R` | `APO-Telyt-R` | `not_found_in_stored_outputs` | Representative Chungmuro-style R tele title was not found in stored datasets but current classifier output is correct. |
| `Leica 12549 Hood Silver [for M 50mm f2.8 Elmar]` | `data/normalized/normalized_latest.json` | `Lens` | `50mm Elmar f2.8` | `M` | `Accessory` | `Accessory` | `M` | `Elmar` | `not_regenerated_still_stale` | Current classifier is already correct; stored output still promotes the hood as a lens. |
| `Leica 12475 Hood Black for M 50mm F1.2 Noctilux ASPH` | `data/normalized/normalized_latest.json` | `Lens` | `75mm Noctilux f1.25` | `M` | `Accessory` | `Accessory` | `M` | `Noctilux` | `not_regenerated_still_stale` | Current classifier is already correct; stored output still collapses the hood into a lens family. |
| `Used Leica SL3 - Extra Battery` | `data/sold_items.json` | `Lens` | `-` | `SL` | `Accessory` | `Accessory` | `SL` | `SL3` | `not_regenerated_still_stale` | Current classifier is already correct; sold output still leaves the battery in Lens lane. |
| `Used Leica Multifunctional Handgrip HG-SCL7 for SL3` | `data/sold_items.json` | `Lens` | `-` | `SL` | `Accessory` | `Accessory` | `SL` | `If` | `not_regenerated_still_stale` | results.json is already Accessory but sold output is stale Lens; current classifier is correct. |

## 5. stale output 해소 여부

### SL lens / accessory drift

- current classifier 기준으로는 `Used Leica Summicron-SL 35mm f/2 ASPH`, `Used Leica APO-Summicron-SL 50mm f/2 ASPH`가 Lens lane에 남는다.
- 하지만 공식 regeneration command를 이번 제약 안에서 실행하지 못했으므로 stored stale output은 그대로다.
- `Leica 35mm F2 AsphSummicron SL`은 Accessory drift는 벗어났지만 current classifier 기준으로도 `M Lens / Summicron-M / mount=M`이라서 별도 P1.1 후보로 남긴다.

### SL zoom collapse

- current classifier 기준으로 `14-24`, `16-35`, `24-90`, `90-280` 대표 title은 모두 `Lens / SL mount`로 정상이다.
- stored output에서는 여전히 `M` drift 또는 prime-like label collapse가 남아 있다.
- regeneration은 미실행 상태라 stale 해소는 0건이다.

### Body recall missing

- `Leica SL2 Black`, `Leica SL3 Black`, `Leica Barnack IIIF Silver`, `Leica Barnack IIIg Silver`는 current classifier 기준 `Body`가 맞다.
- stored output은 여전히 Lens lane 흔적이 남아 있다.
- Barnack 계열은 current classifier가 이미 맞지만, 저장 산출물 재생성이 없어서 stale가 유지된다.

### R tele mount drift

- `Leica R 180mm f3.4 APO-Telyt Black`는 current classifier 기준 `Lens / R mount`가 맞다.
- `LEICA 180mm F3.4 APO-TELYT-R`, `[위탁] R 180/3.4 APO-Telyt (Black)`는 current classifier-only representative title로, 저장 산출물에서 직접 대응 row를 확인하지 못했다.
- stored stale 문제는 대표 `Leica R 180mm f3.4 APO-Telyt Black`에 그대로 남아 있다.

### P2 accessory-token candidates

- `Leica 12549 Hood ...`, `Leica 12475 Hood ...`, `Used Leica SL3 - Extra Battery`, `Used Leica Multifunctional Handgrip ...`는 current classifier 기준 Accessory가 맞다.
- stored output에서는 Lens lane 흔적이 남아 있다.
- 이번 라운드에서는 P2 guardrail 추가가 아니라 regeneration 가능 여부만 점검했다.

## 6. 남은 문제

- **P1.1 후보 유지:** `Leica 35mm F2 AsphSummicron SL`
  - Lens는 맞지만 current classifier 기준으로도 `M Lens / Summicron-M / mount=M` drift가 남아 있다.
  - 이번 라운드에서는 수정하지 않았다.
- **P2 후보 유지:** accessory-token false positive 4건
- **regeneration으로 해결되지 않은 항목:** 이번 라운드에서는 공식 로컬 재생성 엔트리포인트를 확인하지 못해 실제 regeneration을 수행하지 못했다.
- **data source 자체에 없어서 확인하지 못한 항목:** `LEICA 180mm F3.4 APO-TELYT-R`, `[위탁] R 180/3.4 APO-Telyt (Black)`는 stored outputs에서 직접 대응 row를 찾지 못했다.

## 7. 결론

- 이번 round에서 저장 산출물을 current classifier 기준으로 **실제 갱신하지는 못했다.**
- 이유는 단순하다:
  - target files를 쓰는 공식 경로가 crawl-bound `app/test.py`에 묶여 있고,
  - 그 경로는 이번 라운드 허용 범위를 넘는 추가 산출물까지 함께 갱신하며,
  - root `results.json`의 공식 writer도 현 코드에서 분명히 확인되지 않았다.
- 따라서 **P1 stale output은 아직 해소되지 않았다.**
- 다음 추천 작업은 둘 중 하나다.
  1. crawl-bound 공식 경로 실행을 명시적으로 허용하고 관련 산출물 범위를 함께 열기
  2. `data/raw/results.json`을 입력으로 `results.json`, `normalized_latest.json`, `sold_items.json`만 다시 쓰는 **공식 local-only regeneration entrypoint**를 먼저 분리
- 분류 품질 자체는 대체로 닫혀 있으므로, 구조 정리가 끝나면 우선순위는 `P1.1-SL-STRING-DRIFT`와 `P2 accessory-token guardrail` 중에서 선택하면 된다.
