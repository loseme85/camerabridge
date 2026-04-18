"""
golden_set.py
=============
classifier_v2 고정 회귀 테스트셋.

정책:
  - model_raw:       상품명 그대로 추출한 모델명
  - model_canonical: mount/시스템 반영한 표준 모델명 (집계/시세용)
  - variant:         세부 가치 차이 요소 (검사 안 함, 추후 추가 가능)
  - 케이스를 줄이지 않는다 (회귀 방지)
  - expected에 없는 필드는 검사하지 않는다
"""

GOLDEN_SET: list[dict] = [

    # ══════════════════════════════════════════
    # M 마운트 렌즈
    # ══════════════════════════════════════════
    {
        "name": "Leica Summicron-M 35mm f/2 ASPH",
        "price": "3,500,000",
        "expected": {
            "mount": "M", "category": "Lens", "label": "M Lens",
            "model_raw": "Summicron-M", "model_canonical": "Summicron-M",
            "focal_length": "35",
        },
    },
    {
        "name": "Leica Summilux-M 50mm f/1.4 ASPH Black",
        "price": "5,800,000",
        "expected": {
            "mount": "M", "category": "Lens", "label": "M Lens",
            "model_raw": "Summilux-M", "model_canonical": "Summilux-M",
            "focal_length": "50",
        },
    },
    {
        "name": "Leica Noctilux-M 50mm f/0.95 ASPH Black",
        "price": "9,000,000",
        "expected": {
            "mount": "M", "category": "Lens", "label": "M Lens",
            "model_raw": "Noctilux", "model_canonical": "Noctilux",
            "focal_length": "50",
        },
    },
    {
        "name": "Leica M 28mm f1.4 Summilux ASPH 6bit Black",
        "price": "7,000,000",
        "expected": {
            "mount": "M", "category": "Lens", "label": "M Lens",
            "model_raw": "Summilux", "model_canonical": "Summilux-M",
            "focal_length": "28",
        },
    },
    {
        "name": "Leica M 90mm f2.5 Summarit 6bit Black",
        "price": "1,200,000",
        "expected": {
            "mount": "M", "category": "Lens", "label": "M Lens",
            "model_raw": "Summarit", "model_canonical": "Summarit-M",
            "focal_length": "90",
        },
    },
    {
        "name": "Leica M 16-18-21mm f4 Tri-Elmar ASPH 6bit",
        "price": "2,800,000",
        "expected": {
            "mount": "M", "category": "Lens", "label": "M Lens",
            "model_raw": "Tri-Elmar", "model_canonical": "Tri-Elmar",
            "focal_length": "16-18-21",
        },
    },
    {
        "name": "35mm Summicron 8-element",
        "price": "2,500,000",
        "expected": {
            "mount": "M", "category": "Lens", "label": "M Lens",
            "model_raw": "Summicron", "model_canonical": "Summicron-M",
            "focal_length": "35",
        },
    },

    # ══════════════════════════════════════════
    # 3rd Party M 마운트 렌즈
    # ══════════════════════════════════════════
    {
        "name": "[중고] Voigtlander Nokton 50mm f/1.1 VM",
        "price": "800,000",
        "expected": {
            "brand": "3rd Party", "mount": "M", "category": "Lens",
            "label": "3rd Party M Lens",
            "model_raw": "Nokton", "model_canonical": "Nokton",
            "focal_length": "50",
        },
    },
    {
        "name": "[위탁] Zeiss Biogon ZM 35mm f/2",
        "price": "600,000",
        "expected": {
            "brand": "3rd Party", "mount": "M", "category": "Lens",
            "label": "3rd Party M Lens",
            "model_raw": "Biogon", "model_canonical": "Biogon",
            "focal_length": "35",
        },
    },
    {
        "name": "TTArtisan 50mm f/0.95 M mount",
        "price": "350,000",
        "expected": {
            "brand": "3rd Party", "mount": "M", "category": "Lens",
            "label": "3rd Party M Lens",
            "focal_length": "50",
        },
    },
    {
        "name": "Light Lens Lab M 50mm f1.5 Z21 Black",
        "price": "1,200,000",
        "expected": {
            "mount": "M", "category": "Lens", "label": "3rd Party M Lens",
        },
    },

    # ══════════════════════════════════════════
    # R 마운트 렌즈
    # ══════════════════════════════════════════
    {
        "name": "Leica R 50mm f2 Summicron Black",
        "price": "600,000",
        "expected": {
            "mount": "R", "category": "Lens", "label": "R Lens",
            "model_raw": "Summicron", "model_canonical": "Summicron-R",
            "focal_length": "50",
        },
    },
    {
        "name": "Leica R 28mm f2.8 Elmarit Rom Black",
        "price": "500,000",
        "expected": {
            "mount": "R", "category": "Lens", "label": "R Lens",
            "model_raw": "Elmarit", "model_canonical": "Elmarit-R",
            "focal_length": "28",
        },
    },
    {
        "name": "Leica R 180mm f2.8 APO-Elmarit Rom Black",
        "price": "1,800,000",
        "expected": {
            "mount": "R", "category": "Lens", "label": "R Lens",
            "model_raw": "APO-Elmarit", "model_canonical": "APO-Macro-Elmarit-R",
            "focal_length": "180",
        },
    },
    {
        "name": "Leica R 70-180mm f2.8 Vario-Apo-Elmarit",
        "price": "3,000,000",
        "expected": {
            "mount": "R", "category": "Lens", "label": "R Lens",
            "focal_length": "70-180",
        },
    },
    {
        "name": "Leica R 350mm f4.8 Telyt Black",
        "price": "800,000",
        "expected": {
            "mount": "R", "category": "Lens", "label": "R Lens",
            "model_raw": "Telyt", "model_canonical": "Telyt-R",
            "focal_length": "350",
        },
    },
    {
        "name": "Summilux-R 50mm f/1.4 3CAM",
        "price": "2,000,000",
        "expected": {
            "mount": "R", "category": "Lens", "label": "R Lens",
            "model_raw": "Summilux-R", "model_canonical": "Summilux-R",
            "focal_length": "50",
        },
    },

    # ══════════════════════════════════════════
    # L 마운트 (나사마운트 / Barnack)
    # ══════════════════════════════════════════
    {
        "name": "Leica L 50mm f1.5 Summarit Silver",
        "price": "900,000",
        "expected": {
            "mount": "L", "category": "Lens", "label": "L Lens",
            "model_raw": "Summarit", "model_canonical": "Summarit",
            "focal_length": "50",
        },
    },
    {
        "name": "Leica L 50mm f3.5 Elmar",
        "price": "400,000",
        "expected": {
            "mount": "L", "category": "Lens", "label": "L Lens",
            "model_raw": "Elmar", "model_canonical": "Elmar",
            "focal_length": "50",
        },
    },
    {
        "name": "Leica L 35mm f2 APO-Summicron",
        "price": "8,000,000",
        "expected": {
            "mount": "L", "category": "Lens", "label": "L Lens",
            "model_raw": "APO-Summicron", "model_canonical": "APO-Summicron",
            "focal_length": "35",
        },
    },
    {
        "name": "LEICA IIIF Body",
        "price": "1,200,000",
        "expected": {
            "mount": "L", "category": "Body", "label": "L Body",
            "model_raw": "IIIf", "model_canonical": "IIIf",
        },
    },
    {
        "name": "Leica Barnack IIIF Silver",
        "price": "1,100,000",
        "expected": {
            "mount": "L", "category": "Body", "label": "L Body",
        },
    },
    {
        "name": "Leica IIIg Body",
        "price": "1,500,000",
        "expected": {
            "mount": "L", "category": "Body", "label": "L Body",
            "model_raw": "IIIg", "model_canonical": "IIIg",
        },
    },

    # ══════════════════════════════════════════
    # SL 마운트 렌즈 / 바디
    # ══════════════════════════════════════════
    {
        "name": "Leica SL 24-90mm f2.8-4 Vario-Elmarit Black",
        "price": "4,500,000",
        "expected": {
            "mount": "SL", "category": "Lens", "label": "SL Lens",
            "model_raw": "Vario-Elmarit", "model_canonical": "Vario-Elmarit-SL",
            "focal_length": "24-90",
        },
    },
    {
        "name": "Leica SL2 Body Black",
        "price": "7,000,000",
        "expected": {
            "mount": "SL", "category": "Body", "label": "SL Body",
            "model_raw": "SL2", "model_canonical": "SL2",
        },
    },
    {
        "name": "Sigma L 30mm f1.4 DC DN Black for CL TL",
        "price": "400,000",
        "expected": {
            "brand": "3rd Party", "mount": "SL", "category": "Lens",
            "label": "SL Lens", "focal_length": "30",
        },
    },
    {
        "name": "Lumix S Pro 70-200mm f4 OIS Black",
        "price": "1,500,000",
        "expected": {
            "mount": "SL", "category": "Lens", "label": "SL Lens",
            "focal_length": "70-200",
        },
    },
    {
        "name": "Sigma 85mm f1.4 DG HSM L",
        "price": "700,000",
        "expected": {
            "mount": "SL", "category": "Lens", "label": "SL Lens",
            "focal_length": "85",
        },
    },

    # ══════════════════════════════════════════
    # M 바디
    # ══════════════════════════════════════════
    {
        "name": "Leica M6 TTL 0.72 Body",
        "price": "5,000,000",
        "expected": {
            "mount": "M", "category": "Body", "label": "M Body",
            "model_raw": "M6 TTL", "model_canonical": "M6",
        },
    },
    {
        "name": "Leica M3 Silver",
        "price": "3,200,000",
        "expected": {
            "mount": "M", "category": "Body", "label": "M Body",
            "model_raw": "M3", "model_canonical": "M3",
        },
    },
    {
        "name": "Leica M11 Black",
        "price": "10,000,000",
        "expected": {
            "mount": "M", "category": "Body", "label": "M Body",
            "model_raw": "M11", "model_canonical": "M11",
        },
    },

    # ══════════════════════════════════════════
    # Q / Compact / PNS
    # ══════════════════════════════════════════
    {
        "name": "Leica Q2 Monochrom",
        "price": "6,000,000",
        "expected": {
            "mount": "Q", "category": "Body", "label": "Leica Body",
            "model_raw": "Q2 Monochrom", "model_canonical": "Q2",
        },
    },
    {
        "name": "Leica D-LUX 7 Black",
        "price": "1,200,000",
        "expected": {
            "mount": "Compact", "category": "Body",
            "model_raw": "D-LUX 7", "model_canonical": "D-LUX 7",
        },
    },
    {
        "name": "Leica Minilux Zoom Silver",
        "price": "400,000",
        "expected": {
            "mount": "PNS", "category": "Body",
            "model_raw": "Minilux Zoom", "model_canonical": "Minilux",
        },
    },

    # ══════════════════════════════════════════
    # Hasselblad V 마운트
    # ══════════════════════════════════════════
    {
        "name": "Hasselblad 503CW Body",
        "price": "3,200,000",
        "expected": {
            "brand": "Hasselblad", "mount": "V", "category": "Body",
            "label": "V Body",
        },
    },
    {
        "name": "Hasselblad CF 80mm f2.8 Planar",
        "price": "500,000",
        "expected": {
            "brand": "Hasselblad", "mount": "V", "category": "Lens",
            "label": "V Lens",
            "model_raw": "Planar", "model_canonical": "Planar",
            "focal_length": "80",
        },
    },

    # ══════════════════════════════════════════
    # 액세서리
    # ══════════════════════════════════════════
    {
        "name": "Leica 후드 12585",
        "price": "80,000",
        "expected": {"category": "Accessory", "label": "Accessory"},
    },
    {
        "name": "[중고] Leica M 스트랩 블랙",
        "price": "50,000",
        "expected": {"category": "Accessory", "label": "Accessory"},
    },
    {
        "name": "Leica Visoflex II",
        "price": "200,000",
        "expected": {"category": "Accessory", "label": "Accessory"},
    },
    {
        "name": "Leica ITOOY Finder",
        "price": "150,000",
        "expected": {"category": "Accessory", "label": "Accessory"},
    },

    # ══════════════════════════════════════════
    # 엣지 케이스
    # ══════════════════════════════════════════
    {
        "name": "Leica R 35mm f2 Summicron-R",
        "price": "700,000",
        "expected": {
            "mount": "R", "category": "Lens", "label": "R Lens",
            "model_raw": "Summicron-R", "model_canonical": "Summicron-R",
        },
    },
    {
        "name": "Leica M6 TTL 판매완료",
        "price": "",
        "expected": {"sold_quality": "sold_confirmed"},
    },
    {
        "name": "Leica UV 필터 E46",
        "price": "60,000",
        "expected": {"category": "Accessory", "label": "Accessory"},
    },
]


