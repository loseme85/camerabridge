# P3 Beta MVP - Summicron 50 DR / Dual Range Recovery Fixup v0

- Branch: `beta-ui-redesign-controlled-preview`
- Decision status: `summicron_50_dr_dual_range_recovery_fixup_pushed_ready_for_owner_recheck`

## Files changed

- `query_parser.py`
- `api/search.py`
- `data/admin/p3_beta_mvp_summicron_50_dr_dual_range_recovery_fixup_v0.md`

## Exact parser changes

Added narrow DR recovery in strong Summicron 50 context:

- `dr`
- `dual range`
- `dual-range`
- `dualrange`

now all recover to the existing query variant token:

- `Dual Range`

This now works for:

- `50 cron dr`
- `Summicron 50 DR`
- `Summicron 50 Dual Range`
- `Summicron-M 50 Dual Range`
- `Leica Summicron 50 DR`

## Row-side DR signal changes

Added narrow row-side DR recognition in strong Summicron 50 row context:

- ` DR `
- `Dual Range`
- `dual-range`
- `dualrange`

These rows now qualify for the `Dual Range` variant signal even when the normalized row variant list does not explicitly contain `Dual Range`.

Examples now recognized as DR exact candidates:

- `Leica M 50mm f2 Summicron DR Silver`
- `[중고] M 50/2 Summicron DR (Silver)`
- `[위탁] M 50/2 Summicron DR (Silver)`

Safety:

- ordinary Summicron 50 rows are not tagged as DR
- rigid rows are not tagged as DR unless they explicitly also contain DR wording
- non-M rows do not gain DR exactness through this helper because the row context is restricted to Summicron 50 on M / Unknown only

## Before / after behavior

| Query | Before | After |
|---|---|---|
| `50 cron dr` | parsed `Dual Range`, but DR rows did not become exact variant | DR rows now show `Exact variant` |
| `Summicron 50 DR` | same as above | same as above |
| `Summicron 50 Dual Range` | parser missed DR variant entirely | now parses `Dual Range` |
| `Summicron-M 50 Dual Range` | parser missed DR variant entirely | now parses `Dual Range` with `mount=M` |
| `Leica Summicron 50 DR` | parsed DR, but rows still stayed broad same-base | DR rows now exact variant |

## Owner-visible card expectations

### DR / Dual Range queries

For:

- `50 cron dr`
- `Summicron 50 DR`
- `Summicron 50 Dual Range`
- `Summicron-M 50 Dual Range`
- `Leica Summicron 50 DR`

DR rows now show:

- `Evidence role: Exact variant`
- `Price role: Exact match visible, but not enough to unlock price yet`
  or normal outlier / duplicate / no-price handling

Non-DR rows now stay out of DR exact price:

- rigid rows -> not exact DR price
- ordinary Summicron 50 rows -> not exact DR price
- R-mount rows -> not exact DR price
- LTM / M39 rows -> not exact DR price

### Broad `Summicron-M 50`

Unchanged:

- stays broad / mixed-generation locked
- does not unlock DR / Rigid / ordinary mixed exact price

## Runtime result summary

### `50 cron dr`

- `variant_tokens_detected = ['Dual Range']`
- `exact_variant_pool_count = 3`
- DR rows now visible as exact variant
- price still locked because top-result / query-review path remains in boundary hold when a wrong-mount result dominates the top slot

### `Summicron 50 Dual Range`

- now also `variant_tokens_detected = ['Dual Range']`
- same exact DR rows recover

### `Summicron-M 50 Dual Range`

- `variant_tokens_detected = ['Dual Range']`
- DR rows now exact variant
- rigid / ordinary rows remain not exact price

## Regression checks

### `Leica Summicron 50 rigid`

- rigid exactness remains active
- DR rows do not become rigid exact price
- note: existing M vs LTM / M39 rigid mount guard is still not fixed in this round

### `50 cron rigid`

- unchanged
- rigid exact price still works

### `Summicron 50 2nd`

- unchanged
- exact 2nd-gen pool still works

### `Summicron 50 R`

- unchanged
- R-mount exact-base pricing still works

### `Summicron-M 50`

- unchanged
- mixed generations remain locked / same-base only

## Remaining follow-up

Still present after this fix:

- `Leica Summicron 50 rigid` and `50 cron rigid` can still absorb L / M39-looking rigid rows into exact rigid price when the query mount is not explicit

This follow-up was intentionally **not** addressed in this round.

Recommended follow-up label:

- rigid M vs LTM / M39 mount guard

## Validation run

- `python3 -m py_compile query_parser.py api/search.py`
- narrow smoke:
  - `50 cron dr`
  - `Summicron 50 DR`
  - `Summicron 50 Dual Range`
  - `Summicron-M 50 Dual Range`
  - `Leica Summicron 50 DR`
  - `Leica Summicron 50 rigid`
  - `50 cron rigid`
  - `Summicron 50 2nd`
  - `Summicron-M 50`
  - `Summicron 50 R`
