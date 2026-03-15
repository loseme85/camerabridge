from playwright.sync_api import sync_playwright
import time
import json
import re

# ══════════════════════════════════════════════════════
# 검색 아이템 정의
# ══════════════════════════════════════════════════════
SEARCH_ITEMS = [
    {"label": "35mm Summicron", "keywords": ["35mm Summicron", "Summicron 35mm", "35cron"], "must_contain": ["summicron", "35"]},
    {"label": "35mm Summicron ASPH", "keywords": ["35mm Summicron ASPH", "Summicron 35mm ASPH"], "must_contain": ["summicron", "35", "asph"]},
    # ── 35mm Summilux ──
    {"label": "35mm Summilux", "keywords": ["35mm Summilux", "Summilux 35mm", "35lux"], "must_contain": ["summilux", "35"]},
    {"label": "35mm Summilux ASPH", "keywords": ["35mm Summilux ASPH", "Summilux 35mm ASPH"], "must_contain": ["summilux", "35", "asph"]},
    {"label": "35mm Summilux FLE", "keywords": ["35mm Summilux FLE", "Summilux 35mm FLE"], "must_contain": ["summilux", "35", "fle"]},
    # ── 50mm Summicron ──
    {"label": "50mm Summicron", "keywords": ["50mm Summicron", "Summicron 50mm", "50cron"], "must_contain": ["summicron", "50"]},
    {"label": "50mm Summicron DR", "keywords": ["50mm Summicron DR", "Summicron DR", "Dual Range"], "must_contain": ["summicron", "50"]},
    {"label": "50mm APO-Summicron", "keywords": ["50mm APO Summicron", "APO Summicron 50mm", "APO Summicron"], "must_contain": ["apo", "summicron", "50"]},
    # ── 50mm Summilux ──
    {"label": "50mm Summilux", "keywords": ["50mm Summilux", "Summilux 50mm", "50lux"], "must_contain": ["summilux", "50"]},
    {"label": "50mm Summilux ASPH", "keywords": ["50mm Summilux ASPH", "Summilux 50mm ASPH"], "must_contain": ["summilux", "50", "asph"]},
    # ── Noctilux ──
    {"label": "50mm Noctilux", "keywords": ["50mm Noctilux", "Noctilux 50mm", "Noctilux"], "must_contain": ["noctilux"]},
    {"label": "75mm Noctilux", "keywords": ["75mm Noctilux", "Noctilux 75mm", "Noctilux 75", "75 Noctilux"], "must_contain": ["noctilux", "75"]},
    # ── Summaron ──
    {"label": "35mm Summaron", "keywords": ["35mm Summaron", "Summaron 35mm", "Summaron"], "must_contain": ["summaron"]},
    # ── 광각 ──
    {"label": "21mm Super Angulon", "keywords": ["21mm Super Angulon", "Super Angulon 21mm", "Super Angulon"], "must_contain": ["angulon", "21"]},
    {"label": "28mm Elmarit", "keywords": ["28mm Elmarit", "Elmarit 28mm", "Elmarit 28"], "must_contain": ["elmarit", "28"]},
    # ── 올드/클래식 ──
    {"label": "50mm Elmar", "keywords": ["50mm Elmar", "Elmar 50mm", "Elmar 50"], "must_contain": ["elmar", "50"]},
    {"label": "50mm Summar", "keywords": ["50mm Summar", "Summar 50mm", "Summar 50"], "must_contain": ["summar", "50"]},
    {"label": "85mm Summarex", "keywords": ["85mm Summarex", "Summarex 85mm", "Summarex"], "must_contain": ["summarex"]},
    {"label": "Hektor", "keywords": ["Hektor"], "must_contain": ["hektor"]},
    {"label": "Elmax", "keywords": ["Elmax"], "must_contain": ["elmax"]},
    # ── APO 라인업 ──
    {"label": "75mm APO-Summicron", "keywords": ["75mm APO Summicron", "APO Summicron 75mm", "APO Summicron 75"], "must_contain": ["apo", "summicron", "75"]},
    {"label": "90mm APO-Summicron", "keywords": ["90mm APO Summicron", "APO Summicron 90mm", "APO Summicron 90"], "must_contain": ["apo", "summicron", "90"]},
    {"label": "100mm APO-Macro-Elmarit", "keywords": ["100mm APO Macro Elmarit", "APO Macro Elmarit 100mm", "APO-Macro-Elmarit"], "must_contain": ["apo", "elmarit", "100"]},
    {"label": "APO-Telyt", "keywords": ["APO Telyt", "APO-Telyt-R"], "must_contain": ["apo", "telyt"]},
]

