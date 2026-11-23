import json, os, time, requests
os.makedirs("out", exist_ok=True)
H = {"User-Agent": "Mozilla/5.0"}
log = []
def get(base, u):
    for i in range(4):
        r = requests.get(base + u, headers=H, timeout=40)
        log.append(f"{r.status_code} {base}{u}")
        if r.status_code == 429:
            time.sleep(5 * (i + 1)); continue
        return r
    return r
for name, base in (("procam", "https://procam.com"), ("district", "https://districtcamera.com")):
    r = get(base, "/collections.json?limit=250")
    cols = r.json().get("collections", []) if r.status_code == 200 else []
    rows = [(c["handle"], c["products_count"], c["title"]) for c in cols if any(k in (c["handle"] + c["title"]).lower() for k in ("leica", "used", "pre-owned", "preowned"))]
    open(f"out/{name}_collections.txt", "w").write("\n".join(map(str, rows)))
    allp = {}
    for h, n, t in rows:
        if "leica" not in h.lower() and "used" not in h.lower():
            continue
        if n > 3000:
            continue
        for page in range(1, 8):
            rr = get(base, f"/collections/{h}/products.json?limit=250&page={page}")
            if rr.status_code != 200:
                break
            ps = rr.json().get("products", [])
            if not ps:
                break
            for p in ps:
                p["_col"] = h
                allp[p["id"]] = p
            time.sleep(1.5)
    json.dump(list(allp.values()), open(f"out/{name}_products.json", "w"), ensure_ascii=False)
open("out/log.txt", "w").write("\n".join(log))
