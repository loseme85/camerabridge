"""라이카 바디 엔티티 (계열 · 기본형 · 기념판/콜라보).

fam()으로 한 계열을 정의한다.
  - 기념판·콜라보·파생형(variants)이 있으면: 부모(계열 전체) + 자식(기본형 + 각 변형)
  - 없으면: 단일 엔티티
기본형은 변형의 구분 단어가 있는 매물은 받지 않는다 (예: M7 기본형 ← "M7 Titan" 제외).
오리지널 블랙페인트 같은 공장 변형은 엔티티, 비공식 리페인트는 제외한다.
"확인 필요" 주석이 붙은 항목은 공식 자료로 연도·이름을 다시 확인해야 한다.
"""
from __future__ import annotations

MODELS: dict[str, dict] = {}
PARENTS: dict[str, tuple] = {}
ALIASES: dict[str, list[str]] = {}
NAME_KO: dict[str, str] = {}

REPAINT = r"re-?paint|리페인트|재도색|custom|커스텀"
BLACK_PAINT = (r"black ?paint|블랙 ?페인트|블페", [REPAINT])


def _short(name: str) -> str:
    return name.replace("Leica ", "").strip()


def _auto_aliases(short: str, extra=()) -> list[str]:
    s = short.lower()
    base = {s, f"leica {s}", f"라이카 {s}"}
    compact = s.replace(" ", "").replace("-", "")
    if compact != s:
        base.add(compact)
    return sorted(base | {a.lower() for a in extra})


def fam(key, name, ko, mount, must, must_not=(), aliases=(), variants=(), standard_name=None):
    """variants: (slug, 이름, 한국어 이름, [추가로 꼭 있어야 할 말], [추가 제외], [별칭])"""
    short = _short(name)
    if not variants:
        MODELS[key] = {"model_key": key, "display_name": name, "category": "Body", "mount": mount,
                       "title_must": list(must), "title_must_not": list(must_not)}
        ALIASES[key] = _auto_aliases(short, aliases)
        if ko:
            NAME_KO[key] = ko
        return
    children = []
    variant_markers = [v[3][0] for v in variants]
    std = f"{key}:standard"
    MODELS[std] = {"model_key": std, "display_name": standard_name or f"{name} (standard)", "category": "Body", "mount": mount,
                   "title_must": list(must), "title_must_not": list(must_not) + variant_markers}
    ALIASES[std] = [f"{short.lower()} standard", f"{short.lower()} 기본"]
    NAME_KO[std] = f"{ko or name} 기본형"
    children.append(std)
    for slug, vname, vko, vmust, vnot, valiases in variants:
        vk = f"{key}:{slug}"
        MODELS[vk] = {"model_key": vk, "display_name": vname, "category": "Body", "mount": mount,
                      "title_must": list(must) + list(vmust), "title_must_not": list(must_not) + list(vnot)}
        ALIASES[vk] = _auto_aliases(_short(vname), valiases)
        if vko:
            NAME_KO[vk] = vko
        children.append(vk)
    PARENTS[key] = (f"{name} (all)", "Body", mount, children, _auto_aliases(short, aliases), f"{ko or name} (전체)")


def v(slug, name, ko, marker, aliases=(), extra_not=()):
    return (slug, name, ko, [marker], list(extra_not), list(aliases))


BP = lambda base: v("black-paint", f"{base} Black Paint", f"{base} 블랙페인트", BLACK_PAINT[0], [f"{base.lower()} black paint", f"{base.lower()} 블랙페인트"], BLACK_PAINT[1])  # noqa: E731

