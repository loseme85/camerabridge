# P3-ALERT-MVP-QUERY-WATCHLIST

## 1. 작업명
- P3-ALERT-MVP-QUERY-WATCHLIST

## 2. 작업 목적
- MVP alert watchlist에서 어떤 query를 받을지, 어떤 query는 refinement가 필요한지, 어떤 no-result query는 signup alert로 받아야 하는지 contract로 정리

## 3. 구현 요약
- `alert_watchlist_contract.py`에 watchlist enum/dataclass를 추가
- script는 current source planning artifact와 current search endpoint를 읽어 watchlist JSON / validation JSONL / 보고서를 생성
- production search behavior는 변경하지 않음

## 4. watchlist contract 요약
- groups: `['rare_leica_lens', 'rare_leica_body', 'leica_m_classic', 'leica_r_rare', 'leica_sl_modern', 'third_party_l_mount', 'source_gap_alert', 'broad_query_requires_refinement']`
- priorities: `['P0', 'P1', 'P2', 'P3', 'exclude_for_mvp']`
- intents: `['exact_family_alert', 'canonical_family_alert', 'rare_variant_alert', 'source_gap_watch', 'price_drop_watch', 'availability_watch', 'broad_query_refinement_needed']`
- expected_result_behavior: `['should_return_results', 'may_return_results', 'currently_no_result_but_alertable', 'refinement_required', 'exclude_too_broad']`
- trigger_policy: `['new_listing', 'sold_listing_seen', 'price_drop', 'back_in_stock', 'source_gap_resolved', 'manual_review']`
- delivery_readiness: `['ready_for_mvp', 'ready_for_mvp_no_result_signup', 'needs_refinement_ui', 'needs_source_expansion', 'needs_taxonomy_audit', 'needs_price_history', 'exclude_for_now']`

## 5. MVP watchlist group 요약
- total watchlist items: `31`
- included-ish status distribution: `{'include': 24, 'needs_manual_review': 4, 'include_as_source_gap_alert': 1, 'needs_source_expansion': 2}`
- group distribution: `{'rare_leica_lens': 9, 'rare_leica_body': 6, 'leica_r_rare': 4, 'leica_sl_modern': 6, 'source_gap_alert': 1, 'third_party_l_mount': 5}`
- `leica_r_rare` -> item_count=`4` / priority=`{'P0': 1, 'P1': 3}` / status=`{'include': 4}`
- `leica_sl_modern` -> item_count=`6` / priority=`{'P1': 6}` / status=`{'include': 6}`
- `rare_leica_body` -> item_count=`6` / priority=`{'P0': 2, 'P2': 4}` / status=`{'include': 2, 'needs_manual_review': 4}`
- `rare_leica_lens` -> item_count=`9` / priority=`{'P0': 5, 'P1': 4}` / status=`{'include': 9}`
- `source_gap_alert` -> item_count=`1` / priority=`{'P0': 1}` / status=`{'include_as_source_gap_alert': 1}`
- `third_party_l_mount` -> item_count=`5` / priority=`{'P1': 3, 'P2': 2}` / status=`{'include': 3, 'needs_source_expansion': 2}`

