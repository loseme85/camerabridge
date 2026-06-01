# Summaron 35 Taxonomy Audit - Round 1

Date: 2026-04-26

Scope: read-heavy taxonomy audit for the Leica `Summaron 35` family. This round does not change classifier, query parsing, query resolver, search service, admin lookup ranking, or seed files. The goal is to decide which `Summaron 35` splits are strong enough for immediate explicit-seed promotion and which should remain overlay / hold / deferred.

## Executive Summary

`Summaron 35` should not remain a single broad family in the canonical layer. The first-order split is strong:

1. `Summaron 35mm f/3.5`
2. `Summaron 35mm f/2.8`

That split is supported by:

- official / literature treatment as separate lens lines
- different production eras and compatibility variants
- different optical positioning
- clear market price separation in the current local listing pool

However, the next layer down should be treated more conservatively:

- `LTM` vs `M` is best treated as an `overlay` for now, not a separate core price-table entity
- `goggles / eyes` is search-relevant, but the current local sample is too thin to promote to core
- `f/2.8 dual-mount` looks collector-relevant and mechanically meaningful, but current priced local evidence is too sparse, so it should remain `hold`

## Recommended Round-1 Shape

### Immediate core candidates

1. `Leica Summaron 35mm f/3.5`
2. `Leica Summaron 35mm f/2.8`

### Overlay candidates

- `mount = LTM`
- `mount = M`
- `eyes/goggles = yes`
- `eyes/goggles = no`

### Hold candidates

- `Summaron 35mm f/2.8 dual-mount`
- `Summaron 35mm f/2.8 with goggles` as a possible future price split
- `Summaron 35mm f/3.5 with goggles` as a possible future search-facing sub-entity

### Deferred / collector-only for later rounds

- `A36` vs `E39`
- feet vs metric scales
- black paint / finish-era subtypes
- minor catalog / production-lot subtypes

## Family Overview

The Leica `Summaron 35` family spans at least two materially different mainstream lens lines:

- `3.5cm f/3.5 Summaron`
- `35mm f/2.8 Summaron`

Leica Wiki treats the `3.5cm f/3.5` line as a distinct lens family with screw-thread and M-bayonet variants, plus M3 versions with and without goggles. Summichronica separately documents the `35mm f/2.8` line as a later product introduced at Photokina 1958, with its own M2 / M3 / dual-mount variants and a modest optical-performance improvement attributed to lanthanum glass.

That is enough to reject a single broad `Summaron 35` canonical entity.

## Literature / Reference Base

### Source A: Leica Wiki - `Summaron f= 3.5 cm 1:3.5`

Key points:

- production era includes both screw-thread and M-bayonet
- variants include A36 / E39 and M3 versions with or without goggles
- closest focus is 1 meter
- Leica Wiki also includes historical street-price notes by mount / M3 variant

Reference:

- https://wiki.l-camera-forum.com/leica-wiki.en/index.php/Summaron_f%3D_3.5_cm_1%3A3.5

### Source B: Summichronica - `35MM BAYONET MOUNT LENSES`

Key points:

- `3.5cm f/3.5 Summaron` for M is documented in four versions:
  - M3 without goggles
  - M3 with removable goggles
  - M2 without goggles
  - fixed-focus postal version
- `35mm f/2.8 Summaron` is documented as a later line introduced at Photokina 1958
- `35mm f/2.8 Summaron` is described as closely related to the earlier design but improved by a little over half a stop due to lanthanum glass
- `35mm f/2.8 Summaron` has M2, M3-goggles, and postal / special variants, with screw and bayonet versions available at introduction

Reference:

- https://www.summichronica.com/bayonet-mount-lenses-35mm

## Local Listing Evidence

Analysis base: `data/derived/results_resolved_v2.json`

Observed `Summaron 35` lens records in the current local resolved listing pool:

- total observed lens records: `124`

### Current local buckets

