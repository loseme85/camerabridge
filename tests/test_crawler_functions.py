"""수집 함수가 모두 결과를 돌려주는지 (2026-11-06: PR을 합치며 충돌을 정리하다 crawl_fotogoerlitz의
'return results'가 빠져 크롤에서 0건으로 실패함 — 문법 검사로는 안 잡혀서 테스트로 막음)"""
import ast
from pathlib import Path


def test_every_crawler_returns_value():
    tree = ast.parse(Path(__file__).resolve().parents[1].joinpath("app/test.py").read_text(encoding="utf-8"))
    missing = [
        node.name for node in tree.body
        if isinstance(node, ast.FunctionDef) and node.name.startswith("crawl_")
        and not any(isinstance(x, ast.Return) and x.value is not None for x in ast.walk(node))
    ]
    assert missing == []
