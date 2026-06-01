# Macro-Elmar-R 100 Taxonomy Audit - Round 1

Date: 2026-05-13

Scope: audit-only review for the Leica `Macro-Elmar-R 100` family. This round does not add seed rows, does not modify `entities/*.json`, does not modify `canonical_entities_index.json`, and does not change classifier/query/search behavior, ranking, or UI.

## Executive Summary

`Macro-Elmar-R 100` is literature-real, but round-1 local support is effectively absent, so it should remain closed for now.

Round-1 conclusion:

- immediate recommended `core` candidate count: `0`
- recommended first-pass core:
  - none
- strongest deferred candidate:
  - `Leica Macro-Elmar-R 100mm f/4`
- explicit `hold` candidate:
  - none
- literature clearly supports a real Leica R `100mm f/4 Macro-Elmar-R` family
- literature also documents internal configuration markers and macro-system context:
  - helical / bellows versions
  - `Series VII / E55`
  - macro bellows / adapter ecosystem
- but local title support for the broad family is effectively absent even before internal split questions are considered

The safest round-1 answer is:

1. keep `Macro-Elmar-R 100` closed for now
2. do not open any `core` or `hold` row
3. keep `APO-Macro-Elmarit-R 100`, `Macro-Elmarit-R 60`, R-side `90mm` families, and third-party macro lines as hard boundaries

## Literature / Reference Base

### Source A: Leica Classic - `Macro-Elmar-R 4/100mm`

Leica Classic presents the family under `Macro-Elmar-R 4/100mm` as a distinct R-system tele / macro lens.

Reference:

- [Leica Classic - Macro-Elmar-R 4/100mm](https://classic.leica-camera.com/en/Leica-Systems/R-System/Lenses/Tele-Lenses/Macro-Elmar-R-4-100mm/)

### Source B: Leica Wiki - `100mm f/4 Macro-Elmar-R`

Leica Wiki documents `100mm f/4 Macro-Elmar-R` with:

- order numbers:
  - `11232` helical
  - `11230` bellows
  - `11270` bellows set
- production era:
  - `1978-1995`
- variants:
  - helical `3-cam`
  - bellows unit without cams
- filter types:
  - `Series VII`
  - `E55`
- accessory context:
  - bellows
  - `MACRO-ADAPTER-R`

Reference:

- [Leica Wiki - 100mm f/4 Macro-Elmar-R](https://wiki.l-camera-forum.com/leica-wiki.en/index.php/100mm_f/4_Macro-Elmar-R)

### Boundary literature notes

Adjacent Leica families are also clearly separate in literature:

- `100mm f/2.8 APO-Macro-Elmarit-R`
- `60mm f/2.8 Macro-Elmarit-R`

References:

- [Leica Classic - APO-Macro-Elmarit 2,8/100mm](https://classic.leica-camera.com/en/Leica-Systems/R-System/Lenses/Tele-Lenses/APO-Macro-Elmarit-2-8-100mm/)
- [Leica Wiki - 100mm f/2.8 APO-Macro-Elmarit-R](https://wiki.l-camera-forum.com/leica-wiki.en/index.php?title=100mm_f%2F2.8_APO-Macro-Elmarit-R)
- [Leica Wiki - 60mm f/2.8 Macro-Elmarit-R](https://wiki.l-camera-forum.com/leica-wiki.en/index.php/60mm_f/2.8_Macro-Elmarit-R)

## Taxonomy Implication from Literature

Literature clearly supports:

- one real broad family:
  - `Leica Macro-Elmar-R 100mm f/4`

Literature also supports internal structure and system markers:

- helical / bellows configuration
- `3-cam`
- `Series VII / E55`
- macro bellows / adapter usage

However, literature alone is not enough to justify round-1 seed activation. The deciding question is whether local seller titles stabilize this family as a usable row. In the current raw pool, they do not.

## Boundary Check

This family must remain separate from:

- `Leica APO-Macro-Elmarit-R 100mm f/2.8`
- `Leica Macro-Elmarit-R 60mm f/2.8`
- `Leica Elmarit-R 90mm f/2.8`
- `Leica Summicron-R 90mm f/2`
- `Leica APO-Summicron-R 90mm f/2 ASPH`
- `Leica APO-Telyt-R 180 / 280`
- `SL / L-mount` macro or `90mm` lenses
- third-party `90 / 100 / 105mm` macro lenses
- `ELPRO`-only / adapter-only / hood-only / cap / case / accessory-only listings

## Local Listing Evidence

Analysis base:

- `data/raw/raw_*.json`

### Broad retrieval behavior

Broad shorthand does not stabilize this family in the current local raw pool.

The following query-style surfaces did not produce a usable local R-side cluster:

- `macro-elmar-r 100`
- `macro elmar r 100`
- `macro elmar-r 100`
- `r 100/4 macro elmar`
- `100mm f4 macro elmar-r`
- `100mm f/4 macro elmar-r`
- `leica r 100mm f4 macro`
- `macro elmar 100`

Instead, visible local macro-adjacent results are dominated by:

- `APO-Macro-Elmarit-R 100`
- `Macro-Elmar-M 90`
- `Macro-Elmarit-R 60`
- third-party macro lenses
- accessory / bundle wording such as `ELPRO`

Interpretation:

- seller wording is not converging around explicit `R 100/4 Macro-Elmar` titles
- broad `macro elmar 100` should not be allowed to shape normalization for this family in round 1

### Clean local R-side pool

After restricting to explicit `100mm`, explicit R-side `Macro-Elmar` wording, and excluding `APO-Macro-Elmarit-R 100`, `Macro-Elmarit-R 60`, M-side macro, SL-side, and accessory contamination, the usable pool becomes:

- clean local pool: `0`
- unique titles: `0`
- KRW-priced count: `0`
- KRW median: `not available`

Observed result:

- no stable local clean title for `Leica Macro-Elmar-R 100mm f/4` was confirmed in the current raw pool

Interpretation:

- literature confirms the family is real
- but local evidence is currently below even a thin one-title threshold
- this is materially weaker than recent R-side families that were allowed to open

### Marker distribution inside local pool

Round-1 local support for internal markers is absent:

- helical / bellows split: `0` in a confirmed clean local pool
- `Series VII / E55`: `0`
- `ELPRO`: `0` in a confirmed lens-family pool
- bellows / adapter wording: `0` in a confirmed lens-family pool
- hood / case / boxed: `0`

Interpretation:

- literature supports real macro-system structure
- local seller-title support is absent even for the main family
- therefore internal split discussion is far below seed threshold

## Smoke Query Review

### Explicit R-side queries

No stable local repetition was confirmed for:

- `macro-elmar-r 100`
- `macro elmar r 100`
- `macro elmar-r 100`
- `r 100 macro elmar`
- `100 macro elmar-r`
- `100mm f4 macro elmar-r`
- `100mm f/4 macro elmar-r`
- `r 100/4 macro elmar`
- `leica r 100mm f4 macro`

Interpretation:

- explicit R-side `Macro-Elmar-R 100` wording is not showing a usable local cluster
- there is not enough title repetition to justify a conservative round-1 seed row

### Broad shorthand risk

Unsafe broad shorthand:

- `macro elmar 100`
- `100 macro`

Why unsafe:

- weak Leica R anchoring in local titles
- overlaps with generic macro intent
- can expand into M-side macro, APO `100mm` macro, and third-party macro contamination

## Candidate Review

## Candidate 1: `Leica Macro-Elmar-R 100mm f/4`

Pros:

- literature-real Leica R family
- Leica Classic and Leica Wiki both support the family cleanly
- literature supports a distinct `100mm f/4 Macro-Elmar-R` line rather than a vague macro hypothesis
- literature preserves clear separation from `APO-Macro-Elmarit-R 100`

Cons:

- clean local pool is `0`
- unique title support is `0`
- KRW-priced local support is `0`
- local raw retrieval does not stabilize around explicit R-side `100mm f/4 Macro-Elmar` wording
- broad shorthand is vulnerable to APO / M-side / third-party macro contamination

Round-1 verdict:

- `deferred`

Reason:

- this family is real in literature, but current local evidence is effectively absent, so opening even a narrow explicit seed row would be premature

## Hold Candidate Review

No explicit `hold` candidate is recommended in round 1.

Why:

- there is no narrower wording with stronger local repetition than the already-absent main family
- helical / bellows / `Series VII / E55` / adapter markers are real metadata or configuration context, not locally stable row candidates

## Overlay Elements

Keep these as overlay or deferred metadata only:

- `Elpro included`
- `macro adapter included`
- `bellows / adapter wording`
- `tripod collar included`
- `filter thread`
- `black / finish`
- `country marking`
- `hood included`
- `cap included`
- `boxed`
- `case included`
- `condition`
- `original cap`
- `original hood`
- `original box`
- `original case`
- `packaging`

These should not become separate rows in round 1.

## Deferred / Not-for-Round-1

Do not open separate rows for:

- `Elpro included`
- `macro adapter included`
- bellows configuration
- helical configuration
- `Series VII / E55`
- `filter thread`

Do not use as strong shaping aliases:

- `macro elmar 100`
- `100 macro`

Reason:

- these are either under-supported bundle / configuration markers or broad shorthand with weak Leica R anchoring

## Out-of-Family Boundary

Must remain outside this family:

- `Leica APO-Macro-Elmarit-R 100mm f/2.8`
- `Leica Macro-Elmarit-R 60mm f/2.8`
- Leica R `90mm` families
- `Leica APO-Telyt-R 180 / 280`
- `SL / L-mount` macro or `90mm` lenses
- accessory-only listings
- third-party `90 / 100 / 105mm` macro lenses

## Final Round-1 Judgment

Immediate round-1 answer:

- immediate core candidate:
  - `0`
- hold candidate:
  - none

Strongest deferred candidate:

- `Leica Macro-Elmar-R 100mm f/4`

Round-1 decision:

- `seed 보류`

Why:

1. literature clearly confirms a real Leica R macro family
2. literature clearly separates it from `APO-Macro-Elmarit-R 100`
3. local usable evidence is effectively absent
4. broad macro shorthand is not anchored enough to Leica R in the current pool

## Recommendation for Next Round

Do not add a seed row yet.

Only revisit if one of the following improves:

- multiple clean local `Macro-Elmar-R 100` titles appear
- KRW-priced local rows accumulate
- explicit `R 100/4 Macro-Elmar` wording stabilizes independently from `APO-Macro-Elmarit-R 100`, M-side macro, and third-party macro listings

If future evidence improves, the next candidate to open would still be:

- `Leica Macro-Elmar-R 100mm f/4`

But round-1 should keep the family closed.
