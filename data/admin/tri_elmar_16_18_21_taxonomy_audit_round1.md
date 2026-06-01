# Tri-Elmar 16-18-21 Taxonomy Audit - Round 1

Date: 2026-05-09

Scope: read-heavy taxonomy audit for the Leica `Tri-Elmar 16-18-21` / `WATE` family. This round does not add seed rows, does not change classifier/query/search behavior, and does not change admin lookup ranking or UI. The goal is to determine whether the Leica wide-angle tri-focal M lens is mature enough for explicit canonical seeding and, if so, at what granularity.

## Executive Summary

`Tri-Elmar 16-18-21` is seedable, and round-1 should keep it as a narrow single-line Leica M family.

The strongest first-pass recommendation is:

1. `Leica Tri-Elmar-M 16-18-21mm f/4 ASPH`

Round-1 conclusion:

- immediate recommended `core` candidate count: `1`
- recommended first-pass core:
  - `Leica Tri-Elmar-M 16-18-21mm f/4 ASPH`
- explicit `hold` candidate:
  - none recommended in round-1
- `finder included`, `Frankenfinder included`, `hood included`, `boxed`, `case included`, `6bit`, `black / silver`, and `country marking` stay `overlay` or `보류`
- `WATE` is literature-real shorthand, but current local title support is too thin to let it shape a standalone row or broad alias by itself
- `Elmarit 21`, `Super-Elmar 21`, `Super-Angulon 21`, `Summilux 21`, `Tri-Elmar 28-35-50` / `MATE`, `R`, `SL`, accessories, and third-party wide lenses remain out-of-family boundaries

Why this is a single-line family:

- literature documents one stable Leica M line
- local title language converges on one exact `16-18-21 / f4 / Tri-Elmar-M` product
- visible listing variation is mostly bundle metadata, especially `finder set`, rather than a real internal lens split

## Family Overview

The Leica `21mm` wide-angle field is especially easy to contaminate once tri-focal products and accessories are mixed in:

- `Elmarit-M 21`
- `Super-Elmar-M 21`
- `Super-Angulon 21`
- `Summilux-M 21`
- `Tri-Elmar-M 16-18-21` / `WATE`
- `Tri-Elmar-M 28-35-50` / `MATE`
- `Elmarit-R 21`
- `SL` / non-M wide-angle lines
- external viewfinders / `Frankenfinder` / hood / case / box bundles

For canonical purposes, `Tri-Elmar 16-18-21` needs to stay lens-first and M-only.

The round-1 question is whether this is:

1. a broad single-line family, or
2. a family with a visible finder-bundle or naming split that should already become `hold`

Round-1 answer: it is best treated as a clean single-line family, while keeping shorthand and bundle signals below row level.

## Literature / Reference Base

### Source A: Leica Camera official product page

Leica's current product page consistently names the lens as:

- `Tri-Elmar-M 16-18-21 f/4 ASPH.`

It is presented as one Leica M product line with:

- three focal lengths: `16 / 18 / 21`
- fixed maximum aperture `f/4`
- `ASPH`
- close focus to `0.33m`
- floating element construction

Reference:

- [Leica Camera - Tri-Elmar-M 16-18-21 f/4 ASPH.](https://leica-camera.com/en-int/photography/lenses/m/tri-elmar-m-16-18-21mm-f4-asph-black)

### Source B: Leica Wiki

Leica Wiki documents the same line as:

- `16mm-18mm-21mm f/4 ASPH Tri-Elmar-M`

and explicitly notes that it is:

- also known as `WATE`
- produced from `2006-current`
- Leica M mount with `6 bit` identification
- `10 / 7` optical design

Reference:

- [Leica Wiki - 16mm-18mm-21mm f/4 ASPH Tri-Elmar-M](https://wiki.l-camera-forum.com/leica-wiki.en/index.php/16mm-18mm-21mm_f/4_ASPH_Tri-Elmar-M)

### Source C: Leica technical data PDF

Leica technical data also uses:

- `LEICA TRI-ELMAR-M 16-18-21 mm f/4 ASPH.`

and describes the lens as one ultra-wide-angle Leica M design that can be bought together with the Universal Wide-Angle Viewfinder M.

Reference:

- [Leica technical data PDF](https://leica-camera.com/sites/default/files/pm-56130-Tri-Elmar-M16-18-21-TechnicalData.pdf)

### Source D: Universal Wide-Angle Viewfinder M

Leica's viewfinder page explicitly states that the finder is used with:

- `Leica Tri-Elmar-M 16-18-21 mm f/4 ASPH.`

This matters because it confirms that finder bundling is an accessory workflow around the same lens line, not a separate lens line.

Reference:

- [Leica Universal Wide-Angle Viewfinder M](https://leica-camera.com/en-AT/photography/accessories/viewfinders/universal-wide-angle-viewfinder-m)

### Interpretation

The literature stack is clean:

1. `Tri-Elmar-M 16-18-21mm f/4 ASPH` is the stable official line name
2. `WATE` is real shorthand, but not a distinct literature-backed product line
3. the finder relationship is explicit, but it is accessory / bundle context, not a lens split

That supports a narrow single-core recommendation.

## Local Listing Evidence

Analysis base: `data/normalized/normalized_latest.json`

After excluding obvious contamination from:

- `Tri-Elmar 28-35-50` / `MATE`
- `Elmarit 21`
- `Super-Elmar 21`
- `Super-Angulon 21`
- `Summilux 21`
- `R 21`
- `SL` / non-M wide lines
- third-party `21mm` lenses

the local `Tri-Elmar 16-18-21` / `WATE` pool becomes:

- raw WATE-like local pool: `16`
- clean no-bundle local pool: `14`
- unique title strings: `11`

The difference between `16` and `14` is meaningful:

- `2` listings explicitly include `finder` in the title
- those are bundle-inflated listings, not evidence of a separate lens line

### Broad price clustering

KRW-parsed local medians for the clean no-bundle subset:

| Bucket | Count | KRW-priced | Median KRW | Audit note |
| --- | ---: | ---: | ---: | --- |
| broad `Tri-Elmar-M 16-18-21mm f/4 ASPH` clean pool | 14 | 2 | ~5.15M KRW | line title is stable, but KRW sample is thin |

Observed KRW spread in the clean no-bundle subset:

- min priced example: ~`4.80M KRW`
- median: ~`5.15M KRW`
- max priced example: ~`5.50M KRW`

### Local title patterns

Broad recurring titles:

- `Leica M 16-18-21mm f4 Tri-elmar ASPH 6bit Black`
- `[중고] M 16-18-21/4 Tri Elmar ASPH 6bit`
- `[위탁] M 16-18-21/4 Tri Elmar ASPH 6bit`
- `[중고] M 16-18-21/4 Tri Elmar ASPH 6bit (Black)`
- `LEICA 16-18-21mm F4 ASPH TRI-ELMAR-M sn.4055`
- `LEICA 16-18-21mm F4 ASPH TRI-ELMAR-M sn.4182`

Bundle-inflated titles:

- `Leica M 16-18-21mm f4 Tri-elmar ASPH 6bit Black + Finder set`
- `LEICA 16-18-21mm F4 ASPH + finder TRI-ELMAR-M sn.4070`

### Local marker frequency

Repeated local modifiers in the raw WATE-like pool:

- `6bit`: `3`
- `black`: `2`
- `finder`: `2`

Sparse or effectively absent modifiers:

- `silver`
- `hood`
- `boxed`
- `case`
- `country`
- `germany`
- `canada`
- explicit `WATE` wording
- explicit `wide angle tri-elmar` wording

### Interpretation

The local pool supports one strong conclusion:

1. the main lens title language converges on `16-18-21 / f4 / Tri-Elmar-M`
2. explicit `WATE` shorthand is not actually carrying the local pool
3. finder-related wording appears, but as bundle metadata rather than a stable separate market line

The price sample is thinner than ideal, but not contradictory.  
Round-1 can still support a conservative first-pass `core` because the product name and local title convergence are unusually tight.

## Candidate Entity Expansion

## Candidate 1: `Leica Tri-Elmar-M 16-18-21mm f/4 ASPH`

### Official / literature basis

Strong.

This is the broad Leica M line consistently supported by Leica literature and local title language.

### Mechanical distinction

Strong enough for `core`.

It has:

- explicit `Tri-Elmar-M` naming
- explicit `16-18-21`
- explicit `f/4`
- explicit `ASPH`
- stable Leica M ultra-wide tri-focal mechanical identity

### Optical distinction

Strong enough for `core`.

This is not a variant of `Elmarit 21`, `Super-Elmar 21`, `Super-Angulon 21`, or `MATE`. It is its own Leica M optical line.

### Market split potential

Moderately strong.

The local price sample is thin, but the title convergence is very strong and the priced examples do not show contradictory clustering.

### Search-intent split potential

Strong.

Queries like:

- `tri-elmar 16-18-21`
- `16-18-21 tri-elmar`
- `tri-elmar-m 16-18-21`
- `m 16-18-21/4`

all point to the same lens line.

### Final decision

`core`

### One-line reason

`Tri-Elmar-M 16-18-21mm f/4 ASPH` is a literature-real and locally convergent Leica M line, and the visible variation around it is mostly bundle metadata rather than a true internal split.

## Candidate 2: `WATE`

### Official / literature basis

Real shorthand, but not a separate official line.

### Mechanical distinction

None by itself.

### Optical distinction

None by itself.

### Market split potential

Weak.

Current local titles do not rely on `WATE` wording; they overwhelmingly use the full `Tri-Elmar-M 16-18-21` language.

### Search-intent split potential

Plausible in enthusiast shorthand, but weak in current local evidence.

### Final decision

`보류`

### One-line reason

`WATE` is a real collector / user shorthand, but current local title support is too thin to let it shape a separate row or a strong round-1 alias by itself.

## Candidate 3: finder / Frankenfinder / finder set bundle

### Official / literature basis

Real accessory relationship, but not a separate lens line.

### Mechanical distinction

Not enough for standalone canonical status.

### Optical distinction

None.

### Market split potential

Visible, but bundle-driven.

The local pool clearly shows `finder set` titles, but they describe a package around the same lens, not a new canonical lens entity.

### Search-intent split potential

Moderate as metadata, weak as canonical entity.

### Final decision

`overlay`

### One-line reason

finder / `Frankenfinder` inclusion matters operationally and for pricing, but it behaves as bundle metadata rather than a standalone seeded lens row.

## Candidate 4: `tri-elmar 21` / single-focal-length shorthand

### Official / literature basis

Weak as a canonical row signal.

### Mechanical distinction

None by itself.

### Optical distinction

None by itself.

### Market split potential

Weak.

This wording risks being confused with other `21mm` Leica families because `21` is only one position within the tri-focal line.

### Search-intent split potential

Potentially ambiguous.

It can refer to the WATE family, but it is also structurally close to searches for single-focal-length `21mm` lenses.

### Final decision

`보류`

### One-line reason

`tri-elmar 21` is too ambiguous in round-1 because it can blur with other `21mm` Leica families rather than cleanly identify the WATE lens.

## Overlay / Boundary Notes

### Overlay

Keep these below row level:

- `6bit`
- `black / silver`
- `country marking`
- `finder included`
- `Frankenfinder included`
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

### Out-of-family boundary

Keep these outside `Tri-Elmar 16-18-21`:

- `Elmarit 21`
- `Super-Elmar 21`
- `Super-Angulon 21`
- `Summilux 21`
- `Elmarit 24`
- `Elmar-M 24`
- `Summilux 24`
- `Tri-Elmar 28-35-50` / `MATE`
- `R 21`
- `SL / L-mount` wide lenses
- accessories and finder-only listings
- third-party wide lenses

## Final Round-1 Recommendation

- immediate core candidate:
  - `Leica Tri-Elmar-M 16-18-21mm f/4 ASPH`
- hold candidate:
  - none recommended in round-1
- overlay:
  - `6bit`, finish, country, finder / `Frankenfinder` / hood / box / case bundle metadata, and packaging
- out-of-family:
  - `Elmarit 21`, `Super-Elmar 21`, `Super-Angulon 21`, `Summilux 21`, `MATE`, `R`, `SL`, accessories, and third-party wide lenses

## Seed Readiness

Round-1 conclusion: `yes`, this family is ready for a narrow seed round.

If a follow-up seed round is opened, the conservative first move should be:

1. add exactly one `core` row:
   - `Leica Tri-Elmar-M 16-18-21mm f/4 ASPH`
2. keep `WATE`, finder bundle, hood bundle, and boxed completeness below row level
3. do not open a separate shorthand-driven row unless later local evidence shows that `WATE` itself is operationally stable in titles
