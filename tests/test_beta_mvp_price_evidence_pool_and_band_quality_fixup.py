from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = ROOT / "scripts" / "run_p3_beta_mvp_price_evidence_pool_and_band_quality_fixup.py"
JSON_PATH = ROOT / "data" / "admin" / "price_evidence_pool_and_band_quality_fixup_v0.json"

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from api.search import search_from_params


def load_module():
    spec = importlib.util.spec_from_file_location("price_evidence_pool_and_band_quality_fixup", SCRIPT_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


class PriceEvidencePoolAndBandQualityFixupTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.module = load_module()
        cls.payload = cls.module.build_payload()
        cls.rows = {row["query"]: row for row in cls.payload["query_results"]}

    def test_default_decision_status_ready_for_owner_approved_push(self) -> None:
        self.assertEqual(
            self.payload["decision_status"],
            "price_evidence_pool_band_quality_fixup_passed_ready_for_owner_approved_push",
        )

    def test_noctilux_e60_no_longer_uses_raw_noisy_band(self) -> None:
        row = self.rows["Noctilux 50 f1 E60"]
        self.assertFalse(row["price_summary_allowed"])
        self.assertEqual(row["price_scope"], "insufficient_exact_data")
        self.assertEqual(row["price_scope_label"], "Exact variant price data limited")
        self.assertTrue(row["broader_reference_allowed"])
        self.assertEqual(row["broader_reference_quality_state"], "clean_broader_reference_band")
        self.assertNotIn("990,000", row["broader_reference_band"] or "")
        self.assertNotIn("53,000,000", row["broader_reference_band"] or "")

    def test_summilux_3rd_generation_stays_locked_as_exact_variant(self) -> None:
        for query in ["Leica Summilux-M 50mm f1.4 3세대", "Summilux 50 3rd generation"]:
            with self.subTest(query=query):
                row = self.rows[query]
                self.assertFalse(row["price_summary_allowed"])
                self.assertEqual(row["price_scope"], "insufficient_exact_data")
                self.assertEqual(row["price_scope_label"], "Exact variant price data limited")

    def test_35_lux_aa_does_not_open_exact_price(self) -> None:
        row = self.rows["35 lux aa"]
        self.assertFalse(row["price_summary_allowed"])
        self.assertEqual(row["price_scope_label"], "Price summary locked")
        self.assertIn(row["broader_reference_locked_reason"], {None, "too_wide_price_band", "too_noisy_broader_reference"})

    def test_summilux_m_50_asph_stays_locked_on_weak_fallback(self) -> None:
        row = self.rows["Summilux-M 50 ASPH"]
        self.assertFalse(row["price_summary_allowed"])
        self.assertEqual(row["price_scope"], "blocked_weak_only")
        self.assertEqual(row["search_confidence_state"], "weak_only_fallback")
        self.assertGreaterEqual(row["excluded_pool_count"], 1)

    def test_exact_variant_stable_queries_keep_clean_price_scope(self) -> None:
        for query in ["Summicron 35 8-element", "Summicron 50 rigid", "Leica M50/1.2 1세대"]:
            with self.subTest(query=query):
                row = self.rows[query]
                self.assertTrue(row["price_summary_allowed"])
                self.assertEqual(row["price_scope"], "exact_variant")
                self.assertEqual(row["price_band_quality_state"], "clean_exact_variant_band")

    def test_broader_family_references_can_stay_open_when_clean(self) -> None:
        for query in ["Noctilux 50 0.95", "Summaron 35 2.8"]:
            with self.subTest(query=query):
                row = self.rows[query]
                self.assertFalse(row["price_summary_allowed"])
                self.assertTrue(row["broader_reference_allowed"])
                self.assertEqual(row["broader_reference_quality_state"], "clean_broader_reference_band")

    def test_boundary_conflict_stays_locked(self) -> None:
        row = self.rows["APO-Summicron-SL 90"]
        self.assertFalse(row["price_summary_allowed"])
        self.assertEqual(row["price_scope"], "blocked_boundary_conflict")

    def test_body_and_compact_lens_regressions_do_not_return(self) -> None:
        for query in ["M50/1.2", "Leica M50/1.2 1세대"]:
            with self.subTest(query=query):
                response = search_from_params({"q": query, "limit": "10"})
                top = response["results"][0]["display_output"]
                self.assertEqual(top.get("display_category"), "Lens")
                self.assertNotEqual(top.get("display_model"), "M5")

        for query in ["Leica M9", "Leica M10", "Leica M11"]:
            with self.subTest(query=query):
                response = search_from_params({"q": query, "limit": "5"})
                top = response["results"][0]["display_output"]
                self.assertEqual(top.get("display_category"), "Body")

    def test_exact_base_model_safe_regressions_hold(self) -> None:
        for query in ["ltm summaron 35", "Elmarit-R 28"]:
            with self.subTest(query=query):
                row = self.rows[query]
                self.assertTrue(row["price_summary_allowed"])
                self.assertEqual(row["price_scope"], "exact_base_model")

    def test_script_generates_pass_payload(self) -> None:
        subprocess.run([sys.executable, str(SCRIPT_PATH)], cwd=ROOT, check=True, capture_output=True, text=True)
        payload = json.loads(JSON_PATH.read_text(encoding="utf-8"))
        self.assertEqual(
            payload["decision_status"],
            "price_evidence_pool_band_quality_fixup_passed_ready_for_owner_approved_push",
        )
        self.assertEqual(payload["test_verdict"]["noisy_band_still_shown"], [])
        self.assertEqual(payload["test_verdict"]["outlier_not_excluded"], [])
        self.assertEqual(payload["test_verdict"]["wrong_model_or_accessory_price_included"], [])
        self.assertEqual(payload["test_verdict"]["exact_variant_price_regressed"], [])
        self.assertEqual(payload["test_verdict"]["body_lens_regressions"], [])

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
            "price_evidence_pool_band_quality_fixup_pushed_ready_for_owner_recheck",
        )


if __name__ == "__main__":
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(PriceEvidencePoolAndBandQualityFixupTests)
    result = unittest.TextTestRunner(verbosity=0).run(suite)
    if result.wasSuccessful():
        print(f"ok ({result.testsRun} tests)")
    raise SystemExit(0 if result.wasSuccessful() else 1)
