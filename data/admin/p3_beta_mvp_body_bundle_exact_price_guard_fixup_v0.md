# P3 Beta MVP Body Bundle Exact Price Guard Fixup v0

- decision_status: `body_bundle_exact_price_guard_fixup_pushed_ready_for_owner_recheck`
- branch: `beta-ui-redesign-controlled-preview`

## Exact Change

Added a narrow body-query exact-price guard in `api/search.py`.

New behavior:

- if the query is already in strong body-intent context
- and the query text explicitly signals a multi-item / bundle / accessory-attached object
  - `with`
  - `with lens`
  - `with accessories`
  - `kit`
  - `lens kit`
  - `body lens kit`
  - `body+lens`
  - `body + lens`
  - `set`
  - `bundle`
- then clean body-only `exact_base_model` price unlock is blocked

What did **not** change:

- parser behavior
- ranking
- pricing thresholds
- duplicate / outlier policy
- AA / 2매 / FLE / FLE2 logic
- DR / Rigid logic
- broad body-vs-lens category separation behavior

## Files Changed

| File | Change |
| --- | --- |
| `api/search.py` | Added explicit body bundle signal guard before body exact-base price unlock |
| `data/admin/p3_beta_mvp_body_bundle_exact_price_guard_fixup_v0.md` | This report |

## Before / After — P0 Queries

| Query | Before | After |
| --- | --- | --- |
| `Leica M10 lens kit` | `allowed=True`, `scope=exact_base_model`, body-only rows used for price | `allowed=False`, `scope=insufficient_exact_data`, no used-for-price rows |
| `Leica M10 body lens kit` | `allowed=True`, `scope=exact_base_model`, body-only rows used for price | `allowed=False`, `scope=insufficient_exact_data`, no used-for-price rows |
| `Leica M11 lens kit` | `allowed=True`, `scope=exact_base_model`, body-only rows used for price | `allowed=False`, `scope=insufficient_exact_data`, no used-for-price rows |
| `Leica Q2 with accessories` | `allowed=True`, `scope=exact_base_model`, body-only rows used for price | `allowed=False`, `scope=insufficient_exact_data`, no used-for-price rows |
| `Leica M6 with lens` | `allowed=True`, `scope=exact_base_model`, body-only rows used for price | `allowed=False`, `scope=insufficient_exact_data`, no used-for-price rows |

## Exact Base Model Body Price Unlock Blocked

Confirmed blocked for all primary P0 queries:

| Query | Detected | After price state | Used-for-price visible |
| --- | --- | --- | --- |
| `Leica M10 lens kit` | `Leica M10 body` | `allowed=False`, `scope=insufficient_exact_data` | `0` |
| `Leica M10 body lens kit` | `Leica M10 body` | `allowed=False`, `scope=insufficient_exact_data` | `0` |
| `Leica M11 lens kit` | `Leica M11 body` | `allowed=False`, `scope=insufficient_exact_data` | `0` |
| `Leica Q2 with accessories` | `Leica Q2 body` | `allowed=False`, `scope=insufficient_exact_data` | `0` |
| `Leica M6 with lens` | `Leica M6 body` | `allowed=False`, `scope=insufficient_exact_data` | `0` |

Representative top rows stay visible, but are no longer used for exact body price:

- `Leica M10 lens kit`
  - `[위탁] M10 Monochrom 'Leitz Wetzlar' Edition`
  - `[중고] Leica M10 홀스터`
  - `[중고] Leica M10 하프케이스 (Brown)`
- `Leica M11 lens kit`
  - `Leica M11 Glossy Black Paint Finish`
  - `Leica M11 Silver`
  - `Leica M11 Monochrome Black`
- `Leica Q2 with accessories`
  - `Leica Q2 007 Edition`
  - `Leica Q2 Black`
  - `[중고] Leica Q2 Monochrome`

## Already-Safe Bundle Queries

These remained locked / conservative:

| Query | Result |
| --- | --- |
| `Leica M10 with summicron 50` | `allowed=False`, `scope=blocked_boundary_conflict` |
| `Leica M10 summicron 50 kit` | `allowed=False`, `scope=blocked_boundary_conflict` |
| `Leica M11 with summilux 35` | `allowed=False`, `scope=blocked_boundary_conflict` |
| `Leica MP with summicron 35` | `allowed=False`, `scope=blocked_boundary_conflict` |
| `Leica M body lens kit` | `allowed=False`, `scope=insufficient_exact_data` |

## Clean Body Regression Table

These remained unchanged:

| Query | Result |
| --- | --- |
| `Leica M10` | `allowed=True`, `scope=exact_base_model` |
| `Leica M10 body` | `allowed=True`, `scope=exact_base_model` |
| `Leica M11` | `allowed=True`, `scope=exact_base_model` |
| `Leica M11 body` | `allowed=True`, `scope=exact_base_model` |
| `Leica M6` | `allowed=True`, `scope=exact_base_model` |
| `Leica M6 body` | `allowed=True`, `scope=exact_base_model` |
| `Leica Q2` | `allowed=True`, `scope=exact_base_model` |
| `Leica MP body` | still conservative: `allowed=False`, `scope=insufficient_exact_data` |

## Lens / Accessory Regression Table

No side effects reproduced:

| Query | Result |
| --- | --- |
| `Summicron-M 50` | unchanged, conservative |
| `Summilux-M 35` | unchanged, exact-base behavior preserved |
| `Noctilux 50 1.2` | unchanged, locked |
| `Leica hood 12585` | unchanged, locked |
| `Leica M adapter L` | unchanged, locked |

## Recent Boundary Regression Table

Closed boundary fixes remained safe:

| Query | Result |
| --- | --- |
| `Summilux-M 35 2매` | PASS |
| `Summilux-M 35 FLE2` | PASS |
| `50 cron dr` | PASS |
| `Leica Summicron 50 rigid` | PASS |
| `Summicron-M 50 rigid` | PASS |

## Remaining Issues

1. This fix blocks wrong exact body price for explicit bundle / with-lens / with-accessories queries, but does **not** yet improve first-screen ranking.
2. Bundle phrasing still collapses to body-oriented detection text such as `Leica M10 body`.
3. Accessory / adapter intent modeling remains weak for:
   - `Leica 12585`
   - `Leica 12504`
   - several adapter queries
4. Those are lower-priority follow-ups than the P0 exact-price contamination that this patch addresses.

## Verification

- `python3 -m py_compile query_parser.py search_service.py query_resolver.py api/search.py` passed
- primary P0 validation queries passed
- clean body regressions passed
- lens/accessory regressions passed
- recent boundary spot checks passed
