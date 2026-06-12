# P3-BETA-MVP-RESULT-CARD-TITLE-READABILITY-MICRO-FIXUP v0

- branch: `beta-ui-redesign-controlled-preview`
- task: `RESULT-CARD-TITLE-READABILITY-MICRO-FIXUP`

## Files changed

- `app/templates/index.html`
- `index.html`

## Exact UI changes

- Result card title clamp changed from `2` lines to `4` lines.
- Result card title now includes native hover tooltip via `title` attribute.

### Before

- card title used `-webkit-line-clamp:2`
- long Leica titles were clipped too early
- owner QA could miss:
  - `FLE`
  - `FLE II`
  - `FLE2`
  - `AA`
  - `Aspherical`
  - `4th`
  - `6bit`
  - `Black` / `Silver`

### After

- card title uses `-webkit-line-clamp:4`
- full or near-full model names remain visible much more often
- native tooltip exposes the complete title on hover

## What stayed unchanged

- parser
- ranking
- pricing logic
- evidence role logic
- duplicate / outlier logic
- result ordering
- query summary bar
- `Load more`
- result card evidence / price / reason rows
- max 3-column result grid

## Validation run

- template smoke passed
  - `app/templates/index.html` clamp updated to `4`
  - `index.html` clamp updated to `4`
  - native `title` attribute added in both templates
  - `data-load-more` hook still present
- mirror check passed
  - `app/templates/index.html == index.html`
- result grid guard check
  - no result-grid 4-column layout was reintroduced

## Owner smoke queries

Recommended screenshot recheck with:

- `Summilux-M 35 ASPH`
- `Summilux-M 35 FLE`
- `Summilux-M 35 aspherical`
- `35 lux aa`
- `APO-Summicron-M 35 ASPH`

## Final decision

`decision_status = result_card_title_readability_micro_fixup_pushed_ready_for_owner_recheck`
