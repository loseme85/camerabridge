"""운영자 정보·개인정보처리방침·이용약관·Impressum 정적 페이지를 만든다.

출력: ko|en|ja/{about,privacy,terms}/index.html, impressum/index.html (독일어·영어)
운영자 정보가 바뀌면 OPERATOR만 고치고 다시 실행한다: python3 scripts/build_legal_pages.py
footer(lang)는 모델 페이지(build_model_pages.py)도 같이 쓴다. 첫 화면(beta.html) 아래쪽 문구는 footer.* 번역에 따로 있다.
"""
from __future__ import annotations

import argparse
import html
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = "https://camerabridge.io"
LANGS = ("ko", "en", "ja")
UPDATED = "2026-10-29"

# 통신판매업 신고번호·전화는 사장님이 정하면 채운다 (비어 있으면 화면에 안 나옴)
OPERATOR = {
    # 카메라브릿지를 운영하는 회사 이름 (2026-10-29 이름만 정함, 아직 사업자 등록 전 → 법적 운영자는 아래 사업자)
    "brand": "thehingemeta",
    "name": {"ko": "브로콜리스튜디오", "en": "Broccoli Studio", "ja": "Broccoli Studio（ブロッコリースタジオ）"},
    "rep": {"ko": "박창대", "en": "Changdae Park", "ja": "パク・チャンデ（Changdae Park）"},
    "biz_no": "512-22-00825",
    "mail_order_no": "",
    "phone": "",
    "address": {"ko": "서울시 노원구 상계동 450 210호",
                "en": "Room 210, 450 Sanggye-dong, Nowon-gu, Seoul, Republic of Korea",
                "ja": "大韓民国 ソウル特別市 蘆原区 上渓洞 450 210号"},
    "email": "thehingemeta@gmail.com",
}

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500&family=Newsreader:ital,opsz,wght@0,6..72,400;0,6..72,500;1,6..72,400&family=Noto+Serif+KR:wght@400;500;600&display=swap">')

# 첫 화면과 같은 인쇄 카탈로그 틀: 세리프 본문, 굵은 줄 + 가는 줄, 각진 모서리, 장식 없음
CSS = """
:root{--bg:#fbfaf7;--text:#16181a;--soft:#55595c;--muted:#878b8d;--border:#d9d7d0;--accent:#1f4a3a;
--serif:"Newsreader","Noto Serif KR",Georgia,serif;--sans:"Inter","Pretendard Variable",system-ui,-apple-system,sans-serif}
@media (prefers-color-scheme:dark){:root{--bg:#141617;--text:#e8eaea;--soft:#a9afb2;--muted:#7d8488;--border:#2f3436;--accent:#8cc5ad}}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--text);font:17px/1.85 var(--serif);font-optical-sizing:auto;word-break:keep-all;overflow-wrap:anywhere;-webkit-font-smoothing:antialiased}
main{max-width:720px;margin:0 auto;padding:0 20px 72px;counter-reset:sec}
.mast{display:flex;flex-wrap:wrap;align-items:baseline;justify-content:space-between;gap:6px 24px;border-bottom:2px solid var(--text);padding:28px 0 10px}
.mast .home{font-family:var(--serif);font-size:20px;color:var(--text);text-decoration:none;letter-spacing:-0.01em}
.mast .home i{color:var(--muted);font-size:15px}
.mast nav{font:13px/1.4 var(--sans);display:flex;flex-wrap:wrap;gap:4px 16px}
.mast nav a{color:var(--soft);text-decoration:none}
.mast nav a:hover{color:var(--text);text-decoration:underline;text-underline-offset:3px}
.mast nav a[aria-current]{color:var(--text);border-bottom:1px solid var(--text)}
h1{font-family:var(--serif);font-weight:400;font-size:clamp(34px,6vw,48px);line-height:1.1;letter-spacing:-0.02em;margin:44px 0 32px}
h2{font-family:var(--serif);font-weight:500;font-size:21px;line-height:1.35;margin:48px 0 10px;display:grid;grid-template-columns:44px 1fr;align-items:baseline}
h2::before{counter-increment:sec;content:counter(sec,decimal-leading-zero);font:400 13px/1 var(--sans);color:var(--muted);font-variant-numeric:tabular-nums}
h2~p,h2~ul,h2~.table{margin-left:44px}
p{margin:0 0 14px}
ul{margin:0 0 14px;padding-left:1.1em}
li{margin:0 0 6px}
li::marker{color:var(--muted)}
.note{font:13px/1.6 var(--sans);color:var(--muted)}
a{color:var(--accent);text-underline-offset:3px;text-decoration-thickness:1px}
table{width:100%;border-collapse:collapse;margin:0 0 8px;border-top:1px solid var(--text)}
th,td{text-align:left;vertical-align:baseline;border-bottom:1px solid var(--border);padding:11px 12px 11px 0}
th{font:500 13px/1.5 var(--sans);color:var(--soft);width:30%}
td{font-size:16px}
.table{overflow-x:auto}
@media (max-width:560px){body{font-size:16px}h2{grid-template-columns:1fr}h2::before{margin-bottom:6px}h2~p,h2~ul,h2~.table{margin-left:0}th{width:38%}}
"""
FOOTER_CSS = """
footer.legal{max-width:720px;margin:0 auto;padding:0 20px 56px;color:var(--muted);font:12px/1.65 "Inter","Pretendard Variable",system-ui,-apple-system,sans-serif}
footer.legal .rule{border-top:2px solid var(--text);border-bottom:1px solid var(--text);height:5px;margin-bottom:18px}
footer.legal .mark{font:20px/1.3 "Newsreader","Noto Serif KR",Georgia,serif;color:var(--text);margin:0 0 2px;letter-spacing:-0.01em}
footer.legal .mark i{color:var(--muted);font-size:15px}
footer.legal p{margin:0 0 12px}
footer.legal nav{display:flex;flex-wrap:wrap;gap:2px 18px;margin:0 0 14px;font-size:13px}
footer.legal a{color:var(--soft);text-decoration:none}
footer.legal a:hover{color:var(--text);text-decoration:underline;text-underline-offset:3px}
footer.legal .tm{max-width:38em}
"""

