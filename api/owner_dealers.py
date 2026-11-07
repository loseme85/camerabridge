"""사장님 전용 딜러 계정 관리: /owner/dealers

계정 만들기(임시 비밀번호는 만든 화면에서 한 번만 보임) · 비밀번호 다시 만들기 · 끄기/켜기.
들어가기: /owner/usage 와 같은 쿠키(cb_owner). 처음이면 /owner/dealers?key=<OWNER_DASHBOARD_KEY>
딜러는 /dealer/login 에서 받은 아이디·비밀번호로 들어가고, 계정에 묶인 매장만 '내 매장'으로 본다.
"""
from __future__ import annotations

import gzip
import html
import json
import sys
from http.cookies import SimpleCookie
from http.server import BaseHTTPRequestHandler
from pathlib import Path
from urllib.parse import parse_qs, urlparse

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
import dealer_portal as portal  # noqa: E402
from api.owner_usage import COOKIE, authorized  # noqa: E402

DATA = ROOT / "data/dealer/dealer_data.json.gz"
LANGS = {"ko": "한국어", "en": "English", "ja": "日本語", "zh-Hans": "简体中文", "zh-Hant": "繁體中文",
         "de": "Deutsch", "fr": "Français", "it": "Italiano", "es": "Español", "pt": "Português"}
COUNTRY_LANG = {"KR": "ko", "JP": "ja", "CN": "zh-Hans", "TW": "zh-Hant", "HK": "zh-Hant", "DE": "de", "AT": "de", "CH": "de",
                "FR": "fr", "LU": "fr", "IT": "it", "ES": "es", "PT": "pt", "BR": "pt"}
ERRORS = {"id": "아이디는 영문 소문자·숫자·-·_ 3~32자로 써 주세요.", "exists": "같은 아이디가 이미 있습니다.",
          "stores": "묶을 매장을 고르거나, 매장 없이 만들 때는 나라를 골라 주세요.", "missing": "없는 계정입니다."}


def sites() -> dict[str, dict]:
    try:
        return json.loads(gzip.decompress(DATA.read_bytes()))["sites"]
    except (OSError, ValueError, KeyError):
        return {}


