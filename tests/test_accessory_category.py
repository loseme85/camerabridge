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


if __name__ == "__main__":
    test_standalone_hood_with_lens_compatibility_stays_accessory()
    test_lens_with_included_hood_stays_lens()
    test_existing_accessory_classes_remain_accessory()
    test_filter_primary_titles_stay_accessory()
    test_lens_with_included_filter_stays_lens()
    print("test_accessory_category: ok")
