"""딜러(매장) 화면: /dealer

/dealer           로그인했으면 화면(app/templates/dealer.html), 아니면 /dealer/login 으로
/dealer/login     GET 로그인 화면 · POST 아이디·비밀번호 확인 → 쿠키
/dealer/logout    POST 로그아웃
/dealer/data      시세 데이터(data/dealer/dealer_data.json.gz, 압축 그대로). 계정 정보는 화면 HTML에 넣어 보냄
/dealer/password  POST 비밀번호 바꾸기 (JSON)
계정은 사장님이 /owner/dealers 에서 만든다. 로그인·쿠키 규칙은 dealer_portal.py.
"""
from __future__ import annotations

import html
import json
import re
import sys
from http.cookies import SimpleCookie
from http.server import BaseHTTPRequestHandler
from pathlib import Path
from urllib.parse import parse_qs, urlparse

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
import dealer_portal as portal  # noqa: E402

PAGE = ROOT / "app/templates/dealer.html"
DATA = ROOT / "data/dealer/dealer_data.json.gz"
ROUTES = {"/dealer": "app", "/dealer/": "app", "/dealer/login": "login", "/dealer/logout": "logout",
          "/dealer/data": "data", "/dealer/password": "password"}
LANGS = ["ko", "en", "ja", "zh-Hans", "zh-Hant", "de", "fr", "it", "es", "pt"]

