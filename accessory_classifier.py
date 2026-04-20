"""
accessory_classifier.py
=======================
Accessory 전용 분류 모듈.

역할:
  - accessory_type 분류
  - compatible_mounts 추출 (물리적 마운트 호환 정보)
  - compatible_systems 추출 (제품 라인 호환 정보)

설계 원칙:
  - classify_listing_v2가 category=Accessory로 판단한 후에만 호출
  - detect_mount/detect_brand 결과를 재판단하지 않음
  - mount/system 구분을 명확히 함

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
system 분리 원칙 (다음 단계 마이그레이션 준비)

현재 classify_listing_v2 출력의 mount 필드:
  물리적 마운트: M / R / L / SL / S / V / Unknown
  제품 라인:    Q / Compact / PNS          ← 여기가 문제

목표 스키마:
  mount:  M | R | L | SL | S | V | Unknown   (물리적 마운트만)
  system: Q | Compact | PNS | CL | TL | None  (제품 라인)

마이그레이션 순서:
  1. [현재] accessory_classifier.py에서 compatible_systems 추출 → 검증
  2. [다음] classify_listing_v2 반환값에 system 필드 추가 (mount와 병행)
  3. [이후] mount에서 Q/Compact/PNS 제거, system으로 완전 이관
  4. [최종] QA 비교에서 system_match_pct를 별도 핵심 지표로 분리
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

from __future__ import annotations
import re
from typing import Optional


# ─────────────────────────────────────────────
# Accessory 타입 분류
# ─────────────────────────────────────────────

# (키워드, accessory_type) — 구체적인 것 먼저
_ACCESSORY_TYPE_PATTERNS: list[tuple[str, str]] = [
    # 어댑터
    ("adapter", "adapter"),
    ("adaptor", "adapter"),
    ("어댑터",   "adapter"),
    ("mount adapter", "adapter"),
    ("m-l",      "adapter"),    # M to L 어댑터
    ("m to l",   "adapter"),
    ("ltm adapter", "adapter"),
    ("lm adapter",  "adapter"),
    # 파인더 / 뷰파인더
    ("finder",      "finder"),
    ("viewfinder",  "finder"),
    ("view finder", "finder"),
    ("파인더",       "finder"),
    ("viooh",       "finder"),
    ("sbooi",       "finder"),
    # 후드
    ("hood",   "hood"),
    ("후드",    "hood"),
    ("gegenlichtblende", "hood"),
    # 필터
    ("filter", "filter"),
    ("필터",    "filter"),
    ("uva",    "filter"),
    ("uv/ir",  "filter"),
    # 캡
    ("cap",      "cap"),
    ("캡",       "cap"),
    ("lens cap", "cap"),
    ("body cap", "cap"),
    ("리어캡",    "cap"),
    ("프론트캡",  "cap"),
    # 케이스 / 가방 / 파우치
    ("case",      "case"),
    ("케이스",     "case"),
    ("bag",       "bag"),
    ("가방",       "bag"),
    ("pouch",     "pouch"),
    ("파우치",     "pouch"),
    ("holster",   "bag"),
    ("shoulder bag", "bag"),
    ("camera bag",   "bag"),
    # 스트랩
    ("strap",       "strap"),
    ("스트랩",       "strap"),
    ("neck strap",  "strap"),
    ("wrist strap", "strap"),
    # 그립 / 핸드그립
    ("handgrip",     "grip"),
    ("hand grip",    "grip"),
    ("multifunctional handgrip", "grip"),
    ("grip",         "grip"),
    ("그립",          "grip"),
    ("thumb support","grip"),
    ("thumb grip",   "grip"),
    # 프로텍터 / 커버
    ("protector",  "protector"),
    ("프로텍터",    "protector"),
    ("cover",      "protector"),
    ("커버",        "protector"),
    # 플래시
    ("flash",  "flash"),
    ("플래시",  "flash"),
    ("sf20",   "flash"), ("sf24",  "flash"), ("sf26",  "flash"),
    ("sf40",   "flash"), ("sf58",  "flash"), ("sf60",  "flash"),
    ("sf64",   "flash"),
    # 배터리 / 충전기
    ("battery",  "battery"),
    ("배터리",    "battery"),
    ("charger",  "charger"),
    ("충전기",    "charger"),
    # 기타 악세사리
    ("leicavit",   "winder"),
    ("rapidwinder","winder"),
    ("motor winder","winder"),
    ("visoflex",   "visoflex"),
    ("evf",        "evf"),
    ("diopter",    "diopter"),
    ("correction lens", "diopter"),
    ("tripod",     "tripod"),
    ("ball head",  "tripod"),
    ("cable",      "cable"),
    ("케이블",     "cable"),
    ("elpro",      "closeup"),
    ("macro",      "closeup"),
]

_FILTER_TYPE_REGEX: list[tuple[str, str]] = [
    (r'\bb\+w\b.*\be\d{2,3}\b', "bw_thread_filter"),
    (r'\b(?:leica\s+)?a36\s+(?:orange|yellow|green|red)\b', "a36_color_filter"),
]

# ─────────────────────────────────────────────
# compatible_mounts 추출
# 물리적 마운트 호환 정보 (M, R, L, SL 등)
# ─────────────────────────────────────────────

_MOUNT_COMPAT_PATTERNS: list[tuple[str, list[str]]] = [
    # 어댑터: "M-L", "M to L" → M, SL 둘 다 호환
    (r'\bM[-\s]L\b|\bM\s+TO\s+L\b',            ["M", "SL"]),
    (r'\bL[-\s]M\b|\bL\s+TO\s+M\b',            ["SL", "M"]),
    (r'\bLTM[-\s]M\b|\bL39[-\s]M\b',           ["L", "M"]),
    (r'\bLTM\s+TO\s+M\b|\bL39\s+TO\s+M\b',     ["L", "M"]),
    (r'\bLTM\b|\bL39\b|\bM39\b',               ["L"]),   # LTM 단독도 L 호환
    (r'\bM39[-\s]M\b',                          ["L", "M"]),
    (r'\bR[-\s]M\b|\bR\s+TO\s+M\b',            ["R", "M"]),
    (r'\bM[-\s]SL\b',                           ["M", "SL"]),
    # "for M", "M mount" → M 호환
    (r'\bFOR\s+(LEICA\s+)?M\b',                 ["M"]),
    (r'\bM[\s-]MOUNT\b',                        ["M"]),
    (r'\bM\s+마운트\b|M마운트',                  ["M"]),
    # "for R", "R mount" → R 호환
    (r'\bFOR\s+(LEICA\s+)?R\b',                 ["R"]),
    (r'\bR[\s-]MOUNT\b',                        ["R"]),
    # SL/L-mount 명시
    (r'\bL[\s-]MOUNT\b',                        ["SL"]),
    (r'\bFOR\s+SL\b',                           ["SL"]),
    # M 바디 번호 → M 호환
    (r'\bM[3-9]\b|\bM1[01]\b|\bMP\b',           ["M"]),
    # R 바디 번호 → R 호환
    (r'\bR[3-9]\b',                             ["R"]),
    # Visoflex → M 호환
    (r'\bVISOFLEX\b',                           ["M"]),
    # 어댑터 without 명시 — "Leica M" + "adapter" → M 호환
    (r'\bLEICA\s+M\b',                          ["M"]),
]

# ─────────────────────────────────────────────
# compatible_systems 추출
# 제품 라인 호환 정보 (Q, Q2, Q3, Compact, CL, TL, SL...)
# ─────────────────────────────────────────────

_SYSTEM_COMPAT_PATTERNS: list[tuple[str, list[str]]] = [
    # Q 시리즈
    (r'\bQ3\b',              ["Q3", "Q"]),
    (r'\bQ2\s+MONOCHROM\b',  ["Q2 Monochrom", "Q2", "Q"]),
    (r'\bQ2\b',              ["Q2", "Q"]),
    (r'\bQ-P\b',             ["Q-P", "Q"]),
    (r'\bQ\b',               ["Q"]),
    # SL 시리즈
    (r'\bSL3\b',             ["SL3", "SL"]),
    (r'\bSL2-S\b',           ["SL2-S", "SL2", "SL"]),
    (r'\bSL2\b',             ["SL2", "SL"]),
    (r'\bSL\b',              ["SL"]),
    # TL/CL 시리즈
    (r'\bTL2\b',             ["TL2", "TL"]),
    (r'\bTL\b',              ["TL"]),
    (r'\bCL\b',              ["CL"]),
    # Visoflex
    (r'\bVISOFLEX\b',                           ["M"]),
    # M 시리즈
    (r'\bM11\b',             ["M11", "M"]),
    (r'\bM10\b',             ["M10", "M"]),
    (r'\bM9\b',              ["M9", "M"]),
    (r'\bM8\b',              ["M8", "M"]),
    (r'\bM6\b',              ["M6", "M"]),
    (r'\bM\b',               ["M"]),
    # R 시리즈
    (r'\bR9\b',              ["R9", "R"]),
    (r'\bR8\b',              ["R8", "R"]),
    (r'\bR\b',               ["R"]),
    # D-LUX / V-LUX / X 시리즈
    (r'\bD-LUX\s*\d*\b',    ["D-LUX"]),
    (r'\bV-LUX\s*\d*\b',    ["V-LUX"]),
    (r'\bX\s+VARIO\b',      ["X Vario"]),
    (r'\bX[12]?\b',          ["X"]),
    # Sofort
    (r'\bSOFORT\s*2?\b',    ["Sofort"]),
]


# ─────────────────────────────────────────────
# system 분류 (단독 호출용 — 마이그레이션 준비)
# ─────────────────────────────────────────────

# 현재 mount 필드에 섞여 있는 Q/Compact/PNS를
# 별도 system 필드로 분리하기 위한 매핑
_MOUNT_TO_SYSTEM: dict[str, str] = {
    "Q":       "Q",
    "Compact": "Compact",
    "PNS":     "PNS",
}

_SYSTEM_KW: list[tuple[str, str]] = [
    # Q
    ("q3",          "Q"),
    ("q2",          "Q"),
    ("q-p",         "Q"),
    (" q ",         "Q"),
    # Compact
    ("d-lux",       "Compact"),
    ("v-lux",       "Compact"),
    ("digilux",     "Compact"),
    ("c-lux",       "Compact"),
    ("x vario",     "Compact"),
    ("x1",          "Compact"),
    ("x2",          "Compact"),
    ("leica x ",    "Compact"),
    ("sofort",      "Compact"),
    ("leica t ",    "Compact"),
    ("tl2",         "Compact"),
    (" tl ",        "Compact"),
    ("leica cl",    "Compact"),
    # PNS
    ("minilux",     "PNS"),
    ("cm zoom",     "PNS"),
    ("leica c ",    "PNS"),
    ("leica mini",  "PNS"),
    ("af-c1",       "PNS"),
]


def detect_system(normalized_name: str, mount: Optional[str] = None) -> Optional[str]:
    """
    제품 라인(system)을 감지한다.
    현재 mount 필드의 Q/Compact/PNS를 대체할 목적.

    Returns: "Q" | "Compact" | "PNS" | None
    """
    # mount가 이미 system 값이면 그대로 반환
    if mount in _MOUNT_TO_SYSTEM:
        return _MOUNT_TO_SYSTEM[mount]

    n = normalized_name.lower()
    for kw, system in _SYSTEM_KW:
        if kw in n:
            return system
    return None


# ─────────────────────────────────────────────
# 메인 함수
# ─────────────────────────────────────────────

def classify_accessory(
    normalized_name: str,
    normalized_description: Optional[str] = None,
    mount: Optional[str] = None,
) -> dict:
    """
    category=Accessory로 판단된 아이템의 세부 분류.

    입력:
      normalized_name        classify_listing_v2가 정규화한 상품명
      normalized_description 정규화된 설명 (optional)
      mount                  classify_listing_v2가 판단한 mount (optional)

    출력:
      accessory_type:        str | None   예: "adapter", "hood", "bag"
      compatible_mounts:     list[str]    예: ["M", "SL"]
      compatible_systems:    list[str]    예: ["Q2", "Q"]
      acc_confidence:        float
      acc_reason:            list[str]
    """
    n = normalized_name.lower()
    desc = (normalized_description or "").lower()
    combined = n + " " + desc
    combined_upper = combined.upper()
    reasons: list[str] = []

    # ── accessory_type ──
    acc_type: Optional[str] = None
    for kw, atype in _ACCESSORY_TYPE_PATTERNS:
        if kw in combined:
            acc_type = atype
            reasons.append(f"type:{atype}:{kw}")
            break
    if acc_type is None:
        for pattern, label in _FILTER_TYPE_REGEX:
            if re.search(pattern, combined):
                acc_type = "filter"
                reasons.append(f"type:filter_rx:{label}")
                break

    # ── compatible_mounts ──
    compat_mounts: list[str] = []
    seen_mounts: set[str] = set()

    # mount 파라미터로 넘어온 값이 물리적 마운트면 우선 추가
    PHYSICAL_MOUNTS = {"M", "R", "L", "SL", "S", "V"}
    if mount in PHYSICAL_MOUNTS and mount not in seen_mounts:
        compat_mounts.append(mount)
        seen_mounts.add(mount)
        reasons.append(f"compat_mount_from_detect:{mount}")

    for pattern, mounts in _MOUNT_COMPAT_PATTERNS:
        if re.search(pattern, combined_upper):
            for m in mounts:
                if m not in seen_mounts:
                    compat_mounts.append(m)
                    seen_mounts.add(m)
            reasons.append(f"compat_mount_pattern:{pattern[:20]}")

    # ── compatible_systems ──
    compat_systems: list[str] = []
    seen_systems: set[str] = set()

    # mount가 Q/Compact/PNS면 system 힌트로 추가
    if mount in _MOUNT_TO_SYSTEM:
        sys_val = _MOUNT_TO_SYSTEM[mount]
        compat_systems.append(sys_val)
        seen_systems.add(sys_val)
        reasons.append(f"compat_system_from_mount:{sys_val}")

    for pattern, systems in _SYSTEM_COMPAT_PATTERNS:
        if re.search(pattern, combined_upper):
            for s in systems:
                if s not in seen_systems:
                    compat_systems.append(s)
                    seen_systems.add(s)
            reasons.append(f"compat_system_pattern:{pattern[:20]}")

    # confidence: 타입 + 호환 정보가 있을수록 높음
    conf = 0.60
    if acc_type:          conf += 0.20
    if compat_mounts:     conf += 0.10
    if compat_systems:    conf += 0.10
    conf = min(conf, 0.97)

    return {
        "accessory_type":     acc_type,
        "compatible_mounts":  compat_mounts,
        "compatible_systems": compat_systems,
        "acc_confidence":     round(conf, 2),
        "acc_reason":         reasons,
    }


# ─────────────────────────────────────────────
# system 분리 마이그레이션 계획 문서
# ─────────────────────────────────────────────

SYSTEM_MIGRATION_PLAN = """
System 분리 마이그레이션 계획
==============================

