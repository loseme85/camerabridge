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
    q = re.sub(r"\bpre\s+asph\b", "pre-asph", q)
    q = re.sub(r"\b8(?:\s*-\s*|\s+)elements?\b", "8-element", q)
    q = re.sub(r"\btri\s+elmar\b", "tri-elmar", q)
    q = re.sub(r"(?<=\d)\s*mm\b", "mm", q)
    q = re.sub(r"\s+", " ", q)
    return q


def _add_variant(intent: QueryIntent, value: str, source: str) -> None:
    if value not in intent.variant:
        intent.variant.append(value)
    intent.tokens.append({"type": "variant", "raw": source, "value": value})


def _remove_variant(intent: QueryIntent, value: str) -> None:
    intent.variant = [variant for variant in intent.variant if variant != value]
    intent.tokens = [
        token
        for token in intent.tokens
        if not (token.get("type") == "variant" and token.get("value") == value)
    ]


def _set_accessory_intent(intent: QueryIntent, value: str, source: str) -> None:
    intent.accessory_intent = value
    if not any(token.get("type") == "accessory_intent" and token.get("value") == value for token in intent.tokens):
        intent.tokens.append({"type": "accessory_intent", "raw": source, "value": value})


def _set_accessory_code(intent: QueryIntent, value: str, source: str) -> None:
    intent.accessory_code = value.upper()
    intent.tokens.append({"type": "accessory_code", "raw": source, "value": intent.accessory_code})


_BODY_INTENT_ALIASES = {
    "m2": ("M2", "M", None, ()),
    "m3": ("M3", "M", None, ()),
    "m4": ("M4", "M", None, ()),
    "m5": ("M5", "M", None, ()),
    "m6": ("M6", "M", None, ()),
    "m9": ("M9", "M", None, ()),
    "m9-p": ("M9-P", "M", None, ("P",)),
    "m10": ("M10", "M", None, ()),
    "m10-r": ("M10-R", "M", None, ("R",)),
    "m11": ("M11", "M", None, ()),
    "mp": ("MP", "M", None, ()),
    "q2": ("Q2", None, "Q", ()),
    "q3": ("Q3", None, "Q", ()),
    "sl2": ("SL2", "SL", None, ()),
    "r6": ("R6", "R", None, ()),
    "r7": ("R7", "R", None, ()),
    "r8": ("R8", "R", None, ()),
    "barnack": ("Barnack", "L", None, ()),
    "iiic": ("IIIc", "L", None, ()),
    "iiif": ("IIIf", "L", None, ()),
    "iiig": ("IIIg", "L", None, ()),
}


_COMPACT_BODY_PATTERNS: tuple[tuple[str, str], ...] = (
    (r"\bd\s*-\s*lux\s*([0-9]{1,3})?\b|\bd\s+lux\s*([0-9]{1,3})?\b|\bdlux\s*([0-9]{1,3})?\b", "D-LUX"),
    (r"\bv\s*-\s*lux\s*([0-9]{1,3})?\b|\bv\s+lux\s*([0-9]{1,3})?\b|\bvlux\s*([0-9]{1,3})?\b", "V-LUX"),
    (r"\bc\s*-\s*lux\s*([0-9]{1,3})?\b|\bc\s+lux\s*([0-9]{1,3})?\b|\bclux\s*([0-9]{1,3})?\b", "C-LUX"),
    (r"\bsofort\s*([0-9]{1,2})?\b", "Sofort"),
)

_BODY_QUERY_ACCESSORY_BLOCKERS = {
    "battery", "handgrip", "grip", "case", "plate", "strap", "hood",
    "cap", "cover", "adapter", "filter", "finder", "charger", "thumb",
    "protector", "holster", "pouch", "door", "thumbs", "support",
}

_BODY_QUERY_LENS_BLOCKERS = {
    "summicron", "summilux", "noctilux", "elmarit", "elmar", "summarit",
    "summaron", "telyt", "vario", "apo",
}

_COMPACT_LENS_MOUNT_ALIASES = {
    "m": "M",
    "r": "R",
    "sl": "SL",
    "l": "L",
}


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


