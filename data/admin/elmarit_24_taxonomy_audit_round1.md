# Elmarit 24 Taxonomy Audit - Round 1

Date: 2026-05-06

Scope: read-heavy taxonomy audit for the Leica `Elmarit 24` family. This round does not add seed rows, does not change classifier/query/search behavior, and does not change admin lookup ranking or UI. The goal is to determine whether `Elmarit 24` is mature enough for explicit canonical seeding and, if so, at what granularity.

## Executive Summary

`Elmarit 24` is seedable, but more narrowly than `Elmarit 21`.

The strongest round-1 conclusion is:

1. `Leica Elmarit-M 24mm f/2.8 ASPH`

should be treated as the only immediate first-pass `core` entity.

Round-1 conclusion:

- immediate recommended `core` candidate count: `1`
- recommended first-pass core:
  - `Leica Elmarit-M 24mm f/2.8 ASPH`
- broad non-`ASPH` `Elmarit 24` should **not** be opened as a separate round-1 `core` row
- early unlabeled `24mm f/2.8 Elmarit-M` wording should stay inside the main ASPH line as metadata / title variation
- `finder bundle`, `black / silver`, `country marking`, `coding`, and `packaging` stay `overlay` or `보류`
- `Summilux 24`, `Summicron 24`, `Super-Elmar 24`, `Tri-Elmar`, `Elmarit-R 24`, and `SL` zoom contamination remain out-of-family boundary cases

Why this is narrower than a hypothetical `non-ASPH / ASPH` split:

- literature strongly documents the `24mm f/2.8 ASPH Elmarit-M` line
- local title language is dominated by explicit `ASPH` wording
- the small local unlabeled bucket looks more like early inscription / dealer shorthand variation than a stable second M-side product line

## Family Overview

The `24mm` Leica field is easy to distort unless adjacent families are excluded early:

- `Summilux-M 24mm`
- `Summicron-M 24mm`
- `Super-Elmar-M 24mm`
- `Tri-Elmar`
- `Elmarit-R 24mm`
- `Vario-Elmarit-SL` zoom contamination

Once those are excluded, the local M-side `Elmarit 24` pool becomes small but interpretable.

The first taxonomic question is whether Leica M-side `Elmarit 24` is:

1. a true `non-ASPH / ASPH` two-line family, or
2. a single ASPH family with early unlabeled / dealer-shorthand variation.

Round-1 answer: `2`.

## Literature / Reference Base

### Source A: Leica Wiki - `24mm f/2.8 ASPH Elmarit-M`

Leica Wiki documents the `24mm f/2.8 ASPH Elmarit-M` as a distinct Leica M line with:

- production era `1998-2010`
- `7 / 5` optical design
- `E55` filter arrangement
- Leica M bayonet
- explicit `ELMARIT-M ASPH. 1:2.8/24` inscription in the mature line

Reference:

- [Leica Wiki - 24mm f/2.8 ASPH Elmarit-M](https://wiki.l-camera-forum.com/leica-wiki.en/index.php/24mm_f/2.8_ASPH_Elmarit-M)

### Source B: Leica Wiki serial-note evidence

The same Leica Wiki page includes an important note in the serial table:

- `ASPH lenses not labeled ASPH in Puts list`

and shows early `24mm f/2.8 Elmarit-M` serial blocks before later explicit `ASPH` wording appears.

This matters because it weakens the case for a separate Leica M-side `non-ASPH` canonical line. The literature evidence points more strongly toward:

- one ASPH optical family
- with early unlabeled / differently-inscribed production inside it

Reference:

- [Leica Wiki serial table on the ASPH page](https://wiki.l-camera-forum.com/leica-wiki.en/index.php/24mm_f/2.8_ASPH_Elmarit-M)

### Source C: supporting market references

Secondary market references consistently describe the M-side line as `Elmarit-M 24mm f/2.8 ASPH`, including used-market descriptions that call out the optical design and later `6-bit` coding as metadata rather than separate line identity.

References:

- [DPReview - Leica Elmarit-M 24mm f/2.8 ASPH specs](https://www.dpreview.com/products/leica/lenses/leica_m_24_2p8/specifications)
- [B&H used listing overview](https://www.bhphotovideo.com/c/product/802897413-USE/leica_11878_24mm_f_2_8_elmarit_m.html)

## Local Listing Evidence

Analysis base: `data/derived/results_resolved_v2.json`

After excluding obvious contamination from:

- `Vario-Elmarit-SL 14-24`
- `Vario-Elmarit-SL 24-70`
- `Vario-Elmarit-SL 24-90`
- `Elmarit-R 24`
- `Summilux` / `Summicron` / `Noctilux` 24mm families
- `Super-Elmar`, `Super-Angulon`, `Tri-Elmar`

the useful local M-side `Elmarit 24` pool becomes:

- clean local pool: `12`

### Local bucket shape

Within that pool:

| Bucket | Count | KRW-priced | Median KRW | Audit note |
| --- | ---: | ---: | ---: | --- |
| explicit `ASPH` titles | 8 | 5 | ~2.10M KRW | dominant operational line |
| unlabeled `M 24/2.8 Elmarit` titles | 2 | 2 | ~1.58M KRW | sparse, likely early inscription / shorthand |
| `24mm Finder` bundle titles | 2 | 0 | n/a | accessory bundle, not separate lens line |

Observed title examples:

Explicit ASPH:

- `[위탁] M 24/2.8 Elmarit.ASPH (Silver)`
- `LEICA 24mm F2.8 ASPH ELMARIT-M sn.3737`
- `LEICA 24mm F2.8 ASPH ELMARIT-M sn.3844`

Unlabeled:

- `[중고] M 24/2.8 Elmarit (Black)`

Finder bundle:

- `LEICA 24mm F2.8 ASPH ELMARIT-M 24mm Finder sn.3737`

### Interpretation

The local pool does **not** behave like a strong two-line `non-ASPH / ASPH` taxonomy:

1. explicit `ASPH` wording dominates the usable pool
2. the unlabeled bucket is very small
3. literature evidence suggests those unlabeled examples may still belong to the same ASPH family
4. finder-attached listings behave like bundle / completeness language, not a separate optical line

The safest round-1 reading is therefore:

- one main Leica M-side `Elmarit 24` line
- with early unlabeled and finder-bundle wording kept below seed-row level

## Candidate Entity Expansion

## Candidate 1: `Leica Elmarit-M 24mm f/2.8 ASPH`

### Official / literature basis

Strong.

This is the clearly documented Leica M product line in the literature base.

### Mechanical distinction

Strong enough for `core`.

It has:

- explicit `Elmarit-M` naming
- explicit `ASPH` identity in mature production
- stable Leica M optical / barrel identity
- stable `E55` filter arrangement in the documented line

### Optical distinction

Strong enough for `core`.

The ASPH design is the only clearly documented M-side `24mm Elmarit` optical line in the reference base used here.

### Market split potential

Good.

The explicit local ASPH subset forms the dominant priced cluster around roughly `2.10M KRW`.

### Search-intent split potential

Strong.

Dealers and users explicitly write:

- `24mm F2.8 ASPH Elmarit-M`
- `M 24/2.8 Elmarit.ASPH`

### Final decision

`core`

### One-line reason

`Elmarit-M 24mm f/2.8 ASPH` is the only clearly literature-backed and operationally dominant Leica M-side `Elmarit 24` line.

## Candidate 2: broad `Leica Elmarit-M 24mm f/2.8` without `ASPH`

### Official / literature basis

Weak as a separate line.

The current literature base does not cleanly support a separate Leica M-side `non-ASPH` `24mm Elmarit-M` family on the same footing as `Elmarit 21` non-ASPH vs ASPH.

Instead, the strongest evidence points toward early ASPH-family units that were not always labeled `ASPH` in secondary references and serial compilations.

### Mechanical distinction

Not strong enough for round-1 `core`.

We do not have a clean, literature-stable M-side `non-ASPH` mechanical line definition here comparable to the `Elmarit 21` case.

### Optical distinction

Not clearly supported as separate in the current evidence base.

### Market split potential

Too thin.

The unlabeled local bucket has only `2` priced examples, both at roughly `1.58M KRW`.

### Search-intent split potential

Moderate but unstable.

Some dealers omit `ASPH`, but that wording may reflect inscription shorthand or incomplete title habits rather than a genuinely different Leica M product line.

### Final decision

`보류`

### One-line reason

The broad unlabeled `Elmarit 24` wording is operationally visible but not literature-clean enough to justify a separate round-1 canonical row.

## Candidate 3: `24mm Finder` / finder-bundle wording

### Official / literature basis

Real accessory relationship, but not a separate lens line.

### Mechanical distinction

Bundle-level only.

### Optical distinction

None.

### Market split potential

Weak as a lens row.

### Search-intent split potential

Useful as metadata, not as a canonical lens entity.

### Final decision

`overlay`

### One-line reason

Finder wording describes bundle completeness around the same lens, not a separate `Elmarit 24` subtype.

## Candidate 4: finish / coding / country / packaging variation

### Official / literature basis

Mixed to weak.

### Mechanical distinction

Weak.

### Optical distinction

None.

### Market split potential

Too weak for round-1 row creation.

### Search-intent split potential

Usable as metadata only.

### Final decision

`overlay` or `보류`

### One-line reason

`black`, `silver`, `6bit`, `country marking`, and packaging language do not currently rise to separate canonical-row level.

## Candidate 5: boundary families

### Included boundary cases

- `Summilux 24`
- `Summicron 24`
- `Super-Elmar 24`
- `Tri-Elmar`
- `Elmarit-R 24`
- `SL` / `Vario-Elmarit` 24mm zooms

### Official / literature basis

Strongly separate.

### Mechanical / optical distinction

These are different Leica naming families or different mount families, not internal `Elmarit 24` splits.

### Final decision

`out-of-family boundary`

### One-line reason

If these are allowed into the `Elmarit 24` family, the taxonomy immediately widens beyond usable canonical limits.

## Round-1 Recommendation

### Recommended immediate `core` count

`1`

### Recommended first-pass core

1. `Leica Elmarit-M 24mm f/2.8 ASPH`

### Not recommended yet

- broad `Leica Elmarit-M 24mm f/2.8` without `ASPH` as a separate row
- finder-bundle row
- finish / country / coding / packaging rows

## What Should Stay Deferred

The following should remain below round-1 seed level:

- early unlabeled `24mm f/2.8 Elmarit-M` wording
- finder-included bundle wording
- `6bit`
- black / silver finish
- country marking
- boxed completeness

These are not useless signals. They are simply not mature enough to justify separate canonical rows right now.

## Can The Next Round Move To Seed Addition?

`Yes`, but only narrowly.

The safest next round is:

1. add `Leica Elmarit-M 24mm f/2.8 ASPH` as the only immediate `core` row

Do **not** add:

- a separate broad non-`ASPH` row
- a finder-bundle row
- finish / coding / country rows

## Final Judgment

`Elmarit 24` is seedable, but as a **single modern Leica M line**, not as a strong `non-ASPH / ASPH` two-line family.

The correct round-1 posture is:

- open `Leica Elmarit-M 24mm f/2.8 ASPH` as `core`
- keep unlabeled early wording inside that broad line
- leave finder / finish / coding / country detail below canonical row level
