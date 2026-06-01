# 검색 신뢰도 점검표 v0

Last updated: 2026-05-25

## 1. 목적

이 문서는 Camera Bridge Leica normalization의 기초 기준선 1.0이 실제 매물 데이터 위에서 얼마나 안정적으로 작동하는지 점검하는 문서다.

이번 라운드는:

- 새 seed를 추가하지 않는다
- 기준 상품군 구조를 수정하지 않는다
- alias를 바로 열지 않는다
- 코드나 classifier를 건드리지 않는다

대신 다음을 한다:

- 검색 누락 후보를 모은다
- 애매한 이름과 강제 연결 금지 표현이 실제 데이터에서 어떻게 나타나는지 본다
- 잘못 연결 가능성과 렌즈/부속품 경계 문제를 기록한다
- 다음 단계인 `새 이름 접수함 / 분류 검토함`으로 넘길 후보를 정리한다

## 2. 기준선

이 점검표는 아래 기준선을 전제로 한다.

- 기초 기준선 1.0 snapshot 문서:
  - `foundation_1_0_closeout_snapshot.md`
- tracker 기준 현재 상태:
  - `active seeded families`: `51`
  - `deferred / audit-only families`: `33`
  - `explicit future hold candidates`: `2`
- 회귀 기준:
  - `golden_set.py`: `132/132`

기초 기준선 1.0의 핵심 전제는 다음과 같다.

- 기준 상품군은 보수적으로 연다
- broad shorthand는 쉽게 강제 연결하지 않는다
- `overlay`와 `boundary`를 분리해서 다룬다
- unsupported family hypothesis는 `closed`로 남긴다

## 3. 전체 데이터 요약

이번 점검에 사용한 파일 기준 전체 매물 수는 아래와 같다.

| 데이터 파일 | 건수 | 메모 |
|---|---:|---|
| `data/normalized/normalized_latest.json` | `7,869` | 현재 정규화 결과 점검용 주력 파일 |
| `results.json` | `7,923` | raw 결과에 가까운 관찰용 파일 |
| `data/sold_items.json` | `500` | 판매완료 샘플 점검용 |

추가로 확인한 보조 수치:

- `normalized_latest.json`
  - blank label: `1,712`
  - nonblank label: `6,157`
- `results.json`
  - blank label: `2,856`
  - nonblank label: `5,067`
- `sold_items.json`
  - blank label: `327`
  - nonblank label: `173`

의미:

- 현재 정규화 결과 파일에서는 이미 많은 row가 어떤 식으로든 연결되어 있다
- 하지만 raw 관찰 파일인 `results.json`, `sold_items.json`에는 아직 `blank label`과 애매한 분류가 적지 않다
- 따라서 기초 기준선 1.0 자체보다, 실제 검색/분류 파이프라인의 후반 연결 품질을 따로 점검할 필요가 있다

## 4. 기준 상품군 연결 상태

아래 분류는 `normalized_latest.json` 기준의 **휴리스틱 점검값**이다. 현재 데이터에는 명시적 confidence 필드가 없으므로 다음 신호를 사용했다.

- `label` 존재 여부
- Leica lens/body-like title 여부
- accessory token 포함 여부
- `SL` title이 `M` mount로 떨어지는지 여부
- wide zoom title이 prime label로 붕괴하는지 여부

| 상태 그룹 | 건수 | 설명 |
|---|---:|---|
| 기준 상품군 연결됨 | `6,043` | 현재 기준 상품군으로 비교적 안정적으로 연결된 row |
| 미분류 | `0` | `normalized_latest.json` 기준 strict Leica lens/body blank row는 많지 않음 |
| 확신 낮음 | `0` | 별도 confidence 필드가 없어 strict count는 보류 |
| 애매함 | `72` | broad shorthand 또는 lens/accessory 혼합 title |
| 부속품 의심 | `1,640` | accessory category 또는 accessory token 중심 row |
| 잘못 연결 가능성 있음 | `114` | family/mount/category drift가 보이는 row |

보정 메모:

- `results.json`에는 Leica-looking blank-label 후보가 `220`건 있었다
- `sold_items.json`에는 Leica-looking blank-label 후보가 `46`건 있었다

