import importlib.util
from pathlib import Path

# app/ 을 sys.path에 넣으면 'import app'이 app/app.py로 잡혀 다른 테스트가 깨짐 → 파일 경로로 불러옴
_spec = importlib.util.spec_from_file_location("ja_normalize", Path(__file__).resolve().parents[1] / "app" / "ja_normalize.py")
ja = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(ja)


def test_japanese_listing_titles_become_matchable_english():
    cases = {
        "ライカ APO-Summicron-M f2.0/50mm ASPH.": "Leica APO-Summicron-M 50mm f2.0 ASPH.",
        "ライカ Summilux M 1.4/35mm ASPH.B(6bit)": "Leica Summilux M 35mm f1.4 ASPH.B(6bit)",
        "ライカ スーパーAngulonR 21mm F4.0 3-CAM": "Leica Super-Angulon-R 21mm F4.0 3-CAM",
        "ライカ Vario-ElmarT f3.5-5.6/18-56mm ASPH.": "Leica Vario-Elmar-TL 18-56mm f3.5-5.6 ASPH.",
        "ライカ SummicronT f2/23mm ASPH.": "Leica Summicron-TL 23mm f2 ASPH.",
        "ライカ トリElmarM28-35-50mm F4.0 ASPH Black E55": "Leica Tri-Elmar-M 28-35-50mm F4.0 ASPH Black E55",
        "ライカ DII ボディ ブラック": "Leica II (D) Body Black",
        "ライカ A 50mm F3.5": "Leica I (A) 50mm F3.5",
        "ライカ ズミルックスM 50mm F1.4 2代目": "Leica Summilux-M 50mm F1.4 2nd",
        "ライカ D-LUX7用 レザープロテクター Black": "Leica D-LUX7 for Leather Protector Black",
    }
    for ja_title, en in cases.items():
        assert ja.ja_to_en(ja_title) == en, ja_title
