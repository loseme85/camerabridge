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
    "repaint": r"re-?paint|nachlackiert|neu ?lackiert|リペイント|再塗装|리페인트|재도색|shueido|秀栄堂|後塗り|\bcustom\b(?!\s*(?:leather|leatherette|skin|strap|vulcanite))|カスタム|커스텀",  # 가죽만 바꾼 건 리페인트 아님
    # 캐나다(미드랜드) 생산 — 모델마다 뜻이 다름: M2·M3에선 희귀, M4-2·M4-P에선 기본이라 그 모델엔 갈래를 두지 않음
    "canada": r"\bELC\b|midland|\bcanada\b|カナダ|캐나다",
    # 모터 변형 (M2-M)
    "motor": r"\bM2-?M\b|\bM2M\b",
    # 시제품·사내용·선행 생산
    "rare": r"prototype|試作|プロトタイプ|betriebs|pre[- ]?series|pre[- ]?production|null[- ]?serie|0-?serie|\bgold\b|red ?curtain|rideau ?rouge|tendina ?rossa|roter ?vorhang",
    # 개조·변환 (바르낙 Umbau: I → II·III, IIIc → IIIf 등). 지금 모습(제목에서 뒤에 나온 모델)으로 보고 '개조·변환' 갈래
    "converted": r"umbau|umgebaut|convert(?:ed|ion)|upgraded? to|factory ?upgraded|aufgerüstet|nachträglich|改造|standardi[sz]ed",
    # 블랙/니켈 마감 — III(Model F)에선 크롬보다 비쌈(2026-11-21 데이터 2.1배), Leica I에선 기본 마감이라 갈래를 두지 않음
    "black-nickel": r"black ?/ ?nickel|black ?(?:and|&) ?nickel|black ?nickel|schwarz ?/? ?nickel|\bblack\b|schwarz|ブラック|黒",
    # 블랙페인트 — 라이카플렉스(SL)에서 크롬보다 훨씬 비쌈. M 바디는 기존 블랙페인트 갈래가 이미 있어 같은 결과
    "black-paint": r"black ?paint|blackpaint|블랙 ?페인트|ブラックペイント",
    # 기념판·한정판 표시 — 그 모델에 해당 판 갈래가 있으면 그 갈래가 먼저, 없으면 '확인 필요'
    "edition": r"\bedition\b|limited|限定|한정|signature|safari|サファリ|사파리|titan|チタン|티탄|anniversary|\bjahre\b|周年|주년",
}

# 상점 설명(매장정보.desc)·태그에서 읽는 특징 — 제목용 TRAITS와 따로, 아주 좁게 (2026-11-21 Shopify 58,387개 시험:
# 제목용 사전을 그대로 쓰면 'Ship to Canada'·'(Black)'·'gold contacts'·'no defects'가 걸려 오탐이 대부분이었음).
# 부정문('no defects')·호환 안내('does not work with M240')는 빼고, 부품용·작동 불가·리페인트만 읽는다.
DESC_TRAITS: dict[str, str] = {
    "defect": r"for parts|parts only|parts or repair|spares? or repair|\bnot working\b|won.t power on|"
              r"does(?:n.t| not) (?:work|function)(?!\s+(?:with|on|for|in|properly with))|\bjammed\b|ジャンク|bastelobjekt|ricambi",
    "repaint": r"(?<!un)(?<!not )re-?paint|nachlackiert|neu ?lackiert|リペイント|再塗装|리페인트|재도색|shueido|秀栄堂",
}

# 특징 → 갈래 이름 (모델이 그 갈래를 가질 때만)
TRAIT_BUCKET = {"repaint": "repaint", "canada": "canada", "motor": "m2-m", "rare": "rare", "edition": "review",
                "converted": "converted", "black-nickel": "black-nickel", "black-paint": "black-paint"}