FOOT = {
    "ko": {"tm": "Leica는 Leica Camera AG의 상표입니다. 카메라브릿지는 Leica Camera AG와 관계없는 독립 서비스입니다. 가격·재고는 각 매장 정보이며, 일부 링크는 제휴 링크일 수 있습니다.",
           "models": "모델별 시세", "about": "운영자 정보", "privacy": "개인정보처리방침", "terms": "이용약관", "home": "카메라브릿지"},
    "en": {"tm": "Leica is a trademark of Leica Camera AG. Camera Bridge is an independent service and is not affiliated with Leica Camera AG. Prices and stock come from each shop, and some links may be affiliate links.",
           "models": "Prices by model", "about": "About & contact", "privacy": "Privacy", "terms": "Terms", "home": "Camera Bridge"},
    "ja": {"tm": "Leica は Leica Camera AG の商標です。Camera Bridge は Leica Camera AG とは関係のない独立したサービスです。価格・在庫は各店舗の情報で、一部のリンクはアフィリエイトリンクの場合があります。",
           "models": "モデル別相場", "about": "運営者情報", "privacy": "プライバシーポリシー", "terms": "利用規約", "home": "Camera Bridge"},
}


def footer(lang: str) -> str:
    """모든 정적 페이지 아래쪽(판권면): 겹줄 + 브랜드·이메일 + 법적 고지 링크 + 상표·제휴 안내 (운영자 실명·사업자번호는 운영자 정보 페이지에만)"""
    f, o = FOOT[lang], OPERATOR
    links = [f'<a href="/{lang}/leica/">{f["models"]}</a>'] + [f'<a href="/{lang}/{page}/">{f[page]}</a>' for page in ("about", "privacy", "terms")]
    return (f'<footer class="legal"><div class="rule"></div><p class="mark">{f["home"]} <i>by {o["brand"]}</i></p>'
            f'<p><a href="mailto:{o["email"]}">{o["email"]}</a></p>'
            f'<nav>{"".join(links)}<a href="/impressum/">Impressum</a></nav><p class="tm">{f["tm"]}</p></footer>')


def _rows(pairs) -> str:
    return '<div class="table"><table>' + "".join(f"<tr><th>{k}</th><td>{v}</td></tr>" for k, v in pairs) + "</table></div>"


def _list(items) -> str:
    return "<ul>" + "".join(f"<li>{i}</li>" for i in items) + "</ul>"


MAIL = f'<a href="mailto:{OPERATOR["email"]}">{OPERATOR["email"]}</a>'
FEEDBACK_LINK = {"ko": '첫 화면의 "의견 보내기"', "en": 'the "Send feedback" button on the home page',
                 "ja": "トップページの「ご意見を送る」"}


