# P3 Beta MVP — Separate QA And Beta UI Shell Fixup v1

- Decision status: `separate_qa_and_beta_ui_shell_fixup_v1_pushed_ready_for_owner_recheck`
- Branch: `beta-ui-redesign-controlled-preview`

## Exact change

This change adds a separate limited-beta UI shell while keeping the current QA/internal UI intact.

No parser, search, ranking, pricing, evidence-role, price-role, or exact-price unlock logic was changed.

Only the presentation layer changed:

- existing QA UI remains the current shell
- new `/beta` route renders a cleaner, simplified beta-facing shell
- both routes use the same `/api/search` endpoint and the same response payload

## Route / component structure

### Routes

- `/` -> existing QA UI (`index.html`)
- `/search` -> existing QA UI (`index.html`)
- `/qa` -> explicit QA alias (`index.html`)
- `/beta` -> new beta UI shell (`beta.html`)
- `/api/search` -> unchanged shared search API

### Files changed

- [`app/app.py`](/Users/changdaepark/Desktop/LEICA%20SEARCH/app/app.py)
- [`app/templates/beta.html`](/Users/changdaepark/Desktop/LEICA%20SEARCH/app/templates/beta.html)
- [`beta.html`](/Users/changdaepark/Desktop/LEICA%20SEARCH/beta.html)
- [`data/admin/p3_beta_mvp_separate_qa_and_beta_ui_shell_fixup_v1.md`](/Users/changdaepark/Desktop/LEICA%20SEARCH/data/admin/p3_beta_mvp_separate_qa_and_beta_ui_shell_fixup_v1.md)

## QA UI unchanged confirmation

The QA shell was intentionally left unchanged:

- no edits to [`app/templates/index.html`](/Users/changdaepark/Desktop/LEICA%20SEARCH/app/templates/index.html)
- no edits to [`index.html`](/Users/changdaepark/Desktop/LEICA%20SEARCH/index.html)
- `/qa` explicitly points at the current QA template

That preserves owner/internal validation behavior:

- technical query review
- evidence role
- price role
- boundary conflict wording
- QA/debug-heavy explanation style

## Beta UI textual state summary

Direct Safari verification confirmed `/beta` renders a separate shell with:

- topbar pills:
  - `Limited Beta`
  - `Leica 중심 테스트`
  - `동일 검색 로직`
- beta hero title:
  - `프리미엄 카메라 중고 시세와 매물을 한 곳에서 확인하세요.`
- beta disclaimer blocks:
  - Leica-centered limited beta
  - reference-only valuation framing
  - source-check reminder
  - locked-price expectation for rare models
- beta search placeholder:
  - `예: Summilux-M 35 FLE2, 50 cron dr, Leica M10, Leica 12585`
- beta example chips:
  - `Summilux-M 35 FLE2`
  - `50 cron dr`
  - `Leica M10`
  - `Leica 12585`
  - `Summicron 50 hood`

For result screens, beta now presents:

- simplified result summary card
- simplified price status wording
- shorter card labels
- `원문 보기` CTA
- collapsed per-card explanation:
  - `왜 이 결과가 보이나요?`

## Label mapping table

| QA/internal label | Beta label |
| --- | --- |
| `Exact variant` | `정확히 맞는 결과` |
| `Exact base model` | `기본 모델 일치` |
| `Same base model` | `같은 계열 참고 결과` |
| `Broader family` | `관련 결과` |
| `Boundary conflict` | `조건이 달라 가격 계산 제외` |
| `Used for exact price` | `가격 계산에 사용됨` |
| `Used for same base model price` | `가격 계산에 사용됨` |
| `Exact variant match visible, but not selected for exact price` | `정확히 맞지만 가격 계산에서는 제외` |
| `Exact match visible, but not enough to unlock price yet` | `정확히 맞지만 가격 계산에서는 제외` |
| `Same base model result is visible, but not used as exact price` | `참고 결과로만 표시` |
| `Not used — Duplicate listing` | `중복 가능성으로 제외` |
| `Not used — Price outlier` | `가격 범위 이상으로 제외` |
| `No usable price` | `가격 계산 불가` |
| `Not used — Accessory, not camera/lens` | `액세서리라 가격 계산에서 제외` |

