import importlib.util
import json
import sys
import types
from pathlib import Path

_spec = importlib.util.spec_from_file_location("board_api", Path(__file__).resolve().parents[1] / "api" / "board.py")
board = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(board)


class FakeBlob:
    def __init__(self):
        self.store = {}

    def iter_objects(self, prefix=None, **_):
        return [types.SimpleNamespace(pathname=k, url=k) for k in sorted(self.store) if k.startswith(prefix or "")]

    def get(self, url, access="public", use_cache=True):
        assert access == "private"
        return types.SimpleNamespace(content=json.dumps(self.store[url]).encode())

    def put(self, path, body, access="public", content_type=None, overwrite=False):
        assert access == "private"
        self.store[path] = json.loads(body)

    def delete(self, urls):
        for url in [urls] if isinstance(urls, str) else urls:
            self.store.pop(url, None)


def _setup(monkeypatch):
    fake = FakeBlob()
    vercel_mod = types.ModuleType("vercel")
    vercel_mod.blob = fake
    monkeypatch.setitem(sys.modules, "vercel", vercel_mod)
    sent = []
    monkeypatch.setattr(board, "_notify", lambda text: sent.append(text))
    monkeypatch.setenv("DEALER_SESSION_SECRET", "s" * 40)
    monkeypatch.setenv("GOOGLE_CLIENT_ID", "cid.apps.googleusercontent.com")
    monkeypatch.setattr(board, "verify_google", lambda credential: {"tok-a": "sub-a", "tok-b": "sub-b"}.get(credential))
    return fake, sent


def _join(credential: str, nick: str) -> str:
    """구글 로그인 → 쿠키에서 회원 id → 닉네임 정하기."""
    status, out, session = board.login({"credential": credential})
    assert status == 200
    member_id = board.member_from_cookie(session)
    assert board.set_nick({"nick": nick}, member_id)[0] == 200
    return member_id


def _ip(n: int) -> dict:
    return {"x-forwarded-for": f"203.0.113.{n}"}


POST = {"action": "post", "category": "question", "title": "M6 셔터 소리", "body": "M6 셔터 소리가 원래 이런가요?", "elapsed_ms": 5000, "locale": "ko"}


def test_google_member_posts_and_comments_without_password(monkeypatch):
    fake, sent = _setup(monkeypatch)
    a = _join("tok-a", "필름러")
    b = _join("tok-b", "라이카")
    status, out = board.create_post(POST, a)
    assert status == 200
    post_id = out["id"]
    assert board.create_comment({"post_id": post_id, "body": "네 원래 그래요", "elapsed_ms": 4000, "locale": "en"}, b)[0] == 200
    listed = board.list_posts()
    assert listed["total"] == 1 and listed["posts"][0]["comments"] == 1 and listed["posts"][0]["nick"] == "필름러"
    status, read = board.read_post(post_id, a)
    assert read["post"].get("mine") is True and "mine" not in read["comments"][0]
    assert read["post"]["locale"] == "ko" and read["comments"][0]["locale"] == "en"  # 번역 보기를 띄울지 정하는 데 씀
    dump = json.dumps(read, ensure_ascii=False) + json.dumps(listed, ensure_ascii=False)
    assert a not in dump and "sub-a" not in dump  # 회원 id·구글 번호는 밖으로 안 나감
    assert "sub-a" not in json.dumps(fake.store)  # 구글 번호 자체는 저장 안 함 (해시만)
    assert len(sent) == 1


def test_login_needed_and_nick_needed(monkeypatch):
    _setup(monkeypatch)
    assert board.create_post(POST, None) == (401, {"ok": False, "error": "login"})
    assert board.login({"credential": "forged"})[0] == 401
    status, out, session = board.login({"credential": "tok-a"})
    member_id = board.member_from_cookie(session)
    assert out["member"]["nick"] is None
    assert board.create_post(POST, member_id)[1]["error"] == "nick"  # 닉네임 먼저
    assert board.set_nick({"nick": ""}, member_id)[0] == 400
    assert board.me(member_id)["member"] == {"nick": None, "alerts": False, "alerts_email": ""} and board.me(None)["client_id"] == "cid.apps.googleusercontent.com"


def test_session_cookie_is_signed_and_expires(monkeypatch):
    _setup(monkeypatch)
    value = board.session_value("a" * 20, now=1_000)
    assert board.member_from_cookie(value, now=2_000) == "a" * 20
    assert board.member_from_cookie(value, now=1_000 + 91 * 86400) is None  # 90일 뒤 만료
    assert board.member_from_cookie(value.replace("a" * 20, "b" * 20), now=2_000) is None  # 서명 위조
    monkeypatch.delenv("DEALER_SESSION_SECRET")
    assert board.member_from_cookie(value, now=2_000) is None and board.login({"credential": "tok-a"})[0] == 503


