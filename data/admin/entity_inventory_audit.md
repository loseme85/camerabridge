# Entity Inventory Audit - Round 1

Date: 2026-04-23

Scope: read-only audit of the current canonical entity inventory and its relationship to resolved listings/search/admin normalization. No search ranking, classifier, query parser, resolver, service, endpoint, or UI behavior was intentionally changed in this round.

## Executive Summary

The current system does not yet have a populated explicit canonical entity registry. `data/admin/canonical_entities.json` exists, but contains zero stored entities. The admin normalization tool currently derives 682 canonical-like entities from `data/derived/results_resolved_v2.json` at runtime.

That derived inventory is useful for admin lookup, but it is not strong enough to be the long-term basis for exact search or market price tables:

- It only derives Lens and Body entities; Accessory records are excluded.
- It is listing-observed, not product-catalog-driven.
- It has no first-class alias list, price group, generation, release era, aperture, version, reissue/current flag, or structured finish field.
- `system` is not populated in derived entities, so M/R/Q/Compact/SL line reasoning depends mostly on `mount`, `label`, and naming.
- Many high-volume Leica M lens families are too broad for price-table use.
- 1,322 Lens/Body records have no model-canonical entity projection at all.

The highest-priority next step is not another query rule. It is to seed an explicit canonical entity layer for the price-sensitive Leica Lens/Body groups, then attach aliases/dealer rules to those entities.

## Data Sources

| Source | Role | Count / Status |
| --- | --- | --- |
| `data/admin/canonical_entities.json` | Explicit admin-maintained entity registry | 0 entities |
| `normalization_admin.load_canonical_entities()` | Runtime entity source | 682 derived entities |
| `data/derived/results_resolved_v2.json` | Full resolved listing artifact | 7,860 records |
| `data/derived/results_search_index_v1.json` | Compact search-serving artifact | 7,860 records |
| `data/admin/normalization_reviews.json` | Admin review queue | 500 reviews |
| `data/metadata/trusted_metadata.json` | Listing-level trusted overrides | 3 rules |
| `data/metadata/curated_reference.json` | Curated model references | 2 rules |

## Current Inventory Summary

### Resolved Listing Mix

| Category | Records |
| --- | ---: |
| Lens | 4,766 |
| Accessory | 1,713 |
| Body | 1,381 |

### Derived Entity Mix

| Kind | Derived Entities |
| --- | ---: |
| Lens | 479 |
| Body | 203 |
| Accessory | 0 |

### Derived Entity Brand Mix

| Brand | Derived Entities |
| --- | ---: |
| Leica | 623 |
| 3rd Party | 30 |
| Unknown | 29 |

### Derived Entity Mount Mix

| Mount | Derived Entities |
| --- | ---: |
| M | 397 |
| R | 66 |
| Unknown | 52 |
| L | 50 |
| SL | 48 |
| Compact | 35 |
| Q | 14 |
| S | 10 |
| PNS | 9 |
| C/Y | 1 |

### Most Common Variant Tokens

| Variant Token | Derived Entity Count |
| --- | ---: |
| Black | 200 |
| ASPH | 168 |
| Silver | 123 |
| 6bit | 70 |
| Black Paint | 32 |
| Chrome | 32 |
| v4 | 22 |
| v1 | 15 |
| 0.72 | 15 |
| Black Chrome | 14 |
| TTL | 13 |
| FLE | 12 |

These variant tokens are helpful but not equivalent to canonical market entities. For example, `ASPH`, `Black`, and `6bit` are attributes, while `FLE`, `Steel Rim`, `Rigid`, `DR`, `f0.95`, and `Reissue` can define separate price groups.

## Current Entity Structure

Derived entities are projected from final listing output with this shape:

- `kind`
- `brand`
- `mount`
- `system`
- `label`
- `model_raw`
- `model_canonical`
- `focal_length`
- `variant`
- `source`
- `status`
- `id`

Important missing fields for exact search and price-table use:

- `aliases`
- `line`
- `family`
- `aperture`
- `generation`
- `version`
- `release_status`
- `price_group`
- `production_era`
- `finish`
- `special_edition`
- `market_segment`
- `entity_confidence`

## Coverage Gaps

### Gap 1: Explicit Entity Registry Is Empty

The explicit registry is currently a scaffold, not an inventory. All practical entities are derived from current listings, so any absent listing or misclassified listing disappears from admin lookup.

Classification: A, D

Recommended action: seed explicit canonical entities for core price groups before expanding dealer rules aggressively.

### Gap 2: Accessory Entities Are Not Represented

The inventory derives only Lens and Body entities. Hood/filter/adapter/finder search has been improved, but those accessory families are not first-class canonical entities.

Classification: A for admin normalization support, E for price-table priority unless accessory pricing becomes a core feature.

Recommended action: later add accessory entity families only after Lens/Body price groups are stable.

