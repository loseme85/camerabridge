# Elmar-R 180 Taxonomy Audit - Round 1

Date: 2026-05-15

Scope: audit-only review for the Leica `Elmar-R 180` family. This round does not add seed rows, does not modify `entities/*.json`, does not modify `canonical_entities_index.json`, and does not change classifier/query/search behavior, ranking, or UI.

## Executive Summary

`Elmar-R 180` is literature-real, but round-1 local support is absent, so it should remain closed for now.

Round-1 conclusion:

- immediate recommended `core` candidate count: `0`
- recommended first-pass core:
  - none
- strongest deferred candidate:
  - `Leica Elmar-R 180mm f/4`
- explicit `hold` candidate:
  - none
- literature clearly supports a real Leica R `180mm f/4 Elmar-R` family
- literature also supports real internal marker structure:
  - `3-cam`
  - `Safari`
  - `E55`
  - `MACRO-ADAPTER-R` compatibility
- but local title support is effectively absent after contamination is removed

The safest round-1 answer is:

1. keep `Elmar-R 180` closed for now
2. do not open any `core` or `hold` row
3. keep `Elmarit-R 180`, `APO-Elmarit-R 180`, `APO-Telyt-R 180`, `Vario-APO-Elmarit-R 70-180`, `APO-Summicron-R 180`, `APO-Telyt-R 280`, SL/L telephoto, and third-party telephoto lines as hard boundaries

## Literature / Reference Base

### Source A: Leica Wiki - `180mm f/4 Elmar-R`

Leica Wiki documents `180mm f/4 Elmar-R` with:

- order nos.:
  - `11922`
  - `11924-Safari`
- production era:
  - `1976-1996`
- variants:
  - `3-cam`
  - black
  - olive-green `Safari`
- filter type:
  - `E55`
- accessories:
  - `MACRO-ADAPTER-R`
- inscription:
  - `LEITZ WETZLAR ELMAR-R 1:4/180`

Reference:

