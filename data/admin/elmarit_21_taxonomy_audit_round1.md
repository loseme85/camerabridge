# Elmarit 21 Taxonomy Audit - Round 1

Date: 2026-05-01

Scope: read-heavy taxonomy audit for the Leica `Elmarit 21` family. This round does not add seed rows, does not change classifier/query/search behavior, and does not change admin lookup ranking or UI. The goal is to determine whether `Elmarit 21` is mature enough for explicit canonical seeding and, if so, at what granularity.

## Executive Summary

`Elmarit 21` is seedable, and unlike `Elmarit 35`, it already shows a real two-line split in local data.

The strongest round-1 conclusion is:

1. `Leica Elmarit-M 21mm f/2.8`
2. `Leica Elmarit-M 21mm f/2.8 ASPH`

should be treated as separate first-pass `core` entities.

Why this is stronger than a broad single-line family:

- literature treats the non-ASPH and ASPH lenses as separate Leica M product lines
- local title language already separates them cleanly
- local KRW pricing also separates them strongly

Round-1 conclusion:

- immediate recommended `core` candidate count: `2`
- recommended first-pass core:
  - `Leica Elmarit-M 21mm f/2.8`
  - `Leica Elmarit-M 21mm f/2.8 ASPH`
- pre-ASPH internal substructure such as early non-rangefinder / later rangefinder, filter-thread changes, and hood revisions should stay below round-1 seed level
- `Super-Angulon 21`, `Super-Elmar-M 21`, and `Tri-Elmar 16-18-21` should be treated as out-of-family contamination, not internal `Elmarit 21` splits

## Family Overview

The `21mm` Leica field is structurally messy unless we separate adjacent families early:

- `Super-Angulon 21`
- `Super-Elmar-M 21`
- `Tri-Elmar 16-18-21`
- `Elmarit-R 21`
- `Super-Vario-Elmarit-SL` and other SL contamination

Once those are excluded, the local M-side `Elmarit 21` field becomes much cleaner than `Elmarit 35`.

The first taxonomic question is not collector shorthand. It is whether the non-ASPH and ASPH `Elmarit-M 21` lines are strong enough to be distinct canonical entities.

Round-1 answer: `yes`.

## Literature / Reference Base

### Source A: Leica Wiki - `21mm f/2.8 Elmarit M`

Leica Wiki documents the non-ASPH `21mm f/2.8 Elmarit-M` as a distinct Leica M line with:

- production era `1980-1997`
- `8 / 6` optical design
- early non-rangefinder close-focus variant and later rangefinder-coupled variant
- filter / hood revisions across the production run

Reference:

- https://wiki.l-camera-forum.com/leica-wiki.en/index.php/21mm_f/2.8_Elmarit_M

### Source B: Leica Wiki - `21mm f/2.8 ASPH Elmarit-M`

Leica Wiki documents the ASPH successor as a separate product line with:

- production era `1997-2010`
- `9 / 7` optical design with aspherical element
- stable `E55` filter arrangement
- explicit `ASPH.` inscription

Reference:

- https://wiki.l-camera-forum.com/leica-wiki.en/index.php?title=21mm_f%2F2.8_ASPH_Elmarit-M

### Source C: Boundary references for out-of-family contamination

The nearby `21mm` Leica M field includes:

- `21mm f/3.4 Super-Angulon`
- `21mm f/3.4 Super-Elmar-M`

These are separate product names and should not be treated as `Elmarit 21` internal variants.

References:

- https://wiki.l-camera-forum.com/leica-wiki.en/index.php/21mm_f3.4_Super-Angulon
- https://wiki.l-camera-forum.com/leica-wiki.en/index.php?title=21mm_f%2F3.4_Super-Elmar-M

## Local Listing Evidence

Analysis base: `data/derived/results_resolved_v2.json`

After excluding obvious contamination from:

- `Tri-Elmar`
- `Super-Angulon`
- `Super-Elmar`
- `Elmarit-R`
- `Vario-Elmarit-SL`
- non-21 `Elmarit`
- `Summicron` / `Summilux` false matches

the useful local `Elmarit 21` pool is:

- clean local pool: `22`
- non-ASPH bucket: `11`
- ASPH bucket: `11`

### Price clustering

KRW-parsed local medians:

| Bucket | Count | KRW-priced | Median KRW | Audit note |
| --- | ---: | ---: | ---: | --- |
| `Elmarit-M 21mm f/2.8` | 11 | 6 | ~1.39M KRW | clear pre-ASPH cluster |
| `Elmarit-M 21mm f/2.8 ASPH` | 11 | 4 | ~2.83M KRW | clear ASPH cluster |

### Local title patterns

Non-ASPH examples:

- `[중고] M 21/2.8 Elmarit (Black)`
- `LEICA 21mm F2.8 ELMARIT-M sn.3456`
- `LEICA 21mm F2.8 ELMARIT-M sn.3685`

ASPH examples:

- `[중고] M 21/2.8 Elmarit ASPH (Silver)`
- `[중고] M21/2.8 Elmarit ASPH (Black)`
- `LEICA 21mm F2.8 ASPH ELMARIT-M sn.3925`

### Interpretation

This family clears the round-1 threshold on two independent axes:

1. local title language separates `ASPH` and non-`ASPH` directly
2. local market pricing separates them strongly

