from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = ROOT / "scripts" / "run_p3_beta_mvp_body_price_band_quality_fixup.py"
JSON_PATH = ROOT / "data" / "admin" / "body_price_band_quality_fixup_v0.json"
APP_TEMPLATE = ROOT / "app" / "templates" / "index.html"


def load_module():
    spec = importlib.util.spec_from_file_location(
        "body_price_band_quality_fixup",
        SCRIPT_PATH,
    )
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


class BodyPriceBandQualityFixupTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.module = load_module()
        cls.payload = cls.module.build_payload()
        cls.rows = {row["query"]: row for row in cls.payload["rows"]}

    def test_default_decision_status_ready_for_owner_approved_push(self) -> None:
        self.assertEqual(
            self.payload["decision_status"],
            "body_price_band_quality_fixup_passed_ready_for_owner_approved_push",
        )

    def test_leica_m10_remains_body_and_band_is_cleaned(self) -> None:
        row = self.rows["Leica M10"]
        self.assertEqual(row["category"], "Body")
        self.assertFalse((row["display_price_band"] or "").startswith("KRW 80,000 -"))
        self.assertEqual(row["display_price_band"], "KRW 5,780,000 - 6,000,000")
        self.assertEqual(row["price_status"], "Body market summary is available.")
        self.assertEqual(row["display_unlock_requirements"], [])

    def test_leica_m10_accessories_and_variants_are_excluded(self) -> None:
        row = self.rows["Leica M10"]
        self.assertGreaterEqual(row["excluded_reason_counts"].get("accessory", 0), 1)
        self.assertGreaterEqual(row["excluded_reason_counts"].get("variant_boundary", 0), 1)
        evidence = row["display_top_result_evidence"]
        self.assertTrue(any("홀스터" in str(item.get("title")) and "Accessory, not camera/lens" in " ".join(item.get("excluded_reason") or []) for item in evidence))
        self.assertTrue(any("Monochrom" in str(item.get("title")) and "Variant boundary" in " ".join(item.get("excluded_reason") or []) for item in evidence))
        self.assertEqual(self.payload["leica_m10_investigation"]["m10_accessories_used_for_price"], [])

    def test_copy_summary_and_market_entry_copy_remain_human(self) -> None:
        text = APP_TEMPLATE.read_text(encoding="utf-8")
        self.assertIn("Copy summary", text)
        self.assertIn("Price evidence", text)
        self.assertNotIn("Need cleaner exact evidence", text)

    def test_body_guard_queries_remain_body(self) -> None:
        for query in ["leica m5", "Leica M6", "Leica M9", "Leica M11"]:
            self.assertEqual(self.rows[query]["category"], "Body", query)

    def test_lens_guard_queries_do_not_regress(self) -> None:
        self.assertEqual(self.rows["35 lux aa"]["category"], "Lens")
        self.assertEqual(self.rows["Noctilux 50 f1 E60"]["category"], "Lens")
        self.assertEqual(self.rows["Summicron 50 rigid"]["category"], "Lens")
        self.assertEqual(self.rows["M50/1.2"]["category"], "Lens")
        self.assertEqual(self.rows["Leica M50/1.2 1세대"]["category"], "Lens")
        self.assertEqual(self.rows["APO-Summicron-SL 90"]["category"], "Lens")

    def test_script_generates_pass_payload(self) -> None:
        subprocess.run([sys.executable, str(SCRIPT_PATH)], cwd=ROOT, check=True, capture_output=True, text=True)
        payload = json.loads(JSON_PATH.read_text(encoding="utf-8"))
        self.assertEqual(
            payload["decision_status"],
            "body_price_band_quality_fixup_passed_ready_for_owner_approved_push",
        )
        self.assertEqual(payload["price_projection_regressions"], [])
        self.assertEqual(payload["body_lens_regressions"], [])
        self.assertEqual(payload["ui_copy_regressions"], [])

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
            "body_price_band_quality_fixup_pushed_ready_for_owner_recheck",
        )


if __name__ == "__main__":
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(BodyPriceBandQualityFixupTests)
    result = unittest.TextTestRunner(verbosity=0).run(suite)
    if result.wasSuccessful():
        print(f"ok ({result.testsRun} tests)")
    raise SystemExit(0 if result.wasSuccessful() else 1)
