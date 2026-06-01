# P3-QUERY-RANKING

## 1. 작업 목적
- 현재 search entrypoint 기준으로 P3 축의 query recall / ranking이 서로 충돌 없이 유지되는지 통합 smoke로 확인한다.
- 이번 라운드는 observation/report-first이며 production ranking code 수정은 하지 않는다.

## 2. 실행 entrypoint
- `api.search.endpoint_response -> search_service.load_and_search -> data/derived/results_search_index_v1.json`
- top3까지 현재 검색 API 경로를 그대로 사용해 기록했다.

## 3. 총 query 수
- 총 query 수: `109`
- group별 query 수:
  - `body_recall`: `6`
  - `accessory_ranking`: `10`
  - `sl_zoom_recall`: `4`
  - `sl_prime_leica_l`: `8`
  - `broad_alias`: `6`
  - `m_lens_guardrail`: `11`
  - `r_lens_recall`: `22`
  - `broad_r_observation`: `8`
  - `third_party_l_mount`: `14`
  - `no_result_source_coverage`: `4`
  - `short_alias_observation`: `5`
  - `accessory_taxonomy_observation`: `11`

## 4. status 분포
- `guardrail_pass`: `19`
- `needs_source_or_index_followup`: `3`
- `no_result_confirmed`: `4`
- `observation_only`: `15`
- `pass`: `42`
- `weak_pass`: `26`

## 5. group별 요약
- `body_recall`: pass=6
- `accessory_ranking`: guardrail_pass=10
- `sl_zoom_recall`: pass=4
- `sl_prime_leica_l`: pass=7, weak_pass=1
- `broad_alias`: observation_only=2, weak_pass=4
- `m_lens_guardrail`: guardrail_pass=7, weak_pass=4
- `r_lens_recall`: pass=14, weak_pass=8
- `broad_r_observation`: observation_only=8
- `third_party_l_mount`: needs_source_or_index_followup=3, pass=11
- `no_result_source_coverage`: no_result_confirmed=4
- `short_alias_observation`: observation_only=5
- `accessory_taxonomy_observation`: guardrail_pass=2, weak_pass=9

## 6. pass 유지된 핵심 query
- `leica sl2`: `pass` / `Body:SL2:Leica` - none
- `leica sl3`: `pass` / `Body:SL3:Leica` - none
- `leica m10 body`: `pass` / `Body:M10:Leica` - none
- `sl 24-90`: `pass` / `Lens:Vario-Elmarit-SL:Leica` - none
- `sl 14-24`: `pass` / `Lens:Super-Vario-Elmarit-SL:Leica` - none
- `sl 16-35`: `pass` / `Lens:Super-Vario-Elmar-SL:Leica` - none
- `sl 90-280`: `pass` / `Lens:APO-Vario-Elmarit-SL:Leica` - none
- `r 50 summicron`: `pass` / `Lens:Summicron-R:Leica` - none
- `summicron-r 50`: `pass` / `Lens:Summicron-R:Leica` - none
- `r 180 apo`: `pass` / `Lens:APO-Telyt-R:Leica` - none
- `apo-telyt-r 180`: `pass` / `Lens:APO-Telyt-R:Leica` - none
- `panasonic 24-105 l`: `pass` / `Lens::3rd Party` - none

## 7. weak_pass 후보
- `apo summicron sl 35`: `weak_pass` / `Lens:Summicron-SL:Leica` - APO family ranking still weak
- `summicron`: `weak_pass` / `Lens:Summicron:Leica` - lens-first is good, but broad family ambiguity remains
- `summilux`: `weak_pass` / `Lens:Summilux:Leica` - lens-first is good, but broad family ambiguity remains
- `leica summicron`: `weak_pass` / `Lens:Summicron:Leica` - lens-first is good, but broad family ambiguity remains
- `leica summilux`: `weak_pass` / `Lens:Summilux:Leica` - lens-first is good, but broad family ambiguity remains
- `summicron 50`: `weak_pass` / `Lens:Summicron:Leica` - broad M shorthand still ambiguous but stayed lens-side
- `50 cron`: `weak_pass` / `Lens:Summicron-R:Leica` - broad M shorthand still ambiguous but stayed lens-side
- `35 lux`: `weak_pass` / `Lens:Summilux-M:Leica` - broad M shorthand still ambiguous but stayed lens-side
- `50 lux`: `weak_pass` / `Lens:Summilux-M:Leica` - broad M shorthand still ambiguous but stayed lens-side
- `elmarit-r 28`: `weak_pass` / `Lens:Elmarit-R:Leica` - specific R observation query recovered and now stable
- `r 28 elmarit`: `weak_pass` / `Lens:Elmarit-R:Leica` - specific R observation query recovered and now stable
- `elmarit-r 35`: `weak_pass` / `Lens:Elmarit-R:Leica` - specific R observation query recovered and now stable
- `r 35 elmarit`: `weak_pass` / `Lens:Elmarit-R:Leica` - specific R observation query recovered and now stable
- `summicron-r 90`: `weak_pass` / `Lens:Summicron-R:Leica` - specific R observation query recovered and now stable
- `r 90 summicron`: `weak_pass` / `Lens:Summicron-R:Leica` - specific R observation query recovered and now stable
- `vario elmarit r 28-90`: `weak_pass` / `Lens:Vario-Elmarit-R:Leica` - specific R observation query recovered and now stable
- `r 28-90 vario elmarit`: `weak_pass` / `Lens:Vario-Elmarit-R:Leica` - specific R observation query recovered and now stable
- `bp-scl6`: `weak_pass` / `Accessory:Q3:Leica` - accessory result is usable but broad accessory taxonomy remains loose
- `bp-scl5`: `weak_pass` / `Accessory:CL:Unknown` - accessory result is usable but broad accessory taxonomy remains loose
- `leica cap`: `weak_pass` / `Accessory::Leica` - accessory result is usable but broad accessory taxonomy remains loose

## 8. fail / regression 후보
- 없음

