# Summilux 75 Taxonomy Audit - Round 1

Date: 2026-04-30

Scope: read-heavy taxonomy audit for the Leica `Summilux 75` family. This round does not add seed rows, does not change classifier/query/search behavior, and does not change admin lookup ranking or UI. The goal is to determine whether `Summilux 75` is mature enough for explicit canonical seeding and, if so, at what granularity.

## Executive Summary

`Summilux 75` is seedable, but only if round 1 stays conservative.

The strongest immediate structure is:

1. `Leica Summilux-M 75mm f/1.4`

There is also a meaningful internal version signal around the later built-in-hood / commonly dealer-labeled `2세대 캐나다` cluster, but round 1 evidence does **not** support opening multiple `core` rows yet.

Round-1 conclusion:

- immediate recommended `core` candidate count: `1`
- recommended first-pass core:
  - `Leica Summilux-M 75mm f/1.4`
- later built-in-hood / `2세대 캐나다` wording is a plausible future `hold` candidate
- `Germany / Canada`, `black`, `titanium`, `ELC / ELW`, `anniversary`, `6bit` stay below round-1 core level

## Family Overview

Unlike several 90mm families, `Summilux 75` is relatively clean as a Leica M portrait-lens line.

The contamination we need to exclude is mostly:

- `Summicron 75`
- `SL 75`
- unrelated `75mm` non-Leica lenses
- serial-number false hits from `Summilux 35/50`

After excluding those, the remaining local evidence points to a single dominant family line: `75mm f/1.4 Summilux-M`.

The internal taxonomic question is not whether separate families exist.  
It is whether version language like:

- `독일`
- `2세대`
- `캐나다`
- `6bit`

should already become canonical rows, or remain below core level.

## Literature / Reference Base

### Source A: Leica Wiki - `75mm f/1.4 Summilux-M`

Leica Wiki documents the line as:

- Leica order numbers `11814`, `11815` (built-in hood), `11810`
- production era `1980-2007`
- variants including black, titanium, ELC, ELW, 1913-1983 anniversary edition
- Leica M-bayonet
- `7 / 5`
- filter size `E60`
- after 1982, a built-in hood version `11815`

Reference:

- https://wiki.l-camera-forum.com/leica-wiki.en/index.php/75mm_f/1.4_Summilux-M

### Interpretation

The literature strongly supports one broad product line:

- `75mm f/1.4 Summilux-M`

It also confirms that there are meaningful internal production variants, especially:

- pre-built-in-hood versus later built-in-hood
- Canada / Germany inscription history

But literature alone does not mean these should be round-1 `core` entities.

## Local Listing Evidence

Analysis base: `data/derived/results_resolved_v2.json`

Using a strict 75mm focal filter, the useful local pool is approximately:

- total `Summilux 75` listings: `37`
- priced listings with parsable KRW values: `18`
- overall observed median: about `5.13M KRW`

### Repeating local title signals

Observed marker counts:

| Marker | Count | Note |
| --- | ---: | --- |
| `독일` / `Germany` | 6 | meaningful but not necessarily same as one optical version |
| `2세대` | 9 | strongest internal dealer-language split |
| `6bit` | 1 | too sparse |
| `black` | 16 | finish-level only |
| `silver` | 0 | not useful |
| `ver.iii` | 1 | too sparse |

Representative titles:

- `Leica M 75mm f1.4 Summilux [Made in Germany]`
- `[중고] M75/1.4 Summilux 독일 (Black)`
- `[중고] M 75/1.4 Summilux 2세대 캐나다 (Black)`
- `LEICA 75mm F1.4 SUMMILUX-M sn.3259`
- `LEICA 75mm F1.4 Ver.III(Germany) SUMMILUX-M sn.3837`
- `[중고] M 75/1.4 Summilux 6bit (Black)`

### Local price clustering

Within the priced subset:

| Cohort | Count | Median KRW | Interpretation |
| --- | ---: | ---: | --- |
| `독일 / Germany` wording | 7 | ~`6.50M` | premium cluster |
| `2세대 캐나다` wording | 9 | ~`4.68M` | lower but still coherent cluster |
| `6bit` wording | 1 | `6.98M` | too sparse |

