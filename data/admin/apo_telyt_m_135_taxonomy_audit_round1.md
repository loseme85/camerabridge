# APO-Telyt-M 135 Taxonomy Audit - Round 1

Date: 2026-05-08

Scope: read-heavy taxonomy audit for the Leica `APO-Telyt-M 135` family. This round does not add seed rows, does not change classifier/query/search behavior, and does not change admin lookup ranking or UI. The goal is to determine whether `APO-Telyt-M 135` is mature enough for explicit canonical seeding and, if so, at what granularity.

## Executive Summary

`APO-Telyt-M 135` is seedable, and round-1 should stay narrow.

The strongest round-1 conclusion is:

1. `Leica APO-Telyt-M 135mm f/3.4`

should be treated as the only immediate first-pass `core` entity.

Round-1 conclusion:

- immediate recommended `core` candidate count: `1`
- recommended first-pass core:
  - `Leica APO-Telyt-M 135mm f/3.4`
- explicit `hold` candidate:
  - none
- `6bit`, `black`, `country marking`, `hood included`, `cap included`, `boxed`, `case included`, and `packaging` stay `overlay`
- `Tele-Elmar 135`, `Elmarit-M 135`, `Hektor 135`, `Elmar 135`, classic `Telyt 135`, `R 135`, accessories, and third-party 135mm lenses remain out-of-family boundaries

The safest next step is a narrow seed add for `Leica APO-Telyt-M 135mm f/3.4` only.

## Family Overview

The Leica `135mm` field is crowded and easy to contaminate:

- `APO-Telyt-M 135`
- `Tele-Elmar 135`
- `Elmarit-M 135`
- `Hektor 135`
- `Elmar 135`
- classic `Telyt 135`
- `R 135`
- accessories and third-party 135mm lenses

Unlike some historical `90mm` and `28mm` families, the local `APO-Telyt-M 135` field does not show evidence of multiple internal Leica M sub-lines. The main challenge is not internal splitting, but excluding:

- `APO-Telyt-R`
- longer focal-length `APO-Telyt` R lenses
- accessory / extender contamination

Once that contamination is removed, the M-side `135mm f/3.4` line is clean and stable.

## Literature / Reference Base

### Source A: Leica official product page

Leica’s official lens page documents:

- `APO-Telyt-M 135mm f/3.4`

as the Leica M telephoto line. Leica presents it as the longest focal length in the M system and emphasizes apochromatic correction, low distortion, low falloff, and high resolution.

Reference:

- [Leica Camera - APO-Telyt-M 135mm f/3.4](https://www.leica-camera.cn/lenses/APO-Telyt-M-135mm-f-3.4)

### Source B: Leica Wiki

Leica Wiki documents:

- `135mm f/3.4 ASPH Apo-Telyt-M`

with:

- production era beginning in `1998`
- Leica M-bayonet mount
- `5 / 4` optical design
- built-in telescopic hood
- inscription `APO-TELYT-M 1:3.4/135`

Reference:

- [Leica Wiki - 135mm f/3.4 ASPH Apo-Telyt-M](https://wiki.l-camera-forum.com/leica-wiki.en/index.php/135mm_f/3.4_ASPH_Apo-Telyt-M)

### Source C: boundary literature for the predecessor family

Leica Wiki separately documents:

- `135mm f/4 Tele-Elmar`

and explicitly notes it was superseded by the `135mm f/3.4 ASPH Apo-Telyt-M`.

Reference:

- [Leica Wiki - 135mm f/4 Tele-Elmar](https://wiki.l-camera-forum.com/leica-wiki.en/index.php?title=135mm_f%2F4_Tele-Elmar)

### Interpretation

The literature stack is unusually clean:

1. `APO-Telyt-M 135mm f/3.4` is a distinct Leica M line
2. it is not just a minor variant of `Tele-Elmar 135`
3. it has a stable official name
4. no literature-real internal M-family split surfaced in this round

That is the shape of a round-1 `core` candidate.

## Local Listing Evidence

Analysis base: `data/derived/results_resolved_v2.json`

Broad `APO-Telyt` local results initially include:

- `APO-Telyt-M 135`
- `APO-Telyt-R 180`
- `APO-Telyt-R 280`
- extender / accessory contamination

Observed broad `APO-Telyt` totals:

- total raw `APO-Telyt`-matching pool: `24`
- mount split:
  - `M`: `12`
  - `R`: `12`

After excluding obvious contamination from:

- `APO-Telyt-R`
- `180mm` and `280mm` R lines
- accessory/extender-only records

the useful local `APO-Telyt-M 135` pool becomes:

- clean local pool: `16`

### Broad price clustering

KRW-parsed local observations:

- clean local pool priced count: `0`

So round-1 cannot use a local KRW median as a strong decision axis here.

That is weaker than some other rounds, but unlike mixed historical families, the title convergence is very high and there is no evidence of competing internal Leica M sub-lines.

### Local title patterns

Recurring local titles:

- `[중고] M 135/3.4 Apo-Telyt (Black)`
- `LEICA 135mm F3.4 APO-TELYT-M sn.4301`
- `LEICA 135mm F3.4 APO-TELYT-M sn.4239`
- `LEICA 135mm F3.4 APO-TELYT-M sn.3874`
- `LEICA 135mm F3.4 APO-TELYT-M sn.3910`

### Local marker frequency

Repeated local modifiers:

- `apo-telyt-m`: `12`
- `black`: `4`

Not meaningfully present in the clean local pool:

- `6bit`
- `boxed`
- `hood`
- `case`
- `germany`

### Interpretation

This family looks like a clean single-line modern Leica M family.

The important shape is:

1. the M-side line converges on one name
2. contamination comes from non-family R `APO-Telyt` lines, not internal M variants
3. there is no visible local seller shorthand suggesting a second stable M sub-line
4. price support is thin, but title convergence is strong

That is enough for a round-1 immediate `core` recommendation.

## Candidate Entity Expansion

## Candidate 1: `Leica APO-Telyt-M 135mm f/3.4`

### Official / literature basis

Strong.

This is the official Leica M line name and is explicitly separated from older `Tele-Elmar 135` literature.

### Mechanical distinction

Strong.

It is a modern Leica M-bayonet telephoto with:

- `APO-Telyt-M` naming
- `135mm f/3.4`
- built-in telescopic hood
- Leica M system identity

### Optical distinction

Strong.

The apochromatic design is part of the core line identity, not a minor variant tag.

### Market split potential

Moderate.

Local price evidence is thin, but the title support is concentrated enough that a broad `APO-Telyt-M 135` anchor remains operationally useful.

### Search-intent split potential

Strong enough for `core`.

Queries like:

- `apo-telyt 135`
- `apo telyt 135`
- `apo-telyt-m 135`
- `135 apo telyt`
- `135mm f3.4 apo telyt`
- `135mm f/3.4 apo-telyt-m`
- `m 135/3.4 apo telyt`

all point to the same modern Leica M line in current local evidence.

### Risks / caveats

One shorthand remains less safe:

- `apo 135`

That wording is too broad in principle because it could drift toward other APO 135 families or non-Leica glass. It should not drive taxonomy expansion by itself.

### Verdict

- round-1 status: `core`

## Hold Candidates

No round-1 explicit hold candidate surfaced.

Reasons:

- no repeated local wording for an internal M-side generation split
- no repeated `6bit`, packaging, or country-marking subgroup strong enough to become a separate row
- no literature-real internal split requiring a protective hold row

## Contamination / Boundary Review

The `APO-Telyt-M 135` family must remain separate from:

- `Tele-Elmar 135`
- `Elmarit-M 135`
- `Hektor 135`
- `Elmar 135`
- classic `Telyt 135`
- `R 135` lines including `APO-Telyt-R`
- accessories and extenders
- third-party `135mm` lenses

The local raw `APO-Telyt` pool confirms that R-lens contamination is the main boundary risk.

## Overlay vs Core vs Deferred

### Core

- `Leica APO-Telyt-M 135mm f/3.4`

### Overlay

The following should stay below row level:

- `6bit`
- `black`
- `country marking`
- `hood included`
- `cap included`
- `boxed`
- `case included`
- `condition`
- `original cap`
- `original hood`
- `original box`
- `original case`
- `packaging`

These may matter to pricing, but no round-1 evidence suggests they should become separate canonical rows.

### Deferred / 보류

- broad shorthand `apo 135` as a primary alias or row-shaping signal

It may still resolve to the same line in practice, but it is too broad to justify taxonomy choices on its own.

## Final Recommendation

### Immediate core candidate

- `Leica APO-Telyt-M 135mm f/3.4`

### Hold candidate

- none

### Overlay

- `6bit`
- `black`
- `country marking`
- `hood included`
- `cap included`
- `boxed`
- `case included`
- `condition`
- `original cap / hood / box / case`
- `packaging`

### Out-of-family boundary

- `Tele-Elmar 135`
- `Elmarit-M 135`
- `Hektor 135`
- `Elmar 135`
- classic `Telyt 135`
- `R 135`
- `SL / L mount 135`
- accessory-only listings
- third-party 135mm lenses

## Seed Readiness

Round-1 answer:

- immediate `core` add: `yes`
- recommended first-pass scope: one row only
- recommended next step:
  - add `Leica APO-Telyt-M 135mm f/3.4` as a narrow `core` seed

