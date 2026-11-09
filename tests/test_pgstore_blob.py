"""pgstore.PgBlob: Blob과 같은 모양(iter_objects·get·put·delete, .pathname·.url)으로 Neon 표에 저장 (2026-11-08)"""
import pgstore


def test_pgblob_roundtrip(monkeypatch):
    store: dict[str, str] = {}

    def fake_sql(query, params=None, timeout=8.0):
        params = params or []
        if query.startswith("CREATE"):
            return []
        if query.startswith("INSERT INTO blob_docs"):
            store[params[0]] = params[1]
            return []
        if query.startswith("SELECT path FROM blob_docs"):
            return [{"path": p} for p in sorted(store) if p.startswith(params[0])]
        if query.startswith("SELECT body FROM blob_docs"):
            return [{"body": store[params[0]]}] if params[0] in store else []
        if query.startswith("DELETE FROM blob_docs"):
            for p in params[0]:
                store.pop(p, None)
            return []
        raise AssertionError(query)

    monkeypatch.setattr(pgstore, "sql", fake_sql)
    monkeypatch.setattr(pgstore, "_SCHEMA_READY", False)
    b = pgstore.PgBlob()
    b.put("board/posts/1.json", b'{"a": 1}', access="private", content_type="application/json", overwrite=True)
    b.put("board/posts/2.json", '{"a": 2}')
    b.put("board/members/x.json", "{}")
    items = b.iter_objects(prefix="board/posts/")
    assert [i.pathname for i in items] == ["board/posts/1.json", "board/posts/2.json"] and items[0].url == items[0].pathname
    assert b.get(items[0].url, access="private", use_cache=False).content == b'{"a": 1}'
    b.delete(items[0].url)
    b.delete([items[1]])
    assert b.iter_objects(prefix="board/posts/") == []
    try:
        b.get("board/posts/1.json")
        raise AssertionError("없는 파일은 예외")
    except FileNotFoundError:
        pass
