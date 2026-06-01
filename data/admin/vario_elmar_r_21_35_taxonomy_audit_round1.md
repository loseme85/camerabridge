# Vario-Elmar-R 21-35 Taxonomy Audit - Round 1

Date: 2026-05-20

Scope: audit-only review for the Leica `Vario-Elmar-R 21-35` family. This round does not add seed rows, does not modify `entities/*.json`, does not modify `canonical_entities_index.json`, and does not change classifier/query/search behavior, ranking, or UI.

## Executive Summary

`Vario-Elmar-R 21-35` is literature-real, and round-1 local evidence is strong enough to identify one narrow immediate seed candidate for a future seed round.

Round-1 conclusion:

- immediate recommended `core` candidate count: `1`
- recommended first-pass core:
  - `Leica Vario-Elmar-R 21-35mm f/3.5-4 ASPH`
- explicit `hold` candidate:
  - none
- literature clearly supports one real Leica R `21-35mm f/3.5-4 ASPH Vario-Elmar-R` family
- no separate aperture-distinct Leica R `21-35mm` family was confirmed in primary literature for this round
- local title support is narrow but stable:
  - explicit `R 21-35/3.5-4.5 Vario Elmar ASPH ROM`
  - repeated `21-35mm F3.5-4 VARIO-ELMAR-R`
  - repeated `21-35mm F3.5-4 ASPH VARIO-ELMAR-R`
- priced observations exist in KRW and cluster in a coherent band
- broad `21-35` / `vario elmar` / `leica r 21-35` / `21 35 elmar` retrieval remains unsafe and must not be hard-pinned

The safest round-1 answer is:

1. recognize `Leica Vario-Elmar-R 21-35mm f/3.5-4 ASPH` as an immediate future seed candidate
2. do not open any internal version row
3. keep `ROM`, `cam`, `ASPH`, `E67`, hood/case bundles, and similar details as overlay or deferred metadata
4. keep R wide primes, M `Tri-Elmar / WATE`, R standard zooms, SL/L wide zooms, and third-party wide zooms as hard boundaries

## Literature / Reference Base

### Source A: Leica Classic - `Vario-Elmar-R 3,5-4/21-35mm ASPH.`

Leica Classic documents:

- `Vario-Elmar-R 3,5-4/21-35mm ASPH.`
- order no.:
  - `11274`

This establishes a real Leica R wide zoom family with `ASPH` as part of the literature identity.

References:

