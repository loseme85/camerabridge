# P3 Beta MVP — M10 Accessory And Monochrom Price Guard Fixup v1

- Decision status: `m10_accessory_and_monochrom_price_guard_fixup_v1_pushed_ready_for_owner_recheck`
- Branch: `beta-ui-redesign-controlled-preview`

## Exact change

This fix adds a narrow price-scope guard in [`api/search.py`](/Users/changdaepark/Desktop/LEICA%20SEARCH/api/search.py) for two M10 body-query edge cases:

1. Explicit accessory-attached M10 body queries:
   - block clean `exact_base_model` body price unlock when the query contains strong accessory terms such as `protector`, `case`, `half case`, `holster`, `handgrip`, `grip`, `thumb grip`, `strap`, `cover`, `charger`, `battery`

2. `M10 Monochrom` query guard:
   - when the query explicitly includes `Monochrom` / `M10M`, filter body exact-base pricing to Monochrom-compatible rows only
   - if that Monochrom-compatible pool is insufficient, keep price locked
   - do not allow generic `M10` body rows to price a `Monochrom` query

No ranking polish was attempted in this round.

## Before / after — `Leica M10 protector`

### Before

- Detected candidate: `Leica M10 body`
- `price_summary_allowed = True`
- `price_scope = exact_base_model`
- visible generic M10 body rows used for price:
  - `[위탁] Leica M10 (Black)`
  - `[중고] Leica M10 (Silver)`
  - `[중고] Leica M10 (Silver)`

### After

- Detected candidate: `Leica M10 body`
- `price_summary_allowed = False`
- `price_scope = insufficient_exact_data`
- visible `used_for_price = 0`
- body rows may remain visible, but now show:
  - `Same base model result is visible, but not used as exact price`

### Top visible rows after

1. `[위탁] M10 Monochrom 'Leitz Wetzlar' Edition`
2. `[중고] Leica M10 홀스터`
3. `[중고] Leica M10 하프케이스 (Brown)`
4. `[중고] Leica M10 하프케이스 (Black)`
5. `[위탁] Leica M10 (Black)`

Result: the accessory/protector query no longer unlocks clean M10 body price.

## Before / after — `Leica M10 Monochrom`

### Before

- Detected candidate: `Leica M10 body`
- `price_summary_allowed = True`
- `price_scope = exact_base_model`
- generic M10 body rows were used for price
- Monochrom-specific row was visible, but broad M10 price still opened

### After

- Detected candidate: `Leica M10 body`
- `price_summary_allowed = False`
- `price_scope = insufficient_exact_data`
- visible `used_for_price = 0`
- generic M10 body rows are not used for Monochrom price

### Top visible rows after

1. `[위탁] M10 Monochrom 'Leitz Wetzlar' Edition`
2. `[중고] Leica M10 홀스터`
3. `[중고] Leica M10 하프케이스 (Brown)`
4. `[중고] Leica M10 하프케이스 (Black)`
5. `[위탁] Leica M10 (Black)`

Result: broad M10 exact-base pricing is now blocked for `M10 Monochrom`.

## Accessory control table

| Query | Detected candidate | price_summary_allowed | price_scope | used_for_price count | Result |
| --- | --- | --- | --- | ---: | --- |
| `Leica M10 handgrip` | `Leica grip candidate` | `False` | `insufficient_exact_data` | 0 | `PASS` |
| `Leica M10 half case` | `Leica case candidate` | `False` | `insufficient_exact_data` | 0 | `PASS` |
| `Leica M10 strap` | `Leica strap candidate` | `False` | `insufficient_exact_data` | 0 | `PASS` |
| `Leica M10 thumb grip` | `Leica grip candidate` | `False` | `insufficient_exact_data` | 0 | `PASS` |
| `Leica M10 protector` | `Leica M10 body` | `False` | `insufficient_exact_data` | 0 | `PASS` |

Accessory rows are still visible where relevant, but none of these queries opens clean body-only exact price.

## Clean M10 body control table

| Query | Detected candidate | price_summary_allowed | price_scope | used_for_price count | Accessory used for price | Result |
| --- | --- | --- | --- | ---: | --- | --- |
| `Leica M10` | `Leica M10 body` | `True` | `exact_base_model` | 3 | No | `PASS` |
| `Leica M10 body` | `Leica M10 body` | `True` | `exact_base_model` | 3 | No | `PASS` |
| `M10 body` | `Leica M10 body` | `False` | `insufficient_exact_data` | 0 | No | `PASS` |
| `Leica M10 black` | `Leica M10 body` | `True` | `exact_base_model` | 3 | No | `PASS` |
| `Leica M10 silver` | `Leica M10 body` | `True` | `exact_base_model` | 0 | No | `PASS` |

Price safety for clean body queries remains unchanged.

## Variant control table

| Query | Detected candidate | price_summary_allowed | price_scope | used_for_price count | Generic M10 body rows used for Monochrom price | Result |
| --- | --- | --- | --- | ---: | --- | --- |
| `Leica M10 Monochrom` | `Leica M10 body` | `False` | `insufficient_exact_data` | 0 | No | `PASS` |
| `Leica M10-P` | `Leica lens candidate` | `False` | `blocked_weak_only` | 0 | No | `PASS` |
| `Leica M10-R` | `Leica M10-R body` | `True` | `exact_base_model` | 0 | No | `PASS` |

## Bundle/body guard regression table

| Query | price_summary_allowed | price_scope | used_for_price count | Result |
| --- | --- | --- | ---: | --- |
| `Leica M10 lens kit` | `False` | `insufficient_exact_data` | 0 | `PASS` |
| `Leica M10 body lens kit` | `False` | `insufficient_exact_data` | 0 | `PASS` |
| `Leica M11 lens kit` | `False` | `insufficient_exact_data` | 0 | `PASS` |
| `Leica Q2 with accessories` | `False` | `insufficient_exact_data` | 0 | `PASS` |
| `Leica M6 with lens` | `False` | `insufficient_exact_data` | 0 | `PASS` |

## Recent safety regression table

| Query | Detected candidate | price_summary_allowed | price_scope | used_for_price count | Result |
| --- | --- | --- | --- | ---: | --- |
| `Summilux-M 35 FLE2` | `Leica Summilux-M 35 FLE2 candidate` | `True` | `exact_variant` | 5 | `PASS` |
| `Summilux-M 35` | `Leica Summilux-M 35 candidate` | `False` | `insufficient_exact_data` | 0 | `PASS` |
| `50 cron dr` | `Leica Summicron 50 Dual Range candidate` | `False` | `blocked_weak_only` | 0 | `PASS` |
| `Leica Summicron 50 rigid` | `Leica Summicron 50 Rigid candidate` | `False` | `insufficient_exact_data` | 0 | `PASS` |
| `Leica 12585` | `Leica 12585 hood candidate` | `False` | `insufficient_exact_data` | 0 | `PASS` |
| `Summicron 50 hood` | `Leica Summicron 50 hood candidate` | `False` | `blocked_boundary_conflict` | 0 | `PASS` |

## Confirmation

- Parser behavior was not changed broadly
- Ranking polish was not attempted
- Pricing thresholds were not changed
- Duplicate / outlier policy was not changed
- Existing bundle guard behavior was preserved
- Existing Summilux / Summicron safety fixes remained intact

## Remaining issue

The original `Leica M10` first-screen accessory noise remains as a separate P1 polish issue.

This round only fixed the unsafe price-scope cases:

- explicit accessory-attached `Leica M10 protector`
- broad `Leica M10 Monochrom` body-price fallback

First-screen ranking cleanup for clean `Leica M10` body queries should be handled separately.
