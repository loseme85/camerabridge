# Tri-Elmar 28-35-50 Taxonomy Audit - Round 1

Date: 2026-05-09

Scope: read-heavy taxonomy audit for the Leica `Tri-Elmar 28-35-50` / `MATE` family. This round does not add seed rows, does not change classifier/query/search behavior, and does not change admin lookup ranking or UI. The goal is to determine whether the Leica medium-angle tri-focal M lens is mature enough for explicit canonical seeding and, if so, at what granularity.

## Executive Summary

`Tri-Elmar 28-35-50` is seedable, and round-1 should keep it as a narrow single-line Leica M family.

The strongest first-pass recommendation is:

1. `Leica Tri-Elmar-M 28-35-50mm f/4 ASPH`

Round-1 conclusion:

- immediate recommended `core` candidate count: `1`
- recommended first-pass core:
  - `Leica Tri-Elmar-M 28-35-50mm f/4 ASPH`
- explicit `hold` candidate:
  - none recommended in round-1
- `E49`, `E55`, `6bit`, `black / silver`, `hood included`, `boxed`, and `case included` stay `overlay` or `보류`
- `MATE` is literature-real shorthand, but current local title support is too thin to let it shape a standalone row or strong alias by itself
- `tri-elmar 28`, `tri-elmar 35`, and `tri-elmar 50` are too ambiguous for round-1 alias use because they can bleed into prime-lens intent
- `Tri-Elmar 16-18-21` / `WATE`, Leica `28mm / 35mm / 50mm` primes, `R`, `SL`, accessories, and third-party lenses remain out-of-family boundaries

Why this is a single-line family:

- literature documents one stable Leica M line
- local title language converges on one exact `28-35-50 / f4 / Tri-Elmar-M` product
- visible listing variation is mostly version metadata, especially `E49` / `E55`, rather than a mature second row

## Family Overview

The Leica `28mm / 35mm / 50mm` field is especially easy to contaminate once multi-focal products and shorthand are mixed in:

- `Tri-Elmar-M 28-35-50` / `MATE`
- `Tri-Elmar-M 16-18-21` / `WATE`
- `Elmarit-M 28`
- `Summicron-M 28`
- `Summilux-M 28`
- `Summaron 28`
- `Summicron-M 35`
- `Summilux-M 35`
- `Summaron 35`
- `Summicron-M 50`
- `Summilux-M 50`
- `Noctilux-M 50`
- `R` / `SL` / non-M lines
- hood / cap / case / box accessory listings

For canonical purposes, `Tri-Elmar 28-35-50` needs to stay lens-first and M-only.

The round-1 question is whether this is:

1. a broad single-line family, or
2. a family that should already be split by version markers such as `E49` / `E55`

Round-1 answer: it is best treated as a clean single-line family, while keeping shorthand and version signals below row level for now.

## Literature / Reference Base

### Source A: Leica Camera Classic

Leica's classic product page consistently names the lens as:

- `Tri-Elmar-M 4/28-35-50mm ASPH.`

The page also explicitly lists:

- `1st Version 11890/11894`
- `2nd Version 11625`

Reference:

