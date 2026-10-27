"""딜러 화면 데이터: 카메라브릿지 수집 데이터 → data/dealer/dealer_data.json.gz

    python3 scripts/build_dealer_data.py [출력 .json.gz]

크롤링(crawl.yml)에서 build_entity_index.py 다음에 돌린다. 이 파일은 /dealer/data(로그인한 딜러)로만 내보내고,
주소로 직접 여는 것은 vercel.json에서 막는다.
금액은 모두 원(KRW)으로 맞춰 두고, 매장 나라 통화로 바꾸는 것은 화면이 환율로 한다.
나라별 기준가: 판매완료 가격을 등급 비율로 B등급에 맞춘 중앙값을 나라마다 따로 낸다 (sb). 판매 중 가격 기준은 화면이 계산한다.
신품(N)은 라이카 공식 정가(msrp, 나라별)를 먼저 쓴다.
"""
from __future__ import annotations

import datetime as dt
import gzip
import json
import statistics
import sys
from collections import defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))

from condition_grade import grade_of  # noqa: E402

D = REPO / "data"
OUT = Path(sys.argv[1]) if len(sys.argv) > 1 else D / "dealer/dealer_data.json.gz"
FEED_DAYS = 14


def parse_t(s):
    try:
        return dt.datetime.strptime(s[:19], "%Y-%m-%d %H:%M:%S")
    except (TypeError, ValueError):
        return None


