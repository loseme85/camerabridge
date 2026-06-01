# Summilux 28 Taxonomy Audit - Round 1

Date: 2026-05-08

Scope: read-heavy taxonomy audit for the Leica `Summilux 28` family. This round does not add seed rows, does not change classifier/query/search behavior, and does not change admin lookup ranking or UI. The goal is to determine whether `Summilux 28` is mature enough for explicit canonical seeding and, if so, at what granularity.

## Executive Summary

`Summilux 28` is seedable, and round-1 should stay narrow.

The strongest round-1 conclusion is:

1. `Leica Summilux-M 28mm f/1.4 ASPH`

should be treated as the only immediate first-pass `core` entity.

Round-1 conclusion:

- immediate recommended `core` candidate count: `1`
- recommended first-pass core:
  - `Leica Summilux-M 28mm f/1.4 ASPH`
- explicit `hold` candidate:
  - none recommended in round-1
- `6bit`, `black / silver`, `country marking`, `hood included`, `boxed`, `special edition`, and `coding` stay `overlay` or `보류`
- `Summicron 28`, `Elmarit 28`, `Summaron 28`, `Q/Q2/Q3 28mm`, `R 28`, `SL / APO-Summicron-SL 28`, accessories, and third-party 28mm lenses remain out-of-family boundaries

## Family Overview

The Leica `28mm` field is crowded and easy to contaminate:

- `Elmarit-M 28`
- `Summicron-M 28`
- `Summilux-M 28`
- `Summaron-M 28`
- `Q / Q2 / Q3` fixed-lens bodies
- `R 28`
- `SL` / `APO-Summicron-SL 28`
- third-party `Voigtlander`, `Zeiss`, `TTArtisan`, `Thypoch` 28mm lenses

For canonical purposes, `Summilux 28` should remain narrow and lens-only.

The round-1 question is whether this is:

1. a broad single-line family, or
2. a family with a visible internal generation split that should already become `hold`

Round-1 answer: this is best treated as a clean modern Leica M single-line family.

## Literature / Reference Base

### Source A: Leica Camera official product page

Leica’s current product page consistently names the lens as:

- `Summilux-M 28 f/1.4 ASPH.`

It is presented as a current Leica M lens line with:

- `28mm` focal length
- `f/1.4` maximum aperture
- `ASPH`
- `0.7m` close focus distance

Reference:

- [Leica Camera - Summilux-M 28 f/1.4 ASPH.](https://leica-camera.com/en-US/photography/lenses/m/summilux-m-28mm-f1-4-asph-black)
- [Leica Camera technical specification page](https://leica-camera.com/en-US/photography/lenses/m/summilux-m-28-f1-4-asph-silver-finish/technical-specification)

### Source B: Leica press release

Leica’s 2015 launch press release introduces:

- `LEICA SUMMILUX-M 28 mm f/1.4 ASPH.`

as a new high-speed Leica M wide-angle lens.

Reference:

- [Leica press release - Leica Summilux-M 28 mm f/1.4 ASPH.](https://leica-camera.com/en-int/Company/Press-Centre/Press-Releases/2015/Press-Release-New-LEICA-SUMMILUX-M-28-mm-f-1.4-ASPH.-A-new-milestone-in-the-world-of-high-speed-wide-angle-lenses)

### Source C: Leica Wiki

Leica Wiki documents the same line as:

- `28mm f/1.4 ASPH. Summilux-M`

with:

- production era beginning in `2015`
- Leica M bayonet
- `10 / 7` optical design
- `0.7m` close focus distance

Reference:

- [Leica Wiki - 28mm f/1.4 ASPH. Summilux-M](https://wiki.l-camera-forum.com/leica-wiki.en/index.php/28mm_f/1.4_ASPH._Summilux-M)

### Interpretation

The literature stack is unusually clean:

1. the official Leica line name is stable
2. there is no strong literature-backed internal generation split to preserve in round-1
3. black / silver are finish variants, not separate optical lines

That supports a narrow single-core recommendation.

## Local Listing Evidence

Analysis base: `data/normalized/normalized_latest.json`

After excluding obvious contamination from:

- `Summicron 28`
- `Elmarit 28`
- `Summaron 28`
- `Q / Q2 / Q3`
- `R 28`
- `SL` / `APO-Summicron-SL 28`
- `Vario-Elmarit`
- accessories, hoods, finders, boxes, and other non-lens listings
- third-party 28mm lenses

the useful local `Summilux 28` pool becomes:

- clean local pool: `29`

### Broad price clustering

KRW-parsed local medians:

| Bucket | Count | KRW-priced | Median KRW | Audit note |
| --- | ---: | ---: | ---: | --- |
| broad `Summilux-M 28mm f/1.4 ASPH` pool | 29 | 17 | ~6.80M KRW | stable broad family anchor |

Observed price spread:

- min priced example: ~`4.70M KRW`
- median: ~`6.80M KRW`
- max priced example: ~`8.70M KRW`

### Local title patterns

Broad recurring titles:

- `Leica M 28mm f1.4 Summilux ASPH 6bit Black`
- `신품 Leica M 28mm f1.4 Summilux ASPH 6bit Black`
- `[위탁] M 28/1.4 Summilux ASPH (Black)`
- `[위탁] M 28/1.4 Summilux ASPH 6bit (Black)`
- `[중고] M 28/1.4 Summilux ASPH (Black)`
- `[중고] M 28/1.4 Summilux ASPH 6bit (Black)`
- `LEICA 28mm F1.4 ASPH SUMMILUX-M sn.4205`
- `LEICA 28mm F1.4 ASPH SUMMILUX-M sn.4702`

### Local marker frequency

Repeated local modifiers:

- `ASPH`: `28`
- `6bit`: `13`
- `black`: `16`

Sparse or effectively absent modifiers:

- `silver`
- `Safari`
- `Titan`
- `anniversary`
- `Germany`
- `Canada`
- `close focus`
- `0.4m`

### Interpretation

The local pool supports one very strong conclusion:

1. broad `Summilux 28` language is stable
2. title wording converges on a single Leica M line
3. recurring modifiers are metadata-like, not line-splitting

There is no round-1 evidence for a meaningful internal `hold` split.

## Candidate Entity Expansion

## Candidate 1: `Leica Summilux-M 28mm f/1.4 ASPH`

### Official / literature basis

Strong.

This is the broad Leica M line consistently supported by Leica literature and local title language.

### Mechanical distinction

Strong enough for `core`.

It has:

- explicit `Summilux-M` naming
- explicit `28mm f/1.4`
- explicit `ASPH`

### Optical distinction

Strong enough for `core`.

This is not a variant of `Summicron 28` or `Elmarit 28`. It is its own Leica M optical line.

### Market split potential

Strong.

The local priced pool is large enough to anchor a canonical row without overfitting.

### Search-intent split potential

Strong.

Queries like:

- `summilux 28`
- `28 summilux`
- `summilux-m 28`
- `28mm f1.4 summilux`
- `28mm f1.4 asph summilux`
- `28 lux`
- `m 28/1.4 summilux`

all point to the same stable lens intent.

### Verdict

`core`

## Candidate 2: finish / special-edition / coding variants inside `Summilux 28`

### Official / literature basis

Real as variants, but weak as canonical rows.

Black and silver finishes exist in Leica’s official presentation. `6bit` also appears repeatedly in local dealer language.

### Mechanical distinction

Weak for canonical row purposes.

These are finish / coding / completeness modifiers, not a separate optical line.

### Optical distinction

None meaningful for row splitting.

### Market split potential

Not strong enough for row creation in round-1.

Local price movement may reflect condition, dealer type, or scarcity rather than a separate canonical entity.

### Search-intent split potential

Weak to moderate.

Users may care about:

- `6bit`
- `black`
- `silver`
- boxed / hood-included state

but these are safer as metadata than as separate seeded entities.

### Verdict

`overlay`

## Candidate 3: hypothetical internal generation / version split

### Official / literature basis

Weak for round-1 purposes.

The literature reviewed for this line does not expose a strong major internal Leica generation split analogous to, for example, a modern close-focus revision in another family.

### Mechanical distinction

Not operationally visible enough.

### Optical distinction

Not operationally visible enough.

### Market split potential

Weak.

No stable seller wording cluster emerged from the local pool.

### Search-intent split potential

Weak.

There is no repeating local subgroup like `II`, `NEW`, `신형`, or other reliable seller shorthand.

### Verdict

`보류`

## Contamination / Boundary Review

The following must remain out-of-family boundaries:

- `Summicron 28`
- `Elmarit 28`
- `Summaron 28`
- `Q / Q2 / Q3` fixed-lens 28mm bodies
- `R 28`
- `SL` / `APO-Summicron-SL 28`
- `Vario-Elmarit`
- accessory-only results such as hoods, finders, caps, boxes
- third-party `Voigtlander`, `Zeiss`, `TTArtisan`, `Thypoch` 28mm lenses

Boundary examples to keep separate:

- `summicron 28`
- `elmarit 28`
- `summaron 28`
- `q2 28`
- `q3 28`
- `apo summicron sl 28`
- `elmarit-r 28`
- `voigtlander 28`
- `zeiss 28`
- `hood 28 summilux`
- `finder 28 summilux`

## Round-1 Recommendation Table

| Candidate | Verdict | Why |
| --- | --- | --- |
| `Leica Summilux-M 28mm f/1.4 ASPH` | `core` | literature, local title language, and broad price pool all align |
| finish / `6bit` / boxed / hood / country / special-edition metadata | `overlay` | real modifiers, but not separate optical lines |
| hypothetical internal version split | `보류` | no stable local title support |
| other Leica 28mm families / bodies / accessories / third-party | `out-of-family` | boundary must stay strict |

## Immediate Core Candidate Count

Recommended immediate `core` candidate count: `1`

Recommended first-pass `core`:

1. `Leica Summilux-M 28mm f/1.4 ASPH`

## Hold Candidate

None recommended in round-1.

If a later audit discovers a real, repeated market shorthand tied to a documented revision or special line, that should be reconsidered then. Current evidence does not justify an explicit `hold` row yet.

## Overlay Elements

Keep these as `overlay`, not separate rows:

- `6bit`
- `black / silver`
- `country marking`
- `hood included`
- `boxed`
- `condition`
- `special edition`
- `coding`
- `packaging`
- limited finish variants

## Seed Readiness

Yes. `Summilux 28` is ready for a narrow seed round.

The safest next step would be:

1. add exactly one `core` seed row:
   - `Leica Summilux-M 28mm f/1.4 ASPH`

and leave all finish / coding / packaging variation as `overlay`.
