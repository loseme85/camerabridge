# P3 Beta MVP Summilux 35 FLE / FLE2 Ranking Confidence Follow-up v0

- decision_status: `p3_beta_mvp_summilux_35_fle_fle2_ranking_confidence_followup_completed_ready_for_owner_review`
- branch: `beta-ui-redesign-controlled-preview`
- scope: ranking-only local follow-up
- code touched in this round:
  - `api/search.py`
  - `data/admin/p3_beta_mvp_summilux_35_fle_fle2_ranking_confidence_followup_v0.md`

## Summary

This follow-up keeps the existing FLE / FLE2 parser and price-scope rules intact and adds a narrow Summilux 35 rerank only for explicit `FLE` and `FLE2` query contexts.

Result:

- bare `FLE` queries now surface FLE1 / non-FLE2 rows first
- explicit `FLE2` queries keep FLE2 / FLE II rows pinned at the top
- price-scope behavior did not change
- no regression was reproduced in Steel Rim / reissue, AA / 2mae, DR / Rigid, or body/lens category fixes

## Files Changed

| File | Change |
| --- | --- |
| `api/search.py` | Added narrow Summilux 35 FLE/FLE2 rerank buckets inside existing relevance rerank path |
| `data/admin/p3_beta_mvp_summilux_35_fle_fle2_ranking_confidence_followup_v0.md` | This report |

## Bare FLE Before / After

### Before

Query: `Summilux 35 FLE`

- interpreted: `Leica Summilux 35 FLE candidate`
- `price_summary_allowed = False`
- `price_scope = insufficient_exact_data`
- owner-facing issue:
  - first screen leaned too heavily toward `FLE II` / `FLE2`
  - first 8 included multiple explicit `FLE II` / `FLE2` rows before ordinary FLE rows

Representative top rows before:

1. `신품 Leica M 35mm f1.4 Summilux ASPH 6bit FLE II Black`
2. `Leica M 35mm f1.4 Summilux ASPH 6bit FLE II Black`
3. `[위탁] M 35/1.4 Summilux ASPH FLE (Black)`
4. `[중고] M 35/1.4 Summilux ASPH FLE II (Black)`
5. `[중고] M 35/1.4 Summilux ASPH FLE II (Black)`
6. `[위탁] M 35/1.4 Summilux ASPH FLE2 (Black)`

### After

Query: `Summilux 35 FLE`

- interpreted: `Leica Summilux 35 FLE candidate`
- `price_summary_allowed = False`
- `price_scope = insufficient_exact_data`
- `exact_variant_pool_count = 37`
- visible `used_for_price = 0`

Top 8 after:

1. `[위탁] M 35/1.4 Summilux ASPH FLE (Black)`
2. `[위탁] M 35/1.4 Summilux ASPH 6bit FLE (Black)`
3. `[위탁] M 35/1.4 Summilux ASPH 6bit FLE (Black)`
4. `[중고] M 35/1.4 Summilux ASPH FLE (Silver)`
5. `[중고] M 35/1.4 Summilux ASPH FLE (Black)`
6. `[중고] M 35/1.4 Summilux ASPH FLE (Black)`
7. `[위탁] M 35/1.4 Summilux ASPH FLE (Black)`
8. `[중고] M 35/1.4 Summilux ASPH FLE (Black)`

Result:

- first visible cluster is now clean FLE1 / non-FLE2
- explicit `FLE2` rows remain available later as related evidence
- no broad exact-price unlock was introduced

## Explicit FLE2 Before / After

### Before

Query: `Summilux 35 FLE2`

- interpreted: `Leica Summilux 35 FLE2 candidate`
- `price_summary_allowed = True`
- `price_scope = exact_variant`
- owner-facing issue:
  - first two rows were correct FLE2
  - unrelated `2nd`, `Steel Rim`, and broad ASPH rows appeared too early

Representative top rows before:

1. `[위탁] M 35/1.4 Summilux ASPH FLE2 (Black)`
2. `[중고] M 35/1.4 Summilux ASPH 6bit FLE2 (Black)`
3. `Leica M 35mm f1.4 Summilux 2nd Titan`
4. `Leica M 35mm f1.4 Summilux 1st Silver [Steel Rim]`
5. `Leica M 35mm f1.4 Summilux ASPH 4th Titan`
6. `Leica M 35mm f1.4 Summilux 2nd Black`

