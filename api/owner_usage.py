"""사장님 전용 방문 현황 화면: /owner/usage

사용 기록(api/usage.py 가 쌓은 Blob usage/)과 의견(feedback/)을 읽어 한 화면에 보여 준다.
들어가기: /owner/usage?key=<OWNER_DASHBOARD_KEY> 로 한 번 열면 쿠키가 남아 다음부터는 /owner/usage 만으로 열림.
기간: ?days=1 · 7(기본) · 30, 하루만: ?date=YYYY-MM-DD (날짜별 표·막대를 누르면 그날로)
2026-11-07부터 둘러보기만 한 방문(첫 화면·모델 시세 페이지)도 남고, 들어온 곳은 도메인+경로까지 남는다.
"""
from __future__ import annotations

import collections
import datetime as dt
import hmac
import html
import json
import os
import sys
from concurrent.futures import ThreadPoolExecutor
from http.cookies import SimpleCookie
from http.server import BaseHTTPRequestHandler
from pathlib import Path
from urllib.parse import parse_qs, urlparse
from zoneinfo import ZoneInfo

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from scripts.usage_report import summarize, visitor_key  # noqa: E402

KST = dt.timezone(dt.timedelta(hours=9))
COOKIE = "cb_owner"
# 이 화면을 연 브라우저(사장님)는 방문 기록에서 뺀다: /api/usage 에만 가는 표시 쿠키 (값은 비밀 아님, 끄면 기록이 빠질 뿐)
SKIP_USAGE_COOKIE = "cb_skip_usage=1; Path=/api/usage; Max-Age=31536000; HttpOnly; Secure; SameSite=Lax"
ANALYTICS_URL = "https://vercel.com/camerabridge/camerabridge/analytics"
# 들어온 곳 묶음 이름: 도메인에 이 글자가 들어가면 (위에서부터 먼저 맞는 것)
REFERRER_GROUPS = [
    ("com.reddit.frontpage", "레딧 앱"), ("reddit.com", "레딧"), ("google.", "구글 검색"), ("naver.com", "네이버"),
    ("bing.com", "Bing 검색"), ("daum.net", "다음"), ("duckduckgo.com", "DuckDuckGo"), ("yahoo.", "야후"),
    ("yandex.", "얀덱스"), ("ecosia.org", "Ecosia"), ("chatgpt.com", "ChatGPT"), ("perplexity.ai", "Perplexity"),
    ("instagram.com", "인스타그램"), ("facebook.com", "페이스북"), ("threads.", "스레드"), ("t.co", "X(트위터)"),
    ("x.com", "X(트위터)"), ("youtube.com", "유튜브"), ("clien.net", "클리앙"), ("dcinside.com", "디시인사이드"),
    ("slrclub.com", "SLR클럽"), ("kakao.com", "카카오"), ("github.com", "GitHub"), ("rangefinderforum.com", "Rangefinder Forum"),
    ("l-camera-forum.com", "L-Camera Forum"), ("fredmiranda.com", "FredMiranda"), ("vercel.app", "Vercel 미리보기"),
]
SEARCH_GROUPS = {"구글 검색", "네이버", "Bing 검색", "다음", "DuckDuckGo", "야후", "얀덱스", "Ecosia"}
MAX_READS = 400  # 한 번 열 때 읽는 기록 수 상한 (Blob 읽기 한도 아끼기)


def authorized(key: str, cookie_value: str) -> bool:
    expected = os.environ.get("OWNER_DASHBOARD_KEY", "")
    if len(expected) < 16:
        return False
    return any(value and hmac.compare_digest(value, expected) for value in (key, cookie_value))


def _read_many(blob, items) -> list[dict]:
    def read(item):
        try:
            return json.loads(blob.get(item.url, access="private").content)
        except Exception:  # noqa: BLE001
            return None
    with ThreadPoolExecutor(max_workers=8) as pool:
        return [entry for entry in pool.map(read, items) if entry]


