# P3-BETA-MVP-MODEL-MARKET-ENTRY-UI-COPY-PROJECTION-FIXUP

## 1. 작업명
- `P3-BETA-MVP-MODEL-MARKET-ENTRY-UI-COPY-PROJECTION-FIXUP`

## 2. exact copy changes
- Model Market Entry now uses `Exact price`, `Same model price`, `Reference price only`, `Price locked`, and `Body market summary` instead of raw scope text.
- Unlock requirements now reuse the same human wording already used in Query review and render as list-style text instead of slash-joined debug text.
- Price evidence now shows the human summary sentence from the evidence pool summary instead of raw internal scope tokens.

## 3. per-query status
### 35 lux aa
- category = Lens
- interpreted_target = Leica Summilux 35 AA candidate
- market_entry_label = Reference price only
- market_entry_value = KRW 3,380,000 - 8,200,000
- price_status = Reference price only.
- why = AA-specific price evidence is not enough yet.
### Noctilux 50 f1 E60
- category = Lens
- interpreted_target = Leica Noctilux 50 f1 E60 candidate
- market_entry_label = Reference price only
- market_entry_value = KRW 5,900,000 - 8,880,000
- price_status = Reference price only.
- why = E60-specific price evidence is not enough yet.
### Summicron 50 rigid
- category = Lens
- interpreted_target = Leica Summicron 50 Rigid candidate
- market_entry_label = Exact price
- market_entry_value = KRW 2,400,000 - 3,500,000
- price_status = Exact price is available.
- why = Clean exact variant price evidence
### Summilux-M 50 ASPH
- category = Lens
- interpreted_target = Leica Summilux-M 50 ASPH candidate
- market_entry_label = Reference price only
- market_entry_value = KRW 3,150,000 - 6,900,000
- price_status = Reference price only.
- why = Top visible results include third-party or adjacent items.
### M50/1.2
- category = Lens
- interpreted_target = Leica M-mount lens 50 f1.2 candidate
- market_entry_label = Reference price only
- market_entry_value = KRW 5,600,000 - 11,000,000
- price_status = Reference price only.
- why = Only broader reference pricing is safe for this query right now.
### Leica M50/1.2 1세대
- category = Lens
- interpreted_target = Leica M-mount lens 50 f1.2 1st candidate
- market_entry_label = Exact price
- market_entry_value = KRW 43,000,000 - 53,000,000
- price_status = Exact price is available.
- why = Clean exact variant price evidence
### leica m5
- category = Body
- interpreted_target = Leica M5 body
- market_entry_label = Body market summary
- market_entry_value = KRW 1,600,000 - 2,300,000
- price_status = Body market summary is available.
- why = Clean same-model price evidence
### Leica M6
- category = Body
- interpreted_target = Leica M6 body
- market_entry_label = Body market summary
- market_entry_value = KRW 2,700,000 - 6,180,000
- price_status = Body market summary is available.
- why = Clean same-model price evidence
### Leica M9
- category = Body
- interpreted_target = Leica M9 body
- market_entry_label = Body market summary
- market_entry_value = KRW 3,800,000 - 4,500,000
- price_status = Body market summary is available.
- why = Clean same-model price evidence
### Leica M10
- category = Body
- interpreted_target = Leica M10 body
- market_entry_label = Body market summary
- market_entry_value = KRW 80,000 - 7,200,000
- price_status = Body market summary is available.
- why = Reference prices are too spread out to show safely
### Leica M11
- category = Body
- interpreted_target = Leica M11 body
- market_entry_label = Body market summary
- market_entry_value = KRW 8,700,000 - 12,500,000
- price_status = Body market summary is available.
- why = Clean same-model price evidence
### APO-Summicron-SL 90
- category = Lens
- interpreted_target = Leica APO-Summicron-SL 90 candidate
- market_entry_label = Price locked
- market_entry_value = Not enough evidence yet.
- price_status = Price summary is locked.
- why = Results are visible, but not strong enough for model-level pricing.

## 4. regression status
- ui_still_too_technical = []
- query_review_regressions = []
- price_projection_regressions = []
- body_lens_regressions = []

## 5. preview / push context
- preview_url = not recorded
- commit_executed = False
- push_executed = False
- push_succeeded = False
