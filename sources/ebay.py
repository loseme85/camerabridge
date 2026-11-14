from __future__ import annotations

from copy import deepcopy
import datetime as dt
import json
import os
from pathlib import Path
import time
from typing import Any

import requests

from classifier_v2 import classify_listing_v2
from search_index import build_search_fields, normalize_title, parse_price_numeric
from trusted_metadata import (
    CuratedReferenceEntry,
    TrustedMetadataEntry,
    load_curated_reference,
    load_trusted_metadata,
    resolve_listing,
)


PROJECT_ROOT = Path(__file__).resolve().parents[1]
EBAY_TOKEN_URL = "https://api.ebay.com/identity/v1/oauth2/token"
EBAY_BROWSE_SEARCH_URL = "https://api.ebay.com/buy/browse/v1/item_summary/search"
DEFAULT_MARKETPLACE_ID = "EBAY_US"
DEFAULT_TIMEOUT_SECONDS = 4.5
TOKEN_EXPIRY_SKEW_SECONDS = 90
SEARCH_CACHE_TTL_SECONDS = 3600  # 2026-11-14: 같은 검색어는 1시간 — eBay 하루 호출 한도(5,000)·Vercel CPU 아끼기 (EBAY_CACHE_SECONDS로 바꿈)
# 우량 판매자만 (2026-11-14 사장님: eBay는 개인 판매도 섞여 있어 피드백 99% 이상·점수 500 이상 판매자만)
DEFAULT_MIN_FEEDBACK_PERCENT = 99.0
DEFAULT_MIN_FEEDBACK_SCORE = 500
# 카메라·사진(625) 안에서, 경매 빼고(즉시 구매가만), 부품용(7000) 뺀 상태만
DEFAULT_CATEGORY_IDS = "625"
USED_CONDITION_FILTER = "conditionIds:{1000|1500|2000|2010|2020|2030|2500|2750|3000|4000|5000|6000}"
TOKEN_SCOPE = "https://api.ebay.com/oauth/api_scope"
ENABLED_VALUES = {"1", "true", "yes", "on"}

_TOKEN_CACHE: dict[str, Any] = {}
_SEARCH_CACHE: dict[tuple[str, str, int], dict[str, Any]] = {}
_RESOLUTION_CACHE: dict[str, Any] = {}


def ebay_active_listings_enabled() -> bool:
    return str(os.getenv("EBAY_ACTIVE_LISTINGS_ENABLED") or "").strip().lower() in ENABLED_VALUES


def clear_ebay_caches() -> None:
    _TOKEN_CACHE.clear()
    _SEARCH_CACHE.clear()
    _RESOLUTION_CACHE.clear()


def _now_utc(now: dt.datetime | None = None) -> dt.datetime:
    reference = now or dt.datetime.now(dt.timezone.utc)
    if reference.tzinfo is None:
        return reference.replace(tzinfo=dt.timezone.utc)
    return reference.astimezone(dt.timezone.utc)


def _normalize_query(value: Any) -> str:
    return " ".join(str(value or "").strip().lower().split())


def _bool_env(key: str) -> bool:
    return str(os.getenv(key) or "").strip().lower() in ENABLED_VALUES


def _marketplace_id(value: str | None = None) -> str:
    return str(value or os.getenv("EBAY_MARKETPLACE_ID") or DEFAULT_MARKETPLACE_ID).strip() or DEFAULT_MARKETPLACE_ID


def _float_env(key: str, default: float) -> float:
    try:
        return float(str(os.getenv(key) or "").strip() or default)
    except ValueError:
        return default


def _trusted_sellers_only() -> bool:
    return str(os.getenv("EBAY_TRUSTED_SELLERS_ONLY") or "true").strip().lower() in ENABLED_VALUES


def _cache_seconds() -> int:
    return int(_float_env("EBAY_CACHE_SECONDS", SEARCH_CACHE_TTL_SECONDS))


