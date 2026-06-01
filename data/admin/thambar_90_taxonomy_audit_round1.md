# Thambar 90 Taxonomy Audit - Round 1

Date: 2026-05-08

Scope: read-heavy taxonomy audit for the Leica `Thambar 90` family. This round does not add seed rows, does not change classifier/query/search behavior, and does not change admin lookup ranking or UI. The goal is to determine whether `Thambar 90` is mature enough for explicit canonical seeding and, if so, at what granularity.

## Executive Summary

`Thambar 90` is literature-real, but round-1 should stay conservative.

The key issue is that the local pool is very small and the generic `Thambar 90` wording is not a single modern Leica M line. The local evidence contains:

1. modern `Thambar-M 90mm f/2.2` reissue titles
2. plain `Thambar 90mm f/2.2` titles that appear to be original vintage listings

Round-1 conclusion:

- immediate recommended `core` candidate count: `0`
- recommended round-1 disposition: `seed 보류`
- strongest explicit `hold` candidate:
  - `Leica Thambar-M 90mm f/2.2`
- secondary literature-real but still deferred candidate:
  - original `Leica Thambar 9cm / 90mm f/2.2` screw-thread generation
- `center spot filter included`, `hood included`, `cap included`, `boxed`, `case included`, `condition`, and related completeness details stay `overlay`
- `Summicron 90`, `APO-Summicron-M 90`, `Elmarit 90`, `Tele-Elmarit 90`, `Elmar 90`, `Elmar-C 90`, `Macro-Elmar-M 90`, `R 90`, `SL 90`, accessories, and third-party 90mm lenses remain out-of-family boundaries

The safest next step is not a seed add, but a narrow hold-seed audit focused on the modern `Thambar-M 90mm f/2.2` line.

## Family Overview

The Leica `90mm` field is already crowded:

- `Summicron 90`
- `APO-Summicron-M 90`
- `Elmarit 90`
- `Tele-Elmarit 90`
- `Elmar 90`
- `Elmar-C 90`
- `Macro-Elmar-M 90`
- `Thambar 90`
- `R 90`
- `SL / APO-Summicron-SL 90`

`Thambar 90` is special because the vintage/original line and the modern reissue line share the same focal length and soft-focus identity, while using different canonical product naming:

- original historical lens: `Thambar f=9 cm 1:2.2`
- modern Leica M reissue: `Thambar-M 90mm f/2.2`

So the real taxonomy question is not whether the split exists, but whether local listing language is strong enough to safely seed either side.

## Literature / Reference Base

### Source A: Leica official current product page

Leica’s current product page documents:

- `Thambar-M 90 f/2.2`

as a modern Leica M lens line. Leica explicitly describes it as a present-day lens based on the original 1935 design and notes Leica M bayonet / 6-bit identification in the technical section.

References:

- [Leica Camera - Thambar-M 90 f/2.2](https://leica-camera.com/ko-KR/photography/lenses/m/thambar-m-90mm-f2-2-black-painted)

### Source B: Leica 2017 press release

Leica’s 2017 press release presents:

- `Leica Thambar-M 1:2.2/90`

as a modern renaissance of the classic lens. Leica states that the new Thambar-M follows the original lens concept very closely and positions it as a current M-system product.

Reference:

- [Leica press release - Thambar-M 1:2.2/90](https://leica-camera.com/ja-JP/Company/Press-Centre/Press-Releases/2017/Press-Release-Leica-Camera-AG-presents-a-modern-renaissance-of-the-classic-lens-%E2%80%93-the-Leica-Thambar-M-1-2.2-90)

### Source C: Leica Wiki for the original lens

Leica Wiki documents the original line as:

- `Thambar f= 9 cm 1:2.2`

with:

- production era `1935-1942`
- Leica screw-thread mount
- `4 / 3` optical design
- red / black scale for use with / without the spot filter

Reference:

- [Leica Wiki - Thambar f= 9 cm 1:2.2](https://wiki.l-camera-forum.com/leica-wiki.en/index.php?title=Thambar_f%3D_9_cm_1%3A2.2)

### Interpretation

The literature stack supports two true things:

1. `Thambar-M 90mm f/2.2` is a distinct modern Leica M reissue line
2. the original `Thambar 9cm / 90mm f/2.2` screw-thread line is also a distinct historical line

So the split is real in literature. The round-1 question is whether local market wording is strong enough to seed one or both lines safely.

## Local Listing Evidence

Analysis base: `data/derived/results_resolved_v2.json`

After excluding obvious contamination from:

- `Summicron 90`
- `APO-Summicron-M 90`
- `Elmarit 90`
- `Tele-Elmarit 90`
- `Elmar 90`
- `Elmar-C 90`
- `Macro-Elmar-M 90`
- `R 90`
- `SL / APO-Summicron-SL 90`
- accessory-only listings
- third-party 90mm lenses

the useful local `Thambar 90` pool becomes:

- clean local pool: `6`
- unique title strings: `4`

### Broad price clustering

KRW-priced local observations:

- broad `Thambar 90` pool: `0` priced examples
- modern `Thambar-M` subgroup: `0` priced examples
- plain `Thambar` subgroup: `0` priced examples

So round-1 cannot use local price separation as a reliable decision axis here.

### Local title patterns

Modern reissue wording:

- `LEICA 90mm F2.2 THAMBAR-M sn.4694`

Plain historical wording:

- `LEICA 90mm F2.2 Thambar sn.3752`
- `LEICA 90mm F2.2 Thambar sn.4723`
- `LEICA 90mm F2.2 Thambar sn.2472`

### Local marker frequency

Repeated local modifiers:

- `thambar-m`: `2`

Not meaningfully present in local titles:

- `9cm`
- `ltm`
- `original`
- `오리지날`
- `vintage`
- `reissue`
- `복각`
- `신형`
- `center spot filter`
- `hood`
- `case`
- `box`

### Interpretation

This family does not look like a broad modern Leica M single-line family.

Instead:

1. the local pool is tiny
2. the modern reissue side is explicit when `Thambar-M` appears
3. the original side appears locally only as plain `Thambar` titles, without repeated explicit `9cm / LTM / original / vintage` wording
4. priced support is absent

That is enough to justify a narrow future `hold` review for `Thambar-M`, but not enough to open a broad `core` or confidently open the original line as a hold row in round-1.

## Candidate Entity Expansion

## Candidate 1: `Leica Thambar-M 90mm f/2.2`

### Official / literature basis

Strong.

This is a documented modern Leica M line with stable official naming.

### Mechanical distinction

Strong.

It is the modern Leica M reissue line, distinguished in literature by:

- Leica M bayonet
- current M-system product framing
- modern production
- Leica M 6-bit lens identification in the official specification

### Optical distinction

Moderately strong.

Leica explicitly frames it as preserving the original optical character while reissuing the lens as a current Leica M product.

### Market split potential

Moderate.

The local pool is small, but when `Thambar-M` appears, it points cleanly to the modern reissue intent.

### Search-intent split potential

Good enough for a future `hold` row, not a round-1 `core`.

Queries like:

- `thambar-m 90`
- `90mm f2.2 thambar-m`
- `thambar 90 reissue`
- `thambar 90 복각`
- `thambar 90 신형`

would express a narrow modern-reissue intent if local support expands. Right now, only the `Thambar-M` wording itself is directly evidenced locally.

### Verdict

- round-1 status: `hold` candidate

## Candidate 2: original `Leica Thambar 9cm / 90mm f/2.2`

### Official / literature basis

Strong.

This is a real historical line, not a market fiction.

### Mechanical distinction

Strong in literature.

The original lens is documented as a Leica screw-thread design, with historical `9 cm` naming and period-specific accessory context.

### Optical distinction

Real, but not the main operational issue.

The round-1 problem is not whether the original exists. It is whether local listing titles expose that original intent safely enough for seed matching.

### Market split potential

Directionally yes, operationally weak.

The plain `Thambar` listings are very likely original vintage examples, but local sellers are not repeatedly using the safer explicit markers that would let us isolate them without inference.

### Search-intent split potential

Weak for round-1.

The problem is that local listings do **not** repeatedly say:

- `9cm`
- `ltm`
- `original`
- `오리지날`
- `vintage`

So a future hold row like:

- `Leica Thambar 90mm f/2.2 original screw-thread / LTM`

would be literature-correct, but local title support is still too thin.

### Verdict

- round-1 status: `보류`

## Broad Candidate: `Leica Thambar 90mm f/2.2`

### Official / literature basis

Too broad.

This wording collapses original and reissue into one umbrella.

### Search-intent split potential

Not safe enough.

Generic queries like:

- `thambar 90`
- `90 thambar`
- `90mm f2.2 thambar`

can plausibly refer to either:

- the modern `Thambar-M`
- or the original vintage line

### Verdict

- round-1 status: `seed 보류`

## Contamination / Boundary Review

The `Thambar 90` pool must remain separate from:

- `Summicron 90`
- `APO-Summicron-M 90`
- `Elmarit 90`
- `Tele-Elmarit 90`
- `Elmar 90`
- `Elmar-C 90`
- `Macro-Elmar-M 90`
- `R 90` lines
- `SL / APO-Summicron-SL 90`
- accessory-only listings such as hood / filter / center spot filter / cap / case / box
- third-party `90mm` lenses from Voigtlander, Zeiss, and others

No evidence in this round suggests those boundaries should be relaxed.

## Overlay vs Hold vs Deferred

### Overlay

The following should stay below row level:

- `black / chrome / silver`
- `country marking`
- `center spot filter included`
- `hood included`
- `cap included`
- `boxed`
- `case included`
- `condition`
- `original cap`
- `original hood`
- `original box`
- `original case`
- `packaging`

These can move price a lot in collector markets, but they do not justify a round-1 canonical row.

### Hold

- `Leica Thambar-M 90mm f/2.2`

### Deferred / 보류

- original `Leica Thambar 9cm / 90mm f/2.2` screw-thread generation
- broad `Leica Thambar 90mm f/2.2`

## Final Recommendation

### Immediate core candidate

- none
- round-1 recommendation: `seed 보류`

### Hold candidate

- `Leica Thambar-M 90mm f/2.2`

### Overlay

- `black / chrome / silver`
- `country marking`
- `center spot filter included`
- `hood included`
- `cap included`
- `boxed`
- `case included`
- `condition`
- `original cap / hood / box / case`
- `packaging`

### Out-of-family boundary

- `Summicron 90`
- `APO-Summicron-M 90`
- `Elmarit 90`
- `Tele-Elmarit 90`
- `Elmar 90`
- `Elmar-C 90`
- `Macro-Elmar-M 90`
- `R 90`
- `SL / APO-Summicron-SL 90`
- accessory-only listings
- third-party 90mm lenses

## Seed Readiness

Round-1 answer:

- broad `Thambar 90` seed add: `no`
- immediate `core` add: `no`
- narrow future hold-seed audit for `Leica Thambar-M 90mm f/2.2`: `yes`
- original vintage `Thambar 9cm / 90mm f/2.2` hold-seed add: `not yet`

## Practical Next Step

The most conservative next move is:

1. keep broad `Thambar 90` closed
2. run a narrow hold-seed audit for `Leica Thambar-M 90mm f/2.2`
3. leave the original vintage line deferred until local explicit wording (`9cm`, `LTM`, `original`, `오리지날`, `vintage`) appears more consistently
