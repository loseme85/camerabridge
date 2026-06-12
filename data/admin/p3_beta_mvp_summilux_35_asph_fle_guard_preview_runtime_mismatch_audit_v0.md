# P3-BETA-MVP-SUMMILUX-35-ASPH-FLE-GUARD-PREVIEW-RUNTIME-MISMATCH-AUDIT v0

- branch: `beta-ui-redesign-controlled-preview`
- task: `SUMMILUX-35-ASPH-FLE-GUARD-PREVIEW-RUNTIME-MISMATCH-AUDIT`
- app logic changed: `false`

## Executive summary

Latest preview runtime does **not** reproduce the owner-reported FLE contamination.

Both:

- latest preview deployment URL, and
- branch preview alias

return `Summilux-M 35 ASPH` evidence where `FLE` / `FLE II` / `FLE2` rows are:

- `Evidence role: Exact base model`
- `Price role: Same base model result is visible, but not used as exact price`
- `used_for_price = false`

So the current deployed preview runtime appears aligned with local HEAD.

## Commit / deployment alignment

### Local HEAD

- branch: `beta-ui-redesign-controlled-preview`
- local HEAD SHA: `04d04c79ecb14f0fbded462a3145aaf2a8b6687e`

### Latest preview deployment

From Vercel deployment metadata for project `camerabridge`:

- deployment id: `dpl_726564US3xAAxPBsswA8kmXeoTqA`
- deployment url: `https://camerabridge-adghmag69-camerabridge.vercel.app`
- branch alias: `https://camerabridge-git-beta-ui-redesign-controlle-5e3ca4-camerabridge.vercel.app`
- deployment state: `READY`
- deployment commit SHA: `04d04c79ecb14f0fbded462a3145aaf2a8b6687e`
- deployment commit message: `docs: record Summilux 35 FLE guard regression recheck`

Conclusion:

- latest deployed preview commit SHA matches local HEAD SHA

## Runtime path used by preview

The preview runtime path for the owner query is:

- frontend template: `app/templates/index.html` mirrored to `index.html`
- frontend fetch path: relative `GET /api/search`
- backend runtime entry: `api/search.py`

Current card rendering path uses:

- `state.response.display_visible_result_evidence`

for:

- `Evidence role`
- `Price role`
- `Reason`

It does **not** currently read those values from raw `results[*]` fields when evidence projection exists.

## Local runtime recheck

Query checked:

- `Summilux-M 35 ASPH`

Parsed query intent:

- family: `Summilux`
- mount: `M`
- focal: `35`
- aperture: `None`
- variant tokens: `['ASPH']`

## First 24 visible cards for `Summilux-M 35 ASPH`

| idx | title | parsed row variants | has_fle | has_fle2 | evidence role | price role | used_for_price | reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | Leica M 35mm f1.4 Summilux ASPH 4th Titan | `['ASPH','v4']` | false | false | Exact variant | Used for exact price | true | `[]` |
| 1 | Leica M 35mm f1.4 Summilux ASPH 4th Silver | `['ASPH','Silver','v4']` | false | false | Exact variant | Used for exact price | true | `[]` |
| 2 | 신품 Leica M 35mm f1.4 Summilux ASPH 6bit FLE II Black | `['FLE','ASPH','Black','6bit']` | true | true | Exact base model | Same base model result is visible, but not used as exact price | false | `[]` |
| 3 | Leica M 35mm f1.4 Summilux ASPH 4th 6bit Black | `['ASPH','Black','v4','6bit']` | false | false | Exact variant | Used for exact price | true | `[]` |
| 4 | Leica M 35mm f1.4 Summilux ASPH 6bit FLE II Black | `['FLE','ASPH','Black','6bit']` | true | true | Exact base model | Same base model result is visible, but not used as exact price | false | `[]` |
| 5 | [위탁] M 35/1.4 Summilux ASPH FLE (Black) | `['FLE','ASPH','Black']` | true | false | Exact base model | Same base model result is visible, but not used as exact price | false | `[]` |
| 6 | [중고] M 35/1.4 Summilux ASPH FLE II (Black) | `['FLE','ASPH','Black']` | true | true | Exact base model | Same base model result is visible, but not used as exact price | false | `[]` |
| 7 | [중고] M 35/1.4 Summilux ASPH FLE II (Black) | `['FLE','ASPH','Black']` | true | true | Exact base model | Same base model result is visible, but not used as exact price | false | `[]` |
| 8 | [중고] M 35/1.4 Summilux ASPH 4세대 (Black) | `['ASPH','Black','v4']` | false | false | Exact variant | Used for exact price | true | `[]` |
| 9 | [위탁] M 35/1.4 Summilux ASPH FLE2 (Black) | `['FLE','ASPH','Black']` | true | true | Exact base model | Same base model result is visible, but not used as exact price | false | `[]` |
| 10 | [위탁] M 35/1.4 Summilux ASPH 6bit New (Black) | `['ASPH','Black','6bit']` | false | false | Exact variant | Used for exact price | true | `[]` |
| 11 | [중고] M 35/1.4 Summilux ASPH 6bit New (Black) | `['ASPH','Black','6bit']` | false | false | Exact variant | Used for exact price | true | `[]` |
| 12 | [중고] Summilux-M 35mm f/1.4 ASPH (Black) | `['ASPH','Black']` | false | false | Exact variant | Used for exact price | true | `[]` |
| 13 | [중고] M 35/1.4 Summilux ASPH 6bit New (Silver) | `['ASPH','Silver','6bit']` | false | false | Exact variant | Used for exact price | true | `[]` |
| 14 | [중고] M 35/1.4 Summilux ASPH 4세대 (Black) | `['ASPH','Black','v4']` | false | false | Exact variant | Used for exact price | true | `[]` |
| 15 | [중고] M 35/1.4 Summilux ASPH 4세대 (Black) | `['ASPH','Black','v4']` | false | false | Exact variant | Used for exact price | true | `[]` |
| 16 | [중고] M 35/1.4 Summilux ASPH NEW (Black) | `['ASPH','Black']` | false | false | Exact variant | Used for exact price | true | `[]` |
| 17 | [위탁] M 35/1.4 Summilux ASPH 4세대 (Silver) | `['ASPH','Silver','v4']` | false | false | Exact variant | Used for exact price | true | `[]` |
| 18 | [위탁] M 35/1.4 Summilux ASPH 6bit FLE (Black) | `['FLE','ASPH','Black','6bit']` | true | false | Exact base model | Same base model result is visible, but not used as exact price | false | `[]` |
| 19 | [중고] M 35/1.4 Summilux ASPH 4세대 (Black) | `['ASPH','Black','v4']` | false | false | Exact variant | Used for exact price | true | `[]` |
| 20 | [위탁] M 35/1.4 Summilux ASPH 6bit FLE (Black) | `['FLE','ASPH','Black','6bit']` | true | false | Exact base model | Same base model result is visible, but not used as exact price | false | `[]` |
| 21 | [중고] M 35/1.4 Summilux ASPH 4세대 (Silver) | `['ASPH','Silver','v4']` | false | false | Exact variant | Used for exact price | true | `[]` |
| 22 | [중고] M 35/1.4 Summilux ASPH FLE II (Black) | `['FLE','ASPH','Black']` | true | true | Exact base model | Same base model result is visible, but not used as exact price | false | `[]` |
| 23 | [중고] M 35/1.4 Summilux ASPH FLE (Silver) | `['FLE','ASPH','Silver']` | true | false | Exact base model | Same base model result is visible, but not used as exact price | false | `[]` |

