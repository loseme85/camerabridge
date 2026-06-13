# P3 Beta MVP - Summilux 35 FLE2 Exact-Compatible Price Role Projection Fixup v1

`decision_status = summilux_35_fle2_exact_compatible_price_role_projection_fixup_v1_pushed_ready_for_owner_recheck`

## Exact change

This fix does **not** change:

- parser intent
- search scoring
- result ranking
- duplicate/outlier policy
- global price thresholds
- exact price unlock logic

This fix only changes **visible price-role projection copy** for a narrow case:

- explicit FLE2-intent queries
- visible row already classified as `compatibility = Exact variant`
- visible row already classified as `evidence role = Exact variant`
- row is not used for exact price
- row is not excluded for duplicate, outlier, or unusable price
- row had previously fallen through to `exact_base_model_pool` copy

New copy:

- `Exact variant match visible, but not selected for exact price`

## Before / after for the repeated mismatch row

Repeated row:

- `Leica M 35mm f1.4 Summilux ASPH 6bit FLE II Black`

### Before

- compatibility: `Exact variant`
- evidence role: `Exact variant`
- price role: `Same base model result is visible, but not used as exact price`
- used_for_price: `False`

This looked contradictory because the row was already accepted as exact-compatible but was still described with same-base-only price-role copy.

### After

- compatibility: `Exact variant`
- evidence role: `Exact variant`
- price role: `Exact variant match visible, but not selected for exact price`
- used_for_price: `False`

This keeps pricing conservative while removing the exact-vs-same-base contradiction.

## Validation table - FLE2 / FLE II / close focus

| Query | Interpreted target | Price scope | Exact price unlocked | Repeated row present | Repeated row after fix | Notes |
|---|---|---|---:|---:|---|---|
| `Summilux-M 35 FLE2` | `Leica Summilux-M 35 FLE2 candidate` | `exact_variant` | Yes | Yes | `Exact variant match visible, but not selected for exact price` | Exact-compatible row no longer reads as same-base only |
| `Summilux-M 35 FLE II` | `Leica Summilux-M 35 FLE2 candidate` | `exact_variant` | Yes | Yes | `Exact variant match visible, but not selected for exact price` | Same result |
| `Summilux-M 35 close focus` | `Leica Summilux-M 35 FLE2 candidate` | `exact_variant` | Yes | Yes | `Exact variant match visible, but not selected for exact price` | Same result |
| `35 lux FLE2` | `Leica Summilux 35 FLE2 candidate` | `exact_variant` | Yes | Yes | `Exact variant match visible, but not selected for exact price` | Same result |
| `35 lux FLE II` | `Leica Summilux 35 FLE2 candidate` | `exact_variant` | Yes | Yes | `Exact variant match visible, but not selected for exact price` | Same result |

### Primary-set observations

- True selected FLE2 rows still show `Used for exact price`
- The repeated FLE II row keeps:
  - `compatibility = Exact variant`
  - `evidence role = Exact variant`
  - `used_for_price = False`
- No non-FLE2 row was promoted into exact-variant price usage

## Non-FLE2 boundary regression table

| Query | Expected preserved behavior | Result |
|---|---|---|
| `Summilux-M 35` | broad mixed query stays conservative | PASS |
| `Summilux-M 35 ASPH` | ASPH exactness unchanged | PASS |
| `Summilux-M 35 FLE` | FLE remains conservative when mixed | PASS |
| `Summilux-M 35 2매` | AA candidate remains conservative | PASS |
| `Summilux 35 Steel Rim` | Steel Rim candidate remains intact | PASS |

Notes:

- `Summilux-M 35` remains `price_scope = insufficient_exact_data`
- `Summilux-M 35 ASPH` still uses ASPH exact price behavior
- `Summilux-M 35 FLE` still shows exact-compatible FLE rows with locked/limited price behavior
- AA / Steel Rim behavior stayed intact

## Recent P0 safety regression table

| Query | Expected preserved behavior | Result |
|---|---|---|
| `50 cron dr` | DR exactness remains safe | PASS |
| `Leica Summicron 50 rigid` | rigid guard remains safe | PASS |
| `Leica 12585` | hood/accessory stays price-safe | PASS |
| `Leica M10 lens kit` | body bundle exact-price guard remains active | PASS |

Notes:

- No reopened P0 was reproduced
- No body/lens exact price behavior changed
- No accessory query gained a lens/body exact price unlock

## Confirmation of unchanged logic

Confirmed unchanged in this fix:

- parser behavior
- ranking behavior
- price thresholds
- duplicate policy
- outlier policy
- exact price unlock criteria

Only the projected visible price-role copy changed for the narrow FLE2 exact-compatible mismatch case.

## Remaining issues

- This fix does **not** alter which exact-compatible FLE2 rows are selected into the exact price pool.
- It only clarifies their displayed price-role state.
- If owner later wants the remaining non-selected exact-compatible rows to be treated differently, that would be a separate pool-selection / price-policy discussion, not this fix.
