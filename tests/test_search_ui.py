from __future__ import annotations

from pathlib import Path


INDEX_PATH = Path(__file__).resolve().parents[1] / "app/templates/index.html"


def _html() -> str:
    return INDEX_PATH.read_text(encoding="utf-8")


def test_index_calls_search_endpoint() -> None:
    html = _html()
    assert "fetch('/api/search?'" in html
    assert "search_records" not in html


def test_index_does_not_reimplement_legacy_search() -> None:
    html = _html()
    assert "data/raw/results.json" not in html
    assert "function matchesQuery" not in html
    assert "function normalizeQuery" not in html
    assert "classifier_v2" not in html


def test_required_ui_controls_exist() -> None:
    html = _html()
    for element_id in [
        "query-input",
        "category-filter",
        "brand-filter",
        "mount-filter",
        "sold-filter",
        "sort-select",
        "results-grid",
        "prev-button",
        "next-button",
    ]:
        assert f'id="{element_id}"' in html


def test_demo_queries_are_available() -> None:
    html = _html()
    for query in ["mp3 silver", "q3 28", "ltm summaron 35", "35lux aa"]:
        assert f'data-query="{query}"' in html


if __name__ == "__main__":
    test_index_calls_search_endpoint()
    test_index_does_not_reimplement_legacy_search()
    test_required_ui_controls_exist()
    test_demo_queries_are_available()
    print("test_search_ui: ok")