# ─────────────────────────────────────────────
# 실행기
# ─────────────────────────────────────────────

def run_golden_set(classify_fn, verbose: bool = True) -> dict:
    total = len(GOLDEN_SET)
    passed = failed = 0
    failures = []

    for case in GOLDEN_SET:
        item = {"상품명": case["name"], "가격": case.get("price", "")}
        result = classify_fn(item)
        expected = case["expected"]

        case_ok = True
        mismatches = []
        for field, exp_val in expected.items():
            if exp_val is None:
                continue
            actual = result.get(field)
            if actual != exp_val:
                case_ok = False
                mismatches.append(f"{field}: expected={exp_val!r}  actual={actual!r}")

        if case_ok:
            passed += 1
            if verbose:
                print(f"  ✅ {case['name'][:58]}")
        else:
            failed += 1
            failures.append({"name": case["name"], "mismatches": mismatches})
            if verbose:
                print(f"  ❌ {case['name'][:58]}")
                for m in mismatches:
                    print(f"       ↳ {m}")

    pct = round(passed / total * 100, 1)
    print(f"\n골든셋 결과: {passed}/{total} ({pct}%) 통과")
    return {"total": total, "passed": passed, "failed": failed,
            "pass_rate": pct, "failures": failures}


# ── 이번 라운드 추가 케이스 (M mount 서드파티/약식, Accessory/Lens 경계) ──

