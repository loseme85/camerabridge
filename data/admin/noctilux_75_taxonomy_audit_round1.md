# Noctilux 75 Taxonomy Audit - Round 1

Date: 2026-05-01

Scope: read-heavy taxonomy audit for the Leica `Noctilux 75` family. This round does not add seed rows, does not change classifier/query/search behavior, and does not change admin lookup ranking or UI. The goal is to determine whether `Noctilux 75` is mature enough for explicit canonical seeding and, if so, at what granularity.

## Executive Summary

`Noctilux 75` is one of the cleanest Leica lens families audited so far.

The strongest and most practical round-1 structure is:

1. `Leica Noctilux-M 75mm f/1.25 ASPH`

Current evidence does **not** support opening internal split rows.

Round-1 conclusion:

- immediate recommended `core` candidate count: `1`
- recommended first-pass core:
  - `Leica Noctilux-M 75mm f/1.25 ASPH`
- `6bit` is highly visible but behaves as standard metadata, not as a separate canonical entity
- `black / silver / country marking / special edition / anniversary / titanium / boxed completeness` stay below round-1 row level
- `SL 75` and other non-Noctilux 75 contamination should be excluded entirely

## Family Overview

Unlike many Leica families that need strong historical splitting, `Noctilux 75` currently behaves like a single modern Leica M line.

The main contamination to exclude is:

- `Summilux 75`
- `Summicron 75`
- `SL 75`
- non-Leica 75mm fast portrait lenses

After excluding those, the useful pool is almost entirely one product concept:

- `Noctilux-M 75mm f/1.25 ASPH`

That makes the round-1 taxonomic question simple:

- is there any evidence for a real internal split?

Current answer: `not yet`.

## Literature / Reference Base

### Source A: Leica Wiki / Leica official line identity

The line is documented as:

- `Noctilux-M 75mm f/1.25 ASPH`
- Leica M bayonet
- order number `11676`
- `9 / 6`
- filter size `E67`
- integrated hood

References:

- https://leica-camera.com/en-US/photography/lenses/m/noctilux-m-75-f1-25-asph/technical-specification
- https://leica-camera.com/en-US/photography/lenses/m/noctilux-m-75-f1-25-asph/discover

### Interpretation

The literature supports a single modern Leica M line with stable naming.

There is no strong published evidence in the current audit context for:

- major generation split
- optical redesign split
- collector-era early/late split comparable to older Leica families

So literature already points toward a broad single-line family.

## Local Listing Evidence

Analysis base: `data/derived/results_resolved_v2.json`

Strict local filtering for `75` + `Noctilux` yields:

- useful `Noctilux 75` listings: `11`

All usable examples point to the same line:

- `Leica M 75mm f1.25 Noctilux ASPH 6bit Black`
- `[중고] M 75/1.25 Noctilux ASPH 6bit (Black)`
- `LEICA 75mm F1.25 ASPH NOCTILUX-M sn.4710`

### Local marker counts

| Marker | Count | Note |
| --- | ---: | --- |
| `6bit` | 9 | highly repeated, but standard metadata-like |
| `black` | 9 | finish-level only |
| `silver` | 0 | no evidence |
| `germany` | 0 | no evidence |
| `canada` | 0 | no evidence |
| `special / limited / anniversary` | 0 | no evidence |
| `titanium` | 0 | no evidence |

### Price clustering

All priced local records fall into one tight market band:

- `14.5M`
- `14.6M`
- `14.8M`
- `15.5M`
- `15.8M`

This is exactly the kind of pattern we want when recommending a single first-pass core row.

### Interpretation

The local evidence strongly supports:

1. one product line
2. one price cluster
3. no visible internal canonical split

This is one of the clearest “single-line family” cases in the current seed program.

## Candidate Entity Expansion

## Candidate 1: `Leica Noctilux-M 75mm f/1.25 ASPH`

### Official / literature basis

Very strong.

The lens is documented by Leica as a single current product line with stable naming and technical identity.

### Mechanical distinction

Strong enough for `core`.

The line has a coherent physical identity:

- Leica M mount
- integrated hood
- large modern portrait-lens form factor

### Optical distinction

Strong enough for `core`.

It is a unique Leica M 75 portrait line and not a cosmetic subvariant of another 75mm family.

### Market split potential

Strong.

The local pool forms a single tight premium cluster.

### Search-intent split potential

Strong.

Users and dealers clearly search/list:

- `M 75/1.25 Noctilux ASPH`
- `Noctilux-M 75`
- `75mm F1.25 Noctilux-M`

### Final decision

`core`

### One-line reason

`Noctilux-M 75mm f/1.25 ASPH` is a clean, modern Leica M single-line family with strong literature identity and no meaningful round-1 split pressure.

## Candidate 2: `6bit`

### Official / literature basis

Real as coding metadata.

### Mechanical distinction

Weak as a canonical entity split.

### Market split potential

Weak.

`6bit` appears often, but not as a separate pricing or intent cluster.

### Search-intent split potential

Moderate but metadata-like.

### Final decision

`overlay`

### One-line reason

`6bit` is common enough to track, but too ordinary and too non-separating to justify its own row.

## Candidate 3: finish / special edition / anniversary / titanium / country

### Official / literature basis

Insufficient in the current local context.

### Search-intent split potential

Weak.

No repeating local signal supports row-level splitting here.

### Final decision

`overlay` or `보류`

### One-line reason

These axes are either absent or too weak in the current local dataset to justify any round-1 split.

## Recommended Round-1 Core Count

**1**

Recommended immediate core candidate:

1. `Leica Noctilux-M 75mm f/1.25 ASPH`

## What Should Still Wait

- any `6bit` row
- any finish-only row
- any anniversary / special-edition row
- any country-based row

## Can The Next Round Add Seed?

**Yes.**

The safe next-step seed direction is:

- add `Leica Noctilux-M 75mm f/1.25 ASPH` as a single explicit `core` row

It should **not** add:

- a separate `6bit` row
- finish / country / special-edition rows
- any artificial internal split without new evidence
