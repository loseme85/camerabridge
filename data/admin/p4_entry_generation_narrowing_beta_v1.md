# P4 Entry Generation Narrowing Beta v1

- Branch: `p4-entry-generation-narrowing-beta`
- Previous preview URL: `https://camerabridge-f8g3e3hi6-camerabridge.vercel.app`
- Branch alias URL: `https://camerabridge-git-p4-entry-generation-narrow-88fc63-camerabridge.vercel.app`
- Previous deployment commit: `808f10ef15a97d2f7aa5abccbd1f5ac6f7515175`
- Production untouched: confirmed

## Executive Summary

This beta-only round moved the search layer from broad parent-model pricing toward generation/version-level pricing for priority Leica body and lens families.

Owner authenticated smoke on preview exposed one real HOLD gap:

- backend top-level generation override was correct locally
- preview UI still preferred stale nested `market_entry_policy` fields for market summary rendering
- this let broad parent queries like `Leica M6` and `Leica M10` keep showing old parent/base-model price state in the card shell even though top-level response policy had already been narrowed
- exact-generation labels such as `Leica 50mm Summicron-M Type IV` and `Leica 50mm Summicron-M Dual Range` also stayed broader than intended in the market-entry header

Fixup status for this follow-up:

- local fix applied
- production remains untouched
- new preview deployment: pending push for this fixup
- previous preview remains useful as the reproduced HOLD reference
- production remains untouched
- local recheck after fix is PASS
- preview smoke after this fixup: pending new deployment + owner recheck

The core change is:

- broad parent queries such as `Leica M6`, `Leica M10`, and `Leica Q2` now block direct price summary unlock and ask for generation selection
- explicit generation queries such as `Leica M6 TTL`, `Leica M10-P`, `Leica Q2 Monochrom`, `Leica 50mm Summicron-M Type IV`, and `Leica 50mm Noctilux 1.0 E60` now project generation-aware match labels and generation-aware price usage labels
- visible same-base but different-generation rows remain visible, but are explicitly marked reference-only
- obvious body-accessory titles such as `Leica M10 홀스터` and `Leica M10 하프케이스` are now projected as accessory/boundary rows inside the generation layer, so they stop looking like clean body price evidence

## Changed Files

- `api/search.py`
- `index.html`
- `app/templates/index.html`
- `beta.html`
- `app/templates/beta.html`
- `tests/test_search_endpoint.py`
- `tests/test_search_ui.py`
- `data/admin/p4_entry_generation_narrowing_beta_v1.md`

## Preview Deployment

- Branch: `p4-entry-generation-narrowing-beta`
- Previous deployment URL: `https://camerabridge-f8g3e3hi6-camerabridge.vercel.app`
- Previous branch alias: `https://camerabridge-git-p4-entry-generation-narrow-88fc63-camerabridge.vercel.app`
- Previous deployment state: `READY`
- Previous deployment commit: `808f10ef15a97d2f7aa5abccbd1f5ac6f7515175`
- New deployment for this fixup: pending push
- Production untouched: confirmed

## Owner HOLD Root Cause

Owner smoke HOLD was caused by two coupled issues:

1. UI policy precedence bug
   - `getMarketEntryPolicy()` preferred `state.response.market_entry_policy` as a frozen object
   - generation narrowing later updated top-level response fields such as:
     - `price_summary_allowed`
     - `price_scope`
     - `display_price_summary_allowed`
     - `display_price_band`
     - `display_query_review`
   - the preview card shell still rendered stale nested policy values

2. Generation projection sync gap
   - exact-generation overrides did not fully synchronize:
     - `market_entry_title`
     - `display_price_band`
     - `display_broader_reference_allowed`
   - this made `Type IV` and `Dual Range` still look broader than intended in preview

## Current Fixup

This follow-up added:

- API-side synchronization from generation-narrowed top-level response fields back into `market_entry_policy`
- broad parent hard override for:
  - `price_summary_allowed = false`
  - `display_price_summary_allowed = false`
  - `price_scope = generation_disambiguation_required`
  - `display_price_band = Generation selection needed`
  - `display_broader_reference_allowed = false`
- exact-generation market-entry title sync:
  - `Leica M6 TTL`
  - `Leica M10-P`
  - `Leica 50mm Summicron-M Type IV`
  - `Leica 50mm Summicron-M Dual Range`