_NEW_CASES = [
    # M mount 서드파티 브랜드
    {
        "name": "Thypoch Simera 35mm f/1.4 M",
        "price": "800,000",
        "expected": {"mount": "M", "category": "Lens", "label": "3rd Party M Lens",
                     "focal_length": "35"},
    },
    {
        "name": "Handevision IBELUX 40mm f/0.85 M",
        "price": "600,000",
        "expected": {"mount": "M", "category": "Lens", "label": "3rd Party M Lens",
                     "focal_length": "40"},
    },
    {
        "name": "TTArtisan 35mm f/1.4 for Leica M",
        "price": "350,000",
        "expected": {"mount": "M", "category": "Lens", "label": "3rd Party M Lens",
                     "focal_length": "35"},
    },
    {
        "name": "7Artisans 35mm f/2 M mount Black",
        "price": "280,000",
        "expected": {"mount": "M", "category": "Lens", "label": "3rd Party M Lens",
                     "focal_length": "35"},
    },
    # M mount 약식/한국어
    {
        "name": "[중고] 50mm f/2 M 마운트",
        "price": "350,000",
        "expected": {"mount": "M", "category": "Lens"},
    },
    {
        "name": "라이카 M 35mm 써드파티 렌즈",
        "price": "500,000",
        "expected": {"mount": "M", "category": "Lens"},
    },
    {
        "name": "35mm f/2 for M",
        "price": "400,000",
        "expected": {"mount": "M", "category": "Lens", "focal_length": "35"},
    },
    # Accessory/Lens 경계 — Q2 시스템 악세사리
    {
        "name": "Leica Q2 Bag Black",
        "price": "150,000",
        "expected": {"category": "Accessory", "label": "Accessory"},
    },
    {
        "name": "Leica Q2 Case Black",
        "price": "80,000",
        "expected": {"category": "Accessory", "label": "Accessory"},
    },
    {
        "name": "Q2 Protector Blue",
        "price": "50,000",
        "expected": {"category": "Accessory", "label": "Accessory"},
    },
    # M 시스템 악세사리 — mount 힌트 있는 Accessory
    {
        "name": "Leica M 스트랩 블랙",
        "price": "50,000",
        "expected": {"mount": "M", "category": "Accessory", "label": "Accessory"},
    },
]