def render(accounts: dict, site_info: dict, notice: str = "", error: str = "") -> str:
    e = html.escape
    rows = []
    for account_id, a in sorted(accounts.items()):
        state = "꺼짐" if a.get("disabled") else "사용 중"
        toggle = "켜기" if a.get("disabled") else "끄기"
        stores = "모든 매장 (사장님)" if a.get("admin") else ", ".join(a.get("stores") or []) or "매장 없음 (나라 기준)"
        rows.append(f"""<tr{' class="off"' if a.get("disabled") else ""}>
<td><b>{e(account_id)}</b><div class="sub">{e(a.get("name") or "")}</div></td>
<td>{e(stores)}</td><td>{e(a.get("country") or "–")} · {e(LANGS.get(a.get("lang") or "", "–"))}</td>
<td class="sub">{e((a.get("last_login") or "–").replace("T", " ")[:16])}</td><td>{state}</td>
<td class="acts"><form method="post"><input type="hidden" name="do" value="reset"><input type="hidden" name="id" value="{e(account_id)}"><button>비밀번호 다시 만들기</button></form>
<form method="post"><input type="hidden" name="do" value="{"enable" if a.get("disabled") else "disable"}"><input type="hidden" name="id" value="{e(account_id)}"><button>{toggle}</button></form></td></tr>""")
    ordered = sorted(site_info.items(), key=lambda kv: (kv[1].get("country") != "KR", kv[1].get("country") or "ZZ", kv[0]))
    store_opts = "".join(f'<option value="{e(name)}" data-country="{e(v.get("country") or "")}">{e(name)} · {e(v.get("country") or "?")} · 판매 중 {v.get("act", 0)}</option>'
                         for name, v in ordered if v.get("country"))
    countries = sorted({v.get("country") for v in site_info.values() if v.get("country")})
    country_opts = "".join(f'<option value="{c}">{c}</option>' for c in countries)
    lang_opts = "".join(f'<option value="{k}">{v}</option>' for k, v in LANGS.items())
    banner = (f'<div class="notice">{notice}</div>' if notice else "") + (f'<div class="error">{e(error)}</div>' if error else "")
    table = (f"""<table><thead><tr><th>아이디·매장명</th><th>묶인 매장</th><th>나라·언어</th><th>마지막 로그인</th><th>상태</th><th></th></tr></thead>
<tbody>{"".join(rows)}</tbody></table>""" if rows else '<p class="sub">아직 만든 계정이 없습니다.</p>')
    return f"""<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>딜러 계정 · Camera Bridge</title><meta name="robots" content="noindex,nofollow">
<style>
:root{{--border:#e1e4e3;--strong:#c9cecc;--text:#16181a;--soft:#5d6266;--accent:#1f4a3a}}
*{{box-sizing:border-box}}body{{margin:0;font:14px/1.5 -apple-system,BlinkMacSystemFont,"Apple SD Gothic Neo",sans-serif;color:var(--text);background:#fff}}
main{{max-width:1100px;margin:0 auto;padding:20px 16px 48px}}h1{{font-size:22px;margin:0 0 4px}}h2{{font-size:15px;margin:28px 0 8px;padding-bottom:6px;border-bottom:1px solid var(--text)}}
.sub{{color:var(--soft);font-size:12px}}table{{width:100%;border-collapse:collapse}}th,td{{text-align:left;border-bottom:1px solid var(--border);padding:7px 8px 7px 0;vertical-align:top}}
th{{color:var(--soft);font-weight:500;font-size:12px}}tr.off td{{color:var(--soft)}}.acts{{white-space:nowrap}}.acts form{{display:inline}}
button{{font:inherit;border:1px solid var(--strong);background:#fff;padding:3px 8px;cursor:pointer;margin:0 4px 4px 0}}button:hover{{border-color:var(--accent);color:var(--accent)}}
.grid{{display:grid;grid-template-columns:140px minmax(0,1fr);gap:8px 12px;align-items:start;max-width:720px}}
input,select{{font:inherit;padding:5px 8px;border:1px solid var(--strong);width:100%;max-width:420px;background:#fff}}select[multiple]{{height:220px}}
.go{{background:var(--accent);color:#fff;border-color:var(--accent);padding:6px 16px;margin-top:8px}}
.notice{{border:1px solid var(--accent);padding:10px 12px;margin:12px 0;background:#eef3f1}}.notice code{{font-size:16px;font-weight:700}}
.error{{border:1px solid #9b2c22;color:#9b2c22;padding:10px 12px;margin:12px 0}}
nav a{{color:var(--accent);margin-right:12px}}
</style></head><body><main>
<nav><a href="/owner/usage">방문 현황</a><a href="/dealer" target="_blank">딜러 화면 열기</a></nav>
<h1>딜러 계정</h1>
<p class="sub">딜러는 <b>camerabridge.io/dealer/login</b> 에서 아이디·비밀번호로 들어갑니다. 계정에 묶인 매장이 '내 매장'이 되고, 다른 매장으로 바꿀 수 없습니다.
기준가·통화·예상 총액은 계정 나라 기준입니다. 비밀번호를 다시 만들거나 끄면 그 계정의 기존 로그인은 1분 안에 끊깁니다.</p>
{banner}
<h2>계정 목록</h2>
{table}
<h2>새 계정</h2>
<form method="post" class="grid">
<input type="hidden" name="do" value="create">
<label for="nid">아이디</label><div><input id="nid" name="id" required pattern="[a-z0-9][a-z0-9_\\-]{{2,31}}" placeholder="예: chungmuro"><div class="sub">영문 소문자·숫자. 딜러가 로그인할 때 씀</div></div>
<label for="nname">매장명</label><input id="nname" name="name" placeholder="예: 라이카스토어 충무로">
<label for="nstores">묶을 매장</label><div><select id="nstores" name="stores" multiple>{store_opts}</select><div class="sub">수집 중인 매장 이름. 여러 곳은 ⌘ 누르고 고르기. 수집 매장이 없는 딜러(사장님 본인·개인 판매자)는 비워 두고 아래 나라를 고르기</div></div>
<label for="ncountry">나라</label><div><select id="ncountry" name="country"><option value="">첫 매장 나라</option>{country_opts}</select></div>
<label for="nlang">기본 언어</label><div><select id="nlang" name="lang"><option value="">나라에 맞게</option>{lang_opts}</select><div class="sub">딜러가 화면에서 언제든 바꿀 수 있음</div></div>
<label for="nadmin">사장님 계정</label><label><input id="nadmin" type="checkbox" name="admin" value="1" style="width:auto"> 모든 매장을 골라 볼 수 있게 (시연용)</label>
<span></span><button class="go">계정 만들기</button>
</form>
</main></body></html>"""


