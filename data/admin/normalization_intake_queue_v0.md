# 새 이름 접수함 / 분류 검토함 v0

Last updated: 2026-05-25

## 1. 목적

이 문서는 `검색 신뢰도 점검표 v0`에서 발견된 문제 후보를 구조화해서 모으는 운영 문서다.

중요한 원칙:

- 이번 라운드는 수정 라운드가 아니다
- 기초 기준선 1.0을 바로 다시 열지 않는다
- seed, alias, classifier, 검색 로직을 바로 건드리지 않는다
- 먼저 접수하고, 작은 수정 라운드로 나눠 처리한다

즉 이 문서는 “무엇을 고칠까”보다 “무엇을 먼저 검토할까”를 정하는 접수/검토 레이어다.

## 2. 기준선

이 접수함은 아래 기준선 위에서 운영된다.

- 기초 기준선 1.0
- 검색 신뢰도 점검표 v0
- `active seeded families`: `51`
- `deferred / audit-only families`: `33`
- `future hold candidates`: `2`
- `golden_set.py`: `132/132`

운영 원칙:

- taxonomy는 접수함을 통해서만 다시 열 수 있다
- closed hypothesis는 raw title이 다시 나타나도 바로 family로 부활시키지 않는다
- P1부터 작은 수정 라운드 단위로 처리한다

## 3. 접수 상태 모델

접수 상태는 아래 다섯 단계로 운영한다.

- `발견됨`
  - 문제 흔적이 관찰되었지만 아직 수정 후보로 승격하지 않은 상태
- `후보`
  - 다음 수정 라운드에서 다룰 가치가 충분한 상태
- `검토됨`
  - 관련 source, boundary, 재현 경로를 확인한 상태
- `승인됨`
  - 수정 라운드에 넣기로 확정된 상태
- `닫힘`
  - unsupported hypothesis이거나 이미 다른 기준 상품군으로 해소된 상태

이번 v0에서는:

- P1 / P2는 주로 `후보`
- closed hypothesis 감시 항목은 `발견됨`
- `승인됨`은 사용하지 않는다

## 4. 문제 유형 분류

이 접수함에서 사용하는 문제 유형은 아래와 같다.

- `search_missing`
  - 검색 누락
- `blank_label`
  - 미분류
- `low_confidence`
  - 확신 낮음
- `ambiguous`
  - 애매함
- `lens_accessory_boundary`
  - 렌즈/부속품 경계 문제
- `accessory_false_positive`
  - 부속품이 렌즈로 잘못 연결됨
- `lens_false_accessory`
  - 렌즈가 부속품으로 빠짐
- `broad_shorthand_collision`
  - broad shorthand 충돌
- `mount_boundary_drift`
  - mount 경계 문제
- `body_recall_missing`
  - body recall 누락
- `closed_hypothesis_reappearance`
  - closed hypothesis 재출현
- `new_family_candidate`
  - 새 기준 상품군 후보
- `zoom_family_collapse`
  - zoom family collapse

## 5. P1 접수 항목

실제 Leica lens/body 검색 누락 또는 family collapse 가능성이 높은 항목들이다.

| ID | 발견된 제목 | 현재 분류 | 의심되는 기준 상품군 | 문제 유형 | 추천 처리 |
|---|---|---|---|---|---|
| `P1-001` | `Used Leica Summicron-SL 35mm f/2 ASPH` | `Accessory`, blank label | `Summicron-SL 35` | 렌즈가 부속품으로 빠짐 | deferred family recall 검토 |
| `P1-002` | `Used Leica APO-Summicron-SL 50mm f/2 ASPH` | `Accessory` | `APO-Summicron-SL 50` | 렌즈가 부속품으로 빠짐 | sold pipeline accessory drift 점검 |
| `P1-003` | `[중고] SL 14-24/2.8 Vario Elmarit ASPH (Black)` | `24mm Elmarit ASPH`, `mount=M` | `Super-Vario-Elmarit-SL 14-24` | zoom family collapse | SL wide zoom family guard 필요 |
| `P1-004` | `[중고] SL 16-35/3.5-4.5 Super Vario Elmar ASPH (Black)` | `Vario-SL` / `35mm SL Lens` / `mount=M` 혼재 | `Super-Vario-Elmar-SL 16-35` | zoom family collapse | wide zoom title collapse 점검 |
| `P1-005` | `[위탁] SL 24-90/2.8-4 Vario Elmar ASPH (Black)` | `24mm Elmar-M` 쪽 붕괴 | `Vario-Elmarit-SL 24-90` | broad shorthand 충돌 | Elmar vs Elmarit drift 점검 |
| `P1-006` | `[중고] SL APO Vario Elmarit 90-280 f/2.8-4` | generic `Elmarit`, `mount=M` drift | `APO-Vario-Elmarit-SL 90-280` | mount 경계 문제 | SL tele zoom family specificity 강화 검토 |
| `P1-007` | `Leica SL2 Black` | blank label + `category=Lens` | `Leica SL2 Body` | body recall 누락 | body canonical recall 점검 |
| `P1-008` | `Leica SL3 Black` | blank label + `category=Lens` | `Leica SL3 Body` | body recall 누락 | body canonical recall 점검 |
| `P1-009` | `Leica Barnack IIIF Silver` | blank label + `category=Lens` | `Leica IIIF Body` | body recall 누락 | Barnack body mapping 점검 |
| `P1-010` | `Leica R 180mm f3.4 APO-Telyt Black` | blank label + `mount=M` drift | `APO-Telyt-R 180` | mount 경계 문제 | R tele family intake review |

