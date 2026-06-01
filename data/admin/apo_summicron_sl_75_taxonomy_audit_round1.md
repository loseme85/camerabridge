# APO-Summicron-SL 75 Taxonomy Audit - Round 1

Date: 2026-05-21

Scope: audit-only review for the Leica `APO-Summicron-SL 75` family. This round does not add seed rows, does not modify `entities/*.json`, does not modify `canonical_entities_index.json`, and does not change classifier/query/search behavior, ranking, or UI.

## Executive Summary

`APO-Summicron-SL 75` is literature-real, and round-1 local evidence is strong enough to identify one narrow immediate seed candidate for a future seed round.

Round-1 conclusion:

- immediate recommended `core` candidate count: `1`
- recommended first-pass core:
  - `Leica APO-Summicron-SL 75mm f/2 ASPH`
- explicit `hold` candidate:
  - none
- literature clearly supports one real Leica SL `75mm f/2 ASPH APO-Summicron-SL` family
- local title support is stable:
  - repeated `SL APO 75/2 Summicron ASPH`
  - repeated `75mm F2 APO-SUMMICRON-SL`
  - repeated `75mm F2 ASPH APO-SUMMICRON-SL`
- priced observations exist in KRW and cluster in a coherent band
- broad `apo summicron 75` / `summicron 75` / `leica sl 75` / `75 apo` / `75 cron` retrieval remains unsafe and must not be hard-pinned

The safest round-1 answer is:

1. recognize `Leica APO-Summicron-SL 75mm f/2 ASPH` as an immediate future seed candidate
2. do not open any internal version row
3. keep `APO`, `ASPH`, `E67`, filter-thread markers, and hood or case bundle wording as overlay or deferred metadata
4. keep M-side `75mm`, neighboring SL primes, SL `90-280`, `Summilux-R 80`, and third-party L-mount short tele primes as hard boundaries

## Literature / Reference Base

### Source A: Leica Camera technical specification

Leica Camera documents:

- `APO-Summicron-SL 75 f/2 ASPH.`
- order number:
  - `11178`
- bayonet / format:
  - `L-Mount`, full-frame `35mm` format
- filter mount:
  - `E67`
- working range:
  - `0.5 m to infinity`

Reference:

- [Leica Camera - Technical Specifications - APO-Summicron-SL 75 f/2 ASPH.](https://leica-camera.com/en-int/photography/lenses/sl/apo-summicron-sl-75mm-f2-asph-black/technical-specification)

### Source B: Leica Camera product page

Leica Camera product literature documents:

- `APO-Summicron-SL 75 f/2 ASPH.`
- standard-to-short-tele transition placement inside the SL prime line
- explicit paired launch with:
  - `APO-Summicron-SL 90 f/2 ASPH.`

Reference:

- [Leica Camera - APO-Summicron-SL 75 f/2 ASPH.](https://leica-camera.com/en-DK/photography/lenses/sl/apo-summicron-sl-75mm-f2-asph-black)

### Source C: Leica technical data PDF

Leica technical data sheet documents:

- `APO-Summicron-SL 75 f/2 ASPH.`
- order no. `11178`
- optical design:
  - `11 / 9`
- filter mount:
  - `E67`
- no separate internal row-level variant is documented in round 1

Reference:

- [Leica Tech Data PDF - APO-Summicron-SL 75 f/2 ASPH.](https://leica-camera.com/sites/default/files/pm-55397-11178_Datenblatt_APO-Summicron-SL-75mm-ASPH_e.pdf)

## Taxonomy Implication from Literature

Literature clearly supports:

- one real family:
  - `Leica APO-Summicron-SL 75mm f/2 ASPH`

No separate aperture-distinct Leica SL `75mm` family was confirmed in primary literature for this round.

Literature also supports metadata structure around:

- `APO`
- `ASPH`
- `E67`
- filter-thread marker
- hood / cap / case / packaging ecosystem

These are real markers, but round-1 does not justify opening separate rows for them.

## Boundary Check

This family must remain separate from:

- `Leica Summicron-M 75mm f/2`
- `Leica Summilux-M 75mm f/1.4`
- `Leica Noctilux-M 75mm f/1.25`
- `Leica APO-Summicron-SL 90mm f/2 ASPH`
- `Leica APO-Summicron-SL 50mm f/2 ASPH`
- `Leica APO-Vario-Elmarit-SL 90-280mm f/2.8-4`
- `Leica Summilux-R 80mm f/1.4`
- M / R `75mm / 80mm` families
- Sigma / Panasonic / Lumix `75mm / 85mm / 90mm` L-mount primes
- accessory-only listings

## Local Listing Evidence

Analysis base:

- `data/normalized/normalized_latest.json`
- `data/derived/results_resolved_v2.json`
- `data/sold_items.json`

### Broad retrieval behavior

Broad shorthand is risky.

Within the wider `apo summicron / 75 / sl` field, distinct neighboring or contaminating rows appear immediately:

- `Leica M 75mm f2 APO-Summicron ASPH 6bit Black`
- `LEICA 90mm F2 ASPH APO-summicron-SL`
- `LEICA 50mm F2 ASPH APO-SUMMICRON-SL`
- `APO-Vario-Elmarit-SL 90-280`
- Sigma / Panasonic / Lumix short tele prime families

Interpretation:

- broad `apo summicron 75`
- broad `summicron 75`
- broad `leica sl 75`
- broad `75 apo`
- broad `75 cron`

are not safe shaping aliases in round 1 because they can drift into:

- M `75mm` families
- neighboring SL `50 / 90 / 90-280` families
- R `80mm` families
- third-party L-mount short tele primes
- accessory-only listings

### Clean local SL-side pool

After restricting to explicit `75mm`, explicit SL-side wording, and excluding M-side `75`, `90mm`, `50mm`, `90-280`, `85mm`, third-party, and accessory contamination, the usable local pool becomes:

- clean local pool: `5`
- unique titles: `3`
- KRW-priced count: `3`
- KRW median: `4,980,000 KRW`

Representative clean titles:

- `[중고] SL APO 75/2 Summicron ASPH (Black)`
- `LEICA 75mm F2 APO-SUMMICRON-SL sn.4699`
- `LEICA 75mm F2 ASPH APO-SUMMICRON-SL sn.4709`

Observed KRW price points:

- `4,680,000 KRW`
- `4,980,000 KRW`
- `4,980,000 KRW`

Interpretation:

- local wording is family-correct
- multiple title shapes converge on the same intended SL-side family
- priced observations exist in KRW and cluster in a coherent band
- evidence is not huge, but it is clean and good enough for a narrow future core row

## Round-1 Recommendation

### Immediate `core` candidate count

- `1`

### Recommended first-pass `core`

- `Leica APO-Summicron-SL 75mm f/2 ASPH`

### Explicit `hold` candidates

- none

## Why not open more than one row?

Because round-1 literature and local evidence both converge on one stable SL-side `75mm f/2 ASPH` prime family, while:

- `APO`
- `ASPH`
- `E67`
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

- `Summicron-M 75`
- `Summilux-M 75`
- `Noctilux-M 75`
- `APO-Summicron-SL 90`
- `APO-Summicron-SL 50`
- `APO-Vario-Elmarit-SL 90-280`
- `Summilux-R 80`
- M / R `75mm / 80mm`
- Sigma / Panasonic / Lumix `75mm / 85mm / 90mm`
- accessory-only listings

## Seed-Round Readiness

- next seed round:
  - `가능`

The future seed should open one narrow core row only:

- `Leica APO-Summicron-SL 75mm f/2 ASPH`

## Validation

Validation run after this audit-only report update:

- `python3 tests/test_normalization_admin.py`
  - `ok`
- `python3 -m py_compile normalization_admin.py golden_set.py tests/test_normalization_admin.py`
  - `ok`
- `python3 golden_set.py`
  - `132/132`
