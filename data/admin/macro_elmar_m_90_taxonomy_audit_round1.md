# Macro-Elmar-M 90 Taxonomy Audit - Round 1

Date: 2026-04-29

Scope: read-heavy taxonomy audit for the Leica `Macro-Elmar-M 90` family. This round does not add seed rows, does not change classifier/query/search behavior, and does not change admin lookup ranking or UI. The goal is to determine whether `Macro-Elmar-M 90` is mature enough for explicit canonical seeding and, if so, at what granularity.

## Executive Summary

`Macro-Elmar-M 90` is much cleaner than `Elmar 90`.

The literature and the local listing pool both support one clear base product line:

- `Leica Macro-Elmar-M 90mm f/4`

By contrast, the variations currently visible around that line are not strong round-1 `core` splits:

- `Macro-Adapter-M included`
- `6bit`
- `set`
- `black / silver`
- `2014 "big top" production revision`

Those are better treated as `overlay`, `hold`, or `보류`, depending on how explicit the signal is.

Round-1 conclusion:

- immediate recommended `core` candidate count: `1`
- likely next seed step: a single `Macro-Elmar-M 90mm f/4` `core` row
- bundle/accessory completeness should not be mistaken for a separate lens entity

## Family Overview

Unlike the broader and noisier `Elmar 90` family, `Macro-Elmar-M 90` is already a named modern Leica M product line with explicit and stable title language:

- `Macro-Elmar-M`
- `90mm f/4`
- often `M`
- sometimes `6bit`
- sometimes bundled with `Macro-Adapter-M`

That means the main taxonomic question is not "how many historical optical generations are we hiding?" but rather:

1. is the main lens line distinct enough to be a standalone canonical entity?
2. are adapter/set/finish/revision signals true entity splits, or just overlays around the same lens?

The current evidence supports a simple answer:

- one real lens line
- several secondary bundle/revision overlays

## Literature / Reference Base

### Source A: Leica Wiki - `90mm f/4 Macro-Elmar-M`

Leica Wiki documents `Macro-Elmar-M 90mm f/4` as a dedicated Leica M lens line with:

- Leica M bayonet
- `4 / 4` optical construction
- close focus to `0.77 m`
- macro capability with `Macro-Adapter-M`
- production beginning in `2003/2004`

The same reference also shows internal catalog / production nuances:

- black / silver variants
- black set with `MACRO-ADAPTER-M`
- later `11670` "big top" version introduced in `2014`

This is strong evidence that:

- `Macro-Elmar-M 90` is its own family, not a subtype of classic `Elmar 90`
- `adapter set` and `2014 revision` exist, but sit inside the same named product line

References:

- https://wiki.l-camera-forum.com/leica-wiki.en/index.php?title=90mm_f%2F4_Macro-Elmar-M
- https://wiki.l-camera-forum.com/leica-wiki.en/index.php/90_mm_f/4_Macro-Elmar-M

### Source B: Leica Camera product / technical pages

Current Leica product pages describe `Macro-Elmar-M 90 f/4` as a dedicated M-system lens and separately describe the `Macro-Adapter-M` as an optional accessory that extends close-focus capability.

Important implications:

- the adapter is not a separate optical generation of the lens
- the lens remains the same lens whether sold alone or in a set
- close-focus behavior changes with the adapter, but canonical identity does not

References:

- https://leica-camera.com/en-US/photography/lenses/m/macro-elmar-m-90mm-f4-black
- https://leica-camera.com/en-US/photography/lenses/m/macro-elmar-m-90mm-f4-black/technical-specification
- https://leica-camera.com/en-PT/Company/Press-Centre/Press-Releases/2014/Press-Release-LEICA-MACRO-ELMAR-M-90-mm-f-4

## Local Listing Evidence

Analysis base: `data/derived/results_resolved_v2.json`

After excluding obvious contamination such as `APO-Macro-Elmarit-R 100`, the useful local `Macro-Elmar-M 90` pool is about `14` records.

