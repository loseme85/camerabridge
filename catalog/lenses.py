"""라이카 렌즈 엔티티 (계열 · 세대 · 에디션).

build_entity_catalog.py의 기존 렌즈(ID 유지)에 더해, 빠진 세대·모델을 채운다.
  - group(): 계열 부모 + 세대/에디션 자식 + "세대 미표기" 자식
  - lens():  세대 구분이 없는 단일 모델
  - EXTEND_PARENTS: 기존 부모(예: Summilux-M 35)에 새 자식 추가
  - TIGHTEN: 기존 자식이 새 자식의 매물을 가져가지 않도록 제외 규칙 추가
"확인 필요" 주석은 연도·이름을 공식 자료로 다시 확인해야 하는 항목.
"""
from __future__ import annotations

MODELS: dict[str, dict] = {}
PARENTS: dict[str, tuple] = {}
ALIASES: dict[str, list[str]] = {}
NAME_KO: dict[str, str] = {}
EXTEND_PARENTS: dict[str, list[str]] = {}
TIGHTEN: dict[str, list[str]] = {}
OVERRIDE_MUST: dict[str, list[str]] = {}

ACC = [r"\bhood\b", r"후드", r"\bcap\b", r"캡", r"case", r"케이스", r"부속품", r"filter\b", r"필터", r"adapter", r"어댑터",
       r"finder", r"파인더", r"box only", r"박스만", r"manual", r"설명서"]


def f(n: str) -> str:
    """초점거리: 35mm, 35/1.4, 'M 35 ' 등. 135의 35·에디션 번호(33/50) 오인 방지."""
    return rf"(?<![\d./\-–]){n}(?!\s?/\s?\d{{3}})(?![\-–]\d)(?:\s?mm|/|\b)"


FAM = {  # 계열 → (제목 패턴, 별칭 이름들)
    "summilux": (r"(summilux|\blux\b)", ["summilux", "lux", "주미룩스", "룩스"]),
    "summicron": (r"(summicron|\bcron\b)", ["summicron", "cron", "주미크론", "크론"]),
    "apo-summicron": (r"apo.{0,3}summicron|summicron.{0,12}\bapo\b", ["apo summicron", "apo cron", "아포 주미크론"]),
    "elmarit": (r"elmarit", ["elmarit", "엘마리트"]),
    "elmar": (r"\belmar\b(?!it)|elmar-[mc]\b", ["elmar", "엘마"]),
    "summarit": (r"summarit", ["summarit", "즈마릿", "주마릿"]),
    "summaron": (r"summaron", ["summaron", "즈마론", "주마론"]),
    "summitar": (r"summitar", ["summitar", "즈미타", "주미타"]),
    "summar": (r"\bsummar\b", ["summar", "주마"]),
    "summarex": (r"summarex", ["summarex", "주마렉스"]),
    "xenon": (r"xenon", ["xenon", "제논"]),
    "hektor": (r"hektor", ["hektor", "헥토르"]),
    "thambar": (r"thambar", ["thambar", "탐바"]),
    "hologon": (r"hologon", ["hologon", "홀로곤"]),
    "super-angulon": (r"super.?angulon", ["super angulon", "슈퍼앵귤론"]),
    "super-elmar": (r"super.?elmar\b", ["super elmar", "수퍼엘마", "슈퍼엘마"]),
    "tri-elmar": (r"tri.?elmar|\bMATE\b", ["tri elmar", "트라이엘마"]),
    "macro-elmar": (r"macro.?elmar\b", ["macro elmar", "매크로 엘마"]),
    "tele-elmarit": (r"tele.?elmarit", ["tele elmarit", "텔레엘마리트"]),
    "tele-elmar": (r"tele.?elmar\b", ["tele elmar", "텔레엘마"]),
    "apo-telyt": (r"apo.?telyt", ["apo telyt", "아포 텔리트"]),
    "telyt": (r"telyt", ["telyt", "텔리트"]),
    "apo-macro-elmarit": (r"apo.?macro.?elmarit", ["apo macro elmarit", "아포 매크로 엘마리트"]),
    "macro-elmarit": (r"macro.?elmarit", ["macro elmarit", "매크로 엘마리트"]),
    "apo-elmarit": (r"apo.?elmarit", ["apo elmarit", "아포 엘마리트"]),
    "vario-elmarit": (r"vario.?elmarit", ["vario elmarit", "바리오 엘마리트"]),
    "vario-elmar": (r"vario.?elmar\b", ["vario elmar", "바리오 엘마"]),
    "super-vario-elmar": (r"super.?vario.?elmar\b", ["super vario elmar"]),
    "super-vario-elmarit": (r"super.?vario.?elmarit", ["super vario elmarit"]),
    "apo-vario-elmarit": (r"apo.?vario.?elmarit", ["apo vario elmarit"]),
    "apo-vario-elmar": (r"apo.?vario.?elmar\b", ["apo vario elmar"]),
    "fisheye-elmarit": (r"fish.?eye", ["fisheye elmarit", "fisheye", "어안"]),
    "apo-macro-summarit": (r"apo.?macro.?summarit", ["apo macro summarit"]),
    "apo-elmar": (r"apo.?elmar\b", ["apo elmar"]),
    "summicron-c": (r"summicron.?c\b", ["summicron c", "주미크론 c"]),
    "elmar-c": (r"elmar.?c\b", ["elmar c", "엘마 c"]),
}
MOUNT_NOT = {  # M 렌즈에서 다른 마운트 제외
    "M": [r"\bSL\b|-SL\b", r"\bTL\b|-TL\b", r"-R\b|\bR ?\d{2}|\bR\b ?\d", r"-S\b", r"\bL ?\d{2}/|LTM|M39|screw"],
    "SL": [r"\bTL\b|-TL\b", r"-R\b", r"-M\b"], "TL": [r"\bSL\b|-SL\b", r"-M\b", r"-R\b"], "R": [r"-M\b", r"\bSL\b|-SL\b", r"\bTL\b"],
    "S": [r"\bSL\b", r"-M\b", r"-R\b"], None: [],
}
MOUNT_WORD = {"M": "", "SL": "sl", "TL": "tl", "R": "r", "S": "s", None: ""}


