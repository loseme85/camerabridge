import os, re, requests
os.makedirs("out", exist_ok=True)
base = "https://www.fotospina.it"
s = requests.Session(); s.headers["User-Agent"] = "CameraBridge/1.0 (+https://camerabridge.io)"
for name, path in (("robots", "/robots.txt"), ("home", "/"), ("sitemap", "/sitemap.xml"), ("leica", "/leica"), ("search", "/search?q=leica")):
    try:
        r = s.get(base + path, timeout=30)
        print(name, r.status_code, len(r.text))
        open(f"out/{name}.txt", "w").write(f"{r.status_code}\n{r.text[:60000]}")
    except Exception as e:
        print(name, "ERR", e)
        open(f"out/{name}.txt", "w").write(f"ERR {e}")
