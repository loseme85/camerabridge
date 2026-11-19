"""GitHub 서버에서 Cambrian Photography(Shopify) 중고 라이카 컬렉션을 받아 구조를 본다 (이 맥은 429)."""
import json, os, time, requests
os.makedirs("out", exist_ok=True)
base = "https://www.cambrianphoto.co.uk"
s = requests.Session(); s.headers["User-Agent"] = "CameraBridge/1.0 (+https://camerabridge.io)"
out = {}
for col in ("used-leica", "all"):
    items = []
    for page in range(1, 30):
        url = f"{base}/products.json" if col == "all" else f"{base}/collections/{col}/products.json"
        r = s.get(url, params={"limit": 250, "page": page}, timeout=30)
        print(col, page, r.status_code)
        if r.status_code != 200:
            break
        ps = r.json().get("products", [])
        if not ps:
            break
        items += ps
        time.sleep(3)
    out[col] = items
import re
out["all"] = [p for p in out.get("all", []) if re.search(r"(?i)leica|leitz|summicron|summilux|elmar|noctilux|summarit", p["title"] + " " + p["vendor"])]
json.dump(out, open("out/cambrian.json", "w"), ensure_ascii=False)
print({k: len(v) for k, v in out.items()})
