# Search Reliability Smoke v1
## 1. 목적
- P1/P2 이후 실제 query-level 검색 신뢰도를 확인한다.
- classifier 수정 라운드가 아니라 검색 결과 관찰 라운드다.
## 2. 사용한 검색 entrypoint
- entrypoint: `api.search.endpoint_response -> search_service.load_and_search -> data/derived/results_search_index_v1.json`
- input data: `data/derived/results_search_index_v1.json`
- top results 산출 방식: `api.search.endpoint_response`가 `search_service`와 `query_resolver`를 통해 top results를 반환하는 현재 검색 경로를 그대로 사용했다.
- 한계: 이번 smoke는 search index 기반 결과를 본다. `results.json` 직접 검색이나 UI hot patch는 하지 않았다.
## 3. Query Set
- M shorthand
- SL lens / zoom
- Accessory
- R lens
- Body
- Broad dangerous shorthand
## 4. 결과 요약
| query | group | top1 title | top1 category | top1 label | top1 mount | top1 model_canonical | status | note |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 35 lux | M shorthand | Leica M 35mm f1.4 Summilux 2nd Titan | Lens | M Lens | M | Summilux-M | `pass` | - |
| 35 cron | M shorthand | Leica M 35mm f2 APO-Summicron ASPH 6bit Black | Lens | M Lens | M | APO-Summicron | `weak_pass` | Top1은 M mount지만 APO-Summicron 35가 먼저 나온다. family drift는 있으나 M-side neighborhood는 유지된다. |
| 50 cron | M shorthand | Leica R 50mm f2 Summicron Black | Lens | R Lens | R | Summicron-R | `wrong_mount` | Top1이 R 50 Summicron으로 올라와 M shorthand 기대와 어긋난다. |
| 50 lux | M shorthand | Leica M 50mm f1.4 Summilux Classic Silver | Lens | M Lens | M | Summilux-M | `pass` | - |
| nocti e60 | M shorthand | [중고] M 50/1.0 Noctilux 3세대 E60 (Black) | Lens | M Lens | M | Noctilux | `pass` | - |
| noctilux 0.95 | M shorthand | Leica M 50mm f0.95 Noctilux ASPH 6bit Black | Lens | M Lens | M | Noctilux | `pass` | - |
| summicron 35 | M shorthand | LEICA 35mm F2 ASPH Screwmount M39 SUMMICRON-L sn.3867 | Lens | L Lens | L | Summicron | `wrong_mount` | Top1이 LTM/L screw Summicron-L로 가서 M shorthand 기대에서 빗나간다. |
| summilux 50 | M shorthand | LEICA 50mm F1.4 SUMMILUX M39 sn.3868 | Lens | L Lens | L | Summilux | `wrong_mount` | Top1이 L screw Summilux로 가서 M shorthand 기대보다 legacy L 쪽으로 치우친다. |
| 6군8매 | M shorthand | Light Lens LAB M 35mm f2 (8 element) Brass Version 1. | Lens | 3rd Party M Lens | M | - | `weak_pass` | 8-element collector shorthand는 잡지만 Leica보다 Light Lens Lab derivative가 먼저 나온다. |
| steel rim | M shorthand | - | - | - | - | - | `no_result` | query parser가 structured intent를 만들지 못해 no_result다. |
| summicron sl 35 | SL lens / zoom | 신품 Leica SL 35mm f2 Summicron ASPH Black | Lens | SL Lens | SL | Summicron-SL | `pass` | - |
| Leica 35mm F2 AsphSummicron SL | SL lens / zoom | 신품 Leica SL 35mm f2 Summicron ASPH Black | Lens | SL Lens | SL | Summicron-SL | `pass` | - |
| apo summicron sl 35 | SL lens / zoom | 신품 Leica SL 35mm f2 Summicron ASPH Black | Lens | SL Lens | SL | Summicron-SL | `wrong_family` | APO token이 intent에 반영되지 않아 non-APO Summicron-SL 35가 APO-SL 35보다 먼저 나온다. |
| sl 24-90 | SL lens / zoom | Sigma L 30mm f1.4 DC DN Black for CL, TL2, etc | Lens | SL Lens | SL | - | `wrong_family` | SL mount는 잡지만 top1이 Sigma 30mm L-mount lens라 zoom query recall이 약하다. |
| 24-90 vario elmarit | SL lens / zoom | Leica S 30mm f2.8 Elmarit ASPH CS Black | Lens | S Lens | S | Elmarit | `wrong_mount` | Top1이 S Elmarit로 가서 mount/family 모두 어긋난다. |
| sl 14-24 | SL lens / zoom | Sigma L 30mm f1.4 DC DN Black for CL, TL2, etc | Lens | SL Lens | SL | - | `wrong_family` | SL mount broadening은 되지만 specific zoom family recall이 없다. |
| sl 16-35 | SL lens / zoom | Sigma L 30mm f1.4 DC DN Black for CL, TL2, etc | Lens | SL Lens | SL | - | `wrong_family` | SL mount broadening은 되지만 specific zoom family recall이 없다. |
| sl 90-280 | SL lens / zoom | Sigma L 30mm f1.4 DC DN Black for CL, TL2, etc | Lens | SL Lens | SL | - | `wrong_family` | SL mount broadening은 되지만 tele zoom family recall이 없다. |
| leica hood 12585 | Accessory | Leica 12585 Hood for M-50mm, 35mm | Accessory | Accessory | M | - | `pass` | - |
| hood 12549 | Accessory | Leica 12549 Hood Silver [for M 50mm f2.8 Elmar] | Accessory | Accessory | M | Elmar | `pass` | - |
| bp-scl5 | Accessory | - | - | - | - | - | `no_result` | stored data에는 battery rows가 있으나 query parser/search recall이 직접 잡지 못한다. |
| sl3 battery | Accessory | - | - | - | - | - | `no_result` | body/accessory intent를 못 잡아 no_result로 끝난다. |
| m adapter l | Accessory | Leica M-L adapter Black | Accessory | Accessory | M | - | `pass` | - |
| visoflex ii | Accessory | Leica 85mm Tele Finder C. K. S. Silver | Accessory | Accessory | Unknown | - | `wrong_family` | Accessory category는 맞지만 Universal/Tele Finder가 Visoflex II보다 먼저 온다. |
| universal finder | Accessory | Leica 85mm Tele Finder C. K. S. Silver | Accessory | Accessory | Unknown | - | `wrong_family` | Accessory category는 맞지만 exact universal finder보다 tele finder generic이 먼저 온다. |
| leica m strap | Accessory | Leica M 50mm f2.8 Elmar Black | Lens | M Lens | M | Elmar | `wrong_category` | Accessory intent를 못 잡고 M lens rows가 먼저 나온다. |
| r 180 apo | R lens | Leica R 180mm f2.8 APO-Elmart Rom Black | Lens | R Lens | R | Elmar-R | `weak_pass` | R mount는 맞고 APO 180 neighborhood도 맞지만 APO-Telyt-R 180보다 APO-Elmarit 180이 먼저 온다. |
| apo telyt r 180 | R lens | Leica R 180mm f2.8 APO-Elmart Rom Black | Lens | R Lens | R | Elmar-R | `wrong_family` | Telyt intent가 반영되지 않아 APO-Telyt-R 180이 top1이 아니다. |
| r 70-180 | R lens | Leica R 50mm f2 Summicron Black | Lens | R Lens | R | Summicron-R | `wrong_family` | R mount broadening은 되지만 target zoom family recall이 없다. |
| vario apo elmarit r 70-180 | R lens | Leica R 28mm f2.8 Elmarit Rom Black | Lens | R Lens | R | Elmarit-R | `wrong_family` | query family는 맞지만 top1이 28mm Elmarit-R로 잘못 올라간다. |
| r 280 apo telyt | R lens | LEICA R280mm F2.8 APO-TELYT-R sn.3280 | Lens | R Lens | R | APO-Telyt-R | `pass` | - |
| r 90 summicron | R lens | LEICA 90mm F2 SUMMICRON-R sn.3567 | Lens | R Lens | R | Summicron-R | `pass` | - |
| leica sl2 | Body | Leica M 50mm f2.8 Elmar Black | Lens | M Lens | M | Elmar | `wrong_category` | body intent parser가 SL2 body query를 structured body query로 만들지 못한다. |
| leica sl3 | Body | Leica M 50mm f2.8 Elmar Black | Lens | M Lens | M | Elmar | `wrong_category` | body intent parser가 SL3 body query를 structured body query로 만들지 못한다. |
| leica m10 body | Body | Leica M 50mm f2.8 Elmar Black | Lens | M Lens | M | Elmar | `wrong_category` | body token이 parsing에 반영되지 않아 lens rows가 먼저 나온다. |
| leica iiif | Body | Leica Barnack IIIF Silver | Body | L Body | L | IIIf | `pass` | - |
| barnack iiif | Body | Leica Barnack IIIF Silver | Body | L Body | L | IIIf | `pass` | - |
| leica q2 | Body | Leica Q2 007 Edition | Body | Leica Body | Q | Q2 | `pass` | - |
| vario elmarit | Broad dangerous shorthand | Leica S 30mm f2.8 Elmarit ASPH CS Black | Lens | S Lens | S | Elmarit | `over_hard_pinned` | broad shorthand인데 S Elmarit 하나로 과도하게 끌린다. |
| summicron | Broad dangerous shorthand | 신품 호환 Leica 14043 Hood Cover for M 35mm f2 Summicron, M 28mm f2.8 Elmarit | Accessory | Accessory | M | Summicron | `wrong_category` | broad family query인데 hood accessory row가 top1로 올라온다. |
| lux | Broad dangerous shorthand | Leica M 28mm f1.4 Summilux ASPH 6bit Black | Lens | M Lens | M | Summilux-M | `over_hard_pinned` | broad shorthand인데 M Summilux family로 실질 hard-pin된다. |
| apo | Broad dangerous shorthand | - | - | - | - | - | `no_result` | too broad + parser miss로 no_result다. |
| 24 cron | Broad dangerous shorthand | Leica R 50mm f2 Summicron Black | Lens | R Lens | R | Summicron-R | `wrong_family` | closed-hypothesis-adjacent shorthand인데 unrelated R 50 Summicron-R가 top1이다. |
| summicron 24 | Broad dangerous shorthand | 신품 호환 Leica 14043 Hood Cover for M 35mm f2 Summicron, M 28mm f2.8 Elmarit | Accessory | Accessory | M | Summicron | `wrong_category` | broad dangerous shorthand인데 hood accessory row가 top1이다. |
| summicron sl 24 | Broad dangerous shorthand | Leica SL 50mm f2 APO-Summicron ASPH Black | Lens | SL Lens | SL | APO-Summicron | `over_hard_pinned` | closed hypothesis query인데 nearby SL Summicron/APO-Summicron rows로 흘러간다. |

