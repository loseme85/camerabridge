# Summilux 35 2mae AA Intent Recovery Fixup v0

- Branch: `beta-ui-redesign-controlled-preview`
- Decision status: `summilux_35_2mae_aa_intent_recovery_fixup_pushed_ready_for_owner_recheck`

## Exact changes

File changed:
- `/Users/changdaepark/Desktop/LEICA SEARCH/query_parser.py`

Narrow query-intent recovery added for strong `Summilux 35` shorthand:

1. In strong `Summilux 35` context, these explicit shorthand forms now recover AA intent:
   - `2매`
   - `2mae`
   - `2-mae`

2. Added a narrow shorthand recovery for compact query form:
   - `M35 1.4 2매`
   - and equivalent `M 35 1.4 2매` style

3. Recovery scope stays narrow:
   - only `Summilux 35`
   - blocks if query already says `ASPH`
   - blocks if query already says `FLE`
   - blocks if query already says `FLE2`
   - blocks if query already says `pre-ASPH`

No changes to:
- ordinary ASPH exactness
- FLE exactness
- FLE2 / FLE II / close focus exactness
- DR / Dual Range logic
- Rigid mount guard logic
- ranking
- duplicate / outlier policy
- UI

## Before / after: `Summilux-M 35 2매`

### Before
- detected candidate: `Leica Summilux-M 35 candidate`
- bad behavior: broad same-base price unlock
- mixed used-for-price rows included non-AA rows such as:
  - `Leica M 35mm f1.4 Summilux 2nd Titan`
  - `Leica M 35mm f1.4 Summilux ASPH 4th Titan`
  - `Leica M 35mm f1.4 Summilux 2nd Black`
  - `신품 Leica M 35mm f1.4 Summilux ASPH 6bit FLE II Black`

### After
- detected candidate: `Leica Summilux-M 35 AA candidate`
- query intent variant: `AA`
- price state: `Exact variant price data limited`
- price status: `Reference price only.`
- broad same-base unlock: **blocked**
- used-for-price visible rows: `0`
- top visible rows now start with AA-looking rows:
  - `[위탁] M 35/1.4 Summilux 3세대 (2매) (Black)`
  - `[중고] M 35/1.4 Summilux 3세대 (2매) (Black)`
  - `[중고] M35/1.4 Summilux 2매 (Black)`

## Same-base price unlock blocked?

Yes.

For:
- `Summilux-M 35 2매`
- `Summilux 35 2매`
- `35 lux 2mae`

current behavior is:
- no broad same-base price unlock
- no used-for-price visible rows
- AA / 2매 rows are the strongest compatible results
- price remains locked / reference-only when exact AA evidence is thin

## Validation table

| Query | Candidate after fix | Variant | Price behavior | Safe result |
|---|---|---|---|---|
| `Summilux-M 35 2매` | `Leica Summilux-M 35 AA candidate` | `AA` | `Exact variant price data limited` | No broad same-base unlock |
| `Summilux 35 2매` | `Leica Summilux 35 AA candidate` | `AA` | `Exact variant price data limited` | No broad same-base unlock |
| `M35 1.4 2매` | `Leica Summilux-M 35 f1.4 AA candidate` | `AA` | `Exact variant price data limited` | No broad same-base unlock |
| `35 lux 2mae` | `Leica Summilux 35 AA candidate` | `AA` | `Exact variant price data limited` | No broad same-base unlock |
| `Summilux-M 35 3rd gen 2mae` | `Leica Summilux-M 35 AA / 3rd candidate` | `AA` | `Exact variant price data limited` | stays conservative / locked |

## Healthy AA regression checks

All stayed healthy:
- `35 lux aa`
- `Summilux-M 35 AA`
- `Summilux-M 35 aspherical`
- `Summilux 35 aspherical`

Shared result:
- AA candidate text preserved
- `AA` variant preserved
- `Exact variant price data limited`
- no FLE / FLE2 / ordinary ASPH exact-price contamination found

## ASPH / FLE / FLE2 regression table

| Query | Result |
|---|---|
| `Summilux-M 35 ASPH` | still exact ASPH price |
| `35 lux asph` | still exact ASPH price |
| `Summilux-M 35 FLE` | still conservative / reference-only when mixed |
| `35 lux fle` | still conservative / reference-only when mixed |
| `Summilux-M 35 FLE2` | still exact FLE2 price |
| `Summilux-M 35 FLE II` | still exact FLE2 price |
| `Summilux-M 35 close focus` | still exact FLE2 price |

Observed safety:
- ordinary ASPH did not borrow FLE/FLE2/AA exact price
- FLE/FLE2 did not regress
- AA / 2매 queries did not contaminate ASPH / FLE / FLE2 exact price

## DR / Rigid spot checks

No regression found:

| Query | Result |
|---|---|
| `50 cron dr` | still `Dual Range`, still conservative / locked |
| `Summicron 50 DR` | still `Dual Range`, still conservative / locked |
| `Leica Summicron 50 rigid` | bare mixed-mount rigid still locked |
| `Summicron-M 50 rigid` | explicit M rigid still exact |
| `Leica LTM 50 Summicron rigid` | explicit LTM rigid still exact |

## Remaining issues

1. `Summilux-M 35 3rd gen 2mae`
   - now safely recovers AA intent
   - but still remains conservative and does not fully promote many rows into exact AA visible evidence
   - this is acceptable for now because it stays locked rather than unlocking the wrong band

2. `M35 1.4 2매`
   - now safely recovers to `Summilux-M 35 f1.4 AA candidate`
   - top rows are still a bit mixed visually because the shorthand is more compact than the other AA queries
   - price remains locked, so no P0 remains here
