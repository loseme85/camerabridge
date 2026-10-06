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
}

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


def match_entities(record: dict[str, Any], catalog: dict[str, Any] | None = None) -> list[str]:
    """매물이 해당하는 엔티티 ID들 (자식 + 그 부모)."""
    catalog = catalog or load_catalog()
    final = record.get("final_output") or {}
    title = record_title(record)
    hits: list[str] = []
    for entity_id, (rule, must, must_not) in catalog["compiled"].items():
        if not _category_ok(rule, final, title) or not _mount_ok(rule, final, title):
            continue
        if all(p.search(title) for p in must) and not any(p.search(title) for p in must_not):
            hits.append(entity_id)
    if not hits:
        hits = _code_hits(title, final, catalog)
    for i, hit in enumerate(hits):
        if hit in PRICE_SPLIT:
            cheaper, limit, marked = PRICE_SPLIT[hit]
            krw = price_krw(final)
            if krw and krw < limit and not marked.search(title):
                hits[i] = cheaper
    hits = list(dict.fromkeys(hits))
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


def annotate_records(records: Iterable[dict[str, Any]]) -> None:
    catalog = load_catalog()
    for record in records:
        record["entity_ids"] = match_entities(record, catalog)


# ── 검색창 후보 (beta.html의 suggestEntities와 같은 규칙) ──
STOP_TOKENS = {"leica", "라이카", "ライカ", "徕卡", "徠卡", "lens", "렌즈", "body", "바디",
               "0.58", "0.72", "0.85", "0.68", "black", "silver", "chrome", "블랙", "실버", "크롬",
               "used", "중고", "신품", "new", "paint", "블랙페인트"}
APERTURE = re.compile(r"^f?\d+(\.\d+)?$")


def normalize_text(text: str) -> str:
    text = str(text or "").lower()
    text = re.sub(r"엠(?=\d)", "m", text)
    text = re.sub(r"큐(?=\d)", "q", text)
    text = re.sub(r"[‐‑–—\-_/·・,()\[\]'\"“”‘’]+", " ", text)
    text = re.sub(r"(\d)\s?mm\b", r"\1", text)
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
