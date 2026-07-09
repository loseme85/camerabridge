from __future__ import annotations

import json
import re
from functools import lru_cache
from pathlib import Path
from typing import Any, Mapping


PROJECT_ROOT = Path(__file__).resolve().parent
DEFAULT_ENTRY_GENERATION_REGISTRY_PATH = PROJECT_ROOT / "data/config/entry_generation_registry_v1.json"

SPECIAL_EDITION_TOKENS = (
    "millennium",
    "limited",
    "dragon",
    "lhsa",
    "kanto",
    "custom",
    "safari",
    "reporter",
    "daniel craig",
    "greg williams",
    "special package",
    "edition",
    "asc 100",
    "wetzlar",
    "olive green",
)

ACCESSORY_TITLE_TOKENS = (
    " hood",
    " adapter",
    " grip",
    " handgrip",
    " thumb",
    " case",
    " half case",
    " half-case",
    " holster",
    " protector",
    " strap",
    " filter",
    " cap",
    " battery",
    " charger",
    " meter",
    " plate",
    " cover",
    " 홀스터",
    " 하프케이스",
    " 하프 케이스",
    " 케이스",
    " 스트랩",
    " 그립",
    " 핸드그립",
    " 썸그립",
    " 썸 서포트",
    " 보호필름",
    " 프로텍터",
    " 충전기",
    " 배터리",
    " 캡",
    " 후드",
    " 어댑터",
)