## 9. no-result / source coverage 후보
- `sigma 14-24 l`: `needs_source_or_index_followup` / `::` - known third-party source coverage gap
- `sigma 14-24 l mount`: `needs_source_or_index_followup` / `::` - known third-party source coverage gap
- `sigma 14-24 dg dn`: `needs_source_or_index_followup` / `::` - known third-party source coverage gap
- `sigma 14-24 l`: `no_result_confirmed` / `::` - no candidate found in search index / normalized / raw
- `sigma 14-24 l mount`: `no_result_confirmed` / `::` - no candidate found in search index / normalized / raw
- `sigma 14-24 dg dn`: `no_result_confirmed` / `::` - no candidate found in search index / normalized / raw
- `sigma 14-24 dg dn art`: `no_result_confirmed` / `::` - no candidate found in search index / normalized / raw

## 10. taxonomy audit 후보
- `bp-scl6`: `weak_pass` / `Accessory:Q3:Leica` - accessory result is usable but broad accessory taxonomy remains loose
- `bp-scl5`: `weak_pass` / `Accessory:CL:Unknown` - accessory result is usable but broad accessory taxonomy remains loose
- `leica cap`: `weak_pass` / `Accessory::Leica` - accessory result is usable but broad accessory taxonomy remains loose
- `m cap`: `weak_pass` / `Accessory:M3:Leica` - accessory result is usable but broad accessory taxonomy remains loose
- `r cap`: `weak_pass` / `Accessory:R6:Leica` - accessory result is usable but broad accessory taxonomy remains loose
- `sl cap`: `weak_pass` / `Accessory::Unknown` - accessory result is usable but broad accessory taxonomy remains loose
- `leica finder`: `weak_pass` / `Accessory::Leica` - accessory result is usable but broad accessory taxonomy remains loose
- `leica handgrip`: `weak_pass` / `Lens:Elmar:Leica` - broad accessory query is still taxonomy/alias-sensitive
- `leica filter`: `weak_pass` / `Accessory::Leica` - accessory result is usable but broad accessory taxonomy remains loose

## 11. UI disambiguation 후보
- `summicron`: `weak_pass` / `Lens:Summicron:Leica` - lens-first is good, but broad family ambiguity remains
- `summilux`: `weak_pass` / `Lens:Summilux:Leica` - lens-first is good, but broad family ambiguity remains
- `leica summicron`: `weak_pass` / `Lens:Summicron:Leica` - lens-first is good, but broad family ambiguity remains
- `leica summilux`: `weak_pass` / `Lens:Summilux:Leica` - lens-first is good, but broad family ambiguity remains

## 12. 상세 결과
### body_recall
| query | top1 | top2 | top3 | status | weakness | note |
|---|---|---|---|---|---|---|
| leica sl2 | Body / SL Body / SL / SL2 / Leica / Leica SL2 Black | Body / SL2 / Leica SL2 Black | Body / SL2 / Leica SL2-S Reporter | pass | none |  |
| leica sl3 | Body / SL Body / SL / SL3 / Leica / Leica SL3 Black | Body / SL3 / Leica SL3 Reporter | Body / SL3 / Leica SL3 Body Only | pass | none |  |
| leica m10 body | Body / M Body / M / M10 / Leica / [위탁] M10 Monochrom 'Leitz Wetzlar' Edition | Body / M10 / [중고] Leica M10 홀스터 | Body / M10 / [중고] Leica M10 하프케이스 (Brown) | pass | none |  |
| leica iiif | Body / L Body / L / IIIf / Leica / Leica Barnack IIIF Silver | Body / IIIf / Leica Barnack IIIf Silver | Body / IIIf / Leica Barnack IIIF Silver | pass | none |  |
| barnack iiif | Body / L Body / L / IIIf / Leica / Leica Barnack IIIF Silver | Body / IIIf / Leica Barnack IIIf Silver | Body / IIIf / Leica Barnack IIIF Silver | pass | none |  |
| leica q2 | Body / Leica Body / Q / Q2 / Leica / Leica Q2 007 Edition | Body / Q2 / Leica Q2 Black | Body / Q2 / [중고] Leica Q2 Monochrome | pass | none |  |

### accessory_ranking
| query | top1 | top2 | top3 | status | weakness | note |
|---|---|---|---|---|---|---|
| sl3 battery | Accessory / Accessory / SL / Q3 / Unknown / [중고] Q3,SL3 배터리 (BP-SCL6) | Accessory / Q3 / [위탁] Q3,SL3 배터리 (BP-SCL6) | Accessory / Q3 / [중고] Q3,SL3 배터리 (BP-SCL6) | guardrail_pass | none |  |
| leica m strap | Accessory / Accessory / M / M11 / Leica / [중고] Leica M11 strap (Cognac) | Accessory / M11 / [중고] Leica M11 Neck strap (Cognac) | Accessory /  / Leica M-L adapter Black | guardrail_pass | none |  |
| leica hood 12585 | Accessory / Accessory / M /  / Leica / Leica 12585 Hood for M-50mm, 35mm | Accessory /  / [중고] Leica 12585 후드 | Accessory /  / [중고] Leica 12585 후드 | guardrail_pass | none |  |
| hood 12549 | Accessory / Accessory / M / Elmar / Leica / Leica 12549 Hood Silver [for M 50mm f2.8 Elmar] | Accessory / Elmar / Leica 12549 Lens Hood Silver （Elmar） | Lens /  / LEICA 12549 | guardrail_pass | none |  |
| m adapter l | Accessory / Accessory / M /  / Leica / Leica M-L adapter Black | Accessory /  / Leica M-L adapter Black | Accessory /  / Leica M-L adapter Silver | guardrail_pass | none |  |
| r adapter | Accessory / Accessory / R / R6 / Leica / [중고] Leica R6 가죽 케이스 | Accessory / R6 / [중고] Leica R6 가죽 케이스 | Accessory / APO-Telyt / LEICA 280mm F4 APO-TELYT-R APO-EXTENDER-R sn.3622 | guardrail_pass | none |  |
| leica r adapter | Accessory / Accessory / R / R6 / Leica / [중고] Leica R6 가죽 케이스 | Accessory / R6 / [중고] Leica R6 가죽 케이스 | Accessory / APO-Telyt / LEICA 280mm F4 APO-TELYT-R APO-EXTENDER-R sn.3622 | guardrail_pass | none |  |
| leica r cap | Accessory / Accessory / R / R6 / Leica / [중고] Leica R6 가죽 케이스 | Accessory / R6 / [중고] Leica R6 가죽 케이스 | Accessory / APO-Telyt / LEICA 280mm F4 APO-TELYT-R APO-EXTENDER-R sn.3622 | guardrail_pass | none |  |
| r lens cap | Accessory / Accessory / R / R6 / Leica / [중고] Leica R6 가죽 케이스 | Accessory / R6 / [중고] Leica R6 가죽 케이스 | Accessory / APO-Telyt / LEICA 280mm F4 APO-TELYT-R APO-EXTENDER-R sn.3622 | guardrail_pass | none |  |
| r hood | Accessory / Accessory / R / R6 / Leica / [중고] Leica R6 가죽 케이스 | Accessory / R6 / [중고] Leica R6 가죽 케이스 | Accessory / APO-Telyt / LEICA 280mm F4 APO-TELYT-R APO-EXTENDER-R sn.3622 | guardrail_pass | none |  |

