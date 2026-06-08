from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = ROOT / "scripts" / "run_p3_beta_mvp_tri_elmar_wate_mate_compatibility_followup.py"
JSON_PATH = ROOT / "data" / "admin" / "tri_elmar_wate_mate_compatibility_followup_v0.json"
APP_TEMPLATE = ROOT / "app" / "templates" / "index.html"

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from api.search import search_from_params


def load_module():
    spec = importlib.util.spec_from_file_location("tri_elmar_wate_mate_compatibility_followup", SCRIPT_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


class TriElmarWateMateCompatibilityFollowupTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.module = load_module()
        cls.payload = cls.module.build_payload()
        cls.rows = {row["query"]: row for row in cls.payload["rows"]}

    def test_default_decision_status_ready(self) -> None:
        self.assertEqual(
            self.payload["decision_status"],
            "tri_elmar_wate_mate_compatibility_followup_passed_ready_for_owner_approved_push",
        )

    def test_wate_rows_are_compatible_same_base_without_price_unlock(self) -> None:
        row = self.rows["wate"]
        self.assertEqual(row["body_or_lens_path"], "Lens")
        self.assertIn("WATE", row["interpreted_target"])
        self.assertFalse(row["display_price_summary_allowed"])
        tri_rows = [
            item
            for item in row["display_top_result_evidence"]
            if "16-18-21" in str(item.get("title") or "")
        ]
        self.assertTrue(tri_rows)
        for item in tri_rows[:3]:
            title = str(item.get("title") or "").lower()
            if "finder" in title:
                continue
            self.assertEqual(item.get("compatibility_label"), "Exact base model")
            self.assertNotEqual(item.get("price_usage_label"), "Not used — not compatible with this query")

    def test_tri_elmar_16_18_21_query_stays_wate_and_cross_boundary_holds(self) -> None:
        row = self.rows["tri-elmar 16-18-21"]
        self.assertIn("16-18-21", row["interpreted_target"])
        self.assertFalse(row["display_price_summary_allowed"])
        mate_rows = [
            item
            for item in row["display_top_result_evidence"]
            if "28-35-50" in str(item.get("title") or "")
        ]
        for item in mate_rows:
            self.assertIn(item.get("compatibility_label"), {"Query incompatible", "Boundary conflict"})

    def test_mate_rows_are_compatible_same_base_without_boundary_conflict(self) -> None:
        row = self.rows["mate"]
        self.assertEqual(row["body_or_lens_path"], "Lens")
        self.assertIn("MATE", row["interpreted_target"])
        self.assertFalse(row["display_price_summary_allowed"])
        tri_rows = [
            item
            for item in row["display_top_result_evidence"]
            if "28-35-50" in str(item.get("title") or "")
        ]
        self.assertTrue(tri_rows)
        for item in tri_rows[:3]:
            self.assertEqual(item.get("compatibility_label"), "Exact base model")
            self.assertNotIn(item.get("price_usage_label"), {"Not used — not compatible with this query"})

    def test_tri_elmar_28_35_50_query_stays_mate_and_cross_boundary_holds(self) -> None:
        row = self.rows["tri-elmar 28-35-50"]
        self.assertIn("28-35-50", row["interpreted_target"])
        self.assertFalse(row["display_price_summary_allowed"])
        wate_rows = [
            item
            for item in row["display_top_result_evidence"]
            if "16-18-21" in str(item.get("title") or "")
        ]
        for item in wate_rows:
            self.assertIn(item.get("compatibility_label"), {"Query incompatible", "Boundary conflict"})

    def test_generic_tri_elmar_remains_ambiguous(self) -> None:
        row = self.rows["tri-elmar"]
        self.assertEqual(row["interpreted_target"], "Leica Tri-Elmar candidate")
        self.assertFalse(row["display_price_summary_allowed"])
        self.assertNotIn("WATE", row["interpreted_target"])
        self.assertNotIn("MATE", row["interpreted_target"])

    def test_accessory_finder_rows_stay_excluded(self) -> None:
        for query in ["wate", "tri-elmar 16-18-21", "tri-elmar"]:
            with self.subTest(query=query):
                row = self.rows[query]
                finder_rows = [
                    item
                    for item in row["display_top_result_evidence"]
                    if "finder" in str(item.get("title") or "").lower()
                ]
                for item in finder_rows:
                    self.assertFalse(item.get("used_for_price"))
                    self.assertIn("Accessory", str(item.get("price_usage_label") or ""))

    def test_guard_queries_do_not_regress(self) -> None:
        self.assertFalse(search_from_params({"q": "lux", "limit": "5"}).get("display_price_summary_allowed"))
        self.assertFalse(search_from_params({"q": "cron", "limit": "5"}).get("display_price_summary_allowed"))
        self.assertFalse(search_from_params({"q": "nocti", "limit": "5"}).get("display_price_summary_allowed"))
        self.assertEqual(search_from_params({"q": "Leica M10", "limit": "5"})["results"][0]["display_output"]["display_category"], "Body")
        self.assertFalse(str(search_from_params({"q": "Leica M10", "limit": "5"}).get("display_price_band") or "").startswith("KRW 80,000 -"))
        self.assertFalse(search_from_params({"q": "APO-Summicron-SL 90", "limit": "5"}).get("display_price_summary_allowed"))
        self.assertIn("Copy summary", APP_TEMPLATE.read_text(encoding="utf-8"))

    def test_script_generates_pass_payload(self) -> None:
        subprocess.run([sys.executable, str(SCRIPT_PATH)], cwd=ROOT, check=True, capture_output=True, text=True)
        payload = json.loads(JSON_PATH.read_text(encoding="utf-8"))
        self.assertEqual(
            payload["decision_status"],
            "tri_elmar_wate_mate_compatibility_followup_passed_ready_for_owner_approved_push",
        )
        self.assertEqual(payload["cross_boundary_regressions"], [])
        self.assertEqual(payload["generic_tri_elmar_regressions"], [])
        self.assertEqual(payload["accessory_finder_regressions"], [])
        self.assertEqual(payload["price_unlock_regressions"], [])
        self.assertEqual(payload["body_lens_regressions"], [])

    def test_push_context_can_promote_status(self) -> None:
        pushed = self.module.build_payload(
            {
                "commit_executed": True,
                "push_executed": True,
                "push_succeeded": True,
                "preview_deployment_url": "https://example.vercel.app",
                "preview_deployment_id": "dpl_test",
                "preview_deployment_state": "READY",
                "preview_branch": "beta-ui-redesign-controlled-preview",
                "preview_commit": self.payload["git_diff_summary"]["head_commit"],
            }
        )
        self.assertEqual(
            pushed["decision_status"],
            "tri_elmar_wate_mate_compatibility_followup_pushed_ready_for_owner_recheck",
        )


if __name__ == "__main__":
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(TriElmarWateMateCompatibilityFollowupTests)
    result = unittest.TextTestRunner(verbosity=0).run(suite)
    if result.wasSuccessful():
        print(f"ok ({result.testsRun} tests)")
    raise SystemExit(0 if result.wasSuccessful() else 1)
