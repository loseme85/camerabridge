# P3 Kamerastore Allowed-After-Validation Live Guard v1

## Executive Summary

- Scope: scoped Kamerastore-only live guard implementation
- Source under change: `Kamerastore`
- `price_evidence_policy` updated from `blocked_initially` to `allowed_after_validation`
- `price_eligible` promotion was **not** performed
- No preview/prod deploy
- No broad ranking/parser/alias/canonical refactor
- Existing active-source price behavior remained intact in spot checks

This round moved Kamerastore from a source-wide hard block into a guarded live path:

1. clean Kamerastore rows may now enter price evidence candidate pools
2. accessory / bundle / missing canonical / duplicate-excluded rows still stay out
3. scoped Leica body-family effective projection remains active for Kamerastore evaluation
4. duplicate cluster suppression now allows at most one representative candidate per cluster key

Final judgment: **PASS**

## 수정 파일 목록

- `api/search.py`
- `data/config/source_registry_v1.json`
- `data/admin/p3_kamerastore_allowed_after_validation_live_guard_v1.md`

## 1. source_registry 변경 내용

Kamerastore entry:

- `status`: `limited_crawl` (unchanged)
- `price_evidence_policy`: `blocked_initially -> allowed_after_validation`

Important:

- this is **not** `price_eligible`
- Kamerastore is still under source-specific live guard

## 2. Live Guard 구현 내용

Implemented a Kamerastore-only guarded live path in `api/search.py`.

### 2.1 Source-policy gate

Behavior now differs by source policy:

- `blocked_initially`
  - source remains fully blocked from live price evidence
  - shadow-only review stays available

- `allowed_after_validation`
  - row-level live guard runs
  - only guard-passing rows can enter live price evidence candidate pools

### 2.2 Common helper path

Added a shared Kamerastore guard core snapshot so shadow/live do not drift on:

- effective body-family projection
- accessory detection
- bundle detection
- missing canonical detection
- duplicate cluster detection
- representative selection

### 2.3 Scoped Leica body-family projection

Kamerastore live evaluation still uses scoped effective projection for:

- `Leica M Monochrom`
- `Leica M-E`
- `Leica MDa`
- `Leica M (Typ 262)`
- `Leica M (Typ 240)`
- `Leica M-P (Typ 240)`
- `Leica Q2 Monochrom`
- `Leica Q2`
- `Leica T (Typ 701)`
- `Leica S (Typ 007)`

This projection is used for Kamerastore guard evaluation only, not as a broad parser refactor.

## 3. 필수 Live Guard 규칙

### 3.1 Accessory hard block

Blocked when:

- category is `Accessory`
- or title contains:
  - `hood`
  - `adapter`
  - `grip`
  - `handgrip`
  - `thumb`
  - `case`
  - `strap`
  - `filter`
  - `cap`
  - `battery`
  - `charger`
  - `meter`

### 3.2 Bundle hard block

Blocked when title contains:

- ` + `
- `kit`
- `bundle`
- `set`
- `with`

### 3.3 Missing canonical hard block

Blocked when:

- `model_canonical` is missing

### 3.4 Classification drift hard block

Blocked when:

- title is body-like
- but effective category is not `Body`

### 3.5 Duplicate cluster suppression

Cluster key:

- `(title_raw, model_canonical, condition_raw)`

Rule:

- cluster당 최대 1개만 live candidate
- other cluster siblings remain excluded with `duplicate`

Representative priority:

1. guard-clean row
2. better condition
   - `Certified > Restored > Not Passed`
3. later `crawl_time`
4. stable `source_url`

## 4. Guard Pass / Exclude Count

Current live guard snapshot:

- `row_count = 106`
- `allowed_candidate_count = 83`
- `excluded_candidate_count = 23`

Exclusion reason counts:

- `accessory = 9`
- `bundle = 13`
- `duplicate = 11`
- `missing_canonical = 1`

Interpretation:

- earlier shadow cleanup snapshot was stricter because all duplicate-cluster rows stayed excluded
- live mode now keeps one representative candidate where safe

## 5. Duplicate Suppression 결과

Current duplicate summary:

- `duplicate_cluster_count = 9`
- `duplicate_cluster_row_count = 20`
- `duplicate_cluster_representative_count = 8`

Observed behavior:

- duplicate-excluded rows remain visible when relevant
- but excluded siblings do not enter used-for-price path
- no excluded duplicate row was observed with `used_for_price = True` in representative query validation

## 6. Representative Query 결과

## 6.1 Leica 50mm Summicron-M Type IV

Observed:

- clean Summicron rows entered live price evidence
- duplicate-excluded siblings remained `used_for_price = False`

Examples:

- `Leica 50mm f2 Summicron-M (Type IV) (Black, 11819)`
  - guard: `allowed_candidate`
  - used_for_price: `True`

- duplicate sibling:
  - guard: `excluded_candidate`
  - reason: `duplicate`
  - used_for_price: `False`

## 6.2 Leica 35mm Summicron

Observed:

- allowed candidates remain visible
- duplicate-excluded rows remain visible but not used
- query-level price state itself stayed conservative in this validation

## 6.3 Leica M Monochrom

Observed:

- `Leica M Monochrom (Black, 10760)` now evaluates as effective body-family row
- guard status: `allowed_candidate`
- query stayed locked in this validation
- no accessory/bundle Kamerastore row was used for price

## 6.4 Leica M-E / Leica M Typ 240 / Leica M4

Observed:

- effective body-family projection remains active
- compatible body rows can be evaluated as candidates
- query-level locks still apply where exact evidence is thin

## 6.5 Leica Q2

Observed:

- clean `Q2` rows entered live same-base evidence
- duplicate-excluded sibling rows remained `used_for_price = False`

Examples:

- `Leica Q2 (19050)`
  - one representative candidate used
  - duplicate sibling excluded

- `Leica Q2 Monochrom (19055)`
  - one representative candidate used
  - duplicate sibling excluded

## 6.6 Leica Elmarit-R

Observed:

- clean lens rows remained candidate-safe
- accessory-attached bundle row remained excluded

## 6.7 Leica hood / Leica adapter / Leica handgrip

Observed:

- accessory/bundle rows remained excluded
- all tested rows stayed `used_for_price = False`

## 7. 실제 Price Evidence 사용 여부

Kamerastore is now capable of entering live candidate pools under the new policy.

Confirmed examples where guard-passing Kamerastore rows were used:

- `Leica 50mm Summicron-M Type IV`
  - clean allowed candidates used for same-base price

- `Leica Q2`
  - clean allowed candidates used for same-base price

Confirmed excluded examples that remained blocked:

- hood query rows
- adapter-attached bundle rows
- handgrip-attached rows
- duplicate-excluded siblings in lens/body clusters

## 8. 제외 Row가 used_for_price=False로 유지되는지

Validation result:

- excluded live-guard Kamerastore rows with `used_for_price = True`: `0`

This was checked across:

- `Leica 50mm Summicron-M Type IV`
- `Leica 35mm Summicron`
- `Leica M Monochrom`
- `Leica M-E`
- `Leica M Typ 240`
- `Leica M4`
- `Leica Q2`
- `Leica Elmarit-R`
- `Leica hood`
- `Leica adapter`
- `Leica handgrip`

## 9. Existing Active Source Regression 결과

No-write syntax check:

- `api/search.py` OK
- `search_index.py` OK
- `app/app.py` OK
- `final_resolution_pipeline.py` OK

Note:

- direct `python3 -m py_compile ...` attempted first, but local sandbox blocked `__pycache__` write in this thread
- replaced with no-write `compile(...)` validation

Smoke queries:

- `Leica M10`
- `Leica M11-P`
- `Leica 50 Summicron Rigid`
- `Leica Noctilux 0.95`

Observed:

- no Kamerastore live-guard metadata appeared on these top rows
- no obvious regression in top-result pricing state
- no active-source-only query was forced into Kamerastore contamination

## 10. 아직 price_eligible이 아닌 이유

Kamerastore is still **not** `price_eligible` because:

1. this round only enables guarded live candidacy, not full source trust
2. duplicate suppression is source-specific and still needs broader confidence over time
3. sold-history quality is still narrow in the current pilot snapshot
4. the source still needs more longitudinal validation before being treated as a fully trusted price source

## 11. Final Judgment

- policy change to `allowed_after_validation`: applied
- live guard: applied
- excluded rows remain blocked from price evidence
- duplicate cluster suppression: applied
- existing active-source regression: no obvious issue in spot checks

Final judgment: **PASS**
