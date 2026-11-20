import json, re, requests, os
DOMAINS = ["districtcamera.com","victorycamera.com","cameramall.com","recycledphoto.com","kamerahaus.com","seawoodphoto.com","thecameraexchange.com","houstoncameraexchange.com","igorcamera.com","www.allenscamera.com","www.acephoto.com","www.nationalcamera.com","www.procamsd.com","www.prophotodc.com","www.thephotocenter.com","www.occamera.com","www.bergencountycamera.com"]
UA = {"User-Agent": "Mozilla/5.0 (compatible; CameraBridgeBot/1.0; +https://camerabridge.io)"}
out = {}
for d in DOMAINS:
    r = {}
    try:
        rb = requests.get(f"https://{d}/robots.txt", headers=UA, timeout=20)
        r["robots"] = [rb.status_code, "\n".join(l for l in rb.text.splitlines() if re.match(r"(?i)(user-agent|disallow: /(products|collections|search|api)|crawl-delay)", l))[:400]]
    except Exception as e:
        r["robots"] = str(e)[:80]
    try:
        p = requests.get(f"https://{d}/products.json?limit=250&page=1", headers=UA, timeout=25)
        r["pj"] = p.status_code
        if p.status_code == 200 and p.text.startswith("{"):
            n = 0; lei = []; page = 1
            while page <= 12:
                items = (p.json().get("products") or [])
                n += len(items)
                for it in items:
                    t = f"{it.get('title','')} {it.get('vendor','')} {' '.join(it.get('tags') or [])} {it.get('product_type','')}"
                    if re.search(r"(?i)leica|leitz", t):
                        lei.append({"t": it["title"], "v": it.get("vendor"), "pt": it.get("product_type"), "tags": (it.get("tags") or [])[:8], "price": (it.get("variants") or [{}])[0].get("price"), "avail": any(v.get("available") for v in it.get("variants") or [])})
                if len(items) < 250: break
                page += 1
                p = requests.get(f"https://{d}/products.json?limit=250&page={page}", headers=UA, timeout=25)
                if p.status_code != 200: break
            r["total"] = n; r["leica_n"] = len(lei); r["leica_sample"] = lei[:25]
        else:
            r["pj_head"] = p.text[:150]
    except Exception as e:
        r["pj"] = str(e)[:80]
    out[d] = r
os.makedirs("out", exist_ok=True)
json.dump(out, open("out/us_probe.json", "w"), ensure_ascii=False, indent=1)
print(json.dumps({d: {k: (v if k != "leica_sample" else len(v)) for k, v in r.items() if k in ("pj", "total", "leica_n", "robots")} for d, r in out.items()}, ensure_ascii=False, indent=1))
