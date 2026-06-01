# APO-Vario-Elmarit-SL 90-280 Taxonomy Audit - Round 1

Date: 2026-05-21

Scope: audit-only review for the Leica `APO-Vario-Elmarit-SL 90-280` family. This round does not add seed rows, does not modify `entities/*.json`, does not modify `canonical_entities_index.json`, and does not change classifier/query/search behavior, ranking, or UI.

## Executive Summary

`APO-Vario-Elmarit-SL 90-280` is literature-real, and round-1 local evidence is strong enough to identify one narrow immediate seed candidate for a future seed round.

Round-1 conclusion:

- immediate recommended `core` candidate count: `1`
- recommended first-pass core:
  - `Leica APO-Vario-Elmarit-SL 90-280mm f/2.8-4`
- explicit `hold` candidate:
  - none
- literature clearly supports one real Leica SL `90-280mm f/2.8-4 APO-Vario-Elmarit-SL` family
- local title support is narrow but stable:
  - repeated `SL APO Vario Elmarit 90-280 f/2.8-4`
  - repeated `SL 90-280/2.8-4 APO Vario Elmarit ASPH`
  - repeated `90-280mm F2.8-4 APO-VARIO-ELMARIT-SL`
- priced observations exist in KRW and cluster in a coherent band
- broad `90-280` / `apo vario elmarit` / `leica sl 90-280` / `90 280 elmarit` retrieval remains unsafe and must not be hard-pinned

The safest round-1 answer is:

1. recognize `Leica APO-Vario-Elmarit-SL 90-280mm f/2.8-4` as an immediate future seed candidate
2. do not open any internal version row
3. keep `APO`, `OIS`, `E82`, tripod-collar wording, hood/case bundles, and similar details as overlay or deferred metadata
4. keep neighboring R tele zooms, R `180 / 280` families, SL APO-Summicron primes, and third-party L-mount tele zooms as hard boundaries

## Literature / Reference Base

### Source A: Leica Camera - `APO-Vario-Elmarit-SL 90-280 f/2.8-4`

Leica Camera documents:

- `APO-Vario-Elmarit-SL 90-280 f/2.8-4`
- tele zoom in the Leica SL-System
- integrated optical image stabilisation
- removable tripod plate and lockable tripod collar

Reference:

- [Leica Camera - APO-Vario-Elmarit-SL 90-280 f/2.8-4](https://leica-camera.com/en-int/photography/lenses/sl/apo-vario-elmarit-sl-90-280mm-f2-8-4-black)

### Source B: Leica technical data sheet

Leica technical data sheet documents:

- `Leica APO-Vario-Elmarit-SL 90-280 mm f/2.8-4`
- order no.:
  - `11175`
- `L-Mount`, full-frame coverage
- `O.I.S.` performance:
  - `3.5` stops
- filter thread:
  - `E82`
- optical design:
  - `23 / 17`

References:

- [Leica Tech Data PDF - APO-Vario-Elmarit-SL 90-280 mm f/2.8-4](https://leica-camera.com/sites/default/files/pm-55506-Datenblatt_APO-Vario-Elmarit-SL_90-280_en.pdf)
- [Leica Technical Specification page](https://leica-camera.com/en-int/photography/lenses/sl/apo-vario-elmarit-sl-90-280mm-f2-8-4-black/technical-specification)

### Source C: adjacent Leica SL / R boundaries

Separate neighboring families are independently documented:

- `Vario-Elmarit-SL 24-90`
- `Super-Vario-Elmarit-SL 16-35`
- `APO-Summicron-SL 75`
- `APO-Summicron-SL 90`
- `Vario-Elmar-R 105-280`
- `Vario-APO-Elmarit-R 70-180`

References:

- [Leica Camera - Vario-Elmarit-SL 24-90 f/2.8-4 ASPH.](https://leica-camera.com/en-US/photography/lenses/sl/vario-elmarit-sl-24-90mm-f2-8-4-asph-black)
- [Leica Camera - Super-Vario-Elmarit-SL 16-35 f/3.5-4.5 ASPH.](https://leica-camera.com/en-US/photography/lenses/sl/super-vario-elmarit-sl-16-35-f3-5-4-5-asph-black)
- [Leica Wiki - 105mm-280mm f/4.2 Vario-Elmar-R](https://wiki.l-camera-forum.com/leica-wiki.en/index.php/105mm%E2%80%93280mm_f/4.2_Vario-Elmar-R)
- [Leica Wiki - 70mm-180mm f/2.8 Vario-APO-Elmarit-R](https://wiki.l-camera-forum.com/leica-wiki.en/index.php?title=70mm%E2%80%93180mm_f%2F2.8_Vario-APO-Elmarit-R)

## Taxonomy Implication from Literature

Literature clearly supports:

- one real family:
  - `Leica APO-Vario-Elmarit-SL 90-280mm f/2.8-4`

No separate aperture-distinct Leica SL `90-280mm` family was confirmed in primary literature for this round.

Literature also supports metadata structure around:

- `APO`
- `OIS`
- `E82`
- filter-thread marker
- tripod collar
- hood / cap / case / packaging ecosystem

These are real markers, but round-1 does not justify opening separate rows for them.

## Boundary Check

This family must remain separate from:

- `Leica Vario-Elmarit-SL 24-90mm f/2.8-4 ASPH`
- `Leica Super-Vario-Elmarit-SL 16-35mm f/3.5-4.5 ASPH`
- `Leica APO-Summicron-SL 90mm f/2 ASPH`
- `Leica APO-Summicron-SL 75mm f/2 ASPH`
- `Leica Vario-Elmar-R 105-280mm f/4.2`
- `Leica Vario-APO-Elmarit-R 70-180mm f/2.8`
- `Leica APO-Telyt-R 180mm`
- `Leica APO-Elmarit-R 180mm`
- `Leica Elmarit-R 180mm`
- `Leica APO-Summicron-R 180mm`
- `Leica APO-Telyt-R 280mm`
- Sigma / Panasonic / Lumix `70-200mm / 100-400mm`
- accessory-only listings

## Local Listing Evidence

Analysis base:

- `data/normalized/normalized_latest.json`
- `data/derived/results_resolved_v2.json`
- `data/sold_items.json`

### Broad retrieval behavior

Broad shorthand is risky.

Within the wider `90-280 / apo vario elmarit / sl` field, distinct neighboring or contaminating lines appear immediately:

- `[중고] SL 24-90/2.8-4 Vario Elmar ASPH (Black)`
- `[중고] SL 100-400`
- `[중고] SL 100-400/5-6.3 Vario-Elmar (Black)`
- `Panasonic 70-200mm F4 OIS Pro S`
- `[중고] R 105-280/4.2 ROM (Black)`
- `[위탁] R 70-180/2.8 Vario Apo Elmarit (Black)`

Interpretation:

- bare `90-280`
- broad `apo vario elmarit`
- broad `leica sl 90-280`
- broad `90 280 elmarit`

are not safe shaping aliases in round 1 because they can drift into:

- neighboring SL zooms
- Leica R `105-280`
- Leica R `70-180`
- Leica R `180 / 280` families
- Sigma / Panasonic / Lumix tele zooms
- accessory-only listings

### Clean local SL-side pool

After restricting to explicit `90-280mm`, explicit SL-side wording, and excluding `24-90`, `16-35`, `100-400`, `70-200`, `105-280`, `70-180`, SL primes, third-party, and accessory contamination, the usable local pool becomes:

- clean local pool: `17`
- unique titles: `5`
- unique title shapes: `3`
- KRW-priced count: `3`
- KRW median: `6,580,000 KRW`

Representative clean titles:

- `[중고] SL APO Vario Elmarit 90-280 f/2.8-4`
- `[중고] SL 90-280/2.8-4 APO Vario Elmarit ASPH (Black)`
- `LEICA 90-280mm F2.8-4 APO-VARIO-ELMARIT-SL sn.4575`
- `LEICA 90-280mm F2.8-4 APO-VARIO-ELMARIT-SL sn.4572`

Observed KRW price points:

- `5,500,000 KRW`
- `6,580,000 KRW`
- `6,850,000 KRW`

Interpretation:

- local wording is family-correct
- multiple independent title shapes converge on the same intended SL-side family
- priced observations exist and cluster in a coherent KRW band
- this is materially stronger than the nearby deferred R tele zoom families

### Explicit wording stability

The local pool does not rely on one fragile token only. It repeats across:

- `SL APO Vario Elmarit 90-280 f/2.8-4`
- `SL 90-280/2.8-4 APO Vario Elmarit ASPH`
- `90-280mm F2.8-4 APO-VARIO-ELMARIT-SL`

Interpretation:

- family recognition is stable at the main-row level
- `ASPH` omission in some seller titles does not behave like a different family
- `APO` omission is not observed in the clean local pool

## Marker / Metadata Observation

Within the current clean `90-280 APO-Vario-Elmarit-SL` pool, seller wording does not reliably stabilize row-level internal splits for:

- `APO`
- `OIS`
- `E82`
- filter-thread marker
- tripod collar
- hood / cap / case / boxed / packaging

These should remain overlay or deferred metadata in round 1.

## Round-1 Candidate Decision

### Immediate core candidate

Recommended immediate future core row:

- `Leica APO-Vario-Elmarit-SL 90-280mm f/2.8-4`

Why this is strong enough for a future seed round:

- literature identity is clear and singular
- local title wording is stable across several independent title shapes
- priced KRW support exists
- the intended SL-side family separates cleanly from adjacent R, SL, and third-party tele zooms when the query keeps explicit `SL`, `90-280`, or `APO-Vario-Elmarit-SL` anchors

### Hold candidate

No explicit hold candidate is recommended in round 1.

### Deferred / overlay-only items

Do not open separate rows for:

- `APO`
- `OIS`
- `E82`
- filter-thread marker
- tripod collar
- hood / cap / case / boxed / packaging

### Hard-pin prohibited shorthand

Do not hard-pin:

- `90-280`
- `apo vario elmarit`
- `leica sl 90-280`
- `90 280 elmarit`

These remain too broad because they can drift into:

- `SL 24-90`
- `SL 16-35`
- `SL 100-400`
- Leica R `105-280`
- Leica R `70-180`
- Sigma / Panasonic / Lumix tele zooms
- accessory-only rows

## Round-1 Conclusion

Round-1 status for `APO-Vario-Elmarit-SL 90-280`:

- family is real in primary literature
- local title support is strong
- priced KRW support exists
- immediate core candidate count: `1`
- recommended first-pass core:
  - `Leica APO-Vario-Elmarit-SL 90-280mm f/2.8-4`
- explicit hold candidate:
  - none

Accordingly, this family looks seedable in a future narrow seed round, but this audit round itself should remain audit-only.