WHY = {
    "ko": ('<h2 id="why">만든 이유</h2>'
           "<p>저는 라이카 공식 스토어에서 VIP 고객을 관리했고, 개인 프리미엄 샵에서 매니저로 일했습니다. 그때 가장 힘들었던 일은 매입이었습니다. "
           "손님이 가져온 렌즈를 얼마에 사야 하는지, 세대와 상태와 구성품에 따라 값이 몇 배씩 달라지는데 그 자리에서 답해야 했습니다. "
           "경력이 쌓이기 전에는 늘 불안했고, 계산이 빠르지 않은 동료들에게는 더 큰 스트레스였습니다.</p>"
           "<p>지금은 전혀 다른 일을 하지만 그때의 갈증이 남아 카메라브릿지를 만들었습니다. 여러 나라 매장의 매물을 모아 같은 모델끼리 정확히 묶어 보여 주는 것이 목표입니다. "
           "가격 때문에 생기는 스트레스가 조금이라도 줄어 매입하고, 팔고, 사는 일이 쉬워지기를 바랍니다.</p>"
           "<p>카메라브릿지는 Leica Camera AG와 관계없이 혼자 운영하는 독립 서비스입니다.</p>"),
    "en": ('<h2 id="why">Why I built this</h2>'
           "<p>I used to look after VIP clients at an official Leica Store, and later managed a private premium camera shop. "
           "The hardest part of the job was always buying. Someone brings in a lens, and you have to name a price on the spot, "
           "knowing that version, condition and what comes in the box can change its value several times over. "
           "Before I had the experience, it made me anxious every time, and it was even harder for colleagues who weren't quick with numbers.</p>"
           "<p>I work in a different field now, but that frustration stayed with me, so I built Camera Bridge. "
           "It collects listings from shops in many countries and groups them precisely by model, version and generation. "
           "I hope it takes some of the stress out of pricing, whether you're buying stock, selling it, or buying a camera for yourself.</p>"
           "<p>Camera Bridge is an independent, one-person service with no connection to Leica Camera AG.</p>"),
    "ja": ('<h2 id="why">つくった理由</h2>'
           "<p>私はライカ公式ストアで VIP のお客さまを担当し、その後は個人のプレミアムカメラ店でマネージャーをしていました。いちばん大変だったのは買取です。"
           "お客さまが持ち込んだレンズにその場で値をつけなければならないのに、型や世代、状態、付属品で価格は何倍も変わります。"
           "経験が浅いうちは毎回不安で、計算が得意でない同僚にとってはなおさら負担でした。</p>"
           "<p>今はまったく別の仕事をしていますが、あのときのもどかしさが残っていて Camera Bridge をつくりました。"
           "各国の店の在庫を集め、同じモデル・同じ世代ごとに正確にまとめて見せることを目指しています。"
           "価格にまつわるストレスが少しでも減り、買取・販売・購入が楽になればうれしいです。</p>"
           "<p>Camera Bridge は Leica Camera AG とは関係のない、個人で運営する独立したサービスです。</p>"),
}


