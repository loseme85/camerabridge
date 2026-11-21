"""사장님 전용 분류 확인 화면: /owner/classify

모델의 갈래별 매물을 사진·가격과 함께 보여 주고, 매물마다 '이 갈래로' 버튼을 누르면 확정 목록
(data/config/entity_confirmed_v1.json, 상품 주소 → 갈래)에 저장한다. 저장은 GitHub 저장소 파일을 직접 고친다(GH_PAT).
다음 크롤링부터 그 갈래로 나온다 (entity_catalog.refine_by_description 이 규칙보다 먼저 적용).
들어가기: /owner/classify?key=<OWNER_DASHBOARD_KEY> 로 한 번 열면 쿠키가 남아 다음부터는 /owner/classify 만으로 열림.
"""
from __future__ import annotations

import base64
import hmac
import html
import json
import os
import sys
import urllib.error
import urllib.request
from http.cookies import SimpleCookie
from http.server import BaseHTTPRequestHandler
from pathlib import Path
from urllib.parse import parse_qs, urlencode, urlparse

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

COOKIE = "cb_owner"
GH_REPO = "loseme85/camerabridge"
CONFIRMED_FILE = "data/config/entity_confirmed_v1.json"
PAGE_SIZE = 80


def authorized(key: str, cookie_value: str) -> bool:
    expected = os.environ.get("OWNER_DASHBOARD_KEY", "")
    if len(expected) < 16:
        return False
    return any(value and hmac.compare_digest(value, expected) for value in (key, cookie_value))


def _esc(value) -> str:
    return html.escape(str(value if value is not None else ""), quote=True)


# ── 데이터 ──
def _catalog() -> dict:
    from entity_catalog import load_catalog
    return load_catalog()


def _records() -> list[dict]:
    from search_index import DEFAULT_SEARCH_INDEX_PATH, load_search_index
    for path in (Path(DEFAULT_SEARCH_INDEX_PATH), ROOT / "data/derived/results_search_index_v1.json"):
        if path.exists():
            return load_search_index(path)
    raise FileNotFoundError("검색 색인을 찾지 못했습니다")


def _gh(method: str, path: str, body: dict | None = None) -> dict:
    token = os.environ.get("GH_PAT", "")
    if not token:
        raise PermissionError("GH_PAT 가 설정되어 있지 않습니다")
    req = urllib.request.Request(
        f"https://api.github.com/repos/{GH_REPO}/{path}", method=method,
        data=json.dumps(body).encode() if body is not None else None,
        headers={"Authorization": f"token {token}", "Accept": "application/vnd.github+json", "User-Agent": "camerabridge-owner"})
    with urllib.request.urlopen(req, timeout=20) as resp:  # noqa: S310
        return json.loads(resp.read().decode("utf-8"))


def read_confirmed() -> tuple[dict, str | None]:
    """(확정 목록 전체, GitHub 파일 sha). 토큰이 없으면 배포된 파일을 읽고 sha 는 None."""
    try:
        data = _gh("GET", f"contents/{CONFIRMED_FILE}?ref=main")
        return json.loads(base64.b64decode(data["content"]).decode("utf-8")), data["sha"]
    except Exception:  # noqa: BLE001
        try:
            return json.loads((ROOT / CONFIRMED_FILE).read_text(encoding="utf-8")), None
        except (OSError, ValueError):
            return {"schema_version": "entity_confirmed_v1", "links": {}}, None


def save_confirmed(link: str, entity: str | None, note: str) -> str:
    """link 를 entity 로 확정(None 이면 해제). 저장 뒤 메시지."""
    doc, sha = read_confirmed()
    if sha is None:
        raise PermissionError("GitHub 에서 확정 목록을 읽지 못했습니다 (GH_PAT 권한 확인)")
    links = doc.setdefault("links", {})
    if entity:
        import datetime as dt
        links[link] = {"entity": entity, "by": "사장님", "at": dt.datetime.now(dt.timezone(dt.timedelta(hours=9))).date().isoformat(), "note": note[:80]}
    else:
        links.pop(link, None)
    text = json.dumps(doc, ensure_ascii=False, indent=1) + "\n"
    _gh("PUT", f"contents/{CONFIRMED_FILE}", {
        "message": ("분류 확정: " if entity else "분류 확정 해제: ") + link[:80],
        "content": base64.b64encode(text.encode("utf-8")).decode("ascii"), "sha": sha, "branch": "main"})
    return "저장했습니다. 다음 크롤링부터 반영됩니다." if entity else "확정을 해제했습니다."


# ── 화면 ──
def _won(value) -> str:
    return f"₩{int(round(value / 10000)):,}만" if value else "가격 없음"


