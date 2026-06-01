# Elmar 50 Taxonomy Audit - Round 1

Date: 2026-04-28

Scope: read-heavy taxonomy audit for the Leica `Elmar 50` family. This round does not add seed rows, does not change search/classifier/query/search-service behavior, and does not change admin lookup ranking. The purpose is narrower: decide which `Elmar 50` splits are strong enough to become explicit canonical seed candidates and which should remain overlay / hold / deferred.

## Executive Summary

`Elmar 50` should not remain a single broad canonical family. The literature and local market both show at least three, and probably four, meaningful entity layers:

1. early `Elmar 50mm f/3.5` 5-element collapsible line
2. later `Elmar 50mm f/3.5` 4-element collapsible line (`Red Scale` era and adjacent late 3.5 generation)
3. vintage `Elmar 50mm f/2.8` collapsible line
4. modern `Elmar-M 50mm f/2.8`

The strongest round-1 audit conclusion is that the main split axis is not `LTM vs M`. It is:

- optical / generation break inside `f/3.5`
- vintage `f/2.8` versus modern `Elmar-M 50 f/2.8`

Collector micro-variants such as feet/metric, military engravings, A36 vs E39, and black/silver finish should not be promoted to round-1 core entities.

## Working Recommendation

### Recommended immediate core candidates

1. `Leica Elmar 50mm f/3.5 early 5-element collapsible`
2. `Leica Elmar 50mm f/3.5 late 4-element collapsible`
3. `Leica Elmar 50mm f/2.8 collapsible`
4. `Leica Elmar-M 50mm f/2.8`

### Overlay candidates

- `mount = LTM / M`
- `finish = nickel / chrome / black / silver`
- `scale = feet / metric / red scale`
- `engraving / military marking`
- `boxed / hood included / condition`

### Hold / deferred candidates

- `Red Elmar` as its own canonical name rather than an alias to late `f/3.5`
- `Nickel Elmar` as its own canonical name rather than an alias to early `f/3.5`
- `11 o'clock bell push`, `7 o'clock`, flat-top, heavy-cam micro-subtypes
- `6bit` and finish-only sub-splits inside `Elmar-M 50mm f/2.8`

## Family Overview

The Leica `Elmar 50` family is historically broad. Unlike `Summaron 35`, which is already obviously split by maximum aperture, `Elmar 50` spans:

- a long early screw-mount `f/3.5` history
- a documented optical redesign within the `f/3.5` line
- a later vintage `f/2.8` collapsible line
- a much later modern `Elmar-M 50mm f/2.8`

This means a single broad `Elmar 50` seed would be too coarse for price-table and admin normalization use.

The crucial question is where to stop splitting. The round-1 answer is:

- split on major optical / generation families
- do not split on every collector-visible cosmetic subtype

## Literature / Reference Base

### Source A: Leica Wiki - `Elmar (I) f= 5 cm 1:3.5`

Key points:

- production era `1930-1950`
- screw-thread mount
- `5 / 3` optical construction
- variants include nickel, chrome, metric/feet, heavy-cam, 7 o'clock and 11 o'clock bell-push versions

Reference:

- https://wiki.l-camera-forum.com/leica-wiki.en/index.php/Elmar_%28I%29_f%3D_5_cm_1%3A3.5

### Source B: Leica Wiki - `Elmar (II) f= 5 cm 1:3.5`

Key points:

- production era `1952-1953`
- screw-thread mount
- `4 / 3` optical construction
- black scale / red scale variants

Reference:

- https://wiki.l-camera-forum.com/leica-wiki.en/index.php?title=Elmar_%28II%29_f%3D_5_cm_1%3A3.5

### Source C: Leica Wiki - `Elmar (III) f= 5 cm 1:3.5`

Key points:

- production era `1954-1961`
- screw-thread and M-bayonet
- still `4 / 3`
- A36 and E39 variants

Reference:

- https://wiki.l-camera-forum.com/leica-wiki.en/index.php/Elmar_%28III%29_f%3D_5_cm_1%3A3.5

