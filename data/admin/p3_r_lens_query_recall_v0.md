# P3-R-LENS-QUERY-RECALL

## 1. 목적
- Leica R lens query가 search-layer에서 M Lens / SL Lens / Body / Accessory / third-party로 새지 않고, 후보가 있을 때 R Lens로 안정적으로 회수되는지 점검/복구한다.
- 이번 라운드는 classifier/model_detector/taxonomy/output regeneration이 아니라 search-layer parser recall 보정 라운드다.

## 2. 수정 전 문제 요약
- `summicron-r 50`는 `summicron-r` token이 parser에서 죽어서 M Lens top1으로 밀렸다.
- `apo-telyt-r 180`, `r 180 apo`, `apo telyt r 180` 계열은 R mount는 살아도 exact family가 잡히지 않아 `APO-Telyt-R` 대신 `APO-Elmarit/Elmar-R` 쪽이 top1을 먹었다.
- `elmarit-r 28`, `elmarit-r 35`, `summicron-r 90`는 hyphenated `*-r` family token이 parser에서 unknown으로 남아 non-R 결과에 밀렸다.
- `vario elmarit r 28-90`, `r 28-90 vario elmarit`는 `28-90` range + `vario elmarit r` 구조를 parser가 좁게 구조화하지 못해 generic `Elmarit-R 28` 쪽이 top1을 먹었다.

