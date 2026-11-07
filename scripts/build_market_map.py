"""첫 화면 '지금 팔리는 라이카 전부' 점 지도 데이터: data/derived/market_map.json

판매 중이고 모델이 연결된 매물을 점 하나씩 (2026-11-07 사장님: 메인 화면에 전체 매물 그래프).
같은 물건 중복·너무 싼 것(잘못 연결 의심)·세트·대여는 뺀다 (모델 페이지와 같은 기준).

줄(row): 0 M 바디 · 1 그 밖의 바디 · 2 M 렌즈 · 3 그 밖의 렌즈
지역(region): 0 한국 · 1 일본 · 2 유럽 · 3 미국·캐나다 · 4 그 밖 (매장 나라는 data/config/landed_cost_rules.json)
점 하나 = [원화 가격(천 원 단위로 반올림), 줄, 지역, 모델 번호] — 모델 이름은 entities 배열에서 번호로 찾음.
크롤마다 다시 만든다 (build_entity_index.py 다음).
"""
from __future__ import annotations

import datetime as dt
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INDEX = ROOT / "data" / "derived" / "results_search_index_v1.json"
SUMMARY = ROOT / "data" / "derived" / "entity_summary_v1.json"
RULES = ROOT / "data" / "config" / "landed_cost_rules.json"
OUT = ROOT / "data" / "derived" / "market_map.json"
sys.path.insert(0, str(ROOT))
from entity_catalog import krw_rates  # noqa: E402  (모델 페이지와 같은 환율)

RENTAL = re.compile(r"\brental\b|\bfor rent\b|대여|렌탈|レンタル", re.I)
EUROPE = {"GB", "DE", "FR", "IT", "NL", "BE", "LU", "AT", "CH", "ES", "PT", "DK", "SE", "NO", "FI", "PL", "CZ", "GR", "IE", "HU"}


def region_of(country: str | None) -> int:
    if country == "KR":
        return 0
    if country == "JP":
        return 1
    if country in EUROPE:
        return 2
    if country in ("US", "CA"):
        return 3
    return 4


def main() -> None:
    summary = json.loads(SUMMARY.read_text(encoding="utf-8"))
    ents = {e["id"]: e for e in summary["entities"]}
    sources = json.loads(RULES.read_text(encoding="utf-8")).get("sources", {})
    to_krw = krw_rates()
    names: list[str] = []
    name_index: dict[str, int] = {}
    points: list[list[int]] = []
    for record in json.loads(INDEX.read_text(encoding="utf-8"))["records"]:
        final = record.get("final_output") or {}
        if final.get("sold_quality") != "asking" or final.get("entity_note") in ("duplicate", "too_cheap", "set"):
            continue
        price, currency = final.get("parsed_price_numeric"), str(final.get("currency") or "KRW").upper()
        if not price or currency not in to_krw or RENTAL.search(final.get("title_raw") or ""):
            continue
        ids = [e for e in record.get("entity_ids") or [] if e in ents and not ents[e].get("feature")]
        if not ids:
            continue
        leaf = max(ids, key=lambda e: (e.count(":"), len(e)))
        entity = ents[leaf]
        kind = leaf.split(":")[1]
        is_m = (entity.get("mount") == "M") or bool(re.match(r"leica:body:m", leaf))
        row = (0 if is_m else 1) if kind == "body" else (2 if is_m else 3)
        krw = price * to_krw[currency]
        if not 50_000 <= krw <= 300_000_000:
            continue
        if leaf not in name_index:
            name_index[leaf] = len(names)
            names.append(leaf)
        country = (sources.get(final.get("source") or "") or {}).get("country")
        points.append([round(krw / 1000), row, region_of(country), name_index[leaf]])
    OUT.write_text(json.dumps({"schema_version": "market_map_v1",
                               "generated_at": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
                               "entities": names, "points": points}, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    rows = [sum(1 for p in points if p[1] == r) for r in range(4)]
    print(f"✅ 점 지도: 매물 {len(points)}개 (M 바디 {rows[0]} · 바디 {rows[1]} · M 렌즈 {rows[2]} · 렌즈 {rows[3]}), 모델 {len(names)}개, {OUT.stat().st_size // 1024}KB")


if __name__ == "__main__":
    main()
