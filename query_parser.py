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
    mount: Optional[str] = None
    system: Optional[str] = None
    variant: list[str] = field(default_factory=list)
    generation: Optional[str] = None
    filter_size: Optional[str] = None
    optical_formula: Optional[str] = None
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


def _score_confidence(intent: QueryIntent) -> float:
    score = 0.20
    if intent.model_family:
        score += 0.25
    if intent.focal_length:
        score += 0.20
    if intent.variant:
        score += 0.12
    if intent.generation:
        score += 0.10
    if intent.filter_size:
        score += 0.08
    if intent.mount or intent.system:
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
            intent.filter_size = f"E{size}"
            intent.tokens.append({"type": "filter_size", "raw": token, "value": intent.filter_size})
            continue

        focal_aperture_match = re.fullmatch(r"(\d{2,3})/(\d+(?:\.\d+)?)", token)
        if focal_aperture_match:
            focal, aperture = focal_aperture_match.groups()
            intent.focal_length = focal
            intent.tokens.append({"type": "focal_length", "raw": token, "value": focal})
            intent.tokens.append({"type": "aperture_hint", "raw": token, "value": aperture})
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

        if token not in {"매", "군"}:
            intent.tokens.append({"type": "unknown", "raw": token, "value": token})

    if not any([
        intent.model_family,
        intent.focal_length,
        intent.variant,
        intent.generation,
        intent.filter_size,
        intent.mount,
        intent.system,
        intent.optical_formula,
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
