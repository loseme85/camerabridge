# Canonical Seed Status Tracker

Last updated: 2026-05-24

## Legend

- `core added`: explicit core seed가 실제 `entities/*.json`와 `canonical_entities_index.json`에 반영됨
- `hold added`: explicit hold seed가 실제 `entities/*.json`와 `canonical_entities_index.json`에 반영됨
- `audit only`: audit report만 있고 아직 seed 반영 없음
- `hold audit completed`: hold 가능성 audit은 끝났지만 아직 row 반영 전
- `deferred`: seed 보류
- `future hold candidate`: 나중에 hold audit 또는 hold seed 후보
- `overlay`: finish, country, 6bit, box, hood, case, packaging 등 row로 만들지 않는 축
- `boundary`: 다른 family로 분리해야 하는 항목

## Status Snapshot

- `seed added / active families`: `51`
- `deferred / audit-only families`: `33`
- `explicit future hold candidates`: `2`

## Summary by Focal Length

### 14-24mm

| Family | Audit Report | Seed File | Index Status | Current Status | Core Rows | Hold Rows | Deferred / Future Candidates | Overlay Notes | Boundary Notes |
|---|---|---|---|---|---|---|---|---|---|
| Super-Vario-Elmarit-SL 14-24 | `super_vario_elmarit_sl_14_24_taxonomy_audit_round1.md` | - | `not present` | `audit only`; `deferred` | - | - | `Leica Super-Vario-Elmarit-SL 14-24mm f/2.8 ASPH` = literature-real but local title diversity still too thin; strongest deferred candidate; exact naming is `Super-Vario-Elmarit-SL`, not `Super-Vario-Elmar-SL`; order no. `11194`; clean local pool `3`, unique titles `1`, KRW-priced `3`, median `3,080,000 KRW`; representative title `[중고] SL 14-24/2.8 Vario Elmarit ASPH (Black)`; broad `14-24`, broad `super vario elmarit`, broad `leica sl 14-24`, broad `14 24 elmarit`, broad `sl 14-24` = hard-pin 금지 | `ASPH`; bayonet-side filter holder; permanently mounted hood; hood/cap/boxed/case/packaging; front-cap wording; finish; country marking; engraving; condition; unsupported markers `E82`, normal front screw filter thread, tripod collar = do not promote to row-level | `Super-Vario-Elmar-SL 16-35`; `Vario-Elmarit-SL 24-90`; `Super-APO-Summicron-SL 21`; `APO-Summicron-SL 28`; `APO-Summicron-SL 35`; M `Tri-Elmar 16-18-21 / WATE`; M 21mm / 24mm wide primes; `Vario-Elmar-R 21-35`; closed `APO-Summicron-SL 24` hypothesis; Sigma/Panasonic/Lumix 14-24/14-28/16-28/16-35/20/21/24mm lenses; accessories |

### 16-35mm

| Family | Audit Report | Seed File | Index Status | Current Status | Core Rows | Hold Rows | Deferred / Future Candidates | Overlay Notes | Boundary Notes |
|---|---|---|---|---|---|---|---|---|---|
| Super-Vario-Elmar-SL 16-35 | `super_vario_elmarit_sl_16_35_taxonomy_audit_round1.md` | `entities/super_vario_elmar_sl_16_35.json` | `active` | `core added` | `Leica Super-Vario-Elmar-SL 16-35mm f/3.5-4.5 ASPH` | - | `ASPH`, `E82`, filter-thread marker, hood/cap/boxed/case/packaging = deferred metadata / overlay; requested `Super-Vario-Elmarit-SL 16-35` naming = unsupported / hard boundary; bare `16-35`, broad `super vario elmarit`, broad `super vario elmar`, broad `leica sl 16-35`, broad `16 35 elmarit`, broad `16 35 elmar` = hard-pin 금지 | `ASPH`; `E82`; filter-thread marker; hood/cap/boxed/case/packaging | `Vario-Elmarit-SL 24-90`; `APO-Vario-Elmarit-SL 90-280`; `Vario-Elmar-R 21-35`; M `Tri-Elmar 16-18-21 / WATE`; M `Tri-Elmar 28-35-50 / MATE`; M/R wide prime families; Sigma/Panasonic/Lumix wide zooms; accessories |

### 18mm

| Family | Audit Report | Seed File | Index Status | Current Status | Core Rows | Hold Rows | Deferred / Future Candidates | Overlay Notes | Boundary Notes |
|---|---|---|---|---|---|---|---|---|---|
| Super-Elmar 18 | `super_elmar_18_taxonomy_audit_round1.md` | `entities/super_elmar_18.json` | `active` | `core added` | `Leica Super-Elmar-M 18mm f/3.8 ASPH` | - | `18 elmar` / `elmar 18` = broad shorthand; hard-pin 금지 / deferred shorthand | `6bit`; finish; `black / silver`; `country marking`; `finder included`; `hood included`; `cap included`; `boxed`; `case included`; `packaging` | `Tri-Elmar 16-18-21 / WATE`; `Super-Elmar 21`; `Elmarit 21`; `Super-Angulon 21`; `Summilux 21`; `Elmarit 24`; `Elmar-M 24`; `Summilux 24`; `R / SL`; accessory-only listings; third-party wide lenses |

### 21mm

| Family | Audit Report | Seed File | Index Status | Current Status | Core Rows | Hold Rows | Deferred / Future Candidates | Overlay Notes | Boundary Notes |
|---|---|---|---|---|---|---|---|---|---|
| Elmarit 21 | `elmarit_21_taxonomy_audit_round1.md` | `entities/elmarit_21.json` | `active` | `core added` | `Leica Elmarit-M 21mm f/2.8 ASPH`; `Leica Elmarit-M 21mm f/2.8 pre-ASPH` | - | - | finish / country / coding / boxed / hood | Super-Elmar 21 / Super-Angulon 21 / R or non-M contamination |
| Super-Elmar 21 | `super_elmar_21_taxonomy_audit_round1.md` | `entities/super_elmar_21.json` | `active` | `core added` | `Leica Super-Elmar-M 21mm f/3.4 ASPH` | - | - | finish / country / hood / packaging | Elmarit 21 / Super-Angulon 21 |
| Super-Angulon 21 | `super_angulon_21_taxonomy_audit_round1.md`; `super_angulon_21_hold_seed_audit_round2.md` | `entities/super_angulon_21.json` | `active` | `core added` + `hold added` | `Leica Super-Angulon-M 21mm f/3.4` | `Leica Super-Angulon 21mm f/4` | - | finish / country / packaging / hood | Elmarit 21 / Super-Elmar 21 |
| Summilux 21 | `summilux_21_taxonomy_audit_round1.md` | `entities/summilux_21.json` | `active` | `core added` | `Leica Summilux-M 21mm f/1.4 ASPH` | - | `21 lux` = broad shorthand; hard-pin 금지 / deferred shorthand | `6bit`; `black / silver`; `country marking`; `finder included`; `hood included`; `boxed`; `special edition`; `packaging` | `Elmarit 21`; `Super-Elmar 21`; `Super-Angulon 21`; `Tri-Elmar / WATE`; `R 21`; `SL 21`; accessories; third-party `21mm` lenses |
| Tri-Elmar 16-18-21 | `tri_elmar_16_18_21_taxonomy_audit_round1.md` | `entities/tri_elmar_16_18_21.json` | `active` | `core added` | `Leica Tri-Elmar-M 16-18-21mm f/4 ASPH` | - | `WATE` = literature-real shorthand but hard-pin 금지 / deferred shorthand; `wide angle tri-elmar` = 보수 처리; `tri-elmar 21` = ambiguous shorthand / hard-pin 금지 | `6bit`; finish; `country marking`; `finder included`; `Frankenfinder included`; `hood included`; `cap included`; `boxed`; `case included`; `packaging` | `Elmarit 21`; `Super-Elmar 21`; `Super-Angulon 21`; `Summilux 21`; `Elmarit 24`; `Elmar-M 24`; `Summilux 24`; `Tri-Elmar 28-35-50 / MATE`; `R 21`; `SL 21`; finder-only / accessory listings; third-party wide lenses |
| Super-APO-Summicron-SL 21 | `super_apo_summicron_sl_21_taxonomy_audit_round1.md` | - | `not present` | `audit only`; `deferred` | - | - | `Leica Super-APO-Summicron-SL 21mm f/2 ASPH` = literature-real but local clean lens-row support absent; strongest deferred candidate; clean local pool `0`, unique titles `0`, KRW-priced `0`, median 없음; observed local contamination includes `[중고] SL 21/2 APO 용 후드`; actual SL APO wide-prime structure is `Super-APO-Summicron-SL 21` -> `APO-Summicron-SL 28`; broad `super apo summicron 21`, broad `apo summicron 21`, broad `summicron 21`, broad `leica sl 21`, broad `21 apo`, broad `21 cron` = hard-pin 금지 | `Super-APO`; `APO`; `ASPH`; `E67`; filter-thread marker; hood/cap/boxed/case/packaging | `Super-Elmar 21`; `Elmarit 21`; `Super-Angulon 21`; `Summilux 21`; `Tri-Elmar 16-18-21 / WATE`; closed `APO-Summicron-SL 24` hypothesis; `APO-Summicron-SL 28`; `APO-Summicron-SL 35`; `Super-Vario-Elmar-SL 16-35`; `Vario-Elmarit-SL 24-90`; Sigma/Panasonic/Lumix 20/21/24mm L-mount primes; accessories |

### 21-35mm

| Family | Audit Report | Seed File | Index Status | Current Status | Core Rows | Hold Rows | Deferred / Future Candidates | Overlay Notes | Boundary Notes |
|---|---|---|---|---|---|---|---|---|---|
| Vario-Elmar-R 21-35 | `vario_elmar_r_21_35_taxonomy_audit_round1.md` | `entities/vario_elmar_r_21_35.json` | `active` | `core added` | `Leica Vario-Elmar-R 21-35mm f/3.5-4 ASPH` | - | `ROM / cam`, `ASPH`, `E67`, filter-thread marker, hood/cap/boxed/case/packaging = deferred metadata / overlay; bare `21-35`, broad `vario elmar`, broad `leica r 21-35`, broad `21 35 elmar` = hard-pin 금지 | `ROM`; `cam version`; `ASPH`; `E67`; filter-thread marker; hood/cap/boxed/case/packaging | R wide prime 21/24/28/35 families; M `Tri-Elmar 16-18-21 / WATE`; M `Tri-Elmar 28-35-50 / MATE`; `Vario-Elmar-R 28-70`; `Vario-Elmarit-R 28-90`; `Vario-Elmar-R 35-70`; `Vario-Elmarit-SL 16-35`; `Vario-Elmarit-SL 24-90`; `SL / L`; third-party wide zooms; accessories |

### 24mm

