import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from condition_grade import describe_text, grade_of  # noqa: E402


def test_shop_labels_map_to_common_grades():
    assert grade_of("라이카스토어 충무로", "97%", "M 35/1.4 FLE") == ("A", "label")
    assert grade_of("사진집", "95%", "x") == ("B", "label")
    assert grade_of("라이카스토어 충무로", "88%", "x") == ("D", "label")
    assert grade_of("기타무라 (일본)", "AB", "Leica M3") == ("B", "label")
    assert grade_of("기타무라 (일본)", "C", "x") == ("D", "label")
    assert grade_of("Ffordes (영국)", "E++", "x") == ("A", "label")
    assert grade_of("eBay", "Near mint", "x")[0] == "A"


def test_title_and_description_grades():
    assert grade_of("사진집", "정보없음", "신품 Leica M 50mm") == ("N", "title")
    assert grade_of("장씨카메라", "정보없음", "LEICA M6 고장") == ("X", "title")
    assert grade_of("Kamerastore (핀란드)", describe_text("It is in good condition & works well."), "x") == ("C", "text")
    assert grade_of("Leica Store Miami", describe_text("in excellent condition with minimal signs of use"), "x") == ("B", "text")
    assert grade_of("Leica Store Miami", "정보없음", "Used Leica Summilux") == (None, None)


def test_mk_kamera_description_grades() -> None:
    site = "M & K Kamera (홍콩)"
    assert grade_of(site, "M&K: brand new", "Leica M11")[0] == "N"
    assert grade_of(site, "M&K: excellent condition", "Leica M6")[0] == "A"
    assert grade_of(site, "M&K: only minor signs of use", "Leica M6")[0] == "B"
    assert grade_of(site, "M&K: slightly used", "Leica M6")[0] == "B"
    assert grade_of(site, "M&K: normal signs of wear", "Leica M6")[0] == "C"
    assert grade_of(site, "M&K: not working", "Leica M6")[0] == "X"


def test_kamerastore_staff_note_grades() -> None:
    from condition_grade import ks_condition
    site = "Kamerastore (핀란드)"
    def g(note):
        return grade_of(site, ks_condition(note) or "정보없음", "Leica M6")[0]
    assert g("It is in great working condition!") == "B"
    assert g("It has some wear from use but is in good working condition.") == "C"
    assert g("It's quite worn externally, but works well.") == "D"
    assert g("It has a lot of haze inside that will lower overall image quality.") == "D"
    assert g("There are minor scratches on the lens elements that won't affect image quality.") == "B"
    assert g("In German.") is None  # 설명서 등 컨디션 말이 없는 것


def test_leica_france_letter_grades() -> None:
    from condition_grade import LCF_PREFIX
    site = "Leica Store France (프랑스)"
    assert grade_of(site, LCF_PREFIX + "A : Excellent", "LEICA M11")[0] == "A"
    assert grade_of(site, LCF_PREFIX + "C : Good", "SUMMICRON-M 35 mm f/2")[0] == "C"
    assert grade_of(site, LCF_PREFIX + "E : Not fully operational", "LEICA M6")[0] == "X"
    # 'new (2021-ACTU)'는 새 버전이라는 뜻, 신품 아님
    assert grade_of(site, LCF_PREFIX + "B : Very good", "NOCTILUX-M 50 mm f/1.2 new (2021-ACTU)")[0] == "B"


def test_newoldcamera_letter_grades() -> None:
    from condition_grade import NOC_PREFIX
    site = "Newoldcamera (이탈리아)"
    assert grade_of(site, NOC_PREFIX + "A-", "Leica 50mm f/0.95 NOCTILUX-M ASPH. black")[0] == "A"
    assert grade_of(site, NOC_PREFIX + "BA", "Leica 50mm f/2 SUMMICRON-M SAFARI")[0] == "B"
    assert grade_of(site, NOC_PREFIX + "B+/B", "Leica 35mm f/3.5 SUMMARON chrome")[0] == "C"
    assert grade_of(site, NOC_PREFIX + "BC", "Leica IIIC chrome")[0] == "D"
    # 'NEW'는 새 버전(새 디자인)이라는 뜻 → 제목에서 'new version'으로 바꿔 신품으로 안 봄
    assert grade_of(site, NOC_PREFIX + "BA", "Leica 90mm f/4 MACRO-ELMAR-M new version black")[0] == "B"


