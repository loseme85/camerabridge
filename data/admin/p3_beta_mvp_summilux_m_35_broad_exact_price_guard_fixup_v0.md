# P3 Beta MVP — Summilux-M 35 Broad Exact Price Guard Fixup v0

## Decision Status

`summilux_m_35_broad_exact_price_guard_fixup_pushed_ready_for_owner_recheck`

## Exact Change

- Added a narrow `api/search.py` guard for broad `Summilux-M 35` queries.
- The guard applies only when:
  - family is `Summilux`
  - focal is `35`
  - mount is `M`
  - the query has no explicit variant token or generation token
- The guard inspects the broad `exact_base_model` price pool.
- If the pool mixes materially different Summilux 35 variant families, it blocks exact-base-model price unlock.
- Mixed families checked:
  - `2nd / pre-ASPH`
  - ordinary `ASPH`
  - `FLE`
  - `FLE2 / FLE II`
  - `AA / 2매`
  - `Steel Rim / reissue`

## Before / After — `Summilux-M 35`

### Before

From final safety smoke v1:

- interpreted target: `Leica Summilux-M 35 candidate`
- `price_summary_allowed = True`
- `price_scope = exact_base_model`
- visible used-for-price count: `7`
- used-for-price rows mixed materially different variants:
  - `Leica M 35mm f1.4 Summilux 2nd Titan`
  - `Leica M 35mm f1.4 Summilux ASPH 4th Titan`
  - `Leica M 35mm f1.4 Summilux 2nd Black`
  - `Leica M 35mm f1.4 Summilux ASPH 4th Silver`
  - `신품 Leica M 35mm f1.4 Summilux ASPH 6bit FLE II Black`
  - `Leica M 35mm f1.4 Summilux ASPH 4th 6bit Black`
  - `[중고] M 35/1.4 Summilux (스틸림 복각)`

### After

- interpreted target: `Leica Summilux-M 35 candidate`
- `price_summary_allowed = False`
- `price_scope = insufficient_exact_data`
- visible used-for-price count: `0`
- broad mixed rows remain visible, but are no longer used for exact price

## Exact Price Unlock Blocked?

- broad `Summilux-M 35` exact-base-model unlock: `Yes, blocked`
- mixed rows marked `used_for_price`: `No`
- body/lens broad exact unlock regression introduced: `No`

## Primary Validation

| query | interpreted target | price scope | exact price unlocked | visible used-for-price | result |
| --- | --- | --- | --- | ---: | --- |
| `Summilux-M 35` | `Leica Summilux-M 35 candidate` | `insufficient_exact_data` | `False` | `0` | PASS |

## Specific Variant Regression Table

| query | interpreted target | price scope | exact price unlocked | visible used-for-price | result |
| --- | --- | --- | --- | ---: | --- |
| `Summilux-M 35 ASPH` | `Leica Summilux-M 35 ASPH candidate` | `exact_variant` | `True` | `0` | PASS |
| `35 lux asph` | `Leica Summilux 35 ASPH candidate` | `exact_variant` | `True` | `0` | PASS |
| `Summilux-M 35 FLE` | `Leica Summilux-M 35 FLE candidate` | `insufficient_exact_data` | `False` | `0` | PASS |
| `35 lux fle` | `Leica Summilux 35 FLE candidate` | `insufficient_exact_data` | `False` | `0` | PASS |
| `Summilux-M 35 FLE2` | `Leica Summilux-M 35 FLE2 candidate` | `exact_variant` | `True` | `0` | PASS |
| `Summilux-M 35 FLE II` | `Leica Summilux-M 35 FLE2 candidate` | `exact_variant` | `True` | `0` | PASS |
| `Summilux-M 35 close focus` | `Leica Summilux-M 35 FLE2 candidate` | `exact_variant` | `True` | `0` | PASS |
| `Summilux-M 35 2매` | `Leica Summilux-M 35 AA candidate` | `insufficient_exact_data` | `False` | `0` | PASS |
| `Summilux-M 35 AA` | `Leica Summilux-M 35 AA candidate` | `insufficient_exact_data` | `False` | `0` | PASS |
| `Summilux-M 35 aspherical` | `Leica Summilux-M 35 AA candidate` | `insufficient_exact_data` | `False` | `0` | PASS |
| `Summilux 35 Steel Rim` | `Leica Summilux 35 Steel Rim candidate` | `insufficient_exact_data` | `False` | `0` | PASS |

## Broad Lens Safety Regression Table

| query | interpreted target | price scope | exact price unlocked | visible used-for-price | result |
| --- | --- | --- | --- | ---: | --- |
| `Summilux 35` | `Leica Summilux 35 candidate` | `insufficient_exact_data` | `False` | `0` | PASS |
| `Summicron 35` | `Leica Summicron 35 candidate` | `blocked_boundary_conflict` | `False` | `0` | PASS |
| `Summicron 50` | `Leica Summicron 50 candidate` | `insufficient_exact_data` | `False` | `0` | PASS |
| `Summicron-M 50` | `Leica Summicron-M 50 candidate` | `insufficient_exact_data` | `False` | `0` | PASS |
| `Noctilux 50` | `Leica Noctilux 50 candidate` | `insufficient_exact_data` | `False` | `0` | PASS |
| `Noctilux 50 1.2` | `Leica Noctilux 50 f1.2 candidate` | `blocked_boundary_conflict` | `False` | `0` | PASS |
| `APO Summicron SL 50` | `Leica APO-Summicron-SL 50 ASPH candidate` | `blocked_weak_only` | `False` | `0` | PASS |
| `Leica SL 50 APO Summicron` | `Leica APO-Summicron-SL 50 ASPH candidate` | `blocked_weak_only` | `False` | `0` | PASS |

## Recent Boundary Regression Table

| query | interpreted target | price scope | exact price unlocked | visible used-for-price | result |
| --- | --- | --- | --- | ---: | --- |
| `50 cron dr` | `Leica Summicron 50 Dual Range candidate` | `blocked_weak_only` | `False` | `0` | PASS |
| `Summicron-M 50 Dual Range` | `Leica Summicron-M 50 Dual Range candidate` | `exact_variant` | `True` | `0` | PASS |
| `Leica Summicron 50 rigid` | `Leica Summicron 50 Rigid candidate` | `insufficient_exact_data` | `False` | `0` | PASS |
| `Summicron-M 50 rigid` | `Leica Summicron-M 50 Rigid candidate` | `exact_variant` | `True` | `0` | PASS |
| `Leica LTM 50 Summicron rigid` | `Leica Summicron-L 50 Rigid candidate` | `exact_variant` | `True` | `0` | PASS |
| `Leica M10 lens kit` | `Leica M10 body` | `insufficient_exact_data` | `False` | `0` | PASS |
| `Leica M10 body lens kit` | `Leica M10 body` | `insufficient_exact_data` | `False` | `0` | PASS |
| `Leica Q2 with accessories` | `Leica Q2 body` | `insufficient_exact_data` | `False` | `0` | PASS |

## Remaining Issues

- `Summilux-M 35` broad query still shows mixed variant rows in the visible first screen.
- This is acceptable after the guard because those rows are no longer used for exact price.
- Any future improvement here should be treated as ranking polish, not a new price-scope safety fix.

## Validation Notes

- `python3 -m py_compile query_parser.py search_service.py query_resolver.py api/search.py` passed.
- Targeted local smoke passed for:
  - broad `Summilux-M 35`
  - specific Summilux 35 variant queries
  - broad lens safety queries
  - recent DR / Rigid / body-bundle guard regressions
