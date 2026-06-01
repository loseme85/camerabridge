# Summicron-R 90 Taxonomy Audit - Round 1

Date: 2026-05-12

Scope: audit-only review for the Leica `Summicron-R 90` family. This round does not add seed rows, does not modify `entities/*.json`, does not modify `canonical_entities_index.json`, and does not change classifier/query/search behavior, ranking, or UI.

## Executive Summary

`Summicron-R 90` is literature-real, but round-1 local support is still too thin to open as a seed family yet.

Round-1 conclusion:

- immediate recommended `core` candidate count: `0`
- recommended first-pass core:
  - none
- strongest deferred candidate:
  - `Leica Summicron-R 90mm f/2`
- explicit `hold` candidate:
  - none
- literature clearly separates non-APO `Summicron-R 90` from `APO-Summicron-R 90 ASPH`
- `ROM`, `cam`, and filter-thread markers are literature-real
- but the local title pool is too thin even for the broad family, so internal splits are well below seed threshold

The safest round-1 answer is:

1. keep `Summicron-R 90` closed for now
2. do not open any `core` or `hold` row
3. keep `APO-Summicron-R 90` and other `90mm` Leica families as hard boundaries

## Literature / Reference Base

### Source A: Leica Classic - `Summicron-R 2/90mm`

Leica Classic presents the family under `Summicron-R 2/90mm` with order numbers `11219/11254`.

Reference:

- [Leica Classic - Summicron-R 2/90mm](https://classic.leica-camera.com/en/Leica-Systems/R-System/Lenses/Tele-Lenses/Summicron-R-2-90mm/)

### Source B: Leica Wiki - `90mm f/2 Summicron-R`

Leica Wiki documents `90mm f/2 Summicron-R` with:

- order numbers:
  - `11219`
  - `11254`
- production era:
  - `1970-1977` with 1-piece built-in hood
  - `1977-2000` with 2-piece built-in hood
- variants:
  - `2-cam`
  - `3-cam`
- filter types:
  - `Series VII` (1st)
  - `E55` (2nd)

Reference:

- [Leica Wiki - 90mm f/2 Summicron-R](https://wiki.l-camera-forum.com/leica-wiki.en/index.php?title=90mm_f%2F2_Summicron-R)

### Source C: Leica Classic / Leica Wiki - `APO-Summicron-R 2/90mm ASPH.`

Leica literature clearly treats `APO-Summicron-R 90mm f/2 ASPH` as a separate family:

- Leica Classic:
  - `Apo-Summicron-R 2/90mm ASPH.`
- Leica Wiki:
  - `90mm f/2 APO-Summicron-R ASPH`
  - order number `11350`
  - production era `2002-2009`
  - filter mount `E60`

References:

- [Leica Classic - Apo-Summicron-R 2/90mm ASPH.](https://classic.leica-camera.com/en/Leica-Systems/R-System/Lenses/Tele-Lenses/Apo-Summicron-R-2-90mm-ASPH./)
- [Leica Wiki - 90mm f/2 APO-Summicron-R ASPH](https://wiki.l-camera-forum.com/leica-wiki.en/index.php/90mm_f/2_APO-Summicron-R_ASPH)

## Taxonomy Implication from Literature

Literature clearly supports:

- one real broad non-APO family:
  - `Leica Summicron-R 90mm f/2`

and a separate boundary family:

- `Leica APO-Summicron-R 90mm f/2 ASPH`

Literature also supports internal markers for the non-APO line:

- `2-cam / 3-cam`
- `Series VII`
- `E55`

But round-1 must still be grounded in local title behavior. Here, literature is strong but local market support remains too thin for seed activation.

## Boundary Check

This family must remain separate from:

- `Leica Summicron-M 90mm f/2`
- `Leica APO-Summicron-M 90mm f/2 ASPH`
- `Leica APO-Summicron-R 90mm f/2 ASPH`
- `Leica Elmarit-R 90mm f/2.8`
- `Leica Elmarit-M 90mm f/2.8`
- `Leica Tele-Elmarit 90`
- `Leica Elmar 90`
- `Leica Macro-Elmar-M 90`
- `Leica Summilux-R 80`
- `Leica Summicron-R 50`
- `APO-Summicron-SL 90`
- `SL / L-mount 90mm` lenses
- third-party `85 / 90mm` lenses
- hood-only / cap / case / accessory-only listings

## Local Listing Evidence

Analysis base:

- `data/raw/raw_*.json`

### Broad retrieval behavior

Broad shorthand support is effectively absent in the local title pool.

Queries such as:

- `summicron-r 90`
- `summicron r 90`
- `r 90 summicron`
- `90 summicron-r`
- `summicron 90`

did not produce a stable local title cluster.

Interpretation:

- seller wording is not converging around clean shorthand-first patterns
- broad `summicron 90` should not be allowed to shape normalization in round 1

### Clean local R-side pool

After restricting to explicit `90mm` plus explicit non-APO R-side `Summicron` wording and deduplicating repeated snapshots by normalized title plus price, the usable pool becomes:

- clean local pool: `1`
- unique titles: `1`
- KRW-priced count: `0`
- KRW median: `not available`

Observed title:

- `LEICA 90mm F2 SUMMICRON-R sn.3567`

Interpretation:

- this confirms the family is not imaginary in local data
- but the usable evidence is still only a one-title pattern
- there is no priced local support strong enough to justify conservative seed activation

### Marker distribution inside local pool

Round-1 local support for internal split markers is effectively absent:

- `ROM`: `0`
- `2-cam / 3-cam`: `0`
- `E55 / E48 / Series VII`: `0`
- `hood / case / boxed`: `0`
- `APO`: `0` within the strict non-APO pool

Interpretation:

- literature supports meaningful internal structure
- local seller-title support is too thin even for the broad non-APO family
- therefore internal variant rows are clearly out of scope for now

## Smoke Query Review

### Explicit R-side queries

Direct local evidence is extremely thin.

Usable explicit hit pattern:

- `90mm f2 summicron-r`

Weak or absent direct repetition:

- `summicron-r 90`
- `summicron r 90`
- `r 90 summicron`
- `90 summicron-r`
- `90mm f/2 summicron-r`
- `r 90/2 summicron`
- `leica r 90mm f2`
- `summicron 90 r`

Interpretation:

- one explicit title proves the family exists in local market data
- but title repetition is still too thin and unstable for round-1 seed activation

### Broad shorthand risk

Unsafe broad shorthand:

- `summicron 90`

Why unsafe:

- local direct support is too weak
- the project already has multiple adjacent Leica `90mm` families
- `APO`, M-side, R-side, and accessory contamination risk is too high relative to the current evidence

## Candidate Review

## Candidate 1: `Leica Summicron-R 90mm f/2`

Pros:

- literature-real Leica R family
- Leica Classic and Leica Wiki both support the family cleanly
- literature clearly separates it from `APO-Summicron-R 90`

Cons:

- clean local pool is only `1` row / `1` unique title
- priced local support is absent
- broad shorthand does not stabilize the family
- there is no local evidence strong enough to separate internal markers or to prove a durable market cluster

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
- `E55 / E48 / filter thread`
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
- `2-cam / 3-cam`
- `Series VII`
- `E55`

Do not open as part of this family:

- `APO-Summicron-R 90`

Do not use as strong shaping aliases:

- `summicron 90`

Reason:

- these are either under-supported internal markers, separate adjacent families, or broad shorthand with insufficient local anchoring

## Out-of-Family Boundary

Must remain outside this family:

- `Leica Summicron-M 90mm f/2`
- `Leica APO-Summicron-M 90mm f/2 ASPH`
- `Leica APO-Summicron-R 90mm f/2 ASPH`
- `Leica Elmarit-R 90mm f/2.8`
- `Leica Elmarit-M 90mm f/2.8`
- `Leica Tele-Elmarit 90`
- `Leica Elmar 90`
- `Leica Macro-Elmar-M 90`
- `Leica Summilux-R 80`
- `Leica Summicron-R 50`
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

- `Leica Summicron-R 90mm f/2`

Round-1 decision:

- `seed 보류`

Why:

1. literature clearly confirms a real Leica R family
2. literature also clearly separates non-APO from `APO-Summicron-R 90`
3. local usable evidence is still only a one-title pattern
4. there is no KRW-priced support strong enough to justify conservative seed activation

## Recommendation for Next Round

Do not add a seed row yet.

Only revisit if one of the following improves:

- multiple additional clean local `Summicron-R 90` titles appear
- KRW-priced local rows accumulate
- non-APO wording stabilizes independently from `APO-Summicron-R 90` and other Leica `90mm` families

If future evidence improves, the next candidate to open would still be:

- `Leica Summicron-R 90mm f/2`

But round-1 should keep the family closed.