def _parse_explicit_body_model_intent(intent: QueryIntent, normalized: str) -> None:
    """
    Narrow body-query recovery for common user queries that should clearly
    resolve to camera bodies instead of broad Leica lens fallbacks.

    Keep this strict:
    - allow `leica sl2`, `sl2`, `leica sl3`, `sl3` only when no accessory/lens
      blocker tokens are present
    - allow `m10` only when the query also says `body`
    """
    tokens = set(re.findall(r"[a-z0-9가-힣./-]+", normalized))
    if tokens & _BODY_QUERY_LENS_BLOCKERS:
        return

    if tokens & _BODY_QUERY_ACCESSORY_BLOCKERS and "body" not in tokens:
        return

    explicit_patterns = (
        (r"\bleica\s+sl2\b|\bsl2\b", "SL2", "SL", None),
        (r"\bleica\s+sl3\b|\bsl3\b", "SL3", "SL", None),
    )
    for pattern, body_intent, mount, system in explicit_patterns:
        if re.search(pattern, normalized):
            _set_body_intent(intent, body_intent, body_intent.lower(), mount=mount, system=system)
            return

    if re.search(r"\b(?:leica\s+)?m\s+(?:body|camera)(?:\s+body)?\b", normalized):
        _set_body_intent(intent, "M", "m body", mount="M", system=None)
        return

    if re.search(r"\bm10\b", normalized) and re.search(r"\bbody\b", normalized):
        _set_body_intent(intent, "M10", "m10 body", mount="M", system=None)


def _set_compact_lens_notation(
    intent: QueryIntent,
    mount: str,
    focal: str,
    aperture: str,
    source: str,
) -> None:
    if not intent.mount:
        intent.mount = mount
        intent.tokens.append({"type": "mount", "raw": source, "value": mount})
    if not intent.focal_length:
        intent.focal_length = focal
        intent.tokens.append({"type": "focal_length", "raw": source, "value": focal})
    if not intent.aperture:
        _set_aperture(intent, aperture, source, token_type="aperture_hint")
    intent.tokens.append({"type": "compact_lens_notation", "raw": source, "value": f"{mount} {focal}/{aperture}"})


def _parse_compact_mount_lens_notation(intent: QueryIntent, normalized: str) -> None:
    if intent.accessory_intent or intent.body_intent:
        return

    match = re.search(
        r"\b(sl|m|r|l)\s*(\d{2,3})(?:mm)?\s*(?:/\s*|f/?\s*)(\d+(?:\.\d+)?)\b",
        normalized,
    )
    if not match:
        return

    mount_raw, focal, aperture = match.groups()
    mount = _COMPACT_LENS_MOUNT_ALIASES.get(mount_raw)
    if not mount:
        return

    _set_compact_lens_notation(intent, mount, focal, aperture, match.group(0))


def _parse_accessory_compatibility_context(intent: QueryIntent, normalized: str) -> None:
    """
    Narrow query-side compatibility hint for accessory searches that mention a
    specific body line, without turning them into body queries.

    Current scope is intentionally small:
    - `sl2` / `sl3` accessory queries imply SL compatibility
    """
    if not intent.accessory_intent or intent.mount:
        return

    if re.search(r"\bsl2\b|\bsl3\b", normalized):
        intent.mount = "SL"
        intent.tokens.append({"type": "mount", "raw": "sl accessory compatibility", "value": "SL"})


def _parse_summilux_35_steel_rim_reissue_hints(intent: QueryIntent, normalized: str) -> None:
    if intent.accessory_intent or intent.body_intent:
        return

    strong_summilux_35_context = bool(
        ("summilux" in normalized or re.search(r"\blux\b", normalized))
        and (re.search(r"\b35(?:mm)?\b", normalized) or re.search(r"\bm35\b", normalized))
    )
    if not strong_summilux_35_context:
        return

    if re.search(r"\bsteel\s+rim\b|\bsteel-rim\b|스틸림", normalized):
        _add_variant(intent, "Steel Rim", "steel rim")

    if re.search(r"\breissue\b|복각", normalized):
        _add_variant(intent, "Reissue", "reissue")


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


_SL_ZOOM_RANGE_PATTERNS: tuple[tuple[str, str], ...] = (
    (r"\b24[\s/-]?90\b", "24-90"),
    (r"\b14[\s/-]?24\b", "14-24"),
    (r"\b16[\s/-]?35\b", "16-35"),
    (r"\b90[\s/-]?280\b", "90-280"),
)

