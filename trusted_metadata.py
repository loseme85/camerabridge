"""
trusted_metadata.py
===================
Auditable final-resolution layer for human/trusted facts.

This module must stay outside classifier_v2.py.

Responsibilities:
  - Keep manual/trusted overrides separate from classifier output.
  - Apply exact listing-level metadata before narrowly-scoped curated references.
  - Preserve an audit trail showing which fields changed and why.

Non-responsibilities:
  - Do not infer brand/mount/category from product text.
  - Do not contain search aliases.
  - Do not import or modify classifier stages.
"""

from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass, field, asdict
import json
from pathlib import Path
import re
from typing import Any, Optional


OVERRIDABLE_FIELDS = {
    "brand",
    "mount",
    "category",
    "label",
    "model_raw",
    "model_canonical",
    "variant",
    "focal_length",
}

VALID_ENTRY_STATUSES = {"active", "inactive", "disabled"}
TRUSTED_MATCH_KEYS = {"listing_id", "source_url", "source", "normalized_title", "trusted_label"}
CURATED_MATCH_KEYS = {
    "trusted_label",
    "required_title_patterns",
    "classifier_must_equal",
    "raw_must_equal",
}


PROJECT_ROOT = Path(__file__).resolve().parent
DEFAULT_TRUSTED_METADATA_PATH = PROJECT_ROOT / "data/metadata/trusted_metadata.json"
DEFAULT_CURATED_REFERENCE_PATH = PROJECT_ROOT / "data/metadata/curated_reference.json"


class MetadataValidationError(ValueError):
    """Raised when trusted metadata is malformed or too broad to apply."""


def normalize_title(value: str) -> str:
    text = (value or "").strip().lower()
    text = re.sub(r"^\[[^\]]+\]\s*", "", text)
    text = re.sub(r"\s+", " ", text)
    return text


