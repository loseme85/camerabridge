from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = ROOT / "scripts" / "run_p3_beta_mvp_lens_variant_specific_price_scope_fixup.py"
JSON_PATH = ROOT / "data" / "admin" / "lens_variant_specific_price_scope_fixup_v0.json"

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from api.search import search_from_params


def load_module():
    spec = importlib.util.spec_from_file_location("lens_variant_specific_price_scope_fixup", SCRIPT_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


class LensVariantSpecificPriceScopeFixupTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.module = load_module()
        cls.payload = cls.module.build_payload()
        cls.rows = {row["query"]: row for row in cls.payload["query_results"]}

    def test_default_decision_status_ready_for_owner_approved_push(self) -> None:
        self.assertEqual(
            self.payload["decision_status"],
            "lens_variant_specific_price_scope_fixup_passed_ready_for_owner_approved_push",
        )

    def test_variant_data_limited_queries_do_not_open_exact_price(self) -> None:
        for query in [
            "Leica Summilux-M 50mm f1.4 3세대",
            "Summilux 50 3rd generation",
            "Summilux-M 50 pre-ASPH",
            "35 lux aa",
            "Noctilux 50 f1 E60",
        ]:
            with self.subTest(query=query):
                row = self.rows[query]
                self.assertFalse(row["price_summary_allowed"])
                self.assertIn(row["price_scope_label"], {"Exact variant price data limited", "Price summary locked"})
                self.assertTrue(row["current_ui_label_safe"])

    def test_limited_queries_can_offer_broader_reference_only(self) -> None:
        for query in ["Summilux 50 3rd generation", "35 lux aa", "Noctilux 50 f1 E60"]:
            with self.subTest(query=query):
                row = self.rows[query]
                self.assertTrue(row["broader_reference_allowed"])
                self.assertEqual(row["broader_reference_label"], "Broader family reference")

    def test_exact_variant_ready_queries_stay_open(self) -> None:
        for query in ["Summicron 35 8-element", "Summicron 50 rigid"]:
            with self.subTest(query=query):
                row = self.rows[query]
                self.assertTrue(row["price_summary_allowed"])
                self.assertEqual(row["price_scope"], "exact_variant")
                self.assertEqual(row["price_scope_label"], "Exact variant price")

    def test_summilux_m_50_asph_locks_when_search_confidence_is_weak(self) -> None:
        row = self.rows["Summilux-M 50 ASPH"]
        self.assertFalse(row["price_summary_allowed"])
        self.assertEqual(row["price_scope_label"], "Price summary locked")
        self.assertTrue(row["broader_reference_allowed"])

    def test_broader_family_only_queries_do_not_look_exact(self) -> None:
        for query in ["Noctilux 50 0.95", "Summaron 35 2.8"]:
            with self.subTest(query=query):
                row = self.rows[query]
                self.assertFalse(row["price_summary_allowed"])
                self.assertEqual(row["price_scope"], "broader_model_family")
                self.assertEqual(row["price_scope_label"], "Broader family reference")
                self.assertTrue(row["broader_reference_allowed"])

    def test_boundary_conflicts_stay_locked(self) -> None:
        for query in ["Summicron-M 35 ASPH", "APO-Summicron-SL 90"]:
            with self.subTest(query=query):
                row = self.rows[query]
                self.assertFalse(row["price_summary_allowed"])
                self.assertEqual(row["price_scope"], "blocked_boundary_conflict")
                self.assertEqual(row["price_scope_label"], "Price summary locked")

    def test_safe_exact_base_model_regressions_hold(self) -> None:
        for query in ["ltm summaron 35", "Elmarit-R 28"]:
            with self.subTest(query=query):
                row = self.rows[query]
                self.assertTrue(row["price_summary_allowed"])
                self.assertEqual(row["price_scope"], "exact_base_model")
                self.assertEqual(row["price_scope_label"], "Exact base model price")

    def test_compact_lens_query_does_not_regress_to_m5_body(self) -> None:
        response = search_from_params({"q": "M50/1.2", "limit": "10"})
        top = response["results"][0]["display_output"]
        self.assertEqual(top.get("display_category"), "Lens")
        self.assertNotEqual(top.get("display_model"), "M5")

    def test_true_body_paths_remain_safe(self) -> None:
        for query in ["Leica M9", "Leica M10", "Leica M11"]:
            with self.subTest(query=query):
                response = search_from_params({"q": query, "limit": "5"})
                top = response["results"][0]["display_output"]
                self.assertEqual(top.get("display_category"), "Body")

    def test_script_generates_pass_payload(self) -> None:
        subprocess.run([sys.executable, str(SCRIPT_PATH)], cwd=ROOT, check=True, capture_output=True, text=True)
        payload = json.loads(JSON_PATH.read_text(encoding="utf-8"))
        self.assertEqual(
            payload["decision_status"],
            "lens_variant_specific_price_scope_fixup_passed_ready_for_owner_approved_push",
        )
        self.assertEqual(payload["test_verdict"]["unsafe_broader_family_price_as_exact"], [])
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
            "lens_variant_specific_price_scope_fixup_pushed_ready_for_owner_recheck",
        )


if __name__ == "__main__":
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(LensVariantSpecificPriceScopeFixupTests)
    result = unittest.TextTestRunner(verbosity=0).run(suite)
    if result.wasSuccessful():
        print(f"ok ({result.testsRun} tests)")
    raise SystemExit(0 if result.wasSuccessful() else 1)
