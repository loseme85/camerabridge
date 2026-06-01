# Super-Vario-Elmarit-SL 16-35 Taxonomy Audit - Round 1

Date: 2026-05-21

Scope: audit-only review for the requested Leica `Super-Vario-Elmarit-SL 16-35` family. This round does not add seed rows, does not modify `entities/*.json`, does not modify `canonical_entities_index.json`, and does not change classifier/query/search behavior, ranking, or UI.

## Executive Summary

The requested family label `Super-Vario-Elmarit-SL 16-35` is not supported by primary Leica literature in round 1.

Primary literature and local title evidence consistently support:

- `Leica Super-Vario-Elmar-SL 16-35mm f/3.5-4.5 ASPH`

not:

- `Leica Super-Vario-Elmarit-SL 16-35mm f/3.5-4.5 ASPH`

Round-1 conclusion:

- immediate recommended `core` candidate count: `1`
- recommended first-pass core:
  - `Leica Super-Vario-Elmar-SL 16-35mm f/3.5-4.5 ASPH`
- explicit `hold` candidate:
  - none
- literature supports one real Leica SL ultra-wide zoom family, but under `Super-Vario-Elmar-SL` naming
- local title support is strong and stable for the `Super Vario Elmar` naming
- priced KRW observations exist and cluster coherently
- broad `16-35` / `super vario elmarit` / `leica sl 16-35` / `16 35 elmarit` remain unsafe and must not be hard-pinned

The safest round-1 answer is:

1. recognize one real seedable SL-side `16-35mm f/3.5-4.5 ASPH` family
2. record that the literature-supported family name is `Super-Vario-Elmar-SL`, not `Super-Vario-Elmarit-SL`
3. keep `ASPH`, `E82`, filter-thread markers, hood/case bundles, and similar details as overlay or deferred metadata
4. keep M WATE / MATE, R `21-35`, neighboring SL zooms, and third-party wide zooms as hard boundaries

## Literature / Reference Base

### Source A: Leica Camera technical specification

Leica Camera documents:

- `Super-Vario-Elmar-SL 16-35 f/3.5-4.5 ASPH.`
- order number:
  - `11177`
- bayonet:
  - `L-Mount`
- filter mount:
  - `E82`
- no `Elmarit` naming is used on this primary reference page

Reference:

- [Leica Camera - Technical Specifications - Super-Vario-Elmar-SL 16-35 f/3.5-4.5 ASPH.](https://leica-camera.com/en-int/photography/lenses/sl/super-vario-elmar-sl-16-35mm-f3-5-4-5-asph-black/technical-specification)

### Source B: Leica product / press materials

Leica product and press materials document:

- `Super-Vario-Elmar-SL 16-35/3.5-4.5 ASPH.`
- SL-System wide zoom placement
- paired literature positioning with:
  - `Vario-Elmarit-SL 24-90`
  - `APO-Vario-Elmarit-SL 90-280`

References:

- [Leica Tech Data PDF - Super-Vario-Elmar-SL 16-35 f/3.5-4.5 ASPH.](https://leica-camera.com/sites/default/files/pm-54144-11177_Datenblatt_Super-Vario-Elmar-16-35-ASPH_EN.pdf)
- [Leica Press Release - Super-Vario-Elmar-SL 16-35/3.5-4.5 ASPH. expands the SL-System](https://leica-camera.com/fr-FR/Company/Press-Centre/Press-Releases/2018-not-urgent-translatable/Press-Release-Versatile-wide-angle-lens-Super-Vario-Elmar-SL-16%E2%80%9335-3.5%E2%80%934.5-ASPH.-expands-the-SL-System)

### Source C: Leica Wiki

Leica Wiki documents:

- `Super-Vario-Elmar-SL 16-35 mm f/3.5-4.5 ASPH.`
- order no.:
  - `11177`
- bayonet fitting:
  - Leica `L` bayonet
- filter / hood ecosystem:
  - `E82`
- again, the literature naming is `Elmar`, not `Elmarit`

Reference:

- [Leica Wiki - Super-Vario-Elmar-SL 16-35 mm f/3.5-4.5 ASPH.](https://wiki.l-camera-forum.com/leica-wiki.en/index.php/Super-Vario-Elmar-SL_16%E2%80%9335_mm_f/3.5%E2%80%934.5_ASPH.)

## Taxonomy Implication from Literature

Round-1 literature supports:

- one real family:
  - `Leica Super-Vario-Elmar-SL 16-35mm f/3.5-4.5 ASPH`

Round-1 literature does **not** support:

- `Leica Super-Vario-Elmarit-SL 16-35mm f/3.5-4.5 ASPH`

So the requested family label is best treated as a nomenclature mismatch, not as a separate Leica family.

Literature also supports metadata structure around:

- `ASPH`
- `E82`
- filter-thread marker
- hood / cap / case / packaging ecosystem

These are real markers, but round 1 does not justify opening separate rows for them.

## Boundary Check

This family must remain separate from:

- `Leica Vario-Elmarit-SL 24-90mm f/2.8-4 ASPH`
- `Leica APO-Vario-Elmarit-SL 90-280mm f/2.8-4`
- `Leica Vario-Elmar-R 21-35mm f/3.5-4 ASPH`
- `Leica Vario-Elmar-R 28-70mm f/3.5-4.5`
- `Leica Vario-Elmarit-R 28-90mm f/2.8-4.5 ASPH`
- `Leica Vario-Elmar-R 35-70mm f/3.5`
- `Leica Vario-Elmar-R 35-70mm f/4`
- M `Tri-Elmar 16-18-21 / WATE`
- M `Tri-Elmar 28-35-50 / MATE`
- M / R wide prime families:
  - `21mm`
  - `24mm`
  - `28mm`
  - `35mm`
- Sigma / Panasonic / Lumix `14-24mm / 16-28mm / 16-35mm / 17-35mm / 20-35mm`
- accessory-only listings

## Local Listing Evidence

Analysis base:

- `data/normalized/normalized_latest.json`
- `data/derived/results_resolved_v2.json`
- `data/sold_items.json`

### Broad retrieval behavior

Broad shorthand is risky.

Within the wider `16-35 / super vario elmar / sl` field, adjacent or contaminating rows appear:

- `LEICA SL2 16-35mm F3.5-4.5 ASPH sn.4687/5576`
- `Leica 16-35mm F3.5-4.5 Asph Super Vario-Elmar`
  - foreign sold / non-local pricing context
- neighboring SL zoom families remain structurally close in literature and title space
- third-party `16-35` / `17-35` / `20-35` wide zoom retrieval remains plausible on broad shorthand

Interpretation:

- bare `16-35`
- broad `super vario elmarit`
- broad `leica sl 16-35`
- broad `16 35 elmarit`

are not safe shaping aliases in round 1 because they can drift into:

- SL body-kit or bundle-like rows
- neighboring SL zooms
- R `21-35`
- M WATE / Tri-Elmar family references
- third-party wide zooms
- accessory-only listings

### Clean local SL-side pool

After restricting to explicit `16-35mm`, explicit SL-side wording, and excluding body-kit style contamination, neighboring SL zooms, R-side zooms, M WATE / Tri-Elmar, third-party wide zooms, and accessory contamination, the usable local pool becomes:

- clean local pool: `5`
- unique titles: `4`
- KRW-priced count: `3`
- KRW median: `4,950,000 KRW`

Representative clean titles:

- `[중고] SL 16-35/3.5-4.5 Super Vario Elmar ASPH (Black)`
- `LEICA 16-35mm F3.5-4.5 ASPH SUPER-VARIO-ELMAR-SL sn.4689`
- `LEICA 16-35mm F3.5-4.5 ASPH SUPER-VARIO-ELMAR-SL sn.4687`
- `LEICA 16-35mm F3.5-4.5 ASPH SUPER-VARIO-ELMAR-SL sn.4688`

Observed KRW price points:

- `4,500,000 KRW`
- `4,950,000 KRW`
- `5,980,000 KRW`

Interpretation:

- local wording is family-correct for `Super Vario Elmar`
- local wording does not support the requested `Super-Vario-Elmarit-SL` naming
- multiple independent title shapes converge on the same SL-side `16-35` family
- priced observations exist in KRW and cluster in a coherent band

## Round-1 Recommendation

### Immediate `core` candidate count

- `1`

### Recommended first-pass `core`

- `Leica Super-Vario-Elmar-SL 16-35mm f/3.5-4.5 ASPH`

### Explicit `hold` candidates

- none

## Why not seed the requested family name directly?

Because round-1 literature and local evidence both contradict the requested `Elmarit` naming.

The real family appears seedable, but the literature-supported canonical string is:

- `Leica Super-Vario-Elmar-SL 16-35mm f/3.5-4.5 ASPH`

not:

- `Leica Super-Vario-Elmarit-SL 16-35mm f/3.5-4.5 ASPH`

So the next seed round should only open a narrow row if it uses the corrected family naming.

## Overlay / Deferred Metadata

Keep below row level:

- `ASPH`
- `E82`
- filter-thread marker
- hood included
- cap included
- boxed
- case included
- packaging
- finish / country style metadata

Do not open separate rows for:

- `ASPH`-only split
- `E82` split
- hood / case / boxed bundle rows
- body-kit style SL bundle rows

## Out-of-Family Boundaries

Do not merge with:

- `Vario-Elmarit-SL 24-90`
- `APO-Vario-Elmarit-SL 90-280`
- `Vario-Elmar-R 21-35`
- `Vario-Elmar-R 28-70`
- `Vario-Elmarit-R 28-90`
- `Vario-Elmar-R 35-70`
- M `Tri-Elmar 16-18-21 / WATE`
- M `Tri-Elmar 28-35-50 / MATE`
- M / R wide primes
- Sigma / Panasonic / Lumix wide zooms
- accessory-only listings

## Seed-Round Readiness

For the requested family label:

- `Super-Vario-Elmarit-SL 16-35`
  - not seed-ready as named

For the literature-correct family label:

- `Super-Vario-Elmar-SL 16-35`
  - seed-ready in a future narrow seed round

## Validation

Validation run after this audit-only report update:

- `python3 tests/test_normalization_admin.py`
  - `ok`
- `python3 -m py_compile normalization_admin.py golden_set.py tests/test_normalization_admin.py`
  - `ok`
- `python3 golden_set.py`
  - `132/132`