### After

Query: `Summilux 35 FLE2`

- interpreted: `Leica Summilux 35 FLE2 candidate`
- `price_summary_allowed = True`
- `price_scope = exact_variant`
- `exact_variant_pool_count = 6`
- visible `used_for_price = 0`

Top 8 after:

1. `[위탁] M 35/1.4 Summilux ASPH FLE2 (Black)`
2. `[중고] M 35/1.4 Summilux ASPH 6bit FLE2 (Black)`
3. `신품 Leica M 35mm f1.4 Summilux ASPH 6bit FLE II Black`
4. `Leica M 35mm f1.4 Summilux ASPH 6bit FLE II Black`
5. `[중고] M 35/1.4 Summilux ASPH FLE II (Black)`
6. `[중고] M 35/1.4 Summilux ASPH FLE II (Black)`
7. `[위탁] M 35/1.4 Summilux ASPH FLE (Black)`
8. `Leica M 35mm f1.4 Summilux 2nd Titan`

Result:

- first visible cluster is now strongly FLE2 / FLE II
- unrelated `2nd` / `Steel Rim` rows were pushed later
- exact-price scope remained unchanged

## Price-Scope Safety

Confirmed unchanged in local validation:

| Query | interpreted | price_summary_allowed | price_scope | visible used_for_price |
| --- | --- | --- | --- | --- |
| `Summilux 35 FLE` | `Leica Summilux 35 FLE candidate` | `False` | `insufficient_exact_data` | `0` |
| `Summilux-M 35 FLE` | `Leica Summilux-M 35 FLE candidate` | `False` | `insufficient_exact_data` | `0` |
| `Summilux 35 FLE2` | `Leica Summilux 35 FLE2 candidate` | `True` | `exact_variant` | `0` |
| `Summilux-M 35 FLE2` | `Leica Summilux-M 35 FLE2 candidate` | `True` | `exact_variant` | `0` |

Conclusion:

- no new unsafe FLE/FLE2 price unlock was reproduced
- no price-scope guard behavior changed in this round

## Query Results

| Query | Status | Notes |
| --- | --- | --- |
| `Summilux 35 FLE` | PASS | FLE1 rows now lead the first screen; locked price unchanged |
| `Summilux-M 35 FLE` | PASS | Same improvement as mount-unspecified FLE |
| `Leica Summilux 35 FLE` | PASS | Same improvement as bare FLE |
| `Leica Summilux-M 35 FLE` | PASS | Same improvement as M FLE |
| `Summilux 35 FLE2` | WEAK_PASS | FLE2 / FLE II rows are pinned at top; one unrelated `2nd` row still appears later in top 8 |
| `Summilux-M 35 FLE2` | WEAK_PASS | Same as above |
| `Leica Summilux 35 FLE2` | WEAK_PASS | Same as above |
| `Leica Summilux-M 35 FLE2` | WEAK_PASS | Same as above |
| `Summilux 35 ASPH` | PASS | No collapse into FLE2; no unsafe pricing change |
| `Summilux-M 35 ASPH` | PASS | Same as above |
| `Summilux 35 4th` | PASS | 4th-gen path unchanged |
| `Summilux 35 6bit` | PASS | Broad-safe path unchanged |

## Regression Table

| Query | Result |
| --- | --- |
| `Summilux 35 Steel Rim` | PASS |
| `Summilux 35 reissue` | PASS |
| `Summilux 35 2매` | PASS |
| `Summilux-M 35 2매` | PASS |
| `35 lux 2mae` | PASS |
| `M35 1.4 2매` | PASS |
| `Summicron 50 DR` | PASS |
| `Summicron 50 Rigid` | PASS |
| `Leica M body` | PASS |
| `Leica 35mm lens` | PASS |

## Remaining Weak-Pass Items

1. Explicit `FLE2` queries still allow one related-but-not-perfectly-clean `FLE` or unrelated later-generation row into the back of the first 8 results.
2. This is now a ranking polish issue, not a price-scope safety issue.
3. No additional parser or price-guard change is justified from this local follow-up alone.

## Recommendation

- Ready for owner preview validation
- Smallest next action, if owner still feels uncertainty:
  - preview-only validation on latest deployment first
  - only if still needed, a second narrow ranking polish for deeper `FLE2` first-screen clustering
- no additional price-scope or parser follow-up recommended from this local pass
