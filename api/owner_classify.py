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
REVIEW_MAX = 150


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


UNSTATED = ("미표기", "표기 없음", "확인 필요", "not stated", "unspecified", "review")


def has_evidence(record: dict, bucket: str, catalog: dict) -> bool:
    """이 매물이 그 갈래라는 근거가 이미 있는가 — 사장님이 다시 볼 필요 없는 매물.
    ① 사장님 확정·설명 근거로 옮겨진 것 ② 갈래를 가르는 말(갈래 규칙의 셋째 패턴부터)이 제목에 모두 있는 것.
    '미표기·표기 없음·확인 필요' 갈래는 근거가 없는 것이 정의이므로 전부 확인 대상."""
    from entity_catalog import record_title
    reason = str(((record.get("final_output") or {}).get("bucket") or {}).get("reason") or "")
    if reason.startswith(("confirmed:", "desc:")):
        return True
    entity = catalog["entities"].get(bucket) or {}
    if any(word in f"{entity.get('name', '')} {entity.get('name_ko', '')}".lower() for word in UNSTATED):
        return False
    compiled = catalog["compiled"].get(bucket)
    if not compiled or len(compiled[1]) < 3:
        return False
    title = record_title(record)
    return all(p.search(title) for p in compiled[1][2:])


def _head(title: str) -> str:
    return ("<!doctype html><html lang=ko><meta charset=utf-8><meta name=viewport content='width=device-width,initial-scale=1'>"
            f"<meta name=robots content=noindex><title>{_esc(title)}</title><style>"
            "body{font:14px/1.5 system-ui,sans-serif;margin:0;background:#f6f4ef;color:#191715}main{max-width:1000px;margin:0 auto;padding:16px}"
            "h1{font-size:18px}h2{font-size:15px;margin:18px 0 4px}a{color:#1f5473}.tabs a{display:inline-block;margin:2px 4px 2px 0;padding:4px 10px;border:1px solid #c7beb2;"
            "background:#fff;text-decoration:none;color:#191715}.tabs a.on{background:#191715;color:#fff}"
            ".item{display:flex;gap:12px;background:#fff;border:1px solid #d9d2c8;margin:8px 0;padding:10px}.item img{width:96px;height:96px;object-fit:cover;"
            "background:#ebe6de;flex:none}.meta{flex:1;min-width:0}.t{font-weight:600;word-break:break-word}.sub{color:#655d55;font-size:12px}"
            "form{display:inline}button{font:inherit;padding:3px 9px;margin:4px 4px 0 0;border:1px solid #c7beb2;background:#f1eee8;cursor:pointer}"
            "button.copy{font-size:11px;padding:0 6px;margin:0 0 0 4px;font-weight:400}"
            "button.cur{background:#2e6d43;color:#fff;border-color:#2e6d43}.ok{background:#e4f0e7;padding:8px}.bad{background:#f7e1e1;padding:8px}"
            f"</style><main><h1>{_esc(title)}</h1>")


COPY_JS = ("<script>document.addEventListener('click',function(e){var b=e.target.closest('button.copy');if(!b)return;var t=b.getAttribute('data-copy')||'';"
           "function done(){var o=b.textContent;b.textContent='복사됨';setTimeout(function(){b.textContent=o},1200)}"
           "if(navigator.clipboard&&window.isSecureContext){navigator.clipboard.writeText(t).then(done)}"
           "else{var a=document.createElement('textarea');a.value=t;document.body.appendChild(a);a.select();try{document.execCommand('copy');done()}catch(x){}a.remove()}});</script>")


def _is_unstated(entity: dict) -> bool:
    text = f"{entity.get('id', '')} {entity.get('name', '')} {entity.get('name_ko', '')}".lower()
    return text.split(" ")[0].endswith(":review") or "unspecified" in text or any(w in text for w in UNSTATED[:4])


def _item_html(r: dict, kids: list[dict], model: str, bucket: str, confirmed: dict, show_all: bool = False) -> str:
    from entity_catalog import price_krw
    f, raw = r["final_output"], r.get("raw_item") or {}
    link = str(raw.get("링크") or "")
    mine = (confirmed.get(link) or {}).get("entity")
    img = f.get("image_url") or ""
    title = f.get("title_raw") or ""
    out = ["<div class=item>"]
    out.append(f"<img src='{_esc(img)}' loading=lazy alt=''>" if img.startswith("http") else "<img alt=''>")
    out.append("<div class=meta>")
    out.append(f"<div class=t><a href='{_esc(link)}' target=_blank rel='noopener noreferrer'>{_esc(title)}</a> "
               f"<button type=button class=copy data-copy='{_esc(title)}'>복사</button></div>")
    out.append(f"<div class=sub>{_won(price_krw(f))} · {_esc(raw.get('site'))}" + (" · 사장님 확정" if mine else "") + "</div>")
    hidden = (f"<input type=hidden name=model value='{_esc(model)}'><input type=hidden name=bucket value='{_esc(bucket)}'>"
              + ("<input type=hidden name=view value=review>" if model == "" else ""))
    for k in kids:
        on = (mine or bucket) == k["id"]
        out.append("<form method=post action=/owner/classify>"
                   f"<input type=hidden name=link value='{_esc(link)}'><input type=hidden name=entity value='{_esc(k['id'])}'>{hidden}"
                   f"<input type=hidden name=note value='{_esc(title[:60])}'>"
                   f"<button class='{'cur' if on else ''}'>{_esc(k.get('name_ko') or k.get('name'))}</button></form>")
    if mine:
        out.append("<form method=post action=/owner/classify>"
                   f"<input type=hidden name=link value='{_esc(link)}'><input type=hidden name=clear value=1>{hidden}"
                   "<button>확정 해제</button></form>")
    out.append("</div></div>")
    return "".join(out)


