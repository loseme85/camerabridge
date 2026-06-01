# Tele-Elmar 135 Taxonomy Audit - Round 1

Date: 2026-05-08

Scope: read-heavy taxonomy audit for the Leica `Tele-Elmar 135` family. This round does not add seed rows, does not change classifier/query/search behavior, and does not change admin lookup ranking or UI. The goal is to determine whether `Tele-Elmar 135` is mature enough for explicit canonical seeding and, if so, at what granularity.

## Executive Summary

`Tele-Elmar 135` is seedable, but round-1 should stay conservative about internal splitting.

The strongest round-1 conclusion is:

1. `Leica Tele-Elmar 135mm f/4`

should be treated as the only immediate first-pass `core` entity.

There is also one narrower literature-real candidate:

1. `Leica Tele-Elmar-M 135mm f/4`

as a plausible future `hold` row, but not a round-1 second row.

Round-1 conclusion:

- immediate recommended `core` candidate count: `1`
- recommended first-pass core:
  - `Leica Tele-Elmar 135mm f/4`
- explicit future `hold` candidate:
  - `Leica Tele-Elmar-M 135mm f/4`
- `black / chrome`, `country marking`, `E39 / E46`, `hood included`, `cap included`, `boxed`, `case included`, and `packaging` stay `overlay` or `보류`
- `APO-Telyt-M 135`, `Elmarit-M 135`, `Hektor 135`, `Elmar 135`, classic `Telyt 135`, `R 135`, accessories, and third-party 135mm lenses remain out-of-family boundaries

The safest next step is a narrow seed add for `Leica Tele-Elmar 135mm f/4` only, leaving `Tele-Elmar-M 135` for a later hold audit if needed.

## Family Overview

The Leica `135mm` field is crowded and easy to contaminate:

- `Tele-Elmar 135`
- `APO-Telyt-M 135`
- `Elmarit-M 135`
- `Hektor 135`
- `Elmar 135`
- classic `Telyt 135`
- `R 135`
- accessories and third-party 135mm lenses

Unlike `APO-Telyt-M 135`, `Tele-Elmar 135` is not a pure modern single-product line. Literature and local titles suggest one broad Leica M `Tele-Elmar 135mm f/4` family with a later `Tele-Elmar-M` wording inside it.

The real round-1 question is whether that later wording is strong enough to force a second row now.

Round-1 answer: `no`. The family is ready for one broad `core`, but not yet for a second row.

## Literature / Reference Base

### Source A: Leica Wiki - `135mm f/4 Tele-Elmar`

Leica Wiki documents:

- `135mm f/4 Tele-Elmar`

with:

- production era `1965-1998`
- Leica M-bayonet mount
- `5 / 3` optical design
- filter types `E39` and `E46`
- multiple historical variants
- a late `1992-1998` telescoping-hood version explicitly named `Tele-Elmar-M`

Reference:

- [Leica Wiki - 135mm f/4 Tele-Elmar](https://wiki.l-camera-forum.com/leica-wiki.en/index.php?title=135mm_f%2F4_Tele-Elmar)

### Source B: boundary literature for successor family

The same Leica Wiki page explicitly notes:

- the `135mm f/4 Tele-Elmar` was superseded by `135mm f/3.4 ASPH Apo-Telyt-M`

This confirms `APO-Telyt-M 135` is a separate successor family, not a version inside `Tele-Elmar 135`.

Reference:

- [Leica Wiki - 135mm f/4 Tele-Elmar](https://wiki.l-camera-forum.com/leica-wiki.en/index.php?title=135mm_f%2F4_Tele-Elmar)

### Source C: boundary literature for `Elmarit-M 135`

Leica Wiki separately documents:

- `135mm f/2.8 Elmarit-M`

across multiple generations, confirming it is a different 135mm M family and must stay outside `Tele-Elmar 135`.

References:

- [Leica Wiki - 135mm f/2.8 Elmarit-M I](https://wiki.l-camera-forum.com/leica-wiki.en/index.php/135mm_f/2.8_Elmarit-M_I)
- [Leica Wiki - 135mm f/2.8 Elmarit-M II](https://wiki.l-camera-forum.com/leica-wiki.en/index.php/135mm_f/2.8_Elmarit-M_II)
- [Leica Wiki - 135mm f/2.8 Elmarit-M III](https://wiki.l-camera-forum.com/leica-wiki.en/index.php?title=135mm_f%2F2.8_Elmarit-M_III)

### Interpretation

The literature stack supports three true things:

1. `Tele-Elmar 135mm f/4` is a real Leica M family
2. `Tele-Elmar-M 135mm f/4` is literature-real as a later variant inside that family
3. `APO-Telyt-M 135`, `Elmarit-M 135`, and other `135mm` Leica lines are separate boundaries

So the round-1 question is not whether `Tele-Elmar-M` exists. The question is whether local title and market signal justify a second row now.

## Local Listing Evidence

Analysis base: `data/derived/results_resolved_v2.json`

Raw `tele-elmar` matches initially include heavy contamination from:

- `Tele-Elmarit 90`

After excluding `Tele-Elmarit 90` and keeping only `135mm` `Tele-Elmar` titles, the useful local pool becomes:

- clean local pool: `15`

### Broad price clustering

KRW-parsed local observations:

- clean local pool priced count: `0`

So round-1 cannot rely on local KRW median clustering.

That weakens confidence for internal splitting, but the title convergence is still good enough for one broad `core`.

### Local title patterns

Broad recurring titles:

- `[중고] M 135/4 Tele Elmar (Black)`
- `Leica M 135mm f4 Tele-Elmar Black`
- `LEICA 135mm F4 TELE-ELMAR sn.2106`
- `LEICA 135mm F4 TELE-ELMAR sn.2231`

Later / explicit narrow titles:

- `LEICA 135mm F4 TELE-ELMAR-M sn.3634`
- `LEICA 135mm F4 TELE-ELMAR-M sn.3596`
- `LEICA 135mm F4 TELE-ELMAR-M sn.3658`

### Local marker frequency

Repeated local modifiers:

- `m 135/4`: `4`
- `tele-elmar-m`: `3`
- `black`: `6`

Not meaningfully present in the clean local pool:

- `canada`
- `germany`
- `e39`
- `e46`
- `hood`
- `case`
- `boxed`

### Interpretation

This family shows a shape that is cleaner than `Summaron 28`, but less clean than `APO-Telyt-M 135`.

The important pattern is:

1. broad `Tele-Elmar 135` wording is stable enough for one family anchor
2. explicit `Tele-Elmar-M` wording exists and is literature-real
3. but `Tele-Elmar-M` local sample is still thin
4. generic `M 135/4 Tele Elmar` wording is ambiguous because some sellers may just be indicating M mount rather than the later telescoping-hood variant

That is the shape of one immediate `core` plus one future `hold` candidate.

## Candidate Entity Expansion

## Candidate 1: `Leica Tele-Elmar 135mm f/4`

### Official / literature basis

Strong.

This is the broad historical Leica M family consistently supported by Leica Wiki and local title language.

### Mechanical distinction

Strong enough for `core`.

This family identity remains stable even though literature documents internal variation in:

- scale color
- focusing knurl type
- filter thread
- late `Tele-Elmar-M` wording

Those are still better treated as substructure under the family than as separate round-1 rows.

### Optical distinction

Strong enough for `core`.

This is its own Leica 135mm f/4 family, distinct from:

- `APO-Telyt-M 135`
- `Elmarit-M 135`
- `Elmar 135`
- `Hektor 135`

### Market split potential

Moderate.

Local price support is missing, but title support is concentrated enough that a broad family anchor remains useful.

### Search-intent split potential

Strong enough for `core`.

Queries like:

- `tele-elmar 135`
- `tele elmar 135`
- `135 tele-elmar`
- `135mm f4 tele-elmar`
- `135mm f/4 tele-elmar`
- `m 135/4 tele-elmar`
- `135/4 tele elmar`

all point to the same Leica M 135 f/4 family in current local evidence.

### Verdict

- round-1 status: `core`

## Candidate 2: `Leica Tele-Elmar-M 135mm f/4`

### Official / literature basis

Real, but subordinate.

Literature supports it as a late variant / naming inside the `135mm f/4 Tele-Elmar` family rather than a fully separate optics family.

### Mechanical distinction

Real.

The late `Tele-Elmar-M` version is associated in literature with the telescoping hood era and later production years.

### Market split potential

Weak to moderate.

The problem is not whether the variant exists. The problem is whether local titles isolate it cleanly enough.

### Search-intent split potential

Not strong enough for a round-1 row.

Only `3` explicit `TELE-ELMAR-M` titles are visible locally, and broader seller wording like:

- `M 135/4 Tele Elmar`

is not safe enough to interpret as a distinct late-variant query rather than just M-mount shorthand.

### Verdict

- round-1 status: `hold` candidate

## Overlay vs Hold vs Deferred

### Core

- `Leica Tele-Elmar 135mm f/4`

### Hold

- `Leica Tele-Elmar-M 135mm f/4`

### Overlay

The following should stay below row level:

- `black / chrome`
- `country marking`
- `E39 / E46`
- `hood included`
- `cap included`
- `boxed`
- `case included`
- `condition`
- `original cap`
- `original hood`
- `original box`
- `original case`
- `packaging`

### Deferred / 보류

- earlier / later sub-variants below `Tele-Elmar-M`
- country-based or filter-thread-based splitting
- accessory/completeness-driven price differences

## Contamination / Boundary Review

The `Tele-Elmar 135` family must remain separate from:

- `APO-Telyt-M 135`
- `Elmarit-M 135`
- `Hektor 135`
- `Elmar 135`
- classic `Telyt 135`
- `R 135` lines including `Telyt-R`, `Elmarit-R`, and `APO-Telyt-R`
- accessory-only listings such as hood / cap / case / box / finder / goggles
- third-party `135mm` lenses

The biggest raw-data contamination risk in practice is actually `Tele-Elmarit 90`, which must be excluded before looking at `Tele-Elmar 135`.

## Final Recommendation

### Immediate core candidate

- `Leica Tele-Elmar 135mm f/4`

### Hold candidate

- `Leica Tele-Elmar-M 135mm f/4`

### Overlay

- `black / chrome`
- `country marking`
- `E39 / E46`
- `hood included`
- `cap included`
- `boxed`
- `case included`
- `condition`
- `original cap / hood / box / case`
- `packaging`

### Out-of-family boundary

- `APO-Telyt-M 135`
- `Elmarit-M 135`
- `Hektor 135`
- `Elmar 135`
- classic `Telyt 135`
- `R 135`
- accessory-only listings
- third-party 135mm lenses

## Seed Readiness

Round-1 answer:

- immediate `core` add: `yes`
- recommended first-pass scope: one row only
- future narrow hold audit: `yes` for `Tele-Elmar-M 135mm f/4`

The safest next step is:

1. add `Leica Tele-Elmar 135mm f/4` as a narrow `core`
2. leave `Leica Tele-Elmar-M 135mm f/4` for a later hold-seed audit instead of opening both rows at once
