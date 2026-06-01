# Thambar-M 90 Hold-Seed Audit - Round 2

Date: 2026-05-08

Scope: narrow hold-seed audit for the Leica `Thambar 90` family. This round does not add seed rows, does not change classifier/query/search behavior, and does not change admin lookup ranking or UI. The goal is to determine whether the modern `Leica Thambar-M 90mm f/2.2` line is stable enough to become an explicit `hold` row without polluting broad `Thambar 90` intent.

## Executive Summary

Round-1 correctly concluded that broad `Thambar 90` should **not** be opened as a generic `core` row.

Round-2 conclusion:

- add hold row for `Leica Thambar-M 90mm f/2.2`: `yes`
- broad generic `Thambar 90` core: `no`
- generic `thambar 90` query should **not** be forced into the hold row
- original vintage `Thambar 9cm / 90mm f/2.2` row: `defer`

Recommended future `hold` row:

- `Leica Thambar-M 90mm f/2.2`

That is the narrowest structure that preserves a real Leica line without pretending the local market has already stabilized original/reissue wording across the whole `Thambar 90` family.

## Round-1 Recap

Round-1 found:

- immediate `core` candidates: `0`
- broad `Thambar 90` pool was too small and too mixed for a generic seed anchor
- strongest future `hold` candidate:
  - `Leica Thambar-M 90mm f/2.2`
- original `Thambar 9cm / 90mm f/2.2` was literature-real but locally under-labeled

Round-1 local evidence:

- clean local pool: `6`
- unique title strings: `4`
- priced count: `0`
- modern explicit title:
  - `LEICA 90mm F2.2 THAMBAR-M sn.4694`
- plain historical-looking titles:
  - `LEICA 90mm F2.2 Thambar sn.3752`
  - `LEICA 90mm F2.2 Thambar sn.4723`
  - `LEICA 90mm F2.2 Thambar sn.2472`

The key unresolved question for round-2 is whether the local `THAMBAR-M` wording is explicit enough to support a narrow `hold` row, even though broad `Thambar 90` should stay unseeded.

## Literature Baseline

The literature remains clear:

- Leica’s official product page documents `Thambar-M 90mm f/2.2` as a current Leica M line
- Leica’s 2017 press release presents `Thambar-M 1:2.2/90` as a modern renaissance of the classic lens
- Leica Wiki documents the original lens separately as `Thambar f=9 cm 1:2.2` in Leica screw-thread mount

So the modern/original split is real. The round-2 question is only whether local title language is operationally strong enough for a future hold row.

References:

- [Leica Camera - Thambar-M 90 f/2.2](https://leica-camera.com/ko-KR/photography/lenses/m/thambar-m-90mm-f2-2-black-painted)
- [Leica press release - Thambar-M 1:2.2/90](https://leica-camera.com/ja-JP/Company/Press-Centre/Press-Releases/2017/Press-Release-Leica-Camera-AG-presents-a-modern-renaissance-of-the-classic-lens-%E2%80%93-the-Leica-Thambar-M-1-2.2-90)
- [Leica Wiki - Thambar f= 9 cm 1:2.2](https://wiki.l-camera-forum.com/leica-wiki.en/index.php?title=Thambar_f%3D_9_cm_1%3A2.2)

## Local Evidence Refresh

### Broad / generic wording

Generic `Thambar 90` titles are still mixed:

- `LEICA 90mm F2.2 THAMBAR-M sn.4694`
- `LEICA 90mm F2.2 Thambar sn.3752`
- `LEICA 90mm F2.2 Thambar sn.4723`
- `LEICA 90mm F2.2 Thambar sn.2472`

That means generic:

- `thambar 90`
- `90 thambar`
- `90mm f2.2 thambar`
- `90mm f/2.2 thambar`

cannot safely be pinned to the modern row.

### Modern reissue explicit wording

Local modern markers actually observed:

- `Thambar-M`

Observed explicit modern titles:

- `LEICA 90mm F2.2 THAMBAR-M sn.4694`

Modern explicit subgroup:

- count `2`
- priced `0`

### Reissue shorthand that is **not** currently evidenced locally

Not observed in current local titles:

- `reissue`
- `복각`
- `신형`
- `1:2.2/90`

This matters because it means:

1. the modern line itself is still real and future-seedable
2. but the safest future alias set should stay narrower than the full theoretical seller-language universe

### Original / vintage explicit wording

Not meaningfully observed in current local titles:

- `9cm`
- `ltm`
- `original`
- `오리지날`
- `vintage`
- `l 90/2.2`

So the original line remains too thin for a hold row right now.

## Candidate: `Leica Thambar-M 90mm f/2.2`

### Official / literature basis

Strong.

This is a clean official Leica M line with stable naming in Leica’s own materials.

### Mechanical / structural distinction

Strong.

It is the modern Leica M reissue line, distinct from the original screw-thread lens in:

- mount
- product naming
- production era
- current Leica M system identity

### Search-intent split potential

Good enough for `hold`.

The key point is that the local `THAMBAR-M` wording is subtype-explicit. It does not require inference from accessories, finish, or serial era language.

Queries like:

- `thambar-m 90`
- `90 thambar-m`
- `90mm f2.2 thambar-m`
- `90mm f/2.2 thambar-m`

express a clearly modern reissue intent.

### Canonical naming risk

Low.

The safest canonical name is simply the official Leica line name:

- `Leica Thambar-M 90mm f/2.2`

There is no need to bake `reissue`, `복각`, or `신형` into the canonical name.

### Broad-query risk

High if used too broadly.

Generic:

- `thambar 90`
- `90 thambar`
- `90mm f2.2 thambar`
- `90mm f/2.2 thambar`

still mix:

- the modern `Thambar-M`
- and plain historical-looking `Thambar` titles

So the future hold row must only match when explicit `Thambar-M` wording is present.

### Verdict

`hold seed possible: yes`

## Recommended Hold Canonical Name

- `Leica Thambar-M 90mm f/2.2`

## Recommended Safe Aliases

Aliases supported by current local evidence or directly aligned with Leica’s official line name:

- `thambar-m 90`
- `90 thambar-m`
- `90mm f2.2 thambar-m`
- `90mm f/2.2 thambar-m`

Optional but lower-confidence literature-aligned alias:

- `thambar-m 1:2.2/90`

## Aliases That Should Stay Out For Now

These expressions are plausible, but current local support is missing:

- `thambar 90 reissue`
- `thambar 90 복각`
- `thambar 90 신형`

They may become useful later, but round-2 evidence is not strong enough to recommend them in an initial hold-row alias set.

## Broad `Thambar 90` Query Handling

Recommended behavior:

- do **not** hard-pin generic `thambar 90`
- do **not** hard-pin generic `90 thambar`
- do **not** hard-pin generic `90mm f2.2 thambar`
- do **not** hard-pin generic `90mm f/2.2 thambar`

If a future hold row is added, it should only activate when explicit `Thambar-M` wording is present.

## Original Vintage Row Status

Recommended status:

- `defer`

Reason:

- the original line is literature-real
- but local titles are still too thin on explicit `9cm / LTM / original / vintage` markers
- plain `Thambar` titles alone are not enough to safely seed an original-vintage hold row without inference

That means this round should **not** add:

- `Leica Thambar 9cm / 90mm f/2.2`
- `LTM Thambar`
- `original Thambar`
- `vintage Thambar`

## Overlay

The following should remain below row level:

- `black / chrome / silver`
- `country marking`
- `center spot filter included`
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

These may matter a lot to collector pricing, but they are not row-worthy in this round.

## Boundary Families

The `Thambar 90` family must remain separate from:

- `Summicron 90`
- `APO-Summicron-M 90`
- `Elmarit 90`
- `Tele-Elmarit 90`
- `Elmar 90`
- `Elmar-C 90`
- `Macro-Elmar-M 90`
- `R 90`
- `SL / APO-Summicron-SL 90`
- accessory-only listings such as hood / filter / center spot filter / cap / case / box
- third-party 90mm lenses

## Final Recommendation

### Add hold row

- `yes`

### Recommended hold canonical name

- `Leica Thambar-M 90mm f/2.2`

### Broad core

- `no / defer`

### Generic query

- `seed hard-pin 금지`

### Original vintage row

- `defer`

### Next step

- narrow hold-seed add is reasonable for:
  - `Leica Thambar-M 90mm f/2.2`
- original vintage `Thambar 9cm / 90mm f/2.2` should stay deferred until local explicit wording becomes stronger
