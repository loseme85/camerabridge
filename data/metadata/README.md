# Trusted Metadata Layer

This directory is for auditable human or trusted-source facts that must stay
outside `classifier_v2.py`.

Allowed match styles:

- `listing_id` exact match
- `source_url` exact match
- `source` plus `normalized_title` exact match
- trusted source metadata with explicit evidence
- curated references only when title/evidence guards are narrow and the
  classifier result already supports the same broad identity

Forbidden match styles:

- broad substring overrides such as `MP3` alone
- search aliases or user-query slang
- compatibility hints that change category
- silent overwrites without `reason`, `evidence`, and `changed_fields`

Resolution order:

1. Generate classifier output.
2. Apply `trusted_metadata.json` exact listing metadata, if matched.
3. Otherwise apply `curated_reference.json` only under narrow guards.
4. Return classifier output and final output side by side with an audit trail.
