"""라이카 레벨 테스트 문제 은행: data/derived/quiz_bank.json

첫 화면 'How well do you know Leica?' (2026-11-07 사장님: 라이카를 잘 아는 사람만 풀 수 있는 문제로 레벨을 매겨 줌).
문제를 사람이 지어내면 틀릴 수 있어서, 출처를 확인해 둔 데이터와 실제 판매 기록에서만 만든다.

  code_word  옛 라이트 코드 이름(SOOIC 등) → 모델          catalog/codes.py CODE_WORDS (lens-db·딜러 제목)   어려움 3
  order_no   라이카 주문 번호(11873 등) → 모델             catalog/codes.py CODES (공식 6비트 목록 등)       어려움 2~3
  feature    노출계·TTL·28mm 프레임라인·기계식 셔터         catalog/features.py (공식 사양)                   어려움 2
  compare    둘 중 B등급 시세가 더 높은 것                  entity_summary_v1.json b_price_krw (판매 기록)     어려움 2
  price      이 매물, 얼마에 팔렸을까? (보기 4개)           home_feed.json quiz (최근 팔린 실제 매물)          어려움 1~2

화면은 이 은행에서 종류별로 섞어 10문제를 낸다. 크롤마다 다시 만든다 (build_entity_index.py 다음).
"""
from __future__ import annotations

import json
import random
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from catalog import codes as catalog_codes  # noqa: E402

SUMMARY = ROOT / "data" / "derived" / "entity_summary_v1.json"
HOME_FEED = ROOT / "data" / "derived" / "home_feed.json"
OUT = ROOT / "data" / "derived" / "quiz_bank.json"
B = "leica:body:"

# 사양 문제: (문제 키, 정답 후보, 오답 후보) — 공식 사양 (catalog/features.py 머리말)
FEATURE_QUESTIONS = [
    ("no_meter", ["m3", "m2", "m4", "m4-2", "m4-p", "m-a"], ["m5", "cl-film", "m6:classic", "m7", "mp-film"]),
    ("has_meter", ["m5", "cl-film", "m6:classic", "m7", "mp-film"], ["m3", "m2", "m4", "m4-2", "m4-p", "m-a"]),
    ("ttl", ["m6:ttl", "m7"], ["m6:classic", "mp-film", "m4-p", "m-a", "m5"]),
    ("battery", ["m7"], ["m6:classic", "mp-film", "m4-p", "m-a", "m3", "m2"]),
    ("no_28", ["m3", "m2", "m4", "m4-2"], ["m4-p", "m6:classic", "m7", "mp-film", "m-a"]),
]


def family(eid: str) -> str:
    """'leica:lens:summilux-m:35:aa' → 'leica:lens:summilux-m' (같은 계열에서 오답을 골라 어렵게)"""
    return ":".join(eid.split(":")[:3])


