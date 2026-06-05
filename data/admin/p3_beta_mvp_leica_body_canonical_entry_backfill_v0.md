# P3-BETA-MVP-LEICA-BODY-CANONICAL-ENTRY-BACKFILL

- decision_status: `leica_body_canonical_entry_backfill_pushed_ready_for_owner_recheck`

## Previous global coverage audit 요약
- The Leica-wide canonical coverage audit found 57 entry_missing_but_results_exist targets, and Leica body lines were the clearest high-priority backfill slice. This round limits itself to body models with query-compatible Body dominance and parser-connected body intent.

## Body backfill 대상과 제외 대상
- active body candidate count: `15`
- hold/manual review count: `18`
- source gap count: `1`

## Schema inspection 결과
- canonical index path: `/Users/changdaepark/Desktop/LEICA SEARCH/data/admin/canonical_entities_index.json`
- new family ids: `leica_m_film_bodies, leica_m_digital_bodies, leica_q_bodies, leica_sl_bodies`
- new body seed row count: `15`
- runtime direct seed references: `[]`
- note: Canonical seed layer is schema-clear and admin-readable. Direct runtime references to canonical seed files are not present in the current search modules inspected in this round.

## 추가한 canonical body entries
- `Leica M3` -> `entities/leica_m_film_bodies.json` / body_intent=`M3` / top=`Body:M3`
- `Leica M4` -> `entities/leica_m_film_bodies.json` / body_intent=`M4` / top=`Body:M4`
- `Leica M5` -> `entities/leica_m_film_bodies.json` / body_intent=`M5` / top=`Body:M5`
- `Leica M6` -> `entities/leica_m_film_bodies.json` / body_intent=`M6` / top=`Body:M6`
- `Leica M6 TTL` -> `entities/leica_m_film_bodies.json` / body_intent=`M6` / top=`Body:M6`
- `Leica MP` -> `entities/leica_m_film_bodies.json` / body_intent=`MP` / top=`Body:MP`
- `Leica M9` -> `entities/leica_m_digital_bodies.json` / body_intent=`M9` / top=`Body:M9`
- `Leica M9-P` -> `entities/leica_m_digital_bodies.json` / body_intent=`M9-P` / top=`Body:M9-P`
- `Leica M10` -> `entities/leica_m_digital_bodies.json` / body_intent=`M10` / top=`Body:M10`
- `Leica M10-R` -> `entities/leica_m_digital_bodies.json` / body_intent=`M10-R` / top=`Body:M10-R`
- `Leica M11` -> `entities/leica_m_digital_bodies.json` / body_intent=`M11` / top=`Body:M11`
- `Leica Q2` -> `entities/leica_q_bodies.json` / body_intent=`Q2` / top=`Body:Q2`
- `Leica Q3` -> `entities/leica_q_bodies.json` / body_intent=`Q3` / top=`Body:Q3`
- `Leica SL2` -> `entities/leica_sl_bodies.json` / body_intent=`SL2` / top=`Body:SL2`
- `Leica SL3` -> `entities/leica_sl_bodies.json` / body_intent=`SL3` / top=`Body:SL3`

## Already existing entries
- none

## Hold / manual review entries
- `Leica M2`: Top result is still Lens and safe Body dominance is not confirmed.
- `Leica M4-2`: Body parser does not currently connect Leica M4-2 safely.
- `Leica M4-P`: Body parser does not currently connect Leica M4-P safely.
- `Leica M-A`: Body parser does not currently connect Leica M-A safely.
- `Leica M8`: Leica M8 currently falls back to broad Leica Lens results.
- `Leica M8.2`: Leica M8.2 currently falls back to broad Leica Lens results.
- `Leica M Typ 240`: Typ 240 queries are not yet body-safe in parser/ranking.
- `Leica M Typ 262`: Typ 262 queries are not yet body-safe in parser/ranking.
- `Leica M10-P`: Leica M10-P currently collapses into broad Leica Lens fallback.
- `Leica M10 Monochrom`: Query resolves to M10 body line but not yet exact-enough to seed as a separate active body entry.
- `Leica M11-P`: Leica M11-P is not yet parser-connected as an exact body query.
- `Leica M11 Monochrom`: Leica M11 Monochrom still collapses to base M11 body intent rather than an exact canonical body row.
- `Leica Q`: Leica Q still falls into accessory-led results and is not ready for active seed promotion.
- `Leica Q2 Monochrom`: Leica Q2 Monochrom currently resolves into base Q2 body intent rather than an exact canonical body row.
- `Leica Q3 43`: Leica Q3 43 still resolves to base Q3 body intent and remains safer as a hold candidate.
- `Leica SL2-S`: Leica SL2-S still collapses to base SL2 body intent rather than an exact canonical body row.
- `Leica M1`: Owner requested M1 stay out of this active backfill round.
- `Leica M7`: Owner requested M7 stay out of this active backfill round.

## Source gap entries
- `Leica M-P Typ 240`: Observed source coverage is insufficient for safe active seed promotion.