### sl_zoom_recall
| query | top1 | top2 | top3 | status | weakness | note |
|---|---|---|---|---|---|---|
| sl 24-90 | Lens / SL Lens / SL / Vario-Elmarit-SL / Leica / Leica SL 24-90mm f2.8-4 Vario-Elmarit Black | Lens / Vario-Elmarit-SL / Leica SL 24-90mm f2.8-4 Vario-Elmarit Black | Lens / Vario-Elmarit-SL / [위탁] SL 24-90/2.8-4 Vario Elmar ASPH (Black) | pass | none |  |
| sl 14-24 | Lens / SL Lens / SL / Super-Vario-Elmarit-SL / Leica / [중고] SL 14-24/2.8 Vario Elmarit ASPH (Black) | Lens / Super-Vario-Elmarit-SL / [중고] SL 14-24/2.8 Vario Elmarit ASPH (Black) | Lens / Super-Vario-Elmarit-SL / [중고] SL 14-24/2.8 Vario Elmarit ASPH (Black) | pass | none |  |
| sl 16-35 | Lens / SL Lens / SL / Super-Vario-Elmar-SL / Leica / [중고] SL 16-35/3.5-4.5 Super Vario Elmar ASPH (Black) | Lens / Super-Vario-Elmar-SL / [중고] SL 16-35/3.5-4.5 Super Vario Elmar ASPH (Black) | Lens / Super-Vario-Elmar-SL / LEICA SL2 16-35mm F3.5-4.5 ASPH sn.4687/5576 | pass | none |  |
| sl 90-280 | Lens / SL Lens / SL / APO-Vario-Elmarit-SL / Leica / [중고] SL APO Vario Elmarit 90-280 f/2.8-4 | Lens / APO-Vario-Elmarit-SL / [중고] SL APO Vario Elmarit 90-280 f/2.8-4 | Lens / APO-Vario-Elmarit-SL / [중고] SL 90-280/2.8-4 APO Vario Elmarit ASPH (Black) | pass | none |  |

### sl_prime_leica_l
| query | top1 | top2 | top3 | status | weakness | note |
|---|---|---|---|---|---|---|
| summicron sl 35 | Lens / SL Lens / SL / Summicron-SL / Leica / 신품 Leica SL 35mm f2 Summicron ASPH Black | Lens / Summicron-SL / [중고] Leica SL2 with Summicron-SL 35mm f/2 ASPH | Lens / APO-Summicron / LEICA 35mm F2 ASPH APO-SUMMICRON-SL sn.4720 | pass | none |  |
| Leica 35mm F2 AsphSummicron SL | Lens / SL Lens / SL / Summicron-SL / Leica / 신품 Leica SL 35mm f2 Summicron ASPH Black | Lens / Summicron-SL / [중고] Leica SL2 with Summicron-SL 35mm f/2 ASPH | Lens / APO-Summicron / LEICA 35mm F2 ASPH APO-SUMMICRON-SL sn.4720 | pass | none |  |
| apo summicron sl 35 | Lens / SL Lens / SL / Summicron-SL / Leica / 신품 Leica SL 35mm f2 Summicron ASPH Black | Lens / Summicron-SL / [중고] Leica SL2 with Summicron-SL 35mm f/2 ASPH | Lens / APO-Summicron / LEICA 35mm F2 ASPH APO-SUMMICRON-SL sn.4720 | weak_pass | family_ranking_weak | APO family ranking still weak |
| sl 35 summicron | Lens / SL Lens / SL / Summicron-SL / Leica / 신품 Leica SL 35mm f2 Summicron ASPH Black | Lens / Summicron-SL / [중고] Leica SL2 with Summicron-SL 35mm f/2 ASPH | Lens / APO-Summicron / LEICA 35mm F2 ASPH APO-SUMMICRON-SL sn.4720 | pass | none |  |
| sl 50 summicron | Lens / SL Lens / SL / APO-Summicron / Leica / Leica SL 50mm f2 APO-Summicron ASPH Black | Lens / Summicron-SL / [위탁] Leica SL2-S Kit with Summicron-SL 50mm f/2 ASPH | Lens / Summicron-SL / [중고] Leica Summicron-SL 50mm f/2 ASPH | pass | none |  |
| sl 75 summicron | Lens / SL Lens / SL / APO-Summicron / Leica / LEICA 75mm F2 ASPH APO-SUMMICRON-SL sn.4709 | Lens / APO-Summicron / LEICA 75mm F2 APO-SUMMICRON-SL sn.4699 | Lens / APO-Summicron / Leica SL 50mm f2 APO-Summicron ASPH Black | pass | none |  |
| sl 90 summicron | Lens / SL Lens / SL / APO-Summicron / Leica / LEICA 90mm F2 ASPH APO-summicron-SL sn.4713 | Lens / APO-Summicron / [중고] SL 90/2 APO-Summicron | Lens / APO-Summicron / [중고] SL 90/2 APO Summicron ASPH (Black) | pass | none |  |
| Leica L 50mm Summicron | Lens / L Lens / L / Summicron / Leica / Leica L 50mm f2 Summicron Silver | Lens / Summicron / Leica L 50mm f2 Summicron Rigid Silver | Lens / Summicron / Leica L 50mm f2 Summicron Silver | pass | none |  |