# ── M 필름 바디 ──
fam("leica:body:m3", "Leica M3", "라이카 M3", "M", [r"\bM ?3\b"], [r"M3 ?J", r"MP ?3"], ["엠3"], [
    v("double-stroke", "Leica M3 Double Stroke", "M3 더블스트로크", r"double ?stroke|더블 ?스트로크|\bDS\b", ["m3 ds", "m3 더블"]),
    v("single-stroke", "Leica M3 Single Stroke", "M3 싱글스트로크", r"single ?stroke|싱글 ?스트로크|\bSS\b", ["m3 ss", "m3 싱글"]),
    BP("M3"),
    v("olive", "Leica M3 Olive", "M3 올리브", r"olive|올리브", ["m3 olive"], [REPAINT]),
])
fam("leica:body:m3j", "Leica M3J", "라이카 M3J", "M", [r"M3 ?J\b"])
fam("leica:body:m2", "Leica M2", "라이카 M2", "M", [r"\bM ?2\b"], [r"M2-?R", r"\bM ?24\d", r"M ?2 ?\d{2}"], ["엠2"], [
    BP("M2"),
    v("button-rewind", "Leica M2 Button Rewind", "M2 버튼 리와인드", r"button|버튼", ["m2 button rewind"]),
])
fam("leica:body:m2-r", "Leica M2-R", "라이카 M2-R", "M", [r"M2-?R\b"])
fam("leica:body:m1", "Leica M1", "라이카 M1", "M", [r"\bM1\b(?![\d.:])"], [r"M1[0-9]"])
fam("leica:body:md", "Leica MD · MDa · MD-2", "라이카 MD", "M", [r"\bMD(a|-?2)?\b"], [r"M-D"], ["mda", "md-2", "md2"])
fam("leica:body:m4", "Leica M4", "라이카 M4", "M", [r"\bM ?4\b(?!-)"], [], ["엠4"], [
    BP("M4"),
    v("50-jahre", "Leica M4 50 Jahre (Black Chrome)", "M4 50주년", r"50 ?jahre|50 ?years|50th|anniversary|black ?chrome", ["m4 50 jahre", "m4 50th anniversary"]),
    v("olive", "Leica M4 Olive", "M4 올리브", r"olive|올리브", [], [REPAINT]),
])
fam("leica:body:m4-2", "Leica M4-2", "라이카 M4-2", "M", [r"\bM ?4-2\b"], [], ["m42"], [
    v("gold", "Leica M4-2 Gold (Oskar Barnack 100 Jahre)", "M4-2 골드", r"gold|골드", ["m4-2 gold"]),  # 확인 필요
])
fam("leica:body:m4-p", "Leica M4-P", "라이카 M4-P", "M", [r"\bM ?4-?P\b"], [], ["m4p"], [
    v("70-jahre", "Leica M4-P 70 Jahre (1913–1983)", "M4-P 70주년", r"70 ?jahre|1913|70th", ["m4-p 70 jahre"]),
    v("everest", "Leica M4-P Everest '82", "M4-P 에베레스트", r"everest|에베레스트", ["m4-p everest"]),
])
fam("leica:body:m5", "Leica M5", "라이카 M5", "M", [r"\bM ?5\b"], [], ["엠5"], [
    v("50-jahre", "Leica M5 50 Jahre", "M5 50주년", r"50 ?jahre", ["m5 50 jahre"]),
])
fam("leica:body:cl-film", "Leica CL (1973, film)", "라이카 CL (필름)", "M",
    [r"\bCL\b", r"(leitz|minolta|50 ?jahre|summicron-?c|40\s?mm|film|필름|1973)"], [r"\bTL\b|\bSL\b"], ["leitz cl", "minolta cl", "cl film", "cl 필름"])
# M6: 클래식·TTL·리이슈 + 기념판 (모두 M6 부모의 자식)
M6_MARKERS = [r"TTL", r"re-?issue|리이슈|복각|2022", r"M6 ?J\b", r"titan|티탄", r"platin|플래티넘", r"LHSA", r"royal|로얄",
              r"jaguar|재규어", r"millenn?ium|밀레니엄"]
MODELS["leica:body:m6:classic"] = {"model_key": "leica:body:m6:classic", "display_name": "Leica M6 (Classic)", "category": "Body", "mount": "M",
                                   "title_must": [r"\bM ?6\b"], "title_must_not": M6_MARKERS}
ALIASES["leica:body:m6:classic"] = ["leica m6 classic", "m6 classic", "m6 클래식", "라이카 m6 클래식", "엠6 클래식"]
NAME_KO["leica:body:m6:classic"] = "라이카 M6 클래식"
MODELS["leica:body:m6:ttl"] = {"model_key": "leica:body:m6:ttl", "display_name": "Leica M6 TTL", "category": "Body", "mount": "M",
                               "title_must": [r"\bM ?6\b", r"TTL"], "title_must_not": [r"millenn?ium|밀레니엄", r"LHSA"]}
ALIASES["leica:body:m6:ttl"] = ["leica m6 ttl", "m6 ttl", "m6ttl", "라이카 m6 ttl", "엠6 ttl"]
NAME_KO["leica:body:m6:ttl"] = "라이카 M6 TTL"
MODELS["leica:body:m6:reissue"] = {"model_key": "leica:body:m6:reissue", "display_name": "Leica M6 (2022 Reissue)", "category": "Body", "mount": "M",
                                   "title_must": [r"\bM ?6\b", r"(re-?issue|리이슈|2022|복각)"], "title_must_not": [r"TTL"]}
