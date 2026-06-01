# Super-Angulon 21 Hold-Seed Audit - Round 2

Date: 2026-05-01

Scope: round-2 hold-seed audit for `Leica Super-Angulon 21mm f/4`. This round does not add seed rows, does not change classifier/query/search behavior, and does not change admin lookup ranking or UI. The goal is to decide whether the `f/4` line is mature enough for an explicit `hold` row under the already-opened broad `Super-Angulon 21` family.

## Round-1 Summary

Round 1 established:

- immediate `core` for the family:
  - `Leica Super-Angulon 21mm f/3.4`
- `Leica Super-Angulon 21mm f/4` is a literature-real split
- but it was not promoted to round-1 `core`
- finder / hood / bundle stayed below row level
- black / silver stayed overlay

So the narrow round-2 question is not whether `21mm f/4 Super-Angulon` exists.  
It is whether there is enough practical admin-normalization value to justify an explicit `hold` row.

## Candidate Under Review

### A. `Leica Super-Angulon 21mm f/4`

## Literature / Reference Basis

The subtype is real.

Leica Wiki's `21mm f3.4 Super-Angulon` page preserves the serial-history note that the earlier `2.1cm 1:4` `Super-Angulon` line existed before the `f/3.4` line became the dominant M-side product wording.

That means `f/4` is not a seller invention or a metadata quirk. It is a real historical subtype.

## Mechanical / Optical Distinction

### Mechanical distinction

Strong enough to matter.

The split is not merely finish or bundle based. `f/4` is a distinct speed/version axis, which is exactly the kind of thing that can justify a separate canonical row if the local title support is adequate.

### Optical distinction

Real.

`f/4` and `f/3.4` are not the same optical offering under different seller wording. They represent a real internal historical split inside the `Super-Angulon 21` family.

## Search-Intent Separation

### Conceptual search intent

Real.

If a seller writes:

- `M 21/4 Super Angulon`
- `21mm f4 Super-Angulon`

they are expressing a narrower intent than the already-open broad family anchor:

- `Leica Super-Angulon 21mm f/3.4`

### Admin-normalization usefulness

Moderate.

An explicit `hold` row would let admin normalization preserve that earlier slower subtype when the listing itself already names it directly.

## Local Listing Label Availability

Strict M-side filtered local pool in `results_resolved_v2.json`:

- total useful `Super-Angulon 21` listings: `10`
- explicit `f/3.4` titles: `8`
- explicit `f/4` titles: `2`

Representative `f/4` examples:

- `[중고] M 21/4 Super Angulon (Silver)`
- `[중고] M 21/4 Super Angulon (Silver)`

Observed local pricing:

- `f/3.4` median: about `1.60M KRW`
- `f/4` median: about `2.38M KRW`

This is a small sample, so the price difference is not enough for `core`, but it does reinforce that the subtype is not imaginary.

## Broad Row Relationship

Current broad family core:

- `Leica Super-Angulon 21mm f/3.4`

Question:

Does a separate `hold` row create real value, or just taxonomy decoration?

Answer:

It creates real value **if** the title explicitly contains `21/4` or `f/4`.

Why:

- the broad family row remains useful for generic `super angulon 21`
- the narrower `f/4` row would preserve a real earlier subtype only when the listing already gives the exact wording
- this avoids overfitting finder/hood/accessory cues into canonical structure

## Related Axes

### finder / hood / bundle

Still `overlay`.

Reason:

- operationally meaningful
- not a better canonical split axis than the actual optical speed/version split

### black / silver

Still `overlay`.

Reason:

- visible in titles
- but finish is not the right row axis for this round

## Final Recommendation

### Verdict

`explicit hold row 추천`

### Why

`Leica Super-Angulon 21mm f/4` is:

- literature-real
- mechanically and optically meaningful
- explicitly visible in local seller titles
- sparse, but not invisible

That is enough for a cautious explicit `hold` row, even if it is still too early for `core`.

## Recommended Hold Row Shape

If the next round implements it, recommended shape:

- `canonical_name`: `Leica Super-Angulon 21mm f/4`
- `status`: `hold`

Suggested alias direction:

- `super-angulon 21 f4`
- `super angulon 21 f4`
- `21/4 super angulon`
- `21mm f4 super-angulon`
- `m 21/4 super angulon`

Suggested key discriminators:

- `21`
- `f4`
- `super-angulon`
- `super angulon`
- `m 21/4`

## Bottom Line

- `Leica Super-Angulon 21mm f/4` is **not** ready for `core`
- but it **is** ready enough for an explicit `hold` row
- finder / hood / bundle should still stay overlay
- black / silver should still stay below row level

## Can The Next Round Add Hold Seed?

**Yes.**

The next round can safely add:

- `Leica Super-Angulon 21mm f/4` as an explicit `hold` row

It should still avoid:

- finder-only row splits
- hood/bundle rows
- finish-only rows