def _normalize_text(value: Any) -> str:
    text = str(value or "").lower()
    text = text.replace("㎜", "mm").replace("ｍｍ", "mm")
    text = re.sub(r"[^a-z0-9가-힣.+/-]+", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def _as_list(value: Any) -> list[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


@lru_cache(maxsize=1)
def load_entry_generation_registry(
    path: str | Path = DEFAULT_ENTRY_GENERATION_REGISTRY_PATH,
) -> dict[str, Any]:
    with Path(path).open(encoding="utf-8") as f:
        return json.load(f)


def _entry_group_map() -> dict[str, dict[str, Any]]:
    registry = load_entry_generation_registry()
    return {group["group_key"]: group for group in registry.get("groups") or [] if isinstance(group, dict)}


def _title_and_context(record_or_final: Mapping[str, Any]) -> tuple[str, dict[str, Any]]:
    if isinstance(record_or_final.get("final_output"), dict):
        final = dict(record_or_final.get("final_output") or {})
        title = str(record_or_final.get("title") or final.get("title_raw") or "")
    else:
        final = dict(record_or_final)
        title = str(final.get("title_raw") or "")
    return _normalize_text(title), final


def _family_from_final(final: Mapping[str, Any]) -> str | None:
    label = str(final.get("label") or "").strip()
    model = str(final.get("model_canonical") or final.get("model_raw") or "").strip()
    category = str(final.get("category") or "").strip()
    if label:
        return label
    if category == "Body" and model:
        if model.startswith("Q"):
            return "Q Body"
        return "M Body" if str(final.get("mount") or "").strip() == "M" else "Body"
    return model or None


def _has_any(text: str, patterns: tuple[str, ...] | list[str]) -> bool:
    return any(pattern in text for pattern in patterns)


def _special_edition(text: str) -> str | None:
    for token in SPECIAL_EDITION_TOKENS:
        if token in text:
            return token
    return None


def _accessory_entry(final: Mapping[str, Any], text: str) -> dict[str, Any] | None:
    if not _has_any(text, ACCESSORY_TITLE_TOKENS):
        return None
    base_model = str(final.get("model_canonical") or final.get("model_raw") or "").strip()
    display_label = f"Leica {base_model} accessory".strip() if base_model else "Leica accessory"
    return {
        "brand": str(final.get("brand") or "Leica"),
        "category": "Accessory",
        "family": _family_from_final(final),
        "base_model": base_model or None,
        "generation": None,
        "version": None,
        "variant": [str(item) for item in _as_list(final.get("variant")) if item],
        "edition": None,
        "optical_version": None,
        "body_generation": None,
        "price_entry_key": None,
        "display_entry_label": display_label,
        "entry_base_model": base_model or None,
        "entry_generation": None,
        "entry_variant": [str(item) for item in _as_list(final.get("variant")) if item],
        "generation_confidence": 0.82,
        "generation_confidence_reason": "title_accessory_guard",
        "generation_boundary_conflict": True,
        "ordinary_price_eligible": False,
        "exact_generation_price_eligible": False,
        "group_key": None,
        "mount": str(final.get("mount") or ""),
    }


def _body_entry(final: Mapping[str, Any], text: str) -> dict[str, Any] | None:
    category = str(final.get("category") or "")
    if category != "Body":
        return None
    mount = str(final.get("mount") or "")
    model = str(final.get("model_canonical") or final.get("model_raw") or "")
    family = _family_from_final(final)
    special = _special_edition(text)
    variants = [str(item) for item in _as_list(final.get("variant")) if item]

    def _payload(
        *,
        base_model: str,
        generation: str,
        key: str,
        group_key: str,
        ordinary: bool = True,
        edition: str | None = None,
    ) -> dict[str, Any]:
        return {
            "brand": str(final.get("brand") or "Leica"),
            "category": "Body",
            "family": family or "Body",
            "base_model": base_model,
            "generation": generation,
            "version": None,
            "variant": variants,
            "edition": edition,
            "optical_version": None,
            "body_generation": generation,
            "price_entry_key": key,
            "display_entry_label": generation,
            "entry_base_model": base_model,
            "entry_generation": generation,
            "entry_variant": variants,
            "generation_confidence": 0.92 if ordinary else 0.82,
            "generation_confidence_reason": "title_generation_rule",
            "generation_boundary_conflict": False,
            "ordinary_price_eligible": ordinary and edition is None,
            "exact_generation_price_eligible": ordinary,
            "group_key": group_key,
            "mount": mount,
        }

    if "m6" in text:
        if "re issue" in text or "re-issue" in text or "reissue" in text or "복각" in text:
            return _payload(base_model="M6", generation="Leica M6 Reissue", key="leica:m_body:m6:reissue", group_key="leica:m_body:m6")
        if "ttl" in text:
            limited = special or ("limited" if _has_any(text, ("titan", "titanium", "the last 999")) else None)
            return _payload(
                base_model="M6",
                generation="Leica M6 Millennium / Limited" if limited else "Leica M6 TTL",
                key="leica:m_body:m6:limited" if limited else "leica:m_body:m6:ttl",
                group_key="leica:m_body:m6",
                ordinary=not limited,
                edition=limited,
            )
        limited = special or ("limited" if _has_any(text, ("titan", "titanium")) else None)
        return _payload(
            base_model="M6",
            generation="Leica M6 Millennium / Limited" if limited else "Leica M6 Classic",
            key="leica:m_body:m6:limited" if limited else "leica:m_body:m6:classic",
            group_key="leica:m_body:m6",
            ordinary=not limited,
            edition=limited,
        )

    if "m10 monochrom" in text:
        edition = special
        return _payload(
            base_model="M10",
            generation="Leica M10 Monochrom",
            key="leica:m_body:m10:monochrom",
            group_key="leica:m_body:m10",
            ordinary=edition is None,
            edition=edition,
        )
    if "m10-p" in text or "m10 p" in text or re.search(r"\bm10p\b", text):
        edition = special
        return _payload(
            base_model="M10",
            generation="Leica M10-P",
            key="leica:m_body:m10:p",
            group_key="leica:m_body:m10",
            ordinary=edition is None,
            edition=edition,
        )
    if "m10-r" in text or "m10 r" in text or re.search(r"\bm10r\b", text):
        return _payload(base_model="M10", generation="Leica M10-R", key="leica:m_body:m10:r", group_key="leica:m_body:m10")
    if model == "M10" or "m10" in text:
        return _payload(base_model="M10", generation="Leica M10", key="leica:m_body:m10:base", group_key="leica:m_body:m10")

    if "m11 monochrom" in text:
        return _payload(base_model="M11", generation="Leica M11 Monochrom", key="leica:m_body:m11:monochrom", group_key="leica:m_body:m11")
    if "m11-p safari" in text:
        return _payload(base_model="M11", generation="Leica M11-P", key="leica:m_body:m11:p", group_key="leica:m_body:m11", ordinary=False, edition="safari")
    if "m11-p" in text or "m11 p" in text or re.search(r"\bm11p\b", text):
        return _payload(base_model="M11", generation="Leica M11-P", key="leica:m_body:m11:p", group_key="leica:m_body:m11")
    if "m11-d" in text or "m11 d" in text or re.search(r"\bm11d\b", text):
        return _payload(base_model="M11", generation="Leica M11-D", key="leica:m_body:m11:d", group_key="leica:m_body:m11")
    if model == "M11" or "m11" in text:
        return _payload(base_model="M11", generation="Leica M11", key="leica:m_body:m11:base", group_key="leica:m_body:m11")

    if "q2 monochrom" in text or "q2 monochrome" in text:
        return _payload(base_model="Q2", generation="Leica Q2 Monochrom", key="leica:q_body:q2:monochrom", group_key="leica:q_body:q2")
    if "q2" in text:
        edition = special if special in {"reporter", "daniel craig", "greg williams", "special package", "edition"} else None
        return _payload(
            base_model="Q2",
            generation="Leica Q2",
            key="leica:q_body:q2:base",
            group_key="leica:q_body:q2",
            ordinary=edition is None,
            edition=edition,
        )

    if "q3 43" in text:
        return _payload(base_model="Q3", generation="Leica Q3 43", key="leica:q_body:q3:43", group_key="leica:q_body:q3")
    if "q3" in text:
        return _payload(base_model="Q3", generation="Leica Q3", key="leica:q_body:q3:base", group_key="leica:q_body:q3")

    return None


def _lens_entry(final: Mapping[str, Any], text: str) -> dict[str, Any] | None:
    category = str(final.get("category") or "")
    if category != "Lens":
        return None
    brand = str(final.get("brand") or "Leica")
    mount = str(final.get("mount") or "")
    family = str(final.get("model_canonical") or final.get("model_raw") or "")
    focal = str(final.get("focal_length") or "")
    variants = [str(item) for item in _as_list(final.get("variant")) if item]

    def _payload(
        *,
        family_label: str,
        base_model: str,
        generation: str,
        key: str,
        group_key: str,
        optical_version: str | None = None,
        ordinary: bool = True,
        edition: str | None = None,
    ) -> dict[str, Any]:
        return {
            "brand": brand,
            "category": "Lens",
            "family": family_label,
            "base_model": base_model,
            "generation": generation,
            "version": generation,
            "variant": variants,
            "edition": edition,
            "optical_version": optical_version,
            "body_generation": None,
            "price_entry_key": key,
            "display_entry_label": generation,
            "entry_base_model": base_model,
            "entry_generation": generation,
            "entry_variant": variants,
            "generation_confidence": 0.91 if ordinary else 0.8,
            "generation_confidence_reason": "title_generation_rule",
            "generation_boundary_conflict": False,
            "ordinary_price_eligible": ordinary and edition is None,
            "exact_generation_price_eligible": ordinary,
            "group_key": group_key,
            "mount": mount,
        }

    if family in {"Summicron-M", "Summicron"} and focal == "50" and mount in {"M", "L", "Unknown", ""}:
        if "apo" in text:
            return _payload(family_label="Summicron-M", base_model="50mm Summicron-M", generation="Leica 50mm APO-Summicron-M", key="leica:m_lens:50_apo_summicron_m:base", group_key="leica:m_lens:50_summicron_m", optical_version="APO")
        if "rigid" in text:
            return _payload(family_label="Summicron-M", base_model="50mm Summicron-M", generation="Leica 50mm Summicron-M Rigid", key="leica:m_lens:50_summicron_m:rigid", group_key="leica:m_lens:50_summicron_m")
        if "dual range" in text or "dual-range" in text or re.search(r"\bdr\b", text):
            return _payload(family_label="Summicron-M", base_model="50mm Summicron-M", generation="Leica 50mm Summicron-M Dual Range", key="leica:m_lens:50_summicron_m:dual_range", group_key="leica:m_lens:50_summicron_m")
        if "type iv" in text or "version iv" in text or "kob" in text or "king of bokeh" in text:
            return _payload(family_label="Summicron-M", base_model="50mm Summicron-M", generation="Leica 50mm Summicron-M Type IV", key="leica:m_lens:50_summicron_m:type_iv", group_key="leica:m_lens:50_summicron_m")
        if "type v" in text or "version v" in text:
            return _payload(family_label="Summicron-M", base_model="50mm Summicron-M", generation="Leica 50mm Summicron-M Version V", key="leica:m_lens:50_summicron_m:version_v", group_key="leica:m_lens:50_summicron_m")

    if family in {"Summicron-M", "Summicron"} and focal == "35" and mount in {"M", "Unknown", ""}:
        if "8-element" in text or "8 element" in text or "8매" in text:
            return _payload(family_label="Summicron-M", base_model="35mm Summicron-M", generation="Leica 35mm Summicron-M 8-element", key="leica:m_lens:35_summicron_m:8_element", group_key="leica:m_lens:35_summicron_m")
        if "asph ii" in text or "asph 2" in text or "version ii" in text:
            return _payload(family_label="Summicron-M", base_model="35mm Summicron-M", generation="Leica 35mm Summicron-M ASPH II", key="leica:m_lens:35_summicron_m:asph_ii", group_key="leica:m_lens:35_summicron_m")
        if "pre-asph" in text or "pre asph" in text or "kob" in text:
            return _payload(family_label="Summicron-M", base_model="35mm Summicron-M", generation="Leica 35mm Summicron-M pre-ASPH", key="leica:m_lens:35_summicron_m:pre_asph", group_key="leica:m_lens:35_summicron_m")
        if "asph" in text:
            return _payload(family_label="Summicron-M", base_model="35mm Summicron-M", generation="Leica 35mm Summicron-M ASPH", key="leica:m_lens:35_summicron_m:asph", group_key="leica:m_lens:35_summicron_m")

    if family in {"Summilux-M", "Summilux"} and focal == "35" and mount in {"M", "Unknown", ""}:
        if "fle" in text:
            return _payload(family_label="Summilux-M", base_model="35mm Summilux-M", generation="Leica 35mm Summilux-M FLE", key="leica:m_lens:35_summilux_m:fle", group_key="leica:m_lens:35_summilux_m")
        if "asph" in text:
            return _payload(family_label="Summilux-M", base_model="35mm Summilux-M", generation="Leica 35mm Summilux-M ASPH", key="leica:m_lens:35_summilux_m:asph", group_key="leica:m_lens:35_summilux_m")
        return _payload(family_label="Summilux-M", base_model="35mm Summilux-M", generation="Leica 35mm Summilux-M pre-ASPH", key="leica:m_lens:35_summilux_m:pre_asph", group_key="leica:m_lens:35_summilux_m")

    if family == "Noctilux" and focal == "50" and mount in {"M", "Unknown", ""}:
        if "0.95" in text:
            return _payload(family_label="Noctilux-M", base_model="50mm Noctilux-M", generation="Leica 50mm Noctilux-M 0.95", key="leica:m_lens:50_noctilux_m:095", group_key="leica:m_lens:50_noctilux_m", optical_version="0.95")
        if "1.2" in text and ("reissue" in text or "복각" in text):
            return _payload(family_label="Noctilux-M", base_model="50mm Noctilux-M", generation="Leica 50mm Noctilux-M 1.2 reissue", key="leica:m_lens:50_noctilux_m:12_reissue", group_key="leica:m_lens:50_noctilux_m", optical_version="1.2")
        if "e60" in text or "3세대" in text or "4세대" in text:
            return _payload(family_label="Noctilux-M", base_model="50mm Noctilux-M", generation="Leica 50mm Noctilux-M 1.0 E60", key="leica:m_lens:50_noctilux_m:e60", group_key="leica:m_lens:50_noctilux_m", optical_version="1.0 E60")
        if "e58" in text or "2세대" in text:
            return _payload(family_label="Noctilux-M", base_model="50mm Noctilux-M", generation="Leica 50mm Noctilux-M 1.0 E58", key="leica:m_lens:50_noctilux_m:e58", group_key="leica:m_lens:50_noctilux_m", optical_version="1.0 E58")

    return None


def classify_entry(record_or_final: Mapping[str, Any]) -> dict[str, Any]:
    text, final = _title_and_context(record_or_final)
    base = {
        "brand": str(final.get("brand") or "Leica"),
        "category": str(final.get("category") or ""),
        "family": _family_from_final(final),
        "base_model": str(final.get("model_canonical") or final.get("model_raw") or "") or None,
        "generation": None,
        "version": None,
        "variant": [str(item) for item in _as_list(final.get("variant")) if item],
        "edition": None,
        "optical_version": None,
        "body_generation": None,
        "price_entry_key": None,
        "display_entry_label": str(final.get("model_canonical") or final.get("model_raw") or "") or None,
        "entry_base_model": str(final.get("model_canonical") or final.get("model_raw") or "") or None,
        "entry_generation": None,
        "entry_variant": [str(item) for item in _as_list(final.get("variant")) if item],
        "generation_confidence": 0.3,
        "generation_confidence_reason": "no_generation_rule",
        "generation_boundary_conflict": False,
        "ordinary_price_eligible": str(final.get("category") or "") in {"Body", "Lens"},
        "exact_generation_price_eligible": False,
        "group_key": None,
        "mount": str(final.get("mount") or ""),
    }
    entry = _accessory_entry(final, text) or _body_entry(final, text) or _lens_entry(final, text)
    if not entry:
        return base
    return entry


def classify_query_entry(query: str, intent: Mapping[str, Any]) -> dict[str, Any]:
    synthetic = {
        "title_raw": query,
        "brand": str(intent.get("brand") or "Leica"),
        "mount": str(intent.get("mount") or ""),
        "category": "Body" if intent.get("body_intent") else ("Accessory" if intent.get("accessory_intent") else "Lens"),
        "label": "M Body" if intent.get("body_intent") and str(intent.get("mount") or "") == "M" else (str(intent.get("model_family") or "") or None),
        "model_raw": intent.get("body_intent") or intent.get("model_family"),
        "model_canonical": intent.get("body_intent") or intent.get("model_family"),
        "variant": list(intent.get("variant") or []),
        "focal_length": intent.get("focal_length"),
        "accessory_type": intent.get("accessory_intent"),
    }
    entry = classify_entry(synthetic)
    query_text = _normalize_text(query)
    if intent.get("accessory_intent"):
        entry["query_kind"] = "accessory"
        entry["is_generation_specific"] = False
        entry["is_broad_parent_query"] = False
        return entry

    body_intent = str(intent.get("body_intent") or "")
    explicit_generation = str(intent.get("generation") or "").strip()
    body_parent_groups = {
        "M6": "leica:m_body:m6",
        "M10": "leica:m_body:m10",
        "M11": "leica:m_body:m11",
        "Q2": "leica:q_body:q2",
        "Q3": "leica:q_body:q3",
    }
    if body_intent in body_parent_groups and not explicit_generation:
        entry["base_model"] = body_intent
        entry["entry_base_model"] = body_intent
        entry["generation"] = None
        entry["entry_generation"] = None
        entry["price_entry_key"] = None
        entry["display_entry_label"] = f"Leica {body_intent}"
        entry["query_kind"] = "broad_parent"
        entry["is_generation_specific"] = False
        entry["is_broad_parent_query"] = True
        entry["group_key"] = body_parent_groups[body_intent]
        entry["exact_generation_price_eligible"] = False
        return entry

    group = _entry_group_map().get(str(entry.get("group_key") or ""))
    has_price_key = bool(entry.get("price_entry_key"))
    if entry.get("category") == "Body" and body_intent and not has_price_key:
        if body_intent in body_parent_groups:
            entry["base_model"] = body_intent
            entry["entry_base_model"] = body_intent
            entry["display_entry_label"] = f"Leica {body_intent}"
            entry["query_kind"] = "broad_parent"
            entry["is_generation_specific"] = False
            entry["is_broad_parent_query"] = True
            entry["group_key"] = body_parent_groups.get(body_intent)
            return entry

    if entry.get("category") == "Lens" and not has_price_key:
        family = str(intent.get("model_family") or "")
        focal = str(intent.get("focal_length") or "")
        mount = str(intent.get("mount") or "")
        if family == "Summicron" and focal == "50" and mount == "M":
            entry["base_model"] = "50mm Summicron-M"
            entry["entry_base_model"] = "50mm Summicron-M"
            entry["display_entry_label"] = "Leica 50mm Summicron-M"
            entry["group_key"] = "leica:m_lens:50_summicron_m"
            entry["query_kind"] = "broad_parent"
            entry["is_generation_specific"] = False
            entry["is_broad_parent_query"] = True
            return entry

    if (
        entry.get("category") == "Lens"
        and str(intent.get("generation") or "") == "Dual Range"
        and str(intent.get("focal_length") or "") == "50"
    ):
        entry.update({
            "family": "Summicron-M",
            "base_model": "50mm Summicron-M",
            "entry_base_model": "50mm Summicron-M",
            "generation": "Leica 50mm Summicron-M Dual Range",
            "entry_generation": "Leica 50mm Summicron-M Dual Range",
            "price_entry_key": "leica:m_lens:50_summicron_m:dual_range",
            "display_entry_label": "Leica 50mm Summicron-M Dual Range",
            "group_key": "leica:m_lens:50_summicron_m",
            "query_kind": "exact_generation",
            "is_generation_specific": True,
            "is_broad_parent_query": False,
        })
        return entry

    entry["query_kind"] = "exact_generation" if has_price_key else ("broad_parent" if group else "unstructured")
    entry["is_generation_specific"] = has_price_key
    entry["is_broad_parent_query"] = bool(group and not has_price_key)
    if not entry.get("display_entry_label") and entry.get("base_model"):
        entry["display_entry_label"] = f"Leica {entry['base_model']}"
    if "kob" in query_text and entry.get("price_entry_key") == "leica:m_lens:50_summicron_m:type_iv":
        entry["generation_confidence_reason"] = "kob_alias"
    return entry


def compare_query_to_result(query_entry: Mapping[str, Any], result_entry: Mapping[str, Any]) -> dict[str, Any]:
    query_kind = str(query_entry.get("query_kind") or "")
    query_key = str(query_entry.get("price_entry_key") or "")
    result_key = str(result_entry.get("price_entry_key") or "")
    query_base = str(query_entry.get("entry_base_model") or query_entry.get("base_model") or "")
    result_base = str(result_entry.get("entry_base_model") or result_entry.get("base_model") or "")
    query_group = str(query_entry.get("group_key") or "")
    result_group = str(result_entry.get("group_key") or "")
    query_category = str(query_entry.get("category") or "")
    result_category = str(result_entry.get("category") or "")

    matched_tokens: list[str] = []
    missing_tokens: list[str] = []
    conflicting_tokens: list[str] = []

    if query_key and result_key and query_key == result_key:
        matched_tokens.extend([query_base, str(query_entry.get("generation") or query_entry.get("display_entry_label") or "")])
        return {
            "query_match_level": "exact_generation",
            "query_match_score": 100,
            "query_match_label": "Exact generation match",
            "query_entry_key": query_key,
            "result_entry_key": result_key,
            "matched_tokens": [token for token in matched_tokens if token],
            "missing_tokens": [],
            "conflicting_tokens": [],
        }

    if query_kind == "exact_generation" and query_base and result_base == query_base and query_group and result_group == query_group:
        conflicting_tokens.append(str(result_entry.get("generation") or result_entry.get("display_entry_label") or "different generation"))
        return {
            "query_match_level": "exact_base_model",
            "query_match_score": 82,
            "query_match_label": "Same base model, different generation",
            "query_entry_key": query_key or None,
            "result_entry_key": result_key or None,
            "matched_tokens": [query_base],
            "missing_tokens": [],
            "conflicting_tokens": conflicting_tokens,
        }

    if query_kind == "broad_parent" and query_group and result_group == query_group:
        matched_tokens.append(query_base or str(query_entry.get("display_entry_label") or ""))
        return {
            "query_match_level": "exact_base_model",
            "query_match_score": 88,
            "query_match_label": "Same base model generation candidate",
            "query_entry_key": None,
            "result_entry_key": result_key or None,
            "matched_tokens": [token for token in matched_tokens if token],
            "missing_tokens": [],
            "conflicting_tokens": [],
        }

    if query_category == "Accessory" and result_category == "Accessory":
        return {
            "query_match_level": "accessory_compatible",
            "query_match_score": 52,
            "query_match_label": "Accessory / compatible item",
            "query_entry_key": query_key or None,
            "result_entry_key": result_key or None,
            "matched_tokens": [],
            "missing_tokens": [],
            "conflicting_tokens": [],
        }

    if query_category == result_category and query_group and result_group and query_group.split(":")[0:3] == result_group.split(":")[0:3]:
        return {
            "query_match_level": "same_family_reference",
            "query_match_score": 64,
            "query_match_label": "Reference only — same family",
            "query_entry_key": query_key or None,
            "result_entry_key": result_key or None,
            "matched_tokens": [],
            "missing_tokens": [],
            "conflicting_tokens": [],
        }

    if query_category and result_category and query_category != result_category:
        conflicting_tokens.append(result_category)
        return {
            "query_match_level": "boundary_conflict",
            "query_match_score": 24,
            "query_match_label": "Not used for price — boundary conflict",
            "query_entry_key": query_key or None,
            "result_entry_key": result_key or None,
            "matched_tokens": [],
            "missing_tokens": [],
            "conflicting_tokens": conflicting_tokens,
        }

    return {
        "query_match_level": "unknown",
        "query_match_score": 18,
        "query_match_label": "Reference only — broad brand match",
        "query_entry_key": query_key or None,
        "result_entry_key": result_key or None,
        "matched_tokens": [],
        "missing_tokens": missing_tokens,
        "conflicting_tokens": conflicting_tokens,
    }


def suggested_generation_labels(
    query_entry: Mapping[str, Any],
    result_entries: list[Mapping[str, Any]],
    limit: int = 4,
) -> list[str]:
    labels: list[str] = []
    seen: set[str] = set()
    query_group = str(query_entry.get("group_key") or "")
    for entry in result_entries:
        if query_group and str(entry.get("group_key") or "") != query_group:
            continue
        label = str(entry.get("display_entry_label") or "").strip()
        if not label or label in seen:
            continue
        labels.append(label)
        seen.add(label)
        if len(labels) >= limit:
            return labels
    if query_group:
        group = _entry_group_map().get(query_group) or {}
        for label in group.get("broad_query_labels") or []:
            if label not in seen:
                labels.append(label)
                seen.add(label)
            if len(labels) >= limit:
                break
    return labels
