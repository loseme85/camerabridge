import json, os, time, requests
os.makedirs("out", exist_ok=True)
H = {"User-Agent": "Mozilla/5.0"}
base = "https://classicconnection.com"
log = []
def get(u):
    for i in range(4):
        r = requests.get(base + u, headers=H, timeout=40)
        log.append(f"{r.status_code} {u}")
        if r.status_code == 429:
            time.sleep(5 * (i + 1)); continue
        return r
    return r
r = get("/collections.json?limit=250")
cols = r.json().get("collections", []) if r.status_code == 200 else []
json.dump(cols, open("out/collections.json", "w"), ensure_ascii=False)
rows = []
for c in cols:
    if "leica" in c["handle"]:
        rows.append((c["handle"], c["products_count"], c["title"]))
open("out/leica_collections.txt", "w").write("\n".join(map(str, rows)))
allp = {}
for h, n, t in rows:
    if not any(k in h for k in ("used", "demo")):
        continue
    for page in range(1, 6):
        rr = get(f"/collections/{h}/products.json?limit=250&page={page}")
        if rr.status_code != 200:
            break
        ps = rr.json().get("products", [])
        if not ps:
            break
        for p in ps:
            allp[p["id"]] = p
        time.sleep(1.5)
json.dump(list(allp.values()), open("out/products.json", "w"), ensure_ascii=False)
open("out/log.txt", "w").write("\n".join(log) + f"\nproducts={len(allp)}\n")
