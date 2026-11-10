"""게시판 (전 세계 이용자 커뮤니티): 글 목록·읽기·쓰기·댓글·지우기·신고 + 운영자 관리 화면.

회원: 구글 로그인 (Google Identity Services ID 토큰 → tokeninfo로 확인). 구글 이메일·이름·사진은 저장하지 않고,
  구글 계정 고유번호(sub)를 비밀 값과 섞은 해시(회원 id)와 닉네임만 board/members/<회원id>.json 에 저장.
  로그인 유지: cb_member 쿠키 <회원id>.<만료>.<서명> (서명 비밀 = BOARD_SESSION_SECRET, 없으면 DEALER_SESSION_SECRET에서 용도를 나눠 만듦)
  환경 변수 GOOGLE_CLIENT_ID (구글 클라우드의 웹 OAuth 클라이언트 ID, 공개 값) 가 있어야 로그인 버튼이 나옴.
저장 위치: Vercel Blob (private), 의견 보내기와 같은 스토어
  board/posts/<글id>~<분류>~<회원id>.json                보이는 글
  board/comments/<글id>/<댓글id>~<회원id>.json            보이는 댓글
  board/held/…                                            신고 HIDE_REPORTS명 이상 → 자동으로 가림 (운영자가 확인 뒤 되살리거나 지움)
  board/removed/…                                         지운 글·댓글 (REMOVED_DAYS일 보관 뒤 매일 정리 run_retention, 운영자 화면 purge로도)
  board/reports/<글id>[~<댓글id>]/<접속지태그>.json        신고
  board/saves/<회원id>.json                               회원이 스크랩한 상품 (원래 주소 + 저장할 때 제목·가격 등), 최대 SAVE_LIMIT개
가격 알림: 회원이 직접 켜면(구글 계정을 한 번 더 확인) 그때만 이메일을 회원 파일 alerts에 저장, 끄면 바로 지움.
  매일 Vercel Cron(vercel.json) → GET ?r=alerts → 저장한 상품이 지난번 알린 뒤 1% 넘게 내렸거나 팔리면 한 통으로 Resend 발송.
  같은 변화는 한 번만 (상품마다 notified_price·notified_status). RESEND_API_KEY가 없으면 보내지 않음. CRON_SECRET 인증 필수, 미설정이면 실행하지 않음.
스팸 막기: 로그인한 회원만 쓰기, 숨은 입력칸, 쓰기 시작한 지 1.5초 안에 보내면 거절, 회원당 하루 글 POST_LIMIT·댓글 COMMENT_LIMIT건, 링크 MAX_LINKS개까지.
신고는 로그인 없이도 가능 (같은 접속지는 한 번, 접속지 = 날마다 바뀌는 IP 해시).
운영자 관리: /owner/board (cb_owner 쿠키 = OWNER_DASHBOARD_KEY, /owner/usage?key=… 로 한 번 들어가면 생김)
"""
from __future__ import annotations

import datetime as dt
import hashlib
import hmac
import html
import json
import os
import re
import secrets
from concurrent.futures import ThreadPoolExecutor
from http.cookies import SimpleCookie
from http.server import BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse

import requests

KST = dt.timezone(dt.timedelta(hours=9))
CATEGORIES = ("free", "question", "review", "site")  # 자유 · 질문 · 정보·후기 · 사이트 의견
PAGE_SIZE = 20
TITLE_LEN, BODY_LEN, COMMENT_LEN, NICK_LEN = (2, 80), (5, 5000), (1, 1000), (1, 20)
POST_LIMIT, COMMENT_LIMIT = 5, 30
MAX_LINKS = 3
MIN_ELAPSED_MS = 1500
HIDE_REPORTS = 3
REMOVED_DAYS = 30
SAVE_LIMIT = 300
COOKIE = "cb_owner"
MEMBER_COOKIE = "cb_member"
SESSION_DAYS = 90
GOOGLE_ISSUERS = ("accounts.google.com", "https://accounts.google.com")
LINK = re.compile(r"https?://|www\.", re.I)
ID = re.compile(r"^\d{14}-[0-9a-f]{6}$")
STAMP = re.compile(r"(\d{14})-[0-9a-f]{6}")


# ── 공통 ──
def _client_ip(headers) -> str:
    forwarded = headers.get("x-forwarded-for") or headers.get("x-real-ip") or ""
    return forwarded.split(",")[0].strip()


def _tag(headers, day: str) -> str:
    """접속지 태그: 날마다 바뀌는 소금을 섞은 IP 해시 (IP 자체는 남기지 않음)."""
    salt = os.environ.get("FEEDBACK_SALT", "camerabridge")
    return hashlib.sha256(f"{salt}:board:{day}:{_client_ip(headers)}".encode()).hexdigest()[:12]


# ── 회원 (구글 로그인) ──
def _secret() -> bytes | None:
    value = os.environ.get("BOARD_SESSION_SECRET") or os.environ.get("DEALER_SESSION_SECRET", "")
    return hashlib.sha256(b"board-session:" + value.encode()).digest() if len(value) >= 32 else None


def _sign(payload: str, secret: bytes) -> str:
    return hmac.new(secret, payload.encode(), hashlib.sha256).hexdigest()[:32]


def session_value(member_id: str, now: float | None = None) -> str:
    secret = _secret()
    expires = int((now or dt.datetime.now().timestamp()) + SESSION_DAYS * 86400)
    payload = f"{member_id}.{expires}"
    return f"{payload}.{_sign(payload, secret)}"


def member_from_cookie(value: str, now: float | None = None) -> str | None:
    secret = _secret()
    parts = str(value or "").split(".")
    if not secret or len(parts) != 3 or not re.fullmatch(r"[0-9a-f]{20}", parts[0]) or not parts[1].isdigit():
        return None
    if int(parts[1]) < (now or dt.datetime.now().timestamp()):
        return None
    return parts[0] if hmac.compare_digest(_sign(f"{parts[0]}.{parts[1]}", secret), parts[2]) else None


def verify_google(credential: str) -> str | None:
    """구글 ID 토큰을 구글 tokeninfo로 확인 → 계정 고유번호(sub). 우리 클라이언트 ID로 발급된 토큰만."""
    identity = google_identity(credential)
    return identity["sub"] if identity else None


def google_identity(credential: str) -> dict | None:
    """구글 ID 토큰 → {sub, email, email_verified}. 이메일은 알림을 켤 때만 씀."""
    client_id = os.environ.get("GOOGLE_CLIENT_ID", "")
    if not client_id or not credential or len(credential) > 4096:
        return None
    try:
        info = requests.get("https://oauth2.googleapis.com/tokeninfo", params={"id_token": credential}, timeout=8).json()
    except (requests.RequestException, ValueError):
        return None
    if info.get("aud") != client_id or info.get("iss") not in GOOGLE_ISSUERS or not info.get("sub"):
        return None
    if int(info.get("exp") or 0) < dt.datetime.now().timestamp():
        return None
    return {"sub": str(info["sub"]), "email": str(info.get("email") or ""), "email_verified": str(info.get("email_verified")).lower() == "true"}


def _member_id(sub: str) -> str:
    return hmac.new(_secret(), f"google:{sub}".encode(), hashlib.sha256).hexdigest()[:20]


