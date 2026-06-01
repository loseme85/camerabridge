# Vario-Elmarit-SL 24-90 Taxonomy Audit - Round 1

Date: 2026-05-20

Scope: audit-only review for the Leica `Vario-Elmarit-SL 24-90` family. This round does not add seed rows, does not modify `entities/*.json`, does not modify `canonical_entities_index.json`, and does not change classifier/query/search behavior, ranking, or UI.

## Executive Summary

`Vario-Elmarit-SL 24-90` is literature-real, and round-1 local evidence is strong enough to identify one narrow immediate seed candidate for a future seed round.

Round-1 conclusion:

- immediate recommended `core` candidate count: `1`
- recommended first-pass core:
  - `Leica Vario-Elmarit-SL 24-90mm f/2.8-4 ASPH`
- explicit `hold` candidate:
  - none
- literature clearly supports one real Leica SL `24-90mm f/2.8-4 ASPH Vario-Elmarit-SL` family
- local title support is strong and stable:
  - repeated `Leica SL 24-90mm f2.8-4 Vario-Elmarit`
  - repeated `SL 24-90/2.8-4 Vario Elmar ASPH`
  - repeated `24-90mm F2.8-4 ASPH VARIO-ELMARIT-SL`
- priced observations exist in KRW and cluster in a coherent band
- broad `24-90` / `vario elmarit` / `leica sl 24-90` / `24 90 elmarit` retrieval remains unsafe and must not be hard-pinned

The safest round-1 answer is:

1. recognize `Leica Vario-Elmarit-SL 24-90mm f/2.8-4 ASPH` as an immediate future seed candidate
2. do not open any internal version row
3. keep `ASPH`, `OIS`, `E82`, filter-thread markers, hood/case bundles, and similar details as overlay or deferred metadata
4. keep neighboring R zooms, R primes, other SL zooms, and third-party L-mount standard zooms as hard boundaries

## Literature / Reference Base

### Source A: Leica Camera - `Vario-Elmarit-SL 24-90 f/2.8-4 ASPH.`

Leica Camera documents:

- `Vario-Elmarit-SL 24-90 f/2.8-4 ASPH.`
- this is the standard zoom in the SL-System
- integrated optical image stabilisation

Reference:

- [Leica Camera - Vario-Elmarit-SL 24-90 f/2.8-4 ASPH.](https://leica-camera.com/en-US/photography/lenses/sl/vario-elmarit-sl-24-90mm-f2-8-4-asph-black)

### Source B: Leica Wiki - `Vario-Elmarit-SL 24-90 mm f/2.8-4 ASPH.`

Leica Wiki documents:

- order no.:
  - `11176`
- production era:
  - `2015-current`
- image stabilization:
  - multi-axis, `3.5` shutter speed stages
- bayonet fitting:
  - Leica `L` bayonet
- filter / hood:
  - internal thread for `E82` filters
  - lens hood included

Reference:

- [Leica Wiki - Vario-Elmarit-SL 24-90 mm f/2.8-4 ASPH.](https://wiki.l-camera-forum.com/leica-wiki.en/index.php/Vario-Elmarit-SL_24%E2%80%9390_mm_f/2.8%E2%80%934_ASPH.)

### Source C: Leica technical data sheet

Leica technical data sheet documents:

- `LEICA VARIO-ELMARIT-SL 24-90mm f/2.8-4 ASPH.`
- integrated optical image stabilisation
- `E82`
- close focus `30 cm` at `24 mm`

Reference:

- [Leica Tech Data PDF - Vario-Elmarit-SL 24-90 mm f/2.8-4 ASPH.](https://leica-camera.com/sites/default/files/pm-55652-Datenblatt_Vario-Elmarit-SL_24-90_en.pdf)

### Source D: adjacent Leica R / SL boundaries

Separate neighboring families are independently documented:

- `Vario-Elmarit-R 28-90mm f/2.8-4.5 ASPH`
- `Vario-Elmar-R 28-70mm f/3.5-4.5`
- `Vario-Elmar-R 35-70mm f/3.5`
- `Vario-Elmar-R 35-70mm f/4`
- `Vario-Elmarit-R 35-70mm f/2.8 ASPH`
- `Super-Vario-Elmarit-SL 16-35`
- `APO-Vario-Elmarit-SL 90-280`

References:

- [Leica Classic - Vario-Elmarit-R 2,8-4,5/28-90mm ASPH.](https://classic.leica-camera.com/en/Leica-Systems/R-System/Lenses/Zoom-Lenses/Vario-Elmarit-R-2-8-4-5-28-90mm-ASPH./)
- [Leica Classic - Vario-Elmar-R 3,5-4,5/28-70mm](https://classic.leica-camera.com/en/Leica-Systems/R-System/Lenses/Zoom-Lenses/Vario-Elmar-R-3-5-4-5-28-70mm/)
- [Leica Wiki - 35mm-70mm f/3.5 Vario-Elmar-R](https://wiki.l-camera-forum.com/leica-wiki.en/index.php/35mm%E2%80%9370mm_f/3.5_Vario-Elmar-R)
- [Leica Wiki - 35mm-70mm f/4 Vario-Elmar-R](https://wiki.l-camera-forum.com/leica-wiki.en/index.php/35mm%E2%80%9370mm_f/4_Vario-Elmar-R)
- [Leica Camera - Super-Vario-Elmarit-SL 16-35 f/3.5-4.5 ASPH.](https://leica-camera.com/en-US/photography/lenses/sl/super-vario-elmarit-sl-16-35-f3-5-4-5-asph-black)
- [Leica Camera - APO-Vario-Elmarit-SL 90-280 f/2.8-4](https://leica-camera.com/en-int/photography/lenses/sl/apo-vario-elmarit-sl-90-280mm-f2-8-4-black)

## Taxonomy Implication from Literature

Literature clearly supports:

- one real family:
  - `Leica Vario-Elmarit-SL 24-90mm f/2.8-4 ASPH`

No separate aperture-distinct Leica SL `24-90mm` family was confirmed in primary literature for this round.

Literature also supports metadata structure around:

- `ASPH`
- `OIS`
- `E82`
- filter-thread marker
- hood / cap / case / packaging ecosystem

These are real markers, but round-1 does not justify opening separate rows for them.

## Boundary Check

This family must remain separate from:

- `Leica Vario-Elmarit-R 28-90mm f/2.8-4.5 ASPH`
- `Leica Vario-Elmar-R 28-70mm f/3.5-4.5`
- `Leica Vario-Elmar-R 35-70mm f/3.5`
- `Leica Vario-Elmar-R 35-70mm f/4`
- `Leica Vario-Elmarit-R 35-70mm f/2.8 ASPH`
- `Leica Elmarit-R 24mm`
- `Leica Elmarit-R 28mm`
- `Leica Elmarit-R 35mm`
- `Leica Summicron-R 35mm f/2`
- `Leica Summilux-R 35mm f/1.4`
- `Leica Summicron-R 50mm f/2`
- `Leica Summilux-R 50mm f/1.4`
- `Leica Elmarit-R 90mm f/2.8`
- `Super-Vario-Elmarit-SL 16-35`
- `APO-Vario-Elmarit-SL 90-280`
- `SL / L-mount` standard zooms
- Sigma / Panasonic / Lumix `24-70mm / 28-70mm / 24-105mm`
- accessory-only listings

## Local Listing Evidence

Analysis base:

- `data/normalized/normalized_latest.json`
- `data/derived/results_resolved_v2.json`
- `data/sold_items.json`

### Broad retrieval behavior

Broad shorthand is risky.

Within the wider `24-90 / vario elmarit / sl` field, distinct neighboring or contaminating lines appear immediately:

- `[중고] SL 28-70/2.8 Vario-Elmarit`
- `[중고] SL APO Vario Elmarit 90-280 f/2.8-4`
- `[중고] SL 16-35/3.5-4.5 Super Vario Elmar ASPH (Black)`
- `[중고] Leica SL2-S with Vario-Elmarit-SL 24-70mm f/2.8 ASPH`
- `[중고] 파나소닉 24-105 L 마운트`

Interpretation:

- bare `24-90`
- broad `vario elmarit`
- broad `leica sl 24-90`
- broad `24 90 elmarit`

are not safe shaping aliases in round 1 because they can drift into:

- neighboring SL zooms
- Leica R `28-90`
- Leica R `28-70 / 35-70`
- Sigma / Panasonic / Lumix L-mount zooms
- accessory-only listings

### Clean local SL-side pool

After restricting to explicit `24-90mm`, explicit SL-side wording, and excluding `16-35`, `24-70`, `28-70`, `90-280`, R-side `28-90`, third-party, and accessory contamination, the usable local pool becomes:

- clean local pool: `11`
- unique titles: `7`
- KRW-priced count: `8`
- KRW median: `4,505,000 KRW`

Representative clean titles:

- `Leica SL 24-90mm f2.8-4 Vario-Elmarit Black`
- `[위탁] SL 24-90/2.8-4 Vario Elmar ASPH (Black)`
- `[중고] SL Vario Elmarit 24-90/2.8-4 ASPH.`
- `[중고] SL 24-90/2.8-4 Vario Elmar ASPH (Black)`
- `LEICA 24-90mm F2.8-4 ASPH VARIO-ELMARIT-SL sn.4521`
- `LEICA 24-90mm F2.8-4 VARIO-ELMARIT-SL sn.4519`

Observed KRW price points:

- `4,200,000 KRW`
- `4,500,000 KRW`
- `4,500,000 KRW`
- `4,500,000 KRW`
- `4,510,000 KRW`
- `4,780,000 KRW`
- `5,000,000 KRW`
- `5,380,000 KRW`

Interpretation:

- local wording is family-correct
- multiple independent title shapes converge on the same intended SL-side family
- priced observations exist and cluster in a coherent KRW band
- this is materially stronger than the nearby deferred R zoom families

### Explicit wording stability

The local pool does not rely on one fragile token only. It repeats across:

- `SL 24-90mm f2.8-4 Vario-Elmarit`
- `SL 24-90/2.8-4 Vario Elmar ASPH`
- `SL Vario Elmarit 24-90/2.8-4 ASPH`
- `24-90mm F2.8-4 ASPH VARIO-ELMARIT-SL`
- `24-90mm F2.8-4 VARIO-ELMARIT-SL`

Interpretation:

- family recognition is stable at the main-row level
- `ASPH` omission in some seller titles does not behave like a different family
- `Vario Elmar` shorthand appears, but within explicit `SL 24-90/2.8-4` wording it still points to the same intended family rather than a second row

## Marker / Metadata Observation

Within the current clean `24-90 Vario-Elmarit-SL` pool, seller wording does not reliably stabilize row-level internal splits for:

- `ASPH`
- `OIS`
- `E82`
- filter-thread marker
- hood / cap / case / boxed / packaging

These should remain overlay or deferred metadata in round 1.

## Round-1 Candidate Decision

### Immediate core candidate

Recommended immediate future core row:

- `Leica Vario-Elmarit-SL 24-90mm f/2.8-4 ASPH`

Why this is strong enough for a future seed round:

- literature identity is clear and singular
- local title wording is stable across several independent title shapes
- priced KRW support exists
- the intended SL-side family separates cleanly from adjacent R, SL, and third-party zooms when the query keeps explicit `SL`, `24-90`, or `Vario-Elmarit-SL` anchors

### Hold candidate

No explicit hold candidate is recommended in round 1.

### Deferred / overlay-only items

Do not open separate rows for:

- `ROM`
- `cam version`
- `ASPH`
- `OIS`
- `E82`
- filter-thread marker
- hood / cap / case / boxed / packaging

### Hard-pin prohibited shorthand

Do not hard-pin:

- `24-90`
- `vario elmarit`
- `leica sl 24-90`
- `24 90 elmarit`

These remain too broad because they can drift into:

- `SL 16-35`
- `SL 90-280`
- Leica R `28-90`
- Sigma / Panasonic / Lumix standard zooms
- accessory-only rows

## Round-1 Conclusion

Round-1 status for `Vario-Elmarit-SL 24-90`:

- family is real in primary literature
- local title support is strong
- priced KRW support exists
- immediate core candidate count: `1`
- recommended first-pass core:
  - `Leica Vario-Elmarit-SL 24-90mm f/2.8-4 ASPH`
- explicit hold candidate:
  - none

Accordingly, this family looks seedable in a future narrow seed round, but this audit round itself should remain audit-only.
