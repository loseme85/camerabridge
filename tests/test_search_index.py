from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from search_index import build_search_index, load_search_index, write_search_index
from search_service import search_records


RESOLVED_RECORD = {
    "record_index": 42,
    "raw_item": {
        "site": "test dealer",
        "상품명": "Leica M 35mm Summilux ASPH AA",
        "링크": "https://example.invalid/listing",
        "system": "M",
        "huge_unused_field": "x" * 1000,
    },
    "classifier_output": {
        "brand": "Leica",
        "mount": "M",
        "category": "Lens",
    },
    "final_output": {
        "brand": "Leica",
        "mount": "M",
        "category": "Lens",
        "label": "M Lens",
        "model_raw": "Summilux",
        "model_canonical": "Summilux-M",
        "variant": ["ASPH", "AA"],
        "focal_length": "35",
        "title_raw": "Leica M 35mm Summilux ASPH AA",
        "source": "test dealer",
        "source_url": "https://example.invalid/listing",
        "price_raw": "7,300,000원",
        "currency": "KRW",
        "condition_raw": "98%",
        "sold_quality": "asking",
        "normalized_description": "large text should not be copied",
        "risk_flags": ["debug-only"],
    },
    "override_applied": True,
    "audit_trail": [{"changed_fields": {"mount": {"before": "Unknown", "after": "M"}}}],
}


def test_build_search_index_keeps_only_serving_fields() -> None:
    records = build_search_index([RESOLVED_RECORD])
    compact = records[0]

    assert compact["record_index"] == 42
    assert compact["override_applied"] is True
    assert compact["search_id"] == "https://example.invalid/listing"
    assert "classifier_output" not in compact
    assert "audit_trail" not in compact
    assert "huge_unused_field" not in compact["raw_item"]
    assert "normalized_description" not in compact["final_output"]
    assert "risk_flags" not in compact["final_output"]
    assert compact["final_output"]["parsed_price_numeric"] == 7300000.0
    assert compact["final_output"]["normalized_title"] == "leica m 35mm summilux asph aa"


def test_search_records_accepts_compact_index_records() -> None:
    compact_records = build_search_index([RESOLVED_RECORD])
    response = search_records("35lux aa", compact_records, limit=1)

    assert response["result_count"] == 1
    result = response["results"][0]
    assert result["final_output"]["model_canonical"] == "Summilux-M"
    assert result["used_override"] is True
    assert "debug" not in result


def test_write_and_load_search_index_object() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        resolved_path = tmp_path / "resolved.json"
        output_path = tmp_path / "search_index.json"
        resolved_path.write_text(json.dumps([RESOLVED_RECORD], ensure_ascii=False), encoding="utf-8")

        result = write_search_index(resolved_path, output_path)
        loaded = load_search_index(output_path)

        assert result["record_count"] == 1
        assert loaded[0]["final_output"]["model_canonical"] == "Summilux-M"


if __name__ == "__main__":
    test_build_search_index_keeps_only_serving_fields()
    test_search_records_accepts_compact_index_records()
    test_write_and_load_search_index_object()
    print("test_search_index: ok")