ALIASES["leica:body:m6:reissue"] = ["leica m6 reissue", "m6 reissue", "m6 2022", "m6 리이슈", "m6 복각", "라이카 m6 리이슈"]
NAME_KO["leica:body:m6:reissue"] = "라이카 M6 리이슈 (2022)"
M6_EDITIONS = [
    ("m6j", "Leica M6J (40 Jahre Leica M)", "M6J", [r"M6 ?J\b"], ["m6j", "m6 j"]),
    ("titan", "Leica M6 Titan", "M6 티탄", [r"\bM ?6\b", r"titan|티탄"], ["m6 titan", "m6 티탄"]),
    ("platinum", "Leica M6 Platinum (150 Jahre)", "M6 플래티넘", [r"\bM ?6\b", r"platin|플래티넘"], ["m6 platinum"]),
    ("lhsa", "Leica M6 LHSA", "M6 LHSA", [r"\bM ?6\b", r"LHSA"], ["m6 lhsa"]),
    ("royal", "Leica M6 Royal (Centenary · Wedding)", "M6 로얄", [r"\bM ?6\b", r"royal|로얄"], ["m6 royal"]),
    ("jaguar", "Leica M6 Jaguar XK", "M6 재규어", [r"\bM ?6\b", r"jaguar|재규어"], ["m6 jaguar"]),
    ("ttl-millennium", "Leica M6 TTL Millennium (Black Paint)", "M6 TTL 밀레니엄", [r"\bM ?6\b", r"millenn?ium|밀레니엄"], ["m6 ttl millennium", "m6 millennium", "m6 밀레니엄"]),
]
for slug, name, ko, must, aliases in M6_EDITIONS:
    key = f"leica:body:m6:{slug}"
    MODELS[key] = {"model_key": key, "display_name": name, "category": "Body", "mount": "M", "title_must": must, "title_must_not": []}
    ALIASES[key] = aliases
    NAME_KO[key] = ko
PARENTS["leica:body:m6"] = ("Leica M6 (all)", "Body", "M",
                            ["leica:body:m6:classic", "leica:body:m6:ttl", "leica:body:m6:reissue"] + [f"leica:body:m6:{e[0]}" for e in M6_EDITIONS],
                            ["leica m6", "m6", "라이카 m6", "엠6"], "라이카 M6 (전체)")
fam("leica:body:m7", "Leica M7", "라이카 M7", "M", [r"\bM ?7\b"], [], ["엠7"], [
    v("titan", "Leica M7 Titan (M-System 50 Jahre)", "M7 티탄", r"titan|티탄", ["m7 titan"]),
    v("hermes", "Leica M7 Hermès", "M7 에르메스", r"herm[eè]s|에르메스", ["m7 hermes", "m7 에르메스"]),
    v("a-la-carte", "Leica M7 à la carte", "M7 알라카르테", r"[aà] ?la ?carte|알라카르트|알라카르테", ["m7 a la carte", "m7 alacarte"]),
])
fam("leica:body:mp-film", "Leica MP (film)", "라이카 MP", "M", [r"\bMP\b"],
    [r"M-?P\b ?(240|typ)", r"M10-?P", r"M11-?P", r"\bMP ?[36]\b", r"\bQ-?P\b", r"M9-?P"], ["mp film", "엠피"], [
    v("hermes", "Leica MP Hermès", "MP 에르메스", r"herm[eè]s|에르메스", ["mp hermes", "mp 에르메스"]),
    v("lhsa", "Leica MP LHSA (Grey Hammertone)", "MP LHSA", r"LHSA|hammertone|해머톤", ["mp lhsa", "mp hammertone"]),
    v("a-la-carte", "Leica MP à la carte", "MP 알라카르테", r"[aà] ?la ?carte|알라카르트|알라카르테", ["mp a la carte"]),
    v("oskar-barnack", "Leica MP Oskar Barnack Edition (1879–2004)", "MP 오스카 바르낙", r"oskar|barnack", ["mp oskar barnack"], [r"0-?series|o-?series"]),
    v("korea-70", "Leica MP 70th Independence Anniversary (Korea)", "MP 광복 70주년", r"광복|independence", ["mp 광복 70주년", "mp independence"]),
], standard_name="Leica MP (film, standard)")
fam("leica:body:mp3", "Leica MP3 (LHSA)", "라이카 MP3", "M", [r"\bMP ?3\b"], [], ["mp3 lhsa"])
fam("leica:body:mp6", "Leica MP6", "라이카 MP6", "M", [r"\bMP ?6\b"], [], [])  # 확인 필요
fam("leica:body:m-a", "Leica M-A (Typ 127)", "라이카 M-A", "M", [r"\bM-?A\b"], [], ["ma typ 127", "m-a typ 127", "엠에이"])