즉, 현재 normalized output만 보면 미분류가 적어 보이지만, raw 관찰층에서는 아직 접수함으로 보내야 할 후보가 남아 있다.

## 5. 검색 누락 후보

아래는 “Leica item처럼 보이는데 현재 연결이 약하거나 잘못된” 대표 후보다.

| observed title | source file | 현재 분류 | 의심되는 기준 상품군 | 문제 유형 | 추천 처리 | 우선순위 |
|---|---|---|---|---|---|---|
| `Leica SL2 Black` | `results.json` | `label blank`, `category=Lens`, `mount=SL` | `Leica SL2 Body` | 검색 누락 | body canonical recall 점검 | `P1` |
| `Leica SL3 Black` | `results.json` | `label blank`, `category=Lens`, `mount=SL` | `Leica SL3 Body` | 검색 누락 | body canonical recall 점검 | `P1` |
| `Leica Barnack IIIF Silver` | `results.json` | `label blank`, `category=Lens`, `mount=L` | `Leica IIIF Body` | 검색 누락 | Barnack body mapping 점검 | `P1` |
| `Leica Barnack IIIg Silver` | `results.json` | `label blank`, `category=Lens`, `mount=L` | `Leica IIIg Body` | 검색 누락 | Barnack body mapping 점검 | `P1` |
| `Leica R 180mm f3.4 APO-Telyt Black` | `results.json` | `label blank`, `category=Lens`, `mount=M` | `APO-Telyt-R 180` | mount 경계 문제 | R tele family intake review | `P1` |
| `Used Leica Summicron-SL 35mm f/2 ASPH` | `normalized_latest.json` | `label blank`, `category=Accessory`, `mount=Accessory` | `Summicron-SL 35` | 렌즈/부속품 경계 문제 | SL 35 deferred family recall 점검 | `P1` |
| `Used Leica APO-Summicron-SL 50mm f/2 ASPH` | `sold_items.json` | `category=Accessory`, `mount=SL` | `APO-Summicron-SL 50` | 렌즈/부속품 경계 문제 | sold pipeline accessory drift 점검 | `P1` |
| `Leica 35mm F2 AsphSummicron SL` | `sold_items.json` | `category=Accessory`, `mount=M` | `Summicron-SL 35` | 검색 누락 | SL Summicron string normalization 점검 | `P1` |

요약:

- 현재 누락 후보는 prime taxonomy가 비어 있어서라기보다
  - body가 lens로 보이는 경우
  - SL lens가 accessory로 빠지는 경우
  - SL/R mount가 M으로 무너지는 경우
가 더 크다

## 6. 애매한 이름 후보

반복되는 애매한 이름 패턴은 아래 쪽에 모인다.

- `summicron`
- `summilux`
- `elmarit`
- `elmar`
- `apo`
- `cron`
- `lux`
- `vario`
- `telyt`

그리고 focal / zoom shorthand:

- `14-24`
- `16-35`
- `24-90`
- `21`
- `24`
- `28`
- `35`
- `50`
- `75`
- `90`

대표 관찰 예:

| observed title | 현재 상태 | 메모 |
|---|---|---|
| `Leica 50~135mm Elmar Hood` | blank / Accessory | lens word + accessory 혼합 |
| `Leica M 28-35-50mm f4 Tri-Elmar e49 신형 Black` | blank / Accessory | 실제 lens일 수 있으나 accessory lane에 있음 |
| `Leica M 16-18-21mm f4 Tri-elmar ASPH 6bit Black + Finder set` | blank / Accessory | lens + finder bundle 혼합 |
| `Leica M 135mm f4 Tele-Elmar Black` | blank / Accessory | lens title가 accessory lane에 있음 |
| `Angenieux R 180mm f2 3 APO DEM F Black` | blank / Lens | third-party / APO shorthand contamination |
| `[중고] SL APO Vario Elmarit 90-280 f/2.8-4` | connected but generic | broad `vario elmarit`가 family collapse를 유발 |

요약:

- 애매한 이름 문제는 대부분 lens title 자체가 이상해서라기보다
- `bundle / hood / finder / set / accessory token`이 같이 붙으면서 lane drift가 발생한다

## 7. 강제 연결 금지 표현 점검

아래 표는 기초 기준선 1.0에서 이미 `강제 연결 금지`로 잡아둔 표현이 실제 데이터에서 어떻게 보이는지 정리한 것이다.

