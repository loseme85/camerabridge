# APO-Summicron-SL 28 Taxonomy Audit - Round 1

Date: 2026-05-23

Scope: audit-only review for the Leica `APO-Summicron-SL 28` family. This round does not add seed rows, does not modify `entities/*.json`, does not modify `canonical_entities_index.json`, and does not change classifier/query/search behavior, ranking, or UI.

## Executive Summary

`APO-Summicron-SL 28` is literature-real, and round-1 local evidence is strong enough to identify one narrow immediate seed candidate for a future seed round.

Round-1 conclusion:

- immediate recommended `core` candidate count: `1`
- recommended first-pass core:
  - `Leica APO-Summicron-SL 28mm f/2 ASPH`
- explicit `hold` candidate:
  - none
- literature clearly supports one real Leica SL `28mm f/2 ASPH APO-Summicron-SL` family
- local title support is stable:
  - repeated `SL 28/2 APO Summicron ASPH`
  - repeated `28mm F2 ASPH APO-SUMMICRON-SL`
- priced observations exist in KRW
- broad `apo summicron 28` / `summicron 28` / `leica sl 28` / `28 apo` / `28 cron` retrieval remains unsafe and must not be hard-pinned

The safest round-1 answer is:

1. recognize `Leica APO-Summicron-SL 28mm f/2 ASPH` as an immediate future seed candidate
2. do not open any internal version row
3. keep `APO`, `ASPH`, `E67`, filter-thread markers, and hood or case bundle wording as overlay or deferred metadata
4. keep M/R `28mm` families, neighboring SL prime and zoom families, Leica Q fixed-lens `28mm` bodies, and third-party L-mount `24 / 28 / 35mm` primes as hard boundaries

## Literature / Reference Base

### Source A: Leica Camera technical specification

Leica Camera documents:

- `APO-Summicron-SL 28 f/2 ASPH.`
- order number:
  - `11183`
- bayonet / format:
  - `L-Mount`, full-frame `35mm` format
- filter mount:
  - `E67`
- working range:
  - `0.24 m to infinity`

Reference:

- [Leica Camera - Technical Specifications - APO-Summicron-SL 28 f/2 ASPH.](https://leica-camera.com/en-int/photography/lenses/sl/apo-summicron-sl-28-f2-asph-black-finish/technical-specification)

### Source B: Leica Camera product page

Leica Camera product literature documents:

- `APO-Summicron-SL 28 f/2 ASPH.`
- explicit SL-system wide prime positioning
- dedicated `28mm` role distinct from the `35 / 50 / 75 / 90` APO-Summicron-SL line extensions

Reference:

- [Leica Camera - APO-Summicron-SL 28 f/2 ASPH.](https://leica-camera.com/en-US/photography/lenses/sl/apo-summicron-sl-28-f2-asph-black-finish)

### Source C: Leica technical data PDF

Leica technical data sheet documents:

- `APO-Summicron-SL 28 f/2 ASPH.`
- order no. `11183`
- optical design:
  - `13 / 10`
- filter mount:
  - `E67`
- no separate internal row-level variant is documented in round 1

Reference:

- [Leica Tech Data PDF - APO-Summicron-SL 28 f/2 ASPH.](https://leica-camera.com/sites/default/files/pm-59022-Tech_Data_APO-Summicron-SL_28_EN.pdf)

### Source D: Leica Camera press release

Leica Camera press literature explicitly places this lens inside the APO-Summicron-SL series and identifies it as the first true wide-angle lens in that series.

Reference:

- [Leica Camera - Press Release - APO-Summicron-SL 28 f/2 ASPH.](https://leica-camera.com/es-MX/Company/Press-Centre/Press-Releases/2021/Press-Release-The-APO-Summicron-SL-28-f-2-ASPH.-A-wide-angle-lens-with-state-of-the-art-technology-for-the-Leica-SL-System)

## Taxonomy Implication from Literature

Literature clearly supports:

- one real target family:
  - `Leica APO-Summicron-SL 28mm f/2 ASPH`

Literature also supports metadata structure around:

- `APO`
- `ASPH`
- `E67`
- filter-thread marker
- hood / cap / case / packaging ecosystem

These are real markers, but round-1 does not justify opening separate rows for them.

## Boundary Check

This family must remain separate from:

- `Leica Summicron-M 28mm f/2 ASPH`
- `Leica Summilux-M 28mm f/1.4 ASPH`
- `Leica Elmarit-M 28mm f/2.8`
- `Leica Summaron 28mm`
- `Leica Elmarit-R 28mm`
- `Leica APO-Summicron-SL 35mm f/2 ASPH`
- `Leica APO-Summicron-SL 50mm f/2 ASPH`
- `Leica APO-Summicron-SL 75mm f/2 ASPH`
- `Leica APO-Summicron-SL 90mm f/2 ASPH`
- `Leica Super-Vario-Elmar-SL 16-35mm f/3.5-4.5 ASPH`
- `Leica Vario-Elmarit-SL 24-90mm f/2.8-4 ASPH`
- Leica `Q / Q2 / Q3` fixed-lens `28mm` bodies
- Sigma / Panasonic / Lumix `24 / 28 / 35mm` L-mount primes
- accessory-only listings

## Local Listing Evidence

Analysis base:

- `data/normalized/normalized_latest.json`
- `results.json`
- `data/sold_items.json`

### Broad retrieval behavior

Broad shorthand is risky.

Within the wider `apo summicron / 28 / sl` field, distinct neighboring or contaminating lines appear immediately:

- `Leica Summicron-M 28mm`
- `Leica Summilux-M 28mm`
- `Leica Elmarit-M 28mm`
- `Leica Summaron 28mm`
- `Leica Elmarit-R 28mm`
- `Leica APO-Summicron-SL 35mm`
- `Leica APO-Summicron-SL 50mm`
- `Leica APO-Summicron-SL 75mm`
- `Leica APO-Summicron-SL 90mm`
- `Leica SL 16-35mm f3.5-4.5 Super-Vario-Elmar`
- `Leica SL 24-90mm f2.8-4 Vario-Elmarit`
- `Leica Q2`
- `Leica Q3`
- Sigma / Panasonic / Lumix `24 / 28 / 35mm` L-mount primes

Interpretation:

- broad `apo summicron 28`
- broad `summicron 28`
- broad `leica sl 28`
- broad `28 apo`
- broad `28 cron`

are not safe shaping aliases in round 1 because they can drift into:

- M `28mm` Summicron / Summilux / Elmarit / Summaron families
- R `28mm` Elmarit family
- adjacent SL `35 / 50 / 75 / 90 / 16-35 / 24-90` families
- Leica `Q / Q2 / Q3` fixed-lens `28mm` bodies
- third-party L-mount `24 / 28 / 35mm` primes
- accessory-only listings

### Clean local SL-side pool

After restricting to explicit APO-side `28mm`, explicit SL-side wording, and excluding:

- M-side `28mm`
- R-side `28mm`
- neighboring SL `35 / 50 / 75 / 90`
- neighboring SL `16-35 / 24-90`
- Leica Q-series `28mm` bodies
- third-party
- accessory contamination

the usable local pool becomes:

- clean local pool: `6`
- unique titles: `3`
- KRW-priced count: `6`
- KRW median: `4,790,000 KRW`

Representative clean titles:

- `[중고] SL 28/2 APO Summicron ASPH (Black)`
- `[위탁] SL 28/2 APO Summicron ASPH (Black)`
- `LEICA 28mm F2 ASPH APO-SUMMICRON-SL sn.4806`

Observed KRW price points:

- `3,800,000 KRW`
- `3,900,000 KRW`
- `4,400,000 KRW`
- `5,180,000 KRW`
- `5,400,000 KRW`

Interpretation:

- local wording is family-correct
- the pool is source-clustered, but the family shape is explicit and repeated
- priced support exists in KRW
- this is strong enough for one narrow future core row, not for broader aliasing

## Round-1 Recommendation

### Immediate `core` candidate count

- `1`

### Recommended first-pass `core`

- `Leica APO-Summicron-SL 28mm f/2 ASPH`

### Explicit `hold` candidates

- none

## Why not open more than one row?

Because round-1 literature and local evidence both converge on one stable SL-side `28mm f/2 ASPH` APO prime family, while:

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

- `Summicron-M 28`
- `Summilux-M 28`
- `Elmarit-M 28`
- `Summaron 28`
- `Elmarit-R 28`
- `APO-Summicron-SL 35`
- `APO-Summicron-SL 50`
- `APO-Summicron-SL 75`
- `APO-Summicron-SL 90`
- `Super-Vario-Elmar-SL 16-35`
- `Vario-Elmarit-SL 24-90`
- Leica `Q / Q2 / Q3`
- Sigma / Panasonic / Lumix `24 / 28 / 35mm`
- accessory-only listings

## Seed-Round Readiness

- next seed round:
  - `가능`

The future seed should open one narrow core row only:

- `Leica APO-Summicron-SL 28mm f/2 ASPH`

Do not treat broad `summicron`, neighboring SL prime families, or Leica Q-series `28mm` wording as family-safe shorthand.

## Validation

Validation run after this audit-only report update:

- `python3 tests/test_normalization_admin.py`
  - `ok`
- `python3 -m py_compile normalization_admin.py golden_set.py tests/test_normalization_admin.py`
  - `ok`
- `python3 golden_set.py`
  - `132/132`
