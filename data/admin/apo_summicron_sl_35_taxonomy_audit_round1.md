# APO-Summicron-SL 35 Taxonomy Audit - Round 1

Date: 2026-05-21

Scope: audit-only review for the Leica `APO-Summicron-SL 35` family. This round does not add seed rows, does not modify `entities/*.json`, does not modify `canonical_entities_index.json`, and does not change classifier/query/search behavior, ranking, or UI.

## Executive Summary

`APO-Summicron-SL 35` is literature-real, and round-1 local evidence is strong enough to identify one narrow immediate seed candidate for a future seed round.

Round-1 conclusion:

- immediate recommended `core` candidate count: `1`
- recommended first-pass core:
  - `Leica APO-Summicron-SL 35mm f/2 ASPH`
- explicit `hold` candidate:
  - none
- literature clearly supports one real Leica SL `35mm f/2 ASPH APO-Summicron-SL` family
- local title support is stable:
  - repeated `SL 35/2 APO Summicron ASPH`
  - repeated `35mm F2 ASPH APO-SUMMICRON-SL`
- priced observations exist in KRW, though not deeply
- broad `apo summicron 35` / `summicron 35` / `leica sl 35` / `35 apo` / `35 cron` retrieval remains unsafe and must not be hard-pinned

Important correction from round 1:

- literature also supports a separate adjacent family:
  - `Leica Summicron-SL 35mm f/2 ASPH`
- therefore `APO-Summicron-SL 35` must not be merged with non-APO `Summicron-SL 35`
- even `summicron-sl 35` / `summicron sl 35` shorthand is not automatically safe for the APO family

The safest round-1 answer is:

1. recognize `Leica APO-Summicron-SL 35mm f/2 ASPH` as an immediate future seed candidate
2. do not open any internal version row
3. keep `APO`, `ASPH`, `E67`, filter-thread markers, and hood or case bundle wording as overlay or deferred metadata
4. keep adjacent non-APO `Summicron-SL 35`, M/R `35mm` families, neighboring SL prime and zoom families, and third-party L-mount `35mm` primes as hard boundaries

## Literature / Reference Base

### Source A: Leica Camera technical specification

Leica Camera documents:

- `APO-Summicron-SL 35 f/2 ASPH.`
- order number:
  - `11184`
- bayonet / format:
  - `L-Mount`, full-frame `35mm` format
- filter mount:
  - `E67`
- working range:
  - `0.27 m to infinity`

Reference:

- [Leica Camera - Technical Specifications - APO-Summicron-SL 35 f/2 ASPH.](https://leica-camera.com/en-US/photography/lenses/sl/apo-summicron-sl-35mm-f2-asph/technical-specification)

### Source B: Leica Camera product page

Leica Camera product literature documents:

- `APO-Summicron-SL 35 f/2 ASPH.`
- SL-System reportage / wide-normal prime positioning
- explicit premium `35mm` role inside the APO-Summicron-SL prime line

Reference:

- [Leica Camera - APO-Summicron-SL 35 f/2 ASPH.](https://leica-camera.com/en-US/photography/lenses/sl/apo-summicron-sl-35mm-f2-asph)

### Source C: Leica technical data PDF

Leica technical data sheet documents:

- `APO-Summicron-SL 35 f/2 ASPH.`
- order no. `11184`
- optical design:
  - `13 / 11`
- filter mount:
  - `E67`
- no separate internal row-level variant is documented in round 1

Reference:

- [Leica Tech Data PDF - APO-Summicron-SL 35 f/2 ASPH.](https://leica-camera.com/sites/default/files/pm-55403-11184_Datenblatt_APO_Summicron-SL-35mm-ASPH_en.pdf)

### Source D: adjacent non-APO Leica SL 35 family

Leica Camera also documents a separate adjacent family:

- `Summicron-SL 35 f/2 ASPH.`
- order no.:
  - `11192`
- this is literature-real and must not be merged into the APO family

Reference:

- [Leica Camera - Technical Specifications - Summicron-SL 35 f/2 ASPH.](https://leica-camera.com/en-int/photography/lenses/sl/summicron-sl-35mm-f2-asph/technical-specification)

## Taxonomy Implication from Literature

Literature clearly supports:

- one real target family:
  - `Leica APO-Summicron-SL 35mm f/2 ASPH`

Literature also clearly supports one adjacent non-target family:

- `Leica Summicron-SL 35mm f/2 ASPH`

That means:

- `APO-Summicron-SL 35` is real
- non-APO `Summicron-SL 35` is also real
- they must remain separate

Literature also supports metadata structure around:

- `APO`
- `ASPH`
- `E67`
- filter-thread marker
- hood / cap / case / packaging ecosystem

These are real markers, but round-1 does not justify opening separate rows for them.

## Boundary Check

This family must remain separate from:

- `Leica Summicron-M 35mm f/2`
- `Leica Summilux-M 35mm f/1.4`
- `Leica Summaron 35mm`
- `Leica Summicron-R 35mm f/2`
- `Leica Summilux-R 35mm f/1.4`
- `Leica Elmarit-R 35mm f/2.8`
- `Leica Summicron-SL 35mm f/2 ASPH`
- `Leica APO-Summicron-SL 50mm f/2 ASPH`
- `Leica APO-Summicron-SL 75mm f/2 ASPH`
- `Leica APO-Summicron-SL 90mm f/2 ASPH`
- `Leica Super-Vario-Elmar-SL 16-35mm f/3.5-4.5 ASPH`
- `Leica Vario-Elmarit-SL 24-90mm f/2.8-4 ASPH`
- Sigma / Panasonic / Lumix `35mm` L-mount primes
- accessory-only listings

## Local Listing Evidence

Analysis base:

- `data/normalized/normalized_latest.json`
- `results.json`
- `data/sold_items.json`

### Broad retrieval behavior

Broad shorthand is risky.

Within the wider `apo summicron / 35 / sl` field, distinct neighboring or contaminating lines appear immediately:

- `Leica Summicron-M 35mm f/2`
- `Leica Summilux-M 35mm f/1.4`
- `Leica Summaron 35mm`
- `Leica Summicron-R 35mm f/2`
- `Leica Summilux-R 35mm f/1.4`
- `Leica Elmarit-R 35mm f/2.8`
- `Leica Summicron-SL 35mm f/2 ASPH`
- `LEICA 50mm F2 ASPH APO-SUMMICRON-SL`
- `LEICA 75mm F2 APO-SUMMICRON-SL`
- `LEICA 90mm F2 ASPH APO-SUMMICRON-SL`
- `Leica SL 16-35mm f3.5-4.5 Super-Vario-Elmar`
- `Leica SL 24-90mm f2.8-4 Vario-Elmarit`
- Sigma / Panasonic / Lumix `35mm` L-mount prime families

Interpretation:

- broad `apo summicron 35`
- broad `summicron 35`
- broad `leica sl 35`
- broad `35 apo`
- broad `35 cron`

are not safe shaping aliases in round 1 because they can drift into:

- M `35mm` Summicron / Summilux / Summaron families
- R `35mm` Summicron / Summilux / Elmarit families
- adjacent non-APO `Summicron-SL 35`
- neighboring SL `50 / 75 / 90 / 16-35 / 24-90` families
- third-party L-mount `35mm` primes
- accessory-only listings

### Clean local SL-side pool

After restricting to explicit APO-side `35mm`, explicit SL-side wording, and excluding:

- non-APO `Summicron-SL 35`
- M-side `35mm`
- R-side `35mm`
- neighboring SL `50 / 75 / 90`
- neighboring SL `16-35 / 24-90`
- third-party
- accessory contamination

the usable local pool becomes:

- clean local pool: `26`
- unique titles: `5`
- KRW-priced count: `2`
- KRW median: `3,850,000 KRW`

Representative clean titles:

- `[위탁] SL 35/2 APO Summicron ASPH (Black)`
- `[중고] SL 35/2 APO Summicron ASPH (Black)`
- `LEICA 35mm F2 ASPH APO-SUMMICRON-SL sn.4720`
- `LEICA 35mm F2 ASPH APO-SUMMICRON-SL sn.4811`
- `LEICA 35mm F2 ASPH APO-SUMMICRON-SL sn.4719`

Observed KRW price points:

- `3,800,000 KRW`
- `3,900,000 KRW`

Interpretation:

- local wording is family-correct
- the pool is source-clustered, but the family shape is explicit and stable
- priced support exists, though it is not deep
- this is still strong enough for one narrow future core row, not for any broader aliasing

### Adjacent non-APO SL 35 implication

Reviewed local rows also surface the adjacent non-APO family:

- `Used Leica Summicron-SL 35mm f/2 ASPH`
- `[중고] Leica SL2 with Summicron-SL 35mm f/2 ASPH`

These should be treated as evidence that adjacent non-APO `Summicron-SL 35` is live in the local field, not as support for the APO family.

This makes:

- `summicron-sl 35`
- `summicron sl 35`

unsafe as APO-family shaping aliases.

### Accessory / bundle contamination note

One sold row also appears as:

- `Used Leica APO-Summicron-SL 35mm f/2 ASPH - UVa Filter`

That row is family-relevant, but the bundled filter wording is better treated as accessory or overlay contamination in round 1, not as justification for an extra row.

## Round-1 Recommendation

### Immediate `core` candidate count

- `1`

### Recommended first-pass `core`

- `Leica APO-Summicron-SL 35mm f/2 ASPH`

### Explicit `hold` candidates

- none

## Why not open more than one row?

Because round-1 literature and local evidence both converge on one stable SL-side `35mm f/2 ASPH` APO prime family, while:

- `APO`
- `ASPH`
- `E67`
- filter-thread marker
- hood / case / packaging wording

remain below row level and do not justify separate row creation.

The safest round-1 seed shape would be one narrow core row only.

## Overlay / Deferred Metadata

Keep below row level:

- `APO`
- `ASPH`
- `E67`
- filter-thread marker
- hood included
- cap included
- boxed
- case included
- packaging
- finish / country style metadata

Do not open separate rows for:

- `APO`-only split
- `ASPH`-only split
- `E67` split
- hood / case / boxed bundle rows

## Out-of-Family Boundaries

Do not merge with:

- `Summicron-M 35`
- `Summilux-M 35`
- `Summaron 35`
- `Summicron-R 35`
- `Summilux-R 35`
- `Elmarit-R 35`
- `Summicron-SL 35`
- `APO-Summicron-SL 50`
- `APO-Summicron-SL 75`
- `APO-Summicron-SL 90`
- `Super-Vario-Elmar-SL 16-35`
- `Vario-Elmarit-SL 24-90`
- Sigma / Panasonic / Lumix `35mm`
- accessory-only listings

## Seed-Round Readiness

- next seed round:
  - `가능`

The future seed should open one narrow core row only:

- `Leica APO-Summicron-SL 35mm f/2 ASPH`

Do not treat broad `summicron` or adjacent non-APO `Summicron-SL 35` wording as APO-family-safe shorthand.

## Validation

Validation run after this audit-only report update:

- `python3 tests/test_normalization_admin.py`
  - `ok`
- `python3 -m py_compile normalization_admin.py golden_set.py tests/test_normalization_admin.py`
  - `ok`
- `python3 golden_set.py`
  - `132/132`
