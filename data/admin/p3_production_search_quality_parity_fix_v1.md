# P3 Production Search Quality Parity Fix v1

## Summary

- Production had the preview UI shell, but it was still using the older main search stack.
- That older stack did not recover structured body intent for queries like `Leica M10`.
- Result: production showed broad Leica lens weak matches instead of M10 body-focused results.
- Fix approach: keep main live data/index intact, and sync the preview search stack only.

## Root Cause

Preview and main differed in the query-time search pipeline:

- `api/search.py`
- `query_parser.py`
- `query_resolver.py`
- `search_service.py`
- `search_response.py`
- `search_aliases.py`

These differences caused:

- `m10` not recognized as `body_intent`
- candidate narrowing not applied to M-body results
- `display_output` missing from result cards
- evidence/price role projection not returned in preview-style shape

## Files Changed

- `api/search.py`
- `query_parser.py`
- `query_resolver.py`
- `search_service.py`
- `search_response.py`
- `search_aliases.py`
- `data/config/source_registry_v1.json`
- `data/admin/p3_production_search_quality_parity_fix_v1.md`

## Data Safety

- `data/raw`, `data/normalized`, and `data/derived` live main data were not overwritten from preview.
- Current live search index remains:
  - `index_record_count = 7841`
  - `index_generated_at = 2026-07-08T09:05:25.465831+00:00`

## Local Smoke

### Leica M10

- Intent:
  - `body_intent = M10`
  - `mount = M`
- Top results:
  - `Leica M10 Silver`
  - `[위탁] M10 Monochrom 'Leitz Wetzlar' Edition`
  - `[중고] Leica M10 홀스터`
  - `[중고] Leica M10 하프케이스 (Brown)`
  - `[중고] Leica M10 하프케이스 (Black)`
- First result display:
  - `display_category = Body`
  - `display_model = M10`
  - `display_family = M Body`

### Leica Q2

- Intent:
  - `body_intent = Q2`
  - `system = Q`
- Top results are Q2 body rows again.

### Leica 50mm Summicron-M Type IV

- Structured lens intent present.
- Price scope remains conservative:
  - `price_summary_allowed = False`
  - `price_scope = blocked_boundary_conflict`

### Leica hood

- Accessory intent recovered:
  - `accessory_intent = hood`
- Top results are hood/accessory rows.
- Unsafe lens/body price unlock stays blocked.

### Leica M11-P

- Intent:
  - `body_intent = M11-P`
  - `mount = M`
- Top results:
  - `Leica M11-P Silver`
  - `Leica M11-P Black`
  - `신품 Leica M11-P Metal Gray Paint Finish`
  - `Leica M11-P Body Only - Silver`

## Expected Production Outcome

After deploy, production should match preview behavior for:

- `https://camerabridge.vercel.app/?q=Leica+M10`
- `https://camerabridge.vercel.app/?q=Leica+Q2`
- `https://camerabridge.vercel.app/?q=Leica+M11-P`
- `https://camerabridge.vercel.app/?q=Leica+hood`

And API should continue to report live main metadata:

- `meta.index_record_count = 7841`
- `meta.index_generated_at = 2026-07-08T09:05:25.465831+00:00`
- `meta.deployment_commit = new main commit`

## Status

- Local parity fix: `PASS`
- Production verification: `PENDING` until main push + Vercel production smoke complete