### Interpretation

This is enough to say:

1. there is one strong broad family line
2. there is nontrivial internal version language
3. that internal language is **not yet clean enough** to justify multiple round-1 `core` rows

Why not?

- `Germany` is not the same thing as a clean canonical version name
- `2세대 캐나다` is repeated, but it blends version, country marking, and local dealer shorthand
- the literature split is really about built-in hood / order-number progression, while local titles often surface country language instead

So there is clear subtype evidence, but not yet clean enough canonical naming for round-1 multi-core seeding.

## Candidate Entity Expansion

## Candidate 1: `Leica Summilux-M 75mm f/1.4`

### Official / literature basis

Very strong.

This is a clearly documented Leica M line with a long production run and stable naming.

### Mechanical distinction

Strong enough for `core`.

Whatever the internal hood/version progression, the broad `75mm f/1.4 Summilux-M` identity is extremely stable.

### Optical distinction

Strong enough for `core`.

The line is coherent as a product family and not easily confused with `Summicron 75` or other neighboring 75mm products.

### Market split potential

Strong.

The local pool is large enough for a broad price-table anchor, even if internal variants still overlap.

### Search-intent split potential

Strong.

Users and dealers clearly search and list:

- `75mm f1.4 Summilux`
- `M75/1.4 Summilux`
- `Summilux-M 75`

### Final decision

`core`

### One-line reason

`Summilux-M 75mm f/1.4` is a stable Leica M main line with strong literature support, clean title recognition, and enough local market presence to serve as a first-pass core entity.

## Candidate 2: later built-in-hood / commonly dealer-labeled `2세대 캐나다`

### Official / literature basis

Moderate to strong.

The literature does confirm a later built-in-hood progression after 1982, but it does not map perfectly to the local dealer shorthand `2세대 캐나다`.

### Mechanical distinction

Real.

This is not just finish-level metadata. There is an actual production/version distinction underneath the seller wording.

### Optical distinction

Weak as a separate optical family.

The main distinction is version/build progression rather than a wholly separate Leica 75 product concept.

### Market split potential

Moderate.

The local `2세대 캐나다` cluster is repeated and noticeably cheaper than the `독일` cluster.

### Search-intent split potential

Moderate.

When sellers explicitly use `2세대 캐나다`, they are expressing a narrower intent. But the wording mixes:

- country marking
- version shorthand
- local market vocabulary

### Final decision

`hold`

### One-line reason

There is enough repeated local signal to consider a future explicit `hold` row, but not enough canonical cleanliness to open it as round-1 `core`.

## Candidate 3: `Germany` / early version as its own row

### Official / literature basis

Partial.

There are real early/later distinctions, but local `Germany` wording is not the same thing as a clean Leica version label.

### Search-intent split potential

Moderate but noisy.

`Germany` appears in local titles, yet it behaves partly like country marking and partly like a proxy for preferred earlier production.

### Final decision

`overlay` or `보류`

### One-line reason

`Germany` is a strong market descriptor, but not yet clean enough as a round-1 canonical row name.

## Candidate 4: `6bit`, `black`, `titanium`, `ELC / ELW`, `anniversary`

### Official / literature basis

Real variants exist.

### Search-intent split potential

Weak for round 1.

Local title support is sparse or mostly finish-level.

### Final decision

`overlay` or `보류`

### One-line reason

These are real variants, but they are secondary to the main family identity and too sparse for immediate seed splitting.

## Recommended Round-1 Core Count

**1**

Recommended immediate core candidate:

1. `Leica Summilux-M 75mm f/1.4`

## What Should Still Wait

- a separate row for `2세대 캐나다`
- a separate row for `Germany`
- any `6bit`, `titanium`, `ELC / ELW`, `anniversary` split

## Can The Next Round Add Seed?

**Yes.**

The safe next-step seed direction is:

- add `Leica Summilux-M 75mm f/1.4` as a single explicit `core` row

Possible later follow-up:

- a narrow hold-seed audit for the later built-in-hood / `2세대 캐나다` cluster

But round 1 should not open multiple `core` rows.
