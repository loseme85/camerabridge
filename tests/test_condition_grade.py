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
def test_naniwa_condition_grades():
    site = "카메라노나니와 (일본)"
    assert grade_of(site, "A", "Leica 19651 Q3 Protector Black")[0] == "A"
    assert grade_of(site, "AB+", "Leica 20221 M11-D Black Paint")[0] == "A"
    assert grade_of(site, "AB", "Leica Summicron M 50/2 (6BIT) 11826C")[0] == "B"
    assert grade_of(site, "AB-", "Leica Elmarit M 28/2.8")[0] == "B"
    assert grade_of(site, "B+", "Leica IIIf Red Synchro")[0] == "C"
    assert grade_of(site, "B", "Leica M3 (SS)")[0] == "C"
    assert grade_of(site, "C", "Leica Summicron M50/2 (3rd)")[0] == "D"
def test_calumet_condition_grades():
    from condition_grade import CALUMET_PREFIX
    site = "Calumet (독일)"
    assert grade_of(site, CALUMET_PREFIX + "Wie neu", "Leica APO-SUMMICRON-SL 90mm F2 Asph.")[0] == "A"
    assert grade_of(site, CALUMET_PREFIX + "Sehr gut", "Leica M10 Monochrom")[0] == "B"
    assert grade_of(site, CALUMET_PREFIX + "Gut", "Leica M10-P silber verchromt")[0] == "C"
    assert grade_of(site, CALUMET_PREFIX + "Akzeptabel", "Leica Summicron-M 90mm/2,0")[0] == "C"
    assert grade_of(site, CALUMET_PREFIX + "Stark gebraucht", "Leica Minilux Zoom")[0] == "D"
def test_camerawest_condition_grades():
    from condition_grade import CAMERAWEST_PREFIX
    site = "Camera West (미국)"
    assert grade_of(site, CAMERAWEST_PREFIX + "10-", "Leica 90mm f2 APO-Summicron-M Asph")[0] == "A"
    assert grade_of(site, CAMERAWEST_PREFIX + "9+", "Leica Q3")[0] == "B"
    assert grade_of(site, CAMERAWEST_PREFIX + "8+", "Leica 50mm f2 Summicron-M")[0] == "C"
    assert grade_of(site, CAMERAWEST_PREFIX + "7+", "Leica 180mm f2.8 Elmarit-R")[0] == "D"
def test_peterloy_condition_grades():
    from condition_grade import PETERLOY_PREFIX
    site = "Peter Loy (영국)"
    assert grade_of(site, PETERLOY_PREFIX + "3/D", "Leica Visoflex II")[0] == "A"
    assert grade_of(site, PETERLOY_PREFIX + "4/D", "Leica 21mm f3.4 Super-Elmar-M Asph")[0] == "B"
    assert grade_of(site, PETERLOY_PREFIX + "4-5/E", "Leica Standard body, chrome")[0] == "C"
    assert grade_of(site, PETERLOY_PREFIX + "5-6/D", "Leica III body, chrome")[0] == "D"
    assert grade_of(site, PETERLOY_PREFIX + "3/G", "Leica III body, chrome")[0] == "D"
    assert grade_of(site, PETERLOY_PREFIX + "4/J", "Leica IIIa body")[0] == "X"
def test_lucky_condition_grades():
    from condition_grade import LUCKY_PREFIX
    site = "Lucky Camera (일본)"
    assert grade_of(site, LUCKY_PREFIX + "AA", "Leica M4 Chrome")[0] == "A"
    assert grade_of(site, LUCKY_PREFIX + "AB", "Leica Summicron M 35mm f2")[0] == "B"
    assert grade_of(site, LUCKY_PREFIX + "A", "Leica IIIf Body")[0] == "C"
    assert grade_of(site, LUCKY_PREFIX + "B", "Leica Elmar 5cm f3.5")[0] == "D"
