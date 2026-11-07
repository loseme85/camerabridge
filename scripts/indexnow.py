"""IndexNow: 바뀐 모델 페이지를 Bing·네이버·얀덱스 등에 바로 알림 (구글은 IndexNow를 안 씀 → 사이트맵으로).

    python3 scripts/indexnow.py --plan     # 크롤 커밋 전: 지난 커밋과 비교해 내용이 바뀐·새 페이지 주소를 data/derived/indexnow_pending.json 에
    python3 scripts/indexnow.py --send     # 푸시 뒤: 그 목록을 api.indexnow.org 로 보냄 (참여 검색엔진끼리 공유)
    python3 scripts/indexnow.py --all      # 사이트맵의 모든 주소를 한 번에 (처음 한 번)

키 파일: 저장소 맨 위 <KEY>.txt (공개용, 검색엔진이 우리 사이트 것인지 확인할 때 읽음).
알리기 실패는 크롤을 멈추지 않음 (경고만).
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HOST = "camerabridge.io"
KEY = "653564e5e19036e4b40d85befed4b062"
LASTMOD = ROOT / "data" / "derived" / "model_pages_lastmod.json"
PENDING = ROOT / "data" / "derived" / "indexnow_pending.json"
ENDPOINT = "https://api.indexnow.org/indexnow"
BATCH = 10_000  # IndexNow 한 번에 최대 주소 수


def changed_urls() -> list[str]:
    """작업 폴더의 lastmod 지문과 지난 커밋(HEAD)의 것을 비교해 바뀐·새 주소."""
    now = json.loads(LASTMOD.read_text(encoding="utf-8")) if LASTMOD.exists() else {}
    try:
        old_text = subprocess.run(["git", "show", f"HEAD:{LASTMOD.relative_to(ROOT)}"], cwd=ROOT,
                                  capture_output=True, text=True, check=True).stdout
        old = json.loads(old_text)
    except (subprocess.CalledProcessError, ValueError):
        old = {}
    return sorted(url for url, mark in now.items() if (old.get(url) or {}).get("h") != mark.get("h"))


def sitemap_urls() -> list[str]:
    return re.findall(r"<loc>([^<]+)</loc>", (ROOT / "sitemap.xml").read_text(encoding="utf-8"))


def send(urls: list[str]) -> bool:
    ok = True
    for i in range(0, len(urls), BATCH):
        body = json.dumps({"host": HOST, "key": KEY, "keyLocation": f"https://{HOST}/{KEY}.txt",
                           "urlList": urls[i:i + BATCH]}).encode()
        request = urllib.request.Request(ENDPOINT, data=body, method="POST",
                                         headers={"content-type": "application/json; charset=utf-8"})
        try:
            with urllib.request.urlopen(request, timeout=30) as response:
                print(f"IndexNow {len(urls[i:i + BATCH])}개 → {response.status}")
        except Exception as error:  # noqa: BLE001 (알리기 실패는 크롤을 멈추지 않음)
            print(f"⚠️ IndexNow 실패: {error}")
            ok = False
    return ok


def main() -> int:
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--plan", action="store_true")
    group.add_argument("--send", action="store_true")
    group.add_argument("--all", action="store_true")
    args = parser.parse_args()
    if args.plan:
        urls = changed_urls()
        PENDING.write_text(json.dumps(urls, ensure_ascii=False, indent=0), encoding="utf-8")
        print(f"알릴 페이지 {len(urls)}개")
        return 0
    if args.send:
        urls = json.loads(PENDING.read_text(encoding="utf-8")) if PENDING.exists() else []
        if not urls:
            print("알릴 페이지 없음")
            return 0
        send(urls)
        return 0
    send(sitemap_urls())
    return 0


if __name__ == "__main__":
    sys.exit(main())