## Preview API recheck

### Deployment URL

Checked:

- `https://camerabridge-adghmag69-camerabridge.vercel.app/api/search?q=Summilux-M%2035%20ASPH&limit=24`

Observed:

- preview API matches local runtime
- `display_visible_result_evidence` marks FLE rows as `Exact base model`
- `used_for_price = false` for FLE rows

### Branch alias

Checked:

- `https://camerabridge-git-beta-ui-redesign-controlle-5e3ca4-camerabridge.vercel.app/api/search?q=Summilux-M%2035%20ASPH&limit=24`

Observed:

- branch alias also matches local runtime
- FLE / FLE II / FLE2 rows are not exact and not used for price

## Important finding: raw result match data still looks exact

Although `display_visible_result_evidence` is correct, raw `results[*]` still show positive-only variant matching in score breakdown:

- query variant: `ASPH`
- row variant: `['FLE', 'ASPH', ...]`
- raw score breakdown still awards variant exactness because row contains `ASPH`

That means:

- if any old UI path, stale frontend bundle, or alternate card renderer reads from raw `results[*]` instead of `display_visible_result_evidence`, it could still show the wrong owner-facing state

This is the most likely explanation for the owner screenshot if the screenshot really came from a preview page tied to this branch family.

## Guard checks requested

### `Summilux-M 35 aspherical`

- still parses as AA candidate

### `Summilux 35 Aspherical`

- still parses as AA candidate

### `35 lux aspherical`

- still parses as AA candidate

### `Summilux-M 35 FLE`

- FLE rows remain `Exact variant`
- exact-price eligible rows remain exact for explicit FLE query

### `35 lux fle`

- FLE rows remain `Exact variant`

## Cause analysis

### Ruled out

1. stale latest preview deployment SHA  
   - ruled out for the latest preview deployment and branch alias checked here

2. FLE2 token not covered by current guard  
   - ruled out in current local + deployed API response  
   - `FLE2` rows are correctly demoted

3. row variant extraction missing FLE on current runtime path  
   - ruled out for sampled rows  
   - FLE rows carry parsed variants including `FLE`

4. exact_variant_pool admission still allowing FLE rows on current runtime path  
   - ruled out on current local + deployed API response

### Most likely remaining explanation

- owner screenshot came from:
  - an earlier preview deployment, or
  - a stale browser session / cached frontend bundle / older rendered response path

Secondary structural risk still present:

- raw `results[*]` still contain exact-looking score breakdown for FLE rows under ordinary ASPH query
- current correct owner-facing state depends on the UI using `display_visible_result_evidence`

## Smallest safe follow-up if owner still reproduces

No code change was applied in this round because latest preview API already behaves correctly.

If owner still reproduces the exact wrong card state on a current preview page, the smallest next step is:

1. verify the exact preview URL in the screenshot
2. verify whether the page response is using the current card renderer path
3. if needed, harden card rendering further so owner-facing role rows can only come from `display_visible_result_evidence`, never from raw match-score fields

## Files changed

- `data/admin/p3_beta_mvp_summilux_35_asph_fle_guard_preview_runtime_mismatch_audit_v0.md`

## Validation run

- local HEAD SHA check
- Vercel latest deployment metadata check
- local `Summilux-M 35 ASPH` 24-row evidence table
- latest deployment preview API fetch
- branch alias preview API fetch
- guard spot checks:
  - `Summilux-M 35 aspherical`
  - `Summilux 35 Aspherical`
  - `35 lux aspherical`
  - `Summilux-M 35 FLE`
  - `35 lux fle`

## Final decision

`decision_status = summilux_35_asph_fle_guard_preview_runtime_mismatch_audit_completed_ready_for_owner_review`
