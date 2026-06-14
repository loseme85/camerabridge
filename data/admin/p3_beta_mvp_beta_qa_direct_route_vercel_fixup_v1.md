# P3 BETA MVP Beta/QA Direct Route Vercel Fixup V1

Decision status: `beta_qa_direct_route_vercel_fixup_v1_pushed_ready_for_owner_recheck`

## Exact cause of 404

The latest preview already contained Flask routes for:

- `/`
- `/search`
- `/qa`
- `/beta`

However, the deployed preview was not reaching those Flask routes for direct browser entry.  
`vercel.json` was serving the UI shell through static rewrites:

- `/` -> `/app/templates/index.html`
- `/search` -> `/app/templates/index.html`

but it had no matching direct-route rewrites for:

- `/qa`
- `/beta`

As a result, direct Vercel navigation to `/qa` and `/beta` fell through to `NOT_FOUND`, while `/` still worked.

## Exact routing change

Added two narrow static rewrites in [vercel.json](/Users/changdaepark/Desktop/LEICA%20SEARCH/vercel.json):

- `/qa` -> `/app/templates/index.html`
- `/beta` -> `/beta.html`

No API rewrites were changed.  
No search, parser, ranking, pricing, evidence-role, or price-role logic was changed.

## Direct route validation

| Route | Expected shell | Validation |
| --- | --- | --- |
| `/` | QA shell | Existing rewrite preserved |
| `/search` | QA shell | Existing rewrite preserved |
| `/qa` | QA shell | New rewrite added |
| `/beta` | Beta shell | New rewrite added |

Live preview check note:

- Deployment completed successfully on Vercel after push.
- Direct unauthenticated `curl` checks from this environment returned `401` because the preview is access-protected here, even though deployment completion was confirmed.
- Because of that protection, final shell rendering confirmation for `/qa` and `/beta` must be completed by owner/browser recheck on the authenticated preview.

## Query hydration validation

| Route | Expected behavior | Validation |
| --- | --- | --- |
| `/beta?q=Summilux-M+35+FLE2` | Beta shell loads and existing query hydration runs from `q` | Rewrite preserves query string; client hydration logic unchanged |
| `/qa?q=Summilux-M+35+FLE2` | QA shell loads and existing query hydration runs from `q` | Rewrite preserves query string; client hydration logic unchanged |

## API route safety check

| Route | Expected behavior | Validation |
| --- | --- | --- |
| `/api/search?q=Summilux-M+35+FLE2` | JSON API response | Existing `/api/search` rewrite unchanged |

## Logic safety confirmation

Unchanged:

- parser
- search API behavior
- ranking
- pricing logic
- evidence roles
- price roles
- exact-price unlock logic
- result order

This fix is routing/static deployment only.
