"""엔티티 방식 채점: 검색어를 치고 Enter → 1순위 후보 모델이 정답인가.

exact      1순위 후보가 정답 모델                        → 1
parent     1순위가 정답 모델 중 하나이거나 그 부모          → 1
ambiguous  1순위가 후보들을 모두 포함하는 부모, 또는 상위 3개가 모두 후보 → 1 / 1순위가 후보 중 하나 → 0.5
nonexistent 후보가 하나도 안 뜸(아무 모델로 채우지 않음)  → 1
결과 매물은 선택한 엔티티 매물만 나오므로, 매물 정확도는 엔티티 연결 규칙(catalog)에 달려 있다.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from entity_catalog import suggest  # noqa: E402

GOLD = ROOT / "eval" / "query_model_gold_v1.json"
SUMMARY = ROOT / "data" / "derived" / "entity_summary_v1.json"


def covers(entity: dict, expected: set[str], by_id: dict) -> bool:
    if entity["id"] in expected:
        return True
    children = set(entity.get("children") or [])
    return bool(children) and expected <= children


def main() -> None:
    gold = json.loads(GOLD.read_text(encoding="utf-8"))
    entities = json.loads(SUMMARY.read_text(encoding="utf-8"))["entities"]
    by_id = {e["id"]: e for e in entities}
    rows = []
    for case in gold["cases"]:
        expected = set(case["expected_models"])
        top = suggest(case["query"], entities, limit=3)
        first = top[0] if top else None
        intent = case["intent"]
        if intent == "nonexistent":
            score = 1.0 if not top else 0.0
        elif not first:
            score = 0.0
        elif intent == "exact":
            score = 1.0 if first["id"] in expected else 0.0
        elif intent == "parent":
            score = 1.0 if (first["id"] in expected or covers(first, expected, by_id)) else 0.0
        else:
            if covers(first, expected, by_id) or (top and all(t["id"] in expected for t in top)):
                score = 1.0
            elif first["id"] in expected:
                score = 0.5
            else:
                score = 0.0
        rows.append({"query": case["query"], "lang": case["lang"], "intent": intent, "score": score,
                     "top": [t["name"] for t in top]})

    def avg(items):
        items = list(items)
        return round(100 * sum(r["score"] for r in items) / len(items), 1) if items else None

    for r in sorted(rows, key=lambda x: x["score"]):
        if r["score"] < 1:
            print(f"{r['score']:.1f} {r['intent']:11} {r['query']:28} → {r['top'][:3]}")
    print(json.dumps({"overall": avg(rows),
                      "by_intent": {k: avg(r for r in rows if r["intent"] == k) for k in ("exact", "parent", "ambiguous", "nonexistent")},
                      "by_lang": {k: avg(r for r in rows if r["lang"] == k) for k in ("en", "ko")},
                      "cases": len(rows)}, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
