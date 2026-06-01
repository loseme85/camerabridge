# Summicron 90 Taxonomy Audit - Round 1

Date: 2026-04-29

Scope: read-heavy taxonomy audit for the Leica `Summicron 90` family. This round does not add seed rows, does not change classifier/query/search behavior, and does not change admin lookup ranking or UI. The goal is to determine whether `Summicron 90` is mature enough for explicit canonical seeding and, if so, at what granularity.

## Executive Summary

`Summicron 90` is seedable, but only if we keep the round-1 split conservative.

The strongest immediate structure is:

1. `Leica Summicron-M 90mm f/2` (classic M line)
2. `Leica APO-Summicron-M 90mm f/2 ASPH`

Everything else is either too niche, too weakly labeled in local listings, or too close to collector/micro-variant territory for round-1 `core`.

Round-1 conclusion:

- immediate recommended `core` candidate count: `2`
- recommended first-pass cores:
  - `Leica Summicron-M 90mm f/2`
  - `Leica APO-Summicron-M 90mm f/2 ASPH`
- `Canada`, `black/silver`, `E49/E55`, `6bit`, `titanium`, `black paint` should stay below first-pass core level
- early `1:2 / 90 Summicron` Visoflex line is real, but should not be promoted into round-1 core

## Family Overview

The `90mm` Leica landscape is especially easy to contaminate because titles often mingle:

- `Elmar 90`
- `Elmarit 90`
- `Tele-Elmarit 90`
- `Macro-Elmar-M 90`
- `APO-Summicron-M 90`
- `Summicron-R 90`
- `Summicron-SL 90`

After filtering those out, the remaining `Summicron 90` evidence suggests two strong user-facing product lines:

- a non-APO classic `Summicron-M 90`
- a later `APO-Summicron-M 90 ASPH`

Within those lines, literature does show substructure, but current local title language is not strong enough to justify aggressive round-1 splitting.

## Literature / Reference Base

### Source A: Leica Wiki - `90mm f/2 Summicron-M III`

This page documents the classic M-bayonet `Summicron-M 90` line:

- production era `1980-1998`
- M-bayonet
- `5 / 4`
- black, silver, and ELC variants
- first version with hood that covers the aperture ring when collapsed
- filter split `E49 (1st)` and `E55 (2nd)`

This is the strongest literature basis for the mainstream classic `Summicron-M 90` line.

Reference:

- https://wiki.l-camera-forum.com/leica-wiki.en/index.php?title=90mm_f%2F2_Summicron-M_III

### Source B: Leica Wiki - `90mm f/2 Summicron-M II`

This page appears to cover effectively the same classic late M line, but in a shorter / less complete form:

- production era `1982-1998`
- `5 / 4`
- black and silver
- E55 form

For taxonomy purposes, this reinforces that the classic late `Summicron-M 90` exists as a coherent product line even if internal version labeling is inconsistent across references.

Reference:

- https://wiki.l-camera-forum.com/leica-wiki.en/index.php?title=90mm_f%2F2_Summicron-M_II

### Source C: Leica Wiki - `90mm f/2 ASPH Apo-Summicron-M`

This page documents the later APO line:

- production era `1998-current`
- M-bayonet
- `5 / 5`
- black, silver, titanium, black paint variants
- explicit `APO`, `ASPH`, built-in telescopic hood

This is clearly not a cosmetic variant of the classic `Summicron-M 90`. It is a separate optical and market line.

Reference:

- https://wiki.l-camera-forum.com/leica-wiki.en/index.php/90mm_f/2_ASPH_Apo-Summicron-M

### Source D: Leica Wiki - `1:2 / 90 Summicron`

This page documents an earlier `1960` line:

- production year `1960`
- `6 / 6`
- Visoflex II / III mount context
- chrome / black variants

This is a real historical Leica 90mm `Summicron`, but it behaves more like a collector / Visoflex specialty line than a mainstream M-system `Summicron 90` seed candidate.

Reference:

- https://wiki.l-camera-forum.com/leica-wiki.en/index.php/1%3A2_/_90_Summicron

## Local Listing Evidence

Analysis base: `data/derived/results_resolved_v2.json`

