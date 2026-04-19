"""
query_parser.py
===============
Search interpretation layer draft.

This module parses user search text into structured search intent. It is
independent from classifier_v2.py:
  - classifier_v2 interprets listing data.
  - query_parser interprets user query text.

Do not move these aliases into classifier stages.
"""

from __future__ import annotations

from dataclasses import dataclass, field, asdict
import re
from typing import Any, Optional

from search_aliases import (
    DEFAULT_BRAND,
    GENERATION_ALIASES,
    MODEL_FAMILY_ALIASES,
    MODEL_SYSTEM_ALIASES,
    MOUNT_ALIASES,
    SYSTEM_ALIASES,
    VARIANT_ALIASES,
)


@dataclass
class QueryIntent:
    original_query: str
    normalized_query: str
    brand: Optional[str] = None
    model_family: Optional[str] = None
    focal_length: Optional[str] = None
    aperture: Optional[str] = None
    mount: Optional[str] = None
    system: Optional[str] = None
    variant: list[str] = field(default_factory=list)
    generation: Optional[str] = None
    filter_size: Optional[str] = None
    optical_formula: Optional[str] = None
    accessory_intent: Optional[str] = None
    accessory_code: Optional[str] = None
    confidence: float = 0.0
    tokens: list[dict[str, str]] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _normalize_query(query: str) -> str:
    q = (query or "").strip().lower()
    q = q.replace("㎜", "mm")
    q = q.replace("ｍｍ", "mm")
    q = re.sub(r"(?<=\d)\s*mm\b", "mm", q)
    q = re.sub(r"\s+", " ", q)
    return q


def _add_variant(intent: QueryIntent, value: str, source: str) -> None:
    if value not in intent.variant:
        intent.variant.append(value)
    intent.tokens.append({"type": "variant", "raw": source, "value": value})


def _set_accessory_intent(intent: QueryIntent, value: str, source: str) -> None:
    intent.accessory_intent = value
    if not any(token.get("type") == "accessory_intent" and token.get("value") == value for token in intent.tokens):
        intent.tokens.append({"type": "accessory_intent", "raw": source, "value": value})


def _set_accessory_code(intent: QueryIntent, value: str, source: str) -> None:
    intent.accessory_code = value.upper()
    intent.tokens.append({"type": "accessory_code", "raw": source, "value": intent.accessory_code})


def _set_filter_size(intent: QueryIntent, value: str, source: str) -> None:
    intent.filter_size = value.upper()
    if not any(token.get("type") == "filter_size" and token.get("raw") == source for token in intent.tokens):
        intent.tokens.append({"type": "filter_size", "raw": source, "value": intent.filter_size})


def _set_aperture(intent: QueryIntent, value: str, source: str, token_type: str = "aperture") -> None:
    intent.aperture = value
    intent.tokens.append({"type": token_type, "raw": source, "value": value})


def _aperture_value(raw_value: str) -> Optional[str]:
    try:
        numeric = float(raw_value)
    except ValueError:
        return None
    if 0.5 <= numeric <= 8.0:
        return raw_value
    return None


def _has_bare_aperture_context(normalized: str) -> bool:
    if re.search(r"\b\d{2,3}mm\b|\b\d{2,3}/\d", normalized):
        return True
    lens_family_aliases = [
        alias
        for alias, family in MODEL_FAMILY_ALIASES.items()
        if family not in {"MP3", "CM"}
    ]
    family_aliases = "|".join(re.escape(alias) for alias in sorted(lens_family_aliases, key=len, reverse=True))
    return bool(re.search(rf"\b(?:{family_aliases})\b", normalized))


def _parse_aperture_token(token: str, normalized: str) -> Optional[str]:
    prefixed = re.fullmatch(r"f/?(\d+(?:\.\d+)?)", token)
    if prefixed:
        return _aperture_value(prefixed.group(1))

    if re.fullmatch(r"\d+\.\d+", token) and _has_bare_aperture_context(normalized):
        return _aperture_value(token)

    return None


def _parse_compact_family_token(intent: QueryIntent, token: str) -> bool:
    match = re.fullmatch(r"(\d{2,3})([a-z][a-z-]+)", token)
    if not match:
        return False

    focal, alias = match.groups()
    family = MODEL_FAMILY_ALIASES.get(alias)
    if not family:
        return False

    intent.focal_length = focal
    intent.model_family = family
    intent.brand = intent.brand or DEFAULT_BRAND
    intent.tokens.append({"type": "focal_length", "raw": focal, "value": focal})
    intent.tokens.append({"type": "model_family", "raw": alias, "value": family})
    return True