## 6. P0/P1 watchlist item 요약
- `Leica Summilux-M 35mm f/1.4 ASPH` -> priority=`P0` / group=`rare_leica_lens` / query=`summilux m 35` / status=`include`
- `Leica Summilux-M 35mm f/1.4 AA` -> priority=`P0` / group=`rare_leica_lens` / query=`35 lux aa` / status=`include`
- `Leica Summilux-M 50mm f/1.4` -> priority=`P0` / group=`rare_leica_lens` / query=`summilux m 50` / status=`include`
- `Leica Noctilux-M 50mm f/0.95 ASPH` -> priority=`P0` / group=`rare_leica_lens` / query=`noctilux m 50 0.95` / status=`include`
- `Leica APO-Summicron-M 90mm f/2 ASPH` -> priority=`P0` / group=`rare_leica_lens` / query=`apo summicron m 90` / status=`include`
- `Leica Summilux-M 75mm f/1.4` -> priority=`P1` / group=`rare_leica_lens` / query=`summilux m 75` / status=`include`
- `Leica Summicron-M 28mm f/2 ASPH` -> priority=`P1` / group=`rare_leica_lens` / query=`summicron m 28` / status=`include`
- `Leica Summilux-M 28mm f/1.4 ASPH` -> priority=`P1` / group=`rare_leica_lens` / query=`summilux m 28` / status=`include`
- `Leica Summilux-M 24mm f/1.4 ASPH` -> priority=`P1` / group=`rare_leica_lens` / query=`summilux m 24` / status=`include`
- `Leica M6` -> priority=`P0` / group=`rare_leica_body` / query=`m6` / status=`include`
- `Leica MP` -> priority=`P0` / group=`rare_leica_body` / query=`mp` / status=`include`
- `Leica APO-Telyt-R 180mm f/3.4` -> priority=`P0` / group=`leica_r_rare` / query=`r 180 apo telyt` / status=`include`
- `Leica APO-Macro-Elmarit-R 100mm f/2.8` -> priority=`P1` / group=`leica_r_rare` / query=`apo macro elmarit r 100` / status=`include`
- `Leica Summicron-R 50mm f/2` -> priority=`P1` / group=`leica_r_rare` / query=`summicron r 50` / status=`include`
- `Leica Vario-Elmarit-R 28-90mm` -> priority=`P1` / group=`leica_r_rare` / query=`vario elmarit r 28-90` / status=`include`
- `Leica APO-Summicron-SL 50mm f/2 ASPH` -> priority=`P1` / group=`leica_sl_modern` / query=`apo summicron sl 50` / status=`include`
- `Leica APO-Summicron-SL 75mm f/2 ASPH` -> priority=`P1` / group=`leica_sl_modern` / query=`apo summicron sl 75` / status=`include`
- `Leica APO-Summicron-SL 90mm f/2 ASPH` -> priority=`P1` / group=`leica_sl_modern` / query=`apo summicron sl 90` / status=`include`
- `Leica Super-Vario-Elmarit-SL 14-24mm f/2.8 ASPH` -> priority=`P1` / group=`leica_sl_modern` / query=`sl 14-24` / status=`include`
- `Leica Vario-Elmarit-SL 24-90mm` -> priority=`P1` / group=`leica_sl_modern` / query=`sl 24-90` / status=`include`
- `Leica APO-Vario-Elmarit-SL 90-280mm` -> priority=`P1` / group=`leica_sl_modern` / query=`sl 90-280` / status=`include`
- `Sigma 14-24mm f/2.8 DG DN Art L-mount` -> priority=`P0` / group=`source_gap_alert` / query=`sigma 14-24 l` / status=`include_as_source_gap_alert`
- `Sigma 24-70mm f/2.8 DG DN Art L-mount` -> priority=`P1` / group=`third_party_l_mount` / query=`sigma 24-70 l` / status=`include`
- `Sigma 30mm f/1.4 DC DN L-mount` -> priority=`P1` / group=`third_party_l_mount` / query=`sigma l 30mm` / status=`include`
- `Panasonic Lumix S 24-105mm f/4` -> priority=`P1` / group=`third_party_l_mount` / query=`lumix 24-105` / status=`include`

## 7. source gap alert item 요약
- `Sigma 14-24mm f/2.8 DG DN Art L-mount` -> query=`sigma 14-24 l` / aliases=`11` / delivery=`ready_for_mvp_no_result_signup` / ui=`source_coverage_gap/no_result_alert_signup`

