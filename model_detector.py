"""
model_detector.py
=================
label 계층 아래의 model_raw / model_canonical / variant / focal_length 추출.

정책:
  model_raw       상품명에 적힌 표현 그대로
                  예: "Summicron", "Vario-Elmarit", "Q2 Monochrom"
  model_canonical mount/시스템 정보를 반영한 표준 모델명 (집계/시세/검색용)
                  예: "Summicron-R", "Vario-Elmarit-SL", "Q2"
  variant         모델의 세부 가치 차이 요소 (list)
                  예: ["Monochrom"], ["TTL"], ["8-element", "ASPH"]
  focal_length    렌즈 초점거리 숫자 (mm 단위, 단위 제외)
                  예: "35", "50", "24-90"

brand / mount / category / label 재판단 금지.
mount는 canonical suffix 보정에만 참고.
"""

from __future__ import annotations
import re
from typing import Optional


# ─────────────────────────────────────────────
# 렌즈 모델명 패턴 (구체적인 것 먼저)
# ─────────────────────────────────────────────

_LENS_MODEL_PATTERNS: list[tuple[str, str]] = [
    # APO 계열
    ("apo-summicron",           "APO-Summicron"),
    ("apo summicron",           "APO-Summicron"),
    ("apo-macro-elmarit",       "APO-Macro-Elmarit"),
    ("apo-telyt",               "APO-Telyt"),
    ("apo-elmarit",             "APO-Elmarit"),
    # Vario 계열 (elmarit/elmar보다 먼저)
    ("apo-vario-elmarit-sl",    "APO-Vario-Elmarit-SL"),
    ("vario-apo-elmarit-r",     "Vario-APO-Elmarit-R"),
    ("vario-elmarit-sl",        "Vario-Elmarit-SL"),
    ("vario elmarit-sl",        "Vario-Elmarit-SL"),
    ("vario-elmarit-r",         "Vario-Elmarit-R"),
    ("vario-elmarit",           "Vario-Elmarit"),
    ("vario-elmar-s",           "Vario-Elmar-S"),
    ("vario-elmar-r",           "Vario-Elmar-R"),
    ("vario-elmar",             "Vario-Elmar"),
    # Tri-Elmar (elmar보다 먼저)
    ("tri-elmar",               "Tri-Elmar"),
    # Super-Elmar (elmar보다 먼저)
    ("super-elmar-s",           "Super-Elmar-S"),
    ("super-elmar",             "Super-Elmar"),
    # Tele-Elmar (elmar보다 먼저)
    ("tele-elmar",              "Tele-Elmar"),
    # Summicron 계열
    ("summicron-m",             "Summicron-M"),
    ("summicron-r",             "Summicron-R"),
    ("summicron-c",             "Summicron-C"),
    ("summicron",               "Summicron"),
    # Summilux 계열
    ("summilux-m",              "Summilux-M"),
    ("summilux-r",              "Summilux-R"),
    ("summilux-sl",             "Summilux-SL"),
    ("summilux-tl",             "Summilux-TL"),
    ("summilux",                "Summilux"),
    # Noctilux
    ("noctilux",                "Noctilux"),
    # Elmarit 계열 (구체적인 것 먼저)
    ("macro-elmarit",           "APO-Macro-Elmarit"),
    ("elmarit-m",               "Elmarit-M"),
    ("elmarit-r",               "Elmarit-R"),
    ("elmarit-sl",              "Elmarit-SL"),
    ("elmarit-tl",              "Elmarit-TL"),
    ("elmarit",                 "Elmarit"),
    # Elmar 계열
    ("elmar-m",                 "Elmar-M"),
    ("elmar-r",                 "Elmar-R"),
    ("elmar",                   "Elmar"),
    # Summarit 계열
    ("summarit-m",              "Summarit-M"),
    ("summarit-s",              "Summarit-S"),
    ("summarit",                "Summarit"),
    # Summaron / Summitar
    ("summaron",                "Summaron"),
    ("summitar",                "Summitar"),
    # Super-Angulon
    ("super-angulon",           "Super-Angulon"),
    ("angulon",                 "Angulon"),
    # Hologon / Hektor
    ("hologon",                 "Hologon"),
    ("hektor",                  "Hektor"),
    # Telyt
    ("telyt-r",                 "Telyt-R"),
    ("telyt",                   "Telyt"),
    # Nokton / Lanthar (Voigtlander)
    ("nokton",                  "Nokton"),
    ("apo-lanthar",             "APO-Lanthar"),
    ("lanthar",                 "Lanthar"),
    # Zeiss
    ("c-biogon",                "C-Biogon"),
    ("biogon",                  "Biogon"),
    ("distagon",                "Distagon"),
    ("planar",                  "Planar"),
    ("sonnar",                  "Sonnar"),
    ("otus",                    "Otus"),
    ("loxia",                   "Loxia"),
]

