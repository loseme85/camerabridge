# P3 Kamerastore Classification / Duplicate Cleanup v1

## Executive Summary

- Scope: scoped Kamerastore-only shadow cleanup
- Live Kamerastore price evidence policy remains `blocked_initially`
- Kamerastore is still **not** used in actual price summary / used_for_price
- No preview/prod deploy
- No broad ranking/parser/alias refactor

This round improved the Kamerastore shadow layer by:

1. fixing shadow-only body-family classification for key Leica body rows
2. filling missing shadow canonical values for key Leica body families
3. defining a stable duplicate representative strategy for QA review
4. keeping live price evidence unchanged

High-level result:

- before: `allowed_candidate = 70`, `excluded_candidate = 36`
- after: `allowed_candidate = 75`, `excluded_candidate = 31`
- classification drift: `4 -> 0`
- missing canonical: `10 -> 1`
- duplicate representative count: `6 -> 8`

Final judgment: **PASS**

## 수정 파일 목록

- `api/search.py`
- `data/admin/p3_kamerastore_classification_duplicate_cleanup_v1.md`

## 고친 Classification / Canonical 케이스

The cleanup is shadow-only and scoped to Kamerastore rows.

### 1. Leica M Monochrom (Black, 10760)

Before:

- category: `Lens`
- model_canonical: `None`
- shadow reasons:
  - `classification_drift`
  - `duplicate`
  - `missing_canonical`

After:

- shadow effective category: `Body`
- shadow effective model: `M Monochrom`
- remaining shadow reason:
  - `duplicate`

### 2. Leica M-E (Typ 220) (10759)

Before:

- category: `Lens`
- model_canonical: `None`
- shadow reasons:
  - `classification_drift`
  - `missing_canonical`

After:

- shadow effective category: `Body`
- shadow effective model: `M-E`
- shadow status:
  - `allowed_candidate`

### 3. Leica M (Typ 262) (10947)

Before:

- category: `Lens`
- model_canonical: `None`
- shadow reason:
  - `missing_canonical`

After:

- shadow effective category: `Body`
- shadow effective model: `M (Typ 262)`
- shadow status:
  - `allowed_candidate`

### 4. Leica M (Typ 240) (Black Paint, 10770)

Before:

- category: `Body`
- model_canonical: `None`
- shadow reasons:
  - `duplicate`
  - `missing_canonical`

After:

- shadow effective category: `Body`
- shadow effective model: `M (Typ 240)`
- remaining shadow reason:
  - `duplicate`

### 5. Leica MDa (Slotted Baseplate) (10913)

Before:

- category: `Accessory`
- model_canonical: `MDa`
- shadow reasons:
  - `accessory`
  - `classification_drift`

After:

- shadow effective category: `Body`
- shadow effective model: `MDa`
- shadow status:
  - `allowed_candidate`

### 6. Leica Q2 Monochrom (19055)

Before:

- category: `Body`
- model_canonical: `Q2`

After:

- shadow effective category: `Body`
- shadow effective model: `Q2 Monochrom`
- duplicate handling still applies

### 7. Small extra body-family canonical fills

Also filled in shadow-only:

- `Leica T (Typ 701)` -> `T (Typ 701)`
- `Leica S (Typ 007)` -> `S (Typ 007)`

## 아직 막아야 하는 케이스

These rows still should not move into live price evidence:

1. duplicate clusters
   - still excluded in strict row-level shadow replay

2. bundle / accessory rows
   - examples:
     - `Leica M4 ... + Meter MR`
     - `Leica M8 ... + Handgrip`
     - `... + Lens Hood`
     - `... + Adapter`

3. remaining missing canonical row
   - the remaining missing canonical item is accessory-side and should stay blocked

4. live price evidence
   - Kamerastore still remains source-policy blocked

## Duplicate Representative 전략

Representative selection is now explicit:

1. prefer rows that are shadow-clean before duplicate exclusion
2. then prefer stronger condition
   - `Certified` > `Restored` > `Not Passed`
3. then prefer later `crawl_time`
4. then fall back to stable `source_url`

Important:

- strict row-level shadow replay still marks all rows in duplicate clusters as `duplicate`
- the representative is for QA review / explanation only
- this keeps the duplicate risk visible while still letting us identify the best candidate in each cluster

Representative strategy string is exposed in shadow summary:

- `prefer shadow-clean rows, then stronger condition, then latest crawl_time, then stable source_url`

## Before / After Shadow Summary

### Before

- `allowed_candidate_count = 70`
- `excluded_candidate_count = 36`
- `exclusion_reason_counts`
  - `accessory = 10`
  - `bundle = 13`
  - `classification_drift = 4`
  - `duplicate = 20`
  - `missing_canonical = 10`
- `duplicate_cluster_count = 9`
- `duplicate_cluster_row_count = 20`
- `duplicate_cluster_representative_count = 6`

