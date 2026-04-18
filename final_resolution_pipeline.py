"""
Batch final-resolution pipeline.

This module connects classifier output to the trusted metadata layer without
changing classifier_v2.py. The classifier remains the pure inference engine;
trusted/manual facts are applied only after classification and are audited.
"""

from __future__ import annotations

import argparse
from collections import Counter
from copy import deepcopy
import datetime as dt
import json
from pathlib import Path
from typing import Any, Callable, Optional

from trusted_metadata import (
    DEFAULT_CURATED_REFERENCE_PATH,
    DEFAULT_TRUSTED_METADATA_PATH,
    PROJECT_ROOT,
    CuratedReferenceEntry,
    TrustedMetadataEntry,
    load_curated_reference,
    load_trusted_metadata,
    resolve_listing,
)


DEFAULT_INPUT_PATH = PROJECT_ROOT / "data/raw/results.json"
DEFAULT_DERIVED_DIR = PROJECT_ROOT / "data/derived"
DEFAULT_CLASSIFIED_OUTPUT_PATH = DEFAULT_DERIVED_DIR / "results_classified_v2.json"
DEFAULT_RESOLVED_OUTPUT_PATH = DEFAULT_DERIVED_DIR / "results_resolved_v2.json"
DEFAULT_OVERRIDE_REPORT_PATH = DEFAULT_DERIVED_DIR / "override_report.json"


ClassifierFn = Callable[[dict[str, Any]], dict[str, Any]]


def _load_items(path: str | Path) -> list[dict[str, Any]]:
    with open(path, encoding="utf-8") as f:
        payload = json.load(f)
    if not isinstance(payload, list):
        raise ValueError(f"{path} must contain a list of raw listing objects")
    return payload


def _write_json(path: str | Path, payload: Any) -> None:
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)


def _summary_fields(output: dict[str, Any]) -> dict[str, Any]:
    return {
        "brand": output.get("brand"),
        "mount": output.get("mount"),
        "category": output.get("category"),
        "label": output.get("label"),
        "model_canonical": output.get("model_canonical"),
        "variant": output.get("variant"),
        "focal_length": output.get("focal_length"),
    }


def classify_and_resolve_items(
    items: list[dict[str, Any]],
    classifier: Optional[ClassifierFn] = None,
    trusted_entries: Optional[list[TrustedMetadataEntry]] = None,
    curated_entries: Optional[list[CuratedReferenceEntry]] = None,
) -> list[dict[str, Any]]:
    """
    Produce records that preserve classifier output and resolved final output.

    `classifier` is injectable for tests. In normal execution it is imported
    lazily so importing this module does not run or modify classifier_v2.py.
    """
    if classifier is None:
        from classifier_v2 import classify_listing_v2

        classifier = classify_listing_v2

    if trusted_entries is None:
        trusted_entries = load_trusted_metadata()
    if curated_entries is None:
        curated_entries = load_curated_reference()

    resolved_records = []
    for index, raw_item in enumerate(items):
        classifier_output = classifier(raw_item)
        resolved = resolve_listing(
            raw_item=raw_item,
            classifier_output=classifier_output,
            trusted_entries=trusted_entries,
            curated_entries=curated_entries,
        )
        resolved_records.append(
            {
                "record_index": index,
                "raw_item": deepcopy(raw_item),
                "classifier_output": resolved["classifier_output"],
                "final_output": resolved["final_output"],
                "override_applied": resolved["override_applied"],
                "override_source": resolved["override_source"],
                "override_source_id": resolved["override_source_id"],
                "override_reason": resolved["override_reason"],
                "audit_trail": resolved["audit_trail"],
            }
        )
    return resolved_records


