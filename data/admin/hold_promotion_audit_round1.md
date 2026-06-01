# Hold Promotion Audit - Round 1

Date: 2026-04-25

Scope: read-heavy audit for three A-grade hold candidates:

1. Summilux 50 ASPH new
2. Summilux 35 ASPH close-focus generation
3. Noctilux 50 f/1.0 internal split
   - E58
   - E60
   - V3 built-in hood

This round did not change main search/classifier/query/search-service behavior. The goal here is narrower: decide whether each hold candidate is mature enough to be treated as a price-table core entity.

## Executive Summary

| Target | Search/Normalization Split | Market Split Evidence | Recommendation | Final |
| --- | --- | --- | --- | --- |
| Summilux 50 ASPH new | Yes | Too thin in current local listing pool | Keep hold | `hold` |
| Summilux 35 ASPH close-focus generation | Yes | Strong enough in current local listing pool | Promote when explicit seed row is added | `core` recommended |
| Noctilux 50 f/1.0 E58 / E60 / V3 | Yes | Too sparse for current price-table separation | Keep hold | `hold` |

## Important Current Seed-State Note

Two of the three audit targets are not yet explicit rows in the current A-grade seed files:

- `Summilux 50 ASPH new` is not yet a separate seed row from the broader `seed_summilux_50_asph`.
- `Summilux 35 ASPH close-focus generation` is not yet a separate seed row in `summilux_35.json`.
- `Noctilux 50 f/1.0 E58` exists as a seed row and is currently `hold`.
- `Noctilux 50 f/1.0 E60` and `Noctilux 50 f/1.0 V3 built-in hood` are not yet separate seed rows.

So this round is primarily a promotion recommendation audit, not a bulk seed-edit round.

## Evidence Base

### Official / literature sources used