def main() -> None:
    rng = random.Random(20261107)
    summary = json.loads(SUMMARY.read_text(encoding="utf-8"))
    ents = {e["id"]: e for e in summary["entities"]}
    name = lambda eid: ents[eid]["name"].replace(" (all)", "")  # noqa: E731
    questions: list[dict] = []

    def pick_others(correct: str, pool: list[str], n: int = 3) -> list[str] | None:
        others = [x for x in dict.fromkeys(pool) if x != correct and x in ents and name(x) != name(correct)]
        if len(others) < n:
            return None
        return rng.sample(others, n)

    def add(kind: str, level: int, vars_: dict, correct: str, others: list[str], entity: str | None, extra: dict | None = None) -> None:
        options = [correct] + others
        rng.shuffle(options)
        questions.append({"kind": kind, "level": level, "vars": vars_, "options": options, "answer": options.index(correct),
                          "entity": entity, **(extra or {})})

    # 1. 옛 코드 이름 (바디는 바디끼리, 렌즈는 렌즈끼리)
    words = {eid: ws for eid, ws in catalog_codes.CODE_WORDS.items() if eid in ents}
    for eid, ws in words.items():
        same_kind = [x for x in words if x.split(":")[1] == eid.split(":")[1]]
        others = pick_others(eid, same_kind)
        if others:
            add("code_word", 3, {"c": ws[0], "kind": eid.split(":")[1]}, name(eid), [name(x) for x in others], eid)

    # 2. 주문 번호: 한 모델에만 쓰인 번호, 오답은 같은 계열에서 (없으면 같은 종류)
    counts: dict[str, int] = {}
    for ns in catalog_codes.CODES.values():
        for n in ns:
            counts[n] = counts.get(n, 0) + 1
    with_codes = [eid for eid in catalog_codes.CODES if eid in ents]
    for eid in with_codes:
        number = next((n for n in catalog_codes.CODES[eid] if counts[n] == 1), None)
        if not number or ents[eid].get("children"):
            continue
        fam = [x for x in with_codes if family(x) == family(eid)]
        others = pick_others(eid, fam) or pick_others(eid, [x for x in with_codes if x.split(":")[1] == eid.split(":")[1]])
        if others:
            add("order_no", 3 if len(fam) > 3 else 2, {"c": number}, name(eid), [name(x) for x in others], eid)

    # 3. 사양
    for key, right, wrong in FEATURE_QUESTIONS:
        for r in right:
            if B + r not in ents:
                continue
            others = pick_others(B + r, [B + w for w in wrong])
            if others:
                add("feature", 2, {"f": key}, name(B + r), [name(x) for x in others], B + r)

    # 4. 둘 중 B등급 시세가 높은 것: 같은 계열, 20% 넘게 차이 나는 쌍
    priced = [e for e in summary["entities"] if e.get("b_price_krw") and not e.get("children") and not e.get("feature") and (e.get("b_price_n") or 0) >= 5]
    by_family: dict[str, list[dict]] = {}
    for e in priced:
        by_family.setdefault(family(e["id"]), []).append(e)
    for fam_items in by_family.values():
        rng.shuffle(fam_items)
        for a, b in zip(fam_items[::2], fam_items[1::2]):
            hi, lo = (a, b) if a["b_price_krw"] > b["b_price_krw"] else (b, a)
            if hi["b_price_krw"] >= lo["b_price_krw"] * 1.2:
                options = [name(hi["id"]), name(lo["id"])]
                rng.shuffle(options)
                pair = [hi, lo]
                rng.shuffle(pair)
                questions.append({"kind": "compare", "level": 2, "vars": {}, "options": [name(x["id"]) for x in pair],
                                  "answer": pair.index(hi), "entity": hi["id"], "krw": [x["b_price_krw"] for x in pair]})

    # 5. 팔린 가격 맞히기: 보기 4개 (정답 + 비율로 만든 오답), 1단계는 차이 크게, 2단계는 작게
    feed = json.loads(HOME_FEED.read_text(encoding="utf-8")) if HOME_FEED.exists() else {}
    for item in feed.get("quiz") or []:
        if item["entity"] not in ents:
            continue
        level = rng.choice([1, 2])
        ratios = rng.sample([0.5, 0.65, 1.5, 1.9] if level == 1 else [0.75, 0.85, 1.18, 1.35], 3)
        krws = [item["krw"]] + [round(item["krw"] * r, -4) for r in ratios]
        order = list(range(4))
        rng.shuffle(order)
        questions.append({"kind": "price", "level": level, "vars": {"title": item["title"], "grade": item.get("grade"), "source": item["source"],
                                                                   "sold_at": item["sold_at"]},
                          "image": item["image"], "options_krw": [krws[i] for i in order], "answer": order.index(0), "entity": item["entity"]})

    kinds: dict[str, int] = {}
    for q in questions:
        kinds[q["kind"]] = kinds.get(q["kind"], 0) + 1
    OUT.write_text(json.dumps({"schema_version": "quiz_bank_v1", "generated_at": summary.get("generated_at"), "questions": questions},
                              ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    print(f"✅ 레벨 테스트 문제 {len(questions)}개 {kinds}")


if __name__ == "__main__":
    main()
