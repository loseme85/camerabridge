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
    assert 0 < len(models) <= mp.MAX_PAGES
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


def test_variants_shop_table_and_lastmod(tmp_path):
    result = mp.build(tmp_path)
    models = result["models"]
    # 세대·버전은 부모와 따로 페이지 (M6 → M6 Classic·M6 TTL), 주소는 겹치지 않음
    assert {"m6", "m6-classic", "m6-ttl"} <= set(models)
    page = (tmp_path / "en" / "leica" / "m6-ttl" / "index.html").read_text(encoding="utf-8")
    assert "Prices by shop" in page and "Model info" in page and '"BreadcrumbList"' in page
    assert 'href="/en/leica/m6/"' in page  # 부모 페이지로 가는 링크
    # lastmod는 페이지마다 있고 사이트맵에 그대로 들어감
    sitemap = (tmp_path / "sitemap.xml").read_text(encoding="utf-8")
    url = mp.page_url("en", "m6-ttl")
    assert f"<loc>{url}</loc><lastmod>{result['lastmod'][url]['d']}</lastmod>" in sitemap
    # 시험 출력은 실제 lastmod 기록을 건드리지 않음
    assert not (tmp_path / "data").exists()
