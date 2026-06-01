# Summaron 28 Hold-Seed Audit - Round 2

Date: 2026-05-08

Scope: narrow hold-seed audit for the Leica `Summaron 28` family. This round does not add seed rows, does not change classifier/query/search behavior, and does not change admin lookup ranking or UI. The goal is to determine whether the two round-1 `hold` candidates are stable enough to become explicit `hold` rows in a future seed round.

## Executive Summary

Round-1 correctly concluded that broad `Summaron 28` should **not** be opened as a generic `core` row.

Round-2 conclusion:

- add hold row for modern reissue candidate: `yes`
- add hold row for original screw-thread / LTM candidate: `yes`
- broad generic `Summaron 28` core: `no`
- generic `summaron 28` query should **not** be forced into either hold row

Recommended future `hold` rows:

1. `Leica Summaron-M 28mm f/5.6`
2. `Leica Summaron 28mm f/5.6 original screw-thread / LTM`

That is the cleanest way to preserve real line structure without polluting broad generic `Summaron 28` intent.

## Round-1 Recap

Round-1 found:

- immediate `core` candidates: `0`
- broad `Summaron 28` pool was mixed
- two real literature-backed sub-lines were visible:
  - modern `Summaron-M 28mm f/5.6`
  - original screw-thread / `LTM` `Summaron 28mm f/5.6`

Round-1 local evidence:

- broad clean pool: `67`
- broad priced pool: `42`
- broad median: ~`3.05M KRW`
- modern `M / 6bit / 복각 / 신형` subgroup:
  - count `43`
  - priced `24`
  - median ~`2.89M KRW`
- original `L / LTM / 오리지날` subgroup:
  - count `15`
  - priced `14`
  - median ~`3.64M KRW`

The big question for round-2 is whether these two sub-lines can be safely captured as explicit `hold` rows without forcing broad `summaron 28` queries into one side.

## Literature Baseline

The literature remains clear:

- Leica’s official pages and 2016 press release support `Summaron-M 28mm f/5.6` as the modern reissue line
- Leica Wiki supports the original `Summaron f= 2.8 cm 1:5.6` screw-thread line from `1955-1963`

So the question is not whether the split is real. The question is whether the local title language is operationally strong enough for hold-seed use.

## Local Evidence Refresh

### Generic / broad wording

Generic-looking `Summaron 28` titles still mix both families:

- `Leica M 28mm f5.6 Summaron 6bit Silver 신형`
- `Leica L 28mm f5.6 Summaron Silver`
- `LEICA 28mm F5.6 SUMMARON-M sn.4651`
- `LEICA 28mm F5.6 Summaron sn.1325`

Local broad/generic bucket:

- count `37`
- priced `15`
- median ~`2.80M KRW`

This is exactly why generic `summaron 28` should not be pinned to a hold row.

### Modern reissue explicit wording

Repeated local modern markers:

- `Summaron-M`
- `M 28/5.6 Summaron`
- `6bit`
- `복각`
- `신형`

Examples:

- `Leica M 28mm f5.6 Summaron 6bit Silver 신형`
- `[중고] M 28/5.6 Summaron 6bit 복각 (Silver)`
- `[위탁] M 28/5.6 Summaron 6bit (Silver) 복각`
- `LEICA 28mm F5.6 SUMMARON-M sn.4790`

Modern explicit subgroup:

- count `43`
- priced `24`
- median ~`2.89M KRW`

### Original screw-thread / LTM explicit wording

Repeated local original markers:

- `L 28/5.6 Summaron`
- `LTM`
- `오리지날`

Examples:

- `[중고] L 28/5.6 Summaron (Silver)`
- `[위탁] L 28/5.6 Summaron (Silver)`
- `[중고] L 28/5.6 Summaron 오리지날 (Silver)`
- `LEICA 28mm F5.6 + LTM Summaron sn.1412`

Original explicit subgroup:

- count `15`
- priced `14`
- median ~`3.64M KRW`

## Candidate 1: modern reissue `Leica Summaron-M 28mm f/5.6`

### Official / literature basis

Strong.

This is a clean official Leica line with stable product naming.

### Mechanical / structural distinction

Strong.

It is the modern M-bayonet reissue line, typically signaled locally by:

- `Summaron-M`
- `M 28/5.6`
- `6bit`
- `복각`
- `신형`

### Search-intent split potential

Good enough for `hold`.

Queries like:

- `summaron-m 28`
- `m 28/5.6 summaron`
- `summaron 28 6bit`
- `summaron 28 복각`
- `summaron 28 신형`
- `28mm f5.6 summaron-m`

