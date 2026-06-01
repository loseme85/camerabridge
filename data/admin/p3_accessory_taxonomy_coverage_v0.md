# P3-ACCESSORY-TAXONOMY-COVERAGE

## 1. 작업 목적
- accessory taxonomy / alias coverage 약점 점검
- 후보가 있는 경우에만 search-layer에서 좁게 복구
- lens/body/third-party guardrail 유지 확인

## 2. 수정 전 문제 요약
- `leica handgrip`는 before 기준 Lens top1이었다.
- `leica charger`, `leica grip`, `leica case`, `leica pouch`도 before 기준 Lens top1이었다.
- `bp-scl6 / bp-scl5 / cap / finder / filter`는 Accessory 결과가 나오지만 taxonomy / subtype precision이 느슨했다.

## 3. 실행 entrypoint
- `api.search.endpoint_response`
- `search_service.load_and_search`
- `data/derived/results_search_index_v1.json`

## 4. target / observation query before 결과
| query | before top1 | after top1 | top2 | top3 | status | cause | note |
|---|---|---|---|---|---|---|---|
| bp-scl6 | Accessory / Accessory / Q / Q3 / Leica / Leica Q3, SL3 Battery [BP-SCL6] | Accessory / Accessory / Q / Q3 / Leica / Leica Q3, SL3 Battery [BP-SCL6] | [중고] Q3,SL3 배터리 (BP-SCL6) | [위탁] Q3,SL3 배터리 (BP-SCL6) | pass | none |  |
| bp-scl5 | Accessory / Accessory / Unknown / CL / Unknown / [위탁] BP-SCL5 | Accessory / Accessory / Unknown / CL / Unknown / [위탁] BP-SCL5 | LEICA BP-SCL5 for M10/M10-p | LEICA BP-SCL5 for M10 | pass | none |  |
| leica cap | Accessory / Accessory / Unknown /  / Leica / [중고] Leitz Lens Cap E52.5 | Accessory / Accessory / Unknown /  / Leica / [중고] Leitz Lens Cap E52.5 | [중고] Leica Lens Cap E60 | [중고] Leica Lens Cap E55 | pass | none |  |
| m cap | Accessory / Accessory / M / M3 / Leica / [중고] Leica Body Cap for M3 | Accessory / Accessory / M / M3 / Leica / [중고] Leica Body Cap for M3 | Artisan & Artist M8, M9 Case Black | Leica M-L adapter Black | pass | none |  |
| r cap | Accessory / Accessory / R / R6 / Leica / [중고] Leica R6 가죽 케이스 | Accessory / Accessory / R / R6 / Leica / [중고] Leica R6 가죽 케이스 | [중고] Leica R6 가죽 케이스 | LEICA 280mm F4 APO-TELYT-R APO-EXTENDER-R sn.3622 | weak_pass | accessory_taxonomy_gap | cap query stayed accessory but mount-specific cap precision is weak |
| sl cap | Accessory / Accessory / SL /  / Unknown / LM to L 헬리코이드 어댑터 (L 마운트용) | Accessory / Accessory / SL /  / Unknown / LM to L 헬리코이드 어댑터 (L 마운트용) | Jnk SL2 Case [Black / Battery Door Type] | Jnk SL2 Case [Black / Battery Door Type] | weak_pass | accessory_taxonomy_gap | cap query stayed accessory but mount-specific cap precision is weak |
| leica finder | Accessory / Accessory / Unknown /  / Leica / Leica 85mm Tele Finder C. K. S. Silver | Accessory / Accessory / Unknown /  / Leica / Leica 85mm Tele Finder C. K. S. Silver | Leica R Angle Finder Black | Leica 35-135mm VIOOH Finder Black | pass | none |  |
| leica handgrip | Lens / M Lens / M / Elmar / Leica / Leica M 50mm f2.8 Elmar Black | Accessory / Accessory / SL / CL / Leica / Leica CL handgrip Black | Leica M10 Handgrip Black | Leica M10 Handgrip Black | pass | none |  |
| leica filter | Accessory / Accessory / Unknown /  / Leica / Leica E82 UVa II Black | Accessory / Accessory / Unknown /  / Leica / Leica E82 UVa II Black | 신품 Leica E46 UVa II Black | Leica Serie8 UV Filter (M 50/1.2(B) | pass | none |  |

| query | before top1 | after top1 | top2 | top3 | status | cause | note |
|---|---|---|---|---|---|---|---|
| leica battery | Accessory / Accessory / M / M11 / Leica / Leica M11 Battery Silver [BP-SCL7] | Accessory / Accessory / M / M11 / Leica / Leica M11 Battery Silver [BP-SCL7] | Leica Q3, SL3 Battery [BP-SCL6] | Leica M11 Battery Silver [BP-SCL7] | weak_pass | broad_query_ambiguity | usable accessory result, but broad accessory ambiguity remains |
| leica charger | Lens / M Lens / M / Elmar / Leica / Leica M 50mm f2.8 Elmar Black | Accessory / Accessory / Q / Q3 / Leica / [중고] Leica Q3 Drop XL Wireless Charger | [위탁]Leica S Professional Charger | [중고] Leica Q3 Drop XL Wireless Charger | pass | none |  |
| leica strap | Accessory / Accessory / Unknown /  / Leica / 신품 Leica Paracord Strap Black / Red 126cm created by COOPH | Accessory / Accessory / Unknown /  / Leica / 신품 Leica Paracord Strap Black / Red 126cm created by COOPH | [위탁] Leica Carrying Strap (Black) | [중고] Cooph Leica Paracord Handstrap (Red) | weak_pass | broad_query_ambiguity | usable accessory result, but broad accessory ambiguity remains |
| leica hood | Accessory / Accessory / Unknown /  / Leica / Leica 12538 Hood Black | Accessory / Accessory / Unknown /  / Leica / Leica 12538 Hood Black | Leica 12549 Hood Silver [for M 50mm f2.8 Elmar] | Leica 12585 Hood for M-50mm, 35mm | weak_pass | broad_query_ambiguity | usable accessory result, but broad accessory ambiguity remains |
| leica adapter | Accessory / Accessory / M /  / Leica / Leica M-L adapter Black | Accessory / Accessory / M /  / Leica / Leica M-L adapter Black | Leica M-L adapter Black | Leica R-M Adapter | weak_pass | broad_query_ambiguity | usable accessory result, but broad accessory ambiguity remains |
| leica grip | Lens / M Lens / M / Elmar / Leica / Leica M 50mm f2.8 Elmar Black | Accessory / Accessory / SL / CL / Leica / Leica CL handgrip Black | Leica M10 Handgrip Black | Leica M10 Handgrip Black | pass | none |  |
| leica case | Lens / M Lens / M / Elmar / Leica / Leica M 50mm f2.8 Elmar Black | Accessory / Accessory / Q / Q2 / Leica / Leica Q2 Case Red | Leica Visoflex 2 Leather Case Black | [중고] Leica MP 가죽 케이스 | pass | none |  |
| leica pouch | Lens / M Lens / M / Elmar / Leica / Leica M 50mm f2.8 Elmar Black | Accessory / Accessory / M / M10 / Leica / Leica M10 Leather Pouch Black Small front | [중고] Leica Q2 Ettas Pouch (Midnight Blue) | [중고] 키모토 파우치 | pass | none |  |
| body cap | Accessory / Accessory / Unknown /  / Leica / [중고] Leitz Lens Cap E52.5 | Accessory / Accessory / Unknown /  / Leica / [중고] Leitz Lens Cap E52.5 | [중고] Leica Lens Cap E60 | [중고] Leica Lens Cap E55 | weak_pass | broad_query_ambiguity | usable accessory result, but broad accessory ambiguity remains |
| lens cap | Accessory / Accessory / Unknown /  / Leica / [중고] Leitz Lens Cap E52.5 | Accessory / Accessory / Unknown /  / Leica / [중고] Leitz Lens Cap E52.5 | [중고] Leica Lens Cap E60 | [중고] Leica Lens Cap E55 | weak_pass | broad_query_ambiguity | usable accessory result, but broad accessory ambiguity remains |
| rear cap | Accessory / Accessory / Unknown /  / Leica / [중고] Leitz Lens Cap E52.5 | Accessory / Accessory / Unknown /  / Leica / [중고] Leitz Lens Cap E52.5 | [중고] Leica Lens Cap E60 | [중고] Leica Lens Cap E55 | weak_pass | broad_query_ambiguity | usable accessory result, but broad accessory ambiguity remains |
| front cap | Accessory / Accessory / Unknown /  / Leica / [중고] Leitz Lens Cap E52.5 | Accessory / Accessory / Unknown /  / Leica / [중고] Leitz Lens Cap E52.5 | [중고] Leica Lens Cap E60 | [중고] Leica Lens Cap E55 | weak_pass | broad_query_ambiguity | usable accessory result, but broad accessory ambiguity remains |
| leica uv filter | Accessory / Accessory / M /  / Leica / Leica Serie8 UV Filter (M 50/1.2(B) | Accessory / Accessory / M /  / Leica / Leica Serie8 UV Filter (M 50/1.2(B) | Leica 77mm UV Filter | [위탁] Leica E49 UV/IR (Black) | weak_pass | broad_query_ambiguity | usable accessory result, but broad accessory ambiguity remains |
| leica e46 filter | Accessory / Accessory / Unknown /  / Leica / 신품 Leica E46 UVa II Black | Accessory / Accessory / Unknown /  / Leica / 신품 Leica E46 UVa II Black | 신품 Leica E46 UVa II Silver | [중고] B+W ND 1000 E46 (Black) - Summarit 용 | weak_pass | broad_query_ambiguity | usable accessory result, but broad accessory ambiguity remains |
| leica e55 filter | Accessory / Accessory / Unknown /  / Leica / [중고] Leica UVa E55 (Black) | Accessory / Accessory / Unknown /  / Leica / [중고] Leica UVa E55 (Black) | [중고] Leica E55 Uva (Black) | [중고] Leica UVa E55 (Black) | weak_pass | broad_query_ambiguity | usable accessory result, but broad accessory ambiguity remains |
| leica e60 filter | Accessory / Accessory / Unknown /  / Leica / [위탁] Leica UVa E60 (Black) | Accessory / Accessory / Unknown /  / Leica / [위탁] Leica UVa E60 (Black) | [위탁] Leica UVa E60 (Black) | [중고] Leica UVa E60 (Black) | weak_pass | broad_query_ambiguity | usable accessory result, but broad accessory ambiguity remains |
| leica viewfinder | Accessory / Accessory / Unknown /  / Leica / Leica 85mm Tele Finder C. K. S. Silver | Accessory / Accessory / Unknown /  / Leica / Leica 85mm Tele Finder C. K. S. Silver | Leica R Angle Finder Black | Leica 35-135mm VIOOH Finder Black | weak_pass | broad_query_ambiguity | usable accessory result, but broad accessory ambiguity remains |
| leica external finder | Accessory / Accessory / Unknown /  / Leica / Leica 85mm Tele Finder C. K. S. Silver | Accessory / Accessory / Unknown /  / Leica / Leica 85mm Tele Finder C. K. S. Silver | Leica R Angle Finder Black | Leica 35-135mm VIOOH Finder Black | weak_pass | broad_query_ambiguity | usable accessory result, but broad accessory ambiguity remains |
| leica angle finder | Accessory / Accessory / Unknown /  / Leica / Leica 85mm Tele Finder C. K. S. Silver | Accessory / Accessory / Unknown /  / Leica / Leica 85mm Tele Finder C. K. S. Silver | Leica R Angle Finder Black | Leica 35-135mm VIOOH Finder Black | weak_pass | broad_query_ambiguity | usable accessory result, but broad accessory ambiguity remains |

## 5. search index / normalized / raw 후보 존재 여부
- `leica handgrip`: search index / normalized / raw 모두 candidate 존재
- `leica charger`: search index / normalized / raw 모두 candidate 존재
- `leica case`: search index / normalized / raw 모두 candidate 존재
- `leica pouch`: search index / normalized / raw 모두 candidate 존재
- `sl cap`: generic cap candidate는 있으나 SL-specific cap candidate precision은 약함

## 6. 원인 분류
- `leica handgrip`, `leica grip`, `leica charger`, `leica case`, `leica pouch`: `parser_issue`
- `bp-scl5`, `r cap`, `sl cap`, 일부 broad cap/filter/finder 계열: `accessory_taxonomy_gap` 또는 `broad_query_ambiguity`

## 7. 수정 파일 목록
- `query_parser.py`
- `tests/test_accessory_taxonomy_coverage.py`
- `scripts/run_p3_accessory_taxonomy_coverage.py`

## 8. 수정하지 않은 파일/영역
- `classifier_v2.py`
- `model_detector.py`
- `query_resolver.py`
- `search_service.py`
- taxonomy seed / canonical index
- output JSON / normalized / sold_items / results.json

## 9. target / observation query after 결과
| query | before top1 | after top1 | top2 | top3 | status | cause | note |
|---|---|---|---|---|---|---|---|
| bp-scl6 | Accessory / Accessory / Q / Q3 / Leica / Leica Q3, SL3 Battery [BP-SCL6] | Accessory / Accessory / Q / Q3 / Leica / Leica Q3, SL3 Battery [BP-SCL6] | [중고] Q3,SL3 배터리 (BP-SCL6) | [위탁] Q3,SL3 배터리 (BP-SCL6) | pass | none |  |
| bp-scl5 | Accessory / Accessory / Unknown / CL / Unknown / [위탁] BP-SCL5 | Accessory / Accessory / Unknown / CL / Unknown / [위탁] BP-SCL5 | LEICA BP-SCL5 for M10/M10-p | LEICA BP-SCL5 for M10 | pass | none |  |
| leica cap | Accessory / Accessory / Unknown /  / Leica / [중고] Leitz Lens Cap E52.5 | Accessory / Accessory / Unknown /  / Leica / [중고] Leitz Lens Cap E52.5 | [중고] Leica Lens Cap E60 | [중고] Leica Lens Cap E55 | pass | none |  |
| m cap | Accessory / Accessory / M / M3 / Leica / [중고] Leica Body Cap for M3 | Accessory / Accessory / M / M3 / Leica / [중고] Leica Body Cap for M3 | Artisan & Artist M8, M9 Case Black | Leica M-L adapter Black | pass | none |  |
| r cap | Accessory / Accessory / R / R6 / Leica / [중고] Leica R6 가죽 케이스 | Accessory / Accessory / R / R6 / Leica / [중고] Leica R6 가죽 케이스 | [중고] Leica R6 가죽 케이스 | LEICA 280mm F4 APO-TELYT-R APO-EXTENDER-R sn.3622 | weak_pass | accessory_taxonomy_gap | cap query stayed accessory but mount-specific cap precision is weak |
| sl cap | Accessory / Accessory / SL /  / Unknown / LM to L 헬리코이드 어댑터 (L 마운트용) | Accessory / Accessory / SL /  / Unknown / LM to L 헬리코이드 어댑터 (L 마운트용) | Jnk SL2 Case [Black / Battery Door Type] | Jnk SL2 Case [Black / Battery Door Type] | weak_pass | accessory_taxonomy_gap | cap query stayed accessory but mount-specific cap precision is weak |
| leica finder | Accessory / Accessory / Unknown /  / Leica / Leica 85mm Tele Finder C. K. S. Silver | Accessory / Accessory / Unknown /  / Leica / Leica 85mm Tele Finder C. K. S. Silver | Leica R Angle Finder Black | Leica 35-135mm VIOOH Finder Black | pass | none |  |
| leica handgrip | Lens / M Lens / M / Elmar / Leica / Leica M 50mm f2.8 Elmar Black | Accessory / Accessory / SL / CL / Leica / Leica CL handgrip Black | Leica M10 Handgrip Black | Leica M10 Handgrip Black | pass | none |  |
| leica filter | Accessory / Accessory / Unknown /  / Leica / Leica E82 UVa II Black | Accessory / Accessory / Unknown /  / Leica / Leica E82 UVa II Black | 신품 Leica E46 UVa II Black | Leica Serie8 UV Filter (M 50/1.2(B) | pass | none |  |

| query | before top1 | after top1 | top2 | top3 | status | cause | note |
|---|---|---|---|---|---|---|---|
| leica battery | Accessory / Accessory / M / M11 / Leica / Leica M11 Battery Silver [BP-SCL7] | Accessory / Accessory / M / M11 / Leica / Leica M11 Battery Silver [BP-SCL7] | Leica Q3, SL3 Battery [BP-SCL6] | Leica M11 Battery Silver [BP-SCL7] | weak_pass | broad_query_ambiguity | usable accessory result, but broad accessory ambiguity remains |
| leica charger | Lens / M Lens / M / Elmar / Leica / Leica M 50mm f2.8 Elmar Black | Accessory / Accessory / Q / Q3 / Leica / [중고] Leica Q3 Drop XL Wireless Charger | [위탁]Leica S Professional Charger | [중고] Leica Q3 Drop XL Wireless Charger | pass | none |  |
| leica strap | Accessory / Accessory / Unknown /  / Leica / 신품 Leica Paracord Strap Black / Red 126cm created by COOPH | Accessory / Accessory / Unknown /  / Leica / 신품 Leica Paracord Strap Black / Red 126cm created by COOPH | [위탁] Leica Carrying Strap (Black) | [중고] Cooph Leica Paracord Handstrap (Red) | weak_pass | broad_query_ambiguity | usable accessory result, but broad accessory ambiguity remains |
| leica hood | Accessory / Accessory / Unknown /  / Leica / Leica 12538 Hood Black | Accessory / Accessory / Unknown /  / Leica / Leica 12538 Hood Black | Leica 12549 Hood Silver [for M 50mm f2.8 Elmar] | Leica 12585 Hood for M-50mm, 35mm | weak_pass | broad_query_ambiguity | usable accessory result, but broad accessory ambiguity remains |
| leica adapter | Accessory / Accessory / M /  / Leica / Leica M-L adapter Black | Accessory / Accessory / M /  / Leica / Leica M-L adapter Black | Leica M-L adapter Black | Leica R-M Adapter | weak_pass | broad_query_ambiguity | usable accessory result, but broad accessory ambiguity remains |
| leica grip | Lens / M Lens / M / Elmar / Leica / Leica M 50mm f2.8 Elmar Black | Accessory / Accessory / SL / CL / Leica / Leica CL handgrip Black | Leica M10 Handgrip Black | Leica M10 Handgrip Black | pass | none |  |
| leica case | Lens / M Lens / M / Elmar / Leica / Leica M 50mm f2.8 Elmar Black | Accessory / Accessory / Q / Q2 / Leica / Leica Q2 Case Red | Leica Visoflex 2 Leather Case Black | [중고] Leica MP 가죽 케이스 | pass | none |  |
| leica pouch | Lens / M Lens / M / Elmar / Leica / Leica M 50mm f2.8 Elmar Black | Accessory / Accessory / M / M10 / Leica / Leica M10 Leather Pouch Black Small front | [중고] Leica Q2 Ettas Pouch (Midnight Blue) | [중고] 키모토 파우치 | pass | none |  |
| body cap | Accessory / Accessory / Unknown /  / Leica / [중고] Leitz Lens Cap E52.5 | Accessory / Accessory / Unknown /  / Leica / [중고] Leitz Lens Cap E52.5 | [중고] Leica Lens Cap E60 | [중고] Leica Lens Cap E55 | weak_pass | broad_query_ambiguity | usable accessory result, but broad accessory ambiguity remains |
| lens cap | Accessory / Accessory / Unknown /  / Leica / [중고] Leitz Lens Cap E52.5 | Accessory / Accessory / Unknown /  / Leica / [중고] Leitz Lens Cap E52.5 | [중고] Leica Lens Cap E60 | [중고] Leica Lens Cap E55 | weak_pass | broad_query_ambiguity | usable accessory result, but broad accessory ambiguity remains |
| rear cap | Accessory / Accessory / Unknown /  / Leica / [중고] Leitz Lens Cap E52.5 | Accessory / Accessory / Unknown /  / Leica / [중고] Leitz Lens Cap E52.5 | [중고] Leica Lens Cap E60 | [중고] Leica Lens Cap E55 | weak_pass | broad_query_ambiguity | usable accessory result, but broad accessory ambiguity remains |
| front cap | Accessory / Accessory / Unknown /  / Leica / [중고] Leitz Lens Cap E52.5 | Accessory / Accessory / Unknown /  / Leica / [중고] Leitz Lens Cap E52.5 | [중고] Leica Lens Cap E60 | [중고] Leica Lens Cap E55 | weak_pass | broad_query_ambiguity | usable accessory result, but broad accessory ambiguity remains |
| leica uv filter | Accessory / Accessory / M /  / Leica / Leica Serie8 UV Filter (M 50/1.2(B) | Accessory / Accessory / M /  / Leica / Leica Serie8 UV Filter (M 50/1.2(B) | Leica 77mm UV Filter | [위탁] Leica E49 UV/IR (Black) | weak_pass | broad_query_ambiguity | usable accessory result, but broad accessory ambiguity remains |
| leica e46 filter | Accessory / Accessory / Unknown /  / Leica / 신품 Leica E46 UVa II Black | Accessory / Accessory / Unknown /  / Leica / 신품 Leica E46 UVa II Black | 신품 Leica E46 UVa II Silver | [중고] B+W ND 1000 E46 (Black) - Summarit 용 | weak_pass | broad_query_ambiguity | usable accessory result, but broad accessory ambiguity remains |
| leica e55 filter | Accessory / Accessory / Unknown /  / Leica / [중고] Leica UVa E55 (Black) | Accessory / Accessory / Unknown /  / Leica / [중고] Leica UVa E55 (Black) | [중고] Leica E55 Uva (Black) | [중고] Leica UVa E55 (Black) | weak_pass | broad_query_ambiguity | usable accessory result, but broad accessory ambiguity remains |
| leica e60 filter | Accessory / Accessory / Unknown /  / Leica / [위탁] Leica UVa E60 (Black) | Accessory / Accessory / Unknown /  / Leica / [위탁] Leica UVa E60 (Black) | [위탁] Leica UVa E60 (Black) | [중고] Leica UVa E60 (Black) | weak_pass | broad_query_ambiguity | usable accessory result, but broad accessory ambiguity remains |
| leica viewfinder | Accessory / Accessory / Unknown /  / Leica / Leica 85mm Tele Finder C. K. S. Silver | Accessory / Accessory / Unknown /  / Leica / Leica 85mm Tele Finder C. K. S. Silver | Leica R Angle Finder Black | Leica 35-135mm VIOOH Finder Black | weak_pass | broad_query_ambiguity | usable accessory result, but broad accessory ambiguity remains |
| leica external finder | Accessory / Accessory / Unknown /  / Leica / Leica 85mm Tele Finder C. K. S. Silver | Accessory / Accessory / Unknown /  / Leica / Leica 85mm Tele Finder C. K. S. Silver | Leica R Angle Finder Black | Leica 35-135mm VIOOH Finder Black | weak_pass | broad_query_ambiguity | usable accessory result, but broad accessory ambiguity remains |
| leica angle finder | Accessory / Accessory / Unknown /  / Leica / Leica 85mm Tele Finder C. K. S. Silver | Accessory / Accessory / Unknown /  / Leica / Leica 85mm Tele Finder C. K. S. Silver | Leica R Angle Finder Black | Leica 35-135mm VIOOH Finder Black | weak_pass | broad_query_ambiguity | usable accessory result, but broad accessory ambiguity remains |

## 10. known accessory guardrail 결과
| query | before top1 | after top1 | top2 | top3 | status | cause | note |
|---|---|---|---|---|---|---|---|
| sl3 battery | Accessory / Accessory / SL / Q3 / Unknown / [중고] Q3,SL3 배터리 (BP-SCL6) | Accessory / Accessory / SL / Q3 / Unknown / [중고] Q3,SL3 배터리 (BP-SCL6) | [위탁] Q3,SL3 배터리 (BP-SCL6) | [중고] Q3,SL3 배터리 (BP-SCL6) | guardrail_pass | none |  |
| leica m strap | Accessory / Accessory / M / M11 / Leica / [중고] Leica M11 strap (Cognac) | Accessory / Accessory / M / M11 / Leica / [중고] Leica M11 strap (Cognac) | [중고] Leica M11 Neck strap (Cognac) | Leica M-L adapter Black | guardrail_pass | none |  |
| leica hood 12585 | Accessory / Accessory / M /  / Leica / Leica 12585 Hood for M-50mm, 35mm | Accessory / Accessory / M /  / Leica / Leica 12585 Hood for M-50mm, 35mm | [중고] Leica 12585 후드 | [중고] Leica 12585 후드 | guardrail_pass | none |  |
| hood 12549 | Accessory / Accessory / M / Elmar / Leica / Leica 12549 Hood Silver [for M 50mm f2.8 Elmar] | Accessory / Accessory / M / Elmar / Leica / Leica 12549 Hood Silver [for M 50mm f2.8 Elmar] | Leica 12549 Lens Hood Silver （Elmar） | LEICA 12549 | guardrail_pass | none |  |
| m adapter l | Accessory / Accessory / M /  / Leica / Leica M-L adapter Black | Accessory / Accessory / M /  / Leica / Leica M-L adapter Black | Leica M-L adapter Black | Leica M-L adapter Silver | guardrail_pass | none |  |
| r adapter | Accessory / Accessory / R / R6 / Leica / [중고] Leica R6 가죽 케이스 | Accessory / Accessory / R / R6 / Leica / [중고] Leica R6 가죽 케이스 | [중고] Leica R6 가죽 케이스 | LEICA 280mm F4 APO-TELYT-R APO-EXTENDER-R sn.3622 | guardrail_pass | none |  |
| leica r adapter | Accessory / Accessory / R / R6 / Leica / [중고] Leica R6 가죽 케이스 | Accessory / Accessory / R / R6 / Leica / [중고] Leica R6 가죽 케이스 | [중고] Leica R6 가죽 케이스 | LEICA 280mm F4 APO-TELYT-R APO-EXTENDER-R sn.3622 | guardrail_pass | none |  |
| leica r cap | Accessory / Accessory / R / R6 / Leica / [중고] Leica R6 가죽 케이스 | Accessory / Accessory / R / R6 / Leica / [중고] Leica R6 가죽 케이스 | [중고] Leica R6 가죽 케이스 | LEICA 280mm F4 APO-TELYT-R APO-EXTENDER-R sn.3622 | guardrail_pass | none |  |
| r lens cap | Accessory / Accessory / R / R6 / Leica / [중고] Leica R6 가죽 케이스 | Accessory / Accessory / R / R6 / Leica / [중고] Leica R6 가죽 케이스 | [중고] Leica R6 가죽 케이스 | LEICA 280mm F4 APO-TELYT-R APO-EXTENDER-R sn.3622 | guardrail_pass | none |  |
| r hood | Accessory / Accessory / R / R6 / Leica / [중고] Leica R6 가죽 케이스 | Accessory / Accessory / R / R6 / Leica / [중고] Leica R6 가죽 케이스 | [중고] Leica R6 가죽 케이스 | LEICA 280mm F4 APO-TELYT-R APO-EXTENDER-R sn.3622 | guardrail_pass | none |  |

## 11. M Lens guardrail 결과
| query | before top1 | after top1 | top2 | top3 | status | cause | note |
|---|---|---|---|---|---|---|---|
| summicron 50 | Lens / L Lens / L / Summicron / Leica / Leica L 50mm f2 Summicron Silver | Lens / L Lens / L / Summicron / Leica / Leica L 50mm f2 Summicron Silver | Leica L 50mm f2 Summicron Rigid Silver | Leica L 50mm f2 Summicron Silver | weak_pass | broad_query_ambiguity | broad M shorthand stayed lens-side but remains ambiguous |
| summicron m 50 | Lens / M Lens / M / Summicron-M / Leica / Leica M 50mm f2 Summicron Rigid Silver | Lens / M Lens / M / Summicron-M / Leica / Leica M 50mm f2 Summicron Rigid Silver | Leica M 50mm f2 APO-Summicron ASPH Black Chrome finish | Leica M 50mm f 2 Summicron Rigid BlackRepaint | guardrail_pass | none |  |
| m 50 summicron | Lens / M Lens / M / Summicron-M / Leica / Leica M 50mm f2 Summicron Rigid Silver | Lens / M Lens / M / Summicron-M / Leica / Leica M 50mm f2 Summicron Rigid Silver | Leica M 50mm f2 APO-Summicron ASPH Black Chrome finish | Leica M 50mm f 2 Summicron Rigid BlackRepaint | guardrail_pass | none |  |
| leica m 50 summicron | Lens / M Lens / M / Summicron-M / Leica / Leica M 50mm f2 Summicron Rigid Silver | Lens / M Lens / M / Summicron-M / Leica / Leica M 50mm f2 Summicron Rigid Silver | Leica M 50mm f2 APO-Summicron ASPH Black Chrome finish | Leica M 50mm f 2 Summicron Rigid BlackRepaint | guardrail_pass | none |  |
| 50 cron | Lens / R Lens / R / Summicron-R / Leica / Leica R 50mm f2 Summicron Black | Lens / R Lens / R / Summicron-R / Leica / Leica R 50mm f2 Summicron Black | Leica SL 50mm f2 APO-Summicron ASPH Black | Leica M 50mm f2 Summicron Rigid Silver | weak_pass | broad_query_ambiguity | broad M shorthand stayed lens-side but remains ambiguous |
| 35 lux | Lens / M Lens / M / Summilux-M / Leica / Leica M 35mm f1.4 Summilux 2nd Titan | Lens / M Lens / M / Summilux-M / Leica / Leica M 35mm f1.4 Summilux 2nd Titan | Leica M 35mm f1.4 Summilux 1st Silver [Steel Rim] | Leica M 35mm f1.4 Summilux ASPH 4th Titan | guardrail_pass | none |  |
| 50 lux | Lens / M Lens / M / Summilux-M / Leica / Leica M 50mm f1.4 Summilux Classic Silver | Lens / M Lens / M / Summilux-M / Leica / Leica M 50mm f1.4 Summilux Classic Silver | Leica M 50mm f1.4 Summilux 4th Silver | Leica M 50mm f1.4 Summilux ASPH 6bit Silver | guardrail_pass | none |  |
| elmarit m 28 | Lens / M Lens / M / Elmarit-M / Leica / Leica M 28mm f2.8 Elmarit ASPH 5th 6bit Black | Lens / M Lens / M / Elmarit-M / Leica / Leica M 28mm f2.8 Elmarit ASPH 5th 6bit Black | Leica M 28mm f2.8 Elmarit 3rd Black | Leica M 28mm f2.8 Elmarit 2nd Black | guardrail_pass | none |  |
| m 28 elmarit | Lens / M Lens / M / Elmarit-M / Leica / Leica M 28mm f2.8 Elmarit ASPH 5th 6bit Black | Lens / M Lens / M / Elmarit-M / Leica / Leica M 28mm f2.8 Elmarit ASPH 5th 6bit Black | Leica M 28mm f2.8 Elmarit 3rd Black | Leica M 28mm f2.8 Elmarit 2nd Black | guardrail_pass | none |  |
| apo telyt m 135 | Lens / M Lens / M / Tele-Elmar / Leica / Leica M 135mm f4 Tele-Elmar Black | Lens / M Lens / M / Tele-Elmar / Leica / Leica M 135mm f4 Tele-Elmar Black | Leica M 135mm f4.5 Hektor Silver | Leica M 135mm f4 Tele-Elmar Black | guardrail_pass | none |  |
| m 135 apo telyt | Lens / M Lens / M / Tele-Elmar / Leica / Leica M 135mm f4 Tele-Elmar Black | Lens / M Lens / M / Tele-Elmar / Leica / Leica M 135mm f4 Tele-Elmar Black | Leica M 135mm f4.5 Hektor Silver | Leica M 135mm f4 Tele-Elmar Black | guardrail_pass | none |  |
| Leica M 35mm f2 Summicron ASPH 6bit Black with hood | Lens / M Lens / M / APO-Summicron / Leica / Leica M 35mm f2 APO-Summicron ASPH 6bit Black | Lens / M Lens / M / APO-Summicron / Leica / Leica M 35mm f2 APO-Summicron ASPH 6bit Black | Leica M 35mm f2 Summicron ASPH Anthracite Finish | 신품 Leica M 35mm f2 APO-Summicron ASPH 6bit Black | guardrail_pass | none |  |

## 12. SL Lens guardrail 결과
| query | before top1 | after top1 | top2 | top3 | status | cause | note |
|---|---|---|---|---|---|---|---|
| summicron sl 35 | Lens / SL Lens / SL / Summicron-SL / Leica / 신품 Leica SL 35mm f2 Summicron ASPH Black | Lens / SL Lens / SL / Summicron-SL / Leica / 신품 Leica SL 35mm f2 Summicron ASPH Black | [중고] Leica SL2 with Summicron-SL 35mm f/2 ASPH | LEICA 35mm F2 ASPH APO-SUMMICRON-SL sn.4720 | guardrail_pass | none |  |
| Leica 35mm F2 AsphSummicron SL | Lens / SL Lens / SL / Summicron-SL / Leica / 신품 Leica SL 35mm f2 Summicron ASPH Black | Lens / SL Lens / SL / Summicron-SL / Leica / 신품 Leica SL 35mm f2 Summicron ASPH Black | [중고] Leica SL2 with Summicron-SL 35mm f/2 ASPH | LEICA 35mm F2 ASPH APO-SUMMICRON-SL sn.4720 | guardrail_pass | none |  |
| apo summicron sl 35 | Lens / SL Lens / SL / Summicron-SL / Leica / 신품 Leica SL 35mm f2 Summicron ASPH Black | Lens / SL Lens / SL / Summicron-SL / Leica / 신품 Leica SL 35mm f2 Summicron ASPH Black | [중고] Leica SL2 with Summicron-SL 35mm f/2 ASPH | LEICA 35mm F2 ASPH APO-SUMMICRON-SL sn.4720 | weak_pass | broad_query_ambiguity | APO family ranking still loose but stayed lens-side |
| sl 35 summicron | Lens / SL Lens / SL / Summicron-SL / Leica / 신품 Leica SL 35mm f2 Summicron ASPH Black | Lens / SL Lens / SL / Summicron-SL / Leica / 신품 Leica SL 35mm f2 Summicron ASPH Black | [중고] Leica SL2 with Summicron-SL 35mm f/2 ASPH | LEICA 35mm F2 ASPH APO-SUMMICRON-SL sn.4720 | guardrail_pass | none |  |
| sl 50 summicron | Lens / SL Lens / SL / APO-Summicron / Leica / Leica SL 50mm f2 APO-Summicron ASPH Black | Lens / SL Lens / SL / APO-Summicron / Leica / Leica SL 50mm f2 APO-Summicron ASPH Black | [위탁] Leica SL2-S Kit with Summicron-SL 50mm f/2 ASPH | [중고] Leica Summicron-SL 50mm f/2 ASPH | guardrail_pass | none |  |
| sl 75 summicron | Lens / SL Lens / SL / APO-Summicron / Leica / LEICA 75mm F2 ASPH APO-SUMMICRON-SL sn.4709 | Lens / SL Lens / SL / APO-Summicron / Leica / LEICA 75mm F2 ASPH APO-SUMMICRON-SL sn.4709 | LEICA 75mm F2 APO-SUMMICRON-SL sn.4699 | Leica SL 50mm f2 APO-Summicron ASPH Black | guardrail_pass | none |  |
| sl 90 summicron | Lens / SL Lens / SL / APO-Summicron / Leica / LEICA 90mm F2 ASPH APO-summicron-SL sn.4713 | Lens / SL Lens / SL / APO-Summicron / Leica / LEICA 90mm F2 ASPH APO-summicron-SL sn.4713 | [중고] SL 90/2 APO-Summicron | [중고] SL 90/2 APO Summicron ASPH (Black) | guardrail_pass | none |  |
| sl 24-90 | Lens / SL Lens / SL / Vario-Elmarit-SL / Leica / Leica SL 24-90mm f2.8-4 Vario-Elmarit Black | Lens / SL Lens / SL / Vario-Elmarit-SL / Leica / Leica SL 24-90mm f2.8-4 Vario-Elmarit Black | Leica SL 24-90mm f2.8-4 Vario-Elmarit Black | [위탁] SL 24-90/2.8-4 Vario Elmar ASPH (Black) | guardrail_pass | none |  |
| sl 14-24 | Lens / SL Lens / SL / Super-Vario-Elmarit-SL / Leica / [중고] SL 14-24/2.8 Vario Elmarit ASPH (Black) | Lens / SL Lens / SL / Super-Vario-Elmarit-SL / Leica / [중고] SL 14-24/2.8 Vario Elmarit ASPH (Black) | [중고] SL 14-24/2.8 Vario Elmarit ASPH (Black) | [중고] SL 14-24/2.8 Vario Elmarit ASPH (Black) | guardrail_pass | none |  |
| sl 16-35 | Lens / SL Lens / SL / Super-Vario-Elmar-SL / Leica / [중고] SL 16-35/3.5-4.5 Super Vario Elmar ASPH (Black) | Lens / SL Lens / SL / Super-Vario-Elmar-SL / Leica / [중고] SL 16-35/3.5-4.5 Super Vario Elmar ASPH (Black) | [중고] SL 16-35/3.5-4.5 Super Vario Elmar ASPH (Black) | LEICA SL2 16-35mm F3.5-4.5 ASPH sn.4687/5576 | guardrail_pass | none |  |
| sl 90-280 | Lens / SL Lens / SL / APO-Vario-Elmarit-SL / Leica / [중고] SL APO Vario Elmarit 90-280 f/2.8-4 | Lens / SL Lens / SL / APO-Vario-Elmarit-SL / Leica / [중고] SL APO Vario Elmarit 90-280 f/2.8-4 | [중고] SL APO Vario Elmarit 90-280 f/2.8-4 | [중고] SL 90-280/2.8-4 APO Vario Elmarit ASPH (Black) | guardrail_pass | none |  |

## 13. R Lens guardrail 결과
| query | before top1 | after top1 | top2 | top3 | status | cause | note |
|---|---|---|---|---|---|---|---|
| r 50 summicron | Lens / R Lens / R / Summicron-R / Leica / Leica R 50mm f2 Summicron Black | Lens / R Lens / R / Summicron-R / Leica / Leica R 50mm f2 Summicron Black | LEICA 50mm F2 SUMMICRON-R sn.3338 | LEICA 50mm F2 ROM SUMMICRON-R sn.3819 | guardrail_pass | none |  |
| summicron-r 50 | Lens / R Lens / R / Summicron-R / Leica / Leica R 50mm f2 Summicron Black | Lens / R Lens / R / Summicron-R / Leica / Leica R 50mm f2 Summicron Black | LEICA 50mm F2 SUMMICRON-R sn.3338 | LEICA 50mm F2 ROM SUMMICRON-R sn.3819 | guardrail_pass | none |  |
| r 180 apo | Lens / R Lens / R / APO-Telyt-R / Leica / Leica R 180mm f3.4 APO-Telyt Black | Lens / R Lens / R / APO-Telyt-R / Leica / Leica R 180mm f3.4 APO-Telyt Black | Leica R 180mm f3.4 APO-Telyt Black | LEICA 180mm F3.4 APO-TELYT-R sn.3478 | guardrail_pass | none |  |
| apo-telyt-r 180 | Lens / R Lens / R / APO-Telyt-R / Leica / Leica R 180mm f3.4 APO-Telyt Black | Lens / R Lens / R / APO-Telyt-R / Leica / Leica R 180mm f3.4 APO-Telyt Black | Leica R 180mm f3.4 APO-Telyt Black | LEICA 180mm F3.4 APO-TELYT-R sn.3478 | guardrail_pass | none |  |
| elmarit r 135 | Lens / R Lens / R / Elmarit-R / Leica / LEICA 135mm F2.8 ELMARIT-R sn.2155 | Lens / R Lens / R / Elmarit-R / Leica / LEICA 135mm F2.8 ELMARIT-R sn.2155 | LEICA 135mm F2.8 ELMARIT-R sn.2772 | LEICA 135mm F2.8 ELMARIT-R sn.2809 | guardrail_pass | none |  |
| r 135 elmarit | Lens / R Lens / R / Elmarit-R / Leica / LEICA 135mm F2.8 ELMARIT-R sn.2155 | Lens / R Lens / R / Elmarit-R / Leica / LEICA 135mm F2.8 ELMARIT-R sn.2155 | LEICA 135mm F2.8 ELMARIT-R sn.2772 | LEICA 135mm F2.8 ELMARIT-R sn.2809 | guardrail_pass | none |  |
| vario elmarit r 28-90 | Lens / R Lens / R / Vario-Elmarit-R / Leica / LEICA 28-90mm F2.8-4.5 VARIO-ELMARIT-R sn.3975 | Lens / R Lens / R / Vario-Elmarit-R / Leica / LEICA 28-90mm F2.8-4.5 VARIO-ELMARIT-R sn.3975 | LEICA 28-90mm F2.8-4.5 ASPH VARIO-ELMARIT-R sn.3974 | LEICA 28-90mm F2.8-4.5 VARIO-ELMARIT-R sn.3973 | guardrail_pass | none |  |
| r 28-90 vario elmarit | Lens / R Lens / R / Vario-Elmarit-R / Leica / LEICA 28-90mm F2.8-4.5 VARIO-ELMARIT-R sn.3975 | Lens / R Lens / R / Vario-Elmarit-R / Leica / LEICA 28-90mm F2.8-4.5 VARIO-ELMARIT-R sn.3975 | LEICA 28-90mm F2.8-4.5 ASPH VARIO-ELMARIT-R sn.3974 | LEICA 28-90mm F2.8-4.5 VARIO-ELMARIT-R sn.3973 | guardrail_pass | none |  |

## 14. Body guardrail 결과
| query | before top1 | after top1 | top2 | top3 | status | cause | note |
|---|---|---|---|---|---|---|---|
| leica sl2 | Body / SL Body / SL / SL2 / Leica / Leica SL2 Black | Body / SL Body / SL / SL2 / Leica / Leica SL2 Black | Leica SL2 Black | Leica SL2-S Reporter | guardrail_pass | none |  |
| leica sl3 | Body / SL Body / SL / SL3 / Leica / Leica SL3 Black | Body / SL Body / SL / SL3 / Leica / Leica SL3 Black | Leica SL3 Reporter | Leica SL3 Body Only | guardrail_pass | none |  |
| leica m10 body | Body / M Body / M / M10 / Leica / [위탁] M10 Monochrom 'Leitz Wetzlar' Edition | Body / M Body / M / M10 / Leica / [위탁] M10 Monochrom 'Leitz Wetzlar' Edition | [중고] Leica M10 홀스터 | [중고] Leica M10 하프케이스 (Brown) | guardrail_pass | none |  |
| leica iiif | Body / L Body / L / IIIf / Leica / Leica Barnack IIIF Silver | Body / L Body / L / IIIf / Leica / Leica Barnack IIIF Silver | Leica Barnack IIIf Silver | Leica Barnack IIIF Silver | guardrail_pass | none |  |
| barnack iiif | Body / L Body / L / IIIf / Leica / Leica Barnack IIIF Silver | Body / L Body / L / IIIf / Leica / Leica Barnack IIIF Silver | Leica Barnack IIIf Silver | Leica Barnack IIIF Silver | guardrail_pass | none |  |
| leica q2 | Body / Leica Body / Q / Q2 / Leica / Leica Q2 007 Edition | Body / Leica Body / Q / Q2 / Leica / Leica Q2 007 Edition | Leica Q2 Black | [중고] Leica Q2 Monochrome | guardrail_pass | none |  |

## 15. third-party L-mount guardrail 결과
| query | before top1 | after top1 | top2 | top3 | status | cause | note |
|---|---|---|---|---|---|---|---|
| sigma 24-70 l | Lens / SL Lens / SL /  / 3rd Party / [중고] Sigma 24-70/2.8 (SL 마운트) | Lens / SL Lens / SL /  / 3rd Party / [중고] Sigma 24-70/2.8 (SL 마운트) | [위탁] 시그마 24-70/2.8 (SL 마운트) | [중고] Sigma 24-70/2.8 (SL 마운트) | guardrail_pass | none |  |
| sigma 24-70 dg dn | Lens / SL Lens / SL /  / 3rd Party / [중고] Sigma 24-70/2.8 (SL 마운트) | Lens / SL Lens / SL /  / 3rd Party / [중고] Sigma 24-70/2.8 (SL 마운트) | [위탁] 시그마 24-70/2.8 (SL 마운트) | [중고] Sigma 24-70/2.8 (SL 마운트) | guardrail_pass | none |  |
| panasonic 24-105 l | Lens / SL Lens / SL /  / 3rd Party / [중고] 파나소닉 24-105 L 마운트 | Lens / SL Lens / SL /  / 3rd Party / [중고] 파나소닉 24-105 L 마운트 | - | - | guardrail_pass | none |  |
| lumix 24-105 | Lens / SL Lens / SL /  / 3rd Party / [중고] 파나소닉 24-105 L 마운트 | Lens / SL Lens / SL /  / 3rd Party / [중고] 파나소닉 24-105 L 마운트 | - | - | guardrail_pass | none |  |
| sigma l 30mm | Lens / SL Lens / SL /  / 3rd Party / Sigma L 30mm f1.4 DC DN Black for CL, TL2, etc | Lens / SL Lens / SL /  / 3rd Party / Sigma L 30mm f1.4 DC DN Black for CL, TL2, etc | Leica S 30mm f2.8 Elmarit ASPH CS Black | [위탁] Elmarit-S 30mm f/2.8 ASPH CS | guardrail_pass | none |  |
| sigma 30mm l | Lens / SL Lens / SL /  / 3rd Party / Sigma L 30mm f1.4 DC DN Black for CL, TL2, etc | Lens / SL Lens / SL /  / 3rd Party / Sigma L 30mm f1.4 DC DN Black for CL, TL2, etc | Leica S 30mm f2.8 Elmarit ASPH CS Black | [위탁] Elmarit-S 30mm f/2.8 ASPH CS | guardrail_pass | none |  |
| sigma 14-24 l |  /  /  /  /  /  |  /  /  /  /  /  | - | - | no_result_confirmed | no_result_confirmed | no candidate found in search index / normalized / raw |

## 16. broad alias guardrail 결과
| query | before top1 | after top1 | top2 | top3 | status | cause | note |
|---|---|---|---|---|---|---|---|
| summicron | Lens / L Lens / L / Summicron / Leica / Leica L 50mm f2 Summicron Silver | Lens / L Lens / L / Summicron / Leica / Leica L 50mm f2 Summicron Silver | Leica L 50mm f2 Summicron Rigid Silver | Leica L 50mm f2 Summicron Silver | guardrail_pass | none |  |
| summilux | Lens / L Lens / L / Summilux / Leica / [중고] L 50/1.4 Summilux 4세대 (Silver) | Lens / L Lens / L / Summilux / Leica / [중고] L 50/1.4 Summilux 4세대 (Silver) | LEICA 50mm F1.4 SUMMILUX M39 sn.3868 | LEICA 50mm F1.4 Screwmount M39 SUMMILUX-L sn.3868 | guardrail_pass | none |  |
| leica summicron | Lens / L Lens / L / Summicron / Leica / Leica L 50mm f2 Summicron Silver | Lens / L Lens / L / Summicron / Leica / Leica L 50mm f2 Summicron Silver | Leica L 50mm f2 Summicron Rigid Silver | Leica L 50mm f2 Summicron Silver | guardrail_pass | none |  |
| leica summilux | Lens / L Lens / L / Summilux / Leica / [중고] L 50/1.4 Summilux 4세대 (Silver) | Lens / L Lens / L / Summilux / Leica / [중고] L 50/1.4 Summilux 4세대 (Silver) | LEICA 50mm F1.4 SUMMILUX M39 sn.3868 | LEICA 50mm F1.4 Screwmount M39 SUMMILUX-L sn.3868 | guardrail_pass | none |  |
| cron | Lens / R Lens / R / Summicron-R / Leica / Leica R 50mm f2 Summicron Black | Lens / R Lens / R / Summicron-R / Leica / Leica R 50mm f2 Summicron Black | 신품 호환 Leica 14043 Hood Cover for M 35mm f2 Summicron, M 28mm f2.8 Elmarit | Leica M 28mm f2 Summicron ASPH 6bit Safari Edition | observation_only | broad_query_ambiguity | short alias intentionally left ambiguous |
| lux | Lens / M Lens / M / Summilux-M / Leica / Leica M 28mm f1.4 Summilux ASPH 6bit Black | Lens / M Lens / M / Summilux-M / Leica / Leica M 28mm f1.4 Summilux ASPH 6bit Black | Leica M 50mm f1.4 Summilux Classic Silver | Leica M 50mm f1.4 Summilux 4th Silver | observation_only | broad_query_ambiguity | short alias intentionally left ambiguous |

## 17. status 요약
- 총 query 수: `88`
- `guardrail_pass`: `54`
- `no_result_confirmed`: `1`
- `observation_only`: `2`
- `pass`: `11`
- `weak_pass`: `20`

## 18. 남은 위험
- `r cap`: `weak_pass` / `Accessory:R6:Leica` - cap query stayed accessory but mount-specific cap precision is weak
- `sl cap`: `weak_pass` / `Accessory::Unknown` - cap query stayed accessory but mount-specific cap precision is weak
- `leica battery`: `weak_pass` / `Accessory:M11:Leica` - usable accessory result, but broad accessory ambiguity remains
- `leica strap`: `weak_pass` / `Accessory::Leica` - usable accessory result, but broad accessory ambiguity remains
- `leica hood`: `weak_pass` / `Accessory::Leica` - usable accessory result, but broad accessory ambiguity remains
- `leica adapter`: `weak_pass` / `Accessory::Leica` - usable accessory result, but broad accessory ambiguity remains
- `body cap`: `weak_pass` / `Accessory::Leica` - usable accessory result, but broad accessory ambiguity remains
- `lens cap`: `weak_pass` / `Accessory::Leica` - usable accessory result, but broad accessory ambiguity remains
- `rear cap`: `weak_pass` / `Accessory::Leica` - usable accessory result, but broad accessory ambiguity remains
- `front cap`: `weak_pass` / `Accessory::Leica` - usable accessory result, but broad accessory ambiguity remains
- `leica uv filter`: `weak_pass` / `Accessory::Leica` - usable accessory result, but broad accessory ambiguity remains
- `leica e46 filter`: `weak_pass` / `Accessory::Leica` - usable accessory result, but broad accessory ambiguity remains

## 19. no-result / source coverage 후보
- `sigma 14-24 l`: `no_result_confirmed` / `::` - no candidate found in search index / normalized / raw

## 20. 결론
- `leica handgrip`와 같은 명시적 accessory alias는 search-layer parser 보정으로 복구됐다.
- `bp-scl5`, `r cap`, `sl cap`처럼 subtype precision이 느슨한 항목은 taxonomy / alias coverage follow-up이 여전히 필요하다.
- lens/body/third-party/broad alias guardrail은 유지됐다.