def load(days: int, date: str | None = None) -> tuple[list[dict], list[dict], bool]:
    import pgstore  # noqa: WPS433
    if pgstore.enabled():  # Neon Postgres (2026-11 Blob 무료 한도 초과 뒤) — 400건 상한 없이 한 번에
        start = date or (dt.datetime.now(KST).date() - dt.timedelta(days=days - 1)).isoformat()
        entries = pgstore.usage_since(start, date)
        try:
            feedback = pgstore.recent_feedback(20)
        except Exception:  # noqa: BLE001
            feedback = []
        return entries, feedback, False
    from vercel import blob  # noqa: WPS433

    if date:  # 하루만
        usage_items = list(blob.iter_objects(prefix=f"usage/{date}/"))
    else:
        start = (dt.datetime.now(KST).date() - dt.timedelta(days=days - 1)).isoformat()
        usage_items = [i for i in blob.iter_objects(prefix="usage/") if i.pathname.split("/")[1] >= start]
    usage_items.sort(key=lambda i: i.pathname, reverse=True)
    cut = len(usage_items) > MAX_READS
    feedback_items = sorted(blob.iter_objects(prefix="feedback/"), key=lambda i: i.pathname, reverse=True)[:20]
    return _read_many(blob, usage_items[:MAX_READS]), _read_many(blob, feedback_items), cut


COUNTRY_NAMES = {"KR": "한국", "JP": "일본", "US": "미국", "GB": "영국", "DE": "독일", "FR": "프랑스", "IT": "이탈리아",
                 "NL": "네덜란드", "CN": "중국", "TW": "대만", "HK": "홍콩", "SG": "싱가포르", "CA": "캐나다", "AU": "호주",
                 "CH": "스위스", "AT": "오스트리아", "ES": "스페인", "DK": "덴마크", "SE": "스웨덴", "BE": "벨기에"}


# 2026-11-07 전 기록(시간대 없음)은 나라로 짐작: 시간대가 하나뿐인 나라만 (미국·캐나다·호주·브라질 등은 몰라서 한국 시각)
COUNTRY_TZ = {"KR": "Asia/Seoul", "JP": "Asia/Tokyo", "GB": "Europe/London", "IE": "Europe/Dublin", "DE": "Europe/Berlin",
              "FR": "Europe/Paris", "IT": "Europe/Rome", "NL": "Europe/Amsterdam", "BE": "Europe/Brussels", "ES": "Europe/Madrid",
              "PT": "Europe/Lisbon", "GR": "Europe/Athens", "CH": "Europe/Zurich", "AT": "Europe/Vienna", "DK": "Europe/Copenhagen",
              "SE": "Europe/Stockholm", "FI": "Europe/Helsinki", "PL": "Europe/Warsaw", "CZ": "Europe/Prague", "TW": "Asia/Taipei",
              "HK": "Asia/Hong_Kong", "SG": "Asia/Singapore", "CN": "Asia/Shanghai", "TH": "Asia/Bangkok", "MY": "Asia/Kuala_Lumpur"}


def _local_time(created_at: str, tz: str | None, country: str | None, fmt: str = "%m-%d %H:%M") -> tuple[str, str]:
    """(현지 시각 'MM-DD HH:MM', 설명). 시간대를 모르면 한국 시각 그대로."""
    try:
        when = dt.datetime.fromisoformat(created_at)
    except (TypeError, ValueError):
        return str(created_at or "")[5:16].replace("T", " "), ""
    name = tz or COUNTRY_TZ.get(country or "")
    try:
        zone = ZoneInfo(name) if name else None
    except Exception:  # noqa: BLE001
        zone = None
    if not zone:
        return when.astimezone(KST).strftime(fmt), "한국 시각 (현지 시간대 모름)"
    local = when.astimezone(zone)
    city = name.split("/")[-1].replace("_", " ")
    return local.strftime(fmt), f"{city} · 한국 {when.astimezone(KST).strftime('%m-%d %H:%M')}"


def _country_name(code: str | None) -> str:
    """'KR' → '🇰🇷 한국'. 2026-10-29 전 기록에는 나라가 없음."""
    if not code:
        return "기록 전"
    flag = "".join(chr(0x1F1E6 + ord(ch) - ord("A")) for ch in code)
    return f"{flag} {COUNTRY_NAMES.get(code, code)}"