# ── M 디지털 바디 ──
fam("leica:body:m8", "Leica M8", "라이카 M8", "M", [r"\bM ?8\b"], [r"M8\.2"], [], [
    v("white", "Leica M8 White Edition", "M8 화이트", r"white|화이트", ["m8 white"]),
    v("hermes", "Leica M8 Hermès", "M8 에르메스", r"herm[eè]s|에르메스", ["m8 hermes"]),  # 확인 필요
])
fam("leica:body:m8-2", "Leica M8.2", "라이카 M8.2", "M", [r"\bM ?8\.2\b"], [], ["m82"], [
    v("safari", "Leica M8.2 Safari", "M8.2 사파리", r"safari|사파리", ["m8.2 safari"]),
])
fam("leica:body:m9", "Leica M9", "라이카 M9", "M", [r"\bM ?9\b"], [r"M9-?P", r"monochrom"], [], [
    v("titanium", "Leica M9 Titanium", "M9 티타늄", r"titan|티탄|티타늄", ["m9 titanium"]),
    v("neiman-marcus", "Leica M9 Neiman Marcus", "M9 니만 마커스", r"neiman", ["m9 neiman marcus"]),  # 확인 필요
])
fam("leica:body:m9-p", "Leica M9-P", "라이카 M9-P", "M", [r"\bM ?9-?P\b"], [], ["m9p"], [
    v("hermes", "Leica M9-P Hermès", "M9-P 에르메스", r"herm[eè]s|에르메스", ["m9-p hermes"]),
])
fam("leica:body:m-monochrom-ccd", "Leica M Monochrom (2012, CCD)", "라이카 M 모노크롬 (CCD)", "M",
    [r"(\bM\b|M9) ?monochrom"], [r"M ?1[01]", r"246", r"240", r"M-?P"], ["m monochrom ccd", "m9 monochrom", "mm ccd", "m 모노크롬"])
fam("leica:body:m-e", "Leica M-E (Typ 220)", "라이카 M-E", "M", [r"\bM-?E\b|typ ?220"], [r"M10-?E"], ["m-e 220", "me typ 220"])
fam("leica:body:m240", "Leica M (Typ 240)", "라이카 M240", "M", [r"(\bM ?240\b|typ ?240)"], [r"M-?P", r"monochrom"], ["m typ 240", "m240", "엠240"], [
    v("edition-60", "Leica M Edition 60", "M 에디션 60", r"edition ?60|에디션 ?60", ["m edition 60"]),
    v("ara-guler", "Leica M (240) Ara Güler", "M240 아라 귈러", r"ara ?g[uü]ler", ["m240 ara guler"]),
])
fam("leica:body:m-p240", "Leica M-P (Typ 240)", "라이카 M-P 240", "M", [r"\bM-P\b|\bM-?P ?(240|typ ?240)"], [r"M10|M11|M9", r"monochrom", r"\bMP\b(?! ?(240|typ))"], ["m-p 240", "mp 240", "m-p typ 240"], [
    v("correspondent", "Leica M-P Correspondent (Lenny Kravitz)", "M-P 코레스폰던트", r"correspondent|kravitz|크라비츠", ["m-p correspondent", "lenny kravitz m-p"]),
    v("safari", "Leica M-P Safari", "M-P 사파리", r"safari|사파리", ["m-p safari"]),
    v("korea-70", "Leica M-P 70th Independence Anniversary (Korea)", "M-P 광복 70주년", r"광복|independence", ["m-p 광복 70주년"]),
    v("grip", "Leica M-P Grip (Ralph Gibson)", "M-P 그립", r"\bgrip\b|gibson", ["m-p grip"]),  # 확인 필요
])
fam("leica:body:m-monochrom-246", "Leica M Monochrom (Typ 246)", "라이카 M 모노크롬 246", "M", [r"246|(M ?240|typ ?240).*monochrom|monochrom.*240"], [], ["m246", "mm 246", "m monochrom 246"], [
    v("drifter", "Leica M Monochrom Drifter (Lenny Kravitz)", "M 모노크롬 드리프터", r"drifter|kravitz", ["monochrom drifter"]),
    v("your-mark", "Leica M Monochrom 'Your Mark'", "M 모노크롬 유어마크", r"your ?mark", ["monochrom your mark"]),  # 확인 필요
])
fam("leica:body:m262", "Leica M (Typ 262)", "라이카 M262", "M", [r"\bM ?262\b|typ ?262"], [r"M-?D"], ["m typ 262", "m262"])
fam("leica:body:m-d262", "Leica M-D (Typ 262)", "라이카 M-D", "M", [r"\bM-D\b"], [r"M10-?D|M11-?D"], ["m-d 262", "md 262"])
fam("leica:body:m10", "Leica M10", "라이카 M10", "M", [r"\bM ?10\b"], [r"M10-?(P|R|D|E)\b", r"monochrom"], ["엠10"], [
    v("zagato", "Leica M10 Edition Zagato", "M10 자가토", r"zagato|자가토", ["m10 zagato"]),
])
fam("leica:body:m10-p", "Leica M10-P", "라이카 M10-P", "M", [r"\bM ?10-?P\b"], [], ["m10p"], [
    v("white", "Leica M10-P White", "M10-P 화이트", r"white|화이트", ["m10-p white"]),
    v("asc-100", "Leica M10-P ASC 100", "M10-P ASC 100", r"ASC", ["m10-p asc 100"]),
    v("reporter", "Leica M10-P Reporter", "M10-P 리포터", r"reporter|리포터", ["m10-p reporter"]),
    v("ghost", "Leica M10-P Ghost (Hodinkee)", "M10-P 고스트", r"ghost|hodinkee|고스트", ["m10-p ghost"]),
    v("safari", "Leica M10-P Safari", "M10-P 사파리", r"safari|사파리", ["m10-p safari"]),  # 확인 필요
])
fam("leica:body:m10-d", "Leica M10-D", "라이카 M10-D", "M", [r"\bM ?10-?D\b"], [], ["m10d"])
fam("leica:body:m10-r", "Leica M10-R", "라이카 M10-R", "M", [r"\bM ?10-?R\b"], [], ["m10r"], [
    v("black-paint", "Leica M10-R Black Paint", "M10-R 블랙페인트", BLACK_PAINT[0], ["m10-r black paint"], BLACK_PAINT[1]),
])
fam("leica:body:m10-monochrom", "Leica M10 Monochrom", "라이카 M10 모노크롬", "M", [r"\bM ?10\b", r"monochrom"], [r"M10-?P"], ["m10 mono", "m10 모노크롬", "m10 모노"], [
    v("leitz-wetzlar", "Leica M10 Monochrom 'Leitz Wetzlar'", "M10 모노크롬 라이츠 베츨라", r"leitz ?wetzlar", ["m10 monochrom leitz wetzlar"]),
])
fam("leica:body:m10-e", "Leica M10-E", "라이카 M10-E", "M", [r"\bM ?10-?E\b"], [], [])  # 확인 필요
fam("leica:body:m11", "Leica M11", "라이카 M11", "M", [r"\bM ?11\b"], [r"M11-?(P|D|V)\b", r"monochrom"], ["엠11"], [
    v("black-paint", "Leica M11 Black Paint", "M11 블랙페인트", BLACK_PAINT[0] + r"|glossy", ["m11 black paint", "m11 glossy black"], BLACK_PAINT[1]),  # 확인 필요
])
fam("leica:body:m11-p", "Leica M11-P", "라이카 M11-P", "M", [r"\bM ?11-?P\b"], [], ["m11p"], [
    v("safari", "Leica M11-P Safari", "M11-P 사파리", r"safari|사파리", ["m11-p safari"]),  # 확인 필요
])
fam("leica:body:m11-monochrom", "Leica M11 Monochrom", "라이카 M11 모노크롬", "M", [r"\bM ?11\b", r"monochrom"], [], ["m11 mono", "m11 모노크롬", "m11 모노"])
fam("leica:body:m11-d", "Leica M11-D", "라이카 M11-D", "M", [r"\bM ?11-?D\b"], [], ["m11d"])
fam("leica:body:m-ev1", "Leica M EV1", "라이카 M EV1", "M", [r"\bEV ?1\b"], [], ["m ev1", "ev1"])

