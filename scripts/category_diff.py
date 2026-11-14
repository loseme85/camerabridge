"""분류 규칙을 고친 PR 점검: 고치기 전·후 검색 색인을 비교해 카테고리·모델이 바뀐 판매 중 매물을 모두 보여 준다.

2026-11-14 #369: 부속품 규칙을 넣다가 '벨로즈 + Macro-Elmar' 세트 9개와 'KS15-4 (M2-S)' 바디가 잘못 바뀐 것을
바뀐 목록을 한 줄씩 보고서야 찾았다. classifier_v2.py·entity_catalog_v1.json을 고친 PR은 이 목록을 PR 본문에 붙이고
한 줄씩 확인한 뒤 맞게 바뀐 것을 tests/fixtures/category_regressions.json에 더한다.

사용: cp data/derived/results_search_index_v1.json /tmp/before.json  (고치기 전 main에서)
      python3 final_resolution_pipeline.py && python3 scripts/build_entity_index.py  (고친 브랜치에서)
      python3 scripts/category_diff.py /tmp/before.json data/derived/results_search_index_v1.json [--json out.json]
"""
from __future__ import annotations

import json
import sys
from collections import Counter


def load(path: str) -> dict:
    out = {}
    for r in json.load(open(path, encoding="utf-8"))["records"]:
        f = r["final_output"]
        if f.get("sold_quality") != "asking":
            continue
        ents = r.get("entity_ids") or []
        out[f.get("source_url")] = (f.get("category"), ents[-1] if ents else "-", f.get("title_raw") or "",
                                    f.get("price_raw"), (f.get("source") or "").strip())
    return out


def main() -> None:
    before, after = load(sys.argv[1]), load(sys.argv[2])
    rows = []
    for url, (ca, ea, title, price, src) in before.items():
        if url in after and (ca != after[url][0] or ea != after[url][1]):
            rows.append({"from": ca, "to": after[url][0], "entity_from": ea, "entity_to": after[url][1],
                         "title": title, "price": price, "source": src, "url": url})
    rows.sort(key=lambda x: (x["from"], x["to"], x["entity_from"], x["title"]))
    print(f"바뀐 판매 중 매물 {len(rows)}개", dict(Counter(f"{x['from']}→{x['to']}" for x in rows)))
    for x in rows:
        print(f"{x['from']}→{x['to']} | {x['entity_from'].replace('leica:', '')} → {x['entity_to'].replace('leica:', '')} | "
              f"{x['title'][:80]} | {x['price']} | {x['source'][:20]}")
    if "--json" in sys.argv:
        json.dump(rows, open(sys.argv[sys.argv.index("--json") + 1], "w", encoding="utf-8"), ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()