# 로그인 화면 문구 (나머지 화면 문구는 dealer.html 안에)
T = {
    "ko": {"title": "딜러 로그인", "lead": "카메라브릿지가 매장용으로 정리한 시세 화면입니다. 계정은 카메라브릿지에서 만들어 드립니다.",
           "id": "아이디", "pw": "비밀번호", "go": "로그인", "wrong": "아이디나 비밀번호가 맞지 않습니다.",
           "locked": "여러 번 틀려서 10분 동안 막았습니다. 잠시 뒤 다시 해 주세요.", "setup": "로그인을 준비 중입니다. 카메라브릿지에 알려 주세요.",
           "error": "지금 로그인할 수 없습니다. 잠시 뒤 다시 해 주세요."},
    "en": {"title": "Dealer sign-in", "lead": "Camera Bridge market data, arranged for camera shops. Accounts are issued by Camera Bridge.",
           "id": "Username", "pw": "Password", "go": "Sign in", "wrong": "The username or password is incorrect.",
           "locked": "Too many attempts. Please wait 10 minutes and try again.", "setup": "Sign-in is not set up yet. Please let Camera Bridge know.",
           "error": "Sign-in is unavailable right now. Please try again shortly."},
    "ja": {"title": "販売店ログイン", "lead": "Camera Bridge の相場データを販売店向けにまとめた画面です。アカウントは Camera Bridge が発行します。",
           "id": "ID", "pw": "パスワード", "go": "ログイン", "wrong": "ID またはパスワードが正しくありません。",
           "locked": "失敗が続いたため10分間ロックしました。しばらくしてからお試しください。", "setup": "ログインの準備中です。Camera Bridge にお知らせください。",
           "error": "現在ログインできません。しばらくしてからお試しください。"},
    "zh-Hans": {"title": "经销商登录", "lead": "Camera Bridge 为相机店整理的行情数据。账号由 Camera Bridge 开通。",
                "id": "账号", "pw": "密码", "go": "登录", "wrong": "账号或密码不正确。",
                "locked": "错误次数过多，已锁定 10 分钟。请稍后再试。", "setup": "登录尚未开通，请联系 Camera Bridge。",
                "error": "暂时无法登录，请稍后再试。"},
    "zh-Hant": {"title": "經銷商登入", "lead": "Camera Bridge 為相機店整理的行情資料。帳號由 Camera Bridge 開通。",
                "id": "帳號", "pw": "密碼", "go": "登入", "wrong": "帳號或密碼不正確。",
                "locked": "錯誤次數過多，已鎖定 10 分鐘。請稍後再試。", "setup": "登入尚未開通，請聯絡 Camera Bridge。",
                "error": "暫時無法登入，請稍後再試。"},
    "de": {"title": "Händler-Anmeldung", "lead": "Marktdaten von Camera Bridge, aufbereitet für Fotohändler. Zugänge vergibt Camera Bridge.",
           "id": "Benutzername", "pw": "Passwort", "go": "Anmelden", "wrong": "Benutzername oder Passwort ist falsch.",
           "locked": "Zu viele Versuche. Bitte in 10 Minuten erneut versuchen.", "setup": "Die Anmeldung ist noch nicht eingerichtet. Bitte Camera Bridge informieren.",
           "error": "Anmeldung derzeit nicht möglich. Bitte später erneut versuchen."},
    "fr": {"title": "Connexion revendeur", "lead": "Les données de marché de Camera Bridge, organisées pour les magasins photo. Les comptes sont créés par Camera Bridge.",
           "id": "Identifiant", "pw": "Mot de passe", "go": "Se connecter", "wrong": "Identifiant ou mot de passe incorrect.",
           "locked": "Trop de tentatives. Réessayez dans 10 minutes.", "setup": "La connexion n'est pas encore configurée. Prévenez Camera Bridge.",
           "error": "Connexion impossible pour le moment. Réessayez bientôt."},
    "it": {"title": "Accesso rivenditori", "lead": "I dati di mercato di Camera Bridge, organizzati per i negozi di fotografia. Gli account sono creati da Camera Bridge.",
           "id": "Nome utente", "pw": "Password", "go": "Accedi", "wrong": "Nome utente o password errati.",
           "locked": "Troppi tentativi. Riprova tra 10 minuti.", "setup": "L'accesso non è ancora configurato. Avvisa Camera Bridge.",
           "error": "Accesso non disponibile al momento. Riprova tra poco."},
    "es": {"title": "Acceso para tiendas", "lead": "Datos de mercado de Camera Bridge organizados para tiendas de fotografía. Las cuentas las crea Camera Bridge.",
           "id": "Usuario", "pw": "Contraseña", "go": "Entrar", "wrong": "El usuario o la contraseña no son correctos.",
           "locked": "Demasiados intentos. Vuelve a intentarlo en 10 minutos.", "setup": "El acceso aún no está configurado. Avisa a Camera Bridge.",
           "error": "No se puede entrar ahora. Inténtalo de nuevo en breve."},
    "pt": {"title": "Acesso para lojas", "lead": "Dados de mercado da Camera Bridge organizados para lojas de fotografia. As contas são criadas pela Camera Bridge.",
           "id": "Usuário", "pw": "Senha", "go": "Entrar", "wrong": "Usuário ou senha incorretos.",
           "locked": "Muitas tentativas. Tente novamente em 10 minutos.", "setup": "O acesso ainda não foi configurado. Avise a Camera Bridge.",
           "error": "Não é possível entrar agora. Tente novamente em breve."},
}
_data_cache: dict = {"mtime": None, "body": None}


def _logo() -> str:
    """camerabridge.io 첫 화면과 같은 서명 로고 (딜러 화면 HTML에서 꺼내 씀)."""
    match = re.search(r'<svg class="brand-logo".*?</svg>', PAGE.read_text(encoding="utf-8"), re.S)
    return match.group(0) if match else "Camera Bridge"


def pick_lang(query_lang: str | None, accept: str | None) -> str:
    if query_lang in LANGS:
        return query_lang
    for part in (accept or "").split(","):
        tag = part.split(";")[0].strip()
        if not tag:
            continue
        if tag in LANGS:
            return tag
        low = tag.lower()
        if low.startswith("zh"):
            return "zh-Hant" if any(x in low for x in ("hant", "tw", "hk", "mo")) else "zh-Hans"
        if low[:2] in LANGS:
            return low[:2]
    return "en"


