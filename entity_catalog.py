"""엔티티(모델) 카탈로그: 매물 → 엔티티 판정, 엔티티별 매물 연결.

카탈로그 원본은 catalog/build_entity_catalog.py, 결과는 data/config/entity_catalog_v1.json.
"""
from __future__ import annotations

import json
import re
from functools import lru_cache
from pathlib import Path
from typing import Any, Iterable

CATALOG_PATH = Path(__file__).resolve().parent / "data" / "config" / "entity_catalog_v1.json"
FX_PATH = Path(__file__).resolve().parent / "data" / "fx_rates.json"

# 제목만으로 세대를 못 가르는 모델은 가격으로 가른다: {모델: (값싼 쪽 모델, 원화 기준가, 표기가 있으면 가격 무시)}
# 녹티 f/1.2: 복각(ASPH) 중고·신품 약 550만~1,400만 원, 오리지널 약 3,300만 원 이상 (2026-10 수집분)
PRICE_SPLIT = {
    "leica:lens:noctilux:50:f1.2-original": ("leica:lens:noctilux-m:50:f1.2-asph", 20_000_000,
                                             re.compile(r"original|오리지널|1세대|\b1st\b", re.I)),
    # 주미룩스 R 50: 세대 표기 없는 매물 중 250만 원 미만은 1세대 (1세대 약 90만~165만 원, 2세대 E60 약 400만 원)
    "leica:lens:summilux-r:50:unspecified": ("leica:lens:summilux-r:50:v1", 2_500_000, re.compile(r"(?!)")),
    # 주미크론 28 ASPH: 세대 표기 없는 매물 중 500만 원 미만은 1세대 (1세대 약 250만~485만, 2세대 약 550만~690만, 3세대 약 650만 원)
    "leica:lens:summicron-m:28:asph:unspecified": ("leica:lens:summicron-m:28:asph:v1", 5_000_000, re.compile(r"(?!)")),
    # CL: 필름(1973) 표기 없는 매물 중 170만 원 미만은 필름 CL (필름 약 60만~145만, 디지털 2017 약 190만~300만 원).
    # 디지털 표기(TL 렌즈·킷·19301 번호 등)가 있으면 가격 무시. 가격이 없으면('문의요망') 디지털 그대로
    "leica:body:cl-digital:standard": ("leica:body:cl-film", 1_700_000,
                                       re.compile(r"\bTL\b|-TL\b|1930\d|kit|킷|digital|디지털|2017|18-5[06]|sigma|urban", re.I)),
}

# 오리지널·복각처럼 가격대가 뚜렷이 갈리는 쌍: 제목에 어느 쪽 근거도 없으면(또는 둘 다 있으면) 가격으로 정한다 (2026-10-30).
# 가격대는 제목 근거가 확실한 매물로만 잡고, 한쪽 가격대 안이면서 다른 쪽 중앙값과 2배 이상 차이 날 때만 옮긴다.
# (오리지널 쪽, 복각 쪽, 오리지널 근거, 복각 근거)
PRICE_PAIRS = [
    ("leica:lens:summilux-m:35:v1-steel-rim", "leica:lens:summilux-m:35:steel-rim-reissue",
     re.compile(r"\bM3\b|1186[89]|11870|goggle|고글|안경|\beyes?\b|original|오리지널|\b1st\b|first|196\d", re.I),
     re.compile(r"11301|re-?issue|복각|리이슈|2022", re.I)),
    # 주미룩스 35 '1st·V1'만 쓴 구형: 국내는 스틸림, 일본 Ver.1은 그 뒤 구형 → 스틸림 가격대면 스틸림으로 (2026-11-02)
    ("leica:lens:summilux-m:35:v1-steel-rim", "leica:lens:summilux-m:35:pre-asph-unspecified",
     re.compile(r"steel ?rim|스틸 ?림", re.I),
     re.compile(r"^(?!.*(steel ?rim|스틸 ?림|\b1st\b|\b1th\b|\bv\.? ?1\b|ver\.? ?1\b|1세대|first|第1世代)).*$", re.I)),
    ("leica:lens:noctilux:50:f1.2-original", "leica:lens:noctilux-m:50:f1.2-asph",
     re.compile(r"11820|original|오리지널|1세대|\b1st\b|double ?aspherical|\bAA\b", re.I),
     re.compile(r"\bASPH\b|11686|11731|복각|re-?issue", re.I)),
]
PAIR_MIN_SURE = 3  # 쌍마다 제목 근거가 확실한 매물이 이만큼은 있어야 가격대를 믿음
PAIR_GAP = 2.0     # 다른 쪽 중앙값과 이 배수 이상 떨어져야 옮김
TOO_CHEAP = 0.1    # 모델 B급 시세의 10분의 1도 안 되면 부품·액세서리 의심 → 시세 계산에서 뺌
TOO_CHEAP_MIN_N = 5

