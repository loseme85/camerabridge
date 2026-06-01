# Vario-APO-Elmarit-R 70-180 Taxonomy Audit - Round 1

Date: 2026-05-20

Scope: audit-only review for the Leica `Vario-APO-Elmarit-R 70-180` family. This round does not add seed rows, does not modify `entities/*.json`, does not modify `canonical_entities_index.json`, and does not change classifier/query/search behavior, ranking, or UI.

## Executive Summary

`Vario-APO-Elmarit-R 70-180` is literature-real, and unlike the neighboring `180mm` R-side prime families, the local title evidence already converges on one stable zoom family.

Round-1 conclusion:

- immediate recommended `core` candidate count: `1`
- recommended first-pass core:
  - `Leica Vario-APO-Elmarit-R 70-180mm f/2.8`
- explicit `hold` candidate:
  - none
- literature clearly supports a real Leica R `70-180mm f/2.8 Vario-APO-Elmarit-R` zoom family
- local title support is narrow but stable:
  - all clean local rows resolve to the same exact zoom family
  - priced observations cluster in a coherent range
- there is no meaningful local support for internal row splitting by `ROM`, `cam`, filter-thread marker, tripod collar, hood bundle, or case bundle

The safest round-1 answer is:

1. recognize `Leica Vario-APO-Elmarit-R 70-180mm f/2.8` as an immediate seedable candidate
2. do not open any internal version row
3. keep `APO-Telyt-R 180`, `APO-Elmarit-R 180`, non-APO `Elmarit-R 180`, classic `Elmar-R 180`, `APO-Summicron-R 180`, `APO-Telyt-R 280`, SL/L zoom, and third-party `70-200` / `80-200` zooms as hard boundaries

## Literature / Reference Base

### Source A: Leica Wiki - `70mm-180mm f/2.8 Vario-APO-Elmarit-R`

Leica Wiki documents `70mm-180mm f/2.8 Vario-APO-Elmarit-R` with:

- order nos.:
  - `11267`
  - `11279`
- production era:
  - `1995-2006`
- mount:
  - Leica R bayonet
- aperture:
  - `f/2.8 - f/22`
- filter mount:
  - internal thread for screw-in type filters `E77`
- hood:
  - built-in, telescopic, rubber-armored
- accessory:
  - `APO-EXTENDER-R 2x = 140-360 mm f/5.6 APO`
- inscription:
  - `VARIO-APO-ELMARIT-R 1:2.8/70-180`

Reference:

- [Leica Wiki - 70mm-180mm f/2.8 Vario-APO-Elmarit-R](https://wiki.l-camera-forum.com/leica-wiki.en/index.php?title=70mm%E2%80%93180mm_f/2.8_Vario-APO-Elmarit-R)

### Source B: Leica Camera Classic - `Vario-Apo-Elmarit-R 2,8/70-180mm`

Leica Classic also lists the same family under:

- `Vario-Apo-Elmarit-R 2,8/70-180mm`

with current used-market store references for both `11267` and `11279`, reinforcing that this is one stable Leica R zoom family rather than an adjacent-prime spillover.

References:

- [Leica Classic - Vario-Apo-Elmarit-R 2,8/70-180mm](https://classic.leica-camera.com/en/Leica-Systems/R-System/Lenses/Zoom-Lenses/Vario-Apo-Elmarit-R-2-8-70-180mm/)
- [Leica Classic - VARIO-APO-ELMARIT-R f/2.8/70-180 mm (11279)](https://classic.leica-camera.com/en/VARIO-APO-ELMARIT-R-f-2.8-70-180-mm-11279/11279SH-3780045)

### Source C: Leica Wiki - adjacent 180mm prime boundaries

The following are separately documented and must remain distinct:

- `180mm f/3.4 APO-Telyt-R`
- `180mm f/2.8 APO-Elmarit-R`
- `180mm f/2.8 Elmarit-R`
- `180mm f/4 Elmar-R`
- `180mm f/2 APO-Summicron-R`

References:

- [Leica Wiki - 180mm f/3.4 APO-Telyt-R](https://wiki.l-camera-forum.com/leica-wiki.en/index.php/180mm_f/3.4_APO-Telyt-R)
- [Leica Wiki - 180mm f/2.8 APO-Elmarit-R II](https://wiki.l-camera-forum.com/leica-wiki.en/index.php/180mm_f/2.8_APO-Elmarit-R_II)
- [Leica Wiki - 180mm f/2.8 Elmarit-R II](https://wiki.l-camera-forum.com/leica-wiki.en/index.php/180mm_f/2.8_Elmarit-R_II)
- [Leica Wiki - 180mm f/4 Elmar-R](https://wiki.l-camera-forum.com/leica-wiki.en/index.php/180mm_f/4_Elmar-R)
- [Leica Wiki - 180mm f/2 APO-Summicron-R](https://wiki.l-camera-forum.com/leica-wiki.en/index.php/180mm_f/2_APO-Summicron-R)

## Taxonomy Implication from Literature

Literature clearly supports:

- one real broad family:
  - `Leica Vario-APO-Elmarit-R 70-180mm f/2.8`

Literature also supports real metadata structure around:

- `ROM`
- `cam version`
- `E77`
- built-in hood
- `APO-EXTENDER-R 2x`

However, literature does not justify opening any internal split in round 1. The local seller pool does not surface stable row-level variants.

## Boundary Check

This family must remain separate from:

- `Leica APO-Telyt-R 180`
- `Leica APO-Elmarit-R 180`
- non-APO `Leica Elmarit-R 180`
- classic `Leica Elmar-R 180`
- `Leica APO-Summicron-R 180`
- `Leica APO-Telyt-R 280`
- `Leica APO-Telyt-M 135`
- `Leica Elmarit-R 135`
- `APO-Summicron-SL 90`
- `APO-Summicron-SL 180`
- `SL / L-mount` zooms
- third-party `70-200mm / 80-200mm` zooms
- hood-only / cap / case / accessory-only listings

## Local Listing Evidence

Analysis base:

- `data/raw/raw_*.json`

### Broad retrieval behavior

Exact zoom-form retrieval is stable.

In the current raw pool, the following broad-but-still-zoom-shaped queries collapse to the same family:

- `70-180`
- `vario apo elmarit 180`
- `apo elmarit 70-180`
- `70 180 apo`

Observed unique titles:

- `Leica R 70-180mm f2.8 Vario-Apo-Elmarit Black`
- `[위탁] R 70-180/2.8 Vario Apo Elmarit (Black)`
- `LEICA 70-180mm F2.8 VARIO-APO-ELMARIT-R sn.3697`

Interpretation:

- the focal-range wording itself is strongly family-shaping inside the current local pool
- however, broad shorthand like bare `70-180` should still be treated conservatively in seed design because future raw pools can attract `SL 70-200` or third-party `70-200 / 80-200` zooms

### Clean local R-side pool

After restricting to explicit `70-180mm`, explicit R-side `Vario-APO-Elmarit-R` wording, and excluding `APO-Telyt-R 180`, `APO-Elmarit-R 180`, non-APO `Elmarit-R 180`, classic `Elmar-R 180`, `APO-Summicron-R 180`, `APO-Telyt-R 280`, SL/L, third-party, and accessory contamination, the usable pool becomes:

- clean local pool: `3`
- unique titles: `3`
- KRW-priced count: `2`
- KRW median: `4,125,000 KRW`

Representative clean titles:

- `Leica R 70-180mm f2.8 Vario-Apo-Elmarit Black`
- `[위탁] R 70-180/2.8 Vario Apo Elmarit (Black)`
- `LEICA 70-180mm F2.8 VARIO-APO-ELMARIT-R sn.3697`

Observed price points:

- `3,700,000 KRW`
- `3,850,000 KRW`
- `4,400,000 KRW`

Interpretation:

- local wording is stable
- the price cluster is coherent
- the family behaves like one zoom row rather than a set of unstable adjacent telephoto candidates

## Marker / Metadata Observation

Within the current local `70-180 APO-Elmarit-R` pool, seller wording does not reliably stabilize row-level internal splits for:

- `ROM`
- `cam`
- `E77`
- tripod collar
- hood / case / boxed
- `APO-EXTENDER-R`

Observed local marker distribution:

- `ROM`: `0`
- `cam`: `0`
- filter-thread marker: `0`
- tripod collar wording: `0`
- hood / case / box wording: `0`
- extender wording: `0`

These should remain overlay or deferred metadata in round 1.

## Candidate Assessment

### immediate core candidate

- `Leica Vario-APO-Elmarit-R 70-180mm f/2.8`

Reason:

- literature-real
- explicit local title support exists
- local title shapes are stable
- priced observations exist
- boundary against `180mm` primes is strong because the zoom-range wording is explicit

### hold candidate

None.

The local evidence supports one narrow main row more naturally than any explicit-wording-only hold row.

## Overlay / Deferred Elements

Do not create separate rows for:

- `ROM`
- `cam version`
- `E77`
- `filter thread`
- tripod collar
- built-in hood
- hood included
- cap included
- boxed
- case included
- condition
- original cap
- original hood
- original box
- original case
- packaging
- `APO-EXTENDER-R included`

## Out-of-Family Boundary

Must remain hard-separated from:

- `Leica APO-Telyt-R 180`
- `Leica APO-Elmarit-R 180`
- non-APO `Leica Elmarit-R 180`
- classic `Leica Elmar-R 180`
- `Leica APO-Summicron-R 180`
- `Leica APO-Telyt-R 280`
- `Leica APO-Telyt-M 135`
- `Leica Elmarit-R 135`
- `APO-Summicron-SL 90`
- `APO-Summicron-SL 180`
- `SL / L-mount` zooms
- third-party `70-200mm / 80-200mm` telephoto zooms
- accessory-only listings

## Round-1 Decision

Round-1 final answer:

- immediate `core` candidate:
  - `Leica Vario-APO-Elmarit-R 70-180mm f/2.8`
- explicit `hold` candidate:
  - none

## Next Seed Round Readiness

Ready.

If the next round opens one Leica R zoom family seed, this is a good candidate to add first, narrowly and explicitly as:

- `Leica Vario-APO-Elmarit-R 70-180mm f/2.8`

The family should still avoid over-broad aliasing:

- bare `70-180`
- bare `70 180 apo`

should be treated more cautiously than explicit `Vario-APO-Elmarit-R` or `Leica R 70-180mm f/2.8` wording.

## Validation

This round is audit-only, so the expected result is no change in normalization behavior or golden-set output after report creation.
