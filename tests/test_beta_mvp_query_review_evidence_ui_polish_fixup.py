from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = ROOT / "scripts" / "run_p3_beta_mvp_query_review_evidence_ui_polish_fixup.py"
JSON_PATH = ROOT / "data" / "admin" / "query_review_evidence_ui_polish_fixup_v0.json"
APP_TEMPLATE = ROOT / "app" / "templates" / "index.html"
ROOT_TEMPLATE = ROOT / "index.html"

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

TECHNICAL_TOKENS = {
    "exact_variant_pool",
    "exact_base_model_pool",
    "broader_family_pool",
    "query_incompatible",
}


def load_module():
    spec = importlib.util.spec_from_file_location(
        "query_review_evidence_ui_polish_fixup",
        SCRIPT_PATH,
    )
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


class QueryReviewEvidenceUiPolishFixupTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.module = load_module()
        cls.payload = cls.module.build_payload()
        cls.rows = {row["query"]: row for row in cls.payload["query_results"]}

    def test_default_decision_status_ready_for_owner_approved_push(self) -> None:
        self.assertEqual(
            self.payload["decision_status"],
            "query_review_evidence_ui_polish_fixup_passed_ready_for_owner_approved_push",
        )

    def test_35_lux_aa_reads_like_human_copy(self) -> None:
        row = self.rows["35 lux aa"]
        review = row["display_query_review"]
        self.assertIn("AA", review["interpreted_target"])
        self.assertIn("AA-specific price evidence is not enough yet.", review["why"])
        self.assertNotIn("exact_variant_pool", review["evidence_summary"])
        self.assertTrue(
            any(item["price_usage_label"] == "Not used — Price outlier" for item in row["display_top_result_evidence"])
        )

    def test_noctilux_e60_keeps_reference_honest(self) -> None:
        row = self.rows["Noctilux 50 f1 E60"]
        review = row["display_query_review"]
        self.assertIn("E60-specific price evidence is not enough yet.", review["why"])
        self.assertNotIn("990,000", row["display_broader_reference_band"] or "")
        self.assertNotIn("53,000,000", row["display_broader_reference_band"] or "")

    def test_summicron_rigid_exact_price_and_duplicate_copy(self) -> None:
        row = self.rows["Summicron 50 rigid"]
        review = row["display_query_review"]
        self.assertTrue(row["display_price_summary_allowed"])
        self.assertEqual(review["price_status"], "Exact price is available.")
        self.assertEqual(review["why"], "Clean exact variant price evidence")
        self.assertTrue(
            any(item["price_usage_label"] == "Not used — Duplicate listing" for item in row["display_top_result_evidence"])
        )

    def test_summilux_50_asph_explains_weak_fallback_cleanly(self) -> None:
        row = self.rows["Summilux-M 50 ASPH"]
        review = row["display_query_review"]
        self.assertFalse(row["display_price_summary_allowed"])
        self.assertIn("Top visible results include third-party or adjacent items.", review["why"])
        self.assertNotIn("Clean exact variant price evidence", review["why"])

    def test_body_and_compact_lens_language_stays_correct(self) -> None:
        body = self.rows["leica m5"]["display_query_review"]
        self.assertEqual(body["interpreted_target"], "Leica M5 body")
        lens = self.rows["M50/1.2"]["display_query_review"]
        self.assertIn("lens", lens["interpreted_target"].lower())

        for query in ["M50/1.2", "Leica M50/1.2 1세대"]:
            with self.subTest(query=query):
                response = search_from_params({"q": query, "limit": "12"})
                top = response["results"][0]["display_output"]
                self.assertEqual(top.get("display_category"), "Lens")
                self.assertNotEqual(top.get("display_model"), "M5")

    def test_dev_and_technical_tokens_do_not_leak(self) -> None:
        for row in self.payload["query_results"]:
            values = [
                (row.get("display_query_review") or {}).get("interpreted_target") or "",
                (row.get("display_query_review") or {}).get("price_status") or "",
                (row.get("display_query_review") or {}).get("why") or "",
                (row.get("display_query_review") or {}).get("evidence_summary") or "",
            ]
            for item in row.get("display_top_result_evidence") or []:
                values.extend(
                    [
                        item.get("result_role_label") or "",
                        item.get("price_usage_label") or "",
                        item.get("evidence_pool_label") or "",
                        " ".join(item.get("excluded_reason") or []),
                    ]
                )
            joined = " | ".join(values)
            for token in DEV_TOKENS | TECHNICAL_TOKENS:
                self.assertNotIn(token, joined, row["query"])

    def test_templates_include_summary_detail_ui_and_remove_old_copy(self) -> None:
        for template in [APP_TEMPLATE, ROOT_TEMPLATE]:
            with self.subTest(template=str(template)):
                text = template.read_text(encoding="utf-8")
                self.assertIn("Show evidence details", text)
                self.assertIn("Interpreted as", text)
                self.assertNotIn("Used for ${item.evidence_pool", text)
                self.assertNotIn("exact variant ${summary.exact_variant_pool_count", text)

    def test_script_generates_pass_payload(self) -> None:
        subprocess.run([sys.executable, str(SCRIPT_PATH)], cwd=ROOT, check=True, capture_output=True, text=True)
        payload = json.loads(JSON_PATH.read_text(encoding="utf-8"))
        self.assertEqual(
            payload["decision_status"],
            "query_review_evidence_ui_polish_fixup_passed_ready_for_owner_approved_push",
        )
        self.assertEqual(payload["test_verdict"]["dev_token_visible"], [])
        self.assertEqual(payload["test_verdict"]["query_review_too_technical"], [])
        self.assertEqual(payload["test_verdict"]["price_state_copy_confusing"], [])
        self.assertEqual(payload["test_verdict"]["price_projection_regressed"], [])
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
            "query_review_evidence_ui_polish_fixup_pushed_ready_for_owner_recheck",
        )


if __name__ == "__main__":
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(QueryReviewEvidenceUiPolishFixupTests)
    result = unittest.TextTestRunner(verbosity=0).run(suite)
    if result.wasSuccessful():
        print(f"ok ({result.testsRun} tests)")
    raise SystemExit(0 if result.wasSuccessful() else 1)