_THIRD_PARTY_L_MOUNT_RANGE_PATTERNS: tuple[tuple[str, str], ...] = (
    (r"\b24[\s/-]?70\b", "24-70"),
    (r"\b14[\s/-]?24\b", "14-24"),
    (r"\b24[\s/-]?105\b", "24-105"),
)

_R_HYPHENATED_FAMILY_ALIASES: dict[str, str] = {
    "summicron-r": "Summicron-R",
    "elmarit-r": "Elmarit-R",
    "apo-telyt-r": "APO-Telyt-R",
    "telyt-r": "Telyt-R",
    "vario-elmarit-r": "Vario-Elmarit-R",
    "vario-apo-elmarit-r": "Vario-APO-Elmarit-R",
}

_LEICA_HYPHENATED_FAMILY_MOUNTS: dict[str, str] = {
    "summicron-m": "M",
    "summilux-m": "M",
    "noctilux-m": "M",
    "elmarit-m": "M",
    "apo-summicron-m": "M",
    "summicron-sl": "SL",
    "apo-summicron-sl": "SL",
}

_TRI_ELMAR_SHORTHANDS: dict[str, tuple[str, str]] = {
    "wate": ("16-18-21", "WATE"),
    "mate": ("28-35-50", "MATE"),
}

_TRI_ELMAR_RANGE_VARIANTS: dict[str, str] = {
    "16-18-21": "WATE",
    "28-35-50": "MATE",
}


def _parse_sl_zoom_range_hint(intent: QueryIntent, normalized: str) -> None:
    """
    Narrow query-side recovery for Leica SL zoom shorthand such as:
    - sl 24-90
    - sl 14-24
    - sl 16-35
    - sl 90-280

    Keep this strict:
    - require explicit SL token
    - skip if accessory intent exists
    - skip if body intent exists
    - only recognize the four known Leica SL zoom ranges in current scope
    """
    if intent.accessory_intent or intent.body_intent:
        return

    if not re.search(r"\bsl\b", normalized):
        return

    if re.search(r"\b(?:summicron|summilux|noctilux|elmarit|elmar|summarit|summaron|telyt|cron|lux)\b", normalized):
        return

    for pattern, focal_range in _SL_ZOOM_RANGE_PATTERNS:
        match = re.search(pattern, normalized)
        if not match:
            continue
        intent.focal_length = focal_range
        intent.tokens.append({"type": "focal_length", "raw": match.group(0), "value": focal_range})
        if not intent.mount:
            intent.mount = "SL"
            intent.tokens.append({"type": "mount", "raw": "sl", "value": "SL"})
        intent.tokens.append({"type": "zoom_range_hint", "raw": match.group(0), "value": focal_range})
        return


def _parse_third_party_l_mount_range_hint(intent: QueryIntent, normalized: str) -> None:
    """
    Narrow query-side recovery for third-party L-mount zoom shorthand such as:
    - sigma 24-70 l
    - sigma 14-24 l
    - panasonic 24-105 l

    Keep this strict:
    - require explicit third-party brand token
    - require exact supported range
    - require L-mount signal for Sigma/Panasonic
    - do not activate for accessory/body/lens-family queries
    """
    if intent.accessory_intent or intent.body_intent or intent.model_family:
        return

    has_sigma_token = bool(re.search(r"\b(?:sigma|시그마)\b", normalized))
    has_panasonic_token = bool(re.search(r"\b(?:panasonic|파나소닉)\b", normalized))
    has_lumix_token = bool(re.search(r"\b(?:lumix|루믹스)\b", normalized))

    brand_token: Optional[str] = None
    if has_sigma_token:
        brand_token = "sigma"
    elif has_panasonic_token and has_lumix_token:
        # Treat the explicit Panasonic+Lumix pairing as a narrow Lumix-S/L-mount
        # shorthand instead of requiring a separate `l` token.
        brand_token = "lumix"
    elif has_panasonic_token:
        brand_token = "panasonic"
    elif has_lumix_token:
        brand_token = "lumix"

    if not brand_token:
        return

    focal_range: Optional[str] = None
    focal_raw: Optional[str] = None
    for pattern, candidate_range in _THIRD_PARTY_L_MOUNT_RANGE_PATTERNS:
        match = re.search(pattern, normalized)
        if match:
            focal_range = candidate_range
            focal_raw = match.group(0)
            break
    if not focal_range or not focal_raw:
        return

    has_l_mount_signal = bool(
        re.search(
            r"\bl\s+mount\b|\bl-mount\b|\bl마운트\b|\bsl\s+mount\b|\bsl마운트\b|\bdg\s+dn\b|\blumix\s+s\b",
            normalized,
        )
    ) or bool(re.search(r"\bl\b", normalized))

    if brand_token in {"sigma", "panasonic"} and not has_l_mount_signal:
        return

    intent.brand = "3rd Party"
    intent.tokens.append({"type": "brand", "raw": brand_token, "value": "3rd Party"})
    intent.focal_length = focal_range
    intent.tokens.append({"type": "focal_length", "raw": focal_raw, "value": focal_range})
    if not intent.mount:
        intent.mount = "SL"
        intent.tokens.append({"type": "mount", "raw": "l-mount intent", "value": "SL"})
    intent.tokens.append({"type": "third_party_l_mount_hint", "raw": f"{brand_token} {focal_raw}", "value": focal_range})