## 3. target / observation query before 결과
| query | before top1 | after top1 | status | note |
|---|---|---|---|---|
| r 50 summicron | Lens / R Lens / R / Summicron-R / Leica R 50mm f2 Summicron Black | Lens / R Lens / R / Summicron-R / Leica R 50mm f2 Summicron Black | pass |  |
| summicron-r 50 | Lens / M Lens / M / Elmar / Leica M 50mm f2.8 Elmar Black | Lens / R Lens / R / Summicron-R / Leica R 50mm f2 Summicron Black | pass | recovered by narrow R parser hint / hyphenated family parsing |
| summicron r 50 | Lens / R Lens / R / Summicron-R / Leica R 50mm f2 Summicron Black | Lens / R Lens / R / Summicron-R / Leica R 50mm f2 Summicron Black | pass |  |
| r 50/2 summicron | Lens / R Lens / R / Summicron-R / Leica R 50mm f2 Summicron Black | Lens / R Lens / R / Summicron-R / Leica R 50mm f2 Summicron Black | pass |  |
| leica r 50mm f2 summicron | Lens / R Lens / R / Summicron-R / Leica R 50mm f2 Summicron Black | Lens / R Lens / R / Summicron-R / Leica R 50mm f2 Summicron Black | pass |  |
| r 180 apo | Lens / R Lens / R / Elmar-R / Leica R 180mm f2.8 APO-Elmarit Rom Black | Lens / R Lens / R / APO-Telyt-R / Leica R 180mm f3.4 APO-Telyt Black | pass | recovered by narrow R parser hint / hyphenated family parsing |
| r 180 apo telyt | Lens / R Lens / R / Elmar-R / Leica R 180mm f2.8 APO-Elmarit Rom Black | Lens / R Lens / R / APO-Telyt-R / Leica R 180mm f3.4 APO-Telyt Black | pass | recovered by narrow R parser hint / hyphenated family parsing |
| apo telyt r 180 | Lens / R Lens / R / Elmar-R / Leica R 180mm f2.8 APO-Elmarit Rom Black | Lens / R Lens / R / APO-Telyt-R / Leica R 180mm f3.4 APO-Telyt Black | pass | recovered by narrow R parser hint / hyphenated family parsing |
| apo-telyt-r 180 | Lens / R Lens / R / Elmar-R / Leica R 180mm f2.8 APO-Elmarit Rom Black | Lens / R Lens / R / APO-Telyt-R / Leica R 180mm f3.4 APO-Telyt Black | pass | recovered by narrow R parser hint / hyphenated family parsing |
| r 180/3.4 apo | Lens / R Lens / R / APO-Telyt-R / Leica R 180mm f3.4 APO-Telyt Black | Lens / R Lens / R / APO-Telyt-R / Leica R 180mm f3.4 APO-Telyt Black | pass |  |
| leica r 180mm f3.4 apo telyt | Lens / R Lens / R / APO-Telyt-R / Leica R 180mm f3.4 APO-Telyt Black | Lens / R Lens / R / APO-Telyt-R / Leica R 180mm f3.4 APO-Telyt Black | pass |  |
| elmarit r 135 | Lens / R Lens / R / Elmarit-R / LEICA 135mm F2.8 ELMARIT-R sn.2155 | Lens / R Lens / R / Elmarit-R / LEICA 135mm F2.8 ELMARIT-R sn.2155 | pass |  |
| r 135 elmarit | Lens / R Lens / R / Elmarit-R / LEICA 135mm F2.8 ELMARIT-R sn.2155 | Lens / R Lens / R / Elmarit-R / LEICA 135mm F2.8 ELMARIT-R sn.2155 | pass |  |
| leica r 135mm f2.8 elmarit | Lens / R Lens / R / Elmarit-R / LEICA 135mm F2.8 ELMARIT-R sn.2155 | Lens / R Lens / R / Elmarit-R / LEICA 135mm F2.8 ELMARIT-R sn.2155 | pass |  |
| elmarit-r 28 | Lens / M Lens / M / Summilux-M / prior repro: M 28 Summilux top1 | Lens / R Lens / R / Elmarit-R / Leica R 28mm f2.8 Elmarit Rom Black | weak_pass | recovered by narrow R parser hint / hyphenated family parsing |
| r 28 elmarit | Lens / R Lens / R / Elmarit-R / Leica R 28mm f2.8 Elmarit Rom Black | Lens / R Lens / R / Elmarit-R / Leica R 28mm f2.8 Elmarit Rom Black | weak_pass |  |
| leica r 28mm f2.8 elmarit | Lens / R Lens / R / Elmarit-R / Leica R 28mm f2.8 Elmarit Rom Black | Lens / R Lens / R / Elmarit-R / Leica R 28mm f2.8 Elmarit Rom Black | weak_pass |  |
| vario elmarit r 28-90 | Lens / R Lens / R / Elmarit-R / Leica R 28mm f2.8 Elmarit Rom Black | Lens / R Lens / R / Vario-Elmarit-R / LEICA 28-90mm F2.8-4.5 VARIO-ELMARIT-R sn.3975 | weak_pass | recovered by narrow R parser hint / hyphenated family parsing |
| r 28-90 vario elmarit | Lens / R Lens / R / Elmarit-R / Leica R 28mm f2.8 Elmarit Rom Black | Lens / R Lens / R / Vario-Elmarit-R / LEICA 28-90mm F2.8-4.5 VARIO-ELMARIT-R sn.3975 | weak_pass | recovered by narrow R parser hint / hyphenated family parsing |
| leica r 28-90 | Lens / R Lens / R / Summicron-R / Leica R 50mm f2 Summicron Black | Lens / R Lens / R / Summicron-R / Leica R 50mm f2 Summicron Black | observation_only | observation-only ambiguous query; not hard-pinned in this round |
| r 35 elmarit | Lens / R Lens / R / Elmarit-R / LEICA R6.2 35mm F2.8 ELMARIT-R sn.1923 | Lens / R Lens / R / Elmarit-R / LEICA R6.2 35mm F2.8 ELMARIT-R sn.1923 | weak_pass |  |
| elmarit-r 35 | Lens / M Lens / M / unknown / prior repro: third-party M 35 top1 | Lens / R Lens / R / Elmarit-R / LEICA R6.2 35mm F2.8 ELMARIT-R sn.1923 | weak_pass | recovered by narrow R parser hint / hyphenated family parsing |
| r 90 summicron | Lens / R Lens / R / Summicron-R / LEICA 90mm F2 SUMMICRON-R sn.3567 | Lens / R Lens / R / Summicron-R / LEICA 90mm F2 SUMMICRON-R sn.3567 | weak_pass |  |
| summicron-r 90 | Lens / M Lens / M / Summarit-M / prior repro: M 90 Summarit top1 | Lens / R Lens / R / Summicron-R / LEICA 90mm F2 SUMMICRON-R sn.3567 | weak_pass | recovered by narrow R parser hint / hyphenated family parsing |
| leica r | Lens / R Lens / R / Summicron-R / Leica R 50mm f2 Summicron Black | Lens / R Lens / R / Summicron-R / Leica R 50mm f2 Summicron Black | observation_only | observation-only ambiguous query; not hard-pinned in this round |
| r lens | Lens / R Lens / R / Summicron-R / Leica R 50mm f2 Summicron Black | Lens / R Lens / R / Summicron-R / Leica R 50mm f2 Summicron Black | observation_only | observation-only ambiguous query; not hard-pinned in this round |
| r summicron | Lens / R Lens / R / Summicron-R / Leica R 50mm f2 Summicron Black | Lens / R Lens / R / Summicron-R / Leica R 50mm f2 Summicron Black | observation_only | observation-only ambiguous query; not hard-pinned in this round |
| r elmarit | Lens / R Lens / R / Elmarit-R / Leica R 28mm f2.8 Elmarit Rom Black | Lens / R Lens / R / Elmarit-R / Leica R 28mm f2.8 Elmarit Rom Black | observation_only | observation-only ambiguous query; not hard-pinned in this round |
| r apo | Lens / R Lens / R / Summicron-R / Leica R 50mm f2 Summicron Black | Lens / R Lens / R / Summicron-R / Leica R 50mm f2 Summicron Black | observation_only | observation-only ambiguous query; not hard-pinned in this round |
| r telyt | Lens / R Lens / R / Summicron-R / Leica R 50mm f2 Summicron Black | Lens / R Lens / R / Summicron-R / Leica R 50mm f2 Summicron Black | observation_only | observation-only ambiguous query; not hard-pinned in this round |
| r vario | Lens / R Lens / R / Summicron-R / Leica R 50mm f2 Summicron Black | Lens / R Lens / R / Summicron-R / Leica R 50mm f2 Summicron Black | observation_only | observation-only ambiguous query; not hard-pinned in this round |

