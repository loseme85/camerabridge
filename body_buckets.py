"""M 바디 매물의 갈래를 정한다 (2026-11-21 분류 설계 시범, 갈래표는 catalog/buckets.py).

기존 제목 규칙(entity_catalog.match_entities)이 붙인 모델 연결 뒤에 돈다.
  1. 특징 찾기: 리페인트·캐나다·모터·시제품·기념판·고장 (여러 개 가능)
  2. 한 매물이 갈래표의 서로 다른 모델 둘 이상에 붙었으면, 제목에서 먼저 나온 모델 하나만 남김 ('M6A (M7 Prototype)' → M6)
  3. 그 모델 안에서 갈래가 여럿이면 갈래표 우선순위로 하나 (블랙페인트 + 버튼 리와인드 → 블랙페인트)
  4. 고장·부품용이면 entity_note='defect' (그래프·시세에서 빠짐)
가격 검문(특징 없는 스탠다드가 중간값의 2배 넘거나 0.4배 밑 → 확인 필요)은 시세를 알아야 해서
scripts/build_entity_index.py가 review_outliers()로 따로 부른다.
매물마다 final_output.bucket = {"traits": [...], "reason": "..."}를 남겨 왜 그 갈래인지 볼 수 있게 한다.
"""
from __future__ import annotations

import re
import statistics
from typing import Any, Callable

from catalog.buckets import DESC_TRAITS, FAMILIES, GENERIC_FAMILIES, REVIEW_HIGH, REVIEW_LOW, REVIEW_MIN_N, TRAIT_BUCKET, TRAITS, bucket_id

TRAIT_RX = {name: re.compile(rx, re.I) for name, rx in TRAITS.items()}


def traits_of(title: str) -> list[str]:
    return [name for name, rx in TRAIT_RX.items() if rx.search(title or "")]


DESC_RX = {name: re.compile(rx, re.I) for name, rx in DESC_TRAITS.items()}


def desc_traits_of(record: dict[str, Any]) -> list[str]:
    """매장이 알려 준 설명·태그에서 읽은 특징 (제목에 없어도 잡음). 매장정보가 없으면 빈 목록."""
    meta = (record.get("raw_item") or {}).get("매장정보") or {}
    text = " ".join([str(meta.get("desc") or ""), " ".join(meta.get("tags") or [])])
    return [name for name, rx in DESC_RX.items() if rx.search(text)]


def _family_of(entity_id: str, entities: dict[str, Any]) -> str | None:
    parent = (entities.get(entity_id) or {}).get("parent")
    return parent if parent in FAMILIES else None


def _first_position(family: str, title: str, catalog: dict[str, Any]) -> int:
    """제목에서 그 모델 이름이 처음 나오는 자리 (기본형 갈래의 '꼭 있어야 할 말' 첫 패턴 기준)."""
    best = len(title) + 1
    for slug in FAMILIES[family]["standard"]:
        compiled = catalog["compiled"].get(bucket_id(family, slug))
        if not compiled:
            continue
        m = compiled[1][0].search(title)
        if m:
            best = min(best, m.start())
    return best