# ══════════════════════════════════════════════════════
# 세대 태깅 규칙
# ══════════════════════════════════════════════════════
GENERATION_TAGS = [
    {"gen": "1세대", "patterns": [
        r"1st", r"ver\.?1", r"v\.?1\b", r"1세대", r"初期", r"第1", r"1型",
        r"first", r"early", r"초기", r"nickel", r"니켈",
    ]},
    {"gen": "2세대", "patterns": [
        r"2nd", r"ver\.?2", r"v\.?2\b", r"2세대", r"第2", r"2型", r"second",
    ]},
    {"gen": "3세대", "patterns": [
        r"3rd", r"ver\.?3", r"v\.?3\b", r"3세대", r"第3", r"3型",
        r"third", r"asph", r"비구면",
    ]},
    {"gen": "4세대", "patterns": [
        r"4th", r"ver\.?4", r"v\.?4\b", r"4세대", r"第4", r"4型",
    ]},
]

# ══════════════════════════════════════════════════════
# 유틸 함수
# ══════════════════════════════════════════════════════
def detect_generation(name):
    name_upper = name.upper().replace(' ', '') # 판별 시에는 공백을 다 제거하고 비교
    found_tags = []
    slang_dict = {
        '8매': '35mm Summicron 1st (8-Elements)',
        '스틸림': '35mm Summilux 1st Steel Rim',
        '리짓': '50mm Summicron Rigid',
        'DR': '50mm Summicron Dual Range',
        '6매': '35mm Summicron 4th (6-Elements)'
    }
    for slang, full_name in slang_dict.items():
        if slang in name_upper: found_tags.append(full_name)
    gen_patterns = [
        {"gen": "1세대 (v1/E58)", "patterns": [r"1st", r"v\.?1\b", r"1세대", r"E58"]},
        {"gen": "2세대 (v2/E60)", "patterns": [r"2nd", r"v\.?2\b", r"2세대", r"E60"]},
        {"gen": "3세대 (v3/E46)", "patterns": [r"3rd", r"v\.?3\b", r"3세대", r"E46"]},
        {"gen": "4세대 (v4/E39)", "patterns": [r"4th", r"v\.?4\b", r"4세대", r"E39"]},
    ]
    for tag in gen_patterns:
        for pattern in tag["patterns"]:
            if re.search(pattern, name_upper, re.IGNORECASE):
                found_tags.append(tag["gen"])
                break
    return " | ".join(list(set(found_tags))) if found_tags else "세대미상"

def passes_filter(name, must_contain):
    name_lower = " ".join(name.lower().split())
    for word in must_contain:
        w = word.lower()
        # "50" 같은 숫자는 단독 토큰으로만 매칭 (sn.2548 같은 시리얼 넘버 제외)
        if re.match(r"^\d+$", w):
            if not re.search(r"(?<!\d)" + w + r"(?!\d)", name_lower):
                return False
        else:
            if w not in name_lower:
                return False
    return True

def extract_condition_domestic(page):
    """국내 사이트: 상세 페이지에서 XX% 컨디션 추출"""
    try:
        body_text = page.inner_text('body')
        match = re.search(r'제품설명.*?(\d{2,3})%', body_text)
        if match:
            return match.group(1) + "%"
    except:
        pass
    return "정보없음"

def extract_condition_overseas(name):
    """해외 사이트: 상품명에서 컨디션 텍스트 추출"""
    grade_map = {
        "Mint": ["mint", "like new", "s급", "s+급", "s+"],
        "Excellent": ["excellent", "exc", "a급", "a+급"],
        "Good": ["good", "b급", "b+급"],
        "Fair": ["fair", "bargain", "c급"],
    }
    name_lower = name.lower()
    for grade, keywords in grade_map.items():
        for kw in keywords:
            if kw in name_lower:
                return grade
    return "정보없음"

