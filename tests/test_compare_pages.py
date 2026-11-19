"""비교 페이지 (2026-11-19): 한글 사양 값은 다른 언어에 안 보이고, 쌍은 둘 다 페이지가 있을 때만"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import build_model_pages as bmp  # noqa: E402


def test_spec_value_hides_korean_outside_ko():
    assert bmp.spec_value("shutter", "기계식 천 셔터", "en") is None
    assert bmp.spec_value("shutter", "기계식 천 셔터", "ko") == "기계식 천 셔터"
    assert bmp.spec_value("weight_g", 734, "de") == "734 g"
    assert bmp.spec_value("sensor_mp", 60, "en") == "60 MP"
    assert bmp.spec_value("flash_ttl", False, "ja") == "なし"
    assert bmp.spec_value("note", "", "en") is None


def test_short_name_and_slug():
    assert bmp.short_name("Leica Q2", "Leica Q3") == "Q3"
    assert bmp.short_name("라이카 M6", "라이카 M7") == "M7"
    assert bmp.short_name("Leica M10", "Summilux") == "Summilux"
    assert bmp.compare_slug("q2", "q3") == "compare/q2-vs-q3"


def test_every_language_has_compare_texts():
    keys = set(bmp.C["en"])
    for lang in bmp.LANGS:
        assert set(bmp.C[lang]) == keys, lang
        assert set(bmp.C[lang]["f"]) >= set(bmp.COMPARE_FIELDS), lang


def test_pairs_are_unique():
    assert len(set(bmp.COMPARE_PAIRS)) == len(bmp.COMPARE_PAIRS)
    assert all(a != b for a, b in bmp.COMPARE_PAIRS)


def test_compare_trend_scales_to_today_and_needs_samples():
    weeks = ["2026-09-28", "2026-10-05", "2026-10-12", "2026-11-02", "2026-11-16"]
    a = [[0, 1.0, 1], [1, 1.0, 5], [2, 1.1, 5], [3, 1.0, 5], [4, 0.8, 6]]
    b = [[1, 1.0, 4], [2, 1.0, 4], [3, 1.0, 4], [4, 1.0, 4]]
    pts = bmp.compare_trend(a, b, weeks, 800.0, 1000.0)
    assert [w for w, _, _ in pts] == ["2026-10-05", "2026-11-02", "2026-11-16"]  # 9월 주는 A 매물 1개라 뺌, 달마다 첫 주 + 마지막 주
    assert pts[-1][1:] == (800.0, 1000.0)  # 마지막 = 지금 B등급 시세
    assert round(pts[0][1]) == 1000  # A는 0.8로 내려옴 → 10월 초 추정 1000
    assert bmp.compare_trend(a[:1], b, weeks, 1, 1) == []


def test_trend_texts_every_language():
    for lang in bmp.LANGS:
        assert {"trend_h", "trend_lead", "trend_note", "trend_up", "trend_down", "trend_same"} <= set(bmp.C[lang]), lang
