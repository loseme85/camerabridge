# Hektor 135 Taxonomy Audit - Round 1

Date: 2026-05-08

Scope: read-heavy taxonomy audit for the Leica `Hektor 135` family. This round does not add seed rows, does not change classifier/query/search behavior, and does not change admin lookup ranking or UI. The goal is to determine whether `Hektor 135` is mature enough for explicit canonical seeding and, if so, at what granularity.

## Executive Summary

`Hektor 135` looks seedable, but only as one narrow broad family row.

The strongest round-1 conclusion is:

1. `Leica Hektor 135mm f/4.5`

as the only immediate first-pass `core` candidate.

Round-1 does **not** support opening:

- separate `LTM / screw-thread` rows
- separate `M adapter / M seller shorthand` rows
- early / late rows
- finish rows
- accessory bundle rows

Round-1 conclusion:

- immediate recommended `core` candidate count: `1`
- recommended first-pass core:
  - `Leica Hektor 135mm f/4.5`
- explicit `hold` candidate:
  - none
- `LTM / screw-thread / M shorthand`, `black / chrome / nickel`, `adapter included`, `hood included`, `cap included`, `boxed`, `case included`, `packaging`, and filter-thread wording stay `overlay` or `보류`
- `APO-Telyt-M 135`, `Tele-Elmar 135`, `Tele-Elmar-M 135`, `Elmarit-M 135`, `Elmar 135`, classic `Telyt 135`, `R 135`, accessories, and third-party 135mm lenses remain out-of-family boundaries

The safest next step is a narrow seed add for `Leica Hektor 135mm f/4.5` only.

## Family Overview

The Leica `135mm` field is already populated by multiple adjacent families:

- `APO-Telyt-M 135`
- `Tele-Elmar 135`
- `Elmarit-M 135`
- `Hektor 135`
- `Elmar 135`
- classic `Telyt 135`
- `R 135`
- accessories and third-party 135mm lenses

Unlike `APO-Telyt-M 135`, `Hektor 135` is an older vintage-family area where seller mount wording is not always a clean product-line signal.

The real round-1 question is whether:

1. there is one stable `Hektor 135` family anchor
2. or whether `LTM / screw / M adapter / vintage` language forces hold-only treatment

Round-1 answer: there is enough support for one broad family row, but not for any internal seeded sub-rows.

## Literature / Reference Base

The literature convention around Leica `Hektor 135` is straightforward:

- the recognizable family identity is the classic `13.5cm / 135mm Hektor`
- the practically relevant aperture line in local seller language is `f/4.5`

What is *not* literature-clean in the current local market language is a separate Leica line such as:

- `Hektor-M 135`
- a distinct modern `M-mount` Hektor family

That matters because local `M 135/4.5 Hektor` wording is more likely to be seller mount shorthand or adaptation shorthand than a separate canonical Leica product line.

Operational interpretation:

1. `Leica Hektor 135mm f/4.5` is a real broad family identity
2. `LTM / screw-thread / M` wording should not automatically become separate row structure
3. boundary separation from `Tele-Elmar`, `Elmarit-M`, `APO-Telyt-M`, `Elmar`, and `Telyt` remains mandatory

## Local Listing Evidence

Analysis base: `data/derived/results_resolved_v2.json`

Raw `Hektor 135`-like matches include accessory contamination from:

- `LEICA FIKUS / 12530 3.5 / 5 / 9 / 13.5cm Summar, Elmar, Hektor`

After excluding that accessory contamination, the useful local pool becomes:

- clean local pool: `4`

### Broad price clustering

KRW-parsed local observations:

- clean local pool priced count: `3`
- median KRW: `400,000`
- observed priced range: `350,000` to `680,000`

Priced examples:

- `Leica M 135mm f4.5 Hektor Silver` -> `400,000 KRW`
- `[위탁] M 135/4.5 Hektor (Silver)` -> `350,000 KRW`
- `[중고] M 135/4 Hektor (Silver)` -> `680,000 KRW`

The third title appears to use `f/4` wording, but the family context strongly suggests seller shorthand or listing inconsistency rather than a separate canonical line.

### Local title patterns

Broad recurring titles:

- `Leica M 135mm f4.5 Hektor Silver`
- `[위탁] M 135/4.5 Hektor (Silver)`
- `LEICA 135mm F4.5 Hektor sn.1385`

More ambiguous local wording:

- `[중고] M 135/4 Hektor (Silver)`

### Local marker frequency

Repeated local modifiers:

- `m` or `m 135/...` shorthand: strong
- `silver`: `3`
- `f4.5`: direct in multiple titles

Not meaningfully present in the clean local pool:

- `ltm`
- `screw`
- `13.5cm`
- `original`
- `vintage`
- `black`
- `chrome`
- `nickel`
- `hood`
- `case`
- `boxed`

### Interpretation

This family is thin, but the thinness does **not** create multiple competing internal rows.

The important pattern is:

1. accessory contamination is easy to identify and exclude
2. surviving lens titles all point to the same historical `Hektor 135` family
3. explicit `LTM / screw-thread` wording is mostly absent locally
4. `M` wording appears often, but behaves like seller shorthand rather than a literature-clean separate line

That is the shape of one immediate `core` and no round-1 `hold` rows.

## Candidate Entity Expansion

