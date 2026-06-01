# Super-Elmar 24 Taxonomy Audit - Round 1

Date: 2026-05-07

Scope: read-heavy taxonomy audit for the Leica `Super-Elmar 24` family. This round does not add seed rows, does not change classifier/query/search behavior, and does not change admin lookup ranking or UI. The goal is to determine whether `Super-Elmar 24` is mature enough for explicit canonical seeding and, if so, at what granularity.

## Executive Summary

`Super-Elmar 24` should **not** move to seed addition as a family label.

The strongest round-1 conclusion is:

- immediate recommended `core` candidate count: `0`
- `Super-Elmar 24` is **not** supported as a real Leica M product-line name in the current literature and local-title evidence
- the actual modern Leica M-side `24mm` line visible in both literature and local titles is:
  - `Leica Elmar-M 24mm f/3.8 ASPH`
- therefore this round should end in `보류`, with a recommendation to audit `Elmar-M 24mm f/3.8 ASPH` as its own future family or named line, rather than force it under `Super-Elmar 24`

This is not a case where the family is merely sparse. It is a naming-boundary issue:

- `Super-Elmar 21` is a real Leica M line
- `Elmar-M 24mm f/3.8 ASPH` is a real Leica M line
- but `Super-Elmar 24` is not the operational or literature-backed name for the 24mm line

## Family Overview

The neighboring `24mm` Leica field contains several distinct naming families:

- `Elmarit-M 24mm f/2.8 ASPH`
- `Elmar-M 24mm f/3.8 ASPH`
- `Summilux-M 24mm`
- `Summicron-M 24mm`
- `Tri-Elmar`
- `Elmarit-R 24mm`
- `SL` / `Vario-Elmarit` 24mm zoom contamination

The first round-1 taxonomic question is not whether `24mm` Leica wide-angle products exist. They do.

The real question is whether `Super-Elmar 24` is the right family label for any stable Leica M-side line.

Round-1 answer: `no`.

## Literature / Reference Base

### Source A: Leica Wiki - `24mm f/3.8 ASPH Elmar-M`

Leica Wiki documents the relevant modern M-side line as:

- `24mm f/3.8 ASPH Elmar-M`

with:

- production era `2008-current`
- Leica M bayonet with `6-bit` coding
- `8 / 6` optical design
- `E46` filter / hood interface
- inscription:
  - `LEICA ELMAR-M 1:3.8/24 ASPH. E46`

Reference:

- [Leica Wiki - 24mm f/3.8 ASPH Elmar-M](https://wiki.l-camera-forum.com/leica-wiki.en/index.php/24mm_f/3.8_ASPH_Elmar-M)

### Source B: Leica Camera product pages

Leica's own product pages likewise present the modern 24mm compact M line as:

- `Elmar-M 24mm f/3.8 ASPH`

not as `Super-Elmar 24`.

References:

- [Leica Camera UK - Elmar-M 24mm f/3.8 ASPH overview](https://leica-camera.com/en-GB/photography/lenses/m/elmar-m-24mm-f3-8-asph-black/overview)
- [Leica Camera KR - Elmar-M 24mm f/3.8 ASPH overview](https://leica-camera.com/ko-KR/photography/lenses/m/elmar-m-24mm-f3-8-asph-black/overview)

### Source C: market references

Used-market and dealer references also describe the line as:

- `Leica Elmar-M 24mm f/3.8 ASPH`

Reference:

- [B&H - Leica Elmar-M 24mm f/3.8 ASPH overview](https://www.bhphotovideo.com/c/product/586192-REG/Leica_11648_Wide_Angle_24mm_f_3_8.html/overview)

### Interpretation

The literature base does **not** support `Super-Elmar 24` as the right canonical family name.

It supports:

- `Elmar-M 24mm f/3.8 ASPH`

as the real Leica M-side line.

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

the relevant local pool is extremely small and, more importantly, converges on `Elmar-M`, not `Super-Elmar 24`.

Useful local titles:

- `LEICA 24mm F3.8 ELMAR-M sn.4141`
- `LEICA 24mm F3.8 ASPH ELMAR-M sn.4087`
- `LEICA 24mm F3.8 ELMAR-M sn.4087`
- `LEICA 24mm F3.8 ELMAR-M sn.4081`

Clean local pool for this naming area:

- `4` relevant `24mm Elmar-M` titles
- priced subset: `1`
- observed KRW price: `2.50M KRW`

By contrast, true `Super-Elmar` local titles in this search slice are:

- `21mm f/3.4 Super-Elmar-M`

not `24mm`.

### Interpretation

The local pool supports two things:

1. a real Leica M-side `24mm f/3.8 Elmar-M ASPH` line
2. no operational `Super-Elmar 24` title language

That means the naming family requested for this audit is not validated by current local evidence.

## Candidate Entity Expansion

## Candidate 1: broad `Super-Elmar 24`

### Official / literature basis

Weak.

The literature base used here does not document a Leica M line named `Super-Elmar 24`.

### Mechanical distinction

Not applicable as a stable named family.

### Optical distinction

The underlying optical line exists, but it is presented as `Elmar-M 24mm f/3.8 ASPH`, not `Super-Elmar 24`.

### Market split potential

Weak under the `Super-Elmar 24` label.

### Search-intent split potential

Weak.

Users and dealers do not appear to ask for or list this lens primarily as `Super-Elmar 24`.

### Final decision

`보류`

### One-line reason

`Super-Elmar 24` is not the correct operational family label for the modern Leica M 24mm line.

## Candidate 2: `Leica Elmar-M 24mm f/3.8 ASPH`

### Official / literature basis

Strong.

This is the real literature-backed Leica M line exposed by the audit.

### Mechanical distinction

Strong enough for a future canonical row, but under a different family framing.

### Optical distinction

Strong.

This is a separate modern Leica M optical line and should not be folded into `Elmarit 24`.

### Market split potential

Plausible, but current local pool is small.

### Search-intent split potential

Moderate to strong, because local titles directly say `ELMAR-M 24mm F3.8 ASPH`.

### Final decision

`future separate audit candidate`

### One-line reason

The right next step is not `Super-Elmar 24` seeding, but a dedicated audit for `Elmar-M 24mm f/3.8 ASPH`.

## Candidate 3: finish / coding / country / packaging / hood bundle

### Official / literature basis

Mixed to weak.

### Mechanical distinction

Weak as canonical taxonomy.

### Optical distinction

None.

### Market split potential

Too weak in the current local pool.

### Search-intent split potential

Metadata only.

### Final decision

`overlay` or `보류`

### One-line reason

These are secondary descriptors on a line that itself should first be re-audited under the correct family name.

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

Allowing these into `Super-Elmar 24` would compound a family label that is already not well-supported.

## Round-1 Recommendation

### Recommended immediate `core` count

`0`

### Recommended first-pass core

None under the `Super-Elmar 24` family label.

## What Should Stay Deferred

The following should remain unresolved in this family audit:

- any attempt to seed `Super-Elmar 24`
- finish / country / coding / hood bundle substructure

## Can The Next Round Move To Seed Addition?

`No`, not for `Super-Elmar 24` as named.

The safer next step is:

1. open a fresh taxonomy audit for `Leica Elmar-M 24mm f/3.8 ASPH`

and decide there whether the line is strong enough for:

- a single immediate `core` row

## Final Judgment

`Super-Elmar 24` should not be promoted to the seed system as a canonical family at this stage.

The audit evidence says the real Leica M-side line is:

- `Leica Elmar-M 24mm f/3.8 ASPH`

So the correct move is to stop here, keep `Super-Elmar 24` unseeded, and reframe the next round around the proper family name.