def aliases(fam, focal, suffixes=("",), mount=None):
    names = FAM[fam][1]
    mw = MOUNT_WORD.get(mount, "")
    out = set()
    for n in names:
        for sfx in suffixes:
            sfx = f" {sfx}" if sfx else ""
            if mw:
                out |= {f"{n} {mw} {focal}{sfx}", f"{mw} {focal} {n}{sfx}", f"{n}-{mw} {focal}{sfx}"}
            else:
                out |= {f"{n} {focal}{sfx}", f"{focal} {n}{sfx}"}
    return sorted(a.strip().lower() for a in out)


COMPOUND_ELMAR = r"vario.?elmar|tri.?elmar|super.?elmar|tele.?elmar|macro.?elmar|apo.?elmar|elmar.?c\b"
MOUNT_EVIDENCE = {"R": r"-R\b|\bR\s?\d|\bR\b|\bROM\b", "SL": r"-SL\b|\bSL\b", "TL": r"-TL\b|\bTL\b", "S": r"-S\b|\bS\s?\d|\bS\b"}


def _add(key, name, ko, mount, must, must_not, als):
    must = list(must)
    if mount in MOUNT_EVIDENCE:  # R·SL·TL·S 렌즈는 제목에 마운트 표기가 있어야 함 (없으면 M으로 봄)
        must.append(MOUNT_EVIDENCE[mount])
    nots = list(must_not) + MOUNT_NOT.get(mount, []) + ACC
    if any("elmar\\b(?!it)" in m for m in must[:1]):  # 단독 Elmar는 Vario·Tri·Super·Tele·Macro Elmar 제외
        nots.append(COMPOUND_ELMAR)
    MODELS[key] = {"model_key": key, "display_name": name, "category": "Lens", "mount": mount,
                   "title_must": must, "title_must_not": nots}
    ALIASES[key] = sorted(set(a.lower() for a in als))
    if ko:
        NAME_KO[key] = ko


def lens(key, name, ko, mount, fam, focal, extra_must=(), must_not=(), suffixes=("",), extra_aliases=()):
    must = [FAM[fam][0]] + ([f(focal)] if focal and "-" not in focal else ([focal.replace("-", r"\s?-\s?")] if focal else [])) + list(extra_must)
    _add(key, name, ko, mount, must, must_not, aliases(fam, focal, suffixes, mount) + list(extra_aliases))


def group(key, name, ko, mount, fam, focal, children, extra_must=(), must_not=(), unspecified=True, parent_aliases=(), existing=()):
    """children: (slug, 이름, 한국어, 표시 패턴, 추가 제외, 별칭 접미어)"""
    base = [FAM[fam][0]] + ([f(focal)] if "-" not in focal else [focal.replace("-", r"\s?-\s?")]) + list(extra_must)
    kids = list(existing)
    markers = []
    for slug, cname, cko, marker, cnot, sfx in children:
        ck = f"{key}:{slug}"
        _add(ck, cname, cko, mount, base + [marker], list(must_not) + list(cnot), aliases(fam, focal, sfx, mount))
        kids.append(ck)
        markers.append(marker)
    if unspecified:
        uk = f"{key}:unspecified"
        _add(uk, f"{name} (generation not stated)", f"{ko} (세대 미표기)" if ko else None, mount, base, list(must_not) + markers, [])
        ALIASES[uk] = [f"{a} 세대 미표기" for a in aliases(fam, focal, ("",), mount)[:2]]
        kids.append(uk)
    PARENTS[key] = (f"{name} (all)", "Lens", mount, kids, aliases(fam, focal, ("",), mount) + list(parent_aliases), f"{ko} (전체)" if ko else None)
    return markers


def c(slug, name, ko, marker, cnot=(), sfx=("",)):
    return (slug, name, ko, marker, list(cnot), list(sfx))


GEN1, GEN2, GEN3, GEN4 = (r"\b1st\b|\b1th\b|1세대|\bv\.?1\b|first", r"\b2nd\b|2세대|\bv\.?2\b|second", r"\b3rd\b|\b3th\b|3세대|\bv\.?3\b|third",
                          r"\b4th\b|4세대|\bv\.?4\b|fourth")

