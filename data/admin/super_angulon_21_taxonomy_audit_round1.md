# Super-Angulon 21 Taxonomy Audit - Round 1

Date: 2026-05-01

Scope: read-heavy taxonomy audit for the Leica `Super-Angulon 21` family. This round does not add seed rows, does not change classifier/query/search behavior, and does not change admin lookup ranking or UI. The goal is to determine whether `Super-Angulon 21` is mature enough for explicit canonical seeding and, if so, at what granularity.

## Executive Summary

`Super-Angulon 21` is seedable, but only narrowly.

The strongest round-1 conclusion is:

1. `Leica Super-Angulon 21mm f/3.4`

is a valid immediate `core` candidate.

There is also a literature-real earlier `f/4` line, but current local support is too thin for round-1 `core`.

Round-1 conclusion:

- immediate recommended `core` candidate count: `1`
- recommended first-pass core:
  - `Leica Super-Angulon 21mm f/3.4`
- `Leica Super-Angulon 21mm f/4` is a real subtype and a plausible future `hold` candidate
- finder requirement / finder bundle stays below round-1 row level
- black / silver finish stays `overlay`
- `Elmarit 21`, `Super-Elmar 21`, and `Tri-Elmar 16-18-21` remain out-of-family boundary cases

## Family Overview

The `21mm` Leica wide-angle field contains several neighboring families that must be kept separate:

- `Super-Angulon 21`
- `Elmarit 21`
- `Super-Elmar 21`
- `Tri-Elmar 16-18-21`
- `R 21` and `PC-Super-Angulon-R`

For canonical purposes, `Super-Angulon 21` is historically older and mechanically narrower than `Elmarit 21` or `Super-Elmar 21`. It is also the family most likely to be distorted by collector shorthand if we split too aggressively too early.

The first round-1 question is whether the family should stay broad single-line or whether the `f/4` versus `f/3.4` split is already operationally visible.

Round-1 answer:

- `f/3.4` is strong enough for immediate `core`
- `f/4` is real but not yet strong enough for immediate `core`

## Literature / Reference Base

### Source A: Leica Wiki - `21mm f3.4 Super-Angulon`

Leica Wiki documents the `21mm f/3.4 Super-Angulon` as:

- production era `1963-1980`
- Schneider-Kreuznach design
- `8 / 4`
- Leica screw-thread and M-bayonet variants
- accessories including hood and external viewfinder
- compatibility caveats on digital M bodies

The same Leica Wiki page also preserves the serial-number note that earlier `1:4` `2.1cm` lenses existed before the `f/3.4` line became the dominant M-side title language.

Reference:

- https://wiki.l-camera-forum.com/leica-wiki.en/index.php/21mm_f3.4_Super-Angulon

### Source B: family boundary references

The neighboring `21mm` Leica families are distinct and should not be folded into `Super-Angulon 21`:

- `21mm f/2.8 Elmarit-M`
- `21mm f/3.4 Super-Elmar-M`
- `Tri-Elmar 16-18-21`

These have separate product names and different optical generations.

## Local Listing Evidence

Analysis base: `data/derived/results_resolved_v2.json`

The raw `Super-Angulon 21` hit set initially contains contamination from:

- `Super-Angulon-R`
- `PC-Super-Angulon-R 28`
- accessory-only `IWKOO / 12502`

After excluding:

- `R` contamination
- `PC-Super-Angulon`
- finder-only accessory records
- `Elmarit`, `Super-Elmar`, `Tri-Elmar` boundary families

the useful local M-side `Super-Angulon 21` pool becomes:

- strict M-side local pool: `10`

### Price clustering

KRW-parsed local medians:

| Bucket | Count | KRW-priced | Median KRW | Audit note |
| --- | ---: | ---: | ---: | --- |
| `Super-Angulon 21mm f/3.4` | 8 | 8 | ~1.60M KRW | stable M-side anchor line |
| `Super-Angulon 21mm f/4` | 2 | 2 | ~2.38M KRW | real but sparse early subtype |

### Local title patterns

`f/3.4` examples:

- `Leica M 21mm f3.4 Super-Angulon Silver`
- `Leica M 21mm f3.4 Super-Angulon Black`
- `[중고] M21/3.4 Super Angulon (Black)`
- `[위탁] M21/3.4 Super Angulon`

`f/4` examples:

- `[중고] M 21/4 Super Angulon (Silver)`
- `[중고] M 21/4 Super Angulon (Silver)`

