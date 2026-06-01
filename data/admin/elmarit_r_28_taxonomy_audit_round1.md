# Elmarit-R 28 Taxonomy Audit - Round 1

Date: 2026-05-11

Scope: audit-only review for the Leica `Elmarit-R 28` family. This round does not add seed rows, does not modify `entities/*.json`, does not modify `canonical_entities_index.json`, and does not change classifier/query/search behavior, ranking, or UI.

## Executive Summary

`Elmarit-R 28` is seedable, but only as one narrow R-side family anchor in round 1.

Round-1 conclusion:

- immediate recommended `core` candidate count: `1`
- recommended first-pass core:
  - `Leica Elmarit-R 28mm f/2.8`
- explicit `hold` candidate:
  - none
- literature documents real internal version structure:
  - `Elmarit-R I`
  - `Elmarit-R II`
  - `ROM`
  - `2-cam / 3-cam / R-only`
  - `Series 7` vs `E55`
- but local seller-title support is too thin and too unspecific to open those as separate rows in round 1
- broad `elmarit 28` must stay outside the initial alias surface because it heavily contaminates with Leica M `28mm`, `Q`-series `28mm`, and `SL` / `Vario-Elmarit` references

The safest round-1 answer is:

1. open one explicit R-side family row
2. keep `ROM`, `cam`, and filter-thread differences below row level
3. do not let broad `elmarit 28` shorthand expand into M / Q / SL contamination

## Literature / Reference Base

### Source A: Leica Wiki - `28mm f/2.8 Elmarit-R I`

Leica Wiki documents `28mm f/2.8 Elmarit-R I` as a real first family version with:

- production era `1970-1992`
- variants:
  - `2-cam`
  - `3-cam`
  - `R-only`
  - `Safari`
- filter type:
  - `Series 7`
- hood:
  - `12509`

Reference:

- [Leica Wiki - 28mm f/2.8 Elmarit-R I](https://wiki.l-camera-forum.com/leica-wiki.en/index.php?title=28mm_f%2F2.8_Elmarit-R_I)

### Source B: Leica Wiki - `28mm f/2.8 Elmarit-R II`

Leica Wiki documents `28mm f/2.8 Elmarit-R II` as a real later family version with:

- production era `1993-2009`
- filter mount:
  - `E55`
- built-in rectangular telescopic hood
- order numbers:
  - `11259`
  - `11333`

Reference:

- [Leica Wiki - 28mm f/2.8 Elmarit-R II](https://wiki.l-camera-forum.com/leica-wiki.en/index.php/28mm_f/2.8_Elmarit-R_II)

### Source C: Leica Classic - R-System page

Leica Classic also presents the family under `Elmarit-R 2,8/28mm`, which supports the practical market view that:

- the lens is a stable Leica R family
- sellers can describe it at the broad family level even when they omit explicit `I / II` terminology

Reference:

- [Leica Classic - Elmarit-R 2,8/28mm](https://classic.leica-camera.com/en/Leica-Systems/R-System/Lenses/Wideangle-Lenses/Elmarit-R-2-8-28mm/)

## Taxonomy Implication from Literature

Literature clearly supports:

- one real broad family:
  - `Leica Elmarit-R 28mm f/2.8`

and also clearly supports internal variants:

- `Elmarit-R I`
- `Elmarit-R II`
- `ROM`
- `2-cam / 3-cam / R-only`
- `Series 7`
- `E55`

But round-1 should not auto-convert every literature-real marker into a seed row. The operative question is whether local titles actually separate these variants cleanly enough. In this round, they do not.

## Boundary Check

This family must remain separate from:

- `Leica Elmarit-M 28mm f/2.8 ASPH`
- `Leica Summicron-M 28mm f/2 ASPH`
- `Leica Summilux-M 28mm f/1.4 ASPH`
- `Leica Summaron-M 28mm f/5.6`
- `Q / Q2 / Q3` fixed-lens `28mm` references
- `Tri-Elmar 28-35-50 / MATE`
- `Elmarit-R 21`
- `Elmarit-R 24`
- `Elmarit-R 35`
- `SL / L-mount 28mm` lenses
- third-party `28mm` lenses
- hood-only / cap / case / accessory-only listings

## Local Listing Evidence

Analysis base:

- `data/normalized/normalized_latest.json`

### Broad retrieval behavior

Broad `elmarit 28` retrieval is not usable as a family signal.

Observed contamination includes:

- Leica M `28mm Elmarit` generations
- `SL` / `APO Vario-Elmarit` titles
- `Q3 28mm`
- hood / finder compatibility references
- `R 28-90 Vario-Elmarit`

Examples:

- `Leica M 28mm f2.8 Elmarit ASPH 5th 6bit Black`
- `[중고] SL APO Vario Elmarit 90-280 f/2.8-4`
- `[중고] Q3 28mm`
- `신품 호환 Leica 14043 Hood Cover for M 35mm f2 Summicron, M 28mm f2.8 Elmarit`

This means `elmarit 28` must not be treated as a strong row-shaping alias for R-side normalization.

### Clean local R-side pool

After restricting to explicit R-side wording, the usable local pool becomes:

- clean local pool: `6`
- unique titles: `4`
- KRW-priced count: `5`
- KRW median: `850,000`

Observed titles:

- `Leica R 28mm f2.8 Elmarit Rom Black`
- `[위탁] R 28/2.8 Elmarit (Black)`
- `[중고] R 28/2.8 Elmarit`
- `LEICA 28mm F2.8 ELMARIT-R sn.3624`

### Marker distribution inside local pool

Round-1 local support for internal split markers is partial but still too thin for row-level separation:

- `ROM`: `1`
- `3-cam`: `0`
- `2-cam`: `0`
- `1-cam`: `0`
- `E55`: `0`
- `E48`: `0`
- `black`: `2`

Interpretation:

- local titles confirm that `ROM` can appear
- but local repetition is not strong enough to justify a separate `ROM` seed row
- `I / II` and filter-thread differences are literature-real but not operationally stable in seller-title language at this stage

## Smoke Query Review

### Explicit R-side queries

Strong / usable:

- `28mm f2.8 elmarit-r`
- `r 28/2.8 elmarit`
- `leica r 28mm f2.8`

Weak or absent direct local repetition:

- `elmarit-r 28`
- `elmarit r 28`
- `r 28 elmarit`
- `28 elmarit-r`
- `28mm f/2.8 elmarit-r`
- `elmarit 28 r`

Interpretation:

- local seller style is a bit looser than the ideal alias surface
- but it still converges strongly enough on one practical R-family line
- the initial alias set should prefer explicit `R` / `Elmarit-R` wording

### Broad shorthand risk

Unsafe broad shorthand:

- `elmarit 28`

Why unsafe:

- strong contamination from Leica M `28mm Elmarit`
- `Q3 28mm`
- `SL` Vario / APO Vario Elmarit lines

## Candidate Review

## Candidate 1: `Leica Elmarit-R 28mm f/2.8`

### Literature basis

Strong.

Both Leica Wiki and Leica Classic support a real R-side `28mm f/2.8 Elmarit-R` family.

### Local title support

Moderate but coherent.

The clean pool is not large, but the titles converge on the same practical Leica R lens intent.

### Price behavior

Good enough for family-level seeding.

The local priced pool clusters in a coherent used-lens range, even if it is too small to support sub-row creation.

### Search-intent stability

Good enough for `core` when wording is explicit about `R` or `Elmarit-R`.

### Final decision

`core`

### One-line reason

`Leica Elmarit-R 28mm f/2.8` is literature-real and locally coherent enough to seed as one narrow R-family row.

## Candidate 2: `Elmarit-R I` / `Elmarit-R II`

### Literature basis

Strong.

These are real internal family versions.

### Local title support

Weak.

The current local pool does not repeat `I / II` wording directly.

### Final decision

`deferred`

### One-line reason

`I / II` is a real historical split, but round-1 local titles do not separate it cleanly enough for immediate seed rows.

## Candidate 3: `ROM` / `cam` / filter-thread rows

### Literature basis

Real markers exist.

### Local title support

Too thin.

Only `ROM` appears directly, and only once in the clean unique pool.

### Final decision

`deferred`

### One-line reason

These are meaningful variant markers, but round-1 evidence supports keeping them as metadata rather than opening separate rows.

## Overlay Elements

Keep as `overlay`:

- `ROM`
- `1-cam / 2-cam / 3-cam`
- `E55 / E48`
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

- `Leica Elmarit-R 28mm f/2.8 I`
- `Leica Elmarit-R 28mm f/2.8 II`
- `Leica Elmarit-R 28mm f/2.8 ROM`
- `Leica Elmarit-R 28mm f/2.8 3-cam`
- `Leica Elmarit-R 28mm f/2.8 E55`
- `Leica Elmarit-R 28mm f/2.8 Series 7`

### Deferred shorthand

Do not use as strong initial aliases:

- `elmarit 28`

Reason:

- too much M-side, Q-side, and SL-side contamination

## Out-of-Family Boundary

Must remain outside this family:

- `Leica Elmarit-M 28mm f/2.8 ASPH`
- `Leica Summicron-M 28mm f/2 ASPH`
- `Leica Summilux-M 28mm f/1.4 ASPH`
- `Leica Summaron-M 28mm f/5.6`
- `Q / Q2 / Q3 28mm`
- `Tri-Elmar 28-35-50 / MATE`
- `Elmarit-R 21`
- `Elmarit-R 24`
- `Elmarit-R 35`
- `APO-Summicron-SL 28`
- `SL Vario-Elmarit` contamination
- third-party `28mm` lenses
- accessory-only listings

## Final Round-1 Judgment

- immediate core candidate:
  - `Leica Elmarit-R 28mm f/2.8`
- hold candidate:
  - none
- overlay:
  - `ROM`, `cam markers`, `E55 / E48`, filter-thread, finish, country, hood/cap/box/case/packaging
- out-of-family:
  - Leica M `28mm` families, `Q` fixed-lens references, `MATE`, other R wide families, `SL/L`, accessories, third-party

## Recommendation for Next Round

Next round may proceed with one narrow seed only:

- `Leica Elmarit-R 28mm f/2.8`

But that future seed should remain conservative:

- one `core` row only
- no `ROM` row
- no `cam` row
- no `E55 / E48` row
- no broad `elmarit 28` alias
