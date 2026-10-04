"""검색 색인의 매물마다 엔티티 ID를 붙이고, 엔티티 요약(검색창 후보용)을 만든다.

입력·출력: data/derived/results_search_index_v1.json (records[].entity_ids 추가)
요약:      data/derived/entity_summary_v1.json
자동 수집 워크플로에서 final_resolution_pipeline.py 다음에 실행한다.
"""
from __future__ import annotations

import datetime as dt
import json
import statistics
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from entity_catalog import annotate_records, load_catalog  # noqa: E402

INDEX = ROOT / "data" / "derived" / "results_search_index_v1.json"
SUMMARY = ROOT / "data" / "derived" / "entity_summary_v1.json"
FX = ROOT / "data" / "fx_rates.json"


def _krw_rates() -> dict[str, float]:
    try:
        rates = json.loads(FX.read_text(encoding="utf-8"))["rates"]
        krw = rates["KRW"]
        return {code: krw / value for code, value in rates.items()}
    except Exception:
        return {"KRW": 1, "JPY": 9, "USD": 1350, "GBP": 1780, "EUR": 1500}


def main() -> None:
    payload = json.loads(INDEX.read_text(encoding="utf-8"))
    records = payload["records"]
    annotate_records(records)
    INDEX.write_text(json.dumps(payload, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")

    catalog = load_catalog()
    to_krw = _krw_rates()
    stats: dict[str, dict] = {eid: {"total": 0, "active": 0, "active_prices": [], "sold_prices": []} for eid in catalog["entities"]}
    for record in records:
        final = record.get("final_output") or {}
        price = final.get("parsed_price_numeric")
        rate = to_krw.get(str(final.get("currency") or "KRW").upper())
        krw = price * rate if price and rate else None
        active = final.get("sold_quality") == "asking"
        for eid in record.get("entity_ids") or []:
            s = stats[eid]
            s["total"] += 1
            if active:
                s["active"] += 1
                if krw:
                    s["active_prices"].append(krw)
            elif krw and str(final.get("sold_quality") or "").startswith("sold"):
                s["sold_prices"].append(krw)

    entities = []
    for eid, entity in catalog["entities"].items():
        s = stats[eid]
        ap, sp = sorted(s["active_prices"]), sorted(s["sold_prices"])
        entities.append({
            "id": eid, "name": entity["name"], "name_ko": entity.get("name_ko"), "kind": entity["kind"],
            "mount": entity.get("mount"), "parent": entity.get("parent"), "children": entity.get("children") or [],
            "aliases": entity["aliases"], "listing_count": s["total"], "active_count": s["active"],
            "active_price_krw": [round(ap[0]), round(ap[-1])] if ap else None,
            "sold_median_krw": round(statistics.median(sp)) if len(sp) >= 3 else None,
            "sold_price_count": len(sp),
        })
    SUMMARY.write_text(json.dumps({"schema_version": "entity_summary_v1",
                                   "generated_at": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
                                   "entities": entities}, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    linked = sum(1 for r in records if r.get("entity_ids"))
    print(f"✅ 엔티티 연결: 매물 {linked}/{len(records)}, 엔티티 {len(entities)}개 요약")


if __name__ == "__main__":
    main()
