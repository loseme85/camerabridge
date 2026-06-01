# Vario-Elmarit-R 28-90 Taxonomy Audit - Round 1

Date: 2026-05-20

Scope: audit-only review for the Leica `Vario-Elmarit-R 28-90` family. This round does not add seed rows, does not modify `entities/*.json`, does not modify `canonical_entities_index.json`, and does not change classifier/query/search behavior, ranking, or UI.

## Executive Summary

`Vario-Elmarit-R 28-90` is literature-real, and unlike many adjacent R zoom families, the local title evidence already converges on one stable intended family when the query keeps explicit `R`, `28-90`, and `Vario-Elmarit` anchors.

Round-1 conclusion:

- immediate recommended `core` candidate count: `1`
- recommended first-pass core:
  - `Leica Vario-Elmarit-R 28-90mm f/2.8-4.5 ASPH`
- explicit `hold` candidate:
  - none
- literature clearly supports a real Leica R `28-90mm f/2.8-4.5 ASPH Vario-Elmarit-R` zoom family
- local title support is narrow but stable:
  - clean local rows resolve to the same `28-90mm f/2.8-4.5` R-side zoom family
  - priced observations cluster in a coherent KRW band
- local support is strong enough for a future narrow seed row
- broad shorthand remains unsafe:
  - `28-90`
  - `vario elmarit 28-90`
  - `leica r 28-90`
  - `28 90 elmarit`
  can drift into `SL 24-90`, `SL 90-280`, `LTM 28-90`, and third-party zooms

The safest round-1 answer is:

1. recognize `Leica Vario-Elmarit-R 28-90mm f/2.8-4.5 ASPH` as an immediate seedable candidate
2. do not open any internal version row
3. keep `ROM`, `cam`, `ASPH`, filter-thread markers, hood/case bundles, and similar details as overlay/deferred metadata
4. keep R primes, SL `24-90`, other R zooms, and third-party standard zooms as hard boundaries

## Literature / Reference Base

### Source A: Leica Classic - `Vario-Elmarit-R 2,8-4,5/28-90mm ASPH.`

Leica Classic lists the family under:

- `Leica Vario-Elmarit-R 1:2,8-4,5/28-90 mm. ASPH.`
- `Leica Vario-Elmarit-R 28-90mm f/2.8-4.5 ASPH. ROM 11365`

The page shows multiple used-store entries across different stores and conditions, confirming that this is a real Leica R zoom family rather than a one-off market wording.

Reference:

- [Leica Classic - Vario-Elmarit-R 2,8-4,5/28-90mm ASPH.](https://classic.leica-camera.com/en/Leica-Systems/R-System/Lenses/Zoom-Lenses/Vario-Elmarit-R-2-8-4-5-28-90mm-ASPH./)

### Source B: Leica R-lenses user manual / product literature

Leica product literature includes:

- `LEICA VARIO-ELMARIT-R 28-90 MM F/2.8-4.5 ASPH`

which further supports the official family wording and the `ASPH` marker as part of the literature identity.

References:

- [Leica R-Lenses User Manual](https://usermanual.wiki/Leica/LeicaRLensesUsersManual435601.1485557889.pdf)
- [LEICA VARIO-ELMARIT-R 28-90 mm f/2,8-4,5 ASPH. PDF](https://summilux.net/r_system/objectifs/VarioElmarit28-90.pdf)

### Source C: adjacent Leica R / SL zoom boundaries

Separate neighboring zoom families are independently documented:

- `70mm-180mm f/2.8 Vario-APO-Elmarit-R`
- `35mm-70mm f/4 Vario-Elmar-R`
- `80mm-200mm f/4 Vario-Elmar-R`
- `70mm-210mm f/4 Vario-Elmar-R`
- `105mm-280mm f/4.2 Vario-Elmar-R`
- `24-90mm f/2.8-4 Vario-Elmarit-SL`

References:

- [Leica Wiki - 70mm-180mm f/2.8 Vario-APO-Elmarit-R](https://wiki.l-camera-forum.com/leica-wiki.en/index.php?title=70mm%E2%80%93180mm_f%2F2.8_Vario-APO-Elmarit-R)
- [Leica Wiki - 35mm-70mm f/4 Vario-Elmar-R](https://wiki.l-camera-forum.com/leica-wiki.en/index.php?title=35mm%E2%80%9370mm_f%2F4_Vario-Elmar-R)
- [Leica Wiki - 70mm-210mm f/4 Vario-Elmar-R](https://wiki.l-camera-forum.com/leica-wiki.en/index.php/70mm%E2%80%93210mm_f/4_Vario-Elmar-R)
- [Leica Wiki - 80mm-200mm f/4 Vario-Elmar-R](https://wiki.l-camera-forum.com/leica-wiki.en/index.php/80mm%E2%80%93200mm_f/4_Vario-Elmar-R)
- [Leica Classic - Vario-Elmar-R 4,2/105-280mm](https://classic.leica-camera.com/en/Leica-Systems/R-System/Lenses/Zoom-Lenses/Vario-Elmar-R-4-2-105-280mm/)
- [Leica Camera - Vario-Elmarit-SL 24-90 f/2.8-4 ASPH.](https://leica-camera.com/en-US/photography/lenses/sl/vario-elmarit-sl-24-90mm-f2-8-4-asph-black)

## Taxonomy Implication from Literature

Literature clearly supports:

- one real broad family:
  - `Leica Vario-Elmarit-R 28-90mm f/2.8-4.5 ASPH`

Literature also supports real metadata structure around:

- `ROM`
- `cam version`
- `ASPH`
- filter-thread marker
- hood / cap / case / packaging ecosystem

However, literature does not justify internal split rows in round 1. The local seller pool does not surface stable row-level variants for `ROM` vs non-`ROM`, or for `ASPH` vs omitted-`ASPH` wording, strongly enough to warrant separate rows.

## Boundary Check

This family must remain separate from:

- `Leica Elmarit-R 28mm f/2.8`
- `Leica Elmarit-R 35mm`
- `Leica Summicron-R 35mm f/2`
- `Leica Summilux-R 35mm f/1.4`
- `Leica Summicron-R 50mm f/2`
- `Leica Summilux-R 50mm f/1.4`
- `Leica Elmarit-R 90mm f/2.8`
- `Leica Summicron-R 90mm f/2`
- `Leica APO-Summicron-R 90mm f/2`
- `Leica Vario-Elmar-R 35-70`
- `Leica Vario-Elmar-R 80-200`
- `Leica Vario-Elmar-R 70-210`
- `Leica Vario-Elmar-R 105-280`
- `Leica Vario-APO-Elmarit-R 70-180`
- `Leica Vario-Elmarit-SL 24-90`
- `SL / L-mount` zooms
- third-party `24-70mm / 28-70mm / 28-90mm` zooms
- hood-only / cap / case / accessory-only listings

## Local Listing Evidence

Analysis base:

- `data/raw/raw_*.json`
- `data/derived/results_resolved_v2.json`
- `data/normalized/normalized_20260423_142946.json`
- `data/sold_items.json`

### Broad retrieval behavior

Broad shorthand is risky.

Within the wider `24-90 / 28-90 / vario elmarit / asph` raw field, distinct non-family lines appear immediately:

- `[중고] R 28-90 / 2.8-4.5 Vario-Elmarit ROM (Black)`
- `LEICA 28-90mm F2.8-4.5 ASPH VARIO-ELMARIT-R sn.3974`
- `Leica 28-90mm F2.8-4.5 ROM`
- `Leica SL 24-90mm f2.8-4 Vario-Elmarit Black`
- `[중고] SL Vario Elmarit 24-90/2.8-4 ASPH.`
- `[중고] SL APO Vario Elmarit 90-280 f/2.8-4`
- `LEICA 28-90 LTM`
- `[위탁] Leica LTM 28-90`
- `[중고] 보이그랜더 LTM 28-90`
- `Sigma 28-70mm F2.8 DG DN Contemporary - L Mount`

Interpretation:

- bare `28-90`
- broad `vario elmarit 28-90`
- broad `leica r 28-90`
- broad `28 90 elmarit`

are not safe shaping aliases in round 1 because the wider retrieval field already mixes:

- R `28-90` zoom
- SL `24-90`
- SL `90-280`
- `LTM 28-90`
- third-party standard zooms

### Clean local R-side pool

After restricting to explicit `28-90mm`, explicit R-side wording, and excluding `24-90` SL, `90-280` SL, LTM, accessory-only, and third-party contamination, the usable pool becomes:

- clean local pool: `6`
- unique titles: `6`
- KRW-priced count: `3`
- KRW median: `3,800,000 KRW`

Representative clean titles:

- `[중고] R 28-90 / 2.8-4.5 Vario-Elmarit ROM (Black)`
- `[중고] R 28-90 / 2.8-4.5 Rom`
- `LEICA 28-90mm F2.8-4.5 VARIO-ELMARIT-R sn.3975`
- `LEICA 28-90mm F2.8-4.5 ASPH VARIO-ELMARIT-R sn.3974`
- `LEICA 28-90mm F2.8-4.5 VARIO-ELMARIT-R sn.3973`
- `Leica 28-90mm F2.8-4.5 ROM`

Observed price points:

- `3,000,000 KRW`
- `3,800,000 KRW`
- `5,700,000 KRW`
- `문의요망`
- `문의요망`
- `£1,949.00`

Interpretation:

- local wording is family-correct
- multiple independent title shapes converge on the same `R 28-90 / 2.8-4.5` family
- priced observations exist and cluster in a coherent band
- this is materially stronger than the nearby deferred R zoom families

### Explicit wording stability

The local pool does not rely on one fragile token only. It repeats across:

- `R 28-90 / 2.8-4.5 Vario-Elmarit ROM`
- `R 28-90 / 2.8-4.5 Rom`
- `28-90mm F2.8-4.5 VARIO-ELMARIT-R`
- `28-90mm F2.8-4.5 ASPH VARIO-ELMARIT-R`
- `28-90mm F2.8-4.5 ROM`

Interpretation:

- family recognition is stable at the main-row level
- `ASPH` omission in some seller titles does not behave like a different family
- `ROM` appears frequently, but not as a separately priced or separately title-stable internal row

## Marker / Metadata Observation

Within the current clean `28-90 Vario-Elmarit-R` pool, seller wording does not reliably stabilize row-level internal splits for:

- `ROM`
- `cam`
- `ASPH`
- exact filter-thread marker
- hood / case / boxed

Observed local marker distribution:

- `ROM`: `3`
- `ASPH`: `1`
- `cam`: `0`
- exact filter-thread marker: `0`
- hood / case / box wording: `0`

Interpretation:

- `ROM` is common but still not enough to justify a separate row
- `ASPH` is literature-real but often omitted in seller shorthand
- these should remain overlay or deferred metadata in round 1

## Smoke Query Review

The following explicit queries are literature-correct and point toward the same intended family:

- `vario-elmarit-r 28-90`
- `vario elmarit r 28-90`
- `28-90 vario-elmarit-r`
- `28-90mm f2.8-4.5 vario-elmarit-r`
- `28-90mm f/2.8-4.5 vario-elmarit-r`
- `r 28-90/2.8-4.5 vario elmarit`
- `leica r 28-90mm f2.8-4.5`
- `leica r 28-90mm f/2.8-4.5`
- `28-90mm asph vario-elmarit-r`

These queries resolve to a narrow, coherent family cluster.

The following broader shorthands are not safe:

- bare `28-90`
- broad `vario elmarit 28-90`
- broad `leica r 28-90`
- broad `28 90 elmarit`
- `28-90 asph r`

because they can drift into:

- `Leica Vario-Elmarit-SL 24-90`
- `Leica APO-Vario-Elmarit-SL 90-280`
- `Leica 28-90 LTM`
- `Voigtlander LTM 28-90`
- `Sigma 28-70`
- future third-party `24-70 / 28-70 / 28-90` zooms

## Candidate Assessment

### immediate core candidate

- `Leica Vario-Elmarit-R 28-90mm f/2.8-4.5 ASPH`

Reason:

- literature-real
- explicit local title support exists
- local title shapes are stable
- priced observations exist
- boundary against R primes and neighboring zoom families is strong when the query keeps explicit `28-90` plus `R` plus `Vario-Elmarit`

### hold candidate

None.

The local evidence supports one narrow main row more naturally than any explicit-wording-only hold row.

## Overlay / Deferred Elements

Do not create separate rows for:

- `ROM`
- `cam version`
- `ASPH`
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

- `Leica Elmarit-R 28mm f/2.8`
- `Leica Elmarit-R 35mm`
- `Leica Summicron-R 35mm f/2`
- `Leica Summilux-R 35mm f/1.4`
- `Leica Summicron-R 50mm f/2`
- `Leica Summilux-R 50mm f/1.4`
- `Leica Elmarit-R 90mm f/2.8`
- `Leica Summicron-R 90mm f/2`
- `Leica APO-Summicron-R 90mm f/2`
- `Leica Vario-Elmar-R 35-70`
- `Leica Vario-Elmar-R 80-200`
- `Leica Vario-Elmar-R 70-210`
- `Leica Vario-Elmar-R 105-280`
- `Leica Vario-APO-Elmarit-R 70-180`
- `Leica Vario-Elmarit-SL 24-90`
- `APO-Vario-Elmarit-SL 90-280`
- `SL / L-mount` zooms
- third-party `24-70mm / 28-70mm / 28-90mm` zooms
- accessory-only listings

## Round-1 Verdict

- immediate core candidate:
  - `1`
- recommended first-pass core:
  - `Leica Vario-Elmarit-R 28-90mm f/2.8-4.5 ASPH`
- strongest deferred candidate:
  - not applicable because the main row is already seedable in round 1
- explicit hold candidate:
  - none

Final round-1 decision:

- `next seed round 가능`

Why:

1. the family is literature-real
2. the clean local pool is `6`
3. unique local title shapes are `6`
4. KRW-priced support exists with median `3,800,000 KRW`
5. explicit range-plus-family wording separates this zoom reasonably well from neighboring R primes and zooms
6. only the broad shorthand layer remains unsafe

## Next-Round Recommendation

If the next round opens this family, do it narrowly:

- add only:
  - `Leica Vario-Elmarit-R 28-90mm f/2.8-4.5 ASPH`

Do not add:

- separate `ROM` row
- separate `ASPH` vs non-`ASPH` row
- broad `28-90` generic row
- broad `vario elmarit` generic row

Revisit internal splits only if future local data shows:

- repeated seller use of `ROM` as a distinct market row
- repeated full `ASPH` vs omitted-`ASPH` title separation with stable price divergence
- stable local distinction from `SL 24-90`, `SL 90-280`, and non-Leica standard zoom contamination