def build() -> dict:
    recs = json.loads((D / "derived/results_search_index_v1.json").read_text())["records"]
    summary = json.loads((D / "derived/entity_summary_v1.json").read_text())
    rules = json.loads((D / "config/landed_cost_rules.json").read_text())
    fx = json.loads((D / "fx_rates.json").read_text())
    rates = fx["rates"]
    krw_per = {c: rates["KRW"] / v for c, v in rates.items()}  # 1 통화 = ? 원
    factors = summary["grade_factors"]
    ents = {e["id"]: e for e in summary["entities"]}
    now = dt.datetime.strptime(summary["generated_at"][:19], "%Y-%m-%dT%H:%M:%S") + dt.timedelta(hours=9)  # KST

    def country(site):
        return (rules["sources"].get(site) or {}).get("country")

    def primary(eids):
        leaf = [e for e in eids if e in ents and not ents[e].get("children")]
        return (leaf or [e for e in eids if e in ents] or [None])[0]

    def fac(eid, g):
        if g == "X":
            return None
        tbl = factors.get(ents[eid].get("kind")) or factors["Lens"]
        return tbl.get(g or "B", 1.0)

    # ── 매물 ──
    listings, by_url = [], {}
    for r in recs:
        f = r["final_output"]
        price = f.get("parsed_price_numeric")
        cur = (f.get("currency") or "KRW").upper()
        site = f.get("source")
        if not price or cur not in krw_per:
            continue
        krw = price * (f["sold_fx_krw"] if f.get("sold_fx_krw") and cur != "KRW" else krw_per[cur])
        eid = primary(r.get("entity_ids") or [])
        grade, _ = grade_of(site, f.get("condition_raw"), f.get("title_raw"))
        img = f.get("image_url") or ""
        item = {
            "e": eid, "s": site, "t": f.get("title_raw"), "p": price, "c": cur, "k": round(krw),
            "g": grade, "fs": (f.get("first_seen") or "")[:16], "u": f.get("source_url"),
            "img": img if img.startswith("http") and not img.endswith(".svg") else None,
            "kind": f.get("category"), "cond": f.get("condition_raw"),
            "sold": f.get("sold_quality") == "sold_confirmed", "sa": (f.get("sold_at") or "")[:16] or None,
        }
        listings.append(item)
        by_url[item["u"]] = item

    # ── 나라별 판매완료 기준가 (B 등급) ──
    sold_b = defaultdict(lambda: defaultdict(list))
    for it in listings:
        if not it["e"] or not it["sold"]:
            continue
        f_ = fac(it["e"], it["g"])
        if not f_:
            continue
        sold_b[it["e"]]["ALL"].append(it["k"] / f_)
        if country(it["s"]):
            sold_b[it["e"]][country(it["s"])].append(it["k"] / f_)

    # ── 회전 속도: 이벤트(gone/sold의 hours_to_sell) + sold_at 있는 매물 ──
    events = []
    for path in sorted((D / "history").glob("events_*.jsonl")):
        events += [json.loads(line) for line in path.read_text().splitlines() if line.strip()]
    turn = defaultdict(list)
    for ev in events:
        if ev.get("type") in ("gone", "sold") and ev.get("hours_to_sell") is not None:
            it = by_url.get(ev.get("link"))
            if it and it["e"]:
                turn[it["e"]].append(ev["hours_to_sell"] / 24)
    for it in listings:
        if it["e"] and it["sold"] and it["sa"] and it["fs"]:
            a, b = parse_t(it["fs"] + ":00"), parse_t(it["sa"] + ":00")
            if a and b and b >= a:
                turn[it["e"]].append((b - a).total_seconds() / 86400)

    # ── 나라별 공식 신품 정가 (scripts/update_leica_msrp.py, 매일 조금씩) ──
    # 같은 모델에 번호가 여럿이면(블랙·실버 등) 나라마다 가장 낮은 값
    msrp = defaultdict(dict)
    msrp_path = D / "config/leica_msrp.json"
    msrp_data = json.loads(msrp_path.read_text()) if msrp_path.exists() else {"prices": {}}
    catalog = json.loads((D / "config/entity_catalog_v1.json").read_text())
    owner = {code: e["id"] for e in catalog["entities"] for code in (e.get("codes") or [])}
    for code, by_country in msrp_data["prices"].items():
        eid = owner.get(code)
        for c, (price, cur, *_) in by_country.items():
            if eid and cur in krw_per:
                krw = round(price * krw_per[cur])
                msrp[eid][c] = min(msrp[eid].get(c, krw), krw)

    # ── 모델 표 ──
    used = {it["e"] for it in listings if it["e"]}
    entities = {}
    for eid in used:
        e = ents[eid]
        sb = {}
        for c, vals in sold_b[eid].items():
            sb[c] = [round(statistics.median(vals)) if len(vals) >= 2 else None, len(vals)]
        entities[eid] = {
            "n": e["name"], "ko": e.get("name_ko"), "kind": e.get("kind"), "mount": e.get("mount"),
            "parent": e.get("parent"), "al": e.get("aliases", [])[:8], "sb": sb, "msrp": msrp.get(eid) or None,
            "turnD": round(statistics.median(turn[eid]), 1) if len(turn[eid]) >= 2 else None,
            "turnN": len(turn[eid]),
        }

    # ── 최근 변동 ──
    cut = now - dt.timedelta(days=FEED_DAYS)
    feed = []
    for ev in events:
        t = parse_t(ev.get("t", ""))
        if not t or t < cut or ev.get("type") not in ("new", "price", "gone", "sold"):
            continue
        it = by_url.get(ev.get("link"))
        feed.append({
            "ty": ev["type"], "t": ev["t"][:16], "s": ev.get("site"), "ti": ev.get("title"),
            "p": ev.get("price"), "pp": ev.get("prev_price"), "u": ev.get("link"),
            "e": it["e"] if it else None, "h": ev.get("hours_to_sell"),
        })
    feed.sort(key=lambda x: x["t"], reverse=True)

    active = [it for it in listings if not it["sold"]]
    sold = sorted([it for it in listings if it["sold"] and it["e"]], key=lambda x: x["sa"] or x["fs"], reverse=True)
    for it in sold:
        it.pop("img", None)

    sites = defaultdict(lambda: {"act": 0, "sold": 0})
    for it in listings:
        sites[it["s"]]["sold" if it["sold"] else "act"] += 1

    return {
        "generated": now.strftime("%Y-%m-%d %H:%M"),
        "fx": {"rates": {c: round(v, 6) for c, v in krw_per.items()}, "at": fx.get("fetched_at", "")[:10]},
        "factors": factors,
        "sites": {s: {**v, "country": country(s)} for s, v in sites.items()},
        "entities": entities,
        "active": active,
        "sold": sold[:3000],
        "feed": feed[:2000],
        "eventsFrom": min((e["t"] for e in events), default="")[:10],
        "msrpAt": (msrp_data.get("updated_at") or "")[:10],
    }


if __name__ == "__main__":
    out = build()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    # mtime=0: 내용이 같으면 파일도 같게 (크롤링마다 쓸데없는 커밋이 안 생기게)
    OUT.write_bytes(gzip.compress(json.dumps(out, ensure_ascii=False, separators=(",", ":")).encode("utf-8"), 9, mtime=0))
    print(f"딜러 데이터: 모델 {len(out['entities'])} · 판매 중 {len(out['active'])} · 판매완료 {len(out['sold'])} · 변동 {len(out['feed'])}"
          f" → {OUT} {OUT.stat().st_size / 1e6:.2f}MB")
