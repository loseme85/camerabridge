P3-BETA-MVP-M35-SUMMICRON-ASPH-ROW-LEVEL-EVIDENCE-ROLE-FIXUP

Branch: `beta-ui-redesign-controlled-preview`

Decision status:
`m35_summicron_asph_row_level_evidence_role_fixup_pushed_ready_for_owner_recheck`

## Files changed

- `api/search.py`

## Exact fix

Updated visible card evidence projection so `Evidence role` is computed from **row-level conflict / compatibility** instead of being overwritten by query-level `boundary_conflict_detected`.

What changed:

- `Market Entry` and `Query Review` still use query-level boundary conflict gating unchanged
- visible card `Evidence role` now checks each row for:
  - family conflict
  - mount conflict
  - category conflict
  - variant conflict
  - classification conflict
- only rows that truly conflict now get:
  - `Evidence role: Boundary conflict`

## Primary result

For query `Summicron-M 35 ASPH`:

- APO `M 35mm f2 APO-Summicron ASPH` rows remain `Boundary conflict`
- true non-APO `M 35/2 Summicron ASPH` rows now show `Exact variant`
- exact but excluded rows now display correctly as:
  - `Evidence role: Exact variant`
  - `Price role: Not used — Price outlier`
  - `Reason: Price outlier`
  or
  - `Evidence role: Exact variant`
  - `Price role: Not used — Duplicate listing`
  - `Reason: Duplicate listing`

This removes the confusing combination:

- `Evidence role: Boundary conflict`
- `Price role: Exact match visible, but not enough to unlock price yet`

for rows that are actually exact candidates.

## Narrow smoke results

### `Summicron-M 35 ASPH`

Examples after fix:

- `Leica M 35mm f2 APO-Summicron ASPH 6bit Black`
  - `Evidence role: Boundary conflict`
  - `Price role: Not used — not compatible with this query`

- `Leica M 35mm f2 Summicron ASPH Anthracite Finish`
  - `Evidence role: Exact variant`
  - `Price role: Not used — Price outlier`

- `[위탁] M 35/2 Summicron ASPH (Titan)`
  - `Evidence role: Exact variant`
  - `Price role: Exact match visible, but not enough to unlock price yet`

- `[중고] M 35/2 Summicron ASPH 6bit (Silver)`
  - exact sample row:
    - `Evidence role: Exact variant`
    - `Price role: Exact match visible, but not enough to unlock price yet`
  - duplicate row:
    - `Evidence role: Exact variant`
    - `Price role: Not used — Duplicate listing`

### Related query guards

- `Summicron-M 35`
  - broad non-APO rows now show `Exact base model`
  - true conflicts remain `Boundary conflict`

- `APO-Summicron-M 35 ASPH`
  - remains clean
  - APO rows stay `Exact variant`
  - non-APO rows remain `Boundary conflict`

- `Summicron-SL 35 ASPH apo`
  - unchanged
  - exact rows remain `Exact variant`

- `APO-Summicron-SL 50`
  - unchanged
  - ASPH rows remain `Exact variant`

- `35 lux aa`
  - unchanged in structure
  - no UI/grid regression from this fix

## What did not change

- parser
- ranking
- pricing thresholds
- duplicate policy
- price unlock rules
- Market Entry lock behavior
- Query Review boundary message
- result card layout
- query summary bar
- Load more
- 3-column grid

## Validation

- `python3 -m py_compile api/search.py` passed
- narrow search smoke run for:
  - `Summicron-M 35 ASPH`
  - `Summicron-M 35`
  - `APO-Summicron-M 35 ASPH`
  - `Summicron-SL 35 ASPH apo`
  - `APO-Summicron-SL 50`
  - `35 lux aa`

UI guard checks by inspection:

- query summary bar still present
- `Load more` hook still present
- result grid still capped at 3 columns
- 4-column grid did not return
- template mirror still in sync