def _set_model_family(intent: QueryIntent, family: str, source: str) -> None:
    intent.model_family = family
    intent.brand = intent.brand or DEFAULT_BRAND
    intent.tokens.append({"type": "model_family", "raw": source, "value": family})


def _set_mount(intent: QueryIntent, mount: str, source: str) -> None:
    if intent.mount == mount:
        return
    intent.mount = mount
    intent.tokens.append({"type": "mount", "raw": source, "value": mount})


def _set_focal_length(intent: QueryIntent, focal: str, source: str) -> None:
    intent.focal_length = focal
    intent.tokens.append({"type": "focal_length", "raw": source, "value": focal})


def _parse_r_lens_query_hint(intent: QueryIntent, normalized: str) -> None:
    """
    Narrow recovery for Leica R lens shorthand that is too compact for the
    generic token parser.

    Keep this strict:
    - require explicit R-side context
    - skip body/accessory queries
    - only recover exact families/ranges already observed in search recall
    """
    if intent.accessory_intent or intent.body_intent:
        return

    has_r_context = bool(
        re.search(
            r"\bleica\s+r\b|\br\b|\b(?:summicron|elmarit|apo-telyt|telyt|vario-elmarit|vario-apo-elmarit)-r\b",
            normalized,
        )
    )
    if not has_r_context:
        return

    if re.search(r"\b(?:adapter|cap|hood|case|finder|battery|strap|filter)\b", normalized):
        return

    if (
        re.search(r"\b180(?:mm)?\b|\b180/3\.4\b", normalized)
        and re.search(r"\bapo\b", normalized)
        and not re.search(r"\b(?:elmarit|summicron|summilux|vario)\b", normalized)
    ):
        _set_model_family(intent, "APO-Telyt-R", "apo telyt r hint")
        _set_mount(intent, "R", "apo telyt r hint")
        if not intent.focal_length:
            _set_focal_length(intent, "180", "180")
        return

    if (
        re.search(r"\b28[\s/-]?90\b", normalized)
        and re.search(r"\bvario(?:-|\s+)elmarit(?:-|\s+)r\b|\br\b.*\bvario\b.*\belmarit\b|\bvario\b.*\belmarit\b.*\br\b", normalized)
    ):
        _set_model_family(intent, "Vario-Elmarit-R", "vario elmarit r hint")
        _set_mount(intent, "R", "vario elmarit r hint")
        _set_focal_length(intent, "28-90", "28-90")


def _parse_optical_formula(intent: QueryIntent, normalized: str) -> None:
    for groups, elements in re.findall(r"(\d+)\s*군\s*(\d+)\s*매", normalized):
        value = f"{groups} groups / {elements} elements"
        intent.optical_formula = value
        intent.tokens.append({"type": "optical_formula", "raw": f"{groups}군{elements}매", "value": value})
        if elements == "8":
            _add_variant(intent, "8-element", f"{groups}군{elements}매")