| Family | Audit Report | Seed File | Index Status | Current Status | Core Rows | Hold Rows | Deferred / Future Candidates | Overlay Notes | Boundary Notes |
|---|---|---|---|---|---|---|---|---|---|
| Elmarit 24 | `elmarit_24_taxonomy_audit_round1.md` | `entities/elmarit_24.json` | `active` | `core added` | `Leica Elmarit-M 24mm f/2.8 ASPH` | - | - | finish / country / coding / hood / boxed | Elmar-M 24 / Summilux 24 / Summicron 24 / Tri-Elmar / R / SL |
| Elmar-M 24 | `super_elmar_24_taxonomy_audit_round1.md`; `elmar_m_24_taxonomy_audit_round1.md` | `entities/elmar_m_24.json` | `active` | `core added` | `Leica Elmar-M 24mm f/3.8 ASPH` | - | - | 6bit / finish / hood bundle / country / packaging / finder bundle | Elmarit 24 / Summilux 24 / Summicron 24 / Tri-Elmar / R / SL |
| Summilux 24 | `summilux_24_taxonomy_audit_round1.md` | `entities/summilux_24.json` | `active` | `core added` | `Leica Summilux-M 24mm f/1.4 ASPH` | - | - | 6bit / finish / country / packaging / special edition | Elmarit 24 / Elmar-M 24 / Summicron 24 / Tri-Elmar / R / SL |
| Summicron 24 | `summicron_24_taxonomy_audit_round1.md` | - | `not present` | `audit only`; `deferred`; `closed non-family hypothesis` | - | - | `Leica Summicron-M 24mm f/2 ASPH` unsupported; `summicron 24` / `24 summicron` / `24 cron` / `m 24/2 summicron` = contamination shorthand | not applicable because family is unsupported | real 24mm M families are `Elmarit 24` / `Elmar-M 24` / `Summilux 24`; also boundary from 18mm / 21mm / Tri-Elmar / `R / SL` / accessories / third-party |
| Elmarit-R 24 | `elmarit_r_24_taxonomy_audit_round1.md` | `entities/elmarit_r_24.json` | `active` | `core added` | `Leica Elmarit-R 24mm f/2.8` | - | `ROM / cam / E60` = deferred internal split / overlay; broad `elmarit 24` = hard-pin 금지 | `ROM`; `1-cam / 2-cam / 3-cam`; `E60`; `filter thread`; finish; country; hood/cap/boxed/case/packaging | M 24mm families; closed `Summicron 24`; `SL Vario-Elmarit 24-90`; `R 21 / R 28`; `SL / L`; accessories; third-party |
| APO-Summicron-SL 24 | `apo_summicron_sl_24_taxonomy_audit_round1.md` | - | `not present` | `audit only`; `deferred`; `closed non-family hypothesis` | - | - | `Leica APO-Summicron-SL 24mm f/2 ASPH` = unsupported family hypothesis; official Leica SL literature does not show this product line; actual SL APO wide-prime structure jumps from `Super-APO-Summicron-SL 21mm f/2 ASPH` to `APO-Summicron-SL 28mm f/2 ASPH`; clean local pool `0`, unique titles `0`, KRW-priced `0`, median 없음; broad `apo summicron 24`, broad `summicron 24`, broad `leica sl 24`, broad `24 apo`, broad `24 cron` = contamination / hard-pin 금지 | no row-level overlay because family is unsupported; `APO`, `ASPH`, `E67`, filter-thread marker, hood/cap/boxed/case/packaging = hypothetical marker only / do not open row | `Elmarit-M 24`; `Elmar-M 24`; `Summilux-M 24`; closed `Summicron 24` hypothesis; `Elmarit-R 24`; `APO-Summicron-SL 28`; `APO-Summicron-SL 35`; `APO-Summicron-SL 50`; `APO-Summicron-SL 75`; `APO-Summicron-SL 90`; `Super-Vario-Elmar-SL 16-35`; `Vario-Elmarit-SL 24-90`; Sigma/Panasonic/Lumix 20/24/28/35mm L-mount primes; accessories |
| Summicron-SL 24 | `summicron_sl_24_taxonomy_audit_round1.md` | - | `not present` | `audit only`; `deferred`; `closed non-family hypothesis` | - | - | `Leica Summicron-SL 24mm f/2 ASPH` = unsupported family hypothesis; official Leica SL literature does not show this product line; actual SL wide-prime structure is `Super-APO-Summicron-SL 21mm f/2 ASPH` -> `APO-Summicron-SL 28mm f/2 ASPH`; existing closed `APO-Summicron-SL 24` hypothesis remains unsupported; clean local pool `0`, unique titles `0`, KRW-priced `0`, median 없음; broad `summicron-sl 24`, broad `summicron sl 24`, broad `summicron 24`, broad `leica sl 24`, broad `24 cron` = contamination / hard-pin 금지 | no row-level overlay because family is unsupported; `ASPH`, `E67`, filter-thread marker, hood/cap/boxed/case/packaging = hypothetical marker only / do not open row | closed `APO-Summicron-SL 24`; `Super-APO-Summicron-SL 21`; `APO-Summicron-SL 28`; `APO-Summicron-SL 35`; `Summicron-SL 35`; M `Elmarit-M 24`; M `Elmar-M 24`; M `Summilux-M 24`; closed M `Summicron 24` hypothesis; `Elmarit-R 24`; `Super-Vario-Elmarit-SL 14-24`; `Super-Vario-Elmar-SL 16-35`; `Vario-Elmarit-SL 24-90`; Sigma/Panasonic/Lumix 20/24/28mm L-mount primes; accessories |
| Super-Elmar 24 | `super_elmar_24_taxonomy_audit_round1.md` | - | `not present` | `audit only`; `deferred` | - | - | wrong family label closed; reframed to `Elmar-M 24mm f/3.8 ASPH` | - | do not revive `Super-Elmar 24`; use `Elmar-M 24` instead |

### 24-90mm

| Family | Audit Report | Seed File | Index Status | Current Status | Core Rows | Hold Rows | Deferred / Future Candidates | Overlay Notes | Boundary Notes |
|---|---|---|---|---|---|---|---|---|---|
| Vario-Elmarit-SL 24-90 | `vario_elmarit_sl_24_90_taxonomy_audit_round1.md` | `entities/vario_elmarit_sl_24_90.json` | `active` | `core added` | `Leica Vario-Elmarit-SL 24-90mm f/2.8-4 ASPH` | - | `ASPH`, `OIS`, `E82`, filter-thread marker, hood/cap/boxed/case/packaging = deferred metadata / overlay; bare `24-90`, broad `vario elmarit`, broad `leica sl 24-90`, broad `24 90 elmarit` = hard-pin 금지 | `ASPH`; `OIS`; `E82`; filter-thread marker; hood/cap/boxed/case/packaging | `Vario-Elmarit-R 28-90`; `Vario-Elmar-R 28-70`; `Vario-Elmar-R 35-70`; `Vario-Elmarit-R 35-70`; R prime 24/28/35/50/90 families; `Vario-Elmarit-SL 16-35`; `APO-Vario-Elmarit-SL 90-280`; `SL / L`; Sigma/Panasonic/Lumix standard zooms; accessories |

### 28mm

| Family | Audit Report | Seed File | Index Status | Current Status | Core Rows | Hold Rows | Deferred / Future Candidates | Overlay Notes | Boundary Notes |
|---|---|---|---|---|---|---|---|---|---|
| Elmarit 28 | no new audit in this batch | `entities/elmarit_28.json` | `active` | `core added` (pre-existing) | `Leica Elmarit-M 28mm f/2.8 ASPH` | - | - | finish / coding / boxed / hood / packaging | Summicron 28 / Summilux 28 / Summaron 28 / Q / R / SL |
| Summicron 28 | `summicron_28_taxonomy_audit_round1.md` | `entities/summicron_28.json` | `active` | `core added` | `Leica Summicron-M 28mm f/2 ASPH` | - | current close-focus / `ASPH II` / `NEW` / `신형` = `future hold candidate` | 6bit / finish / Safari / Titan / matte black paint / packaging | Elmarit 28 / Summilux 28 / Summaron 28 / Q / R / SL |
| Summilux 28 | `summilux_28_taxonomy_audit_round1.md` | `entities/summilux_28.json` | `active` | `core added` | `Leica Summilux-M 28mm f/1.4 ASPH` | - | no explicit hold candidate | 6bit / finish / packaging | Summicron 28 / Elmarit 28 / Summaron 28 / Q / R / SL |
| Summaron 28 | `summaron_28_taxonomy_audit_round1.md`; `summaron_28_hold_seed_audit_round2.md` | `entities/summaron_28.json` | `active` | `hold added`; broad core 없음 | - | `Leica Summaron-M 28mm f/5.6`; `Leica Summaron 28mm f/5.6 original screw-thread / LTM` | generic `summaron 28` = hard-pin 금지 / ambiguous | finder / hood / boxed / original cap / original hood / original box / packaging | Summicron 28 / Summilux 28 / Elmarit 28 / Q / R / SL |
| Tri-Elmar 28-35-50 | `tri_elmar_28_35_50_taxonomy_audit_round1.md` | `entities/tri_elmar_28_35_50.json` | `active` | `core added` | `Leica Tri-Elmar-M 28-35-50mm f/4 ASPH` | - | `MATE` = literature-real shorthand but hard-pin 금지 / deferred shorthand; `medium angle tri-elmar` = 보수 처리; `tri-elmar 28 / 35 / 50` = prime intent와 섞일 수 있어 hard-pin 금지; `E49 / E55` = real version marker but deferred internal split / overlay | `6bit`; finish; `country marking`; `E49 / E55`; `filter thread`; `hood included`; `cap included`; `boxed`; `case included`; `packaging`; `version marker` | `Tri-Elmar 16-18-21 / WATE`; `Elmarit 28`; `Summicron 28`; `Summilux 28`; `Summaron 28`; `Summicron 35`; `Summilux 35`; `Summaron 35`; `Summicron 50`; `Summilux 50`; `Noctilux 50`; `R / SL`; accessory-only listings; third-party lenses |
| Elmarit-R 28 | `elmarit_r_28_taxonomy_audit_round1.md` | `entities/elmarit_r_28.json` | `active` | `core added` | `Leica Elmarit-R 28mm f/2.8` | - | `I / II`, `ROM / cam`, `E55 / E48 / Series 7` = deferred internal split / overlay; broad `elmarit 28` = hard-pin 금지 | `ROM`; `1-cam / 2-cam / 3-cam / R-only`; `E55 / E48 / Series 7`; `filter thread`; finish; country; hood/cap/boxed/case/packaging | M 28mm families; Q-series; MATE; `R 21 / R 24 / R 35`; `SL / L`; accessories; third-party |
| APO-Summicron-SL 28 | `apo_summicron_sl_28_taxonomy_audit_round1.md` | `entities/apo_summicron_sl_28.json` | `active` | `core added` | `Leica APO-Summicron-SL 28mm f/2 ASPH` | - | `APO`, `ASPH`, `E67`, filter-thread marker, hood/cap/boxed/case/packaging = deferred metadata / overlay; broad `apo summicron 28`, broad `summicron 28`, broad `leica sl 28`, broad `28 apo`, broad `28 cron` = hard-pin 금지 | `APO`; `ASPH`; `E67`; filter-thread marker; hood/cap/boxed/case/packaging | `Summicron-M 28`; `Summilux-M 28`; `Elmarit-M 28`; `Summaron 28`; `Elmarit-R 28`; `APO-Summicron-SL 35`; `APO-Summicron-SL 50`; `APO-Summicron-SL 75`; `APO-Summicron-SL 90`; `Super-Vario-Elmar-SL 16-35`; `Vario-Elmarit-SL 24-90`; Leica `Q / Q2 / Q3`; Sigma/Panasonic/Lumix 24/28/35mm L-mount primes; accessories |
| Summicron-SL 28 | `summicron_sl_28_taxonomy_audit_round1.md` | - | `not present` | `audit only`; `deferred`; `closed non-family hypothesis` | - | - | `Leica Summicron-SL 28mm f/2 ASPH` = unsupported family hypothesis; official Leica SL `28mm f/2` literature supports `Leica APO-Summicron-SL 28mm f/2 ASPH`, not a non-APO `Summicron-SL 28`; clean local pool `0`, unique titles `0`, KRW-priced `0`, median 없음; reviewed local `SL 28 Summicron` visibility collapses into APO contamination such as `[중고] SL 28/2 APO Summicron ASPH (Black)`, `[위탁] SL 28/2 APO Summicron ASPH (Black)`, `LEICA 28mm F2 ASPH APO-SUMMICRON-SL sn.4806`; broad `summicron-sl 28`, broad `summicron sl 28`, broad `summicron 28`, broad `leica sl 28`, broad `28 cron` = contamination / hard-pin 금지 | no row-level overlay because family is unsupported; `ASPH`, `E67`, filter-thread marker, hood/cap/boxed/case/packaging = hypothetical marker only / do not open row | `APO-Summicron-SL 28`; `Summicron-M 28`; `Summilux-M 28`; `Elmarit-M 28`; `Summaron 28`; `Elmarit-R 28`; Leica `Q / Q2 / Q3`; `Super-APO-Summicron-SL 21`; closed `APO-Summicron-SL 24` hypothesis; `APO-Summicron-SL 35`; `Summicron-SL 35`; `Super-Vario-Elmar-SL 16-35`; `Vario-Elmarit-SL 24-90`; Sigma/Panasonic/Lumix 24/28/35mm L-mount primes; accessories |

