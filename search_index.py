"""
search_index.py
===============
Compact search index build/load helpers.

Responsibilities:
  - Convert resolved listing records into a compact search-serving shape.
  - Keep only fields needed by query_resolver, search_service, and response UI.
  - Load compact index files for endpoint/search service use.

Non-responsibilities:
  - Do not classify listings.
  - Do not rank listings.
  - Do not apply trusted metadata overrides.
  - Do not import classifier_v2.py.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parent
SEARCH_INDEX_SCHEMA_VERSION = "search_index.v1"
DEFAULT_RESOLVED_PATH = PROJECT_ROOT / "data/derived/results_resolved_v2.json"
DEFAULT_SEARCH_INDEX_PATH = PROJECT_ROOT / "data/derived/results_search_index_v1.json"
_SEARCH_INDEX_CACHE: dict[str, dict[str, Any]] = {}

RAW_ITEM_FIELDS = [
    "site",
    "상품명",
    "링크",
    "system",
    "label",
    "세대",
]

FINAL_OUTPUT_FIELDS = [
    "brand",
    "mount",
    "system",
    "category",
    "label",
    "model_raw",
    "model_canonical",
    "variant",
    "focal_length",
    "sold_quality",
    "accessory_type",
    "compatible_mounts",
    "compatible_systems",
    "title_raw",
    "normalized_name",
    "source",
    "source_url",
    "image_url",
    "price_raw",
    "currency",
    "condition_raw",
    "crawl_time",
    "first_seen",
]


def normalize_title(value: Any) -> str:
    text = str(value or "").lower()
    text = text.replace("㎜", "mm").replace("ｍｍ", "mm")
    text = re.sub(r"[^a-z0-9가-힣]+", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def _as_list(value: Any) -> list[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


def _joined_tokens(values: list[Any]) -> list[str]:
    joined = " ".join(str(value) for value in values if value)
    normalized = normalize_title(joined)
    if not normalized:
        return []
    return sorted(set(normalized.split()))


def _extract_aperture_tokens(normalized_text: str) -> list[str]:
    tokens: set[str] = set()
    for match in re.finditer(r"\bf\s*(0|1|2|3|4|5|6|7|8|9)\s+(\d{1,2})\b", normalized_text):
        tokens.add(f"{match.group(1)}.{match.group(2)}")
    return sorted(tokens)


def parse_price_numeric(value: Any) -> float | None:
    text = str(value or "")
    if not text or any(keyword in text for keyword in ["문의", "ASK", "Ask", "상담"]):
        return None
    digits = re.findall(r"\d+(?:\.\d+)?", text.replace(",", ""))
    if not digits:
        return None
    try:
        return float(digits[0])
    except ValueError:
        return None


def _compact_dict(source: dict[str, Any], fields: list[str]) -> dict[str, Any]:
    return {
        field_name: source.get(field_name)
        for field_name in fields
        if field_name in source
    }


def build_search_fields(compact_final: dict[str, Any], raw_item: dict[str, Any]) -> dict[str, Any]:
    variant_values = [str(item) for item in _as_list(compact_final.get("variant")) if item]
    model_values = [
        compact_final.get("model_canonical"),
        compact_final.get("model_raw"),
        compact_final.get("label"),
    ]
    text_parts = [
        *model_values,
        compact_final.get("title_raw"),
        compact_final.get("normalized_name"),
        compact_final.get("normalized_title"),
        raw_item.get("상품명"),
        raw_item.get("label"),
        " ".join(variant_values),
    ]
    normalized_parts = []
    seen_parts = set()
    for part in text_parts:
        normalized_part = normalize_title(part)
        if normalized_part and normalized_part not in seen_parts:
            normalized_parts.append(normalized_part)
            seen_parts.add(normalized_part)
    searchable_text = " ".join(normalized_parts)
    model_text = normalize_title(" ".join(str(value) for value in model_values if value))

    mount_token = normalize_title(compact_final.get("mount"))
    system_token = normalize_title(compact_final.get("system") or raw_item.get("system"))
    focal_token = normalize_title(compact_final.get("focal_length"))
    variant_tokens = _joined_tokens(variant_values)

    return {
        "searchable_text": searchable_text,
        "model_text": model_text,
        "variant_tokens": variant_tokens,
        "aperture_tokens": _extract_aperture_tokens(searchable_text),
        "focal_token": focal_token,
        "mount_token": mount_token,
        "system_token": system_token,
    }


def compact_resolved_record(record: dict[str, Any]) -> dict[str, Any]:
    raw_item = record.get("raw_item") if isinstance(record.get("raw_item"), dict) else {}
    final_output = record.get("final_output") if isinstance(record.get("final_output"), dict) else {}
    compact_final = _compact_dict(final_output, FINAL_OUTPUT_FIELDS)
    title = compact_final.get("title_raw") or raw_item.get("상품명") or compact_final.get("normalized_name")
    source_url = compact_final.get("source_url") or raw_item.get("링크")

    compact_final["title_raw"] = title
    compact_final["source"] = compact_final.get("source") or raw_item.get("site")
    compact_final["source_url"] = source_url
    compact_final["parsed_price_numeric"] = parse_price_numeric(compact_final.get("price_raw"))
    compact_final["normalized_title"] = normalize_title(title)
    search_fields = build_search_fields(compact_final, raw_item)

    return {
        "search_id": source_url or f"record:{record.get('record_index')}",
        "record_index": record.get("record_index"),
        "raw_item": _compact_dict(raw_item, RAW_ITEM_FIELDS),
        "final_output": compact_final,
        "search_fields": search_fields,
        "override_applied": bool(record.get("override_applied")),
    }


def build_search_index(resolved_records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [compact_resolved_record(record) for record in resolved_records]


def load_resolved_records(path: str | Path = DEFAULT_RESOLVED_PATH) -> list[dict[str, Any]]:
    with open(path, encoding="utf-8") as f:
        payload = json.load(f)
    if not isinstance(payload, list):
        raise ValueError(f"{path} must contain a list of resolved records")
    return payload


def write_search_index(
    resolved_path: str | Path = DEFAULT_RESOLVED_PATH,
    output_path: str | Path = DEFAULT_SEARCH_INDEX_PATH,
) -> dict[str, Any]:
    resolved_records = load_resolved_records(resolved_path)
    records = build_search_index(resolved_records)
    payload = {
        "schema_version": SEARCH_INDEX_SCHEMA_VERSION,
        "generated_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "source_path": str(resolved_path),
        "record_count": len(records),
        "records": records,
    }

    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, separators=(",", ":"))
    return {
        "schema_version": SEARCH_INDEX_SCHEMA_VERSION,
        "source_path": str(resolved_path),
        "output_path": str(output),
        "record_count": len(records),
    }


def _cache_key(path: str | Path) -> str:
    return str(Path(path).resolve())


def clear_search_index_cache(path: str | Path | None = None) -> None:
    """Clear cached compact index records for tests, demos, and local rebuilds."""
    if path is None:
        _SEARCH_INDEX_CACHE.clear()
        return
    _SEARCH_INDEX_CACHE.pop(_cache_key(path), None)


def search_index_cache_info(path: str | Path = DEFAULT_SEARCH_INDEX_PATH) -> dict[str, Any]:
    """Return lightweight cache diagnostics without exposing record payloads."""
    entry = _SEARCH_INDEX_CACHE.get(_cache_key(path))
    if not entry:
        return {"cached": False, "record_count": 0}
    return {
        "cached": True,
        "record_count": len(entry["records"]),
        "mtime_ns": entry["mtime_ns"],
        "size": entry["size"],
    }


def load_search_index(
    path: str | Path = DEFAULT_SEARCH_INDEX_PATH,
    use_cache: bool = True,
) -> list[dict[str, Any]]:
    index_path = Path(path)
    stat = index_path.stat()
    cache_key = _cache_key(index_path)
    cached = _SEARCH_INDEX_CACHE.get(cache_key) if use_cache else None
    if (
        cached
        and cached["mtime_ns"] == stat.st_mtime_ns
        and cached["size"] == stat.st_size
    ):
        return cached["records"]

    with index_path.open(encoding="utf-8") as f:
        payload = json.load(f)
    if isinstance(payload, list):
        records = payload
    elif isinstance(payload, dict) and isinstance(payload.get("records"), list):
        records = payload["records"]
    else:
        raise ValueError(f"{path} must contain a search index object or record list")

    if use_cache:
        _SEARCH_INDEX_CACHE[cache_key] = {
            "mtime_ns": stat.st_mtime_ns,
            "size": stat.st_size,
            "records": records,
        }
    return records


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build compact search index from resolved records.")
    parser.add_argument("--resolved", default=str(DEFAULT_RESOLVED_PATH))
    parser.add_argument("--output", default=str(DEFAULT_SEARCH_INDEX_PATH))
    return parser.parse_args()


def main() -> None:
    args = _parse_args()
    result = write_search_index(args.resolved, args.output)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
