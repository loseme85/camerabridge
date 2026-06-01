# Super-APO-Summicron-SL 21 Taxonomy Audit - Round 1

Date: 2026-05-23

Scope: audit-only review for the Leica `Super-APO-Summicron-SL 21` family. This round does not add seed rows, does not modify `entities/*.json`, does not modify `canonical_entities_index.json`, and does not change classifier/query/search behavior, ranking, or UI.

## Executive Summary

`Super-APO-Summicron-SL 21` is literature-real, but round-1 local evidence is too thin to justify opening a seed row yet.

Round-1 conclusion:

- immediate recommended `core` candidate count: `0`
- recommended first-pass core:
  - none in this round
- explicit `hold` candidate:
  - none
- strongest deferred candidate:
  - `Leica Super-APO-Summicron-SL 21mm f/2 ASPH`
- literature clearly supports one real Leica SL `21mm f/2 ASPH Super-APO-Summicron-SL` family
- current reviewed local support does not show a clean lens-row pool
- broad `super apo summicron 21` / `apo summicron 21` / `summicron 21` / `leica sl 21` / `21 apo` / `21 cron` retrieval remains unsafe and must not be hard-pinned

The safest round-1 answer is:

1. recognize `Leica Super-APO-Summicron-SL 21mm f/2 ASPH` as a literature-real future seed candidate
2. do not open any core row in this round
3. keep `Super-APO`, `APO`, `ASPH`, `E67`, filter-thread markers, and hood or case bundle wording as overlay or deferred metadata
4. keep M-side `21mm` families, `Tri-Elmar 16-18-21 / WATE`, closed `APO-Summicron-SL 24` hypothesis, neighboring SL prime and zoom families, and third-party L-mount wide primes as hard boundaries

## Literature / Reference Base

### Source A: Leica Camera technical specification

Leica Camera documents:

- `Super-APO-Summicron-SL 21 f/2 ASPH.`
- order number:
  - `11181`
- bayonet / format:
  - `L-Mount`, full-frame `35mm` format
- filter mount:
  - `E67`
- working range:
  - `0.21 m to infinity`

Reference:

- [Leica Camera - Technical Specifications - Super-APO-Summicron-SL 21 f/2 ASPH.](https://leica-camera.com/en-int/photography/lenses/sl/super-apo-summicron-sl-21-f2-asph/technical-specification)

### Source B: Leica Camera product page

Leica Camera product literature documents:

- `Super-APO-Summicron-SL 21 f/2 ASPH.`
- explicit SL-system ultra-wide APO prime positioning
- line naming distinct from both `APO-Summicron-SL 28` and `Super-Vario-Elmar-SL 16-35`

Reference:

- [Leica Camera - Super-APO-Summicron-SL 21 f/2 ASPH.](https://leica-camera.com/en-US/photography/lenses/sl/super-apo-summicron-sl-21-f2-asph)

### Source C: Leica technical data PDF

Leica technical data sheet documents:

- `Super-APO-Summicron-SL 21 f/2 ASPH.`
- order no. `11181`
- optical design:
  - `14 / 11`
- filter mount:
  - `E67`
- no separate internal row-level variant is documented in round 1

Reference:

- [Leica Tech Data PDF - Super-APO-Summicron-SL 21 f/2 ASPH.](https://leica-camera.com/sites/default/files/pm-106496-en_datenblatt-summicron-sl-21-asph_1.pdf)

### Source D: Leica SL ultra-wide launch press literature

Leica's launch literature explicitly introduces:

- `Super-APO-Summicron-SL 21 f/2 ASPH.`
- alongside `Super-Vario-Elmarit-SL 14-24 f/2.8 ASPH.`

This confirms the real SL ultra-wide APO prime family and also reinforces that the adjacent `APO-Summicron-SL 24` hypothesis is not the actual Leica line.

Reference:

- [Leica Camera - Press Release - Super-APO-Summicron-SL 21 f/2 ASPH.](https://leica-camera.com/sites/default/files/2023-10/press_release_apo-summicron-sl_21_super-vario-sl_14-24_october_2023.pdf)

## Taxonomy Implication from Literature

Literature clearly supports:

- one real target family:
  - `Leica Super-APO-Summicron-SL 21mm f/2 ASPH`

Literature also supports metadata structure around:

- `Super-APO`
- `APO`
- `ASPH`
- `E67`
- filter-thread marker
- hood / cap / case / packaging ecosystem

These are real markers, but round-1 does not justify opening separate rows for them.

## Boundary Check

This family must remain separate from:

- `Leica Super-Elmar-M 21mm f/3.4 ASPH`
- `Leica Elmarit-M 21mm f/2.8`
- `Leica Super-Angulon 21mm`
- `Leica Summilux-M 21mm f/1.4 ASPH`
- `Leica Tri-Elmar-M 16-18-21mm f/4 ASPH` / `WATE`
- closed `Leica APO-Summicron-SL 24mm f/2 ASPH` hypothesis
- `Leica APO-Summicron-SL 28mm f/2 ASPH`
- `Leica APO-Summicron-SL 35mm f/2 ASPH`
- `Leica Super-Vario-Elmar-SL 16-35mm f/3.5-4.5 ASPH`
- `Leica Vario-Elmarit-SL 24-90mm f/2.8-4 ASPH`
- Sigma / Panasonic / Lumix `20 / 21 / 24mm` L-mount primes
- accessory-only listings

## Local Listing Evidence

Analysis base:

- `data/normalized/normalized_latest.json`
- `results.json`
- `data/sold_items.json`

### Broad retrieval behavior

Broad shorthand is risky.

Within the wider `21 / summicron / sl / apo` field, distinct neighboring or contaminating lines appear immediately:

- `Leica Super-Elmar 21`
- `Leica Elmarit 21`
- `Leica Super-Angulon 21`
- `Leica Summilux 21`
- `Tri-Elmar 16-18-21` / `WATE`
- closed `APO-Summicron-SL 24` hypothesis
- `APO-Summicron-SL 28`
- `APO-Summicron-SL 35`
- `Leica SL 16-35mm f3.5-4.5 Super-Vario-Elmar`
- `Leica SL 24-90mm f2.8-4 Vario-Elmarit`
- Sigma / Panasonic / Lumix `20 / 21 / 24mm` L-mount primes
- accessory-only rows such as:
  - `[중고] SL 21/2 APO 용 후드`

Interpretation:

- broad `super apo summicron 21`
- broad `apo summicron 21`
- broad `summicron 21`
- broad `leica sl 21`
- broad `21 apo`
- broad `21 cron`

are not safe shaping aliases in round 1 because they can drift into:

- M-side `21mm` Leica families
- `WATE`
- neighboring SL `28 / 35 / 16-35 / 24-90` families
- third-party L-mount `20 / 21 / 24mm` primes
- accessory-only listings

### Clean local SL-side pool

After restricting to explicit `Super-APO-Summicron-SL 21` wording and excluding:

- M-side `21mm`
- `WATE`
- closed `APO-Summicron-SL 24`
- neighboring SL `28 / 35 / 16-35 / 24-90`
- third-party
- accessory contamination

the usable local pool becomes:

- clean local pool: `0`
- unique titles: `0`
- KRW-priced count: `0`
- KRW median: 없음

Observed local contamination note:

- `[중고] SL 21/2 APO 용 후드`

Interpretation:

- local visibility exists only at the accessory level in the current reviewed pool
- there is no clean lens-row support yet
- this is too thin for a conservative seed open

## Round-1 Recommendation

### Immediate `core` candidate count

- `0`

### Recommended first-pass `core`

- none in this round

### Explicit `hold` candidates

- none

### Strongest deferred candidate

- `Leica Super-APO-Summicron-SL 21mm f/2 ASPH`

## Why not open a core row yet?

Because round-1 literature is strong but local evidence is effectively absent at the lens-row level.

The current reviewed pool supports:

- literature-real family status
- hard boundary definition

but does not yet support:

- a stable clean local title pool
- priced clean local evidence
- safe conservative seed activation

## Overlay / Deferred Metadata

Keep below row level:

- `Super-APO`
- `APO`
- `ASPH`
- `E67`
- filter-thread marker
- hood included
- cap included
- boxed
- case included
- packaging

Do not open separate rows for:

- `Super-APO`-only split
- `APO`-only split
- `ASPH`-only split
- `E67` split
- hood / case / boxed bundle rows

## Out-of-Family Boundaries

Do not merge with:

- `Super-Elmar 21`
- `Elmarit 21`
- `Super-Angulon 21`
- `Summilux 21`
- `Tri-Elmar 16-18-21` / `WATE`
- closed `APO-Summicron-SL 24` hypothesis
- `APO-Summicron-SL 28`
- `APO-Summicron-SL 35`
- `Super-Vario-Elmar-SL 16-35`
- `Vario-Elmarit-SL 24-90`
- Sigma / Panasonic / Lumix `20 / 21 / 24mm`
- accessory-only listings

## Seed-Round Readiness

- next seed round:
  - `보류`

The future seed should open one narrow core row only, if and when clean local support appears:

- `Leica Super-APO-Summicron-SL 21mm f/2 ASPH`

Do not treat broad `summicron`, `apo`, or `21` shorthand as family-safe in the meantime.

## Validation

Validation run after this audit-only report update:

- `python3 tests/test_normalization_admin.py`
  - `ok`
- `python3 -m py_compile normalization_admin.py golden_set.py tests/test_normalization_admin.py`
  - `ok`
- `python3 golden_set.py`
  - `132/132`
