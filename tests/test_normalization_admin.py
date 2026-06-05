from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INDEX_PATH = ROOT / "data" / "admin" / "canonical_entities_index.json"


class NormalizationAdminSeedShapeTest(unittest.TestCase):
    def test_index_references_existing_files(self) -> None:
        payload = json.loads(INDEX_PATH.read_text(encoding="utf-8"))
        for family in payload.get("families") or []:
            path = ROOT / "data" / "admin" / family["file"]
            self.assertTrue(path.exists(), str(path))

    def test_family_ids_are_unique(self) -> None:
        payload = json.loads(INDEX_PATH.read_text(encoding="utf-8"))
        ids = [family["id"] for family in payload.get("families") or []]
        self.assertEqual(len(ids), len(set(ids)))

    def test_seed_entities_have_required_fields(self) -> None:
        payload = json.loads(INDEX_PATH.read_text(encoding="utf-8"))
        for family in payload.get("families") or []:
            seed = json.loads((ROOT / "data" / "admin" / family["file"]).read_text(encoding="utf-8"))
            self.assertEqual(seed["schema_version"], "normalization_admin.canonical_seed_family.v1")
            self.assertIn("family_id", seed)
            self.assertIn("family_name", seed)
            for entity in seed.get("entities") or []:
                for key in ["id", "kind", "brand", "label", "canonical_name", "aliases", "status"]:
                    self.assertIn(key, entity)


if __name__ == "__main__":
    unittest.main()
