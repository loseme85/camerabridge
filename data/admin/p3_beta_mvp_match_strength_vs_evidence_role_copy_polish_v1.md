# P3 Beta MVP Match Strength vs Evidence Role Copy Polish v1

## Decision Status

`match_strength_vs_evidence_role_copy_polish_v1_pushed_ready_for_owner_recheck`

## Exact UI / Copy Change

- Updated the small match-strength badge at the top of each result card.
- The badge no longer shows plain `Match strong` for rows that are clearly not exact variant price evidence.
- The new badge now considers:
  - `match_quality`
  - `Evidence role`
  - `Price role`
  - `Reason`

### New badge behavior

- Exact variant rows:
  - `Exact variant match`
  - `Exact variant candidate`
- Same-base rows:
  - `Family match strong`
  - `Family match`
  - `Same-base only`
- Boundary-conflict rows:
  - `Related match`
  - `Variant conflict`

## Files Changed

- [app/templates/index.html](</Users/changdaepark/Desktop/LEICA SEARCH/app/templates/index.html>)
- [index.html](</Users/changdaepark/Desktop/LEICA SEARCH/index.html>)
- [p3_beta_mvp_match_strength_vs_evidence_role_copy_polish_v1.md](</Users/changdaepark/Desktop/LEICA SEARCH/data/admin/p3_beta_mvp_match_strength_vs_evidence_role_copy_polish_v1.md>)

## Before / After — FLE2 Query Examples

### Query: `Summilux-M 35 FLE2`

#### Before

- true FLE2 rows: `Match strong`
- non-FLE2 same-base / boundary rows: also `Match strong`

This was price-safe, but visually implied exactness.

#### After

| row type | title example | evidence role | price role | badge now shown |
| --- | --- | --- | --- | --- |
| true FLE2 exact row | `[위탁] M 35/1.4 Summilux ASPH FLE2 (Black)` | `Exact variant` | `Used for exact price` | `Exact variant match` |
| true FLE2 exact row | `신품 Leica M 35mm f1.4 Summilux ASPH 6bit FLE II Black` | `Exact variant` | `Used for exact price` | `Exact variant match` |
| non-exact related row | `Leica M 35mm f1.4 Summilux 2nd Titan` | `Boundary conflict` | `Same base model result is visible, but not used as exact price` | `Related match` |

### Query: `Summilux-M 35 FLE II`

Same behavior as `Summilux-M 35 FLE2`:

- FLE2 / FLE II exact rows -> `Exact variant match`
- unrelated `2nd / Steel Rim / broad ASPH` rows -> `Related match`

### Query: `Summilux-M 35 close focus`

Same behavior as explicit FLE2:

- close-focus / FLE2 rows -> `Exact variant match`
- unrelated rows -> `Related match`

## Exact Variant Row Copy Examples

| query | title | old top badge | new top badge |
| --- | --- | --- | --- |
| `Summilux-M 35 FLE2` | `[중고] M 35/1.4 Summilux ASPH 6bit FLE2 (Black)` | `Match strong` | `Exact variant match` |
| `Summilux-M 35 ASPH` | `Leica M 35mm f1.4 Summilux ASPH 4th Titan` | `Match strong` | `Exact variant match` |
| `Summilux-M 35 2매` | `[중고] M35/1.4 Summilux 2매 (Black)` | `Match strong` | `Exact variant match` |
| `50 cron dr` | `Leica M 50mm f2 Summicron DR Silver` | `Match medium` | `Exact variant candidate` |

## Same-Base / Boundary-Conflict Row Copy Examples

| query | title | evidence role | price role | old top badge | new top badge |
| --- | --- | --- | --- | --- | --- |
| `Summilux-M 35 FLE2` | `Leica M 35mm f1.4 Summilux 2nd Titan` | `Boundary conflict` | `Same base model result is visible, but not used as exact price` | `Match strong` | `Related match` |
| `Summilux-M 35` | `Leica M 35mm f1.4 Summilux ASPH 4th Titan` | `Same base model` | `Same base model result is visible, but not used as exact price` | `Match strong` | `Family match strong` |
| `Summilux 35 Steel Rim` | `신품 Leica M 35mm f1.4 Summilux Black 스틸림 복각` | `Same base model` | `Not used — Price outlier` / same-base visible | `Match strong` | `Family match strong` |
| `Leica 12585` | `Leica 12585 Hood for M-50mm, 35mm` | `Not compatible with this query` | `Not used — not compatible with this query` | `Match strong` | `Related match` |

## Regression Table

| query | expected | observed | result |
| --- | --- | --- | --- |
| `Summilux-M 35` | pricing unchanged, only badge clearer | broad query remains locked; same-base rows now read `Family match strong` | PASS |
| `Summilux-M 35 ASPH` | exact ASPH behavior unchanged | exact rows read `Exact variant match`; pricing unchanged | PASS |
| `Summilux-M 35 FLE` | no price/ranking change | FLE rows read `Exact variant match`; pricing unchanged | PASS |
| `Summilux-M 35 2매` | AA behavior unchanged | exact AA rows read `Exact variant match`; pricing unchanged | PASS |
| `Summilux 35 Steel Rim` | Steel Rim behavior unchanged | Steel Rim rows remain conservative; badge copy clearer | PASS |
| `50 cron dr` | DR behavior unchanged | DR rows read `Exact variant candidate`; pricing unchanged | PASS |
| `Leica Summicron 50 rigid` | rigid guard unchanged | rigid behavior unchanged; exact rows read more clearly | PASS |
| `Leica 12585` | accessory safety unchanged | no exact price unlock; badge no longer implies exact lens match | PASS |
| `Leica M10 lens kit` | bundle guard unchanged | remains locked; rows read `Family match strong` rather than exact-like | PASS |

## Confirmation: What Did Not Change

- parser logic: unchanged
- search scoring: unchanged
- exact price unlock logic: unchanged
- evidence role assignment: unchanged
- price role assignment: unchanged
- result ordering / ranking: unchanged
- duplicate/outlier policy: unchanged

## Remaining Issues

1. `Summicron 50 hood`
   - candidate label may be acceptable, but first-screen hood coverage is still weak
   - this remains a ranking / candidate-pool polish issue, not a price-safety or match-badge issue

2. Some broad same-base locked queries still read visually dense
   - the badge is now less misleading
   - deeper ranking polish can still improve first-screen clarity later

## Validation Notes

- This change was validated by running the current runtime response through the new badge-selection logic for:
  - `Summilux-M 35 FLE2`
  - `Summilux-M 35 FLE II`
  - `Summilux-M 35 close focus`
  - regression queries listed above
- No pricing, parser, or ranking regressions were introduced in the checked set.
