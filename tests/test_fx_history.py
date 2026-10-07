import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import fx_history  # noqa: E402

_spec = importlib.util.spec_from_file_location("crawl_engine", ROOT / "app" / "crawl_engine.py")
ce = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(ce)

DAYS = {
    "2026-09-01": {"USD": 1.0, "KRW": 1300.0, "JPY": 140.0},
    "2026-10-01": {"USD": 1.0, "KRW": 1400.0, "JPY": 150.0},
}


def test_rates_on_uses_that_day_or_the_closest_earlier_day():
    assert fx_history.rates_on("2026-09-01 10:00:00", DAYS)["KRW"] == 1300.0
    assert fx_history.rates_on("2026-09-20", DAYS)["KRW"] == 1300.0  # 기록 없는 날 → 그 전 날
    assert fx_history.rates_on("2026-10-05", DAYS)["KRW"] == 1400.0
    assert fx_history.rates_on("2026-08-01", DAYS) is None  # 기록보다 이전


def test_krw_per_unit_on_sale_day():
    assert round(fx_history.krw_per_unit_on("JPY", "2026-09-15", DAYS), 4) == round(1300 / 140, 4)
    assert fx_history.krw_per_unit_on("KRW", "2026-09-15", DAYS) == 1.0
    assert fx_history.krw_per_unit_on("HKD", "2026-09-15", DAYS) is None


def _row(n, sold=False, currency="JPY", **extra):
    return {"site": "기타무라 (일본)", "링크": f"https://x/{n}", "상품명": f"item {n}", "가격": "¥100,000", "통화": currency, "품절": sold, **extra}


def test_sold_rows_keep_the_exchange_rate_of_the_moment(monkeypatch):
    monkeypatch.setattr(ce, "_FX_CACHE", {"USD": 1.0, "KRW": 1400.0, "JPY": 150.0})
    prev = [_row(1, first_seen="2026-10-01 09:00:00"), _row(2, first_seen="2026-10-01 09:00:00")]
    cur = [_row(1, sold=True), _row(2), _row(3, sold=True)]
    merged, events, _ = ce.merge_source(prev, {"site": "기타무라 (일본)", "ok": True, "rows": cur, "coverage": "full"}, "2026-10-07 11:00:00")
    sold = next(r for r in merged if r["링크"] == "https://x/1")
    assert sold["sold_at"] == "2026-10-07 11:00:00" and round(sold["sold_fx_krw"], 4) == round(1400 / 150, 4)
    assert "sold_at_unknown" not in sold
    first_seen_sold = next(r for r in merged if r["링크"] == "https://x/3")
    assert first_seen_sold["sold_at_unknown"] is True  # 처음 볼 때 이미 판매완료 → 실제 판매일 모름

    # 다음 실행: 환율이 바뀌어도 판매 때 환율이 그대로 남음
    monkeypatch.setattr(ce, "_FX_CACHE", {"USD": 1.0, "KRW": 1500.0, "JPY": 140.0})
    merged2, _, _ = ce.merge_source(merged, {"site": "기타무라 (일본)", "ok": True, "rows": cur, "coverage": "full"}, "2026-10-07 13:00:00")
    sold2 = next(r for r in merged2 if r["링크"] == "https://x/1")
    assert sold2["sold_at"] == "2026-10-07 11:00:00" and round(sold2["sold_fx_krw"], 4) == round(1400 / 150, 4)
    assert next(r for r in merged2 if r["링크"] == "https://x/3")["sold_at_unknown"] is True
