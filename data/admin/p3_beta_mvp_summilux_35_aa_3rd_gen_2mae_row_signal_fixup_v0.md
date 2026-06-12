# P3 Beta MVP - Summilux 35 AA 3rd Gen 2Mae Row Signal Fixup v0

- Branch: `beta-ui-redesign-controlled-preview`
- Decision status: `summilux_35_aa_3rd_gen_2mae_row_signal_fixup_pushed_ready_for_owner_recheck`

## Files changed

- `api/search.py`
- `data/admin/p3_beta_mvp_summilux_35_aa_3rd_gen_2mae_row_signal_fixup_v0.md`

## Exact change

- Widened the narrow Summilux 35 AA row signal check so `2매` is recognized even when wrapped as `(2매)`.
- Added a narrow price-pool guard for strong Summilux 35 AA queries:
  - if a row is AA-exact by `2매`
  - and also carries `3세대` / `v3`
  - and the row is `asking`
  - then keep the row as `Exact variant` at row level
  - but exclude it from exact price with `outlier`

## Owner-visible result

For AA queries:

- `35 lux aa`
- `Summilux-M 35 aspherical`
- `35 lux aspherical`
- `Summilux-M 35 AA`

these rows now show:

- `[위탁] M 35/1.4 Summilux 3세대 (2매) (Black)`
  - `Evidence role: Exact variant`
  - `Price role: Not used — Price outlier`
  - `Reason: Price outlier`
- `[중고] M 35/1.4 Summilux 3세대 (2매) (Black)`
  - `Evidence role: Exact variant`
  - `Price role: Not used — Price outlier`
  - `Reason: Price outlier`

## Safety checks

- `Summilux-M 35 ASPH`
  - ordinary ASPH rows remain exact
  - FLE / FLE II / FLE2 rows remain same-base only and not exact price
- `Summilux-M 35 FLE`
  - FLE rows remain exact variant
- `Summilux-M 35 pre asph`
  - unchanged
- No parser changes
- No ranking changes
- No pricing threshold changes
- No duplicate policy changes
- No UI/layout/load-more changes

## Validation run

- `python3 -m py_compile api/search.py`
- Narrow smoke:
  - `35 lux aa`
  - `Summilux-M 35 aspherical`
  - `35 lux aspherical`
  - `Summilux-M 35 AA`
  - `Summilux-M 35 ASPH`
  - `Summilux-M 35 FLE`
  - `Summilux-M 35 pre asph`

## Notes

- The plain `2매` row still stays `Exact variant`, but now falls back to `Exact match visible, but not enough to unlock price yet` rather than forcing an unlock.
- This fix stays narrow and does not treat generation-only wording as AA by itself.