look narrow enough to represent an explicit reissue intent.

### Canonical naming risk

Manageable.

The important point is that `6bit`, `복각`, and `신형` should **not** become the canonical name.

The safest canonical name is the official Leica line name:

- `Leica Summaron-M 28mm f/5.6`

and local market shorthand should stay in aliases.

### Broad-query risk

High if used too broadly.

Generic:

- `summaron 28`
- `28 summaron`
- `28mm f5.6 summaron`

still mix original and reissue. So this future hold row must only match when explicit modern wording is present.

### Verdict

`hold seed possible: yes`

### Recommended hold canonical name

- `Leica Summaron-M 28mm f/5.6`

### Recommended safe aliases

- `summaron-m 28`
- `28mm f5.6 summaron-m`
- `m 28/5.6 summaron`
- `summaron 28 복각`
- `summaron 28 신형`

## Candidate 2: original screw-thread / LTM `Summaron 28mm f/5.6`

### Official / literature basis

Strong.

This is a real historical line, not a market fiction.

### Mechanical / structural distinction

Strong.

The original line is signaled locally by:

- `L 28/5.6`
- `LTM`
- `오리지날`
- sometimes `original`

### Search-intent split potential

Good enough for `hold`.

Queries like:

- `summaron 28 ltm`
- `summaron 28 original`
- `summaron 28 오리지날`
- `summaron 28 vintage`
- `l 28/5.6 summaron`
- `ltm 28/5.6 summaron`

look much narrower than broad `summaron 28`.

### Canonical naming risk

Important and nontrivial.

Using only:

- `Leica Summaron 28mm f/5.6`

would be too ambiguous, because the local market also uses `Summaron 28mm f/5.6` wording for the reissue side unless `M` is explicit.

So the hold row should use a clarifying historical suffix in the canonical name.

The safest option is:

- `Leica Summaron 28mm f/5.6 original screw-thread / LTM`

That keeps the row historically legible without freezing raw seller shorthand like `오리지날` or `vintage` into the official row name.

### Broad-query risk

High if used too broadly.

Generic:

- `summaron 28`
- `28 summaron`
- `28mm f5.6 summaron`

cannot be safely forced into this row either.

### Verdict

`hold seed possible: yes`

### Recommended hold canonical name

- `Leica Summaron 28mm f/5.6 original screw-thread / LTM`

### Recommended safe aliases

- `summaron 28 ltm`
- `summaron 28 original`
- `summaron 28 오리지날`
- `summaron 28 vintage`
- `l 28/5.6 summaron`
- `ltm 28/5.6 summaron`

## Broad Generic Query Handling

Recommended treatment:

- broad `Summaron 28` core: `defer`
- generic `summaron 28` query: `do not hard-pin to a hold row`

This applies especially to:

- `summaron 28`
- `28 summaron`
- `28mm f5.6 summaron`

These generic queries still span both modern reissue and original historical intent.

## Overlay Elements

Keep these as `overlay`, not separate rows:

- `silver / black`
- `6bit`
- `finder included`
- `hood included`
- `boxed`
- `original cap`
- `original hood`
- `original box`
- `condition`
- `packaging`

Special note:

- `복각`, `신형`, `오리지날`, `vintage` are useful alias-level intent signals, but they should not become standalone canonical truth labels by themselves.

## Boundary Families

These remain out-of-family:

- `Summicron 28`
- `Summilux 28`
- `Elmarit 28`
- `Q / Q2 / Q3`
- `R 28`
- `SL` / `APO-Summicron-SL 28`
- accessories
- third-party 28mm lenses

Boundary examples:

- `summicron 28`
- `summilux 28`
- `elmarit 28`
- `q2 28`
- `q3 28`
- `apo summicron sl 28`
- `elmarit-r 28`
- `voigtlander 28`
- `zeiss 28`
- `hood 28 summaron`
- `finder 28 summaron`

## Final Recommendation

### Add hold row

- modern reissue: `yes`
- original screw-thread / LTM: `yes`

### Recommended hold canonical names

- modern reissue:
  - `Leica Summaron-M 28mm f/5.6`
- original LTM:
  - `Leica Summaron 28mm f/5.6 original screw-thread / LTM`

### Broad core

- `no` / `defer`

### Generic query

- seed hard-pinning: `forbid`

### Next step

- future hold row addition: `allowed`

The next safe round would be a very narrow seed round that adds:

1. `Leica Summaron-M 28mm f/5.6` as `hold`
2. `Leica Summaron 28mm f/5.6 original screw-thread / LTM` as `hold`

while keeping broad `Summaron 28` generic intent unresolved.