def _trust_rejection(seller: Any, buying_options: list[str], condition_id: str) -> str | None:
    """우량 판매자·즉시 구매·부품용 아님. 통과하면 None."""
    if not _trusted_sellers_only():
        return None
    if buying_options and "FIXED_PRICE" not in buying_options:
        return "auction_only"
    if condition_id == "7000":
        return "for_parts"
    info = seller if isinstance(seller, dict) else {}
    try:
        percent = float(str(info.get("feedbackPercentage")))
        score = int(float(str(info.get("feedbackScore"))))
    except (TypeError, ValueError):
        return "seller_unknown"
    if percent < _float_env("EBAY_MIN_FEEDBACK_PERCENT", DEFAULT_MIN_FEEDBACK_PERCENT):
        return "seller_feedback_percent"
    if score < _float_env("EBAY_MIN_FEEDBACK_SCORE", DEFAULT_MIN_FEEDBACK_SCORE):
        return "seller_feedback_score"
    return None


SELLER_SHOPS_PATH = PROJECT_ROOT / "data" / "config" / "ebay_seller_shops.json"


def _crawled_shop_sellers() -> dict[str, str]:
    """이미 크롤하는 매장의 eBay 판매자 이름 (소문자) → 매장 이름."""
    cached = _RESOLUTION_CACHE.get("seller_shops")
    if cached is None:
        try:
            raw = json.loads(SELLER_SHOPS_PATH.read_text(encoding="utf-8")).get("sellers") or {}
        except (OSError, ValueError):
            raw = {}
        cached = {str(k).strip().lower(): str(v) for k, v in raw.items()}
        _RESOLUTION_CACHE["seller_shops"] = cached
    return cached


def _credentials() -> tuple[str, str]:
    return (
        str(os.getenv("EBAY_CLIENT_ID") or "").strip(),
        str(os.getenv("EBAY_CLIENT_SECRET") or "").strip(),
    )


def _format_price_value(value: Any, currency: str) -> str:
    try:
        numeric = float(str(value))
    except (TypeError, ValueError):
        return ""
    if numeric.is_integer():
        amount = f"{int(numeric):,}"
    else:
        amount = f"{numeric:,.2f}".rstrip("0").rstrip(".")
    return f"{currency} {amount}".strip()


def _parse_timestamp(value: Any) -> dt.datetime | None:
    raw = str(value or "").strip()
    if not raw:
        return None
    if raw.endswith("Z"):
        raw = raw[:-1] + "+00:00"
    try:
        parsed = dt.datetime.fromisoformat(raw)
    except ValueError:
        return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=dt.timezone.utc)
    return parsed.astimezone(dt.timezone.utc)


def _load_resolution_resources() -> tuple[list[TrustedMetadataEntry], list[CuratedReferenceEntry]]:
    trusted_entries = _RESOLUTION_CACHE.get("trusted_entries")
    curated_entries = _RESOLUTION_CACHE.get("curated_entries")
    if trusted_entries is None:
        trusted_entries = load_trusted_metadata()
        _RESOLUTION_CACHE["trusted_entries"] = trusted_entries
    if curated_entries is None:
        curated_entries = load_curated_reference()
        _RESOLUTION_CACHE["curated_entries"] = curated_entries
    return trusted_entries, curated_entries


def _response_json(response: requests.Response) -> dict[str, Any]:
    try:
        payload = response.json()
    except ValueError:
        return {}
    return payload if isinstance(payload, dict) else {}


def _token_is_cached(now: dt.datetime) -> bool:
    expires_at = _TOKEN_CACHE.get("expires_at")
    return bool(_TOKEN_CACHE.get("access_token") and isinstance(expires_at, dt.datetime) and now < expires_at)


