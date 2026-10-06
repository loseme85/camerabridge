from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from classifier_v2 import classify_listing_v2


def _classify(title: str) -> dict:
    return classify_listing_v2({"상품명": title, "가격": "500,000"})


def test_standalone_hood_with_lens_compatibility_stays_accessory() -> None:
    titles = [
        "Leica 12549 Hood Silver [for M 50mm f2.8 Elmar]",
        "Leica 12475 Hood Black for M 50mm F1.2 Noctilux ASPH",
        "LEICA Lens Hood 12550 for M 50mm F2.8",
        "LEICA 12586 50mm F1.4 Hood",
        "Leica LeicaHood 12503 (Nocti50mm F1.2)",
        "[중고] M 50mm F1.4 용 후드 (12586)",
    ]

    for title in titles:
        result = _classify(title)
        assert result["category"] == "Accessory", title
        assert result["label"] == "Accessory", title
        assert result["accessory_type"] == "hood", title


def test_lens_with_included_hood_stays_lens() -> None:
    titles = [
        "Zeiss 21mm F2.8 ZM + Hood - Silver",
        "Leica 60mm F2.8 Asph(Silver) Apo Macro TL + Hood",
    ]

    for title in titles:
        result = _classify(title)
        assert result["category"] == "Lens", title


def test_existing_accessory_classes_remain_accessory() -> None:
    titles = [
        "Leica E82 UVa II Black",
        "Leica Universal Polarizing Filter M",
        "Leica Q2 Case Black",
        "Leica M Adapter L",
        "Leica Universal Finder",
        "Leica M10 Handgrip Black",
        "Leica M Soft Release Button",
        "Leica M 스트랩 블랙",
    ]

    for title in titles:
        result = _classify(title)
        assert result["category"] == "Accessory", title
        assert result["label"] == "Accessory", title


def test_filter_primary_titles_stay_accessory() -> None:
    titles = [
        "[중고] B+W Gradation Green E82",
        "LEICA A36 Orange",
        "Leica Serie8 UV Filter (M 50/1.2(B)",
        "B+W ND 1000 E46 Black Summarit 용",
    ]

    for title in titles:
        result = _classify(title)
        assert result["category"] == "Accessory", title
        assert result["label"] == "Accessory", title
        assert result["accessory_type"] == "filter", title


def test_lens_with_included_filter_stays_lens() -> None:
    titles = [
        "Used Leica Summicron-M 35mm f/2 ASPH, black (11879) - 6-Bit with Filter - Recent Leica CLA",
        "Used Leica Summilux-M 35mm f/1.4 ASPH FLE (11675), silver - UVa Filter",
        "Used Leica APO-Summicron-SL 75mm f/2 ASPH - UVa Filter",
        "Zeiss 21mm F2.8 ZM + Filter - Silver",
        "Leica 60mm F2.8 Asph(Silver) Apo Macro TL + Filter",
    ]

    for title in titles:
        result = _classify(title)
        assert result["category"] == "Lens", title


def test_sl_lens_titles_do_not_fall_into_accessory_lane() -> None:
    expected_mounts = {
        "Used Leica Summicron-SL 35mm f/2 ASPH": "SL",
        "Used Leica APO-Summicron-SL 50mm f/2 ASPH": "SL",
    }

    for title, mount in expected_mounts.items():
        result = _classify(title)
        assert result["category"] == "Lens", title
        assert result["label"] != "Accessory", title
        assert result["mount"] == mount, title


def test_sold_sl_lens_titles_stay_in_lens_lane() -> None:
    sold_items = [
        "Leica 35mm F2 AsphSummicron SL",
    ]

    for title in sold_items:
        result = classify_listing_v2({"상품명": title, "가격": "500,000", "품절": True})
        assert result["category"] == "Lens", title
        assert result["label"] != "Accessory", title


def test_standalone_adapter_and_adaptor_titles_stay_accessory() -> None:
    titles = [
        "Leica M Adapter L",
        "M-L Adapter Black",
        "LTM to M Adapter",
        "R Macro Adapter",
        "Amadeo adaptor for Contax RF to Leica M",
    ]

    for title in titles:
        result = _classify(title)
        assert result["category"] == "Accessory", title
        assert result["label"] == "Accessory", title
        assert result["accessory_type"] == "adapter", title


def test_lens_or_body_with_included_adapter_keeps_primary_category() -> None:
    expected = {
        "Carl Zeiss C 50mm F1.5 Sonnar + Amadeo adaptor": "Lens",
        "Leica 90mm F4 Macro Elmar M + Macro Adapter M": "Lens",
        "LEICA 90mm F4 (6bit) Macro Elmar-M Macro-Adapter-M sn.3976": "Lens",
        "Leica M10 Body with M-L Adapter": "Body",
    }

    for title, category in expected.items():
        result = _classify(title)
        assert result["category"] == category, title


