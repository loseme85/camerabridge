from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from search_index import (
    build_search_index,
    clear_search_index_cache,
    load_search_index,
    search_index_cache_info,
    write_search_index,
)
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
    assert compact["search_fields"]["schema_version"] == "search_fields.v1"
    assert "leica m 35mm summilux asph aa" in compact["search_fields"]["searchable_text"]
    assert compact["search_fields"]["focal_token"] == "35"
    assert compact["search_fields"]["mount_token"] == "m"
    assert compact["search_fields"]["system_token"] == "m"
    assert "summilux" in compact["search_fields"]["model_tokens"]
    assert "aa" in compact["search_fields"]["variant_tokens"]


def test_search_records_accepts_compact_index_records() -> None:
    compact_records = build_search_index([RESOLVED_RECORD])
    response = search_records("35lux aa", compact_records, limit=1)

    assert response["result_count"] == 1
    result = response["results"][0]
    assert result["final_output"]["model_canonical"] == "Summilux-M"
    assert result["used_override"] is True
    assert "debug" not in result
    assert response["candidate_narrowing"]["precomputed_field_record_count"] == 0


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


def test_load_search_index_reuses_module_cache_for_unchanged_file() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        resolved_path = tmp_path / "resolved.json"
        output_path = tmp_path / "search_index.json"
        resolved_path.write_text(json.dumps([RESOLVED_RECORD], ensure_ascii=False), encoding="utf-8")

        write_search_index(resolved_path, output_path)
        clear_search_index_cache(output_path)
        first = load_search_index(output_path)
        second = load_search_index(output_path)
        cache_info = search_index_cache_info(output_path)

        assert first is second
        assert cache_info["cached"] is True
        assert cache_info["record_count"] == 1


def test_load_search_index_reloads_when_file_changes() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        resolved_path = tmp_path / "resolved.json"
        output_path = tmp_path / "search_index.json"
        resolved_path.write_text(json.dumps([RESOLVED_RECORD], ensure_ascii=False), encoding="utf-8")

        write_search_index(resolved_path, output_path)
        clear_search_index_cache(output_path)
        first = load_search_index(output_path)

        updated_record = json.loads(json.dumps(RESOLVED_RECORD, ensure_ascii=False))
        updated_record["record_index"] = 43
        updated_record["final_output"]["model_canonical"] = "Summicron-M"
        updated_record["final_output"]["title_raw"] = "Leica M 50mm Summicron"
        resolved_path.write_text(json.dumps([RESOLVED_RECORD, updated_record], ensure_ascii=False), encoding="utf-8")
        write_search_index(resolved_path, output_path)
        second = load_search_index(output_path)

        assert len(first) == 1
        assert len(second) == 2
        assert second is not first
        assert second[1]["final_output"]["model_canonical"] == "Summicron-M"


def test_load_search_index_can_bypass_cache_for_timing_comparisons() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        resolved_path = tmp_path / "resolved.json"
        output_path = tmp_path / "search_index.json"
        resolved_path.write_text(json.dumps([RESOLVED_RECORD], ensure_ascii=False), encoding="utf-8")

        write_search_index(resolved_path, output_path)
        clear_search_index_cache(output_path)
        cached = load_search_index(output_path)
        uncached = load_search_index(output_path, use_cache=False)

        assert cached == uncached
        assert cached is not uncached
        assert search_index_cache_info(output_path)["cached"] is True


if __name__ == "__main__":
    test_build_search_index_keeps_only_serving_fields()
    test_search_records_accepts_compact_index_records()
    test_write_and_load_search_index_object()
    test_load_search_index_reuses_module_cache_for_unchanged_file()
    test_load_search_index_reloads_when_file_changes()
    test_load_search_index_can_bypass_cache_for_timing_comparisons()
    print("test_search_index: ok")
