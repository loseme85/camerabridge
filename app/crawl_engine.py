"""크롤링 효율 엔진: 사이트별 증분 수집 · 병합 · 변경 기록.

사이트가 늘어나도 한 번 실행하는 비용이 '바뀐 것'에 비례하도록 만든다.
  1) 판매 중 매물이 목록 앞에 오는 사이트(active_first)는 판매 중 구간만 읽고 멈춘다.
     판매완료 기록 전체는 하루 한 번(full sweep)만 다시 읽는다.
  2) 이전 결과와 병합해 바뀐 매물만 갱신하고, 변경은 events 로그에 한 줄씩 남긴다.
  3) 사이트 결과가 평소보다 크게 줄면 그 사이트는 이전 데이터를 유지한다 (일시 누락 방지).
     전체 수집 사이트에서 사라진 매물은 두 번 연속 안 보일 때만 '사라짐'으로 본다.
  4) 행마다 수집 시각을 쓰지 않고, 사이트별 확인 시각을 source_freshness.json 한 곳에 둔다.

새 사이트는 rows(dict 목록)와 coverage("full" | "active_zone")만 돌려주면 이 엔진에 그대로 붙는다.
"""
from __future__ import annotations

import datetime as dt
import json
import os
import re
import time
from concurrent.futures import ThreadPoolExecutor
from typing import Any, Callable

KST = dt.timezone(dt.timedelta(hours=9))
FRESHNESS_PATH = "data/status/source_freshness.json"
HISTORY_DIR = "data/history"

HEALTH_MIN_BASE = 10        # 이전 판매 중이 이보다 적으면 비율 검사 안 함
HEALTH_RATIO = 0.7          # 판매 중(또는 전체)이 이전의 70% 미만이면 '의심' → 이전 데이터 유지
FULL_SWEEP_HOURS = 24       # active_first 사이트의 판매완료 기록 전체 재확인 주기
STOP_AFTER_QUIET_PAGES = 2  # 판매 중 0개 + 전부 아는 매물인 페이지가 연속 이만큼이면 멈춤
MISSING_GRACE_RUNS = 2      # 전체 수집에서 이만큼 연속 안 보여야 '사라짐'
CARRY_FIELDS = ("condition_checked", "image_grade", "image_grade_note", "image_checked")  # 목록 밖에서 채운 값


def now_kst() -> str:
    return dt.datetime.now(KST).strftime("%Y-%m-%d %H:%M:%S")


def _parse_ts(value: str | None) -> dt.datetime | None:
    try:
        return dt.datetime.strptime(value or "", "%Y-%m-%d %H:%M:%S").replace(tzinfo=KST)
    except ValueError:
        return None


def hours_between(start: str | None, end: str | None) -> float | None:
    a, b = _parse_ts(start), _parse_ts(end)
    return round((b - a).total_seconds() / 3600, 1) if a and b else None


# ── 상태 파일 ─────────────────────────────────────────────

def load_freshness(path: str = FRESHNESS_PATH) -> dict[str, dict]:
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except (OSError, ValueError):
        return {}


def save_freshness(data: dict[str, dict], path: str = FRESHNESS_PATH) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(dict(sorted(data.items())), f, ensure_ascii=False, indent=1)
        f.write("\n")


def needs_full_sweep(site: str, freshness: dict[str, dict], now: str, force: bool = False) -> bool:
    if force:
        return True
    hours = hours_between((freshness.get(site) or {}).get("last_full"), now)
    return hours is None or hours >= FULL_SWEEP_HOURS


def append_events(events: list[dict], now: str, history_dir: str = HISTORY_DIR) -> str | None:
    """변경만 월별 jsonl에 한 줄씩 추가 (가격 이력·판매 소요 시간의 원본)."""
    if not events:
        return None
    os.makedirs(history_dir, exist_ok=True)
    path = os.path.join(history_dir, f"events_{now[:7]}.jsonl")
    with open(path, "a", encoding="utf-8") as f:
        for e in events:
            f.write(json.dumps(e, ensure_ascii=False, sort_keys=True) + "\n")
    return path


# ── 병합 ────────────────────────────────────────────────

def _event(kind: str, row: dict, now: str, **extra: Any) -> dict:
    e = {"t": now, "type": kind, "site": row.get("site"), "link": row.get("링크"), "title": row.get("상품명"),
         "price": row.get("가격"), "currency": row.get("통화")}
    e.update({k: v for k, v in extra.items() if v is not None})
    return e