### 28-70mm

| Family | Audit Report | Seed File | Index Status | Current Status | Core Rows | Hold Rows | Deferred / Future Candidates | Overlay Notes | Boundary Notes |
|---|---|---|---|---|---|---|---|---|---|
| Vario-Elmar-R 28-70 | `vario_elmar_r_28_70_taxonomy_audit_round1.md` | - | `not present` | `audit only`; `deferred` | - | - | `Leica Vario-Elmar-R 28-70mm f/3.5-4.5` = literature-real but local support too thin; `ROM / cam`, `E60`, filter-thread marker, `macro mode`, Olympia / signature marker = deferred metadata / overlay; bare `28-70`, broad `vario elmar`, broad `leica r 28-70`, broad `28 70 elmar` = hard-pin 금지 | `ROM`; `cam version`; `E60`; filter-thread marker; `macro mode`; hood/cap/boxed/case/packaging; Olympia / signature marker | `Vario-Elmarit-R 28-90`; `Vario-Elmar-R 35-70mm f/3.5`; `Vario-Elmar-R 35-70mm f/4`; `Vario-Elmarit-R 35-70mm f/2.8 ASPH`; R prime 28/35/50/90 families; `Vario-Elmarit-SL 24-90`; `SL / L`; third-party standard zooms; accessories |

### 28-90mm

| Family | Audit Report | Seed File | Index Status | Current Status | Core Rows | Hold Rows | Deferred / Future Candidates | Overlay Notes | Boundary Notes |
|---|---|---|---|---|---|---|---|---|---|
| Vario-Elmarit-R 28-90 | `vario_elmarit_r_28_90_taxonomy_audit_round1.md` | `entities/vario_elmarit_r_28_90.json` | `active` | `core added` | `Leica Vario-Elmarit-R 28-90mm f/2.8-4.5 ASPH` | - | `ROM / cam`, `ASPH`, filter-thread marker, hood/cap/boxed/case/packaging = deferred metadata / overlay; bare `28-90`, broad `vario elmarit 28-90`, broad `leica r 28-90`, broad `28 90 elmarit`, `28-90 asph r` = hard-pin 금지 | `ROM`; `cam version`; `ASPH`; filter-thread marker; hood/cap/boxed/case/packaging | R prime 28/35/50/90 families; `Vario-Elmar-R 35-70`; `Vario-Elmar-R 80-200`; `Vario-Elmar-R 70-210`; `Vario-Elmar-R 105-280`; `Vario-APO-Elmarit-R 70-180`; `Vario-Elmarit-SL 24-90`; `APO-Vario-Elmarit-SL 90-280`; `SL / L`; LTM 28-90; third-party 24-70/28-70/28-90; accessories |

### 35mm

| Family | Audit Report | Seed File | Index Status | Current Status | Core Rows | Hold Rows | Deferred / Future Candidates | Overlay Notes | Boundary Notes |
|---|---|---|---|---|---|---|---|---|---|
| Summilux 35 | no new audit in this batch | `entities/summilux_35.json` | `active` | `core added` (pre-existing) | `5 core rows present in seed file` | - | - | finish / steel rim / pre-ASPH generation metadata | Summicron 35 / Summaron 35 / non-Leica 35 contamination |
| Summicron 35 | no new audit in this batch | `entities/summicron_35.json` | `active` | `core added` (pre-existing) | `1 core row present in seed file` | - | - | finish / packaging / condition metadata | Summilux 35 / Summaron 35 / R contamination |
| Summaron 35 | `summaron_35_taxonomy_audit_round1.md` | `entities/summaron_35.json` | `active` | `core added` | `2 core rows present in seed file` | - | - | finish / country / packaging | Summicron 35 / Summilux 35 / accessories |
| Elmarit 35 | `elmarit_35_taxonomy_audit_round1.md` | - | `not present` | `audit only`; `deferred` | - | - | local usable M-side pool effectively absent; do not seed yet | accessory / R contamination dominated round-1 pool | Elmarit-R 35 / accessories / non-M contamination |
| Elmarit-R 35 | `elmarit_r_35_taxonomy_audit_round1.md` | - | `not present` | `audit only`; `deferred` | - | - | `Leica Elmarit-R 35mm f/2.8` = literature-real but local support too thin; `I / II / III`, `ROM / cam`, `E55 / E48 / Series` = deferred internal split / overlay; broad `elmarit 35` = hard-pin 금지 | `ROM`; `1-cam / 2-cam / 3-cam`; `E55 / E48 / Series 6 / Series VII`; `filter thread`; finish; country; hood/cap/boxed/case/packaging | `Summicron-R 35`; `Summilux-R 35`; M `35mm` families; M-side `Elmarit 35`; `Elmarit-R 28`; `Elmarit-R 50`; `SL / L`; accessories; third-party |
| Summicron-R 35 | `summicron_r_35_taxonomy_audit_round1.md` | - | `not present` | `audit only`; `deferred` | - | - | `Leica Summicron-R 35mm f/2` = literature-real but local support too thin; `Summicron-R I / II`, `ROM / cam`, `E55 / E48 / Series 7` = deferred internal split / overlay; broad `summicron 35` = hard-pin 금지 | `ROM`; `2-cam / 3-cam`; `E55 / E48 / Series 7`; `filter thread`; finish; country; hood/cap/boxed/case/packaging | `Summilux-R 35`; `Elmarit-R 35`; M `35mm` families; M-side `Elmarit 35`; `Elmarit-R 28`; `Summicron-R 50`; `Summilux-R 50`; `SL / L`; accessories; third-party |
| Summilux-R 35 | `summilux_r_35_taxonomy_audit_round1.md` | - | `not present` | `audit only`; `deferred` | - | - | `Leica Summilux-R 35mm f/1.4` = literature-real but local support / price evidence too thin; `ROM / cam`, `E67 / E60` = deferred internal split / overlay; broad `summilux 35` / `35 lux` = hard-pin 금지 | `ROM`; `1-cam / 2-cam / 3-cam`; `E67 / E60`; `filter thread`; finish; country; hood/cap/boxed/case/packaging | `Summicron-R 35`; `Elmarit-R 35`; M `35mm` families; M-side `Elmarit 35`; `Elmarit-R 28`; `Summicron-R 50`; `Summilux-R 50`; `SL / L`; accessories; third-party |
| APO-Summicron-SL 35 | `apo_summicron_sl_35_taxonomy_audit_round1.md` | `entities/apo_summicron_sl_35.json` | `active` | `core added` | `Leica APO-Summicron-SL 35mm f/2 ASPH` | - | `APO`, `ASPH`, `E67`, filter-thread marker, hood/cap/boxed/case/packaging = deferred metadata / overlay; non-APO `Leica Summicron-SL 35mm f/2 ASPH` = literature-real adjacent family / hard boundary; broad `apo summicron 35`, broad `summicron 35`, broad `leica sl 35`, broad `35 apo`, broad `35 cron`, broad `summicron-sl 35`, broad `summicron sl 35` = hard-pin 금지 | `APO`; `ASPH`; `E67`; filter-thread marker; hood/cap/boxed/case/packaging | `Summicron-M 35`; `Summilux-M 35`; `Summaron 35`; `Summicron-R 35`; `Summilux-R 35`; `Elmarit-R 35`; non-APO `Summicron-SL 35`; `APO-Summicron-SL 50`; `APO-Summicron-SL 75`; `APO-Summicron-SL 90`; `Super-Vario-Elmar-SL 16-35`; `Vario-Elmarit-SL 24-90`; Sigma/Panasonic/Lumix 35mm L-mount primes; accessories |
| Summicron-SL 35 | `summicron_sl_35_taxonomy_audit_round1.md` | - | `not present` | `audit only`; `deferred` | - | - | `Leica Summicron-SL 35mm f/2 ASPH` = literature-real but local support too thin; clean local pool `1`, unique titles `1`, KRW-priced `0`, median 없음; body-kit rows are excluded from clean lens-row support; `ASPH`, `E67`, filter-thread marker, hood/cap/boxed/case/packaging = deferred metadata / overlay; broad `summicron-sl 35`, broad `summicron sl 35`, broad `summicron 35`, broad `leica sl 35`, broad `35 cron` = hard-pin 금지 | `ASPH`; `E67`; filter-thread marker; hood/cap/boxed/case/packaging; finish/country metadata | `APO-Summicron-SL 35`; `Summicron-M 35`; `Summilux-M 35`; `Summaron 35`; `Summicron-R 35`; `Summilux-R 35`; `Elmarit-R 35`; `APO-Summicron-SL 50`; `APO-Summicron-SL 75`; `APO-Summicron-SL 90`; `Super-Vario-Elmar-SL 16-35`; `Vario-Elmarit-SL 24-90`; Sigma/Panasonic/Lumix 35mm L-mount primes; accessories |

### 35-70mm

| Family | Audit Report | Seed File | Index Status | Current Status | Core Rows | Hold Rows | Deferred / Future Candidates | Overlay Notes | Boundary Notes |
|---|---|---|---|---|---|---|---|---|---|
| Vario-Elmar-R 35-70 | `vario_elmar_r_35_70_taxonomy_audit_round1.md` | - | `not present` | `audit only`; `deferred` | - | - | `Leica Vario-Elmar-R 35-70mm f/3.5` = strongest deferred candidate; `Leica Vario-Elmar-R 35-70mm f/4` = secondary deferred candidate; both literature-real and locally separable but KRW-priced support absent; `Leica Vario-Elmarit-R 35-70mm f/2.8 ASPH` = separate adjacent family / do not merge; `ROM / cam`, `E60 / E67`, `macro mode`, filter-thread marker, built-in hood = deferred metadata / overlay; bare `35-70`, broad `vario elmar`, broad `leica r 35-70`, broad `35 70 elmar` = hard-pin 금지 | `ROM`; `cam version`; `E60`; `E67`; `macro mode`; filter-thread marker; built-in hood; hood/cap/boxed/case/packaging | `Vario-Elmarit-R 28-90`; `Vario-Elmarit-R 35-70mm f/2.8 ASPH`; R prime 28/35/50/90 families; `Vario-Elmar-R 70-210`; `Vario-Elmar-R 80-200`; `Vario-Elmar-R 105-280`; `Vario-APO-Elmarit-R 70-180`; `Vario-Elmarit-SL 24-90`; `SL / L`; third-party standard zooms; accessories |
| Vario-Elmarit-R 35-70 | `vario_elmarit_r_35_70_taxonomy_audit_round1.md` | - | `not present` | `audit only`; `deferred` | - | - | `Leica Vario-Elmarit-R 35-70mm f/2.8 ASPH` = literature-real but local support absent; `ROM / cam`, `ASPH`, `macro mode`, `E77`, filter-thread marker = deferred metadata / overlay; bare `35-70`, broad `vario elmarit`, broad `leica r 35-70`, broad `35 70 elmarit`, `35-70 asph` = hard-pin 금지 | `ROM`; `cam version`; `ASPH`; `macro mode`; `E77`; filter-thread marker; hood/cap/boxed/case/packaging | `Vario-Elmar-R 35-70mm f/3.5`; `Vario-Elmar-R 35-70mm f/4`; `Vario-Elmarit-R 28-90`; R prime 28/35/50/90 families; `Vario-Elmar-R 70-210`; `Vario-Elmar-R 80-200`; `Vario-Elmar-R 105-280`; `Vario-APO-Elmarit-R 70-180`; `Vario-Elmarit-SL 24-90`; `SL / L`; third-party standard zooms; accessories |

