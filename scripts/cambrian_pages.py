import os, re, requests
os.makedirs("out", exist_ok=True)
base = "https://www.cambrianphoto.co.uk"
s = requests.Session(); s.headers["User-Agent"] = "CameraBridge/1.0 (+https://camerabridge.io)"
for name, path in (("shipping", "/policies/shipping-policy"), ("terms", "/policies/terms-of-service"), ("contact", "/pages/contact-us"), ("contact2", "/pages/contact")):
    r = s.get(base + path, timeout=30)
    print(name, r.status_code, len(r.text))
    t = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", r.text, flags=re.S)
    t = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", t))
    open(f"out/{name}.txt", "w").write(f"{r.status_code}\n" + t[:6000])