# ── 바디 이름은 제목에서 렌즈 표기보다 앞에 있어야 바디 (2026-10-30, 분류 오류 케이스) ──
# 케이스 1 조리개·초점거리 안의 숫자: "Summaron M3.5/3.5" → M3, "75-200 Vario-Elmarit-R 3 Cam" → R3
# 케이스 2 렌즈 세대 표기: "9cm f4 Elmar (Type II)" → 라이카 II
# 케이스 3 '…용' 렌즈·액세서리: "Summaron-M 35mm f2.8 for Leica M3", "Telyt-R 400mm/F6.8 Leicaflex", "Data Back for R-E, R3"
# → 렌즈 표기가 바디 이름보다 먼저 나오는 제목은 바디로 보지 않고, 'for' 뒤는 바디 규칙에서 뺀다.
#   바디 이름이 먼저 나오면 제목 전체를 본다 (렌즈 뒤에 적힌 기념판 이름 'Millennium' 등을 놓치지 않게). 세트 표기가 있으면 언제나 전체.
LENS_SIGNAL = re.compile(
    r"summi|elmar|nocti|hektor|telyt|angulon|summar|xenon|thambar"
    r"|(?<![.\d])\b\d{2,3}(?:-\d{2,3})?\s?mm\b(?!\s+(?:film|slr|rangefinder|camera|kamera|format|フィルム))|(?<![.\d])\b\d{1,2}(?:\.\d)?\s?cm\b|\bf/?\s?\d(?:\.\d)?\b"
    r"|\b\d(?:\.\d)?\s?/\s?\d{2,3}\b|\b\d{2,3}\s?/\s?\d(?:\.\d)?\b|\b\d\s?-?cams?\b|\bE\s?\d{2}\b"
    r"|\b\d{2,3}\s+lens(?:es)?\b", re.I)  # 'M9-P Set … 35 Lens'처럼 mm가 빠진 세트
BODY_WORD = re.compile(r"\b(?:M|R|CL|SL|S|Q|X|T)\s?-?\d|\bI{1,3}[a-g]?\b|leicaflex|standard|\bbody\b|바디", re.I)
FOR_WORD = re.compile(r"\b(?:for|für|fuer|pour|per|para|voor|fits?)\b|用|対応|専用", re.I)
SET_MARK = re.compile(r"\+|\bset\b|\bkit\b|outfit|\bwith\b|\bw/|&|세트|セット|付|\bmit\b|\bcon\b|\bavec\b", re.I)
# 렌즈 일체형 바디(Q·X·D-Lux·미니룩스·CM 등)는 렌즈 표기가 바디 이름의 일부라 제목 전체를 봄. 라이카 I(Model A)도 렌즈 고정
FIXED_LENS_BODY = re.compile(r"^leica:body:(?:q|q-p|q2|q2-monochrom|q3|q3-43|q3-monochrom|x1|x2|x113|x-[a-z]+|d-lux[\w-]*|c-lux[\w-]*|v-lux|"
                             r"digilux(?:-[12]|-zoom|-4-3|-unspecified)?|minilux[\w-]*|mini|cm[\w-]*|c-series|c2-zoom|z2x|sofort[\w-]*|af-c1|i)(?::|$)")


# 'converted to IIIf'(공장 개조로 사양이 바뀜)는 그대로 두고, 다른 바디 부품을 단 'modified with …'만 (2026-11-05)
MODIFIED_WITH = re.compile(r"\bmodified\s+with\b|\bavec\s+t[ée]l[ée]m[èe]tre\b", re.I)


def body_view(title: str) -> str:
    """바디 규칙이 볼 제목. 세트 표기가 있으면 전체, 아니면 'for' 앞부분, 그중 렌즈 표기가 바디 이름보다 먼저면 그 앞까지."""
    mod = MODIFIED_WITH.search(title)
    if mod and BODY_WORD.search(title[:mod.start()]):
        title = title[:mod.start()]  # 'M1 modified with télémètre de M6' — 개조에 쓴 다른 바디 부품은 모델이 아님 (2026-11-05)
    if SET_MARK.search(title):
        return title
    cut = FOR_WORD.search(title)
    text = title[:cut.start()] if cut else title
    lens_at = LENS_SIGNAL.search(text)
    if lens_at and not BODY_WORD.search(text[:lens_at.start()]):
        return text[:lens_at.start()]
    return text


# 렌즈 모델에만 연결됐어도 제목에 바디 이름과 세트 표기가 같이 있으면 세트 ('M6+M 50/1.4 Summilux', 'A型 Black (Elmar 50mm付)')
SET_BODY = re.compile(r"\bM(?:2|3|4|5|6|7|8|9|10|11|P|-?A|-?D|-?E|D|E)(?:-P|-R| ?TTL)?\b(?![./]\d)"
                      r"|(?<!version )(?<!type )(?<!ver\.)(?<!ver )(?<!mark )(?<!typ )(?<!visoflex )\bI{1,3}[a-g]?(?:-K)?\b|\b[ABC]型|\bCL\b|\bR[3-9]\b|"
                      r"leicaflex|ライカフレックス|\bbody\b|ボディ|ボデー|바디", re.I)


GOGGLES = re.compile(r"goggle|\beyes?\b|眼鏡|メガネ|고글|안경", re.I)


def is_set(record: dict[str, Any], catalog: dict[str, Any] | None = None) -> bool:
    """렌즈 교환식 바디에 연결됐는데 제목에 렌즈 표기도 있는 매물 = 바디·렌즈 세트.
    렌즈 모델에만 연결됐어도 제목에 세트 표기(+·付·with·outfit…)와 바디 이름이 같이 있으면 세트."""
    catalog = catalog or load_catalog()
    title = record_title(record)
    ids = record.get("entity_ids") or []
    leaf = lambda e: not catalog["entities"][e].get("children") and not catalog["entities"][e].get("feature")  # noqa: E731
    bodies = [e for e in ids if catalog["entities"][e].get("kind") == "Body" and leaf(e) and not FIXED_LENS_BODY.match(e)]
    if bodies:
        return bool(LENS_SIGNAL.search(title))
    lenses = [e for e in ids if catalog["entities"][e].get("kind") == "Lens" and leaf(e)]
    if not lenses or not SET_MARK.search(title) or FOR_WORD.search(title) or GOGGLES.search(title):
        return False  # 'with goggles M3'·'M3 Steel Rim With Goggles'는 M3용 안경 달린 렌즈
    return bool(SET_BODY.search(title))


