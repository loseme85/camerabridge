# P3-BROAD-QUERY-AMBIGUITY-UI

## 1. 작업 목적
- broad / ambiguous query에 대해 hard-pin 대신 UI/response-contract 관점의 disambiguation 설계
- current search ranking을 가능한 그대로 두고, refinement UI가 필요한 지점을 분리

## 2. 실행 entrypoint
- `api.search.endpoint_response`
- `search_service.load_and_search`
- `data/derived/results_search_index_v1.json`

## 3. 수정 전 문제 요약
- `summicron`, `summilux`, `cron`, `lux`, `50 cron`, broad R query, broad accessory query는 usable top1이 있어도 ambiguity가 남는다.
- `sigma 14-24 l` 계열은 UI가 아니라 source coverage gap 문제다.
- 이번 라운드는 production code 수정 없이 UI metadata 설계만 정리한다.

## 4. 총 query 수 / group별 query 수
- 총 query 수: `54`
- `broad_family_alias`: `4`
- `bare_short_alias`: `2`
- `focal_short_alias`: `6`
- `broad_r_query`: `8`
- `broad_accessory_query`: `11`
- `source_coverage_gap`: `4`
- `specific_guardrail`: `19`

## 5. status 분포
- `guardrail_pass`: `19`
- `needs_ui_disambiguation`: `25`
- `no_result_confirmed`: `4`
- `observation_only`: `2`
- `pass`: `2`
- `weak_pass`: `2`

## 6. ambiguity type 분포
- `broad_accessory_alias`: `11`
- `broad_family_alias`: `4`
- `broad_mount_alias`: `8`
- `focal_short_alias`: `6`
- `none`: `19`
- `short_alias_bare`: `2`
- `source_coverage_gap`: `4`

## 7. broad family alias 결과
| query | top1 | top2 | top3 | ambiguity | ui pattern | chips | status | notes |
|---|---|---|---|---|---|---|---|---|
| summicron | Lens / L Lens / L / Summicron / Leica / Leica L 50mm f2 Summicron Silver | Lens / L / Summicron / Leica L 50mm f2 Summicron Rigid Silver | Lens / L / Summicron / Leica L 50mm f2 Summicron Silver | broad_family_alias | refinement_chips | M Lens, R Lens, SL Lens, LTM / L Lens | needs_ui_disambiguation | lens-first is fine, but mount/focal/family refinement is needed |
| summilux | Lens / L Lens / L / Summilux / Leica / [중고] L 50/1.4 Summilux 4세대 (Silver) | Lens / L / Summilux / LEICA 50mm F1.4 SUMMILUX M39 sn.3868 | Lens / L / Summilux / LEICA 50mm F1.4 Screwmount M39 SUMMILUX-L sn.3868 | broad_family_alias | refinement_chips | M Lens, R Lens, SL Lens, LTM / L Lens | needs_ui_disambiguation | lens-first is fine, but mount/focal/family refinement is needed |
| leica summicron | Lens / L Lens / L / Summicron / Leica / Leica L 50mm f2 Summicron Silver | Lens / L / Summicron / Leica L 50mm f2 Summicron Rigid Silver | Lens / L / Summicron / Leica L 50mm f2 Summicron Silver | broad_family_alias | refinement_chips | M Lens, R Lens, SL Lens, LTM / L Lens | needs_ui_disambiguation | lens-first is fine, but mount/focal/family refinement is needed |
| leica summilux | Lens / L Lens / L / Summilux / Leica / [중고] L 50/1.4 Summilux 4세대 (Silver) | Lens / L / Summilux / LEICA 50mm F1.4 SUMMILUX M39 sn.3868 | Lens / L / Summilux / LEICA 50mm F1.4 Screwmount M39 SUMMILUX-L sn.3868 | broad_family_alias | refinement_chips | M Lens, R Lens, SL Lens, LTM / L Lens | needs_ui_disambiguation | lens-first is fine, but mount/focal/family refinement is needed |

