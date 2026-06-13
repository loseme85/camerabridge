# P3 Beta MVP Body/Lens Category Separation Follow-up v0

`decision_status = p3_beta_mvp_body_lens_category_separation_followup_completed_ready_for_owner_review`

Canonical preview reference from prior owner testing:
- [camerabridge-l1s6c33ya-camerabridge.vercel.app](https://camerabridge-l1s6c33ya-camerabridge.vercel.app/)

## Files changed
- `/Users/changdaepark/Desktop/LEICA SEARCH/query_parser.py`
- `/Users/changdaepark/Desktop/LEICA SEARCH/search_service.py`
- `/Users/changdaepark/Desktop/LEICA SEARCH/query_resolver.py`
- `/Users/changdaepark/Desktop/LEICA SEARCH/api/search.py`

## Scope
Narrow follow-up only:
- recover generic `Leica M body` / `Leica M camera` body intent
- demote accessory rows for explicit generic `... lens` queries such as `Leica 35mm lens`

Not touched:
- Summilux 35 AA / 2mae
- Summilux 35 FLE / FLE2
- Summicron 50 DR / Rigid exact-price guards
- UI layout / sticky search / Load more

## Exact change summary
1. Added narrow parser recovery for strong `M body` / `M camera` phrasing:
   - `Leica M body`
   - `Leica M camera`
   now set `body_intent = "M"` and keep `mount = "M"`.

2. Added narrow generic M-body text matching in search scoring/candidate narrowing:
   - lets `M3`, `M6`, `M11`, `MP`, `MA`, etc. count as valid generic Leica M body results
   - prevents `Leica M body` from falling back to `M-mount lens candidate`

3. Added narrow relevance rerank for explicit generic `... lens` queries:
   - when query contains `lens`
   - and is not an accessory/body query
   - actual Lens rows are promoted ahead of Accessory rows
   - keeps `Leica 35mm hood` unchanged

## Before / after

### `Leica M body`
Before:
- Interpreted as: `Leica M-mount lens candidate`
- Category: `Lens`
- Top results: Leica M lenses
- Price path: broad same-base lens fallback

After:
- Interpreted as: `Leica M body`
- Category: `Body`
- `price_summary_allowed = false`
- visible `used_for_price = 0`
- Top 3:
  1. `Leica M3 Silver`
  2. `Leica M11 Glossy Black Paint Finish`
  3. `Leica M6 Classic Silver x0.72 [Big Logo]`

Result:
- body intent now routes to body rows
- no M-mount lens fallback dominates first screen

### `Leica 35mm lens`
Before:
- Interpreted as: `Leica lens 35 candidate`
- Category: `Lens`
- Top result contamination included accessory hood rows
- First result:
  - `신품 호환 Leica 14043 Hood Cover for M 35mm f2 Summicron, M 28mm f2.8 Elmarit`

After:
- Interpreted as: `Leica lens 35 candidate`
- Category remains `Lens`
- `price_summary_allowed = false`
- visible `used_for_price = 0`
- Top 3:
  1. `Leica M 35mm f3.5 Summaron Silver`
  2. `Leica M 35mm f1.4 Summilux 2nd Titan`
  3. `Leica L 35mm f3.5 Elmar Silver`

Result:
- actual 35mm Leica lenses now outrank hood/accessory rows
- broad price stays conservative

## Targeted validation table

| Query | Result | Notes |
|---|---|---|
| `Leica M body` | PASS | Body intent recovered; top results are bodies |
| `Leica M camera` | PASS | Same body-intent recovery as `Leica M body` |
| `Leica M lens` | PASS | Still resolves to `Leica M-mount lens candidate` |
| `Leica 35mm lens` | PASS | Lens rows promoted above accessory rows |
| `Leica 35mm hood` | PASS | Accessory hood intent unchanged |
| `Leica M6` | PASS | Stable body behavior |
| `Leica M3` | PASS | Stable body behavior |
| `Leica IIIf` | PASS | Stable body behavior |
| `Barnack IIIf` | PASS | Stable body behavior |
| `Leica Q2` | PASS | Stable body behavior |
| `Leica Q3` | PASS | Stable body behavior |
| `Leica 35mm Summicron` | WEAK_PASS | Still broad lens-family query; accessory-first noise can remain |
| `Leica 35mm Summilux` | PASS | Top rows remain lenses |

## Regression checks: recent boundary work

| Query | Status | Observation |
|---|---|---|
| `Summilux-M 35 2매` | PASS | `Leica Summilux-M 35 AA candidate` preserved |
| `Summilux 35 2매` | PASS | `Leica Summilux 35 AA candidate` preserved |
| `35 lux 2mae` | PASS | `Leica Summilux 35 AA candidate` preserved |
| `M35 1.4 2매` | PASS | `Leica Summilux-M 35 f1.4 AA candidate` preserved |
| `Summilux-M 35 3rd gen 2mae` | PASS | `Leica Summilux-M 35 AA / 3rd candidate` preserved |
| `Summicron 50 DR` | PASS | `Leica Summicron 50 Dual Range candidate`; DR rows still top |
| `Summicron 50 Rigid` | PASS | Existing conservative rigid behavior unchanged |

## Remaining risks / weak-pass items
- `Leica 35mm Summicron` can still surface accessory noise because this follow-up only reranks explicit generic `... lens` wording.
- `Summicron 50 Rigid` bare query still surfaces L-side rigid rows first in the current local ranking path, but the previously closed mixed-mount exact-price guard remains intact and no unsafe exact unlock was observed here.

## Verification run
- `python3 -m py_compile query_parser.py search_service.py query_resolver.py api/search.py`
- targeted local query smoke via `api.search.endpoint_response(...)`

## Commit / push
- Not performed.
- Repo contains unrelated dirty files, so this round should stay uncommitted unless the owner explicitly asks for a scoped cleanup/publish step.
