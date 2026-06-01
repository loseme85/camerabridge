# Foundation 1.0 Closeout Snapshot

Last updated: 2026-05-25

## Purpose

Camera Bridge Leica normalization Foundation 1.0 is the baseline layer for search and classification reliability.

Its job is to give dealer titles, shorthand, contaminated naming, and mixed-family wording a stable canonical landing zone so that:

- search miss rate goes down
- false merges go down
- classifier and ranking layers inherit cleaner family boundaries
- future intake work starts from a known baseline instead of re-litigating taxonomy every round

This is not a complete Leica catalog. It is the stabilized foundation layer that the next reporting and intake stages can safely build on.

## Current Snapshot

- `active seeded families`: `51`
- `deferred / audit-only families`: `33`
- `explicit future hold candidates`: `2`
- `golden_set.py`: `132/132`

## Structural Model

- `core`
  - explicitly opened canonical rows that are live in seed files and index
- `hold`
  - intentionally separated rows that are real enough to preserve, but not broad core landings
- `deferred`
  - literature-real or structurally plausible families that are not ready to seed yet
- `closed non-family hypothesis`
  - unsupported product-line guesses that should stay closed unless future official evidence appears
- `overlay`
  - finish/version/accessory/packaging/coding/filter metadata that should not become separate canonical rows
- `boundary`
  - adjacent families that must stay distinct even when dealer wording collapses them
- `hard-pin prohibited broad alias`
  - broad shorthand that is too contaminated to resolve directly into one family

## SL Wide Closeout

Foundation 1.0 closes the current Leica SL wide-prime / wide-zoom axis at the following state:

- `Super-Vario-Elmarit-SL 14-24`
  - literature-real
  - `deferred`
- `Super-Vario-Elmar-SL 16-35`
  - active `core`
- `Super-APO-Summicron-SL 21`
  - literature-real
  - `deferred`
- `APO-Summicron-SL 24`
  - `closed non-family hypothesis`
- `Summicron-SL 24`
  - `closed non-family hypothesis`
- `APO-Summicron-SL 28`
  - active `core`
- `Summicron-SL 28`
  - `closed non-family hypothesis`
- `APO-Summicron-SL 35`
  - active `core`
- `Summicron-SL 35`
  - literature-real
  - `deferred`
- `Vario-Elmarit-SL 24-90`
  - active `core`

The working SL wide-prime structure at Foundation 1.0 closeout is:

- `Super-APO-Summicron-SL 21mm f/2 ASPH`
- `APO-Summicron-SL 28mm f/2 ASPH`
- `APO-Summicron-SL 35mm f/2 ASPH`

The important negative result is just as valuable:

- no supported official Leica SL `24mm f/2` prime line has been confirmed
- both `APO-Summicron-SL 24` and `Summicron-SL 24` stay closed
- non-APO `Summicron-SL 28` also stays closed

## Representative Closed Hypotheses

These are not “real families with weak support.” They are currently unsupported and intentionally closed.

- `Summicron 24 / Summicron-M 24`
  - unsupported hypothesis
  - real 24mm M structure is carried by `Elmarit 24`, `Elmar-M 24`, `Summilux 24`
- `APO-Summicron-SL 24`
  - unsupported Leica SL family hypothesis
  - official SL wide-prime structure jumps from `Super-APO-Summicron-SL 21` to `APO-Summicron-SL 28`
- `Summicron-SL 24`
  - unsupported Leica SL family hypothesis
  - no official non-APO SL `24mm f/2` line confirmed
- `Summicron-SL 28`
  - unsupported Leica SL family hypothesis
  - official SL `28mm f/2` line resolves to `APO-Summicron-SL 28`
- `Super-Elmar 24`
  - wrong-family label
  - reframed to `Elmar-M 24mm f/3.8 ASPH`

## Overlay Axes Left Intentionally Out of Row-Level Taxonomy

Foundation 1.0 keeps the following as overlay or metadata axes instead of separate canonical rows:

- finish
- country marking
- `6bit` / coding
- `ROM` / cam version
- filter thread
- hood / cap / case / box / packaging
- finder included
- condition
- special edition
- tripod collar

Family-specific markers such as `OIS`, `ASPH`, `APO`, `Super-APO`, `E67`, `E82`, and similar descriptors are only promoted when they are necessary as canonical family markers. Otherwise they stay as metadata or deferred internal markers.

## Hard-Pin Prohibition Principle

Foundation 1.0 repeatedly found that broad dealer shorthand is one of the biggest sources of false resolution. The rule is conservative on purpose.

Examples of broad shorthand that should stay hard-pin prohibited:

- broad `summicron 24`
- broad `leica sl 24`
- broad `24 cron`
- broad `summicron 28`
- broad `apo summicron 24`
- broad `vario elmarit`
- broad focal-only zoom shorthand such as bare `14-24`, `16-35`, `24-90`
- family-unclear `lux`, `cron`, `apo` shorthand

The reason is consistent:

- cross-mount contamination
- adjacent-family contamination
- SL vs M/R confusion
- accessory or bundle contamination
- third-party L-mount contamination

## Boundary Discipline

Foundation 1.0 depends on keeping adjacent structures separate even when dealer wording collapses them.

Important recurring boundaries:

- `M` vs `R` vs `SL`
- prime vs zoom
- `APO` vs non-`APO`
- Leica lens family vs accessory-only listing
- Leica lens family vs fixed-lens body references
- Leica family vs third-party L-mount family

On the SL wide side in particular, the following must remain separated:

- `Super-Vario-Elmarit-SL 14-24` vs `Super-Vario-Elmar-SL 16-35`
- `Super-APO-Summicron-SL 21` vs M `21mm` families and `WATE`
- closed `24mm f/2` SL hypotheses vs real SL `21 / 28 / 35`
- `APO-Summicron-SL 28` vs Q-series / M `28mm` / third-party `28mm`

## Reopen Conditions for Foundation 1.1

Foundation 1.0 should only be reopened when there is evidence that the current baseline is no longer enough.

Valid triggers:

- dealer-listed items exist but our search still misses them
- the same ambiguous dealer naming keeps recurring
- user searches or saved alerts repeatedly produce no-result or low-confidence outcomes
- a newly onboarded dealer source introduces many unknown or ambiguous titles
- price guidance needs a row-level split that the current family structure cannot express safely

Without one of those triggers, the right move is to keep Foundation 1.0 stable and push uncertainty into intake rather than reopening canonical structure casually.

## Handoff to the Next Layer

The next stage should treat this snapshot as the fixed baseline and build operational feedback loops on top of it.

### Search Reliability Report v0

Use the Foundation 1.0 baseline to measure:

- search recall on dealer-listed items
- top-rank correctness on ambiguous titles
- low-confidence clusters by family
- repeated contamination patterns by mount, focal length, and shorthand

### Normalization Intake Queue

Use the same baseline to collect:

- low-confidence titles
- unknown titles
- ambiguous titles
- recurring dealer wording patterns
- candidate aliases that are observed repeatedly but not yet accepted

Recommended intake flow:

- `observed`
- `candidate`
- `reviewed`
- `accepted` or `closed`

That flow should keep future alias growth evidence-based instead of expanding from one-off title shapes.

## Completion Meaning

This document does not mean Foundation 1.0 is “finished forever.”

It means the current canonical baseline is stable enough to freeze, hand off, and build the next layers on top of:

- Search Reliability Report v0
- Normalization Intake Queue
- low-confidence / unknown / ambiguous collection
- dealer search recall measurement

In short: Foundation 1.0 is being fixed as a baseline, not retired as a concept.
