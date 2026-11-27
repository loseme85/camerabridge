"""'Pre-ASPH'(비구면 이전 구형) 매물은 ASPH 모델에 들어가면 안 된다 (2026-11-27 전수 점검: 5개 모델 50건)."""
from __future__ import annotations

import pytest

import entity_catalog as ec
from model_detector import detect_model


def _first(title: str, **final) -> list[str]:
    final = {"category": "Lens", "mount": "M", **final}
    return ec.match_entities({"title": title, "final_output": final})


@pytest.mark.parametrize("title", [
    "Leica Elmarit-M 21mm f2.8 Pre-Asph 11134",
    "Leica Elmarit-M 28mm F2.8 V4 E46 (Pre-ASPH)",
    "Leica Summilux-M 35mm f/1.4 Pre-ASPH Germany",
    "Leica Summilux-M 50mm F1.4 Pre-Asph Black",
    "Leica M 50mm f/1.4 SUMMILUX-M Pre ASPH E46 Silver Chrome",
    "Leica Summicron-M 35mm F/2 v4 Pre-Asph (7 elements) king of bokeh",
])
def test_pre_asph_title_never_matches_asph_model(title: str) -> None:
    ids = _first(title)
    assert ids, title
    assert not [i for i in ids if ":asph" in i], (title, ids)


def test_real_asph_still_matches_asph_model() -> None:
    assert "leica:lens:elmarit-m:21:asph" in _first("Leica Elmarit-M 21mm f2.8 ASPH 6bit")
    assert any(":asph" in i for i in _first("Leica Summilux-M 50mm f/1.4 ASPH Black"))


def test_pre_asph_variant_has_no_plain_asph() -> None:
    assert detect_model("leica elmarit-m 21mm f2.8 pre-asph 11134", None, "lens", "M")["variant"] == ["Pre-ASPH"]
    assert "ASPH" in detect_model("leica summilux-m 35mm f1.4 asph fle", None, "lens", "M")["variant"]
    # 세트에 ASPH 렌즈가 따로 있으면 ASPH도 남김
    both = detect_model("leica black paint set summicron-m 35/2 asph + summilux-m 50/1.4 pre-asph", None, "lens", "M")["variant"]
    assert "ASPH" in both and "Pre-ASPH" in both


@pytest.mark.parametrize("title", [
    "Leica Summilux-M 35mm f1.4 ASPH Pre-FLE 11874",
    "Leica Summilux 35mm F1.4 Black (Pre-Fle) 11874",
    "Leica Summilux-M 35mm F/1.4 ASPH. PRE-FLE E46 Lens 6Bit Black",
    "Leica Summilux 35mm f1.4 Aspherical (11874 pre FLE)",
])
def test_pre_fle_is_4th_gen_asph(title: str) -> None:
    """'Pre-FLE' = FLE 이전 ASPH 4세대(1994). FLE 글자로 FLE 모델에 가면 안 됨 (2026-11-28)."""
    assert _first(title)[0] == "leica:lens:summilux-m:35:asph-1994", title


def test_real_fle_still_fle() -> None:
    assert _first("Leica Summilux-M 35mm f/1.4 ASPH FLE Black 11663")[0] == "leica:lens:summilux-m:35:asph-fle"