def build_override_report(
    resolved_records: list[dict[str, Any]],
    example_limit: int = 8,
) -> dict[str, Any]:
    source_counts = Counter()
    changed_field_counts = Counter()
    examples = []

    for record in resolved_records:
        if not record.get("override_applied"):
            continue

        source = record.get("override_source") or "unknown"
        source_counts[source] += 1

        changed_fields = {}
        for audit_item in record.get("audit_trail", []):
            for field_name, diff in audit_item.get("changed_fields", {}).items():
                changed_field_counts[field_name] += 1
                changed_fields[field_name] = diff

        if len(examples) < example_limit:
            raw_item = record.get("raw_item", {})
            examples.append(
                {
                    "record_index": record.get("record_index"),
                    "title_raw": raw_item.get("상품명"),
                    "source": raw_item.get("site"),
                    "source_url": raw_item.get("링크"),
                    "override_source": record.get("override_source"),
                    "override_source_id": record.get("override_source_id"),
                    "override_reason": record.get("override_reason"),
                    "changed_fields": changed_fields,
                    "classifier_output": _summary_fields(record.get("classifier_output", {})),
                    "final_output": _summary_fields(record.get("final_output", {})),
                }
            )

    override_applied_count = sum(source_counts.values())
    return {
        "generated_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "total_records": len(resolved_records),
        "override_applied_count": override_applied_count,
        "trusted_metadata_applied_count": source_counts.get("trusted_metadata", 0),
        "curated_reference_applied_count": source_counts.get("curated_reference", 0),
        "changed_fields": dict(sorted(changed_field_counts.items())),
        "examples": examples,
    }


def write_resolved_outputs(
    input_path: str | Path = DEFAULT_INPUT_PATH,
    classified_output_path: str | Path = DEFAULT_CLASSIFIED_OUTPUT_PATH,
    resolved_output_path: str | Path = DEFAULT_RESOLVED_OUTPUT_PATH,
    override_report_path: str | Path = DEFAULT_OVERRIDE_REPORT_PATH,
    trusted_path: str | Path = DEFAULT_TRUSTED_METADATA_PATH,
    curated_path: str | Path = DEFAULT_CURATED_REFERENCE_PATH,
    limit: Optional[int] = None,
) -> dict[str, Any]:
    items = _load_items(input_path)
    if limit is not None:
        items = items[:limit]

    trusted_entries = load_trusted_metadata(trusted_path)
    curated_entries = load_curated_reference(curated_path)
    resolved_records = classify_and_resolve_items(
        items,
        trusted_entries=trusted_entries,
        curated_entries=curated_entries,
    )
    classified_records = [record["classifier_output"] for record in resolved_records]
    report = build_override_report(resolved_records)

    _write_json(classified_output_path, classified_records)
    _write_json(resolved_output_path, resolved_records)
    _write_json(override_report_path, report)
    return {
        "classified_output_path": str(classified_output_path),
        "resolved_output_path": str(resolved_output_path),
        "override_report_path": str(override_report_path),
        "report": report,
    }


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate classified and resolved v2 outputs.")
    parser.add_argument("--input", default=str(DEFAULT_INPUT_PATH))
    parser.add_argument("--classified-output", default=str(DEFAULT_CLASSIFIED_OUTPUT_PATH))
    parser.add_argument("--resolved-output", default=str(DEFAULT_RESOLVED_OUTPUT_PATH))
    parser.add_argument("--override-report", default=str(DEFAULT_OVERRIDE_REPORT_PATH))
    parser.add_argument("--trusted-metadata", default=str(DEFAULT_TRUSTED_METADATA_PATH))
    parser.add_argument("--curated-reference", default=str(DEFAULT_CURATED_REFERENCE_PATH))
    parser.add_argument("--limit", type=int, default=None)
    return parser.parse_args()


def main() -> None:
    args = _parse_args()
    result = write_resolved_outputs(
        input_path=args.input,
        classified_output_path=args.classified_output,
        resolved_output_path=args.resolved_output,
        override_report_path=args.override_report,
        trusted_path=args.trusted_metadata,
        curated_path=args.curated_reference,
        limit=args.limit,
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
