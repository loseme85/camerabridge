"""엔티티(모델) 카탈로그 원본 → data/config/entity_catalog_v1.json

엔티티 하나 = 구매자가 '이 물건'이라고 부르는 모델 하나.
  - match: 매물이 이 엔티티인지 판정하는 규칙 (종류·마운트·제목에 꼭 있어야/없어야 할 말)
  - aliases: 검색창 후보에 쓰는 이름 (영어 정식명·줄임말·한국어)
  - children: 부모 엔티티(예: Leica M6)는 자식(클래식·TTL·리이슈) 매물을 모두 포함

모델을 추가·수정할 때는 이 파일만 고치고 다시 실행한다:
  python3 catalog/build_entity_catalog.py
"""
from __future__ import annotations

import json
import re
from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / "data" / "config" / "entity_catalog_v1.json"
import sys as _sys  # noqa: E402

_sys.path.insert(0, str(Path(__file__).resolve().parent))

def f(n: str) -> str:
    """초점거리: 35mm, 35/1.4, 'M 35 ' 등. 135의 35 같은 오인 방지."""
    return rf"(?<![\d./]){n}(?!\s?/\s?\d{{3}})(?:\s?mm|/|\b)"


MODELS: dict[str, dict] = {}


def model(key, name, category, mount=None, must=(), must_not=()):
    MODELS[key] = {"model_key": key, "display_name": name, "category": category, "mount": mount,
                   "title_must": list(must), "title_must_not": list(must_not)}


ACC_NOT = [r"^(?!.*\b(with|w/)\s.*\bhood).*\bhood\b", r"후드", r"\bcap\b", r"캡", r"^(?!.*\b(with|w/)\s.*case).*case", r"케이스", r"strap", r"스트랩", r"holster", r"홀스터",
           r"grip", r"그립", r"battery", r"배터리", r"charger", r"충전기", r"protector", r"cover\b", r"부속품",
           r"adapter", r"어댑터", r"plate", r"플레이트", r"thumb", r"썸", r"manual", r"설명서", r"box only", r"박스만"]

# 타사·호환·모방품 (라이카 엔티티에서 제외)
THIRD_PARTY = [r"leeworks", r"light ?lens ?lab", r"\bLLL\b", r"7 ?artisans", r"ttartisan", r"voigtl", r"zeiss",
               r"sigma", r"ms-?optics", r"kipon", r"호환", r"\bcopy\b", r"카피"]

# ── 바디는 catalog/bodies.py ──

# ── M 렌즈 ──
model("leica:lens:summilux-m:35:asph-fle", "Summilux-M 35mm f/1.4 ASPH FLE", "Lens", "M",
      [r"(summilux|\blux\b)", f("35"), r"FLE"], [r"FLE ?(II|2)\b", r"steel"] + ACC_NOT)
model("leica:lens:summilux-m:35:asph-fle2", "Summilux-M 35mm f/1.4 ASPH FLE II", "Lens", "M",
      [r"(summilux|\blux\b)", f("35"), r"FLE ?(II|2)\b"], ACC_NOT)
model("leica:lens:summilux-m:35:steel-rim-reissue", "Summilux-M 35mm f/1.4 Steel Rim (2021 reissue)", "Lens", "M",
      [r"(summilux|\blux\b)", f("35"), r"(steel ?rim|스틸 ?림)", r"(re-?issue|복각|2021)"], ACC_NOT)
model("leica:lens:summicron-m:35:asph", "Summicron-M 35mm f/2 ASPH", "Lens", "M",
      [r"summicron|cron", f("35"), r"ASPH"], [r"\bAPO\b"] + ACC_NOT)
model("leica:lens:summicron-m:35:v1-8element", "Summicron 35mm f/2 1st (8 elements)", "Lens", "M",
      [r"summicron|cron", f("35"), r"(8 ?el|8매|eight|1st|1세대|\bv\.? ?1\b)"], [r"ASPH"] + ACC_NOT)