# ── Q ──
fam("leica:body:q", "Leica Q (Typ 116)", "라이카 Q", None, [r"\bQ\b(?!-?P)"], [r"\bQ ?[23]\b"], ["q typ 116", "q116", "큐"], [
    v("snow", "Leica Q Snow (Iouri Podladtchikov)", "Q 스노우", r"snow|스노우", ["q snow"]),
    v("safari", "Leica Q Safari", "Q 사파리", r"safari|사파리", ["q safari"]),
    v("khaki", "Leica Q Khaki", "Q 카키", r"khaki|카키", ["q khaki"]),  # 확인 필요
    v("titanium-gray", "Leica Q 'Titanium Gray'", "Q 티타늄 그레이", r"titan|티탄|티타늄", ["q titanium", "q titan"]),
])
fam("leica:body:q-p", "Leica Q-P", "라이카 Q-P", None, [r"\bQ-?P\b"], [], ["qp"])
fam("leica:body:q2", "Leica Q2", "라이카 Q2", None, [r"\bQ ?2\b"], [r"monochrom"], ["큐2"], [
    v("reporter", "Leica Q2 Reporter", "Q2 리포터", r"reporter|리포터", ["q2 reporter"]),
    v("007", "Leica Q2 '007 Edition'", "Q2 007 에디션", r"\b007\b", ["q2 007"]),
    v("ghost", "Leica Q2 Ghost (Hodinkee)", "Q2 고스트", r"ghost|hodinkee|고스트", ["q2 ghost"]),
    v("dawn", "Leica Q2 'Dawn' by Seal", "Q2 던 바이 씰", r"dawn|seal", ["q2 dawn", "q2 dawn by seal"]),
])
fam("leica:body:q2-monochrom", "Leica Q2 Monochrom", "라이카 Q2 모노크롬", None, [r"\bQ ?2\b", r"monochrom"], [], ["q2 mono", "q2 모노크롬", "큐2 모노"], [
    v("reporter", "Leica Q2 Monochrom Reporter", "Q2 모노크롬 리포터", r"reporter|리포터", ["q2 monochrom reporter"]),  # 확인 필요
])
fam("leica:body:q3", "Leica Q3", "라이카 Q3", None, [r"\bQ ?3\b"], [r"\b43\b", r"43\s?mm"], ["큐3"])
fam("leica:body:q3-43", "Leica Q3 43", "라이카 Q3 43", None, [r"\bQ ?3\b", r"\b43(\s?mm)?\b"], [], ["q3 43", "q343", "큐3 43"])