## 4. search index / normalized / raw 후보 존재 여부
- `Summicron-R 50`: search index / normalized / raw 모두 후보 존재.
- `APO-Telyt-R 180`: search index / normalized / raw 모두 후보 존재.
- `Elmarit-R 135`: search index / normalized / raw 모두 후보 존재.
- `Elmarit-R 28`, `Elmarit-R 35`, `Summicron-R 90`: search index / normalized / raw 모두 후보 존재.
- `Vario-Elmarit-R 28-90`: search index / normalized / raw 모두 후보 존재.
- 즉 이번 라운드의 핵심 이슈는 source coverage 부족보다 parser / resolver ranking 입력 품질 쪽이었다.

## 5. 원인 분류
- `summicron-r 50`, `elmarit-r 28`, `elmarit-r 35`, `summicron-r 90`: `parser_issue`
- `r 180 apo`, `r 180 apo telyt`, `apo telyt r 180`, `apo-telyt-r 180`: `parser_issue`
- `vario elmarit r 28-90`, `r 28-90 vario elmarit`: `parser_issue`
- broad observation query (`leica r`, `r lens`, `r apo`, `r telyt`, `r vario`): ambiguity 유지, hard-pin하지 않음

## 6. 수정 파일 목록
- `query_parser.py`
- `tests/test_r_lens_query_recall.py`
- 보고서:
  - `data/admin/p3_r_lens_query_recall_v0.md`
  - `data/admin/p3_r_lens_query_recall_v0.jsonl`

## 7. 수정하지 않은 파일/영역
- `classifier_v2.py` 미수정
- `model_detector.py` 미수정
- `query_resolver.py` 미수정
- taxonomy seed / canonical index 미수정
- `results.json` 미수정
- `data/normalized/normalized_latest.json` 미수정
- `data/sold_items.json` 미수정
- live crawl / output regeneration / search index write 없음

## 8. target / observation query after 결과
- Summicron-R 50 target
  - `r 50 summicron`, `summicron-r 50`, `summicron r 50`, `r 50/2 summicron`, `leica r 50mm f2 summicron`
  - now `Lens / R Lens / R / Summicron-R`
- APO-Telyt-R 180 target
  - `r 180 apo`, `r 180 apo telyt`, `apo telyt r 180`, `apo-telyt-r 180`, `r 180/3.4 apo`, `leica r 180mm f3.4 apo telyt`
  - now `Lens / R Lens / R / APO-Telyt-R`
- Elmarit-R 135 target
  - `elmarit r 135`, `r 135 elmarit`, `leica r 135mm f2.8 elmarit`
  - now `Lens / R Lens / R / Elmarit-R`
- observation improvements
  - `elmarit-r 28` -> `Lens / R Lens / R / Elmarit-R`
  - `elmarit-r 35` -> `Lens / R Lens / R / Elmarit-R`
  - `summicron-r 90` -> `Lens / R Lens / R / Summicron-R`
  - `vario elmarit r 28-90`, `r 28-90 vario elmarit` -> `Lens / R Lens / R / Vario-Elmarit-R`
