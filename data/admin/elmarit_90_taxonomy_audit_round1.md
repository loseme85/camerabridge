# Elmarit 90 Taxonomy Audit - Round 1

Date: 2026-04-29

Scope: read-heavy taxonomy audit for the Leica `Elmarit 90` family. This round does not add seed rows, does not change classifier/query/search behavior, and does not change admin lookup ranking or UI. The goal is to determine whether `Elmarit 90` is mature enough for explicit canonical seeding and, if so, at what granularity.

## Executive Summary

`Elmarit 90` is seedable, but only if we draw a hard line between:

- `Elmarit-M 90mm f/2.8`
- `Tele-Elmarit 90`

The most important round-1 conclusion is structural:

- `Tele-Elmarit 90` should **not** be treated as an internal split inside `Elmarit 90`
- it should be treated as a separate family for canonical purposes

That leaves one strong immediate `core` candidate inside the true `Elmarit 90` family:

1. `Leica Elmarit-M 90mm f/2.8`

Round-1 conclusion:

- immediate recommended `core` candidate count for `Elmarit 90` proper: `1`
- recommended first-pass core:
  - `Leica Elmarit-M 90mm f/2.8`
- `Tele-Elmarit 90` should move to its own future family audit
- `black / silver / titanium / 6bit` stay below round-1 core level
- older ambiguous unlabeled `90mm f/2.8 ELMARIT` titles are real but not strong enough to open a second Elmarit core right now

## Family Overview

The `90mm` Leica field is highly contaminated. Title-level confusion can come from:

- `Elmar 90`
- `Elmar-C 90`
- `Macro-Elmar-M 90`
- `Summicron 90`
- `Tele-Elmarit 90`
- `Elmarit-R 90`
- `Vario-Elmarit` and `APO-Vario-Elmarit` zooms

So the first taxonomic question is not internal styling. It is family boundary:

1. which `90/2.8` items really belong inside `Elmarit 90`?
2. which ones are actually `Tele-Elmarit` and should be split out?

The local and literature evidence both suggest that `Tele-Elmarit 90` is its own family, not merely a trim level of `Elmarit 90`.

## Literature / Reference Base

### Source A: Leica Wiki - `90mm f/2.8 Elmarit-M`

Leica Wiki documents the later `Elmarit-M 90` line as:

- production era `1990-2007`
- M-bayonet
- `4 / 4`
- black, chrome, and titanium variants
- filter size `E46`
- inscription `LEICA ELMARIT-M 1:2.8/90 E46`

This is the clearest literature basis for the true modern `Elmarit-M 90` family.

References:

- https://wiki.l-camera-forum.com/leica-wiki.en/index.php/90mm_f/2.8_Elmarit-M
- https://wiki.l-camera-forum.com/leica-wiki.en/index.php/90mm_f/2.8_Elmarit-M_III

### Source B: Leica Wiki - `90mm f/2.8 Tele-Elmarit`

Leica Wiki documents the earlier "fat" `Tele-Elmarit 90` as:

- production era `1964-1974`
- `5 / 3`
- separate naming (`TELE-ELMARIT`)
- black / silver variants
- E39 / A42 filter arrangement

Reference:

- https://wiki.l-camera-forum.com/leica-wiki.en/index.php/90mm_f/2.8_Tele-Elmarit

### Source C: Leica Wiki - `90mm f/2.8 Tele-Elmarit-M`

Leica Wiki documents the later "thin" `Tele-Elmarit-M 90` as:

- production era `1974-1990`
- `4 / 4`
- M-bayonet
- explicit `TELE-ELMARIT-M` inscription
- Canadian / German variants
- coding / uncoded variants noted

Reference:

- https://wiki.l-camera-forum.com/leica-wiki.en/index.php/90mm_f/2.8_Tele-Elmarit-M
- https://wiki.l-camera-forum.com/leica-wiki.en/index.php/90mm_f/2.8_Tele-Elmarit_II

## First Structural Judgment: Is `Tele-Elmarit 90` Inside `Elmarit 90`?

`No`

Why:

1. Leica Wiki gives `Tele-Elmarit` and `Elmarit-M` separate pages
2. the title inscriptions are explicitly different:
   - `ELMARIT-M`
   - `TELE-ELMARIT`
   - `TELE-ELMARIT-M`
3. local titles also separate them directly
4. the user/search intent is already distinct in dealer language

So for canonical purposes:

- `Elmarit 90` proper should focus on `Elmarit-M 90`
- `Tele-Elmarit 90` should be audited as a separate future family

## Local Listing Evidence

Analysis base: `data/derived/results_resolved_v2.json`

After excluding obvious contamination from:

- `R 90/2.8 Elmarit`
- `24-90` / `90-280` / `28-90` vario lenses
- `Macro-Elmar`
- non-90 `Elmarit`

the useful local pool splits approximately into:

- `Elmarit-M 90`: `38` listings
- `Tele-Elmarit 90`: `17` listings

### Price clustering

KRW-only parsed medians:

| Bucket | Count | KRW-priced | Median KRW | Audit note |
| --- | ---: | ---: | ---: | --- |
| `Elmarit-M 90` | 38 | 21 | ~1.18M KRW | stable modern M line |
| `Tele-Elmarit 90` | 17 | 8 | ~1.04M KRW | distinct title language, overlapping but separate family |

### Local title patterns

`Elmarit-M` examples:

- `[중고] M 90/2.8 Elmarit (Black)`
- `[위탁] M 90/2.8 Elmarit (Silver)`
- `LEICA 90mm F2.8 ELMARIT-M sn.3824`
- `LEICA 90mm F2.8 (6bit) ELMARIT-M sn.3973`

