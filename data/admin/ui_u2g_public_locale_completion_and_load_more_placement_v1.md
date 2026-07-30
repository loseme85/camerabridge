# UI-U2G Public Locale Completion and Load More Placement v1

## Scope
- Public `/` locale surface completion only
- Active-only load more placement clarification
- No crawler, snapshot, API schema, ranking, parser, matching, or pricing logic changes
- Production/main untouched

## Snapshot preserved
- `index_generated_at`: `2026-07-30T08:40:36.953341+00:00`
- `index_record_count`: `7654`

## Exact changes

### 1. Public locale surface completion
- Completed public-shell locale coverage for:
  - top status pills
  - hero eyebrow/title/subtitle
  - beta notice pills
  - search labels and CTA
  - sidebar guidance copy
  - active/history section titles and descriptions
  - load-more button text and progress note
- Preserved original listing data without translation:
  - listing title
  - seller/source
  - price
  - currency
  - URL
  - query text

### 2. Active-only load more placement
- Moved `Load more` into the Active listings section footer
- Placement is now:
  - after active result cards
  - before Market history
- Added localized active-only copy:
  - ko: `현재 판매 중인 매물 더 보기`
  - en: `Load more active listings`
  - ja: `販売中の商品をさらに表示`
  - plus supported translations for `zh-Hans`, `zh-Hant`, `pt`, `es`, `de`, `it`
- Added localized progress note such as:
  - `3 / 260 표시 중`
  - `3 / 260 shown`

### 3. Mobile overflow fix
- Fixed 390px mobile horizontal overflow by allowing `.workspace-main` to shrink inside the grid:
  - `min-width: 0;`

## Validation

### Static / unit validation
- `python3 -m py_compile api/search.py search_service.py search_response.py app/app.py` PASS
- `python3 tests/test_search_ui.py` PASS
- `python3 tests/test_search_response.py` PASS
- `cmp -s app/templates/beta.html beta.html` PASS
- `cmp -s app/templates/index.html index.html` PASS

### Added/updated coverage
- Locale surface keys for hero / notices / search / section / load-more
- Locale switching renders without `runSearch()` / `fetch()` in `setLocale`
- Listing titles remain source-authored text
- Load more stays scoped to active section
- Load more hides when active pagination is complete
- Mobile shrink guard for `.workspace-main`

### Browser smoke
Local public beta shell verified against `http://127.0.0.1:5002/?q=Leica%20M10`

Checked viewports:
- `390 x 844`
- `430 x 932`
- `768 x 1024`
- desktop

Checked locales:
- `ko`
- `en`
- `ja`
- `zh-Hans`
- `zh-Hant`
- `pt`
- `es`
- `de`
- `it`

Verified:
- locale text updates across hero, notice, sections, and load-more
- listing title remains unchanged across locale switches
- active/history sections remain separated
- load more stays inside Active listings and above Market history
- 390px horizontal overflow removed
- `Leica M10` active load-more appends additional active cards without duplicate URL/CTA rows
- history count remains unchanged during active-only load more

## Notes
- Browser smoke used the running committed snapshot only
- No claim is made here that live data wiring changed

## Final decision
- `READY_FOR_PRODUCTION_RELEASE_REVIEW`
