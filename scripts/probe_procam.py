import json, os, time, requests
os.makedirs("out", exist_ok=True)
H = {"User-Agent": "Mozilla/5.0"}
allp, log = [], []
for page in range(1, 60):
    r = None
    for i in range(4):
        r = requests.get(f"https://procam.com/products.json?limit=250&page={page}", headers=H, timeout=40)
        log.append(f"{r.status_code} page{page}")
        if r.status_code == 429:
            time.sleep(5 * (i + 1)); continue
        break
    if r.status_code != 200:
        break
    ps = r.json().get("products", [])
    if not ps:
        break
    allp += ps
    time.sleep(1.5)
leica = [p for p in allp if "leica" in (p["title"] + " " + p["vendor"] + " " + " ".join(p["tags"])).lower()]
json.dump(leica, open("out/procam_leica.json", "w"), ensure_ascii=False)
open("out/log.txt", "w").write("\n".join(log) + f"\ntotal={len(allp)} leica={len(leica)}\n")
