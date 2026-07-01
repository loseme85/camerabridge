# P3 Kamerastore Price Guard Audit v1

## Executive Summary

- Scope: read-only audit only
- Source under review: `Kamerastore`
- Current source status: `limited_crawl`
- Current price evidence policy: `blocked_initially`
- No live price policy, parser, ranking, alias, or preview/prod deployment was changed in this round.

Current local snapshot:

- Kamerastore rows in resolved/index: `106`
- Link-health sample: previously confirmed `29 / 29 alive_200` with `curl`
- Price parse success: `106 / 106`
- Currency consistency: `KRW 106 / 106`

Main conclusion:

- We can now separate a meaningful subset of Kamerastore rows into:
  - price-evidence candidate rows
  - rows that must be excluded by source-specific guards
- But duplicate clusters, missing canonical assignments, and classification drift are still real enough that Kamerastore should **not** be promoted yet.

Final judgment: **PENDING**

## 1. Audit Goal

This round asks one narrow question:

> If Kamerastore were ever considered for price evidence in the future, which rows would need to be excluded first, and what guards would be required?

This is a shadow simulation only.

## 2. Data Profile

Kamerastore rows reviewed: `106`

Category breakdown:

- `Lens`: `55`
- `Body`: `43`
- `Accessory`: `8`

Model canonical distribution notes:

- top model families include `Summicron-M`, `Elmar`, `Summicron-R`, `Elmarit-R`, `Q2`
- rows with missing canonical model: `10`
- duplicate URL count: `0`

Important caveat:

- duplicate-title clusters exist even though exact URL duplication does not
- that means price evidence can still double-count materially similar inventory if source-specific dedupe is not added

## 3. Risk Classification Rules Used in This Audit

### 3.1 Bundle-like title detection

Rows were flagged as bundle-like if title contained one or more of:

- ` + `
- `kit`
- `bundle`
- `set`
- `with`

Accessory-attached bundle markers also counted as contamination signals:

- `hood`
- `adapter`
- `grip`
- `handgrip`
- `meter`
- `case`
- `strap`
- `filter`
- `cap`

### 3.2 Accessory contamination

Rows were flagged as accessory contamination if:

- category was already `Accessory`, or
- title contained accessory terms such as:
  - `hood`
  - `adapter`
  - `grip`
  - `handgrip`
  - `thumb`
  - `case`
  - `filter`
  - `cap`
  - `strap`
  - `charger`
  - `battery`
  - `meter`

### 3.3 Duplicate risk

Rows were flagged as duplicate-risk when the following tuple repeated:

- `title_raw`
- `model_canonical`
- `condition_raw`

### 3.4 Classification drift

Rows were flagged when title looked body-like but resolved category was not `Body`, or when other obvious classification mismatches appeared.

Special attention item:

- `Leica M Monochrom (Black, 10760)`

### 3.5 Missing canonical

Rows without `model_canonical` were flagged as unsafe for future price evidence.

### 3.6 Suspicious price

Rows were flagged if parsed numeric price was missing or non-positive.

In this snapshot:

- suspicious price count: `0`

## 4. Aggregate Results

### 4.1 Price evidence candidate rows

Rows that passed this audit’s exclusion screen:

- `70`

### 4.2 Rows that should be excluded

Rows that hit one or more exclusion reasons:

- `36`

### 4.3 Exclusion reason counts

These counts are overlapping by reason:

- `bundle`: `13`
- `accessory`: `10`
- `duplicate`: `20`
- `classification_drift`: `3`
- `missing_canonical`: `10`
- `suspicious_price`: `0`

## 5. Bundle / Accessory Findings

Bundle-like rows: `13`

Accessory-contaminated rows: `10`

Representative examples:

- `Leica M4 (No Serial) (Black Paint, 10402) + Meter MR`
- `Leica M8 (Black, 10701) + M8/M9 Handgrip (14486)`
- `Leica 35mm f2.5 Summarit-M (11643) + Lens Hood (35/50mm f2.5) (12459)`
- `Leica 60mm f2.8 Macro-Elmarit-R (Type I) (2-Cam) (11205) + R Macro Adapter (14198)`
- `Leica 19mm f2.8 Elmarit-R ... + Adapter ... + Lens Hood ...`

Interpretation:

- These rows are useful for discovery.
- They are not safe as clean single-item price evidence without aggressive exclusion.

## 6. Duplicate Cluster Findings

Duplicate-risk clusters found: `9`

Representative duplicate clusters:

1. `Leica IIIa + 50mm f3.5 Elmar (Type I) (ELMARCHROM / ELMAR)`
   - count: `3`
   - prices: `678000`, `927000`, `797000`

2. `Leica M (Typ 240) (Black Paint, 10770)`
   - count: `3`
   - prices: `5114000`, `5383000`, `5383000`

3. `Leica M Monochrom (Black, 10760)`
   - count: `2`
   - prices: `7221000`, `7221000`

4. `Leica Q2 Monochrom (19055)`
   - count: `2`
   - prices: `7611000`, `7796000`

5. `Leica 50mm f2 Summicron-M (Type IV) (Black, 11819)`
   - count: `2`
   - prices: `3155000`, `2767000`

6. `Leica 35mm f2 Summicron (Type III) (11309)`
   - count: `2`
   - prices: `3341000`, `3006000`

Interpretation:

- URL-level dedupe alone is not enough.
- Kamerastore needs source-specific duplicate cluster suppression before any future price evidence promotion.

## 7. Classification Drift Findings

Classification drift candidates found: `13`

Material examples:

1. `Leica M Monochrom (Black, 10760)`
   - current category: `Lens`
   - mount: `M`
   - model_canonical: `None`
   - issue:
     - body-like title
     - missing canonical
     - duplicate cluster present