### 50mm

| Family | Audit Report | Seed File | Index Status | Current Status | Core Rows | Hold Rows | Deferred / Future Candidates | Overlay Notes | Boundary Notes |
|---|---|---|---|---|---|---|---|---|---|
| Summilux 50 | no new audit in this batch | `entities/summilux_50.json` | `active` | `core added` + existing `hold` | `6 core rows present in seed file` | `1 hold row present in seed file` | - | finish / hood / packaging / generation metadata | Noctilux 50 / Summicron 50 / non-Leica 50 contamination |
| Noctilux 50 | no new audit in this batch | `entities/noctilux_50.json` | `active` | `core added` + `hold added` (pre-existing) | `Leica Noctilux-M 50mm f/1.2 original`; `Leica Noctilux-M 50mm f/1.2 reissue`; `Leica Noctilux-M 50mm f/0.95 ASPH` | `Leica Noctilux-M 50mm f/1.0 E58`; `Leica Noctilux-M 50mm f/1.0 E60`; `Leica Noctilux-M 50mm f/1.0 V3 built-in hood` | - | finish / country / hood / cap / packaging | Summilux 50 / Summicron 50 |
| Elmar 50 | `elmar_50_taxonomy_audit_round1.md` | `entities/elmar_50.json` | `active` | `core added` | `Leica Elmar 50mm f/3.5 early 5-element collapsible`; `Leica Elmar 50mm f/3.5 late 4-element collapsible`; `Leica Elmar 50mm f/2.8 collapsible`; `Leica Elmar-M 50mm f/2.8` | - | - | collapsible / finish / country / packaging | other 50mm families |
| Summicron-R 50 | `summicron_r_50_taxonomy_audit_round1.md` | `entities/summicron_r_50.json` | `active` | `core added` | `Leica Summicron-R 50mm f/2` | - | `Summicron-R I / II`, `ROM / cam`, `Safari`, `E55 / E48` = deferred internal split / overlay; broad `summicron 50` = hard-pin 금지 | `ROM`; `1-cam / 2-cam / 3-cam`; `Safari`; `E55 / E48`; `filter thread`; finish; country; hood/cap/boxed/case/packaging; `special edition` | `Summilux-R 50`; M 50mm families; `Noctilux 50`; `Elmar 50`; `Summicron-R 35`; `Summicron-R 90`; `APO-Summicron-SL 50`; `SL / L`; accessories; third-party |
| Summilux-R 50 | `summilux_r_50_taxonomy_audit_round1.md` | `entities/summilux_r_50.json` | `active` | `core added` | `Leica Summilux-R 50mm f/1.4` | - | `Summilux-R I / II`, `ROM / cam`, `Safari`, `E55 / E60` = deferred internal split / overlay; broad `summilux 50` / `50 lux` = hard-pin 금지 | `ROM`; `1-cam / 2-cam / 3-cam`; `Safari`; `E55 / E60`; `filter thread`; finish; country; hood/cap/boxed/case/packaging; `special edition` | `Summicron-R 50`; M 50mm families; `Noctilux 50`; `Elmar 50`; `Summilux-R 35`; `Summilux-R 80`; `Summicron-R 90`; `APO-Summicron-SL 50`; `SL / L`; accessories; third-party |
| APO-Summicron-SL 50 | `apo_summicron_sl_50_taxonomy_audit_round1.md` | `entities/apo_summicron_sl_50.json` | `active` | `core added` | `Leica APO-Summicron-SL 50mm f/2 ASPH` | - | `APO`, `ASPH`, `E67`, filter-thread marker, hood/cap/boxed/case/packaging = deferred metadata / overlay; non-APO `Leica Summicron-SL 50mm f/2 ASPH` = literature-real adjacent family / hard boundary; broad `apo summicron 50`, broad `summicron 50`, broad `leica sl 50`, broad `50 apo`, broad `50 cron`, broad `summicron-sl 50`, broad `summicron sl 50` = hard-pin 금지 | `APO`; `ASPH`; `E67`; filter-thread marker; hood/cap/boxed/case/packaging | `Summicron-M 50`; `APO-Summicron-M 50`; `Summicron-R 50`; `Summilux-M 50`; `Summilux-R 50`; `Noctilux 50`; `Elmar 50`; non-APO `Summicron-SL 50`; `APO-Summicron-SL 75`; `APO-Summicron-SL 90`; `Vario-Elmarit-SL 24-90`; Sigma/Panasonic/Lumix 50mm L-mount primes; accessories |
| Summicron-SL 50 | `summicron_sl_50_taxonomy_audit_round1.md` | - | `not present` | `audit only`; `deferred` | - | - | `Leica Summicron-SL 50mm f/2 ASPH` = literature-real but local support too thin; clean local pool `1`, unique titles `1`, KRW-priced `1`, median `2,580,000 KRW`; body-kit rows are excluded from clean lens-row support; `ASPH`, `E67`, filter-thread marker, hood/cap/boxed/case/packaging = deferred metadata / overlay; broad `summicron-sl 50`, broad `summicron sl 50`, broad `summicron 50`, broad `leica sl 50`, broad `50 cron` = hard-pin 금지 | `ASPH`; `E67`; filter-thread marker; hood/cap/boxed/case/packaging; finish/country metadata | `APO-Summicron-SL 50`; `Summicron-M 50`; `APO-Summicron-M 50`; `Summicron-R 50`; `Summilux-M 50`; `Summilux-R 50`; `Noctilux 50`; `Elmar 50`; `APO-Summicron-SL 75`; `APO-Summicron-SL 90`; `Vario-Elmarit-SL 24-90`; Sigma/Panasonic/Lumix 50mm L-mount primes; accessories |

### 60mm

| Family | Audit Report | Seed File | Index Status | Current Status | Core Rows | Hold Rows | Deferred / Future Candidates | Overlay Notes | Boundary Notes |
|---|---|---|---|---|---|---|---|---|---|
| Macro-Elmarit-R 60 | `macro_elmarit_r_60_taxonomy_audit_round1.md` | - | `not present` | `audit only`; `deferred` | - | - | `Leica Macro-Elmarit-R 60mm f/2.8` = literature-real but local support too thin; `ROM / cam`, `Series 7 / E55 / E60`, `Macro-Adapter-R / ELPRO` = deferred metadata / overlay; broad `macro elmarit 60` / `60 macro` = hard-pin 금지 | `ROM`; `cam version`; `Series 7 / E55 / E60`; `filter thread`; `Macro-Adapter-R`; `ELPRO included`; finish; country; hood/cap/boxed/case/packaging | `APO-Macro-Elmarit-R 100`; `Macro-Elmar-R 100`; R 50mm families; R 90mm families; `SL / L`; accessories; third-party macro |

### 70-180mm

| Family | Audit Report | Seed File | Index Status | Current Status | Core Rows | Hold Rows | Deferred / Future Candidates | Overlay Notes | Boundary Notes |
|---|---|---|---|---|---|---|---|---|---|
| Vario-APO-Elmarit-R 70-180 | `vario_apo_elmarit_r_70_180_taxonomy_audit_round1.md` | `entities/vario_apo_elmarit_r_70_180.json` | `active` | `core added` | `Leica Vario-APO-Elmarit-R 70-180mm f/2.8` | - | `ROM / cam`, `E77 / filter thread`, `tripod collar`, `built-in hood`, `APO-EXTENDER-R included` = deferred metadata / overlay; bare `70-180`, `70 180 apo`, broad `apo elmarit 180`, broad `vario apo` = hard-pin 금지 | `ROM`; `cam version`; `E77`; `filter thread`; `tripod collar`; `built-in hood`; hood/cap/boxed/case/packaging; `APO-EXTENDER-R included` | `APO-Telyt-R 180`; `APO-Elmarit-R 180`; non-APO `Elmarit-R 180`; classic `Elmar-R 180`; `APO-Summicron-R 180`; `APO-Telyt-R 280`; `APO-Telyt-M 135`; `Elmarit-R 135`; `SL / L` zooms; third-party `70-200 / 80-200`; accessories |

### 70-210mm

| Family | Audit Report | Seed File | Index Status | Current Status | Core Rows | Hold Rows | Deferred / Future Candidates | Overlay Notes | Boundary Notes |
|---|---|---|---|---|---|---|---|---|---|
| Vario-Elmar-R 70-210 | `vario_elmar_r_70_210_taxonomy_audit_round1.md` | - | `not present` | `audit only`; `deferred` | - | - | `Leica Vario-Elmar-R 70-210mm f/4` = literature-real but local support too thin; `ROM / cam`, `E60 / filter thread`, `built-in hood`, `anniversary engraving / signature marker` = deferred metadata / overlay; bare `70-210`, broad `vario elmar`, broad `leica r 70-210`, broad `70 210 elmar` = hard-pin 금지 | `ROM`; `cam version`; `E60`; `filter thread`; `built-in hood`; hood/cap/boxed/case/packaging; anniversary engraving / signature marker | `Vario-APO-Elmarit-R 70-180`; `Vario-Elmar-R 80-200`; older `80-200mm f/4.5`; `Vario-Elmar-R 105-280`; R 180/280 primes; `SL / L` zooms; third-party `70-200 / 70-210 / 80-200`; accessories |

### 75mm

| Family | Audit Report | Seed File | Index Status | Current Status | Core Rows | Hold Rows | Deferred / Future Candidates | Overlay Notes | Boundary Notes |
|---|---|---|---|---|---|---|---|---|---|
| Summilux 75 | `summilux_75_taxonomy_audit_round1.md`; `summilux_75_hold_seed_audit_round2.md` | `entities/summilux_75.json` | `active` | `core added` + `hold added` | `Leica Summilux-M 75mm f/1.4` | `Leica Summilux-M 75mm f/1.4 later built-in-hood generation` | - | finish / country / packaging / hood | Summicron 75 / Noctilux 75 |
| Summicron 75 | `summicron_75_taxonomy_audit_round1.md` | `entities/summicron_75.json` | `active` | `core added` | `Leica Summicron-M 75mm f/2 APO ASPH` | - | - | finish / country / packaging | Summilux 75 / Noctilux 75 |
| Noctilux 75 | `noctilux_75_taxonomy_audit_round1.md` | `entities/noctilux_75.json` | `active` | `core added` | `Leica Noctilux-M 75mm f/1.25 ASPH` | - | - | finish / country / packaging | Summilux 75 / Summicron 75 |
| APO-Summicron-SL 75 | `apo_summicron_sl_75_taxonomy_audit_round1.md` | `entities/apo_summicron_sl_75.json` | `active` | `core added` | `Leica APO-Summicron-SL 75mm f/2 ASPH` | - | `APO`, `ASPH`, `E67`, filter-thread marker, hood/cap/boxed/case/packaging = deferred metadata / overlay; broad `apo summicron 75`, broad `summicron 75`, broad `leica sl 75`, broad `75 apo`, broad `75 cron` = hard-pin 금지 | `APO`; `ASPH`; `E67`; filter-thread marker; hood/cap/boxed/case/packaging | `Summicron-M 75`; `Summilux-M 75`; `Noctilux-M 75`; `APO-Summicron-SL 90`; `APO-Summicron-SL 50`; `APO-Vario-Elmarit-SL 90-280`; `Summilux-R 80`; M/R `75mm / 80mm`; Sigma/Panasonic/Lumix short tele primes; accessories |

