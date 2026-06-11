# P3-BETA-MVP-IMPLICIT-ASPH-EXACTNESS-FIXUP

## Scope
- Branch: `beta-ui-redesign-controlled-preview`
- Goal: treat `ASPH` as an implicit exactness signal only for narrow Leica `APO-Summicron-SL` queries

## Files changed
- `/Users/changdaepark/Desktop/LEICA SEARCH/api/search.py`
- `/Users/changdaepark/Desktop/LEICA SEARCH/data/admin/p3_beta_mvp_implicit_asph_exactness_fixup_v0.md`

## Exact change
Added a narrow implicit exactness rule inside query-side variant signal construction.

If query intent has:
- `model_family = APO-Summicron-SL`
- `mount = SL`
- `focal_length in {'35', '75', '90'}`
- no explicit variant tokens

then runtime now adds implicit query-side exactness signal:
- `ASPH`

This affects exact-variant matching only.

## What did not change
- parser output remains unchanged
- mount inference unchanged
- ranking unchanged
- pricing thresholds unchanged
- duplicate policy unchanged
- UI layout unchanged
- visible card evidence projection logic unchanged

## Before / after

### `APO-Summicron-SL 35`
- before:
  - `variant_tokens_detected = []`
  - visible `SL 35/2 APO Summicron ASPH` rows were `Same base model`
- after:
  - `variant_tokens_detected = ['ASPH']`
  - visible APO-SL 35 ASPH rows are `Exact variant`

### `APO-Summicron-SL 90`
- before:
  - APO SL 90 ASPH rows were only same-base unless query explicitly said `ASPH`
- after:
  - ASPH rows classify as `Exact variant`
  - non-ASPH `SL 90/2 APO-Summicron` rows can still remain same-base if title lacks ASPH

### `APO-Summicron-SL 75`
- after:
  - ASPH rows classify as `Exact variant` when matching rows exist
  - no-price rows remain `No usable price`

## Preserved behavior
- `APO-Summicron-SL 35 ASPH` unchanged
- `Summicron-SL 35 ASPH apo` unchanged
- `APO-Summicron-M 35 ASPH` unchanged
- `Summicron-M 35` does not gain implicit ASPH
- `Summicron-M 35 ASPH` unchanged

## Validation
- `python3 -m py_compile api/search.py` passed

### Parser smoke
Confirmed parser output itself is unchanged for:
- `APO-Summicron-SL 35`
- `APO-Summicron-SL 35 ASPH`
- `APO-Summicron-SL 75`
- `APO-Summicron-SL 90`
- `Summicron-SL 35 ASPH apo`
- `APO-Summicron-M 35 ASPH`
- `Summicron-M 35`
- `Summicron-M 35 ASPH`

### Search/runtime smoke

#### `APO-Summicron-SL 35`
- `variant_tokens_detected = ['ASPH']`
- visible APO-SL 35 ASPH rows now:
  - `role = Exact variant`
  - `compat = Exact variant`
  - `price = Exact match visible, but not enough to unlock price yet`

#### `APO-Summicron-SL 35 ASPH`
- unchanged exact-variant behavior

#### `APO-Summicron-SL 75`
- implicit ASPH applies
- exact ASPH rows become `Exact variant`
- rows without usable price remain `No usable price`

#### `APO-Summicron-SL 90`
- `variant_tokens_detected = ['ASPH']`
- ASPH rows become `Exact variant`
- top row without explicit ASPH in title can still remain same-base, which is acceptable under the current row text

#### `Summicron-SL 35 ASPH apo`
- unchanged

#### `APO-Summicron-M 35 ASPH`
- unchanged

#### `Summicron-M 35`
- unchanged, still no implicit ASPH

#### `Summicron-M 35 ASPH`
- unchanged

## Template / UI guard checks
- visible card evidence projection still present
- `Load more` hook still present
- 4-column result grid did not return

## Result
This fix narrows the exactness gap without changing parser output or pricing thresholds.
It only upgrades exact-variant matching where Leica `APO-Summicron-SL 35/75/90` naming strongly implies `ASPH`.

## Final decision_status
`implicit_asph_exactness_fixup_pushed_ready_for_owner_recheck`
