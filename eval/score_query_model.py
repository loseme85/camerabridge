"""정답 세트로 검색 정확도 채점.

사용: python3 eval/score_query_model.py [API 주소] [--json 결과.json]
  기본 주소 https://camerabridge.vercel.app

점수(검색어마다 0~1):
  exact/parent  : 1위 맞음 0.5 + 상위 5개 중 맞는 비율 0.5
  ambiguous     : 되묻기(needs_disambiguation) 1.0, 아니면 상위 5개가 후보 모델인 비율
  nonexistent   : 되묻기·결과 없음 1.0, 1위가 다른 모델로 채워지면 0
"""
from __future__ import annotations

import concurrent.futures as cf
import json
import re
import sys
import urllib.parse
from pathlib import Path

import requests

GOLD = Path(__file__).resolve().parent / "query_model_gold_v1.json"
INDEX = Path(__file__).resolve().parents[1] / "data" / "derived" / "results_search_index_v1.json"


def models_in_data(models: dict) -> dict:
    """모델마다 수집 데이터에 맞는 매물이 몇 건 있는지 (없으면 '없음'을 보여 주는 게 정답)."""
    try:
        records = json.loads(INDEX.read_text(encoding="utf-8"))["records"]
    except Exception:
        return {}
    rows = [{"title": r["final_output"].get("title_raw") or r["raw_item"].get("상품명", ""), "final_output": r["final_output"]} for r in records]
    return {key: sum(listing_matches(row, spec) for row in rows) for key, spec in models.items()}


def listing_matches(result: dict, spec: dict) -> bool:
    final = result.get("final_output") or {}
    if spec["category"] and final.get("category") != spec["category"]:
        return False
    if spec["mount"] and final.get("mount") not in (spec["mount"], None, "Unknown") and final.get("mount") != spec["mount"]:
        return False
    title = str(result.get("title") or "")
    if not all(re.search(p, title, re.I) for p in spec["title_must"]):
        return False
    return not any(re.search(p, title, re.I) for p in spec["title_must_not"])


PARENTS: dict = {}


def expand(keys: list[str]) -> list[str]:
    """부모 엔티티는 자식 모델(손자까지)로 풀어서 채점한다."""
    out: list[str] = []
    for key in keys:
        out.extend(expand(PARENTS[key]) if key in PARENTS else [key])
    return out


def score_case(base: str, case: dict, models: dict, in_data: dict) -> dict:
    data = requests.get(f"{base}/api/search?limit=10&q={urllib.parse.quote(case['query'])}", timeout=90).json()
    results = data.get("results") or []
    asked = bool((data.get("ui_hints") or {}).get("needs_disambiguation"))
    specs = [models[key] for key in expand(case["expected_models"])]
    good = [any(listing_matches(r, s) for s in specs) for r in results[:5]]
    top1 = bool(good and good[0])
    share = sum(good) / 5 if results else 0.0
    intent = case["intent"]
    available = sum(in_data.get(key, 1) for key in expand(case["expected_models"]))
    if intent in ("exact", "parent") and in_data and available == 0:
        intent = "absent_in_data"  # 정답 모델 매물이 아예 없음 → 다른 모델로 채우지 않아야 정답
    if intent == "absent_in_data":
        score = 1.0 if (asked or not results) else 0.0
    elif intent in ("exact", "parent"):
        score = 0.5 * top1 + 0.5 * share
        if intent == "parent" and asked:
            score = max(score, 1.0)
    elif intent == "ambiguous":
        score = 1.0 if asked else share
    else:  # nonexistent
        score = 1.0 if (asked or not results) else 0.0
    return {
        "id": case["id"], "query": case["query"], "lang": case["lang"], "intent": intent, "score": round(score, 2),
        "top1_ok": top1, "top5_ok": sum(good), "asked": asked,
        "top3": [r.get("title", "")[:70] for r in results[:3]],
    }


def main() -> None:
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    base = (args[0] if args else "https://camerabridge.vercel.app").rstrip("/")
    gold = json.loads(GOLD.read_text(encoding="utf-8"))
    PARENTS.update(gold.get("parents") or {})
    in_data = models_in_data(gold["models"])
    with cf.ThreadPoolExecutor(6) as pool:
        rows = list(pool.map(lambda c: score_case(base, c, gold["models"], in_data), gold["cases"]))

    def avg(items):
        items = list(items)
        return round(100 * sum(r["score"] for r in items) / len(items), 1) if items else None

    summary = {
        "overall": avg(rows),
        "by_intent": {k: avg(r for r in rows if r["intent"] == k) for k in ("exact", "parent", "ambiguous", "nonexistent", "absent_in_data")},
        "by_lang": {k: avg(r for r in rows if r["lang"] == k) for k in ("en", "ko")},
        "top1_exact": round(100 * sum(r["top1_ok"] for r in rows if r["intent"] == "exact") / max(1, sum(r["intent"] == "exact" for r in rows)), 1),
        "cases": len(rows),
    }
    for r in sorted(rows, key=lambda x: x["score"]):
        if r["score"] < 1:
            print(f"{r['score']:.2f} {r['intent']:11} {r['query']:28} 1위: {r['top3'][0] if r['top3'] else '(없음)'}")
    summary["models_absent_in_data"] = sorted(k for k, v in in_data.items() if v == 0)
    print(json.dumps(summary, ensure_ascii=False, indent=1))
    if "--json" in sys.argv:
        out = sys.argv[sys.argv.index("--json") + 1]
        Path(out).write_text(json.dumps({"base": base, "summary": summary, "rows": rows}, ensure_ascii=False, indent=1), encoding="utf-8")


if __name__ == "__main__":
    main()