## QA vs Beta parity table

The beta shell uses the same underlying payload and does not re-rank or re-filter results.

Code-path parity confirmed:

- both templates fetch the same endpoint:
  - `fetch('/api/search?' + params.toString(), ...)`
- both render from the same result array:
  - `state.response.results`
- both preserve the same history/popstate logic
- beta does not introduce any backend fork or beta-only API

Sample shared payload validation:

| Query | Expected shared logic state | Observed shared API state |
| --- | --- | --- |
| `Summilux-M 35 FLE2` | same titles/order, exact_variant pricing | `allowed=True`, `scope=exact_variant`, `used12=5`, `cta12=12` |
| `Summilux-M 35` | same mixed/locked state | `allowed=False`, `scope=insufficient_exact_data`, `used12=0`, `cta12=12` |
| `50 cron dr` | same DR locked/reference behavior | `allowed=False`, `scope=blocked_weak_only`, `used12=0`, `cta12=12` |
| `Leica Summicron 50 rigid` | same rigid guard behavior | `allowed=False`, `scope=insufficient_exact_data`, `used12=0`, `cta12=12` |
| `Leica 12585` | same accessory locked behavior | `allowed=False`, `scope=insufficient_exact_data`, `used12=0`, `cta12=12` |
| `Summicron 50 hood` | same hood locked behavior | `allowed=False`, `scope=blocked_boundary_conflict`, `used12=0`, `cta12=12` |
| `Leica M10` | same clean body exact-base state | `allowed=True`, `scope=exact_base_model`, `used12=3`, `cta12=12` |
| `Leica M10 protector` | same protected locked state | `allowed=False`, `scope=insufficient_exact_data`, `used12=0`, `cta12=12` |
| `Leica M10 Monochrom` | same Monochrom locked state | `allowed=False`, `scope=insufficient_exact_data`, `used12=0`, `cta12=12` |
| `Leica M10 lens kit` | same bundle guard state | `allowed=False`, `scope=insufficient_exact_data`, `used12=0`, `cta12=12` |

Interpretation:

- same result count source
- same result order source
- same price-summary state source
- same used-for-price source
- same source CTA source
- only label/layout differ

## Mobile check

Mobile-specific verification is a `WEAK_PASS`, based on template structure and responsive rules:

- beta shell inherits the existing responsive layout behavior
- cards use the same single-column mobile collapse patterns already present in the QA shell
- labels were shortened
- dense QA role rows were collapsed into a details section
- source CTA remains visible without requiring horizontal scroll

No mobile-only browser overflow regression was introduced in code review.

## Back / Forward check

Beta shell preserves the recently fixed committed-search history behavior because it retains the same history code path as QA:

- committed search uses `historyMode: 'push'`
- initial hydration uses replace semantics
- `popstate` restore logic is unchanged
- sticky search submit still participates in history

Observed:

- committed beta search updated the URL to:
  - `/beta?q=Summilux-M+35+FLE2`

That confirms beta route participation in search-state URL history.

## Sticky search validation

The beta shell preserves the same sticky search behavior because the sticky form wiring was copied intact:

- sticky search form still calls `runSearch(...)`
- sticky search still uses `preserveResultsAnchor: true`
- history entry creation still occurs on committed sticky submit

No beta-only sticky search logic was introduced.

## Source CTA check

Source CTA behavior remains identical at the logic level:

- same `source_url`
- same target behavior
- same source availability

Presentation change only:

- QA: `View source`
- Beta: `원문 보기`

## Confirmation that backend logic was not changed

Not changed in this fix:

- parser
- search API payload shape
- ranking
- evidence role calculation
- price role calculation
- exact-price unlock logic
- duplicate/outlier policy
- result ordering

This was a UI-shell split only.

## Remaining blockers before real limited beta release

This task does **not** approve real limited beta rollout by itself.

Known blockers / follow-ups still matter:

- `Leica M10 protector` / `Leica M10 Monochrom` guard must remain validated on latest preview
- remaining P1 polish such as:
  - M10 first-screen accessory noise
  - adapter/accessory wording polish
  - broad locked-result ranking polish

Also, this task does **not** approve:

- production launch
- production alias connection
- external tester access
- tester links
- production DB writes
- provider / webhook / email actions
