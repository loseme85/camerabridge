# Telyt 135 Taxonomy Audit - Round 1

Date: 2026-05-08

Scope: read-heavy taxonomy audit for the Leica `classic Telyt 135` family. This round does not add seed rows, does not change classifier/query/search behavior, and does not change admin lookup ranking or UI. The goal is to determine whether `classic Telyt 135` is mature enough for explicit canonical seeding and, if so, at what granularity.

## Executive Summary

Round-1 result: `seed 보류`.

There is not enough operational evidence that `classic Telyt 135` is currently visible as a stable, independently searchable family in the local market data.

The strongest round-1 conclusion is:

- immediate recommended `core` candidate count: `0`
- recommended round-1 disposition: `seed 보류`

Why:

1. local `telyt 135` retrieval is almost entirely `APO-Telyt-M 135`
2. after excluding `APO-Telyt-M` contamination, the strict clean local pool is `0`
3. literature-adjacent `Visoflex` references found in current source checking point primarily to other classic Telyt focal lengths such as:
   - `20 cm 1:4 Telyt`
   - `20 cm 1:4.5 Telyt`
   - longer `280 / 400 / 560` Telyt families
4. there is no repeated local title support for a practical `classic Telyt 135` row

Operationally, that means round-1 should not open:

- a broad `Telyt 135` core
- a `Telyt 13.5cm` row
- a `Visoflex Telyt 135` row
- a `Telyt-R 135` row

## Family Overview

The Leica `135mm` region is already occupied by several families that are much more visible in local listings:

- `APO-Telyt-M 135`
- `Tele-Elmar 135`
- `Tele-Elmar-M 135`
- `Elmarit-M 135`
- `Hektor 135`
- `Elmar 135`
- `classic Telyt`
- `R 135`

The round-1 question is whether `classic Telyt 135` appears as a real local family or whether generic `telyt 135` retrieval is just a contamination bucket from nearby APO/R/Visoflex material.

Round-1 answer: contamination dominates, and there is not enough clean local family signal to seed anything.

## Literature / Reference Base

### Source A: Leica Wiki - `135mm f/3.4 ASPH Apo-Telyt-M`

Leica Wiki clearly documents:

- `135mm f/3.4 ASPH Apo-Telyt-M`

as a modern Leica M family with inscription:

- `APO-TELYT-M 1:3.4/135`

Reference:

- [Leica Wiki - 135mm f/3.4 ASPH Apo-Telyt-M](https://wiki.l-camera-forum.com/leica-wiki.en/index.php/135mm_f/3.4_ASPH_Apo-Telyt-M)

This matters because broad local `telyt 135` retrieval is dominated by this family, not by a clean classic Telyt 135 line.

### Source B: Leica Wiki - `Visoflex`

The Leica Wiki `Visoflex` page highlights classic long-lens use with:

- `135mm f/4 Tele-Elmar`
- `F = 20 cm 1:4 Telyt`
- `F = 20 cm 1:4.5 Telyt`
- longer `280 / 400 / 560 / 800` Telyt lines

Reference:

- [Leica Wiki - Visoflex](https://wiki.l-camera-forum.com/leica-wiki.en/index.php/Visoflex)

This is important because it suggests that in current documentary context, the classic Telyt space that stays highly visible around Visoflex is centered more strongly on `20 cm` and longer lines than on a locally retrievable `135mm` Telyt family.

### Source C: Leica Wiki - `OUBIO`

Leica Wiki documents `OUBIO` as a Visoflex adapter for lens heads including:

- `F = 20 cm 1:4 Telyt`
- `F = 20 cm 1:4.5 Telyt`
- multiple longer classic Telyt lines

Reference:

- [Leica Wiki - OUBIO](https://wiki.l-camera-forum.com/leica-wiki.en/index.php/OUBIO)

Again, the relevant classic Telyt references visible here do not produce a strong independent `135mm` local family signal.

### Interpretation

The literature check does **not** say that a classic `Telyt 135` family is impossible.

But it does say something operationally important:

1. `APO-Telyt-M 135` is highly visible and must remain separate
2. classic `Telyt` references that are easy to verify are often centered on non-135 focal lengths
3. the current round-1 local retrieval does not provide enough support to carve out a practical `classic Telyt 135` seed row

## Local Listing Evidence

Analysis base: `data/derived/results_resolved_v2.json`

### Raw retrieval

Broad `telyt` retrieval with `135` or `13.5cm` wording returns:

- raw local pool: `16`

But every one of those raw hits is:

- `APO-Telyt-M 135`

Examples:

- `[중고] M 135/3.4 Apo-Telyt (Black)`
- `LEICA 135mm F3.4 APO-TELYT-M sn.4239`
- `LEICA 135mm F3.4 APO-TELYT-M sn.3910`

### Strict clean pool after contamination removal

After excluding:

- `APO-Telyt-M`
- `APO-Telyt-R`
- `Telyt-R`
- `Tele-Elmar`
- `Elmarit`
- `Hektor`
- `Elmar`
- Visoflex / adapter / hood / cap / case / finder style accessory-only contamination

the surviving strict clean local pool becomes:

- strict clean local pool: `0`

### Broad price clustering

For strict clean classic `Telyt 135`:

- priced count: `0`
- median KRW: none

### Local title patterns

There are no surviving clean local title strings for:

- `Telyt 135`
- `Telyt 13.5cm`
- `135mm f/4 Telyt`
- `135mm f/4.5 Telyt`
- `Visoflex Telyt 135`

### Interpretation

This is the clearest possible round-1 seed defer signal:

1. raw retrieval exists
2. but it all belongs to a different family (`APO-Telyt-M 135`)
3. after proper boundary cleanup, nothing remains

So there is no local market basis for a seeded `classic Telyt 135` row right now.

## Candidate Entity Expansion

## Candidate 1: `classic Telyt 135`

### Official / literature basis

Insufficiently clear for round-1 seeding.

There is not enough confirmed evidence in the current literature/local combination to say that a practical seed row for `classic Telyt 135` is locally active and distinct.

### Mechanical distinction

Not operationally visible in current local data.

### Optical distinction

Potentially real historically, but not locally represented as a distinct family in the current pool.

### Market split potential

None visible in current local data.

### Search-intent split potential

Weak.

Current `telyt 135` retrieval behaves like contamination into `APO-Telyt-M 135`, not a clean standalone family.

### Round-1 verdict

- `보류`

## Candidate 2: `Telyt 13.5cm`

### Official / literature basis

Historically plausible naming direction.

### Mechanical distinction

Not locally visible.

### Optical distinction

No current local support for separate row treatment.

### Market split potential

None visible in current local data.

### Search-intent split potential

Too weak.

### Round-1 verdict

- `보류`

## Candidate 3: `Visoflex Telyt 135`

### Official / literature basis

Visoflex is literature-real, but current literature checks surfaced stronger `20 cm` and longer Telyt associations than a clean `135mm` line.

### Mechanical distinction

Could matter historically, but not represented in current local data as a repeated lens-family title.

### Optical distinction

Not enough evidence for a row.

### Market split potential

None visible locally.

### Search-intent split potential

Weak and easily confused with adapters / housings / accessory bundles.

### Round-1 verdict

- `overlay` / `보류`

## Candidate 4: `LTM / M / adapter / finish / accessory axes`

### Official / literature basis

These are descriptive axes, not current row candidates.

### Mechanical distinction

Potentially meaningful historically, but not visible as local row-shaping signals.

### Optical distinction

None.

### Market split potential

None visible.

### Search-intent split potential

Weak.

### Round-1 verdict

- `overlay`

## Contamination / Boundary Review

The following remain out-of-family and must not be mixed into `classic Telyt 135`:

- `APO-Telyt-M 135`
- `APO-Telyt-R 135 / 180 / 280`
- `Tele-Elmar 135`
- `Tele-Elmar-M 135`
- `Elmarit-M 135`
- `Hektor 135`
- `Elmar 135`
- `Telyt-R 135`
- `R 135`
- Visoflex accessories and adapters
- accessory-only listings such as hood / cap / case / box / finder / adapter
- third-party `135mm` lenses

The most important operational contamination fact in this audit:

- broad `telyt 135` local retrieval currently means `APO-Telyt-M 135`, not classic `Telyt 135`

## Round-1 Recommendation

### Immediate core candidate

Recommended immediate `core` candidate count: `0`

Round-1 disposition:

- `seed 보류`

### Hold candidates

None recommended in round 1.

There is no local title support strong enough to justify even a narrow explicit hold row.

### Overlay axes

Keep as overlay or row-below detail if they ever become relevant later:

- `Visoflex`
- `LTM / M / adapter wording`
- `13.5cm`
- `black / chrome / nickel`
- `hood / cap / case / boxed / packaging`
- `filter / filter thread`

### Deferred / hold-back items

Do not seed yet:

- `classic Telyt 135`
- `Telyt 13.5cm`
- `Visoflex Telyt 135`
- `Telyt-R 135`

## Seed Readiness

Round-1 recommendation:

- next round seed add: `no`

This family should remain closed until:

1. local clean classic `Telyt 135` listings actually appear
2. generic `telyt 135` retrieval stops being dominated by `APO-Telyt-M 135`
3. there is enough local wording to distinguish lens family from Visoflex/accessory context

## Final Disposition

- immediate core candidate:
  - none
- hold candidate:
  - none
- overlay:
  - `13.5cm`
  - `Visoflex`
  - `LTM / M / adapter wording`
  - `black / chrome / nickel`
  - `hood / cap / case / boxed / packaging`
  - `filter / filter thread`
- out-of-family:
  - `APO-Telyt-M 135`
  - `APO-Telyt-R 135 / 180 / 280`
  - `Tele-Elmar 135`
  - `Tele-Elmar-M 135`
  - `Elmarit-M 135`
  - `Hektor 135`
  - `Elmar 135`
  - `Telyt-R 135`
  - `R 135`
  - Visoflex accessories
  - other accessories
  - third-party `135mm` lenses
