# Summicron-SL 24 Taxonomy Audit - Round 1

Date: 2026-05-24

Scope: audit-only review for the `Summicron-SL 24` family hypothesis. This round does not add seed rows, does not modify `entities/*.json`, does not modify `canonical_entities_index.json`, and does not change classifier/query/search behavior, ranking, or UI. The goal is to determine whether `Leica Summicron-SL 24mm f/2 ASPH` is a real, seedable Leica SL product line or whether the apparent family should be closed as non-existent / unsupported.

## Executive Summary

`Summicron-SL 24` should **not** be seeded.

Round-1 conclusion:

- literature status:
  - unsupported family hypothesis
  - closed non-family hypothesis
- immediate recommended `core` candidate count: `0`
- recommended first-pass core:
  - none
- explicit `hold` candidate:
  - none
- strongest deferred candidate:
  - none
- next seed round:
  - not allowed in current state

Why this closes rather than defers as a weak real family:

1. official Leica SL literature does **not** show a `Leica Summicron-SL 24mm f/2 ASPH` line
2. the existing closed `APO-Summicron-SL 24` hypothesis is also unsupported, so there is no parallel APO or non-APO official `24mm f/2` SL prime line to anchor
3. the actual Leica SL wide-prime structure instead shows:
   - `Leica Super-APO-Summicron-SL 21mm f/2 ASPH`
   - `Leica APO-Summicron-SL 28mm f/2 ASPH`
4. the current local title pool contains **no clean `Summicron-SL 24` listings**
5. broad `summicron-sl 24` retrieval space is just contamination from:
   - M-side `24mm` families like `Elmarit-M 24`, `Elmar-M 24`, `Summilux-M 24`
   - the already-closed `Summicron-M 24` hypothesis
   - R-side `Elmarit-R 24`
   - `SL 14-24`, `SL 16-35`, `SL 24-90`
   - third-party `20 / 24 / 28mm` L-mount primes

This is not a case of “real family but weak pool.” It is a closed unsupported family hypothesis.

## Family Hypothesis

The hypothesis tested in this round was:

- `Leica Summicron-SL 24mm f/2 ASPH`

and related seller wording such as:

- `summicron-sl 24`
- `summicron sl 24`
- `24 summicron-sl`
- `24mm f2 summicron-sl`
- `24mm f/2 summicron-sl`
- `leica sl 24mm f2 summicron`
- `sl 24/2 summicron`
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
- zoom neighbors:
  - `Super-Vario-Elmarit-SL 14-24 f/2.8 ASPH.`
  - `Super-Vario-Elmar-SL 16-35 f/3.5-4.5 ASPH.`
  - `Vario-Elmarit-SL 24-90 f/2.8-4 ASPH.`

Notably, it does **not** list any `24mm f/2 Summicron-SL`.

Reference:

- [Leica Camera - Leica SL-Lenses](https://leica-camera.com/en-int/photography/lenses/sl)

### Source B: Leica technical specification - `Super-APO-Summicron-SL 21 f/2 ASPH.`

Leica documents the ultra-wide APO SL prime at `21mm`, with:

- order number:
  - `11181`
- `L-Mount`
- `E67`
- `f/2`

Reference:

- [Leica Camera - Technical Specifications - Super-APO-Summicron-SL 21 f/2 ASPH.](https://leica-camera.com/en-int/photography/lenses/sl/super-apo-summicron-sl-21-f2-asph/technical-specification)

### Source C: Leica technical specification - `APO-Summicron-SL 28 f/2 ASPH.`

Leica documents the next SL wide APO prime at `28mm`, with:

- order number:
  - `11183`
- `L-Mount`
- `E67`
- `f/2`

Again, there is no `24mm f/2 Summicron-SL` between the `21mm` and `28mm` entries.

Reference:

- [Leica Camera - Technical Specifications - APO-Summicron-SL 28 f/2 ASPH.](https://leica-camera.com/en-US/photography/lenses/sl/apo-summicron-sl-28-f2-asph-black-finish/technical-specification)

### Source D: existing adjacent closed and real-family context

This project already established:

- closed non-family hypothesis:
  - `Leica APO-Summicron-SL 24mm f/2 ASPH`
- literature-real but deferred:
  - `Leica Super-APO-Summicron-SL 21mm f/2 ASPH`
- literature-real and active:
  - `Leica APO-Summicron-SL 28mm f/2 ASPH`
- literature-real but deferred:
  - `Leica Summicron-SL 35mm f/2 ASPH`
  - `Leica Summicron-SL 50mm f/2 ASPH`

Round-1 implication:

- there is no evidence of an official non-APO SL `24mm f/2` family sitting between the real `21mm` and real `28mm` structure

## Interpretation

The literature stack argues against the family hypothesis:

1. the actual Leica SL wide-prime line already steps from `21mm` to `28mm`
2. no supporting Leica page or data sheet was found for `Leica Summicron-SL 24mm f/2 ASPH`
3. the already-closed `APO-Summicron-SL 24` hypothesis removes the most likely adjacent confusion path
4. round-1 should treat `Summicron-SL 24` as a closed non-family hypothesis, not as a weak real family awaiting more data

## Local Listing Evidence

Analysis base:

- `data/normalized/normalized_latest.json`
- `results.json`
- `data/sold_items.json`

### Broad retrieval

A broad retrieval around `24 + summicron + sl` produced no local target-family rows.

Reviewed local `SL 24 Summicron` field does not show:

- `Leica Summicron-SL 24mm f/2 ASPH`
- `SL 24/2 Summicron`
- any clean local non-APO `24mm` SL prime line

Instead, the visible local `24mm` field is structurally dominated by contamination such as:

- `Elmarit-M 24`
- `Elmar-M 24`
- `Summilux-M 24`
- `Elmarit-R 24`
- `SL 24-90`
- `Sigma 24mm F2 DG DN Contemporary - L Mount`

### Clean pool after contamination filtering

After excluding:

- M-side `24mm` families
- closed `Summicron-M 24` hypothesis
- closed `APO-Summicron-SL 24` hypothesis
- R-side `Elmarit-R 24`
- `SL 14-24`
- `SL 16-35`
- `SL 24-90`
- neighboring SL `21 / 28 / 35`
- third-party `20 / 24 / 28mm` L-mount primes
- accessory-only rows
- body-kit or bundle rows

the useful local `Summicron-SL 24` pool becomes:

- clean local pool: `0`
- unique titles: `0`
- KRW-priced: `0`
- median: 없음

### Smoke query behavior

Expected target-like queries:

- `summicron-sl 24`
- `summicron sl 24`
- `24 summicron-sl`
- `24mm f2 summicron-sl`
- `24mm f/2 summicron-sl`
- `leica sl 24mm f2 summicron`
- `sl 24/2 summicron`

all returned:

- `0` direct clean local title hits

Broader shorthand queries such as:

- `summicron 24`
- `leica sl 24`
- `24 cron`

only point toward contamination and produce no valid family evidence.

### Interpretation

This is the decisive local result:

1. there is no clean local title support
2. there is no priced subset
3. all broad retrieval comes from contamination, not from a real `24mm Summicron-SL` market line

## Contamination Review

### 24mm Leica M boundary

The real Leica M `24mm` families are:

- `Elmarit-M 24`
- `Elmar-M 24`
- `Summilux-M 24`

These remain separate and already account for the real Leica M `24mm` lens space.

### Closed `Summicron-M 24` hypothesis boundary

This project already carries a closed / unsupported `Summicron 24` hypothesis on the M side.

That closed hypothesis must not be revived or merged into a fake SL-side `Summicron-SL 24` family.

### Closed `APO-Summicron-SL 24` hypothesis boundary

This project already carries a closed / unsupported `APO-Summicron-SL 24` hypothesis.

That closed hypothesis must not be revived or recast as a fake non-APO SL-side `Summicron-SL 24` family.

### R / SL / third-party boundary

These must remain outside:

- `Elmarit-R 24`
- `Super-APO-Summicron-SL 21`
- `APO-Summicron-SL 28`
- `APO-Summicron-SL 35`
- `Summicron-SL 35`
- `Super-Vario-Elmarit-SL 14-24`
- `Super-Vario-Elmar-SL 16-35`
- `Vario-Elmarit-SL 24-90`
- Sigma / Panasonic / Lumix `20 / 24 / 28mm` lenses

### Accessory contamination

These must stay outside the family hypothesis:

- hood-only rows
- cap-only rows
- case-only rows
- boxed / packaging-only fragments

## Candidate Review

## Candidate 1: `Leica Summicron-SL 24mm f/2 ASPH`

### Literature basis

Unsupported.

Round-1 official Leica literature does not show this product line.

### Local title support

Absent.

No clean local title support was found.

### Price behavior

Absent.

No KRW-priced support was found because no clean pool exists.

### Boundary risk

Very high.

The shorthand collapses into:

- closed `APO-Summicron-SL 24`
- M-side `24mm`
- `SL 24-90`
- third-party `24mm`

### Round-1 decision

- reject as a seed candidate
- close as unsupported

## Round-1 Recommendation

### Literature status

- unsupported family hypothesis
- closed non-family hypothesis

### Immediate `core` candidate count

- `0`

### Recommended first-pass `core`

- none

### Explicit `hold` candidates

- none

### Strongest deferred candidate

- none

## Why close the hypothesis instead of deferring it?

Because round-1 evidence does not say:

- real family, weak local support

It says:

- official Leica SL literature does not identify any `Summicron-SL 24mm f/2 ASPH`
- the real SL wide-prime structure already moves from `Super-APO-Summicron-SL 21` to `APO-Summicron-SL 28`
- the local `SL 24 Summicron` pool is completely absent

So this is not a conservative defer. It is a closed unsupported family hypothesis.

## Overlay / Hypothetical Markers

If the hypothesis were ever reopened, these would still remain non-row markers:

- `ASPH`
- `E67`
- filter-thread marker
- hood / cap / case / boxed / packaging

But in round 1 no row should be opened, so these remain hypothetical markers only and should not be promoted.

## Final Round-1 Recommendation

### Seedability in this round

- closed

### Best next action

- do not seed
- do not defer as a literature-real family
- record the hypothesis as unsupported
- continue to use the actual SL wide-prime structure:
  - `Super-APO-Summicron-SL 21`
  - `APO-Summicron-SL 28`

### Unsafe broad aliases

Do **not** hard-pin:

- `summicron-sl 24`
- `summicron sl 24`
- `summicron 24`
- `leica sl 24`
- `24 cron`