# ───────────── M: Summilux 35 (기존 부모에 세대·에디션 추가) ─────────────
SL35 = "leica:lens:summilux-m:35"
EDITION_35LUX = [r"titan|티탄", r"leitz ?wetzlar", r"10 ?jahre", r"independence|광복", r"LHSA", r"classic|클래식"]
for slug, name, ko, marker, extra_not, sfx in [
    ("v1-steel-rim", "Summilux 35mm f/1.4 1st Steel Rim (original)", "주미룩스 35 1세대 스틸림 (오리지널)", r"steel ?rim|스틸 ?림", [r"복각|re-?issue|2021"], ["steel rim", "스틸림", "1st steel rim"]),
    ("v1", "Summilux 35mm f/1.4 1st", "주미룩스 35 1세대", GEN1, [r"steel ?rim|스틸 ?림"], ["1st", "1세대"]),
    ("v2", "Summilux 35mm f/1.4 2nd (pre-ASPH)", "주미룩스 35 2세대", GEN2 + r"|pre-?asph", [], ["2nd", "2세대", "pre asph"]),
    ("aa", "Summilux-M 35mm f/1.4 Aspherical (AA, 1990)", "주미룩스 35 AA", r"aspherical|\bAA\b|더블 ?어스", [], ["aa", "aspherical", "double aspherical"]),
    ("asph-1994", "Summilux-M 35mm f/1.4 ASPH (1994, pre-FLE)", "주미룩스 35 ASPH (1994, FLE 이전)", r"ASPH.{0,40}(4세대|4th|non-?fle|11874|11883)|(4세대|4th|non-?fle).{0,40}ASPH", [r"FLE"], ["asph 1994", "asph 4세대", "asph non fle"]),
    ("asph-unspecified", "Summilux-M 35mm f/1.4 ASPH (version not stated)", "주미룩스 35 ASPH (버전 미표기)", r"ASPH", [r"FLE", r"aspherical|\bAA\b", r"4세대|4th|non-?fle", r"\bnew\b"], ["asph"]),
    ("pre-asph-unspecified", "Summilux 35mm f/1.4 pre-ASPH (generation not stated)", "주미룩스 35 구형 (세대 미표기)", r"^(?!.*(ASPH|aspherical|\bAA\b|FLE|1st|1th|2nd|1세대|2세대|steel|스틸|복각|reissue|titan|티탄|classic|클래식)).*$", [], ["pre asph"]),
    ("titan", "Summilux-M 35mm f/1.4 Titan", "주미룩스 35 티탄", r"titan|티탄", [], ["titan", "티탄"]),
    ("classic", "Summilux-M 35mm f/1.4 'Classic'", "주미룩스 35 클래식", r"classic|클래식", [], ["classic", "클래식"]),  # 확인 필요
    ("leitz-wetzlar", "Summilux-M 35mm f/1.4 ASPH 'Leitz Wetzlar'", "주미룩스 35 라이츠 베츨라", r"leitz ?wetzlar", [], ["leitz wetzlar"]),
    ("10-jahre", "Summilux-M 35mm f/1.4 ASPH '10 Jahre' Limited", "주미룩스 35 10주년 한정", r"10 ?jahre", [], ["10 jahre"]),  # 확인 필요
    ("korea-70", "Summilux-M 35mm f/1.4 ASPH 70th Independence Anniversary (Korea)", "주미룩스 35 광복 70주년", r"independence|광복", [], ["광복 70주년"]),
]:
    key = f"{SL35}:{slug}"
    nots = list(extra_not) + ([m for m in EDITION_35LUX if m != marker] if slug not in ("titan", "leitz-wetzlar", "10-jahre", "korea-70", "classic") else [])
    _add(key, name, ko, "M", [FAM["summilux"][0], f("35"), marker], nots, aliases("summilux", "35", sfx, "M"))
    EXTEND_PARENTS.setdefault(SL35, []).append(key)
for existing in ("asph-fle", "asph-fle2", "steel-rim-reissue"):
    TIGHTEN[f"{SL35}:{existing}"] = EDITION_35LUX + [r"aspherical|\bAA\b"]
OVERRIDE_MUST[f"{SL35}:asph-fle2"] = [FAM["summilux"][0], f("35"), r"FLE ?(II|2)\b|ASPH.{0,30}\bnew\b|\bnew\b.{0,30}ASPH"]
TIGHTEN[f"{SL35}:asph-fle"] = EDITION_35LUX + [r"aspherical|\bAA\b", r"\bnew\b"]

# ───────────── M: Summilux 50 (새 부모) ─────────────
group("leica:lens:summilux-m:50", "Summilux-M 50mm f/1.4", "주미룩스 50", "M", "summilux", "50", [
    c("v1", "Summilux 50mm f/1.4 1st", "주미룩스 50 1세대", GEN1, [], ["1st", "1세대"]),
    c("v2", "Summilux 50mm f/1.4 2nd", "주미룩스 50 2세대", GEN2, [], ["2nd", "2세대"]),
    c("v3", "Summilux-M 50mm f/1.4 3rd", "주미룩스 50 3세대", GEN3, [], ["3rd", "3세대"]),
    c("v4", "Summilux-M 50mm f/1.4 4th (E46, built-in hood)", "주미룩스 50 4세대", GEN4 + r"|E46", [], ["4th", "4세대", "e46"]),
    c("classic", "Summilux-M 50mm f/1.4 'Classic'", "주미룩스 50 클래식", r"classic|클래식", [], ["classic", "클래식"]),  # 확인 필요
    c("titan", "Summilux-M 50mm f/1.4 Titan", "주미룩스 50 티탄", r"titan|티탄", [], ["titan"]),
    c("millennium", "Summilux-M 50mm f/1.4 Millennium (Black Paint)", "주미룩스 50 밀레니엄", r"millenn?ium|밀레니엄", [], ["millennium", "밀레니엄"]),
    c("asph-lhsa", "Summilux-M 50mm f/1.4 ASPH LHSA", "주미룩스 50 ASPH LHSA", r"LHSA", [], ["asph lhsa", "lhsa"]),
    c("asph-kravitz", "Summilux-M 50mm f/1.4 ASPH Lenny Kravitz", "주미룩스 50 ASPH 레니 크라비츠", r"kravitz|lenny", [], ["lenny kravitz", "kravitz"]),
    c("korea-70", "Summilux-M 50mm f/1.4 70th Independence Anniversary (Korea)", "주미룩스 50 광복 70주년", r"independence|광복", [], ["광복 70주년"]),
], must_not=[r"\bSL\b", r"\bTL\b"], existing=["leica:lens:summilux-m:50:asph"])
TIGHTEN["leica:lens:summilux-m:50:asph"] = [r"LHSA", r"kravitz|lenny", r"titan|티탄", r"independence|광복", r"\bSL\b|-SL\b", r"\bTL\b|-TL\b", r"-R\b"]
# 세대 미표기 = ASPH도 세대도 없는 구형
MODELS["leica:lens:summilux-m:50:unspecified"]["title_must_not"].append(r"ASPH")