def check_health(prev_rows: list[dict], run: dict) -> str | None:
    """이전보다 크게 줄었으면 이유 문자열, 괜찮으면 None."""
    prev_active = sum(1 for r in prev_rows if not r.get("품절"))
    cur_active = sum(1 for r in run["rows"] if not r.get("품절"))
    if prev_active >= HEALTH_MIN_BASE and cur_active < HEALTH_RATIO * prev_active:
        return f"판매 중 {prev_active} → {cur_active}"
    if run.get("coverage") == "full" and len(prev_rows) >= HEALTH_MIN_BASE and len(run["rows"]) < HEALTH_RATIO * len(prev_rows):
        return f"전체 {len(prev_rows)} → {len(run['rows'])}"
    return None


def merge_source(prev_rows: list[dict], run: dict, now: str) -> tuple[list[dict], list[dict], dict]:
    """한 사이트의 이전 행 + 이번 수집 → (병합 행, 변경 이벤트, 상태).

    run: {"site", "ok", "rows", "coverage": "full"|"active_zone", "error"?, "pages"?, "seconds"?}
    """
    site = run["site"]
    stat = {"site": site, "coverage": run.get("coverage"), "pages": run.get("pages"), "seconds": run.get("seconds")}
    if not run.get("ok"):
        return list(prev_rows), [], {**stat, "status": "failed", "reason": run.get("error") or "수집 실패", "kept": len(prev_rows)}
    reason = check_health(prev_rows, run)
    if reason:
        return list(prev_rows), [], {**stat, "status": "suspect", "reason": reason, "kept": len(prev_rows)}

    prev = {r["링크"]: r for r in prev_rows if r.get("링크")}
    seen: set[str] = set()
    merged: list[dict] = []
    events: list[dict] = []
    for raw in run["rows"]:
        link = raw.get("링크")
        if not link or link in seen:
            continue
        seen.add(link)
        row = dict(raw)
        row.pop("crawl_time", None)
        row.pop("missing_runs", None)
        p = prev.get(link)
        if p is None:
            row["first_seen"] = now
            if row.get("품절"):
                row.setdefault("sold_at", now)  # 처음 볼 때 이미 판매완료 (기록 보관용, 이벤트 없음)
            else:
                events.append(_event("new", row, now))
        else:
            row["first_seen"] = p.get("first_seen") or now
            # 상세 페이지·사진에서 채운 값은 목록에 없으니 이전 값을 이어감
            for key in CARRY_FIELDS:
                if key in p and key not in row:
                    row[key] = p[key]
            if row.get("컨디션") in (None, "", "정보없음") and p.get("컨디션") not in (None, "", "정보없음"):
                row["컨디션"] = p["컨디션"]
            if p.get("가격") != row.get("가격") and row.get("가격"):
                events.append(_event("price", row, now, prev_price=p.get("가격")))
            if not p.get("품절") and row.get("품절"):
                row["sold_at"] = now
                events.append(_event("sold", row, now, first_seen=row["first_seen"], hours_to_sell=hours_between(row["first_seen"], now)))
            elif p.get("품절") and not row.get("품절"):
                row.pop("sold_at", None)
                events.append(_event("relist", row, now))
            elif row.get("품절") and p.get("sold_at"):
                row["sold_at"] = p["sold_at"]
        merged.append(row)

    carried = gone = left = 0
    for link, p in prev.items():
        if link in seen:
            continue
        if run.get("coverage") == "active_zone":
            if p.get("품절"):
                merged.append(p)  # 이번에 안 읽은 판매완료 기록 → 그대로
                carried += 1
            else:
                # 판매 중 구간을 끝까지 읽었는데 없음 → 판매완료(또는 삭제)로 넘어감
                q = dict(p)
                q["품절"] = True
                q["sold_at"] = now
                merged.append(q)
                events.append(_event("sold", q, now, first_seen=q.get("first_seen"), hours_to_sell=hours_between(q.get("first_seen"), now)))
                left += 1
            continue
        misses = int(p.get("missing_runs") or 0) + 1
        if misses < MISSING_GRACE_RUNS:
            q = dict(p)
            q["missing_runs"] = misses
            merged.append(q)  # 한 번 안 보인 건 일시 누락일 수 있어 한 번 더 기다림
            carried += 1
        else:
            if not p.get("품절"):
                events.append(_event("gone", p, now, first_seen=p.get("first_seen"), hours_to_sell=hours_between(p.get("first_seen"), now)))
            gone += 1
    # 사이트가 주는 순서가 실행마다 조금씩 달라도(API 정렬 동점 등) 파일이 안 바뀌게: 기존 매물은 이전 순서, 신규는 맨 앞
    prev_pos = {r.get("링크"): i for i, r in enumerate(prev_rows)}
    merged.sort(key=lambda r: (r.get("링크") in prev_pos, prev_pos.get(r.get("링크"), 0)))
    active = sum(1 for r in merged if not r.get("품절"))
    stat.update({"status": "ok", "rows": len(merged), "active": active, "carried": carried, "gone": gone, "left_active": left,
                 "new": sum(1 for e in events if e["type"] == "new"), "changed": len(events)})
    return merged, events, stat


