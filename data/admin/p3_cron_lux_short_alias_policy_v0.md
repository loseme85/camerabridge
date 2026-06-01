# P3-CRON-LUX-SHORT-ALIAS-POLICY

## 1. 작업 목적
- `cron / lux` short alias의 search-layer policy 경계 정리
- bare alias는 hard-pin하지 않고 observation-first로 유지
- focal + alias와 explicit mount + alias의 경계를 구분

## 2. 실행 entrypoint
- `api.search.endpoint_response`
- `search_service.load_and_search`
- `data/derived/results_search_index_v1.json`

## 3. 수정 전 문제 요약
- `cron`, `lux`는 Lens-first지만 collector shorthand ambiguity가 크다.
- `50 cron`은 M / R / SL 50 Summicron 후보가 모두 붙을 수 있어 mount hard-pin이 위험하다.
- `35 lux`, `50 lux`는 현재 M Summilux-M 쪽으로 자연스럽게 회수되지만, bare alias 정책과 분리해 다뤄야 한다.

## 4. short alias policy 결론
- bare `cron`, `lux`: `observation_only` 유지. Lens-first만 보장하고 특정 mount/focal/family hard-pin 금지.
- focal + `lux`: explicit non-M token이 없을 때 collector shorthand로서 M Summilux-M 우선 허용 가능.
- focal + `cron`: `50 cron`, `35 cron`, `90 cron` 등은 Lens-side 유지까지만 허용하고 mount hard-pin 금지.
- explicit mount + short alias: `m/r/sl` token이 있으면 해당 mount가 우선한다.
- broad family alias (`summicron`, `summilux`)는 short alias와 별도 정책으로 Lens-first 유지.

## 5. target / observation query before 결과
| query | top1 | top2 | top3 | status | policy | cause | note |
|---|---|---|---|---|---|---|---|
| cron | Lens / R Lens / R / Summicron-R / Leica / Leica R 50mm f2 Summicron Black | Accessory / M / Summicron / Leica / 신품 호환 Leica 14043 Hood Cover for M 35mm f2 Summicron, M 28mm f2.8 Elmarit | Lens / M / Summicron-M / Leica / Leica M 28mm f2 Summicron ASPH 6bit Safari Edition | observation_only | bare_alias_observation_only | short_alias_ambiguity | bare cron stays lens-first but remains ambiguous across M/R/SL |
| lux | Lens / M Lens / M / Summilux-M / Leica / Leica M 28mm f1.4 Summilux ASPH 6bit Black | Lens / M / Summilux-M / Leica / Leica M 50mm f1.4 Summilux Classic Silver | Lens / M / Summilux-M / Leica / Leica M 50mm f1.4 Summilux 4th Silver | observation_only | bare_alias_observation_only | short_alias_ambiguity | bare lux stays lens-first but remains ambiguous across focals |
| 50 cron | Lens / R Lens / R / Summicron-R / Leica / Leica R 50mm f2 Summicron Black | Lens / SL / APO-Summicron / Leica / Leica SL 50mm f2 APO-Summicron ASPH Black | Lens / M / Summicron-M / Leica / Leica M 50mm f2 Summicron Rigid Silver | weak_pass | focal_cron_ambiguous | short_alias_ambiguity | 50 cron stays lens-side but mount ambiguity remains M/R/SL |
| 35 lux | Lens / M Lens / M / Summilux-M / Leica / Leica M 35mm f1.4 Summilux 2nd Titan | Lens / M / Summilux-M / Leica / Leica M 35mm f1.4 Summilux 1st Silver [Steel Rim] | Lens / M / Summilux-M / Leica / Leica M 35mm f1.4 Summilux ASPH 4th Titan | pass | focal_lux_m_shorthand_allowed | no_change_needed | focal + lux behaves like useful M Summilux shorthand |
| 50 lux | Lens / M Lens / M / Summilux-M / Leica / Leica M 50mm f1.4 Summilux Classic Silver | Lens / M / Summilux-M / Leica / Leica M 50mm f1.4 Summilux 4th Silver | Lens / M / Summilux-M / Leica / Leica M 50mm f1.4 Summilux ASPH 6bit Silver | pass | focal_lux_m_shorthand_allowed | no_change_needed | focal + lux behaves like useful M Summilux shorthand |