def _ref_name(host: str | None, landing: str | None = None) -> str:
    """들어온 곳 묶음 이름. host 는 2026-11-07부터 '도메인/경로', 그 전은 도메인만."""
    if not host and "utm_source=model_page" in (landing or ""):
        return "카메라브릿지 모델 페이지"
    if not host:
        return "직접·앱 (주소 입력·즐겨찾기·레딧 앱 등)"
    domain = host.split("/", 1)[0].lower()
    for key, name in REFERRER_GROUPS:
        # 'google.' 처럼 점으로 끝나면 나라별 도메인(google.co.kr 등)까지, 아니면 그 도메인과 하위 도메인만
        hit = ("." + key) in ("." + domain) if key.endswith(".") else domain == key or domain.endswith("." + key)
        if hit:
            return name
    return domain


def _ref_detail(host: str | None) -> str | None:
    """검색엔진은 경로가 의미 없어 묶음 이름만, 그 밖(커뮤니티 글 등)은 도메인+경로 그대로."""
    if not host:
        return None
    return _ref_name(host) if _ref_name(host) in SEARCH_GROUPS else host


def visits(entries: list[dict]) -> list[dict]:
    """방문별 최신순. 새 기록은 브라우저·sid별, 예전 기록은 IP·날짜별."""
    grouped: dict[str, dict] = {}
    for e in sorted(entries, key=lambda e: (visitor_key(e), e.get("created_at", ""), e.get("part", 1))):
        v = grouped.setdefault(visitor_key(e), {"vid": e.get("vid"), "start": e.get("created_at", ""), "end": e.get("created_at", ""), "referrer": e.get("referrer"), "landing": e.get("landing"),
                                          "locale": e.get("locale"), "currency": e.get("currency"), "mobile": e.get("mobile"), "country": e.get("country"), "tz": e.get("tz"),
                                          "duration_s": 0, "scroll": 0, "steps": []})
        v["start"] = min(v["start"], e.get("created_at", "")) or v["start"]
        v["end"] = max(v["end"], e.get("created_at", ""))
        v["duration_s"] = max(v["duration_s"], e.get("duration_s") or 0)
        v["scroll"] = max(v.get("scroll") or 0, e.get("scroll") or 0)
        v["country"] = v["country"] or e.get("country")
        v["tz"] = v["tz"] or e.get("tz")
        page = [("페이지", {"page": e["page"], "s": None})] if e.get("page") and e["page"] not in v.setdefault("pages", []) else []
        if page:
            v["pages"].append(e["page"])
        v["steps"] += page + [("검색", s) for s in e.get("searches", [])] + [("클릭", c) for c in e.get("clicks", [])]
    for v in grouped.values():
        v["steps"].sort(key=lambda step: -1 if step[1].get("s") is None else step[1]["s"])
    return sorted(grouped.values(), key=lambda v: v["end"], reverse=True)


def _esc(value) -> str:
    return html.escape(str(value if value is not None else ""))


def _table(title: str, rows, empty="없음", note="") -> str:
    body = "".join(f"<tr><td>{_esc(name)}</td><td class=n>{_esc(count)}</td></tr>" for name, count in rows) or f"<tr><td class=muted>{empty}</td><td></td></tr>"
    return f"<section class=card><h2>{_esc(title)}</h2>{f'<p class=muted>{note}</p>' if note else ''}<table>{body}</table></section>"


def _bars(entries: list[dict], days: int, date: str | None = None) -> str:
    today = dt.datetime.now(KST).date()
    per_day = collections.defaultdict(set)
    for e in entries:
        per_day[str(e.get("created_at", ""))[:10]].add(visitor_key(e))
    labels = [str(today - dt.timedelta(days=i)) for i in range(days - 1, -1, -1)]
    if days == 1 or date:  # 하루는 시간별
        per_hour = collections.defaultdict(set)
        for e in entries:
            per_hour[str(e.get("created_at", ""))[11:13]].add(visitor_key(e))
        labels, counts = [f"{h:02d}" for h in range(24)], [len(per_hour[f"{h:02d}"]) for h in range(24)]
    else:
        counts = [len(per_day[d]) for d in labels]
    top = max(counts + [1])
    hourly = days == 1 or bool(date)

    def bar(l, c):
        inner = f"<span style='height:{round(c / top * 100)}%'></span><b>{c or ''}</b><i>{_esc(l + '시' if hourly else l[-5:])}</i>"
        if not hourly:  # 날짜 막대를 누르면 그날 하루 보기
            inner = f"<a href='?date={_esc(l)}'>{inner}</a>"
        return f"<div class=bar title='{_esc(l)}: {c}'>{inner}</div>"
    bars = "".join(bar(l, c) for l, c in zip(labels, counts))
    title = f"{date} 시간별" if date else ("오늘 시간별" if days == 1 else "날짜별 (막대를 누르면 그날 보기)")
    return f"<section class='card wide'><h2>{_esc(title)} 방문</h2><div class=bars>{bars}</div></section>"