def update_freshness(freshness: dict[str, dict], stat: dict, now: str) -> None:
    entry = dict(freshness.get(stat["site"]) or {})
    entry.update({k: stat.get(k) for k in ("status", "coverage", "pages", "seconds", "rows", "active", "reason") if stat.get(k) is not None})
    if stat.get("status") != "suspect" and stat.get("status") != "failed":
        entry.pop("reason", None)
        entry["last_success"] = now
        if stat.get("coverage") == "full":
            entry["last_full"] = now
    entry["last_attempt"] = now
    freshness[stat["site"]] = entry


# ── HTTP: 해외(GitHub 미국 서버) 접속을 막는 사이트는 중계 서버로 ─────────────

BROWSER_UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
              "(KHTML, like Gecko) Chrome/124.0 Safari/537.36")


def http_get(url: str, headers: dict | None = None, via_relay: bool = False, timeout: int = 30):
    """via_relay=True이고 RELAY_URL·RELAY_KEY가 있으면 Vercel 도쿄 중계 서버(relay/)를 거쳐 받는다.
    로컬처럼 중계 설정이 없으면 직접 받는다."""
    import requests

    headers = {"User-Agent": BROWSER_UA, **(headers or {})}
    relay_url, relay_key = os.environ.get("RELAY_URL"), os.environ.get("RELAY_KEY")
    if via_relay and relay_url and relay_key:
        return requests.get(relay_url, params={"url": url}, timeout=timeout + 10,
                            headers={"x-relay-key": relay_key, "x-relay-headers": json.dumps(headers)})
    return requests.get(url, headers=headers, timeout=timeout)


# ── 수집기: cafe24 (HTTP, 브라우저 없이) ──────────────────────

CAFE24_SOLD_MARKERS = {
    "사진집": lambda html: "pdi_sold.png" in html or "품절" in html,
    "장씨카메라": lambda html: 'alt="품절"' in html or "icon_202505071559330700.gif" in html or "soldout" in html.lower(),
    "라이카스토어 충무로": lambda html: "icon_202209171535309800.gif" in html or "SOLD OUT" in html or "품절" in html,
}


def parse_cafe24_cards(html: str, site: dict, keep: Callable[[str], bool], fix_img: Callable[[str, str], str],
                       normalize_price: Callable[[str], str]) -> list[dict]:
    """목록 페이지 HTML → 카드 목록. 각 카드: {"active": bool, "row": dict | None(걸러진 카드)}"""
    from bs4 import BeautifulSoup

    base = site["base"]
    sold_marker = CAFE24_SOLD_MARKERS.get(site["name"], lambda h: "품절" in h or "soldout" in h.lower())
    cards = []
    for card in BeautifulSoup(html, "html.parser").select("ul.prdList > li"):
        name_el = card.select_one(".name")
        if not name_el:
            continue
        name = " ".join(name_el.get_text(" ", strip=True).split())
        name = re.sub(r"^상품명\s*:\s*", "", name)  # 화면에서 숨겨진 '상품명 :' 라벨
        if not name:
            continue
        card_html = str(card)
        is_soldout = sold_marker(card_html)
        is_reserved = "예약중" in card_html if site["name"] != "사진집" else False
        if not keep(name):
            cards.append({"active": not is_soldout, "row": None})
            continue
        link_el = card.select_one("a")
        href = (link_el.get("href") or "") if link_el else ""
        if href and not href.startswith("http"):
            href = base + href
        href = href.split("#")[0]
        card_text = card.get_text(" ", strip=True)
        price_match = re.search(r"([\d,]+원)", card_text)
        price = normalize_price(price_match.group(1) if price_match else "문의요망")
        img_url = ""
        for img in card.select("img"):
            raw = img.get("src") or ""
            if "web/product/" in raw or "upload/product/" in raw:
                img_url = fix_img(raw, base)
                break
        if not img_url:
            img = card.select_one("img")
            if img:
                raw = img.get("data-src") or img.get("data-original") or ""
                if raw and "img_product_big.gif" not in raw:
                    img_url = fix_img(raw, base)
        cond = re.search(r"(\d{2,3})%", card_text) or re.search(r"(\d{2,3})%", name)
        cards.append({"active": not is_soldout, "row": {
            "site": site["name"], "상품명": name, "컨디션": cond.group(1) + "%" if cond else "정보없음", "가격": price,
            "통화": site["통화"], "이미지": img_url, "링크": href, "품절": is_soldout, "예약중": is_reserved,
        }})
    return cards


def _page_url(cat_url: str, page: int) -> str:
    return cat_url + (f"&page={page}" if "?" in cat_url else f"?page={page}")