After excluding obvious contamination from:

- `Summicron-SL 90`
- `Summicron-R 90`
- non-90 Summicrons
- `Elmarit`, `Macro-Elmar`, `Tele-Elmarit`

the useful local pool is approximately:

- `classic Summicron-M 90`: `31` listings
- `APO-Summicron-M 90`: `39` listings

### Price clustering

KRW-only parsed medians from local `price_raw`:

| Bucket | Count | KRW-priced | Median KRW | Audit note |
| --- | ---: | ---: | ---: | --- |
| classic `Summicron-M 90` | 31 | 15 | ~1.78M KRW | stable mid-tier classic line |
| `APO-Summicron-M 90 ASPH` | 39 | 21 | ~3.68M KRW | clear premium modern line |

This is exactly the kind of market separation that supports separate canonical cores.

### Local title patterns

Classic examples:

- `[중고] M 90/2 Summicron (Black)`
- `[중고] M 90/2 Summicron Canada (Silver)`
- `LEICA 90mm F2 SUMMICRON-M sn.3703`

APO examples:

- `[중고] M 90/2 Summicron APO (Black)`
- `[중고] APO M 90/2 Summicron ASPH 6bit (Black)`
- `LEICA 90mm F2 ASPH APO-SUMMICRON-M sn.3924`

### Interpretation

The local dataset strongly supports a first-pass split between:

- classic non-APO `Summicron-M 90`
- `APO-Summicron-M 90 ASPH`

By contrast, internal classic distinctions like:

- `Canada`
- `E49`
- `E55`
- subtle barrel/version differences

do not have equally strong and repeatable title-level support.

## Candidate Entity Expansion

## Candidate 1: `Leica Summicron-M 90mm f/2`

### Official / literature basis

Strong.

The late M-bayonet `Summicron-M 90` line is clearly documented on Leica Wiki as a coherent product family.

### Mechanical distinction

Strong enough for `core`.

This is a dedicated classic M 90mm Summicron line with stable size, mount, and handling identity distinct from the APO successor.

### Optical distinction

Strong enough for `core`.

The classic line is `5 / 4`, while the APO successor is `5 / 5`. That is not a trivial cosmetic difference.

### Market split potential

Strong.

The local median around `1.78M KRW` is well below the APO line and forms a usable price-table cluster.

### Search-intent split potential

Strong.

Users and dealers explicitly search / list:

- `M 90/2 Summicron`
- `Summicron 90`
- `Summicron Canada`

Even when subtype wording is thin, the non-APO line is still a stable user-facing product concept.

### Final decision

`core`

### One-line reason

Classic `Summicron-M 90` is a distinct optical and market line with enough local title support to be a first-pass core canonical entity.

## Candidate 2: `Leica APO-Summicron-M 90mm f/2 ASPH`

### Official / literature basis

Very strong.

This is explicitly documented as `APO`, `ASPH`, post-1998, and materially different from the classic line.

### Mechanical distinction

Strong.

The lens has a clearly different physical identity, built-in telescopic hood, and later modern M construction.

### Optical distinction

Very strong.

The APO/ASPH optical identity is explicit in both Leica Wiki and local listing language.

### Market split potential

Very strong.

The local median near `3.68M KRW` is materially separated from the classic line.

### Search-intent split potential

Very strong.

Users and dealers explicitly search / list:

- `Summicron APO 90`
- `APO-Summicron-M 90`
- `90/2 Summicron APO`

### Final decision

`core`

### One-line reason

`APO-Summicron-M 90 ASPH` is an unmistakably separate product line in literature, search intent, and market pricing, so it should be its own core canonical entity.

## Candidate 3: classic `Summicron-M 90` internal E49 / E55 split

### Official / literature basis

Real.

Leica Wiki explicitly notes:

- `E49` first version
- `E55` second version

### Mechanical distinction

Moderate.

There is real barrel / hood / filter-thread distinction inside the classic line.

### Optical distinction

Unclear-to-moderate.

The literature supports internal versioning, but not a strongly separate user-facing optical family in the same way as `APO` vs non-`APO`.

### Market split potential