# 제목에 렌즈 표기가 있으면 바디가 아님 (예: 50/2, 35mm, f1.4)
LENS_IN_TITLE = re.compile(r"(\d{2,3}\s?mm\b|\b\d{2,3}/\d(\.\d)?\b|\bf/?\s?\d\.\d)", re.I)
# 제목 앞쪽에 적힌 마운트 (예: "[중고] M 135/3.4", "Leica SL 50mm")
TITLE_MOUNT = re.compile(r"^(?:\[[^\]]+\]\s*|신품\s+|중고\s+)*(?:leica\s+)?(M|SL|R|L|TL|S)\s*(?:apo\s+)?\d", re.I)
# 한국 매장식 제목("[중고] M 50/2 Rigid")은 계열 이름을 생략함 → 초점거리/조리개로 라이카 계열 추론
SHOP_LENS = re.compile(r"^(?:\[[^\]]+\]\s*|신품\s+|중고\s+)*(?:leica\s+)?(M|L|R|SL|TL)\s*(?:apo\s+)?(\d{2,3}(?:-\d{2,3})?)\s*(?:/\s*(\d+(?:\.\d+)?))?", re.I)
IMPLIED_FAMILY = {("21", "1.4"): "Summilux", ("24", "1.4"): "Summilux", ("28", "1.4"): "Summilux", ("35", "1.4"): "Summilux",
                  ("50", "1.4"): "Summilux", ("75", "1.4"): "Summilux", ("90", "1.5"): "Summilux", ("28", "2"): "Summicron",
                  ("35", "2"): "Summicron", ("50", "2"): "Summicron", ("75", "2"): "APO Summicron", ("90", "2"): "Summicron",
                  ("21", "2.8"): "Elmarit", ("24", "2.8"): "Elmarit", ("28", "2.8"): "Elmarit", ("90", "2.8"): "Elmarit",
                  ("135", "2.8"): "Elmarit", ("28", "5.6"): "Summaron", ("35", "2.8"): "Summaron", ("50", "2.8"): "Elmar",
                  ("35", "2.5"): "Summarit", ("50", "2.5"): "Summarit", ("75", "2.5"): "Summarit", ("90", "2.5"): "Summarit",
                  ("35", "2.4"): "Summarit", ("50", "2.4"): "Summarit", ("75", "2.4"): "Summarit", ("90", "2.4"): "Summarit",
                  ("18", "3.8"): "Super-Elmar", ("24", "3.8"): "Elmar", ("135", "3.4"): "APO-Telyt", ("135", "4"): "Tele-Elmar",
                  ("50", "1.2"): "Noctilux", ("50", "0.95"): "Noctilux", ("50", "1"): "Noctilux", ("75", "1.25"): "Noctilux", ("35", "1.2"): "Noctilux"}
# R·SL·TL 매장식 제목
IMPLIED_BY_MOUNT = {"R": {("19", "2.8"): "Elmarit", ("24", "2.8"): "Elmarit", ("28", "2.8"): "Elmarit", ("35", "2.8"): "Elmarit",
                          ("35", "2"): "Summicron", ("50", "2"): "Summicron", ("90", "2"): "Summicron", ("35", "1.4"): "Summilux",
                          ("50", "1.4"): "Summilux", ("80", "1.4"): "Summilux", ("90", "2.8"): "Elmarit", ("135", "2.8"): "Elmarit",
                          ("180", "2.8"): "Elmarit", ("100", "2.8"): "APO Macro Elmarit", ("60", "2.8"): "Macro Elmarit"},
                    "SL": {("50", "1.4"): "Summilux", ("21", "2"): "APO Summicron", ("28", "2"): "APO Summicron", ("35", "2"): "APO Summicron",
                           ("50", "2"): "APO Summicron", ("75", "2"): "APO Summicron", ("90", "2"): "APO Summicron"},
                    "TL": {("35", "1.4"): "Summilux", ("23", "2"): "Summicron", ("18", "2.8"): "Elmarit", ("60", "2.8"): "APO Macro Elmarit"}}
ZOOM_FAMILY = {"R": "Vario Elmar", "SL": "Vario Elmarit", "TL": "Vario Elmar"}
FAMILY_WORD = re.compile(r"summi|elmar|nocti|hektor|telyt|angulon|summar|xenon|thambar|lux\b|cron\b|ultron|nokton|heliar|skopar|planar|biogon|sonnar", re.I)
# 모델명에 붙은 마운트 (예: Noctilux-M, Summicron-R, APO-Summicron-SL)
NAME_MOUNT = re.compile(r"[a-z]-(M|SL|R|TL|T)\b", re.I)  # -T = 2016 전 TL 이름 (Summicron-T 23)


@lru_cache(maxsize=1)
def krw_rates() -> dict[str, float]:
    """통화 → 원화 환율 (data/fx_rates.json, 없으면 대략값)."""
    try:
        rates = json.loads(FX_PATH.read_text(encoding="utf-8"))["rates"]
        krw = rates["KRW"]
        return {code: krw / value for code, value in rates.items()}
    except Exception:
        return {"KRW": 1, "JPY": 9, "USD": 1350, "GBP": 1780, "EUR": 1500}


def price_krw(final: dict) -> float | None:
    price = final.get("parsed_price_numeric")
    rate = krw_rates().get(str(final.get("currency") or "KRW").upper())
    return price * rate if price and rate else None