| query | top1 | top2 | top3 | status | policy | cause | note |
|---|---|---|---|---|---|---|---|
| 28 cron | Lens / M Lens / M / Summicron-M / Leica / Leica M 28mm f2 Summicron ASPH 6bit Safari Edition | Lens / M / Summicron-M / Leica / Leica M 28mm f2 Summicron ASPH 6bit Black | Lens / M / Summicron-M / Leica / Leica M 28mm f2 Summicron ASPH 6bit Titan | weak_pass | focal_cron_ambiguous | short_alias_ambiguity | focal + cron remains ambiguous without explicit mount |
| 35 cron | Lens / M Lens / M / APO-Summicron / Leica / Leica M 35mm f2 APO-Summicron ASPH 6bit Black | Lens / M / Summicron-M / Leica / Leica M 35mm f2 Summicron ASPH Anthracite Finish | Lens / SL / Summicron-SL / Leica / 신품 Leica SL 35mm f2 Summicron ASPH Black | weak_pass | focal_cron_ambiguous | short_alias_ambiguity | focal + cron remains ambiguous without explicit mount |
| 90 cron | Lens / M Lens / M / APO-Summicron / Leica / Leica M 90mm f2 APO-Summicron ASPH Black | Lens / M / Summicron-M / Leica / LEICA 90mm F2 SUMMICRON-M sn.3703 | Lens / M / APO-Summicron / Leica / LEICA 90mm F2 ASPH (6bit) APO-SUMMICRON-M sn.4208 | weak_pass | focal_cron_ambiguous | short_alias_ambiguity | focal + cron remains ambiguous without explicit mount |
| 21 lux | Lens / M Lens / M / Summilux-M / Leica / Leica M 21mm f1.4 Summilux ASPH 6bit Black | Lens / M / Summilux-M / Leica / LEICA 21mm F1.4 ASPH SUMMILUX-M sn.4083 | Lens / M / Summilux-M / Leica / LEICA 21mm F1.4 ASPH SUMMILUX-M sn.4089 | weak_pass | focal_lux_m_shorthand_allowed | short_alias_ambiguity | focal + lux looks useful but remains collector shorthand |
| 24 lux | Lens / M Lens / M / Summilux-M / Leica / LEICA 24mm F1.4 ASPH SUMMILUX-M sn.4651 | Lens / M / Summilux-M / Leica / LEICA 24mm F1.4 ASPH SUMMILUX-M sn.4079 | Lens / M / Summilux-M / Leica / LEICA 24mm F1.4 ASPH SUMMILUX-M sn.4088 | weak_pass | focal_lux_m_shorthand_allowed | short_alias_ambiguity | focal + lux looks useful but remains collector shorthand |
| 28 lux | Lens / M Lens / M / Summilux-M / Leica / Leica M 28mm f1.4 Summilux ASPH 6bit Black | Lens / M / Summilux-M / Leica / 신품 Leica M 28mm f1.4 Summilux ASPH 6bit Black | Lens / M / Summilux-M / Leica / LEICA 28mm F1.4 ASPH SUMMILUX-M sn.4205 | weak_pass | focal_lux_m_shorthand_allowed | short_alias_ambiguity | focal + lux looks useful but remains collector shorthand |
| 75 lux | Lens / M Lens / M / Summilux-M / Leica / Leica M 75mm f1.4 Summilux [Made in Germany] | Lens / M / Summilux-M / Leica / Leica M 75mm f1.4 Summilux [Made in Germany] | Lens / M / Summilux-M / Leica / LEICA 75mm F1.4 SUMMILUX-M sn.3259 | weak_pass | focal_lux_m_shorthand_allowed | short_alias_ambiguity | focal + lux looks useful but remains collector shorthand |
| m 35 lux | Lens / M Lens / M / Summilux-M / Leica / Leica M 35mm f1.4 Summilux 2nd Titan | Lens / M / Summilux-M / Leica / Leica M 35mm f1.4 Summilux 1st Silver [Steel Rim] | Lens / M / Summilux-M / Leica / Leica M 35mm f1.4 Summilux ASPH 4th Titan | guardrail_pass | explicit_mount_wins | no_change_needed | explicit M token wins as intended |
| m 50 lux | Lens / M Lens / M / Summilux-M / Leica / Leica M 50mm f1.4 Summilux Classic Silver | Lens / M / Summilux-M / Leica / Leica M 50mm f1.4 Summilux 4th Silver | Lens / M / Summilux-M / Leica / Leica M 50mm f1.4 Summilux ASPH 6bit Silver | guardrail_pass | explicit_mount_wins | no_change_needed | explicit M token wins as intended |
| m 50 cron | Lens / M Lens / M / Summicron-M / Leica / Leica M 50mm f2 Summicron Rigid Silver | Lens / M / APO-Summicron / Leica / Leica M 50mm f2 APO-Summicron ASPH Black Chrome finish | Lens / M / Summicron-M / Leica / Leica M 50mm f 2 Summicron Rigid BlackRepaint | guardrail_pass | explicit_mount_wins | no_change_needed | explicit M token wins as intended |
| r 50 cron | Lens / R Lens / R / Summicron-R / Leica / Leica R 50mm f2 Summicron Black | Lens / R / Summicron-R / Leica / LEICA 50mm F2 SUMMICRON-R sn.3338 | Lens / R / Summicron-R / Leica / LEICA 50mm F2 ROM SUMMICRON-R sn.3819 | guardrail_pass | explicit_mount_wins | no_change_needed | explicit R token wins as intended |
| sl 50 cron | Lens / SL Lens / SL / APO-Summicron / Leica / Leica SL 50mm f2 APO-Summicron ASPH Black | Lens / SL / Summicron-SL / Leica / [위탁] Leica SL2-S Kit with Summicron-SL 50mm f/2 ASPH | Lens / SL / Summicron-SL / Leica / [중고] Leica Summicron-SL 50mm f/2 ASPH | guardrail_pass | explicit_mount_wins | no_change_needed | explicit SL token wins as intended |
| leica 35 lux | Lens / M Lens / M / Summilux-M / Leica / Leica M 35mm f1.4 Summilux 2nd Titan | Lens / M / Summilux-M / Leica / Leica M 35mm f1.4 Summilux 1st Silver [Steel Rim] | Lens / M / Summilux-M / Leica / Leica M 35mm f1.4 Summilux ASPH 4th Titan | weak_pass | focal_lux_m_shorthand_allowed | short_alias_ambiguity | focal + lux looks useful but remains collector shorthand |
| leica 50 lux | Lens / M Lens / M / Summilux-M / Leica / Leica M 50mm f1.4 Summilux Classic Silver | Lens / M / Summilux-M / Leica / Leica M 50mm f1.4 Summilux 4th Silver | Lens / M / Summilux-M / Leica / Leica M 50mm f1.4 Summilux ASPH 6bit Silver | weak_pass | focal_lux_m_shorthand_allowed | short_alias_ambiguity | focal + lux looks useful but remains collector shorthand |
| leica 50 cron | Lens / R Lens / R / Summicron-R / Leica / Leica R 50mm f2 Summicron Black | Lens / SL / APO-Summicron / Leica / Leica SL 50mm f2 APO-Summicron ASPH Black | Lens / M / Summicron-M / Leica / Leica M 50mm f2 Summicron Rigid Silver | weak_pass | focal_cron_ambiguous | short_alias_ambiguity | focal + cron remains ambiguous without explicit mount |

## 6. target / observation query after 결과
- 이번 라운드는 production code 수정 없이 policy/documentation round로 진행했다.
- 따라서 before/after search response는 동일하며, current behavior를 정책 기준으로 분류했다.

| query | top1 | top2 | top3 | status | policy | cause | note |
|---|---|---|---|---|---|---|---|
| cron | Lens / R Lens / R / Summicron-R / Leica / Leica R 50mm f2 Summicron Black | Accessory / M / Summicron / Leica / 신품 호환 Leica 14043 Hood Cover for M 35mm f2 Summicron, M 28mm f2.8 Elmarit | Lens / M / Summicron-M / Leica / Leica M 28mm f2 Summicron ASPH 6bit Safari Edition | observation_only | bare_alias_observation_only | short_alias_ambiguity | bare cron stays lens-first but remains ambiguous across M/R/SL |
| lux | Lens / M Lens / M / Summilux-M / Leica / Leica M 28mm f1.4 Summilux ASPH 6bit Black | Lens / M / Summilux-M / Leica / Leica M 50mm f1.4 Summilux Classic Silver | Lens / M / Summilux-M / Leica / Leica M 50mm f1.4 Summilux 4th Silver | observation_only | bare_alias_observation_only | short_alias_ambiguity | bare lux stays lens-first but remains ambiguous across focals |
| 50 cron | Lens / R Lens / R / Summicron-R / Leica / Leica R 50mm f2 Summicron Black | Lens / SL / APO-Summicron / Leica / Leica SL 50mm f2 APO-Summicron ASPH Black | Lens / M / Summicron-M / Leica / Leica M 50mm f2 Summicron Rigid Silver | weak_pass | focal_cron_ambiguous | short_alias_ambiguity | 50 cron stays lens-side but mount ambiguity remains M/R/SL |
| 35 lux | Lens / M Lens / M / Summilux-M / Leica / Leica M 35mm f1.4 Summilux 2nd Titan | Lens / M / Summilux-M / Leica / Leica M 35mm f1.4 Summilux 1st Silver [Steel Rim] | Lens / M / Summilux-M / Leica / Leica M 35mm f1.4 Summilux ASPH 4th Titan | pass | focal_lux_m_shorthand_allowed | no_change_needed | focal + lux behaves like useful M Summilux shorthand |
| 50 lux | Lens / M Lens / M / Summilux-M / Leica / Leica M 50mm f1.4 Summilux Classic Silver | Lens / M / Summilux-M / Leica / Leica M 50mm f1.4 Summilux 4th Silver | Lens / M / Summilux-M / Leica / Leica M 50mm f1.4 Summilux ASPH 6bit Silver | pass | focal_lux_m_shorthand_allowed | no_change_needed | focal + lux behaves like useful M Summilux shorthand |

