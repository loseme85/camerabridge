from playwright.sync_api import sync_playwright
import time
import json
import re
import argparse
import random
import os

# ── 실행 모드 파싱 ──
parser = argparse.ArgumentParser(description='Camera Bridge Crawler')
parser.add_argument('--mock', action='store_true', help='로컬 HTML 파일로 테스트')
parser.add_argument('--live', action='store_true', help='실제 사이트 크롤링 (기본)')
parser.add_argument('--site', type=str, help='특정 사이트만 크롤링 (예: 사진집, Ffordes)')
args, _ = parser.parse_known_args()
MOCK_MODE = args.mock
SITE_FILTER = args.site
FFORDES_ONLY = SITE_FILTER and 'ffordes' in SITE_FILTER.lower()

# ── User-Agent 풀 ──
USER_AGENTS = [
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:122.0) Gecko/20100101 Firefox/122.0",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
]

# ══════════════════════════════════════════════════════
# 검색 아이템 정의
# ══════════════════════════════════════════════════════
SEARCH_ITEMS = [
    # ── 35mm Summicron 세대별 ──
    {"label": "35mm Summicron 1st (8매옥)", "keywords": ["Summicron 35", "35cron", "35mm Summicron"], "must_contain": ["summicron", "35"]},
    {"label": "35mm Summicron ASPH",        "keywords": ["Summicron 35 ASPH", "35mm Summicron ASPH"], "must_contain": ["summicron", "35", "asph"]},
    # ── 35mm Summilux 세대별 ──
    {"label": "35mm Summilux Steel Rim",    "keywords": ["Summilux 35", "35lux", "35mm Summilux"], "must_contain": ["summilux", "35"]},
    {"label": "35mm Summilux ASPH",         "keywords": ["Summilux 35 ASPH", "35mm Summilux ASPH"], "must_contain": ["summilux", "35", "asph"]},
    {"label": "35mm Summilux FLE",          "keywords": ["Summilux 35 FLE", "35mm Summilux FLE"], "must_contain": ["summilux", "35", "fle"]},
    {"label": "35mm Summilux AA",           "keywords": ["Summilux 35 Aspherical", "35mm Summilux Aspherical"], "must_contain": ["summilux", "35", "aspherical"]},
    # ── 50mm Summicron ──
    {"label": "50mm Summicron", "keywords": ["50mm Summicron", "Summicron 50mm", "50cron"], "must_contain": ["summicron", "50"]},
    {"label": "50mm Summicron DR", "keywords": ["50mm Summicron DR", "Summicron DR", "Dual Range"], "must_contain": ["summicron", "50"]},
    {"label": "50mm APO-Summicron", "keywords": ["50mm APO Summicron", "APO Summicron 50mm", "APO Summicron"], "must_contain": ["apo", "summicron", "50"]},
    # ── 50mm Summilux ──
    {"label": "50mm Summilux", "keywords": ["50mm Summilux", "Summilux 50mm", "50lux"], "must_contain": ["summilux", "50"]},
    {"label": "50mm Summilux ASPH", "keywords": ["50mm Summilux ASPH", "Summilux 50mm ASPH"], "must_contain": ["summilux", "50", "asph"]},
    # ── Noctilux ──
    {"label": "50mm Noctilux f0.95", "keywords": ["Noctilux f0.95", "Noctilux ASPH", "50mm Noctilux"], "must_contain": ["noctilux", "0.95"]},
    {"label": "50mm Noctilux f1.0", "keywords": ["Noctilux f1.0", "Noctilux 50mm", "50mm Noctilux f1"], "must_contain": ["noctilux", "1.0"]},
    {"label": "50mm Noctilux f1.2", "keywords": ["Noctilux f1.2", "Noctilux 50mm f1.2"], "must_contain": ["noctilux", "1.2"]},
    {"label": "75mm Noctilux f1.25", "keywords": ["75mm Noctilux", "Noctilux 75mm", "Noctilux 75"], "must_contain": ["noctilux", "75"]},
    # ── 15mm ──
    {"label": "Hologon 15mm f8",         "keywords": ["Hologon 15", "Hologon"],              "must_contain": ["hologon"]},
    # ── 21mm 세대별 ──
    {"label": "21mm Super-Angulon f4",   "keywords": ["Super Angulon 21", "Super-Angulon 21mm f4"],  "must_contain": ["angulon", "21"]},
    {"label": "21mm Super-Angulon f3.4", "keywords": ["Super Angulon 21", "Super-Angulon 21mm"],     "must_contain": ["angulon", "21", "3.4"]},
    {"label": "21mm Elmarit f2.8",       "keywords": ["Elmarit 21", "21mm Elmarit"],                "must_contain": ["elmarit", "21"]},
    {"label": "21mm Elmarit ASPH",       "keywords": ["Elmarit 21 ASPH", "21mm Elmarit ASPH"],      "must_contain": ["elmarit", "21", "asph"]},
    {"label": "21mm Summilux ASPH",      "keywords": ["Summilux 21", "21mm Summilux"],              "must_contain": ["summilux", "21"]},
    # ── 24mm ──
    {"label": "24mm Elmarit ASPH",       "keywords": ["Elmarit 24", "24mm Elmarit"],                "must_contain": ["elmarit", "24"]},
    # ── 28mm 세대별 ──
    {"label": "28mm Elmarit 1~4세대",    "keywords": ["Elmarit 28", "28mm Elmarit"],                "must_contain": ["elmarit", "28"]},
    {"label": "28mm Elmarit ASPH",       "keywords": ["Elmarit 28 ASPH", "28mm Elmarit ASPH"],      "must_contain": ["elmarit", "28", "asph"]},
    {"label": "28mm Summicron ASPH",     "keywords": ["Summicron 28", "28mm Summicron"],            "must_contain": ["summicron", "28"]},
    # ── 35mm 올드 ──
    {"label": "35mm Elmar",              "keywords": ["Elmar 35", "35mm Elmar"],                    "must_contain": ["elmar", "35"]},
    {"label": "35mm Summaron",           "keywords": ["Summaron 35", "35mm Summaron", "Summaron"],   "must_contain": ["summaron"]},
    # ── 올드/클래식 ──
    {"label": "50mm Elmar", "keywords": ["50mm Elmar", "Elmar 50mm", "Elmar 50"], "must_contain": ["elmar", "50"]},
    {"label": "50mm Summar", "keywords": ["50mm Summar", "Summar 50mm", "Summar 50"], "must_contain": ["summar", "50"]},
    {"label": "85mm Summarex", "keywords": ["85mm Summarex", "Summarex 85mm", "Summarex"], "must_contain": ["summarex"]},
    {"label": "Hektor", "keywords": ["Hektor"], "must_contain": ["hektor"]},
    {"label": "Elmax", "keywords": ["Elmax"], "must_contain": ["elmax"]},
    # ── 바디 ──
    {"label": "Leica M3", "keywords": ["Leica M3", "M3 Body", "M3 바디"], "must_contain": ["leica", "m3"]},
    {"label": "Leica M2", "keywords": ["Leica M2", "M2 Body"], "must_contain": ["leica", "m2"]},
    {"label": "Leica M4", "keywords": ["Leica M4", "M4 Body"], "must_contain": ["leica", "m4"]},
    {"label": "Leica M6", "keywords": ["Leica M6", "M6 Body", "M6 TTL"], "must_contain": ["leica", "m6"]},
    {"label": "Leica M7", "keywords": ["Leica M7", "M7 Body"], "must_contain": ["leica", "m7"]},
    {"label": "Leica MP", "keywords": ["Leica MP", "MP Body"], "must_contain": ["leica", "mp", "body"]},
    {"label": "Leica M-A", "keywords": ["Leica MA", "M-A Body"], "must_contain": ["m-a"]},
    {"label": "Leica M8", "keywords": ["Leica M8", "M8 Body"], "must_contain": ["leica", "m8"]},
    {"label": "Leica M9", "keywords": ["Leica M9", "M9 Body", "M9-P"], "must_contain": ["leica", "m9"]},
    {"label": "Leica M10", "keywords": ["Leica M10", "M10 Body", "M10-P", "M10-R"], "must_contain": ["leica", "m10"]},
    {"label": "Leica M11", "keywords": ["Leica M11", "M11 Body", "M11-P"], "must_contain": ["leica", "m11"]},
    {"label": "Leica M240", "keywords": ["Leica M240", "M 240", "Typ 240"], "must_contain": ["leica", "240"]},
    # ── APO 라인업 ──
    {"label": "75mm APO-Summicron", "keywords": ["75mm APO Summicron", "APO Summicron 75mm", "APO Summicron 75"], "must_contain": ["apo", "summicron", "75"]},
    {"label": "90mm APO-Summicron", "keywords": ["90mm APO Summicron", "APO Summicron 90mm", "APO Summicron 90"], "must_contain": ["apo", "summicron", "90"]},
    {"label": "100mm APO-Macro-Elmarit", "keywords": ["100mm APO Macro Elmarit", "APO Macro Elmarit 100mm", "APO-Macro-Elmarit"], "must_contain": ["apo", "elmarit", "100"]},
    {"label": "APO-Telyt", "keywords": ["APO Telyt", "APO-Telyt-R"], "must_contain": ["apo", "telyt"]},
    # ── Barnack 바디 ──
    {"label": "Leica I", "keywords": ["Leica I", "Leica Standard"], "must_contain": ["leica"], "category": "Body", "barnack": True},
    {"label": "Leica II", "keywords": ["Leica II", "Leica IIa", "Leica IIb", "Leica IIc"], "must_contain": ["leica"], "category": "Body", "barnack": True},
    {"label": "Leica III", "keywords": ["Leica III", "Leica IIIa", "Leica IIIb", "Leica IIIc", "Leica IIIf", "Leica IIIg"], "must_contain": ["leica"], "category": "Body", "barnack": True},
    {"label": "Leica IIf", "keywords": ["Leica IIf", "Leica If"], "must_contain": ["leica"], "category": "Body", "barnack": True},
    # ── R System 바디 ──
    {"label": "Leica R3", "keywords": ["Leica R3", "R3 Body"], "must_contain": ["leica", "r3"]},
    {"label": "Leica R4", "keywords": ["Leica R4", "R4 Body"], "must_contain": ["leica", "r4"]},
    {"label": "Leica R5", "keywords": ["Leica R5", "R5 Body"], "must_contain": ["leica", "r5"]},
    {"label": "Leica R6", "keywords": ["Leica R6", "R6 Body", "R6.2"], "must_contain": ["leica", "r6"]},
    {"label": "Leica R7", "keywords": ["Leica R7", "R7 Body"], "must_contain": ["leica", "r7"]},
    {"label": "Leica R8", "keywords": ["Leica R8", "R8 Body"], "must_contain": ["leica", "r8"]},
    {"label": "Leica R9", "keywords": ["Leica R9", "R9 Body"], "must_contain": ["leica", "r9"]},
    # ── R System 렌즈 ──
    {"label": "35mm Summilux-R", "keywords": ["35mm Summilux-R", "Summilux-R 35mm"], "must_contain": ["summilux", "r", "35"]},
    {"label": "50mm Summicron-R", "keywords": ["50mm Summicron-R", "Summicron-R 50mm"], "must_contain": ["summicron", "r", "50"]},
    {"label": "90mm Summicron-R", "keywords": ["90mm Summicron-R", "Summicron-R 90mm"], "must_contain": ["summicron", "r", "90"]},
    # ── P&S (Compact) ──
    # Minilux / CM
    {"label": "Leica Minilux",      "keywords": ["Leica Minilux", "Minilux Zoom"],          "must_contain": ["minilux"]},
    {"label": "Leica CM",           "keywords": ["Leica CM", "Leica CM Zoom"],               "must_contain": ["leica", "cm"]},
    # C 시리즈 (C1/C2/C3/C11)
    {"label": "Leica C1",           "keywords": ["Leica C1"],                                "must_contain": ["leica", "c1"]},
    {"label": "Leica C2",           "keywords": ["Leica C2"],                                "must_contain": ["leica", "c2"]},
    {"label": "Leica C3",           "keywords": ["Leica C3"],                                "must_contain": ["leica", "c3"]},
    {"label": "Leica C11",          "keywords": ["Leica C11"],                               "must_contain": ["leica", "c11"]},
    # C-LUX 시리즈
    {"label": "Leica C-LUX 1",      "keywords": ["C-LUX 1", "C-lux 1"],                     "must_contain": ["c-lux", "1"]},
    {"label": "Leica C-LUX 2",      "keywords": ["C-LUX 2", "C-lux 2"],                     "must_contain": ["c-lux", "2"]},
    {"label": "Leica C-LUX 3",      "keywords": ["C-LUX 3", "C-lux 3"],                     "must_contain": ["c-lux", "3"]},
    {"label": "Leica C Typ 112",    "keywords": ["Leica C Typ 112", "Typ 112"],              "must_contain": ["leica", "112"]},
    # D-LUX 시리즈
    {"label": "Leica D-LUX 2",      "keywords": ["D-LUX 2"],                                 "must_contain": ["d-lux", "2"]},
    {"label": "Leica D-LUX 3",      "keywords": ["D-LUX 3"],                                 "must_contain": ["d-lux", "3"]},
    {"label": "Leica D-LUX 4",      "keywords": ["D-LUX 4"],                                 "must_contain": ["d-lux", "4"]},
    {"label": "Leica D-LUX 5",      "keywords": ["D-LUX 5"],                                 "must_contain": ["d-lux", "5"]},
    {"label": "Leica D-LUX 6",      "keywords": ["D-LUX 6"],                                 "must_contain": ["d-lux", "6"]},
    {"label": "Leica D-LUX Typ109", "keywords": ["D-LUX Typ 109", "D-LUX 109"],             "must_contain": ["d-lux", "109"]},
    # V-LUX 시리즈
    {"label": "Leica V-LUX 1",      "keywords": ["V-LUX 1"],                                 "must_contain": ["v-lux", "1"]},
    {"label": "Leica V-LUX 2",      "keywords": ["V-LUX 2"],                                 "must_contain": ["v-lux", "2"]},
    {"label": "Leica V-LUX 3",      "keywords": ["V-LUX 3"],                                 "must_contain": ["v-lux", "3"]},
    {"label": "Leica V-LUX 4",      "keywords": ["V-LUX 4"],                                 "must_contain": ["v-lux", "4"]},
    {"label": "Leica V-LUX Typ114", "keywords": ["V-LUX Typ 114", "V-LUX 114"],             "must_contain": ["v-lux", "114"]},
    # Mini 시리즈
    {"label": "Leica Mini",         "keywords": ["Leica Mini"],                              "must_contain": ["leica", "mini"]},
    {"label": "Leica Z2X",          "keywords": ["Leica Z2X", "Z2X"],                        "must_contain": ["z2x"]},
    {"label": "Leica AF-C1",        "keywords": ["Leica AF-C1", "AF-C1"],                    "must_contain": ["af-c1"]},
    # X / T 시스템
    {"label": "Leica X Vario",      "keywords": ["Leica X Vario", "X Vario", "Typ 107"],    "must_contain": ["leica", "x", "vario"]},
    {"label": "Leica X Typ113",     "keywords": ["Leica X Typ 113", "X Typ 113"],           "must_contain": ["leica", "x", "113"]},
    {"label": "Leica T",            "keywords": ["Leica T", "Typ 701"],                      "must_contain": ["leica", "701"]},
    # Q 시리즈
    {"label": "Leica Q2",           "keywords": ["Leica Q2", "Q2 Monochrom"],               "must_contain": ["leica", "q2"]},
    {"label": "Leica Q3",           "keywords": ["Leica Q3"],                               "must_contain": ["leica", "q3"]},
]