# 기존 GOLDEN_SET에 추가
GOLDEN_SET.extend(_NEW_CASES)


# ── 실데이터 회귀 방지용 Accessory 케이스 추가 ──

_ACC_REGRESSION_CASES = [
    # Q/Compact system Accessory — mount 신호 있어도 Accessory여야 함
    {"name": "Leica Q3 Round Hood Black",    "price": "120,000",
     "expected": {"category": "Accessory", "label": "Accessory"}},
    {"name": "Leica Q3 Holster Black",       "price": "150,000",
     "expected": {"category": "Accessory", "label": "Accessory"}},
    {"name": "Leica D-LUX 7 Case Black",     "price": "80,000",
     "expected": {"category": "Accessory", "label": "Accessory"}},
    # M mount Accessory — mount=M이어도 Accessory
    {"name": "Leica M Adapter L",            "price": "350,000",
     "expected": {"category": "Accessory", "label": "Accessory",
                  "accessory_type": "adapter"}},
    {"name": "Leica M to L Adapter",         "price": "300,000",
     "expected": {"category": "Accessory", "label": "Accessory",
                  "accessory_type": "adapter"}},
    {"name": "Leica M10 Handgrip Black",     "price": "150,000",
     "expected": {"category": "Accessory", "label": "Accessory"}},
    {"name": "Leica M11 Protector Black",    "price": "80,000",
     "expected": {"category": "Accessory", "label": "Accessory"}},
    {"name": "Leica Thumb Support M Black",  "price": "60,000",
     "expected": {"category": "Accessory", "label": "Accessory"}},
    # Visoflex
    {"name": "Leica Visoflex Type 020",      "price": "200,000",
     "expected": {"category": "Accessory", "label": "Accessory",
                  "accessory_type": "visoflex"}},
    # 파인더 / 필터 / 후드
    {"name": "Leica Universal Finder",       "price": "200,000",
     "expected": {"category": "Accessory", "label": "Accessory",
                  "accessory_type": "finder"}},
    {"name": "Leica UVa II Filter M 46mm",   "price": "80,000",
     "expected": {"category": "Accessory", "label": "Accessory",
                  "accessory_type": "filter"}},
    {"name": "Leica Hood 12585 Black",       "price": "80,000",
     "expected": {"category": "Accessory", "label": "Accessory",
                  "accessory_type": "hood"}},
    # 스트랩 / 케이스
    {"name": "Leica SL Hand Strap Black",    "price": "80,000",
     "expected": {"category": "Accessory", "label": "Accessory",
                  "accessory_type": "strap"}},
    {"name": "Leica Q2 Ghost Edition Case",  "price": "150,000",
     "expected": {"category": "Accessory", "label": "Accessory",
                  "accessory_type": "case"}},
    # M-L 어댑터 compatibility 검증
    {"name": "M-L Adapter Black",            "price": "150,000",
     "expected": {"category": "Accessory", "label": "Accessory",
                  "accessory_type": "adapter", "compatible_mounts": ["M", "SL"]}},
]

