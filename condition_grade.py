"""컨디션 공통 등급 — 사이트마다 다른 표기를 한 기준으로.

등급표 원본: '카메라브릿지 컨디션 등급표' 문서 (2026-10-04 초안).
  N 신품·미사용 · S 최상(99%↑) · A 상(97~98%) · B 중상(94~96%, 기준) · C 중(90~93%) · D 하(89%↓) · X 고장·부품용
반환: (등급 또는 None, 근거)  근거 = label(매장 등급 표기) | title(제목) | text(설명 글) | image(사진 평가)
"""
from __future__ import annotations

import re

GRADES = ["N", "S", "A", "B", "C", "D", "X"]

_BROKEN = re.compile(r"고장|부품용|작동\s?불량|ジャンク|\bjunk\b|for parts|spares|as-?is\b|not working", re.I)
_NEW = re.compile(r"신품|미사용|未使用|新品|\bbrand new\b|\bunused\b|(?<!asph )(?<!asph\. )(?<!bit )\bnew\b(?! ?(old|york|elmar|summicron|summilux|version|ver|type|\(\d{4}))", re.I)

# 일본 매장 (기타무라·나니와 등)
# 나니와는 AB+·AB-·B+도 씀. 사진 평가(표기 가리고 23점, 사진 3장씩, 2026-10-14): 사진이 이 대응보다 평균 0.9등급 후함
# (기존 매장 0.8과 비슷) → 공통 대응 그대로. AB+는 A, AB-는 B, B+는 사진이 B와 차이 없어 C.
# 이 대응 기준 정확 일치 4/23 · 한 등급 이내 15/23.
_JP = {"AA": "S", "A": "A", "AB+": "A", "AB": "B", "AB-": "B", "B+": "C", "B": "C", "C": "D"}
# 영국 Ffordes
_FFORDES = {"NEW": "N", "MINT": "N", "MINT-": "S", "E++": "A", "E+": "B", "E": "C", "VG": "D", "G": "D", "F": "X"}
# 영어권 설명·표기 (긴 표현 먼저)
_EN = [
    (r"like[\s-]?new|(?<!near\s)(?<!near-)\bmint\b(?!-)", "S"),
    (r"near[\s-]?mint|exc(?:ellent)?\s?\+{5}", "A"),
    (r"exc(?:ellent)?\s?\+{3,4}|excellent\s?\+|excellent plus", "B"),
    (r"\bexcellent\b|very good|\bvg\b", "C"),
    (r"\bgood\b|\bfair\b|\buser\b|heavy wear|well[\s-]used", "D"),
]


# 설명 글(Kamerastore·Miami)의 말투: 'good condition'은 보통 사용감이라 등급 표기의 Good(D)보다 후하게
_DESC = [
    (r"like[\s-]?new|(?<!near\s)(?<!near-)\bmint\b|as new", "S"),
    (r"near[\s-]?mint|\bexcellent\b|minimal (signs of )?(use|wear)", "B"),
    (r"very good|\bgood\b|minor (cosmetic )?wear|light wear", "C"),
    (r"\bfair\b|heavy wear|well[\s-]used|signs of heavy|brassing", "D"),
]
DESC_PREFIX = "설명: "


def from_percent(value: int) -> str:
    if value >= 99:
        return "S"
    if value >= 97:
        return "A"
    if value >= 94:
        return "B"
    if value >= 90:
        return "C"
    return "D"


