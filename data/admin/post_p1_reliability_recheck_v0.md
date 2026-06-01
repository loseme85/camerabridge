# Post-P1 Reliability Recheck v0

Last updated: 2026-05-25

## 1. 목적

- P1 처리 이후 현재 classifier 기준으로 문제가 실제로 해소됐는지 확인한다.
- 이번 라운드는 수정 라운드가 아니라 재점검 라운드다.
- stored output과 current classifier output을 비교해서 `stale output`과 `current classifier issue`를 분리한다.

## 2. 기준선

- 기초 기준선 1.0
- 검색 신뢰도 점검표 v0
- 새 이름 접수함 / 분류 검토함 v0
- `active seeded families`: `51`
- `deferred / audit-only families`: `33`
- `explicit future hold candidates`: `2`
- `golden_set.py`: `132/132`

## 3. 재점검 방식

- 기존 저장 산출물:
  - `data/normalized/normalized_latest.json`
  - `results.json`
  - `data/sold_items.json`
- 현재 classifier 출력:
  - `classifier_v2.py` 직접 실행 결과
- 비교 항목:
  - `category`
  - `label`
  - `mount`
  - `model_canonical`
  - `focal_length`
- 핵심 판정:
  - `stale_output_artifact`
  - `resolved_by_current_classifier`
  - `needs_followup`
  - `current_classifier_issue`

이번 재점검에서는 코드/seed/index/tracker는 수정하지 않았고, 보고서 파일만 생성했다.

## 4. P1 대표 title 재점검 결과

