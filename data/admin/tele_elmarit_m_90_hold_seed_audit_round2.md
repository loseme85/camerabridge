# Tele-Elmarit-M 90 Hold-Seed Audit - Round 2

Date: 2026-04-30

Scope: round-2 hold-seed audit for `Leica Tele-Elmarit-M 90mm f/2.8`. This round does not add seed rows, does not change classifier/query/search behavior, and does not change admin lookup ranking or UI. The goal is to decide whether `Tele-Elmarit-M 90` is mature enough for an explicit `hold` row under the already-opened broad `Tele-Elmarit 90` family.

## Round-1 Summary

Round 1 established:

- immediate `core` for the family:
  - `Leica Tele-Elmarit 90mm f/2.8`
- `Tele-Elmarit-M 90mm f/2.8` is a real subtype in literature
- but it was not promoted to round-1 `core`
- `fat / thin` collector naming was kept out because local title support was effectively absent

So the narrow round-2 question is not whether `Tele-Elmarit-M 90` exists.  
It is whether there is enough practical admin-normalization value to justify an explicit `hold` row.

## Candidate Under Review

### A. `Leica Tele-Elmarit-M 90mm f/2.8`

## Literature / Reference Basis

The subtype is real and well documented.

Leica Wiki documents `90mm f/2.8 Tele-Elmarit-M` as:

- a later line than the earlier `Tele-Elmarit`
- production era `1974-1990`
- M-bayonet
- `4 / 4`
- inscription `TELE-ELMARIT-M 1:2.8/90`
- coded / uncoded and Canadian / German variants

By contrast, the earlier broad `Tele-Elmarit 90` line is documented as:

- production era `1964-1974`
- `5 / 3`
- inscription `TELE-ELMARIT 1:2.8/90`

So on literature grounds alone, `Tele-Elmarit-M 90` is clearly a real subtype rather than a cosmetic overlay.

## Mechanical / Optical Distinction

### Mechanical distinction

Strong.

`Tele-Elmarit-M` differs from earlier `Tele-Elmarit` by:

- distinct inscription
- slimmer later form in collector language
- different known production era

### Optical distinction

Strong enough to matter.

The literature split between:

- earlier `Tele-Elmarit` -> `5 / 3`
- later `Tele-Elmarit-M` -> `4 / 4`

is enough to treat the subtype as more than finish or packaging metadata.

## Search-Intent Separation

### Conceptual search intent

Real.

If a user types:

- `tele-elmarit-m 90`
- `tele elmarit m 90`

they are expressing a narrower intent than broad `Tele-Elmarit 90`.

### Admin-normalization usefulness

Moderate.

This subtype is not merely a literature curiosity. It is something an admin could plausibly want to normalize explicitly when the title includes the `-M` wording.

## Local Listing Label Availability

Local filtered `Tele-Elmarit 90` pool in `results_resolved_v2.json`:

- total useful `Tele-Elmarit` listings: `17`
- explicit `Tele-Elmarit-M` titles: `3`

Representative `Tele-Elmarit-M` examples:

- `LEICA 90mm F2.8 TELE-ELMARIT-M sn.1180`
- `LEICA 90mm F2.8 TELE-ELMARIT-M sn.3429`
- `Leica 90mm F2.8 Tele Elmarit M Black`

This is still sparse, but importantly it is **not zero**.

That makes this case stronger than:

- classic `Summicron 90 E49 / E55` where local title signal was effectively absent
- collector `fat / thin` naming where local title signal was also absent

## Broad Row Relationship

Current broad family core:

- `Leica Tele-Elmarit 90mm f/2.8`

Question:

Does a separate `hold` row create real value, or just taxonomy decoration?

Answer:

It creates real value **if** the title explicitly contains `Tele-Elmarit-M`.

Why:

- the broad family row remains useful for generic `tele elmarit 90`
- the narrower `-M` row would let admin normalization preserve a meaningful later subtype when the seller already provides the exact wording
- this does not require promoting `fat / thin` into public seed naming

## Related Axes

### `fat / thin`

Still `보류`.

Reason:

- collector language is real
- local title support remains effectively `0`
- no reason to use it as a seed naming axis yet

### `country marking`

Still `overlay`.

Reason:

- literature-real
- not strong enough as a standalone hold entity

### `coding`

Still `overlay` or low-priority `hold`, not a row.

Reason:

- title signal may appear
- but it is not a better first hold candidate than the actual `Tele-Elmarit-M` subtype name

### `finish`

Still `overlay`.

Reason:

- black / silver is not the right split axis for this round

## Final Recommendation

### Verdict

`explicit hold row 추천`

### Why

`Tele-Elmarit-M 90mm f/2.8` is:

- literature-real
- mechanically and optically meaningful
- title-addressable in local listings
- sparse, but not invisible

That is enough for a cautious explicit `hold` row, even if it is still too early for `core`.

## Recommended Hold Row Shape

If the next round implements it, recommended shape:

- `canonical_name`: `Leica Tele-Elmarit-M 90mm f/2.8`
- `status`: `hold`

Suggested alias direction:

- `tele-elmarit-m 90`
- `tele elmarit m 90`
- `90 tele-elmarit-m`
- `90mm f2.8 tele-elmarit-m`

Suggested key discriminators:

- `90`
- `f2.8`
- `tele-elmarit-m`
- `tele elmarit m`

## Bottom Line

- `Tele-Elmarit-M 90mm f/2.8` is **not** ready for `core`
- but it **is** ready enough for an explicit `hold` row
- `fat / thin` should still stay deferred
- `country / coding / finish` should still stay below row level

## Can The Next Round Add Hold Seed?

**Yes.**

The next round can safely add:

- `Leica Tele-Elmarit-M 90mm f/2.8` as an explicit `hold` row

It should still avoid:

- `fat tele`
- `thin tele`
- country-only rows
- coding-only rows
- finish-only rows