### Local buckets

| Local bucket | Count | Priced | Median (KRW-only where possible) | Audit note |
| --- | ---: | ---: | ---: | --- |
| plain `Macro-Elmar-M 90` | 9 | 3 | ~2.28M KRW | main lens line, strongest signal |
| `6bit` explicit | 2 | 0 | none | weak subtype label, likely metadata/era overlay |
| `Macro-Adapter-M` bundled | 2 | 1 | not comparable | bundle / kit-complete style signal |
| `6bit set` explicit | 1 | 1 | single GBP sample | likely bundle/completeness, not core split |

Representative local titles:

- `[중고] M 90/4 Macro-Elmar (Black)`
- `LEICA 90mm F4 MACRO-ELMAR-M sn.3975`
- `LEICA 90mm F4 (6bit) MACRO-ELMAR-M sn.3975`
- `LEICA 90mm F4 (6bit) Macro Elmar-M Macro-Adapter-M sn.3976`
- `Leica 90mm F4 Macro Elmar M + Macro Adapter M`
- `Leica 90mm F4 Macro Elmar M 6bit Set`

### Interpretation

The listing pool does **not** suggest multiple well-separated user-facing lens entities.

It suggests:

1. a clearly recognized main lens line (`Macro-Elmar-M 90 f/4`)
2. occasional bundle/completeness wording (`+ Macro Adapter M`, `Set`)
3. occasional metadata/revision wording (`6bit`)

That is exactly the pattern where a single `core` lens entity plus overlays is the safe first move.

## Candidate Entity Expansion

## Candidate 1: `Leica Macro-Elmar-M 90mm f/4`

### Official / literature basis

Strong.

This is an explicit Leica product line with stable naming, dedicated product pages, and a distinct Leica Wiki entry.

### Mechanical distinction

Strong.

- collapsible modern M lens
- Leica M bayonet
- optimized for normal use and close-up use with the dedicated adapter

### Optical distinction

Strong enough for `core`.

The literature treats it as a single modern `4 / 4` lens design, separate from:

- classic `Elmar 90`
- `Elmar-C 90`
- `Elmarit 90`
- `Summicron 90`

### Market split potential

Good.

The local priced examples cluster around one modern tele/macro Leica M lens line rather than multiple sub-lines.

### Search-intent split potential

Strong.

Users and dealers clearly search and title this as:

- `Macro-Elmar-M 90`
- `90/4 Macro-Elmar`
- `Macro Elmar M 90`

### Final decision

`core`

### One-line reason

`Macro-Elmar-M 90mm f/4` is a distinct Leica product line with stable title language and enough local evidence to support a single explicit `core` canonical entity.

## Candidate 2: `Macro-Elmar-M 90mm f/4 + Macro-Adapter-M set`

### Official / literature basis

Moderate.

Leica and Leica Wiki both acknowledge adapter-included sets, but the adapter is presented as an accessory for the lens, not as a different lens identity.

### Mechanical distinction

Weak as a lens-entity split.

The optical lens stays the same. The accessory changes usable close-focus range, but not the base lens identity.

### Optical distinction

None.

### Market split potential

Some listing-level price effect is possible, but that is more naturally a bundle/completeness axis than a new canonical lens entity.

### Search-intent split potential

Moderate.

People may search for:

- `macro elmar 90 adapter set`
- `macro elmar m + macro adapter m`

But that is best interpreted as a bundle intent layered on top of the same lens entity.

### Final decision

`overlay`

### One-line reason

`Macro-Adapter-M included` changes the bundle, not the lens itself, so it should remain an overlay rather than a separate canonical entity.

## Candidate 3: `Macro-Elmar-M 90mm f/4 6bit`

### Official / literature basis

Weak-to-moderate as a standalone entity.

`6bit` is real metadata and may correlate with production era, but it is not a separate named Leica product line.

