"""사장님 전용 방문 현황 화면: /owner/usage

사용 기록(api/usage.py 가 쌓은 Blob usage/)과 의견(feedback/)을 읽어 한 화면에 보여 준다.
들어가기: /owner/usage?key=<OWNER_DASHBOARD_KEY> 로 한 번 열면 쿠키가 남아 다음부터는 /owner/usage 만으로 열림.
기간: ?days=1 · 7(기본) · 30
전체 방문 수(검색 안 한 사람 포함)는 Vercel Analytics 에서 본다.
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

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from scripts.usage_report import summarize  # noqa: E402

KST = dt.timezone(dt.timedelta(hours=9))
COOKIE = "cb_owner"
ANALYTICS_URL = "https://vercel.com/camerabridge/camerabridge/analytics"
REFERRER_NAMES = {"www.reddit.com": "레딧", "old.reddit.com": "레딧", "reddit.com": "레딧", "out.reddit.com": "레딧",
                  "www.google.com": "구글", "com.reddit.frontpage": "레딧 앱", "t.co": "X(트위터)"}
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


def load(days: int) -> tuple[list[dict], list[dict], bool]:
    from vercel import blob  # noqa: WPS433

    start = (dt.datetime.now(KST).date() - dt.timedelta(days=days - 1)).isoformat()
    usage_items = [i for i in blob.iter_objects(prefix="usage/") if i.pathname.split("/")[1] >= start]
    usage_items.sort(key=lambda i: i.pathname, reverse=True)
    cut = len(usage_items) > MAX_READS
    feedback_items = sorted(blob.iter_objects(prefix="feedback/"), key=lambda i: i.pathname, reverse=True)[:20]
    return _read_many(blob, usage_items[:MAX_READS]), _read_many(blob, feedback_items), cut


def _ref_name(host: str | None) -> str:
    if not host:
        return "직접·앱 (레딧 앱도 여기로 잡힘)"
    return REFERRER_NAMES.get(host, host)


def visits(entries: list[dict]) -> list[dict]:
    """방문(세션)별로 묶어 최신순."""
    grouped: dict[str, dict] = {}
    for e in sorted(entries, key=lambda e: (e["sid"], e.get("part", 1))):
        v = grouped.setdefault(e["sid"], {"start": e.get("created_at", ""), "end": e.get("created_at", ""), "referrer": e.get("referrer"),
                                          "locale": e.get("locale"), "currency": e.get("currency"), "mobile": e.get("mobile"),
                                          "duration_s": 0, "steps": []})
        v["start"] = min(v["start"], e.get("created_at", "")) or v["start"]
        v["end"] = max(v["end"], e.get("created_at", ""))
        v["duration_s"] = max(v["duration_s"], e.get("duration_s") or 0)
        v["steps"] += [("검색", s) for s in e.get("searches", [])] + [("클릭", c) for c in e.get("clicks", [])]
    for v in grouped.values():
        v["steps"].sort(key=lambda step: step[1].get("s") or 0)
    return sorted(grouped.values(), key=lambda v: v["end"], reverse=True)


def _esc(value) -> str:
    return html.escape(str(value if value is not None else ""))


def _table(title: str, rows, empty="없음", note="") -> str:
    body = "".join(f"<tr><td>{_esc(name)}</td><td class=n>{_esc(count)}</td></tr>" for name, count in rows) or f"<tr><td class=muted>{empty}</td><td></td></tr>"
    return f"<section class=card><h2>{_esc(title)}</h2>{f'<p class=muted>{note}</p>' if note else ''}<table>{body}</table></section>"


def _bars(entries: list[dict], days: int) -> str:
    today = dt.datetime.now(KST).date()
    per_day = collections.defaultdict(set)
    for e in entries:
        per_day[str(e.get("created_at", ""))[:10]].add(e["sid"])
    labels = [str(today - dt.timedelta(days=i)) for i in range(days - 1, -1, -1)]
    if days == 1:  # 오늘은 시간별
        per_hour = collections.defaultdict(set)
        for e in entries:
            per_hour[str(e.get("created_at", ""))[11:13]].add(e["sid"])
        labels, counts = [f"{h:02d}" for h in range(24)], [len(per_hour[f"{h:02d}"]) for h in range(24)]
    else:
        counts = [len(per_day[d]) for d in labels]
    top = max(counts + [1])
    bars = "".join(f"<div class=bar title='{_esc(l)}: {c}'><span style='height:{round(c / top * 100)}%'></span><b>{c or ''}</b><i>{_esc(l[-5:] if days > 1 else l + '시')}</i></div>"
                   for l, c in zip(labels, counts))
    return f"<section class='card wide'><h2>{'오늘 시간별' if days == 1 else '날짜별'} 검색한 방문</h2><div class=bars>{bars}</div></section>"


def render(entries: list[dict], feedback: list[dict], days: int, cut: bool) -> str:
    r = summarize(entries)
    ref_counts = collections.Counter(_ref_name(e.get("referrer")) for e in {e["sid"]: e for e in sorted(entries, key=lambda e: -e.get("part", 1))}.values())
    pct = lambda x: "-" if x is None else f"{round(x * 100)}%"  # noqa: E731
    now = dt.datetime.now(KST).strftime("%Y-%m-%d %H:%M")
    tabs = "".join(f"<a class='{'on' if d == days else ''}' href='?days={d}'>{label}</a>" for d, label in ((1, "오늘"), (7, "7일"), (30, "30일")))

    rows = []
    for v in visits(entries)[:60]:
        steps = []
        for kind, s in v["steps"]:
            if kind == "검색":
                tail = "결과 없음" if s.get("results") == 0 else f"판매 중 {s.get('active', 0)} / 전체 {s.get('results', 0)}"
                steps.append(f"<span class=step>🔎 {_esc(s.get('q'))} <small>{tail}</small></span>")
            else:
                steps.append(f"<span class='step click'>↗ {_esc(s.get('host'))}</span>")
        when = str(v["start"])[5:16].replace("T", " ")
        device = "📱" if v["mobile"] else "💻"
        rows.append(f"<tr><td class=nowrap>{_esc(when)}</td><td>{_esc(_ref_name(v['referrer']))}</td><td class=nowrap>{device} {_esc(v['locale'] or '-')} · {_esc(v['currency'] or '')}</td>"
                    f"<td class=nowrap>{_esc(v['duration_s'] // 60)}분 {_esc(v['duration_s'] % 60)}초</td><td>{''.join(steps)}</td></tr>")
    visit_table = "".join(rows) or "<tr><td colspan=5 class=muted>이 기간에 검색한 방문이 없습니다</td></tr>"

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
.step{{display:inline-block;background:var(--soft);border-radius:8px;padding:2px 8px;margin:2px 4px 2px 0}}.step.click{{background:var(--accent);color:#fff}}
.bars{{display:flex;gap:4px;align-items:flex-end;height:130px}}.bar{{flex:1;display:flex;flex-direction:column;justify-content:flex-end;align-items:center;height:100%;min-width:0}}
.bar span{{display:block;width:100%;background:var(--accent);border-radius:4px 4px 0 0;min-height:1px}}.bar b{{font-size:11px;order:-1}}.bar i{{font-size:10px;color:var(--muted);font-style:normal;white-space:nowrap}}
.note{{background:var(--soft);border-radius:10px;padding:10px 12px;margin-top:12px;font-size:13px}}a{{color:var(--accent)}}
@media (max-width:760px){{.kpis{{grid-template-columns:repeat(2,1fr)}}.grid{{grid-template-columns:1fr}}td{{font-size:13px}}}}
</style></head><body><main>
<header><div><h1>방문 현황</h1><span class=muted>{now} 기준 · 검색하거나 판매처를 누른 방문만</span></div><nav class=tabs>{tabs}</nav></header>
<div class=kpis>
<div class=kpi><b>{r['visits_with_activity']}</b><span>검색한 방문</span></div>
<div class=kpi><b>{r['visits_with_click']}</b><span>판매처까지 간 방문</span></div>
<div class=kpi><b>{r['searches']}</b><span>검색 수</span></div>
<div class=kpi><b>{pct(r['mobile_share'])}</b><span>휴대폰</span></div></div>
<div class=grid>
{_bars(entries, days)}
{_table('어디서 왔나', ref_counts.most_common(10), note='휴대폰 앱(레딧 앱 등)은 출처를 안 알려 줘서 "직접·앱"으로 잡힘')}
{_table('화면 언어', r['locales'])}
{_table('클릭한 판매처', r['click_hosts'])}
{_table('많이 찾은 검색어', r['top_queries'][:10])}
{_table('결과 0건 검색어 (고칠 것)', r['zero_result_queries'][:10])}
{_table('판매 중 0건 검색어', r['no_active_queries'][:10])}
<section class='card wide'><h2>최근 방문 (한 줄 = 한 사람의 방문 흐름)</h2>
<table><tr><td class=muted>시작(한국)</td><td class=muted>어디서</td><td class=muted>기기·언어</td><td class=muted>머문 시간</td><td class=muted>한 일</td></tr>{visit_table}</table></section>
<section class='card wide'><h2>최근 의견 (💬 의견 보내기)</h2><table>{fb_rows}</table></section>
</div>
<p class=note>검색 없이 둘러보기만 한 사람까지 포함한 <b>전체 방문 수·나라</b>는 <a href="{ANALYTICS_URL}" target=_blank rel=noopener>Vercel Analytics</a>에서 봅니다.
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
            self.send_header(name, value)
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
                                        "set-cookie": f"{COOKIE}={key}; Path=/owner; Max-Age=7776000; HttpOnly; Secure; SameSite=Lax"})
        try:
            days = max(1, min(int((query.get("days") or ["7"])[0]), 30))
        except ValueError:
            days = 7
        try:
            entries, feedback, cut = load(days)
        except Exception as error:  # noqa: BLE001
            return self._send(500, f"<!doctype html><meta charset=utf-8><p>기록을 읽지 못했습니다: {_esc(type(error).__name__)}</p>")
        return self._send(200, render(entries, feedback, days, cut))
