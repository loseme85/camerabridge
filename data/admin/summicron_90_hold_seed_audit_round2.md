# Summicron 90 Hold-Seed Audit - Round 2

Date: 2026-04-29

Scope: second audit pass for the Leica `Summicron 90` family, focused not on new `core` additions but on whether the classic internal `E49 / E55` split is mature enough for explicit `hold` rows. This round does not change seed files, search logic, query logic, admin lookup ranking, or UI.

## Round 1 Recap

Round-1 taxonomy audit concluded that `Summicron 90` is seedable, but only conservatively.

Immediate `core` candidates:

1. `Leica Summicron-M 90mm f/2`
2. `Leica APO-Summicron-M 90mm f/2 ASPH`

Round-1 also concluded:

- classic internal `E49 / E55` split is real in literature
- but it is too early for `core`
- `Canada` is better treated as overlay
- APO internal `6bit / titanium / black paint` should stay below first-pass core level

This round asks a narrower operational question:

Can classic `E49` or `E55` move from literature-only structure into explicit `hold` rows?

## Evaluation Criteria

For each candidate:

1. is it a real internal version split in literature?
2. is the mechanical difference strong enough to justify a named hold row?
3. is there meaningful optical / market separation?
4. do users actually search with those terms?
5. do local listing titles expose those terms often enough to support admin normalization?
6. if not `core`, is it still stable enough for explicit `hold`?

## Local Listing Snapshot

Analysis base: `data/derived/results_resolved_v2.json`

Filtered classic non-APO `Summicron-M 90` pool:

- about `31` usable listings

Observed title-level markers:

| Marker | Count | Audit note |
| --- | ---: | --- |
| `Canada` | 4 | visible and repeated |
| `silver` | 8 | finish-level, repeated |
| `black` | 5 | finish-level, repeated |
| `E49` | 0 | no usable classic lens titles |
| `E55` | 0 | no usable classic lens titles |
| `fat` / `thin` | 0 | no usable local labeling |

Representative classic titles:

- `[중고] M 90/2 Summicron (Black)`
- `[중고] M 90/2 Summicron Canada (Silver)`
- `LEICA 90mm F2 SUMMICRON-M sn.3703`

The key signal here is negative:

- there is **no** local classic `Summicron 90` title support for `E49`
- there is **no** local classic `Summicron 90` title support for `E55`

That matters more than literature elegance if we want rows that are actually usable in admin normalization.

## Candidate A: `classic Summicron-M 90mm f/2 E49`

### Official / literature basis

Strong.

Leica Wiki explicitly documents `E49` as the first internal version inside the classic late `Summicron-M 90` line.

### Mechanical distinction

Real.

This is not imaginary collector folklore; it reflects a true internal version difference involving filter thread and barrel / hood behavior.

### Optical distinction

Unclear-to-moderate.

The split is more mechanical / versional than a fully separate user-facing optical family like classic `Summicron 90` versus `APO-Summicron 90`.

### Search-intent split potential

Weak.

Collector-specialist users may understand `E49`, but mainstream dealer and buyer language rarely uses it explicitly.

### Local listing label availability

Insufficient.

Current local classic `Summicron 90` listings show `0` useful `E49` title hits.

That means an admin reviewer would almost never receive a title-level cue strong enough to attach a listing to an `E49` hold row with confidence.

### Explicit hold-row suitability

Not yet.

### Final decision

`keep inside broad classic row`

### One-line reason

`E49` is a real literature split, but current local title language is too weak for an operationally useful explicit `hold` row.

## Candidate B: `classic Summicron-M 90mm f/2 E55`

### Official / literature basis

Strong.

Leica Wiki explicitly documents `E55` as the second internal version inside the same classic late `Summicron-M 90` line.

### Mechanical distinction

Real.

Like `E49`, this is a legitimate internal version marker tied to physical design details, not just finish or country marking.

### Optical distinction

Unclear-to-moderate.

Again, the split is meaningful, but not obviously promoted in the way Leica markets a separate named line.

### Search-intent split potential

Weak.

Advanced users may care, but typical dealer titles do not advertise `E55`.

### Local listing label availability

Insufficient.

Current local classic `Summicron 90` listings show `0` useful `E55` title hits.

### Explicit hold-row suitability

Not yet.

### Final decision

`keep inside broad classic row`

### One-line reason

`E55` is also a real literature split, but current local title support is too weak for a practical explicit `hold` row.

## Canada Overlay Check

### Should `Canada` remain overlay?

`Yes`

Why:

- local classic titles do mention `Canada` repeatedly
- but `Canada` still behaves like production-location / country-marking metadata
- it does not define a clean optical or mechanical canonical line by itself

So `Canada` remains useful:

- as alias support
- as metadata
- as possible future collector note

But not as standalone `hold` or `core`.

## Why APO Internal Variants Stay Lower Priority In This Round

`APO 90` internal signals such as:

- `6bit`
- `titanium`
- `black paint`

may actually have better title visibility than classic `E49 / E55`.

But they are lower priority for this round because:

1. the APO broad row is already explicit and operationally strong
2. APO internal refinements do not block admin normalization of the main APO line
3. the unresolved question we needed to answer now was whether classic `E49 / E55` deserves its own hold rows

So even if APO variants are a future audit target, they are not more urgent than resolving the classic internal split question first.

## Recommendation

### E49 explicit hold row?

`No`

### E55 explicit hold row?

`No`

### Canada overlay?

`Yes`

### Should the next round go to actual classic E49/E55 hold-seed addition?

`Not yet`

## Why The Answer Is "Not Yet"

This is the key distinction:

- literature basis: strong
- title-level operational basis: weak

That is exactly the case where creating explicit `hold` rows makes the taxonomy look more refined on paper than it is in actual admin use.

For now, the correct structure is:

- `Leica Summicron-M 90mm f/2` as the broad classic `core`
- `E49 / E55` preserved conceptually in audit notes, but not materialized as explicit rows
- `Canada` kept as overlay

## Seed-Readiness Verdict For Classic Internal Split

### Can classic `E49 / E55` move to explicit hold rows next round?

`No, not on current evidence`

### What would need to change?

At least one of the following:

1. repeated local listing titles that explicitly say `E49`
2. repeated local listing titles that explicitly say `E55`
3. a stronger admin workflow source that can reliably surface filter-thread / version metadata beyond raw dealer title text

Until then, the safer choice is to leave `E49 / E55` inside the broad classic `Summicron-M 90` row.
