"""밤샘 조사(2026-11-15): 이 맥에서 403이던 매장이 GitHub 서버(실제 크롤이 도는 곳)에서도 막히는지 첫 화면·중고 화면 상태만 본다.
우회하지 않음 — 요청 한 번씩, 일반 브라우저 UA. site-test 브랜치에서만."""
import json, time, requests
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36"
URLS = {
 "Park Cameras": ["https://www.parkcameras.com/", "https://www.parkcameras.com/used/lenses/leica"],
 "Clifton Cameras": ["https://www.cliftoncameras.co.uk/", "https://www.cliftoncameras.co.uk/used-leica/"],
 "London Camera Exchange": ["https://www.lcegroup.co.uk/", "https://www.lcegroup.co.uk/Used/Leica"],
 "Cameraworld": ["https://www.cameraworld.co.uk/", "https://www.cameraworld.co.uk/used/leica"],
 "Used Photo Pro": ["https://www.usedphotopro.com/", "https://www.usedphotopro.com/leica"],
 "Roberts Camera": ["https://robertscamera.com/", "https://robertscamera.com/products/cameras-lenses/cameras/leica"],
 "Hunt's": ["https://www.huntsphotoandvideo.com/", "https://www.huntsphotoandvideo.com/used"],
 "Blue Moon": ["https://www.bluemooncamera.com/"],
 "Cameranu": ["https://www.cameranu.nl/", "https://www.cameranu.nl/nl/c3042/tweedehands"],
 "Foto Koch": ["https://www.fotokoch.de/", "https://www.fotokoch.de/gebraucht.html"],
 "Foto Gregor": ["https://www.fotogregor.de/"],
 "Fotoskoda": ["https://www.fotoskoda.cz/"],
 "KEH": ["https://www.keh.com/"],
 "Adorama": ["https://www.adorama.com/"],
 "Map Camera": ["https://www.mapcamera.com/"],
 "Fujiya": ["https://www.fujiya-camera.co.jp/shop/c/c20/"],
}
out = {}
for shop, urls in URLS.items():
    out[shop] = []
    for u in urls:
        try:
            r = requests.get(u, headers={"User-Agent": UA, "Accept-Language": "en"}, timeout=25)
            body = r.text[:3000].lower()
            flag = "cloudflare" if ("just a moment" in body or "cf-chl" in body) else ("captcha" if "captcha" in body else "")
            out[shop].append((u, r.status_code, flag, len(r.text)))
        except Exception as e:
            out[shop].append((u, "error", type(e).__name__, 0))
        time.sleep(2)
    print(shop, out[shop])
json.dump(out, open("probe_blocked.json", "w"), ensure_ascii=False, indent=1)
