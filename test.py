# ================================================================
# 반도카메라 중고 라이카 크롤러
# 대상: https://bandocamera.co.kr/product/list.html?cate_no=789
#
# 실행 전 준비 (터미널/명령 프롬프트에서):
#   pip install playwright
#   playwright install chromium
# ================================================================

from playwright.sync_api import sync_playwright
import time

# ── 설정 ──────────────────────────────────────────────────────
BASE_URL = "https://bandocamera.co.kr/product/list.html?cate_no=789"
KEYWORD  = "leica"   # 라이카 관련 항목만 필터링 (비워두면 전체 수집)


def crawl_bandocamera():
    results = []

    with sync_playwright() as p:

        # ① 브라우저 열기 (headless=False → 창이 눈에 보임)
        browser = p.chromium.launch(headless=False)
        page    = browser.new_page()

        # ② 중고/위탁 목록 페이지로 이동
        print(f"[1단계] 사이트 접속 중: {BASE_URL}")
        page.goto(BASE_URL, wait_until="domcontentloaded")
        time.sleep(2)   # 페이지가 완전히 뜰 때까지 잠깐 기다림

        # ③ 상품 카드가 화면에 나타날 때까지 대기
        #    카페24 공통 selector → .prdList li  또는  ul.prdList > li
        page.wait_for_selector("ul.prdList > li", timeout=10_000)

        # ④ 페이지네이션 처리 (최대 5페이지까지)
        for page_num in range(1, 6):
            print(f"\n[2단계] {page_num}페이지 수집 중...")

            # 상품 카드 전체 선택
            items = page.query_selector_all("ul.prdList > li")
            print(f"  └─ 상품 {len(items)}개 발견")

            for item in items:
                # ─ 상품명 ─
                name_el = item.query_selector(".name")          # 카페24 기본 selector
                if name_el is None:
                    name_el = item.query_selector("strong.name, p.name")
                name = name_el.inner_text().strip() if name_el else "이름 없음"

                # ─ 가격 ─
                price_el = item.query_selector(".price")
                if price_el is None:
                    price_el = item.query_selector("span.price, li.price")
                price = price_el.inner_text().strip() if price_el else "가격 없음"

                # ─ 링크 ─
                link_el = item.query_selector("a")
                href    = link_el.get_attribute("href") if link_el else ""
                if href and not href.startswith("http"):
                    href = "https://bandocamera.co.kr" + href

                # ─ 이미지 ─
                img_el = item.query_selector("img")
                img    = img_el.get_attribute("src") if img_el else ""

                # ─ 라이카 필터링 ─
                if KEYWORD and KEYWORD.lower() not in name.lower():
                    continue

                results.append({
                    "상품명": name,
                    "가격":   price,
                    "링크":   href,
                    "이미지": img,
                })
                print(f"  ✔  {name}  |  {price}")

            # ─ 다음 페이지로 이동 ─
            next_btn = page.query_selector(f"a.nav[href*='page={page_num + 1}']")
            if next_btn is None:
                # 카페24는 페이지 번호 링크가 다양한 형태
                next_btn = page.query_selector(f"#pageList a[href*='page={page_num + 1}']")

            if next_btn:
                next_btn.click()
                page.wait_for_selector("ul.prdList > li", timeout=10_000)
                time.sleep(1.5)
            else:
                print("\n[3단계] 마지막 페이지 도달 → 수집 종료")
                break

        browser.close()

    # ⑤ 결과 출력
    print("\n" + "=" * 50)
    print(f"총 {len(results)}개 라이카 중고 매물 수집 완료")
    print("=" * 50)
    for r in results:
        print(f"\n📷 {r['상품명']}")
        print(f"   💰 {r['가격']}")
        print(f"   🔗 {r['링크']}")

    return results


# ── 실행 ──────────────────────────────────────────────────────
if __name__ == "__main__":
    crawl_bandocamera()