# ══════════════════════════════════════════════════════
# 완전 제외 브랜드 (크롤링 자체를 하지 않음)
# 라이카와 전혀 무관한 타 시스템 카메라/렌즈
# ══════════════════════════════════════════════════════
NON_LEICA_BRANDS = [
    # ── 일본 카메라 브랜드 ──
    'nikon', 'canon', 'sony', 'fuji', 'fujifilm', 'olympus', 'panasonic',
    'pentax', 'minolta', 'ricoh', 'konica', 'yashica', 'polaroid', 'argus',
    # ── 니콘 렌즈 ──
    'nikkor', 'w-nikkor', 'nikon s',
    # ── 독일/유럽 비라이카 ──
    'contax', 'contarex', 'rollei', 'rolleiflex', 'rolleicord',
    'rodenstock', 'schneider',
    # ── 중국 필름 카메라 ──
    'seagull', '갈매기',
    # ── 기타 완전 타 시스템 ──
    'hasselblad', 'mamiya', 'bronica', 'graflex',
]

# ══════════════════════════════════════════════════════
# 라이카 마운트 호환 써드파티 브랜드
# 크롤링은 하되 "3rd Party"로 태깅
# M마운트 / L39 호환 렌즈들
# ══════════════════════════════════════════════════════
THIRD_PARTY_BRANDS = [
    # ── 보이그랜더 / 코시나 계열 (M마운트) ──
    'voigtlander', 'nokton', 'ultron', 'color-skopar', 'heliar',
    # ── 자이스 ZM 계열 (M마운트) ──
    'zeiss', 'biogon', 'distagon', 'c-sonnar', 'planar zm',
    # ── 중국 M마운트 써드파티 ──
    'ttartisan', '7artisans', '7 artisans',
    'thypoch', 'leeworks',
    'meike', 'kamlan', 'pergear',
    'laowa', 'mitakon', 'sun optics', 'funleader', 'handevision',
    'kolari', 'mandler',
    'light lens lab',
    'polar',  # Polar M마운트 렌즈 (Polar M 35mm 등)
]

