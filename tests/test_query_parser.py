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


def test_filter_accessory_intent_query() -> None:
    examples = {
        "uv filter": "uv filter",
        "nd filter": "nd filter",
        "b+w filter": "b+w filter",
        "e39 filter": "filter_thread",
        "skylight filter": "skylight filter",
        "필터": "필터",
        "uva": "uva",
        "uvir": "uvir",
    }

    for query, raw in examples.items():
        intent = parse_query(query)
        assert intent["accessory_intent"] == "filter"
        assert {"type": "accessory_intent", "raw": raw, "value": "filter"} in intent["tokens"]
        assert not any(token["type"] == "unknown" and token["raw"] in {"filter", "필터", "uv", "uva", "uvir", "nd", "skylight"} for token in intent["tokens"])


def test_filter_thread_context_does_not_turn_all_filter_sizes_into_accessories() -> None:
    e39 = parse_query("e39 filter")
    nocti = parse_query("nocti e60")

    assert e39["accessory_intent"] == "filter"
    assert e39["filter_size"] == "E39"
    assert nocti["accessory_intent"] is None
    assert nocti["model_family"] == "Noctilux"
    assert nocti["filter_size"] == "E60"


def test_a36_color_filter_intent_is_contextual() -> None:
    a36 = parse_query("a36 orange")
    bare_color = parse_query("orange")

    assert a36["accessory_intent"] == "filter"
    assert a36["filter_size"] == "A36"
    assert {"type": "filter_color", "raw": "orange", "value": "orange"} in a36["tokens"]
    assert not any(token["type"] == "unknown" for token in a36["tokens"])
    assert bare_color["accessory_intent"] is None
    assert any(token["type"] == "unknown" and token["raw"] == "orange" for token in bare_color["tokens"])


def test_adapter_accessory_intent_query() -> None:
    examples = {
        "adapter": "adapter",
        "adaptor": "adaptor",
        "mount adapter": "mount adapter",
        "adapter ring": "adapter ring",
        "m-l adapter": "m-l adapter",
        "m to l adapter": "m to l adapter",
        "macro adapter m": "macro adapter m",
        "leica m adapter": "leica m adapter",
    }

    for query, raw in examples.items():
        intent = parse_query(query)
        assert intent["accessory_intent"] == "adapter"
        assert {"type": "accessory_intent", "raw": raw, "value": "adapter"} in intent["tokens"]

    m_to_l = parse_query("m to l adapter")
    assert m_to_l["mount"] is None
    assert {"type": "adapter_detail", "raw": "m to l adapter", "value": "m-l"} in m_to_l["tokens"]
    assert not any(token["type"] == "unknown" and token["raw"] in {"m", "to", "l", "adapter"} for token in m_to_l["tokens"])

    macro = parse_query("macro adapter m")
    assert macro["mount"] is None
    assert {"type": "adapter_detail", "raw": "macro adapter m", "value": "macro"} in macro["tokens"]
    assert not any(token["type"] == "unknown" and token["raw"] in {"macro", "adapter", "m"} for token in macro["tokens"])


def test_mount_token_alone_does_not_create_adapter_intent() -> None:
    intent = parse_query("m")
    assert intent["accessory_intent"] is None
    assert intent["mount"] == "M"


def test_finder_accessory_intent_query() -> None:
    examples = {
        "finder": "finder",
        "viewfinder": "viewfinder",
        "brightline finder": "brightline finder",
        "external finder": "external finder",
        "visoflex": "visoflex",
        "28mm finder": "finder",
        "35mm finder": "finder",
        "파인더": "파인더",
    }

    for query, raw in examples.items():
        intent = parse_query(query)
        assert intent["accessory_intent"] == "finder"
        assert {"type": "accessory_intent", "raw": raw, "value": "finder"} in intent["tokens"]
        assert not any(
            token["type"] == "unknown" and token["raw"] in {"finder", "viewfinder", "brightline", "external", "visoflex", "파인더"}
            for token in intent["tokens"]
        )

    assert parse_query("28mm finder")["focal_length"] == "28"
    assert parse_query("35mm finder")["focal_length"] == "35"