@lru_cache(maxsize=1)
def load_catalog(path: str | None = None) -> dict[str, Any]:
    data = json.loads(Path(path or CATALOG_PATH).read_text(encoding="utf-8"))
    entities = {entity["id"]: entity for entity in data["entities"]}
    compiled = {}
    for entity in entities.values():
        rule = entity.get("match")
        if rule:
            compiled[entity["id"]] = (
                rule,
                [re.compile(p, re.I) for p in rule["title_must"]],
                [re.compile(p, re.I) for p in rule["title_must_not"]],
            )
    codes: dict[str, list[str]] = {}  # 번호 → 엔티티들 (라이카가 옛 번호를 다른 제품에 다시 쓴 경우 둘 이상)
    for entity in entities.values():
        for number in entity.get("codes") or []:
            codes.setdefault(number, []).append(entity["id"])
    features = [(entity["id"], set(entity["feature"]["members"]), [re.compile(p, re.I) for p in entity["feature"]["exclude"]])
                for entity in entities.values() if entity.get("feature")]
    return {"entities": entities, "compiled": compiled, "codes": codes, "features": features}


def record_title(record: dict[str, Any]) -> str:
    final = record.get("final_output") or {}
    raw = record.get("raw_item") or {}
    title = str(final.get("title_raw") or raw.get("상품명") or record.get("title") or final.get("title") or "")
    # 로마 숫자 특수문자 (Ⅲ → III)
    title = title.replace("Ⅲ", "III").replace("Ⅱ", "II").replace("Ⅰ", "I").replace("Ⅳ", "IV")
    # 옛 렌즈의 cm 표기 (영국 딜러 '9cm f4 Elmar'·'13.5cm Hektor') → mm로 바꿔 초점거리 규칙에 걸리게.
    # 제품 번호·코드 이름이 적힌 제목은 그대로 둔다 (번호로 세대가 정해지고, 'FIKUS … 13.5cm' 같은 후드·부품이 렌즈로 가지 않게)
    if not (CODE_IN_TITLE.search(title) or CODE_WORD_IN_TITLE.search(title)):
        title = re.sub(r"(?<![\d.])(\d{1,2}(?:\.\d)?)\s?cm\b", lambda m: f"{round(float(m.group(1)) * 10):d}mm", title)
    shop = SHOP_LENS.match(title)
    if shop and not FAMILY_WORD.search(title):
        mount, focal, aperture = shop.group(1).upper(), shop.group(2), shop.group(3) or ""
        if "." in aperture:
            aperture = aperture.rstrip("0").rstrip(".")
        if "-" in focal:
            family = ZOOM_FAMILY.get(mount)
        elif mount in ("M", "L"):
            family = IMPLIED_FAMILY.get((focal, aperture))
        else:
            family = IMPLIED_BY_MOUNT.get(mount, {}).get((focal, aperture))
            if not family and mount == "SL" and re.search(r"\bapo\b", title, re.I):
                family = "Summicron"
        if family:
            title = f"{title} {family}"
    return title


def _category_ok(rule: dict, final: dict, title: str) -> bool:
    category = final.get("category")
    if rule["category"] == "Body":
        if category == "Body":
            return True
        # 한국 매장 바디가 Lens로 잘못 분류된 경우: 제목에 렌즈 표기가 없으면 바디로 본다
        return category == "Lens" and not LENS_IN_TITLE.search(title)
    if rule["category"] == "Lens" and category == "Body":
        # 한국 매장 렌즈가 Body로 잘못 분류된 경우 (예: "[중고]Leica M50/1.2 1세대 Noctilux"): 매장식 렌즈 표기면 렌즈로 본다
        shop = SHOP_LENS.match(title)
        return bool(shop and shop.group(3))
    return category == rule["category"]


def _mount_ok(rule: dict, final: dict, title: str) -> bool:
    want = rule.get("mount")
    if not want or rule.get("category") == "Body":
        return True  # 바디는 모델 이름이 마운트를 정함 (분류 데이터의 마운트는 믿지 않음)
    explicit = TITLE_MOUNT.match(title) or NAME_MOUNT.search(title)
    if explicit:
        return {"T": "TL"}.get(explicit.group(1).upper(), explicit.group(1).upper()) == want
    got = final.get("mount")
    return got in (want, None, "", "Unknown")


# 제목 속 라이카 제품 번호 (예: "Leica 50mm F2 M Black 6bit - 11826"). 앞뒤가 숫자·소수점이면 번호가 아님
CODE_IN_TITLE = re.compile(r"(?<![\d.,/-])(1[01]\d{3}|19\d{3}|20\d{3})(?![\d.,%])")
# 제목 속 라이츠 코드 이름 (예: "Leica 35mm f2 Summicron (Silver, SAWOM / 11308)"). 대문자로 적힌 것만
CODE_WORD_IN_TITLE = re.compile(r"\b[A-Z]{5}(?:-[A-Z]{1,2})?\b")


# 번호가 적혀 있어도 본품이 아닌 매물 (후드·캡·케이스·필터·어댑터, "for 11879" 같은 호환품, 타사)
NOT_THE_ITEM = re.compile(r"\bhood|후드|フード|\bcap\b|캡|case|케이스|strap|스트랩|filter|필터|フィルター|adapter|어댑터|"
                          r"\bfor\b|用|호환|\bcopy\b|카피|voigtl|zeiss|ttartisan|7 ?artisans|light ?lens ?lab|\bLLL\b|leeworks|box only|박스만", re.I)