| title | source file | stored category | stored label | stored mount | current category | current label | current mount | current model_canonical | result status | note |
|---|---|---|---|---|---|---|---|---|---|---|
| `Used Leica Summicron-SL 35mm f/2 ASPH` | `data/normalized/normalized_latest.json` | `Accessory` | `-` | `Accessory` | `Lens` | `SL Lens` | `SL` | `Summicron-SL` | `stale_output_artifact` | `results.json`도 stale. `sold_items.json`는 이미 Lens. 회귀 테스트 존재. |
| `Used Leica APO-Summicron-SL 50mm f/2 ASPH` | `data/sold_items.json` | `Accessory` | `-` | `SL` | `Lens` | `SL Lens` | `SL` | `APO-Summicron` | `stale_output_artifact` | current classifier는 Lens lane 유지. 회귀 테스트 존재. |
| `Leica 35mm F2 AsphSummicron SL` | `data/normalized/normalized_latest.json` | `Accessory` | `-` | `Accessory` | `Lens` | `M Lens` | `M` | `Summicron-M` | `needs_followup` | Accessory drift는 해소됐지만 SL title이 M mount/model로 남음. P1.1 후보. |
| `[중고] SL 14-24/2.8 Vario Elmarit ASPH (Black)` | `data/normalized/normalized_latest.json` | `Lens` | `24mm Elmarit ASPH` | `M` | `Lens` | `SL Lens` | `SL` | `Super-Vario-Elmarit-SL` | `stale_output_artifact` | `results.json`도 M prime collapse. current classifier는 zoom family recall 유지. |
| `[중고] SL 16-35/3.5-4.5 Super Vario Elmar ASPH (Black)` | `data/normalized/normalized_latest.json` | `Lens` | `Vario-SL` | `M` | `Lens` | `SL Lens` | `SL` | `Super-Vario-Elmar-SL` | `stale_output_artifact` | `results.json`는 `50mm Elmar-M ASPH`까지 붕괴. current classifier는 SL zoom으로 복원. |
| `[위탁] SL 24-90/2.8-4 Vario Elmar ASPH (Black)` | `data/normalized/normalized_latest.json` | `Lens` | `24mm Elmar-M` | `SL` | `Lens` | `SL Lens` | `SL` | `Vario-Elmarit-SL` | `stale_output_artifact` | stored label drift만 남음. current classifier는 family recall 유지. |
| `[중고] SL APO Vario Elmarit 90-280 f/2.8-4` | `data/normalized/normalized_latest.json` | `Lens` | `Elmarit` | `M` | `Lens` | `SL Lens` | `SL` | `APO-Vario-Elmarit-SL` | `stale_output_artifact` | 90-280도 stale output 쪽에서 M drift. current classifier는 SL tele zoom으로 유지. |
| `Leica SL2 Black` | `data/normalized/normalized_latest.json` | `Lens` | `Leica SL2` | `SL` | `Body` | `SL Body` | `SL` | `SL2` | `stale_output_artifact` | `results.json`, `sold_items.json`도 stale. current classifier와 회귀 테스트는 Body. |
| `Leica SL3 Black` | `data/normalized/normalized_latest.json` | `Lens` | `Leica SL3` | `SL` | `Body` | `SL Body` | `SL` | `SL3` | `stale_output_artifact` | `results.json`도 stale. current classifier와 회귀 테스트는 Body. |
| `Leica Barnack IIIF Silver` | `data/normalized/normalized_latest.json` | `Lens` | `Leica Barnack` | `L` | `Body` | `L Body` | `L` | `IIIf` | `stale_output_artifact` | current classifier는 이미 Barnack body로 정상. |
| `Leica Barnack IIIg Silver` | `data/normalized/normalized_latest.json` | `Lens` | `Leica Barnack` | `L` | `Body` | `L Body` | `L` | `IIIg` | `stale_output_artifact` | current classifier는 이미 Barnack body로 정상. |
| `Leica R 180mm f3.4 APO-Telyt Black` | `data/normalized/normalized_latest.json` | `Lens` | `180mm APO-Telyt` | `M` | `Lens` | `R Lens` | `R` | `APO-Telyt-R` | `stale_output_artifact` | `results.json`는 blank label + M drift. current classifier는 정상. |
| `LEICA 180mm F3.4 APO-TELYT-R` | `current_classifier_only` | `-` | `-` | `-` | `Lens` | `R Lens` | `R` | `APO-Telyt-R` | `resolved_by_current_classifier` | stored dataset hit 없음. current classifier와 회귀 테스트는 정상. |
| `[위탁] R 180/3.4 APO-Telyt (Black)` | `current_classifier_only` | `-` | `-` | `-` | `Lens` | `R Lens` | `R` | `APO-Telyt-R` | `resolved_by_current_classifier` | stored dataset hit 없음. current classifier와 회귀 테스트는 정상. |
| `Leica 12549 Hood Silver [for M 50mm f2.8 Elmar]` | `data/normalized/normalized_latest.json` | `Lens` | `50mm Elmar f2.8` | `M` | `Accessory` | `Accessory` | `M` | `Elmar` | `stale_output_artifact` | P2 accessory-token 대표 stale 사례. current classifier는 정답. |
| `Leica 12475 Hood Black for M 50mm F1.2 Noctilux ASPH` | `data/normalized/normalized_latest.json` | `Lens` | `75mm Noctilux f1.25` | `M` | `Accessory` | `Accessory` | `M` | `Noctilux` | `stale_output_artifact` | P2 accessory-token 대표 stale 사례. current classifier는 정답. |
| `Used Leica SL3 - Extra Battery` | `data/sold_items.json` | `Lens` | `-` | `SL` | `Accessory` | `Accessory` | `SL` | `SL3` | `stale_output_artifact` | P2로 넘길 battery case. current classifier는 정답. |
| `Used Leica Multifunctional Handgrip HG-SCL7 for SL3` | `data/sold_items.json` | `Lens` | `-` | `SL` | `Accessory` | `Accessory` | `SL` | `If` | `stale_output_artifact` | `results.json`는 Accessory지만 stale mount/label 흔적 존재. current classifier는 정답. |

## 5. P1 라운드별 결론

### SL lens / accessory drift

- 현재 classifier 기준 상태:
  - `Used Leica Summicron-SL 35mm f/2 ASPH`와 `Used Leica APO-Summicron-SL 50mm f/2 ASPH`는 Lens lane으로 복구되어 있다.
- stale output 여부:
  - 예. `normalized_latest.json`, `results.json`, `sold_items.json`에 stale Accessory 흔적이 남아 있다.
