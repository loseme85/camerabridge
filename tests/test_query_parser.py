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
    assert intent["aperture"] == "2.8"
    assert {"type": "aperture_hint", "raw": "21/2.8", "value": "2.8"} in intent["tokens"]


def test_standalone_aperture_query() -> None:
    intent = parse_query("leica 50mm 1.2 m")
    assert intent["focal_length"] == "50"
    assert intent["aperture"] == "1.2"
    assert intent["mount"] == "M"
    assert {"type": "aperture", "raw": "1.2", "value": "1.2"} in intent["tokens"]
    assert not any(token["raw"] == "1.2" and token["type"] == "unknown" for token in intent["tokens"])


def test_prefixed_aperture_forms_query() -> None:
    f_plain = parse_query("leica 50mm f1.2 1st")
    f_slash = parse_query("leica 50mm f/1.2 1st")
    noct = parse_query("leica 50mm 0.95 m")
    f_one = parse_query("leica 50mm 1.0 m")

    assert f_plain["aperture"] == "1.2"
    assert f_slash["aperture"] == "1.2"
    assert noct["aperture"] == "0.95"
    assert f_one["aperture"] == "1.0"
    assert f_plain["generation"] == "1st"


def test_short_leica_cm_alias_query() -> None:
    intent = parse_query("leica cm")
    assert intent["model_family"] == "CM"
    assert intent["system"] == "PNS"
    assert not any(token["raw"] == "cm" and token["type"] == "unknown" for token in intent["tokens"])


def test_mp3_silver_search_intent() -> None:
    intent = parse_query("mp3 silver")
    assert intent["model_family"] == "MP3"
    assert "Silver" in intent["variant"]


def test_hood_accessory_intent_query() -> None:
    for query in ["leica hood", "lens hood", "후드", "hood for 50mm"]:
        intent = parse_query(query)
        assert intent["accessory_intent"] == "hood"
        assert {"type": "accessory_intent", "raw": "lens hood" if query == "lens hood" else ("후드" if query == "후드" else "hood"), "value": "hood"} in intent["tokens"]
        assert not any(token["raw"] in {"hood", "후드", "for"} and token["type"] == "unknown" for token in intent["tokens"])


def test_hood_accessory_code_is_contextual() -> None:
    hood = parse_query("12586 hood")
    bare = parse_query("12586")

    assert hood["accessory_intent"] == "hood"
    assert hood["accessory_code"] == "12586"
    assert {"type": "accessory_code", "raw": "12586", "value": "12586"} in hood["tokens"]
    assert bare["accessory_code"] is None
    assert any(token["raw"] == "12586" and token["type"] == "unknown" for token in bare["tokens"])


if __name__ == "__main__":
    test_search_layer_does_not_import_classifier()
    test_compact_lux_aa_query()
    test_generation_alias_query()
    test_filter_size_query()
    test_korean_optical_formula_query()
    test_slash_focal_shorthand_query()
    test_standalone_aperture_query()
    test_prefixed_aperture_forms_query()
    test_short_leica_cm_alias_query()
    test_mp3_silver_search_intent()
    test_hood_accessory_intent_query()
    test_hood_accessory_code_is_contextual()
    print("test_query_parser: ok")