def normalize_price(price_text):
    if not price_text:
        return "문의요망"
    cleaned = price_text.strip()
    call_patterns = ["call", "문의", "상담", "p.o.a", "poa", "contact", "enquire"]
    for pat in call_patterns:
        if pat in cleaned.lower():
            return "문의요망"
    if cleaned in ["0", "0원", "-", ""]:
        return "문의요망"
    return cleaned

def fix_img_url(raw, base):
    if not raw:
        return ""
    if raw.startswith("http://") or raw.startswith("https://"):
        return raw
    if raw.startswith("//"):
        return "https:" + raw
    if raw.startswith("/"):
        return base.rstrip("/") + raw
    return base.rstrip("/") + "/" + raw

def is_ffordes_used(href):
    return bool(re.search(r'/p/(SOR|SH|USED|U)-', href, re.IGNORECASE))

# ══════════════════════════════════════════════════════
# 사이트 정의
# ══════════════════════════════════════════════════════
SITES = [
    {
        "name": "라이카스토어 충무로",
        "search_url": "https://leica-storebando.co.kr/product/search.html?keyword={query}",
        "base": "https://leica-storebando.co.kr",
        "type": "cafe24",
        "lang": "ko",
        "통화": "KRW",
        "condition_type": "domestic",
    },
    {
        "name": "사진집",
        "search_url": "https://www.sazinzibb.com/product/search.html?keyword={query}",
        "base": "https://www.sazinzibb.com",
        "type": "cafe24_all",
        "lang": "ko",
        "통화": "KRW",
        "condition_type": "domestic",
    },
    {
        "name": "장씨카메라",
        "search_url": "https://j-camera.com/product/search.html?keyword={query}",
        "base": "https://j-camera.com",
        "type": "cafe24_all",
        "lang": "ko",
        "통화": "KRW",
        "condition_type": "domestic",
    },
    {
        "name": "신성카메라",
        "search_url": "https://www.scamera.co.kr/product/search.html?keyword={query}",
        "base": "https://www.scamera.co.kr",
        "type": "cafe24_all",
        "lang": "ko",
        "통화": "KRW",
        "condition_type": "domestic",
    },
    {
        "name": "억불카메라",
        "search_url": "https://www.ukbulcamera.co.kr/goods/goods_search.php?keyword={query}&pageNum=80&reSearch=n",
        "base": "https://www.ukbulcamera.co.kr",
        "type": "godo",
        "lang": "ko",
        "통화": "KRW",
        "condition_type": "domestic",
    },
        {
        "name": "Ffordes (영국)",
        "search_url": "https://www.ffordes.com/search?q={query}",
        "base": "https://www.ffordes.com",
        "type": "ffordes_search",
        "lang": "en",
        "통화": "GBP",
        "condition_type": "overseas",
    },
]

# ══════════════════════════════════════════════════════
# 크롤러: 카페24 (충무로 등 국내)
# ══════════════════════════════════════════════════════
def crawl_cafe24(page, site, keyword, label, must_contain):
    results = []
    url = site["search_url"].format(query=keyword.replace(" ", "+"))
    print(f"    URL: {url}")

    try:
        page.goto(url, wait_until="domcontentloaded", timeout=15_000)
    except Exception as e:
        print(f"    ❌ 페이지 로드 실패: {e}")
        return results

    time.sleep(2)

    try:
        page.wait_for_selector("ul.prdList > li", timeout=5_000)
    except:
        print(f"    검색 결과 없음")
        return results

    cards = page.query_selector_all("ul.prdList > li")
    print(f"    └─ {len(cards)}개 검색됨")

    for card in cards:
        try:
            name_el = card.query_selector(".name")
            name = name_el.inner_text().strip() if name_el else ""
            if not name:
                continue
            if "[중고]" not in name and "[위탁]" not in name:
                continue
            if not passes_filter(name, must_contain):
                continue

            # 링크
            link_el = card.query_selector("a")
            href = link_el.get_attribute("href") if link_el else ""
            if href and not href.startswith("http"):
                href = site["base"] + href
            href = href.split("#")[0]

            # 가격
            price_el = card.query_selector(".price")
            price_text = price_el.inner_text().strip() if price_el else ""
            price = normalize_price(price_text)

            # 이미지
            img_el = card.query_selector("img")
            img_url = ""
            if img_el:
                raw = img_el.get_attribute("src") or img_el.get_attribute("data-src") or ""
                img_url = fix_img_url(raw, site["base"])

            # 컨디션 (목록에서 직접 추출)
            card_text = card.inner_text()
            # 카드 텍스트 + 상품명에서 컨디션 추출
            cond_match = re.search(r"(\d{2,3})%", card_text)
            if not cond_match:
                cond_match = re.search(r"(\d{2,3})%", name)
            condition = cond_match.group(1) + "%" if cond_match else "정보없음"

            gen = detect_generation(name)

            results.append({
                "site": site["name"],
    "label": label,
                "상품명": name,
                "세대": gen,
                "컨디션": condition,
                "가격": price,
                "통화": site["통화"],
                "이미지": img_url,
                "링크": href,
            })
            print(f"    ✔  {name[:40]} | {gen} | {condition} | {price}")

        except Exception as e:
            print(f"    ⚠️  카드 파싱 오류: {e}")
            continue

    return results