## 8. bare short alias 결과
| query | top1 | top2 | top3 | ambiguity | ui pattern | chips | status | notes |
|---|---|---|---|---|---|---|---|---|
| cron | Lens / R Lens / R / Summicron-R / Leica / Leica R 50mm f2 Summicron Black | Accessory / M / Summicron / 신품 호환 Leica 14043 Hood Cover for M 35mm f2 Summicron, M 28mm f2.8 Elmarit | Lens / M / Summicron-M / Leica M 28mm f2 Summicron ASPH 6bit Safari Edition | short_alias_bare | family_selector | Did you mean Summicron?, Did you mean Summilux?, M, R | observation_only | collector shorthand is intentionally left ambiguous |
| lux | Lens / M Lens / M / Summilux-M / Leica / Leica M 28mm f1.4 Summilux ASPH 6bit Black | Lens / M / Summilux-M / Leica M 50mm f1.4 Summilux Classic Silver | Lens / M / Summilux-M / Leica M 50mm f1.4 Summilux 4th Silver | short_alias_bare | family_selector | Did you mean Summicron?, Did you mean Summilux?, M, R | observation_only | collector shorthand is intentionally left ambiguous |

## 9. focal short alias 결과
| query | top1 | top2 | top3 | ambiguity | ui pattern | chips | status | notes |
|---|---|---|---|---|---|---|---|---|
| 50 cron | Lens / R Lens / R / Summicron-R / Leica / Leica R 50mm f2 Summicron Black | Lens / SL / APO-Summicron / Leica SL 50mm f2 APO-Summicron ASPH Black | Lens / M / Summicron-M / Leica M 50mm f2 Summicron Rigid Silver | focal_short_alias | mount_selector | M 50 Summicron, R 50 Summicron, SL 50 Summicron, Show all 50mm | needs_ui_disambiguation | mount ambiguity across M/R/SL is high |
| leica 50 cron | Lens / R Lens / R / Summicron-R / Leica / Leica R 50mm f2 Summicron Black | Lens / SL / APO-Summicron / Leica SL 50mm f2 APO-Summicron ASPH Black | Lens / M / Summicron-M / Leica M 50mm f2 Summicron Rigid Silver | focal_short_alias | mount_selector | M 50 Summicron, R 50 Summicron, SL 50 Summicron, Show all 50mm | needs_ui_disambiguation | mount ambiguity across M/R/SL is high |
| 35 lux | Lens / M Lens / M / Summilux-M / Leica / Leica M 35mm f1.4 Summilux 2nd Titan | Lens / M / Summilux-M / Leica M 35mm f1.4 Summilux 1st Silver [Steel Rim] | Lens / M / Summilux-M / Leica M 35mm f1.4 Summilux ASPH 4th Titan | focal_short_alias | no_disambiguation_needed | M 35 Summilux, 35mm, ASPH, Show all 35mm | pass | useful M Summilux shorthand |
| 50 lux | Lens / M Lens / M / Summilux-M / Leica / Leica M 50mm f1.4 Summilux Classic Silver | Lens / M / Summilux-M / Leica M 50mm f1.4 Summilux 4th Silver | Lens / M / Summilux-M / Leica M 50mm f1.4 Summilux ASPH 6bit Silver | focal_short_alias | no_disambiguation_needed | M 50 Summilux, 50mm, ASPH, Show all 50mm | pass | useful M Summilux shorthand |
| leica 35 lux | Lens / M Lens / M / Summilux-M / Leica / Leica M 35mm f1.4 Summilux 2nd Titan | Lens / M / Summilux-M / Leica M 35mm f1.4 Summilux 1st Silver [Steel Rim] | Lens / M / Summilux-M / Leica M 35mm f1.4 Summilux ASPH 4th Titan | focal_short_alias | refinement_chips | M 35 Summilux, 35mm, ASPH, Show all 35mm | weak_pass | works well, but still collector shorthand |
| leica 50 lux | Lens / M Lens / M / Summilux-M / Leica / Leica M 50mm f1.4 Summilux Classic Silver | Lens / M / Summilux-M / Leica M 50mm f1.4 Summilux 4th Silver | Lens / M / Summilux-M / Leica M 50mm f1.4 Summilux ASPH 6bit Silver | focal_short_alias | refinement_chips | M 50 Summilux, 50mm, ASPH, Show all 50mm | weak_pass | works well, but still collector shorthand |

