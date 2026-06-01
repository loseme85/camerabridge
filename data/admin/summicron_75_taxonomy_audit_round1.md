# Summicron 75 Taxonomy Audit - Round 1

Date: 2026-04-30

Scope: read-heavy taxonomy audit for the Leica `Summicron 75` family. This round does not add seed rows, does not change classifier/query/search behavior, and does not change admin lookup ranking or UI. The goal is to determine whether `Summicron 75` is mature enough for explicit canonical seeding and, if so, at what granularity.

## Executive Summary

`Summicron 75` is seedable, but the practical round-1 conclusion is narrower than the family name suggests.

The strongest immediate structure is:

1. `Leica APO-Summicron-M 75mm f/2 ASPH`

There is no convincing evidence in the current local market that we should open a broader non-APO `Summicron 75` row or multiple internal round-1 subrows.

Round-1 conclusion:

- immediate recommended `core` candidate count: `1`
- recommended first-pass core:
  - `Leica APO-Summicron-M 75mm f/2 ASPH`
- `6bit` is visible but still behaves like metadata, not like a separate canonical entity
- `black / silver / country marking / special edition / anniversary / titanium` remain below round-1 row level
- `SL APO-Summicron 75` must be kept out of the family

## Family Overview

At first glance, `Summicron 75` looks like a broad Leica focal-length family. In practice, the useful Leica M-side local pool is overwhelmingly one line:

- `APO-Summicron-M 75mm f/2 ASPH`

The main contamination to exclude is:

- `APO-Summicron-SL 75`
- unrelated non-Leica 75mm lenses
- serial-number false hits from other Summicron focal lengths

So the first taxonomic question is not internal styling.  
It is whether `Summicron 75` is really one Leica M product line in current use.

Current evidence says: `yes`.

## Literature / Reference Base

### Source A: Leica Wiki - `75mm f/2 ASPH Apo-Summicron-M`

Leica Wiki documents:

- Leica order no. `11637`
- production era `2005-current`
- Leica M quick-change bayonet
- `7 / 5`
- aspherical and APO construction
- filter size `E49`
- built-in telescopic hood
- inscription `APO-SUMMICRON-M 1:2/75 ASPH.`

Reference:

- https://wiki.l-camera-forum.com/leica-wiki.en/index.php/75mm_f/2_ASPH_Apo-Summicron-M

### Source B: Leica official technical data

Leica’s current technical data also presents this as a stable single line:

- `APO-Summicron-M 75 f/2 ASPH.`
- Leica M bayonet with 6-bit encoding
- built-in extendable hood
- black anodized finish in current catalog presentation

Reference:

- https://leica-camera.com/en-int/photography/lenses/m/apo-summicron-m-75mm-f2-asph-black/technical-specification

### Interpretation

The literature strongly supports one modern Leica M line:

- `APO-Summicron-M 75mm f/2 ASPH`

It does **not** suggest an obvious multi-generation internal split of the kind we saw in several older Leica families.

## Local Listing Evidence

Analysis base: `data/derived/results_resolved_v2.json`

Initial raw title filtering for `75` + `summicron` is noisy because it pulls in:

- `APO-Summicron-SL 75`
- raw serial-number titles

After separating the M line from the SL line, the local structure looks like this:

| Bucket | Count | KRW-priced | Median KRW | Audit note |
| --- | ---: | ---: | ---: | --- |
| `APO-Summicron-M 75` | 36 | 21 | ~`4.18M KRW` | dominant usable M-family line |
| `APO-Summicron-SL 75` | 5 | 3 | ~`4.98M KRW` | contamination, not part of this family |
| residual M-like `other` | 3 | 3 | ~`3.60M KRW` | same line, noisier title formatting |

### Local title patterns

Representative M-line titles:

- `[중고] M 75/2 APO Summicron ASPH 6bit (Black)`
- `LEICA 75mm F2 ASPH (6bit) APO-SUMMICRON-M sn.4129`
- `LEICA 75mm F2 ASPH APO-SUMMICRON-M sn.3986`

Representative SL contamination:

- `[중고] SL APO 75/2 Summicron ASPH (Black)`
- `LEICA 75mm F2 ASPH APO-SUMMICRON-SL sn.4709`

### Internal marker counts in the M-line

Observed repeated markers in the M-only subset:

| Marker | Count | Note |
| --- | ---: | --- |
| `6bit` | 31 | very common, but likely standard coding metadata rather than a distinct market entity |
| `black` | 19 | finish-level |
| `silver` | 0 | not meaningful here |
| `germany` | 0 | no meaningful split |
| `canada` | 0 | no meaningful split |
| `titanium` | 0 | no local support |
| `anniversary / limited / special` | 0 | no local support |

### Interpretation

This family is cleaner than many older Leica lines:

1. there is one overwhelming M-family line
2. `SL` contamination is real but easy to exclude
3. `6bit` is common, but it does not create a second local price cluster or a separate named user intent

So the strongest round-1 move is not to split. It is to recognize that the practical canonical family is:

- `Leica APO-Summicron-M 75mm f/2 ASPH`

## Candidate Entity Expansion

## Candidate 1: `Leica APO-Summicron-M 75mm f/2 ASPH`

### Official / literature basis

Very strong.

The official and Leica Wiki sources both treat this as a stable modern Leica M line with consistent naming.

### Mechanical distinction

Strong enough for `core`.

The line has a coherent product identity:

- Leica M mount
- APO / ASPH design
- built-in telescopic hood
- 6-bit coding as standard-era metadata

### Optical distinction

Strong enough for `core`.

This is not a cosmetic subvariant of another 75mm Leica line. It is the defining Leica M `Summicron 75` line in the current local market.

### Market split potential

Strong.

The local M-only pool is large enough and price-coherent enough for a first-pass price-table anchor.

### Search-intent split potential

Strong.

Users and dealers explicitly search/list:

- `M 75/2 APO Summicron ASPH`
- `APO-Summicron-M 75`
- `75mm F2 APO-Summicron-M`

### Final decision

`core`

### One-line reason

`APO-Summicron-M 75mm f/2 ASPH` is a clean, dominant Leica M product line with stable literature identity and strong local title support.

## Candidate 2: `6bit` as separate row

### Official / literature basis

Real as metadata.

### Mechanical distinction

Weak as a canonical entity split.

It signals coding status, not a fundamentally separate Leica 75 product line.

### Market split potential

Weak.

`6bit` appears constantly, but it does not produce a distinct second cluster in current evidence. It mostly behaves like standard-era listing language.

### Search-intent split potential

Moderate but metadata-like.

People may care, but not in a way that justifies a separate round-1 canonical row.

### Final decision

`overlay`

### One-line reason

`6bit` is common enough to track, but too ordinary and too non-separating to become its own row.

## Candidate 3: finish / special edition / titanium / anniversary

### Official / literature basis

These may exist in literature or catalog space, but they do not have usable local support in the current dataset.

### Search-intent split potential

Weak in round 1.

### Final decision

`overlay` or `보류`

### One-line reason

There is not enough local title repetition or market separation to justify any round-1 row split here.

## Candidate 4: broad `Summicron 75` as a non-APO row

### Official / literature basis

Weak for current Leica M context.

The meaningful local and literature-backed line is specifically the APO-Summicron-M 75 ASPH, not a parallel broad non-APO `Summicron 75` family row.

### Final decision

`보류`

### One-line reason

The practical family should be seeded under the actual Leica line name `APO-Summicron-M 75mm f/2 ASPH`, not an artificially broader non-APO row.

## Recommended Round-1 Core Count

**1**

Recommended immediate core candidate:

1. `Leica APO-Summicron-M 75mm f/2 ASPH`

## What Should Still Wait

- a separate `6bit` row
- any finish-only row
- any special-edition / anniversary / titanium row
- any broad non-APO `Summicron 75` row

## Can The Next Round Add Seed?

**Yes.**

The safe next-step seed direction is:

- add `Leica APO-Summicron-M 75mm f/2 ASPH` as a single explicit `core` row

It should **not** add:

- `APO-Summicron-SL 75` inside the same family
- `6bit` as a separate row
- finish or special-edition rows