def login_page(lang: str, error: str | None = None, account_id: str = "") -> str:
    t = T[lang]
    options = "".join(f'<a href="?lang={code}"{" aria-current=true" if code == lang else ""}>{LANG_NAMES[code]}</a>' for code in LANGS)
    message = f'<p class="err" role="alert">{html.escape(t.get(error, t["error"]))}</p>' if error else ""
    return f"""<!doctype html><html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(t["title"])} · Camera Bridge</title><meta name="robots" content="noindex,nofollow">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Newsreader:opsz,wght@6..72,500;6..72,600&display=swap">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/variable/pretendardvariable-dynamic-subset.min.css">
<style>
:root{{--bg:#fff;--soft:#f5f6f5;--border:#e1e4e3;--strong:#c9cecc;--text:#16181a;--text-soft:#5d6266;--accent:#1f4a3a;--red:#9b2c22}}
*{{box-sizing:border-box}}
body{{margin:0;background:var(--bg);color:var(--text);font:15px/1.55 Inter,"Pretendard Variable",Pretendard,system-ui,sans-serif;-webkit-font-smoothing:antialiased}}
header{{border-bottom:1px solid var(--text);padding:14px 16px}}
header a{{display:inline-flex;color:var(--accent);text-decoration:none}}.brand-logo{{display:block;height:40px;width:auto;margin:-4px 0}}
main{{max-width:400px;margin:56px auto;padding:0 16px}}
h1{{font-family:Newsreader,Georgia,serif;font-weight:600;font-size:30px;margin:0 0 6px}}
.lead{{color:var(--text-soft);margin:0 0 24px}}
label{{display:block;font-size:13px;color:var(--text-soft);margin:14px 0 4px}}
input{{width:100%;font:inherit;font-size:16px;padding:9px 10px;border:1px solid var(--strong);border-radius:0;background:var(--bg);color:var(--text)}}
input:focus{{outline:2px solid var(--accent);outline-offset:-1px;border-color:var(--accent)}}
button{{margin-top:20px;width:100%;font:inherit;font-weight:600;padding:10px;border:1px solid var(--accent);border-radius:0;background:var(--accent);color:#fff;cursor:pointer}}
.err{{border-left:3px solid var(--red);padding:6px 10px;background:#f8ecea;color:var(--red);margin:0 0 8px}}
.langs{{display:flex;flex-wrap:wrap;gap:4px 12px;border-top:1px solid var(--border);margin-top:32px;padding-top:12px;font-size:13px}}
.langs a{{color:var(--text-soft);text-decoration:none}}.langs a[aria-current]{{color:var(--text);font-weight:600}}
</style></head><body>
<header><a href="/" aria-label="Camera Bridge">{_logo()}</a></header>
<main>
<h1>{html.escape(t["title"])}</h1>
<p class="lead">{html.escape(t["lead"])}</p>
{message}
<form method="post" action="/dealer/login?lang={lang}">
<label for="id">{html.escape(t["id"])}</label><input id="id" name="id" autocomplete="username" autocapitalize="none" spellcheck="false" required value="{html.escape(account_id)}">
<label for="pw">{html.escape(t["pw"])}</label><input id="pw" name="pw" type="password" autocomplete="current-password" required>
<button type="submit">{html.escape(t["go"])}</button>
</form>
<nav class="langs" aria-label="Language">{options}</nav>
</main></body></html>"""


LANG_NAMES = {"ko": "한국어", "en": "English", "ja": "日本語", "zh-Hans": "简体中文", "zh-Hant": "繁體中文",
              "de": "Deutsch", "fr": "Français", "it": "Italiano", "es": "Español", "pt": "Português"}


def data_body() -> bytes:
    """압축된 시세 데이터. 파일이 바뀌지 않았으면 메모리에 있는 것을 쓴다."""
    mtime = DATA.stat().st_mtime
    if _data_cache["mtime"] != mtime:
        _data_cache.update(mtime=mtime, body=DATA.read_bytes())
    return _data_cache["body"]


