"""GitHub 서버에서 Cambrian Photography(Shopify) 중고 라이카 컬렉션을 받아 구조를 본다 (이 맥은 429)."""
import json, os, time, requests
os.makedirs("out", exist_ok=True)
base = "https://www.cambrianphoto.co.uk"
s = requests.Session(); s.headers["User-Agent"] = "CameraBridge/1.0 (+https://camerabridge.io)"
out = {}
for col in ("used-leica",):
    items = []
    for page in range(1, 10):
        r = s.get(f"{base}/collections/{col}/products.json", params={"limit": 250, "page": page}, timeout=30)
        print(col, page, r.status_code)
        if r.status_code != 200:
            break
        ps = r.json().get("products", [])
        if not ps:
            break
        items += ps
        time.sleep(3)
    out[col] = items
json.dump(out, open("out/cambrian.json", "w"), ensure_ascii=False)
print({k: len(v) for k, v in out.items()})
