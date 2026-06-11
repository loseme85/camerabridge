# P3-BETA-MVP-VISIBLE-CARD-EVIDENCE-PROJECTION-FIXUP

## Scope
- Branch: `beta-ui-redesign-controlled-preview`
- Goal: make visible result cards transparent and consistent without changing pricing, ranking, parser, or duplicate policy

## Files changed
- `/Users/changdaepark/Desktop/LEICA SEARCH/api/search.py`
- `/Users/changdaepark/Desktop/LEICA SEARCH/app/templates/index.html`
- `/Users/changdaepark/Desktop/LEICA SEARCH/index.html`

## Exact changes

### 1. Visible-card evidence projection is no longer top-5 only
- kept existing `display_top_result_evidence` for Query Review
- added `display_visible_result_evidence` for the full visible result slice
- evidence is now projected for every visible card in the current response page

### 2. Card evidence join is row-level, not loose title-only
- each projected evidence item now includes:
  - `result_index`
  - `evidence_signature`
  - `currency`
- result cards now resolve evidence by:
  1. `result_index`
  2. signature fallback

This avoids many title-collision problems for repeated Leica rows.

### 3. Generic `Reference / not exact` fallback removed
- cards no longer fall back to:
  - `Reference / not exact`
- fallback is now:
  - `Visible result, not classified for pricing yet`
  - or `No usable price`

### 4. Duplicate / outlier / no-price states surface clearly
- duplicate-excluded cards now show:
  - `Price role: Not used — Duplicate listing`
  - `Reason: Duplicate listing`
- outlier-excluded cards now show:
  - `Price role: Not used — Price outlier`
  - `Reason: Price outlier`
- rows without usable prices now show:
  - `Price role: No usable price`
  - `Reason: Not used for market estimate`

## Focus smoke results

### `Summicron-M 35 ASPH`
- visible evidence count: `12`
- top evidence count: `5`
- previously unresolved visible cards now carry row-level evidence
- examples:
  - `Leica M 35mm f2 Summicron ASPH Anthracite Finish`
    - `Price role: Not used — Price outlier`
    - `Reason: Price outlier`
  - `[중고] M 35/2 Summicron ASPH Hammertone LHSA`
    - `Price role: Not used — Price outlier`
    - `Reason: Price outlier`
  - `[중고] M 35/2 Summicron ASPH 6bit (Silver) 복각`
    - `Price role: Not used — Price outlier`
    - `Reason: Price outlier`

### `Summicron-SL 35 ASPH apo`
- visible evidence count: `12`
- duplicate-excluded rows are now explicit
- examples:
  - repeated `[중고] SL 35/2 APO Summicron ASPH (Black)` rows
    - some remain:
      - `Evidence role: Exact variant`
      - `Price role: Exact match visible, but not enough to unlock price yet`
    - repeated duplicate rows now show:
      - `Price role: Not used — Duplicate listing`
      - `Reason: Duplicate listing`

### `APO-Summicron-SL 35`
- same-base APO rows now project consistently across the visible slice
- repeated duplicates now show `Not used — Duplicate listing`

### `APO-Summicron-M 35 ASPH`
- exact APO rows project consistently
- incompatible non-APO or wrong-family rows now keep explicit `Not used — not compatible with this query`

## What stayed unchanged
- pricing calculation
- price unlock thresholds
- duplicate detection policy
- parser
- ranking
- result card layout
- Load more behavior
- 3-column grid cap
- Model Market Entry logic
- Query Review logic

## Validation
- `python3 -m py_compile api/search.py` passed
- narrow search smoke passed for:
  - `Summicron-M 35 ASPH`
  - `Summicron-SL 35 ASPH apo`
  - `APO-Summicron-SL 35`
  - `APO-Summicron-M 35 ASPH`
- template mirror check passed:
  - `app/templates/index.html == index.html`
- template smoke checks passed:
  - visible evidence projection present
  - `Reference / not exact` fallback removed
  - `Load more` hook still present
  - 4-column result-grid breakpoint did not return

## Commit / push
- pending in this report until commit step completes

## Final decision_status
`visible_card_evidence_projection_fixup_pushed_ready_for_owner_recheck`