### Source D: Leica Wiki - `Elmar f= 5 cm 1:2.8`

Key points:

- production era `1957-1962` screw, `1958-1966` bayonet, with later serial continuation listed through `1971`
- screw-thread and M-bayonet
- `4 / 3`
- lanthanum glass in first and last element
- 15-blade diaphragm

Reference:

- https://wiki.l-camera-forum.com/leica-wiki.en/index.php?title=Elmar_f%3D_5_cm_1%3A2.8

### Source E: Leica Wiki - `50mm f/2.8 Elmar-M`

Key points:

- production era `1994-2007`
- M mount only
- modern `Elmar-M` product line
- collapsible body, but clearly a later and separately branded lens family

Reference:

- https://wiki.l-camera-forum.com/leica-wiki.en/index.php/50mm_f/2.8_Elmar-M

## Local Listing Evidence

Analysis base: `data/derived/results_resolved_v2.json`

Observed `Elmar 50` lens records after excluding obvious hood / Tri-Elmar contamination:

- total observed lens records: `98`

### Local signals worth trusting

#### `f/3.5` sub-signals

| Bucket | Count | Priced | Median KRW | Notes |
| --- | ---: | ---: | ---: | --- |
| `Red Elmar` | 20 | 7 | 700,000 | late `f/3.5` language is active in local market |
| `Nickel Elmar` | 12 | 8 | 940,000 | early/vintage presentation clearly trades differently |
| generic / plain `f/3.5` | 17 | 2 | 650,000 | many unpriced serial-only listings |

#### `f/2.8` sub-signals

| Bucket | Count | Priced | Median KRW | Notes |
| --- | ---: | ---: | ---: | --- |
| modern-ish `M / 6bit / black / silver` | 20 | 20 | 1,165,000 | looks like `Elmar-M 50mm f/2.8` pool |
| vintage-ish serial-only `f/2.8` | 18 | 2 | 900,000 | sparse pricing, but clearly older line |

### What the local data says

1. `f/3.5` and `f/2.8` are not one market object.
2. Inside `f/3.5`, the late `Red Elmar` style pool and early `Nickel / older collapsible` pool are different enough to justify at least a serious split review.
3. Inside `f/2.8`, modern `Elmar-M` behavior is visible and should not be permanently merged with vintage `5 cm f/2.8` collapsible stock.

## Candidate Entity Expansion

## Candidate 1: `Leica Elmar 50mm f/3.5 early 5-element collapsible`

### Official / literature basis

Strong.

`Elmar (I) f= 5 cm 1:3.5` is explicitly documented as the early `1930-1950` screw-mount line with `5 / 3` optical construction.

### Mechanical distinction

Strong.

- screw-thread only
- early collapsible barrel
- early bell-push / heavy-cam / nickel-era variants

### Optical distinction

Strong.

This is not merely a mount overlay of later `f/3.5`; Leica Wiki treats it as the earlier `5 / 3` design before the later `4 / 3` redesign.

### Market split potential

Strong enough.

Local `Nickel Elmar` pricing sits materially above the `Red Elmar` pool, and the collector market already treats the earliest collapsible Elmars as a distinct object.

### Search-intent split potential

Strong.

Queries like `Nickel Elmar`, `11 o'clock Elmar`, and early collapsible `5cm Elmar` language are common enough to justify a distinct seed target.

### Final decision

`core`

### One-line reason

The early `5 / 3` collapsible Elmar is a true optical-generation split, not just a finish overlay.

## Candidate 2: `Leica Elmar 50mm f/3.5 late 4-element collapsible`

### Official / literature basis

Strong.

`Elmar (II)` and `Elmar (III)` document a later `4 / 3` `f/3.5` line spanning screw and M-bayonet forms, including the classic `Red Scale` era.

### Mechanical distinction

Strong enough.

- later collapsible barrel family
- screw plus later M-bayonet forms
- A36 / E39 and scale variants

