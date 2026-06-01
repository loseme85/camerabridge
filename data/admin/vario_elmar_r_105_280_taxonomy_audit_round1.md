# Vario-Elmar-R 105-280 Taxonomy Audit - Round 1

Date: 2026-05-20

Scope: audit-only review for the Leica `Vario-Elmar-R 105-280` family. This round does not add seed rows, does not modify `entities/*.json`, does not modify `canonical_entities_index.json`, and does not change classifier/query/search behavior, ranking, or UI.

## Executive Summary

`Vario-Elmar-R 105-280` is literature-real, but round-1 local support is still too thin to justify seed activation.

Round-1 conclusion:

- immediate recommended `core` candidate count: `0`
- recommended first-pass core:
  - none
- strongest deferred candidate:
  - `Leica Vario-Elmar-R 105-280mm f/4.2`
- explicit `hold` candidate:
  - none
- literature clearly supports a real Leica R `105-280mm f/4.2 Vario-Elmar-R` zoom family
- local title support is explicit but collapses to one abbreviated `ROM` title shape only
- broad `105-280` / `leica r 105-280` retrieval is vulnerable to drift into neighboring Leica R zooms, SL/L long zooms, and third-party telephoto zooms

The safest round-1 answer is:

1. keep `Leica Vario-Elmar-R 105-280mm f/4.2` closed for now
2. do not open any `core` or `hold` row
3. keep `Vario-APO-Elmarit-R 70-180`, `Vario-Elmar-R 70-210`, `Vario-Elmar-R 80-200`, older `80-200mm f/4.5`, the R-side `180mm / 280mm` primes, SL/L zooms, and third-party `70-200 / 70-300 / 100-300` zooms as hard boundaries

## Literature / Reference Base

### Source A: Leica Wiki - `105mm-280mm f/4.2 Vario-Elmar-R`

Leica Wiki documents `105mm-280mm f/4.2 Vario-Elmar-R` with:

- order no.:
  - `11268`
- production era:
  - `1996-2006`
- mount:
  - Leica R bayonet, including ROM-era compatibility on later R bodies
- optical structure:
  - `13 / 10`
- focusing range:
  - `1.7 m` to infinity
- aperture range:
  - listed from roughly `f/4.2` through `f/22`
- inscription:
  - `VARIO-ELMAR-R 1:4.2 /105-280`

References:

- [Leica Wiki - 105mm-280mm f/4.2 Vario-Elmar-R](https://wiki.l-camera-forum.com/leica-wiki.en/index.php/105mm%E2%80%93280mm_f/4.2_Vario-Elmar-R)
- [Leica Classic - Vario-Elmar-R 4,2/105-280mm](https://classic.leica-camera.com/en/Leica-Systems/R-System/Lenses/Zoom-Lenses/Vario-Elmar-R-4-2-105-280mm/)

### Source B: Leica Classic - ROM listing confirmation

Leica Classic separately shows used-store entries for both:

- `Leica Vario-Elmar-R 1:4,2/105-280mm`
- `Leica Vario-Elmar-R 11268 4,2/105-280mm ROM`

This reinforces that:

- the family is real
- `ROM` is a real market marker
- but `ROM` is best treated as metadata or overlay in round 1 rather than as a separate row

Reference:

- [Leica Classic - Leica Vario-Elmar-R 4,2/105-280mm ROM](https://classic.leica-camera.com/en/Leica-Vario-Elmar-R-4-2-105-280mm-ROM/11268SH-3734549)

### Source C: adjacent Leica R zoom boundaries

Separate neighboring zoom families are independently documented:

- `70mm-180mm f/2.8 Vario-APO-Elmarit-R`
- `70mm-210mm f/4 Vario-Elmar-R`
- `80mm-200mm f/4 Vario-Elmar-R`
- older `80mm-200mm f/4.5 Vario-Elmar-R`

References:

- [Leica Wiki - 70mm-180mm f/2.8 Vario-APO-Elmarit-R](https://wiki.l-camera-forum.com/leica-wiki.en/index.php?title=70mm%E2%80%93180mm_f%2F2.8_Vario-APO-Elmarit-R)
- [Leica Wiki - 70mm-210mm f/4 Vario-Elmar-R](https://wiki.l-camera-forum.com/leica-wiki.en/index.php/70mm%E2%80%93210mm_f/4_Vario-Elmar-R)
- [Leica Wiki - 80mm-200mm f/4 Vario-Elmar-R](https://wiki.l-camera-forum.com/leica-wiki.en/index.php/80mm%E2%80%93200mm_f/4_Vario-Elmar-R)
- [Leica Wiki - 80mm-200mm f/4.5 Vario-Elmar-R](https://wiki.l-camera-forum.com/leica-wiki.en/index.php/80mm%E2%80%93200mm_f/4.5_Vario-Elmar-R)

### Source D: SL / L long-zoom boundary

Modern long zooms such as the SL `90-280mm` line are separately documented under the SL system and should remain out of family.

References:

- [Leica Camera - APO-Vario-Elmarit-SL 90-280 f/2.8-4](https://leica-camera.com/en-int/photography/lenses/sl/apo-vario-elmarit-sl-90-280mm-f2-8-4-black)
- [Leica Classic - Leica 90-280 APO-Vario Elmarit-SL f/2.8-4 ASPH](https://classic.leica-camera.com/en/Leica-90-280-APO-Vario-Elmarit-SL-f-2.8-4-ASPH/11175SH-4572457)

## Taxonomy Implication from Literature

Literature clearly supports:

- one real broad family:
  - `Leica Vario-Elmar-R 105-280mm f/4.2`

Literature also supports meaningful metadata around:

- `ROM`
- `cam version`
- built-in hood
- filter or filter-system markers
- tripod-collar / grip ecosystem
- case and bundled accessory context

However, literature does not justify round-1 seed activation by itself. The deciding question is whether local seller titles stabilize this family as a usable row. In the current raw pool, they do not.

## Boundary Check

This family must remain separate from:

- `Leica Vario-APO-Elmarit-R 70-180mm f/2.8`
- `Leica Vario-Elmar-R 70-210mm f/4`
- `Leica Vario-Elmar-R 80-200mm f/4`
- older `Leica Vario-Elmar-R 80-200mm f/4.5`
- `Leica APO-Telyt-R 180`
- `Leica APO-Elmarit-R 180`
- non-APO `Leica Elmarit-R 180`
- `Leica APO-Summicron-R 180`
- `Leica APO-Telyt-R 280`
- `APO-Vario-Elmarit-SL 90-280`
- `SL / L-mount` zooms
- third-party `100-300mm / 70-300mm / 70-200mm / 80-200mm` zooms
- hood-only / cap / case / accessory-only listings

## Local Listing Evidence

Analysis base:

- `data/raw/raw_*.json`
- `data/derived/results_resolved_v2.json`

### Broad retrieval behavior

Broad shorthand is risky.

Within the wider `vario elmar` and long-zoom raw field, distinct non-family lines appear immediately:

- `Leica R 70-180mm f2.8 Vario-Apo-Elmarit Black`
- `[위탁] R 70-210/4 Vario-Elmar`
- `LEICA 80-200mm F4 VARIO-ELMAR-R sn.3699`
- `[중고] R 105-280/4.2 ROM (Black)`
- `[중고] SL APO Vario Elmarit 90-280 f/2.8-4`
- `LEICA 90-280mm F2.8-4 APO-VARIO-ELMARIT-SL sn.4575`
- `Lumix S Pro 70-200mm f4 OIS Black`
- `Panasonic 70-200mm F4 OIS Pro S`

Interpretation:

- bare `105-280`
- broad `vario elmar`
- broad `leica r 105-280`
- broad `105 280 elmar`

are not safe shaping aliases in round 1 because the wider retrieval field already mixes adjacent Leica R zooms, SL/L long zooms, and non-Leica telephoto zooms.

### Clean local R-side pool

After restricting to explicit `105-280mm`, explicit R-side range/aperture wording, and excluding `70-180`, `70-210`, `80-200`, `90-280`, the R-side `180mm / 280mm` primes, SL/L, third-party, and accessory contamination, the usable pool becomes:

- clean local pool: `1`
- unique titles: `1`
- KRW-priced count: `1`
- KRW median: `5,800,000 KRW`

Representative clean title:

- `[중고] R 105-280/4.2 ROM (Black)`

Observed price:

- `5,800,000 KRW`

Interpretation:

- the title is family-correct in range, aperture, mount, and ROM-era context
- but the local pool is still effectively one abbreviated listing pattern
- current evidence is too thin for round-1 seed activation

### Explicit wording stability

An additional issue is that the current local pool does not show repeated full-string `Vario-Elmar-R 105-280mm` wording.

In the present resolved pool:

- explicit `Leica Vario-Elmar-R 105-280mm f/4.2` title wording: `0`
- abbreviated `R 105-280/4.2 ROM` title wording: `1`

That makes the family literature-real but still title-thin in the local market snapshot.

## Marker / Metadata Observation

Within the current clean `105-280 Vario-Elmar-R` pool, seller wording does not reliably stabilize row-level internal splits for:

- `ROM`
- `cam`
- exact filter-thread wording
- tripod collar or grip wording
- hood / case / boxed

Observed local marker distribution:

- `ROM`: `1`
- `cam`: `0`
- exact filter-thread marker: `0`
- tripod collar wording: `0`
- hood / case / box wording: `0`

Interpretation:

- `ROM` is visible and literature-real, but still not repeated strongly enough to justify a separate row
- filter-thread and support-accessory markers remain metadata rather than row splits

These should remain overlay or deferred metadata in round 1.

## Smoke Query Review

The following explicit queries are literature-correct and point toward the same intended family:

- `vario-elmar-r 105-280`
- `vario elmar r 105-280`
- `105-280 vario-elmar-r`
- `105-280mm f4.2 vario-elmar-r`
- `105-280mm f/4.2 vario-elmar-r`
- `r 105-280/4.2 vario elmar`
- `leica r 105-280mm f4.2`
- `leica r 105-280mm f/4.2`

But round-1 local support is still only one clean title shape, and that title is abbreviated seller shorthand rather than repeated full-family wording, so these are not enough to justify seed activation yet.

The following broader shorthands are not safe:

- bare `105-280`
- broad `vario elmar`
- broad `leica r 105-280`
- broad `105 280 elmar`

because they can drift into:

- `Leica Vario-APO-Elmarit-R 70-180mm f/2.8`
- `Leica Vario-Elmar-R 70-210mm f/4`
- `Leica Vario-Elmar-R 80-200mm f/4`
- older `Leica Vario-Elmar-R 80-200mm f/4.5`
- `Leica APO-Vario-Elmarit-SL 90-280`
- `Lumix / Panasonic 70-200mm`
- future third-party `70-300mm / 100-300mm` zooms

## Candidate Assessment

### immediate core candidate

None.

Although the family is literature-real and the one clean local title is directionally correct, round-1 usable local evidence is still too thin.

### strongest deferred candidate

- `Leica Vario-Elmar-R 105-280mm f/4.2`

### hold candidate

None.

The current evidence does not support a separate explicit-wording-only hold row. It supports a deferred family review instead.

## Overlay / Deferred Elements

Do not create separate rows for:

- `ROM`
- `cam version`
- exact filter-thread marker
- tripod collar / grip ecosystem
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

## Out-of-Family / Hard Boundary

Must remain out of family:

- `Leica Vario-APO-Elmarit-R 70-180mm f/2.8`
- `Leica Vario-Elmar-R 70-210mm f/4`
- `Leica Vario-Elmar-R 80-200mm f/4`
- older `Leica Vario-Elmar-R 80-200mm f/4.5`
- `Leica APO-Telyt-R 180`
- `Leica APO-Elmarit-R 180`
- non-APO `Leica Elmarit-R 180`
- `Leica APO-Summicron-R 180`
- `Leica APO-Telyt-R 280`
- `APO-Vario-Elmarit-SL 90-280`
- `SL / L-mount` zooms
- third-party `100-300mm / 70-300mm / 70-200mm / 80-200mm` zooms
- accessory-only listings

## Round-1 Verdict

- immediate core candidate:
  - `0`
- recommended first-pass core:
  - none
- strongest deferred candidate:
  - `Leica Vario-Elmar-R 105-280mm f/4.2`
- explicit hold candidate:
  - none

Final round-1 decision:

- `seed 보류`

Why:

1. the family is literature-real
2. the local clean pool is only `1`
3. the only clean local title shape is `[중고] R 105-280/4.2 ROM (Black)`
4. the current local market does not repeatedly expose full `Vario-Elmar-R 105-280mm` wording
5. broad `105-280` / `vario elmar` retrieval already drifts into adjacent Leica zooms, SL/L long zooms, and non-Leica zooms

## Next-Round Recommendation

Do not add seed yet.

Revisit when:

- multiple clean local titles appear for the `105-280mm f/4.2` family
- KRW-priced support is no longer single-listing
- local seller wording repeatedly exposes full family naming rather than only abbreviated `R 105-280/4.2 ROM`
- local pool shows stable separation from:
  - `70-180mm f/2.8`
  - `70-210mm f/4`
  - `80-200mm f/4`
  - `90-280mm` SL zoom contamination
  - future third-party `70-300mm / 100-300mm` retrieval drift