# ───────────── M: Summicron 35 (기존 부모에 추가) ─────────────
SC35 = "leica:lens:summicron-m:35"
for slug, name, ko, marker, extra_not, sfx in [
    ("v1-eyes", "Summicron 35mm f/2 1st (8 elements) with eyes (M3)", "주미크론 35 8매 안경(고글)", r"\beyes?\b|고글|goggle|안경", [], ["eye", "고글", "8 element eye"]),
    ("v2", "Summicron 35mm f/2 2nd", "주미크론 35 2세대", GEN2, [], ["2nd", "2세대"]),
    ("v3", "Summicron 35mm f/2 3rd (7 elements)", "주미크론 35 3세대 (7매)", GEN3 + r"|7 ?el|7매", [], ["3rd", "3세대", "7 element", "7매"]),
    ("millennium", "Summicron-M 35mm f/2 Millennium (Black Paint)", "주미크론 35 밀레니엄", r"millenn?ium|밀레니엄", [], ["millennium"]),
    ("ara-guler", "Summicron-M 35mm f/2 ASPH Ara Güler", "주미크론 35 아라 귈러", r"ara ?g[uü]ler", [], ["ara guler"]),
    ("your-mark", "Summicron-M 35mm f/2 'Your Mark'", "주미크론 35 유어마크", r"your ?mark", [], ["your mark"]),  # 확인 필요
    ("titan", "Summicron-M 35mm f/2 ASPH Titan", "주미크론 35 티탄", r"titan|티탄", [], ["titan"]),
    ("unspecified", "Summicron 35mm f/2 pre-ASPH (generation not stated)", "주미크론 35 구형 (세대 미표기)",
     r"^(?!.*(ASPH|APO|1st|2nd|3rd|3th|4th|1세대|2세대|3세대|4세대|5세대|8 ?el|8매|7 ?el|7매|6매|6 ?el|eye|고글|현행|millenn|titan|ara ?g|your ?mark)).*$", [], [""]),
]:
    key = f"{SC35}:{slug}"
    _add(key, name, ko, "M", [FAM["summicron"][0], f("35"), marker], [r"\bAPO\b"] + list(extra_not), aliases("summicron", "35", sfx, "M"))
    EXTEND_PARENTS.setdefault(SC35, []).append(key)
TIGHTEN[f"{SC35}:v1-8element"] = [r"\beyes?\b|고글|goggle|안경"]
TIGHTEN[f"{SC35}:asph"] = [r"millenn?ium|밀레니엄", r"ara ?g[uü]ler", r"your ?mark", r"titan|티탄", r"\bSL\b|-SL\b", r"\bTL\b"]
OVERRIDE_MUST[f"{SC35}:asph"] = [FAM["summicron"][0], f("35"), r"ASPH|5세대|현행"]

# ───────────── M: Summicron 50 (기존 부모에 추가) ─────────────
SC50 = "leica:lens:summicron:50"
for slug, name, ko, marker, mount, extra_not, sfx in [
    ("collapsible", "Summicron 50mm f/2 Collapsible (L · M)", "주미크론 50 침동", r"collaps|침동|토륨|thorium|radioactive", None, [], ["collapsible", "침동", "토륨"]),
    ("rigid-early", "Summicron 50mm f/2 Rigid 1st (early)", "주미크론 50 리짓 전기형", r"(rigid|리짓|리지드).{0,20}(전기|early|1st)|(전기|early).{0,20}(rigid|리짓)", None, [], ["rigid early", "리짓 전기형"]),
    ("rigid-late", "Summicron 50mm f/2 Rigid 2nd (late)", "주미크론 50 리짓 후기형", r"(rigid|리짓|리지드).{0,20}(후기|late|2nd)|(후기|late).{0,20}(rigid|리짓)", None, [], ["rigid late", "리짓 후기형"]),
    ("v3", "Summicron-M 50mm f/2 3rd", "주미크론 50 3세대", GEN3, "M", [], ["3rd", "3세대"]),
    ("50-jahre", "Summicron-M 50mm f/2 '50 Jahre'", "주미크론 50 50주년", r"50 ?jahre", "M", [], ["50 jahre"]),
]:
    key = f"{SC50}:{slug}"
    _add(key, name, ko, mount, [FAM["summicron"][0], f("50"), marker], [r"\bAPO\b", r"\bSL\b|-SL\b", r"-R\b|\bR ?50"] + list(extra_not), aliases("summicron", "50", sfx, None))
    EXTEND_PARENTS.setdefault(SC50, []).append(key)
TIGHTEN["leica:lens:summicron:50:rigid"] = [r"전기|early|후기|late|1st|2nd"]
TIGHTEN["leica:lens:summicron-m:50:current"] = [GEN3, r"50 ?jahre", r"토륨|thorium"]

# ───────────── M: Elmarit 28 (새 부모, 기존 ASPH 포함) ─────────────
group("leica:lens:elmarit-m:28", "Elmarit-M 28mm f/2.8", "엘마리트 28", "M", "elmarit", "28", [
    c("v1", "Elmarit 28mm f/2.8 1st (Canada, 1965)", "엘마리트 28 1세대", GEN1, [], ["1st", "1세대"]),
    c("v2", "Elmarit-M 28mm f/2.8 2nd", "엘마리트 28 2세대", GEN2, [], ["2nd", "2세대"]),
    c("v3", "Elmarit-M 28mm f/2.8 3rd", "엘마리트 28 3세대", GEN3, [], ["3rd", "3세대"]),
    c("v4", "Elmarit-M 28mm f/2.8 4th", "엘마리트 28 4세대", GEN4, [], ["4th", "4세대"]),
], must_not=[r"\bR\b|-R\b", r"ASPH"], existing=["leica:lens:elmarit-m:28:asph"])
# ───────────── M: 90mm f/2.8 ─────────────
group("leica:lens:elmarit-m:90", "Elmarit-M 90mm f/2.8", "엘마리트 90", "M", "elmarit", "90", [
    c("v1", "Elmarit 90mm f/2.8 1st", "엘마리트 90 1세대", GEN1, [], ["1st"]),
    c("v2", "Elmarit-M 90mm f/2.8 2nd", "엘마리트 90 2세대", GEN2, [], ["2nd"]),
], must_not=[r"tele", r"\bR\b|-R\b", r"APO", r"macro"])
group("leica:lens:tele-elmarit-m:90", "Tele-Elmarit 90mm f/2.8", "텔레엘마리트 90", "M", "tele-elmarit", "90", [
    c("fat", "Tele-Elmarit 90mm f/2.8 (fat, 1964)", "텔레엘마리트 90 팻", r"\bfat\b|팻|뚱", [], ["fat"]),
    c("thin", "Tele-Elmarit-M 90mm f/2.8 (thin, 1974)", "텔레엘마리트 90 씬", r"\bthin\b|씬|슬림", [], ["thin"]),
])
# ───────────── M: 그 밖 (단일 모델) ─────────────
lens("leica:lens:elmarit-m:21", "Elmarit-M 21mm f/2.8 (pre-ASPH)", "엘마리트 21", "M", "elmarit", "21", must_not=[r"ASPH"])
lens("leica:lens:elmarit-m:21:asph", "Elmarit-M 21mm f/2.8 ASPH", "엘마리트 21 ASPH", "M", "elmarit", "21", [r"ASPH"], suffixes=("asph",))
lens("leica:lens:elmarit-m:24:asph", "Elmarit-M 24mm f/2.8 ASPH", "엘마리트 24", "M", "elmarit", "24")
lens("leica:lens:elmarit-m:135", "Elmarit-M 135mm f/2.8 (with eyes)", "엘마리트 135", "M", "elmarit", "135")
lens("leica:lens:summilux-m:21", "Summilux-M 21mm f/1.4 ASPH", "주미룩스 21", "M", "summilux", "21")
lens("leica:lens:summilux-m:24", "Summilux-M 24mm f/1.4 ASPH", "주미룩스 24", "M", "summilux", "24")
lens("leica:lens:summilux-m:28", "Summilux-M 28mm f/1.4 ASPH", "주미룩스 28", "M", "summilux", "28")
lens("leica:lens:summilux-m:90", "Summilux-M 90mm f/1.5 ASPH", "주미룩스 90", "M", "summilux", "90")
lens("leica:lens:apo-summicron-m:75", "APO-Summicron-M 75mm f/2 ASPH", "아포 주미크론 75", "M", "summicron", "75", [r"\bAPO\b|apo-"], suffixes=("apo",),
     extra_aliases=["apo summicron 75", "apo 75 cron", "75 cron", "아포 주미크론 75"])
