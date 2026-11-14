"""밤샘 조사(2026-11-15): Schouten Select Shopify 'leica' 컬렉션 앞 3쪽을 probe_schouten.json으로 (site-test 브랜치에서만)."""
import json, time, requests
s = requests.Session(); s.headers["User-Agent"] = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36"
out = []
for page in range(1, 4):
    r = s.get("https://schouten-select.com/collections/leica/products.json", params={"limit": 250, "page": page}, timeout=30)
    print(page, r.status_code)
    if r.status_code != 200: break
    ps = r.json().get("products", [])
    if not ps: break
    out += ps; time.sleep(3)
json.dump(out, open("probe_schouten.json", "w"), ensure_ascii=False)
print("products", len(out), "available", sum(any(v.get("available") for v in p.get("variants") or []) for p in out))
