# Vario-Elmar-R 28-70 Taxonomy Audit - Round 1

Date: 2026-05-20

Scope: audit-only review for the Leica `Vario-Elmar-R 28-70` family. This round does not add seed rows, does not modify `entities/*.json`, does not modify `canonical_entities_index.json`, and does not change classifier/query/search behavior, ranking, or UI.

## Executive Summary

`Vario-Elmar-R 28-70` is literature-real, but round-1 local support is too thin for seed activation.

Round-1 conclusion:

- immediate recommended `core` candidate count: `0`
- recommended first-pass core:
  - none
- strongest deferred candidate:
  - `Leica Vario-Elmar-R 28-70mm f/3.5-4.5`
- explicit `hold` candidate:
  - none
- literature clearly supports one real Leica R `28-70mm f/3.5-4.5 Vario-Elmar-R` family
- no additional aperture-distinct Leica R `28-70mm` family was confirmed in primary literature for this round
- current reviewed local support is very thin:
  - one relaxed local row exists
  - but explicit `Vario-Elmar-R` seller wording does not repeat in a stable local title pool
- broad `28-70` / `vario elmar` / `leica r 28-70` / `28 70 elmar` retrieval is unsafe and can drift into adjacent Leica R zooms, SL/L zooms, and third-party standard zooms

The safest round-1 answer is:

1. keep `Leica Vario-Elmar-R 28-70mm f/3.5-4.5` closed for now
2. do not open any `core` or `hold` row
3. treat `ROM`, `cam`, `macro`, filter-thread marker, hood/case/box details as overlay or deferred metadata
4. keep `28-90`, `35-70`, R primes, SL/L zooms, and third-party standard zooms as hard boundaries

## Literature / Reference Base

### Source A: Leica Classic - `Vario-Elmar-R 3,5-4,5/28-70mm`

Leica Classic documents:

- `Vario-Elmar-R 3,5-4,5/28-70mm`
- order nos.:
  - `11265`
  - `11364`

This supports a real Leica R `28-70mm f/3.5-4.5` zoom family, with later `ROM` examples appearing under the same literature family rather than as a separate optical row.

References:

- [Leica Classic - Vario-Elmar-R 3,5-4,5/28-70mm](https://classic.leica-camera.com/en/Leica-Systems/R-System/Lenses/Zoom-Lenses/Vario-Elmar-R-3-5-4-5-28-70mm/)
- [Leica Classic - Vario Elmar R 28-70 3.5-4.5 (11364)](https://classic.leica-camera.com/en/Vario-Elmar-R-28-70-3.5-4.5-11364/11364SH-3826029)
- [Leica Classic - VARIO-ELMAR-R 1:3.5-4.5/28-70 mm](https://classic.leica-camera.com/en/VARIO-ELMAR-R-1-3.5-4.5-28-70-mm/11364SH-3530936)

### Source B: Leica Wiki - `28mm-70mm f/3.5-4.5 Vario Elmar-R`

Leica Wiki documents:

- order nos.:
  - `11265`
  - `11364-ROM`
- production era:
  - `1990-1997`
- manufacturer:
  - `Sigma`
- aperture:
  - `f/3.5 - f/22`
- closest focus:
  - `50 cm`
- accessory note:
  - hood `12509` or `12437`
- inscription examples:
  - `LEICA VARIO-ELMAR-R 1:3.5-4.5 28-70mm`
  - `LEICA VARIO-ELMAR-R 1:3.5-4.5 28-70 E60`

Leica Wiki also notes an Olympia variant, but that is a version marker or special-edition marker, not a separate canonical row.

Reference:

- [Leica Wiki - 28mm-70mm f/3.5-4.5 Vario Elmar-R](https://wiki.l-camera-forum.com/leica-wiki.en/index.php?title=28mm%E2%80%9370mm_f%2F3.5%E2%80%934.5_Vario_Elmar-R)

### Source C: adjacent Leica R / SL zoom boundaries

Separate neighboring zoom families are independently documented:

- `Vario-Elmarit-R 28-90mm f/2.8-4.5 ASPH`
- `Vario-Elmar-R 35-70mm f/3.5`
- `Vario-Elmar-R 35-70mm f/4`
- `Vario-Elmarit-R 35-70mm f/2.8 ASPH`
- `Vario-Elmarit-SL 24-90mm f/2.8-4`

References:

- [Leica Classic - Vario-Elmarit-R 2,8-4,5/28-90mm ASPH.](https://classic.leica-camera.com/en/Leica-Systems/R-System/Lenses/Zoom-Lenses/Vario-Elmarit-R-2-8-4-5-28-90mm-ASPH./)
- [Leica Wiki - 35mm-70mm f/3.5 Vario-Elmar-R](https://wiki.l-camera-forum.com/leica-wiki.en/index.php/35mm%E2%80%9370mm_f/3.5_Vario-Elmar-R)
- [Leica Wiki - 35mm-70mm f/4 Vario-Elmar-R](https://wiki.l-camera-forum.com/leica-wiki.en/index.php?title=35mm%E2%80%9370mm_f%2F4_Vario-Elmar-R)
- [Leica Classic - Vario-Elmarit-R 2,8/35-70mm ASPH.](https://classic.leica-camera.com/en/Leica-Systems/R-System/Lenses/Zoom-Lenses/Vario-Elmarit-R-2-8-35-70mm-ASPH./11275/)
- [Leica Camera - Vario-Elmarit-SL 24-90 f/2.8-4 ASPH.](https://leica-camera.com/en-US/photography/lenses/sl/vario-elmarit-sl-24-90mm-f2-8-4-asph-black)

## Taxonomy Implication from Literature

Literature clearly supports:

- one real family:
  - `Leica Vario-Elmar-R 28-70mm f/3.5-4.5`

No separate aperture-distinct Leica R `28-70mm` family was confirmed in primary literature for this round.

Literature also supports metadata structure around:

- `ROM`
- `cam version`
- `E60`
- filter-thread marker
- hood references
- Olympia or signature-style special markers

But literature alone does not justify round-1 seed activation. The deciding question is whether local seller titles stabilize this family into a usable clean pool. In the current reviewed local pool, that stabilization is still too weak.

## Boundary Check

This family must remain separate from:

- `Leica Vario-Elmarit-R 28-90mm f/2.8-4.5 ASPH`
- `Leica Vario-Elmar-R 35-70mm f/3.5`
- `Leica Vario-Elmar-R 35-70mm f/4`
- `Leica Vario-Elmarit-R 35-70mm f/2.8 ASPH`
- `Leica Elmarit-R 28mm f/2.8`
- `Leica Elmarit-R 35mm`
- `Leica Summicron-R 35mm f/2`
- `Leica Summilux-R 35mm f/1.4`
- `Leica Summicron-R 50mm f/2`
- `Leica Summilux-R 50mm f/1.4`
- `Leica Elmarit-R 90mm f/2.8`
- `Leica Vario-Elmarit-SL 24-90mm f/2.8-4`
- `SL / L-mount` zooms
- third-party `24-70mm / 28-70mm / 28-75mm / 35-70mm` zooms
- accessory-only listings

## Local Listing Evidence

Analysis base:

- `data/raw/raw_*.json`
- `data/normalized/normalized_latest.json`
- `data/sold_items.json`
- `data/derived/results_resolved_v2.json`

### Broad retrieval behavior

Broad shorthand is risky.

Within the wider `28-70` retrieval field, distinct non-family lines appear immediately:

- `[중고] SL 28-70/2.8 Vario-Elmarit`
- `[중고] Sigma 28-70/2.8 (Black)`
- `Sigma 28-70mm F2.8 DG DN Contemporary - L Mount`

Interpretation:

- bare `28-70`
- broad `vario elmar`
- broad `leica r 28-70`
- broad `28 70 elmar`

are not safe shaping aliases in round 1 because the wider retrieval field already mixes:

- Leica R `28-70`
- `SL 28-70` / `SL 24-90` adjacent zoom intent
- third-party `24-70 / 28-70 / 28-75 / 35-70`
- accessory-only rows

### Clean local R-side pool

Under a relaxed filter that accepts Leica brand plus `28-70mm f/3.5-4.5` plus R-mount metadata, the usable pool becomes:

- clean local pool: `1`
- unique titles: `1`
- KRW-priced count: `0`
- KRW median: none

Representative clean title:

- `Leica 28-70mm F3.5-4.5 ROM`

Observed price:

- `£399.00`

Interpretation:

- one likely family-correct row exists
- but it does not repeat
- it does not use stable explicit `Vario-Elmar-R` seller wording
- KRW-priced support is absent

### Explicit wording stability

In the current reviewed local pool:

- explicit `Vario-Elmar-R 28-70mm` seller wording does not repeat
- the only usable row is stabilized mainly by:
  - Leica brand
  - `28-70mm F3.5-4.5`
  - `ROM`
  - R-mount or `28-70mm R Zoom` metadata

Interpretation:

- family existence is plausible in local data
- but seller-title stability is not yet good enough for round-1 seed activation

## Marker / Metadata Observation

Within the current clean `28-70 Vario-Elmar-R` pool, seller wording does not reliably stabilize row-level internal splits for:

- `ROM`
- `cam`
- exact filter-thread wording
- `macro`
- hood / case / boxed

Observed local marker distribution:

- `ROM`: `1`
- `cam`: `0`
- exact filter-thread wording: `0`
- explicit `macro` wording: `0`
- hood / case / box wording: `0`

Interpretation:

- `ROM` is present, but not enough to justify a separate row
- `ROM` should remain overlay or deferred metadata in round 1
- no other marker is locally stable enough to justify a split

## Smoke Query Review

The following explicit queries are literature-correct and point toward the intended family:

- `vario-elmar-r 28-70`
- `vario elmar r 28-70`
- `28-70 vario-elmar-r`
- `28-70mm f3.5-4.5 vario-elmar-r`
- `28-70mm f/3.5-4.5 vario-elmar-r`
- `r 28-70/3.5-4.5 vario elmar`
- `leica r 28-70mm f3.5-4.5`
- `leica r 28-70mm f/3.5-4.5`
- `leica r 28-70`
- `vario elmar 28-70`

The following broader shorthands are not safe:

- bare `28-70`
- broad `vario elmar`
- broad `leica r 28-70`
- broad `28 70 elmar`

because they can drift into:

- `Vario-Elmarit-R 28-90mm f/2.8-4.5 ASPH`
- `Vario-Elmar-R 35-70mm f/3.5`
- `Vario-Elmar-R 35-70mm f/4`
- `Vario-Elmarit-R 35-70mm f/2.8 ASPH`
- `Vario-Elmarit-SL 24-90mm f/2.8-4`
- `SL / L-mount` zooms
- third-party `24-70mm / 28-70mm / 28-75mm / 35-70mm` zooms
- accessory-only listings

## Candidate Assessment

### immediate core candidate

None.

Current local support is too thin and price evidence is not KRW-based.

### strongest deferred candidate

- `Leica Vario-Elmar-R 28-70mm f/3.5-4.5`

### explicit hold candidate

None.

## Overlay / Deferred Metadata

Keep as overlay or deferred metadata only:

- `ROM`
- `cam version`
- `E60`
- filter-thread marker
- `macro mode`
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
- Olympia or signature marker

## Out-of-Family / Hard Boundary

Must remain out of family:

- `Leica Vario-Elmarit-R 28-90mm f/2.8-4.5 ASPH`
- `Leica Vario-Elmar-R 35-70mm f/3.5`
- `Leica Vario-Elmar-R 35-70mm f/4`
- `Leica Vario-Elmarit-R 35-70mm f/2.8 ASPH`
- R prime `28mm / 35mm / 50mm / 90mm` families
- `Leica Vario-Elmarit-SL 24-90mm f/2.8-4`
- `SL / L-mount` zooms
- third-party `24-70mm / 28-70mm / 28-75mm / 35-70mm` zooms
- accessory-only listings

## Round-1 Verdict

- immediate core candidate:
  - `0`
- recommended first-pass core:
  - none
- strongest deferred candidate:
  - `Leica Vario-Elmar-R 28-70mm f/3.5-4.5`
- explicit hold candidate:
  - none

Final round-1 decision:

- `seed 보류`

Why:

1. literature clearly supports `Leica Vario-Elmar-R 28-70mm f/3.5-4.5` as a real Leica R family
2. no additional aperture-distinct Leica R `28-70mm` family was confirmed in primary literature
3. the current reviewed local pool has only one relaxed family-likely row
4. explicit `Vario-Elmar-R` seller wording does not repeat stably
5. KRW-priced support is absent
6. broad `28-70` retrieval remains too contamination-prone

## Next-Round Recommendation

Do not add seed yet.

Revisit when:

- explicit clean local titles for `Leica Vario-Elmar-R 28-70mm f/3.5-4.5` appear
- KRW-priced support appears
- local wording shows the family can be held apart from:
  - `Vario-Elmarit-R 28-90`
  - `Vario-Elmar-R 35-70`
  - `Vario-Elmarit-R 35-70`
  - `Vario-Elmarit-SL 24-90`
  - third-party standard zoom contamination
