# APO-Summicron 90 Hold-Seed Audit - Round 2

Date: 2026-04-29

Scope: second audit pass for the Leica `APO-Summicron-M 90mm f/2 ASPH` line, focused not on changing the existing broad `core` row but on whether internal variants are strong enough for explicit `hold` rows. This round does not change seed files, search logic, query logic, admin lookup ranking, or UI.

## Round 1 Recap

Round-1 taxonomy audit concluded that `Summicron 90` is seedable with two conservative cores:

1. `Leica Summicron-M 90mm f/2`
2. `Leica APO-Summicron-M 90mm f/2 ASPH`

Round-1 also concluded that APO-internal signals such as:

- `6bit`
- `titanium`
- `black paint`

are real, but should remain below first-pass core level.

This round asks a narrower question:

Can any of those move from broad-row metadata into explicit `hold` rows?

## Evaluation Criteria

For each candidate:

1. is it a real literature / catalog variant?
2. is the distinction mechanical / market-significant enough to deserve its own hold row?
3. is it optical, or mainly finish / coding metadata?
4. do users and dealers actually search with the variant term?
5. do local listings expose that term often enough to support operational admin normalization?
6. if not `core`, is it still stable enough for explicit `hold`?

## Local Listing Snapshot

Analysis base: `data/derived/results_resolved_v2.json`

Filtered APO `Summicron 90` pool:

- about `39` usable listings

Observed title-level markers:

| Marker | Count | Audit note |
| --- | ---: | --- |
| `6bit` | 13 | repeated and operationally visible |
| `titanium` | 1 | real but very sparse |
| `black paint` | 0 | literature-real, local title support absent |
| `silver` | 0 | broad APO pool does not expose it as a repeat local title signal |
| `black` | 16 | generic finish wording, not a distinct entity signal |

Representative APO titles:

- `[중고] APO M 90/2 Summicron ASPH 6bit (Black)`
- `LEICA 90mm F2 ASPH (6bit) APO-SUMMICRON-M sn.4208`
- `LEICA 90mm F2 ASPH APO-SUMMICRON-M TITANIUM sn.3926`
- `Leica APO Summicron M 2/90mm ASPH.(6bit)`

KRW price comparison:

| Bucket | Count | KRW-priced | Median KRW | Audit note |
| --- | ---: | ---: | ---: | --- |
| `6bit` titles | 13 | 7 | ~3.38M KRW | repeated but overlaps broad APO line |
| non-`6bit` APO titles | 26 | 14 | ~3.79M KRW | overlapping market cluster |

Interpretation:

- `6bit` is genuinely visible in local titles
- but it does **not** create a clean separate market cluster
- `titanium` and `black paint` have much weaker title support

## Candidate A: `APO-Summicron-M 90mm f/2 ASPH 6bit`

### Official / literature basis

Moderate.

`6bit` coding is real Leica metadata and appears repeatedly in local listings. But it is not presented by Leica as a separate named product line the way `APO-Summicron-M 90` itself is.

### Mechanical distinction

Weak-to-moderate.

Coding matters for camera communication and can correlate with production era, but it does not define a separate optical family.

### Optical distinction

Weak.

The lens remains the same APO-Summicron-M 90 optical line.

### Search-intent split potential

Moderate.

Buyers and dealers do sometimes care about coded versus uncoded M lenses, and the local dataset shows repeated `6bit` wording.

### Local listing label availability

Strong enough to be visible, but not enough to force a separate canonical row.

This is the best-supported candidate in the round:

- `13` local title hits
- clear operational visibility

But title repetition alone is not enough if the variant is still better understood as metadata than as a named entity.

### Explicit hold-row suitability

`Not recommended yet`

### Final decision

`keep inside broad APO row`

### One-line reason

`6bit` is the strongest APO internal signal, but it still behaves more like repeated coding metadata than a separate canonical hold entity.

## Candidate B: `APO-Summicron-M 90mm f/2 ASPH titanium`

### Official / literature basis

Strong.

Leica Wiki explicitly lists order number `11632` titanium and shows it as a real factory variant.

### Mechanical distinction

Weak-to-moderate.

This is a real factory finish/material edition, but not a separate optical design.

### Optical distinction

None.

### Search-intent split potential

Moderate among collectors, weak in the general market.

### Local listing label availability

Too weak today.

Current local evidence is effectively one explicit title:

- `LEICA 90mm F2 ASPH APO-SUMMICRON-M TITANIUM sn.3926`

That is enough to prove existence, but not enough to justify a broadly useful hold row.

### Explicit hold-row suitability

`Not recommended yet`

### Final decision

`keep inside broad APO row`

### One-line reason

`titanium` is a real factory variant, but current local title support is too sparse for a practical explicit `hold` row.

## Candidate C: `APO-Summicron-M 90mm f/2 ASPH black paint`

### Official / literature basis

Strong.

Leica Wiki explicitly lists order number `11636` black paint.

### Mechanical distinction

Weak.

This is a finish / edition distinction, not a separate optical line.

### Optical distinction

None.

### Search-intent split potential

Collector-moderate, general-market weak.

### Local listing label availability

Insufficient.

Current local APO 90 titles show effectively `0` useful `black paint` hits.

### Explicit hold-row suitability

`Not recommended`

### Final decision

`keep inside broad APO row`

### One-line reason

`black paint` is literature-real but currently invisible in local APO 90 title language, so an explicit hold row would be decorative rather than useful.

## Finish Overlay Check

### Should `silver` and generic finish wording remain overlay?

`Yes`

Why:

- finish differences are real
- but they are not separate optical families
- local APO 90 titles do not expose silver consistently enough to justify its own row
- generic `black` wording is common and too broad to become a canonical split

So for now:

- `silver` stays overlay
- `black` stays overlay
- finish metadata remains below explicit hold-row level

## Why APO Variants Are More Visible Than Classic E49 / E55, But Still Not Hold-Ready

Compared with classic `E49 / E55`, APO internal variants have one clear advantage:

- local title language exposes them more directly, especially `6bit`

But they still fail the stricter canonical test because:

1. `6bit` is mostly coding metadata, not a named Leica line
2. `titanium` and `black paint` are too sparse locally
3. none of the three create a clearly separate market cluster comparable to broad classic versus broad APO

So APO internal variants are closer to hold-readiness than classic `E49 / E55`, but not across the line.

## Recommendation

### `6bit` explicit hold row?

`No`

### `titanium` explicit hold row?

`No`

### `black paint` explicit hold row?

`No`

### `silver` / general finish overlay?

`Yes`

### Should the next round go to actual APO-variant hold-seed addition?

`Not yet`

## Why The Answer Is "Not Yet"

This round produced a mixed result:

- title visibility: moderate for `6bit`, weak for the others
- literature reality: strong for `titanium` and `black paint`
- canonical usefulness: still weak across all three

That means the APO broad row is doing its job:

- it captures the real product line
- it absorbs secondary variation without forcing premature sub-rows

For now, that is the safer and more operationally honest structure.

## Seed-Readiness Verdict For APO Internal Variants

### Can APO internal `6bit / titanium / black paint` move to explicit hold rows next round?

`No, not on current evidence`

### What would need to change?

At least one of the following:

1. repeated local titles explicitly using `titanium`
2. repeated local titles explicitly using `black paint`
3. evidence that `6bit` is being used in practice as a stable entity selector rather than just a coding descriptor
4. a stronger admin workflow source that exposes variant metadata beyond raw title text

Until then, the safest structure is to keep all three inside the broad `Leica APO-Summicron-M 90mm f/2 ASPH` row.
