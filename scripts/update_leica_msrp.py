"""라이카 공식 사이트의 나라별 신품 정가 → data/config/leica_msrp.json

    python3 scripts/update_leica_msrp.py [--budget N]

딜러 화면의 신품(N) 기준가에 쓴다. 나라마다 정가·세금이 달라서 중고 기준가 × 등급 비율로는 맞지 않음.
- 상품 목록: leica-camera.com 사이트 지도에서 사진 카메라·렌즈 상품 페이지와 나라별 주소(hreflang).
  라이카 판매 페이지가 있는 나라는 지도에서 그대로 읽어서, 라이카가 나라를 늘리면 따라 늘어남
- 가격: 상품 페이지의 view_item 기록(item_id = 라이카 제품 번호, currency, value)
- 우리 모델 목록(entity_catalog_v1.json)에 제품 번호가 있는 현행 상품만
- 하루에 조금씩(--budget 요청, 요청 사이 6초) 오래된 것부터 이어서 받는다. 한 번에 다 받으면 라이카가 429로 막음
  (2026-10-27 1.5초 간격으로 수십 페이지 뒤 429). 429·503이 오면 바로 멈추고 받은 데까지 저장
- 영국 정가와 환율로 비교해 0.6~1.8배를 벗어나면 버림 (덴마크 페이지는 유로 가격에 DKK를 붙여 둠)
- robots.txt: /product/* 와 en-CA 는 막혀 있어 쓰지 않음. 매일 (.github/workflows/leica-msrp.yml)
"""
from __future__ import annotations

import datetime as dt
import json
import re
import sys
import time
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "app"))
from crawl_engine import http_get  # noqa: E402

BASE = "https://leica-camera.com"
OUT = REPO / "data/config/leica_msrp.json"
CATALOG = REPO / "data/config/entity_catalog_v1.json"
FX = REPO / "data/fx_rates.json"
DELAY = 6
BUDGET = 150
REFRESH_DAYS = 30
SKIP_LOCALES = {"en-GB", "x-default", "en-CA"}  # 영국은 기준으로 따로 받음, en-CA는 robots.txt
PRODUCT_PATH = re.compile(r"^/en-GB/photography/(cameras|lenses)/[^/]+/[^/]+$")
VIEW_ITEM = re.compile(r'"event":"view_item","ecommerce":\{"currency":"([A-Z]{3})","value":([0-9.]+),"items":\[\{"item_id":"(\d{5})"')


class Blocked(Exception):
    pass


def get(url: str) -> str | None:
    time.sleep(DELAY)
    try:
        response = http_get(url, timeout=40)
    except Exception:  # noqa: BLE001
        return None
    if response.status_code in (429, 503):
        raise Blocked(f"{response.status_code} {url}")
    return response.text if response.status_code == 200 else None


def country_of(locale: str) -> str:
    """en-DK → DK, de-CH·fr-CH → CH. 나라가 없는 지역(zh-Hant)은 그대로."""
    return locale.rsplit("-", 1)[-1] if re.fullmatch(r"[a-z]{2}-[A-Z]{2}", locale) else locale


def sitemap_products() -> dict[str, dict[str, str]]:
    """en-GB 카메라·렌즈 상품마다 {지역: 주소}."""
    index = get(f"{BASE}/sitemap.xml") or ""
    products = {}
    for page in re.findall(r"<loc>([^<]+sitemap\.xml\?page=\d+)</loc>", index):
        xml = get(page.replace("&amp;", "&")) or ""
        for block in re.findall(r"<url>(.*?)</url>", xml, re.S):
            alts = dict(re.findall(r'hreflang="([^"]+)" href="([^"]+)"', block))
            gb = alts.get("en-GB", "")
            if PRODUCT_PATH.match(gb.replace(BASE, "")):
                products[gb] = {loc: url for loc, url in alts.items() if loc not in SKIP_LOCALES}
    return products


def price_of(html: str | None) -> tuple[str, float, str] | None:
    """(제품 번호, 가격, 통화)"""
    match = VIEW_ITEM.search(html or "")
    if not match or float(match.group(2)) <= 0:
        return None
    return match.group(3), float(match.group(2)), match.group(1)


def plausible(price: float, cur: str, gb: list, krw_per: dict) -> bool:
    """영국 정가와 환율로 비교해 0.6~1.8배 안이면 믿음."""
    if cur not in krw_per or gb[1] not in krw_per:
        return False
    ratio = price * krw_per[cur] / (gb[0] * krw_per[gb[1]])
    return 0.6 <= ratio <= 1.8