lens("leica:lens:apo-summicron-m:90", "APO-Summicron-M 90mm f/2 ASPH", "아포 주미크론 90", "M", "summicron", "90", [r"\bAPO\b|apo-"], suffixes=("apo",),
     extra_aliases=["apo summicron 90", "apo 90 cron", "아포 주미크론 90"])
TIGHTEN["leica:lens:summicron-m:90"] = [r"\bAPO\b|apo-"]
for focal in ("35", "50", "75", "90"):
    group(f"leica:lens:summarit-m:{focal}", f"Summarit-M {focal}mm", f"즈마릿 {focal}", "M", "summarit", focal, [
        c("f2.5", f"Summarit-M {focal}mm f/2.5", f"즈마릿 {focal} f/2.5", r"2\.5", [], ["2.5"]),
        c("f2.4", f"Summarit-M {focal}mm f/2.4", f"즈마릿 {focal} f/2.4", r"2\.4", [], ["2.4"]),
    ], must_not=[r"1\.5"] if focal == "50" else [])
lens("leica:lens:summarit:50:f1.5", "Summarit 50mm f/1.5 (screw mount, 1949)", "즈마릿 50 f/1.5", None, "summarit", "50", [r"1\.5"], suffixes=("1.5",))
group("leica:lens:summaron-m:28:f5.6", "Summaron 28mm f/5.6", "즈마론 28", None, "summaron", "28", [
    c("original", "Summaron 28mm f/5.6 (original, L)", "즈마론 28 오리지널", r"오리지널|original|\bL ?28|LTM|M39|screw", [], ["original"]),
    c("reissue", "Summaron-M 28mm f/5.6 (2016 reissue)", "즈마론 28 복각", r"복각|re-?issue|summaron-m|\bM ?28|6 ?bit|신품", [], ["reissue", "복각"]),
], unspecified=True)
group("leica:lens:summaron:35", "Summaron 35mm", "즈마론 35", None, "summaron", "35", [
    c("f3.5", "Summaron 35mm f/3.5", "즈마론 35 f/3.5", r"3\.5", [r"\beyes?\b|고글"], ["3.5"]),
    c("f3.5-eyes", "Summaron 35mm f/3.5 with eyes (M3)", "즈마론 35 f/3.5 고글", r"3\.5.{0,40}(\beyes?\b|고글)|(\beyes?\b|고글).{0,40}3\.5", [], ["3.5 eye"]),
    c("f2.8", "Summaron 35mm f/2.8", "즈마론 35 f/2.8", r"2\.8", [r"\beyes?\b|고글"], ["2.8"]),
    c("f2.8-eyes", "Summaron 35mm f/2.8 with eyes (M3)", "즈마론 35 f/2.8 고글", r"2\.8.{0,40}(\beyes?\b|고글)|(\beyes?\b|고글).{0,40}2\.8", [], ["2.8 eye"]),
])
lens("leica:lens:super-elmar-m:18", "Super-Elmar-M 18mm f/3.8 ASPH", "수퍼엘마 18", "M", "super-elmar", "18")
group("leica:lens:tri-elmar-m:28-35-50", "Tri-Elmar-M 28-35-50mm f/4 (MATE)", "트라이엘마 28-35-50", "M", "tri-elmar", "28-35-50", [
    c("e49", "Tri-Elmar-M 28-35-50 E49 (1st)", "트라이엘마 28-35-50 E49", r"E49|1st|1세대|구형", [], ["e49"]),
    c("e46", "Tri-Elmar-M 28-35-50 ASPH E46 (2nd)", "트라이엘마 28-35-50 E46", r"E46|ASPH|2nd|2세대|신형", [], ["e46", "asph"]),
], parent_aliases=["mate", "메이트"])
group("leica:lens:super-angulon:21", "Super-Angulon 21mm", "슈퍼앵귤론 21", "M", "super-angulon", "21", [
    c("f4", "Super-Angulon 21mm f/4", "슈퍼앵귤론 21 f/4", r"(?<![\d.])4\b|f/?4\b", [r"3\.4"], ["f4"]),
    c("f3.4", "Super-Angulon-M 21mm f/3.4", "슈퍼앵귤론 21 f/3.4", r"3\.4", [], ["3.4"]),
], must_not=[r"\bR\b|-R\b"])
lens("leica:lens:elmar:24:asph", "Elmar-M 24mm f/3.8 ASPH", "엘마 24", "M", "elmar", "24")
group("leica:lens:elmar:50:f3.5", "Elmar 50mm f/3.5", "엘마 50 f/3.5", None, "elmar", "50", [
    c("nickel", "Elmar 50mm f/3.5 Nickel", "엘마 50 니켈", r"nickel|니켈", [], ["nickel", "니켈"]),
    c("red-scale", "Elmar 50mm f/3.5 Red Scale", "엘마 50 레드스케일", r"red|레드", [], ["red scale"]),
    c("m-mount", "Elmar 50mm f/3.5 (M mount)", "엘마 50 f/3.5 M", r"\bM ?50|elmar-?m|\bM\b ?마운트", [], ["m"]),
], extra_must=[r"3\.5"], must_not=[r"2\.8", r"\b65\b"])
lens("leica:lens:elmar:35", "Elmar 35mm f/3.5", "엘마 35", None, "elmar", "35", must_not=[r"\bAPO\b"])
group("leica:lens:elmar:90", "Elmar 90mm f/4", "엘마 90", None, "elmar", "90", [
    c("collapsible", "Elmar 90mm f/4 Collapsible", "엘마 90 침동", r"collaps|침동", [], ["collapsible", "침동"]),
    c("3-element", "Elmar 90mm f/4 3-element (rigid)", "엘마 90 3매", r"3 ?el|3매", [], ["3 element"]),
], must_not=[r"macro|tele|elmarit|-C\b|elmar ?c\b"])
lens("leica:lens:elmar:65", "Elmar 65mm f/3.5 (Visoflex)", "엘마 65", None, "elmar", "65")
lens("leica:lens:elmar:135", "Elmar 135mm f/4", "엘마 135", None, "elmar", "135", must_not=[r"tele"])
lens("leica:lens:macro-elmar-m:90", "Macro-Elmar-M 90mm f/4", "매크로 엘마 90", "M", "macro-elmar", "90")
lens("leica:lens:apo-telyt-m:135", "APO-Telyt-M 135mm f/3.4", "아포 텔리트 135", "M", "apo-telyt", "135")
lens("leica:lens:tele-elmar-m:135", "Tele-Elmar-M 135mm f/4", "텔레엘마 135", "M", "tele-elmar", "135")
lens("leica:lens:telyt:visoflex", "Telyt (Visoflex) 200 · 280 · 400 · 560", "텔리트 (비조플렉스)", None, "telyt", "", [r"\b(200|280|400|560)\b"], must_not=[r"apo|-R\b|\bR\b"],
     extra_aliases=["telyt 200", "telyt 280", "telyt 400", "telyt 560"])