def test_standalone_finder_titles_stay_accessory() -> None:
    titles = [
        "Leica 35mm Brightline Finder Silver",
        "Leica SBOOI 50mm Finder",
        "Leica Universal Viewfinder M",
        "Leica VIDOM 35-135mm Universal Finder Nickel",
    ]

    for title in titles:
        result = _classify(title)
        assert result["category"] == "Accessory", title
        assert result["label"] == "Accessory", title
        assert result["accessory_type"] == "finder", title


def test_lens_or_body_with_included_finder_keeps_primary_category() -> None:
    expected = {
        "Leica M 16-18-21mm f4 Tri-elmar ASPH 6bit Black + Finder set": "Lens",
        "[위탁] Avenon 28/3.5 + 파인더 Set": "Lens",
        "LEICA 135mm F4 ELMAR + finder sn.1769": "Lens",
        "Voigtlander 12mm F5.6 + Finder": "Lens",
        "Used Leica M6 0.72, black chrome 'Big Logo' (1988) with MP Finder - Recent Leica CLA": "Body",
        "Leica M10 Body with Visoflex Finder": "Body",
    }

    for title, category in expected.items():
        result = _classify(title)
        assert result["category"] == category, title

    low_foreign_price_body = classify_listing_v2({
        "상품명": "Used Leica M6 0.72, black chrome 'Big Logo' (1988) with MP Finder - Recent Leica CLA",
        "가격": "£4,295",
    })
    assert low_foreign_price_body["category"] == "Body"


def test_explicit_sl_accessories_stay_accessory() -> None:
    expected = {
        "Used Leica SL3 - Extra Battery": "battery",
        "Used Leica Multifunctional Handgrip HG-SCL7 for SL3": "grip",
        "Leica 12549 Hood Silver [for M 50mm f2.8 Elmar]": "hood",
    }

    for title, accessory_type in expected.items():
        result = _classify(title)
        assert result["category"] == "Accessory", title
        assert result["label"] == "Accessory", title
        assert result["accessory_type"] == accessory_type, title


if __name__ == "__main__":
    test_standalone_hood_with_lens_compatibility_stays_accessory()
    test_lens_with_included_hood_stays_lens()
    test_existing_accessory_classes_remain_accessory()
    test_filter_primary_titles_stay_accessory()
    test_lens_with_included_filter_stays_lens()
    test_sl_lens_titles_do_not_fall_into_accessory_lane()
    test_sold_sl_lens_titles_stay_in_lens_lane()
    test_standalone_adapter_and_adaptor_titles_stay_accessory()
    test_lens_or_body_with_included_adapter_keeps_primary_category()
    test_standalone_finder_titles_stay_accessory()
    test_lens_or_body_with_included_finder_keeps_primary_category()
    test_explicit_sl_accessories_stay_accessory()
    print("test_accessory_category: ok")


def test_foreign_currency_prices_are_not_read_as_won() -> None:
    # 2026-10: £2,299 · €3,499 · ¥150,000 바디가 "20만 원 이하 = 액세서리" 규칙에 걸려 검색에서 빠지던 문제
    body = classify_listing_v2({"상품명": "Leica M6 0.72x Black Body Only", "가격": "£2,299.00", "통화": "GBP"})
    assert body["category"] == "Body"
    body = classify_listing_v2({"상품명": "Leica M6 (0.72x) (Silver, 10414)", "가격": "€3,499", "통화": "EUR"})
    assert body["category"] == "Body"
    body = classify_listing_v2({"상품명": "Leica M3 Body", "가격": "¥150,000", "통화": "JPY"})
    assert body["category"] == "Body"
    cheap = classify_listing_v2({"상품명": "Leica M3 Body", "가격": "150,000"})
    assert cheap["category"] == "Accessory"  # 원화 15만 원 바디는 그대로 의심


def test_foreign_dealer_accessory_words() -> None:
    for title in ["Leica MRMeter Black", "Leica 8倍双眼鏡 ウルトラVit 8×20BR Black", "Leica Q3 for サムレスト Black",
                  "[중고] Leica MP Rewind crank (Silver)", "Leica ABLON Film Leader Cutter Silver"]:
        assert classify_listing_v2({"상품명": title, "가격": "¥40,000", "통화": "JPY"})["category"] == "Accessory", title


def test_macro_lens_is_not_m_a_body() -> None:
    # 'leica ma'(M-A) 키워드가 'Leica Macro-Elmar'에 걸리던 것
    assert classify_listing_v2({"상품명": "Leica Macro-Elmar-M 90mm/F4.0 Black", "가격": "HK$9,800", "통화": "HKD"})["category"] == "Lens"
    assert classify_listing_v2({"상품명": "Leica M-A (Typ 127) Silver", "가격": "HK$29,800", "통화": "HKD"})["category"] == "Body"


def test_rangefinder_camera_is_not_viewfinder_accessory() -> None:
    body = classify_listing_v2({"상품명": "Leica M7 0.72 Black Film Rangefinder Camera 10503", "가격": "HK$31,800", "통화": "HKD"})
    assert body["category"] == "Body"
    finder = classify_listing_v2({"상품명": "Leica 24mm Viewfinder Black 12019", "가격": "HK$2,800", "통화": "HKD"})
    assert finder["category"] == "Accessory"
