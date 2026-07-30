# UI-U2 Public Beta Blocking Fix v1

## Base
- base commit: `2f3c27d39f344c2b1104f72d46ca8687a64a8c37`
- branch: `ui-public-beta-blockers-v1`
- production: untouched
- main merge: none
- commit/push/deploy: not performed in this round

## Changed Files
- `/Users/changdaepark/Desktop/LEICA SEARCH UI U2 CLEAN/app/app.py`
- `/Users/changdaepark/Desktop/LEICA SEARCH UI U2 CLEAN/app/templates/beta.html`
- `/Users/changdaepark/Desktop/LEICA SEARCH UI U2 CLEAN/beta.html`
- `/Users/changdaepark/Desktop/LEICA SEARCH UI U2 CLEAN/tests/test_search_ui.py`

## Route Before / After

Before:
- `/` -> `index.html` QA/internal shell
- `/search` -> `index.html` QA/internal shell
- `/qa` -> `index.html` QA/internal shell
- `/beta` -> `beta.html` public beta shell

After:
- `/` -> `beta.html` public-facing shell
- `/search` -> `beta.html` public-facing shell
- `/beta` -> `beta.html` public-facing shell
- `/qa` -> `index.html` internal diagnostic shell

## Public vs QA Boundary

Public routes now use the beta shell only:
- `/`
- `/search`
- `/beta`

Internal diagnostic route remains:
- `/qa`

The beta card no longer renders per-card diagnostic grids or role rows. QA/internal template remains unchanged on `/qa`.

## Removed Internal Fields From Public Card

Removed from visible public listing card:
- detected model
- detected entry
- search match field row
- used_for_price field row
- exclusion reason field row
- generation confidence field row
- price role field row
- internal mount/category diagnostics
- projected reference badge
- marker detected badge
- per-card evidence role / price role detail rows
- top visible evidence mini-cards under market summary

Retained as user-facing public elements:
- image
- title
- asking price
- active/sold status
- source
- inferred location
- observed / last verified date
- listing CTA
- public-facing match / price-comparison badges
- simple “Why is this result shown?” explanation

## Responsive Layout Fix

Applied public layout narrowing fix:
- `workspace-grid` changed from `1fr + 300px sidebar` to single-column public layout
- public sidebar hidden from the main flow
- overview cards hidden from the public beta route
- results grid changed to `repeat(auto-fit, minmax(320px, 1fr))`
- archive/history cards also use auto-fit responsive grid
- result card moved from dense 4-column diagnostic grid to stacked fact rows
- price/source row now wraps safely
- title clamp reduced to 3 lines
- action CTA remains visible without horizontal overflow

Expected outcome:
- no large unused right gutter
- wider usable cards on desktop
- one-column readable cards on mobile

## Existing Language Inventory

Current public beta locale tabs present:
- `ko` / 한국어
- `en` / English
- `ja` / 日本語
- `zh-Hans` / 简体中文
- `zh-Hant` / 繁體中文
- `pt` / Português
- `es` / Español
- `de` / Deutsch
- `it` / Italiano

## Translation Coverage Matrix

Expanded visible public-shell coverage for:
- topbar
- hero
- search controls
- filter labels
- summary captions
- pagination labels
- common shell labels
- market summary labels
- public card labels
- public location/date badges
- load more
- price-state captions
- warning/footer copy
- intro / loading / error / empty state cards

Fallback contract:
- supported tabs remain the 9 locale selectors above
- unsupported browser locale values still normalize to English via `normalizeLocale()`
- locale switching remains client-side only and does not re-fetch API data

Remaining note:
- `/qa` keeps its existing internal template and separate internal locale dictionary/accessor
- public route now uses the beta locale surface consistently, but the codebase as a whole still has two template-level locale systems (`index.html` and `beta.html`)

## Data-Source Trace

Observed runtime path:
- `/api/search` -> `api/search.py`
- runtime dependency loader -> `search_index.DEFAULT_SEARCH_INDEX_PATH`
- resolved path -> `/Users/changdaepark/Desktop/LEICA SEARCH UI U2 CLEAN/data/derived/results_search_index_v1.json`

Index metadata observed locally:
- `index_record_count`: `8067`
- `index_generated_at`: `2026-06-30T14:58:36.151117+00:00`
- `index_source_path`: `/Users/changdaepark/Desktop/LEICA SEARCH/data/derived/results_resolved_v2.json`

