# Summicron-R 50 Taxonomy Audit - Round 1

Date: 2026-05-12

Scope: audit-only review for the Leica `Summicron-R 50` family. This round does not add seed rows, does not modify `entities/*.json`, does not modify `canonical_entities_index.json`, and does not change classifier/query/search behavior, ranking, or UI.

## Executive Summary

`Summicron-R 50` is seedable, but only as one narrow R-side family anchor in round 1.

Round-1 conclusion:

- immediate recommended `core` candidate count: `1`
- recommended first-pass core:
  - `Leica Summicron-R 50mm f/2`
- explicit `hold` candidate:
  - none
- literature documents real internal version structure:
  - `1st Model`
  - `2nd Model`
  - `ROM`
  - `3-cam`
  - `Safari`
  - `E55`
- but local seller-title support is too thin and too unspecific to open those as separate rows in round 1
- broad `summicron 50` must stay outside the initial alias surface because it heavily contaminates with Leica M `50mm`, `Rigid`, anniversary editions, and SL-side references

The safest round-1 answer is:

1. open one explicit R-side family row
2. keep `ROM`, `cam`, and filter-thread differences below row level
3. do not let broad `summicron 50` shorthand expand into M / SL contamination

## Literature / Reference Base

### Source A: Leica Classic - `Summicron-R 2/50mm`

Leica Classic presents the family under `Summicron-R 2/50mm` and explicitly groups:

- `1st Model 11218/11228`
- `2nd Model 11215/11216/11345`
- `Safari 11217`

This is strong evidence that Leica treats `Summicron-R 50mm f/2` as a real broad R-side family with internal historical versions rather than unrelated separate lines.

Reference:

- [Leica Classic - Summicron-R 2/50mm](https://classic.leica-camera.com/en/Leica-Systems/R-System/Lenses/Standard-Lenses/Summicron-R-2-50mm/)

### Source B: Leica Wiki - `50mm f/2 Summicron-R II`

Leica Wiki documents `50mm f/2 Summicron-R II` as a real later family version with:

- order numbers:
  - `11215`
  - `11216`
  - `11345-ROM`
  - `11217-Safari`
- production era:
  - `1976-2009`
- variants:
  - `Black`
  - `Safari green`
  - `R-only`
  - `3-cam`
- filter mount:
  - `E55`
- built-in telescopic hood

Reference:

- [Leica Wiki - 50mm f/2 Summicron-R II](https://wiki.l-camera-forum.com/leica-wiki.en/index.php?title=50mm_f%2F2_Summicron-R_II)

## Taxonomy Implication from Literature

Literature clearly supports:

- one real broad family:
  - `Leica Summicron-R 50mm f/2`

and also clearly supports internal variants:

- `Summicron-R I`
- `Summicron-R II`
- `ROM`
- `3-cam`
- `Safari`
- `E55`

But round-1 should not auto-convert every literature-real marker into a seed row. The operative question is whether local titles actually separate these variants cleanly enough. In this round, they do not.

## Boundary Check

This family must remain separate from:

- `Leica Summilux-R 50mm f/1.4`
- `Leica Summicron-M 50`
- `Leica Summilux-M 50`
- `Leica Noctilux 50`
- `Leica Elmar 50`
- `Summicron-R 35`
- `Summicron-R 90`
- `SL / L-mount 50mm` lenses
- third-party `50mm` lenses
- hood-only / cap / case / accessory-only listings

## Local Listing Evidence

Analysis base:

- `data/raw/raw_*.json`

### Broad retrieval behavior

Broad `summicron 50` retrieval is not usable as a family signal.

Observed contamination includes:

- `50mm Summicron-M` variants
- `50mm Summicron 50th Anniversary`
- `50mm Summicron Rigid`
- `50mm APO-Summicron-SL`
- third-party `50mm` lenses

Examples:

- `LEICA 50mm F2 SUMMICRON-M 50 Jahre chrome finish sn.3952`
- `[위탁] M 50/2 Summicron 50주년 (Silver)`
- `Leica M 50mm f2 Summicron Rigid Silver`
- `Used Leica APO-Summicron-SL 50mm`

This means `summicron 50` must not be treated as a strong row-shaping alias for R-side normalization.

### Clean local R-side pool

After restricting to explicit R-side wording and excluding obvious non-R contamination or body-set contamination, the usable local pool becomes:

- clean local pool: `10`
- unique titles: `9`
- KRW-priced count: `3`
- KRW median: `550,000`

Observed titles:

- `Leica R 50mm f2 Summicron Black`
- `LEICA 50mm F2 SUMMICRON-R sn.3338`
- `LEICA 50mm F2 ROM SUMMICRON-R sn.3819`
- `[위탁] R 50/2 Summicron (Black)`

Interpretation:

- this is enough to confirm the family is materially present in local market data
- title surface is still not detailed enough for variant-level splits
- but the broad R-side family line itself is stable enough for a narrow round-1 core

### Marker distribution inside local pool

Round-1 local support for internal split markers is partial but still too thin for row-level separation:

- `ROM`: `1`
- `3-cam`: `0`
- `2-cam`: `0`
- `E55`: `0`
- `E48`: `0`
- `hood / case / boxed`: `0`

Interpretation:

- local titles confirm that `ROM` can appear
- but local repetition is not strong enough to justify a separate `ROM` seed row
- filter-thread and cam differences are literature-real but not operationally stable in seller-title language at this stage

## Smoke Query Review

### Explicit R-side queries

Strong / usable:

- `50mm f2 summicron-r`
- `r 50/2 summicron`
- `leica r 50mm f2`

Weak or absent direct local repetition:

- `summicron-r 50`
- `summicron r 50`
- `r 50 summicron`
- `50 summicron-r`
- `50mm f/2 summicron-r`
- `summicron 50 r`

Interpretation:

- local seller style is looser than the ideal alias surface
- but it still converges strongly enough on one practical R-family line
- the initial alias set should prefer explicit `R` / `Summicron-R` wording

### Broad shorthand risk

Unsafe broad shorthand:

- `summicron 50`

Why unsafe:

- strong contamination from Leica M `50mm Summicron`
- `Rigid` and anniversary lines
- SL-side `Summicron` references

## Candidate Review

## Candidate 1: `Leica Summicron-R 50mm f/2`

### Literature basis

Strong.

Both Leica Wiki and Leica Classic support a real R-side `50mm f/2 Summicron-R` family.

### Local title support

Good enough for family-level seeding.

The clean local pool is still not huge, but title repetition converges on the same practical Leica R lens intent.

### Price behavior

Good enough for family-level seeding.

The priced local pool is small but coherent, and there is no evidence that the broad family is splitting into multiple incompatible price bands at row level.

### Search-intent stability

Good enough for `core` when wording is explicit about `R` or `Summicron-R`.

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
- `E55 / E48`
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

- `Summicron-R I`
- `Summicron-R II`
- `ROM`
- `3-cam`
- `Safari`
- `E55`

Do not use as strong shaping aliases:

- `summicron 50`

Reason:

- these are either under-supported internal variants or broad shorthand with heavy contamination risk

## Out-of-Family Boundary

Must remain outside this family:

- `Leica Summilux-R 50mm f/1.4`
- `Leica Summicron-M 50`
- `Leica Summilux-M 50`
- `Leica Noctilux 50`
- `Leica Elmar 50`
- `Summicron-R 35`
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

- `Leica Summicron-R 50mm f/2`

Hold candidate:

- none

Round-1 decision:

- seedable as one narrow `core`

Why:

1. literature clearly confirms a real Leica R family
2. explicit local R-side titles repeat enough to anchor one broad family row
3. priced local evidence is thin but coherent
4. internal markers are not stable enough for row-level splitting

## Recommendation for Next Round

If the next round proceeds to seed activation:

1. add exactly one broad `core` row
   - `Leica Summicron-R 50mm f/2`
2. keep `ROM`, `cam`, `Safari`, and `E55` below row level
3. do not let broad `summicron 50` shorthand shape the initial alias surface
