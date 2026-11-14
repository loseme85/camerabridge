"""시세 이탈 점검: 크롤할 때마다 모델 시세에서 크게 벗어난 판매 중 매물을 찾는다 (2026-11-14 사장님).

시세에서 크게 벗어난 매물은 대개 모델 연결이 틀린 것이다 — 부속품(설명서·벨로즈·빈 상자)이 본품으로,
바디+렌즈 세트가 렌즈로, 한정판·리페인트가 일반 모델로 잡힌 경우. 한 모델의 판매 중 매물이 4개 이상일 때
중앙값의 0.45배 미만·2.5배 초과를 이탈로 본다.

결과: data/derived/price_outlier_audit.json
  - items: 지금 이탈 매물 전체 (주소·모델·배율·짐작 원인)
  - new:   지난 크롤에 없던 이탈 매물 → 워크플로가 텔레그램으로 알림, 밤샘 때 분류를 고친다
짐작 원인(hint): accessory(부속품 말) · set(세트) · edition(한정판·특수 마감) · defect(고장·부품용) · check(직접 확인)
"""
from __future__ import annotations

import json
import re
import statistics
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

from build_entity_index import krw_rates  # noqa: E402
from entity_catalog import load_catalog  # noqa: E402

INDEX = ROOT / "data/derived/results_search_index_v1.json"
OUT = ROOT / "data/derived/price_outlier_audit.json"
LOW, HIGH, MIN_ITEMS = 0.45, 2.5, 4

HINTS = (
    ("defect", re.compile(r"not working|for parts|defekt|ohne funktion|ジャンク|故障|부품용|고장|restoration|repair", re.I)),
    ("accessory", re.compile(r"manual|anleitung|説明書|取説|box only|empty box|元箱のみ|dummy|bellows|balgen|extension tube|"
                             r"zwischenring|handgriff|grip|protekt|case|tasche|etui|ケース|hood|sonnenblende|finder|sucher(?!kamera)|"
                             r"cap|deckel|adapter|strap|riemen|ストラップ", re.I)),
    ("set", re.compile(r"\bwith\b|\bmit\b|\bw/|\+|付|\bset\b|\bkit\b|\bcon\b|세트|セット", re.I)),
    ("edition", re.compile(r"edition|limited|titan|チタン|safari|hermes|herm[eè]s|black ?paint|ブラックペイント|後塗|repaint|"
                           r"jahre|anniversary|周年|gold|lhsa|a la carte|à la carte|\b\d{1,3}\s?/\s?\d{2,4}\b|#\d", re.I)),
)


def hint(title: str, note: str) -> str:
    if note == "set":
        return "set"
    for name, rx in HINTS:
        if rx.search(title):
            return name
    return "check"


def main() -> None:
    cat = load_catalog()["entities"]
    rates = krw_rates()
    leaf = lambda e: e in cat and not cat[e].get("children") and not cat[e].get("feature")  # noqa: E731
    by: dict[str, list] = defaultdict(list)
    for r in json.load(open(INDEX, encoding="utf-8"))["records"]:
        f = r["final_output"]
        if f.get("sold_quality") != "asking" or f.get("entity_note") == "duplicate":
            continue
        price, rate = f.get("parsed_price_numeric"), rates.get(str(f.get("currency") or "KRW").upper())
        leaves = [e for e in r.get("entity_ids") or [] if leaf(e)]
        if not price or not rate or not leaves:
            continue
        by[leaves[-1]].append((price * rate, f))

    items = []
    for ent, rows in by.items():
        if len(rows) < MIN_ITEMS:
            continue
        med = statistics.median(k for k, _ in rows)
        for k, f in rows:
            ratio = k / med
            if ratio < LOW or ratio > HIGH:
                title = f.get("title_raw") or ""
                items.append({"url": f.get("source_url"), "entity": ent, "ratio": round(ratio, 2), "category": f.get("category"),
                              "title": title[:100], "price": f.get("price_raw"), "source": (f.get("source") or "").strip(),
                              "hint": hint(title, f.get("entity_note") or "")})
    items.sort(key=lambda x: (x["entity"], x["ratio"]))

    try:
        seen = {x["url"] for x in json.load(open(OUT, encoding="utf-8")).get("items", [])}
    except Exception:  # noqa: BLE001 — 첫 실행
        seen = None
    new = [] if seen is None else [x for x in items if x["url"] not in seen]
    counts = defaultdict(int)
    for x in items:
        counts[x["hint"]] += 1
    OUT.write_text(json.dumps({"total": len(items), "by_hint": dict(counts), "new": new, "items": items},
                              ensure_ascii=False, indent=0) + "\n", encoding="utf-8")
    print(f"시세 이탈 {len(items)}개 (새로 {len(new)}개) {dict(counts)}")


if __name__ == "__main__":
    main()
