# Summilux 21 Taxonomy Audit - Round 1

Date: 2026-05-08

Scope: read-heavy taxonomy audit for the Leica `Summilux 21` family. This round does not add seed rows, does not change classifier/query/search behavior, and does not change admin lookup ranking or UI. The goal is to determine whether `Summilux 21` is mature enough for explicit canonical seeding and, if so, at what granularity.

## Executive Summary

`Summilux 21` is seedable, and round-1 should keep it as a narrow single-line modern Leica M family.

The strongest first-pass recommendation is:

1. `Leica Summilux-M 21mm f/1.4 ASPH`

Round-1 conclusion:

- immediate recommended `core` candidate count: `1`
- recommended first-pass core:
  - `Leica Summilux-M 21mm f/1.4 ASPH`
- explicit `hold` candidate:
  - none recommended in round-1
- `6bit` stays `overlay`
- `black / silver`, `country marking`, `hood included`, `finder included`, `boxed`, `condition`, and `special edition` stay `overlay` or `보류`
- `Elmarit 21`, `Super-Elmar 21`, `Super-Angulon 21`, `Tri-Elmar 16-18-21`, `WATE`, `R 21`, `SL / L-mount 21`, accessories, and third-party `21mm` lenses remain out-of-family boundaries

Why this is a single-line family:

- literature documents one stable Leica M product line
- local title language converges on one exact line name
- no internal generation split, close-focus split, or edition split is visible in the current local pool

## Family Overview

The Leica `21mm` field is crowded and easy to contaminate:

- `Elmarit-M 21`
- `Super-Elmar-M 21`
- `Super-Angulon 21`
- `Tri-Elmar 16-18-21`
- `WATE`
- `Elmarit-R 21`
- `SL` / `APO-Summicron-SL 21` and other non-M `21mm` lines
- third-party `Voigtlander`, `Zeiss`, `TTArtisan`, and `Thypoch` `21mm` lenses

For canonical purposes, `Summilux 21` should remain narrow and M-lens only.

The round-1 question is whether this is:

1. a broad single-line family, or
2. a family with a visible internal split that should already become `hold`

Round-1 answer: this is best treated as a clean modern Leica M single-line family.

## Literature / Reference Base

### Source A: Leica Camera official product page

Leica's current product page consistently names the lens as:

- `Summilux-M 21 f/1.4 ASPH.`

It is presented as a current Leica M lens line with:

- `21mm` focal length
- `f/1.4` maximum aperture
- `ASPH`
- `0.7m` close focus
- rectangular screw-on hood workflow

References:

- [Leica Camera - Summilux-M 21 f/1.4 ASPH.](https://leica-camera.com/en-US/photography/lenses/m/summilux-m-21mm-f1-4-asph-black)
- [Leica Camera technical specification](https://leica-camera.com/en-US/photography/lenses/m/summilux-m-21mm-f1-4-asph-black/technical-specification)

### Source B: Leica Wiki

Leica Wiki documents the same line as:

- `21mm f/1.4 ASPH Summilux-M`

with:

- production era `2008-current`
- Leica M bayonet with `6 bit` lens identification
- `10 / 8` optical design
- `f/1.4-f/16`
- `0.7m` focusing range
- Series VIII filter in hood

Reference:

- [Leica Wiki - 21mm f/1.4 ASPH Summilux-M](https://wiki.l-camera-forum.com/leica-wiki.en/index.php/21mm_f/1.4_ASPH_Summilux-M)

### Source C: Leica M-lens lineup reference

Leica's current M-lens catalog still lists:

- `Summilux-M 21 f/1.4 ASPH.`

as one current M-lens line, separate from neighboring `21mm` families.

Reference:

- [Leica M-Lenses](https://leica-camera.com/en-US/photography/lenses/m)

### Interpretation

The literature stack is very clean:

1. the official Leica line name is stable
2. there is no strong literature-backed internal generation split to preserve in round-1
3. the nearby `21mm` Leica families are clearly separate product names

That supports a narrow single-core recommendation.

## Local Listing Evidence

Analysis base: `data/normalized/normalized_latest.json`

After excluding obvious contamination from:

- serial-number false matches from non-`21mm` `Summilux` titles
- `Tri-Elmar` / `WATE`
- `Elmarit 21`
- `Super-Elmar 21`
- `Super-Angulon 21`
- `R 21`
- `SL` / non-M `21mm` lines
- accessories, hoods, finders, caps, and boxes
- third-party `21mm` lenses

the useful local `Summilux 21` pool becomes:

- clean local pool: `18`
- unique title strings: `9`

### Broad price clustering

KRW-parsed local medians:

| Bucket | Count | KRW-priced | Median KRW | Audit note |
| --- | ---: | ---: | ---: | --- |
| broad `Summilux-M 21mm f/1.4 ASPH` pool | 18 | 14 | ~6.74M KRW | stable single-line anchor |

Observed price spread:

- min priced example: ~`4.50M KRW`
- median: ~`6.74M KRW`
- max priced example: ~`7.58M KRW`

### Local title patterns

Broad recurring titles:

- `Leica M 21mm f1.4 Summilux ASPH 6bit Black`
- `[중고] M 21/1.4 Summilux ASPH (Black)`
- `[중고] M 21/1.4 Summilux ASPH 6bit (Black)`
- `[위탁] M 21/1.4 Summilux ASPH 6bit (Black)`
- `LEICA 21mm F1.4 ASPH SUMMILUX-M sn.4083`
- `LEICA 21mm F1.4 ASPH SUMMILUX-M sn.4584`

### Local marker frequency

Repeated local modifiers:

- `ASPH`: `18`
- `6bit`: `9`
- `black`: `11`

Sparse or effectively absent modifiers:

- `silver`
- `germany`
- `canada`
- `finder`
- `hood`
- `boxed`
- `special edition`

### Interpretation

The local pool supports one strong conclusion:

1. broad `Summilux 21` language is stable
2. title wording converges on a single Leica M line
3. recurring modifiers are metadata-like, not line-splitting

There is no round-1 evidence for a meaningful internal `hold` split.

## Candidate Entity Expansion

## Candidate 1: `Leica Summilux-M 21mm f/1.4 ASPH`

### Official / literature basis

Strong.

This is the broad Leica M line consistently supported by Leica literature and local title language.

### Mechanical distinction

Strong enough for `core`.

It has:

- explicit `Summilux-M` naming
- explicit `21mm f/1.4`
- explicit `ASPH`
- stable modern Leica M hood / filter workflow

### Optical distinction

Strong enough for `core`.

This is not a variation of `Elmarit 21`, `Super-Elmar 21`, or `Super-Angulon 21`. It is its own Leica M optical line.

### Market split potential

Strong.

The local priced pool is coherent enough to anchor a canonical row without overfitting.

### Search-intent split potential

Strong.

Queries like:

- `summilux 21`
- `summilux-m 21`
- `21mm f1.4 summilux`
- `m 21/1.4 summilux`

all point to the same line.

### Final decision

`core`

### One-line reason

`Summilux-M 21mm f/1.4 ASPH` is a distinct, clean modern Leica M line with stable title language and no visible round-1 internal split.

## Candidate 2: `6bit`

### Official / literature basis

Real feature, but not a separate line.

### Mechanical distinction

Visible but not enough for standalone canonical status.

### Optical distinction

None.

### Market split potential

Weak as a separate row.

The local pool shows `6bit` repeatedly, but it behaves like expected metadata on the same main line rather than a distinct market entity.

### Search-intent split potential

Moderate as metadata, weak as canonical entity.

### Final decision

`overlay`

### One-line reason

`6bit` appears often, but it behaves like metadata on the main `Summilux-M 21` line rather than a separate seed row.

## Candidate 3: finish / country / finder / hood / boxed / special-edition variations

### Official / literature basis

Weak to mixed.

### Mechanical distinction

Weak.

### Optical distinction

None.

### Market split potential

Too thin in current local data.

### Search-intent split potential

Low in round-1 local evidence.

These modifiers are either absent or too sparse in the clean local pool to justify a row.

### Final decision

`overlay` or `보류`

### One-line reason

finish, country, finder / hood bundle, boxed completeness, and special-edition wording are not strong enough in current local data to justify separate canonical rows.

## Candidate 4: broad shorthand `21 lux`

### Official / literature basis

Weak as a canonical row signal.

### Mechanical distinction

None by itself.

### Optical distinction

None by itself.

### Market split potential

Weak.

As a shorthand, it risks pulling in generic `21mm` and `lux` noise beyond the exact Leica line name.

### Search-intent split potential

Usable as conversational shorthand, but too broad to shape taxonomy by itself.

### Final decision

`보류`

### One-line reason

`21 lux` is plausible user shorthand, but it is too broad to support row-shaping on its own in round-1.

## Overlay / Boundary Notes

### Overlay

Keep these below row level:

- `6bit`
- `black / silver`
- `country marking`
- `hood included`
- `finder included`
- `cap included`
- `boxed`
- `condition`
- `original cap`
- `original hood`
- `original box`
- `packaging`
- `special edition`

### Out-of-family boundary

Keep these outside `Summilux 21`:

- `Elmarit 21`
- `Super-Elmar 21`
- `Super-Angulon 21`
- `Tri-Elmar 16-18-21`
- `WATE`
- `R 21`
- `SL / L-mount 21`
- accessories and finders
- third-party `21mm` lenses

## Final Round-1 Recommendation

- immediate core candidate:
  - `Leica Summilux-M 21mm f/1.4 ASPH`
- hold candidate:
  - none recommended in round-1
- overlay:
  - `6bit`, finish, country, finder / hood / boxed completeness, packaging, and special-edition wording
- out-of-family:
  - `Elmarit 21`, `Super-Elmar 21`, `Super-Angulon 21`, `Tri-Elmar`, `WATE`, `R`, `SL`, accessories, and third-party `21mm` lenses

## Seed Readiness

Round-1 conclusion: `yes`, this family is ready for a narrow seed round.

If a follow-up seed round is opened, the conservative first move should be:

1. add exactly one `core` row:
   - `Leica Summilux-M 21mm f/1.4 ASPH`
2. keep `6bit`, finish, country, finder / hood / box, and special-edition signals below row level
3. do not create an internal split unless later local evidence shows a real market separation