GOLDEN_SET.extend(_ACC_REGRESSION_CASES)


# ── Hard Accessory 강화 + M alias 확장 케이스 ──

_HARDENING_CASES = [
    # Extender → Accessory
    {"name": "Leica APO Extender R 1.4x",       "price": "300,000",
     "expected": {"category": "Accessory", "label": "Accessory"}},
    {"name": "Leica Extender R 2x",             "price": "200,000",
     "expected": {"category": "Accessory", "label": "Accessory"}},
    # Base Plate → Accessory (Q/M mount 있어도)
    {"name": "Leica Q2 Base Plate Black",        "price": "60,000",
     "expected": {"category": "Accessory", "label": "Accessory"}},
    {"name": "Leica M10 Base Plate",             "price": "80,000",
     "expected": {"category": "Accessory", "label": "Accessory"}},
    # EVF / Flash → Accessory
    {"name": "Leica EVF2 Electronic Viewfinder", "price": "300,000",
     "expected": {"category": "Accessory", "label": "Accessory"}},
    {"name": "Leica SF64 Flash Black",           "price": "200,000",
     "expected": {"category": "Accessory", "label": "Accessory",
                  "accessory_type": "flash"}},
    # Soft Release / Hot Shoe → Accessory
    {"name": "Leica M Soft Release Button",      "price": "30,000",
     "expected": {"category": "Accessory", "label": "Accessory"}},
    # M-Hexanon → M mount
    {"name": "Konica M-Hexanon 50mm f/2 Black",  "price": "400,000",
     "expected": {"mount": "M", "category": "Lens", "label": "3rd Party M Lens",
                  "focal_length": "50"}},
    {"name": "Konica M-Hexanon 28mm f/2.8",      "price": "500,000",
     "expected": {"mount": "M", "category": "Lens", "label": "3rd Party M Lens",
                  "focal_length": "28"}},
    # Konica Hexanon LTM → L mount
    {"name": "Konica Hexanon 35mm f/2 LTM",      "price": "500,000",
     "expected": {"mount": "L", "category": "Lens", "focal_length": "35"}},
    # 추가 M alias
    {"name": "Peace 50mm f/2 M mount Black",     "price": "400,000",
     "expected": {"mount": "M", "category": "Lens", "focal_length": "50"}},
    {"name": "Mandler Optics 50mm f/1.5 M",      "price": "800,000",
     "expected": {"mount": "M", "category": "Lens", "focal_length": "50"}},
    {"name": "Polar 35mm f/2 M mount Black",     "price": "350,000",
     "expected": {"mount": "M", "category": "Lens", "focal_length": "35"}},
]

