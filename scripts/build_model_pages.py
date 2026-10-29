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
LANGS = ("ko", "en", "ja")
PAGE_COUNT = 50          # 매물 많은 순서로 이만큼
LISTINGS_SHOWN = 30      # 페이지마다 보여 줄 판매 중 매물 (싼 순)
DISPLAY_CURRENCY = {"ko": "KRW", "en": "USD", "ja": "JPY"}
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
}
SOURCE_COUNTRY = {"Leica Store Miami": "미국"}

T = {
    "ko": {
        "title": "{name} 중고 시세·매물 | 카메라브릿지",
        "desc": "{name} 중고 판매 중 {active}개 ({shops}개 매장), {range}. 한국·일본·유럽·미국 라이카 매장 매물과 판매완료 가격을 한곳에서.",
        "h1": "{name} 중고 시세", "active": "판매 중", "active_val": "{n}개 · {shops}개 매장",
        "range": "판매 중 가격", "sold": "팔린 매물 중간값", "sold_val": "{price} (팔린 매물 {n}개)",
        "sold_note": "판매완료로 바뀌기 직전에 본 표시 가격의 중간값입니다. 실제 거래 가격과 다를 수 있습니다.",
        "updated": "{time} 기준 · 가격은 매장 표시 가격을 오늘 환율로 원화 환산", "listings": "판매 중 매물 (싼 순)",
        "col_item": "매물", "col_shop": "매장", "col_cond": "상태", "col_price": "가격",
        "more": "카메라브릿지에서 {name} 전체 검색", "children": "세대·버전별", "parent": "전체 보기",
        "none": "지금 판매 중인 매물이 없습니다.", "index_title": "라이카 중고 시세 · 모델별 | 카메라브릿지",
        "index_h1": "라이카 모델별 중고 시세", "index_desc": "라이카 카메라·렌즈 모델별 중고 시세와 판매 중 매물.",
        "count": "{n}개", "home": "카메라브릿지", "list": "모델별 시세", "approx": "약 ",
    },
    "en": {
        "title": "{name} Used Price & Listings | Camera Bridge",
        "desc": "{active} used {name} listings from {shops} shops, {range}. Leica shops in Korea, Japan, Europe and the US, with sold prices, in one place.",
        "h1": "{name} used prices", "active": "For sale now", "active_val": "{n} listings · {shops} shops",
        "range": "Asking prices", "sold": "Sold median", "sold_val": "{price} ({n} sold listings)",
        "sold_note": "Median of the last asking price seen before a listing was marked sold. Actual sale prices may differ.",
        "updated": "As of {time} · shop prices converted to USD at today's rate", "listings": "For sale now (cheapest first)",
        "col_item": "Listing", "col_shop": "Shop", "col_cond": "Condition", "col_price": "Price",
        "more": "Search all {name} on Camera Bridge", "children": "By generation / version", "parent": "See all",
        "none": "No listings for sale right now.", "index_title": "Leica Used Prices by Model | Camera Bridge",
        "index_h1": "Leica used prices by model", "index_desc": "Used prices and live listings for Leica cameras and lenses, by model.",
        "count": "{n}", "home": "Camera Bridge", "list": "Prices by model", "approx": "≈ ",
    },
    "ja": {
        "title": "{name} 中古相場・在庫 | Camera Bridge",
        "desc": "{name} の中古在庫 {active} 点（{shops} 店）、{range}。韓国・日本・欧州・米国のライカ取扱店の在庫と販売済み価格をまとめて。",
        "h1": "{name} 中古相場", "active": "販売中", "active_val": "{n} 点 · {shops} 店",
        "range": "販売価格", "sold": "販売済み中央値", "sold_val": "{price}（販売済み {n} 点）",
        "sold_note": "販売済みになる直前に確認した表示価格の中央値です。実際の取引価格とは異なる場合があります。",
        "updated": "{time} 時点 · 各店の表示価格を本日のレートで円換算", "listings": "販売中の在庫（安い順）",
        "col_item": "商品", "col_shop": "店舗", "col_cond": "状態", "col_price": "価格",
        "more": "Camera Bridge で {name} をすべて検索", "children": "世代・バージョン別", "parent": "すべて見る",
        "none": "現在販売中の在庫はありません。", "index_title": "ライカ中古相場 · モデル別 | Camera Bridge",
        "index_h1": "ライカ モデル別中古相場", "index_desc": "ライカのカメラ・レンズのモデル別中古相場と販売中の在庫。",
        "count": "{n} 点", "home": "Camera Bridge", "list": "モデル別相場", "approx": "約",
    },
}