def handle_post(form: dict, site_info: dict) -> tuple[str, str]:
    """(알림 HTML, 오류 문구)"""
    action = (form.get("do") or [""])[0]
    account_id = (form.get("id") or [""])[0].strip().lower()
    e = html.escape
    try:
        if action == "create":
            stores = [s for s in form.get("stores", []) if s in site_info]
            country = (form.get("country") or [""])[0] or (site_info[stores[0]].get("country") if stores else "") or ""
            lang = (form.get("lang") or [""])[0] or COUNTRY_LANG.get(country, "en")
            password = portal.create_account(account_id, name=(form.get("name") or [""])[0], stores=stores,
                                             country=country, lang=lang, admin=bool(form.get("admin")))
            return (f"<b>{e(account_id)}</b> 계정을 만들었습니다. 임시 비밀번호: <code>{e(password)}</code><br>"
                    "이 화면을 벗어나면 다시 볼 수 없습니다. 딜러에게 아이디·비밀번호와 camerabridge.io/dealer/login 주소를 전하고, "
                    "처음 들어가면 비밀번호를 바꾸라고 알려 주세요."), ""
        accounts = portal.load_accounts(fresh=True)["accounts"]
        if account_id not in accounts:
            return "", ERRORS["missing"]
        if action == "reset":
            password = portal.reset_password(account_id)
            return f"<b>{e(account_id)}</b> 새 임시 비밀번호: <code>{e(password)}</code> (이 화면에서만 보임)", ""
        if action in ("disable", "enable"):
            portal.set_disabled(account_id, action == "disable")
            return f"<b>{e(account_id)}</b> 계정을 {'껐' if action == 'disable' else '켰'}습니다.", ""
    except ValueError as error:
        return "", ERRORS.get(str(error), str(error))
    return "", "알 수 없는 요청입니다."


class handler(BaseHTTPRequestHandler):
    def _authorized(self) -> tuple[bool, str]:
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

    def _page(self, notice: str = "", error: str = "", headers: dict | None = None) -> None:
        try:
            accounts = portal.load_accounts(fresh=True)["accounts"]
        except Exception:  # noqa: BLE001
            accounts, error = {}, error or "계정 저장소(Blob)를 읽지 못했습니다."
        self._send(200, render(accounts, sites(), notice, error), headers)

    def do_GET(self):  # noqa: N802
        ok, key = self._authorized()
        if not ok:
            return self._send(401, "<p>권한이 없습니다. /owner/dealers?key=… 로 열어 주세요.</p>")
        headers = {"set-cookie": f"{COOKIE}={key}; Path=/owner; Max-Age=7776000; HttpOnly; Secure; SameSite=Lax"} if key else None
        return self._page(headers=headers)

    def do_POST(self):  # noqa: N802
        ok, _ = self._authorized()
        if not ok:
            return self._send(401, "<p>권한이 없습니다.</p>")
        length = min(int(self.headers.get("content-length") or 0), 20_000)
        form = parse_qs(self.rfile.read(length).decode("utf-8", "replace"))
        try:
            notice, error = handle_post(form, sites())
        except Exception:  # noqa: BLE001
            notice, error = "", "저장하지 못했습니다. 잠시 뒤 다시 해 주세요."
        return self._page(notice, error)
