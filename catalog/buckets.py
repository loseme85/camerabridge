"""M 바디 갈래표 — 모델 그래프의 갈래(스탠다드·블랙페인트·…·확인 필요)를 정하는 지식표 (2026-11-21 분류 설계 시범).

설계: parkstudio 저장소 camera-bridge/분류설계.md
  - 스탠다드 = 공장 기본 마감 그대로, 에디션·시제품·리페인트·개조가 아닌 것 (사장님 2026-11-21)
  - 특징(TRAITS)은 여러 개 붙을 수 있다. 갈래는 모델마다 정한 우선순위(PRIORITY)에서 앞선 것 하나 (대분류 먼저: 블랙페인트 > 버튼 리와인드)
  - 고장·부품용(defect)은 그래프·시세에서 뺀다 (entity_note='defect')
  - 특징 없이 스탠다드 중간값의 2배를 넘거나 0.4배 밑이면 '확인 필요'(review) 갈래로 — 스탠다드를 더럽히지 않게

이 파일은 catalog/bodies.py(새 갈래 엔티티 추가)와 body_buckets.py(매물 갈래 정하기)가 같이 읽는다.
"""
from __future__ import annotations

# ── 특징 사전: 여러 언어 단서 (제목에서 찾음) ──
TRAITS: dict[str, str] = {
    # 고장·부품용 — 같은 물건이지만 제대로 된 매물이 아님 → 그래프에서 뺌 (2026-11-21 사장님)
    "defect": r"for parts|parts only|\bparts\s*[-–:]|bastel|ジャンク|\bjunk\b|\bas[- ]is\b|faulty|defect|corroded|부품용|고장품|"
              r"\bLEGGI\b|ricambi|for (?:restoration|repair)|\brestoration\b|senza lenti",
    # 리페인트·커스텀 (비공식 도색·개조 외장)
    "repaint": r"re-?paint|nachlackiert|neu ?lackiert|リペイント|再塗装|리페인트|재도색|shueido|秀栄堂|\bcustom\b(?!\s*(?:leather|leatherette|skin|strap|vulcanite))|カスタム|커스텀",  # 가죽만 바꾼 건 리페인트 아님
    # 캐나다(미드랜드) 생산 — 모델마다 뜻이 다름: M2·M3에선 희귀, M4-2·M4-P에선 기본이라 그 모델엔 갈래를 두지 않음
    "canada": r"\bELC\b|midland|\bcanada\b|カナダ|캐나다",
    # 모터 변형 (M2-M)
    "motor": r"\bM2-?M\b|\bM2M\b",
    # 시제품·사내용·선행 생산
    "rare": r"prototype|試作|プロトタイプ|betriebs|pre[- ]?series|pre[- ]?production|null[- ]?serie|0-?serie",
    # 기념판·한정판 표시 — 그 모델에 해당 판 갈래가 있으면 그 갈래가 먼저, 없으면 '확인 필요'
    "edition": r"\bedition\b|limited|限定|한정|signature|safari|サファリ|사파리|titan|チタン|티탄|anniversary|\bjahre\b|周年|주년",
}

# 특징 → 갈래 이름 (모델이 그 갈래를 가질 때만)
TRAIT_BUCKET = {"repaint": "repaint", "canada": "canada", "motor": "m2-m", "rare": "rare", "edition": "review"}

# 새 갈래 이름 (영어 표시명 꼬리, 한국어 꼬리)
BUCKET_NAMES = {
    "repaint": ("Repaint · Custom", "리페인트·커스텀"),
    "canada": ("Canada (Midland)", "캐나다 생산"),
    "rare": ("Prototype · Rare", "시제품·희귀"),
    "review": ("Needs review", "확인 필요"),
}

