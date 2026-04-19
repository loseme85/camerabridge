"""
classifier_v2.py
================
Camera Bridge 분류 파이프라인 v2

파이프라인 순서 (고정):
  normalize_text
  -> detect_brand
  -> detect_mount
  -> detect_category
  -> auto_label
  -> extract_flags
  -> classify_sold_quality
  -> classify_listing_v2   (오케스트레이터)

원칙:
  - 각 함수는 자기 책임만 수행한다
  - detect_mount는 절대 "Accessory"를 반환하지 않는다
  - auto_label은 brand/mount/category를 입력받아 label만 결정한다
  - legacy (test.py) 함수를 직접 호출하지 않는다
"""

from __future__ import annotations
import re
from typing import Optional
from model_detector import detect_model
from accessory_classifier import classify_accessory


# ─────────────────────────────────────────────
# 0. 공통 상수
# ─────────────────────────────────────────────

# 공식 label 집합 (이 목록 밖의 값은 반환하지 않는다)
VALID_LABELS = {
    # category-only
    "Lens", "Body", "Accessory", "Unknown",
    # mount + category
    "M Lens", "R Lens", "L Lens", "SL Lens", "S Lens", "V Lens",
    "M Body", "R Body", "L Body", "SL Body", "S Body", "V Body",
    # brand + category
    "Leica Lens", "Leica Body",
    "Hasselblad Lens", "Hasselblad Body",
    "Canon Lens", "Canon Body",
    "Nikon Lens", "Nikon Body",
    "Zeiss Lens", "Voigtlander Lens",
    # 3rd party
    "3rd Party Lens", "3rd Party M Lens",
    "3rd Party Body",
}

VALID_MOUNTS = {
    "M", "R", "L", "SL", "S", "Q",
    "Compact", "PNS",
    "V",          # Hasselblad V
    "C/Y",        # Contax/Yashica legacy SLR mount
    "EF", "F", "RF", "E",
    "Unknown",
}

VALID_BRANDS = {
    "Leica", "Leitz",
    "Hasselblad",
    "Canon", "Nikon",
    "Zeiss", "Voigtlander",
    "Sigma", "Panasonic",
    "Cosina",
    "3rd Party",
    "Unknown",
}

VALID_CATEGORIES = {"Lens", "Body", "Accessory", "Unknown"}

THIRD_PARTY_BRANDS = [
    # Leica M mount 호환 서드파티 (전통)
    "voigtlander", "보이그랜더",
    "zeiss", "carl zeiss",
    # 신규 서드파티 M mount 브랜드
    "ttartisan", "티티아티산",
    "7artisans", "7 artisans", "7아티산",
    "thypoch",
    "funleader",
    "kamlan",
    "handevision",
    "pergear",
    "nisi",
    "meike",
    "pixii",
    "ms-optics", "ms optics",
    "artizlab",
    "light lens lab",
    "meyer optik",
    "laowa",
    # 추가 M mount 서드파티
    "peace",        # Peace 렌즈
    "mandler",      # Mandler Optics
    "coiro",        # Coiro (와인더/악세사리 제외용 — detect_category에서 필터링)
    "polar",        # Polar 렌즈
    "minox",        # Minox M mount 렌즈
    "konica",       # Konica M-Hexanon
    "heliar",       # Voigtlander Heliar 계열
    "skopar",       # Voigtlander Skopar 계열
    "septon",       # Voigtlander Septon
    # L-mount / SL 서드파티
    "cosina",
    "sigma",
    "panasonic", "lumix",
    # 기타
    "novoflex",
    "rollei",
    "minolta",
]


# ─────────────────────────────────────────────
# 1. normalize_text
# ─────────────────────────────────────────────

def normalize_text(name: str, description: Optional[str] = None) -> dict:
    """
    텍스트 정리만 수행. 브랜드/마운트/라벨 판단 금지.

    Returns:
        normalized_name: str
        normalized_description: str
        search_text: str          # name + description 결합 (분류용)
    """
    # 오타 보정 맵
    TYPO_MAP = [
        ("summicrom", "summicron"),
        ("summiarit", "summarit"),
        ("loctilux",  "noctilux"),
        ("elmatit",   "elmarit"),
        ("eleamrit",  "elmarit"),
        ("elemarit",  "elmarit"),
        ("summcron-c","summicron-c"),
        ("summcron",  "summicron"),
        ("summmicron","summicron"),
        ("summicton", "summicron"),
        ("apo-sumicron", "apo-summicron"),
        ("super -elmar", "super-elmar"),
        ("super-angvlon","super-angulon"),
        ("tri-elamr", "tri-elmar"),
        ("tri elamr", "tri-elmar"),
        ("summroan",  "summaron"),
        ("suimmilux", "summilux"),
        ("lecia",     "leica"),
    ]

    def _clean(text: str) -> str:
        t = text.lower().strip()
        # [중고], [위탁], [매장진열] 등 접두어 제거
        t = re.sub(r'^\[[^\]]+\]\s*', '', t)
        # 상품명 : 형식 제거
        if t.startswith('상품명') and ':' in t:
            t = t.split(':', 1)[-1].strip()
        # 오타 보정
        for wrong, right in TYPO_MAP:
            t = t.replace(wrong, right)
        # 과도한 공백 정리
        t = re.sub(r'\s+', ' ', t).strip()
        return t

    norm_name = _clean(name)
    norm_desc = _clean(description) if description else ""
    search_text = (norm_name + " " + norm_desc).strip()

    return {
        "normalized_name": norm_name,
        "normalized_description": norm_desc,
        "search_text": search_text,
    }


# ─────────────────────────────────────────────
# 2. detect_brand
# ─────────────────────────────────────────────

def detect_brand(normalized_name: str, normalized_description: Optional[str] = None) -> dict:
    """
    브랜드만 판단. mount/category/label 판단 금지.

    Returns:
        brand: str                 (VALID_BRANDS 중 하나)
        brand_confidence: float
        brand_reason: list[str]
    """
    text = normalized_name + " " + (normalized_description or "")
    n = text.lower()
    reasons = []

    # ── 0순위: 상품명 첫 토큰이 서드파티 브랜드인지 먼저 확인 ──
    # "TTArtisan 35mm ... for Leica M" 같은 케이스에서
    # "leica" 키워드에 먼저 걸려 오분류되는 것을 방지
    first_token = normalized_name.split()[0].lower() if normalized_name.strip() else ""
    for brand_kw in THIRD_PARTY_BRANDS:
        if first_token == brand_kw or normalized_name.lower().startswith(brand_kw):
            reasons.append(f"3rd_party_first_token:{brand_kw}")
            return {"brand": "3rd Party", "brand_confidence": 0.93, "brand_reason": reasons}

    # ── 1순위: Leica 고유 렌즈/바디 키워드 (브랜드 확정) ──
    LEICA_KW = [
        "leica", "leitz", "ernst leitz", "wetzlar",
        "summicron", "summilux", "noctilux",
        "elmarit", "elmar", "summarit", "summaron",
        "summar", "summarex", "hektor", "hologon",
        "telyt", "super-angulon", "angulon",
        "summitar",
    ]
    for kw in LEICA_KW:
        if kw in n:
            reasons.append(f"leica_kw:{kw}")
            return {"brand": "Leica", "brand_confidence": 0.97, "brand_reason": reasons}

    # ── 2순위: Hasselblad ──
    if "hasselblad" in n or "하셀블라드" in n:
        reasons.append("hasselblad_kw")
        return {"brand": "Hasselblad", "brand_confidence": 0.97, "brand_reason": reasons}

    # ── 3순위: 3rd Party (라이카 마운트 호환 서드파티) ──
    for brand_kw in THIRD_PARTY_BRANDS:
        if brand_kw in n:
            reasons.append(f"3rd_party_kw:{brand_kw}")
            return {"brand": "3rd Party", "brand_confidence": 0.90, "brand_reason": reasons}

    # ── 4순위: Canon / Nikon (독립 시스템) ──
    if "canon" in n or "캐논" in n:
        reasons.append("canon_kw")
        return {"brand": "Canon", "brand_confidence": 0.90, "brand_reason": reasons}
    if "nikon" in n or "니콘" in n:
        reasons.append("nikon_kw")
        return {"brand": "Nikon", "brand_confidence": 0.90, "brand_reason": reasons}

    reasons.append("no_brand_match")
    return {"brand": "Unknown", "brand_confidence": 0.40, "brand_reason": reasons}


# ─────────────────────────────────────────────
# 3. detect_mount
# ─────────────────────────────────────────────

_SL_BRANDS_FOR_L_TOKEN = {
    "TTARTISAN", "7ARTISANS", "LAOWA", "VENUS OPTICS",
    "SIGMA", "PANASONIC", "LUMIX", "MEIKE",
    "VILTROX", "TOKINA",
}

_FRACTIONAL_LENS_SPEC_RE = (
    r'\d{2,3}(?:-\d{2,3}){0,2}\s*/\s*'
    r'\d+(?:\.\d+)?(?:-\d+(?:\.\d+)?)?'
)


