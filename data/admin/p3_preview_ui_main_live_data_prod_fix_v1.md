# P3 Preview UI to Main Live Data Production Fix v1

## Executive Summary

- Goal: move the validated preview UI/UX onto production `https://camerabridge.vercel.app` without overwriting main branch live crawl data.
- Root production failure: `api/search.py` on main imported `search_ui_hints`, but `search_ui_hints.py` was missing from main, causing `ModuleNotFoundError` and `500 FUNCTION_INVOCATION_FAILED`.
- Separate live-data gap: main auto crawl updated `data/raw/results.json`, but did not rebuild `results_classified_v2.json`, `results_resolved_v2.json`, or `results_search_index_v1.json`, leaving production on stale derived artifacts.
- Fix approach:
  - bring over preview UI/runtime support files only
  - preserve main raw/normalized data
  - rebuild main derived files from current main raw data
  - update crawl workflow so future main auto crawls also rebuild derived/index before commit

## Root Cause

1. `api/search.py` on main imported `build_query_ui_hints` from `search_ui_hints`.
2. `search_ui_hints.py` was not present on main, so Vercel serverless import failed.
3. `.github/workflows/crawl.yml` ran `python3 app/test.py` and committed `data/`, but never ran `final_resolution_pipeline.py`.
4. Result:
   - raw/normalized moved forward with main auto crawl
   - resolved/index stayed on an old artifact

## Files Changed

- `.github/workflows/crawl.yml`
- `api/search.py`
- `app/app.py`
- `app/templates/index.html`
- `app/templates/beta.html`
- `beta.html`
- `index.html`
- `data/derived/override_report.json`
- `data/derived/results_classified_v2.json`
- `data/derived/results_resolved_v2.json`
- `data/derived/results_search_index_v1.json`
- `final_resolution_pipeline.py`
- `search_index.py`
- `search_ui_hints.py`
- `vercel.json`
- `data/admin/p3_preview_ui_main_live_data_prod_fix_v1.md`

## Scoped UI Adoption

- Production root keeps using main branch deployment.
- `app/templates/index.html` was replaced with the preview branch shell so `/` now serves the preview-tested UI/UX.
- `index.html` was also replaced with the preview branch shell because Vercel production root is served from the top-level static entrypoint.
- `app/app.py`, `app/templates/beta.html`, `beta.html`, and `vercel.json` were aligned so local and Vercel route behavior matches the preview shell pattern for `/`, `/search`, `/qa`, and `/beta`.
- No preview `data/raw`, `data/normalized`, or preview-derived files were copied into main.

## API / Runtime Fix

- Added missing `search_ui_hints.py` to main so `api/search.py` imports resolve on Vercel.
- Added index metadata exposure to `/api/search` response:
  - `index_path`
  - `index_generated_at`
  - `index_record_count`
  - `index_source_path`
  - `api_runtime`
  - `deployment_commit`
  - `request_query`
- Added `load_search_index_metadata()` in `search_index.py`.

## Live Data Rebuild

### Before rebuild

- `data/raw/results.json`: 7841
- `data/normalized/normalized_latest.json`: 7841
- `data/derived/results_resolved_v2.json`: 7860
- `data/derived/results_search_index_v1.json`: 7860
- stale index `generated_at`: `2026-04-22T14:39:05.238676+00:00`

### After rebuild

- `data/raw/results.json`: 7841
- `data/normalized/normalized_latest.json`: 7841
- `data/derived/results_classified_v2.json`: 7841
- `data/derived/results_resolved_v2.json`: 7841
- `data/derived/results_search_index_v1.json`: 7841
- rebuilt index `generated_at`: `2026-07-08T09:05:25.465831+00:00`
- rebuilt index `source_path`: `data/derived/results_resolved_v2.json`

## Workflow Fix

- Added:

```yaml
- name: Rebuild resolved outputs and search index
  run: python3 final_resolution_pipeline.py
```

- This means future scheduled main auto crawls now:
  1. crawl raw data
  2. rebuild classified/resolved/search index
  3. commit updated derived artifacts together

## Local Verification

### Compile

```bash
python3 -m py_compile api/search.py app/test.py search_ui_hints.py search_index.py final_resolution_pipeline.py app/app.py
```

Passed, with existing `app/test.py` `SyntaxWarning` messages only.

### Rebuild

```bash
python3 final_resolution_pipeline.py
```

Passed and regenerated derived outputs from current main raw data.

### Local API smoke

Used direct `endpoint_response()` and Flask test client.

- `/api/search?q=Leica%20M10&limit=1` -> `200`
- `/api/search?q=Leica%20Q2&limit=1` -> `200`
- `/api/search?q=Leica%2050mm%20Summicron-M%20Type%20IV&limit=1` -> `200`

Example meta payload:

```json
{
  "index_path": "/private/tmp/camerabridge-main-fix/data/derived/results_search_index_v1.json",
  "index_generated_at": "2026-07-08T09:05:25.465831+00:00",
  "index_record_count": 7841,
  "index_source_path": "data/derived/results_resolved_v2.json",
  "api_runtime": "vercel-python",
  "deployment_commit": null,
  "request_query": "Leica M10"
}
```

### Local route smoke

- `/` -> `200`
- `/search` -> `200`
- `/qa` -> `200`
- `/beta` -> `200`
- `/api/search?q=Leica%20M10&limit=1` -> `200`

## Expected Production Outcome

After pushing to main and waiting for Vercel production deployment:

- `https://camerabridge.vercel.app/`
  - should show the preview-tested UI shell
- `https://camerabridge.vercel.app/api/search?q=Leica%20M10&limit=1`
  - should return `200`
  - should include `meta`
  - should report the rebuilt main index metadata, not the old `7860` artifact

## Remaining Risks

- This change fixes the missing import and derived-index freshness gap, but does not independently audit ranking quality.
- `deployment_commit` in local smoke is `null`; on Vercel it should be filled by `VERCEL_GIT_COMMIT_SHA`.
- Any future workflow failure before `final_resolution_pipeline.py` would again risk raw/derived drift, so post-deploy production smoke is still required.

## Final Status

- Local scoped fix: `PASS`
- Production deploy verification: `PENDING` until main push + Vercel production smoke complete
