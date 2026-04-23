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
    body_intent: Optional[str] = None
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


_BODY_INTENT_ALIASES = {
    "m2": ("M2", "M", None),
    "m3": ("M3", "M", None),
    "m4": ("M4", "M", None),
    "m5": ("M5", "M", None),
    "m6": ("M6", "M", None),
    "mp": ("MP", "M", None),
    "q2": ("Q2", None, "Q"),
    "q3": ("Q3", None, "Q"),
    "r6": ("R6", "R", None),
    "r7": ("R7", "R", None),
    "r8": ("R8", "R", None),
    "barnack": ("Barnack", "L", None),
    "iiic": ("IIIc", "L", None),
    "iiif": ("IIIf", "L", None),
    "iiig": ("IIIg", "L", None),
}


_COMPACT_BODY_PATTERNS: tuple[tuple[str, str], ...] = (
    (r"\bd\s*-\s*lux\s*([0-9]{1,3})?\b|\bd\s+lux\s*([0-9]{1,3})?\b|\bdlux\s*([0-9]{1,3})?\b", "D-LUX"),
    (r"\bv\s*-\s*lux\s*([0-9]{1,3})?\b|\bv\s+lux\s*([0-9]{1,3})?\b|\bvlux\s*([0-9]{1,3})?\b", "V-LUX"),
    (r"\bc\s*-\s*lux\s*([0-9]{1,3})?\b|\bc\s+lux\s*([0-9]{1,3})?\b|\bclux\s*([0-9]{1,3})?\b", "C-LUX"),
    (r"\bsofort\s*([0-9]{1,2})?\b", "Sofort"),
)


def _set_body_intent(
    intent: QueryIntent,
    value: str,
    source: str,
    mount: Optional[str] = None,
    system: Optional[str] = None,
) -> None:
    intent.body_intent = value
    intent.tokens.append({"type": "body_intent", "raw": source, "value": value})
    if mount and not intent.mount:
        intent.mount = mount
        intent.tokens.append({"type": "mount", "raw": source, "value": mount})
    if system and not intent.system:
        intent.system = system
        intent.tokens.append({"type": "system", "raw": source, "value": system})


def _parse_compact_body_intent(intent: QueryIntent, normalized: str) -> None:
    for pattern, family in _COMPACT_BODY_PATTERNS:
        match = re.search(pattern, normalized)
        if not match:
            continue
        suffix = next((group for group in match.groups() if group), None)
        value = f"{family} {suffix}" if suffix else family
        _set_body_intent(intent, value, match.group(0), system="Compact")
        break


def _body_intent_token_allowed(token: str, rough_tokens: list[str]) -> bool:
    try:
        index = rough_tokens.index(token)
    except ValueError:
        return True
    previous = rough_tokens[index - 1] if index > 0 else ""
    if previous in {"for", "용", "호환", "compatible"}:
        return False
    return True


def _set_filter_size(intent: QueryIntent, value: str, source: str) -> None:
    intent.filter_size = value.upper()
    if not any(token.get("type") == "filter_size" and token.get("raw") == source for token in intent.tokens):
        intent.tokens.append({"type": "filter_size", "raw": source, "value": intent.filter_size})


def _add_adapter_detail(intent: QueryIntent, value: str, source: str) -> None:
    if not any(token.get("type") == "adapter_detail" and token.get("value") == value for token in intent.tokens):
        intent.tokens.append({"type": "adapter_detail", "raw": source, "value": value})


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
        finder_source: Optional[str] = None
        if re.search(r"\bbrightline\s+(?:view)?finder\b", normalized):
            finder_source = "brightline finder"
        elif re.search(r"\bexternal\s+(?:view)?finder\b", normalized):
            finder_source = "external finder"
        elif re.search(r"\bviewfinder\b", normalized):
            finder_source = "viewfinder"
        elif re.search(r"\bvisoflex\b", normalized):
            finder_source = "visoflex"
        elif re.search(r"\bfinder\b", normalized) or "파인더" in normalized:
            finder_source = "finder" if re.search(r"\bfinder\b", normalized) else "파인더"

        if finder_source:
            _set_accessory_intent(intent, "finder", finder_source)

    if not intent.accessory_intent:
        adapter_source: Optional[str] = None
        if re.search(r"\bm\s*-\s*l\s+(?:adapter|adaptor)\b", normalized):
            adapter_source = "m-l adapter"
            _add_adapter_detail(intent, "m-l", adapter_source)
        elif re.search(r"\bm\s+to\s+l\s+(?:adapter|adaptor)\b", normalized):
            adapter_source = "m to l adapter"
            _add_adapter_detail(intent, "m-l", adapter_source)
        elif re.search(r"\bmacro\s+(?:adapter|adaptor)\s+m\b", normalized):
            adapter_source = "macro adapter m"
            _add_adapter_detail(intent, "macro", adapter_source)
        elif re.search(r"\bmount\s+(?:adapter|adaptor)\b", normalized):
            adapter_source = "mount adapter"
        elif re.search(r"\b(?:adapter|adaptor)\s+ring\b", normalized):
            adapter_source = "adapter ring"
        elif re.search(r"\bleica\s+m\s+(?:adapter|adaptor)\b", normalized):
            adapter_source = "leica m adapter"
            _add_adapter_detail(intent, "m", adapter_source)
        elif re.search(r"\b(?:adapter|adaptor)\b", normalized) or "어댑터" in normalized:
            adapter_source = "adaptor" if re.search(r"\badaptor\b", normalized) else ("어댑터" if "어댑터" in normalized else "adapter")

        if adapter_source:
            _set_accessory_intent(intent, "adapter", adapter_source)

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


