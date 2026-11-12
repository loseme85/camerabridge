"""밤샘 사이트 조사 (2026-11-12): 이 맥 주소가 Shopify에 묶여(429) GitHub 서버에서 대기 후보 매장 구조를 한 번에 본다.
매장마다 products.json을 천천히(쪽 사이 3초, 429면 Retry-After만큼 기다림) 최대 MAX_PAGES쪽까지 읽어
라이카 상품 수·견본(제목·종류·태그·가격·판매 여부·설명 앞부분)과 중고 관련 컬렉션 이름을 probe_<매장>.json으로 남긴다.
site-test 브랜치에서만 쓰고 main에는 넣지 않는다."""
from __future__ import annotations

import json
import re
import time

import requests

SHOPS = [
    "https://tokiwa-camera.co.jp", "https://www.thecamerastore.com", "https://timlei.ca", "https://artralab.com",
    "https://grandemarvin.com", "https://prophotosupply.com", "https://www.leicastoremanchester.com",
    "https://www.kamera-express.lu", "https://www.yaotomi.co.jp", "https://www.profotica.nl", "https://khrome.de",
    "https://grainoverpixel.com", "https://clickundsurr.de", "https://www.fotododici.com", "https://kamerastockholm.se",
    "https://unit-filmcamera.com", "https://www.leicastore.com.br", "https://cameraboutique.at",
    "https://www.robertwhite.co.uk", "https://www.carmarthencameras.com", "https://kmcamera.com",
]
MAX_PAGES = 12
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36"
LEICA = re.compile(r"leica|leitz|ライカ|라이카|summicron|summilux|elmarit|noctilux|elmar\b", re.I)
USED = re.compile(r"used|pre-?owned|second|occasion|gebraucht|usat|brugt|begagnad|semi-?novo|中古|usado|tweedehands|vintage", re.I)


def get(sess: requests.Session, url: str, params: dict | None = None):
    for attempt in range(4):
        try:
            resp = sess.get(url, params=params, timeout=30)
        except Exception as error:  # noqa: BLE001
            return None, f"error {error.__class__.__name__}"
        if resp.status_code == 429:
            time.sleep(min(int(resp.headers.get("Retry-After") or 0) or 20 * (attempt + 1), 90))
            continue
        return resp, str(resp.status_code)
    return None, "429 x4"


def probe(base: str) -> dict:
    sess = requests.Session()
    sess.headers["User-Agent"] = UA
    out: dict = {"base": base}
    resp, status = get(sess, f"{base}/collections.json", {"limit": 250})
    out["collections_status"] = status
    if resp is not None and resp.ok:
        try:
            cols = resp.json().get("collections", [])
            out["collections"] = [(c.get("handle"), c.get("products_count")) for c in cols
                                  if LEICA.search(c.get("handle", "") + c.get("title", "")) or USED.search(c.get("handle", "") + c.get("title", ""))][:40]
        except ValueError:
            out["collections"] = "not json"
    time.sleep(3)
    total, leica = 0, []
    out["pages"] = 0
    for page in range(1, MAX_PAGES + 1):
        resp, status = get(sess, f"{base}/products.json", {"limit": 250, "page": page})
        out["products_status"] = status
        if resp is None or not resp.ok:
            break
        try:
            items = resp.json().get("products", [])
        except ValueError:
            out["products_status"] = "not json"
            break
        if not items:
            break
        out["pages"] = page
        total += len(items)
        for p in items:
            text = " ".join([p.get("title", ""), p.get("vendor", ""), " ".join(p.get("tags") or [])])
            if LEICA.search(text):
                variants = p.get("variants") or [{}]
                leica.append({
                    "title": p.get("title"), "vendor": p.get("vendor"), "type": p.get("product_type"),
                    "tags": (p.get("tags") or [])[:12], "handle": p.get("handle"),
                    "price": variants[0].get("price"), "available": any(v.get("available") for v in variants),
                    "body": re.sub(r"<[^>]+>", " ", p.get("body_html") or "")[:400],
                    "image": ((p.get("images") or [{}])[0] or {}).get("src"),
                })
        time.sleep(3)
    out["total_products_seen"] = total
    out["leica_count"] = len(leica)
    out["leica_available"] = sum(1 for x in leica if x["available"])
    out["leica_samples"] = leica[:60]
    return out


def main() -> None:
    for base in SHOPS:
        result = probe(base)
        name = re.sub(r"^https?://(www\.)?", "", base).split("/")[0]
        json.dump(result, open(f"probe_{name}.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print(f"{name}: collections {result['collections_status']} · products {result.get('products_status')} · "
              f"{result['pages']}쪽 {result['total_products_seen']}개 · 라이카 {result['leica_count']} (판매 중 {result['leica_available']})")
        if isinstance(result.get("collections"), list):
            print("   컬렉션:", result["collections"][:12])
        for x in result["leica_samples"][:6]:
            print("   ·", x["price"], "|", str(x["title"])[:60], "|", x["type"], "|", x["available"])


if __name__ == "__main__":
    main()