### broad_alias
| query | top1 | top2 | top3 | status | weakness | note |
|---|---|---|---|---|---|---|
| summicron | Lens / L Lens / L / Summicron / Leica / Leica L 50mm f2 Summicron Silver | Lens / Summicron / Leica L 50mm f2 Summicron Rigid Silver | Lens / Summicron / Leica L 50mm f2 Summicron Silver | weak_pass | ui_disambiguation_needed | lens-first is good, but broad family ambiguity remains |
| summilux | Lens / L Lens / L / Summilux / Leica / [중고] L 50/1.4 Summilux 4세대 (Silver) | Lens / Summilux / LEICA 50mm F1.4 SUMMILUX M39 sn.3868 | Lens / Summilux / LEICA 50mm F1.4 Screwmount M39 SUMMILUX-L sn.3868 | weak_pass | ui_disambiguation_needed | lens-first is good, but broad family ambiguity remains |
| leica summicron | Lens / L Lens / L / Summicron / Leica / Leica L 50mm f2 Summicron Silver | Lens / Summicron / Leica L 50mm f2 Summicron Rigid Silver | Lens / Summicron / Leica L 50mm f2 Summicron Silver | weak_pass | ui_disambiguation_needed | lens-first is good, but broad family ambiguity remains |
| leica summilux | Lens / L Lens / L / Summilux / Leica / [중고] L 50/1.4 Summilux 4세대 (Silver) | Lens / Summilux / LEICA 50mm F1.4 SUMMILUX M39 sn.3868 | Lens / Summilux / LEICA 50mm F1.4 Screwmount M39 SUMMILUX-L sn.3868 | weak_pass | ui_disambiguation_needed | lens-first is good, but broad family ambiguity remains |
| cron | Lens / R Lens / R / Summicron-R / Leica / Leica R 50mm f2 Summicron Black | Accessory / Summicron / 신품 호환 Leica 14043 Hood Cover for M 35mm f2 Summicron, M 28mm f2.8 Elmarit | Lens / Summicron-M / Leica M 28mm f2 Summicron ASPH 6bit Safari Edition | observation_only | broad_query_ambiguity | short alias intentionally left ambiguous |
| lux | Lens / M Lens / M / Summilux-M / Leica / Leica M 28mm f1.4 Summilux ASPH 6bit Black | Lens / Summilux-M / Leica M 50mm f1.4 Summilux Classic Silver | Lens / Summilux-M / Leica M 50mm f1.4 Summilux 4th Silver | observation_only | broad_query_ambiguity | short alias intentionally left ambiguous |

### m_lens_guardrail
| query | top1 | top2 | top3 | status | weakness | note |
|---|---|---|---|---|---|---|
| summicron 50 | Lens / L Lens / L / Summicron / Leica / Leica L 50mm f2 Summicron Silver | Lens / Summicron / Leica L 50mm f2 Summicron Rigid Silver | Lens / Summicron / Leica L 50mm f2 Summicron Silver | weak_pass | broad_query_ambiguity | broad M shorthand still ambiguous but stayed lens-side |
| summicron m 50 | Lens / M Lens / M / Summicron-M / Leica / Leica M 50mm f2 Summicron Rigid Silver | Lens / APO-Summicron / Leica M 50mm f2 APO-Summicron ASPH Black Chrome finish | Lens / Summicron-M / Leica M 50mm f 2 Summicron Rigid BlackRepaint | guardrail_pass | none |  |
| m 50 summicron | Lens / M Lens / M / Summicron-M / Leica / Leica M 50mm f2 Summicron Rigid Silver | Lens / APO-Summicron / Leica M 50mm f2 APO-Summicron ASPH Black Chrome finish | Lens / Summicron-M / Leica M 50mm f 2 Summicron Rigid BlackRepaint | guardrail_pass | none |  |
| leica m 50 summicron | Lens / M Lens / M / Summicron-M / Leica / Leica M 50mm f2 Summicron Rigid Silver | Lens / APO-Summicron / Leica M 50mm f2 APO-Summicron ASPH Black Chrome finish | Lens / Summicron-M / Leica M 50mm f 2 Summicron Rigid BlackRepaint | guardrail_pass | none |  |
| 50 cron | Lens / R Lens / R / Summicron-R / Leica / Leica R 50mm f2 Summicron Black | Lens / APO-Summicron / Leica SL 50mm f2 APO-Summicron ASPH Black | Lens / Summicron-M / Leica M 50mm f2 Summicron Rigid Silver | weak_pass | broad_query_ambiguity | broad M shorthand still ambiguous but stayed lens-side |
| 35 lux | Lens / M Lens / M / Summilux-M / Leica / Leica M 35mm f1.4 Summilux 2nd Titan | Lens / Summilux-M / Leica M 35mm f1.4 Summilux 1st Silver [Steel Rim] | Lens / Summilux-M / Leica M 35mm f1.4 Summilux ASPH 4th Titan | weak_pass | broad_query_ambiguity | broad M shorthand still ambiguous but stayed lens-side |
| 50 lux | Lens / M Lens / M / Summilux-M / Leica / Leica M 50mm f1.4 Summilux Classic Silver | Lens / Summilux-M / Leica M 50mm f1.4 Summilux 4th Silver | Lens / Summilux-M / Leica M 50mm f1.4 Summilux ASPH 6bit Silver | weak_pass | broad_query_ambiguity | broad M shorthand still ambiguous but stayed lens-side |
| elmarit m 28 | Lens / M Lens / M / Elmarit-M / Leica / Leica M 28mm f2.8 Elmarit ASPH 5th 6bit Black | Lens / Elmarit-M / Leica M 28mm f2.8 Elmarit 3rd Black | Lens / Elmarit-M / Leica M 28mm f2.8 Elmarit 2nd Black | guardrail_pass | none |  |
| m 28 elmarit | Lens / M Lens / M / Elmarit-M / Leica / Leica M 28mm f2.8 Elmarit ASPH 5th 6bit Black | Lens / Elmarit-M / Leica M 28mm f2.8 Elmarit 3rd Black | Lens / Elmarit-M / Leica M 28mm f2.8 Elmarit 2nd Black | guardrail_pass | none |  |
| apo telyt m 135 | Lens / M Lens / M / Tele-Elmar / Leica / Leica M 135mm f4 Tele-Elmar Black | Lens / Hektor / Leica M 135mm f4.5 Hektor Silver | Lens / Tele-Elmar / Leica M 135mm f4 Tele-Elmar Black | guardrail_pass | none |  |
| m 135 apo telyt | Lens / M Lens / M / Tele-Elmar / Leica / Leica M 135mm f4 Tele-Elmar Black | Lens / Hektor / Leica M 135mm f4.5 Hektor Silver | Lens / Tele-Elmar / Leica M 135mm f4 Tele-Elmar Black | guardrail_pass | none |  |