def grade_of(site: str | None, condition: str | None, title: str | None = "") -> tuple[str | None, str | None]:
    cond = (condition or "").strip()
    title = title or ""
    if _BROKEN.search(title) or _BROKEN.search(cond):
        return "X", "title" if _BROKEN.search(title) else "label"
    if _NEW.search(title):
        return "N", "title"
    pct = re.fullmatch(r"(\d{2,3})\s?%", cond)
    if pct:
        return from_percent(int(pct.group(1))), "label"
    up = cond.upper()
    if site and ("기타무라" in site or "일본" in site) and up in _JP:
        return _JP[up], "label"
    if site and "ffordes" in site.lower() and up in _FFORDES:
        return _FFORDES[up], "label"
    if cond.startswith(KS_PREFIX):
        return _KS_GRADE.get(cond[len(KS_PREFIX):]), "text"
    if cond.startswith(LCF_PREFIX):
        letter = cond[len(LCF_PREFIX):].strip()[:1].upper()
        return (_LCF[letter], "label") if letter in _LCF else (None, None)
    if cond.startswith(NOC_PREFIX):
        return _NOC.get(cond[len(NOC_PREFIX):].strip().upper().replace(" ", "")), "label"
    if cond.startswith(CAMTEC_PREFIX):
        return _CAMTEC.get(cond[len(CAMTEC_PREFIX):].strip().upper()), "label"
    if cond.startswith(HARRISON_PREFIX):
        return _HARRISON.get(cond[len(HARRISON_PREFIX):].strip()), "label"
    if cond.startswith(WEX_PREFIX):
        return _WEX.get(re.sub(r"\s*\(.*\)\s*$", "", cond[len(WEX_PREFIX):]).strip().lower()), "label"
    if cond.startswith(CALUMET_PREFIX):
        return _CALUMET.get(cond[len(CALUMET_PREFIX):].strip()), "label"
    if cond.startswith(CAMERAWEST_PREFIX):
        return _CAMERAWEST.get(cond[len(CAMERAWEST_PREFIX):].strip()), "label"
    if cond.startswith(PETERLOY_PREFIX):
        cosmetic, _, working = cond[len(PETERLOY_PREFIX):].strip().partition("/")
        if working == "J":
            return "X", "label"
        grade = _PETERLOY.get(cosmetic)
        if grade and working in ("G", "H") and GRADES.index(grade) < GRADES.index("D"):
            grade = "D"  # 결함 있음·미확인은 외관과 상관없이 D
        return grade, "label"
    if cond.startswith(AKASAKA_PREFIX):
        return _AKASAKA.get(cond[len(AKASAKA_PREFIX):].strip()), "label"
    if cond.startswith(GLAZERS_PREFIX):
        return _GLAZERS.get(cond[len(GLAZERS_PREFIX):].strip().upper()), "label"
    if cond.startswith(TAMARKIN_PREFIX):
        return _TAMARKIN.get(cond[len(TAMARKIN_PREFIX):].strip().upper()), "label"
    if cond.startswith(LEICA_CLASSIC_PREFIX):
        return _LEICA_CLASSIC.get(cond[len(LEICA_CLASSIC_PREFIX):].strip().upper()), "label"
    if cond.startswith(FOTOHANDEL_PREFIX):
        return _FOTOHANDEL.get(cond[len(FOTOHANDEL_PREFIX):].replace(" ", "").upper()), "label"
    if cond.startswith(SANPOU_PREFIX):
        return _SANPOU.get(cond[len(SANPOU_PREFIX):].strip().upper()), "label"
    if cond.startswith(HEIDELBERG_PREFIX):
        return _HEIDELBERG.get(cond[len(HEIDELBERG_PREFIX):].strip()), "label"
    if cond.startswith(JCH_PREFIX):
        return _JCH.get(cond[len(JCH_PREFIX):].strip().lower()), "label"
    if cond.startswith(VIBE_PREFIX):
        return _VIBE.get(cond[len(VIBE_PREFIX):].strip().upper()), "label"
    if cond.startswith(KOESTER_PREFIX):
        return _KOESTER.get(cond[len(KOESTER_PREFIX):].strip()), "text"
    if cond.startswith(CE_PREFIX):
        phrase = cond[len(CE_PREFIX):]
        return next((g for pat, g in _CE if re.search(pat, phrase, re.I)), None), "text"
    if cond.startswith(LUCKY_PREFIX):
        return _LUCKY.get(cond[len(LUCKY_PREFIX):].strip().upper()), "label"
    if cond.startswith(APERTURE_PREFIX):
        return _APERTURE.get(cond[len(APERTURE_PREFIX):].strip()), "label"
    if cond.startswith(MK_PREFIX):
        if "not working" in cond:
            return "X", "label"
        for pattern, grade in _MK:
            if re.search(pattern, cond, re.I):
                return grade, "text"
        return None, None
    if cond.startswith(DESC_PREFIX):
        for pattern, grade in _DESC:
            if re.search(pattern, cond[len(DESC_PREFIX):], re.I):
                return grade, "text"
        return None, None
    if cond and cond.lower() not in ("정보없음", "used", "new", ""):
        for pattern, grade in _EN:
            if re.search(pattern, cond, re.I):
                return grade, "text"
    if up == "NEW":
        return "N", "label"
    return None, None