# ── SL · TL · CL · S ──
fam("leica:body:sl601", "Leica SL (Typ 601)", "라이카 SL (601)", "SL", [r"\bSL\b(?! ?\d)|typ ?601"], [r"\b\d{2,3}(-\d{2,3})?\s?(mm|/)", r"\bSL ?[23]\b"], ["sl typ 601", "sl601", "sl 601"])
fam("leica:body:sl2", "Leica SL2", "라이카 SL2", "SL", [r"\bSL ?2\b"], [r"SL2-?S"], [])
fam("leica:body:sl2-s", "Leica SL2-S", "라이카 SL2-S", "SL", [r"\bSL ?2-?S\b"], [], ["sl2s"], [
    v("reporter", "Leica SL2-S Reporter", "SL2-S 리포터", r"reporter|리포터", ["sl2-s reporter"]),
])
fam("leica:body:sl3", "Leica SL3", "라이카 SL3", "SL", [r"\bSL ?3\b"], [r"SL3-?S"], [])
fam("leica:body:sl3-s", "Leica SL3-S", "라이카 SL3-S", "SL", [r"\bSL ?3-?S\b"], [], ["sl3s"])
fam("leica:body:t701", "Leica T (Typ 701)", "라이카 T", "TL", [r"\bT\b ?\(?typ ?701|\bleica T\b(?! ?L)"], [], ["t typ 701", "t701"])
fam("leica:body:tl", "Leica TL", "라이카 TL", "TL", [r"\bTL\b(?! ?2)"], [r"\b\d{2,3}(-\d{2,3})?\s?(mm|/)", r"\d{2}-\d{2}", r"elmar|summi|vario|apo"], [])
fam("leica:body:tl2", "Leica TL2", "라이카 TL2", "TL", [r"\bTL ?2\b"], [], [])
fam("leica:body:cl-digital", "Leica CL (2017)", "라이카 CL (디지털)", "TL", [r"\bCL\b"],
    [r"(leitz|minolta|50 ?jahre|summicron-?c|40\s?mm|film|필름|1973)", r"\b\d{2,3}(-\d{2,3})?\s?(mm|/)"], ["cl 2017", "cl digital", "cl 디지털"], [
    v("paul-smith", "Leica CL Paul Smith", "CL 폴 스미스", r"paul ?smith|폴 ?스미스", ["cl paul smith"]),
    v("bauhaus", "Leica CL '100 Jahre Bauhaus'", "CL 바우하우스", r"bauhaus|바우하우스", ["cl bauhaus"]),
])
fam("leica:body:s2", "Leica S2", "라이카 S2", "S", [r"\bS ?2(-?P)?\b"], [r"SL"], ["s2-p"])
fam("leica:body:s006", "Leica S (Typ 006) · S-E", "라이카 S (006)", "S", [r"\bS\b ?\(?typ ?006|\bS-?E\b"], [], ["s typ 006", "s-e", "s006"])
fam("leica:body:s007", "Leica S (Typ 007)", "라이카 S (007)", "S", [r"\bS\b ?\(?typ ?007"], [], ["s typ 007", "s007"])
fam("leica:body:s3", "Leica S3", "라이카 S3", "S", [r"\bS ?3\b"], [r"SL"], [])

# ── 컴팩트 ──
fam("leica:body:x1", "Leica X1", "라이카 X1", None, [r"\bX ?1\b"], [], [])
fam("leica:body:x2", "Leica X2", "라이카 X2", None, [r"\bX ?2\b"], [], [], [
    v("paul-smith", "Leica X2 Paul Smith", "X2 폴 스미스", r"paul ?smith|폴 ?스미스", ["x2 paul smith"]),
    v("a-la-carte", "Leica X2 à la carte", "X2 알라카르테", r"[aà] ?la ?carte|알라카르테", ["x2 a la carte"]),
])
fam("leica:body:x-vario", "Leica X Vario (Typ 107)", "라이카 X 바리오", None, [r"\bX ?Vario\b"], [], ["x vario"])
fam("leica:body:x113", "Leica X (Typ 113)", "라이카 X (113)", None, [r"\bX\b ?\(?typ ?113|\bleica X\b(?! ?[12]|-|\s?vario)|\bX ?moncler|x-moncler"], [r"X-?U|X-?E\b"], ["x typ 113", "x113"], [
    v("moncler", "Leica X Moncler", "X 몽클레어", r"moncler|몽클레어", ["x moncler"]),
])
fam("leica:body:x-u", "Leica X-U (Typ 113)", "라이카 X-U", None, [r"\bX-?U\b"], [], ["xu"])
fam("leica:body:x-e", "Leica X-E (Typ 102)", "라이카 X-E", None, [r"\bX-E\b"], [], ["xe"])
DLUX_GENS = []
for gen in ("2", "3", "4", "5", "6"):
    fam(f"leica:body:d-lux-{gen}", f"Leica D-Lux {gen}", f"라이카 D-Lux {gen}", None, [rf"D-?Lux ?{gen}\b"], [], [f"dlux{gen}", f"d lux {gen}", f"디룩스 {gen}"])
    DLUX_GENS.append(f"leica:body:d-lux-{gen}")
