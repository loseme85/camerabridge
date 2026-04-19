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


if __name__ == "__main__":
    test_standalone_hood_with_lens_compatibility_stays_accessory()
    test_lens_with_included_hood_stays_lens()
    test_existing_accessory_classes_remain_accessory()
    print("test_accessory_category: ok")