Unlike collector-only shorthand, the split is not inferred indirectly. It is written plainly in dealer titles.

## Candidate Entity Expansion

## Candidate 1: `Leica Elmarit-M 21mm f/2.8`

### Official / literature basis

Strong.

The non-ASPH `21mm f/2.8 Elmarit-M` is a documented Leica M line with its own production era, optical formula, and internal mechanical evolution.

### Mechanical distinction

Strong enough for `core`.

Even before we care about sub-versions, the non-ASPH line is mechanically distinct from the ASPH successor:

- no `ASPH.` naming
- different filter / hood conventions across the line
- earlier internal close-focus / rangefinder-coupling evolution

### Optical distinction

Strong enough for `core`.

The literature treats this as a separate non-ASPH optical design from the later ASPH lens.

### Market split potential

Strong.

The local priced subset centers around roughly `1.39M KRW`, clearly below the ASPH cluster.

### Search-intent split potential

Strong.

Users and dealers explicitly write:

- `21/2.8 Elmarit`
- `21mm F2.8 Elmarit-M`

without `ASPH`, and those titles are operationally distinct from the ASPH titles.

### Final decision

`core`

### One-line reason

The non-ASPH `Elmarit-M 21` is a distinct Leica M line with stable title language and a clearly separate local price band.

## Candidate 2: `Leica Elmarit-M 21mm f/2.8 ASPH`

### Official / literature basis

Strong.

The ASPH version is explicitly documented as a successor line with different optics and separate production era.

### Mechanical distinction

Strong enough for `core`.

It has:

- explicit `ASPH.` naming
- stable `E55` filter arrangement
- different barrel / weight profile from the pre-ASPH line

### Optical distinction

Strong enough for `core`.

The aspherical redesign is not a cosmetic variation. It is a real optical line change.

### Market split potential

Strong.

The local priced subset centers around roughly `2.83M KRW`, about double the non-ASPH median.

### Search-intent split potential

Strong.

Dealers explicitly write:

- `21/2.8 Elmarit ASPH`
- `21mm F2.8 ASPH Elmarit-M`

### Final decision

`core`

### One-line reason

The ASPH `Elmarit-M 21` is a literature-real and market-real successor line that local dealer titles already separate cleanly.

## Candidate 3: pre-ASPH early non-rangefinder / later rangefinder-coupled split

### Official / literature basis

Real.

Leica Wiki notes an internal break inside the pre-ASPH line around the focusing / rangefinder behavior and filter / hood arrangement.

### Mechanical distinction

Real but not round-1 ready.

This is a genuine sub-line, not mere packaging noise.

### Optical distinction

Weak as a separate market entity signal.

The stronger distinction here is mechanical / usability-oriented, not a top-level optical family rename.

### Market split potential

Unclear from local data.

### Search-intent split potential

Weak locally.

The local titles do not repeatedly expose:

- early non-RF
- later RF
- E39 vs E60

at a level strong enough to open immediate seed rows.

### Final decision

`hold`

### One-line reason

The split is literature-real, but local title language is still too weak for first-pass canonical seeding.

## Candidate 4: black / silver finish

### Official / literature basis

Real finish variation, but not a separate optical line.

### Mechanical distinction

Not enough for standalone canonical entities.

### Optical distinction

None.

### Market split potential

Some ASPH silver premium may exist, but round-1 evidence is too thin.

### Search-intent split potential

Visible in local titles, but still best treated as metadata.

### Final decision

`overlay`

### One-line reason

Finish wording appears in titles but behaves like metadata, not a stable first-pass canonical split.

## Candidate 5: coding / country marking / packaging / finder bundle

### Official / literature basis

Mixed and weak.

### Mechanical distinction

Weak or bundle-driven.

Finder / hood / package completeness can matter operationally, but they do not define the lens line itself.

### Optical distinction

None.

### Market split potential

Unclear and likely secondary.

### Search-intent split potential

Too weak for round-1.

### Final decision

`overlay` or `보류`

### One-line reason

These are better treated as metadata or later audit topics than immediate canonical rows.

## Candidate 6: `Super-Angulon 21`, `Super-Elmar 21`, `Tri-Elmar 21` boundary

### Official / literature basis

Strongly separate.

These are not `Elmarit 21` sub-lines.

### Final decision

`보류` inside this family, meaning out-of-family contamination to exclude

### One-line reason

They belong to separate Leica naming families and should not be allowed to widen `Elmarit 21`.

## Round-1 Recommendation

Recommended immediate `core` candidate count: `2`

Recommended first-pass seed rows:

1. `Leica Elmarit-M 21mm f/2.8`
2. `Leica Elmarit-M 21mm f/2.8 ASPH`

## What Should Stay Below Seed Level For Now

- pre-ASPH internal early / late mechanical split
- filter-thread / hood / barrel micro-variants
- black / silver finish
- coding
- country marking
- completeness / finder bundle wording

## Can The Next Round Move To Seed Addition?

`Yes`

This family is materially stronger than `Elmarit 35`.

Why the answer is yes:

1. literature clearly supports a real non-ASPH / ASPH split
2. local title language mirrors that split directly
3. local price clustering also supports it

So the safest next round would be a narrow seed addition round with only:

- `Leica Elmarit-M 21mm f/2.8`
- `Leica Elmarit-M 21mm f/2.8 ASPH`

and no early/late pre-ASPH sub-splits yet.