def about_body(lang: str) -> tuple[str, str]:
    o = OPERATOR
    if lang == "ko":
        pairs = [("서비스", "카메라브릿지 (camerabridge.io) — 라이카 중고 매물·시세 검색"),
                 ("회사", f'{o["brand"]} (사업자 등록 전까지 아래 사업자가 운영)'), ("상호", o["name"]["ko"]),
                 ("대표자", o["rep"]["ko"]), ("사업자등록번호", o["biz_no"]), ("주소", o["address"]["ko"]),
                 ("이메일", MAIL), ("호스팅 제공자", "Vercel Inc. (미국)")]
        if o["mail_order_no"]:
            pairs.insert(4, ("통신판매업 신고번호", o["mail_order_no"]))
        if o["phone"]:
            pairs.append(("전화", o["phone"]))
        body = (_rows(pairs) + WHY[lang]
                + "<h2>서비스 성격</h2><p>카메라브릿지는 여러 나라 카메라 매장이 공개한 라이카 중고 매물과 가격을 모아 보여 주는 검색 서비스입니다. "
                  "물건을 직접 팔거나 거래를 중개하지 않으며, 구매·결제·배송·반품은 각 매장과 직접 이루어집니다.</p>"
                + "<h2>제휴 링크 안내</h2><p>일부 매장 링크(예: eBay)는 제휴(어필리에이트) 링크일 수 있습니다. 이 링크로 구매하면 카메라브릿지가 매장으로부터 수수료를 받을 수 있으며, "
                  "구매자가 내는 가격은 달라지지 않습니다. 수수료 여부는 검색 결과 순서와 가격 표시에 영향을 주지 않습니다.</p>"
                + "<h2>상표</h2><p>Leica 및 관련 제품명은 Leica Camera AG의 상표입니다. 카메라브릿지는 Leica Camera AG의 공식 서비스가 아니며 후원·제휴 관계가 없습니다. "
                  "매물 제목·사진은 각 매장의 것이며 원래 매장 페이지로 연결합니다.</p>"
                + f"<h2>매장 문의</h2><p>매물 표시를 고치거나 빼고 싶은 매장, 데이터 연결을 원하는 매장은 {MAIL}로 연락해 주세요.</p>")
        return "운영자 정보", body
    if lang == "ja":
        pairs = [("サービス", "Camera Bridge（camerabridge.io）— ライカ中古在庫・相場検索"),
                 ("会社", f'{o["brand"]}（法人登録までは下記の事業者が運営）'), ("事業者名", o["name"]["ja"]),
                 ("代表者", o["rep"]["ja"]), ("事業者登録番号（韓国）", o["biz_no"]), ("所在地", o["address"]["ja"]),
                 ("メール", MAIL), ("ホスティング", "Vercel Inc.（米国）")]
        if o["mail_order_no"]:
            pairs.insert(4, ("通信販売業申告番号（韓国）", o["mail_order_no"]))
        if o["phone"]:
            pairs.append(("電話", o["phone"]))
        body = (_rows(pairs) + WHY[lang]
                + "<h2>サービスについて</h2><p>Camera Bridge は、各国のカメラ店が公開しているライカ中古在庫と価格をまとめて表示する検索サービスです。"
                  "商品の販売や取引の仲介は行わず、購入・決済・配送・返品は各店舗と直接行っていただきます。</p>"
                + "<h2>アフィリエイトリンクについて</h2><p>一部の店舗リンク（例：eBay）はアフィリエイトリンクの場合があります。リンク経由で購入されると Camera Bridge が店舗から手数料を受け取ることがありますが、"
                  "購入価格は変わりません。手数料の有無は検索結果の順序や価格表示に影響しません。</p>"
                + "<h2>商標</h2><p>Leica および関連製品名は Leica Camera AG の商標です。Camera Bridge は Leica Camera AG の公式サービスではなく、提携・後援関係もありません。"
                  "商品名・写真は各店舗のもので、元の店舗ページへリンクしています。</p>"
                + f"<h2>店舗の方へ</h2><p>掲載内容の修正・削除やデータ連携のご相談は {MAIL} までご連絡ください。</p>")
        return "運営者情報", body
    pairs = [("Service", "Camera Bridge (camerabridge.io) — used Leica listings and price search"),
             ("Company", f'{o["brand"]} (operated by the business below until it is registered)'), ("Operator", o["name"]["en"]),
             ("Owner", o["rep"]["en"]), ("Business registration no. (Korea)", o["biz_no"]), ("Address", o["address"]["en"]),
             ("Email", MAIL), ("Hosting", "Vercel Inc. (USA)")]
    if o["mail_order_no"]:
        pairs.insert(4, ("Mail-order business reg. no. (Korea)", o["mail_order_no"]))
    if o["phone"]:
        pairs.append(("Phone", o["phone"]))
    body = (_rows(pairs) + WHY[lang]
            + "<h2>What Camera Bridge is</h2><p>Camera Bridge is a search service that collects used Leica listings and prices published by camera shops in several countries. "
              "We do not sell items or broker transactions; purchase, payment, shipping and returns are always between you and the shop.</p>"
            + "<h2>Affiliate disclosure</h2><p>Some shop links (for example eBay) may be affiliate links. If you buy through one, Camera Bridge may earn a commission from the shop "
              "at no extra cost to you. Commissions do not affect the order of results or the prices shown.</p>"
            + "<h2>Trademarks</h2><p>Leica and related product names are trademarks of Leica Camera AG. Camera Bridge is not an official Leica service and is not sponsored by or affiliated with Leica Camera AG. "
              "Listing titles and photos belong to each shop and link back to the original shop page.</p>"
            + f"<h2>For shops</h2><p>To correct or remove a listing, or to connect your inventory data, email {MAIL}.</p>")
    return "About & contact", body


