# Summilux-R 35 Taxonomy Audit - Round 1

Date: 2026-05-11

Scope: audit-only review for the Leica `Summilux-R 35` family. This round does not add seed rows, does not modify `entities/*.json`, does not modify `canonical_entities_index.json`, and does not change classifier/query/search behavior, ranking, or UI.

## Executive Summary

`Summilux-R 35` is literature-real, but round-1 local support is still too thin to open as a seed family yet.

Round-1 conclusion:

- immediate recommended `core` candidate count: `0`
- recommended first-pass core:
  - none
- strongest deferred candidate:
  - `Leica Summilux-R 35mm f/1.4`
- explicit `hold` candidate:
  - none
- `ROM`, `cam`, and filter-thread markers are literature-real
- but the local title pool is too thin even for the broad family, so internal splits are well below seed threshold

The safest round-1 answer is:

1. keep `Summilux-R 35` closed for now
2. do not open any `core` or `hold` row
3. treat broad `summilux 35` and `35 lux` wording as too contaminated to support canonical seeding

## Literature / Reference Base

### Source A: Leica Classic - `Summilux-R 1,4/35mm`

Leica Classic presents the family under `Summilux-R 1,4/35mm` and explicitly shows:

- `11143`
- `11144`

Classic-store examples also confirm real market wording such as:

- `3CAM`
- `ROM`
- `E67`

Reference:

- [Leica Classic - Summilux-R 1,4/35mm](https://classic.leica-camera.com/en/Leica-Systems/R-System/Lenses/Wideangle-Lenses/Summilux-R-1-4-35mm/)

### Source B: Leica Wiki - `35mm f/1.4 Summilux-R`

Leica Wiki documents `35mm f/1.4 Summilux-R` as a real family with:

- order numbers:
  - `11143`
  - `11144`
  - `11337-ROM`
- production era:
  - `1984-2009`
- lens mount:
  - Leica R-bayonet
- filter mount:
  - `E67`
- built-in telescopic hood

Reference:

- [Leica Wiki - 35mm f/1.4 Summilux-R](https://wiki.l-camera-forum.com/leica-wiki.en/index.php/35mm_f/1.4_Summilux-R)

## Taxonomy Implication from Literature

Literature clearly supports:

- one real broad family:
  - `Leica Summilux-R 35mm f/1.4`

and also clearly supports internal markers:

- `3CAM`
- `ROM`
- `E67`

But round-1 must still be grounded in local title behavior. Here, literature is strong but local market support remains thin.

## Boundary Check

This family must remain separate from:

- `Leica Summicron-R 35mm f/2`
- `Leica Elmarit-R 35mm f/2.8`
- `Leica Summilux-M 35`
- `Leica Summicron-M 35`
- `Leica Summaron 35`
- M-side `Elmarit 35` hypothesis
- `Elmarit-R 28`
- `Summicron-R 50`
- `Summilux-R 50`
- `SL / L-mount 35mm` lenses
- third-party `35mm` lenses
- hood-only / cap / case / accessory-only listings

## Local Listing Evidence

Analysis base:

- `data/raw/raw_*.json`

### Broad retrieval behavior

Broad `summilux 35` retrieval is not usable as an R-side family signal.

Observed contamination includes:

- `35mm Summilux-M`
- `35mm Summilux ASPH`
- third-party `35mm` lenses
- likely M-side shorthand such as `35 lux`

Examples:

- `[중고] Summilux-M 35mm f/1.4 ASPH (Black)`
- `[중고] Summilux-M 35mm f/1.4 ASPH (Silver)`
- `Used Leica Summilux-M 35mm f/1.4 ASPH FLE (11663), black`
- third-party `35mm` lens titles from `Voigtlander` and `Zeiss`

This means `summilux 35` and `35 lux` must not be treated as strong row-shaping aliases for R-side normalization.

### Clean local R-side pool

After restricting to explicit `35mm` plus explicit R-side `Summilux` wording, the usable local pool becomes:

- clean local pool: `3`
- unique titles: `2`
- KRW-priced count: `0`
- KRW median: `not available`

Observed titles:

- `LEICA 35mm F1.4 SUMMILUX-R sn.3272`
- `[위탁] R 35/1.4 Summilux (Black)`

Interpretation:

- this is enough to confirm the family is not imaginary in local market data
- but it is still very thin compared with already-activated modern M or stronger R-side families
- there is no stable KRW-priced support yet

### Marker distribution inside local pool

Round-1 local support for internal split markers is effectively absent:

- `ROM`: `0`
- `1-cam / 2-cam / 3-cam`: `0`
- `E67 / E60`: `0`
- `hood / case / boxed`: `0`

Interpretation:

- literature supports meaningful internal structure
- local seller-title support is too thin even for the broad family
- therefore internal variant rows are clearly out of scope for now

## Smoke Query Review

### Explicit R-side queries

Direct local evidence is thin but real.

Usable explicit hit patterns:

- `35mm f1.4 summilux-r`
- `r 35/1.4 summilux`

Weak or absent direct repetition:

- `summilux-r 35`
- `summilux r 35`
- `r 35 summilux`
- `35 summilux-r`
- `35mm f/1.4 summilux-r`
- `leica r 35mm f1.4`
- `summilux 35 r`
- `35 lux r`

Interpretation:

- clean explicit hits prove the family exists in local market data
- but title repetition is still too thin and unstable for round-1 seed activation

### Broad shorthand risk

Unsafe broad shorthand:

- `summilux 35`
- `35 lux`

Why unsafe:

- heavily contaminated by M-side `35mm Summilux`
- can overlap with SL-side and third-party `35mm` titles
- too little explicit R-side support to stabilize those shorthands

## Candidate Review

## Candidate 1: `Leica Summilux-R 35mm f/1.4`

Pros:

- literature-real Leica R family
- Leica Classic and Leica Wiki both support the family cleanly
- local market does show explicit R-side titles

Cons:

- clean local pool is only `3` rows / `2` unique titles
- priced local support is effectively absent
- broad shorthand `summilux 35` is badly contaminated
- no stable local support for internal markers

Round-1 verdict:

- `deferred`

Reason:

- this family is real, but the local evidence is not yet strong enough to justify an explicit seed row in a conservative first pass

## Hold Candidate Review

No explicit `hold` candidate is recommended in round-1.

Why:

- there is no narrower wording with stronger local repetition than the already-thin main family
- internal variants are literature-real but locally under-supported

## Overlay Elements

Keep these as overlay or deferred metadata only:

- `ROM`
- `1-cam / 2-cam / 3-cam`
- `E67 / E60`
- `filter thread`
- `finish`
- `country marking`
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

These should not become separate rows in round-1.

## Deferred / Not-for-Round-1

Do not open separate rows for:

- `ROM`
- `1-cam / 2-cam / 3-cam`
- `E67`

Do not use as strong shaping aliases:

- `summilux 35`
- `35 lux`

Reason:

- these are either under-supported internal markers or broad shorthand with heavy contamination risk

## Out-of-Family Boundary

Must remain outside this family:

- `Leica Summicron-R 35mm f/2`
- `Leica Elmarit-R 35mm f/2.8`
- `Leica Summilux-M 35`
- `Leica Summicron-M 35`
- `Leica Summaron 35`
- M-side `Elmarit 35` hypothesis
- `Elmarit-R 28`
- `Summicron-R 50`
- `Summilux-R 50`
- `APO-Summicron-SL 35`
- `SL / L-mount 35mm` lenses
- accessory-only listings
- third-party `35mm` lenses

## Final Round-1 Judgment

Immediate round-1 answer:

- immediate core candidate:
  - `0`
- hold candidate:
  - none

Strongest deferred candidate:

- `Leica Summilux-R 35mm f/1.4`

Round-1 decision:

- `seed 보류`

Why:

1. literature clearly confirms a real Leica R family
2. local broad shorthand is too contaminated
3. explicit local R-side titles exist, but only at a very thin level
4. there is no KRW-priced support strong enough to justify conservative seed activation

## Recommendation for Next Round

Do not add a seed row yet.

Only revisit if one of the following improves:

- multiple additional clean local `Summilux-R 35` titles appear
- KRW-priced local rows accumulate
- R-side explicit wording becomes more stable than the current two-title pattern

If future evidence improves, the next candidate to open would still be:

- `Leica Summilux-R 35mm f/1.4`

But round-1 should keep the family closed.