def _cache_token(payload: dict[str, Any], now: dt.datetime) -> str:
    token = str(payload.get("access_token") or "").strip()
    expires_in = int(payload.get("expires_in") or 0)
    if not token or expires_in <= 0:
        raise ValueError("eBay token response did not include access_token/expires_in")
    safe_window = max(expires_in - TOKEN_EXPIRY_SKEW_SECONDS, 30)
    _TOKEN_CACHE["access_token"] = token
    _TOKEN_CACHE["expires_at"] = now + dt.timedelta(seconds=safe_window)
    return token


def get_application_token(
    *,
    now: dt.datetime | None = None,
    timeout: float = DEFAULT_TIMEOUT_SECONDS,
    post: Any = None,
) -> dict[str, Any]:
    reference_now = _now_utc(now)
    if _token_is_cached(reference_now):
        return {
            "ok": True,
            "access_token": _TOKEN_CACHE["access_token"],
            "cache_hit": True,
            "status": "cached",
        }

    client_id, client_secret = _credentials()
    if not client_id or not client_secret:
        return {
            "ok": False,
            "status": "missing_credentials",
            "cache_hit": False,
            "error_code": "missing_credentials",
        }

    http_post = post or requests.post
    try:
        response = http_post(
            EBAY_TOKEN_URL,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            data={"grant_type": "client_credentials", "scope": TOKEN_SCOPE},
            auth=(client_id, client_secret),
            timeout=timeout,
        )
    except requests.Timeout:
        return {"ok": False, "status": "timeout", "cache_hit": False, "error_code": "token_timeout"}
    except requests.RequestException as exc:
        return {
            "ok": False,
            "status": "request_error",
            "cache_hit": False,
            "error_code": "token_request_error",
            "message": str(exc),
        }

    payload = _response_json(response)
    if response.status_code != 200:
        return {
            "ok": False,
            "status": "http_error",
            "cache_hit": False,
            "error_code": f"token_http_{response.status_code}",
            "http_status": response.status_code,
            "payload": payload,
        }

    try:
        token = _cache_token(payload, reference_now)
    except (TypeError, ValueError) as exc:
        return {
            "ok": False,
            "status": "invalid_payload",
            "cache_hit": False,
            "error_code": "token_invalid_payload",
            "message": str(exc),
        }

    return {
        "ok": True,
        "access_token": token,
        "cache_hit": False,
        "status": "fetched",
    }


def _seller_display_name(seller: Any) -> str | None:
    if isinstance(seller, str):
        return seller.strip() or None
    if not isinstance(seller, dict):
        return None
    for key in ["username", "userId", "sellerId", "sellerUserName"]:
        value = str(seller.get(key) or "").strip()
        if value:
            return value
    return None


