"""자유 검색이 0건이면 검색창 후보 규칙으로 모델을 찾아 그 매물을 보여 준다 (2026-11-20 방문 현황 '결과 0건 검색어')."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from api.search import search_with_zero_result_fallback
from search_index import build_search_index

ALC_ID = "leica:body:m7:a-la-carte"


def _record(index: int, title: str, entity_ids: list[str]) -> dict:
    final = {
        "source": "A dealer",
        "source_url": f"https://example.invalid/{index}",
        "title_raw": title,
        "price_raw": "9,000,000원",
        "currency": "KRW",
        "brand": "Leica",
        "mount": "M",
        "category": "Body",
        "label": "M Body",
        "model_raw": "M7",
        "model_canonical": "M7",
        "variant": [],
        "sold_quality": "asking",
    }
    return {
        "record_index": index,
        "raw_item": {"site": "A dealer", "상품명": title, "링크": final["source_url"]},
        "classifier_output": {"brand": "Leica", "mount": "M", "category": "Body", "label": "M Body", "model_canonical": "M7"},
        "final_output": final,
        "override_applied": False,
        "audit_trail": [],
    }


def _records() -> list[dict]:
    rows = build_search_index([
        _record(1, "LEICA M7 アラカルト BlackPaint", [ALC_ID]),
        _record(2, "Leica M7 0.72 silver", ["leica:body:m7"]),
    ])
    rows[0]["entity_ids"] = [ALC_ID, "leica:body:m7"]
    rows[1]["entity_ids"] = ["leica:body:m7"]
    return rows


ENTITIES = [
    {"id": ALC_ID, "aliases": ["Leica M7 à la carte", "m7 a la carte"], "listing_count": 1, "active_count": 1},
    {"id": "leica:body:m7", "aliases": ["Leica M7", "m7"], "listing_count": 2, "active_count": 2},
]


def test_zero_result_query_falls_back_to_catalog_model() -> None:
    response = search_with_zero_result_fallback({"q": ["a la carte"], "limit": ["5"]}, records=_records(), entities=ENTITIES)
    assert response["result_count"] == 1
    assert response["zero_result_fallback"]["original_query"] == "a la carte"
    assert response["zero_result_fallback"]["entity"] == ALC_ID


def test_query_with_results_is_unchanged() -> None:
    response = search_with_zero_result_fallback({"q": ["m7"], "limit": ["5"]}, records=_records(), entities=ENTITIES)
    assert response["result_count"] >= 1
    assert "zero_result_fallback" not in response


def test_unknown_query_stays_empty() -> None:
    response = search_with_zero_result_fallback({"q": ["hasselblad"], "limit": ["5"]}, records=_records(), entities=ENTITIES)
    assert response["result_count"] == 0
    assert "zero_result_fallback" not in response