# ─────────────────────────────────────────────
# 바디 모델명 패턴 (구체적인 것 먼저)
# ─────────────────────────────────────────────

_BODY_MODEL_PATTERNS: list[tuple[str, str]] = [
    # M 디지털
    ("m11-p",           "M11-P"),
    ("m11",             "M11"),
    ("m10-r",           "M10-R"),
    ("m10-p",           "M10-P"),
    ("m10-d",           "M10-D"),
    ("m10",             "M10"),
    ("m9-p",            "M9-P"),
    ("m9",              "M9"),
    ("m8.2",            "M8.2"),
    ("m8",              "M8"),
    ("m262",            "M262"),
    ("m240",            "M240"),
    ("m-e",             "M-E"),
    ("m-d",             "M-D"),
    ("m-p",             "M-P"),
    ("m-a",             "M-A"),
    ("ma",              "M-A"),
    # M 필름 (구체적인 variant 포함형 먼저)
    ("m11 monochrom",   "M11 Monochrom"),
    ("m10 monochrom",   "M10 Monochrom"),
    ("m monochrom",     "M Monochrom"),
    ("m6 ttl 0.58",     "M6 TTL"),
    ("m6 ttl 0.72",     "M6 TTL"),
    ("m6 ttl 0.85",     "M6 TTL"),
    ("m6 ttl",          "M6 TTL"),
    ("m6 복각",         "M6 복각"),
    ("m6j",             "M6J"),
    ("m6",              "M6"),
    ("mp3",             "MP3"),
    ("mp",              "MP"),
    ("m7",              "M7"),
    ("m5",              "M5"),
    ("m4-p",            "M4-P"),
    ("m4-2",            "M4-2"),
    ("m4",              "M4"),
    ("m3 ds",           "M3 DS"),
    ("m3 ss",           "M3 SS"),
    ("m3",              "M3"),
    ("m2-r",            "M2-R"),
    ("m2",              "M2"),
    ("m1",              "M1"),
    ("mda",             "MDa"),
    # R 바디
    ("r9",              "R9"),
    ("r8",              "R8"),
    ("r7",              "R7"),
    ("r6.2",            "R6.2"),
    ("r6",              "R6"),
    ("r5",              "R5"),
    ("r4",              "R4"),
    ("r3",              "R3"),
    ("r-e",             "R-E"),
    ("leicaflex sl2",   "Leicaflex SL2"),
    ("leicaflex sl",    "Leicaflex SL"),
    ("leicaflex",       "Leicaflex"),
    # Barnack
    ("iiig",            "IIIg"),
    ("iiif",            "IIIf"),
    ("iiic",            "IIIc"),
    ("iiib",            "IIIb"),
    ("iiia",            "IIIa"),
    ("iif",             "IIf"),
    ("if",              "If"),
    ("standard",        "Standard"),
    # Q 시스템 (구체적인 것 먼저)
    ("q2 monochrom",    "Q2 Monochrom"),
    ("q3",              "Q3"),
    ("q2",              "Q2"),
    ("q-p",             "Q-P"),
    ("q",               "Q"),
    # SL
    ("sl3",             "SL3"),
    ("sl2-s",           "SL2-S"),
    ("sl2",             "SL2"),
    ("sl",              "SL"),
    # S
    ("s3",              "S3"),
    ("s2",              "S2"),
    ("s-e",             "S-E"),
    # Monochrom (Q2/M 특정 패턴 처리 후)
    ("monochrom",       "Monochrom"),
    # Compact
    ("d-lux 8",         "D-LUX 8"),
    ("d-lux 7",         "D-LUX 7"),
    ("d-lux 6",         "D-LUX 6"),
    ("d-lux 5",         "D-LUX 5"),
    ("d-lux 4",         "D-LUX 4"),
    ("d-lux 3",         "D-LUX 3"),
    ("d-lux typ 109",   "D-LUX Typ 109"),
    ("d-lux",           "D-LUX"),
    ("v-lux 5",         "V-LUX 5"),
    ("v-lux 4",         "V-LUX 4"),
    ("v-lux typ 114",   "V-LUX Typ 114"),
    ("v-lux",           "V-LUX"),
    ("x2",              "X2"),
    ("x1",              "X1"),
    ("x vario",         "X Vario"),
    ("x typ 113",       "X Typ 113"),
    ("t typ 701",       "T Typ 701"),
    ("tl2",             "TL2"),
    ("tl",              "TL"),
    ("cl",              "CL"),
    ("c-lux",           "C-LUX"),
    ("c1",              "C1"),
    ("minilux zoom",    "Minilux Zoom"),
    ("minilux",         "Minilux"),
    ("cm zoom",         "CM Zoom"),
    ("sofort 2",        "Sofort 2"),
    ("sofort",          "Sofort"),
    ("digilux 3",       "Digilux 3"),
    ("digilux 2",       "Digilux 2"),
    ("digilux 1",       "Digilux 1"),
    ("digilux",         "Digilux"),
]