def app_page(account_id: str, account: dict) -> bytes:
    """딜러 화면 HTML에 로그인한 계정 정보(window.ME)를 넣어서."""
    me = json.dumps(portal.public_account(account_id, account), ensure_ascii=False).replace("<", "\\u003c")
    return PAGE.read_bytes().replace(b"<!--ME-->", f"<script>window.ME = {me};</script>".encode("utf-8"), 1)


class handler(BaseHTTPRequestHandler):
    def _route(self) -> str:
        url = urlparse(self.path)
        return ROUTES.get(url.path) or (parse_qs(url.query).get("r") or [""])[0]

    def _query(self) -> dict:
        return parse_qs(urlparse(self.path).query)

    def _cookie(self) -> str:
        cookie = SimpleCookie(self.headers.get("cookie") or "")
        return cookie[portal.COOKIE].value if portal.COOKIE in cookie else ""

    def _body(self) -> bytes:
        return self.rfile.read(min(int(self.headers.get("content-length") or 0), 8_000))

    def _send(self, status: int, body: bytes = b"", content_type: str = "text/html; charset=utf-8", headers: dict | None = None) -> None:
        self.send_response(status)
        self.send_header("content-type", content_type)
        self.send_header("cache-control", "no-store")
        self.send_header("x-robots-tag", "noindex, nofollow")
        self.send_header("x-frame-options", "DENY")
        self.send_header("referrer-policy", "same-origin")
        for name, value in (headers or {}).items():
            self.send_header(name, value)
        self.end_headers()
        self.wfile.write(body)

    def _redirect(self, to: str, cookie: str | None = None) -> None:
        headers = {"location": to}
        if cookie:
            headers["set-cookie"] = cookie
        self._send(303, b"", headers=headers)

    def _json(self, status: int, payload: dict, cookie: str | None = None) -> None:
        self._send(status, json.dumps(payload, ensure_ascii=False).encode("utf-8"), "application/json",
                   {"set-cookie": cookie} if cookie else None)

    def _account(self):
        try:
            return portal.current_account(self._cookie())
        except Exception:  # noqa: BLE001 (계정 저장소를 못 읽으면 로그아웃 상태로)
            return None

    def do_GET(self):  # noqa: N802
        route = self._route()
        lang = pick_lang((self._query().get("lang") or [None])[0], self.headers.get("accept-language"))
        if route == "login":
            if self._account():
                return self._redirect("/dealer")
            return self._send(200, login_page(lang).encode("utf-8"))
        if route == "app":
            current = self._account()
            if not current:
                return self._redirect("/dealer/login")
            return self._send(200, app_page(*current))
        if route == "data":
            if not self._account():
                return self._json(401, {"ok": False})
            return self._send(200, data_body(), "application/json", {"content-encoding": "gzip"})
        return self._send(404, b"not found", "text/plain")

    def do_POST(self):  # noqa: N802
        route = self._route()
        if route == "login":
            lang = pick_lang((self._query().get("lang") or [None])[0], self.headers.get("accept-language"))
            form = parse_qs(self._body().decode("utf-8", "replace"))
            account_id = (form.get("id") or [""])[0]
            try:
                result = portal.login(account_id, (form.get("pw") or [""])[0])
            except Exception:  # noqa: BLE001
                result = "error"
            if isinstance(result, str):
                return self._send(401 if result == "wrong" else 503, login_page(lang, result, account_id).encode("utf-8"))
            return self._redirect("/dealer", portal.session_cookie(result[0]))
        if route == "logout":
            return self._redirect("/dealer/login", portal.clear_cookie())
        if route == "password":
            current = self._account()
            if not current:
                return self._json(401, {"ok": False})
            try:
                body = json.loads(self._body() or b"{}")
                result = portal.change_password(current[0], str(body.get("current") or ""), str(body.get("new") or ""))
            except Exception:  # noqa: BLE001
                result = "error"
            if isinstance(result, str):
                return self._json(400, {"ok": False, "error": result})
            return self._json(200, {"ok": True}, portal.session_cookie(result[0]))
        return self._send(404, b"not found", "text/plain")
