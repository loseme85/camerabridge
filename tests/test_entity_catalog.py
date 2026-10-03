from __future__ import annotations

import json
from pathlib import Path

from entity_catalog import Suggester, load_catalog, match_entities

ROOT = Path(__file__).resolve().parents[1]


def _record(title: str, category: str = "Lens", mount: str | None = "M") -> dict:
    return {"final_output": {"title_raw": title, "category": category, "mount": mount}}


def test_listing_links_to_exact_model_and_parent() -> None:
    ids = match_entities(_record("[중고] M 35/1.4 Summilux ASPH 6bit FLE2 (Black)"))
    assert "leica:lens:summilux-m:35:asph-fle2" in ids
    assert "leica:lens:summilux-m:35" in ids
    assert "leica:lens:summilux-m:35:asph-fle" not in ids


def test_noctilux_is_not_summilux_and_copies_are_excluded() -> None:
    assert "leica:lens:summilux-m:50:asph" not in match_entities(_record("[중고] M 50/0.95 Noctilux ASPH 6bit (Black)"))
    assert match_entities(_record("Leeworks M 50mm f1.1 Noctilux M Silver")) == []
    assert "leica:lens:noctilux-m:50:f1.0" in match_entities(_record("LEICA 50mm F1.0 NOCTILUX-M sn.3220"))


def test_korean_shop_body_misfiled_as_lens_still_links_but_accessories_do_not() -> None:
    assert "leica:body:m7" in match_entities(_record("[중고] M7 0.72 (Black)", category="Lens"))
    assert match_entities(_record("[중고] JNK M7 케이스 (Brown)", category="Accessory")) == []
    assert "leica:body:m10" not in match_entities(_record("[중고] Leica M10 하프케이스 (Black)", category="Body"))


def test_edition_numbers_are_not_focal_lengths() -> None:
    ids = match_entities(_record("LEICA 35mm F2 ASPH SUMMICRON-M sn.4618 (33/50)"))
    assert "leica:lens:summicron-m:35:asph" in ids
    assert "leica:lens:summicron-m:50:current" not in ids


def _suggester() -> Suggester:
    summary = ROOT / "data" / "derived" / "entity_summary_v1.json"
    return Suggester(json.loads(summary.read_text(encoding="utf-8"))["entities"])


def test_suggest_understands_shorthand_korean_typos_and_units() -> None:
    s = _suggester()
    assert s.suggest("m6 ttl 0.72", 1)[0]["id"] == "leica:body:m6:ttl"
    assert s.suggest("주미룩스 35 fle", 1)[0]["id"] == "leica:lens:summilux-m:35:asph-fle"
    assert s.suggest("notilux 0.95", 1)[0]["id"] == "leica:lens:noctilux-m:50:f0.95"
    assert s.suggest("summicron 90mm", 1)[0]["id"] == "leica:lens:summicron-m:90"
    assert s.suggest("엠6", 1)[0]["id"] == "leica:body:m6"


def test_suggest_does_not_fill_nonexistent_models() -> None:
    s = _suggester()
    assert s.suggest("summilux 135", 3) == []
    assert s.suggest("24 cron", 3) == []
    assert s.suggest("summicron sl 24", 3) == []


def test_catalog_entities_have_aliases_and_rules() -> None:
    catalog = load_catalog()
    for entity in catalog["entities"].values():
        assert entity["aliases"], entity["id"]
        assert entity["match"] or entity["children"], entity["id"]
