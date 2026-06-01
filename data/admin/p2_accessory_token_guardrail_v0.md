# P2 Accessory Token Guardrail v0

## 1. 목적

- accessory token false positive를 점검한다.
- hood / cap / battery / handgrip / filter / adapter / finder / strap 같은 주상품 accessory listing이 Lens 또는 Body로 잘못 승격되지 않도록 확인한다.
- 동시에 실제 lens listing에 `with hood`, `+ Finder set`, `box and hood` 같은 bundle 표현이 들어간 경우 Lens를 계속 보호한다.

이번 라운드는 taxonomy 작업이 아니라 classifier boundary 보정 라운드다. seed / alias / canonical family는 추가하지 않는다.

## 2. 점검한 대표 title

| title | group | before category | before label | before mount | after category | after label | after mount | status | note |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Leica 12549 Hood Silver [for M 50mm f2.8 Elmar] | hood/cap | Accessory | Accessory | M | Accessory | Accessory | M | already_correct | hood compatibility title kept as Accessory |
| Leica 12475 Hood Black for M 50mm F1.2 Noctilux ASPH | hood/cap | Accessory | Accessory | M | Accessory | Accessory | M | already_correct | hood compatibility title kept as Accessory |
| LEICA Lens Hood 12550 for M 50mm F2.8 | hood/cap | Accessory | Accessory | M | Accessory | Accessory | M | already_correct | explicit `Lens Hood` primary noun kept as Accessory |
| 신품 호환 Leica 14043 Hood Cover for M 35mm f2 Summicron, M 28mm f2.8 Elmarit | hood/cap | Accessory | Accessory | M | Accessory | Accessory | M | already_correct | hood cover compatibility title kept as Accessory |
| Used Leica SL3 - Extra Battery | battery/grip | Accessory | Accessory | SL | Accessory | Accessory | SL | already_correct | body compatibility hint did not override Accessory |
| Used Leica Multifunctional Handgrip HG-SCL7 for SL3 | battery/grip | Accessory | Accessory | SL | Accessory | Accessory | SL | already_correct | handgrip primary noun kept as Accessory |
| BP-SCL5 | battery/grip | Accessory | Accessory | Unknown | Accessory | Accessory | Unknown | already_correct | battery code kept as Accessory |
| Leica M10 Handgrip Black | battery/grip | Accessory | Accessory | M | Accessory | Accessory | M | already_correct | body hint kept but category stayed Accessory |
| Leica UVa II Filter M 46mm | filter/adapter/finder/strap | Accessory | Accessory | Unknown | Accessory | Accessory | Unknown | already_correct | filter title kept as Accessory |
| Leica M Adapter L | filter/adapter/finder/strap | Accessory | Accessory | M | Accessory | Accessory | M | already_correct | adapter title kept as Accessory |
| Leica M to L Adapter | filter/adapter/finder/strap | Accessory | Accessory | M | Accessory | Accessory | M | already_correct | adapter title kept as Accessory |
| Leica Visoflex II | filter/adapter/finder/strap | Accessory | Accessory | Unknown | Accessory | Accessory | Unknown | already_correct | finder accessory kept as Accessory |
| Leica Universal Finder | filter/adapter/finder/strap | Accessory | Accessory | Unknown | Accessory | Accessory | Unknown | already_correct | finder title kept as Accessory |
| Leica M 스트랩 블랙 | filter/adapter/finder/strap | Accessory | Accessory | M | Accessory | Accessory | M | already_correct | strap title kept as Accessory |
| Leica M 16-18-21mm f4 Tri-Elmar ASPH 6bit Black + Finder set | lens boundary | Lens | M Lens | M | Lens | M Lens | M | already_correct | lens + finder bundle stayed Lens |
| Leica M 28-35-50mm f4 Tri-Elmar e49 신형 Black | lens boundary | Lens | M Lens | M | Lens | M Lens | M | already_correct | pure lens listing stayed Lens |
| Leica M 35mm f2 Summicron ASPH 6bit Black with hood | lens boundary | Accessory | Accessory | M | Lens | M Lens | M | resolved_by_minimal_guardrail | integer `f2` lens signal now counts as lens-positive, so `with hood` no longer demotes the listing |
| Leica M 50mm f1.4 Summilux ASPH Black with box and hood | lens boundary | Lens | M Lens | M | Lens | M Lens | M | already_correct | lens + box/hood bundle stayed Lens |
| Used Leica Summicron-SL 35mm f/2 ASPH | lens boundary | Lens | SL Lens | SL | Lens | SL Lens | SL | already_correct | SL lens remained protected |
| Leica 35mm F2 AsphSummicron SL | lens boundary | Lens | SL Lens | SL | Lens | SL Lens | SL | already_correct | P1.1 fix remained intact |
| SL 35/2 APO Summicron ASPH Black | lens boundary | Lens | SL Lens | SL | Lens | SL Lens | SL | already_correct | APO-Summicron-SL boundary preserved |
| Leica SL2 Black | body boundary | Body | SL Body | SL | Body | SL Body | SL | already_correct | body title did not fall into Accessory |
| Leica SL3 Black | body boundary | Body | SL Body | SL | Body | SL Body | SL | already_correct | body title did not fall into Accessory |
| Leica M10 Body Black | body boundary | Body | M Body | M | Body | M Body | M | already_correct | body title did not fall into Accessory |

