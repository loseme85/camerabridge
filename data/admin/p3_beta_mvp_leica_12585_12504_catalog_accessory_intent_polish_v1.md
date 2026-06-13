# P3 Beta MVP Leica 12585 / 12504 Catalog Accessory Intent Polish v1

## Decision Status

`leica_12585_12504_catalog_accessory_intent_polish_v1_pushed_ready_for_owner_recheck`

## Exact Changes

- Added a very small query-side recovery for known Leica hood catalog codes:
  - `12585`
  - `12504`
- In those cases, the parser now recovers:
  - `accessory_intent = hood`
  - `accessory_code = 12585` or `12504`
- Added accessory-aware interpreted-target text so hood/accessory queries no longer default to broad `Leica lens candidate`.
- Added a narrow relevance rerank for `hood` intent queries:
  - exact catalog-number hood rows first
  - accessory/hood rows ahead of generic lens rows
  - no price-scope changes

## Before / After — 12585 / 12504

| query | before candidate | after candidate | before first screen | after first screen | result |
| --- | --- | --- | --- | --- | --- |
| `Leica 12585` | `Leica lens candidate` | `Leica 12585 hood candidate` | generic Leica lens rows | exact `12585` hood rows lead | PASS |
| `12585` | `Leica lens candidate` | `Leica 12585 hood candidate` | no useful visible result set | exact `12585` hood rows lead | PASS |
| `12585 hood` | `Leica lens candidate` | `Leica 12585 hood candidate` | hood rows visible, but broad label | hood rows visible with hood-specific label | PASS |
| `Leica hood 12585` | `Leica lens candidate` | `Leica 12585 hood candidate` | hood rows visible, but broad label | hood rows visible with hood-specific label | PASS |
| `Leica 12504` | `Leica lens candidate` | `Leica 12504 hood candidate` | generic Leica lens rows | exact `12504` hood rows lead | PASS |
| `12504` | `Leica lens candidate` | `Leica 12504 hood candidate` | weak/broad lens-like interpretation | `12504` hood rows lead | PASS |
| `12504 hood` | `Leica lens candidate` | `Leica 12504 hood candidate` | hood rows visible, but broad label | hood rows visible with hood-specific label | PASS |
| `Leica 12504 hood` | `Leica lens candidate` | `Leica 12504 hood candidate` | hood rows visible, but broad label | hood rows visible with hood-specific label | PASS |

## Candidate Label Before / After

### Catalog-number hood queries

- `Leica 12585`
  - before: `Leica lens candidate`
  - after: `Leica 12585 hood candidate`
- `12585`
  - before: `Leica lens candidate`
  - after: `Leica 12585 hood candidate`
- `Leica 12504`
  - before: `Leica lens candidate`
  - after: `Leica 12504 hood candidate`
- `12504`
  - before: `Leica lens candidate`
  - after: `Leica 12504 hood candidate`

### Related hood controls

- `Leica lens hood` -> `Leica hood candidate`
- `Leica 35mm hood` -> `Leica 35 hood candidate`
- `Leica 50mm hood` -> `Leica 50 hood candidate`
- `Leica Summicron hood` -> `Leica Summicron hood candidate`
- `Summicron 50 hood` -> `Leica Summicron 50 hood candidate`
- `Summilux 35 hood` -> `Leica Summilux 35 hood candidate`
- `Noctilux 50 1.2 hood` -> `Leica Noctilux 50 f1.2 hood candidate`

## First-Screen Ranking Observations

### 12585

After the polish, these now lead the first visible cluster:

- `Leica 12585 Hood for M-50mm, 35mm`
- `[중고] Leica 12585 후드`
- `LEICA 12585 HOOD`

Generic Leica lens rows no longer dominate the first screen.

### 12504

After the polish, these now lead the first visible cluster:

- `[중고] Leica 12504 후드`
- `Light Lens Lab 12504 Hood Black for M-35mm [Aluminium]`
- `LEICA 35mm F1.4 SUMMILUX 12504 Hood sn.2548`
- `LEICA 12504 HOOD`

### Related hood controls

- `Leica lens hood`: good accessory-first first screen
- `Leica 35mm hood`: good hood/accessory-first first screen
- `Leica 50mm hood`: good hood/accessory-first first screen
- `Leica Summicron hood`: good hood/accessory-first first screen
- `Summilux 35 hood`: improved label and hood rows at top
- `Noctilux 50 1.2 hood`: improved label and hood rows pinned at top
- `Summicron 50 hood`: still weak
  - candidate label is now correct
  - but top 40 local results did not surface explicit hood rows
  - this remains ranking / candidate-pool polish, not a price-safety issue

## Price Safety Confirmation

For all audited catalog-number / hood queries in this round:

- exact lens/body price unlocked: `No`
- visible lens/body rows used for price: `0`
- accessory queries remain locked / reference-only / insufficient exact data
- no lens/body exact price contamination was introduced

## Regression Safety Table

| query | expected safety | observed result |
| --- | --- | --- |
| `Summilux-M 35` | broad mixed price remains locked | PASS |
| `Summilux-M 35 2매` | AA candidate remains conservative | PASS |
| `Summilux-M 35 FLE2` | FLE2 exact scope remains intact | PASS |
| `50 cron dr` | DR rows remain safe | PASS |
| `Leica Summicron 50 rigid` | rigid mixed-mount guard remains intact | PASS |
| `Leica M10 lens kit` | body-bundle guard remains active | PASS |

## Remaining Issues

1. `Summicron 50 hood`
   - candidate label is improved
   - first-screen ranking is still weak because explicit hood rows did not surface in the local candidate pool
   - severity: `P1`

2. broader hood/accessory ranking polish
   - some family-specific hood searches still show lens-family rows earlier than ideal after the first hood rows
   - severity: `P1`

## Validation Notes

- `python3 -m py_compile query_parser.py search_service.py query_resolver.py api/search.py` passed
- primary validation passed for:
  - `Leica 12585`
  - `12585`
  - `12585 hood`
  - `Leica hood 12585`
  - `Leica 12504`
  - `12504`
  - `12504 hood`
  - `Leica 12504 hood`
- related hood controls remained price-safe
- regression safety controls remained intact
