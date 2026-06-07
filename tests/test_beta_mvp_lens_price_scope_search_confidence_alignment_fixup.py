from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = ROOT / "scripts" / "run_p3_beta_mvp_lens_price_scope_search_confidence_alignment_fixup.py"
JSON_PATH = ROOT / "data" / "admin" / "lens_price_scope_search_confidence_alignment_fixup_v0.json"

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from api.search import search_from_params


def load_module():
    spec = importlib.util.spec_from_file_location("lens_price_scope_search_confidence_alignment_fixup", SCRIPT_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


class LensPriceScopeSearchConfidenceAlignmentFixupTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.module = load_module()
        cls.payload = cls.module.build_payload()
        cls.rows = {row["query"]: row for row in cls.payload["query_results"]}

    def test_default_decision_status_ready_for_owner_approved_push(self) -> None:
        self.assertEqual(
            self.payload["decision_status"],
            "lens_price_scope_search_confidence_alignment_fixup_passed_ready_for_owner_approved_push",
        )

    def test_summilux_m_50_asph_does_not_open_exact_price_on_weak_fallback(self) -> None:
        row = self.rows["Summilux-M 50 ASPH"]
        self.assertFalse(row["price_summary_allowed"])
        self.assertEqual(row["price_scope_label"], "Price summary locked")
        self.assertEqual(row["search_confidence_state"], "weak_only_fallback")
        self.assertFalse(row["price_scope_search_aligned"])
        self.assertTrue(row["third_party_top_domination_detected"])
        self.assertEqual(row["exact_or_strong_visible_result_count"], 0)

    def test_exact_variant_ready_queries_stay_open_when_search_is_aligned(self) -> None:
        for query in ["Summicron 35 8-element", "Summicron 50 rigid"]:
            with self.subTest(query=query):
                row = self.rows[query]
                self.assertTrue(row["price_summary_allowed"])
                self.assertEqual(row["price_scope"], "exact_variant")
                self.assertTrue(row["price_scope_search_aligned"])
                self.assertEqual(row["top_result_compatibility"], "exact_variant_strong")

    def test_exact_variant_data_limited_queries_stay_limited(self) -> None:
        for query in [
            "Leica Summilux-M 50mm f1.4 3세대",
            "Noctilux 50 f1 E60",
        ]:
            with self.subTest(query=query):
                row = self.rows[query]
                self.assertFalse(row["price_summary_allowed"])
                self.assertEqual(row["price_scope"], "insufficient_exact_data")
                self.assertEqual(row["price_scope_label"], "Exact variant price data limited")
                self.assertTrue(row["broader_reference_allowed"])

    def test_summilux_50_3rd_generation_can_open_when_exact_evidence_and_search_align(self) -> None:
        row = self.rows["Summilux 50 3rd generation"]
        self.assertTrue(row["price_summary_allowed"])
        self.assertEqual(row["price_scope"], "exact_variant")
        self.assertEqual(row["price_scope_label"], "Exact variant price")
        self.assertTrue(row["price_scope_search_aligned"])

    def test_35_lux_aa_stays_locked_when_no_exact_strong_visible_results(self) -> None:
        row = self.rows["35 lux aa"]
        self.assertFalse(row["price_summary_allowed"])
        self.assertEqual(row["price_scope_label"], "Price summary locked")
        self.assertFalse(row["price_scope_search_aligned"])
        self.assertIn("no_exact_or_strong_visible_results", row["price_scope_search_alignment_reason"])

    def test_boundary_conflict_stays_locked(self) -> None:
        row = self.rows["APO-Summicron-SL 90"]
        self.assertFalse(row["price_summary_allowed"])
        self.assertEqual(row["price_scope"], "blocked_boundary_conflict")
        self.assertEqual(row["search_confidence_state"], "boundary_conflict")

    def test_compact_lens_and_body_regressions_hold(self) -> None:
        response = search_from_params({"q": "M50/1.2", "limit": "10"})
        top = response["results"][0]["display_output"]
        self.assertEqual(top.get("display_category"), "Lens")
        self.assertNotEqual(top.get("display_model"), "M5")
        for query in ["Leica M9", "Leica M10", "Leica M11"]:
            with self.subTest(query=query):
                body = search_from_params({"q": query, "limit": "5"})["results"][0]["display_output"]
                self.assertEqual(body.get("display_category"), "Body")

    def test_exact_base_model_safe_path_holds(self) -> None:
        row = self.rows["ltm summaron 35"]
        self.assertTrue(row["price_summary_allowed"])
        self.assertEqual(row["price_scope"], "exact_base_model")
        self.assertTrue(row["price_scope_search_aligned"])

    def test_script_generates_pass_payload(self) -> None:
        subprocess.run([sys.executable, str(SCRIPT_PATH)], cwd=ROOT, check=True, capture_output=True, text=True)
        payload = json.loads(JSON_PATH.read_text(encoding="utf-8"))
        self.assertEqual(
            payload["decision_status"],
            "lens_price_scope_search_confidence_alignment_fixup_passed_ready_for_owner_approved_push",
        )
        self.assertEqual(payload["test_verdict"]["exact_price_opens_on_weak_fallback"], [])
        self.assertEqual(payload["test_verdict"]["exact_variant_ready_regressions"], [])
        self.assertEqual(payload["test_verdict"]["boundary_conflict_price_opened"], [])
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
            "lens_price_scope_search_confidence_alignment_fixup_pushed_ready_for_owner_recheck",
        )


if __name__ == "__main__":
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(LensPriceScopeSearchConfidenceAlignmentFixupTests)
    result = unittest.TextTestRunner(verbosity=0).run(suite)
    if result.wasSuccessful():
        print(f"ok ({result.testsRun} tests)")
    raise SystemExit(0 if result.wasSuccessful() else 1)
