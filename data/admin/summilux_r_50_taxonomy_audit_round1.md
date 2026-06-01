# Summilux-R 50 Taxonomy Audit - Round 1

Date: 2026-05-12

Scope: audit-only review for the Leica `Summilux-R 50` family. This round does not add seed rows, does not modify `entities/*.json`, does not modify `canonical_entities_index.json`, and does not change classifier/query/search behavior, ranking, or UI.

## Executive Summary

`Summilux-R 50` is seedable, but only as one narrow R-side family anchor in round 1.

Round-1 conclusion:

- immediate recommended `core` candidate count: `1`
- recommended first-pass core:
  - `Leica Summilux-R 50mm f/1.4`
- explicit `hold` candidate:
  - none
- literature documents real internal version structure:
  - `Summilux-R I`
  - `Summilux-R II`
  - `ROM`
  - `2-cam / 3-cam`
  - `Safari`
  - `E55`
  - `E60`
- but local seller-title support is still too thin and too unspecific to open those as separate rows in round 1
- broad `summilux 50` and `50 lux` must stay outside the initial alias surface because they heavily contaminate with Leica M `50mm`, SL-side references, and third-party `50mm` titles

The safest round-1 answer is:

1. open one explicit R-side family row
2. keep `ROM`, `cam`, and filter-thread differences below row level
3. do not let broad `summilux 50` or `50 lux` shorthand expand into M / SL contamination

## Literature / Reference Base

### Source A: Leica Classic - `Summilux-R 1,4/50mm`

Leica Classic presents the family under `Summilux-R 1,4/50mm`, which is already enough to establish a real Leica R-side family line.

Reference:

- [Leica Classic - Summilux-R 1,4/50mm](https://classic.leica-camera.com/at/de/lcc/objektive/leicaflex-sl-r/standard/50-14-2/index.html)

### Source B: Leica Wiki - `50mm f/1.4 Summilux-R I`

Leica Wiki documents `50mm f/1.4 Summilux-R I` with:

- production era:
  - `1970-1998`
- variants:
  - `2-cam`
  - `3-cam`
  - black
  - `Safari`
  - gold
- filter type:
  - `E55`
- hood note:
  - external hood early, built-in hood later

Reference:

- [Leica Wiki - 50mm f/1.4 Summilux-R I](https://wiki.l-camera-forum.com/leica-wiki.en/index.php/50mm_f/1.4_Summilux-R_I)

### Source C: Leica Wiki - `50mm f/1.4 Summilux-R II`

Leica Wiki documents `50mm f/1.4 Summilux-R II` with:

- production era:
  - `1998-2009`
- variants:
  - `Non-ROM`
  - `ROM`
- filter / hood:
  - `E60`
  - built-in telescopic hood

Reference:

- [Leica Wiki - 50mm f/1.4 Summilux-R II](https://wiki.l-camera-forum.com/leica-wiki.en/index.php/50mm_f/1.4_Summilux-R_II)

## Taxonomy Implication from Literature

Literature clearly supports:

- one real broad family:
  - `Leica Summilux-R 50mm f/1.4`

and also clearly supports internal variants / markers:

- `Summilux-R I`
- `Summilux-R II`
- `ROM`
- `2-cam / 3-cam`
- `Safari`
- `E55`
- `E60`

But round-1 should not auto-convert every literature-real marker into a seed row. The operative question is whether local titles actually separate these variants cleanly enough. In this round, they do not.

## Boundary Check

This family must remain separate from:

- `Leica Summicron-R 50mm f/2`
- `Leica Summilux-M 50`
- `Leica Summicron-M 50`
- `Leica Noctilux 50`
- `Leica Elmar 50`
- `Summilux-R 35`
- `Summilux-R 80`
- `Summicron-R 90`
- `APO-Summicron-SL 50`
- `SL / L-mount 50mm` lenses
- third-party `50mm` lenses
- hood-only / cap / case / accessory-only listings

## Local Listing Evidence

Analysis base:

- `data/raw/raw_*.json`

### Broad retrieval behavior

Broad `summilux 50` retrieval is not usable as an R-side family signal.

Observed contamination includes:

- `50mm Summilux-M`
- M-side ASPH / FLE style titles
- `50mm APO-Summicron-SL`
- third-party `50mm` lenses

Examples:

- `[중고] SL Summilux 50/1.4 ASPH`
- M-side `50mm Summilux` style titles
- third-party `50mm` brand results

This means `summilux 50` and `50 lux` must not be treated as strong row-shaping aliases for R-side normalization.

### Clean local R-side pool

After restricting to explicit `50mm` plus explicit R-side `Summilux` wording and excluding obvious body-set contamination, the usable local pool becomes:

- clean local pool: `20`
- unique titles: `16`
- KRW-priced count: `7`
- KRW median: `3,980,000`

Observed titles:

- `Leica R 50mm f1.4 Summilux E60 Rom Black`
- `LEICA 50mm F1.4 SUMMILUX-R sn.3290`
- `LEICA 50mm F1.4 SUMMILUX-R sn.3633`
- `LEICA 50mm F1.4 E60 SUMMILUX-R (ROM) sn.3821`
- `[중고] R 50/1.4 Summilux E60 ROM (Black)`

Interpretation:

- this is enough to confirm that the family is materially present in local market data
- title surface is much thicker than the weaker deferred R-side `35mm` candidates
- local support is sufficient for one narrow family-level `core`
- but title support is still not specific enough to separate `I / II`, `ROM`, `Safari`, or filter-thread variants into separate rows

### Marker distribution inside local pool

Round-1 local support for internal split markers is real but still not row-level:

- `ROM`: repeated
- `E60`: repeated
- `Safari`: not repeated in clean local lens-only titles
- `2-cam / 3-cam`: not visibly repeated in clean local titles
- `hood / case / boxed`: not meaningfully repeated

Interpretation:

- local titles confirm that `ROM` and `E60` can appear
- literature confirms broader internal structure including `I / II`, `2-cam / 3-cam`, `Safari`, `E55`, and `E60`
- but local repetition is not strong enough to justify separate seed rows for those markers

## Smoke Query Review

### Explicit R-side queries

Strong / usable:

- `50mm f1.4 summilux-r`
- `r 50/1.4 summilux`
- `leica r 50mm f1.4`

Weak or absent direct local repetition:

- `summilux-r 50`
- `summilux r 50`
- `r 50 summilux`
- `50 summilux-r`
- `50mm f/1.4 summilux-r`
- `summilux 50 r`
- `50 lux r`

Interpretation:

- local seller style leans more toward formatted focal-length-first titles than ideal alias wording
- but the family still converges clearly enough on one practical R-side lens intent
- the initial alias set should prefer explicit `R` / `Summilux-R` wording

### Broad shorthand risk

Unsafe broad shorthand:

- `summilux 50`
- `50 lux`

Why unsafe:

- strong contamination from Leica M `50mm Summilux`
- overlap with SL-side `50mm` titles
- overlap with third-party `50mm` titles

## Candidate Review

## Candidate 1: `Leica Summilux-R 50mm f/1.4`

### Literature basis

Strong.

Leica Classic and Leica Wiki both support a real R-side `50mm f/1.4 Summilux-R` family.

### Local title support

Good enough for family-level seeding.

The clean local pool is not tiny, and title repetition converges on the same practical Leica R lens intent.

### Price behavior

Good enough for family-level seeding.

The priced local pool is still modest, but coherent enough for a broad family anchor. There is no evidence that the broad family is splitting into multiple incompatible price bands at row level.

### Search-intent stability

Good enough for `core` when wording is explicit about `R`, `Summilux-R`, or a clear `R 50/1.4` pattern.

### Final decision

- `core`

## Hold Candidate Review

No explicit `hold` candidate is recommended in round 1.

Why:

- there is no narrower wording with stronger local support than the broad family line itself
- internal variants are literature-real but locally under-supported at row level

## Overlay Elements

Keep these as overlay or deferred metadata only:

- `ROM`
- `1-cam / 2-cam / 3-cam`
- `E55 / E60`
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

These should not become separate rows in round 1.

## Deferred / Not-for-Round-1

Do not open separate rows for:

- `Summilux-R I`
- `Summilux-R II`
- `ROM`
- `2-cam / 3-cam`
- `Safari`
- `E55`
- `E60`

Do not use as strong shaping aliases:

- `summilux 50`
- `50 lux`

Reason:

- these are either under-supported internal variants or broad shorthand with heavy contamination risk

## Out-of-Family Boundary

Must remain outside this family:

- `Leica Summicron-R 50mm f/2`
- `Leica Summilux-M 50`
- `Leica Summicron-M 50`
- `Leica Noctilux 50`
- `Leica Elmar 50`
- `Summilux-R 35`
- `Summilux-R 80`
- `Summicron-R 90`
- `APO-Summicron-SL 50`
- `SL / L-mount 50mm` lenses
- accessory-only listings
- third-party `50mm` lenses

## Final Round-1 Judgment

Immediate round-1 answer:

- immediate core candidate:
  - `1`

Recommended first-pass core:

- `Leica Summilux-R 50mm f/1.4`

Hold candidate:

- none

Round-1 decision:

- seedable as one narrow `core`

Why:

1. literature clearly confirms a real Leica R family
2. explicit local R-side titles repeat enough to anchor one broad family row
3. priced local evidence is not huge but is coherent enough for round-1 family activation
4. internal markers are not stable enough for row-level splitting

## Recommendation for Next Round

If the next round proceeds to seed activation:

1. add exactly one broad `core` row
   - `Leica Summilux-R 50mm f/1.4`
2. keep `ROM`, `cam`, `Safari`, and `E55 / E60` below row level
3. do not let broad `summilux 50` or `50 lux` shorthand shape the initial alias surface