def assign(record: dict[str, Any], catalog: dict[str, Any], with_parents: Callable[[list[str], dict, str], list[str]], title: str) -> bool:
    """매물 하나의 갈래를 정한다. 바꾸었으면 True."""
    entities = catalog["entities"]
    ids = record.get("entity_ids") or []
    leaves = [e for e in ids if e in entities and not entities[e].get("children") and not entities[e].get("feature")]
    fams: dict[str, list[str]] = {}
    for leaf in leaves:
        fam = _family_of(leaf, entities)
        if fam:
            fams.setdefault(fam, []).append(leaf)
    if not fams:
        return False
    final = record.setdefault("final_output", {})
    traits = traits_of(title)
    reasons = []
    for t in desc_traits_of(record):  # 설명에서만 나온 특징 (2026-11-21 수집 보강 2단계)
        if t not in traits:
            traits.append(t)
            reasons.append(f"desc:{t}")
    if len(fams) > 1:  # 서로 다른 모델 둘 이상 → 제목에서 먼저 나온 모델. 개조품('I Umbau zu III')은 지금 모습인 뒤 모델
        if "converted" in traits:  # 지금 모습 = 제목 뒤쪽 모델. 구체적 모델(IIIf)이 있으면 넓은 이름(III)보다 먼저
            pool = [f for f in fams if f not in GENERIC_FAMILIES] or list(fams)
            keep = max(pool, key=lambda f: _first_position(f, title, catalog))
        else:
            keep = min(fams, key=lambda f: (_first_position(f, title, catalog), f in GENERIC_FAMILIES))
        reasons.append("conflict:" + ",".join(sorted(f.split(":")[-1] for f in fams)))
        fams = {keep: fams[keep]}
    family, fam_leaves = next(iter(fams.items()))
    spec = FAMILIES[family]
    slugs = {leaf[len(family) + 1:] for leaf in fam_leaves}
    # 이 모델에서 뜻이 있는 특징만 남김 (예: '블랙'은 III에서만 갈래, M3에선 의미 없음) — 가격 검문이 특징 있는 매물을 건너뛰므로
    traits = [t for t in traits if t == "defect" or TRAIT_BUCKET.get(t) in spec["new"] or TRAIT_BUCKET.get(t) in slugs]
    candidates = set(slugs)
    for trait in traits:
        slug = TRAIT_BUCKET.get(trait)
        if slug and (slug in spec["new"] or slug in slugs):
            candidates.add(slug)
    known = set(spec["priority"]) - {"*"}
    chosen = None
    for slug in spec["priority"]:
        if slug == "*":
            others = sorted(candidates - known)
            if others:
                chosen = others[0]
                break
        elif slug in candidates:
            chosen = slug
            break
    if chosen is None:
        chosen = sorted(candidates)[0]
    if chosen not in slugs:
        reasons.append(f"trait:{next(t for t in traits if TRAIT_BUCKET.get(t) == chosen)}")
    elif len(slugs) > 1:
        reasons.append("priority:" + ",".join(sorted(slugs)))
    if "defect" in traits and not final.get("entity_note"):
        final["entity_note"] = "defect"
        reasons.append("defect")
    final["bucket"] = {"traits": traits, "reason": ";".join(reasons)} if (traits or reasons) else None
    if final["bucket"] is None:
        final.pop("bucket")
    new_leaf = bucket_id(family, chosen)
    other = [e for e in leaves if _family_of(e, entities) is None]
    if [new_leaf] == fam_leaves and len(fams) == 1 and not reasons:
        return False
    new_ids = with_parents(list(dict.fromkeys(other + [new_leaf])), catalog, title)
    changed = new_ids != ids
    record["entity_ids"] = new_ids
    return changed or bool(reasons)


def review_outliers(records: list[dict[str, Any]], value: Callable[[dict], float | None], catalog: dict[str, Any],
                    with_parents: Callable[[list[str], dict, str], list[str]], title_of: Callable[[dict], str],
                    skip: set[int] = frozenset()) -> int:
    """특징 없는 스탠다드 매물이 그 갈래 판매 중 중간값의 REVIEW_HIGH배를 넘거나 REVIEW_LOW배 밑이면 '확인 필요'로 옮긴다."""
    entities = catalog["entities"]
    standard_ids = {bucket_id(f, s): f for f, spec in FAMILIES.items() for s in spec["standard"]}
    prices: dict[str, list[float]] = {}
    for record in records:
        final = record.get("final_output") or {}
        if id(record) in skip or final.get("sold_quality") != "asking" or final.get("entity_note"):
            continue
        v = value(record)
        if not v:
            continue
        for eid in record.get("entity_ids") or []:
            if eid in standard_ids:
                prices.setdefault(eid, []).append(v)
    medians = {eid: statistics.median(vs) for eid, vs in prices.items() if len(vs) >= REVIEW_MIN_N}
    moved = 0
    for record in records:
        final = record.get("final_output") or {}
        if id(record) in skip or final.get("entity_note") in ("duplicate", "too_cheap", "set", "defect"):
            continue
        if (final.get("bucket") or {}).get("traits"):
            continue  # 특징이 있는 매물은 이미 갈래를 정함
        ids = record.get("entity_ids") or []
        hit = next((e for e in ids if e in medians), None)
        if not hit:
            continue
        v = value(record)
        if not v:
            continue
        ratio = v / medians[hit]
        family = standard_ids[hit]
        if REVIEW_LOW <= ratio <= FAMILIES[family].get("review_high", REVIEW_HIGH):
            continue
        review = bucket_id(family, "review")
        if review not in entities:
            continue
        title = title_of(record)
        other = [e for e in ids if e in entities and not entities[e].get("children") and not entities[e].get("feature") and e != hit
                 and (entities[e].get("parent") != family)]
        record["entity_ids"] = with_parents(list(dict.fromkeys(other + [review])), catalog, title)
        final["bucket"] = {"traits": [], "reason": f"price:{ratio:.2f}x"}
        moved += 1
    return moved
