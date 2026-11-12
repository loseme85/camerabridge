"""사라진 옛 모델 주소는 가장 가까운 지금 페이지로 넘김 (2026-11-12 구글 서치 콘솔 404: summilux-m-35-v1)"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
from build_model_pages import redirect_page, redirect_target  # noqa: E402


def test_target_is_closest_live_parent():
    live = {"summilux-m-35", "summilux-m-35-v1-steel-rim", "m6"}
    assert redirect_target("summilux-m-35-v1", live) == "summilux-m-35"
    assert redirect_target("m6-something-old", live) == "m6"
    assert redirect_target("nothing-here", live) == ""


def test_redirect_page_moves_at_once():
    page = redirect_page("https://camerabridge.io/ko/leica/summilux-m-35/")
    assert 'http-equiv="refresh" content="0; url=https://camerabridge.io/ko/leica/summilux-m-35/"' in page
    assert 'rel="canonical" href="https://camerabridge.io/ko/leica/summilux-m-35/"' in page