- 남은 follow-up 여부:
  - `Leica 35mm F2 AsphSummicron SL`은 Accessory drift는 해소됐지만 SL title이 `M Lens / Summicron-M`으로 남아서 `P1.1` 후속 후보다.

### SL zoom collapse

- 현재 classifier 기준 상태:
  - `14-24`, `16-35`, `24-90`, `90-280` 모두 `Lens / SL`로 유지되고, family recall도 복구되어 있다.
- stale output 여부:
  - 예. stored output에는 `M` mount, prime label, generic label collapse가 남아 있다.
- 남은 follow-up 여부:
  - 현재 representative title 기준 major issue는 닫힘.
  - 다만 전체 데이터에는 `14-24`, `16-35`, `24-90`, `90-280` 패턴의 stale rows가 아직 다수 남아 있으므로 regeneration 필요.

### Body recall missing

- 현재 classifier 기준 상태:
  - `Leica SL2 Black`, `Leica SL3 Black`, `Leica Barnack IIIF Silver`, `Leica Barnack IIIg Silver` 모두 Body로 나온다.
- stale output 여부:
  - 예. stored output에는 여전히 `Lens`와 blank label 흔적이 남아 있다.
- 남은 follow-up 여부:
  - representative title 기준 current classifier issue는 닫힘.

### R tele mount drift

- 현재 classifier 기준 상태:
  - `Leica R 180mm f3.4 APO-Telyt Black`, `LEICA 180mm F3.4 APO-TELYT-R`, `[위탁] R 180/3.4 APO-Telyt (Black)`는 모두 `Lens / R mount`다.
- stale output 여부:
  - 예. stored output의 `Leica R 180mm f3.4 APO-Telyt Black`는 `mount=M` drift가 남아 있다.
- 남은 follow-up 여부:
  - representative title 기준 current classifier issue는 닫힘.

## 6. 남은 P1.1 후보

현재 명확한 `P1.1` 후보는 아래 한 건이다.

- `Leica 35mm F2 AsphSummicron SL`

설명:

- Lens lane에는 남아 있다.
- 하지만 current classifier 기준으로도 `mount=M`, `model_canonical=Summicron-M`으로 남는다.
- 즉 `Accessory` 문제는 닫혔지만, `SL vs M mount/model drift`가 남아 있다.
- 이번 라운드에서는 수정하지 않고 `P1.1` 후보로만 기록한다.

## 7. P2로 넘길 항목

다음 항목은 P1 major fix가 아니라 `P2 accessory-token guardrail` 레이어에서 다루는 게 적절하다.

- `Leica 12549 Hood Silver [for M 50mm f2.8 Elmar]`
- `Leica 12475 Hood Black for M 50mm F1.2 Noctilux ASPH`
- `Used Leica SL3 - Extra Battery`
- `Used Leica Multifunctional Handgrip HG-SCL7 for SL3`

판단:

- current classifier에서는 이미 대부분 맞다.
- 그러나 stored output에는 Lens lane/blank label stale 흔적이 남아 있다.
- 따라서 taxonomy나 seed 이슈가 아니라 regeneration + P2 guardrail 운영 문제로 보는 것이 맞다.

## 8. 결론

- `P1 major fixes`는 representative title 기준으로 거의 닫혔다.
- `current_classifier_issue`로 남은 대표 케이스는 보이지 않았고,
  실질적인 후속은 `Leica 35mm F2 AsphSummicron SL` 한 건의 `P1.1` mount/model drift다.
- 따라서 다음 단계는 `P2 accessory-token guardrail`로 넘어가도 된다.
- 다만 `normalized output regeneration`은 필요하다.
  - 이유:
    - stored output에 stale Accessory/Lens drift, stale mount drift, stale body misclassification이 광범위하게 남아 있다.
- 다음 추천 작업 단위:
  - `P1.1-SL-SUMMICRON-STRING-DRIFT`
  - `P2-ACCESSORY-TOKEN-GUARDRAIL`
  - `POST-P1-REGEN-VALIDATION`