### r_lens_recall
| query | top1 | top2 | top3 | status | weakness | note |
|---|---|---|---|---|---|---|
| r 50 summicron | Lens / R Lens / R / Summicron-R / Leica / Leica R 50mm f2 Summicron Black | Lens / Summicron-R / LEICA 50mm F2 SUMMICRON-R sn.3338 | Lens / Summicron-R / LEICA 50mm F2 ROM SUMMICRON-R sn.3819 | pass | none |  |
| summicron-r 50 | Lens / R Lens / R / Summicron-R / Leica / Leica R 50mm f2 Summicron Black | Lens / Summicron-R / LEICA 50mm F2 SUMMICRON-R sn.3338 | Lens / Summicron-R / LEICA 50mm F2 ROM SUMMICRON-R sn.3819 | pass | none |  |
| summicron r 50 | Lens / R Lens / R / Summicron-R / Leica / Leica R 50mm f2 Summicron Black | Lens / Summicron-R / LEICA 50mm F2 SUMMICRON-R sn.3338 | Lens / Summicron-R / LEICA 50mm F2 ROM SUMMICRON-R sn.3819 | pass | none |  |
| r 50/2 summicron | Lens / R Lens / R / Summicron-R / Leica / Leica R 50mm f2 Summicron Black | Lens / Summicron-R / LEICA 50mm F2 SUMMICRON-R sn.3338 | Lens / Summicron-R / LEICA 50mm F2 ROM SUMMICRON-R sn.3819 | pass | none |  |
| leica r 50mm f2 summicron | Lens / R Lens / R / Summicron-R / Leica / Leica R 50mm f2 Summicron Black | Lens / Summicron-R / LEICA 50mm F2 SUMMICRON-R sn.3338 | Lens / Summicron-R / LEICA 50mm F2 ROM SUMMICRON-R sn.3819 | pass | none |  |
| r 180 apo | Lens / R Lens / R / APO-Telyt-R / Leica / Leica R 180mm f3.4 APO-Telyt Black | Lens / APO-Telyt-R / Leica R 180mm f3.4 APO-Telyt Black | Lens / APO-Telyt-R / LEICA 180mm F3.4 APO-TELYT-R sn.3478 | pass | none |  |
| r 180 apo telyt | Lens / R Lens / R / APO-Telyt-R / Leica / Leica R 180mm f3.4 APO-Telyt Black | Lens / APO-Telyt-R / Leica R 180mm f3.4 APO-Telyt Black | Lens / APO-Telyt-R / LEICA 180mm F3.4 APO-TELYT-R sn.3478 | pass | none |  |
| apo telyt r 180 | Lens / R Lens / R / APO-Telyt-R / Leica / Leica R 180mm f3.4 APO-Telyt Black | Lens / APO-Telyt-R / Leica R 180mm f3.4 APO-Telyt Black | Lens / APO-Telyt-R / LEICA 180mm F3.4 APO-TELYT-R sn.3478 | pass | none |  |
| apo-telyt-r 180 | Lens / R Lens / R / APO-Telyt-R / Leica / Leica R 180mm f3.4 APO-Telyt Black | Lens / APO-Telyt-R / Leica R 180mm f3.4 APO-Telyt Black | Lens / APO-Telyt-R / LEICA 180mm F3.4 APO-TELYT-R sn.3478 | pass | none |  |
| r 180/3.4 apo | Lens / R Lens / R / APO-Telyt-R / Leica / Leica R 180mm f3.4 APO-Telyt Black | Lens / APO-Telyt-R / Leica R 180mm f3.4 APO-Telyt Black | Lens / APO-Telyt-R / LEICA 180mm F3.4 APO-TELYT-R sn.3478 | pass | none |  |
| leica r 180mm f3.4 apo telyt | Lens / R Lens / R / APO-Telyt-R / Leica / Leica R 180mm f3.4 APO-Telyt Black | Lens / APO-Telyt-R / Leica R 180mm f3.4 APO-Telyt Black | Lens / APO-Telyt-R / LEICA 180mm F3.4 APO-TELYT-R sn.3478 | pass | none |  |
| elmarit r 135 | Lens / R Lens / R / Elmarit-R / Leica / LEICA 135mm F2.8 ELMARIT-R sn.2155 | Lens / Elmarit-R / LEICA 135mm F2.8 ELMARIT-R sn.2772 | Lens / Elmarit-R / LEICA 135mm F2.8 ELMARIT-R sn.2809 | pass | none |  |
| r 135 elmarit | Lens / R Lens / R / Elmarit-R / Leica / LEICA 135mm F2.8 ELMARIT-R sn.2155 | Lens / Elmarit-R / LEICA 135mm F2.8 ELMARIT-R sn.2772 | Lens / Elmarit-R / LEICA 135mm F2.8 ELMARIT-R sn.2809 | pass | none |  |
| leica r 135mm f2.8 elmarit | Lens / R Lens / R / Elmarit-R / Leica / LEICA 135mm F2.8 ELMARIT-R sn.2155 | Lens / Elmarit-R / LEICA 135mm F2.8 ELMARIT-R sn.2772 | Lens / Elmarit-R / LEICA 135mm F2.8 ELMARIT-R sn.2809 | pass | none |  |
| elmarit-r 28 | Lens / R Lens / R / Elmarit-R / Leica / Leica R 28mm f2.8 Elmarit Rom Black | Lens / Elmarit-R / LEICA 28mm F2.8 ELMARIT-R sn.3624 | Lens / Elmarit-R / LEICA 28mm F2.8 ELMARIT-R sn.3624 | weak_pass | none | specific R observation query recovered and now stable |
| r 28 elmarit | Lens / R Lens / R / Elmarit-R / Leica / Leica R 28mm f2.8 Elmarit Rom Black | Lens / Elmarit-R / LEICA 28mm F2.8 ELMARIT-R sn.3624 | Lens / Elmarit-R / LEICA 28mm F2.8 ELMARIT-R sn.3624 | weak_pass | none | specific R observation query recovered and now stable |
| elmarit-r 35 | Lens / R Lens / R / Elmarit-R / Leica / LEICA R6.2 35mm F2.8 ELMARIT-R sn.1923 | Lens / Elmarit-R / Leica R 28mm f2.8 Elmarit Rom Black | Lens / Elmarit-R / Leica R 24mm f2.8 Elmarit Black | weak_pass | none | specific R observation query recovered and now stable |
| r 35 elmarit | Lens / R Lens / R / Elmarit-R / Leica / LEICA R6.2 35mm F2.8 ELMARIT-R sn.1923 | Lens / Elmarit-R / Leica R 28mm f2.8 Elmarit Rom Black | Lens / APO-Macro-Elmarit-R / Leica R 70-180mm f2.8 Vario-Apo-Elmarit Black | weak_pass | none | specific R observation query recovered and now stable |
| summicron-r 90 | Lens / R Lens / R / Summicron-R / Leica / LEICA 90mm F2 SUMMICRON-R sn.3567 | Lens / Summicron-R / Leica R 50mm f2 Summicron Black | Lens / Summicron-R / [위탁] R 50/2 Summicron (Black) | weak_pass | none | specific R observation query recovered and now stable |
| r 90 summicron | Lens / R Lens / R / Summicron-R / Leica / LEICA 90mm F2 SUMMICRON-R sn.3567 | Lens / Summicron-R / Leica R 50mm f2 Summicron Black | Lens / Summicron-R / [위탁] R 50/2 Summicron (Black) | weak_pass | none | specific R observation query recovered and now stable |
| vario elmarit r 28-90 | Lens / R Lens / R / Vario-Elmarit-R / Leica / LEICA 28-90mm F2.8-4.5 VARIO-ELMARIT-R sn.3975 | Lens / Vario-Elmarit-R / LEICA 28-90mm F2.8-4.5 ASPH VARIO-ELMARIT-R sn.3974 | Lens / Vario-Elmarit-R / LEICA 28-90mm F2.8-4.5 VARIO-ELMARIT-R sn.3973 | weak_pass | none | specific R observation query recovered and now stable |
| r 28-90 vario elmarit | Lens / R Lens / R / Vario-Elmarit-R / Leica / LEICA 28-90mm F2.8-4.5 VARIO-ELMARIT-R sn.3975 | Lens / Vario-Elmarit-R / LEICA 28-90mm F2.8-4.5 ASPH VARIO-ELMARIT-R sn.3974 | Lens / Vario-Elmarit-R / LEICA 28-90mm F2.8-4.5 VARIO-ELMARIT-R sn.3973 | weak_pass | none | specific R observation query recovered and now stable |

