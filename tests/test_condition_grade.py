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
