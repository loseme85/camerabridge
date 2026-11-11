"""방문 기록·의견을 Neon Postgres에 쌓는다 (Vercel Blob 무료 한도를 2026-11에 넘어 쓰기·읽기가 막힘).

드라이버 없이 Neon HTTP SQL 엔드포인트(POST https://<호스트>/sql)를 쓴다 — 함수 묶음 크기가 늘지 않음.
연결 주소는 Vercel이 Neon을 프로젝트에 연결할 때 넣어 주는 환경 변수(DATABASE_URL, 없으면 POSTGRES_URL).
주소가 없으면 enabled()가 False → 부르는 쪽이 예전처럼 Blob을 씀.

표
  usage_events(id, created_at, day, entry jsonb)   — api/usage.py 가 방문 묶음마다 한 줄
  feedback_events(id, created_at, day, tag, entry jsonb) — api/feedback.py 의견 한 건마다 한 줄
  blob_docs(path PK, body, updated_at)             — 게시판·회원·저장 목록·가격 알림·딜러 계정 (예전 Blob 파일 한 개 = 한 줄, 2026-11-08)
"""
from __future__ import annotations

import json
import os
import urllib.parse
import urllib.request

_SCHEMA_READY = False
SCHEMA = [
    "CREATE TABLE IF NOT EXISTS usage_events (id bigserial PRIMARY KEY, created_at timestamptz NOT NULL DEFAULT now(),"
    " day date NOT NULL, entry jsonb NOT NULL)",
    "CREATE INDEX IF NOT EXISTS usage_events_day ON usage_events (day)",
    "CREATE INDEX IF NOT EXISTS usage_events_browser ON usage_events ((entry->>'vid')) WHERE entry->>'vid' IS NOT NULL",
    "CREATE TABLE IF NOT EXISTS feedback_events (id bigserial PRIMARY KEY, created_at timestamptz NOT NULL DEFAULT now(),"
    " day date NOT NULL, tag text, entry jsonb NOT NULL)",
    "CREATE INDEX IF NOT EXISTS feedback_events_day ON feedback_events (day)",
    "CREATE TABLE IF NOT EXISTS blob_docs (path text PRIMARY KEY, body text NOT NULL, updated_at timestamptz NOT NULL DEFAULT now())",
]


def url() -> str:
    return os.environ.get("DATABASE_URL") or os.environ.get("POSTGRES_URL") or ""


def enabled() -> bool:
    return url().startswith(("postgres://", "postgresql://"))


def sql(query: str, params: list | None = None, timeout: float = 8.0) -> list[dict]:
    """한 문장 실행 → 행 목록(dict). 실패하면 예외 (부르는 쪽이 잡음)"""
    conn = url()
    host = urllib.parse.urlparse(conn).hostname
    body = json.dumps({"query": query, "params": params or []}).encode("utf-8")
    req = urllib.request.Request(f"https://{host}/sql", data=body, method="POST", headers={
        "Content-Type": "application/json", "Neon-Connection-String": conn})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        data = json.loads(resp.read() or b"{}")
    return list(data.get("rows") or [])


def ensure_schema() -> None:
    """함수가 처음 뜰 때 한 번 표를 만든다 (이미 있으면 아무것도 안 함)"""
    global _SCHEMA_READY
    if _SCHEMA_READY:
        return
    for statement in SCHEMA:
        sql(statement)
    _SCHEMA_READY = True


def _entry(row: dict) -> dict:
    value = row.get("entry")
    return json.loads(value) if isinstance(value, str) else (value or {})


def add_usage(entry: dict) -> None:
    ensure_schema()
    sql("INSERT INTO usage_events (day, entry) VALUES ($1::date, $2::jsonb)",
        [str(entry.get("created_at", ""))[:10], json.dumps(entry, ensure_ascii=False)])


def usage_since(start_day: str, end_day: str | None = None, limit: int = 5000) -> list[dict]:
    """start_day(포함)부터 end_day(포함, 없으면 끝까지)의 방문 묶음, 최신 먼저"""
    ensure_schema()
    if end_day:
        rows = sql("SELECT entry FROM usage_events WHERE day >= $1::date AND day <= $2::date ORDER BY id DESC LIMIT $3",
                   [start_day, end_day, limit])
    else:
        rows = sql("SELECT entry FROM usage_events WHERE day >= $1::date ORDER BY id DESC LIMIT $2", [start_day, limit])
    return [_entry(r) for r in rows]


