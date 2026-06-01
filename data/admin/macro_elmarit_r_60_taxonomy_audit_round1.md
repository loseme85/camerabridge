# Macro-Elmarit-R 60 Taxonomy Audit - Round 1

Date: 2026-05-13

Scope: audit-only review for the Leica `Macro-Elmarit-R 60` family. This round does not add seed rows, does not modify `entities/*.json`, does not modify `canonical_entities_index.json`, and does not change classifier/query/search behavior, ranking, or UI.

## Executive Summary

`Macro-Elmarit-R 60` is literature-real, but round-1 local support is still too thin to open as a seed family yet.

Round-1 conclusion:

- immediate recommended `core` candidate count: `0`
- recommended first-pass core:
  - none
- strongest deferred candidate:
  - `Leica Macro-Elmarit-R 60mm f/2.8`
- explicit `hold` candidate:
  - none
- literature clearly supports a real Leica R `60mm f/2.8 Macro-Elmarit-R` family
- literature also supports internal marker structure and macro-system context:
  - `2-cam / 3-cam`
  - `Series 7 / E55`
  - `Macro-Adapter-R`
  - hood generation change
- but local title support is effectively a single repeated product pattern and does not justify round-1 seed activation

The safest round-1 answer is:

1. keep `Macro-Elmarit-R 60` closed for now
2. do not open any `core` or `hold` row
3. keep `APO-Macro-Elmarit-R 100`, `Macro-Elmar-R 100`, R-side `50mm / 90mm` families, and third-party macro lines as hard boundaries

## Literature / Reference Base

### Source A: Leica Classic - `Macro-Elmarit-R 2,8/60mm`

Leica Classic presents the family under `Macro-Elmarit-R 2,8/60mm` and shows a real two-stage product structure:

- `1st Model`
  - `11205 / 11212`
- `2nd Model`
  - `11253`

Reference:

- [Leica Classic - Macro-Elmarit-R 2,8/60mm](https://classic.leica-camera.com/en/Leica-Systems/R-System/Lenses/Tele-Lenses/Macro-Elmarit-R-2-8-60mm/)

### Source B: Leica Wiki - `60mm f/2.8 Macro-Elmarit-R`

Leica Wiki documents `60mm f/2.8 Macro-Elmarit-R` with:

- order numbers:
  - `11203`
  - `11205` (`2-cam`)
  - `11212` (`3-cam`)
  - `11347`
  - `11253` (`R-module`)
- production era:
  - `1972-2009`
- variants:
  - `2-cam` version with separate hood
  - `3-cam` version with built-in hood
- filter mount:
  - `Series 7`
  - internal thread `E55`
- accessories:
  - `MACRO-ADAPTER-R`
  - `APO-EXTENDER-R 1.4x / 2x`

Reference:

- [Leica Wiki - 60mm f/2.8 Macro-Elmarit-R](https://wiki.l-camera-forum.com/leica-wiki.en/index.php/60mm_f/2.8_Macro-Elmarit-R)

## Taxonomy Implication from Literature

Literature clearly supports:

- one real broad family:
  - `Leica Macro-Elmarit-R 60mm f/2.8`

Literature also supports meaningful internal structure:

- `2-cam / 3-cam`
- `Series 7 / E55`
- hood generation change
- `Macro-Adapter-R`
- late `R-module` / electronic-era continuation

However, literature alone is not enough to justify round-1 seed activation. The deciding question is whether local seller titles stabilize this family as a usable row. In the current raw pool, they do not.

## Boundary Check

This family must remain separate from:

- `Leica APO-Macro-Elmarit-R 100mm f/2.8`
- `Leica Macro-Elmar-R 100mm f/4`
- `Leica Summicron-R 50mm f/2`
- possible `Leica Elmarit-R 50mm` interpretation space
- `Leica Elmarit-R 90mm f/2.8`
- `Leica Summicron-R 90mm f/2`
- `Leica APO-Summicron-R 90mm f/2 ASPH`
- `SL / L-mount` macro lenses
- third-party `55 / 60 / 90 / 100 / 105mm` macro lenses
- macro-adapter-only / hood-only / cap / case / accessory-only listings

## Local Listing Evidence

Analysis base:

- `data/raw/raw_*.json`

### Broad retrieval behavior

Broad shorthand does not stabilize this family in the current local raw pool.

The following query-style surfaces are weak:

- `macro-elmarit-r 60`
- `macro elmarit r 60`
- `macro elmarit-r 60`
- `r 60 macro elmarit`
- `60 macro elmarit-r`
- `60mm f2.8 macro elmarit-r`
- `60mm f/2.8 macro elmarit-r`
- `r 60/2.8 macro elmarit`
- `leica r 60mm f2.8 macro`
- `macro elmarit 60`

At local raw level, the visible family evidence converges almost entirely on one repeated product-title pattern:

- `LEICA 60mm F2.8 MACRO ELMARIT-R sn.2630`

Interpretation:

- this confirms the family is not imaginary in local data
- but seller wording is not producing a broad, independently repeated local cluster
- broad `macro elmarit 60` should not be allowed to shape normalization in round 1

### Clean local R-side pool

After restricting to explicit `60mm`, explicit R-side `Macro-Elmarit` wording, and excluding `APO-Macro-Elmarit-R 100`, `Macro-Elmar-R 100`, M-side macro, SL-side, and third-party contamination, the usable pool becomes:

- clean local pool: `2`
- unique titles: `2`
- KRW-priced count: `0`
- KRW median: `not available`

Observed titles:

- `상품명 : LEICA 60mm F2.8 MACRO ELMARIT-R sn.2630 60mm Elmarit-R`
- `LEICA 60mm F2.8 MACRO ELMARIT-R sn.2630 60mm Elmarit-R`

Interpretation:

- these are effectively one repeated product pattern rather than a diverse local market cluster
- priced local support is absent
- this is still too thin for conservative seed activation

### Marker distribution inside local pool

Round-1 local support for internal markers is absent:

- `ROM`: `0`
- `cam`: `0` in seller-title wording
- `Series 7 / E55`: `0`
- `E60`: `0`
- `Macro-Adapter-R`: `0`
- `ELPRO`: `0`
- hood / case / boxed: `0`

Interpretation:

- literature supports real internal structure
- local seller-title support is thin even for the broad family
- therefore marker-level rows are clearly out of scope for now

## Smoke Query Review

### Explicit R-side queries

Usable but very thin explicit evidence appears in focal-length-first product wording:

- `60mm f2.8 macro elmarit-r`

Weak or absent direct repetition:

- `macro-elmarit-r 60`
- `macro elmarit r 60`
- `macro elmarit-r 60`
- `r 60 macro elmarit`
- `60 macro elmarit-r`
- `60mm f/2.8 macro elmarit-r`
- `r 60/2.8 macro elmarit`
- `leica r 60mm f2.8 macro`
- `macro elmarit 60`

Interpretation:

- one explicit title pattern proves the family exists in local data
- but title repetition is still too thin and too narrow for round-1 seed activation

### Broad shorthand risk

Unsafe broad shorthand:

- `macro elmarit 60`
- `60 macro`

Why unsafe:

- weak Leica R anchoring in local titles
- overlaps with generic macro intent
- can expand into third-party macro, APO `100mm` macro, and adjacent Leica R macro families

## Candidate Review

## Candidate 1: `Leica Macro-Elmarit-R 60mm f/2.8`

Pros:

- literature-real Leica R family
- Leica Classic and Leica Wiki both support the family cleanly
- literature supports substantial production history and real internal marker structure
- literature keeps the line clearly separate from `APO-Macro-Elmarit-R 100` and `Macro-Elmar-R 100`

Cons:

- clean local pool is only `2`
- the two local rows collapse to one repeated product pattern
- KRW-priced local support is absent
- there is no local evidence strong enough to separate internal markers or prove durable market depth

Round-1 verdict:

- `deferred`

Reason:

- this family is real, but the local evidence is still too thin to justify an explicit seed row in a conservative first pass

## Hold Candidate Review

No explicit `hold` candidate is recommended in round 1.

Why:

- there is no narrower wording with stronger local repetition than the already-thin main family
- `cam`, `Series 7 / E55`, and `Macro-Adapter-R` are real metadata or bundle context, not locally stable row candidates

## Overlay Elements

Keep these as overlay or deferred metadata only:

- `ROM`
- `cam version`
- `E55 / E60 / filter thread`
- `macro adapter included`
- `ELPRO included`
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

These should not become separate rows in round 1.

## Deferred / Not-for-Round-1

Do not open separate rows for:

- `ROM`
- `cam version`
- `Series 7 / E55 / E60`
- `filter thread`
- `Macro-Adapter-R`
- `ELPRO included`

Do not use as strong shaping aliases:

- `macro elmarit 60`
- `60 macro`

Reason:

- these are either under-supported internal markers or broad shorthand with weak Leica R anchoring

## Out-of-Family Boundary

Must remain outside this family:

- `Leica APO-Macro-Elmarit-R 100mm f/2.8`
- `Leica Macro-Elmar-R 100mm f/4`
- Leica R `50mm` families
- Leica R `90mm` families
- `SL / L-mount` macro lenses
- accessory-only listings
- third-party `55 / 60 / 90 / 100 / 105mm` macro lenses

## Final Round-1 Judgment

Immediate round-1 answer:

- immediate core candidate:
  - `0`
- hold candidate:
  - none

Strongest deferred candidate:

- `Leica Macro-Elmarit-R 60mm f/2.8`

Round-1 decision:

- `seed 보류`

Why:

1. literature clearly confirms a real Leica R macro family
2. literature clearly separates it from `APO-Macro-Elmarit-R 100` and `Macro-Elmar-R 100`
3. local usable evidence is only a very thin repeated product pattern
4. priced local support is absent

## Recommendation for Next Round

Do not add a seed row yet.

Only revisit if one of the following improves:

- multiple clean local `Macro-Elmarit-R 60` titles appear beyond the current repeated product pattern
- KRW-priced local rows accumulate
- explicit `R 60/2.8 Macro-Elmarit` wording stabilizes independently from adjacent Leica macro and third-party macro listings

If future evidence improves, the next candidate to open would still be:

- `Leica Macro-Elmarit-R 60mm f/2.8`

But round-1 should keep the family closed.