lens("leica:lens:summitar:50", "Summitar 50mm f/2", "즈미타 50", None, "summitar", "50")
lens("leica:lens:summar:50", "Summar 50mm f/2", "주마 50", None, "summar", "50")
lens("leica:lens:summarex:85", "Summarex 85mm f/1.5", "주마렉스 85", None, "summarex", "85")
lens("leica:lens:xenon:50", "Xenon 50mm f/1.5", "제논 50", None, "xenon", "50")
for focal, ap in (("28", "6.3"), ("50", "2.5"), ("73", "1.9"), ("125", "2.5"), ("135", "4.5")):
    lens(f"leica:lens:hektor:{focal}", f"Hektor {focal}mm f/{ap}", f"헥토르 {focal}", None, "hektor", focal)
group("leica:lens:thambar:90", "Thambar 90mm f/2.2", "탐바 90", None, "thambar", "90", [
    c("original", "Thambar 90mm f/2.2 (original, 1935)", "탐바 90 오리지널", r"오리지널|original|1935|\bL\b|LTM", [r"복각|re-?issue|thambar-m"], ["original"]),
    c("reissue", "Thambar-M 90mm f/2.2 (2017 reissue)", "탐바 90 복각", r"복각|re-?issue|thambar-m|신품|2017", [], ["reissue", "복각"]),
])
lens("leica:lens:hologon:15", "Hologon 15mm f/8", "홀로곤 15", "M", "hologon", "15")
lens("leica:lens:summicron-c:40", "Summicron-C 40mm f/2 (CL)", "주미크론 C 40", None, "summicron", "40", must_not=[r"\bSL\b", r"\bR\b"],
     extra_aliases=["summicron c 40", "40 cron", "주미크론 40"])
lens("leica:lens:elmar-c:90", "Elmar-C 90mm f/4 (CL)", "엘마 C 90", None, "elmar-c", "90")

# ───────────── SL ─────────────
lens("leica:lens:vario-elmarit-sl:24-70", "Vario-Elmarit-SL 24-70mm f/2.8 ASPH", "SL 24-70", "SL", "vario-elmarit", "24-70", extra_aliases=["sl 24-70", "24-70 sl"])
lens("leica:lens:apo-vario-elmarit-sl:90-280", "APO-Vario-Elmarit-SL 90-280mm f/2.8-4", "SL 90-280", "SL", "vario-elmarit", "90-280", extra_aliases=["sl 90-280", "90-280"])
lens("leica:lens:super-vario-elmar-sl:16-35", "Super-Vario-Elmar-SL 16-35mm f/3.5-4.5 ASPH", "SL 16-35", "SL", "vario-elmar", "16-35", extra_aliases=["sl 16-35", "16-35 sl"])
lens("leica:lens:super-vario-elmarit-sl:14-24", "Super-Vario-Elmarit-SL 14-24mm f/2.8 ASPH", "SL 14-24", "SL", "vario-elmarit", "14-24", extra_aliases=["sl 14-24"])
lens("leica:lens:vario-elmar-sl:100-400", "Vario-Elmar-SL 100-400mm f/5-6.3", "SL 100-400", "SL", "vario-elmar", "100-400", extra_aliases=["sl 100-400"])
for focal in ("21", "28", "50", "75", "90"):
    lens(f"leica:lens:apo-summicron-sl:{focal}", f"APO-Summicron-SL {focal}mm f/2 ASPH", f"아포 주미크론 SL {focal}", "SL", "summicron", focal, [r"\bAPO\b|apo-"], suffixes=("apo",),
         extra_aliases=[f"apo summicron sl {focal}", f"sl {focal} apo", f"아포 주미크론 sl {focal}"])