- exact-generation band sync so exact-generation rows no longer inherit broad base-model display band
- frontend merge logic so top-level runtime overrides take precedence over nested stale policy fields

## Local Recheck After Owner HOLD

### Leica M6

- Before owner smoke:
  - preview showed body market summary and used price evidence
- After local fix:
  - `price_summary_allowed = false`
  - `price_scope = generation_disambiguation_required`
  - `display_price_band = Generation selection needed`
  - `used_for_price = 0`
  - suggestions:
    - `Leica M6 Classic`
    - `Leica M6 TTL`
    - `Leica M6 Reissue`
    - `Leica M6 Millennium / Limited`

### Leica M10

- Before owner smoke:
  - preview showed broad M10 body market summary
- After local fix:
  - `price_summary_allowed = false`
  - `price_scope = generation_disambiguation_required`
  - `display_price_band = Generation selection needed`
  - `used_for_price = 0`

### Leica M10-P

- After local fix:
  - `market_entry_title = Leica M10-P`
  - `price_scope = exact_generation`
  - `display_price_summary_allowed = true`
  - `display_broader_reference_allowed = false`

### Leica 50mm Summicron-M Type IV

- Before owner smoke:
  - market entry still read too broadly as `Summicron-M`
- After local fix:
  - `market_entry_title = Leica 50mm Summicron-M Type IV`
  - `price_scope = exact_generation`
  - `display_price_band_source = exact_generation`
  - `display_broader_reference_allowed = false`

### Leica 50mm Dual Range

- Before owner smoke:
  - market entry still looked broad / generic
- After local fix:
  - `market_entry_title = Leica 50mm Summicron-M Dual Range`
  - `price_scope = exact_generation`
  - no broad reference fallback is displayed
  - `display_broader_reference_allowed = false`

### Leica 35mm Summicron pre-ASPH

- After local fix:
  - remains locked
  - `price_scope = insufficient_exact_generation_data`
  - `display_price_summary_allowed = false`

## Preview Smoke Status

Preview verification attempt summary:

- Direct preview API fetch attempted for:
  - `Leica M10`
  - `Leica M10-P`
  - `Leica 50mm Summicron-M Type IV`
- Direct preview page fetch attempted for:
  - `/?q=Leica+M10`
- Result:
  - preview requests redirect to the Vercel login / SSO gate
  - path-specific `_vercel_share` access links were generated successfully
  - however, this deployment still resolved to the Vercel login flow during automated verification

Current decision:

- Local logic/card exposure: `PASS`
- Preview deployment creation: `PASS`
- Preview smoke: `PENDING (access-gated)`
- Owner smoke: `PENDING`

## Local vs Preview Difference

- Local:
  - full API and card-level behavior verified
  - broad parent queries lock to `generation_disambiguation_required`
  - exact generation queries promote clean same-generation rows only
- Preview:
  - deployed commit matches local code commit
  - deployment is `READY`
  - automated smoke could not reach app payload because the preview is still protected behind Vercel login/SSO
  - no backend/runtime regression was directly observed, but app-response parity is still pending owner-visible or authenticated verification

## Entry Generation Registry Summary

Added generation taxonomy for:

- Body:
  - Leica M6 Classic / TTL / Reissue / Millennium-Limited
  - Leica M10 / M10-P / M10-R / M10 Monochrom
  - Leica M11 / M11-P / M11-D / M11 Monochrom
  - Leica Q2 / Q2 Monochrom
  - Leica Q3 / Q3 43
- Lens:
  - Leica 50mm Summicron-M Rigid / Dual Range / Type IV / Version V / APO
  - Leica 35mm Summicron-M 8-element / pre-ASPH / ASPH / ASPH II
  - Leica 35mm Summilux-M pre-ASPH / ASPH / FLE
  - Leica 50mm Noctilux-M 1.0 E58 / 1.0 E60 / 0.95 / 1.2 reissue

## Exact Change

### 1. Query-side generation narrowing

- Added query generation hints for:
  - `M6 TTL`
  - `M6 Reissue`
  - `M6 Classic`
  - `M10-P`
  - `M10-R`
  - `M10 Monochrom`
  - `Q2 Monochrom`
  - `Q3 43`
  - `Summicron 50 Type IV / KOB / Version V / Rigid / Dual Range`
  - `Noctilux 50 0.95 / 1.0 E58 / 1.0 E60 / 1.2 reissue`