`Tele-Elmarit` examples:

- `[중고] M 90/2.8 Tele Elmarit (Black)`
- `LEICA 90mm F2.8 TELE-ELMARIT sn.2490`
- `LEICA 90mm F2.8 TELE-ELMARIT-M sn.1180`
- `LEICA 90mm F2.8 (1st) TELE-ELMARIT sn.2001`

### Interpretation

Two important things are true at once:

1. the price bands overlap more than classic `Summicron 90` versus `APO 90`
2. the title language separates the families clearly

That means the right first-pass move is **not** to merge them into one `Elmarit 90` family and then split internally.  
It is to treat `Tele-Elmarit 90` as out-of-family for this audit.

## Candidate Entity Expansion

## Candidate 1: `Leica Elmarit-M 90mm f/2.8`

### Official / literature basis

Strong.

This is a clearly documented Leica M product line from the 1990-2007 era with stable naming and a dedicated literature identity.

### Mechanical distinction

Strong enough for `core`.

It has:

- explicit `Elmarit-M` naming
- M-bayonet identity
- `E46` filter size
- stable modern barrel form

### Optical distinction

Strong enough for `core`.

The literature treats this as its own `4 / 4` line, distinct from earlier `Tele-Elmarit` variants.

### Market split potential

Good.

The local median around `1.18M KRW` forms a usable market cluster.

### Search-intent split potential

Strong.

Users and dealers explicitly search / list:

- `M 90/2.8 Elmarit`
- `90mm f2.8 Elmarit-M`

### Final decision

`core`

### One-line reason

`Elmarit-M 90mm f/2.8` is a clearly named Leica M line with strong literature support and enough local title stability to be a first-pass core entity.

## Candidate 2: `Tele-Elmarit 90` as an internal split inside Elmarit 90

### Official / literature basis

Strong, but in the wrong direction.

The literature strongly supports `Tele-Elmarit 90` as real, but it supports it as a **separate family**, not as an internal cosmetic split inside `Elmarit 90`.

### Mechanical distinction

Strong.

There are meaningful fat/thin, filter-size, and inscription differences.

### Optical distinction

Strong enough to matter.

The fat `Tele-Elmarit` and later `Tele-Elmarit-M` are not just finish changes of `Elmarit-M 90`.

### Market split potential

Real.

Even if the price overlap is not dramatic, the collector and user vocabulary is already separate.

### Search-intent split potential

Strong.

Dealers directly say `Tele Elmarit`, `Tele-Elmarit-M`, and even `1st Tele-Elmarit`.

### Final decision

`separate family, not an internal Elmarit 90 split`

### One-line reason

`Tele-Elmarit 90` should be audited and seeded separately rather than folded into the `Elmarit 90` family.

## Candidate 3: unlabeled early `90mm f/2.8 ELMARIT`

### Official / literature basis

Moderate.

Some raw titles appear as just:

- `LEICA 90mm F2.8 ELMARIT sn.1709`

without `-M` or `Tele-` wording.

### Mechanical distinction

Potentially meaningful, but ambiguous.

These may represent older line naming, incomplete dealer wording, or noisy carry-over from nearby families.

### Optical distinction

Unclear in current local evidence.

### Market split potential

Possible, but unproven.

### Search-intent split potential

Weak-to-moderate.

Because the titles do not expose a stable subtype name, they are not seed-ready as a separate line.

### Final decision

`hold`

### One-line reason

The unlabeled early `90/2.8 Elmarit` signal is real enough to note, but too ambiguous for a round-1 core split.

## Candidate 4: `Elmarit-M 90` internal black / silver / titanium / 6bit variants

### Official / literature basis

Real.

Leica Wiki lists:

- black
- chrome
- titanium

and local titles expose:

- black
- silver
- one `6bit`

### Mechanical distinction

Weak-to-moderate.

These are real variants but not separate optical product lines.

### Optical distinction

None or near-none at the family level.

### Market split potential

Possible for titanium or chrome, but current local evidence is too thin.

### Search-intent split potential

Moderate for finish, weak for more specific splitting.

### Final decision

`overlay` / `hold`

### One-line reason

Internal `Elmarit-M 90` variants exist, but they are not strong enough to split out of the main row in round 1.

## Recommended Round-1 Taxonomy

### Recommended immediate `core`

1. `Leica Elmarit-M 90mm f/2.8`

### Recommended `hold`

- unlabeled early `90mm f/2.8 Elmarit` ambiguity
- possible future `Elmarit-M 90` internal titanium / coded review

### Recommended `overlay`

- `black`
- `silver`
- `country marking`
- `6bit`
- `boxed / completeness`

### Recommended `보류`

- fat/thin internal splitting **inside** `Tele-Elmarit`
- collector-level filter-thread or hood subtyping

## Seed-Readiness Verdict

### Can this family move to explicit seed next round?

`Yes, but narrowly`

### Recommended first seed shape

One conservative `core` row only:

1. `Leica Elmarit-M 90mm f/2.8`

### What should not be done next round

- do not fold `Tele-Elmarit 90` into the same family file
- do not create a broad mixed `Elmarit 90 / Tele-Elmarit 90` row
- do not split black/silver/titanium/6bit in round 1

## Final Recommendation

`Elmarit 90` is seedable, but only once we define the family boundary strictly:

- `Elmarit-M 90` = this family's first `core`
- `Tele-Elmarit 90` = separate future family audit

That keeps the taxonomy both historically honest and operationally usable.
