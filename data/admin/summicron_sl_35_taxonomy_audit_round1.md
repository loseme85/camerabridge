# Summicron-SL 35 Taxonomy Audit - Round 1

Date: 2026-05-22

Scope: audit-only review for the Leica `Summicron-SL 35` family. This round does not add seed rows, does not modify `entities/*.json`, does not modify `canonical_entities_index.json`, and does not change classifier/query/search behavior, ranking, or UI.

## Executive Summary

`Summicron-SL 35` is literature-real, but round-1 local evidence is too thin to justify a seed row yet.

Round-1 conclusion:

- immediate recommended `core` candidate count: `0`
- recommended first-pass core:
  - none in this round
- explicit `hold` candidate:
  - none
- strongest deferred candidate:
  - `Leica Summicron-SL 35mm f/2 ASPH`
- literature clearly supports one real Leica SL `35mm f/2 ASPH Summicron-SL` family
- however current reviewed local evidence collapses to:
  - one clean lens listing
  - plus body-kit rows that must not be used as lens-row support
- broad `summicron-sl 35` / `summicron sl 35` / `summicron 35` / `leica sl 35` / `35 cron` retrieval remains unsafe and must not be hard-pinned

The safest round-1 answer is:

1. recognize `Leica Summicron-SL 35mm f/2 ASPH` as literature-real
2. keep it deferred for now because clean local support is only one explicit lens-row title shape
3. keep `ASPH`, `E67`, filter-thread markers, and hood or case bundle wording as overlay or deferred metadata
4. keep adjacent `APO-Summicron-SL 35`, M/R `35mm` families, neighboring SL families, and third-party L-mount `35mm` primes as hard boundaries

## Literature / Reference Base

### Source A: Leica Camera technical specification

Leica Camera documents:

- `Summicron-SL 35 f/2 ASPH.`
- order number:
  - `11192`
- bayonet / format:
  - `L-Mount`, full-frame `35mm` format
- filter mount:
  - `E67`
- working range:
  - `0.24 m to infinity`

Reference:

- [Leica Camera - Technical Specifications - Summicron-SL 35 f/2 ASPH.](https://leica-camera.com/en-int/photography/lenses/sl/summicron-sl-35mm-f2-asph/technical-specification)

### Source B: Leica Camera product page

Leica Camera product literature documents:

- `Summicron-SL 35 f/2 ASPH.`
- compact SL wide-normal prime positioning
- explicit travel / street / reportage / close-distance role inside the SL line

Reference:

- [Leica Camera - Summicron-SL 35 f/2 ASPH.](https://leica-camera.com/en-US/photography/lenses/sl/summicron-sl-35mm-f2-asph)

### Source C: Leica technical data PDF

Leica technical data sheet documents:

- `Summicron-SL 35 f/2 ASPH.`
- order no. `11192`
- optical design:
  - `11 / 9`
- filter mount:
  - `E67`
- no separate internal row-level variant is documented in round 1

Reference:

- [Leica Tech Data PDF - Summicron-SL 35 f/2 ASPH.](https://leica-camera.com/sites/default/files/pm-90744-EN_Datenblatt%20Summicron-SL%2035%20ASPH.pdf)

### Source D: adjacent APO Leica SL 35 family

Leica Camera also documents a separate adjacent family:

- `APO-Summicron-SL 35 f/2 ASPH.`
- order no.:
  - `11184`
- this is literature-real and must not be merged into the non-APO family

Reference:

- [Leica Camera - APO-Summicron-SL 35 f/2 ASPH.](https://leica-camera.com/en-US/photography/lenses/sl/apo-summicron-sl-35mm-f2-asph/discover)

## Taxonomy Implication from Literature

Literature clearly supports:

- one real target family:
  - `Leica Summicron-SL 35mm f/2 ASPH`

Literature also clearly supports one adjacent non-target family:

- `Leica APO-Summicron-SL 35mm f/2 ASPH`

That means:

- non-APO `Summicron-SL 35` is real
- `APO-Summicron-SL 35` is also real
- they must remain separate

Literature also supports metadata structure around:

- `ASPH`
- `E67`
- filter-thread marker
- hood / cap / case / packaging ecosystem

These are real markers, but round-1 does not justify opening separate rows for them.

## Boundary Check

This family must remain separate from:

- `Leica APO-Summicron-SL 35mm f/2 ASPH`
- `Leica Summicron-M 35mm f/2`
- `Leica Summilux-M 35mm f/1.4`
- `Leica Summaron 35mm`
- `Leica Summicron-R 35mm f/2`
- `Leica Summilux-R 35mm f/1.4`
- `Leica Elmarit-R 35mm f/2.8`
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

Within the wider `summicron / 35 / sl` field, distinct neighboring or contaminating lines appear immediately:

- `Leica APO-Summicron-SL 35mm f/2 ASPH`
- `Leica Summicron-M 35mm f/2`
- `Leica Summilux-M 35mm f/1.4`
- `Leica Summaron 35mm`
- `Leica Summicron-R 35mm f/2`
- `Leica Summilux-R 35mm f/1.4`
- `Leica Elmarit-R 35mm f/2.8`
- `Leica APO-Summicron-SL 50mm f/2 ASPH`
- `Leica APO-Summicron-SL 75mm f/2 ASPH`
- `Leica APO-Summicron-SL 90mm f/2 ASPH`
- `Leica SL 16-35mm f3.5-4.5 Super-Vario-Elmar`
- `Leica SL 24-90mm f2.8-4 Vario-Elmarit`
- Sigma / Panasonic / Lumix `35mm` L-mount prime families

Interpretation:

- broad `summicron-sl 35`
- broad `summicron sl 35`
- broad `summicron 35`
- broad `leica sl 35`
- broad `35 cron`

are not safe shaping aliases in round 1 because they can drift into:

- adjacent APO `Summicron-SL 35`
- M `35mm` Summicron / Summilux / Summaron families
- R `35mm` Summicron / Summilux / Elmarit families
- neighboring SL `50 / 75 / 90 / 16-35 / 24-90` families
- third-party L-mount `35mm` primes
- accessory-only listings

### Clean local SL-side pool

After restricting to explicit non-APO `35mm f/2 ASPH` Summicron-SL wording, and excluding:

- APO rows
- body-kit rows
- M-side `35mm`
- R-side `35mm`
- neighboring SL `50 / 75 / 90 / 16-35 / 24-90`
- third-party
- accessory contamination

the usable local pool becomes:

- clean local pool: `1`
- unique titles: `1`
- KRW-priced count: `0`
- KRW median: none

Representative clean title:

- `Used Leica Summicron-SL 35mm f/2 ASPH`

Interpretation:

- local wording is family-correct
- but support is currently only one explicit clean lens listing
- there is no clean KRW-priced lens-row support yet
- this is not enough for a conservative round-1 seed open

### Body-kit contamination

Additional local rows do exist, but they are not clean lens-row support:

- `[중고] Leica SL2 with Summicron-SL 35mm f/2 ASPH`

This supports that the family is locally visible, but it must remain outside the clean lens-row pool because it is a body-kit listing.

### Miscellaneous contaminated local rows

Another reviewed row appears as:

- `Leica 35mm F2 AsphSummicron SL`

That row is not stable enough to count as clean family support in round 1 because it appears in a contaminated accessory-leaning context and does not preserve reliable explicit non-APO SL-side title shape.

## Round-1 Recommendation

### Immediate `core` candidate count

- `0`

### Recommended first-pass `core`

- none in this round

### Explicit `hold` candidates

- none

### Strongest deferred candidate

- `Leica Summicron-SL 35mm f/2 ASPH`

## Why not open a row yet?

Because round-1 literature is clear, but local clean lens-row support is still only:

- one explicit title shape
- zero clean KRW-priced lens rows

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
- filter-thread row
- hood / case / boxed bundle rows

## Out-of-Family Boundaries

Do not merge with:

- `APO-Summicron-SL 35`
- `Summicron-M 35`
- `Summilux-M 35`
- `Summaron 35`
- `Summicron-R 35`
- `Summilux-R 35`
- `Elmarit-R 35`
- `APO-Summicron-SL 50`
- `APO-Summicron-SL 75`
- `APO-Summicron-SL 90`
- `Super-Vario-Elmar-SL 16-35`
- `Vario-Elmarit-SL 24-90`
- Sigma / Panasonic / Lumix `35mm`
- accessory-only listings

## Seed-Round Readiness

- next seed round:
  - `보류`

The key blocker is not literature quality. It is local support depth:

- one clean lens-row title shape
- no clean KRW-priced support
- live adjacent APO family contamination risk

## Validation

Validation run after this audit-only report update:

- `python3 tests/test_normalization_admin.py`
  - `ok`
- `python3 -m py_compile normalization_admin.py golden_set.py tests/test_normalization_admin.py`
  - `ok`
- `python3 golden_set.py`
  - `132/132`
