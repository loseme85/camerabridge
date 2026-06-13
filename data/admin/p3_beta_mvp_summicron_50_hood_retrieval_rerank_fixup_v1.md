# P3 Beta MVP - Summicron 50 Hood Retrieval / Rerank Fixup v1

`decision_status = summicron_50_hood_retrieval_rerank_fixup_v1_pushed_ready_for_owner_recheck`

## Exact change

This fix adds a **narrow hood-intent supplemental retrieval path** only for explicit Summicron 50 hood queries:

- `Summicron 50 hood`
- `Leica Summicron 50 hood`
- `Summicron-M 50 hood`

What changed:

1. Detect explicit `Summicron 50` + `hood` query intent.
2. Build a narrow supplemental hood query:
   - `Leica 50mm hood`
   - or `Leica M 50mm hood` for M-mount wording
3. Pull only hood-like accessory rows from that supplemental query:
   - category `Accessory`
   - accessory type `hood`
   - or rows with hood/shade text
4. Merge those rows into the visible/evidence candidate set.
5. Re-run the existing hood-aware rerank on the original query.

What did **not** change:

- exact price unlock logic
- accessory pricing
- ranking for normal non-hood lens queries
- DR / Rigid logic
- body bundle guard
- 12585 / 12504 catalog behavior

## Before / after for primary queries

### `Summicron 50 hood`

Before:

- candidate: `Leica Summicron 50 hood candidate`
- hood intent detected
- top 12 dominated by Summicron lens rows
- no hood rows in first screen
- no hood rows even in top 60

After:

- candidate: `Leica Summicron 50 hood candidate`
- hood intent detected
- top 12 is hood/accessory-led
- hood rows appear at positions `1-12`
- price remains locked
- `used_for_price = 0`

Top rows after:

1. `Leica 12549 Hood Silver [for M 50mm f2.8 Elmar]`
2. `Leica 12475 Hood Black for M 50mm F1.2 Noctilux ASPH`
3. `[중고] Leica Lens Hood Noctilux-M 50mm f/1.2 ASPH`
4. `LEICA Lens Hood 12550 for M 50mm F2.8`
5. `신품 호환 Leica 14043 Hood Cover for M 35mm f2 Summicron, M 28mm f2.8 Elmarit`
6. `Leica 12585 Hood for M-50mm, 35mm`

### `Leica Summicron 50 hood`

Before:

- same failure pattern as `Summicron 50 hood`
- lens rows dominated first screen
- no hood rows visible in first screen

After:

- hood/accessory rows fill the first visible cluster
- price remains locked
- `used_for_price = 0`

### `Summicron-M 50 hood`

Before:

- top 12 dominated by M-mount Summicron lens rows
- no hood rows visible

After:

- hood rows appear at positions `1-6`
- lens rows move below the first hood cluster
- price remains locked
- `used_for_price = 0`

Top rows after:

1. `Leica 12549 Hood Silver [for M 50mm f2.8 Elmar]`
2. `Leica 12475 Hood Black for M 50mm F1.2 Noctilux ASPH`
3. `[중고] Leica Lens Hood Noctilux-M 50mm f/1.2 ASPH`
4. `LEICA Lens Hood 12550 for M 50mm F2.8`
5. `Leica 12585 Hood for M-50mm, 35mm`
6. `Leica XOOIM Hood For M-50mm`

## Top 12 before / after summary

| Query | Before | After |
|---|---|---|
| `Summicron 50 hood` | top 12 all lens rows | top 12 all hood/accessory rows |
| `Leica Summicron 50 hood` | top 12 all lens rows | top 12 all hood/accessory rows |
| `Summicron-M 50 hood` | top 12 mostly M-lens rows | first 6 rows are hood/accessory rows, lens rows moved later |

## Price safety confirmation

Across all three primary hood queries:

- `price_summary_allowed = False`
- no lens/body exact price unlock
- `used_for_price = 0`
- visible rows remain non-exact / boundary / not-compatible pricing evidence

This remains a retrieval/ranking polish fix only.

## Healthy hood control table

| Query | Result |
|---|---|
| `Leica 50mm hood` | PASS - healthy hood retrieval preserved |
| `Leica lens hood` | PASS - healthy hood retrieval preserved |
| `Leica 12585` | PASS - catalog-number hood rows still lead |
| `Leica 12504` | PASS - catalog-number hood rows still lead |
| `Noctilux 50 1.2 hood` | PASS - hood rows still lead |
| `Summilux 35 hood` | PASS - hood rows still lead |

## Regression safety table

| Query | Expected preserved behavior | Result |
|---|---|---|
| `Summicron 50` | normal lens query not polluted by hood rows | PASS |
| `Summicron-M 50` | normal M-lens query not polluted by hood rows | PASS |
| `50 cron dr` | DR safety unchanged | PASS |
| `Summicron-M 50 Dual Range` | DR safety unchanged | PASS |
| `Leica Summicron 50 rigid` | rigid safety unchanged | PASS |
| `Summicron-M 50 rigid` | rigid safety unchanged | PASS |
| `Summilux-M 35 FLE2` | Summilux safety unchanged | PASS |
| `Summilux-M 35` | broad Summilux safety unchanged | PASS |
| `Leica M10 lens kit` | body bundle guard unchanged | PASS |

## Remaining issues

- The new hood-first cluster is intentionally broad and compatibility-light.
- Some surfaced hood rows are generic 50mm or adjacent Leica hood rows rather than a clean Summicron-only hood family.
- This is acceptable for the current P1 goal because:
  - hood/accessory rows now surface first
  - exact price remains locked
  - no lens/body price contamination appears

If owner wants another polish round later, the next refinement would be:

- prefer Summicron-compatible hood rows above generic 50mm hood rows
- mildly demote Noctilux-specific hood rows inside Summicron hood intent