| Bucket | Count | Priced | Median KRW | Audit note |
| --- | ---: | ---: | ---: | --- |
| `f/3.5 LTM` | 19 | 19 | 1,000,000 | strong evidence that screw-mount listings exist as their own search flavor |
| `f/3.5 M no goggles` | 50 | 16 | 1,075,000 | largest `f/3.5` bucket |
| `f/3.5 M goggles` | 4 | 3 | 900,000 | thin sample, but clearly a distinct compatibility form |
| `f/2.8 M no goggles` | 36 | 17 | 2,480,000 | largest `f/2.8` bucket |
| `f/2.8 M goggles` | 7 | 3 | 1,800,000 | lower than non-goggles in current local pool, but sample is thin |
| `f/2.8 dual-mount / LTM-coded` | 8 | 2 | 2,175,000 | interesting, but not enough priced evidence to define a stable core split |

### What the local data says

1. `f/3.5` and `f/2.8` are clearly different market bands.
   - `f/3.5` sits roughly around `1.0M KRW`
   - `f/2.8` sits roughly around `2.2M - 2.5M KRW`

2. `LTM` vs `M` for `f/3.5` is not showing a strong enough price break to require separate core entities.
   - `f/3.5 LTM` median: `1.0M`
   - `f/3.5 M no goggles` median: `1.075M`

3. `goggles / eyes` matters in search language and mechanical fit, but the current local evidence is still thin for price-table core promotion.

4. `f/2.8 dual-mount` looks meaningful and collectible, but the local priced sample is too sparse to lock it as core in this round.

## Candidate Entity Expansion

## Candidate 1: Leica Summaron 35mm f/3.5

### Official / literature basis

Strong.

Leica Wiki documents `Summaron f= 3.5 cm 1:3.5` as its own lens line with screw-thread and M-bayonet production, plus M3 versions with and without goggles.

### Mechanical distinction

Strong relative to `f/2.8`.

- different maximum aperture
- different production window
- 1 meter close focus
- documented M3 / M2 compatibility variants

### Optical distinction

Strong enough.

Even if related historically, this is not just a mount-overlay version of the `f/2.8`; it is the older, slower line.

### Market split potential

Strong.

The local price band is materially below `f/2.8`, and the listing pool is large enough to treat it as its own price-table anchor.

### Search-intent split potential

Strong.

Users and dealers often search `summaron 35 3.5`, `ltm summaron 35`, or `35/3.5 summaron`.

### Final decision

`core`

### One-line reason

`f/3.5` is a clearly distinct historical and market lens line with enough local evidence to stand as its own canonical core entity.

## Candidate 2: Leica Summaron 35mm f/2.8

### Official / literature basis

Strong.

Summichronica documents `35mm f/2.8 Summaron` as a later lens introduced at Photokina 1958, with screw and bayonet availability from introduction and distinct M2 / M3 usage variants.

### Mechanical distinction

Strong.

- faster aperture
- separate production line
- different compatibility variants
- 65 cm close focus on the M3 goggles version versus 1 meter on the M2 non-goggles version

### Optical distinction

Strong enough.

The line is described as closely related to the older design but optically improved by a little over half a stop due to lanthanum glass. That is enough for a separate canonical price-group anchor.

### Market split potential

Strong.

The local market band is materially above `f/3.5`, and the listing volume is healthy enough to support a core entity.

### Search-intent split potential

Strong.

Users and dealers do search for `35/2.8 Summaron`, often separately from `35/3.5`.

### Final decision

`core`

### One-line reason

`f/2.8` is a later and meaningfully distinct Summaron 35 line with a clearly different local market price band.

## Candidate 3: `LTM` vs `M` as split axis

### Official / literature basis

Real, but not sufficient by itself for round-1 core promotion.

Leica Wiki explicitly lists screw-thread and M-bayonet for `f/3.5`, and Summichronica notes screw and bayonet availability for `f/2.8`.

### Mechanical distinction

Yes.

Mount and camera-body compatibility differ materially.

### Optical distinction

Usually no.

The mount change does not, by itself, imply a different optical design or a new mainstream lens family.

### Market split potential

Weak-to-moderate in current local evidence.

For `f/3.5`, local medians are close enough that mount alone does not justify separate core entities in round 1.

### Search-intent split potential

Yes.

Queries like `ltm summaron 35` are real and useful, but that is compatible with an overlay approach.

### Final decision

`overlay`

### One-line reason

Mount matters for lookup and compatibility, but current evidence does not require a separate price-table core entity per mount.

## Candidate 4: `goggles / eyes`

### Official / literature basis

Strong as a product form.

