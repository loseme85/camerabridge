# Elmarit-R 24 Taxonomy Audit - Round 1

Date: 2026-05-11

Scope: audit-only review for the Leica `Elmarit-R 24` family. This round does not add seed rows, does not modify `entities/*.json`, does not modify `canonical_entities_index.json`, and does not change classifier/query/search behavior, ranking, or UI.

## Executive Summary

`Elmarit-R 24` is seedable, but only as one narrow R-side line.

Round-1 conclusion:

- immediate recommended `core` candidate count: `1`
- recommended first-pass core:
  - `Leica Elmarit-R 24mm f/2.8`
- explicit `hold` candidate:
  - none
- `ROM`, `1-cam / 2-cam / 3-cam`, and `E60` are real variant markers in literature, but remain `overlay` or `deferred internal split`
- broad `elmarit 24` must stay outside the seed alias surface because it strongly contaminates with Leica M `24mm` and SL zoom titles

The safest round-1 answer is:

1. open one explicit R-side family anchor
2. keep version markers below row level
3. do not let `elmarit 24` broaden into M / SL contamination

## Literature / Reference Base

### Source A: Leica Wiki - `24mm f/2.8 Elmarit-R`

Leica Wiki documents `24mm f/2.8 Elmarit-R` as a distinct Leica R family with:

- production era `1974-2006`
- manufacturer `Minolta`
- variants:
  - `without ROM`
  - `ROM possible`
  - `with ROM`
- order numbers:
  - `11221`
  - `11257`
  - `11331`
- inscription examples:
  - `ELMARIT-R 1:2.8/24 LEITZ WETZLAR`
  - `ELMARIT-R 1:2.8/24 E60 LEICA`

Reference:

- [Leica Wiki - 24mm f/2.8 Elmarit-R](https://wiki.l-camera-forum.com/leica-wiki.en/index.php/24mm_f/2.8_Elmarit-R)

Implication for taxonomy:

- `Elmarit-R 24mm f/2.8` is literature-real
- `ROM` and `E60` are literature-real markers
- but the literature does not require round-1 row splitting by `ROM` or `cam` generation

### Source B: Leica Classic - R-System page

Leica Classic lists the family as `Elmarit-R 2,8/24mm` under the R-System wide-angle lens section and surfaces mixed market naming such as:

- `Leica Elmarit-R 11221 2,8/24mm`
- `LEICA ELMARIT-R 1:2.8/24 mm ROM`
- `LEICA Elmarit-R 2.8/24`

Reference:

- [Leica Classic - Elmarit-R 2,8/24mm](https://classic.leica-camera.com/en/Leica-Systems/R-System/Lenses/Wideangle-Lenses/Elmarit-R-2-8-24mm/)

Implication for taxonomy:

- market wording consistently converges on one R-family line
- `ROM` is visible as listing metadata, not yet as a separate row requirement

## Boundary Check

This family must remain separate from:

- `Leica Elmarit-M 24mm f/2.8 ASPH`
- `Leica Elmar-M 24mm f/3.8 ASPH`
- `Leica Summilux-M 24mm f/1.4 ASPH`
- closed `Summicron 24` non-family hypothesis
- `Tri-Elmar 16-18-21 / WATE`
- `Super-Elmar 18`
- Leica `21mm` M families
- Leica R `21mm` / `28mm` wide families
- `SL` / `L-mount` `24mm` lenses
- third-party `24mm` lenses
- hood-only / cap / case / accessory-only listings

## Local Listing Evidence

Analysis base:

- `data/normalized/normalized_latest.json`

### Broad retrieval behavior

Broad `elmarit 24` retrieval is not usable as a family signal.

Observed contamination includes:

- `SL Vario-Elmarit 24-90`
- Leica M-side `24mm Elmarit`
- possible mixed `24` serial or title fragments

Example:

- `[중고] SL Vario Elmarit 24-90/2.8-4 ASPH.`

This means `elmarit 24` must not be treated as a strong row-shaping alias for R-side normalization.

### Clean local R-side pool

After restricting to explicit R-side wording, the usable local pool becomes:

- clean local pool: `4`
- unique titles: `4`
- KRW-priced count: `1`
- KRW median: `750,000`

Observed titles:

- `Leica R 24mm f2.8 Elmarit Black`
- `LEICA 24mm F2.8 ELMARIT-R sn.3658`
- `LEICA 24mm F2.8 ELMARIT-R sn.3102`
- `LEICA R8 24mm F2.8 ELMARIT-R SN.9569`

### Marker distribution inside local pool

Round-1 local support for internal split markers is weak:

- `ROM`: `0` direct local titles in the clean pool
- `1-cam / 2-cam / 3-cam`: `0`
- `E60`: `0`
- `hood / case / boxed`: `0`
- `black`: `1`

Interpretation:

- literature supports these markers as real
- local seller title support is too thin to promote any of them to seed-row level

## Smoke Query Review

### Explicit R-side queries

Strong / usable:

- `24mm f2.8 elmarit-r`
- `leica r 24mm f2.8`

Weak or absent direct local repetition:

- `elmarit-r 24`
- `elmarit r 24`
- `r 24 elmarit`
- `24 elmarit-r`
- `24mm f/2.8 elmarit-r`
- `r 24/2.8 elmarit`
- `elmarit 24 r`

Interpretation:

- local title style is explicit enough to support one family row
- but aliases should stay conservative and favor `24mm f2.8 Elmarit-R` / `Leica R 24mm f2.8 Elmarit` style phrasing

### Broad shorthand risk

Unsafe broad shorthand:

- `elmarit 24`

Why unsafe:

- directly contaminated by `SL Vario-Elmarit 24-90`
- easily overlaps with Leica M `Elmarit 24`

## Candidate Review

## Candidate 1: `Leica Elmarit-R 24mm f/2.8`

### Literature basis

Strong.

Both Leica Wiki and Leica Classic support a single real R-side `24mm f/2.8 Elmarit-R` family.

### Local title support

Thin but coherent.

The local pool is small, but every clean title points to the same R-side line.

### Price behavior

Too thin for internal split, but not contradictory for the family itself.

The single KRW-priced example does not justify sub-rows.

### Search-intent stability

Good enough for `core` when wording is explicit about `R` or `Elmarit-R`.

### Final decision

`core`

### One-line reason

`Leica Elmarit-R 24mm f/2.8` is literature-real and locally coherent enough to seed as one narrow R-family line.

## Candidate 2: `ROM` / `cam` / `E60` internal rows

### Literature basis

Real markers exist.

### Local title support

Weak.

Round-1 clean pool does not show repeatable direct local title support for:

- `ROM`
- `1-cam / 2-cam / 3-cam`
- `E60`

### Final decision

`deferred`

### One-line reason

These are real variant markers, but round-1 evidence supports preserving them as metadata rather than opening separate rows.

## Overlay Elements

Keep as `overlay`:

- `ROM`
- `1-cam / 2-cam / 3-cam`
- `E60`
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

- `Elmarit-R 24mm f/2.8 ROM`
- `Elmarit-R 24mm f/2.8 3-cam`
- `Elmarit-R 24mm f/2.8 E60`

### Deferred shorthand

Do not use as strong initial aliases:

- `elmarit 24`

Reason:

- too much M-side and SL-side contamination

## Out-of-Family Boundary

Must remain outside this family:

- `Leica Elmarit-M 24mm f/2.8 ASPH`
- `Leica Elmar-M 24mm f/3.8 ASPH`
- `Leica Summilux-M 24mm f/1.4 ASPH`
- closed `Summicron 24` hypothesis
- `Tri-Elmar 16-18-21 / WATE`
- `Super-Elmar 18`
- Leica `21mm` M families
- `Elmarit-R 21`
- `Elmarit-R 28`
- `APO-Summicron-SL 24`
- third-party `24mm` lenses
- accessory-only listings

## Final Round-1 Judgment

- immediate core candidate:
  - `Leica Elmarit-R 24mm f/2.8`
- hold candidate:
  - none
- overlay:
  - `ROM`, `cam markers`, `E60`, `filter thread`, finish, country, hood/cap/box/case/packaging
- out-of-family:
  - Leica M `24mm` families, `18mm` / `21mm` M families, `WATE`, other R wide families, `SL/L`, accessories, third-party

## Recommendation for Next Round

Next round may proceed with one narrow seed only:

- `Leica Elmarit-R 24mm f/2.8`

But that future seed should remain conservative:

- one `core` row only
- no `ROM` row
- no `cam` row
- no `E60` row
- no broad `elmarit 24` alias