def test_code_only_finder_aliases_are_deferred() -> None:
    for query in ["sbooi", "vidom", "fokos"]:
        intent = parse_query(query)
        assert intent["accessory_intent"] is None
        assert any(token["type"] == "unknown" and token["raw"] == query for token in intent["tokens"])


def test_body_shorthand_intent_query() -> None:
    examples = {
        "m2": ("M2", "M", None),
        "m3": ("M3", "M", None),
        "m4": ("M4", "M", None),
        "m5": ("M5", "M", None),
        "m6": ("M6", "M", None),
        "mp": ("MP", "M", None),
        "r6": ("R6", "R", None),
        "r7": ("R7", "R", None),
        "r8": ("R8", "R", None),
        "q2": ("Q2", None, "Q"),
        "q3": ("Q3", None, "Q"),
        "barnack": ("Barnack", "L", None),
        "iiic": ("IIIc", "L", None),
        "iiif": ("IIIf", "L", None),
        "iiig": ("IIIg", "L", None),
    }

    for query, (body_intent, mount, system) in examples.items():
        intent = parse_query(query)
        assert intent["body_intent"] == body_intent
        assert intent["mount"] == mount
        assert intent["system"] == system
        assert {"type": "body_intent", "raw": query, "value": body_intent} in intent["tokens"]
        assert not any(token["type"] == "unknown" and token["raw"] == query for token in intent["tokens"])
        assert "no_structured_search_intent" not in intent["warnings"]


def test_body_shorthand_does_not_override_existing_lens_or_accessory_intent() -> None:
    mp3 = parse_query("mp3 silver")
    lens = parse_query("m 21/2.8")
    adapter = parse_query("m to l adapter")
    compatibility = parse_query("vit for m2")

    assert mp3["model_family"] == "MP3"
    assert mp3["body_intent"] is None
    assert lens["mount"] == "M"
    assert lens["body_intent"] is None
    assert adapter["accessory_intent"] == "adapter"
    assert adapter["body_intent"] is None
    assert compatibility["body_intent"] is None


def test_compact_body_line_normalization_query() -> None:
    examples = {
        "d lux 8": "D-LUX 8",
        "d-lux 8": "D-LUX 8",
        "dlux 8": "D-LUX 8",
        "leica d-lux 8": "D-LUX 8",
        "d-lux": "D-LUX",
        "v-lux": "V-LUX",
        "v lux": "V-LUX",
        "c-lux": "C-LUX",
        "c lux": "C-LUX",
        "sofort": "Sofort",
    }

    for query, body_intent in examples.items():
        intent = parse_query(query)
        assert intent["body_intent"] == body_intent
        assert intent["system"] == "Compact"
        assert intent["model_family"] is None
        assert not any(token["type"] == "unknown" and token["raw"] in {"d", "v", "c", "lux", "8"} for token in intent["tokens"])
        assert "no_structured_search_intent" not in intent["warnings"]


def test_d_lux_phrase_does_not_parse_lux_as_summilux() -> None:
    intent = parse_query("d lux 8")

    assert intent["body_intent"] == "D-LUX 8"
    assert intent["model_family"] is None
    assert not any(token["type"] == "model_family" and token["raw"] == "lux" for token in intent["tokens"])


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
    test_filter_accessory_intent_query()
    test_filter_thread_context_does_not_turn_all_filter_sizes_into_accessories()
    test_a36_color_filter_intent_is_contextual()
    test_adapter_accessory_intent_query()
    test_mount_token_alone_does_not_create_adapter_intent()
    test_finder_accessory_intent_query()
    test_code_only_finder_aliases_are_deferred()
    test_body_shorthand_intent_query()
    test_body_shorthand_does_not_override_existing_lens_or_accessory_intent()
    test_compact_body_line_normalization_query()
    test_d_lux_phrase_does_not_parse_lux_as_summilux()
    print("test_query_parser: ok")
