"""매일 환율을 받아 data/fx_rates.json 에 저장한다 (화면의 통화 환산·예상 총액용).

1순위 open.er-api.com (대만 달러 포함), 실패하면 frankfurter(ECB, 대만 달러 없음).
둘 다 실패하면 기존 파일을 그대로 둔다.
"""
from __future__ import annotations

import datetime as dt
import json
from pathlib import Path

import requests

OUT_PATH = Path(__file__).resolve().parents[1] / "data" / "fx_rates.json"
CURRENCIES = ["USD", "KRW", "JPY", "EUR", "GBP", "CNY", "TWD", "HKD", "BRL", "SGD"]


def _from_open_er_api() -> dict:
    data = requests.get("https://open.er-api.com/v6/latest/USD", timeout=20).json()
    if data.get("result") != "success":
        raise ValueError(f"open.er-api result={data.get('result')}")
    return {
        "provider": "ExchangeRate-API (open.er-api.com)",
        "provider_url": "https://www.exchangerate-api.com",
        "source_updated_at": data.get("time_last_update_utc"),
        "rates": data["rates"],
    }


def _from_frankfurter() -> dict:
    data = requests.get("https://api.frankfurter.dev/v1/latest?base=USD", timeout=20).json()
    rates = dict(data["rates"])
    rates["USD"] = 1.0
    return {
        "provider": "Frankfurter (European Central Bank)",
        "provider_url": "https://frankfurter.dev",
        "source_updated_at": data.get("date"),
        "rates": rates,
    }


def main() -> None:
    for fetch in (_from_open_er_api, _from_frankfurter):
        try:
            payload = fetch()
            break
        except Exception as exc:  # noqa: BLE001 - 다음 출처로 넘어감
            print(f"⚠️ 환율 {fetch.__name__} 실패: {exc}")
    else:
        print("❌ 환율 갱신 실패, 기존 파일 유지")
        return

    rates = {code: float(payload["rates"][code]) for code in CURRENCIES if code in payload["rates"]}
    out = {
        "base": "USD",
        "fetched_at": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
        "provider": payload["provider"],
        "provider_url": payload["provider_url"],
        "source_updated_at": payload["source_updated_at"],
        "rates": rates,
    }
    OUT_PATH.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"✅ 환율 갱신: {len(rates)}개 통화 ({payload['provider']})")


if __name__ == "__main__":
    main()