# ══════════════════════════════════════════════════════
# 유틸 함수
# ══════════════════════════════════════════════════════
def detect_mount(name):
    """마운트 타입 자동 분류 - 이중 마운트(LTM) 지원"""
    n = name.upper()

    # [중고], [위탁], [매장진열] 등 접두어 제거
    import re as _re
    n = _re.sub(r'^\[[^\]]+\]\s*', '', n).strip()

    # M 바디 단독 표기 (접두어 제거 후 M으로 시작하는 경우) - R보다 먼저 체크
    if re.match(r'^M[2-9]\b|^M1[0-9]\b|^MP\b|^M-A\b|^MA\b|^M-D\b|^M-E\b|^M-P\b|^M240\b|^M MONOCHROM\b|^MONOCHROM\b', n):
        return "M"

    # ── Leicaflex (필름 SLR) → R 마운트 ──
    if 'LEICAFLEX' in n:
        return "R"

    # R-mount (가장 먼저 - -R 표기가 명확)
    if any(x in n for x in ['-R ','-R/','SUMMILUX-R','SUMMICRON-R','ELMARIT-R',
                              'ELMAR-R','TELYT-R','LEICA R3','LEICA R4','LEICA R5',
                              'LEICA R6','LEICA R7','LEICA R8','LEICA R9']):
        return "R"
    # R 마운트 - "R 50/", "R 35/", "R 28/" 등 충무로식 표기
    if any(x in (' ' + n) for x in [' R 50',' R 35',' R 28',' R 21',' R 24',
                                      ' R 60',' R 70',' R 80',' R 90',' R 100',
                                      ' R 16',' R 19','ROM ']):
        return "R"
    # SL 마운트 (디지털 미러리스 SL/SL2 시스템)
    if any(x in n for x in ['SL2','SL3','LEICA SL','VARIO-ELMARIT-SL','APO-VARIO-ELMARIT-SL',
                              'SUMMILUX-SL','SUMMICRON-SL','ELMARIT-SL','APO-SUMMICRON-SL',
                              ' SL ',' SL/','SL 24','SL 35','SL 50','SL 75','SL 90']):
        return "SL"
    # TL 마운트
    if any(x in n for x in ['LEICA TL','LEICA CL',' TL ',' TL/',' TL2','TL ',
                              'SUMMILUX-TL','SUMMICRON-TL','ELMARIT-TL','SUPER-VARIO-ELMAR-TL']):
        return "SL"
    # Q 시스템
    if any(x in n for x in ['LEICA Q','Q2 ','Q3 ',' Q2',' Q3']):
        return "Q"
    # L-MOUNT 명시
    if 'L-MOUNT' in n:
        return "SL"

    # Leica L 마운트 (나사마운트 렌즈/바디)
    # LTM 단독 (어댑터만) vs 렌즈/바디와 함께 있는 경우 구분
    LENS_BODY_KW = [
        'SUMMICRON','SUMMILUX','NOCTILUX','ELMARIT','ELMAR','SUMMAR',
        'HEKTOR','XENON','SUMMAREX','TELYT','ANGULON','HOLOGON',
        'LEICA I ','LEICA II','LEICA III','LEICA IF','LEICA IIF',
        'LEITZ WETZLAR','ERNST LEITZ',
        '3.5CM','7.3CM','9CM ','13.5CM',
    ]
    l_kw = ['L39','M39','SCREW','나사',
            ' L 50/',' L 35/',' L 28/',' L 21/',' L 90/',' L 135/',
            ' L50/',' L35/',' L28/',' L90/']

    # LTM 키워드가 있을 때: 렌즈/바디 키워드도 있으면 L마운트, 없으면 어댑터(Unknown)
    has_ltm = 'LTM' in n
    has_lens_body = any(x in n for x in LENS_BODY_KW)
    has_l_kw = any(x in n for x in l_kw)

    if has_ltm and not has_lens_body:
        return "Unknown"  # LTM 단독 어댑터 → detect_category에서 Accessory로

    if has_ltm and has_lens_body:
        return "L"  # LTM + 렌즈/바디 → L마운트

    # Summar/Summarit 구형 나사마운트 - SUMMARIT-M 제외
    if 'SUMMAR' in n and 'SUMMARIT-M' not in n and 'SUMMARON' not in n:
        return "L"

    if has_l_kw:
        return "L"

    # 상품명에 'LEICA L' 명시된 경우 → L마운트 우선
    if 'LEICA L' in n and 'LEICA L-MOUNT' not in n:
        return "L"

    # Ffordes 스타일: 끝에 " M BLACK", " M CHROME" 등
    if re.search(r'\bM\s+(BLACK|CHROME|SILVER|ANTHRACITE|BODY)$', n):
        return "M"
    if re.search(r'\bM\s+\d', n):  # "M 50mm", "M 28mm" 등
        return "M"

    # M-mount (확장)
    if any(x in n for x in [
        'SUMMICRON','SUMMILUX','NOCTILUX','ELMARIT','ELMAR',
        'SUMMARON','SUPER-ANGULON','SUMMAREX','HEKTOR','XENON',
        'SUMMARIT-M','SUMMARIT-S',
        'LEICA M',' M3',' M4',' M5',' M6',' M7',' M8',
        ' M9',' M10',' M11','LEICA MP','LEICA MA','LEICA M-A',
        '-M ','-M/','APO-SUMMICRON','APO-TELYT','APO-MACRO',
    ]):
        return "M"

    # ── Visoflex (M 바디 액세서리) ──
    if 'VISOFLEX' in n and 'VISOFLEX2' not in n and 'VISOFLEX 2' not in n:
        return "M"

    # ── Leica C 렌즈 (CL/SL 마운트) ──
    if re.match(r'LEICA C \d+', n) or re.match(r'CL \d+', n):
        return "SL"

    # ── Compact (디지털 컴팩트/미러리스 바디) ──
    _compact_kw = [
        'D-LUX','DLUX','C-LUX','CLUX','DIGILUX',
        'LEICA X1','LEICA X2','LEICA X ','LEICA X-','X TYP','X(TYP','X-U ',
        'X VARIO','X-VARIO','V-LUX','VLUX',
        'LEICA TL','LEICA CL','SOFORT','LEICA T ','DIGILUX',
        'D-LUX 3','D-LUX 4','D-LUX 5','D-LUX 6','D-LUX 7','D-LUX 8',
        'D-LUX TYP','D-LUX (TYP',
    ]
    if any(x in n for x in _compact_kw):
        return "Compact"

    # ── PNS (필름 자동카메라) ──
    _pns_kw = [
        'MINILUX','CM ZOOM','LEICA CM ','LEICA C1 ','LEICA C2 ','AF-C1',
        'LEICA MINI ','LEICA C ZOOM','C2 ZOOM','CM-ZOOM',
    ]
    if any(x in n for x in _pns_kw):
        return "PNS"

    # ── S 마운트 (중형 시스템) ──
    _s_kw = [
        'LEICA S ','LEICA S(','S TYP 006','S TYP 007','SUMMARIT-S',
        'VARIO-ELMAR-S','SUPER-ELMAR-S','ELMAR-S','APO-MACRO-SUMMARIT-S',
        ' S 35/',' S 45/',' S 70/',' S 120/',' S 180/',
    ]
    if any(x in n for x in _s_kw):
        return "S"

    return "Unknown"

def resolve_mount_from_category(mount, category):
    """mount가 Unknown이고 category가 Accessory면 Accessory 반환"""
    if mount == "Unknown" and category == "Accessory":
        return "Accessory"
    return mount

def detect_noctilux_gen(name):
    """Noctilux 전용 세대 감지"""
    n = name.lower()
    if 'f1.2' in n or '1.2' in n:
        return 'v1 (f1.2)'
    if 'f0.95' in n or '0.95' in n:
        return 'v4 (f0.95 ASPH)'
    if 'f1.0' in n or '1.0' in n:
        # E58 vs E60 구분
        if 'e58' in n or 'e 58' in n:
            return 'v2/v3 (f1.0 E58)'
        if 'e60' in n or 'e 60' in n:
            return 'v2/v3 (f1.0 E60)'
        return 'v2/v3 (f1.0)'
    return None

def detect_generation(name):
    name_upper = name.upper().replace(' ', '')
    found_tags = []
    slang_dict = {
        '8매': '35mm Summicron 1st (8-Elements)',
        '스틸림': '35mm Summilux 1st Steel Rim',
        '리짓': '50mm Summicron Rigid',
        'DR': '50mm Summicron Dual Range',
        '6매': '35mm Summicron 4th (6-Elements)'
    }
    for slang, full_name in slang_dict.items():
        if slang in name_upper:
            found_tags.append(full_name)
    # Noctilux 전용 세대 감지
    if 'NOCTILUX' in name_upper:
        nocti_gen = detect_noctilux_gen(name)
        if nocti_gen:
            found_tags.append(nocti_gen)
    gen_patterns = [
        {"gen": "1세대 (v1)", "patterns": [r"1st", r"v\.?1", r"1세대", r"E58"]},
        {"gen": "2세대 (v2)", "patterns": [r"2nd", r"v\.?2", r"2세대", r"E60"]},
        {"gen": "3세대 (v3)", "patterns": [r"3rd", r"v\.?3", r"3세대", r"E46"]},
        {"gen": "4세대 (v4)", "patterns": [r"4th", r"v\.?4", r"4세대", r"E39"]},
        {"gen": "5세대 (v5)", "patterns": [r"5th", r"v\.?5", r"5세대"]},
    ]
    for tag in gen_patterns:
        for pattern in tag["patterns"]:
            if re.search(pattern, name_upper, re.IGNORECASE):
                found_tags.append(tag["gen"])
                break
    return " | ".join(list(set(found_tags))) if found_tags else "세대미상"

def detect_system(name):
    """상품명에서 시스템 분류"""
    n = name.upper()
    # R System (M보다 먼저 체크)
    if any(x in n for x in [
        'SUMMILUX-R', 'SUMMICRON-R', 'ELMARIT-R', 'ELMAR-R', 'APO-MACRO-ELMARIT-R',
        'VARIO-ELMARIT-R', 'APO-TELYT-R', 'TELYT-R', 'SUPER-ELMAR-R',
        'R3 ', 'R4 ', 'R5 ', 'R6 ', 'R7 ', 'R8 ', 'R9 ', ' R3', ' R4', ' R5', ' R6',
        ' R7', ' R8', ' R9', 'LEICA R3', 'LEICA R4', 'LEICA R5', 'LEICA R6', 'LEICA R7', 'LEICA R8', 'LEICA R9', '-R SN', '-R (',
        'LEICA R 50', 'LEICA R 35', 'LEICA R 28', 'LEICA R 21',
        'LEICA R 90', 'LEICA R 100', 'LEICA R 180', 'LEICA R 135',
        'LEICA R 60', 'LEICA R 70', 'LEICAFLEX'
    ]):
        return "R System"
    # SL/Q/S System
    if any(x in n for x in ['SL2', 'SL-2', ' SL ', 'VARIO-ELMARIT-SL', 'APO-VARIO',
                              'LEICA Q', 'Q2 ', 'Q3 ', ' Q2', ' Q3',
                              'LEICA S ', ' S3', 'S-E', 'SUPER-APO']):
        return "SL/Q/S"
    # P&S (Compact) - Barnack보다 먼저
    if any(x in n for x in ['MINILUX', 'AF-C1', 'Z2X', 'LEICA C ', 'MINILUX ZOOM', 'LEICA MINI']):
        return "P&S"
    # Barnack (LTM/M39) - 나사마운트 올드 카메라/렌즈
    # 악세사리 코드네임이 있으면 Barnack 제외
    acc_codes = ['FOOKH', 'FIKUS', 'SOOMP', 'SOOKY', 'FILCA', 'TOOCA', 'VALOO',
                 'ITOOY', 'IROOA', 'SBOOI', 'VIOOH', 'SBLOO', 'SGVOO', 'IUFOO',
                 '12504', '12501', '12522', '12526', '12530', '12505', '14464']
    if any(x in n for x in acc_codes):
        return "Other"  # 악세사리는 시스템 분류 안 함
    barnack_bodies = ['LEICA I ', 'LEICA II ', 'LEICA III', 'LEICA IF', 'LEICA IIF',
                      'LEICA IIIA', 'LEICA IIIB', 'LEICA IIIC', 'LEICA IIIF', 'LEICA IIIG',
                      'LEICA 250', 'LEICA 72', 'ERNST LEITZ']
    barnack_lens = ['3.5CM', '5CM ', '5CM/', '7.3CM', '9CM ', '13.5CM',
                    'SUMMITAR', 'HEKTOR', 'SUMMAR ', 'ELMAX', 'XENON',
                    'LTM', 'L39', 'M39', 'SCREW MOUNT', '나사', 'LEITZ']
    # LEICA IIIF + 렌즈 세트는 Barnack으로 분류 (렌즈 동반해도 OK)
    if any(x in n for x in barnack_bodies + barnack_lens):
        return "Barnack"
    # M System
    if any(x in n for x in ['SUMMICRON', 'SUMMILUX', 'NOCTILUX', 'ELMARIT-M',
                              'SUMMARON', 'SUPER-ANGULON', 'LEICA M', ' M3', ' M4',
                              ' M5', ' M6', ' M7', ' M8', ' M9', ' M10', ' M11',
                              'LEICA MP', 'LEICA MA', 'LEICA M-A']):
        return "M System"
    return "Other"