## 8. rare Leica lens/body alert 요약
- `Leica Summilux-M 35mm f/1.4 ASPH` -> group=`rare_leica_lens` / priority=`P0` / status=`include` / query=`summilux m 35`
- `Leica Summilux-M 35mm f/1.4 AA` -> group=`rare_leica_lens` / priority=`P0` / status=`include` / query=`35 lux aa`
- `Leica Summilux-M 50mm f/1.4` -> group=`rare_leica_lens` / priority=`P0` / status=`include` / query=`summilux m 50`
- `Leica Noctilux-M 50mm f/0.95 ASPH` -> group=`rare_leica_lens` / priority=`P0` / status=`include` / query=`noctilux m 50 0.95`
- `Leica APO-Summicron-M 90mm f/2 ASPH` -> group=`rare_leica_lens` / priority=`P0` / status=`include` / query=`apo summicron m 90`
- `Leica Summilux-M 75mm f/1.4` -> group=`rare_leica_lens` / priority=`P1` / status=`include` / query=`summilux m 75`
- `Leica Summicron-M 28mm f/2 ASPH` -> group=`rare_leica_lens` / priority=`P1` / status=`include` / query=`summicron m 28`
- `Leica Summilux-M 28mm f/1.4 ASPH` -> group=`rare_leica_lens` / priority=`P1` / status=`include` / query=`summilux m 28`
- `Leica Summilux-M 24mm f/1.4 ASPH` -> group=`rare_leica_lens` / priority=`P1` / status=`include` / query=`summilux m 24`
- `Leica M6` -> group=`rare_leica_body` / priority=`P0` / status=`include` / query=`m6`
- `Leica MP` -> group=`rare_leica_body` / priority=`P0` / status=`include` / query=`mp`
- `Leica M-A` -> group=`rare_leica_body` / priority=`P2` / status=`needs_manual_review` / query=`leica m-a`
- `Leica M10 Monochrom` -> group=`rare_leica_body` / priority=`P2` / status=`needs_manual_review` / query=`leica m10 monochrom`
- `Leica M10-R` -> group=`rare_leica_body` / priority=`P2` / status=`needs_manual_review` / query=`leica m10-r`
- `Leica M11 Monochrom` -> group=`rare_leica_body` / priority=`P2` / status=`needs_manual_review` / query=`leica m11 monochrom`
- `Leica APO-Telyt-R 180mm f/3.4` -> group=`leica_r_rare` / priority=`P0` / status=`include` / query=`r 180 apo telyt`
- `Leica APO-Macro-Elmarit-R 100mm f/2.8` -> group=`leica_r_rare` / priority=`P1` / status=`include` / query=`apo macro elmarit r 100`
- `Leica Summicron-R 50mm f/2` -> group=`leica_r_rare` / priority=`P1` / status=`include` / query=`summicron r 50`
- `Leica Vario-Elmarit-R 28-90mm` -> group=`leica_r_rare` / priority=`P1` / status=`include` / query=`vario elmarit r 28-90`

## 9. third-party L-mount alert 요약
- `Sigma 14-24mm f/2.8 DG DN Art L-mount` -> priority=`P0` / status=`include_as_source_gap_alert` / query=`sigma 14-24 l`
- `Sigma 24-70mm f/2.8 DG DN Art L-mount` -> priority=`P1` / status=`include` / query=`sigma 24-70 l`
- `Sigma 30mm f/1.4 DC DN L-mount` -> priority=`P1` / status=`include` / query=`sigma l 30mm`
- `Panasonic Lumix S 24-105mm f/4` -> priority=`P1` / status=`include` / query=`lumix 24-105`
- `Sigma 28-70mm f/2.8 DG DN L-mount` -> priority=`P2` / status=`needs_source_expansion` / query=`sigma 28-70 dg dn l`
- `Sigma 28-105mm f/2.8 DG DN Art L-mount` -> priority=`P2` / status=`needs_source_expansion` / query=`sigma 28-105 dg dn l`

