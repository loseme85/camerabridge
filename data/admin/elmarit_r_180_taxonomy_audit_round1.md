# Elmarit-R 180 Taxonomy Audit - Round 1

Date: 2026-05-14

Scope: audit-only review for the Leica `Elmarit-R 180` family. This round does not add seed rows, does not modify `entities/*.json`, does not modify `canonical_entities_index.json`, and does not change classifier/query/search behavior, ranking, or UI.

## Executive Summary

`Elmarit-R 180` is literature-real, but round-1 local support is too thin and too concentrated to justify immediate seed activation.

Round-1 conclusion:

- immediate recommended `core` candidate count: `0`
- recommended first-pass core:
  - none
- strongest deferred candidate:
  - `Leica Elmarit-R 180mm f/2.8`
- explicit `hold` candidate:
  - none
- literature clearly supports a real Leica R non-APO `180mm f/2.8 Elmarit-R` family
- literature also supports real internal marker structure:
  - `Elmarit-R I / II`
  - `3-cam`
  - `R-only`
  - `E67`
- but local title support collapses to one repeated seller-title pattern, with only one KRW-priced observation

The safest round-1 answer is:

1. keep `Elmarit-R 180` closed for now
2. do not open any `core` or `hold` row
3. keep `APO-Elmarit-R 180`, `APO-Telyt-R 180`, classic `Elmar-R 180`, `Vario-APO-Elmarit-R 70-180`, `APO-Summicron-R 180`, `APO-Telyt-R 280`, SL/L telephoto, and third-party telephoto lines as hard boundaries

## Literature / Reference Base

### Source A: Leica Wiki - `180mm f/2.8 Elmarit-R I`

Leica Wiki documents `180mm f/2.8 Elmarit-R I` with:

- production era:
  - `1970-1977`
- variants:
  - `1-cam`
  - `2-cam`
  - `3-cam`
- filter type:
  - `Series VIII`

Reference:

- [Leica Wiki - 180mm f/2.8 Elmarit-R I](https://wiki.l-camera-forum.com/leica-wiki.en/index.php?title=180mm_f%2F2.8_Elmarit-R_I)

### Source B: Leica Wiki - `180mm f/2.8 Elmarit-R II`

Leica Wiki documents `180mm f/2.8 Elmarit-R II` with:

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

For hard APO boundary, Leica Wiki separately documents:

- `180mm f/2.8 APO-Elmarit-R I`
- `180mm f/2.8 APO-Elmarit-R II`

with separate APO-specific construction, late `ROM`, `Series VIII` / `E67`, and built-in hood / tripod collar structure on later line.

References:

- [Leica Wiki - 180mm f/2.8 APO-Elmarit-R I](https://wiki.l-camera-forum.com/leica-wiki.en/index.php?title=180mm_f%2F2.8_APO-Elmarit-R_I)
- [Leica Wiki - 180mm f/2.8 APO-Elmarit-R II](https://wiki.l-camera-forum.com/leica-wiki.en/index.php/180mm_f/2.8_APO-Elmarit-R_II)

### Source D: Leica Wiki - `180mm f/3.4 APO-Telyt-R`

For adjacent APO telephoto boundary, Leica Wiki documents:

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

### Source E: Leica Wiki - `180mm f/4 Elmar-R`

For classic non-Elmarit telephoto boundary, Leica Wiki documents:

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

### Source F: Leica Wiki - `70mm–180mm f/2.8 Vario-APO-Elmarit-R`

For zoom boundary:

- `70mm–180mm f/2.8 Vario-APO-Elmarit-R`

Reference:

- [Leica Wiki - 70mm-180mm f/2.8 Vario-APO-Elmarit-R](https://wiki.l-camera-forum.com/leica-wiki.en/index.php?title=70mm%E2%80%93180mm_f%2F2.8_Vario-APO-Elmarit-R)

## Taxonomy Implication from Literature

Literature clearly supports:

- one real broad non-APO family:
  - `Leica Elmarit-R 180mm f/2.8`

Literature also supports real internal structure:

- `Elmarit-R I`
- `Elmarit-R II`
- `1-cam / 2-cam / 3-cam`
- `R-only`
- `Series VIII`
- `E67`

However, literature alone does not justify row splitting in round 1.

The round-1 question is not whether internal structure exists. It does. The question is whether local seller titles reliably surface that split. In the current raw pool, they do not.

## Boundary Check

This family must remain separate from:

- `Leica APO-Elmarit-R 180mm f/2.8`
- `Leica APO-Telyt-R 180mm f/3.4`
- classic `Leica Elmar-R 180mm f/4`
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

Broad `elmarit 180` retrieval is highly risky.

When the local raw pool is widened to `180` plus `elmarit`, distinct non-family lines appear:

- `Leica R 70-180mm f2.8 Vario-Apo-Elmarit Black`
- `[위탁] R 180/2.8 APO Elmarit ROM (Black)`
- `[중고] R 180/2.8 APO Elmarit ROM (Black)`
- `LEICA 180mm F2.8 ROM APO-MACRO-ELMARIT-R sn.3840`
- `LEICA 180mm F2.8 APO-ELMARIT-R sn.3897`
- `Leica R 180mm f3.4 APO-Telyt Black`
- `Leica R 180mm f2 APO-Summicron Black [영상용 개조]`
- `Angenieux R 180mm f2 3 APO DEM F Black`

Interpretation:

- broad `elmarit 180`
- broad `180 elmarit`
- broad `r 180 elmarit`

cannot be trusted as shaping aliases in round 1 because the wider `180mm` Leica telephoto field is dominated by APO, zoom, and neighboring R telephoto lines.

### Clean local R-side pool

After restricting to explicit `180mm`, explicit R-side non-APO `Elmarit-R` wording, and excluding `APO-Elmarit-R 180`, `APO-Telyt-R 180`, classic `Elmar-R 180`, `Vario-APO-Elmarit-R 70-180`, `APO-Summicron-R 180`, `APO-Telyt-R 280`, M-side `APO-Telyt-M 135`, SL/L, third-party, and accessory contamination, the usable pool becomes:

- clean local pool: `1`
- unique titles: `1`
- KRW-priced count: `1`
- KRW median: `2200000`

Representative clean title:

- `[위탁] R 180/2.8 Elmarit (Black)`

Interpretation:

- this confirms non-APO `Elmarit-R 180` is not imaginary in local data
- but local support is effectively a single seller-title pattern
- one KRW-priced observation is not enough to show stable family price behavior
- this is weaker than other rounds already kept closed

### Marker distribution inside local pool

Round-1 local support for internal markers is absent:

- `ROM`: `0`
- `cam / R-only`: `0`
- `E67 / Series`: `0`
- hood / case / boxed: `0`
- explicit `I / II` markers: `0`

Interpretation:

- literature supports real internal marker structure
- local seller-title support is only for the broad family, not for marker-level splits
- therefore `I / II`, `ROM`, cam, and filter-thread rows are clearly out of scope for now

## Smoke Query Review

### Explicit R-side queries

Usable but very thin evidence appears in explicit product wording:

- `elmarit-r 180`
- `180mm f2.8 elmarit-r`
- `r 180/2.8 elmarit`
- `leica r 180mm f2.8`

But the usable local pool collapses to a single stable pattern:

- `[위탁] R 180/2.8 Elmarit (Black)`

Interpretation:

- explicit R-side wording can find a real family signal
- but repetition is too thin for conservative seed activation

### Broad shorthand risk

Unsafe broad shorthand:

- `elmarit 180`
- `180 elmarit`
- `r 180 elmarit`

Why unsafe:

- overlaps with `APO-Elmarit-R 180`
- drifts into `Vario-APO-Elmarit-R 70-180`
- drifts into `APO-Macro-Elmarit-R 100`
- drifts into `APO-Telyt-R 180`
- reaches non-Leica `180mm` telephoto listings

## Candidate Review

## Candidate 1: `Leica Elmarit-R 180mm f/2.8`

Pros:

- literature-real Leica R non-APO telephoto family
- literature supports meaningful internal structure and long production run
- local titles do confirm at least one explicit R-side family instance

Cons:

- clean local pool is only `1`
- unique titles are only `1`
- local evidence is effectively one repeated seller-title shape
- priced support is only one observation
- local seller wording does not support `I / II` splitting
- broad shorthand is highly exposed to adjacent `180mm` Leica contamination

Round-1 judgment:

- not ready for immediate `core`
- should remain the strongest deferred candidate

## Hold Candidate Review

No explicit `hold` candidate is recommended in round 1.

Reason:

- `I / II` are literature-real but not locally title-stable
- there is not enough explicit recurring seller wording for a narrower safe row
- if the main family itself is not yet opened, no narrower `hold` row should open first

## Overlay Elements

These should remain overlay or deferred metadata only:

- `Elmarit-R I / II`
- `ROM`
- `cam version`
- `1-cam / 2-cam / 3-cam`
- `R-only`
- `Series VIII / E67`
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

- `Elmarit-R I`
- `Elmarit-R II`
- `ROM`
- `cam`
- `R-only`
- `Series VIII / E67`
- hood / cap / case / boxed

Do not use strong shaping aliases:

- `elmarit 180`
- `180 elmarit`
- `r 180 elmarit`

## Final Judgment

Round-1 recommendation:

- immediate `core` candidate: `0`
- recommended first-pass core:
  - none
- strongest deferred candidate:
  - `Leica Elmarit-R 180mm f/2.8`
- explicit `hold` candidate:
  - none

The family is real, but local support is far too thin for conservative seed activation.

The main reasons are:

1. literature clearly confirms a distinct Leica R non-APO `Elmarit-R 180mm f/2.8` family
2. local explicit titles do show the family
3. the usable local pool is effectively one title shape
4. local seller wording does not support `I / II` splitting
5. broad `elmarit 180` shorthand is too exposed to APO / zoom / telephoto contamination

## Recommendation for Next Round

Do not add seed yet.

Revisit only if:

- more clean local title diversity appears
- multiple KRW-priced local rows accumulate beyond the current single priced observation
- explicit non-APO `Elmarit-R 180` wording keeps recurring independently of the current one seller-title pattern
- seller wording starts separating version structure in a stable way
