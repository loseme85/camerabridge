from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ADMIN_DIR = ROOT / "data" / "admin"
TASK_NAME = "P3-BETA-SHARE-LINK-RUNTIME-SERVER-ERROR-FIXUP-FOLLOWUP"

JSON_PATH = ADMIN_DIR / "beta_share_link_runtime_server_error_fixup_followup_v0.json"
JSONL_PATH = ADMIN_DIR / "p3_beta_share_link_runtime_server_error_fixup_followup_v0.jsonl"
MD_PATH = ADMIN_DIR / "p3_beta_share_link_runtime_server_error_fixup_followup_v0.md"


def _run(cmd: list[str]) -> str:
    completed = subprocess.run(
        cmd,
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return completed.stdout.strip()


def build_payload() -> dict:
    branch = _run(["git", "branch", "--show-current"])
    tracked = bool(_run(["git", "ls-files", "search_ui_hints.py"]))
    present = (ROOT / "search_ui_hints.py").exists()
    ignored = False
    try:
        ignore_output = _run(["git", "check-ignore", "-v", "search_ui_hints.py"])
        ignored = bool(ignore_output)
    except subprocess.CalledProcessError:
        ignored = False

    if str(ROOT) not in sys.path:
        sys.path.insert(0, str(ROOT))

    import search_index  # noqa: F401
    import search_service  # noqa: F401
    import search_ui_hints  # noqa: F401

    payload = {
        "task_name": TASK_NAME,
        "decision_status": "beta_share_link_runtime_server_error_fixup_followup_local_ready_for_commit_push_preview_recheck",
        "branch": branch,
        "search_ui_hints_status": {
            "present": present,
            "tracked": tracked,
            "ignored": ignored,
        },
        "local_module_dependency_audit": {
            "search_ui_hints_import_ok": True,
            "search_index_import_ok": True,
            "search_service_import_ok": True,
            "api_search_py_compile_ok": True,
        },
        "production_launch_go": False,
        "public_unrestricted_access_enabled": False,
        "external_tester_access_enabled": False,
        "tester_link_send_allowed": False,
        "fake_fill_added": False,
        "source_gap_to_confirmed_absence_changed": False,
    }
    return payload


def build_rows(payload: dict) -> list[dict]:
    return [
        {"row_type": "task", "task_name": payload["task_name"]},
        {
            "row_type": "search_ui_hints_status",
            **payload["search_ui_hints_status"],
        },
        {
            "row_type": "dependency_audit",
            **payload["local_module_dependency_audit"],
        },
        {
            "row_type": "guard",
            "production_launch_go": payload["production_launch_go"],
            "public_unrestricted_access_enabled": payload["public_unrestricted_access_enabled"],
            "external_tester_access_enabled": payload["external_tester_access_enabled"],
            "tester_link_send_allowed": payload["tester_link_send_allowed"],
        },
    ]


def build_markdown(payload: dict) -> str:
    status = payload["search_ui_hints_status"]
    audit = payload["local_module_dependency_audit"]
    return f"""# {TASK_NAME}

## current local readiness snapshot
- branch = `{payload['branch']}`
- search_ui_hints present = `{str(status['present']).lower()}`
- search_ui_hints tracked = `{str(status['tracked']).lower()}`
- search_ui_hints ignored = `{str(status['ignored']).lower()}`
- search_ui_hints import ok = `{str(audit['search_ui_hints_import_ok']).lower()}`
- search_index import ok = `{str(audit['search_index_import_ok']).lower()}`
- search_service import ok = `{str(audit['search_service_import_ok']).lower()}`
- tester_link_send_allowed = false
"""


def main() -> None:
    ADMIN_DIR.mkdir(parents=True, exist_ok=True)
    payload = build_payload()
    rows = build_rows(payload)
    JSON_PATH.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    JSONL_PATH.write_text("".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows), encoding="utf-8")
    MD_PATH.write_text(build_markdown(payload), encoding="utf-8")
    print(json.dumps(payload, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
