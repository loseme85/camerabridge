"""카메라브릿지 중계 서버 (Vercel 도쿄).

GitHub Actions(미국)에서 막히는 일본 사이트를 도쿄에서 대신 받아 그대로 돌려준다.
열린 중계가 되지 않도록: 비밀 키(x-relay-key)가 맞고, 허용한 사이트(https)만.
사이트 추가: ALLOWED_HOSTS에 호스트 한 줄.
"""
import hmac
import json
import os
import urllib.error
import urllib.request
from http.server import BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse

ALLOWED_HOSTS = {
    "shop.kitamura.jp",  # 기타무라 (일본)
}
DROP_HEADERS = {"host", "connection", "content-length", "transfer-encoding", "cookie", "x-relay-key", "x-relay-headers"}
MAX_BYTES = 4_000_000  # Vercel 응답 한도(4.5MB) 안쪽


class handler(BaseHTTPRequestHandler):
    def _send(self, status, body, content_type="application/json"):
        if isinstance(body, (dict, list)):
            body = json.dumps(body).encode()
        self.send_response(status)
        self.send_header("content-type", content_type)
        self.send_header("x-relay-region", os.environ.get("VERCEL_REGION", ""))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        key = os.environ.get("RELAY_KEY", "")
        if not key or not hmac.compare_digest(self.headers.get("x-relay-key", ""), key):
            return self._send(401, {"error": "unauthorized"})
        target = (parse_qs(urlparse(self.path).query).get("url") or [""])[0]
        parsed = urlparse(target)
        if parsed.scheme != "https" or parsed.hostname not in ALLOWED_HOSTS:
            return self._send(403, {"error": "host not allowed"})
        try:
            extra = json.loads(self.headers.get("x-relay-headers") or "{}")
        except ValueError:
            return self._send(400, {"error": "bad x-relay-headers"})
        headers = {k: str(v) for k, v in extra.items() if k.lower() not in DROP_HEADERS}
        try:
            with urllib.request.urlopen(urllib.request.Request(target, headers=headers), timeout=25) as r:
                body, status, ctype = r.read(MAX_BYTES + 1), r.status, r.headers.get("content-type", "")
        except urllib.error.HTTPError as e:
            body, status, ctype = e.read(MAX_BYTES + 1), e.code, e.headers.get("content-type", "")
        except Exception as e:  # noqa: BLE001
            return self._send(502, {"error": f"upstream: {type(e).__name__}"})
        if len(body) > MAX_BYTES:
            return self._send(502, {"error": "response too large"})
        return self._send(status, body, ctype or "application/octet-stream")