## 6. P2 접수 항목

부속품/후드/배터리/그립 등 accessory guardrail 후보다.

| ID | 발견된 제목 | 현재 분류 | 의심되는 기준 상품군 | 문제 유형 | 추천 처리 |
|---|---|---|---|---|---|
| `P2-001` | `Leica 12549 Hood Silver [for M 50mm f2.8 Elmar]` | `50mm Elmar f2.8`, `category=Lens` | `Accessory` | 부속품이 렌즈로 잘못 연결됨 | accessory token rule 검토 |
| `P2-002` | `Leica 12475 Hood Black for M 50mm F1.2 Noctilux ASPH` | `75mm Noctilux f1.25`, `category=Lens` | `Accessory` | 부속품이 렌즈로 잘못 연결됨 | Noctilux family false positive 가드 검토 |
| `P2-003` | `Used Leica SL3 - Extra Battery` | `category=Lens` | `Accessory` | 부속품이 렌즈로 잘못 연결됨 | sold accessory lane 보정 후보 |
| `P2-004` | `Used Leica Multifunctional Handgrip HG-SCL7 for SL3` | `category=Lens` | `Accessory` | 부속품이 렌즈로 잘못 연결됨 | accessory token guardrail 후보 |

## 7. P4 감시 항목

이 항목들은 수정 후보가 아니라 closed hypothesis 재출현 감시 항목이다.

공통 원칙:

- official Leica literature 전까지 reopen 금지
- raw title 재출현만 기록
- taxonomy를 다시 열 근거로 바로 쓰지 않음

| ID | 가설명 | 상태 | 문제 유형 | 추천 처리 |
|---|---|---|---|---|
| `P4-001` | `Summicron-SL 24 family hypothesis` | `발견됨` | closed hypothesis 재출현 | official Leica literature 전까지 reopen 금지 |
| `P4-002` | `APO-Summicron-SL 24 family hypothesis` | `발견됨` | closed hypothesis 재출현 | official Leica literature 전까지 reopen 금지 |
| `P4-003` | `Summicron-SL 28 family hypothesis` | `발견됨` | closed hypothesis 재출현 | official Leica literature 전까지 reopen 금지 |

## 8. 다음 수정 라운드 추천 순서

이번 문서는 수정하지 않고, 다음 수정 라운드의 우선순위만 추천한다.

추천 순서:

1. SL lens가 accessory로 빠지는 문제
2. SL wide zoom이 M prime / generic label로 붕괴하는 문제
3. Leica body가 lens + blank label로 남는 문제
4. R tele mount boundary drift
5. accessory token false positive

## 9. 다음 라운드에서 열 수 있는 작업 단위

다음부터는 감으로 열지 않고 아래 작업 단위로 나누는 것을 권장한다.

- `P1-SL-LENS-ACCESSORY-DRIFT`
- `P1-SL-WIDE-ZOOM-COLLAPSE`
- `P1-BODY-RECALL-MISSING`
- `P1-R-TELE-MOUNT-DRIFT`
- `P2-ACCESSORY-TOKEN-GUARDRAIL`

## 10. 결론

기초 기준선 1.0은 유지한다.

이번 라운드에서 한 일은:

- 문제를 바로 고치지 않고
- 검색 실패 후보를 구조화해서
- 새 이름 접수함 / 분류 검토함으로 넣고
- 다음 수정 라운드를 작은 단위로 열 수 있게 만든 것이다

앞으로는 taxonomy를 바로 다시 열기보다:

- 접수함에 항목을 쌓고
- P1부터 순서대로
- 작은 수정 라운드로 처리하는 흐름이 기본이 된다
