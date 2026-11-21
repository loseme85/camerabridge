"""수집 보강 시험 (읽기 전용): Shopify 매장의 설명·상품 종류·태그를 받아, 제목에는 없고 설명에만 있는 특징을 뽑는다.
결과는 out/store_meta_sim.json (저장소 데이터는 바꾸지 않음)."""
import html, json, re, sys, time, collections
from urllib.parse import urlparse
import requests
sys.path.insert(0, ".")
from body_buckets import traits_of

idx = json.load(open("data/derived/results_search_index_v1.json"))["records"]
by = {r["raw_item"].get("링크"): r for r in idx}
hosts = collections.Counter()
for link in by:
    if link and "/products/" in link:
        u = urlparse(link)
        hosts[f"{u.scheme}://{u.netloc}"] += 1
bases = [h for h, _ in hosts.most_common(30)]
out, stat = [], {}
S = requests.Session()
S.headers["User-Agent"] = "Mozilla/5.0 (compatible; CameraBridgeBot/1.0)"
for b in bases:
    n = 0
    status = "ok"
    for pg in range(1, 15):
        resp = None
        for wait in (0, 15, 45):
            time.sleep(wait)
            try:
                resp = S.get(f"{b}/products.json", params={"limit": 250, "page": pg}, timeout=40)
            except Exception as e:
                status = f"err {e}"[:60]; break
            if resp.status_code != 429:
                break
        if resp is None or resp.status_code != 200:
            status = status if resp is None else f"http {resp.status_code}"
            break
        ps = resp.json().get("products", [])
        if not ps:
            break
        for p in ps:
            n += 1
            link = f"{b}/products/{p['handle']}"
            r = by.get(link)
            if not r:
                continue
            desc = re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", p.get("body_html") or ""))).strip()[:500]
            t = set(traits_of(r["raw_item"].get("상품명")))
            d = set(traits_of(desc)) - t
            out.append(dict(site=r["raw_item"].get("site"), title=r["raw_item"].get("상품명"), link=link,
                            ents=r.get("entity_ids", []), cat=r["final_output"].get("category"),
                            price=r["final_output"].get("price_raw"), new=sorted(d), desc=desc,
                            ptype=p.get("product_type"), tags=p.get("tags")))
        time.sleep(4)
    stat[b] = dict(read=n, status=status)
    print(b, n, status, flush=True)
json.dump(out, open("out/store_meta_sim.json", "w"), ensure_ascii=False)
json.dump(stat, open("out/stat.json", "w"), ensure_ascii=False)
print("matched", len(out), "with new traits", sum(1 for x in out if x["new"]))
