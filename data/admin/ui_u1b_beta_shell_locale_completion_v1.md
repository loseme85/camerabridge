# UI-U1B Beta Shell Locale Completion v1

## Root / Branch / HEAD
- root: `/Users/changdaepark/Desktop/LEICA SEARCH`
- branch: `p4-entry-generation-narrowing-beta`
- HEAD: `8ea984b9e70de4276b623d91f72ce0e599b8417f`

## Decision
- recommendation: `READY_FOR_OWNER_UI_SMOKE`
- production: untouched
- commit / push / merge / deploy: not performed

## Scope Lock
This round only completed beta-shell locale coverage and user-facing copy cleanup.

Modified in U1B:
- `app/templates/beta.html`
- `beta.html`
- `tests/test_search_ui.py`
- `data/admin/ui_u1b_beta_shell_locale_completion_v1.md`

Not modified in U1B:
- `search_response.py`
- `api/search.py`
- `search_service.py`
- parser / resolver / ranking
- pricing / evidence eligibility
- crawler / catalog / workflow
- `app/templates/index.html`
- `index.html`

## Full Dirty File Inventory
Current `git status --short` at report time:

```text
 M app/templates/beta.html
 M app/templates/index.html
 M beta.html
 M crawler/sessions/crawl_sessions.json
 M data/.DS_Store
 M data/admin/.DS_Store
 M data/admin/beta_mvp_result_card_runtime_normalization_projection_fixup_v0.json
 M data/admin/body_price_band_quality_fixup_v0.json
 M data/admin/lens_boundary_conflict_resolution_fixup_v0.json
 M data/admin/lens_price_scope_search_confidence_alignment_fixup_v0.json
 M data/admin/lens_variant_specific_price_scope_fixup_v0.json
 M data/admin/lens_variant_token_parser_coverage_fixup_v0.json
 M data/admin/model_market_entry_ui_copy_projection_fixup_v0.json
 M data/admin/p3_beta_mvp_body_price_band_quality_fixup_v0.jsonl
 M data/admin/p3_beta_mvp_lens_boundary_conflict_resolution_fixup_v0.jsonl
 M data/admin/p3_beta_mvp_lens_boundary_conflict_resolution_fixup_v0.md
 M data/admin/p3_beta_mvp_lens_price_scope_search_confidence_alignment_fixup_v0.jsonl
 M data/admin/p3_beta_mvp_lens_variant_specific_price_scope_fixup_v0.jsonl
 M data/admin/p3_beta_mvp_lens_variant_token_parser_coverage_fixup_v0.jsonl
 M data/admin/p3_beta_mvp_lens_variant_token_parser_coverage_fixup_v0.md
 M data/admin/p3_beta_mvp_model_market_entry_ui_copy_projection_fixup_v0.jsonl
 M data/admin/p3_beta_mvp_model_market_entry_ui_copy_projection_fixup_v0.md
 M data/admin/p3_beta_mvp_price_band_runtime_projection_and_query_result_visibility_fixup_v0.jsonl
 M data/admin/p3_beta_mvp_price_evidence_pool_and_band_quality_fixup_v0.jsonl
 M data/admin/p3_beta_mvp_query_review_evidence_ui_copy_button_and_unlock_copy_fixup_v0.jsonl
 M data/admin/p3_beta_mvp_query_review_evidence_ui_copy_button_and_unlock_copy_fixup_v0.md
 M data/admin/p3_beta_mvp_query_review_evidence_ui_polish_fixup_v0.jsonl
 M data/admin/p3_beta_mvp_query_review_evidence_ui_polish_fixup_v0.md
 M data/admin/p3_beta_mvp_query_review_evidence_ui_polish_followup_v0.jsonl
 M data/admin/p3_beta_mvp_query_review_evidence_ui_polish_followup_v0.md
 M data/admin/p3_beta_mvp_result_card_runtime_normalization_projection_fixup_v0.jsonl
 M data/admin/p3_beta_mvp_result_card_runtime_normalization_projection_fixup_v0.md
 M data/admin/p4_entry_generation_narrowing_beta_v1.md
 M data/admin/price_band_runtime_projection_and_query_result_visibility_fixup_v0.json
 M data/admin/price_evidence_pool_and_band_quality_fixup_v0.json
 M data/admin/query_review_evidence_ui_copy_button_and_unlock_copy_fixup_v0.json
 M data/admin/query_review_evidence_ui_polish_fixup_v0.json
 M data/admin/query_review_evidence_ui_polish_followup_v0.json
 M data/derived/flags_latest.json
 M data/derived/qa_report_latest.json
 M data/derived/sold_quality_latest.json
 D data/normalized/normalized_20260602_215813.json
 D data/normalized/normalized_20260603_163914.json
 D data/raw/raw_20260531_180030.json
 D data/raw/raw_20260531_201151.json
 D data/raw/raw_20260601_173123.json
 D data/raw/raw_20260601_173124.json
 M data/status.json
 M index.html
 M search_response.py
 M tests/test_search_response.py
 M tests/test_search_ui.py
?? data/admin/leica_global_canonical_entry_coverage_audit_v0.json
?? data/admin/lens_variant_specific_price_scope_policy_audit_v0.json
?? data/admin/lens_variant_token_parser_coverage_audit_v0.json
?? data/admin/locked_entry_and_price_unlock_audit_v0.json
?? data/admin/p3_beta_mvp_accessory_bundle_body_lens_contamination_audit_v1.md
?? data/admin/p3_beta_mvp_apo_summicron_sl_implicit_asph_focal_coverage_audit_v0.md
?? data/admin/p3_beta_mvp_apo_token_family_intent_audit_v0.md
?? data/admin/p3_beta_mvp_body_lens_category_separation_latest_preview_validation_passed_v0.md
?? data/admin/p3_beta_mvp_boundary_regression_smoke_v1.md
?? data/admin/p3_beta_mvp_boundary_smoke_set_audit_v0.md
?? data/admin/p3_beta_mvp_data_freshness_hold_recheck_v1.md
?? data/admin/p3_beta_mvp_exact_evidence_role_consistency_audit_v0.md
?? data/admin/p3_beta_mvp_exact_sample_pool_and_duplicate_policy_audit_v0.md
?? data/admin/p3_beta_mvp_final_safety_smoke_audit_v1.md
?? data/admin/p3_beta_mvp_final_safety_smoke_closure_note_v1.md
?? data/admin/p3_beta_mvp_implicit_asph_exactness_audit_v0.md
?? data/admin/p3_beta_mvp_latest_preview_search_regression_smoke_v0.md
?? data/admin/p3_beta_mvp_leica_12585_12504_catalog_accessory_intent_audit_v1.md
?? data/admin/p3_beta_mvp_leica_global_canonical_entry_coverage_audit_v0.jsonl
?? data/admin/p3_beta_mvp_leica_global_canonical_entry_coverage_audit_v0.md
?? data/admin/p3_beta_mvp_leica_m_token_mount_intent_audit_v0.md
?? data/admin/p3_beta_mvp_lens_variant_specific_price_scope_policy_audit_v0.jsonl
?? data/admin/p3_beta_mvp_lens_variant_specific_price_scope_policy_audit_v0.md
?? data/admin/p3_beta_mvp_lens_variant_token_parser_coverage_audit_v0.jsonl
?? data/admin/p3_beta_mvp_lens_variant_token_parser_coverage_audit_v0.md
?? data/admin/p3_beta_mvp_limited_beta_owner_pack_v1.md
?? data/admin/p3_beta_mvp_locked_entry_and_price_unlock_audit_v0.jsonl
?? data/admin/p3_beta_mvp_locked_entry_and_price_unlock_audit_v0.md
?? data/admin/p3_beta_mvp_m10_accessory_noise_first_screen_audit_v1.md
?? data/admin/p3_beta_mvp_m35_summicron_asph_evidence_role_conflict_audit_v0.md
?? data/admin/p3_beta_mvp_match_confidence_and_market_entry_gate_audit_v0.md
?? data/admin/p3_beta_mvp_owner_pack_final_recheck_v1.md
?? data/admin/p3_beta_mvp_product_trust_audit_v1.md
?? data/admin/p3_beta_mvp_result_card_classification_explanation_ui_micro_audit_v0.md
?? data/admin/p3_beta_mvp_summicron_50_dr_dual_range_boundary_audit_v0.md
?? data/admin/p3_beta_mvp_summicron_50_hood_ranking_polish_audit_v1.md
?? data/admin/p3_beta_mvp_summicron_50_rigid_mount_guard_audit_v0.md
?? data/admin/p3_beta_mvp_summilux_35_2mae_latest_preview_owner_recheck_passed_v0.md
?? data/admin/p3_beta_mvp_summilux_35_2mae_owner_recheck_failed_ui_evidence_v0.md
?? data/admin/p3_beta_mvp_summilux_35_2mae_owner_recheck_packet_v0.md
?? data/admin/p3_beta_mvp_summilux_35_2mae_preview_runtime_mismatch_audit_v0.md
?? data/admin/p3_beta_mvp_summilux_35_aa_exactness_recognition_audit_v0.md
?? data/admin/p3_beta_mvp_summilux_35_asph_fle_contamination_audit_v0.md
?? data/admin/p3_beta_mvp_summilux_35_aspherical_aa_alias_audit_v0.md
?? data/admin/p3_beta_mvp_summilux_35_fle2_row_level_evidence_consistency_audit_v1.md
?? data/admin/p3_beta_mvp_summilux_35_fle_fle2_boundary_audit_v0.md
?? data/admin/p3_beta_mvp_summilux_35_fle_fle2_boundary_confidence_audit_v0.md
?? data/admin/p3_beta_mvp_summilux_35_fle_fle2_ranking_confidence_latest_preview_validation_passed_v0.md
?? data/admin/p3_beta_mvp_summilux_35_steel_rim_reissue_intent_audit_v0.md
?? data/admin/p3_existing_crawler_pagination_reuse_audit_v1.md
?? data/admin/p3_kamerastore_preview_guard_verification_v1.md
?? data/admin/p3_link_survival_audit_v1.md
?? data/admin/p3_link_survival_sample_v1.json
?? data/admin/p3_live_crawl_to_beta_regression_v1.md
?? data/admin/p3_live_normalized_to_runtime_reconnect_v1.md
?? data/admin/p3_m11p_body_entry_fix_v1.md
?? data/admin/p3_preview_latest_index_deploy_fix_v1.md
?? data/admin/p3_source_registry_v1.md
?? data/admin/p4_clean_production_merge_candidate_v1.md
?? data/admin/p4_production_merge_review_v1.md
?? data/admin/p5a_catalog_schema_bridge_plan_v1.md
?? data/admin/p5b_reference_entry_catalog_seed_v1.md
?? data/admin/p5c_reference_entry_catalog_audit_plan_v1.md
?? data/admin/p5d_leica_universe_catalog_production_workflow_v1.md
?? data/admin/p5e1_leica_m6_family_audit_packet_v1.md
?? data/admin/p5e1_leica_m6_family_candidate_inventory_v1.md
?? data/admin/p5e1r1_leica_m6_family_audit_packet_v1.md
?? data/admin/p5e1r1_leica_m6_family_candidate_inventory_v1.md
?? data/admin/p5e2_leica_m6_collector_proof_packet_v1.md
?? data/admin/p5e2_leica_m6_collector_source_ledger_v1.md
?? data/admin/p5e3_leica_m6_draft_catalog_update_proposal_v1.md
?? data/admin/reference_catalog_merge_plan_v1.md
?? data/admin/ui_u1a_active_asking_first_safety_locale_review_v1.md
?? data/config/reference_entry_catalog_v1.json
?? data/normalized/normalized_20260630_235217.json
?? data/normalized/normalized_20260630_235809.json
?? data/raw/raw_20260630_235216.json
?? data/raw/raw_20260630_235217.json
?? data/raw/raw_20260630_235808.json
?? data/raw/raw_20260630_235809.json
?? scripts/run_p3_beta_mvp_leica_global_canonical_entry_coverage_audit.py
?? scripts/run_p3_beta_mvp_lens_variant_specific_price_scope_policy_audit.py
?? scripts/run_p3_beta_mvp_lens_variant_token_parser_coverage_audit.py
?? scripts/run_p3_beta_mvp_locked_entry_and_price_unlock_audit.py
?? scripts/run_p3_beta_mvp_product_trust_audit_v1.py
?? tests/test_beta_mvp_leica_global_canonical_entry_coverage_audit.py
?? tests/test_beta_mvp_lens_variant_specific_price_scope_policy_audit.py
?? tests/test_beta_mvp_lens_variant_token_parser_coverage_audit.py
?? tests/test_beta_mvp_locked_entry_and_price_unlock_audit.py
?? tmp_kamerastore_link_checks_v1.tsv
?? tmp_kamerastore_url_sample_v1.json
?? tmp_kamerastore_url_sample_v1.tsv
```

