import json, re, requests, os
UA = {"User-Agent": "Mozilla/5.0 (compatible; CameraBridgeBot/1.0; +https://camerabridge.io)"}
out = {}
for d in ["kamerahaus.com", "victorycamera.com", "cameramall.com", "recycledphoto.com", "districtcamera.com"]:
    items = []; page = 1
    while page <= 14:
        r = requests.get(f"https://{d}/products.json?limit=250&page={page}", headers=UA, timeout=30)
        if r.status_code != 200: break
        b = r.json().get("products") or []
        items += b
        if len(b) < 250: break
        page += 1
    lei = [i for i in items if re.search(r"(?i)leica|leitz", f"{i.get('title','')} {i.get('vendor','')} {i.get('product_type','')}")]
    cut = []
    for i in lei[:400]:
        cut.append({"id": i["id"], "handle": i["handle"], "title": i["title"], "vendor": i.get("vendor"), "pt": i.get("product_type"), "tags": i.get("tags"),
                    "created": i.get("created_at"), "published": i.get("published_at"),
                    "variants": [{"price": v.get("price"), "avail": v.get("available"), "sku": v.get("sku"), "title": v.get("title"), "cap": v.get("compare_at_price")} for v in (i.get("variants") or [])[:2]],
                    "img": ((i.get("images") or [{}])[0].get("src")),
                    "body": re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", i.get("body_html") or ""))[:700]})
    out[d] = {"total": len(items), "leica": cut}
os.makedirs("out", exist_ok=True)
json.dump(out, open("out/us_probe2.json", "w"), ensure_ascii=False)
print({d: (v["total"], len(v["leica"])) for d, v in out.items()})
