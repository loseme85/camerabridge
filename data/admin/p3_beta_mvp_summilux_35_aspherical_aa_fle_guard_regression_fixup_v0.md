# P3-BETA-MVP-SUMMILUX-35-ASPHERICAL-AA-FLE-GUARD-REGRESSION-FIXUP v0

- branch: `beta-ui-redesign-controlled-preview`
- task: `SUMMILUX-35-ASPHERICAL-AA-FIXUP-REGRESSION-FLE-GUARD`
- app logic changed: `false`

## Summary

Current branch HEAD does **not** reproduce the reported P0 regression locally.

The narrow Summilux 35 FLE guard is already active in runtime exact-variant compatibility:

- ordinary `Summilux-M 35 ASPH` keeps ordinary ASPH rows as exact candidates
- `FLE` / `FLE II` rows are demoted to `Exact base model`
- those `FLE` rows are **not** used for exact price
- explicit `Summilux-M 35 FLE` / `35 lux fle` queries still keep FLE rows as `Exact variant`
- the recent context alias fix also remains active:
  - `Summilux-M 35 aspherical` -> `AA`
  - `Summilux 35 Aspherical` -> `AA`
  - `35 lux aspherical` -> `AA`

Because the requested behavior is already present on current HEAD, this round adds a verification report only and avoids layering extra logic on top of a working guard.

## Relevant code already present

### Query-side context alias recovery

`query_parser.py` currently narrows `aspherical -> AA` only in strong `Summilux 35` context and leaves global `aspherical -> ASPH` behavior unchanged outside that context.

### Runtime exact-variant guard

`api/search.py` currently blocks `FLE` rows from ordinary `Summilux 35 ASPH` exactness when:

- family root is `Summilux`
- focal is `35`
- query variant includes `ASPH`
- query variant does not include `FLE`
- row variant includes `FLE`

That is the exact narrow guard requested by this task.

## Narrow validation

### 1. `Summilux-M 35 ASPH`

Parsed intent:

- family: `Summilux`
- mount: `M`
- focal: `35`
- variant: `['ASPH']`

Observed ordinary ASPH rows:

- `Leica M 35mm f1.4 Summilux ASPH 4th Titan`
  - Evidence role: `Exact variant`
  - Price role: `Used for exact price`
  - used_for_price: `true`

- `Leica M 35mm f1.4 Summilux ASPH 4th Silver`
  - Evidence role: `Exact variant`
  - Price role: `Used for exact price`
  - used_for_price: `true`

Observed FLE rows:

- `신품 Leica M 35mm f1.4 Summilux ASPH 6bit FLE II Black`
  - Evidence role: `Exact base model`
  - Price role: `Same base model result is visible, but not used as exact price`
  - used_for_price: `false`

- `[위탁] M 35/1.4 Summilux ASPH FLE (Black)`
  - Evidence role: `Exact base model`
  - Price role: `Same base model result is visible, but not used as exact price`
  - used_for_price: `false`

Result:

- ordinary ASPH rows: exact allowed
- FLE / FLE II rows: **not** exact
- FLE / FLE II rows: **not** used for exact price

### 2. `Summilux-M 35 aspherical`

Parsed intent:

- family: `Summilux`
- mount: `M`
- focal: `35`
- variant: `['AA']`

Observed behavior:

- detected as AA candidate
- does not behave as ordinary ASPH
- visible rows stay conservative, mostly `Exact base model`

### 3. `Summilux 35 Aspherical`

Parsed intent:

- family: `Summilux`
- mount: `None`
- focal: `35`
- variant: `['AA']`

Observed behavior:

- detected as AA candidate
- does not behave as ordinary ASPH

### 4. `35 lux aspherical`

Parsed intent:

- family: `Summilux`
- mount: `None`
- focal: `35`
- variant: `['AA']`

Observed behavior:

- detected as AA candidate
- does not behave as ordinary ASPH

### 5. `35 lux aa`

Parsed intent:

- family: `Summilux`
- mount: `None`
- focal: `35`
- variant: `['AA']`

Observed behavior:

- unchanged
- still parsed as AA

### 6. `Summilux-M 35 AA`

Parsed intent:

- family: `Summilux`
- mount: `M`
- focal: `35`
- variant: `['AA']`

Observed behavior:

- unchanged
- still parsed as AA

### 7. `Summilux-M 35 FLE`

Parsed intent:

- family: `Summilux`
- mount: `M`
- focal: `35`
- variant: `['FLE']`

Observed FLE rows:

- `Leica M 35mm f1.4 Summilux ASPH 6bit FLE II Black`
  - Evidence role: `Exact variant`
  - Price role: `Used for exact price`
  - used_for_price: `true`

- `[위탁] M 35/1.4 Summilux ASPH FLE (Black)`
  - Evidence role: `Exact variant`
  - Price role: `Used for exact price`
  - used_for_price: `true`

Result:

- explicit FLE queries remain exact

### 8. Additional unchanged guards

- `Summilux-M 35 pre asph`
  - remains `pre-ASPH`
- `Summicron-M 35 ASPH`
  - unchanged
- `APO-Summicron-M 35 ASPH`
  - unchanged

## Interpretation

The owner-observed regression was **not reproducible** on current local branch HEAD.

Most likely explanations:

1. the owner checked a stale preview that did not include the existing FLE guard, or
2. the owner saw an earlier deployment before the current branch state.

Local runtime behavior now matches the requested expected results.

## Files changed

- `data/admin/p3_beta_mvp_summilux_35_aspherical_aa_fle_guard_regression_fixup_v0.md`

## Validation run

- `python3 -m py_compile api/search.py query_parser.py`
- narrow search/runtime smoke for:
  - `Summilux-M 35 ASPH`
  - `Summilux-M 35 aspherical`
  - `Summilux 35 Aspherical`
  - `35 lux aspherical`
  - `35 lux aa`
  - `Summilux-M 35 AA`
  - `Summilux-M 35 FLE`
  - `35 lux fle`
  - `Summilux-M 35 pre asph`
  - `Summicron-M 35 ASPH`
  - `APO-Summicron-M 35 ASPH`

## Recommended owner recheck

Recheck the latest branch head / latest preview specifically for:

- `Summilux-M 35 ASPH`
  - confirm visible `FLE` / `FLE II` rows show:
    - `Evidence role: Exact base model`
    - not `Exact variant`
    - not `Used for exact price`

- `Summilux-M 35 aspherical`
  - confirm detected candidate remains AA

- `Summilux-M 35 FLE`
  - confirm FLE rows remain exact

## Final decision

`decision_status = summilux_35_aspherical_aa_fle_guard_regression_fixup_pushed_ready_for_owner_recheck`