## U1B Changes
### Translated shell strings
- top bar beta pills
- hero eyebrow / title / subtitle / notices
- beta search panel labels, placeholder, button, ARIA labels
- hero sidebar labels and bullets
- overview cards
- filter labels and dynamic option labels
- sticky search ARIA / placeholder / button label
- workspace-side beta note / how-to-read / safety note
- pagination buttons
- query summary labels
- query review panel labels
- state cards: loading / error / intro / no-result / broad-query / source-gap
- market entry summary labels
- result-card labels:
  - interpreted entry
  - search match
  - used for price
  - exclusion reason
  - generation confidence
  - mount
  - status
  - price role
- details / explanation rows
- load-more button
- warning/footer helper copy
- copy-to-clipboard completion text
- debug index prefix line

### Preserved data strings
The following remain unmodified across locale switching:
- Leica product names
- listing titles
- source / seller names
- original currency and prices
- listing URLs
- article / catalog numbers
- model identifiers

### Intentionally fixed-language strings
- `CAMERA BRIDGE` wordmark
- Leica / Summicron / Summilux / M6 / M10 / FLE2 / DR etc. product-family identifiers
- temporary debug metadata field token `generated_at`

### Hidden / normalized internal terms
- raw `quality.display_message` is no longer surfaced directly in beta footer copy
- raw `query_match_label` no longer leaks directly into the visible “Search match” data point
- boundary / compatibility copy is normalized through beta-facing labels and reasons