def test_new_version_words_are_not_brand_new() -> None:
    assert grade_of("라이카스토어 충무로", "98%", "[위탁] M 28/2 Summicron ASPH NEW (Black)")[0] == "A"
    assert grade_of("사진집", "97%", "Leica M 28mm f2 Summicron ASPH 6bit New Type Black")[0] == "A"
    assert grade_of("M & K Kamera (홍콩)", None, "Brand New Leica Summicron-M 28mm/F2.0 ASPH 11618")[0] == "N"


def test_camtec_title_grades():
    from condition_grade import CAMTEC_PREFIX
    site = "Camtec Photo (캐나다)"
    assert grade_of(site, CAMTEC_PREFIX + "A+", "Leica Summilux-M 90mm f/1.5 ASPH")[0] == "A"
    assert grade_of(site, CAMTEC_PREFIX + "A", "Leica Summilux-M 50mm f/1.4 ASPH")[0] == "B"
    assert grade_of(site, CAMTEC_PREFIX + "A-", "Leica D-Lux 4 Black")[0] == "C"
    assert grade_of(site, CAMTEC_PREFIX + "Open Box", "Leica Summicron-M 35mm f/2 ASPH. Black (E39)")[0] == "N"


def test_aperture_description_grades():
    from condition_grade import APERTURE_PREFIX
    site = "Aperture (영국)"
    assert grade_of(site, APERTURE_PREFIX + "Mint", "Leica 28mm f5.6 Summaron-M Black")[0] == "A"
    assert grade_of(site, APERTURE_PREFIX + "Exc++", "Leica M9-P Silver")[0] == "B"
    assert grade_of(site, APERTURE_PREFIX + "Exc+", "Leica 50mm f2 Summicron-R 1 Cam")[0] == "C"
    assert grade_of(site, APERTURE_PREFIX + "User", "Leica M2 Black Paint")[0] == "D"
    assert grade_of(site, APERTURE_PREFIX + "New", "Leica 35mm f1.4 Summilux-TL ASPH Black Anodized")[0] == "N"


def test_harrison_description_grades():
    from condition_grade import HARRISON_PREFIX, harrison_condition
    site = "Harrison Cameras (영국)"
    assert harrison_condition("<p>Lovely lens.</p>\n<p>Condition: Used - Very good<br>Includes caps</p>") == "Very Good"
    assert harrison_condition("<p>Condition Very Good Marks around the camera</p>") == "Very Good"
    assert harrison_condition("<p>In excellent condition, it's a cost-effective way</p><p>Used - Excellent</p>") == "Excellent"
    assert harrison_condition("<p>No grade here.</p>") is None
    assert grade_of(site, HARRISON_PREFIX + "Mint", "Leica D-Lux 8 Camera 19191")[0] == "A"
    assert grade_of(site, HARRISON_PREFIX + "Excellent", "Leica M6 TTL Silver .72 Rangefinder Camera Body 10434")[0] == "B"
    assert grade_of(site, HARRISON_PREFIX + "Very Good", "Leica M7 0.72 Black Rangefinder Camera Body 10503")[0] == "B"
    assert grade_of(site, HARRISON_PREFIX + "Good", "Leica R4 Silver Camera Body")[0] == "C"
def test_wex_condition_grades():
    from condition_grade import WEX_PREFIX
    site = "Wex Photo Video (영국)"
    assert grade_of(site, WEX_PREFIX + "As new (10)", "Leica D-Lux 8 Digital Camera")[0] == "S"
    assert grade_of(site, WEX_PREFIX + "Mint (9+)", "Leica M11-D Digital Camera Body")[0] == "A"
    assert grade_of(site, WEX_PREFIX + "Excellent (9)", "Leica Q3 43 Digital Camera")[0] == "B"
    assert grade_of(site, WEX_PREFIX + "Very good (9-)", "Leica 50mm f0.95 Noctilux-M Asph Lens- Black")[0] == "B"
    assert grade_of(site, WEX_PREFIX + "Good (8)", "Leica Summicron-M 35mm f2 ASPH Black Paint Millennium (11611)")[0] == "C"
