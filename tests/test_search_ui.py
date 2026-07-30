from __future__ import annotations

from pathlib import Path
import re


PROJECT_ROOT = Path(__file__).resolve().parents[1]
INDEX_PATHS = [
    PROJECT_ROOT / "app/templates/index.html",
    PROJECT_ROOT / "index.html",
]
BETA_PATHS = [
    PROJECT_ROOT / "app/templates/beta.html",
    PROJECT_ROOT / "beta.html",
]
ALL_HTML_PATHS = INDEX_PATHS + BETA_PATHS
APP_PY_PATH = PROJECT_ROOT / "app/app.py"


def _html_files(paths: list[Path] | None = None) -> list[str]:
    active_paths = paths or ALL_HTML_PATHS
    return [path.read_text(encoding="utf-8") for path in active_paths]


def _function_body(html: str, function_name: str) -> str:
    match = re.search(
        rf"function {re.escape(function_name)}\([^)]*\)\{{(?P<body>.*?)\n    \}}",
        html,
        re.DOTALL,
    )
    assert match, f"Missing function body for {function_name}"
    return match.group("body")


def test_index_calls_search_endpoint() -> None:
    for html in _html_files():
        assert "fetch('/api/search?'" in html
        assert "search_records" not in html


def test_public_routes_use_beta_shell_and_qa_uses_internal_shell() -> None:
    app_py = APP_PY_PATH.read_text(encoding="utf-8")
    assert '@app.route("/")' in app_py
    assert '@app.route("/search")' in app_py
    assert 'def index() -> str:\n    return render_template("beta.html")' in app_py
    assert '@app.route("/qa")' in app_py
    assert 'def qa_index() -> str:\n    return render_template("index.html")' in app_py
    assert '@app.route("/beta")' in app_py
    assert 'def beta_index() -> str:\n    return render_template("beta.html")' in app_py


def test_index_does_not_reimplement_legacy_search() -> None:
    for html in _html_files():
        assert "data/raw/results.json" not in html
        assert "function matchesQuery" not in html
        assert "function normalizeQuery" not in html
        assert "classifier_v2" not in html


def test_required_ui_controls_exist() -> None:
    for html in _html_files():
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


def test_beta_files_include_locale_switcher() -> None:
    for html in _html_files(BETA_PATHS):
        assert 'id="locale-select"' in html
        assert "SUPPORTED_LOCALES" in html


def test_demo_queries_are_available() -> None:
    for html in _html_files(INDEX_PATHS):
        for query in ["mp3 silver", "q3 28", "ltm summaron 35", "35lux aa"]:
            assert f'data-query="{query}"' in html


def test_quality_summary_message_is_consumed_from_api() -> None:
    for html in _html_files(INDEX_PATHS):
        assert "result_quality_summary" in html
        assert "quality.display_message" in html
        assert "match_quality ===" not in html
    for html in _html_files(BETA_PATHS):
        assert "result_quality_summary" in html
        assert "function getQualitySummary()" in html
        assert "quality.display_message" not in html


def test_market_entry_policy_merges_top_level_runtime_overrides() -> None:
    for html in _html_files():
        assert "const apiPolicy = state.response.market_entry_policy || {};" in html
        assert "...apiPolicy," in html


def test_exact_generation_headline_and_label_mappings_exist() -> None:
    for html in _html_files():
        assert "Exact generation price" in html
        assert "exact generation match visible, but not selected for exact price" in html.lower()


def test_active_first_market_sections_and_sorts_exist() -> None:
    for html in _html_files():
        assert "buildDisplaySections" in html
        assert "active_asking" in html
        assert "sold_confirmed" in html
        assert "Recommended" in html
        assert "Price: Low to High" in html
        assert "Price: High to Low" in html
        assert "Active listings" in html
        assert "Market history" in html


def test_template_mirrors_stay_in_sync() -> None:
    assert INDEX_PATHS[0].read_text(encoding="utf-8") == INDEX_PATHS[1].read_text(encoding="utf-8")
    assert BETA_PATHS[0].read_text(encoding="utf-8") == BETA_PATHS[1].read_text(encoding="utf-8")