- Added compact recovery for `Leica 50mm Dual Range` even when the query omits `Summicron`

### 2. Broad parent-model protection

Broad parent queries now block direct price bands when the query matches a generation-aware group and multiple meaningful generations are present.

Current protected broad groups:

- `Leica M6`
- `Leica M10`
- `Leica M11`
- `Leica Q2`
- `Leica Q3`
- `Leica 50mm Summicron-M` broad family group

Result:

- `price_scope = generation_disambiguation_required`
- `price_summary_allowed = false`
- generation chooser chips are exposed in `ui_hints`
- visible rows are still shown, but marked reference-only

### 3. Generation-aware result projection

Each result now receives:

- `query_match_level`
- `query_match_score`
- `query_match_label`
- `query_entry_key`
- `result_entry_key`
- `matched_tokens`
- `missing_tokens`
- `conflicting_tokens`
- `price_usage_role`
- `price_usage_label`

Generation-aware examples:

- `Exact generation match`
- `Same base model, different generation`
- `Reference only — same family`
- `Not used for price — boundary conflict`
- `Used for exact-generation price`
- `Reference only — not used for Leica M6 TTL price`
- `Reference only — generation selection needed`

### 4. Accessory projection inside the generation layer

Without changing the upstream normalized data, obvious accessory titles are now projected as accessory rows inside the entry-generation layer when their titles contain accessory terms such as:

- `hood`
- `adapter`
- `grip`
- `handgrip`
- `case`
- `holster`
- `strap`
- `filter`
- `cap`
- `battery`
- `charger`
- Korean equivalents such as `홀스터`, `하프케이스`, `케이스`, `후드`, `어댑터`

This changed rows such as:

- `[중고] Leica M10 홀스터`
- `[중고] Leica M10 하프케이스 (Brown)`

from same-base-looking body rows into boundary-conflict accessory rows for generation-aware search display.

### 5. Result card exposure

QA/internal and beta cards now expose:

- `Detected entry`
- `Search match`
- `Used for price`
- `Exclusion reason`
- `Generation confidence`

This sits alongside the existing model/family/mount/category/price-role information.

## Before / After Highlights

### Before

- `Leica M6`
  - broad parent query was over-interpreted as a specific generation
  - Classic / TTL / Reissue / limited rows were mixed into a single market band
- `Leica M10`
  - broad parent query could still unlock a parent-model-style price band
  - accessory titles like `Leica M10 홀스터` looked too close to body evidence
- `Leica M10-P`
  - body intent was previously unstable in earlier preview rounds
- `Leica 50mm Dual Range`
  - could remain broad or under-modeled

### After

- `Leica M6`
  - detected as `Leica M6`
  - `price_scope = generation_disambiguation_required`
  - chips: `Leica M6 Classic`, `Leica M6 TTL`, `Leica M6 Reissue`, `Leica M6 Millennium / Limited`
- `Leica M10`
  - detected as `Leica M10`
  - `price_scope = generation_disambiguation_required`
  - accessory titles stay visible but now show boundary-conflict style projection
- `Leica M10-P`
  - detected as `Leica M10-P`
  - exact-generation rows rank first
  - top rows show `Used for exact-generation price`
- `Leica 50mm Dual Range`
  - detected as `Leica 50mm Summicron-M Dual Range`
  - different Summicron 50 generations are visible but no longer look like the same generation

## Smoke Summary