def _require_dict(value: Any, context: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise MetadataValidationError(f"{context} must be a dict")
    return value


def _require_nonempty_string(value: Any, context: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise MetadataValidationError(f"{context} must be a non-empty string")
    return value


def _validate_status(value: Any, context: str) -> None:
    if value is None:
        return
    if value not in VALID_ENTRY_STATUSES:
        raise MetadataValidationError(f"{context}.status must be one of {sorted(VALID_ENTRY_STATUSES)}")


def _validate_override_patch_dict(data: dict[str, Any], context: str) -> None:
    _require_dict(data, context)

    fields = _require_dict(data.get("fields"), f"{context}.fields")
    if not fields:
        raise MetadataValidationError(f"{context}.fields must not be empty")

    unknown_fields = sorted(set(fields) - OVERRIDABLE_FIELDS)
    if unknown_fields:
        raise MetadataValidationError(
            f"{context}.fields contains non-overridable fields: {unknown_fields}"
        )

    confidence = data.get("confidence")
    if not isinstance(confidence, (int, float)) or not 0 <= float(confidence) <= 1:
        raise MetadataValidationError(f"{context}.confidence must be a number between 0 and 1")

    _require_nonempty_string(data.get("reason"), f"{context}.reason")

    evidence = data.get("evidence")
    if not isinstance(evidence, list) or not evidence:
        raise MetadataValidationError(f"{context}.evidence must be a non-empty list")
    if not all(isinstance(item, str) and item.strip() for item in evidence):
        raise MetadataValidationError(f"{context}.evidence must contain non-empty strings")


def _validate_trusted_match(match: dict[str, Any], context: str) -> None:
    _require_dict(match, context)
    unknown_keys = sorted(set(match) - TRUSTED_MATCH_KEYS)
    if unknown_keys:
        raise MetadataValidationError(f"{context} contains unsupported keys: {unknown_keys}")

    for key, value in match.items():
        _require_nonempty_string(value, f"{context}.{key}")

    has_listing_exact = bool(match.get("listing_id"))
    has_url_exact = bool(match.get("source_url"))
    has_source_title_exact = bool(match.get("source") and match.get("normalized_title"))
    has_trusted_label_with_source = bool(match.get("source") and match.get("trusted_label"))

    if not any([
        has_listing_exact,
        has_url_exact,
        has_source_title_exact,
        has_trusted_label_with_source,
    ]):
        raise MetadataValidationError(
            f"{context} needs listing_id, source_url, source+normalized_title, "
            "or source+trusted_label exact guards"
        )


def _validate_regex(pattern: Any, context: str) -> None:
    _require_nonempty_string(pattern, context)
    try:
        re.compile(pattern)
    except re.error as exc:
        raise MetadataValidationError(f"{context} is not a valid regex: {exc}") from exc


def _validate_curated_match(match: dict[str, Any], context: str) -> None:
    _require_dict(match, context)
    unknown_keys = sorted(set(match) - CURATED_MATCH_KEYS)
    if unknown_keys:
        raise MetadataValidationError(f"{context} contains unsupported keys: {unknown_keys}")

    patterns = match.get("required_title_patterns") or []
    trusted_label = match.get("trusted_label")
    classifier_must_equal = match.get("classifier_must_equal") or {}
    raw_must_equal = match.get("raw_must_equal") or {}

    if trusted_label is not None:
        _require_nonempty_string(trusted_label, f"{context}.trusted_label")

    if patterns:
        if not isinstance(patterns, list):
            raise MetadataValidationError(f"{context}.required_title_patterns must be a list")
        for index, pattern in enumerate(patterns):
            _validate_regex(pattern, f"{context}.required_title_patterns[{index}]")

    if classifier_must_equal:
        _require_dict(classifier_must_equal, f"{context}.classifier_must_equal")
    if raw_must_equal:
        _require_dict(raw_must_equal, f"{context}.raw_must_equal")

    has_narrow_title_guard = bool(trusted_label) or len(patterns) >= 2
    has_supporting_guard = bool(trusted_label or classifier_must_equal or raw_must_equal)

    if not has_narrow_title_guard:
        raise MetadataValidationError(
            f"{context} requires trusted_label or at least two title patterns"
        )
    if not has_supporting_guard:
        raise MetadataValidationError(
            f"{context} requires classifier_must_equal, raw_must_equal, or trusted_label"
        )


def _validate_trusted_metadata_dict(data: dict[str, Any], context: str) -> None:
    _require_dict(data, context)
    _require_nonempty_string(data.get("id"), f"{context}.id")
    _validate_status(data.get("status"), context)
    _validate_trusted_match(_require_dict(data.get("match"), f"{context}.match"), f"{context}.match")
    _validate_override_patch_dict(_require_dict(data.get("override"), f"{context}.override"), f"{context}.override")


def _validate_curated_reference_dict(data: dict[str, Any], context: str) -> None:
    _require_dict(data, context)
    _require_nonempty_string(data.get("id"), f"{context}.id")
    _require_nonempty_string(data.get("canonical_name"), f"{context}.canonical_name")
    _validate_status(data.get("status"), context)
    _validate_curated_match(_require_dict(data.get("match"), f"{context}.match"), f"{context}.match")
    _validate_override_patch_dict(_require_dict(data.get("patch"), f"{context}.patch"), f"{context}.patch")


@dataclass
class OverridePatch:
    fields: dict[str, Any]
    confidence: float
    reason: str
    evidence: list[str] = field(default_factory=list)
    updated_at: Optional[str] = None
    updated_by: Optional[str] = None

    def safe_fields(self) -> dict[str, Any]:
        return {
            key: value
            for key, value in self.fields.items()
            if key in OVERRIDABLE_FIELDS
        }


@dataclass
class TrustedMetadataEntry:
    id: str
    match: dict[str, Any]
    override: OverridePatch
    source: str = "trusted_metadata"
    status: str = "active"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class CuratedReferenceEntry:
    id: str
    canonical_name: str
    match: dict[str, Any]
    patch: OverridePatch
    source: str = "curated_reference"
    status: str = "active"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _override_patch_from_dict(data: dict[str, Any]) -> OverridePatch:
    fields = data.get("fields") or {}
    if not isinstance(fields, dict):
        raise ValueError("override fields must be a dict")

    return OverridePatch(
        fields=fields,
        confidence=float(data.get("confidence", 0.0)),
        reason=str(data.get("reason") or ""),
        evidence=list(data.get("evidence") or []),
        updated_at=data.get("updated_at"),
        updated_by=data.get("updated_by"),
    )


def trusted_metadata_entry_from_dict(data: dict[str, Any]) -> TrustedMetadataEntry:
    _validate_trusted_metadata_dict(data, "trusted_metadata_entry")
    return TrustedMetadataEntry(
        id=str(data["id"]),
        status=str(data.get("status") or "active"),
        source=str(data.get("source") or "trusted_metadata"),
        match=dict(data.get("match") or {}),
        override=_override_patch_from_dict(dict(data.get("override") or {})),
    )


def curated_reference_entry_from_dict(data: dict[str, Any]) -> CuratedReferenceEntry:
    _validate_curated_reference_dict(data, "curated_reference_entry")
    return CuratedReferenceEntry(
        id=str(data["id"]),
        status=str(data.get("status") or "active"),
        source=str(data.get("source") or "curated_reference"),
        canonical_name=str(data.get("canonical_name") or ""),
        match=dict(data.get("match") or {}),
        patch=_override_patch_from_dict(dict(data.get("patch") or {})),
    )


def load_trusted_metadata(path: str | Path = DEFAULT_TRUSTED_METADATA_PATH) -> list[TrustedMetadataEntry]:
    with open(path, encoding="utf-8") as f:
        payload = json.load(f)
    if not isinstance(payload, list):
        raise ValueError("trusted metadata file must contain a list")
    entries = []
    for index, item in enumerate(payload):
        try:
            entries.append(trusted_metadata_entry_from_dict(item))
        except MetadataValidationError as exc:
            raise MetadataValidationError(f"{path}[{index}]: {exc}") from exc
    return entries


def load_curated_reference(path: str | Path = DEFAULT_CURATED_REFERENCE_PATH) -> list[CuratedReferenceEntry]:
    with open(path, encoding="utf-8") as f:
        payload = json.load(f)
    if not isinstance(payload, list):
        raise ValueError("curated reference file must contain a list")
    entries = []
    for index, item in enumerate(payload):
        try:
            entries.append(curated_reference_entry_from_dict(item))
        except MetadataValidationError as exc:
            raise MetadataValidationError(f"{path}[{index}]: {exc}") from exc
    return entries


def resolve_listing_with_metadata_files(
    raw_item: dict[str, Any],
    classifier_output: dict[str, Any],
    trusted_path: str | Path = DEFAULT_TRUSTED_METADATA_PATH,
    curated_path: str | Path = DEFAULT_CURATED_REFERENCE_PATH,
) -> dict[str, Any]:
    return resolve_listing(
        raw_item=raw_item,
        classifier_output=classifier_output,
        trusted_entries=load_trusted_metadata(trusted_path),
        curated_entries=load_curated_reference(curated_path),
    )


def _raw_value(raw_item: dict[str, Any], key: str) -> str:
    aliases = {
        "source": "site",
        "source_url": "링크",
        "title": "상품명",
        "label": "label",
        "listing_id": "listing_id",
    }
    raw_key = aliases.get(key, key)
    return str(raw_item.get(raw_key) or "")


def _matches_exact_listing(raw_item: dict[str, Any], match: dict[str, Any]) -> bool:
    if "listing_id" in match:
        if _raw_value(raw_item, "listing_id") != str(match["listing_id"]):
            return False

    if "source_url" in match:
        if _raw_value(raw_item, "source_url") != str(match["source_url"]):
            return False

    if "source" in match:
        if _raw_value(raw_item, "source") != str(match["source"]):
            return False

    if "normalized_title" in match:
        if normalize_title(_raw_value(raw_item, "title")) != normalize_title(str(match["normalized_title"])):
            return False

    if "trusted_label" in match:
        if _raw_value(raw_item, "label") != str(match["trusted_label"]):
            return False

    return True


def find_trusted_metadata(
    raw_item: dict[str, Any],
    entries: list[TrustedMetadataEntry],
) -> Optional[TrustedMetadataEntry]:
    for entry in entries:
        if entry.status != "active":
            continue
        if _matches_exact_listing(raw_item, entry.match):
            return entry
    return None


def _matches_curated_reference(
    raw_item: dict[str, Any],
    classifier_output: dict[str, Any],
    match: dict[str, Any],
) -> bool:
    """
    Curated references are model-level facts, so they need stronger guards
    than listing-level trusted metadata. Prefer exact trusted labels or exact
    title patterns plus already-compatible classifier evidence.
    """
    if "trusted_label" in match:
        if _raw_value(raw_item, "label") != str(match["trusted_label"]):
            return False

    for pattern in match.get("required_title_patterns", []):
        if not re.search(pattern, _raw_value(raw_item, "title"), flags=re.IGNORECASE):
            return False

    for field_name, expected in match.get("classifier_must_equal", {}).items():
        if classifier_output.get(field_name) != expected:
            return False

    for field_name, expected in match.get("raw_must_equal", {}).items():
        if _raw_value(raw_item, field_name) != str(expected):
            return False

    return bool(
        match.get("trusted_label")
        or match.get("required_title_patterns")
    )


def find_curated_reference(
    raw_item: dict[str, Any],
    classifier_output: dict[str, Any],
    entries: list[CuratedReferenceEntry],
) -> Optional[CuratedReferenceEntry]:
    for entry in entries:
        if entry.status != "active":
            continue
        if _matches_curated_reference(raw_item, classifier_output, entry.match):
            return entry
    return None


def _apply_patch(
    final_output: dict[str, Any],
    patch: OverridePatch,
    source: str,
    source_id: str,
) -> dict[str, Any]:
    changed_fields = {}
    for field_name, value in patch.safe_fields().items():
        before = final_output.get(field_name)
        if before != value:
            final_output[field_name] = value
            changed_fields[field_name] = {"before": before, "after": value}

    return {
        "source": source,
        "source_id": source_id,
        "reason": patch.reason,
        "confidence": patch.confidence,
        "evidence": patch.evidence,
        "updated_at": patch.updated_at,
        "updated_by": patch.updated_by,
        "changed_fields": changed_fields,
    }


def resolve_listing(
    raw_item: dict[str, Any],
    classifier_output: dict[str, Any],
    trusted_entries: Optional[list[TrustedMetadataEntry]] = None,
    curated_entries: Optional[list[CuratedReferenceEntry]] = None,
) -> dict[str, Any]:
    """
    Return classifier output and final resolved output side by side.

    Resolution order:
      1. Keep classifier output unchanged.
      2. Apply exact trusted metadata if matched.
      3. Else apply curated reference only under narrow match conditions.
      4. Record audit fields for every change.
    """
    trusted_entries = trusted_entries or []
    curated_entries = curated_entries or []

    classifier_snapshot = deepcopy(classifier_output)
    final_output = deepcopy(classifier_output)
    audit_trail = []

    trusted_match = find_trusted_metadata(raw_item, trusted_entries)
    curated_match = None

    if trusted_match:
        audit_trail.append(
            _apply_patch(
                final_output,
                trusted_match.override,
                trusted_match.source,
                trusted_match.id,
            )
        )
    else:
        curated_match = find_curated_reference(raw_item, classifier_output, curated_entries)
        if curated_match:
            audit_trail.append(
                _apply_patch(
                    final_output,
                    curated_match.patch,
                    curated_match.source,
                    curated_match.id,
                )
            )

    override_applied = any(item["changed_fields"] for item in audit_trail)

    return {
        "classifier_output": classifier_snapshot,
        "final_output": final_output,
        "override_applied": override_applied,
        "override_source": audit_trail[0]["source"] if override_applied else None,
        "override_source_id": audit_trail[0]["source_id"] if override_applied else None,
        "override_reason": audit_trail[0]["reason"] if override_applied else None,
        "audit_trail": audit_trail,
    }