lens("leica:lens:summilux-sl:50", "Summilux-SL 50mm f/1.4 ASPH", "주미룩스 SL 50", "SL", "summilux", "50")
for focal in ("28", "35", "50"):
    lens(f"leica:lens:summicron-sl:{focal}", f"Summicron-SL {focal}mm f/2 ASPH (2024)", f"주미크론 SL {focal}", "SL", "summicron", focal, must_not=[r"\bAPO\b|apo-"])
TIGHTEN["leica:lens:apo-summicron-sl:35"] = []
# ───────────── TL ─────────────
lens("leica:lens:summilux-tl:35", "Summilux-TL 35mm f/1.4 ASPH", "주미룩스 TL 35", "TL", "summilux", "35")
lens("leica:lens:summicron-tl:23", "Summicron-TL 23mm f/2 ASPH", "주미크론 TL 23", "TL", "summicron", "23")
lens("leica:lens:elmarit-tl:18", "Elmarit-TL 18mm f/2.8 ASPH", "엘마리트 TL 18", "TL", "elmarit", "18")
lens("leica:lens:apo-macro-elmarit-tl:60", "APO-Macro-Elmarit-TL 60mm f/2.8 ASPH", "TL 60 매크로", "TL", "macro-elmarit", "60")
lens("leica:lens:super-vario-elmar-tl:11-23", "Super-Vario-Elmar-TL 11-23mm f/3.5-4.5 ASPH", "TL 11-23", "TL", "vario-elmar", "11-23", extra_aliases=["tl 11-23"])
lens("leica:lens:vario-elmar-tl:18-56", "Vario-Elmar-TL 18-56mm f/3.5-5.6 ASPH", "TL 18-56", "TL", "vario-elmar", "18-56", extra_aliases=["tl 18-56"])
lens("leica:lens:apo-vario-elmar-tl:55-135", "APO-Vario-Elmar-TL 55-135mm f/3.5-4.5", "TL 55-135", "TL", "vario-elmar", "55-135", extra_aliases=["tl 55-135"])
# ───────────── R ─────────────
lens("leica:lens:summilux-r:35", "Summilux-R 35mm f/1.4", "주미룩스 R 35", "R", "summilux", "35")
group("leica:lens:summilux-r:50", "Summilux-R 50mm f/1.4", "주미룩스 R 50", "R", "summilux", "50", [
    c("v1", "Summilux-R 50mm f/1.4 1st (E55)", "주미룩스 R 50 1세대", GEN1 + r"|E55", [], ["1st", "e55"]),
    c("v2", "Summilux-R 50mm f/1.4 2nd (E60)", "주미룩스 R 50 2세대", GEN2 + r"|E60", [], ["2nd", "e60"]),
])
lens("leica:lens:summicron-r:35", "Summicron-R 35mm f/2", "주미크론 R 35", "R", "summicron", "35")
lens("leica:lens:summicron-r:90", "Summicron-R 90mm f/2", "주미크론 R 90", "R", "summicron", "90", must_not=[r"APO"])
for focal in ("19", "24", "28", "35", "90", "135", "180"):
    lens(f"leica:lens:elmarit-r:{focal}", f"Elmarit-R {focal}mm", f"엘마리트 R {focal}", "R", "elmarit", focal, must_not=[r"apo|macro|vario|fish|tele"])
lens("leica:lens:macro-elmarit-r:60", "Macro-Elmarit-R 60mm f/2.8", "매크로 엘마리트 R 60", "R", "macro-elmarit", "60", must_not=[r"\bapo\b"])
lens("leica:lens:apo-macro-elmarit-r:100", "APO-Macro-Elmarit-R 100mm f/2.8", "아포 매크로 엘마리트 R 100", "R", "apo-macro-elmarit", "100")
lens("leica:lens:elmarit-r:100", "Macro-Elmar-R 100mm f/4 · Elmar-R 100", "엘마 R 100", "R", "elmar", "100")
lens("leica:lens:apo-summicron-r:180", "APO-Summicron-R 180mm f/2", "아포 주미크론 R 180", "R", "summicron", "180", [r"\bAPO\b|apo-"])
lens("leica:lens:apo-elmarit-r:180", "APO-Elmarit-R 180mm f/2.8", "아포 엘마리트 R 180", "R", "apo-elmarit", "180")
lens("leica:lens:apo-telyt-r:280", "APO-Telyt-R 280mm f/4 · f/2.8", "아포 텔리트 R 280", "R", "apo-telyt", "280")
lens("leica:lens:telyt-r:long", "Telyt-R 250 · 350 · 400 · 560 · 800", "텔리트 R 장망원", "R", "telyt", "", [r"\b(250|350|400|560|800)\b"], must_not=[r"\bapo\b"])
for zoom in ("21-35", "28-70", "35-70", "70-210", "80-200", "105-280"):
    lens(f"leica:lens:vario-elmar-r:{zoom}", f"Vario-Elmar-R {zoom}mm", f"바리오 엘마 R {zoom}", "R", "vario-elmar", zoom, extra_aliases=[f"r {zoom}", f"{zoom} r"])
for zoom in ("28-90", "35-70"):
    lens(f"leica:lens:vario-elmarit-r:{zoom}", f"Vario-Elmarit-R {zoom}mm", f"바리오 엘마리트 R {zoom}", "R", "vario-elmarit", zoom, must_not=[r"\bapo\b"], extra_aliases=[f"r {zoom} elmarit"])