| 표현 | 실제 title count | 현재 분류 경향 | 위험 유형 | 대표 title |
|---|---:|---|---|---|
| broad `summicron 24` | `0` | 현재 normalized 최신본에서는 직접 관찰 없음 | closed hypothesis 재출현 대비 | - |
| broad `leica sl 24` | `2` | 둘 다 `24-90mm Vario-Elmarit SL`로 연결 | `24mm prime`과 `24-90 zoom` 충돌 | `Leica SL 24-90mm f2.8-4 Vario-Elmarit Black` |
| broad `24 cron` | `0` | 현재 관찰 없음 | closed hypothesis 재출현 대비 | - |
| broad `summicron 28` | `0` | 현재 직접 관찰 없음 | closed SL 28 hypothesis 대비 | - |
| broad `apo summicron 24` | `0` | 현재 직접 관찰 없음 | closed APO-SL 24 hypothesis 대비 | - |
| broad `vario elmarit` | `50` | `14-24 / 24-70 / 24-90 / 90-280`가 함께 섞임 | broad shorthand 충돌 | `[중고] SL Vario Elmarit 24-90/2.8-4 ASPH.` |
| bare `14-24` | `3` | 모두 `24mm Elmarit ASPH` + `mount=M`로 무너짐 | ultra-wide zoom -> prime collapse | `[중고] SL 14-24/2.8 Vario Elmarit ASPH (Black)` |
| bare `16-35` | `8` | `Vario-SL`, `35mm SL Lens`, `mount=M` 혼재 | wide zoom -> 35mm prime-like collapse | `LEICA 16-35mm F3.5-4.5 ASPH SUPER-VARIO-ELMAR-SL sn.4689` |
| bare `24-90` | `45` | 일부는 정답, 일부는 `24mm Elmar-M` / `mount=M` drift | standard zoom -> 24mm prime collapse | `[위탁] SL 24-90/2.8-4 Vario Elmar ASPH (Black)` |

해석:

- 기초 기준선 1.0에서 broad shorthand를 막아둔 판단은 대체로 맞다
- 특히 `vario elmarit`, bare `14-24`, bare `16-35`, bare `24-90`는 바로 hard-pin하면 오분류가 커진다

## 8. SL wide 축 점검

기초 기준선 1.0에서 정리한 SL wide 축을 현재 데이터 위에 대조하면 아래와 같다.

| 축 | tracker 상태 | 관찰 결과 | 현재 리스크 |
|---|---|---|---|
| `Super-Vario-Elmarit-SL 14-24` | literature-real / deferred | `3`건 관찰, 모두 `24mm Elmarit ASPH` + `mount=M` | family collapse + mount drift |
| `Super-Vario-Elmar-SL 16-35` | active core | `8`건 관찰, `Vario-SL` / `35mm SL Lens` / `mount=M` 혼재 | label collapse |
| `Super-APO-Summicron-SL 21` | literature-real / deferred | lens row 없음, accessory hood `1`건만 관찰 | accessory contamination only |
| `APO-Summicron-SL 24` | closed | `0`건 | closed hypothesis 유지 |
| `Summicron-SL 24` | closed | `0`건 | closed hypothesis 유지 |
| `APO-Summicron-SL 28` | active core | `4`건 관찰, label은 대체로 맞으나 `mount=M` | mount boundary drift |
| `Summicron-SL 28` | closed | `0`건 | closed hypothesis 유지 |
| `APO-Summicron-SL 35` | active core | `22`건 관찰, 상대적으로 가장 안정적 | 비교적 양호 |
| `Summicron-SL 35` | literature-real / deferred | `2`건 관찰, `1`건은 body bundle, `1`건은 accessory lane | deferred recall 약함 |
| `Vario-Elmarit-SL 24-90` | active core | `45`건 관찰, 일부는 정답 / 일부는 `24mm Elmar-M` collapse | broad shorthand / Elmar vs Elmarit drift |

closeout 결론:

- `SL 24mm f/2` closed hypothesis들은 현재 데이터에서도 다시 살아나지 않았다
- 반대로 real family인 `14-24`, `16-35`, `24-90`은 실제 데이터에서 **family collapse**가 분명히 보인다
- 즉 다음 단계 우선순위는 closed hypothesis 재논의보다 **SL zoom / wide family search reliability** 쪽이 더 높다

