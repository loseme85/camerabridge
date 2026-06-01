# APO-Telyt-R 180 Taxonomy Audit - Round 1

Date: 2026-05-14

Scope: audit-only review for the Leica `APO-Telyt-R 180` family. This round does not add seed rows, does not modify `entities/*.json`, does not modify `canonical_entities_index.json`, and does not change classifier/query/search behavior, ranking, or UI.

## Executive Summary

`APO-Telyt-R 180` is literature-real, but round-1 local support is still too thin and price support is minimal, so it should remain closed for now.

Round-1 conclusion:

- immediate recommended `core` candidate count: `0`
- recommended first-pass core:
  - none
- strongest deferred candidate:
  - `Leica APO-Telyt-R 180mm f/3.4`
- explicit `hold` candidate:
  - none
- literature clearly supports a real Leica R `180mm f/3.4 APO-Telyt-R` family
- literature also supports real internal marker structure:
  - `3-cam`
  - `R-cam only`
  - `Series 7.5`
  - `E60`
- but local title support is still narrow, concentrated in only two repeated title shapes, and has only one KRW-priced observation

The safest round-1 answer is:

1. keep `APO-Telyt-R 180` closed for now
2. do not open any `core` or `hold` row
3. keep `APO-Elmarit-R 180`, `Elmarit-R 180`, classic `Elmar-R 180`, generic `Telyt 180`, `APO-Telyt-R 280`, M-side `APO-Telyt-M 135`, SL/L telephoto, and third-party telephoto lines as hard boundaries

## Literature / Reference Base

### Source A: Leica Wiki - `180mm f/3.4 APO-Telyt-R`

Leica Wiki documents `180mm f/3.4 APO-Telyt-R` with:

- order numbers:
  - `11240`
  - `11242`
- production era:
  - `1975-1998`
- variants:
  - `3-cam`
  - `R-cam only`
- filter type:
  - `Series 7.5` early
  - `E60` late
- inscription:
  - `LEITZ CANADA APO-TELYT-R 1:3.4/180`

Reference:

- [Leica Wiki - 180mm f/3.4 APO-Telyt-R](https://wiki.l-camera-forum.com/leica-wiki.en/index.php/180mm_f/3.4_APO-Telyt-R)

### Source B: Leica Wiki - `180mm f/2.8 APO-Elmarit-R I`

Leica Wiki separately documents the faster telephoto line:

- `180mm f/2.8 APO-Elmarit-R I`

with:

- production era:
  - `1998-2004`
- filter type:
  - `Series VIII`
- accessories:
  - `Leica APO-EXTENDER-R 2x`

Reference:

- [Leica Wiki - 180mm f/2.8 APO-Elmarit-R I](https://wiki.l-camera-forum.com/leica-wiki.en/index.php?title=180mm_f%2F2.8_APO-Elmarit-R_I)

### Source C: Leica Wiki - `180mm f/2.8 APO-Elmarit-R II`

Leica Wiki also documents:

- `180mm f/2.8 APO-Elmarit-R II`

with:

- production era:
  - `2004-2009`
- filter type:
  - `E67`
- built-in hood
- rotating tripod collar support

Reference:

- [Leica Wiki - 180mm f/2.8 APO-Elmarit-R II](https://wiki.l-camera-forum.com/leica-wiki.en/index.php/180mm_f/2.8_APO-Elmarit-R_II)

### Source D: Leica Wiki - `180mm f/2.8 Elmarit-R II`

Leica Wiki separately documents the non-APO telephoto line:

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

### Source E: Leica Wiki - `180mm f/4 Elmar-R`

For adjacent classic R telephoto boundary, Leica Wiki documents:

- `180mm f/4 Elmar-R`

with:

- production era:
  - `1976-1996`
- variants:
  - `3-cam`
  - `Safari`
- filter type:
  - `E55`

Reference:

- [Leica Wiki - 180mm f/4 Elmar-R](https://wiki.l-camera-forum.com/leica-wiki.en/index.php/180mm_f/4_Elmar-R)

## Taxonomy Implication from Literature

Literature clearly supports:

- one real broad family:
  - `Leica APO-Telyt-R 180mm f/3.4`

Literature also supports meaningful internal structure:

- `3-cam`
- `R-cam only`
- `Series 7.5`
- `E60`
- country inscription variation

Literature also makes boundary separation clear:

- `APO-Telyt-R 180` is not the same as `APO-Elmarit-R 180mm f/2.8`
- `APO-Telyt-R 180` is not the same as `Elmarit-R 180mm f/2.8`
- `APO-Telyt-R 180` is not the same as `APO-Telyt-R 280`
- classic `Elmar-R 180` and generic `Telyt 180` wording should not be allowed to collapse into the same row

However, literature alone is not enough to justify round-1 seed activation. The deciding question is whether local seller titles stabilize this family as a usable row. In the current raw pool, they do not yet do so strongly enough.

## Boundary Check

This family must remain separate from:

- `Leica APO-Elmarit-R 180mm f/2.8`
- `Leica Elmarit-R 180mm f/2.8`
- classic `Leica Elmar-R 180mm f/4`
- generic `Telyt 180`
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

When the local raw pool is widened to `180` plus `apo` / `telyt`, distinct non-family lines appear:

- `Leica R 180mm f2.8 APO-Elmart Rom Black`
- `Leica R 70-180mm f2.8 Vario-Apo-Elmarit Black`
- `Leica R 180mm f3.4 APO-Telyt Black`
- `Leica R 180mm f2 APO-Summicron Black [영상용 개조]`
- `[위탁] R 180/2.8 APO Elmarit ROM (Black)`
- `LEICA 180mm F2.8 ROM APO-MACRO-ELMARIT-R sn.3840`
- `LEICA 180mm F2.8 APO-ELMARIT-R sn.3897`
- `Angenieux R 180mm f2 3 APO DEM F Black`

Interpretation:

- broad `apo telyt 180`
- broad `telyt 180`
- broad `180 apo`

cannot be trusted as shaping aliases in round 1 because the wider `180mm` Leica telephoto field is crowded with adjacent APO and non-APO R lines.

### Clean local R-side pool

After restricting to explicit `180mm`, explicit R-side `APO-Telyt-R` wording, and excluding `APO-Elmarit-R 180`, `Elmarit-R 180`, `APO-Telyt-R 280`, M-side `APO-Telyt-M 135`, SL/L, third-party, and accessory contamination, the usable pool becomes:

- clean local pool: `2`
- unique titles: `2`
- KRW-priced count: `1`
- KRW median: `500000`

Representative clean titles:

- `Leica R 180mm f3.4 APO-Telyt Black`
- `LEICA 180mm F3.4 APO-TELYT-R sn.3478`

Interpretation:

- this confirms the family is not imaginary in local data
- but seller wording is still narrow and not especially diverse
- only one KRW-priced observation is not enough to treat price behavior as stable
- this is materially weaker than the rounds where a narrow `core` row was immediately justified

### Marker distribution inside local pool

Round-1 local support for internal markers is absent or too weak:

- `ROM`: `0`
- `cam`: `0` in seller-title wording
- `Series / E60 / E67`: `0`
- hood / case / boxed: `0`

Visible but not row-level:

- `Black`

Interpretation:

- literature supports real internal marker structure
- local seller-title support is only for the broad family, not for marker-level splits
- `Black` appears as a finish description, not a canonical row candidate
- therefore internal rows are clearly out of scope for now

## Smoke Query Review

### Explicit R-side queries

Usable but still modest evidence appears in explicit product wording:

- `apo-telyt-r 180`
- `apo telyt r 180`
- `180mm f3.4 apo-telyt-r`
- `leica r 180mm f3.4 apo`

The same two title shapes recur:

- `Leica R 180mm f3.4 APO-Telyt Black`
- `LEICA 180mm F3.4 APO-TELYT-R sn.3478`

Interpretation:

- explicit R-side wording can find real family evidence
- but repetition is still too narrow for conservative seed activation

### Broad shorthand risk

Unsafe broad shorthand:

- `apo telyt 180`
- `telyt 180`
- `180 apo`

Why unsafe:

- overlaps with other `180mm` Leica APO lines
- drifts into `APO-Elmarit-R 180`
- drifts into `Vario-APO-Elmarit-R 70-180`
- drifts into `APO-Summicron-R 180`
- can cross into third-party `180mm` telephoto listings

## Candidate Review

## Candidate 1: `Leica APO-Telyt-R 180mm f/3.4`

Pros:

- literature-real Leica R family
- literature supports long production history and real internal marker structure
- local titles do confirm multiple explicit R-side product instances

Cons:

- clean local pool is only `2`
- unique titles are only `2`
- local evidence is concentrated in only two repeated seller-title shapes
- KRW-priced support is only `1`
- broad shorthand is highly exposed to adjacent Leica `180mm` contamination

Round-1 judgment:

- not ready for immediate `core`
- should remain the strongest deferred candidate

## Hold Candidate Review

No explicit `hold` candidate is recommended in round 1.

Reason:

- there is not enough evidence for a stable explicit sub-line below the main family
- marker-level wording remains literature-real but locally under-supported
- if the main line itself is not yet opened, no narrower explicit `hold` row should be opened first

## Overlay Elements

These should remain overlay or deferred metadata only:

- `ROM`
- `cam version`
- `3-cam`
- `R-cam only`
- `Series 7.5 / E60`
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

## Deferred / Not-for-Round-1

Do not open separate rows for:

- `ROM`
- `cam version`
- `Series 7.5 / E60`
- `filter thread`
- hood / cap / case / boxed

Do not use strong shaping aliases:

- `apo telyt 180`
- `telyt 180`
- `180 apo`

## Final Judgment

Round-1 recommendation:

- immediate `core` candidate: `0`
- recommended first-pass core:
  - none
- strongest deferred candidate:
  - `Leica APO-Telyt-R 180mm f/3.4`
- explicit `hold` candidate:
  - none

The family is real, but local support is still too thin for conservative seed activation.

The main reasons are:

1. literature clearly confirms a distinct Leica R `APO-Telyt-R 180mm f/3.4` family
2. local explicit titles do show the family
3. the local pool is still only two repeated title shapes
4. KRW-priced support is minimal
5. broad `apo telyt 180` / `telyt 180` / `180 apo` are too exposed to adjacent Leica `180mm` contamination

## Recommendation for Next Round

Do not add seed yet.

Revisit only if:

- more clean local title diversity appears
- multiple KRW-priced local rows accumulate
- explicit `APO-Telyt-R 180` wording keeps recurring independently of the current two repeated title shapes
