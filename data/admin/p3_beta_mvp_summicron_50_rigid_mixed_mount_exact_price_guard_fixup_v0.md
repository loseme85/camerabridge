# P3 Beta MVP Summicron 50 Rigid Mixed Mount Exact Price Guard Fixup v0

- branch: `beta-ui-redesign-controlled-preview`
- decision_status: `summicron_50_rigid_mixed_mount_exact_price_guard_fixup_pushed_ready_for_owner_recheck`

## Files changed

- `/Users/changdaepark/Desktop/LEICA SEARCH/api/search.py`

## Exact change

- Added a narrow exact-price unlock guard for bare `Summicron 50 Rigid` queries.
- The guard only applies when:
  - family root is `Summicron`
  - focal length is `50`
  - query variant includes `Rigid`
  - query mount is unspecified

## Mixed-mount detection

- Added narrow M-side rigid row detection for strong `Summicron 50` context
- Added narrow L / LTM / M39-side rigid row detection for strong `Summicron 50` context
- If both mount families appear inside the exact rigid result set for a bare rigid query:
  - exact variant price does not unlock
  - mixed exact band is not shown
  - result cards remain visible
  - row evidence roles stay visible

## Owner-visible behavior after fix

### Bare rigid queries

- `Leica Summicron 50 rigid`
- `50 cron rigid`
- `Summicron 50 rigid`

Now show:

- `price_scope = insufficient_exact_data`
- `display_price_scope_label = Exact variant price data limited`
- `display_price_band = Exact variant price data limited`
- `display_price_band_quality_state = Mixed M / LTM-M39 rigid exact evidence`

Visible rows still show `Exact variant`, but no mixed exact price unlock happens.

### Explicit M rigid queries

- `Summicron-M 50 rigid`
- `Leica M 50 Summicron rigid`

Remain unchanged:

- M rigid rows stay exact
- exact price still unlocks
- exact band remains `KRW 2,400,000 - 2,800,000`

### Explicit LTM / M39 rigid queries

- `Leica LTM 50 Summicron rigid`
- `Leica M39 50 Summicron rigid`

Remain unchanged:

- L-side rigid rows stay exact
- exact price still unlocks
- exact band remains `KRW 3,500,000 - 4,230,000`

## DR regression check

Unchanged:

- `Summicron 50 DR`
- `50 cron dr`
- `Summicron 50 Dual Range`

DR rows remain `Exact variant`, and rigid rows do not enter DR exact price.

## Broad query regression check

Unchanged:

- `Summicron-M 50` remains conservative / locked
- `Summicron 50 R` remains R-mount behavior

## Validation run

- `python3 -m py_compile /Users/changdaepark/Desktop/LEICA SEARCH/api/search.py`
- narrow validation queries:
  - `Leica Summicron 50 rigid`
  - `50 cron rigid`
  - `Summicron 50 rigid`
  - `Summicron-M 50 rigid`
  - `Leica M 50 Summicron rigid`
  - `Leica LTM 50 Summicron rigid`
  - `Leica M39 50 Summicron rigid`
  - `Summicron 50 DR`
  - `50 cron dr`
  - `Summicron 50 Dual Range`
  - `Summicron-M 50`
  - `Summicron 50 R`

## What did not change

- query parser broad behavior
- ranking
- pricing thresholds
- duplicate policy
- outlier policy
- UI layout
- query summary bar
- Load more

## Commit / push

- commit: `b4075395ab137cb503799d0ee582b64d896dbfca`
- push: success