## 9. 부속품 오분류 후보

부속품 토큰:

- `hood`
- `cap`
- `case`
- `box`
- `finder`
- `adapter`
- `filter`
- `pouch`
- `strap`
- `grip`
- `plate`
- `collar`

현재 관찰된 대표 오분류 후보:

| observed title | 현재 분류 | 의심되는 정답 | 문제 유형 | 우선순위 |
|---|---|---|---|---|
| `Leica 12549 Hood Silver [for M 50mm f2.8 Elmar]` | `50mm Elmar f2.8`, `category=Lens` | Accessory | 부속품 오분류 | `P2` |
| `신품 호환 Leica 14043 Hood Cover for M 35mm f2 Summicron, M 28mm f2.8 Elmarit` | `40mm Summicron-C`, `category=Lens` | Accessory | 부속품 오분류 | `P2` |
| `Leica 12475 Hood Black for M 50mm F1.2 Noctilux ASPH` | `75mm Noctilux f1.25`, `category=Lens` | Accessory | 부속품 오분류 | `P2` |
| `LEICA Lens Hood 12550 for M 50mm F2.8` | `Leica M5`, `category=Lens` | Accessory | 부속품 오분류 | `P2` |
| `Used Leica SL3 - Extra Battery` | `category=Lens` | Accessory | 렌즈/부속품 경계 문제 | `P2` |
| `Used Leica Multifunctional Handgrip HG-SCL7 for SL3` | `category=Lens` | Accessory | 렌즈/부속품 경계 문제 | `P2` |

반대 방향 후보도 있다:

- `Used Leica Summicron-SL 35mm f/2 ASPH`
  - 실제 lens title인데 `Accessory`로 빠짐
- `Used Leica APO-Summicron-SL 50mm f/2 ASPH`
  - 실제 lens title인데 `Accessory`로 빠짐

## 10. 새 이름 접수함으로 넘길 후보

아래 목록은 이번 라운드에서 바로 고치지 않고, `새 이름 접수함 / 분류 검토함`으로 넘길 후보다.

| observed title | source file | 현재 분류 | 의심되는 기준 상품군 | 문제 유형 | 추천 처리 | 우선순위 |
|---|---|---|---|---|---|---|
| `Used Leica Summicron-SL 35mm f/2 ASPH` | `normalized_latest.json` | `Accessory`, blank label | `Summicron-SL 35` | 렌즈/부속품 경계 문제 | deferred family recall 검토 | `P1` |
| `Used Leica APO-Summicron-SL 50mm f/2 ASPH` | `sold_items.json` | `Accessory` | `APO-Summicron-SL 50` | 렌즈/부속품 경계 문제 | sold pipeline recheck | `P1` |
| `[중고] SL 14-24/2.8 Vario Elmarit ASPH (Black)` | `normalized_latest.json` | `24mm Elmarit ASPH`, `mount=M` | `Super-Vario-Elmarit-SL 14-24` | 잘못 연결 | SL wide zoom family guard 필요 | `P1` |
| `[중고] SL 16-35/3.5-4.5 Super Vario Elmar ASPH (Black)` | `normalized_latest.json` | `Vario-SL` 또는 `35mm SL Lens`, `mount=M` | `Super-Vario-Elmar-SL 16-35` | 잘못 연결 | zoom title collapse 점검 | `P1` |
| `[위탁] SL 24-90/2.8-4 Vario Elmar ASPH (Black)` | `normalized_latest.json` | `24mm Elmar-M` | `Vario-Elmarit-SL 24-90` | broad shorthand 충돌 | Elmar vs Elmarit drift 점검 | `P1` |
| `[중고] SL APO Vario Elmarit 90-280 f/2.8-4` | `normalized_latest.json` | `Elmarit`, `mount=M` | `APO-Vario-Elmarit-SL 90-280` | mount 경계 문제 | SL tele zoom family specificity 강화 후보 | `P1` |
| `Leica SL2 Black` | `results.json` | blank label, `category=Lens` | `Leica SL2 Body` | 검색 누락 | body recall 샘플로 수집 | `P1` |
| `Leica SL3 Black` | `results.json` | blank label, `category=Lens` | `Leica SL3 Body` | 검색 누락 | body recall 샘플로 수집 | `P1` |
| `Leica Barnack IIIF Silver` | `results.json` | blank label, `category=Lens` | `Leica IIIF Body` | 검색 누락 | Barnack body lane 점검 | `P1` |
| `Leica R 180mm f3.4 APO-Telyt Black` | `results.json` | blank label, `mount=M` | `APO-Telyt-R 180` | mount 경계 문제 | R tele intake 후보 | `P1` |
| `Leica 12549 Hood Silver [for M 50mm f2.8 Elmar]` | `normalized_latest.json` | `50mm Elmar f2.8`, `category=Lens` | Accessory | 부속품 오분류 | accessory token rule 검토 | `P2` |
| `Leica 12475 Hood Black for M 50mm F1.2 Noctilux ASPH` | `normalized_latest.json` | `75mm Noctilux f1.25`, `category=Lens` | Accessory | 부속품 오분류 | accessory token rule 검토 | `P2` |
| `Used Leica SL3 - Extra Battery` | `sold_items.json` | `category=Lens` | Accessory | 부속품 오분류 | sold accessory lane 보정 후보 | `P2` |
| `Summicron-SL 24` family hypothesis | `foundation/tracker context` | closed | none | closed hypothesis 재출현 감시 | official literature 전까지 reopen 금지 | `P4` |
| `Summicron-SL 28` family hypothesis | `foundation/tracker context` | closed | none | closed hypothesis 재출현 감시 | official literature 전까지 reopen 금지 | `P4` |