model("leica:lens:summicron-m:35:v4", "Summicron 35mm f/2 4th (pre-ASPH)", "Lens", "M",
      [r"summicron|cron", f("35"), r"(4th|v4|4세대|6매|6 ?el|IV\b|king ?of ?bokeh|bokeh ?king|\bKOB\b)"], [r"ASPH"] + ACC_NOT)
model("leica:lens:apo-summicron-m:35", "APO-Summicron-M 35mm f/2 ASPH", "Lens", "M",
      [r"APO", r"summicron|cron", f("35")], ACC_NOT)
model("leica:lens:summilux-m:50:asph", "Summilux-M 50mm f/1.4 ASPH", "Lens", "M",
      [r"(summilux|\blux\b)", f("50"), r"ASPH"], ACC_NOT)
model("leica:lens:summicron-m:50:current", "Summicron-M 50mm f/2 (4th/5th)", "Lens", "M",
      [r"summicron|cron", f("50")], [r"\bAPO\b", r"rigid|리짓", r"\bDR\b|dual ?range", r"collaps|침동", r"\bR\b ?50|-R\b", r"\bSL\b", r"\bL ?50|LTM|M39"] + ACC_NOT)
model("leica:lens:summicron:50:rigid", "Summicron 50mm f/2 Rigid", "Lens", None, [r"summicron|cron", f("50"), r"rigid|리짓|고정"], [r"\bDR\b|dual ?range"] + ACC_NOT)
model("leica:lens:summicron:50:dr", "Summicron 50mm f/2 Dual Range", "Lens", "M", [r"summicron|cron", f("50"), r"\bDR\b|dual ?range"], ACC_NOT)
model("leica:lens:apo-summicron-m:50", "APO-Summicron-M 50mm f/2 ASPH", "Lens", "M", [r"APO", r"summicron|cron", f("50")], [r"\bSL\b"] + ACC_NOT)
model("leica:lens:noctilux-m:50:f0.95", "Noctilux-M 50mm f/0.95 ASPH", "Lens", "M", [r"nocti", r"0\.95"], [r"\b75\b", f("35")] + ACC_NOT)
# Noctilux-M 50 f/1.0 은 세대 부모 → catalog/lenses.py
model("leica:lens:noctilux:50:f1.2-original", "Noctilux 50mm f/1.2 (original, 1966)", "Lens", "M",
      [r"nocti", r"1\.2\b|original|오리지널|1세대|\b1st\b"],  # 국내 표기 1세대 = f/1.2 오리지널
      [r"복각", r"re-?issue", r"ASPH", r"6 ?bit", r"신품", r"\b75\b", f("35"), r"0\.95", r"(?<![\d.])1\.0\b|/1\b(?!\.\d)|f/?1\b(?!\.\d)|E58|E60"] + ACC_NOT)
model("leica:lens:noctilux-m:50:f1.2-asph", "Noctilux-M 50mm f/1.2 ASPH (2021 reissue)", "Lens", "M",
      [r"nocti", r"1\.2\b", r"(복각|re-?issue|ASPH|6 ?bit|신품)"], [r"오리지널|original", r"\b75\b", f("35")] + ACC_NOT)
