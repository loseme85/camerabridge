"""법적 고지 페이지(scripts/build_legal_pages.py)와 아래쪽 운영자 정보가 빠짐없이 나오는지."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import build_legal_pages as lp  # noqa: E402


def test_pages_exist_with_operator_footer(tmp_path):
    written = lp.build(tmp_path)
    assert len(written) == len(lp.LANGS) * 3 + 1
    for lang in lp.LANGS:
        for name in ("about", "privacy", "terms"):
            page = (tmp_path / lang / name / "index.html").read_text(encoding="utf-8")
            assert f'<html lang="{lang}">' in page
            assert lp.OPERATOR["email"] in page
            assert 'href="/impressum/"' in page and "Leica Camera AG" in page
        about = (tmp_path / lang / "about" / "index.html").read_text(encoding="utf-8")
        assert lp.OPERATOR["biz_no"] in about and lp.OPERATOR["rep"][lang] in about
    impressum = (tmp_path / "impressum" / "index.html").read_text(encoding="utf-8")
    assert "§ 5" in impressum and lp.OPERATOR["address"]["en"] in impressum


def test_footer_shows_brand_only():
    for lang in lp.LANGS:
        foot = lp.footer(lang)
        assert lp.OPERATOR["brand"] in foot and lp.OPERATOR["email"] in foot
        assert lp.OPERATOR["biz_no"] not in foot and lp.OPERATOR["rep"][lang] not in foot
        assert lp.OPERATOR["name"][lang] not in foot


def test_empty_optional_fields_are_hidden():
    about = "".join(lp.about_body("ko"))
    if lp.OPERATOR["mail_order_no"]:
        assert lp.OPERATOR["mail_order_no"] in about
    else:
        assert "통신판매업" not in about


def test_committed_pages_match_generator(tmp_path):
    lp.build(tmp_path)
    for path in tmp_path.rglob("index.html"):
        committed = ROOT / path.relative_to(tmp_path)
        assert committed.read_text(encoding="utf-8") == path.read_text(encoding="utf-8"), committed


def test_home_page_has_legal_footer():
    beta = (ROOT / "beta.html").read_text(encoding="utf-8")
    assert beta == (ROOT / "app/templates/beta.html").read_text(encoding="utf-8")
    for page in ("about", "privacy", "terms"):
        assert f'data-legal-page="{page}"' in beta
    assert 'href="/impressum/"' in beta and "thehingemeta" in beta
    assert lp.OPERATOR["biz_no"] not in beta and "박창대" not in beta and "브로콜리" not in beta