def crawl_cafe24_all(page, site, keyword, label, must_contain):
    """중고 태그([중고],[위탁]) 없이 전체 상품을 중고로 간주하는 카페24 크롤러"""
    results = []
    url = site["search_url"].format(query=keyword.replace(" ", "+"))
    print(f"    URL: {url}")

    try:
        page.goto(url, wait_until="domcontentloaded", timeout=15_000)
    except Exception as e:
        print(f"    ❌ 페이지 로드 실패: {e}")
        return results

    time.sleep(2)

    try:
        page.wait_for_selector("ul.prdList > li", timeout=5_000)
    except:
        print(f"    검색 결과 없음")
        return results

    cards = page.query_selector_all("ul.prdList > li")
    print(f"    └─ {len(cards)}개 검색됨")

    for card in cards:
        try:
            name_el = card.query_selector(".name")
            name = name_el.inner_text().strip() if name_el else ""
            if not name:
                continue
            if not passes_filter(name, must_contain):
                continue

            link_el = card.query_selector("a")
            href = link_el.get_attribute("href") if link_el else ""
            if href and not href.startswith("http"):
                href = site["base"] + href
            href = href.split("#")[0]

            card_text = card.inner_text()
            # 상품명 줄바꿈 정리
            name = " ".join(name.split())

            # 가격: "원" 포함된 숫자 추출
            price_match = re.search(r"([\d,]+원)", card_text)
            price = price_match.group(1) if price_match else "문의요망"

            img_el = card.query_selector("img")
            img_url = ""
            if img_el:
                raw = img_el.get_attribute("src") or img_el.get_attribute("data-src") or ""
                img_url = fix_img_url(raw, site["base"])

            # 카드 텍스트 + 상품명에서 컨디션 추출
            cond_match = re.search(r"(\d{2,3})%", card_text)
            if not cond_match:
                cond_match = re.search(r"(\d{2,3})%", name)
            condition = cond_match.group(1) + "%" if cond_match else "정보없음"

            gen = detect_generation(name)

            # 품절 감지
            soldout_keywords = ["품절", "sold out", "판매완료", "out of stock"]
            card_text_lower = card_text.lower()
            is_soldout = any(kw in card_text_lower for kw in soldout_keywords)
            # 품절 버튼 확인
            soldout_btn = card.query_selector(".icon-sold-out, .soldout, [class*='soldout'], [class*='sold-out']")
            if soldout_btn:
                is_soldout = True

            results.append({
                "site": site["name"],
    "label": label,
                "상품명": name,
                "세대": gen,
                "컨디션": condition,
                "가격": price,
                "통화": site["통화"],
                "이미지": img_url,
                "링크": href,
                "품절": is_soldout,
            })
            print(f"    {'🚫품절' if is_soldout else '✔ '} {name[:40]} | {gen} | {condition} | {price}")

        except Exception as e:
            print(f"    ⚠️  카드 파싱 오류: {e}")
            continue

    return results