def render_review(notice: str = "", error: str = "") -> str:
    """모든 모델에서 '확인 필요·세대 미표기' 갈래에 있는 매물만 모아서 (사장님이 볼 것만)"""
    from entity_catalog import price_krw
    catalog = _catalog()
    entities = catalog["entities"]
    confirmed = read_confirmed()[0].get("links") or {}
    groups: dict[str, list[dict]] = {}
    for r in _records():
        if (r.get("final_output") or {}).get("sold_quality") == "sold_confirmed":
            continue
        link = str((r.get("raw_item") or {}).get("링크") or "")
        decided = confirmed.get(link, {}).get("entity")
        if decided and decided in entities and not _is_unstated(entities[decided]):
            continue  # 사장님이 이미 제대로 된 갈래로 확정함
        for e in r.get("entity_ids") or []:
            ent = entities.get(e)
            if ent and not ent.get("children") and ent.get("parent") in entities and _is_unstated(ent):
                groups.setdefault(ent["parent"], []).append(r)
                break
    out = [_head("확인 필요 모아 보기")]
    if notice:
        out.append(f"<p class=ok>{_esc(notice)}</p>")
    if error:
        out.append(f"<p class=bad>{_esc(error)}</p>")
    total = sum(len(v) for v in groups.values())
    out.append(f"<p><a href='/owner/classify'>← 모델별로 보기</a> · 확인 필요 {total}개 ({len(groups)}개 모델), 모델마다 가격 낮은 순</p>")
    shown = 0
    for parent_id, rows in sorted(groups.items(), key=lambda kv: -len(kv[1])):
        parent = entities[parent_id]
        kids = [entities[c] for c in parent.get("children") or [] if c in entities]
        out.append(f"<h2><a href='/owner/classify?{urlencode({'model': parent_id})}'>{_esc(parent.get('name_ko') or parent.get('name'))}</a> ({len(rows)})</h2>")
        for r in sorted(rows, key=lambda x: price_krw(x["final_output"]) or 0):
            if shown >= REVIEW_MAX:
                break
            out.append(_item_html(r, kids, "", next((k["id"] for k in kids if _is_unstated(k)), ""), confirmed))
            shown += 1
    if shown < total:
        out.append(f"<p class=sub>{total - shown}개는 더 있습니다 (위쪽을 처리하면 나옵니다).</p>")
    out.append(COPY_JS + "</main>")
    return "".join(out)


def render(model: str, bucket: str, notice: str = "", error: str = "", show_all: bool = False) -> str:
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
    out = [_head("분류 확인")]
    if notice:
        out.append(f"<p class=ok>{_esc(notice)}</p>")
    if error:
        out.append(f"<p class=bad>{_esc(error)}</p>")
    out.append("<form method=get action=/owner/classify><select name=model onchange='this.form.submit()'><option value=''>모델 고르기…</option>")
    for p in parents:
        out.append(f"<option value='{_esc(p['id'])}'{' selected' if p['id'] == model else ''}>{_esc(p.get('name_ko') or p.get('name'))} ({counts.get(p['id'], 0)})</option>")
    out.append("</select> <noscript><button>열기</button></noscript></form>")
    out.append("<p><a href='/owner/classify?view=review'>확인 필요한 것만 모아 보기 (모든 모델)</a></p>")
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
    total = len(rows)
    if not show_all:  # 근거가 이미 있는 매물은 숨김 (사장님이 볼 것만)
        rows = [r for r in rows if not has_evidence(r, bucket, catalog)]
    base = urlencode({"model": model, "bucket": bucket})
    toggle = (f"<a href='/owner/classify?{base}'>확인할 것만 보기</a>" if show_all else f"<a href='/owner/classify?{base}&all=1'>근거 있는 것까지 전부 보기</a>")
    out.append(f"<p class=sub>{'전체 ' if show_all else '확인할 것 '}{len(rows)}개"
               + ("" if show_all else f" (제목·설명에 근거가 있는 {total - len(rows)}개는 숨김, 전체 {total}개)")
               + f" · 가격 낮은 순, 최대 {PAGE_SIZE}개 · {toggle}</p>")
    for r in rows[:PAGE_SIZE]:
        out.append(_item_html(r, kids, model, bucket, confirmed))
    out.append(COPY_JS)
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
            if (q.get("view") or [""])[0] == "review":
                return self._send(200, render_review((q.get("ok") or [""])[0], (q.get("err") or [""])[0]))
            return self._send(200, render((q.get("model") or [""])[0], (q.get("bucket") or [""])[0], (q.get("ok") or [""])[0], (q.get("err") or [""])[0], bool((q.get("all") or [""])[0])))
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
        if form.get("all"):
            back["all"] = "1"
        if form.get("view") == "review":
            back = {"view": "review"}
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