def test_bad_input_and_daily_limit(monkeypatch):
    fake, _ = _setup(monkeypatch)
    a = _join("tok-a", "필름러")
    assert board.create_post({**POST, "website": "spam"}, a) == (200, {"ok": True})
    assert board.create_post({**POST, "elapsed_ms": 500}, a)[0] == 429
    assert board.create_post({**POST, "category": "sale"}, a)[1]["error"] == "category"
    assert board.create_post({**POST, "title": "x"}, a)[1]["error"] == "title"
    assert board.create_post({**POST, "body": "a http://x.co b http://y.co c http://z.co d http://w.co"}, a)[1]["error"] == "links"
    for _ in range(board.POST_LIMIT):
        assert board.create_post(POST, a)[0] == 200
    assert board.create_post(POST, a)[1]["error"] == "limit"
    assert board.create_post(POST, _join("tok-b", "다른사람"))[0] == 200  # 회원마다 따로 셈


def test_only_author_deletes(monkeypatch):
    fake, _ = _setup(monkeypatch)
    a, b = _join("tok-a", "필름러"), _join("tok-b", "라이카")
    post_id = board.create_post(POST, a)[1]["id"]
    board.create_comment({"post_id": post_id, "body": "댓글", "elapsed_ms": 4000}, b)
    assert board.delete_entry({"post_id": post_id}, b)[0] == 403
    assert board.delete_entry({"post_id": post_id}, None)[0] == 403
    assert board.delete_entry({"post_id": post_id}, a)[0] == 200
    assert board.list_posts()["total"] == 0 and board.read_post(post_id)[0] == 404
    assert all(k.startswith(("board/removed/", "board/members/")) for k in fake.store)


def test_three_reports_hide_post_until_owner_restores(monkeypatch):
    fake, _ = _setup(monkeypatch)
    post_id = board.create_post(POST, _join("tok-a", "필름러"))[1]["id"]
    assert board.report({"post_id": post_id, "reason": "광고"}, _ip(5))[1]["hidden"] is False
    board.report({"post_id": post_id}, _ip(5))  # 같은 접속지는 한 번으로
    assert board.report({"post_id": post_id}, _ip(6))[1]["hidden"] is False
    assert board.report({"post_id": post_id}, _ip(7))[1]["hidden"] is True
    assert board.list_posts()["total"] == 0
    (held,) = [k for k in fake.store if k.startswith("board/held/")]
    board.owner_action({"action": "restore", "path": held})
    assert board.list_posts()["total"] == 1


def test_owner_needs_key(monkeypatch):
    monkeypatch.setenv("OWNER_DASHBOARD_KEY", "k" * 20)
    assert board.authorized("k" * 20) and not board.authorized("") and not board.authorized("nope")
    monkeypatch.setenv("OWNER_DASHBOARD_KEY", "short")
    assert not board.authorized("short")


def test_members_save_listings_and_see_price_changes(monkeypatch):
    fake, _ = _setup(monkeypatch)
    a = _join("tok-a", "필름러")
    item = {"url": "https://shop.example/m6", "title": "Leica M6", "price": 4000000, "currency": "KRW", "source": "샵", "image": "javascript:alert(1)"}
    assert board.save_item(item, None)[0] == 401  # 로그인한 회원만
    assert board.save_item({**item, "url": "ftp://x"}, a)[1]["error"] == "url"
    assert board.save_item(item, a)[1]["urls"] == ["https://shop.example/m6"]
    assert board.save_item({**item, "url": "https://shop.example/q3"}, a)[0] == 200
    assert board.save_item(item, a)[1]["urls"] == ["https://shop.example/m6", "https://shop.example/q3"]  # 같은 주소는 하나만, 최근이 앞
    saved = fake.store[f"board/saves/{a}.json"]["items"][0]
    assert saved["image"] == ""  # http(s)가 아닌 그림 주소는 저장 안 함
    current = {"https://shop.example/m6": {"sold_quality": "asking", "parsed_price_numeric": 3600000, "currency": "KRW"}}
    status, out = board.list_saves(a, with_status=True, current=current)
    now = {i["url"]: i["now"] for i in out["items"]}
    assert now["https://shop.example/m6"] == {"status": "asking", "price": 3600000, "currency": "KRW"}
    assert now["https://shop.example/q3"]["status"] == "gone"
    assert board.unsave_item({"url": "https://shop.example/m6"}, a)[1]["urls"] == ["https://shop.example/q3"]
    assert board.list_saves(_join("tok-b", "다른사람"))[1]["urls"] == []  # 회원마다 따로


