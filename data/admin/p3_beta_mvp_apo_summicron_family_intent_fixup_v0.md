# P3-BETA-MVP-APO-SUMMICRON-FAMILY-INTENT-FIXUP

## Scope
- Branch: `beta-ui-redesign-controlled-preview`
- Goal: upgrade standalone `apo` into APO-Summicron family intent only in strong Summicron + M/SL query contexts

## Files changed
- `/Users/changdaepark/Desktop/LEICA SEARCH/query_parser.py`
- `/Users/changdaepark/Desktop/LEICA SEARCH/data/admin/p3_beta_mvp_apo_summicron_family_intent_fixup_v0.md`

## Exact parser change
Added a narrow parser-side recovery pass:
- if query contains standalone `apo`
- and parsed family is `Summicron`
- and parsed mount is `M` or `SL`
- then upgrade:
  - `Summicron` + `M` -> `APO-Summicron-M`
  - `Summicron` + `SL` -> `APO-Summicron-SL`

This recovery:
- does not run for bare `apo`
- does not run for non-Summicron families
- does not infer `M` or `SL` by itself
- does not change explicit APO hyphen queries that already work

Also:
- consumed `apo` is removed from `unknown` tokens when the upgrade succeeds

## Before / after

### `Summicron-M 35 ASPH apo`
- before:
  - parsed family `Summicron`
  - `apo` remained `unknown`
  - expected family `Summicron-M`
- after:
  - parsed family `APO-Summicron-M`
  - expected family `APO-Summicron-M`

### `35 apo summicron m`
- before:
  - parsed family `Summicron`
  - expected family drifted via runtime text hints
- after:
  - parsed family `APO-Summicron-M`
  - expected family `APO-Summicron-M`

### `apo summicron m 35`
- before:
  - parsed family `Summicron`
- after:
  - parsed family `APO-Summicron-M`

### `Summicron-SL 35 ASPH apo`
- before:
  - parsed family `Summicron`
  - non-APO SL rows could be `Exact variant / Used for exact price`
- after:
  - parsed family `APO-Summicron-SL`
  - APO SL rows are exact
  - non-APO SL rows are not compatible

## Preserved behavior
- `APO-Summicron-M 35 ASPH` stays correct
- `APO-Summicron-SL 35` stays correct
- `APO-Summicron-SL 90` stays correct
- `Summicron-M 35 ASPH` stays non-APO
- `Summicron-SL 35 ASPH` stays non-APO
- `Summicron 35 ASPH` stays non-APO
- bare `apo` still does not create a family

## Validation
- `python3 -m py_compile query_parser.py`

### Parser smoke
- `Summicron-M 35 ASPH apo` -> `APO-Summicron-M`
- `APO-Summicron-M 35 ASPH` -> unchanged
- `35 apo summicron m` -> `APO-Summicron-M`
- `apo summicron m 35` -> `APO-Summicron-M`
- `Summicron-SL 35 ASPH apo` -> `APO-Summicron-SL`
- `APO-Summicron-SL 35` -> unchanged
- `APO-Summicron-SL 90` -> unchanged
- `Summicron-M 35 ASPH` -> unchanged non-APO
- `Summicron-SL 35 ASPH` -> unchanged non-APO
- `Summicron 35 ASPH` -> unchanged non-APO
- `apo` -> still no family

### Search smoke
Most important corrected path:
- `Summicron-SL 35 ASPH apo`
  - before:
    - non-APO SL rows could be `Exact variant`
    - `Used for exact price`
  - after:
    - APO SL rows -> `Exact variant`
    - non-APO SL rows no longer used as exact price evidence
    - price status now remains conservative:
      - `Reference price only.`
      - `No exact strong visible listings yet.`

Also corrected:
- `Summicron-M 35 ASPH apo`
  - APO M rows are exact
  - non-APO M rows are incompatible

## What did not change
- ranking
- pricing logic
- price unlock thresholds
- result card UI
- Model Market Entry UI
- Load more
- grid

## Final decision_status
`apo_summicron_family_intent_fixup_pushed_ready_for_owner_recheck`
