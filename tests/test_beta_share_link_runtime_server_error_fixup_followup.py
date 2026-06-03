from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.run_p3_beta_share_link_runtime_server_error_fixup_followup import (  # noqa: E402
    build_payload,
    build_rows,
)


class FollowupLocalReadinessTest(unittest.TestCase):
    def setUp(self) -> None:
        self.payload = build_payload()
        self.rows = build_rows(self.payload)

    def test_task_name(self) -> None:
        self.assertEqual(
            self.payload["task_name"],
            "P3-BETA-SHARE-LINK-RUNTIME-SERVER-ERROR-FIXUP-FOLLOWUP",
        )

    def test_expected_branch(self) -> None:
        self.assertEqual(self.payload["branch"], "beta-ui-redesign-controlled-preview")

    def test_search_ui_hints_present(self) -> None:
        status = self.payload["search_ui_hints_status"]
        self.assertTrue(status["present"])
        self.assertFalse(status["ignored"])

    def test_search_ui_hints_tracked_after_commit(self) -> None:
        self.assertTrue(self.payload["search_ui_hints_status"]["tracked"])

    def test_local_dependency_audit(self) -> None:
        audit = self.payload["local_module_dependency_audit"]
        self.assertTrue(audit["search_ui_hints_import_ok"])
        self.assertTrue(audit["search_index_import_ok"])
        self.assertTrue(audit["search_service_import_ok"])
        self.assertTrue(audit["api_search_py_compile_ok"])

    def test_guard_values(self) -> None:
        self.assertFalse(self.payload["production_launch_go"])
        self.assertFalse(self.payload["public_unrestricted_access_enabled"])
        self.assertFalse(self.payload["external_tester_access_enabled"])
        self.assertFalse(self.payload["tester_link_send_allowed"])
        self.assertFalse(self.payload["fake_fill_added"])
        self.assertFalse(self.payload["source_gap_to_confirmed_absence_changed"])

    def test_rows_serializable(self) -> None:
        for row in self.rows:
            json.dumps(row, ensure_ascii=False)


if __name__ == "__main__":
    unittest.main()