def _detect_shorthand_mount(n: str, raw: str) -> Optional[tuple[str, float, str, str]]:
    """
    브랜드 전체명이 생략된 매장식 mount/body shorthand.
    mount만 반환하고, Lens/Body 판단은 detect_category에 맡긴다.
    """
    if re.search(r'\bMDA\b', raw):
        return ("M", 0.93, "M_body_shorthand", "MDA")

    if re.search(r'\bLEICA\s+MP3\b', n):
        return ("M", 0.91, "M_body_shorthand", "LEICA MP3")

    if re.search(rf'(?<![A-Z0-9-])M\s+{_FRACTIONAL_LENS_SPEC_RE}', n):
        return ("M", 0.90, "M_lens_shorthand", "M NN/F")

    if re.search(
        rf'(?<![A-Z0-9])SL\s+(?:'
        rf'{_FRACTIONAL_LENS_SPEC_RE}|'
        r'\d{2,3}(?:-\d{2,3})\b|'
        r'(?:APO[-\s]+)?(?:SUMMICRON|SUMMILUX|VARIO|ELMARIT|ELMAR)\b'
        r')',
        n,
    ):
        return ("SL", 0.91, "SL_lens_shorthand", "SL lens shorthand")

    if re.search(
        rf'(?<![A-Z0-9])TL\s+(?:'
        rf'{_FRACTIONAL_LENS_SPEC_RE}|'
        r'\d{2,3}(?:-\d{2,3})\b|'
        r'(?:SUMMICRON|SUMMILUX|VARIO|ELMARIT|ELMAR)\b'
        r')',
        n,
    ):
        return ("SL", 0.90, "TL_lens_shorthand", "TL lens shorthand")

    if re.search(r'(?<![A-Z0-9])Q(?:2|3|P|-P)?\s+(?:28|43)(?:\s*MM)?\b', n):
        return ("Q", 0.90, "Q_body_shorthand", "Q focal shorthand")

    return None


def _detect_legacy_mount_abbrev(n: str, raw: str) -> Optional[tuple[str, float, str, str]]:
    """
    Legacy/non-Leica mount abbreviations that should not fall into broad M/Zeiss fallback.
    """
    if re.search(r'\bC\s*/\s*Y\b|\bCONTAX[\s/-]*YASHICA\b', n):
        return ("C/Y", 0.92, "CY_mount_explicit", "C/Y")

    if re.search(r'\bM[-\s]?EV\d\b', n):
        return ("M", 0.86, "M_legacy_shorthand", "M EV")

    if re.search(r'\bFOR\s+(?:LEICA\s+)?M(?:[2-9]|1[01])\b', n):
        return ("M", 0.86, "M_for_m_body", "for M body")

    return None


def _detect_l_family_mount(n: str) -> Optional[tuple[str, float, str, str]]:
    """
    L 표기 전용 분기.
    - LTM/L39/M39/Leica L 숫자 표기는 Barnack L
    - L-Mount 명시 또는 L-mount alliance 브랜드의 독립 L 토큰은 modern L(SL)
    - 단순 단어 안의 L 문자는 판단하지 않음
    """
    if re.search(r'\b(?:LTM|L39|M39)\b', n):
        return ("L", 0.95, "L_ltm_l39", "LTM/L39/M39")

    if re.search(r'\bLEICA\s+L\s+\d', n):
        return ("L", 0.90, "L_leica_l_prefix", "LEICA L NN")

    if re.search(r'\bL[\s-]MOUNT\b|\bFOR\s+L\b|L마운트|L\s+마운트', n):
        return ("SL", 0.93, "SL_l_mount_explicit", "L mount")

    if any(b in n for b in _SL_BRANDS_FOR_L_TOKEN):
        if re.search(r'\bL\s+\d{2,3}(?:-\d{2,3})?\s*(?:MM|[/.])', n):
            return ("SL", 0.88, "SL_3rd_l_prefix", "3rd_party+L+focal")
        if re.search(r'\bL\s*$|\bL\s+(BLACK|SILVER|CHROME|BODY|LENS|MOUNT)\b', n):
            return ("SL", 0.88, "SL_3rd_trailing_L", "3rd_party+trailing_L")

    if re.search(r'(?<![A-Z])L\s+\d{2,3}(?:-\d{2,3})?[/.]', n):
        return ("L", 0.88, "L_chungmuro", "L NN/")

    return None