## 5. 실패 / 약한 query 목록
### no_result
- `steel rim`: query parser가 structured intent를 만들지 못해 no_result다.
- `bp-scl5`: stored data에는 battery rows가 있으나 query parser/search recall이 직접 잡지 못한다.
- `sl3 battery`: body/accessory intent를 못 잡아 no_result로 끝난다.
- `apo`: too broad + parser miss로 no_result다.
### wrong_category
- `leica m strap`: Accessory intent를 못 잡고 M lens rows가 먼저 나온다.
- `leica sl2`: body intent parser가 SL2 body query를 structured body query로 만들지 못한다.
- `leica sl3`: body intent parser가 SL3 body query를 structured body query로 만들지 못한다.
- `leica m10 body`: body token이 parsing에 반영되지 않아 lens rows가 먼저 나온다.
- `summicron`: broad family query인데 hood accessory row가 top1로 올라온다.
- `summicron 24`: broad dangerous shorthand인데 hood accessory row가 top1이다.
### wrong_mount
- `50 cron`: Top1이 R 50 Summicron으로 올라와 M shorthand 기대와 어긋난다.
- `summicron 35`: Top1이 LTM/L screw Summicron-L로 가서 M shorthand 기대에서 빗나간다.
- `summilux 50`: Top1이 L screw Summilux로 가서 M shorthand 기대보다 legacy L 쪽으로 치우친다.
- `24-90 vario elmarit`: Top1이 S Elmarit로 가서 mount/family 모두 어긋난다.
### wrong_family
- `apo summicron sl 35`: APO token이 intent에 반영되지 않아 non-APO Summicron-SL 35가 APO-SL 35보다 먼저 나온다.
- `sl 24-90`: SL mount는 잡지만 top1이 Sigma 30mm L-mount lens라 zoom query recall이 약하다.
- `sl 14-24`: SL mount broadening은 되지만 specific zoom family recall이 없다.
- `sl 16-35`: SL mount broadening은 되지만 specific zoom family recall이 없다.
- `sl 90-280`: SL mount broadening은 되지만 tele zoom family recall이 없다.
- `visoflex ii`: Accessory category는 맞지만 Universal/Tele Finder가 Visoflex II보다 먼저 온다.
- `universal finder`: Accessory category는 맞지만 exact universal finder보다 tele finder generic이 먼저 온다.
- `apo telyt r 180`: Telyt intent가 반영되지 않아 APO-Telyt-R 180이 top1이 아니다.
- `r 70-180`: R mount broadening은 되지만 target zoom family recall이 없다.
- `vario apo elmarit r 70-180`: query family는 맞지만 top1이 28mm Elmarit-R로 잘못 올라간다.
- `24 cron`: closed-hypothesis-adjacent shorthand인데 unrelated R 50 Summicron-R가 top1이다.
### over_hard_pinned
- `vario elmarit`: broad shorthand인데 S Elmarit 하나로 과도하게 끌린다.
- `lux`: broad shorthand인데 M Summilux family로 실질 hard-pin된다.
- `summicron sl 24`: closed hypothesis query인데 nearby SL Summicron/APO-Summicron rows로 흘러간다.
### closed_hypothesis_leak
- 없음
### needs_followup
- 없음

