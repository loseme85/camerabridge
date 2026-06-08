from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = ROOT / "scripts" / "run_p3_beta_mvp_lens_boundary_conflict_resolution_fixup.py"
JSON_PATH = ROOT / "data" / "admin" / "lens_boundary_conflict_resolution_fixup_v0.json"

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from api.search import search_from_params


def load_module():
    spec = importlib.util.spec_from_file_location("lens_boundary_conflict_resolution_fixup", SCRIPT_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


class LensBoundaryConflictResolutionFixupTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.module = load_module()
        cls.payload = cls.module.build_payload()
        cls.rows = {row["query"]: row for row in cls.payload["rows"]}

    def test_default_decision_status_ready(self) -> None:
        self.assertEqual(
            self.payload["decision_status"],
            "lens_boundary_conflict_resolution_fixup_passed_ready_for_owner_approved_push",
        )

    def test_summilux_m_50_asph_stays_safe_against_third_party_contamination(self) -> None:
        row = self.rows["Summilux-M 50 ASPH"]
        self.assertEqual(row["body_or_lens_path"], "Lens")
        if row["display_price_summary_allowed"]:
            self.assertEqual(row["top_result_compatibility"], "exact_variant_strong")
            self.assertFalse(row["third_party_top_domination_detected"])
            self.assertFalse(row["boundary_conflict_detected"])
        else:
            self.assertTrue(row["third_party_top_domination_detected"])
        third_party_rows = [
            item
            for item in row["display_top_result_evidence"]
            if "voigtlander" in str(item.get("title") or "").lower() or "nokton" in str(item.get("title") or "").lower()
        ]
        for item in third_party_rows:
            self.assertFalse(item.get("used_for_price"))
            self.assertNotIn(item.get("compatibility_label"), {"Broader family", "Exact base model", "Exact variant"})

    def test_apo_summicron_sl_90_stays_locked_and_never_uses_wrong_mount_rows(self) -> None:
        row = self.rows["APO-Summicron-SL 90"]
        self.assertEqual(row["body_or_lens_path"], "Lens")
        self.assertFalse(row["display_price_summary_allowed"])
        offenders = [
            item
            for item in row["display_top_result_evidence"]
            if any(token in str(item.get("title") or "") for token in ["Leica M 90", "Leica R 90", "Summarit", "Elmarit", "TTArtisan", "Leica L 90"])
        ]
        for item in offenders:
            self.assertFalse(item.get("used_for_price"))
            self.assertIn(item.get("compatibility_label"), {"Boundary conflict", "Query incompatible"})

    def test_primary_shorthand_sl90_queries_stay_reference_only(self) -> None:
        for query in ["apo summicron sl 90", "leica sl 90 apo summicron"]:
            with self.subTest(query=query):
                row = self.rows[query]
                self.assertEqual(row["body_or_lens_path"], "Lens")
                self.assertFalse(row["display_price_summary_allowed"])
                self.assertTrue(row["display_broader_reference_allowed"])

    def test_existing_pass_cases_hold(self) -> None:
        rigid = self.rows["Summicron 50 rigid"]
        self.assertEqual(rigid["body_or_lens_path"], "Lens")
        self.assertTrue(rigid["display_price_summary_allowed"])
        self.assertEqual(rigid["display_price_scope_label"], "Exact variant price")

        m5012 = self.rows["M50/1.2"]
        self.assertEqual(m5012["body_or_lens_path"], "Lens")
        self.assertFalse(m5012["display_price_summary_allowed"])

        for query in ["leica m5", "Leica M6", "Leica M9", "Leica M10", "Leica M11"]:
            with self.subTest(query=query):
                self.assertEqual(self.rows[query]["body_or_lens_path"], "Body")
        self.assertFalse(str(self.rows["Leica M10"]["display_price_band"] or "").startswith("KRW 80,000 -"))

    def test_ui_copy_guard_holds(self) -> None:
        self.assertEqual(self.payload["ui_copy_regressions"], [])
        template_text = (ROOT / "app" / "templates" / "index.html").read_text(encoding="utf-8")
        self.assertIn("Copy summary", template_text)
        for forbidden in [
            "exact_variant / cleaned",
            "exact_base_model / cleaned",
            "broader_family / cleaned",
            "Need no third-party contamination in the selected price pool.",
            "Need exact or strong compatible visible Leica results.",
        ]:
            self.assertNotIn(forbidden, json.dumps(self.payload, ensure_ascii=False))

    def test_script_generates_pass_payload(self) -> None:
        subprocess.run([sys.executable, str(SCRIPT_PATH)], cwd=ROOT, check=True, capture_output=True, text=True)
        payload = json.loads(JSON_PATH.read_text(encoding="utf-8"))
        self.assertEqual(
            payload["decision_status"],
            "lens_boundary_conflict_resolution_fixup_passed_ready_for_owner_approved_push",
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
                "preview_deployment_url": "https://example.vercel.app",
                "preview_deployment_id": "dpl_test",
                "preview_deployment_state": "READY",
                "preview_branch": "beta-ui-redesign-controlled-preview",
                "preview_commit": self.payload["git_diff_summary"]["head_commit"],
            }
        )
        self.assertEqual(
            pushed["decision_status"],
            "lens_boundary_conflict_resolution_fixup_pushed_ready_for_owner_recheck",
        )


if __name__ == "__main__":
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(LensBoundaryConflictResolutionFixupTests)
    result = unittest.TextTestRunner(verbosity=0).run(suite)
    if result.wasSuccessful():
        print(f"ok ({result.testsRun} tests)")
    raise SystemExit(0 if result.wasSuccessful() else 1)