def privacy_body(lang: str) -> tuple[str, str]:
    o = OPERATOR
    if lang == "ko":
        body = (f"<p>{o['name']['ko']}(이하 \"운영자\")는 카메라브릿지(camerabridge.io)를 운영하며 「개인정보 보호법」에 따라 이용자의 개인정보를 보호합니다. "
                "카메라브릿지는 회원 가입 없이 쓸 수 있고, 아래의 최소한의 정보만 처리합니다.</p>"
                + "<h2>1. 처리하는 정보와 목적</h2>" + _rows([
                    ("의견 보내기", "의견 내용, 이메일(선택 입력), 접속지 식별값(IP 주소를 날짜별로 바꾼 해시값, IP 자체는 저장 안 함) — 의견 확인·답장, 스팸 막기(하루 5건 제한)"),
                    ("매장(딜러) 계정", "아이디, 매장 이름, 비밀번호(복원할 수 없는 해시값으로 저장) — 매장 전용 시세 화면 로그인"),
                    ("방문 기록", "접속 나라 코드, 화면 언어·통화, 들어온 사이트 주소(도메인만)·첫 주소, 모바일 여부, 머문 시간, 검색어·고른 모델·결과 수, 매장 링크 클릭, 탭마다 새로 만드는 무작위 번호 — 서비스 개선과 이용 통계. IP 주소·이메일·쿠키는 남기지 않음"),
                    ("방문 통계", "Vercel Web Analytics의 집계 통계(쿠키 없음, 개인 식별 안 함) — 방문 수 확인"),
                ])
                + "<h2>2. 보유 기간</h2>" + _list([
                    "의견: 받은 날부터 1년 (답장이 이어지면 마지막 연락부터 1년)",
                    "매장 계정: 계정을 없앨 때까지",
                    "방문 기록: 기록한 날부터 1년",
                    "기간이 지나거나 목적을 이루면 바로 지웁니다. 전자 파일은 복구할 수 없게 지웁니다.",
                ])
                + "<h2>3. 제3자 제공</h2><p>개인정보를 다른 곳에 팔거나 제공하지 않습니다. 법령에 따른 요청이 있을 때만 예외로 합니다.</p>"
                + "<h2>4. 처리 위탁과 국외 이전</h2><p>서비스 운영을 위해 아래 업체에 정보 보관·전송을 맡깁니다. 정보는 이용 시점에 인터넷으로 전송되며, 위 보유 기간 동안 보관됩니다.</p>"
                + _rows([
                    ("Vercel Inc. (미국)", "사이트 호스팅, 의견·매장 계정·방문 기록 비공개 저장(Vercel Blob), 방문 통계"),
                    ("Telegram FZ-LLC (아랍에미리트)", "새 의견이 오면 운영자에게 의견 내용·이메일을 알림으로 전달"),
                ])
                + "<p>국외 이전을 원하지 않으면 의견 보내기를 쓰지 않거나 이메일을 비워 두시면 됩니다. 다만 사이트 이용 자체는 Vercel을 거칩니다.</p>"
                + "<h2>5. 이용자의 권리</h2><p>자신의 정보를 보거나 고치거나 지우거나 처리를 멈추라고 언제든 요청할 수 있습니다. "
                  f"{MAIL}로 연락하시면 지체 없이 처리합니다. 방문 기록은 사람을 알아볼 수 있는 정보와 연결되지 않아 특정 방문을 골라 지우기 어려울 수 있습니다.</p>"
                + "<h2>6. 쿠키와 브라우저 저장소</h2><p>매장 계정으로 로그인할 때만 로그인 유지용 쿠키(cb_dealer)를 씁니다. "
                  "일반 이용자에게는 쿠키를 쓰지 않으며, 고른 언어·통화·배송 나라를 기억하려고 브라우저 저장소(localStorage)를 씁니다. 브라우저 설정에서 지울 수 있습니다.</p>"
                + "<h2>7. 안전 조치</h2><p>모든 연결은 HTTPS로 암호화하고, 저장 정보는 비공개 저장소에 두며 운영자만 볼 수 있습니다. 비밀번호는 해시값으로만 저장합니다.</p>"
                + "<h2>8. 만 14세 미만</h2><p>카메라브릿지는 만 14세 미만 아동을 대상으로 하지 않으며, 알면서 아동의 정보를 받지 않습니다.</p>"
                + "<h2>9. 개인정보 보호책임자</h2>" + _rows([("책임자", f"{o['rep']['ko']} (대표)"), ("연락처", MAIL)])
                + "<p>개인정보 침해 신고·상담은 개인정보침해신고센터(privacy.kisa.or.kr, 국번 없이 118), 개인정보분쟁조정위원회(kopico.go.kr, 1833-6972)에도 하실 수 있습니다.</p>"
                + f"<h2>10. 바뀔 때</h2><p>이 방침이 바뀌면 이 페이지에 알립니다. 시행일: {UPDATED}</p>")
        return "개인정보처리방침", body
    if lang == "ja":
        body = (f"<p>{o['name']['ja']}（以下「運営者」）は Camera Bridge（camerabridge.io）を運営し、利用者の個人情報を保護します。"
                "Camera Bridge は会員登録なしで使え、以下の最小限の情報のみを扱います。</p>"
                + "<h2>1. 取り扱う情報と目的</h2>" + _rows([
                    ("ご意見の送信", "内容、メールアドレス（任意）、接続元識別値（IP アドレスを日ごとに変換したハッシュ値。IP 自体は保存しません）— 内容の確認・返信、スパム防止（1日5件まで）"),
                    ("店舗（ディーラー）アカウント", "ID、店舗名、パスワード（復元できないハッシュ値で保存）— 店舗専用画面へのログイン"),
                    ("利用記録", "接続国コード、表示言語・通貨、参照元（ドメインのみ）・最初のページ、モバイルかどうか、滞在時間、検索語・選んだモデル・結果数、店舗リンクのクリック、タブごとに作るランダムな番号 — サービス改善と利用統計。IP アドレス・メール・Cookie は残しません"),
                    ("アクセス統計", "Vercel Web Analytics の集計統計（Cookie なし、個人を特定しません）"),
                ])
                + "<h2>2. 保存期間</h2>" + _list([
                    "ご意見：受け取った日から1年（やり取りが続く場合は最後の連絡から1年）",
                    "店舗アカウント：アカウント削除まで",
                    "利用記録：記録した日から1年",
                    "期間が過ぎるか目的を果たした情報は速やかに削除します。",
                ])
                + "<h2>3. 第三者提供</h2><p>法令に基づく場合を除き、個人情報を第三者に販売・提供しません。</p>"
                + "<h2>4. 委託と国外移転</h2>" + _rows([
                    ("Vercel Inc.（米国）", "ホスティング、ご意見・店舗アカウント・利用記録の非公開保存、アクセス統計"),
                    ("Telegram FZ-LLC（アラブ首長国連邦）", "新しいご意見の内容・メールを運営者へ通知"),
                ])
                + f"<h2>5. 利用者の権利</h2><p>ご自身の情報の開示・訂正・削除・利用停止をいつでも求めることができます。{MAIL} までご連絡ください。</p>"
                + "<h2>6. Cookie とブラウザ保存領域</h2><p>店舗アカウントでログインする場合のみログイン維持用 Cookie（cb_dealer）を使います。"
                  "一般の利用者には Cookie を使わず、選んだ言語・通貨・配送先を覚えるためにブラウザの保存領域（localStorage）を使います。</p>"
                + "<h2>7. 安全対策</h2><p>通信はすべて HTTPS で暗号化し、保存情報は非公開の保存先で運営者のみが閲覧します。</p>"
                + "<h2>8. 個人情報保護責任者</h2>" + _rows([("責任者", f"{o['rep']['ja']}（代表）"), ("連絡先", MAIL)])
                + f"<h2>9. 改定</h2><p>改定する場合はこのページでお知らせします。施行日：{UPDATED}</p>")
        return "プライバシーポリシー", body
    body = (f"<p>{o['name']['en']} (\"we\") operates Camera Bridge (camerabridge.io). Camera Bridge works without an account, and we process only the minimal information below. "
            "This policy is written to meet Korea's Personal Information Protection Act and the EU/UK GDPR.</p>"
            + "<h2>1. What we process, why, and on what basis</h2>" + _rows([
                ("Feedback form", "Your message, email (optional), and a sender tag (a daily-rotating hash of your IP address; the IP itself is not stored) — to read and reply to feedback and to block spam (5 per day). Basis: your consent by sending it, and our legitimate interest in preventing abuse."),
                ("Shop (dealer) accounts", "Username, shop name and password (stored only as a one-way hash) — to sign in to the dealer view. Basis: contract with the shop."),
                ("Usage log", "Country code of the connection, interface language and currency, referring site (domain only) and first page, mobile or not, time on page, searches, chosen models, result counts, clicks to shops, and a random ID created per browser tab — to improve the service and count usage. No IP address, email or cookie is kept. Basis: legitimate interest in running and improving the service."),
                ("Analytics", "Aggregated visit statistics from Vercel Web Analytics (cookieless, does not identify you)."),
            ])
            + "<h2>2. How long we keep it</h2>" + _list([
                "Feedback: 1 year from receipt (or from the last message if we keep corresponding)",
                "Shop accounts: until the account is closed",
                "Usage log: 1 year from the day it was recorded",
                "After that, data is deleted without delay.",
            ])
            + "<h2>3. Sharing</h2><p>We do not sell or share personal information, except where required by law.</p>"
            + "<h2>4. Processors and international transfers</h2>" + _rows([
                ("Vercel Inc. (USA)", "Hosting, private storage of feedback, shop accounts and usage log (Vercel Blob), analytics"),
                ("Telegram FZ-LLC (UAE)", "Forwards new feedback (message and email) to the operator as a notification"),
            ])
            + "<p>Data is transferred over the internet when you use the service. Transfers to the US rely on Vercel's standard contractual clauses / data processing terms.</p>"
            + f"<h2>5. Your rights</h2><p>You may ask to access, correct, delete or restrict the processing of your information, object to processing, or withdraw consent, at any time by emailing {MAIL}. "
              "If you are in the EU/UK you may also complain to your local data protection authority. Usage-log entries are not linked to anything that identifies you, so we may not be able to single out a particular visit.</p>"
            + "<h2>6. Cookies and browser storage</h2><p>We set a cookie (cb_dealer) only when a shop signs in to keep the session; it is strictly necessary. "
              "Regular visitors get no cookies. We use your browser's local storage to remember the language, currency and shipping country you chose; you can clear it in your browser settings.</p>"
            + "<h2>7. Security</h2><p>All connections use HTTPS. Stored data is kept in private storage that only the operator can access, and passwords are stored only as hashes.</p>"
            + "<h2>8. Children</h2><p>Camera Bridge is not directed to children under 14 (under 16 in the EU), and we do not knowingly collect their information.</p>"
            + "<h2>9. Controller and contact</h2>" + _rows([("Controller", f"{o['name']['en']}, {o['address']['en']}"), ("Privacy contact", f"{o['rep']['en']} — {MAIL}")])
            + f"<h2>10. Changes</h2><p>We will post any changes on this page. Effective: {UPDATED}</p>")
    return "Privacy policy", body


