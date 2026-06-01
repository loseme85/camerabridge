# Tele-Elmarit 90 Taxonomy Audit - Round 1

Date: 2026-04-30

Scope: read-heavy taxonomy audit for the Leica `Tele-Elmarit 90` family. This round does not add seed rows, does not change classifier/query/search behavior, and does not change admin lookup ranking or UI. The goal is to determine whether `Tele-Elmarit 90` is mature enough for explicit canonical seeding and, if so, at what granularity.

## Executive Summary

`Tele-Elmarit 90` is strong enough to treat as a **separate family**, but its internal split should remain conservative in round 1.

The key round-1 judgment is:

- `Tele-Elmarit 90` and `Tele-Elmarit-M 90` are real literature/product distinctions
- but current local title support is much stronger for broad `Tele-Elmarit 90` than for a clean internal two-core split

Round-1 conclusion:

- immediate recommended `core` candidate count: `1`
- recommended first-pass core:
  - `Leica Tele-Elmarit 90mm f/2.8`
- `Tele-Elmarit-M 90mm f/2.8` is a real subtype and a plausible future `hold` candidate, but not yet a round-1 `core`
- `fat / thin`, `country marking`, `black / silver`, `coding`, `boxed-completeness` stay below round-1 core level

## Family Overview

This family should be kept separate from:

- `Elmarit-M 90mm f/2.8`
- `Elmar 90`
- `Elmar-C 90mm f/4`
- `Macro-Elmar-M 90mm f/4`
- `Summicron 90`

The most important structural question is not whether `Tele-Elmarit 90` exists. It clearly does.  
The real question is whether round 1 should open:

1. one broad `Tele-Elmarit 90` core, or
2. separate `Tele-Elmarit` and `Tele-Elmarit-M` cores immediately.

Current evidence supports option `1`.

## Literature / Reference Base

### Source A: Leica Wiki - `90mm f/2.8 Tele-Elmarit`

Leica Wiki documents the earlier `Tele-Elmarit 90` as:

- known as `"FAT" Tele-Elmarit`
- production era `1964-1974`
- M-bayonet
- `5 / 3`
- black and silver variants
- filter system `E39 / A42`
- inscription `TELE-ELMARIT 1:2.8/90`

Reference:

- https://wiki.l-camera-forum.com/leica-wiki.en/index.php/90mm_f/2.8_Tele-Elmarit

### Source B: Leica Wiki - `90mm f/2.8 Tele-Elmarit-M`

Leica Wiki documents the later `Tele-Elmarit-M 90` as:

- known as `"THIN" Tele-Elmarit`
- production era `1974-1990`
- M-bayonet
- `4 / 4`
- Canadian / German / coded vs uncoded variants
- inscription `TELE-ELMARIT-M 1:2.8/90`

Reference:

- https://wiki.l-camera-forum.com/leica-wiki.en/index.php/90mm_f/2.8_Tele-Elmarit-M

### Interpretation

The literature does support a real internal product split:

- `Tele-Elmarit 90`
- `Tele-Elmarit-M 90`

But round-1 canonical seeding should still depend on local listing language and admin normalization usefulness, not on literature alone.

## Local Listing Evidence

Analysis base: `data/derived/results_resolved_v2.json`

Local titles filtered for:

- `90`
- `tele`
- `elmarit`

Resulting local pool:

- total useful `Tele-Elmarit 90` listings: `17`

### Local title signals

Observed local marker counts:

| Marker | Count | Note |
| --- | ---: | --- |
| explicit `Tele-Elmarit-M` | 3 | real but sparse |
| plain `Tele-Elmarit` | 14 | dominant title language |
| `(1st)` marker | 2 | weak collector labeling |
| `fat` wording | 0 | collector term not used in local titles |
| `thin` wording | 0 | collector term not used in local titles |
| `black` | 5 | finish-level signal only |
| `silver` | 0 | too sparse |
| `Canada` | 0 | not useful in current local titles |
| `Germany` | 0 | not useful in current local titles |

Representative plain titles:

- `[중고] M 90/2.8 Tele Elmarit (Black)`
- `LEICA 90mm F2.8 TELE-ELMARIT sn.2490`
- `LEICA 90mm F2.8 (1st) TELE-ELMARIT sn.2001`