def test_akasaka_condition_grades():
    from condition_grade import AKASAKA_PREFIX
    site = "Akasaka Camera (일본)"
    assert grade_of(site, AKASAKA_PREFIX + "新同品", "LeicavitM Silver")[0] == "S"
    assert grade_of(site, AKASAKA_PREFIX + "美品", "Leica Vario-Elmar-R 28-70mm f3.5-4.5 ROM")[0] == "B"
    assert grade_of(site, AKASAKA_PREFIX + "良品", "Leica Summicron 50mm f2.0 M")[0] == "B"
    assert grade_of(site, AKASAKA_PREFIX + "中", "Leica Nickel Hektor 50mm f2.5 L")[0] == "C"
def test_glazers_condition_grades():
    from condition_grade import GLAZERS_PREFIX
    site = "Glazers Camera (미국)"
    assert grade_of(site, GLAZERS_PREFIX + "EX", "Leica Elmarit-TL 18mm f2.8 ASPH")[0] == "A"
    assert grade_of(site, GLAZERS_PREFIX + "VG", "Leica M6 Classic Silver Body")[0] == "B"
    assert grade_of(site, GLAZERS_PREFIX + "Good", "Leica Summilux-SL 50mm f1.4")[0] == "C"
    assert grade_of(site, GLAZERS_PREFIX + "Fair", "Leica Summicron-M 50mm f2 Rigid Haze")[0] == "D"
def test_tamarkin_condition_grades():
    from condition_grade import TAMARKIN_PREFIX
    site = "Tamarkin Camera (미국)"
    assert grade_of(site, TAMARKIN_PREFIX + "Near Mint", "Leica 21mm Super-Elmar-M f3.4 ASPH")[0] == "A"
    assert grade_of(site, TAMARKIN_PREFIX + "Ex++", "Leica M3 Double Stroke Body")[0] == "B"
    assert grade_of(site, TAMARKIN_PREFIX + "Ex+", "Leica 50mm Summilux f1.4 Silver Chrome")[0] == "B"
    assert grade_of(site, TAMARKIN_PREFIX + "VG", "Leica 28mm Summilux-M f1.4 ASPH")[0] == "D"
def test_leica_classic_condition_grades():
    from condition_grade import LEICA_CLASSIC_PREFIX
    site = "Leica Classic (오스트리아)"
    assert grade_of(site, LEICA_CLASSIC_PREFIX + "A", "Leica SF 24D")[0] == "S"
    assert grade_of(site, LEICA_CLASSIC_PREFIX + "A-", "Leica Summilux-M 35mm f/1.4 ASPH")[0] == "A"
    assert grade_of(site, LEICA_CLASSIC_PREFIX + "B/A", "Leica Summicron-M 50mm f/2")[0] == "B"
    assert grade_of(site, LEICA_CLASSIC_PREFIX + "B", "Leica Elmarit-M 90mm f/2.8")[0] == "C"
    assert grade_of(site, LEICA_CLASSIC_PREFIX + "B/C", "Leica M3")[0] == "D"
def test_cameraelectronic_condition_grades():
    from condition_grade import ce_condition
    site = "Camera Electronic (호주)"
    assert grade_of(site, ce_condition("Pre-Owned Leica SL3-S Body Boxed As New"), "Leica SL3-S Body")[0] == "S"
    assert grade_of(site, ce_condition("Pre-Owned Leica Summilux-M 50mm f/1.4 ASPH Lens Mint in Box"), "Leica Summilux-M 50mm f1.4 ASPH Lens")[0] == "A"
    assert grade_of(site, ce_condition("A classic rangefinder in excellent condition."), "Leica M6 TTL .85 Silver Body")[0] == "C"
    assert grade_of(site, ce_condition("Shows minimal signs of wear."), "Leica Elmarit-R 135mm f2.8 Lens")[0] == "D"
def test_fotohandel_condition_grades():
    from condition_grade import FOTOHANDEL_PREFIX
    site = "fotohandel.de (독일)"
    assert grade_of(site, FOTOHANDEL_PREFIX + "A", "Leica Summilux-M 35mm f1.4 Asph. E46 11874")[0] == "A"
    assert grade_of(site, FOTOHANDEL_PREFIX + "A-", "Leica M3 Double Stroke")[0] == "B"
    assert grade_of(site, FOTOHANDEL_PREFIX + "A-B", "Leica Elmarit 28mm f2.8 Version II 11801")[0] == "B"
    assert grade_of(site, FOTOHANDEL_PREFIX + "B", "Leica Super-Angulon 21mm f3.4 11103")[0] == "C"
    assert grade_of(site, FOTOHANDEL_PREFIX + "B-C", "Leica Summicron-M 50mm f2.0 11819")[0] == "D"
