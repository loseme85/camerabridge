from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from trusted_metadata import (
    CuratedReferenceEntry,
    MetadataValidationError,
    OverridePatch,
    TrustedMetadataEntry,
    curated_reference_entry_from_dict,
    load_curated_reference,
    load_trusted_metadata,
    resolve_listing,
    trusted_metadata_entry_from_dict,
)
from final_resolution_pipeline import build_override_report


BASE_CLASSIFIER_OUTPUT = {
    "brand": "Leica",
    "mount": "Unknown",
    "category": "Body",
    "label": "Body",
    "model_raw": None,
    "model_canonical": None,
    "variant": [],
    "focal_length": None,
}


def test_trusted_exact_match_applies_with_audit() -> None:
    entry = TrustedMetadataEntry(
        id="trusted_exact",
        match={"source_url": "https://example.invalid/exact"},
        override=OverridePatch(
            fields={"mount": "M", "label": "M Body"},
            confidence=0.99,
            reason="Exact trusted listing.",
            evidence=["source_url exact match"],
        ),
    )
    resolved = resolve_listing(
        raw_item={"상품명": "MP3", "링크": "https://example.invalid/exact"},
        classifier_output=BASE_CLASSIFIER_OUTPUT,
        trusted_entries=[entry],
        curated_entries=[],
    )

    assert resolved["classifier_output"]["mount"] == "Unknown"
    assert resolved["final_output"]["mount"] == "M"
    assert resolved["override_applied"] is True
    assert resolved["audit_trail"][0]["changed_fields"]["mount"]["before"] == "Unknown"


def test_curated_reference_requires_narrow_title_guard() -> None:
    entry = CuratedReferenceEntry(
        id="curated_mp3_lhsa",
        canonical_name="Leica MP3",
        match={
            "required_title_patterns": ["\\bLEICA\\s+MP3\\b", "\\bLHSA\\b"],
            "classifier_must_equal": {"brand": "Leica", "category": "Body"},
        },
        patch=OverridePatch(
            fields={"mount": "M", "model_canonical": "MP3"},
            confidence=0.95,
            reason="Narrow curated model reference.",
            evidence=["title contains Leica MP3 and LHSA"],
        ),
    )

    resolved = resolve_listing(
        raw_item={"상품명": "[위탁] MP3 (Silver)"},
        classifier_output=BASE_CLASSIFIER_OUTPUT,
        trusted_entries=[],
        curated_entries=[entry],
    )

    assert resolved["override_applied"] is False
    assert resolved["final_output"]["mount"] == "Unknown"


def test_narrow_curated_reference_applies_with_audit() -> None:
    entry = CuratedReferenceEntry(
        id="curated_mp3_lhsa",
        canonical_name="Leica MP3",
        match={
            "required_title_patterns": ["\\bLEICA\\s+MP3\\b", "\\bLHSA\\b"],
            "classifier_must_equal": {"brand": "Leica", "category": "Body"},
        },
        patch=OverridePatch(
            fields={"mount": "M", "label": "M Body", "model_canonical": "MP3"},
            confidence=0.95,
            reason="Narrow curated model reference.",
            evidence=["title contains Leica MP3 and LHSA"],
        ),
    )

    resolved = resolve_listing(
        raw_item={"상품명": "LEICA MP3 LHSA Special Edition Silver Body"},
        classifier_output=BASE_CLASSIFIER_OUTPUT,
        trusted_entries=[],
        curated_entries=[entry],
    )

    assert resolved["override_applied"] is True
    assert resolved["override_source"] == "curated_reference"
    assert resolved["final_output"]["mount"] == "M"
    assert resolved["classifier_output"]["mount"] == "Unknown"


def test_metadata_json_loaders_validate_operational_files() -> None:
    assert len(load_trusted_metadata()) == 3
    assert len(load_curated_reference()) == 2


def test_malformed_trusted_metadata_rejected() -> None:
    bad_entry = {
        "id": "bad_trusted",
        "status": "active",
        "match": {"source_url": "https://example.invalid/item"},
        "override": {
            "fields": {"compatible_mounts": ["M"]},
            "confidence": 0.9,
            "reason": "This tries to override a non-final field.",
            "evidence": ["bad field"],
        },
    }

    try:
        trusted_metadata_entry_from_dict(bad_entry)
    except MetadataValidationError:
        return
    raise AssertionError("malformed trusted metadata should be rejected")


def test_broad_curated_reference_rejected() -> None:
    bad_entry = {
        "id": "bad_curated",
        "status": "active",
        "source": "curated_reference",
        "canonical_name": "Leica MP3",
        "match": {
            "required_title_patterns": ["MP3"],
            "classifier_must_equal": {"brand": "Leica", "category": "Body"},
        },
        "patch": {
            "fields": {"mount": "M"},
            "confidence": 0.9,
            "reason": "Too broad.",
            "evidence": ["MP3 substring only"],
        },
    }

    try:
        curated_reference_entry_from_dict(bad_entry)
    except MetadataValidationError:
        return
    raise AssertionError("broad curated reference should be rejected")


def test_override_report_counts_changed_fields() -> None:
    records = [
        {
            "record_index": 0,
            "raw_item": {"상품명": "LEICA MP3 LHSA", "site": "x", "링크": "u"},
            "classifier_output": BASE_CLASSIFIER_OUTPUT,
            "final_output": {**BASE_CLASSIFIER_OUTPUT, "mount": "M"},
            "override_applied": True,
            "override_source": "curated_reference",
            "override_source_id": "curated_mp3_lhsa",
            "override_reason": "Narrow curated model reference.",
            "audit_trail": [
                {
                    "changed_fields": {
                        "mount": {"before": "Unknown", "after": "M"},
                    }
                }
            ],
        }
    ]
    report = build_override_report(records)
    assert report["override_applied_count"] == 1
    assert report["curated_reference_applied_count"] == 1
    assert report["changed_fields"]["mount"] == 1


if __name__ == "__main__":
    test_trusted_exact_match_applies_with_audit()
    test_curated_reference_requires_narrow_title_guard()
    test_narrow_curated_reference_applies_with_audit()
    test_metadata_json_loaders_validate_operational_files()
    test_malformed_trusted_metadata_rejected()
    test_broad_curated_reference_rejected()
    test_override_report_counts_changed_fields()
    print("test_final_resolution: ok")
