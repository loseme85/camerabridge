"""모델별 시세 페이지(scripts/build_model_pages.py)가 언어별로 짝을 맞춰 만들어지는지."""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import build_model_pages as mp  # noqa: E402


def test_pages_sitemap_and_hreflang(tmp_path):
    result = mp.build(tmp_path)
    models = result["models"]
    assert len(models) == mp.PAGE_COUNT
    assert len(set(models)) == len(models)
    for lang in mp.LANGS:
        assert (tmp_path / lang / "leica" / "index.html").exists()
        page = (tmp_path / lang / "leica" / models[0] / "index.html").read_text(encoding="utf-8")
        assert f'<html lang="{lang}">' in page
        assert f'rel="canonical" href="https://camerabridge.io/{lang}/leica/{models[0]}/"' in page
        assert sorted(re.findall(r'hreflang="([^"]+)"', page)) == ["en", "ja", "ko", "x-default"]
    sitemap = (tmp_path / "sitemap.xml").read_text(encoding="utf-8")
    assert sitemap.count("<url>") == 1 + (len(models) + 1) * len(mp.LANGS)
    assert "<loc>https://camerabridge.io/</loc>" in sitemap


def test_listing_filters():
    assert mp.condition_text("Harrison: Good") == "Good"
    assert mp.condition_text("정보없음") == "—"
    assert mp.RENTAL.search("Leica M6 + 35mm f2 Summicron lens – Rental")
    assert not mp.RENTAL.search("Leica M6 Classic black")
    assert mp.money(239005, "KRW", "ko", approx=True) == "239,000원"
    assert mp.shop_parts("Calumet (독일)") == ("Calumet", "독일")
    assert mp.shop_parts("국민카메라") == ("국민카메라", "한국")
