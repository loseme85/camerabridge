# P3 Beta MVP - Summilux-M 35 Compact FLE2 Row Evidence Fixup v1

`decision_status = summilux_m_35_compact_fle2_row_evidence_fixup_v1_pushed_ready_for_owner_recheck`

## Exact change

This fix adds a **narrow projection fallback** only for explicit compact `FLE2` intent in Summilux-M 35 context.

If a visible row:

- belongs to an explicit `Summilux-M 35 FLE2`-style query
- has clear row-level `FLE2` / `FLE II` / `FLE 2` / `close focus` signal
- is not excluded for duplicate / outlier / unusable price
- would otherwise still project as `Exact base model`

then the visible evidence projection is promoted to:

- `compatibility = Exact variant`
- `evidence role = Exact variant`
- `evidence_pool = exact_variant_pool`

This is a **projection consistency fix**, not a parser change and not a ranking change.

## Before / after for `Summilux-M 35 FLE2`

### Owner-observed before

Under the compact query:

- `Summilux-M 35 FLE2`

some obvious FLE2 rows were reportedly shown as:

- badge: `Family match strong`
- evidence role: `Same base model`
- price role: `Same base model result is visible, but not used as exact price`

Observed rows:

- `[위탁] M 35/1.4 Summilux ASPH FLE2 (Black)`
- `[중고] M 35/1.4 Summilux ASPH 6bit FLE2 (Black)`

### After

Current local runtime after the fix:

- `[위탁] M 35/1.4 Summilux ASPH FLE2 (Black)`
  - compatibility: `Exact variant`
  - evidence role: `Exact variant`
  - price role: `Used for exact price`
- `[중고] M 35/1.4 Summilux ASPH 6bit FLE2 (Black)`
  - compatibility: `Exact variant`
  - evidence role: `Exact variant`
  - price role: `Used for exact price`

The compact `FLE2` query now aligns with:

- `Summilux-M 35 FLE II`
- `Summilux-M 35 close focus`
- `35 lux FLE2`
- `35 lux FLE II`

## Trace for the two observed rows

| Row title | Query | Compatibility | Evidence role | Evidence pool | Price role | Used for price |
|---|---|---|---|---|---|---:|
| `[위탁] M 35/1.4 Summilux ASPH FLE2 (Black)` | `Summilux-M 35 FLE2` | `Exact variant` | `Exact variant` | `exact_variant_pool` | `Used for exact price` | `True` |
| `[중고] M 35/1.4 Summilux ASPH 6bit FLE2 (Black)` | `Summilux-M 35 FLE2` | `Exact variant` | `Exact variant` | `exact_variant_pool` | `Used for exact price` | `True` |

Additional checked row:

| Row title | Query | Compatibility | Evidence role | Evidence pool | Price role | Used for price |
|---|---|---|---|---|---|---:|
| `Leica M 35mm f1.4 Summilux ASPH 6bit FLE II Black` | `Summilux-M 35 FLE2` | `Exact variant` | `Exact variant` | `exact_base_model_pool` | `Exact variant match visible, but not selected for exact price` | `False` |

This row keeps the earlier projection fix and remains price-safe.

## Regression table

| Query | Expected preserved behavior | Result |
|---|---|---|
| `Summilux-M 35 FLE II` | FLE2 interpretation stays correct | PASS |
| `Summilux-M 35 close focus` | FLE2 interpretation stays correct | PASS |
| `35 lux FLE2` | FLE2 interpretation stays correct | PASS |
| `35 lux FLE II` | FLE2 interpretation stays correct | PASS |
| `Summilux-M 35` | broad mixed query remains conservative | PASS |
| `Summilux-M 35 ASPH` | ASPH behavior unchanged | PASS |
| `Summilux-M 35 FLE` | FLE behavior unchanged | PASS |
| `Summilux-M 35 2매` | AA behavior unchanged | PASS |
| `Summilux 35 Steel Rim` | Steel Rim behavior unchanged | PASS |
| `50 cron dr` | DR safety unchanged | PASS |
| `Leica Summicron 50 rigid` | rigid safety unchanged | PASS |
| `Leica 12585` | hood/accessory behavior unchanged | PASS |
| `Leica M10 lens kit` | body bundle guard unchanged | PASS |

## Confirmation of unchanged broader logic

Confirmed unchanged by this fix:

- parser behavior
- ranking behavior
- price thresholds
- duplicate policy
- outlier policy
- FLE vs FLE2 global boundary policy
- AA / 2매 logic
- DR / Dual Range logic
- Rigid mount guard
- body bundle guard
- accessory/hood logic

This change only adds a narrow row-level evidence projection safeguard for compact explicit `FLE2` intent.

## Remaining issues

- No new P0 was reproduced.
- The remaining FLE2 concerns, if any, are now limited to preview verification and minor presentation consistency rather than pricing safety.