def _member(blob, member_id: str | None) -> dict | None:
    return _read(blob, f"board/members/{member_id}.json") if member_id else None


def login(body: dict) -> tuple[int, dict, str | None]:
    if not _secret():
        return 503, {"ok": False, "error": "unavailable"}, None
    sub = verify_google(str(body.get("credential") or ""))
    if not sub:
        return 401, {"ok": False, "error": "login"}, None
    member_id = _member_id(sub)
    blob = _blob()
    member = _member(blob, member_id)
    if not member:
        member = {"id": member_id, "nick": None, "created_at": _now()[0].isoformat(timespec="seconds")}
        _put(blob, f"board/members/{member_id}.json", member)
    return 200, {"ok": True, "member": _public_member(member)}, session_value(member_id)


def set_nick(body: dict, member_id: str | None) -> tuple[int, dict]:
    blob = _blob()
    member = _member(blob, member_id)
    if not member:
        return 401, {"ok": False, "error": "login"}
    nick = _clean(body.get("nick"), NICK_LEN[1]).replace("\n", " ")
    if not (NICK_LEN[0] <= len(nick) <= NICK_LEN[1]):
        return 400, {"ok": False, "error": "nick"}
    member = {**member, "nick": nick}
    _put(blob, f"board/members/{member_id}.json", member)
    return 200, {"ok": True, "member": _public_member(member)}


def _mask(email: str) -> str:
    name, _, domain = email.partition("@")
    return f"{name[:2]}{'*' * max(1, len(name) - 2)}@{domain}" if domain else ""


def _public_member(member: dict) -> dict:
    alerts = member.get("alerts") or {}
    return {"nick": member.get("nick"), "alerts": bool(alerts.get("email")), "alerts_email": _mask(alerts.get("email") or "")}


def me(member_id: str | None) -> dict:
    member = _member(_blob(), member_id) if member_id else None
    return {"ok": True, "client_id": os.environ.get("GOOGLE_CLIENT_ID") or None,
            "member": _public_member(member) if member else None}


# ── 가격 알림 (회원이 켰을 때만 이메일 저장) ──
def alerts_on(body: dict, member_id: str | None, current: dict | None = None, send=None) -> tuple[int, dict]:
    blob = _blob()
    member = _member(blob, member_id)
    if not member:
        return 401, {"ok": False, "error": "login"}
    identity = google_identity(str(body.get("credential") or ""))
    if not identity or _member_id(identity["sub"]) != member_id:
        return 401, {"ok": False, "error": "login"}
    if not identity["email"] or not identity["email_verified"]:
        return 400, {"ok": False, "error": "email"}
    member = {**member, "alerts": {"email": identity["email"], "locale": str(body.get("locale") or "")[:12] or "en",
                                   "since": _now()[0].isoformat(timespec="seconds")}}
    _put(blob, f"board/members/{member_id}.json", member)
    # 켜는 순간의 가격을 기준으로 (켜기 전 변화는 알리지 않음)
    current = current if current is not None else _current_listings_safe()
    if current is not None:
        items = _saves(blob, member_id)
        for item in items:
            listing = current.get(item.get("url")) or {}
            item["notified_price"] = listing.get("parsed_price_numeric") or item.get("price")
            item["notified_status"] = "asking" if listing.get("sold_quality") == "asking" else ("sold" if listing else "gone")
        _put(blob, f"board/saves/{member_id}.json", {"items": items})
    # 켰다는 확인 메일 (2026-11-08 사장님: 알림 신청하면 내 메일로 확인 메일) — 못 보내도 켜기는 그대로
    try:
        subject, html_body = _confirm_email(member_id, member["alerts"], len(_saves(blob, member_id)))
        (send or _send_email)(member["alerts"]["email"], subject, html_body)
    except Exception:  # noqa: BLE001
        pass
    return 200, {"ok": True, "member": _public_member(member)}


CONFIRM_TEXT = {
    "ko": ("가격 알림을 켰어요 · 카메라브릿지", "카메라브릿지 가격 알림을 켰습니다.",
           "저장한 상품이 1% 넘게 내리거나 팔리면 한 번에 묶어 메일로 알려 드려요. 지금 저장한 상품: {n}개.",
           "상품 카드의 책갈피 아이콘으로 더 저장할 수 있어요.", "저장한 상품 보기", "알림 끄기"),
    "ja": ("価格通知をオンにしました · Camera Bridge", "Camera Bridge の価格通知をオンにしました。",
           "保存した商品が1%以上値下がりするか売り切れると、まとめてメールでお知らせします。現在の保存商品：{n}件。",
           "商品カードのしおりアイコンでさらに保存できます。", "保存した商品を見る", "通知を停止"),
    "en": ("Price alerts are on · Camera Bridge", "Price alerts are on for your Camera Bridge account.",
           "We'll email you once when a listing you saved drops more than 1% or sells. Saved listings now: {n}.",
           "Save more with the bookmark icon on any listing.", "See saved listings", "Turn off alerts"),
    "de": ("Preisalarm ist aktiv · Camera Bridge", "Der Preisalarm für dein Camera-Bridge-Konto ist aktiv.",
           "Wir schreiben dir, sobald ein gemerktes Angebot um mehr als 1 % fällt oder verkauft ist. Gemerkte Angebote: {n}.",
           "Mit dem Lesezeichen-Symbol kannst du weitere Angebote merken.", "Gemerkte Angebote ansehen", "Alarm ausschalten"),
    "it": ("Avvisi di prezzo attivi · Camera Bridge", "Gli avvisi di prezzo per il tuo account Camera Bridge sono attivi.",
           "Ti scriviamo quando un annuncio salvato scende di oltre l'1% o viene venduto. Annunci salvati: {n}.",
           "Salvane altri con l'icona segnalibro su ogni annuncio.", "Vedi annunci salvati", "Disattiva avvisi"),
    "es": ("Alertas de precio activadas · Camera Bridge", "Las alertas de precio de tu cuenta de Camera Bridge están activadas.",
           "Te escribiremos cuando un anuncio guardado baje más de un 1 % o se venda. Anuncios guardados: {n}.",
           "Guarda más con el icono de marcador en cualquier anuncio.", "Ver anuncios guardados", "Desactivar alertas"),
    "pt": ("Alertas de preço ativados · Camera Bridge", "Os alertas de preço da sua conta Camera Bridge estão ativados.",
           "Avisaremos por e-mail quando um anúncio salvo cair mais de 1% ou for vendido. Anúncios salvos: {n}.",
           "Salve mais com o ícone de marcador em qualquer anúncio.", "Ver anúncios salvos", "Desativar alertas"),
    "zh": ("价格提醒已开启 · Camera Bridge", "你的 Camera Bridge 价格提醒已开启。",
           "保存的商品降价超过 1% 或售出时，我们会合并发一封邮件通知你。当前保存的商品：{n} 件。",
           "在任意商品卡片上点书签图标即可保存更多。", "查看保存的商品", "关闭提醒"),
}