| Query | Detected | Price scope | Allowed | Notes |
|---|---|---:|---:|---|
| `Leica M6` | `Leica M6` | `generation_disambiguation_required` | No | broad parent blocked |
| `Leica M6 Classic` | `Leica M6 Classic` | `exact_generation` | Yes | classic exact rows used |
| `Leica M6 TTL` | `Leica M6 TTL` | `exact_generation` | Yes | TTL exact rows used |
| `Leica M6 Reissue` | `Leica M6 Reissue` | `exact_generation` | Yes | reissue exact rows used |
| `Leica M10` | `Leica M10` | `generation_disambiguation_required` | No | broad parent blocked |
| `Leica M10-P` | `Leica M10-P` | `exact_generation` | Yes | exact-generation rows pinned |
| `Leica M10-R` | `Leica M10-R` | `exact_generation` | Yes | exact-generation rows pinned |
| `Leica M10 Monochrom` | `Leica M10 Monochrom` | `exact_generation` | Yes | monochrom exact rows pinned |
| `Leica M11-P` | `Leica M11-P` | `exact_generation` | Yes | exact-generation rows pinned |
| `Leica Q2` | `Leica Q2` | `generation_disambiguation_required` | No | broad parent blocked |
| `Leica Q2 Monochrom` | `Leica Q2 Monochrom` | `exact_generation` | Yes | monochrom exact rows pinned |
| `Leica 50mm Summicron-M Type IV` | `Leica 50mm Summicron-M Type IV` | `exact_generation` | Yes | Type IV exact |
| `Leica 50 Summicron KOB` | `Leica 50mm Summicron-M Type IV` | `exact_generation` | Yes | KOB alias recovered |
| `Leica 50mm Summicron Rigid` | `Leica 50mm Summicron-M Rigid` | `exact_generation` | Yes | rigid exact |
| `Leica 50mm Dual Range` | `Leica 50mm Summicron-M Dual Range` | `exact_generation` | Yes | dual-range recovery added |
| `Leica 35mm Summicron ASPH` | `Leica 35mm Summicron-M ASPH` | `exact_generation` | Yes | ASPH exact |
| `Leica 35mm Summicron pre-ASPH` | `Leica 35mm Summicron-M pre-ASPH` | `insufficient_exact_generation_data` | No | still thin / noisy |
| `Leica 50mm Noctilux 0.95` | `Leica 50mm Noctilux-M 0.95` | `exact_generation` | Yes | 0.95 exact |
| `Leica 50mm Noctilux 1.0 E60` | `Leica 50mm Noctilux-M 1.0 E60` | `exact_generation` | Yes | E60 exact |

## Query-Level Top Results

### Leica M6
- Detected: `Leica M6`
- Price scope: `generation_disambiguation_required`
- Match distribution: `{'exact_base_model': 10}`
- Top 10 shows Classic / TTL / Reissue / Limited rows together, all as:
  - `Same base model generation candidate`
  - `Reference only — generation selection needed`

Top visible titles:
1. Leica M6 (0.72x) (Black, 10404)
2. Leica M6 Classic Silver x0.72 [Big Logo]
3. Leica M6 TTL Silver 0.72x
4. Leica M6 Re-Issue Black
5. Leica M6 TTL Olive Green x0.85 [Custom]
6. Leica M6 Titan Classic 0.72x
7. [위탁] Leica M6 TTL 0.72 millennium (Black paint) -2000대 한정-
8. [중고] Leica M6 millennium(Black paint)
9. [중고] Leica M6 Classic Reissue
10. LEICA M6 TTL sn.2499

### Leica M10
- Detected: `Leica M10`
- Price scope: `generation_disambiguation_required`
- Match distribution: `{'exact_base_model': 5, 'boundary_conflict': 5}`
- Broad price is blocked
- accessory rows now surface as boundary-conflict/reference-only rows rather than pseudo-clean body evidence

Top visible titles:
1. Leica M10 Silver
2. [위탁] M10 Monochrom 'Leitz Wetzlar' Edition
3. [위탁] Leica M10 (Black)
4. [중고] Leica M10 (Silver)
5. [중고] Leica M10 (Silver)
6. [중고] Leica M10 홀스터
7. [중고] Leica M10 하프케이스 (Brown)
8. [중고] Leica M10 하프케이스 (Black)
9. [중고] Leica M10 하프케이스 (Black)
10. [중고] Leica M10 하프케이스 (Brown)

Representative row projection:

- `Leica M10 Silver`
  - entry: `Leica M10`
  - match: `Same base model generation candidate`
  - used_for_price: `false`
- `[중고] Leica M10 홀스터`
  - entry: `Leica M10 accessory`
  - match: `Not used for price — boundary conflict`
  - used_for_price: `false`

### Leica M10-P
- Detected: `Leica M10-P`
- Price scope: `exact_generation`
- Match distribution: `{'exact_generation': 10}`

Top visible titles:
1. LEICA M10-P sn.5506
2. LEICA M10-P sn.5488
3. LEICA M10-P sn.5333
4. LEICA M10-P sn.5501
5. LEICA M10-P sn.5333
6. LEICA M10-P Edition 'Safari' sn.5492
7. LEICA M10-P sn.5333
8. LEICA M10-P sn.5325
9. LEICA M10-P sn.5492
10. LEICA M10-P sn.5491

