# Summicron-R 35 Taxonomy Audit - Round 1

Date: 2026-05-11

Scope: audit-only review for the Leica `Summicron-R 35` family. This round does not add seed rows, does not modify `entities/*.json`, does not modify `canonical_entities_index.json`, and does not change classifier/query/search behavior, ranking, or UI.

## Executive Summary

`Summicron-R 35` is literature-real, but round-1 local support is still too thin to open as a seed family yet.

Round-1 conclusion:

- immediate recommended `core` candidate count: `0`
- recommended first-pass core:
  - none
- strongest deferred candidate:
  - `Leica Summicron-R 35mm f/2`
- explicit `hold` candidate:
  - none
- `I / II`, `ROM`, `cam`, and filter-thread markers are literature-real
- but the local title pool is too thin even for the broad family, so internal splits are well below seed threshold

The safest round-1 answer is:

1. keep `Summicron-R 35` closed for now
2. do not open any `core` or `hold` row
3. treat broad `summicron 35` wording as too contaminated to support canonical seeding

## Literature / Reference Base

### Source A: Leica Classic - `Summicron-R 2/35mm`

Leica Classic presents the family under `Summicron-R 2/35mm` and explicitly groups:

- `1st Model 11227`
- `2nd Model 11115/11339`

This is strong evidence that Leica treats `Summicron-R 35mm f/2` as a real broad R-side family with internal historical versions rather than unrelated separate lines.

Reference:

- [Leica Classic - Summicron-R 2/35mm](https://classic.leica-camera.com/en/Leica-Systems/R-System/Lenses/Wideangle-Lenses/Summicron-R-2-35mm/)

### Source B: Leica Wiki - `35mm f/2 Summicron-R I`

Leica Wiki documents `35mm f/2 Summicron-R I` as a real early family version with:

- production era `1972-1976`
- variants:
  - `2-cam`
  - `3-cam`
- filter type:
  - `Series 7`

Reference:

- [Leica Wiki - 35mm f/2 Summicron-R I](https://wiki.l-camera-forum.com/leica-wiki.en/index.php/35mm_f/2_Summicron-R_I)

### Source C: Leica Wiki - `35mm f/2 Summicron-R II`

Leica Wiki documents `35mm f/2 Summicron-R II` as a real later family version with:

- production era `1977-2009`
- order numbers:
  - `11115`
  - `11339-ROM`
- lens mount:
  - Leica R-bayonet
- filter thread:
  - `E55`
- built-in telescopic hood

Reference:

- [Leica Wiki - 35mm f/2 Summicron-R II](https://wiki.l-camera-forum.com/leica-wiki.en/index.php/35mm_f/2_Summicron-R_II)

## Taxonomy Implication from Literature

Literature clearly supports:

- one real broad family:
  - `Leica Summicron-R 35mm f/2`

and also clearly supports internal variants:

- `Summicron-R I`
- `Summicron-R II`
- `2-cam / 3-cam`
- `ROM`
- `Series 7`
- `E55`

But round-1 must still be grounded in local title behavior. Here, literature is strong but local market support remains thin.

## Boundary Check

This family must remain separate from:

- `Leica Summilux-R 35mm f/1.4`
- `Leica Elmarit-R 35mm f/2.8`
- `Leica Summicron-M 35`
- `Leica Summilux-M 35`
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
- `data/normalized/normalized_latest.json`

### Broad retrieval behavior

Broad `summicron 35` retrieval is not usable as a family signal.

Observed contamination includes:

- `35mm Summicron-M`
- `35mm APO-Summicron`
- `35mm Summicron-SL`
- `50mm Summicron`
- accessory compatibility listings
- third-party `35mm` lenses

Examples:

- `Leica M 35mm f2 APO-Summicron ASPH 6bit Black`
- `Leica M 35mm f2 Summicron ASPH Anthracite Finish`
- `신품 Leica SL 35mm f2 Summicron ASPH Black`
- `신품 호환 Leica 14043 Hood Cover for M 35mm f2 Summicron, M 28mm f2.8 Elmarit`
- `Zeiss 35mm F2 ZM - Black`

This means `summicron 35` must not be treated as a strong row-shaping alias for R-side normalization.

### Clean local R-side pool

After restricting to explicit `35mm` plus explicit R-side `Summicron` wording, the usable local pool becomes:

- clean local pool: `3`
- unique titles: `2`
- KRW-priced count: `2`
- KRW median: `1,500,000`

Observed titles:

- `LEICA 35mm F2 SUMMICRON-R sn.3475`
- `[위탁] R 35/2 Summicron (Black)`

Interpretation:

- this is enough to confirm the family is not imaginary in local market data
- but it is still very thin compared with already-activated modern M or stronger R-side families

### Marker distribution inside local pool

Round-1 local support for internal split markers is effectively absent:

- `ROM`: `0`
- `1-cam / 2-cam / 3-cam`: `0`
- `E55 / E48 / Series 7`: `0`
- `hood / case / boxed`: `0`

Interpretation:

- literature supports meaningful internal structure
- local seller-title support is too thin even for the broad family
- therefore internal variant rows are clearly out of scope for now

## Smoke Query Review

### Explicit R-side queries

Direct local evidence is thin but real.

Usable explicit hit patterns:

- `35mm f2 summicron-r`
- `r 35/2 summicron`

Weak or absent direct repetition:

- `summicron-r 35`
- `summicron r 35`
- `r 35 summicron`
- `35 summicron-r`
- `35mm f/2 summicron-r`
- `leica r 35mm f2`
- `summicron 35 r`

Interpretation:

- clean explicit hits prove the family exists in local market data
- but title repetition is still too thin and unstable for round-1 seed activation

### Broad shorthand risk

Unsafe broad shorthand:

- `summicron 35`

Why unsafe:

- heavily contaminated by M-side `35mm Summicron`
- overlaps with `APO-Summicron-SL 35`
- can pull accessories and third-party `35mm` results
- too little explicit R-side support to stabilize it

## Candidate Review

## Candidate 1: `Leica Summicron-R 35mm f/2`

Pros:

- literature-real Leica R family
- Leica Classic and Leica Wiki both support the family cleanly
- local market does show explicit R-side titles

Cons:

- clean local pool is only `3` rows / `2` unique titles
- priced local support is only `2`
- broad shorthand `summicron 35` is badly contaminated
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
- `E55 / E48 / Series 7`
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

- `Summicron-R I`
- `Summicron-R II`
- `ROM`
- `2-cam / 3-cam`
- `Series 7`
- `E55`

Do not use as strong shaping aliases:

- `summicron 35`

Reason:

- these are either under-supported internal splits or broad shorthand with heavy contamination risk

## Out-of-Family Boundary

Must remain outside this family:

- `Leica Summilux-R 35mm f/1.4`
- `Leica Elmarit-R 35mm f/2.8`
- `Leica Summicron-M 35`
- `Leica Summilux-M 35`
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

- `Leica Summicron-R 35mm f/2`

Round-1 decision:

- `seed 보류`

Why:

1. literature clearly confirms a real Leica R family
2. local broad shorthand is too contaminated
3. explicit local R-side titles exist, but only at a very thin level
4. this is not yet strong enough for conservative seed activation

## Recommendation for Next Round

Do not add a seed row yet.

Only revisit if one of the following improves:

- multiple additional clean local `Summicron-R 35` titles appear
- more KRW-priced local rows accumulate
- R-side explicit wording becomes more stable than the current two-title pattern

If future evidence improves, the next candidate to open would still be:

- `Leica Summicron-R 35mm f/2`

But round-1 should keep the family closed.
