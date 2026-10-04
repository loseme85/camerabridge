"""엔티티 점검: 크롤 뒤 '빠진 모델' 후보를 찾는다 (시세가 다른 버전이 비슷한 모델에 흡수된 경우).

1) 겹침: 한 매물이 부모·자식 관계가 아닌 두 모델에 동시에 연결
2) 흡수: 모델 이름에 없는 구분 단어(모노크롬·티탄·사파리·블랙페인트·기념판…)가 제목에 있는 매물
같은 (모델, 단어)가 MIN_COUNT건 이상이면 후보 → data/derived/entity_audit.json, 워크플로가 텔레그램으로 알림.
에디션 자체가 그 마감인 경우(LHSA·클래식 블랙페인트 등)나 표준 마감 표기(M11-P 'BlackPaint')는 OK 목록에.
"""
from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "data/derived/results_search_index_v1.json"
CATALOG = ROOT / "data/config/entity_catalog_v1.json"
OUT = ROOT / "data/derived/entity_audit.json"
MIN_COUNT = 3

WORDS = {
    "monochrom": r"monochrom|모노크롬|モノクローム",
    "titan": r"titan|티탄|チタン",
    "reporter": r"reporter|리포터",
    "safari": r"safari|사파리|サファリ",
    "LHSA": r"LHSA",
    "black paint": r"black ?paint|블랙 ?페인트|ブラックペイント",
    "anniversary": r"jahre|anniversary|주년|周年|jubilee",
    "hermes": r"herm[eè]s|에르메스",
    "gold": r"\bgold\b|골드",
}
# (모델 id에 들어 있는 말, 단어): 에디션 자체가 그 마감이거나, 표준 마감을 그렇게 부르는 경우
OK = [
    (r"lhsa|classic|ara-guler|your-mark|millennium|korea|mp3|m3j|a-la-carte|ttl-millennium", "black paint"),
    (r"d-lux-8|m11-p|m11-d|m10-d", "black paint"),
    (r"c-lux|d-lux|sofort", "gold"),  # 기본 색상 선택지
]


def _name_text(entity: dict) -> str:
    return " ".join([entity.get("name") or "", entity.get("name_ko") or ""] + list(entity.get("aliases") or [])).lower()


def audit(records: list[dict], entities: dict) -> dict:
    def ancestors(eid: str) -> set[str]:
        out = set()
        while entities.get(eid, {}).get("parent"):
            eid = entities[eid]["parent"]
            out.add(eid)
        return out

    overlap: Counter = Counter()
    absorbed: Counter = Counter()
    examples: dict = {}
    for record in records:
        title = (record.get("raw_item") or {}).get("상품명") or (record.get("final_output") or {}).get("title_raw") or ""
        leaves = [i for i in (record.get("entity_ids") or []) if i in entities and not entities[i].get("children")]
        for a in leaves:
            for b in leaves:
                if a < b and a not in ancestors(b) and b not in ancestors(a):
                    overlap[(a, b)] += 1
                    examples.setdefault(("overlap", a, b), title[:80])
        if (record.get("final_output") or {}).get("category") == "Accessory":
            continue
        for eid in leaves:
            name = _name_text(entities[eid])
            for word, pattern in WORDS.items():
                if re.search(pattern, title, re.I) and not re.search(pattern, name, re.I):
                    if any(re.search(ok_id, eid) and ok_word == word for ok_id, ok_word in OK):
                        continue
                    absorbed[(eid, word)] += 1
                    examples.setdefault(("absorbed", eid, word), title[:80])
    return {
        "overlap": [{"a": a, "b": b, "count": n, "example": examples[("overlap", a, b)]}
                    for (a, b), n in overlap.most_common() if n >= MIN_COUNT],
        "absorbed": [{"entity": e, "word": w, "count": n, "example": examples[("absorbed", e, w)]}
                     for (e, w), n in absorbed.most_common() if n >= MIN_COUNT],
    }


def main() -> None:
    records = json.loads(INDEX.read_text(encoding="utf-8"))["records"]
    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    entities = {e["id"]: e for e in catalog["entities"]}
    result = audit(records, entities)
    previous = {}
    if OUT.exists():
        try:
            previous = json.loads(OUT.read_text(encoding="utf-8"))
        except ValueError:
            previous = {}
    seen = {(x["entity"], x["word"]) for x in previous.get("absorbed", [])} | {(x["a"], x["b"]) for x in previous.get("overlap", [])}
    result["new"] = [x for x in result["absorbed"] if (x["entity"], x["word"]) not in seen] + \
                    [x for x in result["overlap"] if (x["a"], x["b"]) not in seen]
    OUT.write_text(json.dumps(result, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"🔍 엔티티 점검: 겹침 {len(result['overlap'])} · 흡수 후보 {len(result['absorbed'])} · 새로 생김 {len(result['new'])}")


if __name__ == "__main__":
    main()