def _code_hits(title: str, final: dict, catalog: dict) -> list[str]:
    """모델명 규칙에 안 걸린 매물: 제목에 적힌 제품 번호로 연결."""
    if NOT_THE_ITEM.search(title):
        return []
    hits: list[str] = []
    found = CODE_IN_TITLE.findall(title) + [w.lower().replace("-", " ") for w in CODE_WORD_IN_TITLE.findall(title)]
    for number in found:
        owners = catalog.get("codes", {}).get(number) or []
        if len(owners) != 1 or owners[0] in hits:
            continue  # 모르는 번호, 또는 여러 제품에 쓰인 번호는 제목만으로 정하지 않음
        entity_id = owners[0]
        kind = catalog["entities"][entity_id].get("kind")
        category = final.get("category")
        if category not in (kind, None, "", "Unknown") and not (kind == "Body" and category == "Lens" and not LENS_IN_TITLE.search(title)):
            continue
        hits.append(entity_id)
    return hits


# 다른 물건에 끼우는 부속품 ("aperture setting ring for 50mm f2.8 Elmar", "focusing mount for 135mm f4 Elmar", "Elmar-M 50mm f2.8용")
# → 렌즈·바디 시세에 섞이지 않게 어느 모델에도 연결하지 않음 (영국 딜러 화면에서 £23·£29 부속품이 렌즈 최저가로 보임, 2026-10-27)
ACCESSORY_FOR = re.compile(
    r"\b(rings?|mounts?|hoods?|shades?|caps?|adapters?|finders?|viewfinders?|filters?|cases?|collars?|bayonets?|tubes?|spools?|releases?|cranks?)\s+for\s+(?:the\s+|a\s+)?"
    r"(?:\d|[a-z-]*(?:elmar|summ|noct|lux|cron|angulon|telyt|hektor|leica|leitz|barnack))"
    r"|(?:mm|f ?/?\d(?:\.\d+)?)\s*용(?![가-힣])"
    # 2026-11-02 섞임 점검: 상자만·설명서·접사 장치·포커싱 마운트·조리개 링·삼각대·후드(프랑스어)는 어느 모델에도 안 붙임
    r"|^(?:leica\s+|leitz\s+)?(?:box\b|focus(?:ing)?\s+mount\b)|\bbox\s+rossa\b|\binstructions?\b|\bbedienungsanleitung\b|\bmode d'emploi\b"
    r"|close[- ]?(?:focus|up)\s+device|\bSOOKY\b|\bADVOO|ghiera|diaframma|treppiede|parasoleil", re.I)


# classifier_v2._BUNDLE_SPLIT과 같은 묶음말 (검색 쪽은 분류기를 불러오지 않으므로 따로 둠)
BUNDLE_LENS_NAME = re.compile(r"summ|elmar|noctilux|hektor|telyt|angulon|rokkor|thambar|\bapo\b", re.I)
BUNDLE_ACC_TAIL = re.compile(r"hood|shade|filter|adapter|adattat|finder|sucher|case|cap\b|tappo|tube|visoflex|ring|grip|"
                             r"후드|필터|フード|フィルター|occhialini|glasses|follow focus", re.I)
BUNDLE_SPLIT = re.compile(r"\s(?:\+|&(?!\s*\d)|with|w/|mit|und|avec|con|plus)\s|\s?\+\s?(?=[a-z])|付き?|付属", re.I)


def match_entities(record: dict[str, Any], catalog: dict[str, Any] | None = None) -> list[str]:
    """매물이 해당하는 엔티티 ID들 (자식 + 그 부모)."""
    catalog = catalog or load_catalog()
    final = record.get("final_output") or {}
    title = record_title(record)
    if ACCESSORY_FOR.search(title):
        return []
    hits = _rule_hits(catalog, final, title)
    lens_at = LENS_SIGNAL.search(title)
    if not hits and final.get("category") == "Body" and lens_at and not BODY_WORD.search(title[:lens_at.start()]):
        # 바디로 분류됐지만 렌즈 표기가 먼저 나오고 바디 이름은 그 뒤에만 있는 매물(케이스 3)은 렌즈로 다시 본다
        hits = _rule_hits(catalog, {**final, "category": "Lens"}, title)
    if not hits:
        hits = _code_hits(title, final, catalog)
    if not hits and final.get("category") in ("Lens", "Body"):
        # 본품 + 구성품 ('Summicron-M ASPH. (11879) + Lens Hood (12526)'·'M10 with Extra Battery'): 뒤의 후드·배터리 말 때문에
        # 모델 규칙(must_not)·번호 연결(NOT_THE_ITEM)이 막히므로 묶음말 앞부분으로 다시 본다 (2026-11-14, 분류는 classifier_v2 bundle_head)
        split = BUNDLE_SPLIT.search(title)
        tail = title[split.end():] if split else ""
        # 뒤가 렌즈면 바디+렌즈 세트 ('R4 + Summilux-R 50mm'·'CL with 18-56mm') — 한쪽 모델에만 붙이면 시세가 오르므로 붙이지 않음.
        # 후드·필터 설명의 초점거리('+ Lens Hood (35mm f1.4-2)')는 렌즈가 아님
        lens_tail = (LENS_IN_TITLE.search(tail) or BUNDLE_LENS_NAME.search(tail)) and not BUNDLE_ACC_TAIL.search(tail)
        if split and split.start() >= 6 and not lens_tail:
            head = title[:split.start()]
            hits = _rule_hits(catalog, final, head) or _code_hits(head, final, catalog)
    for i, hit in enumerate(hits):
        if hit in PRICE_SPLIT:
            cheaper, limit, marked = PRICE_SPLIT[hit]
            krw = price_krw(final)
            if krw and krw < limit and not marked.search(title):
                hits[i] = cheaper
    return _with_parents(list(dict.fromkeys(hits)), catalog, title)


BUILT_IN_HOOD = re.compile(r"built[- ]?in[- ]?hood", re.I)