### 80mm

| Family | Audit Report | Seed File | Index Status | Current Status | Core Rows | Hold Rows | Deferred / Future Candidates | Overlay Notes | Boundary Notes |
|---|---|---|---|---|---|---|---|---|---|
| Summilux-R 80 | `summilux_r_80_taxonomy_audit_round1.md` | `entities/summilux_r_80.json` | `active` | `core added` | `Leica Summilux-R 80mm f/1.4` | - | `ROM / cam`, `E67 / E60` = deferred internal split / overlay; broad `summilux 80` / `80 lux` = hard-pin 금지 | `ROM`; `1-cam / 2-cam / 3-cam`; `E67 / E60`; `filter thread`; finish; country; hood/cap/boxed/case/packaging | `Summilux-R 50`; R 90mm families; M 75mm families; `APO-Summicron-SL 75 / 90`; `SL / L`; accessories; third-party |

### 80-200mm

| Family | Audit Report | Seed File | Index Status | Current Status | Core Rows | Hold Rows | Deferred / Future Candidates | Overlay Notes | Boundary Notes |
|---|---|---|---|---|---|---|---|---|---|
| Vario-Elmar-R 80-200 | `vario_elmar_r_80_200_taxonomy_audit_round1.md` | - | `not present` | `audit only`; `deferred` | - | - | `Leica Vario-Elmar-R 80-200mm f/4` = literature-real but local support too thin; older `Leica Vario-Elmar-R 80-200mm f/4.5` = real adjacent family / do not merge; `ROM / cam`, `E60 / filter thread`, `STA-1 tripod collar`, `built-in hood`, `APO-EXTENDER-R included` = deferred metadata / overlay; bare `80-200`, broad `vario elmar`, broad `leica r 80-200`, broad `80 200 elmar` = hard-pin 금지 | `ROM`; `cam version`; `E60`; `filter thread`; `STA-1 tripod collar`; `built-in hood`; hood/cap/boxed/case/packaging; `APO-EXTENDER-R included` | `Vario-APO-Elmarit-R 70-180`; `Vario-Elmar-R 70-210`; `Vario-Elmar-R 105-280`; older `80-200mm f/4.5`; R 180/280 primes; `SL / L` zooms; third-party `70-200 / 80-200`; accessories |

### 90mm

| Family | Audit Report | Seed File | Index Status | Current Status | Core Rows | Hold Rows | Deferred / Future Candidates | Overlay Notes | Boundary Notes |
|---|---|---|---|---|---|---|---|---|---|
| Macro-Elmar-M 90 | `macro_elmar_m_90_taxonomy_audit_round1.md` | `entities/macro_elmar_m_90.json` | `active` | `core added` | `Leica Macro-Elmar-M 90mm f/4` | - | - | finish / hood / cap / packaging | Elmar 90 / Summicron 90 / Elmarit 90 |
| Elmar 90 | `elmar_90_taxonomy_audit_round1.md`; `elmar_c_90_hold_seed_audit_round2.md` | `entities/elmar_90.json` | `active` | `hold added`; broad core 없음 | - | `Leica Elmar-C 90mm f/4` | `Elmar III`; `LTM Elmar 90`; broad `Elmar 90` = `deferred` | black / chrome / silver / hood / cap / filter / box / pouch / adapter | Macro-Elmar-M 90 / Elmarit 90 / Tele-Elmarit 90 / Summicron 90 / R 90 |
| Elmar-C 90 | `elmar_90_taxonomy_audit_round1.md`; `elmar_c_90_hold_seed_audit_round2.md` | `entities/elmar_90.json` (within parent family) | `active via Elmar 90 family` | `hold added` | - | `Leica Elmar-C 90mm f/4` | generic `elmar 90` must not hard-pin here | same overlays as `Elmar 90` | distinct from Macro-Elmar-M 90 / classic Elmar 90 / LTM Elmar 90 |
| Summicron 90 | `summicron_90_taxonomy_audit_round1.md` | `entities/summicron_90.json` | `active` | `core added` | `Leica Summicron-M 90mm f/2`; `Leica APO-Summicron-M 90mm f/2 ASPH` | - | - | finish / country / hood / packaging | Elmarit 90 / Tele-Elmarit 90 / APO family contamination split inside same family file |
| APO-Summicron-M 90 | `summicron_90_taxonomy_audit_round1.md`; `apo_summicron_90_hold_seed_audit_round2.md` | `entities/summicron_90.json` (within parent family) | `active via Summicron 90 family` | `core added` (inside `Summicron 90`) | `Leica APO-Summicron-M 90mm f/2 ASPH` | - | no separate family file; covered by `Summicron 90` family | finish / country / hood / packaging | keep separate from non-APO contamination at lookup level |
| Summicron-R 90 | `summicron_r_90_taxonomy_audit_round1.md` | - | `not present` | `audit only`; `deferred` | - | - | `Leica Summicron-R 90mm f/2` = literature-real but local support too thin; `ROM / cam`, `Series VII / E55` = deferred internal split / overlay; `APO-Summicron-R 90` = hard boundary; broad `summicron 90` = hard-pin 금지 | `ROM`; `1-cam / 2-cam / 3-cam`; `Series VII / E55`; `filter thread`; finish; country; hood/cap/boxed/case/packaging | M 90mm families; `APO-Summicron-M 90`; `APO-Summicron-R 90`; `Elmarit-R 90`; `Tele-Elmarit 90`; `Elmar 90`; `Macro-Elmar-M 90`; `Summilux-R 80`; `Summicron-R 50`; `APO-Summicron-SL 90`; `SL / L`; accessories; third-party |
| APO-Summicron-R 90 | `apo_summicron_r_90_taxonomy_audit_round1.md` | - | `not present` | `audit only`; `deferred` | - | - | `Leica APO-Summicron-R 90mm f/2 ASPH` = literature-real but local support absent; `ROM / E60 / ASPH` = deferred metadata / overlay; broad `apo summicron 90` / `90 apo` = hard-pin 금지 | `ROM`; `E60`; `ASPH`; `filter thread`; finish; country; hood/cap/boxed/case/packaging | non-APO `Summicron-R 90`; `APO-Summicron-M 90`; `APO-Summicron-SL 90`; M 90mm families; `Elmarit-R 90`; `Elmarit-M 90`; `Tele-Elmarit 90`; `Elmar 90`; `Macro-Elmar-M 90`; `Summilux-R 80`; `SL / L`; accessories; third-party |
| APO-Summicron-SL 90 | `apo_summicron_sl_90_taxonomy_audit_round1.md` | `entities/apo_summicron_sl_90.json` | `active` | `core added` | `Leica APO-Summicron-SL 90mm f/2 ASPH` | - | `APO`, `ASPH`, `E67`, filter-thread marker, hood/cap/boxed/case/packaging = deferred metadata / overlay; broad `apo summicron 90`, broad `summicron 90`, broad `leica sl 90`, broad `90 apo`, broad `90 cron` = hard-pin 금지 | `APO`; `ASPH`; `E67`; filter-thread marker; hood/cap/boxed/case/packaging | `APO-Summicron-M 90`; non-APO `Summicron-M 90`; `APO-Summicron-R 90`; non-APO `Summicron-R 90`; `Elmarit-M 90`; `Elmarit-R 90`; `Tele-Elmarit 90`; `Macro-Elmar-M 90`; `Elmar-C 90`; `Thambar 90`; `APO-Vario-Elmarit-SL 90-280`; `APO-Summicron-SL 75`; `APO-Summicron-SL 50`; Sigma/Panasonic/Lumix short tele primes; accessories |
| Elmarit-R 90 | `elmarit_r_90_taxonomy_audit_round1.md` | - | `not present` | `audit only`; `deferred` | - | - | `Leica Elmarit-R 90mm f/2.8` = literature-real but local support too thin; `ROM / cam`, `Series VII / E55 / E48` = deferred internal split / overlay; broad `elmarit 90` = hard-pin 금지 | `ROM`; `1-cam / 2-cam / 3-cam`; `Series VII / E55 / E48`; `filter thread`; finish; country; hood/cap/boxed/case/packaging | M-side `Elmarit 90`; `Tele-Elmarit 90`; `Summicron-R 90`; `APO-Summicron-R 90`; M `90mm` families; `Elmar 90`; `Macro-Elmar-M 90`; `Summilux-R 80`; `APO-Summicron-SL 90`; `SL / L`; accessories; third-party |
| Elmarit 90 | `elmarit_90_taxonomy_audit_round1.md` | `entities/elmarit_90.json` | `active` | `core added` | `Leica Elmarit-M 90mm f/2.8` | - | - | finish / country / hood / packaging | Tele-Elmarit 90 / Summicron 90 / Elmar 90 |
| Tele-Elmarit 90 | `tele_elmarit_90_taxonomy_audit_round1.md`; `tele_elmarit_m_90_hold_seed_audit_round2.md` | `entities/tele_elmarit_90.json` | `active` | `core added` + `hold added` | `Leica Tele-Elmarit 90mm f/2.8` | `Leica Tele-Elmarit-M 90mm f/2.8` | - | finish / country / hood / packaging | Elmarit 90 / Summicron 90 / Tele-Elmar 135 contamination |
| Thambar 90 | `thambar_90_taxonomy_audit_round1.md`; `thambar_m_90_hold_seed_audit_round2.md` | `entities/thambar_90.json` | `active` | `hold added`; broad core 없음 | - | `Leica Thambar-M 90mm f/2.2` | original `Thambar 9cm / LTM / original / vintage` = `deferred`; generic `thambar 90` = hard-pin 금지 | center spot filter / hood / cap / case / box / packaging | Summicron 90 / Elmarit 90 / Tele-Elmarit 90 / Elmar 90 / Macro-Elmar-M 90 |

### 90-280mm

| Family | Audit Report | Seed File | Index Status | Current Status | Core Rows | Hold Rows | Deferred / Future Candidates | Overlay Notes | Boundary Notes |
|---|---|---|---|---|---|---|---|---|---|
| APO-Vario-Elmarit-SL 90-280 | `apo_vario_elmarit_sl_90_280_taxonomy_audit_round1.md` | `entities/apo_vario_elmarit_sl_90_280.json` | `active` | `core added` | `Leica APO-Vario-Elmarit-SL 90-280mm f/2.8-4` | - | `APO`, `OIS`, `E82`, filter-thread marker, tripod collar, hood/cap/boxed/case/packaging = deferred metadata / overlay; bare `90-280`, broad `apo vario elmarit`, broad `leica sl 90-280`, broad `90 280 elmarit` = hard-pin 금지 | `APO`; `OIS`; `E82`; filter-thread marker; tripod collar; hood/cap/boxed/case/packaging | `Vario-Elmarit-SL 24-90`; `Super-Vario-Elmarit-SL 16-35`; `APO-Summicron-SL 90`; `APO-Summicron-SL 75`; `Vario-Elmar-R 105-280`; `Vario-APO-Elmarit-R 70-180`; R `180 / 280` tele families; Sigma/Panasonic/Lumix tele zooms; accessories |

### 100mm

