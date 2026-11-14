"""분류 회귀 시험: 사람이 한 줄씩 확인한 매물 분류(tests/fixtures/category_regressions.json)가 규칙을 고친 뒤에도 그대로인지.

2026-11-14 #369: 부속품 규칙을 넣다가 벨로즈 + Macro-Elmar 세트가 부속품으로, KS15-4 (M2-S) 바디가 렌즈로 바뀌었다.
분류 규칙 PR은 scripts/category_diff.py로 바뀐 목록을 확인하고, 맞게 바뀐 것을 fixture에 더한다.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from classifier_v2 import classify_listing_v2  # noqa: E402

CASES = json.load(open(ROOT / "tests/fixtures/category_regressions.json", encoding="utf-8"))["cases"]


def test_reviewed_categories_stay_the_same() -> None:
    wrong = []
    for case in CASES:
        got = classify_listing_v2({"상품명": case["title"], "가격": 0, "통화": "", "site": "", "description": ""})["category"]
        if got != case["category"]:
            wrong.append(f"{case['title']}: {got} (확인한 분류 {case['category']})")
    assert not wrong, "\n".join(wrong)


def test_accessory_plus_lens_sets_stay_lens() -> None:
    for title in ("Leica Balgen 16860 mit Macro-Elmar 100mm f/4.0", "Leica Bellows-R + Macro-Elmar 100mm f/4 + Leica M adapter",
                  "Leica Macro-Elmar R 100/4 フォーカシング Bellows RSet",
                  "Leica R Leicaflex Leitz 16860 Bellows Bellows Con Macro-Elmar 100mm f4", "Leica Balgen mit Elmar 90mm f4 L39"):
        assert classify_listing_v2({"상품명": title, "가격": 0, "통화": "", "site": "", "description": ""})["category"] == "Lens", title
    for title in ("Leica Extension Tube (90mm f4 Elmar) (OTQNO /16468)", "Leica Zwischenring 16468X für Elmar 90mm f4.0",
                  "Leica 50mm f2.0 Dummy + Doos", "Leica Macro Bellows-R 16860"):
        assert classify_listing_v2({"상품명": title, "가격": 0, "통화": "", "site": "", "description": ""})["category"] == "Accessory", title


def test_military_m2_is_body() -> None:
    for title in ("Leica KS15-4 (M2-S)", "Leica KS-15 (4) M2 body", "Leica M2-(R)"):
        assert classify_listing_v2({"상품명": title, "가격": 0, "통화": "", "site": "", "description": ""})["category"] == "Body", title


def test_main_item_with_accessory_tail_is_main_item() -> None:
    """'렌즈 + Lens Hood (12526)'·'M10 with Extra Battery'는 본품, 'Motor Drive R4 con Impugnatura'·'M body & lens cap set'은 부속품."""
    cases = {
        "Leica 35mm f2 Summicron-M ASPH. (Type I) (Black, 11879) + Lens Hood (35mm f2 ASPH. / 28mm f2.8 ASPH.) (12526)": "Lens",
        "Used Leica M10, black chrome with Extra Battery": "Body",
        "Leica M2 Silver Film Rangefinder Camera with leather case": "Body",
        "Leica MP Hammertone 0.72x LHSA with Leicavit": "Body",
        "Leica Motor Drive R4 con Impugnatura": "Accessory",
        "Leica M body & lens cap set": "Accessory",
        "Leica 12480 Lens Cap f. Noctilux 11686 - like new with 2 years guarantee Accessory": "Accessory",
        "Leica hood 12585H 35-50MM + cap 14033": "Accessory",
        "Leica Visoflex II + Right-Angle Visoflex Prism Finder (OTXBO / 16460)": "Accessory",
    }
    for title, want in cases.items():
        assert classify_listing_v2({"상품명": title, "가격": 0, "통화": "", "site": "", "description": ""})["category"] == want, title


def test_main_item_with_accessory_links_to_its_model() -> None:
    """'렌즈 + Lens Hood'·'바디 with Extra Battery'는 그 모델에 붙고, '바디 + 렌즈' 세트는 한쪽 모델에만 붙지 않는다."""
    from entity_catalog import load_catalog, match_entities

    catalog = load_catalog()

    def ids(title: str, category: str) -> list[str]:
        return match_entities({"final_output": {"title_raw": title, "category": category}}, catalog)

    assert "leica:lens:noctilux-m:50:f1.0" in ids("Leica 50mm f1 Noctilux-M (Type III) (11821) + Lens Hood (50mm f1) (12544)", "Lens")
    assert "leica:lens:summilux-r:50" in ids("Leica Leitz Summilux-R 50mm f/1.4 3cam + 12508 hood", "Lens")
    assert "leica:body:sl2-s" in ids("Used Leica SL2-S with Extra Battery", "Body")
    assert "leica:body:r7" not in ids("Leica R7 + Leitz Elmarit-R 35mm f2.8", "Body")


def test_summilux_50_black_paint_reissue_is_separate() -> None:
    """복각(11713, 2021)과 1960년대 원판 블랙 페인트가 한 칸에 섞여 시세 폭이 넓던 것 (시세 이탈 2차 2026-11-15)."""
    from entity_catalog import load_catalog, match_entities

    catalog = load_catalog()

    def ids(title: str, price: float) -> list[str]:
        return match_entities({"final_output": {"title_raw": title, "category": "Lens", "currency": "KRW", "parsed_price_numeric": price}}, catalog)

    assert "leica:lens:summilux-m:50:black-paint-reissue" in ids("Leica Summilux-M 50mm f1.4 GlossyBlackPaint[11713]", 6_500_000)
    assert "leica:lens:summilux-m:50:black-paint" in ids("Leica Summilux-M 50mm F1.4 OriginalBlackPaint 真鍮マウント", 40_000_000)
    assert "leica:lens:summilux-m:50:black-paint-reissue" in ids("Leica Summilux-M 50mm f1.4 black paint", 7_000_000)
    assert "leica:lens:summilux-m:50:black-paint" in ids("Leica M 50mm f1.4 Summilux 4th Black Paint", 11_500_000)