def _adapter_intent_token_consumed(intent: QueryIntent, token: str, normalized: str) -> bool:
    if intent.accessory_intent != "adapter":
        return False
    if token in {"adapter", "adaptor", "어댑터", "mount", "ring", "to", "macro"}:
        return True
    if token in {"m", "l"} and re.search(r"\b(?:m\s*-\s*l|m\s+to\s+l|leica\s+m|macro\s+(?:adapter|adaptor)\s+m)\b", normalized):
        return True
    if token == "m-l" and re.search(r"\bm\s*-\s*l\s+(?:adapter|adaptor)\b", normalized):
        return True
    return False


def _finder_intent_token_consumed(intent: QueryIntent, token: str, normalized: str) -> bool:
    if intent.accessory_intent != "finder":
        return False
    if token in {"finder", "viewfinder", "brightline", "external", "visoflex", "파인더"}:
        return True
    return False


def _compact_body_intent_token_consumed(intent: QueryIntent, token: str, normalized: str) -> bool:
    body_intent = intent.body_intent or ""
    body_norm = body_intent.lower()
    if not body_norm.startswith(("d-lux", "v-lux", "c-lux", "sofort")):
        return False

    if token in {"d", "v", "c", "lux", "d-lux", "v-lux", "c-lux", "dlux", "vlux", "clux", "sofort"}:
        return True

    compacted = re.sub(r"[^a-z0-9]+", "", token)
    if compacted in {"dlux", "vlux", "clux"}:
        return True

    suffix_match = re.search(r"\b(?:d|v|c)-?lux\s*([0-9]{1,3})\b|\b(?:d|v|c)\s+lux\s*([0-9]{1,3})\b|\b(?:d|v|c)lux\s*([0-9]{1,3})\b|\bsofort\s*([0-9]{1,2})\b", normalized)
    suffix = next((group for group in suffix_match.groups() if group), None) if suffix_match else None
    if suffix and token == suffix:
        return True
    if suffix and compacted in {f"dlux{suffix}", f"vlux{suffix}", f"clux{suffix}", f"sofort{suffix}"}:
        return True

    return False


def _score_confidence(intent: QueryIntent) -> float:
    score = 0.20
    if intent.model_family:
        score += 0.25
    if intent.body_intent:
        score += 0.22
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
    _parse_compact_body_intent(intent, normalized)

    rough_tokens = re.findall(r"[a-z0-9가-힣./-]+", normalized)
    for token in rough_tokens:
        if _parse_compact_family_token(intent, token):
            continue

        if token in {"leica", "라이카"}:
            intent.brand = "Leica"
            intent.tokens.append({"type": "brand", "raw": token, "value": "Leica"})
            continue

        if _adapter_intent_token_consumed(intent, token, normalized):
            continue

        if _compact_body_intent_token_consumed(intent, token, normalized):
            continue

        body_alias = _BODY_INTENT_ALIASES.get(token)
        if body_alias and _body_intent_token_allowed(token, rough_tokens):
            body_intent, body_mount, body_system = body_alias
            _set_body_intent(intent, body_intent, token, mount=body_mount, system=body_system)
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

        if _finder_intent_token_consumed(intent, token, normalized):
            continue

        if _adapter_intent_token_consumed(intent, token, normalized):
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
        intent.body_intent,
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