def detect_mount(
    normalized_name: str,
    normalized_description: Optional[str] = None,
    brand: Optional[str] = None,
) -> dict:
    """
    마운트만 판단.
    - "Accessory"를 절대 반환하지 않는다 → Accessory 판단은 detect_category로
    - brand는 ambiguous case 보정에만 참고하며 재판정하지 않는다

    Returns:
        mount: str                 (VALID_MOUNTS 중 하나)
        mount_confidence: float
        mount_reason: list[str]
    """
    n = (normalized_name + " " + (normalized_description or "")).upper()
    raw = normalized_name.upper()
    reasons = []

    def hit(label, kw):
        reasons.append(f"{label}:{kw}")

    # ══════════════════════════════════════════
    # 설계 원칙: 명시적(explicit) 신호가 항상 일반 렌즈 키워드보다 우선한다.
    # 순서: R → S → Q → SL → PNS → Compact → L → Hasselblad-V → M
    # M 마운트 렌즈 키워드(SUMMICRON 등)는 가장 마지막에 체크한다.
    # ══════════════════════════════════════════

    # ── [R] 1단계: 가장 명시적인 R 신호 ──
    # "-R" suffix, "xCAM", "ROM" 등 R 마운트 고유 표기
    r_suffix_kw = [
        "SUMMILUX-R", "SUMMICRON-R", "ELMARIT-R", "ELMAR-R",
        "TELYT-R", "APO-TELYT-R", "SUPER-ELMAR-R",
        "APO-MACRO-ELMARIT-R", "VARIO-ELMARIT-R", "VARIO-APO-ELMARIT-R",
        "VARIO-ELMAR-R", "MACRO-ELMARIT-R",
        "APO-SUMMICRON-R",   # 명시적 suffix
        "3CAM", "2CAM", "1CAM", " ROM ", "-ROM",
        "APO EXTENDER R", "EXTENDER R",
        "LEICAFLEX",
        "ANGENIEUX", "PC SUPER ANGULON",
    ]
    for kw in r_suffix_kw:
        if kw in n:
            hit("R_suffix", kw)
            return {"mount": "R", "mount_confidence": 0.97, "mount_reason": reasons}

    # ── [R] 2단계: "LEICA R" prefix + 바디/렌즈 ──
    if re.search(r'\bLEICA\s+R\s+\d', n):
        hit("R_leica_r_prefix", "LEICA R NN")
        return {"mount": "R", "mount_confidence": 0.96, "mount_reason": reasons}

    # "LEICA R APO-..." 패턴 — 숫자 없어도 R 렌즈 패밀리명이 따라오면 R
    if re.search(r'\bLEICA\s+R\s+APO', n):
        hit("R_leica_r_apo", "LEICA R APO")
        return {"mount": "R", "mount_confidence": 0.95, "mount_reason": reasons}

    # LEICA R3~R9 바디명 명시
    if any(kw in n for kw in ["LEICA R3", "LEICA R4", "LEICA R5",
                                "LEICA R6", "LEICA R7", "LEICA R8", "LEICA R9"]):
        hit("R_body_leica", "LEICA R3-9")
        return {"mount": "R", "mount_confidence": 0.97, "mount_reason": reasons}

    # ── [R] 3단계: 충무로식 R 약식 "R NN/" / "R NN-NN/" ──
    if re.search(r'(?<![A-Z])R\s+\d{2,3}(?:-\d{2,3})?[/.]', n):
        hit("R_chungmuro", "R NN/")
        return {"mount": "R", "mount_confidence": 0.92, "mount_reason": reasons}

    # ── [R] 4단계: TELYT / VARIO 단독 (R-family 렌즈) ──
    # -M, -SL suffix가 없으면 R로 판단
    if "TELYT" in n and not any(x in n for x in ["APO-TELYT-M", "TELYT-M", "TELYT-SL"]):
        hit("R_telyt", "TELYT")
        return {"mount": "R", "mount_confidence": 0.88, "mount_reason": reasons}

    if "VARIO" in n and not any(x in n for x in [
        "VARIO-ELMARIT-SL", "VARIO-ELMARIT-TL", "APO-VARIO",
        "VARIO-ELMAR-S", "VARIO-SL",
    ]):
        # LEICA R이 포함되거나 -R suffix 있으면 R
        if "LEICA R" in n or re.search(r'VARIO.*-R\b', n):
            hit("R_vario", "VARIO+R")
            return {"mount": "R", "mount_confidence": 0.88, "mount_reason": reasons}

    # ── [R] 5단계: R6~R9 바디 단독 표기 ──
    if re.search(r'(?<![A-Z])R[6-9][\d.]*(?!\w)', raw):
        hit("R_body_number", "R6-R9")
        return {"mount": "R", "mount_confidence": 0.88, "mount_reason": reasons}

    # ── [S] S 마운트 ──
    s_kw = [
        "LEICA S ", "LEICA S(", "S TYP 006", "S TYP 007",
        "SUMMARIT-S", "VARIO-ELMAR-S", "SUPER-ELMAR-S", "ELMAR-S",
        "APO-MACRO-SUMMARIT-S", "LEICA S-E",
        "ELMARIT-S", "APO-ELMARIT-S",   # S 마운트 렌즈 suffix
    ]
    for kw in s_kw:
        if kw in n:
            hit("S_kw", kw)
            return {"mount": "S", "mount_confidence": 0.95, "mount_reason": reasons}

    # "LEICA S NN/" 충무로식 S 약식
    if re.search(r'\bLEICA\s+S\s+\d{2,3}[/.]', n):
        hit("S_leica_s_prefix", "LEICA S NN/")
        return {"mount": "S", "mount_confidence": 0.92, "mount_reason": reasons}

    # S 렌즈의 CS leaf-shutter 표기는 M 렌즈 패밀리명보다 먼저 고정한다.
    if " CS" in n and any(x in n for x in [
        "SUMMARIT", "ELMARIT", "SUPER-ELMAR", "VARIO-ELMAR",
        "APO-MACRO", "APO-ELMAR",
    ]):
        hit("S_cs_lens", "S lens CS")
        return {"mount": "S", "mount_confidence": 0.91, "mount_reason": reasons}

    legacy_abbrev = _detect_legacy_mount_abbrev(n, raw)
    if legacy_abbrev:
        mount_value, confidence, reason_label, reason_kw = legacy_abbrev
        hit(reason_label, reason_kw)
        return {"mount": mount_value, "mount_confidence": confidence, "mount_reason": reasons}

    shorthand = _detect_shorthand_mount(n, raw)
    if shorthand:
        mount_value, confidence, reason_label, reason_kw = shorthand
        hit(reason_label, reason_kw)
        return {"mount": mount_value, "mount_confidence": confidence, "mount_reason": reasons}

    # ── [Q] Q 시스템 ──
    if re.search(r'\bQ[23P]?\b', n) and "LEICA" in n:
        hit("Q_kw", "Q/Q2/Q3")
        return {"mount": "Q", "mount_confidence": 0.93, "mount_reason": reasons}

    # ── [SL] SL / L-Mount 마운트 ──
    sl_explicit = [
        "SL2", "SL3", "LEICA SL",
        "VARIO-ELMARIT-SL", "APO-VARIO-ELMARIT-SL",
        "SUMMILUX-SL", "SUMMICRON-SL", "ELMARIT-SL", "APO-SUMMICRON-SL",
        "L-MOUNT", "L MOUNT",
        "LEICA TL", "LEICA CL",
        "SUMMILUX-TL", "SUMMICRON-TL", "ELMARIT-TL",
        "SUPER-VARIO-ELMAR-TL",
    ]
    for kw in sl_explicit:
        if kw in n:
            hit("SL_explicit", kw)
            return {"mount": "SL", "mount_confidence": 0.96, "mount_reason": reasons}

    # Sigma / Panasonic / Lumix L-mount
    if any(x in n for x in ["SIGMA", "PANASONIC", "LUMIX"]):
        if any(x in n for x in ["DG DN", "DC DN", "L MOUNT", "L-MOUNT", "FOR L", "L마운트", "L 마운트"]):
            hit("SL_3rd_explicit", "sigma/panasonic+L_mount")
            return {"mount": "SL", "mount_confidence": 0.93, "mount_reason": reasons}
        if re.search(r'\bS\s*(PRO|1|5|1R|1H|5II|5M2)\b', n) or "LUMIX S" in n:
            hit("SL_lumix_s", "LUMIX S-series")
            return {"mount": "SL", "mount_confidence": 0.90, "mount_reason": reasons}
        if "DG HSM" in n or "DG DN" in n:
            hit("SL_sigma_dg", "SIGMA DG HSM/DN")
            return {"mount": "SL", "mount_confidence": 0.87, "mount_reason": reasons}

    l_family = _detect_l_family_mount(n)
    if l_family:
        mount_value, confidence, reason_label, reason_kw = l_family
        hit(reason_label, reason_kw)
        return {"mount": mount_value, "mount_confidence": confidence, "mount_reason": reasons}

    # ── [PNS] 필름 자동카메라 ──
    pns_kw = [
        "MINILUX", "CM ZOOM", "LEICA CM ", "LEICA C1 ", "LEICA C2 ",
        "AF-C1", "LEICA MINI ", "C2 ZOOM", "CM-ZOOM",
    ]
    for kw in pns_kw:
        if kw in n:
            hit("PNS_kw", kw)
            return {"mount": "PNS", "mount_confidence": 0.93, "mount_reason": reasons}

    # ── [Compact] 디지털 컴팩트 ──
    compact_kw = [
        "D-LUX", "DLUX", "C-LUX", "DIGILUX",
        "LEICA X1", "LEICA X2", "LEICA X ", "X TYP", "X-U ",
        "X VARIO", "V-LUX", "SOFORT",
        "LEICA T ", "LEICA TL", "LEICA CL",
    ]
    for kw in compact_kw:
        if kw in n:
            hit("Compact_kw", kw)
            return {"mount": "Compact", "mount_confidence": 0.93, "mount_reason": reasons}

    # ── [L] Barnack 나사마운트 (LTM / L39 / M39) ──
    l_explicit = [
        "L39", "M39", "SCREW MOUNT", "나사마운트",
        "LTM", "SUMMITAR", "BARNACK",
        "LEICA IF", "LEICA IIF", "ERNST LEITZ",
        "3.5CM", "7.3CM", "9CM ", "13.5CM",
        "CARL ZEISS JENA",
        "SUMMCRON-C", "SUMMICRON-C",
        "THAMBAR", "KE-7A",
        # Cooke 렌즈 (LTM 구형)
        "COOKE",
        # Carl Zeiss C (Contax/LTM — Zeiss ZM과 구분)
        # ZM은 M mount이지만 "C" 모델(Contax 마운트 변환)은 LTM
        # 단, "CARL ZEISS C " 패턴이 있는 경우만
    ]
    for kw in l_explicit:
        if kw in n:
            hit("L_explicit", kw)
            return {"mount": "L", "mount_confidence": 0.95, "mount_reason": reasons}

    # Carl Zeiss "C" 모델 (Contax/LTM) — ZM(M mount)과 구분
    # "Carl Zeiss C 50mm", "Zeiss C-Sonnar", "Zeiss C Biogon" 등
    if "CARL ZEISS" in n and re.search(
        r'\bC\s+\d|\bC[-\s]SONNAR\b|\bC[-\s]BIOGON\b|\bC[-\s]PLANAR\b', n
    ):
        if "ZM" not in n and "L-MOUNT" not in n:
            hit("L_zeiss_c_model", "carl_zeiss_C_model")
            return {"mount": "L", "mount_confidence": 0.85, "mount_reason": reasons}

    # "LEICA I/II/III" 바디 명시
    if re.search(r'\bLEICA\s+(I\b|IF\b|IIF?\b|III[ABCDFG]?\b|STANDARD\b)', n):
        hit("L_barnack_body", "LEICA I/II/III")
        return {"mount": "L", "mount_confidence": 0.93, "mount_reason": reasons}

    # "LEICA L NN" prefix → 나사마운트 렌즈 (SL 아님)
    if re.search(r'\bLEICA\s+L\s+\d', n):
        hit("L_leica_l_prefix", "LEICA L NN")
        return {"mount": "L", "mount_confidence": 0.90, "mount_reason": reasons}

    # 충무로식 L 약식: "L 50/", "L 35/" 등
    if re.search(r'(?<![A-Z])L\s+\d{2,3}[/.]', n):
        hit("L_chungmuro", "L NN/")
        return {"mount": "L", "mount_confidence": 0.88, "mount_reason": reasons}

    # ── [V] Hasselblad V 마운트 ──
    if brand == "Hasselblad" or "HASSELBLAD" in n:
        hit("V_hasselblad", "hasselblad")
        return {"mount": "V", "mount_confidence": 0.93, "mount_reason": reasons}

    # ══════════════════════════════════════════
    # M 마운트: 렌즈 키워드가 여기서 처음 체크된다.
    # 위 R/L/SL 체크를 통과한 것만 M으로 판단한다.
    # ══════════════════════════════════════════

    # M 바디 명시 패턴 (접두어 제거 후 M으로 시작)
    if re.match(r'^M[2-9]\b|^M1[0-9]\b|^MP\b|^M-A\b|^MA\b|^M-D\b|^M-E\b|^M-P\b|^M240\b|^MONOCHROM\b', raw):
        hit("M_body_explicit", "M-body")
        return {"mount": "M", "mount_confidence": 0.97, "mount_reason": reasons}

    if re.search(r'\bMDA\b', raw):
        hit("M_body_explicit", "MDA")
        return {"mount": "M", "mount_confidence": 0.93, "mount_reason": reasons}

    # "LEICA M" prefix
    if re.search(r'\bLEICA\s+M\b', n):
        hit("M_leica_m_prefix", "LEICA M")
        return {"mount": "M", "mount_confidence": 0.96, "mount_reason": reasons}

    # M 마운트 렌즈 키워드 (R suffix 없는 것만 여기 도달)
    m_lens_kw = [
        "SUMMICRON",     # -R 없는 것만 여기 도달
        "SUMMILUX",
        "NOCTILUX",
        "ELMARIT-M", "SUMMARIT-M",
        "SUMMARON", "SUPER-ANGULON",
        "APO-SUMMICRON",
        "APO-TELYT-M",
        "VM ", " ZM ", "M ROKKOR", "ELCAN", "COLLAPSIBLE",
        "LIGHT LENS LAB",
        "ARTIZLAB", "MS-OPTICS", "MS OPTICS",
        "MEYER OPTIK",
        "LEICAVIT", "VIT M",
        # 서드파티 M mount 브랜드
        "TTARTISAN", "7ARTISANS", "7 ARTISANS",
        "THYPOCH",
        "FUNLEADER",
        "KAMLAN",
        "HANDEVISION",
        "PERGEAR",
        "NISI",
        "MEIKE",
        "VENUS OPTICS", "LAOWA",
        "PIXII",
        # 추가 M mount alias
        "M-HEXANON", "M HEXANON",  # Konica M mount (M-Hexanon만, 일반 Hexanon은 L)
        "PEACE",                    # Peace 렌즈 (M mount)
        "MANDLER",                  # Mandler Optics (M mount)
        "COIRO",                    # Coiro (M mount 호환 와인더 제외)
        "POLAR",                    # Polar 렌즈 (M mount)
        "MINOX",                    # Minox M mount 렌즈
        "HELIAR",                   # Voigtlander Heliar (M mount)
        "COLOR SKOPAR",             # Voigtlander Color-Skopar
        "ULTRA WIDE HELIAR",
        "SUPER WIDE HELIAR",
        "SEPTON",                   # Voigtlander Septon
        "SKOPAR",
    ]
    for kw in m_lens_kw:
        if kw in n:
            hit("M_lens_kw", kw)
            return {"mount": "M", "mount_confidence": 0.92, "mount_reason": reasons}

    # Leica M 바디 번호 (M3~M11)
    if any(re.search(rf'\b{kw}\b', n) for kw in
           [" M3", " M4", " M5", " M6", " M7", " M8", " M9", " M10", " M11",
            "LEICA MP", "LEICA MA", "LEICA M-A"]):
        hit("M_body_number", "M3-M11")
        return {"mount": "M", "mount_confidence": 0.95, "mount_reason": reasons}

    # Voigtlander → M (finder/meter 제외)
    if any(x in n for x in ["VOIGTLANDER", "보이그랜더"]):
        if not any(x in n for x in ["FINDER", "METER", "파인더"]):
            hit("M_voigtlander", "voigtlander")
            return {"mount": "M", "mount_confidence": 0.88, "mount_reason": reasons}

    # Zeiss ZM → M
    if "ZEISS" in n and "CARL ZEISS JENA" not in n:
        hit("M_zeiss_zm", "zeiss")
        return {"mount": "M", "mount_confidence": 0.85, "mount_reason": reasons}

    # Konica Hexanon LTM (M-Hexanon이 아닌 일반 Hexanon) → L
    if "HEXANON" in n and "M-HEXANON" not in n and "M HEXANON" not in n:
        hit("L_hexanon_ltm", "hexanon_ltm")
        return {"mount": "L", "mount_confidence": 0.82, "mount_reason": reasons}

    # 충무로식 M 약식: "M50/", "M35/" 등
    if re.search(r'(?<![A-Z])M\d{2,3}[/.]', raw):
        hit("M_chungmuro", "MNN/")
        return {"mount": "M", "mount_confidence": 0.88, "mount_reason": reasons}

    # "M mount" / "M-mount" 명시
    if re.search(r'\bM[\s-]MOUNT\b', n):
        hit("M_mount_explicit", "M mount")
        return {"mount": "M", "mount_confidence": 0.90, "mount_reason": reasons}

    # "for M" / "for Leica M" 명시 (서드파티 렌즈 상품명 패턴)
    if re.search(r'\bFOR\s+(LEICA\s+)?M\b', n):
        hit("M_for_m", "for M")
        return {"mount": "M", "mount_confidence": 0.88, "mount_reason": reasons}

    # "M 마운트" 한국어 (n은 .upper() 기준)
    if "M 마운트" in n or "M마운트" in n:
        hit("M_korean_mount", "M 마운트")
        return {"mount": "M", "mount_confidence": 0.88, "mount_reason": reasons}

    # 한국어 "라이카 M" 패턴 (upper 기준: 한글은 대소문자 없음)
    if "라이카 M" in n or "라이카M" in n:
        hit("M_korean_leica_m", "라이카 M")
        return {"mount": "M", "mount_confidence": 0.88, "mount_reason": reasons}

    # " M" 단독 후치 표기 — 상품명 끝에 " M"으로 끝나거나 " M " 사이에 있는 경우
    # 단, 조리개값(f/M 등), 단위(MM) 오탐 방지
    # 예: "Thypoch Simera 35mm f/1.4 M", "Simera 28mm f/5.6 M"
    if re.search(r'(?<=\s)M\s*$', raw) or re.search(r'\s+M\s+(?:BLACK|SILVER|CHROME|BODY|LENS)\b', n):
        hit("M_trailing", "trailing M")
        return {"mount": "M", "mount_confidence": 0.82, "mount_reason": reasons}
    if "6BIT" in n and "LEICA" in n:
        hit("M_6bit", "6bit")
        return {"mount": "M", "mount_confidence": 0.87, "mount_reason": reasons}

    reasons.append("no_mount_match")
    return {"mount": "Unknown", "mount_confidence": 0.30, "mount_reason": reasons}