| query | top1 | top2 | top3 | status | policy | cause | note |
|---|---|---|---|---|---|---|---|
| 28 cron | Lens / M Lens / M / Summicron-M / Leica / Leica M 28mm f2 Summicron ASPH 6bit Safari Edition | Lens / M / Summicron-M / Leica / Leica M 28mm f2 Summicron ASPH 6bit Black | Lens / M / Summicron-M / Leica / Leica M 28mm f2 Summicron ASPH 6bit Titan | weak_pass | focal_cron_ambiguous | short_alias_ambiguity | focal + cron remains ambiguous without explicit mount |
| 35 cron | Lens / M Lens / M / APO-Summicron / Leica / Leica M 35mm f2 APO-Summicron ASPH 6bit Black | Lens / M / Summicron-M / Leica / Leica M 35mm f2 Summicron ASPH Anthracite Finish | Lens / SL / Summicron-SL / Leica / 신품 Leica SL 35mm f2 Summicron ASPH Black | weak_pass | focal_cron_ambiguous | short_alias_ambiguity | focal + cron remains ambiguous without explicit mount |
| 90 cron | Lens / M Lens / M / APO-Summicron / Leica / Leica M 90mm f2 APO-Summicron ASPH Black | Lens / M / Summicron-M / Leica / LEICA 90mm F2 SUMMICRON-M sn.3703 | Lens / M / APO-Summicron / Leica / LEICA 90mm F2 ASPH (6bit) APO-SUMMICRON-M sn.4208 | weak_pass | focal_cron_ambiguous | short_alias_ambiguity | focal + cron remains ambiguous without explicit mount |
| 21 lux | Lens / M Lens / M / Summilux-M / Leica / Leica M 21mm f1.4 Summilux ASPH 6bit Black | Lens / M / Summilux-M / Leica / LEICA 21mm F1.4 ASPH SUMMILUX-M sn.4083 | Lens / M / Summilux-M / Leica / LEICA 21mm F1.4 ASPH SUMMILUX-M sn.4089 | weak_pass | focal_lux_m_shorthand_allowed | short_alias_ambiguity | focal + lux looks useful but remains collector shorthand |
| 24 lux | Lens / M Lens / M / Summilux-M / Leica / LEICA 24mm F1.4 ASPH SUMMILUX-M sn.4651 | Lens / M / Summilux-M / Leica / LEICA 24mm F1.4 ASPH SUMMILUX-M sn.4079 | Lens / M / Summilux-M / Leica / LEICA 24mm F1.4 ASPH SUMMILUX-M sn.4088 | weak_pass | focal_lux_m_shorthand_allowed | short_alias_ambiguity | focal + lux looks useful but remains collector shorthand |
| 28 lux | Lens / M Lens / M / Summilux-M / Leica / Leica M 28mm f1.4 Summilux ASPH 6bit Black | Lens / M / Summilux-M / Leica / 신품 Leica M 28mm f1.4 Summilux ASPH 6bit Black | Lens / M / Summilux-M / Leica / LEICA 28mm F1.4 ASPH SUMMILUX-M sn.4205 | weak_pass | focal_lux_m_shorthand_allowed | short_alias_ambiguity | focal + lux looks useful but remains collector shorthand |
| 75 lux | Lens / M Lens / M / Summilux-M / Leica / Leica M 75mm f1.4 Summilux [Made in Germany] | Lens / M / Summilux-M / Leica / Leica M 75mm f1.4 Summilux [Made in Germany] | Lens / M / Summilux-M / Leica / LEICA 75mm F1.4 SUMMILUX-M sn.3259 | weak_pass | focal_lux_m_shorthand_allowed | short_alias_ambiguity | focal + lux looks useful but remains collector shorthand |
| m 35 lux | Lens / M Lens / M / Summilux-M / Leica / Leica M 35mm f1.4 Summilux 2nd Titan | Lens / M / Summilux-M / Leica / Leica M 35mm f1.4 Summilux 1st Silver [Steel Rim] | Lens / M / Summilux-M / Leica / Leica M 35mm f1.4 Summilux ASPH 4th Titan | guardrail_pass | explicit_mount_wins | no_change_needed | explicit M token wins as intended |
| m 50 lux | Lens / M Lens / M / Summilux-M / Leica / Leica M 50mm f1.4 Summilux Classic Silver | Lens / M / Summilux-M / Leica / Leica M 50mm f1.4 Summilux 4th Silver | Lens / M / Summilux-M / Leica / Leica M 50mm f1.4 Summilux ASPH 6bit Silver | guardrail_pass | explicit_mount_wins | no_change_needed | explicit M token wins as intended |
| m 50 cron | Lens / M Lens / M / Summicron-M / Leica / Leica M 50mm f2 Summicron Rigid Silver | Lens / M / APO-Summicron / Leica / Leica M 50mm f2 APO-Summicron ASPH Black Chrome finish | Lens / M / Summicron-M / Leica / Leica M 50mm f 2 Summicron Rigid BlackRepaint | guardrail_pass | explicit_mount_wins | no_change_needed | explicit M token wins as intended |
| r 50 cron | Lens / R Lens / R / Summicron-R / Leica / Leica R 50mm f2 Summicron Black | Lens / R / Summicron-R / Leica / LEICA 50mm F2 SUMMICRON-R sn.3338 | Lens / R / Summicron-R / Leica / LEICA 50mm F2 ROM SUMMICRON-R sn.3819 | guardrail_pass | explicit_mount_wins | no_change_needed | explicit R token wins as intended |
| sl 50 cron | Lens / SL Lens / SL / APO-Summicron / Leica / Leica SL 50mm f2 APO-Summicron ASPH Black | Lens / SL / Summicron-SL / Leica / [위탁] Leica SL2-S Kit with Summicron-SL 50mm f/2 ASPH | Lens / SL / Summicron-SL / Leica / [중고] Leica Summicron-SL 50mm f/2 ASPH | guardrail_pass | explicit_mount_wins | no_change_needed | explicit SL token wins as intended |
| leica 35 lux | Lens / M Lens / M / Summilux-M / Leica / Leica M 35mm f1.4 Summilux 2nd Titan | Lens / M / Summilux-M / Leica / Leica M 35mm f1.4 Summilux 1st Silver [Steel Rim] | Lens / M / Summilux-M / Leica / Leica M 35mm f1.4 Summilux ASPH 4th Titan | weak_pass | focal_lux_m_shorthand_allowed | short_alias_ambiguity | focal + lux looks useful but remains collector shorthand |
| leica 50 lux | Lens / M Lens / M / Summilux-M / Leica / Leica M 50mm f1.4 Summilux Classic Silver | Lens / M / Summilux-M / Leica / Leica M 50mm f1.4 Summilux 4th Silver | Lens / M / Summilux-M / Leica / Leica M 50mm f1.4 Summilux ASPH 6bit Silver | weak_pass | focal_lux_m_shorthand_allowed | short_alias_ambiguity | focal + lux looks useful but remains collector shorthand |
| leica 50 cron | Lens / R Lens / R / Summicron-R / Leica / Leica R 50mm f2 Summicron Black | Lens / SL / APO-Summicron / Leica / Leica SL 50mm f2 APO-Summicron ASPH Black | Lens / M / Summicron-M / Leica / Leica M 50mm f2 Summicron Rigid Silver | weak_pass | focal_cron_ambiguous | short_alias_ambiguity | focal + cron remains ambiguous without explicit mount |

