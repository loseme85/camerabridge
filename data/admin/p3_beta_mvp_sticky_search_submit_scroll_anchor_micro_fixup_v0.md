# Sticky Search Submit Scroll Anchor Micro Fixup v0

- Branch: `beta-ui-redesign-controlled-preview`
- Decision status: `sticky_search_submit_scroll_anchor_micro_fixup_pushed_ready_for_owner_recheck`

## Scope

UI-only micro fix.

Kept unchanged:
- search logic
- parser
- ranking
- pricing
- evidence roles
- result ordering
- Load more
- query summary content
- result card layout

## Exact change

Updated the sticky search submit path so it preserves a results-area anchor after the new result set renders.

Implementation in both:
- `app/templates/index.html`
- `index.html`

Added:
- `pendingResultsAnchorScroll`
- `getResultsAnchorElement()`
- `getStickyAnchorOffset()`
- `scrollResultsIntoView()`

Updated sticky submit to call:

```js
runSearch(0, { preferSticky: true, preserveResultsAnchor: true });
```

Behavior:
- sticky submit does not bounce the user back to the hero search area
- after results render, the page scrolls to the query summary / results anchor
- offset accounts for the sticky bar and topbar so the summary and first row are not hidden underneath

Hero submit behavior remains unchanged.

## Validation

Live local app check:
- started local app on `http://127.0.0.1:5001`
- searched `50 cron dr` from the top form
- scrolled into the results area until sticky search was active
- entered `Summilux-M 35 FLE2` into the sticky search
- pressed `Enter`

Confirmed:
- page did not jump back to the hero/top area
- sticky search remained visible
- results re-rendered directly under the sticky bar
- query summary updated to `Summilux-M 35 FLE2`
- URL updated to `?q=Summilux-M+35+FLE2&sort=relevance`
- hero input and sticky input stayed synced
- first visible result cards remained usable below the sticky bar
- result CTA buttons stayed visible
- `Load more` remained present

Mirror / template checks:
- `app/templates/index.html` and `index.html` are identical

Layout safety:
- no result-grid column rules changed
- no card layout rules changed
- no mobile width CSS changed in this patch
- no horizontal overflow risk introduced by the new logic because this change is submit/scroll behavior only

## Owner-visible expectation

Flow:
1. Search `50 cron dr`
2. Scroll into result cards
3. Use sticky search to submit `Summilux-M 35 FLE2`
4. New results appear under the sticky bar without needing to scroll back down from the hero area

## Notes

- This fix intentionally uses a post-render scroll with `requestAnimationFrame` so the anchor lands after DOM updates complete.
- Sticky anchor target prefers the query summary region, then falls back to the results grid or state region.
