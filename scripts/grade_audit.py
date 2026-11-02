"""등급 점검: 매장 표기 → 공통 등급(condition_grade) 대응이 사진으로 봐도 맞는지 주기적으로 다시 맞춰 본다.

사이트를 붙일 때 한 번 사진 평가로 대응을 정했지만, 매장이 표기 습관을 바꾸거나 처음 표본이 적었으면 어긋날 수 있다.
사진 평가는 사람(또는 Claude)이 표기를 가린 채 한다 — 이 스크립트는 표본 뽑기와 채점만.

  python3 scripts/grade_audit.py sample --history <기록.json> --sites 5 --per-site 20 --out <폴더>
      → 오래 점검 안 한 매장부터 골라, 매장마다 등급별로 고르게 표본을 뽑아 사진 시트(sheet*.jpg)와 정답지(key.json, 표기 포함)
  (사진 시트를 보고 번호마다 N·S·A·B·C·D·X를 매겨 mine.json에 {"0": "A", "1": "B", …})
  python3 scripts/grade_audit.py score --key <폴더>/key.json --mine <폴더>/mine.json --history <기록.json> --report <보고.md>
      → 매장별 정확 일치·한 등급 이내·쏠림(사진이 평균 몇 등급 후한지), 기준을 벗어나면 '대응 다시 보기'

기준: 기존 매장 사진 평가에서 사진이 매장 표기보다 평균 0.3~0.8등급 후했다 (2026-10). 한 등급 이내 75% 미만이거나
쏠림이 −0.3 미만(매장이 사진보다 후함 = 우리가 등급을 높게 줌)·1.3 초과(매장이 엄함 = 낮게 줌)면 대응을 다시 본다.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import random
import subprocess
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from condition_grade import GRADES, grade_of  # noqa: E402

RESULTS = ROOT / "data/raw/results.json"
MIN_WITHIN_ONE = 0.75
BIAS_RANGE = (-0.3, 1.3)


def _graded_listings() -> dict[str, list[dict]]:
    """매장 → 판매 중이고 표기로 등급이 정해지고 사진이 있는 매물"""
    by_site: dict[str, list[dict]] = defaultdict(list)
    for row in json.loads(RESULTS.read_text(encoding="utf-8")):
        if row.get("품절") or not row.get("이미지"):
            continue
        grade, how = grade_of(row.get("site"), row.get("컨디션"), row.get("상품명"))
        if grade and grade != "X" and how == "label":
            by_site[row["site"]].append({"site": row["site"], "label": row.get("컨디션"), "grade": grade, "title": row.get("상품명"),
                                         "link": row.get("링크"), "image": row.get("이미지")})
    return by_site


def _history(path: Path | None) -> dict:
    if path and path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return {"sites": {}}


def pick_sites(by_site: dict[str, list[dict]], history: dict, count: int, minimum: int = 12) -> list[str]:
    """한 번도 안 본 매장 → 오래전에 본 매장 순, 같으면 매물이 많은 순"""
    eligible = [s for s, rows in by_site.items() if len(rows) >= minimum]
    last = lambda s: (history.get("sites", {}).get(s, {}).get("last") or "")  # noqa: E731
    return sorted(eligible, key=lambda s: (last(s), -len(by_site[s])))[:count]


def stratified(rows: list[dict], n: int, seed: int) -> list[dict]:
    """매장 표기별로 고르게 (표기마다 차례로 하나씩)"""
    rng = random.Random(seed)
    by_label: dict[str, list[dict]] = defaultdict(list)
    for row in rows:
        by_label[str(row["label"])].append(row)
    for items in by_label.values():
        rng.shuffle(items)
    out: list[dict] = []
    while len(out) < n and any(by_label.values()):
        for label in sorted(by_label):
            if by_label[label] and len(out) < n:
                out.append(by_label[label].pop())
    return out


def _sheets(items: list[dict], out: Path) -> int:
    from PIL import Image, ImageDraw  # noqa: WPS433
    size, cols, per = 380, 4, 12
    sheets = 0
    for start in range(0, len(items), per):
        group = items[start:start + per]
        canvas = Image.new("RGB", (size * cols, size * ((len(group) + cols - 1) // cols)), "white")
        draw = ImageDraw.Draw(canvas)
        for k, item in enumerate(group):
            x, y = (k % cols) * size, (k // cols) * size
            path = out / f"{item['n']:03d}.jpg"
            try:
                img = Image.open(path).convert("RGB")
                img.thumbnail((size - 8, size - 8))
                canvas.paste(img, (x + 4, y + 4))
            except Exception:  # noqa: BLE001
                draw.text((x + 20, y + 40), "no image", fill="black")
            draw.rectangle([x, y, x + 44, y + 22], fill="yellow")
            draw.text((x + 6, y + 5), str(item["n"]), fill="black")
        canvas.save(out / f"sheet{sheets}.jpg", quality=82)
        sheets += 1
    return sheets


def sample(args) -> None:
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    by_site = _graded_listings()
    history = _history(Path(args.history) if args.history else None)
    sites = args.site or pick_sites(by_site, history, args.sites)
    items: list[dict] = []
    seed = int(dt.date.today().strftime("%Y%m%d"))
    for site in sites:
        items += stratified(by_site.get(site, []), args.per_site, seed)
    random.Random(seed).shuffle(items)  # 매장끼리 섞어 매장 습관을 보고 짐작하지 않게
    for n, item in enumerate(items):
        item["n"] = n
        subprocess.run(["curl", "-sL", "-m", "25", "-A", "Mozilla/5.0", "-o", str(out / f"{n:03d}.jpg"), item["image"]], check=False)
    (out / "key.json").write_text(json.dumps({"sites": sites, "items": items}, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"매장 {len(sites)}곳 · 표본 {len(items)}점 · 시트 {_sheets(items, out)}장 → {out}")
    for site in sites:
        print(f"  {site}: {sum(1 for i in items if i['site'] == site)}점")


def score(args) -> None:
    key = json.loads(Path(args.key).read_text(encoding="utf-8"))
    mine = {int(k): str(v).upper() for k, v in json.loads(Path(args.mine).read_text(encoding="utf-8")).items()}
    idx = {g: i for i, g in enumerate(GRADES)}
    per: dict[str, list[tuple[str, str, str]]] = defaultdict(list)
    for item in key["items"]:
        photo = mine.get(item["n"])
        if photo in idx:  # 사진이 안 열린 표본은 빼고
            per[item["site"]].append((str(item["label"]), item["grade"], photo))
    today = dt.date.today().isoformat()
    history = _history(Path(args.history) if args.history else None)
    lines = [f"## 등급 점검 {today}", "", "| 매장 | 표본 | 정확 일치 | 한 등급 이내 | 쏠림 | 판정 |", "|---|---|---|---|---|---|"]
    flagged = []
    for site in sorted(per):
        rows = per[site]
        n = len(rows)
        exact = sum(1 for _, g, p in rows if g == p)
        within = sum(1 for _, g, p in rows if abs(idx[g] - idx[p]) <= 1)
        bias = sum(idx[g] - idx[p] for _, g, p in rows) / n  # + = 사진이 우리 등급보다 후함
        ok = within / n >= MIN_WITHIN_ONE and BIAS_RANGE[0] <= bias <= BIAS_RANGE[1]
        verdict = "괜찮음" if ok else "대응 다시 보기"
        if not ok:
            flagged.append(site)
        lines.append(f"| {site} | {n} | {exact}/{n} | {within}/{n} | {bias:+.2f} | {verdict} |")
        history.setdefault("sites", {})[site] = {"last": today, "n": n, "exact": exact, "within": within, "bias": round(bias, 2), "ok": ok}
    for site in flagged:
        lines += ["", f"### {site} — 표기별 (매장 표기 → 우리 등급 · 사진 등급)"]
        by_label: dict[str, list[str]] = defaultdict(list)
        mapped = {}
        for label, g, p in per[site]:
            by_label[label].append(p)
            mapped[label] = g
        for label in sorted(by_label):
            photos = ", ".join(f"{g} {by_label[label].count(g)}" for g in GRADES if by_label[label].count(g))
            lines.append(f"- `{label}` → {mapped[label]} · 사진 {photos}")
    report = "\n".join(lines) + "\n"
    if args.report:
        path = Path(args.report)
        old = path.read_text(encoding="utf-8") if path.exists() else "# 등급 점검 기록\n\n`scripts/grade_audit.py`로 표본을 뽑아 사진으로 평가한 결과. 새 결과를 위에 더한다.\n\n"
        head, _, rest = old.partition("\n## ")
        path.write_text(head.rstrip("\n") + "\n\n" + report + ("\n## " + rest if rest else ""), encoding="utf-8")
    if args.history:
        Path(args.history).write_text(json.dumps(history, ensure_ascii=False, indent=1), encoding="utf-8")
    print(report)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = parser.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("sample")
    s.add_argument("--out", required=True)
    s.add_argument("--history")
    s.add_argument("--sites", type=int, default=5)
    s.add_argument("--per-site", type=int, default=20)
    s.add_argument("--site", action="append", help="이 매장만 (여러 번 줄 수 있음)")
    s.set_defaults(fn=sample)
    c = sub.add_parser("score")
    c.add_argument("--key", required=True)
    c.add_argument("--mine", required=True)
    c.add_argument("--history")
    c.add_argument("--report")
    c.set_defaults(fn=score)
    args = parser.parse_args()
    args.fn(args)


if __name__ == "__main__":
    main()