def test_price_drop_alerts_only_for_members_who_turn_them_on(monkeypatch):
    fake, _ = _setup(monkeypatch)
    identities = {"tok-a": {"sub": "sub-a", "email": "film@example.com", "email_verified": True},
                  "tok-b": {"sub": "sub-b", "email": "", "email_verified": False}}
    monkeypatch.setattr(board, "google_identity", lambda c: identities.get(c))
    a = _join("tok-a", "필름러")
    board.save_item({"url": "https://shop/m6", "title": "Leica M6", "price": 4000000, "currency": "KRW", "source": "샵"}, a)
    board.save_item({"url": "https://shop/q3", "title": "Leica Q3", "price": 7000000, "currency": "KRW", "source": "샵"}, a)
    sent = []
    send = lambda to, subject, body: sent.append((to, subject, body)) or True
    now = {"https://shop/m6": {"sold_quality": "asking", "parsed_price_numeric": 4000000, "currency": "KRW"},
           "https://shop/q3": {"sold_quality": "asking", "parsed_price_numeric": 7000000, "currency": "KRW"}}
    assert board.run_alerts(current=now, send=send)["members"] == 0 and sent == []  # 켜지 않으면 안 보냄
    assert "film@example.com" not in json.dumps(fake.store)  # 켜기 전에는 이메일을 저장하지 않음
    assert board.alerts_on({"credential": "tok-b"}, a)[0] == 401  # 다른 사람 계정으로는 못 켬
    status, out = board.alerts_on({"credential": "tok-a", "locale": "ko"}, a, current=now)
    assert status == 200 and out["member"]["alerts"] is True and out["member"]["alerts_email"] == "fi**@example.com"
    assert board.run_alerts(current=now, send=send)["sent"] == 0  # 변화 없음
    now["https://shop/m6"]["parsed_price_numeric"] = 3600000  # 10% 내림
    del now["https://shop/q3"]  # 사라짐
    assert board.run_alerts(current=now, send=send)["sent"] == 1
    to, subject, body = sent[0]
    assert to == "film@example.com" and "2개" in subject and "−10%" in body and "더 이상 안 보임" in body and "r=unsub" in body
    assert board.run_alerts(current=now, send=send)["sent"] == 0  # 같은 변화는 다시 안 보냄
    assert len(sent) == 1
    sig = body.split("&s=")[1].split('"')[0]
    assert not board.unsubscribe(a, "wrong") and board.unsubscribe(a, sig)
    assert "film@example.com" not in json.dumps(fake.store)  # 끄면 이메일 지움


def test_failed_send_is_retried_next_time(monkeypatch):
    fake, _ = _setup(monkeypatch)
    monkeypatch.setattr(board, "google_identity", lambda c: {"sub": "sub-a", "email": "a@example.com", "email_verified": True})
    a = _join("tok-a", "필름러")
    board.save_item({"url": "https://shop/m6", "title": "M6", "price": 100, "currency": "KRW"}, a)
    now = {"https://shop/m6": {"sold_quality": "asking", "parsed_price_numeric": 100, "currency": "KRW"}}
    board.alerts_on({"credential": "x"}, a, current=now)
    now["https://shop/m6"]["parsed_price_numeric"] = 80
    monkeypatch.delenv("RESEND_API_KEY", raising=False)
    failed = board.run_alerts(current=now, send=lambda *x: False)
    assert failed["sent"] == 0 and failed["waiting"] == 1  # 못 보낸 건 기다리는 수로 (메일 키 없음 경고용)
    assert failed["mail_ready"] is False
    got = []
    assert board.run_alerts(current=now, send=lambda *x: got.append(x) or True)["sent"] == 1 and got


def _rec(url, price, currency="KRW", source="국민카메라", cond="", title="Leica Summicron 35mm f2 4th", entity="leica:lens:summicron-m:35:v4",
         status="asking"):
    return ({"source_url": url, "title_raw": title, "source": source, "currency": currency, "parsed_price_numeric": price,
             "condition_raw": cond, "category": "Lens", "sold_quality": status},
            [entity, "leica:lens:summicron-m:35"])


