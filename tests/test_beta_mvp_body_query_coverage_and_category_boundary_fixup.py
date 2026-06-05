from __future__ import annotations

import importlib.util
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = ROOT / "scripts" / "run_p3_beta_mvp_body_query_coverage_and_category_boundary_fixup.py"


def load_module():
    spec = importlib.util.spec_from_file_location("body_query_boundary_fixup", SCRIPT_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


class BetaMvpBodyQueryCoverageAndCategoryBoundaryFixupTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.module = load_module()
        cls.payload = cls.module.build_payload()
        cls.rows = {row["query"]: row for row in cls.payload["query_regression_results"]}

    def test_default_decision_status_ready_for_owner_approved_push(self):
        self.assertEqual(
            self.payload["decision_status"],
            "beta_mvp_body_query_coverage_category_boundary_fixup_passed_ready_for_owner_approved_push",
        )

    def test_m9_queries_resolve_to_body(self):
        for query in ["Leica M9", "leica m9", "m9"]:
            row = self.rows[query]
            self.assertTrue(row["body_query_detected"])
            self.assertEqual(row["intent"].get("body_intent"), "M9")
            self.assertEqual(row["top_result_category"], "Body")
            self.assertEqual(row["top_result_model"], "M9")
            self.assertEqual(row["top_three_lens_domination_count"], 0)
            self.assertTrue(row["weak_brand_lens_fallback_suppressed"])

    def test_m9_p_and_m10_r_keep_variant_body_path(self):
        self.assertEqual(self.rows["Leica M9-P"]["intent"].get("body_intent"), "M9-P")
        self.assertIn("P", self.rows["Leica M9-P"]["intent"].get("variant") or [])
        self.assertEqual(self.rows["Leica M10-R"]["intent"].get("body_intent"), "M10-R")
        self.assertIn("R", self.rows["Leica M10-R"]["intent"].get("variant") or [])

    def test_m10_and_m11_no_longer_let_lens_dominate(self):
        for query in ["Leica M10", "Leica M11"]:
            row = self.rows[query]
            self.assertEqual(row["top_result_category"], "Body")
            self.assertEqual(row["top_three_boundary_conflict_count"], 0)
            self.assertEqual(row["top_three_weak_brand_lens_count"], 0)

    def test_existing_safe_body_queries_remain_safe(self):
        for query in ["q3 28", "Leica SL2", "Leica MP silver"]:
            row = self.rows[query]
            self.assertTrue(row["body_query_detected"])
            self.assertEqual(row["top_result_category"], "Body")

    def test_broad_lens_query_not_misclassified_as_body(self):
        row = self.rows["summicron"]
        self.assertFalse(row["body_query_detected"])
        self.assertEqual(row["top_result_category"], "Lens")

    def test_safe_lens_queries_remain_lens(self):
        self.assertEqual(self.rows["ltm summaron 35"]["top_result_category"], "Lens")
        self.assertEqual(self.rows["35 lux aa"]["top_result_category"], "Lens")

    def test_accessory_queries_remain_accessory(self):
        self.assertEqual(self.rows["leica hood 12585"]["top_result_category"], "Accessory")
        self.assertEqual(self.rows["m adapter l"]["top_result_category"], "Accessory")

    def test_no_result_queries_stay_empty(self):
        self.assertEqual(self.rows["ricoh gr iiix"]["total_ranked"], 0)
        self.assertEqual(self.rows["hasselblad xpan"]["total_ranked"], 0)

    def test_market_entry_gate_stays_connected_for_body_queries(self):
        for query in ["Leica M9", "Leica M10", "Leica M11", "Leica M9-P", "Leica M10-R"]:
            row = self.rows[query]
            self.assertTrue(row["market_entry_allowed"])
            self.assertTrue(row["price_summary_allowed"])

    def test_body_parser_alias_changes_recorded(self):
        aliases = self.payload["body_parser_alias_changes"]["new_aliases"]
        self.assertIn("m9", aliases)
        self.assertIn("m10-r", aliases)
        self.assertIn("m11", aliases)

    def test_production_alias_connect_remains_false(self):
        self.assertFalse(self.payload["production_alias_connect_allowed"])
        self.assertFalse(self.payload["guards"]["production_alias_connect_allowed"])

    def test_push_context_can_promote_decision_status(self):
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
            "beta_mvp_body_query_coverage_category_boundary_fixup_pushed_ready_for_owner_recheck",
        )

    def test_scenario_validation_all_passed(self):
        self.assertTrue(all(item["status"] == "passed" for item in self.payload["scenario_validation"]))

    def test_payload_serializable(self):
        json.dumps(self.payload, ensure_ascii=False)


if __name__ == "__main__":
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(
        BetaMvpBodyQueryCoverageAndCategoryBoundaryFixupTests
    )
    result = unittest.TextTestRunner(verbosity=0).run(suite)
    if result.wasSuccessful():
        print(f"ok ({result.testsRun} tests)")
    raise SystemExit(0 if result.wasSuccessful() else 1)