model("leica:lens:noctilux-m:75", "Noctilux-M 75mm f/1.25 ASPH", "Lens", "M", [r"nocti", f("75")], ACC_NOT)
model("leica:lens:noctilux-m:35", "Noctilux-M 35mm f/1.2 ASPH", "Lens", "M", [r"nocti", f("35")], ACC_NOT)
model("leica:lens:elmarit-m:28:asph", "Elmarit-M 28mm f/2.8 ASPH", "Lens", "M", [r"elmarit", f("28"), r"ASPH"], ACC_NOT)
model("leica:lens:elmar-m:50:f2.8", "Elmar-M 50mm f/2.8", "Lens", None, [r"elmar\b|elmar-m", f("50"), r"2\.8"], [r"elmarit"] + ACC_NOT)
model("leica:lens:summicron-m:90", "Summicron-M 90mm f/2", "Lens", "M", [r"summicron|cron", f("90")], [r"\bAPO\b", r"-R\b|\bR ?90", r"\bSL\b"] + ACC_NOT)
model("leica:lens:summilux-m:75", "Summilux-M 75mm f/1.4", "Lens", "M", [r"(summilux|\blux\b)", f("75")], [r"\bSL\b"] + ACC_NOT)
model("leica:lens:tri-elmar-m:16-18-21", "Tri-Elmar-M 16-18-21mm f/4 (WATE)", "Lens", "M", [r"(tri.?elmar|WATE)", r"16"], ACC_NOT)
model("leica:lens:super-elmar-m:21", "Super-Elmar-M 21mm f/3.4 ASPH", "Lens", "M", [r"super-? ?elmar", f("21")], ACC_NOT)
# ── SL · R 렌즈 ──
model("leica:lens:vario-elmarit-sl:24-90", "Vario-Elmarit-SL 24-90mm f/2.8-4 ASPH", "Lens", "SL", [r"24-90"], ACC_NOT)
model("leica:lens:apo-summicron-sl:35", "APO-Summicron-SL 35mm f/2 ASPH", "Lens", "SL", [r"APO", r"summicron", f("35")], ACC_NOT)
model("leica:lens:summicron-r:50", "Summicron-R 50mm f/2", "Lens", "R", [r"summicron", f("50")], ACC_NOT)
model("leica:lens:apo-telyt-r:180", "APO-Telyt-R 180mm f/3.4", "Lens", "R", [r"telyt", f("180")], ACC_NOT)
model("leica:lens:summilux-r:80", "Summilux-R 80mm f/1.4", "Lens", "R", [r"summilux", f("80")], ACC_NOT)