def render(model: str, bucket: str, notice: str = "", error: str = "") -> str:
    from entity_catalog import price_krw
    catalog = _catalog()
    entities = catalog["entities"]
    records = _records()
    confirmed = read_confirmed()[0].get("links") or {}
    parents = sorted((e for e in entities.values() if len(e.get("children") or []) >= 2 and e["id"].startswith("leica:")),
                     key=lambda e: e["id"])
    counts: dict[str, int] = {}
    live = [r for r in records if (r.get("final_output") or {}).get("sold_quality") != "sold_confirmed"]
    for r in live:
        for e in r.get("entity_ids") or []:
            counts[e] = counts.get(e, 0) + 1
    head = ("<!doctype html><html lang=ko><meta charset=utf-8><meta name=viewport content='width=device-width,initial-scale=1'>"
            "<meta name=robots content=noindex><title>분류 확인</title><style>"
            "body{font:14px/1.5 system-ui,sans-serif;margin:0;background:#f6f4ef;color:#191715}main{max-width:1000px;margin:0 auto;padding:16px}"
            "h1{font-size:18px}a{color:#1f5473}.tabs a{display:inline-block;margin:2px 4px 2px 0;padding:4px 10px;border:1px solid #c7beb2;"
            "background:#fff;text-decoration:none;color:#191715}.tabs a.on{background:#191715;color:#fff}"
            ".item{display:flex;gap:12px;background:#fff;border:1px solid #d9d2c8;margin:8px 0;padding:10px}.item img{width:96px;height:96px;object-fit:cover;"
            "background:#ebe6de;flex:none}.meta{flex:1;min-width:0}.t{font-weight:600;word-break:break-word}.sub{color:#655d55;font-size:12px}"
            "form{display:inline}button{font:inherit;padding:3px 9px;margin:4px 4px 0 0;border:1px solid #c7beb2;background:#f1eee8;cursor:pointer}"
            "button.cur{background:#2e6d43;color:#fff;border-color:#2e6d43}.ok{background:#e4f0e7;padding:8px}.bad{background:#f7e1e1;padding:8px}"
            "</style><main><h1>분류 확인</h1>")
    out = [head]
    if notice:
        out.append(f"<p class=ok>{_esc(notice)}</p>")
    if error:
        out.append(f"<p class=bad>{_esc(error)}</p>")
    out.append("<form method=get action=/owner/classify><select name=model onchange='this.form.submit()'><option value=''>모델 고르기…</option>")
    for p in parents:
        out.append(f"<option value='{_esc(p['id'])}'{' selected' if p['id'] == model else ''}>{_esc(p.get('name_ko') or p.get('name'))} ({counts.get(p['id'], 0)})</option>")
    out.append("</select> <noscript><button>열기</button></noscript></form>")
    parent = entities.get(model)
    if not parent:
        out.append("<p>모델을 고르면 갈래별 매물이 나옵니다.</p></main>")
        return "".join(out)
    kids = [entities[c] for c in parent.get("children") or [] if c in entities]
    if bucket not in {k["id"] for k in kids}:
        bucket = next((k["id"] for k in kids if counts.get(k["id"])), kids[0]["id"] if kids else "")
    out.append("<div class=tabs>")
    for k in kids:
        out.append(f"<a class='{'on' if k['id'] == bucket else ''}' href='/owner/classify?{urlencode({'model': model, 'bucket': k['id']})}'>"
                   f"{_esc(k.get('name_ko') or k.get('name'))} ({counts.get(k['id'], 0)})</a>")
    out.append("</div>")
    items = [r for r in live if bucket in (r.get("entity_ids") or [])]
    # 확정 목록에서 이 갈래로 옮겨진 매물은 색인이 새로 만들어지기 전이라도 아래에 같이 보여 줌
    pending_here = [r for r in live if confirmed.get(str((r.get("raw_item") or {}).get("링크") or ""), {}).get("entity") == bucket and bucket not in (r.get("entity_ids") or [])]
    rows = sorted(items + pending_here, key=lambda r: price_krw(r["final_output"]) or 0)
    out.append(f"<p class=sub>{len(rows)}개 (가격 낮은 순, 최대 {PAGE_SIZE}개). 버튼을 누르면 그 갈래로 확정됩니다.</p>")
    for r in rows[:PAGE_SIZE]:
        f, raw = r["final_output"], r.get("raw_item") or {}
        link = str(raw.get("링크") or "")
        mine = (confirmed.get(link) or {}).get("entity")
        img = f.get("image_url") or ""
        out.append("<div class=item>")
        out.append(f"<img src='{_esc(img)}' loading=lazy alt=''>" if img.startswith("http") else "<img alt=''>")
        out.append("<div class=meta>")
        out.append(f"<div class=t><a href='{_esc(link)}' target=_blank rel='noopener noreferrer'>{_esc(f.get('title_raw'))}</a></div>")
        out.append(f"<div class=sub>{_won(price_krw(f))} · {_esc(raw.get('site'))}" + (" · 사장님 확정" if mine else "") + "</div>")
        for k in kids:
            on = (mine or bucket) == k["id"]
            out.append("<form method=post action=/owner/classify>"
                       f"<input type=hidden name=link value='{_esc(link)}'><input type=hidden name=entity value='{_esc(k['id'])}'>"
                       f"<input type=hidden name=model value='{_esc(model)}'><input type=hidden name=bucket value='{_esc(bucket)}'>"
                       f"<input type=hidden name=note value='{_esc((f.get('title_raw') or '')[:60])}'>"
                       f"<button class='{'cur' if on else ''}'>{_esc(k.get('name_ko') or k.get('name'))}</button></form>")
        if mine:
            out.append("<form method=post action=/owner/classify>"
                       f"<input type=hidden name=link value='{_esc(link)}'><input type=hidden name=clear value=1>"
                       f"<input type=hidden name=model value='{_esc(model)}'><input type=hidden name=bucket value='{_esc(bucket)}'>"
                       "<button>확정 해제</button></form>")
        out.append("</div></div>")
    out.append("</main>")
    return "".join(out)


