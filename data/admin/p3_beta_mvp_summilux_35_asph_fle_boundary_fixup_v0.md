P3-BETA-MVP-SUMMILUX-35-ASPH-FLE-BOUNDARY-FIXUP

Branch: `beta-ui-redesign-controlled-preview`

Decision status:
`summilux_35_asph_fle_boundary_fixup_pushed_ready_for_owner_recheck`

## Files changed

- `api/search.py`

## Exact fix

Added a narrow exact-variant guard in row-level exactness matching:

- family root: `Summilux`
- focal length: `35`
- mount: `M` or mount-agnostic query
- query variant includes `ASPH`
- query variant does **not** include `FLE`
- row includes `FLE`

When that happens:

- the row no longer qualifies as `Exact variant`
- the row no longer enters ordinary ASPH exact-price evidence
- the row falls back to `Exact base model` / same-base reference behavior

This changes exact-variant admission only.

It does **not** change:

- parser output
- ranking
- pricing thresholds
- duplicate policy
- UI layout

## Primary result

### `Summilux-M 35 ASPH`

Before:

- FLE / FLE II rows could show:
  - `Evidence role: Exact variant`
  - `Price role: Used for exact price`
  - `used_for_price = True`

After:

- ordinary ASPH rows remain:
  - `Evidence role: Exact variant`
  - `Price role: Used for exact price`

- FLE / FLE II rows now show:
  - `Evidence role: Exact base model`
  - `Price role: Same base model result is visible, but not used as exact price`
  - `used_for_price = False`

### `Summilux 35 Aspherical`

After:

- same ordinary ASPH protection now applies
- FLE / FLE II rows no longer act as exact price evidence

## Preserved behavior

### `Summilux-M 35 FLE`

- FLE / FLE II rows remain:
  - `Evidence role: Exact variant`
  - exact-price-eligible when other price gates pass

### `35 lux fle`

- unchanged
- FLE rows remain exact

### `35 lux aa`

- unchanged
- remains conservative

### `Summilux-M 35 pre asph`

- unchanged

### `35 lux pre asph`

- unchanged

### `Summicron-M 35 ASPH`

- unchanged

### `APO-Summicron-M 35 ASPH`

- unchanged

## Validation

- `python3 -m py_compile api/search.py` passed

Narrow runtime smoke checked:

- `Summilux-M 35 ASPH`
- `Summilux 35 Aspherical`
- `Summilux-M 35 FLE`
- `35 lux fle`
- `35 lux aa`
- `Summilux-M 35 pre asph`
- `35 lux pre asph`
- `Summicron-M 35 ASPH`
- `APO-Summicron-M 35 ASPH`

Observed results:

- ordinary ASPH / Aspherical queries no longer use FLE rows as exact price evidence
- explicit FLE queries still use FLE rows as exact evidence
- AA and pre-ASPH stay conservative
- Summicron / APO-Summicron guard queries did not regress

UI guard checks by inspection:

- query summary bar still present
- `Load more` hook still present
- 4-column result grid did not return
- template mirror remains in sync

## What did not change

- query summary bar
- Load more
- 3-column grid
- duplicate / outlier / no-price reason behavior
- Market Entry logic
- Query Review logic