def _day_table(entries: list[dict], days: int) -> str:
    """날짜별 한 줄: 방문·직접 검색한 방문·판매처 간 방문·많이 온 곳. 날짜를 누르면 그날 보기."""
    today = dt.datetime.now(KST).date()
    by_day: dict[str, list[dict]] = collections.defaultdict(list)
    for e in entries:
        by_day[str(e.get("created_at", ""))[:10]].append(e)
    rows = []
    for i in range(days):
        d = str(today - dt.timedelta(days=i))
        es = by_day.get(d, [])
        sids = {visitor_key(e) for e in es}
        typed = {visitor_key(e) for e in es if any(x.get("via") in ("typed", "pick") for x in e.get("searches", []))}
        clicked = {visitor_key(e) for e in es if e.get("clicks")}
        firsts = {visitor_key(e): e for e in sorted(es, key=lambda e: e.get("created_at", ""), reverse=True)}.values()
        top = ", ".join(f"{n} {c}" for n, c in collections.Counter(_ref_name(e.get("referrer"), e.get("landing")) for e in firsts).most_common(3))
        rows.append(f"<tr><td class=nowrap><a href='?date={d}'>{d[5:]}</a></td><td class=n>{len(sids)}</td><td class=n>{len(typed)}</td>"
                    f"<td class=n>{len(clicked)}</td><td><small>{_esc(top) or '-'}</small></td></tr>")
    head = "<tr><td class=muted>날짜</td><td class='muted n'>방문</td><td class='muted n'>직접 검색</td><td class='muted n'>판매처로</td><td class=muted>많이 온 곳</td></tr>"
    return f"<section class='card wide days'><h2>날짜별 (날짜를 누르면 그날 하루)</h2><table>{head}{''.join(rows)}</table></section>"


def load_browser_history(entries: list[dict]) -> dict[str, dict] | None:
    import pgstore
    ids = sorted({e["vid"] for e in entries if e.get("vid")})
    if not ids:
        return {}
    if not pgstore.enabled():
        return None  # Blob 조회 기간만으로 누적 횟수를 추정하지 않는다.
    try:
        return pgstore.browser_history(ids)
    except Exception:  # 누적 집계 실패로 기존 방문 화면까지 막지 않는다.
        return None


def _browser_cell(v: dict, history: dict[str, dict] | None) -> str:
    vid = v.get("vid")
    if not vid:
        return '<span class=muted>재방문 식별 없음</span>'
    label = f"브라우저 {_esc(vid[:8])}"
    record = (history or {}).get(vid)
    if not record:
        return label + '<br><small>누적 집계 확인 불가</small>'
    first, first_note = _local_time(record["first_seen"], v["tz"], v["country"], "%Y-%m-%d %H:%M")
    last, last_note = _local_time(record["last_seen"], v["tz"], v["country"], "%Y-%m-%d %H:%M")
    return (f'{label}<br><b>누적 {_esc(record["visits"])}회</b>'
            f'<br><small title="{_esc(first_note)}">첫 방문 {_esc(first)}</small>'
            f'<br><small title="{_esc(last_note)}">최근 방문 {_esc(last)}</small>')


