"""2026-11-16 밤샘 후보의 GitHub 서버 공개 목록 접속만 확인. 데이터·운영 상태는 쓰지 않는다."""
import time
import requests
from urllib.parse import urlsplit
from urllib.robotparser import RobotFileParser

UA = 'CameraBridge/1.0 (+https://camerabridge.io)'
URLS = [
 'https://realcamera.co.uk/wp-json/wc/store/v1/products?search=leica&per_page=100&page=1',
 'https://realcamera.co.uk/wp-json/wc/store/v1/products?search=leica&per_page=100&page=2',
 'https://elle-et-lui-photographie.fr/boutique/occasion?marque=leica',
 'https://elle-et-lui-photographie.fr/boutique/produit/7840',
 'https://leicaboutique.co.za/used-leica-m-rangefinder-cameras',
]
session = requests.Session()
session.headers['User-Agent'] = UA
robots = {}
for url in URLS:
    parts = urlsplit(url)
    base = parts.scheme + '://' + parts.netloc
    try:
        if base not in robots:
            r = session.get(base + '/robots.txt', timeout=30)
            if r.status_code in (401, 403, 429):
                robots[base] = None
                print(base, 'robots blocked', r.status_code, flush=True)
                continue
            rp = RobotFileParser()
            rp.parse(r.text.splitlines() if r.status_code == 200 else [])
            robots[base] = rp
        rp = robots[base]
        if rp is None or not rp.can_fetch(UA, url):
            print(url, 'skipped', flush=True)
            continue
        time.sleep(8)
        r = session.get(url, timeout=40)
        print(url, r.status_code, len(r.content), r.headers.get('X-WP-TotalPages'), flush=True)
        if r.status_code in (401, 403, 429):
            robots[base] = None
    except requests.RequestException as exc:
        print(url, type(exc).__name__, flush=True)