def test_sanpou_condition_grades():
    from condition_grade import SANPOU_PREFIX
    site = "三宝カメラ (일본)"
    assert grade_of(site, SANPOU_PREFIX + "AB", "Leica Summilux-M 35mm f1.4 ASPH Titan")[0] == "A"
    assert grade_of(site, SANPOU_PREFIX + "B", "Leica M3 Body (2 Stroke)")[0] == "B"

def test_kikuya_grades():
    from condition_grade import KIKUYA_PREFIX
    site = "喜久屋カメラ (일본)"
    assert grade_of(site, KIKUYA_PREFIX + "A-", "Leica SUMMILUX-M 35mm f1.4 2nd")[0] == "B"
    assert grade_of(site, KIKUYA_PREFIX + "AB", "Leica M3 Body")[0] == "B"
    assert grade_of(site, KIKUYA_PREFIX + "B", "Leica FOOKH LENS HOOD")[0] == "C"
def test_heidelberg_condition_grades():
    from condition_grade import HEIDELBERG_PREFIX
    site = "Leica Store Heidelberg (독일)"
    assert grade_of(site, HEIDELBERG_PREFIX + "1-", "Leica Summilux-M 35mm f1.4 ASPH. 11663")[0] == "A"
    assert grade_of(site, HEIDELBERG_PREFIX + "2", "Leica Elmarit-M 90mm f2.8 11807")[0] == "B"
    assert grade_of(site, HEIDELBERG_PREFIX + "2-3", "Leica Objektivdeckel Q Messing")[0] == "C"
    assert grade_of(site, HEIDELBERG_PREFIX + "Demo", "Leica M11 black gloss paint Body")[0] == "S"
def test_vibe_condition_grades():
    from condition_grade import VIBE_PREFIX
    site = "Vibe.pl (폴란드)"
    assert grade_of(site, VIBE_PREFIX + "5", "Leica Summilux-M 50mm f1.4 Asph. 6-bit black (11891)")[0] == "A"
    assert grade_of(site, VIBE_PREFIX + "4", "Leica Elmarit-M 90mm f2.8 (11 807)")[0] == "B"
    assert grade_of(site, VIBE_PREFIX + "3", "Leica Summicron-M 50mm f2.0 Leitz Wetzlar")[0] == "C"
def test_koester_condition_grades():
    from condition_grade import KOESTER_PREFIX
    site = "Foto Köster (독일)"
    assert grade_of(site, KOESTER_PREFIX + "sehr gut", "Leica Tele-Elmarit-M 90mm f2.8")[0] == "A"
    assert grade_of(site, KOESTER_PREFIX + "gut", "Leica Summicron-M 90mm f2.0")[0] == "B"
    assert grade_of(site, KOESTER_PREFIX + "defekt", "Leica Elmar 90mm f4.0 L39 defekt")[0] in ("D", "X")
def test_mfcamera_condition_grades():
    from condition_grade import MFCAMERA_PREFIX
    site = "MF Camera (미국)"
    assert grade_of(site, MFCAMERA_PREFIX + "Like New", "Leica M6 Black Paint")[0] == "S"
    assert grade_of(site, MFCAMERA_PREFIX + "Like New Minus", "Leica M10-R Black Paint")[0] == "A"
    assert grade_of(site, MFCAMERA_PREFIX + "Excellent Plus", "Leica M11 Black")[0] == "B"
    assert grade_of(site, MFCAMERA_PREFIX + "Excellent", "Leica M8 Silver Chrome")[0] == "C"
