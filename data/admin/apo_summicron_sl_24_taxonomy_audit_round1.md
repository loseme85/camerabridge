# APO-Summicron-SL 24 Taxonomy Audit - Round 1

Date: 2026-05-23

Scope: audit-only review for the Leica `APO-Summicron-SL 24` family hypothesis. This round does not add seed rows, does not modify `entities/*.json`, does not modify `canonical_entities_index.json`, and does not change classifier/query/search behavior, ranking, or UI. The goal is to determine whether `Leica APO-Summicron-SL 24mm f/2 ASPH` is a real, seedable Leica SL product line or whether the apparent family should be closed as non-existent / unsupported.

## Executive Summary

`APO-Summicron-SL 24` should **not** be seeded.

Round-1 conclusion:

- immediate recommended `core` candidate count: `0`
- recommended first-pass core:
  - none
- explicit `hold` candidate:
  - none
- round-1 recommendation:
  - `seed 보류`
  - close the hypothesized `APO-Summicron-SL 24` family for now

Why this closes rather than defers as a weak real family:

1. the Leica literature stack does **not** show a `Leica APO-Summicron-SL 24mm f/2 ASPH` line
2. Leica SL wide-prime literature instead shows:
   - `Leica Super-APO-Summicron-SL 21mm f/2 ASPH`
   - `Leica APO-Summicron-SL 28mm f/2 ASPH`
3. the current Leica SL lens lineup does not surface any `24mm APO-Summicron-SL`
4. the local title pool contains **no clean `24mm APO-Summicron-SL` listings**
5. broad `apo summicron 24` retrieval is just contamination from:
   - M-side `24mm` families like `Elmarit-M 24`, `Elmar-M 24`, `Summilux-M 24`
   - R-side `Elmarit-R 24`
   - `SL 24-90`
   - third-party `24mm` L-mount primes

This is not a case of “real family but weak pool.”  
It is closer to “the proposed Leica SL family does not exist in the literature stack that governs the rest of this taxonomy.”

## Family Hypothesis

The hypothesis tested in this round was:

- `Leica APO-Summicron-SL 24mm f/2 ASPH`

and related seller wording such as:

- `apo-summicron-sl 24`
- `apo summicron sl 24`
- `24 apo-summicron-sl`
- `24mm f2 apo-summicron-sl`
- `24mm f/2 apo-summicron-sl`
- `sl 24/2 apo summicron`
- `24 apo`
- `24 cron`

Round-1 answer: this should not be opened as a canonical family.

## Literature / Reference Base

### Source A: Leica SL lens lineup

Leica's current SL lens lineup shows the relevant wide-prime structure as:

- `Super-APO-Summicron-SL 21 f/2 ASPH.`
- `APO-Summicron-SL 28 f/2 ASPH.`
- `APO-Summicron-SL 35 f/2 ASPH.`
- `APO-Summicron-SL 50 f/2 ASPH.`
- `APO-Summicron-SL 75 f/2 ASPH.`
- `APO-Summicron-SL 90 f/2 ASPH.`

Notably, it does **not** list any `24mm APO-Summicron-SL`.

Reference:

- [Leica Camera - Leica SL-Lenses](https://leica-camera.com/en-int/photography/lenses/sl)

### Source B: Leica technical specification - `Super-APO-Summicron-SL 21 f/2 ASPH.`

Leica documents the ultra-wide APO SL prime at `21mm`, with:

- order number:
  - `11181`
- `L-Mount`
- `E67`
- `f/2`

This is the literature-real ultra-wide APO SL prime next to the proposed `24mm` gap.

Reference:

- [Leica Camera - Technical Specifications - Super-APO-Summicron-SL 21 f/2 ASPH.](https://leica-camera.com/en-int/photography/lenses/sl/super-apo-summicron-sl-21-f2-asph/technical-specification)

### Source C: Leica technical specification - `APO-Summicron-SL 28 f/2 ASPH.`

Leica documents the next APO SL wide prime at `28mm`, with:

- order number:
  - `11183`
- `L-Mount`
- `E67`
- `f/2`

Again, there is no `24mm APO-Summicron-SL` between the `21mm` and `28mm` entries.

Reference:

- [Leica Camera - Technical Specifications - APO-Summicron-SL 28 f/2 ASPH.](https://leica-camera.com/en-US/photography/lenses/sl/apo-summicron-sl-28-f2-asph-black-finish/technical-specification)

### Source D: Leica press release for SL ultra-wide expansion

Leica's SL-system ultra-wide expansion press material pairs:

- `Super-Vario-Elmarit-SL 14-24 f/2.8 ASPH.`
- `Super-APO-Summicron-SL 21 f/2 ASPH.`

The literature expands downward to `21mm`, not to any `24mm APO-Summicron-SL`.

Reference:

- [Leica Camera - Press Release - Super-APO-Summicron-SL 21 f/2 ASPH. and Super-Vario-Elmarit-SL 14-24 f/2.8 ASPH.](https://leica-camera.com/sites/default/files/2023-10/press_release_apo-summicron-sl_21_super-vario-sl_14-24_october_2023.pdf)

## Interpretation

The literature stack argues against the family hypothesis:

1. the actual Leica SL wide-prime line already steps from `21mm` to `28mm`
2. no supporting Leica page or data sheet was found for `Leica APO-Summicron-SL 24mm f/2 ASPH`
3. round-1 should treat `APO-Summicron-SL 24` as a non-family hypothesis, not as a weak family awaiting more data

## Local Listing Evidence

Analysis base:

- `data/normalized/normalized_latest.json`
- `results.json`
- `data/sold_items.json`

### Broad retrieval

A naive broad retrieval around `24 + summicron + sl + apo` produced no clean target-family rows.

Instead, the visible local `24mm` field is dominated by contamination such as:

- `LEICA 24mm F2.8 ASPH ELMARIT-M ...`
- `LEICA 24mm F2.8 ELMARIT-R ...`
- `Sigma 24mm F2 DG DN Contemporary - L Mount`

### Clean pool after contamination filtering

After excluding:

- M-side `24mm` families
- R-side `Elmarit-R 24`
- `SL 24-90`
- neighboring SL APO prime families
- third-party `20 / 24 / 28 / 35mm` L-mount primes
- accessory-only rows

the useful local `APO-Summicron-SL 24` pool becomes:

- clean local pool: `0`
- unique titles: `0`
- KRW-priced: `0`
- median: 없음

### Smoke query behavior

Expected target-like queries:

- `apo-summicron-sl 24`
- `apo summicron sl 24`
- `24 apo-summicron-sl`
- `24mm f2 apo-summicron-sl`
- `24mm f/2 apo-summicron-sl`
- `leica sl 24mm f2 apo summicron`
- `sl 24/2 apo summicron`

all returned:

- `0` direct clean local title hits

Broader shorthand queries such as:

- `apo summicron 24`
- `summicron 24`
- `leica sl 24`
- `24 apo`
- `24 cron`

only point toward contamination and produce no valid family evidence.

### Interpretation

This is the decisive local result:

1. there is no clean local title support
2. there is no priced subset
3. all broad retrieval comes from contamination, not from a real `24mm APO-Summicron-SL` market line

## Contamination Review

### 24mm Leica M boundary

The real Leica M `24mm` families are:

- `Elmarit-M 24`
- `Elmar-M 24`
- `Summilux-M 24`

These remain separate and already account for the actual Leica M `24mm` lens space.

### Closed `Summicron 24` hypothesis boundary

This project already carries a closed / unsupported `Summicron 24` hypothesis.

That closed hypothesis must not be revived or merged into a fake SL-side `APO-Summicron-SL 24` family.

### R / SL / third-party boundary

These must remain outside:

- `Elmarit-R 24`
- `APO-Summicron-SL 28`
- `APO-Summicron-SL 35`
- `APO-Summicron-SL 50`
- `APO-Summicron-SL 75`
- `APO-Summicron-SL 90`
- `Super-Vario-Elmar-SL 16-35`
- `Vario-Elmarit-SL 24-90`
- Sigma / Panasonic / Lumix `20 / 24 / 28 / 35mm` lenses

### Accessory contamination

These must stay outside the family hypothesis:

- hood-only rows
- cap-only rows
- case-only rows
- boxed / packaging-only fragments

## Candidate Review

## Candidate 1: `Leica APO-Summicron-SL 24mm f/2 ASPH`

### Literature basis

Unsupported.

Round-1 official Leica literature does not show this product line.

### Local title support

Absent.

No clean local title support was found.

### Price behavior

Absent.

No KRW-priced clean local rows exist.

### Search-intent stability

Poor.

The query surface is dominated by real neighboring Leica M / R / SL / third-party `24mm` families.

### Final decision

`closed non-family hypothesis`

### One-line reason

`Leica APO-Summicron-SL 24mm f/2 ASPH` is unsupported by the Leica literature stack and has no clean local market evidence.

## Overlay Elements

No family row should be opened, so these are not row-level decisions for now:

- `APO`
- `ASPH`
- `E67`
- filter-thread marker
- hood included
- cap included
- boxed
- case included
- packaging

## Out-of-Family Boundaries

Do not merge with:

- `Elmarit-M 24`
- `Elmar-M 24`
- `Summilux-M 24`
- closed `Summicron 24` hypothesis
- `Elmarit-R 24`
- `APO-Summicron-SL 28`
- `APO-Summicron-SL 35`
- `APO-Summicron-SL 50`
- `APO-Summicron-SL 75`
- `APO-Summicron-SL 90`
- `Super-Vario-Elmar-SL 16-35`
- `Vario-Elmarit-SL 24-90`
- Sigma / Panasonic / Lumix `20 / 24 / 28 / 35mm`
- accessory-only listings

## Seed-Round Readiness

- next seed round:
  - `불가`

Round-1 recommendation:

- do not open any `APO-Summicron-SL 24` row
- keep the family hypothesis closed unless future official Leica literature proves that this exact product line exists

## Validation

Validation run after this audit-only report update:

- `python3 tests/test_normalization_admin.py`
  - `ok`
- `python3 -m py_compile normalization_admin.py golden_set.py tests/test_normalization_admin.py`
  - `ok`
- `python3 golden_set.py`
  - `132/132`