## 3. 수정 여부

- classifier 수정: 있음
- 테스트 추가: 있음
- 수정 범위: 최소 1건

실제 current classifier issue는 1건이었다.

- `Leica M 35mm f2 Summicron ASPH 6bit Black with hood`

이 title은 `with hood` 때문에 Accessory로 밀렸는데, 원인은 `f2` 같은 정수 조리개 표기가 렌즈 보호 신호로 충분히 잡히지 않던 점이었다. 따라서 broad accessory rule을 새로 열지 않고, 기존 렌즈 보호 신호가 `f2` / `f4` 같은 dealer shorthand도 읽도록 좁게 보정했다.

## 4. Accessory positive 결과

### hood

- `Leica 12549 Hood Silver [for M 50mm f2.8 Elmar]`
- `Leica 12475 Hood Black for M 50mm F1.2 Noctilux ASPH`
- `LEICA Lens Hood 12550 for M 50mm F2.8`
- `신품 호환 Leica 14043 Hood Cover for M 35mm f2 Summicron, M 28mm f2.8 Elmarit`

모두 `Accessory / Accessory` 유지.

### battery / handgrip

- `Used Leica SL3 - Extra Battery`
- `Used Leica Multifunctional Handgrip HG-SCL7 for SL3`
- `BP-SCL5`
- `Leica M10 Handgrip Black`

모두 `Accessory / Accessory` 유지.

### filter / adapter / finder / strap

- `Leica UVa II Filter M 46mm`
- `Leica M Adapter L`
- `Leica M to L Adapter`
- `Leica Visoflex II`
- `Leica Universal Finder`
- `Leica M 스트랩 블랙`

모두 `Accessory / Accessory` 유지.

## 5. Lens boundary 결과

- `Leica M 16-18-21mm f4 Tri-Elmar ASPH 6bit Black + Finder set` -> `Lens / M Lens / M`
- `Leica M 28-35-50mm f4 Tri-Elmar e49 신형 Black` -> `Lens / M Lens / M`
- `Leica M 35mm f2 Summicron ASPH 6bit Black with hood` -> `Lens / M Lens / M`
- `Leica M 50mm f1.4 Summilux ASPH Black with box and hood` -> `Lens / M Lens / M`
- `Used Leica Summicron-SL 35mm f/2 ASPH` -> `Lens / SL Lens / SL`
- `Leica 35mm F2 AsphSummicron SL` -> `Lens / SL Lens / SL`
- `SL 35/2 APO Summicron ASPH Black` -> `Lens / SL Lens / SL`

핵심 확인:

- hood / finder / box included 표현이 있는 실제 lens listing은 Accessory로 밀리지 않는다.
- P1.1에서 고친 `Leica 35mm F2 AsphSummicron SL`도 그대로 유지된다.
- APO-Summicron-SL 35 경계도 유지된다.

## 6. 남은 후속

- current classifier issue: 이번 대표 title 범위에서는 없음
- output regeneration: 이번 라운드에서는 실행하지 않음
- 남은 후속은 좁다:
  - 이번 classifier 보정을 저장 산출물에 반영하려면 local-only regeneration write pass를 다시 한 번 실행해야 한다.
  - 더 넓은 accessory token 라운드는 필요할 수 있지만, 현재 대표 token 세트에서는 major issue가 보이지 않았다.

## 7. 결론

- P2 accessory-token guardrail은 대표 범위 기준으로 닫을 수 있다.
- classifier는 최소 1건만 수정했다.
- 대부분의 accessory positive title은 이미 current classifier에서 올바르게 처리되고 있었다.
- 이번 라운드의 실질 수정은 `Leica M 35mm f2 Summicron ASPH 6bit Black with hood`가 Accessory로 떨어지지 않도록 한 좁은 보정이다.

다음 추천 작업:

1. 필요하면 local-only regeneration write pass를 다시 실행해서 이번 classifier 보정을 저장 산출물에 반영
2. 그 다음 더 넓은 accessory-token 확장 라운드를 열지, 아니면 다른 search reliability backlog로 넘어갈지 판단