### Optical distinction

Strong.

The official `4 / 3` redesign is enough to justify separation from the earlier `5 / 3` line.

### Market split potential

Strong enough.

`Red Elmar` appears frequently in the local pool and trades below the earlier `Nickel Elmar` bucket in a way that looks like a stable market distinction rather than random noise.

### Search-intent split potential

Strong.

`Red Elmar` is already a recognizable dealer and buyer phrase.

### Final decision

`core`

### One-line reason

The later `4 / 3` collapsible Elmar family is both officially distinct and actively named in the market.

## Candidate 3: `LTM` vs `M` for `f/3.5`

### Official / literature basis

Real, but not sufficient by itself for a round-1 core split.

`Elmar (III)` explicitly spans screw-thread and M-bayonet.

### Mechanical distinction

Yes.

Mount and camera compatibility differ.

### Optical distinction

Usually no.

The mount split does not, by itself, define a new optical family.

### Market split potential

Moderate at best.

Search cares about `LTM` vs `M`, but the taxonomy does not need separate core price groups on mount alone if optical-generation lines are already separated.

### Search-intent split potential

Yes.

Useful as normalization metadata and aliasing, not necessarily as core entity.

### Final decision

`overlay`

### One-line reason

Mount is important for search and compatibility, but it is not the main round-1 price-table split.

## Candidate 4: `Red Elmar` as its own canonical entity

### Official / literature basis

Real as a market phrase, but weaker as a pure family name.

Leica Wiki uses `Red scale` as a variant signal within the later `f/3.5` line rather than as a separately named factory family.

### Mechanical distinction

Partial.

It tracks the later `4 / 3` generation, but is still partly a scale/era naming pattern rather than a fully independent product line.

### Optical distinction

Indirect.

The optical distinction is really `early 5 / 3` versus `late 4 / 3`, not `red letters` by themselves.

### Market split potential

Strong enough to matter, but better modeled as the most visible alias for the late `f/3.5` core entity.

### Search-intent split potential

Very strong.

### Final decision

`overlay` alias on the late `f/3.5` core, not its own round-1 core row

### One-line reason

`Red Elmar` is a powerful lookup alias, but the deeper canonical split is the late `4 / 3` generation rather than the red-scale cosmetic label alone.

## Candidate 5: `Nickel Elmar` as its own canonical entity

### Official / literature basis

Real as a finish/era descriptor, but again weaker than the underlying early `5 / 3` optical family.

### Mechanical distinction

Mostly finish/era, not a wholly separate design line by itself.

### Optical distinction

Indirect.

The meaningful split is early `5 / 3` versus late `4 / 3`, and `Nickel` is just a visible market proxy for the earlier side.

### Market split potential

Real.

The local `Nickel Elmar` pool is clearly valued differently from `Red Elmar`.

### Search-intent split potential

Strong.

### Final decision

`overlay` alias on the early `f/3.5` core, not a separate round-1 core row

### One-line reason

`Nickel Elmar` matters in lookup and market language, but it should hang off the early `5 / 3` core rather than become its own first-round seed family row.

## Candidate 6: `Leica Elmar 50mm f/2.8 collapsible` (vintage)

### Official / literature basis

Strong.

Leica Wiki documents `Elmar f= 5 cm 1:2.8` as a distinct vintage lens line, produced in screw and M forms starting in the late 1950s.

### Mechanical distinction

Strong.

- collapsible
- screw and M production
- E39 / A42 accessory environment
- 15-blade diaphragm

### Optical distinction

Strong enough.

This is not just a later badge on the `f/3.5`; it is a separate faster Elmar line with its own glass/material description and official lifecycle.

### Market split potential

Moderate-to-strong.

Even with sparse priced local vintage-only examples, this is clearly not the same object as either `f/3.5` or the 1990s `Elmar-M 50 f/2.8`.

### Search-intent split potential

Strong.

Buyers and dealers do search `Elmar 50 2.8` separately from `Elmar 50 3.5`.