### Gap 3: High-Volume Leica M Lens Groups Are Too Broad

Large listing clusters are currently grouped by family/focal/variant in ways that still mix price groups.

Examples:

| Group | Records | Why Too Broad |
| --- | ---: | --- |
| Leica M Summilux-M 50 | 236 | ASPH/current, pre-ASPH v1-v4, Classic/Reissue, LHSA/Black Paint all appear in one broad family/focal space |
| Leica M Summilux-M 35 | 205 | pre-ASPH, Steel Rim original/reissue, ASPH, FLE/FLE II, Titan/special finishes need separation |
| Leica M Summicron-M 35 | 291 | ASPH, pre-ASPH v2/v3/v4/KOB, APO, black paint/LHSA variants mix |
| Leica M Summicron-M 50 | 261 | Rigid, DR, v2/v3/v4/v5, APO, 50th/MP Classic need separation |
| Leica M Noctilux 50 | 80 | f1.2 original/reissue, f1.0, f0.95 ASPH are separate market groups |
| Leica M Elmarit-M 28 | 54 | 1st/2nd/3rd/4th and ASPH should not share one price group |

Classification: D

Recommended action: create explicit canonical entities for these as price-table anchor entities.

### Gap 4: Body Lines Need Price-Group Separation

Body shorthand search now works, but canonical entities still need explicit price groups.

Examples:

| Group | Records / Signals | Required Separation |
| --- | --- | --- |
| M6 | 186 M6 records; 51 TTL signals; Classic/Reissue and Black Paint signals present | M6 Classic, M6 TTL, M6 Reissue, Millennium/LHSA/special editions |
| MP | 88 MP records; Black Paint, LHSA, 50th, Hermes, Classic signals present | MP standard, MP LHSA, MP3/LHSA, MP 50th, Hermes/special editions |
| M3/M2/M4/M5 | high user-search value | base body generations and common variants |
| Q/Q2/Q3 | strong production search coverage but accessory pollution exists in raw listing pool | Q, Q2, Q2 Monochrom/edition, Q3, Q3 43 if present |
| D-LUX/V-LUX/C-LUX/Sofort | compact line query has been normalized, but explicit alias coverage is weak | product-line entities plus model-specific variants |

Classification: A, D

Recommended action: add explicit body entities for M/Q/R/Barnack/Compact market groups.

### Gap 5: Canonical Lookup Does Not Share Query Parser Alias Knowledge

Admin canonical entity lookup is literal token matching over derived entity fields. It does not understand many user/dealer aliases.

Observed lookup misses:

| Query | Current Canonical Lookup Result |
| --- | --- |
| `m 50 lux asph` | no result |
| `50lux asph` | no result |
| `m 35 cron v4` | no result |
| `35cron v4` | no result |
| `noctilux 1.2` | no result |
| `dlux 8` | no result |
| `barnack` | no result |
| `light lens lab 35 8 element` | no result |
| `voigtlander 35 ultron` | no result |

Classification: B

Recommended action: add `aliases` to canonical entities and make admin lookup use alias tokens. Do not solve this with dealer rules unless the alias is dealer-specific.

### Gap 6: 1,322 Lens/Body Records Do Not Project To Any Entity

Lens/Body records with no `model_canonical` or `model_raw` cannot become derived canonical entities.

| Signature | Missing Records | Likely Layer |
| --- | ---: | --- |
| SL2 | 102 | classifier/category/model QA, not entity only |
| M10 | 83 | classifier/category/model QA, not entity only |
| M11 | 47 | classifier/category/model QA, not entity only |
| Light Lens Lab | 33 | entity/model coverage plus alias |
| Sigma | 27 | third-party model coverage |
| Voigtlander | 18 | third-party model coverage |
| SL3 | 16 | classifier/category/model QA |
| TTArtisan | 11 | third-party model coverage |
| M-Monochrom | 10 | body model coverage |

Classification: mixed A/B plus separate classifier/category QA for body-as-lens misclassifications.

Recommended action: do not hide these in search. For inventory, explicitly seed important Leica body entities and third-party high-volume lens entities; separately schedule classifier/model QA for SL2/SL3/M10/M11-as-Lens cases.

## Dealer Rule vs Entity Expansion

| Problem Type | Use Entity Expansion | Use Dealer Rule | Notes |
| --- | --- | --- | --- |
| `Summilux-M 50 ASPH` vs pre-ASPH | Yes | No | Market price group difference |
| `Noctilux 50 f0.95` vs `f1.0` vs `f1.2` | Yes | No | Aperture defines entity/price group |
| `M6 Classic` vs `M6 TTL` vs `M6 Reissue` | Yes | No | Body model market groups |
| Dealer abbreviates `D-LUX` as `DLUX` globally | Entity alias | Maybe | If global, entity alias; if dealer-specific spelling, dealer rule |
| Dealer writes `blkpt` for Black Paint | No | Yes | Dealer vocabulary normalization |
| Dealer-specific `finder set` bundle phrasing | No | Yes | Pattern meaning depends on dealer/title style |
| Listing-level wrong category from source | No | Maybe trusted metadata | If one-off listing, trusted metadata; if systemic, classifier QA |
| `M 50/1.4 ASPH` canonical lookup miss | Entity alias | No | Common market shorthand |
| Third-party model names like Light Lens Lab / Voigtlander | Yes for high-volume groups | Maybe | Entity first for price groups, dealer rule for quirky spelling |

