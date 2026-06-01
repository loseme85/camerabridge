# Vario-Elmarit-R 35-70 Taxonomy Audit - Round 1

Date: 2026-05-20

Scope: audit-only review for the Leica `Vario-Elmarit-R 35-70` family. This round does not add seed rows, does not modify `entities/*.json`, does not modify `canonical_entities_index.json`, and does not change classifier/query/search behavior, ranking, or UI.

## Executive Summary

`Vario-Elmarit-R 35-70` is literature-real, but round-1 local support is currently absent.

Round-1 conclusion:

- immediate recommended `core` candidate count: `0`
- recommended first-pass core:
  - none
- strongest deferred candidate:
  - `Leica Vario-Elmarit-R 35-70mm f/2.8 ASPH`
- explicit `hold` candidate:
  - none
- literature clearly supports a real Leica R `35-70mm f/2.8 ASPH Vario-Elmarit-R` zoom family
- literature also supports two separate adjacent Leica R `Vario-Elmar-R 35-70` families:
  - `Leica Vario-Elmar-R 35-70mm f/3.5`
  - `Leica Vario-Elmar-R 35-70mm f/4`
- these must not be merged into `Vario-Elmarit-R 35-70mm f/2.8 ASPH`
- current local support is too thin for seed activation:
  - no clean local rows stabilize the family
  - no KRW-priced local support exists
- broad `35-70` / `vario elmarit` / `leica r 35-70` / `35 70 elmarit` / `35-70 asph` retrieval is unsafe and can drift into adjacent Leica zoom families, SL/L zooms, and third-party standard zooms

The safest round-1 answer is:

1. keep `Leica Vario-Elmarit-R 35-70mm f/2.8 ASPH` closed for now
2. do not merge it with `Vario-Elmar-R 35-70mm f/3.5`
3. do not merge it with `Vario-Elmar-R 35-70mm f/4`
4. do not open any `core` or `hold` row yet

## Literature / Reference Base

### Source A: Leica Classic - `Vario-Elmarit-R 2,8/35-70mm ASPH.`

Leica Classic documents:

- `Leica Vario-Elmarit-R 35-70mm f/2.8 ASPH`
- order no.:
  - `11275`
- Leica R zoom family status as a distinct `Vario-Elmarit-R` line
- constant `f/2.8` aperture
- built-in macro function
- rare-production positioning

References:

- [Leica Classic - Vario-Elmarit-R 2,8/35-70mm ASPH.](https://classic.leica-camera.com/en/Leica-Systems/R-System/Lenses/Zoom-Lenses/Vario-Elmarit-R-2-8-35-70mm-ASPH./11275/)
- [Leica Classic - Leica Vario-Elmarit-R 35-70mm f/2.8 ASPH 11275](https://classic.leica-camera.com/en/Leica-Vario-Elmarit-R-35-70mm-f-2.8-ASPH-11275/11275SH-3839532)

### Source B: Leica Wiki - `35mm-70mm Vario-Elmarit-R ASPH`

Leica Wiki documents:

- Leica order no.:
  - `11 275`
- production era:
  - `1998-2002`
- aperture:
  - `f/2.8 > f/22`
- macro setting:
  - documented
- filter type:
  - `E77`
- inscription example:
  - `VARIO-ELMARIT-R 1:2.8/35-70 ASPH.`

Reference:

- [Leica Wiki - 35mm-70mm Vario-Elmarit-R ASPH](https://wiki.l-camera-forum.com/leica-wiki.en/index.php?title=35mm%E2%80%9370mm_Vario-Elmarit-R_ASPH)

### Source C: adjacent Leica R `35-70` families that must not be merged

Leica literature independently documents:

- `Leica Vario-Elmar-R 35-70mm f/3.5`
- `Leica Vario-Elmar-R 35-70mm f/4`

These are separate `Vario-Elmar-R` families and must not be merged into:

- `Leica Vario-Elmarit-R 35-70mm f/2.8 ASPH`

References:

- [Leica Wiki - 35mm-70mm f/3.5 Vario-Elmar-R](https://wiki.l-camera-forum.com/leica-wiki.en/index.php/35mm%E2%80%9370mm_f/3.5_Vario-Elmar-R)
- [Leica Wiki - 35mm-70mm f/4 Vario-Elmar-R](https://wiki.l-camera-forum.com/leica-wiki.en/index.php?title=35mm%E2%80%9370mm_f%2F4_Vario-Elmar-R)

### Source D: adjacent Leica R / SL zoom boundaries

Separate neighboring zoom families are independently documented:

- `Vario-Elmarit-R 28-90mm f/2.8-4.5 ASPH`
- `Vario-Elmar-R 70-210mm f/4`
- `Vario-Elmar-R 80-200mm f/4`
- `Vario-Elmar-R 105-280mm f/4.2`
- `Vario-APO-Elmarit-R 70-180mm f/2.8`
- `Vario-Elmarit-SL 24-90mm f/2.8-4`

References:

- [Leica Classic - Vario-Elmarit-R 2,8-4,5/28-90mm ASPH.](https://classic.leica-camera.com/en/Leica-Systems/R-System/Lenses/Zoom-Lenses/Vario-Elmarit-R-2-8-4-5-28-90mm-ASPH./)
- [Leica Wiki - 70mm-210mm f/4 Vario-Elmar-R](https://wiki.l-camera-forum.com/leica-wiki.en/index.php/70mm%E2%80%93210mm_f/4_Vario-Elmar-R)
- [Leica Wiki - 80mm-200mm f/4 Vario-Elmar-R](https://wiki.l-camera-forum.com/leica-wiki.en/index.php/80mm%E2%80%93200mm_f/4_Vario-Elmar-R)
- [Leica Classic - Vario-Elmar-R 4,2/105-280mm](https://classic.leica-camera.com/en/Leica-Systems/R-System/Lenses/Zoom-Lenses/Vario-Elmar-R-4-2-105-280mm/)
- [Leica Wiki - 70mm-180mm f/2.8 Vario-APO-Elmarit-R](https://wiki.l-camera-forum.com/leica-wiki.en/index.php?title=70mm%E2%80%93180mm_f%2F2.8_Vario-APO-Elmarit-R)
- [Leica Camera - Vario-Elmarit-SL 24-90 f/2.8-4 ASPH.](https://leica-camera.com/en-US/photography/lenses/sl/vario-elmarit-sl-24-90mm-f2-8-4-asph-black)

## Taxonomy Implication from Literature

Literature clearly supports:

- one real family:
  - `Leica Vario-Elmarit-R 35-70mm f/2.8 ASPH`

Literature also supports real metadata around:

- `ROM`
- `cam version`
- `ASPH`
- `macro function`
- `E77`
- filter-thread marker
- hood / cap / case / packaging ecosystem

But literature alone does not justify round-1 seed activation. The deciding question is whether local seller titles stabilize the family into a usable local pool. In the current reviewed local pool, they do not.

## Boundary Check

This family must remain separate from:

- `Leica Vario-Elmar-R 35-70mm f/3.5`
- `Leica Vario-Elmar-R 35-70mm f/4`
- `Leica Vario-Elmarit-R 28-90mm f/2.8-4.5 ASPH`
- `Leica Elmarit-R 28mm f/2.8`
- `Leica Elmarit-R 35mm`
- `Leica Summicron-R 35mm f/2`
- `Leica Summilux-R 35mm f/1.4`
- `Leica Summicron-R 50mm f/2`
- `Leica Summilux-R 50mm f/1.4`
- `Leica Elmarit-R 90mm f/2.8`
- `Leica Summicron-R 90mm f/2`
- `Leica APO-Summicron-R 90mm f/2`
- `Leica Vario-Elmar-R 70-210mm f/4`
- `Leica Vario-Elmar-R 80-200mm f/4`
- `Leica Vario-Elmar-R 105-280mm f/4.2`
- `Leica Vario-APO-Elmarit-R 70-180mm f/2.8`
- `Leica Vario-Elmarit-SL 24-90mm f/2.8-4`
- `SL / L-mount` zooms
- third-party `24-70mm / 28-70mm / 35-70mm` zooms
- accessory-only listings

## Local Listing Evidence

Analysis base:

- `data/raw/raw_*.json`
- `data/derived/results_resolved_v2.json`

### Broad retrieval behavior

Broad shorthand is risky.

Within the wider `35-70 / vario elmarit / asph` field, nearby or contaminating patterns are already visible or strongly expected:

- `Vario-Elmar-R 35-70mm f/3.5`
- `Vario-Elmar-R 35-70mm f/4`
- `Vario-Elmarit-R 28-90mm f/2.8-4.5 ASPH`
- `Vario-Elmarit-SL 24-90mm f/2.8-4`
- third-party `24-70 / 28-70 / 35-70` zooms
- accessory-only rows

Interpretation:

- bare `35-70`
- broad `vario elmarit`
- broad `leica r 35-70`
- broad `35 70 elmarit`
- `35-70 asph`

are not safe shaping aliases in round 1 because the wider retrieval field can drift into:

- `Vario-Elmar-R 35-70` aperture families
- adjacent `28-90` Leica R zoom rows
- `SL / L` standard zooms
- third-party standard zooms
- accessory-only listings

### Clean local R-side pool

After restricting to explicit `35-70mm`, explicit `Vario-Elmarit-R`, explicit `f/2.8` or `ASPH`, and excluding `Vario-Elmar-R` `f/3.5` / `f/4`, `28-90`, R primes, SL/L, third-party, and accessory contamination, the usable pool becomes:

- clean local pool: `0`
- unique titles: `0`
- KRW-priced count: `0`
- KRW median: none

Representative clean titles:

- none

Interpretation:

- literature confirms the family is real
- but no clean local row currently stabilizes the family
- the current local pool is too thin for round-1 seed activation

### Explicit wording stability

No clean local row in the current reviewed pool stabilizes:

- `Leica Vario-Elmarit-R 35-70mm f/2.8 ASPH`

Interpretation:

- the family is literature-real
- but local seller wording is currently absent rather than merely sparse
- this is weaker than the already-deferred `Vario-Elmar-R 35-70` `f/3.5` and `f/4` rows

## Marker / Metadata Observation

Within the current clean `35-70 Vario-Elmarit-R` pool, seller wording does not reliably stabilize row-level internal splits for:

- `ROM`
- `cam`
- `ASPH`
- `macro`
- exact filter-thread wording
- hood / case / boxed

Observed local marker distribution:

- `ROM`: `0`
- `cam`: `0`
- `ASPH`: `0`
- explicit `macro` wording: `0`
- exact filter-thread wording: `0`
- hood / case / box wording: `0`

Interpretation:

- `ROM` is literature-real but absent locally in a clean family-shaped way
- `ASPH` is literature-real and part of the canonical family wording
- `macro` is literature-real but should remain metadata rather than a separate row
- these remain overlay or deferred metadata rather than row-level splits

## Smoke Query Review

The following explicit queries are literature-correct and point toward the intended family:

- `vario-elmarit-r 35-70`
- `vario elmarit r 35-70`
- `35-70 vario-elmarit-r`
- `35-70mm f2.8 vario-elmarit-r`
- `35-70mm f/2.8 vario-elmarit-r`
- `35-70mm f2.8 asph vario-elmarit-r`
- `35-70mm f/2.8 asph vario-elmarit-r`
- `r 35-70/2.8 vario elmarit`
- `r 35-70/2.8 asph vario elmarit`
- `leica r 35-70mm f2.8 asph`
- `leica r 35-70mm f/2.8 asph`
- `vario elmarit 35-70 asph`

The following broader shorthands are not safe:

- bare `35-70`
- broad `vario elmarit`
- broad `leica r 35-70`
- broad `35 70 elmarit`
- `35-70 asph`

because they can drift into:

- `Leica Vario-Elmar-R 35-70mm f/3.5`
- `Leica Vario-Elmar-R 35-70mm f/4`
- `Leica Vario-Elmarit-R 28-90mm f/2.8-4.5 ASPH`
- `Leica Vario-Elmarit-SL 24-90mm f/2.8-4`
- `SL / L-mount` zooms
- third-party `24-70mm / 28-70mm / 35-70mm` zooms
- accessory-only listings

## Candidate Assessment

### immediate core candidate

None.

Current local support is absent.

### strongest deferred candidate

- `Leica Vario-Elmarit-R 35-70mm f/2.8 ASPH`

### explicit hold candidate

None.

## Overlay / Deferred Metadata

Keep as overlay or deferred metadata only:

- `ROM`
- `cam version`
- `ASPH`
- `macro mode`
- `E77`
- filter-thread marker
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

- `Leica Vario-Elmar-R 35-70mm f/3.5`
- `Leica Vario-Elmar-R 35-70mm f/4`
- `Leica Vario-Elmarit-R 28-90mm f/2.8-4.5 ASPH`
- R prime `28mm / 35mm / 50mm / 90mm` families
- `Leica Vario-Elmar-R 70-210mm f/4`
- `Leica Vario-Elmar-R 80-200mm f/4`
- `Leica Vario-Elmar-R 105-280mm f/4.2`
- `Leica Vario-APO-Elmarit-R 70-180mm f/2.8`
- `Leica Vario-Elmarit-SL 24-90mm f/2.8-4`
- `SL / L-mount` zooms
- third-party `24-70mm / 28-70mm / 35-70mm` zooms
- accessory-only listings

## Round-1 Verdict

- immediate core candidate:
  - `0`
- recommended first-pass core:
  - none
- strongest deferred candidate:
  - `Leica Vario-Elmarit-R 35-70mm f/2.8 ASPH`
- explicit hold candidate:
  - none

Final round-1 decision:

- `seed 보류`

Why:

1. literature clearly supports `Leica Vario-Elmarit-R 35-70mm f/2.8 ASPH` as a real Leica R family
2. the family must remain separate from `Vario-Elmar-R 35-70mm f/3.5` and `f/4`
3. but the current reviewed local pool has no clean stabilizing row at all
4. there is no KRW-priced support and no usable median
5. broad `35-70` / `vario elmarit` retrieval remains too contamination-prone

## Next-Round Recommendation

Do not add seed yet.

Revisit when:

- explicit clean local titles for `Leica Vario-Elmarit-R 35-70mm f/2.8 ASPH` appear
- KRW-priced support appears
- local wording shows the family can be held apart from:
  - `Vario-Elmar-R 35-70mm f/3.5`
  - `Vario-Elmar-R 35-70mm f/4`
  - `Vario-Elmarit-R 28-90`
  - `Vario-Elmarit-SL 24-90`
  - third-party standard zoom contamination
