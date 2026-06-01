# Elmar 90 Taxonomy Audit - Round 1

Date: 2026-05-08

Scope: read-heavy taxonomy audit for the Leica `Elmar 90` family. This round does not add seed rows, does not change classifier/query/search behavior, and does not change admin lookup ranking or UI. The goal is to determine whether `Elmar 90` is mature enough for explicit canonical seeding and, if so, at what granularity.

## Executive Summary

`Elmar 90` is a real Leica family, but it is still too noisy to seed broadly in round 1.

The literature shows several meaningful lines:

1. classic `90mm f/4 Elmar`
2. late `Elmar (III) 1:4 / 90mm`
3. `90mm f/4 Elmar-C`

But local listing language does **not** support a broad `Elmar 90` core row safely. The family is mixed across:

- generic `Elmar 90` titles
- original `L` / screw-thread references
- occasional `M 90/4 Elmar`
- `Elmar-C`
- `Elmar (III)` / `3-element`
- contamination from `Macro-Elmar-M`, `Elmarit 90`, `Tele-Elmarit 90`, and R / SL lines

Round-1 conclusion:

- immediate recommended `core` candidate count: `0`
- recommended round-1 disposition: `seed 보류`
- strongest future `hold` candidate:
  - `Leica Elmar-C 90mm f/4`
- secondary possible hold candidate:
  - `Elmar (III) 1:4 / 90mm`
- `Leica Elmar-M 90mm f/4` is **not** supported as a standalone Leica line in the literature and should not be treated as a separate family anchor
- `Macro-Elmar-M 90mm f/4` is a different family and must remain boundary-separated

## Family Overview

The Leica `90mm` field is already crowded by many adjacent families:

- `Elmar 90`
- `Elmar-C 90`
- `Macro-Elmar-M 90`
- `Elmarit 90`
- `Tele-Elmarit 90`
- `Summicron 90`
- `APO-Summicron-M 90`
- `R 90` families

That means broad `Elmar 90` is more fragile than families like `Summilux 28` or `Summicron 28`.

The round-1 question is whether there is any broad `Elmar 90` row that is:

1. literature-real
2. locally well labeled
3. price-stable enough
4. safe for generic queries

Round-1 answer: no.

## Literature / Reference Base

### Source A: Leica Wiki - `90mm f/4 Elmar`

Leica Wiki documents the classic `90mm f/4 Elmar` line as:

- production era `1954-1968`
- Leica screw-thread and M-bayonet
- `4 / 3` optical construction
- collapsible and rigid versions
- optional `eyes` variants

Reference:

- [Leica Wiki - 90mm f/4 Elmar](https://wiki.l-camera-forum.com/leica-wiki.en/index.php/90mm_f/4_Elmar)

### Source B: Leica Wiki - `Elmar (III) 1:4 / 90mm`

Leica Wiki documents a later line as:

- `Elmar (III) 1:4 / 90mm`
- production era `1964-1965`
- Leica screw-thread and M-bayonet
- `3 / 3` optical construction

Reference:

- [Leica Wiki - Elmar (III) 1:4 / 90mm](https://wiki.l-camera-forum.com/leica-wiki.en/index.php/Elmar_%28III%29_1%3A4_/_90mm)

### Source C: Leica Wiki - `90mm f/4 Elmar-C`

Leica Wiki documents `90mm f/4 Elmar-C` as:

- production era `1973-1977`
- Leica M-bayonet
- `4 / 4` optical construction
- distinct CL-era line

Reference:

- [Leica Wiki - 90mm f/4 Elmar-C](https://wiki.l-camera-forum.com/leica-wiki.en/index.php/90mm_f/4_Elmar-C)

### Source D: Macro-Elmar-M exclusion

Leica Wiki documents `90mm f/4 Macro-Elmar-M` as a modern M-family product line, not as a subtype of classic `Elmar 90`.

Reference:

- [Leica Wiki - 90mm f/4 Macro-Elmar-M](https://wiki.l-camera-forum.com/leica-wiki.en/index.php/90_mm_f/4_Macro-Elmar-M)

### Interpretation

The literature supports several real splits inside the broader historical `Elmar 90` area.

But it does **not** support a standalone line called:

- `Leica Elmar-M 90mm f/4`

as a clean modern product family in the way that `Macro-Elmar-M 90` or `Elmar-M 24` are cleanly documented.

That matters because local titles containing `Elmar-M 90` are likely to be:

- contamination from `Macro-Elmar-M`
- seller shorthand
- or a mistaken collapsing of distinct Leica lines

## Local Listing Evidence

Analysis base: `data/normalized/normalized_latest.json`

After excluding obvious contamination from:

- `Macro-Elmar-M`
- `Elmarit 90`
- `Tele-Elmarit 90`
- `Summicron 90`
- `APO-Summicron 90`
- `Thambar 90`
- `Elmarit-R`
- `Summicron-R`
- `Vario-Elmarit`
- third-party 90mm lenses
- accessory-only titles

the useful local `Elmar 90` pool becomes:

- clean local pool: `23`

### Broad price clustering

KRW-parsed local medians:

| Bucket | Count | KRW-priced | Median KRW | Audit note |
| --- | ---: | ---: | ---: | --- |
| broad `Elmar 90` pool | 23 | 7 | ~1.76M KRW | mixed family, not safe as broad seed anchor |
| `M 90/4 Elmar`-like wording | 6 | 4 | ~2.18M KRW | still mixed with Macro-Elmar contamination signals |
| `Elmar-C` explicit | 2 | 0 | none | very sparse but subtype-explicit |
| `Elmar III / 3-element` explicit | 1 | 0 | none | literature-real, but title support is tiny |
| `LTM / L / Elmar-L` explicit | 1 | 0 | none | too sparse for immediate row decisions |

Observed broad range:

- min priced example: ~`350,000 KRW`
- median: ~`1.76M KRW`
- max priced example: ~`2.98M KRW`

### Local title patterns

Broad recurring titles:

- `LEICA 90mm F4 Elmar sn.6465`
- `LEICA 90mm F4 ELMAR sn.1913`
- `LEICA 90mm F4 Elmar sn.6733`
- `LEICA 90mm F4 Elmar sn.1310`
- `Leica 90mm F4 Elmar`

Subtype-explicit titles:

- `LEICA 90mm F4 ELMAR-C sn.2573`
- `Leica 90mm F4 C Elmar`
- `LEICA 90mm F4 Elmar 3-element sn.2089`
- `LEICA 90mm F4 Elmar-L sn.1212`

Contaminating or ambiguous titles:

- `[중고] M 90/4 Macro-Elmar (Black)`
- `Leica 90mm F4 Macro Elmar M + Macro Adapter M`
- `Leica 90mm F4 Macro Elmar M 6bit Set`

### Local marker frequency

Observed local markers:

- `elmar-c`: `1`
- `elmar-m`: `2`
- `m 90/4`: `4`
- `adapter`: `2`
- `cl`: `1`
- `black`: `3`
- `silver`: `2`

Important absences:

- `collapsible`
- `침동`
- `rigid`
- strong repeated `LTM`

### Interpretation

This is the key operational result:

1. broad `Elmar 90` language is not stable enough for a seed anchor
2. `Elmar-C` is the clearest subtype by name
3. `Elmar (III)` is real, but barely visible locally
4. `Elmar-M 90` is not a clean local family signal and overlaps with `Macro-Elmar-M`
5. `collapsible / rigid` is literature-real but locally almost invisible

## Candidate Entity Expansion

## Candidate 1: broad `Leica Elmar 90mm f/4`

### Official / literature basis

Real as a historical umbrella, but too broad.

### Mechanical distinction

Too mixed.

This umbrella contains:

- screw-thread vs M-bayonet
- collapsible vs rigid
- early `4 / 3` vs late `3 / 3`

### Optical distinction

Too mixed.

### Market split potential

Weak as a broad anchor.

The broad pool price is blurred by subtype mixing.

### Search-intent split potential

Weak.

Generic:

- `elmar 90`
- `90 elmar`
- `90mm f4 elmar`

can refer to multiple materially different lines.

### Verdict

`보류`

## Candidate 2: `Leica Elmar-C 90mm f/4`

### Official / literature basis

Strong.

This is a distinct documented CL-era line.

### Mechanical distinction

Strong.

It is not merely a finish or bundle variant of the classic `Elmar 90`.

### Optical distinction

Strong enough for a hold-level subtype.

The `4 / 4` CL-era structure is distinct from the older historical `Elmar` lines.

### Market split potential

Moderate, but local sample is thin.

### Search-intent split potential

Good.

Queries like:

- `elmar-c 90`
- `90mm f4 elmar-c`

are already subtype-explicit.

### Verdict

`hold`

## Candidate 3: `Elmar (III) 1:4 / 90mm`

### Official / literature basis

Strong.

This is a real late `3 / 3` line in the literature.

### Mechanical distinction

Moderate to strong.

### Optical distinction

Strong.

This is one of the clearest optical redesigns inside the historical `Elmar 90` family.

### Market split potential

Possible, but current local evidence is very thin.

### Search-intent split potential

Weak to moderate.

It becomes meaningful only when explicit wording such as:

- `3-element`
- `Elmar III`

appears.

### Verdict

`보류` leaning `future hold`

## Candidate 4: `Leica Elmar-M 90mm f/4`

### Official / literature basis

Weak / unsupported.

The literature reviewed does not show a clean Leica product line with this exact role comparable to `Elmar-M 24mm f/3.8 ASPH`.

### Mechanical distinction

Unclear.

### Optical distinction

Unclear.

### Market split potential

Weak.

The local `elmar-m` wording at `90mm` overlaps with `Macro-Elmar-M` contamination.

### Search-intent split potential

Weak.

### Verdict

`out-of-family / misframed candidate`

## Candidate 5: collapsible / rigid `90mm f/4 Elmar`

### Official / literature basis

Strong.

The split is real in the literature.

### Mechanical distinction

Strong.

### Optical distinction

Weak to moderate.

### Market split potential

Possibly meaningful for collectors.

### Search-intent split potential

Too weak locally in round-1.

The important problem is that local title support for:

- `collapsible elmar 90`
- `침동 elmar 90`
- `rigid elmar 90`

is effectively absent.

### Verdict

`보류`

## Overlay Review

Keep these as `overlay`, not separate rows:

- `black / chrome / silver`
- `country marking`
- `hood included`
- `cap included`
- `filter included`
- `boxed`
- `condition`
- `original cap`
- `original hood`
- `original box`
- `packaging`
- `goggles / adapter / pouch` inclusion

Special note:

- `collapsible` should remain below row level in round-1 unless a later audit finds much stronger local title support

## Contamination / Boundary Review

The following must remain out-of-family boundaries:

- `Elmarit 90`
- `Tele-Elmarit 90`
- `Macro-Elmar-M 90`
- `Summicron 90`
- `APO-Summicron-M 90`
- `Thambar 90`
- `R 90` families
- `CL/C system` lines when they are not explicitly `Elmar-C`
- accessory-only results such as hoods, caps, filters, adapters
- third-party 90mm lenses

Boundary examples to keep separate:

- `elmarit 90`
- `tele-elmarit 90`
- `macro-elmar-m 90`
- `summicron 90`
- `apo summicron 90`
- `thambar 90`
- `elmarit-r 90`
- `summicron-r 90`
- `voigtlander 90`
- `zeiss 90`
- `hood 90 elmar`
- `filter 90 elmar`
- `adapter elmar 90`

## Round-1 Recommendation Table

| Candidate | Verdict | Why |
| --- | --- | --- |
| broad `Leica Elmar 90mm f/4` | `보류` | historically real, but too mixed for a safe broad seed anchor |
| `Leica Elmar-C 90mm f/4` | `hold` | subtype-explicit and literature-real, but still sparse locally |
| `Elmar (III) 1:4 / 90mm` | `보류` | strong literature, weak local title support |
| `Leica Elmar-M 90mm f/4` | `out-of-family / misframed` | not supported as a clean independent Leica line |
| collapsible / rigid `90mm f/4 Elmar` | `보류` | literature-real, but locally almost invisible |

## Immediate Core Candidate Count

Recommended immediate `core` candidate count: `0`

Round-1 recommendation:

- `seed 보류`

## Hold Candidates

Recommended explicit `hold` candidate for future rounds:

1. `Leica Elmar-C 90mm f/4`

Secondary candidate to revisit later:

1. `Elmar (III) 1:4 / 90mm`

## Seed Readiness

Not for immediate broad seeding.

The safest next step would be:

1. do **not** add a broad generic `Elmar 90` row
2. if needed, revisit `Elmar-C 90mm f/4` first as a narrow `hold` candidate
3. keep `Macro-Elmar-M 90` and `Elmarit` / `Tele-Elmarit` families strictly separated

In short: `Elmar 90` has real structure, but round-1 broad seeding would still be too blunt.