## 7. search index / normalized / raw 후보 존재 여부
- `cron`, `50 cron`, `35 cron`, `90 cron` -> Summicron 계열 candidate 존재
- `lux`, `35 lux`, `50 lux`, `21/24/28/75 lux` -> Summilux 계열 candidate 존재
- `sigma 14-24 l`만 known source coverage gap으로 no-result 유지

## 8. 원인 분류
- bare alias: `short_alias_ambiguity`
- focal + cron: `short_alias_ambiguity`
- focal + lux: 대부분 `no_change_needed`, 일부 collector shorthand ambiguity 잔존
- explicit mount + alias: `no_change_needed`
- `sigma 14-24 l`: `source_coverage_gap`

## 9. 수정 파일 목록
- `scripts/run_p3_cron_lux_short_alias_policy.py`

## 10. 수정하지 않은 파일/영역
- `classifier_v2.py`
- `model_detector.py`
- `query_parser.py`
- `query_resolver.py`
- `search_service.py`
- taxonomy seed / canonical index
- output JSON / normalized / sold_items / results.json

## 11. broad family alias guardrail 결과
| query | top1 | top2 | top3 | status | policy | cause | note |
|---|---|---|---|---|---|---|---|
| summicron | Lens / L Lens / L / Summicron / Leica / Leica L 50mm f2 Summicron Silver | Lens / L / Summicron / Leica / Leica L 50mm f2 Summicron Rigid Silver | Lens / L / Summicron / Leica / Leica L 50mm f2 Summicron Silver | guardrail_pass | lens_first_only | no_change_needed |  |
| summilux | Lens / L Lens / L / Summilux / Leica / [중고] L 50/1.4 Summilux 4세대 (Silver) | Lens / L / Summilux / Leica / LEICA 50mm F1.4 SUMMILUX M39 sn.3868 | Lens / L / Summilux / Leica / LEICA 50mm F1.4 Screwmount M39 SUMMILUX-L sn.3868 | guardrail_pass | lens_first_only | no_change_needed |  |
| leica summicron | Lens / L Lens / L / Summicron / Leica / Leica L 50mm f2 Summicron Silver | Lens / L / Summicron / Leica / Leica L 50mm f2 Summicron Rigid Silver | Lens / L / Summicron / Leica / Leica L 50mm f2 Summicron Silver | guardrail_pass | lens_first_only | no_change_needed |  |
| leica summilux | Lens / L Lens / L / Summilux / Leica / [중고] L 50/1.4 Summilux 4세대 (Silver) | Lens / L / Summilux / Leica / LEICA 50mm F1.4 SUMMILUX M39 sn.3868 | Lens / L / Summilux / Leica / LEICA 50mm F1.4 Screwmount M39 SUMMILUX-L sn.3868 | guardrail_pass | lens_first_only | no_change_needed |  |