# 렌즈 보호 키워드 - 조리개값(f숫자)이 있으면 렌즈로 보호
# "HOOD"만 있고 렌즈 모델명+조리개가 없으면 악세사리
import re as _re
def _has_aperture(name):
    """상품명에 조리개값(f숫자)이 있으면 렌즈"""
    return bool(_re.search(r'f\s*\d+[\./]\d+', name, _re.IGNORECASE))

LENS_PROTECT_KW = [
    # 조리개 표기가 있는 렌즈명 패턴 (함수로 보완)
    'super-angulon', 'angulon',
    'elmarit-m', 'summicron-m', 'summilux-m', 'noctilux',
    'summitar', 'nokton', 'voigtlander',
    # 시리얼 넘버 패턴 (sn. 이 있으면 개별 렌즈/바디)
    ' sn.', ' sn ',
    # Compact/PNS 카메라 (가격 기반 Accessory 오분류 방지)
    'minilux', 'd-lux', 'v-lux', 'c-lux', 'c1', 'c2', 'cl ',
    'leica m', 'leica r', 'leica q', 'leica sl', 'leica s',
    'sofort', 'digilux',
]
# 명백한 악세사리 코드네임 (5자리 영문/숫자)
ACCESSORY_CODES = [
    'itooy', 'irooa', 'sbooi', 'viooh', 'sbloo', 'sgvoo', 'iufoo',
    'fookh', 'fison', 'tooca', 'valoo', 'itdoo', 'irooa',
    '12585', '12504', '12501', '14464', '14066', '12522', '12526',
    '12564', '12575', '12595', '14100', '14101', '14269', '14358',
]

def detect_category(name, price_str=""):
    """상품명/가격으로 카테고리 분류 (Accessory 최우선, 렌즈 보호)"""
    n = name.lower()
    nu = name.upper()

    # ── 0순위: 악세사리 코드네임 → 무조건 Accessory ──
    if any(code in n for code in ACCESSORY_CODES):
        return "Accessory"

    # ── 렌즈 보호 체크 (조리개값 또는 렌즈 키워드 있으면 보호) ──
    is_lens = any(kw in n for kw in LENS_PROTECT_KW) or _has_aperture(name)

    # ── 1순위: Accessory 키워드 (단, 렌즈 보호 키워드 없을 때만) ──
    # 단독 악세사리 키워드 (렌즈 이름 없이 단독으로 있는 경우)
    strict_acc_kw = [
        '후드', '스트랩', 'hood', 'strap', 'case', '케이스',
        '파인더', 'viewfinder', 'adapter', '어댑터',
        'grip', '그립', 'cover', '커버', 'pouch', '파우치',
        'charger', '충전기', 'battery', '배터리', 'cable', '케이블',
        'flash', '플래시', '리어캡', '프론트캡', 'front cap', 'rear cap',
        'eye cup', 'lens cap', 'body cap',
    ]
    # 캡/필터는 렌즈 이름 없을 때만 악세사리
    cap_filter_kw = ['캡', 'cap', 'filter', '필터']

    is_strict_acc = any(kw in n for kw in strict_acc_kw)
    is_cap_filter = any(kw in n for kw in cap_filter_kw)

    if is_strict_acc and not is_lens:
        return "Accessory"
    if is_cap_filter and not is_lens:
        return "Accessory"

    # ── 가격 50만원 이하 → Accessory (단, 렌즈 보호 키워드 없을 때만) ──
    if not is_lens and price_str and price_str not in ['문의요망', '']:
        try:
            nums = re.findall(r"[\d,]+", price_str.replace('£', ''))
            if nums:
                p = float(nums[0].replace(',', ''))
                if 0 < p <= 500000:
                    return "Accessory"
        except:
            pass

    # ── 2순위: Body 키워드 ──
    body_kw = ['body', '바디', 'leica m3', 'leica m2', 'leica m4', 'leica m5',
               'leica m6', 'leica m7', 'leica mp', 'leica m-a', 'leica ma',
               'leica m8', 'leica m9', 'leica m10', 'leica m11', 'leica m240',
               'typ 240', 'r3 ', 'r4 ', 'r5 ', 'r6 ', 'r7 ', 'r8 ', 'r9 ',
               'leica i ', 'leica ii', 'leica iii', 'leica if', 'leica iif']
    if any(kw in n for kw in body_kw):
        return "Body"

    return "Lens"

def detect_brand(name):
    """상품명에서 브랜드 자동 분류
    ※ 라이카 키워드를 반드시 먼저 체크 → 라이카 상품이 3rd Party로 빠지지 않도록
    """
    n = name.lower()

    # ── 1순위: 라이카 키워드 (무조건 Leica) ──
    leica_kw = [
        'leica', 'summicron', 'summilux', 'noctilux', 'elmarit',
        'summaron', 'elmar', 'summar', 'summarit', 'summarex',
        'hektor', 'hologon', 'telyt', 'super-angulon', 'angulon',
        'minilux', 'leitz', 'wetzlar', 'ernst leitz',
        'd-lux', 'v-lux', 'c-lux',
    ]
    for kw in leica_kw:
        if kw in n:
            return "Leica"

    # ── 2순위: 라이카 마운트 호환 써드파티 ──
    for brand in THIRD_PARTY_BRANDS:
        if brand in n:
            return "3rd Party"

    # ── 3순위: 완전 비라이카 (크롤링 단계에서 이미 걸러지지만 혹시 몰라) ──
    for brand in NON_LEICA_BRANDS:
        if brand in n:
            return "Non-Leica"

    return "Other"

# 부속품 제외 키워드
ACCESSORY_KEYWORDS = [
    "케이스", "스트랩", "필터", "캡", "설명서", "충전기", "배터리",
    "후드only", "hood only", "어댑터", "파우치", "케이블", "핸드그립",
    "grip only", "strap only", "cap only", "lens cap", "body cap",
    "filter only", "box only", "박스only", "뷰파인더", "viewfinder",
    "hood", "case", "strap", "pouch", "charger", "flash", "플래시",
    "리어캡", "프론트캡", "front cap", "rear cap", "eye cup",
    # 코드네임
    "itooy", "irooa", "sbooi", "viooh", "sbloo", "sgvoo", "iufoo",
    "fookh", "fison", "tooca", "valoo", "itdoo",
    "12585", "12504", "12501", "14464", "14066", "12522", "12526",
    "12564", "12575", "12595", "14100", "14269", "14358",
]

# 바디 전용 제외 키워드
BODY_EXCLUDE_KW = ['lens only', '렌즈만', 'no body', 'lenses only', 'lens set']
# 렌즈 전용 제외 키워드
LENS_EXCLUDE_KW = ['body only', '바디만', 'no lens', 'body set']
# Barnack 바디 오인식 방지 - 이게 있으면 렌즈/악세사리
BARNACK_EXCLUDE = ['elmarit', 'summicron', 'summilux', 'noctilux', 'summaron',
                   'summitar', 'hektor', 'elmar', 'summarex', 'telyt',
                   'minilux', 'digital', 'typ ', 'q2', 'q3', 'm9', 'm10', 'm11',
                   'f/', 'f=', '1:2', '1:3', '1:4', '1:1', 'filter', 'hood', 'cap']
# 디지털/M기종 키워드 (Barnack 검색에서 제외)
MODERN_LEICA = ['m9', 'm10', 'm11', 'digital', 'typ 240', 'typ 262', 'q2', 'q3',
                'sl2', ' sl ', 'monochrom', 'ccd', 'cmos']

def passes_barnack_filter(name):
    """Barnack 바디 전용 필터 - 렌즈/악세사리 오인식 방지"""
    n = name.lower()
    # 렌즈명 포함 시 제외
    if any(kw in n for kw in BARNACK_EXCLUDE):
        return False
    # 디지털/현행 기종 제외
    if any(kw in n for kw in MODERN_LEICA):
        return False
    # 로마자 I/II/III가 독립 단어인지 확인 (regex )
    if re.search(r'I{1,3}', name, re.IGNORECASE):
        # 조리개 표기 근처면 렌즈 → 제외
        if re.search(r'[f]\s*[/=]?\s*\d|1:\d|\d\.\d', n):
            return False
        return True
    return True

# 비라이카 브랜드 키워드 (바디 검색 시 제외) → NON_LEICA_BRANDS 전역 상수 사용