## 10. broad R query 결과
| query | top1 | top2 | top3 | ambiguity | ui pattern | chips | status | notes |
|---|---|---|---|---|---|---|---|---|
| leica r | Lens / R Lens / R / Summicron-R / Leica / Leica R 50mm f2 Summicron Black | Lens / R / Elmar-R / Leica R 180mm f2.8 APO-Elmart Rom Black | Lens / R / Elmarit-R / Leica R 28mm f2.8 Elmarit Rom Black | broad_mount_alias | family_selector | Summicron-R, Elmarit-R, APO-Telyt-R, Vario-Elmarit-R | needs_ui_disambiguation | broad R query should offer family/focal refinement |
| r lens | Lens / R Lens / R / Summicron-R / Leica / Leica R 50mm f2 Summicron Black | Lens / R / Elmar-R / Leica R 180mm f2.8 APO-Elmart Rom Black | Lens / R / Elmarit-R / Leica R 28mm f2.8 Elmarit Rom Black | broad_mount_alias | family_selector | Summicron-R, Elmarit-R, APO-Telyt-R, Vario-Elmarit-R | needs_ui_disambiguation | broad R query should offer family/focal refinement |
| r summicron | Lens / R Lens / R / Summicron-R / Leica / Leica R 50mm f2 Summicron Black | Lens / R / Summicron-R / [위탁] R 50/2 Summicron (Black) | Lens / R / Summicron-R / [위탁] R 35/2 Summicron (Black) | broad_mount_alias | family_selector | Summicron-R, Elmarit-R, APO-Telyt-R, Vario-Elmarit-R | needs_ui_disambiguation | broad R query should offer family/focal refinement |
| r elmarit | Lens / R Lens / R / Elmarit-R / Leica / Leica R 28mm f2.8 Elmarit Rom Black | Lens / R / APO-Macro-Elmarit-R / Leica R 70-180mm f2.8 Vario-Apo-Elmarit Black | Lens / R / APO-Macro-Elmarit / Leica R 100mm f2.8 APO-Macro-Elmarit Black | broad_mount_alias | family_selector | Summicron-R, Elmarit-R, APO-Telyt-R, Vario-Elmarit-R | needs_ui_disambiguation | broad R query should offer family/focal refinement |
| r apo | Lens / R Lens / R / Summicron-R / Leica / Leica R 50mm f2 Summicron Black | Lens / R / Elmar-R / Leica R 180mm f2.8 APO-Elmart Rom Black | Lens / R / Elmarit-R / Leica R 28mm f2.8 Elmarit Rom Black | broad_mount_alias | family_selector | Summicron-R, Elmarit-R, APO-Telyt-R, Vario-Elmarit-R | needs_ui_disambiguation | broad R query should offer family/focal refinement |
| r telyt | Lens / R Lens / R / Summicron-R / Leica / Leica R 50mm f2 Summicron Black | Lens / R / Elmar-R / Leica R 180mm f2.8 APO-Elmart Rom Black | Lens / R / Elmarit-R / Leica R 28mm f2.8 Elmarit Rom Black | broad_mount_alias | family_selector | Summicron-R, Elmarit-R, APO-Telyt-R, Vario-Elmarit-R | needs_ui_disambiguation | broad R query should offer family/focal refinement |
| r vario | Lens / R Lens / R / Summicron-R / Leica / Leica R 50mm f2 Summicron Black | Lens / R / Elmar-R / Leica R 180mm f2.8 APO-Elmart Rom Black | Lens / R / Elmarit-R / Leica R 28mm f2.8 Elmarit Rom Black | broad_mount_alias | family_selector | Summicron-R, Elmarit-R, APO-Telyt-R, Vario-Elmarit-R | needs_ui_disambiguation | broad R query should offer family/focal refinement |
| leica r 28-90 | Lens / R Lens / R / Summicron-R / Leica / Leica R 50mm f2 Summicron Black | Lens / R / Elmar-R / Leica R 180mm f2.8 APO-Elmart Rom Black | Lens / R / Elmarit-R / Leica R 28mm f2.8 Elmarit Rom Black | broad_mount_alias | family_selector | Summicron-R, Elmarit-R, APO-Telyt-R, Vario-Elmarit-R | needs_ui_disambiguation | broad R query should offer family/focal refinement |

