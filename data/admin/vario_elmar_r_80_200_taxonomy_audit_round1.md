# Vario-Elmar-R 80-200 Taxonomy Audit - Round 1

Date: 2026-05-20

Scope: audit-only review for the Leica `Vario-Elmar-R 80-200` family. This round does not add seed rows, does not modify `entities/*.json`, does not modify `canonical_entities_index.json`, and does not change classifier/query/search behavior, ranking, or UI.

## Executive Summary

`Vario-Elmar-R 80-200` is literature-real, but round-1 local support is still too thin to justify seed activation.

Round-1 conclusion:

- immediate recommended `core` candidate count: `0`
- recommended first-pass core:
  - none
- strongest deferred candidate:
  - `Leica Vario-Elmar-R 80-200mm f/4`
- explicit `hold` candidate:
  - none
- literature clearly supports a real Leica R `80-200mm f/4 Vario-Elmar-R` zoom family
- literature also shows that this is not the same family as the older `80-200mm f/4.5 Vario-Elmar-R`
- local title support is explicit but collapses to one title shape only
- broad `80-200` / `leica r 80-200` retrieval drifts into adjacent Leica R zooms and non-Leica `70-200` zooms

The safest round-1 answer is:

1. keep `Leica Vario-Elmar-R 80-200mm f/4` closed for now
2. do not open any `core` or `hold` row
3. keep `Vario-APO-Elmarit-R 70-180`, `Vario-Elmar-R 70-210`, `Vario-Elmar-R 105-280`, the R-side `180mm / 280mm` primes, SL/L zooms, and third-party `70-200 / 80-200` zooms as hard boundaries

## Literature / Reference Base

### Source A: Leica Wiki - `80mm–200mm f/4 Vario-Elmar-R`

Leica Wiki documents `80mm–200mm f/4 Vario-Elmar-R` with:

- order nos.:
  - `11280`
  - `11281-ROM`
- production era:
  - `1996-2009`
- mount:
  - Leica R bayonet
- aperture:
  - `f/4 - f/22`
- filter mount / hood:
  - `E60`
  - built-in telescopic hood
- accessories:
  - `APO-EXTENDER-R 2x`
  - `STA-1` tripod collar
- inscription:
  - `VARIO-ELMAR-R 1:4 /80-200 E 60`

References:

- [Leica Wiki - 80mm-200mm f/4 Vario-Elmar-R](https://wiki.l-camera-forum.com/leica-wiki.en/index.php/80mm%E2%80%93200mm_f/4_Vario-Elmar-R)
- [Leica Classic - Vario-Elmar-R 4/80-200mm](https://classic.leica-camera.com/en/Leica-Systems/R-System/Lenses/Zoom-Lenses/Vario-Elmar-R-4-80-200mm/)

### Source B: older `80mm–200mm f/4.5 Vario-Elmar-R` boundary

Leica Wiki separately documents an older:

- `80mm–200mm f/4.5 Vario-Elmar-R`

with:

- order no.:
  - `11224`
- production era:
  - `1974-1978`
- manufacturer:
  - `Minolta`
- filter mount / hood:
  - `E60`
  - built-in telescopic hood
- inscription:
  - `VARIO-ELMAR-R 1:4.5 / 80 - 200`

This is a real adjacent family and should not be merged into the later `f/4` row.

References:

- [Leica Wiki - 80mm-200mm f/4.5 Vario-Elmar-R](https://wiki.l-camera-forum.com/leica-wiki.en/index.php/80mm%E2%80%93200mm_f/4.5_Vario-Elmar-R)
- [Leica Classic - Vario-Elmar-R 4,5/80-200mm](https://classic.leica-camera.com/en/Leica-Systems/R-System/Lenses/Zoom-Lenses/Vario-Elmar-R-4-5-80-200mm/)

### Source C: adjacent Leica R zoom boundaries

Separate neighboring zoom families are independently documented:

- `70mm–180mm f/2.8 Vario-APO-Elmarit-R`
- `70mm–210mm f/4 Vario-Elmar-R`
- `105mm–280mm f/4.2 Vario-Elmar-R`

References:

- [Leica Wiki - 70mm-180mm f/2.8 Vario-APO-Elmarit-R](https://wiki.l-camera-forum.com/leica-wiki.en/index.php?title=70mm%E2%80%93180mm_f%2F2.8_Vario-APO-Elmarit-R)
- [Leica Wiki - 70mm-210mm f/4 Vario-Elmar-R](https://wiki.l-camera-forum.com/leica-wiki.en/index.php/70mm%E2%80%93210mm_f/4_Vario-Elmar-R)
- [Leica Classic - Vario-Elmar-R 4,2/105-280mm](https://classic.leica-camera.com/en/Leica-Systems/R-System/Lenses/Zoom-Lenses/Vario-Elmar-R-4-2-105-280mm/)

## Taxonomy Implication from Literature

Literature clearly supports:

- one real broad family:
  - `Leica Vario-Elmar-R 80-200mm f/4`

Literature also supports meaningful internal metadata:

- `ROM`
- `cam version`
- `E60`
- built-in hood
- `STA-1` tripod collar
- `APO-EXTENDER-R 2x`

However, literature does not justify round-1 seed activation by itself. The deciding question is whether local seller titles stabilize this family as a usable row. In the current raw pool, they do not.

## Boundary Check

This family must remain separate from:

- `Leica Vario-APO-Elmarit-R 70-180mm f/2.8`
- `Leica Vario-Elmar-R 70mm-210mm f/4`
- `Leica Vario-Elmar-R 105mm-280mm f/4.2`
- `Leica APO-Telyt-R 180`
- `Leica APO-Elmarit-R 180`
- non-APO `Leica Elmarit-R 180`
- `Leica APO-Summicron-R 180`
- `Leica APO-Telyt-R 280`
- older `Leica Vario-Elmar-R 80-200mm f/4.5`
- `SL / L-mount` zooms
- third-party `70-200mm / 80-200mm` zooms
- hood-only / cap / case / accessory-only listings

## Local Listing Evidence

Analysis base:

- `data/raw/raw_*.json`
- `data/derived/results_resolved_v2.json`

### Broad retrieval behavior

Broad range retrieval is risky.

Within the wider `70-200 / 80-200` raw field, distinct non-family lines appear immediately:

- `LEICA 80-200mm F4 VARIO-ELMAR-R sn.3699`
- `LEICA 70-210mm F4 VARIO-ELMAR-R sn.3582`
- `[위탁] R 70-210/4 Vario-Elmar`
- `[중고] R 105-280/4.2 ROM (Black)`
- `Lumix S Pro 70-200mm f4 OIS Black`
- `Panasonic 70-200mm F4 OIS Pro S`

Interpretation:

- bare `80-200`
- broad `vario elmar`
- broad `leica r 80-200`
- broad `80 200 elmar`

are not safe shaping aliases in round 1 because the wider retrieval field already mixes adjacent Leica R zooms and non-Leica `70-200` zooms.

### Clean local R-side pool

After restricting to explicit `80-200mm`, explicit R-side `Vario-Elmar-R` wording, and excluding `70-180`, `70-210`, `105-280`, the R-side `180mm / 280mm` primes, SL/L, third-party, and accessory contamination, the usable pool becomes:

- clean local pool: `1`
- unique titles: `1`
- KRW-priced count: `1`
- KRW median: `600,000 KRW`

Representative clean title:

- `LEICA 80-200mm F4 VARIO-ELMAR-R sn.3699`

Observed price:

- `600,000 KRW`

Interpretation:

- the explicit title is family-correct
- but the local pool is still effectively one repeated listing pattern
- current evidence is too thin for round-1 seed activation

## Marker / Metadata Observation

Within the current clean `80-200 Vario-Elmar-R` pool, seller wording does not reliably stabilize row-level internal splits for:

- `ROM`
- `cam`
- `E60`
- tripod collar
- hood / case / boxed
- `APO-EXTENDER-R`

Observed local marker distribution:

- `ROM`: `0`
- `cam`: `0`
- `filter-thread marker`: `0`
- `tripod collar wording`: `0`
- `hood / case / box wording`: `0`
- `extender wording`: `0`

These should remain overlay or deferred metadata in round 1.

## Smoke Query Review

The following explicit queries are literature-correct and point toward the same intended family:

- `vario-elmar-r 80-200`
- `vario elmar r 80-200`
- `80-200 vario-elmar-r`
- `80-200mm f4 vario-elmar-r`
- `80-200mm f/4 vario-elmar-r`
- `r 80-200/4 vario elmar`
- `leica r 80-200mm f4`
- `leica r 80-200mm f/4`

But round-1 local support is still only one clean title shape, so these are not enough to justify seed activation yet.

The following broader shorthands are not safe:

- bare `80-200`
- broad `vario elmar`
- broad `leica r 80-200`
- broad `80 200 elmar`

because they can drift into:

- `Leica Vario-Elmar-R 70-210mm f/4`
- `Leica Vario-Elmar-R 105-280mm f/4.2`
- `Lumix / Panasonic 70-200mm`
- future third-party `70-200 / 80-200` zooms

## Candidate Assessment

### immediate core candidate

None.

Although the family is literature-real and the one clean local title is correct, round-1 usable local evidence is still too thin.

### strongest deferred candidate

- `Leica Vario-Elmar-R 80-200mm f/4`

### hold candidate

None.

The current evidence does not support a separate explicit-wording-only hold row. It supports a deferred family review instead.

## Overlay / Deferred Elements

Do not create separate rows for:

- `ROM`
- `cam version`
- `E60`
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

## Out-of-Family / Hard Boundary

Must remain out of family:

- `Leica Vario-APO-Elmarit-R 70-180mm f/2.8`
- `Leica Vario-Elmar-R 70mm-210mm f/4`
- `Leica Vario-Elmar-R 105mm-280mm f/4.2`
- `Leica APO-Telyt-R 180`
- `Leica APO-Elmarit-R 180`
- non-APO `Leica Elmarit-R 180`
- `Leica APO-Summicron-R 180`
- `Leica APO-Telyt-R 280`
- older `Leica Vario-Elmar-R 80-200mm f/4.5`
- `SL / L-mount` zooms
- third-party `70-200mm / 80-200mm` zooms
- accessory-only listings

## Round-1 Verdict

- immediate core candidate:
  - `0`
- recommended first-pass core:
  - none
- strongest deferred candidate:
  - `Leica Vario-Elmar-R 80-200mm f/4`
- explicit hold candidate:
  - none

Final round-1 decision:

- `seed 보류`

Why:

1. the family is literature-real
2. the local clean pool is only `1`
3. the only clean local title shape is `LEICA 80-200mm F4 VARIO-ELMAR-R sn.3699`
4. broad `80-200` / `vario elmar` retrieval already drifts into adjacent Leica zooms and non-Leica `70-200` zooms
5. the older `80-200mm f/4.5 Vario-Elmar-R` is a real neighboring family, so even `80-200 vario elmar` needs care

## Next-Round Recommendation

Do not add seed yet.

Revisit when:

- multiple clean local titles appear for the `f/4` family
- KRW-priced support is no longer single-listing
- local seller wording shows that the later `f/4` family can be stably separated from:
  - older `80-200mm f/4.5`
  - `70-210mm f/4`
  - `105-280mm f/4.2`
  - `70-200mm` SL/L or third-party zoom contamination
