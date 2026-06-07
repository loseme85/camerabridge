from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = ROOT / "scripts" / "run_p3_beta_mvp_price_band_runtime_projection_and_query_result_visibility_fixup.py"
JSON_PATH = ROOT / "data" / "admin" / "price_band_runtime_projection_and_query_result_visibility_fixup_v0.json"

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from api.search import search_from_params


DEV_TOKENS = {
    "dangerous_unknown_family_token",
    "exact_model_like_match_missing",
    "no_exact_or_strong_visible_results",
    "weak_only_fallback",
    "third_party_top_domination",
    "too_wide_price_band",
}


def load_module():
    spec = importlib.util.spec_from_file_location(
        "price_band_runtime_projection_and_query_result_visibility_fixup",
        SCRIPT_PATH,
    )
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


class PriceBandRuntimeProjectionAndQueryResultVisibilityFixupTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.module = load_module()
        cls.payload = cls.module.build_payload()
        cls.rows = {row["query"]: row for row in cls.payload["query_results"]}

    def test_default_decision_status_ready_for_owner_approved_push(self) -> None:
        self.assertEqual(
            self.payload["decision_status"],
            "price_band_runtime_projection_query_result_visibility_fixup_passed_ready_for_owner_approved_push",
        )

    def test_35_lux_aa_uses_display_contract_consistently(self) -> None:
        row = self.rows["35 lux aa"]
        self.assertFalse(row["display_price_summary_allowed"])
        self.assertEqual(row["display_price_band"], "Price summary locked")
        if row["display_broader_reference_allowed"]:
            self.assertEqual(row["display_broader_reference_band"], row["broader_reference_band"])
            self.assertIn(
                row["broader_reference_quality_state"],
                {"clean_exact_base_model_band", "clean_broader_reference_band"},
            )
            self.assertIn(
                row["display_broader_reference_label"],
                {"Exact base model reference", "Broader family reference"},
            )
        else:
            self.assertIsNone(row["display_broader_reference_band"])
            self.assertTrue(row["display_broader_reference_locked_reason"])

    def test_noctilux_e60_runtime_band_matches_display_band(self) -> None:
        row = self.rows["Noctilux 50 f1 E60"]
        self.assertFalse(row["display_price_summary_allowed"])
        self.assertTrue(row["display_broader_reference_allowed"])
        self.assertEqual(row["display_broader_reference_band"], row["broader_reference_band"])
        self.assertNotIn("990,000", row["display_broader_reference_band"] or "")
        self.assertNotIn("53,000,000", row["display_broader_reference_band"] or "")

    def test_summicron_50_rigid_uses_cleaned_display_band(self) -> None:
        row = self.rows["Summicron 50 rigid"]
        self.assertTrue(row["display_price_summary_allowed"])
        self.assertEqual(row["display_price_band"], row["price_summary_band"])
        self.assertEqual(row["display_price_scope_label"], "Exact variant price")
        self.assertFalse(row["display_broader_reference_allowed"])

    def test_summicron_35_8_element_keeps_exact_variant_band(self) -> None:
        row = self.rows["Summicron 35 8-element"]
        self.assertTrue(row["display_price_summary_allowed"])
        self.assertEqual(row["display_price_band"], row["price_summary_band"])
        self.assertEqual(row["display_price_scope_label"], "Exact variant price")

    def test_query_review_panel_fields_exist_for_key_queries(self) -> None:
        for query in [
            "35 lux aa",
            "Noctilux 50 f1 E60",
            "Summicron 50 rigid",
            "Leica Summilux-M 50mm f1.4 3세대",
            "Summilux-M 50 ASPH",
            "M50/1.2",
            "Leica M9",
            "ricoh gr iiix",
            "hasselblad xpan",
        ]:
            with self.subTest(query=query):
                row = self.rows[query]
                self.assertTrue(row["display_query_review"])
                if row["top_result_title"]:
                    self.assertGreaterEqual(row["display_top_result_evidence_count"], 1)

    def test_dev_tokens_are_not_used_in_user_facing_display_fields(self) -> None:
        for row in self.payload["query_results"]:
            values = [
                row.get("display_price_scope_label") or "",
                row.get("display_price_band") or "",
                row.get("display_broader_reference_locked_reason") or "",
                row.get("display_match_state_message") or "",
                (row.get("display_query_review") or {}).get("match_state") or "",
                (row.get("display_query_review") or {}).get("price_status") or "",
            ]
            if row.get("display_top_result_evidence"):
                values.extend(
                    " ".join(item.get("excluded_reason") or [])
                    for item in row["display_top_result_evidence"]
                )
            joined = " | ".join(values)
            for token in DEV_TOKENS:
                self.assertNotIn(token, joined, row["query"])

    def test_body_and_compact_lens_regressions_do_not_return(self) -> None:
        for query in ["M50/1.2", "Leica M50/1.2 1세대"]:
            with self.subTest(query=query):
                response = search_from_params({"q": query, "limit": "12"})
                top = response["results"][0]["display_output"]
                self.assertEqual(top.get("display_category"), "Lens")
                self.assertNotEqual(top.get("display_model"), "M5")

        for query in ["Leica M9", "Leica M10", "Leica M11"]:
            with self.subTest(query=query):
                response = search_from_params({"q": query, "limit": "12"})
                top = response["results"][0]["display_output"]
                self.assertEqual(top.get("display_category"), "Body")

    def test_script_generates_pass_payload(self) -> None:
        subprocess.run([sys.executable, str(SCRIPT_PATH)], cwd=ROOT, check=True, capture_output=True, text=True)
        payload = json.loads(JSON_PATH.read_text(encoding="utf-8"))
        self.assertEqual(
            payload["decision_status"],
            "price_band_runtime_projection_query_result_visibility_fixup_passed_ready_for_owner_approved_push",
        )
        self.assertEqual(payload["test_verdict"]["disallowed_broader_reference_visible"], [])
        self.assertEqual(payload["test_verdict"]["band_projection_mismatch"], [])
        self.assertEqual(payload["test_verdict"]["query_result_panel_missing"], [])
        self.assertEqual(payload["test_verdict"]["dev_token_visible"], [])
        self.assertEqual(payload["test_verdict"]["exact_variant_price_regressed"], [])
        self.assertEqual(payload["test_verdict"]["body_lens_regression"], [])

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
            "price_band_runtime_projection_query_result_visibility_fixup_pushed_ready_for_owner_recheck",
        )


if __name__ == "__main__":
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(
        PriceBandRuntimeProjectionAndQueryResultVisibilityFixupTests
    )
    result = unittest.TextTestRunner(verbosity=0).run(suite)
    if result.wasSuccessful():
        print(f"ok ({result.testsRun} tests)")
    raise SystemExit(0 if result.wasSuccessful() else 1)
