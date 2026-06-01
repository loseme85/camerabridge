# Elmarit-M 135 Taxonomy Audit - Round 1

Date: 2026-05-08

Scope: read-heavy taxonomy audit for the Leica `Elmarit-M 135` family. This round does not add seed rows, does not change classifier/query/search behavior, and does not change admin lookup ranking or UI. The goal is to determine whether `Elmarit-M 135` is mature enough for explicit canonical seeding and, if so, at what granularity.

## Executive Summary

`Elmarit-M 135` is seedable, but round-1 should stay narrow.

The strongest round-1 conclusion is:

1. `Leica Elmarit-M 135mm f/2.8`

as the only immediate first-pass `core` candidate.

Round-1 does **not** support opening:

- generation I / II / III rows
- `goggles / eyes` rows
- `Canada / Germany` rows
- `black / chrome` rows
- `E55 / Series VII` filter or accessory rows

Round-1 conclusion:

- immediate recommended `core` candidate count: `1`
- recommended first-pass core:
  - `Leica Elmarit-M 135mm f/2.8`
- explicit `hold` candidate:
  - none
- `goggles / eyes`, `black / chrome`, `country marking`, `hood included`, `cap included`, `boxed`, `case included`, `packaging`, and filter-thread wording stay `overlay` or `보류`
- `APO-Telyt-M 135`, `Tele-Elmar 135`, `Hektor 135`, `Elmar 135`, classic `Telyt 135`, `R 135`, accessories, and third-party 135mm lenses remain out-of-family boundaries

The safest next step is a narrow seed add for `Leica Elmarit-M 135mm f/2.8` only, leaving generations and `eyes/goggles` outside round-1 seed rows.

## Family Overview

The Leica `135mm` field is now crowded by several already-audited or adjacent families:

- `APO-Telyt-M 135`
- `Tele-Elmar 135`
- `Elmarit-M 135`
- `Hektor 135`
- `Elmar 135`
- classic `Telyt 135`
- `R 135`
- accessories and third-party 135mm lenses

`Elmarit-M 135` is not a modern single-SKU line like `APO-Telyt-M 135`, but the local titles still converge more tightly than the noisier historical families such as broad `Elmar 90`.

The real round-1 question is whether the family needs generation or `eyes/goggles` splitting immediately.

Round-1 answer: `no`. The family is ready for one broad `core`, but not for internal seed rows.

## Literature / Reference Base

Established Leica literature convention treats `135mm f/2.8 Elmarit-M` as a real M-family with internal historical generations, commonly enumerated as:

- `Elmarit-M I`
- `Elmarit-M II`
- `Elmarit-M III`

That same literature convention also treats `eyes / goggles` equipped forms as mechanically meaningful variants inside the broader `Elmarit-M 135` space rather than as a separate top-level family on the level of:

- `APO-Telyt-M 135`
- `Tele-Elmar 135`
- `Elmar 135`
- `Hektor 135`

Operationally, that means the literature supports two things at once:

1. `Leica Elmarit-M 135mm f/2.8` is a real Leica M family
2. generation and `eyes/goggles` substructure exists, but is not automatically strong enough for round-1 row splitting

## Local Listing Evidence

Analysis base: `data/derived/results_resolved_v2.json`

Raw `135mm Elmarit` matches include contamination from:

- `Tele-Elmarit-M 135`
- `Elmarit-R 135`

After excluding those non-family rows and keeping only M-side `135mm f/2.8 Elmarit` titles, the useful local pool becomes:

- clean local pool: `6`
- unique title strings: `5`

### Broad price clustering

KRW-parsed local observations:

- clean local pool priced count: `3`
- median KRW: `650,000`
- observed priced range: `550,000` to `680,000`

All three priced examples are broad seller shorthand:

- `[위탁] M135/2.8 Elmarit (Black)` -> `650,000 KRW`
- `[중고] M 135/2.8 Elmarit (Black)` -> `680,000 KRW`
- `[위탁] M135/2.8 Elmarit (Black)` -> `550,000 KRW`

There is not enough local priced support to separate:

- generations
- `eyes/goggles`
- country marking
- filter-thread variants

### Local title patterns

Broad recurring titles:

- `[위탁] M135/2.8 Elmarit (Black)`
- `[중고] M 135/2.8 Elmarit (Black)`
- `LEICA 135mm F2.8 ELMARIT-M sn.3487`

Narrower explicit titles:

- `LEICA 135mm F2.8 eye ELMARIT sn.2038`
- `LEICA 135mm F2.8 eye ELMARIT-M sn.3486`

### Local marker frequency

Repeated local modifiers:

- `elmarit-m`: `2`
- `eye`: `2`
- `m 135/2.8` shorthand: `3`
- `black`: `3`

Not meaningfully present in the clean local pool:

- `goggles`
- `안경`
- `canada`
- `germany`
- `chrome`
- `e55`
- `series vii`
- `hood`
- `case`
- `boxed`

### Interpretation

This family is small but still more coherent than it first looks:

1. broad `135mm f/2.8 Elmarit` wording consistently points to the same Leica M family
2. explicit `eye` wording exists, but the sample is too thin to justify a separate row
3. local language does **not** reliably distinguish generation I / II / III
4. country and filter-thread language are effectively absent in the useful pool

That is the shape of one immediate `core` and no round-1 `hold` rows.

## Candidate Entity Expansion