## Smoke query 결과
- `Leica M2`: body_intent=`M2`, market=`False`, price=`False`, top=`Lens:None`, top3=`['Lens', 'Lens', 'Lens']`
- `M2`: body_intent=`M2`, market=`False`, price=`False`, top=`Lens:None`, top3=`['Lens', 'Lens', 'Lens']`
- `Leica M3`: body_intent=`M3`, market=`True`, price=`True`, top=`Body:M3`, top3=`['Body', 'Body', 'Body']`
- `M3`: body_intent=`M3`, market=`True`, price=`True`, top=`Body:M3`, top3=`['Body', 'Body', 'Body']`
- `Leica M4`: body_intent=`M4`, market=`True`, price=`True`, top=`Body:M4`, top3=`['Body', 'Body', 'Body']`
- `Leica M5`: body_intent=`M5`, market=`True`, price=`True`, top=`Body:M5`, top3=`['Body', 'Body', 'Body']`
- `Leica M6`: body_intent=`M6`, market=`True`, price=`True`, top=`Body:M6`, top3=`['Body', 'Body', 'Body']`
- `M6`: body_intent=`M6`, market=`True`, price=`True`, top=`Body:M6`, top3=`['Body', 'Body', 'Body']`
- `Leica MP`: body_intent=`MP`, market=`True`, price=`True`, top=`Body:MP`, top3=`['Body', 'Body', 'Body']`
- `MP silver`: body_intent=`MP`, market=`True`, price=`True`, top=`Body:MP`, top3=`['Body', 'Body', 'Body']`
- `Leica M9`: body_intent=`M9`, market=`True`, price=`True`, top=`Body:M9`, top3=`['Body', 'Body', 'Body']`
- `Leica M10`: body_intent=`M10`, market=`True`, price=`True`, top=`Body:M10`, top3=`['Body', 'Body', 'Body']`
- `Leica M10-R`: body_intent=`M10-R`, market=`True`, price=`True`, top=`Body:M10-R`, top3=`['Body', 'Body', 'Body']`
- `Leica M11`: body_intent=`M11`, market=`True`, price=`True`, top=`Body:M11`, top3=`['Body', 'Body', 'Body']`
- `Leica Q2`: body_intent=`Q2`, market=`True`, price=`True`, top=`Body:Q2`, top3=`['Body', 'Body', 'Body']`
- `Leica Q3`: body_intent=`Q3`, market=`True`, price=`True`, top=`Body:Q3`, top3=`['Body', 'Body', 'Body']`
- `q3 28`: body_intent=`Q3`, market=`True`, price=`True`, top=`Body:Q3`, top3=`['Body', 'Body', 'Body']`
- `Leica SL2`: body_intent=`SL2`, market=`True`, price=`True`, top=`Body:SL2`, top3=`['Body', 'Body', 'Body']`
- `Leica SL3`: body_intent=`SL3`, market=`True`, price=`True`, top=`Body:SL3`, top3=`['Body', 'Body', 'Body']`
- `Leica M1`: body_intent=`None`, market=`False`, price=`False`, top=`Lens:Elmar`, top3=`['Lens', 'Lens', 'Lens']`
- `Leica M7`: body_intent=`None`, market=`False`, price=`False`, top=`Lens:Elmar`, top3=`['Lens', 'Lens', 'Lens']`

## Market entry / price summary gate 유지 여부
- Maintained. Canonical body backfill does not bypass the existing query-confidence gate; market entry and price summary still follow query-compatible Body evidence only.

## Body / lens regression 결과
- `M50/1.2`: top=`Lens:Noctilux`, market=`False`, compact_lens=`False`, stale_body=`False`
- `Leica M50/1.2 1세대`: top=`Lens:Noctilux`, market=`False`, compact_lens=`False`, stale_body=`False`
- `ltm summaron 35`: top=`Lens:Summaron`, market=`True`, compact_lens=`False`, stale_body=`False`
- `35 lux aa`: top=`Lens:Summilux-M`, market=`True`, compact_lens=`False`, stale_body=`False`
- `summicron`: top=`Lens:Summicron`, market=`False`, compact_lens=`False`, stale_body=`False`
- `ricoh gr iiix`: top=`None:None`, market=`False`, compact_lens=`False`, stale_body=`False`
- `hasselblad xpan`: top=`None:None`, market=`False`, compact_lens=`False`, stale_body=`False`

## Git diff 요약
- data/.DS_Store | Bin 6148 -> 6148 bytes
-  1 file changed, 0 insertions(+), 0 deletions(-)

## Commit / push 수행 여부
- commit_executed = `True`
- push_executed = `True`
- commit_hash = `b2a4c0150b2dce2823ccd654a91a388a0b47e69d`
- preview_deployment_url = `https://camerabridge-nk0e7mngd-camerabridge.vercel.app`

## Production / public / access guard
- `production_launch_go` = `False`
- `production_alias_connect_allowed` = `False`
- `public_unrestricted_access_enabled` = `False`
- `external_tester_access_enabled` = `False`
- `invite_sent_count` = `0`
- `provider_send_count` = `0`
- `webhook_call_count` = `0`
- `production_DB_write_count` = `0`
- `access_activation_performed` = `False`
- `main_direct_push_executed` = `False`
- `production_promote_executed` = `False`
- `tester_link_send_allowed` = `False`
- `raw_identity_recorded` = `False`
- `raw_contact_recorded` = `False`
- `external_link_sent` = `False`
- `fake_fill_added` = `False`

## 테스트 결과
- Body seed files use the same family schema as existing admin seed files.
- Only parser-connected, top-Body-dominant Leica body lines were promoted to active seed rows.
- Compact lens notation regressions remain blocked separately and must not reclassify M50/1.2 as M5 Body.

## Production alias 연결 가능 여부
- `production_alias_connect_allowed = False`

## 다음 backlog 후보
- P3-BETA-MVP-LEICA-BODY-CANONICAL-ENTRY-OWNER-RECHECK
- P3-BETA-MVP-LEICA-COMPACT-PNS-CANONICAL-ENTRY-BACKFILL
- P3-BETA-MVP-QUERY-PARSER-UNKNOWN-TOKEN-COVERAGE-FIXUP
- P3-BETA-MVP-LEICA-LENS-CANONICAL-ENTRY-COVERAGE-FOLLOWUP
