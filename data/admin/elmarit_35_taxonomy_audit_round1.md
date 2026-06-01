# Elmarit 35 Taxonomy Audit - Round 1

Date: 2026-05-01

Scope: read-heavy taxonomy audit for the Leica `Elmarit 35` family. This round does not add seed rows, does not change classifier/query/search behavior, and does not change admin lookup ranking or UI. The goal is to determine whether `Elmarit 35` is mature enough for explicit canonical seeding and, if so, at what granularity.

## Executive Summary

`Elmarit 35` is **not ready** for explicit seed addition in round 1.

The central problem is not literature ambiguity. It is local evidence quality:

- the local usable pool is effectively absent for Leica M-side `Elmarit 35`
- observed matches are almost entirely contamination from `Elmarit-R 35` or accessories
- there is not enough real local title language to support even a conservative first-pass `core`

Round-1 conclusion:

- immediate recommended `core` candidate count: `0`
- do **not** add `Elmarit 35` seed rows yet
- keep the family in audit state until real M-side listing support appears

## Family Overview

In Leica literature, `35mm Elmarit` is a meaningful historical area with real optical and mechanical evolution.  
In the current local data, however, almost none of that structure is visible in a usable way for admin normalization.

The contamination problem is severe:

- `Elmarit-R 35`
- accessory titles referencing `M 28 Elmarit` or `M 35` hoods
- non-M Leica systems
- non-Leica 35mm listings with stray `Elmarit` text

So the round-1 question is not “which split is right?”  
It is “is there enough real local M-side `Elmarit 35` evidence to seed anything at all?”

Current answer: `no`.

## Literature / Reference Base

The Leica historical literature does support real distinctions such as:

- pre-ASPH versus ASPH
- version / barrel / filter-size changes
- country and coding differences

However, for this audit those literature distinctions are not enough by themselves.  
A seed candidate also needs local title support or market clustering strong enough to make the canonical row operationally useful.

In round 1, that second half is missing.

## Local Listing Evidence

Analysis base: `data/derived/results_resolved_v2.json`

Strict local filtering for:

- `35`
- `elmarit`

produced only `2` usable hits:

1. `신품 호환 Leica 14043 Hood Cover for M 35mm f2 Summicron, M 28mm f2.8 Elmarit`
2. `LEICA R6.2 35mm F2.8 ELMARIT-R sn.1923`

### Interpretation

These are not seedable M-family evidence:

- item 1 is accessory contamination
- item 2 is `Elmarit-R 35`, not `Elmarit 35` in the M-family sense relevant here

That means the current local usable pool for Leica M-side `Elmarit 35` is effectively:

- `0`

This is a much weaker local basis than the families that have already been seeded.

## Candidate Entity Expansion

## Candidate 1: broad `Leica Elmarit-M 35mm`

### Official / literature basis

Potentially real in history, but not actionable in current local data.

### Mechanical distinction

Would matter if the titles existed locally. They currently do not.

### Optical distinction

Potentially meaningful, but not enough without local market support.

### Market split potential

Unproven in the current dataset.

### Search-intent split potential

Weak in current local evidence.

There is no repeated local dealer wording showing that users/sellers are actually surfacing this family in operational titles.

### Final decision

`보류`

### One-line reason

The family may be real in Leica history, but the local title pool is too empty and too contaminated to justify even a broad first-pass row.

## Candidate 2: pre-ASPH / ASPH split

### Official / literature basis

Potentially real.

### Local title support

Absent.

### Market split potential

Unobservable in current local evidence.

### Final decision

`보류`

### One-line reason

Without local M-side titles, even a literature-real split should not be promoted.

## Candidate 3: filter size / hood / barrel / coding / country marking splits

### Official / literature basis

These may matter historically, but they are even less justified than the broad family row under current data conditions.

### Final decision

`보류`

### One-line reason

Collector- and metadata-level splitting is out of scope when the base family itself is not locally supported.

## Recommended Round-1 Core Count

**0**

No explicit round-1 `core` seed candidate is recommended.

## What Should Still Wait

- any broad `Elmarit 35` row
- any pre-ASPH / ASPH split
- any country / coding / filter-size / hood / barrel split

## Can The Next Round Add Seed?

**Not yet.**

Before seed addition, at least one of the following needs to improve:

1. more real local M-side `Elmarit 35` listings
2. cleaner title language that distinguishes M-side `Elmarit 35` from R/accessory contamination
3. clearer market clustering on real `Elmarit 35` titles

## Bottom Line

`Elmarit 35` is not failing because the Leica literature is weak.  
It is failing because the current local evidence is too sparse and too contaminated to support responsible seeding.

Round-1 recommendation:

- keep `Elmarit 35` in audit state
- do not open seed rows yet
