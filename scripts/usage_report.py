"""사용 기록 요약: api/usage.py 가 Blob 에 쌓은 방문 묶음을 읽어 주간 요약을 낸다.

    vercel env pull .env.local            # BLOB_READ_WRITE_TOKEN 받기 (처음 한 번)
    python3 scripts/usage_report.py              # 최근 7일
    python3 scripts/usage_report.py --days 30
    python3 scripts/usage_report.py --since 2026-10-04 --json

방문 수·나라·기기는 Vercel 프로젝트 화면 Analytics 에서 본다. 여기서는 검색·클릭만.
"""
from __future__ import annotations

import argparse
import collections
import datetime as dt
import json
import os
from pathlib import Path

KST = dt.timezone(dt.timedelta(hours=9))


def load_token() -> None:
    if os.environ.get("BLOB_READ_WRITE_TOKEN"):
        return
    env = Path(__file__).resolve().parent.parent / ".env.local"
    if env.exists():
        for line in env.read_text().splitlines():
            if line.startswith("BLOB_READ_WRITE_TOKEN="):
                os.environ["BLOB_READ_WRITE_TOKEN"] = line.split("=", 1)[1].strip().strip('"')


def fetch(days: list[str]) -> list[dict]:
    from vercel import blob

    entries = []
    for day in days:
        for item in blob.iter_objects(prefix=f"usage/{day}/"):
            try:
                entries.append(json.loads(blob.get(item.url, access="private").content))
            except Exception as error:  # noqa: BLE001
                print(f"읽기 실패 {item.pathname}: {error}")
    return entries


def summarize(entries: list[dict]) -> dict:
    sessions = {e["sid"] for e in entries}
    searches = [s for e in entries for s in e.get("searches", [])]
    clicks = [c for e in entries for c in e.get("clicks", [])]
    first = {}
    for e in sorted(entries, key=lambda e: e.get("part", 1)):
        first.setdefault(e["sid"], e)
    norm = lambda q: " ".join(str(q).lower().split())  # noqa: E731
    return {
        "visits_with_activity": len(sessions),
        "visits_with_click": len({e["sid"] for e in entries if e.get("clicks")}),
        "searches": len(searches),
        "clicks": len(clicks),
        "referrers": collections.Counter(e.get("referrer") or "(직접·알 수 없음)" for e in first.values()).most_common(10),
        "locales": collections.Counter(e.get("locale") or "-" for e in first.values()).most_common(10),
        "mobile_share": round(sum(1 for e in first.values() if e.get("mobile")) / len(first), 2) if first else None,
        "top_queries": collections.Counter(norm(s["q"]) for s in searches).most_common(20),
        "top_entities": collections.Counter(s["entity"] for s in searches if s.get("entity")).most_common(15),
        "zero_result_queries": collections.Counter(norm(s["q"]) for s in searches if s.get("results") == 0).most_common(20),
        "no_active_queries": collections.Counter(norm(s["q"]) for s in searches if s.get("results") and s.get("active") == 0).most_common(20),
        "free_text_share": round(sum(1 for s in searches if not s.get("entity")) / len(searches), 2) if searches else None,
        "click_hosts": collections.Counter(c["host"] for c in clicks).most_common(10),
    }


def print_report(start: str, end: str, r: dict) -> None:
    print(f"# 사용 기록 {start} ~ {end} (KST)\n")
    print(f"- 검색·클릭한 방문 {r['visits_with_activity']} · 판매처까지 간 방문 {r['visits_with_click']}")
    print(f"- 검색 {r['searches']} (모델 안 고르고 그대로 검색 {r['free_text_share']}) · 판매처 클릭 {r['clicks']} · 휴대폰 {r['mobile_share']}")
    sections = [
        ("어디서 왔나", "referrers"), ("화면 언어", "locales"), ("많이 찾은 검색어", "top_queries"),
        ("많이 고른 모델", "top_entities"), ("결과 0건 검색어 → 고칠 것", "zero_result_queries"),
        ("판매 중 0건 검색어", "no_active_queries"), ("클릭한 판매처", "click_hosts"),
    ]
    for title, key in sections:
        print(f"\n## {title}")
        for name, count in r[key] or [("(없음)", "")]:
            print(f"- {name} {count}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--days", type=int, default=7)
    parser.add_argument("--since", help="YYYY-MM-DD (KST)")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    today = dt.datetime.now(KST).date()
    start = dt.date.fromisoformat(args.since) if args.since else today - dt.timedelta(days=args.days - 1)
    days = [str(start + dt.timedelta(days=i)) for i in range((today - start).days + 1)]
    load_token()
    report = summarize(fetch(days))
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print_report(days[0], days[-1], report)


if __name__ == "__main__":
    main()