def _confirm_email(member_id: str, alerts: dict, saved: int) -> tuple[str, str]:
    subject, title, how, more, see, stop_text = CONFIRM_TEXT.get((alerts.get("locale") or "en")[:2], CONFIRM_TEXT["en"])
    stop = f"https://camerabridge.io/api/board?r=unsub&m={member_id}&s={unsubscribe_sig(member_id)}"
    body = (f'<div style="font:15px/1.5 -apple-system,Helvetica,sans-serif;color:#16181a;max-width:560px">'
            f'<p style="font:22px/1.3 Georgia,serif;margin:0 0 12px">{html.escape(title)}</p>'
            f'<p>{html.escape(how.format(n=saved))}</p><p>{html.escape(more)}</p>'
            f'<p><a href="https://camerabridge.io/#saved" style="color:#16181a">{html.escape(see)}</a></p>'
            f'<p style="color:#878b8d;font-size:12px"><a href="{stop}" style="color:#878b8d">{html.escape(stop_text)}</a> · Camera Bridge</p></div>')
    return subject, body


def alerts_off(member_id: str | None) -> tuple[int, dict]:
    blob = _blob()
    member = _member(blob, member_id)
    if not member:
        return 401, {"ok": False, "error": "login"}
    member.pop("alerts", None)
    _put(blob, f"board/members/{member_id}.json", member)
    return 200, {"ok": True, "member": _public_member(member)}


def unsubscribe_sig(member_id: str) -> str:
    return _sign(f"unsub:{member_id}", _secret())


def unsubscribe(member_id: str, sig: str) -> bool:
    if not _secret() or not re.fullmatch(r"[0-9a-f]{20}", member_id or "") or not hmac.compare_digest(unsubscribe_sig(member_id), sig or ""):
        return False
    alerts_off(member_id)
    return True


ALERT_TEXT = {
    "ko": {"subject": "저장한 상품 {n}개에 변화가 있어요", "drop": "가격 내림 {a} → {b} (−{p}%)", "sold": "판매 완료", "gone": "더 이상 안 보임",
           "list": "저장한 상품 모두 보기", "stop": "이 알림 끄기", "intro": "카메라브릿지에 저장한 상품의 소식입니다.",
           "want_subject": "찾던 매물 {n}개가 나왔어요", "want": "{name} · {grade} 등급 · 도착 총액 {total} (판매가 {listed}, 배송·세금 포함 예상)"},
    "ja": {"subject": "保存した商品 {n}件に変化があります", "drop": "値下げ {a} → {b}（−{p}%）", "sold": "売り切れ", "gone": "掲載終了",
           "list": "保存した商品をすべて見る", "stop": "この通知を停止", "intro": "Camera Bridge に保存した商品のお知らせです。",
           "want_subject": "探していた商品が{n}件見つかりました", "want": "{name} · {grade}ランク · 到着総額 {total}（販売価格 {listed}、送料・税込の見込み）"},
    "en": {"subject": "{n} of your saved listings changed", "drop": "Price dropped {a} → {b} (−{p}%)", "sold": "Sold", "gone": "No longer listed",
           "list": "See all saved listings", "stop": "Turn off these emails", "intro": "Updates on the listings you saved on Camera Bridge.",
           "want_subject": "{n} listings match what you're looking for", "want": "{name} · grade {grade} · est. delivered {total} (listed {listed}, incl. shipping & taxes)"},
}


def _fmt(price, currency) -> str:
    if price is None:
        return "—"
    return f"{currency or ''} {price:,.0f}".strip()


def _alert_events(items: list[dict], current: dict) -> list[dict]:
    """지난번 알린 뒤 1% 넘게 내렸거나 팔린 상품. items를 고쳐 놓음(notified_*)."""
    events = []
    for item in items:
        listing = current.get(item.get("url"))
        status = "gone" if not listing else ("asking" if listing.get("sold_quality") == "asking" else "sold")
        before = item.get("notified_price") if item.get("notified_price") is not None else item.get("price")
        price = (listing or {}).get("parsed_price_numeric")
        same_currency = (listing or {}).get("currency") == item.get("currency")
        if status == "asking" and price and before and same_currency and price < before * 0.99:
            events.append({"kind": "drop", "item": item, "before": before, "after": price})
            item["notified_price"] = price
        elif status == "asking" and price and same_currency and (before is None or price > before):
            item["notified_price"] = price  # 오르면 기준만 올림 (알리지 않음)
        if status != "asking" and item.get("notified_status", "asking") == "asking":
            events.append({"kind": status, "item": item})
        item["notified_status"] = status
    return events


def _alert_email(member_id: str, alerts: dict, events: list[dict]) -> tuple[str, str]:
    text = ALERT_TEXT.get((alerts.get("locale") or "en")[:2], ALERT_TEXT["en"])
    rows = []
    for event in events:
        if event["kind"] == "want":
            match, want = event["match"], event["want"]
            note = text["want"].format(name=want.get("name") or want["entity"], grade=match["grade"], total=_fmt(match["total"], want["currency"]),
                                       listed=_fmt(match["listed"], match["listed_currency"]))
            rows.append(f'<tr><td style="padding:8px 0;border-bottom:1px solid #ddd"><a href="{html.escape(match["url"] or "")}" style="color:#16181a">'
                        f'{html.escape(match.get("title") or match["url"] or "")}</a><br><span style="color:#5d6266;font-size:13px">'
                        f'{html.escape(match.get("source") or "")} · {html.escape(note)}</span></td></tr>')
            continue
        item = event["item"]
        if event["kind"] == "drop":
            pct = round((1 - event["after"] / event["before"]) * 100)
            note = text["drop"].format(a=_fmt(event["before"], item.get("currency")), b=_fmt(event["after"], item.get("currency")), p=pct)
        else:
            note = text[event["kind"]]
        rows.append(f'<tr><td style="padding:8px 0;border-bottom:1px solid #ddd"><a href="{html.escape(item["url"])}" style="color:#16181a">'
                    f'{html.escape(item.get("title") or item["url"])}</a><br><span style="color:#5d6266;font-size:13px">'
                    f'{html.escape(item.get("source") or "")} · {html.escape(note)}</span></td></tr>')
    stop = f"https://camerabridge.io/api/board?r=unsub&m={member_id}&s={unsubscribe_sig(member_id)}"
    body = (f'<div style="font:15px/1.5 -apple-system,Helvetica,sans-serif;color:#16181a;max-width:560px">'
            f'<p>{html.escape(text["intro"])}</p><table style="width:100%;border-collapse:collapse">{"".join(rows)}</table>'
            f'<p><a href="https://camerabridge.io/#saved" style="color:#16181a">{html.escape(text["list"])}</a></p>'
            f'<p style="color:#878b8d;font-size:12px"><a href="{stop}" style="color:#878b8d">{html.escape(text["stop"])}</a> · Camera Bridge</p></div>')
    wanted = sum(1 for e in events if e["kind"] == "want")
    subject = text["want_subject"].format(n=wanted) if wanted == len(events) else text["subject"].format(n=len(events))
    return subject, body


