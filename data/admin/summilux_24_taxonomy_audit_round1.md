# Summilux 24 Taxonomy Audit - Round 1

Date: 2026-05-08

Scope: read-heavy taxonomy audit for the Leica `Summilux 24` family. This round does not add seed rows, does not change classifier/query/search behavior, and does not change admin lookup ranking or UI. The goal is to determine whether `Summilux 24` is mature enough for explicit canonical seeding and, if so, at what granularity.

## Executive Summary

`Summilux 24` is seedable, and round-1 should keep it as a broad single-line modern Leica M family.

The strongest first-pass recommendation is:

1. `Leica Summilux-M 24mm f/1.4 ASPH`

Round-1 conclusion:

- immediate recommended `core` candidate count: `1`
- recommended first-pass core:
  - `Leica Summilux-M 24mm f/1.4 ASPH`
- `6bit` stays `overlay`
- `black / silver / country marking / special edition / anniversary / titanium / boxed completeness` stay `overlay` or `보류`
- `Elmarit 24`, `Elmar-M 24`, `Summicron 24`, `Tri-Elmar`, `Elmarit-R 24`, and `SL` / non-Leica contamination remain out-of-family boundary cases

Why this is a single-line family:

- literature documents one stable Leica M product line
- local title language converges on one exact line name
- no internal market split is visible in the current local pool

## Family Overview

The neighboring `24mm` Leica field contains multiple close but distinct families:

- `Elmarit-M 24mm f/2.8 ASPH`
- `Elmar-M 24mm f/3.8 ASPH`
- `Summilux-M 24mm f/1.4 ASPH`
- `Summicron-M 24mm`
- `Tri-Elmar`
- `Elmarit-R 24mm`
- `SL` / `Vario-Elmarit` contamination

For canonical purposes, `Summilux 24` needs to stay narrow.

Once boundary families are excluded, the local pool becomes small but extremely clean.

The first round-1 taxonomic question is whether there are major internal splits worth seeding now.

Round-1 answer: `no`.

This family behaves like a modern single-line Leica M product.

## Literature / Reference Base

### Source A: Leica Wiki - `24mm f/1.4 ASPH Summilux-M`

Leica Wiki documents the lens as a distinct Leica M line with:

- production era `2008-current`
- Leica M bayonet with `6 bit` lens identification
- `10 / 8` optical design
- `f/1.4` maximum aperture
- separate screw-on hood with Series VII filter support

Reference:

- [Leica Wiki - 24mm f/1.4 ASPH Summilux-M](https://wiki.l-camera-forum.com/leica-wiki.en/index.php/24mm_f/1.4_ASPH_Summilux-M)

### Source B: Leica Camera product pages

Leica's own product pages present the same line as:

- `Summilux-M 24 f/1.4 ASPH.`

and describe it as one compact, high-speed Leica M wide-angle line.

References:

- [Leica Camera AT - Summilux-M 24 f/1.4 ASPH.](https://leica-camera.com/en-AT/photography/lenses/m/summilux-m-24mm-f1-4-asph-black)
- [Leica Camera KR - Summilux-M 24 f/1.4 ASPH.](https://leica-camera.com/ko-KR/photography/lenses/m/summilux-m-24mm-f1-4-asph-black)

### Interpretation

The literature stack is very consistent:

- one exact Leica line name
- one optical design family
- no documented internal version tree that rises to round-1 seed level

## Local Listing Evidence

Analysis base: `data/derived/results_resolved_v2.json`

After excluding obvious contamination from:

- `Elmarit`
- `Elmar-M`
- `Summicron`
- `Tri-Elmar`
- `SL` / `Vario` zooms
- `R 24`
- non-24 `Summilux` titles pulled in by serial numbers

the useful local `Summilux 24` pool is:

- clean local pool: `8`

### Price clustering

KRW-parsed local medians:

| Bucket | Count | KRW-priced | Median KRW | Audit note |
| --- | ---: | ---: | ---: | --- |
| `Summilux-M 24mm f/1.4 ASPH` | 8 | 6 | ~5.58M KRW | stable single-line cluster |

Observed price range in KRW-priced subset:

- min: `4.90M KRW`
- max: `5.88M KRW`

### Local title patterns

Representative local titles:

- `[중고] M 24/1.4 Summilux ASPH 6bit (Black)`
- `LEICA 24mm F1.4 ASPH SUMMILUX-M sn.4651`
- `LEICA 24mm F1.4 ASPH SUMMILUX-M sn.4079`
- `LEICA 24mm F1.4 ASPH SUMMILUX-M sn.4158`

### Local marker frequency

Repeated local modifiers:

- `ASPH`: `8`
- `6bit`: `4`
- `black`: `4`

Not meaningfully present in the clean local pool:

- `silver`
- `germany`
- `canada`
- `anniversary`
- `titanium`

### Interpretation

This family clears the round-1 threshold on two independent axes:

1. title language converges on one exact line
2. priced examples form one coherent local cluster

Repeated modifiers look like metadata, not separate product lines.

## Candidate Entity Expansion

## Candidate 1: `Leica Summilux-M 24mm f/1.4 ASPH`

### Official / literature basis

Strong.

Leica literature and Leica Wiki both treat this as a distinct Leica M product line.

### Mechanical distinction

Strong enough for `core`.

It has:

- explicit `Summilux-M` naming
- explicit `ASPH`
- stable modern M-mount barrel / hood arrangement
- stable `f/1.4` high-speed wide-angle identity

### Optical distinction

Strong enough for `core`.

This is not a variation of `Elmarit 24` or `Elmar-M 24`. It is its own Leica M optical line.

### Market split potential

Good.

The local priced subset forms a coherent cluster around roughly `5.58M KRW`.

### Search-intent split potential

Strong.

Dealers and users explicitly write:

- `M 24/1.4 Summilux ASPH`
- `24mm F1.4 ASPH SUMMILUX-M`

### Final decision

`core`

### One-line reason

`Summilux-M 24mm f/1.4 ASPH` is a distinct, clean modern Leica M line with stable title language and no visible round-1 internal split.

## Candidate 2: `6bit`

### Official / literature basis

Real feature, but not a separate line.

### Mechanical distinction

Visible but not enough for standalone canonical status.

### Optical distinction

None.

### Market split potential

Weak as a separate row.

The local pool shows `6bit` repeatedly, but always on the same main line.

### Search-intent split potential

Moderate as metadata, weak as canonical entity.

### Final decision

`overlay`

### One-line reason

`6bit` behaves like expected metadata on the main `Summilux-M 24` line rather than a separate seed row.

## Candidate 3: finish / country / special-edition / packaging variations

### Official / literature basis

Weak to mixed.

### Mechanical distinction

Weak.

### Optical distinction

None.

### Market split potential

Too thin in the current local data.

### Search-intent split potential

Usable as metadata only.

### Final decision

`overlay` or `보류`

### One-line reason

`black`, `silver`, `country marking`, packaging, and special-edition language do not rise to separate canonical-row level in the current pool.

## Candidate 4: boundary families

### Included boundary cases

- `Elmarit 24`
- `Elmar-M 24`
- `Summicron 24`
- `Tri-Elmar`
- `Elmarit-R 24`
- `SL` / `Vario-Elmarit` 24mm zooms

### Official / literature basis

Strongly separate.

### Mechanical / optical distinction

These are different Leica lines or different mount families, not internal `Summilux 24` variants.

### Final decision

`out-of-family boundary`

### One-line reason

Boundary discipline keeps `Summilux 24` from collapsing into a generic `24mm Leica fast lens` bucket.

## Round-1 Recommendation

### Recommended immediate `core` count

`1`

### Recommended first-pass core

1. `Leica Summilux-M 24mm f/1.4 ASPH`

### Not recommended yet

- any `6bit` row
- finish row
- country row
- packaging row

## What Should Stay Deferred

The following should remain below round-1 seed level:

- `6bit`
- black / silver finish
- country marking
- packaging / completeness language

These are not useless signals. They are just not strong enough to justify separate canonical rows right now.

## Can The Next Round Move To Seed Addition?

`Yes`, but only narrowly.

The safest next round is:

1. add `Leica Summilux-M 24mm f/1.4 ASPH` as the only immediate `core` row

Do **not** add:

- a `6bit` row
- a finish row
- country / packaging rows

## Final Judgment

`Summilux 24` is seedable, and round-1 should treat it as a clean single-line Leica M family.

The correct first-pass posture is:

- open `Leica Summilux-M 24mm f/1.4 ASPH` as `core`
- keep `6bit` and finish-style descriptors below canonical row level
- keep adjacent `24mm` Leica families strictly outside the taxonomy
