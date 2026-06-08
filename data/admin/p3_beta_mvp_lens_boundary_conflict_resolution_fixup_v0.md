# P3-BETA-MVP-LENS-BOUNDARY-CONFLICT-RESOLUTION-FIXUP

## 1. 작업명
- `P3-BETA-MVP-LENS-BOUNDARY-CONFLICT-RESOLUTION-FIXUP`

## 2. exact boundary logic changes
- Broader family matching now requires visible family evidence when the requested Leica family is specific.
- Third-party 50mm rows without Summilux family evidence are no longer treated as broader-family compatible rows for Summilux-M 50 ASPH.
- SL 90 exact queries continue to treat M/R 90mm and adjacent 90mm rows as boundary conflicts instead of strong SL-compatible evidence.

## 3. Summilux-M 50 ASPH before / after
- before issue = Third-party Nokton rows could still appear as broader-family-like visible evidence instead of clean query-incompatible rows.
- after price status = Reference price only.
- after why = Top visible results include third-party or adjacent items.
- after top_result_compatibility = third_party_top_domination

## 4. APO-Summicron-SL 90 before / after
- before issue = M/R 90mm and adjacent 90mm rows needed to remain boundary conflicts rather than SL-compatible evidence.
- after price status = Price summary is locked.
- after why = Results are visible, but not strong enough for model-level pricing.
- after top_result_compatibility = boundary_conflict

## 5. price unlock change 여부
- No new exact price unlock was introduced in this round.

## 6. third-party / adjacent rows blocking 여부
- Summilux-M 50 ASPH keeps exact price locked when visible results are still third-party or adjacent.
- APO-Summicron-SL 90 keeps price locked when visible rows are still boundary conflicts.

## 7. M/R 90mm rows for SL 90
- Leica M 90mm f2.5 Summarit 6bit Black -> Boundary conflict / Not used — not compatible with this query
- Leica M 90mm f2 APO-Summicron ASPH Black -> Boundary conflict / Not used — not compatible with this query
- Leica M 90mm f2.8 Elmarit Black -> Boundary conflict / Not used — not compatible with this query
- Leica L 90mm f4 Elmar Silver -> Boundary conflict / Not used — not compatible with this query
- TTArtisan L 90mm f1.25 DJ-Optical Black -> Boundary conflict / Not used — not compatible with this query

## 8. UI / copy guard
- Query review regression = none
- Model Market Entry copy remains human-readable.
- Copy summary remains visible via existing guard tests.

## 9. Body price band quality regression
- body_lens_regressions = none
- price_projection_regressions = none

## 10. decision_status
- `lens_boundary_conflict_resolution_fixup_pushed_ready_for_owner_recheck`
