"""사진 등급 대기열: 매장 표기로 등급을 못 정한 판매 중 매물을 모아 두었다가, 루틴 때 조금씩 사진으로 등급을 매긴다.

크롤링 때마다 API로 사진을 보내는 대신(요금), 저녁루틴·등급 점검 때 Claude가 30개씩 시트를 보고 매긴다 (2026-11-02 사장님).
결과는 data/config/photo_grades.json (링크 → {grade, at, note})에 쌓이고, final_resolution_pipeline이 image_grade로 붙여
화면에 '사진으로 추정'으로 나온다. 한 번 본 매물은 다시 대기열에 오르지 않는다 ('?' = 사진으로 판단 못 함도 기록).

  python3 scripts/photo_grade_queue.py status
  python3 scripts/photo_grade_queue.py queue --n 30 --out <폴더>
      → 비싼 매물부터 n개: 사진(000.jpg …)·시트(sheet*.jpg, 12개씩)·key.json
  (시트를 보고 번호마다 N·S·A·B·C·D·X 또는 ?를 mine.json에 {"0": "B", "1": "?", …})
  python3 scripts/photo_grade_queue.py apply --key <폴더>/key.json --mine <폴더>/mine.json

사진 평가 기준: 매장 표기 대응을 맞출 때 사진이 매장 표기보다 평균 0.3~0.9등급 후했다 (grade_audit). 그래서 사진만 볼 때는
한 단계 엄하게 본다 — 흠이 안 보이면 A(새것 같음·박스는 S), 가벼운 사용감 B, 뚜렷한 사용감·도장 벗겨짐 C, 찍힘·큰 흠 D, 부품·고장 X.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))
from condition_grade import GRADES, grade_of  # noqa: E402
from entity_catalog import load_catalog, price_krw  # noqa: E402
from grade_audit import _sheets  # noqa: E402

INDEX = ROOT / "data/derived/results_search_index_v1.json"
GRADES_PATH = ROOT / "data/config/photo_grades.json"
SKIP_NOTES = ("too_cheap", "set", "duplicate")


def _load_grades() -> dict:
    if GRADES_PATH.exists():
        return json.loads(GRADES_PATH.read_text(encoding="utf-8"))
    return {"grades": {}}


def candidates() -> list[dict]:
    """판매 중 · 가격 있음 · 모델 연결 · 매장 표기로 등급 모름 · 사진 있음 · 아직 안 본 매물, 비싼 순"""
    seen = _load_grades()["grades"]
    ents = load_catalog()["entities"]
    out = []
    for record in json.loads(INDEX.read_text(encoding="utf-8"))["records"]:
        final = record.get("final_output") or {}
        link = final.get("source_url") or (record.get("raw_item") or {}).get("링크")
        if final.get("sold_quality") != "asking" or not final.get("image_url") or not link or link in seen:
            continue
        if (final.get("entity_note") or "") in SKIP_NOTES:
            continue
        leaves = [e for e in record.get("entity_ids") or [] if e in ents and not ents[e].get("children") and not ents[e].get("feature")]
        krw = price_krw(final)
        if not leaves or not krw:
            continue
        if grade_of(final.get("source"), final.get("condition_raw"), final.get("title_raw"))[0] or final.get("image_grade"):
            continue
        out.append({"link": link, "image": final["image_url"], "title": final.get("title_raw"), "site": final.get("source"),
                    "model": ents[leaves[0]].get("name_ko") or ents[leaves[0]]["name"], "krw": round(krw)})
    return sorted(out, key=lambda c: -c["krw"])


def status(_args) -> None:
    rows = candidates()
    by_site: dict[str, int] = {}
    for row in rows:
        by_site[row["site"]] = by_site.get(row["site"], 0) + 1
    done = _load_grades()["grades"]
    print(f"대기 {len(rows)}개 · 평가함 {sum(1 for g in done.values() if g.get('grade'))}개 · 사진으로 판단 못 함 {sum(1 for g in done.values() if not g.get('grade'))}개")
    for site, n in sorted(by_site.items(), key=lambda kv: -kv[1])[:10]:
        print(f"  {site}: {n}")


def queue(args) -> None:
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    items = candidates()[: args.n]
    for n, item in enumerate(items):
        item["n"] = n
        subprocess.run(["curl", "-sL", "-m", "25", "-A", "Mozilla/5.0", "-o", str(out / f"{n:03d}.jpg"), item["image"]], check=False)
    (out / "key.json").write_text(json.dumps({"items": items}, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"사진 {len(items)}개 · 시트 {_sheets(items, out) if items else 0}장 → {out} (대기 남음 {max(0, len(candidates()) - len(items))}개)")


def apply(args) -> None:
    key = json.loads(Path(args.key).read_text(encoding="utf-8"))["items"]
    mine = {int(k): str(v).strip().upper() for k, v in json.loads(Path(args.mine).read_text(encoding="utf-8")).items()}
    data = _load_grades()
    today = dt.date.today().isoformat()
    added = unsure = 0
    for item in key:
        mark = mine.get(item["n"])
        if mark is None:
            continue  # 안 매긴 번호는 다음에 다시
        if mark in GRADES:
            data["grades"][item["link"]] = {"grade": mark, "at": today, "site": item["site"]}
            added += 1
        else:
            data["grades"][item["link"]] = {"grade": None, "at": today, "site": item["site"], "note": "사진으로 판단 못 함"}
            unsure += 1
    data["grades"] = dict(sorted(data["grades"].items()))
    GRADES_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"등급 {added}개 · 판단 못 함 {unsure}개 → {GRADES_PATH.relative_to(ROOT)}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = parser.add_subparsers(dest="cmd", required=True)
    sub.add_parser("status").set_defaults(fn=status)
    q = sub.add_parser("queue")
    q.add_argument("--n", type=int, default=30)
    q.add_argument("--out", required=True)
    q.set_defaults(fn=queue)
    a = sub.add_parser("apply")
    a.add_argument("--key", required=True)
    a.add_argument("--mine", required=True)
    a.set_defaults(fn=apply)
    args = parser.parse_args()
    args.fn(args)


if __name__ == "__main__":
    main()
