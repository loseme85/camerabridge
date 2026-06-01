# Vario-Elmar-R 70-210 Taxonomy Audit - Round 1

Date: 2026-05-20

Scope: audit-only review for the Leica `Vario-Elmar-R 70-210` family. This round does not add seed rows, does not modify `entities/*.json`, does not modify `canonical_entities_index.json`, and does not change classifier/query/search behavior, ranking, or UI.

## Executive Summary

`Vario-Elmar-R 70-210` is literature-real, but round-1 local support is still too thin to justify seed activation.

Round-1 conclusion:

- immediate recommended `core` candidate count: `0`
- recommended first-pass core:
  - none
- strongest deferred candidate:
  - `Leica Vario-Elmar-R 70-210mm f/4`
- explicit `hold` candidate:
  - none
- literature clearly supports a real Leica R `70-210mm f/4 Vario-Elmar-R` zoom family
- local title support is explicit but still only resolves to two narrow title shapes
- broad `70-210` / `leica r 70-210` retrieval drifts into adjacent Leica R zooms and non-Leica `70-200` zooms

The safest round-1 answer is:

1. keep `Leica Vario-Elmar-R 70-210mm f/4` closed for now
2. do not open any `core` or `hold` row
3. keep `Vario-APO-Elmarit-R 70-180`, `Vario-Elmar-R 80-200`, older `80-200mm f/4.5`, `Vario-Elmar-R 105-280`, the R-side `180mm / 280mm` primes, SL/L zooms, and third-party `70-200 / 70-210 / 80-200` zooms as hard boundaries

## Literature / Reference Base

### Source A: Leica Wiki - `70mm–210mm f/4 Vario-Elmar-R`

Leica Wiki documents `70mm–210mm f/4 Vario-Elmar-R` with:

- order no.:
  - `11246`
- production era:
  - `1984-2000`
- aperture:
  - `f/4 - f/22`
- filter type:
  - `E60`
- inscription:
  - `LEITZ VARIO-ELMAR-R 1:4/70-210 E60`
- note:
  - anniversary-edition marker is documented separately in literature

Reference:

- [Leica Wiki - 70mm-210mm f/4 Vario-Elmar-R](https://wiki.l-camera-forum.com/leica-wiki.en/index.php/70mm%E2%80%93210mm_f/4_Vario-Elmar-R)

### Source B: Leica Classic - `Vario-Elmar-R 4/70-210mm`

Leica Classic also lists the same family under:

- `Vario-Elmar-R 4/70-210mm`
- `Leitz Vario-Elmar-R 4.0/70-210mm`

with used-market store entries across multiple years and conditions, reinforcing that this is a stable Leica R zoom family rather than spillover from adjacent zooms.

References:

- [Leica Classic - Vario-Elmar-R 4/70-210mm](https://classic.leica-camera.com/en/Leica-Systems/R-System/Lenses/Zoom-Lenses/Vario-Elmar-R-4-70-210mm/)
- [Leica Classic - Leitz Vario-Elmar-R 4.0/70-210mm](https://classic.leica-camera.com/en/Leitz-Vario-Elmar-R-4.0-70-210mm/11246SH-3581789)

### Source C: adjacent Leica R zoom boundaries

Separate neighboring zoom families are independently documented:

- `70mm–180mm f/2.8 Vario-APO-Elmarit-R`
- `80mm–200mm f/4 Vario-Elmar-R`
- older `80mm–200mm f/4.5 Vario-Elmar-R`
- `105mm–280mm f/4.2 Vario-Elmar-R`

References:

- [Leica Wiki - 70mm-180mm f/2.8 Vario-APO-Elmarit-R](https://wiki.l-camera-forum.com/leica-wiki.en/index.php?title=70mm%E2%80%93180mm_f%2F2.8_Vario-APO-Elmarit-R)
- [Leica Wiki - 80mm-200mm f/4 Vario-Elmar-R](https://wiki.l-camera-forum.com/leica-wiki.en/index.php/80mm%E2%80%93200mm_f/4_Vario-Elmar-R)
- [Leica Wiki - 80mm-200mm f/4.5 Vario-Elmar-R](https://wiki.l-camera-forum.com/leica-wiki.en/index.php/80mm%E2%80%93200mm_f/4.5_Vario-Elmar-R)
- [Leica Classic - Vario-Elmar-R 4,2/105-280mm](https://classic.leica-camera.com/en/Leica-Systems/R-System/Lenses/Zoom-Lenses/Vario-Elmar-R-4-2-105-280mm/)

## Taxonomy Implication from Literature

Literature clearly supports:

- one real broad family:
  - `Leica Vario-Elmar-R 70-210mm f/4`

Literature also supports meaningful metadata around:

- `ROM`
- `cam version`
- `E60`
- built-in hood
- anniversary-edition / engraving markers

However, literature does not justify round-1 seed activation by itself. The deciding question is whether local seller titles stabilize this family as a usable row. In the current raw pool, they do not yet do so strongly enough.

## Boundary Check

This family must remain separate from:

- `Leica Vario-APO-Elmarit-R 70-180mm f/2.8`
- `Leica Vario-Elmar-R 80-200mm f/4`
- older `Leica Vario-Elmar-R 80-200mm f/4.5`
- `Leica Vario-Elmar-R 105-280mm f/4.2`
- `Leica APO-Telyt-R 180`
- `Leica APO-Elmarit-R 180`
- non-APO `Leica Elmarit-R 180`
- `Leica APO-Summicron-R 180`
- `Leica APO-Telyt-R 280`
- `SL / L-mount` zooms
- third-party `70-200mm / 70-210mm / 80-200mm` zooms
- hood-only / cap / case / accessory-only listings

## Local Listing Evidence

Analysis base:

- `data/raw/raw_*.json`
- `data/derived/results_resolved_v2.json`

### Broad retrieval behavior

Broad range retrieval is risky.

Within the wider `70-200 / 70-210 / 80-200` raw field, distinct non-family lines appear immediately:

- `Leica R 70-180mm f2.8 Vario-Apo-Elmarit Black`
- `[위탁] R 70-180/2.8 Vario Apo Elmarit (Black)`
- `LEICA 80-200mm F4 VARIO-ELMAR-R sn.3699`
- `[중고] R 105-280/4.2 ROM (Black)`
- `Lumix S Pro 70-200mm f4 OIS Black`
- `Panasonic 70-200mm F4 OIS Pro S`

Interpretation:

- bare `70-210`
- broad `vario elmar`
- broad `leica r 70-210`
- broad `70 210 elmar`

are not safe shaping aliases in round 1 because the wider retrieval field already mixes adjacent Leica R zooms and non-Leica `70-200` zooms.

### Clean local R-side pool

After restricting to explicit `70-210mm`, explicit R-side `Vario-Elmar-R` wording, and excluding `70-180`, `80-200`, older `80-200mm f/4.5`, `105-280`, the R-side `180mm / 280mm` primes, SL/L, third-party, and accessory contamination, the usable pool becomes:

- clean local pool: `2`
- unique titles: `2`
- KRW-priced count: `1`
- KRW median: `550,000 KRW`

Representative clean titles:

- `[위탁] R 70-210/4 Vario-Elmar`
- `LEICA 70-210mm F4 VARIO-ELMAR-R sn.3582`

Observed price points:

- `550,000 KRW`
- `문의요망`

Interpretation:

- the explicit titles are family-correct
- but the local pool still collapses to two narrow title shapes
- only one listing is KRW-priced
- current evidence is still too thin for round-1 seed activation

## Marker / Metadata Observation

Within the current clean `70-210 Vario-Elmar-R` pool, seller wording does not reliably stabilize row-level internal splits for:

- `ROM`
- `cam`
- `E60`
- built-in hood
- hood / case / boxed
- engraving / anniversary marker

Observed local marker distribution:

- `ROM`: `0`
- `cam`: `0`
- `E60 wording`: `0`
- built-in hood wording: `0`
- box / case wording: `0`
- special engraving wording: `0`

These should remain overlay or deferred metadata in round 1.

## Smoke Query Review

The following explicit queries are literature-correct and point toward the same intended family:

- `vario-elmar-r 70-210`
- `vario elmar r 70-210`
- `70-210 vario-elmar-r`
- `70-210mm f4 vario-elmar-r`
- `70-210mm f/4 vario-elmar-r`
- `r 70-210/4 vario elmar`
- `leica r 70-210mm f4`
- `leica r 70-210mm f/4`

But round-1 local support is still only two clean title shapes, with one priced row, so these are not enough to justify seed activation yet.

The following broader shorthands are not safe:

- bare `70-210`
- broad `vario elmar`
- broad `leica r 70-210`
- broad `70 210 elmar`

because they can drift into:

- `Leica Vario-APO-Elmarit-R 70-180mm f/2.8`
- `Leica Vario-Elmar-R 80-200mm f/4`
- older `Leica Vario-Elmar-R 80-200mm f/4.5`
- `Leica Vario-Elmar-R 105-280mm f/4.2`
- `Lumix / Panasonic 70-200mm`
- future third-party `70-200 / 70-210 / 80-200` zooms

## Candidate Assessment

### immediate core candidate

None.

The family is literature-real and local titles are correct, but round-1 local support is still too narrow.

### strongest deferred candidate

- `Leica Vario-Elmar-R 70-210mm f/4`

### hold candidate

None.

The current evidence does not support a separate explicit-wording-only hold row. It supports a deferred family review instead.

## Overlay / Deferred Elements

Do not create separate rows for:

- `ROM`
- `cam version`
- `E60`
- `filter thread`
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
- anniversary engraving / signature marker

## Out-of-Family / Hard Boundary

Must remain out of family:

- `Leica Vario-APO-Elmarit-R 70-180mm f/2.8`
- `Leica Vario-Elmar-R 80-200mm f/4`
- older `Leica Vario-Elmar-R 80-200mm f/4.5`
- `Leica Vario-Elmar-R 105-280mm f/4.2`
- `Leica APO-Telyt-R 180`
- `Leica APO-Elmarit-R 180`
- non-APO `Leica Elmarit-R 180`
- `Leica APO-Summicron-R 180`
- `Leica APO-Telyt-R 280`
- `SL / L-mount` zooms
- third-party `70-200mm / 70-210mm / 80-200mm` zooms
- accessory-only listings

## Round-1 Verdict

- immediate core candidate:
  - `0`
- recommended first-pass core:
  - none
- strongest deferred candidate:
  - `Leica Vario-Elmar-R 70-210mm f/4`
- explicit hold candidate:
  - none

Final round-1 decision:

- `seed 보류`

Why:

1. the family is literature-real
2. the local clean pool is only `2`
3. the usable pool collapses to two narrow title shapes
4. only one listing has KRW price support
5. broad `70-210` / `vario elmar` retrieval already drifts into adjacent Leica R zooms and non-Leica `70-200` zooms

## Next-Round Recommendation

Do not add seed yet.

Revisit when:

- multiple additional clean local titles appear for the `f/4` family
- KRW-priced support is no longer single-listing
- local seller wording shows that `70-210mm f/4` can be stably separated from:
  - `70-180mm f/2.8`
  - `80-200mm f/4`
  - older `80-200mm f/4.5`
  - `105-280mm f/4.2`
  - `70-200mm` SL/L or third-party zoom contamination