def describe_text(text: str) -> str | None:
    """설명 글에서 컨디션 표현을 뽑아 '컨디션' 칸에 넣을 말로 ('설명: Good condition' 꼴)."""
    t = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", text or ""))
    for pattern, _ in _DESC:
        m = re.search(rf"({pattern})(?: condition)?", t, re.I)
        if m:
            return DESC_PREFIX + m.group(0).strip()
    return None


# 홍콩 M & K Kamera: 설명 첫 문장이 정해진 몇 가지 말투 (2026-10-06 판매 중 815점 기준)
# 사진 평가(표기 가리고 28점, 사진 3장씩)로 맞춤: 'slightly used'와 'only minor signs of use'는 사진으로 갈리지 않아(각각 사진 A·B 중심)
# 둘 다 B. 기존 매장처럼 사진이 표기보다 한 등급쯤 후한 것을 감안했다.
MK_PREFIX = "M&K: "
_MK = [
    (r"brand new", "N"),
    (r"excellent condition", "A"),
    (r"excellent appearance|used preciously|only minor signs of use|slightly used", "B"),
    (r"normal signs of wear", "C"),
    (r"heavy (signs of )?(use|wear)|obvious signs", "D"),
]


def mk_condition(html: str) -> str | None:
    """M & K Kamera 상품 설명에서 컨디션 말투를 뽑아 'M&K: only minor signs of use' 꼴로."""
    t = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", html or ""))
    if re.search(r"not working|for parts|as-?is", t, re.I):
        return MK_PREFIX + "not working"
    for pattern, _ in _MK:
        m = re.search(pattern, t, re.I)
        if m:
            return MK_PREFIX + m.group(0).lower()
    return None


# 핀란드 Kamerastore: 직원 메모(상품 설명) 말투로. 등급 표기가 없고, 사이트의 Restored·Certified·Rescue는 작동 상태 구분이라 외관 등급이 아님.
# 사진 평가(말투 가리고 30점, 사진 3장씩, 2026-10-06)로 맞춤 — 사진이 표기보다 한 등급쯤 후한 것을 감안.
KS_PREFIX = "Kamerastore: "
NEG = r"(won'?t|will not|do(es)? not|doesn'?t|don'?t|without) (significantly )?affect"
_KS = [  # (이름, 패턴) 위에서부터 먼저 걸리는 것
    ("issue", r"fungus|(moderate|major|heavy|some) haze|sticky|not working|doesn'?t work|does not work|broken|separation|inaccurate|needs? (a )?(repair|service)|light leak|(affects?|affecting) (the )?image|lower (the )?(overall )?image quality|a lot of (haze|scratch|coating|fungus)|de-?silver|very hazy|haze layers|not accurate|in ?accurate|pinholes"),
    ("heavy", r"quite worn|heavily worn|heavy (signs of )?(wear|use)|well[\s-]used|significant wear|brassing|very worn|lots of wear|a lot of (external )?wear|corrosion|paint is coming off"),
    ("some", r"some (general |light )?(wear|marks|signs)|a bit worn|moderate(ly)? (wear|worn)|noticeable wear|signs of (wear|use)|shows wear|has wear|\bworn\b|\bdents?\b|general scratches|moderate cosmetic"),
    ("minor", r"minor (external |cosmetic )?(wear|marks|scratch)|light (wear|marks)|small (marks|scratch)|slight(ly)? (wear|worn)|tiny (marks|scratch)"),
    ("great", r"great (working )?(shape|condition)|excellent|like new|very good (working )?condition|very clean|clean and|mint"),
    ("working", r"working well|works well|works (perfectly|great)|good working condition|in working condition|in (a )?good condition|cleaned, lubricated|tested working"),
]
_KS_GRADE = {"issue": "D", "heavy": "D", "some": "C", "minor": "B", "great": "B", "working": "B"}


def ks_condition(html: str) -> str | None:
    """Kamerastore 상품 설명(직원 메모)에서 말투 단계를 뽑아 'Kamerastore: minor' 꼴로."""
    t = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", html or ""))
    for name, pattern in _KS:
        for m in re.finditer(pattern, t, re.I):
            if name == "issue" and re.search(NEG, t[max(0, m.start() - 60):m.end() + 40], re.I):
                continue
            return KS_PREFIX + name
    return None


