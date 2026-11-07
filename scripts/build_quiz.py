"""라이카 레벨 테스트 문제 은행: data/derived/quiz_bank.json

첫 화면 'How well do you know Leica?' (2026-11-07 사장님: 라이카를 잘 아는 사람만 풀 수 있는 문제로 레벨을 매겨 줌).
문제를 사람이 지어내면 틀릴 수 있어서, 출처를 확인해 둔 데이터와 실제 판매 기록에서만 만든다.

  code_word  옛 라이트 코드 이름(SOOIC 등) → 모델          catalog/codes.py CODE_WORDS (lens-db·딜러 제목)   어려움 3
  order_no   라이카 주문 번호(11873 등) → 모델             catalog/codes.py CODES (공식 6비트 목록 등)       어려움 2~3
  feature    노출계·TTL·28mm 프레임라인·기계식 셔터         catalog/features.py (공식 사양)                   어려움 2
  variant    'Double Stroke'·'Everest '82'·'with eyes'는 어느 모델의 변형?   catalog 변형·기념판 (부모 모델)    어려움 2~3
             같은 이름이 여러 모델에 있는 변형(블랙페인트·올리브·50 Jahre 등)은 정답이 둘이 되므로 뺌
  (2026-11-07 사장님: 가격 문제 말고 매니아여야 아는 것 — 가격·시세 비교 문제는 뺌)

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

    # 4. 변형·기념판 → 바탕 모델 (바디는 바디끼리, 렌즈는 렌즈끼리)
    def label_of(e: dict) -> str:
        pn = name(e["parent"])
        n = e["name"]
        return (n[len(pn):] if n.startswith(pn) else n).strip(" -·")
    lens_words = re.compile(r"eyes|goggle|rigid|collapsible|dual range|steel rim|safari|titan|classic|lhsa|black paint|built-in hood|"
                            r"close focus|red|jahre|years|anniversary|edition|limited|8 elements|chrome|silver|military|olive", re.I)
    skip_label = re.compile(r"^\(?(standard|classic|generation not stated|\d{4} reissue)\)?$|not stated|differs by shop|\(all\)|^\(?typ\b|^[\d.]+$", re.I)

    def core(label: str) -> str:
        """중복 판단용 핵심 말: 'f/1.4 ASPH Safari' · 'Safari' → 'safari' (조리개·ASPH·연도·괄호 빼고)"""
        text = re.sub(r"\(.*?\)|f/\d+(?:\.\d+)?|\basph\b|\b\d{4}\b|['’‘\"]", " ", label.lower())
        return " ".join(text.split())

    def gives_away(label: str, parent: str) -> bool:
        """변형 이름에 바탕 모델 이름이 들어 있으면 답이 보임 (M2 Black Paint → M2)"""
        words = [w for w in re.split(r"[\s()·]+", name(parent).lower()) if len(w) >= 2 and w not in ("leica", "f/1.4", "f/2", "f/2.8")]
        return bool(re.search(r"\bleica\b", label, re.I)) or any(re.search(rf"(?<![\w-]){re.escape(w)}(?![\w-])", label.lower()) for w in words)

    def series_of(eid: str) -> str:
        """비슷한 오답: 'leica:body:m6' → body:m, 'leica:lens:summilux-m' → lens:summilux"""
        part = eid.split(":")[2]
        return eid.split(":")[1] + ":" + (re.match(r"[a-z]+", part).group(0) if re.match(r"[a-z]+", part) else part)
    variants: dict[tuple[str, str], set[str]] = {}
    for e in summary["entities"]:
        if not e.get("parent") or e.get("feature") or e["parent"] not in ents:
            continue
        label = label_of(e)
        kind = e["id"].split(":")[1]
        if not label or skip_label.search(label) or gives_away(label, e["parent"]) or not core(label):
            continue  # 기본형·'세대 모름'·바탕 모델 이름이 들어 있는 것은 문제로 안 냄
        if kind == "lens" and not lens_words.search(label):
            continue  # 렌즈는 세대 번호보다 매니아가 아는 별칭·한정판만
        variants.setdefault((kind, core(label)), set()).add(e["parent"])
    skip_ids = {e["id"] for e in summary["entities"]
                if not e.get("parent") or e.get("feature") or (e.get("parent") in ents and (skip_label.search(label_of(e) or "x") or gives_away(label_of(e), e["parent"])))}
    parents_by_kind: dict[str, list[str]] = {}
    for e in summary["entities"]:
        if e.get("children") and not e.get("feature"):
            parents_by_kind.setdefault(e["id"].split(":")[1], []).append(e["id"])
    for e in summary["entities"]:
        if not e.get("parent") or e["parent"] not in ents:
            continue
        kind = e["id"].split(":")[1]
        label = label_of(e)
        owners = variants.get((kind, core(label)))
        if not owners or len(owners) != 1 or e["id"] in skip_ids:
            continue  # 여러 모델에 같은 이름의 변형이 있으면 정답이 둘
        pool = parents_by_kind.get(kind, [])
        similar = [x for x in pool if series_of(x) == series_of(e["parent"]) and (kind == "lens" or x.startswith(B + "m") == e["parent"].startswith(B + "m"))]
        others = pick_others(e["parent"], similar) or pick_others(e["parent"], [x for x in pool if x.startswith(B + "m") == e["parent"].startswith(B + "m")]) or pick_others(e["parent"], pool)
        if others:
            add("variant", 3 if e.get("edition") or re.search(r"\d{4}", label) else 2, {"v": label, "kind": kind},
                name(e["parent"]), [name(x) for x in others], e["id"])

    kinds: dict[str, int] = {}
    for q in questions:
        kinds[q["kind"]] = kinds.get(q["kind"], 0) + 1
    OUT.write_text(json.dumps({"schema_version": "quiz_bank_v1", "generated_at": summary.get("generated_at"), "questions": questions},
                              ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    print(f"✅ 레벨 테스트 문제 {len(questions)}개 {kinds}")


if __name__ == "__main__":
    main()