# ─────────────────────────────────────────────
# Variant 패턴
# ─────────────────────────────────────────────

_VARIANT_PATTERNS: list[tuple[str, str]] = [
    # 렌즈 특수 에디션/세대
    ("8-element",       "8-element"),
    ("8 element",       "8-element"),
    ("8매",             "8-element"),
    ("steel rim",       "Steel Rim"),
    ("스틸림",           "Steel Rim"),
    ("rigid",           "Rigid"),
    ("리짓",             "Rigid"),
    ("dual range",      "Dual Range"),
    ("fle",             "FLE"),
    ("asph",            "ASPH"),
    ("pre-asph",        "Pre-ASPH"),
    ("pre asph",        "Pre-ASPH"),
    ("6-element",       "6-element"),
    ("6 element",       "6-element"),
    ("6매",             "6-element"),
    # 조리개 (Noctilux 등 조리개가 variant가 되는 경우)
    ("f0.95",           "f0.95"),
    ("f1.0",            "f1.0"),
    ("f1.2",            "f1.2"),
    ("f1.25",           "f1.25"),
    # 바디 finish
    ("black paint",     "Black Paint"),
    ("black chrome",    "Black Chrome"),
    ("anthracite",      "Anthracite"),
    ("olive",           "Olive"),
    ("titanium",        "Titanium"),
    ("chrome",          "Chrome"),
    ("silver",          "Silver"),
    ("black",           "Black"),
    # 바디 special
    ("a la carte",      "A La Carte"),
    ("hermes",          "Hermès"),
    ("panda",           "Panda"),
    ("big logo",        "Big Logo"),
    ("0.58",            "0.58"),
    ("0.72",            "0.72"),
    ("0.85",            "0.85"),
    # 세대
    ("v1", "v1"), ("v2", "v2"), ("v3", "v3"), ("v4", "v4"), ("v5", "v5"),
    ("1세대", "v1"), ("2세대", "v2"), ("3세대", "v3"), ("4세대", "v4"),
    ("1st", "v1"), ("2nd", "v2"), ("3rd", "v3"), ("4th", "v4"),
    # 기타
    ("wate",            "WATE"),
    ("mate",            "MATE"),
    # ROM은 단어 경계 필요 (monochrom 안의 rom 방지) → 별도 처리
    ("3cam",            "3CAM"),
    ("2cam",            "2CAM"),
    ("1cam",            "1CAM"),
    ("6bit",            "6bit"),
    ("ttl",             "TTL"),
    ("monochrom",       "Monochrom"),
    ("복각",             "복각"),
    ("zoom",            "Zoom"),
    ("ds",              "DS"),
    ("ss",              "SS"),
]

# 단어 경계가 필요한 variant (부분 문자열 매칭 금지)
_VARIANT_WORD_BOUNDARY: set[str] = {"rom", "ds", "ss", "ttl", "zoom"}

# ─────────────────────────────────────────────
# 초점거리 추출
# ─────────────────────────────────────────────

def extract_focal_length(text: str) -> Optional[str]:
    n = text.lower()
    # 줌: "24-90mm", "16-18-21mm"
    zoom = re.search(r'(\d{1,3}(?:-\d{1,3})+)\s*mm', n)
    if zoom:
        return zoom.group(1)
    # cm 표기 구형: "3.5cm" → "35"mm
    cm = re.search(r'(\d+(?:\.\d+)?)\s*cm\b', n)
    if cm:
        return str(int(float(cm.group(1)) * 10))
    # 단초점: "50mm"
    single = re.search(r'(?<!\d)(\d{2,3})\s*mm', n)
    if single:
        return single.group(1)
    # "f2/35", "1:2/35" 구형
    alt = re.search(r'(?:f\d+(?:\.\d+)?|1:\d+(?:\.\d+)?)\s*/\s*(\d{2,3})', n)
    if alt:
        return alt.group(1)
    return None


# ─────────────────────────────────────────────
# canonical suffix 보정 맵
# ─────────────────────────────────────────────