- broad R observation 유지
  - `leica r`, `r lens`, `r summicron`, `r elmarit`는 R Lens-first
  - `r apo`, `r telyt`, `r vario`는 여전히 broad/ambiguous observation-only
  - `leica r 28-90`도 broad shorthand라 observation-only로 유지

## 9. M Lens guardrail 결과
- 유지됨.
- `summicron m 50`, `m 50 summicron`, `leica m 50 summicron`, `apo telyt m 135`, `m 135 apo telyt`는 계속 M Lens.
- broad `summicron 50`, `50 cron`도 R hard-pin 없이 기존 ambiguous behavior 유지.

## 10. SL Lens guardrail 결과
- 유지됨.
- `summicron sl 35`, `Leica 35mm F2 AsphSummicron SL`, `apo summicron sl 35`, `sl 35/50/75/90 summicron`, `sl 24-90`, `sl 14-24`, `sl 16-35`, `sl 90-280` 모두 기존 SL Lens/SL zoom 상태 유지.

## 11. broad alias guardrail 결과
- 유지됨.
- `summicron`, `summilux`, `leica summicron`, `leica summilux`는 기존 Lens-first 유지.
- `cron`, `lux`는 observation-only 성격 유지.
- broad alias를 R Lens로 hard-pin하지 않았다.

## 12. body guardrail 결과
- 유지됨.
- `leica sl2`, `leica sl3`, `leica m10 body`, `leica iiif`, `barnack iiif`, `leica q2` 모두 Body 유지.

## 13. accessory guardrail 결과
- 유지됨.
- `sl3 battery`, `leica m strap`, `leica hood 12585`, `hood 12549`, `m adapter l`은 기존 Accessory 유지.
- 이번 라운드에서 `cap` accessory intent도 좁게 추가되어 `r adapter`, `leica r adapter`, `leica r cap`, `r lens cap`, `r hood`도 Accessory로 유지된다.

## 14. third-party L-mount guardrail 결과
- 유지됨.
- `sigma 24-70 l`, `sigma 24-70 dg dn`, `panasonic 24-105 l`, `lumix 24-105`, `sigma l 30mm`, `sigma 30mm l` 모두 기존 third-party behavior 유지.
- `sigma 14-24 l`는 후보가 없어 no-result / source coverage issue 유지.

## 15. 테스트 결과
- `python3 tests/test_r_lens_query_recall.py` = ok
- `python3 tests/test_third_party_brand_canonicalization.py` = ok
- `python3 tests/test_third_party_l_mount_recall.py` = ok
- `python3 tests/test_no_result_recall.py` = ok
- `python3 tests/test_broad_alias_control.py` = ok
- `python3 tests/test_sl_zoom_query_recall.py` = ok
- `python3 tests/test_accessory_search_ranking.py` = ok
- `python3 tests/test_search_body_query_recall.py` = ok
- `python3 tests/test_accessory_token_guardrail.py` = ok
- `python3 tests/test_accessory_category.py` = ok
- `python3 tests/test_sl_string_drift.py` = ok
- `python3 tests/test_sl_zoom_classification.py` = ok
- `python3 tests/test_body_classification.py` = ok
- `python3 tests/test_r_tele_classification.py` = ok
- `python3 tests/test_normalization_admin.py` = ok
- `py_compile` = ok
- `golden_set.py` = 132/132

## 16. 남은 위험
- `leica r 28-90`, `r apo`, `r telyt`, `r vario` 같은 broad R shorthand는 여전히 ambiguity가 높다.
- 이번 라운드에서는 broad R 전체를 특정 family로 hard-pin하지 않았으므로, 이 쿼리들은 observation-only로 남긴다.
- R family taxonomy/seed를 열지 않았기 때문에 더 넓은 R query precision은 별도 audit이 필요하다.

## 17. 다음 backlog 후보
- `P3-QUERY-RANKING`
- `P3-ACCESSORY-TAXONOMY-COVERAGE`
- `P3-SL-ZOOM-FAMILY-TAXONOMY-AUDIT`
- `P3-CRON-LUX-SHORT-ALIAS-POLICY`
- `P3-THIRD-PARTY-SOURCE-COVERAGE`
- `P3-R-LENS-TAXONOMY-AUDIT`