## 12. explicit M Lens guardrail 결과
| query | top1 | top2 | top3 | status | policy | cause | note |
|---|---|---|---|---|---|---|---|
| summicron m 50 | Lens / M Lens / M / Summicron-M / Leica / Leica M 50mm f2 Summicron Rigid Silver | Lens / M / APO-Summicron / Leica / Leica M 50mm f2 APO-Summicron ASPH Black Chrome finish | Lens / M / Summicron-M / Leica / Leica M 50mm f 2 Summicron Rigid BlackRepaint | guardrail_pass | lens_first_only | no_change_needed |  |
| m 50 summicron | Lens / M Lens / M / Summicron-M / Leica / Leica M 50mm f2 Summicron Rigid Silver | Lens / M / APO-Summicron / Leica / Leica M 50mm f2 APO-Summicron ASPH Black Chrome finish | Lens / M / Summicron-M / Leica / Leica M 50mm f 2 Summicron Rigid BlackRepaint | guardrail_pass | lens_first_only | no_change_needed |  |
| leica m 50 summicron | Lens / M Lens / M / Summicron-M / Leica / Leica M 50mm f2 Summicron Rigid Silver | Lens / M / APO-Summicron / Leica / Leica M 50mm f2 APO-Summicron ASPH Black Chrome finish | Lens / M / Summicron-M / Leica / Leica M 50mm f 2 Summicron Rigid BlackRepaint | guardrail_pass | lens_first_only | no_change_needed |  |
| summilux m 35 | Lens / M Lens / M / Summilux-M / Leica / Leica M 35mm f1.4 Summilux 2nd Titan | Lens / M / Summilux-M / Leica / Leica M 35mm f1.4 Summilux 1st Silver [Steel Rim] | Lens / M / Summilux-M / Leica / Leica M 35mm f1.4 Summilux ASPH 4th Titan | guardrail_pass | lens_first_only | no_change_needed |  |
| m 35 summilux | Lens / M Lens / M / Summilux-M / Leica / Leica M 35mm f1.4 Summilux 2nd Titan | Lens / M / Summilux-M / Leica / Leica M 35mm f1.4 Summilux 1st Silver [Steel Rim] | Lens / M / Summilux-M / Leica / Leica M 35mm f1.4 Summilux ASPH 4th Titan | guardrail_pass | lens_first_only | no_change_needed |  |
| leica m 35 summilux | Lens / M Lens / M / Summilux-M / Leica / Leica M 35mm f1.4 Summilux 2nd Titan | Lens / M / Summilux-M / Leica / Leica M 35mm f1.4 Summilux 1st Silver [Steel Rim] | Lens / M / Summilux-M / Leica / Leica M 35mm f1.4 Summilux ASPH 4th Titan | guardrail_pass | lens_first_only | no_change_needed |  |
| summilux m 50 | Lens / M Lens / M / Summilux-M / Leica / Leica M 50mm f1.4 Summilux Classic Silver | Lens / M / Summilux-M / Leica / Leica M 50mm f1.4 Summilux 4th Silver | Lens / M / Summilux-M / Leica / Leica M 50mm f1.4 Summilux ASPH 6bit Silver | guardrail_pass | lens_first_only | no_change_needed |  |
| m 50 summilux | Lens / M Lens / M / Summilux-M / Leica / Leica M 50mm f1.4 Summilux Classic Silver | Lens / M / Summilux-M / Leica / Leica M 50mm f1.4 Summilux 4th Silver | Lens / M / Summilux-M / Leica / Leica M 50mm f1.4 Summilux ASPH 6bit Silver | guardrail_pass | lens_first_only | no_change_needed |  |
| leica m 50 summilux | Lens / M Lens / M / Summilux-M / Leica / Leica M 50mm f1.4 Summilux Classic Silver | Lens / M / Summilux-M / Leica / Leica M 50mm f1.4 Summilux 4th Silver | Lens / M / Summilux-M / Leica / Leica M 50mm f1.4 Summilux ASPH 6bit Silver | guardrail_pass | lens_first_only | no_change_needed |  |
| elmarit m 28 | Lens / M Lens / M / Elmarit-M / Leica / Leica M 28mm f2.8 Elmarit ASPH 5th 6bit Black | Lens / M / Elmarit-M / Leica / Leica M 28mm f2.8 Elmarit 3rd Black | Lens / M / Elmarit-M / Leica / Leica M 28mm f2.8 Elmarit 2nd Black | guardrail_pass | lens_first_only | no_change_needed |  |
| m 28 elmarit | Lens / M Lens / M / Elmarit-M / Leica / Leica M 28mm f2.8 Elmarit ASPH 5th 6bit Black | Lens / M / Elmarit-M / Leica / Leica M 28mm f2.8 Elmarit 3rd Black | Lens / M / Elmarit-M / Leica / Leica M 28mm f2.8 Elmarit 2nd Black | guardrail_pass | lens_first_only | no_change_needed |  |
| apo telyt m 135 | Lens / M Lens / M / Tele-Elmar / Leica / Leica M 135mm f4 Tele-Elmar Black | Lens / M / Hektor / Leica / Leica M 135mm f4.5 Hektor Silver | Lens / M / Tele-Elmar / Leica / Leica M 135mm f4 Tele-Elmar Black | guardrail_pass | lens_first_only | no_change_needed |  |
| m 135 apo telyt | Lens / M Lens / M / Tele-Elmar / Leica / Leica M 135mm f4 Tele-Elmar Black | Lens / M / Hektor / Leica / Leica M 135mm f4.5 Hektor Silver | Lens / M / Tele-Elmar / Leica / Leica M 135mm f4 Tele-Elmar Black | guardrail_pass | lens_first_only | no_change_needed |  |

## 13. explicit R Lens guardrail 결과
| query | top1 | top2 | top3 | status | policy | cause | note |
|---|---|---|---|---|---|---|---|
| r 50 summicron | Lens / R Lens / R / Summicron-R / Leica / Leica R 50mm f2 Summicron Black | Lens / R / Summicron-R / Leica / LEICA 50mm F2 SUMMICRON-R sn.3338 | Lens / R / Summicron-R / Leica / LEICA 50mm F2 ROM SUMMICRON-R sn.3819 | guardrail_pass | lens_first_only | no_change_needed |  |
| summicron-r 50 | Lens / R Lens / R / Summicron-R / Leica / Leica R 50mm f2 Summicron Black | Lens / R / Summicron-R / Leica / LEICA 50mm F2 SUMMICRON-R sn.3338 | Lens / R / Summicron-R / Leica / LEICA 50mm F2 ROM SUMMICRON-R sn.3819 | guardrail_pass | lens_first_only | no_change_needed |  |
| r 180 apo | Lens / R Lens / R / APO-Telyt-R / Leica / Leica R 180mm f3.4 APO-Telyt Black | Lens / R / APO-Telyt-R / Leica / Leica R 180mm f3.4 APO-Telyt Black | Lens / R / APO-Telyt-R / Leica / LEICA 180mm F3.4 APO-TELYT-R sn.3478 | guardrail_pass | lens_first_only | no_change_needed |  |
| apo-telyt-r 180 | Lens / R Lens / R / APO-Telyt-R / Leica / Leica R 180mm f3.4 APO-Telyt Black | Lens / R / APO-Telyt-R / Leica / Leica R 180mm f3.4 APO-Telyt Black | Lens / R / APO-Telyt-R / Leica / LEICA 180mm F3.4 APO-TELYT-R sn.3478 | guardrail_pass | lens_first_only | no_change_needed |  |
| elmarit r 135 | Lens / R Lens / R / Elmarit-R / Leica / LEICA 135mm F2.8 ELMARIT-R sn.2155 | Lens / R / Elmarit-R / Leica / LEICA 135mm F2.8 ELMARIT-R sn.2772 | Lens / R / Elmarit-R / Leica / LEICA 135mm F2.8 ELMARIT-R sn.2809 | guardrail_pass | lens_first_only | no_change_needed |  |
| r 135 elmarit | Lens / R Lens / R / Elmarit-R / Leica / LEICA 135mm F2.8 ELMARIT-R sn.2155 | Lens / R / Elmarit-R / Leica / LEICA 135mm F2.8 ELMARIT-R sn.2772 | Lens / R / Elmarit-R / Leica / LEICA 135mm F2.8 ELMARIT-R sn.2809 | guardrail_pass | lens_first_only | no_change_needed |  |
| vario elmarit r 28-90 | Lens / R Lens / R / Vario-Elmarit-R / Leica / LEICA 28-90mm F2.8-4.5 VARIO-ELMARIT-R sn.3975 | Lens / R / Vario-Elmarit-R / Leica / LEICA 28-90mm F2.8-4.5 ASPH VARIO-ELMARIT-R sn.3974 | Lens / R / Vario-Elmarit-R / Leica / LEICA 28-90mm F2.8-4.5 VARIO-ELMARIT-R sn.3973 | guardrail_pass | lens_first_only | no_change_needed |  |
| r 28-90 vario elmarit | Lens / R Lens / R / Vario-Elmarit-R / Leica / LEICA 28-90mm F2.8-4.5 VARIO-ELMARIT-R sn.3975 | Lens / R / Vario-Elmarit-R / Leica / LEICA 28-90mm F2.8-4.5 ASPH VARIO-ELMARIT-R sn.3974 | Lens / R / Vario-Elmarit-R / Leica / LEICA 28-90mm F2.8-4.5 VARIO-ELMARIT-R sn.3973 | guardrail_pass | lens_first_only | no_change_needed |  |
| summilux-r 80 | Lens / R Lens / R / Summilux-R / Leica / LEICA 80mm F1.4 SUMMILUX-R sn.3133 | Lens / R / Summilux-R / Leica / LEICA 80mm F1.4 SUMMILUX-R sn.3599 | Lens / R / Summilux-R / Leica / LEICA 80mm F1.4 SUMMILUX-R sn.3599 | guardrail_pass | lens_first_only | no_change_needed |  |
| r 80 summilux | Lens / R Lens / R / Summilux-R / Leica / LEICA 80mm F1.4 SUMMILUX-R sn.3133 | Lens / R / Summilux-R / Leica / LEICA 80mm F1.4 SUMMILUX-R sn.3599 | Lens / R / Summilux-R / Leica / LEICA 80mm F1.4 SUMMILUX-R sn.3599 | guardrail_pass | lens_first_only | no_change_needed |  |