## 현재 상태 (v2.0)
classify_listing_v2 출력:
  mount: "M" | "R" | "L" | "SL" | "S" | "V" | "Q" | "Compact" | "PNS" | "Unknown"

문제:
  Q / Compact / PNS 는 물리적 마운트가 아니라 제품 라인(product line)이다.
  이것이 mount 필드에 섞여 있어 QA 지표가 부정확해진다.

## 목표 스키마 (v2.1)
classify_listing_v2 출력:
  mount:  "M" | "R" | "L" | "SL" | "S" | "V" | "Unknown"   (물리적 마운트만)
  system: "Q" | "Q2" | "Q3" | "Compact" | "PNS" | "CL" | "TL" | None

## 마이그레이션 단계

### Step 1 — accessory_classifier.py 검증 (현재)
  - compatible_systems를 Accessory에서 추출 → 실데이터로 검증
  - detect_system()이 올바르게 동작하는지 확인

### Step 2 — classify_listing_v2에 system 필드 추가 (병행)
  classify_listing_v2 반환값에:
    "system": detect_system(nn, nd, mount=mt["mount"])
  추가. mount는 유지, system을 새로 추가하는 방식.

### Step 3 — auto_label 업데이트
  현재:
    if mount in ("Compact", "PNS", "Q"):
        label = "Leica Body" 또는 "Body"
  변경 후:
    if system in ("Q", "Compact", "PNS"):
        label = "Leica Body" 또는 "Body"