# 라이카 프랑스 공식 중고 몰: 'A : Excellent'·'B : Very good'·'C : Good'·'D : Operational'·'E : Not fully operational'
LCF_PREFIX = "LCF: "
# 사진 평가(표기 가리고 24점, 사진 3장씩, 2026-10-06): 사진이 표기보다 평균 0.6등급 후함 → 기존 매장(0.8)과 비슷해 글자 그대로.
# 정확 일치 8/24 · 한 등급 이내 21/24. D(Operational)는 사진은 깨끗해도 작동 문제를 뜻해 D로 둠.
_LCF = {"A": "A", "B": "B", "C": "C", "D": "D", "E": "X"}


# 이탈리아 Newoldcamera: A-·AB·BA·B+·B+/B·B/B+·B·BC·C (A-가 가장 좋음)
NOC_PREFIX = "NOC: "
# 사진 평가(표기 가리고 23점, 사진 3장씩, 2026-10-08): 사진이 표기보다 평균 0.6등급 후함 → 기존 매장(0.6~0.8)과 비슷해 그대로.
# 정확 일치 11/23 · 한 등급 이내 22/23. A-·AB는 상자까지 있는 새것 같은 매물이 많지만 사진 후함을 빼고 A.
_NOC = {"A-": "A", "AB": "A", "BA": "B", "B+": "B", "B+/B": "C", "B/B+": "C", "B": "C", "BC": "D", "C": "D"}


# 캐나다 Camtec Photo: 제목 끝 '*A+*'·'*A*'·'*A-*'·'Open Box' (Open Box는 미사용 데모·반품, 사진도 신품 견본)
CAMTEC_PREFIX = "Camtec: "
# 사진 평가(표기 가리고 20점, 사진 3장씩, 2026-10-11): 표기를 한 칸 위로 옮긴 등급과 사진이 거의 같음(평균 차이 0) →
# 기존 매장은 사진이 표기보다 0.8등급 후했으니 Camtec 표기가 그만큼 후한 것. 한 칸 내려 A+→A, A→B, A-→C.
# 내린 대응 기준 정확 일치 3/17 · 한 등급 이내 15/17 (Open Box 3점 제외, 사진이 평균 0.9등급 후함 — 기존 매장과 같음).
_CAMTEC = {"OPEN BOX": "N", "A+": "A", "A": "B", "A-": "C", "B+": "C", "B": "D", "B-": "D", "C": "D"}


# 영국 Aperture: 설명 첫 줄 'Mint'·'Mint-'·'Exc+++'·'Exc++'·'Exc+'·'Exc'·'User' (+ 'Brand New'은 New)
APERTURE_PREFIX = "Aperture: "
# 사진 평가(표기 가리고 26점, 사진 3장씩, 2026-10-13): 사진 평균 Mint S~A · Mint-·Exc+++·Exc++ A · Exc+·Exc B · User C~D.
# 기존 매장처럼 사진이 표기보다 한 등급쯤 후한 것을 빼면 Mint A, Mint-·Exc+++·Exc++ B, Exc+·Exc C, User D.
# 이 대응 기준 정확 일치 4/26 · 한 등급 이내 20/26 (사진이 평균 1.1등급 후함 — Camtec 0.9·기존 0.8과 비슷).
# Mint-와 Exc++의 사진 차이가 없어 같은 B로 둔다 (Ffordes는 같은 글자를 더 후하게 쓰지만 이 매장 사진 기준).
_APERTURE = {"New": "N", "Mint": "A", "Mint-": "B", "Exc+++": "B", "Exc++": "B", "Exc+": "C", "Exc": "C", "User": "D"}
APERTURE_LABELS = set(_APERTURE)


# 영국 Harrison Cameras: 설명 끝 'Condition: Used - Very Good' (사이트 등급표 Mint·Excellent·Very Good·Good·Fairly Well Used)
HARRISON_PREFIX = "Harrison: "
# 사진 평가(표기 가리고 26점, 사진 3장씩, 2026-10-13): 사진 평균 Mint A · Excellent A · Very Good A~B · Good B.
# 기존 매장처럼 사진이 표기보다 한 등급쯤 후한 것을 빼면 Mint A, Excellent B, Very Good B, Good C, Fairly Well Used D.
# 이 대응 기준 정확 일치 8/26 · 한 등급 이내 25/26 (사진이 평균 0.7등급 후함 — 기존 0.8과 비슷).
# Excellent와 Very Good의 사진 차이가 작아 같은 B로 둔다.
_HARRISON = {"Mint": "A", "Excellent": "B", "Very Good": "B", "Good": "C", "Fairly Well Used": "D"}