Top exact rows:

- `LEICA M10-P sn.5506`
  - match: `Exact generation match`
  - used_for_price: `true`
  - price role: `Used for exact-generation price`

### Leica Q2
- Detected: `Leica Q2`
- Price scope: `generation_disambiguation_required`
- Match distribution: `{'exact_base_model': 10}`

Top visible titles:
1. Leica Q2 (Daniel Craig x Greg Williams) (19058 / 19062)
2. Leica Q2 Monochrom (19055)
3. Leica Q2 Monochrom (19055)
4. Leica Q2 (19050)
5. Leica Q2 (19050)
6. Leica Q2 007 Edition
7. Leica Q2 Black
8. [위탁] Leica Q2
9. [중고] Leica Q2 Monochrome
10. [중고] Leica Q2 x Helinox Special package Edition

### Leica 50mm Summicron-M Type IV
- Detected: `Leica 50mm Summicron-M Type IV`
- Price scope: `exact_generation`
- Match distribution: `{'exact_generation': 3, 'exact_base_model': 2, 'unknown': 5}`

Top visible titles:
1. Leica 50mm f2 Summicron-M (Type IV) (Black, 11819)
2. Leica 50mm f2 Summicron-M (Type IV) (Black, 11819)
3. Leica 50mm f2 Summicron-M (Type IV) (Black, 11819)
4. Leica 50mm f2 Summicron-M (Type V) (Black, 11826 / 11719)
5. Leica 50mm f2 Summicron (Type II, Dual Range) (SOOIC-MN / SOMNI / 11918 / 11318)
6. Leica 50mm f2 Summicron (Type II) (Silver, SOOIC-MS / SOSIC / 11118 / 11618 / 11818)
7. Leica 50mm f2 Summicron (Type III) (11817)
8. Leica 50mm f2 Summicron (Type III) (11817)
9. Leica 50mm f2 Summicron (Type III) (11817)
10. Leica 50mm f2 Summicron (Type II) (Silver, SOOIC-MS / SOSIC / 11118 / 11618 / 11818)

### Leica 50mm Dual Range
- Detected: `Leica 50mm Summicron-M Dual Range`
- Price scope: `exact_generation`
- Match distribution: `{'exact_generation': 1, 'exact_base_model': 4, 'unknown': 5}`

Top visible titles:
1. Leica 50mm f2 Summicron (Type II, Dual Range) (SOOIC-MN / SOMNI / 11918 / 11318)
2. Leica 50mm f2 Summicron-M (Type IV) (Black, 11819)
3. Leica 50mm f2 Summicron-M (Type V) (Black, 11826 / 11719)
4. Leica 50mm f2 Summicron-M (Type IV) (Black, 11819)
5. Leica 50mm f2 Summicron-M (Type IV) (Black, 11819)
6. Leica 50mm f2 Summicron (Type II) (Silver, SOOIC-MS / SOSIC / 11118 / 11618 / 11818)
7. Leica 50mm f2 Summicron (Type III) (11817)
8. Leica 50mm f2 Summicron (Type III) (11817)
9. Leica 50mm f2 Summicron (Type III) (11817)
10. Leica 50mm f2 Summicron (Type II) (Silver, SOOIC-MS / SOSIC / 11118 / 11618 / 11818)

### Leica 35mm Summicron pre-ASPH
- Detected: `Leica 35mm Summicron-M pre-ASPH`
- Price scope: `insufficient_exact_generation_data`
- Match distribution: `{'exact_base_model': 1, 'boundary_conflict': 1, 'unknown': 8}`

Top visible titles:
1. Leica M 35mm f2 Summicron ASPH Black Paint Millenium
2. 신품 호환 Leica 14043 Hood Cover for M 35mm f2 Summicron, M 28mm f2.8 Elmarit
3. [중고] L 35/2 Summicron ASPH (Silver)
4. [위탁] L 35/2 Summicron 6군8매 (Black repaint)
5. [중고] L 35/2 Summicron 6군8매 (Black repaint)
6. [중고] L 35/2 Summicron Canada (Silver)
7. LEICA 35mm F2 ASPH Screwmount M39 SUMMICRON-L sn.3867
8. Leica 35mm f2 Summicron (Type III) (11309)
9. Leica 35mm f2 Summicron (Type III) (11309)
10. Leica 35mm f2 Summicron-M (Type IV) (Black, 11310)