def terms_body(lang: str) -> tuple[str, str]:
    if lang == "ko":
        items = [
            ("1. 서비스", "카메라브릿지는 여러 매장이 공개한 라이카 중고 매물·가격을 모아 검색하게 해 주는 무료 정보 서비스입니다. 회원 가입 없이 쓸 수 있습니다."),
            ("2. 정보의 정확성", "가격·재고·상태·예상 총액(배송비·관세 등)은 매장 정보와 추정치를 바탕으로 하며, 늦게 반영되거나 틀릴 수 있습니다. 환산 가격은 참고용 환율을 씁니다. 구매 전에 반드시 매장 원래 페이지에서 확인해 주세요."),
            ("3. 거래", "카메라브릿지는 물건을 팔거나 거래를 중개하지 않습니다. 구매·결제·배송·반품·보증은 이용자와 매장 사이의 일이며, 운영자는 그 거래에 책임지지 않습니다."),
            ("4. 외부 링크와 제휴", "매물 링크는 매장 사이트로 연결됩니다. 일부는 제휴 링크일 수 있으며 구매 가격은 달라지지 않습니다."),
            ("5. 매장 계정", "매장 계정은 운영자가 만들어 드립니다. 아이디·비밀번호는 매장이 관리하며 다른 사람과 나누어 쓰지 않습니다. 매장 화면의 데이터는 매장 내부 참고용으로만 씁니다."),
            ("6. 금지 행위", "서비스를 방해하는 행위(과도한 자동 요청, 보안 우회, 다른 사람 계정 사용)와 법을 어기는 행위를 금지합니다."),
            ("7. 권리", "매물 제목·사진은 각 매장의 것입니다. Leica는 Leica Camera AG의 상표이며 카메라브릿지는 Leica Camera AG와 관계없습니다."),
            ("8. 책임 제한", "운영자는 고의나 중대한 과실이 없는 한, 정보 오류나 서비스 중단으로 생긴 손해에 책임지지 않습니다. 서비스는 예고 없이 바뀌거나 멈출 수 있습니다."),
            ("9. 약관 변경", "약관을 바꾸면 이 페이지에 시행일과 함께 알립니다."),
            ("10. 준거법", "이 약관은 대한민국 법을 따르며, 분쟁은 민사소송법에 따른 관할 법원에서 다룹니다."),
        ]
        return "이용약관", "".join(f"<h2>{h}</h2><p>{p}</p>" for h, p in items) + f'<p class="note">시행일: {UPDATED} · 문의 {MAIL}</p>'
    if lang == "ja":
        items = [
            ("1. サービス", "Camera Bridge は、各店舗が公開するライカ中古在庫・価格をまとめて検索できる無料の情報サービスです。会員登録は不要です。"),
            ("2. 情報の正確性", "価格・在庫・状態・到着時の目安（送料・関税など）は店舗情報と推定に基づき、反映の遅れや誤りがある場合があります。購入前に必ず店舗の元ページでご確認ください。"),
            ("3. 取引", "Camera Bridge は商品の販売や取引の仲介を行いません。購入・決済・配送・返品・保証は利用者と店舗との間のもので、運営者は責任を負いません。"),
            ("4. 外部リンクとアフィリエイト", "在庫リンクは店舗サイトに移動します。一部はアフィリエイトリンクの場合がありますが、購入価格は変わりません。"),
            ("5. 店舗アカウント", "店舗アカウントは運営者が発行します。ID・パスワードは店舗が管理し、共有しないでください。店舗画面のデータは店舗内部の参考用としてのみ使用してください。"),
            ("6. 禁止事項", "過度な自動アクセス、セキュリティの回避、他人のアカウントの使用など、サービスを妨げる行為や違法行為を禁止します。"),
            ("7. 権利", "商品名・写真は各店舗のものです。Leica は Leica Camera AG の商標で、Camera Bridge は Leica Camera AG とは関係ありません。"),
            ("8. 責任の制限", "運営者は故意または重大な過失がない限り、情報の誤りやサービスの停止による損害について責任を負いません。"),
            ("9. 規約の変更", "変更する場合は施行日とともにこのページでお知らせします。"),
            ("10. 準拠法", "本規約は大韓民国法に準拠します。"),
        ]
        return "利用規約", "".join(f"<h2>{h}</h2><p>{p}</p>" for h, p in items) + f'<p class="note">施行日：{UPDATED} · お問い合わせ {MAIL}</p>'
    items = [
        ("1. The service", "Camera Bridge is a free information service that lets you search used Leica listings and prices published by shops. No account is needed."),
        ("2. Accuracy", "Prices, stock, condition and estimated delivered totals (shipping, duties, taxes) are based on shop data and estimates, and may be delayed or wrong. Converted prices use reference exchange rates. Always check the original shop page before you buy."),
        ("3. Purchases", "Camera Bridge does not sell items or broker transactions. Purchase, payment, shipping, returns and warranty are between you and the shop, and we are not a party to them."),
        ("4. Links and affiliates", "Listing links take you to the shop's site. Some may be affiliate links; the price you pay does not change."),
        ("5. Shop accounts", "Shop accounts are issued by the operator. Shops keep their credentials private and use dealer-view data for internal reference only."),
        ("6. Prohibited use", "Do not disrupt the service (excessive automated requests, bypassing security, using another account) or use it unlawfully."),
        ("7. Rights", "Listing titles and photos belong to each shop. Leica is a trademark of Leica Camera AG; Camera Bridge is not affiliated with Leica Camera AG."),
        ("8. Liability", "Except for intent or gross negligence, we are not liable for losses caused by inaccurate information or interruptions. Mandatory consumer rights in your country are not affected. The service may change or stop without notice."),
        ("9. Changes", "We will post changes to these terms on this page with the effective date."),
        ("10. Governing law", "These terms are governed by the laws of the Republic of Korea, without prejudice to mandatory consumer protection laws of your country of residence."),
    ]
    return "Terms of use", "".join(f"<h2>{h}</h2><p>{p}</p>" for h, p in items) + f'<p class="note">Effective: {UPDATED} · Contact {MAIL}</p>'


