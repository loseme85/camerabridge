# P3 Kamerastore Allowed-After-Validation Review v1

## Executive Summary

- Scope: audit-only promotion review
- Source under review: `Kamerastore`
- Current source status: `limited_crawl`
- Current `price_evidence_policy`: `blocked_initially`
- Live price evidence remains unchanged
- No deploy / no push / no ranking-parser-price logic change in this round

Current readiness snapshot:

- limited crawl pilot: `PASS`
- link survival sample: effectively `PASS`
- price parse success: `106 / 106`
- currency consistency: `KRW 106 / 106`
- shadow price guard: `PASS`
- classification / duplicate cleanup: `PASS`
- classification drift: `4 -> 0`
- missing canonical: `10 -> 1`
- allowed candidate: `70 -> 75`
- excluded candidate: `36 -> 31`

Review conclusion:

- `blocked_initially -> allowed_after_validation` is now **reasonable**
- but only if Kamerastore stays behind **source-specific live guard rules**
- Kamerastore is still **not** ready for `price_eligible`

Final judgment: **PASS**

## 1. Current Kamerastore Status

- source registry status: `limited_crawl`
- source registry price evidence policy: `blocked_initially`
- rows in current local snapshot: `106`
- live `used_for_price`: still blocked at source-policy level

This review does **not** change live behavior.

## 2. allowed_after_validation vs price_eligible

### allowed_after_validation

Meaning:

- source-wide hard block can be relaxed
- but only for rows that pass source-specific guards
- bad rows must still be excluded before they can influence any price pool
- duplicate suppression and category sanity checks must run first

### price_eligible

Meaning:

- source rows are trusted enough to actually participate in user-facing price evidence
- exact/reference price summaries can use compatible rows
- duplicate, bundle, accessory, category drift, and canonical issues are already controlled in live path

Kamerastore is **not there yet**.

## 3. Link Readiness

Based on the earlier detail URL audit:

- sampled detail URLs: `29`
- `curl HEAD 200`: `29 / 29`
- `curl GET 200`: `29 / 29`
- browser-like `GET 200`: `29 / 29`
- redirect-away / 403 / 404 / timeout: `0`

Important clarification:

- the earlier timeout signal was traced to Python client TLS certificate verification failure
- it did **not** reproduce as mass dead links
- public-facing `View source` readiness looks acceptable for this source at sampled scale

Assessment:

- link readiness: **PASS**

## 4. Price Readiness

Using current Kamerastore-resolved raw payload fields:

- row count: `106`
- price populated: `106 / 106`
- currency: `KRW 106 / 106`
- condition populated: `106 / 106`
- active/asking state: `106 / 106`
- sold/reserved rows in current pilot snapshot: `0`

Implication:

- discovery/display price quality is strong enough
- no zero/null price problem is visible in the current pilot
- current sample does not yet test sold-history pricing behavior

Assessment:

- price parse readiness: **PASS**
- sold-history readiness: **not yet validated**

## 5. Classification Readiness

Current post-cleanup shadow summary:

- `allowed_candidate_count = 75`
- `excluded_candidate_count = 31`
- `classification_drift = 0`
- `missing_canonical = 1`

High-signal body-family recovery is now in place for the scoped Kamerastore shadow layer:

- `Leica M Monochrom` -> effective `Body / M Monochrom`
- `Leica M-E (Typ 220)` -> effective `Body / M-E`
- `Leica M (Typ 262)` -> effective `Body / M (Typ 262)`
- `Leica M (Typ 240)` -> effective `Body / M (Typ 240)`
- `Leica MDa` -> effective `Body / MDa`
- `Leica Q2 Monochrom` -> effective `Body / Q2 Monochrom`

Remaining missing canonical row:

- `Leica 21mm Optical Viewfinder (SBKOO / 12002)`
- current reasons:
  - `accessory`
  - `missing_canonical`

This remaining row is already safe to exclude.

Assessment:

- classification readiness: **PASS**

## 6. Guard Readiness

Current shadow exclusion counts:

- `accessory = 9`
- `bundle = 13`
- `duplicate = 20`
- `missing_canonical = 1`

### Required source-specific live guards

If Kamerastore ever moves to `allowed_after_validation`, the live path must keep these guards:

1. accessory hard block
   - category `Accessory`
   - or title contains:
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

2. bundle hard block
   - title contains:
     - ` + `
     - `kit`
     - `bundle`
     - `set`
     - `with`

3. missing canonical hard block
   - no `model_canonical`

4. classification drift hard block
   - body-like title but non-body classification
   - scoped Leica body-family effective projection must still run

