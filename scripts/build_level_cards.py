"""라이카 레벨 테스트 공유 카드: img/level/{1..7}.png (1200×630) + 공유 주소 lv/{1..7}/index.html

2026-11-08 사장님(방문 늘리기 3번): 결과를 공유하면 레딧·카톡·X 미리보기에 'Level 6 / 7' 카드가 뜨고, 누르면 퀴즈로 바로.
첫 화면은 정적 파일이라 주소의 ?lv= 로 미리보기를 바꿀 수 없어서 레벨마다 작은 페이지를 둔다 (미리보기 태그 + 퀴즈로 이동).
레벨 이름을 바꾸면 이 스크립트를 다시 돌린다 (크롤마다 돌릴 필요 없음). 글꼴은 맥 기본 Georgia.
"""
from __future__ import annotations

import html
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
NAMES = ["Curious", "Enthusiast", "Shooter", "Collector", "Expert", "Connoisseur", "Wetzlar Master"]  # beta.html quiz_lv1~7 (en)
FONT_DIR = Path("/System/Library/Fonts/Supplemental")
BG, INK, SOFT, RULE, ACCENT = (251, 250, 247), (22, 24, 26), (110, 114, 117), (22, 24, 26), (31, 74, 58)


def font(name: str, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(str(FONT_DIR / name), size)


def card(level: int) -> Image.Image:
    img = Image.new("RGB", (1200, 630), BG)
    d = ImageDraw.Draw(img)
    # 인쇄 카탈로그 틀: 위 굵은 줄 + 가는 줄, 장식 없음
    d.rectangle([60, 56, 1140, 59], fill=RULE)
    d.rectangle([60, 66, 1140, 66], fill=RULE)
    d.text((60, 92), "Camera Bridge", font=font("Georgia Italic.ttf", 34), fill=ACCENT)
    d.text((1140, 100), "Leica level test", font=font("Georgia.ttf", 26), fill=SOFT, anchor="ra")
    big = font("Georgia.ttf", 150)
    d.text((60, 330), f"Level {level}", font=big, fill=INK, anchor="ls")  # 글자 밑선(ls)을 맞춤
    d.text((60 + d.textlength(f"Level {level}", font=big) + 22, 330), "/ 7", font=font("Georgia.ttf", 56), fill=SOFT, anchor="ls")
    d.text((64, 372), NAMES[level - 1], font=font("Georgia Italic.ttf", 64), fill=INK)
    # 7칸 막대: 받은 레벨까지 채움 (각진 네모)
    for i in range(7):
        x0 = 64 + i * 84
        box = [x0, 480, x0 + 70, 494]
        d.rectangle(box, fill=INK if i < level else None, outline=INK, width=2)
    d.rectangle([60, 540, 1140, 540], fill=RULE)
    d.text((60, 562), "How well do you know Leica?", font=font("Georgia.ttf", 30), fill=INK)
    d.text((1140, 562), "camerabridge.io", font=font("Georgia.ttf", 30), fill=SOFT, anchor="ra")
    return img


def page(level: int) -> str:
    title = f"I got Level {level} / 7 ({NAMES[level - 1]}) on the Leica level test"
    desc = "Double strokes, commemorative bodies, nicknames, old Leitz code words — 10 questions only Leica nerds get right. How well do you know Leica?"
    image = f"https://camerabridge.io/img/level/{level}.png"
    target = f"/?quiz=1&utm_source=quiz-share&utm_content=lv{level}"
    t, dsc = html.escape(title), html.escape(desc)
    return (f'<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">'
            f"<title>{t} | Camera Bridge</title><meta name=\"description\" content=\"{dsc}\"><meta name=\"robots\" content=\"noindex\">"
            f'<meta property="og:type" content="website"><meta property="og:site_name" content="Camera Bridge">'
            f'<meta property="og:url" content="https://camerabridge.io/lv/{level}/"><meta property="og:title" content="{t}">'
            f'<meta property="og:description" content="{dsc}"><meta property="og:image" content="{image}">'
            f'<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">'
            f'<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{t}">'
            f'<meta name="twitter:description" content="{dsc}"><meta name="twitter:image" content="{image}">'
            f'<meta http-equiv="refresh" content="0; url={target}"><script>location.replace({target!r});</script></head>'
            f'<body><p><a href="{target}">Take the Leica level test</a></p></body></html>\n')


def main() -> None:
    (ROOT / "img" / "level").mkdir(parents=True, exist_ok=True)
    for level in range(1, 8):
        card(level).save(ROOT / "img" / "level" / f"{level}.png", optimize=True)
        out = ROOT / "lv" / str(level) / "index.html"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(page(level), encoding="utf-8")
    print("✅ 레벨 카드 7장 (img/level/) · 공유 주소 7개 (lv/)")


if __name__ == "__main__":
    main()