fam("leica:body:d-lux-109", "Leica D-Lux (Typ 109)", "라이카 D-Lux 109", None, [r"D-?Lux", r"109"], [], ["d-lux 109", "dlux 109", "d-lux typ 109", "디룩스 109"])
fam("leica:body:d-lux-7", "Leica D-Lux 7", "라이카 D-Lux 7", None, [r"D-?Lux ?7\b"], [], ["dlux7", "디룩스 7"], [
    v("bape", "Leica D-Lux 7 'A Bathing Ape × Stash'", "D-Lux 7 베이프", r"bape|bathing ?ape|stash", ["d-lux 7 bape"]),
    v("vans", "Leica D-Lux 7 Vans × Ray Barbee", "D-Lux 7 반스", r"vans|barbee|반스", ["d-lux 7 vans"]),
    v("007", "Leica D-Lux 7 '007 Edition'", "D-Lux 7 007 에디션", r"\b007\b", ["d-lux 7 007"]),  # 확인 필요
])
fam("leica:body:d-lux-8", "Leica D-Lux 8", "라이카 D-Lux 8", None, [r"D-?Lux ?8\b"], [], ["dlux8", "디룩스 8"], [
    v("100-years", "Leica D-Lux 8 '100 Years of Leica'", "D-Lux 8 100주년", r"100 ?years|100주년|100 ?jahre", ["d-lux 8 100 years"]),
])
fam("leica:body:d-lux-unspecified", "Leica D-Lux (generation not stated)", "라이카 D-Lux (세대 미표기)", None, [r"D-?Lux(?! ?\d)"], [r"109", r"typ"], [])
PARENTS["leica:body:d-lux"] = ("Leica D-Lux (all)", "Body", None, DLUX_GENS + ["leica:body:d-lux-109", "leica:body:d-lux-7", "leica:body:d-lux-8", "leica:body:d-lux-unspecified"],
                               ["leica d-lux", "d-lux", "dlux", "라이카 d-lux", "디룩스"], "라이카 D-Lux (전체)")
fam("leica:body:c-lux", "Leica C-Lux (2018)", "라이카 C-Lux", None, [r"C-?Lux\b(?! ?[123]\b)"], [], ["clux", "씨룩스"])
fam("leica:body:c-lux-old", "Leica C-Lux 1 · 2 · 3", "라이카 C-Lux 1·2·3", None, [r"C-?Lux ?[123]\b"], [], ["c-lux 1", "c-lux 2", "c-lux 3"])
fam("leica:body:v-lux", "Leica V-Lux (1 · 2 · 3 · 4 · 5 · Typ 114)", "라이카 V-Lux", None, [r"V-?Lux"], [], ["vlux", "v-lux 5", "v-lux 114"])
fam("leica:body:digilux", "Leica Digilux (1 · 2 · 3 · Zoom)", "라이카 디지룩스", None, [r"digilux"], [], ["digilux 2", "digilux 3", "디지룩스"])
fam("leica:body:minilux", "Leica Minilux", "라이카 미니룩스", None, [r"minilux"], [r"zoom|줌"], ["미니룩스"])
fam("leica:body:minilux-zoom", "Leica Minilux Zoom", "라이카 미니룩스 줌", None, [r"minilux", r"zoom|줌"], [], ["minilux zoom", "미니룩스 줌"])
fam("leica:body:cm", "Leica CM", "라이카 CM", None, [r"\bCM\b"], [r"zoom|줌"], [])
fam("leica:body:cm-zoom", "Leica CM Zoom", "라이카 CM 줌", None, [r"\bCM\b", r"zoom|줌"], [], ["cm zoom"])
fam("leica:body:c-series", "Leica C1 · C2 · C3 · C11", "라이카 C1·C2·C3", None, [r"\bC ?(1|2|3|11)\b(?! ?[0-9])"], [r"C-?Lux"], ["c1", "c2", "c3", "c2 zoom"])
fam("leica:body:z2x", "Leica Z2X", "라이카 Z2X", None, [r"\bZ2X\b"], [], [])
fam("leica:body:sofort", "Leica Sofort (2016)", "라이카 소포트", None, [r"sofort"], [r"sofort ?2"], ["소포트"])
fam("leica:body:sofort-2", "Leica Sofort 2", "라이카 소포트 2", None, [r"sofort ?2"], [], ["sofort2", "소포트 2"], [
    v("burton", "Leica Sofort 2 Burton Edition", "소포트 2 버튼", r"burton|버튼", ["sofort 2 burton"]),
])

