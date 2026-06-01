# Output Regeneration Write Pass v0

## 1. 목적

- local-only output regeneration entrypoint의 실제 `--write` 실행 결과를 admin 문서로 고정한다.
- 이번 기록은 classifier 수정이나 taxonomy 변경이 아니라, **저장 산출물 갱신 사실과 검증 상태**를 남기는 closeout note다.

## 2. 실행 명령

```bash
python3 scripts/regenerate_outputs_from_raw.py --write
```

실행 결과:

- mode: `write`
- input rows: `7869`
- wrote targets:
  - `results`: `false`
  - `normalized`: `true`
  - `sold_items`: `true`

## 3. 실제로 수정된 파일

- [normalized_latest.json](/Users/changdaepark/Desktop/LEICA%20SEARCH/data/normalized/normalized_latest.json)
- [sold_items.json](/Users/changdaepark/Desktop/LEICA%20SEARCH/data/sold_items.json)

## 4. 의도적으로 수정하지 않은 파일

- [results.json](/Users/changdaepark/Desktop/LEICA%20SEARCH/results.json)

root `results.json`은 이번 write pass에서 의도적으로 건드리지 않았다. 새 entrypoint의 기본 안전 원칙에 따라 `--write-root-results` 없이 실행했기 때문이다.

## 5. Diff Stat 요약

```text
data/normalized/normalized_latest.json | 315689 lines
data/sold_items.json | 20644 lines
2 files changed, 313898 insertions, 22435 deletions
```

이번 write pass는 개별 row hot patch가 아니라, local cached raw data를 current classifier로 다시 태운 **재생성 결과**다.

## 6. 대표 title 저장 결과 확인

- `Used Leica Summicron-SL 35mm f/2 ASPH`
  - `Lens / SL Lens / SL / Summicron-SL`

- `Used Leica APO-Summicron-SL 50mm f/2 ASPH`
  - `sold_items`에서 `Lens / SL Lens / SL / APO-Summicron`

- `Leica 35mm F2 AsphSummicron SL`
  - `Lens / M Lens / M / Summicron-M`
  - `P1.1` 후보 유지

- `[중고] SL 14-24/2.8 Vario Elmarit ASPH (Black)`
  - `Lens / SL Lens / SL / Super-Vario-Elmarit-SL`

- `[중고] SL 16-35/3.5-4.5 Super Vario Elmar ASPH (Black)`
  - `Lens / SL Lens / SL / Super-Vario-Elmar-SL`

- `[위탁] SL 24-90/2.8-4 Vario Elmar ASPH (Black)`
  - `Lens / SL Lens / SL / Vario-Elmarit-SL`

- `Leica SL2 Black`
  - `Body / SL Body / SL / SL2`

- `Leica R 180mm f3.4 APO-Telyt Black`
  - `Lens / R Lens / R / APO-Telyt-R`

- `Used Leica SL3 - Extra Battery`
  - `sold_items`에서 `Accessory / Accessory / SL / SL3`

## 7. 테스트 결과

아래 검증은 모두 통과했다.

- `test_r_tele_classification: ok`
- `test_body_classification: ok`
- `test_sl_zoom_classification: ok`
- `test_accessory_category: ok`
- `test_normalization_admin: ok`
- `test_output_regeneration_entrypoint: ok`
- `py_compile: ok`

## 8. golden_set.py 결과

- `132/132`

## 9. 남은 후속

- `P1.1-SL-STRING-DRIFT`
  - `Leica 35mm F2 AsphSummicron SL`은 Lens lane에는 남았지만, current classifier 기준으로도 `M Lens / Summicron-M / mount=M` drift가 있다.

- `P2 accessory-token guardrail`
  - 이번 write pass로 stale stored output은 상당 부분 해소됐지만, accessory token false positive 계열은 별도 guardrail 라운드로 다루는 편이 맞다.

## 10. 결론

- local-only regeneration write pass는 성공적으로 완료됐다.
- stale output 해소의 핵심 대상이었던 `normalized_latest.json`과 `sold_items.json`은 current classifier 기준으로 갱신됐다.
- root `results.json`은 안전 원칙에 따라 그대로 유지했다.
- 이제 다음 작업은 `P1.1-SL-STRING-DRIFT`를 먼저 칠지, 아니면 `P2 accessory-token guardrail`로 넘어갈지 선택하는 단계다.