## 10. broad query exclusion/refinement 요약
- `summicron` -> status=`exclude_too_broad` / reason=`Broad family alias; should use refinement chips or canonicalized family watch instead.` / canonical=`summicron m 28 / summicron r 50 / apo summicron sl 50 등 구체 타깃으로 유도`
- `summilux` -> status=`exclude_too_broad` / reason=`Broad family alias; too many mounts and focal lengths.` / canonical=`summilux m 35 / summilux m 50 같은 canonical family alert로 유도`
- `cron` -> status=`refinement_required` / reason=`Collector shorthand only; family selector가 필요함.` / canonical=`Summicron family or mount-specific target`
- `lux` -> status=`refinement_required` / reason=`Collector shorthand only; mount/focal refinement이 필요함.` / canonical=`Summilux-M 35 / 50 등으로 canonicalize`
- `50 cron` -> status=`refinement_required` / reason=`M/R/SL ambiguity가 커서 default watchlist query로는 부적합.` / canonical=`m 50 summicron / r 50 summicron / sl 50 summicron`
- `35 lux` -> status=`refinement_required` / reason=`usable shorthand지만 MVP watchlist는 canonical target과 함께만 제공해야 함.` / canonical=`summilux m 35`
- `50 lux` -> status=`refinement_required` / reason=`usable shorthand지만 MVP watchlist는 canonical target과 함께만 제공해야 함.` / canonical=`summilux m 50`
- `leica r` -> status=`refinement_required` / reason=`R family/focal ambiguity가 커서 family selector가 필요함.` / canonical=`apo telyt r 180 / summicron r 50 / vario elmarit r 28-90`
- `leica cap` -> status=`refinement_required` / reason=`Accessory subtype ambiguity가 커서 default watchlist query로는 너무 넓음.` / canonical=`body cap / lens cap / filter / strap 등으로 세분화`
- `leica lens` -> status=`exclude_too_broad` / reason=`Category-level broad query라 alert target으로 부적합.` / canonical=`family/mount/focal 기반 canonical watch`
- `leica m` -> status=`exclude_too_broad` / reason=`Bodies, lenses, accessories가 섞일 수 있는 broad system query.` / canonical=`m6 / mp / summilux m 35 / summicron m 28 등`
- `leica sl` -> status=`exclude_too_broad` / reason=`SL body와 lens가 함께 섞이는 broad system query.` / canonical=`sl2 / sl3 / sl 24-90 / apo summicron sl 50 등`

