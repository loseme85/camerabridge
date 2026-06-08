# P3-BETA-MVP-TRI-ELMAR-WATE-MATE-COMPATIBILITY-FOLLOWUP

## 1. 작업명
- `P3-BETA-MVP-TRI-ELMAR-WATE-MATE-COMPATIBILITY-FOLLOWUP`

## 2. exact compatibility logic changed
- Tri-Elmar WATE / MATE rows can now inherit compatible same-base usage labels even when they stay visible-only for pricing.
- WATE queries accept 16-18-21 Tri-Elmar-M rows as compatible same-base/reference evidence.
- MATE queries accept 28-35-50 Tri-Elmar-M rows as compatible same-base/reference evidence.
- WATE vs MATE cross-boundary separation remains intact.

## 3. before / after for `wate`
- before issue = Compatible 16-18-21 Tri-Elmar rows could show up as not compatible with this query.
- after interpreted_target = Leica Tri-Elmar-M 16-18-21 WATE candidate
- after price_status = Reference price only.

## 4. before / after for `mate`
- before issue = Compatible 28-35-50 Tri-Elmar rows could show up as boundary conflict instead of same-base evidence.
- after interpreted_target = Leica Tri-Elmar-M 28-35-50 MATE candidate
- after price_status = Reference price only.

## 5. before / after for `tri-elmar 16-18-21`
- Leica M 16-18-21mm f4 Tri-elmar ASPH 6bit Black -> Exact base model / Same base model result is visible, but not used as exact price
- LEICA 16-18-21mm F4 ASPH TRI-ELMAR-M (6bit) sn.4182 -> Exact base model / Same base model result is visible, but not used as exact price
- Leica M 16-18-21mm f4 Tri-elmar ASPH 6bit Black + Finder set -> Exact base model / Not used — Accessory, not camera/lens

## 6. before / after for `tri-elmar 28-35-50`
- Leica M 28-35-50mm f4 Tri-Elmar e49 신형 Black -> Exact base model / Same base model result is visible, but not used as exact price
- Leica M 16-18-21mm f4 Tri-elmar ASPH 6bit Black -> Query incompatible / Not used — not compatible with this query
- Leica M 16-18-21mm f4 Tri-elmar ASPH 6bit Black + Finder set -> Query incompatible / Not used — not compatible with this query

## 7. cross-boundary guard status
- cross_boundary_regressions = none

## 8. generic `tri-elmar` ambiguity guard status
- generic_tri_elmar_regressions = none

## 9. accessory / finder guard status
- accessory_finder_regressions = none

## 10. price / routing / UI guard
- price_unlock_regressions = none
- body_lens_regressions = none
- technical_copy_regressions = none

## 11. decision_status
- `tri_elmar_wate_mate_compatibility_followup_passed_ready_for_owner_approved_push`
