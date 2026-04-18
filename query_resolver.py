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


WEIGHTS = {
    "brand": 6,
    "model_family": 25,
    "focal_length": 20,
    "mount_system": 12,
    "variant": 15,
    "generation": 8,
    "filter_size": 6,
    "optical_formula": 6,
    "aperture_hint": 5,
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
    return [
        str(token.get("value"))
        for token in intent.get("tokens", [])
        if token.get("type") == "aperture_hint" and token.get("value")
    ]


def _aperture_pattern(value: str) -> str:
    parts = str(value).split(".")
    if len(parts) == 1:
        return rf"\bf\s*{re.escape(parts[0])}\b"
    return rf"\bf\s*{re.escape(parts[0])}\s*{re.escape(parts[1])}\b"


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


def _structured_constraints(intent: dict[str, Any]) -> list[str]:
    fields = [
        "model_family",
        "focal_length",
        "mount",
        "system",
        "generation",
        "filter_size",
        "optical_formula",
    ]
    present = [field for field in fields if intent.get(field)]
    if intent.get("variant"):
        present.append("variant")
    if _explicit_brand_requested(intent):
        present.append("brand")
    if _aperture_hints(intent):
        present.append("aperture_hint")
    return present


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
        lambda: _score_optical_formula(intent, final, text, breakdown, matched, mismatches),
        lambda: _score_aperture_hint(intent, text, breakdown, matched, mismatches),
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
    if possible_score and score < 35:
        warnings.append("weak_match")

    return MatchResult(
        score=score,
        raw_score=round(raw_score, 2),
        possible_score=round(possible_score, 2),
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
    min_score: float = 1.0,
) -> dict[str, Any]:
    intent = parse_query(query_or_intent) if isinstance(query_or_intent, str) else query_or_intent
    results = [score_listing(intent, record) for record in records]
    results = [result for result in results if result["score"] >= min_score]
    results.sort(key=lambda item: (-item["score"], item.get("record_index") if item.get("record_index") is not None else 10**9))
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
