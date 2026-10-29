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
import math
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


def _link_gone(events, by_url, primary) -> dict:
    """사라진 매물은 검색 색인에 없어 모델을 모름 → 이벤트에 남은 제목·가격으로 분류기를 다시 돌려 링크 → 모델."""
    from entity_catalog import annotate_records
    from final_resolution_pipeline import classify_and_resolve_items

    seen, raw = set(), []
    for ev in events:
        link = ev.get("link")
        if ev.get("type") in ("gone", "sold") and link and link not in by_url and link not in seen:
            seen.add(link)
            raw.append({"site": ev.get("site"), "상품명": ev.get("title") or "", "가격": ev.get("price") or "",
                        "통화": ev.get("currency") or "", "링크": link})
    recs = classify_and_resolve_items(raw)
    annotate_records(recs)
    return {r["raw_item"]["링크"]: primary(r.get("entity_ids") or []) for r in recs}


def price_trend(ents, country, krw_per) -> dict:
    """나라별 가격 지수 (data/dealer/price_weekly.json → 첫 주 = 1).
    1) 모델마다 전 기간·전 판매처 가격(지금 환율, 원)의 중앙값을 기준으로 0.5~2배 밖 매물은 뺀다
       (특별판·잘못 연결된 매물 하나가 몇 달 걸려 있다가 빠지면 중앙값이 크게 흔들림 — 충무로 M6 2,580만 원, 2026-10-29).
    2) 주마다 그 나라 판매처 가운데 지난번 기록과 이번 주에 모두 있는 판매처만 비교해(판매처 통화 그대로)
       중앙값 비율의 가중 기하평균(가중치 = 두 주 매물 수 중 작은 쪽)을 곱해 나간다. 한 주 변화는 ±15%에서 자른다.
    새로 붙은 판매처·환율은 지수를 움직이지 않는다. 겹치는 판매처가 없는 주는 그대로 둔다."""
    path = D / "dealer/price_weekly.json"
    if not path.exists():
        return {"weeks": [], "e": {}, "lv": {}}
    hist = json.loads(path.read_text())
    weeks = sorted(hist["weeks"])
    cur_of = {}
    for w in weeks:
        cur_of.update(hist["weeks"][w].get("cur", {}))
    cap = math.log(1.15)
    out, level = {}, {}
    for eid in sorted({e for w in weeks for e in hist["weeks"][w]["e"]}):
        if eid not in ents:
            continue
        rows = [(i, site, p) for i, w in enumerate(weeks) for site, ps in hist["weeks"][w]["e"].get(eid, {}).items()
                if country(site) and krw_per.get(cur_of.get(site, "KRW")) for p in ps]
        if not rows:
            continue
        ref = statistics.median(p * krw_per[cur_of.get(s, "KRW")] for _, s, p in rows)
        cells = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))  # 주 → 나라 → 판매처 → 가격들
        for i, site, p in rows:
            if 0.5 <= p * krw_per[cur_of.get(site, "KRW")] / ref <= 2:
                cells[i][country(site)][site].append(p)
        by_c = defaultdict(list)
        prev, idx = {}, {}
        for i in sorted(cells):
            for c, sites in cells[i].items():
                cur = {s: (statistics.median(ps), len(ps)) for s, ps in sites.items()}
                if c in prev:
                    common = [s for s in cur if s in prev[c]]
                    wsum = sum(min(cur[s][1], prev[c][s][1]) for s in common)
                    if wsum:
                        logr = sum(min(cur[s][1], prev[c][s][1]) * math.log(cur[s][0] / prev[c][s][0]) for s in common) / wsum
                        idx[c] *= math.exp(max(-cap, min(cap, logr)))
                else:
                    idx[c] = 1.0
                by_c[c].append([i, round(idx[c], 4), sum(n for _, n in cur.values())])
                prev[c] = cur
        # 마지막 주 나라별 B등급 가격 수준(원, 지금 환율): 걸러낸 매물 가격의 중앙값
        last = cells.get(len(weeks) - 1, {})
        lv = {c: round(statistics.median(p * krw_per[cur_of.get(s, "KRW")] for s, ps in sites.items() for p in ps))
              for c, sites in last.items()}
        series = {c: v for c, v in by_c.items() if len(v) >= 2}
        if series:
            out[eid] = series
            level[eid] = lv
    return {"weeks": weeks, "e": out, "lv": level}


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
    # 사이트를 처음 본 날 이미 있던 매물은 올라온 날을 모르니 뺀다. 처음 볼 때 이미 판매완료였던 매물
    # (판매 끝난 물건을 목록에 남기는 매장)도 뺀다 — 2026-10-29 전엔 이 둘이 '0일'로 섞여 중간값이 0.0일이 됐음
    site_first = {}
    for it in listings:
        if it["fs"]:
            site_first[it["s"]] = min(site_first.get(it["s"], it["fs"]), it["fs"])
    for ev in events:
        if ev.get("type") == "new":
            site_first[ev["site"]] = min(site_first.get(ev["site"], ev["t"][:16]), ev["t"][:16])
    gone_eid = _link_gone(events, by_url, primary)
    turn_by = {}  # 링크 → (모델, 일)
    for ev in events:
        if ev.get("type") in ("gone", "sold") and ev.get("hours_to_sell") is not None:
            eid = (by_url.get(ev.get("link")) or {}).get("e") or gone_eid.get(ev.get("link"))
            t = parse_t(ev.get("t", ""))
            if not eid or not t:
                continue
            first = t - dt.timedelta(hours=ev["hours_to_sell"])
            if first.strftime("%Y-%m-%d") <= site_first.get(ev.get("site"), "")[:10]:
                continue
            turn_by[ev["link"]] = (eid, ev["hours_to_sell"] / 24)
    for it in listings:
        if it["e"] and it["sold"] and it["sa"] and it["fs"] and it["fs"][:10] > site_first.get(it["s"], "")[:10]:
            a, b = parse_t(it["fs"] + ":00"), parse_t(it["sa"] + ":00")
            if a and b and b > a:
                turn_by[it["u"]] = (it["e"], (b - a).total_seconds() / 86400)
    turn = defaultdict(list)
    for eid, days in turn_by.values():
        turn[eid].append(days)

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
        "trend": price_trend(ents, country, krw_per),
    }


if __name__ == "__main__":
    out = build()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    # mtime=0: 내용이 같으면 파일도 같게 (크롤링마다 쓸데없는 커밋이 안 생기게)
    OUT.write_bytes(gzip.compress(json.dumps(out, ensure_ascii=False, separators=(",", ":")).encode("utf-8"), 9, mtime=0))
    print(f"딜러 데이터: 모델 {len(out['entities'])} · 판매 중 {len(out['active'])} · 판매완료 {len(out['sold'])} · 변동 {len(out['feed'])}"
          f" → {OUT} {OUT.stat().st_size / 1e6:.2f}MB")