def _parse_optical_formula(intent: QueryIntent, normalized: str) -> None:
    for groups, elements in re.findall(r"(\d+)\s*군\s*(\d+)\s*매", normalized):
        value = f"{groups} groups / {elements} elements"
        intent.optical_formula = value
        intent.tokens.append({"type": "optical_formula", "raw": f"{groups}군{elements}매", "value": value})
        if elements == "8":
            _add_variant(intent, "8-element", f"{groups}군{elements}매")


def _parse_accessory_intent(intent: QueryIntent, normalized: str) -> None:
    if re.search(r"\blens\s+hood\b", normalized):
        _set_accessory_intent(intent, "hood", "lens hood")
    elif re.search(r"\bhood\b", normalized) or "후드" in normalized:
        _set_accessory_intent(intent, "hood", "hood" if "hood" in normalized else "후드")

    if not intent.accessory_intent:
        filter_source: Optional[str] = None
        if "필터" in normalized:
            filter_source = "필터"
        elif re.search(r"\bb\+w\b.*\b(?:filter|fiter)\b", normalized):
            filter_source = "b+w filter"
        elif re.search(r"\be\d{2,3}\b.*\b(?:filter|fiter|uv|uva|uvir|nd|skylight)\b", normalized):
            filter_source = "filter_thread"
        elif re.search(r"\b(?:uv|uva|uvir|nd|skylight)\s+(?:filter|fiter)\b", normalized):
            filter_source = re.search(r"\b(?:uv|uva|uvir|nd|skylight)\s+(?:filter|fiter)\b", normalized).group(0)  # type: ignore[union-attr]
        elif re.search(r"\b(?:filter|fiter)\b", normalized):
            filter_source = "filter"
        elif re.search(r"\b(?:uva|uvir)\b", normalized):
            filter_source = re.search(r"\b(?:uva|uvir)\b", normalized).group(0)  # type: ignore[union-attr]

        a36_color = re.search(r"\ba36\s+(orange|yellow|green|red)\b", normalized)
        if a36_color:
            filter_source = a36_color.group(0)
            _set_filter_size(intent, "A36", "a36")
            intent.tokens.append({"type": "filter_color", "raw": a36_color.group(1), "value": a36_color.group(1)})

        if filter_source:
            _set_accessory_intent(intent, "filter", filter_source)
            kind = re.search(r"\b(uv|uva|uvir|nd|skylight)\b", filter_source)
            if kind:
                intent.tokens.append({"type": "filter_kind", "raw": kind.group(1), "value": kind.group(1).upper()})
            if "b+w" in filter_source:
                intent.tokens.append({"type": "filter_brand", "raw": "b+w", "value": "B+W"})

    # Leica accessory codes are intentionally parsed only inside an explicit
    # accessory-intent query. A standalone 5-digit number remains unparsed.
    if intent.accessory_intent:
        for code in re.findall(r"\b\d{5}[a-z]?\b", normalized):
            _set_accessory_code(intent, code, code)


def _filter_intent_token_consumed(intent: QueryIntent, token: str, normalized: str) -> bool:
    if intent.accessory_intent != "filter":
        return False
    if token in {"filter", "fiter", "필터", "uv", "uva", "uvir", "nd", "skylight"}:
        return True
    if token in {"b", "w"} and "b+w" in normalized:
        return True
    if token == "a36" and intent.filter_size == "A36":
        return True
    if token in {"orange", "yellow", "green", "red"} and re.search(rf"\ba36\s+{re.escape(token)}\b", normalized):
        return True
    return False


def _score_confidence(intent: QueryIntent) -> float:
    score = 0.20
    if intent.model_family:
        score += 0.25
    if intent.focal_length:
        score += 0.20
    if intent.aperture:
        score += 0.05
    if intent.variant:
        score += 0.12
    if intent.generation:
        score += 0.10
    if intent.filter_size:
        score += 0.08
    if intent.mount or intent.system:
        score += 0.08
    if intent.accessory_intent:
        score += 0.10
    if intent.accessory_code:
        score += 0.08
    if intent.brand:
        score += 0.05
    return min(round(score, 2), 0.95)


