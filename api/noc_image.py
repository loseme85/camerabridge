"""Newoldcamera(이탈리아) 매물 사진: 그때그때 새 주소로 넘겨줌.

사진 경로가 없는 매물은 사진이 Azure Blob에 있고, 사이트 API가 주는 서명 주소가 1시간이면 만료된다.
크롤 결과에는 /api/noc_image?code=<상품코드>를 넣고, 열 때마다 첫 사진의 새 서명 주소로 302 이동.
열린 중계가 되지 않도록 상품코드 형식(예: 26U2960)만 받고, 받은 주소가 nocimage 저장소일 때만 이동.
"""
from __future__ import annotations

import re
from http.server import BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse

import requests

API = "https://apinoccore.azurewebsites.net/api/BlobService/GetBlobsImageOrder"
CODE = re.compile(r"^\d{2}[A-Z]\d{4}$")
BLOB = re.compile(r"^https://nocimage\.blob\.core\.windows\.net/products/")


class handler(BaseHTTPRequestHandler):
    def _send(self, status, location=None, cache="no-store"):
        self.send_response(status)
        if location:
            self.send_header("location", location)
        self.send_header("cache-control", cache)
        self.end_headers()

    def do_GET(self):
        code = (parse_qs(urlparse(self.path).query).get("code") or [""])[0].upper()
        if not CODE.match(code):
            return self._send(400)
        try:
            resp = requests.get(API, params={"containerName": "products", "productCode": code, "targetOrder": 0},
                                headers={"Accept": "application/json"}, timeout=8)
            uri = ((resp.json() or {}).get("blob") or {}).get("uri") or ""
        except Exception:  # noqa: BLE001
            return self._send(502)
        if not BLOB.match(uri):
            return self._send(404, cache="public, max-age=3600")
        # 서명은 1시간 유효 → 브라우저·CDN은 30분만 기억
        return self._send(302, uri, cache="public, max-age=1800, s-maxage=1800")
