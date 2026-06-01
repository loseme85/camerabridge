# Elmarit-R 135 Taxonomy Audit - Round 1

Date: 2026-05-14

Scope: audit-only review for the Leica `Elmarit-R 135` family. This round does not add seed rows, does not modify `entities/*.json`, does not modify `canonical_entities_index.json`, and does not change classifier/query/search behavior, ranking, or UI.

## Executive Summary

`Elmarit-R 135` is literature-real, but round-1 local support is still too thin and price evidence is absent, so it should remain closed for now.

Round-1 conclusion:

- immediate recommended `core` candidate count: `0`
- recommended first-pass core:
  - none
- strongest deferred candidate:
  - `Leica Elmarit-R 135mm f/2.8`
- explicit `hold` candidate:
  - none
- literature clearly supports a real Leica R `135mm f/2.8 Elmarit-R` family
- literature also supports real internal marker structure:
  - `1-cam / 2-cam / 3-cam`
  - `Series VII`
  - `E55`
  - `ROM conversion`
- but local title support is still modest, entirely serial-number-driven, and lacks KRW-priced support

The safest round-1 answer is:

1. keep `Elmarit-R 135` closed for now
2. do not open any `core` or `hold` row
3. keep M-side `Elmarit-M 135`, `Tele-Elmar 135`, `APO-Telyt-M 135`, `Elmar 135`, `Hektor 135`, and classic `Telyt 135` as hard boundaries

## Literature / Reference Base

### Source A: Leica Wiki - `135mm f/2.8 Elmarit-R I`

Leica Wiki documents `135mm f/2.8 Elmarit-R I` with:

- order number:
  - `11111`
- production era:
  - `1964-1968`
- variants:
  - `1-cam`
  - `2-cam`
  - `3-cam`
- filter type:
  - `Series VII`
- accessories:
  - `ELPRO` close-focusing attachment

Reference:

