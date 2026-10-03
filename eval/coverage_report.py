"""엔티티 커버리지: 라이카 바디·렌즈 매물 중 정확한 모델 엔티티(자식)에 연결된 비율.

연결 안 된 매물 = 아직 엔티티가 없는 물건 → 다음에 만들 엔티티 목록.
사용: python3 eval/coverage_report.py [--list N]
"""
from __future__ import annotations

import collections
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from entity_catalog import load_catalog, match_entities  # noqa: E402

INDEX = ROOT / "data" / "derived" / "results_search_index_v1.json"
NOT_LEICA = re.compile(r"leeworks|light ?lens ?lab|\bLLL\b|7 ?artisans|ttartisan|voigtl|zeiss|sigma|ms-?optics|kipon|호환|\bcopy\b|카피|"
                       r"minolta|konica|canon|nikon|fuji|ricoh|contax|rollei|hasselblad|panasonic|lumix|olympus|pentax|sony|tamron|"
                       r"kodak|meyer|jupiter|kmz|\bfed\b|zorki|laowa|thypoch|funleader|astrhori|brightin|skier|cosina|yashica|mamiya|"
                       r"polaroid|lomo|schneider|angenieux|kern|steinheil|nokton|heliar|color-skopar", re.I)


def main() -> None:
    catalog = load_catalog()
    leaf = {eid for eid, e in catalog["entities"].items() if not e.get("children")}
    records = json.loads(INDEX.read_text(encoding="utf-8"))["records"]
    total = collections.Counter()
    linked = collections.Counter()
    missing = collections.defaultdict(list)
    for record in records:
        final = record.get("final_output") or {}
        title = final.get("title_raw") or ""
        category = final.get("category")
        if category not in ("Body", "Lens") or NOT_LEICA.search(title):
            continue
        total[category] += 1
        ids = record.get("entity_ids") or match_entities(record, catalog)
        if any(i in leaf for i in ids):
            linked[category] += 1
        else:
            missing[category].append(title)
    for category in ("Body", "Lens"):
        t, l = total[category], linked[category]
        print(f"{category}: {l}/{t} = {100 * l / max(t, 1):.1f}%")
    t, l = sum(total.values()), sum(linked.values())
    print(f"전체 라이카 바디·렌즈: {l}/{t} = {100 * l / max(t, 1):.1f}%")
    if "--list" in sys.argv:
        n = int(sys.argv[sys.argv.index("--list") + 1])
        for category in ("Body", "Lens"):
            print(f"\n## 엔티티 없는 {category} 예시")
            for title in collections.Counter(missing[category]).most_common(n):
                print(f"  {title[1]:3} {title[0][:80]}")


if __name__ == "__main__":
    main()
