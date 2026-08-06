from __future__ import annotations

import datetime as dt
import json
import os
from pathlib import Path
import sys
from unittest.mock import patch

import requests

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from sources.ebay import clear_ebay_caches, get_application_token, search_active_listings


FIXTURE_PATH = Path(__file__).resolve().parent / "fixtures" / "ebay_browse_search_sample.json"


class _FakeResponse:
    def __init__(self, status_code: int, payload: dict | None = None) -> None:
        self.status_code = status_code
        self._payload = payload or {}

    def json(self) -> dict:
        return self._payload


def _fixture_payload() -> dict:
    return json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))


def _token_response() -> _FakeResponse:
    return _FakeResponse(
        200,
        {
            "access_token": "test-token",
            "expires_in": 7200,
            "token_type": "Application Access Token",
        },
    )


def test_ebay_disabled_by_default() -> None:
    clear_ebay_caches()
    with patch.dict(os.environ, {}, clear=True):
        response = search_active_listings("Leica M10", limit=5)

    assert response["status"] == "disabled"
    assert response["records"] == []
    assert response["diagnostics"]["enabled"] is False


def test_ebay_missing_credentials_is_fail_soft() -> None:
    clear_ebay_caches()
    with patch.dict(os.environ, {"EBAY_ACTIVE_LISTINGS_ENABLED": "true"}, clear=True):
        response = search_active_listings("Leica M10", limit=5)

    assert response["status"] == "missing_credentials"
    assert response["records"] == []
    assert response["diagnostics"]["request_success"] is False


def test_ebay_token_retrieval_is_cached() -> None:
    clear_ebay_caches()
    calls: list[str] = []

    def fake_post(*args, **kwargs):
        calls.append("post")
        return _token_response()

    with patch.dict(
        os.environ,
        {
            "EBAY_ACTIVE_LISTINGS_ENABLED": "true",
            "EBAY_CLIENT_ID": "client-id",
            "EBAY_CLIENT_SECRET": "client-secret",
        },
        clear=True,
    ):
        first = get_application_token(post=fake_post)
        second = get_application_token(post=fake_post)

    assert first["ok"] is True
    assert first["cache_hit"] is False
    assert second["ok"] is True
    assert second["cache_hit"] is True
    assert calls == ["post"]


def test_ebay_browse_normalization_preserves_fields_and_rejects_expired_duplicates() -> None:
    clear_ebay_caches()

    def fake_post(*args, **kwargs):
        return _token_response()

    def fake_get(*args, **kwargs):
        return _FakeResponse(200, _fixture_payload())

    with patch.dict(
        os.environ,
        {
            "EBAY_ACTIVE_LISTINGS_ENABLED": "true",
            "EBAY_CLIENT_ID": "client-id",
            "EBAY_CLIENT_SECRET": "client-secret",
            "EBAY_MARKETPLACE_ID": "EBAY_US",
        },
        clear=True,
    ):
        response = search_active_listings(
            "Leica M10",
            limit=10,
            now=dt.datetime(2026, 8, 5, 0, 0, tzinfo=dt.timezone.utc),
            post=fake_post,
            get=fake_get,
        )

    assert response["status"] == "ok"
    assert response["diagnostics"]["returned_count"] == 7
    assert response["diagnostics"]["accepted_count"] == 5
    assert response["diagnostics"]["duplicate_count"] == 1
    assert response["diagnostics"]["rejected_reasons"]["expired"] == 1

    first = response["records"][0]
    assert first["final_output"]["source"] == "eBay"
    assert first["final_output"]["source_marketplace"] == "EBAY_US"
    assert first["final_output"]["source_item_id"] == "v1|1001|0"
    assert first["final_output"]["legacy_item_id"] == "1001"
    assert first["final_output"]["buying_options"] == ["FIXED_PRICE"]
    assert first["final_output"]["seller"] == "rangefinder_store"
    assert first["final_output"]["country"] == "US"
    assert first["final_output"]["city"] == "Miami"
    assert first["final_output"]["affiliate_url"] == "https://www.ebay.com/itm/1001?mkcid=1"
    assert first["final_output"]["sold_quality"] == "asking"
    assert first["final_output"]["evidence_role"] == "asking"
    assert first["final_output"]["price_role"] == "asking_only"
    assert first["final_output"]["last_seen"] == "2026-08-05T00:00:00+00:00"
    assert first["final_output"]["parsed_price_numeric"] == 3499.0

    missing_seller = next(
        record for record in response["records"]
        if record["final_output"].get("source_item_id") == "v1|1005|0"
    )
    assert missing_seller["final_output"]["seller"] is None


def test_ebay_rate_limit_is_fail_soft() -> None:
    clear_ebay_caches()

    def fake_post(*args, **kwargs):
        return _token_response()

    def fake_get(*args, **kwargs):
        return _FakeResponse(429, {"errors": [{"message": "Too many requests"}]})

    with patch.dict(
        os.environ,
        {
            "EBAY_ACTIVE_LISTINGS_ENABLED": "true",
            "EBAY_CLIENT_ID": "client-id",
            "EBAY_CLIENT_SECRET": "client-secret",
        },
        clear=True,
    ):
        response = search_active_listings("Leica M10", limit=5, post=fake_post, get=fake_get)

    assert response["status"] == "rate_limited"
    assert response["records"] == []
    assert response["diagnostics"]["error_code"] == "browse_http_429"


def test_ebay_timeout_is_fail_soft() -> None:
    clear_ebay_caches()

    def fake_post(*args, **kwargs):
        return _token_response()

    def fake_get(*args, **kwargs):
        raise requests.Timeout("timeout")

    with patch.dict(
        os.environ,
        {
            "EBAY_ACTIVE_LISTINGS_ENABLED": "true",
            "EBAY_CLIENT_ID": "client-id",
            "EBAY_CLIENT_SECRET": "client-secret",
        },
        clear=True,
    ):
        response = search_active_listings("Leica M10", limit=5, post=fake_post, get=fake_get)

    assert response["status"] == "timeout"
    assert response["records"] == []
    assert response["diagnostics"]["error_code"] == "browse_timeout"


if __name__ == "__main__":
    test_ebay_disabled_by_default()
    test_ebay_missing_credentials_is_fail_soft()
    test_ebay_token_retrieval_is_cached()
    test_ebay_browse_normalization_preserves_fields_and_rejects_expired_duplicates()
    test_ebay_rate_limit_is_fail_soft()
    test_ebay_timeout_is_fail_soft()
    print("test_ebay_source: ok")