Possible, but unproven in local data.

### Search-intent split potential

Weak in the current local pool.

Current titles rarely expose `E49` or `E55` directly.

### Final decision

`hold`

### One-line reason

The classic internal version split is real, but current local title language is too weak for a round-1 core split.

## Candidate 4: `Canada` classic Summicron 90

### Official / literature basis

Weak as a separate canonical line.

`Canada` is visible in titles, but that is usually a production-location / engraving cue, not a stable standalone Leica family branch.

### Mechanical distinction

Weak.

### Optical distinction

Weak.

### Market split potential

Possible collector relevance, but not enough for first-pass core seeding.

### Search-intent split potential

Moderate.

Some dealers do title `Summicron Canada`, and local listings include several such examples.

### Final decision

`overlay`

### One-line reason

`Canada` is a useful alias or metadata cue inside the classic line, not a round-1 separate canonical entity.

## Candidate 5: APO line internal 6bit / titanium / black paint / silver

### Official / literature basis

Real.

The Leica Wiki page lists:

- black
- silver/chrome
- titanium
- black paint

and local titles often expose `6bit`.

### Mechanical distinction

Weak-to-moderate.

These are real variants, but not strong enough yet to override the dominant APO line identity.

### Optical distinction

Weak.

### Market split potential

Possible for titanium / black paint, but current local evidence is too sparse for first-pass splitting.

### Search-intent split potential

Moderate.

### Final decision

`hold`

### One-line reason

The APO line clearly has internal collectible variants, but round 1 should preserve them below the core APO row.

## Candidate 6: `1:2 / 90 Summicron` Visoflex line

### Official / literature basis

Strong historically.

It is a real Leica `Summicron 90` line with distinct literature documentation.

### Mechanical distinction

Very strong.

It is tied to the Visoflex system and does not behave like the later mainstream `Summicron-M 90`.

### Optical distinction

Strong.

`6 / 6` and specialized mount context make it historically distinct.

### Market split potential

Collector-specific and likely real, but current local listing support is effectively absent.

### Search-intent split potential

Weak in the current local pool.

### Final decision

`보류`

### One-line reason

This is a real historical line, but it belongs more to collector-specialist taxonomy than a safe first-pass seed round.

## Candidate 7: finish / feet-meters / engraving / boxed completeness

### Official / literature basis

Real at metadata level, weak at canonical entity level.

### Mechanical distinction

Weak.

### Optical distinction

None.

### Market split potential

Collector-sensitive, but listing-structure dependent.

### Search-intent split potential

Weak.

### Final decision

`overlay` or `보류` depending on subtype

### One-line reason

These are secondary presentation / completeness signals, not round-1 core entities.

## Recommended Round-1 Taxonomy

### Recommended immediate `core`

1. `Leica Summicron-M 90mm f/2`
2. `Leica APO-Summicron-M 90mm f/2 ASPH`

### Recommended `hold`

- classic `E49 / E55` split
- APO internal collectible variants (`6bit`, `titanium`, `black paint`, etc.)

### Recommended `overlay`

- `Canada`
- finish (`black`, `silver`)
- mount / metadata / engraving nuance
- boxed / completeness

### Recommended `보류`

- `1:2 / 90 Summicron` Visoflex line
- collector-only subtyping not visible in current listing language

## Relationship Between Classic Summicron 90 and APO 90

This should be made explicit:

- `APO-Summicron-M 90 ASPH` is **not** just a finish or minor revision of classic `Summicron-M 90`
- it is a separate major line with different optical identity, pricing, and search intent

So for canonical seeding purposes, it should become its own `core` row rather than being treated as a sub-variant folded into one generic `Summicron 90`.

## Seed-Readiness Verdict

### Can this family move to explicit seed next round?

`Yes`

### Recommended first seed shape

A conservative but useful next round would add exactly two `core` rows:

1. `Leica Summicron-M 90mm f/2`
2. `Leica APO-Summicron-M 90mm f/2 ASPH`

and stop there.

### Why this is safe

Because both lines are:

- literature-distinct
- title-distinct
- price-distinct

while the remaining substructure is still too weakly labeled for aggressive splitting.