def render(entries: list[dict], feedback: list[dict], days: int, cut: bool, date: str | None = None,
           history: dict[str, dict] | None = None) -> str:
    r = summarize(entries)
    firsts = {visitor_key(e): e for e in sorted(entries, key=lambda e: (e.get("created_at", ""), e.get("part", 1)), reverse=True)}.values()
    ref_counts = collections.Counter(_ref_name(e.get("referrer"), e.get("landing")) for e in firsts)
    ref_details = collections.Counter(d for d in (_ref_detail(e.get("referrer")) for e in firsts) if d)
    country_counts = collections.Counter(_country_name(v["country"]) for v in visits(entries))
    pct = lambda x: "-" if x is None else f"{round(x * 100)}%"  # noqa: E731
    now = dt.datetime.now(KST).strftime("%Y-%m-%d %H:%M")
    tabs = "".join(f"<a class='{'on' if d == days and not date else ''}' href='?days={d}'>{label}</a>" for d, label in ((1, "오늘"), (7, "7일"), (30, "30일")))
    if date:  # 하루 보기: 전날·다음날
        day = dt.date.fromisoformat(date)
        prev_d, next_d = day - dt.timedelta(days=1), day + dt.timedelta(days=1)
        nxt = f"<a href='?date={next_d}'>다음날 ▶</a>" if next_d <= dt.datetime.now(KST).date() else ""
        tabs = f"<a href='?date={prev_d}'>◀ 전날</a><a class=on href='?date={date}'>{date[5:]}</a>{nxt}" + tabs

    rows = []
    for v in visits(entries)[:60]:
        steps = []
        for kind, s in v["steps"]:
            if kind == "페이지":
                steps.append(f"<span class='step page'>📄 {_esc(s.get('page'))}</span>")
                continue
            if kind == "검색":
                tail = "결과 없음" if s.get("results") == 0 else f"판매 중 {s.get('active', 0)} / 전체 {s.get('results', 0)}"
                via = s.get("via")
                if via == "typed":
                    label = f"⌨️ 직접 검색 “{_esc(s.get('q'))}”"
                elif via == "pick":
                    label = (f"⌨️ “{_esc(s.get('typed'))}” 치고 → {_esc(s.get('q'))} 고름" if s.get("typed") else f"⌨️ 후보에서 {_esc(s.get('q'))} 고름")
                elif via == "link":
                    label = f"🔗 링크로 열림: {_esc(s.get('q'))}"
                elif via == "chip":
                    label = f"👆 모델 버튼: {_esc(s.get('q'))}"
                else:
                    label = f"🔎 {_esc(s.get('q'))}"
                steps.append(f"<span class='step{' typed' if via in ('typed', 'pick') else ''}'>{label} <small>{tail}</small></span>")
            else:
                steps.append(f"<span class='step click'>↗ {_esc(s.get('host'))}</span>")
        when, when_note = _local_time(v["start"], v["tz"], v["country"])
        device = "📱" if v["mobile"] else "💻"
        rows.append(f"<tr><td class=nowrap>{_esc(when)}{f"<br><small>{_esc(when_note)}</small>" if when_note else ''}</td><td>{_esc(_ref_name(v['referrer'], v['landing']))}{f"<br><small>{_esc(v['referrer'])}</small>" if v['referrer'] and '/' in v['referrer'] else ''}{f"<br><small>→ {_esc(v['landing'])}</small>" if v['landing'] and v['landing'] != '/' else ''}</td><td class=nowrap>{_esc(_country_name(v['country']))}<br><small>{device} {_esc(v['locale'] or '-')} · {_esc(v['currency'] or '')}</small></td>"
                    f"<td class=nowrap>{_browser_cell(v, history)}</td><td class=nowrap>{_esc(v['duration_s'] // 60)}분 {_esc(v['duration_s'] % 60)}초{f"<br><span class=muted>{_esc(v['scroll'])}% 내려 봄</span>" if v.get('scroll') else ''}</td><td>{''.join(steps)}</td></tr>")
    visit_table = "".join(rows) or "<tr><td colspan=6 class=muted>이 기간에 방문이 없습니다</td></tr>"

    fb_rows = "".join(f"<tr><td class=nowrap>{_esc(str(f.get('created_at', ''))[5:16].replace('T', ' '))}</td><td>{_esc(f.get('locale') or '-')}</td><td>{_esc(f.get('message'))}</td></tr>" for f in feedback) \
        or "<tr><td colspan=3 class=muted>아직 없음</td></tr>"

    return f"""<!doctype html><html lang=ko><head><meta charset=utf-8><meta name=viewport content="width=device-width,initial-scale=1">
<meta name=robots content="noindex,nofollow"><title>방문 현황 · Camera Bridge</title><style>
:root{{--bg:#f6f6f4;--card:#fff;--text:#1d1d1b;--muted:#77756f;--line:#e4e2dc;--accent:#c8102e;--soft:#f1efe9}}
@media (prefers-color-scheme:dark){{:root{{--bg:#151514;--card:#1e1e1c;--text:#eceae4;--muted:#9a978f;--line:#33322f;--accent:#ff5a6e;--soft:#272724}}}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--text);font:15px/1.5 -apple-system,BlinkMacSystemFont,"Apple SD Gothic Neo",sans-serif}}
main{{max-width:1100px;margin:0 auto;padding:20px 16px 60px}}header{{display:flex;flex-wrap:wrap;gap:12px;align-items:center;justify-content:space-between}}
h1{{font-size:22px;margin:0}}h2{{font-size:15px;margin:0 0 10px}}.muted{{color:var(--muted)}}small{{color:var(--muted)}}
.tabs a{{padding:6px 12px;border:1px solid var(--line);border-radius:999px;color:var(--text);text-decoration:none;margin-left:4px}}.tabs a.on{{background:var(--text);color:var(--bg)}}
.kpis{{display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin:16px 0}}.kpi{{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:12px}}
.kpi b{{display:block;font-size:26px}}.kpi span{{color:var(--muted);font-size:13px}}
.grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:10px}}.card{{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:14px;overflow:auto}}.wide{{grid-column:1/-1}}
table{{width:100%;border-collapse:collapse}}td{{padding:6px 4px;border-top:1px solid var(--line);vertical-align:top}}tr:first-child td{{border-top:0}}td.n{{text-align:right;font-variant-numeric:tabular-nums}}.nowrap{{white-space:nowrap}}
.visit-table{{min-width:1000px}}
.step{{display:inline-block;background:var(--soft);border-radius:8px;padding:2px 8px;margin:2px 4px 2px 0}}.step.click{{background:var(--accent);color:#fff}}.step.page{{background:transparent;border:1px solid var(--line)}}.step.typed{{outline:2px solid var(--text)}}
.days td a{{color:var(--text)}}.days tr.on td{{font-weight:700}}.bar a{{display:contents;color:inherit}}
.bars{{display:flex;gap:4px;align-items:flex-end;height:130px}}.bar{{flex:1;display:flex;flex-direction:column;justify-content:flex-end;align-items:center;height:100%;min-width:0}}
.bar span{{display:block;width:100%;background:var(--accent);border-radius:4px 4px 0 0;min-height:1px}}.bar b{{font-size:11px;order:-1}}.bar i{{font-size:10px;color:var(--muted);font-style:normal;white-space:nowrap}}
.note{{background:var(--soft);border-radius:10px;padding:10px 12px;margin-top:12px;font-size:13px}}a{{color:var(--accent)}}
@media (max-width:760px){{.kpis{{grid-template-columns:repeat(2,1fr)}}.grid{{grid-template-columns:1fr}}td{{font-size:13px}}}}
</style></head><body><main>
<header><div><h1>방문 현황{f' · {_esc(date)}' if date else ''}</h1><span class=muted>{now} 기준 · 새 기록은 브라우저의 방문별 · 예전 기록은 같은 IP 하루 1번</span></div><nav class=tabs>{tabs}</nav></header>
<div class=kpis>
<div class=kpi><b>{r['visits']}</b><span>방문</span></div>
<div class=kpi><b>{r['visits_with_activity']}</b><span>검색·클릭한 방문</span></div>
<div class=kpi><b>{r['visits_with_click']}</b><span>판매처까지 간 방문</span></div>
<div class=kpi><b>{pct(r['mobile_share'])}</b><span>휴대폰</span></div></div>
<div class=grid>
{_bars(entries, days, date)}
{_day_table(entries, days) if days > 1 and not date else ''}
{_table('어디서 왔나', ref_counts.most_common(12), note='휴대폰 앱(레딧·카카오톡 앱 등)은 출처를 안 알려 줘서 "직접·앱"으로 잡힘')}
{_table('들어온 곳 자세히', ref_details.most_common(15), note='커뮤니티 글·사이트는 주소까지. 구글은 검색어를 안 알려 줌 → 검색어는 서치 콘솔에서')}
{_table('처음 들어온 페이지', r['landings'])}
{_table('많이 본 페이지', r['pages'][:10])}
{_table('나라별 방문', country_counts.most_common(15), note='접속한 곳 기준 (2026-10-29부터 기록, 그 전은 "기록 전")')}
{_table('화면 언어', r['locales'])}
{_table('클릭한 판매처', r['click_hosts'])}
{_table('손님이 직접 친 검색어', r['typed_queries'][:10], note='검색창에 직접 친 것 (후보를 골랐으면 고르기 전에 친 글자)')}
{_table('링크·버튼으로 연 모델', r['opened_models'][:10], note='모델 시세 페이지의 "전체 매물 보기"나 첫 화면 모델 버튼')}
{_table('결과 0건 검색어 (고칠 것)', r['zero_result_queries'][:10])}
{_table('판매 중 0건 검색어', r['no_active_queries'][:10])}
<section class='card wide'><h2>최근 방문 (새 기록은 한 줄 = 한 번의 방문)</h2>
<p class=muted>누적 횟수·첫 방문·최근 방문은 선택 기간과 관계없이 보유 기록 전체(최근 365일) 기준입니다.
브라우저 식별 적용 이후부터 집계하며, 저장소 삭제·다른 브라우저·다른 기기는 별도로 셉니다.
같은 탭의 페이지 이동·반복 전송은 한 번, 새 탭·외부 유입·페이지 이동 시 30분 이상 간격은 새 방문입니다.
식별값 없는 기록은 재방문 여부를 알 수 없습니다. 시각은 해당 방문의 현지 시각입니다.</p>
<table class=visit-table><tr><td class=muted>시작 (손님 현지 시각)</td><td class=muted>어디서 · 처음 들어온 주소</td><td class=muted>나라·기기·언어</td><td class=muted>브라우저별 재방문</td><td class=muted>머문 시간</td><td class=muted>한 일</td></tr>{visit_table}</table></section>
<section class='card wide'><h2>최근 의견 (💬 의견 보내기)</h2><table>{fb_rows}</table></section>
</div>
<p class=note>2026-11-07 전 기록은 검색·클릭한 방문만 남아 있습니다. 집계 방식이 다른 <a href="{ANALYTICS_URL}" target=_blank rel=noopener>Vercel Analytics</a> 통계와 숫자가 다를 수 있습니다.
{'<br>⚠️ 기록이 많아 최근 ' + str(MAX_READS) + '건만 읽었습니다.' if cut else ''}</p>
</main></body></html>"""


