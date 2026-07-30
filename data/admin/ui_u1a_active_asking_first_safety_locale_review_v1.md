# UI-U1A Active Asking First Safety & Locale Completion Review v1

## Base
- Branch: `p4-entry-generation-narrowing-beta`
- HEAD: `8ea984b9e70de4276b623d91f72ce0e599b8417f`
- Date: `2026-07-30`

## Exact Changed Files
- `app/templates/index.html`
- `index.html`
- `app/templates/beta.html`
- `beta.html`
- `search_response.py`
- `tests/test_search_response.py`
- `tests/test_search_ui.py`

Note:
- `search_response.py` additive response projection fields (`crawl_time`, `first_seen`) were already present in the working tree and were reviewed in this round.
- Unrelated dirty/untracked files in the worktree were left untouched.

## Freshness Field Semantics
- Current API response does not expose `last_seen` in the active response contract.
- Client freshness now uses:
  1. `last_seen` if present in `final_output`
  2. `crawl_time` otherwise
  3. `first_seen` only as a late tie-break
- `first_seen` is no longer used as the primary active freshness signal.
- Missing or malformed timestamps fall back to score `0` without throwing UI errors.

## Client Ordering Contract
- This round should be described as:
  - additive response projection
  - client presentation change
- No matching logic, server ranking logic, price eligibility, price calculation, or crawler behavior was intentionally changed.
- Active-asking-first ordering is enforced client-side in the rendered sections.
- Active section compatibility ordering now respects:
  1. exact / compatible active
  2. similar active
  3. excluded / incompatible active

## Section Isolation
- User-facing results remain split into:
  - `Active listings`
  - `Market history`
- Client sort options now operate within each section only:
  - `Recommended`
  - `Newest`
  - `Price: Low to High`
  - `Price: High to Low`
- Sort changes are now client-side only.
- `sort` is no longer sent in `/api/search` requests from the UI search fetch path.
- History URL state still preserves `sort` for Back/Forward hydration.

### Local log confirmation
After the sort fix, local server logs showed one `/api/search` call per query and no follow-up `sort=` refetches during sort changes:
- example:
  - `GET /api/search?q=Leica+M6&limit=12&offset=0`
  - no extra `sort=newest|price_asc|price_desc` requests after UI sort changes

## Response Contract Change
- Existing response keys were not removed.
- Existing key types were not changed.
- `crawl_time` and `first_seen` remain additive optional fields under `result.final_output`.
- Missing timestamp fields do not break serialization or UI rendering.

## Locale Coverage

### Completed for this round
- `Active listings / 현재 판매 중`
- `Market history / 과거 거래 / 가격 기록`
- `Recommended / 추천순`
- `Newest / 최신순`
- `Price: Low to High / 낮은 가격순`
- `Price: High to Low / 높은 가격순`
- `Active / 판매 중`
- `Sold / 판매 완료`
- `Removed / 판매 종료`
- `Archive / 과거 기록`
- listing count formatting
- no active listings
- no market history
- `View listing / 매물 보기`
- root no-result / source-gap state now switches correctly between KO and EN
- locale switch preserves:
  - current query
  - current results
  - result ordering
  - price text
  - section split
  - scroll position
  - no re-search on locale change

### Remaining untranslated or mixed strings
This is **not** a full i18n completion.

Remaining beta-shell examples still visible or statically present:
- `Limited Beta`
- `What to check`
- `How to read results`
- `Price policy`
- `Source coverage`
- `Interpreted as`
- `Search`
- `Sort`
- `Category`
- `Brand`
- `Mount`
- `Sold quality`
- several beta sidebar/hero paragraphs remain Korean-only or mixed KO/EN
- beta `renderEmptyState()` is still Korean-first and not fully locale-aware for EN

Remaining QA/internal examples:
- `Search results`
- `Query review`
- `Interpreted as`
- some QA/debug summary strings remain English under KO locale

## Mirror Validation
- `app/templates/index.html` == `index.html`: PASS
- `app/templates/beta.html` == `beta.html`: PASS

## Automated Validation
Executed:

```bash
python3 -m py_compile api/search.py search_service.py search_response.py app/app.py
python3 tests/test_search_response.py
python3 tests/test_search_ui.py
```

Result:
- `py_compile`: PASS
- `tests/test_search_response.py`: PASS
- `tests/test_search_ui.py`: PASS

Added/covered by automation:
- additive response fields present without breaking existing keys
- missing timestamp fields do not break response contract
- template mirror sync
- freshness preference `last_seen -> crawl_time`
- `first_seen` tie-break presence
- active compatibility tier helper presence
- active/history section isolation presence
- locale switch does not call re-search
- sort changes are client-side only
- localized `View listing` CTA in beta

Additional note:
- `tests/test_search_endpoint.py` was also run manually once during review and hit an existing unrelated assertion (`test_data_file_missing_returns_503`). It was not used as the acceptance gate for UI-U1A.

## Owner Smoke Summary

### A. Leica M6
- Active section rendered first; market history rendered second.
- Broad generation rows remained reference-only.
- No visible active row used `used_for_price=true`.
- Sort changes remained within the same fetched result window after the client-side sort fix.
- KO/EN locale switch preserved titles/order.

### B. Summilux-M 35 FLE2
- Exact-compatible active rows stayed ahead of adjacent generation rows across the verified sort states.
- Same-base or boundary rows remained visible but non-exact.
- Locale switch preserved titles/order.

### C. 50 cron dr
- DR exact row stayed first in active results across verified sort states.
- Non-DR contamination remained below DR exact evidence.
- Sold/history rows did not appear in the active section.

### D. Leica M10 lens kit
- Active results remained safety-conservative.
- Accessory/boundary rows stayed `used_for_price=false`.
- Body-only rows did not surface as exact active kit evidence.

### E. nonexistent model
- Root no-result state now switches correctly:
  - KO: `확인 가능한 결과를 충분히 찾지 못했습니다.`
  - EN: `No verified matches found for this search.`
- No raw internal state was exposed in the empty state.
- Locale switch preserved the empty-state structure without triggering re-search.

## Safety Observations
- Existing server-side safety labels and exclusion decisions were respected.
- Client compatibility tiering does not override server evidence decisions; it only orders already-visible active rows more safely.
- Asking price and sold/history sections remain visually separated.
- Asking/sold statistics were not blended in this UI pass.

## Unrelated Dirty Files
- Large unrelated tracked/untracked worktree state remains present.
- This review did not modify or clean unrelated files.

## Recommendation
- Active-asking-first section behavior: PASS
- Sort isolation after client-side fix: PASS
- Root locale completion for required active-first surface: PASS
- Beta shell full translation completeness: PARTIAL

## Final Decision
`PARTIAL_REVISION_NEEDED`

Reason:
- Active-asking-first safety behavior and root owner smoke are in good shape.
- Full beta-shell locale completion is not finished yet, and remaining untranslated/mixed strings are still visible.