## 11. source priority mapping 요약
- `Camera no Naniwa` -> groups=`['leica_sl_modern', 'third_party_l_mount']` / priority_counts=`{'P1': 7}` / watchlist_ids=`['leica_sl_modern_apo_summicron_sl_50', 'leica_sl_modern_apo_summicron_sl_75', 'leica_sl_modern_apo_summicron_sl_90', 'leica_sl_modern_super_vario_elmarit_sl_14_24', 'leica_sl_modern_vario_elmarit_sl_24_90', 'leica_sl_modern_apo_vario_elmarit_sl_90_280']`
- `Ffordes` -> groups=`['rare_leica_lens', 'rare_leica_body', 'leica_r_rare']` / priority_counts=`{'P0': 8, 'P1': 7}` / watchlist_ids=`['rare_leica_lens_summilux_m_35_asph', 'rare_leica_lens_summilux_m_35_aa', 'rare_leica_lens_summilux_m_50', 'rare_leica_lens_noctilux_m_50_095', 'rare_leica_lens_apo_summicron_m_90', 'rare_leica_lens_summilux_m_75']`
- `Ffordes (영국)` -> groups=`['third_party_l_mount']` / priority_counts=`{'P1': 2}` / watchlist_ids=`['third_party_l_mount_sigma_30mm_dc_dn_l', 'third_party_l_mount_lumix_s_24_105_f4']`
- `Fujiya Camera` -> groups=`['rare_leica_lens', 'rare_leica_body', 'leica_r_rare', 'leica_sl_modern', 'source_gap_alert', 'third_party_l_mount']` / priority_counts=`{'P0': 9, 'P1': 14}` / watchlist_ids=`['rare_leica_lens_summilux_m_35_asph', 'rare_leica_lens_summilux_m_35_aa', 'rare_leica_lens_summilux_m_50', 'rare_leica_lens_noctilux_m_50_095', 'rare_leica_lens_apo_summicron_m_90', 'rare_leica_lens_summilux_m_75']`
- `KEH` -> groups=`['leica_sl_modern', 'source_gap_alert', 'third_party_l_mount']` / priority_counts=`{'P1': 7, 'P0': 1}` / watchlist_ids=`['leica_sl_modern_apo_summicron_sl_50', 'leica_sl_modern_apo_summicron_sl_75', 'leica_sl_modern_apo_summicron_sl_90', 'leica_sl_modern_super_vario_elmarit_sl_14_24', 'leica_sl_modern_vario_elmarit_sl_24_90', 'leica_sl_modern_apo_vario_elmarit_sl_90_280']`
- `Kitamura` -> groups=`['leica_sl_modern', 'third_party_l_mount']` / priority_counts=`{'P1': 9}` / watchlist_ids=`['leica_sl_modern_apo_summicron_sl_50', 'leica_sl_modern_apo_summicron_sl_75', 'leica_sl_modern_apo_summicron_sl_90', 'leica_sl_modern_super_vario_elmarit_sl_14_24', 'leica_sl_modern_vario_elmarit_sl_24_90', 'leica_sl_modern_apo_vario_elmarit_sl_90_280']`
- `Leica Store Miami` -> groups=`['rare_leica_lens', 'rare_leica_body', 'leica_r_rare']` / priority_counts=`{'P0': 8, 'P1': 7}` / watchlist_ids=`['rare_leica_lens_summilux_m_35_asph', 'rare_leica_lens_summilux_m_35_aa', 'rare_leica_lens_summilux_m_50', 'rare_leica_lens_noctilux_m_50_095', 'rare_leica_lens_apo_summicron_m_90', 'rare_leica_lens_summilux_m_75']`
- `Lemonsha` -> groups=`['rare_leica_lens', 'rare_leica_body', 'leica_r_rare']` / priority_counts=`{'P0': 8, 'P1': 7}` / watchlist_ids=`['rare_leica_lens_summilux_m_35_asph', 'rare_leica_lens_summilux_m_35_aa', 'rare_leica_lens_summilux_m_50', 'rare_leica_lens_noctilux_m_50_095', 'rare_leica_lens_apo_summicron_m_90', 'rare_leica_lens_summilux_m_75']`
- `MPB UK/EU` -> groups=`['source_gap_alert']` / priority_counts=`{'P0': 1}` / watchlist_ids=`['third_party_l_mount_sigma_14_24_dg_dn_art']`
- `MPB US` -> groups=`['leica_sl_modern', 'source_gap_alert', 'third_party_l_mount']` / priority_counts=`{'P1': 7, 'P0': 1}` / watchlist_ids=`['leica_sl_modern_apo_summicron_sl_50', 'leica_sl_modern_apo_summicron_sl_75', 'leica_sl_modern_apo_summicron_sl_90', 'leica_sl_modern_super_vario_elmarit_sl_14_24', 'leica_sl_modern_vario_elmarit_sl_24_90', 'leica_sl_modern_apo_vario_elmarit_sl_90_280']`
- `Map Camera` -> groups=`['rare_leica_lens', 'rare_leica_body', 'leica_r_rare', 'leica_sl_modern', 'source_gap_alert', 'third_party_l_mount']` / priority_counts=`{'P0': 9, 'P1': 16}` / watchlist_ids=`['rare_leica_lens_summilux_m_35_asph', 'rare_leica_lens_summilux_m_35_aa', 'rare_leica_lens_summilux_m_50', 'rare_leica_lens_noctilux_m_50_095', 'rare_leica_lens_apo_summicron_m_90', 'rare_leica_lens_summilux_m_75']`
- `Meister Camera` -> groups=`['rare_leica_lens', 'rare_leica_body', 'leica_r_rare']` / priority_counts=`{'P0': 8, 'P1': 7}` / watchlist_ids=`['rare_leica_lens_summilux_m_35_asph', 'rare_leica_lens_summilux_m_35_aa', 'rare_leica_lens_summilux_m_50', 'rare_leica_lens_noctilux_m_50_095', 'rare_leica_lens_apo_summicron_m_90', 'rare_leica_lens_summilux_m_75']`
- `Red Dot Cameras` -> groups=`['rare_leica_lens', 'rare_leica_body', 'leica_r_rare']` / priority_counts=`{'P0': 8, 'P1': 7}` / watchlist_ids=`['rare_leica_lens_summilux_m_35_asph', 'rare_leica_lens_summilux_m_35_aa', 'rare_leica_lens_summilux_m_50', 'rare_leica_lens_noctilux_m_50_095', 'rare_leica_lens_apo_summicron_m_90', 'rare_leica_lens_summilux_m_75']`
- `라이카스토어 충무로` -> groups=`['rare_leica_lens', 'rare_leica_body', 'leica_r_rare', 'leica_sl_modern', 'third_party_l_mount']` / priority_counts=`{'P0': 8, 'P1': 16}` / watchlist_ids=`['rare_leica_lens_summilux_m_35_asph', 'rare_leica_lens_summilux_m_35_aa', 'rare_leica_lens_summilux_m_50', 'rare_leica_lens_noctilux_m_50_095', 'rare_leica_lens_apo_summicron_m_90', 'rare_leica_lens_summilux_m_75']`
- `사진집` -> groups=`['leica_sl_modern', 'third_party_l_mount']` / priority_counts=`{'P1': 9}` / watchlist_ids=`['leica_sl_modern_apo_summicron_sl_50', 'leica_sl_modern_apo_summicron_sl_75', 'leica_sl_modern_apo_summicron_sl_90', 'leica_sl_modern_super_vario_elmarit_sl_14_24', 'leica_sl_modern_vario_elmarit_sl_24_90', 'leica_sl_modern_apo_vario_elmarit_sl_90_280']`
- `장씨카메라` -> groups=`['third_party_l_mount']` / priority_counts=`{'P1': 2}` / watchlist_ids=`['third_party_l_mount_sigma_30mm_dc_dn_l', 'third_party_l_mount_lumix_s_24_105_f4']`

