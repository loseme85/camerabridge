# P3-BETA-MVP-SUMMILUX-35-AA-ROW-SIGNAL-EXACTNESS-FIXUP v0

- branch: `beta-ui-redesign-controlled-preview`
- task: `SUMMILUX-35-AA-ROW-SIGNAL-EXACTNESS-FIXUP`

## Files changed

- `api/search.py`

## Exact change

Added narrow runtime row-side `AA` recognition for strong `Summilux 35` row context only.

New behavior is limited to rows where:

- category is `Lens`
- family root is `Summilux`
- focal is `35`
- mount is `M` or unknown

and the row text contains one of:

- `AA`
- `Double Aspherical`
- `ASPHERICAL`
- `2매`

with an important exclusion:

- rows containing `FLE`, `FLE II`, `FLE2`, `floating element`, or `close focus` do **not** become `AA`

Also added a narrow guard so ordinary `Summilux 35 ASPH` exact-variant scope does not accept these `AA`-signaled rows as ordinary ASPH exact evidence.

## Result

### AA queries now recognize row-side AA signals

The following queries now produce visible `Exact variant` AA matches where the row signal is clear:

- `35 lux aa`
- `35 lux aspherical`
- `Summilux-M 35 aspherical`
- `Summilux 35 Aspherical`
- `Summilux-M 35 AA`

Examples:

- `[중고] M35/1.4 Summilux 2매 (Black)`
  - `Evidence role: Exact variant`
  - `Price role: Exact match visible, but not enough to unlock price yet`
  - `used_for_price = false`

- `LEICA 35mm F1.4 ASPHERICAL SUMMILUX-M sn.3460`
  - `Evidence role: Exact variant`
  - `Price role: No usable price`
  - `used_for_price = false`

- `LEICA 35mm F1.4 ASPHERICAL SUMMILUX-M sn.3461`
  - `Evidence role: Exact variant`
  - `Price role: No usable price`
  - duplicate rows remain duplicates

AA evidence summary improved from:

- `0 exact AA listings`

to:

- `1 exact AA listing`

for the checked AA queries.

### Price behavior remains conservative

AA rows are not being force-promoted into unlocked exact prices.

Observed conservative outcomes remain intact:

- `Not used — Price outlier`
- `No usable price`
- `Duplicate listing`
- `Exact match visible, but not enough to unlock price yet`

## Safety checks

### Ordinary ASPH query remains protected

For `Summilux-M 35 ASPH`:

- ordinary ASPH rows remain `Exact variant`
- FLE / FLE II / FLE2 rows remain `Exact base model`
- FLE / FLE II / FLE2 rows remain not used for exact price

### FLE query remains protected

For `Summilux-M 35 FLE`:

- FLE rows remain `Exact variant`
- FLE rows still enter exact-price eligibility normally

### pre-ASPH query remains unchanged

For `Summilux-M 35 pre asph`:

- pre-ASPH behavior remains conservative
- no new AA contamination observed

### No wrong exact-price borrowing observed

Current runtime still avoids:

- ordinary ASPH rows being used as AA exact price evidence inappropriately
- FLE / FLE2 rows being used as AA exact price evidence
- AA rows being used as ordinary ASPH exact price evidence

## Validation

- `python3 -m py_compile api/search.py`
- narrow smoke:
  - `35 lux aa`
  - `35 lux aspherical`
  - `Summilux-M 35 aspherical`
  - `Summilux 35 Aspherical`
  - `Summilux-M 35 AA`
  - `Summilux-M 35 ASPH`
  - `Summilux-M 35 FLE`
  - `Summilux-M 35 pre asph`

## Representative smoke results

### `35 lux aa`

- interpreted target: `Leica Summilux 35 AA candidate`
- price status: `Reference price only.`
- evidence summary: `Price evidence found: 1 exact AA listing, 39 same-base listings, 39 broader references. Excluded from price: 0 listings.`

### `Summilux-M 35 aspherical`

- interpreted target: `Leica Summilux-M 35 AA candidate`
- `ASPHERICAL` rows now show `Exact variant`
- `2매` row now shows `Exact variant`
- FLE ASPHERICAL limited-edition row remains `Exact base model`

### `Summilux-M 35 ASPH`

- ordinary ASPH rows remain exact
- FLE / FLE II / FLE2 rows remain same-base only

### `Summilux-M 35 FLE`

- FLE rows remain exact and exact-price eligible

## What did not change

- query parser
- ranking
- pricing thresholds
- duplicate policy
- UI layout
- query summary bar
- Load more

## Final decision

`decision_status = summilux_35_aa_row_signal_exactness_fixup_pushed_ready_for_owner_recheck`