def harrison_condition(body_html: str) -> str | None:
    """Harrison 설명에서 등급 글자. 'Condition: Used - Very good'·'Condition Very Good …'·'Used - Excellent' 모두."""
    import html as _html
    text = _html.unescape(re.sub(r"<[^>]+>", "\n", body_html or ""))
    m = re.search(r"(?im)^\s*(?:condition\s*:?\s*)?(?:used\s*-\s*)?(mint|excellent|very good|good|fairly well used)\b", text)
    if not m:
        return None
    return {"mint": "Mint", "excellent": "Excellent", "very good": "Very Good",
            "good": "Good", "fairly well used": "Fairly Well Used"}[re.sub(r"\s+", " ", m.group(1).lower())]
# 영국 Wex Photo Video: 'Condition' 칸 'As new (10)'·'Mint (9+)'·'Excellent (9)'·'Very good (9-)'·'Good (8)' (괄호 숫자는 매장 점수)
WEX_PREFIX = "Wex: "
# 사진 평가(표기 가리고 26점, 사진 2~3장씩, 2026-10-13): 사진 평균 As new S~A · Mint A · Excellent A · Very good A · Good A~B.
# 사진이 표기보다 후한 만큼(기존 0.8등급) 빼면 As new S, Mint A, Excellent B, Very good B, Good C.
# 이 대응 기준 정확 일치 9/26 · 한 등급 이내 23/26 (사진이 평균 0.6등급 후함). Excellent·Very good은 사진 차이가 없어 같은 B.
# 표본에 없던 아래 등급(Well used 등)은 Wex 등급표 순서대로 D.
_WEX = {"as new": "S", "mint": "A", "excellent": "B", "very good": "B", "good": "C",
        "well used": "D", "heavily used": "D", "poor": "D"}
# 독일 Calumet: 등급 선택지 'Wie neu (A)'·'Sehr gut (AB)'·'Gut (B)'·'Akzeptabel (BC)'·'Stark gebraucht (C)'
CALUMET_PREFIX = "Calumet: "
# 사진 평가(표기 가리고 25점, 사진 3장씩, 2026-10-14): 사진 평균 Wie neu A · Sehr gut A · Gut B · Akzeptabel A~B · Stark gebraucht B~C.
# 기존 매장처럼 사진이 표기보다 한 등급쯤 후한 것을 빼면 Wie neu A, Sehr gut B, Gut C, Akzeptabel C, Stark gebraucht D.
# 이 대응 기준 정확 일치 8/25 · 한 등급 이내 21/25 (사진이 평균 0.84등급 후함 — 기존 0.8과 같음).
_CALUMET = {"Wie neu": "A", "Sehr gut": "B", "Gut": "C", "Akzeptabel": "C", "Stark gebraucht": "D"}
# 미국 Camera West (+ Leica Store SF): 설명의 'I rate it cosmetically a (9+)' 점수 10-·9+·9·8+·8·7+
CAMERAWEST_PREFIX = "CameraWest: "
# 사진 평가(표기 가리고 25점, 사진 3장씩, 2026-10-14): 사진 평균 10- A · 9+ A~B · 9 B · 8+ B · 8 B · 7+ C.
# 기존 매장처럼 사진이 표기보다 한 등급쯤 후한 것을 빼면 10- A, 9+ B, 9 B, 8+ C, 8 C, 7+ D.
# 이 대응 기준 정확 일치 7/25 · 한 등급 이내 23/25 (사진이 평균 0.72등급 후함 — 기존 0.8과 비슷). 표본 없는 10은 A, 7 이하는 D.
_CAMERAWEST = {"10": "A", "10-": "A", "9+": "B", "9": "B", "9-": "B", "8+": "C", "8": "C", "8-": "C",
               "7+": "D", "7": "D", "7-": "D", "6+": "D", "6": "D", "5": "D"}
# 영국 Peter Loy: 설명의 'Condition 4-5/E' — 외관 1(새것)·3(near mint)·4(Exc+)·5(Exc)·6(많이 씀), 작동 C·D·E(정상)·G(결함)·H(미확인)·J(사용 불가)
PETERLOY_PREFIX = "PeterLoy: "
# 사진 평가(표기 가리고 25점, 사진 1장씩 — 매장 사진이 대부분 1장, 2026-10-14): 사진 평균 3 A · 3-4 A~B · 4 A~B · 4-5 A~B · 5 B · 5-6 B.
# 기존 매장처럼 사진이 표기보다 한 등급쯤 후한 것을 빼면 3 A, 3-4·4 B, 4-5·5 C, 5-6·6 D.
# 이 대응 기준 정확 일치 10/25 · 한 등급 이내 20/25 (사진이 평균 0.8등급 후함 — 기존과 같음).
_PETERLOY = {"1": "S", "1-2": "S", "2": "S", "2-3": "A", "3": "A", "3-4": "B", "4": "B", "4-5": "C", "5": "C",
             "5-6": "D", "6": "D", "6-7": "D", "7": "D"}