def _send_email(to: str, subject: str, body: str) -> bool:
    key = os.environ.get("RESEND_API_KEY", "")
    if not key:
        return False
    sender = os.environ.get("ALERT_FROM", "Camera Bridge <alerts@camerabridge.io>")
    try:
        response = requests.post("https://api.resend.com/emails", timeout=15, headers={"Authorization": f"Bearer {key}"},
                                 json={"from": sender, "to": [to], "subject": subject, "html": body})
        return response.status_code < 300
    except requests.RequestException:
        return False


def _current_listings_safe():
    try:
        return _current_listings()
    except Exception:  # noqa: BLE001
        return None


def run_alerts(current: dict | None = None, send=None, records=None) -> dict:
    """알림을 켠 회원마다 변화(저장한 상품 + 원하는 매물)를 모아 한 통씩. 보내지 못하면 notified를 저장하지 않아 다음에 다시 시도."""
    send = send or _send_email
    blob = _blob()
    current = current if current is not None else _current_listings()
    records_cache = {"v": records}

    def recs():
        if records_cache["v"] is None:
            records_cache["v"] = _current_records()
        return records_cache["v"]
    members = sent = waiting = 0
    for item in _names(blob, "board/members/"):
        member = _read(blob, item) or {}
        alerts = member.get("alerts") or {}
        if not alerts.get("email") or not member.get("id"):
            continue
        members += 1
        items = _saves(blob, member["id"])
        events = _alert_events(items, current)
        wants = _wants(blob, member["id"])
        if wants:
            events += _want_events(wants, recs())
        if events:
            subject, body = _alert_email(member["id"], alerts, events)
            if not send(alerts["email"], subject, body):
                waiting += 1  # 못 보냄 (메일 키 없음·발송 실패) → 다음 검사에서 다시
                continue
            sent += 1
        _put(blob, f"board/saves/{member['id']}.json", {"items": items})
        if wants:
            _put(blob, f"board/wants/{member['id']}.json", {"items": wants})
    # mail_ready: 메일 키가 있는지. 없으면 알림을 켠 사람이 있어도 한 통도 안 나감 (크롤링 기록에 경고로 띄움)
    return {"ok": True, "members": members, "sent": sent, "waiting": waiting,
            "mail_ready": bool(os.environ.get("RESEND_API_KEY"))}


def _clean(text, limit: int) -> str:
    text = re.sub(r"[\u0000-\u0008\u000b\u000c\u000e-\u001f\u007f]", "", str(text or ""))
    text = re.sub(r"[ \t]+\n", "\n", text.replace("\r\n", "\n")).strip()
    return re.sub(r"\n{4,}", "\n\n\n", text)[:limit + 1]


def _now():
    now = dt.datetime.now(KST)
    return now, now.strftime("%Y%m%d%H%M%S"), now.strftime("%Y-%m-%d")


def _new_id(stamp: str) -> str:
    return f"{stamp}-{secrets.token_hex(3)}"



KEEP_DAYS = 365  # 개인정보처리방침: 의견·방문 기록은 받은 날(기록한 날)부터 1년
RETENTION_PREFIXES = ("usage/", "feedback/")  # usage/<YYYY-MM-DD>/… · feedback/<YYYY-MM-DD>/…


def run_retention(blob=None, today: dt.date | None = None, catch_up_days: int = 30) -> dict:
    """보유 기간이 지난 기록 지우기 (매일 Vercel Cron에서 알림 뒤에 부름, 2026-11-05).
    - 방문 기록·의견: 날짜 폴더가 KEEP_DAYS일 지난 것. 매일 돌므로 지난 catch_up_days일치만 봄 (빠진 날을 메움, 목록을 크게 읽지 않음)
    - 지운 글·댓글(board/removed/): 쓴 날 기준 REMOVED_DAYS일 지난 것 (전에는 운영자 화면 'purge'로만 비웠음)"""
    blob = blob or _blob()
    today = today or dt.datetime.now(KST).date()
    deleted = {"usage": 0, "feedback": 0, "removed": 0}
    for back in range(catch_up_days):
        day = (today - dt.timedelta(days=KEEP_DAYS + back)).isoformat()
        for prefix in RETENTION_PREFIXES:
            urls = [i.url for i in _names(blob, f"{prefix}{day}/")]
            for start in range(0, len(urls), 500):
                blob.delete(urls[start:start + 500])
            deleted[prefix.rstrip("/")] += len(urls)
    cutoff = (dt.datetime.now(KST) - dt.timedelta(days=REMOVED_DAYS)).strftime("%Y%m%d")
    old = [i.url for i in _names(blob, "board/removed/") if (STAMP.findall(i.pathname) or ["99999999"])[-1][:8] < cutoff]
    if old:
        blob.delete(old)
    deleted["removed"] = len(old)
    try:  # Neon Postgres로 옮긴 방문 기록·의견 (2026-11, pgstore.py)
        import sys as _sys
        from pathlib import Path as _Path
        _sys.path.insert(0, str(_Path(__file__).resolve().parent.parent))
        import pgstore  # noqa: WPS433
        if pgstore.enabled():
            pgstore.delete_older_than(KEEP_DAYS)
            deleted["db"] = "ok"
    except Exception as error:  # noqa: BLE001
        deleted["db"] = f"error: {type(error).__name__}"
    return deleted

def _blob():
    # 2026-11-08: Blob 무료 한도 초과(12/1까지 막힘) → Neon이 연결돼 있으면 같은 모양의 Neon 저장소 (pgstore.PgBlob)
    import sys as _sys
    from pathlib import Path as _Path
    root = str(_Path(__file__).resolve().parent.parent)
    if root not in _sys.path:
        _sys.path.insert(0, root)
    import pgstore  # noqa: WPS433
    return pgstore.blob_store()


def _names(blob, prefix: str) -> list:
    try:
        return list(blob.iter_objects(prefix=prefix))
    except Exception:  # noqa: BLE001
        return []


def _read(blob, item) -> dict | None:
    try:
        return json.loads(blob.get(item.url if hasattr(item, "url") else item, access="private", use_cache=False).content)
    except Exception:  # noqa: BLE001
        return None


def _read_many(blob, items) -> list:
    with ThreadPoolExecutor(max_workers=8) as pool:
        return list(pool.map(lambda item: _read(blob, item), items))


def _put(blob, path: str, entry: dict) -> None:
    blob.put(path, json.dumps(entry, ensure_ascii=False).encode("utf-8"), access="private",
             content_type="application/json", overwrite=True)


def _move(blob, item, to_prefix: str, entry: dict | None = None) -> None:
    """글·댓글을 다른 칸(held/removed/posts)으로 옮김: 새 자리에 쓰고 옛 자리를 지움."""
    entry = entry if entry is not None else _read(blob, item)
    rest = item.pathname.split("/", 2)[2]
    _put(blob, f"board/{to_prefix}/{rest}", entry or {})
    blob.delete(item.url)


def _notify(text: str) -> None:
    token, chat = os.environ.get("TELEGRAM_BOT_TOKEN"), os.environ.get("TELEGRAM_CHAT_ID")
    if not token or not chat:
        return
    try:
        requests.post(f"https://api.telegram.org/bot{token}/sendMessage",
                      json={"chat_id": chat, "text": text[:4000], "disable_web_page_preview": True}, timeout=8)
    except requests.RequestException:
        pass


