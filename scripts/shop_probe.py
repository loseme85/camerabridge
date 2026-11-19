"""GitHub 서버에서 Shopify 매장의 전체 상품을 받아 라이카 계열만 남긴다 (이 맥은 429)."""
import json, os, re, sys, time, requests
base = os.environ["BASE"]
os.makedirs("out", exist_ok=True)
s = requests.Session(); s.headers["User-Agent"] = "CameraBridge/1.0 (+https://camerabridge.io)"
items = []
for page in range(1, 40):
    r = s.get(f"{base}/products.json", params={"limit": 250, "page": page}, timeout=30)
    print(page, r.status_code)
    if r.status_code != 200:
        break
    ps = r.json().get("products", [])
    if not ps:
        break
    items += ps
    time.sleep(3)
pat = re.compile(r"(?i)leica|leitz|summicron|summilux|elmar|noctilux|summarit|hektor|telyt")
keep = [p for p in items if pat.search(p["title"] + " " + p["vendor"] + " " + " ".join(p["tags"]))]
json.dump({"total": len(items), "leica": keep}, open("out/shop.json", "w"), ensure_ascii=False)
print(len(items), len(keep))
