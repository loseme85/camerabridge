"""모델별 시세 페이지(검색 노출용 정적 HTML)와 sitemap.xml을 만든다.

입력: data/derived/entity_summary_v1.json (모델 요약), data/derived/results_search_index_v1.json (매물), data/fx_rates.json
출력: ko/leica/<모델>/index.html · en/… · ja/… (언어별 같은 내용), 언어별 목록 ko/leica/index.html …, sitemap.xml
자동 수집 워크플로에서 build_entity_index.py 다음에 실행한다.

  python3 scripts/build_model_pages.py            # 저장소 루트에 씀
  python3 scripts/build_model_pages.py --out DIR  # 다른 곳에 (시험용)
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import html
import json
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

from entity_catalog import krw_rates  # noqa: E402
from build_legal_pages import FOOTER_CSS, footer  # noqa: E402

SUMMARY = ROOT / "data" / "derived" / "entity_summary_v1.json"
INDEX = ROOT / "data" / "derived" / "results_search_index_v1.json"
SITE = "https://camerabridge.io"
LANGS = ("ko", "en", "ja", "de", "it", "es", "pt", "zh-Hans", "zh-Hant")  # 2026-11-08 사장님: 방문 늘리기 — 독일어·이탈리아어·스페인어·포르투갈어·중국어 2종 추가
PATH = {l: l.lower() for l in LANGS}  # 주소: /zh-hans/leica/…
MIN_ACTIVE = 3           # 판매 중 매물이 이만큼 있는 모델만 페이지로 (빈약한 페이지는 안 만듦)
MAX_PAGES = 400          # 매물 많은 순서로 최대 이만큼
LASTMOD = ROOT / "data" / "derived" / "model_pages_lastmod.json"  # 페이지별 내용 지문과 실제로 바뀐 날
LISTINGS_SHOWN = 30      # 페이지마다 보여 줄 판매 중 매물 (싼 순)
DISPLAY_CURRENCY = {"ko": "KRW", "en": "USD", "ja": "JPY", "de": "EUR", "it": "EUR", "es": "EUR", "pt": "EUR", "zh-Hans": "CNY", "zh-Hant": "HKD"}
# 잘못 연결됐을 가능성이 큰 매물은 페이지에서 뺀다: 대여 상품, 그 모델 B등급 기준가의 이 비율보다 싼 것
RENTAL = re.compile(r"\brental\b|\bfor rent\b|대여|렌탈|レンタル", re.I)
MIN_PRICE_RATIO = 0.35

# 판매처 이름 끝 '(나라)' → 나라 이름. 괄호가 없으면 한국 매장 (Leica Store Miami만 예외)
COUNTRY = {
    "한국": {"ko": "한국", "en": "Korea", "ja": "韓国"}, "일본": {"ko": "일본", "en": "Japan", "ja": "日本"},
    "미국": {"ko": "미국", "en": "USA", "ja": "米国"}, "영국": {"ko": "영국", "en": "UK", "ja": "英国"},
    "독일": {"ko": "독일", "en": "Germany", "ja": "ドイツ"}, "프랑스": {"ko": "프랑스", "en": "France", "ja": "フランス"},
    "이탈리아": {"ko": "이탈리아", "en": "Italy", "ja": "イタリア"}, "네덜란드": {"ko": "네덜란드", "en": "Netherlands", "ja": "オランダ"},
    "덴마크": {"ko": "덴마크", "en": "Denmark", "ja": "デンマーク"}, "스위스": {"ko": "스위스", "en": "Switzerland", "ja": "スイス"},
    "스페인": {"ko": "스페인", "en": "Spain", "ja": "スペイン"}, "포르투갈": {"ko": "포르투갈", "en": "Portugal", "ja": "ポルトガル"},
    "오스트리아": {"ko": "오스트리아", "en": "Austria", "ja": "オーストリア"}, "핀란드": {"ko": "핀란드", "en": "Finland", "ja": "フィンランド"},
    "룩셈부르크": {"ko": "룩셈부르크", "en": "Luxembourg", "ja": "ルクセンブルク"}, "홍콩": {"ko": "홍콩", "en": "Hong Kong", "ja": "香港"},
    "싱가포르": {"ko": "싱가포르", "en": "Singapore", "ja": "シンガポール"}, "말레이시아": {"ko": "말레이시아", "en": "Malaysia", "ja": "マレーシア"},
    "아랍에미리트": {"ko": "아랍에미리트", "en": "UAE", "ja": "アラブ首長国連邦"}, "호주": {"ko": "호주", "en": "Australia", "ja": "オーストラリア"},
    "캐나다": {"ko": "캐나다", "en": "Canada", "ja": "カナダ"},
    "폴란드": {"ko": "폴란드", "en": "Poland", "ja": "ポーランド"},
    "뉴질랜드": {"ko": "뉴질랜드", "en": "New Zealand", "ja": "ニュージーランド"},
    "칠레": {"ko": "칠레", "en": "Chile", "ja": "チリ"},
    "그리스": {"ko": "그리스", "en": "Greece", "ja": "ギリシャ"},
    "노르웨이": {"ko": "노르웨이", "en": "Norway", "ja": "ノルウェー"},
    "벨기에": {"ko": "벨기에", "en": "Belgium", "ja": "ベルギー"},
    "스웨덴": {"ko": "스웨덴", "en": "Sweden", "ja": "スウェーデン"},
    "체코": {"ko": "체코", "en": "Czechia", "ja": "チェコ"},
    "헝가리": {"ko": "헝가리", "en": "Hungary", "ja": "ハンガリー"},
}
SOURCE_COUNTRY = {"Leica Store Miami": "미국"}
# 새 6개 언어 나라 이름 (de, it, es, pt, zh-Hans, zh-Hant 순서)
COUNTRY_NEW_LANGS = {'한국': ('Korea', 'Corea del Sud', 'Corea del Sur', 'Coreia do Sul', '韩国', '韓國'), '일본': ('Japan', 'Giappone', 'Japón', 'Japão', '日本', '日本'), '미국': ('USA', 'Stati Uniti', 'EE. UU.', 'EUA', '美国', '美國'), '영국': ('Vereinigtes Königreich', 'Regno Unito', 'Reino Unido', 'Reino Unido', '英国', '英國'), '독일': ('Deutschland', 'Germania', 'Alemania', 'Alemanha', '德国', '德國'), '프랑스': ('Frankreich', 'Francia', 'Francia', 'França', '法国', '法國'), '이탈리아': ('Italien', 'Italia', 'Italia', 'Itália', '意大利', '義大利'), '네덜란드': ('Niederlande', 'Paesi Bassi', 'Países Bajos', 'Países Baixos', '荷兰', '荷蘭'), '덴마크': ('Dänemark', 'Danimarca', 'Dinamarca', 'Dinamarca', '丹麦', '丹麥'), '스위스': ('Schweiz', 'Svizzera', 'Suiza', 'Suíça', '瑞士', '瑞士'), '스페인': ('Spanien', 'Spagna', 'España', 'Espanha', '西班牙', '西班牙'), '포르투갈': ('Portugal', 'Portogallo', 'Portugal', 'Portugal', '葡萄牙', '葡萄牙'), '오스트리아': ('Österreich', 'Austria', 'Austria', 'Áustria', '奥地利', '奧地利'), '핀란드': ('Finnland', 'Finlandia', 'Finlandia', 'Finlândia', '芬兰', '芬蘭'), '룩셈부르크': ('Luxemburg', 'Lussemburgo', 'Luxemburgo', 'Luxemburgo', '卢森堡', '盧森堡'), '홍콩': ('Hongkong', 'Hong Kong', 'Hong Kong', 'Hong Kong', '香港', '香港'), '싱가포르': ('Singapur', 'Singapore', 'Singapur', 'Singapura', '新加坡', '新加坡'), '말레이시아': ('Malaysia', 'Malesia', 'Malasia', 'Malásia', '马来西亚', '馬來西亞'), '아랍에미리트': ('VAE', 'Emirati Arabi Uniti', 'EAU', 'EAU', '阿联酋', '阿聯酋'), '호주': ('Australien', 'Australia', 'Australia', 'Austrália', '澳大利亚', '澳洲'), '캐나다': ('Kanada', 'Canada', 'Canadá', 'Canadá', '加拿大', '加拿大'), '폴란드': ('Polen', 'Polonia', 'Polonia', 'Polônia', '波兰', '波蘭'), '뉴질랜드': ('Neuseeland', 'Nuova Zelanda', 'Nueva Zelanda', 'Nova Zelândia', '新西兰', '紐西蘭'), '칠레': ('Chile', 'Cile', 'Chile', 'Chile', '智利', '智利'), '그리스': ('Griechenland', 'Grecia', 'Grecia', 'Grécia', '希腊', '希臘'), '노르웨이': ('Norwegen', 'Norvegia', 'Noruega', 'Noruega', '挪威', '挪威'), '벨기에': ('Belgien', 'Belgio', 'Bélgica', 'Bélgica', '比利时', '比利時'), '스웨덴': ('Schweden', 'Svezia', 'Suecia', 'Suécia', '瑞典', '瑞典'), '체코': ('Tschechien', 'Repubblica Ceca', 'Chequia', 'Chéquia', '捷克', '捷克'), '헝가리': ('Ungarn', 'Ungheria', 'Hungría', 'Hungria', '匈牙利', '匈牙利')}
for _ko, _names in COUNTRY_NEW_LANGS.items():
    COUNTRY.setdefault(_ko, {}).update(dict(zip(("de", "it", "es", "pt", "zh-Hans", "zh-Hant"), _names)))

T = {
    "ko": {
        "title": "{name} 중고 시세·매물 | 카메라브릿지",
        "q_price": "{name} 중고 가격은 얼마인가요?",
        "a_price": "지금 {countries}개 나라 {shops}개 매장에 {n}개가 올라와 있습니다. 판매 가격은 {low}부터 {high}까지, 중간값은 {median}입니다.",
        "a_sold": " 최근 팔린 매물 {k}개의 판매완료 직전 표시 가격 중간값은 {sold}입니다.",
        "q_where": "{name} 중고는 어느 나라가 가장 싼가요?",
        "a_where": "지금 나라별 최저가: {list}. 오늘 환율로 환산한 매장 표시 가격이며, 배송비·관세는 빠져 있습니다.",
        "related": "비슷한 모델", "sep": ", ",
        "new": "새 제품 정가 (라이카 영국)", "vs_new": "중고 B등급 / 정가", "vs_new_val": "정가의 {pct}%",
        "a_new": " 새 제품은 라이카 영국 공식 가격 {new}이고, 중고 B등급 시세는 그 {pct}% 수준입니다.",
        "desc": "{name} 중고 판매 중 {active}개 ({shops}개 매장), {range}. 한국·일본·유럽·미국 라이카 매장 매물과 판매완료 가격을 한곳에서.",
        "h1": "{name} 중고 시세", "active": "판매 중", "active_val": "{n}개 · {shops}개 매장",
        "range": "판매 중 가격", "sold": "팔린 매물 중간값", "sold_val": "{price} (팔린 매물 {n}개)",
        "sold_note": "판매완료로 바뀌기 직전에 본 표시 가격의 중간값입니다. 실제 거래 가격과 다를 수 있습니다.",
        "updated": "{time} 기준 · 가격은 매장 표시 가격을 오늘 환율로 원화 환산", "listings": "판매 중 매물 (싼 순)",
        "col_item": "매물", "col_shop": "매장", "col_cond": "상태", "col_price": "가격",
        "more": "카메라브릿지에서 {name} 전체 검색", "children": "세대·버전별", "parent": "전체 보기",
        "none": "지금 판매 중인 매물이 없습니다.", "index_title": "라이카 중고 시세 · 모델별 | 카메라브릿지",
        "index_h1": "라이카 모델별 중고 시세", "index_desc": "라이카 카메라·렌즈 모델별 중고 시세와 판매 중 매물.",
        "shops_h": "판매처별 가격", "col_count": "매물", "col_low": "최저가", "col_cur": "통화", "info_h": "모델 정보", "kind": "종류", "kind_Body": "카메라 바디", "kind_Lens": "렌즈", "mount": "마운트", "codes": "제품 코드", "bodies": "카메라 바디", "lenses": "렌즈", "aka": "다른 이름", "count": "{n}개", "home": "카메라브릿지", "list": "모델별 시세", "approx": "약 ",
    },
    "en": {
        "title": "{name} Used Price & Listings | Camera Bridge",
        "q_price": "How much is a used {name}?",
        "a_price": "Right now {n} are listed at {shops} shops in {countries} countries. Asking prices run from {low} to {high}, with a median of {median}.",
        "a_sold": " The last {k} that sold had a median final asking price of {sold}.",
        "q_where": "Where is a used {name} cheapest?",
        "a_where": "Cheapest by country right now: {list}. Shop prices converted at today's rate; shipping and import tax not included.",
        "related": "Similar models", "sep": ", ",
        "new": "New price (Leica UK)", "vs_new": "Used grade B vs new", "vs_new_val": "{pct}% of new",
        "a_new": " New, it costs {new} at Leica UK; a grade B used one runs about {pct}% of that.",
        "desc": "{active} used {name} listings from {shops} shops, {range}. Leica shops in Korea, Japan, Europe and the US, with sold prices, in one place.",
        "h1": "{name} used prices", "active": "For sale now", "active_val": "{n} listings · {shops} shops",
        "range": "Asking prices", "sold": "Sold median", "sold_val": "{price} ({n} sold listings)",
        "sold_note": "Median of the last asking price seen before a listing was marked sold. Actual sale prices may differ.",
        "updated": "As of {time} · shop prices converted to USD at today's rate", "listings": "For sale now (cheapest first)",
        "col_item": "Listing", "col_shop": "Shop", "col_cond": "Condition", "col_price": "Price",
        "more": "Search all {name} on Camera Bridge", "children": "By generation / version", "parent": "See all",
        "none": "No listings for sale right now.", "index_title": "Leica Used Prices by Model | Camera Bridge",
        "index_h1": "Leica used prices by model", "index_desc": "Used prices and live listings for Leica cameras and lenses, by model.",
        "shops_h": "Prices by shop", "col_count": "Listings", "col_low": "Lowest", "col_cur": "Currency", "info_h": "Model info", "kind": "Type", "kind_Body": "Camera body", "kind_Lens": "Lens", "mount": "Mount", "codes": "Product codes", "bodies": "Camera bodies", "lenses": "Lenses", "aka": "Also known as", "count": "{n}", "home": "Camera Bridge", "list": "Prices by model", "approx": "≈ ",
    },
    "ja": {
        "title": "{name} 中古相場・在庫 | Camera Bridge",
        "q_price": "{name} の中古価格はいくら？",
        "a_price": "現在 {countries} か国 {shops} 店に {n} 点が出品されています。販売価格は {low} から {high}、中央値は {median} です。",
        "a_sold": " 最近販売済みになった {k} 点の、販売済み直前の表示価格の中央値は {sold} でした。",
        "q_where": "{name} の中古はどの国が安い？",
        "a_where": "現在の国別最安値：{list}。各店の表示価格を本日のレートで換算したもので、送料・関税は含みません。",
        "related": "似ているモデル", "sep": "、",
        "new": "新品価格（ライカ英国）", "vs_new": "中古B等級 / 新品", "vs_new_val": "新品の {pct}%",
        "a_new": " 新品はライカ英国の公式価格で {new}、中古B等級の相場はその約 {pct}% です。",
        "desc": "{name} の中古在庫 {active} 点（{shops} 店）、{range}。韓国・日本・欧州・米国のライカ取扱店の在庫と販売済み価格をまとめて。",
        "h1": "{name} 中古相場", "active": "販売中", "active_val": "{n} 点 · {shops} 店",
        "range": "販売価格", "sold": "販売済み中央値", "sold_val": "{price}（販売済み {n} 点）",
        "sold_note": "販売済みになる直前に確認した表示価格の中央値です。実際の取引価格とは異なる場合があります。",
        "updated": "{time} 時点 · 各店の表示価格を本日のレートで円換算", "listings": "販売中の在庫（安い順）",
        "col_item": "商品", "col_shop": "店舗", "col_cond": "状態", "col_price": "価格",
        "more": "Camera Bridge で {name} をすべて検索", "children": "世代・バージョン別", "parent": "すべて見る",
        "none": "現在販売中の在庫はありません。", "index_title": "ライカ中古相場 · モデル別 | Camera Bridge",
        "index_h1": "ライカ モデル別中古相場", "index_desc": "ライカのカメラ・レンズのモデル別中古相場と販売中の在庫。",
        "shops_h": "店舗別価格", "col_count": "在庫", "col_low": "最安値", "col_cur": "通貨", "info_h": "モデル情報", "kind": "種類", "kind_Body": "カメラボディ", "kind_Lens": "レンズ", "mount": "マウント", "codes": "製品コード", "bodies": "カメラボディ", "lenses": "レンズ", "aka": "別名", "count": "{n} 点", "home": "Camera Bridge", "list": "モデル別相場", "approx": "約",
    },
}

# 새 6개 언어 (2026-11-08)
T.update({'de': {'title': '{name} gebraucht: Preise & Angebote | Camera Bridge', 'q_price': 'Was kostet eine gebrauchte {name}?', 'a_price': 'Aktuell sind {n} Stück bei {shops} Händlern in {countries} Ländern gelistet. Die Angebotspreise reichen von {low} bis {high}, der Median liegt bei {median}.', 'a_sold': ' Die letzten {k} verkauften Exemplare hatten einen mittleren letzten Angebotspreis von {sold}.', 'q_where': 'Wo ist eine gebrauchte {name} am günstigsten?', 'a_where': 'Günstigste Länder aktuell: {list}. Händlerpreise zum heutigen Kurs umgerechnet, ohne Versand und Einfuhrabgaben.', 'related': 'Ähnliche Modelle', 'sep': ', ', 'new': 'Neupreis (Leica UK)', 'vs_new': 'Gebraucht Zustand B / neu', 'vs_new_val': '{pct}% vom Neupreis', 'a_new': ' Neu kostet sie {new} bei Leica UK; gebraucht in Zustand B etwa {pct}% davon.', 'desc': '{active} gebrauchte {name} von {shops} Händlern, {range}. Leica-Händler in Korea, Japan, Europa und den USA mit Verkaufspreisen an einem Ort.', 'h1': '{name} gebraucht: Preise', 'active': 'Jetzt im Angebot', 'active_val': '{n} Angebote · {shops} Händler', 'range': 'Angebotspreise', 'sold': 'Median verkauft', 'sold_val': '{price} ({n} verkauft)', 'sold_note': 'Median des letzten Angebotspreises, bevor ein Angebot als verkauft markiert wurde. Tatsächliche Verkaufspreise können abweichen.', 'updated': 'Stand {time} · Händlerpreise zum heutigen Kurs in EUR umgerechnet', 'listings': 'Jetzt im Angebot (günstigste zuerst)', 'col_item': 'Angebot', 'col_shop': 'Händler', 'col_cond': 'Zustand', 'col_price': 'Preis', 'more': 'Alle {name} auf Camera Bridge suchen', 'children': 'Nach Generation / Version', 'parent': 'Alle ansehen', 'none': 'Derzeit keine Angebote.', 'index_title': 'Leica Gebrauchtpreise nach Modell | Camera Bridge', 'index_h1': 'Leica Gebrauchtpreise nach Modell', 'index_desc': 'Gebrauchtpreise und aktuelle Angebote für Leica Kameras und Objektive, nach Modell.', 'shops_h': 'Preise nach Händler', 'col_count': 'Angebote', 'col_low': 'Günstigster', 'col_cur': 'Währung', 'info_h': 'Modellinfo', 'kind': 'Art', 'kind_Body': 'Kameragehäuse', 'kind_Lens': 'Objektiv', 'mount': 'Bajonett', 'codes': 'Bestellnummern', 'bodies': 'Kameragehäuse', 'lenses': 'Objektive', 'aka': 'Auch bekannt als', 'count': '{n}', 'home': 'Camera Bridge', 'list': 'Preise nach Modell', 'approx': '≈ ', 'lead': 'Gebrauchte {name}: Marktwert Zustand B {b}, {n} im Angebot bei {shops} Händlern (Stand {date}).'}, 'it': {'title': '{name} usata: prezzi e annunci | Camera Bridge', 'q_price': 'Quanto costa una {name} usata?', 'a_price': 'Al momento ce ne sono {n} in vendita in {shops} negozi di {countries} paesi. I prezzi vanno da {low} a {high}, con una mediana di {median}.', 'a_sold': ' Gli ultimi {k} venduti avevano un ultimo prezzo richiesto mediano di {sold}.', 'q_where': 'Dove costa meno una {name} usata?', 'a_where': 'Paesi più economici ora: {list}. Prezzi dei negozi convertiti al cambio di oggi, spedizione e dazi esclusi.', 'related': 'Modelli simili', 'sep': ', ', 'new': 'Prezzo nuovo (Leica UK)', 'vs_new': 'Usato grado B / nuovo', 'vs_new_val': '{pct}% del nuovo', 'a_new': ' Nuova costa {new} da Leica UK; usata in grado B circa il {pct}%.', 'desc': '{active} {name} usate da {shops} negozi, {range}. Negozi Leica in Corea, Giappone, Europa e USA, con prezzi di vendita, in un solo posto.', 'h1': '{name} usata: prezzi', 'active': 'In vendita ora', 'active_val': '{n} annunci · {shops} negozi', 'range': 'Prezzi richiesti', 'sold': 'Mediana venduti', 'sold_val': '{price} ({n} venduti)', 'sold_note': "Mediana dell'ultimo prezzo visto prima che l'annuncio fosse segnato come venduto. I prezzi reali possono differire.", 'updated': 'Aggiornato {time} · prezzi convertiti in EUR al cambio di oggi', 'listings': 'In vendita ora (dal più economico)', 'col_item': 'Annuncio', 'col_shop': 'Negozio', 'col_cond': 'Condizione', 'col_price': 'Prezzo', 'more': 'Cerca tutte le {name} su Camera Bridge', 'children': 'Per generazione / versione', 'parent': 'Vedi tutto', 'none': 'Nessun annuncio al momento.', 'index_title': 'Prezzi Leica usate per modello | Camera Bridge', 'index_h1': 'Prezzi Leica usate per modello', 'index_desc': "Prezzi dell'usato e annunci attuali di fotocamere e obiettivi Leica, per modello.", 'shops_h': 'Prezzi per negozio', 'col_count': 'Annunci', 'col_low': 'Minimo', 'col_cur': 'Valuta', 'info_h': 'Scheda modello', 'kind': 'Tipo', 'kind_Body': 'Corpo macchina', 'kind_Lens': 'Obiettivo', 'mount': 'Innesto', 'codes': 'Codici prodotto', 'bodies': 'Corpi macchina', 'lenses': 'Obiettivi', 'aka': 'Conosciuta anche come', 'count': '{n}', 'home': 'Camera Bridge', 'list': 'Prezzi per modello', 'approx': '≈ ', 'lead': '{name} usata: valore di mercato grado B {b}, {n} in vendita in {shops} negozi (al {date}).'}, 'es': {'title': '{name} usada: precios y anuncios | Camera Bridge', 'q_price': '¿Cuánto cuesta una {name} usada?', 'a_price': 'Ahora hay {n} a la venta en {shops} tiendas de {countries} países. Los precios van de {low} a {high}, con una mediana de {median}.', 'a_sold': ' Las últimas {k} vendidas tuvieron un último precio pedido mediano de {sold}.', 'q_where': '¿Dónde es más barata una {name} usada?', 'a_where': 'Países más baratos ahora: {list}. Precios de tienda convertidos al cambio de hoy, sin envío ni impuestos de importación.', 'related': 'Modelos similares', 'sep': ', ', 'new': 'Precio nueva (Leica UK)', 'vs_new': 'Usada grado B / nueva', 'vs_new_val': '{pct}% de la nueva', 'a_new': ' Nueva cuesta {new} en Leica UK; usada en grado B, cerca del {pct}%.', 'desc': '{active} {name} usadas de {shops} tiendas, {range}. Tiendas Leica de Corea, Japón, Europa y EE. UU., con precios de venta, en un solo lugar.', 'h1': '{name} usada: precios', 'active': 'A la venta ahora', 'active_val': '{n} anuncios · {shops} tiendas', 'range': 'Precios pedidos', 'sold': 'Mediana vendidas', 'sold_val': '{price} ({n} vendidas)', 'sold_note': 'Mediana del último precio visto antes de que el anuncio se marcara como vendido. El precio real puede variar.', 'updated': 'A {time} · precios convertidos a EUR al cambio de hoy', 'listings': 'A la venta ahora (más baratas primero)', 'col_item': 'Anuncio', 'col_shop': 'Tienda', 'col_cond': 'Estado', 'col_price': 'Precio', 'more': 'Buscar todas las {name} en Camera Bridge', 'children': 'Por generación / versión', 'parent': 'Ver todo', 'none': 'No hay anuncios ahora.', 'index_title': 'Precios de Leica usadas por modelo | Camera Bridge', 'index_h1': 'Precios de Leica usadas por modelo', 'index_desc': 'Precios de segunda mano y anuncios actuales de cámaras y objetivos Leica, por modelo.', 'shops_h': 'Precios por tienda', 'col_count': 'Anuncios', 'col_low': 'Más barato', 'col_cur': 'Moneda', 'info_h': 'Ficha del modelo', 'kind': 'Tipo', 'kind_Body': 'Cuerpo de cámara', 'kind_Lens': 'Objetivo', 'mount': 'Montura', 'codes': 'Códigos de producto', 'bodies': 'Cuerpos de cámara', 'lenses': 'Objetivos', 'aka': 'También conocida como', 'count': '{n}', 'home': 'Camera Bridge', 'list': 'Precios por modelo', 'approx': '≈ ', 'lead': '{name} usada: valor de mercado grado B {b}, {n} a la venta en {shops} tiendas (a {date}).'}, 'pt': {'title': '{name} usada: preços e anúncios | Camera Bridge', 'q_price': 'Quanto custa uma {name} usada?', 'a_price': 'Agora há {n} à venda em {shops} lojas de {countries} países. Os preços vão de {low} a {high}, com mediana de {median}.', 'a_sold': ' As últimas {k} vendidas tiveram um último preço pedido mediano de {sold}.', 'q_where': 'Onde uma {name} usada é mais barata?', 'a_where': 'Países mais baratos agora: {list}. Preços das lojas convertidos ao câmbio de hoje, sem frete nem impostos de importação.', 'related': 'Modelos semelhantes', 'sep': ', ', 'new': 'Preço nova (Leica UK)', 'vs_new': 'Usada grau B / nova', 'vs_new_val': '{pct}% da nova', 'a_new': ' Nova custa {new} na Leica UK; usada em grau B, cerca de {pct}%.', 'desc': '{active} {name} usadas de {shops} lojas, {range}. Lojas Leica na Coreia, Japão, Europa e EUA, com preços de venda, num só lugar.', 'h1': '{name} usada: preços', 'active': 'À venda agora', 'active_val': '{n} anúncios · {shops} lojas', 'range': 'Preços pedidos', 'sold': 'Mediana vendidas', 'sold_val': '{price} ({n} vendidas)', 'sold_note': 'Mediana do último preço visto antes de o anúncio ser marcado como vendido. O preço real pode variar.', 'updated': 'Em {time} · preços convertidos em EUR ao câmbio de hoje', 'listings': 'À venda agora (mais baratas primeiro)', 'col_item': 'Anúncio', 'col_shop': 'Loja', 'col_cond': 'Estado', 'col_price': 'Preço', 'more': 'Procurar todas as {name} na Camera Bridge', 'children': 'Por geração / versão', 'parent': 'Ver tudo', 'none': 'Nenhum anúncio agora.', 'index_title': 'Preços de Leica usadas por modelo | Camera Bridge', 'index_h1': 'Preços de Leica usadas por modelo', 'index_desc': 'Preços de usados e anúncios atuais de câmeras e objetivas Leica, por modelo.', 'shops_h': 'Preços por loja', 'col_count': 'Anúncios', 'col_low': 'Mais barato', 'col_cur': 'Moeda', 'info_h': 'Ficha do modelo', 'kind': 'Tipo', 'kind_Body': 'Corpo de câmera', 'kind_Lens': 'Objetiva', 'mount': 'Encaixe', 'codes': 'Códigos do produto', 'bodies': 'Corpos de câmera', 'lenses': 'Objetivas', 'aka': 'Também conhecida como', 'count': '{n}', 'home': 'Camera Bridge', 'list': 'Preços por modelo', 'approx': '≈ ', 'lead': '{name} usada: valor de mercado grau B {b}, {n} à venda em {shops} lojas (em {date}).'}, 'zh-Hans': {'title': '{name} 二手价格与在售 | Camera Bridge', 'q_price': '二手 {name} 多少钱？', 'a_price': '目前 {countries} 个国家的 {shops} 家店铺共有 {n} 件在售，售价从 {low} 到 {high}，中位数为 {median}。', 'a_sold': ' 最近售出的 {k} 件，售出前最后标价的中位数为 {sold}。', 'q_where': '二手 {name} 哪个国家最便宜？', 'a_where': '目前各国最低价：{list}。按今日汇率换算的店铺标价，不含运费和进口税。', 'related': '相似型号', 'sep': '、', 'new': '新品价格（徕卡英国）', 'vs_new': '二手 B 级 / 新品', 'vs_new_val': '新品的 {pct}%', 'a_new': ' 新品在徕卡英国官方售价 {new}，二手 B 级约为其 {pct}%。', 'desc': '二手 {name} 在售 {active} 件（{shops} 家店铺），{range}。汇集韩国、日本、欧洲、美国徕卡店铺的在售与成交价格。', 'h1': '{name} 二手行情', 'active': '在售', 'active_val': '{n} 件 · {shops} 家店铺', 'range': '在售价格', 'sold': '成交中位数', 'sold_val': '{price}（已售 {n} 件）', 'sold_note': '这是标记为已售前最后看到的标价中位数，可能与实际成交价不同。', 'updated': '{time} · 店铺标价按今日汇率换算为人民币', 'listings': '在售商品（价格从低到高）', 'col_item': '商品', 'col_shop': '店铺', 'col_cond': '成色', 'col_price': '价格', 'more': '在 Camera Bridge 搜索全部 {name}', 'children': '按代数 / 版本', 'parent': '查看全部', 'none': '目前没有在售商品。', 'index_title': '徕卡二手行情 · 按型号 | Camera Bridge', 'index_h1': '徕卡二手行情（按型号）', 'index_desc': '徕卡相机和镜头的二手行情与在售商品，按型号查看。', 'shops_h': '各店铺价格', 'col_count': '在售', 'col_low': '最低价', 'col_cur': '货币', 'info_h': '型号信息', 'kind': '类别', 'kind_Body': '相机机身', 'kind_Lens': '镜头', 'mount': '卡口', 'codes': '产品编号', 'bodies': '相机机身', 'lenses': '镜头', 'aka': '别名', 'count': '{n} 件', 'home': 'Camera Bridge', 'list': '按型号行情', 'approx': '约', 'lead': '二手 {name}：B 级市场价 {b}，{shops} 家店铺在售 {n} 件（{date}）。'}, 'zh-Hant': {'title': '{name} 二手價格與在售 | Camera Bridge', 'q_price': '二手 {name} 多少錢？', 'a_price': '目前 {countries} 個國家的 {shops} 家店鋪共有 {n} 件在售，售價從 {low} 到 {high}，中位數為 {median}。', 'a_sold': ' 最近售出的 {k} 件，售出前最後標價的中位數為 {sold}。', 'q_where': '二手 {name} 哪個國家最便宜？', 'a_where': '目前各國最低價：{list}。按今日匯率換算的店鋪標價，不含運費和進口稅。', 'related': '相似型號', 'sep': '、', 'new': '新品價格（徠卡英國）', 'vs_new': '二手 B 級 / 新品', 'vs_new_val': '新品的 {pct}%', 'a_new': ' 新品在徠卡英國官方售價 {new}，二手 B 級約為其 {pct}%。', 'desc': '二手 {name} 在售 {active} 件（{shops} 家店鋪），{range}。匯集韓國、日本、歐洲、美國徠卡店鋪的在售與成交價格。', 'h1': '{name} 二手行情', 'active': '在售', 'active_val': '{n} 件 · {shops} 家店鋪', 'range': '在售價格', 'sold': '成交中位數', 'sold_val': '{price}（已售 {n} 件）', 'sold_note': '這是標記為已售前最後看到的標價中位數，可能與實際成交價不同。', 'updated': '{time} · 店鋪標價按今日匯率換算為港幣', 'listings': '在售商品（價格由低到高）', 'col_item': '商品', 'col_shop': '店鋪', 'col_cond': '成色', 'col_price': '價格', 'more': '在 Camera Bridge 搜尋全部 {name}', 'children': '按代數 / 版本', 'parent': '查看全部', 'none': '目前沒有在售商品。', 'index_title': '徠卡二手行情 · 按型號 | Camera Bridge', 'index_h1': '徠卡二手行情（按型號）', 'index_desc': '徠卡相機和鏡頭的二手行情與在售商品，按型號查看。', 'shops_h': '各店鋪價格', 'col_count': '在售', 'col_low': '最低價', 'col_cur': '貨幣', 'info_h': '型號資訊', 'kind': '類別', 'kind_Body': '相機機身', 'kind_Lens': '鏡頭', 'mount': '卡口', 'codes': '產品編號', 'bodies': '相機機身', 'lenses': '鏡頭', 'aka': '別名', 'count': '{n} 件', 'home': 'Camera Bridge', 'list': '按型號行情', 'approx': '約', 'lead': '二手 {name}：B 級市場價 {b}，{shops} 家店鋪在售 {n} 件（{date}）。'}})
# 첫 줄 한 줄 답 (AI 검색·검색엔진이 인용하기 쉬운 숫자 문장)
for _l, _v in {'ko': '{name} 중고: B등급 시세 {b}, {shops}개 매장에 {n}개 판매 중 ({date} 기준).', 'en': 'Used {name}: grade B market value {b}, {n} for sale at {shops} shops (as of {date}).', 'ja': '中古 {name}：B等級の相場 {b}、{shops} 店で {n} 点販売中（{date} 時点）。'}.items():
    T[_l]["lead"] = _v

CSS = """
:root{--bg:#FEFEFD;--text:#22201E;--soft:#6E6A64;--muted:#8a9094;--border:#e1e4e3;--accent:#1f4a3a;--row:#f5f6f5}
@media (prefers-color-scheme:dark){:root{--bg:#141617;--text:#e8eaea;--soft:#a9afb2;--muted:#7d8488;--border:#2c3133;--accent:#8cc5ad;--row:#1b1e1f}}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--text);font:15px/1.6 "Jost","Pretendard Variable",Pretendard,system-ui,-apple-system,"Segoe UI",sans-serif;font-variant-numeric:tabular-nums}
main{max-width:960px;margin:0 auto;padding:24px 16px 64px}
nav{font-size:13px;color:var(--muted);margin-bottom:20px}
nav a{color:var(--soft)}
h1{font:500 34px/1.2 "EB Garamond","Pretendard Variable",Pretendard,Georgia,serif;margin:0 0 6px;letter-spacing:-.005em}
h2{font-family:"EB Garamond","Pretendard Variable",Pretendard,Georgia,serif;font-weight:500}
.ko-name{color:var(--soft);margin:0 0 20px}
.lead{font-size:16px;margin:0 0 18px}
dl{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:0;margin:0 0 8px;border-top:1px solid var(--border)}
dl div{padding:12px 0;border-bottom:1px solid var(--border)}
dt{font-size:13px;color:var(--muted)}
dd{margin:2px 0 0;font-size:18px;font-weight:600}
dd.small{font-size:14px;font-weight:400}
.note{font-size:13px;color:var(--muted);margin:8px 0 28px}
h2{font-size:17px;margin:32px 0 10px}
.table{overflow-x:auto}
table{width:100%;border-collapse:collapse;font-size:14px}
th{text-align:left;font-weight:500;color:var(--muted);border-bottom:1px solid var(--border);padding:8px 8px 8px 0}
td{border-bottom:1px solid var(--border);padding:8px 8px 8px 0;vertical-align:top}
td.price,th.price{text-align:right;white-space:nowrap;padding-right:0}
td .orig{display:block;font-size:12px;color:var(--muted)}
a{color:var(--accent)}
.more{display:inline-block;margin-top:20px;padding:10px 14px;border:1px solid var(--accent);text-decoration:none}
ul.links{padding-left:18px}
ul.links li{margin:4px 0}
ul.links span{color:var(--muted);font-size:13px}
"""

SYMBOL = {"KRW": "₩", "USD": "$", "JPY": "¥", "EUR": "€", "CNY": "CN¥", "TWD": "NT$", "GBP": "£", "HKD": "HK$", "CHF": "CHF ", "DKK": "DKK ",
          "AUD": "A$", "SGD": "S$", "CAD": "C$", "MYR": "RM ", "PLN": "zł ", "NZD": "NZ$", "CLP": "CLP ", "SEK": "SEK ", "CZK": "Kč ", "HUF": "Ft "}


def money(amount: float, currency: str, lang: str, approx: bool = False) -> str:
    """approx=True: 환산 가격이라 원 1,000·엔 100·달러 1 단위로 반올림"""
    if approx:
        amount = round(amount, -3 if currency == "KRW" else -2 if currency == "JPY" else 0)
    if currency == "KRW" and lang == "ko":
        return f"{round(amount):,}원"
    digits = 0 if currency in ("KRW", "JPY") else 0 if amount >= 1000 else 2
    return f"{SYMBOL.get(currency, currency + ' ')}{amount:,.{digits}f}"


def slug_of(entity_id: str) -> str:
    return entity_id.split(":", 2)[2].replace(":", "-").replace(".", "")


def display_name(entity: dict, lang: str) -> str:
    if lang == "ko" and entity.get("name_ko"):
        return entity["name_ko"].replace(" (전체)", "")
    return entity["name"].replace(" (all)", "")


def condition_text(raw: str) -> str:
    """'Harrison: Good' → 'Good', '정보없음' → '—'. 매장 자체 표기를 그대로 보여 준다."""
    text = re.sub(r"^[^:]{2,30}:\s*", "", raw or "").strip()
    if not text or text in ("정보없음", "Unknown"):
        return "—"
    return text if len(text) <= 32 else text[:31] + "…"


def shop_parts(source: str) -> tuple[str, str]:
    """'Calumet (독일)' → ('Calumet', '독일')"""
    if source.endswith(")") and " (" in source:
        name, country = source[:-1].rsplit(" (", 1)
        if country in COUNTRY:
            return name, country
    return source, SOURCE_COUNTRY.get(source, "한국")


def pick_entities(entities: list[dict]) -> list[dict]:
    """판매 중 MIN_ACTIVE개 이상인 모델을 매물 많은 순으로 최대 MAX_PAGES개. '세대 미표기' 묶음, 부모와 사실상 같은 '기본형'은 뺀다
    (M6 → M6 Classic·M6 TTL처럼 세대·버전은 각자 페이지, 부모 페이지는 '세대·버전별'로 이어 줌)."""
    by_id = {e["id"]: e for e in entities}
    pool = []
    for e in entities:
        if e.get("feature") or e["kind"] not in ("Body", "Lens") or (e.get("active_count") or 0) < MIN_ACTIVE:
            continue
        if "unspecified" in e["id"]:
            continue
        parent = by_id.get(e.get("parent") or "")
        if e["id"].endswith(":standard") and parent and parent["listing_count"] <= e["listing_count"] * 1.5:
            continue
        pool.append(e)
    pool.sort(key=lambda e: (-e["listing_count"], e["id"]))
    return pool[:MAX_PAGES]


def footer_for(lang: str) -> str:
    """법적 고지 페이지는 한·영·일만 있어 새 언어는 영어 바닥글, '모델별 시세' 링크만 그 언어로"""
    if lang in ("ko", "en", "ja"):
        return footer(lang)
    return footer("en").replace('href="/en/leica/"', f'href="/{PATH[lang]}/leica/"', 1)


def page_url(lang: str, slug: str | None = None) -> str:
    return f"{SITE}/{PATH[lang]}/leica/{slug}/" if slug else f"{SITE}/{PATH[lang]}/leica/"


def head(lang: str, title: str, desc: str, url_for, json_ld: dict | None) -> str:
    alternates = "".join(f'<link rel="alternate" hreflang="{l}" href="{url_for(l)}">' for l in LANGS)
    alternates += f'<link rel="alternate" hreflang="x-default" href="{url_for("en")}">'
    blocks = json_ld if isinstance(json_ld, list) else [json_ld] if json_ld else []
    ld = "".join(f'<script type="application/ld+json">{json.dumps(b, ensure_ascii=False)}</script>' for b in blocks)
    return (f'<!DOCTYPE html><html lang="{lang}"><head><meta charset="UTF-8">'
            f'<meta name="viewport" content="width=device-width, initial-scale=1.0">'
            f"<title>{html.escape(title)}</title><meta name=\"description\" content=\"{html.escape(desc)}\">"
            f'<link rel="canonical" href="{url_for(lang)}">{alternates}'
            f'<meta property="og:type" content="website"><meta property="og:site_name" content="Camera Bridge">'
            f'<meta property="og:url" content="{url_for(lang)}"><meta property="og:title" content="{html.escape(title)}">'
            f'<meta property="og:description" content="{html.escape(desc)}">{ld}<link rel=\"stylesheet\" href=\"/img/fonts/fonts.css\"><link rel=\"stylesheet\" href=\"https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/variable/pretendardvariable-dynamic-subset.min.css\"><style>{CSS}{FOOTER_CSS}</style>'
            # 방문 기록(어디서 왔나·매장 클릭, 첫 화면과 같은 /api/usage)과 Vercel 방문 통계
            f'<script defer src="/track.js"></script><script defer src="/_vercel/insights/script.js"></script></head><body><main>')


def build(out: Path) -> dict:
    summary = json.loads(SUMMARY.read_text(encoding="utf-8"))
    entities = summary["entities"]
    by_id = {e["id"]: e for e in entities}
    picked = pick_entities(entities)
    slugs = {e["id"]: slug_of(e["id"]) for e in picked}
    assert len(set(slugs.values())) == len(slugs), "모델 주소가 겹침"
    to_krw = krw_rates()
    usd_krw = to_krw.get("USD", 1350)
    jpy_krw = to_krw.get("JPY", 9)
    convert = {"KRW": lambda k: k, "USD": lambda k: k / usd_krw, "JPY": lambda k: k / jpy_krw}
    for _cur in set(DISPLAY_CURRENCY.values()) - set(convert):
        convert[_cur] = (lambda rate: (lambda k: k / rate))(to_krw[_cur])
    updated = dt.datetime.fromisoformat(summary["generated_at"]).astimezone(dt.timezone(dt.timedelta(hours=9)))
    updated_text = updated.strftime("%Y-%m-%d %H:%M KST")

    # 판매 중 매물을 모델별로
    listings: dict[str, list[dict]] = {eid: [] for eid in slugs}
    for record in json.loads(INDEX.read_text(encoding="utf-8"))["records"]:
        final = record.get("final_output") or {}
        if final.get("sold_quality") != "asking":
            continue
        price, currency = final.get("parsed_price_numeric"), str(final.get("currency") or "KRW").upper()
        rate = to_krw.get(currency)
        if not price or not rate or not final.get("source_url"):
            continue
        for eid in record.get("entity_ids") or []:
            if eid in listings:
                listings[eid].append({"title": final.get("title_raw") or "", "source": final.get("source") or "",
                                      "url": final["source_url"], "cond": final.get("condition_raw") or "",
                                      "price": price, "currency": currency, "krw": price * rate})

    for lang in LANGS:
        shutil.rmtree(out / PATH[lang] / "leica", ignore_errors=True)
    old_marks = json.loads(LASTMOD.read_text(encoding="utf-8")) if LASTMOD.exists() else {}
    marks: dict[str, dict] = {}
    today = updated.date().isoformat()

    def mark(url: str, html_text: str) -> None:
        """기준 시각 줄을 뺀 내용이 지난번과 같으면 그때 날짜를, 바뀌었으면 오늘을 lastmod로"""
        digest = hashlib.sha256(html_text.replace(updated_text, "").encode()).hexdigest()[:16]
        prev = old_marks.get(url) or {}
        marks[url] = {"h": digest, "d": prev["d"] if prev.get("h") == digest else today}

    # 새 제품 정가: 라이카 영국 공식 가격(부가세 포함, scripts/update_leica_msrp.py) — 제품 번호로 모델에 연결
    msrp_path = ROOT / "data" / "config" / "leica_msrp.json"
    msrp = json.loads(msrp_path.read_text(encoding="utf-8")).get("prices", {}) if msrp_path.exists() else {}
    from catalog import codes as catalog_codes
    new_price: dict[str, float] = {}  # 모델 → 영국 정가(GBP)
    for eid, numbers in catalog_codes.CODES.items():
        gb = [msrp[n]["GB"][0] for n in numbers if n in msrp and "GB" in msrp[n] and msrp[n]["GB"][1] == "GBP"]
        if gb:
            new_price[eid] = min(gb)
    gbp_krw = to_krw.get("GBP")

    def series(slug: str) -> str:
        """비슷한 모델 묶음: 주소 앞의 글자 부분 (q2→q, m262→m, sl2→sl, summilux-m-35…→summilux)"""
        return re.match(r"[a-z]+", slug).group(0) if re.match(r"[a-z]+", slug) else slug

    for e in picked:
        eid = e["id"]
        slug = slugs[eid]
        floor = (e.get("b_price_krw") or 0) * MIN_PRICE_RATIO
        rows = sorted((r for r in listings[eid] if r["krw"] >= floor and not RENTAL.search(r["title"])), key=lambda r: r["krw"])
        shops = len({r["source"] for r in rows})
        children = [by_id[c] for c in e.get("children") or [] if c in slugs]
        parent = by_id.get(e.get("parent") or "") if (e.get("parent") or "") in slugs else None
        family_ids = {c["id"] for c in children} | ({parent["id"]} if parent else set()) | {eid}
        related = sorted((x for x in picked if x["id"] not in family_ids and x["kind"] == e["kind"] and not x.get("parent")
                          and series(slugs[x["id"]]) == series(slug)), key=lambda x: (-x.get("active_count", 0), x["id"]))[:8]
        by_country: dict[str, float] = {}
        for r in rows:
            c = shop_parts(r["source"])[1]
            by_country[c] = min(by_country.get(c, r["krw"]), r["krw"])
        for lang in LANGS:
            t, cur = T[lang], DISPLAY_CURRENCY[lang]
            conv = convert[cur]
            name = display_name(e, lang)
            lo_hi = (rows[0]["krw"], rows[-1]["krw"]) if rows else None
            range_text = f"{money(conv(lo_hi[0]), cur, lang, True)} – {money(conv(lo_hi[1]), cur, lang, True)}" if lo_hi else "—"
            title = t["title"].format(name=name)
            desc = t["desc"].format(name=name, active=len(rows), shops=shops, range=range_text)
            json_ld = {"@context": "https://schema.org", "@type": "Product", "name": e["name"].replace(" (all)", ""),
                       "brand": {"@type": "Brand", "name": "Leica"}, "url": page_url(lang, slug)}
            if lo_hi:
                json_ld["offers"] = {"@type": "AggregateOffer", "priceCurrency": cur, "offerCount": len(rows),
                                     "lowPrice": round(conv(lo_hi[0]), 2), "highPrice": round(conv(lo_hi[1]), 2)}
            crumbs = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": t["home"], "item": f"{SITE}/"},
                {"@type": "ListItem", "position": 2, "name": t["list"], "item": page_url(lang)},
                {"@type": "ListItem", "position": 3, "name": name, "item": page_url(lang, slug)}]}
            parts = [head(lang, title, desc, lambda l, s=slug: page_url(l, s), [json_ld, crumbs])]
            parts.append(f'<nav><a href="/">{t["home"]}</a> › <a href="/{PATH[lang]}/leica/">{t["list"]}</a></nav>')
            parts.append(f"<h1>{html.escape(t['h1'].format(name=name))}</h1>")
            if lang in ("en", "ja") and e.get("name_ko"):
                parts.append(f'<p class="ko-name">{html.escape(e["name_ko"].replace(" (전체)", ""))}</p>')
            elif lang == "ko":
                parts.append(f'<p class="ko-name">{html.escape(e["name"].replace(" (all)", ""))}</p>')
            if rows:  # 한 줄 답: AI 검색·검색엔진이 그대로 인용하기 쉬운 숫자 문장
                b = e.get("b_price_krw") or rows[len(rows) // 2]["krw"]
                parts.append(f'<p class="lead">{html.escape(t["lead"].format(name=name, b=money(conv(b), cur, lang, True), n=len(rows), shops=shops, date=updated.date().isoformat()))}</p>')
            parts.append("<dl>")
            parts.append(f"<div><dt>{t['active']}</dt><dd>{t['active_val'].format(n=len(rows), shops=shops)}</dd></div>")
            parts.append(f"<div><dt>{t['range']}</dt><dd>{range_text}</dd></div>")
            if e.get("sold_median_krw") and e.get("sold_price_count"):
                sold = t["sold_val"].format(price=money(conv(e["sold_median_krw"]), cur, lang, True), n=e["sold_price_count"])
                parts.append(f"<div><dt>{t['sold']}</dt><dd>{sold}</dd></div>")
            vs_new = None
            if new_price.get(eid) and gbp_krw and e.get("b_price_krw") and not children:
                vs_new = round(e["b_price_krw"] / (new_price[eid] * gbp_krw) * 100)
                if 40 <= vs_new <= 130:  # 벗어나면 옛 제품과 복각판이 한 번호로 섞였을 수 있어 안 보임 (틀린 숫자보다 안 보이는 게 나음)
                    parts.append(f"<div><dt>{t['new']}</dt><dd>£{new_price[eid]:,.0f}</dd></div>")
                    parts.append(f"<div><dt>{t['vs_new']}</dt><dd>{t['vs_new_val'].format(pct=vs_new)}</dd></div>")
                else:
                    vs_new = None
            parts.append("</dl>")
            note = t["updated"].format(time=updated_text)
            if e.get("sold_median_krw"):
                note += "<br>" + t["sold_note"]
            parts.append(f'<p class="note">{note}</p>')
            if len(rows) >= 2:  # 검색하는 질문에 그대로 답하는 문장 (데이터로 매번 새로 씀)
                mid = rows[len(rows) // 2]["krw"]
                answer = t["a_price"].format(n=len(rows), shops=shops, countries=len(by_country), low=money(conv(lo_hi[0]), cur, lang, True),
                                             high=money(conv(lo_hi[1]), cur, lang, True), median=money(conv(mid), cur, lang, True))
                if e.get("sold_median_krw") and e.get("sold_price_count"):
                    answer += t["a_sold"].format(k=e["sold_price_count"], sold=money(conv(e["sold_median_krw"]), cur, lang, True))
                if vs_new:
                    answer += t["a_new"].format(new=f"£{new_price[eid]:,.0f}", pct=vs_new)
                parts.append(f"<h2>{html.escape(t['q_price'].format(name=name))}</h2><p>{html.escape(answer)}</p>")
                if len(by_country) >= 2:
                    cheap = t["sep"].join(f"{COUNTRY[c][lang]} {money(conv(v), cur, lang, True)}" for c, v in sorted(by_country.items(), key=lambda kv: kv[1])[:4])
                    parts.append(f"<h2>{html.escape(t['q_where'].format(name=name))}</h2><p>{html.escape(t['a_where'].format(list=cheap))}</p>")
            if children or parent:
                parts.append(f"<h2>{t['children'] if children else t['parent']}</h2><ul class=\"links\">")
                for c in children or [parent]:
                    parts.append(f'<li><a href="/{PATH[lang]}/leica/{slugs[c["id"]]}/">{html.escape(display_name(c, lang))}</a> '
                                 f'<span>{t["count"].format(n=c["active_count"])}</span></li>')
                parts.append("</ul>")
            info = [(t["kind"], t["kind_" + e["kind"]])]
            if e.get("mount"):
                info.append((t["mount"], html.escape(str(e["mount"]))))
            if e.get("codes"):
                info.append((t["codes"], html.escape(", ".join(e["codes"][:8]))))
            aka = [a for a in e.get("aliases") or [] if a.lower() != name.lower() and (lang == "ko" or not re.search(r"[가-힣]", a))][:5]
            if aka:
                info.append((t["aka"], html.escape(", ".join(aka))))
            parts.append(f"<h2>{t['info_h']}</h2><dl>" + "".join(f"<div><dt>{k}</dt><dd class=\"small\">{v}</dd></div>" for k, v in info) + "</dl>")
            if rows:
                by_shop: dict[str, list[dict]] = {}
                for r in rows:
                    by_shop.setdefault(r["source"], []).append(r)
                parts.append(f'<h2>{t["shops_h"]}</h2><div class="table"><table><thead><tr><th>{t["col_shop"]}</th>'
                             f'<th>{t["col_count"]}</th><th>{t["col_cur"]}</th><th class="price">{t["col_low"]}</th></tr></thead><tbody>')
                for source, shop_rows in sorted(by_shop.items(), key=lambda kv: kv[1][0]["krw"]):
                    shop, country = shop_parts(source)
                    low = shop_rows[0]
                    shown = money(conv(low["krw"]), cur, lang, low["currency"] != cur)
                    if low["currency"] != cur:
                        shown = t["approx"] + shown
                    parts.append(f'<tr><td>{html.escape(shop)}<span class="orig">{COUNTRY[country][lang]}</span></td>'
                                 f'<td>{len(shop_rows)}</td><td>{html.escape(low["currency"])}</td><td class="price">{shown}</td></tr>')
                parts.append("</tbody></table></div>")
            parts.append(f"<h2>{t['listings']}</h2>")
            if rows:
                parts.append(f'<div class="table"><table><thead><tr><th>{t["col_item"]}</th><th>{t["col_shop"]}</th>'
                             f'<th>{t["col_cond"]}</th><th class="price">{t["col_price"]}</th></tr></thead><tbody>')
                for r in rows[:LISTINGS_SHOWN]:
                    shop, country = shop_parts(r["source"])
                    shown = money(conv(r["krw"]), cur, lang, r["currency"] != cur)
                    orig = "" if r["currency"] == cur else f'<span class="orig">{money(r["price"], r["currency"], lang)}</span>'
                    if r["currency"] != cur:
                        shown = t["approx"] + shown
                    parts.append(f'<tr><td><a href="{html.escape(r["url"])}" rel="noopener" target="_blank">{html.escape(r["title"])}</a></td>'
                                 f'<td>{html.escape(shop)}<span class="orig">{COUNTRY[country][lang]}</span></td>'
                                 f'<td>{html.escape(condition_text(r["cond"]))}</td><td class="price">{shown}{orig}</td></tr>')
                parts.append("</tbody></table></div>")
            else:
                parts.append(f"<p>{t['none']}</p>")
            if related:
                parts.append(f"<h2>{t['related']}</h2><ul class=\"links\">" + "".join(
                    f'<li><a href="/{PATH[lang]}/leica/{slugs[x["id"]]}/">{html.escape(display_name(x, lang))}</a> <span>{t["count"].format(n=x.get("active_count", 0))}</span></li>'
                    for x in related) + "</ul>")
            parts.append(f'<a class="more" href="/?entity={html.escape(eid)}&amp;utm_source=model_page&amp;utm_content={slug}">{html.escape(t["more"].format(name=name))}</a>')
            parts.append(f"</main>{footer_for(lang)}</body></html>\n")
            path = out / PATH[lang] / "leica" / slug / "index.html"
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("".join(parts), encoding="utf-8")
            mark(page_url(lang, slug), "".join(parts))

    # 언어별 목록
    for lang in LANGS:
        t = T[lang]
        parts = [head(lang, t["index_title"], t["index_desc"], lambda l: page_url(l), None)]
        parts.append(f'<nav><a href="/">{t["home"]}</a></nav><h1>{t["index_h1"]}</h1>')
        for kind, heading in (("Body", t["bodies"]), ("Lens", t["lenses"])):
            parts.append(f'<h2>{heading}</h2><ul class="links">')
            for e in picked:
                if e["kind"] == kind:
                    parts.append(f'<li><a href="/{PATH[lang]}/leica/{slugs[e["id"]]}/">{html.escape(display_name(e, lang))}</a> '
                                 f'<span>{t["count"].format(n=e["active_count"])}</span></li>')
            parts.append("</ul>")
        parts.append(f'<p class="note">{t["updated"].format(time=updated_text)}</p></main>{footer_for(lang)}</body></html>\n')
        (out / PATH[lang] / "leica" / "index.html").write_text("".join(parts), encoding="utf-8")
        mark(page_url(lang), "".join(parts))

    # 사이트맵: 첫 화면 + 언어별 목록 + 모델 페이지 (언어별 짝 표시)
    urls = ['  <url><loc>https://camerabridge.io/</loc><changefreq>daily</changefreq></url>']
    for slug in [None] + [slugs[e["id"]] for e in picked]:
        alts = "".join(f'<xhtml:link rel="alternate" hreflang="{l}" href="{page_url(l, slug)}"/>' for l in LANGS)
        for lang in LANGS:
            urls.append(f"  <url><loc>{page_url(lang, slug)}</loc><lastmod>{marks[page_url(lang, slug)]['d']}</lastmod>{alts}</url>")
    (out / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
        + "\n".join(urls) + "\n</urlset>\n", encoding="utf-8")
    # llms.txt (2026-11-08): ChatGPT 등 AI 검색이 사이트를 이해하고 모델 페이지를 인용하기 쉽게 — 무엇인지·숫자 기준·언어별 목록·인기 모델
    top = sorted(picked, key=lambda e: -(e.get("active_count") or 0))[:40]
    shops_n = len({r["source"] for rows in listings.values() for r in rows})
    lines = ["# Camera Bridge", "",
             "> Used Leica cameras and lenses listed at dealers worldwide, matched to the exact model, graded on one condition scale, "
             "and priced as an estimated total to your door (shipping and import tax). Updated several times a day.", "",
             f"- Coverage as of {updated.date().isoformat()}: {sum(len(v) for v in listings.values()) and len({r['url'] for rows in listings.values() for r in rows}):,} listings "
             f"linked to {len(picked)} model pages, from about {shops_n} shops.",
             "- Prices on model pages are shop asking prices converted at the day's exchange rate. 'Sold median' is the median of the last "
             "asking price seen before a listing was marked sold, not a confirmed transaction price.",
             "- Grade scale: S (like new), A, B, C, D. 'Grade B market value' is the typical price for a grade B example.", "",
             "## Model price pages by language", ""]
    for lang in LANGS:
        lines.append(f"- [{lang}]({page_url(lang)})")
    lines += ["", "## Most listed models (English)", ""]
    for e in top:
        lines.append(f"- [{e['name'].replace(' (all)', '')}]({page_url('en', slugs[e['id']])}): {e.get('active_count')} for sale")
    lines += ["", "## Search", "", "- Search any model, nickname (e.g. Bokeh King, Double Stroke), old Leitz code word (e.g. SOOIC) "
              "or order number (e.g. 11873): https://camerabridge.io/", ""]
    (out / "llms.txt").write_text("\n".join(lines), encoding="utf-8")
    if out == ROOT:  # 시험 출력(--out)에서는 기록을 건드리지 않음
        LASTMOD.write_text(json.dumps(marks, ensure_ascii=False, indent=0, sort_keys=True), encoding="utf-8")
    return {"pages": len(picked) * len(LANGS), "models": [slugs[e["id"]] for e in picked], "lastmod": marks}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, default=ROOT)
    result = build(parser.parse_args().out)
    print(f"모델 페이지 {result['pages']}개 ({len(result['models'])}개 모델 × {len(LANGS)}개 언어, 판매 중 {MIN_ACTIVE}개 이상)")


if __name__ == "__main__":
    main()