def passes_filter(name, must_contain, item_meta=None):
    """향상된 필터 - 카테고리별 상호 배타적 필터링"""
    name_lower = " ".join(name.lower().split())

    # 바디 검색 시 비라이카 브랜드 제외
    item_cat = item_meta.get("category", "") if item_meta else ""
    if item_cat == "Body":
        if any(kw in name_lower for kw in NON_LEICA_BRANDS):
            return False

    # Barnack 바디 전용 필터
    if item_meta and item_meta.get("barnack"):
        if not passes_barnack_filter(name):
            return False

    # 카테고리별 상호 배제
    item_cat = item_meta.get("category", "") if item_meta else ""
    if item_cat == "Body":
        if any(kw in name_lower for kw in BODY_EXCLUDE_KW):
            return False
    elif item_cat == "Lens":
        if any(kw in name_lower for kw in LENS_EXCLUDE_KW):
            return False

    for word in must_contain:
        w = word.lower()
        # 숫자 단독 매칭 방지 (sn.2548 같은 시리얼 넘버 제외)
        if re.match(r"^\d+$", w):
            if not re.search(r"(?<!\d)" + w + r"(?!\d)", name_lower):
                return False
        else:
            if w not in name_lower:
                return False
    return True

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
        "base": "https://leica-storebando.co.kr",
        "categories": [
            "https://leica-storebando.co.kr/product/list.html?cate_no=442",  # 충무로
            "https://leica-storebando.co.kr/product/list.html?cate_no=436",  # 대치
        ],
        "통화": "KRW",
    },
    {
        "name": "사진집",
        "base": "https://www.sazinzibb.com",
        "categories": [
            "https://www.sazinzibb.com/category/%EC%A4%91%EA%B3%A0%EC%83%81%ED%92%88/27/",
            "https://www.sazinzibb.com/category/%EC%9C%84%ED%83%81%EC%A0%9C%ED%92%88/28/",
        ],
        "통화": "KRW",
    },
    {
        "name": "장씨카메라",
        "base": "https://j-camera.com",
        "categories": [
            "https://j-camera.com/product/list.html?cate_no=358",
            "https://j-camera.com/product/list.html?cate_no=421",  # 악세사리
        ],
        "통화": "KRW",
    },
]

# 카테고리 기반 크롤러 함수 추가

def crawl_category(page, site):
    """카테고리 페이지를 전체 순회하며 상품 수집"""
    results = []
    site_name = site["name"]
    base = site["base"]

    for cat_url in site["categories"]:
        print(f"\n  📂 카테고리: {cat_url}")
        page_num = 1

        while True:
            # 페이지 URL 구성
            if "?" in cat_url:
                url = cat_url + f"&page={page_num}"
            else:
                url = cat_url + f"?page={page_num}"

            print(f"    └─ {page_num}페이지 수집 중...")

            try:
                page.goto(url, wait_until="domcontentloaded", timeout=15_000)
            except Exception as e:
                print(f"    ❌ 로드 실패: {e}")
                break

            try:
                page.wait_for_selector("ul.prdList > li", timeout=6_000)
            except:
                print(f"    마지막 페이지 도달")
                break

            # lazy loading 트리거 - 페이지 전체 스크롤
            page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            page.wait_for_timeout(500)
            page.evaluate("window.scrollTo(0, 0)")

            cards = page.query_selector_all("ul.prdList > li")
            if not cards:
                break

            print(f"    └─ {len(cards)}개 상품 발견")
            found_any = False

            for card in cards:
                try:
                    name_el = card.query_selector(".name")
                    if not name_el:
                        continue
                    name = " ".join(name_el.inner_text().strip().split())
                    if not name:
                        continue

                    # 비라이카 브랜드 제외 (전역 NON_LEICA_BRANDS 사용)
                    name_lower = name.lower()
                    if any(b in name_lower for b in NON_LEICA_BRANDS):
                        continue

                    # 카테고리 분류 (악세사리도 수집하되 태깅만)
                    cat = detect_category(name)

                    # 링크
                    link_el = card.query_selector("a")
                    href = link_el.get_attribute("href") if link_el else ""
                    if href and not href.startswith("http"):
                        href = base + href
                    href = href.split("#")[0]

                    # 가격
                    card_text = card.inner_text()
                    price_match = re.search(r"([\d,]+원)", card_text)
                    price = price_match.group(1) if price_match else "문의요망"
                    price = normalize_price(price)

                    # 이미지 - 실제 상품 이미지 찾기
                    img_url = ""
                    all_imgs = card.query_selector_all("img")
                    for img_el in all_imgs:
                        raw = img_el.get_attribute("src") or ""
                        # //도메인/web/product/ 또는 /web/product/ 패턴
                        if "web/product/" in raw or "upload/product/" in raw:
                            img_url = fix_img_url(raw, base)
                            break
                    # 못찾으면 data-src 시도
                    if not img_url:
                        img_el = card.query_selector("img")
                        if img_el:
                            raw = (img_el.get_attribute("data-src") or
                                   img_el.get_attribute("data-original") or "")
                            if raw and "img_product_big.gif" not in raw:
                                img_url = fix_img_url(raw, base)

                    # 컨디션
                    cond_match = re.search(r"(\d{2,3})%", card_text)
                    if not cond_match:
                        cond_match = re.search(r"(\d{2,3})%", name)
                    condition = cond_match.group(1) + "%" if cond_match else "정보없음"

                    # 품절 감지
                    card_html = card.inner_html()
                    is_soldout = False
                    is_reserved = False

                    if site_name == "사진집":
                        is_soldout = "pdi_sold.png" in card_html or "품절" in card_html
                    elif site_name == "장씨카메라":
                        is_soldout = ('alt="품절"' in card_html or
                                     "icon_202505071559330700.gif" in card_html or
                                     "soldout" in card_html.lower())
                        is_reserved = "예약중" in card_html
                    elif site_name == "라이카스토어 충무로":
                        is_soldout = ("icon_202209171535309800.gif" in card_html or
                                     "SOLD OUT" in card_html or "품절" in card_html)
                        is_reserved = "예약중" in card_html

                    # label 자동 감지
                    gen = detect_generation(name)
                    sys = detect_system(name)
                    mount = detect_mount(name)
                    label = auto_label(name)

                    brand = detect_brand(name)
                    results.append({
                        "site": site_name,
                        "label": label,
                        "상품명": name,
                        "세대": gen,
                        "컨디션": condition,
                        "가격": price,
                        "통화": site["통화"],
                        "이미지": img_url,
                        "링크": href,
                        "품절": is_soldout,
                        "예약중": is_reserved,
                        "category": cat,
                        "system": sys,
                        "mount": mount,
                        "brand": brand,
                    })
                    found_any = True
                    status = "🚫품절" if is_soldout else ("📋예약중" if is_reserved else "✔ ")
                    print(f"    {status} {name[:45]} | {condition} | {price}")

                except Exception as e:
                    print(f"    ⚠️  파싱 오류: {e}")
                    continue

            if not found_any:
                break
            page_num += 1

    return results


