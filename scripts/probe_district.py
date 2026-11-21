"""District Camera(Shopify) 읽기 전용 시험: 컬렉션 목록과 라이카 상품 수·종류·태그·제목 표본 (저장소 데이터는 안 바꿈)"""
import json, re, time, html, requests
S = requests.Session(); S.headers["User-Agent"] = "Mozilla/5.0 (compatible; CameraBridgeBot/1.0)"
base = "https://districtcamera.com"
def get(path, **p):
    for wait in (0, 15, 45, 90):
        time.sleep(wait)
        r = S.get(base + path, params=p, timeout=40)
        if r.status_code != 429: return r
    return r
out = {}
r = get("/collections.json", limit=250); out["collections_status"] = r.status_code
try: out["collections"] = [(c["handle"], c["title"], c.get("products_count")) for c in r.json()["collections"]]
except Exception as e: out["collections_err"] = str(e)[:100]
prods = []
for pg in range(1, 30):
    r = get("/products.json", limit=250, page=pg)
    if r.status_code != 200: out["products_status"] = r.status_code; break
    ps = r.json().get("products", [])
    if not ps: break
    prods += ps; time.sleep(4)
out["total_products"] = len(prods)
lei = [p for p in prods if re.search(r"leica|leitz", p.get("title", "") + " " + p.get("vendor", "") + " " + " ".join(p.get("tags") or []), re.I)]
out["leica_products"] = len(lei)
out["vendors"] = {}
for p in prods: out["vendors"][p.get("vendor", "")] = out["vendors"].get(p.get("vendor", ""), 0) + 1
out["vendors"] = dict(sorted(out["vendors"].items(), key=lambda x: -x[1])[:12])
out["types"] = {}
for p in lei: out["types"][p.get("product_type", "")] = out["types"].get(p.get("product_type", ""), 0) + 1
out["sample"] = [{"title": p["title"], "type": p.get("product_type"), "tags": (p.get("tags") or [])[:8], "price": (p["variants"][0]["price"] if p.get("variants") else None),
                  "avail": (p["variants"][0].get("available") if p.get("variants") else None), "desc": re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", p.get("body_html") or "")))[:200]} for p in lei[:25]]
import os; os.makedirs("out", exist_ok=True)
json.dump(out, open("out/district.json", "w"), ensure_ascii=False, indent=1)
print(json.dumps({k: v for k, v in out.items() if k != "sample"}, ensure_ascii=False)[:1500])