def browser_history(browser_ids: list[str]) -> dict[str, dict]:
    """표시할 브라우저의 보유 기록 전체(최근 365일). 화면 기간·5,000건 상한과 무관.

    같은 방문의 여러 전송·재전송·페이지 이동은 sid 하나로 센다.
    별도 누적 표를 만들지 않아 기존 기록 삭제 시 이 집계에서도 함께 빠진다.
    """
    if not browser_ids:
        return {}
    ensure_schema()
    rows = sql(
        "SELECT entry->>'vid' AS vid, COUNT(DISTINCT entry->>'sid') AS visits, "
        "MIN(entry->>'created_at') AS first_seen, MAX(entry->>'created_at') AS last_seen "
        "FROM usage_events WHERE entry->>'vid' = ANY($1::text[]) "
        "AND day >= ((now() AT TIME ZONE 'Asia/Seoul')::date - 364) "
        "GROUP BY entry->>'vid'", [sorted(set(browser_ids))])
    return {row["vid"]: {"visits": int(row["visits"]), "first_seen": row["first_seen"],
                         "last_seen": row["last_seen"]} for row in rows}


def add_feedback(entry: dict, tag: str) -> None:
    ensure_schema()
    sql("INSERT INTO feedback_events (day, tag, entry) VALUES ($1::date, $2, $3::jsonb)",
        [str(entry.get("created_at", ""))[:10], tag, json.dumps(entry, ensure_ascii=False)])


def feedback_count_today(day: str, tag: str) -> int:
    ensure_schema()
    rows = sql("SELECT count(*) AS n FROM feedback_events WHERE day = $1::date AND tag = $2", [day, tag])
    return int((rows[0] if rows else {}).get("n") or 0)


def recent_feedback(limit: int = 20) -> list[dict]:
    ensure_schema()
    return [_entry(r) for r in sql("SELECT entry FROM feedback_events ORDER BY id DESC LIMIT $1", [limit])]


def delete_older_than(days: int = 365) -> None:
    """개인정보처리방침 보유 기간(1년): 그보다 오래된 방문 기록·의견 지우기"""
    ensure_schema()
    sql("DELETE FROM usage_events WHERE day < (now() - ($1 || ' days')::interval)::date", [str(days)])
    sql("DELETE FROM feedback_events WHERE day < (now() - ($1 || ' days')::interval)::date", [str(days)])


# ── Blob과 같은 모양의 저장소 (2026-11-08) ─────────────────────────────────────
# api/board.py·dealer_portal.py는 vercel.blob의 iter_objects·get·put·delete와 목록 항목의 .pathname·.url만 쓴다.
# 같은 이름의 함수를 Neon 표(blob_docs) 위에 두어 코드를 거의 그대로 두고 저장소만 바꾼다. url = pathname.
class _Item:
    __slots__ = ("pathname", "url")

    def __init__(self, pathname: str):
        self.pathname = pathname
        self.url = pathname


class _Content:
    __slots__ = ("content",)

    def __init__(self, content: bytes):
        self.content = content


class PgBlob:
    def iter_objects(self, prefix: str = "", **_kw):
        ensure_schema()
        rows = sql("SELECT path FROM blob_docs WHERE left(path, length($1)) = $1 ORDER BY path", [prefix])
        return [_Item(r["path"]) for r in rows]

    def get(self, url_or_path, **_kw) -> _Content:
        ensure_schema()
        path = getattr(url_or_path, "pathname", url_or_path)
        rows = sql("SELECT body FROM blob_docs WHERE path = $1", [path])
        if not rows:
            raise FileNotFoundError(path)
        return _Content(str(rows[0]["body"]).encode("utf-8"))

    def put(self, path: str, data, **_kw) -> _Item:
        ensure_schema()
        body = data.decode("utf-8") if isinstance(data, (bytes, bytearray)) else str(data)
        sql("INSERT INTO blob_docs (path, body, updated_at) VALUES ($1, $2, now()) "
            "ON CONFLICT (path) DO UPDATE SET body = EXCLUDED.body, updated_at = now()", [path, body])
        return _Item(path)

    def delete(self, url_or_list, **_kw) -> None:
        ensure_schema()
        items = url_or_list if isinstance(url_or_list, (list, tuple)) else [url_or_list]
        paths = [getattr(x, "pathname", x) for x in items]
        if paths:
            sql("DELETE FROM blob_docs WHERE path = ANY($1::text[])", [paths])


def blob_store():
    """Neon이 연결돼 있으면 Neon 저장소, 아니면 예전 Vercel Blob"""
    if enabled():
        return PgBlob()
    from vercel import blob  # noqa: WPS433
    return blob