def _rule_hits(catalog: dict[str, Any], final: dict, title: str) -> list[str]:
    hits: list[str] = []
    body_title = body_view(title)
    for entity_id, (rule, must, must_not) in catalog["compiled"].items():
        if not _category_ok(rule, final, title) or not _mount_ok(rule, final, title):
            continue
        text = body_title if rule["category"] == "Body" and not FIXED_LENS_BODY.match(entity_id) else title
        # 'Built-in-hood'(후드 붙은 렌즈 버전)은 부속품 후드가 아님 → '빼는 말'(hood) 검사에서만 다른 말로 (2026-11-15 Fotopia Summicron-M 90 v1)
        text_nn = BUILT_IN_HOOD.sub("builtin-shade", text)
        if all(p.search(text) for p in must) and not any(p.search(text_nn) for p in must_not):
            hits.append(entity_id)
    return hits


def _with_parents(hits: list[str], catalog: dict[str, Any], title: str) -> list[str]:
    """자식 엔티티들에 부모(부모의 부모까지)와 사양 묶음을 붙인다."""
    parents: set[str] = set()
    frontier = {catalog["entities"][h].get("parent") for h in hits} - {None}
    while frontier:  # 부모의 부모까지 (예: D-Lux 7 BAPE → D-Lux 7 → D-Lux 전체)
        parents |= frontier
        frontier = {catalog["entities"][p].get("parent") for p in frontier} - {None} - parents
    linked = set(hits) | parents
    # 사양 묶음 (예: 28mm 프레임라인 있는 M 바디): 그 바디 매물이면 묶음에도 넣는다
    features = [fid for fid, members, exclude in catalog.get("features", [])
                if linked & members and not any(p.search(title) for p in exclude)]
    return hits + sorted(parents) + features


# ── 같은 물건의 여러 기록 (2026-11-02): 장씨카메라는 같은 물건(같은 번호 sn.)을 제목만 바꿔 여러 번 올림
# ('MP Black Paint sn.2890' · 'MP sn.2890'). 간단한 제목은 기본형·세대 미표기로 가서 모델이 갈라지고 매물 수가 부풂.
# 같은 매장·같은 번호·같은 계열이면 한 물건: 가장 자세한 제목의 모델로 맞추고, 하나만 남기고 나머지는 entity_note='duplicate'.
# 번호는 다른 상품에도 다시 쓰여서(sn.2061 = 주미룩스 35·엘마리트 28) 계열이 같을 때만, 자세한 모델이 둘 이상이면 건드리지 않음.
SAME_ITEM_NO = re.compile(r"\bsn\.?\s*(\d{3,6})\b", re.I)
GENERIC_LEAF = re.compile(r":(standard|unspecified|current|classic|pre-asph-unspecified|asph-unspecified)$|-unspecified$")


def _generic_leaf(entity_id: str, ents: dict[str, Any]) -> bool:
    """기본형·세대 미표기처럼 '더 자세한 표기가 없을 때' 가는 모델"""
    name = str((ents.get(entity_id) or {}).get("name_ko") or "")
    return bool(GENERIC_LEAF.search(entity_id)) or any(w in name for w in ("미표기", "표기 없음", "기본형", "(블랙)"))


def _family(entity_id: str, catalog: dict[str, Any]) -> str:
    entity = catalog["entities"].get(entity_id) or {}
    return entity.get("parent") or entity_id


def merge_same_item(records: list[dict[str, Any]], catalog: dict[str, Any] | None = None) -> int:
    """같은 물건 기록을 묶어 모델을 맞추고 중복 표시. 중복으로 표시한 수를 돌려준다."""
    catalog = catalog or load_catalog()
    ents = catalog["entities"]
    groups: dict[tuple, list[tuple[dict, str]]] = {}
    for record in records:
        final = record.get("final_output") or {}
        m = SAME_ITEM_NO.search(str(final.get("title_raw") or ""))
        if not m:
            continue
        leaves = [i for i in record.get("entity_ids") or [] if i in ents and not ents[i].get("children") and not ents[i].get("feature")]
        if len(leaves) != 1:
            continue
        groups.setdefault((final.get("source"), m.group(1), _family(leaves[0], catalog)), []).append((record, leaves[0]))
    marked = 0
    for members in groups.values():
        if len(members) < 2:
            continue
        specific = {leaf for _, leaf in members if not _generic_leaf(leaf, ents)}
        if len(specific) > 1:
            continue  # 자세한 모델끼리 다름 → 다른 물건일 수 있어 그대로
        if specific:
            target = specific.pop()
            for record, leaf in members:
                if leaf != target:
                    title = record_title(record)
                    record["entity_ids"] = _with_parents([target], catalog, title)
        # 남길 기록: 판매 중 > 가격 있음 > 최근에 처음 본 것
        def rank(item):
            final = item[0].get("final_output") or {}
            return (final.get("sold_quality") == "asking", bool(final.get("parsed_price_numeric")), str(final.get("first_seen") or ""))
        keep = max(members, key=rank)[0]
        for record, _ in members:
            if record is not keep and not (record.get("final_output") or {}).get("entity_note"):
                record.setdefault("final_output", {})["entity_note"] = "duplicate"
                marked += 1
    return marked


NOT_A_BODY = re.compile(r"case|tasche|sonnenblende|\bhood\b|hand ?g?rip|handgrip|\bgrip\b|그립|data ?back|데이타백|데이터백|motor|winder|와인더|"
                        r"spiegelkasten|visoflex|visiflex|turret|(?<!interchangeable )\blens\b|렌즈|strap|스트랩|battery|배터리|charger|충전|케이스|후드", re.I)