def crawl_cafe24_http(site: dict, known_links: set[str], full: bool, keep: Callable[[str], bool],
                      fix_img: Callable[[str, str], str], normalize_price: Callable[[str], str],
                      session=None, workers: int = 3, max_pages: int = 400) -> dict:
    """cafe24 목록을 HTTP로 읽는다. active_first 사이트는 full=False면 판매 중 구간까지만.

    한 페이지라도 못 읽으면 ok=False (병합 단계에서 이전 데이터 유지).
    """
    import requests

    started = time.time()
    sess = session or requests.Session()
    if "python-requests" in str(sess.headers.get("User-Agent", "python-requests")):  # 기본 UA는 막는 사이트가 있음
        sess.headers["User-Agent"] = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
                                      "(KHTML, like Gecko) Chrome/124.0 Safari/537.36")
    incremental = bool(site.get("active_first")) and not full
    rows: list[dict] = []
    pages_read = 0

    def fetch(url: str) -> str:
        last = None
        for attempt in range(3):
            try:
                resp = sess.get(url, timeout=30)
                resp.raise_for_status()
                return resp.text
            except Exception as e:  # noqa: BLE001
                last = e
                time.sleep(1.5 * (attempt + 1))
        raise RuntimeError(f"{url}: {last}")

    try:
        for cat_url in site["categories"]:
            page, quiet, done = 1, 0, False
            while not done and page <= max_pages:
                batch = list(range(page, min(page + workers, max_pages + 1)))
                with ThreadPoolExecutor(len(batch)) as ex:
                    htmls = list(ex.map(lambda n: fetch(_page_url(cat_url, n)), batch))
                for html in htmls:
                    cards = parse_cafe24_cards(html, site, keep, fix_img, normalize_price)
                    if not cards:
                        done = True  # 마지막 페이지 지남
                        break
                    pages_read += 1
                    page_rows = [c["row"] for c in cards if c["row"]]
                    rows.extend(page_rows)
                    if incremental:
                        no_active = not any(c["active"] for c in cards)
                        all_known = all(r["링크"] in known_links for r in page_rows)
                        quiet = quiet + 1 if (no_active and all_known) else 0
                        if quiet >= STOP_AFTER_QUIET_PAGES:
                            done = True
                            break
                page += len(batch)
                time.sleep(0.3)
    except Exception as e:  # noqa: BLE001
        return {"site": site["name"], "ok": False, "rows": rows, "coverage": "full" if not incremental else "active_zone",
                "error": str(e)[:200], "pages": pages_read, "seconds": round(time.time() - started, 1)}
    return {"site": site["name"], "ok": pages_read > 0, "rows": rows, "coverage": "active_zone" if incremental else "full",
            "error": None if pages_read else "목록이 비어 있음", "pages": pages_read, "seconds": round(time.time() - started, 1)}


def wrap_full_run(site_name: str, collect: Callable[[], list[dict]]) -> dict:
    """기존 수집 함수(전체 목록을 돌려주는 것)를 엔진 형식으로."""
    started = time.time()
    try:
        rows = collect() or []
        return {"site": site_name, "ok": bool(rows), "rows": rows, "coverage": "full",
                "error": None if rows else "0건", "seconds": round(time.time() - started, 1)}
    except Exception as e:  # noqa: BLE001
        return {"site": site_name, "ok": False, "rows": [], "coverage": "full", "error": str(e)[:200],
                "seconds": round(time.time() - started, 1)}


# ── 상세 페이지에서 컨디션 채우기 (목록에 없고 상세에만 있는 사이트) ──────────────

def enrich_detail_condition(rows: list[dict], site: str, pattern: str, now: str, cap: int = 400, workers: int = 4,
                            session=None) -> int:
    """'컨디션'이 비어 있는 매물의 상세 페이지를 읽어 채운다. 판매 중 먼저, 한 번 읽은 매물은 다시 안 읽음.
    판매완료 기록은 실행마다 cap개씩 나눠서 채운다 (예: 장씨카메라 4천 건 → 하루 이틀)."""
    import requests

    todo = [r for r in rows if r.get("site") == site and (r.get("컨디션") in (None, "", "정보없음"))
            and not r.get("condition_checked")]
    todo.sort(key=lambda r: bool(r.get("품절")))
    todo = todo[:cap]
    if not todo:
        return 0
    sess = session or requests.Session()
    sess.headers["User-Agent"] = BROWSER_UA
    rx = re.compile(pattern)

    def one(row):
        try:
            html = sess.get(row["링크"], timeout=20).text
            m = rx.search(re.sub(r"<[^>]+>", " ", html))
            return row, (m.group(1) + "%") if m else None
        except Exception:  # noqa: BLE001
            return row, None

    filled = 0
    with ThreadPoolExecutor(workers) as ex:
        for row, cond in ex.map(one, todo):
            row["condition_checked"] = now[:10]
            if cond:
                row["컨디션"] = cond
                filled += 1
    return filled