def _normalize_browse_item(
    item: dict[str, Any],
    *,
    fetch_time: dt.datetime,
    marketplace_id: str,
    record_index: int,
) -> tuple[dict[str, Any] | None, str | None]:
    item_id = str(item.get("itemId") or "").strip()
    source_url = str(item.get("itemWebUrl") or "").strip()
    title = str(item.get("title") or "").strip()
    dedupe_key = item_id or source_url
    if not dedupe_key:
        return None, "missing_identity"
    if not title:
        return None, "missing_title"

    end_at = _parse_timestamp(item.get("itemEndDate"))
    if end_at and end_at < fetch_time:
        return None, "expired"

    image = item.get("image") if isinstance(item.get("image"), dict) else {}
    price = item.get("price") if isinstance(item.get("price"), dict) else {}
    item_location = item.get("itemLocation") if isinstance(item.get("itemLocation"), dict) else {}
    seller = item.get("seller") if isinstance(item.get("seller"), dict) else item.get("seller")
    buying_options = item.get("buyingOptions")
    buying_options_list = buying_options if isinstance(buying_options, list) else ([buying_options] if buying_options else [])
    buying_options_list = [str(option).strip().upper() for option in buying_options_list if str(option or "").strip()]

    currency = str(price.get("currency") or "").strip()
    raw_price_value = price.get("value")
    price_raw = _format_price_value(raw_price_value, currency)
    condition_label = str(item.get("condition") or "").strip()
    condition_id = str(item.get("conditionId") or "").strip()
    condition_raw = condition_label or condition_id
    trust_reason = _trust_rejection(seller, buying_options_list, condition_id)
    if trust_reason:
        return None, trust_reason
    seller_name = _seller_display_name(seller)
    # 우리가 이미 크롤하는 매장이 eBay에도 올린 물건 → 매장 직접 매물만 보여 줌 (중복 방지)
    if seller_name and seller_name.strip().lower() in _crawled_shop_sellers():
        return None, "seller_is_crawled_shop"
    created_at = _parse_timestamp(item.get("itemCreationDate") or item.get("itemOriginDate"))
    created_iso = created_at.isoformat() if created_at else ""
    end_iso = end_at.isoformat() if end_at else ""
    fetch_iso = fetch_time.isoformat()

    raw_item = {
        "상품명": title,
        "가격": price_raw,
        "통화": currency,
        "이미지": str(image.get("imageUrl") or "").strip(),
        "링크": source_url,
        "site": "eBay",
        "컨디션": condition_raw,
        "품절": False,
        "description": "",
        "crawl_time": fetch_iso,
        "first_seen": created_iso or fetch_iso,
    }

    trusted_entries, curated_entries = _load_resolution_resources()
    classified = classify_listing_v2(raw_item)
    resolved = resolve_listing(
        raw_item=raw_item,
        classifier_output=classified,
        trusted_entries=trusted_entries,
        curated_entries=curated_entries,
    )

    final_output = deepcopy(resolved["final_output"])
    final_output.update(
        {
            "source": "eBay",
            "source_url": source_url,
            "affiliate_url": str(item.get("itemAffiliateWebUrl") or "").strip() or None,
            "title_raw": title,
            "price_raw": price_raw,
            "currency": currency,
            "image_url": str(image.get("imageUrl") or "").strip(),
            "condition_raw": condition_raw,
            "source_marketplace": str(item.get("listingMarketplaceId") or marketplace_id or "").strip() or DEFAULT_MARKETPLACE_ID,
            "source_item_id": item_id or None,
            "legacy_item_id": str(item.get("legacyItemId") or "").strip() or None,
            "buying_options": buying_options_list,
            "condition_id": condition_id or None,
            "seller": seller_name,
            "seller_feedback_score": seller.get("feedbackScore") if isinstance(seller, dict) else None,
            "seller_feedback_percentage": seller.get("feedbackPercentage") if isinstance(seller, dict) else None,
            "country": str(item_location.get("country") or "").strip() or None,
            "city": str(item_location.get("city") or "").strip() or None,
            "item_created_at": created_iso or None,
            "item_end_at": end_iso or None,
            "crawl_time": fetch_iso,
            "first_seen": created_iso or fetch_iso,
            "last_seen": fetch_iso,
            "sold_quality": "asking",
            "evidence_role": "asking",
            "price_role": "asking_only",
        }
    )
    final_output["normalized_title"] = normalize_title(title)
    final_output["parsed_price_numeric"] = parse_price_numeric(price_raw)
    search_fields = build_search_fields(final_output, raw_item)

    return {
        "search_id": f"ebay:{dedupe_key}",
        "record_index": record_index,
        "raw_item": raw_item,
        "classifier_output": resolved["classifier_output"],
        "final_output": final_output,
        "search_fields": search_fields,
        "override_applied": bool(resolved.get("override_applied")),
        "override_source": resolved.get("override_source"),
        "override_source_id": resolved.get("override_source_id"),
        "override_reason": resolved.get("override_reason"),
        "audit_trail": list(resolved.get("audit_trail") or []),
    }, None