- [Leica Wiki - 135mm f/2.8 Elmarit-R I](https://wiki.l-camera-forum.com/leica-wiki.en/index.php?title=135mm_f%2F2.8_Elmarit-R_I)

### Source B: Leica Wiki - `135mm f/2.8 Elmarit-R II`

Leica Wiki documents `135mm f/2.8 Elmarit-R II` with:

- order number:
  - `11211`
- production era:
  - `1968-1998`
- variants:
  - `ROM conversion`
- filter type:
  - `E55`
- inscriptions:
  - `LEITZ CANADA`
  - `LEITZ WETZLAR`
  - `E 55 ... LEICA`
- accessories:
  - `ELPRO` close-focusing attachment type 4

Reference:

- [Leica Wiki - 135mm f/2.8 Elmarit-R II](https://wiki.l-camera-forum.com/leica-wiki.en/index.php/135mm_f/2.8_Elmarit-R_II)

## Taxonomy Implication from Literature

Literature clearly supports:

- one real broad family:
  - `Leica Elmarit-R 135mm f/2.8`

Literature also supports meaningful internal structure:

- `1-cam / 2-cam / 3-cam`
- `Series VII`
- `E55`
- `ROM conversion`
- country inscription variation

However, literature alone is not enough to justify round-1 seed activation. The deciding question is whether local seller titles stabilize this family as a usable row. In the current raw pool, they do not yet do so strongly enough.

## Boundary Check

This family must remain separate from:

- `Leica Elmarit-M 135mm f/2.8`
- `Leica Tele-Elmar 135`
- `Leica APO-Telyt-M 135`
- `Leica Elmar 135`
- `Leica Hektor 135`
- classic `Leica Telyt 135`
- `Leica APO-Telyt-R 180 / 280`
- `Leica Summicron-R 90mm f/2`
- `Leica Elmarit-R 90mm f/2.8`
- `APO-Summicron-SL 90`
- `SL / L-mount` lenses
- third-party `135mm` lenses
- hood-only / cap / case / accessory-only listings

## Local Listing Evidence

Analysis base:

- `data/raw/raw_*.json`

### Broad retrieval behavior

Broad shorthand remains risky.

The following query-style surfaces do map to the family, but they do not show strong market depth:

- `elmarit-r 135`
- `elmarit r 135`
- `r 135 elmarit`
- `135 elmarit-r`
- `135mm f2.8 elmarit-r`
- `135mm f/2.8 elmarit-r`
- `r 135/2.8 elmarit`
- `leica r 135mm f2.8`
- `elmarit 135 r`

At local raw level, the visible family evidence converges on a small set of serial-number-led product titles:

- `LEICA 135mm F2.8 ELMARIT-R sn.2155`
- `LEICA 135mm F2.8 ELMARIT-R sn.2772`
- `LEICA 135mm F2.8 ELMARIT-R sn.2809`

Interpretation:

- this confirms the family is not imaginary in local data
- but seller wording is still narrow and not especially diverse
- broad `elmarit 135` should not be allowed to shape normalization in round 1 because too many adjacent Leica `135mm` families exist

### Clean local R-side pool

After restricting to explicit `135mm`, explicit R-side `Elmarit-R` wording, and excluding M-side `Elmarit-M 135`, `Tele-Elmar 135`, `APO-Telyt-M 135`, `Elmar 135`, `Hektor 135`, classic `Telyt 135`, SL, third-party, and accessory contamination, the usable pool becomes:

- clean local pool: `6`
- unique titles: `6`
- KRW-priced count: `0`
- KRW median: `not available`

Representative clean titles:

- `상품명 : LEICA 135mm F2.8 ELMARIT-R sn.2155 135mm Elmarit-R`
- `상품명 : LEICA 135mm F2.8 ELMARIT-R sn.2772 135mm Elmarit-R`
- `상품명 : LEICA 135mm F2.8 ELMARIT-R sn.2809 135mm Elmarit-R`
- `LEICA 135mm F2.8 ELMARIT-R sn.2155 135mm Elmarit-R`
- `LEICA 135mm F2.8 ELMARIT-R sn.2772 135mm Elmarit-R`
- `LEICA 135mm F2.8 ELMARIT-R sn.2809 135mm Elmarit-R`

Interpretation:

- the family is materially present in local data
- but the pool is still modest and serial-number-centric
- priced local support is absent
- this is stronger than a zero-signal family, but still thin for conservative seed activation

### Marker distribution inside local pool

Round-1 local support for internal markers is absent:

- `ROM`: `0`
- `cam`: `0` in seller-title wording
- `Series VII / E55 / E48`: `0`
- hood / case / boxed: `0`
- country / finish wording: `0`

Interpretation:

- literature supports real internal marker structure
- local seller-title support is only for the broad family, not for marker-level splits
- therefore internal rows are clearly out of scope for now

## Smoke Query Review

### Explicit R-side queries

Usable but still modest evidence appears in explicit product wording:

- `elmarit-r 135`
- `135mm f2.8 elmarit-r`
- `leica r 135mm f2.8`

Weak or absent direct repetition:

- `elmarit 135`
- `r 135/2.8 elmarit`
- `elmarit 135 r`

Interpretation:

- explicit R-side wording can find real family evidence
- but repetition is still not broad enough, and local pricing support is absent

### Broad shorthand risk

Unsafe broad shorthand:

- `elmarit 135`

Why unsafe:

- overlaps with `Elmarit-M 135`
- adjacent Leica `135mm` families are already dense
- can drift into `Tele-Elmar 135`, `APO-Telyt-M 135`, `Elmar 135`, `Hektor 135`, and `Telyt 135`

## Candidate Review

## Candidate 1: `Leica Elmarit-R 135mm f/2.8`

Pros:

- literature-real Leica R family
- literature supports long production history and real internal marker structure
- local titles do confirm multiple explicit R-side product instances

Cons:

- clean local pool is only `6`
- unique titles are only `6`
- local evidence is serial-number-led rather than richly repeated across seller wording styles
- KRW-priced local support is absent
- broad shorthand is highly exposed to adjacent Leica `135mm` contamination

Round-1 verdict:

- `deferred`

Reason:

- this family is real, but the local evidence is still thinner than recent R-side families that were safe to seed in round 1

## Hold Candidate Review

No explicit `hold` candidate is recommended in round 1.

Why:

- there is no narrower wording with stronger local repetition than the main family
- `ROM`, `cam`, and filter-thread markers are real metadata, not locally stable row candidates

## Overlay Elements

Keep these as overlay or deferred metadata only:

- `ROM`
- `cam version`
- `Series VII / E55 / E48`
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

These should not become separate rows in round 1.

## Deferred / Not-for-Round-1

Do not open separate rows for:

- `ROM`
- `cam version`
- `Series VII / E55 / E48`
- `filter thread`

Do not use as strong shaping aliases:

- `elmarit 135`

Reason:

- these are either under-supported internal markers or broad shorthand with strong Leica `135mm` family contamination risk

## Out-of-Family Boundary

Must remain outside this family:

- `Leica Elmarit-M 135mm f/2.8`
- `Leica Tele-Elmar 135`
- `Leica APO-Telyt-M 135`
- `Leica Elmar 135`
- `Leica Hektor 135`
- classic `Leica Telyt 135`
- `Leica APO-Telyt-R 180 / 280`
- `Leica Summicron-R 90mm f/2`
- `Leica Elmarit-R 90mm f/2.8`
- `APO-Summicron-SL 90`
- `SL / L-mount` lenses
- accessory-only listings
- third-party `135mm` lenses

## Final Round-1 Judgment

Immediate round-1 answer:

- immediate core candidate:
  - `0`
- hold candidate:
  - none

Strongest deferred candidate:

- `Leica Elmarit-R 135mm f/2.8`

Round-1 decision:

- `seed 보류`

Why:

1. literature clearly confirms a real Leica R `135mm` Elmarit family
2. local titles do show real family presence
3. but the pool is still modest and serial-number-led
4. priced local support is absent
5. broad `elmarit 135` is too exposed to adjacent Leica `135mm` family contamination

## Recommendation for Next Round

Do not add a seed row yet.

Only revisit if one of the following improves:

- more clean local `Elmarit-R 135` titles appear beyond the current serial-number-driven set
- KRW-priced local rows accumulate
- explicit `R 135/2.8 Elmarit` wording stabilizes independently from other Leica `135mm` families

If future evidence improves, the next candidate to open would still be:

- `Leica Elmarit-R 135mm f/2.8`

But round-1 should keep the family closed.
