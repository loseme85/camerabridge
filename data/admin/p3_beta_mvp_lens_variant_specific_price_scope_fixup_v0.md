# P3-BETA-MVP-LENS-VARIANT-SPECIFIC-PRICE-SCOPE-FIXUP

- decision_status: `lens_variant_specific_price_scope_fixup_passed_ready_for_owner_approved_push`
- previous audit: `lens_variant_specific_price_scope_policy_audit_completed_ready_for_fixup`
- preview_deployment_url: `None`
- preview_deployment_state: `None`
- preview_commit: `None`

## Exact Variant Ready
- `Summilux-M 50 ASPH` -> `Exact variant price` / allowed=True / band=KRW 3,650,000 - 5,000,000
- `Summicron 35 8-element` -> `Exact variant price` / allowed=True / band=KRW 2,970,000 - 7,580,000
- `Summicron 50 rigid` -> `Exact variant price` / allowed=True / band=KRW 1,500,000 - 4,230,000

## Exact Variant Data Limited
- `Leica Summilux-M 50mm f1.4 3세대` -> `Exact variant price data limited` / broader_reference=True / band=KRW 2,700,000 - 5,500,000
- `Summilux 50 3rd generation` -> `Exact variant price data limited` / broader_reference=True / band=KRW 2,700,000 - 5,500,000
- `Summilux-M 50 pre-ASPH` -> `Exact variant price data limited` / broader_reference=True / band=KRW 2,200,000 - 5,500,000
- `35 lux aa` -> `Exact variant price data limited` / broader_reference=True / band=KRW 25,300,000 - 33,800,000
- `Noctilux 50 f1 E60` -> `Exact variant price data limited` / broader_reference=True / band=KRW 990,000 - 53,000,000

## Broader Family Reference
- `Noctilux 50 0.95` -> `Broader family reference` / broader_reference=True
- `Summaron 35 2.8` -> `Broader family reference` / broader_reference=True

## Boundary Conflict
- `Summicron-M 35 ASPH` -> `Price summary locked` / allowed=False
- `APO-Summicron-SL 90` -> `Price summary locked` / allowed=False

## Body/Lens Regression
- `ltm summaron 35` -> display_category=Lens / price_scope=exact_base_model
- `Elmarit-R 28` -> display_category=Lens / price_scope=exact_base_model
- `M50/1.2` -> display_category=Lens / price_scope=broader_model_family
- `Leica M9` -> display_category=Body / price_scope=exact_base_model
- `Leica M10` -> display_category=Body / price_scope=exact_base_model
- `Leica M11` -> display_category=Body / price_scope=exact_base_model
