# Elmar 135 Taxonomy Audit - Round 1

Date: 2026-05-08

Scope: read-heavy taxonomy audit for the Leica `Elmar 135` family. This round does not add seed rows, does not change classifier/query/search behavior, and does not change admin lookup ranking or UI. The goal is to determine whether `Elmar 135` is mature enough for explicit canonical seeding and, if so, at what granularity.

## Executive Summary

`Elmar 135` is literature-real, but round-1 should remain conservative and **not** seed it yet.

The strongest round-1 conclusion is:

- immediate recommended `core` candidate count: `0`
- recommended round-1 disposition: `seed 보류`

The broad `Elmar 135` area is operationally fragile because local `elmar 135` retrieval is heavily contaminated by:

- `Tele-Elmar 135`
- `APO-Vario-Elmar-TL 55-135`
- accessories such as hoods and finders
- adjacent `Elmarit` / `Hektor` / `Telyt` naming regions

After strict contamination removal, the surviving local `Elmar 135` signal is only:

- `3` clean listings
- `2` unique title strings
- effectively one dealer shorthand pattern:
  - `M 135/4 Elmar (Silver)`

That is too thin and too dealer-shaped to justify a broad explicit seed row in round 1.

The safest interpretation is:

- broad `Elmar 135` core: `no / defer`
- strongest future candidate:
  - `Leica Elmar 135mm f/4`
- but even that should remain `보류` until title support broadens beyond one narrow local wording cluster

## Family Overview

The Leica `135mm` space is now one of the most crowded parts of the taxonomy:

- `APO-Telyt-M 135`
- `Tele-Elmar 135`
- `Tele-Elmar-M 135`
- `Elmarit-M 135`
- `Hektor 135`
- `Elmar 135`
- classic `Telyt 135`
- `R 135`
- accessories and third-party 135mm lenses

That makes `Elmar 135` more vulnerable than `Hektor 135` or `Elmarit-M 135`.

The key round-1 question is whether there is a stable, search-safe broad family anchor for:

- `Leica Elmar 135mm f/4`

Round-1 answer: not yet.

## Literature / Reference Base

The literature direction is straightforward enough:

- the relevant broad family identity is `Elmar 135mm f/4`
- historical naming can also appear as `13.5cm f/4`
- screw-thread / LTM context is historically relevant

However, literature support alone is not enough for seeding here, because local market language does not currently repeat those distinctions in a stable way.

What matters operationally:

1. `Elmar 135` is a real Leica family area
2. it must remain distinct from:
   - `Tele-Elmar 135`
   - `Elmarit-M 135`
   - `Hektor 135`
   - classic `Telyt 135`
   - `R 135`
3. local title support is still too thin to safely promote broad `Elmar 135` into a round-1 seed row

## Local Listing Evidence

Analysis base: `data/derived/results_resolved_v2.json`

Raw `Elmar 135` retrieval is heavily contaminated by:

- `Tele-Elmar 135`
- `APO-Vario-Elmar-TL 55-135`
- `Elmarit-M 135`
- `Hektor 135`
- accessory listings such as:
  - `Leica 50~135mm Elmar Hood`
  - `LEICA 135mm F4 ELMAR + finder`
  - `LEICA FIKUS / 12530 ... 13.5cm Summar, Elmar, Hektor`

After excluding those contaminating families and accessory-only items, the useful local `Elmar 135` pool becomes:

- strict clean local pool: `3`
- unique title strings: `2`

### Broad price clustering

KRW-parsed local observations:

- clean local pool priced count: `3`
- median KRW: `680,000`
- observed priced range: `440,000` to `950,000`

All priced examples come from the same narrow wording cluster:

- `[위탁] M 135/4 Elmar (Silver)` -> `950,000 KRW`
- `[중고] M 135/4 Elmar (Silver)` -> `680,000 KRW`
- `[위탁] M 135/4 Elmar (Silver)` -> `440,000 KRW`

This is not enough breadth to conclude that broad `Elmar 135` is operationally stable.

### Local title patterns

Surviving strict-clean titles:

- `[위탁] M 135/4 Elmar (Silver)`
- `[중고] M 135/4 Elmar (Silver)`

Important absences from the strict-clean pool:

- `13.5cm`
- `LTM`
- `screw`
- `vintage`
- `adapter`
- `black / chrome / nickel`
- explicit `finder`, `case`, `boxed`, `hood`

### Interpretation

The local result is the opposite of a healthy broad seed candidate:

