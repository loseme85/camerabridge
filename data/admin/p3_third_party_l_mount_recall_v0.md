# P3-THIRD-PARTY-L-MOUNT-RECALL

## 1. 작업 목적

- third-party L-mount query의 recall / parser intent / ranking / brand canonicalization 상태를 더 넓게 점검한다.
- 후보가 실제로 있는 경우에만 search-layer에서 좁게 복구하고, 후보가 없으면 no-result를 유지한다.
- classifier/model_detector/taxonomy/output JSON은 이번 라운드에서 수정하지 않는다.

## 2. 수정 전 문제 요약

- `sigma 24-70 l`, `panasonic 24-105 l`, `lumix 24-105`는 이전 라운드에서 no-result를 벗어났지만, Panasonic/Lumix row는 brand가 `Unknown`으로 남아 있었다.
- `sigma 14-24 l`는 여전히 search index / normalized / raw 모두 후보가 없었다.
- 이번 expanded observation에서 `panasonic lumix 24-105`와 `lumix 24-105 f4`는 실제 후보가 있는데도 각각 parser / candidate narrowing 때문에 no-result였다.

## 3. search index / normalized / raw 후보 존재 여부

- `sigma 24-70` 계열: search index / normalized / raw 모두 후보 존재
- `sigma 14-24` 계열: search index / normalized / raw 모두 후보 없음
- `panasonic 24-105` / `lumix 24-105` 계열: search index / normalized / raw 모두 후보 존재 (`[중고] 파나소닉 24-105 L 마운트`)

## 4. brand canonicalization 상태

- Sigma 24-70 row는 search 결과에서 `brand=3rd Party`로 안정적이다.
- Panasonic/Lumix 24-105 row는 search index / normalized에서 `brand=Unknown`, raw에서는 `brand=Other`로 남아 있다.
- 즉 Panasonic/Lumix brand 문제는 이번 라운드 search-layer recall보다 아래 단계의 canonicalization/normalization follow-up 성격이 더 강하다.

## 5. 수정 파일 목록

- `query_parser.py`
- `search_service.py`
- `tests/test_third_party_l_mount_recall.py`

## 6. 수정하지 않은 파일 / 영역

- `classifier_v2.py` 수정 없음
- `model_detector.py` 수정 없음
- taxonomy seed / canonical index 수정 없음
- `data/normalized/normalized_latest.json` 수정 없음
- `data/sold_items.json` 수정 없음
- `results.json` 수정 없음

## 7. target / observation query before / after

| query | before | after | cause | status | note |
|---|---|---|---|---|---|
| sigma 24-70 l | no result | [중고] Sigma 24-70/2.8 (SL 마운트) | parser_issue | pass | Candidate existed in search index/normalized/raw already; prior narrow parser recovery remains healthy. |
| sigma 14-24 l | no result | no result | raw_source_coverage_issue | needs_source_or_index_followup | No candidate found in search index, normalized, or raw. No fake result added. |
| panasonic 24-105 l | no result | [중고] 파나소닉 24-105 L 마운트 | brand_canonicalization_issue | weak_pass | Recall is useful, but brand remains Unknown in normalized/search index while raw stores Other. |
| lumix 24-105 | no result | [중고] 파나소닉 24-105 L 마운트 | brand_canonicalization_issue | weak_pass | Useful Panasonic row recovered; remaining weakness is brand canonicalization. |
| sigma 24-70 l mount | [중고] Sigma 24-70/2.8 (SL 마운트) | [중고] Sigma 24-70/2.8 (SL 마운트) | parser_issue | observation_only | Observation query stays aligned with the recovered Sigma 24-70 SL-mount row. |
| sigma 24-70 dg dn | [중고] Sigma 24-70/2.8 (SL 마운트) | [중고] Sigma 24-70/2.8 (SL 마운트) | parser_issue | observation_only | Observation query stays aligned with the recovered Sigma 24-70 SL-mount row. |
| sigma 24-70 dg dn art | [중고] Sigma 24-70/2.8 (SL 마운트) | [중고] Sigma 24-70/2.8 (SL 마운트) | parser_issue | observation_only | Observation query stays aligned with the recovered Sigma 24-70 SL-mount row. |
| sigma 14-24 l mount | no result | no result | raw_source_coverage_issue | needs_source_or_index_followup | Still no candidate coverage; query remains no-result by policy. |
| sigma 14-24 dg dn | no result | no result | raw_source_coverage_issue | needs_source_or_index_followup | Still no candidate coverage; query remains no-result by policy. |
| sigma 14-24 dg dn art | no result | no result | raw_source_coverage_issue | needs_source_or_index_followup | Still no candidate coverage; query remains no-result by policy. |
| panasonic 24-105 l mount | [중고] 파나소닉 24-105 L 마운트 | [중고] 파나소닉 24-105 L 마운트 | brand_canonicalization_issue | observation_only | Observation query already worked; no new ranking issue found. |
| panasonic lumix 24-105 | no result | [중고] 파나소닉 24-105 L 마운트 | parser_issue | weak_pass | This round added narrow dual-brand parsing so Panasonic+Lumix wording no longer falls through to no structured intent. |
| lumix s 24-105 | [중고] 파나소닉 24-105 L 마운트 | [중고] 파나소닉 24-105 L 마운트 | brand_canonicalization_issue | observation_only | Useful row exists and stays retrievable; brand remains Unknown. |
| lumix 24-105 f4 | no result | [중고] 파나소닉 24-105 L 마운트 | resolver_ranking_issue | weak_pass | This round widened candidate narrowing for spaced focal ranges so the Panasonic 24-105 row survives to scoring. |