### broad_r_observation
| query | top1 | top2 | top3 | status | weakness | note |
|---|---|---|---|---|---|---|
| leica r | Lens / R Lens / R / Summicron-R / Leica / Leica R 50mm f2 Summicron Black | Lens / Elmar-R / Leica R 180mm f2.8 APO-Elmart Rom Black | Lens / Elmarit-R / Leica R 28mm f2.8 Elmarit Rom Black | observation_only | broad_query_ambiguity | broad R query intentionally not hard-pinned |
| r lens | Lens / R Lens / R / Summicron-R / Leica / Leica R 50mm f2 Summicron Black | Lens / Elmar-R / Leica R 180mm f2.8 APO-Elmart Rom Black | Lens / Elmarit-R / Leica R 28mm f2.8 Elmarit Rom Black | observation_only | broad_query_ambiguity | broad R query intentionally not hard-pinned |
| leica r 28-90 | Lens / R Lens / R / Summicron-R / Leica / Leica R 50mm f2 Summicron Black | Lens / Elmar-R / Leica R 180mm f2.8 APO-Elmart Rom Black | Lens / Elmarit-R / Leica R 28mm f2.8 Elmarit Rom Black | observation_only | broad_query_ambiguity | broad R query intentionally not hard-pinned |
| r summicron | Lens / R Lens / R / Summicron-R / Leica / Leica R 50mm f2 Summicron Black | Lens / Summicron-R / [위탁] R 50/2 Summicron (Black) | Lens / Summicron-R / [위탁] R 35/2 Summicron (Black) | observation_only | broad_query_ambiguity | broad R query intentionally not hard-pinned |
| r elmarit | Lens / R Lens / R / Elmarit-R / Leica / Leica R 28mm f2.8 Elmarit Rom Black | Lens / APO-Macro-Elmarit-R / Leica R 70-180mm f2.8 Vario-Apo-Elmarit Black | Lens / APO-Macro-Elmarit / Leica R 100mm f2.8 APO-Macro-Elmarit Black | observation_only | broad_query_ambiguity | broad R query intentionally not hard-pinned |
| r apo | Lens / R Lens / R / Summicron-R / Leica / Leica R 50mm f2 Summicron Black | Lens / Elmar-R / Leica R 180mm f2.8 APO-Elmart Rom Black | Lens / Elmarit-R / Leica R 28mm f2.8 Elmarit Rom Black | observation_only | broad_query_ambiguity | broad R query intentionally not hard-pinned |
| r telyt | Lens / R Lens / R / Summicron-R / Leica / Leica R 50mm f2 Summicron Black | Lens / Elmar-R / Leica R 180mm f2.8 APO-Elmart Rom Black | Lens / Elmarit-R / Leica R 28mm f2.8 Elmarit Rom Black | observation_only | broad_query_ambiguity | broad R query intentionally not hard-pinned |
| r vario | Lens / R Lens / R / Summicron-R / Leica / Leica R 50mm f2 Summicron Black | Lens / Elmar-R / Leica R 180mm f2.8 APO-Elmart Rom Black | Lens / Elmarit-R / Leica R 28mm f2.8 Elmarit Rom Black | observation_only | broad_query_ambiguity | broad R query intentionally not hard-pinned |