def crawl_godo(page, site, keyword, label, must_contain):
    import re as _re
    results = []
    url = site["search_url"].format(query=keyword.replace(" ", "+"))
    print(f"    URL: {url}")
    try:
        page.goto(url, wait_until="networkidle", timeout=20_000)
    except Exception as e:
        print(f"    ❌ 로드 실패: {e}")
        return results
    time.sleep(5)

    items = page.evaluate("""() => {
        const results = [];
        const strongs = document.querySelectorAll("strong");
        const seen = new Set();
        for (const s of strongs) {
            const name = s.innerText.trim();
            if (!name || name.startsWith("[") || name.includes("검색결과") || name.includes("검색")) continue;
            if (/^[\d,]+$/.test(name)) continue;
            if (/^\d{2,3}-\d{3,4}-\d{4}$/.test(name)) continue;
            const li = s.closest("li");
            if (!li) continue;
            const a = li.querySelector("a");
            const href = a ? a.href : "";
            if (seen.has(href)) continue;
            seen.add(href);
            const img = li.querySelector("img");
            const soldout = !!li.querySelector(".soldout-img");
            results.push({
                name: name,
                text: li.innerText.trim(),
                href: href,
                img: img ? img.src : "",
                soldout: soldout,
            });
        }
        return results;
    }""")

    print(f"    └─ {len(items)}개 상품 발견")
    for item in items:
        try:
            name = item["name"]
            if not name or not passes_filter(name, must_contain):
                continue
            card_text = item["text"]
            price_match = _re.search(r"([\d,]+원)", card_text)
            price = price_match.group(1) if price_match else "문의요망"
            cond_match = _re.search(r"(\d{2,3})%", card_text)
            condition = cond_match.group(1) + "%" if cond_match else "정보없음"
            img_url = fix_img_url(item["img"], site["base"])
            gen = detect_generation(name)
            soldout = item.get("soldout", False)
            results.append({
                "site": site["name"],
    "label": label,
                "상품명": name,
                "세대": gen,
                "컨디션": condition,
                "가격": price,
                "통화": site["통화"],
                "이미지": img_url,
                "링크": item["href"],
                "품절": soldout,
            })
            status = "🚫품절" if soldout else "✔ "
            print(f"    {status} {name[:40]} | {gen} | {condition} | {price}")
        except Exception as e:
            print(f"    ⚠️  파싱 오류: {e}")
    return results

def crawl_ffordes_search(page, site, keyword, label, must_contain):
    """Ffordes 검색 방식 크롤러"""
    results = []
    url = site["search_url"].format(query=keyword.replace(" ", "+"))
    print(f"    URL: {url}")

    try:
        page.goto(url, wait_until="domcontentloaded", timeout=30_000)
    except Exception as e:
        print(f"    ❌ 로드 실패: {e}")
        return results
    time.sleep(2)

    items = page.query_selector_all("div.catGridCol")
    items = [i for i in items if i.query_selector(".priceTxt")]
    print(f"    └─ {len(items)}개 상품 발견")

    for item in items:
        try:
            a_el = item.query_selector("a[href]")
            href = a_el.get_attribute("href") if a_el else ""
            if not href or not is_ffordes_used(href):
                continue
            full_href = site["base"] + href if not href.startswith("http") else href
            name_el = item.query_selector("a.setScroll, .prodName, h2, h3")
            name = name_el.inner_text().strip() if name_el else ""
            if not name:
                name = href.split("/")[-1].replace("-", " ").title()
            if not passes_filter(name, must_contain):
                continue
            price_el = item.query_selector(".priceTxt")
            price = normalize_price(price_el.inner_text().strip() if price_el else "")
            img_el = item.query_selector("img")
            img_url = ""
            if img_el:
                raw = img_el.get_attribute("src") or img_el.get_attribute("data-src") or ""
                img_url = fix_img_url(raw, site["base"])
            condition = extract_condition_overseas(name)
            gen = detect_generation(name)
            results.append({
                "site": site["name"],
    "label": label,
                "상품명": name,
                "세대": gen,
                "컨디션": condition,
                "가격": price,
                "통화": site["통화"],
                "이미지": img_url,
                "링크": full_href,
            })
            print(f"    ✔  {name[:40]} | {gen} | {condition} | {price}")
        except Exception as e:
            print(f"    ⚠️  파싱 오류: {e}")
            continue

    return results