# 일본 Lucky Camera: 상세 '程度' AAA(미사용·극상)·AA(꽤 좋음)·AB(꽤 좋지만 흠 1~2곳)·A(보통 중고)·B(외관 많이 씀)·N(새것)
LUCKY_PREFIX = "Lucky: "
# 사진 평가(표기 가리고 25점, 사진 3장씩, 2026-10-14): 사진 평균 AA A · AB A~B · A B · B B~C.
# 기존 매장처럼 사진이 표기보다 한 등급쯤 후한 것을 빼면 AAA S, AA A, AB B, A C, B D.
# 이 대응 기준 정확 일치 10/25 · 한 등급 이내 20/25 (사진이 평균 0.84등급 후함 — 기존 0.8과 같음).
# 같은 글자라도 기타무라·나니와(A=상)보다 이 매장의 A가 '보통 중고'라 한 칸 낮음.
_LUCKY = {"N": "N", "AAA": "S", "AA": "A", "AB": "B", "A": "C", "B": "D"}
# 일본 Akasaka Camera: 목록 카드의 '程度' 新同品(새것 같음)·美品·良品·中(보통 중고). 극미품·並品은 표본 없어 순서대로.
AKASAKA_PREFIX = "Akasaka: "
# 사진 평가(표기 가리고 25점, 사진 3장씩, 2026-10-15): 美品 A 5 · 良品 A 6·B 3 · 中 A 4·B 1·C 5 · 新同品 S 1.
# 美品과 良品은 사진으로 차이가 거의 없어 둘 다 B, 中은 빈티지(니켈 엘마·헥토르·주마리트)는 C·나머지는 A로 갈려 C.
# 이 대응 기준 정확 일치 9/25 · 한 등급 이내 21/25 (사진이 평균 0.8등급 후함 — 기존 0.8과 같음).
_AKASAKA = {"新品": "N", "新同品": "S", "極美品": "A", "美品": "B", "良品": "B", "中": "C", "並品": "D", "並": "D"}
# 미국 Glazer's Camera: 제목 괄호 (M) Mint · (EX) Excellent · (VG) Very Good · (G)/(Good) · (Fair)
GLAZERS_PREFIX = "Glazers: "
# 사진 평가(표기 가리고 25점, 사진 최대 3장, 2026-10-15): EX A 5·S 2 · VG A 7·B 1 · G A 3·B 2·C 1 · Fair B 3 · M A 1.
# Fair는 모두 렌즈 안 흐림·접합 분리(Haze·Cement separation)라 사진엔 안 보여도 D.
# 이 대응 기준 정확 일치 7/25 · 한 등급 이내 19/25 (사진이 평균 0.88등급 후함 — 기존 0.8과 비슷).
_GLAZERS = {"M": "S", "EX": "A", "VG": "B", "G": "C", "GOOD": "C", "FAIR": "D", "POOR": "D"}
# 미국 Tamarkin Camera: 상세 가격 아래 'Nr. 258xxxx, Ex++'. 매장 등급표: Mint(새것 같음)·Near Mint(흠 1~2곳)·
# Ex++(아주 작은 흔적)·Ex+(평균보다 나음)·Ex(보통 사용감)·VG(많이 씀, 작동 정상)
TAMARKIN_PREFIX = "Tamarkin: "
# 사진 평가(표기 가리고 26점, 사진 3장씩, 2026-10-15): Mint S 1·A 1 · Near Mint A 4 · Ex++ A 6·B 2 · Ex+ A 4·B 4 ·
# Ex A 2 · VG A 1·B 1. Ex++와 Ex+는 사진으로 차이가 거의 없어 둘 다 B, VG는 매장 설명('많이 씀')대로 D.
# 이 대응 기준 정확 일치 10/26 · 한 등급 이내 22/26 (사진이 평균 0.7등급 후함 — 기존 0.8과 비슷).
_TAMARKIN = {"MINT": "S", "NEAR MINT": "A", "EX++": "B", "EX+": "B", "EX": "C", "VG": "D"}
# Leica Classic (라이카 매장 통합 중고 몰): 상세 'Condition' A·A-·A/B·B/A·B+·B·B-·B/C·C+·C·C/B·C-
LEICA_CLASSIC_PREFIX = "Leica Classic: "
# 사진 평가(표기 가리고 24점, 사진 3장씩, 2026-10-15): A S 2 · A- S 1·A 2·B 1 · A/B S 1·A 2 · B/A A 2·B 1·C 1 ·
# B+ A 1·B 1·C 2 · B A 3·B 1 · B- A 2 · B/C A 1. A/B·B/A·B+는 사진으로 갈리지 않아 셋 다 B.
# 이 대응 기준 정확 일치 6/24 · 한 등급 이내 17/24 (사진이 평균 0.75등급 후함 — 기존 0.8과 비슷).
_LEICA_CLASSIC = {"A+": "S", "A": "S", "A-": "A", "A/B": "B", "B/A": "B", "B+": "B", "B": "C", "B-": "C",
                  "B/C": "D", "C/B": "D", "C+": "D", "C": "D", "C-": "D"}
