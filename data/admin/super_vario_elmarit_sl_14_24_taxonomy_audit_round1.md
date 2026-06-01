# Super-Vario-Elmarit-SL 14-24 Taxonomy Audit - Round 1

Date: 2026-05-23

Scope: audit-only review for the Leica `Super-Vario-Elmarit-SL 14-24` family. This round does not add seed rows, does not modify `entities/*.json`, does not modify `canonical_entities_index.json`, and does not change classifier/query/search behavior, ranking, or UI.

## Executive Summary

`Super-Vario-Elmarit-SL 14-24` is literature-real, and round-1 naming is clearly supported under the exact Leica string:

- `Leica Super-Vario-Elmarit-SL 14-24mm f/2.8 ASPH`

Round-1 conclusion:

- immediate recommended `core` candidate count: `0`
- recommended first-pass core:
  - none in this round
- explicit `hold` candidate:
  - none
- strongest deferred candidate:
  - `Leica Super-Vario-Elmarit-SL 14-24mm f/2.8 ASPH`
- literature clearly supports one real Leica SL ultra-wide zoom family under `Super-Vario-Elmarit-SL` naming
- local title support exists, but is still too thin and too repetitive:
  - one repeated local title shape only
  - no second stable clean local wording pattern yet
- priced KRW observations exist, but they come from the same narrow local title form
- broad `14-24` / `super vario elmarit` / `leica sl 14-24` / `14 24 elmarit` / `sl 14-24` retrieval remains unsafe and must not be hard-pinned

The safest round-1 answer is:

1. recognize `Leica Super-Vario-Elmarit-SL 14-24mm f/2.8 ASPH` as a literature-real future seed candidate
2. keep this round in `audit only / deferred`
3. keep `ASPH`, bayonet-side filter-holder wording, permanently mounted hood wording, front-cap or case bundle wording, and similar details as overlay or deferred metadata
4. keep `Super-Vario-Elmar-SL 16-35`, `Vario-Elmarit-SL 24-90`, M `Tri-Elmar 16-18-21 / WATE`, R `21-35`, and Sigma / Panasonic / Lumix ultra-wide zooms as hard boundaries

## Literature / Reference Base

### Source A: Leica Camera technical specification

Leica Camera documents:

- `Super-Vario-Elmarit-SL 14-24 f/2.8 ASPH.`
- order number:
  - `11194`
- bayonet:
  - Leica `L` bayonet
- no front screw filter thread is documented
- instead:
  - `Holder for foil filter on bayonet`
- hood:
  - `Permanently mounted`

Reference:

- [Leica Camera - Technical Specifications - Super-Vario-Elmarit-SL 14-24 f/2.8 ASPH.](https://leica-camera.com/en-int/photography/lenses/sl/leica-super-vario-elmarit-sl-14-24-f28-asph-black-anodized-finish/technical-specification)

### Source B: Leica Camera product page

Leica Camera product literature documents:

- `Super-Vario-Elmarit-SL 14-24 f/2.8 ASPH.`
- explicit SL-system ultra-wide zoom positioning
- focal range:
  - `14-24mm`
- maximum angle of view:
  - up to `114°`

Reference:

- [Leica Camera - Super-Vario-Elmarit-SL 14-24 f/2.8 ASPH.](https://leica-camera.com/en-US/photography/lenses/sl/leica-super-vario-elmarit-sl-14-24-f28-asph-black-anodized-finish)

### Source C: Leica technical data PDF

Leica technical data sheet documents:

- `LEICA SUPER-VARIO-ELMARIT-SL 14-24 f/2.8 ASPH.`
- order no.:
  - `11194`
- optical design:
  - `18 / 13`
- fixed hood and bayonet-side filter-holder structure

Reference:

- [Leica Tech Data PDF - Super-Vario-Elmarit-SL 14-24 f/2.8 ASPH.](https://leica-camera.com/sites/default/files/pm-101480-en_datenblatt_super-vario-elmarit-sl_14-24_asph.pdf)

### Source D: Leica SL ultra-wide launch press literature

Leica's launch literature explicitly introduces:

- `Super-Vario-Elmarit-SL 14-24 f/2.8 ASPH.`
- alongside:
  - `Super-APO-Summicron-SL 21 f/2 ASPH.`

This is also the same literature context that clarifies the real SL ultra-wide structure and helps close the unsupported `APO-Summicron-SL 24` hypothesis.

Reference:

- [Leica Press Release - Leica expands the SL-System with two new ultra-wide-angle lenses](https://leica-camera.com/sites/default/files/2023-10/press_release_apo-summicron-sl_21_super-vario-sl_14-24_october_2023.pdf)

## Taxonomy Implication from Literature

Literature clearly supports:

- one real family:
  - `Leica Super-Vario-Elmarit-SL 14-24mm f/2.8 ASPH`

Round-1 literature also confirms that the exact naming is:

- `Super-Vario-Elmarit-SL`

not:

- `Super-Vario-Elmar-SL 14-24`

This matters because nearby SL ultra-wide zoom naming is asymmetric:

- `Leica Super-Vario-Elmar-SL 16-35mm f/3.5-4.5 ASPH`
- `Leica Super-Vario-Elmarit-SL 14-24mm f/2.8 ASPH`

So `Elmar` / `Elmarit` should not be flattened into one generic family pattern.

Literature supports metadata structure around:

- `ASPH`
- bayonet-side filter holder
- permanently mounted hood
- front-cap and packaging ecosystem

Round-1 literature does **not** support:

- `E82` for this family
- a normal front screw filter thread
- tripod collar wording

These should remain overlay or deferred metadata only, and unsupported markers should not be promoted into row-level splits.

## Boundary Check

This family must remain separate from:

- `Leica Super-Vario-Elmar-SL 16-35mm f/3.5-4.5 ASPH`
- `Leica Vario-Elmarit-SL 24-90mm f/2.8-4 ASPH`
- `Leica Super-APO-Summicron-SL 21mm f/2 ASPH`
- `Leica APO-Summicron-SL 28mm f/2 ASPH`
- `Leica APO-Summicron-SL 35mm f/2 ASPH`
- M `Tri-Elmar 16-18-21mm f/4 ASPH` / `WATE`
- M `21mm` and `24mm` wide-prime families
- `Leica Vario-Elmar-R 21-35mm f/3.5-4 ASPH`
- closed `Leica APO-Summicron-SL 24mm f/2 ASPH` hypothesis
- Sigma / Panasonic / Lumix `14-24mm / 14-28mm / 16-28mm / 16-35mm / 20mm / 21mm / 24mm`
- accessory-only listings

## Local Listing Evidence

Analysis base:

- `data/normalized/normalized_latest.json`
- `results.json`
- `data/sold_items.json`

### Broad retrieval behavior

Broad shorthand is risky.

Within the wider `14-24 / vario elmarit / sl` field, distinct neighboring or contaminating lines appear immediately:

- `[중고] SL 24-90/2.8-4 Vario Elmar ASPH (Black)`
- `Tri-Elmar 16-18-21 (WATE)`
- `Sigma 14-24mm F2.8 DG DN Art - L Mount`
- `Sigma 16-28mm F2.8 DG DN Contemporary - L Mount`

Interpretation:

- bare `14-24`
- broad `super vario elmarit`
- broad `leica sl 14-24`
- broad `14 24 elmarit`
- broad `sl 14-24`

are not safe shaping aliases in round 1 because they can drift into:

- neighboring SL zooms
- M `WATE`
- R `21-35`
- third-party L-mount ultra-wide zooms
- accessory-only listings

### Clean local SL-side pool

After restricting to explicit `14-24`, explicit SL-side wording, explicit `Vario Elmarit`, and excluding:

- `16-35`
- `24-90`
- M `WATE`
- R `21-35`
- third-party ultra-wide zooms
- accessory contamination

the usable local pool becomes:

- clean local pool: `3`
- unique titles: `1`
- KRW-priced count: `3`
- KRW median: `3,080,000 KRW`

Representative clean title:

- `[중고] SL 14-24/2.8 Vario Elmarit ASPH (Black)`

Observed KRW price points:

- `3,080,000 KRW`
- `3,080,000 KRW`
- `3,180,000 KRW`

Interpretation:

- local wording is directionally family-correct
- priced KRW observations do exist
- but the reviewed clean pool currently repeats one seller title shape only
- there is not yet a second or third independent clean wording pattern like:
  - full `Super-Vario-Elmarit-SL`
  - explicit `14-24mm F2.8 ASPH SUPER-VARIO-ELMARIT-SL`
  - alternate clean SL-side retail wording

That makes the current local support materially thinner than the SL families that were opened in earlier rounds.

## Marker / Metadata Observation

Within the current clean `14-24 Super-Vario-Elmarit-SL` pool, seller wording does not justify row-level internal splits for:

- `ASPH`
- bayonet-side filter-holder marker
- permanently mounted hood
- hood / cap / case / boxed / packaging
- front-cap wording

These should remain overlay or deferred metadata in round 1.

`E82` should not be opened because current primary literature does not support it for this family.

`Tripod collar` should also remain out because current primary literature does not support it for this family.

## Round-1 Candidate Decision

### Immediate `core` candidate count

- `0`

### Recommended first-pass `core`

- none in this round

### Explicit `hold` candidates

- none

### Strongest deferred candidate

- `Leica Super-Vario-Elmarit-SL 14-24mm f/2.8 ASPH`

## Why not open a core row yet?

Because round-1 literature is strong, but local clean lens-row support is still too narrow.

The current reviewed pool supports:

- exact family reality in Leica literature
- exact `Super-Vario-Elmarit-SL` naming
- coherent KRW pricing

but does not yet support:

- multiple independent clean local title shapes
- robust enough separation from adjacent ultra-wide zoom contamination on shorthand

This is closer to:

- `literature-real, locally visible, but still too thin for conservative seed open`

than to:

- `immediate narrow seed candidate`

## Overlay / Deferred Metadata

Keep below row level:

- `ASPH`
- bayonet-side filter holder
- permanently mounted hood
- hood / cap / case / boxed / packaging
- front-cap wording
- finish
- country marking
- engraving
- condition

Do **not** open separate rows for:

- `ASPH`
- filter-holder wording
- hood bundle wording
- case bundle wording
- boxed bundle wording
- front-cap wording
- `E82`
- tripod collar

## Final Round-1 Recommendation

### Literature status

- literature-real

### Seedability in this round

- deferred

### Best next action

- do not seed in this round
- keep `Leica Super-Vario-Elmarit-SL 14-24mm f/2.8 ASPH` as the strongest deferred candidate
- wait for broader clean local lens-row support before opening a core row

### If a future seed round is attempted

Open only one narrow row:

- `Leica Super-Vario-Elmarit-SL 14-24mm f/2.8 ASPH`

with all of the following kept out of row-level expansion:

- `ASPH`
- filter-holder wording
- hood / cap / case / boxed / packaging
- front-cap wording
- any inferred `E82`
- any tripod-collar wording

### Hard boundaries to preserve

- `Leica Super-Vario-Elmar-SL 16-35mm f/3.5-4.5 ASPH`
- `Leica Vario-Elmarit-SL 24-90mm f/2.8-4 ASPH`
- `Leica Super-APO-Summicron-SL 21mm f/2 ASPH`
- `Leica APO-Summicron-SL 28mm f/2 ASPH`
- `Leica APO-Summicron-SL 35mm f/2 ASPH`
- M `Tri-Elmar 16-18-21 / WATE`
- `Leica Vario-Elmar-R 21-35mm`
- Sigma / Panasonic / Lumix ultra-wide zooms
- accessory-only listings

### Unsafe broad aliases

Do **not** hard-pin:

- `14-24`
- `super vario elmarit`
- `leica sl 14-24`
- `14 24 elmarit`
- `sl 14-24`