### Final decision

`core`

### One-line reason

The vintage `5 cm f/2.8` collapsible Elmar is a distinct historical and market line.

## Candidate 7: `Leica Elmar-M 50mm f/2.8`

### Official / literature basis

Strong.

Leica Wiki treats `50mm f/2.8 Elmar-M` as a separate modern product line with its own production era (`1994-2007`) and separate M-only identity.

### Mechanical distinction

Strong.

- M mount only
- modern production
- separate finish set
- 0.7 m focus
- explicit `Elmar-M` naming

### Optical distinction

Moderate.

The page frames it as the direct descendant of the vintage `f/2.8` line, so the split is more product-line and era-based than radically optical. But for canonical price tables that is still enough.

### Market split potential

Moderate, but sufficient.

Local modern-ish listings cluster around roughly `1.16M KRW` median, above the sparse vintage `f/2.8` samples. More importantly, the modern line is named and sold as its own object.

### Search-intent split potential

Strong.

`Elmar-M 50 2.8`, black/silver M listings, and `6bit` language are clearly modern-product cues.

### Final decision

`core`

### One-line reason

Even if optically descended from the vintage `f/2.8`, the modern `Elmar-M 50mm f/2.8` behaves as a separate canonical market entity.

## Candidate 8: `LTM` vs `M` for vintage `f/2.8`

### Official / literature basis

Real but secondary.

Vintage `f/2.8` exists in screw and M forms.

### Mechanical distinction

Yes.

### Optical distinction

Usually no.

### Market split potential

Not strong enough in the current local data to justify separate round-1 core entities.

### Search-intent split potential

Useful, but better as overlay.

### Final decision

`overlay`

### One-line reason

Mount is useful metadata, but the bigger split is vintage `f/2.8` versus modern `Elmar-M 2.8`.

## Candidate 9: collector micro-variants

Examples:

- `11 o'clock` / `7 o'clock`
- heavy-cam
- Swedish army 3-crown
- feet vs metric
- military engravings
- A36 vs E39
- flat-top / fine mechanical subforms

### Final decision

`보류`

### One-line reason

These are real collector distinctions, but too fine-grained for round-1 core taxonomy.

## Round-1 Recommendation

### Recommended immediate core entity count

`4`

Recommended round-1 core candidates:

1. `Leica Elmar 50mm f/3.5 early 5-element collapsible`
2. `Leica Elmar 50mm f/3.5 late 4-element collapsible`
3. `Leica Elmar 50mm f/2.8 collapsible`
4. `Leica Elmar-M 50mm f/2.8`

### Recommended overlays

- `mount`
- `finish`
- `scale`
- `engraving`
- `boxed / hood included / condition`

### Recommended holds / deferreds

- `Red Elmar` as a standalone canonical name instead of an alias
- `Nickel Elmar` as a standalone canonical name instead of an alias
- micro-collector subtypes

## What Should Still Wait

Do not immediately seed as independent round-1 core rows:

- `Red Elmar` as separate from the broader late `f/3.5` line
- `Nickel Elmar` as separate from the broader early `f/3.5` line
- `LTM` vs `M` for any vintage line
- military / bell-push / scale micro-variants
- finish-only splits inside `Elmar-M 50mm f/2.8`

## Is This Ready For Seed Addition?

Yes, but only with disciplined scope.

The family is ready for explicit seeding next round if we keep it to the four broad lines above and model `mount`, `finish`, `Red Scale`, `Nickel`, and similar collector signals as aliases or overlays rather than immediate new core rows.

## Final Recommendation

`Elmar 50` is ready to move into the explicit-seed pipeline, but not as a single family row and not as a collector-fragmented mess.

The right round-1 canonical stance is:

- split by major optical / generation families
- keep mount as overlay
- keep `Red Elmar` / `Nickel Elmar` as very important aliases
- defer micro-collector subtypes

That preserves enough structure for exact search and future price-table work without overfitting the first pass.
