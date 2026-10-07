"""날짜별 환율 기록 (data/fx_history.json).

판매 완료가를 원화 등으로 바꿀 때 '오늘 환율'이 아니라 '팔린 날 환율'을 쓰기 위해 날마다 환율을 쌓아 둔다.
형식: {"base": "USD", "days": {"2026-10-07": {"KRW": 1380.1, "JPY": 150.2, ...}}}  (1 USD 당 통화 단위)
그날 기록이 없으면 그 전 가장 가까운 날 환율을 쓴다.
"""
from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path

HISTORY_PATH = Path(__file__).resolve().parent / "data" / "fx_history.json"


@lru_cache(maxsize=1)
def load_history(path: str | None = None) -> dict[str, dict[str, float]]:
    try:
        data = json.loads(Path(path or HISTORY_PATH).read_text(encoding="utf-8"))
        return dict(sorted((data.get("days") or {}).items()))
    except Exception:
        return {}


def save_history(days: dict[str, dict[str, float]], path: str | None = None) -> None:
    out = {"base": "USD", "days": dict(sorted(days.items()))}
    Path(path or HISTORY_PATH).write_text(json.dumps(out, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    load_history.cache_clear()


def upsert_day(day: str, rates: dict[str, float], path: str | None = None) -> None:
    days = dict(load_history(path))
    days[day] = {code: float(value) for code, value in rates.items() if value}
    save_history(days, path)


def rates_on(when: str | None, days: dict[str, dict[str, float]] | None = None) -> dict[str, float] | None:
    """그날(없으면 그 전 가장 가까운 날) 환율. 기록보다 이전 날짜면 None."""
    days = load_history() if days is None else days
    if not when or not days:
        return None
    day = str(when)[:10]
    best = None
    for key in days:  # 날짜순
        if key <= day:
            best = key
        else:
            break
    return days.get(best) if best else None


def krw_per_unit_on(currency: str | None, when: str | None, days: dict[str, dict[str, float]] | None = None) -> float | None:
    """그날 환율로 통화 1단위 = 몇 원."""
    code = str(currency or "KRW").strip().upper()
    if code == "KRW":
        return 1.0
    rates = rates_on(when, days)
    if not rates or not rates.get(code) or not rates.get("KRW"):
        return None
    return rates["KRW"] / rates[code]
