P3-BETA-MVP-QA-CAPTURE-QUERY-SUMMARY-BAR-MICRO-FIXUP

Branch: `beta-ui-redesign-controlled-preview`

Decision status:
`qa_capture_query_summary_bar_micro_fixup_pushed_ready_for_owner_recheck`

## Files changed

- `app/templates/index.html`
- `index.html`

## Exact UI behavior implemented

Added a compact query summary bar above the result grid after a search returns visible results.

The bar shows:

- `Search query`
- active query text
- visible result count
- `Detected:` line when parsed target details are available

Example shape:

- `Search query: APO-Summicron-SL 50`
- `5 visible`
- `Detected: Leica APO-Summicron-SL 50 candidate`

The summary bar appears close to the result cards, so owner QA screenshots can capture both:

- the searched query
- the first visible row of result cards

## Grid / layout behavior

- compact non-sticky bar only
- no full search-box pinning
- low vertical footprint
- appears above `results-grid`
- mobile-safe wrapping for long query text

Grid behavior remains unchanged:

- mobile: 1 column
- medium: 2 columns
- desktop: max 3 columns

## What did not change

- search behavior
- parser
- ranking
- pricing
- evidence projection
- result cards
- Load more behavior
- Model Market Entry
- Query Review
- duplicate / outlier / no-price reason display

## Validation run

Template smoke checks passed:

- query summary CSS present
- query summary region present
- query summary renderer present
- query summary renders before `results-grid`
- `Load more` hook still present
- 3-column result grid still present
- 4-column result grid did not return
- `app/templates/index.html` and `index.html` remain in sync

## Commit / push

- commit hash: `7a7f0ed2b7747202629fbe585460fe528501900d`
- push status: success

## Latest Vercel deployment URL

- not verified in this session
