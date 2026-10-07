"""data/fx_history.json 을 지난 날짜까지 채운다 (한 번 실행용, 다시 돌려도 안전).

1) git 기록의 data/fx_rates.json — 자동 크롤마다 저장된 값, 날마다 마지막 값
2) 그 전 날짜는 Frankfurter(유럽중앙은행) 기간 조회 — 대만 달러(TWD)는 없음
이미 있는 날짜는 덮어쓰지 않는다 (날마다 쌓인 실제 값을 우선).
"""
from __future__ import annotations

import datetime as dt
import json
import subprocess
import sys
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from fx_history import load_history, save_history  # noqa: E402

KST = dt.timezone(dt.timedelta(hours=9))
CURRENCIES = ["USD", "KRW", "JPY", "EUR", "GBP", "CNY", "TWD", "HKD", "BRL", "SGD"]
START = "2026-04-01"  # 가장 오래된 수집 기록 무렵


def _kst_day(value: str) -> str:
    try:
        return dt.datetime.fromisoformat(value).astimezone(KST).strftime("%Y-%m-%d")
    except ValueError:
        return value[:10]


def from_git() -> dict[str, dict[str, float]]:
    log = subprocess.run(["git", "log", "--format=%H", "--", "data/fx_rates.json"], cwd=ROOT,
                         capture_output=True, text=True, check=True).stdout.split()
    days: dict[str, dict[str, float]] = {}
    for sha in reversed(log):  # 오래된 것부터 → 같은 날은 마지막 값이 남음
        try:
            data = json.loads(subprocess.run(["git", "show", f"{sha}:data/fx_rates.json"], cwd=ROOT,
                                             capture_output=True, text=True, check=True).stdout)
        except (subprocess.CalledProcessError, ValueError):
            continue
        rates = {k: float(v) for k, v in (data.get("rates") or {}).items() if k in CURRENCIES and v}
        if rates.get("KRW"):
            days[_kst_day(str(data.get("fetched_at") or ""))] = rates
    return days


def from_frankfurter(start: str, end: str) -> dict[str, dict[str, float]]:
    symbols = ",".join(c for c in CURRENCIES if c not in ("USD", "TWD"))
    data = requests.get(f"https://api.frankfurter.dev/v1/{start}..{end}", params={"base": "USD", "symbols": symbols}, timeout=30).json()
    return {day: {**{k: float(v) for k, v in rates.items()}, "USD": 1.0} for day, rates in (data.get("rates") or {}).items()}


def main() -> None:
    days = dict(load_history())
    git_days = from_git()
    first_git = min(git_days) if git_days else dt.date.today().isoformat()
    ecb_end = (dt.date.fromisoformat(first_git) - dt.timedelta(days=1)).isoformat()
    ecb_days = from_frankfurter(START, ecb_end) if START <= ecb_end else {}
    added = 0
    for source in (git_days, ecb_days):
        for day, rates in source.items():
            if day not in days:
                days[day] = rates
                added += 1
    save_history(days)
    print(f"✅ 날짜별 환율 {len(days)}일 (새로 {added}일 · git {len(git_days)}일 · 유럽중앙은행 {len(ecb_days)}일)")


if __name__ == "__main__":
    main()
