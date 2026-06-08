# P3-BETA-MVP-RESULT-CARD-PRICE-ROLE-REASON-UI-MICRO-FIXUP

## files changed
- `app/templates/index.html`
- `index.html`
- `data/admin/p3_beta_mvp_result_card_price_role_reason_ui_micro_fixup_v0.md`

## exact UI changes
- Kept current card fields:
  - `Detected model`
  - `Family`
  - `Match role`
  - `Price role`
  - `Focal length`
  - `Aperture`
  - `Mount`
  - `Category`
- Added a short conditional card row:
  - `Reason`

## which existing fields are used for reason display
- `excluded_reason`
- `compatibility_label`
- `result_role_label`
- `price_usage_label`
- `match_quality` as last-resort fallback

## reason display behavior
- If `excluded_reason` exists:
  - show the first excluded reason
- If exact price is used:
  - show `Exact variant evidence` or `Exact price evidence`
- If `Exact variant`:
  - show `Model / focal / variant matched`
- If `Exact base model` or `Same base model`:
  - show `Same base model, not exact variant`
- If `Broader family`:
  - show `Broader family reference`
- If `Boundary conflict`:
  - show `Boundary conflict`
- If `Query incompatible`:
  - show `Not compatible with this query`
- If no clear supported reason exists:
  - omit the `Reason` row

## whether any backend / search / pricing / parser logic changed
- No
- Template-only UI mapping

## whether Query review / Model Market Entry changed
- No

## whether Load more / grid changed
- No

## validation run
- Template smoke:
  - `Reason` row present in `renderCard`
  - `Match role` and `Price role` still present
  - `Source coverage` did not return to `renderCard`
  - `Price confidence` did not return to `renderCard`
  - `Copy summary` still present
  - `data-load-more="true"` still present
  - no 4-column breakpoint returned
- Template mirror check:
  - `app/templates/index.html` and `index.html` remain in sync

## latest Vercel deployment URL
- Not verified in this round

## final decision_status
- `result_card_price_role_reason_ui_micro_fixup_pushed_ready_for_owner_recheck`