- Leica Summilux-M 50 f/1.4 ASPH. 2023 press release:
  [Leica press release PDF](https://leica-camera.com/sites/default/files/2023-04/press_release_summilux_m-series-_leica_summilux-m_50_f_1.4_asph.pdf)
  - states 11 aperture blades instead of 9
  - closest focusing distance extended from 70 cm to 45 cm
  - describes the lens as technically and optically refined versus the previous model
- Leica Summilux-M 35 f/1.4 ASPH. redesign press release:
  [Leica press release PDF](https://leica-camera.com/sites/default/files/2022-09/press_release_summilux-m_35_september_202246.pdf)
  - states 11 aperture blades instead of 9
  - closest focusing distance reduced from 70 cm to 40 cm
  - notes a new double-cam unit and almost doubled focus throw to 176 degrees
- Leica Wiki reference for Noctilux 50 f/1.0:
  [Leica Wiki 50mm f/1 Noctilux-M](https://wiki.l-camera-forum.com/leica-wiki.en/index.php/50mm_f/1_Noctilux-M)
  - distinguishes E58, E60, and built-in hood versions
  - notes multiple variants across the 1976-2008 production era
  - includes historical variant-level street-price notes

### Local listing evidence used

Local listing analysis was based on `data/derived/results_resolved_v2.json` (`7,860` resolved records).

## A. Summilux 50 ASPH new

### 1. Official / literature split

Yes. Leica explicitly presents the 2023 version as a technically and optically refined lens versus the previous Summilux-M 50 ASPH. The official release calls out:

- 11 blades instead of 9
- 70 cm to 45 cm close-focus extension
- new double-cam gear
- revised integrated hood design

That is enough to justify a distinct normalization/search entity.

### 2. Mechanical distinction

Strong.

- 45 cm close-focus extension
- double-cam focusing mechanism
- revised hood construction
- different handling profile from the older ASPH version

### 3. Optical distinction

Moderate-to-strong.

Leica explicitly says the lens was refined "technically and optically" and highlights the 11-blade diaphragm / rounder bokeh. That is enough to treat it as more than a cosmetic refresh.

### 4. Search-intent separability

Good in principle, but inconsistent in live listing language.

In local listings, the new generation does not consistently appear as:

- `45cm`
- `close focus`
- `2023`

Instead, the few visible examples are titled as:

- `ASPH II`
- `ASPH FLE II` (dealer wording contamination)

So search separation is possible, but title conventions are still noisy.

### 5. Market / price-table separability

Weak-to-moderate in the current local corpus.

Local observed buckets:

- older / unspecified 50 ASPH:
  - `125` records
  - `26` priced
  - median about `3.625M KRW`
- new ASPH / ASPH II heuristic:
  - `3` records
  - `3` priced
  - median `5.5M KRW`

That price gap points in the right direction, but the sample is too thin and too dealer-title-dependent to treat as a stable core price group yet.

### 6. Final decision

`hold`

### 7. One-line reason

The product split is real, but current local market coverage is still too sparse and title conventions are too noisy to promote this into a stable core price-table entity today.

## B. Summilux 35 ASPH close-focus generation

### 1. Official / literature split

Yes, strongly.

Leica's 2022 redesign release is explicit:

- 11 blades instead of 9
- close focus reduced from 70 cm to 40 cm
- patent-pending double-cam unit
- focus throw almost doubled to 176 degrees
- revised integrated round hood

This is not a cosmetic micro-revision. It is an official generation break.

### 2. Mechanical distinction

Strong.

- 40 cm close focus
- new double-cam mechanism
- much longer focus throw
- different hood construction

This is easy to defend as a separate generation in normalization.

### 3. Optical distinction

Moderate-to-strong.

Leica itself ties the redesign to improved bokeh and refined handling/close-focus behavior. Even if one treats the optical formula as evolutionary rather than entirely new, the generation split is still meaningful enough for an independent market entity.

### 4. Search-intent separability

Strong.

The local market already uses clear tokens:

- `FLE II`
- `close focus`
- `40 cm`

So buyers and dealers are already searching for it as something distinct from prior FLE.

### 5. Market / price-table separability

Strong enough for core promotion in the current local corpus.

Local observed buckets:

- close-focus generation:
  - `12` records
  - `11` priced
  - median `6.0M KRW`
  - range `5.5M` to `8.2M`
- prior FLE:
  - `36` records
  - `11` priced
  - median `4.0M KRW`
  - range `3.6M` to `4.7M`

This is not a tiny spread. The median gap is roughly `2.0M KRW`, and the titles are already using generation-specific wording. The sample is still dealer-heavy, but it is much healthier than the 50 ASPH new case.

### 6. Final decision

`core` recommended

### 7. One-line reason

The official generation split is clear, the mechanical distinction is strong, the search language is already explicit, and the local price band is materially separated from earlier FLE.

## C. Noctilux 50 f/1.0 internal split (E58 / E60 / V3 built-in hood)

### 1. Official / literature split

There is solid literature support for variant separation.

Leica Wiki documents:

- 1st version: `E58`
- 2 E60 versions without hood
- last E60 version with built-in hood

So normalization/search split is justified.

### 2. Mechanical distinction

Strong enough for normalization:

- filter-size change from `E58` to `E60`
- hood construction change
- final built-in hood version

### 3. Optical distinction

Weak-to-moderate as a promotion driver.

The important distinction here looks more like versioning / handling / production-era structure than a clearly market-priced optical family break in the current local data.

### 4. Search-intent separability

Yes.

Collectors and advanced buyers do search for:

- `E58`
- `E60`
- built-in hood / telescopic hood version

So keeping internal split as normalization entities still makes sense.

### 5. Market / price-table separability

Too weak in the current local corpus.

Local observed buckets:

- `E58`
  - `2` records
  - `0` priced
- `E60`
  - `0` records
  - `0` priced
- `V3 built-in hood`
  - `0` records
  - `0` priced
- generic f/1.0 pool
  - `31` records
  - `3` priced
  - median about `6.0M KRW`

Leica Wiki does include historical street-price notes by variant generation, but in the current local production dataset the price evidence is simply too sparse to support three separate core price groups.

### 6. Final decision

`hold` for all three internal splits

### 7. One-line reason

The internal split is real for normalization and collector search, but the current listing pool does not yet support stable, variant-level core price groups.

## Promotion Decisions

| Candidate | Decision | Why |
| --- | --- | --- |
| Summilux 50 ASPH new | Keep `hold` | real generation split, but current local market sample too thin |
| Summilux 35 ASPH close-focus generation | Promote to `core` | official redesign + explicit search language + meaningful local price separation |
| Noctilux 50 f/1.0 E58 | Keep `hold` | variant is real, but price-table evidence too sparse |
| Noctilux 50 f/1.0 E60 | Keep `hold` | not enough local records/prices |
| Noctilux 50 f/1.0 V3 built-in hood | Keep `hold` | not enough local records/prices |

## Recommended Follow-up

### Promote next

1. Add an explicit seed row for `Summilux-M 35mm f/1.4 ASPH close-focus generation`
2. Mark that row `core`
3. Keep prior `FLE` and `pre-FLE ASPH` as separate price-table neighbors

### Keep on hold for now

1. `Summilux 50 ASPH new`
   - revisit after more local sold/asking coverage accumulates
   - especially once dealer titles consistently use `ASPH II`, `45cm`, or equivalent wording
2. `Noctilux 50 f/1.0` internal split
   - revisit once E60 / built-in hood examples appear in meaningful count
   - or once external sold-history evidence is intentionally incorporated into price-table policy

## Seed Status Change In This Round

None.

Reason:

- this round's primary output is an audit decision report
- the only strong promotion recommendation is `Summilux 35 ASPH close-focus generation`
- that entity does not yet exist as an explicit seed row, so there was no narrow one-line status flip to apply
- `Noctilux 50 f/1.0 E58` remains correctly set to `hold`

## Bottom Line

This was not a "promote hold by default" round.

The current evidence supports:

- `Summilux 35 ASPH close-focus generation` as a true core candidate
- `Summilux 50 ASPH new` as a valid split that still needs more market evidence
- `Noctilux 50 f/1.0` internal variants as valid normalization splits that should remain on hold for price-table purposes for now
