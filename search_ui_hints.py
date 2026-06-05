"""
search_ui_hints.py
==================
Query-level UI hint policy for broad or ambiguous search queries.

Responsibilities:
  - Classify known broad query patterns.
  - Return additive UI metadata for API consumers.
  - Stay strictly out of ranking, filtering, and result ordering.
"""

from __future__ import annotations

import re
from typing import Any


POLICY_VERSION = "p3_broad_query_ambiguity_ui_v0"


def _normalize_query(query: Any) -> str:
    return re.sub(r"\s+", " ", str(query or "").strip().lower())


def _normalize_signal_text(query: Any) -> str:
    text = str(query or "").lower()
    text = text.replace("l-mount", "l mount").replace("l마운트", "l mount")
    text = text.replace("sl 마운트", "sl mount").replace("dgdn", "dg dn")
    text = text.replace("시그마", "sigma").replace("아트", "art")
    text = text.replace("f/2.8", "f2.8")
    text = re.sub(r"[^a-z0-9가-힣]+", " ", text)
    return f" {re.sub(r'\\s+', ' ', text).strip()} "


def _default_hints() -> dict[str, Any]:
    return {
        "needs_disambiguation": False,
        "ambiguity_type": "none",
        "recommended_ui_pattern": "no_disambiguation_needed",
        "recommended_chips": [],
        "suggested_filters": {},
        "hard_pin_allowed": False,
        "recommended_message": "",
        "policy_version": POLICY_VERSION,
    }


def _hints(
    *,
    needs_disambiguation: bool,
    ambiguity_type: str,
    recommended_ui_pattern: str,
    recommended_chips: list[str],
    suggested_filters: dict[str, Any],
    hard_pin_allowed: bool,
    recommended_message: str,
) -> dict[str, Any]:
    return {
        "needs_disambiguation": needs_disambiguation,
        "ambiguity_type": ambiguity_type,
        "recommended_ui_pattern": recommended_ui_pattern,
        "recommended_chips": recommended_chips,
        "suggested_filters": suggested_filters,
        "hard_pin_allowed": hard_pin_allowed,
        "recommended_message": recommended_message,
        "policy_version": POLICY_VERSION,
    }


BROAD_FAMILY_ALIASES = {
    "summicron": {
        "chips": ["M Lens", "R Lens", "SL Lens", "LTM / L Lens", "35mm", "50mm", "90mm", "APO", "ASPH"],
        "filters": {
            "category": ["Lens"],
            "mount": ["M", "R", "SL", "L"],
            "family": ["Summicron", "Summicron-M", "Summicron-R", "Summicron-SL", "APO-Summicron-SL"],
        },
    },
    "leica summicron": {
        "chips": ["M Lens", "R Lens", "SL Lens", "LTM / L Lens", "35mm", "50mm", "90mm", "APO", "ASPH"],
        "filters": {
            "category": ["Lens"],
            "mount": ["M", "R", "SL", "L"],
            "family": ["Summicron", "Summicron-M", "Summicron-R", "Summicron-SL", "APO-Summicron-SL"],
        },
    },
    "summilux": {
        "chips": ["M Lens", "R Lens", "SL Lens", "LTM / L Lens", "35mm", "50mm", "90mm", "APO", "ASPH"],
        "filters": {
            "category": ["Lens"],
            "mount": ["M", "R", "SL", "L"],
            "family": ["Summilux", "Summilux-M", "Summilux-R", "Summilux-SL"],
        },
    },
    "leica summilux": {
        "chips": ["M Lens", "R Lens", "SL Lens", "LTM / L Lens", "35mm", "50mm", "90mm", "APO", "ASPH"],
        "filters": {
            "category": ["Lens"],
            "mount": ["M", "R", "SL", "L"],
            "family": ["Summilux", "Summilux-M", "Summilux-R", "Summilux-SL"],
        },
    },
}


BARE_SHORT_ALIASES = {
    "cron": {
        "family": ["Summicron", "Summicron-M", "Summicron-R", "Summicron-SL", "APO-Summicron"],
    },
    "lux": {
        "family": ["Summilux", "Summilux-M", "Summilux-R", "Summilux-SL"],
    },
}


FOCAL_CRON_ALIASES = {"50 cron", "leica 50 cron"}
FOCAL_LUX_STRONG = {"35 lux": "35mm", "50 lux": "50mm"}
FOCAL_LUX_WEAK = {"leica 35 lux": "35mm", "leica 50 lux": "50mm"}