### third_party_l_mount
| query | top1 | top2 | top3 | status | weakness | note |
|---|---|---|---|---|---|---|
| sigma 24-70 l | Lens / SL Lens / SL /  / 3rd Party / [중고] Sigma 24-70/2.8 (SL 마운트) | Lens /  / [위탁] 시그마 24-70/2.8 (SL 마운트) | Lens /  / [중고] Sigma 24-70/2.8 (SL 마운트) | pass | none |  |
| sigma 24-70 l mount | Lens / SL Lens / SL /  / 3rd Party / [중고] Sigma 24-70/2.8 (SL 마운트) | Lens /  / [위탁] 시그마 24-70/2.8 (SL 마운트) | Lens /  / [중고] Sigma 24-70/2.8 (SL 마운트) | pass | none |  |
| sigma 24-70 dg dn | Lens / SL Lens / SL /  / 3rd Party / [중고] Sigma 24-70/2.8 (SL 마운트) | Lens /  / [위탁] 시그마 24-70/2.8 (SL 마운트) | Lens /  / [중고] Sigma 24-70/2.8 (SL 마운트) | pass | none |  |
| sigma 24-70 dg dn art | Lens / SL Lens / SL /  / 3rd Party / [중고] Sigma 24-70/2.8 (SL 마운트) | Lens /  / [위탁] 시그마 24-70/2.8 (SL 마운트) | Lens /  / [중고] Sigma 24-70/2.8 (SL 마운트) | pass | none |  |
| sigma l 30mm | Lens / SL Lens / SL /  / 3rd Party / Sigma L 30mm f1.4 DC DN Black for CL, TL2, etc | Lens / Elmarit / Leica S 30mm f2.8 Elmarit ASPH CS Black | Lens / Elmarit / [위탁] Elmarit-S 30mm f/2.8 ASPH CS | pass | none |  |
| sigma 30mm l | Lens / SL Lens / SL /  / 3rd Party / Sigma L 30mm f1.4 DC DN Black for CL, TL2, etc | Lens / Elmarit / Leica S 30mm f2.8 Elmarit ASPH CS Black | Lens / Elmarit / [위탁] Elmarit-S 30mm f/2.8 ASPH CS | pass | none |  |
| sigma 14-24 l |  /  /  /  /  /  | - | - | needs_source_or_index_followup | source_coverage_gap | known third-party source coverage gap |
| sigma 14-24 l mount |  /  /  /  /  /  | - | - | needs_source_or_index_followup | source_coverage_gap | known third-party source coverage gap |
| sigma 14-24 dg dn |  /  /  /  /  /  | - | - | needs_source_or_index_followup | source_coverage_gap | known third-party source coverage gap |
| panasonic 24-105 l | Lens / SL Lens / SL /  / 3rd Party / [중고] 파나소닉 24-105 L 마운트 | - | - | pass | none |  |
| lumix 24-105 | Lens / SL Lens / SL /  / 3rd Party / [중고] 파나소닉 24-105 L 마운트 | - | - | pass | none |  |
| panasonic lumix 24-105 | Lens / SL Lens / SL /  / 3rd Party / [중고] 파나소닉 24-105 L 마운트 | - | - | pass | none |  |
| lumix s 24-105 | Lens / SL Lens / SL /  / 3rd Party / [중고] 파나소닉 24-105 L 마운트 | - | - | pass | none |  |
| lumix 24-105 f4 | Lens / SL Lens / SL /  / 3rd Party / [중고] 파나소닉 24-105 L 마운트 | - | - | pass | none |  |

### no_result_source_coverage
| query | top1 | top2 | top3 | status | weakness | note |
|---|---|---|---|---|---|---|
| sigma 14-24 l |  /  /  /  /  /  | - | - | no_result_confirmed | source_coverage_gap | no candidate found in search index / normalized / raw |
| sigma 14-24 l mount |  /  /  /  /  /  | - | - | no_result_confirmed | source_coverage_gap | no candidate found in search index / normalized / raw |
| sigma 14-24 dg dn |  /  /  /  /  /  | - | - | no_result_confirmed | source_coverage_gap | no candidate found in search index / normalized / raw |
| sigma 14-24 dg dn art |  /  /  /  /  /  | - | - | no_result_confirmed | source_coverage_gap | no candidate found in search index / normalized / raw |

### short_alias_observation
| query | top1 | top2 | top3 | status | weakness | note |
|---|---|---|---|---|---|---|
| cron | Lens / R Lens / R / Summicron-R / Leica / Leica R 50mm f2 Summicron Black | Accessory / Summicron / 신품 호환 Leica 14043 Hood Cover for M 35mm f2 Summicron, M 28mm f2.8 Elmarit | Lens / Summicron-M / Leica M 28mm f2 Summicron ASPH 6bit Safari Edition | observation_only | broad_query_ambiguity | short alias intentionally left ambiguous |
| lux | Lens / M Lens / M / Summilux-M / Leica / Leica M 28mm f1.4 Summilux ASPH 6bit Black | Lens / Summilux-M / Leica M 50mm f1.4 Summilux Classic Silver | Lens / Summilux-M / Leica M 50mm f1.4 Summilux 4th Silver | observation_only | broad_query_ambiguity | short alias intentionally left ambiguous |
| r apo | Lens / R Lens / R / Summicron-R / Leica / Leica R 50mm f2 Summicron Black | Lens / Elmar-R / Leica R 180mm f2.8 APO-Elmart Rom Black | Lens / Elmarit-R / Leica R 28mm f2.8 Elmarit Rom Black | observation_only | broad_query_ambiguity | short alias intentionally left ambiguous |
| r telyt | Lens / R Lens / R / Summicron-R / Leica / Leica R 50mm f2 Summicron Black | Lens / Elmar-R / Leica R 180mm f2.8 APO-Elmart Rom Black | Lens / Elmarit-R / Leica R 28mm f2.8 Elmarit Rom Black | observation_only | broad_query_ambiguity | short alias intentionally left ambiguous |
| r vario | Lens / R Lens / R / Summicron-R / Leica / Leica R 50mm f2 Summicron Black | Lens / Elmar-R / Leica R 180mm f2.8 APO-Elmart Rom Black | Lens / Elmarit-R / Leica R 28mm f2.8 Elmarit Rom Black | observation_only | broad_query_ambiguity | short alias intentionally left ambiguous |