# ─────────────────────────────────────────────
# 4. detect_category
# ─────────────────────────────────────────────

# 명백한 악세사리 코드/키워드 (detect_mount에서 이관)
_ACCESSORY_CODES = {
    "itooy", "irooa", "sbooi", "viooh", "sbloo", "sgvoo", "iufoo",
    "xooim", "sgood", "sbkoo", "shooc", "sootf", "soogz", "saioo",
    "elpro", "vtroo", "fookh", "fison", "tooca", "valoo", "itdoo",
    "12585", "12504", "12501", "14464", "14066", "12522", "12526",
    "12564", "12575", "12595", "14100", "14269", "14358",
}

_HARD_ACC_PHRASES = (
    # 어댑터/익스텐더
    "adapter", "어댑터",
    "extender", "익스텐더",
    # 케이스/백/스트랩
    "bag", "가방", "case", "케이스", "pouch", "파우치",
    "holster", "shoulder bag", "wrist strap", "neck strap",
    "포토백", "카메라백",
    # 그립/프로텍터/플레이트
    "protector", "thumb support", "thumbs support",
    "thumb grip", "thumbs grip",
    "handgrip", "hand grip", "thumbs up", "thumb up",
    "grip",
    "base plate", "l-plate", "plate",
    "플레이트",
    "quick release",
    # 후드/파인더
    "hood", "후드",
    "finder", "viewfinder", "view finder", "파인더",
    # 필터
    "filter", "필터", "polariz", "polfilter",
    # Visoflex/플래시/EVF
    "visoflex",
    "flash", "플래시",
    "evf", "electronic viewfinder",
    # 기타 물리 악세사리
    "strap", "스트랩",
    "cover", "커버",
    "diopter", "correction lens",
    "motor winder", "rapidwinder",
    "leicavit",
    "soft release", "release button",
    "soft button", "소프트버튼",
    "hot shoe", "cold shoe",
    "hand strap",
    "winder",
    "cable release",
    "remote",
    "gimbal", "stabilizer", "cage", "케이지",
    "tripod", "트라이포드",
    "holster", "홀스터",
    "엄지그립", "엄지그림",
)

_HARD_ACC_REGEX = (
    (r'\be\d{2,3}\s+uva(?:\s+ii)?\b', "e_uv_filter"),
    (r'\buva(?:\s+ii)?\b', "uva"),
    (r'\buv(?:/ir)?\b', "uv"),
    (r'\buvir\b', "uvir_filter"),
    (r'\b(?:nd|skylight|yellow)\s+(?:filter|fiter)\b', "optical_filter"),
    (r'\bb\+w\b.*\b(?:nd|uv|filter|fiter)\b', "bw_filter"),
    (r'\bpl\s+e\d{2}\b', "polarizing_filter"),
    (r'\b(?:light|exposure)\s+meter\b|\bmeter\b', "meter"),
    (r'\bsekonic\b', "sekonic_meter"),
    (r'\brig\b|\bcamera\s+rig\b|\bdji\s+rs\s*\d\b', "rig"),
    (r'\bsf[-\s]?(?:20|24d?|26|40|58|60|64|c1)\b', "flash_code"),
    (r'\bbp-scl\d+\b', "battery_code"),
    (r'\b(?:leica\s+)?m\s+motor\b|\bmotor\s+m\b', "motor_winder"),
    (r'\bbooks?\b', "book"),
)


_ACCESSORY_PRIMARY_REGEX = (
    (r'\blens\s+hood\b', "lens_hood_primary"),
    (r'\bleica\s*hood\b[^+]{0,80}\b\d{5}[a-z]?\b', "leicahood_code"),
    (r'\bhood\b[^+]{0,80}\bfor\b', "hood_for_lens"),
    (r'\b(?:for|용)\b[^+]{0,80}(?:\bhood\b|후드)', "for_hood"),
    (r'\b\d{5}[a-z]?\b[^+]{0,80}\bhood\b|\bhood\b[^+]{0,80}\b\d{5}[a-z]?\b', "hood_code"),
    (r'\b\d{5}[a-z]?\b[^+]{0,80}후드|후드[^+]{0,80}\b\d{5}[a-z]?\b', "hood_code_kr"),
)


def _iter_hard_accessory_hits(combined: str):
    for kw in _HARD_ACC_PHRASES:
        if kw in combined:
            yield ("kw", kw)
    for pattern, label in _HARD_ACC_REGEX:
        if re.search(pattern, combined):
            yield ("rx", label)

_ACCESSORY_KW = [
    # 물리적 부속
    "후드", "스트랩", "파인더", "파우치", "충전기", "배터리",
    "어댑터", "케이블", "케이스", "그립", "커버",
    "hood", "strap", "viewfinder", "view finder", "finder",
    "adapter", "pouch", "charger", "battery", "cable",
    "case", "grip", "cover",
    "flash", "플래시",
    # 캡/필터
    "front cap", "rear cap", "리어캡", "프론트캡",
    "lens cap", "body cap", "eye cup",
    "uv filter", "polariz", "polfilter",
    # 악세사리 전용 제품
    "leicavit", "rapidwinder", "rapid winder",
    "visoflex",
    "evf2", "evf 2",
    "sf20","sf24","sf26","sf40","sf58","sf64","sf60",
    "handgrip", "hand grip", "thumbs up", "thumb up",
    "diopter", "correction lens",
    "motor winder", "trigger",
    "tripod", "ball head", "tabletop",
    "holster", "wrist strap", "neck strap",
    "wotancraft", "oberwerth", "ona bag",
    "ultravid", "ultravd", "geovid", "trinovid",
    "10x25", "10×25",
    "150 jahre", "stemar", "stereo midland",
    "be@rbrick",
    "novoflex",
    # 코드네임 항목
    "televid",
]

_LENS_PROTECT_KW = [
    # Leica 렌즈 패밀리
    "summicron", "summilux", "noctilux", "elmarit", "elmar",
    "summaron", "super-angulon", "angulon", "summarit",
    "hektor", "summitar", "nokton", "voigtlander",
    # 조리개 표기 패턴
    "f0.", "f1.", "f2.", "f3.", "f4.",
    # 시리얼 / 개별 렌즈 신호
    " sn.", " sn ",
    # 마운트 명시 → 렌즈로 보호
    "m mount", "m-mount", "l mount", "l-mount",
    "r mount", "r-mount", "sl mount",
    "for leica m", "for m",
    "m 마운트", "m마운트",
    # 서드파티 M mount 브랜드 (렌즈 보호)
    "ttartisan", "7artisans", "thypoch", "funleader",
    "kamlan", "handevision", "pergear", "nisi",
    "ms-optics", "ms optics", "artizlab",
    "light lens lab",
]

