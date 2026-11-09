"""모델별 시세 페이지(scripts/build_model_pages.py)가 언어별로 짝을 맞춰 만들어지는지."""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import build_model_pages as mp  # noqa: E402


def test_pages_sitemap_and_hreflang(tmp_path):
    result = mp.build(tmp_path)
    models = result["models"]
    assert len(models) > 0  # 기존 공개 주소는 신규 후보 수 제한과 별도로 유지
    assert len(set(models)) == len(models)
    for lang in mp.LANGS:
        path = mp.PATH[lang]  # 2026-11-08: 9개 언어, 주소는 소문자 (/zh-hans/)
        assert (tmp_path / path / "leica" / "index.html").exists()
        page = (tmp_path / path / "leica" / models[0] / "index.html").read_text(encoding="utf-8")
        assert f'<html lang="{lang}">' in page
        assert f'rel="canonical" href="https://camerabridge.io/{path}/leica/{models[0]}/"' in page
        assert sorted(re.findall(r'hreflang="([^"]+)"', page)) == sorted(list(mp.LANGS) + ["x-default"])
        assert '<p class="lead">' in page  # 한 줄 답
    assert (tmp_path / "llms.txt").read_text(encoding="utf-8").startswith("# Camera Bridge")
    sitemap = (tmp_path / "sitemap.xml").read_text(encoding="utf-8")
    assert sitemap.count("<url>") == 1 + (len(models) + 1) * len(mp.LANGS)
    assert "<loc>https://camerabridge.io/</loc>" in sitemap
    # Search Console 404로 신고된 세 모델은 모든 언어에서 복원되어야 한다.
    for slug in ("x2-standard", "m4-50-jahre", "m6-leitz-wetzlar"):
        assert slug in models
        for lang in mp.LANGS:
            assert (tmp_path / mp.PATH[lang] / "leica" / slug / "index.html").exists()
            assert f"<loc>{mp.page_url(lang, slug)}</loc>" in sitemap


def test_listing_filters():
    assert mp.condition_text("Harrison: Good") == "Good"
    assert mp.condition_text("정보없음") == "—"
    assert mp.RENTAL.search("Leica M6 + 35mm f2 Summicron lens – Rental")
    assert not mp.RENTAL.search("Leica M6 Classic black")
    assert mp.money(239005, "KRW", "ko", approx=True) == "239,000원"
    assert mp.shop_parts("Calumet (독일)") == ("Calumet", "독일")
    assert mp.shop_parts("국민카메라") == ("국민카메라", "한국")
    assert mp.shop_parts("Lampersky (헝가리)") == ("Lampersky", "헝가리")  # 예전엔 나라 이름표가 없어 '한국'으로 나옴
    for country in mp.COUNTRY.values():
        assert set(mp.LANGS) <= set(country), country


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


def test_vercel_exclude_files_within_limit():
    """vercel.json functions.excludeFiles는 256자까지 (넘으면 배포 전체가 실패 — 2026-11-08 9개 언어 추가 때 실제로 일어남)"""
    import json
    from pathlib import Path
    conf = json.loads((Path(__file__).resolve().parents[1] / "vercel.json").read_text(encoding="utf-8"))
    for spec in conf.get("functions", {}).values():
        assert len(spec.get("excludeFiles", "")) <= 256


def test_published_urls_survive_stock_rank_and_standard_ratio_changes(monkeypatch):
    def model(eid, active, total, **extra):
        return {"id": eid, "kind": "Body", "active_count": active, "listing_count": total, **extra}

    entities = [model("leica:body:parent", 20, 30),
                model("leica:body:parent:standard", 8, 21, parent="leica:body:parent"),
                model("leica:body:rare", 0, 5),
                model("leica:body:runner-up", 3, 10),
                model("leica:body:new-thin", 2, 2)]
    monkeypatch.setattr(mp, "MAX_PAGES", 1)
    assert [e["id"] for e in mp.pick_entities(entities)] == ["leica:body:parent"]
    published = {"leica:body:parent:standard", "leica:body:rare", "leica:body:runner-up"}
    assert {e["id"] for e in mp.pick_entities(entities, published)} == published | {"leica:body:parent"}


def test_retained_empty_page_uses_current_data_and_dry_run_preserves_registry(tmp_path, monkeypatch):
    summary = json.loads(mp.SUMMARY.read_text(encoding="utf-8"))
    entity = next(e for e in summary["entities"] if e["id"] == "leica:body:m4:50-jahre")
    entity.update(active_count=0, sold_median_krw=None, sold_price_count=0)
    summary["entities"] = [entity]
    source = tmp_path / "source"
    source.mkdir()
    summary_path, index_path = source / "summary.json", source / "index.json"
    registry, lastmod = source / "published.json", source / "lastmod.json"
    summary_path.write_text(json.dumps(summary))
    index_path.write_text(json.dumps({"records": []}))
    registry.write_text(json.dumps({"entity_ids": [entity["id"]]}))
    # 기존 lastmod로부터 공개 이력을 복구할 때도 수량 기준으로 삭제되지 않는다.
    lastmod.write_text(json.dumps({mp.page_url("ko", "m4-50-jahre"): {"h": "old", "d": "2026-11-01"}}))
    before = registry.read_bytes(), lastmod.read_bytes()
    for key, value in (("SUMMARY", summary_path), ("INDEX", index_path), ("PUBLISHED", registry), ("LASTMOD", lastmod)):
        monkeypatch.setattr(mp, key, value)
    output = tmp_path / "site"
    result = mp.build(output)
    assert result["models"] == ["m4-50-jahre"]
    page = (output / "en/leica/m4-50-jahre/index.html").read_text()
    assert mp.T["en"]["none"] in page
    assert mp.T["en"]["active_val"].format(n=0, shops=0) in page
    assert '"AggregateOffer"' not in page
    assert "Leica M4 50 Jahre" in page
    assert (registry.read_bytes(), lastmod.read_bytes()) == before
    registry.write_text(json.dumps({"entity_ids": []}))
    assert mp.build(output)["models"] == ["m4-50-jahre"]