### After

- `allowed_candidate_count = 75`
- `excluded_candidate_count = 31`
- `exclusion_reason_counts`
  - `accessory = 9`
  - `bundle = 13`
  - `duplicate = 20`
  - `missing_canonical = 1`
- `classification_drift = 0`
- `duplicate_cluster_count = 9`
- `duplicate_cluster_row_count = 20`
- `duplicate_cluster_representative_count = 8`

## Allowed / Excluded 변화

- `allowed_candidate: 70 -> 75`
- `excluded_candidate: 36 -> 31`

Rows effectively recovered into shadow-allowed state include:

- `Leica M-E (Typ 220) (10759)`
- `Leica M (Typ 262) (10947)`
- `Leica MDa (Slotted Baseplate) (10913)`
- body-family canonical-filled rows such as `M Typ 240` no longer lose eligibility for missing canonical alone

## Classification Drift 변화

- before: `4`
- after: `0`

Most important improvement:

- `Leica M Monochrom`
- `Leica M-E`
- `Leica MDa (Slotted Baseplate)`

no longer show shadow classification drift.

## Missing Canonical 변화

- before: `10`
- after: `1`

Most important improvement:

- `Leica M Monochrom` now shadows to `M Monochrom`
- `Leica M-E` now shadows to `M-E`
- `Leica M (Typ 240)` now shadows to `M (Typ 240)`
- `Leica M (Typ 262)` now shadows to `M (Typ 262)`
- `Leica Q2 Monochrom` now shadows to `Q2 Monochrom`

## Representative Query 결과

### Leica M Monochrom

Observed:

- `Leica M Monochrom (Black, 10760)`
  - shadow effective category: `Body`
  - shadow effective model: `M Monochrom`
  - shadow status: `excluded_candidate`
  - remaining reason: `duplicate`
  - representative eligible: `True`

### Leica M-E

Observed:

- `Leica M-E (Typ 220) (10759)`
  - shadow effective category: `Body`
  - shadow effective model: `M-E`
  - shadow status: `allowed_candidate`

### Leica M Typ 240

Observed:

- `Leica M (Typ 240) (Black Paint, 10770)`
  - shadow effective category: `Body`
  - shadow effective model: `M (Typ 240)`
  - shadow status: `excluded_candidate`
  - reason: `duplicate`

### Leica Q2

Observed:

- `Leica Q2 (Daniel Craig x Greg Williams)`:
  - `allowed_candidate`
- `Leica Q2 Monochrom (19055)`:
  - shadow model now `Q2 Monochrom`
  - remaining reason: `duplicate`

### Leica 50mm Summicron-M Type IV

Observed:

- at least one visible Type IV row remains `allowed_candidate`
- duplicate siblings remain `excluded_candidate`

### Leica 35mm Summicron

Observed:

- one `35mm Summicron (Type III)` row is representative-eligible duplicate
- `35mm Summicron-M (Type IV)` remains `allowed_candidate`

## Live Price Evidence 미반영 확인

Confirmed:

- Kamerastore rows still show `used_for_price = False`
- live price labels still say variants of:
  - `Not used — Current source is not price-eligible yet`
- no existing active source price evidence behavior was changed

## Existing Source Regression 결과

Smoke queries checked:

- `Leica M10`
- `Leica M11-P`
- `Leica 50 Summicron Rigid`
- `Leica Noctilux 0.95`

Observed:

- top results still came from existing active sources such as `사진집`
- `kamerastore_live_price_used = False` remained true across checks
- no active source pricing regression was observed

Regression result: **PASS**

## Allowed-After-Validation 승급 가능 여부

Current answer: **still PENDING**

Why:

- shadow classification/canonical quality improved materially
- but duplicate clusters are still present and still intentionally excluded in strict row-level shadow replay
- bundle/accessory contamination still exists
- live source policy must remain `blocked_initially`

So this round improves readiness, but does not yet justify source promotion.

## 실행한 검증

1. no-write syntax check
   - `compile()` on `api/search.py`

2. full-source shadow summary recompute
   - `row_count`
   - `allowed_candidate_count`
   - `excluded_candidate_count`
   - `exclusion_reason_counts`
   - `duplicate_cluster_*`

3. representative query checks
   - `Leica M Monochrom`
   - `Leica M-E`
   - `Leica M Typ 240`
   - `Leica Q2`
   - `Leica 50mm Summicron-M Type IV`
   - `Leica 35mm Summicron`

4. regression smoke
   - `Leica M10`
   - `Leica M11-P`
   - `Leica 50 Summicron Rigid`
   - `Leica Noctilux 0.95`

## Final Judgment

**PASS**

Because:

- major Leica body-family drift cases were fixed in scoped shadow mode
- missing canonical count dropped sharply
- duplicate representative strategy is now explicit and stable
- live price evidence still does not use Kamerastore
- existing source behavior did not regress
