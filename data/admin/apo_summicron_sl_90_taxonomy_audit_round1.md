# APO-Summicron-SL 90 Taxonomy Audit - Round 1

Date: 2026-05-21

Scope: audit-only review for the Leica `APO-Summicron-SL 90` family. This round does not add seed rows, does not modify `entities/*.json`, does not modify `canonical_entities_index.json`, and does not change classifier/query/search behavior, ranking, or UI.

## Executive Summary

`APO-Summicron-SL 90` is literature-real, and round-1 local evidence is strong enough to identify one narrow immediate seed candidate for a future seed round.

Round-1 conclusion:

- immediate recommended `core` candidate count: `1`
- recommended first-pass core:
  - `Leica APO-Summicron-SL 90mm f/2 ASPH`
- explicit `hold` candidate:
  - none
- literature clearly supports one real Leica SL `90mm f/2 ASPH APO-Summicron-SL` family
- local title support is strong and stable:
  - repeated `SL 90/2 APO Summicron ASPH`
  - repeated `APO SL 90/2 Summicron ASPH`
  - repeated `90mm F2 ASPH APO-Summicron-SL`
- priced observations exist in KRW and cluster in a coherent band
- broad `apo summicron 90` / `summicron 90` / `leica sl 90` / `90 apo` / `90 cron` retrieval remains unsafe and must not be hard-pinned

The safest round-1 answer is:

1. recognize `Leica APO-Summicron-SL 90mm f/2 ASPH` as an immediate future seed candidate
2. do not open any internal version row
3. keep `APO`, `ASPH`, `E67`, filter-thread markers, and hood or case bundle wording as overlay or deferred metadata
4. keep M-side and R-side `90mm` families, neighboring SL families, and third-party L-mount short tele primes as hard boundaries

## Literature / Reference Base

### Source A: Leica Camera technical specification

Leica Camera documents:

- `APO-Summicron-SL 90 f/2 ASPH.`
- order number:
  - `11179`
- bayonet / format:
  - `L-Mount`, full-frame `35mm` format
- filter mount:
  - `E67`
- working range:
  - `0.6 m to infinity`

Reference:

