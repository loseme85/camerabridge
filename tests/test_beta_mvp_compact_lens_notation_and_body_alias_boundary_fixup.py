from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "run_p3_beta_mvp_compact_lens_notation_and_body_alias_boundary_fixup.py"
JSON_PATH = ROOT / "data" / "admin" / "beta_mvp_compact_lens_notation_and_body_alias_boundary_fixup_v0.json"
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from api.search import search_from_params
from classifier_v2 import classify_listing_v2
from query_parser import parse_query


class CompactLensBodyAliasBoundaryFixupTests(unittest.TestCase):
    def test_compact_m50_slash_not_body(self) -> None:
        intent = parse_query("M50/1.2")
        self.assertIsNone(intent["body_intent"])
        self.assertEqual(intent["mount"], "M")
        self.assertEqual(intent["focal_length"], "50")
        self.assertEqual(intent["aperture"], "1.2")

    def test_compact_m35_slash_not_body(self) -> None:
        intent = parse_query("M35/2")
        self.assertIsNone(intent["body_intent"])
        self.assertEqual(intent["mount"], "M")
        self.assertEqual(intent["focal_length"], "35")
        self.assertEqual(intent["aperture"], "2")

    def test_compact_m28_slash_not_body(self) -> None:
        intent = parse_query("M28/2.8")
        self.assertIsNone(intent["body_intent"])
        self.assertEqual(intent["mount"], "M")
        self.assertEqual(intent["focal_length"], "28")
        self.assertEqual(intent["aperture"], "2.8")

    def test_true_m5_body_alias_kept(self) -> None:
        intent = parse_query("Leica M5")
        self.assertEqual(intent["body_intent"], "M5")
        self.assertEqual(intent["mount"], "M")

    def test_true_m9_body_alias_kept(self) -> None:
        intent = parse_query("Leica M9")
        self.assertEqual(intent["body_intent"], "M9")
        self.assertEqual(intent["mount"], "M")

    def test_classifier_corrects_compact_listing_to_lens(self) -> None:
        classified = classify_listing_v2({"상품명": "[중고]Leica M50/1.2 1세대", "상품설명": ""})
        self.assertEqual(classified["category"], "Lens")
        self.assertEqual(classified["mount"], "M")
        self.assertEqual(classified["focal_length"], "50")
        self.assertTrue(classified["compact_lens_notation_detected"])
        self.assertTrue(classified["body_alias_boundary_blocked"])
        self.assertNotEqual(classified["model_canonical"], "M5")

    def test_search_compact_query_no_longer_returns_body_top(self) -> None:
        response = search_from_params({"q": "M50/1.2", "limit": 5})
        self.assertEqual(response["intent"]["mount"], "M")
        self.assertEqual(response["intent"]["focal_length"], "50")
        self.assertEqual(response["intent"]["aperture"], "1.2")
        top = (response["results"][0].get("final_output") or {})
        self.assertEqual(top.get("category"), "Lens")
        self.assertNotEqual(top.get("model_canonical"), "M5")

    def test_search_exact_listing_query_not_treated_as_m5_body(self) -> None:
        response = search_from_params({"q": "Leica M50/1.2 1세대", "limit": 5})
        top = (response["results"][0].get("final_output") or {})
        self.assertEqual(top.get("category"), "Lens")
        self.assertNotEqual(top.get("model_canonical"), "M5")
        self.assertFalse(response["market_entry_allowed"])
        self.assertFalse(response["price_summary_allowed"])

    def test_body_queries_still_return_body_top(self) -> None:
        for query, expected in [("Leica M5", "M5"), ("Leica M9", "M9"), ("Leica M10", "M10"), ("Leica M11", "M11")]:
            with self.subTest(query=query):
                response = search_from_params({"q": query, "limit": 5})
                top = (response["results"][0].get("final_output") or {})
                self.assertEqual(top.get("category"), "Body")
                self.assertEqual(top.get("model_canonical"), expected)

    def test_other_regressions_hold(self) -> None:
        expectations = {
            "q3 28": "Body",
            "ltm summaron 35": "Lens",
            "35 lux aa": "Lens",
            "summicron": "Lens",
            "leica hood 12585": "Accessory",
            "ricoh gr iiix": None,
        }
        for query, expected in expectations.items():
            with self.subTest(query=query):
                response = search_from_params({"q": query, "limit": 5})
                results = response.get("results") or []
                top = (results[0].get("final_output") or {}) if results else {}
                self.assertEqual(top.get("category"), expected)

    def test_script_generates_pass_payload(self) -> None:
        subprocess.run([sys.executable, str(SCRIPT)], cwd=ROOT, check=True, capture_output=True, text=True)
        payload = json.loads(JSON_PATH.read_text(encoding="utf-8"))
        self.assertEqual(
            payload["decision_status"],
            "beta_mvp_compact_lens_body_alias_boundary_fixup_passed_ready_for_owner_approved_push",
        )
        self.assertEqual(payload["test_verdict"]["parser_failures"], [])
        self.assertEqual(payload["test_verdict"]["body_alias_regressions"], [])
        self.assertEqual(payload["test_verdict"]["category_boundary_failures"], [])


if __name__ == "__main__":
    unittest.main()
