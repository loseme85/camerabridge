# Summaron 28 Taxonomy Audit - Round 1

Date: 2026-05-08

Scope: read-heavy taxonomy audit for the Leica `Summaron 28` family. This round does not add seed rows, does not change classifier/query/search behavior, and does not change admin lookup ranking or UI. The goal is to determine whether `Summaron 28` is mature enough for explicit canonical seeding and, if so, at what granularity.

## Executive Summary

`Summaron 28` is real, but round-1 should be more conservative than for `Summicron 28` or `Summilux 28`.

The main reason is that local `Summaron 28` listings are not a single modern Leica M line. They are a mixed field containing:

1. modern `Summaron-M 28mm f/5.6` reissue listings
2. original screw-thread / `L` / `LTM` vintage listings

Both are literature-real and both appear locally with meaningful support.

Round-1 conclusion:

- immediate recommended `core` candidate count: `0`
- recommended round-1 disposition: `seed 보류`
- explicit `hold` candidates:
  - `Leica Summaron-M 28mm f/5.6` modern reissue line
  - `Leica Summaron 28mm f/5.6` original screw-thread / LTM generation
- `silver / black`, `finder included`, `hood included`, `boxed`, `original cap`, `original hood`, `original box`, `condition`, and `packaging` stay `overlay`
- `Summicron 28`, `Summilux 28`, `Elmarit 28`, `Q/Q2/Q3 28mm`, `R 28`, `SL / APO-Summicron-SL 28`, accessories, and third-party 28mm lenses remain out-of-family boundaries

The safest next step is not a round-1 seed add, but a narrow hold-seed audit for the two explicit sub-lines above.

## Family Overview

The `28mm` Leica field is crowded and easy to contaminate:

- `Elmarit-M 28`
- `Summicron-M 28`
- `Summilux-M 28`
- `Summaron`
- `Q / Q2 / Q3` fixed-lens bodies
- `R 28`
- `SL` / `APO-Summicron-SL 28`
- accessories and third-party 28mm lenses

Unlike `Summilux 28`, the `Summaron 28` space is not one clean modern family. It is structurally split between:

- a 2016 Leica M reissue line
- an original screw-thread historical line

That split is real in literature and visible in local seller wording.

## Literature / Reference Base

### Source A: Leica Camera official current product page

Leica’s official product page documents:

- `Summaron-M 28 f/5.6`

as a modern Leica M lens line.

Leica explicitly says the current model is based on a screw-mount predecessor produced between `1955` and `1963`, while adding modern M-bayonet and `6-bit` coding.

References:

- [Leica Camera - Summaron-M 28 f/5.6](https://leica-camera.com/en-US/photography/lenses/m/summaron-m-28mm-f5-6-silver)
- [Leica technical specification page](https://leica-camera.com/ko-KR/photography/lenses/m/summaron-m-28mm-f5-6-silver/technical-specification)

### Source B: Leica 2016 press release

Leica’s 2016 press release presents:

- `LEICA SUMMARON-M 28 mm f/5.6`

as a modern renaissance of a classic lens, and explicitly distinguishes it from its screw-mount ancestor.

Reference:

- [Leica press release - Summaron-M 28 mm f/5.6](https://leica-camera.com/en-GB/Company/Press-Centre/Press-Releases/Press-Releases-2016/Press-Release-Renaissance-of-a-classic-lens-Ultra-compact-LEICA-SUMMARON-M-28-mm-f-5.6-wide-angle-lens-for-unobtrusive-reportage-photography)

### Source C: Leica Wiki for the original lens

Leica Wiki documents the original line as:

- `Summaron f= 2.8 cm 1:5.6`

with:

- production era `1955-1963`
- screw-thread origin
- original historical inscription
- later small M-assigned runs and adapter-related context in Leica history

Reference:

- [Leica Wiki - Summaron f= 2.8 cm 1:5.6](https://wiki.l-camera-forum.com/leica-wiki.en/index.php/Summaron_f%3D_2.8_cm_1%3A5.6)

### Interpretation

The literature stack supports two true things:

1. `Summaron-M 28mm f/5.6` is a distinct modern Leica M line
2. the original `Summaron 28mm f/5.6` screw-thread / LTM line is also a distinct historical line

So this is not a fake split invented by the market. The question is whether local listing language is strong enough to open either line as immediate `core`.

## Local Listing Evidence

Analysis base: `data/normalized/normalized_latest.json`

After excluding obvious contamination from:

- `Summicron 28`
- `Summilux 28`
- `Elmarit 28`
- `Q / Q2 / Q3`
- `R 28`
- `SL` / `APO-Summicron-SL 28`
- `Vario-Elmarit`
- accessory-only listings
- third-party 28mm lenses

the useful local `Summaron 28` pool becomes:

- clean local pool: `67`

### Broad price clustering

KRW-parsed local medians:

| Bucket | Count | KRW-priced | Median KRW | Audit note |
| --- | ---: | ---: | ---: | --- |
| broad `Summaron 28` pool | 67 | 42 | ~3.05M KRW | mixed original + reissue family |
| modern `M` / `6bit` / `복각` / `신형` subgroup | 43 | 24 | ~2.89M KRW | modern reissue cluster |
| `L` / `LTM` / `오리지날` subgroup | 15 | 14 | ~3.64M KRW | vintage original cluster |

Observed broad range:

- min priced example: ~`2.50M KRW`
- median: ~`3.05M KRW`
- max priced example: ~`5.88M KRW`

### Local title patterns

Modern reissue wording:

- `Leica M 28mm f5.6 Summaron 6bit Silver 신형`
- `[중고] M 28/5.6 Summaron 6bit 복각 (Silver)`
- `[위탁] M 28/5.6 Summaron 6bit (Silver) 복각`
- `LEICA 28mm F5.6 SUMMARON-M sn.4790`
- `LEICA 28mm F5.6 SUMMARON-M sn.4711`

Original / historical wording:

- `Leica L 28mm f5.6 Summaron Silver`
- `[중고] L 28/5.6 Summaron (Silver)`
- `[중고] L 28/5.6 Summaron 오리지날 (Silver)`
- `LEICA 28mm F5.6 Summaron sn.1412`
- `LEICA 28mm F5.6 + LTM Summaron sn.1412`

### Local marker frequency

Repeated local modifiers:

- `복각`: `11`
- `silver`: `29`
- `6bit`: frequent inside the reissue subgroup

Sparse but meaningful modifiers:

- `LTM`: `1`
- `black`: `2`
- `오리지날`: visible in at least one direct title

Near-absent as repeated group labels:

- `finder`
- `hood`
- `box`
- `goggles`
- `goggle`

### Interpretation

This family differs from clean modern Leica M families in one important way:

1. broad generic `Summaron 28` language does not point to one single line
2. local title support does separate reissue vs original, but mainly when explicit `M / 6bit / 복각` or `L / 오리지날 / LTM` wording is present
3. the priced pools look directionally distinct, but also collector-influenced

That is the shape of explicit `hold` candidates, not a round-1 broad `core`.

## Candidate Entity Expansion

## Candidate 1: `Leica Summaron-M 28mm f/5.6`

### Official / literature basis

Strong.

This is a documented modern Leica M line introduced in 2016.

### Mechanical distinction

Strong.

It has:

- `Summaron-M` naming
- Leica M bayonet
- `6-bit` coding
- modern manufacturing

### Optical distinction

Moderately strong.

Leica positions it as preserving the original formula, but it is still a distinct current production line with a different canonical product identity.

### Market split potential

Moderate to strong.

The local `M / 6bit / 복각 / 신형` subgroup is large enough to be real, but not broad enough to safely stand in for every generic `Summaron 28` query.

### Search-intent split potential

Moderate.

When users say:

- `summaron-m 28`
- `m 28/5.6 summaron`
- `summaron 28 복각`

the intent looks much narrower and safer than generic `summaron 28`.

### Verdict

`hold`

## Candidate 2: `Leica Summaron 28mm f/5.6` original screw-thread / LTM generation

### Official / literature basis

Strong.

This is the historical 1955-1963 original line.

### Mechanical distinction

Strong.

It is a screw-thread / `L` / `LTM` historical line and not identical to the modern `Summaron-M`.

### Optical distinction

Historically meaningful.

Although Leica markets the reissue as preserving the optical formula, the collector market still treats the original screw-thread line as its own object.

### Market split potential

Moderate.

Local `L / 오리지날 / LTM` titles are clearly visible and trend higher than the modern reissue pool.

### Search-intent split potential

Moderate.

When users say:

- `summaron 28 vintage`
- `summaron 28 ltm`
- `summaron 28 original`

the search intent is clearly narrower than broad `summaron 28`.

### Verdict

`hold`

## Candidate 3: broad generic `Summaron 28`

### Official / literature basis

Too mixed.

The family name exists, but it spans both original and reissue lines in current local usage.

### Mechanical distinction

Too mixed for round-1.

### Optical distinction

Too mixed for round-1.

### Market split potential

Ambiguous.

The broad pool median is not a clean market anchor because it blends reissue and vintage listings.

### Search-intent split potential

Weak for a seeded broad row.

Generic `summaron 28` can plausibly mean either:

- modern `Summaron-M 28 f/5.6`
- original `LTM` / historical `Summaron 28 f/5.6`

### Verdict

`보류`

## Overlay Review

Keep these as `overlay`, not separate rows:

- `black / silver`
- `country marking`
- `hood included`
- `finder included`
- `boxed`
- `condition`
- `original cap`
- `original hood`
- `original box`
- `packaging`

Special note:

- `복각` wording is sometimes a real subgroup signal, but round-1 should still avoid turning the raw Korean seller shorthand itself into a canonical truth row name.

## Contamination / Boundary Review

The following must remain out-of-family boundaries:

- `Summicron 28`
- `Summilux 28`
- `Elmarit 28`
- `Q / Q2 / Q3` fixed-lens 28mm bodies
- `R 28`
- `SL` / `APO-Summicron-SL 28`
- `Vario-Elmarit`
- accessory-only results such as hoods, finders, caps, boxes
- third-party `Voigtlander`, `Zeiss`, `TTArtisan`, `Thypoch` 28mm lenses

Boundary examples to keep separate:

- `summicron 28`
- `summilux 28`
- `elmarit 28`
- `q2 28`
- `q3 28`
- `apo summicron sl 28`
- `elmarit-r 28`
- `voigtlander 28`
- `zeiss 28`
- `hood 28 summaron`
- `finder 28 summaron`

## Round-1 Recommendation Table

| Candidate | Verdict | Why |
| --- | --- | --- |
| `Leica Summaron-M 28mm f/5.6` | `hold` | literature-real, local `M / 6bit / 복각 / 신형` wording repeats, but broad generic family remains mixed |
| `Leica Summaron 28mm f/5.6` original screw-thread / LTM generation | `hold` | literature-real and locally visible, but too collector-shaped for broad core in round-1 |
| broad generic `Summaron 28` | `보류` | local pool blends original and reissue, so generic query is not stable enough |
| finish / finder / hood / box / packaging elements | `overlay` | meaningful metadata, not separate optical lines |
| other Leica 28mm families / bodies / accessories / third-party | `out-of-family` | boundary must stay strict |

## Immediate Core Candidate Count

Recommended immediate `core` candidate count: `0`

Round-1 recommendation:

- `seed 보류`

## Hold Candidates

Recommended explicit `hold` candidates for future rounds:

1. `Leica Summaron-M 28mm f/5.6`
2. `Leica Summaron 28mm f/5.6` original screw-thread / LTM generation

These are strong enough for a future narrow hold-seed audit, but not yet broad enough to justify a round-1 core anchor.

## Seed Readiness

Not for immediate round-1 core seeding.

The safest next step would be:

1. do not add a broad generic `Summaron 28` seed row
2. if needed, run a narrow follow-up audit on:
   - modern `Summaron-M 28mm f/5.6`
   - original `Summaron 28mm f/5.6` screw-thread / LTM line
3. only then decide whether either deserves an explicit `hold` row

In short: `Summaron 28` is taxonomy-real, but round-1 broad seeding would be too blunt.