### Mechanical distinction

Weak.

No strong evidence in current materials that `6bit` alone creates a user-facing mechanical identity comparable to a separate lens line.

### Optical distinction

Weak.

The literature still treats this as the same `Macro-Elmar-M 90` lens.

### Market split potential

Possible but currently unproven.

The local sample is too thin to justify a separate seed row, even as `hold`, in round 1.

### Search-intent split potential

Moderate.

Some dealers do mention `6bit`, but more as a listing descriptor than as the primary model name.

### Final decision

`hold`

### One-line reason

`6bit` is real metadata and maybe worth preserving later, but it is not strong enough yet to split the main `Macro-Elmar-M 90` line.

## Candidate 4: `Macro-Elmar-M 90mm f/4 2014 "big top" revision`

### Official / literature basis

Real, but niche.

Leica Wiki records a `2014` "big top" version and the current Leica page centers order number `11670`.

### Mechanical distinction

Moderate.

The revision appears to involve physical / technical detail changes, but the public-facing product name remains the same.

### Optical distinction

Unclear as a practical canonical split.

### Market split potential

Collector-level or advanced-buyer-level only, based on current evidence.

### Search-intent split potential

Weak.

Typical dealer titles in the local dataset do not expose `big top` wording.

### Final decision

`보류`

### One-line reason

The `2014` revision is real, but not exposed strongly enough in current title language to justify a round-1 explicit row.

## Candidate 5: black / silver finish

### Official / literature basis

Real.

Leica Wiki records black and silver/chrome variants.

### Mechanical distinction

Weak.

Finish alone is not enough here.

### Optical distinction

None.

### Market split potential

Possibly meaningful in collector pricing, but not enough for round-1 canonical splitting.

### Search-intent split potential

Weak-to-moderate.

### Final decision

`overlay`

### One-line reason

Finish is a secondary attribute, not a first-pass canonical split.

## Candidate 6: boxed / complete / hood-included / pre-production

### Official / literature basis

Weak as canonical entity axes.

### Mechanical distinction

None or near-none.

### Market split potential

Collector-sensitive, but listing-structure dependent.

### Search-intent split potential

Weak.

### Final decision

`보류`

### One-line reason

These are collector/completeness nuances, not stable first-pass entity splits.

## Recommended Round-1 Taxonomy

### Recommended immediate `core`

1. `Leica Macro-Elmar-M 90mm f/4`

### Recommended `overlay`

- `Macro-Adapter-M included`
- `set / kit-complete`
- `finish`
- `boxed`
- `hood included`
- `condition`

### Recommended `hold`

- `6bit`

### Recommended `보류`

- `2014 "big top" revision`
- pre-production / rare revision nuances
- collector-only completeness or packaging variations

## Why This Family Is More Seed-Ready Than `Elmar 90`

`Macro-Elmar-M 90` is better behaved because:

1. the family name itself is explicit and modern
2. local listings usually say `Macro-Elmar` directly
3. contamination can be filtered out more easily than in generic `Elmar 90`
4. the adapter relationship is conceptually clear: accessory/bundle, not a separate optical family

That makes it suitable for a narrow first seed round.

## Recommended Next Step

Yes, the next round can reasonably move to seed addition.

But it should stay narrow:

- add exactly one explicit `core` row:
  - `Leica Macro-Elmar-M 90mm f/4`
- do **not** add separate rows yet for:
  - `Macro-Adapter-M set`
  - `6bit`
  - `big top`
  - finish variants

## Seed-Readiness Verdict

### Can this family move to explicit seed next round?

`Yes`

### Recommended first seed shape

- one `core` row only
- bundle/accessory/finish/revision remain overlay or hold

### Why this is safe

Because the strongest distinction here is not internal subtype splitting.  
It is simply recognizing `Macro-Elmar-M 90mm f/4` as a distinct modern Leica M lens family and refusing to overreact to listing-level bundle detail.
