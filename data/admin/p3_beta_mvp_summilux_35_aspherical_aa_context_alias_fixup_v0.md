P3-BETA-MVP-SUMMILUX-35-ASPHERICAL-AA-CONTEXT-ALIAS-FIXUP

Branch: `beta-ui-redesign-controlled-preview`

Decision status:
`summilux_35_aspherical_aa_context_alias_fixup_pushed_ready_for_owner_recheck`

## Files changed

- `query_parser.py`

## Exact fix

Added a narrow context-sensitive alias rule in query parsing:

If all of the following are true:

- strong `Summilux 35` context
- query contains `aspherical`
- query does **not** explicitly contain `asph`
- query does **not** contain `FLE`
- query does **not** contain `pre asph`

then:

- query-side variant is parsed as `AA`

not:

- `ASPH`

This change applies only to the narrow `Summilux 35` collector context.

Global `aspherical -> ASPH` behavior remains unchanged elsewhere.

## Before / after

### `Summilux-M 35 aspherical`

Before:

- parsed as variant `ASPH`
- behaved like ordinary later ASPH query

After:

- parsed as variant `AA`
- now follows AA / Double Aspherical intent path

### `Summilux 35 Aspherical`

Before:

- parsed as `ASPH`

After:

- parsed as `AA`

### `35 lux aspherical`

Before:

- parsed as `ASPH`

After:

- parsed as `AA`

## Preserved behavior

- `Summilux-M 35 ASPH` remains ordinary `ASPH`
- `35 lux aa` remains `AA`
- `Summilux-M 35 AA` remains `AA`
- `Summilux-M 35 FLE` remains `FLE`
- `Summilux-M 35 pre asph` remains `pre-ASPH`
- `Summicron-M 35 ASPH` unchanged
- `APO-Summicron-M 35 ASPH` unchanged

## Validation

- `python3 -m py_compile query_parser.py` passed

Narrow smoke checked:

- `Summilux-M 35 ASPH`
- `Summilux-M 35 aspherical`
- `Summilux 35 Aspherical`
- `35 lux aspherical`
- `35 lux aa`
- `Summilux-M 35 AA`
- `Summilux-M 35 FLE`
- `Summilux-M 35 pre asph`
- `Summicron-M 35 ASPH`
- `APO-Summicron-M 35 ASPH`

Observed:

- `Summilux-M 35 aspherical` now parses as `AA`
- `Summilux 35 Aspherical` now parses as `AA`
- `35 lux aspherical` now parses as `AA`
- ordinary `Summilux-M 35 ASPH` remains ordinary ASPH
- FLE path remains unchanged
- Summicron / APO-Summicron guard queries did not regress

## Important follow-up note

This fix changes query intent correctly, but it does **not** fully solve AA exact-price recognition by itself.

After this alias fix:

- `aspherical` queries now correctly route into `AA` intent
- but visible/runtime results still mostly show:
  - `Exact base model`
  - outlier / no-price / duplicate states

So the likely next follow-up, if owner wants it, is:

- narrow AA row-compatibility / exactness recognition

## What did not change

- ranking
- pricing thresholds
- duplicate policy
- UI layout
- query summary bar
- Load more
- 3-column grid

