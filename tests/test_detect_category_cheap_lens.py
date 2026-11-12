"""싼 옛 렌즈('F4'처럼 정수 조리개)가 50만원 이하 가격 규칙으로 액세서리가 되던 것, 'leica macro'가 바디(M-A)가 되던 것,
가격 0이 배송비만 총액으로 보이던 것 (2026-11-12)."""
import ast
import re
from pathlib import Path

SRC = Path(__file__).resolve().parents[1].joinpath("app/test.py").read_text(encoding="utf-8")


def _detect_category():
    a, b = SRC.index("def _has_aperture"), SRC.index("\ndef detect_brand")
    ns = {"re": re, "_re": re}
    exec(SRC[a:b], ns)
    return ns["detect_category"]


def test_cheap_old_lens_stays_lens():
    f = _detect_category()
    assert f("Leica Elmar-R 180mm F4 3cam", "€113") == "Lens"
    assert f("Leica M 135mm f4 Tele-Elmar Black", "450,000원") == "Lens"
    assert f("Leica M Elmar 9cm F4", "€142") == "Lens"


def test_cheap_accessories_stay_accessory():
    f = _detect_category()
    assert f("Leica Extension Tube (90mm f4 Elmar) (OTQNO /16468)", "€60") == "Accessory"
    assert f("Leitz 14071 short focusing mount for 135mm f4 Elmar", "€80") == "Accessory"
    assert f("Leica M5 Leather Case (14544)", "€34") == "Accessory"


def test_macro_is_not_ma_body():
    f = _detect_category()
    assert f("Leica MACRO-ELMAR 100/4", "¥45,000") != "Body"
    assert f("Leica MA Black", "€4,000") == "Body"


def test_zero_price_becomes_inquiry():
    assert "가격 0은 '가격 문의'" in SRC
    pat = re.search(r're\.fullmatch\(r"(\[\^\\d\]\*0\+[^"]+)"', SRC).group(1)
    assert re.fullmatch(pat, "€0") and re.fullmatch(pat, "0원") and not re.fullmatch(pat, "€10")