## 14. explicit SL Lens guardrail 결과
| query | top1 | top2 | top3 | status | policy | cause | note |
|---|---|---|---|---|---|---|---|
| summicron sl 35 | Lens / SL Lens / SL / Summicron-SL / Leica / 신품 Leica SL 35mm f2 Summicron ASPH Black | Lens / SL / Summicron-SL / Leica / [중고] Leica SL2 with Summicron-SL 35mm f/2 ASPH | Lens / SL / APO-Summicron / Leica / LEICA 35mm F2 ASPH APO-SUMMICRON-SL sn.4720 | guardrail_pass | lens_first_only | no_change_needed |  |
| Leica 35mm F2 AsphSummicron SL | Lens / SL Lens / SL / Summicron-SL / Leica / 신품 Leica SL 35mm f2 Summicron ASPH Black | Lens / SL / Summicron-SL / Leica / [중고] Leica SL2 with Summicron-SL 35mm f/2 ASPH | Lens / SL / APO-Summicron / Leica / LEICA 35mm F2 ASPH APO-SUMMICRON-SL sn.4720 | guardrail_pass | lens_first_only | no_change_needed |  |
| apo summicron sl 35 | Lens / SL Lens / SL / Summicron-SL / Leica / 신품 Leica SL 35mm f2 Summicron ASPH Black | Lens / SL / Summicron-SL / Leica / [중고] Leica SL2 with Summicron-SL 35mm f/2 ASPH | Lens / SL / APO-Summicron / Leica / LEICA 35mm F2 ASPH APO-SUMMICRON-SL sn.4720 | weak_pass | lens_first_only | short_alias_ambiguity | APO family ranking still weak but stayed SL lens-side |
| sl 35 summicron | Lens / SL Lens / SL / Summicron-SL / Leica / 신품 Leica SL 35mm f2 Summicron ASPH Black | Lens / SL / Summicron-SL / Leica / [중고] Leica SL2 with Summicron-SL 35mm f/2 ASPH | Lens / SL / APO-Summicron / Leica / LEICA 35mm F2 ASPH APO-SUMMICRON-SL sn.4720 | guardrail_pass | lens_first_only | no_change_needed |  |
| sl 50 summicron | Lens / SL Lens / SL / APO-Summicron / Leica / Leica SL 50mm f2 APO-Summicron ASPH Black | Lens / SL / Summicron-SL / Leica / [위탁] Leica SL2-S Kit with Summicron-SL 50mm f/2 ASPH | Lens / SL / Summicron-SL / Leica / [중고] Leica Summicron-SL 50mm f/2 ASPH | guardrail_pass | lens_first_only | no_change_needed |  |
| sl 75 summicron | Lens / SL Lens / SL / APO-Summicron / Leica / LEICA 75mm F2 ASPH APO-SUMMICRON-SL sn.4709 | Lens / SL / APO-Summicron / Leica / LEICA 75mm F2 APO-SUMMICRON-SL sn.4699 | Lens / SL / APO-Summicron / Leica / Leica SL 50mm f2 APO-Summicron ASPH Black | guardrail_pass | lens_first_only | no_change_needed |  |
| sl 90 summicron | Lens / SL Lens / SL / APO-Summicron / Leica / LEICA 90mm F2 ASPH APO-summicron-SL sn.4713 | Lens / SL / APO-Summicron / Leica / [중고] SL 90/2 APO-Summicron | Lens / SL / APO-Summicron / Leica / [중고] SL 90/2 APO Summicron ASPH (Black) | guardrail_pass | lens_first_only | no_change_needed |  |
| sl 24-90 | Lens / SL Lens / SL / Vario-Elmarit-SL / Leica / Leica SL 24-90mm f2.8-4 Vario-Elmarit Black | Lens / SL / Vario-Elmarit-SL / Leica / Leica SL 24-90mm f2.8-4 Vario-Elmarit Black | Lens / SL / Vario-Elmarit-SL / Leica / [위탁] SL 24-90/2.8-4 Vario Elmar ASPH (Black) | guardrail_pass | lens_first_only | no_change_needed |  |
| sl 14-24 | Lens / SL Lens / SL / Super-Vario-Elmarit-SL / Leica / [중고] SL 14-24/2.8 Vario Elmarit ASPH (Black) | Lens / SL / Super-Vario-Elmarit-SL / Leica / [중고] SL 14-24/2.8 Vario Elmarit ASPH (Black) | Lens / SL / Super-Vario-Elmarit-SL / Leica / [중고] SL 14-24/2.8 Vario Elmarit ASPH (Black) | guardrail_pass | lens_first_only | no_change_needed |  |
| sl 16-35 | Lens / SL Lens / SL / Super-Vario-Elmar-SL / Leica / [중고] SL 16-35/3.5-4.5 Super Vario Elmar ASPH (Black) | Lens / SL / Super-Vario-Elmar-SL / Leica / [중고] SL 16-35/3.5-4.5 Super Vario Elmar ASPH (Black) | Lens / SL / Super-Vario-Elmar-SL / Leica / LEICA SL2 16-35mm F3.5-4.5 ASPH sn.4687/5576 | guardrail_pass | lens_first_only | no_change_needed |  |
| sl 90-280 | Lens / SL Lens / SL / APO-Vario-Elmarit-SL / Leica / [중고] SL APO Vario Elmarit 90-280 f/2.8-4 | Lens / SL / APO-Vario-Elmarit-SL / Leica / [중고] SL APO Vario Elmarit 90-280 f/2.8-4 | Lens / SL / APO-Vario-Elmarit-SL / Leica / [중고] SL 90-280/2.8-4 APO Vario Elmarit ASPH (Black) | guardrail_pass | lens_first_only | no_change_needed |  |

