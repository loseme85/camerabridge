# Summicron-SL 28 Taxonomy Audit - Round 1

Date: 2026-05-23

Scope: audit-only review for the `Summicron-SL 28` family hypothesis. This round does not add seed rows, does not modify `entities/*.json`, does not modify `canonical_entities_index.json`, and does not change classifier/query/search behavior, ranking, or UI.

## Executive Summary

`Summicron-SL 28` is not supported as a real Leica SL family in round 1.

Primary Leica literature for SL `28mm f/2` consistently documents:

- `Leica APO-Summicron-SL 28mm f/2 ASPH`

and does not document:

- `Leica Summicron-SL 28mm f/2 ASPH`

Round-1 conclusion:

- literature status:
  - unsupported family hypothesis
  - closed non-family hypothesis
- immediate recommended `core` candidate count: `0`
- recommended first-pass core:
  - none
- explicit `hold` candidate:
  - none
- strongest deferred candidate:
  - none
- next seed round:
  - not allowed in current state
- local `SL 28 Summicron` retrieval collapses entirely into APO contamination
- broad `summicron-sl 28` / `summicron sl 28` / `summicron 28` / `leica sl 28` / `28 cron` retrieval remains unsafe and must not be hard-pinned

The safest round-1 answer is:

1. close `Leica Summicron-SL 28mm f/2 ASPH` as an unsupported family hypothesis
2. keep `Leica APO-Summicron-SL 28mm f/2 ASPH` as the only literature-real SL `28mm f/2` family
3. do not treat body-kit or shorthand pollution as support for a non-APO family
4. keep M `28mm`, Q-series `28mm`, neighboring SL families, and third-party L-mount `24 / 28 / 35mm` lenses as hard boundaries

## Literature / Reference Base

### Source A: Leica Camera technical specification for SL `28mm f/2`

Leica Camera documents:

- `APO-Summicron-SL 28 f/2 ASPH.`
- order number:
  - `11183`
- bayonet / format:
  - `L-Mount`, full-frame `35mm` format
- filter mount:
  - `E67`

No non-APO `Summicron-SL 28` family is documented on the corresponding official `28mm f/2` SL literature path.

Reference:

- [Leica Camera - Technical Specifications - APO-Summicron-SL 28 f/2 ASPH.](https://leica-camera.com/en-US/photography/lenses/sl/apo-summicron-sl-28-f2-asph-black-finish/technical-specification)

### Source B: Leica Camera product page for SL `28mm f/2`

Leica Camera product literature for the SL `28mm f/2` line consistently uses:

- `APO-Summicron-SL 28 f/2 ASPH.`

The official Leica product copy positions this as the SL `28mm` wide-angle prime and does not surface a separate non-APO `Summicron-SL 28`.

Reference:

- [Leica Camera - APO-Summicron-SL 28 f/2 ASPH.](https://leica-camera.com/en-US/photography/lenses/sl/apo-summicron-sl-28-f2-asph-black-finish)

### Source C: Leica press literature for the SL `28mm f/2`

Leica press literature describes:

- `APO-Summicron-SL 28 f/2 ASPH.`

as the SL-system wide-angle lens introduction in this line.

This reinforces that the literature-real SL `28mm f/2` family is the APO family, not a parallel non-APO `Summicron-SL 28`.

Reference:

- [Leica Camera Press Release - The APO-Summicron-SL 28 f/2 ASPH.](https://leica-camera.com/es-MX/Company/Press-Centre/Press-Releases/2021/Press-Release-The-APO-Summicron-SL-28-f-2-ASPH.-A-wide-angle-lens-with-state-of-the-art-technology-for-the-Leica-SL-System)

### Source D: adjacent non-APO Summicron-SL families

In nearby SL focal lengths, Leica does document literature-real non-APO families such as:

- `Summicron-SL 35 f/2 ASPH.`
- `Summicron-SL 50 f/2 ASPH.`

That makes the absence of an official `Summicron-SL 28` line more meaningful, not less.

Round-1 implication:

- non-APO `Summicron-SL 35` is real
- non-APO `Summicron-SL 50` is real
- non-APO `Summicron-SL 28` is not supported by primary Leica literature in this round

## Taxonomy Implication from Literature

Round-1 literature supports:

- one real SL-side `28mm f/2` family:
  - `Leica APO-Summicron-SL 28mm f/2 ASPH`

Round-1 literature does **not** support:

- `Leica Summicron-SL 28mm f/2 ASPH`

That means:

- `Summicron-SL 28` should not be treated as a weak real family
- it should be treated as an unsupported family hypothesis
- it should be closed unless future official Leica literature proves the exact non-APO product line exists

If future evidence appears, the hypothesis can be reopened. In round 1, it should remain closed.

## Boundary Check

This hypothesis must remain separate from:

- `Leica APO-Summicron-SL 28mm f/2 ASPH`
- `Leica Summicron-M 28mm f/2 ASPH`
- `Leica Summilux-M 28mm f/1.4 ASPH`
- `Leica Elmarit-M 28mm f/2.8 ASPH`
- `Leica Summaron 28mm`
- `Leica Elmarit-R 28mm f/2.8`
- Leica `Q / Q2 / Q3` fixed-lens `28mm` bodies
- `Leica Super-APO-Summicron-SL 21mm f/2 ASPH`
- closed `Leica APO-Summicron-SL 24mm f/2 ASPH` hypothesis
- `Leica APO-Summicron-SL 35mm f/2 ASPH`
- `Leica Summicron-SL 35mm f/2 ASPH`
- `Leica Super-Vario-Elmar-SL 16-35mm f/3.5-4.5 ASPH`
- `Leica Vario-Elmarit-SL 24-90mm f/2.8-4 ASPH`
- Sigma / Panasonic / Lumix `24 / 28 / 35mm` L-mount lenses
- accessory-only listings

## Local Listing Evidence

Analysis base:

- `data/normalized/normalized_latest.json`
- `results.json`
- `data/sold_items.json`

### Broad retrieval behavior

Broad shorthand is risky.

Within the wider `summicron / 28 / sl` field, reviewed local rows collapse into:

- `Leica APO-Summicron-SL 28mm f/2 ASPH`
- M `28mm` Summicron families
- Q-series `28mm`
- neighboring SL prime and zoom families
- third-party L-mount `24 / 28 / 35mm`

Representative reviewed local `SL 28 Summicron` rows are all APO-side:

- `[중고] SL 28/2 APO Summicron ASPH (Black)`
- `[위탁] SL 28/2 APO Summicron ASPH (Black)`
- `LEICA 28mm F2 ASPH APO-SUMMICRON-SL sn.4806`

Interpretation:

- broad `summicron-sl 28`
- broad `summicron sl 28`
- broad `summicron 28`
- broad `leica sl 28`
- broad `28 cron`

are not safe shaping aliases in round 1 because they drift into:

- the already-seeded `APO-Summicron-SL 28`
- M-side `28mm` Summicron / Summilux / Elmarit / Summaron families
- Q-series `28mm` fixed-lens bodies
- neighboring SL `21 / 35 / 16-35 / 24-90`
- Sigma / Panasonic / Lumix L-mount wide primes
- accessory-only listings

### Clean local non-APO SL-side pool

After restricting to explicit non-APO `Summicron-SL 28mm f/2 ASPH` wording, and excluding:

- APO rows
- M-side `28mm`
- R-side `28mm`
- Q-series
- neighboring SL `21 / 35 / 16-35 / 24-90`
- third-party
- accessory contamination
- body-kit or bundle contamination

the usable local pool becomes:

- clean local pool: `0`
- unique titles: `0`
- KRW-priced count: `0`
- KRW median: none

Interpretation:

- there is no clean local evidence for a non-APO `Summicron-SL 28`
- all reviewed `SL 28 Summicron` local visibility points to APO contamination instead

### Body-kit / bundle handling

No reviewed body-kit or bundle row was accepted as clean lens-row support for this hypothesis.

Round-1 rule remains:

- even if a future `SL body + 28 Summicron` bundle appears, it must not be counted as lens-only support for the family hypothesis

## Round-1 Recommendation

### Literature status

- unsupported family hypothesis
- closed non-family hypothesis

### Immediate `core` candidate count

- `0`

### Recommended first-pass `core`

- none

### Explicit `hold` candidates

- none

### Strongest deferred candidate

- none

## Why close the hypothesis instead of deferring it?

Because round-1 evidence does not say:

- real family, weak local support

It says:

- official Leica SL `28mm f/2` literature consistently identifies the family as `APO-Summicron-SL 28`
- non-APO `Summicron-SL 28` does not appear as a supported product line
- local `SL 28 Summicron` retrieval collapses entirely into APO contamination

So this is not a conservative defer. It is a closed unsupported family hypothesis.

## Overlay / Deferred Metadata

If the hypothesis were ever reopened, these would still remain non-row markers:

- `ASPH`
- `E67`
- filter-thread marker
- hood / cap / case / boxed / packaging

But in round 1 no row should be opened, so these remain hypothetical markers only and should not be promoted.

## Final Round-1 Recommendation

### Seedability in this round

- closed

### Best next action

- do not seed
- do not defer as a literature-real family
- record the hypothesis as unsupported
- continue to use `APO-Summicron-SL 28` as the only SL-side `28mm f/2` canonical family

### Unsafe broad aliases

Do **not** hard-pin:

- `summicron-sl 28`
- `summicron sl 28`
- `summicron 28`
- `leica sl 28`
- `28 cron`