def crawl_ffordes(page, site, label, must_contain):
    results = []

    for base_url in site["category_urls"]:
        # 초기 로드 (retry 포함)
        loaded = False
        for attempt in range(3):
            try:
                page.goto(base_url, wait_until="domcontentloaded", timeout=30_000)
                loaded = True
                break
            except Exception as e:
                print(f"    ⚠️  로드 재시도 {attempt+1}/3: {e}")
                time.sleep(3)
        if not loaded:
            print(f"    ❌ {base_url} 로드 실패, 건너뜀")
            continue
        time.sleep(2)

        page_num = 1
        while True:
            # 1페이지는 이미 로드됨, 2페이지부터 클릭
            if page_num > 1:
                next_btn = page.query_selector("a.next")
                next_href = next_btn.get_attribute("href") if next_btn else ""
                if not next_btn or "javascript" in next_href or not next_href:
                    print(f"    └─ 마지막 페이지, 중단")
                    break
                # 클릭 전 첫 상품 href로 페이지 변경 감지
                first_item = page.query_selector("div.catGridCol a[href]")
                prev_first = first_item.get_attribute("href") if first_item else ""
                next_btn.click()
                # 콘텐츠가 바뀔 때까지 최대 5초 대기
                for _ in range(10):
                    time.sleep(0.5)
                    fi = page.query_selector("div.catGridCol a[href]")
                    if fi and fi.get_attribute("href") != prev_first:
                        break
                else:
                    print(f"    └─ 마지막 페이지, 중단")
                    break

            print(f"    페이지 {page_num}: {page.url}")

            items = page.query_selector_all("div.catGridCol")
            items = [i for i in items if i.query_selector(".priceTxt")]

            if not items:
                print(f"    └─ 상품 없음, 중단")
                break

            print(f"    └─ {len(items)}개 상품 발견")

            for item in items:
                try:
                    a_el = item.query_selector("a[href]")
                    href = a_el.get_attribute("href") if a_el else ""
                    if not href or not is_ffordes_used(href):
                        continue
                    full_href = site["base"] + href if not href.startswith("http") else href
                    name_el = item.query_selector("a.setScroll, .prodName, h2, h3")
                    name = name_el.inner_text().strip() if name_el else ""
                    if not name:
                        name = href.split("/")[-1].replace("-", " ").title()
                    if not passes_filter(name, must_contain):
                        continue
                    price_el = item.query_selector(".priceTxt")
                    price_text = price_el.inner_text().strip() if price_el else ""
                    price = normalize_price(price_text)
                    img_el = item.query_selector("img")
                    img_url = ""
                    if img_el:
                        raw = img_el.get_attribute("src") or img_el.get_attribute("data-src") or ""
                        img_url = fix_img_url(raw, site["base"])
                    condition = extract_condition_overseas(name)
                    gen = detect_generation(name)
                    results.append({
                        "site": site["name"],
    "label": label,
                        "상품명": name,
                        "세대": gen,
                        "컨디션": condition,
                        "가격": price,
                        "통화": site["통화"],
                        "이미지": img_url,
                        "링크": full_href,
                    })
                    print(f"    ✔  {name[:40]} | {gen} | {condition} | {price}")
                except Exception as e:
                    print(f"    ⚠️  파싱 오류: {e}")
                    continue

            page_num += 1

    return results

# ══════════════════════════════════════════════════════
# 메인 실행
# ══════════════════════════════════════════════════════
def push_to_github():
    import subprocess, os
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        print("❌ GITHUB_TOKEN 환경변수가 없어요!")
        return

    repo = "loseme85/camerabridge"
    remote = f"https://{token}@github.com/{repo}.git"

    cmds = [
        ["git", "add", "results.json"],
        ["git", "commit", "-m", "Auto update results.json"],
        ["git", "push", remote, "main"],
    ]

    for cmd in cmds:
        result = subprocess.run(cmd, capture_output=True, text=True)
        combined = result.stdout + result.stderr
        if result.returncode != 0 and "nothing to commit" not in combined and "nothing added to commit" not in combined:
            print(f"❌ {' '.join(cmd)}: {result.stderr}")
            return

    print("✅ GitHub push 완료! Vercel 자동 배포 시작됨")


