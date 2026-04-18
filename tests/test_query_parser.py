from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from query_parser import parse_query


def test_search_layer_does_not_import_classifier() -> None:
    assert "classifier_v2" not in sys.modules


def test_compact_lux_aa_query() -> None:
    intent = parse_query("35lux aa")
    assert intent["model_family"] == "Summilux"
    assert intent["focal_length"] == "35"
    assert "AA" in intent["variant"]


def test_generation_alias_query() -> None:
    intent = parse_query("50cron 2nd")
    assert intent["model_family"] == "Summicron"
    assert intent["focal_length"] == "50"
    assert intent["generation"] == "2nd"


def test_filter_size_query() -> None:
    intent = parse_query("nocti e60")
    assert intent["model_family"] == "Noctilux"
    assert intent["filter_size"] == "E60"


def test_korean_optical_formula_query() -> None:
    intent = parse_query("6군8매")
    assert intent["optical_formula"] == "6 groups / 8 elements"
    assert "8-element" in intent["variant"]


def test_slash_focal_shorthand_query() -> None:
    intent = parse_query("m 21/2.8")
    assert intent["mount"] == "M"
    assert intent["focal_length"] == "21"
    assert {"type": "aperture_hint", "raw": "21/2.8", "value": "2.8"} in intent["tokens"]


def test_mp3_silver_search_intent() -> None:
    intent = parse_query("mp3 silver")
    assert intent["model_family"] == "MP3"
    assert "Silver" in intent["variant"]


if __name__ == "__main__":
    test_search_layer_does_not_import_classifier()
    test_compact_lux_aa_query()
    test_generation_alias_query()
    test_filter_size_query()
    test_korean_optical_formula_query()
    test_slash_focal_shorthand_query()
    test_mp3_silver_search_intent()
    print("test_query_parser: ok")
