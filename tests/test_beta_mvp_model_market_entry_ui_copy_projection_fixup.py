from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = ROOT / "scripts" / "run_p3_beta_mvp_model_market_entry_ui_copy_projection_fixup.py"
JSON_PATH = ROOT / "data" / "admin" / "model_market_entry_ui_copy_projection_fixup_v0.json"
APP_TEMPLATE = ROOT / "app" / "templates" / "index.html"
ROOT_TEMPLATE = ROOT / "index.html"


def load_module():
    spec = importlib.util.spec_from_file_location(
        "model_market_entry_ui_copy_projection_fixup",
        SCRIPT_PATH,
    )
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


class ModelMarketEntryUiCopyProjectionFixupTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.module = load_module()
        cls.payload = cls.module.build_payload()
        cls.rows = {row["query"]: row for row in cls.payload["rows"]}

    def test_default_decision_status_ready_for_owner_approved_push(self) -> None:
        self.assertEqual(
            self.payload["decision_status"],
            "model_market_entry_ui_copy_projection_fixup_passed_ready_for_owner_approved_push",
        )

    def test_templates_no_longer_contain_raw_market_entry_scope_copy(self) -> None:
        for template in [APP_TEMPLATE, ROOT_TEMPLATE]:
            with self.subTest(template=str(template)):
                text = template.read_text(encoding="utf-8")
                self.assertNotIn("display_price_band_source || 'locked'} / excluded", text)
                self.assertNotIn("display_price_band_source || 'locked'} / cleaned", text)
                self.assertNotIn("unlockRequirements.slice(0, 2).join(' / ')", text)
                self.assertIn("Price evidence", text)
                self.assertIn("Current evidence already supports this summary.", text)

    def test_query_review_copy_button_still_visible(self) -> None:
        for template in [APP_TEMPLATE, ROOT_TEMPLATE]:
            with self.subTest(template=str(template)):
                text = template.read_text(encoding="utf-8")
                self.assertIn("Copy summary", text)
                self.assertIn("data-copy-query-review", text)

    def test_expected_user_facing_market_entry_labels(self) -> None:
        self.assertEqual(self.rows["Summicron 50 rigid"]["market_entry_label"], "Exact price")
        self.assertEqual(self.rows["M50/1.2"]["market_entry_label"], "Reference price only")
        self.assertEqual(self.rows["leica m5"]["market_entry_label"], "Body market summary")
        self.assertEqual(self.rows["35 lux aa"]["market_entry_label"], "Reference price only")

    def test_no_internal_unlock_copy_or_scope_tokens_in_rows(self) -> None:
        forbidden = {
            "undefined",
            "exact_variant / cleaned",
            "exact_base_model / cleaned",
            "broader_family / cleaned",
            "Need no third-party contamination in the selected price pool.",
            "Need exact or strong compatible visible Leica results.",
            "Need 2+ exact variant priced listings.",
        }
        for row in self.payload["rows"]:
            text = " | ".join(
                [
                    str(row.get("market_entry_label") or ""),
                    str(row.get("market_entry_value") or ""),
                    str(row.get("why") or ""),
                    " ".join(row.get("display_unlock_requirements") or []),
                    str((row.get("display_query_review") or {}).get("copy_summary_text") or ""),
                ]
            )
            for token in forbidden:
                self.assertNotIn(token, text, row["query"])

    def test_routing_and_projection_expectations_hold(self) -> None:
        self.assertEqual(self.rows["35 lux aa"]["category"], "Lens")
        self.assertEqual(self.rows["Noctilux 50 f1 E60"]["market_entry_label"], "Reference price only")
        self.assertEqual(self.rows["Summilux-M 50 ASPH"]["market_entry_label"], "Reference price only")
        self.assertEqual(self.rows["APO-Summicron-SL 90"]["market_entry_label"], "Price locked")
        self.assertEqual(self.rows["M50/1.2"]["category"], "Lens")
        self.assertEqual(self.rows["Leica M50/1.2 1세대"]["category"], "Lens")
        for query in ["leica m5", "Leica M6", "Leica M9", "Leica M10", "Leica M11"]:
            self.assertEqual(self.rows[query]["category"], "Body", query)

    def test_no_query_review_price_or_body_regressions(self) -> None:
        self.assertEqual(self.payload["ui_still_too_technical_rows"], [])
        self.assertEqual(self.payload["query_review_regressions"], [])
        self.assertEqual(self.payload["price_projection_regressions"], [])
        self.assertEqual(self.payload["body_lens_regressions"], [])

    def test_script_generates_pass_payload(self) -> None:
        subprocess.run([sys.executable, str(SCRIPT_PATH)], cwd=ROOT, check=True, capture_output=True, text=True)
        payload = json.loads(JSON_PATH.read_text(encoding="utf-8"))
        self.assertEqual(
            payload["decision_status"],
            "model_market_entry_ui_copy_projection_fixup_passed_ready_for_owner_approved_push",
        )

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
            "model_market_entry_ui_copy_projection_fixup_pushed_ready_for_owner_recheck",
        )


if __name__ == "__main__":
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(ModelMarketEntryUiCopyProjectionFixupTests)
    result = unittest.TextTestRunner(verbosity=0).run(suite)
    if result.wasSuccessful():
        print(f"ok ({result.testsRun} tests)")
    raise SystemExit(0 if result.wasSuccessful() else 1)