## Translation Architecture
- reused existing `UX_LOCALE_COPY` dictionary and `ux(...)` accessor
- did not add a separate i18n system
- reused existing locale storage key: `cb.beta.locale`
- added static-shell translation hooks through:
  - `data-i18n`
  - `data-i18n-placeholder`
  - `data-i18n-aria-label`
- `setLocale(...)` behavior remains:
  - no `runSearch(...)`
  - no `fetch(...)`
  - preserves scroll
  - re-renders current state only

## Locale Switching Behavior
Verified contract:
- current query preserved
- current result set preserved
- current order preserved
- active/history section membership preserved
- selected sort preserved
- prices preserved
- titles preserved
- URLs preserved
- scroll preserved

## String Leakage Audit
### KO state
Verified on `/beta` local smoke:
- visible shell labels render in Korean:
  - `검색`
  - `정렬`
  - `검색어`
  - `검색한 모델`
  - `현재 판매 중`
  - `과거 거래 / 가격 기록`
  - `검색 결과 안내`
  - `안전 안내`

### EN state
Verified on `/beta` local smoke:
- visible shell labels render in English:
  - `Search`
  - `Sort`
  - `Search query`
  - `Interpreted as`
  - `Active listings`
  - `Market history`
  - `How to read results`
  - `Safety note`

