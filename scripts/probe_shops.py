"""밤샘 조사(2026-11-15): Camera Market(스페인) — 라이카 컬렉션과 개인 판매 컬렉션 표본 (site-test 브랜치에서만)."""
import json, time, requests
s = requests.Session(); s.headers["User-Agent"] = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36"
out = {}
for col in ["camaras-leica", "productos-de-usuarios-particulares", "lentes"]:
    rows = []
    for page in range(1, 6):
        r = s.get(f"https://cameramarket.co/collections/{col}/products.json", params={"limit": 250, "page": page}, timeout=30)
        print(col, page, r.status_code)
        if r.status_code != 200: break
        ps = r.json().get("products", [])
        if not ps: break
        rows += ps; time.sleep(3)
    out[col] = rows
json.dump(out, open("probe_cameramarket.json", "w"), ensure_ascii=False)
for k, v in out.items(): print(k, len(v))