2. `Leica M-E (Typ 220) (10759)`
   - current category: `Lens`
   - model_canonical: `None`

3. `Leica MDa (Slotted Baseplate) (10913)`
   - current category: `Accessory`
   - model_canonical: `MDa`
   - likely body-family drift

4. `Leica M (Typ 262) (10947)`
   - current category looks plausible upstream for body context, but canonical is missing

Interpretation:

- The worst current blocker is not raw price quality.
- It is row-level classification trust for certain body-family titles.

## 8. Shadow Simulation by Representative Query

This section does **not** change live behavior.
It only asks: if Kamerastore rows were considered, which rows would survive a source-specific guard?

### 8.1 Leica 50mm Summicron-M Type IV

- Kamerastore matching rows: `3`
- allowed candidates: `1`
- excluded: `2`
- exclusion reason:
  - `duplicate`

Reading:

- This family could be made safer with source-local duplicate suppression.

### 8.2 Leica 35mm Summicron

- matching rows: `3`
- allowed candidates: `1`
- excluded: `2`
- exclusion reason:
  - `duplicate`

Reading:

- Similar story: not impossible, but duplicate control is mandatory.

### 8.3 Leica M Monochrom

- matching rows: `2`
- allowed candidates: `0`
- excluded: `2`
- reasons:
  - `classification_drift`
  - `duplicate`
  - `missing_canonical`

Reading:

- This is not safe for future price evidence until classification and canonical assignment are fixed.

### 8.4 Leica M4

- matching rows: `4`
- allowed candidates: `3`
- excluded: `1`
- excluded row:
  - `Leica M4 ... + Meter MR`
- reasons:
  - `accessory`
  - `bundle`

Reading:

- Body-family queries can work if bundle/accessory rows are explicitly blocked.

### 8.5 Leica M Typ 240

- matching rows: `4`
- allowed candidates: `1`
- excluded: `3`
- reasons:
  - `duplicate`
  - `missing_canonical`

Reading:

- This family is not ready without canonical cleanup and duplicate suppression.

### 8.6 Leica Q2

- matching rows: `5`
- allowed candidates: `1`
- excluded: `4`
- exclusion reason:
  - `duplicate`

Reading:

- Q2 can be made safer, but duplicate clusters must be handled first.

### 8.7 Leica Elmarit-R

- matching rows: `6`
- allowed candidates: `4`
- excluded: `2`
- excluded examples:
  - lens + adapter
  - lens + hood / accessory pack

Reading:

- Lens-family rows can be relatively clean if bundle/accessory guards are strict.

### 8.8 Leica hood

- matching rows: `4`
- allowed candidates: `0`
- excluded: `4`
- reasons:
  - `accessory`
  - `bundle`

Reading:

- Correct future behavior would keep these out of lens/body price evidence entirely.

### 8.9 Leica adapter

- matching rows: `3`
- allowed candidates: `0`
- excluded: `3`
- reasons:
  - `accessory`
  - `bundle`

### 8.10 Leica handgrip

- matching rows: `1`
- allowed candidates: `0`
- excluded: `1`
- reasons:
  - `accessory`
  - `bundle`

## 9. Proposed Source-Specific Guard Rules

If Kamerastore is ever reconsidered for `allowed_after_validation`, the minimum safe guard set should be:

1. **Accessory hard block**
   - If category is `Accessory`, never allow price evidence.
   - Also hard-block titles containing:
     - hood
     - adapter
     - grip / handgrip / thumb
     - case
     - strap
     - filter
     - cap
     - battery
     - charger
     - meter

2. **Bundle hard block**
   - Exclude titles containing:
     - ` + `
     - `kit`
     - `bundle`
     - `set`
     - `with`

3. **Duplicate cluster block**
   - Within Kamerastore, treat repeated `(title_raw, model_canonical, condition_raw)` clusters as a single candidate at most.
   - Prefer the cleanest row per cluster rather than counting every row.

4. **Missing canonical block**
   - Rows without `model_canonical` must not enter price evidence.

5. **Classification drift block**
   - Body-like titles resolved as `Lens` or `Accessory` must be excluded.
   - This explicitly includes current `M Monochrom` / `M-E` style failures.

6. **Condition-aware future gate**
   - If the source is later promoted, condition grouping should be reviewed before exact evidence use.

## 10. Promotion Readiness Judgment

Question:

> Can Kamerastore move from `blocked_initially` to `allowed_after_validation` now?

Answer:

- **Not yet**

Why:

- Duplicate pressure is too high (`20` rows flagged for duplicate risk)
- Missing canonical rows are still meaningful (`10`)
- Classification drift remains present (`3` high-signal rows, including `M Monochrom`)
- Bundle/accessory contamination is non-trivial (`13` bundle, `10` accessory)

What improved from the last audit:

- We now have a workable exclusion framework.
- We can explain which rows are plausible candidates and which must stay out.

What still blocks promotion:

- We do not yet have confidence that Kamerastore rows can enter price evidence without source-specific duplicate and classification safeguards.

## 11. Allowed-After-Validation Outlook

Current stance:

- `blocked_initially` should remain unchanged
- `price_eligible` is still premature

Best next step:

- open a narrow follow-up for **Kamerastore-only classification + duplicate guard design**
- especially:
  - `M Monochrom`
  - `M-E`
  - `M Typ 240`
  - repeated Summicron / Q2 duplicate clusters
  - body + accessory bundle rows

## 12. Final Judgment

**PENDING**

Reason:

- This audit successfully separated a candidate pool (`70`) from an excluded pool (`36`).
- The guard requirements are now concrete.
- But classification drift and duplicate risk are still too meaningful to justify a source promotion today.
