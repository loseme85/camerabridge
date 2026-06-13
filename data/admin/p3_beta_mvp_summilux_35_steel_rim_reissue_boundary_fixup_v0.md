# P3 Beta MVP Summilux 35 Steel Rim / Reissue Boundary Fixup v0

`decision_status = p3_beta_mvp_summilux_35_steel_rim_reissue_boundary_fixup_completed_ready_for_owner_review`

## Files changed
- `/Users/changdaepark/Desktop/LEICA SEARCH/query_parser.py`
- `/Users/changdaepark/Desktop/LEICA SEARCH/api/search.py`
- `/Users/changdaepark/Desktop/LEICA SEARCH/data/admin/p3_beta_mvp_summilux_35_steel_rim_reissue_boundary_fixup_v0.md`

## Exact change summary
1. Added narrow query-side hint recovery for strong `Summilux 35` context:
   - `Steel Rim` -> variant `Steel Rim`
   - `reissue` / `복각` -> variant `Reissue`

2. Added narrow query/result variant boundary for price-scope matching:
   - `Steel Rim` exact matching now excludes rows that are explicitly `reissue` / `복각`
   - `Reissue` exact matching requires explicit reissue text

This keeps the fix tightly scoped to Steel Rim / reissue intent without reopening AA / FLE / DR / body-lens paths.

## Before / after

### `Summilux-M 35 Steel Rim`
Before:
- Interpreted as: `Leica Summilux-M 35 candidate`
- `price_summary_allowed = True`
- `price_scope = exact_base_model`
- `exact_variant_pool_count = 0`
- broad same-base Summilux-M 35 pricing unlocked

After:
- Interpreted as: `Leica Summilux-M 35 Steel Rim candidate`
- `variant_tokens_detected = ['Steel Rim']`
- `price_summary_allowed = False`
- `price_scope = insufficient_exact_data`
- `exact_variant_pool_count = 6`
- broad same-base exact-base-model unlock no longer occurs

Top 5 after:
1. `Leica M 35mm f1.4 Summilux 1st Silver [Steel Rim]`
2. `신품 Leica M 35mm f1.4 Summilux Black 스틸림 복각`
3. `[중고] M 35/1.4 Summilux (스틸림 복각)`
4. `[위탁] M 35/1.4 Summilux (스틸림 복각)`
5. `[위탁] M 35/1.4 Summilux Steel Rim`

### `Summilux 35 Steel Rim`
Before:
- Interpreted as: `Leica Summilux 35 candidate`
- no Steel Rim variant signal
- Steel Rim row visible, but broad query remained under-modeled

After:
- Interpreted as: `Leica Summilux 35 Steel Rim candidate`
- `variant_tokens_detected = ['Steel Rim']`
- `price_summary_allowed = False`
- `price_scope = insufficient_exact_data`
- Steel Rim / Steel Rim-adjacent rows dominate the first screen

Top 5 after:
1. `Leica M 35mm f1.4 Summilux 1st Silver [Steel Rim]`
2. `신품 Leica M 35mm f1.4 Summilux Black 스틸림 복각`
3. `[중고] M 35/1.4 Summilux (스틸림 복각)`
4. `[위탁] M 35/1.4 Summilux (스틸림 복각)`
5. `[위탁] M 35/1.4 Summilux Steel Rim`

### `Summilux 35 reissue`
Before:
- Interpreted as: `Leica Summilux 35 candidate`
- explicit reissue row existed but ranked low
- no reissue-specific intent was modeled

After:
- Interpreted as: `Leica Summilux 35 Reissue candidate`
- `variant_tokens_detected = ['Reissue']`
- `price_summary_allowed = True`
- `price_scope = exact_variant`
- `exact_variant_pool_count = 3`

Top 5 after:
1. `LEICA 35mm F1.4 SUMMILUX-M Steel Rim Reissue sn.4917`
2. `LEICA 35mm F1.4 SUMMILUX-M Steel Rim Reissue sn.4838`
3. `Leica M 35mm f1.4 Summilux 2nd Titan`
4. `Leica M 35mm f1.4 Summilux 1st Silver [Steel Rim]`
5. `Leica M 35mm f1.4 Summilux ASPH 4th Titan`

