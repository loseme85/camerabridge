"""
query_resolver.py
=================
Search ranking layer.

Responsibilities:
  - Match QueryIntent objects against resolved listing records.
  - Prefer final_output over classifier_output.
  - Return score breakdowns and mismatch/warning details.

Non-responsibilities:
  - Do not classify listings.
  - Do not apply trusted overrides.
  - Do not import classifier_v2.py.
"""

from __future__ import annotations

from dataclasses import dataclass, field, asdict
import json
import re
from pathlib import Path
from typing import Any, Optional

from query_parser import parse_query


PROJECT_ROOT = Path(__file__).resolve().parent
DEFAULT_RESOLVED_PATH = PROJECT_ROOT / "data/derived/results_resolved_v2.json"
DEFAULT_MIN_SCORE = 25.0


WEIGHTS = {
    "brand": 6,
    "model_family": 25,
    "focal_length": 20,
    "mount_system": 12,
    "variant": 15,
    "generation": 8,
    "filter_size": 6,
    "filter_detail": 8,
    "adapter_detail": 8,
    "optical_formula": 6,
    "aperture_hint": 5,
    "accessory_intent": 18,
    "accessory_code": 22,
}

MATCH_QUALITY_RANKS = {
    "none": 0,
    "weak": 1,
    "medium": 2,
    "strong": 3,
}

BRAND_FAMILY_HINTS = {
    "Leica": {
        "elmar",
        "elmarit",
        "hektor",
        "mp3",
        "noctilux",
        "q2",
        "q3",
        "summarit",
        "summaron",
        "summicron",
        "summilux",
        "telyt",
        "tri elmar",
    },
    "Zeiss": {
        "biogon",
        "distagon",
        "planar",
        "sonnar",
        "zm",
    },
    "Voigtlander": {
        "color skopar",
        "heliar",
        "nokton",
        "skopar",
        "ultron",
    },
}

BRAND_CONTEXT_SIGNALS = {
    "Leica": {
        "mounts": {"L", "M", "SL"},
        "systems": {"Q"},
    },
}


