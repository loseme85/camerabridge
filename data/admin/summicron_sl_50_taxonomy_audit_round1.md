# Summicron-SL 50 Taxonomy Audit - Round 1

Date: 2026-05-21

Scope: audit-only review for the Leica `Summicron-SL 50` family. This round does not add seed rows, does not modify `entities/*.json`, does not modify `canonical_entities_index.json`, and does not change classifier/query/search behavior, ranking, or UI.

## Executive Summary

`Summicron-SL 50` is literature-real, but round-1 local evidence is too thin to justify a seed row yet.

Round-1 conclusion:

- immediate recommended `core` candidate count: `0`
- recommended first-pass core:
  - none in this round
- explicit `hold` candidate:
  - none
- strongest deferred candidate:
  - `Leica Summicron-SL 50mm f/2 ASPH`
- literature clearly supports one real Leica SL `50mm f/2 ASPH Summicron-SL` family
- however current reviewed local evidence collapses to:
  - one clean lens listing
  - plus body-kit rows that must not be used as lens-row support
- broad `summicron-sl 50` / `summicron sl 50` / `summicron 50` / `leica sl 50` / `50 cron` retrieval remains unsafe and must not be hard-pinned

The safest round-1 answer is:

1. recognize `Leica Summicron-SL 50mm f/2 ASPH` as literature-real
2. keep it deferred for now because clean local support is only one title shape
3. keep `ASPH`, `E67`, filter-thread markers, and hood or case bundle wording as overlay or deferred metadata
4. keep adjacent `APO-Summicron-SL 50`, M/R `50mm` families, neighboring SL families, and third-party L-mount `50mm` primes as hard boundaries

## Literature / Reference Base

### Source A: Leica Camera technical specification

Leica Camera documents:

- `Summicron-SL 50 f/2 ASPH.`
- order number:
  - `11193`
- bayonet / format:
  - `L-Mount`, full-frame `35 mm` format
- filter mount:
  - `E67`
- working range:
  - `0.45 m to infinity`

Reference:

- [Leica Camera - Technical Specifications - Summicron-SL 50 f/2 ASPH.](https://leica-camera.com/en-int/photography/lenses/sl/summicron-sl-50mm-f2-asph/technical-specification)

### Source B: Leica Camera product page

Leica Camera product literature documents:

- `Summicron-SL 50 f/2 ASPH.`
- compact SL standard-prime positioning
- explicit standard-lens role inside the SL line

Reference:

- [Leica Camera - Summicron-SL 50 f/2 ASPH.](https://leica-camera.com/en-int/photography/lenses/sl/summicron-sl-50mm-f2-asph)

### Source C: Leica technical data PDF

Leica technical data sheet documents:

- `Summicron-SL 50 f/2 ASPH.`
- order no. `11193`
- optical design:
  - `9 / 8`
- filter mount:
  - `E67`
- no separate internal row-level variant is documented in round 1

Reference:

- [Leica Tech Data PDF - Summicron-SL 50 f/2 ASPH.](https://leica-camera.com/sites/default/files/pm-90762-EN_Datenblatt%20Summicron-SL%2050%20ASPH.pdf)

### Source D: adjacent APO Leica SL 50 family

Leica Camera also documents a separate adjacent family:

- `APO-Summicron-SL 50 f/2 ASPH.`
- order no.:
  - `11185`

Reference:

- [Leica Camera - Technical Specifications - APO-Summicron-SL 50 f/2 ASPH.](https://leica-camera.com/en-int/photography/lenses/sl/apo-summicron-sl-50mm-f2-asph-black/technical-specification)

## Taxonomy Implication from Literature

Literature clearly supports:

- one real target family:
  - `Leica Summicron-SL 50mm f/2 ASPH`

Literature also clearly supports one adjacent non-target family:

- `Leica APO-Summicron-SL 50mm f/2 ASPH`

That means:

- non-APO `Summicron-SL 50` is real
- `APO-Summicron-SL 50` is also real
- they must remain separate

Literature also supports metadata structure around:

- `ASPH`
- `E67`
- filter-thread marker
- hood / cap / case / packaging ecosystem

These are real markers, but round-1 does not justify opening separate rows for them.

## Boundary Check

This family must remain separate from:

- `Leica APO-Summicron-SL 50mm f/2 ASPH`
- `Leica Summicron-M 50mm f/2`
- `Leica APO-Summicron-M 50mm f/2 ASPH`
- `Leica Summicron-R 50mm f/2`
- `Leica Summilux-M 50mm f/1.4`
- `Leica Summilux-R 50mm f/1.4`
- `Leica Noctilux-M 50mm`
- `Leica Elmar 50mm`
- `Leica APO-Summicron-SL 75mm f/2 ASPH`
- `Leica APO-Summicron-SL 90mm f/2 ASPH`
- `Leica Vario-Elmarit-SL 24-90mm f/2.8-4 ASPH`
- Sigma / Panasonic / Lumix `50mm` L-mount primes
- accessory-only listings

## Local Listing Evidence

Analysis base:

- `data/normalized/normalized_latest.json`
- `data/derived/results_resolved_v2.json`
- `data/sold_items.json`

### Broad retrieval behavior

Broad shorthand is risky.

Within the wider `summicron / 50 / sl` field, distinct neighboring or contaminating lines appear immediately:

- `Leica APO-Summicron-SL 50mm f/2 ASPH`
- `Leica Summicron-M 50mm f/2`
- `Leica APO-Summicron-M 50mm f/2 ASPH`
- `Leica Summicron-R 50mm f/2`
- `Leica Summilux-M 50mm f/1.4`
- `Leica Summilux-R 50mm f/1.4`
- `Leica Noctilux 50`
- `Leica Elmar 50`
- `Leica APO-Summicron-SL 75mm f/2 ASPH`
- `Leica APO-Summicron-SL 90mm f/2 ASPH`
- `Leica SL 24-90mm f/2.8-4 Vario-Elmarit`
- Sigma / Panasonic / Lumix `50mm` L-mount prime families

Interpretation:

- broad `summicron-sl 50`
- broad `summicron sl 50`
- broad `summicron 50`
- broad `leica sl 50`
- broad `50 cron`

are not safe shaping aliases in round 1 because they can drift into:

- adjacent APO `Summicron-SL 50`
- M `50mm` Summicron families
- R `50mm` Summicron families
- `Summilux` / `Noctilux` / `Elmar` `50mm` families
- neighboring SL `75 / 90 / 24-90` families
- third-party L-mount `50mm` primes
- accessory-only listings

### Clean local SL-side pool

After restricting to explicit non-APO `50mm f/2 ASPH` Summicron-SL wording, and excluding:

- APO rows
- body-kit rows
- M-side `50mm`
- R-side `50mm`
- neighboring SL `75 / 90 / 24-90`
- third-party
- accessory contamination

the usable local pool becomes:

- clean local pool: `1`
- unique titles: `1`
- KRW-priced count: `1`
- KRW median: `2,580,000 KRW`

Representative clean title:

- `[중고] Leica Summicron-SL 50mm f/2 ASPH`

Observed KRW price point:

- `2,580,000 KRW`

Interpretation:

- local wording is family-correct
- but support is currently only one explicit clean lens listing
- this is not enough yet for a round-1 seed open

### Body-kit contamination

Additional local rows do exist, but they are not clean lens-row support:

- `[위탁] Leica SL2-S Kit with Summicron-SL 50mm f/2 ASPH`
- `[중고] Leica SL2(s) with Summicron-SL 50mm f/2 ASPH`

These support that the family is locally visible, but they must remain outside the clean lens-row pool because they are body-kit listings.

## Round-1 Recommendation

### Immediate `core` candidate count

- `0`

### Recommended first-pass `core`

- none in this round

### Explicit `hold` candidates

- none

### Strongest deferred candidate

- `Leica Summicron-SL 50mm f/2 ASPH`

## Why not open a row yet?

Because round-1 literature is clear, but local clean lens-row support is still only:

- one explicit title shape
- one KRW-priced clean lens row

That means the family is real, but the current local pool is still too thin for a conservative seed round.

The safest round-1 status is:

- literature-real
- local support visible
- seed deferred

## Overlay / Deferred Metadata

Keep below row level:

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

- `ASPH`-only split
- `E67` split
- filter-thread-only split
- hood / case / boxed bundle rows

## Out-of-Family Boundaries

Do not merge with:

- `APO-Summicron-SL 50`
- `Summicron-M 50`
- `APO-Summicron-M 50`
- `Summicron-R 50`
- `Summilux-M 50`
- `Summilux-R 50`
- `Noctilux 50`
- `Elmar 50`
- `APO-Summicron-SL 75`
- `APO-Summicron-SL 90`
- `Vario-Elmarit-SL 24-90`
- Sigma / Panasonic / Lumix `50mm` L-mount primes
- accessory-only listings

## Seedability Decision

`Summicron-SL 50` is literature-real, but round-1 local clean support is too thin for seeding right now.

The family should remain:

- `audit only`
- `deferred`

until:

- multiple clean explicit lens titles appear
- KRW-priced support becomes more than a single clean row

## Validation Snapshot

Round preserved current project validation:

- `python3 tests/test_normalization_admin.py` = `ok`
- `python3 -m py_compile normalization_admin.py golden_set.py tests/test_normalization_admin.py` = `ok`
- `python3 golden_set.py` = `132/132`

## Final Round-1 Verdict

`Leica Summicron-SL 50mm f/2 ASPH` is a literature-real Leica SL normal-prime family and must remain distinct from `APO-Summicron-SL 50`.

However, current local clean support is only one explicit lens row plus body-kit contamination, so the correct round-1 outcome is:

- no immediate core row
- no hold row
- one strongest deferred candidate:
  - `Leica Summicron-SL 50mm f/2 ASPH`