def old(day: str | None, today: dt.date) -> bool:
    return not day or (today - dt.date.fromisoformat(day)).days >= REFRESH_DAYS


def main(budget: int = BUDGET) -> None:
    today = dt.date.today()
    catalog = json.loads(CATALOG.read_text())
    entities = catalog["entities"] if isinstance(catalog, dict) else catalog
    entities = entities.values() if isinstance(entities, dict) else entities
    known = {code for e in entities for code in (e.get("codes") or []) if re.fullmatch(r"\d{5}", code)}
    rates = json.loads(FX.read_text())["rates"]
    krw_per = {c: rates["KRW"] / v for c, v in rates.items()}
    state = json.loads(OUT.read_text()) if OUT.exists() else {}
    pages = state.get("pages") or {}            # 영국 상품 주소 → {code, at, alts}
    prices = state.get("prices") or {}          # 제품 번호 → {나라: [가격, 통화, 받은 날]}
    misses = state.get("misses") or {}          # 제품 번호 → {나라: 가격이 없거나 버린 날} (30일 동안 다시 안 봄)
    rejected = state.get("rejected") or {}      # 제품 번호 → {나라: [가격, 통화]} 환율 비교로 버린 값
    unknown = state.get("not_in_catalog") or {}
    used, todo = 0, []
    try:
        if not pages or old(state.get("sitemap_at"), today):
            for gb, alts in sitemap_products().items():
                pages.setdefault(gb, {})["alts"] = alts
            for gb in [gb for gb, p in pages.items() if "alts" not in p]:
                del pages[gb]
            state["sitemap_at"] = today.isoformat()
            used += 25
        # 할 일: 영국 페이지(제품 번호·기준 정가) → 나라별 페이지, 오래된 것부터
        todo = []
        for gb, page in pages.items():
            if old(page.get("at"), today):
                todo.append((page.get("at") or "", "GB", gb, gb))
            code = page.get("code")
            if code not in known or code not in prices or "GB" not in prices[code]:
                continue
            for locale, url in page["alts"].items():
                country = country_of(locale)
                last = (prices[code].get(country) or [None, None, None])[2] or misses.get(code, {}).get(country)
                if old(last, today):
                    todo.append((last or "", country, url, gb))
        todo.sort(key=lambda t: (t[0], t[1] != "GB"))
        for _, country, url, gb in todo:
            if used >= budget:
                break
            used += 1
            got = price_of(get(url + "/shop-now"))
            if country == "GB":
                pages[gb]["at"] = today.isoformat()
                if not got:
                    continue
                pages[gb]["code"] = got[0]
                if got[0] in known:
                    prices.setdefault(got[0], {})["GB"] = [got[1], got[2], today.isoformat()]
                else:
                    unknown[got[0]] = gb.rsplit("/", 1)[-1]
                continue
            code = pages[gb]["code"]
            if got and got[0] == code and plausible(got[1], got[2], prices[code]["GB"], krw_per):
                prices[code][country] = [got[1], got[2], today.isoformat()]
                misses.get(code, {}).pop(country, None)
                rejected.get(code, {}).pop(country, None)
            else:
                misses.setdefault(code, {})[country] = today.isoformat()
                if got and got[0] == code:
                    rejected.setdefault(code, {})[country] = [got[1], got[2]]
    except Blocked as e:
        print(f"라이카가 막음({e}) — 받은 데까지 저장하고 내일 이어서")
    OUT.write_text(json.dumps({
        "source": f"{BASE} (상품 페이지 view_item)",
        "updated_at": dt.datetime.now(dt.timezone.utc).isoformat(timespec="minutes"),
        "sitemap_at": state.get("sitemap_at"),
        "prices": dict(sorted(prices.items())),
        "rejected": dict(sorted((k, v) for k, v in rejected.items() if v)),
        "not_in_catalog": dict(sorted(unknown.items())),
        "misses": dict(sorted((k, v) for k, v in misses.items() if v)),
        "pages": dict(sorted(pages.items())),
    }, ensure_ascii=False, indent=1) + "\n")
    countries = {c for by in prices.values() for c in by}
    print(f"요청 {used}회 · 정가 {len(prices)}개 제품 · {len(countries)}개 나라 · 아직 안 본 페이지 {max(len(todo) - used, 0)}개")


if __name__ == "__main__":
    main(int(sys.argv[sys.argv.index("--budget") + 1]) if "--budget" in sys.argv else BUDGET)
