"""도착 총액 (판매가 + 배송비 + 관세·부가세) — 화면(beta.html computeLandedCost·landedTaxUsd)과 같은 계산을 서버에서.

원하는 매물 알림처럼 화면 밖에서 '세금까지 다 낸 총액'이 필요할 때 쓴다. 규칙은 data/config/landed_cost_rules.json,
환율은 data/fx_rates.json (1 USD = rates[통화]). 화면 계산과 같은지는 tests/test_landed_cost.py가 node로 화면 코드를 돌려 비교한다.
"""
from __future__ import annotations

import json
import math
import re
from functools import lru_cache
from pathlib import Path

ROOT = Path(__file__).resolve().parent
ROUND_STEP = {"KRW": 1000, "JPY": 100, "TWD": 10, "CNY": 10, "HKD": 10, "BRL": 10}


@lru_cache(maxsize=1)
def load_rules() -> dict:
    return json.loads((ROOT / "data/config/landed_cost_rules.json").read_text(encoding="utf-8"))


@lru_cache(maxsize=1)
def load_rates() -> dict:
    return json.loads((ROOT / "data/fx_rates.json").read_text(encoding="utf-8")).get("rates") or {}


def _rate(rates: dict, code) -> float | None:
    try:
        value = float(rates.get(str(code or "").upper()))
    except (TypeError, ValueError):
        return None
    return value if math.isfinite(value) and value > 0 else None


def convert(value, from_currency, to_currency, rates: dict) -> float | None:
    a, b = _rate(rates, from_currency), _rate(rates, to_currency)
    if value is None or not a or not b:
        return None
    return value / a * b


def round_estimate(value: float, currency: str) -> float:
    step = ROUND_STEP.get(currency, 1)
    # 화면의 Math.round와 같게 (0.5는 올림)
    return math.floor(value / step + 0.5) * step


def _num(value, default=0.0) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def source_rule(source: str, rules: dict) -> dict | None:
    sources = rules.get("sources") or {}
    source = str(source or "").strip()
    if source in sources:
        return sources[source]
    if re.search(r"ebay", source, re.I):
        return sources.get("eBay") or {"country": None, "ships_international": True}
    return None


def _region_of(code: str, rules: dict) -> str:
    for name, members in (rules.get("regions") or {}).items():
        if code in (members or []):
            return name
    return ""


def _pick(table, duty_key: str, category: str) -> float:
    table = table or {}
    if table.get(duty_key) is not None:
        return _num(table.get(duty_key))
    return _num(table.get(category))


def tax_usd(dest: str, dest_rule: dict, ctx: dict, rules: dict, rates: dict) -> tuple[float, list]:
    duty_key = "Body_digital" if ctx["category"] == "Body" and ctx["digital"] else ctx["category"]
    pick = lambda table: _pick(table, duty_key, ctx["category"])  # noqa: E731
    base = ctx["price_usd"] + ctx["shipping_usd"]
    flags: list = []
    tax = 0.0
    rule = dest_rule.get("rule")
    if rule == "kr":
        by_origin = dest_rule.get("exempt_usd_from_origin") or {}
        exempt = _num(by_origin.get(ctx["origin"]) if by_origin.get(ctx["origin"]) is not None else dest_rule.get("exempt_usd"))
        if ctx["price_usd"] > exempt:
            duty_rate = pick(dest_rule.get("duty"))
            fta = dest_rule.get("eu_fta")
            if fta and duty_rate > 0 and ctx["eu_origin"] and ctx["eu_seller"]:
                if ctx["price_usd"] <= _num(fta.get("proof_waiver_usd")):
                    duty_rate = 0
                    flags.append("kr_fta")
                else:
                    flags.append("kr_fta_over")
            duty = base * duty_rate
            tax = duty + (base + duty) * _num(dest_rule.get("vat"))
    elif rule == "jp":
        taxable = ctx["price_usd"] * _num(dest_rule.get("taxable_ratio"), 1) if dest_rule.get("taxable_ratio") else ctx["price_usd"]
        taxable_jpy = convert(taxable, "USD", "JPY", rates)
        if taxable_jpy is None or taxable_jpy > _num(dest_rule.get("exempt_taxable_jpy")):
            duty = taxable * pick(dest_rule.get("duty"))
            tax = duty + (taxable + duty) * _num(dest_rule.get("vat"))
    elif rule == "cn_postal":
        postal = ctx["price_usd"] * pick(dest_rule.get("postal_tax"))
        postal_cny = convert(postal, "USD", "CNY", rates)
        if postal_cny is None or postal_cny > _num(dest_rule.get("exempt_tax_cny")):
            tax = postal
        value_cny = convert(ctx["price_usd"], "USD", "CNY", rates)
        limit = dest_rule.get("single_parcel_limit_cny")
        if value_cny is not None and limit is not None and value_cny > _num(limit):
            flags.append("cn_parcel_limit")
    elif rule == "tw":
        base_twd = convert(base, "USD", "TWD", rates)
        if base_twd is None or base_twd > _num(dest_rule.get("exempt_twd")):
            duty = base * pick(dest_rule.get("duty"))
            tax = duty + (base + duty) * _num(dest_rule.get("vat"))
    elif rule == "us":
        tax = ctx["price_usd"] * (pick(dest_rule.get("duty")) + _num(dest_rule.get("additional_tariff"))) + _num(dest_rule.get("brokerage_usd"))
    elif rule == "gb":
        price_gbp = convert(ctx["price_usd"], "USD", "GBP", rates)
        duty = base * pick(dest_rule.get("duty")) if price_gbp is not None and price_gbp > _num(dest_rule.get("duty_exempt_gbp")) else 0
        tax = duty + (base + duty) * _num(dest_rule.get("vat")) + (convert(_num(dest_rule.get("handling_gbp")), "GBP", "USD", rates) or 0)
    elif rule == "eu":
        eu_rule = rules.get("eu_rule") or {}
        price_eur = convert(ctx["price_usd"], "USD", "EUR", rates)
        duty = base * pick(eu_rule.get("duty")) if price_eur is not None and price_eur > _num(eu_rule.get("duty_exempt_eur")) else 0
        tax = duty + (base + duty) * _num(dest_rule.get("vat")) + (convert(_num(eu_rule.get("handling_eur")), "EUR", "USD", rates) or 0)
    elif rule == "br":
        import_tax = base * _num(dest_rule.get("import_tax"))
        icms = _num(dest_rule.get("icms"))
        tax = import_tax + ((base + import_tax) / (1 - icms) * icms if icms < 1 else 0)
    return tax, flags