def impressum_body() -> str:
    o = OPERATOR
    de = _rows([("Anbieter", f"{o['name']['en']} (브로콜리스튜디오), Inhaber: {o['rep']['en']} — Camera Bridge by {o['brand']}"),
                ("Anschrift", o["address"]["en"]),
                ("Kontakt", f"E-Mail: {MAIL} · Kontaktformular: „Feedback senden“ auf der Startseite"),
                ("Unternehmensregister", f"Koreanische Unternehmensnummer (사업자등록번호) {o['biz_no']}"),
                ("Umsatzsteuer-ID", "Nicht vorhanden (Unternehmen mit Sitz in der Republik Korea)"),
                ("Verantwortlich für den Inhalt (§ 18 Abs. 2 MStV)", f"{o['rep']['en']}, Anschrift wie oben")])
    en = _rows([("Provider", f"{o['name']['en']}, owner {o['rep']['en']}"), ("Address", o["address"]["en"]),
                ("Contact", f"Email {MAIL} · contact form: \"Send feedback\" on the home page"),
                ("Business registration (Korea)", o["biz_no"]), ("Responsible for content", o["rep"]["en"])])
    return ("<p>Angaben gemäß § 5 Digitale-Dienste-Gesetz (DDG)</p>" + de
            + "<h2>Verbraucherstreitbeilegung</h2><p>Wir sind nicht bereit und nicht verpflichtet, an Streitbeilegungsverfahren vor einer Verbraucherschlichtungsstelle teilzunehmen.</p>"
            + "<h2>Haftung für Links</h2><p>Camera Bridge verlinkt auf Angebote externer Händler. Für deren Inhalte, Preise und Angebote sind ausschließlich die jeweiligen Händler verantwortlich.</p>"
            + "<h2>Marken</h2><p>Leica ist eine Marke der Leica Camera AG. Camera Bridge ist ein unabhängiger Dienst und steht in keiner Verbindung zur Leica Camera AG.</p>"
            + '<p><a href="/en/privacy/">Datenschutzerklärung (English)</a></p>'
            + "<h2>Legal notice (English)</h2>" + en)