class handler(BaseHTTPRequestHandler):
    def _auth(self) -> tuple[bool, str]:
        key = (parse_qs(urlparse(self.path).query).get("key") or [""])[0]
        cookie = SimpleCookie(self.headers.get("cookie") or "")
        return authorized(key, cookie[COOKIE].value if COOKIE in cookie else ""), key

    def _send(self, status: int, body: str, headers: dict | None = None) -> None:
        data = body.encode("utf-8")
        self.send_response(status)
        self.send_header("content-type", "text/html; charset=utf-8")
        self.send_header("cache-control", "no-store")
        self.send_header("x-robots-tag", "noindex, nofollow")
        self.send_header("x-frame-options", "DENY")
        for name, value in (headers or {}).items():
            self.send_header(name, value)
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):  # noqa: N802
        ok, key = self._auth()
        if not ok:
            return self._send(401, "<!doctype html><meta charset=utf-8><meta name=robots content=noindex><p>권한이 없습니다. /owner/classify?key=… 로 열어 주세요.</p>")
        if key:
            return self._send(302, "", {"location": "/owner/classify",
                                        "set-cookie": f"{COOKIE}={key}; Path=/owner; Max-Age=7776000; HttpOnly; Secure; SameSite=Lax"})
        q = parse_qs(urlparse(self.path).query)
        try:
            return self._send(200, render((q.get("model") or [""])[0], (q.get("bucket") or [""])[0], (q.get("ok") or [""])[0], (q.get("err") or [""])[0]))
        except Exception as error:  # noqa: BLE001
            return self._send(500, f"<!doctype html><meta charset=utf-8><p>화면을 만들지 못했습니다: {_esc(type(error).__name__)}</p>")

    def do_POST(self):  # noqa: N802
        ok, _ = self._auth()
        host = self.headers.get("host") or ""
        origin = urlparse(self.headers.get("origin") or "").netloc
        if not ok or (origin and origin != host):  # 다른 사이트에서 보낸 요청은 거절
            return self._send(401, "<p>권한이 없습니다.</p>")
        length = min(int(self.headers.get("content-length") or 0), 20_000)
        form = {k: v[0] for k, v in parse_qs(self.rfile.read(length).decode("utf-8", "replace")).items()}
        link, entity = form.get("link", ""), form.get("entity", "")
        back = {"model": form.get("model", ""), "bucket": form.get("bucket", "")}
        try:
            if not link.startswith(("http://", "https://")):
                raise ValueError("주소가 이상합니다")
            if form.get("clear"):
                back["ok"] = save_confirmed(link, None, "")
            else:
                if entity not in _catalog()["entities"]:
                    raise ValueError("없는 갈래입니다")
                back["ok"] = save_confirmed(link, entity, form.get("note", ""))
        except urllib.error.HTTPError as error:
            back["err"] = f"저장하지 못했습니다 (GitHub {error.code}). " + ("GH_PAT 에 이 저장소 파일 쓰기 권한이 필요합니다." if error.code in (403, 404) else "잠시 뒤 다시 해 주세요.")
        except Exception as error:  # noqa: BLE001
            back["err"] = f"저장하지 못했습니다: {error}"[:200]
        return self._send(303, "", {"location": "/owner/classify?" + urlencode(back)})