| Family | Audit Report | Seed File | Index Status | Current Status | Core Rows | Hold Rows | Deferred / Future Candidates | Overlay Notes | Boundary Notes |
|---|---|---|---|---|---|---|---|---|---|
| APO-Macro-Elmarit-R 100 | `apo_macro_elmarit_r_100_taxonomy_audit_round1.md` | `entities/apo_macro_elmarit_r_100.json` | `active` | `core added` | `Leica APO-Macro-Elmarit-R 100mm f/2.8` | - | `ROM / E60`, `ELPRO / macro adapter / tripod collar` = deferred metadata / overlay; broad `macro elmarit 100` / `apo macro 100` = hard-pin 금지 | `ROM`; `cam version`; `E60`; `filter thread`; `ELPRO included`; `macro adapter included`; `tripod collar included`; finish; country; hood/cap/boxed/case/packaging | `Macro-Elmar-R 100`; `Macro-Elmarit-R 60`; R 90mm families; `APO-Telyt-R 180 / 280`; `APO-Summicron-SL 90`; `SL / L`; ELPRO/accessories; third-party macro |
| Macro-Elmar-R 100 | `macro_elmar_r_100_taxonomy_audit_round1.md` | - | `not present` | `audit only`; `deferred` | - | - | `Leica Macro-Elmar-R 100mm f/4` = literature-real but local support absent; `helical / bellows`, `Series VII / E55`, `ELPRO / macro adapter` = deferred metadata / overlay; broad `macro elmar 100` / `100 macro` = hard-pin 금지 | `ELPRO included`; `macro adapter included`; `bellows / adapter wording`; `tripod collar included`; `Series VII / E55`; `filter thread`; finish; country; hood/cap/boxed/case/packaging | `APO-Macro-Elmarit-R 100`; `Macro-Elmarit-R 60`; R 90mm families; `APO-Telyt-R 180 / 280`; `APO-Summicron-SL 90`; `SL / L`; ELPRO/accessories; third-party macro |

### 105-280mm

| Family | Audit Report | Seed File | Index Status | Current Status | Core Rows | Hold Rows | Deferred / Future Candidates | Overlay Notes | Boundary Notes |
|---|---|---|---|---|---|---|---|---|---|
| Vario-Elmar-R 105-280 | `vario_elmar_r_105_280_taxonomy_audit_round1.md` | - | `not present` | `audit only`; `deferred` | - | - | `Leica Vario-Elmar-R 105-280mm f/4.2` = literature-real but local support too thin; `ROM / cam`, filter-thread marker, tripod collar / grip ecosystem, built-in hood = deferred metadata / overlay; bare `105-280`, broad `vario elmar`, broad `leica r 105-280`, broad `105 280 elmar` = hard-pin 금지 | `ROM`; `cam version`; filter-thread marker; tripod collar / grip ecosystem; built-in hood; hood/cap/boxed/case/packaging | `Vario-APO-Elmarit-R 70-180`; `Vario-Elmar-R 70-210`; `Vario-Elmar-R 80-200`; older `80-200mm f/4.5`; R 180/280 primes; `APO-Vario-Elmarit-SL 90-280`; `SL / L` zooms; third-party `70-200 / 70-300 / 100-300`; accessories |

### 135mm

| Family | Audit Report | Seed File | Index Status | Current Status | Core Rows | Hold Rows | Deferred / Future Candidates | Overlay Notes | Boundary Notes |
|---|---|---|---|---|---|---|---|---|---|
| APO-Telyt-M 135 | `apo_telyt_m_135_taxonomy_audit_round1.md` | `entities/apo_telyt_m_135.json` | `active` | `core added` | `Leica APO-Telyt-M 135mm f/3.4` | - | broad `apo 135` = hard-pin 금지 | 6bit / finish / country / hood / cap / case / packaging | R / `APO-Telyt-R` / accessory contamination |
| Tele-Elmar 135 | `tele_elmar_135_taxonomy_audit_round1.md` | `entities/tele_elmar_135.json` | `active` | `core added` | `Leica Tele-Elmar 135mm f/4` | - | `Leica Tele-Elmar-M 135mm f/4` = `future hold candidate`; broad `tele 135` = hard-pin 금지 | E39 / E46 / finish / country / accessory | APO-Telyt-M 135 / Elmarit-M 135 / Elmar 135 / R 135 |
| Elmarit-M 135 | `elmarit_m_135_taxonomy_audit_round1.md` | `entities/elmarit_m_135.json` | `active` | `core added` | `Leica Elmarit-M 135mm f/2.8` | - | generation I / II / III = `deferred`; eyes / goggles = `overlay or deferred` | finish / country / filter-thread / hood / case / packaging | Elmarit-R 135 / Tele-Elmarit 90 / other Leica 135 families |
| Elmarit-R 135 | `elmarit_r_135_taxonomy_audit_round1.md` | - | `not present` | `audit only`; `deferred` | - | - | `Leica Elmarit-R 135mm f/2.8` = literature-real but local price support absent; `ROM / cam`, `Series VII / E55 / E48` = deferred metadata / overlay; broad `elmarit 135` = hard-pin 금지 | `ROM`; `1-cam / 2-cam / 3-cam`; `Series VII / E55 / E48`; `filter thread`; finish; country; hood/cap/boxed/case/packaging | `Elmarit-M 135`; `Tele-Elmar 135`; `APO-Telyt-M 135`; `Elmar 135`; `Hektor 135`; classic `Telyt 135`; `APO-Telyt-R 180 / 280`; R 90mm families; `SL / L`; accessories; third-party |
| Hektor 135 | `hektor_135_taxonomy_audit_round1.md` | `entities/hektor_135.json` | `active` | `core added` | `Leica Hektor 135mm f/4.5` | - | `13.5cm` / LTM / screw / M shorthand = `overlay or description` | finish / country / hood / cap / case / adapter / packaging | FIKUS / hood / adapter accessory contamination; other Leica 135 families |
| Elmar 135 | `elmar_135_taxonomy_audit_round1.md` | - | `not present` | `audit only`; `deferred` | - | - | `Leica Elmar 135mm f/4` = strongest deferred candidate; strict clean local pool too thin | 13.5cm / LTM / screw / adapter / finish / accessory metadata only | Tele-Elmar 135 / TL 55-135 / accessory contamination large |
| classic Telyt 135 | `telyt_135_taxonomy_audit_round1.md` | - | `not present` | `audit only`; `deferred` | - | - | broad core 없음; hold candidate 없음; strict clean pool = `0` | Visoflex / LTM / M / adapter wording = overlay or defer | broad `telyt 135` retrieval dominated by `APO-Telyt-M 135` contamination; R / APO-Telyt-R / accessories |

### 180mm

| Family | Audit Report | Seed File | Index Status | Current Status | Core Rows | Hold Rows | Deferred / Future Candidates | Overlay Notes | Boundary Notes |
|---|---|---|---|---|---|---|---|---|---|
| APO-Telyt-R 180 | `apo_telyt_r_180_taxonomy_audit_round1.md` | - | `not present` | `audit only`; `deferred` | - | - | `Leica APO-Telyt-R 180mm f/3.4` = literature-real but local support too thin; `3-cam / R-cam only`, `Series 7.5 / E60` = deferred metadata / overlay; broad `apo telyt 180` / `telyt 180` / `180 apo` = hard-pin 금지 | `ROM`; `cam version`; `3-cam`; `R-cam only`; `Series 7.5 / E60`; `filter thread`; finish; country; hood/cap/boxed/case/packaging | `APO-Elmarit-R 180`; `Elmarit-R 180`; classic `Elmar-R 180`; generic `Telyt 180`; `Vario-APO-Elmarit-R 70-180`; `APO-Summicron-R 180`; `APO-Telyt-R 280`; M 135mm families; `SL / L`; accessories; third-party |
| APO-Elmarit-R 180 | `apo_elmarit_r_180_taxonomy_audit_round1.md` | - | `not present` | `audit only`; `deferred` | - | - | `Leica APO-Elmarit-R 180mm f/2.8` = literature-real but local support still too narrow; `APO-Elmarit-R I / II`, `ROM / cam`, `Series VIII / E67`, `built-in hood / tripod collar` = deferred metadata / overlay; broad `apo elmarit 180` / `180 apo` / `apo 180` = hard-pin 금지 | `APO-Elmarit-R I / II`; `ROM`; `cam version`; `Series VIII / E67`; `filter thread`; `built-in hood`; `tripod collar`; finish; country; hood/cap/boxed/case/packaging | `APO-Telyt-R 180`; non-APO `Elmarit-R 180`; classic `Elmar-R 180`; generic `Telyt 180`; `Vario-APO-Elmarit-R 70-180`; `APO-Summicron-R 180`; `APO-Telyt-R 280`; M 135mm families; `SL / L`; accessories; third-party |
| Elmarit-R 180 | `elmarit_r_180_taxonomy_audit_round1.md` | - | `not present` | `audit only`; `deferred` | - | - | `Leica Elmarit-R 180mm f/2.8` = literature-real but local support far too thin; `Elmarit-R I / II`, `ROM / cam`, `1-cam / 2-cam / 3-cam / R-only`, `Series VIII / E67` = deferred metadata / overlay; broad `elmarit 180` / `180 elmarit` / `r 180 elmarit` = hard-pin 금지 | `Elmarit-R I / II`; `ROM`; `cam version`; `1-cam / 2-cam / 3-cam`; `R-only`; `Series VIII / E67`; `filter thread`; finish; country; hood/cap/boxed/case/packaging | `APO-Elmarit-R 180`; `APO-Telyt-R 180`; classic `Elmar-R 180`; generic `Telyt 180`; `Vario-APO-Elmarit-R 70-180`; `APO-Summicron-R 180`; `APO-Telyt-R 280`; M 135mm families; `SL / L`; accessories; third-party |
| Elmar-R 180 | `elmar_r_180_taxonomy_audit_round1.md` | - | `not present` | `audit only`; `deferred` | - | - | `Leica Elmar-R 180mm f/4` = literature-real but local support absent; `3-cam`, `Safari`, `E55`, `MACRO-ADAPTER-R` = deferred metadata / overlay; broad `elmar 180` / `180 elmar` / `r 180 elmar` = hard-pin 금지 | `3-cam`; `Safari`; `E55`; `filter thread`; `MACRO-ADAPTER-R`; finish; country; hood/cap/boxed/case/packaging | `Elmarit-R 180`; `APO-Elmarit-R 180`; `APO-Telyt-R 180`; generic `Telyt 180`; `Vario-APO-Elmarit-R 70-180`; `APO-Summicron-R 180`; `APO-Telyt-R 280`; M 135mm families; `SL / L`; accessories; third-party |
| APO-Summicron-R 180 | `apo_summicron_r_180_taxonomy_audit_round1.md` | - | `not present` | `audit only`; `deferred` | - | - | `Leica APO-Summicron-R 180mm f/2` = literature-real but local support far too thin; `ROM / cam`, `E100 / filter drawer / built-in hood`, `APO-EXTENDER-R included`, `영상용 개조` = deferred metadata / overlay; broad `apo summicron 180` / `summicron 180` / `180 cron` / `180 apo` = hard-pin 금지 | `ROM`; `cam version`; `E100`; `filter drawer`; `filter thread`; `built-in hood`; hood/cap/boxed/case/packaging; `APO-EXTENDER-R included`; `영상용 개조` | `APO-Telyt-R 180`; `APO-Elmarit-R 180`; non-APO `Elmarit-R 180`; classic `Elmar-R 180`; generic `Telyt 180`; `Vario-APO-Elmarit-R 70-180`; `APO-Telyt-R 280`; M 135mm families; `SL / L`; accessories; third-party |

### 280mm

