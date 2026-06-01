# Elmar-M 24 Taxonomy Audit - Round 1

Date: 2026-05-08

Scope: read-heavy taxonomy audit for the Leica `Elmar-M 24mm f/3.8 ASPH` line. This round does not add seed rows, does not change classifier/query/search behavior, and does not change admin lookup ranking or UI. The goal is to determine whether this line is mature enough for explicit canonical seeding and, if so, at what granularity.

## Executive Summary

The `Super-Elmar 24` label should stay closed, and the correct reframing is:

1. `Leica Elmar-M 24mm f/3.8 ASPH`

as the actual Leica M-side line under review.

Round-1 conclusion:

- immediate recommended `core` candidate count: `1`
- recommended first-pass core:
  - `Leica Elmar-M 24mm f/3.8 ASPH`
- this behaves like a narrow modern single-line Leica M family
- `6bit`, finish, hood / bundle, country marking, and packaging remain `overlay` or `보류`
- `Elmarit 24`, `Summilux 24`, `Summicron 24`, `Tri-Elmar`, `Elmarit-R 24`, and `SL / Vario-Elmarit` contamination remain outside the family

Why this is the right reframing:

- literature names the line `Elmar-M 24mm f/3.8 ASPH`
- local titles also converge on `ELMAR-M 24mm F3.8`
- the previous `Super-Elmar 24` label was not supported by either literature or local title language

## Why The Reframing Matters

The prior `Super-Elmar 24` audit established an important correction:

- `Super-Elmar 24` is not the correct canonical family label
- the real Leica M-side 24mm compact modern line is `Elmar-M 24mm f/3.8 ASPH`

So this round does not continue the old family. It replaces it with the correct line identity.

That naming correction matters because canonical seeding should follow:

1. the actual Leica line name
2. the language dealers actually use
3. the boundary between nearby families

## Family / Line Overview

The neighboring `24mm` Leica field includes several close but distinct families:

- `Elmarit-M 24mm f/2.8 ASPH`
- `Elmar-M 24mm f/3.8 ASPH`
- `Summilux-M 24mm`
- `Summicron-M 24mm`
- `Tri-Elmar`
- `Elmarit-R 24mm`
- `SL` / `Vario-Elmarit` zoom contamination

The first question is whether `Elmar-M 24mm f/3.8 ASPH` should be treated as:

1. a single exact Leica line, or
2. a family with meaningful internal splits already visible in current local data.

Round-1 answer: `1`.

This line behaves like a compact modern single-line Leica M product.

## Literature / Reference Base

### Source A: Leica Wiki - `24mm f/3.8 ASPH Elmar-M`

Leica Wiki documents the line as:

- `24mm f/3.8 ASPH Elmar-M`

with:

- production era `2008-current`
- Leica M bayonet with `6-bit` coding
- `8 / 6` optical design
- `E46` filter thread
- inscription:
  - `LEICA ELMAR-M 1:3.8/24 ASPH. E46`

Reference:

- [Leica Wiki - 24mm f/3.8 ASPH Elmar-M](https://wiki.l-camera-forum.com/leica-wiki.en/index.php/24mm_f/3.8_ASPH_Elmar-M)

### Source B: Leica Camera product pages

Leica's own product pages use the same line name:

- `Elmar-M 24mm f/3.8 ASPH`

References:

- [Leica Camera UK - Elmar-M 24mm f/3.8 ASPH overview](https://leica-camera.com/en-GB/photography/lenses/m/elmar-m-24mm-f3-8-asph-black/overview)
- [Leica Camera KR - Elmar-M 24mm f/3.8 ASPH overview](https://leica-camera.com/ko-KR/photography/lenses/m/elmar-m-24mm-f3-8-asph-black/overview)

### Source C: market references

Secondary market references also preserve the same naming:

- `Leica Elmar-M 24mm f/3.8 ASPH`

Reference:

- [B&H - Leica Elmar-M 24mm f/3.8 ASPH overview](https://www.bhphotovideo.com/c/product/586192-REG/Leica_11648_Wide_Angle_24mm_f_3_8.html/overview)

### Interpretation

The literature and market-reference stack is unusually consistent here:

- no competing `Super-Elmar 24` naming
- no documented internal optical split
- one stable Leica M line name

## Local Listing Evidence

Analysis base: `data/derived/results_resolved_v2.json`

After excluding obvious contamination from:

- `Elmarit`
- `Summilux`
- `Summicron`
- `Super-Angulon`
- `Tri-Elmar`
- `Vario-Elmarit-SL`
- `SL` zooms
- `R 24`

the useful local pool becomes:

- clean local pool: `4`

Representative local titles:

- `LEICA 24mm F3.8 ELMAR-M sn.4141`
- `LEICA 24mm F3.8 ASPH ELMAR-M sn.4087`
- `LEICA 24mm F3.8 ELMAR-M sn.4087`
- `LEICA 24mm F3.8 ELMAR-M sn.4081`

Price signal:

- priced subset: `1`
- observed KRW price: `2.50M KRW`

Marker frequency in the clean local pool:

- `ASPH`: `1`
- `6bit`: `0`
- `black`: `0`
- `silver`: `0`
- `hood`: `0`

### Interpretation

The pool is small, but it is also very clean:

1. every relevant title points to the same `Elmar-M 24mm f/3.8` line
2. no local evidence suggests a competing internal subtype
3. no local evidence suggests a real alternative family label

This is thinner than `Super-Elmar 21`, but cleaner in naming convergence than many older Leica families.

## Candidate Entity Expansion

## Candidate 1: `Leica Elmar-M 24mm f/3.8 ASPH`

### Official / literature basis

Strong.

This is the exact line name used in Leica literature and supporting market references.

### Mechanical distinction

Strong enough for `core`.

It has:

- explicit `Elmar-M` naming
- explicit `ASPH`
- stable `E46` filter / hood interface
- stable compact M-mount modern barrel identity

### Optical distinction

Strong enough for `core`.

This is not a variation of `Elmarit 24`. It is its own Leica M optical line.

### Market split potential

Moderate.

The local priced subset is thin, but the exact-title convergence is high and there is no competing internal bucket in the current pool.

### Search-intent split potential

Strong.

Users and dealers explicitly write:

- `ELMAR-M 24mm F3.8`
- `24mm F3.8 ASPH ELMAR-M`

### Final decision

`core`

### One-line reason

`Leica Elmar-M 24mm f/3.8 ASPH` is a literature-stable, locally visible, single-line Leica M family that can be seeded narrowly as one `core` row.

## Candidate 2: `6bit`

### Official / literature basis

Real feature, but not a separate line.

### Mechanical distinction

Visible in literature, but not enough for standalone canonical status.

### Optical distinction

None.

### Market split potential

Too weak in the current local pool.

### Search-intent split potential

Metadata only.

### Final decision

`overlay`

### One-line reason

`6bit` belongs in metadata if needed, not as a separate canonical row.

## Candidate 3: finish / hood bundle / country / packaging

### Official / literature basis

Weak to mixed.

### Mechanical distinction

Weak as taxonomy.

### Optical distinction

None.

### Market split potential

Too weak in the current local pool.

### Search-intent split potential

Metadata only.

### Final decision

`overlay` or `보류`

### One-line reason

These are secondary descriptors on a line that currently shows no meaningful internal family split.

## Candidate 4: boundary families

### Included boundary cases

- `Elmarit 24`
- `Summilux 24`
- `Summicron 24`
- `Tri-Elmar`
- `Elmarit-R 24`
- `SL` / `Vario-Elmarit` 24mm zooms

### Official / literature basis

Strongly separate.

### Final decision

`out-of-family boundary`

### One-line reason

These are different Leica lines or different systems and must stay excluded for the `Elmar-M 24` taxonomy to remain clean.

## Round-1 Recommendation

### Recommended immediate `core` count

`1`

### Recommended first-pass core

1. `Leica Elmar-M 24mm f/3.8 ASPH`

### Not recommended yet

- any secondary `6bit` row
- finish row
- hood / bundle row
- country row

## Can The Next Round Move To Seed Addition?

`Yes`, but only narrowly.

The safest next round is:

1. add `Leica Elmar-M 24mm f/3.8 ASPH` as the only immediate `core` row

Do **not** add:

- `6bit`
- finish / country / packaging rows
- any attempt to revive `Super-Elmar 24`

## Final Judgment

The correct round-1 posture is:

- close `Super-Elmar 24` as a bad family label
- recognize `Leica Elmar-M 24mm f/3.8 ASPH` as the real Leica M-side line
- treat it as a narrow single-line `core` candidate

This is a naming-correction audit that successfully resolves into a valid future seed target.