def _has_summilux_35_context(normalized: str, intent: QueryIntent) -> bool:
    if intent.focal_length != "35":
        return False
    family = str(intent.model_family or "")
    if family in {"Summilux", "Summilux-M"}:
        return True
    return bool(re.search(r"\b(?:summilux|summilux-m|lux)\b", normalized))


def _has_summicron_50_context(normalized: str, intent: QueryIntent) -> bool:
    if intent.focal_length != "50":
        return False
    family = str(intent.model_family or "")
    if family in {"Summicron", "Summicron-M"}:
        return True
    return bool(re.search(r"\b(?:summicron|summicron-m|cron)\b", normalized))


def _apply_context_bound_variant_recovery(intent: QueryIntent, normalized: str) -> None:
    summilux_35_aa_shorthand_match = re.search(r"(?<!\d)2매(?!\d)|\b2(?:\s*-\s*|\s+)mae\b|\b2mae\b", normalized)
    if (
        summilux_35_aa_shorthand_match
        and not intent.model_family
        and re.search(r"\bm35(?:mm)?(?:\s*/\s*|\s+f?\s*|\s+)1\.4\b|\bm\s*35(?:mm)?(?:\s*/\s*|\s+f?\s*|\s+)1\.4\b", normalized)
    ):
        _set_model_family(intent, "Summilux-M", "m35 1.4 2mae shorthand")
        _set_mount(intent, "M", "m35 1.4 2mae shorthand")
        if not intent.focal_length:
            _set_focal_length(intent, "35", "m35 1.4 2mae shorthand")
        if not intent.aperture:
            _set_aperture(intent, "1.4", "m35 1.4 2mae shorthand", token_type="aperture_hint")

    if (
        "aspherical" in normalized
        and _has_summilux_35_context(normalized, intent)
        and "ASPH" in intent.variant
        and "FLE" not in intent.variant
        and "pre-ASPH" not in intent.variant
        and "AA" not in intent.variant
        and "asph" not in re.findall(r"[a-z0-9가-힣./-]+", normalized)
    ):
        intent.variant = [variant for variant in intent.variant if variant != "ASPH"]
        intent.tokens = [
            token
            for token in intent.tokens
            if not (
                token.get("type") == "variant"
                and token.get("raw") == "aspherical"
                and token.get("value") == "ASPH"
            )
        ]
        _add_variant(intent, "AA", "aspherical")

    if _has_summilux_35_context(normalized, intent):
        if (
            summilux_35_aa_shorthand_match
            and "AA" not in intent.variant
            and "ASPH" not in intent.variant
            and "FLE" not in intent.variant
            and "FLE2" not in intent.variant
            and "pre-ASPH" not in intent.variant
        ):
            _add_variant(intent, "AA", summilux_35_aa_shorthand_match.group(0))

        fle2_match = re.search(r"\bfle(?:\s*-\s*|\s+)?(?:ii|2)\b|\bfle2\b|\bclose(?:-|\s+)focus\b", normalized)
        if fle2_match:
            if "FLE" in intent.variant:
                _remove_variant(intent, "FLE")
            if "FLE2" not in intent.variant:
                _add_variant(intent, "FLE2", fle2_match.group(0))
        elif "fle" in normalized and "FLE" not in intent.variant:
            _add_variant(intent, "FLE", "fle")

    if (
        _has_summicron_50_context(normalized, intent)
        and "Dual Range" not in intent.variant
        and re.search(r"\bdr\b|\bdual(?:-|\s*)range\b", normalized)
    ):
        _add_variant(intent, "Dual Range", "dual range")

    tri_elmar_context = bool(re.search(r"\b(?:tri-elmar|trielmar|wate|mate)\b", normalized))
    if not tri_elmar_context:
        return

    if "wate" in normalized:
        if not (
            intent.model_family == "Tri-Elmar"
            and intent.mount == "M"
            and intent.focal_length == "16-18-21"
            and "WATE" in intent.variant
        ):
            _set_model_family(intent, "Tri-Elmar", "wate")
            _set_mount(intent, "M", "wate")
            _set_focal_length(intent, "16-18-21", "wate")
            _add_variant(intent, "WATE", "wate")
        return

    if "mate" in normalized:
        if not (
            intent.model_family == "Tri-Elmar"
            and intent.mount == "M"
            and intent.focal_length == "28-35-50"
            and "MATE" in intent.variant
        ):
            _set_model_family(intent, "Tri-Elmar", "mate")
            _set_mount(intent, "M", "mate")
            _set_focal_length(intent, "28-35-50", "mate")
            _add_variant(intent, "MATE", "mate")
        return

    for pattern, focal_range in (
        (r"\b16(?:[\s/-]+)18(?:[\s/-]+)21\b", "16-18-21"),
        (r"\b28(?:[\s/-]+)35(?:[\s/-]+)50\b", "28-35-50"),
    ):
        match = re.search(pattern, normalized)
        if not match:
            continue
        variant = _TRI_ELMAR_RANGE_VARIANTS[focal_range]
        if (
            intent.model_family == "Tri-Elmar"
            and intent.mount == "M"
            and intent.focal_length == focal_range
            and variant in intent.variant
        ):
            return
        _set_model_family(intent, "Tri-Elmar", "tri-elmar range")
        _set_mount(intent, "M", "tri-elmar range")
        _set_focal_length(intent, focal_range, match.group(0))
        _add_variant(intent, variant, match.group(0))
        return


