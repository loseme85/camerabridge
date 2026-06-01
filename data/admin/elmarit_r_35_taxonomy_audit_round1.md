# Elmarit-R 35 Taxonomy Audit - Round 1

Date: 2026-05-11

Scope: audit-only review for the Leica `Elmarit-R 35` family. This round does not add seed rows, does not modify `entities/*.json`, does not modify `canonical_entities_index.json`, and does not change classifier/query/search behavior, ranking, or UI.

## Executive Summary

`Elmarit-R 35` is literature-real, but round-1 local support is too thin to open as a seed family yet.

Round-1 conclusion:

- immediate recommended `core` candidate count: `0`
- recommended first-pass core:
  - none
- strongest deferred candidate:
  - `Leica Elmarit-R 35mm f/2.8`
- explicit `hold` candidate:
  - none
- `I / II / III`, `ROM`, `cam`, and filter-thread markers are literature-real
- but the local title pool is too thin even for the broad family, so internal splits are well below seed threshold

The safest round-1 answer is:

1. keep `Elmarit-R 35` closed for now
2. do not open any `core` or `hold` row
3. treat broad `elmarit 35` wording as too contaminated to support canonical seeding

## Literature / Reference Base

### Source A: Leica Wiki - `35mm f/2.8 Elmarit-R I`

Leica Wiki documents `35mm f/2.8 Elmarit-R I` as a real early family version with:

- production era `1964-1973`
- variants:
  - `1-cam`
  - `2-cam`
  - `3-cam`
  - black and chrome versions
- filter type:
  - `Series 6 + 14160`

Reference:

- [Leica Wiki - 35mm f/2.8 Elmarit-R I](https://wiki.l-camera-forum.com/leica-wiki.en/index.php?title=35mm_f%2F2.8_Elmarit-R_I)

### Source B: Leica Wiki - `35mm f/2.8 Elmarit-R II`

Leica Wiki documents `35mm f/2.8 Elmarit-R II` as a real second family version with:

- production era `1973-1979`
- variants:
  - `2-cam`
  - `3-cam`
- filter type:
  - `Series VII`

Reference:

- [Leica Wiki - 35mm f/2.8 Elmarit-R II](https://wiki.l-camera-forum.com/leica-wiki.en/index.php?title=35mm_f%2F2.8_Elmarit-R_II)

### Source C: Leica Wiki - `35mm f/2.8 Elmarit-R III`

Leica Wiki documents `35mm f/2.8 Elmarit-R III` as a real later family version with:

- production era `1979-1996`
- variants:
  - `3-cam`
  - `R-only`
- filter type:
  - `E55`
- built-in hood

Reference:

- [Leica Wiki - 35mm f/2.8 Elmarit-R III](https://wiki.l-camera-forum.com/leica-wiki.en/index.php/35mm_f/2.8_Elmarit-R_III)

### Source D: Leica Classic - R-System page

Leica Classic presents the family under `Elmarit-R 2,8/35mm` and explicitly groups:

- `1. + 2. Model 11101/11201`
- `3rd Model 11231/11251`

Reference:

- [Leica Classic - Elmarit-R 2,8/35mm](https://classic.leica-camera.com/en/Leica-Systems/R-System/Lenses/Wideangle-Lenses/Elmarit-R-2-8-35mm/)

## Taxonomy Implication from Literature

Literature clearly supports:

- one real broad family:
  - `Leica Elmarit-R 35mm f/2.8`

and also clearly supports internal variants:

- `Elmarit-R I`
- `Elmarit-R II`
- `Elmarit-R III`
- `1-cam / 2-cam / 3-cam / R-only`
- `Series 6`
- `Series VII`
- `E55`

But round-1 must still be grounded in local title behavior. Here, literature is strong but market support is weak.

## Boundary Check

This family must remain separate from:

- `Leica Summicron-R 35mm f/2`
- `Leica Summilux-R 35mm f/1.4`
- `Leica Summicron-M 35`
- `Leica Summilux-M 35`
- `Leica Summaron 35`
- M-side `Elmarit 35` hypothesis
- `Elmarit-R 28`
- `Elmarit-R 50`
- `SL / L-mount 35mm` lenses
- third-party `35mm` lenses
- hood-only / cap / case / accessory-only listings

## Local Listing Evidence

Analysis base:

- `data/normalized/normalized_latest.json`

### Broad retrieval behavior

Broad `elmarit 35` retrieval is not usable as a family signal.

Observed contamination includes:

- `135mm Elmarit-R`
- `135mm Elmarit-M`
- `28mm Elmarit-M`
- `21mm Elmarit-M`
- `19mm Elmarit-R`
- macro / tele R Elmarit lines
- hood compatibility listings

Examples:

- `[위탁] M135/2.8 Elmarit (Black)`
- `LEICA 28mm F2.8 ELMARIT-M sn.3558`
- `LEICA 19mm F2.8 ELMARIT-R sn.3504`
- `신품 호환 Leica 14043 Hood Cover for M 35mm f2 Summicron, M 28mm f2.8 Elmarit`

This means `elmarit 35` must not be treated as a strong row-shaping alias for R-side normalization.

### Clean local R-side pool

After restricting to explicit `35mm` and `Elmarit-R` wording, the usable local pool becomes:

- clean local pool: `1`
- unique titles: `1`
- KRW-priced count: `1`
- KRW median: `1,200,000`

Observed title:

- `LEICA R6.2 35mm F2.8 ELMARIT-R sn.1923`

### Marker distribution inside local pool

Round-1 local support for internal split markers is effectively absent:

- `ROM`: `0`
- `1-cam / 2-cam / 3-cam`: `0`
- `E55 / E48 / Series VII`: `0`
- `hood / case / boxed`: `0`

Interpretation:

- literature supports meaningful internal structure
- local seller-title support is too thin even for the broad family
- therefore internal variant rows are clearly out of scope for now

## Smoke Query Review

### Explicit R-side queries

Direct local evidence is very thin.

Usable explicit hit pattern:

- `35mm f2.8 elmarit-r`

Weak or absent direct repetition:

- `elmarit-r 35`
- `elmarit r 35`
- `r 35 elmarit`
- `35 elmarit-r`
- `35mm f/2.8 elmarit-r`
- `r 35/2.8 elmarit`
- `leica r 35mm f2.8`
- `elmarit 35 r`

Interpretation:

- one clean hit proves the family exists in local market data
- but the title surface is too thin and unstable for round-1 seed activation

### Broad shorthand risk

Unsafe broad shorthand:

- `elmarit 35`

Why unsafe:

- heavily contaminated by non-35 Elmarit titles
- easily overlaps with M-side and R-side non-target families
- too little explicit R-side support to stabilize it

## Candidate Review

## Candidate 1: `Leica Elmarit-R 35mm f/2.8`

### Literature basis

Strong.

Both Leica Wiki and Leica Classic support a real R-side `35mm f/2.8 Elmarit-R` family.

### Local title support

Too thin for round-1 seed activation.

The clean local pool contains only one usable title.

### Price behavior

Insufficient.

A single KRW-priced example cannot establish stable family-level market behavior.

### Search-intent stability

Not strong enough yet.

The explicit query surface is too sparse, and broad shorthand is highly contaminated.

### Final decision

`deferred`

### One-line reason

`Leica Elmarit-R 35mm f/2.8` is literature-real but currently under-supported in local title evidence for seed activation.

## Candidate 2: `Elmarit-R I / II / III`

### Literature basis

Strong.

These are real internal family versions.

### Local title support

Absent.

The current local pool does not repeat `I / II / III` wording directly.

### Final decision

`deferred`

### One-line reason

Internal version structure is real, but local titles do not support version-level seeding.

## Candidate 3: `ROM / cam / filter-thread` rows

### Literature basis

Real markers exist.

### Local title support

Absent in the clean pool.

### Final decision

`deferred`

### One-line reason

These remain metadata only until local title support becomes materially stronger.

## Overlay Elements

Keep as `overlay` if the family is revisited later:

- `ROM`
- `1-cam / 2-cam / 3-cam`
- `E55 / E48 / Series 6 / Series VII`
- `filter thread`
- `black / finish`
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

## Deferred / Hold / Not-for-Round-1

### No round-1 hold candidate

There is no clear explicit `hold` row at this stage.

### Deferred internal split

Do not open separate rows yet for:

- `Leica Elmarit-R 35mm f/2.8 I`
- `Leica Elmarit-R 35mm f/2.8 II`
- `Leica Elmarit-R 35mm f/2.8 III`
- `Leica Elmarit-R 35mm f/2.8 ROM`
- `Leica Elmarit-R 35mm f/2.8 3-cam`
- `Leica Elmarit-R 35mm f/2.8 E55`

### Deferred shorthand

Do not use as strong initial aliases:

- `elmarit 35`

Reason:

- too much M/R/SL/accessory contamination

## Out-of-Family Boundary

Must remain outside this family:

- `Leica Summicron-R 35mm f/2`
- `Leica Summilux-R 35mm f/1.4`
- `Leica Summicron-M 35`
- `Leica Summilux-M 35`
- `Leica Summaron 35`
- M-side `Elmarit 35` hypothesis
- `Elmarit-R 28`
- `Elmarit-R 50`
- `APO-Summicron-SL 35`
- third-party `35mm` lenses
- accessory-only listings

## Final Round-1 Judgment

- immediate core candidate:
  - `seed 보류`
- hold candidate:
  - none
- overlay:
  - `ROM`, `cam markers`, `E55 / E48 / Series` markers, finish, country, hood/cap/box/case/packaging
- out-of-family:
  - Leica M `35mm` families, `Summicron-R 35`, `Summilux-R 35`, other R families, `SL/L`, accessories, third-party

## Recommendation for Next Round

Do not open a seed row yet.

If future local evidence improves, revisit only this narrow candidate:

- `Leica Elmarit-R 35mm f/2.8`

But until multiple clean local titles appear, the family should remain closed.