## 15. accessory guardrail 결과
| query | top1 | top2 | top3 | status | policy | cause | note |
|---|---|---|---|---|---|---|---|
| sl3 battery | Accessory / Accessory / SL / Q3 / Unknown / [중고] Q3,SL3 배터리 (BP-SCL6) | Accessory / SL / Q3 / Unknown / [위탁] Q3,SL3 배터리 (BP-SCL6) | Accessory / SL / Q3 / Unknown / [중고] Q3,SL3 배터리 (BP-SCL6) | guardrail_pass | no_hard_pin | no_change_needed |  |
| leica m strap | Accessory / Accessory / M / M11 / Leica / [중고] Leica M11 strap (Cognac) | Accessory / M / M11 / Leica / [중고] Leica M11 Neck strap (Cognac) | Accessory / M /  / Leica / Leica M-L adapter Black | guardrail_pass | no_hard_pin | no_change_needed |  |
| leica hood 12585 | Accessory / Accessory / M /  / Leica / Leica 12585 Hood for M-50mm, 35mm | Accessory / Unknown /  / Leica / [중고] Leica 12585 후드 | Accessory / Unknown /  / Leica / [중고] Leica 12585 후드 | guardrail_pass | no_hard_pin | no_change_needed |  |
| hood 12549 | Accessory / Accessory / M / Elmar / Leica / Leica 12549 Hood Silver [for M 50mm f2.8 Elmar] | Accessory / Unknown / Elmar / Leica / Leica 12549 Lens Hood Silver （Elmar） | Lens / Unknown /  / Leica / LEICA 12549 | guardrail_pass | no_hard_pin | no_change_needed |  |
| m adapter l | Accessory / Accessory / M /  / Leica / Leica M-L adapter Black | Accessory / M /  / Leica / Leica M-L adapter Black | Accessory / M /  / Leica / Leica M-L adapter Silver | guardrail_pass | no_hard_pin | no_change_needed |  |
| r adapter | Accessory / Accessory / R / R6 / Leica / [중고] Leica R6 가죽 케이스 | Accessory / R / R6 / Leica / [중고] Leica R6 가죽 케이스 | Accessory / R / APO-Telyt / Leica / LEICA 280mm F4 APO-TELYT-R APO-EXTENDER-R sn.3622 | guardrail_pass | no_hard_pin | no_change_needed |  |
| leica r adapter | Accessory / Accessory / R / R6 / Leica / [중고] Leica R6 가죽 케이스 | Accessory / R / R6 / Leica / [중고] Leica R6 가죽 케이스 | Accessory / R / APO-Telyt / Leica / LEICA 280mm F4 APO-TELYT-R APO-EXTENDER-R sn.3622 | guardrail_pass | no_hard_pin | no_change_needed |  |
| leica r cap | Accessory / Accessory / R / R6 / Leica / [중고] Leica R6 가죽 케이스 | Accessory / R / R6 / Leica / [중고] Leica R6 가죽 케이스 | Accessory / R / APO-Telyt / Leica / LEICA 280mm F4 APO-TELYT-R APO-EXTENDER-R sn.3622 | guardrail_pass | no_hard_pin | no_change_needed |  |
| r lens cap | Accessory / Accessory / R / R6 / Leica / [중고] Leica R6 가죽 케이스 | Accessory / R / R6 / Leica / [중고] Leica R6 가죽 케이스 | Accessory / R / APO-Telyt / Leica / LEICA 280mm F4 APO-TELYT-R APO-EXTENDER-R sn.3622 | guardrail_pass | no_hard_pin | no_change_needed |  |
| r hood | Accessory / Accessory / R / R6 / Leica / [중고] Leica R6 가죽 케이스 | Accessory / R / R6 / Leica / [중고] Leica R6 가죽 케이스 | Accessory / R / APO-Telyt / Leica / LEICA 280mm F4 APO-TELYT-R APO-EXTENDER-R sn.3622 | guardrail_pass | no_hard_pin | no_change_needed |  |
| leica handgrip | Accessory / Accessory / SL / CL / Leica / Leica CL handgrip Black | Accessory / M / M10 / Leica / Leica M10 Handgrip Black | Accessory / M / M10 / Leica / Leica M10 Handgrip Black | guardrail_pass | no_hard_pin | no_change_needed |  |
| leica charger | Accessory / Accessory / Q / Q3 / Leica / [중고] Leica Q3 Drop XL Wireless Charger | Accessory / S /  / Leica / [위탁]Leica S Professional Charger | Accessory / Q / Q3 / Leica / [중고] Leica Q3 Drop XL Wireless Charger | guardrail_pass | no_hard_pin | no_change_needed |  |
| leica case | Accessory / Accessory / Q / Q2 / Leica / Leica Q2 Case Red | Accessory / Unknown /  / Leica / Leica Visoflex 2 Leather Case Black | Accessory / M / MP / Leica / [중고] Leica MP 가죽 케이스 | guardrail_pass | no_hard_pin | no_change_needed |  |
| leica pouch | Accessory / Accessory / M / M10 / Leica / Leica M10 Leather Pouch Black Small front | Accessory / Q / Q2 / Leica / [중고] Leica Q2 Ettas Pouch (Midnight Blue) | Accessory / Unknown /  / Unknown / [중고] 키모토 파우치 | guardrail_pass | no_hard_pin | no_change_needed |  |
| leica filter | Accessory / Accessory / Unknown /  / Leica / Leica E82 UVa II Black | Accessory / Unknown /  / Leica / 신품 Leica E46 UVa II Black | Accessory / M /  / Leica / Leica Serie8 UV Filter (M 50/1.2(B) | guardrail_pass | no_hard_pin | no_change_needed |  |

## 16. body guardrail 결과
| query | top1 | top2 | top3 | status | policy | cause | note |
|---|---|---|---|---|---|---|---|
| leica sl2 | Body / SL Body / SL / SL2 / Leica / Leica SL2 Black | Body / SL / SL2 / Leica / Leica SL2 Black | Body / SL / SL2 / Leica / Leica SL2-S Reporter | guardrail_pass | no_hard_pin | no_change_needed |  |
| leica sl3 | Body / SL Body / SL / SL3 / Leica / Leica SL3 Black | Body / SL / SL3 / Leica / Leica SL3 Reporter | Body / SL / SL3 / Leica / Leica SL3 Body Only | guardrail_pass | no_hard_pin | no_change_needed |  |
| leica m10 body | Body / M Body / M / M10 / Leica / [위탁] M10 Monochrom 'Leitz Wetzlar' Edition | Body / M / M10 / Leica / [중고] Leica M10 홀스터 | Body / M / M10 / Leica / [중고] Leica M10 하프케이스 (Brown) | guardrail_pass | no_hard_pin | no_change_needed |  |
| leica iiif | Body / L Body / L / IIIf / Leica / Leica Barnack IIIF Silver | Body / L / IIIf / Leica / Leica Barnack IIIf Silver | Body / L / IIIf / Leica / Leica Barnack IIIF Silver | guardrail_pass | no_hard_pin | no_change_needed |  |
| barnack iiif | Body / L Body / L / IIIf / Leica / Leica Barnack IIIF Silver | Body / L / IIIf / Leica / Leica Barnack IIIf Silver | Body / L / IIIf / Leica / Leica Barnack IIIF Silver | guardrail_pass | no_hard_pin | no_change_needed |  |
| leica q2 | Body / Leica Body / Q / Q2 / Leica / Leica Q2 007 Edition | Body / Q / Q2 / Leica / Leica Q2 Black | Body / Q / Q2 / Leica / [중고] Leica Q2 Monochrome | guardrail_pass | no_hard_pin | no_change_needed |  |

## 17. third-party L-mount guardrail 결과
| query | top1 | top2 | top3 | status | policy | cause | note |
|---|---|---|---|---|---|---|---|
| sigma 24-70 l | Lens / SL Lens / SL /  / 3rd Party / [중고] Sigma 24-70/2.8 (SL 마운트) | Lens / SL /  / 3rd Party / [위탁] 시그마 24-70/2.8 (SL 마운트) | Lens / SL /  / 3rd Party / [중고] Sigma 24-70/2.8 (SL 마운트) | guardrail_pass | no_hard_pin | no_change_needed |  |
| sigma 24-70 dg dn | Lens / SL Lens / SL /  / 3rd Party / [중고] Sigma 24-70/2.8 (SL 마운트) | Lens / SL /  / 3rd Party / [위탁] 시그마 24-70/2.8 (SL 마운트) | Lens / SL /  / 3rd Party / [중고] Sigma 24-70/2.8 (SL 마운트) | guardrail_pass | no_hard_pin | no_change_needed |  |
| panasonic 24-105 l | Lens / SL Lens / SL /  / 3rd Party / [중고] 파나소닉 24-105 L 마운트 | - | - | guardrail_pass | no_hard_pin | no_change_needed |  |
| lumix 24-105 | Lens / SL Lens / SL /  / 3rd Party / [중고] 파나소닉 24-105 L 마운트 | - | - | guardrail_pass | no_hard_pin | no_change_needed |  |
| sigma l 30mm | Lens / SL Lens / SL /  / 3rd Party / Sigma L 30mm f1.4 DC DN Black for CL, TL2, etc | Lens / S / Elmarit / Leica / Leica S 30mm f2.8 Elmarit ASPH CS Black | Lens / S / Elmarit / Leica / [위탁] Elmarit-S 30mm f/2.8 ASPH CS | guardrail_pass | no_hard_pin | no_change_needed |  |
| sigma 30mm l | Lens / SL Lens / SL /  / 3rd Party / Sigma L 30mm f1.4 DC DN Black for CL, TL2, etc | Lens / S / Elmarit / Leica / Leica S 30mm f2.8 Elmarit ASPH CS Black | Lens / S / Elmarit / Leica / [위탁] Elmarit-S 30mm f/2.8 ASPH CS | guardrail_pass | no_hard_pin | no_change_needed |  |
| sigma 14-24 l |  /  /  /  /  /  | - | - | no_result_confirmed | no_hard_pin | source_coverage_gap | known third-party source coverage gap |

## 18. status 요약
- 총 query 수: `86`
- `guardrail_pass`: `69`
- `no_result_confirmed`: `1`
- `observation_only`: `2`
- `pass`: `2`
- `weak_pass`: `12`

## 19. 남은 위험
- `50 cron`: `weak_pass` / `Lens:Summicron-R:Leica` - 50 cron stays lens-side but mount ambiguity remains M/R/SL
- `28 cron`: `weak_pass` / `Lens:Summicron-M:Leica` - focal + cron remains ambiguous without explicit mount
- `35 cron`: `weak_pass` / `Lens:APO-Summicron:Leica` - focal + cron remains ambiguous without explicit mount
- `90 cron`: `weak_pass` / `Lens:APO-Summicron:Leica` - focal + cron remains ambiguous without explicit mount
- `21 lux`: `weak_pass` / `Lens:Summilux-M:Leica` - focal + lux looks useful but remains collector shorthand
- `24 lux`: `weak_pass` / `Lens:Summilux-M:Leica` - focal + lux looks useful but remains collector shorthand
- `28 lux`: `weak_pass` / `Lens:Summilux-M:Leica` - focal + lux looks useful but remains collector shorthand
- `75 lux`: `weak_pass` / `Lens:Summilux-M:Leica` - focal + lux looks useful but remains collector shorthand
- `leica 35 lux`: `weak_pass` / `Lens:Summilux-M:Leica` - focal + lux looks useful but remains collector shorthand
- `leica 50 lux`: `weak_pass` / `Lens:Summilux-M:Leica` - focal + lux looks useful but remains collector shorthand
- `leica 50 cron`: `weak_pass` / `Lens:Summicron-R:Leica` - focal + cron remains ambiguous without explicit mount
- `apo summicron sl 35`: `weak_pass` / `Lens:Summicron-SL:Leica` - APO family ranking still weak but stayed SL lens-side

## 20. observation-only query
- `cron`: `observation_only` / `Lens:Summicron-R:Leica` - bare cron stays lens-first but remains ambiguous across M/R/SL
- `lux`: `observation_only` / `Lens:Summilux-M:Leica` - bare lux stays lens-first but remains ambiguous across focals

## 21. no-result / source coverage 후보
- `sigma 14-24 l`: `no_result_confirmed` / `::` - known third-party source coverage gap

## 22. 결론
- `cron`, `lux`는 current behavior 기준으로 Lens-first는 확보돼 있어도 collector shorthand ambiguity가 커서 `observation_only` 유지가 가장 안전하다.
- `35 lux`, `50 lux`는 current ranking상 M Summilux shorthand로 충분히 usable하다.
- `50 cron`은 Lens-side는 괜찮지만 M/R/SL ambiguity가 크므로 hard-pin 없이 `weak_pass` 정책이 적절하다.
- explicit mount가 들어간 short alias는 이미 잘 동작하고 있어 이번 라운드에서 production 수정은 필요하지 않았다.
