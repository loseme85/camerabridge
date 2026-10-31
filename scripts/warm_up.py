"""배포 직후 미리 깨우기: 인기 모델 검색을 한 번씩 보내 서버를 켜 두고 결과를 CDN에 저장해 둔다.

배포가 새로 되면 서버가 처음 켜지며 30MB 색인을 읽느라 첫 검색이 2~3초 걸린다 (2026-10-31 측정).
크롤링 워크플로가 배포 성공을 확인한 뒤 실행한다. 화면이 보내는 주소와 똑같이 보내야 CDN 저장분이 쓰인다:
  목록  /api/search?q=<모델 이름>&entity=<id>&limit=12&offset=0   (beta.html runSearch, PAGE_SIZE 12)
  그래프 /api/search?q=<모델 이름>&entity=<id>&limit=100&offset=0·100·200   (loadPriceLadder)
모델 이름은 화면 언어에 따라 영어 이름 또는 한국어 이름 (entityDisplayName).
"""
from __future__ import annotations

import json
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from urllib.parse import urlencode

import requests

ROOT = Path(__file__).resolve().parents[1]
BASE = (sys.argv[1] if len(sys.argv) > 1 else "https://camerabridge.io").rstrip("/")


def urls() -> list[str]:
    picks = json.loads((ROOT / "data/config/home_picks.json").read_text(encoding="utf-8"))["picks"]
    entities = {e["id"]: e for e in json.loads((ROOT / "data/derived/entity_summary_v1.json").read_text(encoding="utf-8"))["entities"]}
    out = [f"{BASE}/", f"{BASE}/api/board?page=1"]
    for entity_id in picks:
        entity = entities.get(entity_id)
        if not entity:
            continue
        for name in {entity.get("name"), entity.get("name_ko")} - {None, ""}:
            out.append(f"{BASE}/api/search?{urlencode({'q': name, 'entity': entity_id, 'limit': 12, 'offset': 0})}")
            out += [f"{BASE}/api/search?{urlencode({'q': name, 'entity': entity_id, 'limit': 100, 'offset': offset})}" for offset in (0, 100, 200)]
    return out


def hit(url: str) -> tuple[int, float]:
    started = time.time()
    try:
        status = requests.get(url, timeout=30, headers={"User-Agent": "CameraBridge-warmup"}).status_code
    except requests.RequestException:
        status = 0
    return status, time.time() - started


def main() -> None:
    targets = urls()
    started = time.time()
    with ThreadPoolExecutor(max_workers=6) as pool:  # 서버 여러 개를 함께 깨우되 한꺼번에 몰리지 않게
        results = list(pool.map(hit, targets))
    ok = sum(1 for status, _ in results if status == 200)
    slow = max((seconds for _, seconds in results), default=0)
    print(f"🔥 미리 깨우기: {ok}/{len(targets)}건 성공 · 가장 느린 요청 {slow:.1f}초 · 전체 {time.time() - started:.0f}초")


if __name__ == "__main__":
    main()