_BODY_KW = [
    "body", "바디",
    # M 바디
    "leica m3", "leica m2", "leica m4", "leica m5", "leica m6",
    "leica m7", "leica mp", "leica m-a", "leica ma",
    "leica m8", "leica m9", "leica m10", "leica m11", "leica m240",
    "mda", "leica mda",
    "typ 240",
    # R 바디
    "r3 ", "r4 ", "r5 ", "r6 ", "r7 ", "r8 ", "r9 ",
    "leicaflex",
    # Barnack 바디
    "leica i ", "leica ii", "leica iii",
    "leica if", "leica iif", "leica iiif", "leica iiig", "leica iiic",
    "leica iiia", "leica iiib", "leica standard",
    "barnack",
    # SL/Q 바디 — "leica sl"은 렌즈에도 등장하므로 body_kw에서 제외,
    # mount=SL + category 판단은 mount 신호로만 처리
    "leica q ", "leica q2", "leica q3",
]

# Barnack 바디 강제 키워드 (렌즈 protect 무시하고 Body 우선)
_BARNACK_BODY_KW = [
    "barnack", "leica iiif", "leica iiig", "leica iiic",
    "leica iiia", "leica iiib", "leica standard",
    "leica iif", "leica if",
]


def detect_category(
    normalized_name: str,
    normalized_description: Optional[str] = None,
    brand: Optional[str] = None,
    mount: Optional[str] = None,
    price_str: Optional[str] = None,
) -> dict:
    """
    Lens / Body / Accessory / Unknown 판단.
    - Accessory 최우선
    - detect_mount에서 넘어온 Accessory 케이스를 여기서 처리
    - 세부 label 판단 금지

    Returns:
        category: str
        category_confidence: float
        category_reason: list[str]
    """
    n = normalized_name.lower()
    desc = (normalized_description or "").lower()
    combined = n + " " + desc
    reasons = []

    # ══════════════════════════════════════════════════════════════
    # 설계 원칙:
    #   Accessory 판정이 category의 최최우선이다.
    #   mount 신호는 Accessory 판정을 막지 않는다.
    #   compatibility(compatible_mounts/systems)는 category=Accessory
    #   확정 후 accessory_classifier에서만 계산한다.
    # ══════════════════════════════════════════════════════════════

    # ── 0순위: 악세사리 코드네임 (무조건 Accessory) ──
    for code in _ACCESSORY_CODES:
        if code in combined:
            reasons.append(f"acc_code:{code}")
            return {"category": "Accessory", "category_confidence": 0.99, "category_reason": reasons}

    # ── 0.5순위: Barnack 바디 강제 → Body (렌즈 키워드보다 우선) ──
    for kw in _BARNACK_BODY_KW:
        if kw in combined:
            reasons.append(f"barnack_body_kw:{kw}")
            return {"category": "Body", "category_confidence": 0.93, "category_reason": reasons}

    # ── 렌즈 보호 판단 (mount 신호는 포함하지 않음) ──────────────
    # 핵심: mount=M이라도 "Leica M Adapter L"은 Accessory여야 한다.
    # → is_protected_by_mount 제거. mount 신호는 category 판단에 영향 없음.
    has_aperture = bool(re.search(r'f\s*\d+[\./]\d+|f\d+[\./]\d+|1:\d+[\./]\d+', combined))
    has_lens_kw  = any(kw in combined for kw in _LENS_PROTECT_KW)
    has_focal    = bool(re.search(r'\d{2,3}\s*mm', combined))

    # 강한 렌즈 보호: (조리개 + 초점거리) 또는 렌즈 패밀리 키워드
    is_lens_protected_strong = (has_aperture and has_focal) or has_lens_kw
    # 약한 렌즈 보호: 조리개 또는 초점거리 단독 (가격 판단만 막음)
    is_lens_protected_weak   = has_aperture or has_focal

    # ── 0.8순위: accessory 본품 제목 패턴 ─────────────────────
    # "Lens Hood", "Hood ... for M 50mm", "12586 ... Hood"는
    # 렌즈 모델/초점거리/조리개가 compatibility 설명으로 들어와도
    # 상품 정체성은 후드다. 반면 "Lens + Hood" 번들형은 Lens로 유지한다.
    for pattern, label in _ACCESSORY_PRIMARY_REGEX:
        if re.search(pattern, combined):
            reasons.append(f"primary_acc_rx:{label}")
            return {"category": "Accessory", "category_confidence": 0.98, "category_reason": reasons}

    # ── 1순위: 강제 Accessory 신호 ────────────────────────────
    # 이 신호들은 mount/system/숫자/mm 신호보다 먼저 category를 확정한다.
    for hit_type, signal in _iter_hard_accessory_hits(combined):
        # 단, 렌즈 본품 + hood 세트로 강하게 보이는 경우만 기존 보호를 유지한다.
        if is_lens_protected_strong and signal in {"hood", "후드"}:
            if has_aperture and has_focal and has_lens_kw:
                continue
        reasons.append(f"hard_acc_{hit_type}:{signal}")
        return {"category": "Accessory", "category_confidence": 0.97, "category_reason": reasons}

    # ── 2순위: 일반 Accessory 키워드 (강한 렌즈 보호 없을 때만) ──
    for kw in _ACCESSORY_KW:
        if kw in combined and not is_lens_protected_strong:
            reasons.append(f"acc_kw:{kw}")
            return {"category": "Accessory", "category_confidence": 0.92, "category_reason": reasons}

    # 캡/필터 (강한 렌즈 보호 없을 때만)
    if any(x in combined for x in ["캡", "cap", "filter", "필터"]) and not is_lens_protected_strong:
        reasons.append("cap_filter")
        return {"category": "Accessory", "category_confidence": 0.88, "category_reason": reasons}

    # ── 3순위: mount=Compact/PNS/Q → Body ──
    # 이 분기는 _HARD_ACC_KW를 통과한 것만 도달하므로
    # hood/case/protector 등은 이미 위에서 Accessory로 빠져있다.
    if mount in ("Compact", "PNS", "Q"):
        reasons.append(f"mount_compact_pns_q:{mount}")
        return {"category": "Body", "category_confidence": 0.90, "category_reason": reasons}

    # ── 4순위: 가격 기반 Accessory ──
    # 약한 렌즈 보호 있으면 스킵 (서드파티 렌즈 저가 보호)
    if not is_lens_protected_weak and price_str and price_str not in ("문의요망", ""):
        try:
            nums = re.findall(r"[\d,]+", price_str.replace("£", ""))
            if nums:
                price_val = float(nums[0].replace(",", ""))
                if 0 < price_val <= 200000:
                    reasons.append(f"price_low:{price_val}")
                    return {"category": "Accessory", "category_confidence": 0.75, "category_reason": reasons}
        except Exception:
            pass

    # ── 5순위: Body 키워드 ──
    for kw in _BODY_KW:
        if kw in combined:
            reasons.append(f"body_kw:{kw}")
            return {"category": "Body", "category_confidence": 0.88, "category_reason": reasons}

    # ── 6순위: 렌즈 fallback ──
    if is_lens_protected_strong or is_lens_protected_weak:
        reasons.append("lens_protected")
        return {"category": "Lens", "category_confidence": 0.85, "category_reason": reasons}

    reasons.append("default_lens")
    return {"category": "Lens", "category_confidence": 0.60, "category_reason": reasons}


# ─────────────────────────────────────────────
# 5. auto_label
# ─────────────────────────────────────────────