### Step 4 — detect_mount에서 Q/Compact/PNS 제거
  detect_mount가 반환하는 VALID_MOUNTS에서 Q/Compact/PNS 제거.
  대신 detect_system이 담당.

### Step 5 — QA 지표 업데이트
  compare_v1_v2에 system_match_pct 추가.
  v1의 mount=Q/Compact/PNS는 v2의 system으로 비교.

### 하위 호환 주의사항
  - results.json, index.html 등이 mount 필드를 직접 사용하는 경우
    system 필드 추가 후 mount도 유지해야 한다 (점진적 교체).
  - frontend가 system 필드를 인식하도록 업데이트 필요.
"""


# ─────────────────────────────────────────────
# 테스트
# ─────────────────────────────────────────────

if __name__ == "__main__":
    TEST_CASES = [
        # (name, mount, expected_type, expected_mounts, expected_systems)
        ("M-L Adapter Black",           "Unknown", "adapter",  ["M", "SL"],     []),
        ("Leica Q2 Bag Black",          "Q",       "bag",      [],              ["Q2", "Q"]),
        ("Leica Q2 Case Black",         "Q",       "case",     [],              ["Q2", "Q"]),
        ("Q2 Protector Blue",           "Unknown", "protector",[],              ["Q2", "Q"]),
        ("Leica M Hood 12585",          "Unknown", "hood",     ["M"],           ["M"]),
        ("Leica M6 Handgrip Black",     "M",       "grip",     ["M"],           ["M6", "M"]),
        ("Leica Visoflex II",           "M",       "visoflex", ["M"],           ["M"]),
        ("Leica Universal Polarizing Filter M", "M", "filter", ["M"],           ["M"]),
        ("LTM to M Adapter",            "Unknown", "adapter",  ["L", "M"],      []),
        ("R to M Adapter",              "Unknown", "adapter",  ["R", "M"],      []),
        ("Leica SF40 Flash",            "Unknown", "flash",    [],              []),
        ("Leica Q3 Case Blue",          "Q",       "case",     [],              ["Q3", "Q"]),
        ("Leica SL2 Battery",           "Unknown", "battery",  [],              ["SL2", "SL"]),
        ("Leica M Thumb Support",       "M",       "grip",     ["M"],           ["M"]),
    ]

    print("=" * 75)
    print("accessory_classifier 테스트")
    print("=" * 75)
    ok = fail = 0
    for name, mount, exp_type, exp_mts, exp_sys in TEST_CASES:
        r = classify_accessory(name, mount=mount)
        t_ok  = r["accessory_type"] == exp_type
        mt_ok = set(r["compatible_mounts"]) >= set(exp_mts)  # 최소 포함
        sys_ok= set(r["compatible_systems"]) >= set(exp_sys)
        all_ok = t_ok and mt_ok and sys_ok
        if all_ok: ok += 1
        else: fail += 1
        st = "✅" if all_ok else "❌"
        print(f"  {st} {name[:42]:<42} type={r['accessory_type']!r:<12} "
              f"mounts={r['compatible_mounts']}  systems={r['compatible_systems'][:2]}")
        if not t_ok:
            print(f"       ↳ type: exp={exp_type!r} got={r['accessory_type']!r}")
        if not mt_ok:
            print(f"       ↳ mounts: exp>={exp_mts} got={r['compatible_mounts']}")
        if not sys_ok:
            print(f"       ↳ systems: exp>={exp_sys} got={r['compatible_systems']}")

    print(f"\n결과: {ok}/{ok+fail} 통과")

    print("\n" + "=" * 75)
    print("system 분리 마이그레이션 계획")
    print("=" * 75)
    print(SYSTEM_MIGRATION_PLAN)
