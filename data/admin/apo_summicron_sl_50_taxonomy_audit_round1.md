# APO-Summicron-SL 50 Taxonomy Audit - Round 1

Date: 2026-05-21

Scope: audit-only review for the Leica `APO-Summicron-SL 50` family. This round does not add seed rows, does not modify `entities/*.json`, does not modify `canonical_entities_index.json`, and does not change classifier/query/search behavior, ranking, or UI.

## Executive Summary

`APO-Summicron-SL 50` is literature-real, and round-1 local evidence is strong enough to identify one narrow immediate seed candidate for a future seed round.

Round-1 conclusion:

- immediate recommended `core` candidate count: `1`
- recommended first-pass core:
  - `Leica APO-Summicron-SL 50mm f/2 ASPH`
- explicit `hold` candidate:
  - none
- literature clearly supports one real Leica SL `50mm f/2 ASPH APO-Summicron-SL` family
- local title support is strong and stable:
  - repeated `SL 50/2 APO Summicron ASPH`
  - repeated `SL 50/2 APO Summicron`
  - repeated `50mm F2 ASPH APO-SUMMICRON-SL`
- priced observations exist in KRW and cluster in a coherent band
- broad `apo summicron 50` / `summicron 50` / `leica sl 50` / `50 apo` / `50 cron` retrieval remains unsafe and must not be hard-pinned

Important correction from round 1:

- literature also supports a separate adjacent family:
  - `Leica Summicron-SL 50mm f/2 ASPH`
- therefore `APO-Summicron-SL 50` must not be merged with non-APO `Summicron-SL 50`
- even `summicron-sl 50` / `summicron sl 50` shorthand is not automatically safe for the APO family

The safest round-1 answer is:

1. recognize `Leica APO-Summicron-SL 50mm f/2 ASPH` as an immediate future seed candidate
2. do not open any internal version row
3. keep `APO`, `ASPH`, `E67`, filter-thread markers, and hood or case bundle wording as overlay or deferred metadata
4. keep M-side and R-side `50mm` families, neighboring SL prime and zoom families, non-APO `Summicron-SL 50`, and third-party L-mount `50mm` primes as hard boundaries

## Literature / Reference Base

### Source A: Leica Camera technical specification

Leica Camera documents:

- `APO-Summicron-SL 50 f/2 ASPH.`
- order number:
  - `11185`
- bayonet / format:
  - `L-Mount`, full-frame `35 mm` format
- filter mount:
  - `E67`
- working range:
  - `0.35 m to infinity`

Reference:

- [Leica Camera - Technical Specifications - APO-Summicron-SL 50 f/2 ASPH.](https://leica-camera.com/en-int/photography/lenses/sl/apo-summicron-sl-50mm-f2-asph-black/technical-specification)

### Source B: Leica Camera product page

Leica Camera product literature documents:

- `APO-Summicron-SL 50 f/2 ASPH.`
- SL-System fast standard-prime positioning
- explicit standard-lens role inside the SL prime line

Reference:

- [Leica Camera - APO-Summicron-SL 50 f/2 ASPH.](https://leica-camera.com/en-DK/photography/lenses/sl/apo-summicron-sl-50mm-f2-asph-black)

### Source C: Leica technical data PDF

Leica technical data sheet documents:

- `APO-Summicron-SL 50 f/2 ASPH.`
- order no. `11185`
- optical design:
  - `12 / 10`
- filter mount:
  - `E67`
- no separate internal row-level variant is documented in round 1

Reference:

- [Leica Tech Data PDF - APO-Summicron-SL 50 f/2 ASPH.](https://leica-camera.com/sites/default/files/pm-55406-11185_Datenblatt_APO-Summicron-SL-50-ASPH_en.pdf)

### Source D: adjacent non-APO Leica SL 50 family

Leica Camera also documents a separate adjacent family:

- `Summicron-SL 50 f/2 ASPH.`
- order no.:
  - `11193`
- this is literature-real and must not be merged into the APO family

Reference:

- [Leica Camera - Technical Specs - Summicron-SL 50 f/2 ASPH.](https://leica-camera.com/en-int/photography/lenses/sl/summicron-sl-50mm-f2-asph/technical-specification)

## Taxonomy Implication from Literature

Literature clearly supports:

- one real target family:
  - `Leica APO-Summicron-SL 50mm f/2 ASPH`

Literature also clearly supports one adjacent non-target family:

- `Leica Summicron-SL 50mm f/2 ASPH`

That means:

- `APO-Summicron-SL 50` is real
- non-APO `Summicron-SL 50` is also real
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

- `Leica Summicron-M 50mm f/2`
- `Leica APO-Summicron-M 50mm f/2 ASPH`
- `Leica Summicron-R 50mm f/2`
- `Leica Summilux-M 50mm f/1.4`
- `Leica Summilux-R 50mm f/1.4`
- `Leica Noctilux-M 50mm`
- `Leica Elmar 50mm`
- `Leica Summicron-SL 50mm f/2 ASPH`
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

Within the wider `apo summicron / 50 / sl` field, distinct neighboring or contaminating lines appear immediately:

- `Leica Summicron-M 50mm f/2`
- `Leica APO-Summicron-M 50mm f/2 ASPH`
- `Leica Summicron-R 50mm f/2`
- `Leica Summilux-M 50mm f/1.4`
- `Leica Summilux-R 50mm f/1.4`
- `Leica Noctilux-M 50mm`
- `Leica Summicron-SL 50mm f/2 ASPH`
- `LEICA 75mm F2 APO-SUMMICRON-SL`
- `LEICA 90mm F2 ASPH APO-SUMMICRON-SL`
- `Leica SL 24-90mm f2.8-4 Vario-Elmarit`
- Sigma / Panasonic / Lumix `50mm` L-mount prime families

Interpretation:

- broad `apo summicron 50`
- broad `summicron 50`
- broad `leica sl 50`
- broad `50 apo`
- broad `50 cron`

are not safe shaping aliases in round 1 because they can drift into:

- M `50mm` Summicron families
- R `50mm` Summicron families
- `Summilux` / `Noctilux` / `Elmar` `50mm` families
- adjacent non-APO `Summicron-SL 50`
- neighboring SL `75 / 90 / 24-90` families
- third-party L-mount `50mm` primes
- accessory-only listings

### Clean local SL-side pool

After restricting to explicit APO-side `50mm`, explicit SL-side wording, and excluding:

- body-kit rows
- non-APO `Summicron-SL 50`
- M-side `50mm`
- R-side `50mm`
- `75mm`
- `90mm`
- `24-90`
- third-party
- accessory contamination

the usable local pool becomes:

- clean local pool: `24`
- unique titles: `6`
- KRW-priced count: `19`
- KRW median: `4,850,000 KRW`

Representative clean titles:

- `[중고] SL 50/2 APO Summicron ASPH (Black)`
- `[위탁] SL 50/2 APO Summicron ASPH (Black)`
- `[중고] SL 50/2 APO Summicron (Black)`
- `LEICA 50mm F2 ASPH APO-SUMMICRON-SL sn.4777`
- `LEICA 50mm F2 ASPH APO-SUMMICRON-SL sn.4776`

Observed KRW price points:

- `4,000,000 KRW`
- `4,400,000 KRW`
- `4,480,000 KRW`
- `4,680,000 KRW`
- `4,680,000 KRW`
- `4,780,000 KRW`
- `4,780,000 KRW`
- `4,780,000 KRW`
- `4,800,000 KRW`
- `4,850,000 KRW`
- `4,880,000 KRW`
- `4,880,000 KRW`
- `4,880,000 KRW`
- `4,980,000 KRW`
- `4,980,000 KRW`
- `4,980,000 KRW`
- `4,980,000 KRW`
- `5,000,000 KRW`
- `5,250,000 KRW`

Interpretation:

- local wording is family-correct
- multiple independent title shapes converge on the same intended SL-side APO family
- priced observations exist and cluster in a coherent KRW band
- local support is comfortably strong enough for a narrow future core row

### Adjacent non-APO SL 50 implication

One reviewed local row also surfaced:

- `[중고] Leica Summicron-SL 50mm f/2 ASPH`

That row should be treated as evidence that adjacent non-APO `Summicron-SL 50` is live in the local pool, not as support for the APO family.

This makes:

- `summicron-sl 50`
- `summicron sl 50`

unsafe broad shorthand for the APO family, even though `SL 50/2 APO Summicron` phrasing itself is stable.

## Round-1 Recommendation

### Immediate `core` candidate count

- `1`

### Recommended first-pass `core`

- `Leica APO-Summicron-SL 50mm f/2 ASPH`

### Explicit `hold` candidates

- none

## Why not open more than one row?

Because round-1 literature and local evidence both converge on one stable SL-side `50mm f/2 ASPH` APO prime family, while:

- `APO`
- `ASPH`
- `E67`
- hood / case / packaging wording

remain below row level and do not justify separate row creation.

Also, adjacent non-APO `Summicron-SL 50` is literature-real, so broad `Summicron-SL 50` shorthand should not be consumed into the APO row.

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
- filter-thread-only split
- hood / case / boxed bundle rows

## Out-of-Family Boundaries

Do not merge with:

- `Summicron-M 50`
- `APO-Summicron-M 50`
- `Summicron-R 50`
- `Summilux-M 50`
- `Summilux-R 50`
- `Noctilux 50`
- `Elmar 50`
- `Summicron-SL 50`
- `APO-Summicron-SL 75`
- `APO-Summicron-SL 90`
- `Vario-Elmarit-SL 24-90`
- Sigma / Panasonic / Lumix `50mm` L-mount primes
- accessory-only listings

## Seedability Decision

`APO-Summicron-SL 50` is seedable in principle, but only as one very narrow row:

- `Leica APO-Summicron-SL 50mm f/2 ASPH`

No evidence in round 1 supports:

- multiple internal row splits
- separate `APO` / `ASPH` rows
- separate `E67` rows
- safe hard-pinning of broad `50mm Summicron` shorthand

## Recommended Future Seed Shape

If a future seed round is opened, the safest first-pass shape is:

- family:
  - `APO-Summicron-SL 50`
- one core row only:
  - `Leica APO-Summicron-SL 50mm f/2 ASPH`
- keep `APO`, `ASPH`, `E67`, filter-thread markers, and hood/case/boxed wording as overlay
- do not treat non-APO `Summicron-SL 50` as alias-equivalent
- do not hard-pin:
  - `apo summicron 50`
  - `summicron 50`
  - `leica sl 50`
  - `50 apo`
  - `50 cron`
  - `summicron-sl 50`
  - `summicron sl 50`

## Validation Snapshot

Round preserved current project validation:

- `python3 tests/test_normalization_admin.py` = `ok`
- `python3 -m py_compile normalization_admin.py golden_set.py tests/test_normalization_admin.py` = `ok`
- `python3 golden_set.py` = `132/132`

## Final Round-1 Verdict

`Leica APO-Summicron-SL 50mm f/2 ASPH` is a literature-real, locally supported Leica SL normal-prime family and is strong enough to be considered an immediate narrow seed candidate in a future seed round.

However, broad `50mm Summicron` shorthand remains unsafe, and adjacent non-APO `Summicron-SL 50` must remain a separate family boundary.