def auto_label(
    normalized_name: str,
    normalized_description: Optional[str] = None,
    brand: Optional[str] = None,
    mount: Optional[str] = None,
    category: Optional[str] = None,
) -> dict:
    """
    이미 계산된 brand / mount / category를 받아 최종 label만 결정.

    원칙:
      category > mount > brand > label 세부화
      확실한 정보만 사용, 불확실하면 더 일반적인 label로 fallback
      brand/mount/category 재판단 금지
      model명/variant는 label에 넣지 않음

    Returns:
        label: str                 (VALID_LABELS 중 하나)
        label_confidence: float
        label_reason: list[str]
    """
    reasons = []
    b = brand or "Unknown"
    m = mount or "Unknown"
    cat = category or "Unknown"

    def ret(label, conf, reason):
        reasons.append(reason)
        assert label in VALID_LABELS, f"invalid label: {label}"
        return {"label": label, "label_confidence": conf, "label_reason": reasons}

    # ── 1순위: Accessory ──
    if cat == "Accessory":
        return ret("Accessory", 0.99, "category=Accessory")

    # ── 2순위: mount + category ──
    if cat == "Lens":
        if m == "M":
            if b == "3rd Party":
                return ret("3rd Party M Lens", 0.95, "3rd_party+M+Lens")
            return ret("M Lens", 0.95, "M+Lens")
        if m == "R":
            return ret("R Lens", 0.95, "R+Lens")
        if m == "L":
            return ret("L Lens", 0.93, "L+Lens")
        if m == "SL":
            return ret("SL Lens", 0.93, "SL+Lens")
        if m == "S":
            return ret("S Lens", 0.93, "S+Lens")
        if m == "V":
            return ret("V Lens", 0.93, "V+Lens")

    if cat == "Body":
        if m == "M":
            return ret("M Body", 0.95, "M+Body")
        if m == "R":
            return ret("R Body", 0.95, "R+Body")
        if m == "L":
            return ret("L Body", 0.93, "L+Body")
        if m == "SL":
            return ret("SL Body", 0.93, "SL+Body")
        if m == "S":
            return ret("S Body", 0.93, "S+Body")
        if m == "V":
            return ret("V Body", 0.93, "V+Body")
        # Compact/PNS/Q → Body로 처리 (mount 세부 label 없음)
        if m in ("Compact", "PNS", "Q"):
            if b == "Leica":
                return ret("Leica Body", 0.88, f"Leica+{m}+Body")
            return ret("Body", 0.80, f"{m}+Body_no_mount_label")

    # ── 3순위: brand + category (mount=Unknown일 때) ──
    if cat == "Lens":
        if b == "Leica":
            return ret("Leica Lens", 0.82, "Leica+Lens+no_mount")
        if b == "Leitz":
            return ret("Leica Lens", 0.80, "Leitz+Lens")
        if b == "Hasselblad":
            return ret("Hasselblad Lens", 0.88, "Hasselblad+Lens")
        if b == "Canon":
            return ret("Canon Lens", 0.85, "Canon+Lens")
        if b == "Nikon":
            return ret("Nikon Lens", 0.85, "Nikon+Lens")
        if b == "Zeiss":
            return ret("Zeiss Lens", 0.85, "Zeiss+Lens")
        if b == "Voigtlander":
            return ret("Voigtlander Lens", 0.85, "Voigtlander+Lens")
        if b == "3rd Party":
            return ret("3rd Party Lens", 0.82, "3rd_party+Lens+no_mount")

    if cat == "Body":
        if b == "Leica":
            return ret("Leica Body", 0.82, "Leica+Body+no_mount")
        if b == "Hasselblad":
            return ret("Hasselblad Body", 0.88, "Hasselblad+Body")
        if b == "Canon":
            return ret("Canon Body", 0.85, "Canon+Body")
        if b == "Nikon":
            return ret("Nikon Body", 0.85, "Nikon+Body")
        if b == "3rd Party":
            return ret("3rd Party Body", 0.78, "3rd_party+Body")

    # ── 4순위: category-only ──
    if cat == "Lens":
        return ret("Lens", 0.60, "Lens_only")
    if cat == "Body":
        return ret("Body", 0.60, "Body_only")

    # ── 5순위: Unknown ──
    return ret("Unknown", 0.30, "all_unknown")


# ─────────────────────────────────────────────
# 6. extract_flags
# ─────────────────────────────────────────────

_RISK_FLAGS = {
    "fungus":          ["곰팡이", "fungus", "fungi", "fungal"],
    "haze":            ["헤이즈", "haze", "haziness", "무화", "안개"],
    "separation":      ["분리", "separation", "balsam separation", "element separation"],
    "repair":          ["수리", "repair", "repaired", "수리품", "수리필요"],
    "repaint":         ["리페인트", "repaint", "재도색"],
    "modified":        ["개조", "modified", "modification"],
    "no_serial":       ["무각인", "no serial", "serial removed", "시리얼 제거"],
    "not_working":     ["작동불가", "not working", "broken", "고장"],
    "scratch":         ["스크래치", "scratch", "scratched"],
    "dent":            ["덴트", "dent", "dented"],
    "dust":            ["먼지", "dust", "내부먼지"],
    "coating_worn":    ["코팅마모", "coating worn", "coating damage"],
}

_POSITIVE_FLAGS = {
    "cla":             ["cla", "클리닝", "cleaning adjustment", "cleaned"],
    "serviced":        ["서비스", "serviced", "overhaul", "오버홀"],
    "receipt":         ["영수증", "receipt", "invoice", "정품"],
    "box":             ["박스", "box", "original box", "오리지널 박스"],
    "mint":            ["민트", "mint", "미사용", "like new"],
}


def extract_flags(
    normalized_name: str,
    normalized_description: Optional[str] = None,
) -> dict:
    """
    상태/진위 관련 플래그 추출.
    label/brand/mount 판단 금지.

    Returns:
        risk_flags: list[str]
        positive_flags: list[str]
        flag_confidence: float
    """
    combined = (normalized_name + " " + (normalized_description or "")).lower()
    risk, positive = [], []

    for flag, kws in _RISK_FLAGS.items():
        if any(kw in combined for kw in kws):
            risk.append(flag)

    for flag, kws in _POSITIVE_FLAGS.items():
        if any(kw in combined for kw in kws):
            positive.append(flag)

    conf = 0.90 if risk or positive else 0.50
    return {"risk_flags": risk, "positive_flags": positive, "flag_confidence": conf}


# ─────────────────────────────────────────────
# 7. classify_sold_quality
# ─────────────────────────────────────────────

def classify_sold_quality(
    status_raw: Optional[str] = None,
    title_raw: Optional[str] = None,
    description_raw: Optional[str] = None,
    price_raw=None,
) -> dict:
    """
    sold 상태만 분류. brand/mount/label 판단 금지.

    sold_quality 값:
      asking / sold_confirmed / sold_likely / ended_unsold / expired_unknown

    Returns:
        sold_quality: str
        sold_confidence: float
        sold_reason: list[str]
    """
    combined = " ".join(filter(None, [
        str(status_raw or ""),
        str(title_raw or ""),
        str(description_raw or ""),
    ])).lower()
    reasons = []

    SOLD_CONFIRMED = ["판매완료", "sold out", "sold", "품절", "판매됨"]
    SOLD_LIKELY    = ["예약중", "보류", "reserved", "pending"]
    ENDED_UNSOLD   = ["종료", "ended", "expired", "listing ended"]

    for kw in SOLD_CONFIRMED:
        if kw in combined:
            reasons.append(f"sold_confirmed:{kw}")
            return {"sold_quality": "sold_confirmed", "sold_confidence": 0.97, "sold_reason": reasons}

    for kw in SOLD_LIKELY:
        if kw in combined:
            reasons.append(f"sold_likely:{kw}")
            return {"sold_quality": "sold_likely", "sold_confidence": 0.80, "sold_reason": reasons}

    for kw in ENDED_UNSOLD:
        if kw in combined:
            reasons.append(f"ended_unsold:{kw}")
            return {"sold_quality": "ended_unsold", "sold_confidence": 0.75, "sold_reason": reasons}

    reasons.append("default_asking")
    return {"sold_quality": "asking", "sold_confidence": 0.85, "sold_reason": reasons}


# ─────────────────────────────────────────────
# 8. classify_listing_v2  (오케스트레이터)
# ─────────────────────────────────────────────

def classify_listing_v2(raw_item: dict) -> dict:
    """
    raw_item → classified listing (v2 schema)

    파이프라인 순서:
      normalize_text
      -> detect_brand
      -> detect_mount
      -> detect_category
      -> auto_label
      -> extract_flags
      -> classify_sold_quality

    raw_item 예상 필드:
      상품명 (str)              필수
      가격 (str)                optional
      통화 (str)                optional
      이미지 (str)              optional
      링크 (str)                optional
      site (str)               optional
      컨디션 (str)              optional
      품절 (bool)               optional
      description (str)        optional

    출력 스키마 (고정):
      # 원본
      source
      source_url
      title_raw
      price_raw
      currency
      image_url
      condition_raw
      # 정규화
      normalized_name
      normalized_description
      # 분류 결과
      brand / brand_confidence / brand_reason
      mount / mount_confidence / mount_reason
      category / category_confidence / category_reason
      label / label_confidence / label_reason
      # 플래그
      risk_flags / positive_flags / flag_confidence
      # sold
      sold_quality / sold_confidence / sold_reason
      # 메타
      crawl_time / first_seen
    """
    # ── 원본 필드 추출 ──
    title_raw   = raw_item.get("상품명", "")
    price_raw   = raw_item.get("가격", "")
    currency    = raw_item.get("통화", "")
    image_url   = raw_item.get("이미지", "")
    source_url  = raw_item.get("링크", "")
    source      = raw_item.get("site", "")
    condition   = raw_item.get("컨디션", "")
    description = raw_item.get("description", "")
    is_sold     = raw_item.get("품절", False)
    crawl_time  = raw_item.get("crawl_time", "")
    first_seen  = raw_item.get("first_seen", crawl_time)

    # ── 파이프라인 실행 ──
    norm    = normalize_text(title_raw, description)
    nn      = norm["normalized_name"]
    nd      = norm["normalized_description"]

    br      = detect_brand(nn, nd)
    mt      = detect_mount(nn, nd, brand=br["brand"])
    cat     = detect_category(nn, nd, brand=br["brand"], mount=mt["mount"], price_str=price_raw)
    lbl     = auto_label(nn, nd, brand=br["brand"], mount=mt["mount"], category=cat["category"])
    mdl     = detect_model(nn, nd, category=cat["category"], mount=mt["mount"])
    flags   = extract_flags(nn, nd)
    sold    = classify_sold_quality(
        status_raw="품절" if is_sold else None,
        title_raw=title_raw,
        description_raw=description,
        price_raw=price_raw,
    )

    # Accessory 전용 분류 (category=Accessory일 때만)
    acc = None
    if cat["category"] == "Accessory":
        acc = classify_accessory(nn, nd, mount=mt["mount"])

    return {
        # 원본
        "source":           source,
        "source_url":       source_url,
        "title_raw":        title_raw,
        "price_raw":        price_raw,
        "currency":         currency,
        "image_url":        image_url,
        "condition_raw":    condition,
        # 정규화
        "normalized_name":        nn,
        "normalized_description": nd,
        # 분류 — label 계층
        "brand":              br["brand"],
        "brand_confidence":   br["brand_confidence"],
        "brand_reason":       br["brand_reason"],
        "mount":              mt["mount"],
        "mount_confidence":   mt["mount_confidence"],
        "mount_reason":       mt["mount_reason"],
        "category":           cat["category"],
        "category_confidence":cat["category_confidence"],
        "category_reason":    cat["category_reason"],
        "label":              lbl["label"],
        "label_confidence":   lbl["label_confidence"],
        "label_reason":       lbl["label_reason"],
        # 모델 계층 (label 아래)
        "model_raw":      mdl["model_raw"],
        "model_canonical":mdl["model_canonical"],
        "variant":        mdl["variant"],
        "focal_length":   mdl["focal_length"],
        # Accessory 전용 (category=Accessory일 때만 값 있음)
        "accessory_type":     acc["accessory_type"]     if acc else None,
        "compatible_mounts":  acc["compatible_mounts"]  if acc else [],
        "compatible_systems": acc["compatible_systems"] if acc else [],
        # 플래그
        "risk_flags":         flags["risk_flags"],
        "positive_flags":     flags["positive_flags"],
        "flag_confidence":    flags["flag_confidence"],
        # sold
        "sold_quality":       sold["sold_quality"],
        "sold_confidence":    sold["sold_confidence"],
        "sold_reason":        sold["sold_reason"],
        # 메타
        "crawl_time":   crawl_time,
        "first_seen":   first_seen,
    }


