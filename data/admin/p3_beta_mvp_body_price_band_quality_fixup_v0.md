# P3-BETA-MVP-BODY-PRICE-BAND-QUALITY-FIXUP

## 1. 작업명
- `P3-BETA-MVP-BODY-PRICE-BAND-QUALITY-FIXUP`

## 2. exact body price quality rules added
- Accessory-like body titles are excluded from body price evidence even if a stale normalized row still says Body.
- Adjacent body variants and special editions such as Monochrom / Reporter / Safari / Leitz Wetzlar / limited editions are excluded from generic base-body pricing as variant boundary rows unless the query explicitly asks for them.
- Body base-model price now respects the same cleaned-band quality gate before it can open.

## 3. Leica M10 before / after
- before = KRW 80,000 - 7,200,000
- after = KRW 5,780,000 - 6,000,000
- after price status = Body market summary is available.
- after why = Clean same-model price evidence

## 4. M10 accessory / variant handling
- accessory_excluded_count = 6
- variant_boundary_excluded_count = 1
- accessories_used_for_price = []
- adjacent_variant_rows = [{'title': "[위탁] M10 Monochrom 'Leitz Wetzlar' Edition", 'usage': 'Not used — Variant boundary', 'excluded_reason': ['Variant boundary']}]

## 5. regression status
- ui_copy_regressions = []
- price_projection_regressions = []
- body_lens_regressions = []

## 6. query summary
### Leica M10
- category = Body
- interpreted_target = Leica M10 body
- market_entry_value = KRW 5,780,000 - 6,000,000
- price_status = Body market summary is available.
- why = Clean same-model price evidence
- excluded_reason_counts = {'variant_boundary': 1, 'accessory': 6}
### leica m5
- category = Body
- interpreted_target = Leica M5 body
- market_entry_value = KRW 1,600,000 - 2,300,000
- price_status = Body market summary is available.
- why = Clean same-model price evidence
- excluded_reason_counts = {'duplicate': 1}
### Leica M6
- category = Body
- interpreted_target = Leica M6 body
- market_entry_value = KRW 2,700,000 - 4,200,000
- price_status = Body market summary is available.
- why = Clean same-model price evidence
- excluded_reason_counts = {'variant_boundary': 6, 'duplicate': 7, 'outlier': 2}
### Leica M9
- category = Body
- interpreted_target = Leica M9 body
- market_entry_value = KRW 3,800,000 - 4,500,000
- price_status = Body market summary is available.
- why = Clean same-model price evidence
- excluded_reason_counts = {'variant_boundary': 3}
### Leica M11
- category = Body
- interpreted_target = Leica M11 body
- market_entry_value = KRW 8,700,000 - 12,500,000
- price_status = Body market summary is available.
- why = Clean same-model price evidence
- excluded_reason_counts = {'variant_boundary': 3, 'duplicate': 1, 'outlier': 1}
### 35 lux aa
- category = Lens
- interpreted_target = Leica Summilux 35 AA candidate
- market_entry_value = KRW 3,380,000 - 8,200,000
- price_status = Reference price only.
- why = AA-specific price evidence is not enough yet.
- excluded_reason_counts = {}
### Noctilux 50 f1 E60
- category = Lens
- interpreted_target = Leica Noctilux 50 f1 E60 candidate
- market_entry_value = KRW 5,900,000 - 8,880,000
- price_status = Reference price only.
- why = E60-specific price evidence is not enough yet.
- excluded_reason_counts = {}
### Summicron 50 rigid
- category = Lens
- interpreted_target = Leica Summicron 50 Rigid candidate
- market_entry_value = KRW 2,400,000 - 3,500,000
- price_status = Exact price is available.
- why = Clean exact variant price evidence
- excluded_reason_counts = {'duplicate': 2, 'outlier': 2}
### M50/1.2
- category = Lens
- interpreted_target = Leica M-mount lens 50 f1.2 candidate
- market_entry_value = KRW 5,600,000 - 11,000,000
- price_status = Reference price only.
- why = Only broader reference pricing is safe for this query right now.
- excluded_reason_counts = {'wrong_model': 1, 'third_party': 1, 'duplicate': 14, 'outlier': 3}
### Leica M50/1.2 1세대
- category = Lens
- interpreted_target = Leica M-mount lens 50 f1.2 1st candidate
- market_entry_value = KRW 43,000,000 - 53,000,000
- price_status = Exact price is available.
- why = Clean exact variant price evidence
- excluded_reason_counts = {}
### APO-Summicron-SL 90
- category = Lens
- interpreted_target = Leica APO-Summicron-SL 90 candidate
- market_entry_value = Not enough evidence yet.
- price_status = Price summary is locked.
- why = Results are visible, but not strong enough for model-level pricing.
- excluded_reason_counts = {}