Representative `-M` titles:

- `LEICA 90mm F2.8 TELE-ELMARIT-M sn.1180`
- `LEICA 90mm F2.8 TELE-ELMARIT-M sn.3429`
- `Leica 90mm F2.8 Tele Elmarit M Black`

### Market split evidence

This pool is usable for taxonomy, but weak for hard internal market splitting:

- local title labeling is present
- local price evidence is too thin / inconsistent in this subset for a confident first-pass two-core separation

That means literature alone is not enough to justify opening both internal sublines as round-1 core rows.

## Candidate Entity Expansion

## Candidate 1: `Leica Tele-Elmarit 90mm f/2.8`

### Official / literature basis

Strong.

This is a documented Leica M-bayonet product line with distinct naming and production history.

### Mechanical distinction

Strong enough for `core`.

The product inscription and optical/mechanical identity are separate from `Elmarit-M 90`.

### Optical distinction

Strong enough for `core`.

The literature identifies the earlier `Tele-Elmarit` as `5 / 3`, distinct from later `Tele-Elmarit-M`.

### Market split potential

Moderate.

The local pool is not large enough to prove internal fat/thin pricing, but it is large enough to justify a separate broad `Tele-Elmarit 90` family anchor.

### Search-intent split potential

Strong.

Users and dealers explicitly search / list:

- `Tele Elmarit 90`
- `Tele-Elmarit 90`

### Final decision

`core`

### One-line reason

`Tele-Elmarit 90` is clearly distinct from `Elmarit-M 90` and has enough title-level support to be a first-pass family anchor.

## Candidate 2: `Leica Tele-Elmarit-M 90mm f/2.8`

### Official / literature basis

Strong.

This is a real Leica line, not a cosmetic metadata variant.

### Mechanical distinction

Strong.

The literature distinguishes it from the earlier `Tele-Elmarit` with different inscription, slimmer form, and `4 / 4` design.

### Optical distinction

Strong enough to matter.

This is not merely finish or coding.

### Market split potential

Unclear in round 1.

There are only `3` explicit local titles with `Tele-Elmarit-M`, which is too thin for a confident immediate core split.

### Search-intent split potential

Real, but sparse.

If a user types the explicit `Tele-Elmarit-M` wording, the intent is clear. The issue is not conceptual clarity; it is low local repeat frequency.

### Final decision

`hold`

### One-line reason

`Tele-Elmarit-M 90` is a real and likely useful explicit subtype, but current local title support is still too sparse for round-1 core.

## Candidate 3: `fat / thin` collector-language split

### Official / literature basis

Real as collector shorthand, but not the best round-1 canonical surface.

### Mechanical distinction

Strong in reality.

### Search-intent split potential

Weak in local data.

Current local titles do not actually use `fat` or `thin`.

### Final decision

`보류`

### One-line reason

`fat / thin` is a useful collector overlay vocabulary, but local admin normalization should not make it a first-pass seed split before title language supports it.

## Overlay / Hold / Deferred Layers

Keep these below round-1 core level:

- `black / silver`
- `country marking`
- `coding`
- `boxed-completeness`

Current round-1 recommendations:

- `Tele-Elmarit-M 90` -> `hold`
- `fat / thin` wording -> `보류`
- finish / country / coding -> `overlay`

## Recommended Round-1 Core Count

**1**

Recommended immediate core candidate:

1. `Leica Tele-Elmarit 90mm f/2.8`

## What Should Still Wait

- `Leica Tele-Elmarit-M 90mm f/2.8` should not be promoted to `core` yet
- `fat / thin` should not be the public seed naming axis yet
- finish, country, and coding should stay below explicit seed level

## Can The Next Round Add Seed?

**Yes, but conservatively.**

Safe next-step seed direction:

- add `Leica Tele-Elmarit 90mm f/2.8` as the first explicit `core` row

Still premature for round-2 core:

- immediate separate `Tele-Elmarit-M 90mm f/2.8` core
- fat/thin collector split as first-pass row names

Possible future follow-up:

- a narrow `hold-seed audit` for `Tele-Elmarit-M 90mm f/2.8`