## Candidate 1: `Leica Elmarit-M 135mm f/2.8`

### Official / literature basis

Strong enough for `core`.

The family is literature-real and distinct from:

- `APO-Telyt-M 135`
- `Tele-Elmar 135`
- `Hektor 135`
- `Elmar 135`
- classic `Telyt 135`

### Mechanical distinction

Strong enough for `core`, but not for round-1 sub-rows.

The family contains internal mechanical variation around:

- generation I / II / III
- `eyes / goggles`
- filter-thread and accessory details

But the current local title set does not label those splits cleanly enough for explicit seeded children.

### Optical distinction

Strong enough for `core`.

This is Leica's `135mm f/2.8 Elmarit-M` family and is optically distinct from the `f/4` `Tele-Elmar` and `f/3.4` `APO-Telyt-M` lines.

### Market split potential

Moderate.

The broad family has enough title convergence for one row, but not enough priced depth for internal price-table splitting.

### Search-intent split potential

Strong enough for one broad family anchor.

Queries like:

- `elmarit 135`
- `elmarit-m 135`
- `135mm f2.8 elmarit`
- `m 135/2.8 elmarit`

all point toward the same family intent.

### Round-1 verdict

- `core`

## Candidate 2: `generation I / II / III`

### Official / literature basis

Real in literature.

### Mechanical distinction

Real in literature, but weak locally.

### Optical distinction

Potentially meaningful historically, but not visible enough in local seller wording.

### Market split potential

Weak in current local data.

There is no stable repeated local language such as:

- `I`
- `II`
- `III`
- `1st`
- `2nd`
- `3rd`

that can safely drive row-level normalization.

### Search-intent split potential

Weak in current local data.

### Round-1 verdict

- `보류`

## Candidate 3: `goggles / eyes`

### Official / literature basis

Real as a mechanical variant.

### Mechanical distinction

Meaningful, but not clearly a standalone family row yet.

The local pool does contain:

- `eye ELMARIT`
- `eye ELMARIT-M`

which proves buyers and sellers can name the feature.

### Optical distinction

No evidence that `eyes/goggles` should be treated as a separate optical line.

### Market split potential

Too thin in current local data.

Only `2` clean local titles carry explicit `eye` wording, and none has dependable local KRW support in the current pool.

### Search-intent split potential

Real, but thin.

This looks more like an overlay-worthy search facet than an immediate row.

### Round-1 verdict

- `overlay` / `보류`

## Candidate 4: `Canada / Germany / black / chrome / E55 / Series VII`

### Official / literature basis

Potentially real descriptive variation, but not visible enough locally.

### Mechanical distinction

Not strong enough for round-1 canonical row promotion.

### Optical distinction

No evidence of distinct optical entities in current local data.

### Market split potential

Weak.

These markers are either absent or too thin in the useful local pool.

### Search-intent split potential

Weak.

### Round-1 verdict

- `overlay`

## Contamination / Boundary Review

The following remain out-of-family and must not be mixed into `Elmarit-M 135`:

- `APO-Telyt-M 135`
- `Tele-Elmar 135`
- `Tele-Elmar-M 135`
- `Hektor 135`
- `Elmar 135`
- classic `Telyt 135`
- `Telyt-R 135`
- `Elmarit-R 135`
- `APO-Telyt-R 135`
- `APO-Telyt-R 180`
- `APO-Telyt-R 280`
- `Tele-Elmarit 90`
- accessory-only listings such as hood / case / cap / goggles-only
- third-party `135mm` lenses

One local contamination note matters here:

- `LEICA 135mm F4 TELE-ELMARIT-M sn.3415`

contains both `tele` and `elmarit`, but it is not part of the `Elmarit-M 135mm f/2.8` family and must stay outside this family.

## Round-1 Recommendation

### Immediate core candidate

Recommended immediate `core` candidate count: `1`

1. `Leica Elmarit-M 135mm f/2.8`

### Hold candidates

None recommended in round 1.

The family does not yet show a narrow internal split that is both:

- literature-real
- local-title-explicit
- and operationally safe

### Overlay axes

Keep as overlay or row-below detail:

- `black / chrome`
- `country marking`
- `eyes / goggles`
- `hood included`
- `cap included`
- `boxed`
- `case included`
- `condition`
- `original cap / hood / box / case`
- `packaging`
- `filter / filter thread / Series VII`

### Deferred / hold-back items

Do not seed yet:

- generation I / II / III
- `eyes / goggles` as a separate canonical row
- country split
- filter-thread split

## Seed Readiness

Round-1 recommendation:

- next round seed add: `yes`
- but only as a very narrow single-row add

Safest next step:

1. add `Leica Elmarit-M 135mm f/2.8` as one broad `core`
2. keep `eyes/goggles`, generations, country, and accessory detail outside seeded rows

## Final Disposition

- immediate core candidate:
  - `Leica Elmarit-M 135mm f/2.8`
- hold candidate:
  - none
- overlay:
  - `eyes / goggles`
  - `black / chrome`
  - `country marking`
  - `hood / cap / case / boxed / packaging`
  - `filter / filter thread / Series VII`
- out-of-family:
  - `APO-Telyt-M 135`
  - `Tele-Elmar 135`
  - `Tele-Elmar-M 135`
  - `Hektor 135`
  - `Elmar 135`
  - classic `Telyt 135`
  - `R 135`
  - accessories
  - third-party `135mm` lenses