def crawl_site(site):
    """단일 사이트 크롤링 - 병렬 처리용"""
    import time as _time
    from playwright.sync_api import sync_playwright

    site_results = []

    # 억불카메라는 headless=False 필요
    is_godo = site["type"] == "godo"

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=not is_godo)
        page = browser.new_page()

        # 리소스 차단 (CSS/폰트/광고, 이미지는 허용)
        def block_resources(route):
            if route.request.resource_type in ["stylesheet", "font"]:
                route.abort()
            elif any(x in route.request.url for x in ["google-analytics", "googletagmanager", "facebook", "ads", "tracker"]):
                route.abort()
            else:
                route.continue_()
        page.route("**/*", block_resources)
        page.set_default_timeout(15000)

        print(f"\n{'='*50}")
        print(f"▶ {site['name']} 수집 시작")
        print(f"{'='*50}")

        seen_links = set()

        for search_item in SEARCH_ITEMS:
            label = search_item["label"]
            must_contain = search_item["must_contain"]
            keywords = search_item["keywords"]
            print(f"\n  🔍 필터: '{label}'")

            seen_in_item = set()
            for keyword in keywords:
                try:
                    if site["type"] == "cafe24":
                        res = crawl_cafe24(page, site, keyword, label, must_contain)
                    elif site["type"] == "cafe24_all":
                        res = crawl_cafe24_all(page, site, keyword, label, must_contain)
                    elif site["type"] == "ffordes":
                        res = crawl_ffordes(page, site, label, must_contain)
                    elif site["type"] == "godo":
                        res = crawl_godo(page, site, keyword, label, must_contain)
                    elif site["type"] == "ffordes_search":
                        res = crawl_ffordes_search(page, site, keyword, label, must_contain)
                    else:
                        res = []
                    for r in res:
                        if r["링크"] not in seen_in_item:
                            seen_in_item.add(r["링크"])
                            if r["링크"] not in seen_links:
                                seen_links.add(r["링크"])
                                site_results.append(r)
                except Exception as e:
                    print(f"    ❌ {keyword} 오류: {e}")
                _time.sleep(0.3)

        browser.close()

    print(f"\n  ✅ {site['name']}: {len(site_results)}개 수집 완료")
    return site_results


def crawl_all():
    import time as _time
    from concurrent.futures import ThreadPoolExecutor, as_completed

    start_time = _time.time()
    all_results = []

    # 억불카메라(godo)는 별도 순차 처리 (headless=False 필요)
    parallel_sites = [s for s in SITES if s["type"] != "godo"]
    godo_sites = [s for s in SITES if s["type"] == "godo"]

    print(f"🚀 병렬 크롤링 시작 ({len(parallel_sites)}개 사이트 동시 처리)")
    print(f"⏳ 억불카메라 ({len(godo_sites)}개)는 별도 처리")

    # 병렬 처리
    with ThreadPoolExecutor(max_workers=len(parallel_sites)) as executor:
        futures = {executor.submit(crawl_site, site): site for site in parallel_sites}
        for future in as_completed(futures):
            site = futures[future]
            try:
                results = future.result()
                all_results.extend(results)
            except Exception as e:
                print(f"❌ {site['name']} 오류: {e}")

    # 억불카메라 순차 처리
    for site in godo_sites:
        results = crawl_site(site)
        all_results.extend(results)

    # 전체 중복 제거
    seen = set()
    unique_results = []
    for r in all_results:
        if r["링크"] not in seen:
            seen.add(r["링크"])
            unique_results.append(r)

    elapsed = _time.time() - start_time

    with open("results.json", "w", encoding="utf-8") as f:
        json.dump(unique_results, f, ensure_ascii=False, indent=2)

    print(f"\n{'='*50}")
    print(f"✅ 최종 {len(unique_results)}개 → results.json 저장 완료")
    print(f"⏱️  총 소요 시간: {elapsed:.1f}초 ({elapsed/60:.1f}분)")
    print(f"{'='*50}")
    for r in unique_results:
        print(f"\n  📷 [{r['세대']}] {r['상품명']}")
        print(f"     💰 {r['가격']} {r['통화']} | 컨디션: {r['컨디션']}")
        print(f"     🖼  {r['이미지'] or '이미지 없음'}")
        print(f"     🔗 {r['링크']}")

if __name__ == "__main__":
    crawl_all()
    push_to_github()

# ══════════════════════════════════════════════════════
# GitHub 자동 Push
# ══════════════════════════════════════════════════════