def fix_body_category(record: dict[str, Any]) -> bool:
    """연결된 모델이 모두 바디인데 분류가 렌즈면 바디로 바로잡는다.
    라이카 전문점은 제목에 브랜드를 안 써서('[위탁] SL3', '[중고] M11 (Silver)' — 라이카스토어 충무로) 분류기가 기본값 렌즈로 둠
    (2026-11-12 밤: 충무로 바디 수백 개가 렌즈 → 가격순·검색 의도에서 '비슷한 매물'로 밀림). 렌즈·세트가 섞이면 그대로."""
    final = record.get("final_output") or {}
    leaves = [i for i in record.get("entity_ids") or [] if ":feature:" not in i]
    if NOT_A_BODY.search(record_title(record)):
        return False  # 바디 이름이 들어간 부속품 (X1 케이스, M240 핸드그립, R 모터 드라이브 등)
    if final.get("category") == "Lens" and leaves and all(i.startswith("leica:body:") for i in leaves):
        final["category"] = "Body"
        return True
    return False


def annotate_records(records: Iterable[dict[str, Any]]) -> None:
    catalog = load_catalog()
    for record in records:
        record["entity_ids"] = match_entities(record, catalog)
        (record.get("final_output") or {}).pop("entity_note", None)
        fix_body_category(record)