def page(lang: str, path: str, title: str, body: str, home: str) -> str:
    url = f"{SITE}{path}"
    f = FOOT[lang if lang in LANGS else "en"]
    base = lang if lang in LANGS else "en"
    tabs = [(f"/{base}/{name}/", f[name]) for name in ("about", "privacy", "terms")] + [("/impressum/", "Impressum")]
    body = re.sub(r"<h2>\d+\. ", "<h2>", body)  # 번호는 CSS가 붙임 (01, 02 …)
    current = ' aria-current="page"'
    nav = "".join(f'<a href="{href}"{current if href == path else ""}>{label}</a>' for href, label in tabs)
    return (f'<!DOCTYPE html><html lang="{lang}"><head><meta charset="UTF-8">'
            '<meta name="viewport" content="width=device-width, initial-scale=1.0">'
            f"<title>{html.escape(title)} | Camera Bridge</title><link rel=\"canonical\" href=\"{url}\">{FONTS}"
            f"<style>{CSS}{FOOTER_CSS}</style></head><body><main><header class=\"mast\"><a class=\"home\" href=\"/\">{home}</a>"
            f"<nav>{nav}</nav></header><h1>{html.escape(title)}</h1>{body}</main>"
            f"{footer(base)}</body></html>\n")


def build(out: Path) -> list[Path]:
    written = []
    for lang in LANGS:
        for name, make in (("about", about_body), ("privacy", privacy_body), ("terms", terms_body)):
            title, body = make(lang)
            path = out / lang / name / "index.html"
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(page(lang, f"/{lang}/{name}/", title, body, FOOT[lang]["home"]), encoding="utf-8")
            written.append(path)
    path = out / "impressum" / "index.html"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(page("de", "/impressum/", "Impressum", impressum_body(), "Camera Bridge"), encoding="utf-8")
    written.append(path)
    return written


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, default=ROOT)
    print(f"법적 고지 페이지 {len(build(parser.parse_args().out))}개")


if __name__ == "__main__":
    main()
