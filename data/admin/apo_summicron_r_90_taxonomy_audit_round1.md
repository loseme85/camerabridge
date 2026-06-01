# APO-Summicron-R 90 Taxonomy Audit - Round 1

Date: 2026-05-13

Scope: audit-only review for the Leica `APO-Summicron-R 90` family. This round does not add seed rows, does not modify `entities/*.json`, does not modify `canonical_entities_index.json`, and does not change classifier/query/search behavior, ranking, or UI.

## Executive Summary

`APO-Summicron-R 90` is literature-real, but round-1 local support is effectively absent, so it should remain closed for now.

Round-1 conclusion:

- immediate recommended `core` candidate count: `0`
- recommended first-pass core:
  - none
- strongest deferred candidate:
  - `Leica APO-Summicron-R 90mm f/2 ASPH`
- explicit `hold` candidate:
  - none
- literature clearly separates this line from non-APO `Summicron-R 90`
- literature also separates it from `APO-Summicron-M 90` and `APO-Summicron-SL 90`
- but local title support for the R-side APO family is effectively absent even before internal splits are considered

The safest round-1 answer is:

1. keep `APO-Summicron-R 90` closed for now
2. do not open any `core` or `hold` row
3. keep non-APO `Summicron-R 90`, M-side `90mm` families, and `SL` APO `90mm` lines as hard boundaries

## Literature / Reference Base

### Source A: Leica Classic - `Apo-Summicron-R 2/90mm ASPH.`

Leica Classic presents the family under `Apo-Summicron-R 2/90mm ASPH.` as a distinct R-system tele lens.

Reference:

- [Leica Classic - Apo-Summicron-R 2/90mm ASPH.](https://classic.leica-camera.com/en/Leica-Systems/R-System/Lenses/Tele-Lenses/Apo-Summicron-R-2-90mm-ASPH./)

### Source B: Leica Wiki - `90mm f/2 APO-Summicron-R ASPH`

Leica Wiki documents `90mm f/2 APO-Summicron-R ASPH` with:

- order number:
  - `11350`
- production era:
  - `2002-2009`
- filter mount:
  - `E60`
- late R-system APO / ASPH identity

Reference:

- [Leica Wiki - 90mm f/2 APO-Summicron-R ASPH](https://wiki.l-camera-forum.com/leica-wiki.en/index.php/90mm_f/2_APO-Summicron-R_ASPH)

## Taxonomy Implication from Literature

Literature clearly supports:

- one real broad family:
  - `Leica APO-Summicron-R 90mm f/2 ASPH`

Literature also suggests a narrow late-line marker set:

- `ROM`
- `E60`
- `ASPH`

In contrast to older R families, this line does not present as a broad cam-era family with multiple title-stable historical sublines in the sources used for this round. Practically, the literature picture is one late explicit APO R family rather than a cluster of locally separable internal rows.

## Boundary Check

This family must remain separate from:

- non-APO `Leica Summicron-R 90mm f/2`
- `Leica Summicron-M 90mm f/2`
- `Leica APO-Summicron-M 90mm f/2 ASPH`
- `Leica Elmarit-R 90mm f/2.8`
- `Leica Elmarit-M 90mm f/2.8`
- `Leica Tele-Elmarit 90`
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

Broad APO shorthand does not stabilize the R-side family in local raw titles.

Queries and title patterns such as:

- `apo-summicron-r 90`
- `apo summicron r 90`
- `r 90 apo summicron`
- `90mm f2 apo summicron-r`
- `apo summicron 90 r`
- `apo summicron 90`

do not produce a usable local R-side APO cluster.

Instead, the visible local surface is dominated by:

- `APO-Summicron-M 90`
- other M-side `APO-Summicron` lines
- `APO-Summicron-SL 90`
- adjacent Leica `90mm` families

Interpretation:

- local seller wording is not converging around explicit R-side APO `90mm` titles
- broad `apo summicron 90` must not be allowed to shape normalization for this family in round 1

### Clean local R-side pool

After restricting to explicit `90mm`, explicit `R` intent, and explicit `APO-Summicron` wording while excluding M-side, SL-side, and accessory contamination, the usable pool becomes:

- clean local pool: `0`
- unique titles: `0`
- KRW-priced count: `0`
- KRW median: `not available`

Observed result:

- no stable local clean title for `Leica APO-Summicron-R 90mm f/2 ASPH` was confirmed in the current raw pool

Interpretation:

- literature confirms the family is real
- but local evidence is currently below even a thin one-title threshold
- this is materially weaker than recent R-side families that were allowed to open

### Marker distribution inside local pool

Round-1 local support for internal markers is absent:

- `ROM`: `0`
- `E60`: `0`
- `ASPH`: `0` in a confirmed R-side clean pool
- `hood / case / boxed`: `0`

Interpretation:

- literature supports real late-line metadata
- local seller-title support is absent even for the main family
- therefore internal split discussion is far below seed threshold

## Smoke Query Review

### Explicit R-side queries

No stable local repetition was confirmed for:

- `apo-summicron-r 90`
- `apo summicron r 90`
- `apo summicron-r 90`
- `r 90 apo summicron`
- `90 apo summicron-r`
- `90mm f2 apo summicron-r`
- `90mm f/2 apo summicron-r`
- `r 90/2 apo summicron`
- `leica r 90mm f2 apo`
- `apo cron r 90`
- `apo summicron 90 r`

Interpretation:

- explicit R-side APO wording is not showing a usable local cluster
- there is not enough title repetition to justify a conservative round-1 seed row

### Broad shorthand risk

Unsafe broad shorthand:

- `apo summicron 90`
- `90 apo`

Why unsafe:

- heavily contaminated by `APO-Summicron-M 90`
- overlaps with `APO-Summicron-SL 90`
- not anchored strongly enough to Leica R in local seller titles

## Candidate Review

## Candidate 1: `Leica APO-Summicron-R 90mm f/2 ASPH`

Pros:

- literature-real Leica R family
- Leica Classic and Leica Wiki both support the family cleanly
- literature clearly separates it from non-APO `Summicron-R 90`
- literature clearly separates it from `APO-Summicron-M 90` and `APO-Summicron-SL 90`

Cons:

- clean local pool is `0`
- unique title support is `0`
- KRW-priced local support is `0`
- local raw retrieval is dominated by M-side APO `90mm` and adjacent families
- there is no evidence strong enough to prove a stable local row-level market cluster yet

Round-1 verdict:

- `deferred`

Reason:

- this family is real in literature, but current local evidence is effectively absent, so opening even a narrow explicit seed row would be premature

## Hold Candidate Review

No explicit `hold` candidate is recommended in round 1.

Why:

- there is no narrower wording with stronger local repetition than the already-absent main family
- `ROM`, `E60`, and `ASPH` are real metadata markers, not locally stable row candidates

## Overlay Elements

Keep these as overlay or deferred metadata only:

- `ROM`
- `E60`
- `filter thread`
- `ASPH`
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

These should not become separate rows in round 1.

## Deferred / Not-for-Round-1

Do not open separate rows for:

- `ROM`
- `E60`
- `filter thread`
- `ASPH`

Do not use as strong shaping aliases:

- `apo summicron 90`
- `90 apo`

Reason:

- these are either under-supported metadata markers or broad shorthand with strong M/SL contamination risk

## Out-of-Family Boundary

Must remain outside this family:

- non-APO `Leica Summicron-R 90mm f/2`
- `Leica APO-Summicron-M 90mm f/2 ASPH`
- `Leica Summicron-M 90mm f/2`
- `Leica Elmarit-R 90mm f/2.8`
- `Leica Elmarit-M 90mm f/2.8`
- `Leica Tele-Elmarit 90`
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

- `Leica APO-Summicron-R 90mm f/2 ASPH`

Round-1 decision:

- `seed 보류`

Why:

1. literature clearly confirms a real Leica R APO family
2. literature clearly separates it from non-APO `Summicron-R 90`
3. local usable evidence is effectively absent
4. broad APO `90mm` shorthand is dominated by M-side and SL-side contamination

## Recommendation for Next Round

Do not add a seed row yet.

Only revisit if one of the following improves:

- multiple clean local `APO-Summicron-R 90` titles appear
- KRW-priced local rows accumulate
- explicit `R`-side APO wording stabilizes independently from M-side `APO-Summicron-M 90` and `APO-Summicron-SL 90`

If future evidence improves, the next candidate to open would still be:

- `Leica APO-Summicron-R 90mm f/2 ASPH`

But round-1 should keep the family closed.