5. duplicate cluster suppression
   - cluster key:
     - `(title_raw, model_canonical, condition_raw)`
   - only one row from a cluster may advance as candidate

Assessment:

- guard readiness: **PASS**

## 7. Duplicate Strategy Readiness

Current duplicate summary:

- duplicate clusters: `9`
- duplicate-cluster rows: `20`
- duplicate-cluster representatives: `8`

Representative strategy from the cleanup round:

1. prefer shadow-clean rows
2. then stronger condition
   - `Certified` > `Restored` > `Not Passed`
3. then later `crawl_time`
4. then stable `source_url`

Why this matters:

- Kamerastore has no obvious URL-level duplication problem
- but title/model/condition cluster duplication is real
- without suppression, price evidence could double-count materially same inventory

Assessment:

- duplicate strategy readiness: **PASS**
- but duplicate suppression must be part of the live guard, not optional

## 8. Representative Query Shadow Result

This section is shadow-only. No live user price behavior changed.

### Leica 50mm Summicron-M Type IV

- clean Summicron-M Type IV rows appear as `allowed_candidate`
- duplicate siblings still appear as `excluded_candidate`
- no live `used_for_price` promotion happened

### Leica 35mm Summicron

- clean rows remain `allowed_candidate`
- duplicate Type III rows are still excluded by duplicate guard

### Leica M Monochrom

- `Leica M Monochrom (Black, 10760)` is no longer classification drift
- it is now effectively a body-family row
- remaining exclusion is duplicate-only in shadow replay

### Leica M-E

- `Leica M-E (Typ 220)` now surfaces as effective `Body / M-E`
- shadow status: `allowed_candidate`

### Leica M Typ 240

- body-family projection is recovered
- duplicate-sensitive rows still require cluster suppression

### Leica M4

- clean body row visible
- shadow status: `allowed_candidate`

### Leica Q2

- `Q2` body rows remain allowed candidates
- `Q2 Monochrom` duplicate siblings remain duplicate-excluded

### Leica Elmarit-R

- clean lens rows are candidate-safe
- accessory-attached bundle row remains excluded

### Leica hood / Leica adapter / Leica handgrip

- accessory-oriented Kamerastore rows stay excluded
- no sign that these rows should move into future price evidence

## 9. Promotion Risk Review

### Candidate ratio

- allowed candidates: `75 / 106` (`70.8%`)
- excluded candidates: `31 / 106` (`29.2%`)

Interpretation:

- a meaningful majority of rows can now be separated into candidate-safe territory
- the excluded minority is also well explained, not random

### Excluded rows

The `31` excluded rows are still clearly justified by source-specific guards:

- accessory contamination
- bundle contamination
- duplicate clusters
- one remaining missing canonical accessory row

### Main remaining risk

The biggest remaining risk is **not** raw price parsing.

It is this:

- if Kamerastore ever enters live evidence without source-specific duplicate suppression and row blocking,
  duplicate/body-accessory/bundle contamination could still distort prices

## 10. Promotion Decision

### Can Kamerastore move to allowed_after_validation?

**Yes, conditionally.**

Recommended interpretation:

- `allowed_after_validation = PASS`
- but only with source-specific live guards turned on
- and still **separate** from `price_eligible`

### Required live guard conditions for that promotion

If promoted to `allowed_after_validation`, all of the following must be enforced:

1. accessory hard block
2. bundle hard block
3. missing canonical hard block
4. scoped Leica body-family classification drift block
5. duplicate cluster suppression with max one representative candidate
6. regression smoke on:
   - `Leica M Monochrom`
   - `Leica M-E`
   - `Leica M Typ 240`
   - `Leica Q2`
   - `Leica 35mm Summicron`
   - `Leica 50mm Summicron-M Type IV`
   - `Leica hood`
   - `Leica adapter`
   - `Leica handgrip`

## 11. Why Kamerastore Is Still Not price_eligible

Kamerastore should remain **not** `price_eligible` because:

1. duplicate clusters still require live suppression
2. bundle/accessory attached rows are common enough to matter
3. current pilot has only active inventory, not broad sold-history validation
4. source-specific guard logic still needs to exist in live path, not only shadow review
5. this review did not test broad cross-query price calibration against active sources

## 12. Recommended Next Step

Recommended next stage:

- keep source status operationally conservative
- review a **code-change proposal** for:
  - `blocked_initially -> allowed_after_validation`
  - with Kamerastore-only live guard enforcement
- do **not** promote to `price_eligible` in the same round

## 13. Final Judgment

- `allowed_after_validation` review: **PASS**
- `price_eligible` review: **not approved**
- live behavior today: unchanged

Final judgment: **PASS**