- [Leica Camera - Technical Specifications - APO-Summicron-SL 90 f/2 ASPH.](https://leica-camera.com/en-US/photography/lenses/sl/apo-summicron-sl-90mm-f2-asph-black/technical-specification)

### Source B: Leica Camera product page

Leica Camera product literature documents:

- `APO-Summicron-SL 90 f/2 ASPH.`
- SL-System short-tele prime positioning
- portrait, stage, event, and reportage orientation
- quiet, precise autofocus

Reference:

- [Leica Camera - APO-Summicron-SL 90 f/2 ASPH.](https://leica-camera.com/en-US/photography/lenses/sl/apo-summicron-sl-90mm-f2-asph-black)

### Source C: Leica technical data PDF

Leica technical data sheet documents:

- `APO-Summicron-SL 90 f/2 ASPH.`
- order no. `11179`
- optical design:
  - `11 / 9`
- filter mount:
  - `E67`
- no separate internal row-level variant is documented in round 1

Reference:

- [Leica Tech Data PDF - APO-Summicron-SL 90 f/2 ASPH.](https://leica-camera.com/sites/default/files/pm-55400-11179_Datenblatt_APO-Summicron-SL-90mm-ASPH_e.pdf)

## Taxonomy Implication from Literature

Literature clearly supports:

- one real family:
  - `Leica APO-Summicron-SL 90mm f/2 ASPH`

No separate aperture-distinct Leica SL `90mm` family was confirmed in primary literature for this round.

Literature also supports metadata structure around:

- `APO`
- `ASPH`
- `E67`
- filter-thread marker
- hood / cap / case / packaging ecosystem

These are real markers, but round-1 does not justify opening separate rows for them.

## Boundary Check

This family must remain separate from:

- `Leica APO-Summicron-M 90mm f/2 ASPH`
- `Leica Summicron-M 90mm f/2`
- `Leica APO-Summicron-R 90mm f/2 ASPH`
- `Leica Summicron-R 90mm f/2`
- `Leica Elmarit-M 90mm f/2.8`
- `Leica Elmarit-R 90mm f/2.8`
- `Leica Tele-Elmarit 90mm f/2.8`
- `Leica Macro-Elmar-M 90mm f/4`
- `Leica Elmar-C 90mm f/4`
- `Leica Thambar-M 90mm f/2.2`
- `Leica APO-Vario-Elmarit-SL 90-280mm f/2.8-4`
- `Leica APO-Summicron-SL 75mm f/2 ASPH`
- `Leica APO-Summicron-SL 50mm f/2 ASPH`
- Sigma / Panasonic / Lumix `85mm / 90mm / 100mm` L-mount primes
- accessory-only listings

## Local Listing Evidence

Analysis base:

- `data/normalized/normalized_latest.json`
- `data/derived/results_resolved_v2.json`
- `data/sold_items.json`

### Broad retrieval behavior

Broad shorthand is risky.

Within the wider `apo summicron / 90 / sl` field, distinct neighboring or contaminating lines appear immediately:

- `Leica M 90mm f2 APO-Summicron ASPH Black`
- `LEICA 90mm F2 APO-SUMMICRON-M`
- `LEICA 75mm F2 APO-SUMMICRON-SL`
- `LEICA 50mm F2 ASPH APO-SUMMICRON-SL`
- `APO-Vario-Elmarit-SL 90-280`
- Sigma / Panasonic / Lumix short tele prime families

Interpretation:

- broad `apo summicron 90`
- broad `summicron 90`
- broad `leica sl 90`
- broad `90 apo`
- broad `90 cron`

are not safe shaping aliases in round 1 because they can drift into:

- M `90mm` Summicron families
- R `90mm` Summicron families
- neighboring SL `50 / 75 / 90-280` families
- third-party L-mount short tele primes
- accessory-only listings

### Clean local SL-side pool

After restricting to explicit `90mm`, explicit SL-side wording, and excluding M-side `90`, R-side `90`, `75mm`, `50mm`, `90-280`, third-party, and accessory contamination, the usable local pool becomes:

- clean local pool: `11`
- unique titles: `4`
- KRW-priced count: `10`
- KRW median: `4,915,000 KRW`

Representative clean titles:

- `[중고] APO SL 90/2 Summicron ASPH (Black)`
- `[중고] SL 90/2 APO Summicron ASPH (Black)`
- `[중고] SL 90/2 APO-Summicron`
- `LEICA 90mm F2 ASPH APO-summicron-SL sn.4713`

Observed KRW price points:

- `4,580,000 KRW`
- `4,580,000 KRW`
- `4,580,000 KRW`
- `4,580,000 KRW`
- `4,880,000 KRW`
- `4,950,000 KRW`
- `4,980,000 KRW`
- `4,980,000 KRW`
- `4,980,000 KRW`
- `4,980,000 KRW`

Interpretation:

- local wording is family-correct
- multiple independent title shapes converge on the same intended SL-side family
- priced observations exist and cluster in a coherent KRW band
- this is materially stronger than many neighboring deferred `90mm` families

### Explicit wording stability

The local pool does not rely on one fragile token only. It repeats across:

- `SL 90/2 APO Summicron ASPH`
- `APO SL 90/2 Summicron ASPH`
- `SL 90/2 APO-Summicron`
- `90mm F2 ASPH APO-Summicron-SL`

That is strong enough for a narrow future core row, while still not making broad `90` shorthand safe.

## Round-1 Recommendation

### Immediate `core` candidate count

- `1`

### Recommended first-pass `core`

- `Leica APO-Summicron-SL 90mm f/2 ASPH`

### Explicit `hold` candidates

- none

## Why not open more than one row?

Because round-1 literature and local evidence both converge on one stable SL-side `90mm f/2 ASPH` prime family, while:

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

- M `90mm` Summicron families
- R `90mm` Summicron families
- M / R `Elmarit 90`
- `Tele-Elmarit 90`
- `Macro-Elmar-M 90`
- `Elmar-C 90`
- `Thambar 90`
- `APO-Vario-Elmarit-SL 90-280`
- `APO-Summicron-SL 75`
- `APO-Summicron-SL 50`
- Sigma / Panasonic / Lumix `85mm / 90mm / 100mm`
- accessory-only listings

## Seed-Round Readiness

- next seed round:
  - `가능`

The future seed should open one narrow core row only:

- `Leica APO-Summicron-SL 90mm f/2 ASPH`

## Validation

Validation run after this audit-only report update:

- `python3 tests/test_normalization_admin.py`
  - `ok`
- `python3 -m py_compile normalization_admin.py golden_set.py tests/test_normalization_admin.py`
  - `ok`
- `python3 golden_set.py`
  - `132/132`
