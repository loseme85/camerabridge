from __future__ import annotations

import importlib.util
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = ROOT / "scripts" / "run_p3_beta_mvp_market_entry_confidence_gate_fixup.py"


def load_module():
    spec = importlib.util.spec_from_file_location("market_entry_confidence_gate_fixup", SCRIPT_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


class BetaMvpMarketEntryConfidenceGateFixupTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.module = load_module()
        cls.payload = cls.module.build_payload()
        cls.rows = {row["query"]: row for row in cls.payload["query_regression_results"]}

    def test_default_decision_status_ready_for_owner_approved_push(self):
        self.assertEqual(
            self.payload["decision_status"],
            "beta_mvp_market_entry_confidence_gate_fixup_passed_ready_for_owner_approved_push",
        )

    def test_gate_fields_declared(self):
        self.assertIn("market_entry_allowed", self.payload["implemented_gate_fields"])
        self.assertIn("price_summary_allowed", self.payload["implemented_gate_fields"])
        self.assertIn("dangerous_unknown_family_token_detected", self.payload["implemented_gate_fields"])

    def test_summicron_m_35_asph_stays_locked(self):
        row = self.rows["Summicron-M 35 ASPH"]
        self.assertFalse(row["market_entry_allowed"])
        self.assertFalse(row["price_summary_allowed"])
        self.assertEqual(row["top_result_model"], "APO-Summicron")
        self.assertIn("dangerous_unknown_family_token", row["market_entry_block_reason"])

    def test_leica_m_35_summicron_asph_does_not_allow_apo_anchor(self):
        row = self.rows["Leica M 35mm f2 Summicron ASPH"]
        self.assertFalse(row["market_entry_allowed"])
        self.assertFalse(row["price_summary_allowed"])
        self.assertEqual(row["top_result_model"], "APO-Summicron")
        self.assertIn("family_conflict", row["market_entry_block_reason"])

    def test_mount_cross_anchor_queries_stay_locked(self):
        self.assertFalse(self.rows["APO-Summicron-SL 50"]["market_entry_allowed"])
        self.assertFalse(self.rows["APO-Summicron-SL 90"]["market_entry_allowed"])
        self.assertFalse(self.rows["Summicron-M 50"]["market_entry_allowed"])

    def test_broad_queries_are_blocked_and_require_refinement(self):
        for query in ["summicron", "leica lens"]:
            row = self.rows[query]
            self.assertFalse(row["market_entry_allowed"])
            self.assertFalse(row["price_summary_allowed"])
            self.assertTrue(row["needs_disambiguation"])

    def test_ltm_summaron_35_regression_path_stays_good(self):
        row = self.rows["ltm summaron 35"]
        self.assertTrue(row["market_entry_allowed"])
        self.assertTrue(row["price_summary_allowed"])
        self.assertEqual(row["top_result_model"], "Summaron")

    def test_35_lux_aa_market_entry_recovers(self):
        row = self.rows["35 lux aa"]
        self.assertTrue(row["market_entry_allowed"])
        self.assertFalse(row["boundary_conflict_detected"])
        self.assertEqual(row["top_result_model"], "Summilux-M")

    def test_q3_28_body_regression_path_stays_good(self):
        row = self.rows["q3 28"]
        self.assertTrue(row["market_entry_allowed"])
        self.assertTrue(row["price_summary_allowed"])
        self.assertEqual(row["top_result_category"], "Body")

    def test_no_result_queries_stay_locked_without_fake_fill(self):
        for query in ["ricoh gr iiix", "hasselblad xpan"]:
            row = self.rows[query]
            self.assertFalse(row["market_entry_allowed"])
            self.assertFalse(row["price_summary_allowed"])
            self.assertEqual(row["total_ranked"], 0)

    def test_ui_copy_changes_recorded(self):
        copies = {item["copy"] for item in self.payload["ui_copy_changes"]}
        self.assertIn("Exact model summary is locked until confidence is high enough.", copies)
        self.assertIn("Not enough exact confidence for price summary", copies)
        self.assertIn("Refine this search", copies)

    def test_production_alias_connect_remains_blocked(self):
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
            "beta_mvp_market_entry_confidence_gate_fixup_pushed_ready_for_owner_recheck",
        )

    def test_scenario_validation_all_passed(self):
        self.assertTrue(all(item["status"] == "passed" for item in self.payload["scenario_validation"]))

    def test_payload_serializable(self):
        json.dumps(self.payload, ensure_ascii=False)


if __name__ == "__main__":
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(BetaMvpMarketEntryConfidenceGateFixupTests)
    result = unittest.TextTestRunner(verbosity=0).run(suite)
    if result.wasSuccessful():
        print(f"ok ({result.testsRun} tests)")
    raise SystemExit(0 if result.wasSuccessful() else 1)