### Allowed visible proper nouns
- Leica product names
- listing titles
- source/store names
- `CAMERA BRIDGE`

## Smoke Test Results
Local beta route used:
- `http://127.0.0.1:5001/beta`

### A. `Leica M6`
- KO:
  - `검색한 모델: Leica M6`
  - active/history labels localized
  - sort kept as `최신순`
- EN:
  - `Interpreted as: Leica M6`
  - `Active listings` / `Market history`
  - sort kept as `Newest`
- KO back:
  - query/result/order/price/sort preserved

### B. `Summilux-M 35 FLE2`
- KO:
  - `검색한 모델: Leica 35mm Summilux-M FLE`
  - `정확 조건 기준 가격을 계산했어요.`
- EN:
  - `Interpreted as: Leica 35mm Summilux-M FLE`
  - `An exact-condition price was calculated.`
- KO back:
  - localized shell restored, titles unchanged

### C. `50 cron dr`
- KO:
  - `검색한 모델: Leica 50mm Summicron-M Dual Range`
- EN:
  - `Interpreted as: Leica 50mm Summicron-M Dual Range`
- KO back:
  - query/results/order preserved

### D. `Leica M10 lens kit`
- KO:
  - `검색한 모델: Leica M10`
  - top visible listing title preserved as source data