def infer_by_price(records: list[dict[str, Any]], value, catalog: dict[str, Any] | None = None) -> int:
    """PRICE_PAIRS의 쌍마다 제목 근거가 없는 매물을 가격대로 옮긴다. value(record) = B급 환산 원화.
    옮긴 매물은 final_output.entity_note = 'price_inferred'. 옮긴 수를 돌려준다."""
    catalog = catalog or load_catalog()
    moved = 0
    for high, low, high_mark, low_mark in PRICE_PAIRS:
        pair = []
        for record in records:
            ids = record.get("entity_ids") or []
            if high in ids or low in ids:
                title = record_title(record)
                sure_high, sure_low = bool(high_mark.search(title)), bool(low_mark.search(title))
                side = high if sure_high and not sure_low else low if sure_low and not sure_high else None
                pair.append((record, side, value(record)))
        bands = {}
        for side in (high, low):
            prices = sorted(v for _, s, v in pair if s == side and v)
            if len(prices) < PAIR_MIN_SURE:
                break
            bands[side] = (prices[0], prices[-1], prices[len(prices) // 2])
        if len(bands) < 2:
            continue
        for record, side, v in pair:
            if side or not v:
                continue  # 제목 근거가 한쪽에만 있으면 제목을 따름
            for target, other in ((high, low), (low, high)):
                lo, hi, _ = bands[target]
                gap = max(v, bands[other][2]) / min(v, bands[other][2])
                if lo <= v <= hi and gap >= PAIR_GAP:
                    ids = record["entity_ids"]
                    if other in ids:
                        title = record_title(record)
                        leaves = [i for i in ids if not catalog["entities"][i].get("children") and not catalog["entities"][i].get("feature")]
                        hits = [target if i == other else i for i in leaves]
                        record["entity_ids"] = _with_parents(list(dict.fromkeys(hits)), catalog, title)
                        record.setdefault("final_output", {})["entity_note"] = "price_inferred"
                        moved += 1
                    break
    return moved


def flag_too_cheap(records: list[dict[str, Any]], value, catalog: dict[str, Any] | None = None) -> set[int]:
    """모델 B급 시세(그 모델 매물 중앙값)의 TOO_CHEAP배도 안 되는 매물 → final_output.entity_note = 'too_cheap'.
    설명서·부품·대여처럼 모델로 잘못 연결된 매물을 시세 계산에서 빼기 위함. 표시한 매물의 id()를 돌려준다."""
    catalog = catalog or load_catalog()
    entities = catalog["entities"]
    by_entity: dict[str, list[float]] = {}
    for record in records:
        v = value(record)
        for eid in record.get("entity_ids") or []:
            if v and not entities[eid].get("children") and not entities[eid].get("feature"):
                by_entity.setdefault(eid, []).append(v)
    medians = {eid: sorted(vs)[len(vs) // 2] for eid, vs in by_entity.items() if len(vs) >= TOO_CHEAP_MIN_N}
    flagged = set()
    for record in records:
        v = value(record)
        if v and any(v < TOO_CHEAP * medians[e] for e in record.get("entity_ids") or [] if e in medians):
            record.setdefault("final_output", {})["entity_note"] = "too_cheap"
            flagged.add(id(record))
    return flagged


# ── 검색창 후보 (beta.html의 suggestEntities와 같은 규칙) ──
STOP_TOKENS = {"leica", "라이카", "ライカ", "徕卡", "徠卡", "lens", "렌즈", "body", "바디",
               "0.58", "0.72", "0.85", "0.68", "black", "silver", "chrome", "블랙", "실버", "크롬",
               "used", "중고", "신품", "new", "paint", "블랙페인트", "mandler"}  # mandler: 설계자 이름 (화면 ENTITY_STOP_TOKENS와 같게)
APERTURE = re.compile(r"^f?\d+(\.\d+)?$")


def normalize_text(text: str) -> str:
    text = str(text or "").lower()
    text = re.sub(r"엠(?=\d)", "m", text)
    text = re.sub(r"큐(?=\d)", "q", text)
    text = re.sub(r"[‐‑–—\-_/·・,()\[\]'\"“”‘’]+", " ", text)
    text = re.sub(r"(\d)\s?mm\b", r"\1", text)
    text = re.sub(r"(\d)([a-z]{3,})\b", r"\1 \2", text)  # 붙여 쓴 '50lux'·'35cron' → '50 lux' (안 그러면 '35lux'로 잘못 고쳐 읽음)
    text = re.sub(r"\b0(\d\d)\b", r"0.\1", text)
    return re.sub(r"\s+", " ", text).strip()


def _edit_distance(a: str, b: str, cap: int = 3) -> int:
    if abs(len(a) - len(b)) > cap:
        return cap
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        for j, cb in enumerate(b, 1):
            cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (ca != cb)))
        prev = cur
    return prev[-1]


class Suggester:
    """카탈로그 별칭으로 검색어 → 후보 엔티티."""

    def __init__(self, entities: list[dict]):
        self.entities = entities
        self.aliases = {e["id"]: [normalize_text(a) for a in e.get("aliases") or []] for e in entities}
        self.codes = {e["id"]: set(e.get("codes") or []) for e in entities}
        self.tokens = {eid: {t for a in al for t in a.split(" ") if t and t not in STOP_TOKENS} for eid, al in self.aliases.items()}
        self.vocab = set().union(*self.tokens.values()) if self.tokens else set()

    def _fix_token(self, token: str) -> str | None:
        """알려진 단어로 맞추기: 그대로/접두어/오타. 모르는 단어면 None(무시). 숫자는 절대 무시하지 않음."""
        if re.fullmatch(r"\d+", token):
            return token
        if token in self.vocab or any(v.startswith(token) for v in self.vocab):
            return token
        if len(token) >= 5:
            limit = 1 if len(token) <= 6 else 2
            best = min(self.vocab, key=lambda v: _edit_distance(token, v), default=None)
            if best and _edit_distance(token, best) <= limit:
                return best
        return None

    def _score(self, query: str, eid: str) -> float:
        if query in self.codes[eid]:
            return 1000  # 제품 번호 (예: 11873). 앞부분만 같은 번호는 후보로 내지 않음 ("100" → 10043 R4 방지)
        best = 0.0
        qc = query.replace(" ", "")
        for alias in self.aliases[eid]:
            if alias == query:
                return 1000
            if alias.startswith(query):
                best = max(best, 900 - 0.3 * (len(alias) - len(query)))
            ac = alias.replace(" ", "")
            if ac == qc:
                best = max(best, 950)
            elif ac.startswith(qc):
                best = max(best, 880 - 0.3 * (len(ac) - len(qc)))
        if best:
            return best
        raw = [t for t in query.split(" ") if t and t not in STOP_TOKENS]
        tokens = [self._fix_token(t) for t in raw]
        known = [t for t in tokens if t]
        if not known:
            return 0
        is_ap = lambda t: APERTURE.match(t) is not None and "." in t  # noqa: E731

        def token_score(etokens: set[str]) -> float | None:
            bonus = 0.0
            used = 0
            for t in known:
                if is_ap(t):
                    bare = t.lstrip("f")
                    if bare in etokens:
                        bonus += 60
                        used += 1
                        continue
                    if any(is_ap(x) for x in etokens):
                        return None  # 이 모델엔 다른 조리개가 지정돼 있음
                    continue  # 조리개가 모델을 가르지 않으면 무시
                if re.fullmatch(r"\d+", t):
                    if t not in etokens:
                        return None
                    used += 1
                elif t in etokens:
                    used += 1
                elif any(x.startswith(t) for x in etokens):
                    used += 1
                    bonus -= 2  # 앞부분만 같음
                else:
                    return None
            return bonus - 3 * max(0, len(etokens) - used)

        best_alias = None
        for alias in self.aliases[eid]:
            atoks = {t for t in alias.split(" ") if t and t not in STOP_TOKENS}
            got = token_score(atoks)
            if got is not None:
                best_alias = max(best_alias if best_alias is not None else -1e9, got)
        ignored = len(raw) - len(known)
        if best_alias is not None:
            return 760 + 10 * len(known) - 5 * ignored + best_alias
        union = token_score(self.tokens[eid])  # 여러 별칭을 합쳐서 (예: wate + 16 18 21)
        if union is None:
            return 0
        return 700 + 10 * len(known) - 5 * ignored + union + 3 * max(0, len(self.tokens[eid]) - len(known))

    def suggest(self, query: str, limit: int = 12) -> list[dict]:
        import math

        q = normalize_text(query)
        if not q:
            return []
        bare = re.sub(r"^(leica|라이카|ライカ|徕卡|徠卡)\s+", "", q)
        scored = []
        for entity in self.entities:
            score = max(self._score(q, entity["id"]), self._score(bare, entity["id"]) if bare != q else 0)
            if score >= 700:
                active = math.log10(1 + (entity.get("active_count") or 0))
                # 앞부분만 맞는 후보끼리는 판매 중 매물이 많은 모델을 먼저
                weight = 8 if 850 <= score < 950 else 2
                scored.append((score + weight * active, entity))
        scored.sort(key=lambda item: (-item[0], -(item[1].get("listing_count") or 0)))
        return group_children([entity for _, entity in scored])[:limit]


def group_children(ordered: list[dict]) -> list[dict]:
    """부모가 후보에 있으면 그 자식(세대·에디션) 후보를 부모 바로 아래, 카탈로그 순서(세대순)로 붙인다. 한 단계만."""
    by_id = {e["id"]: e for e in ordered}
    out: list[dict] = []
    seen: set[str] = set()

    def put(entity: dict) -> bool:
        if entity["id"] in seen:
            return False
        seen.add(entity["id"])
        out.append(entity)
        return True

    for entity in ordered:
        if put(entity):  # 한 단계만: 손자(세대 안의 세대)는 자기 점수 자리에
            for child in entity.get("children") or []:
                if child in by_id:
                    put(by_id[child])
    return out


def suggest(query: str, summary_entities: list[dict], limit: int = 12) -> list[dict]:
    return Suggester(summary_entities).suggest(query, limit)
