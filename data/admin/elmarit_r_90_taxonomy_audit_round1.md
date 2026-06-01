# Elmarit-R 90 Taxonomy Audit - Round 1

Date: 2026-05-13

Scope: audit-only review for the Leica `Elmarit-R 90` family. This round does not add seed rows, does not modify `entities/*.json`, does not modify `canonical_entities_index.json`, and does not change classifier/query/search behavior, ranking, or UI.

## Executive Summary

`Elmarit-R 90` is literature-real, but round-1 local support is still too thin to open as a seed family yet.

Round-1 conclusion:

- immediate recommended `core` candidate count: `0`
- recommended first-pass core:
  - none
- strongest deferred candidate:
  - `Leica Elmarit-R 90mm f/2.8`
- explicit `hold` candidate:
  - none
- literature supports real internal historical structure:
  - early / late non-APO line
  - `1-cam / 2-cam / 3-cam`
  - `Series VII`
  - `E55`
- but the local title pool is too thin even for the broad family, so internal splits are well below seed threshold
- broad `elmarit 90` is heavily contaminated by `Vario-Elmarit`, M-side `90mm`, and adjacent Leica `90mm` families

The safest round-1 answer is:

1. keep `Elmarit-R 90` closed for now
2. do not open any `core` or `hold` row
3. keep `Tele-Elmarit 90`, `Summicron-R 90`, and M-side `90mm` families as hard boundaries

## Literature / Reference Base

### Source A: Leica Classic - `Elmarit-R 2,8/90mm`

Leica Classic presents the family under `Elmarit-R 2,8/90mm`.

Reference:

- [Leica Classic - Elmarit-R 2,8/90mm](https://classic.leica-camera.com/en/Leica-Systems/R-System/Lenses/Tele-Lenses/Elmarit-R-2-8-90mm/)

### Source B: Leica Wiki - `90mm f/2.8 Elmarit-R`

Leica Wiki documents `90mm f/2.8 Elmarit-R` with:

- order numbers:
  - `11201`
  - `11202`
  - `11203`
  - `11209`
- production eras:
  - `1968-1976`
  - `1976-1998`
- variants:
  - `1-cam`
  - `2-cam`
  - `3-cam`
- filter types:
  - `Series VII`
  - `E55`
- built-in hood on later version

Reference:

- [Leica Wiki - 90mm f/2.8 Elmarit-R](https://wiki.l-camera-forum.com/leica-wiki.en/index.php?title=90mm_f%2F2.8_Elmarit-R)

### Boundary literature notes

Separate adjacent families are clearly documented in Leica literature:

- `Tele-Elmarit 90`
- `Summicron-R 90`
- `APO-Summicron-R 90 ASPH`

Those must not be folded into `Elmarit-R 90`.

## Taxonomy Implication from Literature

Literature clearly supports:

- one real broad family:
  - `Leica Elmarit-R 90mm f/2.8`

and also clearly supports internal markers:

- `1-cam / 2-cam / 3-cam`
- `Series VII`
- `E55`

But round-1 must still be grounded in local title behavior. Here, literature is strong but local market support remains too thin for seed activation.

## Boundary Check

This family must remain separate from:

- `Leica Elmarit-M 90mm f/2.8`
- `Leica Tele-Elmarit 90mm f/2.8`
- `Leica Tele-Elmarit-M 90mm f/2.8`
- `Leica Summicron-R 90mm f/2`
- `Leica APO-Summicron-R 90mm f/2 ASPH`
- `Leica Summicron-M 90mm f/2`
- `Leica APO-Summicron-M 90mm f/2 ASPH`
- `Leica Elmar 90`
- `Leica Macro-Elmar-M 90`
- `Leica Summilux-R 80`
- `APO-Summicron-SL 90`
- `SL / L-mount 90mm` lenses
- third-party `85 / 90mm` lenses
- hood-only / cap / case / accessory-only listings

## Local Listing Evidence

Analysis base:

- `data/raw/raw_*.json`

### Broad retrieval behavior

Broad `elmarit 90` retrieval is not usable as an R-side family signal.

Observed contamination includes:

- `SL APO Vario-Elmarit 90-280`
- `Vario-Elmarit-R 28-90`
- M-side `90mm` families
- adjacent Leica `90mm` accessory / family overlaps

This means `elmarit 90` must not be treated as a strong row-shaping alias for R-side normalization.

### Clean local R-side pool

After restricting to explicit `90mm` plus explicit R-side `Elmarit` wording, excluding `Tele-Elmarit`, excluding `Vario-Elmarit 28-90`, and deduplicating repeated snapshots by normalized title plus price, the usable pool becomes:

- clean local pool: `1`
- unique titles: `1`
- KRW-priced count: `1`
- KRW median: `880,000`

Observed title:

- `[중고] R 90/2.8 Elmarit (Black)`

Interpretation:

- this confirms the family is not imaginary in local market data
- but the usable evidence is still only a one-title pattern
- local support is too thin to justify conservative seed activation

### Marker distribution inside local pool

Round-1 local support for internal split markers is effectively absent:

- `ROM`: `0`
- `1-cam / 2-cam / 3-cam`: `0`
- `Series VII / E55 / E48`: `0`
- `hood / case / boxed`: `0`

Interpretation:

- literature supports meaningful internal structure
- local seller-title support is too thin even for the broad family
- therefore internal variant rows are clearly out of scope for now

## Smoke Query Review

### Explicit R-side queries

Direct local evidence is extremely thin.

Usable explicit hit pattern:

- `r 90/2.8 elmarit`

Weak or absent direct repetition:

- `elmarit-r 90`
- `elmarit r 90`
- `r 90 elmarit`
- `90 elmarit-r`
- `90mm f2.8 elmarit-r`
- `90mm f/2.8 elmarit-r`
- `leica r 90mm f2.8`
- `elmarit 90 r`

Interpretation:

- one explicit title proves the family exists in local market data
- but title repetition is still too thin and unstable for round-1 seed activation

### Broad shorthand risk

Unsafe broad shorthand:

- `elmarit 90`

Why unsafe:

- heavily contaminated by `SL APO Vario-Elmarit 90-280`
- contaminated by `Vario-Elmarit-R 28-90`
- overlaps with M-side `90mm` family language
- too little explicit R-side support to stabilize it

## Candidate Review

## Candidate 1: `Leica Elmarit-R 90mm f/2.8`

Pros:

- literature-real Leica R family
- Leica Classic and Leica Wiki both support the family cleanly
- literature clearly separates it from `Tele-Elmarit 90`, `Summicron-R 90`, and `APO-Summicron-R 90`

Cons:

- clean local pool is only `1` row / `1` unique title
- priced local support is only `1` row
- broad shorthand `elmarit 90` is badly contaminated
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
- `E55 / E48 / Series marker / filter thread`
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
- `Series VII`
- `E55`

Do not use as strong shaping aliases:

- `elmarit 90`

Reason:

- these are either under-supported internal markers or broad shorthand with heavy contamination risk

## Out-of-Family Boundary

Must remain outside this family:

- `Leica Elmarit-M 90mm f/2.8`
- `Leica Tele-Elmarit 90mm f/2.8`
- `Leica Tele-Elmarit-M 90mm f/2.8`
- `Leica Summicron-R 90mm f/2`
- `Leica APO-Summicron-R 90mm f/2 ASPH`
- `Leica Summicron-M 90mm f/2`
- `Leica APO-Summicron-M 90mm f/2 ASPH`
- `Leica Elmar 90`
- `Leica Macro-Elmar-M 90`
- `Leica Summilux-R 80`
- `APO-Summicron-SL 90`
- `SL / L-mount 90mm` lenses
- accessory-only listings
- third-party `85 / 90mm` lenses

## Final Round-1 Judgment

Immediate round-1 answer:

- immediate core candidate:
  - `0`
- hold candidate:
  - none

Strongest deferred candidate:

- `Leica Elmarit-R 90mm f/2.8`

Round-1 decision:

- `seed 보류`

Why:

1. literature clearly confirms a real Leica R family
2. literature clearly separates it from `Tele-Elmarit 90`, `Summicron-R 90`, and M-side `90mm` families
3. local usable evidence is still only a one-title pattern
4. broad `elmarit 90` is too contaminated to stabilize the family

## Recommendation for Next Round

Do not add a seed row yet.

Only revisit if one of the following improves:

- multiple additional clean local `Elmarit-R 90` titles appear
- KRW-priced local rows accumulate
- explicit R-side wording becomes more stable than the current one-title pattern

If future evidence improves, the next candidate to open would still be:

- `Leica Elmarit-R 90mm f/2.8`

But round-1 should keep the family closed.