## 6. 의미 있는 발견
- SL 35 계열 query는 현재 꽤 안정적으로 `SL Lens / Summicron-SL` 또는 `APO-Summicron` neighborhood로 간다.
- 반면 SL zoom shorthand (`sl 24-90`, `sl 14-24`, `sl 16-35`, `sl 90-280`)는 mount=SL broadening만 되고 family recall은 약하다.
- accessory query는 `hood 12549`, `m adapter l`처럼 code/intent가 강한 경우는 좋지만, `bp-scl5`, `sl3 battery`, `leica m strap`처럼 token parser가 직접 못 읽는 케이스는 약하다.
- R query는 mount=R 축은 대체로 유지하지만, exact family ranking이 흔들린다.
- body query는 `leica iiif`, `barnack iiif`, `leica q2`는 강하지만, `leica sl2`, `leica sl3`, `leica m10 body`는 structured body intent를 못 만들고 lens rows로 무너진다.
- broad dangerous shorthand에서는 closed hypothesis가 직접 top1으로 새지는 않았지만, `summicron sl 24`처럼 nearby SL family로 과하게 끌리는 현상이 남아 있다.

## 7. 다음 후보 backlog
- `P3-query-ranking`: M shorthand, SL zoom, R lens query에서 top1 family ordering이 흔들리는 문제
- `P3-broad-alias-control`: broad `summicron` / `lux` / `vario elmarit` / `summicron sl 24` query hard-pin 제어
- `P3-no-result-recall`: `steel rim`, `bp-scl5`, `sl3 battery`, `apo` 같은 parser miss / zero-result recall
- `P3-accessory-search-ranking`: `leica m strap`, `summicron`, `summicron 24`에서 accessory intent를 더 잘 드러내는 검색 랭킹 보정
- `P3-R-lens-query-recall`: `apo telyt r 180`, `r 70-180`, `vario apo elmarit r 70-180` recall 개선
- `P3-body-query-recall`: `leica sl2`, `leica sl3`, `leica m10 body` body intent parsing / ranking 개선

## 8. 결론
- 현재 검색 신뢰도는 일부 축에서는 MVP 수준에 가까워졌다. 특히 SL 35, Barnack body, Q2, 일부 accessory code query는 꽤 안정적이다.
- 하지만 classifier를 더 고치기보다 이제는 query parser / ranking / broad shorthand control 쪽 backlog가 더 앞에 온다.
- 특히 body query recall, SL zoom recall, broad shorthand 제어, accessory search ranking이 다음 단계다.
- 다음 추천 작업: `P3-body-query-recall`, `P3-query-ranking`, `P3-broad-alias-control`, `P3-accessory-search-ranking` 순으로 검토한다.