# ── 검색 별칭 (소문자, 띄어쓰기 자유: 검색창이 하이픈·슬래시·공백을 같게 본다) ──
ALIASES: dict[str, list[str]] = {
    "leica:lens:summilux-m:35:asph-fle": ["summilux-m 35 asph fle", "summilux 35 fle", "35 lux fle", "35lux fle", "주미룩스 35 fle", "35 룩스 fle"],
    "leica:lens:summilux-m:35:asph-fle2": ["summilux-m 35 asph fle ii", "summilux 35 fle ii", "summilux 35 fle2", "35 lux fle2", "35 lux fle ii", "주미룩스 35 fle2", "35 룩스 fle2"],
    "leica:lens:summilux-m:35:steel-rim-reissue": ["summilux 35 steel rim reissue", "35 lux steel rim", "steel rim reissue", "스틸림 복각", "주미룩스 35 스틸림"],
    "leica:lens:summicron-m:35:asph": ["summicron-m 35 asph", "summicron 35 asph", "35 cron asph", "주미크론 35 asph", "35 크론 asph"],
    "leica:lens:summicron-m:35:v1-8element": ["summicron 35 8 element", "summicron 35 1st", "summicron 35 v1", "35 cron 8 element", "35 cron v1", "35 cron 1st", "8 element", "8매", "6군8매", "주미크론 35 8매", "주미크론 35 1세대", "35 크론 1세대", "35 크론 8매"],
    "leica:lens:summicron-m:35:v4": ["summicron 35 4th", "summicron 35 v4", "35 cron v4", "35 cron 4th", "6매", "주미크론 35 4세대", "35 크론 4세대", "35 크론 v4", "칠공팔공 6매",
                                     "king of bokeh", "bokeh king", "kob", "35 cron kob", "킹 오브 보케", "보케 킹"],
    "leica:lens:apo-summicron-m:35": ["apo-summicron-m 35", "apo summicron m 35", "apo 35 cron", "아포 주미크론 35"],
    "leica:lens:summilux-m:50:asph": ["summilux-m 50 asph", "summilux 50 asph", "50 lux asph", "주미룩스 50 asph", "50 룩스 asph"],
    "leica:lens:summicron-m:50:current": ["summicron-m 50", "summicron m 50", "summicron 50 4th", "summicron 50 5th", "50 cron m", "주미크론 m 50"],
    "leica:lens:summicron:50:rigid": ["summicron 50 rigid", "50 cron rigid", "rigid", "리짓", "리지드", "주미크론 50 리짓"],
    "leica:lens:summicron:50:dr": ["summicron 50 dual range", "summicron 50 dr", "50 cron dr", "dual range", "주미크론 50 dr"],
    "leica:lens:apo-summicron-m:50": ["apo-summicron-m 50", "apo summicron m 50", "apo summicron 50", "apo 50 cron", "아포 주미크론 50"],
    "leica:lens:noctilux-m:50:f0.95": ["noctilux-m 50 0.95", "noctilux 0.95", "nocti 0.95", "녹티룩스 0.95", "녹티 0.95"],
    "leica:lens:noctilux:50:f1.2-original": ["noctilux 1.2 original", "noctilux 50 1.2 original", "nocti 1.2 original", "녹티룩스 1.2 오리지널", "녹티 1.2 오리지널",
                                             "noctilux original", "noctilux 1st", "nocti 1st", "noctilux 1st gen", "녹티룩스 오리지널", "녹티 오리지널",
                                             "녹티룩스 1세대", "녹티 1세대", "녹티룩스 1st", "녹티 1st"],
    "leica:lens:noctilux-m:50:f1.2-asph": ["noctilux-m 50 1.2 asph", "noctilux 1.2 asph", "noctilux 1.2 reissue", "nocti 1.2", "녹티룩스 1.2 복각", "녹티 1.2 복각", "noctilux 1.2"],
    "leica:lens:noctilux-m:75": ["noctilux-m 75", "noctilux 75", "nocti 75", "녹티룩스 75"],
    "leica:lens:noctilux-m:35": ["noctilux-m 35", "noctilux 35", "nocti 35", "녹티룩스 35"],
    "leica:lens:elmarit-m:28:asph": ["elmarit-m 28 asph", "elmarit 28 asph", "28 elmarit", "엘마리트 28", "엘마리트 28 asph"],
    "leica:lens:elmar-m:50:f2.8": ["elmar-m 50 2.8", "elmar 50 2.8", "50 elmar 2.8", "엘마 50 2.8"],
    "leica:lens:summicron-m:90": ["summicron-m 90", "summicron 90", "90 cron", "주미크론 90"],
    "leica:lens:summilux-m:75": ["summilux-m 75", "summilux 75", "75 lux", "주미룩스 75"],
    "leica:lens:tri-elmar-m:16-18-21": ["tri-elmar-m 16-18-21", "tri elmar 16 18 21", "wate", "트라이엘마 16-18-21", "와테"],
    "leica:lens:super-elmar-m:21": ["super-elmar-m 21", "super elmar 21", "21 super elmar", "수퍼엘마 21", "슈퍼엘마 21"],
    "leica:lens:vario-elmarit-sl:24-90": ["vario-elmarit-sl 24-90", "sl 24-90", "24-90 vario elmarit", "24-90", "sl 24-90 줌"],
    "leica:lens:apo-summicron-sl:35": ["apo-summicron-sl 35", "apo summicron sl 35", "sl 35 apo", "아포 주미크론 sl 35"],
    "leica:lens:summicron-r:50": ["summicron-r 50", "summicron r 50", "r 50 cron", "50 cron r", "주미크론 r 50"],
    "leica:lens:apo-telyt-r:180": ["apo-telyt-r 180", "apo telyt r 180", "r 180 apo", "180 apo telyt", "아포 텔리트 180"],
    "leica:lens:summilux-r:80": ["summilux-r 80", "summilux r 80", "r 80 lux", "주미룩스 r 80"],
}