def test_classicconnection_condition_grades():
    from condition_grade import CLASSICCONNECTION_PREFIX
    site = "Classic Connection (미국)"
    assert grade_of(site, CLASSICCONNECTION_PREFIX + "MINT", "Leica 90mm f2.8 Elmarit-M Late production")[0] == "S"
    assert grade_of(site, CLASSICCONNECTION_PREFIX + "MINT-", "Leica M5 50 Jahre Anniversary black")[0] == "A"
    assert grade_of(site, CLASSICCONNECTION_PREFIX + "EX++", "Leica 50mm f2 Summicron-M black Wetzlar")[0] == "B"
    assert grade_of(site, CLASSICCONNECTION_PREFIX + "EX+", "Leica M3 double stroke")[0] == "C"
    assert grade_of(site, CLASSICCONNECTION_PREFIX + "VG", "Leica IIIc converted to IIIf")[0] == "D"
def test_classiccamera_condition_grades():
    from condition_grade import CLASSICCAMERA_PREFIX
    site = "The Classic Camera (영국)"
    assert grade_of(site, CLASSICCAMERA_PREFIX + "Mint", "Leica M11-D Black Boxed")[0] == "A"
    assert grade_of(site, CLASSICCAMERA_PREFIX + "EXC+++", "Leica 90mm F2 Summicron-M Black")[0] == "B"
    assert grade_of(site, CLASSICCAMERA_PREFIX + "EXC++", "Leica M2 Body Button Rewind Boxed")[0] == "C"
    assert grade_of(site, CLASSICCAMERA_PREFIX + "EXC", "Leitz 13.5cm f4.5 Hektor L39")[0] == "D"

def test_jch_condition_grades():
    from condition_grade import JCH_PREFIX
    site = "Japan Camera Hunter (일본)"
    assert grade_of(site, JCH_PREFIX + "mint", "Leica M4 Black With Box")[0] == "S"
    assert grade_of(site, JCH_PREFIX + "mint minus", "Leica Elmarit-M 28mm f2.8 ASPH 6 bit")[0] == "A"
    assert grade_of(site, JCH_PREFIX + "excellent plus", "Leica M2 Button rewind")[0] == "B"
    assert grade_of(site, JCH_PREFIX + "excellent", "Leica Summilux 50mm f1.4 Type 1")[0] == "C"
    assert grade_of(site, JCH_PREFIX + "good user", "Leica II Black with 50mm Elmar f3.5 Nickel")[0] == "D"
def test_rangefinder_condition_grades():
    from condition_grade import RANGEFINDER_PREFIX
    site = "Rangefinder (홍콩)"
    assert grade_of(site, RANGEFINDER_PREFIX + "99", "Leica Tri-Elmar-M 16-18-21mm f4.0 ASPH")[0] == "S"
    assert grade_of(site, RANGEFINDER_PREFIX + "97", "Leica Summicron-M 50mm f2.0 Black Anodized")[0] == "A"
    assert grade_of(site, RANGEFINDER_PREFIX + "95", "Leica Summilux-M 24mm f1.4 ASPH")[0] == "B"
    assert grade_of(site, RANGEFINDER_PREFIX + "90", "Leica Q3 43 Black")[0] == "C"
    assert grade_of(site, RANGEFINDER_PREFIX + "88", "Leica M3J Black Paint")[0] == "D"
    assert grade_of(site, RANGEFINDER_PREFIX + "New", "Leica M11 Monochrom")[0] == "N"


def test_lecuit_condition_grades():
    from condition_grade import LECUIT_PREFIX
    site = "Lecuit (룩셈부르크)"
    assert grade_of(site, LECUIT_PREFIX + "A", "Leica Summicron-M 50mm f2.0 (11826)")[0] == "A"
    assert grade_of(site, LECUIT_PREFIX + "B", "Leica Elmarit-M 90mm f2.8 (11807)")[0] == "B"
    assert grade_of(site, LECUIT_PREFIX + "C", "Leica Tele-Elmar-M 135mm f4.0")[0] == "C"
    assert grade_of(site, LECUIT_PREFIX + "D", "Leica M4-P silver")[0] == "D"
    assert grade_of(site, LECUIT_PREFIX + "A+", "Leica M11 Monochrom")[0] == "S"
    assert grade_of(site, LECUIT_PREFIX + "Ex-Display", "Leica APO-Summicron-SL 28mm f2.0 ASPH.")[0] == "S"