### accessory_taxonomy_observation
| query | top1 | top2 | top3 | status | weakness | note |
|---|---|---|---|---|---|---|
| leica m strap | Accessory / Accessory / M / M11 / Leica / [중고] Leica M11 strap (Cognac) | Accessory / M11 / [중고] Leica M11 Neck strap (Cognac) | Accessory /  / Leica M-L adapter Black | guardrail_pass | none |  |
| sl3 battery | Accessory / Accessory / SL / Q3 / Unknown / [중고] Q3,SL3 배터리 (BP-SCL6) | Accessory / Q3 / [위탁] Q3,SL3 배터리 (BP-SCL6) | Accessory / Q3 / [중고] Q3,SL3 배터리 (BP-SCL6) | guardrail_pass | none |  |
| bp-scl6 | Accessory / Accessory / Q / Q3 / Leica / Leica Q3, SL3 Battery [BP-SCL6] | Accessory / Q3 / [중고] Q3,SL3 배터리 (BP-SCL6) | Accessory / Q3 / [위탁] Q3,SL3 배터리 (BP-SCL6) | weak_pass | accessory_taxonomy_gap | accessory result is usable but broad accessory taxonomy remains loose |
| bp-scl5 | Accessory / Accessory / Unknown / CL / Unknown / [위탁] BP-SCL5 | Accessory / M10-P / LEICA BP-SCL5 for M10/M10-p | Accessory / M10 / LEICA BP-SCL5 for M10 | weak_pass | accessory_taxonomy_gap | accessory result is usable but broad accessory taxonomy remains loose |
| leica cap | Accessory / Accessory / Unknown /  / Leica / [중고] Leitz Lens Cap E52.5 | Accessory /  / [중고] Leica Lens Cap E60 | Accessory /  / [중고] Leica Lens Cap E55 | weak_pass | accessory_taxonomy_gap | accessory result is usable but broad accessory taxonomy remains loose |
| m cap | Accessory / Accessory / M / M3 / Leica / [중고] Leica Body Cap for M3 | Accessory / M9 / Artisan & Artist M8, M9 Case Black | Accessory /  / Leica M-L adapter Black | weak_pass | accessory_taxonomy_gap | accessory result is usable but broad accessory taxonomy remains loose |
| r cap | Accessory / Accessory / R / R6 / Leica / [중고] Leica R6 가죽 케이스 | Accessory / R6 / [중고] Leica R6 가죽 케이스 | Accessory / APO-Telyt / LEICA 280mm F4 APO-TELYT-R APO-EXTENDER-R sn.3622 | weak_pass | accessory_taxonomy_gap | accessory result is usable but broad accessory taxonomy remains loose |
| sl cap | Accessory / Accessory / SL /  / Unknown / LM to L 헬리코이드 어댑터 (L 마운트용) | Accessory / SL2 / Jnk SL2 Case [Black / Battery Door Type] | Accessory / SL2 / Jnk SL2 Case [Black / Battery Door Type] | weak_pass | accessory_taxonomy_gap | accessory result is usable but broad accessory taxonomy remains loose |
| leica finder | Accessory / Accessory / Unknown /  / Leica / Leica 85mm Tele Finder C. K. S. Silver | Accessory /  / Leica R Angle Finder Black | Accessory /  / Leica 35-135mm VIOOH Finder Black | weak_pass | accessory_taxonomy_gap | accessory result is usable but broad accessory taxonomy remains loose |
| leica handgrip | Lens / M Lens / M / Elmar / Leica / Leica M 50mm f2.8 Elmar Black | Lens / Summilux-M / Leica M 28mm f1.4 Summilux ASPH 6bit Black | Lens / Summarit-M / Leica M 90mm f2.5 Summarit 6bit Black | weak_pass | accessory_taxonomy_gap | broad accessory query is still taxonomy/alias-sensitive |
| leica filter | Accessory / Accessory / Unknown /  / Leica / Leica E82 UVa II Black | Accessory /  / 신품 Leica E46 UVa II Black | Accessory /  / Leica Serie8 UV Filter (M 50/1.2(B) | weak_pass | accessory_taxonomy_gap | accessory result is usable but broad accessory taxonomy remains loose |

## 13. 수정 파일 목록
- `scripts/run_p3_query_ranking_smoke.py`
- `data/admin/p3_query_ranking_v0.md`
- `data/admin/p3_query_ranking_v0.jsonl`

## 14. 수정하지 않은 파일/영역
- `classifier_v2.py` 미수정
- `model_detector.py` 미수정
- `query_parser.py` 미수정
- `query_resolver.py` 미수정
- `search_service.py` 미수정
- taxonomy seed / canonical index 미수정
- output JSON (`results.json`, `data/normalized/normalized_latest.json`, `data/sold_items.json`) 미수정
- search index / raw data 미수정

## 15. output JSON 미수정 여부
- 이번 라운드에서 output JSON write 없음

## 16. taxonomy seed / canonical index 미수정 여부
- 이번 라운드에서 taxonomy seed / canonical index write 없음

## 17. 다음 backlog 우선순위
- `P3-ACCESSORY-TAXONOMY-COVERAGE`
- `P3-CRON-LUX-SHORT-ALIAS-POLICY`
- `P3-R-LENS-TAXONOMY-AUDIT`
- `P3-SL-ZOOM-FAMILY-TAXONOMY-AUDIT`
- `P3-THIRD-PARTY-SOURCE-COVERAGE`
- `P3-BROAD-QUERY-AMBIGUITY-UI`
- `P3-DIVERSITY-AWARE-RANKING`