def _apply_apo_summicron_family_recovery(intent: QueryIntent, normalized: str) -> None:
    if not re.search(r"\bapo\b", normalized):
        return

    family = str(intent.model_family or "")
    mount = str(intent.mount or "")
    if family != "Summicron":
        return

    upgraded_family = None
    if mount == "M":
        upgraded_family = "APO-Summicron-M"
    elif mount == "SL":
        upgraded_family = "APO-Summicron-SL"

    if not upgraded_family:
        return

    intent.model_family = upgraded_family
    intent.brand = intent.brand or DEFAULT_BRAND
    intent.tokens = [
        token
        for token in intent.tokens
        if not (token.get("type") == "unknown" and token.get("raw") == "apo" and token.get("value") == "apo")
    ]
    intent.tokens.append({"type": "model_family", "raw": "apo summicron context", "value": upgraded_family})


def _parse_accessory_intent(intent: QueryIntent, normalized: str) -> None:
    if re.search(r"\blens\s+hood\b", normalized):
        _set_accessory_intent(intent, "hood", "lens hood")
    elif re.search(r"\bhood\b", normalized) or "후드" in normalized:
        _set_accessory_intent(intent, "hood", "hood" if "hood" in normalized else "후드")

    if not intent.accessory_intent:
        if re.search(r"\blens\s+cap\b", normalized):
            _set_accessory_intent(intent, "cap", "lens cap")
        elif re.search(r"\bcap\b", normalized) or "캡" in normalized:
            _set_accessory_intent(intent, "cap", "cap" if "cap" in normalized else "캡")

    if not intent.accessory_intent:
        battery_source: Optional[str] = None
        battery_code_match = re.search(r"\bbp\s*-?\s*scl\s*([0-9]{1,2})\b", normalized)
        if battery_code_match:
            battery_source = battery_code_match.group(0)
        elif re.search(r"\bbatter(?:y|ies)\b", normalized):
            battery_source = "battery"
        elif "배터리" in normalized:
            battery_source = "배터리"

        if battery_source:
            _set_accessory_intent(intent, "battery", battery_source)
            if battery_code_match:
                _set_accessory_code(intent, f"BP-SCL{battery_code_match.group(1)}", battery_source)

    if not intent.accessory_intent:
        strap_source: Optional[str] = None
        if re.search(r"\bhand\s+strap\b", normalized):
            strap_source = "hand strap"
        elif re.search(r"\bneck\s+strap\b", normalized):
            strap_source = "neck strap"
        elif re.search(r"\bshoulder\s+strap\b", normalized):
            strap_source = "shoulder strap"
        elif re.search(r"\bstrap\b", normalized) or "스트랩" in normalized:
            strap_source = "strap" if re.search(r"\bstrap\b", normalized) else "스트랩"

        if strap_source:
            _set_accessory_intent(intent, "strap", strap_source)

    if not intent.accessory_intent:
        misc_accessory_intent: Optional[tuple[str, str]] = None
        if re.search(r"\bhand\s*grip\b|\bhandgrip\b", normalized) or "핸드그립" in normalized:
            misc_accessory_intent = ("grip", "handgrip" if "handgrip" in normalized else ("hand grip" if re.search(r"\bhand\s+grip\b", normalized) else "핸드그립"))
        elif re.search(r"\bgrip\b", normalized):
            misc_accessory_intent = ("grip", "grip")
        elif re.search(r"\bcharger\b", normalized) or "충전기" in normalized:
            misc_accessory_intent = ("charger", "charger" if re.search(r"\bcharger\b", normalized) else "충전기")
        elif re.search(r"\bcase\b", normalized) or "케이스" in normalized:
            misc_accessory_intent = ("case", "case" if re.search(r"\bcase\b", normalized) else "케이스")
        elif re.search(r"\bpouch\b", normalized) or "파우치" in normalized:
            misc_accessory_intent = ("pouch", "pouch" if re.search(r"\bpouch\b", normalized) else "파우치")

        if misc_accessory_intent:
            _set_accessory_intent(intent, misc_accessory_intent[0], misc_accessory_intent[1])

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