def auto_label(name):
    """상품명에서 label 자동 감지 - 세대/조리개별 세분화"""
    n = name.lower()

    # ── Noctilux (키워드 명시 또는 조리개로 추론) ──
    if "noctilux" in n or "loctilux" in n:
        if "0.95" in n: return "50mm Noctilux f0.95"
        if "1.2" in n: return "50mm Noctilux f1.2"
        if "original" in n: return "50mm Noctilux f1.2"  # 충무로 1세대 표기
        if "1.0" in n: return "50mm Noctilux f1.0"
        if "75" in n or "1.25" in n: return "75mm Noctilux f1.25"
        return "Noctilux"
    # 복각 + 1.2 → Noctilux f1.2
    if '복각' in n and '1.2' in n and not any(k in n for k in _nocti_exc):
        return "50mm Noctilux f1.2"

    # 충무로/장씨 약식: "M 50/1.2", "M50/1.2", "복각" 등 → Noctilux 추론
    _nocti_exc = ['filter','필터','hood','후드','cap','case','strap','serie','canon','nikon','sony','fuji','sigma dp']
    if not any(k in n for k in _nocti_exc):
        if re.search(r'\b50/1\.2\b', n) or ("f1.2" in n and "50" in n and "1.25" not in n):
            return "50mm Noctilux f1.2"
        if re.search(r'\b75/1\.25\b', n) or ("f1.25" in n and "75" in n):
            return "75mm Noctilux f1.25"
        if re.search(r'\b50/0\.95\b', n) or ("f0.95" in n and "50" in n):
            return "50mm Noctilux f0.95"
        if re.search(r'\b50/1\.0\b', n):
            return "50mm Noctilux f1.0"

    # ── Summilux 세대별 ──
    if "summilux" in n:
        import re as _re3
        mm_m = _re3.search(r'(\d+)(?:mm|/)', n)
        mm = mm_m.group(1) if mm_m else ""
        # 35mm 세분화
        if mm == "35":
            # ── Rule A: ASPHERICAL 풀스펠링 → AA (두매, 컬렉터 아이템) ──
            # "aspherical"이 풀스펠링으로 있으면 AA (ASPH. 약어와 구분)
            if "aspherical" in n: return "35mm Summilux AA"
            # ── Rule B: 2매/두매/Double/AA 키워드 → AA ──
            if any(kw in n for kw in ["2매","2 매","두매","double"," aa ","(aa)"]): return "35mm Summilux AA"
            # ── 현행 ASPH (약어) ──
            if "fle ii" in n or "fle2" in n: return "35mm Summilux ASPH FLE II"
            if "fle" in n: return "35mm Summilux ASPH FLE"
            if "asph" in n: return "35mm Summilux ASPH"
            if "pre-asph" in n: return "35mm Summilux Pre-ASPH"
            if "steel rim" in n or "steel" in n: return "35mm Summilux Steel Rim"
            if "titan" in n: return "35mm Summilux Titan"
            if "1세대" in n or "1st" in n: return "35mm Summilux Steel Rim"
            if "2세대" in n or "2nd" in n or "pre" in n: return "35mm Summilux Pre-ASPH"
            if "3세대" in n or "3rd" in n: return "35mm Summilux Pre-ASPH"
            if "4세대" in n or "4th" in n: return "35mm Summilux ASPH"
            return "35mm Summilux"
        # 50mm 세분화
        if mm == "50":
            if "asph" in n: return "50mm Summilux ASPH"
            if "black paint" in n or "blackpaint" in n: return "50mm Summilux Black Paint"
            if "titan" in n: return "50mm Summilux Titan"
            if "1세대" in n or "1st" in n: return "50mm Summilux 1세대"
            if "2세대" in n or "2nd" in n: return "50mm Summilux 2세대"
            if "3세대" in n or "3rd" in n: return "50mm Summilux 3세대"
            if "4세대" in n or "4th" in n: return "50mm Summilux 4세대"
            if not any(x in n for x in ["asph","black paint","blackpaint","titan",
                                          "세대","1st","2nd","3rd","4th","special",
                                          "edition","limited","한정"]):
                return "50mm Summilux (올드)"
            return "50mm Summilux"
        # 75mm
        if mm == "75": return "75mm Summilux"
        # 기타 mm
        if "asph" in n and mm: return f"{mm}mm Summilux ASPH"
        if mm: return f"{mm}mm Summilux"
        return "Summilux"

    # ── Summicron 세대별 ──
    if "summicron" in n:
        if "apo" in n:
            for mm in ["35","50","75","90"]:
                if mm in n: return f"{mm}mm APO-Summicron"
        # mm 추출 - 가장 먼저
        import re as _re2
        mm_match = _re2.search(r"(\d+)(?:mm|/)", n)
        mm = mm_match.group(1) if mm_match else ""
        # 50mm 세분화
        if mm == "50":
            if "asph" in n: return "50mm Summicron ASPH"
            if "dr" in n or "dual" in n: return "50mm Summicron DR"
            if "rigid" in n: return "50mm Summicron Rigid"
            if "침동" in n or "collapsible" in n: return "50mm Summicron (침동)"
            if "2세대" in n or "3세대" in n or "4세대" in n: return "50mm Summicron (올드)"
            return "50mm Summicron"
        # 35mm 세분화
        if mm == "35":
            if "asph" in n: return "35mm Summicron ASPH"
            if "8매" in n or "8-el" in n or "8el" in n: return "35mm Summicron 1st (8매)"
            if "6매" in n or "6-el" in n: return "35mm Summicron (6매)"
            return "35mm Summicron"
        if mm in ["28","75","90"]: return f"{mm}mm Summicron"
        return "Summicron"

    # ── Elmarit ──
    if "elmarit" in n and "tri" not in n:
        import re as _re4
        mm_e = _re4.search(r'(\d+)(?:mm|/)', n)
        mm = mm_e.group(1) if mm_e else ""
        # 28mm 세분화
        if mm == "28":
            if "asph" in n: return "28mm Elmarit ASPH"
            if "1세대" in n or "1st" in n or "9 element" in n or "9element" in n: return "28mm Elmarit 1세대"
            if "2세대" in n or "2nd" in n: return "28mm Elmarit 2세대"
            if "3세대" in n or "3rd" in n: return "28mm Elmarit 3세대"
            if "4세대" in n or "4th" in n: return "28mm Elmarit 4세대"
            if "vario" in n: return "28mm Vario-Elmarit"
            return "28mm Elmarit"
        # 21mm 세분화
        if mm == "21":
            if "asph" in n: return "21mm Elmarit ASPH"
            return "21mm Elmarit"
        if mm: return f"{mm}mm Elmarit"
        return "Elmarit"

    # ── Summarit ──
    if "summarit" in n:
        for mm in ["35","50","75","90"]:
            if mm in n: return f"{mm}mm Summarit"
        return "Summarit"

    # ── Summaron ──
    if "summaron" in n:
        if "35" in n: return "35mm Summaron"
        if "28" in n: return "28mm Summaron"
        return "Summaron"

    # ── Super-Angulon ──
    if "angulon" in n:
        for mm in ["21","16"]:
            if mm in n: return f"{mm}mm Super-Angulon"
        return "Super-Angulon"

    # ── Elmar 세분화 ──
    if "elmar" in n and "elmarit" not in n and "tri" not in n:
        if "50" in n or "5/2.8" in n or "5/3.5" in n:
            if "asph" in n: return "50mm Elmar-M ASPH"
            if "2.8" in n: return "50mm Elmar f2.8"
            if "3.5" in n: return "50mm Elmar f3.5"
            return "50mm Elmar"
        if "35" in n: return "35mm Elmar"
        for mm in ["90","65","24"]:
            if mm in n: return f"{mm}mm Elmar"
        return "Elmar"

    # ── Tri-Elmar ──
    if "tri" in n and "elmar" in n:
        if "16" in n or "21" in n: return "Tri-Elmar 16-18-21 (WATE)"
        return "Tri-Elmar 28-35-50 (MATE)"

    # ── Hektor ──
    if "hektor" in n: return "Hektor"

    # ── Summar ──
    if "summar" in n and "summarit" not in n and "summaron" not in n:
        return "50mm Summar"

    # ── Hologon ──
    if "hologon" in n: return "15mm Hologon"

    # M75, M90 등 렌즈 표기 먼저 처리
    import re as _re5
    lens_focal = _re5.search(r'm(\d{2,3})/(\d)', n.replace(" ",""))
    if lens_focal:
        focal = lens_focal.group(1)
        if focal in ["75","90","135","50","35","28","21"]:
            return f"{focal}mm Lens"

    # ── Bodies M 시스템 ── (렌즈 키워드 없을 때만)
    lens_kw = ["summicron","summilux","noctilux","elmarit","elmar","summaron","nokton",
                "angulon","hektor","summar","hologon","telyt","vario","apo"]
    if not any(kw in n for kw in lens_kw):
        for m in ["m11","m10","m9","m8","m7","m6","m4","m3","m2","mp","m-a","m240"]:
            if m in n.replace(" ",""): return f"Leica {m.upper()}"
    if "q3" in n: return "Leica Q3"
    if "q2" in n: return "Leica Q2"

    # ── Compact ──
    for c in ["d-lux","v-lux","c-lux","minilux","c2","c1","mini"]:
        if c in n: return f"Leica {c.upper()}"
    return ""


# ══════════════════════════════════════════════════════
# 크롤러: 카페24 (충무로 등 국내)
# ══════════════════════════════════════════════════════
def crawl_cafe24(page, site, keyword, label, must_contain, item_meta=None):
    results = []
    url = site["search_url"].format(query=keyword.replace(" ", "+"))
    print(f"    URL: {url}")

    try:
        page.goto(url, wait_until="domcontentloaded", timeout=15_000)
    except Exception as e:
        print(f"    ❌ 페이지 로드 실패: {e}")
        return results

    try:
        page.wait_for_selector("ul.prdList > li", timeout=6_000)
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
            # 위탁/중고 카테고리면 태그 없어도 통과
            is_used_category = '중고' in cat_url or '위탁' in cat_url
            if not is_used_category and "[중고]" not in name and "[위탁]" not in name:
                continue
            if not passes_filter(name, must_contain, item_meta):
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

            # 컨디션 (카드 텍스트 + 상품명에서 추출)
            card_text = card.inner_text()
            cond_match = re.search(r"(\d{2,3})%", card_text)
            if not cond_match:
                cond_match = re.search(r"(\d{2,3})%", name)
            condition = cond_match.group(1) + "%" if cond_match else "정보없음"

            gen = detect_generation(name)

            # 충무로 품절/예약중 감지
            card_html = card.inner_html()
            is_soldout = (
                "icon_202209171535309800.gif" in card_html or
                "SOLD OUT" in card_html or
                "품절" in card_html
            )
            is_reserved = "예약중" in card_html

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
                "예약중": is_reserved,
            })
            status = "🚫품절" if is_soldout else ("📋예약중" if is_reserved else "✔ ")
            print(f"    {status} {name[:40]} | {gen} | {condition} | {price}")

        except Exception as e:
            print(f"    ⚠️  카드 파싱 오류: {e}")
            continue

    return results

def crawl_cafe24_all(page, site, keyword, label, must_contain, item_meta=None):
    """중고 태그([중고],[위탁]) 없이 전체 상품을 중고로 간주하는 카페24 크롤러"""
    results = []
    url = site["search_url"].format(query=keyword.replace(" ", "+"))
    print(f"    URL: {url}")

    try:
        page.goto(url, wait_until="domcontentloaded", timeout=15_000)
    except Exception as e:
        print(f"    ❌ 페이지 로드 실패: {e}")
        return results

    try:
        page.wait_for_selector("ul.prdList > li", timeout=6_000)
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
            if not passes_filter(name, must_contain, item_meta):
                continue

            link_el = card.query_selector("a")
            href = link_el.get_attribute("href") if link_el else ""
            if href and not href.startswith("http"):
                href = site["base"] + href
            href = href.split("#")[0]

            # 상품명 줄바꿈 정리
            name = " ".join(name.split())
            card_text = card.inner_text()

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

            # 품절 감지 (사이트별 이미지 패턴)
            card_html = card.inner_html()
            card_text_lower = card_text.lower()
            site_name = site["name"]
            is_soldout = False
            is_reserved = False

            if site_name == "사진집":
                is_soldout = "pdi_sold.png" in card_html or "품절" in card_html
            elif site_name == "장씨카메라":
                is_soldout = ('alt="품절"' in card_html or
                             "icon_202505071559330700.gif" in card_html or
                             "품절" in card_html)
                is_reserved = "예약중" in card_html
            else:
                is_soldout = any(kw in card_text_lower for kw in ["품절", "sold out", "판매완료"])
                soldout_btn = card.query_selector(".icon-sold-out, .soldout, [class*='soldout']")
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
                "예약중": is_reserved,
            })
            status = "🚫품절" if is_soldout else ("📋예약중" if is_reserved else "✔ ")
            print(f"    {status} {name[:40]} | {gen} | {condition} | {price}")

        except Exception as e:
            print(f"    ⚠️  카드 파싱 오류: {e}")
            continue

    return results