- [Leica Classic - Vario-Elmar-R 3,5-4/21-35mm ASPH.](https://classic.leica-camera.com/en/Leica-Systems/R-System/Lenses/Zoom-Lenses/Vario-Elmar-R-3-5-4-21-35mm-ASPH./)
- [Leica Classic - LEICA VARIO-ELMAR-R 1:3.5-4/21-35 ASPH. 11274](https://classic.leica-camera.com/de/LEICA-VARIO-ELMAR-R-1-3-5-4-21-35-ASPH.-11274/11274SH-3951553)

### Source B: Leica Wiki - `21mm-35mm f/3.5-f/4.0 ASPH. Vario-Elmar-R`

Leica Wiki documents:

- order no.:
  - `11274`
- production era:
  - `2002-2009`
- Leica R bayonet identity
- filter:
  - internal thread for screw-in filters `E67`
- hood:
  - `12438`
- inscription example:
  - `VARIO-ELMAR-R 1:3.5-4/21-35 ASPH. E67`

Reference:

- [Leica Wiki - 21mm-35mm f/3.5-f/4.0 ASPH. Vario-Elmar-R](https://wiki.l-camera-forum.com/leica-wiki.en/index.php/21mm%E2%80%9335mm_f/3.5%E2%80%93f/4.0_ASPH._Vario-Elmar-R)

### Source C: adjacent Leica R / M / SL boundaries

Separate neighboring families are independently documented:

- R prime `21 / 24 / 28 / 35`
- `Vario-Elmar-R 28-70mm f/3.5-4.5`
- `Vario-Elmarit-R 28-90mm f/2.8-4.5 ASPH`
- `Vario-Elmar-R 35-70mm f/3.5`
- `Vario-Elmar-R 35-70mm f/4`
- M `Tri-Elmar 16-18-21 / WATE`
- M `Tri-Elmar 28-35-50 / MATE`
- `Vario-Elmarit-SL 16-35`
- `Vario-Elmarit-SL 24-90`

References:

- [Leica Classic - Vario-Elmar-R 3,5-4,5/28-70mm](https://classic.leica-camera.com/en/Leica-Systems/R-System/Lenses/Zoom-Lenses/Vario-Elmar-R-3-5-4-5-28-70mm/)
- [Leica Classic - Vario-Elmarit-R 2,8-4,5/28-90mm ASPH.](https://classic.leica-camera.com/en/Leica-Systems/R-System/Lenses/Zoom-Lenses/Vario-Elmarit-R-2-8-4-5-28-90mm-ASPH./)
- [Leica Wiki - 35mm-70mm f/3.5 Vario-Elmar-R](https://wiki.l-camera-forum.com/leica-wiki.en/index.php/35mm%E2%80%9370mm_f/3.5_Vario-Elmar-R)
- [Leica Wiki - 35mm-70mm f/4 Vario-Elmar-R](https://wiki.l-camera-forum.com/leica-wiki.en/index.php/35mm%E2%80%9370mm_f/4_Vario-Elmar-R)
- [Leica Camera - Super-Vario-Elmarit-SL 16-35 f/3.5-4.5 ASPH.](https://leica-camera.com/en-US/photography/lenses/sl/super-vario-elmarit-sl-16-35mm-f3-5-4-5-asph-black)
- [Leica Camera - Vario-Elmarit-SL 24-90 f/2.8-4 ASPH.](https://leica-camera.com/en-US/photography/lenses/sl/vario-elmarit-sl-24-90mm-f2-8-4-asph-black)

## Taxonomy Implication from Literature

Literature clearly supports:

- one real family:
  - `Leica Vario-Elmar-R 21-35mm f/3.5-4 ASPH`

No separate aperture-distinct Leica R `21-35mm` family was confirmed in primary literature for this round.

Literature also supports metadata structure around:

- `ROM`
- `cam version`
- `ASPH`
- `E67`
- filter-thread marker
- hood / cap / case / packaging ecosystem

One Leica Classic used-store page uses `f/3.5-5 ASPH` wording on an individual listing, but the family page and Leica Wiki consistently identify the canonical family as `f/3.5-4 ASPH`. The round-1 canonical reading should therefore remain `f/3.5-4 ASPH`.

## Boundary Check

This family must remain separate from:

- `Leica Elmarit-R 21mm`
- `Leica Elmarit-R 24mm`
- `Leica Elmarit-R 28mm`
- `Leica Elmarit-R 35mm`
- `Leica Summicron-R 35mm f/2`
- `Leica Summilux-R 35mm f/1.4`
- `Leica Vario-Elmar-R 28-70mm f/3.5-4.5`
- `Leica Vario-Elmarit-R 28-90mm f/2.8-4.5 ASPH`
- `Leica Vario-Elmar-R 35-70mm f/3.5`
- `Leica Vario-Elmar-R 35-70mm f/4`
- `Leica Tri-Elmar-M 16-18-21mm f/4 ASPH`
- `Leica Tri-Elmar-M 28-35-50mm f/4 ASPH`
- `Leica Super-Elmar-M 21mm f/3.4 ASPH`
- `Leica Summilux-M 21mm f/1.4 ASPH`
- `Vario-Elmarit-SL 16-35`
- `Vario-Elmarit-SL 24-90`
- `SL / L-mount` zooms
- third-party `16-35mm / 17-35mm / 20-35mm / 21-35mm` zooms
- accessory-only listings

## Local Listing Evidence

Analysis base:

- `data/normalized/normalized_latest.json`
- `data/raw/raw_*.json`
- `data/derived/results_resolved_v2.json`
- `data/sold_items.json`

### Broad retrieval behavior

Broad shorthand is risky.

Within the wider `21-35` field, neighboring or contaminating patterns are nearby or structurally plausible:

- R prime `21 / 24 / 28 / 35`
- M `Tri-Elmar 16-18-21 / WATE`
- M `Tri-Elmar 28-35-50 / MATE`
- `SL 16-35`
- third-party `16-35 / 17-35 / 20-35 / 21-35`
- hood / cap / case-only rows

Interpretation:

- bare `21-35`
- broad `vario elmar`
- broad `leica r 21-35`
- broad `21 35 elmar`

are not safe shaping aliases in round 1 because they can drift into:

- Leica R wide primes
- M `Tri-Elmar / WATE`
- SL/L wide zooms
- third-party wide zooms
- accessory-only listings

### Clean local R-side pool

After restricting to explicit `21-35mm`, explicit R-side `Vario-Elmar-R` wording, and excluding primes, M Tri-Elmar, SL/L, third-party, and accessory contamination, the usable pool becomes:

- clean local pool: `6`
- unique titles: `5`
- KRW-priced count: `2`
- KRW median: `2,740,000 KRW`

Representative clean titles:

- `[중고] R 21-35/3.5-4.5 Vario Elmar ASPH ROM (Black)`
- `LEICA 21-35mm F3.5-4 VARIO-ELMAR-R sn.3942`
- `LEICA 21-35mm F3.5-4 VARIO-ELMAR-R sn.3950`
- `LEICA 21-35mm F3.5-4 ASPH VARIO-ELMAR-R sn.3950`
- `LEICA 21-35mm F3.5-4 ASPH VARIO-ELMAR-R sn.3941`

Observed KRW price points:

- `3,180,000 KRW`
- `2,300,000 KRW`

Interpretation:

- local wording is family-correct
- multiple independent title shapes converge on the same intended R-side family
- priced observations exist and are coherent enough for a future narrow seed row

### Explicit wording stability

The local pool does not rely on a single fragile token. It repeats across:

- `R 21-35/3.5-4.5 Vario Elmar ASPH ROM`
- `21-35mm F3.5-4 VARIO-ELMAR-R`
- `21-35mm F3.5-4 ASPH VARIO-ELMAR-R`

Interpretation:

- family recognition is stable at the main-row level
- `ASPH` omission in some seller titles does not behave like a different family
- `ROM` appears, but not as a separate priced or separately title-stable internal row

## Marker / Metadata Observation

Within the current clean `21-35 Vario-Elmar-R` pool, seller wording does not reliably stabilize row-level internal splits for:

- `ROM`
- `cam`
- exact filter-thread wording
- hood / case / boxed

Observed local marker distribution:

- `ROM`: `1`
- `ASPH`: `3`
- `cam`: `0`
- exact filter-thread wording: `0`
- hood / case / box wording: `0`

Interpretation:

- `ROM` is present but not enough to justify a separate row
- `ASPH` is literature-real and part of the main canonical row
- these remain overlay or deferred metadata rather than row-level splits

## Smoke Query Review

The following explicit queries are literature-correct and point toward the intended family:

- `vario-elmar-r 21-35`
- `vario elmar r 21-35`
- `21-35 vario-elmar-r`
- `21-35mm f3.5-4 vario-elmar-r`
- `21-35mm f/3.5-4 vario-elmar-r`
- `21-35mm asph vario-elmar-r`
- `r 21-35/3.5-4 vario elmar`
- `leica r 21-35mm f3.5-4`
- `leica r 21-35mm f/3.5-4`
- `leica r 21-35 asph`
- `vario elmar 21-35`

These queries resolve to a narrow, coherent family cluster.

The following broader shorthands are not safe:

- bare `21-35`
- broad `vario elmar`
- broad `leica r 21-35`
- broad `21 35 elmar`

because they can drift into:

- R wide prime families
- M `Tri-Elmar / WATE`
- `Vario-Elmar-R 28-70`
- `Vario-Elmarit-R 28-90`
- `Vario-Elmar-R 35-70`
- `SL / L-mount` wide zooms
- third-party wide zooms
- accessory-only listings

## Candidate Assessment

### immediate core candidate

- `Leica Vario-Elmar-R 21-35mm f/3.5-4 ASPH`

### explicit hold candidate

None.

## Overlay / Deferred Metadata

Keep as overlay or deferred metadata only:

- `ROM`
- `cam version`
- `ASPH`
- `E67`
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

- R prime `21mm / 24mm / 28mm / 35mm` families
- `Leica Vario-Elmar-R 28-70mm f/3.5-4.5`
- `Leica Vario-Elmarit-R 28-90mm f/2.8-4.5 ASPH`
- `Leica Vario-Elmar-R 35-70mm f/3.5`
- `Leica Vario-Elmar-R 35-70mm f/4`
- M `Tri-Elmar 16-18-21 / WATE`
- M `Tri-Elmar 28-35-50 / MATE`
- `Vario-Elmarit-SL 16-35`
- `Vario-Elmarit-SL 24-90`
- `SL / L-mount` zooms
- third-party `16-35mm / 17-35mm / 20-35mm / 21-35mm` zooms
- accessory-only listings

## Round-1 Verdict

- immediate core candidate:
  - `1`
- recommended first-pass core:
  - `Leica Vario-Elmar-R 21-35mm f/3.5-4 ASPH`
- explicit hold candidate:
  - none

Final round-1 decision:

- `future seed candidate 인정`

Why:

1. literature clearly supports one real Leica R `21-35mm f/3.5-4 ASPH` family
2. no additional aperture-distinct Leica R `21-35mm` family was confirmed in primary literature
3. local titles repeatedly surface explicit family-correct wording
4. KRW-priced support exists and clusters coherently
5. broad shorthand is still unsafe, so any future seed should be narrow and explicit

## Next-Round Recommendation

If seed is added later, open only one narrow core row:

- `Leica Vario-Elmar-R 21-35mm f/3.5-4 ASPH`

Do not add broad shorthand as strong alias yet.