BROAD_R_QUERIES = {
    "leica r",
    "r lens",
    "r summicron",
    "r elmarit",
    "r apo",
    "r telyt",
    "r vario",
    "leica r 28-90",
}

BROAD_ACCESSORY_QUERIES = {
    "leica cap",
    "leica battery",
    "leica strap",
    "leica hood",
    "leica adapter",
    "leica filter",
    "leica finder",
    "body cap",
    "lens cap",
    "rear cap",
    "front cap",
}

BROAD_GENERIC_LENS_QUERIES = {
    "leica lens",
    "leica lenses",
}

SOURCE_COVERAGE_GAP_QUERIES = {
    "sigma 14-24 l",
    "sigma 14-24 l mount",
    "sigma 14-24 dg dn",
    "sigma 14-24 dg dn art",
}

SPECIFIC_GUARDRAIL_QUERIES = {
    "m 50 cron",
    "r 50 cron",
    "sl 50 cron",
    "m 35 lux",
    "m 50 lux",
    "summicron m 50",
    "m 50 summicron",
    "r 50 summicron",
    "summicron-r 50",
    "summicron sl 35",
    "sl 50 summicron",
    "sl 24-90",
    "sl 90-280",
    "leica sl2",
    "leica sl3",
    "sl3 battery",
    "leica handgrip",
    "panasonic 24-105 l",
    "lumix 24-105",
}


def _is_sigma_14_24_source_gap_alias(query: str, result_count: int) -> bool:
    if result_count > 0:
        return False

    text = _normalize_signal_text(query)
    tokens = set(text.split())

    if "sigma" not in tokens:
        return False
    if "14 24" not in text:
        return False

    disallowed_mount_terms = {
        "canon",
        "nikon",
        "sony",
        "fuji",
        "fujifilm",
        "pentax",
        "mft",
        "m43",
        "micro43",
        "micro",
        "fourthirds",
        "rf",
        "ef",
        "efs",
        "eos",
        "z",
        "xf",
        "x",
        "e",
    }
    if tokens & disallowed_mount_terms:
        return False

    mount_or_family_signals = [
        " l ",
        " l mount ",
        " sl mount ",
        " dg dn ",
        " art ",
        " f2 8 ",
        " 2 8 ",
    ]
    return any(signal in text for signal in mount_or_family_signals)


