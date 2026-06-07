# P3-BETA-MVP-PRICE-BAND-RUNTIME-PROJECTION-AND-QUERY-RESULT-VISIBILITY-FIXUP

- decision_status: `price_band_runtime_projection_query_result_visibility_fixup_passed_ready_for_owner_approved_push`
- preview_deployment_url: `None`

## Owner Recheck Hold
- runtime price band projection and UI display were not reliably aligned before this fix.
- query/result evidence needed to be visible in one place for owner review.

## 35 lux aa
- `display_price_summary_allowed`: `False`
- `display_broader_reference_allowed`: `True`
- `display_broader_reference_label`: `Exact base model reference`
- `display_broader_reference_band`: `KRW 3,380,000 - 8,200,000`
- `broader_reference_quality_state`: `clean_exact_base_model_band`

## Noctilux 50 f1 E60
- `display_price_band`: `Exact variant price data limited`
- `display_broader_reference_band`: `KRW 5,900,000 - 8,880,000`
- `display_match_state_message`: `Exact or strong compatible listings are visible.`

## Summicron 50 rigid
- `display_price_band`: `KRW 2,400,000 - 3,500,000`
- `price_summary_band`: `KRW 2,400,000 - 3,500,000`
- `display_top_result_evidence_count`: `5`

## Verdict
- disallowed broader reference visible: `[]`
- band projection mismatch: `[]`
- query result panel missing: `[]`
- dev token visible: `[]`

