# Summilux-R 80 Taxonomy Audit - Round 1

Date: 2026-05-12

Scope: audit-only review for the Leica `Summilux-R 80` family. This round does not add seed rows, does not modify `entities/*.json`, does not modify `canonical_entities_index.json`, and does not change classifier/query/search behavior, ranking, or UI.

## Executive Summary

`Summilux-R 80` is seedable, but only as one narrow R-side family anchor in round 1.

Round-1 conclusion:

- immediate recommended `core` candidate count: `1`
- recommended first-pass core:
  - `Leica Summilux-R 80mm f/1.4`
- explicit `hold` candidate:
  - none
- literature documents real internal version structure:
  - `ROM`
  - `2-cam / 3-cam`
  - `E67`
- but local seller-title support is still too thin and too unspecific to open those as separate rows in round 1
- broad `summilux 80` and `80 lux` must stay outside the initial alias surface because they do not show stable local support and could expand into non-R contamination

The safest round-1 answer is:

1. open one explicit R-side family row
2. keep `ROM`, `cam`, and filter-thread differences below row level
3. do not let broad `summilux 80` or `80 lux` shorthand shape the initial alias surface

## Literature / Reference Base

### Source A: Leica Classic - `Summilux-R 1,4/80mm`

Leica Classic presents the family under `Summilux-R 1,4/80mm` and shows the broad family line cleanly.

Reference:

- [Leica Classic - Summilux-R 1,4/80mm](https://classic.leica-camera.com/en/Leica-Systems/R-System/Lenses/Tele-Lenses/Summilux-R-1-4-80mm/)

### Source B: Leica Wiki - `80mm f/1.4 Summilux-R`

Leica Wiki documents `80mm f/1.4 Summilux-R` with:

- order numbers:
  - `11880`
  - `11881`
  - `11349-ROM`
- production era:
  - `1980-2009`
- variants:
  - `ROM conversion lenses`
  - `ROM lenses after 1996`
- filter mount / hood:
  - `E67`
  - built-in telescopic hood

Reference:

- [Leica Wiki - 80mm f/1.4 Summilux-R](https://wiki.l-camera-forum.com/leica-wiki.en/index.php?title=80mm_f%2F1.4_Summilux-R)

## Taxonomy Implication from Literature

Literature clearly supports:

- one real broad family:
  - `Leica Summilux-R 80mm f/1.4`

and also clearly supports internal markers:

- `ROM`
- `2-cam / 3-cam`
- `E67`

Literature does not, by itself, justify separate seed rows for those markers in round 1. The deciding question is whether local titles split those variants cleanly enough. In this round, they do not.

## Boundary Check

This family must remain separate from:

- `Leica Summilux-R 50mm f/1.4`
- `Leica Summicron-R 90`
- `Leica Elmarit-R 90`
- `Leica APO-Summicron-R 90`
- `Leica Summilux-M 75mm f/1.4`
- `Leica Summicron-M 75mm f/2`
- `Leica Noctilux-M 75mm f/1.25`
- `APO-Summicron-SL 75`
- `APO-Summicron-SL 90`
- `SL / L-mount 75mm / 90mm` lenses
- third-party `75 / 80 / 85 / 90mm` lenses
- hood-only / cap / case / accessory-only listings

## Local Listing Evidence

Analysis base:

- `data/raw/raw_*.json`

### Broad retrieval behavior

Broad shorthand retrieval is weak.

Observed direct query-style support for:

- `summilux-r 80`
- `summilux r 80`
- `summilux 80`
- `80 lux`

was effectively absent in the simple local title pool.

Interpretation:

- local seller style is not using shorthand-first naming
- broad shorthand should not be allowed to shape normalization in round 1

### Clean local R-side pool

After restricting to explicit `80mm` plus explicit R-side `Summilux` wording and deduplicating repeated snapshots by normalized title plus price, the usable local pool becomes:

- clean local pool: `8`
- unique titles: `7`
- KRW-priced count: `4`
- KRW median: `3,540,000`

Observed titles:

- `LEICA 80mm F1.4 SUMMILUX-R sn.3133`
- `LEICA 80mm F1.4 SUMMILUX-R sn.3599`
- `LEICA 80mm F1.4 (ROM) SUMMILUX-R sn.3798`
- `LEICA 80mm F1.4 ROM SUMMILUX-R sn.3798`
- `[중고] R 80/1.4 Summilux ROM (Black)`
- `[위탁] R 80/1.4 Summilux ROM (Black)`

Interpretation:

- this is enough to confirm the family is materially present in local market data
- title repetition converges on one practical Leica R lens intent
- priced rows are not huge, but they are coherent enough for one family-level `core`
- title support is still not specific enough to separate `ROM`, `2-cam / 3-cam`, or filter-thread variants into separate rows

### Marker distribution inside local pool

Round-1 local support for internal split markers is partial but still not row-level:

- `ROM`: repeated
- `2-cam / 3-cam`: not visibly repeated in clean local titles
- `E67 / E60`: not visibly repeated in clean local titles
- `hood / case / boxed`: not meaningfully repeated
- `Safari`: not observed

Interpretation:

- local titles confirm that `ROM` can appear
- literature confirms broader internal structure
- but local repetition is not strong enough to justify separate seed rows for those markers

## Smoke Query Review

### Explicit R-side queries

Strong / usable family evidence appears in focal-length-first title patterns:

- `80mm f1.4 Summilux-R`
- `R 80/1.4 Summilux`
- `Leica R 80mm f1.4`

Weak or absent direct local repetition:

- `summilux-r 80`
- `summilux r 80`
- `r 80 summilux`
- `80 summilux-r`
- `80mm f/1.4 summilux-r`
- `summilux 80 r`
- `summilux 80`
- `80 lux`

Interpretation:

- local seller style converges more on focal-length-first naming than on neat alias-style naming
- the family itself is still stable enough for a single explicit R-side row
- the initial alias set should prefer explicit `R` / `Summilux-R` wording rather than broad shorthand

### Broad shorthand risk

Unsafe broad shorthand:

- `summilux 80`
- `80 lux`

Why unsafe:

- local direct support is too weak
- the wording is not sufficiently anchored to Leica R in seller-title language
- broad shorthand would not add enough precision to justify the contamination risk

## Candidate Review

## Candidate 1: `Leica Summilux-R 80mm f/1.4`

### Literature basis

Strong.

Leica Classic and Leica Wiki both support a real R-side `80mm f/1.4 Summilux-R` family.

### Local title support

Good enough for family-level seeding.

The clean local pool is not huge, but it is clearly thicker than a mere one-off hypothesis and converges on the same R-side lens intent.

### Price behavior

Good enough for family-level seeding.

The priced local pool is modest but coherent, and there is no evidence that the broad family is splitting into incompatible price bands at row level.

### Search-intent stability

Good enough for `core` when wording is explicit about `R`, `Summilux-R`, or a clear `R 80/1.4` pattern.

### Final decision

- `core`

## Hold Candidate Review

No explicit `hold` candidate is recommended in round 1.

Why:

- there is no narrower wording with stronger local support than the broad family line itself
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

These should not become separate rows in round 1.

## Deferred / Not-for-Round-1

Do not open separate rows for:

- `ROM`
- `2-cam / 3-cam`
- `E67`
- `E60`

Do not use as strong shaping aliases:

- `summilux 80`
- `80 lux`

Reason:

- these are either under-supported internal variants or broad shorthand with weak local anchoring

## Out-of-Family Boundary

Must remain outside this family:

- `Leica Summilux-R 50mm f/1.4`
- `Leica Summicron-R 90`
- `Leica Elmarit-R 90`
- `Leica APO-Summicron-R 90`
- `Leica Summilux-M 75mm f/1.4`
- `Leica Summicron-M 75mm f/2`
- `Leica Noctilux-M 75mm f/1.25`
- `APO-Summicron-SL 75`
- `APO-Summicron-SL 90`
- `SL / L-mount 75mm / 90mm` lenses
- accessory-only listings
- third-party `75 / 80 / 85 / 90mm` lenses

## Final Round-1 Judgment

Immediate round-1 answer:

- immediate core candidate:
  - `1`

Recommended first-pass core:

- `Leica Summilux-R 80mm f/1.4`

Hold candidate:

- none

Round-1 decision:

- seedable as one narrow `core`

Why:

1. literature clearly confirms a real Leica R family
2. explicit local R-side titles repeat enough to anchor one broad family row
3. priced local evidence is not huge but is coherent enough for conservative family activation
4. internal markers are not stable enough for row-level splitting

## Recommendation for Next Round

If the next round proceeds to seed activation:

1. add exactly one broad `core` row
   - `Leica Summilux-R 80mm f/1.4`
2. keep `ROM`, `cam`, and `E67 / E60` below row level
3. do not let broad `summilux 80` or `80 lux` shorthand shape the initial alias surface
