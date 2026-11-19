import json, os, sys
sys.path.insert(0, ".")
os.makedirs("out", exist_ok=True)
import app.test as t
rows = t.crawl_leicamiami()
json.dump(rows, open("out/site_rows_miami.json", "w"), ensure_ascii=False)
print(len(rows))
