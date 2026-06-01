# APO-Summicron-R 180 Taxonomy Audit - Round 1

Date: 2026-05-17

Scope: audit-only review for the Leica `APO-Summicron-R 180` family. This round does not add seed rows, does not modify `entities/*.json`, does not modify `canonical_entities_index.json`, and does not change classifier/query/search behavior, ranking, or UI.

## Executive Summary

`APO-Summicron-R 180` is literature-real, but round-1 local support is far too thin to justify immediate seed activation.

Round-1 conclusion:

- immediate recommended `core` candidate count: `0`
- recommended first-pass core:
  - none
- strongest deferred candidate:
  - `Leica APO-Summicron-R 180mm f/2`
- explicit `hold` candidate:
  - none
- literature clearly supports a real Leica R `180mm f/2 APO-Summicron-R` family
- literature also supports real internal marker structure:
  - `ROM`
  - `E100`
  - filter drawer / built-in hood structure
  - `APO-EXTENDER-R 2x`
- but local title support collapses to a single repeated modified-title pattern

The safest round-1 answer is:

1. keep `APO-Summicron-R 180` closed for now
2. do not open any `core` or `hold` row
3. keep `APO-Telyt-R 180`, `APO-Elmarit-R 180`, non-APO `Elmarit-R 180`, classic `Elmar-R 180`, `Vario-APO-Elmarit-R 70-180`, `APO-Telyt-R 280`, SL/L telephoto, and third-party telephoto lines as hard boundaries

## Literature / Reference Base

### Source A: Leica Wiki - `180mm f/2 APO-Summicron-R`

Leica Wiki documents `180mm f/2 APO-Summicron-R` with:

- order nos.:
  - `11271`
  - `11354-ROM`
- production era:
  - `1994-2009`
- aperture:
  - `f/2 - f/16`
- filter structure:
  - Series 6 filters in filter drawer
  - additional internal thread for screw-in type filters `E100`
- hood:
  - built-in, telescopic, rubber-armored
- accessory:
  - `APO-EXTENDER-R 2x = 360 mm f/4 APO`
- inscription:
  - `APO-SUMMICRON-R 1:2/180`

Reference:

- [Leica Wiki - 180mm f/2 APO-Summicron-R](https://wiki.l-camera-forum.com/leica-wiki.en/index.php/180mm_f/2_APO-Summicron-R)

### Source B: Leica Wiki - `180mm f/3.4 APO-Telyt-R`

For adjacent APO telephoto boundary, Leica Wiki separately documents:

- `180mm f/3.4 APO-Telyt-R`

Reference:

- [Leica Wiki - 180mm f/3.4 APO-Telyt-R](https://wiki.l-camera-forum.com/leica-wiki.en/index.php/180mm_f/3.4_APO-Telyt-R)

### Source C: Leica Wiki - `180mm f/2.8 APO-Elmarit-R II`

For adjacent fast APO telephoto boundary, Leica Wiki separately documents:

- `180mm f/2.8 APO-Elmarit-R II`

with:

- `E67`
- built-in hood
- rotating tripod collar support

Reference:

- [Leica Wiki - 180mm f/2.8 APO-Elmarit-R II](https://wiki.l-camera-forum.com/leica-wiki.en/index.php/180mm_f/2.8_APO-Elmarit-R_II)

### Source D: Leica Wiki - `180mm f/2.8 Elmarit-R II`

For non-APO boundary, Leica Wiki separately documents:

- `180mm f/2.8 Elmarit-R II`

with:

- `3-cam`
- `R-only`
- `E67`

Reference:

- [Leica Wiki - 180mm f/2.8 Elmarit-R II](https://wiki.l-camera-forum.com/leica-wiki.en/index.php/180mm_f/2.8_Elmarit-R_II)

### Source E: Leica Wiki - `70mm-180mm f/2.8 Vario-APO-Elmarit-R`

For zoom boundary, Leica Wiki separately documents:

- `70mm-180mm f/2.8 Vario-APO-Elmarit-R`

Reference:

- [Leica Wiki - 70mm-180mm f/2.8 Vario-APO-Elmarit-R](https://wiki.l-camera-forum.com/leica-wiki.en/index.php?title=70mm%E2%80%93180mm_f%2F2.8_Vario-APO-Elmarit-R)

## Taxonomy Implication from Literature

Literature clearly supports:

- one real broad family:
  - `Leica APO-Summicron-R 180mm f/2`

Literature also supports real metadata structure:

- `ROM`
- `E100`
- filter drawer
- built-in hood
- `APO-EXTENDER-R 2x`

However, literature does not support opening any internal split in round 1. There is no local basis for row-level separation by `ROM`, filter detail, or accessory bundle.

## Boundary Check

This family must remain separate from:

- `Leica APO-Telyt-R 180mm f/3.4`
- `Leica APO-Elmarit-R 180mm f/2.8`
- non-APO `Leica Elmarit-R 180mm f/2.8`
- classic `Leica Elmar-R 180mm f/4`
- generic `Telyt 180`
- `Leica Vario-APO-Elmarit-R 70-180mm f/2.8`
- `Leica APO-Telyt-R 280`
- `Leica APO-Telyt-M 135`
- `Leica Elmarit-R 135`
- `Leica Tele-Elmar 135`
- `SL / L-mount` telephoto lines
- third-party `180mm f/2` or adjacent telephoto lenses
- hood-only / cap / case / accessory-only listings

## Local Listing Evidence

Analysis base:

- `data/raw/raw_*.json`

### Broad retrieval behavior

Broad shorthand is not useful here.

When scanning the local raw pool for `180`, `apo`, and `summicron`, the only R-side candidate that survives is one repeated modified-title pattern:

- `Leica R 180mm f2 APO-Summicron Black [영상용 개조]`

Interpretation:

- broad `apo summicron 180`
- broad `summicron 180`
- broad `180 cron`
- broad `180 apo`

do not show a healthy multi-title market cluster in round 1. Instead, they collapse to one repeated seller phrasing.

### Clean local R-side pool

After restricting to explicit `180mm`, explicit R-side `APO-Summicron-R` wording, and excluding M-side `APO-Summicron`, SL/L, `APO-Telyt-R 180`, `APO-Elmarit-R 180`, non-APO `Elmarit-R 180`, classic `Elmar-R 180`, `Vario-APO-Elmarit-R 70-180`, `APO-Telyt-R 280`, third-party, and accessory contamination, the usable pool becomes:

- clean local pool: `1`
- unique titles: `1`
- KRW-priced count: `1`
- KRW median: `13,000,000 KRW`

Representative clean title:

- `Leica R 180mm f2 APO-Summicron Black [영상용 개조]`

### Quality note on local support

The local support is not just small. It is concentrated in one repeated modified listing:

- only one title shape
- repeated across multiple raw snapshots
- explicitly marked as `영상용 개조`

That makes round-1 evidence weaker than the raw price count alone might suggest.

## Marker / Metadata Observation

Within the current local `180 APO-Summicron-R` pool, seller wording does not reliably stabilize row-level internal splits for:

- `ROM`
- `cam`
- `E100`
- tripod collar
- hood / case / boxed

Observed local marker distribution in the raw pool:

- `ROM`: `0`
- `cam`: `0`
- `E100 / E67 / E60 / Series`: `0`
- tripod collar wording: `0`
- hood / case / box wording: `0`
- `영상용 개조` modification wording: repeated on all observed raw matches

These should remain overlay or deferred metadata in round 1.

## Candidate Assessment

### immediate core candidate

None.

Reason:

- only `1` clean local title
- only `1` priced observation
- the sole local evidence is a repeated modified listing rather than a stable broader market cluster

### strongest deferred candidate

- `Leica APO-Summicron-R 180mm f/2`

Reason:

- literature-real
- local title support exists
- price support exists
- but current local evidence is far too narrow for activation

### hold candidate

None.

There is no safer explicit-wording-only hold row than the base literature-real family candidate already identified. The correct round-1 action is deferral, not hold-row creation.

## Overlay / Deferred Elements

Do not create separate rows for:

- `ROM`
- `cam version`
- `E100`
- `filter thread`
- tripod collar
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
- `영상용 개조`

## Out-of-Family Boundary

Must remain hard-separated from:

- `Leica APO-Telyt-R 180`
- `Leica APO-Elmarit-R 180`
- non-APO `Leica Elmarit-R 180`
- classic `Leica Elmar-R 180`
- `Leica Vario-APO-Elmarit-R 70-180`
- `Leica APO-Telyt-R 280`
- `Leica APO-Telyt-M 135`
- `Leica Elmarit-R 135`
- `Leica Tele-Elmar 135`
- `SL / L-mount` telephoto lines
- third-party `180mm` telephoto lenses
- accessory-only listings

## Round-1 Decision

Round-1 final answer:

- immediate `core` candidate:
  - none
- strongest deferred candidate:
  - `Leica APO-Summicron-R 180mm f/2`
- explicit `hold` candidate:
  - none

## Next Seed Round Readiness

Not ready yet.

The next round becomes plausible only if:

- more than one clean title shape appears
- non-modified local listings appear in addition to the current `영상용 개조` entry
- KRW-priced support expands beyond the current repeated single-source pattern

## Validation

This round is audit-only, so the expected result is no change in normalization behavior or golden-set output after report creation.
