# P3 Kamerastore Link / Price Readiness Audit v1

## Executive Summary

- Scope: read-only audit only after the Kamerastore limited crawl pilot.
- Current source status remains `limited_crawl`.
- Current `price_evidence_policy` remains `blocked_initially`.
- No ranking, parser, alias, canonical, or price logic was changed in this round.

High-level result:

- Detail URLs look live in the sampled set.
- The earlier `timeout` signal does **not** look like mass dead links.
- The stronger root cause is client-method / TLS validation mismatch in the earlier audit path.
- Price fields are clean enough for discovery use.
- Price evidence readiness is **not** ready yet because category / bundle contamination and row classification drift are still present.

Final judgment: **PENDING**

## 1. Detail URL Timeout Root Cause

### 1.1 Sample used

- Raw Kamerastore rows in current dataset: `106`
- Representative detail URL sample checked: `29` unique URLs
  - Intended target was 30, but the bucketed sample produced 29 unique product URLs.

### 1.2 URL normalization check

Checked across raw -> normalized -> resolved:

- Raw Kamerastore rows: `106`
- Normalized Kamerastore rows: `106`
- Resolved Kamerastore rows: `106`
- Raw URL missing from normalized: `0`
- Raw URL missing from resolved: `0`

Observed:

- `https://kamerastore.com` prefix is present.
- `/en-int/` locale segment is present and stable.
- No duplicated locale prefix issue was found.
- No malformed relative product URL was found in the sampled data.
- Raw / normalized / resolved detail URLs matched exactly in the checked set.

Conclusion:

- The current timeout problem does **not** come from URL normalization drift.

## 2. HEAD vs GET vs Browser-like Checks

### 2.1 curl health check results

For the 29 sampled detail URLs:

- `HEAD`: `29 / 29` returned `200`
- `GET`: `29 / 29` returned `200`
- `GET` with browser-like User-Agent: `29 / 29` returned `200`
- Redirected away from product page: `0`
- `403`: `0`
- `404`: `0`
- timeout: `0`

Typical response time:

- HEAD: about `0.8s - 1.7s`
- GET: about `0.4s - 1.8s`
- browser-like GET: about `1.1s - 1.8s`

Sample live URLs:

- `https://kamerastore.com/en-int/products/leica-50mm-f2-summicron-m-type-iv-leica-m-5`
- `https://kamerastore.com/en-int/products/leica-m4-black-paint-leica-m-2`
- `https://kamerastore.com/en-int/products/leica-q2-daniel-craig-x-greg-williams-19058-19062-t140106`

### 2.2 Python client reproduction

The earlier “all timeout” signal appears to have been a client-side audit artifact.

Reproduced with Python `urllib` on representative Kamerastore URLs:

- `urllib HEAD default` -> failed
- `urllib GET default` -> failed
- `urllib GET browser UA` -> failed

Repeated failure detail:

- `URLError`
- `[SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: unable to get local issuer certificate`

When repeated with an unverified TLS context:

- `GET` returned `200`
- Product HTML loaded successfully

Conclusion:

- The earlier timeout/dead-link conclusion should be revised.
- The dominant failure mode is **TLS certificate validation failure in the Python audit client**, not obvious detail-page death.

### 2.3 Browser-context note

- Playwright browser-context open was attempted.
- Local Playwright browser binary was not installed in this thread runtime, so a true Playwright page-open check could not be completed here.
- Fallback evidence from `curl GET` and HTML fetch confirmed live product-page responses.

## 3. Link Survival Sample Result

Sample classification for the 29 checked URLs:

- `alive_200`: `29`
- `valid_redirect`: `0`
- `forbidden_403`: `0`
- `not_found_404`: `0`
- `timeout`: `0`
- `tls_dns_error`: `0` at curl level
- `malformed_url`: `0`

Important nuance:

- Python default client failures were TLS verification failures, not link deletion.

## 4. Price Parse Quality

Current Kamerastore rows in resolved/index:

- Resolved rows: `106`
- Index rows: `106`

Price quality:

- Price parse-like success: `106 / 106`
- Zero / null price rows: `0`
- Currency consistency: `KRW 106 / 106`

Assessment:

- Price text parsing is currently strong enough for discovery display.
- Currency consistency is clean in the current pilot sample.

## 5. Currency Quality

- All 106 Kamerastore rows currently resolve to `KRW`.
- No mixed-currency contamination was observed inside this pilot snapshot.

Caution:

- This is operationally clean for the current branch snapshot, but it is still a transformed output from the current crawl path, not a broad multi-locale validation.

## 6. Sold / Available Status Quality

Resolved sold-status summary:

- `asking`: `106`
- sold / reserved / unknown in resolved output: `0`

Condition field presence:

- `condition_raw` present: `106 / 106`
- Missing condition: `0`

Assessment:

- Current pilot data behaves like active inventory / asking inventory.
- Sold / reserved / historical-state handling is **not** yet meaningfully tested from Kamerastore in this snapshot.

## 7. Category Contamination Result

Resolved category breakdown:

- `Lens`: `55`
- `Body`: `43`
- `Accessory`: `8`

Risky title-pattern counts inside the 106 rows:

- bundle-like titles: `13`
- hood terms: `4`
- adapter terms: `3`
- grip terms: `1`

Examples:

- `Leica M4 (No Serial) (Black Paint, 10402) + Meter MR`
- `Leica M8 (Black, 10701) + M8/M9 Handgrip (14486)`
- `Leica 19mm f2.8 Elmarit-R ... + Leica R - Canon EF Mount Adapter ... + Lens Hood ...`

Observed classification drift examples:

- `Leica M Monochrom (Black, 10760)` -> currently classified as `Lens`, mount `M`, `model_canonical = None`
- `Leica Q2 (Daniel Craig x Greg Williams)` -> classified as `Body`
- `Leica Standard (Model E) (Black Paint)` -> classified as `Body`

Interpretation:

- The dataset is usable for search/discovery exposure.
- It is **not** yet trustworthy enough for price evidence usage because bundle/accessory-attached titles and some body-model rows are still classification-sensitive.

## 8. Representative Canonical Attachment Checks

Direct resolved/index inspection shows:

- `Leica 50mm f2 Summicron-M (Type IV) (Black, 11819)`
  - category: `Lens`
  - mount: `M`
  - model_canonical: `Summicron-M`

- `Leica 35mm f2 Summicron (Type III) (11309)`
  - category: `Lens`
  - mount: `M`
  - model_canonical: `Summicron-M`

- hood-bearing rows found in sample:
  - `4`
  - all currently surface as `Accessory`

Current sample gaps:

- No `M10` row in the 106-row pilot sample
- No `M11-P` row in the 106-row pilot sample
- No `Noctilux 0.95` row in the 106-row pilot sample
- No explicit `case` row in the 106-row pilot sample

Operational takeaway:

- Kamerastore is currently adding discoverable Leica inventory, but the pilot snapshot is still narrow and uneven across major body families.

## 9. Price Evidence Risk if Enabled Today

This round did **not** change policy. Kamerastore remains blocked from price evidence.

If Kamerastore were allowed into the price evidence pool today, the main risk cases would be:

1. Bundle / multi-item inflation
   - `13` bundle-like rows exist in only 106 rows.
   - These include lens + hood, body + meter, body + handgrip, lens + adapter combinations.

2. Classification drift
   - Example: `Leica M Monochrom (Black, 10760)` currently lands as `Lens`.
   - That is not acceptable for automatic price evidence.

3. Duplicate-title clusters
   - `15` duplicate title clusters were found.
   - Examples:
     - `Leica 50mm f2 Summicron-M (Type IV) (Black, 11819)` x3
     - `Leica IIIa + 50mm f3.5 Elmar ...` x3
     - `Leica M (Typ 240) (Black Paint, 10770)` x3
   - This would need explicit duplicate handling before price eligibility.

4. Sold/reference behavior untested
   - All 106 rows are currently `asking`.
   - There is not yet enough evidence here to trust sold/history weighting behavior for this source.

## 10. Kamerastore Promotion Readiness

### Against proposed pass criteria

- link alive or valid redirect >= 85%:
  - **PASS** on curl sample (`29 / 29` alive)

- price parse success >= 95%:
  - **PASS** (`106 / 106`)

- currency consistency >= 95%:
  - **PASS** (`106 / 106 KRW`)

- sold / available status classification possible:
  - **PARTIAL**
  - Asking inventory is clear, but sold/reserved diversity is not demonstrated

- accessory / bundle contamination safely guardable:
  - **PENDING**
  - Current blocked policy is doing the right thing, but the source is not yet safe to graduate

- no regression requirement:
  - No change was made in this round

### Promotion judgment

- `active_source` discovery exposure: already acceptable in limited-crawl form
- `price_eligible`: **not ready**

Recommended current stance:

- Keep `status = limited_crawl`
- Keep `price_evidence_policy = blocked_initially`

## 11. Recommended Next Work

Smallest safe next steps before any price-evidence discussion:

1. Fix client-side link audit method
   - replace Python default TLS audit path with a curl-based or verified-cert-capable method
   - do not treat Python certificate failure as dead-link evidence

2. Run a Kamerastore-specific classification audit
   - focus on:
     - `M Monochrom`
     - body + accessory bundles
     - hood / adapter attached rows
     - duplicate-title clusters

3. Re-audit after a slightly larger limited crawl
   - keep low page cap
   - keep price evidence blocked

4. Only then consider a source-specific price readiness gate
   - duplicate suppression
   - bundle exclusion
   - category hard-guard validation
   - sold/history coverage check

## 12. Final Judgment

**PENDING**

Why not PASS:

- The earlier timeout issue is mostly explained and looks fixable.
- But Kamerastore is still not ready for `price_eligible` promotion because:
  - bundle-like rows are non-trivial (`13 / 106`)
  - accessory contamination exists
  - duplicate-title clusters exist
  - at least one important body-family row (`M Monochrom`) is misclassified
  - sold/history behavior is not yet proven in this source snapshot

Why not HOLD:

- URLs are not broadly dead.
- Raw/normalized/resolved/index flow is intact.
- Discovery/search exposure can continue safely while price evidence remains blocked.
