# APO-Elmarit-R 180 Taxonomy Audit - Round 1

Date: 2026-05-14

Scope: audit-only review for the Leica `APO-Elmarit-R 180` family. This round does not add seed rows, does not modify `entities/*.json`, does not modify `canonical_entities_index.json`, and does not change classifier/query/search behavior, ranking, or UI.

## Executive Summary

`APO-Elmarit-R 180` is literature-real, but round-1 local support is still too thin and too concentrated to justify immediate seed activation.

Round-1 conclusion:

- immediate recommended `core` candidate count: `0`
- recommended first-pass core:
  - none
- strongest deferred candidate:
  - `Leica APO-Elmarit-R 180mm f/2.8`
- explicit `hold` candidate:
  - none
- literature clearly supports a real Leica R `180mm f/2.8 APO-Elmarit-R` family
- literature also supports real internal marker structure:
  - `APO-Elmarit-R I`
  - `APO-Elmarit-R II`
  - `ROM`
  - `Series VIII`
  - `E67`
  - built-in hood / tripod collar on later line
- but local title support is still concentrated in only three repeated title shapes, and seller wording does not distinguish `I / II`

The safest round-1 answer is:

1. keep `APO-Elmarit-R 180` closed for now
2. do not open any `core` or `hold` row
3. keep `APO-Telyt-R 180`, non-APO `Elmarit-R 180`, classic `Elmar-R 180`, `Vario-APO-Elmarit-R 70-180`, `APO-Summicron-R 180`, `APO-Telyt-R 280`, SL/L telephoto, and third-party telephoto lines as hard boundaries

## Literature / Reference Base

### Source A: Leica Wiki - `180mm f/2.8 APO-Elmarit-R I`

Leica Wiki documents `180mm f/2.8 APO-Elmarit-R I` with:

- order no.:
  - `11273`
- production era:
  - `1998-2004`
- variants:
  - `1-cam`
  - `2-cam`
  - `3-cam`
  - `ELC`
  - `ELW`
- filter type:
  - `Series VIII`
- accessories:
  - `Leica APO-EXTENDER-R 2x`

Reference:

- [Leica Wiki - 180mm f/2.8 APO-Elmarit-R I](https://wiki.l-camera-forum.com/leica-wiki.en/index.php?title=180mm_f%2F2.8_APO-Elmarit-R_I)

### Source B: Leica Wiki - `180mm f/2.8 APO-Elmarit-R II`

Leica Wiki documents `180mm f/2.8 APO-Elmarit-R II` with:

- order no.:
  - `11357`
- production era:
  - `2004-2009`
- filter type:
  - `E67`
- accessories:
  - `APO-EXTENDER-R 1.4x`
  - `APO-EXTENDER-R 2x`
  - rotating tripod collar `STA-1 14636`
- built-in telescopic rubber-armored hood
- inscription:
  - `APO-ELMARIT-R 1:2.8/180`

Reference:

- [Leica Wiki - 180mm f/2.8 APO-Elmarit-R II](https://wiki.l-camera-forum.com/leica-wiki.en/index.php/180mm_f/2.8_APO-Elmarit-R_II)

### Source C: Leica Wiki - `180mm f/2.8 Elmarit-R II`

For non-APO boundary, Leica Wiki separately documents:

- `180mm f/2.8 Elmarit-R II`

with:

- production era:
  - `1979-1998`
- variants:
  - `3-cam`
  - `R-only`
- filter type:
  - `E67`
- the page explicitly mixes separate serial ranges for the Apo version and non-Apo parent line, reinforcing that the APO line must be handled carefully and separately

Reference:

- [Leica Wiki - 180mm f/2.8 Elmarit-R II](https://wiki.l-camera-forum.com/leica-wiki.en/index.php/180mm_f/2.8_Elmarit-R_II)

### Source D: Leica Wiki - `180mm f/3.4 APO-Telyt-R`

For adjacent APO telephoto boundary, Leica Wiki documents:

- `180mm f/3.4 APO-Telyt-R`

as a distinct line with:

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

For zoom boundary, Leica Wiki separately documents:

- `70mm–180mm f/2.8 Vario-APO-Elmarit-R`

Reference:

- [Leica Wiki - 70mm-180mm f/2.8 Vario-APO-Elmarit-R](https://wiki.l-camera-forum.com/leica-wiki.en/index.php?title=70mm%E2%80%93180mm_f%2F2.8_Vario-APO-Elmarit-R)

### Source F: Leica Wiki - `180mm f/2 APO-Summicron-R`

For another neighboring fast APO telephoto boundary:

- `180mm f/2 APO-Summicron-R`

Reference:

- [Leica Wiki - 180mm f/2 APO-Summicron-R](https://wiki.l-camera-forum.com/leica-wiki.en/index.php/180mm_f/2_APO-Summicron-R)

## Taxonomy Implication from Literature

Literature clearly supports:

- one real broad family:
  - `Leica APO-Elmarit-R 180mm f/2.8`

Literature also supports real internal structure:

- `APO-Elmarit-R I`
- `APO-Elmarit-R II`
- `ROM`
- `Series VIII`
- `E67`
- built-in hood / tripod collar

However, literature alone does not justify row splitting in round 1.

The deciding round-1 question is not whether `I / II` exist. They do. The question is whether local seller titles reliably surface that split. In the current raw pool, they do not.

## Boundary Check

This family must remain separate from:

- `Leica APO-Telyt-R 180mm f/3.4`
- non-APO `Leica Elmarit-R 180mm f/2.8`
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

Broad `180 apo` retrieval is dangerous.

When the local raw pool is widened to `180` plus `apo` / `elmarit`, distinct non-family lines appear:

- `Leica R 70-180mm f2.8 Vario-Apo-Elmarit Black`
- `Leica R 180mm f3.4 APO-Telyt Black`
- `Leica R 180mm f2 APO-Summicron Black [영상용 개조]`
- `[위탁] R 180/2.8 Elmarit (Black)`
- `LEICA 180mm F2.8 ROM APO-MACRO-ELMARIT-R sn.3840`
- `LEICA 70-180mm F2.8 VARIO-APO-ELMARIT-R sn.3697`
- `Angenieux R 180mm f2 3 APO DEM F Black`

Interpretation:

- broad `apo elmarit 180`
- broad `180 apo`
- broad `apo 180`

are not safe shaping aliases in round 1 because the wider `180mm` Leica telephoto field is crowded with adjacent APO, non-APO, macro, zoom, and third-party lines.

### Clean local R-side pool

After restricting to explicit `180mm`, explicit R-side `APO-Elmarit-R` wording, and excluding `APO-Telyt-R 180`, non-APO `Elmarit-R 180`, classic `Elmar-R 180`, `Vario-APO-Elmarit-R 70-180`, `APO-Summicron-R 180`, `APO-Telyt-R 280`, M-side `APO-Telyt-M 135`, SL/L, third-party, and accessory contamination, the usable pool becomes:

- clean local pool: `3`
- unique titles: `3`
- KRW-priced count: `2`
- KRW median: `2950000`

Representative clean titles:

- `[위탁] R 180/2.8 APO Elmarit ROM (Black)`
- `[중고] R 180/2.8 APO Elmarit ROM (Black)`
- `LEICA 180mm F2.8 APO-ELMARIT-R sn.3897`

Interpretation:

- this confirms the family is real in local data
- but seller wording is still narrow and concentrated
- the pool is still only three title shapes
- the two priced rows are useful but not enough to show a stable local family price band

### Marker distribution inside local pool

Round-1 local support is strong only for broad family + ROM wording:

- `ROM`: present in repeated local titles
- `Black`: present in repeated local titles

Round-1 local support is absent for:

- `cam`
- `Series VIII`
- `E67`
- built-in hood
- tripod collar
- boxed / case wording
- explicit `I / II` markers

Interpretation:

- `ROM` is real and repeated, but still behaves like metadata rather than a stable row split
- `I / II` exist in literature, but local seller titles do not separate them
- therefore `I / II`, `ROM`, `Series VIII / E67`, hood, and tripod collar all remain overlay or deferred in round 1

## Smoke Query Review

### Explicit R-side queries

Usable but still modest evidence appears in explicit product wording:

- `apo-elmarit-r 180`
- `apo elmarit r 180`
- `180mm f2.8 apo-elmarit-r`
- `r 180/2.8 apo elmarit`
- `leica r 180mm f2.8 apo`

The same three title shapes recur:

- `[위탁] R 180/2.8 APO Elmarit ROM (Black)`
- `[중고] R 180/2.8 APO Elmarit ROM (Black)`
- `LEICA 180mm F2.8 APO-ELMARIT-R sn.3897`

Interpretation:

- explicit R-side wording can find real family evidence
- but repetition is still too narrow for conservative seed activation

### Broad shorthand risk

Unsafe broad shorthand:

- `apo elmarit 180`
- `180 apo`
- `apo 180`

Why unsafe:

- overlaps with `Vario-APO-Elmarit-R 70-180`
- drifts into `APO-Macro-Elmarit-R 100`
- drifts into `APO-Telyt-R 180`
- drifts into `APO-Summicron-R 180`
- reaches non-Leica `180mm` telephoto listings

## Candidate Review

## Candidate 1: `Leica APO-Elmarit-R 180mm f/2.8`

Pros:

- literature-real Leica R family
- literature supports meaningful internal structure and long production run
- local titles do confirm explicit R-side family presence
- there is at least some KRW-priced local support

Cons:

- clean local pool is only `3`
- unique titles are only `3`
- local evidence is concentrated in three repeated title shapes
- seller wording does not separate `I / II`
- broad shorthand is highly exposed to adjacent Leica `180mm` contamination

Round-1 judgment:

- not ready for immediate `core`
- should remain the strongest deferred candidate

## Hold Candidate Review

No explicit `hold` candidate is recommended in round 1.

Reason:

- `I / II` are literature-real but not locally title-stable
- `ROM` is repeated but still acts like metadata, not a distinct explicit row
- if the main family itself is not yet opened, no narrower `hold` row should open first

## Overlay Elements

These should remain overlay or deferred metadata only:

- `ROM`
- `cam version`
- `1-cam / 2-cam / 3-cam`
- `Series VIII / E67`
- `filter thread`
- built-in hood
- tripod collar
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

- `APO-Elmarit-R I`
- `APO-Elmarit-R II`
- `ROM`
- `Series VIII / E67`
- built-in hood
- tripod collar

Do not use strong shaping aliases:

- `apo elmarit 180`
- `180 apo`
- `apo 180`

## Final Judgment

Round-1 recommendation:

- immediate `core` candidate: `0`
- recommended first-pass core:
  - none
- strongest deferred candidate:
  - `Leica APO-Elmarit-R 180mm f/2.8`
- explicit `hold` candidate:
  - none

The family is real, but local support is still too thin for conservative seed activation.

The main reasons are:

1. literature clearly confirms a distinct Leica R `APO-Elmarit-R 180mm f/2.8` family
2. local explicit titles do show the family
3. the local pool is still only three repeated title shapes
4. local seller wording does not support `I / II` splitting
5. broad `apo elmarit 180` / `180 apo` / `apo 180` are too exposed to adjacent Leica `180mm` contamination

## Recommendation for Next Round

Do not add seed yet.

Revisit only if:

- more clean local title diversity appears
- multiple KRW-priced local rows accumulate beyond the current narrow cluster
- explicit `APO-Elmarit-R 180` wording keeps recurring independently of the current three repeated title shapes
- seller wording starts separating version structure in a stable way
