# Super-Elmar 18 Taxonomy Audit - Round 1

Date: 2026-05-10

Scope: read-heavy taxonomy audit for the Leica `Super-Elmar 18` family. This round does not add seed rows, does not change classifier/query/search behavior, and does not change admin lookup ranking or UI. The goal is to determine whether `Leica Super-Elmar-M 18mm f/3.8 ASPH` is mature enough for explicit canonical seeding and, if so, at what granularity.

## Executive Summary

`Super-Elmar 18` is seedable, and round-1 should keep it as a narrow single-line Leica M family.

The strongest first-pass recommendation is:

1. `Leica Super-Elmar-M 18mm f/3.8 ASPH`

Round-1 conclusion:

- immediate recommended `core` candidate count: `1`
- recommended first-pass core:
  - `Leica Super-Elmar-M 18mm f/3.8 ASPH`
- explicit `hold` candidate:
  - none recommended in round-1
- `6bit`, `black / silver`, `country marking`, `finder included`, `hood included`, `boxed`, `case included`, and `packaging` stay `overlay`
- `18 elmar` / `elmar 18` are too broad and should stay `deferred shorthand`
- `Tri-Elmar 16-18-21` / `WATE`, `Super-Elmar 21`, `Elmarit 21`, `Super-Angulon 21`, `Summilux 21`, `24mm` families, `R`, `SL`, accessories, and third-party wide lenses remain out-of-family boundaries

Why this is a single-line family:

- literature documents one stable Leica M line
- local title language converges strongly on one exact `18mm / f3.8 / Super-Elmar-M` product
- visible listing variation is mostly metadata such as `6bit` and `black`, not a real internal lens split

## Family Overview

The Leica ultra-wide field around `18mm` is especially easy to contaminate:

- `Super-Elmar-M 18`
- `Tri-Elmar-M 16-18-21` / `WATE`
- `Super-Elmar-M 21`
- `Elmarit-M 21`
- `Super-Angulon 21`
- `Summilux-M 21`
- `Elmarit-M 24`
- `Elmar-M 24`
- `Summilux-M 24`
- `R` / `SL` / non-M wide-angle lines
- finder / hood / cap / case / box accessory listings

For canonical purposes, `Super-Elmar 18` needs to stay lens-first and M-only.

The round-1 question is whether this is:

1. a broad single-line family, or
2. a family with a visible internal split worth seeding now

Round-1 answer: it is best treated as a clean single-line family.

## Literature / Reference Base

### Source A: Leica Camera product page

Leica's current product page consistently names the lens as:

- `Super-Elmar-M 18 f/3.8 ASPH.`

It presents the lens as one modern Leica M product line with:

- `18mm` focal length
- `f/3.8`
- `ASPH`
- Leica M bayonet
- compact integrated Leica-wide design

References:

- [Leica Camera - Super-Elmar-M 18 f/3.8 ASPH.](https://leica-camera.com/en-GB/photography/lenses/m/super-elmar-m-18mm-f3-8-asph-black?artnr=11649)
- [Leica technical data PDF](https://leica-camera.com/sites/default/files/pm-56073-Super-Elmar-M18-TechnicalData.pdf?srsltid=AfmBOoo1Zf9R1SYHRZ440l8BslzZOE_Zrte46kJ98XSMtkrTex69hlVG)

### Source B: Leica Wiki

Leica Wiki documents the same line as:

- `18mm f/3.8 ASPH Super-Elmar-M`

and explicitly notes:

- production era `2009-`
- Leica M bayonet with `6 bit` identification
- accessory compatibility with dedicated viewfinders and hood options

Reference:

- [Leica Wiki - 18mm f/3.8 ASPH Super-Elmar-M](https://wiki.l-camera-forum.com/leica-wiki.en/index.php/18mm_f/3.8_ASPH_Super-Elmar-M)

### Interpretation

The literature stack is clean:

1. `Super-Elmar-M 18mm f/3.8 ASPH` is the stable official line name
2. no meaningful literature-backed generation split surfaced in round-1
3. finder / hood are accessory workflow context, not a separate lens line

That supports a narrow single-core recommendation.

## Local Listing Evidence

Analysis base: `data/normalized/normalized_latest.json`

Broad local retrieval on `super-elmar 18` also pulls some nearby `Super-Elmar 21` noise. After excluding obvious contamination from:

- `Tri-Elmar 16-18-21` / `WATE`
- `Super-Elmar 21`
- `Elmarit 21`
- `Super-Angulon 21`
- `Summilux 21`
- `24mm` Leica M families
- obvious accessory-only listings

the useful local `Super-Elmar 18` pool becomes:

- raw local pool: `15`
- clean local pool: `12`
- unique title strings: `7`

### Broad price clustering

KRW-parsed local medians:

| Bucket | Count | KRW-priced | Median KRW | Audit note |
| --- | ---: | ---: | ---: | --- |
| broad `Super-Elmar-M 18mm f/3.8 ASPH` clean pool | 12 | 4 | ~3.19M KRW | stable single-line cluster |

Observed price range in KRW-priced subset:

- min priced example: ~`2.50M KRW`
- median: ~`3.19M KRW`
- max priced example: ~`3.28M KRW`

### Local title patterns

Representative local titles:

- `[중고] M 18/3.8 Super Elmar ASPH 6bit (Black)`
- `[위탁] M 18/3.8 Super Elmar ASPH 6bit (Black)`
- `LEICA 18mm F3.8 ASPH SUPER-ELMAR-M sn.4084`
- `LEICA 18mm F3.8 ASPH SUPER-ELMAR-M sn.4209`
- `LEICA 18mm F3.8 ASPH SUPER-ELMAR-M sn.4258`

### Local marker frequency

Repeated local modifiers:

- `super-elmar-m`: `9`
- `6bit`: `3`
- `black`: `3`

Not meaningfully present in the clean local pool:

- `silver`
- `finder`
- `hood`
- `boxed`
- `case`
- `germany`
- `canada`

### Interpretation

This family is cleaner than many neighboring wide-angle Leica lines:

1. title language converges on one modern `18mm f/3.8 ASPH Super-Elmar-M` line
2. local pricing forms one usable cluster
3. repeated modifiers look like metadata, not separate line names

The family does not currently show a strong internal split that would justify multiple round-1 canonical rows.

## Candidate Entity Expansion

## Candidate 1: `Leica Super-Elmar-M 18mm f/3.8 ASPH`

### Official / literature basis

Strong.

Leica literature and Leica Wiki both treat this as a distinct modern Leica M product line.

### Mechanical distinction

Strong enough for `core`.

It has:

- explicit `Super-Elmar-M` naming
- explicit `18mm`
- explicit `f/3.8`
- `ASPH`
- stable modern Leica M ultra-wide identity

### Optical distinction

Strong enough for `core`.

This is not a variant of `Tri-Elmar 16-18-21`, `Super-Elmar 21`, `Elmarit 21`, or `Summilux 21`. It is its own Leica M optical line.

### Market split potential

Good.

The local priced subset forms a coherent cluster around roughly `3.19M KRW`.

### Search-intent split potential

Strong.

Dealers and users explicitly write:

- `Super-Elmar 18`
- `Super-Elmar-M 18`
- `18/3.8 Super Elmar ASPH`

### Final decision

`core`

### One-line reason

`Super-Elmar-M 18mm f/3.8 ASPH` is a distinct, clean modern Leica M line with stable title language and no strong round-1 internal split signal.

## Candidate 2: `6bit`

### Official / literature basis

Real feature, but not a separate line.

### Mechanical distinction

Visible but not enough for standalone canonical status.

### Optical distinction

None.

### Market split potential

Weak as a separate row.

### Final decision

`overlay`

### One-line reason

`6bit` appears as expected metadata on the same main `Super-Elmar-M 18` line rather than as a separate market entity.

## Candidate 3: finder / hood / boxed bundle axis

### Official / literature basis

Accessory-real, not line-real.

### Mechanical distinction

Weak as canonical split.

### Market split potential

Too thin in current local data.

### Final decision

`overlay`

### One-line reason

finder / hood / bundle signals are structurally relevant for wide-angle Leica sales, but current local evidence does not justify a separate row.

## Candidate 4: `18 elmar` / `elmar 18`

### Official / literature basis

Weak as family identifier.

### Local title support

Unsafe.

Broad retrieval on `18 elmar` or `elmar 18` pulls:

- `Tri-Elmar 16-18-21`
- `R 180`
- `TL 18-56 Vario-Elmar`
- other non-target Elmar / Elmarit strings

### Final decision

`deferred shorthand`

### One-line reason

`18 elmar` is much too broad to be a safe round-1 alias for `Super-Elmar-M 18`.

## Contamination Review

### WATE / Tri-Elmar 16-18-21 contamination

This boundary is critical.

The `Tri-Elmar 16-18-21` / `WATE` family is real and already separate. Any `16-18-21` title must stay outside `Super-Elmar 18`.

Boundary examples:

- `tri-elmar 16-18-21`
- `wate`
- `wide angle tri-elmar`

### 21mm family contamination

The neighboring `21mm` field is dense and must remain separate:

- `Super-Elmar 21`
- `Elmarit 21`
- `Super-Angulon 21`
- `Summilux 21`

### 24mm family contamination

The `24mm` field also remains outside:

- `Elmarit 24`
- `Elmar-M 24`
- `Summilux 24`

### Accessory contamination

Finder-only and hood-only queries must stay outside:

- `finder super-elmar 18`
- `hood super-elmar 18`
- `cap super-elmar 18`

## Core / Hold / Overlay / Deferred / Boundary

### Core candidate

Immediate round-1 `core` candidate:

- `Leica Super-Elmar-M 18mm f/3.8 ASPH`

### Hold candidate

None recommended in round-1.

### Overlay

Keep below row level:

- `6bit`
- `black / silver`
- `country marking`
- `finder included`
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

### Deferred / 보류

- `18 elmar`
- `elmar 18`
- finder / hood / box driven bundle interpretation

### Out-of-family boundary

- `Tri-Elmar 16-18-21` / `WATE`
- `Super-Elmar 21`
- `Elmarit 21`
- `Super-Angulon 21`
- `Summilux 21`
- `Elmarit 24`
- `Elmar-M 24`
- `Summilux 24`
- `R mount`
- `SL / L mount`
- accessory-only listings
- third-party wide lenses

## Final Recommendation

### immediate core candidate

`1`

- `Leica Super-Elmar-M 18mm f/3.8 ASPH`

### hold candidate

None in round-1.

### overlay

- `6bit`
- `finish`
- `country marking`
- `finder / hood / cap / boxed / case / packaging`

### out-of-family

- `Tri-Elmar 16-18-21 / WATE`
- Leica `21mm / 24mm` families
- `R`
- `SL`
- accessories
- third-party lenses

### next-round seedability

Yes.

The next conservative seed round should add exactly one row:

- `Leica Super-Elmar-M 18mm f/3.8 ASPH`

and should keep:

- `18 elmar`
- `elmar 18`

out of the initial strong alias set.