## Price-scope safety result

### Main fix target
- `Summilux-M 35 Steel Rim`
  - PASS
  - broad same-base exact price unlock is blocked
  - query now requires Steel Rim-compatible exact evidence

### Steel Rim family
- `Summilux 35 Steel Rim`
- `Leica Summilux 35 Steel Rim`
  - PASS
  - no broad same-base exact-base-model unlock
  - both remain locked because exact Steel Rim evidence is still not strong enough

### Reissue family
- `Summilux 35 reissue`
- `Leica Summilux 35 reissue`
  - PASS
  - no fallback to broad same-base candidate
  - current runtime reports a clean exact-variant reissue pool of 3

## Top-result ranking result

### Improved
- `Summilux 35 Steel Rim`
- `Leica Summilux 35 Steel Rim`
- `Summilux-M 35 Steel Rim`
- `Summilux 35 reissue`
- `Leica Summilux 35 reissue`

all now show Steel Rim / reissue-relevant rows at the top instead of broad 2nd/ASPH first.

### Still slightly broad
- `Summilux 35 Steel Rim` still shows reissue rows high in the visible stack because they are Steel Rim-related titles.
- This no longer causes the original unsafe broad exact-base-model unlock for `Summilux-M 35 Steel Rim`.

## Regression table

| Query | Status | Observation |
|---|---|---|
| `Summilux 35 1st` | PASS | Interpreted target unchanged; 1st-gen rows remain top |
| `Summilux 35 silver` | PASS | Silver path unchanged |
| `Summilux 35 2nd` | PASS | 2nd-gen path unchanged |
| `Summilux 35 2매` | PASS | AA candidate preserved |
| `Summilux-M 35 2매` | PASS | AA candidate preserved |
| `35 lux 2mae` | PASS | AA candidate preserved |
| `M35 1.4 2매` | PASS | AA candidate preserved |
| `Summilux 35 FLE` | PASS | FLE path preserved |
| `Summilux 35 FLE2` | PASS | FLE2 path preserved |
| `Summicron 50 DR` | PASS | DR path preserved |
| `Summicron 50 Rigid` | PASS | Rigid guard path preserved |
| `Leica M body` | PASS | Body intent preserved |
| `Leica 35mm lens` | PASS | lens-category ranking preserved |

## Remaining weak-pass items
- `Summilux 35 Steel Rim` still surfaces reissue rows high in the first visible group because their titles explicitly contain Steel Rim language.
- `Summilux 35 1st silver steel rim` now interprets as `Steel Rim / Silver / 1st candidate`, which is useful, but the exact pool remains small and price stays locked.
- `Summilux 35 reissue` currently reaches `exact_variant` with a small exact pool (`3`). That appears acceptable in local runtime, but should still get latest-preview owner validation before closing.

## Verification
- `python3 -m py_compile query_parser.py search_service.py query_resolver.py api/search.py`
- targeted local smoke:
  - `Summilux 35 Steel Rim`
  - `Leica Summilux 35 Steel Rim`
  - `Summilux-M 35 Steel Rim`
  - `Summilux 35 reissue`
  - `Leica Summilux 35 reissue`
  - `Summilux 35 1st silver steel rim`
  - `Summilux 35 1st`
  - `Summilux 35 silver`
  - `Summilux 35 2nd`
  - `Summilux 35 2매`
  - `Summilux-M 35 2매`
  - `35 lux 2mae`
  - `M35 1.4 2매`
  - `Summilux 35 FLE`
  - `Summilux 35 FLE2`
  - `Summicron 50 DR`
  - `Summicron 50 Rigid`
  - `Leica M body`
  - `Leica 35mm lens`

## Commit / push
- Not performed
- Repo contains unrelated dirty files

## Proposed commit message
- `fix: guard Summilux 35 Steel Rim and reissue intent`