lens("leica:lens:apo-vario-elmarit-r:70-180", "APO-Vario-Elmarit-R 70-180mm f/2.8", "아포 바리오 엘마리트 R 70-180", "R", "apo-vario-elmarit", "70-180", extra_aliases=["r 70-180"])
lens("leica:lens:super-angulon-r:21", "Super-Angulon-R 21mm", "슈퍼앵귤론 R 21", "R", "super-angulon", "21")
lens("leica:lens:super-angulon-r:28", "PC-Super-Angulon-R 28mm f/2.8", "PC 슈퍼앵귤론 R 28", "R", "super-angulon", "28")
lens("leica:lens:fisheye-elmarit-r:16", "Fisheye-Elmarit-R 16mm f/2.8", "어안 엘마리트 R 16", "R", "fisheye-elmarit", "16")
# ───────────── S (중형) ─────────────
for key, name, fam, focal in (("summarit-s:35", "Summarit-S 35mm f/2.5", "summarit", "35"), ("summarit-s:70", "Summarit-S 70mm f/2.5", "summarit", "70"),
                              ("elmarit-s:30", "Elmarit-S 30mm f/2.8", "elmarit", "30"), ("elmarit-s:45", "Elmarit-S 45mm f/2.8", "elmarit", "45"),
                              ("summicron-s:100", "Summicron-S 100mm f/2", "summicron", "100"), ("apo-macro-summarit-s:120", "APO-Macro-Summarit-S 120mm f/2.5", "apo-macro-summarit", "120"),
                              ("apo-elmar-s:180", "APO-Elmar-S 180mm f/3.5", "apo-elmar", "180"), ("super-elmar-s:24", "Super-Elmar-S 24mm f/3.5", "super-elmar", "24"),
                              ("vario-elmar-s:30-90", "Vario-Elmar-S 30-90mm f/3.5-5.6", "vario-elmar", "30-90")):
    lens(f"leica:lens:{key}", name, None, "S", fam, focal)

# 35/1.4 '복각'은 스틸림 복각 하나뿐 (제목에 스틸림이 없어도)
OVERRIDE_MUST["leica:lens:summilux-m:35:steel-rim-reissue"] = [FAM["summilux"][0], f("35"), r"(steel ?rim|스틸 ?림).{0,40}(re-?issue|복각|2021)|(re-?issue|복각|2021)"]
TIGHTEN["leica:lens:summilux-m:35:steel-rim-reissue"] = [r"ASPH|FLE"]
# Noctilux 0.95 광복 70주년 (한국 기념판)
_add("leica:lens:noctilux-m:50:f0.95-korea-70", "Noctilux-M 50mm f/0.95 70th Independence Anniversary (Korea)", "녹티룩스 0.95 광복 70주년", "M",
     [r"nocti", r"0\.95", r"independence|광복"], [], ["noctilux 0.95 광복 70주년", "녹티룩스 0.95 광복"])
EXTEND_PARENTS.setdefault("leica:lens:noctilux-m:50", []).append("leica:lens:noctilux-m:50:f0.95-korea-70")
TIGHTEN["leica:lens:noctilux-m:50:f0.95"] = [r"independence|광복"]

# ───────────── M: Noctilux 50 f/1.0 (세대 부모) ─────────────
# 국내 표기: 1세대 = f/1.2 오리지널(1966), 2세대 = f/1.0 E58(1976–), 3세대 = f/1.0 E60 분리 후드(1982–), 4세대 = f/1.0 E60 후드 내장(1993–2008, 말기 6bit).
# 시리얼(sn.xxxx = 앞 네 자리): E58은 ~2,92만대까지, 후드 내장은 ~3,60만대부터 → 경계 구간(300만~370만)은 세대 미표기로 둔다.
NX10 = "leica:lens:noctilux-m:50:f1.0"
NX10_BASE = [r"nocti", r"((?<![\d.])1\.0\b|/1\b(?!\.\d)|f/?1\b(?!\.[1-9])|E60|E58)"]
NX10_NOT = [r"0\.95", r"1\.2", r"1\.25", r"\b75\b", f("35")]
SN = r"(?:sn|s/n|no|#)\.?\s?#?"
NX10_GEN = {
    "v2-e58": ("Noctilux 50mm f/1.0 E58 (2nd gen, 1976)", "녹티룩스 50 f/1.0 2세대 (E58)",
               rf"E58|2세대|\b(1st|v\.?1|version ?1)\b|{SN}2[,.]?\d{{3}}\b", ["e58", "2세대", "2nd gen", "v1"]),
    "v3-e60": ("Noctilux-M 50mm f/1.0 E60 separate hood (3rd gen, 1982)", "녹티룩스 50 f/1.0 3세대 (E60 분리 후드)",
               r"3세대", ["3세대", "3rd gen", "e60 3세대", "e60 분리 후드"]),
    "v4-builtin-hood": ("Noctilux-M 50mm f/1.0 E60 built-in hood (4th gen, 1993–2008)", "녹티룩스 50 f/1.0 4세대 (후드 내장)",
                        rf"4세대|6 ?[bp]it|{SN}3[,.]?[7-9]\d{{2}}\b", ["4세대", "4th gen", "6bit", "후드 내장", "built in hood", "e60 4세대", "e60 후드 내장"]),
}
_nx_kids = []
for slug, (name, ko, marker, sfx) in NX10_GEN.items():
    others = [m for s2, (_, _, m, _) in NX10_GEN.items() if s2 != slug]
    key = f"{NX10}:{slug}"
    als = [f"{n} {s}" for n in ("noctilux 1.0", "nocti 1.0", "녹티룩스 1.0", "녹티 1.0") for s in sfx]
    _add(key, name, ko, "M", NX10_BASE + [marker], NX10_NOT + others, als)
    _nx_kids.append(key)
_add(f"{NX10}:unspecified", "Noctilux-M 50mm f/1.0 (generation not stated)", "녹티룩스 50 f/1.0 (세대 미표기)", "M",
     NX10_BASE, NX10_NOT + [m for (_, _, m, _) in NX10_GEN.values()], ["noctilux 1.0 세대 미표기", "녹티룩스 1.0 세대 미표기"])
PARENTS[NX10] = ("Noctilux-M 50mm f/1.0 (all)", "Lens", "M", _nx_kids + [f"{NX10}:unspecified"],
                 ["noctilux-m 50 1.0", "noctilux 1.0", "nocti 1.0", "nocti e60", "noctilux e60", "녹티 e60", "noctilux 50 1.0", "녹티룩스 1.0", "녹티 1.0", "녹티룩스 50 1.0"],
                 "녹티룩스 50 f/1.0 (전체)")
