"""밤샘 (2026-11-12): 새 매장 10곳의 배송 안내를 GitHub 서버에서 읽어 probe_ship_<매장>.txt로 (이 맥 주소는 Shopify 429)."""
import re
import time

import requests

SHOPS = ["https://timlei.ca", "https://www.leicastoremanchester.com", "https://tokiwa-camera.co.jp", "https://www.thecamerastore.com",
         "https://www.robertwhite.co.uk", "https://www.profotica.nl", "https://www.fotododici.com", "https://khrome.de",
         "https://kmcamera.com", "https://cameraboutique.at"]
PATHS = ["/policies/shipping-policy", "/pages/shipping", "/pages/shipping-policy", "/pages/delivery", "/pages/versand",
         "/pages/spedizioni", "/pages/verzending", "/pages/international-shipping", "/pages/faq"]
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36"
WORDS = re.compile(r"international|worldwide|world-wide|overseas|ship to|we ship|countries|europe|EU\b|united kingdom|canada|"
                   r"usa|united states|korea|japan|海外|発送|international|versand|ausland|spedizion|estero|verzend|buitenland|weltweit", re.I)

for base in SHOPS:
    name = re.sub(r"^https?://(www\.)?", "", base).split("/")[0]
    out = []
    for path in PATHS:
        try:
            r = requests.get(base + path, headers={"User-Agent": UA}, timeout=25)
        except Exception as e:  # noqa: BLE001
            out.append(f"{path}: error {e.__class__.__name__}")
            continue
        if r.status_code != 200:
            out.append(f"{path}: {r.status_code}")
            time.sleep(2)
            continue
        text = re.sub(r"\s+", " ", re.sub(r"<script.*?</script>|<style.*?</style>|<[^>]+>", " ", r.text, flags=re.S))
        hits = [text[max(0, m.start() - 160): m.end() + 160] for m in WORDS.finditer(text)][:12]
        out.append(f"{path}: 200 ({len(text)}자)\n  " + "\n  ".join(hits))
        time.sleep(2)
    open(f"probe_ship_{name}.txt", "w", encoding="utf-8").write("\n".join(out))
    print(name, "→", ", ".join(o.split("\n")[0] for o in out))