def test_ohnuki_condition_grades():
    from condition_grade import OHNUKI_PREFIX
    site = "カメラの大貫 (일본)"
    assert grade_of(site, OHNUKI_PREFIX + "B", "Leica M6 0.85 TTL")[0] == "A"
    assert grade_of(site, OHNUKI_PREFIX + "C+", "Leica MP 0.72 Black Paint 10302")[0] == "B"
    assert grade_of(site, OHNUKI_PREFIX + "C", "Leica M2")[0] == "B"
    assert grade_of(site, OHNUKI_PREFIX + "C-", "Leica IIIg")[0] == "C"
    assert grade_of(site, OHNUKI_PREFIX + "D", "Leica M3 ELC")[0] == "C"
    assert grade_of(site, OHNUKI_PREFIX + "E", "Leica IIIf")[0] in ("D", "X")


def test_roterpunkt_condition_grades():
    from condition_grade import ROTERPUNKT_PREFIX
    site = "Roter Punkt (독일)"
    assert grade_of(site, ROTERPUNKT_PREFIX + "A+++", "Leica SUMMICRON-M 28mm ASPH. 6-bit #11672")[0] == "S"
    assert grade_of(site, ROTERPUNKT_PREFIX + "A++", "Leica M10-P silver Body")[0] == "A"
    assert grade_of(site, ROTERPUNKT_PREFIX + "A+", "Leica SUMMARIT-M 75mm f2.5 black 6bit #11645")[0] == "B"
    assert grade_of(site, ROTERPUNKT_PREFIX + "A", "Leica M2 silver Body")[0] == "B"
    assert grade_of(site, ROTERPUNKT_PREFIX + "A-B", "Leica Summilux-M 35mm f1.4 ASPH. FLE 6bit #11663")[0] == "B"
    assert grade_of(site, ROTERPUNKT_PREFIX + "Neuware", "Leica M11 #24030 Thumb Rest black")[0] == "N"


def test_photografica_condition_grades():
    from condition_grade import PHOTOGRAFICA_PREFIX
    site = "Photografica (덴마크)"
    assert grade_of(site, PHOTOGRAFICA_PREFIX + "mint", "Leica Elmar-M 24mm f3.8 ASPH (black)")[0] == "S"
    assert grade_of(site, PHOTOGRAFICA_PREFIX + "excellent", "Leica Summilux-M 24mm f1.4 ASPH BLACK")[0] == "A"
    assert grade_of(site, PHOTOGRAFICA_PREFIX + "very good", "Leica APO-Summicron-M 90mm f2.0 ASPH")[0] == "B"
    assert grade_of(site, PHOTOGRAFICA_PREFIX + "good", "Leica Summilux-M 50mm f1.4 11114")[0] == "B"
    assert grade_of(site, PHOTOGRAFICA_PREFIX + "fair", "Leica Tele-Elmarit-M 90mm f2.8 (Fat)")[0] == "C"
    assert grade_of(site, PHOTOGRAFICA_PREFIX + "new", "Leica D-LUX 8 black")[0] == "N"



def test_suffren_etat_out_of_ten():
    from condition_grade import SUFFREN_PREFIX
    site = "Photo Suffren (프랑스)"
    assert grade_of(site, SUFFREN_PREFIX + "10", "Leica Summicron-SL 35mm f2 Asph")[0] == "S"
    assert grade_of(site, SUFFREN_PREFIX + "9.5", "Leica MP black paint 0,72")[0] == "A"
    assert grade_of(site, SUFFREN_PREFIX + "9", "Leica Summicron-M 35mm f2 Asph.")[0] == "A"
    assert grade_of(site, SUFFREN_PREFIX + "8", "Leica Elmarit-M 90mm f2.8")[0] == "B"
    assert grade_of(site, SUFFREN_PREFIX + "7", "Leitz Elmarit 90mm f2.8 chrome")[0] == "C"


