"""모델 페이지: 한정판·기념판·희귀 사양·세트는 위쪽 범위에서 빼고 따로 (2026-11-12 사장님: M6 범위 최대 $31,233이 일반 M6 값과 안 맞음)"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
from build_model_pages import is_special  # noqa: E402

M6 = {"id": "leica:body:m6", "kind": "Body"}
Q2 = {"id": "leica:body:q2", "kind": "Body"}
CRON35 = {"id": "leica:lens:summicron-m:35", "kind": "Lens"}


def row(title, eids=()):
    return {"title": title, "eids": set(eids)}


def test_editions_and_sets_are_special():
    assert is_special(row("Leica M6 TTL 0.85 Øresundsbron Black Paint set with Summilux-M 50mm f1.4 10492"), M6, set())
    assert is_special(row("Leica 【世界300台 Limited品】M6 TTL 0.85 GreenPaint 10478"), M6, set())
    assert is_special(row("Leica M6 TTL (0.85) サファリ"), M6, set())
    assert is_special(row("Leica M6 Titan", ["leica:body:m6:titan"]), M6, {"leica:body:m6:titan"})
    assert is_special(row("Leica M6J Elmar M 50/2.8"), M6, set())


def test_plain_listings_are_not_special():
    assert not is_special(row("Leica M6 0.72x Black Body Only"), M6, set())
    assert not is_special(row("Used Leica M6, black (2022 Edition)"), M6, set())
    assert not is_special(row("Leica Q2 mit SUMMILUX-M 28mm F1.7 ASPH."), Q2, set())
    assert not is_special(row("Leica Summicron 35mm f2 chrome (8-element) with M3 goggles"), CRON35, set())
    assert not is_special(row("Leica Summicron - M 8 Element 35mm f2.0 with glasses"), CRON35, set())


def test_lens_with_body_is_a_set():
    assert is_special(row("Leica M3 + Summicron 35 f2 set"), CRON35, set())
