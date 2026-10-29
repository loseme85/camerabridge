import datetime as dt
import json

from scripts import build_dealer_data
from scripts.build_price_history import week_of

ENTS = {"leica:body:m3:standard": {"kind": "Body"}}
COUNTRY = {"충무로": "KR", "사진집": "KR", "Ffordes": "GB"}.get
KRW = {"KRW": 1.0, "GBP": 1800.0}


def trend(tmp_path, monkeypatch, weeks):
    (tmp_path / "dealer").mkdir()
    cur = {"충무로": "KRW", "사진집": "KRW", "Ffordes": "GBP"}
    payload = {"weeks": {w: {"at": w, "e": {"leica:body:m3:standard": e}, "cur": cur} for w, e in weeks.items()}}
    (tmp_path / "dealer/price_weekly.json").write_text(json.dumps(payload, ensure_ascii=False))
    monkeypatch.setattr(build_dealer_data, "D", tmp_path)
    return build_dealer_data.price_trend(ENTS, COUNTRY, KRW)


def test_week_of_is_monday():
    assert week_of(dt.date(2026, 10, 29)) == "2026-10-26"
    assert week_of(dt.date(2026, 10, 26)) == "2026-10-26"


def test_same_shop_price_change_moves_index_new_shop_does_not(tmp_path, monkeypatch):
    out = trend(tmp_path, monkeypatch, {
        "2026-10-12": {"충무로": [3000000.0]},
        "2026-10-19": {"충무로": [3300000.0], "사진집": [5000000.0]},  # 충무로 +10%, 사진집은 새로 붙음
        "2026-10-26": {"충무로": [3300000.0], "사진집": [5000000.0]},
    })
    kr = out["e"]["leica:body:m3:standard"]["KR"]
    assert [round(v, 2) for _, v, _ in kr] == [1.0, 1.1, 1.1]
    assert [n for _, _, n in kr] == [1, 2, 2]


def test_outlier_listing_is_dropped(tmp_path, monkeypatch):
    # 2,580만 원짜리 한 대가 걸려 있다 빠져도 지수가 흔들리지 않음 (충무로 M6, 2026-10-29)
    out = trend(tmp_path, monkeypatch, {
        "2026-10-05": {"충무로": [3000000.0, 25800000.0]},
        "2026-10-12": {"충무로": [3000000.0, 25800000.0]},
        "2026-10-19": {"충무로": [3000000.0]},
    })
    assert [v for _, v, _ in out["e"]["leica:body:m3:standard"]["KR"]] == [1.0, 1.0, 1.0]


def test_weekly_move_is_capped_and_countries_are_separate(tmp_path, monkeypatch):
    out = trend(tmp_path, monkeypatch, {
        "2026-10-12": {"충무로": [3000000.0], "Ffordes": [1500.0]},
        "2026-10-19": {"충무로": [3900000.0], "Ffordes": [1500.0]},  # 한 주에 +30% → +15%까지만
    })
    series = out["e"]["leica:body:m3:standard"]
    assert series["KR"][-1][1] == 1.15
    assert series["GB"][-1][1] == 1.0
    assert out["lv"]["leica:body:m3:standard"] == {"KR": 3900000, "GB": 2700000}