GOLDEN_SET.extend(_HARDENING_CASES)


# ── L/SL/LTM 분해 + S/R 누수 + Optical Accessory hardening ──

_MOUNT_REFINEMENT_CASES = [
    # R 누수 수정 — APO prefix + LEICA R 조합
    {"name": "Leica R APO-Summicron 90mm f2 Black", "price": "800,000",
     "expected": {"mount": "R", "category": "Lens", "label": "R Lens"}},
    {"name": "Leica R APO-Telyt 280mm f4",           "price": "600,000",
     "expected": {"mount": "R", "category": "Lens", "label": "R Lens"}},
    # 서드파티 trailing L → SL
    {"name": "TTArtisan 90mm f1.25 L",               "price": "600,000",
     "expected": {"mount": "SL", "category": "Lens", "label": "SL Lens"}},
    {"name": "Laowa 20mm f4 Zero-D L",               "price": "800,000",
     "expected": {"mount": "SL", "category": "Lens", "label": "SL Lens"}},
    # Cooke LTM → L
    {"name": "Cooke Amotal 2inch f2",                "price": "500,000",
     "expected": {"mount": "L", "category": "Lens", "label": "L Lens"}},
    {"name": "Cooke Kinetal 40mm f1.5",              "price": "400,000",
     "expected": {"mount": "L", "category": "Lens", "label": "L Lens"}},
    # Carl Zeiss C model → L (ZM M mount과 구분)
    {"name": "Carl Zeiss C 50mm f1.5 Sonnar",        "price": "800,000",
     "expected": {"mount": "L", "category": "Lens"}},
    {"name": "Carl Zeiss C Biogon 21mm f4.5",        "price": "600,000",
     "expected": {"mount": "L", "category": "Lens"}},
    # ZM은 여전히 M
    {"name": "[위탁] Zeiss Biogon ZM 35mm f/2",      "price": "600,000",
     "expected": {"mount": "M", "category": "Lens", "label": "3rd Party M Lens"}},
    # S 마운트
    {"name": "Leica S 30mm f2.8 Elmarit ASPH CS",   "price": "3,000,000",
     "expected": {"mount": "S", "category": "Lens", "label": "S Lens"}},
    {"name": "Leica Summarit-S 70mm f2.5 CS",        "price": "1,500,000",
     "expected": {"mount": "S", "category": "Lens", "label": "S Lens"}},
    # Leica L prefix (나사마운트) — SL과 구분 유지
    {"name": "Leica L 50mm f3.5 Elmar",              "price": "400,000",
     "expected": {"mount": "L", "category": "Lens", "label": "L Lens"}},
]

GOLDEN_SET.extend(_MOUNT_REFINEMENT_CASES)


# ── Accessory hard gate + L token/R/S priority 회귀 케이스 ──

