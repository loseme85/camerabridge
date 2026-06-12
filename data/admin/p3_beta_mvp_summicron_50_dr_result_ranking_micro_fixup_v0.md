# P3 Beta MVP Summicron 50 DR Result Ranking Micro Fixup v0

- branch: `beta-ui-redesign-controlled-preview`
- decision_status: `summicron_50_dr_result_ranking_micro_fixup_pushed_ready_for_owner_recheck`

## Files changed

- `/Users/changdaepark/Desktop/LEICA SEARCH/api/search.py`

## Exact parser changes

- None.
- Query parser behavior was left unchanged in this round.

## Exact ranking changes

- Added a narrow relevance-only re-rank for strong `Summicron 50` + `Dual Range` query context.
- Added a narrow expanded-pool promotion step so visible result cards can be drawn from the re-ranked 60-result evidence scan pool when explicit DR rows exist beyond the original first 12 results.

## Row-side DR ranking signals used

- `DR`
- `Dual Range`
- `dual-range`
- `dualrange`

## Narrow DR ranking behavior

For explicit `Dual Range` queries only:

- exact `DR` rows in M-side `Summicron 50` context are ranked first
- additional DR-signaled M-side rows are ranked next
- ordinary / rigid / APO / collapsible / LTM / wrong-mount rows are pushed lower
- L / R / SL rows are demoted beneath DR rows

This is applied only when:

- family root is `Summicron`
- focal length is `50`
- query variant includes `Dual Range`
- sort is `relevance`

## Before / after behavior

### Before

- `Summicron 50 DR`
- `Summicron 50 Dual Range`
- `Leica Summicron 50 DR`

often opened with L / R / rigid / ordinary rows in the first visible screen, while true DR rows stayed buried deeper in the expanded pool.

### After

These queries now start with DR rows such as:

- `Leica M 50mm f2 Summicron DR Silver`
- `[중고] M 50/2 Summicron DR (Silver)`
- `[위탁] M 50/2 Summicron DR (Silver)`

and those rows project as:

- `Evidence role: Exact variant`
- `Price role: Exact match visible, but not enough to unlock price yet`
  or existing duplicate / outlier / no-price states

## Owner-visible expectations

### `50 cron dr`

- DR rows now appear first
- first visible cards are exact DR candidates
- non-DR rows remain visible lower down and are not used as exact DR price unless existing logic allows it

### `Summicron 50 DR`

- DR rows now appear first instead of L / rigid rows dominating the first screen

### `Summicron 50 Dual Range`

- DR rows now appear first

### `Summicron-M 50 Dual Range`

- DR rows remain first
- exact DR price behavior remains intact

### `Leica Summicron 50 DR`

- DR rows now appear first

## Regression checks

Unchanged in narrow smoke:

- `Leica Summicron 50 rigid`
- `50 cron rigid`
- `Summicron 50 2nd`
- `Summicron-M 50`
- `Summicron 50 R`

Observed regression state remained acceptable:

- rigid query still surfaces rigid rows
- 2nd query still surfaces 2nd-generation rows
- broad `Summicron-M 50` stays mixed and conservative
- `Summicron 50 R` stays R-mount oriented

## Validation run

- `python3 -m py_compile /Users/changdaepark/Desktop/LEICA SEARCH/api/search.py`
- narrow DR smoke:
  - `50 cron dr`
  - `Summicron 50 DR`
  - `Summicron 50 Dual Range`
  - `Summicron-M 50 Dual Range`
  - `Leica Summicron 50 DR`
- regression smoke:
  - `Leica Summicron 50 rigid`
  - `50 cron rigid`
  - `Summicron 50 2nd`
  - `Summicron-M 50`
  - `Summicron 50 R`

## Remaining follow-up

- `Rigid` M vs LTM / M39 mount guard remains a separate follow-up and was intentionally not changed in this round.

## Commit / push

- commit: `bbbd0548421bc7b926c0958da7d4d1d401ad2cf0`
- push: success