class handler(BaseHTTPRequestHandler):
    def _send(self, status: int, body: str, extra: dict | None = None) -> None:
        data = body.encode("utf-8")
        self.send_response(status)
        self.send_header("content-type", "text/html; charset=utf-8")
        self.send_header("cache-control", "no-store")
        self.send_header("x-robots-tag", "noindex, nofollow")
        for name, value in (extra or {}).items():
            for one in (value if isinstance(value, list) else [value]):
                self.send_header(name, one)
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):  # noqa: N802
        query = parse_qs(urlparse(self.path).query)
        key = (query.get("key") or [""])[0]
        cookie = SimpleCookie(self.headers.get("cookie") or "")
        cookie_value = cookie[COOKIE].value if COOKIE in cookie else ""
        if not authorized(key, cookie_value):
            return self._send(401, "<!doctype html><meta charset=utf-8><meta name=robots content=noindex><p>권한이 없습니다.</p>")
        if key:  # 키는 쿠키로 옮기고 주소창에서 지움
            return self._send(302, "", {"location": "/owner/usage",
                                        "set-cookie": [f"{COOKIE}={key}; Path=/owner; Max-Age=7776000; HttpOnly; Secure; SameSite=Lax",
                                                       SKIP_USAGE_COOKIE]})
        try:
            days = max(1, min(int((query.get("days") or ["7"])[0]), 30))
        except ValueError:
            days = 7
        date = (query.get("date") or [""])[0]
        try:
            date = dt.date.fromisoformat(date).isoformat() if date else None
        except ValueError:
            date = None
        try:
            entries, feedback, cut = load(days, date)
        except Exception as error:  # noqa: BLE001
            return self._send(500, f"<!doctype html><meta charset=utf-8><p>기록을 읽지 못했습니다: {_esc(type(error).__name__)}</p>")
        return self._send(200, render(entries, feedback, days, cut, date, load_browser_history(entries)), {"set-cookie": SKIP_USAGE_COOKIE})