## 11. broad accessory query 결과
| query | top1 | top2 | top3 | ambiguity | ui pattern | chips | status | notes |
|---|---|---|---|---|---|---|---|---|
| leica cap | Accessory / Accessory / Unknown /  / Leica / [중고] Leitz Lens Cap E52.5 | Accessory / Unknown /  / [중고] Leica Lens Cap E60 | Accessory / Unknown /  / [중고] Leica Lens Cap E55 | broad_accessory_alias | accessory_subtype_selector | Battery, Cap, Lens Cap, Body Cap | needs_ui_disambiguation | accessory-first is correct, but subtype precision needs UI refinement |
| leica battery | Accessory / Accessory / M / M11 / Leica / Leica M11 Battery Silver [BP-SCL7] | Accessory / Q / Q3 / Leica Q3, SL3 Battery [BP-SCL6] | Accessory / M / M11 / Leica M11 Battery Silver [BP-SCL7] | broad_accessory_alias | accessory_subtype_selector | Battery, Cap, Lens Cap, Body Cap | needs_ui_disambiguation | accessory-first is correct, but subtype precision needs UI refinement |
| leica strap | Accessory / Accessory / Unknown /  / Leica / 신품 Leica Paracord Strap Black / Red 126cm created by COOPH | Accessory / Unknown /  / [위탁] Leica Carrying Strap (Black) | Accessory / Unknown /  / [중고] Cooph Leica Paracord Handstrap (Red) | broad_accessory_alias | accessory_subtype_selector | Battery, Cap, Lens Cap, Body Cap | needs_ui_disambiguation | accessory-first is correct, but subtype precision needs UI refinement |
| leica hood | Accessory / Accessory / Unknown /  / Leica / Leica 12538 Hood Black | Accessory / M / Elmar / Leica 12549 Hood Silver [for M 50mm f2.8 Elmar] | Accessory / M /  / Leica 12585 Hood for M-50mm, 35mm | broad_accessory_alias | accessory_subtype_selector | Battery, Cap, Lens Cap, Body Cap | needs_ui_disambiguation | accessory-first is correct, but subtype precision needs UI refinement |
| leica adapter | Accessory / Accessory / M /  / Leica / Leica M-L adapter Black | Accessory / M /  / Leica M-L adapter Black | Accessory / Unknown /  / Leica R-M Adapter | broad_accessory_alias | accessory_subtype_selector | Battery, Cap, Lens Cap, Body Cap | needs_ui_disambiguation | accessory-first is correct, but subtype precision needs UI refinement |
| leica filter | Accessory / Accessory / Unknown /  / Leica / Leica E82 UVa II Black | Accessory / Unknown /  / 신품 Leica E46 UVa II Black | Accessory / M /  / Leica Serie8 UV Filter (M 50/1.2(B) | broad_accessory_alias | accessory_subtype_selector | Battery, Cap, Lens Cap, Body Cap | needs_ui_disambiguation | accessory-first is correct, but subtype precision needs UI refinement |
| leica finder | Accessory / Accessory / Unknown /  / Leica / Leica 85mm Tele Finder C. K. S. Silver | Accessory / Unknown /  / Leica R Angle Finder Black | Accessory / Unknown /  / Leica 35-135mm VIOOH Finder Black | broad_accessory_alias | accessory_subtype_selector | Battery, Cap, Lens Cap, Body Cap | needs_ui_disambiguation | accessory-first is correct, but subtype precision needs UI refinement |
| body cap | Accessory / Accessory / Unknown /  / Leica / [중고] Leitz Lens Cap E52.5 | Accessory / Unknown /  / [중고] Leica Lens Cap E60 | Accessory / Unknown /  / [중고] Leica Lens Cap E55 | broad_accessory_alias | accessory_subtype_selector | Battery, Cap, Lens Cap, Body Cap | needs_ui_disambiguation | accessory-first is correct, but subtype precision needs UI refinement |
| lens cap | Accessory / Accessory / Unknown /  / Leica / [중고] Leitz Lens Cap E52.5 | Accessory / Unknown /  / [중고] Leica Lens Cap E60 | Accessory / Unknown /  / [중고] Leica Lens Cap E55 | broad_accessory_alias | accessory_subtype_selector | Battery, Cap, Lens Cap, Body Cap | needs_ui_disambiguation | accessory-first is correct, but subtype precision needs UI refinement |
| rear cap | Accessory / Accessory / Unknown /  / Leica / [중고] Leitz Lens Cap E52.5 | Accessory / Unknown /  / [중고] Leica Lens Cap E60 | Accessory / Unknown /  / [중고] Leica Lens Cap E55 | broad_accessory_alias | accessory_subtype_selector | Battery, Cap, Lens Cap, Body Cap | needs_ui_disambiguation | accessory-first is correct, but subtype precision needs UI refinement |
| front cap | Accessory / Accessory / Unknown /  / Leica / [중고] Leitz Lens Cap E52.5 | Accessory / Unknown /  / [중고] Leica Lens Cap E60 | Accessory / Unknown /  / [중고] Leica Lens Cap E55 | broad_accessory_alias | accessory_subtype_selector | Battery, Cap, Lens Cap, Body Cap | needs_ui_disambiguation | accessory-first is correct, but subtype precision needs UI refinement |

## 12. source coverage gap 결과
| query | top1 | top2 | top3 | ambiguity | ui pattern | chips | status | notes |
|---|---|---|---|---|---|---|---|---|
| sigma 14-24 l |  /  /  /  /  /  | - | - | source_coverage_gap | no_result_alert_signup | Sigma L mount, Sigma 14-24, L mount wide zoom, Alert me | no_result_confirmed | known source coverage gap; fake fill should stay disabled |
| sigma 14-24 l mount |  /  /  /  /  /  | - | - | source_coverage_gap | no_result_alert_signup | Sigma L mount, Sigma 14-24, L mount wide zoom, Alert me | no_result_confirmed | known source coverage gap; fake fill should stay disabled |
| sigma 14-24 dg dn |  /  /  /  /  /  | - | - | source_coverage_gap | no_result_alert_signup | Sigma L mount, Sigma 14-24, L mount wide zoom, Alert me | no_result_confirmed | known source coverage gap; fake fill should stay disabled |
| sigma 14-24 dg dn art |  /  /  /  /  /  | - | - | source_coverage_gap | no_result_alert_signup | Sigma L mount, Sigma 14-24, L mount wide zoom, Alert me | no_result_confirmed | known source coverage gap; fake fill should stay disabled |

## 13. specific guardrail 결과
| query | top1 | top2 | top3 | ambiguity | ui pattern | chips | status | notes |
|---|---|---|---|---|---|---|---|---|
| m 50 cron | Lens / M Lens / M / Summicron-M / Leica / Leica M 50mm f2 Summicron Rigid Silver | Lens / M / APO-Summicron / Leica M 50mm f2 APO-Summicron ASPH Black Chrome finish | Lens / M / Summicron-M / Leica M 50mm f 2 Summicron Rigid BlackRepaint | none | no_disambiguation_needed |  | guardrail_pass | explicit mount shorthand guardrail holds |
| r 50 cron | Lens / R Lens / R / Summicron-R / Leica / Leica R 50mm f2 Summicron Black | Lens / R / Summicron-R / LEICA 50mm F2 SUMMICRON-R sn.3338 | Lens / R / Summicron-R / LEICA 50mm F2 ROM SUMMICRON-R sn.3819 | none | no_disambiguation_needed |  | guardrail_pass | explicit mount shorthand guardrail holds |
| sl 50 cron | Lens / SL Lens / SL / APO-Summicron / Leica / Leica SL 50mm f2 APO-Summicron ASPH Black | Lens / SL / Summicron-SL / [위탁] Leica SL2-S Kit with Summicron-SL 50mm f/2 ASPH | Lens / SL / Summicron-SL / [중고] Leica Summicron-SL 50mm f/2 ASPH | none | no_disambiguation_needed |  | guardrail_pass | explicit mount shorthand guardrail holds |
| m 35 lux | Lens / M Lens / M / Summilux-M / Leica / Leica M 35mm f1.4 Summilux 2nd Titan | Lens / M / Summilux-M / Leica M 35mm f1.4 Summilux 1st Silver [Steel Rim] | Lens / M / Summilux-M / Leica M 35mm f1.4 Summilux ASPH 4th Titan | none | no_disambiguation_needed |  | guardrail_pass | explicit mount shorthand guardrail holds |
| m 50 lux | Lens / M Lens / M / Summilux-M / Leica / Leica M 50mm f1.4 Summilux Classic Silver | Lens / M / Summilux-M / Leica M 50mm f1.4 Summilux 4th Silver | Lens / M / Summilux-M / Leica M 50mm f1.4 Summilux ASPH 6bit Silver | none | no_disambiguation_needed |  | guardrail_pass | explicit mount shorthand guardrail holds |
| summicron m 50 | Lens / M Lens / M / Summicron-M / Leica / Leica M 50mm f2 Summicron Rigid Silver | Lens / M / APO-Summicron / Leica M 50mm f2 APO-Summicron ASPH Black Chrome finish | Lens / M / Summicron-M / Leica M 50mm f 2 Summicron Rigid BlackRepaint | none | no_disambiguation_needed |  | guardrail_pass | specific query guardrail holds |
| m 50 summicron | Lens / M Lens / M / Summicron-M / Leica / Leica M 50mm f2 Summicron Rigid Silver | Lens / M / APO-Summicron / Leica M 50mm f2 APO-Summicron ASPH Black Chrome finish | Lens / M / Summicron-M / Leica M 50mm f 2 Summicron Rigid BlackRepaint | none | no_disambiguation_needed |  | guardrail_pass | specific query guardrail holds |
| r 50 summicron | Lens / R Lens / R / Summicron-R / Leica / Leica R 50mm f2 Summicron Black | Lens / R / Summicron-R / LEICA 50mm F2 SUMMICRON-R sn.3338 | Lens / R / Summicron-R / LEICA 50mm F2 ROM SUMMICRON-R sn.3819 | none | no_disambiguation_needed |  | guardrail_pass | specific query guardrail holds |
| summicron-r 50 | Lens / R Lens / R / Summicron-R / Leica / Leica R 50mm f2 Summicron Black | Lens / R / Summicron-R / LEICA 50mm F2 SUMMICRON-R sn.3338 | Lens / R / Summicron-R / LEICA 50mm F2 ROM SUMMICRON-R sn.3819 | none | no_disambiguation_needed |  | guardrail_pass | specific query guardrail holds |
| summicron sl 35 | Lens / SL Lens / SL / Summicron-SL / Leica / 신품 Leica SL 35mm f2 Summicron ASPH Black | Lens / SL / Summicron-SL / [중고] Leica SL2 with Summicron-SL 35mm f/2 ASPH | Lens / SL / APO-Summicron / LEICA 35mm F2 ASPH APO-SUMMICRON-SL sn.4720 | none | no_disambiguation_needed |  | guardrail_pass | specific query guardrail holds |
| sl 50 summicron | Lens / SL Lens / SL / APO-Summicron / Leica / Leica SL 50mm f2 APO-Summicron ASPH Black | Lens / SL / Summicron-SL / [위탁] Leica SL2-S Kit with Summicron-SL 50mm f/2 ASPH | Lens / SL / Summicron-SL / [중고] Leica Summicron-SL 50mm f/2 ASPH | none | no_disambiguation_needed |  | guardrail_pass | specific query guardrail holds |
| sl 24-90 | Lens / SL Lens / SL / Vario-Elmarit-SL / Leica / Leica SL 24-90mm f2.8-4 Vario-Elmarit Black | Lens / SL / Vario-Elmarit-SL / Leica SL 24-90mm f2.8-4 Vario-Elmarit Black | Lens / SL / Vario-Elmarit-SL / [위탁] SL 24-90/2.8-4 Vario Elmar ASPH (Black) | none | no_disambiguation_needed |  | guardrail_pass | specific query guardrail holds |
| sl 90-280 | Lens / SL Lens / SL / APO-Vario-Elmarit-SL / Leica / [중고] SL APO Vario Elmarit 90-280 f/2.8-4 | Lens / SL / APO-Vario-Elmarit-SL / [중고] SL APO Vario Elmarit 90-280 f/2.8-4 | Lens / SL / APO-Vario-Elmarit-SL / [중고] SL 90-280/2.8-4 APO Vario Elmarit ASPH (Black) | none | no_disambiguation_needed |  | guardrail_pass | specific query guardrail holds |
| leica sl2 | Body / SL Body / SL / SL2 / Leica / Leica SL2 Black | Body / SL / SL2 / Leica SL2 Black | Body / SL / SL2 / Leica SL2-S Reporter | none | no_disambiguation_needed |  | guardrail_pass | body guardrail holds |
| leica sl3 | Body / SL Body / SL / SL3 / Leica / Leica SL3 Black | Body / SL / SL3 / Leica SL3 Reporter | Body / SL / SL3 / Leica SL3 Body Only | none | no_disambiguation_needed |  | guardrail_pass | body guardrail holds |
| sl3 battery | Accessory / Accessory / SL / Q3 / Unknown / [중고] Q3,SL3 배터리 (BP-SCL6) | Accessory / SL / Q3 / [위탁] Q3,SL3 배터리 (BP-SCL6) | Accessory / SL / Q3 / [중고] Q3,SL3 배터리 (BP-SCL6) | none | no_disambiguation_needed |  | guardrail_pass | accessory guardrail holds |
| leica handgrip | Accessory / Accessory / SL / CL / Leica / Leica CL handgrip Black | Accessory / M / M10 / Leica M10 Handgrip Black | Accessory / M / M10 / Leica M10 Handgrip Black | none | no_disambiguation_needed |  | guardrail_pass | accessory guardrail holds |
| panasonic 24-105 l | Lens / SL Lens / SL /  / 3rd Party / [중고] 파나소닉 24-105 L 마운트 | - | - | none | no_disambiguation_needed |  | guardrail_pass | third-party guardrail holds |
| lumix 24-105 | Lens / SL Lens / SL /  / 3rd Party / [중고] 파나소닉 24-105 L 마운트 | - | - | none | no_disambiguation_needed |  | guardrail_pass | third-party guardrail holds |

## 14. query별 recommended UI patterns
- broad family alias: `refinement_chips`
- bare short alias: `family_selector`
- focal short alias (`50 cron`): `mount_selector`
- usable focal lux shorthand (`35 lux`, `50 lux`): `no_disambiguation_needed`
- broad R query: `family_selector`
- broad accessory query: `accessory_subtype_selector`
- source coverage gap: `no_result_alert_signup`

## 15. query별 recommended chips / filters
- broad family alias chips: `M Lens`, `R Lens`, `SL Lens`, `35mm`, `50mm`, `90mm`, `APO`, `ASPH`
- bare short alias chips: `Did you mean Summicron?`, `Did you mean Summilux?`, `M`, `R`, `SL`, `Show only lenses`
- focal cron chips: `M 50 Summicron`, `R 50 Summicron`, `SL 50 Summicron`, `Show all 50mm`
- focal lux chips: `M 35 Summilux`, `M 50 Summilux`, `35mm`, `50mm`, `ASPH`
- broad R chips: `Summicron-R`, `Elmarit-R`, `APO-Telyt-R`, `Vario-Elmarit-R`, `28mm`, `50mm`, `90mm`, `180mm`
- broad accessory chips: `Battery`, `Cap`, `Lens Cap`, `Body Cap`, `Filter`, `Finder`, `Hood`, `Adapter`, `M`, `R`, `SL`, `Q`

## 16. no-result alert/signup 후보
- `sigma 14-24 l`: `no_result_confirmed` / `source_coverage_gap` / `no_result_alert_signup` - known source coverage gap; fake fill should stay disabled
- `sigma 14-24 l mount`: `no_result_confirmed` / `source_coverage_gap` / `no_result_alert_signup` - known source coverage gap; fake fill should stay disabled
- `sigma 14-24 dg dn`: `no_result_confirmed` / `source_coverage_gap` / `no_result_alert_signup` - known source coverage gap; fake fill should stay disabled
- `sigma 14-24 dg dn art`: `no_result_confirmed` / `source_coverage_gap` / `no_result_alert_signup` - known source coverage gap; fake fill should stay disabled

## 17. implementation backlog
- `P3-BROAD-QUERY-AMBIGUITY-UI-IMPLEMENTATION`: response metadata (`ambiguity_type`, `recommended_ui_pattern`, `recommended_chips`, `suggested_filters`) 실제 API 계약으로 노출
- `P3-DIVERSITY-AWARE-RANKING`: broad query top3 다양성 개선
- `P3-ACCESSORY-SUBTYPE-PRECISION`: broad accessory query subtype precision 개선

## 18. 수정 파일 목록
- `scripts/run_p3_broad_query_ambiguity_ui.py`
- `data/admin/p3_broad_query_ambiguity_ui_v0.md`
- `data/admin/p3_broad_query_ambiguity_ui_v0.jsonl`

## 19. 수정하지 않은 파일/영역
- `classifier_v2.py`
- `model_detector.py`
- `query_parser.py`
- `query_resolver.py`
- `search_service.py`
- taxonomy seed / canonical index
- output JSON / normalized / sold_items / results.json

## 20. 남은 위험
- `summicron`: `needs_ui_disambiguation` / `broad_family_alias` / `refinement_chips` - lens-first is fine, but mount/focal/family refinement is needed
- `summilux`: `needs_ui_disambiguation` / `broad_family_alias` / `refinement_chips` - lens-first is fine, but mount/focal/family refinement is needed
- `leica summicron`: `needs_ui_disambiguation` / `broad_family_alias` / `refinement_chips` - lens-first is fine, but mount/focal/family refinement is needed
- `leica summilux`: `needs_ui_disambiguation` / `broad_family_alias` / `refinement_chips` - lens-first is fine, but mount/focal/family refinement is needed
- `50 cron`: `needs_ui_disambiguation` / `focal_short_alias` / `mount_selector` - mount ambiguity across M/R/SL is high
- `leica 50 cron`: `needs_ui_disambiguation` / `focal_short_alias` / `mount_selector` - mount ambiguity across M/R/SL is high
- `leica r`: `needs_ui_disambiguation` / `broad_mount_alias` / `family_selector` - broad R query should offer family/focal refinement
- `r lens`: `needs_ui_disambiguation` / `broad_mount_alias` / `family_selector` - broad R query should offer family/focal refinement
- `r summicron`: `needs_ui_disambiguation` / `broad_mount_alias` / `family_selector` - broad R query should offer family/focal refinement
- `r elmarit`: `needs_ui_disambiguation` / `broad_mount_alias` / `family_selector` - broad R query should offer family/focal refinement
- `r apo`: `needs_ui_disambiguation` / `broad_mount_alias` / `family_selector` - broad R query should offer family/focal refinement
- `r telyt`: `needs_ui_disambiguation` / `broad_mount_alias` / `family_selector` - broad R query should offer family/focal refinement