# 호주 Camera Electronic: 등급 표기 없이 제목·설명 글의 말투 ('Boxed As New'·'Mint in Box'·'excellent condition'·'well-used')
CE_PREFIX = "CE: "
# 사진 평가(표기 가리고 16점, 2026-10-15): 공용 설명 대응(_DESC)으로는 사진과 평균 -0.06등급 — 다른 매장(사진이 0.8 후함)보다
# 이 매장 말투가 한 칸 후해서 한 칸씩 내림. 이 대응 기준 사진이 평균 0.5등급 후함, 한 등급 이내 13/16.
_CE = [
    (r"like[\s-]?new|as new", "S"),
    (r"\bmint\b", "A"),
    (r"excellent", "C"),
    (r"very good|\bgood\b|minor (?:signs of )?(?:use|wear)|light wear|minimal signs", "D"),
    (r"\bfair\b|well[\s-]used|heavy (?:signs of )?(?:use|wear)", "D"),
]


def ce_condition(text: str) -> str | None:
    """Camera Electronic 제목+설명에서 첫 말투를 뽑아 'CE: Mint' 꼴로."""
    t = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", text or ""))
    for pat, _ in _CE:
        m = re.search(pat, t, re.I)
        if m:
            return CE_PREFIX + m.group(0)
    return None
# 독일 fotohandel.de: 카드·상세의 'Zustandsbeschreibung' A·A-·A-B·B·B-·B-C (A-B는 A와 B 사이)
FOTOHANDEL_PREFIX = "fotohandel: "
# 사진 평가(표기 가리고 27점, 사진 3장씩, 2026-10-18): A S 6·A 2 · A- A 5·B 1·C 1 · A-B A 3·B 2·C 1 · B B 1·C 2 ·
# B- B 1 · B-C B 2. 기존 매장처럼 사진이 표기보다 한 등급쯤 후한 것을 빼면 A A, A-·A-B B, B·B- C, B-C D.
# 이 대응 기준 정확 일치 7/27 · 한 등급 이내 25/27 (사진이 평균 0.67등급 후함 — 기존 0.8과 비슷).
# A-와 A-B는 사진으로 갈리지 않아 둘 다 B. 표본 없는 A+는 S, C는 D.
_FOTOHANDEL = {"A+": "S", "A": "A", "A-": "B", "A-B": "B", "B+": "C", "B": "C", "B-": "C", "B-C": "D", "C": "D"}
# 일본 三宝カメラ (Sanpou): 제목 끝 【AB】·【B】 (라이카는 거의 B, 가끔 AB). 기타무라 등과 같은 글자지만 이 매장 B는 폭이 넓은 '보통 중고'
SANPOU_PREFIX = "Sanpou: "
# 사진 평가(표기 가리고 25점, 사진 2장씩 — 매장 사진이 흰 배경 2장, 2026-10-18): AB S 2·A 5 · B A 8·B 8·C 2.
# 일본 공통 대응(AB B·B C)이면 사진이 평균 1.32등급 후해 기존(0.8)보다 크게 벗어나 한 칸 올림: AB A, B B.
# 이 대응 기준 정확 일치 13/25 · 한 등급 이내 25/25 (사진이 평균 0.32등급 후함). 표본 없는 AA·A는 S·A, C는 D.
_SANPOU = {"AAA": "S", "AA": "S", "A": "A", "AB": "A", "B": "B", "BC": "C", "C": "D"}

