from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from api.search import search_from_params
from search_service import load_search_records


ROOT = Path(__file__).resolve().parents[1]
INDEX_PATH = ROOT / "data" / "admin" / "canonical_entities_index.json"
BODY_FAMILY_IDS = {
    "leica_m_film_bodies",
    "leica_m_digital_bodies",
    "leica_q_bodies",
    "leica_sl_bodies",
}


def _summary(query: str) -> dict:
    response = search_from_params({"q": query, "limit": "5"}, records=load_search_records())
    results = list(response.get("results") or [])
    top = results[0] if results else {}
    display = top.get("display_output") or {}
    final = top.get("final_output") or {}
    return {
        "body_intent": (response.get("intent") or {}).get("body_intent"),
        "market_entry_allowed": bool(response.get("market_entry_allowed")),
        "top_category": display.get("display_category") or final.get("category"),
        "top_model": display.get("display_model") or final.get("model_canonical") or final.get("model_raw"),
        "top_three_categories": [
            ((item.get("display_output") or {}).get("display_category") or (item.get("final_output") or {}).get("category"))
            for item in results[:3]
        ],
        "total_ranked": int(response.get("total_ranked") or 0),
    }


class LeicaBodyCanonicalEntryBackfillTest(unittest.TestCase):
    def test_index_contains_new_body_families(self) -> None:
        payload = json.loads(INDEX_PATH.read_text(encoding="utf-8"))
        families = {item["id"]: item for item in payload.get("families") or []}
        for family_id in BODY_FAMILY_IDS:
            self.assertIn(family_id, families)
            path = ROOT / "data" / "admin" / families[family_id]["file"]
            self.assertTrue(path.exists(), str(path))

    def test_new_body_seed_files_only_contain_leica_body_rows(self) -> None:
        payload = json.loads(INDEX_PATH.read_text(encoding="utf-8"))
        for family in payload.get("families") or []:
            if family["id"] not in BODY_FAMILY_IDS:
                continue
            path = ROOT / "data" / "admin" / family["file"]
            seed = json.loads(path.read_text(encoding="utf-8"))
            self.assertEqual(seed["status"], "active")
            for entity in seed.get("entities") or []:
                self.assertEqual(entity["kind"], "Body")
                self.assertEqual(entity["brand"], "Leica")
                self.assertTrue(entity["canonical_name"].startswith("Leica "))

    def test_high_confidence_body_queries_still_top_body(self) -> None:
        expected = {
            "Leica M3": "M3",
            "Leica M4": "M4",
            "Leica M5": "M5",
            "Leica M6": "M6",
            "Leica MP": "MP",
            "Leica M9": "M9",
            "Leica M10": "M10",
            "Leica M10-R": "M10-R",
            "Leica M11": "M11",
            "Leica Q2": "Q2",
            "Leica Q3": "Q3",
            "Leica SL2": "SL2",
            "Leica SL3": "SL3",
        }
        for query, model in expected.items():
            with self.subTest(query=query):
                summary = _summary(query)
                self.assertEqual(summary["top_category"], "Body")
                self.assertEqual(summary["top_model"], model)
                self.assertTrue(all(cat == "Body" for cat in summary["top_three_categories"]))

    def test_hold_candidates_remain_out_of_active_seed_promotions(self) -> None:
        payload = json.loads(INDEX_PATH.read_text(encoding="utf-8"))
        text = json.dumps(payload, ensure_ascii=False)
        for needle in ["Leica M2 body", "Leica M1 body", "Leica M7 body", "Leica M-A body", "Leica Q body"]:
            with self.subTest(needle=needle):
                self.assertNotIn(needle, text)

    def test_m2_still_not_promoted_as_safe_body_entry(self) -> None:
        summary = _summary("Leica M2")
        self.assertEqual(summary["body_intent"], "M2")
        self.assertNotEqual(summary["top_category"], "Body")

    def test_compact_lens_notation_regression_stays_blocked(self) -> None:
        for query in ["M50/1.2", "Leica M50/1.2 1세대"]:
            with self.subTest(query=query):
                summary = _summary(query)
                self.assertNotEqual(summary["top_model"], "M5")
                self.assertNotEqual(summary["top_category"], "Body")

    def test_no_result_regression_stays_safe(self) -> None:
        for query in ["ricoh gr iiix", "hasselblad xpan"]:
            with self.subTest(query=query):
                summary = _summary(query)
                self.assertEqual(summary["total_ranked"], 0)


if __name__ == "__main__":
    unittest.main()