def crawl_godo(page, site, keyword, label, must_contain, item_meta=None):
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
            price_match = re.search(r"([\d,]+원)", card_text)
            price = price_match.group(1) if price_match else "문의요망"
            cond_match = re.search(r"(\d{2,3})%", card_text)
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

def crawl_ffordes_search(page, site, keyword, label, must_contain, item_meta=None):
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
            if not passes_filter(name, must_contain, item_meta):
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
                "품절": False,
            })
            print(f"    ✔  {name[:40]} | {gen} | {condition} | {price}")
        except Exception as e:
            print(f"    ⚠️  파싱 오류: {e}")
            continue

    return results

# ══════════════════════════════════════════════════════
# 단일 사이트 크롤링 - 병렬 처리용
# ══════════════════════════════════════════════════════
def crawl_site(site):
    site_results = []

    # Mock 모드: 로컬 HTML 파일 파싱
    if MOCK_MODE:
        mock_file = f"mock_{site['name'].replace(' ','_')}.html"
        if os.path.exists(mock_file):
            print(f"  [MOCK] {site['name']} → {mock_file}")
        else:
            print(f"  [MOCK] {mock_file} 없음, 스킵")
        return site_results

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        ctx = browser.new_context(
            user_agent=random.choice(USER_AGENTS),
            viewport={"width": 1280, "height": 800},
            locale="ko-KR",
        )
        page = ctx.new_page()

        # 리소스 차단 (이미지/CSS/폰트/광고)
        def block_resources(route):
            if route.request.resource_type in ["stylesheet", "font", "media"]:
                route.abort()
            elif any(x in route.request.url for x in ["google-analytics", "googletagmanager", "facebook", "ads", "tracker", "hotjar", "clarity"]):
                route.abort()
            else:
                route.continue_()
        page.route("**/*", block_resources)
        page.set_default_timeout(20000)

        print(f"\n{'='*50}")
        print(f"▶ {site['name']} 수집 시작")
        print(f"{'='*50}")

        seen_links = set()

        # 카테고리 방식으로 전체 수집
        res = crawl_category(page, site)
        for r in res:
            if r["링크"] not in seen_links:
                seen_links.add(r["링크"])
                site_results.append(r)

        ctx.close()
        browser.close()

    print(f"\n  ✅ {site['name']}: {len(site_results)}개 수집 완료")
    return site_results


def write_status(pct, current_site, total_count, done_sites, eta=0):
    """실시간 진행률을 status.json에 기록"""
    import datetime
    status = {
        "pct": pct,
        "current_site": current_site,
        "total_count": total_count,
        "done_sites": done_sites,
        "eta_seconds": eta,
        "updated_at": datetime.datetime.now().isoformat(),
        "running": pct < 100,
    }
    try:
        with open("status.json", "w", encoding="utf-8") as f:
            json.dump(status, f, ensure_ascii=False)
    except Exception as e:
        print(f"    ⚠️ status.json 쓰기 실패: {e}")


def crawl_ffordes(page):
    """Ffordes 크롤러 - Leica 카테고리 전체"""
    results = []
    base = "https://www.ffordes.com"

    # 라이카 관련 카테고리 (렌즈/바디 중심)
    categories = [
        ("https://www.ffordes.com/c/194/leica-m", "M"),      # Leica M 렌즈
        ("https://www.ffordes.com/c/192/leica-m", "M"),      # Leica M 바디
        ("https://www.ffordes.com/c/202/leica-r", "R"),      # Leica R 렌즈
        ("https://www.ffordes.com/c/199/leica-r", "R"),      # Leica R 바디
        ("https://www.ffordes.com/c/211/leica-screw", "L"),  # Leica Screw 렌즈
        ("https://www.ffordes.com/c/1080/leica-screw", "L"), # Leica Screw 바디
        ("https://www.ffordes.com/c/189/leica", "M"),        # Leica 디지털
        ("https://www.ffordes.com/c/1413/leica-sl", "SL"),   # Leica SL
        ("https://www.ffordes.com/c/1433/l-mount", "SL"),    # L-Mount
    ]

    seen_links = set()

    for cat_url, mount_hint in categories:
        print(f"\n  📂 Ffordes: {cat_url}")
        try:
            page.goto(cat_url, wait_until="domcontentloaded", timeout=30_000)
            page.wait_for_selector('#sscProductArray article', timeout=20_000)
        except Exception as e:
            print(f"    ❌ 로드 실패: {e}")
            continue

        # 카테고리 ID 추출 (URL에서 숫자 부분)
        import re as _re
        cat_id = _re.search(r'/c/(\d+)/', cat_url)
        cat_id = cat_id.group(1) if cat_id else ''

        total_pages = page.evaluate("()=>parseInt(document.getElementById('TotalPages')?.value||'1')")
        print(f"    총 {total_pages}페이지")

        for page_num in range(1, total_pages + 1):
            if page_num > 1:
                try:
                    next_url = f"{cat_url}?p={page_num}&q={cat_id}"
                    page.goto(next_url, wait_until="domcontentloaded", timeout=30_000)
                    page.wait_for_selector('#sscProductArray article', timeout=8_000)
                except Exception as e:
                    print(f"    ⚠️ p{page_num} 이동 실패: {e}")
                    break

            items = page.evaluate("""() => {
                const results = [];
                const articles = document.querySelectorAll('#sscProductArray article');
                for (const a of articles) {
                    const name = a.querySelector('meta[itemprop="name"]')?.content?.trim() || '';
                    if (!name) continue;
                    const img = a.querySelector('meta[itemprop="image"]')?.content || '';
                    const linkEl = a.querySelector('a[href*="/p/"]');
                    const href = linkEl ? 'https://www.ffordes.com' + linkEl.getAttribute('href') : '';
                    if (!href) continue;
                    const priceEl = a.querySelector('.prodPrice .priceTxt, .priceTxt, .prodPrice');
                    const priceRaw = priceEl ? priceEl.innerText.trim() : '';
                    const priceMatch = priceRaw.match(/£[\d,\.]+/);
                    const price = priceMatch ? priceMatch[0] : '';
                    const isUsed = a.classList.contains('Used');
                    const isSold = a.querySelector('.soldout, .out-of-stock') !== null ||
                                   a.innerText.toLowerCase().includes('sold out');
                    results.push({name, href, img, price, isUsed, isSold});
                }
                return results;
            }""")

            if not items:
                print(f"    마지막 페이지 도달 (p{page_num})")
                break

            print(f"    └─ p{page_num}: {len(items)}개")
            found_any = False

            for item in items:
                href = item.get('href', '')
                if not href or href in seen_links:
                    continue
                seen_links.add(href)
                found_any = True

                name = item.get('name', '').strip()
                price = item.get('price', '')
                is_sold = item.get('isSold', False)
                is_used = item.get('isUsed', True)
                img = item.get('img', '')

                # 신품 제외 (중고 사이트 목적)
                if not is_used:
                    continue

                label = auto_label(name)
                mount = detect_mount(name)
                # URL 기반 마운트 보완 (detect_mount가 Unknown일 때)
                if mount == 'Unknown':
                    _url_lower = href.lower()
                    if '/leica-screw/' in _url_lower:
                        mount = 'L'
                    elif '/leica-m/' in _url_lower:
                        mount = 'M'
                    elif '/leica-r/' in _url_lower:
                        mount = 'R'
                    elif '/l-mount/' in _url_lower or '/leica-sl/' in _url_lower:
                        mount = 'SL'
                    elif mount_hint:
                        mount = mount_hint

                status = "🚫sold" if is_sold else "✔ "
                cond = "Used" if is_used else "New"
                print(f"    {status} {name[:45]} | {price} | {cond}")

                results.append({
                    "site": "Ffordes (영국)",
                    "label": label,
                    "상품명": name,
                    "세대": "",
                    "컨디션": cond,
                    "가격": price,
                    "통화": "GBP",
                    "이미지": img,
                    "링크": href,
                    "품절": is_sold,
                    "예약중": False,
                    "mount": mount,
                    "brand": "Leica",
                })

            if not found_any:
                break

    print(f"\n  ✅ Ffordes 완료: {len(results)}개")
    return results