## 11. 우선순위별 다음 작업

### P1

실제 검색 누락 가능성이 높고 Leica lens/body일 가능성이 높은 후보.

우선 처리 대상:

- SL lens가 accessory로 빠지는 경우
- SL wide zoom이 M family 또는 generic prime label로 붕괴하는 경우
- Leica body가 lens + blank label로 남는 경우
- R mount tele lens가 M mount나 blank label로 흔들리는 경우

권장 작업:

- `새 이름 접수함`에 먼저 등록
- source title 재수집
- raw title -> current classification -> intended family 비교
- search recall 샘플셋에 편입

### P2

애매하지만 반복되면 alias / guardrail 후보가 될 수 있는 것.

우선 처리 대상:

- hood / cap / case / handgrip / battery가 lens family로 잘못 들어간 사례
- Elmar / Elmarit / Vario naming drift
- bundle title 때문에 lane이 흔들리는 사례

권장 작업:

- accessory token dictionary 보강 후보로 수집
- bundle pattern 관찰용 태그 추가

### P3

대체로 부속품/박스/후드 성격이 강한 저우선순위 후보.

권장 작업:

- 접수함에 넣되 바로 taxonomy reopen으로 연결하지 않음
- accessory lane cleaning 후보로만 유지

### P4

closed hypothesis 또는 third-party contamination 가능성이 높은 것.

대상:

- `Summicron-SL 24`
- `APO-Summicron-SL 24`
- `Summicron-SL 28`
- 기타 official literature가 없는 parallel SL prime guesses

권장 작업:

- 재출현만 기록
- official Leica 문헌 전까지 family reopen 금지

## 12. 결론

기초 기준선 1.0 자체는 현재도 유효하다. 특히 SL wide 구조에서:

- `SL 24mm f/2` closed hypotheses는 여전히 닫아두는 쪽이 맞고
- real family인 `21 / 28 / 35 / 14-24 / 16-35 / 24-90` 축은 충분히 구분할 가치가 있다

하지만 실제 데이터에서는 taxonomy 부족보다 **검색 신뢰도 부족**이 더 먼저 보인다.

이번 점검에서 가장 큰 신호는 아래 두 가지다.

- real Leica lens/body가 accessory 또는 blank lane으로 빠지는 문제
- SL zoom / wide family가 broad shorthand 때문에 M family 또는 generic prime label로 붕괴하는 문제

즉 다음 단계는 foundation 구조를 다시 짜는 것이 아니라:

- `새 이름 접수함 / 분류 검토함`으로 후보를 모으고
- Search Reliability Report v1에서 recall / false positive / false negative를 더 정밀하게 보는 흐름이 맞다
