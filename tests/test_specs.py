"""사양표(catalog/specs.py): 키가 실제 엔티티인지, 부모·바탕 모델 상속이 맞는지."""
import json
from pathlib import Path

from catalog.specs import BASED_ON, SPECS, spec_for

ROOT = Path(__file__).resolve().parent.parent
_ents = json.loads((ROOT / "data/config/entity_catalog_v1.json").read_text(encoding="utf-8"))["entities"]
if isinstance(_ents, dict):
    _ents = [dict(v, id=k) for k, v in _ents.items()]
PARENTS = {e["id"]: e.get("parent") for e in _ents}


def test_keys_are_entities():
    missing = [k for k in list(SPECS) + list(BASED_ON) + list(BASED_ON.values()) if k not in PARENTS]
    assert missing == []


def test_version_overrides_parent():
    ttl = spec_for("leica:body:m6:ttl", PARENTS)
    assert ttl["flash_ttl"] is True and ttl["meter"] == "TTL (LED)" and "weight_g" not in ttl
    assert spec_for("leica:body:m6:classic", PARENTS)["flash_ttl"] is False


def test_based_on_and_lens_versions():
    assert spec_for("leica:body:m10-r", PARENTS)["finder"] == "0.73x"
    assert spec_for("leica:body:m10-r", PARENTS)["sensor_mp"] == 40
    ii = spec_for("leica:lens:summilux-m:50:asph:asph-ii", PARENTS)
    assert ii["min_focus_m"] == 0.45 and ii["filter"] == "E46" and ii["aperture"] == "f/1.4"
    assert spec_for("leica:lens:summilux-m:50:v2", PARENTS)["min_focus_m"] == 1.0


def test_every_body_and_lens_has_specs():
    empty = [i for i in PARENTS if i.split(":")[1] in ("body", "lens") and not spec_for(i, PARENTS)]
    assert empty == []


def test_specs_json_matches_table():
    """사양표를 고치고 scripts/build_specs_json.py를 안 돌렸으면 실패."""
    import scripts.build_specs_json as b
    on_disk = json.loads((ROOT / "data/derived/specs_v1.json").read_text(encoding="utf-8"))
    assert on_disk == json.loads(json.dumps(b.build(), ensure_ascii=False))
