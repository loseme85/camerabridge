from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "run_p3_beta_mvp_result_card_runtime_normalization_projection_fixup.py"
JSON_PATH = ROOT / "data" / "admin" / "beta_mvp_result_card_runtime_normalization_projection_fixup_v0.json"
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from api.search import search_from_params


TARGET_TITLE = "[중고]Leica M50/1.2 1세대"


def _find_title_result(response: dict, title: str = TARGET_TITLE) -> dict | None:
    for result in response.get("results") or []:
        if (result.get("title") or "") == title:
            return result
    return None


class ResultCardRuntimeProjectionFixupTests(unittest.TestCase):
    def test_compact_title_row_in_body_query_uses_display_projection(self) -> None:
        response = search_from_params({"q": "Leica M5", "limit": "100"})
        result = _find_title_result(response)
        self.assertIsNotNone(result)
        display = result.get("display_output") or {}
        final = result.get("final_output") or {}
        self.assertEqual(final.get("category"), "Lens")
        self.assertEqual(display.get("display_category"), "Lens")
        self.assertIsNone(display.get("display_model"))
        self.assertEqual(display.get("display_family"), "M Lens")
        self.assertEqual(display.get("display_mount"), "M")
        self.assertEqual(display.get("display_focal_length"), "50")
        self.assertEqual(display.get("display_aperture"), "f1.2")
        self.assertTrue(display.get("stale_normalization_detected"))
        self.assertTrue(display.get("classification_conflict_detected"))

    def test_owner_target_query_does_not_surface_m5_body_card_metadata(self) -> None:
        response = search_from_params({"q": TARGET_TITLE, "limit": "100"})
        result = _find_title_result(response)
        self.assertIsNotNone(result)
        display = result.get("display_output") or {}
        self.assertNotEqual(display.get("display_category"), "Body")
        self.assertNotEqual(display.get("display_model"), "M5")
        self.assertTrue(display.get("compact_lens_notation_detected"))

    def test_compact_m50_query_display_path_is_lens(self) -> None:
        response = search_from_params({"q": "M50/1.2", "limit": "100"})
        result = _find_title_result(response)
        self.assertIsNotNone(result)
        display = result.get("display_output") or {}
        self.assertEqual(display.get("display_category"), "Lens")
        self.assertEqual(display.get("display_mount"), "M")
        self.assertEqual(display.get("display_focal_length"), "50")
        self.assertEqual(display.get("display_aperture"), "f1.2")

    def test_m35_compact_query_not_m3_body(self) -> None:
        response = search_from_params({"q": "M35/2", "limit": "5"})
        top = response["results"][0]["display_output"]
        self.assertEqual(top.get("display_category"), "Lens")
        self.assertNotEqual(top.get("display_model"), "M3")

    def test_m28_compact_query_not_m2_body(self) -> None:
        response = search_from_params({"q": "M28/2.8", "limit": "5"})
        top = response["results"][0]["display_output"]
        self.assertEqual(top.get("display_category"), "Lens")
        self.assertNotEqual(top.get("display_model"), "M2")

    def test_true_m5_body_top_still_body(self) -> None:
        response = search_from_params({"q": "Leica M5", "limit": "5"})
        top = response["results"][0]["display_output"]
        self.assertEqual(top.get("display_category"), "Body")
        self.assertEqual(top.get("display_model"), "M5")

    def test_true_body_regressions_hold(self) -> None:
        for query, expected in [("Leica M9", "M9"), ("Leica M10", "M10"), ("Leica M11", "M11"), ("q3 28", "Q3")]:
            with self.subTest(query=query):
                response = search_from_params({"q": query, "limit": "5"})
                top = response["results"][0]["display_output"]
                self.assertEqual(top.get("display_category"), "Body")
                self.assertEqual(top.get("display_model"), expected)

    def test_lens_accessory_no_result_regressions_hold(self) -> None:
        expectations = {
            "ltm summaron 35": "Lens",
            "35 lux aa": "Lens",
            "summicron": "Lens",
            "leica hood 12585": "Accessory",
            "ricoh gr iiix": None,
        }
        for query, expected in expectations.items():
            with self.subTest(query=query):
                response = search_from_params({"q": query, "limit": "5"})
                results = response.get("results") or []
                top = (results[0].get("display_output") or {}) if results else {}
                self.assertEqual(top.get("display_category"), expected)

    def test_market_entry_gate_can_see_display_conflict(self) -> None:
        response = search_from_params({"q": TARGET_TITLE, "limit": "100"})
        self.assertFalse(response["market_entry_allowed"])
        self.assertFalse(response["price_summary_allowed"])

    def test_script_generates_pass_payload(self) -> None:
        subprocess.run([sys.executable, str(SCRIPT)], cwd=ROOT, check=True, capture_output=True, text=True)
        payload = json.loads(JSON_PATH.read_text(encoding="utf-8"))
        self.assertEqual(
            payload["decision_status"],
            "beta_mvp_result_card_runtime_projection_fixup_passed_ready_for_owner_approved_push",
        )
        self.assertEqual(payload["test_verdict"]["stale_display_failures"], [])
        self.assertEqual(payload["test_verdict"]["true_body_alias_regressions"], [])
        self.assertEqual(payload["test_verdict"]["stale_display_truth_failures"], [])


if __name__ == "__main__":
    unittest.main()