def test_cardinal_condition_grades():
    from condition_grade import CARDINAL_PREFIX, cardinal_condition
    site = "Cardinal Camera Used (미국)"
    assert cardinal_condition("<p>Lens is in absolutely excellent condition. Glass is excellent with no fungus or haze.</p>") == CARDINAL_PREFIX + "absolutely excellent"
    assert cardinal_condition("Lens is in very good condition. Glass is nice with no fungus, haze, or scratches.") == CARDINAL_PREFIX + "very good"
    assert cardinal_condition("Lens is in good shape. Glass does have light haze and a few fungus spots.") == CARDINAL_PREFIX + "good / issue"
    assert cardinal_condition("Camera is being sold as is for parts. Jammed and does not work.") == CARDINAL_PREFIX + "as is"
    # 'works absolutely perfectly'는 작동 설명이라 외관 등급이 아님
    assert cardinal_condition("This is a very special M2. Works absolutely perfectly. Very nice camera.") == CARDINAL_PREFIX + "very good"
    assert grade_of(site, CARDINAL_PREFIX + "absolutely excellent", "Leica MP 0.72")[0] == "A"
    assert grade_of(site, CARDINAL_PREFIX + "excellent", "Leica Summilux-M 35mm")[0] == "B"
    assert grade_of(site, CARDINAL_PREFIX + "good", "Leica M3")[0] == "C"
    assert grade_of(site, CARDINAL_PREFIX + "good / issue", "Leica M3")[0] == "D"
    assert grade_of(site, CARDINAL_PREFIX + "as is", "Leica IIIc")[0] == "X"


def test_fivestar_condition_grades():
    from condition_grade import FIVESTAR_PREFIX, fivestar_condition
    site = "Five Star Camera (일본)"
    page = "<p>【Appearance】 {} *Please refer photo. 【Optic】 No haze. 【Function】 We have inspected each function.</p>"
    best = "There are few scratches or signs of use on the exterior, making it one of the best used models of the same model."
    good = "There are few scratches or signs of use on the exterior. It is in relatively good condition compared to other used products."
    average = "There are scratches and signs of use on the exterior. It is in average condition, typical of a used item."
    worn = "The exterior shows signs of use, including significant paint peeling, rust, and surface rust."
    assert fivestar_condition(page.format(best)) == FIVESTAR_PREFIX + "best"
    assert fivestar_condition(page.format(good)) == FIVESTAR_PREFIX + "good"
    assert fivestar_condition(page.format(average)) == FIVESTAR_PREFIX + "average"
    assert fivestar_condition(page.format(worn)) == FIVESTAR_PREFIX + "worn"
    assert [grade_of(site, FIVESTAR_PREFIX + k, "Leica M4")[0] for k in ("best", "good", "average", "worn", "as is")] == ["A", "B", "B", "C", "X"]


def test_leica_store_amsterdam_condition_grades():
    from condition_grade import LSA_PREFIX, lsa_condition
    site = "Leica Store Amsterdam (네덜란드)"
    # 렌즈 소개 문구('among the best lenses')가 아니라 상태 문장만 봄
    intro = "The APO-SUMMICRON-SL series are among the best lenses Leica even produced. "
    assert lsa_condition(intro + "And this very lens is in great condition, there are some small traces of use visible.") == LSA_PREFIX + "minimal"
    assert lsa_condition("<p>Camera shows some traces of use.</p><p>Condition:</p><p>Some traces of use</p>") == LSA_PREFIX + "some"
    assert lsa_condition("This Leica M2 is in near mint condition.") == LSA_PREFIX + "mint"
    assert lsa_condition("Lens is well used and it has some traces of use visible.") == LSA_PREFIX + "well used"
    assert [grade_of(site, LSA_PREFIX + k, "Leica Q2")[0] for k in ("mint", "minimal", "small", "some", "well used")] == ["S", "A", "B", "C", "D"]