# ─────────────────────────────────────────────
# 9. compare_v1_v2  (QA 비교용)
# ─────────────────────────────────────────────

def _qa_v2_likely_correct_note(
    title: str,
    v1_mount: str,
    v1_category: str,
    v2: dict,
) -> Optional[str]:
    """
    QA 비교 보조 해석.
    classifier 결과를 바꾸지 않고, v1 legacy/오염 가능성이 큰 mismatch만 표시한다.
    """
    mt_reason = " ".join(v2.get("mount_reason") or [])
    cat_reason = " ".join(v2.get("category_reason") or [])
    v2_mt = v2.get("mount")
    v2_cat = v2.get("category")

    if v1_mount == "Accessory" and v2_cat in ("Lens", "Body"):
        if "lens_protected" in cat_reason:
            return "v2_likely_correct:v1_accessory_but_lens_signals"
        if "body_kw" in cat_reason or "mount_compact_pns_q" in cat_reason:
            return "v2_likely_correct:v1_accessory_but_body_signals"

    if v2_cat == "Accessory" and "primary_acc_rx" in cat_reason:
        return "v2_likely_correct:accessory_primary_signal"

    if v2_cat == "Body" and v2_mt in ("PNS", "Compact", "Q"):
        if any(x in mt_reason for x in [
            "PNS_kw", "Compact_kw", "Q_kw", "Q_body_shorthand",
        ]):
            return "v2_likely_correct:explicit_compact_pns_body"

    if v2_mt == "M" and v2_cat == "Lens" and any(x in mt_reason for x in [
        "M_leica_m_prefix", "M_lens_shorthand", "M_legacy_shorthand",
        "M_for_m_body", "M_6bit",
    ]):
        return "v2_likely_correct:explicit_m_lens"

    if v2_mt == "M" and v2_cat == "Body" and any(x in mt_reason for x in [
        "M_body", "M_body_shorthand",
    ]):
        return "v2_likely_correct:explicit_m_body"

    if v2_mt in ("R", "S", "SL", "Q") and any(x in mt_reason for x in [
        f"{v2_mt}_", "TL_lens_shorthand", "SL_lens_shorthand", "Q_body_shorthand",
    ]):
        return f"v2_likely_correct:explicit_{str(v2_mt).lower()}_signal"

    if v2_mt == "L" and v2_cat == "Lens" and any(x in mt_reason for x in [
        "L_chungmuro", "L_ltm_l39", "L_leica_l_prefix",
    ]):
        title_u = title.upper()
        if any(x in title_u for x in [
            "SUMMARON", "NICKEL", "ELMAR", "SUMMICRON",
            "HEKTOR", "SUMMARIT", "LTM", "L39",
        ]):
            return "v2_likely_correct:legacy_l_screw_shorthand"

    if v2_mt == "C/Y" and "CY_mount_explicit" in mt_reason:
        return "v2_likely_correct:explicit_cy_mount"

    return None


def compare_v1_v2(
    items: list[dict],
    v1_label_key: str = "label",
    v1_mount_key: str = "mount",
    v1_brand_key: str = "brand",
    v1_category_key: str = "category",
) -> dict:
    """
    v1 results.json과 v2 결과를 비교하는 QA 함수.

    ══════════════════════════════════════════════════
    지표 설계 원칙

    핵심 지표 (판단 기준):
      mount_match_pct_nonac    Lens/Body만 대상 mount 일치율
                               → Accessory legacy 오염을 분모에서 제거
      category_match_pct       전체 category 일치율
      brand_match_pct          전체 brand 일치율

    참고 지표 (절대값 무의미):
      mount_match_pct_all      전체 mount 일치율 (Accessory 포함 — 왜곡됨)
      label_match_pct          v1/v2 label 체계 달라 무의미

    Accessory 전용 지표:
      accessory_count          v2 기준 Accessory 건수
      accessory_legacy_mount   v1 mount="Accessory"였던 건수 (오염원)
      accessory_with_mount_hint  compatible_mount 힌트 있는 건수
      accessory_with_system_hint compatible_system 힌트 있는 건수

    System 지표 (Q/Compact/PNS = 물리 mount 아님):
      system_items             해당 건수
      system_consistency_pct   v1/v2 일치율

    canonical 보정 추적:
      canonical_corrections    model_raw ≠ model_canonical 건수

    mismatch_type:
      ACC_LEGACY  v1 mount=Accessory, v2 cat=Accessory → 실제 오류 아님
      MT_ONLY     mount만 불일치
      CAT_ONLY    category만 불일치
      MT+CAT      둘 다 불일치
    ══════════════════════════════════════════════════
    """
    total = len(items)
    if total == 0:
        return {"total": 0, "error": "empty input"}

    # ── 카운터 ──
    mt_all_match = mt_all_mis = 0
    mt_nonac_total = mt_nonac_match = mt_nonac_mis = 0
    cat_match = cat_mis = 0
    br_match = br_mis = 0
    lbl_match = lbl_mis = 0
    v2_unk_mt = v2_unk_cat = 0
    v1_unk_lbl = 0
    acc_count = acc_legacy_mount = acc_with_mount_hint = acc_with_system_hint = 0
    SYSTEM_MOUNTS = {"Q", "Compact", "PNS"}
    sys_count = sys_mt_consistent = 0
    canonical_corrections = 0
    v2_likely_correct_count = 0
    v2_likely_correct_cat_mis = 0
    v2_likely_correct_mt_mis = 0
    mismatches = []

    for item in items:
        v2 = classify_listing_v2(item)

        v1_mt  = (item.get(v1_mount_key)    or "").strip()
        v1_cat = (item.get(v1_category_key) or "").strip()
        v1_br  = (item.get(v1_brand_key)    or "").strip()
        v1_lbl = (item.get(v1_label_key)    or "").strip()

        v2_mt  = v2["mount"]
        v2_cat = v2["category"]
        v2_br  = v2["brand"]
        v2_lbl = v2["label"]

        # Unknown
        if v2_mt  == "Unknown": v2_unk_mt  += 1
        if v2_cat == "Unknown": v2_unk_cat += 1
        if not v1_lbl or v1_lbl in ("Unknown", ""): v1_unk_lbl += 1

        # canonical 보정
        raw   = v2.get("model_raw")        or ""
        canon = v2.get("model_canonical")  or ""
        corrected = bool(raw and canon and raw != canon)
        if corrected: canonical_corrections += 1

        # 일치 여부
        mt_ok  = (v1_mt  == v2_mt)
        cat_ok = (v1_cat == v2_cat)
        br_ok  = (v1_br  == v2_br)
        lbl_ok = (v1_lbl == v2_lbl)

        if mt_ok:  mt_all_match += 1
        else:      mt_all_mis   += 1
        if cat_ok: cat_match += 1
        else:      cat_mis   += 1
        if br_ok:  br_match  += 1
        else:      br_mis    += 1
        if lbl_ok: lbl_match += 1
        else:      lbl_mis   += 1

        # ── Accessory 전용 ──
        is_acc_v2 = (v2_cat == "Accessory")
        if is_acc_v2:
            acc_count += 1
            if v1_mt == "Accessory":
                acc_legacy_mount += 1
            if v2_mt not in ("Unknown", "Accessory"):
                acc_with_mount_hint += 1
            name_l = (item.get("상품명") or "").lower()
            if any(x in name_l for x in ["q2","q3"," q ","sl","d-lux","tl","cl"]):
                acc_with_system_hint += 1

        # ── mount non-accessory 핵심 지표 ──
        # 분모: v2 category = Lens 또는 Body
        if v2_cat in ("Lens", "Body"):
            mt_nonac_total += 1
            if mt_ok: mt_nonac_match += 1
            else:     mt_nonac_mis   += 1

        # ── System 지표 ──
        if v2_mt in SYSTEM_MOUNTS or v1_mt in SYSTEM_MOUNTS:
            sys_count += 1
            if v2_mt == v1_mt: sys_mt_consistent += 1

        # ── mismatch 기록 ──
        if not (mt_ok and cat_ok):
            if v1_mt == "Accessory" and v2_cat == "Accessory":
                mtype = "ACC_LEGACY"
            elif not mt_ok and not cat_ok:
                mtype = "MT+CAT"
            elif not mt_ok:
                mtype = "MT_ONLY"
            else:
                mtype = "CAT_ONLY"

            qa_note = _qa_v2_likely_correct_note(
                item.get("상품명", ""), v1_mt, v1_cat, v2
            )
            if qa_note:
                v2_likely_correct_count += 1
                if not cat_ok:
                    v2_likely_correct_cat_mis += 1
                if not mt_ok:
                    v2_likely_correct_mt_mis += 1

            mismatches.append({
                "mismatch_type":      mtype,
                "qa_note":            qa_note,
                "title":              item.get("상품명", ""),
                "v1_mount":           v1_mt,   "v2_mount":    v2_mt,
                "v1_category":        v1_cat,  "v2_category": v2_cat,
                "v1_brand":           v1_br,   "v2_brand":    v2_br,
                "v1_label":           v1_lbl,  "v2_label":    v2_lbl,
                "v2_mount_reason":    v2["mount_reason"],
                "v2_category_reason": v2["category_reason"],
                "v2_label_reason":    v2["label_reason"],
                "model_raw":          v2.get("model_raw"),
                "model_canonical":    v2.get("model_canonical"),
                "canonical_corrected": corrected,
            })

    def pct(n, d=total): return round(n / d * 100, 1) if d else 0.0

    from collections import Counter
    mtype_counts = dict(Counter(m["mismatch_type"] for m in mismatches))

    return {
        # ── 핵심 지표 ──────────────────────────────
        "total":                    total,
        "mount_nonac_total":        mt_nonac_total,
        "mount_nonac_match":        mt_nonac_match,
        "mount_nonac_mismatch":     mt_nonac_mis,
        "mount_match_pct_nonac":    pct(mt_nonac_match, mt_nonac_total),
        "category_match":           cat_match,
        "category_mismatch":        cat_mis,
        "category_match_pct":       pct(cat_match),
        "category_match_adjusted":  cat_match + v2_likely_correct_cat_mis,
        "category_mismatch_adjusted": max(cat_mis - v2_likely_correct_cat_mis, 0),
        "category_match_pct_adjusted": pct(cat_match + v2_likely_correct_cat_mis),
        "brand_match":              br_match,
        "brand_mismatch":           br_mis,
        "brand_match_pct":          pct(br_match),
        # ── 참고 지표 ──────────────────────────────
        "mount_match_pct_all":      pct(mt_all_match),
        "label_match_pct":          pct(lbl_match),
        # ── Unknown 현황 ───────────────────────────
        "v2_unknown_mount":         v2_unk_mt,
        "v2_unknown_mount_pct":     pct(v2_unk_mt),
        "v2_unknown_category":      v2_unk_cat,
        "v2_unknown_cat_pct":       pct(v2_unk_cat),
        "v1_unknown_label":         v1_unk_lbl,
        # ── Accessory 전용 ─────────────────────────
        "accessory_count":            acc_count,
        "accessory_pct":              pct(acc_count),
        "accessory_legacy_mount":     acc_legacy_mount,
        "accessory_with_mount_hint":  acc_with_mount_hint,
        "accessory_with_system_hint": acc_with_system_hint,
        # ── System 지표 ────────────────────────────
        "system_items":               sys_count,
        "system_mount_consistent":    sys_mt_consistent,
        "system_consistency_pct":     pct(sys_mt_consistent, sys_count) if sys_count else 0.0,
        # ── canonical 보정 추적 ────────────────────
        "canonical_corrections":      canonical_corrections,
        "canonical_correction_pct":   pct(canonical_corrections),
        # ── QA 보조 해석 ──────────────────────────────────
        "v2_likely_correct_mismatches": v2_likely_correct_count,
        "v2_likely_correct_cat_mismatches": v2_likely_correct_cat_mis,
        "v2_likely_correct_mount_mismatches": v2_likely_correct_mt_mis,
        # ── mismatch 분류 ──────────────────────────
        "mismatch_type_counts":       mtype_counts,
        "mismatches":                 mismatches[:200],
    }