CSS = """
:root{--bg:#fff;--text:#16181a;--soft:#5d6266;--muted:#8a9094;--border:#e1e4e3;--accent:#1f4a3a;--row:#f5f6f5}
@media (prefers-color-scheme:dark){:root{--bg:#141617;--text:#e8eaea;--soft:#a9afb2;--muted:#7d8488;--border:#2c3133;--accent:#8cc5ad;--row:#1b1e1f}}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--text);font:15px/1.6 Inter,"Pretendard Variable",ui-sans-serif,system-ui,-apple-system,"Segoe UI",sans-serif}
main{max-width:960px;margin:0 auto;padding:24px 16px 64px}
nav{font-size:13px;color:var(--muted);margin-bottom:20px}
nav a{color:var(--soft)}
h1{font-size:26px;line-height:1.3;margin:0 0 4px}
.ko-name{color:var(--soft);margin:0 0 20px}
dl{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:0;margin:0 0 8px;border-top:1px solid var(--border)}
dl div{padding:12px 0;border-bottom:1px solid var(--border)}
dt{font-size:13px;color:var(--muted)}
dd{margin:2px 0 0;font-size:18px;font-weight:600}
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

SYMBOL = {"KRW": "₩", "USD": "$", "JPY": "¥", "EUR": "€", "GBP": "£", "HKD": "HK$", "CHF": "CHF ", "DKK": "DKK ",
          "AUD": "A$", "SGD": "S$", "CAD": "C$", "MYR": "RM "}


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
    """매물 많은 순 PAGE_COUNT개. '세대 미표기' 묶음, 부모와 사실상 같은 '기본형'은 뺀다."""
    by_id = {e["id"]: e for e in entities}
    pool = []
    for e in entities:
        if e.get("feature") or e["kind"] not in ("Body", "Lens") or not e.get("active_count"):
            continue
        if "unspecified" in e["id"]:
            continue
        parent = by_id.get(e.get("parent") or "")
        if e["id"].endswith(":standard") and parent and parent["listing_count"] <= e["listing_count"] * 1.5:
            continue
        pool.append(e)
    pool.sort(key=lambda e: (-e["listing_count"], e["id"]))
    return pool[:PAGE_COUNT]


def page_url(lang: str, slug: str | None = None) -> str:
    return f"{SITE}/{lang}/leica/{slug}/" if slug else f"{SITE}/{lang}/leica/"


def head(lang: str, title: str, desc: str, url_for, json_ld: dict | None) -> str:
    alternates = "".join(f'<link rel="alternate" hreflang="{l}" href="{url_for(l)}">' for l in LANGS)
    alternates += f'<link rel="alternate" hreflang="x-default" href="{url_for("en")}">'
    ld = f'<script type="application/ld+json">{json.dumps(json_ld, ensure_ascii=False)}</script>' if json_ld else ""
    return (f'<!DOCTYPE html><html lang="{lang}"><head><meta charset="UTF-8">'
            f'<meta name="viewport" content="width=device-width, initial-scale=1.0">'
            f"<title>{html.escape(title)}</title><meta name=\"description\" content=\"{html.escape(desc)}\">"
            f'<link rel="canonical" href="{url_for(lang)}">{alternates}'
            f'<meta property="og:type" content="website"><meta property="og:site_name" content="Camera Bridge">'
            f'<meta property="og:url" content="{url_for(lang)}"><meta property="og:title" content="{html.escape(title)}">'
            f'<meta property="og:description" content="{html.escape(desc)}">{ld}<style>{CSS}{FOOTER_CSS}</style></head><body><main>')


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
        shutil.rmtree(out / lang / "leica", ignore_errors=True)

    for e in picked:
        eid = e["id"]
        slug = slugs[eid]
        floor = (e.get("b_price_krw") or 0) * MIN_PRICE_RATIO
        rows = sorted((r for r in listings[eid] if r["krw"] >= floor and not RENTAL.search(r["title"])), key=lambda r: r["krw"])
        shops = len({r["source"] for r in rows})
        children = [by_id[c] for c in e.get("children") or [] if c in slugs]
        parent = by_id.get(e.get("parent") or "") if (e.get("parent") or "") in slugs else None
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
            parts = [head(lang, title, desc, lambda l, s=slug: page_url(l, s), json_ld)]
            parts.append(f'<nav><a href="/">{t["home"]}</a> › <a href="/{lang}/leica/">{t["list"]}</a></nav>')
            parts.append(f"<h1>{html.escape(t['h1'].format(name=name))}</h1>")
            if lang != "ko" and e.get("name_ko"):
                parts.append(f'<p class="ko-name">{html.escape(e["name_ko"].replace(" (전체)", ""))}</p>')
            elif lang == "ko":
                parts.append(f'<p class="ko-name">{html.escape(e["name"].replace(" (all)", ""))}</p>')
            parts.append("<dl>")
            parts.append(f"<div><dt>{t['active']}</dt><dd>{t['active_val'].format(n=len(rows), shops=shops)}</dd></div>")
            parts.append(f"<div><dt>{t['range']}</dt><dd>{range_text}</dd></div>")
            if e.get("sold_median_krw") and e.get("sold_price_count"):
                sold = t["sold_val"].format(price=money(conv(e["sold_median_krw"]), cur, lang, True), n=e["sold_price_count"])
                parts.append(f"<div><dt>{t['sold']}</dt><dd>{sold}</dd></div>")
            parts.append("</dl>")
            note = t["updated"].format(time=updated_text)
            if e.get("sold_median_krw"):
                note += "<br>" + t["sold_note"]
            parts.append(f'<p class="note">{note}</p>')
            if children or parent:
                parts.append(f"<h2>{t['children'] if children else t['parent']}</h2><ul class=\"links\">")
                for c in children or [parent]:
                    parts.append(f'<li><a href="/{lang}/leica/{slugs[c["id"]]}/">{html.escape(display_name(c, lang))}</a> '
                                 f'<span>{t["count"].format(n=c["active_count"])}</span></li>')
                parts.append("</ul>")
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
            parts.append(f'<a class="more" href="/?entity={html.escape(eid)}&amp;utm_source=model_page&amp;utm_content={slug}">{html.escape(t["more"].format(name=name))}</a>')
            parts.append(f"</main>{footer(lang)}</body></html>\n")
            path = out / lang / "leica" / slug / "index.html"
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("".join(parts), encoding="utf-8")

    # 언어별 목록
    for lang in LANGS:
        t = T[lang]
        parts = [head(lang, t["index_title"], t["index_desc"], lambda l: page_url(l), None)]
        parts.append(f'<nav><a href="/">{t["home"]}</a></nav><h1>{t["index_h1"]}</h1><ul class="links">')
        for e in picked:
            parts.append(f'<li><a href="/{lang}/leica/{slugs[e["id"]]}/">{html.escape(display_name(e, lang))}</a> '
                         f'<span>{t["count"].format(n=e["active_count"])}</span></li>')
        parts.append(f'</ul><p class="note">{t["updated"].format(time=updated_text)}</p></main>{footer(lang)}</body></html>\n')
        (out / lang / "leica" / "index.html").write_text("".join(parts), encoding="utf-8")

    # 사이트맵: 첫 화면 + 언어별 목록 + 모델 페이지 (언어별 짝 표시)
    lastmod = updated.date().isoformat()
    urls = ['  <url><loc>https://camerabridge.io/</loc><changefreq>daily</changefreq></url>']
    for slug in [None] + [slugs[e["id"]] for e in picked]:
        alts = "".join(f'<xhtml:link rel="alternate" hreflang="{l}" href="{page_url(l, slug)}"/>' for l in LANGS)
        for lang in LANGS:
            urls.append(f"  <url><loc>{page_url(lang, slug)}</loc><lastmod>{lastmod}</lastmod>{alts}</url>")
    (out / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
        + "\n".join(urls) + "\n</urlset>\n", encoding="utf-8")
    return {"pages": len(picked) * len(LANGS), "models": [slugs[e["id"]] for e in picked]}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, default=ROOT)
    result = build(parser.parse_args().out)
    print(f"모델 페이지 {result['pages']}개 ({len(result['models'])}개 모델 × {len(LANGS)}개 언어)")


if __name__ == "__main__":
    main()
