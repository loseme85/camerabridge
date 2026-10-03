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

# 제목에 렌즈 표기가 있으면 바디가 아님 (예: 50/2, 35mm, f1.4)
LENS_IN_TITLE = re.compile(r"(\d{2,3}\s?mm\b|\b\d{2,3}/\d(\.\d)?\b|\bf/?\s?\d\.\d)", re.I)
# 제목 앞쪽에 적힌 마운트 (예: "[중고] M 135/3.4", "Leica SL 50mm")
TITLE_MOUNT = re.compile(r"^(?:\[[^\]]+\]\s*|신품\s+|중고\s+)*(?:leica\s+)?(M|SL|R|L|TL|S)\s+\d", re.I)
# 모델명에 붙은 마운트 (예: Noctilux-M, Summicron-R, APO-Summicron-SL)
NAME_MOUNT = re.compile(r"[a-z]-(M|SL|R|TL)\b", re.I)


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
    return {"entities": entities, "compiled": compiled}


def record_title(record: dict[str, Any]) -> str:
    final = record.get("final_output") or {}
    raw = record.get("raw_item") or {}
    title = str(final.get("title_raw") or raw.get("상품명") or record.get("title") or final.get("title") or "")
    # 로마 숫자 특수문자 (Ⅲ → III)
    return title.replace("Ⅲ", "III").replace("Ⅱ", "II").replace("Ⅰ", "I").replace("Ⅳ", "IV")


def _category_ok(rule: dict, final: dict, title: str) -> bool:
    category = final.get("category")
    if rule["category"] == "Body":
        if category == "Body":
            return True
        # 한국 매장 바디가 Lens로 잘못 분류된 경우: 제목에 렌즈 표기가 없으면 바디로 본다
        return category == "Lens" and not LENS_IN_TITLE.search(title)
    return category == rule["category"]


def _mount_ok(rule: dict, final: dict, title: str) -> bool:
    want = rule.get("mount")
    if not want or rule.get("category") == "Body":
        return True  # 바디는 모델 이름이 마운트를 정함 (분류 데이터의 마운트는 믿지 않음)
    explicit = TITLE_MOUNT.match(title) or NAME_MOUNT.search(title)
    if explicit:
        return explicit.group(1).upper() == want
    got = final.get("mount")
    return got in (want, None, "", "Unknown")


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
    parents: set[str] = set()
    frontier = {catalog["entities"][h].get("parent") for h in hits} - {None}
    while frontier:  # 부모의 부모까지 (예: D-Lux 7 BAPE → D-Lux 7 → D-Lux 전체)
        parents |= frontier
        frontier = {catalog["entities"][p].get("parent") for p in frontier} - {None} - parents
    return hits + sorted(parents)


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
        best = 0.0
        qc = query.replace(" ", "")
        for alias in self.aliases[eid]:
            if alias == query:
                return 1000
            if alias.startswith(query):
                best = max(best, 900 - (len(alias) - len(query)))
            ac = alias.replace(" ", "")
            if ac == qc:
                best = max(best, 950)
            elif ac.startswith(qc):
                best = max(best, 850 - (len(ac) - len(qc)))
        if best:
            return best
        raw = [t for t in query.split(" ") if t and t not in STOP_TOKENS]
        tokens = [self._fix_token(t) for t in raw]
        known = [t for t in tokens if t]
        if not known:
            return 0
        etokens = self.tokens[eid]
        bonus = 0
        for t in known:
            if APERTURE.match(t) and "." in t:
                bare = t.lstrip("f")
                if bare in etokens:
                    bonus += 60  # 적은 조리개가 모델과 정확히 맞음 (예: 0.95)
                    continue
                if any(APERTURE.match(x) and "." in x for x in etokens):
                    return 0  # 이 모델엔 다른 조리개가 지정돼 있음
                continue  # 조리개가 모델을 가르지 않으면 무시
            if re.fullmatch(r"\d+", t):
                if t not in etokens:
                    return 0
            elif not any(x.startswith(t) for x in etokens):
                return 0
        ignored = len(raw) - len(known)
        return 700 + 10 * len(known) - 5 * ignored + bonus

    def suggest(self, query: str, limit: int = 8) -> list[dict]:
        import math

        q = normalize_text(query)
        if not q:
            return []
        bare = re.sub(r"^(leica|라이카|ライカ|徕卡|徠卡)\s+", "", q)
        scored = []
        for entity in self.entities:
            score = max(self._score(q, entity["id"]), self._score(bare, entity["id"]) if bare != q else 0)
            if score >= 700:
                scored.append((score + math.log10(1 + (entity.get("active_count") or 0)), entity))
        scored.sort(key=lambda item: (-(item[0] // 50), -(item[1].get("active_count") or 0), -(item[1].get("listing_count") or 0)))
        return [entity for _, entity in scored[:limit]]


def suggest(query: str, summary_entities: list[dict], limit: int = 8) -> list[dict]:
    return Suggester(summary_entities).suggest(query, limit)