# ─────────────────────────────────────────────
# 10. CLI (python classifier_v2.py로 단독 실행)
# ─────────────────────────────────────────────

if __name__ == "__main__":
    import json, sys

    # 단건 테스트
    SMOKE_TESTS = [
        {"상품명": "Leica Summicron-M 35mm f/2 ASPH", "가격": "3,500,000"},
        {"상품명": "Leica M6 TTL 0.72 Body", "가격": "5,000,000"},
        {"상품명": "[중고] Voigtlander Nokton 50mm f/1.1 VM", "가격": "800,000"},
        {"상품명": "Leica 후드 12585", "가격": "80,000"},
        {"상품명": "LEICA IIIF Body", "가격": "1,200,000"},
        {"상품명": "Summilux-R 50mm f/1.4 3CAM", "가격": "2,000,000"},
        {"상품명": "[위탁] Zeiss Biogon ZM 35mm f/2", "가격": "600,000"},
        {"상품명": "Leica Q2 Monochrom", "가격": "6,000,000"},
        {"상품명": "TTArtisan 50mm f/0.95 M mount", "가격": "350,000"},
        {"상품명": "Hasselblad 503CW Body", "가격": "3,200,000"},
    ]

    print("=" * 70)
    print("classifier_v2 smoke test")
    print("=" * 70)
    for item in SMOKE_TESTS:
        result = classify_listing_v2(item)
        print(
            f"  {result['title_raw'][:45]:<45} "
            f"brand={result['brand']:<12} "
            f"mount={result['mount']:<8} "
            f"cat={result['category']:<10} "
            f"label={result['label']}"
        )

    # results.json이 있으면 QA 비교 실행
    if len(sys.argv) > 1:
        path = sys.argv[1]
        print(f"\n{'='*70}")
        print(f"QA 비교: {path}")
        print("=" * 70)
        with open(path, encoding="utf-8") as f:
            existing = json.load(f)
        report = compare_v1_v2(existing)
        n = report["total"]
        na = report["mount_nonac_total"]

        print(f"\n  총 {n}건\n")
        print(f"  ── 핵심 지표 (판단 기준) ──────────────────────────────────")
        print(f"  mount   일치율 [Lens/Body만]: {report['mount_match_pct_nonac']:>5}%"
              f"  ({report['mount_nonac_match']}/{na}건)")
        print(f"  category 일치율 [전체]:       {report['category_match_pct']:>5}%"
              f"  ({report['category_match']}/{n}건)")
        print(f"  category 보정 일치율 [v2 likely 제외]: {report['category_match_pct_adjusted']:>5}%"
              f"  ({report['category_match_adjusted']}/{n}건)")
        print(f"  brand    일치율 [전체]:       {report['brand_match_pct']:>5}%"
              f"  ({report['brand_match']}/{n}건)")

        print(f"\n  ── 참고 지표 ──────────────────────────────────────────────")
        print(f"  mount   일치율 [전체, Acc 포함]: {report['mount_match_pct_all']:>5}%  ← Accessory 오염 포함")
        print(f"  label   일치율:                  {report['label_match_pct']:>5}%  ← v1/v2 체계 달라 무의미")

        print(f"\n  ── Accessory 전용 지표 ────────────────────────────────────")
        print(f"  Accessory 건수:            {report['accessory_count']:>5}건 ({report['accessory_pct']}%)")
        print(f"  v1 mount=Accessory 오염:   {report['accessory_legacy_mount']:>5}건  ← 비교 왜곡 원인")
        print(f"  compatible_mount 힌트 있음: {report['accessory_with_mount_hint']:>5}건")
        print(f"  compatible_system 힌트 있음: {report['accessory_with_system_hint']:>4}건")

        print(f"\n  ── System 지표 (Q/Compact/PNS = 물리 mount 아님) ─────────")
        print(f"  system 건수:      {report['system_items']:>5}건")
        print(f"  v1/v2 일치:       {report['system_mount_consistent']:>5}건 ({report['system_consistency_pct']}%)")

        print(f"\n  ── Unknown 현황 ───────────────────────────────────────────")
        print(f"  v2 mount=Unknown:    {report['v2_unknown_mount']:>5}건 ({report['v2_unknown_mount_pct']}%)")
        print(f"  v2 category=Unknown: {report['v2_unknown_category']:>5}건 ({report['v2_unknown_cat_pct']}%)")
        print(f"  v1 label 미분류:     {report['v1_unknown_label']:>5}건")

        print(f"\n  ── canonical 보정 추적 ────────────────────────────────────")
        print(f"  model_canonical 보정: {report['canonical_corrections']}건 ({report['canonical_correction_pct']}%)")

        mc = report.get("mismatch_type_counts", {})
        total_mis = sum(mc.values())
        print(f"\n  ── mismatch 분류 ({total_mis}건) ─────────────────────────────")
        for mtype in ("ACC_LEGACY", "MT_ONLY", "CAT_ONLY", "MT+CAT"):
            cnt = mc.get(mtype, 0)
            note = {
                "ACC_LEGACY": "← v1 legacy 오염, 실제 오류 아님",
                "MT_ONLY":    "← 실제 mount 오류 후보",
                "CAT_ONLY":   "← category 오류",
                "MT+CAT":     "← mount + category 동시 불일치",
            }[mtype]
            print(f"  {mtype:<12} {cnt:>5}건  {note}")
        print(f"  {'V2_LIKELY':<12} {report.get('v2_likely_correct_mismatches', 0):>5}건  "
              f"← v2가 더 맞을 가능성이 큰 보조 표시")

        print(f"\n  ── MT_ONLY / MT+CAT 불일치 상위 30건 ─────────────────────")
        real_errors = [m for m in report["mismatches"]
                       if m["mismatch_type"] in ("MT_ONLY", "MT+CAT")]
        for m in real_errors[:30]:
            qa_mark = " ✓v2" if m.get("qa_note") else ""
            print(f"  [{m['mismatch_type']:<6}{qa_mark:<4}] {m['title'][:40]:<40} "
                  f"mt:{m['v1_mount']!r:>10}→{m['v2_mount']!r:<10} "
                  f"cat:{m['v1_category']!r}→{m['v2_category']!r}")

        out_path = path.replace(".json", "_qa_v2.json")
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        print(f"\n  QA 리포트 저장 → {out_path}")
