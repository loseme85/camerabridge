# P3-BETA-MVP-LEICA-HYPHEN-FAMILY-MOUNT-INTENT-FIXUP

## Scope
- Branch: `beta-ui-redesign-controlled-preview`
- Goal: stamp explicit mount intent for narrow Leica hyphen-family tokens at parser/search-intent level

## Files changed
- `/Users/changdaepark/Desktop/LEICA SEARCH/query_parser.py`
- `/Users/changdaepark/Desktop/LEICA SEARCH/search_aliases.py`

## Exact token changes
- `summicron-m` -> family `Summicron` + mount `M`
- `summilux-m` -> family `Summilux` + mount `M`
- `noctilux-m` -> family `Noctilux` + mount `M`
- `elmarit-m` -> family `Elmarit` + mount `M`
- `apo-summicron-m` -> family `APO-Summicron-M` + mount `M`
- `apo-summicron-sl` -> family `APO-Summicron-SL` + mount `SL`
- `summicron-sl` -> family `Summicron` + mount `SL`

## Implementation
- added narrow parser-side mount map for Leica hyphen-family aliases
- when a matching hyphen-family token is consumed as `model_family`, parser now also calls `_set_mount(...)`
- no mount is inferred from bare family tokens

## Before / after

### `Summicron-M 35 ASPH`
- before: `family=Summicron`, `mount=None`
- after: `family=Summicron`, `mount=M`

### `APO-Summicron-M 35 ASPH`
- before: `family=APO-Summicron-M`, `mount=None`
- after: `family=APO-Summicron-M`, `mount=M`

### `Summilux-M 50 ASPH`
- before: `family=Summilux`, `mount=None`
- after: `family=Summilux`, `mount=M`

### `Noctilux-M 50`
- before: `family=Noctilux`, `mount=None`
- after: `family=Noctilux`, `mount=M`

### `Elmarit-M 28 ASPH`
- before: `family=Elmarit`, `mount=None`
- after: `family=Elmarit`, `mount=M`

### `Summicron-SL 35 ASPH`
- before: `family=None`, `mount=None`
- after: `family=Summicron`, `mount=SL`

### `APO-Summicron-SL 90`
- before: `family=APO-Summicron-SL`, `mount=None`
- after: `family=APO-Summicron-SL`, `mount=SL`

## Unsafe broad alias guard
Still unchanged:
- bare `Summicron 35 ASPH` -> `mount=None`
- bare `Summilux 50 ASPH` -> `mount=None`

This fix does **not** infer mount from bare:
- `summicron`
- `summilux`
- `noctilux`
- `elmarit`
- `asph`
- `35`
- `50`
- `tri-elmar`

## Search/runtime smoke result
- `expected_query_mount` now follows explicit hyphen-family Leica queries
- `expected_query_family` remains narrow and mount-aware where existing logic already supports it
- no intentional ranking, pricing, or UI behavior changes were introduced

## Validation run
- `python3 -m py_compile query_parser.py search_aliases.py`
- parser smoke:
  - `Summicron-M 35 ASPH`
  - `APO-Summicron-M 35 ASPH`
  - `Summilux-M 50 ASPH`
  - `Noctilux-M 50`
  - `Elmarit-M 28 ASPH`
  - `Summicron-SL 35 ASPH`
  - `APO-Summicron-SL 90`
  - `bare Summicron 35 ASPH`
  - `bare Summilux 50 ASPH`
- search smoke via `search_from_params(...)` for the same query family

## Result
- `-M` queries now parse explicit `mount=M`
- `-SL` queries now parse explicit `mount=SL`
- bare family queries remain mount-neutral

## Final decision_status
`leica_hyphen_family_mount_intent_fixup_pushed_ready_for_owner_recheck`