def _public(entry: dict, member_id: str | None = None) -> dict:
    """밖으로 보내는 칸만 (회원 id는 내보내지 않고, 내 글인지만 mine으로)."""
    row = {k: entry.get(k) for k in ("id", "post_id", "category", "title", "body", "nick", "created_at", "locale")
           if entry.get(k) is not None}
    if member_id and entry.get("member") == member_id:
        row["mine"] = True
    return row


def _check_human(body: dict) -> tuple[int, dict] | None:
    if str(body.get("website") or "").strip():  # 숨은 칸: 사람은 비워 둠
        return 200, {"ok": True}
    try:
        elapsed = int(body.get("elapsed_ms") or 0)
    except (TypeError, ValueError):
        elapsed = 0
    if elapsed < MIN_ELAPSED_MS:
        return 429, {"ok": False, "error": "too_fast"}
    return None


def _writer(blob, member_id: str | None) -> tuple[dict | None, str]:
    member = _member(blob, member_id)
    if not member:
        return None, "login"
    if not member.get("nick"):
        return None, "nick"
    return member, ""


def _find_post(blob, post_id: str, where: str = "posts"):
    if not ID.match(post_id or ""):
        return None
    items = _names(blob, f"board/{where}/{post_id}~")
    return items[0] if items else None


