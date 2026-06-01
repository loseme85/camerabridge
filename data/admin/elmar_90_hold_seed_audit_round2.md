# Elmar 90 Hold-Seed Audit - Round 2

Date: 2026-04-29

Scope: second audit pass for the Leica `Elmar 90` family, focused not on `core` seeding but on whether any candidate is mature enough for an explicit `hold` row. This round does not change seed files, search logic, query logic, admin lookup ranking, or UI.

## Round 1 Recap

Round 1 conclusion:

- immediate `core` candidate count: `0`
- reason:
  - local pool too small
  - subtype contamination too high
  - title labeling too weak

Most plausible future candidates identified in round 1:

1. `90mm f/4 Elmar-C`
2. `Elmar (III) 1:4 / 90mm`

Additional literature-backed but weakly labeled candidates:

- `90mm f/4 Elmar` collapsible
- `90mm f/4 Elmar` rigid

This round asks a narrower question:

Can any of those move from pure taxonomy-audit state into explicit `hold` rows?

## Evaluation Criteria

For each candidate:

1. Is it a real independent line in official / literature sources?
2. Is the mechanical or optical distinction strong enough to justify a named explicit row?
3. Is search intent separable?
4. Do local listing titles expose that distinction often enough to attach listings to it with acceptable admin confidence?
5. If not core, is it still stable enough for explicit `hold`?

## Local Listing Snapshot

Useful `Elmar 90` pool after excluding obvious contamination is still very small.

Observed local counts:

| Candidate bucket | Count | Priced | Notes |
| --- | ---: | ---: | --- |
| `Elmar-C` explicit | 3 | 2 | titles explicitly say `Elmar-C` or `C Elmar` |
| `Elmar (III)` explicit `3-element` | 1 | 0 | one clean collector-style title |
| `collapsible` explicit | 0 | 0 | no direct local label signal |
| `rigid` explicit | 0 | 0 | no direct local label signal |
| generic `90/4 Elmar` | 13 | 5 | too broad to subtype confidently |

This matters because explicit `hold` rows still need enough label stability to be usable in admin normalization.

## Candidate A: `90mm f/4 Elmar-C`

### Official / literature basis

Strong.

Leica Wiki documents `90mm f/4 Elmar-C` as a distinct 1973-1977 CL-era line, with:

- M-bayonet
- `4 / 4` optical construction
- separate low-cost / compact system identity
- separate naming convention (`Elmar-C`)

### Mechanical distinction

Strong.

`Elmar-C` is not just a finish or mount variant of the older `Elmar 90` lines. It is a compact CL-era product line with different body fit expectations and a distinct physical identity.

### Optical distinction

Moderate-to-strong.

The literature treats it as a distinct `4 / 4` lens, not simply a relabeled earlier `90/4 Elmar`.

### Search-intent separation

Good.

Users and dealers can meaningfully search:

- `Elmar-C 90`
- `90mm f/4 Elmar-C`
- `C Elmar`

Unlike generic `90/4 Elmar`, the name itself is already subtype-explicit.

### Local listing label availability

Good enough for `hold`.

Local examples:

- `LEICA 90mm F4 ELMAR-C sn.2573`
- `Leica 90mm F4 C Elmar`

Sample is small, but the subtype wording is explicit and stable.

### Explicit hold-row suitability

Yes.

This is exactly the kind of entity that is often too sparse for `core` but still strong enough for explicit `hold`:

- official line is distinct
- search intent is distinct
- listing titles can identify it directly

### Final decision

`explicit hold row recommended`

### Recommended hold row

- `canonical_name`: `Leica Elmar-C 90mm f/4`
- `status`: `hold`
- `aliases`:
  - `90 elmar-c`
  - `90mm f4 elmar-c`
  - `90 c elmar`
  - `elmar-c 90`
- `key_discriminators`:
  - `90`
  - `f4`
  - `elmar-c`
  - `c elmar`
  - `cl line`

### One-line reason

`Elmar-C` has enough literature independence and enough title-level explicitness to justify a named `hold` row now.

## Candidate B: `Elmar (III) 1:4 / 90mm`

### Official / literature basis

Strong.

Leica Wiki clearly documents a late `1964-1965` `3 / 3` line, making it one of the clearest optical redesigns in the `Elmar 90` family.

### Mechanical distinction

Moderate.

It is historically specific and collector-distinct, but not usually presented in dealer titles with a stable mainstream naming convention.

### Optical distinction

Strong.

This is the best optical split in the whole family: a real `3-element` late line versus earlier `4 / 3` lines.

### Search-intent separation

Collector-strong, mainstream-weak.

Collectors may search:

- `Elmar III 90`
- `90mm Elmar 3-element`

But ordinary dealer language usually does not.

### Local listing label availability

Too weak today.

Current local evidence is effectively:

- `LEICA 90mm F4 Elmar 3-element sn.2089`

That is a real signal, but it is only one listing and not enough to feel operationally stable for admin normalization.

### Explicit hold-row suitability

Not yet.

This is close, but not quite there. The literature is strong enough that a future hold row is plausible, yet the current local label availability is too thin. Adding it now would make the seed more elegant on paper than useful in practice.

### Final decision

`still taxonomy-audit state`

### One-line reason

`Elmar (III)` is a real historical line, but current local title support is too sparse for a useful explicit `hold` row.

## Comparison Case: `90mm f/4 Elmar` collapsible / rigid

### Literature strength

Strong.

Leica Wiki explicitly distinguishes collapsible and rigid versions and even notes separate approximate street-value ranges.

### Search-intent strength

Moderate.

Collectors do search `collapsible Elmar 90` and `rigid Elmar 90`.

### Local listing label availability

Poor.

Current local dataset has:

- `0` explicit `collapsible` titles
- `0` explicit `rigid` titles

That means the theoretical split is stronger than the current operational label quality.

### Final decision

`still too early for explicit hold rows`

### One-line reason

The literature split is real, but the local listing language does not yet support stable assignment into `collapsible` vs `rigid` hold rows.

## Recommendation Summary

### Recommend explicit `hold` row now

1. `Leica Elmar-C 90mm f/4`

### Do not recommend explicit `hold` row yet

1. `Elmar (III) 1:4 / 90mm`
2. `90mm f/4 Elmar` collapsible
3. `90mm f/4 Elmar` rigid

## Should The Next Round Add A Hold Seed?

Yes, but very narrowly.

The next implementation round may safely add:

- `Leica Elmar-C 90mm f/4` -> `status = hold`

It should *not* yet add:

- `Elmar (III) 1:4 / 90mm`
- collapsible / rigid `90mm f/4 Elmar`

Those should remain in audit state until either:

- more local listings appear with explicit wording
- or admin review data proves those labels recur often enough to justify explicit hold rows

## Final Recommendation

`Elmar 90` is still not ready for `core`, but it is no longer a total no-go for explicit seeding.

The right round-2 move is:

- promote `Elmar-C` into a very narrow explicit `hold` row
- keep `Elmar (III)` and `collapsible / rigid` in taxonomy-audit state

That gives the seed system one genuinely useful foothold in the family without pretending the rest of the `Elmar 90` structure is more observable than it currently is.
