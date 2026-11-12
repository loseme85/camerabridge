"""used-photo.de 제목 다듬기: 앞부분이 이름, 머리말('Leica 20002 –'·'Leica Prime –')일 때만 다음 부분.
2026-11-12: 'Leica Leicavit M – 14009 | M7 M6 MP'가 맞는 카메라 목록으로 바뀌어 M7 검색에 섞임."""
import ast
import re
from pathlib import Path


def _load():
    src = Path(__file__).resolve().parents[1].joinpath("app/test.py").read_text(encoding="utf-8")
    node = next(n for n in ast.parse(src).body if isinstance(n, ast.FunctionDef) and n.name == "_usedphoto_name")
    ns = {"re": re}
    exec(compile(ast.Module(body=[node], type_ignores=[]), "app/test.py", "exec"), ns)
    return ns["_usedphoto_name"]


def test_accessory_keeps_its_name_not_compatible_bodies():
    f = _load()
    assert f("Leica Leicavit M Black Paint – 14009 | M7 M6 MP M4 M4-P M4-2") == "Leica Leicavit M Black Paint 14009"
    assert f("Leica 18767 Visoflex 020 – M10 TL TL2 X Typ 113") == "Leica 18767 Visoflex 020"
    assert f("Leica CF Titan Blitz – f. Minilux Zoom |") == "Leica CF Titan Blitz"


def test_prefix_parts_are_skipped():
    f = _load()
    assert f("LEICA 20002 – Leica M10-R") == "Leica M10-R 20002"
    assert f("Leica Prime – Leica APO-Summicron-M 35mm f2 ASPH. | 11699") == "Leica APO-Summicron-M 35mm f2 ASPH. 11699"
    assert f("Leica Steel Rim 2026 – Leica Summilux-M 35mm f1.4 – 11301") == "Leica Summilux-M 35mm f1.4 11301"
    assert f("Full Service – Leica M4-2 Black Chrome – 10410 |") == "Leica M4-2 Black Chrome 10410"