## Immediate Entity Top N

These should be seeded as explicit canonical entities before more dealer-rule accumulation.

1. Leica M Summilux-M 50 price groups
   - ASPH/current
   - pre-ASPH v1/v2/v3/v4
   - Classic/Reissue
   - Black Paint/LHSA/special editions as separate entity or special-edition overlay

2. Leica M Summilux-M 35 price groups
   - pre-ASPH Steel Rim/original
   - Steel Rim Reissue
   - ASPH pre-FLE
   - FLE / FLE II
   - Titan/special editions as overlay

3. Leica M Summicron-M 35 price groups
   - pre-ASPH v2/v3/v4/KOB
   - ASPH
   - APO-Summicron-M 35
   - LHSA/Black Paint/50th as special overlays where needed

4. Leica M Summicron-M 50 price groups
   - Rigid
   - DR
   - v2/v3/v4/v5
   - APO-Summicron-M 50
   - 50th/MP Classic special editions

5. Leica M Noctilux 50 price groups
   - f1.2 original
   - f1.2 reissue
   - f1.0
   - f0.95 ASPH

6. Leica M Elmarit-M 28 price groups
   - 1st/9-element
   - 2nd/3rd/4th
   - ASPH

7. Leica M body price groups
   - M6 Classic
   - M6 TTL
   - M6 Reissue
   - MP standard
   - MP3/LHSA and MP special editions

8. Leica Q and compact body groups
   - Q / Q2 / Q2 Monochrom / Q3 / Q3 43 if present
   - D-LUX 8, D-LUX line, V-LUX line, C-LUX line, Sofort

9. Barnack body groups
   - IIIc / IIIf / IIIg
   - Barnack as line alias, not a single entity

10. High-volume third-party M lens groups
   - Light Lens Lab 35/2 8-element
   - Light Lens Lab 50/2 Rigid/Elcan style
   - Voigtlander Nokton / Ultron / Heliar common groups

## Price-Table Must-Split Candidates

| Candidate | Reason |
| --- | --- |
| Summilux-M 50 ASPH vs pre-ASPH | Large price spread and different optical era |
| Summilux-M 35 Steel Rim original vs Steel Rim Reissue | Similar title tokens, different market behavior |
| Summilux-M 35 FLE vs non-FLE ASPH | Common modern market split |
| Summicron-M 35 v4/KOB vs ASPH vs APO | Same family/focal, very different price behavior |
| Summicron-M 50 Rigid vs DR vs modern v4/v5 vs APO | Same focal/family, distinct collector/usage pricing |
| Noctilux 50 f1.2 vs f1.0 vs f0.95 | Aperture/generation is the market group |
| Elmarit-M 28 ASPH vs pre-ASPH generations | Modern ASPH pricing differs from vintage versions |
| M6 Classic vs TTL vs Reissue | Same body shorthand, separate market groups |
| MP standard vs MP3/LHSA/Hermes/50th | Special editions should not pollute standard MP price |
| Q2 vs Q3 vs compact accessories | Same Q tokens, different body generations/accessories |

## Launch Priority

### Before Public Price Table

1. Populate explicit canonical entities for the Top N Leica Lens/Body groups.
2. Add alias support to canonical entities and admin lookup.
3. Add `price_group`, `generation`, `release_status`, `aperture`, and `aliases` fields to the canonical entity schema.
4. Keep dealer rules as normalization overlays pointing into explicit entities, not as the source of market truth.
5. Schedule separate classifier/model QA for high-volume body-as-lens misses like SL2/SL3/M10/M11.

### Can Wait Until After First Price Table

1. Accessory canonical entities for hood/filter/adapter/finder.
2. Rare code-only finder/accessory kits.
3. Deep third-party catalog expansion beyond observed high-volume groups.
4. One-off special finishes unless they have enough sold/asking data to form a market group.

## Recommended Next Round

Add an explicit canonical entity schema upgrade and seed file, but keep it narrow:

- Add 20-40 explicit Leica Lens/Body entities covering the Top N price groups.
- Add `aliases`, `price_group`, `generation`, `release_status`, and `aperture`.
- Make admin canonical lookup use explicit aliases before falling back to derived entities.
- Do not run bulk auto-generation or automatic approval yet.

This will give dealer corrections a stable target and will make future price-table grouping much safer.