def test_active_first_freshness_prefers_last_seen_then_crawl_time() -> None:
    for html in _html_files():
        assert "parseTimestampScore(finalField(result, 'last_seen'))" in html
        assert "parseTimestampScore(finalField(result, 'crawl_time'))" in html
        assert "function getResultFirstSeenScore(result)" in html
        assert "parseTimestampScore(finalField(result, 'first_seen'))" in html
        assert "const raw = String(finalField(result, 'crawl_time') || finalField(result, 'first_seen') || '').trim();" not in html


def test_active_first_sorting_keeps_compatible_active_before_similar_or_excluded() -> None:
    for html in _html_files():
        assert "function getActiveCompatibilityTier(result, originalIndex)" in html
        assert "if(left.compatibilityTier !== right.compatibilityTier) return left.compatibilityTier - right.compatibilityTier;" in html
        assert "item.includes('accessory')" in html
        assert "item.includes('bundle')" in html
        assert "item.includes('wrong mount')" in html
        assert "item.includes('variant boundary')" in html


def test_active_and_history_sections_are_sorted_independently() -> None:
    for html in _html_files():
        assert "const active = [" in html
        assert "const history = [" in html
        assert "sortMarketBucket(buckets.active_asking, sortMode)" in html
        assert "sortMarketBucket(buckets.sold_confirmed, sortMode)" in html
        assert "renderResultSection('active', displaySections.active)" in html
        assert "renderArchiveSection(displaySections.history)" in html


def test_language_switch_preserves_results_without_research() -> None:
    for html in _html_files():
        body = _function_body(html, "setLocale")
        assert "render();" in body
        assert "window.scrollTo({ top: currentScrollY, behavior: 'auto' });" in body
        assert "runSearch(" not in body
        assert "fetch(" not in body


def test_sort_changes_are_client_side_only() -> None:
    for html in _html_files():
        build_params_body = _function_body(html, "buildParams")
        assert "params.set('sort'" not in build_params_body
        build_history_body = _function_body(html, "buildHistoryParamsFromState")
        assert "params.set('sort', next.sort);" in build_history_body
        assert "['category-filter','brand-filter','mount-filter','sold-filter','sort-select']" not in html
        assert "['category-filter','brand-filter','mount-filter','sold-filter'].forEach(id => {" in html
        assert "els['sort-select'].addEventListener('change', () => {" in html
        sort_body = _function_body(html, "bindEvents")
        assert "render();" in sort_body


def test_locale_strings_cover_active_first_surface() -> None:
    for html in _html_files():
        assert "현재 판매 중" in html
        assert "Market history" in html
        assert "추천순" in html
        assert "Newest" in html
        assert "낮은 가격순" in html
        assert "Price: High to Low" in html
        assert "판매 중" in html
        assert "판매 완료" in html
        assert "판매 종료" in html
        assert "과거 기록" in html
        assert "매물 보기" in html


def test_beta_uses_localized_view_listing_cta() -> None:
    for html in _html_files(BETA_PATHS):
        assert "ux('cta.view_listing', 'View listing')" in html


def test_beta_has_locale_translation_hooks_for_static_shell() -> None:
    for html in _html_files(BETA_PATHS):
        assert '[data-i18n]' in html
        assert "applyLocaleAttributes('data-i18n-placeholder', 'placeholder');" in html
        assert "applyLocaleAttributes('data-i18n-aria-label', 'aria-label');" in html
        assert 'data-i18n="workspace_sidebar.how_to_read.label"' in html
        assert 'data-i18n="filters.category.label"' in html
        assert 'data-i18n-placeholder="search.placeholder"' in html
        assert 'data-i18n-placeholder="search.sticky_placeholder"' in html