def build_query_ui_hints(query: str, results: list[dict[str, Any]] | None = None) -> dict[str, Any]:
    norm = _normalize_query(query)
    result_count = len(results or [])

    if norm in BROAD_FAMILY_ALIASES:
        policy = BROAD_FAMILY_ALIASES[norm]
        return _hints(
            needs_disambiguation=True,
            ambiguity_type="broad_family_alias",
            recommended_ui_pattern="refinement_chips",
            recommended_chips=policy["chips"],
            suggested_filters=policy["filters"],
            hard_pin_allowed=False,
            recommended_message="This is a broad Leica lens family query. Refine by mount, focal length, or variant.",
        )

    if norm in BROAD_GENERIC_LENS_QUERIES:
        return _hints(
            needs_disambiguation=True,
            ambiguity_type="broad_generic_lens_query",
            recommended_ui_pattern="refinement_chips",
            recommended_chips=["M Lens", "R Lens", "SL Lens", "35mm", "50mm", "90mm", "Summicron", "Summilux"],
            suggested_filters={
                "category": ["Lens"],
                "mount": ["M", "R", "SL", "L"],
            },
            hard_pin_allowed=False,
            recommended_message="This query is too broad for a model-level summary. Refine by family, mount, or focal length first.",
        )

    if norm in BARE_SHORT_ALIASES:
        family = BARE_SHORT_ALIASES[norm]["family"]
        return _hints(
            needs_disambiguation=True,
            ambiguity_type="short_alias_bare",
            recommended_ui_pattern="family_selector",
            recommended_chips=["Did you mean Summicron?", "Did you mean Summilux?", "M", "R", "SL", "Show only lenses"],
            suggested_filters={
                "category": ["Lens"],
                "mount": ["M", "R", "SL"],
                "family": family,
            },
            hard_pin_allowed=False,
            recommended_message="Collector shorthand can match multiple Leica lens families. Choose a family or mount to refine.",
        )

    if norm in FOCAL_CRON_ALIASES:
        return _hints(
            needs_disambiguation=True,
            ambiguity_type="focal_short_alias",
            recommended_ui_pattern="mount_selector",
            recommended_chips=["M 50 Summicron", "R 50 Summicron", "SL 50 Summicron", "Show all 50mm"],
            suggested_filters={
                "category": ["Lens"],
                "mount": ["M", "R", "SL"],
                "focal_length": ["50mm"],
                "family": ["Summicron", "Summicron-M", "Summicron-R", "Summicron-SL", "APO-Summicron-SL"],
            },
            hard_pin_allowed=False,
            recommended_message="50 cron can refer to M, R, or SL 50mm Summicron families. Choose a mount to refine.",
        )

    if norm in FOCAL_LUX_STRONG:
        focal = FOCAL_LUX_STRONG[norm]
        return _hints(
            needs_disambiguation=False,
            ambiguity_type="focal_short_alias",
            recommended_ui_pattern="no_disambiguation_needed",
            recommended_chips=[f"M {focal.replace('mm', '')} Summilux", focal, "ASPH", f"Show all {focal}"],
            suggested_filters={
                "category": ["Lens"],
                "mount": ["M"],
                "focal_length": [focal],
                "family": ["Summilux-M"],
            },
            hard_pin_allowed=True,
            recommended_message="This shorthand is treated as a useful Leica M Summilux query.",
        )

    if norm in FOCAL_LUX_WEAK:
        focal = FOCAL_LUX_WEAK[norm]
        return _hints(
            needs_disambiguation=True,
            ambiguity_type="focal_short_alias",
            recommended_ui_pattern="refinement_chips",
            recommended_chips=[f"M {focal.replace('mm', '')} Summilux", focal, "ASPH", f"Show all {focal}"],
            suggested_filters={
                "category": ["Lens"],
                "mount": ["M"],
                "focal_length": [focal],
                "family": ["Summilux-M"],
            },
            hard_pin_allowed=False,
            recommended_message="This looks like Leica M Summilux shorthand, but you can refine by focal length or variant.",
        )

    if norm in BROAD_R_QUERIES:
        return _hints(
            needs_disambiguation=True,
            ambiguity_type="broad_mount_alias",
            recommended_ui_pattern="family_selector",
            recommended_chips=["Summicron-R", "Elmarit-R", "APO-Telyt-R", "Vario-Elmarit-R", "28mm", "50mm", "90mm", "180mm", "28-90mm"],
            suggested_filters={
                "category": ["Lens"],
                "mount": ["R"],
                "family": ["Summicron-R", "Elmarit-R", "APO-Telyt-R", "Vario-Elmarit-R", "Summilux-R"],
                "focal_length": ["28mm", "35mm", "50mm", "80mm", "90mm", "135mm", "180mm", "28-90mm"],
            },
            hard_pin_allowed=False,
            recommended_message="This is a broad Leica R query. Refine by R family or focal length.",
        )

    if norm in BROAD_ACCESSORY_QUERIES:
        return _hints(
            needs_disambiguation=True,
            ambiguity_type="broad_accessory_alias",
            recommended_ui_pattern="accessory_subtype_selector",
            recommended_chips=["Battery", "Cap", "Lens Cap", "Body Cap", "Filter", "Finder", "Hood", "Adapter", "M", "R", "SL", "Q"],
            suggested_filters={
                "category": ["Accessory"],
                "accessory_type": ["Battery", "Cap", "Lens Cap", "Body Cap", "Filter", "Finder", "Hood", "Adapter", "Strap"],
                "mount_or_system": ["M", "R", "SL", "Q"],
            },
            hard_pin_allowed=False,
            recommended_message="This is a broad accessory query. Refine by accessory type or compatible system.",
        )

    if (norm in SOURCE_COVERAGE_GAP_QUERIES or _is_sigma_14_24_source_gap_alias(query, result_count)) and result_count == 0:
        return _hints(
            needs_disambiguation=False,
            ambiguity_type="source_coverage_gap",
            recommended_ui_pattern="no_result_alert_signup",
            recommended_chips=["Sigma L mount", "Sigma 14-24", "L mount wide zoom", "Alert me"],
            suggested_filters={
                "brand": ["3rd Party", "Sigma"],
                "mount": ["L", "SL"],
                "focal_range": ["14-24mm"],
            },
            hard_pin_allowed=False,
            recommended_message="No matching listing is currently available. Create an alert to be notified when this item appears.",
        )

    if norm in SPECIFIC_GUARDRAIL_QUERIES:
        return _hints(
            needs_disambiguation=False,
            ambiguity_type="none",
            recommended_ui_pattern="no_disambiguation_needed",
            recommended_chips=[],
            suggested_filters={},
            hard_pin_allowed=True,
            recommended_message="",
        )

    return _default_hints()