# ── 읽기 ──
def list_posts(category: str = "", page: int = 1) -> dict:
    blob = _blob()
    items = [i for i in _names(blob, "board/posts/") if not category or f"~{category}~" in i.pathname]
    items.sort(key=lambda i: i.pathname, reverse=True)
    pages = max(1, -(-len(items) // PAGE_SIZE))
    page = max(1, min(page, pages))
    chosen = items[(page - 1) * PAGE_SIZE: page * PAGE_SIZE]
    counts: dict[str, int] = {}
    for item in _names(blob, "board/comments/"):
        post_id = item.pathname.split("/")[2]
        counts[post_id] = counts.get(post_id, 0) + 1
    posts = []
    for entry in _read_many(blob, chosen):
        if entry:
            row = _public(entry)
            row.pop("body", None)
            row["comments"] = counts.get(entry["id"], 0)
            posts.append(row)
    return {"ok": True, "posts": posts, "page": page, "pages": pages, "total": len(items)}


def read_post(post_id: str, member_id: str | None = None) -> tuple[int, dict]:
    blob = _blob()
    item = _find_post(blob, post_id)
    entry = _read(blob, item) if item else None
    if not entry:
        return 404, {"ok": False, "error": "not_found"}
    comment_items = sorted(_names(blob, f"board/comments/{post_id}/"), key=lambda i: i.pathname)
    comments = [_public(c, member_id) for c in _read_many(blob, comment_items) if c]
    return 200, {"ok": True, "post": _public(entry, member_id), "comments": comments}


# ── 쓰기 ──
def create_post(body: dict, member_id: str | None) -> tuple[int, dict]:
    blocked = _check_human(body)
    if blocked:
        return blocked
    category = str(body.get("category") or "")
    if category not in CATEGORIES:
        return 400, {"ok": False, "error": "category"}
    title = _clean(body.get("title"), TITLE_LEN[1]).replace("\n", " ")
    text = _clean(body.get("body"), BODY_LEN[1])
    if not (TITLE_LEN[0] <= len(title) <= TITLE_LEN[1]):
        return 400, {"ok": False, "error": "title"}
    if not (BODY_LEN[0] <= len(text) <= BODY_LEN[1]):
        return 400, {"ok": False, "error": "body"}
    if len(LINK.findall(title + " " + text)) > MAX_LINKS:
        return 400, {"ok": False, "error": "links"}
    blob = _blob()
    member, error = _writer(blob, member_id)
    if not member:
        return 401 if error == "login" else 400, {"ok": False, "error": error}
    now, stamp, _ = _now()
    today = stamp[:8]
    mine = [i for i in _names(blob, f"board/posts/{today}") + _names(blob, f"board/held/{today}") if i.pathname.endswith(f"~{member_id}.json")]
    if len(mine) >= POST_LIMIT:
        return 429, {"ok": False, "error": "limit"}
    entry = {"id": _new_id(stamp), "created_at": now.isoformat(timespec="seconds"), "category": category, "title": title,
             "body": text, "nick": member["nick"], "member": member_id, "locale": str(body.get("locale") or "")[:12] or None}
    _put(blob, f"board/posts/{entry['id']}~{category}~{member_id}.json", entry)
    _notify(f"📝 게시판 새 글 ({category})\n\n{title}\n{text[:500]}\n\n— {member['nick']}\nhttps://camerabridge.io/#board/{entry['id']}")
    return 200, {"ok": True, "id": entry["id"]}


def create_comment(body: dict, member_id: str | None) -> tuple[int, dict]:
    blocked = _check_human(body)
    if blocked:
        return blocked
    post_id = str(body.get("post_id") or "")
    text = _clean(body.get("body"), COMMENT_LEN[1])
    if not (COMMENT_LEN[0] <= len(text) <= COMMENT_LEN[1]):
        return 400, {"ok": False, "error": "body"}
    if len(LINK.findall(text)) > MAX_LINKS:
        return 400, {"ok": False, "error": "links"}
    blob = _blob()
    member, error = _writer(blob, member_id)
    if not member:
        return 401 if error == "login" else 400, {"ok": False, "error": error}
    if not _find_post(blob, post_id):
        return 404, {"ok": False, "error": "not_found"}
    now, stamp, _ = _now()
    today = stamp[:8]
    mine = [i for i in _names(blob, "board/comments/") if i.pathname.split("/")[-1].startswith(today) and i.pathname.endswith(f"~{member_id}.json")]
    if len(mine) >= COMMENT_LIMIT:
        return 429, {"ok": False, "error": "limit"}
    entry = {"id": _new_id(stamp), "post_id": post_id, "created_at": now.isoformat(timespec="seconds"), "body": text,
             "nick": member["nick"], "member": member_id, "locale": str(body.get("locale") or "")[:12] or None}
    _put(blob, f"board/comments/{post_id}/{entry['id']}~{member_id}.json", entry)
    return 200, {"ok": True, "id": entry["id"]}


def _target(blob, post_id: str, comment_id: str = ""):
    if comment_id:
        if not ID.match(comment_id or "") or not ID.match(post_id or ""):
            return None
        items = _names(blob, f"board/comments/{post_id}/{comment_id}~")
        return items[0] if items else None
    return _find_post(blob, post_id)


def delete_entry(body: dict, member_id: str | None) -> tuple[int, dict]:
    """글쓴이(로그인한 그 회원)가 지움 → board/removed 로 옮김 (글이면 댓글도 같이)."""
    blob = _blob()
    post_id, comment_id = str(body.get("post_id") or ""), str(body.get("comment_id") or "")
    item = _target(blob, post_id, comment_id)
    entry = _read(blob, item) if item else None
    if not entry:
        return 404, {"ok": False, "error": "not_found"}
    if not member_id or not hmac.compare_digest(str(entry.get("member") or ""), member_id):
        return 403, {"ok": False, "error": "not_yours"}
    _move(blob, item, "removed", {**entry, "removed_at": _now()[0].isoformat(timespec="seconds"), "removed_by": "author"})
    if not comment_id:
        for comment in _names(blob, f"board/comments/{post_id}/"):
            _move(blob, comment, "removed")
    return 200, {"ok": True}


def report(body: dict, headers) -> tuple[int, dict]:
    """신고: 같은 접속지는 한 번만. HIDE_REPORTS명이 신고하면 board/held 로 옮겨 가림."""
    blob = _blob()
    post_id, comment_id = str(body.get("post_id") or ""), str(body.get("comment_id") or "")
    item = _target(blob, post_id, comment_id)
    if not item:
        return 404, {"ok": False, "error": "not_found"}
    _, _, day = _now()
    key = f"{post_id}~{comment_id}" if comment_id else post_id
    reason = _clean(body.get("reason"), 200)
    _put(blob, f"board/reports/{key}/{_tag(headers, day)}.json", {"reason": reason, "day": day})
    count = len(_names(blob, f"board/reports/{key}/"))
    hidden = count >= HIDE_REPORTS
    if hidden:
        _move(blob, item, "held")
    _notify(f"🚩 게시판 신고 {count}건{' → 자동으로 가림' if hidden else ''}\n{item.pathname}\n{reason}\nhttps://camerabridge.io/owner/board")
    return 200, {"ok": True, "hidden": hidden}


# ── 상품 스크랩 (구글 로그인 회원만) ──
def _saves(blob, member_id: str) -> list[dict]:
    return (_read(blob, f"board/saves/{member_id}.json") or {}).get("items") or []


def _clip(value, limit: int) -> str:
    return str(value or "").strip()[:limit]


def save_item(body: dict, member_id: str | None) -> tuple[int, dict]:
    if not member_id:
        return 401, {"ok": False, "error": "login"}
    url = _clip(body.get("url"), 1000)
    if not re.match(r"^https?://", url):
        return 400, {"ok": False, "error": "url"}
    try:
        price = float(body.get("price")) if body.get("price") not in (None, "") else None
    except (TypeError, ValueError):
        price = None
    blob = _blob()
    items = [i for i in _saves(blob, member_id) if i.get("url") != url]
    if len(items) >= SAVE_LIMIT:
        return 400, {"ok": False, "error": "limit"}
    items.insert(0, {"url": url, "saved_at": _now()[0].isoformat(timespec="seconds"), "title": _clip(body.get("title"), 200),
                     "price": price, "currency": _clip(body.get("currency"), 5).upper() or None, "source": _clip(body.get("source"), 80),
                     "image": _clip(body.get("image"), 1000) if re.match(r"^https?://", str(body.get("image") or "")) else "",
                     "grade": _clip(body.get("grade"), 3), "entity": _clip(body.get("entity"), 120)})
    _put(blob, f"board/saves/{member_id}.json", {"items": items})
    return 200, {"ok": True, "urls": [i["url"] for i in items]}


def unsave_item(body: dict, member_id: str | None) -> tuple[int, dict]:
    if not member_id:
        return 401, {"ok": False, "error": "login"}
    blob = _blob()
    url = _clip(body.get("url"), 1000)
    items = [i for i in _saves(blob, member_id) if i.get("url") != url]
    _put(blob, f"board/saves/{member_id}.json", {"items": items})
    return 200, {"ok": True, "urls": [i["url"] for i in items]}


# ── 원하는 매물 알림: 모델·최소 등급·세금까지 낸 최대 총액 → 조건에 맞는 새 매물이 나오면 메일 ──
WANT_LIMIT = 20
GRADE_ORDER = ["N", "S", "A", "B", "C", "D"]


def _wants(blob, member_id: str) -> list[dict]:
    return (_read(blob, f"board/wants/{member_id}.json") or {}).get("items") or []


def _current_records() -> list[tuple[dict, list]]:
    """지금 색인의 (매물, 연결된 모델들)"""
    import sys  # noqa: WPS433
    from pathlib import Path  # noqa: WPS433
    root = Path(__file__).resolve().parents[1]
    if str(root) not in sys.path:
        sys.path.insert(0, str(root))
    from search_index import DEFAULT_SEARCH_INDEX_PATH, load_search_index  # noqa: WPS433
    path = Path(DEFAULT_SEARCH_INDEX_PATH)
    records = load_search_index(path if path.is_absolute() else root / path)
    return [(r.get("final_output") or {}, r.get("entity_ids") or []) for r in records]


def want_matches(want: dict, records) -> list[dict]:
    """판매 중이고, 그 모델(하위 모델 포함)이고, 등급이 최소 등급 이상이고, 도착 총액이 상한 이하인 매물 (싼 순)"""
    import sys  # noqa: WPS433
    from pathlib import Path  # noqa: WPS433
    root = Path(__file__).resolve().parents[1]
    if str(root) not in sys.path:
        sys.path.insert(0, str(root))
    from condition_grade import grade_of  # noqa: WPS433
    from landed_cost import landed_total  # noqa: WPS433
    floor = GRADE_ORDER.index(want["grade"]) if want.get("grade") in GRADE_ORDER else len(GRADE_ORDER) - 1
    out = []
    for final, entity_ids in records:
        if want["entity"] not in entity_ids or final.get("sold_quality") != "asking":
            continue
        if (final.get("entity_note") or "") in ("too_cheap",):
            continue
        grade = grade_of(final.get("source"), final.get("condition_raw"), final.get("title_raw"))[0] or final.get("image_grade")  # 사진 추정 포함
        if grade not in GRADE_ORDER or GRADE_ORDER.index(grade) > floor:
            continue  # 등급을 모르는 매물은 알리지 않음 (컨디션을 확인할 수 없어서)
        cost = landed_total(final, want["currency"], want["dest"])
        total = (cost or {}).get("total")
        if total is None or total > want["max_total"]:
            continue
        out.append({"url": final.get("source_url"), "title": final.get("title_raw"), "source": final.get("source"), "grade": grade,
                    "total": total, "listed": cost["listed"], "listed_currency": cost["currency"], "image": final.get("image_url")})
    return sorted(out, key=lambda m: m["total"])


def want_add(body: dict, member_id: str | None, records=None) -> tuple[int, dict]:
    if not member_id:
        return 401, {"ok": False, "error": "login"}
    entity = _clip(body.get("entity"), 120)
    if not re.fullmatch(r"leica:[a-z0-9:._+-]+", entity):
        return 400, {"ok": False, "error": "entity"}
    grade = str(body.get("grade") or "B").upper()
    currency = str(body.get("currency") or "").upper()[:3]
    dest = str(body.get("dest") or "").upper()[:2]
    try:
        max_total = float(body.get("max_total"))
    except (TypeError, ValueError):
        return 400, {"ok": False, "error": "price"}
    import sys  # noqa: WPS433
    from pathlib import Path  # noqa: WPS433
    root = Path(__file__).resolve().parents[1]
    if str(root) not in sys.path:
        sys.path.insert(0, str(root))
    from landed_cost import load_rates, load_rules  # noqa: WPS433
    if grade not in GRADE_ORDER or max_total <= 0 or currency not in load_rates() or dest not in (load_rules().get("destinations") or {}):
        return 400, {"ok": False, "error": "bad"}
    blob = _blob()
    items = [w for w in _wants(blob, member_id) if not (w.get("entity") == entity and w.get("grade") == grade)]
    if len(items) >= WANT_LIMIT:
        return 400, {"ok": False, "error": "limit"}
    want = {"id": secrets.token_hex(4), "entity": entity, "name": _clip(body.get("name"), 120) or entity, "grade": grade,
            "max_total": max_total, "currency": currency, "dest": dest, "since": _now()[0].isoformat(timespec="seconds")}
    matches = want_matches(want, records if records is not None else _current_records())
    want["notified"] = [m["url"] for m in matches]  # 지금 있는 매물은 화면에서 보여 주고, 메일은 새로 나오는 것만
    items.append(want)
    _put(blob, f"board/wants/{member_id}.json", {"items": items})
    member = _member(blob, member_id) or {}
    return 200, {"ok": True, "want": {k: v for k, v in want.items() if k != "notified"}, "matches": matches[:10],
                 "alerts": bool((member.get("alerts") or {}).get("email"))}


def want_remove(body: dict, member_id: str | None) -> tuple[int, dict]:
    if not member_id:
        return 401, {"ok": False, "error": "login"}
    blob = _blob()
    items = [w for w in _wants(blob, member_id) if w.get("id") != str(body.get("id") or "")]
    _put(blob, f"board/wants/{member_id}.json", {"items": items})
    return 200, {"ok": True}


def list_wants(member_id: str | None, records=None) -> tuple[int, dict]:
    if not member_id:
        return 401, {"ok": False, "error": "login"}
    items = _wants(_blob(), member_id)
    records = records if records is not None else (_current_records() if items else [])
    out = []
    for want in items:
        matches = want_matches(want, records)
        out.append({**{k: v for k, v in want.items() if k != "notified"}, "count": len(matches), "matches": matches[:5]})
    return 200, {"ok": True, "items": out}


def _want_events(wants: list[dict], records) -> list[dict]:
    """지난번 알린 뒤 새로 조건에 맞게 된 매물. wants를 고쳐 놓음(notified)."""
    events = []
    for want in wants:
        matches = want_matches(want, records)
        seen = set(want.get("notified") or [])
        for match in matches:
            if match["url"] not in seen:
                events.append({"kind": "want", "want": want, "match": match})
        want["notified"] = sorted(seen | {m["url"] for m in matches})[-500:]
    return events


def _current_listings() -> dict[str, dict]:
    """원래 주소 → 지금 색인의 매물 (가격·판매 상태). 검색 색인을 불러옴 (파일이 바뀔 때만 다시 읽음)."""
    import sys  # noqa: WPS433
    from pathlib import Path  # noqa: WPS433
    root = Path(__file__).resolve().parents[1]
    if str(root) not in sys.path:
        sys.path.insert(0, str(root))
    from search_index import DEFAULT_SEARCH_INDEX_PATH, load_search_index  # noqa: WPS433
    path = Path(DEFAULT_SEARCH_INDEX_PATH)
    records = load_search_index(path if path.is_absolute() else root / path)
    return {(r.get("final_output") or {}).get("source_url"): (r.get("final_output") or {}) for r in records}


def list_saves(member_id: str | None, with_status: bool = False, current=None) -> tuple[int, dict]:
    if not member_id:
        return 401, {"ok": False, "error": "login"}
    items = _saves(_blob(), member_id)
    if not with_status:
        return 200, {"ok": True, "urls": [i["url"] for i in items]}
    now = current if current is not None else _current_listings()
    out = []
    for item in items:
        listing = now.get(item["url"])
        status = "gone" if not listing else ("asking" if listing.get("sold_quality") == "asking" else "sold")
        out.append({**item, "now": {"status": status, "price": (listing or {}).get("parsed_price_numeric"),
                                    "currency": (listing or {}).get("currency")}})
    return 200, {"ok": True, "items": out}


# ── 운영자 ──
def authorized(cookie_value: str) -> bool:
    expected = os.environ.get("OWNER_DASHBOARD_KEY", "")
    return len(expected) >= 16 and bool(cookie_value) and hmac.compare_digest(cookie_value, expected)


def owner_action(form: dict) -> None:
    """hold(가리기) · restore(되살리기) · remove(지우기) · purge(지운 지 REMOVED_DAYS일 지난 것 비우기)."""
    blob = _blob()
    action, path = form.get("action", ""), form.get("path", "")
    if action == "purge":  # 지운 날 기준이 아니라 글·댓글을 쓴 날 기준 (지운 날은 파일 안에만 있음)
        cutoff = (dt.datetime.now(KST) - dt.timedelta(days=REMOVED_DAYS)).strftime("%Y%m%d")
        old = [i.url for i in _names(blob, "board/removed/") if (STAMP.findall(i.pathname) or ["99999999"])[-1][:8] < cutoff]
        if old:
            blob.delete(old)
        return
    if not path.startswith(("board/posts/", "board/comments/", "board/held/")):
        return
    items = [i for i in _names(blob, path) if i.pathname == path]
    if not items:
        return
    is_comment = "/" in path.split("/", 2)[2]  # 댓글은 <글id>/<댓글id>, 글은 <글id>~…
    to = {"hold": "held", "remove": "removed", "restore": "comments" if is_comment else "posts"}.get(action)
    if to:
        _move(blob, items[0], to)


def owner_page() -> str:
    blob = _blob()
    held = sorted(_names(blob, "board/held/"), key=lambda i: i.pathname, reverse=True)[:50]
    recent = sorted(_names(blob, "board/posts/"), key=lambda i: i.pathname, reverse=True)[:30]
    comments = sorted(_names(blob, "board/comments/"), key=lambda i: i.pathname.split("/")[-1], reverse=True)[:30]
    reports: dict[str, int] = {}
    for item in _names(blob, "board/reports/"):
        reports[item.pathname.split("/")[2]] = reports.get(item.pathname.split("/")[2], 0) + 1

    def rows(items, buttons):
        entries = _read_many(blob, items)
        out = []
        for item, entry in zip(items, entries):
            entry = entry or {}
            key = f"{entry.get('post_id')}~{entry.get('id')}" if entry.get("post_id") else entry.get("id", "")
            forms = "".join(f'<form method="post"><input type="hidden" name="action" value="{a}"><input type="hidden" name="path" value="{html.escape(item.pathname)}"><button>{label}</button></form>'
                            for a, label in buttons)
            out.append(f"<tr><td>{html.escape(entry.get('created_at', '')[:16])}</td><td>{html.escape(entry.get('nick', ''))}</td>"
                       f"<td><b>{html.escape(entry.get('title', ''))}</b> {html.escape((entry.get('body') or '')[:300])}</td>"
                       f"<td>{reports.get(key, 0)}</td><td class=act>{forms}</td></tr>")
        return "".join(out) or '<tr><td colspan=5>없음</td></tr>'

    head = "<tr><th>시각</th><th>닉네임</th><th>내용</th><th>신고</th><th></th></tr>"
    return ("<!doctype html><html lang=ko><meta charset=utf-8><meta name=robots content=noindex><title>게시판 관리</title>"
            "<style>body{font:14px/1.5 -apple-system,sans-serif;margin:24px;color:#16181a}table{border-collapse:collapse;width:100%;margin-bottom:28px}"
            "td,th{border-bottom:1px solid #ddd;padding:6px 8px;text-align:left;vertical-align:top}.act form{display:inline}button{margin-right:4px}</style>"
            "<h1>게시판 관리</h1><p>신고 3명이면 자동으로 가려져 아래 '가려진 글'에 옵니다. 지운 글은 30일 보관 뒤 비웁니다.</p>"
            f"<h2>가려진 글·댓글 ({len(held)})</h2><table>{head}{rows(held, [('restore', '되살리기'), ('remove', '지우기')])}</table>"
            f"<h2>최근 글</h2><table>{head}{rows(recent, [('hold', '가리기'), ('remove', '지우기')])}</table>"
            f"<h2>최근 댓글</h2><table>{head}{rows(comments, [('hold', '가리기'), ('remove', '지우기')])}</table>"
            '<form method="post"><input type="hidden" name="action" value="purge"><button>지운 지 30일 지난 것 비우기</button></form>')


class handler(BaseHTTPRequestHandler):
    def _send(self, status: int, payload, content_type: str = "application/json", cache: str = "no-store", extra: dict | None = None) -> None:
        body = payload if isinstance(payload, bytes) else (payload.encode() if isinstance(payload, str) else json.dumps(payload, ensure_ascii=False).encode())
        self.send_response(status)
        self.send_header("content-type", content_type)
        self.send_header("cache-control", cache)
        for name, value in (extra or {}).items():
            self.send_header(name, value)
        self.end_headers()
        self.wfile.write(body)

    def _query(self) -> dict:
        return {k: v[0] for k, v in parse_qs(urlparse(self.path).query).items()}

    def _cookie(self, name: str) -> str:
        cookie = SimpleCookie(self.headers.get("cookie") or "")
        return cookie[name].value if name in cookie else ""

    def _owner(self) -> bool:
        return authorized(self._cookie(COOKIE))

    def _member_id(self) -> str | None:
        return member_from_cookie(self._cookie(MEMBER_COOKIE))

    def do_GET(self):  # noqa: N802
        query = self._query()
        try:
            if query.get("r") == "owner":
                if not self._owner():
                    return self._send(401, "<!doctype html><meta charset=utf-8><p>권한이 없습니다. /owner/usage?key=… 로 먼저 들어가 주세요.</p>", "text/html; charset=utf-8")
                return self._send(200, owner_page(), "text/html; charset=utf-8", extra={"x-robots-tag": "noindex, nofollow"})
            if query.get("r") == "me":
                return self._send(200, me(self._member_id()))
            if query.get("r") == "alerts":  # Vercel Cron (매일)
                secret = os.environ.get("CRON_SECRET", "")
                if not secret:
                    return self._send(503, {"ok": False, "error": "cron_not_configured"})
                if not hmac.compare_digest((self.headers.get("authorization") or "").encode(), f"Bearer {secret}".encode()):
                    return self._send(401, {"ok": False})
                result = run_alerts()
                try:
                    result["retention"] = run_retention()
                except Exception as e:  # noqa: BLE001 (정리 실패가 알림 응답을 막지 않게)
                    result["retention"] = {"error": str(e)[:200]}
                return self._send(200, result)
            if query.get("r") == "unsub":
                done = unsubscribe(query.get("m", ""), query.get("s", ""))
                message = "알림을 껐습니다. · Email alerts are turned off." if done else "링크가 맞지 않습니다. · This link is not valid."
                return self._send(200 if done else 400, f"<!doctype html><meta charset=utf-8><meta name=robots content=noindex><p style='font:16px sans-serif;margin:40px'>{message} <a href='https://camerabridge.io/'>camerabridge.io</a></p>", "text/html; charset=utf-8")
            if query.get("r") == "wants":
                status, payload = list_wants(self._member_id())
                return self._send(status, payload)
            if query.get("r") == "saves":
                status, payload = list_saves(self._member_id(), with_status=bool(query.get("full")))
                return self._send(status, payload)
            if query.get("id"):  # 내 글 표시(mine) 때문에 캐시하지 않음
                status, payload = read_post(query["id"], self._member_id())
                return self._send(status, payload)
            try:
                page = int(query.get("page") or 1)
            except ValueError:
                page = 1
            category = query.get("category") if query.get("category") in CATEGORIES else ""
            # 목록은 잠깐 저장(캐시). 글쓴이는 쓰거나 지운 직후 ?fresh=… 로 새 목록을 받음
            cache = "no-store" if query.get("fresh") else "public, s-maxage=15, stale-while-revalidate=45"
            return self._send(200, list_posts(category, page), cache=cache)
        except Exception:  # noqa: BLE001
            return self._send(503, {"ok": False, "error": "unavailable"})

    def do_POST(self):  # noqa: N802
        length = min(int(self.headers.get("content-length") or 0), 32_000)
        raw = self.rfile.read(length) or b""
        query = self._query()
        try:
            if query.get("r") == "owner":
                if not self._owner():
                    return self._send(401, "권한이 없습니다.", "text/plain; charset=utf-8")
                owner_action({k: v[0] for k, v in parse_qs(raw.decode()).items()})
                return self._send(303, b"", "text/plain", extra={"location": "/owner/board"})
            try:
                body = json.loads(raw or b"{}")
            except ValueError:
                return self._send(400, {"ok": False, "error": "bad_json"})
            if not isinstance(body, dict):
                return self._send(400, {"ok": False, "error": "bad_request"})
            action = body.get("action")
            member_id = self._member_id()
            if action == "login":
                status, payload, session = login(body)
                cookie = (f"{MEMBER_COOKIE}={session}; Path=/api/board; Max-Age={SESSION_DAYS * 86400}; HttpOnly; Secure; SameSite=Lax"
                          if session else None)
                return self._send(status, payload, extra={"set-cookie": cookie} if cookie else None)
            if action == "logout":
                return self._send(200, {"ok": True}, extra={"set-cookie": f"{MEMBER_COOKIE}=; Path=/api/board; Max-Age=0; HttpOnly; Secure; SameSite=Lax"})
            if action == "nick":
                status, payload = set_nick(body, member_id)
            elif action == "post":
                status, payload = create_post(body, member_id)
            elif action == "comment":
                status, payload = create_comment(body, member_id)
            elif action == "delete":
                status, payload = delete_entry(body, member_id)
            elif action == "alerts_on":
                status, payload = alerts_on(body, member_id)
            elif action == "alerts_off":
                status, payload = alerts_off(member_id)
            elif action == "save":
                status, payload = save_item(body, member_id)
            elif action == "unsave":
                status, payload = unsave_item(body, member_id)
            elif action == "want":
                status, payload = want_add(body, member_id)
            elif action == "unwant":
                status, payload = want_remove(body, member_id)
            elif action == "report":
                status, payload = report(body, self.headers)
            else:
                status, payload = 400, {"ok": False, "error": "action"}
            return self._send(status, payload)
        except Exception:  # noqa: BLE001
            return self._send(503, {"ok": False, "error": "unavailable"})