def test_sabatini_condition_grades():
    from condition_grade import SABATINI_PREFIX
    site = "Sabatini Fotografia (이탈리아)"
    assert grade_of(site, SABATINI_PREFIX + "BA", "Leica Summilux-M 50mm f1.4 ASPH")[0] == "A"
    assert grade_of(site, SABATINI_PREFIX + "B+", "Leica Summicron-M 28mm f2 ASPH")[0] == "B"
    assert grade_of(site, SABATINI_PREFIX + "B+/B", "Leica Elmar-M 50mm f2.8")[0] == "C"
    assert grade_of(site, SABATINI_PREFIX + "B", "Leica Vario-Elmar-R 28-70mm F3.5-4.5")[0] == "C"
def test_komehyo_condition_grades():
    from condition_grade import KOMEHYO_PREFIX
    site = "KOMEHYO (일본)"
    assert grade_of(site, KOMEHYO_PREFIX + "中古品A", "Leica SUMMICRON-M 50mm F2.0(VER.4)")[0] == "A"
    assert grade_of(site, KOMEHYO_PREFIX + "中古品B", "Leica M2 self-timer")[0] == "B"
    assert grade_of(site, KOMEHYO_PREFIX + "中古品C", "Leica ELMARIT-M 90mm F2.8")[0] == "C"
def test_konstanz_condition_grades():
    from condition_grade import KONSTANZ_PREFIX, konstanz_condition
    site = "Leica Store Konstanz (독일)"
    assert konstanz_condition("<p>gebraucht &#8211; sehr guter Zustand</p>") == KONSTANZ_PREFIX + "sehr gut"
    assert konstanz_condition("Vorführware &#8211; Neuware &#8211; OVP!") == KONSTANZ_PREFIX + "Vorführware"
    assert konstanz_condition("gebraucht &#8211; neuwertig") == KONSTANZ_PREFIX + "neuwertig"
    assert konstanz_condition("gebrauchter Zustand") == KONSTANZ_PREFIX + "gebraucht"
    assert grade_of(site, KONSTANZ_PREFIX + "neuwertig", "Leica Summicron-M 28mm f2")[0] == "A"
    assert grade_of(site, KONSTANZ_PREFIX + "gut", "Leica M4 silver Body")[0] == "B"
    assert grade_of(site, KONSTANZ_PREFIX + "gebraucht", "Leica M3 silver double stroke Body")[0] == "C"
    assert grade_of(site, KONSTANZ_PREFIX + "Vorführware", "Leica M11-P black Body")[0] == "S"


def test_ms_materiale_grades():
    from condition_grade import MS_PREFIX
    site = "M&S Materiale Fotografico (이탈리아)"
    assert grade_of(site, MS_PREFIX + "A-", "Leica Summilux-M 35mm f1.4 ASPH.")[0] == "A"
    assert grade_of(site, MS_PREFIX + "B+", "Leica M5 Black")[0] == "A"
    assert grade_of(site, MS_PREFIX + "B", "Leica Summicron 50mm f2")[0] == "B"
    assert grade_of(site, MS_PREFIX + "B-", "Leica Elmarit-M 90mm f2.8")[0] == "B"
def test_leicastorepl_condition_grades():
    from condition_grade import LEICASTOREPL_PREFIX, leicastorepl_condition
    site = "Leica Store Poland (폴란드)"
    assert leicastorepl_condition("Leica APO-Summicron-M - Stan Idealny / Pełen Zestaw") == LEICASTOREPL_PREFIX + "idealny"
    assert leicastorepl_condition("Leica M10-P Aparat jest w stanie dobrym. Do aparatu") == LEICASTOREPL_PREFIX + "dobry"
    assert leicastorepl_condition("Obiektyw bez uszkodzeń, w stanie bardzo dobrym") == LEICASTOREPL_PREFIX + "bardzo dobry"
    assert leicastorepl_condition("Leica Summilux-SL 50 - Używany Szukasz") is None
    assert leicastorepl_condition("Leica M10 Monochrom Opis produktu Nowy Rozdział, idealny wybór") is None  # 홍보 글은 상태 아님
    assert grade_of(site, LEICASTOREPL_PREFIX + "bardzo dobry", "Leica M-E (Typ 240)")[0] == "A"
    assert grade_of(site, LEICASTOREPL_PREFIX + "dobry", "Leica M4-2 Black")[0] == "B"
