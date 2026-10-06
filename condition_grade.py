"""컨디션 공통 등급 — 사이트마다 다른 표기를 한 기준으로.

등급표 원본: '카메라브릿지 컨디션 등급표' 문서 (2026-10-04 초안).
  N 신품·미사용 · S 최상(99%↑) · A 상(97~98%) · B 중상(94~96%, 기준) · C 중(90~93%) · D 하(89%↓) · X 고장·부품용
반환: (등급 또는 None, 근거)  근거 = label(매장 등급 표기) | title(제목) | text(설명 글) | image(사진 평가)
"""
from __future__ import annotations

import re

GRADES = ["N", "S", "A", "B", "C", "D", "X"]

_BROKEN = re.compile(r"고장|부품용|작동\s?불량|ジャンク|\bjunk\b|for parts|spares|as-?is\b|not working", re.I)
_NEW = re.compile(r"신품|미사용|未使用|新品|\bbrand new\b|\bunused\b|\bnew\b(?! ?(old|york|elmar|summicron|summilux|version|ver))", re.I)

# 일본 매장 (기타무라 등)
_JP = {"AA": "S", "A": "A", "AB": "B", "B": "C", "C": "D"}
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