# 한국어 표시 이름 (검색창 후보 보조 줄)
NAME_KO = {
    "leica:lens:summilux-m:35:asph-fle": "주미룩스 35 FLE", "leica:lens:summilux-m:35:asph-fle2": "주미룩스 35 FLE II",
    "leica:lens:summilux-m:35:steel-rim-reissue": "주미룩스 35 스틸림 복각", "leica:lens:summicron-m:35:asph": "주미크론 35 ASPH",
    "leica:lens:summicron-m:35:v1-8element": "주미크론 35 1세대 8매", "leica:lens:summicron-m:35:v4": "주미크론 35 4세대 (6매)",
    "leica:lens:apo-summicron-m:35": "아포 주미크론 M 35", "leica:lens:summilux-m:50:asph": "주미룩스 50 ASPH",
    "leica:lens:summicron-m:50:current": "주미크론 M 50 (4·5세대)", "leica:lens:summicron:50:rigid": "주미크론 50 리짓",
    "leica:lens:summicron:50:dr": "주미크론 50 DR", "leica:lens:apo-summicron-m:50": "아포 주미크론 M 50",
    "leica:lens:noctilux-m:50:f0.95": "녹티룩스 50 f/0.95",
    "leica:lens:noctilux:50:f1.2-original": "녹티룩스 50 f/1.2 오리지널", "leica:lens:noctilux-m:50:f1.2-asph": "녹티룩스 50 f/1.2 ASPH (복각)",
    "leica:lens:noctilux-m:75": "녹티룩스 75", "leica:lens:noctilux-m:35": "녹티룩스 35",
    "leica:lens:elmarit-m:28:asph": "엘마리트 28 ASPH",
    "leica:lens:elmar-m:50:f2.8": "엘마 50 f/2.8",
    "leica:lens:summicron-m:90": "주미크론 90", "leica:lens:summilux-m:75": "주미룩스 75", "leica:lens:tri-elmar-m:16-18-21": "트라이엘마 16-18-21",
    "leica:lens:super-elmar-m:21": "수퍼엘마 21", "leica:lens:summicron-r:50": "주미크론 R 50", "leica:lens:apo-telyt-r:180": "아포 텔리트 R 180",
    "leica:lens:summilux-r:80": "주미룩스 R 80", "leica:lens:apo-summicron-sl:35": "아포 주미크론 SL 35",
}

# ── 부모 엔티티: 세대·버전이 여럿인 이름. 자식 매물을 모두 포함하고, 고르면 자식으로 좁힐 수 있다 ──
PARENTS = {
    "leica:lens:noctilux-m:50": ("Noctilux-M 50mm (all)", "Lens", "M", ["leica:lens:noctilux-m:50:f0.95", "leica:lens:noctilux-m:50:f1.0", "leica:lens:noctilux:50:f1.2-original", "leica:lens:noctilux-m:50:f1.2-asph"],
                                 ["noctilux", "nocti", "noctilux 50", "녹티룩스", "녹티", "녹티룩스 50"], "녹티룩스 50 (전체)"),
    "leica:lens:summilux-m:35": ("Summilux-M 35mm (all)", "Lens", "M",
                                 ["leica:lens:summilux-m:35:asph-fle", "leica:lens:summilux-m:35:asph-fle2", "leica:lens:summilux-m:35:steel-rim-reissue"],
                                 ["summilux 35", "summilux-m 35", "35 lux", "35lux", "주미룩스 35", "35 룩스"], "주미룩스 35 (전체)"),
    "leica:lens:summicron:50": ("Summicron 50mm (all)", "Lens", None,
                                ["leica:lens:summicron-m:50:current", "leica:lens:summicron:50:rigid", "leica:lens:summicron:50:dr", "leica:lens:summicron-r:50", "leica:lens:apo-summicron-m:50"],
                                ["summicron 50", "50 cron", "50cron", "주미크론 50", "50 크론"], "주미크론 50 (전체)"),
    "leica:lens:summicron-m:35": ("Summicron-M 35mm (all)", "Lens", "M",
                                  ["leica:lens:summicron-m:35:asph", "leica:lens:summicron-m:35:v1-8element", "leica:lens:summicron-m:35:v4", "leica:lens:apo-summicron-m:35"],
                                  ["summicron 35", "35 cron", "35cron", "주미크론 35", "35 크론"], "주미크론 35 (전체)"),
}