## Candidate 1: `Leica Hektor 135mm f/4.5`

### Official / literature basis

Strong enough for `core`.

The broad family identity is literature-real and distinct from:

- `APO-Telyt-M 135`
- `Tele-Elmar 135`
- `Elmarit-M 135`
- `Elmar 135`
- classic `Telyt 135`

### Mechanical distinction

Strong enough for one broad `core`, but not for round-1 sub-rows.

Local wording does not support a clean row split between:

- `LTM / screw-thread`
- `M` or adapted shorthand
- early / late mechanics

### Optical distinction

Strong enough for `core`.

The local family identity consistently points to the Leica `135mm Hektor` line rather than another 135mm Leica family.

### Market split potential

Moderate.

The priced sample is small, but it does not show evidence of multiple distinct price-table clusters inside the clean pool.

### Search-intent split potential

Strong enough for one broad family anchor.

Queries like:

- `hektor 135`
- `135 hektor`
- `135mm f4.5 hektor`
- `hektor 13.5cm`

all naturally point toward the same family intent.

### Round-1 verdict

- `core`

## Candidate 2: `Hektor 13.5cm f/4.5`

### Official / literature basis

Real historical naming.

### Mechanical distinction

Not strong enough locally for a separate row.

The local lens pool does not actually repeat `13.5cm` wording on the lens listings themselves; that wording appears more clearly in accessory contamination than in clean lens titles.

### Optical distinction

Not enough evidence that `13.5cm` wording should become its own row instead of remaining inside the broad family.

### Market split potential

Weak in current local data.

### Search-intent split potential

Real, but better absorbed by the broad family row.

### Round-1 verdict

- `overlay` / `보류`

## Candidate 3: `LTM / screw-thread / M adapter / M shorthand`

### Official / literature basis

These are meaningful descriptive axes, but not a clean seeded row in the current local market evidence.

### Mechanical distinction

Potentially real, but operationally weak.

The local pool shows:

- repeated `M` wording

but almost no:

- `LTM`
- `screw`
- `adapter`

So round-1 cannot safely separate:

- original screw-mount identity
- seller shorthand indicating mounting or adaptation

### Optical distinction

No evidence of different optical families.

### Market split potential

Weak.

### Search-intent split potential

Not strong enough for row promotion yet.

### Round-1 verdict

- `overlay` / `보류`

## Candidate 4: `black / chrome / nickel / accessory bundle`

### Official / literature basis

Potentially meaningful descriptors, but too thin locally.

### Mechanical distinction

Not strong enough for row-level treatment.

### Optical distinction

None.

### Market split potential

Weak and easily distorted by condition or accessory completeness.

### Search-intent split potential

Weak.

### Round-1 verdict

- `overlay`

## Contamination / Boundary Review

The following remain out-of-family and must not be mixed into `Hektor 135`:

- `APO-Telyt-M 135`
- `Tele-Elmar 135`
- `Tele-Elmar-M 135`
- `Elmarit-M 135`
- `Elmar 135`
- classic `Telyt 135`
- `Telyt-R 135`
- `Elmarit-R 135`
- `APO-Telyt-R 135`
- `APO-Telyt-R 180`
- `APO-Telyt-R 280`
- accessory-only listings such as hood / case / cap / adapter
- third-party `135mm` lenses

The most obvious local contamination in this audit was:

- `LEICA FIKUS / 12530 3.5 / 5 / 9 / 13.5cm Summar, Elmar, Hektor`

which mentions `13.5cm Hektor` compatibility but is not a lens listing.

## Round-1 Recommendation

### Immediate core candidate

Recommended immediate `core` candidate count: `1`

1. `Leica Hektor 135mm f/4.5`

### Hold candidates

None recommended in round 1.

The family does not yet show a narrow internal split that is simultaneously:

- literature-clean
- local-title-explicit
- and operationally safer than a broad family row

### Overlay axes

Keep as overlay or row-below detail:

- `LTM / screw-thread / M shorthand`
- `black / chrome / nickel`
- `country marking`
- `M adapter included`
- `hood included`
- `cap included`
- `boxed`
- `case included`
- `condition`
- `original cap / hood / box / case`
- `packaging`
- `filter / filter thread`

### Deferred / hold-back items

Do not seed yet:

- `Hektor 13.5cm` as a separate row
- `LTM / screw-thread` as a separate row
- `M adapter / M shorthand` as a separate row
- early / late generation rows

## Seed Readiness

Round-1 recommendation:

- next round seed add: `yes`
- but only as a very narrow single-row add

Safest next step:

1. add `Leica Hektor 135mm f/4.5` as one broad `core`
2. keep `13.5cm`, `LTM / screw`, and mount-description language outside seeded sub-rows

## Final Disposition

- immediate core candidate:
  - `Leica Hektor 135mm f/4.5`
- hold candidate:
  - none
- overlay:
  - `LTM / screw-thread / M shorthand`
  - `black / chrome / nickel`
  - `M adapter included`
  - `hood / cap / case / boxed / packaging`
  - `filter / filter thread`
- out-of-family:
  - `APO-Telyt-M 135`
  - `Tele-Elmar 135`
  - `Tele-Elmar-M 135`
  - `Elmarit-M 135`
  - `Elmar 135`
  - classic `Telyt 135`
  - `R 135`
  - accessories
  - third-party `135mm` lenses