def _compact_lens_notation_token_consumed(intent: QueryIntent, token: str) -> bool:
    if not any(item.get("type") == "compact_lens_notation" for item in intent.tokens):
        return False
    if re.fullmatch(r"(?:sl|m|r|l)\d{2,3}(?:mm)?(?:/\d+(?:\.\d+)?)?", token):
        return True
    return False


def _parsed_body_intent_token_consumed(intent: QueryIntent, token: str) -> bool:
    body_intent = _normalize_query(intent.body_intent or "")
    if not body_intent:
        return False
    token_norm = _normalize_query(token)
    return token_norm in {
        body_intent,
        body_intent.replace(" ", ""),
        body_intent.replace(" ", "-"),
        body_intent.replace("-", ""),
    }


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
    _parse_explicit_body_model_intent(intent, normalized)
    _parse_accessory_compatibility_context(intent, normalized)
    _parse_r_lens_query_hint(intent, normalized)
    _parse_sl_zoom_range_hint(intent, normalized)
    _parse_third_party_l_mount_range_hint(intent, normalized)
    _parse_compact_mount_lens_notation(intent, normalized)
    _parse_summilux_35_steel_rim_reissue_hints(intent, normalized)

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

        if _compact_lens_notation_token_consumed(intent, token):
            continue

        if _parsed_body_intent_token_consumed(intent, token):
            continue

        body_alias = _BODY_INTENT_ALIASES.get(token)
        if body_alias and not intent.accessory_intent and not intent.model_family and _body_intent_token_allowed(token, rough_tokens):
            body_intent, body_mount, body_system, body_variants = body_alias
            _set_body_intent(intent, body_intent, token, mount=body_mount, system=body_system)
            for variant in body_variants:
                _add_variant(intent, variant, token)
            continue

        tri_elmar_shorthand = _TRI_ELMAR_SHORTHANDS.get(token)
        if tri_elmar_shorthand:
            focal_range, shorthand = tri_elmar_shorthand
            _set_model_family(intent, "Tri-Elmar", token)
            _set_mount(intent, "M", token)
            _set_focal_length(intent, focal_range, token)
            _add_variant(intent, shorthand, token)
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

        r_family = _R_HYPHENATED_FAMILY_ALIASES.get(token)
        if r_family:
            _set_model_family(intent, r_family, token)
            _set_mount(intent, "R", token)
            continue

        family = MODEL_FAMILY_ALIASES.get(token)
        if family:
            intent.model_family = family
            intent.brand = intent.brand or DEFAULT_BRAND
            intent.tokens.append({"type": "model_family", "raw": token, "value": family})
            hyphen_mount = _LEICA_HYPHENATED_FAMILY_MOUNTS.get(token)
            if hyphen_mount and not intent.mount:
                _set_mount(intent, hyphen_mount, token)
            family_system = MODEL_SYSTEM_ALIASES.get(token)
            if family_system and not intent.system:
                intent.system = family_system
                intent.tokens.append({"type": "system", "raw": token, "value": family_system})
            continue

        variant = VARIANT_ALIASES.get(token)
        if variant:
            if variant == "FLE" and not _has_summilux_35_context(normalized, intent):
                intent.tokens.append({"type": "unknown", "raw": token, "value": token})
                continue
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

    _apply_context_bound_variant_recovery(intent, normalized)
    _apply_apo_summicron_family_recovery(intent, normalized)

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