## 12. validation 결과
- validation row count: `54`
- behavior_match true: `50` / `54`
- include/source-gap items with fake fill detected: `4`
- `leica m-a` -> count=`3` / top1=`Lens`:`Leica M 50mm f2.8 Elmar Black` / hint=`none`:`no_disambiguation_needed` / status=`needs_manual_review`
- `leica m10 monochrom` -> count=`3` / top1=`Lens`:`Leica M 50mm f2.8 Elmar Black` / hint=`none`:`no_disambiguation_needed` / status=`needs_manual_review`
- `leica m10-r` -> count=`3` / top1=`Lens`:`Leica M 50mm f2.8 Elmar Black` / hint=`none`:`no_disambiguation_needed` / status=`needs_manual_review`
- `leica m11 monochrom` -> count=`3` / top1=`Lens`:`Leica M 50mm f2.8 Elmar Black` / hint=`none`:`no_disambiguation_needed` / status=`needs_manual_review`
- `sigma 28-70 dg dn l` -> count=`0` / top1=``:`` / hint=`none`:`no_disambiguation_needed` / status=`needs_source_expansion`
- `sigma 28-105 dg dn l` -> count=`0` / top1=``:`` / hint=`none`:`no_disambiguation_needed` / status=`needs_source_expansion`

## 13. fake fill 방지 확인
- `sigma 14-24` source-gap watch는 current search에서 no-result + `source_coverage_gap/no_result_alert_signup`이어야 하며, Leica SL 14-24나 Sigma 24-70로 대체되면 안 됨
- 이번 validation에서도 source-gap alias rows는 no-result 유지 여부를 별도로 기록

## 14. 수정 파일 목록
- `alert_watchlist_contract.py`
- `scripts/run_p3_alert_mvp_query_watchlist.py`
- `tests/test_alert_mvp_query_watchlist.py`
- `data/admin/p3_alert_mvp_query_watchlist_v0.md`
- `data/admin/p3_alert_mvp_query_watchlist_v0.jsonl`
- `data/admin/alert_mvp_watchlist_v0.json`

## 15. 수정하지 않은 파일/영역
- production search code
- crawler production code
- output JSON / taxonomy seed / canonical index / raw data / search index

## 16. 테스트 결과
- script run / JSONL validation / watchlist JSON validation / py_compile / golden set recorded separately

## 17. 남은 위험
- `Leica M-A`, `M10 Monochrom`, `M10-R`, `M11 Monochrom` body query는 current search behavior가 아직 launch-safe하지 않음
- `Thambar-M 90`, `APO-Telyt-M 135` 같은 niche M-lens는 taxonomy/query audit 없이는 default MVP watchlist에 넣기 어려움
- third-party L-mount는 `Sigma 14-24` 외 family 확장이 source breadth와 current query behavior에 더 의존함

## 18. 다음 backlog 후보
- `P3-ALERT-MVP-SIGNUP-FLOW`
- `P3-ALERT-MVP-STORAGE-SCHEMA`
- `P3-ALERT-MVP-DELIVERY-SIMULATION`
- `P3-THIRD-PARTY-SOURCE-LIST-EXPANSION-IMPLEMENTATION`
- `P3-SOURCE-CAPABILITY-DASHBOARD`
