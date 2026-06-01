# Elmar-C 90 Hold-Seed Audit - Round 2

Date: 2026-05-08

Scope: narrow hold-seed audit for `Leica Elmar-C 90mm f/4`. This round does not add seed rows, does not change classifier/query/search behavior, and does not change admin lookup ranking or UI. The goal is to decide whether `Elmar-C 90` is mature enough for an explicit `hold` row under the still-unseeded broader `Elmar 90` family.

## Executive Summary

`Leica Elmar-C 90mm f/4` is safe enough for an explicit `hold` row.

Round-2 conclusion:

- add hold row: `yes`
- recommended hold canonical name:
  - `Leica Elmar-C 90mm f/4`
- broad `Elmar 90` core: `no / defer`
- generic `elmar 90` query:
  - seed hard-pin: `forbid`

This is the right shape because:

1. `Elmar-C 90` is literature-real
2. local titles that mention it are subtype-explicit
3. generic `Elmar 90` is still mixed across classic `Elmar`, `Elmar-C`, `Elmar III`, and contamination from `Macro-Elmar-M`

So `Elmar-C 90` is exactly the kind of subtype that is too narrow for round-1 `core`, but strong enough for explicit `hold`.

## Round-1 Recap

Round-1 conclusion for `Elmar 90`:

- immediate `core` candidates: `0`
- broad `Elmar 90` seed: `defer`
- strongest future `hold` candidate:
  - `Leica Elmar-C 90mm f/4`
- secondary future candidate:
  - `Elmar (III) 1:4 / 90mm`
- `Leica Elmar-M 90mm f/4` was judged not to be a clean independent Leica line

The round-2 question is therefore very narrow:

Can `Elmar-C 90` stand as an explicit `hold` row without polluting broad `Elmar 90` intent?

## Literature Recheck

### Source A: Leica Wiki - `90mm f/4 Elmar-C`

Leica Wiki documents:

- `90mm f/4 Elmar-C`

with:

- production era `1973-1977`
- Leica M-bayonet
- `4 / 4` optical construction
- CL-era identity
- inscription `ELMAR-C 1:4/90`

Reference:

- [Leica Wiki - 90mm f/4 Elmar-C](https://wiki.l-camera-forum.com/leica-wiki.en/index.php/90mm_f/4_Elmar-C)

### Source B: contrast case - classic `90mm f/4 Elmar`

Leica Wiki documents classic `90mm f/4 Elmar` separately as:

- production era `1954-1968`
- screw-mount and M-bayonet
- `4 / 3`
- collapsible and rigid variants

Reference:

- [Leica Wiki - 90mm f/4 Elmar](https://wiki.l-camera-forum.com/leica-wiki.en/index.php/90mm_f/4_Elmar)

### Source C: contamination boundary - `Macro-Elmar-M 90 f/4`

Leica’s current product pages describe `Macro-Elmar-M 90 f/4` as a distinct modern M lens line, not as part of classic `Elmar 90`.

Reference:

- [Leica Camera - Macro-Elmar-M 90 f/4](https://leica-camera.com/en-US/photography/lenses/m/macro-elmar-m-90mm-f4-black)

### Interpretation

The literature position is strong and uncomplicated:

1. `Elmar-C 90` is a real named Leica line
2. it is not just a cosmetic or finish variant of classic `Elmar 90`
3. it is also not `Macro-Elmar-M 90`

That clears the first and most important hurdle for a `hold` row.

## Local Title Evidence

Analysis base: `data/normalized/normalized_latest.json`

After excluding obvious contamination from:

- `Macro-Elmar-M`
- `Elmarit 90`
- `Tele-Elmarit 90`
- `Summicron 90`
- `APO-Summicron 90`
- `Thambar 90`
- `R` 90 families
- accessories and third-party 90mm listings

the broad useful `Elmar 90` pool remains small and mixed.

### Explicit `Elmar-C` sample

Observed explicit `Elmar-C` titles:

- `LEICA 90mm F4 ELMAR-C sn.2573`
- `Leica 90mm F4 C Elmar`

Explicit `Elmar-C` bucket:

- count `2`
- priced `0`

This is sparse, but the important thing is that the subtype wording is direct and stable.

### Generic `Elmar 90` examples

Generic / mixed examples still include:

- `Leica L 90mm f4 Elmar Silver`
- `LEICA 90mm F4 Elmar sn.6465`
- `LEICA 90mm F4 ELMAR sn.1913`
- `LEICA 90mm F4 Elmar 3-element sn.2089`
- `LEICA M4 90mm F4 Elmar sn.1211 /sn.1261`

That confirms the round-1 concern:

- generic `elmar 90`
- `90 elmar`
- `90mm f4 elmar`

are still too broad to assign to `Elmar-C`.

## Search-Intent Separation

### Explicit `Elmar-C` intent

The following forms are subtype-explicit and operationally useful:

- `elmar-c 90`
- `90 elmar-c`
- `90mm f4 elmar-c`
- `90mm f/4 elmar-c`
- `90mm f4 c elmar`
- `c elmar 90`
- `cl elmar 90`

These are not generic `Elmar 90` searches. They are narrow enough to indicate CL-era `Elmar-C` intent.

### Generic `Elmar 90` intent

The following must remain unresolved:

- `elmar 90`
- `90 elmar`
- `90mm f4 elmar`
- `90mm f/4 elmar`

These generic queries can still refer to:

- classic `90mm f/4 Elmar`
- `Elmar-C`
- `Elmar (III)`
- screw-thread / `L`

So broad `Elmar 90` intent should not be pinned to the `Elmar-C` hold row.

## Canonical Naming Review

### Recommended canonical name

- `Leica Elmar-C 90mm f/4`

This remains the safest canonical name because:

1. it matches literature usage
2. it matches local subtype-explicit listing wording
3. it avoids overfitting to dealer shorthand

### Alias safety

Safe aliases:

- `elmar-c 90`
- `90 elmar-c`
- `90mm f4 elmar-c`
- `90mm f/4 elmar-c`
- `90mm f4 c elmar`
- `c elmar 90`
- `cl elmar 90`

These preserve explicit intent while keeping generic `Elmar 90` out of the hold row.

## Overlay Review

Keep these as `overlay`, not separate rows:

- `black / chrome / silver`
- `country marking`
- `hood included`
- `cap included`
- `filter included`
- `boxed`
- `condition`
- `original cap / hood / box`
- `packaging`
- `adapter / pouch` inclusion

## Boundary Review

The following must remain out-of-family boundaries:

- `macro-elmar-m 90`
- `macro elmar 90`
- `elmar-m 90`
- `elmar iii 90`
- `3-element elmar 90`
- `ltm elmar 90`
- `l 90/4 elmar`
- `elmarit 90`
- `tele-elmarit 90`
- `summicron 90`
- `apo summicron 90`
- `thambar 90`
- `elmarit-r 90`
- `summicron-r 90`
- `voigtlander 90`
- `zeiss 90`
- `hood 90 elmar`
- `filter 90 elmar`
- `adapter elmar 90`

Special note:

- `Macro-Elmar-M 90` is the most important contamination boundary here
- `Leica Elmar-M 90mm f/4` should not be introduced as a separate canonical row

## Final Recommendation

### Add hold row

- `yes`

### Recommended hold canonical name

- `Leica Elmar-C 90mm f/4`

### Broad core

- `no / defer`

### Generic query

- seed hard-pin: `forbid`

### Next step

- future hold row addition: `allowed`

The next safe seed round would be a very narrow one that adds exactly:

1. `Leica Elmar-C 90mm f/4` as `hold`

while continuing to keep:

- broad `Elmar 90`
- `Elmar (III)`
- `LTM` / classic `Elmar 90`

below row level.