def search_active_listings(
    query: str,
    limit: int,
    marketplace_id: str | None = None,
    *,
    now: dt.datetime | None = None,
    timeout: float = DEFAULT_TIMEOUT_SECONDS,
    get: Any = None,
    post: Any = None,
) -> dict[str, Any]:
    requested_at = _now_utc(now)
    started = time.perf_counter()
    normalized_query = _normalize_query(query)
    effective_limit = max(1, min(int(limit or 1), 100))
    marketplace = _marketplace_id(marketplace_id)
    diagnostics: dict[str, Any] = {
        "source": "eBay",
        "enabled": ebay_active_listings_enabled(),
        "marketplace": marketplace,
        "query": query,
        "normalized_query": normalized_query,
        "requested_limit": effective_limit,
        "request_success": False,
        "cache": "none",
        "returned_count": 0,
        "accepted_count": 0,
        "rejected_count": 0,
        "duplicate_count": 0,
        "rejected_reasons": {},
        "latency_ms": 0,
        "status": "disabled",
    }

    if not diagnostics["enabled"]:
        diagnostics["status"] = "disabled"
        return {"enabled": False, "status": "disabled", "records": [], "diagnostics": diagnostics}

    client_id, client_secret = _credentials()
    if not client_id or not client_secret:
        diagnostics["status"] = "missing_credentials"
        return {"enabled": True, "status": "missing_credentials", "records": [], "diagnostics": diagnostics}

    cache_key = (marketplace, normalized_query, effective_limit)
    cached_entry = _SEARCH_CACHE.get(cache_key)
    if cached_entry and requested_at < cached_entry["expires_at"]:
        diagnostics.update(deepcopy(cached_entry["diagnostics"]))
        diagnostics["cache"] = "hit"
        diagnostics["status"] = "ok"
        return {
            "enabled": True,
            "status": "ok",
            "records": deepcopy(cached_entry["records"]),
            "diagnostics": diagnostics,
        }

    token_result = get_application_token(now=requested_at, timeout=timeout, post=post)
    diagnostics["token_cache"] = token_result.get("cache_hit", False)
    if not token_result.get("ok"):
        diagnostics["status"] = str(token_result.get("status") or "token_error")
        diagnostics["error_code"] = token_result.get("error_code")
        diagnostics["latency_ms"] = int((time.perf_counter() - started) * 1000)
        return {
            "enabled": True,
            "status": diagnostics["status"],
            "records": [],
            "diagnostics": diagnostics,
        }

    headers = {
        "Authorization": f"Bearer {token_result['access_token']}",
        "Accept": "application/json",
        "X-EBAY-C-MARKETPLACE-ID": marketplace,
    }
    params = {"q": query, "limit": effective_limit}
    if _trusted_sellers_only():
        params["filter"] = f"buyingOptions:{{FIXED_PRICE}},{USED_CONDITION_FILTER}"
        params["category_ids"] = str(os.getenv("EBAY_CATEGORY_IDS") or DEFAULT_CATEGORY_IDS).strip()
    # eBay Partner Network: 캠페인 ID가 있으면 결과에 제휴 링크(itemAffiliateWebUrl)가 오고 화면은 그 링크로 보냄
    campaign_id = str(os.getenv("EBAY_EPN_CAMPAIGN_ID") or "").strip()
    if campaign_id:
        headers["X-EBAY-C-ENDUSERCTX"] = f"affiliateCampaignId={campaign_id},affiliateReferenceId=camerabridge"
    http_get = get or requests.get

    def _run_search_request(headers_override: dict[str, str]) -> requests.Response:
        return http_get(
            EBAY_BROWSE_SEARCH_URL,
            headers=headers_override,
            params=params,
            timeout=timeout,
        )

    try:
        response = _run_search_request(headers)
        if response.status_code == 401:
            _TOKEN_CACHE.clear()
            retry_token = get_application_token(now=requested_at, timeout=timeout, post=post)
            diagnostics["token_cache_retry"] = retry_token.get("cache_hit", False)
            if not retry_token.get("ok"):
                diagnostics["status"] = str(retry_token.get("status") or "token_error")
                diagnostics["error_code"] = retry_token.get("error_code")
                diagnostics["latency_ms"] = int((time.perf_counter() - started) * 1000)
                return {
                    "enabled": True,
                    "status": diagnostics["status"],
                    "records": [],
                    "diagnostics": diagnostics,
                }
            headers["Authorization"] = f"Bearer {retry_token['access_token']}"
            response = _run_search_request(headers)
    except requests.Timeout:
        diagnostics["status"] = "timeout"
        diagnostics["error_code"] = "browse_timeout"
        diagnostics["latency_ms"] = int((time.perf_counter() - started) * 1000)
        return {"enabled": True, "status": "timeout", "records": [], "diagnostics": diagnostics}
    except requests.RequestException as exc:
        diagnostics["status"] = "request_error"
        diagnostics["error_code"] = "browse_request_error"
        diagnostics["message"] = str(exc)
        diagnostics["latency_ms"] = int((time.perf_counter() - started) * 1000)
        return {"enabled": True, "status": "request_error", "records": [], "diagnostics": diagnostics}

    payload = _response_json(response)
    diagnostics["http_status"] = response.status_code
    diagnostics["request_success"] = response.status_code == 200
    if response.status_code != 200:
        diagnostics["status"] = {
            401: "unauthorized",
            403: "forbidden",
            429: "rate_limited",
        }.get(response.status_code, "http_error" if response.status_code < 500 else "upstream_error")
        diagnostics["error_code"] = f"browse_http_{response.status_code}"
        diagnostics["latency_ms"] = int((time.perf_counter() - started) * 1000)
        return {
            "enabled": True,
            "status": diagnostics["status"],
            "records": [],
            "diagnostics": diagnostics,
        }

    item_summaries = payload.get("itemSummaries")
    items = item_summaries if isinstance(item_summaries, list) else []
    diagnostics["returned_count"] = len(items)
    seen_keys: set[str] = set()
    records: list[dict[str, Any]] = []
    rejected_reasons: dict[str, int] = {}
    duplicate_count = 0

    for index, item in enumerate(items, start=1):
        if not isinstance(item, dict):
            rejected_reasons["invalid_item"] = rejected_reasons.get("invalid_item", 0) + 1
            continue
        item_id = str(item.get("itemId") or "").strip()
        fallback_url = str(item.get("itemWebUrl") or "").strip()
        unique_key = f"ebay:{item_id}" if item_id else f"url:{fallback_url}"
        if unique_key in seen_keys:
            duplicate_count += 1
            rejected_reasons["duplicate_item_id"] = rejected_reasons.get("duplicate_item_id", 0) + 1
            continue
        normalized_record, rejected_reason = _normalize_browse_item(
            item,
            fetch_time=requested_at,
            marketplace_id=marketplace,
            record_index=-index,
        )
        if rejected_reason:
            rejected_reasons[rejected_reason] = rejected_reasons.get(rejected_reason, 0) + 1
            continue
        seen_keys.add(unique_key)
        records.append(normalized_record)

    diagnostics["accepted_count"] = len(records)
    diagnostics["duplicate_count"] = duplicate_count
    diagnostics["rejected_reasons"] = rejected_reasons
    diagnostics["rejected_count"] = sum(rejected_reasons.values())
    diagnostics["cache"] = "miss"
    diagnostics["status"] = "ok"
    diagnostics["latency_ms"] = int((time.perf_counter() - started) * 1000)

    _SEARCH_CACHE[cache_key] = {
        "records": deepcopy(records),
        "diagnostics": deepcopy(diagnostics),
        "expires_at": requested_at + dt.timedelta(seconds=_cache_seconds()),
    }

    return {
        "enabled": True,
        "status": "ok",
        "records": records,
        "diagnostics": diagnostics,
    }


if __name__ == "__main__":
    output = search_active_listings("Leica M10", limit=5)
    print(json.dumps(output["diagnostics"], ensure_ascii=False, indent=2))
