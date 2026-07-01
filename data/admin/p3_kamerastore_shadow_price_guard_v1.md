# P3 Kamerastore Shadow Price Guard v1

## Executive Summary

- Scope: Kamerastore-only shadow price guard
- Current source status: `limited_crawl`
- Current source policy: `blocked_initially`
- Live pricing behavior remains unchanged
- Kamerastore rows are still **not** used for actual price evidence

This round adds a Kamerastore-only shadow guard in `api/search.py` so we can:

1. compute row-level guard status and exclusion reasons
2. reproduce the previously audited `allowed_candidate / excluded_candidate` split
3. keep `used_for_price = False` in the actual price evidence path
4. avoid changing active source behavior

Final judgment for this task: **PASS**

Promotion judgment for Kamerastore itself:

- `allowed_after_validation`: **not yet**

## 수정 파일 목록

- `api/search.py`
- `data/admin/p3_kamerastore_shadow_price_guard_v1.md`

## Exact Change

Added a Kamerastore-only shadow layer with three pieces:

1. **Source policy-aware activation**
   - shadow guard activates only for source name `Kamerastore`
   - and only while source policy is `blocked_initially`

2. **Row-level shadow annotation**
   - each visible Kamerastore result can now carry:
     - `shadow_price_guard_status`
     - `shadow_exclusion_reasons`
     - `shadow_duplicate_cluster_size`
     - `shadow_duplicate_cluster_representative`
     - `shadow_duplicate_cluster_representative_eligible`
     - `shadow_price_evidence_live_applied = False`

3. **Top-level QA summary**
   - response now includes:
     - `shadow_price_guard.kamerastore.allowed_candidate_count`
     - `shadow_price_guard.kamerastore.excluded_candidate_count`
     - exclusion reason counts
     - duplicate cluster counts

Important:

- this does **not** change the existing live price evidence pool
- it does **not** make Kamerastore price-eligible
- it does **not** change ranking, parser, alias, canonical, or production/preview deployment

## Guard Rule 목록

### 1. Accessory hard block

Excluded when:

- `category == Accessory`
- or title contains one of:
  - `hood`
  - `adapter`
  - `grip`
  - `handgrip`
  - `thumb`
  - `case`
  - `strap`
  - `filter`
  - `cap`
  - `battery`
  - `charger`
  - `meter`

### 2. Bundle hard block

Excluded when title contains:

- ` + `
- `kit`
- `bundle`
- `set`
- `with`

### 3. Missing canonical block

Excluded when:

- `model_canonical` is missing

### 4. Classification drift block

Excluded when title looks body-like but resolved category is not `Body`.

High-signal body-like checks include:

- `Monochrom`
- `M Typ 240`
- `M Typ 262`
- `M-E`
- `MDa`
- `Q2`
- `M4 / M5 / M7 / M8 / M9 / M10 / M11`
- `Leicaflex`
- `Standard (Model ...)`

### 5. Duplicate cluster suppression metadata

Cluster key:

- `(title_raw, model_canonical, condition_raw)`

Behavior:

- strict row-level shadow replay still reproduces the prior audit counts
- duplicate rows are marked with `duplicate`
- one cluster representative is still identified for QA review
- representative rows are marked separately via:
  - `shadow_duplicate_cluster_representative`
  - `shadow_duplicate_cluster_representative_eligible`

## Kamerastore Shadow Allowed / Excluded Count

Current full-source shadow summary:

- `row_count = 106`
- `allowed_candidate_count = 70`
- `excluded_candidate_count = 36`

These counts reproduce the prior guard audit split.

## Exclusion Reason별 Count

Overlapping reason counts:

- `accessory = 10`
- `bundle = 13`
- `classification_drift = 4`
- `duplicate = 20`
- `missing_canonical = 10`

Notes:

- `classification_drift = 4` in the implemented shadow pass because repeated `M Monochrom` rows each carry the drift signal
- no `suspicious_price` rows were found in the current snapshot

## Duplicate Cluster 처리 결과

Duplicate summary:

- `duplicate_cluster_count = 9`
- `duplicate_cluster_row_count = 20`
- `duplicate_cluster_representative_count = 6`

Representative examples:

1. `Leica Q2 Monochrom (19055)`
   - representative found
   - representative eligible: `True`
   - strict shadow status still remains `excluded_candidate` because duplicate replay is preserved

2. `Leica 50mm f2 Summicron-M (Type IV) (Black, 11819)`
   - representative found
   - representative eligible: `True`

3. `Leica 35mm f2 Summicron (Type III) (11309)`
   - representative found
   - representative eligible: `True`

Non-clean representative examples:

1. `Leica M Monochrom (Black, 10760)`
   - representative found
   - representative eligible: `False`
   - reasons:
     - `classification_drift`
     - `duplicate`
     - `missing_canonical`

2. `Leica M (Typ 240) (Black Paint, 10770)`
   - representative found
   - representative eligible: `False`
   - reasons:
     - `duplicate`
     - `missing_canonical`

## Classification Drift 처리 결과

Classification drift rows currently caught:

1. `Leica M Monochrom (Black, 10760)`  
   - two rows
   - shadow reasons:
     - `classification_drift`
     - `duplicate`
     - `missing_canonical`

