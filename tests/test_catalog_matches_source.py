"""카탈로그 JSON은 코드(catalog/*.py)에서 만든 결과와 같아야 한다 — 원본은 코드 하나 (2026-11-23 분류 설계 ⑤).

JSON만 직접 고치면 다음에 build_entity_catalog.py를 돌릴 때 그 고침이 사라진다(2026-11-14 액세서리 모델 43개가 그렇게 JSON에만 있었음).
이 시험이 실패하면: 고치려는 것을 catalog/*.py에 넣고 `python3 catalog/build_entity_catalog.py`로 JSON을 다시 만든다.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "catalog"))


def test_catalog_json_is_built_from_source() -> None:
    import build_entity_catalog

    built = json.loads(json.dumps(build_entity_catalog.build(), ensure_ascii=False))
    stored = json.loads((ROOT / "data" / "config" / "entity_catalog_v1.json").read_text(encoding="utf-8"))
    built.pop("updated_at", None)
    stored.pop("updated_at", None)
    built_ids = {e["id"] for e in built["entities"]}
    stored_ids = {e["id"] for e in stored["entities"]}
    assert built_ids == stored_ids, f"코드에만 {sorted(built_ids - stored_ids)[:5]} · JSON에만 {sorted(stored_ids - built_ids)[:5]}"
    by_id = {e["id"]: e for e in stored["entities"]}
    diff = [e["id"] for e in built["entities"] if e != by_id[e["id"]]]
    assert not diff, f"코드와 다른 JSON 항목 {len(diff)}개: {diff[:5]}"
