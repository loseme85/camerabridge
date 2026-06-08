from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = ROOT / "scripts" / "run_p3_beta_mvp_lens_variant_token_parser_coverage_fixup.py"
JSON_PATH = ROOT / "data" / "admin" / "lens_variant_token_parser_coverage_fixup_v0.json"
APP_TEMPLATE = ROOT / "app" / "templates" / "index.html"

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from api.search import search_from_params
from query_parser import parse_query


def load_module():
    spec = importlib.util.spec_from_file_location("lens_variant_token_parser_coverage_fixup", SCRIPT_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


class LensVariantTokenParserCoverageFixupTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.module = load_module()
        cls.payload = cls.module.build_payload()
        cls.rows = {row["query"]: row for row in cls.payload["rows"]}

    def test_default_decision_status_ready(self) -> None:
        self.assertEqual(
            self.payload["decision_status"],
            "lens_variant_token_parser_coverage_fixup_passed_ready_for_owner_approved_push",
        )

    def test_pre_asph_split_normalizes_to_pre_asph(self) -> None:
        intent = parse_query("pre asph summilux 35")
        self.assertEqual(intent["model_family"], "Summilux")
        self.assertEqual(intent["focal_length"], "35")
        self.assertIn("pre-ASPH", intent["variant"])
        self.assertNotIn("ASPH", [item for item in intent["variant"] if item != "pre-ASPH"])

    def test_spaced_8_element_variants_are_recognized(self) -> None:
        for query in ["35 cron 8 element", "summicron 35 8 element", "summicron 35 8매"]:
            with self.subTest(query=query):
                intent = parse_query(query)
                self.assertEqual(intent["model_family"], "Summicron")
                self.assertEqual(intent["focal_length"], "35")
                self.assertIn("8-element", intent["variant"])

    def test_hyphenated_family_aliases_and_fle_are_narrow(self) -> None:
        hyphen = parse_query("summilux-m 50 asph")
        self.assertEqual(hyphen["focal_length"], "50")
        self.assertTrue(str(hyphen["model_family"]).startswith("Summilux"))
        self.assertIn("ASPH", hyphen["variant"])

        fle = parse_query("fle summilux 35")
        self.assertEqual(fle["model_family"], "Summilux")
        self.assertEqual(fle["focal_length"], "35")
        self.assertIn("FLE", fle["variant"])

        short_fle = parse_query("35 lux fle")
        self.assertEqual(short_fle["model_family"], "Summilux")
        self.assertEqual(short_fle["focal_length"], "35")
        self.assertIn("FLE", short_fle["variant"])

        bare_fle = parse_query("fle")
        self.assertIsNone(bare_fle["model_family"])
        self.assertEqual(bare_fle["variant"], [])

    def test_wate_and_mate_shorthand_recover_tri_elmar_ranges(self) -> None:
        cases = {
            "wate": ("16-18-21", "WATE"),
            "mate": ("28-35-50", "MATE"),
            "tri-elmar 16-18-21": ("16-18-21", "WATE"),
            "tri-elmar 28-35-50": ("28-35-50", "MATE"),
            "16 18 21 tri elmar": ("16-18-21", "WATE"),
            "28 35 50 tri elmar": ("28-35-50", "MATE"),
        }
        for query, (focal, variant) in cases.items():
            with self.subTest(query=query):
                intent = parse_query(query)
                self.assertEqual(intent["model_family"], "Tri-Elmar")
                self.assertEqual(intent["focal_length"], focal)
                self.assertIn(variant, intent["variant"])

    def test_unsafe_broad_aliases_do_not_unlock_exact_price_by_themselves(self) -> None:
        for query in ["lux", "cron", "nocti", "E60", "1세대", "BP"]:
            with self.subTest(query=query):
                response = search_from_params({"q": query, "limit": "5"})
                self.assertFalse(response.get("display_price_summary_allowed"))

    def test_guard_queries_do_not_regress(self) -> None:
        self.assertEqual(search_from_params({"q": "M50/1.2 1세대", "limit": "5"})["results"][0]["display_output"]["display_category"], "Lens")
        self.assertEqual(search_from_params({"q": "Leica M10", "limit": "5"})["results"][0]["display_output"]["display_category"], "Body")
        self.assertFalse(str(search_from_params({"q": "Leica M10", "limit": "5"}).get("display_price_band") or "").startswith("KRW 80,000 -"))

        sl90 = search_from_params({"q": "APO-Summicron-SL 90", "limit": "5"})
        self.assertFalse(sl90.get("display_price_summary_allowed"))

        summilux = search_from_params({"q": "Summilux-M 50 ASPH", "limit": "5"})
        if summilux.get("display_price_summary_allowed"):
            self.assertEqual(summilux.get("top_result_compatibility"), "exact_variant_strong")
            self.assertFalse(summilux.get("third_party_top_domination_detected"))
        self.assertIn("Copy summary", APP_TEMPLATE.read_text(encoding="utf-8"))

    def test_script_generates_pass_payload(self) -> None:
        subprocess.run([sys.executable, str(SCRIPT_PATH)], cwd=ROOT, check=True, capture_output=True, text=True)
        payload = json.loads(JSON_PATH.read_text(encoding="utf-8"))
        self.assertEqual(
            payload["decision_status"],
            "lens_variant_token_parser_coverage_fixup_passed_ready_for_owner_approved_push",
        )
        self.assertEqual(payload["unsafe_broad_alias_regressions"], [])
        self.assertEqual(payload["pre_asph_regressions"], [])
        self.assertEqual(payload["tri_elmar_regressions"], [])
        self.assertEqual(payload["body_lens_regressions"], [])

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
            "lens_variant_token_parser_coverage_fixup_pushed_ready_for_owner_recheck",
        )


if __name__ == "__main__":
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(LensVariantTokenParserCoverageFixupTests)
    result = unittest.TextTestRunner(verbosity=0).run(suite)
    if result.wasSuccessful():
        print(f"ok ({result.testsRun} tests)")
    raise SystemExit(0 if result.wasSuccessful() else 1)