# ── 모델별 갈래표 ──
# standard: 그 모델의 기본형 갈래 (M6는 클래식·TTL 둘)
# new: 이 시범에서 새로 만드는 갈래
# priority: 매물에 해당하는 갈래가 여럿이면 앞선 것. "*" = 표에 없는 기존 갈래(기념판 등)
_COMMON = ["*", "repaint", "rare", "review"]
FAMILIES: dict[str, dict] = {
    "leica:body:m3": {"standard": ["standard"], "new": ["canada", "repaint", "rare", "review"],
                      "priority": ["black-paint", "first-batch", "early", "repaint", "canada", "rare", "*", "review", "double-stroke", "single-stroke", "standard"]},
    "leica:body:m2": {"standard": ["standard"], "new": ["m2-m", "canada", "repaint", "rare", "review"],
                      "priority": ["black-paint", "m2-m", "canada", "repaint", "rare", "*", "review", "button-rewind", "standard"]},
    "leica:body:m4": {"standard": ["standard"], "new": ["repaint", "rare", "review"], "priority": ["black-paint"] + _COMMON + ["standard"]},
    "leica:body:m4-2": {"standard": ["standard"], "new": ["repaint", "rare", "review"], "priority": _COMMON + ["standard"]},
    "leica:body:m4-p": {"standard": ["standard"], "new": ["repaint", "rare", "review"], "priority": _COMMON + ["standard"]},
    "leica:body:m5": {"standard": ["standard"], "new": ["repaint", "rare", "review"], "priority": _COMMON + ["standard"]},
    "leica:body:m6": {"standard": ["classic", "ttl"], "new": ["repaint", "rare", "review"], "priority": _COMMON + ["ttl", "classic"]},
    "leica:body:m7": {"standard": ["standard"], "new": ["repaint", "rare", "review"], "priority": _COMMON + ["standard"]},
    "leica:body:mp-film": {"standard": ["standard"], "new": ["repaint", "rare", "review"], "priority": ["black-paint"] + _COMMON + ["standard"]},
    "leica:body:m-a": {"standard": ["standard"], "new": ["repaint", "rare", "review"], "priority": _COMMON + ["standard"]},
    "leica:body:m8": {"standard": ["standard"], "new": ["repaint", "rare", "review"], "priority": _COMMON + ["standard"]},
    "leica:body:m9": {"standard": ["standard"], "new": ["repaint", "rare", "review"], "priority": _COMMON + ["standard"]},
    "leica:body:m9-p": {"standard": ["standard"], "new": ["repaint", "rare", "review"], "priority": _COMMON + ["standard"]},
    "leica:body:m240": {"standard": ["standard"], "new": ["repaint", "rare", "review"], "priority": _COMMON + ["standard"]},
    "leica:body:m-p240": {"standard": ["standard"], "new": ["repaint", "rare", "review"], "priority": _COMMON + ["standard"]},
    "leica:body:m10": {"standard": ["standard"], "new": ["repaint", "rare", "review"], "priority": _COMMON + ["standard"]},
    "leica:body:m10-p": {"standard": ["standard"], "new": ["repaint", "rare", "review"], "priority": _COMMON + ["standard"]},
    "leica:body:m11": {"standard": ["standard"], "new": ["repaint", "rare", "review"], "priority": _COMMON + ["standard"]},
    "leica:body:m11-p": {"standard": ["standard"], "new": ["repaint", "rare", "review"], "priority": _COMMON + ["standard"]},
}

# 가격 검문: 특징 없는 스탠다드 매물이 그 갈래 판매 중 중간값의 몇 배 밖이면 '확인 필요'
REVIEW_HIGH = 2.0
REVIEW_LOW = 0.4
REVIEW_MIN_N = 6  # 중간값을 믿으려면 판매 중 매물이 이만큼은 있어야 함


def bucket_id(family: str, slug: str) -> str:
    return f"{family}:{slug}"


def add_children(MODELS: dict, PARENTS: dict, ALIASES: dict, NAME_KO: dict) -> None:
    """갈래표의 새 갈래를 엔티티로 추가한다. 제목 규칙으로는 붙지 않고(title_must가 절대 안 맞음) body_buckets.py만 옮긴다."""
    for family, spec in FAMILIES.items():
        name, kind, mount, kids, aliases, name_ko = PARENTS[family]
        base = name.replace(" (all)", "")
        base_ko = (name_ko or base).replace(" (전체)", "")
        for slug in spec["new"]:
            key = bucket_id(family, slug)
            if key in MODELS:
                continue
            en, ko = BUCKET_NAMES.get(slug, ("", ""))
            if slug == "m2-m":
                en, ko = "M2-M (Motor)", "M2-M (모터)"
                display, display_ko = "Leica M2-M (Motor)", "라이카 M2-M (모터)"
            else:
                display, display_ko = f"{base} {en}", f"{base_ko} {ko}"
            MODELS[key] = {"model_key": key, "display_name": display, "category": "Body", "mount": mount,
                           "title_must": [r"(?!)"], "title_must_not": []}
            short = base.replace("Leica ", "").lower()
            words = {"repaint": ["repaint", "리페인트", "custom"], "canada": ["canada", "캐나다", "midland"],
                     "rare": ["prototype", "시제품"], "review": ["needs review", "확인 필요"]}.get(slug, [])
            ALIASES[key] = ["leica m2-m", "m2-m", "m2m", "m2 motor"] if slug == "m2-m" else [f"{short} {w}" for w in words]
            NAME_KO[key] = display_ko
            kids = kids + [key]
        PARENTS[family] = (name, kind, mount, kids, aliases, name_ko)