Both Leica Wiki and Summichronica treat goggled / RF versions as real catalog variants, especially for M3 usage.

### Mechanical distinction

Strong.

- dedicated viewing / framing unit
- M3-specific usability and handling differences
- removable goggles in some `f/3.5` forms
- fixed or integrated goggle-associated market identity in `f/2.8` listings

### Optical distinction

Usually no at the lens-core level.

The goggle assembly changes framing and rangefinder coupling behavior more than it changes the core optical formula.

### Market split potential

Possible, but not yet strong enough in the current local dataset.

- `f/2.8` non-goggles median is materially above `f/2.8` goggles in current local data
- `f/3.5` goggles also seem somewhat lower than the main `f/3.5` pool

But the priced sample counts are still thin.

### Search-intent split potential

Yes.

Buyers do search `eye`, `eyes`, `goggles`, and this should remain visible in normalization.

### Final decision

`overlay` for now, with `hold` potential for later sub-splitting

### One-line reason

Goggles clearly matter in search and mechanics, but the current local price evidence is not yet healthy enough for immediate core promotion.

## Candidate 5: `f/2.8 dual-mount`

### Official / literature basis

Moderate.

The literature confirms screw and bayonet availability and collector-facing subtypes, and local titles explicitly use `Dual-Mount`.

### Mechanical distinction

Meaningful.

Dual-mount copies clearly represent a usability / compatibility subtype rather than a random dealer wording variant.

### Optical distinction

Not clearly separate.

This looks more like a mount / chassis / compatibility subtype than a fully separate optical family.

### Market split potential

Unclear in the current local pool.

The local priced sample is too sparse to make a stable price-table call.

### Search-intent split potential

Real.

`dual-mount` is a clear buyer / collector query.

### Final decision

`hold`

### One-line reason

Dual-mount looks like a real collector-facing subtype, but the local priced evidence is too thin to call it core yet.

## Candidate 6: filter-thread / scale / finish-era micro-variants

Examples:

- `A36` vs `E39`
- feet vs metric
- black paint / late yellow-scale variants

### Official / literature basis

These are documented, but they behave more like collector overlays than round-1 canonical anchors.

### Mechanical / optical distinction

Mostly weak at the mainstream entity level.

### Market split potential

May matter in rarefied collector markets, but not enough evidence here for round-1 core taxonomy.

### Final decision

`보류`

### One-line reason

Collector nuance is real, but this is too fine-grained for round-1 core seeding.

## Round-1 Recommendation

### Recommended immediate core entity count

`2`

Recommended round-1 core entities:

1. `Leica Summaron 35mm f/3.5`
2. `Leica Summaron 35mm f/2.8`

### Recommended overlays

- `mount: LTM / M`
- `goggles: yes / no`

### Recommended holds

- `Leica Summaron 35mm f/2.8 dual-mount`
- `Leica Summaron 35mm f/2.8 with goggles` as a future possible price split
- `Leica Summaron 35mm f/3.5 with goggles` as a future possible search-facing sub-entity

## What Should Still Wait

Do not seed these as round-1 core entities yet:

- `f/3.5 LTM` as its own price-table core
- `f/3.5 M` as its own price-table core
- `f/2.8 LTM / dual-mount` as immediate core
- `eyes / goggles` as immediate price-table core
- `A36 / E39` filter-thread micro-variants
- finish / scale collector variants

## Is This Ready For Seed Addition?

Yes, but only narrowly.

### Safe next round

Seed addition is justified for:

1. `Leica Summaron 35mm f/3.5`
2. `Leica Summaron 35mm f/2.8`

### Not yet safe for broad sub-split seeding

Do not immediately seed:

- `LTM` vs `M` as separate core entities
- `goggles` as separate core entities
- `dual-mount` as core

Those should remain overlay / hold until we either:

- get stronger local priced evidence
- or decide that collector-market exactness matters more than current mainstream price-table stability

## Final Recommendation

`Summaron 35` is ready to enter the explicit-seed system, but only with a conservative round-1 shape:

- `Summaron 35mm f/3.5` -> `core`
- `Summaron 35mm f/2.8` -> `core`
- mount / goggles -> overlay
- dual-mount and collector subtypes -> hold / deferred

That keeps the taxonomy sharp enough for search and price-table use without prematurely hard-coding collector-level fragmentation.
