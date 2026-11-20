import json, re, requests, os
UA = {"User-Agent": "Mozilla/5.0 (compatible; CameraBridgeBot/1.0; +https://camerabridge.io)"}
os.makedirs("out", exist_ok=True)
for d in ["kamerahaus.com", "victorycamera.com", "cameramall.com"]:
    items = []; page = 1
    while page <= 20:
        r = requests.get(f"https://{d}/products.json?limit=250&page={page}", headers=UA, timeout=30)
        if r.status_code != 200: break
        b = r.json().get("products") or []
        items += b
        if len(b) < 250: break
        page += 1
    lei = [i for i in items if re.search(r"(?i)leica|leitz", f"{i.get('title','')} {i.get('vendor','')} {i.get('product_type','')} {' '.join(i.get('tags') or [])}")]
    json.dump({"products": lei, "total": len(items)}, open(f"out/{d}.json", "w"), ensure_ascii=False)
    print(d, len(items), len(lei))