| Family | Audit Report | Seed File | Index Status | Current Status | Core Rows | Hold Rows | Deferred / Future Candidates | Overlay Notes | Boundary Notes |
|---|---|---|---|---|---|---|---|---|---|
| APO-Telyt-R 280 | `apo_telyt_r_280_taxonomy_audit_round1.md` | - | `not present` | `audit only`; `deferred` | - | - | `Leica APO-Telyt-R 280mm f/4` = strongest deferred candidate; `Leica APO-Telyt-R 280mm f/2.8` = secondary deferred candidate; `f/2.8` and `f/4` must not be merged; `ROM / cam`, `E60 / E112`, `tripod collar`, `APO-EXTENDER-R included` = deferred metadata / overlay; broad `apo telyt 280` / `telyt 280` / `280 apo` = hard-pin 금지 | `ROM`; `cam version`; `E60 / E112`; `filter thread`; `tripod collar`; hood/cap/boxed/case/packaging; `APO-EXTENDER-R included` | `APO-Telyt-R 180`; `APO-Elmarit-R 180`; `Elmarit-R 180`; `Elmar-R 180`; `Vario-APO-Elmarit-R 70-180`; `APO-Summicron-R 180`; M 135mm families; `SL / L`; third-party 280/300mm; accessories |

## Open Backlog

- generic `elmar 90`이 full project spot check에서 기존 `Macro-Elmar-M 90` core로 보일 수 있음
  - 이번 `Elmar-C 90` hold seed 자체의 실패가 아니라 main search / ranking scope 이슈
- `Summicron 28` current close-focus / `ASPH II` / `NEW` / `신형`
  - `future hold candidate`
- `Leica Tele-Elmar-M 135mm f/4`
  - `future hold candidate`
- `Summicron 24`
  - 현재 문헌/로컬 근거 없음
  - `Leica Summicron-M 24mm f/2 ASPH`는 unsupported
  - `summicron 24` / `24 cron`은 `M240` 및 다른 focal-length Summicron contamination
  - 새 문헌 또는 다수의 clean local title이 나오기 전까지 seed 금지
- `APO-Summicron-SL 24`
  - unsupported Leica SL family hypothesis
  - official Leica literature does not show `Leica APO-Summicron-SL 24mm f/2 ASPH`
  - actual SL APO wide-prime literature supports `Super-APO-Summicron-SL 21` and `APO-Summicron-SL 28`, not `24`
  - clean local pool `0`, unique titles `0`, KRW-priced `0`
  - broad `apo summicron 24` / `summicron 24` / `leica sl 24` / `24 apo` / `24 cron` is contamination
  - do not seed unless future official Leica literature proves this exact product line exists
- `Super-APO-Summicron-SL 21`
  - literature-real Leica SL ultra-wide APO prime family
  - strongest deferred candidate: `Leica Super-APO-Summicron-SL 21mm f/2 ASPH`
  - clean local pool `0`, unique titles `0`, KRW-priced `0`, median 없음
  - current reviewed local pool에는 accessory contamination만 있음
  - clean lens-row support가 생기기 전까지 seed 금지
  - closed `APO-Summicron-SL 24` hypothesis와 병합 금지
  - actual SL APO wide-prime line은 `Super-APO-Summicron-SL 21` -> `APO-Summicron-SL 28`
  - broad `super apo summicron 21` / `apo summicron 21` / `summicron 21` / `leica sl 21` / `21 apo` / `21 cron`은 hard-pin 금지
- `Super-Vario-Elmarit-SL 14-24`
  - literature-real Leica SL ultra-wide zoom family
  - strongest deferred candidate: `Leica Super-Vario-Elmarit-SL 14-24mm f/2.8 ASPH`
  - exact naming = `Super-Vario-Elmarit-SL`
  - `Super-Vario-Elmar-SL 16-35`와 병합 금지
  - clean local pool `3`, unique titles `1`, KRW-priced `3`, median `3,080,000 KRW`
  - current local support repeats one title shape only
  - broader clean local lens-row title diversity가 생기기 전까지 seed 금지
  - broad `14-24` / `super vario elmarit` / `leica sl 14-24` / `sl 14-24`은 hard-pin 금지
  - unsupported markers: `E82` / normal front screw filter thread / tripod collar
- `Summicron-SL 28`
  - unsupported Leica SL family hypothesis
  - official Leica SL `28mm f/2` literature supports `APO-Summicron-SL 28`, not non-APO `Summicron-SL 28`
  - clean local pool `0`, unique titles `0`, KRW-priced `0`
  - local `SL 28 Summicron` examples collapse into APO contamination
  - do not seed unless future official Leica literature proves this exact non-APO product line exists
  - broad `summicron-sl 28` / `summicron sl 28` / `summicron 28` / `leica sl 28` / `28 cron` hard-pin 금지
- `Summicron-SL 50`
  - literature-real non-APO SL `50mm f/2 ASPH` family
  - strongest deferred candidate: `Leica Summicron-SL 50mm f/2 ASPH`
  - clean local pool `1`, unique titles `1`, KRW-priced `1`, median `2,580,000 KRW`
  - 현재 clean lens-row support가 단일 title shape뿐이라 seed 금지
  - body-kit rows는 clean lens-row support에서 제외
  - `APO-Summicron-SL 50`과 병합 금지
  - broad `summicron-sl 50` / `summicron sl 50` / `summicron 50` / `leica sl 50` / `50 cron`은 hard-pin 금지
- `Elmarit-R 35`
  - literature-real family
  - clean local pool `1`로 seed activation 보류
  - `Leica Elmarit-R 35mm f/2.8`는 multiple clean local titles가 나오기 전까지 seed 금지
  - broad `elmarit 35`는 `M / R / SL / accessory` contamination 때문에 hard-pin 금지
- `Summicron-R 35`
  - literature-real family
  - clean local pool `3`, unique titles `2`로 seed activation 보류
  - `Leica Summicron-R 35mm f/2`는 multiple clean local titles가 더 쌓이기 전까지 seed 금지
  - broad `summicron 35`는 `M-side / SL / accessory / third-party` contamination 때문에 hard-pin 금지
- `Summilux-R 35`
  - literature-real family
  - clean local pool `3`, unique titles `2`, KRW-priced `0`으로 seed activation 보류
  - `Leica Summilux-R 35mm f/1.4`는 multiple clean local titles와 KRW-priced support가 더 쌓이기 전까지 seed 금지
  - broad `summilux 35` / `35 lux`는 `M-side / SL / third-party` contamination 때문에 hard-pin 금지
- `Summicron-SL 35`
  - literature-real non-APO SL `35mm f/2 ASPH` family
  - strongest deferred candidate: `Leica Summicron-SL 35mm f/2 ASPH`
  - clean local pool `1`, unique titles `1`, KRW-priced `0`, median 없음
  - 현재 clean lens-row support가 단일 title shape이고 KRW-priced clean support가 없어서 seed 금지
  - body-kit rows는 clean lens-row support에서 제외
  - `APO-Summicron-SL 35`와 병합 금지
  - broad `summicron-sl 35` / `summicron sl 35` / `summicron 35` / `leica sl 35` / `35 cron`은 hard-pin 금지
- `Vario-Elmar-R 35-70`
  - literature-real R-side standard zoom family
  - `f/3.5`와 `f/4`는 aperture-distinct candidate이며 병합 금지
  - strongest deferred candidate: `Leica Vario-Elmar-R 35-70mm f/3.5`
  - secondary deferred candidate: `Leica Vario-Elmar-R 35-70mm f/4`
  - clean local pool `9`, unique titles `7`, KRW-priced `0`, median 없음
  - `f/3.5`: local count `6`, unique titles `5`, KRW-priced `0`
  - `f/4`: local count `3`, unique titles `2`, KRW-priced `0`
  - `Leica Vario-Elmarit-R 35-70mm f/2.8 ASPH`는 separate adjacent family이며 `Vario-Elmar-R 35-70`와 병합 금지
  - KRW-priced support가 생기기 전까지 `f/3.5` / `f/4` 모두 seed 금지
  - broad `35-70` / `vario elmar` / `leica r 35-70` / `35 70 elmar`는 body-kit / accessory bundle / non-Leica 35-70 / `Vario-Elmarit-R 28-90` / `SL-L 24-90` / third-party standard zoom contamination 때문에 hard-pin 금지
- `Vario-Elmarit-R 35-70`
  - literature-real R-side standard zoom family
  - strongest deferred candidate: `Leica Vario-Elmarit-R 35-70mm f/2.8 ASPH`
  - clean local pool `0`, unique titles `0`, KRW-priced `0`, median 없음
  - current reviewed local pool에서 clean family-shaped row가 없음
  - explicit clean local titles와 KRW-priced support가 생기기 전까지 seed 금지
  - `Vario-Elmar-R 35-70mm f/3.5` / `Vario-Elmar-R 35-70mm f/4`와 병합 금지
  - `Vario-Elmarit-R 28-90mm f/2.8-4.5 ASPH`와도 병합 금지
  - broad `35-70` / `vario elmarit` / `leica r 35-70` / `35 70 elmarit` / `35-70 asph`는 adjacent Leica R 35-70, 28-90, SL/L, third-party standard zoom contamination 때문에 hard-pin 금지
- `Vario-Elmar-R 28-70`
  - literature-real R-side standard zoom family
  - strongest deferred candidate: `Leica Vario-Elmar-R 28-70mm f/3.5-4.5`
  - clean local pool `1`, unique titles `1`, KRW-priced `0`, median 없음
  - observed local row는 `Leica 28-70mm F3.5-4.5 ROM` 한 줄뿐
  - explicit `Vario-Elmar-R` seller wording이 반복되지 않음
  - KRW-priced support와 repeated explicit family wording이 생기기 전까지 seed 금지
  - `ROM`은 same-family metadata / overlay이며 separate row 금지
  - broad `28-70` / `vario elmar` / `leica r 28-70` / `28 70 elmar`는 `SL 28-70` / `SL 24-90` / third-party standard zoom / `Vario-Elmarit-R 28-90` / `Vario-Elmar-R 35-70` contamination 때문에 hard-pin 금지
- `Summicron-R 90`
  - literature-real non-APO R-side family
  - clean local pool `1`, unique titles `1`, KRW-priced `0`으로 seed activation 보류
  - `Leica Summicron-R 90mm f/2`는 multiple clean local titles와 KRW-priced support가 더 쌓이기 전까지 seed 금지
  - `APO-Summicron-R 90mm f/2 ASPH`는 별도 hard boundary
  - broad `summicron 90`은 `M-side / APO / R-side / SL / accessory` contamination 때문에 hard-pin 금지
- `APO-Summicron-R 90`
  - literature-real R-side APO family
  - clean local pool `0`, unique titles `0`, KRW-priced `0`으로 seed activation 보류
  - `Leica APO-Summicron-R 90mm f/2 ASPH`는 multiple clean local titles와 KRW-priced support가 쌓이기 전까지 seed 금지
  - broad `apo summicron 90` / `90 apo`는 `APO-Summicron-M 90` / `APO-Summicron-SL 90` / M-side APO lines contamination 때문에 hard-pin 금지
- `Elmarit-R 90`
  - literature-real R-side family
  - clean local pool `1`, unique titles `1`, KRW-priced `1`로 seed activation 보류
  - `Leica Elmarit-R 90mm f/2.8`는 multiple clean local titles와 KRW-priced support가 더 쌓이기 전까지 seed 금지
  - broad `elmarit 90`은 `SL APO Vario-Elmarit 90-280` / `Vario-Elmarit-R 28-90` / M-side `90mm` contamination 때문에 hard-pin 금지
