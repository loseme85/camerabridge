from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = ROOT / "scripts" / "run_p3_beta_mvp_query_review_evidence_ui_copy_button_and_unlock_copy_fixup.py"
JSON_PATH = ROOT / "data" / "admin" / "query_review_evidence_ui_copy_button_and_unlock_copy_fixup_v0.json"
APP_TEMPLATE = ROOT / "app" / "templates" / "index.html"
ROOT_TEMPLATE = ROOT / "index.html"

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from api.search import search_from_params


FORBIDDEN_TOKENS = {
    "exact_variant_pool",
    "exact_base_model_pool",
    "broader_family_pool",
    "query_incompatible",
    "third_party_top_result",
    "Need no third-party contamination in the selected price pool.",
    "Need exact or strong compatible visible Leica results.",
    "Need 2+ exact variant priced listings.",
}


def load_module():
    spec = importlib.util.spec_from_file_location(
        "query_review_evidence_ui_copy_button_and_unlock_copy_fixup",
        SCRIPT_PATH,
    )
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


class QueryReviewEvidenceUiCopyButtonAndUnlockCopyFixupTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.module = load_module()
        cls.payload = cls.module.build_payload()
        cls.rows = {row["query"]: row for row in cls.payload["query_results"]}

    def test_default_decision_status_ready_for_owner_approved_push(self) -> None:
        self.assertEqual(
            self.payload["decision_status"],
            "query_review_evidence_ui_copy_button_and_unlock_copy_fixup_passed_ready_for_owner_approved_push",
        )

    def test_templates_include_visible_copy_summary_button(self) -> None:
        for template in [APP_TEMPLATE, ROOT_TEMPLATE]:
            with self.subTest(template=str(template)):
                text = template.read_text(encoding="utf-8")
                self.assertIn("Copy summary", text)
                self.assertIn("data-copy-query-review", text)
                self.assertIn("query-review-copy", text)

    def test_templates_no_longer_join_unlock_copy_with_debug_slashes(self) -> None:
        for template in [APP_TEMPLATE, ROOT_TEMPLATE]:
            with self.subTest(template=str(template)):
                text = template.read_text(encoding="utf-8")
                self.assertNotIn("unlock.join(' / ')", text)
                self.assertIn("query-review-unlock-list", text)

    def test_unlock_copy_is_human_readable(self) -> None:
        review = self.rows["35 lux aa"]["display_query_review"]
        needed = review["needed_to_unlock"]
        self.assertIn(
            "Price stays locked until at least 2 exact variant listings have reliable prices.",
            needed,
        )
        self.assertIn(
            "Price stays locked until the visible search results strongly match this Leica item.",
            needed,
        )
        self.assertIn("Price stays locked until:", review["copy_summary_text"])

    def test_noctilux_e60_and_rigid_keep_user_facing_labels(self) -> None:
        e60 = self.rows["Noctilux 50 f1 E60"]
        rigid = self.rows["Summicron 50 rigid"]
        self.assertIn("Leica Noctilux 50 f1 E60 candidate", e60["display_query_review"]["interpreted_target"])
        self.assertTrue(any(item["price_usage_label"] == "Not used — Third-party item" for item in e60["display_top_result_evidence"]))
        self.assertTrue(any(item["price_usage_label"] == "Not used — Duplicate listing" for item in rigid["display_top_result_evidence"]))
        self.assertEqual(rigid["display_query_review"]["price_status"], "Exact price is available.")

    def test_summilux_50_asph_stays_locked_with_readable_reason(self) -> None:
        row = self.rows["Summilux-M 50 ASPH"]
        self.assertFalse(row["display_price_summary_allowed"])
        self.assertIn("Top visible results include third-party or adjacent items.", row["display_query_review"]["why"])

    def test_m50_12_is_lens_and_reference_only(self) -> None:
        row = self.rows["M50/1.2"]
        review = row["display_query_review"]
        self.assertEqual(row["top_display_category"], "Lens")
        self.assertNotEqual(row["top_display_model"], "M5")
        self.assertEqual(review["price_status"], "Reference price only.")
        self.assertIn("Only broader reference pricing is safe for this query right now.", review["why"])

    def test_body_paths_remain_intact(self) -> None:
        for query in ["leica m5", "Leica M9", "Leica M10", "Leica M11"]:
            with self.subTest(query=query):
                response = search_from_params({"q": query, "limit": "12"})
                top = response["results"][0]["display_output"]
                self.assertEqual(top.get("display_category"), "Body")

    def test_no_internal_tokens_in_user_facing_summary(self) -> None:
        for row in self.payload["query_results"]:
            review = row.get("display_query_review") or {}
            text = " | ".join(
                [
                    review.get("copy_summary_text") or "",
                    review.get("evidence_summary") or "",
                    review.get("why") or "",
                    " ".join(review.get("needed_to_unlock") or []),
                ]
                + [item.get("result_role_label") or "" for item in row.get("display_top_result_evidence") or []]
                + [item.get("price_usage_label") or "" for item in row.get("display_top_result_evidence") or []]
            )
            for token in FORBIDDEN_TOKENS:
                self.assertNotIn(token, text, row["query"])

    def test_script_generates_pass_payload(self) -> None:
        subprocess.run([sys.executable, str(SCRIPT_PATH)], cwd=ROOT, check=True, capture_output=True, text=True)
        payload = json.loads(JSON_PATH.read_text(encoding="utf-8"))
        self.assertEqual(
            payload["decision_status"],
            "query_review_evidence_ui_copy_button_and_unlock_copy_fixup_passed_ready_for_owner_approved_push",
        )
        self.assertEqual(payload["copy_button_missing_rows"], [])
        self.assertEqual(payload["ui_still_too_technical_rows"], [])
        self.assertEqual(payload["regression_rows"], [])

    def test_push_context_can_promote_status(self) -> None:
        pushed = self.module.build_payload(
            {
                "commit_executed": True,
                "push_executed": True,
                "push_succeeded": True,
                "preview_deployment_url": "https://vercel.com/camerabridge/camerabridge",
                "preview_deployment_id": "pending_unverified",
                "preview_deployment_state": "PENDING",
                "preview_branch": "beta-ui-redesign-controlled-preview",
                "preview_commit": self.payload["git_diff_summary"]["head_commit"],
            }
        )
        self.assertEqual(
            pushed["decision_status"],
            "query_review_evidence_ui_copy_button_and_unlock_copy_fixup_pushed_ready_for_owner_recheck",
        )


if __name__ == "__main__":
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(QueryReviewEvidenceUiCopyButtonAndUnlockCopyFixupTests)
    result = unittest.TextTestRunner(verbosity=0).run(suite)
    if result.wasSuccessful():
        print(f"ok ({result.testsRun} tests)")
    raise SystemExit(0 if result.wasSuccessful() else 1)
