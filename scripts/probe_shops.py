"""매장 연락 이메일 조사 (2026-11-13 밤샘, 한 번만): shops_list.json의 매장마다 첫 화면·연락처·법적 고지 화면을 읽어
이메일·문의 양식 주소를 probe_contacts.json으로 남긴다. 공개 화면만 읽고 양식을 보내지 않는다. site-test 브랜치에서만 씀."""
from __future__ import annotations

import json
import re
import time
from urllib.parse import urljoin, urlparse

import requests

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36"
EMAIL = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)*\.[A-Za-z]{2,}")
JUNK = re.compile(r"\.(png|jpe?g|gif|webp|svg|css|js)$|sentry|example|domain\.com|wixpress|shopify|godo\.co\.kr|design102|cafe24|"
                  r"makeshop|@2x|yourname|youremail|email@|name@|test@|noreply|no-reply|privacy@leica|user@|johndoe|wordpress|"
                  r"schema\.org|w3\.org|jquery|bootstrap|@media|@font|@import|@keyframes", re.I)
LINK_WORDS = re.compile(r"contact|kontakt|contatt|contacto|お問い?合わせ|問合|inquiry|toiawase|impressum|imprint|mentions|legal|note-legali|"
                        r"tokutei|law|特定商|会社概要|company|about|chi-siamo|om-oss|o-nas|kontakty|문의|회사소개|이용안내|shopinfo", re.I)
FORM_WORDS = re.compile(r"contact|kontakt|contatt|お問い?合わせ|inquiry|toiawase|문의", re.I)
PATHS = ["/pages/contact", "/contact", "/contact-us", "/kontakt", "/impressum", "/pages/impressum", "/legal", "/policies/contact-information",
         "/policies/legal-notice", "/mentions-legales", "/contatti", "/law", "/shop/law_info.html", "/company"]


def fetch(sess, url):
    for attempt in range(3):
        try:
            r = sess.get(url, timeout=20)
        except Exception as e:  # noqa: BLE001
            return None, f"error {e.__class__.__name__}"
        if r.status_code == 429:
            time.sleep(min(int(r.headers.get("Retry-After") or 0) or 15 * (attempt + 1), 60))
            continue
        if not r.ok:
            return None, str(r.status_code)
        try:
            text = r.content.decode(r.apparent_encoding or "utf-8", errors="replace") if not r.encoding or r.encoding.lower() == "iso-8859-1" else r.text
        except Exception:  # noqa: BLE001
            text = r.text
        return text, "200"
    return None, "429"


def emails_in(html):
    found = []
    for m in EMAIL.finditer(html.replace("&#64;", "@").replace("%40", "@").replace("[at]", "@").replace("(at)", "@")):
        e = m.group(0).strip(".").lower()
        if not JUNK.search(e) and e not in found:
            found.append(e)
    return found


def probe(shop):
    base = shop["base"]
    sess = requests.Session()
    sess.headers["User-Agent"] = UA
    out = {**shop, "emails": {}, "forms": [], "status": {}}
    host = urlparse(base).netloc.replace("www.", "")
    home, st = fetch(sess, base)
    out["status"]["home"] = st
    pages = []
    if home:
        for e in emails_in(home):
            out["emails"].setdefault(e, base)
        for href, label in re.findall(r'<a[^>]+href="([^"#]+)"[^>]*>(.*?)</a>', home, re.I | re.S):
            label = re.sub(r"<[^>]+>", " ", label)
            if LINK_WORDS.search(href + " " + label):
                url = urljoin(base, href)
                if urlparse(url).netloc.replace("www.", "") == host and url not in pages:
                    pages.append(url)
                if FORM_WORDS.search(href + " " + label) and url not in out["forms"]:
                    out["forms"].append(url)
    for path in PATHS:
        url = urljoin(base, path)
        if url not in pages:
            pages.append(url)
    for url in pages[:9]:
        time.sleep(1)
        html, st = fetch(sess, url)
        out["status"][url] = st
        if html:
            for e in emails_in(html):
                out["emails"].setdefault(e, url)
            if re.search(r"<form[^>]*>", html, re.I) and FORM_WORDS.search(url) and url not in out["forms"]:
                out["forms"].append(url)
        if out["emails"]:
            break
    out["forms"] = out["forms"][:3]
    return out


def main():
    shops = [s for s in json.load(open("shops_list.json", encoding="utf-8")) if s.get("base")]
    results = []
    for i, shop in enumerate(shops, 1):
        try:
            r = probe(shop)
        except Exception as e:  # noqa: BLE001
            r = {**shop, "error": str(e)}
        results.append(r)
        print(i, shop["source"], list(r.get("emails", {}))[:3], (r.get("forms") or [""])[0], flush=True)
        json.dump(results, open("probe_contacts.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()
