# Summicron 24 Taxonomy Audit - Round 1

Date: 2026-05-11

Scope: read-heavy taxonomy audit for the Leica `Summicron 24` family hypothesis. This round does not add seed rows, does not change classifier/query/search behavior, and does not change admin lookup ranking or UI. The goal is to determine whether `Leica Summicron-M 24mm f/2 ASPH` is a real, seedable Leica M product line or whether the apparent family should be closed as non-existent / unsupported.

## Executive Summary

`Summicron 24` should **not** be seeded.

Round-1 conclusion:

- immediate recommended `core` candidate count: `0`
- recommended first-pass core:
  - none
- explicit `hold` candidate:
  - none
- round-1 recommendation:
  - `seed 보류`
  - close the hypothesized `Summicron 24` family for now

Why this closes rather than defers as a weak real family:

1. the Leica literature stack does **not** show a `Summicron-M 24mm f/2 ASPH` line
2. Leica-wide-angle 24mm M literature consistently shows:
   - `Summilux-M 24mm f/1.4 ASPH`
   - `Elmarit-M 24mm f/2.8 ASPH`
   - `Elmar-M 24mm f/3.8 ASPH`
3. the local title pool contains **no clean `24mm Summicron` listings**
4. broad `summicron 24` retrieval is just contamination from:
   - `24` inside body names like `M240`
   - other focal lengths such as `35 / 50 / 90 Summicron`

This is not a case of “real family but weak pool.”  
It is closer to “no evidence that this Leica M family exists in the first place.”

## Family Hypothesis

The hypothesis tested in this round was:

- `Leica Summicron-M 24mm f/2 ASPH`

and related seller wording such as:

- `summicron 24`
- `24 summicron`
- `summicron-m 24`
- `24mm f2 summicron`
- `m 24/2 summicron`
- `24 cron`

Round-1 answer: this should not be opened as a canonical family.

## Literature / Reference Base

### Source A: Leica Wiki - M lenses by focal length

Leica Wiki's `M Lenses x Focal Length` page shows the modern Leica M wide-angle structure around `24mm` as:

- `24mm f/1.4 ASPH Summilux-M`
- `24mm f/2.8 ASPH Elmarit-M`
- `24mm f/3.8 ASPH Elmar-M`

Notably, it does **not** list any `24mm f/2 Summicron-M`.

Reference:

- [Leica Wiki - M Lenses x Focal Length](https://wiki.l-camera-forum.com/leica-wiki.en/index.php/M_Lenses_x_Focal_Length)

### Source B: Leica Wiki - M lenses by type

Leica Wiki's `M Lenses x Type` page shows the same pattern in the wide-angle section:

- `18mm f/3.8 ASPH Super-Elmar-M`
- `21mm f/1.4 ASPH Summilux-M`
- `21mm f/2.8 ASPH Elmarit-M`
- `21mm f/3.4 ASPH Super-Elmar-M`
- `24mm f/1.4 ASPH Summilux-M`
- `24mm f/2.8 ASPH Elmarit-M`
- `24mm f/3.8 ASPH Elmar-M`

Again, no `24mm f/2 Summicron-M` appears.

Reference:

- [Leica Wiki - M Lenses x Type](https://wiki.l-camera-forum.com/leica-wiki.en/index.php/M_Lenses_x_Type)

### Source C: Leica Wiki - M lenses by maximum aperture

Leica Wiki's `M Lenses x Maximum Aperture` page shows:

- `24mm f/1.4 ASPH Summilux-M`

and then `Summicron-M` entries begin at other focal lengths such as `28mm`, `35mm`, `50mm`, and `90mm`.

There is no `24mm f/2 Summicron-M`.

Reference:

- [Leica Wiki - M Lenses x Maximum Aperture](https://wiki.l-camera-forum.com/leica-wiki.en/index.php/M_Lenses_x_Maximum_Aperture)

### Source D: Leica official ecosystem check

Direct Leica official search did not surface a `Summicron-M 24 f/2 ASPH` product page.  
Related Leica accessory pages for `24mm` M lenses list:

- `Elmar-M 24 mm f/3.8 ASPH.`

but do not show a `Summicron-M 24`.

Reference:

- [Leica Camera - Lens front cap M E46](https://leica-camera.com/en-US/photography/accessories/caps/lens-front-cap-m-e46/shop-now)

### Interpretation

The literature stack argues against the family hypothesis:

1. the actual Leica M `24mm` family set is already occupied by `Summilux`, `Elmarit`, and `Elmar-M`
2. no supporting Leica or Leica Wiki line was found for `Summicron-M 24mm f/2 ASPH`
3. round-1 should treat `Summicron 24` as a non-family hypothesis, not as a weak family awaiting more data

## Local Listing Evidence

Analysis base: `data/normalized/normalized_latest.json`

### Broad retrieval

A naive broad retrieval on `summicron + 24` produced:

- raw pool: `13`

But the contents are pure contamination, including:

- `M240 Ara Guler Edition + M 35/2 Summicron ASPH 6bit (Black Paint)`
- `LEICA 90mm F2 ASPH APO-SUMMICRON-M ...`
- `LEICA 35mm F2 ... SUMMICRON ...`
- `LEICA 50mm F2 SUMMICRON ...`

### Clean pool after contamination filtering

After excluding:

- non-24 focal lengths
- body-model contamination like `M240`
- non-M or non-target Summicron listings
- false matches driven by raw token overlap

the useful local `Summicron 24` pool becomes:

- clean local pool: `0`
- unique title strings: `0`
- KRW-priced: `0`

### Smoke query behavior

Expected target-like queries:

- `24mm f2 summicron`
- `24mm f/2 summicron`
- `24mm f2 asph summicron`
- `24mm f/2 asph summicron`

all returned:

- `0` direct local title hits

Broader shorthand queries such as:

- `summicron 24`
- `24 summicron`
- `summicron-m 24`
- `m 24/2 summicron`
- `24 cron`

only matched token contamination and produced no valid family evidence.

### Interpretation

This is the decisive local result:

1. there is no clean local title support
2. there is no priced subset
3. all broad retrieval comes from contamination, not from a real `24mm Summicron-M` market line

## Contamination Review

### 24mm Leica M boundary

The real Leica M `24mm` families are:

- `Elmarit 24`
- `Elmar-M 24`
- `Summilux 24`

These remain separate and already account for the actual `24mm` Leica M lens space.

### 18mm / 21mm boundary

These must remain outside any hypothetical `Summicron 24` family:

- `Super-Elmar 18`
- `Elmarit 21`
- `Super-Elmar 21`
- `Super-Angulon 21`
- `Summilux 21`
- `Tri-Elmar 16-18-21` / `WATE`

### R / SL / third-party boundary

These must also remain outside:

- `Elmarit-R 24`
- `APO-Summicron-SL 24`
- `Voigtlander 24`
- `Zeiss 24`
- other third-party `24mm` lenses

### Accessory contamination

Accessory-only queries such as:

- `finder summicron 24`
- `hood summicron 24`
- `cap summicron 24`

do not rescue the family hypothesis. They remain accessory-side noise around a nonexistent family.

## Core / Hold / Overlay / Deferred / Boundary

### Core candidate

None.

### Hold candidate

None.

### Overlay

Not applicable as a seeded family, because the family itself is unsupported.

If the family were real, the following would remain below row level:

- `6bit`
- `black / silver`
- `country marking`
- `finder included`
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

### Deferred / 보류

- `24 cron`
- `summicron 24`
- `24 summicron`
- `m 24/2 summicron`

These are not row candidates; they are shorthand patterns that currently only produce contamination.

### Out-of-family boundary

- `Elmarit 24`
- `Elmar-M 24`
- `Summilux 24`
- `Super-Elmar 18`
- `Elmarit 21`
- `Super-Elmar 21`
- `Super-Angulon 21`
- `Summilux 21`
- `Tri-Elmar 16-18-21` / `WATE`
- `R mount`
- `SL / L mount`
- accessory-only listings
- third-party `24mm` lenses

## Final Recommendation

### immediate core candidate

`0`

### hold candidate

None.

### overlay

No overlay recommendation is needed because no family should be seeded.

### out-of-family

- real Leica `24mm` M families: `Elmarit 24`, `Elmar-M 24`, `Summilux 24`
- Leica `18mm / 21mm` M families
- `Tri-Elmar` / `WATE`
- `R`
- `SL`
- accessories
- third-party lenses

### next-round seedability

No.

Round-1 recommendation is:

- `seed 보류`
- keep `Summicron 24` closed

If new evidence ever appears, the threshold to revisit should be:

1. a literature-backed Leica source showing a real `24mm Summicron-M` line, or
2. multiple clean local `24mm f/2 Summicron` titles that are clearly not contamination

At present, neither condition is met.