2. `Leica MDa (10103)`  
   - shadow reasons:
     - `accessory`
     - `classification_drift`

3. `Leica M-E (Typ 220) (10759)`  
   - shadow reasons:
     - `classification_drift`
     - `missing_canonical`

Interpretation:

- the shadow guard catches the specific body-family drift cases we were worried about
- these rows remain blocked from any future price-evidence consideration until canonical/classification cleanup happens

## Representative Query Shadow 결과

### Leica 50mm Summicron-M Type IV

- visible Kamerastore rows present
- representative Type IV row shows:
  - `shadow_price_guard_status = allowed_candidate`
- actual visible evidence still shows:
  - `used_for_price = False`
  - `price_usage_label = Not used — Current source is not price-eligible yet`

### Leica 35mm Summicron

- duplicate `35mm Summicron (Type III)` rows are marked:
  - `shadow_price_guard_status = excluded_candidate`
  - `shadow_exclusion_reasons = ['duplicate']`
- `35mm Summicron-M (Type IV)` remains `allowed_candidate`

### Leica M Monochrom

- `Leica M Monochrom (Black, 10760)` is marked:
  - `shadow_price_guard_status = excluded_candidate`
  - `shadow_exclusion_reasons = ['classification_drift', 'duplicate', 'missing_canonical']`

### Leica M4

- clean `Leica M4 (Silver, 10400)` row:
  - `allowed_candidate`
- `Leica M4 ... + Meter MR` row:
  - `excluded_candidate`
  - reasons:
    - `accessory`
    - `bundle`

### Leica M Typ 240

- `Leica M-P (Typ 240) (Silver, 10772)`:
  - `allowed_candidate`
- `Leica M (Typ 240) (Black Paint, 10770)`:
  - `excluded_candidate`
  - reasons:
    - `duplicate`
    - `missing_canonical`

### Leica Q2

- `Leica Q2 (Daniel Craig x Greg Williams)`:
  - `allowed_candidate`
- `Leica Q2 Monochrom (19055)`:
  - `excluded_candidate`
  - reason:
    - `duplicate`

### Leica Elmarit-R

- clean lens rows remain `allowed_candidate`
- bundle/accessory-attached row remains `excluded_candidate`

### Leica hood / Leica adapter / Leica handgrip

- all visible Kamerastore rows remain `excluded_candidate`
- typical reasons:
  - `accessory`
  - `bundle`

## 실제 Price Evidence에 반영되지 않았는지 확인

Verified through `display_visible_result_evidence`:

- Kamerastore visible rows still show:
  - `used_for_price = False`
- typical live label remains:
  - `Not used — Current source is not price-eligible yet`

Examples:

1. `Leica 35mm f2 Summicron (Type III) (11309)`
   - `used_for_price = False`
   - `price_usage_label = Not used — Current source is not price-eligible yet`

2. `Leica Q2 (Daniel Craig x Greg Williams) (19058 / 19062)`
   - `used_for_price = False`
   - `price_usage_label = Not used — Current source is not price-eligible yet`

3. `Leica 135mm f2.8 Elmarit-R (Type I) (1-Cam) (11111)`
   - `used_for_price = False`
   - `price_usage_label = Not used — Current source is not price-eligible yet`

So the new shadow layer does not leak into live price summaries.

## Existing Active Source Regression 결과

Smoke checks run:

- `Leica M10`
- `Leica M11-P`
- `Leica 50 Summicron Rigid`
- `Leica Noctilux 0.95`

Observed:

- all queries still returned normal top results from existing active sources
- top result sources remained existing active sources such as `사진집`
- no Kamerastore promotion happened
- no active source pricing behavior changed

Regression result: **PASS**

## Allowed-After-Validation 가능 여부 판단

Current answer: **not yet**

Why:

- shadow guard itself now works
- but source promotion still needs:
  - row-level classification cleanup for body-family drift
  - duplicate strategy refinement if Kamerastore ever enters real price evidence
  - canonical completion for missing model rows

In other words:

- this task PASSes
- Kamerastore price-evidence promotion still remains future work

## 실행한 검증

1. no-write syntax check
   - `compile()` on `api/search.py`

2. full-source shadow snapshot
   - loaded current compact index
   - executed `_build_kamerastore_shadow_price_guard_snapshot(...)`

3. representative query checks
   - `Leica 50mm Summicron-M Type IV`
   - `Leica 35mm Summicron`
   - `Leica M Monochrom`
   - `Leica M4`
   - `Leica M Typ 240`
   - `Leica Q2`
   - `Leica Elmarit-R`
   - `Leica hood`
   - `Leica adapter`
   - `Leica handgrip`

4. regression smoke
   - `Leica M10`
   - `Leica M11-P`
   - `Leica 50 Summicron Rigid`
   - `Leica Noctilux 0.95`

## Final Judgment

**PASS**

Because:

- the Kamerastore-only shadow guard runs stably
- `allowed_candidate / excluded_candidate` split is reproduced as `70 / 36`
- row-level exclusion reasons are attached without changing live pricing
- actual price evidence still does not use Kamerastore
- existing active source behavior remains intact