- `Macro-Elmar-R 100`
  - literature-real R-side macro family
  - clean local pool `0`, unique titles `0`, KRW-priced `0`으로 seed activation 보류
  - `Leica Macro-Elmar-R 100mm f/4`는 multiple clean local titles와 KRW-priced support가 쌓이기 전까지 seed 금지
  - broad `macro elmar 100` / `100 macro`은 `APO-Macro-Elmarit-R 100` / M-side macro / `Macro-Elmarit-R 60` / third-party macro contamination 때문에 hard-pin 금지
- `Macro-Elmarit-R 60`
  - literature-real R-side macro family
  - clean local pool `2`, unique titles `2`, KRW-priced `0`으로 seed activation 보류
  - 현재 observed local rows는 사실상 `LEICA 60mm F2.8 MACRO ELMARIT-R sn.2630` 반복 제품 패턴 수준
  - `Leica Macro-Elmarit-R 60mm f/2.8`는 multiple clean local titles와 KRW-priced support가 쌓이기 전까지 seed 금지
  - broad `macro elmarit 60` / `60 macro`은 `APO-Macro-Elmarit-R 100` / `Macro-Elmar-R 100` / R 50mm·90mm / third-party macro contamination 때문에 hard-pin 금지
- `Elmarit-R 135`
  - literature-real R-side 135mm family
  - clean local pool `6`, unique titles `6`, KRW-priced `0`으로 seed activation 보류
  - 현재 observed local rows는 serial-number-led 소규모 묶음
  - `Leica Elmarit-R 135mm f/2.8`는 KRW-priced support와 더 다양한 clean local titles가 쌓이기 전까지 seed 금지
  - broad `elmarit 135`는 `Elmarit-M 135` / `Tele-Elmar 135` / `APO-Telyt-M 135` / `Elmar 135` / `Hektor 135` / classic `Telyt 135` contamination 때문에 hard-pin 금지
- `APO-Telyt-R 180`
  - literature-real R-side 180mm APO telephoto family
  - clean local pool `2`, unique titles `2`, KRW-priced `1`, median `500,000 KRW`로 seed activation 보류
  - 현재 observed local rows는 `Leica R 180mm f3.4 APO-Telyt Black` / `LEICA 180mm F3.4 APO-TELYT-R sn.3478` 두 title shape 중심
  - `Leica APO-Telyt-R 180mm f/3.4`는 더 다양한 clean local titles와 KRW-priced support가 쌓이기 전까지 seed 금지
  - broad `apo telyt 180` / `telyt 180` / `180 apo`는 `APO-Elmarit-R 180` / `Vario-APO-Elmarit-R 70-180` / `APO-Summicron-R 180` / `APO-Telyt-R 280` / third-party `180mm` contamination 때문에 hard-pin 금지
- `APO-Elmarit-R 180`
  - literature-real R-side 180mm APO telephoto family
  - clean local pool `3`, unique titles `3`, KRW-priced `2`, median `2,950,000 KRW`지만 seed activation은 아직 보류
  - 현재 observed local rows는 `[위탁] R 180/2.8 APO Elmarit ROM (Black)` / `[중고] R 180/2.8 APO Elmarit ROM (Black)` / `LEICA 180mm F2.8 APO-ELMARIT-R sn.3897` 세 title shape 중심
  - `Leica APO-Elmarit-R 180mm f/2.8`는 더 다양한 clean local titles와 안정적인 KRW-priced support가 쌓이기 전까지 seed 금지
  - `APO-Elmarit-R I / II`는 문헌상 real이지만 local seller title split이 안정화되기 전까지 separate row 금지
  - broad `apo elmarit 180` / `180 apo` / `apo 180`는 `Vario-APO-Elmarit-R 70-180` / `APO-Telyt-R 180` / `APO-Summicron-R 180` / non-APO `Elmarit-R 180` / third-party `180mm` contamination 때문에 hard-pin 금지
- `Elmarit-R 180`
  - literature-real R-side non-APO 180mm telephoto family
  - clean local pool `1`, unique titles `1`, KRW-priced `1`, median `2,200,000 KRW`지만 seed activation은 아직 보류
  - 현재 observed local row는 `[위탁] R 180/2.8 Elmarit (Black)` 한 title shape 중심
  - `Leica Elmarit-R 180mm f/2.8`는 더 다양한 clean local titles와 안정적인 KRW-priced support가 쌓이기 전까지 seed 금지
  - `Elmarit-R I / II`는 문헌상 real이지만 local seller title split이 안정화되기 전까지 separate row 금지
  - broad `elmarit 180` / `180 elmarit` / `r 180 elmarit`는 `APO-Elmarit-R 180` / `Vario-APO-Elmarit-R 70-180` / `APO-Telyt-R 180` / `APO-Macro-Elmarit-R 100` / other Leica `180mm` / third-party `180mm` contamination 때문에 hard-pin 금지
- `Elmar-R 180`
  - literature-real R-side 180mm f/4 telephoto family
  - clean local pool `0`, unique titles `0`, KRW-priced `0`으로 seed activation 보류
  - `Leica Elmar-R 180mm f/4`는 clean local titles와 KRW-priced support가 쌓이기 전까지 seed 금지
  - `3-cam`, `Safari`, `E55`, `MACRO-ADAPTER-R`는 문헌상 real marker지만 local seller title support가 생기기 전까지 separate row 금지
  - broad `elmar 180` / `180 elmar` / `r 180 elmar`는 `Elmarit-R 180` / `APO-Elmarit-R 180` / `APO-Telyt-R 180` / `Vario-APO-Elmarit-R 70-180` / `APO-Summicron-R 180` / `APO-Telyt-R 280` / `SL / L` / third-party `180mm` contamination 때문에 hard-pin 금지
- `APO-Summicron-R 180`
  - literature-real R-side 180mm f/2 APO telephoto family
  - clean local pool `1`, unique titles `1`, KRW-priced `1`, median `13,000,000 KRW`지만 seed activation은 보류
  - 현재 observed local row는 `Leica R 180mm f2 APO-Summicron Black [영상용 개조]` 단일 modified-listing title shape
  - `Leica APO-Summicron-R 180mm f/2`는 non-modified clean local titles와 더 안정적인 KRW-priced support가 쌓이기 전까지 seed 금지
  - `ROM`, `E100`, `filter drawer`, `built-in hood`, `APO-EXTENDER-R 2x`는 문헌상 real marker지만 local seller title support가 생기기 전까지 separate row 금지
  - broad `apo summicron 180` / `summicron 180` / `180 cron` / `180 apo`는 `APO-Telyt-R 180` / `APO-Elmarit-R 180` / non-APO `Elmarit-R 180` / classic `Elmar-R 180` / `Vario-APO-Elmarit-R 70-180` / `APO-Telyt-R 280` / `SL / L` / third-party `180mm` contamination 때문에 hard-pin 금지
- `APO-Telyt-R 280`
  - literature-real R-side 280mm APO telephoto family
  - `f/4`와 `f/2.8`은 aperture-distinct row candidates이며 하나로 병합 금지
  - total clean local pool `5`, unique titles `5`, KRW-priced `2`, median `2,400,000 KRW`지만 seed activation은 아직 보류
  - `Leica APO-Telyt-R 280mm f/4`는 strongest deferred candidate: local count `4`, KRW-priced `2`, median `2,400,000 KRW`
  - `Leica APO-Telyt-R 280mm f/2.8`는 secondary deferred candidate: local count `1`, KRW-priced `0`
  - `Leica APO-Telyt-R 280mm f/4`는 더 다양한 clean local titles와 안정적인 KRW-priced support가 쌓이기 전까지 seed 금지
  - `Leica APO-Telyt-R 280mm f/2.8`는 single-title 상태를 벗어나기 전까지 seed 금지
  - broad `apo telyt 280` / `telyt 280` / `280 apo`는 `APO-Telyt-R 180` / `APO-Elmarit-R 180` / `Elmarit-R 180` / `Elmar-R 180` / `Vario-APO-Elmarit-R 70-180` / `APO-Summicron-R 180` / `SL / L` / third-party `280 / 300mm` contamination 때문에 hard-pin 금지
- `Vario-Elmar-R 80-200`
  - literature-real R-side telephoto zoom family
  - strongest deferred candidate: `Leica Vario-Elmar-R 80-200mm f/4`
  - clean local pool `1`, unique titles `1`, KRW-priced `1`, median `600,000 KRW`로 seed activation 보류
  - observed local title은 `LEICA 80-200mm F4 VARIO-ELMAR-R sn.3699` 단일 title shape
  - older `Leica Vario-Elmar-R 80-200mm f/4.5`는 real adjacent family이며 `f/4`와 병합 금지
  - `Leica Vario-Elmar-R 80-200mm f/4`는 multiple clean local titles와 안정적인 KRW-priced support가 쌓이기 전까지 seed 금지
  - broad `80-200` / `vario elmar` / `leica r 80-200` / `80 200 elmar`는 `Vario-Elmar-R 70-210` / `Vario-Elmar-R 105-280` / older `80-200 f/4.5` / `SL-L 70-200` / Lumix-Panasonic / third-party zoom contamination 때문에 hard-pin 금지
- `Vario-Elmar-R 70-210`
  - literature-real R-side telephoto zoom family
  - strongest deferred candidate: `Leica Vario-Elmar-R 70-210mm f/4`
  - clean local pool `2`, unique titles `2`, KRW-priced `1`, median `550,000 KRW`로 seed activation 보류
  - observed local titles는 `[위탁] R 70-210/4 Vario-Elmar` / `LEICA 70-210mm F4 VARIO-ELMAR-R sn.3582` 두 title shape 중심
  - `Leica Vario-Elmar-R 70-210mm f/4`는 multiple clean local titles와 안정적인 KRW-priced support가 쌓이기 전까지 seed 금지
  - broad `70-210` / `vario elmar` / `leica r 70-210` / `70 210 elmar`는 `Vario-APO-Elmarit-R 70-180` / `Vario-Elmar-R 80-200` / older `80-200 f/4.5` / `Vario-Elmar-R 105-280` / `SL-L 70-200` / Lumix-Panasonic / third-party zoom contamination 때문에 hard-pin 금지
- `Vario-Elmar-R 105-280`
  - literature-real R-side telephoto zoom family
  - strongest deferred candidate: `Leica Vario-Elmar-R 105-280mm f/4.2`
  - clean local pool `1`, unique titles `1`, KRW-priced `1`, median `5,800,000 KRW`로 seed activation 보류
  - observed local title은 `[중고] R 105-280/4.2 ROM (Black)` 단일 약식 title shape
  - full `Vario-Elmar-R 105-280mm` wording이 반복되기 전까지 seed 금지
  - `ROM`은 문헌상 real marker지만 현재는 row-level split이 아니라 overlay / deferred metadata
  - broad `105-280` / `vario elmar` / `leica r 105-280` / `105 280 elmar`는 `Vario-APO-Elmarit-R 70-180` / `Vario-Elmar-R 70-210` / `Vario-Elmar-R 80-200` / older `80-200 f/4.5` / `APO-Vario-Elmarit-SL 90-280` / `SL-L` / Lumix-Panasonic / third-party zoom contamination 때문에 hard-pin 금지
- `Elmar 135`
  - local support 부족으로 `deferred`
- classic `Telyt 135`
  - strict clean pool `0`으로 `deferred`
- original `Thambar 9cm / LTM / vintage`
  - local explicit support 부족으로 `deferred`

## Recent Validation Snapshot

- `python3 tests/test_normalization_admin.py` = `ok`
- `python3 -m py_compile normalization_admin.py golden_set.py tests/test_normalization_admin.py` = `ok`
- `python3 golden_set.py` = `132/132`