- EN:
  - same result identity retained
  - shell strings translated
- KO back:
  - locale swap restored without result change

### E. `zzzz nonexistent model`
- KO:
  - localized empty-state title/body shown
- EN:
  - `Not enough verifiable matches were found.`
  - `Try adding details such as the model, mount, or focal length.`
- KO back:
  - empty-state localized back to Korean

## API Re-request Check
Validated locally with live Flask server log:

Observed log sequence for five submitted searches:
- exactly one `GET /api/search?...` per committed search
- no extra `/api/search` line appeared during locale-only toggles

Representative confirmed example:
- `Leica M6` search produced one `/api/search?q=Leica+M6&limit=12&offset=0`
- subsequent KO -> EN -> KO locale changes produced no new `/api/search` lines

## Automated Test Results
Executed:

```bash
python3 -m py_compile api/search.py search_service.py search_response.py app/app.py
python3 tests/test_search_ui.py
python3 tests/test_search_response.py
```

Results:
- `py_compile`: PASS
- `tests/test_search_ui.py`: PASS
- `tests/test_search_response.py`: PASS

## Mirror Validation
Validated:

```bash
cmp -s app/templates/beta.html beta.html && echo beta_sync:ok
```

Result:
- `beta_sync:ok`

## Remaining Untranslated Strings
No remaining mixed KO/EN shell leakage was observed in the tested beta route.

Known intentional non-translated content:
- product/listing/source data
- brand/proper nouns
- temporary debug metadata token `generated_at`

Broader non-KO/EN locales:
- new shell-completion keys currently guarantee full KO/EN coverage
- other supported locales continue to fall back to English where no dedicated translation was added in this round

## Unrelated Dirty Files Untouched
All pre-existing dirty files outside:
- `app/templates/beta.html`
- `beta.html`
- `tests/test_search_ui.py`
- this report

were intentionally left untouched.

## Recommendation
- status: `READY_FOR_OWNER_UI_SMOKE`

Why:
- active-asking-first behavior preserved
- client-side sort preservation preserved
- locale switch preserves query/results/order/price/scroll
- no locale-triggered API refetch observed
- beta shell KO/EN strings completed
- automated tests pass
- production untouched
