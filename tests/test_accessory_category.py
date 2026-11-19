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


def test_enlarger_lens_and_film_cassette_are_accessory() -> None:
    # 2026-11-07: 초점거리가 있어도 확대기 렌즈·필름 카세트는 촬영용 렌즈 시세에 넣지 않음
    for title in ["Leica LEITZ FOCOTAR 60mm F4.5", "Leica 50/4.5 FOCOTAR Leitz Wetzlar Germany",
                  "Leica Rapid Loading System (14260)", "Leica DRXOO 35mm Reloadable Film Cassette"]:
        assert _classify(title)["category"] == "Accessory", title
    # 'Rapid Load' 장치가 붙은 M3 바디는 그대로 바디
    assert _classify("Leica M3 Single Stroke Rapid Load")["category"] == "Body"


def test_foreign_language_accessory_words() -> None:
    # 2026-11-13: X1 검색에 독일어 배터리·가죽 케이스가 바디로 섞임
    for title in [
        "Leica Akku für Leica X1 X2 BP-DC8 18706",
        "Leica Ledertasche für X1 18709",
        "Leica Bereitschaftstasche M / M-P (Typ 240) 14890",
        "Leica Ladegerät BC-SCL6",
        "Etui Leica X2",
        "Custodia in pelle Leica X1",
    ]:
        assert _classify(title)["category"] == "Accessory", title


def test_foreign_language_bundles_stay_main_item() -> None:
    for title, category in [
        ("Leica M10 + Akku + Ladegerät", "Body"),
        ("Leica X1 mit Tasche und Akku", "Body"),
        ("Leica X1 (18400)", "Body"),
    ]:
        assert _classify(title)["category"] == category, title


def test_foreign_parts_and_manuals() -> None:
    # 2026-11-13 판매 중 가격대 점검: 바디 최저가가 이런 것이었음
    for title in [
        "Leica Schnelladespule f. M1 M2 M3 MD & OVP 14260",
        "Leitz Wetzlar Visiflex II Spiegelkasten",
        'Leica Borsetta "Andrea" C-Lux in pelle Black',
        "Leica Anastigmat Anleitung von 1928 wie arbeitet man mit Leica Kamera",
    ]:
        assert _classify(title)["category"] == "Accessory", title
    assert _classify("Leica M6 0.72 mit Anleitung und Box")["category"] == "Body"


def test_strong_accessory_words_before_body_rules() -> None:
    # 2026-11-14 시세 이탈 점검: 바르낙·콤팩트 바디 판단보다 먼저 부속품
    for title in [
        "Leica IIIc 取扱説明書",
        "Leica MP for 巻き戻しクランク 14437",
        "Leica Q2 for サムサポート 19543",
        "FONDELLO LEICA M MONOCHROM TYP246",
        "Leica M2 M3 black paint back door Filmandruckplatte",
        "Leica IIIf for Case",
        "Leica A型 for 革Case",
        "Leica Extension Tube (90mm f4 Elmar) (OTQNO /16468)",
        "Leica Werbung Display R3 Rare Blinkdisplay advertising",
    ]:
        assert _classify(title)["category"] == "Accessory", title
    for title, category in [
        ("Leica A型 Black (New Elmar 50mm F3.5付)", "Body"),
        ("Leica DRP Ernst Leitz Wetzlar Sucherkamera mit Leitz Elmar 50mm f3.5 Objektiv", "Body"),
        ("Leica Macro-Elmarit-R 60mm/F2.8 w/ 1:1 Extension tube boxed 11203", "Lens"),
        ("Leica Macro-Elmar 100/4(for bellows)", "Lens"),
        ("Leica M6 0.72 mit Anleitung und Box", "Body"),
    ]:
        assert _classify(title)["category"] == category, title


def test_bodies_and_lenses_with_accessory_words_stay_body_or_lens() -> None:
    # 2026-11-19 악세사리 점검: 본체인데 부속품 키워드(finder·plate·strap·leicavit)에 걸려 악세사리로 빠지던 제목
    expected = {
        "Leica MP 0.72 Silver Chrome Rangefinder": "Body",
        "Leica M3, silver-chrome-plated Body": "Body",
        "Leica M4-2 black chrome-plated Body": "Body",
        "Leica M3 ダブルストローク(Finder切替ナシ)": "Body",
        "Leica M3 DS Black後塗 Leicavit対応改造品": "Body",
        "Leica M5 Black 革Strap付": "Body",
        "Leica <<Strap付き！！>> LEICA Leica M4 Body Silver Chrome 127万台 Mマウント #LE20275601": "Body",
        "Leica ＜＜保護Filter付き！！＞＞ LEICA Leica Summicron M 50mm f2.0 Collapsible #LE2027600": "Lens",
        "Leica M 35mm f1.4 SUMMILUX ASPH. Silver, Chrome-plated 미개봉신품": "Lens",
    }
    for title, category in expected.items():
        assert _classify(title)["category"] == category, title


def test_real_accessories_with_similar_words_stay_accessory() -> None:
    for title in [
        "Leica FOKOS Rangefinder fofer for camera",
        "Leica 35mm View finder",
        "Voigtlander 28-35mm Finder Black",
        "Leica M6 for 底Case",
        "Leica Leicavit M Black Paint",
        "Leica baseplate M4 base plate",
        "Viewfinder for rangefinder Leica M",
    ]:
        assert _classify(title)["category"] == "Accessory", title


def test_lens_turret_is_accessory() -> None:
    assert _classify("Leica OROLF Lens Turret for screw mount lenses with M2/M3")["category"] == "Accessory"


def test_built_in_hood_lenses_and_visoflex_lenses_stay_lens() -> None:
    # 2026-11-19 전체 점검: 후드 내장 렌즈·Visoflex용 렌즈·f값 없는 싼 렌즈가 악세사리로 빠지던 것
    for title in [
        "Leica SUMMILUX M 75/1.4 Hood組込",
        "Leica Noctilux-M 50mm f/1.0 E60 Hood組込 11822 代引き不可",
        "Leica Summilux-M 35mm F1.4 ASPH - Black / 11726 / FLE / Built-in-hood",
        "Leica Telyt 200/4(VISOFLEX)",
        "Leitz Wetzlar Telyt 200mm f4 lens for Visoflex",
        "Leica Hektor-M 135/4.5",
        "Leica Elmar 9cm/4",
        "Leitz Telyt 200mm f4 (L39) Screw Mount w. Extension Ring",
        "Leica 50mm f/1.5 XENON chrome 3 RING",
    ]:
        assert _classify(title)["category"] == "Lens", title


def test_manuals_caps_rings_boxes_are_accessories() -> None:
    for title in [
        "Leica Minilux Instructions",
        "Leica 55mm (E55) Front Cap, Black, Snap-On, 14289, for 90mm f2",
        "Leica Bayonet Ring 28/90MM",
        "Leica box ROSSA IIIG",
        "Leica Summilux 1:1.4 / 50 / 11114, Empty box / Packaging only",
        "Leica Motor Chrome MOOLY",
        "Leica Elmarit-R 90/2.8 for LensCap 14089",
    ]:
        assert _classify(title)["category"] == "Accessory", title


def test_old_r_bodies_and_rangefinder_bodies_stay_body() -> None:
    for title in ["Leica R4 Black", "Leicaflex (Mk.1) body", "Leica M6 Rangefinder Chrome", "Leica M2 ST Recovered, DAG Overhauled",
                  "Leica SL Typ 601 24MP 10850 Digitalkamera accessory"]:
        assert _classify(title)["category"] == "Body", title