Current crawler-adjacent local snapshot observed in original repo:
- `data/raw/results.json` mtime: `2026-06-30 23:58:09`
- `data/normalized/normalized_latest.json` mtime: `2026-06-30 23:58:09`
- `data/derived/results_resolved_v2.json` mtime: `2026-06-30 23:58:35`
- `data/derived/results_search_index_v1.json` mtime: `2026-06-30 23:58:36`
- `data/status.json updated_at`: `2026-06-30T23:58:09.708394+09:00`
- `data/status.json total_count`: `8067`

Comparison:
- clean worktree snapshot and original repo snapshot match exactly
- no external DB / object storage / live service read path was found in the runtime search path
- the current public beta runtime is reading committed JSON snapshot files, not an external live source

## Preview vs Crawler Freshness Comparison

Local comparison result:
- clean worktree index: `8067` / `2026-06-30T14:58:36.151117+00:00`
- original repo index: `8067` / `2026-06-30T14:58:36.151117+00:00`
- original repo status total: `8067`

Decision:
- `COMMITTED_SNAPSHOT_ONLY`

Interpretation:
- this patch candidate is locally aligned with the currently committed local crawler snapshot
- but the runtime does not show an external “always current” crawler-backed dataset architecture

## Data Connection Decision

Decision class:
- `B. COMMITTED_SNAPSHOT_ONLY`

Reason:
- runtime search loads `results_search_index_v1.json` from repo paths
- no external object storage / database / runtime dataset service path was found
- freshness metadata comes from the committed index snapshot itself

Implication:
- public beta should not be treated as externally live-current unless a separate publication/storage pipeline is introduced

## Automated Validation

Passed:
- `python3 -m py_compile api/search.py search_service.py search_response.py app/app.py`
- `python3 tests/test_search_ui.py`
- `python3 tests/test_search_response.py`

Added/updated regression checks:
- public routes use beta shell
- `/qa` retains internal shell
- beta public card renders user-facing fields
- beta public card no longer renders diagnostic card fields
- dataset update line is present
- locale switch remains client-side only

## Local Smoke

Route smoke via Flask test client:
- `/` -> 200, beta shell
- `/beta` -> 200, beta shell
- `/qa` -> 200, internal shell

API smoke:
- `Leica M6`
  - 200
  - `price_summary_allowed=false`
  - `display_price_summary_allowed=false`
  - top row `used_for_price=false`
  - top row `price_usage_label=Reference only — generation selection needed`
- `Summilux-M 35 FLE2`
  - 200
  - exact summary allowed
  - top row `used_for_price=true`
  - top row `price_usage_label=Used for exact-generation price`
- `50 cron dr`
  - 200
  - exact summary allowed
  - top row `used_for_price=true`
- `Leica M10 lens kit`
  - 200
  - summary locked
  - top row `used_for_price=false`
- `zzzz nonexistent model`
  - 200
  - `result_count=0`

Public dataset meta exposed locally:
- `index_record_count=8067`
- `index_generated_at=2026-06-30T14:58:36.151117+00:00`

## Browser / Viewport Validation

Attempted:
- local owner-style browser smoke with Playwright

Blocked:
- Playwright browser binary not installed in the clean worktree environment
- Chromium launch failed before viewport screenshots could run

Status:
- automated viewport/browser smoke remains pending until browser binary is available or preview deployment validation is run

## Remaining Blockers

1. Live data architecture is still snapshot-based.
   - public beta runtime is not wired to an external current crawler dataset source
   - result freshness is only as current as the committed snapshot

2. Preview validation is still pending.
   - this round intentionally avoided commit/push/deploy
   - owner preview smoke cannot be re-run on Vercel until a scoped preview deploy exists

3. Codebase-wide single i18n system is still not fully unified.
   - public route is now beta-only
   - internal QA route still uses its own internal template dictionary

4. Browser-level responsive verification is pending.
   - CSS was narrowed and tests passed
   - visual confirmation at `390 / 430 / 768 / desktop` still needs a browser run

## Production Untouched Confirmation

- no production deploy
- no production alias change
- no main merge
- no crawler data rebuild
- no runtime search/parsing/ranking safety loosening

## Recommendation

- UI blocker patch candidate: ready for owner inspection after scoped preview deploy
- live data architecture: not ready for public-live interpretation

Final decision:
- `HOLD_LIVE_DATA_ARCHITECTURE`
