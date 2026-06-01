# Summicron 28 Taxonomy Audit - Round 1

Date: 2026-05-08

Scope: read-heavy taxonomy audit for the Leica `Summicron 28` family. This round does not add seed rows, does not change classifier/query/search behavior, and does not change admin lookup ranking or UI. The goal is to determine whether `Summicron 28` is mature enough for explicit canonical seeding and, if so, at what granularity.

## Executive Summary

`Summicron 28` is seedable, but round-1 should be conservative.

The strongest round-1 conclusion is:

1. `Leica Summicron-M 28mm f/2 ASPH`

should be treated as the only immediate first-pass `core` entity.

There is also one meaningful narrower candidate:

1. `Leica Summicron-M 28mm f/2 ASPH current close-focus generation`

as a plausible explicit `hold` row for a future round, driven by local `II / NEW / 신형` wording and Leica’s 2023 close-focus revision.

Round-1 conclusion:

- immediate recommended `core` candidate count: `1`
- recommended first-pass core:
  - `Leica Summicron-M 28mm f/2 ASPH`
- explicit `hold` candidate:
  - current close-focus / `ASPH II` / `NEW` / `신형` line
- `6bit`, `black / silver`, `country marking`, `hood included`, `boxed`, `special edition`, and `coding` stay `overlay` or `보류`
- `Safari`, `titan`, and `matte black paint` are real market variants, but round-1 should not promote them beyond metadata / special-edition territory
- `Elmarit 28`, `Summilux 28`, `Summaron 28`, `Q/Q2/Q3 28mm`, `R 28`, `SL APO-Summicron-SL 28`, accessories, and third-party 28mm lenses remain out-of-family boundaries

## Family Overview

The `28mm` Leica field is crowded and easily contaminated:

- `Elmarit-M 28`
- `Summicron-M 28`
- `Summilux-M 28`
- `Summaron-M 28`
- `Q / Q2 / Q3` fixed-lens bodies
- `R 28`
- `SL APO-Summicron-SL 28`
- third-party `ZM` / `Voigtlander` / other M-mount 28mm lenses

For canonical purposes, `Summicron 28` needs to remain narrow and lens-only.

The first round-1 taxonomic question is whether this is:

1. a broad single-line family, or
2. a family with a major current-generation split already visible enough to preserve as an explicit `hold`.

Round-1 answer: `both`, but asymmetrically:

- broad `Summicron-M 28mm f/2 ASPH` is clearly ready for `core`
- the newer close-focus generation is real, but safer as a future `hold` row than an immediate `core` split

## Literature / Reference Base

### Source A: Leica Wiki - `28mm f/2 ASPH Summicron-M`

Leica Wiki documents the classic Leica M line as:

- `28mm f/2 ASPH Summicron-M`

with:

- production era beginning in `2000`
- Leica M bayonet
- `9 / 6` optical design
- `E46` filter thread
- `0.7m` minimum focusing distance in the long-running earlier line

Reference:

- [Leica Wiki - 28mm f/2 ASPH Summicron-M](https://wiki.l-camera-forum.com/leica-wiki.en/index.php/28mm_f/2_ASPH_Summicron-M)

### Source B: Leica Camera - current `Summicron-M 28 f/2 ASPH.`

Leica’s current product page documents a revised lens with:

- improved minimum focusing distance of `0.4m`
- a dual-curve focusing mechanism
- current production framing as the modern Leica M `Summicron 28`

References:

- [Leica Camera - Summicron-M 28 f/2 ASPH.](https://leica-camera.com/en-int/photography/lenses/m/summicron-m-28-f2-asph-black)
- [Leica Camera US technical specifications](https://leica-camera.com/en-US/photography/lenses/m/summicron-m-28-f2-asph-black/technical-specification)

### Source C: Leica press release for the 2023 revision

Leica’s 2023 press release explicitly presents a further-developed `Summicron-M 28 f/2 ASPH.` with:

- updated technical features
- closest focusing distance extended from `70 cm` to `40 cm`

Reference:

- [Leica press release - New Leica Summicron-M 28 f/2 ASPH.](https://leica-camera.com/es-MX/press/new-leica-summicron-m-28-f2-asph)

### Interpretation

The literature stack supports two true things at once:

1. a broad Leica M family called `Summicron-M 28mm f/2 ASPH`
2. a real later/current close-focus generation inside that family

But literature alone is not enough to promote the later generation to round-1 `core`; local operational signal still needs to be strong enough.

## Local Listing Evidence

Analysis base: `data/derived/results_resolved_v2.json`

After excluding obvious contamination from:

- `APO-Summicron-SL 28`
- `Q / Q2 / Q3` bodies and fixed 28mm lenses
- `Elmarit`, `Summilux`, `Summaron`
- hoods, caps, boxes, and accessory-only listings
- `R 28`
- third-party 28mm lenses

the useful local `Summicron 28` pool becomes:

- clean local pool: `68`

### Broad price clustering

KRW-parsed local medians:

| Bucket | Count | KRW-priced | Median KRW | Audit note |
| --- | ---: | ---: | ---: | --- |
| broad `Summicron-M 28mm f/2 ASPH` pool | 68 | 36 | ~4.68M KRW | stable broad family anchor |
| `ASPH II / NEW / 신형` subgroup | 6 | 6 | ~6.20M KRW | plausible explicit hold subgroup |

Additional special-edition markers:

| Marker | Count | KRW-priced | Median KRW | Audit note |
| --- | ---: | ---: | ---: | --- |
| `Safari` | 5 | 3 | ~5.88M KRW | special edition, not line split |
| `Titan` | 1 | 1 | ~8.90M KRW | too sparse, special variant |
| `Matte black paint` | 1 | 1 | ~8.80M KRW | too sparse, special variant |

### Local title patterns

Broad recurring titles:

- `[중고] M 28/2 Summicron ASPH 6bit (Black)`
- `LEICA 28mm F2 ASPH SUMMICRON-M sn.4613`
- `LEICA 28mm F2 ASPH SUMMICRON-M sn.3901`

Later-generation / explicit narrow titles:

- `LEICA 28mm F2 ASPH II SUMMICRON-M sn.4922`
- `LEICA 28mm F2 ASPH II SUMMICRON-M sn.4900`
- `[위탁] M 28/2 Summicron ASPH NEW (Black)`
- `[중고] M 28/2 Summicron ASPH 6bit 신형 (Black)`

### Local marker frequency

Repeated local modifiers:

- `6bit`: `36`
- `Safari`: `5`
- `II / NEW / 신형`: `6`
- `black`: frequent

Thin / sparse modifiers:

- `silver`
- `titan`
- `matte black paint`

### Interpretation

This family shows a clearer internal split signal than many other modern Leica M families, but not enough for an immediate two-core recommendation:

1. broad `Summicron 28` language is extremely stable
2. current-generation wording exists and repeats
3. current-generation prices trend higher
4. but the subgroup is still small and seller wording mixes official and dealer shorthand

That is exactly the shape of a future `hold` candidate, not a round-1 second `core`.

## Candidate Entity Expansion

## Candidate 1: `Leica Summicron-M 28mm f/2 ASPH`

### Official / literature basis

Strong.

This is the broad Leica M line consistently supported by Leica literature, Leica Wiki, and local title language.

### Mechanical distinction

Strong enough for `core`.

It has:

- explicit `Summicron-M` naming
- explicit `ASPH`
- stable `28mm f/2` reportage-wide identity

### Optical distinction

Strong enough for `core`.

This is not a variant of `Elmarit 28` or `Summilux 28`. It is its own Leica M optical line.

### Market split potential

Strong.

The broad priced pool is large enough and stable enough to anchor a canonical row.

### Search-intent split potential

Strong.

Users and dealers explicitly write:

- `M 28/2 Summicron ASPH`
- `28mm F2 ASPH SUMMICRON-M`
- `28 cron`

### Final decision

`core`

### One-line reason

`Summicron-M 28mm f/2 ASPH` is a literature-stable, high-support Leica M line that is safe to anchor as a broad canonical row.

## Candidate 2: `Leica Summicron-M 28mm f/2 ASPH current close-focus generation`

### Official / literature basis

Real.

Leica officially documents the current close-focus redesign with `0.4m` minimum focus and updated mechanics.

### Mechanical distinction

Strong enough for a narrower row.

This is not just finish or coding. It is a real functional redesign inside the same family.

### Optical distinction

Moderate.

The line remains `Summicron-M 28 f/2 ASPH`, but Leica positions it as a further-developed version with updated technical features.

### Market split potential

Moderate.

The `II / NEW / 신형` subgroup prices materially above much of the older broad pool.

### Search-intent split potential

Moderate to strong when explicit wording is present.

Titles already use:

- `ASPH II`
- `NEW`
- `신형`

### Final decision

`hold`

### One-line reason

The current close-focus generation is real and operationally visible, but still best captured as an explicit `hold` row rather than an immediate second `core`.

## Candidate 3: `6bit`

### Official / literature basis

Real feature, but not a separate line.

### Mechanical distinction

Visible but not enough for standalone canonical status.

### Optical distinction

None.

### Market split potential

Weak as a row by itself.

It is spread across both older and newer examples and also across special variants.

### Search-intent split potential

Metadata only.

### Final decision

`overlay`

### One-line reason

`6bit` is repeated and useful, but it behaves like metadata across the family rather than a separate seed row.

## Candidate 4: Safari / Titan / Matte Black Paint / Silver

### Official / literature basis

Mixed but real as product variants.

### Mechanical distinction

Mostly finish / edition level.

### Optical distinction

None.

### Market split potential

They can price higher, but the local pool is sparse and collector-driven.

### Search-intent split potential

Special-edition intent exists, but round-1 canonical splitting would be premature.

### Final decision

`overlay` or `보류`

### One-line reason

These are real market variants, but they should not outrun the main family taxonomy at round 1.

## Candidate 5: boundary families

### Included boundary cases

- `Elmarit 28`
- `Summilux 28`
- `Summaron 28`
- `Q / Q2 / Q3` fixed-lens bodies
- `R 28`
- `APO-Summicron-SL 28`
- accessories and third-party 28mm lenses

### Official / literature basis

Strongly separate.

### Final decision

`out-of-family boundary`

### One-line reason

Without strict boundaries, `Summicron 28` would collapse into a generic Leica or 28mm bucket.

## Round-1 Recommendation

### Recommended immediate `core` count

`1`

### Recommended first-pass core

1. `Leica Summicron-M 28mm f/2 ASPH`

### Recommended explicit `hold` candidates

1. `Leica Summicron-M 28mm f/2 ASPH current close-focus generation`

### Overlay elements

- `6bit`
- black / silver
- country marking
- hood included
- boxed
- condition
- special edition
- coding

## What Should Stay Deferred

The following should remain below round-1 seed level:

- `Safari` as a standalone canonical row
- `Titan` as a standalone canonical row
- `matte black paint` as a standalone canonical row
- any generic `v1 / v2` framing that is not backed by explicit local wording

## Can The Next Round Move To Seed Addition?

`Yes`, but conservatively.

The safest next round is:

1. add `Leica Summicron-M 28mm f/2 ASPH` as the only immediate `core` row

Optional later round:

1. audit or add an explicit `hold` row for the current close-focus / `ASPH II` generation

## Final Judgment

`Summicron 28` is seedable, but round-1 should not over-split it.

The correct posture is:

- open `Leica Summicron-M 28mm f/2 ASPH` as the broad family anchor
- keep the newer close-focus / `II` generation as a plausible `hold` candidate
- leave `6bit`, finish, and special-edition language below canonical-row level