_BOUNDARY_REFINEMENT_CASES = [
    # UV/UVa/filter 계열 — E 구경, mm 숫자, mount 신호가 있어도 Accessory
    {"name": "Leica E82 UVa II Black",           "price": "250,000",
     "expected": {"category": "Accessory", "label": "Accessory"}},
    {"name": "Leica UV 60mm Black",              "price": "250,000",
     "expected": {"category": "Accessory", "label": "Accessory"}},
    {"name": "Leica Universal Polarizing Filter M", "price": "180,000",
     "expected": {"category": "Accessory", "label": "Accessory"}},
    # plural thumb support / meter / rig
    {"name": "Leica M10, M11 Thumbs Support Silver", "price": "150,000",
     "expected": {"category": "Accessory", "label": "Accessory"}},
    {"name": "Sekonic L-508 Zoom Master Black",  "price": "250,000",
     "expected": {"category": "Accessory", "label": "Accessory"}},
    {"name": "DJI RS 3 Combo",                   "price": "400,000",
     "expected": {"category": "Accessory", "label": "Accessory"}},
    # third-party modern L token — M brand fallback보다 먼저 SL로 고정
    {"name": "TTArtisan L 90mm f1.25 DJ-Optical Black", "price": "600,000",
     "expected": {"mount": "SL", "category": "Lens", "label": "SL Lens"}},
    {"name": "TTArtisan L 90/1.25 DJ-Optical Black", "price": "600,000",
     "expected": {"mount": "SL", "category": "Lens", "label": "SL Lens"}},
    {"name": "Laowa L 20mm f4 Zero-D Shift Black",      "price": "800,000",
     "expected": {"mount": "SL", "category": "Lens", "label": "SL Lens"}},
    # R/S explicit priority — M 렌즈 키워드보다 먼저 평가
    {"name": "Leica R 70-210/4 Vario-Elmar",     "price": "500,000",
     "expected": {"mount": "R", "category": "Lens", "label": "R Lens"}},
    {"name": "Leica APO-Macro-Summarit 120mm f2.5 CS", "price": "1,500,000",
     "expected": {"mount": "S", "category": "Lens", "label": "S Lens"}},
]

GOLDEN_SET.extend(_BOUNDARY_REFINEMENT_CASES)


# ── shorthand mount/body + v1 accessory 왜곡 방지 케이스 ──

_SHORTHAND_REFINEMENT_CASES = [
    {"name": "M 21/2.8 Elmarit ASPH Silver",        "price": "2,000,000",
     "expected": {"mount": "M", "category": "Lens", "label": "M Lens"}},
    {"name": "SL 35/2 APO Summicron ASPH Black",    "price": "3,000,000",
     "expected": {"mount": "SL", "category": "Lens", "label": "SL Lens"}},
    {"name": "TL 35/1.4 Summilux ASPH Black",       "price": "1,200,000",
     "expected": {"mount": "SL", "category": "Lens", "label": "SL Lens"}},
    {"name": "Q3 28mm",                             "price": "8,000,000",
     "expected": {"mount": "Q", "category": "Body"}},
    {"name": "MDa Silver",                          "price": "1,200,000",
     "expected": {"mount": "M", "category": "Body", "label": "M Body"}},
    # v1이 Accessory로 오염된 실렌즈 후보 — v2는 Lens로 유지되어야 함
    {"name": "Leica M 50mm f1.4 Summilux ASPH 6bit Black chrome finish e43",
     "price": "4,000,000",
     "expected": {"mount": "M", "category": "Lens", "label": "M Lens"}},
    {"name": "Leica M 28-35-50mm f4 Tri-Elmar e49 신형 Black",
     "price": "4,000,000",
     "expected": {"mount": "M", "category": "Lens", "label": "M Lens"}},
    {"name": "Leica M 135mm f4 Tele-Elmar Black",   "price": "900,000",
     "expected": {"mount": "M", "category": "Lens", "label": "M Lens"}},
    {"name": "Leica L 90mm f4 Elmar Silver",        "price": "800,000",
     "expected": {"mount": "L", "category": "Lens", "label": "L Lens"}},
]

GOLDEN_SET.extend(_SHORTHAND_REFINEMENT_CASES)


# ── 명확한 accessory class hard gate 회귀 케이스 ──

