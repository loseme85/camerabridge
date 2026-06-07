# P3-BETA-MVP-LENS-PRICE-SCOPE-SEARCH-CONFIDENCE-ALIGNMENT-FIXUP

- decision_status: `lens_price_scope_search_confidence_alignment_fixup_passed_ready_for_owner_approved_push`
- owner_recheck_hold_reason: Summilux-M 50 ASPH exposed exact variant price while visible search results stayed weak-only and third-party-dominated.
- preview_deployment_url: `None`

## Search Confidence Mismatch
- `Summilux-M 50 ASPH` -> allowed=False / scope=blocked_weak_only / search_confidence=weak_only_fallback / top=third_party_top_domination

## Exact Variant Ready
- `Summicron 35 8-element` -> allowed=True / scope=exact_variant / top=exact_variant_strong
- `Summicron 50 rigid` -> allowed=True / scope=exact_variant / top=exact_variant_strong

## Exact Variant Data Limited
- `Leica Summilux-M 50mm f1.4 3세대` -> label=Exact variant price data limited / broader_reference=True
- `Summilux 50 3rd generation` -> label=Exact variant price data limited / broader_reference=True
- `35 lux aa` -> label=Price summary locked / broader_reference=True
- `Noctilux 50 f1 E60` -> label=Exact variant price data limited / broader_reference=True