# 독일 Leica Store Heidelberg: 설명의 'Bewertet … mit der Schulnote 1-2' (독일 학교 점수, 1 가장 좋음 ~ 3), 매장 진열품은 'Demo'
HEIDELBERG_PREFIX = "Heidelberg: "
# 사진 평가(표기 가리고 26점, 사진 3장씩 — 여백 잘라서, 2026-10-18): 1 S 3 · 1- S 3·A 3 · 1-2 S 1·A 5 · 2+ S 1·A 2 ·
# 2 S 1·A 1·B 2 · 2- S 1·A 1 · 2-3 C 1 · 3 S 1. 매장 사진이 밝은 흰 배경이라 대부분 S~A로 보여 점수와 사진 차이가 작음.
# 기존 매장처럼 사진이 한 등급쯤 후한 것을 빼면 1·1-·1-2 A, 2+·2·2- B, 2-3 C, 3 D.
# 이 대응 기준 정확 일치 11/26 · 한 등급 이내 22/26 (사진이 평균 0.81등급 후함 — 기존 0.8과 같음). Demo(진열품)는 S.
_HEIDELBERG = {"1+": "S", "1": "A", "1-": "A", "1-2": "A", "2+": "B", "2": "B", "2-": "B", "2-3": "C", "3+": "C", "3": "D",
               "3-": "D", "3-4": "D", "4": "D", "Demo": "S"}

# 폴란드 Vibe.pl: 설명의 'Stan zużycia: 4' — NOWY(신품)·DEMO(진열품)·5(흔적 거의 없음)·4(작은 흔적)·3(보통 흔적)·2(많이 씀)·1
VIBE_PREFIX = "Vibe: "
# 사진 평가(표기 가리고 29점 — 판매 끝난 것 포함, 사진 3장씩, 2026-10-18): 5 S 3·A 4·B 1 · 4 S 2·A 14·B 3 · 3 B 1·C 1.
# 기존 매장처럼 사진이 한 등급쯤 후한 것을 빼면 5 A, 4 B, 3 C, 2·1 D.
# 이 대응 기준 정확 일치 8/29 · 한 등급 이내 27/29 (사진이 평균 0.72등급 후함 — 기존 0.8과 비슷). DEMO는 S.
_VIBE = {"DEMO": "S", "5": "A", "4": "B", "3": "C", "2": "D", "1": "D"}

# 독일 Foto Köster: 등급표 없이 상세 설명 글의 말투 — 'sehr guten Zustand mit kaum erkennbaren Abnutzungen'·'wie neu'·'Top-Zustand'
# (sehr gut) · 'guten Zustand mit normalen/minimalen kosmetischen Abnutzungen' (gut) · 'Nebel'·'defekt'·'Kratzer auf der Frontlinse' (defekt)
KOESTER_PREFIX = "Koester: "
# 사진 평가(표기 가리고 27점, 사진 3장씩, 2026-10-18): sehr gut S 3·A 3 · gut A 7·B 8·C 2 · defekt A 1·B 1·C 2.
# 기존 매장처럼 사진이 한 등급쯤 후한 것을 빼면 sehr gut A, gut B, defekt D (렌즈 안 흐림은 사진에 잘 안 보여도 D).
# 이 대응 기준 정확 일치 11/27 · 한 등급 이내 25/27 (사진이 평균 0.56등급 후함).
_KOESTER = {"sehr gut": "A", "gut": "B", "defekt": "D"}

# 일본 Japan Camera Hunter: 설명 첫 문장 'Mint minus condition.' / 'Excellent plus condition.' (영어권 수출점 말투)
JCH_PREFIX = "JCH: "
# 사진 평가(표기 가리고 28점, 사진 3장씩, 2026-10-19): 아래 대응 기준 정확 일치 14/28 · 한 등급 이내 24/28, 사진이 평균 0.36등급
# 후함 (기존 0.8보다 덜 후함 — 한 칸 내리면 사진이 1.36등급 후해져 더 벌어져 그대로 둠). Mint minus는 사진상 A~S, Excellent plus는 A~B.
_JCH = {"like new": "S", "mint": "S", "near mint": "A", "mint minus": "A", "excellent plus": "B", "excellent": "C",
        "very good": "C", "good": "D", "clean user": "D", "good user": "D", "user": "D"}