def crawl_all():
    from concurrent.futures import ThreadPoolExecutor, as_completed

    start_time = time.time()
    all_results = []
    write_status(0, "Starting...", 0, 0)

    # 기존 results.json 로드 (first_seen 보존 + 조기종료용)
    existing_links = set()
    existing_first_seen = {}  # 링크 → first_seen 맵
    try:
        with open("results.json", "r", encoding="utf-8") as f:
            existing = json.load(f)
            for r in existing:
                existing_links.add(r["링크"])
                if r.get("first_seen"):
                    existing_first_seen[r["링크"]] = r["first_seen"]
        print(f"📋 기존 매물 {len(existing_links)}개 로드 (first_seen {len(existing_first_seen)}개 보존)")
    except:
        pass

    # sold_items.json 로드 → 이미 품절된 링크는 크롤링 스킵
    sold_links = set()
    try:
        with open("sold_items.json", "r", encoding="utf-8") as f:
            sold = json.load(f)
            for r in sold:
                sold_links.add(r["링크"])
        print(f"🚫 품절 링크 {len(sold_links)}개 로드 → 크롤링 스킵")
    except:
        pass
    globals()['SOLD_LINKS'] = sold_links

    # 억불카메라(godo)는 별도 순차 처리 (headless=False 필요)
    # 특정 사이트만 크롤링 (--site 옵션)
    active_sites = SITES
    if FFORDES_ONLY:
        # Ffordes만 실행
        parallel_sites = []
        godo_sites = []
        print(f"🎯 Ffordes 전용 모드")
    elif SITE_FILTER:
        active_sites = [s for s in SITES if SITE_FILTER in s["name"]]
        print(f"🎯 사이트 필터: {SITE_FILTER} ({len(active_sites)}개)")
        parallel_sites = active_sites
        godo_sites = []
    else:
        parallel_sites = active_sites
        godo_sites = []

    print(f"🚀 병렬 크롤링 시작 ({len(parallel_sites)}개 사이트 동시 처리)")

    total_sites = len(parallel_sites) + 1  # +1 for Ffordes
    done_sites = 0

    # 병렬 처리
    if parallel_sites:
        with ThreadPoolExecutor(max_workers=min(len(parallel_sites), 4)) as executor:
            futures = {executor.submit(crawl_site, site): site for site in parallel_sites}
            for future in as_completed(futures):
                site = futures[future]
                try:
                    results = future.result()
                    all_results.extend(results)
                except Exception as e:
                    print(f"❌ {site['name']} 오류: {e}")
                done_sites += 1
                elapsed = time.time() - start_time
                eta = int(elapsed / done_sites * (total_sites - done_sites)) if done_sites else 0
                write_status(int(done_sites/total_sites*100), site['name'], len(all_results), done_sites, eta)

    # 억불카메라 순차 처리
    for site in godo_sites:
        results = crawl_site(site)
        all_results.extend(results)
        done_sites += 1
        write_status(int(done_sites/total_sites*100), site['name'], len(all_results), done_sites, 0)

    # Ffordes 크롤링
    print(f"\n🇬🇧 Ffordes 크롤링 시작")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.set_extra_http_headers({"Accept-Language": "en-GB,en;q=0.9"})
        try:
            ffordes_results = crawl_ffordes(page)
            all_results.extend(ffordes_results)
        except Exception as e:
            print(f"❌ Ffordes 오류: {e}")
        finally:
            browser.close()
    done_sites += 1
    write_status(int(done_sites/total_sites*100), "Ffordes", len(all_results), done_sites, 0)

    # 전체 중복 제거
    seen = set()
    unique_results = []
    for r in all_results:
        if r["링크"] not in seen:
            seen.add(r["링크"])
            unique_results.append(r)

    elapsed = time.time() - start_time

    # label 자동 보정 + 상품명 정리 + system/category 분류
    import datetime
    crawl_time = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9))).strftime("%Y-%m-%d %H:%M:%S")
    for r in unique_results:
        name = r['상품명']
        # 상품명에서 "상품명 :" 제거
        if name.startswith('상품명') and ':' in name:
            name = name.split(':', 1)[-1].strip()
            r['상품명'] = name
        name_lower = name.lower()
        # system/category 분류
        r['category'] = detect_category(r['상품명'], r.get('가격', ''))
        if r['category'] == 'Accessory':
            r['label'] = ''  # Accessory는 label 제거 (평균가 왜곡 방지)
        r['mount'] = detect_mount(r['상품명'])
        # brand 필드: 없으면 상품명에서 자동 감지
        if not r.get('brand'):
            r['brand'] = detect_brand(r['상품명'])
        # crawl_time은 항상 최신으로
        r['crawl_time'] = crawl_time
        # first_seen: 기존 데이터면 보존, 신규면 현재 시간
        link = r.get('링크', '')
        if link in existing_first_seen:
            r['first_seen'] = existing_first_seen[link]  # 기존 날짜 유지
        else:
            r['first_seen'] = crawl_time  # 신규 매물!
            if 'first_seen' not in r or r.get('first_seen') == crawl_time:
                print(f"  🆕 신규: {r['상품명'][:40]}")
        # Noctilux label 조리개별 보정 + generation 필드
        if 'noctilux' in name_lower:
            nocti_gen = detect_noctilux_gen(name)
            if nocti_gen:
                r['noctilux_gen'] = nocti_gen
        if r['label'] in ['50mm Noctilux']:
            if '0.95' in name_lower:
                r['label'] = '50mm Noctilux f0.95'
            elif '1.2' in name_lower:
                r['label'] = '50mm Noctilux f1.2'
            elif '1.0' in name_lower or 'e58' in name_lower or 'e60' in name_lower:
                r['label'] = '50mm Noctilux f1.0'

        # ── 가격 기반 브랜드/label 보정 ──
        try:
            price_str = r.get('가격', '')
            currency = r.get('통화', 'KRW')
            price_num = int(re.sub(r'[^0-9]', '', price_str)) if price_str else 0
            # GBP→KRW 환산 (대략 1GBP=1,700원)
            if currency == 'GBP':
                price_num = price_num * 1700

            # Noctilux f1.2 가격 기반 추론
            if r['label'] in ['50mm Lens', '50mm Noctilux f1.2', ''] and                re.search(r'50/1\.2|50mm.*1\.2|1\.2.*50mm', name_lower):
                if price_num >= 15_000_000:
                    # 1,500만원↑ → 오리지널
                    r['label'] = '50mm Noctilux f1.2'
                    r['brand'] = 'Leica'
                elif price_num >= 5_000_000:
                    # 500~1,500만원 → 라이카 공식 복각
                    r['label'] = '50mm Noctilux f1.2'
                    r['brand'] = 'Leica'
                elif 1_000_000 <= price_num < 5_000_000:
                    # 100~500만원 → 써드파티 복각
                    r['label'] = '50mm Noctilux f1.2'
                    if r.get('brand') not in ['Leica']:
                        r['brand'] = '3rd Party'
        except Exception:
            pass

    # ── 판매 완료 추적 (sold_items.json) ──
    import datetime as dt
    now_str = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_links = {r["링크"] for r in unique_results}

    # 기존 sold_items 로드
    sold_items = []
    try:
        with open("sold_items.json", "r", encoding="utf-8") as f:
            sold_items = json.load(f)
    except:
        # 없으면 빈 파일 생성
        with open("sold_items.json", "w", encoding="utf-8") as f:
            import json as _j; _j.dump([], f)

    sold_links = {r["링크"] for r in sold_items}

    # 이전에 있었으나 지금 없는 매물 → 판매 완료
    newly_sold = []
    try:
        with open("results.json", "r", encoding="utf-8") as f:
            prev_results = json.load(f)
        for r in prev_results:
            if r["링크"] not in new_links and r["링크"] not in sold_links and not r.get("품절"):
                sold_r = dict(r)
                sold_r["is_sold"] = True
                sold_r["sold_at"] = now_str
                # 판매 소요 시간 계산
                if r.get("crawl_time"):
                    try:
                        t0 = dt.datetime.strptime(r["crawl_time"], "%Y-%m-%d %H:%M:%S")
                        t1 = dt.datetime.strptime(now_str, "%Y-%m-%d %H:%M:%S")
                        hours = round((t1 - t0).total_seconds() / 3600, 1)
                        sold_r["hours_to_sell"] = hours
                    except:
                        sold_r["hours_to_sell"] = None
                newly_sold.append(sold_r)
                print(f"  💸 판매 완료: {r['상품명'][:40]}")
    except:
        pass

    if newly_sold:
        sold_items.extend(newly_sold)
        # 최근 500개만 유지
        sold_items = sold_items[-500:]
        with open("sold_items.json", "w", encoding="utf-8") as f:
            json.dump(sold_items, f, ensure_ascii=False, indent=2)
        print(f"  💸 총 {len(newly_sold)}개 판매 완료 추가 → sold_items.json")

    with open("results.json", "w", encoding="utf-8") as f:
        json.dump(unique_results, f, ensure_ascii=False, indent=2)

    # 신규 매물 카운트 (crawl_sessions 저장에 필요)
    new_count = sum(1 for r in unique_results if r.get('first_seen') == crawl_time)

    # ── crawl_sessions.json 누적 저장 ──
    import datetime as _dt3
    _KST3 = _dt3.timezone(_dt3.timedelta(hours=9))
    end_time = _dt3.datetime.now(_KST3).strftime("%Y-%m-%d %H:%M:%S")
    session_entry = {
        "start_time": crawl_time,
        "end_time": end_time,
        "new_items": new_count,
        "total_items": len(unique_results),
    }
    try:
        with open("crawl_sessions.json", "r", encoding="utf-8") as f:
            sessions_log = json.load(f)
    except:
        sessions_log = []
    sessions_log = [s for s in sessions_log if s.get("start_time") != crawl_time]
    sessions_log.append(session_entry)
    sessions_log = sessions_log[-100:]
    with open("crawl_sessions.json", "w", encoding="utf-8") as f:
        json.dump(sessions_log, f, ensure_ascii=False, indent=2)
    print(f"📋 crawl_sessions.json 저장 완료 (총 {len(sessions_log)}개 세션)")

    write_status(100, "완료", len(unique_results), len(SITES), 0)
    print(f"\n{'='*50}")
    print(f"✅ 최종 {len(unique_results)}개 → results.json 저장 완료")
    print(f"🆕 신규 매물: {new_count}개 추가됨")
    print(f"⏱️  총 소요 시간: {elapsed:.1f}초 ({elapsed/60:.1f}분)")
    print(f"{'='*50}")
    for r in unique_results:
        print(f"\n  📷 [{r['세대']}] {r['상품명']}")
        print(f"     💰 {r['가격']} {r['통화']} | 컨디션: {r['컨디션']}")
        print(f"     🖼  {r['이미지'] or '이미지 없음'}")
        print(f"     🔗 {r['링크']}")

# ══════════════════════════════════════════════════════
# GitHub 자동 Push
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
        ["git", "add", "--ignore-errors", "results.json", "index.html", "admin.html", "sold_items.json"],
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


if __name__ == "__main__":
    crawl_all()
    # GitHub Actions 환경에서는 워크플로우가 push 담당
    if os.environ.get('GITHUB_ACTIONS'):
        print("ℹ️  GitHub Actions 환경 → 워크플로우에서 push 처리")
    else:
        push_to_github()
