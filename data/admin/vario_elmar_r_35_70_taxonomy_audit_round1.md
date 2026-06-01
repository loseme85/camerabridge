# Vario-Elmar-R 35-70 Taxonomy Audit - Round 1

Date: 2026-05-20

Scope: audit-only review for the Leica `Vario-Elmar-R 35-70` family. This round does not add seed rows, does not modify `entities/*.json`, does not modify `canonical_entities_index.json`, and does not change classifier/query/search behavior, ranking, or UI.

## Executive Summary

`Vario-Elmar-R 35-70` is literature-real, but round-1 local support is still not strong enough for seed activation.

Round-1 conclusion:

- immediate recommended `core` candidate count: `0`
- recommended first-pass core:
  - none
- strongest deferred candidate:
  - `Leica Vario-Elmar-R 35-70mm f/3.5`
- secondary deferred candidate:
  - `Leica Vario-Elmar-R 35-70mm f/4`
- explicit `hold` candidate:
  - none
- literature clearly supports two distinct Leica R `35-70mm` zoom families:
  - `Leica Vario-Elmar-R 35-70mm f/3.5`
  - `Leica Vario-Elmar-R 35-70mm f/4`
- literature also supports a separate:
  - `Leica Vario-Elmarit-R 35-70mm f/2.8 ASPH`
  which must not be merged into `Vario-Elmar-R`
- local title support does show a stable aperture split between `f/3.5` and `f/4`
- but price support is absent:
  - all clean local rows are KRW `문의요망`
- broad `35-70` / `vario elmar` / `leica r 35-70` retrieval already drifts into body kits, accessory bundles, and non-Leica `35-70` zooms

The safest round-1 answer is:

1. keep both `Leica Vario-Elmar-R 35-70mm f/3.5` and `Leica Vario-Elmar-R 35-70mm f/4` closed for now
2. do not merge `f/3.5` and `f/4`
3. do not open any `core` or `hold` row
4. keep `Vario-Elmarit-R 35-70mm f/2.8 ASPH` as a separate adjacent future family, not part of `Vario-Elmar-R`

## Literature / Reference Base

### Source A: Leica Wiki - `35mm-70mm f/3.5 Vario-Elmar-R`

Leica Wiki documents `35mm-70mm f/3.5 Vario-Elmar-R` with:

- order nos.:
  - `11244`
  - `11248`
- production era:
  - `1983-1996`
- manufacturer transition markers:
  - early `E60`
  - later `E67`
- aperture:
  - `f/3.5 - f/22`
- filter type:
  - `E60`
  - `E67` after later serial ranges
- inscription examples:
  - `LEITZ VARIO-ELMAR-R 1:3.5/35-70 E60`
  - `LEICA VARIO-ELMAR-R 1:3.5/35-70 E67`

References:

- [Leica Wiki - 35mm-70mm f/3.5 Vario-Elmar-R](https://wiki.l-camera-forum.com/leica-wiki.en/index.php/35mm%E2%80%9370mm_f/3.5_Vario-Elmar-R)
- [Leica Classic - Vario-Elmar-R 3,5/35-70mm](https://classic.leica-camera.com/en/Leica-Systems/R-System/Lenses/Zoom-Lenses/Vario-Elmar-R-3-5-35-70mm/)
- [Leica Classic - Leica VARIO-ELMAR-R 3.5/35-70mm](https://classic.leica-camera.com/en/Leica-VARIO-ELMAR-R-3.5-35-70mm/11244SH-3539474)

### Source B: Leica Wiki - `35mm-70mm f/4 Vario-Elmar-R`

Leica Wiki documents `35mm-70mm f/4 Vario-Elmar-R` with:

- order no.:
  - `11277`
- production era:
  - `1997-2009`
- manufacturer:
  - `Kyocera`
- aperture:
  - `f/4 - f/16`
- filter type:
  - `E60`
- macro function:
  - separate macro-position documented in literature
- built-in hood:
  - documented
- inscription example:
  - `LEICA VARIO-ELMAR-R 1:4/35-70 E60`

References:

- [Leica Wiki - 35mm-70mm f/4 Vario-Elmar-R](https://wiki.l-camera-forum.com/leica-wiki.en/index.php/35mm%E2%80%9370mm_f/4_Vario-Elmar-R)
- [Leica Classic - Vario-Elmar-R 4/35-70mm 11277](https://classic.leica-camera.com/en/Leica-Systems/R-System/Lenses/Zoom-Lenses/Vario-Elmar-R-4-35-70mm-11277/)
- [Leica Classic - Leica Vario-Elmar-R 4.0/35-70mm ROM](https://classic.leica-camera.com/en/Leica-Vario-Elmar-R-4.0-35-70mm-ROM/11277SH-3775759)

### Source C: separate adjacent family - `Vario-Elmarit-R 35-70mm f/2.8 ASPH`

Leica Classic independently documents:

- `Leica Vario-Elmarit-R 35-70mm f/2.8 ASPH`
- order no.:
  - `11275`
- very rare production
- built-in macro function

This is not a `Vario-Elmar-R` row and must remain a separate adjacent family.

References:

- [Leica Classic - Vario-Elmarit-R 2,8/35-70mm ASPH.](https://classic.leica-camera.com/en/Leica-Systems/R-System/Lenses/Zoom-Lenses/Vario-Elmarit-R-2-8-35-70mm-ASPH./11275/)
- [Leica Classic - Leica Vario-Elmarit-R 35-70mm f/2.8 ASPH 11275](https://classic.leica-camera.com/en/Leica-Vario-Elmarit-R-35-70mm-f-2.8-ASPH-11275/11275SH-3839532)

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

- two real `Vario-Elmar-R` candidates that must not be merged:
  - `Leica Vario-Elmar-R 35-70mm f/3.5`
  - `Leica Vario-Elmar-R 35-70mm f/4`

Literature also supports meaningful metadata around:

- `ROM`
- `cam version`
- `E60`
- `E67`
- `macro function`
- filter-thread markers
- built-in hood
- hood / cap / case / packaging ecosystem

But literature does not justify round-1 seed activation by itself. The deciding question is whether local seller titles stabilize the aperture split into usable rows. In the current raw pool, the title split is visible, but price support is absent.

## Boundary Check

This family must remain separate from:

- `Leica Vario-Elmarit-R 28-90mm f/2.8-4.5 ASPH`
- `Leica Vario-Elmarit-R 35-70mm f/2.8 ASPH`
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
- hood-only / cap / case / accessory-only listings

## Local Listing Evidence

Analysis base:

- `data/raw/raw_*.json`
- `data/derived/results_resolved_v2.json`

### Broad retrieval behavior

Broad shorthand is risky.

Within the wider `35-70` raw field, distinct non-family lines already appear:

- `LEICA R7 35-70mm F4 sn.1919`
- `LEICA R8 + winder 35-70 VARIO-ELMAR-R sn.2427`
- `angenieux 35-70mm F2.5-3.3 sn.1513`
- `LEICA 35-70mm F3.5 VABIO-ELMAR-B sn.3489`

Interpretation:

- bare `35-70`
- broad `vario elmar`
- broad `leica r 35-70`
- broad `35 70 elmar`

are not safe shaping aliases in round 1 because the wider retrieval field already mixes:

- Leica body-kit or body-bundle titles
- accessory or bundle-style titles
- non-Leica `35-70` zooms
- typo-corrupted or mount-ambiguous titles

By inference from the broader standard-zoom ecosystem, these shorthands are also vulnerable to drift into:

- `Vario-Elmarit-R 28-90`
- `Vario-Elmarit-SL 24-90`
- third-party `24-70 / 28-70 / 35-70` zooms

### Clean local R-side pool

After restricting to explicit `35-70mm`, explicit R-side `Vario-Elmar-R` wording, and excluding body kits, accessory bundles, `VABIO-ELMAR-B`, `Vario-Elmarit-R 28-90`, R primes, SL/L, and third-party contamination, the usable pool becomes:

- clean local pool: `9`
- unique titles: `7`
- KRW-priced count: `0`
- KRW median: none

Representative clean titles:

- `LEICA 35-70mm F3.5 VARIO-ELMAR-R sn.3538`
- `LEICA 35-70mm F3.5 VARIO-ELMAR-R sn.3653`
- `LEICA 35-70mm F3.5 VARIO-ELMAR-R sn.3734`
- `LEICA 35-70mm F4 VARIO-ELMAR-R sn.3775`
- `LEICA 35-70mm F4 VARIO-ELMAR-R sn.3833`

Observed price behavior:

- all clean rows are `문의요망`
- no clean KRW-priced support exists yet

Interpretation:

- the family is explicit and real in local titles
- the aperture split is visible
- but there is still no usable price evidence for either row
- current evidence is still too thin for round-1 seed activation

### Aperture split stability

The local pool does not collapse into one blended `35-70 Vario-Elmar-R` bucket. It separates cleanly into:

- `Leica Vario-Elmar-R 35-70mm f/3.5`
  - local count: `6`
  - unique titles: `5`
  - KRW-priced: `0`
- `Leica Vario-Elmar-R 35-70mm f/4`
  - local count: `3`
  - unique titles: `2`
  - KRW-priced: `0`

Interpretation:

- `f/3.5` and `f/4` should not be merged into one canonical row
- but neither row currently has enough price evidence to justify activation

### `f/2.8 ASPH` local status

No clean local row in the current reviewed pool stabilizes:

- `Leica Vario-Elmarit-R 35-70mm f/2.8 ASPH`

Interpretation:

- literature confirms it is a real adjacent family
- but it does not belong inside `Vario-Elmar-R 35-70`
- in this round it should remain boundary-only or future-candidate-only, not merged

## Marker / Metadata Observation

Within the current clean `35-70 Vario-Elmar-R` pool, seller wording does not reliably stabilize row-level internal splits for:

- `ROM`
- `cam`
- `E60`
- `E67`
- `macro`
- exact filter-thread wording
- hood / case / boxed

Observed local marker distribution:

- `ROM`: `0`
- `cam`: `0`
- `E60 / E67 wording`: `0`
- explicit `macro` wording: `0`
- hood / case / box wording: `0`

Interpretation:

- `E60 / E67` is literature-real for the `f/3.5` line, but still metadata in round 1
- `macro` is literature-real for the `f/4` line, but should not generate a second row beyond the `f/4` family itself
- these remain overlay or deferred metadata rather than row-level splits

## Smoke Query Review

The following explicit queries are literature-correct and point toward the intended family space:

- `vario-elmar-r 35-70`
- `vario elmar r 35-70`
- `35-70 vario-elmar-r`
- `35-70mm f4 vario-elmar-r`
- `35-70mm f/4 vario-elmar-r`
- `35-70mm f3.5 vario-elmar-r`
- `35-70mm f/3.5 vario-elmar-r`
- `r 35-70/4 vario elmar`
- `r 35-70/3.5 vario elmar`
- `leica r 35-70mm f4`
- `leica r 35-70mm f3.5`

The following broader shorthands are not safe:

- bare `35-70`
- broad `vario elmar`
- broad `leica r 35-70`
- broad `35 70 elmar`

because they can drift into:

- body or bundle titles like `LEICA R7 35-70mm F4`
- accessory or bundle titles like `LEICA R8 + winder 35-70 VARIO-ELMAR-R`
- non-Leica `35-70` zooms such as `angenieux 35-70mm F2.5-3.3`
- adjacent Leica zoom families like `Vario-Elmarit-R 28-90`
- future `SL 24-90` / third-party standard zoom contamination

## Candidate Assessment

### immediate core candidate

None.

There is not enough price support yet for either aperture family.

### strongest deferred candidate

- `Leica Vario-Elmar-R 35-70mm f/3.5`

### secondary deferred candidate

- `Leica Vario-Elmar-R 35-70mm f/4`

### explicit hold candidate

None.

## Overlay / Deferred Metadata

Keep as overlay or deferred metadata only:

- `ROM`
- `cam version`
- `E60`
- `E67`
- `macro mode`
- filter-thread marker
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

- `Leica Vario-Elmarit-R 28-90mm f/2.8-4.5 ASPH`
- `Leica Vario-Elmarit-R 35-70mm f/2.8 ASPH`
- R prime `28mm / 35mm / 50mm / 90mm` families
- `Leica Vario-Elmar-R 70-210mm f/4`
- `Leica Vario-Elmar-R 80-200mm f/4`
- `Leica Vario-Elmar-R 105-280mm f/4.2`
- `Leica Vario-APO-Elmarit-R 70-180mm f/2.8`
- `Leica Vario-Elmarit-SL 24-90mm f/2.8-4`
- `SL / L-mount` zooms
- `LTM 28-90`
- third-party `24-70mm / 28-70mm / 35-70mm` zooms
- accessory-only listings

## Round-1 Verdict

- immediate core candidate:
  - `0`
- recommended first-pass core:
  - none
- strongest deferred candidate:
  - `Leica Vario-Elmar-R 35-70mm f/3.5`
- secondary deferred candidate:
  - `Leica Vario-Elmar-R 35-70mm f/4`
- explicit hold candidate:
  - none

Final round-1 decision:

- `seed 보류`

Why:

1. literature supports both `f/3.5` and `f/4` as real separate Leica R families
2. local titles also show a real aperture split
3. but all clean local rows are unpriced KRW `문의요망`
4. neither row has KRW-priced support or a usable median
5. broad `35-70` / `vario elmar` retrieval already drifts into body kits, bundle rows, and third-party zoom contamination

## Next-Round Recommendation

Do not add seed yet.

Revisit when:

- clean local KRW-priced support appears for `Leica Vario-Elmar-R 35-70mm f/3.5`
- clean local KRW-priced support appears for `Leica Vario-Elmar-R 35-70mm f/4`
- local seller wording continues to keep `f/3.5` and `f/4` separate
- local pool shows the split can be held apart from:
  - `Vario-Elmarit-R 28-90`
  - R prime `28 / 35 / 50 / 90`
  - `Vario-Elmar-R 70-210`
  - `Vario-Elmar-R 80-200`
  - `Vario-Elmar-R 105-280`
  - `Vario-Elmarit-SL 24-90`
  - third-party standard zoom contamination
