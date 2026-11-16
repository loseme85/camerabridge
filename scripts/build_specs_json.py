"""사양표(catalog/specs.py) → data/derived/specs_v1.json (대화창 '물어보기'가 읽음)

    python3 scripts/build_specs_json.py

엔티티마다 부모·바탕 모델을 겹쳐 쓴 최종 사양을 적는다. checked: 출처가 있는 엔티티만 true.
화면은 checked_only가 true면 확인된 값만 보여 주고, 사장님 미리보기(?ask=1)에서는 확인 전 값도 '확인 전' 표시와 함께 보여 준다.
사양표를 고치면 이 스크립트를 다시 돌린다 (tests/test_specs.py가 파일이 사양표와 같은지 확인).
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from catalog.specs import CHECKED, CHECKED_ONLY, spec_for  # noqa: E402

OUT = ROOT / "data" / "derived" / "specs_v1.json"


def build() -> dict:
    ents = json.loads((ROOT / "data/config/entity_catalog_v1.json").read_text(encoding="utf-8"))["entities"]
    parents = {e["id"]: e.get("parent") for e in ents}
    specs = {}
    for e in ents:
        if e["id"].split(":")[1] not in ("body", "lens"):
            continue
        spec = spec_for(e["id"], parents)
        if spec:
            specs[e["id"]] = spec
    return {"version": 1, "checked_only": CHECKED_ONLY, "checked": dict(sorted(CHECKED.items())), "specs": specs}


def main() -> None:
    OUT.write_text(json.dumps(build(), ensure_ascii=False, separators=(",", ":"), sort_keys=True) + "\n", encoding="utf-8")
    print(OUT.relative_to(ROOT), OUT.stat().st_size, "bytes")


if __name__ == "__main__":
    main()
