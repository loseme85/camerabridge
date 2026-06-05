# P3-BETA-MVP-RESULT-CARD-RUNTIME-NORMALIZATION-PROJECTION-FIXUP

- decision_status: `beta_mvp_result_card_runtime_projection_fixup_pushed_ready_for_owner_recheck`

## Owner recheck failure summary
- Owner preview still showed [중고]Leica M50/1.2 1세대 as Detected model=M5 / Family=M Body / Category=Body after the compact-lens boundary fix.

## Screenshot issue summary
- The result card was still reading stale normalized Body metadata even though title-level compact lens notation indicates an M-mount 50mm f/1.2 lens.

## Root cause hypothesis
- stale final_output rows in the existing search index still contain Body/M5 metadata
- runtime compact-lens projection previously missed slash notation when it read normalized title text only
- result card UI was reading raw final_output fields directly instead of a safer display projection layer

## Safe display projection design
- add display_output to each API result
- prefer display_category/display_model/display_family/display_mount/display_focal_length/display_aperture for UI
- when compact lens notation conflicts with stale Body output, project the card to Lens and blank unsafe body model claims

## Stale final_output conflict guard
- compact_lens_notation_detected
- body_alias_boundary_blocked
- classification_conflict_detected
- stale_body_normalization_detected
- result_card_confidence_state

## Result card UI changes
- result cards now read display_output instead of raw final_output for Detected model / Family / Mount / Category
- compact lens conflicts show Runtime projection and Lens notation detected badges
- focal length and aperture are shown on the card when compact notation can safely provide them

## Market entry / price summary gate connection
- classification or stale-normalization conflict now contributes to market entry blocking
- summary-scope checks now honor display-safe category/mount/focal fields
- the stale M50/1.2 row cannot be used as Body evidence for M5 market entry or price summary

## Query regression highlights
- `[중고]Leica M50/1.2 1세대`: top=`Lens` title_row_index=`32`
- `M50/1.2`: top=`Lens` title_row_index=`59`
- `Leica M50/1.2 1세대`: top=`Lens` title_row_index=`32`
- `M35/2`: top=`Lens` title_row_index=`None`
- `M28/2.8`: top=`Lens` title_row_index=`None`
- `Leica M5`: top=`Body` title_row_index=`66`
- `M5 body`: top=`Body` title_row_index=`100`
- `Leica M9`: top=`Body` title_row_index=`None`
- `Leica M10`: top=`Body` title_row_index=`None`
- `Leica M11`: top=`Body` title_row_index=`None`
- `q3 28`: top=`Body` title_row_index=`None`

## Git diff summary
- branch: `beta-ui-redesign-controlled-preview`
- head_commit: `d4658fe11b2a85f83c0332c0e38d7a57c15f8cef`
- head_subject: `d4658fe fix: project safe result card metadata for compact lens conflicts`
- diff_stat: `...ult_card_runtime_normalization_projection_fixup_v0.json |  6 +++---
 ...lt_card_runtime_normalization_projection_fixup_v0.jsonl |  2 +-
 ...esult_card_runtime_normalization_projection_fixup_v0.md | 14 ++++++--------
 3 files changed, 10 insertions(+), 12 deletions(-)`
