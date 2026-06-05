# P3-BETA-MVP-COMPACT-LENS-NOTATION-AND-BODY-ALIAS-BOUNDARY-FIXUP

- decision_status: `beta_mvp_compact_lens_body_alias_boundary_fixup_passed_ready_for_owner_approved_push`
- compact lens notation now parses as lens intent before body alias fallback
- stale Body rows with compact lens notation are projected back to Lens at search time
- true Leica body aliases (M5, M9, M10, M11) remain intact

## Compact Query Results
- `M50/1.2` -> body_intent=`None`, mount=`M`, focal=`50`, aperture=`1.2`, top_category=`Lens`
- `Leica M50/1.2 1세대` -> body_intent=`None`, mount=`M`, focal=`50`, aperture=`1.2`, top_category=`Lens`
- `M50/2` -> body_intent=`None`, mount=`M`, focal=`50`, aperture=`2`, top_category=`Lens`
- `M35/2` -> body_intent=`None`, mount=`M`, focal=`35`, aperture=`2`, top_category=`Lens`
- `M28/2.8` -> body_intent=`None`, mount=`M`, focal=`28`, aperture=`2.8`, top_category=`Lens`

## True Body Alias Regression
- `Leica M5` -> body_intent=`M5`, top_category=`Body`, top_model=`M5`
- `M5 body` -> body_intent=`M5`, top_category=`Body`, top_model=`M5`
- `Leica M9` -> body_intent=`M9`, top_category=`Body`, top_model=`M9`
- `Leica M10` -> body_intent=`M10`, top_category=`Body`, top_model=`M10`
- `Leica M11` -> body_intent=`M11`, top_category=`Body`, top_model=`M11`
- `q3 28` -> body_intent=`Q3`, top_category=`Body`, top_model=`Q3`