- [Leica Wiki - 180mm f/4 Elmar-R](https://wiki.l-camera-forum.com/leica-wiki.en/index.php/180mm_f/4_Elmar-R)

### Source B: Leica Wiki - `180mm f/2.8 Elmarit-R II`

For non-Elmar boundary inside the same focal length, Leica Wiki separately documents:

- `180mm f/2.8 Elmarit-R II`

with:

- production era:
  - `1979-1998`
- variants:
  - `3-cam`
  - `R-only`
- filter type:
  - `E67`

Reference:

- [Leica Wiki - 180mm f/2.8 Elmarit-R II](https://wiki.l-camera-forum.com/leica-wiki.en/index.php/180mm_f/2.8_Elmarit-R_II)

### Source C: Leica Wiki - `180mm f/2.8 APO-Elmarit-R I / II`

For APO boundary, Leica Wiki separately documents:

- `180mm f/2.8 APO-Elmarit-R I`
- `180mm f/2.8 APO-Elmarit-R II`

References:

- [Leica Wiki - 180mm f/2.8 APO-Elmarit-R I](https://wiki.l-camera-forum.com/leica-wiki.en/index.php?title=180mm_f%2F2.8_APO-Elmarit-R_I)
- [Leica Wiki - 180mm f/2.8 APO-Elmarit-R II](https://wiki.l-camera-forum.com/leica-wiki.en/index.php/180mm_f/2.8_APO-Elmarit-R_II)

### Source D: Leica Wiki - `180mm f/3.4 APO-Telyt-R`

For adjacent APO telephoto boundary:

- `180mm f/3.4 APO-Telyt-R`

with:

- production era:
  - `1975-1998`
- variants:
  - `3-cam`
  - `R-cam only`
- filter type:
  - `Series 7.5`
  - `E60`

Reference:

- [Leica Wiki - 180mm f/3.4 APO-Telyt-R](https://wiki.l-camera-forum.com/leica-wiki.en/index.php/180mm_f/3.4_APO-Telyt-R)

### Source E: Leica Wiki - `70mm–180mm f/2.8 Vario-APO-Elmarit-R`

For zoom boundary:

- `70mm–180mm f/2.8 Vario-APO-Elmarit-R`

Reference:

- [Leica Wiki - 70mm-180mm f/2.8 Vario-APO-Elmarit-R](https://wiki.l-camera-forum.com/leica-wiki.en/index.php?title=70mm%E2%80%93180mm_f%2F2.8_Vario-APO-Elmarit-R)

## Taxonomy Implication from Literature

Literature clearly supports:

- one real broad family:
  - `Leica Elmar-R 180mm f/4`

Literature also supports meaningful internal structure:

- `3-cam`
- `Safari`
- `E55`
- macro-adapter ecosystem

However, literature alone is not enough to justify round-1 seed activation. The deciding question is whether local seller titles stabilize this family as a usable row. In the current raw pool, they do not.

## Boundary Check

This family must remain separate from:

- `Leica Elmarit-R 180mm f/2.8`
- `Leica APO-Elmarit-R 180mm f/2.8`
- `Leica APO-Telyt-R 180mm f/3.4`
- generic `Telyt 180`
- `Leica Vario-APO-Elmarit-R 70-180mm f/2.8`
- `Leica APO-Summicron-R 180mm f/2`
- `Leica APO-Telyt-R 280`
- `Leica APO-Telyt-M 135`
- `Leica Elmarit-R 135`
- `Leica Tele-Elmar 135`
- `APO-Summicron-SL 90`
- `APO-Summicron-SL 180`
- `SL / L-mount` lenses
- third-party `180mm` lenses
- hood-only / cap / case / accessory-only listings

## Local Listing Evidence

Analysis base:

- `data/raw/raw_*.json`

### Broad retrieval behavior

Broad shorthand is risky.

Within the wider `180mm` raw field, distinct non-family lines dominate:

- `Leica R 70-180mm f2.8 Vario-Apo-Elmarit Black`
- `[위탁] R 180/2.8 Elmarit (Black)`
- `[위탁] R 180/2.8 APO Elmarit ROM (Black)`
- `Leica R 180mm f3.4 APO-Telyt Black`
- `Leica R 180mm f2 APO-Summicron Black [영상용 개조]`
- `LEICA 180mm F2.8 ROM APO-MACRO-ELMARIT-R sn.3840`
- `LEICA 180mm F2.8 APO-ELMARIT-R sn.3897`
- `Angenieux R 180mm f2 3 APO DEM F Black`

Interpretation:

- broad `elmar 180`
- broad `180 elmar`
- broad `r 180 elmar`

are not safe shaping aliases in round 1 because the wider `180mm` Leica telephoto field is dense and local Elmar-side evidence is not independently strong.

### Clean local R-side pool

After restricting to explicit `180mm`, explicit R-side `Elmar-R` wording, and excluding `Elmarit-R 180`, `APO-Elmarit-R 180`, `APO-Telyt-R 180`, `Vario-APO-Elmarit-R 70-180`, `APO-Summicron-R 180`, `APO-Telyt-R 280`, M-side `135mm`, SL/L, third-party, and accessory contamination, the usable pool becomes:

- clean local pool: `0`
- unique titles: `0`
- KRW-priced count: `0`
- KRW median: `not available`

Interpretation:

- this family is literature-real
- but local title support is effectively absent in round 1
- no seller-title cluster currently stabilizes `Elmar-R 180` as a usable explicit row

### Marker distribution inside local pool

Because the clean local pool is empty, local support is absent for:

- `3-cam`
- `Safari`
- `E55`
- hood / case / boxed
- macro-adapter wording
- finish / country wording

Interpretation:

- literature supports real internal marker structure
- local seller-title support does not yet surface any of it
- therefore all internal markers remain overlay or deferred only

## Smoke Query Review

### Explicit R-side queries

The following are literature-correct but do not currently produce a stable local cluster:

- `elmar-r 180`
- `elmar r 180`
- `180 elmar-r`
- `180mm f4 elmar-r`
- `r 180/4 elmar`
- `leica r 180mm f4`

Interpretation:

- explicit R-side wording is valid conceptually
- but there is no local title repetition strong enough for conservative seed activation

### Broad shorthand risk

Unsafe broad shorthand:

- `elmar 180`
- `180 elmar`
- `r 180 elmar`

Why unsafe:

- broad `elmar` wording is weakly anchored
- the wider `180mm` pool is already dominated by `Elmarit`, `APO-Elmarit`, `APO-Telyt`, zoom, and third-party telephoto listings

## Candidate Review

## Candidate 1: `Leica Elmar-R 180mm f/4`

Pros:

- literature-real Leica R telephoto family
- literature supports meaningful internal marker structure
- clearly distinct from `Elmarit-R 180`, `APO-Elmarit-R 180`, and `APO-Telyt-R 180`

Cons:

- clean local pool is `0`
- unique titles are `0`
- KRW-priced support is `0`
- no stable seller-title cluster currently surfaces the family
- broad shorthand is highly exposed to adjacent `180mm` Leica contamination

Round-1 judgment:

- not ready for immediate `core`
- should remain the strongest deferred candidate

## Hold Candidate Review

No explicit `hold` candidate is recommended in round 1.

Reason:

- there is no local title support for a narrower explicit sub-line
- if the main family itself has no usable local cluster, no `hold` row should open first

## Overlay Elements

These should remain overlay or deferred metadata only:

- `3-cam`
- `Safari`
- `E55`
- `filter thread`
- `MACRO-ADAPTER-R`
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

## Deferred / Not-for-Round-1

Do not open separate rows for:

- `3-cam`
- `Safari`
- `E55`
- macro-adapter bundle
- hood / cap / case / boxed

Do not use strong shaping aliases:

- `elmar 180`
- `180 elmar`
- `r 180 elmar`

## Final Judgment

Round-1 recommendation:

- immediate `core` candidate: `0`
- recommended first-pass core:
  - none
- strongest deferred candidate:
  - `Leica Elmar-R 180mm f/4`
- explicit `hold` candidate:
  - none

The family is real, but local support is absent and broad shorthand is too dangerous.

The main reasons are:

1. literature clearly confirms a distinct Leica R `Elmar-R 180mm f/4` family
2. local usable pool is currently `0`
3. there is no KRW-priced support
4. local seller wording does not surface any internal structure
5. broad `elmar 180` shorthand is too exposed to adjacent Leica `180mm` contamination

## Recommendation for Next Round

Do not add seed yet.

Revisit only if:

- clean local `Elmar-R 180` titles begin appearing independently
- multiple KRW-priced local rows accumulate
- explicit `180mm f/4 Elmar-R` wording starts recurring beyond the current zero-signal local state