### Interpretation

This family does show a real internal split, but only one side is mature enough for round-1 seeding.

Why:

1. literature clearly supports `f/4` and `f/3.4` as distinct lines
2. local titles also expose that split directly
3. but local `f/4` support is only `2` listings, versus `8` for `f/3.4`

So the split is not imaginary; it is simply asymmetrically mature.

## Candidate Entity Expansion

## Candidate 1: `Leica Super-Angulon 21mm f/3.4`

### Official / literature basis

Strong.

This is a documented Leica M-side product line with stable title language and substantial historical production.

### Mechanical distinction

Strong enough for `core`.

The family identity is operationally stable:

- explicit `21/3.4`
- persistent external-viewfinder wide-angle workflow
- stable M-side dealer wording

### Optical distinction

Strong enough for `core`.

This is not a cosmetic variant of `Elmarit 21` or `Super-Elmar 21`; it is its own classic optical line.

### Market split potential

Good.

The local `f/3.4` priced subset centers around roughly `1.60M KRW`.

### Search-intent split potential

Strong.

Dealers and users explicitly write:

- `21/3.4 Super Angulon`
- `21mm f3.4 Super-Angulon`

### Final decision

`core`

### One-line reason

`21mm f/3.4 Super-Angulon` is the dominant, clearly titled M-side line in local data and has enough literature and market support to anchor the family.

## Candidate 2: `Leica Super-Angulon 21mm f/4`

### Official / literature basis

Real.

The Leica Wiki serial-history notes confirm an earlier `1:4` `2.1cm` `Super-Angulon` phase before the `f/3.4` line took over.

### Mechanical distinction

Real enough for a future row.

This is not just a finish or accessory difference; it is a real speed/version split.

### Optical distinction

Real.

The `f/4` and `f/3.4` lenses are not the same labeled optical offering in market practice.

### Market split potential

Possible, but current evidence is too thin.

The two local `f/4` examples price above the `f/3.4` cluster, but the sample is too small to treat that as stable round-1 evidence.

### Search-intent split potential

Visible, but sparse.

The wording exists and is explicit, but current operational repetition is limited.

### Final decision

`hold`

### One-line reason

`21mm f/4 Super-Angulon` is literature-real and title-visible, but current local support is too thin for immediate round-1 core seeding.

## Candidate 3: finder requirement / finder bundle / hood bundle

### Official / literature basis

Real accessories and workflow requirements exist.

### Mechanical distinction

Not enough for standalone canonical rows.

These describe how the lens is used or bundled, not a separate lens line.

### Optical distinction

None.

### Market split potential

Weak and bundle-driven.

### Search-intent split potential

Some operational value, but still metadata-level.

### Final decision

`overlay`

### One-line reason

Finder / hood / bundle signals matter operationally but do not define separate canonical lens entities.

## Candidate 4: black / silver finish

### Official / literature basis

Real finish variation.

### Mechanical distinction

Weak for canonical purposes.

### Optical distinction

None.

### Market split potential

Unclear and likely secondary.

### Search-intent split potential

Visible but still metadata-like.

### Final decision

`overlay`

### One-line reason

Black and silver appear in titles but behave like finish metadata, not first-pass canonical rows.

## Candidate 5: `Elmarit 21`, `Super-Elmar 21`, `Tri-Elmar 21` boundary

### Official / literature basis

Strongly separate.

These are neighboring Leica naming families, not internal `Super-Angulon 21` variants.

### Final decision

`보류` inside this family, meaning out-of-family contamination to exclude

### One-line reason

The family boundary must stay tight or `Super-Angulon 21` will incorrectly absorb later Leica 21mm lines.

## Round-1 Recommendation

Recommended immediate `core` candidate count: `1`

Recommended first-pass seed row:

1. `Leica Super-Angulon 21mm f/3.4`

Recommended future `hold` candidate:

1. `Leica Super-Angulon 21mm f/4`

## What Should Stay Below Seed Level For Now

- finder bundle / hood bundle
- black / silver finish
- country marking
- packaging completeness
- collector-only shorthand

## Can The Next Round Move To Seed Addition?

`Yes`

But it should be narrow:

- add `Leica Super-Angulon 21mm f/3.4` as the only immediate `core` row
- keep `21mm f/4` for a later hold-seed audit unless more local support appears

That is the most conservative and operationally useful next step.
