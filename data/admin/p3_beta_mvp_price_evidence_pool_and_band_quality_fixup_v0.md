# P3-BETA-MVP-PRICE-EVIDENCE-POOL-AND-BAND-QUALITY-FIXUP

- decision_status: `price_evidence_pool_band_quality_fixup_passed_ready_for_owner_approved_push`
- preview_deployment_url: `None`

## Price Evidence Pool
- exact_variant_pool / exact_base_model_pool / broader_family_pool / excluded_pool are separated before band calculation.
- noisy or incompatible prices are removed before price band rendering.

## Noctilux E60
- `price_summary_allowed`: `False`
- `price_scope_label`: `Exact variant price data limited`
- `broader_reference_band`: `KRW 5,900,000 - 8,880,000`
- `broader_reference_quality_state`: `clean_exact_base_model_band`
- `unlock_requirements`: `Need 2+ exact variant priced listings.`

## Summilux 50 3rd Generation
- `price_summary_allowed`: `False`
- `price_scope_label`: `Exact variant price data limited`
- `broader_reference_band`: `KRW 2,500,000 - 6,150,000`

## 35 lux aa
- `price_summary_allowed`: `False`
- `broader_reference_allowed`: `True`
- `broader_reference_locked_reason`: `None`

## Exact Variant Stable
- `Summicron 35 8-element` -> allowed=True / band=KRW 2,970,000 - 8,600,000 / excluded=3
- `Summicron 50 rigid` -> allowed=True / band=KRW 2,400,000 - 3,500,000 / excluded=4
- `Leica M50/1.2 1세대` -> allowed=True / band=KRW 43,000,000 - 53,000,000 / excluded=0

