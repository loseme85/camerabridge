# APO-Telyt-R 280 Taxonomy Audit - Round 1

Date: 2026-05-16

Scope: audit-only review for the Leica `APO-Telyt-R 280` family. This round does not add seed rows, does not modify `entities/*.json`, does not modify `canonical_entities_index.json`, and does not change classifier/query/search behavior, ranking, or UI.

## Executive Summary

`APO-Telyt-R 280` is literature-real, and literature clearly supports two aperture-distinct rows inside the family:

- `Leica APO-Telyt-R 280mm f/2.8`
- `Leica APO-Telyt-R 280mm f/4`

However, round-1 local evidence is still too thin to justify immediate seed activation.

Round-1 conclusion:

- immediate recommended `core` candidate count: `0`
- recommended first-pass core:
  - none
- strongest deferred candidate:
  - `Leica APO-Telyt-R 280mm f/4`
- secondary deferred candidate:
  - `Leica APO-Telyt-R 280mm f/2.8`
- explicit `hold` candidate:
  - none
- literature clearly supports real Leica R `280mm APO-Telyt-R` lines
- local title support splits by aperture, but the usable pool remains narrow:
  - `f/4` has the only meaningful repeated local support
  - `f/2.8` appears only once in the clean local pool and has no KRW-priced support

The safest round-1 answer is:

1. keep `APO-Telyt-R 280` closed for now
2. do not open any `core` or `hold` row
3. treat `f/2.8` and `f/4` as literature-real internal row candidates, but defer both until local support is stronger
4. keep `APO-Telyt-R 180`, `APO-Elmarit-R 180`, `Elmarit-R 180`, `Elmar-R 180`, `Vario-APO-Elmarit-R 70-180`, SL/L telephoto, and third-party long telephoto lines as hard boundaries

## Literature / Reference Base

### Source A: Leica Wiki - `280mm f/2.8 APO-Telyt-R`

Leica Wiki documents `280mm f/2.8 APO-Telyt-R` as a real Leica R telephoto line with distinct fast-aperture positioning and dedicated lens construction.

Reference:

- [Leica Wiki - 280mm f/2.8 APO-Telyt-R](https://wiki.l-camera-forum.com/leica-wiki.en/index.php/280mm_f/2.8_APO-Telyt-R)

### Source B: Leica Wiki - `280mm f/4 APO-Telyt-R`

Leica Wiki separately documents `280mm f/4 APO-Telyt-R` as a different Leica R telephoto line, confirming that `f/2.8` and `f/4` are not just seller shorthand variants of the same row.

Reference:

- [Leica Wiki - 280mm f/4 APO-Telyt-R](https://wiki.l-camera-forum.com/leica-wiki.en/index.php/280mm_f/4_APO-Telyt-R)

### Source C: Leica Wiki - `180mm f/3.4 APO-Telyt-R`

For focal-length boundary, Leica Wiki separately documents:

- `180mm f/3.4 APO-Telyt-R`

Reference:

- [Leica Wiki - 180mm f/3.4 APO-Telyt-R](https://wiki.l-camera-forum.com/leica-wiki.en/index.php/180mm_f/3.4_APO-Telyt-R)

### Source D: Leica Wiki - `180mm f/2.8 APO-Elmarit-R`

For adjacent APO telephoto boundary, Leica Wiki separately documents:

- `180mm f/2.8 APO-Elmarit-R I`
- `180mm f/2.8 APO-Elmarit-R II`

References:

- [Leica Wiki - 180mm f/2.8 APO-Elmarit-R I](https://wiki.l-camera-forum.com/leica-wiki.en/index.php?title=180mm_f%2F2.8_APO-Elmarit-R_I)
- [Leica Wiki - 180mm f/2.8 APO-Elmarit-R II](https://wiki.l-camera-forum.com/leica-wiki.en/index.php/180mm_f/2.8_APO-Elmarit-R_II)

### Source E: Leica Wiki - `70mm-180mm f/2.8 Vario-APO-Elmarit-R`

For zoom boundary, Leica Wiki separately documents:

- `70mm-180mm f/2.8 Vario-APO-Elmarit-R`

Reference:

- [Leica Wiki - 70mm-180mm f/2.8 Vario-APO-Elmarit-R](https://wiki.l-camera-forum.com/leica-wiki.en/index.php?title=70mm%E2%80%93180mm_f%2F2.8_Vario-APO-Elmarit-R)

## Taxonomy Implication from Literature

Literature clearly supports:

- one broad Leica R family:
  - `Leica APO-Telyt-R 280`

Literature also supports two distinct aperture-level internal candidates:

- `Leica APO-Telyt-R 280mm f/2.8`
- `Leica APO-Telyt-R 280mm f/4`

Literature also suggests real metadata structure around:

- `ROM`
- `cam version`
- `E60`
- `E112`
- tripod collar
- hood / case ecosystem

But literature alone is not enough to open either row in round 1. The deciding question is whether local seller titles stabilize either aperture line strongly enough. In the current raw pool, they do not yet do so.

## Boundary Check

This family must remain separate from:

- `Leica APO-Telyt-R 180`
- `Leica APO-Elmarit-R 180`
- non-APO `Leica Elmarit-R 180`
- classic `Leica Elmar-R 180`
- `Leica Vario-APO-Elmarit-R 70-180`
- `Leica APO-Summicron-R 180`
- `Leica APO-Telyt-M 135`
- `Leica Elmarit-R 135`
- `Leica Tele-Elmar 135`
- `APO-Summicron-SL 90`
- `APO-Summicron-SL 180`
- `SL / L-mount` lenses
- third-party `280mm / 300mm` lenses
- hood-only / cap / case / accessory-only listings

## Local Listing Evidence

Analysis base:

- `data/raw/raw_*.json`

### Broad retrieval behavior

Broad shorthand is risky.

When the local raw pool is widened to `280` plus `apo` / `telyt`, distinct non-family or boundary-neighbor lines appear:

- `Leica R 180mm f3.4 APO-Telyt Black`
- `Leica R 180mm f2.8 APO-Elmart Rom Black`
- `Leica R 70-180mm f2.8 Vario-Apo-Elmarit Black`
- `Leica R280mm f2.8 Apo-Telyt Black`
- `Leica R 280mm f4 APO Telyt Black`
- `LEICA 280mm F4 APO-TELYT-R APO-EXTENDER-R sn.3622`
- `LEICA 180mm F2 APO-SUMMICRON-R sn.3783`

Interpretation:

- broad `apo telyt 280`
- broad `telyt 280`
- broad `280 apo`

cannot be trusted as shaping aliases in round 1 because the wider Leica R telephoto field includes multiple adjacent APO, non-APO, zoom, and extender-bundled lines.

### Clean local R-side pool

After restricting to explicit `280mm`, explicit R-side `APO-Telyt-R` wording, and excluding `APO-Telyt-R 180`, `APO-Elmarit-R 180`, non-APO `Elmarit-R 180`, classic `Elmar-R 180`, `Vario-APO-Elmarit-R 70-180`, M-side `APO-Telyt-M 135`, SL/L, third-party, and accessory contamination, the usable pool becomes:

- clean local pool: `5`
- unique titles: `5`
- KRW-priced count: `2`
- KRW median: `2,400,000 KRW`

Representative clean titles:

- `[위탁] R 280/4 APO telyt (Black)`
- `LEICA 280mm F4 APO-TELYT-R APO-EXTENDER-R sn.3622`
- `LEICA R280mm F2.8 APO-TELYT-R sn.3280`
- `LEICA 280mm F4 APO-TELYT-R sn.3658`
- `LEICA 280mm F4 APO-TELYT-R sn.3659`

### f/2.8 vs f/4 split

The local pool does not behave like one undifferentiated `280 APO-Telyt-R` price cluster.

Observed split:

- `Leica APO-Telyt-R 280mm f/4`
  - local count: `4`
  - KRW-priced count: `2`
  - KRW median: `2,400,000 KRW`
- `Leica APO-Telyt-R 280mm f/2.8`
  - local count: `1`
  - KRW-priced count: `0`
  - KRW median: none

Interpretation:

- title wording and price observations suggest `f/4` and `f/2.8` should not be merged into one canonical row
- however, only `f/4` has repeated local support
- `f/2.8` remains literature-real but locally too thin for round-1 activation

## Marker / Metadata Observation

Within the current local `280 APO-Telyt-R` pool, seller wording does not reliably stabilize row-level internal splits for:

- `ROM`
- `cam`
- `E60`
- `E112`
- tripod collar
- hood / case / boxed

These should remain overlay or deferred metadata in round 1.

`APO-EXTENDER-R` appears in at least one local title, but this behaves like bundle/accessory metadata rather than a stable row split.

## Candidate Assessment

### immediate core candidate

None.

Even though `f/4` is the strongest local line, round-1 support is still too narrow:

- only `4` clean titles
- only `2` KRW-priced observations
- title shapes are still clustered in a small seller pattern pool

### strongest deferred candidate

- `Leica APO-Telyt-R 280mm f/4`

Reason:

- literature-real
- explicit local title support exists
- price observations exist
- but the pool is still too small for immediate activation

### secondary deferred candidate

- `Leica APO-Telyt-R 280mm f/2.8`

Reason:

- literature-real
- explicit local title support exists
- but only one clean local title and zero KRW-priced support

### hold candidate

None.

No separate explicit-wording-only row is safer than the two literature-real aperture candidates already identified. Round-1 evidence points to deferral, not hold-row creation.

## Overlay / Deferred Elements

Do not create separate rows for:

- `ROM`
- `cam version`
- `E60 / E112`
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

## Out-of-Family Boundary

Must remain hard-separated from:

- `Leica APO-Telyt-R 180`
- `Leica APO-Elmarit-R 180`
- non-APO `Leica Elmarit-R 180`
- classic `Leica Elmar-R 180`
- `Leica Vario-APO-Elmarit-R 70-180`
- `Leica APO-Summicron-R 180`
- `Leica APO-Telyt-M 135`
- `Leica Elmarit-R 135`
- `Leica Tele-Elmar 135`
- `APO-Summicron-SL 90`
- `APO-Summicron-SL 180`
- `SL / L-mount` telephoto lines
- third-party `280mm / 300mm` telephoto lenses
- accessory-only listings

## Round-1 Decision

Round-1 final answer:

- immediate `core` candidate:
  - none
- strongest deferred candidate:
  - `Leica APO-Telyt-R 280mm f/4`
- secondary deferred candidate:
  - `Leica APO-Telyt-R 280mm f/2.8`
- explicit `hold` candidate:
  - none

## Next Seed Round Readiness

Not ready yet.

The next round becomes plausible only if:

- `Leica APO-Telyt-R 280mm f/4` gains more clean local title shapes
- KRW-priced support for `f/4` grows beyond the current thin pool
- `Leica APO-Telyt-R 280mm f/2.8` appears in more than a single clean local listing

If one line opens first, the evidence currently favors:

1. `Leica APO-Telyt-R 280mm f/4`
2. `Leica APO-Telyt-R 280mm f/2.8` only later, after distinct local support is established

## Validation

This round is audit-only, so the expected result is no change in normalization behavior or golden-set output after report creation.