def landed_total(listing: dict, target: str, dest: str, rules: dict | None = None, rates: dict | None = None) -> dict | None:
    """listing: 색인의 final_output (source·currency·parsed_price_numeric·category·title_raw·country).
    → {'listed','currency','converted','total','shipping','taxes','international','store_only'} (target 통화), 계산 못 하면 None"""
    rules = rules if rules is not None else load_rules()
    rates = rates if rates is not None else load_rates()
    listed = listing.get("parsed_price_numeric")
    currency = str(listing.get("currency") or "").strip().upper()
    if listed is None or not _rate(rates, currency) or not _rate(rates, target):
        return None
    converted = convert(listed, currency, target, rates)
    out = {"listed": listed, "currency": currency, "converted": converted, "total": None}
    srule = source_rule(listing.get("source"), rules)
    origin = (srule or {}).get("country") or (str(listing.get("country") or "").upper() if re.fullmatch(r"[A-Za-z]{2}", str(listing.get("country") or "")) else "")
    dest_rule = (rules.get("destinations") or {}).get(dest)
    if not origin or not dest_rule:
        return out
    if srule and srule.get("online_purchase") is False:
        out["store_only"] = True
        return out
    category = listing.get("category") if listing.get("category") in ("Body", "Lens", "Accessory") else "Lens"
    title = str(listing.get("title_raw") or listing.get("title") or "")
    try:
        digital = bool(re.search(rules.get("digital_body_pattern") or "$^", title, re.I))
    except re.error:
        digital = False
    price_usd = convert(listed, currency, "USD", rates)
    eu = rules.get("eu_countries") or []
    same_market = origin == dest or (origin in eu and dest in eu)
    ship = rules.get("shipping_usd") or {}
    domestic = ship.get("domestic") or {}
    tax = 0.0
    if same_market:
        key = "EU" if origin in eu and origin != dest else origin
        table = domestic.get(key) or domestic.get("EU" if origin in eu else "default") or domestic.get("default") or {}
        shipping_usd = _num(table.get(category))
    else:
        same_region = _region_of(origin, rules) and _region_of(origin, rules) == _region_of(dest, rules)
        table = ship.get("region") if same_region else (ship.get("far_from_us") if origin == "US" else ship.get("far"))
        shipping_usd = _num((table or {}).get(category)) + price_usd * _num(ship.get("insurance_rate_international"))
        if srule and srule.get("ships_international") is False:
            fees = rules.get("forwarding_fee_usd") or {}
            origin_domestic = domestic.get(origin) or domestic.get("default") or {}
            fee = fees.get(origin) if fees.get(origin) is not None else fees.get("default", 0)
            shipping_usd += _num(origin_domestic.get(category)) + _num(fee)
        try:
            eu_origin = not re.search(rules.get("non_eu_made_pattern") or "$^", title, re.I)
        except re.error:
            eu_origin = False
        tax, _ = tax_usd(dest, dest_rule, {"price_usd": price_usd, "shipping_usd": shipping_usd, "category": category, "digital": digital,
                                           "origin": origin, "eu_origin": eu_origin, "eu_seller": origin in eu}, rules, rates)
    shipping = round_estimate(convert(shipping_usd, "USD", target, rates), target)
    taxes = round_estimate(convert(tax, "USD", target, rates), target)
    out.update({"shipping": shipping, "taxes": taxes, "total": round_estimate(converted + shipping + taxes, target),
                "international": not same_market})
    return out