def build() -> dict:
    import bodies
    import codes
    import features
    import lenses

    for module in (bodies, lenses):
        for key, spec in module.MODELS.items():
            assert key not in MODELS, key
            MODELS[key] = spec
        ALIASES.update(module.ALIASES)
        NAME_KO.update(module.NAME_KO)
        for key, value in module.PARENTS.items():
            assert key not in PARENTS, key
            PARENTS[key] = value
    for parent, children in lenses.EXTEND_PARENTS.items():
        name, kind, mount, kids, als, ko = PARENTS[parent]
        PARENTS[parent] = (name, kind, mount, kids + [c for c in children if c not in kids], als, ko)
    for parent, order in lenses.CHILD_ORDER.items():  # 적힌 순서가 먼저, 나머지(APO 등)는 뒤에 그대로
        name, kind, mount, kids, als, ko = PARENTS[parent]
        rank = {(slug if ":" in slug else f"{parent}:{slug}"): i for i, slug in enumerate(order)}
        PARENTS[parent] = (name, kind, mount, sorted(kids, key=lambda k: rank.get(k, len(rank))), als, ko)
    for key, extra in lenses.TIGHTEN.items():
        MODELS[key]["title_must_not"] = MODELS[key]["title_must_not"] + extra
    for key, must in lenses.OVERRIDE_MUST.items():
        MODELS[key]["title_must"] = must
    all_codes: dict[str, list[str]] = {}
    for key, numbers in codes.CODES.items():
        assert key in MODELS or key in PARENTS, f"codes: unknown entity {key}"
        assert len(numbers) == len(set(numbers)), f"codes: duplicate on {key}"
        for number in numbers:
            assert re.fullmatch(r"\d{5}", number), number
        all_codes[key] = list(numbers)
    for key, words in codes.CODE_WORDS.items():
        assert key in MODELS or key in PARENTS, f"code words: unknown entity {key}"
        for word in words:
            assert re.fullmatch(r"[A-Z]{5}(-[A-Z]{1,2})?", word), word
        # 검색창과 같은 정규화 (소문자, 하이픈 → 띄어쓰기): "SOOIC-M" → "sooic m"
        all_codes.setdefault(key, []).extend(w.lower().replace("-", " ") for w in words)
    entities = []
    for key, spec in MODELS.items():
        assert key in ALIASES, f"aliases missing: {key}"
        entities.append({
            "id": key, "name": spec["display_name"], "name_ko": NAME_KO.get(key), "kind": spec["category"],
            "mount": spec["mount"], "parent": next((p for p, v in PARENTS.items() if key in v[3]), None), "children": [],
            "aliases": sorted(set(a.lower() for a in ALIASES[key])), "codes": all_codes.get(key, []),
            "match": {"category": spec["category"], "mount": spec["mount"], "title_must": spec["title_must"],
                      "title_must_not": spec["title_must_not"] + THIRD_PARTY
                      + ([p for p in ACC_NOT if p not in spec["title_must_not"]] if spec["category"] == "Body" else [])},
        })
    for key, (name, kind, mount, children, aliases, name_ko) in PARENTS.items():
        for child in children:
            assert child in MODELS or child in PARENTS, child
        grand = next((p for p, v in PARENTS.items() if key in v[3]), None)
        entities.append({"id": key, "name": name, "name_ko": name_ko, "kind": kind, "mount": mount, "parent": grand,
                         "children": children, "aliases": sorted(set(a.lower() for a in aliases)),
                         "codes": all_codes.get(key, []), "match": None})
    for key, (name, name_ko, members, aliases, exclude) in features.FEATURES.items():
        for member in members:
            assert member in MODELS or member in PARENTS, f"features: unknown member {member}"
        entities.append({"id": key, "name": name, "name_ko": name_ko, "kind": "Body", "mount": "M", "parent": None,
                         "children": [], "aliases": sorted(set(a.lower() for a in aliases)), "codes": [], "match": None,
                         "feature": {"members": members, "exclude": exclude}})
    return {"schema_version": "entity_catalog_v1", "updated_at": "2026-10-03", "entities": entities}


if __name__ == "__main__":
    catalog = build()
    OUT.write_text(json.dumps(catalog, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"entities {len(catalog['entities'])} → {OUT}")
