"""모델·판매처별 주간 가격 기록 → data/dealer/price_weekly.json (딜러 화면의 가격 추이)

    python3 scripts/build_price_history.py              # 지금 수집분으로 이번 주 칸을 덮어씀 (crawl.yml, build_dealer_data.py 앞)
    python3 scripts/build_price_history.py --backfill   # git에 남은 지난 크롤 결과(2026-04~)로 주마다 다시 만듦

주마다 그 주 마지막 크롤의 판매 중 매물을 모델·판매처별로 묶어 B등급 환산 가격들을 남긴다.
가격은 판매처 통화 그대로 둔다 — 추이는 판매처 안에서 지난주와 비교해 이어 붙이므로(build_dealer_data.py)
환율 변동과 새로 붙은 판매처가 '가격 변화'로 섞이지 않는다.
이 파일은 data/dealer/ 아래라 주소로 직접 열 수 없다 (vercel.json).
"""
from __future__ import annotations

import datetime as dt
import json
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))

from condition_grade import grade_of  # noqa: E402
from search_index import parse_price_numeric  # noqa: E402

D = REPO / "data"
OUT = D / "dealer/price_weekly.json"
RAW = "data/raw/results.json"
BACKFILL_FROM = dt.date(2026, 4, 13)  # data/raw/results.json이 git에 처음 들어온 주


def week_of(day: dt.date) -> str:
    """그 주 월요일 (KST 날짜 기준)."""
    return (day - dt.timedelta(days=day.weekday())).isoformat()


def load_context():
    summary = json.loads((D / "derived/entity_summary_v1.json").read_text())
    ents = {e["id"]: e for e in summary["entities"]}
    return ents, summary["grade_factors"]


def primary(eids, ents):
    # build_dealer_data.py와 같은 규칙: 세부 모델이 있으면 가장 아래 모델
    leaf = [e for e in eids if e in ents and not ents[e].get("children")]
    return (leaf or [e for e in eids if e in ents] or [None])[0]


def _sig(x: float) -> float:
    """유효숫자 3자리 (파일 크기를 줄임, 추이에는 충분)."""
    return float(f"{x:.3g}")


def week_entry(records, ents, factors, at: str) -> dict:
    """검색 색인 형식 레코드(final_output + entity_ids) → {"at", "e": {모델: {판매처: [B등급 환산 가격, ...]}}, "cur": {판매처: 통화}}."""
    groups: dict[str, dict[str, list[float]]] = {}
    cur_of: dict[str, str] = {}
    for r in records:
        f = r["final_output"]
        if f.get("sold_quality") == "sold_confirmed" or (r.get("raw_item") or {}).get("품절"):
            continue
        # 지난 크롤 결과를 다시 분류한 레코드에는 숫자 가격이 없음 → 검색 색인과 같은 방법으로 뽑음
        price = f.get("parsed_price_numeric") or parse_price_numeric(f.get("price_raw"))
        eid = primary(r.get("entity_ids") or [], ents)
        if not price or not eid or ents[eid].get("kind") not in ("Body", "Lens"):
            continue
        site = f.get("source")
        grade, _ = grade_of(site, f.get("condition_raw"), f.get("title_raw"))
        if grade == "X":
            continue
        # 등급을 모르면 B로 본다 — 판매처 안에서만 비교하므로 판매처마다 일정하게 섞임
        price_b = price / (factors.get(ents[eid]["kind"]) or {}).get(grade or "B", 1.0)
        groups.setdefault(eid, {}).setdefault(site, []).append(price_b)
        cur_of[site] = (f.get("currency") or "KRW").upper()
    e = {eid: {s: sorted(_sig(x) for x in v) for s, v in sorted(by.items())} for eid, by in sorted(groups.items())}
    return {"at": at, "e": e, "cur": dict(sorted(cur_of.items()))}


def load_out() -> dict:
    if OUT.exists():
        return json.loads(OUT.read_text())
    return {"_설명": "scripts/build_price_history.py가 만든다. weeks[월요일].e[모델][판매처] = 판매 중 매물의 B등급 환산 가격들(판매처 통화)",
            "weeks": {}}


def save(out: dict) -> None:
    out["weeks"] = dict(sorted(out["weeks"].items()))
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(out, ensure_ascii=False, separators=(",", ":")) + "\n")
    print(f"  📈 가격 기록 {len(out['weeks'])}주 → {OUT.relative_to(REPO)}")


def update_current() -> None:
    ents, factors = load_context()
    idx = json.loads((D / "derived/results_search_index_v1.json").read_text())
    at = (dt.datetime.strptime(idx["generated_at"][:19], "%Y-%m-%dT%H:%M:%S") + dt.timedelta(hours=9))
    out = load_out()
    out["weeks"][week_of(at.date())] = week_entry(idx["records"], ents, factors, at.strftime("%Y-%m-%d %H:%M"))
    save(out)


def git(*args) -> str:
    return subprocess.run(["git", *args], cwd=REPO, capture_output=True, text=True, check=True).stdout


def backfill() -> None:
    from entity_catalog import annotate_records
    from final_resolution_pipeline import classify_and_resolve_items

    ents, factors = load_context()
    out = load_out()
    # 주마다 그 주 마지막 크롤 커밋 (커밋 시각은 KST로)
    last: dict[str, tuple[str, str]] = {}
    for line in git("log", "--reverse", "--format=%H %cI", "--", RAW).splitlines():
        sha, when = line.split()
        t = dt.datetime.fromisoformat(when).astimezone(dt.timezone(dt.timedelta(hours=9)))
        if t.date() >= BACKFILL_FROM:
            last[week_of(t.date())] = (sha, t.strftime("%Y-%m-%d %H:%M"))
    this_week = week_of(dt.date.today())
    for wk, (sha, at) in sorted(last.items()):
        if wk == this_week:
            continue  # 이번 주는 update_current가 채움
        items = json.loads(git("show", f"{sha}:{RAW}"))
        live = [x for x in items if not x.get("품절")]
        recs = classify_and_resolve_items(live)
        annotate_records(recs)
        out["weeks"][wk] = week_entry(recs, ents, factors, at)
        print(f"  {wk} ({at}) 판매 중 {len(live)} → 모델 {len(out['weeks'][wk]['e'])}개")
    save(out)


if __name__ == "__main__":
    if "--backfill" in sys.argv:
        backfill()
    update_current()
