P3-BETA-MVP-APO-SUMMICRON-SL-IMPLICIT-ASPH-ADD-50-FIXUP

Branch: `beta-ui-redesign-controlled-preview`

Decision status:
`apo_summicron_sl_implicit_asph_add_50_fixup_pushed_ready_for_owner_recheck`

## Files changed

- `api/search.py`

## Exact change

Expanded the narrow implicit `ASPH` exactness focal allowlist for `APO-Summicron-SL` from:

- `{35, 75, 90}`

to:

- `{35, 50, 75, 90}`

This change applies only when:

- `model_family = APO-Summicron-SL`
- `mount = SL`
- query focal length is in the allowlist
- query variant is empty

No other family or mount path changed.

## What changed in behavior

### `APO-Summicron-SL 50`

Before:

- runtime variant exactness did not add implicit `ASPH`
- visible `SL 50/2 APO Summicron ASPH` rows stayed `Same base model`

After:

- runtime `variant_tokens_detected = ['ASPH']`
- visible `SL 50/2 APO Summicron ASPH` rows classify as `Exact variant`
- current top visible rows still show:
  - `Price role: Exact match visible, but not enough to unlock price yet`

This preserves price safety while fixing exactness classification.

## Guard behavior preserved

- `APO-Summicron-SL 35`: unchanged, still implicit `ASPH`
- `APO-Summicron-SL 75`: unchanged, still implicit `ASPH`
- `APO-Summicron-SL 90`: unchanged, still implicit `ASPH`
- `APO-Summicron-SL 28`: unchanged, still no implicit `ASPH`
- `APO-Summicron-SL 21`: unchanged, still held
- `APO-Summicron-SL 50 ASPH`: unchanged explicit variant path
- `Summicron-SL 50 ASPH apo`: unchanged APO-SL path
- `APO-Summicron-M 35 ASPH`: unchanged
- `Summicron-M 35`: unchanged
- `Summicron-M 35 ASPH`: unchanged

## Pricing / evidence safety

No pricing thresholds changed.

Confirmed after fix:

- active asking rows still do not become sold exact-price evidence automatically
- duplicate rows still show `Not used — Duplicate listing`
- outlier rows still show `Not used — Price outlier`
- no-price rows still show `No usable price`

Examples seen in smoke:

- `APO-Summicron-SL 90`
  - duplicate exact row still shows `Not used — Duplicate listing`
- `Summicron-M 35 ASPH`
  - outlier row still shows `Not used — Price outlier`

## Validation run

- `python3 -m py_compile api/search.py` passed
- narrow runtime smoke passed for:
  - `APO-Summicron-SL 35`
  - `APO-Summicron-SL 50`
  - `APO-Summicron-SL 75`
  - `APO-Summicron-SL 90`
  - `APO-Summicron-SL 28`
  - `APO-Summicron-SL 21`
  - `APO-Summicron-SL 50 ASPH`
  - `Summicron-SL 50 ASPH apo`
  - `APO-Summicron-M 35 ASPH`
  - `Summicron-M 35`
  - `Summicron-M 35 ASPH`

Template/UI guard checks by inspection:

- visible card evidence projection hooks unchanged
- `Load more` hook still present
- result grid still capped at 3 columns

## What did not change

- parser output
- ranking
- pricing thresholds
- duplicate policy
- UI layout
- visible card evidence projection logic
- Load more behavior
- 3-column max result grid