# ── 바르낙 (스크루마운트) ──
BARNACK = [
    ("i", "Leica I (Model A · C)", r"\bI\b ?\(?[AC]\)?(?!\w)|\bLeica I\b(?! ?[cfg]\b)"), ("ic", "Leica Ic", r"\bI ?c\b"), ("if", "Leica If", r"\bI ?f\b"), ("ig", "Leica Ig", r"\bI ?g\b"),
    ("ii", "Leica II (Model D)", r"\bII\b ?\(?D?\)?(?! ?[a-f]\b)|\bIID\b"), ("iia", "Leica IIa", r"\bII ?a\b"), ("iic", "Leica IIc", r"\bII ?c\b"), ("iif", "Leica IIf", r"\bII ?f\b"),
    ("iii", "Leica III (Model F)", r"\bIII\b ?\(?F?\)?(?! ?[a-g]\b)"), ("iiia", "Leica IIIa", r"\bIII ?a\b"), ("iiib", "Leica IIIb", r"\bIII ?b\b"), ("iiic", "Leica IIIc", r"\bIII ?c\b"),
    ("iiid", "Leica IIId", r"\bIII ?d\b"), ("iiif", "Leica IIIf", r"\bIII ?f\b|ⅢF"), ("iiig", "Leica IIIg", r"\bIII ?g\b"), ("72", "Leica 72", r"leica ?72\b"),
    ("250", "Leica 250 Reporter", r"\b250\b.*reporter|reporter.*\b250\b"),
    ("standard", "Leica Standard (E)", r"\bstandard\b"),
]
for slug, name, pattern in BARNACK:
    short = _short(name).split(" (")[0].lower()
    fam(f"leica:body:{slug}", name, f"라이카 {_short(name).split(' (')[0]}", None, [pattern],
        [r"\bM ?\d", r"\bR ?\d", r"\bSL\b", r"\bQ\b", r"\bX\b", r"\bS ?\d", r"\bQ ?\d", r"magnifier|data ?back|soft ?release|vit\b"] if slug in ("i", "ii", "iii", "standard") else [r"\bM ?\d"],
        [short, f"barnack {short}", f"바르낙 {short}"])

# ── R · 라이카플렉스 ──
fam("leica:body:leicaflex", "Leicaflex (standard)", "라이카플렉스", "R", [r"leicaflex"], [r"leicaflex ?sl"], ["leicaflex", "라이카플렉스"])
fam("leica:body:leicaflex-sl", "Leicaflex SL", "라이카플렉스 SL", "R", [r"leicaflex ?sl\b(?! ?2)"], [], ["leicaflex sl"])
fam("leica:body:leicaflex-sl2", "Leicaflex SL2", "라이카플렉스 SL2", "R", [r"leicaflex ?sl ?2"], [], ["leicaflex sl2"])
for model_name in ("R3", "R4", "R4s", "R5", "R-E", "R6", "R6.2", "R7", "R8", "R9"):
    slug = model_name.lower().replace(".", "-")
    pat = {"R3": r"\bR ?3\b", "R4": r"\bR ?4\b(?!s)", "R4s": r"\bR ?4 ?s\b", "R5": r"\bR ?5\b", "R-E": r"\bR-E\b(?!-?issue)",
           "R6": r"\bR ?6\b(?!\.2)", "R6.2": r"\bR ?6\.2\b", "R7": r"\bR ?7\b", "R8": r"\bR ?8\b", "R9": r"\bR ?9\b"}[model_name]
    variants = [v("gold", "Leica R3 Gold", "R3 골드", r"gold|골드", ["r3 gold"]),
                v("safari", "Leica R3 Safari", "R3 사파리", r"safari|사파리", ["r3 safari"])] if model_name == "R3" else []
    fam(f"leica:body:{slug}", f"Leica {model_name}", f"라이카 {model_name}", "R", [pat],
        [r"\b\d{2,3}\s?mm\b(?!.*(set|세트|\+))"], [], variants)

# ── 그 밖 ──
fam("leica:body:0-series-2004", "Leica 0-Series Replica (Oskar Barnack Edition, 2004)", "라이카 0-시리즈 복각 (2004)", None,
    [r"(0-?series|o-?series|0 ?serie|null ?serie|oskar ?barnack.*(1879|2004))"], [r"\bMP\b"], ["0 series", "0-series replica", "oskar barnack edition", "0시리즈"])
fam("leica:body:mini", "Leica mini · mini II · mini 3 · mini zoom", "라이카 미니", None, [r"\bmini\b(?!lux)"], [r"cooper|data ?back"], ["leica mini", "mini zoom", "mini ii", "미니"])