## 8. 원인 분류

- `parser_issue`: `sigma 24-70` 계열 recovery 유지, `panasonic lumix 24-105` 신규 복구
- `resolver_ranking_issue`: `lumix 24-105 f4`는 candidate narrowing에서 Panasonic row가 빠지던 문제를 좁게 복구
- `brand_canonicalization_issue`: Panasonic/Lumix 24-105 row는 useful result지만 `brand=Unknown`이 남아 있음
- `raw_source_coverage_issue`: `sigma 14-24` 계열은 source/raw 후보 자체가 없음

## 9. Guardrail 결과

- known third-party pass: `sigma l 30mm`, `sigma 30mm l` 유지
- Leica SL zoom: `sl 24-90`, `sl 14-24`, `sl 16-35`, `sl 90-280` 유지
- Leica L / SL prime: `Leica L 50mm Summicron`, `summicron sl 35`, `Leica 35mm F2 AsphSummicron SL`, `apo summicron sl 35`, `sl 35/50/75/90 summicron`, `35 lux`, `50 lux` 유지
- broad alias: `summicron`, `summilux`, `leica summicron`, `leica summilux`는 Lens-first 유지; `cron`, `lux`는 observation-only 성격 유지
- body: `leica sl2`, `leica sl3`, `leica m10 body`, `leica iiif`, `barnack iiif`, `leica q2` 유지
- accessory: `sl3 battery`, `leica m strap`, `leica hood 12585`, `hood 12549`, `m adapter l` 유지

## 10. 테스트 결과

- 신규 `tests/test_third_party_l_mount_recall.py` 통과
- 기존 search-layer / classifier guardrail 테스트 통과
- `golden_set.py`는 `132/132` 유지

## 11. 남은 위험

- `sigma 14-24` 계열은 여전히 source/index coverage가 없다.
- Panasonic/Lumix 24-105 row는 useful recall이 되지만 `brand=Unknown` 문제는 남아 있다.
- 이번 라운드는 third-party taxonomy 확장이 아니라 recall/ranking 보정 라운드이므로 brand canonicalization은 다음 backlog로 분리하는 것이 안전하다.

## 12. 다음 backlog 후보

- `P3-THIRD-PARTY-BRAND-CANONICALIZATION`
- `P3-R-LENS-QUERY-RECALL`
- `P3-QUERY-RANKING`
- `P3-ACCESSORY-TAXONOMY-COVERAGE`
- `P3-SL-ZOOM-FAMILY-TAXONOMY-AUDIT`
- `P3-CRON-LUX-SHORT-ALIAS-POLICY`

## 13. 상태 분포

- `guardrail_pass`: `33`
- `needs_source_or_index_followup`: `4`
- `observation_only`: `5`
- `pass`: `1`
- `weak_pass`: `4`