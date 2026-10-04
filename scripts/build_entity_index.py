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

from condition_grade import grade_of  # noqa: E402
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


# 등급별 가격 비율 (B = 1). 데이터가 모자라면 이 기본값 (2026-10 수집분으로 계산한 등급표 초안)
DEFAULT_FACTORS = {
    "Body": {"N": 1.18, "S": 1.05, "A": 1.0, "B": 1.0, "C": 0.94, "D": 0.73},
    "Lens": {"N": 1.25, "S": 1.08, "A": 1.06, "B": 1.0, "C": 0.93, "D": 0.78},
}


def _grade_factors(stats: dict, entities: dict) -> dict:
    """모든 모델을 합쳐 등급별 가격 비율: 모델마다 (그 등급 중앙값 / B 중앙값), 그 비율들의 중앙값."""
    out = {}
    for kind, default in DEFAULT_FACTORS.items():
        ratios: dict[str, list[float]] = {}
        for eid, s in stats.items():
            if entities[eid].get("kind") != kind or entities[eid].get("children"):
                continue
            by: dict[str, list[float]] = {}
            for grade, krw, _ in s["graded"]:
                by.setdefault(grade, []).append(krw)
            if len(by.get("B", [])) < 2:
                continue
            base = statistics.median(by["B"])
            for grade, prices in by.items():
                if grade != "B" and len(prices) >= 2:
                    ratios.setdefault(grade, []).append(statistics.median(prices) / base)
        factors = dict(default)
        for grade, rs in ratios.items():
            if len(rs) >= 5:  # 모델 5개 이상에서 나온 비율만 믿음
                factors[grade] = round(min(1.6, max(0.4, statistics.median(rs))), 3)
        out[kind] = factors
    return out


def _b_grade_price(graded: list, factors: dict) -> dict:
    """매물마다 B급 기준가로 환산(가격 / 등급 비율) → 중앙값. 판매 완료 3건 이상이면 판매 완료만, 아니면 판매 중까지."""
    sold = [krw / factors.get(g, 1.0) for g, krw, kind in graded if kind == "sold"]
    pool, basis = (sold, "sold") if len(sold) >= 3 else ([krw / factors.get(g, 1.0) for g, krw, _ in graded], "asking")
    if len(pool) < 3:
        return {}
    return {"b_price_krw": round(statistics.median(pool)), "b_price_n": len(pool), "b_price_basis": basis}


def main() -> None:
    payload = json.loads(INDEX.read_text(encoding="utf-8"))
    records = payload["records"]
    annotate_records(records)
    INDEX.write_text(json.dumps(payload, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")

    catalog = load_catalog()
    to_krw = _krw_rates()
    stats: dict[str, dict] = {eid: {"total": 0, "active": 0, "active_prices": [], "sold_prices": [], "graded": []}
                              for eid in catalog["entities"]}
    for record in records:
        final = record.get("final_output") or {}
        price = final.get("parsed_price_numeric")
        rate = to_krw.get(str(final.get("currency") or "KRW").upper())
        krw = price * rate if price and rate else None
        active = final.get("sold_quality") == "asking"
        sold = str(final.get("sold_quality") or "").startswith("sold")
        grade, _ = grade_of(final.get("source"), final.get("condition_raw"), final.get("title_raw"))
        for eid in record.get("entity_ids") or []:
            s = stats[eid]
            s["total"] += 1
            if active:
                s["active"] += 1
                if krw:
                    s["active_prices"].append(krw)
            elif krw and sold:
                s["sold_prices"].append(krw)
            if krw and grade and grade != "X" and (active or sold):
                s["graded"].append((grade, krw, "sold" if sold else "asking"))
    factors = _grade_factors(stats, catalog["entities"])

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
            **_b_grade_price(s["graded"], factors.get(entity["kind"], factors["Lens"])),
        })
    SUMMARY.write_text(json.dumps({"schema_version": "entity_summary_v1",
                                   "generated_at": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
                                   "grade_factors": factors,
                                   "entities": entities}, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    linked = sum(1 for r in records if r.get("entity_ids"))
    print(f"✅ 엔티티 연결: 매물 {linked}/{len(records)}, 엔티티 {len(entities)}개 요약")


if __name__ == "__main__":
    main()
