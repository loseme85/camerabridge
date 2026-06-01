# Super-Elmar 21 Taxonomy Audit - Round 1

Date: 2026-05-01

Scope: read-heavy taxonomy audit for the Leica `Super-Elmar 21` family. This round does not add seed rows, does not change classifier/query/search behavior, and does not change admin lookup ranking or UI. The goal is to determine whether `Super-Elmar 21` is mature enough for explicit canonical seeding and, if so, at what granularity.

## Executive Summary

`Super-Elmar 21` is seedable, and round-1 should keep it as a broad single-line family.

The strongest first-pass recommendation is:

1. `Leica Super-Elmar-M 21mm f/3.4 ASPH`

Round-1 conclusion:

- immediate recommended `core` candidate count: `1`
- recommended first-pass core:
  - `Leica Super-Elmar-M 21mm f/3.4 ASPH`
- `6bit` stays `overlay`
- `black / silver / country marking / special edition / anniversary / titanium / boxed completeness` stay `overlay` or `보류`
- `Elmarit 21`, `Super-Angulon 21`, and `Tri-Elmar 16-18-21` remain out-of-family boundary cases, not internal `Super-Elmar 21` splits

## Family Overview

The `21mm` Leica wide-angle field contains several close neighboring families:

- `Elmarit 21`
- `Super-Angulon 21`
- `Super-Elmar 21`
- `Tri-Elmar 16-18-21`
- `Elmarit-R 21`
- `SL` / `Super-Vario` contamination

For canonical purposes, `Super-Elmar 21` needs to stay narrow. Once boundary families are excluded, the local M-side pool becomes notably clean.

The first round-1 taxonomic question is whether there are major internal splits worth seeding now.

Round-1 answer: `no`.

This family behaves like a modern single-line Leica M product.

## Literature / Reference Base

### Source A: Leica Wiki - `21mm f/3.4 Super-Elmar-M`

Leica Wiki documents the lens as a distinct Leica M line with:

- production era `2011-current`
- `8 / 7` optical design
- `2` aspherical surfaces
- `E46` filter thread
- Leica M bayonet with `6-bit` coding
- inscription `LEICA SUPER-ELMAR-M 21mm 1:3.4 / 21 ASPH. E46`

Reference:

- https://wiki.l-camera-forum.com/leica-wiki.en/index.php?title=21mm_f%2F3.4_Super-Elmar-M

### Source B: Leica Camera - `Super-Elmar-M 21 f/3.4 ASPH`

Leica's current product description presents this as a single modern M-lens line with:

- compact 21mm M design
- `0.7m` close focus
- `E46` filter thread
- supplied rectangular metal hood

Reference:

- https://leica-camera.com/en-US/photography/lenses/m/super-elmar-m-21mm-f3-4-asph-black

## Local Listing Evidence

Analysis base: `data/derived/results_resolved_v2.json`

After excluding obvious contamination from:

- `Elmarit`
- `Super-Angulon`
- `Tri-Elmar`
- `SL` / `Super-Vario`
- non-21 `Super-Elmar`
- `Summicron` / `Summilux` false matches

the useful local `Super-Elmar 21` pool is:

- clean local pool: `29`

### Price clustering

KRW-parsed local medians:

| Bucket | Count | KRW-priced | Median KRW | Audit note |
| --- | ---: | ---: | ---: | --- |
| `Super-Elmar-M 21mm f/3.4 ASPH` | 29 | 11 | ~2.98M KRW | stable single-line cluster |

Observed price range in KRW-priced subset:

- min: `2.50M KRW`
- max: `3.30M KRW`

### Local title patterns

Representative local titles:

- `Leica M 21mm f3.4 Super-Elmar 6bit Black`
- `[위탁] M 21/3.4 Super Elmar ASPH 6bit (Black)`
- `[중고] M 21/3.4 Super Elmar ASPH 6bit (Black)`
- `LEICA 21mm F3.4 ASPH SUPER-ELMAR-M sn.4315`
- `LEICA 21mm F3.4 SUPER-ELMAR-M sn.4181`

### Local marker frequency

Repeated local modifiers:

- `6bit`: `7`
- `black`: `7`

Not meaningfully present in the clean local pool:

- `silver`
- `germany`
- `canada`
- `special`
- `anniversary`
- `titanium`

### Interpretation

This family is cleaner than many older Leica lines:

1. title language converges on one modern line name
2. local pricing forms one usable cluster
3. repeated modifiers look like metadata, not separate line names

The family does not currently show a strong internal split that would justify multiple round-1 canonical rows.

## Candidate Entity Expansion

## Candidate 1: `Leica Super-Elmar-M 21mm f/3.4 ASPH`

### Official / literature basis

Strong.

Leica literature and Leica Wiki both treat this as a distinct modern Leica M product line.

### Mechanical distinction

Strong enough for `core`.

It has:

- explicit `Super-Elmar-M` naming
- explicit `ASPH`
- stable `E46` filter format
- stable M-mount modern barrel / hood configuration

### Optical distinction

Strong enough for `core`.

This is not a variant of `Elmarit 21`. It is a distinct Leica M optical line with separate product identity and specification.

### Market split potential

Good.

The local priced subset forms a coherent cluster around roughly `2.98M KRW`.

### Search-intent split potential

Strong.

Dealers and users explicitly write:

- `Super-Elmar 21`
- `Super-Elmar-M 21`
- `21/3.4 Super Elmar ASPH`

### Final decision

`core`

### One-line reason

`Super-Elmar-M 21mm f/3.4 ASPH` is a distinct, clean modern Leica M line with stable title language and no strong round-1 internal split signal.

## Candidate 2: `6bit`

### Official / literature basis

Real feature, but not a separate line.

### Mechanical distinction

Visible but not enough for standalone canonical status.

### Optical distinction

None.

### Market split potential

Weak as a separate row.

The local pool shows `6bit` frequently, but it appears as expected metadata on the same main line, not as a separate market entity.

### Search-intent split potential

Moderate as metadata, weak as canonical entity.

### Final decision

`overlay`

### One-line reason

`6bit` appears often, but it behaves like expected metadata on the main `Super-Elmar-M 21` line rather than a distinct seed row.

## Candidate 3: finish / country / special-edition / packaging variations

### Official / literature basis

Weak to mixed.

### Mechanical distinction

Weak.

### Optical distinction

None.

### Market split potential

Too thin in current local data.

### Search-intent split potential

Weak.

### Final decision

`overlay` or `보류`

### One-line reason

These signals are either absent or too thin locally to justify canonical rows.

## Candidate 4: `Elmarit 21`, `Super-Angulon 21`, `Tri-Elmar 21` boundary

### Official / literature basis

Strongly separate.

These are distinct Leica naming families, not internal `Super-Elmar 21` variants.

### Final decision

`보류` inside this family, meaning out-of-family contamination to exclude

### One-line reason

Boundary families must remain excluded or the `Super-Elmar 21` taxonomy will widen incorrectly.

## Round-1 Recommendation

Recommended immediate `core` candidate count: `1`

Recommended first-pass seed row:

1. `Leica Super-Elmar-M 21mm f/3.4 ASPH`

## What Should Stay Below Seed Level For Now

- `6bit`
- black / silver finish
- country marking
- special / anniversary / titanium language
- completeness / boxed wording

## Can The Next Round Move To Seed Addition?

`Yes`

The safest next round would be a narrow seed addition with only:

- `Leica Super-Elmar-M 21mm f/3.4 ASPH`

and no internal hold rows yet.