### Leica 50mm Noctilux 1.0 E60
- Detected: `Leica 50mm Noctilux-M 1.0 E60`
- Price scope: `exact_generation`
- Match distribution: `{'exact_generation': 7, 'exact_base_model': 1, 'unknown': 2}`

Top visible titles:
1. [중고] M 50/1.0 Noctilux 3세대 E60 (Black)
2. [중고] M 50/1.0 Noctilux 4세대 6bit (Black)
3. [중고] M 50/1.0 Noctilux 4세대 (Black)
4. [중고] M 50/1.0 Noctilux 4세대 (Black)
5. [중고] M 50/1.0 Noctilux 4세대 (Black)
6. [중고] M 50/1.0 Noctilux 4세대 (Black)
7. [중고] M 50/1.0 Noctilux 4세대 (Black)
8. [중고] M 50/1.0 Noctilux 2세대 E58 (Black)
9. LEICA 50mm F1.0 NOCTILUX-M sn.3442
10. LEICA 50mm F1.0 NOCTILUX-M sn.3928

## Query Match Level Distribution Highlights

- broad protected body queries:
  - mostly `exact_base_model` generation candidates
  - no price rows used
- exact body generation queries:
  - dominated by `exact_generation`
- exact lens generation queries:
  - `exact_generation` rows lead
  - different generations fall to `Same base model, different generation`
- weak/sparse generation queries:
  - `Leica 35mm Summicron pre-ASPH` still falls back to mixed broad references and remains locked

## Used-for-Price Row Examples

- `Leica M6 TTL`
  - `Leica M6 TTL Silver 0.72x`
  - `LEICA M6 TTL sn.2499`
  - `Used for exact-generation price`
- `Leica M10-P`
  - `LEICA M10-P sn.5506`
  - `Used for exact-generation price`
- `Leica 50mm Summicron-M Type IV`
  - `Leica 50mm f2 Summicron-M (Type IV) (Black, 11819)`
  - `Used for exact-generation price`
- `Leica 50mm Noctilux 1.0 E60`
  - `[중고] M 50/1.0 Noctilux 3세대 E60 (Black)`
  - `Used for exact-generation price`

## Excluded / Reference-Only Examples

- `Leica M6` broad query
  - all visible generations:
    - `Reference only — generation selection needed`
- `Leica M10` broad query
  - `[중고] Leica M10 홀스터`
    - entry: `Leica M10 accessory`
    - match: `Not used for price — boundary conflict`
- `Leica 50mm Summicron-M Type IV`
  - `Leica 50mm f2 Summicron-M (Type V) (Black, 11826 / 11719)`
    - `Same base model, different generation`
    - `Reference only — not used for Leica 50mm Summicron-M Type IV price`
- `Leica 50mm Noctilux 1.0 E60`
  - `[중고] M 50/1.0 Noctilux 2세대 E58 (Black)`
    - `Same base model, different generation`
    - `Reference only — not used for Leica 50mm Noctilux-M 1.0 E60 price`

## Validation Commands

```bash
python3 -m py_compile api/search.py query_parser.py query_resolver.py search_index.py search_service.py app/app.py entry_generation.py
python3 -c 'from api.search import endpoint_response; ... smoke queries ...'
python3 -c "from app.app import app; app.run(host='127.0.0.1', port=5001, debug=False)"
```

## Local QA URL

- Local QA/internal URL: `http://127.0.0.1:5001`

## Known Remaining Risks

- `Leica 35mm Summicron pre-ASPH` remains weak-pass only:
  - exact-generation lock is correct
  - result quality is still sparse and broad references dominate
- `Leica 50mm Dual Range` now resolves correctly, but exact visible evidence is still thin on the first screen
- limited/special-edition rows are still visible inside the same generation family and depend on existing duplicate/outlier/source quality rules
- upstream normalized category fields are not rewritten by this round; accessory/body cleanup here is generation-layer projection only
- no preview deployment has been created yet in this round, so browser-level verification is still local-only

## Production Guardrail

- `camerabridge.vercel.app` untouched
- no production alias change
- no production deployment
- no main data overwrite
