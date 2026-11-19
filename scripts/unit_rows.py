import json, os, sys
sys.path.insert(0, ".")
os.makedirs("out", exist_ok=True)
import app.test as t
rows = t.crawl_unit()
json.dump(rows, open("out/site_rows_unit.json", "w"), ensure_ascii=False)
print(len(rows))
