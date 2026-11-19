import json, os, re, time, requests
os.makedirs("out", exist_ok=True)
base = "https://www.teds.com.au"
s = requests.Session(); s.headers["User-Agent"] = "CameraBridge/1.0 (+https://camerabridge.io)"
pat = re.compile(r"(?i)leica|leitz|summicron|summilux|elmar|noctilux|summarit|hektor|telyt")
out = {}
r = s.get(base + "/collections.json", params={"limit": 250}, timeout=30)
print("collections.json", r.status_code)
cols = [c["handle"] for c in r.json().get("collections", [])] if r.status_code == 200 else []
out["collections"] = cols
cand = [c for c in cols if re.search(r"(?i)second|used|pre-?owned|leica", c)]
print(len(cols), cand[:40])
out["cand"] = cand
for col in cand[:12]:
    items = []
    for page in range(1, 8):
        r = s.get(f"{base}/collections/{col}/products.json", params={"limit": 250, "page": page}, timeout=30)
        if r.status_code != 200:
            print(col, page, r.status_code); break
        ps = r.json().get("products", [])
        if not ps: break
        items += ps; time.sleep(3)
    keep = [p for p in items if pat.search(p["title"] + " " + p["vendor"])]
    print(col, len(items), len(keep))
    out[col] = {"n": len(items), "leica": keep}
json.dump(out, open("out/teds.json", "w"), ensure_ascii=False)
