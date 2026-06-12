# P3 Beta MVP - Summilux 35 FLE2 Boundary Fixup v0

- Branch: `beta-ui-redesign-controlled-preview`
- Decision status: `summilux_35_fle2_boundary_fixup_pushed_ready_for_owner_recheck`

## Files changed

- `query_parser.py`
- `search_aliases.py`
- `api/search.py`
- `data/admin/p3_beta_mvp_summilux_35_fle2_boundary_fixup_v0.md`

## Exact change

### 1. Query intent

Added a distinct `FLE2` query variant for strong Summilux 35 context:

- `fle2`
- `fle ii`
- `fle 2`
- `close focus`
- `close-focus`

These no longer collapse to broad `FLE`.

### 2. Row-side signal extraction

Added a distinct row-side `FLE2` signal for titles containing:

- `FLE2`
- `FLE II`
- `FLE 2`
- `close focus`
- `close-focus`

Rows with only:

- `FLE`
- `floating element`

remain broad FLE / FLE1-side.

### 3. Exact compatibility

For explicit `FLE2` queries:

- FLE2 rows can be `Exact variant`
- FLE1-only rows are no longer exact-price candidates
- FLE1-only rows now show as same-base only

### 4. Bare FLE mixed-pool lock

For bare:

- `Summilux-M 35 FLE`
- `35 lux fle`

if FLE1 and FLE2 rows are mixed in the exact-variant evidence set:

- exact price is now kept locked
- cards still show visible exact matches
- but no unlocked exact price band is shown from the mixed pool

## Owner-visible behavior

### `Summilux-M 35 FLE2`

FLE2 rows:

- `Evidence role: Exact variant`
- `Price role: Used for exact price` or normal outlier/duplicate handling

FLE1-only rows:

- `Evidence role: Same base model`
- `Price role: Same base model result is visible, but not used as exact price`

### `Summilux-M 35 FLE II`

Same as `FLE2`.

### `35 lux fle2`

Same as `FLE2`.

### `Summilux-M 35 close focus`

Now behaves as `FLE2` intent instead of broad same-base fallback.

### `Summilux-M 35 FLE`

Visible FLE1/FLE2 rows may still both appear as exact-family matches,
but mixed-generation evidence no longer unlocks an exact price band.

## Validation summary

### Parser / intent

- `Summilux-M 35 FLE` -> `variant=['FLE']`
- `Summilux-M 35 FLE2` -> `variant=['FLE2']`
- `Summilux-M 35 FLE II` -> `variant=['FLE2']`
- `35 lux fle2` -> `variant=['FLE2']`
- `35 lux fle ii` -> `variant=['FLE2']`
- `Summilux-M 35 close focus` -> `variant=['FLE2']`

### Runtime smoke

- `Summilux-M 35 FLE`
  - `price_summary_allowed = False`
  - `price_scope_label = Exact variant price data limited`
  - mixed FLE1/FLE2 pool no longer unlocks exact price

- `Summilux-M 35 FLE2`
  - `variant_tokens_detected = ['FLE2']`
  - `price_summary_allowed = True`
  - `display_price_band = KRW 6,700,000 - 8,200,000`
  - visible FLE1 rows remain same-base only

- `Summilux-M 35 FLE II`
  - same as `FLE2`

- `35 lux fle2`
  - same as `FLE2`

- `Summilux-M 35 close focus`
  - now follows `FLE2` exact variant path

### Required safety checks

- explicit `FLE2` queries do not use FLE1 rows as exact price
- bare `FLE` query does not unlock exact price from mixed FLE1/FLE2 pool
- `Summilux-M 35 ASPH` still keeps FLE/FLE2 rows out of exact ASPH price
- `Summilux-M 35 aspherical` / `35 lux aa` still keep FLE/FLE2 rows out of AA exact price
- no UI layout changes

## Validation run

- `python3 -m py_compile query_parser.py search_aliases.py api/search.py`
- narrow smoke:
  - `Summilux-M 35 FLE`
  - `35 lux fle`
  - `Summilux-M 35 FLE2`
  - `Summilux-M 35 FLE II`
  - `35 lux fle2`
  - `35 lux fle ii`
  - `Summilux-M 35 close focus`
  - `Summilux-M 35 ASPH`
  - `Summilux-M 35 aspherical`
  - `35 lux aa`