@dataclass
class ScoreItem:
    field: str
    query_value: Any
    listing_value: Any
    weight: float
    awarded: float
    match_type: str
    listing_field: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class MatchResult:
    score: float
    raw_score: float
    possible_score: float
    match_quality: str = "none"
    match_quality_rank: int = 0
    implicit_brand_preference_score: float = 0.0
    implicit_brand_preference_reasons: list[str] = field(default_factory=list)
    matched_fields: list[str] = field(default_factory=list)
    score_breakdown: list[dict[str, Any]] = field(default_factory=list)
    mismatch_reasons: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    used_override: bool = False
    record_index: Optional[int] = None
    title_raw: Optional[str] = None
    source: Optional[str] = None
    source_url: Optional[str] = None
    final_output: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _normalize(value: Any) -> str:
    text = str(value or "").lower()
    text = text.replace("㎜", "mm").replace("ｍｍ", "mm")
    text = re.sub(r"[^a-z0-9가-힣]+", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def _contains_normalized_word(text: str, needle: str) -> bool:
    if not needle:
        return False
    if " " not in needle and needle in set(text.split()):
        return True
    return bool(re.search(rf"\b{re.escape(needle)}\b", text))


def _as_list(value: Any) -> list[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


def _final_output(record: dict[str, Any]) -> dict[str, Any]:
    final = record.get("final_output")
    if isinstance(final, dict):
        return final
    return record


def _raw_item(record: dict[str, Any]) -> dict[str, Any]:
    raw = record.get("raw_item")
    return raw if isinstance(raw, dict) else {}


def _source_text(record: dict[str, Any], final: dict[str, Any]) -> str:
    raw = _raw_item(record)
    parts = [
        final.get("model_canonical"),
        final.get("model_raw"),
        final.get("label"),
        final.get("title_raw"),
        final.get("normalized_name"),
        raw.get("상품명"),
        raw.get("label"),
        " ".join(str(item) for item in _as_list(final.get("variant"))),
    ]
    return _normalize(" ".join(str(part) for part in parts if part))


def _explicit_brand_requested(intent: dict[str, Any]) -> bool:
    if any(token.get("type") == "brand" for token in intent.get("tokens", [])):
        return True
    return bool(re.search(r"\b(leica|라이카)\b", intent.get("normalized_query", ""), re.IGNORECASE))


def _family_hint_brands(value: Any) -> set[str]:
    text = _normalize(value)
    if not text:
        return set()

    brands = set()
    for brand, hints in BRAND_FAMILY_HINTS.items():
        for hint in hints:
            hint_norm = _normalize(hint)
            if hint_norm and re.search(rf"\b{re.escape(hint_norm)}\b", text):
                brands.add(brand)
                break
    return brands


def _listing_family_hint_brands(final: dict[str, Any]) -> set[str]:
    values = [
        final.get("model_canonical"),
        final.get("model_raw"),
        final.get("label"),
    ]
    brands: set[str] = set()
    for value in values:
        brands.update(_family_hint_brands(value))
    return brands


def _query_has_brand_context(intent: dict[str, Any], brand: str) -> bool:
    context = BRAND_CONTEXT_SIGNALS.get(brand, {})
    if intent.get("model_family") and brand in _family_hint_brands(intent.get("model_family")):
        return True
    if intent.get("mount") in context.get("mounts", set()):
        return True
    if intent.get("system") in context.get("systems", set()):
        return True
    return False


def _implicit_brand_preference(
    intent: dict[str, Any],
    final: dict[str, Any],
    match_quality: str,
) -> tuple[float, list[str]]:
    """
    Soft tie-break for brand-unspecified collector shorthand.

    This does not change the relevance score and is only applied to strong
    matches, so it cannot promote weak or under-specified listings.
    """
    if match_quality != "strong" or _explicit_brand_requested(intent):
        return 0.0, []

    preferred_brand = intent.get("brand")
    if not preferred_brand or not _query_has_brand_context(intent, preferred_brand):
        return 0.0, []

    reasons: list[str] = []
    preference = 0.0
    listing_brand = final.get("brand")
    family_brands = _listing_family_hint_brands(final)

    if _normalize(listing_brand) == _normalize(preferred_brand):
        preference += 2.0
        reasons.append(f"listing_brand_matches_default:{preferred_brand}")

    if preferred_brand in family_brands:
        preference += 1.0
        reasons.append(f"model_family_affinity:{preferred_brand}")

    return preference, reasons


def _alias_expanded(intent: dict[str, Any], field_type: str, canonical_value: str) -> bool:
    canonical_norm = _normalize(canonical_value)
    for token in intent.get("tokens", []):
        if token.get("type") != field_type:
            continue
        if _normalize(token.get("raw")) != canonical_norm:
            return True
    return False


def _add_score(
    breakdown: list[dict[str, Any]],
    matched_fields: list[str],
    item: ScoreItem,
) -> float:
    if item.awarded > 0:
        matched_fields.append(item.field)
    breakdown.append(item.to_dict())
    return item.awarded


def _candidate_text_values(final: dict[str, Any], fields: list[str]) -> list[tuple[str, str]]:
    values = []
    for field_name in fields:
        value = final.get(field_name)
        if value:
            values.append((field_name, str(value)))
    return values


def _score_brand(intent: dict[str, Any], final: dict[str, Any], breakdown: list[dict[str, Any]], matched: list[str], mismatches: list[str]) -> tuple[float, float]:
    if not intent.get("brand") or not _explicit_brand_requested(intent):
        return 0.0, 0.0

    possible = WEIGHTS["brand"]
    query_brand = intent["brand"]
    listing_brand = final.get("brand")
    if _normalize(query_brand) == _normalize(listing_brand):
        awarded = _add_score(
            breakdown,
            matched,
            ScoreItem("brand", query_brand, listing_brand, possible, possible, "exact", "brand"),
        )
        return awarded, possible

    mismatches.append("brand_mismatch")
    breakdown.append(ScoreItem("brand", query_brand, listing_brand, possible, 0, "mismatch", "brand").to_dict())
    return 0.0, possible


def _score_model_family(intent: dict[str, Any], final: dict[str, Any], text: str, breakdown: list[dict[str, Any]], matched: list[str], mismatches: list[str]) -> tuple[float, float]:
    family = intent.get("model_family")
    if not family:
        return 0.0, 0.0

    possible = WEIGHTS["model_family"]
    family_norm = _normalize(family)
    values = _candidate_text_values(final, ["model_canonical", "model_raw", "label"])
    for field_name, value in values:
        value_norm = _normalize(value)
        if value_norm == family_norm:
            match_type = "alias_expanded" if _alias_expanded(intent, "model_family", family) else "exact"
            awarded = possible if match_type == "exact" else possible - 2
            return _add_score(
                breakdown,
                matched,
                ScoreItem("model_family", family, value, possible, awarded, match_type, field_name),
            ), possible
        if family_norm and re.search(rf"\b{re.escape(family_norm)}\b", value_norm):
            match_type = "alias_expanded" if _alias_expanded(intent, "model_family", family) else "normalized"
            awarded = possible - 2 if match_type == "alias_expanded" else possible - 1
            return _add_score(
                breakdown,
                matched,
                ScoreItem("model_family", family, value, possible, awarded, match_type, field_name),
            ), possible

    if family_norm and re.search(rf"\b{re.escape(family_norm)}\b", text):
        return _add_score(
            breakdown,
            matched,
            ScoreItem("model_family", family, "source_text", possible, 8, "weak_lexical_hit", "title_raw"),
        ), possible

    mismatches.append("model_family_mismatch")
    breakdown.append(ScoreItem("model_family", family, None, possible, 0, "mismatch", "model_canonical").to_dict())
    return 0.0, possible


def _score_focal_length(intent: dict[str, Any], final: dict[str, Any], text: str, breakdown: list[dict[str, Any]], matched: list[str], mismatches: list[str]) -> tuple[float, float]:
    focal = intent.get("focal_length")
    if not focal:
        return 0.0, 0.0

    possible = WEIGHTS["focal_length"]
    listing_focal = final.get("focal_length")
    if listing_focal:
        listing_norm = _normalize(listing_focal)
        focal_norm = _normalize(focal)
        if listing_norm == focal_norm:
            return _add_score(
                breakdown,
                matched,
                ScoreItem("focal_length", focal, listing_focal, possible, possible, "exact", "focal_length"),
            ), possible

        range_parts = re.findall(r"\d{2,3}", str(listing_focal))
        if focal in range_parts:
            return _add_score(
                breakdown,
                matched,
                ScoreItem("focal_length", focal, listing_focal, possible, 15, "range_compatible", "focal_length"),
            ), possible

    if re.search(rf"\b{re.escape(str(focal))}\s*(mm|/)\b", text):
        return _add_score(
            breakdown,
            matched,
            ScoreItem("focal_length", focal, "source_text", possible, 8, "weak_lexical_hit", "title_raw"),
        ), possible

    mismatches.append("focal_length_mismatch")
    breakdown.append(ScoreItem("focal_length", focal, listing_focal, possible, 0, "mismatch", "focal_length").to_dict())
    return 0.0, possible


def _listing_system(record: dict[str, Any], final: dict[str, Any]) -> str:
    raw = _raw_item(record)
    return str(final.get("system") or raw.get("system") or "")


def _score_mount_system(intent: dict[str, Any], record: dict[str, Any], final: dict[str, Any], breakdown: list[dict[str, Any]], matched: list[str], mismatches: list[str]) -> tuple[float, float]:
    query_mount = intent.get("mount")
    query_system = intent.get("system")
    if not query_mount and not query_system:
        return 0.0, 0.0

    possible = WEIGHTS["mount_system"]
    listing_mount = final.get("mount")
    listing_system = _listing_system(record, final)

    if query_mount:
        if _normalize(query_mount) == _normalize(listing_mount):
            return _add_score(
                breakdown,
                matched,
                ScoreItem("mount", query_mount, listing_mount, possible, possible, "exact", "mount"),
            ), possible
        mismatches.append("mount_mismatch")
        breakdown.append(ScoreItem("mount", query_mount, listing_mount, possible, 0, "mismatch", "mount").to_dict())
        return 0.0, possible

    if query_system:
        query_norm = _normalize(query_system)
        if query_norm in {_normalize(listing_mount), _normalize(listing_system)}:
            return _add_score(
                breakdown,
                matched,
                ScoreItem("system", query_system, listing_system or listing_mount, possible, possible, "exact", "system"),
            ), possible
        if query_system == "Q" and listing_mount == "Q":
            return _add_score(
                breakdown,
                matched,
                ScoreItem("system", query_system, listing_mount, possible, possible, "mount_system_equivalent", "mount"),
            ), possible
        mismatches.append("system_mismatch")
        breakdown.append(ScoreItem("system", query_system, listing_system or listing_mount, possible, 0, "mismatch", "system").to_dict())
        return 0.0, possible

    return 0.0, 0.0


def _score_variants(intent: dict[str, Any], final: dict[str, Any], text: str, breakdown: list[dict[str, Any]], matched: list[str], mismatches: list[str]) -> tuple[float, float]:
    variants = intent.get("variant") or []
    if not variants:
        return 0.0, 0.0

    possible = WEIGHTS["variant"]
    per_variant = possible / len(variants)
    awarded_total = 0.0
    listing_variants = [str(item) for item in _as_list(final.get("variant"))]
    listing_variant_norms = {_normalize(item) for item in listing_variants}

    for variant in variants:
        variant_norm = _normalize(variant)
        if variant_norm in listing_variant_norms:
            awarded_total += _add_score(
                breakdown,
                matched,
                ScoreItem("variant", variant, listing_variants, per_variant, per_variant, "exact", "variant"),
            )
        elif variant_norm and re.search(rf"\b{re.escape(variant_norm)}\b", text):
            awarded_total += _add_score(
                breakdown,
                matched,
                ScoreItem("variant", variant, "source_text", per_variant, per_variant * 0.55, "partial_variant_hit", "title_raw"),
            )
        else:
            mismatches.append(f"variant_mismatch:{variant}")
            breakdown.append(ScoreItem("variant", variant, listing_variants, per_variant, 0, "mismatch", "variant").to_dict())

    return awarded_total, possible


def _score_generation(intent: dict[str, Any], final: dict[str, Any], text: str, breakdown: list[dict[str, Any]], matched: list[str], mismatches: list[str]) -> tuple[float, float]:
    generation = intent.get("generation")
    if not generation:
        return 0.0, 0.0

    possible = WEIGHTS["generation"]
    gen_norm = _normalize(generation)
    raw_generation = _raw_item(final).get("세대") if isinstance(final, dict) else None
    listing_values = " ".join(str(item) for item in _as_list(final.get("variant")) + [final.get("model_canonical"), raw_generation])
    listing_norm = _normalize(listing_values)

    if gen_norm and (re.search(rf"\b{re.escape(gen_norm)}\b", listing_norm) or re.search(rf"\b{re.escape(gen_norm)}\b", text)):
        return _add_score(
            breakdown,
            matched,
            ScoreItem("generation", generation, listing_values or "source_text", possible, possible, "normalized", "variant/title_raw"),
        ), possible

    mismatches.append("generation_mismatch")
    breakdown.append(ScoreItem("generation", generation, listing_values, possible, 0, "mismatch", "variant/title_raw").to_dict())
    return 0.0, possible


def _score_filter_size(intent: dict[str, Any], text: str, breakdown: list[dict[str, Any]], matched: list[str], mismatches: list[str]) -> tuple[float, float]:
    filter_size = intent.get("filter_size")
    if not filter_size:
        return 0.0, 0.0

    possible = WEIGHTS["filter_size"]
    filter_norm = _normalize(filter_size)
    if filter_norm and re.search(rf"\b{re.escape(filter_norm)}\b", text):
        return _add_score(
            breakdown,
            matched,
            ScoreItem("filter_size", filter_size, "source_text", possible, possible, "weak_spec_hint", "title_raw"),
        ), possible

    mismatches.append("filter_size_mismatch")
    breakdown.append(ScoreItem("filter_size", filter_size, None, possible, 0, "mismatch", "title_raw").to_dict())
    return 0.0, possible


def _filter_detail_tokens(intent: dict[str, Any]) -> list[dict[str, str]]:
    if intent.get("accessory_intent") != "filter":
        return []
    return [
        token
        for token in intent.get("tokens", [])
        if token.get("type") in {"filter_kind", "filter_brand", "filter_color"}
    ]


def _score_filter_detail(intent: dict[str, Any], text: str, breakdown: list[dict[str, Any]], matched: list[str], mismatches: list[str]) -> tuple[float, float]:
    details = _filter_detail_tokens(intent)
    if not details:
        return 0.0, 0.0

    possible = WEIGHTS["filter_detail"]
    per_detail = possible / len(details)
    awarded_total = 0.0
    for detail in details:
        value = detail.get("value") or detail.get("raw")
        value_norm = _normalize(value)
        if value_norm and _contains_normalized_word(text, value_norm):
            awarded_total += _add_score(
                breakdown,
                matched,
                ScoreItem("filter_detail", value, "source_text", per_detail, per_detail, "exact_text_hint", "title_raw"),
            )
        else:
            mismatches.append(f"filter_detail_mismatch:{value}")
            breakdown.append(ScoreItem("filter_detail", value, None, per_detail, 0, "mismatch", "title_raw").to_dict())
    return awarded_total, possible


def _adapter_detail_tokens(intent: dict[str, Any]) -> list[dict[str, str]]:
    if intent.get("accessory_intent") != "adapter":
        return []
    return [
        token
        for token in intent.get("tokens", [])
        if token.get("type") == "adapter_detail"
    ]


def _adapter_detail_text_hit(value: str, text: str) -> bool:
    value_norm = _normalize(value)
    if value_norm == "macro":
        return _contains_normalized_word(text, "macro")
    if value_norm == "m l":
        return bool(re.search(r"\bm\s+l\b|\bm\s+adapter\s+l\b|\blm\s+to\s+l\b|\bm\s+to\s+l\b", text))
    if value_norm == "m":
        return bool(re.search(r"\bm\s+adapter\b|\badapter\s+m\b|\bm\s+l\b|\bm\s+adapter\s+l\b", text))
    return bool(value_norm and _contains_normalized_word(text, value_norm))


def _score_adapter_detail(intent: dict[str, Any], text: str, breakdown: list[dict[str, Any]], matched: list[str], mismatches: list[str]) -> tuple[float, float]:
    details = _adapter_detail_tokens(intent)
    if not details:
        return 0.0, 0.0

    possible = WEIGHTS["adapter_detail"]
    per_detail = possible / len(details)
    awarded_total = 0.0
    for detail in details:
        value = detail.get("value") or detail.get("raw")
        if value and _adapter_detail_text_hit(value, text):
            awarded_total += _add_score(
                breakdown,
                matched,
                ScoreItem("adapter_detail", value, "source_text", per_detail, per_detail, "exact_text_hint", "title_raw"),
            )
        else:
            mismatches.append(f"adapter_detail_mismatch:{value}")
            breakdown.append(ScoreItem("adapter_detail", value, None, per_detail, 0, "mismatch", "title_raw").to_dict())
    return awarded_total, possible


def _score_optical_formula(intent: dict[str, Any], final: dict[str, Any], text: str, breakdown: list[dict[str, Any]], matched: list[str], mismatches: list[str]) -> tuple[float, float]:
    formula = intent.get("optical_formula")
    if not formula:
        return 0.0, 0.0

    possible = WEIGHTS["optical_formula"]
    formula_norm = _normalize(formula)
    compact_formula = formula_norm.replace(" groups ", " group ").replace(" elements", " element")
    if formula_norm and (formula_norm in text or compact_formula in text):
        return _add_score(
            breakdown,
            matched,
            ScoreItem("optical_formula", formula, "source_text", possible, possible, "exact_text_hint", "title_raw"),
        ), possible

    if "8 element" in text or "8매" in text or "8 element" in _normalize(final.get("variant")):
        return _add_score(
            breakdown,
            matched,
            ScoreItem("optical_formula", formula, "8-element hint", possible, possible * 0.65, "partial_formula_hint", "variant/title_raw"),
        ), possible

    mismatches.append("optical_formula_mismatch")
    breakdown.append(ScoreItem("optical_formula", formula, None, possible, 0, "mismatch", "variant/title_raw").to_dict())
    return 0.0, possible


def _aperture_hints(intent: dict[str, Any]) -> list[str]:
    hints: list[str] = []
    if intent.get("aperture"):
        hints.append(str(intent["aperture"]))

    for token in intent.get("tokens", []):
        if token.get("type") not in {"aperture", "aperture_hint"} or not token.get("value"):
            continue
        value = str(token["value"])
        if value not in hints:
            hints.append(value)
    return hints


def _aperture_pattern(value: str) -> str:
    parts = str(value).split(".")
    if len(parts) == 1:
        return rf"\bf\s*{re.escape(parts[0])}\b"
    return rf"\bf\s*{re.escape(parts[0])}\s+{re.escape(parts[1])}\b"


def _score_aperture_hint(intent: dict[str, Any], text: str, breakdown: list[dict[str, Any]], matched: list[str], mismatches: list[str]) -> tuple[float, float]:
    hints = _aperture_hints(intent)
    if not hints:
        return 0.0, 0.0

    possible = WEIGHTS["aperture_hint"]
    per_hint = possible / len(hints)
    awarded_total = 0.0
    for hint in hints:
        if re.search(_aperture_pattern(hint), text):
            awarded_total += _add_score(
                breakdown,
                matched,
                ScoreItem("aperture_hint", hint, "source_text", per_hint, per_hint, "exact_text_hint", "title_raw"),
            )
        else:
            mismatches.append(f"aperture_hint_mismatch:{hint}")
            breakdown.append(ScoreItem("aperture_hint", hint, None, per_hint, 0, "mismatch", "title_raw").to_dict())
    return awarded_total, possible


def _score_accessory_intent(
    intent: dict[str, Any],
    final: dict[str, Any],
    text: str,
    breakdown: list[dict[str, Any]],
    matched: list[str],
    mismatches: list[str],
) -> tuple[float, float]:
    accessory_intent = intent.get("accessory_intent")
    accessory_code = intent.get("accessory_code")
    if not accessory_intent and not accessory_code:
        return 0.0, 0.0

    awarded_total = 0.0
    possible_total = 0.0

    if accessory_intent:
        possible = WEIGHTS["accessory_intent"]
        possible_total += possible
        category = final.get("category")
        accessory_type = final.get("accessory_type")
        if _normalize(category) == "accessory":
            has_intent_text = _accessory_intent_text_hit(accessory_intent, text)
            if accessory_type and _normalize(accessory_type) == _normalize(accessory_intent):
                match_type = "category_type_exact"
                awarded = possible
            elif has_intent_text:
                match_type = "category_text_exact"
                awarded = possible
            else:
                match_type = "category_broad_accessory"
                awarded = 3
            awarded_total += _add_score(
                breakdown,
                matched,
                ScoreItem("accessory_intent", accessory_intent, category, possible, awarded, match_type, "category/title_raw"),
            )
        elif _accessory_intent_text_hit(accessory_intent, text):
            # Lens bundles such as "21mm lens + Hood" or "lens - UVa Filter"
            # remain visible, but they should not outrank standalone Accessory
            # records for explicit accessory queries.
            awarded_total += _add_score(
                breakdown,
                matched,
                ScoreItem("accessory_intent", accessory_intent, category, possible, 4, "bundle_text_hint", "title_raw"),
            )
        else:
            mismatches.append("accessory_intent_mismatch")
            breakdown.append(
                ScoreItem("accessory_intent", accessory_intent, category, possible, 0, "mismatch", "category").to_dict()
            )

    if accessory_code:
        possible = WEIGHTS["accessory_code"]
        possible_total += possible
        code_norm = _normalize(accessory_code)
        if code_norm and _contains_normalized_word(text, code_norm):
            awarded_total += _add_score(
                breakdown,
                matched,
                ScoreItem("accessory_code", accessory_code, "source_text", possible, possible, "exact_text_hint", "title_raw"),
            )
        else:
            mismatches.append("accessory_code_mismatch")
            breakdown.append(
                ScoreItem("accessory_code", accessory_code, None, possible, 0, "mismatch", "title_raw").to_dict()
            )

    return awarded_total, possible_total


def _accessory_intent_text_hit(accessory_intent: str, text: str) -> bool:
    if accessory_intent == "hood":
        return bool(re.search(r"\bhood\b|후드", text))
    if accessory_intent == "filter":
        return bool(
            re.search(
                r"\b(?:filter|fiter|uv|uva|uvir|nd|skylight)\b|\bb\s+w\b|필터",
                text,
            )
        )
    if accessory_intent == "adapter":
        return bool(re.search(r"\b(?:adapter|adaptor)\b|어댑터", text))
    return False


def _has_positive(
    breakdown: list[dict[str, Any]],
    field_name: str,
    match_types: Optional[set[str]] = None,
) -> bool:
    for item in breakdown:
        if item.get("field") != field_name or float(item.get("awarded") or 0) <= 0:
            continue
        if match_types is None or item.get("match_type") in match_types:
            return True
    return False


def _match_quality(
    intent: dict[str, Any],
    breakdown: list[dict[str, Any]],
    mismatches: list[str],
) -> tuple[str, int]:
    """
    Summarize ranking confidence without changing classifier output.

    Strong means a listing satisfies multiple structured anchors. Medium means
    a plausible core match exists but is missing one important anchor. Weak is
    reserved for mount-only, focal-only, or source-text-only hits.
    """
    if not any(float(item.get("awarded") or 0) > 0 for item in breakdown):
        return "none", MATCH_QUALITY_RANKS["none"]

    if "mount_mismatch" in mismatches or "system_mismatch" in mismatches or "brand_mismatch" in mismatches:
        return "weak", MATCH_QUALITY_RANKS["weak"]

    precise_family = _has_positive(breakdown, "model_family", {"exact", "alias_expanded", "normalized"})
    precise_focal = _has_positive(breakdown, "focal_length", {"exact", "range_compatible"})
    focal_hit = _has_positive(breakdown, "focal_length")
    mount_hit = _has_positive(breakdown, "mount", {"exact"})
    system_hit = _has_positive(breakdown, "system", {"exact", "mount_system_equivalent"})
    variant_hit = _has_positive(breakdown, "variant")
    aperture_hit = _has_positive(breakdown, "aperture_hint", {"exact_text_hint"})
    accessory_hit = _has_positive(breakdown, "accessory_intent", {"category_type_exact", "category_text_exact"})
    accessory_code_hit = _has_positive(breakdown, "accessory_code", {"exact_text_hint"})
    generation_hit = _has_positive(breakdown, "generation")
    filter_hit = _has_positive(breakdown, "filter_size")
    formula_hit = _has_positive(breakdown, "optical_formula")
    mount_or_system_hit = mount_hit or system_hit

    if precise_family and precise_focal and (
        mount_or_system_hit
        or variant_hit
        or aperture_hit
        or generation_hit
        or filter_hit
        or formula_hit
    ):
        return "strong", MATCH_QUALITY_RANKS["strong"]

    if precise_family and variant_hit and not intent.get("focal_length"):
        return "strong", MATCH_QUALITY_RANKS["strong"]

    if mount_or_system_hit and precise_focal and aperture_hit:
        return "strong", MATCH_QUALITY_RANKS["strong"]

    if precise_focal and aperture_hit and generation_hit:
        return "strong", MATCH_QUALITY_RANKS["strong"]

    if accessory_hit and accessory_code_hit:
        return "strong", MATCH_QUALITY_RANKS["strong"]

    has_lens_specific_adapter_constraint = bool(
        intent.get("model_family")
        or intent.get("focal_length")
        or _aperture_hints(intent)
        or intent.get("generation")
        or intent.get("variant")
    )
    if intent.get("accessory_intent") == "adapter" and accessory_hit and not has_lens_specific_adapter_constraint:
        return "strong", MATCH_QUALITY_RANKS["strong"]

    if precise_family and precise_focal:
        return "medium", MATCH_QUALITY_RANKS["medium"]

    if precise_family and (variant_hit or mount_or_system_hit or aperture_hit or generation_hit or filter_hit or formula_hit):
        return "medium", MATCH_QUALITY_RANKS["medium"]

    if mount_or_system_hit and focal_hit:
        return "medium", MATCH_QUALITY_RANKS["medium"]

    if precise_focal and aperture_hit:
        return "medium", MATCH_QUALITY_RANKS["medium"]

    if formula_hit or filter_hit:
        return "medium", MATCH_QUALITY_RANKS["medium"]

    if accessory_hit or accessory_code_hit:
        return "medium", MATCH_QUALITY_RANKS["medium"]

    return "weak", MATCH_QUALITY_RANKS["weak"]


def _structured_constraints(intent: dict[str, Any]) -> list[str]:
    fields = [
        "model_family",
        "focal_length",
        "mount",
        "system",
        "generation",
        "filter_size",
        "optical_formula",
        "accessory_intent",
        "accessory_code",
    ]
    present = [field for field in fields if intent.get(field)]
    if intent.get("variant"):
        present.append("variant")
    if _explicit_brand_requested(intent):
        present.append("brand")
    if _aperture_hints(intent):
        present.append("aperture_hint")
    return present


def _essential_unparsed_tokens(intent: dict[str, Any]) -> list[str]:
    return [
        str(token.get("raw"))
        for token in intent.get("tokens", [])
        if token.get("type") == "unknown"
        and re.fullmatch(r"f/?\d+(?:\.\d+)?|\d+\.\d+", str(token.get("raw") or ""))
    ]


def _has_aperture_mismatch(mismatches: list[str]) -> bool:
    return any(reason.startswith("aperture_hint_mismatch:") for reason in mismatches)


def _suppress_broad_essential_fallback(
    score: float,
    match_quality: str,
    match_quality_rank: int,
    intent: dict[str, Any],
    breakdown: list[dict[str, Any]],
    mismatches: list[str],
    warnings: list[str],
) -> tuple[float, str, int]:
    """
    Keep broad fallback visible but stop it from dominating essential misses.

    This is intentionally narrow: aperture-like user intent is treated as an
    essential search constraint only when the parser saw it or flagged an
    aperture-like token as unparsed. It does not change classifier output.
    """
    essential_unknowns = _essential_unparsed_tokens(intent)
    if essential_unknowns:
        warnings.append("essential_unparsed_tokens:" + ",".join(essential_unknowns))
        if match_quality in {"weak", "medium"}:
            score = min(score, 60.0)
            match_quality = "weak"
            match_quality_rank = MATCH_QUALITY_RANKS["weak"]

    if _has_aperture_mismatch(mismatches):
        warnings.append("essential_constraint_mismatch:aperture")
        precise_family = _has_positive(breakdown, "model_family", {"exact", "alias_expanded", "normalized"})
        if not precise_family:
            score = min(score, 72.0)
            if match_quality == "medium":
                match_quality = "weak"
                match_quality_rank = MATCH_QUALITY_RANKS["weak"]

    return score, match_quality, match_quality_rank


def score_listing(intent: dict[str, Any], record: dict[str, Any]) -> dict[str, Any]:
    final = _final_output(record)
    text = _source_text(record, final)
    matched: list[str] = []
    breakdown: list[dict[str, Any]] = []
    mismatches: list[str] = []
    warnings = list(intent.get("warnings") or [])
    raw = _raw_item(record)

    unknown_tokens = [token["raw"] for token in intent.get("tokens", []) if token.get("type") == "unknown"]
    if unknown_tokens:
        warnings.append("unparsed_tokens:" + ",".join(unknown_tokens))

    if not _structured_constraints(intent):
        warnings.append("ambiguous_query:no_structured_constraints")

    raw_score = 0.0
    possible_score = 0.0
    for scorer in [
        lambda: _score_brand(intent, final, breakdown, matched, mismatches),
        lambda: _score_model_family(intent, final, text, breakdown, matched, mismatches),
        lambda: _score_focal_length(intent, final, text, breakdown, matched, mismatches),
        lambda: _score_mount_system(intent, record, final, breakdown, matched, mismatches),
        lambda: _score_variants(intent, final, text, breakdown, matched, mismatches),
        lambda: _score_generation(intent, final, text, breakdown, matched, mismatches),
        lambda: _score_filter_size(intent, text, breakdown, matched, mismatches),
        lambda: _score_filter_detail(intent, text, breakdown, matched, mismatches),
        lambda: _score_adapter_detail(intent, text, breakdown, matched, mismatches),
        lambda: _score_optical_formula(intent, final, text, breakdown, matched, mismatches),
        lambda: _score_aperture_hint(intent, text, breakdown, matched, mismatches),
        lambda: _score_accessory_intent(intent, final, text, breakdown, matched, mismatches),
    ]:
        awarded, possible = scorer()
        raw_score += awarded
        possible_score += possible

    score = round((raw_score / possible_score) * 100, 2) if possible_score else 0.0
    if "mount_mismatch" in mismatches or "system_mismatch" in mismatches:
        score = min(score, 40.0)
        warnings.append("hard_constraint_mismatch:mount_or_system")
    if "brand_mismatch" in mismatches:
        score = min(score, 40.0)
        warnings.append("hard_constraint_mismatch:brand")
    if "accessory_intent_mismatch" in mismatches and intent.get("accessory_intent"):
        warnings.append("accessory_intent_non_accessory_listing")
    if "accessory_code_mismatch" in mismatches and intent.get("accessory_code"):
        warnings.append("accessory_code_mismatch")
    match_quality, match_quality_rank = _match_quality(intent, breakdown, mismatches)
    score, match_quality, match_quality_rank = _suppress_broad_essential_fallback(
        score,
        match_quality,
        match_quality_rank,
        intent,
        breakdown,
        mismatches,
        warnings,
    )
    implicit_preference_score, implicit_preference_reasons = _implicit_brand_preference(
        intent,
        final,
        match_quality,
    )
    if possible_score and (score < 35 or match_quality in {"none", "weak"}):
        warnings.append("weak_match")

    return MatchResult(
        score=score,
        raw_score=round(raw_score, 2),
        possible_score=round(possible_score, 2),
        match_quality=match_quality,
        match_quality_rank=match_quality_rank,
        implicit_brand_preference_score=implicit_preference_score,
        implicit_brand_preference_reasons=implicit_preference_reasons,
        matched_fields=matched,
        score_breakdown=breakdown,
        mismatch_reasons=mismatches,
        warnings=warnings,
        used_override=bool(record.get("override_applied")),
        record_index=record.get("record_index"),
        title_raw=final.get("title_raw") or raw.get("상품명"),
        source=final.get("source") or raw.get("site"),
        source_url=final.get("source_url") or raw.get("링크"),
        final_output=final,
    ).to_dict()


def rank_listings(
    query_or_intent: str | dict[str, Any],
    records: list[dict[str, Any]],
    limit: int = 10,
    min_score: float = DEFAULT_MIN_SCORE,
) -> dict[str, Any]:
    intent = parse_query(query_or_intent) if isinstance(query_or_intent, str) else query_or_intent
    results = [score_listing(intent, record) for record in records]
    results = [result for result in results if result["score"] >= min_score]
    results.sort(
        key=lambda item: (
            -int(item.get("match_quality_rank") or 0),
            -item["score"],
            -float(item.get("implicit_brand_preference_score") or 0.0),
            item.get("record_index") if item.get("record_index") is not None else 10**9,
        )
    )
    return {
        "intent": intent,
        "results": results[:limit],
        "total_ranked": len(results),
    }


def load_resolved_records(path: str | Path = DEFAULT_RESOLVED_PATH) -> list[dict[str, Any]]:
    with open(path, encoding="utf-8") as f:
        payload = json.load(f)
    if not isinstance(payload, list):
        raise ValueError(f"{path} must contain a list of resolved records")
    return payload


def _compact_result(result: dict[str, Any]) -> dict[str, Any]:
    final = result.get("final_output", {})
    return {
        "score": result["score"],
        "title": result["title_raw"],
        "source": result["source"],
        "used_override": result["used_override"],
        "matched_fields": result["matched_fields"],
        "model_canonical": final.get("model_canonical"),
        "focal_length": final.get("focal_length"),
        "mount": final.get("mount"),
        "variant": final.get("variant"),
        "match_quality": result.get("match_quality"),
        "implicit_brand_preference_score": result.get("implicit_brand_preference_score"),
        "implicit_brand_preference_reasons": result.get("implicit_brand_preference_reasons"),
        "warnings": result["warnings"],
    }


def run_ranking_demo(
    queries: Optional[list[str]] = None,
    path: str | Path = DEFAULT_RESOLVED_PATH,
    limit: int = 3,
) -> list[dict[str, Any]]:
    records = load_resolved_records(path)
    demo_queries = queries or [
        "35lux aa",
        "50cron 2nd",
        "nocti e60",
        "8매",
        "6군8매",
        "ltm summaron 35",
        "q3 28",
        "mp3 silver",
        "sl 35/2",
        "m 21/2.8",
    ]
    output = []
    for query in demo_queries:
        ranked = rank_listings(query, records, limit=limit, min_score=25)
        output.append(
            {
                "query": query,
                "intent": ranked["intent"],
                "top_results": [_compact_result(result) for result in ranked["results"]],
            }
        )
    return output


if __name__ == "__main__":
    print(json.dumps(run_ranking_demo(), ensure_ascii=False, indent=2))
