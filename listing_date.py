"""게시 추정일: 매물 사진 주소에 남은 올린 날짜로 '언제쯤 게시됐는지' 어림한다.

판매일을 모르는 판매완료 기록(처음 볼 때 이미 팔림 — 국내 매장의 예전 판매 기록 등)이 '언제쯤 팔린 값'인지 가늠하는 데 쓴다.
팔린 날은 게시일과 같거나 그 뒤 (우리가 본 판매는 게시 후 중간값 4.5일).

- cafe24: /web/product/big/202412/… → 2024-12
- WordPress: /wp-content/uploads/2026/06/… → 2026-06
- Shopify 등 파일 버전: ?v=1783637860 · ?1730109430 (유닉스 시각) → 그날
- Drupal 등: /public/2025-11/… → 2025-11, Lecuit: /260915-occ-… → 2026-09-15
"""
from __future__ import annotations

import datetime as dt
import re

_YM_PATH = re.compile(r"/(?:web/)?product/(?:big|medium|small|tiny|extra/\w+)/(20\d{2})(0[1-9]|1[0-2])/")
_WP = re.compile(r"/uploads/(20\d{2})/(0[1-9]|1[0-2])/")
_YM_DASH = re.compile(r"/(20\d{2})-(0[1-9]|1[0-2])/")
_UNIX = re.compile(r"[?&](?:v=)?(1[5-9]\d{8})(?:\b|$)")
_YYMMDD = re.compile(r"/(2[0-9])(0[1-9]|1[0-2])(0[1-9]|[12]\d|3[01])-occ-")


def estimate_listed(image_url: str | None, now: dt.date | None = None) -> tuple[str | None, str | None]:
    """사진 주소 → ('2024-12', 'month') · ('2026-10-15', 'day') · (None, None). 오늘보다 뒤인 날짜는 버린다."""
    url = image_url or ""
    today = now or dt.date.today()
    m = _YM_PATH.search(url) or _WP.search(url) or _YM_DASH.search(url)
    if m:
        y, mo = int(m.group(1)), int(m.group(2))
        if (y, mo) <= (today.year, today.month) and y >= 2005:
            return f"{y:04d}-{mo:02d}", "month"
        return None, None
    m = _YYMMDD.search(url)
    if m:
        try:
            day = dt.date(2000 + int(m.group(1)), int(m.group(2)), int(m.group(3)))
        except ValueError:
            return None, None
        return (day.isoformat(), "day") if day <= today else (None, None)
    m = _UNIX.search(url)
    if m:
        day = dt.datetime.fromtimestamp(int(m.group(1)), dt.timezone(dt.timedelta(hours=9))).date()
        return (day.isoformat(), "day") if dt.date(2015, 1, 1) <= day <= today else (None, None)
    return None, None


def as_datetime_text(listed: str | None) -> str | None:
    """'2024-12' → '2024-12-15 00:00:00' (그 달 가운데), '2026-10-15' → '2026-10-15 00:00:00'"""
    if not listed:
        return None
    return (listed + "-15" if len(listed) == 7 else listed) + " 00:00:00"