def test_beta_locale_dictionary_covers_shell_completion_keys() -> None:
    for html in _html_files(BETA_PATHS):
        for snippet in [
            "topbar: {",
            "hero: {",
            "search: {",
            "sidebar: {",
            "overview: {",
            "filters: {",
            "workspace_sidebar: {",
            "summary: {",
            "query_review: {",
            "state_card: {",
            "market_entry: {",
            "card: {",
            "warnings: {",
        ]:
            assert snippet in html
        assert "detected: { ko: '검색한 모델', en: 'Interpreted as'" in html
        assert "idle: { ko: '결과 더 보기', en: 'Load more'," in html
        assert "loading: { ko: '불러오는 중...', en: 'Loading…'," in html


def test_beta_locale_switch_keeps_sort_selection_intact() -> None:
    for html in _html_files(BETA_PATHS):
        body = _function_body(html, "setLocale")
        assert "sort-select" not in body
        assert "commitHistoryState(" not in body
        assert "render();" in body


def test_beta_empty_and_error_states_are_locale_driven() -> None:
    for html in _html_files(BETA_PATHS):
        assert "ux('state_card.error_title'" in html
        assert "ux('state_card.error_body'" in html
        assert "ux('state_card.empty_source_gap_title'" in html
        assert "ux('state_card.empty_broad_title'" in html
        assert "ux('state_card.empty_none_title'" in html
        assert "ux('refinement.title'" in html


def test_beta_card_labels_use_locale_keys_instead_of_raw_shell_copy() -> None:
    for html in _html_files(BETA_PATHS):
        body = _function_body(html, "renderCard")
        assert "ux('public_card.source', 'Seller / source')" in body
        assert "ux('public_card.location', 'Location')" in body
        assert "getObservedMeta(result)" in body
        assert "getPublicPriceBadge(result, priceRole, reason)" in body
        assert "ux('common.details_why', 'Why is this result shown?')" in body
        assert "detectedEntry" not in body
        assert "generationConfidence" not in body
        assert "renderDataPoint(" not in body
        assert "renderRoleRow(" not in body


def test_beta_public_card_hides_internal_diagnostic_fields() -> None:
    for html in _html_files(BETA_PATHS):
        body = _function_body(html, "renderCard")
        forbidden = [
            "Interpreted entry",
            "Search match",
            "Used for price",
            "Exclusion reason",
            "Generation confidence",
            "Price role",
            "Marker detected",
            "Projected reference",
        ]
        for text in forbidden:
            assert text not in body


def test_beta_public_surface_shows_dataset_update_line() -> None:
    for html in _html_files(BETA_PATHS):
        assert "function formatDatasetUpdateLine(meta)" in html
        assert "ux('summary.dataset_updated_prefix', 'Listing data updated')" in html


if __name__ == "__main__":
    test_index_calls_search_endpoint()
    test_public_routes_use_beta_shell_and_qa_uses_internal_shell()
    test_index_does_not_reimplement_legacy_search()
    test_required_ui_controls_exist()
    test_beta_files_include_locale_switcher()
    test_demo_queries_are_available()
    test_quality_summary_message_is_consumed_from_api()
    test_market_entry_policy_merges_top_level_runtime_overrides()
    test_exact_generation_headline_and_label_mappings_exist()
    test_active_first_market_sections_and_sorts_exist()
    test_template_mirrors_stay_in_sync()
    test_active_first_freshness_prefers_last_seen_then_crawl_time()
    test_active_first_sorting_keeps_compatible_active_before_similar_or_excluded()
    test_active_and_history_sections_are_sorted_independently()
    test_language_switch_preserves_results_without_research()
    test_sort_changes_are_client_side_only()
    test_locale_strings_cover_active_first_surface()
    test_beta_uses_localized_view_listing_cta()
    test_beta_has_locale_translation_hooks_for_static_shell()
    test_beta_locale_dictionary_covers_shell_completion_keys()
    test_beta_locale_switch_keeps_sort_selection_intact()
    test_beta_empty_and_error_states_are_locale_driven()
    test_beta_card_labels_use_locale_keys_instead_of_raw_shell_copy()
    test_beta_public_card_hides_internal_diagnostic_fields()
    test_beta_public_surface_shows_dataset_update_line()
    print("test_search_ui: ok")