1. almost all broad `elmar 135` retrieval is contamination
2. the residual clean pool is only `3` listings
3. those `3` listings reduce to one local shorthand pattern
4. there is no repeated support for:
   - `13.5cm`
   - `LTM`
   - `screw-thread`
   - `vintage`

So round-1 cannot responsibly turn this into a seeded family anchor.

## Candidate Entity Expansion

## Candidate 1: `Leica Elmar 135mm f/4`

### Official / literature basis

Real in literature.

### Mechanical distinction

Broadly coherent as a historical Leica family, but weak in local seller language.

### Optical distinction

Distinct from:

- `Tele-Elmar 135`
- `Elmarit-M 135`
- `Hektor 135`
- classic `Telyt 135`

### Market split potential

Too weak in current local data.

The clean pool is not just small; it is narrowly dealer-shaped.

### Search-intent split potential

Not strong enough in current local evidence.

Generic searches like:

- `elmar 135`
- `135 elmar`
- `135mm f4 elmar`

currently retrieve too much neighboring family noise before reaching the intended family.

### Round-1 verdict

- `보류`

## Candidate 2: `Elmar 13.5cm f/4`

### Official / literature basis

Real historical naming.

### Mechanical distinction

Historically meaningful, but not locally visible enough.

### Optical distinction

No evidence in local data that it should become a separate canonical row.

### Market split potential

Weak in current local data.

### Search-intent split potential

Weak in current local data, because `13.5cm` wording is effectively absent in the surviving clean pool.

### Round-1 verdict

- `overlay` / `보류`

## Candidate 3: `LTM / screw-thread / M adapter / M shorthand`

### Official / literature basis

Relevant descriptive axes, but not a clean row in local market language.

### Mechanical distinction

Potentially real, but not operationally reliable.

### Optical distinction

No evidence of separate optical lines.

### Market split potential

Weak.

### Search-intent split potential

Weak.

Current local `M 135/4 Elmar` wording looks more like seller shorthand than a safely row-shaping signal.

### Round-1 verdict

- `overlay` / `보류`

## Candidate 4: `finish / country / accessory bundle`

### Official / literature basis

Potentially relevant as description, but too thin in current local evidence.

### Mechanical distinction

Not strong enough for row-level treatment.

### Optical distinction

None.

### Market split potential

Weak and easily distorted by condition or completeness.

### Search-intent split potential

Weak.

### Round-1 verdict

- `overlay`

## Contamination / Boundary Review

The following remain out-of-family and must not be mixed into `Elmar 135`:

- `APO-Telyt-M 135`
- `Tele-Elmar 135`
- `Tele-Elmar-M 135`
- `Elmarit-M 135`
- `Hektor 135`
- classic `Telyt 135`
- `Telyt-R 135`
- `Elmarit-R 135`
- `APO-Telyt-R 135`
- `APO-Telyt-R 180`
- `APO-Telyt-R 280`
- accessory-only listings such as hood / case / cap / box / finder / adapter
- third-party `135mm` lenses

The biggest local contamination patterns in this audit were:

- `Tele-Elmar 135`
- `APO-Vario-Elmar-TL 55-135`
- accessory items mentioning `Elmar` and `13.5cm`

## Round-1 Recommendation

### Immediate core candidate

Recommended immediate `core` candidate count: `0`

Round-1 disposition:

- `seed 보류`

### Hold candidates

No explicit hold row is recommended yet.

Even the broadest future candidate:

- `Leica Elmar 135mm f/4`

still lacks enough local title diversity to justify seeded promotion.

### Overlay axes

Keep as overlay or row-below detail:

- `13.5cm`
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

- `Leica Elmar 135mm f/4`
- `Elmar 13.5cm f/4`
- `LTM / screw-thread Elmar 135`
- `M adapter / M shorthand Elmar 135`
- early / late generation rows

## Seed Readiness

Round-1 recommendation:

- next round seed add: `no`

This family should stay out of seeded rows until:

1. local `Elmar 135` title support grows beyond one dealer-shaped wording cluster
2. broad contamination from `Tele-Elmar`, `TL 55-135`, and accessories is less dominant

## Final Disposition

- immediate core candidate:
  - none
- hold candidate:
  - none
- overlay:
  - `13.5cm`
  - `LTM / screw-thread / M shorthand`
  - `black / chrome / nickel`
  - `adapter / hood / cap / case / boxed / packaging`
  - `filter / filter thread`
- out-of-family:
  - `APO-Telyt-M 135`
  - `Tele-Elmar 135`
  - `Tele-Elmar-M 135`
  - `Elmarit-M 135`
  - `Hektor 135`
  - classic `Telyt 135`
  - `R 135`
  - accessories
  - third-party `135mm` lenses