- [Leica Camera Classic - Tri-Elmar-M 4/28-35-50mm ASPH.](https://classic.leica-camera.com/en/Leica-Systems/M-System/Lenses/Wideangle-Lenses/Tri-Elmar-M-4-28-35-50mm-ASPH./)

### Source B: Leica Wiki

Leica Wiki documents the same line as:

- `28mm-35mm-50mm f/4 ASPH Tri-Elmar-M`

and explicitly notes:

- also known as `MATE` as in `Medium Angle Tri-Elmar`
- production era `1998-2007`
- variant structure around `E55` first version and `E49-A53` later versions
- inscription based on `LEICA TRI-ELMAR-M 1:4/28-35-50 ASPH.`

Reference:

- [Leica Wiki - 28mm-35mm-50mm f/4 ASPH Tri-Elmar-M](https://wiki.l-camera-forum.com/leica-wiki.en/index.php/28mm-35mm-50mm_f/4_ASPH_Tri-Elmar-M)

### Source C: Leica Camera Classic used listings

Leica Classic used pages repeatedly use:

- `Leica Tri-Elmar-M 28-35-50 MM F4 ASPH.`
- `Leica Tri-Elmar-M 4.0/28-35-50mm ASPH. 6Bit`

These pages are useful because they show Leica itself still treats `6Bit`, hood, and packaging as listing metadata around the same lens line rather than separate canonical products.

References:

- [Leica Classic used listing - Tri-Elmar-M 28-35-50 MM F4 ASPH.](https://classic.leica-camera.com/en/Leica-Tri-Elmar-M-28-35-50-MM-F4-ASPH./11890SH-3772281)
- [Leica Classic used listing - Tri-Elmar-M 4.0/28-35-50mm ASPH. 6Bit](https://classic.leica-camera.com/en/Leica-Tri-Elmar-M-4.0-28-35-50mm-ASPH.-6Bit/11625SH-3948154)

### Interpretation

The literature stack is clean:

1. `Tri-Elmar-M 28-35-50mm f/4 ASPH` is the stable official line name
2. `MATE` is real shorthand, but not a distinct literature-backed product line
3. `E55` and `E49` are real version markers, but literature still frames them as variants inside the same line

That supports a narrow single-core recommendation.

## Local Listing Evidence

Analysis base: `data/normalized/normalized_latest.json`

After excluding obvious contamination from:

- `Tri-Elmar 16-18-21` / `WATE`
- Leica `28mm / 35mm / 50mm` prime families
- `R` / `SL` / non-M lines
- obvious accessory-only listings

the local `Tri-Elmar 28-35-50` / `MATE` pool becomes:

- raw local pool: `14`
- clean local pool: `14`
- unique title strings: `9`

The pool is small but very coherent.

### Broad price clustering

KRW-parsed local medians for the clean subset:

| Bucket | Count | KRW-priced | Median KRW | Audit note |
| --- | ---: | ---: | ---: | --- |
| broad `Tri-Elmar-M 28-35-50mm f/4 ASPH` clean pool | 14 | 7 | ~5.20M KRW | line title is stable |
| explicit `E49` subgroup | 4 | 4 | ~5.53M KRW | looks stronger, but still small |
| explicit `E55` subgroup | 2 | 2 | ~4.34M KRW | visible but thin |

Observed KRW spread in the clean pool:

- min priced example: ~`2.70M KRW`
- median: ~`5.20M KRW`
- max priced example: ~`5.68M KRW`

### Local title patterns

Broad recurring titles:

- `Leica M 28-35-50mm f4 Tri-Elmar e49 신형 Black`
- `[중고] M 28-35-50/4 Tri Elmar E49 (Black)`
- `[중고] M 28-35-50/4 Tri Elmar E55 (Black)`
- `[위탁] M 28-35-50/4 Tri Elmar E55 (Black)`
- `LEICA 28-35-50mm F4 ASPH TRI-ELMAR-M sn.3753`
- `LEICA 28-35-50mm F4 ASPH TRI-ELMAR-M sn.3800`
- `Leica 28/35/50mm F4 Tri Elmar (11890)`

### Local marker frequency

Repeated local modifiers in the clean pool:

- `E49`: `4`
- `E55`: `2`
- `black`: `6`
- `신형`: `1`

Sparse or effectively absent modifiers:

- explicit `MATE` wording in title
- explicit `medium angle tri-elmar` wording
- explicit `6bit` wording
- `silver`
- `hood`
- `boxed`
- `case`
- `country`
- `germany`
- `canada`

### Interpretation

The local pool supports three strong conclusions:

1. the main lens title language converges on `28-35-50 / f4 / Tri-Elmar-M`
2. explicit `MATE` shorthand is not actually carrying the local pool
3. `E49` and `E55` are visible, but still look more like version metadata than a finished second-row taxonomy split

The price sample is better than some recent audits and points in the same direction: main family first, version split later if needed.

## Candidate Entity Expansion

## Candidate 1: `Leica Tri-Elmar-M 28-35-50mm f/4 ASPH`

### Official / literature basis

Strong.

This is the broad Leica M line consistently supported by Leica literature and local title language.

### Mechanical distinction

Strong enough for `core`.

It has:

- explicit `Tri-Elmar-M` naming
- explicit `28-35-50`
- explicit `f/4`
- `ASPH`
- stable Leica M tri-focal mechanical identity

### Local title support

Strong enough for `core`.

The local clean pool is thin but coherent, and the repeating titles are unmistakably about the same lens line.

### Price behavior

Good enough for `core`.

The broad pool clusters in one usable range. The `E49` and `E55` subgroups show some separation, but not enough yet to require separate rows.

### Risk

Manageable.

The main risks are shorthand contamination:

- `MATE`
- `tri-elmar 28`
- `tri-elmar 35`
- `tri-elmar 50`

These should not be used aggressively in round-1 aliasing.

### Round-1 recommendation

Recommend as immediate `core`.

## Candidate 2: `MATE` shorthand

### Official / literature basis

Real shorthand, but not a standalone line.

### Local title support

Weak.

Current local title evidence shows effectively no direct `MATE` wording.

### Risk

High.

`MATE` is broad, easy to misuse, and not locally reinforced enough for a strong seed alias.

### Round-1 recommendation

Do not use as a row or strong alias in round-1. Keep as `deferred shorthand`.

## Candidate 3: `E49` / `E55` version split

### Official / literature basis

Real.

Leica Wiki and Leica Classic both support multiple versions.

### Local title support

Visible, but still thin.

`E49` appears `4` times and `E55` appears `2` times in the clean pool.

### Price behavior

Suggestive, not decisive.

- `E49` median ~`5.53M KRW`
- `E55` median ~`4.34M KRW`

This may reflect real version spread, but the sample is still too small to justify immediate row split.

### Round-1 recommendation

Keep as `deferred internal split`, not `hold` yet.

## Contamination Review

### WATE / wide-angle Tri-Elmar contamination

This boundary is critical.

The `Tri-Elmar 16-18-21` / `WATE` family is real and already separate. Local title language makes the split easy whenever `16-18-21` appears.

Boundary examples:

- `tri-elmar 16-18-21`
- `wate`
- `wide angle tri-elmar`

These must stay outside `MATE`.

### Prime-lens contamination

The shorthand queries below are dangerous:

- `tri-elmar 28`
- `tri-elmar 35`
- `tri-elmar 50`

They can point at the multi-focal lens, but they can also collide conceptually with prime-lens shopping intent around `28`, `35`, and `50`.

These should remain below row level for now.

### Accessory contamination

The current local pool does not show strong hood/case-only contamination inside the clean subset, but the family is structurally exposed to it.

Accessory-only queries that must stay outside:

- `hood tri-elmar 28-35-50`
- `case tri-elmar 28-35-50`
- `cap tri-elmar 28-35-50`

## Core / Hold / Overlay / Deferred / Boundary

### Core candidate

Immediate round-1 `core` candidate:

- `Leica Tri-Elmar-M 28-35-50mm f/4 ASPH`

### Hold candidate

None recommended in round-1.

### Overlay

Keep below row level:

- `6bit`
- `black / silver`
- `country marking`
- `version / generation marker` when not row-stable
- `E49 / E55 / filter thread`
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

- `MATE` shorthand
- `medium angle tri-elmar`
- `tri-elmar 28`
- `tri-elmar 35`
- `tri-elmar 50`
- `E49` / `E55` version split

### Out-of-family boundary

- `Tri-Elmar 16-18-21` / `WATE`
- `Elmarit 28`
- `Summicron 28`
- `Summilux 28`
- `Summaron 28`
- `Summicron 35`
- `Summilux 35`
- `Summaron 35`
- `Summicron 50`
- `Summilux 50`
- `Noctilux 50`
- `R mount`
- `SL / L mount`
- accessory-only listings
- third-party lenses

## Final Recommendation

### immediate core candidate

`1`

- `Leica Tri-Elmar-M 28-35-50mm f/4 ASPH`

### hold candidate

None in round-1.

### overlay

- `6bit`
- `finish`
- `country marking`
- `version markers`
- `E49 / E55`
- `hood / cap / boxed / case / packaging`

### out-of-family

- `Tri-Elmar 16-18-21 / WATE`
- Leica `28mm / 35mm / 50mm` prime families
- `R`
- `SL`
- accessories
- third-party wide or standard lenses

### next-round seedability

Yes.

The next conservative seed round should add exactly one row:

- `Leica Tri-Elmar-M 28-35-50mm f/4 ASPH`

and should keep:

- `MATE`
- `medium angle tri-elmar`
- `tri-elmar 28 / 35 / 50`
- `E49 / E55`

out of the initial strong alias set.