_ACCESSORY_CLASS_REFINEMENT_CASES = [
    {"name": "SF 40",                            "price": "300,000",
     "expected": {"category": "Accessory", "label": "Accessory"}},
    {"name": "BP-SCL5",                         "price": "180,000",
     "expected": {"category": "Accessory", "label": "Accessory"}},
    {"name": "Soft Button 12mm Red",            "price": "50,000",
     "expected": {"category": "Accessory", "label": "Accessory"}},
    {"name": "B+W ND 1000 E46 Black Summarit 용", "price": "80,000",
     "expected": {"category": "Accessory", "label": "Accessory"}},
    {"name": "RRS SL2 L 플레이트",                "price": "120,000",
     "expected": {"category": "Accessory", "label": "Accessory"}},
    {"name": "Leica Books M The First 70 Years", "price": "80,000",
     "expected": {"category": "Accessory", "label": "Accessory"}},
]

GOLDEN_SET.extend(_ACCESSORY_CLASS_REFINEMENT_CASES)


# ── non-Leica / legacy abbreviation / L boundary 회귀 케이스 ──

_LEGACY_ABBREV_REFINEMENT_CASES = [
    # Non-Leica legacy SLR mount — Zeiss M fallback으로 흘리지 않음
    {"name": "Carlzeiss C/Y 18mm f4 Distagon Black", "price": "500,000",
     "expected": {"mount": "C/Y", "category": "Lens", "label": "3rd Party Lens"}},
    # Legacy M shorthand / compatibility-style body token — mount만 M으로 보강
    {"name": "M EV1",                              "price": "500,000",
     "expected": {"mount": "M", "category": "Lens"}},
    {"name": "호환 Vit For M2 Black",                "price": "150,000",
     "expected": {"mount": "M"}},
    # L shorthand here means Leica screw/LTM family, not modern L-mount
    {"name": "L 28/5.6 Summaron Silver",           "price": "1,200,000",
     "expected": {"mount": "L", "category": "Lens", "label": "L Lens"}},
    {"name": "L 50/3.5 Nickel Elmar",              "price": "800,000",
     "expected": {"mount": "L", "category": "Lens", "label": "L Lens"}},
]

GOLDEN_SET.extend(_LEGACY_ABBREV_REFINEMENT_CASES)


# ── Compact/PNS body explicit 회귀 케이스 ──

_COMPACT_PNS_REFINEMENT_CASES = [
    {"name": "Leica Minilux Black",          "price": "1,000,000",
     "expected": {"mount": "PNS", "category": "Body", "label": "Leica Body"}},
    {"name": "Leica Minilux Zoom",           "price": "1,000,000",
     "expected": {"mount": "PNS", "category": "Body", "label": "Leica Body"}},
    {"name": "Leica C2 Zoom Black",          "price": "300,000",
     "expected": {"mount": "PNS", "category": "Body", "label": "Leica Body"}},
    {"name": "Leica Sofort2 White",          "price": "300,000",
     "expected": {"mount": "Compact", "category": "Body", "label": "Leica Body"}},
    {"name": "Leica Sofort2 Burton Edition", "price": "400,000",
     "expected": {"mount": "Compact", "category": "Body", "label": "Leica Body"}},
]

GOLDEN_SET.extend(_COMPACT_PNS_REFINEMENT_CASES)


# ── Leica MP3 explicit-title mount 회귀 케이스 ──

_MP3_REFINEMENT_CASES = [
    {"name": "LEICA MP3 LHSA Special Edition 789/1000", "price": "문의요망",
     "expected": {"brand": "Leica", "mount": "M", "category": "Body", "label": "M Body"}},
    # 단독 MP3는 seller/source/label context 없이는 broad rule로 고정하지 않는다.
    {"name": "MP3 Silver Body", "price": "5,000,000",
     "expected": {"mount": "Unknown", "category": "Body"}},
]

GOLDEN_SET.extend(_MP3_REFINEMENT_CASES)


if __name__ == "__main__":
    from classifier_v2 import classify_listing_v2
    print("=" * 65)
    print("Golden Set 회귀 테스트")
    print("=" * 65)
    run_golden_set(classify_listing_v2)