_MOUNT_SUFFIX_MAP: dict[str, dict[str, str]] = {
    "SL": {
        "Vario-Elmarit":     "Vario-Elmarit-SL",
        "APO-Vario-Elmarit": "APO-Vario-Elmarit-SL",
        "Elmarit":           "Elmarit-SL",
        "Summicron":         "Summicron-SL",
        "Summilux":          "Summilux-SL",
        "Elmar":             "Elmar-SL",
        "Summarit":          "Summarit-SL",
    },
    "R": {
        "Vario-Elmarit":     "Vario-Elmarit-R",
        "Vario-APO-Elmarit": "Vario-APO-Elmarit-R",
        "Elmarit":           "Elmarit-R",
        "APO-Elmarit":       "APO-Macro-Elmarit-R",
        "Summicron":         "Summicron-R",
        "Summilux":          "Summilux-R",
        "Telyt":             "Telyt-R",
        "APO-Telyt":         "APO-Telyt-R",
        "Elmar":             "Elmar-R",
        "Super-Elmar":       "Super-Elmar-R",
    },
    "M": {
        "Elmarit":   "Elmarit-M",
        "Summarit":  "Summarit-M",
        "Summicron": "Summicron-M",
        "Summilux":  "Summilux-M",
    },
    "L": {},   # 나사마운트는 suffix 없이 그대로
}

# 바디 모델에서 variant를 분리하는 맵
# key=model_raw, value=(model_canonical_base, variant_str)
_BODY_VARIANT_SPLIT: dict[str, tuple[str, str]] = {
    "Q2 Monochrom":    ("Q2",       "Monochrom"),
    "M11 Monochrom":   ("M11",      "Monochrom"),
    "M10 Monochrom":   ("M10",      "Monochrom"),
    "M Monochrom":     ("M",        "Monochrom"),
    "M6 TTL":          ("M6",       "TTL"),
    "M3 DS":           ("M3",       "DS"),
    "M3 SS":           ("M3",       "SS"),
    "M6 복각":         ("M6",       "복각"),
    "Minilux Zoom":    ("Minilux",  "Zoom"),
    "CM Zoom":         ("CM",       "Zoom"),
    "Sofort 2":        ("Sofort",   "2"),
    "Leicaflex SL2":   ("Leicaflex","SL2"),
    "Leicaflex SL":    ("Leicaflex","SL"),
}


# ─────────────────────────────────────────────
# 메인 함수
# ─────────────────────────────────────────────

def detect_model(
    normalized_name: str,
    normalized_description: Optional[str] = None,
    category: Optional[str] = None,
    mount: Optional[str] = None,
) -> dict:
    """
    Returns:
        model_raw:       str | None  상품명 그대로 추출
        model_canonical: str | None  집계/시세용 표준 모델명
        variant:         list[str]   세부 가치 차이 요소
        focal_length:    str | None  초점거리 (mm 숫자)
    """
    n = normalized_name.lower()
    combined = n + " " + (normalized_description or "").lower()
    cat = (category or "").lower()

    model_raw: Optional[str] = None
    variants: list[str] = []
    focal_length: Optional[str] = None

    # ── 초점거리 ──
    if cat in ("lens", ""):
        focal_length = extract_focal_length(combined)

    # ── model_raw: 상품명 패턴 매칭 ──
    if cat == "body":
        for kw, canon in _BODY_MODEL_PATTERNS:
            if kw in n:
                model_raw = canon
                break
    elif cat == "lens":
        for kw, canon in _LENS_MODEL_PATTERNS:
            if kw in n:
                model_raw = canon
                break
    else:
        for kw, canon in _LENS_MODEL_PATTERNS:
            if kw in n:
                model_raw = canon
                break
        if not model_raw:
            for kw, canon in _BODY_MODEL_PATTERNS:
                if kw in n:
                    model_raw = canon
                    break

    # ── model_canonical + variant 분리 ──
    if model_raw and model_raw in _BODY_VARIANT_SPLIT:
        # 바디: "Q2 Monochrom" → canonical="Q2", variant=["Monochrom"]
        base, var = _BODY_VARIANT_SPLIT[model_raw]
        model_canonical = base
        variants.append(var)
    elif model_raw and cat == "lens" and mount and mount in _MOUNT_SUFFIX_MAP:
        # 렌즈: suffix 보정 (상품명에 없는 -R/-SL/-M 추가)
        model_canonical = _MOUNT_SUFFIX_MAP[mount].get(model_raw, model_raw)
    else:
        model_canonical = model_raw  # 보정 없으면 raw = canonical

    # ── Variant 추출 ──
    already = {v.lower() for v in variants}
    exclude = {
        (model_raw or "").lower(),
        (model_canonical or "").lower(),
    }
    for kw, canon in _VARIANT_PATTERNS:
        if canon.lower() in already or canon.lower() in exclude:
            continue
        # 단어 경계가 필요한 키워드는 정규식으로 검사
        if kw in _VARIANT_WORD_BOUNDARY:
            if not re.search(rf'\b{re.escape(kw)}\b', n):
                continue
        elif kw not in n:
            continue
        variants.append(canon)
        already.add(canon.lower())

    return {
        "model_raw":       model_raw,
        "model_canonical": model_canonical,
        "variant":         variants,
        "focal_length":    focal_length,
    }
