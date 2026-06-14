# P3 Beta MVP Search History Back Navigation UX Fixup v1

- Decision status: `search_history_back_navigation_ux_fixup_v1_pushed_ready_for_owner_recheck`
- Branch: `beta-ui-redesign-controlled-preview`
- Scope: browser history UX only

## Exact change

Added committed-search browser history state management to the search UI.

- New committed searches now build a canonical URL/state from:
  - `q`
  - `sort`
  - active filters
  - `offset`
  - visible result count when Load more expanded the first page
- Committed searches use `history.pushState(...)`.
- Initial hydration and in-place cleanup use `history.replaceState(...)`.
- `popstate` now restores:
  - query text
  - filters/sort
  - previous results via replayed search
  - expanded visible count where supported
  - stored scroll position when available, otherwise the results anchor
- Sticky search submit now also creates a committed history entry while preserving the existing results-anchor behavior.
- Duplicate committed states do not spam history; identical committed state falls back to `replaceState`.

## Before / after

### Before

- Search pages behaved like a flat single state.
- Browser Back/Forward mainly changed the URL or tab history shell behavior, but did not reliably restore the previous committed search screen.
- Sticky search submit updated results but was not treated as a restorable history step.

### After

- Each committed search becomes a browser history entry.
- Browser Back restores the previous committed query, summary, and result grid.
- Browser Forward restores the next committed query, summary, and result grid.
- Direct `?q=...` loads hydrate into the same state model without creating duplicate entries.
- Sticky search submit participates in history and keeps the results-area anchor behavior.

## Back / Forward validation

| Scenario | Validation | Result |
| --- | --- | --- |
| A1 | `Summicron 50 hood` -> `Leica Summicron 50 hood` -> `Summicron-M 50 hood` | PASS |
| A2 | Back once restored `Leica Summicron 50 hood` URL, input text, query review, and results | PASS |
| A3 | Back again restored `Summicron 50 hood` URL, input text, query review, and results | PASS |
| A4 | Forward restored `Leica Summicron 50 hood` state again | PASS |
| B1 | Direct load `?q=Leica+12585` hydrated query, summary, and results on page load | PASS |
| C1 | Duplicate committed state protection reviewed in code via stable history key comparison | PASS |

Notes:

- Scenario A was manually verified in local Safari against `http://127.0.0.1:5001`.
- Scenario B direct URL hydration was manually verified in local Safari.
- Duplicate-state handling is implemented via `historyKey` comparison before pushing.

## Sticky search validation

| Check | Result |
| --- | --- |
| Sticky submit uses committed history entry path | PASS |
| Sticky submit preserves existing results-anchor flow | PASS |
| Sticky and hero inputs stay synchronized through restored state | PASS |

Notes:

- Sticky submit now calls the same search flow with `historyMode: 'push'`.
- The existing sticky anchor behavior remains on the `preserveResultsAnchor` path.

## Direct URL hydration validation

| Check | Result |
| --- | --- |
| Initial page load with `?q=Leica+12585` hydrates results | PASS |
| Initial state is seeded with `replaceState`, not duplicate `pushState` | PASS |
| Restored state can replay from URL params when `event.state` is missing | PASS |

## Regression table

| Area | Result | Notes |
| --- | --- | --- |
| Parser behavior | PASS | No parser files changed |
| Search scoring / ranking | PASS | No search scoring logic changed |
| Price roles / evidence roles | PASS | No pricing or evidence logic changed |
| Exact price unlock logic | PASS | No unlock logic changed |
| Load more | PASS | Visible-count state is preserved for first-page expansion path |
| View source buttons | PASS | No card CTA logic changed |
| Sticky search anchor | PASS | Existing preserve-results path retained |
| Recent safety queries (`Summilux-M 35 FLE2`, `50 cron dr`, `Leica M10 lens kit`) | PASS | No search/data logic touched |

## Files changed

- `app/templates/index.html`
- `index.html`

## Confirmation

This fixup did **not** change:

- parser logic
- search scoring
- ranking rules
- evidence role assignment
- price role assignment
- exact price unlock logic
- pricing thresholds
- duplicate/outlier policy

This is a small search-page navigation/state UX fix only.
