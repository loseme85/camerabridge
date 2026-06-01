# APO-Macro-Elmarit-R 100 Taxonomy Audit - Round 1

Date: 2026-05-13

Scope: audit-only review for the Leica `APO-Macro-Elmarit-R 100` family. This round does not add seed rows, does not modify `entities/*.json`, does not modify `canonical_entities_index.json`, and does not change classifier/query/search behavior, ranking, or UI.

## Executive Summary

`APO-Macro-Elmarit-R 100` is seedable, but only as one narrow R-side family anchor in round 1.

Round-1 conclusion:

- immediate recommended `core` candidate count: `1`
- recommended first-pass core:
  - `Leica APO-Macro-Elmarit-R 100mm f/2.8`
- explicit `hold` candidate:
  - none
- literature documents real internal marker structure:
  - `ROM`
  - `E60`
  - `ELPRO 1:2-1:1`
  - tripod collar / accessory ecosystem
- but local seller-title support is not strong enough to open separate rows for those markers
- broad `macro elmarit 100` and `apo macro 100` should stay outside the initial alias surface because they are not sufficiently anchored to Leica R and can expand into adjacent Leica macro and third-party contamination

The safest round-1 answer is:

1. open one explicit R-side family row
2. keep `ROM`, `E60`, `ELPRO`, and bundle differences below row level
3. do not let broad macro shorthand shape the initial alias surface

## Literature / Reference Base

### Source A: Leica Classic - `APO-Macro-Elmarit 2,8/100mm`

Leica Classic presents the family under `APO-Macro-Elmarit 2,8/100mm` with order numbers `11210/11352`.

Reference:

- [Leica Classic - APO-Macro-Elmarit 2,8/100mm](https://classic.leica-camera.com/en/Leica-Systems/R-System/Lenses/Tele-Lenses/APO-Macro-Elmarit-2-8-100mm/)

### Source B: Leica Wiki - `100mm f/2.8 APO-Macro-Elmarit-R`

Leica Wiki documents `100mm f/2.8 APO-Macro-Elmarit-R` with:

- order numbers:
  - `11210`
  - `11352-ROM`
- production era:
  - `1987-2009`
- filter mount / hood:
  - `E60`
  - built-in telescopic hood
- accessories:
  - `ELPRO 1:2-1:1`
  - rotating tripod collar `STA-1`

Reference:

- [Leica Wiki - 100mm f/2.8 APO-Macro-Elmarit-R](https://wiki.l-camera-forum.com/leica-wiki.en/index.php?title=100mm_f%2F2.8_APO-Macro-Elmarit-R)

### Boundary literature notes

Separate adjacent families are also clearly documented in Leica literature:

- `100mm f/4 Macro-Elmar-R`
- `60mm f/2.8 Macro-Elmarit-R`

References:

- [Leica Classic - Macro-Elmar-R 4/100mm](https://classic.leica-camera.com/en/Leica-Systems/R-System/Lenses/Tele-Lenses/Macro-Elmar-R-4-100mm/)
- [Leica Wiki - 100mm f/4 Macro-Elmar-R](https://wiki.l-camera-forum.com/leica-wiki.en/index.php/100mm_f/4_Macro-Elmar-R)
- [Leica Wiki - 60mm f/2.8 Macro-Elmarit-R](https://wiki.l-camera-forum.com/leica-wiki.en/index.php/60mm_f/2.8_Macro-Elmarit-R)

## Taxonomy Implication from Literature

Literature clearly supports:

- one real broad family:
  - `Leica APO-Macro-Elmarit-R 100mm f/2.8`

and also clearly supports internal markers:

- `ROM`
- `E60`
- `ELPRO 1:2-1:1`

Literature does not, by itself, justify separate seed rows for those markers in round 1. The deciding question is whether local titles split those variants cleanly enough. In this round, they do not.

## Boundary Check

This family must remain separate from:

- `Leica Macro-Elmar-R 100mm f/4`
- `Leica Macro-Elmarit-R 60mm f/2.8`
- `Leica Elmarit-R 90mm f/2.8`
- `Leica Summicron-R 90mm f/2`
- `Leica APO-Summicron-R 90mm f/2 ASPH`
- `Leica APO-Telyt-R 180 / 280`
- `SL / L-mount` macro or `90mm` lenses
- third-party `90 / 100 / 105mm` macro lenses
- `ELPRO`-only / adapter-only / hood-only / cap / case / accessory-only listings

## Local Listing Evidence

Analysis base:

- `data/raw/raw_*.json`

### Broad retrieval behavior

Broad shorthand retrieval is weak and should not define the initial family alias surface.

Observed direct query-style support for:

- `macro elmarit 100`
- `apo macro 100`
- `apo elmarit 100 r`

is effectively absent in the simple local title pool.

At the same time, explicit product-name style titles for the real family do recur:

- `Leica R 100mm f2.8 APO-Macro-Elmarit Black`
- `Leica R 100mm f2.8 APO-Macro-Elmarit ROM Black`
- `LEICA 100mm F2.8 APO-MACRO-ELMARIT-R sn.3561`
- `LEICA R100mm F2.8 (ROM) APO-MACRO-ELMARIT-R sn.3890`
- `LEICA 100mm F2.8 ROM APO-MACRO-ELMARIT-R ELPRO 1:2-1:1 ...`

Interpretation:

- local seller style converges more on product-name-first wording than on neat query-alias wording
- the family itself is still stable enough for one explicit R-side row
- broad shorthand should not be allowed to widen the initial alias surface

### Clean local R-side pool

After restricting to explicit `100mm` plus explicit R-side `APO-Macro-Elmarit` wording and deduplicating repeated snapshots by normalized title plus price, the usable local pool becomes:

- clean local pool: `11`
- unique titles: `10`
- KRW-priced count: `3`
- KRW median: `1,850,000`

Representative clean titles:

- `Leica R 100mm f2.8 APO-Macro-Elmarit Black`
- `Leica R 100mm f2.8 APO-Macro-Elmarit ROM Black`
- `LEICA 100mm F2.8 rom APO-MACRO-ELMARIT-R sn.3830`
- `LEICA 100mm F2.8 APO-MACRO-ELMARIT-R sn.3561`
- `LEICA R100mm F2.8 (ROM) APO-MACRO-ELMARIT-R sn.3890`
- `LEICA 100mm F2.8 ROM APO-MACRO-ELMARIT-R ELPRO 1:2-1:1 sn.1654 / 6854`

Interpretation:

- this is enough to confirm the family is materially present in local market data
- title repetition converges on one practical Leica R APO Macro lens intent
- priced rows are not huge, but they are coherent enough for one family-level `core`
- local support is still not specific enough to separate `ROM`, `E60`, or `ELPRO included` into separate rows

### Marker distribution inside local pool

Round-1 local support for internal split markers is partial but still not row-level:

- `ROM`: repeated
- `E60`: not visibly repeated in clean local titles
- `ELPRO`: appears as bundled wording, but not as a stable standalone row signal
- `hood / case / boxed`: not meaningfully repeated
- `cam`: not visibly repeated in clean local titles

Interpretation:

- local titles confirm that `ROM` and `ELPRO` can appear
- literature confirms broader internal structure
- but local repetition is not strong enough to justify separate seed rows for those markers

## Smoke Query Review

### Explicit R-side queries

Strong / usable family evidence appears in product-name-heavy and focal-length-first title patterns:

- `100mm f2.8 apo macro elmarit-r`
- `leica r 100mm f2.8 apo macro`
- explicit `APO-MACRO-ELMARIT-R` title forms

Weak or absent direct local repetition:

- `apo-macro-elmarit-r 100`
- `apo macro elmarit r 100`
- `apo macro elmarit-r 100`
- `r 100 apo macro elmarit`
- `100 apo macro elmarit-r`
- `r 100/2.8 apo macro elmarit`
- `apo elmarit 100 r`
- `macro elmarit 100`
- `apo macro 100`

Interpretation:

- seller wording is a bit rougher than the ideal alias surface
- but the family itself is stable enough for a single explicit R-side row
- the initial alias set should prefer explicit `R` / `APO-Macro-Elmarit-R` wording rather than broad shorthand

### Broad shorthand risk

Unsafe broad shorthand:

- `macro elmarit 100`
- `apo macro 100`

Why unsafe:

- insufficient R-side anchoring in local seller wording
- can expand into generic macro intent
- can overlap with non-Leica and adjacent Leica macro families

## Candidate Review

## Candidate 1: `Leica APO-Macro-Elmarit-R 100mm f/2.8`

### Literature basis

Strong.

Both Leica Classic and Leica Wiki support a real R-side `100mm f/2.8 APO-Macro-Elmarit-R` family.

### Local title support

Good enough for family-level seeding.

The clean pool is not enormous, but it is clearly thicker than a one-off hypothesis and converges on the same R-side APO macro lens intent.

### Price behavior

Good enough for family-level seeding.

The priced local pool is modest but coherent, and there is no evidence that the broad family is splitting into incompatible price bands at row level.

### Search-intent stability

Good enough for `core` when wording is explicit about `R`, `APO-Macro-Elmarit-R`, or a clear `100mm f/2.8 APO` macro pattern.

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
- `cam version`
- `E60`
- `filter thread`
- `Elpro included`
- `macro adapter included`
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
- `cam version`
- `E60`
- `filter thread`
- `ELPRO 1:2-1:1`
- `macro adapter`

Do not use as strong shaping aliases:

- `macro elmarit 100`
- `apo macro 100`

Reason:

- these are either under-supported internal markers or broad shorthand with weak Leica R anchoring

## Out-of-Family Boundary

Must remain outside this family:

- `Leica Macro-Elmar-R 100mm f/4`
- `Leica Macro-Elmarit-R 60mm f/2.8`
- `Leica Elmarit-R 90mm f/2.8`
- `Leica Summicron-R 90mm f/2`
- `Leica APO-Summicron-R 90mm f/2 ASPH`
- `Leica APO-Telyt-R 180 / 280`
- `SL / L-mount` macro or `90mm` lenses
- accessory-only listings
- third-party `90 / 100 / 105mm` macro lenses

## Final Round-1 Judgment

Immediate round-1 answer:

- immediate core candidate:
  - `1`
- hold candidate:
  - none

Recommended first-pass core:

- `Leica APO-Macro-Elmarit-R 100mm f/2.8`

Round-1 decision:

- seedable as one narrow `core`

Why:

1. literature clearly confirms a real Leica R APO macro family
2. local title support is materially present rather than hypothetical
3. priced rows are modest but coherent enough for one family-level row
4. local support is still not strong enough to justify marker-level subrows

## Recommendation for Next Round

If the project opens this family in seed form, keep the first pass extremely narrow:

- add only `Leica APO-Macro-Elmarit-R 100mm f/2.8`

Do not add separate rows for:

- `ROM`
- `E60`
- `ELPRO`
- `macro adapter`
- hood / box / case / condition bundles

Do not use broad shorthand such as:

- `macro elmarit 100`
- `apo macro 100`

The next seed round should open one explicit R-side `core` and keep all internal markers below row level.