# 새 갈래 이름 (영어 표시명 꼬리, 한국어 꼬리)
BUCKET_NAMES = {
    "repaint": ("Repaint · Custom", "리페인트·커스텀"),
    "canada": ("Canada (Midland)", "캐나다 생산"),
    "rare": ("Prototype · Rare", "시제품·희귀"),
    "review": ("Needs review", "확인 필요"),
    "converted": ("Converted (Umbau)", "개조·변환"),
    "black-nickel": ("Black / Nickel", "블랙/니켈"),
    "black-paint": ("Black Paint", "블랙페인트"),
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

# 바르낙 (2026-11-21 데이터로 정함: 레드 다이얼 IIIf 34개 1.1배·샤크스킨 IIIc 12개 1.1배 → 따로 두지 않음)
_BARNACK = ["converted", "repaint", "canada", "rare", "black-nickel", "*", "review", "standard"]
for _slug in ("i", "ic", "if", "ii", "iic", "iif", "iii", "iiia", "iiib", "iiic", "iiif", "iiig", "standard"):
    FAMILIES[f"leica:body:{_slug}"] = {"standard": ["standard"], "barnack": True, "priority": _BARNACK, "review_high": 2.5,
                                      "new": ["converted"] + (["black-nickel"] if _slug == "iii" else []) + (["canada"] if _slug == "iiif" else [])
                                      + ["repaint", "rare", "review"]}

# R 바디 (2026-11-23 ④ 넓히기): 라이카플렉스·R3~R9. 사파리·골드(R3)는 기존 갈래가 먼저('*'), 나머지 기념판은 확인 필요
for _slug, _black in (("leicaflex", True), ("leicaflex-sl", True), ("leicaflex-sl2", False), ("r3", False), ("r4", False), ("r4s", False),
                      ("r5", False), ("r-e", False), ("r6", False), ("r6-2", False), ("r7", False), ("r8", False), ("r9", False)):
    FAMILIES[f"leica:body:{_slug}"] = {"standard": ["standard"], "new": (["black-paint"] if _black else []) + ["repaint", "rare", "review"],
                                      "priority": (["black-paint"] if _black else []) + ["repaint", "*", "rare", "review", "standard"]}

# 필름·인스턴트·광학줌 콤팩트 (2026-11-23 ④ 넓히기): 한정판·시제품은 따로, 못 가린 것은 확인 필요. (D-Lux·Q·X는 이미 판별 갈래가 있음)
for _slug in ("sofort", "z2x", "mini", "minilux", "v-lux"):
    FAMILIES[f"leica:body:{_slug}"] = {"standard": ["standard"], "new": ["rare", "review"], "priority": ["rare", "*", "review", "standard"]}

# 가격 검문: 특징 없는 스탠다드 매물이 그 갈래 판매 중 중간값의 몇 배 밖이면 '확인 필요'
REVIEW_HIGH = 2.0  # 모델에 review_high가 있으면 그 값 (바르낙 2.5: 상태·정비에 따라 값 폭이 큼)
# 같은 자리에서 두 모델이 걸리면 넓은 이름보다 구체적인 모델 ('Leica III F' → IIIf, 'Leica I c' → Ic)
GENERIC_FAMILIES = {"leica:body:i", "leica:body:ii", "leica:body:iii", "leica:body:standard"}
REVIEW_LOW = 0.4
REVIEW_MIN_N = 6  # 중간값을 믿으려면 판매 중 매물이 이만큼은 있어야 함


def bucket_id(family: str, slug: str) -> str:
    return f"{family}:{slug}"


def add_children(MODELS: dict, PARENTS: dict, ALIASES: dict, NAME_KO: dict) -> None:
    """갈래표의 새 갈래를 엔티티로 추가한다. 제목 규칙으로는 붙지 않고(title_must가 절대 안 맞음) body_buckets.py만 옮긴다."""
    for family, spec in FAMILIES.items():
        if family not in PARENTS:  # 갈래가 없던 단일 모델(바르낙): 같은 ID를 '전체'로, 기존 규칙은 '스탠다드' 갈래로
            single = MODELS.pop(family)
            std = f"{family}:standard"
            name, ko = single["display_name"], NAME_KO.get(family) or single["display_name"]
            MODELS[std] = {**single, "model_key": std, "display_name": f"{name} (standard)"}
            short = name.replace("Leica ", "").split(" (")[0].lower()
            ALIASES[std] = [f"{short} standard", f"{short} 기본"]
            NAME_KO[std] = f"{ko} 기본형"
            PARENTS[family] = (f"{name} (all)", "Body", single["mount"], [std], ALIASES.pop(family, []), f"{ko} (전체)")
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
                     "rare": ["prototype", "시제품"], "review": ["needs review", "확인 필요"],
                     "converted": ["umbau", "converted", "개조"], "black-nickel": ["black nickel", "블랙 니켈"],
                     "black-paint": ["black paint", "블랙페인트"]}.get(slug, [])
            ALIASES[key] = ["leica m2-m", "m2-m", "m2m", "m2 motor"] if slug == "m2-m" else [f"{short} {w}" for w in words]
            NAME_KO[key] = display_ko
            kids = kids + [key]
        PARENTS[family] = (name, kind, mount, kids, aliases, name_ko)