def test_want_alert_by_grade_and_delivered_total(monkeypatch):
    fake, _ = _setup(monkeypatch)
    monkeypatch.setattr(board, "google_identity", lambda c: {"sub": "sub-a", "email": "a@example.com", "email_verified": True})
    a = _join("tok-a", "필름러")
    records = [_rec("https://k/1", 2400000, cond="95%"),  # A, 국내 → 총액 240만 + 배송
               _rec("https://k/2", 2000000, cond="85%"),  # C → 등급 미달
               _rec("https://k/3", 3000000, cond="97%"),  # 총액 초과
               _rec("https://k/4", 1500000, cond=""),  # 등급 모름 → 알리지 않음
               _rec("https://k/5", 2000000, cond="96%", status="sold_confirmed")]  # 팔림
    status, out = board.want_add({"entity": "leica:lens:summicron-m:35:v4", "name": "Summicron 35 4th", "grade": "B",
                                  "max_total": 2500000, "currency": "KRW", "dest": "KR"}, a, records=records)
    assert status == 200 and [m["url"] for m in out["matches"]] == ["https://k/1"] and out["alerts"] is False
    assert out["matches"][0]["total"] == 2407000  # 판매가 + 국내 배송 (세금 없음)
    # 부모 모델로 걸어도 하위 모델 매물이 잡힘 (A 이상: 97%만, 95%는 B)
    assert [m["url"] for m in board.want_add({"entity": "leica:lens:summicron-m:35", "grade": "A", "max_total": 5000000, "currency": "KRW",
                                              "dest": "KR"}, a, records=records)[1]["matches"]] == ["https://k/3"]
    assert board.want_add({"entity": "bad id", "grade": "B", "max_total": 1, "currency": "KRW", "dest": "KR"}, a)[0] == 400
    assert board.want_add({"entity": "leica:lens:x", "grade": "B", "max_total": 1, "currency": "XXX", "dest": "KR"}, a)[0] == 400
    # 메일은 알림을 켠 회원에게, 등록할 때 있던 매물은 빼고 새로 나온 것만
    board.alerts_on({"credential": "x", "locale": "ko"}, a, current={})
    sent = []
    send = lambda to, subject, body: sent.append((to, subject, body)) or True
    assert board.run_alerts(current={}, send=send, records=records)["sent"] == 0
    records.append(_rec("https://k/6", 2100000, cond="A", source="기타무라 (일본)", currency="KRW"))  # 새 매물, 일본 → 한국 (세금 포함)
    records.append(_rec("https://k/7", 2300000, cond="96%"))  # 새 매물, 국내
    assert board.run_alerts(current={}, send=send, records=records)["sent"] == 1
    to, subject, body = sent[0]
    assert to == "a@example.com" and "찾던 매물" in subject and "https://k/7" in body and "도착 총액" in body
    assert board.run_alerts(current={}, send=send, records=records)["sent"] == 0  # 같은 매물은 다시 안 보냄
    status, listed = board.list_wants(a, records=records)
    assert status == 200 and len(listed["items"]) == 2 and "notified" not in listed["items"][0]
    board.want_remove({"id": listed["items"][0]["id"]}, a)
    assert len(board.list_wants(a, records=records)[1]["items"]) == 1


def test_run_retention_deletes_only_expired_days():
    import datetime as dt
    from types import SimpleNamespace
    import importlib, sys
    sys.path.insert(0, "api")
    board = importlib.import_module("board")
    today = dt.date(2027, 11, 10)
    old_day = (today - dt.timedelta(days=365)).isoformat()
    new_day = (today - dt.timedelta(days=364)).isoformat()
    store = {f"usage/{old_day}/a.json", f"usage/{new_day}/b.json", f"feedback/{old_day}/c.json", "board/removed/x~20200101~m.json"}

    class FakeBlob:
        def iter_objects(self, prefix=None):
            return [SimpleNamespace(pathname=p, url=p) for p in sorted(store) if p.startswith(prefix)]

        def delete(self, urls):
            for u in ([urls] if isinstance(urls, str) else urls):
                store.discard(u)

    result = board.run_retention(FakeBlob(), today=today)
    assert f"usage/{new_day}/b.json" in store
    assert f"usage/{old_day}/a.json" not in store and f"feedback/{old_day}/c.json" not in store
    assert result["usage"] == 1 and result["feedback"] == 1


def test_alerts_on_sends_confirmation_email(monkeypatch):
    """2026-11-08 사장님: 알림을 켜면 확인 메일 — 받는 사람 언어로, 끄기 링크 포함, 못 보내도 켜기는 성공"""
    _setup(monkeypatch)
    monkeypatch.setattr(board, "google_identity", lambda c: {"sub": "sub-c", "email": "lens@example.com", "email_verified": True})
    monkeypatch.setattr(board, "verify_google", lambda c: "sub-c")
    a = _join("tok-c", "렌즈")
    board.save_item({"url": "https://shop/m3", "title": "Leica M3", "price": 3000000, "currency": "KRW", "source": "샵"}, a)
    sent = []
    status, _ = board.alerts_on({"credential": "tok-c", "locale": "ko"}, a, current={}, send=lambda to, s, b: sent.append((to, s, b)) or True)
    assert status == 200 and len(sent) == 1
    to, subject, body = sent[0]
    assert to == "lens@example.com" and "가격 알림을 켰어요" in subject and "1개" in body and "r=unsub" in body
    def boom(*_a):
        raise RuntimeError("mail down")
    assert board.alerts_on({"credential": "tok-c", "locale": "de"}, a, current={}, send=boom)[0] == 200
