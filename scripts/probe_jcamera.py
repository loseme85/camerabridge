"""J-カメラ가 GitHub 서버에서 다시 열리는지 읽기 전용 시험 (수집기를 직접 한 번 돌려 개수만 봄, 데이터 저장 안 함)"""
import json, os, sys, time
sys.path.insert(0, "."); sys.path.insert(0, "app")
os.environ["GITHUB_ACTIONS"] = "1"
import importlib.util
spec = importlib.util.spec_from_file_location("t", "app/test.py"); t = importlib.util.module_from_spec(spec); spec.loader.exec_module(t)
t0 = time.time()
try:
    rows = t.crawl_jcamera()
    out = {"ok": True, "rows": len(rows), "sec": round(time.time() - t0), "sample": [(r["상품명"], r["가격"], r["링크"]) for r in rows[:5]],
           "sites": sorted({r.get("원본매장") or r.get("shop") or "" for r in rows})[:10]}
except Exception as e:
    out = {"ok": False, "error": f"{type(e).__name__}: {e}"[:300], "sec": round(time.time() - t0)}
os.makedirs("out", exist_ok=True); json.dump(out, open("out/jcamera.json", "w"), ensure_ascii=False, indent=1)
print(json.dumps(out, ensure_ascii=False)[:800])