def parse_query(query: str, default_brand: Optional[str] = DEFAULT_BRAND) -> dict[str, Any]:
    """
    Parse a user query into structured search intent.

    The output is meant to match against classified listing fields later:
      - model_family -> model_raw/model_canonical family matching
      - focal_length -> classified focal_length
      - variant/generation/filter_size -> classified variant or derived specs
      - mount/system -> classified mount or future system field
    """
    normalized = _normalize_query(query)
    intent = QueryIntent(
        original_query=query,
        normalized_query=normalized,
        brand=default_brand,
    )

    _parse_optical_formula(intent, normalized)
    _parse_accessory_intent(intent, normalized)

    rough_tokens = re.findall(r"[a-z0-9가-힣./-]+", normalized)
    for token in rough_tokens:
        if _parse_compact_family_token(intent, token):
            continue

        if token in {"leica", "라이카"}:
            intent.brand = "Leica"
            intent.tokens.append({"type": "brand", "raw": token, "value": "Leica"})
            continue

        filter_match = re.fullmatch(r"e\s*([0-9]{2,3})|e([0-9]{2,3})", token)
        if filter_match:
            size = filter_match.group(1) or filter_match.group(2)
            _set_filter_size(intent, f"E{size}", token)
            continue

        focal_aperture_match = re.fullmatch(r"(\d{2,3})/(\d+(?:\.\d+)?)", token)
        if focal_aperture_match:
            focal, aperture = focal_aperture_match.groups()
            intent.focal_length = focal
            intent.tokens.append({"type": "focal_length", "raw": token, "value": focal})
            _set_aperture(intent, aperture, token, token_type="aperture_hint")
            continue

        aperture = _parse_aperture_token(token, normalized)
        if aperture:
            _set_aperture(intent, aperture, token)
            continue

        focal_match = re.fullmatch(r"(\d{2,3})(?:mm)?", token)
        if focal_match:
            intent.focal_length = focal_match.group(1)
            intent.tokens.append({"type": "focal_length", "raw": token, "value": intent.focal_length})
            continue

        family = MODEL_FAMILY_ALIASES.get(token)
        if family:
            intent.model_family = family
            intent.brand = intent.brand or DEFAULT_BRAND
            intent.tokens.append({"type": "model_family", "raw": token, "value": family})
            family_system = MODEL_SYSTEM_ALIASES.get(token)
            if family_system and not intent.system:
                intent.system = family_system
                intent.tokens.append({"type": "system", "raw": token, "value": family_system})
            continue

        variant = VARIANT_ALIASES.get(token)
        if variant:
            _add_variant(intent, variant, token)
            continue

        generation = GENERATION_ALIASES.get(token)
        if generation:
            intent.generation = generation
            intent.tokens.append({"type": "generation", "raw": token, "value": generation})
            continue

        mount = MOUNT_ALIASES.get(token)
        if mount:
            intent.mount = mount
            intent.tokens.append({"type": "mount", "raw": token, "value": mount})
            continue

        system = SYSTEM_ALIASES.get(token)
        if system:
            intent.system = system
            intent.tokens.append({"type": "system", "raw": token, "value": system})
            continue

        if re.fullmatch(r"\d+군\d+매", token):
            continue

        if intent.accessory_intent == "hood" and token in {"hood", "후드", "for", "용"}:
            continue

        if intent.accessory_intent == "hood" and token == "lens" and re.search(r"\blens\s+hood\b", normalized):
            continue

        if _filter_intent_token_consumed(intent, token, normalized):
            continue

        if intent.accessory_code and token.upper() == intent.accessory_code:
            continue

        if token not in {"매", "군"}:
            intent.tokens.append({"type": "unknown", "raw": token, "value": token})
            if re.fullmatch(r"f/?\d+(?:\.\d+)?|\d+\.\d+", token):
                intent.warnings.append(f"possible_unparsed_aperture:{token}")

    if not any([
        intent.model_family,
        intent.focal_length,
        intent.variant,
        intent.generation,
        intent.filter_size,
        intent.mount,
        intent.system,
        intent.optical_formula,
        intent.accessory_intent,
        intent.accessory_code,
    ]):
        intent.warnings.append("no_structured_search_intent")

    intent.confidence = _score_confidence(intent)
    return intent.to_dict()


if __name__ == "__main__":
    import json

    examples = [
        "35lux aa",
        "50cron 2nd",
        "nocti e60",
        "8매",
        "6군8매",
        "35 summicron 8매",
        "50 lux pre-asph e46",
        "m 35 cron",
        "ltm summaron 35",
        "q3 28",
    ]
    for example in examples:
        print(json.dumps(parse_query(example), ensure_ascii=False, indent=2))
