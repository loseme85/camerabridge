"""사장님 분류 확인 화면 (api/owner_classify.py, 2026-11-22) — 인증·화면·저장 요청 내용"""
from __future__ import annotations

import base64
import json
import threading
import urllib.error
import urllib.request
from http.server import HTTPServer

import pytest

from api import owner_classify as oc

KEY = "k" * 20


@pytest.fixture()
def server(monkeypatch):
    monkeypatch.setenv("OWNER_DASHBOARD_KEY", KEY)
    srv = HTTPServer(("127.0.0.1", 0), oc.handler)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    yield f"http://127.0.0.1:{srv.server_address[1]}"
    srv.shutdown()


def _get(url, cookie=None):
    req = urllib.request.Request(url, headers={"cookie": f"cb_owner={cookie}"} if cookie else {})
    try:
        with urllib.request.urlopen(req) as r:
            return r.status, r.read().decode("utf-8")
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode("utf-8")


def test_needs_key(server):
    assert _get(server + "/owner/classify")[0] == 401
    assert _get(server + "/owner/classify", "wrong-key-wrong-key-xx")[0] == 401


def test_page_lists_buckets_and_buttons(server):
    status, page = _get(server + "/owner/classify?model=leica:lens:summilux-m:35&bucket=leica:lens:summilux-m:35:v1-steel-rim", KEY)
    assert status == 200
    assert "스틸림" in page and "name=entity" in page and "name=link" in page


def test_save_writes_confirmed_file(monkeypatch):
    calls = []
    doc = {"schema_version": "entity_confirmed_v1", "links": {}}
    def fake_gh(method, path, body=None):
        calls.append((method, path, body))
        if method == "GET":
            return {"content": base64.b64encode(json.dumps(doc).encode()).decode(), "sha": "abc"}
        return {}
    monkeypatch.setattr(oc, "_gh", fake_gh)
    msg = oc.save_confirmed("https://x.example/a", "leica:lens:summilux-m:35:v1-steel-rim-goggles", "메모")
    assert "저장" in msg
    put = calls[-1]
    assert put[0] == "PUT" and put[2]["sha"] == "abc" and put[2]["branch"] == "main"
    saved = json.loads(base64.b64decode(put[2]["content"]))
    assert saved["links"]["https://x.example/a"]["entity"].endswith("v1-steel-rim-goggles")
    oc.save_confirmed("https://x.example/a", None, "")  # 해제는 같은 흐름으로 (doc 는 fake 라 그대로)


def test_post_rejects_foreign_origin_and_bad_input(server, monkeypatch):
    monkeypatch.setattr(oc, "save_confirmed", lambda *a, **k: "저장했습니다.")
    def post(data, origin=None):
        headers = {"cookie": f"cb_owner={KEY}", "content-type": "application/x-www-form-urlencoded"}
        if origin:
            headers["origin"] = origin
        req = urllib.request.Request(server + "/owner/classify", data=data.encode(), headers=headers, method="POST")
        class NoRedirect(urllib.request.HTTPRedirectHandler):
            def redirect_request(self, *a, **k):
                return None
        try:
            return urllib.request.build_opener(NoRedirect).open(req).status, ""
        except urllib.error.HTTPError as e:
            return e.code, e.headers.get("location", "")
    assert post("link=https://x/a&entity=leica:lens:summilux-m:35:v1-steel-rim", origin="https://evil.example")[0] == 401
    status, loc = post("link=javascript:alert(1)&entity=leica:lens:summilux-m:35:v1-steel-rim")
    assert status == 303 and "err=" in loc
    status, loc = post("link=https://x/a&entity=leica:lens:summilux-m:35:v1-steel-rim")
    assert status == 303 and "ok=" in loc
