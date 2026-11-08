from playwright.sync_api import sync_playwright
import time
import json
import threading
import re
import argparse
import random
import os
import sys as _sys_root
_sys_root.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # 저장소 루트 모듈 (condition_grade)

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
    # ROM, 3cam, 2cam → R 마운트
    if any(x in n for x in ['3CAM','2CAM','1CAM',' ROM ','ROM\"','-ROM','APO EXTENDER R','EXTENDER R']):
        return 'R'
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
        if 'LEICA' in n or 'VOIGTLANDER' in n:
            return "L"  # LEICA/Voigtlander LTM → L마운트
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

    # Ffordes 스타일: VM, ZM → M 마운트
    if re.search(r'\bVM\b', n) and not any(x in n for x in ['ADAPTER','CONVERTER']):
        return "M"
    if re.search(r'\bZM\b', n):
        return "M"
    # Ffordes 스타일: 끝에 " M BLACK", " M CHROME" 등
    if re.search(r'\bM\s+(BLACK|CHROME|SILVER|ANTHRACITE|BODY)\b', n):
        return "M"
    if re.search(r'\bM\s+\d', n):  # "M 50mm", "M 28mm" 등
        return "M"
    # Ffordes 스타일: 6bit → M 마운트
    if '6BIT' in n and 'LEICA' in n:
        return "M"
    # M Rokkor, Elcan → M 마운트
    if 'M ROKKOR' in n or 'ELCAN' in n or 'COLLAPSIBLE' in n:
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

    # ── Finder/뷰파인더/악세사리 → Accessory ──
    if any(x in n for x in ['FINDER','VIEWFINDER','UNIVERSALSUCHER','VIEW FINDER',
                              'SUCHER','SOFT RELEASE','TELEVID','TRINOVID']):
        return "Accessory"
    if any(x in n for x in ['HOLSTER','LUIGI','OBERWERTH','ZEGNA','ACAM-']):
        return "Accessory"
    # ── Carl Zeiss Jena → L ──
    if 'CARL ZEISS JENA' in n:
        return "L"
    # ── Sigma L Mount → SL ──
    if 'SIGMA' in n and any(x in n for x in ['DG DN','L MOUNT','L-MOUNT']):
        return "SL"
    # ── Lumix S → SL ──
    if 'LUMIX S' in n or ('PANASONIC' in n and ' S ' in n):
        return "SL"
    # ── Meyer Optik → M ──
    if 'MEYER OPTIK' in n:
        return "M"
    # ── Artizlab → M ──
    if 'ARTIZLAB' in n:
        return "M"
    # ── Visoflex2 → M ──
    if 'VISOFLEX2' in n or 'VISOFLEX 2' in n:
        return "M"
    # ── Laowa/TTArtisan L → SL ──
    if any(x in n for x in ['LAOWA','TTARTISAN']) and any(x in n for x in ['L MOUNT','L-MOUNT',' L ']):
        return "SL"
    # ── Light Lens Lab L → SL ──
    if 'LIGHT LENS LAB L' in n:
        return "SL"
    # ── ROM, 3CAM → R ──
    if any(x in n for x in ['3CAM','2CAM','1CAM',' ROM','APO EXTENDER R']):
        return "R"

    # ── 판매완료/보류 → Unknown 유지 ──
    if re.search(r'판매완료|보류|SOLD', n):
        return "Unknown"
    # ── 가방/쌍안경/삼각대/기타 악세사리 → Accessory ──
    if any(x in n for x in ['가방','BAG','쌍안경','BC SN','10X25','10×25','BC ','TRIPOD',
                              'BALL HEAD','TABLETOP','디옵터','DIOPTER','JNK (',
                              '오버베르트','OBERWERTH','ONA BAG']):
        return "Accessory"
    # ── VIT M (Leicavit) → M Accessory ──
    if 'VIT M' in n or 'VIT(MP)' in n or 'LEICAVIT' in n:
        return "M"
    # ── Coiro/호환 Vit → M Accessory ──
    if 'COIRO' in n or 'VIT FOR M' in n:
        return "M"
    # ── BE@RBRICK → Accessory ──
    if 'BE@RBRICK' in n:
        return "Accessory"
    # ── Q/Q2/Q3/Q-P 바디 ──
    if re.search(r'^Q[23P-]?\s*[\(\s\-\{]|^Q[23P-]?\s*$|^Q[23P-]?\b', n):
        return "Q"
    # ── SL 바디 단독 ──
    if re.search(r'^SL\s*[\(\-\s\{]|^SL\s*$', n):
        return "SL"
    # ── TL2/TL 바디 → SL ──
    if re.search(r'^TL2?\s*[\(\-\s\{]|^TL2?\s*$', n):
        return "SL"
    # ── CL + 세트 → SL ──
    if re.search(r'^CL[\+\s]', n):
        return "SL"
    # ── X1/X2/X typ → Compact ──
    if re.search(r'^X[12]?\s*[\(\s\{]|^X\s*TYP|^X[12]\s*$', n):
        return "Compact"
    # ── R6/R6.2/R8/R9 → R ──
    if re.search(r'^R[6-9][\d\.]*\s*[\(\s\{]|^R[6-9][\d\.]*\s*$', n):
        return "R"
    # ── R-E → R ──
    if re.search(r'LEICA R-E', n):
        return "R"
    # ── S 마운트 약식 → S ──
    if re.search(r'^S \d+/\d', n):
        return "S"
    # ── Sigma SL/L마운트 → SL ──
    if 'SIGMA' in n and any(x in n for x in ['SL 마운트','L마운트','DG DN','CONTEMPORARY','DG HSM','DN OS']):
        return "SL"
    elif '시그마' in n and any(x in n for x in ['SL 마운트','L마운트']):
        return "SL"
    # ── Light Lens Lab M → M ──
    if 'LIGHT LENS LAB' in n and 'LIGHT LENS LAB L' not in n:
        return "M"
    # ── M50/M35/M21/M90 약식 → M ──
    if re.search(r'^M\d+/\d', n):
        return "M"
    # ── M21/3.4 Super Angulon → M ──
    if 'SUPER ANGULON' in n and 'M21' in n:
        return "M"
    # ── M-10R → M ──
    if re.search(r'^M-10', n):
        return "M"
    # ── T 바디 → SL ──
    if re.search(r'^T\s*[\(\-\s\{]|^T\s*$', n):
        return "SL"
    # ── MDa → M ──
    if re.search(r'^MDA?\s*[\(\s]|^MDA?\s*$', n):
        return "M"
    # ── IIIf/IIIg 단독 표기 → L ──
    if re.search(r'^III[A-Z]?\s*(BODY\s*)?[\(\-\s]|^III[A-Z]?\s*(BODY)?\s*$', n):
        return "L"
    # ── L 85/1.5 Sumalex → L ──
    if 'SUMALEX' in n or 'SUMMROAN' in n:
        return "L"
    # ── 장씨 바르낙 로마숫자 ──
    if any(x in n for x in ['LEICA Ⅰ','LEICA ⅡF','LEICA ⅡD','LEICA ⅡC','LEICA ⅢF',
                              'LEICA ⅢG','LEICA ⅢA','LEICA Ⅲ ','LEICA ⅢF',
                              'LEICA STANDARD NICKEL','LEICA IG ','LEICA IF ']):
        return "L"
    # ── 장씨 LEICA III/II/I 바디 ──
    if re.search(r'LEICA\s+II[ICD]?\s+', n) or re.search(r'LEICA\s+III[ABCDFG]?\s', n):
        return "L"
    # ── LEICA VIT M → M ──
    if 'LEICA VIT' in n:
        return "M"
    # ── Carl Zeiss Sonnar/Opton → L ──
    if any(x in n for x in ['CARL ZEISS','ZEISS-OPTON']) and 'C/Y' not in n:
        return "L"
    # ── Zeiss ZM (충무로 약식) → M ──
    if re.search(r'^ZEISS\s+\d+|^ZM\s+', n):
        return "M"
    # ── Cooke L → L ──
    if 'COOKE' in n:
        return "L"
    # ── Voigtlander LTM → L ──
    if 'VOIGTLANDER' in n and 'LTM' in n:
        return "L"
    # ── angenieux R → R ──
    if 'ANGENIEUX' in n:
        return "R"
    # ── Panasonic S → SL ──
    if 'PANASONIC' in n:
        return "SL"
    # ── 50 Jahre CL → L (특별판) ──
    if '50 JAHRE CL' in n:
        return "L"
    # ── LEICA O-series → L ──
    if 'O-SERISE' in n or 'O-SERIES' in n or 'OSKAR BARNACK' in n:
        return "L"
    # ── Stemar 스테레오 → L ──
    if 'STEMAR' in n:
        return "L"
    # ── LTM → L ──
    if 'LTM' in n:
        return "L"
    # ── R250 Telyt → R ──
    if 'R250' in n:
        return "R"
    # ── LECIA MP (오타) → M ──
    if 'LECIA MP' in n:
        return "M"
    # ── Carlzeiss C (C/Y 제외) → L ──
    if 'CARLZEISS C' in n and 'C/Y' not in n:
        return "L"
    # ── Sigma 28-70 → SL ──
    if 'SIGMA' in n and re.search(r'28-70|24-70|100-400|150-600', n):
        return "SL"
    # ── LEICA 35mm F1.4 ASPH FLE → M ──
    if re.search(r'LEICA \d+MM F[\d\.]+.*ASPH', n) and 'FLE' in n:
        return "M"
    # ── LEICA 35mm/90mm/135mm 렌즈 세트 → L ──
    if re.search(r'LEICA \d+MM/\d+MM', n):
        return "L"
    # ── 캐논 → M (어댑터로 사용) ──
    if '캐논' in n:
        return "M"
    # ── CL 바디 → SL ──
    if re.search(r'^CL\s*[\(\[]', n) or re.search(r'^CL\s+(SILVER|BLACK)', n):
        return "SL"
    # ── Q/Q2/Q3/Q-P (느슨한 패턴) ──
    if re.search(r'\]\s*Q[23P\-]?\s*[\(\s\{\[]|\]\s*Q[23]?\s*$|\]Q[23]?\b', n):
        return "Q"
    # ── SL 단독 표기 ──
    if re.search(r'\]\s*SL\s*[\(\s\{\[]|\]\s*SL\s*$', n):
        return "SL"
    # ── TL2/TL 단독 ──
    if re.search(r'\]\s*TL2?\s*[\(\s\{\[]|\]\s*TL2?\s*$', n):
        return "SL"
    # ── CL+ 세트 → SL ──
    if re.search(r'\]\s*CL[\+\s]', n):
        return "SL"
    # ── X1/X2/X typ → Compact ──
    if re.search(r'\]\s*X[12]?\s*[\(\s\{\[]|\]\s*X\s+TYP|\]\s*X[12]\s*$', n):
        return "Compact"
    # ── R8/R9 단독 ──
    if re.search(r'\]\s*R[89]\s*[\(\s\{]|\]\s*R[89]\s*$', n):
        return "R"
    # ── R6/R6.2 단독 ──
    if re.search(r'\]\s*R6[\d\.]*\s*[\(\s\{]|\]\s*R6[\d\.]*\s*$', n):
        return "R"
    # ── S 마운트 약식 ──
    if re.search(r'\]\s*S \d+/\d', n):
        return "S"
    # ── M50/M35 약식 ──
    if re.search(r'\]\s*M\d+/\d', n):
        return "M"
    # ── M-10R ──
    if re.search(r'\]\s*M-10R\b', n):
        return "M"
    # ── MDa ──
    if re.search(r'\]\s*MDA?\s', n):
        return "M"
    # ── T 바디 → SL ──
    if re.search(r'\]\s*T\s*[\(\-\s]|\]\s*T\s*$', n):
        return "SL"
    # ── IIIf 단독 → L ──
    if re.search(r'\]\s*III[A-Z]?\s*[\(\-\s]|\]\s*III[A-Z]?\s*(BODY)?\s*$', n):
        return "L"
    # ── M-10R → M ──
    if re.search(r'\]\s*M-10R\b', n):
        return "M"
    # ── MDa → M ──
    if re.search(r'\]\s*MDA?\s*[\(\s]|\]\s*MDA?\s*$', n):
        return "M"
    # ── R9/R8 (Anthracite/Black) ──
    if re.search(r'\]\s*R[89]\s*[\(\s\{]|\]\s*R[89]\s*$', n):
        return "R"
    # ── X2/X1/X (typ) → Compact ──
    if re.search(r'\]\s*X[12]?\s*[\(\s\{\[]|\]\s*X[12]\s*$', n):
        return "Compact"
    # ── IIIf/IIIf Body → L ──
    if re.search(r'\]\s*III[A-Z]?\s*(BODY\s*)?[\(\-\s]|\]\s*III[A-Z]?\s*(BODY)?\s*$', n):
        return "L"
    # ── CL+ → SL ──
    if re.search(r'\]\s*CL\+', n):
        return "SL"
    # ── T (Silver/Black) → SL ──
    if re.search(r'\]\s*T\s*[\(\-\s]|\]\s*T\s*$', n):
        return "SL"
    # ── M-10R → M ──
    if re.search(r'\]\s*M-10R\b', n):
        return "M"
    # ── MDa → M ──
    if re.search(r'\]\s*MDA?\s*[\(\s]|\]\s*MDA?\s*$', n):
        return "M"
    # ── R9/R8 (Anthracite/Black) ──
    if re.search(r'\]\s*R[89]\s*[\(\s\{]|\]\s*R[89]\s*$', n):
        return "R"
    # ── X2/X1/X (typ) → Compact ──
    if re.search(r'\]\s*X[12]?\s*[\(\s\{\[]|\]\s*X[12]\s*$', n):
        return "Compact"
    # ── IIIf/IIIf Body → L ──
    if re.search(r'\]\s*III[A-Z]?\s*(BODY\s*)?[\(\-\s]|\]\s*III[A-Z]?\s*(BODY)?\s*$', n):
        return "L"
    # ── CL+ → SL ──
    if re.search(r'\]\s*CL\+', n):
        return "SL"
    # ── T (Silver/Black) → SL ──
    if re.search(r'\]\s*T\s*[\(\-\s]|\]\s*T\s*$', n):
        return "SL"
    # ── Zeiss Biogon (충무로 약식) → M ──
    if re.search(r'\]\s*ZEISS\s+|\]\s*ZM\s+', n):
        return "M"
    # ── zeiss 소문자 → M ──
    if re.search(r'\]\s*ZEISS\s+\d+', n):
        return "M"
    # ── LEICA LTM/35-135 LTM → L ──
    if 'LTM' in n:
        return "L"
    # ── 시그마 DG HSM → SL ──
    if '시그마' in n and 'DG HSM' in n:
        return "SL"
    # ── zeiss 소문자 → M ──
    if re.search(r'\]\s*ZEISS\s+\d+', n):
        return "M"
    # ── LEICA LTM/35-135 LTM → L ──
    if 'LTM' in n:
        return "L"
    # ── 시그마 DG HSM → SL ──
    if '시그마' in n and 'DG HSM' in n:
        return "SL"
    # ── LEICA I sn. → L ──
    if re.search(r'LEICA\s+I\s+SN\.', n):
        return "L"
    # ── LEICA IIlC → L ──
    if re.search(r'LEICA\s+II[ILD]?[A-Z]?\s+', n):
        return "L"
    # ── LEICA LTM/35-135 → L ──
    if re.search(r'LEICA\s+\d+-\d+\s+LTM|LEICA\s+LTM|LEICA\s+\d+-\d+\s*LTM', n):
        return "L"
    # ── LEICA 12xxx Hood → Accessory ──
    if re.search(r'LEICA\s+1[24]\d{3}[A-Z]?\b', n):
        return "Accessory"
    # ── LEICA 35mm sn. → M ──
    if re.search(r'LEICA\s+\d+MM\s+F[\d\.]+\s+ASPH.*SN\.', n):
        return "M"
    if re.search(r'LEICA\s+\d+MM\s+F[\d\.]+.*SN\.', n) and 'LEICA I' not in n:
        return "M"
    # ── LEICA M6J → M ──
    if 'M6J' in n:
        return "M"
    # ── LEICA S-E → S ──
    if 'LEICA S-E' in n:
        return "S"
    # ── LEICA R-E → R ──
    if 'LEICA R-E' in n:
        return "R"
    # ── LEICA Stereo → L ──
    if 'STEREO MIDLAND' in n:
        return "L"
    # ── LEICA 150 Jahre → L ──
    if '150 JAHRE' in n:
        return "L"
    # ── Sigma 28-70 → SL ──
    if re.search(r'\]\s*SIGMA\s+\d+-\d+', n):
        return "SL"
    # ── Voigtlander LTM → L ──
    if 'VOIGTLANDER' in n and 'LTM' in n:
        return "L"
    # ── Voigtlander 파인더 → Accessory ──
    if 'VOIGTLANDER' in n and '파인더' in n:
        return "Accessory"
    # ── Leicavit → M Accessory ──
    if 'LEICAVIT' in n:
        return "M"
    # ── MP3 → M 바디 ──
    if re.match(r'^MP\d\b', n):
        return "M"
    # ── M EV1 → M 바디 ──
    if re.match(r'^M EV\d', n):
        return "M"
    # ── Novoflex 어댑터 → Accessory ──
    if 'NOVOFLEX' in n:
        return "Accessory"
    # ── Panasonic S → SL (L-Mount Alliance) ──
    if 'PANASONIC' in n and re.search(r'\d+mm.*\bS\b', n):
        return "SL"
    # ── Angenieux R → R ──
    if 'ANGENIEUX' in n and ' R' in n:
        return "R"
    # ── PC Super Angulon R → R ──
    if 'PC SUPER ANGULON' in n and ' R' in n:
        return "R"
    # ── Summitar → L ──
    if 'SUMMITAR' in n:
        return "L"
    # ── Apo Macro TL → SL ──
    if 'APO MACRO TL' in n or 'MACRO TL' in n:
        return "SL"
    # ── Oskar Barnack / O-series → L ──
    if 'OSKAR BARNACK' in n or 'O-SERIE' in n or 'O SERIE' in n:
        return "L"
    # ── IF/IIIF/IIIG 바디 (장씨 스타일) ──
    if re.search(r'^LEICA\s+(IF|IIF|IIIF|IIIG|IIIC|IIIA|IIC|IID|IIlC)\b', n):
        return "L"
    # ── Barnack IF/II → L ──
    if 'BARNACK' in n:
        return "L"
    # ── 플래시/악세사리 코드명 → Accessory ──
    flash_kw = ['SF20','SF24','SF26','SF40','SF58','SF60','SF64','SF 20','SF 24',
                'SF 26','SF 40','SF 58','SF 60','SF 64','SF-20','SF-26','SF-60',
                'ULTRAVID','ULTRAVD','GEOVID','TRINOVID',
                'TRIPOD','BALL HEAD','TABLETOP','CARBON TRAVEL',
                'EVF2','VC METER','HANDGRIP','FINGER LOOP','SYSTEM CASE',
                'SCA-ADAPTER','ELPRO','VTROO','OZTNO','APDOO',
                'SGOOD','SBKOO','SHOOC','SAIOO','SUOOQ','SOOTF','SOOGZ','XOOIM',
                'SERIE ','SERIE7','SERIE8','POCKET WATCH','RAPIDWINDER',
                'WOTANCRAFT','FOGG ','OBERWERTH','ABRAHAMSSON',
                'UVA','UV/IR','UVIR','YELLOW FI','A36 ORANGE','A36-E']
    if any(x in n for x in flash_kw):
        return "Accessory"
    # ── Q 시스템 ──
    if re.search(r'^\[.*?\]\s*Q[2-3P]?[\s\(\-]', n) or re.search(r'^\[.*?\]Q[2-3]?', n):
        return "Q"
    # ── SL 바디 단독 표기 ──
    if re.search(r'^\[.*?\]\s*SL\s*[\(\-\s]|^\[.*?\]\s*SL$', n):
        return "SL"
    # ── TL2 → SL ──
    if re.search(r'^\[.*?\]\s*TL2?\s*[\(\-\s]', n):
        return "SL"
    # ── ZM 렌즈 → M ──
    if 'ZM' in n and any(x in n for x in ['ZEISS','BIOGON','DISTAGON','PLANAR','SONNAR']):
        return "M"
    # ── Voigtlander → M ──
    if any(x in n for x in ['VOIGTLANDER','보이그랜더']) and        not any(x in n for x in ['FINDER','METER','파인더']):
        return "M"
    # ── Sigma/파나소닉/루믹스 L마운트 → SL ──
    if 'SIGMA' in n and any(x in n for x in ['SL 마운트','L 마운트','L마운트','SL마운트','DG DN','HSM','L MOUNT']):
        return "SL"
    if any(x in n for x in ['파나소닉','루믹스','PANASONIC','LUMIX']) and        any(x in n for x in ['L 마운트','L마운트','L MOUNT',' S ']):
        return "SL"
    # ── R8/R9 바디 → R ──
    if re.search(r'^\[.*?\]\s*R[89]\s*[\(\-\s]', n):
        return "R"
    # ── IIIf/IIIc 등 바르낙 약식 → L ──
    if re.search(r'^\[.*?\]\s*III[A-Z]?\s*[\(\-\s]', n):
        return "L"
    # ── MDa → M ──
    if re.search(r'^\[.*?\]\s*MDA?\s', n):
        return "M"
    # ── M-Rokkor → M ──
    if 'M-ROKKOR' in n or 'M ROKKOR' in n:
        return "M"
    # ── M50/, M35/ 약식 → M ──
    if re.search(r'^\[.*?\]\s*M\d+/\d', n):
        return "M"
    # ── Thambar, KE-7A, Summcron-C → L ──
    if any(x in n for x in ['THAMBAR','KE-7A','KE7A','LOCTILUX','SUMMCRON-C','SUMMICRON-C']):
        return "L"
    # ── LEICA C 바디 → Compact ──
    if re.search(r'LEICA C SN\.|LEICA C \(TY|LEICA C2-ZOOM', n):
        return "Compact"
    # ── LEICA S-E → S ──
    if re.search(r'LEICA S-E', n):
        return "S"
    # ── LTM → L ──
    if 'LTM' in n:
        return "L"
    # ── MS-Optics → M ──
    if 'MS-OPTICS' in n or 'MS OPTICS' in n:
        return "M"
    # ── Extender L → SL ──
    if 'EXTENDER L' in n:
        return "SL"
    # ── TTArtisan L → SL ──
    if 'TTARTISAN' in n and any(x in n for x in ['L MOUNT','L- MOUNT',' L ']):
        return "SL"

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
    return " | ".join(dict.fromkeys(found_tags)) if found_tags else "세대미상"  # 순서 고정 (set은 실행마다 순서가 달라짐)

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
]
# 명백한 악세사리 코드네임 (5자리 영문/숫자)
ACCESSORY_CODES = [
    'itooy', 'irooa', 'sbooi', 'viooh', 'sbloo', 'sgvoo', 'iufoo',
    'e39', 'e43', 'e46', 'e49', 'evf2', 'sf20', 'sf24', 'sf26', 'sf40', 'sf58', 'sf64',
    'xooim', 'sgood', 'sbkoo', 'shooc', 'sootf', 'soogz', 'saioo', 'elpro', 'vtroo',
    'fookh', 'fison', 'tooca', 'valoo', 'itdoo', 'irooa',
    '12585', '12504', '12501', '14464', '14066', '12522', '12526',
    '12564', '12575', '12595', '14100', '14101', '14269', '14358',
]

# 분류용 대략 환율 (가격 문자열 기호 → 원화)
PRICE_SYMBOL_TO_KRW = {'¥': 9, '£': 1800, '€': 1500, 'A$': 880, '$': 1350, 'CHF': 1650, 'DKK': 200, 'MYR': 300, 'zł': 370, 'NZ$': 800, 'SEK': 130, 'Kč': 62}

def detect_category(name, price_str=""):
    """상품명/가격으로 카테고리 분류 (Accessory 최우선, 렌즈 보호)"""
    n = name.lower()
    nu = name.upper()

    # ── 0순위: 판매완료/보류 → Accessory ──
    if '판매완료' in name or '보류' in name: return "Accessory"
    # ── 렌즈 보호 체크 (조리개값 또는 렌즈 키워드 있으면 보호) ──
    is_lens = any(kw in n for kw in LENS_PROTECT_KW) or _has_aperture(name)

    # ── 0순위: 악세사리 코드네임 → 무조건 Accessory ──
    # 단, E39~E49 필터 구경은 렌즈 이름에도 붙으므로 (예: Summilux-M 50mm F1.4 E43) 렌즈면 건너뜀
    filter_codes = ('e39', 'e43', 'e46', 'e49')
    if any(code in n for code in ACCESSORY_CODES if not (is_lens and code in filter_codes)):
        return "Accessory"

    # ── 1순위: Accessory 키워드 (단, 렌즈 보호 키워드 없을 때만) ──
    # 단독 악세사리 키워드 (렌즈 이름 없이 단독으로 있는 경우)
    strict_acc_kw = [
        '후드', '스트랩', 'hood', 'strap', 'case', '케이스',
        '파인더', 'viewfinder', 'view finder', 'finder', 'adapter', '어댑터',
        'grip', '그립', 'cover', '커버', 'pouch', '파우치',
        'charger', '충전기', 'battery', '배터리', 'cable', '케이블',
        'flash', '플래시', '리어캡', '프론트캡', 'front cap', 'rear cap',
        'eye cup', 'lens cap', 'body cap',
        'leicavit', 'rapidwinder', 'rapid winder',
        'e39 uva','e43 uva','e46 uva','e49 uva','43mm uva','yellow fiter','yellow filter',
        'm motor','10x25','10×25','view finder','21-24-28mm','evf2','evf 2',
        'sf20','sf24','sf26','sf40','sf58','sf64','sf-20','sf-26','sf-60',
        'ultravid','ultravd','150 jahre','stemar','stereo','tripod','ball head',
        'evf2', 'evf 2', 'sf60', 'sf 60', 'sf40', 'sf 40', 'sf24', 'sf 24',
        '21-24-28mm view','21-24-28mm','view finder','10×25','10x25','150 jahre','jahre photo','jahre photographie',
        'bc sn','leica t ','leica ig ','visoflex',
        'uv filter', 'polariz', 'polfilter',
        'handgrip', 'hand grip', 'thumbs up', 'thumb up',
        'protector', 'holster', 'wrist strap', 'neck strap',
        'motor winder', 'trigger',
        'correction lens', 'diopter',
        'close-up device',
        'accessory',
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
                # 외화는 원화로 대략 바꿔서 50만원 기준 적용
                for sym, rate in PRICE_SYMBOL_TO_KRW.items():
                    if sym in price_str:
                        p *= rate
                        break
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
        "active_first": True,  # 판매 중이 목록 앞 → 증분 수집 가능
        "base": "https://leica-storebando.co.kr",
        "categories": [
            "https://leica-storebando.co.kr/product/list.html?cate_no=442",  # 충무로
            "https://leica-storebando.co.kr/product/list.html?cate_no=436",  # 대치
        ],
        "통화": "KRW",
    },
    {
        "name": "사진집",
        "active_first": True,  # 판매 중이 목록 앞 → 증분 수집 가능
        "base": "https://www.sazinzibb.com",
        "categories": [
            "https://www.sazinzibb.com/category/%EC%A4%91%EA%B3%A0%EC%83%81%ED%92%88/27/",
            "https://www.sazinzibb.com/category/%EC%9C%84%ED%83%81%EC%A0%9C%ED%92%88/28/",
        ],
        "통화": "KRW",
    },
    {
        "name": "장씨카메라",
        "active_first": True,  # 판매 중이 목록 앞 → 증분 수집 가능
        "base": "https://j-camera.com",
        "categories": [
            "https://j-camera.com/product/list.html?cate_no=358",
            "https://j-camera.com/product/list.html?cate_no=421",  # 악세사리
        ],
        "통화": "KRW",
    },
    {
        "name": "국민카메라",
        "active_first": False,  # 판매 중·위탁이 등록순으로 섞여 있어 매번 전체 (10쪽 안팎)
        "name_fix": lambda t: _kookmin_name(t),
        "base": "https://kookmincamera.co.kr",
        "categories": [
            "https://kookmincamera.co.kr/product/list.html?cate_no=530",  # 라이카 - USED(중고)
        ],
        "통화": "KRW",
    },
    {
        "name": "무한카메라",
        "active_first": False,  # 판매 중·판매완료가 섞여 있어 매번 전체 (50쪽 안팎)
        "name_fix": lambda t: _muhan_name(t),
        "base": "https://muhan8.co.kr",
        "categories": [
            "https://muhan8.co.kr/product/list.html?cate_no=105",  # BODY
            "https://muhan8.co.kr/product/list.html?cate_no=106",  # LENS
            "https://muhan8.co.kr/product/list.html?cate_no=107",  # Accessory (Hood, Filter, Etc..)
        ],
        "통화": "KRW",
    },
    {
        "name": "일광카메라",
        "active_first": False,  # 분류마다 판매 중·품절이 섞여 매번 전체 (라이카 분류 6곳, 쪽당 12개)
        "name_fix": lambda t: _ilkwang_name(t),
        "base": "https://ilkwang.co.kr",
        "categories": [
            "https://ilkwang.co.kr/product/list.html?cate_no=523",  # 렌즈교환식(필름) > 라이카
            "https://ilkwang.co.kr/product/list.html?cate_no=728",  # 미러리스 > 라이카
            "https://ilkwang.co.kr/product/list.html?cate_no=721",  # 일체형/컴팩트 > 라이카
            "https://ilkwang.co.kr/product/list.html?cate_no=978",  # 일체형/컴팩트(필름) > 라이카
            "https://ilkwang.co.kr/product/list.html?cate_no=545",  # SLR렌즈 > 라이카
            "https://ilkwang.co.kr/product/list.html?cate_no=938",  # 미러리스렌즈 > 라이카
        ],
        "통화": "KRW",
    },
    {
        "name": "신성카메라",
        "active_first": False,  # 판매된 물건은 목록에서 빠짐 (라이카 분류 3곳 20개 안팎)
        "name_fix": lambda t: _scamera_name(t),
        "cond_fix": lambda t: _scamera_grade(t),
        "base": "https://scamera.co.kr",
        "categories": [
            "https://scamera.co.kr/product/list.html?cate_no=53",  # 중고 35mm카메라 > 라이카
            "https://scamera.co.kr/product/list.html?cate_no=93",  # 중고 35mm렌즈 > 라이카
            "https://scamera.co.kr/product/list.html?cate_no=48",  # 중고 DSLR카메라 > 라이카
        ],
        "통화": "KRW",
    },
    {
        "name": "강산 중고샵",
        "active_first": False,  # 판매 중·품절 섞임, 라이카 카메라 79·렌즈 66개 (쪽당 12개)
        "name_fix": lambda t: _ekangsan_name(t),
        "base": "https://www.ekangsan.com",
        "categories": [
            "https://www.ekangsan.com/product/list.html?cate_no=108",  # 카메라 > 라이카
            "https://www.ekangsan.com/product/list.html?cate_no=163",  # 렌즈 > LEICA
        ],
        "통화": "KRW",
    },
    {
        "name": "UA카메라",
        "active_first": False,  # 라이카 분류가 없어 사이트 검색 '라이카' 결과(40여 개, 판매 중·품절 섞임)
        "name_fix": lambda t: _uacamera_name(t),
        "base": "https://uacamera.co.kr",
        "categories": [
            "https://uacamera.co.kr/product/search.html?keyword=%EB%9D%BC%EC%9D%B4%EC%B9%B4",  # 검색 '라이카'
        ],
        "통화": "KRW",
    },
    {
        "name": "THE CAMERA",
        "active_first": False,  # 여러 브랜드가 섞인 중고·위탁 분류 (쪽당 100개), 라이카 위탁 60여 개
        "name_fix": lambda t: _thecamera_name(t),
        "base": "https://thecamera.co.kr",
        "categories": [
            "https://thecamera.co.kr/product/list.html?cate_no=105",  # 위탁상품
            "https://thecamera.co.kr/product/list.html?cate_no=97",  # 중고카메라
            "https://thecamera.co.kr/product/list.html?cate_no=344",  # 중고 렌즈
        ],
        "통화": "KRW",
    },
]

def _thecamera_name(title):
    """THE CAMERA(임성재tv) 제목 '[위탁] Leica M10-P + 라이카 엄지그립 [4072]' → 'Leica M10-P + 라이카 엄지그립'
    ('[위탁]'·'[중고]' 머리말과 끝 관리번호 빼기). 라이카·라이츠가 아니거나 '추가결제' 같은 결제용 상품이면 빈 이름(건너뜀)"""
    t = re.sub(r"^\s*(?:\[[^\]]*\]\s*)+", "", title)
    t = re.sub(r"\s*\[?\b\d{4}\]?\s*$", "", t)
    if not re.match(r"(?:라이카|라이츠|leica|leitz)\b", t, re.I) or re.search(r"추가\s*결제|결제\s*전용", t):
        return ""
    t = re.sub(r"(?i)\bvariso\b", "Vario", t)  # 오타
    t = re.sub(r"(?i)\bvario\s+(elmar|elmarit)", r"Vario-\1", t)
    t = re.sub(r"\s+-\s+(?=[RM]\b)", "-", t)  # 'Summilux - R' → 'Summilux-R'
    t = re.sub(r"(?i)\s*\+\s*(?:hood|후드)\b", "", t)  # 덤 후드
    t = re.sub(r"(?i)\b(\d(?:\.\d)?)\s*cm\b", lambda m: f"{round(float(m.group(1)) * 10)}mm", t)  # '5Cm' → '50mm'
    if re.search(r"(?i)\brigid\b", t) and not re.search(r"(?i)summicron", t):
        t = re.sub(r"(?i)\b50mm\b", "Summicron 50mm", t, count=1)  # '50mm F2 1st Rigid'
    m = re.match(r"(?i)(leica)\s+R\s+(\d+)mm\s+f?\s*(\d(?:\.\d)?)\b(.*)$", t)
    if m:  # 'Leica R 50mm F1.4 …' 렌즈 이름 빠진 R 렌즈 → 화각·조리개로 이름 채움 (100mm f2.8처럼 둘 이상이면 그대로)
        fam = {("50", "1.4"): "Summilux-R", ("50", "2"): "Summicron-R", ("19", "2.8"): "Elmarit-R", ("28", "2.8"): "Elmarit-R",
               ("35", "2.8"): "Elmarit-R", ("90", "2"): "Summicron-R", ("135", "2.8"): "Elmarit-R", ("180", "2.8"): "Elmarit-R",
               ("35", "2"): "Summicron-R", ("24", "2.8"): "Elmarit-R"}.get((m.group(2), m.group(3).rstrip("0").rstrip(".") if "." in m.group(3) else m.group(3)))
        if fam:
            t = f"{m.group(1)} {fam} {m.group(2)}mm f/{m.group(3)}{m.group(4)}"
    return re.sub(r"\s+", " ", t).strip()


def _ilkwang_name(title):
    """일광카메라 제목 '중고/라이카 필름카메라 M3[92%]' → '라이카 M3' ('중고/'·'필름카메라'·'디지털카메라'·[92%] 빼기 — %는 카드 글에서 상태로 읽음), 라이카·라이츠 아니면 빈 이름"""
    t = re.sub(r"^(?:중고|위탁)\s*/\s*", "", title)
    if not re.match(r"(?:라이카|라이츠|leica|leitz)\b", t, re.I):
        return ""
    t = re.sub(r"\s*(?:필름|디지털)카메라\s*", " ", t)
    t = re.sub(r"\[\d{2,3}%\]", " ", t)  # 상태 %는 카드 글에서 따로 읽음
    return re.sub(r"\s+", " ", t).strip()


def _scamera_name(title):
    """신성카메라 제목 '[중고-위탁판매] 라이카 LEICA M6 TTL 0.72 BODY 박스품 (S)' → 'LEICA M6 TTL 0.72 BODY'
    (머리말·'라이카'·끝 등급·박스품·s/n·덧붙인 구성품 문구 빼기)"""
    if re.search(r"(?i)보이그랜더|voigtl|썬포토|7artisans|ttartisan", title):
        return ""  # 'For 라이카 M 마운트' 다른 회사 렌즈 (빈 이름은 수집기가 건너뜀)
    t = re.sub(r"^\[[^\]]*\]\s*", "", title)
    t = re.sub(r"^(?:라이카|미니룩스)\s+", "", t)
    t = re.sub(r"\s*\((?:S|A\+|A|A-|B\+|B|B-|C\+|C)\)\s*$", "", t)
    t = re.sub(r"\s*[,+]?\s*(?:박스품|정품|라이카코리아 정품|스트랩포함|케이스포함)\b", "", t)
    t = re.sub(r"\s*s/n\s*[\d*x]+\S*", "", t, flags=re.I)
    t = re.split(r"\s\+\s(?=.*(?:후드|필터|UV|B\+W|B$|케이스|캡|스트랩))", t)[0]
    t = re.sub(r"\s*-\s*\[[^\]]*\]\s*$", "", t)
    return re.sub(r"\s+", " ", t).strip(" ,+-")


def _scamera_grade(title):
    """제목 끝 등급 '(A+)' → 'SC: A+' (없으면 None)"""
    m = re.search(r"\((S|A\+|A|A-|B\+|B|B-|C\+|C)\)\s*$", title.strip())
    return "SC: " + m.group(1) if m else None


def _uacamera_name(title):
    """UA카메라 검색 '라이카' 결과 다듬기: 라이카 제품만 ('시그마 … (L마운트 / 라이카…)'·'파나소닉 라이카 DG …'는 빈 이름 → 빠짐),
    앞의 '라이카' → 'Leica', '(해외배송 가능상품)' 꼬리 뗌"""
    t = re.sub(r"\s*\(해외배송[^)]*\)", "", title).strip()
    if not re.match(r"(?:라이카|leica|leitz)\b", t, re.I) or re.search(r"파나소닉|panasonic", t, re.I):
        return ""
    return re.sub(r"^라이카\s*", "Leica ", t)


def _ekangsan_name(title):
    """강산 중고샵 제목 '[중고]   라이카 Leica SUMMICRON 35mm F2 ASPH.(3878847)' → 'Leica SUMMICRON 35mm F2 ASPH.' (머리말·'라이카'·끝 일련번호 빼기)"""
    if re.search(r"(?i)파나소닉|panasonic|lumix|ttartisan|7artisans|voigtl|보이그랜더", title):
        return ""  # 라이카 분류에 섞인 다른 회사 물건
    t = re.sub(r"^\[[^\]]*\]\s*", "", title)
    t = re.sub(r"^라이카\s+", "", t)
    t = re.sub(r"\b(\d{2,3})mf(\d)", r"\1mm f\2", t)  # 'M 50mf2' 오타
    t = re.sub(r"\s*\[(?:No|NO)?[\dA-Za-z-]{5,}\]\s*$", "", t)  # 끝 '[No4648-05]' 관리 번호
    t = re.sub(r"(\d{2,3})mm(F\d)", r"\1mm \2", t)
    t = re.sub(r"\s*\((?:[\dXx*]{4,}|[A-Z]?\d{3,}[Xx*]*)\)\s*$", "", t)
    return re.sub(r"\s+", " ", t).strip()


# 국민카메라 제목은 렌즈 이름 없이 '라이카 M 50mm f2'처럼 마운트·초점거리·조리개만 적는 일이 많아, 그 셋으로 라이카 렌즈가
# 하나로 정해질 때만 이름을 채운다 (M 90/2.8은 Elmarit·Tele-Elmarit, R 180/2.8은 Elmarit·APO-Elmarit, L 50/2는 Summicron·
# Summitar라 채우지 않음 — 틀린 모델에 붙이는 것보다 안 붙는 게 낫다)
_KOOKMIN_FAMILY = {
    "M": {(21, 2.8): "Elmarit-M", (21, 3.4): "Super-Angulon", (24, 2.8): "Elmarit-M", (24, 1.4): "Summilux-M",
          (28, 2.8): "Elmarit-M", (28, 2.0): "Summicron-M", (28, 5.6): "Summaron", (28, 1.4): "Summilux-M",
          (35, 1.4): "Summilux-M", (35, 2.0): "Summicron-M", (35, 2.8): "Summaron", (35, 3.5): "Summaron",
          (35, 2.5): "Summarit-M", (50, 0.95): "Noctilux-M", (50, 1.0): "Noctilux-M", (50, 1.1): "Noctilux-M",
          (50, 1.2): "Noctilux", (50, 1.4): "Summilux-M", (50, 1.5): "Summarit", (50, 2.0): "Summicron-M",
          (50, 2.8): "Elmar-M", (50, 3.5): "Elmar", (75, 1.4): "Summilux-M", (75, 2.0): "APO-Summicron-M",
          (75, 2.5): "Summarit-M", (90, 2.0): "Summicron-M", (135, 2.8): "Elmarit-M", (65, 3.5): "Elmar"},
    "R": {(15, 2.8): "Elmarit-R", (16, 2.8): "Fisheye-Elmarit-R", (19, 2.8): "Elmarit-R", (21, 2.8): "Elmarit-R",
          (21, 4.0): "Super-Angulon-R", (24, 2.8): "Elmarit-R", (28, 2.8): "Elmarit-R", (35, 1.4): "Summilux-R",
          (35, 2.0): "Summicron-R", (35, 2.8): "Elmarit-R", (50, 1.4): "Summilux-R", (50, 2.0): "Summicron-R",
          (60, 2.8): "Macro-Elmarit-R", (80, 1.4): "Summilux-R", (90, 2.0): "Summicron-R", (90, 2.8): "Elmarit-R",
          (100, 2.8): "APO-Macro-Elmarit-R", (135, 2.8): "Elmarit-R", (180, 3.4): "APO-Telyt-R", (180, 2.0): "APO-Summicron-R",
          (250, 4.0): "Telyt-R", (280, 2.8): "APO-Telyt-R", (350, 4.8): "Telyt-R"},
    "R_ZOOM": {"21-35": "Vario-Elmar-R", "28-70": "Vario-Elmar-R", "35-70": "Vario-Elmar-R", "70-210": "Vario-Elmar-R",
               "80-200": "Vario-Elmar-R", "70-180": "Vario-APO-Elmarit-R"},
}
_KOOKMIN_KO = [  # 한글 렌즈 이름·말 → 영어 (긴 것 먼저)
    (r"레드\s?엘마", "Red Elmar"), (r"스마론|summiron", "Summaron"), (r"슈마리트", "Summarit"), (r"슈미타", "Summitar"),
    (r"엘마리트|ELMMARIT", "Elmarit"), (r"엘마|ELMMAR\b", "Elmar"), (r"주미크론|즈미크론", "Summicron"),
    (r"주미룩스|즈미룩스", "Summilux"), (r"녹티룩스", "Noctilux"), (r"비조렌즈", "Visoflex"), (r"바르낙", "Barnack"),
    (r"리지드", "Rigid"), (r"침동", "Collapsible"), (r"블랙\s?크롬", "Black Chrome"), (r"블랙\s?페인트|페인팅", "Black Paint"),
    (r"실버", "Silver"), (r"사파리", "Safari"), (r"티타늄|\bTi\b", "Titanium"), (r"토륨렌즈", "Thorium"),
    (r"6군\s?8매", "8 elements"), (r"루끼(?:개조)?", "goggles"), (r"피니시", "finish"), (r"\(?신품\)?", "New"),
    (r"Ⅲ\s?([a-gA-G])\b", lambda m: "III" + m.group(1).lower()), (r"Ⅲ", "III"), (r"Ⅱ", "II"),
    (r"\bM\s?바디\s*\((\d{3})\)", r"M (Typ \1) Body"), (r"\bQ1\b", "Q (Typ 116)"), (r"\bRE\s+바디", "R-E Body"),
    (r"바디", "Body"),
    (r"(\d)세대", lambda m: m.group(1) + {"1": "st", "2": "nd", "3": "rd"}.get(m.group(1), "th")),
]
_KOOKMIN_FAMILY_WORDS = r"summ|elmar|noctilux|angulon|telyt|hektor|thambar|xenon|apo|visoflex|tri-elmar|wate|macro"


def _kookmin_name(title):
    """국민카메라 제목 다듬기: '1853 라이카 M 50mm f2 2세대' → 'Leica Summicron-M 50mm f2.0 2nd',
    '[4433] LEICA 라이카 SUMMICRON 90mm F2 1세대 위탁' → 'Leica SUMMICRON 90mm f2.0 1st'. 앞의 재고 번호·'위탁'·'(BOX)'는 떼고,
    'A.S'·'A S'·'A•S'는 ASPH"""
    name = re.sub(r"^\s*(?:\[\d+\]|\(\d+\)|\d{3,4})\s*", "", title)
    if re.search(r"아티산|artisan|라이트\s?렌즈|^라이트\b|코니카|미놀타|소련|동독|레뷰논|아베논|zenitar|voigt|보이그|캐논|니콘", name, re.I):
        return ""  # 다른 회사 렌즈 (빈 이름은 목록에서 빠짐)
    name = re.sub(r"\(?위탁(?:상품)?\)?|\(BOX\)|박스품?|\(\d+컷\)|\(NO \d+ 넘버\)", " ", name)
    name = re.sub(r"\bA\s?[.•·]?\s?S\b\.?", "ASPH", name)
    name = re.sub(r"^\s*(?:LEICA\s+)?라이카\s*", "Leica ", name)
    for ko, en in _KOOKMIN_KO:
        name = re.sub(ko, en, name, flags=re.I)
    name = re.sub(r"\b(\d{2,3})mm\s*/\s*(\d(?:\.\d)?)\b", r"\1mm f\2", name)  # '50mm/2' → '50mm f2'
    name = re.sub(r"\b[fF](\d)(?![\d.])", r"f\1.0", name)
    name = re.sub(r"\bF(\d\.\d)", r"f\1", name)
    if not re.search(_KOOKMIN_FAMILY_WORDS, name, re.I):
        zm = re.search(r"(?:\bR\s+|Leica\s+)(\d{2,3}-\d{2,3})mm", name)  # 이 줌들은 R 렌즈뿐
        pm = re.search(r"\b(M|R|L)?\s*(\d{2,3})mm\s+f(\d(?:\.\d+)?)", name)
        fam = None
        if zm:
            fam = _KOOKMIN_FAMILY["R_ZOOM"].get(zm.group(1))
        elif pm and (pm.group(1) or "M") in ("M", "R"):
            fam = _KOOKMIN_FAMILY[pm.group(1) or "M"].get((int(pm.group(2)), float(pm.group(3))))
        if fam:
            name = re.sub(r"\b(?:M|R)\s+(?=\d{2,3}(?:-\d{2,3})?mm)", "", name, count=1)
            name = re.sub(r"(?=\b\d{2,3}(?:-\d{2,3})?mm)", fam + " ", name, count=1)
    if not re.match(r"\s*(leica|leitz|ernst)", name, re.I):
        name = "Leica " + name.strip()
    return re.sub(r"\s+", " ", name).strip(" ,-")


def _muhan_name(title):
    """무한카메라 제목 다듬기: 여러 브랜드가 '[Leica] Elmar 50mm F2.8'처럼 앞에 브랜드를 달고 섞여 있어 [Leica]·[Leitz]만 남기고
    (빈 이름은 목록에서 빠짐) 'Leica Elmar 50mm F2.8'로. 상태는 간략설명 'E95%,L93%'의 앞(외관) 숫자를 cafe24 파서가 읽음"""
    m = re.match(r"\s*\[([^\]]+)\]\s*(.*)$", title)
    if not m or not re.fullmatch(r"\s*(?:leica|leitz|ernst leitz)\s*", m.group(1), re.I):
        return ""
    name = m.group(2)
    name = re.sub(r"\s*(?:외부|상태|내부)?\s*\d{2,3}\s?%.*$|\s*\[[^\]]*\].*$|\s*/\s*위탁제품.*$", "", name)  # 상태·구성품 꼬리
    name = re.sub(r"\s*\((?:스틸림 복각|[^)]*포함)\)|\s*(?:미사용\s?신품|신동품|미사용).*$", "", name)
    name = re.sub(r"\b[lI]{3}\s?([a-gA-G])\b", lambda m: "III" + m.group(1).lower(), name)  # 'lllf' → 'IIIf'
    name = re.sub(r"\b[lI]{2}\s?([a-gA-G])\b", lambda m: "II" + m.group(1).lower(), name)
    name = re.sub(r"\bll\b", "II", name)
    name = re.sub(r"\b[sS]liver\b", "Silver", name)
    name = re.sub(r"\bF/\s?(\d)", r"F\1", name)
    name = re.sub(r"\bM 1\b", "M1", name)
    name = re.sub(r"\s*\(NEW\)", "", name)  # 'Summilux II FLE (NEW)'는 새 버전이라는 뜻 (신품 아님)
    name = name.replace("앞캡", "front cap").replace("뒷캡", "rear cap")
    for ko, en in (("마이크", "Microphone adapter"), ("후드", "hood"), ("하판", "bottom plate"), ("케이스", "case"),
                   ("그립", "grip"), ("필터", "filter"), ("스트랩", "strap")):
        name = name.replace(ko, en)  # 액세서리가 '… M240 마이크'처럼 바디 이름으로 붙지 않게
    name = re.sub(r"(\b(?:28mm f5\.6|35mm f2\.8)\b.*?)\bSUMMICRON\b", r"\1Summaron", name, flags=re.I)  # 매장 오기 (Summicron은 f2)
    for ko, en in (("침동", "Collapsible"), ("토륨렌즈", "Thorium"), ("리지드", "Rigid"), ("복각", "Reissue"),
                   ("블랙페인트", "Black Paint"), ("실버", "Silver"), ("블랙", "Black"), ("마운트", " mount")):
        name = re.sub(ko, en, name)
    name = re.sub(r"(\d{2,3})mm\s?F\s?(\d(?:\.\d)?)", r"\1mm f\2", name)
    name = re.sub(r"\bF\s?(\d(?:\.\d)?)\b", r"f\1", name)
    return ("Leica " + re.sub(r"\s+", " ", name)).strip(" ,-")


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
                page.goto(url, wait_until="domcontentloaded", timeout=30_000)
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

                    # 판매완료/보류 텍스트 제외
                    if re.search(r'^\d+[-\s]*판매완료|^\d+[-\s]*보류', name):
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
    # ── 오타 보정 (맨 앞에서 처리) ──
    import re as _re_typo
    _typo_map = [
        ("summicrom","summicron"), ("summiarit","summarit"), ("loctilux","noctilux"),
        ("elmatit","elmarit"), ("eleamrit","elmarit"), ("elemarit","elmarit"),
        ("summcron-c","summicron-c"), ("summcron","summicron"), ("summmicron","summicron"),
        ("summicton","summicron"), ("apo-sumicron","apo-summicron"),
        ("super -elmar","super-elmar"), ("super-angvlon","super-angulon"),
        ("tri-elamr","tri-elmar"), ("tri elamr","tri-elmar"),
        ("summroan","summaron"), ("suimmilux","summilux"),
    ]
    for _wrong, _right in _typo_map:
        if _wrong in n: n = n.replace(_wrong, _right)
    if _re_typo.search(r'sui+mmilux', n): n = _re_typo.sub(r'sui+mmilux','summilux',n)
    # 판매완료/보류 → 빈 문자열
    if re.search(r"판매완료|보류|-판매|sold out", n): return ""

    # ── 판매완료/보류 포함된 상품명 ──
    if '판매완료' in name or '보류' in name or re.search(r'^\d+\s*-\s*(판매완료|보류)', name): return ""

    # ── 충무로 단축 표기 R 렌즈 (예: R 100/2.8, R 19/2.8) ──
    _n_strip = n.strip().lstrip('[중고] ').lstrip('[위탁] ')
    _r_lens_match = re.search(r'^r\s+(\d+)[-/]', _n_strip)
    if _r_lens_match:
        mm = _r_lens_match.group(1)
        return f"{mm}mm R Lens"
    _r_zoom_match = re.search(r'^r\s+(\d+)-(\d+)', _n_strip)
    if _r_zoom_match:
        return f"{_r_zoom_match.group(1)}-{_r_zoom_match.group(2)}mm R Zoom"
    _r_zoom2 = re.search(r'^r\s+(\d+)-(\d+)\s*/\s*', _n_strip)
    if _r_zoom2:
        return f"{_r_zoom2.group(1)}-{_r_zoom2.group(2)}mm R Zoom"

    # ── 충무로 단축 표기 S 렌즈 (예: S 35/2.5) ──
    _s_lens_match = re.search(r'^s\s+(\d+)/', _n_strip)
    if _s_lens_match:
        mm = _s_lens_match.group(1)
        return f"{mm}mm S Lens"

    # ── 충무로 단축 표기 TL 렌즈 (예: TL 11-23) ──
    _tl_match = re.search(r'^tl\s+(\d+)', _n_strip)
    if _tl_match:
        return "TL Lens"

    # ── ZM 렌즈 (Zeiss M마운트) ──
    if "zm " in n or " zm" in n: return "3rd Party"

    # ── L 35/3.5 Summaron 오타 ──
    if "summroan" in n: n = n.replace("summroan", "summaron")

    # ── O-series (초기 바르낙) ──
    if "o-series" in n or "o series" in n: return "Leica O-Series"

    # ── R 마운트 렌즈 (M 마운트보다 먼저 체크) ──
    _is_r = any(x in n for x in ["elmarit-r","summicron-r","summilux-r","apo-macro-elmarit",
                                   "macro-elmarit-r","vario-apo-elmarit","vario-elmar-r",
                                   "vario-elmarit-r","telyt-r","apo-telyt-r"])
    if _is_r:
        import re as _re9
        mm_r = _re9.search(r'(\d+)(?:mm|/)', n)
        mm = mm_r.group(1) if mm_r else ""
        if "apo-macro" in n or "macro-elmarit" in n:
            if mm: return f"{mm}mm APO-Macro-Elmarit-R"
            return "APO-Macro-Elmarit-R"
        if "summilux-r" in n:
            if mm: return f"{mm}mm Summilux-R"
            return "Summilux-R"
        if "summicron-r" in n:
            if mm: return f"{mm}mm Summicron-R"
            return "Summicron-R"
        if "elmarit-r" in n:
            if mm: return f"{mm}mm Elmarit-R"
            return "Elmarit-R"
        if "vario" in n and mm: return f"Vario-{mm}mm R"
        if mm: return f"{mm}mm R Lens"

    # ── Noctilux (키워드 명시 또는 조리개로 추론) ──
    if "noctilux" in n or "loctilux" in n:
        if "0.95" in n: return "50mm Noctilux f0.95"
        if "75" in n or "1.25" in n: return "75mm Noctilux f1.25"
        if "1.2" in n and "1.25" not in n: return "50mm Noctilux f1.2"
        if "original" in n: return "50mm Noctilux f1.2"  # 충무로 1세대 표기
        if "1.0" in n: return "50mm Noctilux f1.0"
        return "Noctilux"
    # 복각 + 1.2 → Noctilux f1.2
    _nocti_exc = ['filter','필터','hood','후드','cap','case','strap','serie','canon','nikon','sony','fuji','sigma dp']
    if '복각' in n and '1.2' in n and not any(k in n for k in _nocti_exc):
        return "50mm Noctilux f1.2"

    # 충무로/장씨 약식: "M 50/1.2", "M50/1.2", "복각" 등 → Noctilux 추론
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
        # 21mm
        if mm == "21":
            if "asph" in n: return "21mm Summilux ASPH"
            return "21mm Summilux"
        # 24mm
        if mm == "24":
            if "asph" in n: return "24mm Summilux ASPH"
            return "24mm Summilux"
        # 28mm
        if mm == "28":
            if "asph" in n: return "28mm Summilux ASPH"
            return "28mm Summilux"
        # 35mm 세분화
        if mm == "35":
            if "f2" in n and "asph" in n: return "35mm Summicron ASPH"
            if "f2" in n or "summicron" in n:
                if "8 element" in n or "8element" in n or "8매" in n: return "35mm Summicron 8-element"
                if "1세대" in n or "1st" in n: return "35mm Summicron 8-element"
                if "2세대" in n or "2nd" in n: return "35mm Summicron v2"
                if "4세대" in n or "4th" in n: return "35mm Summicron v4"
                if "5세대" in n or "5th" in n: return "35mm Summicron v5"
                if "millennium" in n: return "35mm Summicron Millennium"
                if "your mark" in n: return "35mm Summicron Your Mark"
                if "eye" in n and "summicron" in n: return "35mm Summicron Eye"
            if "aspherical" in n: return "35mm Summilux AA"
            if any(kw in n for kw in ["2매","2 매","두매","double"," aa ","(aa)"]): return "35mm Summilux AA"
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
        # 90mm
        if mm == "90":
            if "asph" in n: return "90mm Summilux ASPH"
            return "90mm Summilux"
        # 기타 mm
        if "asph" in n and mm: return f"{mm}mm Summilux ASPH"
        if mm: return f"{mm}mm Summilux"
        return "Summilux"

    # ── Summicron 세대별 ──
    if "summicron" in n:
        if "apo" in n:
            for mm in ["21","28","35","50","75","90"]:
                if mm in n: return f"{mm}mm APO-Summicron"
        import re as _re2
        mm_match = _re2.search(r"(\d+)(?:mm|/)", n)
        mm = mm_match.group(1) if mm_match else ""
        # 50mm 세분화
        if mm == "50":
            if "asph" in n: return "50mm Summicron ASPH"
            if "dr" in n or "dual" in n: return "50mm Summicron DR"
            if "rigid" in n: return "50mm Summicron Rigid"
            if "침동" in n or "collapsible" in n: return "50mm Summicron (침동)"
            if "6bit" in n or "6 bit" in n: return "50mm Summicron 6bit"
            if "50 jahre" in n or "50주년" in n: return "50mm Summicron 50th"
            if "black paint" in n or "blackpaint" in n: return "50mm Summicron Black Paint"
            if "sl " in n or "/sl" in n or "summicron-sl" in n: return "50mm Summicron SL"
            if "2세대" in n or "3세대" in n or "4세대" in n: return "50mm Summicron (올드)"
            return "50mm Summicron"
        # 35mm 세분화
        if mm == "35":
            if "f2" in n and "asph" in n: return "35mm Summicron ASPH"
            if "f2" in n or "summicron" in n:
                if "8 element" in n or "8element" in n or "8매" in n: return "35mm Summicron 8-element"
                if "1세대" in n or "1st" in n: return "35mm Summicron 8-element"
                if "2세대" in n or "2nd" in n: return "35mm Summicron v2"
                if "4세대" in n or "4th" in n: return "35mm Summicron v4"
                if "5세대" in n or "5th" in n: return "35mm Summicron v5"
                if "millennium" in n: return "35mm Summicron Millennium"
                if "your mark" in n: return "35mm Summicron Your Mark"
                if "eye" in n and "summicron" in n: return "35mm Summicron Eye"
            if "asph" in n: return "35mm Summicron ASPH"
            if "8매" in n or "8-el" in n or "8el" in n: return "35mm Summicron 1st (8매)"
            if "6매" in n or "6-el" in n: return "35mm Summicron (6매)"
            return "35mm Summicron"
        # 28mm 세분화
        if mm == "28":
            if "asph" in n: return "28mm Summicron ASPH"
            return "28mm Summicron"
        # 75mm
        if mm == "75": return "75mm Summicron"
        # 90mm 세분화
        if mm == "90":
            if "asph" in n or "apo" in n: return "90mm Summicron ASPH"
            return "90mm Summicron"
        # 40mm (CL용)
        if mm == "40": return "40mm Summicron-C"
        if mm: return f"{mm}mm Summicron"
        return "Summicron"

    # ── Elmarit ──
    if "elmarit" in n and "tri" not in n:
        import re as _re4
        mm_e = _re4.search(r'(\d+)(?:mm|/)', n)
        mm = mm_e.group(1) if mm_e else ""
        if mm == "21":
            if "asph" in n: return "21mm Elmarit ASPH"
            return "21mm Elmarit"
        if mm == "24":
            if "asph" in n: return "24mm Elmarit ASPH"
            return "24mm Elmarit"
        if mm == "28":
            if "asph" in n and "elmarit" in n: return "28mm Elmarit ASPH"
            if "asph" in n and "summicron" in n: return "28mm Summicron ASPH"
            if "asph" in n and "summilux" in n: return "28mm Summilux ASPH"
            if "asph" in n: return "28mm Elmarit ASPH"
            if "1세대" in n or "1st" in n or "9 element" in n or "9element" in n: return "28mm Elmarit 1세대"
            if "2세대" in n or "2nd" in n: return "28mm Elmarit 2세대"
            if "3세대" in n or "3rd" in n: return "28mm Elmarit 3세대"
            if "4세대" in n or "4th" in n: return "28mm Elmarit 4세대"
            if "vario" in n: return "28mm Vario-Elmarit"
            return "28mm Elmarit"
        if mm == "90":
            if "asph" in n: return "90mm Elmarit ASPH"
            return "90mm Elmarit"
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
        for mm in ["21","16","18"]:
            if mm in n: return f"{mm}mm Super-Angulon"
        return "Super-Angulon"

    # ── Super-Elmar ──
    if "super-elmar" in n or "super elmar" in n:
        import re as _re6
        mm_se = _re6.search(r'(\d+)(?:mm|/)', n)
        mm = mm_se.group(1) if mm_se else ""
        if mm: return f"{mm}mm Super-Elmar"
        return "Super-Elmar"

    # ── Thambar ──
    if "thambar" in n: return "90mm Thambar"

    # ── APO-Telyt ──
    if "apo-telyt" in n or "apo telyt" in n:
        import re as _re7
        mm_at = _re7.search(r'(\d+)(?:mm|/)', n)
        mm = mm_at.group(1) if mm_at else ""
        if mm: return f"{mm}mm APO-Telyt"
        return "APO-Telyt"

    # ── Telyt ──
    if "telyt" in n and "apo" not in n:
        import re as _re8
        mm_t = _re8.search(r'(\d+)(?:mm|/)', n)
        mm = mm_t.group(1) if mm_t else ""
        if mm: return f"{mm}mm Telyt"
        return "Telyt"

    # ── Elmar 세분화 ──
    if "elmar" in n and "elmarit" not in n and "tri" not in n and "super" not in n:
        if "50" in n or "5/2.8" in n or "5/3.5" in n:
            if "asph" in n: return "50mm Elmar-M ASPH"
            if "2.8" in n: return "50mm Elmar f2.8"
            if "3.5" in n: return "50mm Elmar f3.5"
            return "50mm Elmar"
        if "35" in n: return "35mm Elmar"
        for mm in ["90","65","24","18"]:
            if mm in n: return f"{mm}mm Elmar"
        return "Elmar"

    # ── Tri-Elmar ──
    if "tri" in n and "elmar" in n:
        if "16" in n or "21" in n: return "Tri-Elmar 16-18-21 (WATE)"
        return "Tri-Elmar 28-35-50 (MATE)"

    # ── 135mm 렌즈 ──
    if "135" in n:
        if "elmarit" in n: return "135mm Elmarit-M"
        if "tele-elmar" in n or "tele elmar" in n: return "135mm Tele-Elmar"
        if "apo-telyt" in n: return "135mm APO-Telyt"
        if "hektor" in n: return "135mm Hektor"

    # ── Ffordes 표기 렌즈 (mm + F값) ──
    import re as _re_ff
    _ff = _re_ff.search(r'^leica\s+(\d+)mm\s+f([\d\.]+)', n)
    if _ff:
        mm, fval = _ff.group(1), _ff.group(2)
        if mm=="28" and fval=="1.4": return "28mm Summilux ASPH"
        if mm=="28" and fval in ["2.8","2"]: return "28mm Elmarit ASPH"
        if mm=="28" and fval=="5.6": return "28mm Summaron"
        if mm=="50" and fval=="1.0": return "50mm Noctilux f1.0"
        if mm=="50" and fval=="1.4": return "50mm Summilux ASPH"
        if mm=="50" and fval=="3.5": return "50mm Elmar f3.5"
        if mm=="75" and fval=="2.5": return "75mm Summarit"
        if mm=="90" and fval=="2.8": return "90mm Elmarit"
        if mm=="90" and fval=="2": return "90mm Summicron"
        if mm=="100" and fval=="2.8": return "100mm APO-Macro-Elmarit-R"
        if mm=="135" and fval=="2.8": return "135mm Elmarit-M"
        if mm=="280" and fval=="2.8": return "280mm APO-Telyt-R"
        if mm=="16": return "16-35mm SL Lens"
        if mm=="28": return f"{mm}mm Elmarit"
        return f"{mm}mm Lens"
    # ── 28mm Summicron ASPH (Ffordes 표기) ──
    # 이미 Summicron 섹션에서 처리됨

    # ── ELCAN ──
    if "elcan" in n: return "50mm ELCAN"

    # ── Stemar (스테레오 렌즈) ──
    if "stemar" in n or "stereo" in n: return "Stemar"

    # ── O-series ──
    if "o-serise" in n or "o-series" in n or "o series" in n: return "Leica O-Series"

    # ── 28mm F6.3 (바르낙 렌즈) ──
    if "28" in n and "6.3" in n: return "28mm Hektor"

    # ── ASPHERICAL (35mm Summilux 1세대) ──
    if "aspherical" in n and "35" in n and "summilux" not in n: return "35mm Summilux Steel Rim"
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

    # ── 악세사리 (렌즈 키워드 없을 때) ──
    if any(x in n for x in ["10×25","10x25","21-24-28mm","view finder","150 jahre","jahre photo","bc sn"]): return "Accessory"

    # ── Bodies M 시스템 ── (렌즈 키워드 없을 때만)
    lens_kw = ["summicron","summilux","noctilux","elmarit","elmar","summaron","nokton",
                "angulon","hektor","summar","hologon","telyt","vario","apo"]
    if not any(kw in n for kw in lens_kw):
        for m in ["m11","m10","m9","m8","m7","m6","m4","m3","m2","mp","m-a","m240"]:
            if m in n.replace(" ",""): return f"Leica {m.upper()}"
    # ── Q-P 바디 ──
    if not any(kw in n for kw in lens_kw):
        if "q-p" in n.replace(" ",""): return "Leica Q-P"
    # ── T 바디 ──
    if not any(kw in n for kw in lens_kw):
        if re.search(r'leica t', n) and "tl" not in n: return "Leica T"
        if re.search(r'leica t\s+sn', n): return "Leica T"
    # ── IG 바디 ──
    if not any(kw in n for kw in lens_kw):
        if re.search(r'leica ig', n): return "Leica IG"
    # ── S-E 바디 ──
    if not any(kw in n for kw in lens_kw):
        if "leica s-e" in n: return "Leica S-E"
    # ── Barnack IID/IIC/IIIa ──
    if not any(kw in n for kw in lens_kw):
        if any(x in n for x in ["ⅱd","ⅱc","ⅲa","iid","iic","iiic","iiia","leica ⅱ","leica ⅲ","illc","illd"]): return "Leica Barnack"
    # ── Leica C 바디 ──
    if not any(kw in n for kw in lens_kw):
        if re.search(r'leica c\s+sn\.', n): return "Leica C"
    # ── T/IG 바디 (lens_kw 정의 후) ──
    if not any(kw in n for kw in lens_kw):
        _tn = n.replace('[중고]','').replace('[위탁]','').strip()
        if _tn in ["t","t (silver)","t (black)"] : return "Leica T"
        if "leica t " in n and "tl" not in n: return "Leica T"
        if n == "leica t" or re.search(r'leica t', n) and "tl" not in n: return "Leica T"
    if not any(kw in n for kw in lens_kw):
        if "leica ig" in n: return "Leica IG"
    # ── Barnack IIlC (소문자 l) ──
    if not any(kw in n for kw in lens_kw):
        if "illc" in n or "illd" in n or "iilc" in n or "iiic" in n: return "Leica Barnack"
    # ── 150 JAHRE ──
    if "jahre" in n: return "Accessory"
    # ── Tri-Elmar MATE (28-35-50) ──
    if "28-35-50" in n: return "Tri-Elmar 28-35-50 (MATE)"

    if "q3" in n: return "Leica Q3"
    if "q2" in n: return "Leica Q2"
    if "q " in n or n.endswith(" q") or "/q " in n: return "Leica Q"

    # ── SL 시스템 바디 ──
    if not any(kw in n for kw in lens_kw):
        if "sl2-s" in n.replace(" ",""): return "Leica SL2-S"
        if "sl2" in n.replace(" ",""): return "Leica SL2"
        if "sl " in n or n.endswith(" sl"): return "Leica SL"
        if " cl" in n or n.startswith("cl "): return "Leica CL"
        if "m10-r" in n.replace(" ",""): return "Leica M10-R"
        if "m10-p" in n.replace(" ",""): return "Leica M10-P"
        if "m10" in n.replace(" ",""): return "Leica M10"
        if "m11-p" in n.replace(" ",""): return "Leica M11-P"
        if "m11" in n.replace(" ",""): return "Leica M11"

    # ── Compact ──
    for c in ["d-lux","v-lux","c-lux","minilux","c2","c1","mini"]:
        if c in n: return f"Leica {c.upper()}"

    # ── Leicavit / 악세사리 ──
    if "leicavit" in n: return "Leicavit"

    # ── 3rd Party 브랜드 ──
    _3rd_brands = ["thypoch","peace ","cooke ","oberwerth","luigi","ona ","rrs ","sekonic",
                   "artisan","coiro","carlzeiss","carl zeiss","zeiss-opton","zeiss opton",
                   "meyer optik","cosina","voigtlander","bessa","prominent",
                   "sigma ","lumix ","panasonic","루믹스","시그마","파나소닉",
                   "보이그랜더","linhof","nippon kogaku","nikon","canon ","캐논","minolta",
                   "ms-optics","laowa","light lens lab","7artisan","ttartisan",
                   "fogg ","wotancraft","zeiss zm","zeiss biogon","zeiss 21","zeiss 25","zeiss 28","zeiss 35",
                   "obo ob","오버베르트","오버베르","wotancraft","fogg "]
    if any(b in n for b in _3rd_brands): return "3rd Party"

    # ── 악세사리 브랜드/키워드 ──
    if "be@rbrick" in n or "bebrick" in n: return "Accessory"

    # ── SL 렌즈 ──
    if any(x in n for x in ["super-vario-elmar-sl","vario-elmarit-sl","summicron-sl","summilux-sl","apo-summicron-sl","vario-elmar-sl"]):
        import re as _re_sl
        mm_sl = _re_sl.search(r'(\d+)(?:mm|/)', n)
        mm = mm_sl.group(1) if mm_sl else ""
        if mm: return f"{mm}mm SL Lens"
        return "SL Lens"

    # ── R 바디 ──
    if not any(kw in n for kw in lens_kw):
        for rb in ["r9","r8","r7","r6","r5","r4","r3","r-e","re "]:
            if rb in n.replace(" ",""): return f"Leica {rb.upper().strip()}"

    # ── M 바디 추가 ──
    if not any(kw in n for kw in lens_kw):
        if "m5" in n.replace(" ",""): return "Leica M5"
        if "m240" in n.replace(" ","") or "typ 240" in n or "typ240" in n.replace(" ",""): return "Leica M240"
        if "m typ 262" in n or "typ262" in n.replace(" ",""): return "Leica M262"

    # ── Barnack 추가 ──
    if not any(kw in n for kw in lens_kw):
        for bk in ["iiid","iid ","iic ","if "]:
            if bk in n: return "Leica Barnack"

    # ── S 시스템 바디 ──
    if not any(kw in n for kw in lens_kw):
        for sb in ["leica s "," s2 "," s3 "]:
            if sb in n: return "Leica S"

    # ── 악세사리 추가 ──
    if any(x in n for x in ["ev1","trinovid","televid","leica meter","macro-adapter-r","macro adapter r",
                              "lupe","self timer","pocket watch","extender","geovid","noctovid",
                              "uva e","uvb e","soft release","release button",
                              "oztno","fokos","apdoo","igemo","elpro","vtroo","xooim",
                              "sgood","sbkoo","shooc","sootf","soogz","saioo",
                              "sf20","sf24","sf26","sf40","sf58","sf64","sf 20","sf 24","sf 26","sf 40","sf 58","sf 64","sf-20","sf-26","sf-60",
                              "uva slim","serie 7 uva","serie 8 uva","uvir","uv/ir",
                              "vit m","m vit","m-vit","leicavit",
                              "handgrip","finger loop","finger loo","system case","tabletop tripod","ball head",
                              "leica bag","leica 가방","가방","tripod","sca-adapter",
                              "디옵터","diopter","correction lens",
                              "12549","12586","12521","12503","12544",
                              "flash sf","ultravid","ultravd","a36 orange"]): return "Accessory"

    # ── UVa/UV 필터 (E39/E43/E46/E49) ──
    if re.search(r'e\d{2}\s*uva|uva\s*e\d{2}|serie\s*\d+\s*uva', n): return "Accessory"

    # ── SL(Typ 601) 바디 ──
    if not any(kw in n for kw in lens_kw):
        if "typ 601" in n or "typ601" in n.replace(" ",""): return "Leica SL"
        if "typ 240" in n or "typ240" in n.replace(" ",""): return "Leica M240"
        if "typ 262" in n or "typ262" in n.replace(" ",""): return "Leica M262"
        if "tye112" in n.replace(" ",""): return "Leica C"
        if "tye240" in n.replace(" ","") or "tye 240" in n: return "Leica M240"

    # ── T/TL 바디 ──
    if not any(kw in n for kw in lens_kw):
        if "tl2" in n.replace(" ",""): return "Leica TL2"
        if re.search(r'leica t', n): return "Leica T"

    # ── M 바디 추가 ──
    if not any(kw in n for kw in lens_kw):
        if "m-9p" in n.replace(" ",""): return "Leica M9-P"
        if "m-10r" in n.replace(" ",""): return "Leica M10-R"
        if "m-240" in n.replace(" ",""): return "Leica M240"
        if "m-262" in n.replace(" ",""): return "Leica M262"
        if "monocrom" in n or "monochrom" in n: return "Leica M Monochrom"

    # ── X 시리즈 추가 ──
    if not any(kw in n for kw in lens_kw):
        if "x-u" in n.replace(" ",""): return "Leica X-U"
        if "x-1" in n.replace(" ",""): return "Leica X1"
        if "x-2" in n.replace(" ",""): return "Leica X2"
        if "x-moncler" in n.replace(" ",""): return "Leica X"
        if "x-vabio" in n.replace(" ",""): return "Leica X Vario"

    # ── Ffordes R 줌렌즈 (28-70, 28-90) ──
    import re as _re_rz
    _rz = _re_rz.search(r'leica\s+(\d+)-(\d+)mm', n)
    if _rz:
        m1, m2 = _rz.group(1), _rz.group(2)
        if "vario-elmar" in n or "super vario" in n: return f"{m1}-{m2}mm Super-Vario-Elmar"
        return f"{m1}-{m2}mm R Zoom"

    # ── LTM 렌즈 (바르낙용 줌) ──
    if "ltm" in n:
        import re as _re_ltm
        mm_ltm = _re_ltm.search(r'(\d+)-(\d+)', n)
        if mm_ltm: return f"{mm_ltm.group(1)}-{mm_ltm.group(2)}mm LTM Lens"
        return "LTM Lens"

    # ── Super-Vario-Elmar-T (TL 렌즈) ──
    if "super-vario-elmar-t" in n or "super vario elmar t" in n:
        import re as _re_svt
        mm_svt = _re_svt.search(r'(\d+)-(\d+)', n)
        if mm_svt: return f"{mm_svt.group(1)}-{mm_svt.group(2)}mm TL Lens"
        return "TL Lens"

    # ── Barnack 바디 추가 패턴 (로마숫자) ──
    if not any(kw in n for kw in lens_kw):
        if any(x in n for x in ["ⅰ ","ⅱ ","ⅲ ","ⅰf","ⅱf","ⅲf","ⅲg","iiig","iiif","standard nickel","model b","model c","model e","leica i ","leica ii ","leica iii "]): return "Leica Barnack"

    # ── Leica C 렌즈 ──
    if re.search(r'leica c\s+\d+/', n): return "Leica C Lens"

    # ── Leica CL kit ──
    if "cl vario" in n or "cl kit" in n: return "Leica CL"

    # ── Xenon (바르낙 렌즈) ──
    if "xenon" in n: return "50mm Xenon"

    # ── CM/C 컴팩트 ──
    if not any(kw in n for kw in lens_kw):
        if "cm zoom" in n or "leica cm" in n: return "Leica CM"
        if re.search(r'leica c', n) and "40" not in n: return "Leica C"

    # ── M1 바디 ──
    if not any(kw in n for kw in lens_kw):
        if "m1 " in n or n.endswith("m1"): return "Leica M1"

    # ── S 시스템 렌즈 ──
    if re.search(r's\s*\d+/', n) or re.search(r's\s*\d+mm', n):
        import re as _re_s
        mm_s = _re_s.search(r'(\d+)(?:mm|/)', n)
        mm = mm_s.group(1) if mm_s else ""
        if mm: return f"{mm}mm S Lens"

    # ── M-D 바디 ──
    if not any(kw in n for kw in lens_kw):
        if "m-d" in n.replace(" ",""): return "Leica M-D"


    if "eleamrit" in n: n = n.replace("eleamrit","elmarit")
    if re.search(r'el[ea]marit', n): n = re.sub(r'el[ea]marit','elmarit',n)
    if "apo-sumicron" in n: n = n.replace("apo-sumicron","apo-summicron")
    if "super -elmar" in n: n = n.replace("super -elmar","super-elmar")
    if "super-angvlon" in n: n = n.replace("super-angvlon","super-angulon")
    if "summiarit" in n: n = n.replace("summiarit","summarit")

    # ── Barnack 바디 ──
    if not any(kw in n for kw in lens_kw):
        for barnack in ["iiig","iiif","iiic","iiia","iif","iic","if ","i "," ii "]:
            if barnack in n: return "Leica Barnack"
        if "barnack" in n: return "Leica Barnack"

    # ── Visoflex (X2보다 먼저) ──
    if "visoflex" in n: return "Visoflex"

    # ── X Vario (vario가 lens_kw에 있어서 먼저 체크) ──
    if "leica x vario" in n or " x vario" in n or "x-vario" in n: return "Leica X Vario"

    # ── X 시리즈 바디 ──
    if not any(kw in n for kw in lens_kw):
        if "x2" in n.replace(" ",""): return "Leica X2"
        if "x1" in n.replace(" ",""): return "Leica X1"
        if "x " in n or n.endswith(" x"): return "Leica X"

    # ── SL3 추가 ──
    if not any(kw in n for kw in lens_kw):
        if "sl3" in n.replace(" ",""): return "Leica SL3"

    # ── M 모노크롬 ──
    if not any(kw in n for kw in lens_kw):
        if "monochrom" in n or "m-m" in n.replace(" ",""): return "Leica M Monochrom"
        if "m-e" in n.replace(" ",""): return "Leica M-E"
        if "m-p" in n.replace(" ",""): return "Leica M-P"

    # ── TL 시스템 렌즈 ──
    if "tl" in n and any(x in n for x in ["elmar","summicron","summilux","vario","apo"]):
        import re as _re_tl
        mm_tl = _re_tl.search(r'(\d+[-~]\d+mm|\d+mm)', n)
        mm = mm_tl.group(0).replace('mm','') if mm_tl else ""
        if mm: return f"{mm}mm TL Lens"
        return "TL Lens"

    # ── Summitar (L39) ──
    if "summitar" in n: return "50mm Summitar"

    # ── 세트 매물 (여러 렌즈) ──
    if re.search(r'\d+mm/\d+mm|\d+mm\s*/\s*\d+mm', n): return "Set"

    # ── Visoflex ──
    if "visoflex" in n: return "Visoflex"

    # ── Sofort ──
    if "sofort" in n: return "Leica Sofort"

    # ── M-D / MDa 바디 ──
    if not any(kw in n for kw in lens_kw):
        if "m-d" in n.replace(" ",""): return "Leica M-D"
        if "mda" in n.replace(" ",""): return "Leica MDa"
        if "m-a" in n.replace(" ",""): return "Leica M-A"

    # ── Barnack 로마숫자 바디 ──
    if not any(kw in n for kw in lens_kw):
        import re as _re_bn
        if _re_bn.search(r'leica\s+(i|ii|iii|if|iif|iiif|iiig|iiic|standard)', n):
            return "Leica Barnack"

    # ── SL 렌즈 ──
    if "sl" in n and any(x in n for x in ["elmar","summicron","summilux","vario","apo","elmarit"]):
        import re as _re_sl
        mm_sl = _re_sl.search(r'(\d+[-~]\d+mm|\d+mm)', n)
        mm = mm_sl.group(0).replace('mm','') if mm_sl else ""
        if "apo-summicron" in n or "apo summicron" in n:
            return f"{mm}mm APO-Summicron-SL" if mm else "APO-Summicron-SL"
        if "summilux" in n:
            return f"{mm}mm Summilux-SL" if mm else "Summilux-SL"
        if "vario" in n:
            return f"{mm}mm Vario-SL" if mm else "Vario-SL"
        if mm: return f"{mm}mm SL Lens"
        return "SL Lens"

    # ── Summicron 오타 (SUMMICROM) ──
    if "summicrom" in n:
        import re as _re_sc
        mm_sc = _re_sc.search(r'(\d+)(?:mm|/)', n)
        mm = mm_sc.group(1) if mm_sc else "50"
        return f"{mm}mm Summicron"

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
        "updated_at": datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9))).isoformat(),
        "running": pct < 100,
    }
    try:
        with open("data/status.json", "w", encoding="utf-8") as f:
            json.dump(status, f, ensure_ascii=False)
    except Exception as e:
        print(f"    ⚠️ status.json 쓰기 실패: {e}")


def crawl_leicamiami():
    """Leica Store Miami - Shopify JSON API 크롤링"""
    import urllib.request
    results = []
    base = "https://leicastoremiami.com"
    url = f"{base}/collections/used/products.json?limit=250"
    print(f"\n  📂 Leica Store Miami: {url}")
    try:
        import requests
        resp = requests.get(url, headers={"User-Agent": random.choice(USER_AGENTS)}, timeout=20)
        resp.raise_for_status()
        data = resp.json()
        products = data.get("products", [])
        print(f"    └─ {len(products)}개 상품 발견")
        for p in products:
            name = p.get("title", "").strip()
            if not name:
                continue
            variant = p["variants"][0] if p.get("variants") else {}
            price_raw = variant.get("price", "")
            try:
                price = f"${float(price_raw):,.0f}" if price_raw else "문의요망"
            except:
                price = "문의요망"
            available = variant.get("available", True)
            handle = p.get("handle", "")
            from condition_grade import ks_condition
            cond_text = ks_condition(p.get("body_html") or "") or "정보없음"
            link = f"{base}/products/{handle}" if handle else ""
            img = ""
            if p.get("images"):
                img = p["images"][0].get("src", "")
            label = auto_label(name)
            mount = detect_mount(name)
            gen = detect_generation(name)
            brand = detect_brand(name)
            cat = detect_category(name, price)
            results.append({
                "게시일": _shopify_listed(p),
                "site": "Leica Store Miami",
                "label": label,
                "상품명": name,
                "세대": gen,
                "컨디션": cond_text,
                "가격": price,
                "통화": "USD",
                "이미지": img,
                "링크": link,
                "품절": not available,
                "예약중": False,
                "mount": mount,
                "category": cat,
                "brand": brand,
            })
            print(f"    {'✔ ' if available else '✘ '} {name[:50]} | {price}")
    except Exception as e:
        print(f"    ❌ 오류: {e}")
    print(f"  ✅ Leica Store Miami 완료: {len(results)}개")
    return results


def crawl_kamerastore():
    """Kamerastore (핀란드) - Shopify JSON API, 라이카 컬렉션 전체"""
    import requests
    results = []
    base = "https://kamerastore.com"
    page_num = 1
    print(f"\n  📂 Kamerastore 크롤링 시작")
    while True:
        url = f"{base}/collections/leica/products.json?limit=250&page={page_num}"
        try:
            resp = requests.get(url, headers={"User-Agent": random.choice(USER_AGENTS)}, timeout=20)
            resp.raise_for_status()
            products = resp.json().get("products", [])
        except Exception as e:
            print(f"    ❌ {page_num}페이지 오류: {e}")
            break
        if not products:
            break
        print(f"    └─ {page_num}페이지 {len(products)}개 상품 발견")
        for p in products:
            name = (p.get("title") or "").strip()
            if not name:
                continue
            variant = p["variants"][0] if p.get("variants") else {}
            available = variant.get("available", True)
            link = f"{base}/products/{p['handle']}" if p.get("handle") else ""
            if not available or link in globals().get('SOLD_LINKS', ()):
                continue
            try:
                price = f"€{float(variant.get('price')):,.0f}"
            except (TypeError, ValueError):
                price = "문의요망"
            img = p["images"][0].get("src", "") if p.get("images") else ""
            cat = detect_category(name, price)
            mount = 'Accessory' if cat == 'Accessory' else detect_mount(name)
            from condition_grade import ks_condition
            cond_text = ks_condition(p.get("body_html") or "") or "정보없음"
            results.append({
                "게시일": _shopify_listed(p),
                "site": "Kamerastore (핀란드)",
                "label": auto_label(name),
                "상품명": name,
                "세대": detect_generation(name),
                "컨디션": cond_text,
                "가격": price,
                "통화": "EUR",
                "이미지": img,
                "링크": link,
                "품절": False,
                "예약중": False,
                "mount": mount,
                "category": cat,
                "brand": detect_brand(name),
            })
        page_num += 1
        time.sleep(random.uniform(1.0, 2.0))
    print(f"  ✅ Kamerastore 완료: {len(results)}개")
    return results


def crawl_mkkamera():
    """M & K Kamera (홍콩) - Shopify JSON API. 라이카·라이츠만, 판매 중만"""
    import requests
    from condition_grade import mk_condition
    results = []
    base = "https://mkkcamera.com"
    page_num = 1
    print(f"\n  📂 M & K Kamera 크롤링 시작")
    while True:
        url = f"{base}/products.json?limit=250&page={page_num}"
        try:
            resp = requests.get(url, headers={"User-Agent": random.choice(USER_AGENTS)}, timeout=20)
            resp.raise_for_status()
            products = resp.json().get("products", [])
        except Exception as e:
            print(f"    ❌ {page_num}페이지 오류: {e}")
            break
        if not products:
            break
        print(f"    └─ {page_num}페이지 {len(products)}개 상품 발견")
        for p in products:
            name = (p.get("title") or "").strip()
            if not name or not re.search(r"leica|leitz", f"{name} {p.get('vendor') or ''}", re.I):
                continue
            variant = p["variants"][0] if p.get("variants") else {}
            available = variant.get("available", True)
            link = f"{base}/products/{p['handle']}" if p.get("handle") else ""
            if not available or link in globals().get('SOLD_LINKS', ()):
                continue
            try:
                price = f"HK${float(variant.get('price')):,.0f}"
            except (TypeError, ValueError):
                price = "문의요망"
            name = re.sub(r"\s*#\d+\s*$", "", name)  # 끝의 매장 관리 번호(#24041) 제거
            img = p["images"][0].get("src", "") if p.get("images") else ""
            cat = detect_category(name, price)
            mount = 'Accessory' if cat == 'Accessory' else detect_mount(name)
            results.append({
                "게시일": _shopify_listed(p),
                "site": "M & K Kamera (홍콩)",
                "label": auto_label(name),
                "상품명": name,
                "세대": detect_generation(name),
                "컨디션": mk_condition(p.get("body_html") or "") or "정보없음",
                "가격": price,
                "통화": "HKD",
                "이미지": img,
                "링크": link,
                "품절": False,
                "예약중": False,
                "mount": mount,
                "category": cat,
                "brand": detect_brand(name),
            })
        page_num += 1
        time.sleep(random.uniform(1.0, 2.0))
    print(f"  ✅ M & K Kamera 완료: {len(results)}개")
    return results


def _lsg_normalize(name: str) -> str:
    """라이카 싱가포르 제목 표기 → 모델 연결이 아는 표기"""
    name = name.replace("–", "-").replace("—", "-")
    name = re.sub(r"\bf/?(\d(?:\.\d+)?)/(\d{2,3})\s?mm", r"\2mm f/\1", name, flags=re.I)  # f2/35mm → 35mm f/2
    name = re.sub(r"(?<![\w/.:])(\d(?:\.\d+)?)/(\d{2,3})\s?mm", r"\2mm f/\1", name)  # 1.4/75mm → 75mm f/1.4
    name = re.sub(r"\bM-(\d{2,3})\s?mm", r"M \1mm", name)  # Summilux M-35mm → Summilux M 35mm
    return name


def crawl_leicasg():
    """Leica Store Singapore (싱가포르) - 라이카 싱가포르 공식 몰 중고 컬렉션 (Shopify JSON, collections/pre-owned).
    등급 표기 없음, 싱가포르 안에만 배송. 판매 중만"""
    import requests
    results = []
    base = "https://leica-store.sg"
    print(f"\n  📂 Leica Store Singapore 크롤링 시작")
    for page_num in range(1, 20):
        url = f"{base}/collections/pre-owned/products.json?limit=250&page={page_num}"
        try:
            resp = requests.get(url, headers={"User-Agent": random.choice(USER_AGENTS)}, timeout=20)
            resp.raise_for_status()
            products = resp.json().get("products", [])
        except Exception as e:
            print(f"    ❌ {page_num}페이지 오류: {e}")
            break
        if not products:
            break
        print(f"    └─ {page_num}페이지 {len(products)}개 상품 발견")
        for p in products:
            name = (p.get("title") or "").strip()
            if not name:
                continue
            variant = p["variants"][0] if p.get("variants") else {}
            available = any(v.get("available") for v in p.get("variants") or [variant])
            link = f"{base}/products/{p['handle']}" if p.get("handle") else ""
            if not available or link in globals().get('SOLD_LINKS', ()):
                continue
            try:
                price = f"S${float(variant.get('price')):,.0f}"
            except (TypeError, ValueError):
                price = "문의요망"
            name = re.sub(r"\s*\(pre-?owned\)\s*$", "", name, flags=re.I)  # 끝의 (Pre-Owned) 제거
            name = re.sub(r"^Is\s+(?=Summi|Elma|Nocti)", "", name)  # 제목 앞 오타 'Is Summicron'
            name = _lsg_normalize(name)
            if not re.search(r"leica|leitz", f"{name} {p.get('vendor') or ''}", re.I):
                continue
            img = p["images"][0].get("src", "") if p.get("images") else ""
            cat = detect_category(name, price)
            mount = 'Accessory' if cat == 'Accessory' else detect_mount(name)
            results.append({
                "게시일": _shopify_listed(p),
                "site": "Leica Store Singapore (싱가포르)",
                "label": auto_label(name),
                "상품명": name,
                "세대": detect_generation(name),
                "컨디션": "정보없음",
                "가격": price,
                "통화": "SGD",
                "이미지": img,
                "링크": link,
                "품절": False,
                "예약중": False,
                "mount": mount,
                "category": cat,
                "brand": detect_brand(name),
            })
        time.sleep(random.uniform(1.0, 2.0))
    print(f"  ✅ Leica Store Singapore 완료: {len(results)}개")
    return results


# 라이카 프랑스 제목의 프랑스어 → 기존 분류가 아는 영어 (부속품 이름)
_LCF_WORDS = [(r"pare-?soleil", "hood"), (r"\bviseurs?\b", "viewfinder"), (r"[ée]tui", "case"), (r"\bloupe\b", "magnifier"),
              (r"adapt(?:at)?eur", "adapter"), (r"\bfiltre\b", "filter"), (r"correction de dioptrie", "diopter correction"),
              (r"t[ée]l[ée]m[èe]tre", "rangefinder"), (r"bo[iî]tier de transport", "carrying case"), (r"\bsac\b", "bag"),
              (r"bouchon", "cap"), (r"courroie", "strap"), (r"poign[ée]e", "grip"), (r"\bavec\b", "with"), (r"\bmonture\b", "mount")]


def _lcf_normalize(name: str) -> str:
    name = re.sub(r"(\d),(\d)", r"\1.\2", name)  # 프랑스식 소수점 f/2,8 → f/2.8
    # 조리개를 앞에 쓴 표기: 2.8/70mm-200mm → 70-200mm f/2.8, 2/35mm → 35mm f/2
    name = re.sub(r"(?<![\w/.])(\d(?:\.\d+)?)/(\d{2,3})\s?mm\s?-\s?(\d{2,3})\s?mm", r"\2-\3mm f/\1", name)
    name = re.sub(r"(?<![\w/.])(\d(?:\.\d+)?)/(\d{2,3})(?:\s?mm)?\b", r"\2mm f/\1", name)
    for pattern, word in _LCF_WORDS:
        name = re.sub(pattern, word, name, flags=re.I)
    return name


def crawl_leicafrance():
    """Leica Store France (프랑스) - 라이카 프랑스 공식 중고 몰 (Drupal 정적 HTML, ?page=N 30개씩).
    매장 5곳(파리 3·마르세유·릴) 재고. 온라인 결제 없이 매장 연락·방문 구매. 판매 완료(SOLD OUT)도 목록에 남음 → 품절로 담음"""
    import html as _html
    import requests
    from condition_grade import LCF_PREFIX
    results = []
    base = "https://www.leica-camera-france-occasions.com"
    print(f"\n  📂 Leica Store France 크롤링 시작")
    for page_num in range(0, 60):
        try:
            resp = requests.get(f"{base}/en/occasions?page={page_num}", headers={"User-Agent": random.choice(USER_AGENTS)}, timeout=20)
            resp.raise_for_status()
        except Exception as e:
            print(f"    ❌ {page_num}페이지 오류: {e}")
            break
        articles = re.findall(r"<article .*?</article>", resp.text, re.S)
        if not articles:
            break
        print(f"    └─ {page_num + 1}페이지 {len(articles)}개 상품 발견")
        for a in articles:
            def field(label):
                m = re.search(label + r"\s*:\s*</div>\s*([^<]+)", a)
                return _html.unescape(m.group(1)).strip() if m else ""
            m = re.search(r"field--name-title[^>]*>([^<]+)", a)
            path = re.search(r'about="([^"]+)"', a)
            if not m or not path:
                continue
            name = re.sub(r"\s+", " ", _html.unescape(m.group(1))).strip()
            name = _lcf_normalize(name)
            if re.search(r"oberwerth|artisan|billingham|peak design|gitzo|sigma|zeiss|voigtl|panasonic|lumix", name, re.I) or field("System") == "Sport Optics":
                continue  # 다른 브랜드 가방·쌍안경
            link = base + path.group(1)
            sold = "sold-out-lblTeaser" in a
            if sold and link in globals().get('SOLD_LINKS', ()):
                continue
            pm = re.search(r"([\d\s.,]+)\s*€", field("Price"))
            try:
                digits = re.sub(r"[^\d]", "", pm.group(1)) if pm else ""
                price = f"€{float(digits):,.0f}" if digits else "문의요망"
            except ValueError:
                price = "문의요망"
            img = re.search(r'<img src="([^"]+)"', a)
            img = (base + img.group(1)) if img and img.group(1).startswith("/") else (img.group(1) if img else "")
            if "materiel-expo" in a:
                name += " (Ex-demo)"
            cond = field("Condition")
            cat = detect_category(name, price)
            mount = 'Accessory' if cat == 'Accessory' else detect_mount(name)
            results.append({
                "site": "Leica Store France (프랑스)",
                "label": auto_label(name),
                "상품명": name,
                "세대": detect_generation(name),
                "컨디션": (LCF_PREFIX + cond) if cond else "정보없음",
                "가격": price,
                "통화": "EUR",
                "이미지": img,
                "링크": link,
                "품절": sold,
                "예약중": False,
                "mount": mount,
                "category": cat,
                "brand": detect_brand(name),
                "매장": field("Location"),
            })
        time.sleep(random.uniform(1.0, 2.0))
    print(f"  ✅ Leica Store France 완료: {len(results)}개")
    return results


# Newoldcamera 제목의 이탈리아어 → 기존 분류가 아는 영어 (부속품 이름·색)
_NOC_WORDS = [(r"\bparaluce\b", "hood"), (r"\bmirino\b", "viewfinder"), (r"\bborsa(?: pronto)?\b", "case"), (r"\btracoll[ae]\b", "strap"),
              (r"\bcinghi[ae]\b", "strap"), (r"\bimpugnatura\b", "grip"), (r"\badattatore\b", "adapter"), (r"\banello\b", "ring"),
              (r"\blentina(?: di)? correzione(?: diottrica)?\b", "diopter correction lens"), (r"\bfiltro\b", "filter"),
              (r"\btappo\b", "cap"), (r"\bscatola\b", "box"), (r"\bimballo\b", "box"), (r"\bistruzioni\b", "manual"),
              (r"\bcustodia\b", "case"), (r"\bastuccio\b", "case"), (r"\bcalotta\b", "top cover"), (r"\bcaricabatterie\b", "charger"),
              (r"\bbatteria\b", "battery"), (r"\bin pelle\b", "leather"), (r"\bcuoio\b", "leather"), (r"\bner[ao]\b", "black"),
              (r"\bmarrone\b", "brown"), (r"\b2 ganci\b", "2 lugs"), (r"\bnew\b", "new version"), (r"\bCR\b", "chrome"), (r"\bRTN\b", "")]
# 다른 브랜드 (라이카 마운트용 써드파티·가방 등) — 브랜드 칸 뒤에 붙거나 제목에 들어감
_NOC_OTHER = re.compile(r"voigtl|zeiss|contax|7artisans|dj-optical|astrhori|\bnisi\b|novoflex|oberwerth|metabones|lockcircle|"
                        r"ttartisan|kipon|canon|konica|rollei|schneider|light lens lab|wollensak|planar|biogon|sonnar|distagon", re.I)


def _noc_normalize(name: str) -> str:
    name = re.sub(r"\s+", " ", name).strip()
    # 초점거리를 앞에 쓴 표기: 50/2 → 50mm f/2, 28-35-50/4 → 28-35-50mm f/4, 11-23/3.5-4.5 → 11-23mm f/3.5-4.5
    name = re.sub(r"(?<![\w/.])(\d{2,3}(?:-\d{2,3})*)/(\d(?:\.\d+)?(?:-\d(?:\.\d+)?)?)(?![\w/])", r"\1mm f/\2", name)
    for pattern, word in _NOC_WORDS:
        name = re.sub(pattern, word, name, flags=re.I)
    name = re.sub(r"\s+", " ", name).strip()
    if not re.search(r"leica|leitz", name, re.I):
        name = "Leica " + name
    return name


def crawl_newoldcamera():
    """Newoldcamera (이탈리아) - 밀라노 중고 전문점. 화면은 ASP.NET + JSON API(noc-gateway, 브랜드·종류별 판매 중 목록).
    라이카 브랜드 칸(LEICA, LEICA-M, LEICA-R, LEICA-V(스크루) …)만. 등급 표기 A-·AB·BA·B+·B+/B·B/B+·B·BC·C.
    사진 경로가 없는 매물은 서명 주소가 1시간이면 만료돼 camerabridge.io/api/noc_image가 그때그때 받아 넘김"""
    import requests
    from condition_grade import NOC_PREFIX
    results = []
    base = "https://www.newoldcamera.com"
    api = "https://noc-gateway-api.icyriver-4199ba13.northeurope.azurecontainerapps.io/api/v1/products"
    headers = {"User-Agent": random.choice(USER_AGENTS)}
    print(f"\n  📂 Newoldcamera 크롤링 시작")
    # 종류: CO 바디 · OB 렌즈 · AC 부속품 · BO 가방 · Fl 플래시 · EP 노출계
    combos, seen = [], set()
    for tipo in ("CO", "OB", "AC", "BO", "Fl", "EP"):
        try:
            resp = requests.get(f"{base}/_Marche.aspx", params={"Tipo": tipo, "Bottega": "Usato"}, headers=headers, timeout=20)
            resp.raise_for_status()
        except Exception as e:
            print(f"    ❌ 브랜드 목록({tipo}) 오류: {e}")
            continue
        for marca in sorted(set(re.findall(r"Marca=(LEICA[^\"&]*)&(?:amp;)?Tipo=" + tipo, resp.text))):
            if not _NOC_OTHER.search(marca):
                combos.append((marca, tipo))
    for marca, tipo in combos:
        try:
            resp = requests.get(api, params={"Marca": marca, "Tipo": tipo, "Disponibile": "M", "Bottega": "Usato"}, headers=headers, timeout=30)
            resp.raise_for_status()
            items = resp.json()
        except Exception as e:
            print(f"    ❌ {marca}/{tipo} 오류: {e}")
            continue
        print(f"    └─ {marca}/{tipo} {len(items)}개 상품 발견")
        for it in items:
            code = it.get("codice")
            if not code or code in seen:
                continue
            seen.add(code)
            raw = (it.get("modello") or "").strip()
            if not raw or _NOC_OTHER.search(raw) or any(b in raw.lower() for b in THIRD_PARTY_BRANDS):
                continue
            link = f"{base}/Scheda.aspx?Codice={code}"
            if link in globals().get('SOLD_LINKS', ()):
                continue
            name = _noc_normalize(raw)
            sale, promo = it.get("prezzoVendita") or 0, it.get("prezzoPromozione") or 0
            value = promo if 0 < promo < sale else sale
            price = f"€{float(value):,.0f}" if value else "문의요망"
            vp = it.get("virtualPath") or ""
            img = (base + vp) if vp.startswith("/") else f"https://camerabridge.io/api/noc_image?code={code}"
            cond = (it.get("stato") or "").strip()
            cat = detect_category(name, price)
            mount = 'Accessory' if cat == 'Accessory' else detect_mount(name)
            results.append({
                "site": "Newoldcamera (이탈리아)",
                "label": auto_label(name),
                "상품명": name,
                "세대": detect_generation(name),
                "컨디션": (NOC_PREFIX + cond) if cond else "정보없음",
                "가격": price,
                "통화": "EUR",
                "이미지": img,
                "링크": link,
                "품절": False,
                "예약중": bool(it.get("prenotato")),
                "mount": mount,
                "category": cat,
                "brand": detect_brand(name),
            })
        time.sleep(random.uniform(0.5, 1.0))
    print(f"  ✅ Newoldcamera 완료: {len(results)}개")
    return results


def crawl_camtec():
    """Camtec Photo (캐나다) - 토론토 라이카 딜러. 라이카 중고·데모 목록(collections/leica/demos-pre-owned-etc) 정적 HTML, ?page=N 20개씩.
    등급은 제목 끝 표기(*A+*·*A*·*A-*·Open Box). robots.txt Crawl-delay 10초라 페이지 사이 10초 쉼. 판매 중만 목록에 나옴"""
    import html as _html
    import requests
    from condition_grade import CAMTEC_PREFIX
    results = []
    base = "https://www.camtecphoto.com"
    print(f"\n  📂 Camtec Photo 크롤링 시작")
    for page_num in range(1, 20):
        try:
            resp = requests.get(f"{base}/en/collections/leica/demos-pre-owned-etc", params={"page": page_num},
                                headers={"User-Agent": random.choice(USER_AGENTS)}, timeout=30)
            resp.raise_for_status()
        except Exception as e:
            print(f"    ❌ {page_num}페이지 오류: {e}")
            break
        entries = resp.text.split('class="product-list-entry"')[1:]
        if not entries:
            break
        print(f"    └─ {page_num}페이지 {len(entries)}개 상품 발견")
        for b in entries:
            m = re.search(r'<h2><a href="([^"?]+)[^"]*"[^>]*>([^<]+)', b)
            if not m:
                continue
            link, raw = m.group(1), re.sub(r"\s+", " ", _html.unescape(m.group(2))).strip()
            if link in globals().get('SOLD_LINKS', ()):
                continue
            name, cond = _camtec_split(raw)
            name = re.sub(r"\s+with .*\bEnsemble\b.*$", "", name)  # 'M11-D with Protector Leather Case Ensemble' → 바디로
            if not re.match(r"(leica|leitz)\b", name, re.I) or re.search(r"a selection of", name, re.I) \
                    or any(b2 in name.lower() for b2 in THIRD_PARTY_BRANDS):
                continue  # Voigtländer·Sigma·SmallRig 등 다른 브랜드('… for Leica Q3'), 여러 개 묶음
            if re.search(r"televid|ultravid|noctivid|geovid|binocular|spotting", name, re.I):
                continue  # 쌍안경·필드스코프
            prices = re.findall(r'<span class="bold">\$([\d,]+(?:\.\d+)?)', b)
            try:
                price = f"C${float(prices[-1].replace(',', '')):,.0f}" if prices else "문의요망"
            except ValueError:
                price = "문의요망"
            img = re.search(r'<img src="([^"]+)"', b)
            cat = detect_category(name, price)
            mount = 'Accessory' if cat == 'Accessory' else detect_mount(name)
            results.append({
                "site": "Camtec Photo (캐나다)",
                "label": auto_label(name),
                "상품명": name,
                "세대": detect_generation(name),
                "컨디션": (CAMTEC_PREFIX + cond) if cond else "정보없음",
                "가격": price,
                "통화": "CAD",
                "이미지": img.group(1) if img else "",
                "링크": link,
                "품절": False,
                "예약중": False,
                "mount": mount,
                "category": cat,
                "brand": detect_brand(name),
            })
        time.sleep(10)
    print(f"  ✅ Camtec Photo 완료: {len(results)}개")
    return results


def _camtec_split(raw: str):
    """Camtec 제목 끝 등급 표기를 떼어 (상품명, 등급). '- *A+*'·'*A +*'·'*Open Box*'·'- Open box' 꼴"""
    m = re.search(r"\s*-?\s*\*?\s*(A\s?\+|A-|A|B\s?\+|B-|B|C|Open\s?Box)\s*\*?\s*$", raw, re.I)
    if not m or (m.group(1).upper() in ("A", "B", "C") and "*" not in raw[m.start():]):
        return raw.strip(" -"), ""
    cond = re.sub(r"\s", "", m.group(1)).upper().replace("OPENBOX", "Open Box")
    return raw[:m.start()].strip(" -"), cond


APERTURE_CATEGORIES = ["leica-digital", "leica-rangefinder-cameras", "leica-m-lenses",
                       "leica-screw-mount", "leica-r-series", "leica-accessories"]


def crawl_aperture():
    """Aperture (영국) - 런던 라이카 중고 전문점. Lightspeed 쇼핑몰이라 분류 목록에 ?format=json을 붙이면 JSON.
    Pre-Owned Leica 하위 분류 6개(보이그랜더 분류는 뺌)를 100개씩. 판매 중만 목록에 나옴.
    등급은 설명 첫 줄(Mint·Mint-·Exc+++·Exc++·Exc+·Exc·User). robots.txt Crawl-delay 2초 지킴"""
    import requests
    from condition_grade import APERTURE_PREFIX, APERTURE_LABELS
    results, seen = [], set()
    base = "https://www.apertureuk.com"
    print(f"\n  📂 Aperture 크롤링 시작")
    s = requests.Session()
    s.headers["User-Agent"] = random.choice(USER_AGENTS)
    for cat_slug in APERTURE_CATEGORIES:
        for page_num in range(1, 20):
            try:
                resp = s.get(f"{base}/pre-owned-leica/{cat_slug}/page{page_num}.html",
                             params={"format": "json", "limit": 100}, timeout=30)
                resp.raise_for_status()
                col = resp.json().get("collection") or {}
            except Exception as e:
                print(f"    ❌ {cat_slug} {page_num}페이지 오류: {e}")
                break
            prods = col.get("products") or {}
            items = list(prods.values()) if isinstance(prods, dict) else list(prods)
            print(f"    └─ {cat_slug} {page_num}페이지 {len(items)}개 상품 발견")
            for p in items:
                link = f"{base}/{p.get('url', '')}"
                if not p.get("url") or link in seen or link in globals().get('SOLD_LINKS', ()):
                    continue
                seen.add(link)
                # 제목 끝 매장 재고 번호('   ALC176604'·'  110-84')는 뗀다
                name = re.sub(r"\s{2,}([A-Z]{1,4}\d{3,}|\d{3}-\d{2})\s*$", "", (p.get("title") or "").rstrip())
                name = re.sub(r"\s+", " ", name).strip()
                brand_new = bool(re.match(r"brand new\s+", name, re.I))
                name = re.sub(r"^brand new\s+", "", name, flags=re.I)
                name = re.sub(r"\bSL-2(-?S)?\b", lambda m: "SL2" + ("-S" if m.group(1) else ""), name)  # 'SL-2S' → SL2-S
                name = re.sub(r"\bApo-Macro-Elmar\b(?!it)", "Apo-Macro-Elmarit-R", name)  # 100mm f2.8 R 렌즈 오타
                # 브랜드 칸은 'Leica'인데 제목이 Nikon·Schneider인 것, 브랜드 칸이 빈 라이카가 있어 제목으로 거른다
                if not re.match(r"(leica|leitz)\b", name, re.I) or any(b2 in name.lower() for b2 in THIRD_PARTY_BRANDS):
                    continue  # Aperture 자체 캡·Sigma·Zeiss 등 다른 브랜드
                desc = (p.get("description") or "").strip()
                first = desc.splitlines()[0].strip() if desc else ""
                if brand_new or re.search(r"\bbrand new\b", first, re.I):
                    first = "New"
                cond = APERTURE_PREFIX + first if first in APERTURE_LABELS else "정보없음"
                amount = ((p.get("price") or {}).get("price_incl")) or 0
                price = f"£{float(amount):,.0f}" if amount else "문의요망"
                img = f"https://cdn.webshopapp.com/shops/299238/files/{p['image']}/file.jpg" if p.get("image") else ""
                cat = detect_category(name, price)
                mount = 'Accessory' if cat == 'Accessory' else detect_mount(name)
                results.append({
                    "site": "Aperture (영국)",
                    "label": auto_label(name),
                    "상품명": name,
                    "세대": detect_generation(name),
                    "컨디션": cond,
                    "가격": price,
                    "통화": "GBP",
                    "이미지": img,
                    "링크": link,
                    "품절": not p.get("available", True),
                    "예약중": False,
                    "mount": mount,
                    "category": cat,
                    "brand": detect_brand(name),
                })
            time.sleep(2)
            if not col.get("page_next"):
                break
    print(f"  ✅ Aperture 완료: {len(results)}개")
    return results


def crawl_harrison():
    """Harrison Cameras (영국, 셰필드) - Shopify JSON. 중고 컬렉션(used, 약 1,700개) 전체를 250개씩 훑어
    브랜드 칸이 'Used Leica'이거나 제목이 Leica·Leitz로 시작하는 라이카만. 품절도 목록에 남아 있어 품절로 표시.
    등급은 설명 끝 'Condition: Used - Excellent' (Mint·Excellent·Very Good·Good·Fairly Well Used)"""
    import requests
    from condition_grade import HARRISON_PREFIX, harrison_condition
    results, seen = [], set()
    base = "https://harrisoncameras.co.uk"
    print(f"\n  📂 Harrison Cameras 크롤링 시작")
    s = requests.Session()
    s.headers["User-Agent"] = random.choice(USER_AGENTS)
    for page_num in range(1, 30):
        products = None
        for attempt in range(4):  # Shopify가 연달아 부르면 429 — 기다렸다 다시
            try:
                resp = s.get(f"{base}/collections/used/products.json",
                             params={"limit": 250, "page": page_num}, timeout=30)
                if resp.status_code == 429:
                    time.sleep(int(resp.headers.get("Retry-After") or 0) or 30 * (attempt + 1))
                    continue
                resp.raise_for_status()
                products = resp.json().get("products", [])
                break
            except Exception as e:
                print(f"    ⚠️ {page_num}페이지 오류: {e}")
                time.sleep(5)
        if products is None:
            # 중간 페이지가 빠지면 나머지 라이카가 판매완료로 잘못 바뀌니 이번 실행은 실패로 (이전 데이터 유지)
            raise RuntimeError(f"Harrison {page_num}페이지 못 읽음")
        if not products:
            break
        print(f"    └─ {page_num}페이지 {len(products)}개 상품 발견")
        for p in products:
            name = re.sub(r"^used\s+", "", (p.get("title") or "").strip(), flags=re.I)
            # 다른 매장 제목처럼: '35mm Compact Camera'·'Rangefinder Camera Body'의 필름 크기·종류 말, 딸린 케이스, 괄호 설명을 뗀다
            # (그대로 두면 '35mm'로 렌즈, 'case'·'finder'로 액세서리로 잘못 갈림)
            name = re.sub(r"\s*\((?:fixed focus )?lens for [^)]*\)", "", name, flags=re.I)
            name = re.sub(r"\b(?:35mm\s+)?(?:analog|compact|aps\s+compact)\s+camera\b", "Camera", name, flags=re.I)
            name = re.sub(r"\b35mm\s+(?=camera\b)", "", name, flags=re.I)
            name = re.sub(r"\brangefinder\s+camera\s+body\b", "Body", name, flags=re.I)
            if not re.search(r"\bcase\s+for\b", name, re.I):
                name = re.sub(r"\s*(?:with|&)\s+(?:leica\s+)?(?:ever ready\s+)?case\b.*$", "", name, flags=re.I)
            name = re.sub(r"\s+", " ", name).strip()
            vendor = (p.get("vendor") or "").lower()
            # 브랜드 칸이 Panasonic·Voigtlander인 'Leica' 표기 렌즈·어댑터는 뺀다
            if not ("leica" in vendor or (vendor in ("used miscellaneous", "") and re.match(r"(leica|leitz)\b", name, re.I))):
                continue
            if any(b2 in name.lower() for b2 in THIRD_PARTY_BRANDS):
                continue
            link = f"{base}/products/{p['handle']}" if p.get("handle") else ""
            if not link or link in seen or link in globals().get('SOLD_LINKS', ()):
                continue
            seen.add(link)
            variant = p["variants"][0] if p.get("variants") else {}
            try:
                price = f"£{float(variant.get('price')):,.0f}"
            except (TypeError, ValueError):
                price = "문의요망"
            label = harrison_condition(p.get("body_html") or "")
            cond = HARRISON_PREFIX + label if label else "정보없음"
            img = p["images"][0].get("src", "") if p.get("images") else ""
            cat = detect_category(name, price)
            mount = 'Accessory' if cat == 'Accessory' else detect_mount(name)
            results.append({
                "게시일": _shopify_listed(p),
                "site": "Harrison Cameras (영국)",
                "label": auto_label(name),
                "상품명": name,
                "세대": detect_generation(name),
                "컨디션": cond,
                "가격": price,
                "통화": "GBP",
                "이미지": img,
                "링크": link,
                "품절": not variant.get("available", True),
                "예약중": False,
                "mount": mount,
                "category": cat,
                "brand": detect_brand(name),
            })
        time.sleep(random.uniform(4.0, 5.0))  # 250개씩 7쪽, 간격이 짧으면 429
    print(f"  ✅ Harrison Cameras 완료: {len(results)}개")
    return results


WEX_ALGOLIA = {"app": "C1EVKDF8ZJ", "key": "07c4ecf5dcac1fc1f1ae3b98dd387d06", "index": "prod_CatalogFeed"}


def crawl_wex():
    """Wex Photo Video (영국) - 대형몰의 라이카 중고(leica-used 분류). 목록 화면이 쓰는 사이트 검색 중계
    (/qkax/search-gateway, Algolia 형식)에 화면에 박힌 공개 검색 키로 한 번에 받는다. 판매 중만 나옴.
    등급은 'Condition' 칸 (As new (10)·Mint (9+)·Excellent (9)·Very good (9-)·Good (8)…)"""
    import requests
    from condition_grade import WEX_PREFIX
    results, seen = [], set()
    base = "https://www.wexphotovideo.com"
    print(f"\n  📂 Wex Photo Video 크롤링 시작")
    headers = {"User-Agent": random.choice(USER_AGENTS), "Content-Type": "application/json",
               "X-Algolia-Application-Id": WEX_ALGOLIA["app"], "X-Algolia-API-Key": WEX_ALGOLIA["key"],
               "Referer": f"{base}/leica-used/", "Origin": base}
    hits, page_num = [], 0
    while True:
        params = f"filters=categories%3A%22leica-used%22&hitsPerPage=200&page={page_num}&query="
        resp = requests.post(f"{base}/qkax/search-gateway/1/indexes/*/queries", headers=headers, timeout=30,
                             json={"requests": [{"indexName": WEX_ALGOLIA["index"], "params": params}]})
        resp.raise_for_status()
        res = (resp.json().get("results") or [{}])[0]
        hits += res.get("hits") or []
        print(f"    └─ {page_num + 1}페이지 {len(res.get('hits') or [])}개 상품 발견 (전체 {res.get('nbHits')})")
        page_num += 1
        if page_num >= (res.get("nbPages") or 1):
            break
        time.sleep(1)
    for h in hits:
        link = base + (h.get("productUrl") or "")
        if not h.get("productUrl") or link in seen or link in globals().get('SOLD_LINKS', ()):
            continue
        seen.add(link)
        name = re.sub(r"^used\s+", "", (h.get("title") or h.get("displayName") or "").strip(), flags=re.I)
        # 옛 T 시스템 렌즈 이름 'Vario Elmar T' → 지금 이름 '-TL' (TL 마운트로 읽히게)
        name = re.sub(r"\b(Elmar|Elmarit|Summicron|Summilux)[ -]T\b(?!L)", r"\1-TL", name, flags=re.I)
        name = re.sub(r"\s+", " ", name).strip()
        if "leica" not in (h.get("manufacturer") or "").lower() or any(b2 in name.lower() for b2 in THIRD_PARTY_BRANDS):
            continue
        amount = h.get("Price") or 0
        price = f"£{float(amount):,.0f}" if amount else "문의요망"
        cond_raw = (h.get("Condition") or "").strip()
        cond = WEX_PREFIX + cond_raw if cond_raw else "정보없음"
        img = ""
        if h.get("imageUrl"):
            img = base + re.sub(r"width=\d+", "width=600", h["imageUrl"][0])
        cat = detect_category(name, price)
        mount = 'Accessory' if cat == 'Accessory' else detect_mount(name)
        results.append({
            "site": "Wex Photo Video (영국)",
            "label": auto_label(name),
            "상품명": name,
            "세대": detect_generation(name),
            "컨디션": cond,
            "가격": price,
            "통화": "GBP",
            "이미지": img,
            "링크": link,
            "품절": not h.get("availability", True),
            "예약중": False,
            "mount": mount,
            "category": cat,
            "brand": detect_brand(name),
        })
    print(f"  ✅ Wex Photo Video 완료: {len(results)}개")
    return results


def _naniwa_get(url):
    """나니와 목록 한 쪽 (Shift_JIS). 직접 받다가 막히면(미국 서버 등) 도쿄 중계 서버로.
    USER_AGENTS를 돌려 쓰지 않는다 — 'Chrome/120.0.0.0' 꼴 UA만 CloudFront 403이 남 (공용 BROWSER_UA는 정상)"""
    import crawl_engine as _ce
    try:
        resp = _ce.http_get(url)
        resp.raise_for_status()
        if 'StyleT_Item_' not in resp.text and 'navipage_sum_' not in resp.text:
            raise ValueError("목록 화면이 아님")
    except Exception as e:
        print(f"    ↪ 직접 접속 실패({e}) → 중계 서버")
        resp = _ce.http_get(url, via_relay=True)
        resp.raise_for_status()
    return resp.content.decode("cp932", "ignore")


def _naniwa_name(name_ja, ja_to_en):
    """나니와 제목 다듬기. 'Elmarit-R 2.8/90'·'1:2.8/90'처럼 조리개가 앞에 오는 표기를 '90/2.8'로 (R 렌즈에 많음),
    '5Cm' → '5cm'"""
    name = re.sub(r"(?<=\d)Cm\b", "cm", name_ja)
    name = re.sub(r"\b1:(?=\d)", "", name)
    name = re.sub(r"(?<![\d.:/])(\d(?:\.\d{1,2})?)\s*/\s*(\d{2,3})(?![\d.])", r"\2/\1", name)
    from ja_normalize import LENS_NAMES
    name = ja_to_en(name)
    name = re.sub(rf"({LENS_NAMES})(?=\d)", r"\1 ", name)  # 'Elmar50/3.5' → 'Elmar 50/3.5'
    name = re.sub(r"\b([RLM])(\d{2,3})(?=/)", r"\1 \2", name)  # 'Super-Angulon R21/4' → 'R 21/4'
    name = re.sub(r"\bM6TTL\b", "M6 TTL", name)
    name = re.sub(r"\b(I{1,3}) ([a-g])\b", r"\1\2", name)  # 'III f' → 'IIIf' (III와 IIIf 둘 다에 걸리던 것)
    return re.sub(r"\s+", " ", name).strip()


def crawl_naniwa():
    """카메라노나니와 (일본) - 나니와 그룹 온라인 (35개 매장 재고). 사이트 검색 화면(정적 HTML, Shift_JIS)을
    중고(pb_salestype=2)·'Leica'로 100개씩 끝까지 넘긴다 (지금 13쪽 · 1분쯤). 판매 중만 목록에 나옴.
    등급은 목록 아이콘 글자 A·AB＋·AB·AB-·B+·B·C (일본 매장 공통 대응)"""
    import html as _html
    from ja_normalize import ja_to_en
    results, seen = [], set()
    base = "https://cameranonaniwa.jp"
    print(f"\n  📂 카메라노나니와 크롤링 시작")
    for page_num in range(1, 40):
        url = f"{base}/shop/goods/search.aspx?p={page_num}&ps=100&search=x&pb_salestype=2&pb_search=x&pb_keyword=Leica"
        try:
            html = _naniwa_get(url)
        except Exception as e:
            print(f"    ❌ {page_num}페이지 오류: {e}")
            if page_num == 1:
                raise  # 첫 페이지부터 못 받으면 실패로 (병합 단계에서 이전 데이터 유지)
            break
        items = html.split('<div class="StyleT_Item_')[1:]
        if not items:
            break
        print(f"    └─ {page_num}페이지 {len(items)}개 상품 발견")
        for b in items:
            m_name = re.search(r'class="name1_">([^<]*)', b)
            m_link = re.search(r'href="/shop/g/g(\d+)/"', b)
            if not m_name or not m_link:
                continue
            raw = re.sub(r"\s+", " ", _html.unescape(m_name.group(1))).strip()
            if "(ライカ)" not in raw or "SOLD OUT" in b:
                continue  # 다른 브랜드의 'ライカM用' 렌즈·어댑터, 판매 끝
            gid = m_link.group(1)
            link = f"{base}/shop/g/g{gid}/"
            if link in seen or link in globals().get('SOLD_LINKS', ()):
                continue
            seen.add(link)
            # '（Leica） 【中古】(ライカ) Leica ズミクロン M50/2' → 'Leica ズミクロン M50/2'
            name_ja = raw.split("(ライカ)", 1)[1].strip()
            if not name_ja.lower().startswith(("leica", "leitz")):
                name_ja = "Leica " + name_ja
            name = _naniwa_name(name_ja, ja_to_en)
            if any(b2 in name.lower() for b2 in THIRD_PARTY_BRANDS):
                continue
            m_price = re.search(r'class="tax_price">\s*￥\s*([\d,]+)', b)
            price = f"¥{int(m_price.group(1).replace(',', '')):,}" if m_price else "문의요망"
            m_cond = re.search(r'/img/filter/2/CND\d+\.png" alt="([^"]+)"', b)
            cond = m_cond.group(1).replace("＋", "+").replace("－", "-").strip() if m_cond else "정보없음"
            cat = detect_category(name, price)
            mount = 'Accessory' if cat == 'Accessory' else detect_mount(name)
            results.append({
                "site": "카메라노나니와 (일본)",
                "label": auto_label(name),
                "상품명": name,
                "세대": detect_generation(name),
                "컨디션": cond,
                "가격": price,
                "통화": "JPY",
                "이미지": f"{base}/img/goods/L/{gid}-01.jpg",
                "링크": link,
                "품절": False,
                "예약중": False,
                "mount": mount,
                "category": cat,
                "brand": detect_brand(name),
            })
        if len(items) < 100:
            break
        time.sleep(random.uniform(1.5, 2.5))
    print(f"  ✅ 카메라노나니와 완료: {len(results)}개")
    return results


CALUMET_CONDS = {"Wie neu": "wie-neu", "Sehr gut": "sehr-gut", "Gut": "gut", "Akzeptabel": "akzeptabel",
                 "Stark gebraucht": "stark-gebraucht"}


def _calumet_unit(html):
    """Calumet 중고 상품 화면에서 지금 보이는 한 대의 (주소, 사진). 사진은 그 기기를 찍은 것(…_<번호>_1.jpg)"""
    pl = re.search(r'product:product_link" content="([^"]+)"', html)
    og = re.search(r'property="og:image" content="([^"?]+)', html)
    return (pl.group(1) if pl else None), (og.group(1) if og else "")


def crawl_calumet():
    """Calumet Photo Video (독일) - 독일 13개 매장 체인 (뮌헨 Foto Video Sauter 포함, 같은 재고).
    사이트 검색 'leica gebraucht'(정적 HTML, 48개씩 7쪽)로 중고 상품을 모으고, 상품 화면마다 등급별 선택지
    ('Sehr gut (3x)'·가격, 재고 없는 등급은 '(Nx)'가 없음)를 읽어 등급 하나를 한 행으로. 상품 화면 120개쯤이라 4~5분 → 6시간마다.
    등급: Wie neu·Sehr gut·Gut·Akzeptabel·Stark gebraucht"""
    import html as _html
    import requests
    from condition_grade import CALUMET_PREFIX
    results = []
    base = "https://www.calumet.de"
    sess = requests.Session()
    sess.headers["User-Agent"] = random.choice(USER_AGENTS)
    print(f"\n  📂 Calumet 크롤링 시작")
    tiles = {}
    for page_num in range(1, 20):
        try:
            resp = sess.get(f"{base}/search", params={"search": "leica gebraucht", "p": page_num}, timeout=40)
            resp.raise_for_status()
        except Exception as e:
            print(f"    ❌ 검색 {page_num}페이지 오류: {e}")
            if page_num == 1:
                raise
            break
        found = re.findall(r'class="\s*card\s*product-box.*?href="([^"]+)"\s*title="([^"]+)"', resp.text, re.S)
        new = [(h, t) for h, t in found if h not in tiles]
        if not new:
            break  # 마지막 쪽 다음은 첫 쪽이 다시 나옴
        for h, t in new:
            tiles[h] = _html.unescape(t)
        print(f"    └─ 검색 {page_num}페이지 {len(new)}개")
        time.sleep(1)
    # 'Panasonic LUMIX Leica DG'·'Voigtländer … für Leica M' 같은 다른 브랜드 제외
    tiles = {h: t for h, t in tiles.items() if h.endswith("/gebraucht") and re.match(r"(leica|leitz)\b", t, re.I)}
    print(f"    └─ 라이카 중고 상품 {len(tiles)}개")
    for path, title in tiles.items():
        try:
            resp = sess.get(base + path, timeout=40)
            resp.raise_for_status()
        except Exception as e:
            print(f"    ⚠️  {path}: {e}")
            continue
        page = resp.text
        name = re.sub(r"\s+gebraucht\s*$", "", title, flags=re.I).strip()
        name = re.sub(r"\s+", " ", name)
        if any(b2 in name.lower() for b2 in THIRD_PARTY_BRANDS):
            continue
        shown_link, shown_img = _calumet_unit(page)
        opts = re.findall(r'product-detail-configurator-option-label-text">\s*(.*?)</div>.*?c-Price-finalValue">\s*([\d.,]+)\s*€',
                          page, re.S)
        for label, amount in opts:
            m = re.match(r"\s*(.*?)\s*\((\d+)x\)", re.sub(r"\s+", " ", label))
            if not m or m.group(1) not in CALUMET_CONDS:
                continue  # '(Nx)'가 없으면 그 등급 재고 없음
            cond, slug = m.group(1), CALUMET_CONDS[m.group(1)]
            link, img = shown_link, shown_img
            if not (link and f"/gebraucht/{slug}/" in link):
                # 화면에 안 보이는 등급은 그 등급 화면에서 한 대의 주소·사진
                try:
                    sub = sess.get(f"{base}{path}/{slug}", timeout=40)
                    link, img = _calumet_unit(sub.text)
                except Exception:
                    link, img = None, shown_img
                link = link or f"{base}{path}/{slug}"
                time.sleep(0.5)
            if link in globals().get('SOLD_LINKS', ()):
                continue
            price = f"€{float(amount.replace('.', '').replace(',', '.')):,.0f}"
            cat = detect_category(name, price)
            mount = 'Accessory' if cat == 'Accessory' else detect_mount(name)
            results.append({
                "site": "Calumet (독일)",
                "label": auto_label(name),
                "상품명": name,
                "세대": detect_generation(name),
                "컨디션": CALUMET_PREFIX + cond,
                "가격": price,
                "통화": "EUR",
                "이미지": img,
                "링크": link,
                "품절": False,
                "예약중": False,
                "mount": mount,
                "category": cat,
                "brand": detect_brand(name),
            })
        time.sleep(0.5)
    print(f"  ✅ Calumet 완료: {len(results)}개")
    return results


def _shopify_all(sess, url, label):
    """Shopify products.json을 250개씩 끝까지. 429면 기다렸다 다시, 중간 쪽을 못 읽으면 실패로 (이전 데이터 유지)"""
    products = []
    for page_num in range(1, 40):
        page = None
        for attempt in range(4):
            try:
                resp = sess.get(url, params={"limit": 250, "page": page_num}, timeout=30)
                if resp.status_code == 429:
                    time.sleep(int(resp.headers.get("Retry-After") or 0) or 20 * (attempt + 1))
                    continue
                resp.raise_for_status()
                page = resp.json().get("products", [])
                break
            except Exception as e:
                print(f"    ⚠️ {label} {page_num}페이지 오류: {e}")
                time.sleep(5)
        if page is None:
            raise RuntimeError(f"{label} {page_num}페이지 못 읽음")
        if not page:
            break
        print(f"    └─ {label} {page_num}페이지 {len(page)}개")
        products += page
        time.sleep(3)
    return products


def _camerawest_name(name):
    """Camera West 제목 다듬기: 꼬리말(', Hood'·'(9+)'·'DAG serviced'·'Open Box'·'Certified Refurbished') 떼기,
    렌즈 이름을 뺀 줄임말('50mm f1.4 Asph'·'35mm f2 Apo SL'·'16-35mm f3.5-4.5')에 이름 넣기, 흔한 오타"""
    name = re.sub(r"\s*\((?:10|[5-9])[+\-]?\)", "", name)
    name = re.sub(r",?\s*\b(?:no\s+)?(?:hood|shade)\b", "", name, flags=re.I)
    name = re.sub(r",?\s*\b(?:DAG\s+(?:serviced|CLA|overhaul)|CLA'?d|certified refurbished|open box|N/A|late)\b", "", name, flags=re.I)
    name = re.sub(r"\s*-\s*$", "", name)
    name = re.sub(r"Summicrion|Summicon\b", "Summicron", name, flags=re.I)
    name = re.sub(r"\bAnguron\b", "Angulon", name, flags=re.I)
    name = re.sub(r"\bM EVI\b", "M EV1", name)
    # 렌즈 이름 없이 초점거리만 쓴 것
    name = re.sub(r"^(Leica 50mm f1\.4) Asph\b", r"\1 Summilux-M Asph", name, flags=re.I)
    name = re.sub(r"^(Leica 90mm f2) Asph\b", r"\1 APO-Summicron-M Asph", name, flags=re.I)
    name = re.sub(r"^(Leica (?:28|35|50|75|90)mm f2) Apo SL\b", r"\1 APO-Summicron-SL", name, flags=re.I)
    name = re.sub(r"^Leica (?:SL )?16-35mm f3\.5-4\.5$", "Leica 16-35mm f3.5-4.5 Super-Vario-Elmar-SL", name, flags=re.I)
    name = re.sub(r"^Leica 90-280mm f2\.8-4$", "Leica 90-280mm f2.8-4 APO-Vario-Elmarit-SL", name, flags=re.I)
    return re.sub(r"\s+", " ", name).strip(" ,")


def crawl_camerawest():
    """Camera West (미국 캘리포니아) - Shopify JSON. 중고 컬렉션(pre-owned, 약 1,000개)에서 라이카만.
    같은 그룹의 Leica Store San Francisco(leicastoresf.com) 중고도 함께 — 둘에 같은 기기가 많아(약 200개)
    제목 끝 일련번호로 겹친 것은 Camera West 쪽만 남긴다. 품절도 목록에 남아 있어 품절로 표시.
    등급은 설명의 'I rate it cosmetically a (9+)'·'rated at a (8+)' 점수 (10-·9+·9·8+·8·7+)"""
    import requests
    from condition_grade import CAMERAWEST_PREFIX, describe_text
    results, serials, seen, cw_names = [], set(), set(), set()
    sess = requests.Session()
    sess.headers["User-Agent"] = random.choice(USER_AGENTS)
    print(f"\n  📂 Camera West 크롤링 시작")
    stores = [("https://www.camerawest.com", "/collections/pre-owned/products.json", "Camera West"),
              ("https://leicastoresf.com", "/products.json", "Leica Store SF")]
    for base, path, label in stores:
        for p in _shopify_all(sess, base + path, label):
            tags = [t.lower() for t in p.get("tags") or []]
            if label == "Leica Store SF" and "used" not in tags:
                continue  # SF는 새 상품과 섞여 있음
            name = re.sub(r"\s+", " ", (p.get("title") or "")).strip()
            vendor = (p.get("vendor") or "").lower()
            ptype = (p.get("product_type") or "").lower()
            if not re.match(r"(leica|leitz)", name, re.I):
                continue  # 브랜드 칸이 Leica여도 제목이 'Nikon S3 …'인 것 등
            if "book" in ptype or "sport optics" in ptype or any(b2 in name.lower() for b2 in THIRD_PARTY_BRANDS):
                continue  # 'Leica Store SF Books' 사진집, 쌍안경·조준경, 다른 브랜드
            if re.search(r"noctivid|ultravid|trinovid|colorline|amplus|\bPRS\b|calonox|rangemaster|\b[CL]RF\b|"
                         r"geovid|binocular|opera glass|\d+x\d+", name, re.I):
                continue
            m_serial = re.search(r"#?\b(\d{6,8})\s*$", name)
            serial = m_serial.group(1) if m_serial else None
            if serial and serial in serials:
                continue  # Camera West에 이미 있는 같은 기기
            # 제목 끝 일련번호·', Boxed'는 상품명에서 뗀다 (모델 연결에 방해)
            name = re.sub(r",?\s*#?\b\d{6,8}\s*$", "", name)
            name = re.sub(r",?\s*\bBoxed\b", "", name, flags=re.I).strip(" ,")
            name = _camerawest_name(name)
            link = f"{base}/products/{p['handle']}" if p.get("handle") else ""
            if not link or link in seen or link in globals().get('SOLD_LINKS', ()):
                continue
            variant = p["variants"][0] if p.get("variants") else {}
            try:
                price = f"${float(variant.get('price')):,.0f}"
            except (TypeError, ValueError):
                price = "문의요망"
            if label == "Leica Store SF" and (name.lower(), price) in cw_names:
                continue  # 일련번호 없이 두 곳에 같이 올린 것
            seen.add(link)
            if serial:
                serials.add(serial)
            if label == "Camera West":
                cw_names.add((name.lower(), price))
            body = re.sub(r"<[^>]+>", " ", p.get("body_html") or "")
            m_grade = re.search(r"\(\s*(10-?|[5-9][+\-]?)\s*\)", body)
            if m_grade:
                cond = CAMERAWEST_PREFIX + m_grade.group(1)
            elif re.search(r"open box", p.get("title") or "", re.I):
                cond = "New"
            else:
                cond = describe_text(body) or "정보없음"
            img = p["images"][0].get("src", "") if p.get("images") else ""
            cat = detect_category(name, price)
            mount = 'Accessory' if cat == 'Accessory' else detect_mount(name)
            results.append({
                "게시일": _shopify_listed(p),
                "site": "Camera West (미국)",
                "label": auto_label(name),
                "상품명": name,
                "세대": detect_generation(name),
                "컨디션": cond,
                "가격": price,
                "통화": "USD",
                "이미지": img,
                "링크": link,
                "품절": not any(v.get("available") for v in p.get("variants") or [{}]),
                "예약중": False,
                "mount": mount,
                "category": cat,
                "brand": detect_brand(name),
            })
    print(f"  ✅ Camera West 완료: {len(results)}개")
    return results


def crawl_peterloy():
    """Peter Loy (영국) - 빈티지 카메라 전문점. 재고표 한 화면(/stock-list/, 정적 HTML, 500개쯤)에 제목·설명·가격(£)이 다 있음.
    판매 완료는 'Sold'로 남아 있어 건너뜀. 등급은 설명의 'Condition 4-5/E' (외관 1~6 · 작동 C·D·E 정상, G 결함, H 미확인, J 사용 불가)"""
    import html as _html
    import requests
    from condition_grade import PETERLOY_PREFIX
    results = []
    base = "https://www.peterloy.com"
    print(f"\n  📂 Peter Loy 크롤링 시작")
    resp = requests.get(f"{base}/stock-list/", headers={"User-Agent": random.choice(USER_AGENTS)}, timeout=60)
    resp.raise_for_status()
    items = resp.text.split('<div class="post-item">')[1:]
    print(f"    └─ 재고표 {len(items)}개")
    for b in items:
        m_title = re.search(r'eg-stock-list-skin-element-0">(.*?)</div>', b, re.S)
        m_price = re.search(r'st-price">\s*([\d,.]+)', b)
        m_id = re.search(r'data-id="(\d+)"', b)
        if not (m_title and m_price and m_id):
            continue  # 'Sold'는 가격 자리에 Sold만 있음
        name = re.sub(r"\s+", " ", _html.unescape(re.sub(r"<[^>]+>", "", m_title.group(1)))).strip(" ,.")
        if not re.match(r"(leica|leitz)", name, re.I) or any(b2 in name.lower() for b2 in THIRD_PARTY_BRANDS):
            continue
        m_ex = re.search(r'post-excerpt">(.*?)</div>', b, re.S)
        excerpt = _html.unescape(re.sub(r"<[^>]+>", "", m_ex.group(1))) if m_ex else ""
        m_cond = re.search(r"Condition:?\s*(?:body\s*)?(\d(?:-\d)?/[CDEGHJ])", excerpt)
        link = f"{base}/?p={m_id.group(1)}"  # 상품 화면으로 넘어가는 고정 주소
        if link in globals().get('SOLD_LINKS', ()):
            continue
        price = f"£{float(m_price.group(1).replace(',', '')):,.0f}"
        m_img = re.search(r"background-image: url\('([^']+)'", b)
        cat = detect_category(name, price)
        if cat == "Accessory" and re.search(r"\bbody\b", name, re.I) and not re.search(r"body cap|case|cover", name, re.I):
            cat = "Body"  # £300 아래 바르낙 바디가 가격 기준(50만원)으로 액세서리가 되던 것
        mount = 'Accessory' if cat == 'Accessory' else detect_mount(name)
        results.append({
            "site": "Peter Loy (영국)",
            "label": auto_label(name),
            "상품명": name,
            "세대": detect_generation(name),
            "컨디션": PETERLOY_PREFIX + m_cond.group(1) if m_cond else "정보없음",
            "가격": price,
            "통화": "GBP",
            "이미지": m_img.group(1) if m_img else "",
            "링크": link,
            "품절": False,
            "예약중": False,
            "mount": mount,
            "category": cat,
            "brand": detect_brand(name),
        })
    print(f"  ✅ Peter Loy 완료: {len(results)}개")
    return results


LUCKY_JA = {"ノクティルクス": "Noctilux", "ビゾフレックス": "Visoflex ", "ビゾー": "Visoflex ", "ビゾ": "Visoflex ",
            "トリウム": "Thorium", "スタンダード": "Standard", "カム": "CAM", "ボディー": "Body", "ボディ": "Body"}


def _lucky_name(name_ja, ja_to_en):
    """Lucky Camera 제목 다듬기: 'LSummaron 3.5cmF3.5'·'MElmar9cmF4'처럼 붙은 마운트 글자·F값, 'IIIGBody'·'ICBody'처럼
    붙은 Body와 대문자 모델 글자, 'フレックスI'(=ライカフレックス) 등"""
    name = re.sub(r"^フレックス", "Leicaflex ", name_ja)
    for ja, en in LUCKY_JA.items():
        name = name.replace(ja, en)
    name = "Leica " + name if not name.startswith("Leicaflex") else name
    name = ja_to_en(name)
    name = re.sub(r"(?<=[A-Za-z0-9])(?=(?:Body|Black|Silver|Chrome)(?:\b|[A-Z]))", " ", name)
    name = re.sub(r"\b([LMR])(?=(?:Summ|Elm|Hek|Noct|Tel|Macro|Super|Tri|Thambar|Xenon|Angulon))", r"\1 ", name)
    name = re.sub(r"(Summ[a-z]*|Elmar[a-z]*|Hektor|Telyt|Noctilux|Summilux|Xenon)(?=\d)", r"\1 ", name)  # 'Elmar9cm' → 'Elmar 9cm'
    name = name.replace("Leicaフレックス", "Leicaflex ")
    name = re.sub(r"\bElmarC\s*(?=\d)", "Elmar-C ", name)  # CL용 'ElmarC90mm' → 'Elmar-C 90mm'
    name = re.sub(r"(\d(?:cm|mm))F(\d)", r"\1 F\2", name)  # '9cmF4' → '9cm F4'
    name = re.sub(r"\b(I{1,3}|D?II)([A-G])\b", lambda m: m.group(1) + m.group(2).lower(), name)  # 'IIIG' → 'IIIg'
    name = re.sub(r"\bLeica DII\b", "Leica II (D)", name)
    name = re.sub(r"[ー-]+(?=\s|$)", "", name)  # 'Bodyー'
    return re.sub(r"\s+", " ", name).strip()


def crawl_lucky():
    """Lucky Camera (일본, 신주쿠) - 빈티지·라이카 중고점. 라이카 분류(/shop/LEICA/page/N/, 정적 HTML, 10개씩 30쪽쯤)에서
    목록의 이름·가격·사진, 상세 화면의 '程度'(AAA·AA·AB·A·B·N) 등급. 상세는 처음 본 매물만 읽고 전에 읽은 등급은
    이전 결과(data/raw/results.json)에서 다시 쓴다 (처음엔 5분쯤) → 12시간마다. 'soldout' 표시는 건너뜀"""
    import html as _html
    import unicodedata
    import requests
    from ja_normalize import ja_to_en
    from urllib.parse import unquote
    from condition_grade import LUCKY_PREFIX
    results, seen = [], set()
    base = "https://lucky-camera.com"
    sess = requests.Session()
    sess.headers["User-Agent"] = random.choice(USER_AGENTS)
    known = {}
    try:
        with open("data/raw/results.json", encoding="utf-8") as f:
            known = {r["링크"]: r.get("컨디션") for r in json.load(f) if r.get("site") == "Lucky Camera (일본)"}
    except (OSError, ValueError):
        pass
    print(f"\n  📂 Lucky Camera 크롤링 시작 (이전 등급 {len(known)}개)")
    last_page, page_num = 1, 1
    while page_num <= last_page and page_num < 80:
        url = f"{base}/shop/LEICA/" + (f"page/{page_num}/" if page_num > 1 else "")
        html = None
        for attempt in range(3):
            try:
                resp = sess.get(url, timeout=30)
                resp.raise_for_status()
                html = resp.text
                break
            except Exception as e:
                print(f"    ⚠️ {page_num}페이지 오류: {e}")
                time.sleep(5)
        if html is None:
            raise RuntimeError(f"Lucky Camera {page_num}페이지 못 읽음")  # 빠진 쪽이 판매완료로 바뀌지 않게
        last_page = max([last_page] + [int(n) for n in re.findall(r"/shop/LEICA/page/(\d+)/", html)])
        articles = html.split('<article class="article')[1:]
        print(f"    └─ {page_num}/{last_page}페이지 {len(articles)}개")
        for a in articles:
            if a.startswith(" soldout"):
                continue
            m = re.search(r'<h4><a href="([^"]+)">(.*?)</a></h4>', a, re.S)
            if not m:
                continue
            link = m.group(1)
            raw = unicodedata.normalize("NFKC", _html.unescape(re.sub(r"<[^>]+>", "", m.group(2)))).strip()
            if not re.search(r"leica|leitz|ライカ|ライツ", raw, re.I) or link in seen or link in globals().get('SOLD_LINKS', ()):
                continue
            seen.add(link)
            # 'LEICA(ライカ) Mエルマー 50mmF2.8(旧型) シルバー' → 'Leica Mエルマー …' → 영어 표기
            name_ja = re.sub(r"^(?:LEICA|Leica|leica)?\s*[(]?ライカ[)]?\s*", "", raw)
            name = _lucky_name(name_ja, ja_to_en)
            if any(b2 in name.lower() for b2 in THIRD_PARTY_BRANDS):
                continue
            m_price = re.search(r'class="price"><a[^>]*>\s*¥\s*([\d,]+)', a)
            amount = int(m_price.group(1).replace(",", "")) if m_price else 0
            price = f"¥{amount:,}" if amount else "문의요망"
            cond = known.get(link)
            if not cond or cond == "정보없음":
                cond = "정보없음"
                try:
                    detail = sess.get(link, timeout=30).text
                    m_grade = re.search(r"程度\s*</(?:th|dt|td)>\s*<(?:td|dd)[^>]*>\s*([^<]+?)\s*<", detail)
                    if m_grade:
                        cond = LUCKY_PREFIX + unicodedata.normalize("NFKC", m_grade.group(1)).strip()
                except Exception as e:
                    print(f"    ⚠️ 상세 오류 {unquote(link)[-40:]}: {e}")
                time.sleep(0.7)
            m_img = re.search(r'<img[^>]*src="([^"]+)"', a)
            img = re.sub(r"-\d+x\d+(?=\.jpg$)", "", m_img.group(1)) if m_img else ""
            cat = detect_category(name, price)
            mount = 'Accessory' if cat == 'Accessory' else detect_mount(name)
            results.append({
                "site": "Lucky Camera (일본)",
                "label": auto_label(name),
                "상품명": name,
                "세대": detect_generation(name),
                "컨디션": cond,
                "가격": price,
                "통화": "JPY",
                "이미지": img,
                "링크": link,
                "품절": False,
                "예약중": False,
                "mount": mount,
                "category": cat,
                "brand": detect_brand(name),
            })
        page_num += 1
        time.sleep(1)
    print(f"  ✅ Lucky Camera 완료: {len(results)}개")
    return results


AKASAKA_JA = {"ライカビット": "Leicavit ", "ワインダー": "Winder ", "フード": " Hood", "ファインダー": " Finder",
              "ケース": " Case", "フィルター": " Filter", "革張替え": "Re-leathered", "セルフ": "Self-timer",
              "改造": "Modified", "全回転": "Full Rotation", "短鏡胴": "Short Mount", "メガネ": "Goggles"}


def _akasaka_name(name_ja, ja_to_en):
    """Akasaka Camera 제목 다듬기: '沈胴ズミクロン 50/2 L 104万台' → 'Leica Collapsible Summicron 50/2 L'.
    일련번호대('104万台'·'327万代')와 '送料430円' 같은 배송비 표기는 뺀다"""
    import unicodedata
    name = unicodedata.normalize("NFKC", name_ja).replace("\u3000", " ")
    name = re.sub(r"\s*\d+万[台代]", "", name)
    name = re.sub(r"\s*送料\d+円", "", name)
    name = re.sub(r"^(?:ライカ|ライツ|Leica|Leitz)\s*", "", name)
    for ja, en in AKASAKA_JA.items():
        name = name.replace(ja, en)
    name = ja_to_en("Leica " + name)
    name = re.sub(r"Collapsible(?=\S)", "Collapsible ", name)
    # '50/2'·'28-70/3.5-4.5' → '50mm f2'·'28-70mm f3.5-4.5' (조리개로 읽혀야 렌즈로 분류됨)
    # 정수 조리개는 'f4.0'처럼 (_has_aperture가 소수점 있는 값만 조리개로 봄)
    name = re.sub(r"\b(\d{2,3}(?:-\d{2,3})?)/(\d+(?:\.\d+)?(?:-\d+(?:\.\d+)?)?)\b",
                  lambda m: f"{m.group(1)}mm f{m.group(2)}" + ("" if "." in m.group(2) else ".0"), name)
    name = re.sub(r"\b(I{1,3})([A-G])\b", lambda m: m.group(1) + m.group(2).lower(), name)  # 'IIIG' → 'IIIg'
    return re.sub(r"\s+", " ", name).strip()


def crawl_akasaka():
    """Akasaka Camera (일본, 도쿄 아카사카) - 라이카·클래식 중고점. 분류 화면(/product/index/<번호>/page:N, 정적 HTML,
    15개씩)의 카드에 이름·등급(程度)·가격·사진이 다 있다. 라이카 바디(36)·라이카 렌즈(37)·신착(25)·중고 액세서리(9)에서
    메이커가 ライカ인 것만. 'sold_out' 카드는 건너뛰고, 가격 대신 '商談中'이면 예약중"""
    import html as _html
    import unicodedata
    import requests
    from ja_normalize import ja_to_en
    from condition_grade import AKASAKA_PREFIX
    results, seen = [], set()
    base = "https://www.akasaka-camera.com"
    sess = requests.Session()
    sess.headers["User-Agent"] = random.choice(USER_AGENTS)
    print("\n  📂 Akasaka Camera 크롤링 시작")
    for cat_id in (36, 37, 25, 9):
        page_num = 1
        while page_num < 40:
            url = f"{base}/product/index/{cat_id}/page:{page_num}"
            html = None
            for attempt in range(3):
                try:
                    resp = sess.get(url, timeout=30)
                    resp.raise_for_status()
                    html = resp.text
                    break
                except Exception as e:
                    print(f"    ⚠️ {cat_id}분류 {page_num}페이지 오류: {e}")
                    time.sleep(5)
            if html is None:
                raise RuntimeError(f"Akasaka Camera {cat_id}분류 {page_num}페이지 못 읽음")  # 빠진 쪽이 판매완료로 바뀌지 않게
            cards = html.split('<figure class="product_figure')[1:]
            print(f"    └─ {cat_id}분류 {page_num}페이지 {len(cards)}개")
            for card in cards:
                if card.startswith(" sold_out"):
                    continue
                def cell(label):
                    m = re.search(label + r"</th>\s*<td>(.*?)</td>", card, re.S)
                    return unicodedata.normalize("NFKC", _html.unescape(re.sub(r"<[^>]+>", "", m.group(1)))).strip() if m else ""
                if not re.search(r"ライカ|ライツ|leica|leitz", cell("メーカー"), re.I) or cell("メーカー").startswith("N.Y."):
                    continue
                m_link = re.search(r'<a href="(https://www\.akasaka-camera\.com/product/view/\d+)"', card)
                if not m_link or m_link.group(1) in seen:
                    continue
                link = m_link.group(1)
                seen.add(link)
                if "ロッコール" in cell("品名"):  # 미놀타 M-Rokkor (라이츠 제조라도 미놀타 상표)
                    continue
                name = _akasaka_name(cell("品名"), ja_to_en)
                if any(b2 in name.lower() for b2 in THIRD_PARTY_BRANDS):
                    continue
                m_price = re.search(r'class="price[^"]*">\s*([\d,]+)', card)
                amount = int(m_price.group(1).replace(",", "")) if m_price else 0
                price = f"¥{amount:,}" if amount else "문의요망"
                grade = cell("程度")
                m_img = re.search(r'<img src="([^"]+)"', card)
                img = ("https:" + m_img.group(1) if m_img.group(1).startswith("//") else m_img.group(1)) if m_img else ""
                cat = detect_category(name, price)
                mount = 'Accessory' if cat == 'Accessory' else detect_mount(name)
                results.append({
                    "site": "Akasaka Camera (일본)",
                    "label": auto_label(name),
                    "상품명": name,
                    "세대": detect_generation(name),
                    "컨디션": AKASAKA_PREFIX + grade if grade and grade not in ("ー", "-") else "정보없음",
                    "가격": price,
                    "통화": "JPY",
                    "이미지": img,
                    "링크": link,
                    "품절": False,
                    "예약중": "商談中" in card,
                    "mount": mount,
                    "category": cat,
                    "brand": detect_brand(name),
                })
            if f"/product/index/{cat_id}/page:{page_num + 1}" not in html:
                break
            page_num += 1
            time.sleep(1)
    print(f"  ✅ Akasaka Camera 완료: {len(results)}개")
    return results


GLAZERS_EXTRA_FAMILY = {("M", "35", "3.5"): "Summaron", ("R", "180", "3.4"): "APO Telyt", ("SL", "100-400", ""): "Vario Elmar",
                        ("TL", "60", "2.8"): "APO Macro Elmarit"}


def _glazers_lens_name(name):
    """'Leica M 50mm F1.4 ASPH' → 'Leica Summilux-M 50mm f1.4 ASPH'. 계열 이름 없이 마운트·초점거리·조리개만 쓴 제목에
    entity_catalog의 매장식 계열 표(IMPLIED_FAMILY·IMPLIED_BY_MOUNT)로 이름을 넣는다"""
    from entity_catalog import IMPLIED_FAMILY, IMPLIED_BY_MOUNT, ZOOM_FAMILY, FAMILY_WORD
    name = re.sub(r"\bPC SUP(?:ER)? ANG\b", "PC-Super-Angulon-R", name, flags=re.I)
    name = re.sub(r"\bSuper Angulon R\b", "Super-Angulon-R", name, flags=re.I)
    m = re.match(r"^Leica (M|SL|R|TL)\s+(APO\s+)?(\d{2,3}(?:-\d{2,3})?)(?:mm)?\s*(?:F|f/?)?\s*(\d+(?:\.\d+)?(?:-\d+(?:\.\d+)?)?)?\b(.*)$", name, re.I)
    if not m or FAMILY_WORD.search(name):
        return name
    mount, apo, focal, ap, rest = m.group(1).upper(), m.group(2), m.group(3), m.group(4) or "", m.group(5)
    ap1 = ap.split("-")[0]
    fam = GLAZERS_EXTRA_FAMILY.get((mount, focal, ap1)) or GLAZERS_EXTRA_FAMILY.get((mount, focal, ""))
    if not fam and "-" in focal:
        fam = ZOOM_FAMILY.get(mount)
    if not fam:
        fam = (IMPLIED_FAMILY if mount == "M" else IMPLIED_BY_MOUNT.get(mount, {})).get((focal, ap1))
    if not fam:
        return name
    if apo and not fam.upper().startswith("APO"):
        fam = "APO " + fam
    fam = fam.replace(" ", "-")
    ap_txt = f" f{ap}" if ap else ""
    return re.sub(r"\s+", " ", f"Leica {fam}-{mount} {focal}mm{ap_txt} {rest}").strip()


def crawl_glazers():
    """Glazer's Camera (미국, 시애틀) - Shopify JSON. 라이카 컬렉션(collections/leica, 약 300개)에서 'Used' 태그만.
    등급은 제목 괄호 (M)·(EX)·(VG)·(G)·(Good)·(Fair). 'Mozilla/5.0'만 보내면 429라 브라우저 UA로, 쪽 사이 4초"""
    import requests
    from condition_grade import GLAZERS_PREFIX
    results, seen = [], set()
    base = "https://glazerscamera.com"
    print(f"\n  📂 Glazer's Camera 크롤링 시작")
    s = requests.Session()
    s.headers["User-Agent"] = random.choice(USER_AGENTS)
    s.headers["Accept"] = "application/json"
    for page_num in range(1, 20):
        products = None
        for attempt in range(4):
            try:
                resp = s.get(f"{base}/collections/leica/products.json", params={"limit": 250, "page": page_num}, timeout=30)
                if resp.status_code == 429:
                    time.sleep(int(resp.headers.get("Retry-After") or 0) or 20 * (attempt + 1))
                    continue
                resp.raise_for_status()
                products = resp.json().get("products", [])
                break
            except Exception as e:
                print(f"    ⚠️ {page_num}페이지 오류: {e}")
                time.sleep(5)
        if products is None:
            raise RuntimeError(f"Glazer's {page_num}페이지 못 읽음")  # 빠진 쪽이 판매완료로 바뀌지 않게
        if not products:
            break
        print(f"    └─ {page_num}페이지 {len(products)}개 상품 발견")
        for p in products:
            if "Used" not in (p.get("tags") or []):
                continue
            title = re.sub(r"^used\s+", "", (p.get("title") or "").strip(), flags=re.I)
            # 'Leica M 50mm F1.4 ASPH (G) Missing Hood' → 등급 G, 이름은 괄호 앞뒤를 잇는다
            m_grade = re.search(r"\((M|EX|VG|G|Good|Fair|Poor)\)", title, re.I)
            grade = m_grade.group(1) if m_grade else ""
            name = re.sub(r"\s*\((?:M|EX|VG|G|Good|Fair|Poor)\)\s*", " ", title, flags=re.I)
            name = re.sub(r"^LEICA\b", "Leica", name)
            name = re.sub(r"\bW/\s*", "with ", name, flags=re.I)
            # 덧붙인 메모 중 분류를 흔드는 말('No Box or case'·'Missing Hood')은 뗀다
            name = re.sub(r"\s*\b(?:no box(?: or case)?|missing hood)\b", "", name, flags=re.I)
            name = re.sub(r"\bHG-SCL(\d)", r"Handgrip HG-SCL\1", name)
            name = re.sub(r"\bKIT\b", "Body Kit", name)
            name = re.sub(r"(Kit with \d{2,3}-\d{2,3})\s?mm\b", r"\1 zoom", name, flags=re.I)  # 렌즈 표기 때문에 바디 연결이 막히지 않게
            name = re.sub(r"\bEV-1\b", "EV1", name)
            name = _glazers_lens_name(name)
            # 카메라 분류 태그인데 이름에 Body·렌즈 표기가 없으면 Body ('Leica M EV-1'·'Leica X1'·'Leica R4s')
            used_tag = " ".join(t for t in p.get("tags") or [] if t.startswith("Used:"))
            if (re.search(r"Rangefinder Cameras?|SLR Cameras|Used Mirrorless$|Digital Compacts", used_tag)
                    and not re.search(r"body|\d\s*mm|case|strap|grip|cap\b|\b\d{5}\b", name, re.I)):
                name = re.sub(r"^(\S+\s+\S+(?:\s+(?:Typ|Type)\s+\d+)?)", r"\1 Body", name) if re.search(r"Typ|Type", name) else name + " Body"
            name = re.sub(r"\s+", " ", name).strip()
            if not re.match(r"leica|leitz", name, re.I) or any(b2 in name.lower() for b2 in THIRD_PARTY_BRANDS):
                continue
            link = f"{base}/products/{p['handle']}" if p.get("handle") else ""
            if not link or link in seen or link in globals().get('SOLD_LINKS', ()):
                continue
            seen.add(link)
            variant = p["variants"][0] if p.get("variants") else {}
            try:
                price = f"${float(variant.get('price')):,.0f}"
            except (TypeError, ValueError):
                price = "문의요망"
            img = p["images"][0].get("src", "") if p.get("images") else ""
            cat = detect_category(name, price)
            mount = 'Accessory' if cat == 'Accessory' else detect_mount(name)
            results.append({
                "게시일": _shopify_listed(p),
                "site": "Glazers Camera (미국)",
                "label": auto_label(name),
                "상품명": name,
                "세대": detect_generation(name),
                "컨디션": GLAZERS_PREFIX + grade if grade else "정보없음",
                "가격": price,
                "통화": "USD",
                "이미지": img,
                "링크": link,
                "품절": not any(v.get("available") for v in p.get("variants") or [{}]),
                "예약중": False,
                "mount": mount,
                "category": cat,
                "brand": detect_brand(name),
            })
        time.sleep(4)
    print(f"  ✅ Glazer's Camera 완료: {len(results)}개")
    return results


def crawl_tamarkin():
    """Tamarkin Camera (미국, 시카고) - 라이카 딜러. 분류 화면 7곳(정적 HTML, 쪽 넘김 없음)의 카드에 이름·가격·사진,
    중고 여부와 등급은 상세 화면 가격 아래 'Nr. 258xxxx, Ex++' 줄에만 있어 카드마다 상세를 읽는다 (약 170개 · 1분)
    → 6시간마다. 이 줄이 없는 것은 새 제품이라 뺀다. 'SOLD OUT'·가격 $0은 건너뜀"""
    import html as _html
    import requests
    from concurrent.futures import ThreadPoolExecutor
    from condition_grade import TAMARKIN_PREFIX
    base = "https://www.tamarkin.com/products/"
    cats = ["m-series/cameras", "m-series/lenses", "m-series/accessories", "leica-screw-mount", "collectibles",
            "sl-system", "compact-digital"]
    sess = requests.Session()
    sess.headers["User-Agent"] = random.choice(USER_AGENTS)
    print("\n  📂 Tamarkin Camera 크롤링 시작")
    cards, seen = [], set()
    for cat in cats:
        try:
            resp = sess.get(base + cat, timeout=30)
            resp.raise_for_status()
        except Exception as e:
            raise RuntimeError(f"Tamarkin {cat} 못 읽음: {e}")  # 빠진 분류가 판매완료로 바뀌지 않게
        found = re.findall(r'<div class="prod-card[^"]*"[^>]*>\s*<a href="([^"]+)".*?<img data-src="([^"]+)".*?'
                           r'product-card__title">(.*?)</div>\s*<div class="prod-card__price">\s*(.*?)\s*</div>', resp.text, re.S)
        print(f"    └─ {cat} {len(found)}개")
        for link, img, title, price in found:
            if link not in seen:
                seen.add(link)
                cards.append((link, img, _html.unescape(re.sub(r"<[^>]+>", "", title)).strip(), price.strip(), cat))

    def detail(card):
        link, img, title, price, _cat = card
        if "sold out" in title.lower() or not re.search(r"[1-9]", price):
            return None
        try:
            h = sess.get(link, timeout=30).text
        except Exception as e:
            print(f"    ⚠️ 상세 오류 {link[-40:]}: {e}")
            return None
        text = _html.unescape(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", re.sub(r"<script.*?</script>|<style.*?</style>", "", h, flags=re.S))))
        m = re.search(re.escape(price) + r"\s+(?:Nr\.\s*)?\d+x+,\s*([A-Za-z +]+?)\s+Interested\?", text)
        return (card, m.group(1).strip()) if m else None

    with ThreadPoolExecutor(4) as ex:
        used = [x for x in ex.map(detail, cards) if x]
    results = []
    for (link, img, title, price, from_cat), grade in used:
        name = title.replace("Summliux", "Summilux").replace("Elmarit-RF", "Elmarit-M")
        name = re.sub(r"\bf(\d+),(\d+)", r"f\1.\2", name)  # 'f1,4' → 'f1.4'
        name = re.sub(r"\s*-\s*DISCONTINUED\b", "", name, flags=re.I)
        name = re.sub(r"^(\d{2,3}(?:-\d{2,3})*)\s+", r"\1mm ", name)  # '35 Summilux' → '35mm Summilux'
        if not re.match(r"leica|leitz", name, re.I):
            name = "Leica " + name
        if from_cat in ("m-series/cameras", "compact-digital") and not re.search(r"\bbody\b", name, re.I):
            name = re.sub(r"(\s+OPEN BOX)?$", lambda m: " Body" + (m.group(1) or ""), name, count=1)  # 'Leica Q3' → 'Leica Q3 Body'
        name = re.sub(r"\s+", " ", name).strip()
        if any(b2 in name.lower() for b2 in THIRD_PARTY_BRANDS):
            continue
        cat = detect_category(name, price)
        mount = 'Accessory' if cat == 'Accessory' else detect_mount(name)
        results.append({
            "site": "Tamarkin Camera (미국)",
            "label": auto_label(name),
            "상품명": name,
            "세대": detect_generation(name),
            "컨디션": TAMARKIN_PREFIX + grade,
            "가격": price.replace(" ", ""),
            "통화": "USD",
            "이미지": img,
            "링크": link,
            "품절": False,
            "예약중": False,
            "mount": mount,
            "category": cat,
            "brand": detect_brand(name),
        })
    print(f"  ✅ Tamarkin Camera 완료: {len(results)}개 (카드 {len(cards)}개 중 중고)")
    return results


def _nivo_name(title):
    """Nivo Schweitzer 제목 다듬기: 'occasion LEICA 11604 Summicron-M 28mm/2.0 ASPH. • black • 6-bit coding [sn #4068634]'
    → 'Leica 11604 Summicron-M 28mm f/2.0 ASPH. black 6-bit coding'. 일련번호·창고 기호(TB288·DOR172·E46·OT:518)는 떼고
    네덜란드어 부속 이름은 영어로"""
    name = re.sub(r"^\s*occasion\s+", "", title, flags=re.I)
    name = re.sub(r"\[\s*(?:sn\b|#)[^\]]*\]|\bNo:\s*\d+|\b(?:TB|DOR:?|OT:)\s?\d+\b|\bE\d{2}\b", " ", name, flags=re.I)
    name = re.sub(r"\[\s*typ\s*(\d+)\s*\]", r"(Typ \1)", name, flags=re.I)  # 'Q [typ 116]' → 'Q (Typ 116)'
    name = re.sub(r"\[(Leica[^\]]*|Leicaflex[^\]]*)\]", r"for \1", name)  # '[Leica M10]' → 'for Leica M10'
    name = re.sub(r"\[([\d,\s]+)[^\]]*\]", " ", name)
    # 조리개는 'f2.0' 꼴로 (분류기의 렌즈 판별이 'f/2.0'은 못 읽음)
    name = re.sub(r"(\d+(?:-\d+)?)mm/(\d+(?:\.\d+)?)", r"\1mm f\2", name)  # '28mm/2.0' → '28mm f2.0'
    name = re.sub(r"\b(\d),(\d)/(\d+-\d+)mm", r"\3mm f\1.\2", name)  # '4,5/75-200mm' → '75-200mm f4.5'
    name = re.sub(r"\b(?:Elmarit|Summicron|Summilux|Elmar)(?:-[MR])?\s+(\d\.\d)\s+(\d+)mm", lambda m: m.group(0).replace(f"{m.group(1)} {m.group(2)}mm", f"{m.group(2)}mm f{m.group(1)}"), name)  # 'Elmarit-M 2.8 90mm'
    name = re.sub(r"(\d+mm)/(\d+(?:\.\d+)?)", r"\1 f\2", name)
    for nl, en in ((r"opsteekzoeker", "Viewfinder"), (r"flitser", "Flash"), (r"tussenringen", "extension tubes"),
                   (r"Universele Polarisatiefilter", "Universal Polarizing Filter"), (r"Combitas", "Combination Case"),
                   (r"Ever ready case", "Ever Ready Case"), (r"\bdoos\b", "box"), (r"accu'?s?\b", "batteries"),
                   (r"\bdop(?:pen)?\b", "cap"), (r"voor/achter", "front/rear"), (r"\bachter\b", "rear"), (r"\+ zk\b", "with hood")):
        name = re.sub(nl, en, name, flags=re.I)
    name = re.sub(r"\bincl\.?\s*", "with ", name, flags=re.I)
    name = re.sub(r"^LEICA\s+LEITZ WETZLAR\b", "Leitz Wetzlar", name)
    name = re.sub(r"^LEICA\b", "Leica", name)
    name = re.sub(r"\s+-M\b", "-M", name)  # 'Noctilux -M' → 'Noctilux-M'
    name = name.replace("•", " ")
    name = re.sub(r"\s+", " ", name).strip(" ,")
    # 바디·렌즈 뒤 부속 목록('with Visoflex'·'with 2 batteries'·'with box')은 분류를 흔들어 뗀다
    if re.search(r"\bbody\b|\d+mm\b|\(Typ \d+\)", name, re.I) and not re.search(r"Viewfinder|Extender|Case|Flash", name):
        name = re.split(r"\s+with\s+", name)[0]
    # 카메라 이름 뒤에 Body ('Leica 19000 Q (Typ 116)' → '… Body', 'SL2 body' → 'SL2 Body')
    name = re.sub(r"\bbody\b", "Body", name)
    if re.match(r"Leica (?:\d{5} )?(?:Q\d?|SL\d?|M\d+(?:-\w+)?|CL|TL2?)(?: \(Typ \d+\))?(?: (?:black|silver)(?: chrome| paint)?)?$", name, re.I):
        name += " Body"
    return name


def crawl_nivo():
    """Nivo Schweitzer (네덜란드, 암스테르담) - 라이카 매장. 'Leica occasions' 분류 화면(정적 HTML, ?page=N 24개씩)에
    이름·가격(부가세 포함)·재고 표시. 등급 표기는 목록·상세 어디에도 없어 등급 없이 담는다. 마지막 쪽을 넘기면
    마지막 쪽이 다시 나오므로 첫 상품이 같으면 멈춤. 'Niet op voorraad'(재고 없음)는 품절"""
    import html as _html
    import requests
    base = "https://www.nivo-schweitzer.nl"
    sess = requests.Session()
    sess.headers["User-Agent"] = random.choice(USER_AGENTS)
    print("\n  📂 Nivo Schweitzer 크롤링 시작")
    results, seen, first_ids = [], set(), set()
    for page_num in range(1, 30):
        try:
            resp = sess.get(f"{base}/leica-winkel/leica-occasions/c23442?page={page_num}", timeout=30)
            resp.raise_for_status()
        except Exception as e:
            raise RuntimeError(f"Nivo {page_num}쪽 못 읽음: {e}")  # 빠진 쪽이 판매완료로 바뀌지 않게
        boxes = re.findall(r"id='artikel_(\d+)'(.*?)priceExclBtw", resp.text, re.S)
        if not boxes or boxes[0][0] in first_ids:
            break
        first_ids.add(boxes[0][0])
        print(f"    └─ {page_num}페이지 {len(boxes)}개")
        for _id, blk in boxes:
            t = re.search(r'productboxLink" href="([^"]+)">([^<]+)', blk)
            if not t:
                continue
            title = _html.unescape(t.group(2)).strip()
            if not re.match(r"\s*occasion\s+leica\b", title, re.I):
                continue  # Zeiss ZM·Voigtländer 등 다른 브랜드
            link = base + t.group(1)
            if link in seen:
                continue
            seen.add(link)
            name = _nivo_name(title)
            if any(b2 in name.lower() for b2 in THIRD_PARTY_BRANDS):
                continue
            pm = re.search(r'priceInclBtw">\s*(?:&euro;|€)(?:&nbsp;|\s)*([\d.]+),(\d{2})', blk)
            price = f"€{int(pm.group(1).replace('.', '')):,}" if pm else "문의요망"
            img = re.search(r'<img src="([^"]+)"[^>]*class="prodImage"', blk)
            img = (base + img.group(1)) if img and img.group(1).startswith("/") else (img.group(1) if img else "")
            sold = "Niet op voorraad" in blk
            if sold and link in globals().get('SOLD_LINKS', ()):
                continue
            cat = detect_category(name, price)
            mount = 'Accessory' if cat == 'Accessory' else detect_mount(name)
            results.append({
                "site": "Nivo Schweitzer (네덜란드)",
                "label": auto_label(name),
                "상품명": name,
                "세대": detect_generation(name),
                "컨디션": "정보없음",
                "가격": price,
                "통화": "EUR",
                "이미지": img,
                "링크": link,
                "품절": sold,
                "예약중": False,
                "mount": mount,
                "category": cat,
                "brand": detect_brand(name),
            })
        time.sleep(2)
    print(f"  ✅ Nivo Schweitzer 완료: {len(results)}개")
    return results


def _fotohandel_name(title):
    """fotohandel.de 제목 다듬기: 'Leica Elmarit 28mm 2.8 Version II - 11801' → 'Leica Elmarit 28mm f2.8 Version II 11801'.
    가게 꼬리('| fotohandel.de …')·'werkstattüberholt'·'in OVP'·'Leica Service' 같은 정비·상자 말은 떼고, 조리개는 'f2.8' 꼴로
    (분류기가 '28mm 2.8'은 렌즈로 못 읽음), 독일어 색·부속 이름은 영어로"""
    name = re.sub(r"\s*\|\s*fotohandel\.de.*$", "", title.strip(), flags=re.I)
    name = re.sub(r"\s*-?\s*\b(?:werkstatt(?:ü|ue)berholt|aktueller leica service|leica service|in OVP|Tauschsensor|neuwertig)\b",
                  " ", name, flags=re.I)
    name = re.sub(r"\s*-\s*Betriebsk\.?$", "", name)
    name = re.sub(r"[„“\"]", "", name)
    name = re.sub(r"Macro-Set M Macro\s*\|\s*Elmar-M", "Macro-Elmar-M", name)  # 매크로 세트 (렌즈+어댑터)
    name = name.replace(" | ", " ")
    name = re.sub(r"\bschwarz\s+eloxiert\b", "black anodized", name, flags=re.I)
    name = re.sub(r"\bschwarz\s+lackiert\b", "black paint", name, flags=re.I)
    name = re.sub(r"\bblack chrome\b", "black", name, flags=re.I)  # M4 검정 크롬은 보통 판 (50 Jahre 기념판과 갈리게)
    name = re.sub(r"\bschwarz\b", "black", name, flags=re.I)
    name = re.sub(r"\bchrom\b", "chrome", name, flags=re.I)
    name = re.sub(r"\bsilber\b", "silver", name, flags=re.I)
    name = re.sub(r"\bGegenlichtblende\b", "Lens Hood", name, flags=re.I)
    name = re.sub(r"\bBetriebskamera\b", "Company Camera", name, flags=re.I)
    name = re.sub(r"\bmit\b", "with", name)
    name = re.sub(r"\b(\d{2,3}mm)\s+(\d(?:\.\d)?)(?=\s|$)", r"\1 f\2", name)  # '28mm 2.8' → '28mm f2.8'
    name = re.sub(r"\bf(\d)(?![\d.])", r"f\1.0", name)  # 'f2' → 'f2.0'
    name = re.sub(r"\s+-\s+", " ", name)
    name = re.sub(r"\s+", " ", name).strip(" ,-*|")
    if re.match(r"Leica (?:M\d|MP|M-[AP]|CL|Q\d?|SL\d?|Minilux|R\d)\b", name) and not re.search(
            r"\d+mm|Hood|Book|Akku|Griff|Sucher|Visoflex|Kit\b", name, re.I):
        name += " Body"  # 'Leica M1 chrome'처럼 바디 이름만 있으면 렌즈로 갈리지 않게
    return name


def crawl_fotohandel():
    """fotohandel.de (독일, 쇼른도르프) - 라이카·핫셀 중고 전문점(Shopware). 라이카 분류 아래 하위 분류 6곳(정적 HTML, 모두 36개
    이하라 쪽 넘김 없음 — robots.txt가 ?p= 쪽 넘김을 막음)의 카드에 이름·가격·사진·'Zustandsbeschreibung' 등급(A·A-·A-B·B·B-·B-C).
    'Lieblingsstücke|Archiv' 표시나 가격 0은 판매 끝난 보관 글이라 뺌. 라이카가 아닌 것(KEKS·Sigma 등)도 뺌"""
    import html as _html
    import json as _json
    import requests
    from condition_grade import FOTOHANDEL_PREFIX
    base = "https://www.fotohandel.de/Leica/"
    cats = ["Leica-M-gebraucht/Leica-M-Kameras-analog/", "Leica-M-gebraucht/Leica-M-Kameras-digital/",
            "Leica-M-gebraucht/Leica-M-Objektive/", "Leica-R-gebraucht/", "Leica-Sonstige-digital-gebraucht/",
            "Leica-Minilux-Kompaktkameras-analog/", "Suchauftrag-Benachrichtigung/Leica-Neuzugaenge/"]
    sess = requests.Session()
    sess.headers["User-Agent"] = random.choice(USER_AGENTS)
    print("\n  📂 fotohandel.de 크롤링 시작")
    results, seen = [], set()
    for cat in cats:
        try:
            resp = sess.get(base + cat, timeout=30)
            resp.raise_for_status()
        except Exception as e:
            raise RuntimeError(f"fotohandel {cat} 못 읽음: {e}")  # 빠진 분류가 판매완료로 바뀌지 않게
        boxes = resp.text.split('class="card product-box')[1:]
        print(f"    └─ {cat} {len(boxes)}개")
        for blk in boxes:
            info = re.search(r'data-product-information="([^"]+)"', blk)
            link = re.search(r'href="([^"]+)"[^>]*class="product-name', blk)
            if not info or not link:
                continue
            link = link.group(1)
            if link in seen or "Archiv" in blk:
                continue
            seen.add(link)
            try:
                d = _json.loads(_html.unescape(info.group(1)))
            except ValueError:
                continue
            title = re.sub(r"\s+", " ", d.get("name") or "").strip()
            if not title.lower().startswith("leica") or (d.get("brand") or "Leica").strip().lower() != "leica":
                continue
            price = float(d.get("price") or 0)
            if price <= 0:
                continue
            name = _fotohandel_name(title)
            if any(b2 in name.lower() for b2 in THIRD_PARTY_BRANDS):
                continue
            grade = "".join(re.findall(r'zustand_uebersicht">\s*([^<]*?)\s*<', blk))
            img = re.search(r'<img src="([^"?]+)', blk)
            cat_ = detect_category(name, f"€{int(price):,}")
            mount = 'Accessory' if cat_ == 'Accessory' else detect_mount(name)
            results.append({
                "site": "fotohandel.de (독일)",
                "label": auto_label(name),
                "상품명": name,
                "세대": detect_generation(name),
                "컨디션": FOTOHANDEL_PREFIX + grade if grade else "정보없음",
                "가격": f"€{int(round(price)):,}",
                "통화": "EUR",
                "이미지": img.group(1) if img else "",
                "링크": link,
                "품절": False,
                "예약중": False,
                "mount": mount,
                "category": cat_,
                "brand": detect_brand(name),
            })
        time.sleep(2)
    print(f"  ✅ fotohandel.de 완료: {len(results)}개")
    return results


SANPOU_JA = {"ストローク": " Stroke", "セルフタイマー付": "Self-timer", "シャークスキン": "Sharkskin", "ヌーキー": "with NOOKY",
             "固定鏡筒": "Rigid", "6枚玉": "6-element", "8枚玉": "8-element", "ツノ無し": "", "逆ローレット": "",
             "(ヒョットコ)": "", "フラッシュ": "Flash", "直立": "Upright ", "型": "", "Lマウント": "L", "ドイツ": "Germany",
             "ビゾ用": "", "前期": "", "後期": "", "初期": "", "キャップ": "Cap", "フード": "Hood"}


def _sanpou_name(title, ja_to_en):
    """三宝カメラ 제목 다듬기: 'Leica ズミクロンM35mm F2 (6枚玉) ツノ無し 【B】' → 'Leica Summicron-M 35mm f2.0 (6-element)'.
    끝의 【등급】은 떼고(따로 읽음), 'Elmar90mm'처럼 붙은 초점거리는 띄우고, 'F2.8'은 'f2.8'로"""
    import unicodedata
    name = unicodedata.normalize("NFKC", title).replace("\u3000", " ")
    name = re.sub(r"【[^】]*】", "", name)
    for ja, en in SANPOU_JA.items():
        name = name.replace(ja, en)
    name = ja_to_en(name)
    name = re.sub(r"\bBODY\b", "Body", name)
    name = re.sub(r"([A-Za-z])(\d{2,3})(?=mm|\s+F\d)", r"\1 \2", name)  # 'Elmar90mm'·'Elmar35 F3.5'
    name = re.sub(r"\b(\d{2,3})\s+F(\d)", r"\1mm F\2", name)  # 'Elmar 35 F3.5' → 'Elmar 35mm F3.5'
    name = re.sub(r"\bF(\d+(?:\.\d+)?)", lambda m: "f" + m.group(1) + ("" if "." in m.group(1) else ".0"), name)
    name = re.sub(r"\(\s*\)", "", name)
    name = re.sub(r"\bElmar (65mm)", r"Viso-Elmar \1", name)  # 비조플렉스용 엘마 65
    name = re.sub(r"\bD II\b", "II (D) Body", name)  # 'D II + 50mm' (바디+렌즈 세트) → 바디로
    name = re.sub(r"\b(I{1,3})\s+([a-gA-G])\b", lambda m: m.group(1) + m.group(2).lower(), name)  # 'III f' → 'IIIf'
    name = re.sub(r"\b(Summilux|Summicron|Summaron|Elmarit|Elmar|Macro-Elmar) (M|R) (?=\d)", r"\1-\2 ", name, flags=re.I)
    return re.sub(r"\s+", " ", name).strip(" ,-")


def crawl_sanpou():
    """三宝カメラ (일본, 도쿄 신주쿠) - 클래식·라이카 중고점(MakeShop, EUC-JP). 라이카 카메라(ct316)·렌즈(ct330)·
    액세서리(ct344) 분류 화면(정적 HTML, 한 쪽에 다 나옴 — page2/는 비어 있음)의 카드에 이름·가격·사진,
    제목 끝 【AB】·【B】가 등급. robots.txt 없음. 품절 상품은 목록에서 빠짐"""
    import html as _html
    import requests
    from ja_normalize import ja_to_en
    from condition_grade import SANPOU_PREFIX
    base = "https://www.sanpou.ne.jp"
    sess = requests.Session()
    sess.headers["User-Agent"] = random.choice(USER_AGENTS)
    print("\n  📂 三宝カメラ 크롤링 시작")
    results, seen = [], set()
    for ct in (316, 330, 344):
        for page_num in range(1, 10):
            url = f"{base}/shopbrand/ct{ct}/" if page_num == 1 else f"{base}/shopbrand/ct{ct}/page{page_num}/order/"
            try:
                resp = sess.get(url, timeout=30)
                resp.raise_for_status()
            except Exception as e:
                raise RuntimeError(f"三宝カメラ ct{ct} {page_num}쪽 못 읽음: {e}")  # 빠진 쪽이 판매완료로 바뀌지 않게
            text = resp.content.decode("euc-jp", "ignore")
            cards = text.split('<div class="img-item-list">')[1:]
            print(f"    └─ ct{ct} {page_num}페이지 {len(cards)}개")
            if not cards:
                break
            for card in cards:
                m = re.search(r'<p class="item-name"><a href="(/shopdetail/(\d+))[^"]*">([^<]+)</a>', card)
                if not m or m.group(2) in seen:
                    continue
                seen.add(m.group(2))
                title = _html.unescape(m.group(3)).strip()
                if not re.match(r"\s*(?:leica|leitz|ライカ)", title, re.I):
                    continue
                name = _sanpou_name(title, ja_to_en)
                if any(b2 in name.lower() for b2 in THIRD_PARTY_BRANDS):
                    continue
                grade = re.findall(r"【([^】]+)】", title)
                pm = re.search(r'<p class="price">(?:<!--[^>]*-->)?\s*([\d,]+)円', card)
                price = f"¥{int(pm.group(1).replace(',', '')):,}" if pm else "문의요망"
                img = re.search(r'<img[^>]+src="([^"]+)"', card)
                cat = detect_category(name, price)
                mount = 'Accessory' if cat == 'Accessory' else detect_mount(name)
                results.append({
                    "site": "三宝カメラ (일본)",
                    "label": auto_label(name),
                    "상품명": name,
                    "세대": detect_generation(name),
                    "컨디션": SANPOU_PREFIX + grade[-1].strip() if grade else "정보없음",
                    "가격": price,
                    "통화": "JPY",
                    "이미지": img.group(1) if img else "",
                    "링크": f"{base}{m.group(1)}/",
                    "품절": False,
                    "예약중": False,
                    "mount": mount,
                    "category": cat,
                    "brand": detect_brand(name),
                })
            if f"/shopbrand/ct{ct}/page{page_num + 1}/" not in text:
                break
            time.sleep(2)
        time.sleep(2)
    print(f"  ✅ 三宝カメラ 완료: {len(results)}개")
    return results


_HEIDELBERG_WORDS = [(r"schwarz(?:es)? glänzend(?: lackiert)?", "black gloss paint"), (r"schwarz(?:es)?", "black"),
                     (r"silber", "silver"), (r"Metallgrau", "Metal Grey"), (r"olivgrün", "olive green"),
                     (r"Gegenlichtblende", "Lens Hood"), (r"Objektivdeckel", "Lens Cap"), (r"Akku", "Battery"),
                     (r"Daumenstütze", "Thumb Support"), (r"Handgriff", "Handgrip"), (r"Trageriemen", "Strap"),
                     (r"Leder", "Leather"), (r"Messing", "Brass"), (r"Protektor", "Protector"), (r"für", "for"),
                     (r"rund", "round"), (r"Polfilter", "Polarizing Filter"), (r"Kabelfernauslöser", "Cable Release"),
                     (r"Elektrischer", "Electric")]


def _heidelberg_name(title):
    """Leica Store Heidelberg 제목 다듬기: 'Leica Summilux-M F1.4 50mm ASPH. 11728' → 'Leica Summilux-M 50mm f1.4 ASPH. 11728'.
    조리개를 초점거리 앞에 쓴 표기를 뒤로 옮기고(분류기는 '50mm f1.4' 꼴을 읽음), 독일식 소수점(F3,5)·'1:1.4/35' 표기를 고치고,
    렌즈·바디 뒤 'mit …'(딸린 필터·보호대 목록)는 떼고, 독일어 색·부속 이름은 영어로"""
    import unicodedata
    name = re.sub(r"\s+", " ", unicodedata.normalize("NFC", title)).strip()  # Shopify 제목의 ü가 나뉜 글자(NFD)라 합침
    name = re.sub(r"(\d),(\d)", r"\1.\2", name)
    name = name.replace("Power Set", "Charger Power Set")
    name = re.sub(r"Vario-Elmarit-SL\s+100-400", "Vario-Elmar-SL 100-400", name)  # 매장 오타 (100-400은 Vario-Elmar)
    name = re.sub(r"\s+-\s+(?:originale?s?\b.*)?", " ", name)
    name = re.sub(r"\s+mit\s+(?:UV Filter|Brille|Protektor)\b.*$", "", name)
    name = re.sub(r"\b1:(\d+(?:\.\d+)?)/(\d{2,3})\b", r"\2mm F\1", name)  # '1:1.4/35' → '35mm F1.4'
    name = re.sub(r"\b[fF]/?(\d+(?:\.\d+)?(?:-\d+(?:\.\d+)?)?)\s+(\d{2,3}(?:-\d{2,3})?mm)\b", r"\2 F\1", name)
    name = re.sub(r"\b[fF]/?(\d+(?:\.\d+)?)(?=[\s-]|$)", lambda m: "f" + m.group(1) + ("" if "." in m.group(1) else ".0"), name)
    for de, en in _HEIDELBERG_WORDS:
        name = re.sub(rf"\b{de}\b", en, name, flags=re.I)
    name = re.sub(r"\bmit\b", "with", name)
    name = re.sub(r"\s+", " ", name).strip(" ,-")
    if re.match(r"Leica (?:M\d|MP|M-[AP]|CL|Q\d?|SL\d?|R\d)(?:[- ]\S+)?(?: (?:black|silver|Metal Grey|Monochrom|black gloss paint))*$", name):
        name += " Body"  # 'Leica M6 black'처럼 바디 이름만 있으면 렌즈로 갈리지 않게
    return name


def crawl_heidelberg():
    """Leica Store Heidelberg (독일) - 라이카 매장(Shopify)의 'Pre-Owned' 컬렉션 JSON (판매 중 70개쯤). 벤더가 모두
    매장 이름이라 제목이 Leica·Leitz로 시작하는 것만 담음(Voigtländer·Zeiss·Sigma·Nikon 등은 뺌). 등급은 설명의
    'Schulnote 1-2'(독일 학교 점수, 1이 가장 좋음), 매장 진열품은 'Demo'"""
    import html as _html
    import requests
    from condition_grade import HEIDELBERG_PREFIX
    results = []
    base = "https://leica-store-heidelberg.de"
    print(f"\n  📂 Leica Store Heidelberg 크롤링 시작")
    for page_num in range(1, 20):
        url = f"{base}/collections/pre-owned/products.json?limit=250&page={page_num}"
        try:
            resp = requests.get(url, headers={"User-Agent": random.choice(USER_AGENTS)}, timeout=30)
            resp.raise_for_status()
            products = resp.json().get("products", [])
        except Exception as e:
            raise RuntimeError(f"Leica Store Heidelberg {page_num}페이지 못 읽음: {e}")  # 빠진 쪽이 판매완료로 바뀌지 않게
        if not products:
            break
        print(f"    └─ {page_num}페이지 {len(products)}개 상품 발견")
        for p in products:
            title = (p.get("title") or "").strip()
            if not re.match(r"(?:leica|leitz)\b", title, re.I):
                continue
            variants = p.get("variants") or [{}]
            if not any(v.get("available") for v in variants):
                continue
            link = f"{base}/products/{p['handle']}"
            name = _heidelberg_name(title)
            if any(b2 in name.lower() for b2 in THIRD_PARTY_BRANDS):
                continue
            try:
                price = f"€{float(variants[0].get('price')):,.0f}"
            except (TypeError, ValueError):
                price = "문의요망"
            text = _html.unescape(re.sub(r"<[^>]+>", " ", p.get("body_html") or ""))
            m = re.search(r"Schulnote\s*([1-6](?:\s*[-+]\s*[1-6]?)?)", text)
            if m:
                cond = HEIDELBERG_PREFIX + re.sub(r"\s+", "", m.group(1))
            elif re.search(r"\bDemo", text):
                cond = HEIDELBERG_PREFIX + "Demo"
            else:
                cond = "정보없음"
            img = p["images"][0].get("src", "") if p.get("images") else ""
            cat = detect_category(name, price)
            mount = 'Accessory' if cat == 'Accessory' else detect_mount(name)
            results.append({
                "게시일": _shopify_listed(p),
                "site": "Leica Store Heidelberg (독일)",
                "label": auto_label(name),
                "상품명": name,
                "세대": detect_generation(name),
                "컨디션": cond,
                "가격": price,
                "통화": "EUR",
                "이미지": img,
                "링크": link,
                "품절": False,
                "예약중": False,
                "mount": mount,
                "category": cat,
                "brand": detect_brand(name),
            })
        time.sleep(random.uniform(1.0, 2.0))
    print(f"  ✅ Leica Store Heidelberg 완료: {len(results)}개")
    return results


def _vibe_name(title):
    """Vibe.pl 제목 다듬기: 'Leica 75/2.5 Summarit-M 6-Bit (11645)' → 'Leica Summarit-M 75mm f2.5 6-Bit (11645)'.
    '초점/조리개 이름' 순서를 '이름 초점mm f조리개'로, 폴란드어 앞말(Obiektyw·Aparat cyfrowy)·'używany'·색 이름 정리"""
    import html as _html
    name = re.sub(r"\s+", " ", _html.unescape(title)).strip()
    name = re.sub(r"^(?:Obiektyw|Aparat(?: cyfrowy| analogowy)?)\s+", "", name, flags=re.I)
    name = re.sub(r"\s*[–-]\s*(?:UŻYWANE|Aparat\b.*)$", "", name, flags=re.I)
    name = re.sub(r"\s+(?:używany|Aparat Analogowy Dalmierz)\b.*$", "", name, flags=re.I)
    name = re.sub(r"\b(\d{2,3}(?:-\d{2,3})?)/(\d+(?:\.\d+)?)\s+((?:APO-|Macro-|Vario-|Super-)*(?:Summilux|Summicron|Summarit|Summaron|Elmarit|Elmar|Noctilux|Tele-Elmarit|Tele-Elmar|Super-Angulon|Telyt)(?:-[A-Z]+)?)",
                  lambda m: f"{m.group(3)} {m.group(1)}mm f{m.group(2)}" + ("" if "." in m.group(2) else ".0"), name)
    name = re.sub(r"\b(\d{2,3})/(\d+(?:\.\d+)?)\b", lambda m: f"{m.group(1)}mm f{m.group(2)}" + ("" if "." in m.group(2) else ".0"), name)
    name = re.sub(r"\b(\d{2,3})mm f(\d+(?:\.\d+)?)\b", lambda m: f"{m.group(1)}mm f{m.group(2)}" + ("" if "." in m.group(2) else ".0"), name)
    name = re.sub(r"Macro-Elmarit-R (100mm f4\.0)", r"Macro-Elmar-R \1", name)  # 100/4는 Macro-Elmar (매장 오타)
    name = re.sub(r"\s+ver\.?\s?(\d)\b", r" Version \1", name, flags=re.I)
    name = re.sub(r"\bCzarn[ya]\b", "black", name, flags=re.I)
    name = re.sub(r"\bSrebrn[ya]\b", "silver", name, flags=re.I)
    name = re.sub(r"\s+", " ", name).strip(" ,-–")
    if re.match(r"Leica (?:M\d*|MP|CL|Q\d?|SL\d?(?:-S)?|R\d)(?: \((?:Typ|TYP) \d+\))?(?: (?:black|silver|body))*$", name, re.I):
        name = re.sub(r"\s+body$", "", name, flags=re.I) + " Body"
    return name


def crawl_vibe():
    """Vibe.pl (폴란드, 크라쿠프 InterFoto 매장 온라인) - WooCommerce. 공개 상품 API(/wp-json/wc/store/v1/products?search=leica)
    한 번에 100개씩. 신품·중고·대여(Rent-to-Own)가 섞여 있어 중고만: 설명에 'Stan zużycia: 5·4·3…'(매장 등급)이 있거나
    중고 보증 'Gwarancja: 3'(3개월)이거나 제목에 'UŻYWANE'. Panasonic Leica DG·Sigma·Voigtländer 등은 뺌. 재고 있는 것만"""
    import html as _html
    import requests
    from condition_grade import VIBE_PREFIX
    base = "https://vibe.pl"
    sess = requests.Session()
    sess.headers["User-Agent"] = random.choice(USER_AGENTS)
    print("\n  📂 Vibe.pl 크롤링 시작")
    results, seen = [], set()
    for page_num in range(1, 20):
        url = f"{base}/wp-json/wc/store/v1/products?search=leica&per_page=100&page={page_num}"
        try:
            try:
                resp = sess.get(url, timeout=60)
                resp.raise_for_status()
            except Exception as e:  # 미국 서버(GitHub)에서는 403 → 도쿄 중계 서버
                import crawl_engine as _ce
                print(f"    ↪ 직접 접속 실패({e}) → 중계 서버")
                resp = _ce.http_get(url, {"Accept": "application/json"}, via_relay=True, timeout=50)
                resp.raise_for_status()
            products = resp.json()
        except Exception as e:
            raise RuntimeError(f"Vibe.pl {page_num}쪽 못 읽음: {e}")  # 빠진 쪽이 판매완료로 바뀌지 않게
        if not products:
            break
        print(f"    └─ {page_num}페이지 {len(products)}개")
        for p in products:
            title = _html.unescape(p.get("name") or "")
            if not re.match(r"(?:Obiektyw |Aparat (?:cyfrowy |analogowy )?)?(?:Leica|Leitz)\b", title, re.I):
                continue
            link = p.get("permalink") or ""
            if not p.get("is_in_stock") or link in seen:
                continue
            seen.add(link)
            text = _html.unescape(re.sub(r"<[^>]+>", " ", (p.get("short_description") or "") + " " + (p.get("description") or "")))
            stan = re.search(r"Stan zużycia:\s*([0-9]|DEMO|NOWY)\b", text, re.I)
            if stan and stan.group(1).upper() == "NOWY":
                continue
            if not (stan or re.search(r"Gwarancja:\s*3\b", text) or "UŻYWAN" in title.upper()):
                continue  # 신품
            name = _vibe_name(title)
            if any(b2 in name.lower() for b2 in THIRD_PARTY_BRANDS):
                continue
            pr = p.get("prices") or {}
            try:
                amount = int(pr.get("price")) / 10 ** int(pr.get("currency_minor_unit") or 0)
                price = f"{amount:,.0f} zł"
            except (TypeError, ValueError):
                price = "문의요망"
            imgs = p.get("images") or []
            cat = detect_category(name, price)
            mount = 'Accessory' if cat == 'Accessory' else detect_mount(name)
            results.append({
                "site": "Vibe.pl (폴란드)",
                "label": auto_label(name),
                "상품명": name,
                "세대": detect_generation(name),
                "컨디션": VIBE_PREFIX + stan.group(1).upper() if stan else "정보없음",
                "가격": price,
                "통화": "PLN",
                "이미지": imgs[0].get("src", "") if imgs else "",
                "링크": link,
                "품절": False,
                "예약중": False,
                "mount": mount,
                "category": cat,
                "brand": detect_brand(name),
            })
        if len(products) < 100:
            break
        time.sleep(2)
    print(f"  ✅ Vibe.pl 완료: {len(results)}개")
    return results


def _koester_name(title):
    """Foto Köster 제목 다듬기: 제조사 칸이 Leica인데 제목엔 'Leica'가 없어('Summicron M 90/2', 'I g Gehäuse') 앞에 붙이고,
    '90/2'·'1:2,8/90' → '90mm f2.0'·'90mm f2.8', 'Gehäuse' → 'Body', 'III G' → 'IIIg', 'flex' → 'Leicaflex'"""
    import html as _html
    name = re.sub(r"\s+", " ", _html.unescape(title)).strip()
    name = re.sub(r"(\d),(\d)", r"\1.\2", name)
    name = re.sub(r"\s*-\s*defekt\b", " defekt", name, flags=re.I)
    name = re.sub(r"^flex\b", "Leicaflex", name, flags=re.I)
    name = re.sub(r"\s+mit Sucher\b", "", name)
    name = re.sub(r"-M(\d)", r"-M \1", name)  # 'Elmar-M50/2.8'
    for de, en in (("Bereitschaftstasche", "Ever-Ready Case"), ("Gegenlichtblende", "Lens Hood"), ("Einstellschnecke", "Focusing Mount"),
                   ("Sucher", "Viewfinder"), ("Kabel", "Cable"), ("braun", "brown")):
        name = re.sub(rf"\b{de}\b", en, name)
    name = re.sub(r"\bfür\b", "for", name)
    name = re.sub(r"^DRP II m\.\s*", "II (D) Body with ", name)
    name = re.sub(r"^Nah-Summicron-M\b", "Dual Range Summicron-M", name)
    name = re.sub(r"^Elmar (65)/", r"Viso-Elmar \1/", name)
    name = re.sub(r"\b1:(\d+(?:\.\d+)?)/(\d{2,3})\b", r"\2/\1", name)  # '1:2.8/90' → '90/2.8'
    name = re.sub(r"\b(\d{2,3}(?:-\d{2,3})?)/(\d+(?:\.\d+)?)\b",
                  lambda m: f"{m.group(1)}mm f{m.group(2)}" + ("" if "." in m.group(2) else ".0"), name)
    name = re.sub(r"\bf/(\d)", r"f\1", name)
    name = re.sub(r"\b(Summicron|Summilux|Elmarit|Elmar|Summaron) (M|R)\b", r"\1-\2", name)
    name = re.sub(r"\b(I{1,3}) ([A-Ga-g])\b", lambda m: m.group(1) + m.group(2).lower(), name)
    name = re.sub(r"\bI([FG])\b", lambda m: "I" + m.group(1).lower(), name)
    name = re.sub(r"\bGehäuse\b", "Body", name)
    name = re.sub(r"\bmit Sucher\b", "", name)
    name = re.sub(r"\bmit Brille\b", "with Goggles", name)
    name = re.sub(r",?\s*Version EU,?\s*US,?\s*CN", "", name)
    name = re.sub(r"\bschwarz lackiert\b", "black paint", name)
    name = re.sub(r"\bschwarz eloxiert\b", "black anodized", name)
    name = re.sub(r"\bschwarz\b", "black", name)
    name = re.sub(r"\bsilber\b", "silver", name)
    name = re.sub(r"\bM-?39\b", "L39", name)
    name = re.sub(r"\s+", " ", name).strip(" ,-")
    return name if re.match(r"(?:Leica|Leitz)", name, re.I) else "Leica " + name


def _koester_condition(desc):
    """Foto Köster 설명 글의 상태 말투 → 등급 단계 (매장 등급표 없음). 'Lieferumfang und Zustand wie abgebildet'만 있으면 None"""
    d = desc.lower()
    if re.search(r"defekt|nebel|kratzer auf der frontlinse|pilz|fungus", d):
        return "defekt"
    if re.search(r"wie neu|top-zustand|sehr gut", d):
        return "sehr gut"
    if re.search(r"\bgut(?:e[nmr]?)?\b[^.]{0,40}zustand|zustand[^.]{0,20}\bgut", d):
        return "gut"
    return None


def crawl_koester():
    """Foto Köster (독일, 뮌스터) - 사진 매장(Shopware). '중고 기기'(Gebrauchtgeräte) 분류를 제조사 Leica로 거른 목록
    (?manufacturer=…&p=N, 정적 HTML)에 이름·가격·사진. 등급표가 없고 상태는 상세 설명 글에만 있어('sehr guten Zustand mit kaum
    erkennbaren Abnutzungen'·'guten Zustand'·'Nebel') 상세를 함께 읽음 — 40개쯤이라 6시간마다"""
    import html as _html
    import json as _json
    import requests
    from condition_grade import KOESTER_PREFIX
    base = "https://www.foto-koester.de"
    sess = requests.Session()
    sess.headers["User-Agent"] = random.choice(USER_AGENTS)
    print("\n  📂 Foto Köster 크롤링 시작")
    cards = []
    for page_num in range(1, 20):
        try:
            resp = sess.get(f"{base}/gebrauchtgeraete/", params={"manufacturer": "006e484887ba4574a1e5903c2ad7fb04",
                                                                 "limit": 48, "p": page_num}, timeout=40)
            resp.raise_for_status()
        except Exception as e:
            raise RuntimeError(f"Foto Köster {page_num}쪽 못 읽음: {e}")  # 빠진 쪽이 판매완료로 바뀌지 않게
        boxes = resp.text.split('class="card product-box')[1:]
        new = 0
        for blk in boxes:
            info = re.search(r'data-product-information="([^"]+)"', blk)
            link = re.search(r'href="([^"]+)"[^>]*class="product-name', blk) or re.search(r'class="product-name[^"]*"[^>]*href="([^"]+)"', blk)
            if not info or not link or any(c[0] == link.group(1) for c in cards):
                continue
            img = re.search(r'<img[^>]+src="([^"?]+)', blk)
            cards.append((link.group(1), _json.loads(_html.unescape(info.group(1))), img.group(1) if img else ""))
            new += 1
        print(f"    └─ {page_num}페이지 {len(boxes)}개")
        if new == 0 or f"p={page_num + 1}" not in resp.text:
            break
        time.sleep(2)
    results = []
    for link, d, img in cards:
        price = float(d.get("price") or 0)
        if price <= 0:
            continue
        name = _koester_name(d.get("name") or "")
        if any(b2 in name.lower() for b2 in THIRD_PARTY_BRANDS) or re.search(r"Elmaron|Colorplan|Hektor-P|Pradovit", name):
            continue  # 영사기 렌즈는 카메라 매물이 아님
        cond = "정보없음"
        try:
            page = sess.get(link, timeout=30).text
            m = re.search(r'class="product-detail-description-text"[^>]*>(.*?)</div>', page, re.S)
            grade = _koester_condition(_html.unescape(re.sub(r"<[^>]+>", " ", m.group(1))) if m else "")
            if grade:
                cond = KOESTER_PREFIX + grade
        except Exception as e:
            print(f"    ⚠️ 상세 못 읽음 ({link}): {e}")
        time.sleep(1)
        cat = detect_category(name, f"€{int(price):,}")
        mount = 'Accessory' if cat == 'Accessory' else detect_mount(name)
        results.append({
            "site": "Foto Köster (독일)",
            "label": auto_label(name),
            "상품명": name,
            "세대": detect_generation(name),
            "컨디션": cond,
            "가격": f"€{int(round(price)):,}",
            "통화": "EUR",
            "이미지": img,
            "링크": link,
            "품절": False,
            "예약중": False,
            "mount": mount,
            "category": cat,
            "brand": detect_brand(name),
        })
    print(f"  ✅ Foto Köster 완료: {len(results)}개")
    return results



def _lecuit_name(title):
    """Lecuit 제목 다듬기: 'Occasion • Leica Summicron-M 1:2/28mm ASPH. (2000-2016)' → 'Leica Summicron-M 28mm f2.0 ASPH.'.
    앞의 'Occasion •'·뒤의 '• Ex-Display'와 연도 괄호는 떼고, '1:2.8/90'·'2/35mm'·'4/280' 꼴 조리개·초점거리는 '90mm f2.8'로
    (분류기가 '1:2/28mm'를 렌즈로 못 읽음), 프랑스어 'noir'·'argent'·'viseur'는 영어로"""
    name = re.sub(r"^\s*Occasion\s*•\s*", "", title.strip(), flags=re.I)
    name = re.sub(r"\s*•\s*Ex-?Display\s*$", "", name, flags=re.I)
    name = re.sub(r"\s*\((?:19|20)\d{2}\s*-\s*(?:19|20)\d{2}\)", "", name)
    name = re.sub(r"\s*\*.*$", "", name)
    name = name.replace("–", "-")

    def _ap(ap):
        ap = ap.replace(",", ".")
        return ap if ("." in ap or "-" in ap) else ap + ".0"

    def _fl(m):
        return f" {m.group(2)}mm f{_ap(m.group(1))}"
    name = re.sub(r"\s+f\s*1\s*:\s*(\d(?:[.,]\d)?)\s+(\d{2,3})\s*mm\b", r" \1/\2", name, flags=re.I)  # 'f1:2 35mm' → '2/35' (아래에서 '35mm f2.0'로)
    name = re.sub(r"\s+(?:1\s*:\s*|f/?)?(\d(?:[.,]\d)?(?:-\d(?:[.,]\d)?)?)\s*/\s*(\d{2,3}(?:-\d{2,3})*)(?:\s*mm)?\b", _fl, name, flags=re.I)
    name = re.sub(r"\bsac tout pr[êe]t\b", "Ever ready case", name, flags=re.I)
    name = re.sub(r"\bEVF\s?2\b", "Visoflex EVF2", name)  # 'EVF 2 … for Leica M (Typ 240)'가 M240 바디로 붙지 않게
    name = re.sub(r"\bM39\b", "LTM", name)
    name = re.sub(r"\s+(\d{2,3})\s*mm\s+f\s*[/:]?\s*(\d(?:[.,]\d)?)\b", lambda m: f" {m.group(1)}mm f{_ap(m.group(2))}", name, flags=re.I)
    for fr, en in (("pour", "for"), ("noir", "black"), ("argent", "silver"), ("chromé", "chrome"), ("viseur", "Viewfinder"), ("avec lunette", "with goggles")):
        name = re.sub(rf"\b{fr}\b", en, name, flags=re.I)
    return re.sub(r"\s+", " ", name).strip(" ,-")


def crawl_lecuit():
    """Lecuit (룩셈부르크) - 사진·광학 매장(ePages). 'SECONDE MAIN'(중고) 분류를 제조사 Leica Camera로 거른 화면
    (ViewAction=ViewFaceted, 60개씩 ?Page=N, 정적 HTML)에 이름·가격·사진·재고, 등급(A++~D)은 상품 화면 'Etat' 칸에만 있어
    새 매물만 상세를 읽고 아는 매물은 지난 등급을 씀. 전시품('• Ex-Display')도 같은 분류에 있음"""
    import html as _html
    import requests
    from condition_grade import LECUIT_PREFIX
    base = "https://www.lecuit.lu/epages/Lecuit.sf/fr_FR/"
    site = "Lecuit (룩셈부르크)"
    sess = requests.Session()
    sess.headers["User-Agent"] = random.choice(USER_AGENTS)
    known = {}
    try:
        with open("data/raw/results.json", encoding="utf-8") as f:
            known = {r["링크"]: r.get("컨디션") for r in json.load(f) if r.get("site") == site}
    except (OSError, ValueError):
        pass
    print(f"\n  📂 Lecuit 크롤링 시작 (이전 등급 {len(known)}개)")
    cards = []
    for page_num in range(1, 15):
        try:
            resp = sess.get(base, params={"ViewAction": "ViewFaceted", "ObjectID": "3114990", "PageSize": "60",
                                          "FacetValue_CategoryID": "3114990", "CurrencyID": "EUR",
                                          "FacetValue_Manufacturer": "Leica Camera", "Page": page_num}, timeout=40)
            resp.raise_for_status()
        except Exception as e:
            raise RuntimeError(f"Lecuit {page_num}쪽 못 읽음: {e}")  # 빠진 쪽이 판매완료로 바뀌지 않게
        boxes = resp.text.split('class="InfoArea"')[1:]
        new = 0
        for blk in boxes:
            m = re.search(r'<h3[^>]*>\s*<a href="\?ObjectPath=([^"]+)"[^>]*>([^<]+)</a>', blk)
            if not m or any(c[0] == m.group(1) for c in cards):
                continue
            pm = re.search(r"itemprop='price' content='([\d.]+)'", blk)
            img = re.search(r'class="ProductSmallImage" src="([^"]+)"', blk)
            cards.append((m.group(1), _html.unescape(m.group(2)).strip(), float(pm.group(1)) if pm else 0.0,
                          img.group(1).replace("_m.jpg", "_ml.jpg") if img else "", "En stock" in blk))
            new += 1
        print(f"    └─ {page_num}페이지 {len(boxes)}개")
        if new == 0 or f"Page={page_num + 1}" not in resp.text:
            break
        time.sleep(2)
    if not cards:
        raise RuntimeError("Lecuit 목록이 비어 있음")  # 화면이 바뀌었으면 전부 판매완료로 바뀌지 않게
    results = []
    for path, title, price, img, in_stock in cards:
        if price <= 0:
            continue
        name = _lecuit_name(title)
        if any(b2 in name.lower() for b2 in THIRD_PARTY_BRANDS) or re.search(r"Pradovit|Colorplan|Hektor-P|matchTechnical", name, re.I):
            continue  # 영사기 부품·다른 회사 액세서리
        link = f"{base}?ObjectPath={path}"
        if re.search(r"Ex-?Display", title, re.I):
            cond = LECUIT_PREFIX + "Ex-Display"
        elif known.get(link):
            cond = known[link]
        else:
            cond = "정보없음"
            try:
                page = sess.get(base, params={"ObjectPath": path}, timeout=30).text
                em = re.search(r'AttributeLabel[^>]*>\s*Etat\s*</td>\s*<td[^>]*>(.*?)</td>', page, re.S)
                letter = re.match(r"\s*(A\+\+|A\+|A|B|C|D)\b", _html.unescape(re.sub(r"<[^>]+>", " ", em.group(1)))) if em else None
                if letter:
                    cond = LECUIT_PREFIX + letter.group(1)
            except Exception as e:
                print(f"    ⚠️ 상세 못 읽음 ({link}): {e}")
            time.sleep(1)
        cat = detect_category(name, f"€{int(price):,}")
        mount = 'Accessory' if cat == 'Accessory' else detect_mount(name)
        results.append({
            "site": site,
            "label": auto_label(name),
            "상품명": name,
            "세대": detect_generation(name),
            "컨디션": cond,
            "가격": f"€{int(round(price)):,}",
            "통화": "EUR",
            "이미지": ("https://www.lecuit.lu" + img) if img.startswith("/") else img,
            "링크": link,
            "품절": not in_stock,
            "예약중": False,
            "mount": mount,
            "category": cat,
            "brand": detect_brand(name),
        })
    print(f"  ✅ Lecuit 완료: {len(results)}개")
    return results


_OHNUKI_JA = [  # ja_to_en 앞에 바꿀 말 (긴 것 먼저)
    (r"トリプレット", "Triplet "), (r"ライツカナダ", "Leitz Canada "), (r"卓上三脚", "Table tripod "), (r"ベローズ", "Bellows "),
    (r"レリーズ", "Release "), (r"ライカフレックス", "Leicaflex "), (r"ライツミノルタ", "Leitz Minolta "), (r"ミニルックス", "Minilux "),
    (r"ゾフォート", "Sofort "), (r"シャークスキン", "Sharkskin"), (r"セルフ付", "with self-timer"),
    (r"メガネ無し", ""), (r"メガネ付き?", "with goggles"), (r"レプリカ", "Replica"), (r"復刻版", "Replica"),
    (r"(\d)枚玉", r"\1 elements"), (r"ドイツ", "Germany"), (r"0型", "0-Series"),
]


def _ohnuki_name(title):
    """カメラの大貫 제목 다듬기: 'ライカ M6 0.85\u3000243万台' → 'Leica M6 0.85', 'DR ズミクロンM50/2 メガネ無し' → 'DR Summicron-M 50/2'.
    일련번호 대역('243万台')·'[期間限定HP限定商品]'·'【訳あり…】'은 떼고, ja_to_en이 모르는 말(ライカフレックス·ミニルックス 등)은 먼저 바꿈"""
    name = title.replace("\u3000", " ")
    name = re.sub(r"\[[^\]]*限定[^\]]*\]|【[^】]*】|\d+(?:\.\d+)?万台|訳あり\S*", " ", name)
    for ja, en in _OHNUKI_JA:
        name = re.sub(ja, en, name)
    from ja_normalize import ja_to_en
    name = ja_to_en(name)
    name = re.sub(r"\bSH/\d+/\d+\b", "", name)  # 'SH/210/400' 셔터 점검 기록
    name = re.sub(r"(?<=[A-Za-z])-\s+(?=[A-Z])", "-", name)  # 'Super- Vario- Elmar' → 'Super-Vario-Elmar'
    name = re.sub(r"(?<=[A-Za-z])(\d{2,3})/(\d(?:\.\d)?)\b", r" \1/\2", name)  # 'M50/2' → 'M 50/2'
    if not re.match(r"\s*(leica|leitz)", name, re.I):
        name = "Leica " + name.strip()
    return re.sub(r"\s+", " ", name).strip(" ,-")


def crawl_ohnuki():
    """カメラの大貫 (일본, 도쿄 신주쿠) - 중고 카메라점 Shopify. 중고 라이카 컬렉션 4곳(필름 바디·디지털·렌즈·액세서리)의
    products.json에서 판매 중만 (요청 사이 4~5초 — 빠르면 429). 등급은 설명 표의 '● ランク C+' (B~E, 매장이 엄격해 C가 보통 중고)"""
    import html as _html
    import requests
    from condition_grade import OHNUKI_PREFIX
    base = "https://www.camera-ohnuki.com"
    site = "カメラの大貫 (일본)"
    sess = requests.Session()
    sess.headers["User-Agent"] = random.choice(USER_AGENTS)
    print(f"\n  📂 カメラの大貫 크롤링 시작")
    results, seen = [], set()
    for col in ("used-leica", "used-leica-digital-camera", "used-leica-lenses", "used-leica-accessories"):
        for page_num in range(1, 10):
            try:
                for wait in (20, 40, 0):  # 빠르게 읽으면 429
                    resp = sess.get(f"{base}/collections/{col}/products.json", params={"limit": 250, "page": page_num}, timeout=30)
                    if resp.status_code != 429 or not wait:
                        break
                    time.sleep(wait)
                resp.raise_for_status()
                products = resp.json().get("products", [])
            except Exception as e:
                raise RuntimeError(f"大貫 {col} {page_num}쪽 못 읽음: {e}")  # 빠진 쪽이 판매완료로 바뀌지 않게
            if not products:
                break
            print(f"    └─ {col} {page_num}페이지 {len(products)}개")
            for p in products:
                if p["id"] in seen:
                    continue
                seen.add(p["id"])
                variants = p.get("variants") or [{}]
                if not any(v.get("available") for v in variants):
                    continue
                title = _html.unescape(p.get("title") or "")
                if re.search(r"フォクトレンダー|ノクトン|テーラーホブソン|ツァイス|キヤノン|ニコン|コシナ|七工匠|銘匠", title):
                    continue  # 다른 회사 렌즈
                text = _html.unescape(re.sub(r"<[^>]+>", " ", p.get("body_html") or ""))
                m = re.search(r"ランク\s*([A-E][+\-]?)", text)
                cond = OHNUKI_PREFIX + m.group(1) if m else "정보없음"
                name = _ohnuki_name(title)
                try:
                    price = f"¥{float(variants[0].get('price')):,.0f}"
                except (TypeError, ValueError):
                    continue
                img = p["images"][0].get("src", "") if p.get("images") else ""
                cat = detect_category(name, price)
                mount = 'Accessory' if cat == 'Accessory' else detect_mount(name)
                results.append({
                    "게시일": _shopify_listed(p),
                    "site": site,
                    "label": auto_label(name),
                    "상품명": name,
                    "세대": detect_generation(name),
                    "컨디션": cond,
                    "가격": price,
                    "통화": "JPY",
                    "이미지": img,
                    "링크": f"{base}/products/{p['handle']}",
                    "품절": False,
                    "예약중": False,
                    "mount": mount,
                    "category": cat,
                    "brand": detect_brand(name),
                })
            if len(products) < 250:
                break
            time.sleep(random.uniform(4.0, 5.0))
        time.sleep(random.uniform(4.0, 5.0))
    print(f"  ✅ カメラの大貫 완료: {len(results)}개")
    return results


_KIKUYA_LENS = r"SUMMILUX|SUMMICRON|SUMMARIT|SUMMITAR|SUMMARON|SUMMAR|NOCTILUX|ELMARIT|ELMAR|HEKTOR|TELYT|ANGULON"
_KIKUYA_FOCAL = r"(\d+(?:\.\d+)?)\s?(mm|cm)\s?f\s?(\d+(?:\.\d+)?)"


def _kikuya_name(parts):
    """喜久屋カメラ 제목 다듬기: 줄(<br>)마다 일본어·영어가 따로 있어 영어 줄만 이어 쓰고, 일본어 줄의 초점거리를 붙임.
    ['ライカM', 'ズミルックス', '35mmf1.4', 'LEICA M SUMMILUX', '2nd'] → 'Leica SUMMILUX-M 35mm f1.4 2nd',
    ['ライカL', '沈胴ズミクロン5cmf2.0', 'LEICA SUMMICRON'] → 'Leica SUMMICRON 50mm f2.0 collapsible L39'"""
    import unicodedata
    ja = [unicodedata.normalize("NFKC", p) for p in parts]
    en = [p for p in ja if re.fullmatch(r"[\x20-\x7e]+", p) and re.search(r"[A-Za-z]", p)
          and not re.fullmatch(_KIKUYA_FOCAL + r"|No\.\s?\d+", p, re.I)]  # '35mmf1.4'·'No.843414' 줄은 뺌
    name = " ".join(en)
    m = re.match(r"(.+?)\s+(LEICA|LEITZ)\b(.*)", name)
    if m and not re.search(r"\b(?:LEICA|LEITZ)\b", m.group(1)):  # 'SLOOZ LEICA 28mm…' → 'LEICA SLOOZ 28mm…'
        name = f"{m.group(2)} {m.group(1)}{m.group(3)}"
    name = re.sub(r"\bVEIW\b", "VIEW", name)
    name = re.sub(r"\b(I{1,3})([A-G])\b", lambda m: m.group(1) + m.group(2).lower(), name)  # 'IIIC' → 'IIIc'
    name = re.sub(r"\bLEICA (?:M|L) (?=" + _KIKUYA_LENS + r")", "LEICA ", name)
    m_mount = any(re.match(r"ライカM(?!用|\d|L)", p) for p in ja)
    l_mount = any(re.match(r"ライカL(?!用)", p) for p in ja)
    lens = re.search(r"\b(" + _KIKUYA_LENS + r")\b(-M)?", name)
    fm = next((m for m in (re.search(_KIKUYA_FOCAL, p, re.I) for p in ja) if m), None)
    if lens:
        word = lens.group(1) + ("-M" if m_mount or lens.group(2) else "")
        focal = ""
        if fm and not re.search(r"\d\s?(?:mm|cm)\b", name, re.I):
            mm = float(fm.group(1)) * (10 if fm.group(2).lower() == "cm" else 1)
            focal = f" {mm:g}mm f{fm.group(3)}"
        name = name[:lens.start()] + word + focal + name[lens.end():]
        if any("沈胴" in p for p in ja):
            name += " collapsible"
        if l_mount and not m_mount:
            name += " L39"
    elif re.search(r"\b(?:M[1-7]|I{1,3}[a-g]?|MINOLTA CL)\b", name) and not re.search(r"ROKKOR|FINDER|HOOD|FILTER", name):
        name += " Body"
    name = re.sub(r"^LEICA\b", "Leica", name)
    name = re.sub(r"^LEITZ\b", "Leitz", name)
    name = re.sub(r"\bCL M-ROKKOR (\d+)mm\s?f", r"CL Body + M-ROKKOR \1mm f", name)  # 바디·렌즈 세트
    name = re.sub(r"\b(\S{4,}) \1\b", r"\1", name)  # 'NOOKY-HESUM NOOKY-HESUM'
    return re.sub(r"\s+", " ", name).strip(" /,-")


def crawl_kikuya():
    """喜久屋カメラ＆ウォッチ (일본, 도쿄) - 중고 카메라점(카라미숍 Color Me, EUC-JP). '中古ライカ販売' 분류(cbid=1729227)
    정적 HTML 한 쪽에 다 나옴(63점 안팎). 이름은 줄마다 일본어·영어, 설명 끝 'AB'·'A-'가 등급.
    다른 회사 렌즈(ライカL用 キャノン 등)·비순정 부품·책은 영어 줄에 LEICA/LEITZ가 없어 빠짐. 'SOLD OUT'은 뺌"""
    import html as _html
    import unicodedata
    import requests
    from condition_grade import KIKUYA_PREFIX
    base = "https://kikuya-camera.shop-pro.jp"
    site = "喜久屋カメラ (일본)"
    sess = requests.Session()
    sess.headers["User-Agent"] = random.choice(USER_AGENTS)
    print("\n  📂 喜久屋カメラ 크롤링 시작")
    try:
        resp = sess.get(base + "/", params={"mode": "cate", "cbid": "1729227", "csid": "0", "sort": "n"}, timeout=30)
        resp.raise_for_status()
    except Exception as e:
        raise RuntimeError(f"喜久屋カメラ 목록 못 읽음: {e}")  # 빈 목록이 판매완료로 바뀌지 않게
    text = resp.content.decode("euc-jp", "ignore")
    boxes = re.findall(r'<div class="item_box[^"]*">(.*?)</div>\s*</div>', text, re.S)
    if not boxes:
        raise RuntimeError("喜久屋カメラ 목록에 상품 없음 (화면 바뀜?)")
    print(f"    └─ 목록 {len(boxes)}개")
    results, seen = [], set()
    for b in boxes:
        pid = re.search(r"\?pid=(\d+)", b)
        nm = re.search(r'class="item_name">\s*<a[^>]*>(.*?)</a>', b, re.S)
        if not pid or not nm or pid.group(1) in seen or "SOLD OUT" in b:
            continue
        seen.add(pid.group(1))
        parts = [_html.unescape(re.sub(r"<[^>]+>", "", p)).strip() for p in re.split(r"<br\s*/?>", nm.group(1))]
        parts = [p for p in parts if p and not re.match(r"^\([^)]*\)", p) and "商談中" not in p and "様専用" not in p]
        if "非純正" in " ".join(parts):
            continue
        name = _kikuya_name(parts)
        if not re.search(r"\b(?:LEICA|LEITZ)\b", name, re.I) or any(b2 in name.lower() for b2 in THIRD_PARTY_BRANDS):
            continue
        pm = re.search(r'class="item_price">\s*([\d,]+)円', b)
        price = f"¥{int(pm.group(1).replace(',', '')):,}" if pm else "문의요망"
        dm = re.search(r'class="item_description">(.*?)</p>', b, re.S)
        desc = unicodedata.normalize("NFKC", re.sub(r"<[^>]+>", " ", dm.group(1))).replace("ー", "-").strip() if dm else ""
        gm = re.search(r"\b(AA|AB|A\+|A-|A|B\+|B-|BC|B|C)$", desc)
        img = re.search(r'<img src="([^"]+)"', b)
        cat = detect_category(name, price)
        if cat == "Lens" and not re.search(_KIKUYA_LENS + r"|ROKKOR", name):
            cat = "Accessory"  # 'SHUTTER BUTTON' 등 비싼 부품이 렌즈로 잡히지 않게
        mount = 'Accessory' if cat == 'Accessory' else detect_mount(name)
        results.append({
            "site": site,
            "label": auto_label(name),
            "상품명": name,
            "세대": detect_generation(name),
            "컨디션": KIKUYA_PREFIX + gm.group(1) if gm else "정보없음",
            "가격": price,
            "통화": "JPY",
            "이미지": img.group(1).replace("_th.jpg", ".jpg") if img else "",
            "링크": f"{base}/?pid={pid.group(1)}",
            "품절": False,
            "예약중": False,
            "mount": mount,
            "category": cat,
            "brand": detect_brand(name),
        })
    print(f"  ✅ 喜久屋カメラ 완료: {len(results)}개")
    return results


_KASAN_OTHER = r"미야자키|miyazaki|ms-?optics|주비터|jupiter|linhof|린호프|user made|보이그|voigt|라이트\s|light\s?lens|코니카|konica|마이어|meyer|핸드크로스|handcross|캐논|canon|니콘|nikon|zeiss|자이스|미놀타|minolta|아티산|artisan|ttartisan|7artisans"


def _kasan_name(title):
    """가산카메라 제목 다듬기: '라이카 Leica SUMMILUX M50mm F1.4 블랙 (12586 후드포함)/95%' → 'Leica SUMMILUX M 50mm f1.4 black'.
    끝의 상태 '/95%'·'[98%]'와 괄호 속 구성품·일련번호('no3498***')는 떼고, 앞의 한글 '라이카'·'라이카 필터' 같은 말은 뺌"""
    name = re.sub(r"\s*/?\s*\[?\s*\d{2,3}\s?%\s*\]?\s*$", "", title.strip())
    name = re.sub(r"\s*\[\s*\d{2,3}\s*\]\s*$", "", name)
    name = re.sub(r"^\s*판매완료\s*", "", name)
    name = re.sub(r"^(?:라이카|바르낙)(?:\s+(?:필터|후드|뷰파인더|바르낙))*\s+", "", name)
    name = re.sub(r"\.?\s*(?:렌즈)?광학부?\s*상태\S*|\s*상태\s?좋음", "", name)
    name = re.sub(r"\s*\([^)]*(?:포함|세트|셋트|케이스|정품|후드|필타|박스|캡|스트랩|스트렙)[^)]*\)", "", name)
    name = re.sub(r"\s*(?:\.?\s*no\.?\s?\d{3,}\**|\.no\d+\**)", "", name, flags=re.I)
    name = re.sub(r"[.+,]?\s*(?:UV)?(?:후드|필타|변환링|정품)\S*|\s*/\s*\(\d{4}년생산\)|\s*버전\s?\d", "", name)
    name = re.sub(r"(?:f\s?=\s?)?(\d{1,2}(?:\.\d)?)\s?cm(?=\b|[A-Zf])", lambda m: f" {round(float(m.group(1)) * 10)}mm ", name)  # 'f=5cm' → '50mm'
    name = re.sub(r"\s?[fF]\s?1\s?:\s?(\d(?:\.\d)?)", r" f\1", name)  # 'f1:2'·'F1:3.5' → 'f2'
    name = re.sub(r"\s+-\s+(?=[A-Z]\b)", "-", name)  # 'SUMMICRON - L' → 'SUMMICRON-L'
    name = re.sub(r"\bv\.(\d)\b", r"v\1", name)
    name = re.sub(r"\b(M|R)(\d{2,3})mm", r"\1 \2mm", name)  # 'M50mm' → 'M 50mm'
    name = re.sub(r"\bF\s?(\d(?:\.\d)?)\b", r"f\1", name)
    name = re.sub(r"(?<=mm)\s?1\s?:\s?(\d(?:\.\d)?)\b|\s1\s?:\s?(\d(?:\.\d)?)\b", lambda m: " f" + (m.group(1) or m.group(2)), name)
    name = re.sub(r"(?<=[A-Za-z])-\s+(?=[A-Z])", "-", name)  # 'Vario- Elmar' → 'Vario-Elmar'
    if re.search(r"black paint", name, re.I):
        name = name.replace("블랙페인트", "")
    for ko, en in (("블랙페인트", "Black Paint"), ("블랙", "black"), ("실버", "silver"), ("박스세트|박스셋트|박스풀셋트", ""),
                   ("미사용신품|미사용", "unused"), ("오버홀완료", "serviced"), ("호환후드", ""), ("마운트", " mount")):
        name = re.sub(ko, en, name)
    if not re.match(r"\s*(leica|leitz|ernst)", name, re.I):
        name = "Leica " + name.strip()
    return re.sub(r"\s+", " ", name).strip(" ,-./")


def crawl_kasan():
    """가산카메라 (한국) - 빈티지·필름 카메라점(고도몰). 라이카 '중고제품' 분류(cateCd=014004, 20개씩 page=N, 정적 HTML)에
    이름·가격·사진, 품절은 <li class="item_soldout">. 상태는 제목 끝 '/95%' (국내 % 대응 그대로)"""
    import html as _html
    import requests
    base = "https://www.kasancamera.co.kr"
    site = "가산카메라"
    sess = requests.Session()
    sess.headers["User-Agent"] = random.choice(USER_AGENTS)
    print("\n  📂 가산카메라 크롤링 시작")
    results, seen = [], set()
    for page_num in range(1, 40):
        try:
            resp = sess.get(f"{base}/goods/goods_list.php", params={"cateCd": "014004", "page": page_num}, timeout=30)
            resp.raise_for_status()
        except Exception as e:
            raise RuntimeError(f"가산카메라 {page_num}쪽 못 읽음: {e}")  # 빠진 쪽이 판매완료로 바뀌지 않게
        items = re.findall(r'<li\s+(?:class="([^"]*)"\s+)?style="width:[^"]*">\s*<div class="item_cont">(.*?)<!-- //item_cont -->', resp.text, re.S)
        new = 0
        for cls, blk in items:
            g = re.search(r"goodsNo=(\d+)", blk)
            nm = re.search(r'class="item_name">([^<]*)<', blk)
            if not g or not nm or g.group(1) in seen:
                continue
            seen.add(g.group(1))
            new += 1
            title = _html.unescape(nm.group(1)).strip()
            if re.search(_KASAN_OTHER, title, re.I) or any(b2 in title.lower() for b2 in THIRD_PARTY_BRANDS):
                continue
            pm = re.search(r'class="item_price">(.*?)</strong>', blk, re.S)
            ptxt = re.sub(r"<[^>]+>", "", pm.group(1)) if pm else ""
            digits = re.sub(r"[^\d]", "", ptxt)
            sold = "item_soldout" in (cls or "") or "판매완료" in ptxt or title.startswith("판매완료")
            price = f"{int(digits):,}원" if digits else "문의요망"
            pc = re.search(r"(\d{2,3})\s?%\s*\]?\s*$", title) or re.search(r"\[\s*(\d{2,3})\s*\]\s*$", title)
            cond = f"{pc.group(1)}%" if pc else "정보없음"
            name = _kasan_name(title)
            img = re.search(r'<img\s+src="([^"]+)"', blk)
            cat = detect_category(name, price)
            mount = 'Accessory' if cat == 'Accessory' else detect_mount(name)
            results.append({
                "site": site,
                "label": auto_label(name),
                "상품명": name,
                "세대": detect_generation(name),
                "컨디션": cond,
                "가격": price,
                "통화": "KRW",
                "이미지": img.group(1) if img else "",
                "링크": f"{base}/goods/goods_view.php?goodsNo={g.group(1)}",
                "품절": sold,
                "예약중": False,
                "mount": mount,
                "category": cat,
                "brand": detect_brand(name),
            })
        print(f"    └─ {page_num}페이지 {len(items)}개")
        if new == 0:
            break
        time.sleep(1.5)
    if not results:
        raise RuntimeError("가산카메라 목록이 비어 있음")
    print(f"  ✅ 가산카메라 완료: {len(results)}개")
    return results

def _kcamera_name(title):
    """K-Camera 제목 다듬기: _kasan_name 앞에 '/95%/판매완료' 꼬리, 'Rangefinder Film Camera'('finder'라 액세서리로 갈림)·
    'Film Camera'·'Digital', 바디에 딸린 '.스트렙'·'케이스,스트랩'·'호환충전기'·'(그립.컷수…)', '라이카 코리아정품'을 뗌"""
    t = re.sub(r"\s*/\s*판매완료\s*$", "", title.strip())
    t = re.sub(r"\s*(?:Rangefinder\s+)?(?:Film|Digital)\s+Camera\S*|\bRangefinder\b|(?<=Body)\s+Digital\b", " ", t, flags=re.I)
    t = re.sub(r"\s*라이카\s?코리아\s?정품|\s*코리아정품", " ", t)
    t = re.sub(r"\s*\([^)]*(?:그립|컷수|밧데리|배터리)[^)]*\)", " ", t)
    if re.search(r"\bbody\b|\b(?:M\d{1,2}|X1|X2|C2|R\d)\b", t, re.I):
        t = re.sub(r"[.,]?\s*(?:호환충전기|케이스|스트렙|스트랩)(?:[.,]\s*(?:케이스|스트렙|스트랩))*", " ", t)
    t = re.sub(r"\s*[.,]\s*(?:케이스|스트렙|스트랩)\s*(?=/|$)", " ", t)
    t = re.sub(r"\s*\.?\s*컷수\s?[\d,]+|x{3,}|\(\s*\)", " ", t)
    t = re.sub(r"\bBlackr\b", "Black", t)
    t = re.sub(r"\bBody(?=silver|black)", "Body ", t, flags=re.I)
    t = re.sub(r"\b(silver|black)\s+\1\b", r"\1", t, flags=re.I)
    t = re.sub(r"\(L-?\s*mount\s+L39\s+Visoflex용\)", "Visoflex", t, flags=re.I)
    return _kasan_name(t)


def crawl_kcamera():
    """K-Camera (한국) - 남대문·충무로 라이카·필름 카메라점(고도몰). 라이카 '중고제품 / USED' 분류(cateCd=001002, 20개씩 page=N,
    정적 HTML, 8쪽 160점 안팎)에 이름·가격·사진, 품절은 <li class="item_soldout">. 제목 꼴이 가산카메라와 같아
    ('라이카 Leica … /98%') 이름 다듬기는 _kasan_name, 상태는 제목 끝 '/98%' (국내 % 대응 그대로). robots.txt 'Allow: /'"""
    import html as _html
    import requests
    base = "https://www.kcamera.co.kr"
    site = "K-Camera"
    sess = requests.Session()
    sess.headers["User-Agent"] = random.choice(USER_AGENTS)
    print("\n  📂 K-Camera 크롤링 시작")
    results, seen = [], set()
    for page_num in range(1, 40):
        try:
            resp = sess.get(f"{base}/goods/goods_list.php", params={"cateCd": "001002", "page": page_num}, timeout=30)
            resp.raise_for_status()
        except Exception as e:
            raise RuntimeError(f"K-Camera {page_num}쪽 못 읽음: {e}")  # 빠진 쪽이 판매완료로 바뀌지 않게
        items = re.findall(r'<li\s+(?:class="([^"]*)"\s+)?style="width:[^"]*">\s*<div class="item_cont">(.*?)<!-- //item_cont -->', resp.text, re.S)
        new = 0
        for cls, blk in items:
            g = re.search(r"goodsNo=(\d+)", blk)
            nm = re.search(r'class="item_name">([^<]*)<', blk)
            if not g or not nm or g.group(1) in seen:
                continue
            seen.add(g.group(1))
            new += 1
            title = _html.unescape(nm.group(1)).strip()
            if re.search(_KASAN_OTHER, title, re.I) or any(b2 in title.lower() for b2 in THIRD_PARTY_BRANDS):
                continue
            pm = re.search(r'class="item_price">(.*?)</strong>', blk, re.S)
            ptxt = re.sub(r"<[^>]+>", "", pm.group(1)) if pm else ""
            digits = re.sub(r"[^\d]", "", ptxt)
            sold = "item_soldout" in (cls or "") or "판매완료" in ptxt or "판매완료" in title  # 제목 끝 '/95%/판매완료'도 있음
            price = f"{int(digits):,}원" if digits else "문의요망"
            pc = re.search(r"(\d{2,3})\s?%\s*\]?\s*(?:/\s*판매완료\s*)?$", title)
            cond = f"{pc.group(1)}%" if pc else "정보없음"
            name = _kcamera_name(title)
            img = re.search(r'<img\s+src="([^"]+)"', blk)
            cat = detect_category(name, price)
            mount = 'Accessory' if cat == 'Accessory' else detect_mount(name)
            results.append({
                "site": site,
                "label": auto_label(name),
                "상품명": name,
                "세대": detect_generation(name),
                "컨디션": cond,
                "가격": price,
                "통화": "KRW",
                "이미지": img.group(1) if img else "",
                "링크": f"{base}/goods/goods_view.php?goodsNo={g.group(1)}",
                "품절": sold,
                "예약중": False,
                "mount": mount,
                "category": cat,
                "brand": detect_brand(name),
            })
        print(f"    └─ {page_num}페이지 {len(items)}개")
        if new == 0:
            break
        time.sleep(1.5)
    if not results:
        raise RuntimeError("K-Camera 목록이 비어 있음")
    print(f"  ✅ K-Camera 완료: {len(results)}개")
    return results

def _cameraelectronic_name(title):
    """Camera Electronic 제목 다듬기: 'Pre-Owned Leica M6 TTL .85 Silver Body Model 10466 With Box, Body, Cap, Strap SN: 2496525
    (Second Hand)' → 'Leica M6 TTL .85 Silver Body Model 10466'. 딸린 물건 목록('With …'·'in Box'·'Boxed …')과 연도·일련번호는
    떼고(그대로면 case·strap·charger 때문에 액세서리로 갈림), 'Digital Camera'·'Film Camera' 같은 말은 Body로"""
    name = re.sub(r"^pre[\s-]?owned\s+", "", title.strip(), flags=re.I)
    name = re.sub(r"\s*\(second hand\)\s*", " ", name, flags=re.I)
    name = re.sub(r"\s+(?:with\b|w/|in box\b|boxed\b|year \d{4}\b|sn[:\s]|serviced\b|made in\b|-\s*3 cam|,\s*mint\b|mint\b|like new\b).*$",
                  "", name, flags=re.I)
    name = re.sub(r"\b(?:mirrorless\s+|compact\s+|slr\s+|film\s+|rangefinder\s+)*(?:digital\s+)?(?:compact\s+)?camera(?:\s+body)?\b",
                  "Body", name, flags=re.I)
    name = re.sub(r"\bBody\s+Body\b", "Body", name)
    name = re.sub(r"\bSummalux\b", "Summilux", name)
    name = re.sub(r"\b(APO)[ -](Summicron|Summilux|Elmarit|Telyt)[ -](SL|M|R|TL)\b", r"\1-\2-\3", name, flags=re.I)  # 'APO-Summicron SL'
    name = re.sub(r"\b(Vario-Elmar|Super-Vario-Elmar|APO-Vario-Elmar)[ ](TL|SL|R)\b", r"\1-\2", name, flags=re.I)
    name = re.sub(r"\b[fF]/\s?(\d)", r"f\1", name)  # 'f/4.5' → 'f4.5' (_has_aperture가 'f4.5' 꼴만 읽음)
    name = re.sub(r"\bf(\d)(?![\d.])", r"f\1.0", name)  # 정수 조리개 'f2' → 'f2.0'
    name = re.sub(r"\s*\.$", "", name)
    return re.sub(r"\s+", " ", name).strip(" ,-")


_MF_GRADE_RE = re.compile(r"\b(Like New Minus|Like New|Open Box|Mint|Excellent Plus|Excellent|Very Good|Good)\b", re.I)


def _mf_option_grade(p):
    """상품 옵션 'Product Condition'의 값('Excellent Plus-CLA'd' 등, 판매 중인 옵션 먼저) → 등급 매치 (2026-11-02)"""
    variants = p.get("variants") or []
    for i, opt in enumerate(p.get("options") or []):
        if "condition" in str(opt.get("name") or "").lower():
            vals = [v.get(f"option{i + 1}") for v in variants if v.get("available")] + [v.get(f"option{i + 1}") for v in variants]
            for val in vals:
                m = _MF_GRADE_RE.match(str(val or ""))
                if m:
                    return m
    return None


def crawl_mfcamera():
    """MF Camera (미국) - 캘리포니아 폴섬 중고점 Shopify products.json 전체(350개쯤)에서 라이카·라이츠 중고만.
    신품이 섞여 있어 태그에 Used·Pre-Owned·As Is·CLA가 있거나 제목에 상태 말이 있는 것만 담고, 'New' 태그만 있거나
    설명에 'Brand New'인 것은 뺌. 등급은 제목 끝 '– Excellent Plus' 또는 설명의 'Condition: Excellent'"""
    import html as _html
    import requests
    from condition_grade import MFCAMERA_PREFIX
    results = []
    base = "https://www.mfcamera.com"
    print(f"\n  📂 MF Camera 크롤링 시작")
    for page_num in range(1, 20):
        url = f"{base}/products.json?limit=250&page={page_num}"
        try:
            resp = requests.get(url, headers={"User-Agent": USER_AGENTS[1]}, timeout=30)
            resp.raise_for_status()
            products = resp.json().get("products", [])
        except Exception as e:
            raise RuntimeError(f"MF Camera {page_num}페이지 못 읽음: {e}")  # 빠진 쪽이 판매완료로 바뀌지 않게
        if not products:
            break
        print(f"    └─ {page_num}페이지 {len(products)}개 상품 발견")
        for p in products:
            title = re.sub(r"\s+", " ", _html.unescape(p.get("title") or "")).strip()
            if not re.match(r"(?:leica|leitz)\b", title, re.I):
                continue
            variants = p.get("variants") or [{}]
            if not any(v.get("available") for v in variants):
                continue
            tags = " ".join(p.get("tags") or []).lower()
            text = re.sub(r"\s+", " ", _html.unescape(re.sub(r"<[^>]+>", " ", p.get("body_html") or "")))
            used = re.search(r"used|pre-owned|as is|\bcla\b", tags) or _MF_GRADE_RE.search(title)
            if not used or re.search(r"brand new|\bsealed\b", text, re.I) or re.search(r"pre-? ?order", title, re.I):
                continue
            m = _MF_GRADE_RE.search(re.split(r"\s+[\u2013\u2014-]\s+", title, maxsplit=1)[-1]) if re.search(r"\s[\u2013\u2014-]\s", title) else None
            m = m or re.search(r"(?:Condition|Cosmetic(?: Condition)?)\s*[:\-\u2013]\s*(Like New Minus|Like New|Open Box|Mint|Excellent Plus|Excellent|Very Good|Good)\b", text, re.I)
            m = m or _mf_option_grade(p)
            cond = MFCAMERA_PREFIX + m.group(1).title() if m else "정보없음"
            name = re.split(r"\s+[\u2013\u2014|]\s+|\s+-\s+(?=[A-Z][a-z])", title, maxsplit=1)[0]
            name = re.sub(r"\s+Used(?:\s+(?:Like New Minus|Like New|Excellent Plus|Excellent|Very Good|Good))?\b|\s*\(Used\)", "", name, flags=re.I)
            name = re.sub(r"\s*(?:MFR|MFG|MPN)?\s*#\s?\d+\b|\s*\(\d{5}\)|\s+\d{5}$", "", name)
            name = re.sub(r"\b(?:Digital |Film |Mirrorless |35mm )*(?:Rangefinder )?(?:Camera|Lens)\b(?: Body(?: Only)?)?|\s+Rangefinder\b|\s*\(\s*\)|\bManual Focus\b", "", name, flags=re.I)
            name = re.sub(r"\bf/(\d)", r"f\1", name)
            name = re.sub(r"\s+", " ", name).strip(" ,-")
            link = f"{base}/products/{p['handle']}"
            try:
                price = f"${float(variants[0].get('price')):,.0f}"
            except (TypeError, ValueError):
                price = "문의요망"
            img = p["images"][0].get("src", "") if p.get("images") else ""
            cat = detect_category(name, price)
            mount = 'Accessory' if cat == 'Accessory' else detect_mount(name)
            results.append({
                "게시일": _shopify_listed(p),
                "site": "MF Camera (미국)",
                "label": auto_label(name),
                "상품명": name,
                "세대": detect_generation(name),
                "컨디션": cond,
                "가격": price,
                "통화": "USD",
                "이미지": img,
                "링크": link,
                "품절": False,
                "예약중": False,
                "mount": mount,
                "category": cat,
                "brand": detect_brand(name),
            })
        time.sleep(random.uniform(1.0, 2.0))
    print(f"  ✅ MF Camera 완료: {len(results)}개")
    return results


_CC_GRADE_ORDER = ["LN", "MINT", "MINT-", "NEAR MINT", "EX++", "EX+", "EX", "EX-", "VG", "G"]


_CC_GRADE_RE = re.compile(r"(?<![\w/\-])((?:LN|Like New|Near Mint|Mint|M(?=[+\-/])|Ex|VG|Vg)[+\-]*(?:\s*/\s*(?:LN|Mint|M|Ex|VG|Vg)?[+\-]*)*)(?=[\s,.;)]|$)")


def _classicconnection_grade(text):
    """Classic Connection 제목·설명의 상태 표기(마지막 것) → 낮은 쪽 하나: 'Ex+/++' → 'EX+', 'Ex++/Mint-' → 'EX++',
    'Mint/LN-' → 'MINT', 'Ex/Vg' → 'VG', 'M-' → 'MINT-'. 'Summicron-M'·'Leica M'의 M은 등급으로 보지 않음"""
    found = _CC_GRADE_RE.findall(text)
    if not found:
        return None
    grades = []
    last = None
    for part in re.split(r"\s*/\s*", found[-1]):
        if not part.strip():
            continue
        word = re.match(r"(LN|Like New|Near Mint|Mint|M|Ex|VG|Vg)?([+\-]*)$", part.strip())
        if not word:
            continue
        base = (word.group(1) or last or "").upper().replace("LIKE NEW", "LN")
        base = "MINT" if base == "M" else base
        if not base:
            continue
        last = word.group(1) or last
        grade = base + word.group(2)
        if base == "EX" and grade not in _CC_GRADE_ORDER:
            grade = "EX++" if word.group(2).count("+") >= 2 else "EX"
        if base == "MINT" and grade not in _CC_GRADE_ORDER:
            grade = "MINT-" if "-" in word.group(2) else "MINT"
        if base == "LN":
            grade = "LN"
        if grade in _CC_GRADE_ORDER:
            grades.append(grade)
    return max(grades, key=_CC_GRADE_ORDER.index) if grades else None


def _classicconnection_name(title):
    """Classic Connection 제목 다듬기: 등급·연도·'with …' 딸린 물건·'camera'·'lens' 말을 떼어 본품 이름만
    ('Leica M3 Double Stroke Chrome camera with Leica 50mm,… Ex+' → 'Leica M3 Double Stroke Chrome')"""
    name = re.sub(r"\s*/\s*(?:Free Shipping|On Hold|In Stock)\b.*$", "", title.replace("\u2011", "-"), flags=re.I)
    name = _CC_GRADE_RE.sub("", name)
    name = re.sub(r"\s*\((?:circa\s*)?\d{4}[^)]*\)", "", name)
    name = re.sub(r"\bcirca \d{4}\b", "", name)
    name = re.sub(r"\s*\(?Free Shipping\b.*$|\s*Cat\s?#\s?\d+", "", name, flags=re.I)
    name = re.split(r"\s+(?:with|w/|sold with|in|including)\s+|\s+[\u2013\u2014+/-]\s+|,\s+", name, maxsplit=1, flags=re.I)[0]
    if name.count("(") > name.count(")"):
        name = name[:name.rindex("(")]  # 괄호 안에서 잘렸으면 괄호째 뗌
    name = re.sub(r"\b(\d{2,3})/(\d(?:[.,]\d+)?)\b", lambda m: f"{m.group(1)}mm f{m.group(2).replace(',', '.')}", name)
    name = re.sub(r"\bf/(\d)", r"f\1", name)
    name = re.sub(r"\bf(\d),(\d)\b", r"f\1.\2", name)  # 'f1,5' → 'f1.5'
    name = re.sub(r"\b(\d{1,2}(?:\.\d)?)cm\b", lambda m: f"{round(float(m.group(1)) * 10)}mm", name)  # '9cm' → '90mm'
    name = re.sub(r"\b(?:35mm )?(?:classic )?(?:camera|lens)\b", "", name, flags=re.I)
    name = re.sub(r"[\u201c\u201d\"]", "", name)
    return re.sub(r"\s+", " ", name).strip(" ,&+/")


def crawl_classicconnection():
    """Classic Connection (미국) - 라이카 중고 전문 딜러 WooCommerce 상품 API(Store API) JSON. 라이카 분류 아래 이름에
    'Used'·'Demo'가 든 분류(M·스크루·SLR·SL·디지털 중고 등)만 골라 받고(400개쯤, 40초) 라이카·라이츠·판매 중만.
    등급은 제목 끝(없으면 설명)의 'Ex++'·'Mint-'·'Ex+/++' 표기에서 낮은 쪽"""
    import html as _html
    import requests
    from condition_grade import CLASSICCONNECTION_PREFIX
    results = []
    base = "https://classicconnection.com"
    headers = {"User-Agent": USER_AGENTS[1]}
    print(f"\n  📂 Classic Connection 크롤링 시작")
    try:
        resp = requests.get(f"{base}/wp-json/wc/store/v1/products/categories?per_page=100", headers=headers, timeout=60)
        resp.raise_for_status()
        cats = resp.json()
    except Exception as e:
        raise RuntimeError(f"Classic Connection 분류 못 읽음: {e}")
    leica_ids = {c["id"] for c in cats if _html.unescape(c.get("name") or "").strip() == "Leica"}
    used_ids = [str(c["id"]) for c in cats if c.get("parent") in leica_ids and re.search(r"used|demo", _html.unescape(c.get("name") or ""), re.I)]
    if not used_ids:
        raise RuntimeError("Classic Connection 라이카 중고 분류를 못 찾음")
    seen = set()
    for page_num in range(1, 30):
        url = f"{base}/wp-json/wc/store/v1/products?category={','.join(used_ids)}&per_page=100&page={page_num}"
        try:
            resp = requests.get(url, headers=headers, timeout=60)
            resp.raise_for_status()
            products = resp.json()
        except Exception as e:
            raise RuntimeError(f"Classic Connection {page_num}페이지 못 읽음: {e}")  # 빠진 쪽이 판매완료로 바뀌지 않게
        if not products:
            break
        print(f"    └─ {page_num}페이지 {len(products)}개 상품 발견")
        for p in products:
            title = re.sub(r"\s+", " ", _html.unescape(p.get("name") or "")).strip()
            if p.get("id") in seen or not re.match(r"(?:leica|leitz)\b", title, re.I) or not p.get("is_in_stock"):
                continue
            seen.add(p.get("id"))
            if re.search(r"\bsold\b|on hold|(?<!like )\bnew\b(?!\s*(?:york|jersey))", title, re.I):
                continue  # 판매됨·보류·새 상품(중고 분류에 섞임)
            prices = p.get("prices") or {}
            try:
                value = int(prices.get("price")) / 10 ** int(prices.get("currency_minor_unit", 2))
            except (TypeError, ValueError):
                value = 0
            if value <= 0:
                continue  # 가격 없는 상품(문의)은 뺌
            price = f"${value:,.0f}"
            text = _html.unescape(re.sub(r"<[^>]+>", " ", (p.get("short_description") or "") + " " + (p.get("description") or "")))
            grade = _classicconnection_grade(title) or _classicconnection_grade(re.sub(r"\s+", " ", text)[:400])
            cond = CLASSICCONNECTION_PREFIX + grade if grade else "정보없음"
            name = _classicconnection_name(title)
            img = p["images"][0].get("src", "") if p.get("images") else ""
            cat = detect_category(name, price)
            mount = 'Accessory' if cat == 'Accessory' else detect_mount(name)
            results.append({
                "site": "Classic Connection (미국)",
                "label": auto_label(name),
                "상품명": name,
                "세대": detect_generation(name),
                "컨디션": cond,
                "가격": price,
                "통화": "USD",
                "이미지": img,
                "링크": p.get("permalink") or "",
                "품절": False,
                "예약중": False,
                "mount": mount,
                "category": cat,
                "brand": detect_brand(name),
            })
        if len(products) < 100:
            break
        time.sleep(random.uniform(1.0, 2.0))
    print(f"  ✅ Classic Connection 완료: {len(results)}개")
    return results


def _classiccamera_condition(text):
    """The Classic Camera 설명의 상태 글귀 → 'Mint-'·'EXC+++'·'Near Mint' 같은 짧은 표기 (설명 첫 줄 'Condition EXC + +', 'Used Product in EXC++ Condition' 등)"""
    m = re.search(r"\b(as new|like new|near[\s-]?mint|mint\s*-?|exc(?:ellent)?\.?(?:\s*\+)*|good)(?![a-z])", text, re.I)
    if not m:
        return None
    word = m.group(1).lower()
    if word.startswith(("as new", "like new")):
        return "As New"
    if word.startswith("near"):
        return "Near Mint"
    if word.startswith("mint"):
        return "Mint-" if "-" in word else "Mint"
    if word.startswith("exc"):
        return "EXC" + "+" * min(word.count("+"), 3)
    return "Good"


def crawl_classiccamera():
    """The Classic Camera (영국) - 런던 라이카 전문점 WooCommerce 상품 API(Store API) JSON 전체(650개쯤)에서
    'Used …' 분류에 든 라이카·라이츠만 (새 상품·다른 브랜드 제외). 등급은 설명의 'Condition EXC + +'·'Mint-' 글귀"""
    import html as _html
    import requests
    from condition_grade import CLASSICCAMERA_PREFIX
    results = []
    base = "https://www.theclassiccamera.com"
    print(f"\n  📂 The Classic Camera 크롤링 시작")
    for page_num in range(1, 30):
        url = f"{base}/wp-json/wc/store/v1/products?per_page=100&page={page_num}"
        try:
            resp = requests.get(url, headers={"User-Agent": USER_AGENTS[1]}, timeout=60)
            resp.raise_for_status()
            products = resp.json()
        except Exception as e:
            raise RuntimeError(f"The Classic Camera {page_num}페이지 못 읽음: {e}")  # 빠진 쪽이 판매완료로 바뀌지 않게
        if not products:
            break
        print(f"    └─ {page_num}페이지 {len(products)}개 상품 발견")
        for p in products:
            name = re.sub(r"\s+", " ", _html.unescape(p.get("name") or "")).strip()
            cats = [_html.unescape(c.get("name") or "") for c in p.get("categories") or []]
            if not re.match(r"(?:leica|leitz)\b", name, re.I) or not any(c.startswith("Used") for c in cats) or not p.get("is_in_stock"):
                continue
            # 바르낙 모델명의 l(엘)을 I로: 'Leica lllF' → 'Leica IIIf', 'la Converted To IIl' → 'Ia Converted To III'
            name = re.sub(r"(?<=Leica )([lI]{1,3})([a-gA-G])?\b", lambda m: m.group(1).replace("l", "I") + (m.group(2) or "").lower(), name)
            name = re.sub(r"\b(?=[lI]*l)[lI]{2,3}\b", lambda m: m.group(0).replace("l", "I"), name)
            name = re.sub(r"\bf/(\d)", r"f\1", name)
            name = re.sub(r"\b(M6|M4-P)TTL\b", r"\1 TTL", name)
            name = re.sub(r"\bVisoflex 111\b", "Visoflex III", name)
            prices = p.get("prices") or {}
            try:
                price = f"£{int(prices.get('price')) / 10 ** int(prices.get('currency_minor_unit', 2)):,.0f}"
            except (TypeError, ValueError):
                price = "문의요망"
            text = _html.unescape(re.sub(r"<[^>]+>", " ", (p.get("short_description") or "") + " " + (p.get("description") or "")))
            grade = _classiccamera_condition(re.sub(r"\s+", " ", text))
            cond = CLASSICCAMERA_PREFIX + grade if grade else "정보없음"
            img = p["images"][0].get("src", "") if p.get("images") else ""
            cat = detect_category(name, price)
            mount = 'Accessory' if cat == 'Accessory' else detect_mount(name)
            results.append({
                "site": "The Classic Camera (영국)",
                "label": auto_label(name),
                "상품명": name,
                "세대": detect_generation(name),
                "컨디션": cond,
                "가격": price,
                "통화": "GBP",
                "이미지": img,
                "링크": p.get("permalink") or "",
                "품절": False,
                "예약중": False,
                "mount": mount,
                "category": cat,
                "brand": detect_brand(name),
            })
        if len(products) < 100:
            break
        time.sleep(random.uniform(1.0, 2.0))
    print(f"  ✅ The Classic Camera 완료: {len(results)}개")
    return results


def _jch_name(title):
    """Japan Camera Hunter 제목 다듬기: '*rare* Leica Summilux-M 35mm f1.4 AA E46 【CLA’D】' → 'Leica Summilux-M 35mm f1.4 AA E46 CLA'D',
    'Leica Elmarit M28/2.8 ASPH' → 'Leica Elmarit-M 28mm f2.8 ASPH', 'F/1.0' → 'f1.0'"""
    import html as _html
    name = re.sub(r"\s+", " ", _html.unescape(title).replace("\u202f", " ")).strip()
    name = re.sub(r"^\*[^*]+\*\s*", "", name)
    name = re.sub(r"[【】]", " ", name).replace("\u2019", "'")
    name = re.sub(r"\s+(?:w/\s*|with\s+)?(?:\S+\s+)?hood\b", "", name, flags=re.I)  # 'W/12452 Hood'·'ITDOO Hood' (렌즈가 액세서리로 가지 않게)
    name = re.sub(r"\s+&\s+\S+\s+Winder\b.*$", "", name, flags=re.I)
    name = re.sub(r"\bHector\b", "Hektor", name)
    name = re.sub(r"\b(\d(?:\.\d)?)cm\b", lambda m: f"{round(float(m.group(1)) * 10)}mm", name)  # '3.5cm' → '35mm'
    name = re.sub(r"\b(Summicron|Summilux|Elmarit|Elmar|Summaron|Summarit|Noctilux)[\s-]?M\s?(\d{2,3})/(\d+(?:\.\d+)?)",
                  r"\1-M \2mm f\3", name)
    name = re.sub(r"\b(\d(?:\.\d+)?)/(\d{2,3})(?:mm)?\b", r"\2mm f\1", name)  # '2.8/90mm'·'R 4/180' → '90mm f2.8'
    name = re.sub(r"\b(\d{2,3})/(\d+(?:\.\d+)?)\b", r"\1mm f\2", name)
    name = re.sub(r"\b(\d{2,3})mm (\d\.\d)\b", r"\1mm f\2", name)  # '35mm 2.8' → '35mm f2.8'
    name = re.sub(r"\b[fF]/(\d+(?:\.\d+)?)", r"f\1", name)
    name = re.sub(r"\bF(\d+(?:\.\d+)?)\b", r"f\1", name)
    name = re.sub(r"\b(f\d+)(?![.\d])", r"\1.0", name)
    name = re.sub(r"\s+w/\s+", " with ", name)
    return re.sub(r"\s+", " ", name).strip()


def crawl_jch():
    """Japan Camera Hunter (일본) - 도쿄 필름 카메라 수출점 WooCommerce 상품 API(Store API)의 'leica' 검색 JSON (70개쯤).
    매장 자체 상품(JCH shop 분류: 핫슈 커버·와인더)과 다른 브랜드(코와 + 어댑터 등)는 뺌. 가격은 USD, 해외 배송.
    등급은 설명 첫 문장 'Mint minus condition.'"""
    import html as _html
    import requests
    from condition_grade import JCH_PREFIX
    results = []
    base = "https://www.japancamerahunter.com"
    print(f"\n  📂 Japan Camera Hunter 크롤링 시작")
    for page_num in range(1, 20):
        url = f"{base}/wp-json/wc/store/v1/products?search=leica&per_page=100&page={page_num}"
        for attempt in range(3):  # 서버가 느려 가끔 30초 넘게 걸림
            try:
                resp = requests.get(url, headers={"User-Agent": USER_AGENTS[1]}, timeout=60)
                resp.raise_for_status()
                products = resp.json()
                break
            except Exception as e:
                if attempt == 2:
                    raise RuntimeError(f"Japan Camera Hunter {page_num}페이지 못 읽음: {e}")  # 빠진 쪽이 판매완료로 바뀌지 않게
                time.sleep(10)
        if not products:
            break
        print(f"    └─ {page_num}페이지 {len(products)}개 상품 발견")
        for p in products:
            name = _jch_name(p.get("name") or "")
            cats = {c.get("name") for c in p.get("categories") or []}
            if not re.match(r"(?:leica|leitz)\b", name, re.I) or "JCH shop" in cats or not p.get("is_in_stock"):
                continue
            if any(b2 in name.lower() for b2 in THIRD_PARTY_BRANDS):
                continue
            prices = p.get("prices") or {}
            try:
                price = f"${int(prices.get('price')) / 10 ** int(prices.get('currency_minor_unit', 2)):,.0f}"
            except (TypeError, ValueError):
                price = "문의요망"
            text = _html.unescape(re.sub(r"<[^>]+>", " ", (p.get("short_description") or "") + " " + (p.get("description") or "")))
            text = re.sub(r"\s+", " ", text.replace("\u202f", " ")).strip()
            m = re.match(r"((?:mint|near mint|like new|excellent|very good|good|clean|user)(?: (?:minus|plus|user))?) condition", text, re.I)
            cond = JCH_PREFIX + m.group(1).lower() if m else "정보없음"
            img = p["images"][0].get("src", "") if p.get("images") else ""
            cat = detect_category(name, price)
            mount = 'Accessory' if cat == 'Accessory' else detect_mount(name)
            results.append({
                "site": "Japan Camera Hunter (일본)",
                "label": auto_label(name),
                "상품명": name,
                "세대": detect_generation(name),
                "컨디션": cond,
                "가격": price,
                "통화": "USD",
                "이미지": img,
                "링크": p.get("permalink") or "",
                "품절": False,
                "예약중": False,
                "mount": mount,
                "category": cat,
                "brand": detect_brand(name),
            })
        if len(products) < 100:
            break
        time.sleep(random.uniform(1.0, 2.0))
    print(f"  ✅ Japan Camera Hunter 완료: {len(results)}개")
    return results


def crawl_howardparker():
    """Howard Parker Photographic (영국) - 빈티지 라이카 전문 소규모 매장(SumUp 몰). 사이트맵(sitemap.products.xml)에서
    leica·leitz 상품 주소를 골라 상세의 구조화 데이터(JSON-LD Product)로 이름·가격(GBP)·재고·사진을 읽는다.
    'reserved-' 주소·OutOfStock은 예약중/품절. 등급 표기 없어 설명 글('Excellent condition' 등)로 (describe_text)"""
    import json as _json
    from concurrent.futures import ThreadPoolExecutor
    import requests
    import crawl_engine as _ce
    from condition_grade import describe_text
    base = "https://howard-parker.com"
    sess = requests.Session()
    sess.headers["User-Agent"] = _ce.BROWSER_UA
    print(f"\n  📂 Howard Parker 크롤링 시작")
    xml = sess.get(f"{base}/sitemap.products.xml", timeout=30)
    xml.raise_for_status()
    links = [u for u in re.findall(r"<loc>([^<]+)</loc>", xml.text)
             if re.search(r"/product/(?:reserved-)?(?:leica|leitz)", u, re.I) and not re.search(r"m-fit-|copy-of", u, re.I)]
    print(f"    └─ 사이트맵 라이카 상품 {len(links)}개")

    def one(url):
        html = sess.get(url, timeout=30).text
        for block in re.findall(r'<script[^>]*application/ld\+json[^>]*>(.*?)</script>', html, re.S):
            try:
                data = _json.loads(block)
            except ValueError:
                continue
            for node in data.get("@graph", [data]) if isinstance(data, dict) else []:
                if node.get("@type") == "Product":
                    return url, node
        return url, None

    results = []
    with ThreadPoolExecutor(3) as ex:
        for url, node in ex.map(one, links):
            if not node:
                continue
            offer = node.get("offers") or {}
            if isinstance(offer, list):
                offer = offer[0] if offer else {}
            name = re.sub(r"\s*\[[^\]]*\]\s*$", "", node.get("name") or "").strip()
            name = re.sub(r"^\[?Reserved\]?\s*[-:]?\s*", "", name, flags=re.I)
            # 딸린 케이스·상자('in Case'·'Boxed')는 액세서리로 읽히지 않게 뺀다
            name = re.sub(r"\s+(?:in|with|w/)\s+(?:original\s+)?(?:ever[- ]ready\s+)?(?:case|box)\b", "", name, flags=re.I)
            name = re.sub(r"\s+(?:boxed|in original box)\b", "", name, flags=re.I)
            try:
                price = f"£{float(offer.get('price')):,.0f}"
            except (TypeError, ValueError):
                price = "문의요망"
            imgs = node.get("image") or []
            img = imgs[0] if isinstance(imgs, list) and imgs else (imgs if isinstance(imgs, str) else "")
            reserved = "/product/reserved-" in url
            sold = "OutOfStock" in str(offer.get("availability") or "") and not reserved
            cat = detect_category(name, price)
            mount = 'Accessory' if cat == 'Accessory' else detect_mount(name)
            results.append({
                "site": "Howard Parker (영국)",
                "label": auto_label(name),
                "상품명": name,
                "세대": detect_generation(name),
                "컨디션": describe_text(node.get("description") or "") or "정보없음",
                "가격": price,
                "통화": "GBP",
                "이미지": img,
                "링크": url,
                "품절": sold,
                "예약중": reserved,
                "mount": mount,
                "category": cat,
                "brand": detect_brand(name),
            })
    print(f"  ✅ Howard Parker 완료: {len(results)}개")
    return results


def crawl_photoco():
    """PhotoCo Camera House (호주 애들레이드) - WooCommerce 'Leica Pre-Owned' 분류(180개쯤, 2쪽)를 상품 API(Store API) JSON으로.
    판매 중만, 라이카·라이츠만. 등급 표기 없음. robots.txt Crawl-delay 600초라 쪽 사이 10분 쉬고, 하루 한 번만 돈다"""
    import html as _html
    import requests
    import crawl_engine as _ce
    results = []
    base = "https://photococamera.com"
    print(f"\n  📂 PhotoCo 크롤링 시작")
    for page_num in range(1, 6):
        if page_num > 1:
            time.sleep(600)
        url = f"{base}/wp-json/wc/store/v1/products?category=730&per_page=100&page={page_num}"
        try:
            resp = requests.get(url, headers={"User-Agent": _ce.BROWSER_UA}, timeout=60)
            resp.raise_for_status()
            products = resp.json()
        except Exception as e:
            raise RuntimeError(f"PhotoCo {page_num}페이지 못 읽음: {e}")  # 빠진 쪽이 판매완료로 바뀌지 않게
        if not products:
            break
        print(f"    └─ {page_num}페이지 {len(products)}개 상품 발견")
        for p in products:
            title = _html.unescape(p.get("name") or "")
            if not re.search(r"\b(?:leica|leitz)", title, re.I) or not p.get("is_in_stock"):
                continue
            name = _photoco_name(title)
            prices = p.get("prices") or {}
            try:
                price = f"A${int(prices.get('price')) / 10 ** int(prices.get('currency_minor_unit', 2)):,.0f}"
            except (TypeError, ValueError):
                price = "문의요망"
            img = p["images"][0].get("src", "") if p.get("images") else ""
            cat = detect_category(name, price)
            mount = 'Accessory' if cat == 'Accessory' else detect_mount(name)
            results.append({
                "site": "PhotoCo (호주)",
                "label": auto_label(name),
                "상품명": name,
                "세대": detect_generation(name),
                "컨디션": "정보없음",
                "가격": price,
                "통화": "AUD",
                "이미지": img,
                "링크": p.get("permalink") or "",
                "품절": False,
                "예약중": False,
                "mount": mount,
                "category": cat,
                "brand": detect_brand(name),
            })
        if len(products) < 100:
            break
    print(f"  ✅ PhotoCo 완료: {len(results)}개")
    return results


def _photoco_name(title):
    """PhotoCo 제목 다듬기: 'Leica M39 3.5cm f3.5 Summaron' → '… 35mm …', 'Leica 1f Body' → 'Leica If Body',
    'Leica 35mm f1.4 TL Summilux' → 'Leica Summilux-TL 35mm f1.4', 계열 없는 'Leica M 24mm f3.8'은 Glazer's 표로 계열을 채움"""
    name = re.sub(r"\s+(?:Boxed|Bxd\.?)\s*$", "", _rangefinder_name(title), flags=re.I)
    name = re.sub(r"\s*\+\s*(?:Hood|Adapter|Caps?|Goggles)\b", "", name, flags=re.I)
    name = re.sub(r"\bAsph\.?\s*Lens\b", "ASPH.", name, flags=re.I)
    name = re.sub(r"\b(\d{1,2}(?:\.\d)?)\s?cm\b", lambda m: f"{float(m.group(1)) * 10:g}mm", name)
    name = re.sub(r"^Leica 1([cfg])\b", lambda m: "Leica I" + m.group(1), name)
    name = re.sub(r"\b35mm (SLR|Film|Rangefinder)\b", r"\1", name, flags=re.I)  # 필름 규격 '35mm'를 렌즈로 읽지 않게
    name = re.sub(r"\b13\.5(?=\s+f\d)", "135mm", name)  # 'Hektor 13.5 f4.5' (13.5cm)
    name = re.sub(r"(?<!APO-)\bSummicron-M 75mm", "APO-Summicron-M 75mm", name)  # 주미크론 75는 APO뿐
    name = re.sub(r"\b(\d{2,3}mm f[\d.]+) TL (Summilux|Summicron|Elmarit|APO-Macro-Elmarit)\b", r"\2-TL \1", name)
    name = re.sub(r"^Leica M39 (?:LTM )?(.+)$", r"Leica \1 LTM", name)  # 'M39'를 바디로 읽지 않게
    name = re.sub(r"\bf(\d)\.0\b", r"f\1", name)
    name = re.sub(r"^Leica (M|R|SL) (\d{2,3}mm f[\d.]+) APO\b", r"Leica \1 APO \2", name)
    return _glazers_lens_name(name)


# J-カメラ에서 담는 매장: 이미 따로 수집하는 곳(기타무라·나니와·대원·키쿠야·코메효·삼보·톱카메라·파이브스타·아카사카)과
# 봇 수집을 막은 곳(맵카메라·후지야)은 뺀다
JCAMERA_SHOPS = ["aikoudou", "esakura", "irohas", "Inherit", "otsuka", "ogisaku", "camerasb", "sanwa0", "yamagen", "yamagen2",
                 "rokko", "cross", "comphoto", "saito", "j2", "suginami", "sukiya", "suzuki", "takanashi", "tokyocam", "nissin",
                 "nisshindo", "nitto", "kitsunedou", "fotoborse", "fujii", "fujikoshi", "penguin", "matsuo", "ricoh"]


def crawl_jcamera():
    """J-カメラ (j-camera.net, 일본 중고점 모음 검색) - 제조사 'ライカ'(mk=14)에 위 매장만 골라 100개씩 정적 HTML.
    robots.txt Crawl-delay 10초 지킴 (7쪽 안팎 → 1분). 카드의 '程度'(中古美品·中古良品·A·AB 등)가 등급, 매장 이름은 상품명 끝 괄호로"""
    import html as _html
    import requests
    import crawl_engine as _ce
    from condition_grade import JCAMERA_PREFIX
    from ja_normalize import ja_to_en
    base = "https://j-camera.net"
    query = "mk[]=14&" + "&".join(f"sh[]={s}" for s in JCAMERA_SHOPS) + "&sr=-15&max=100"
    sess = requests.Session()
    sess.headers["User-Agent"] = _ce.BROWSER_UA
    results, seen = [], set()
    print(f"\n  📂 J-カメラ 크롤링 시작")
    for page_num in range(0, 40):
        if page_num:
            time.sleep(10)
        try:
            resp = sess.get(f"{base}/listp.php?{query}&p={page_num}", timeout=40)
            resp.raise_for_status()
            text = resp.content.decode("utf-8", "replace")
        except Exception as e:
            raise RuntimeError(f"J-カメラ {page_num + 1}페이지 못 읽음: {e}")  # 빠진 쪽이 판매완료로 바뀌지 않게
        cards = re.findall(r'<tr class="item">(.*?)</tr>', text, re.S)
        new = 0
        for card in cards:
            item = re.search(r'href="itemp\.php\?id=(\d+)', card)
            if not item or item.group(1) in seen:
                continue
            seen.add(item.group(1))
            new += 1
            title = _html.unescape((re.search(r"<strong>(.*?)</strong>", card, re.S) or [None, ""])[1]).strip()
            grade = _html.unescape((re.search(r"<li>程度</li>\s*<li><p>([^<]*)</p>", card) or [None, ""])[1]).strip()
            shop = re.search(r'<li class="itemmaker">[^<]*</li>\s*<li>([^<]*)</li>\s*<li>([^<]*)</li>', card)
            kind, shop_name = (shop.group(1), shop.group(2)) if shop else ("", "")
            yen = re.search(r'itemkakaku">&yen;([\d,]+)', card)
            price = f"¥{yen.group(1)}" if yen else "문의요망"
            name = _jcamera_name(title)
            img = re.search(r'<img src="(https?://[^"]+)"[^>]*alt=', card)
            cat = "Accessory" if kind == "アクセサリー" else detect_category(name, price)
            mount = 'Accessory' if cat == 'Accessory' else detect_mount(name)
            results.append({
                "site": "J-カメラ (일본)",
                "label": auto_label(name),
                "상품명": name,
                "세대": detect_generation(name),
                "컨디션": JCAMERA_PREFIX + grade if grade else "정보없음",
                "가격": price,
                "통화": "JPY",
                "이미지": img.group(1) if img else "",
                "링크": f"{base}/itemp.php?id={item.group(1)}",
                "품절": False,
                "예약중": False,
                "mount": mount,
                "category": cat,
                "brand": detect_brand(name),
                "shop": shop_name,
            })
        print(f"    └─ {page_num + 1}페이지 {len(cards)}개")
        if not new or len(cards) < 100:
            break
    print(f"  ✅ J-カメラ 완료: {len(results)}개")
    return results


def _jcamera_name(title):
    """J-カメラ 제목 다듬기: 【希少】·【1954年製】 같은 꼬리표 빼기, 오타(Sumicron·ズミルクス)·붙여 쓴 이름(Elmar90mm·M6TTL)·
    일본식 바르낙 이름(3c·0型 復刻·A型) 고치기. 일본어를 ja_to_en으로 바꾼 뒤에 고친다 (エルマー90mm → Elmar90mm)"""
    from ja_normalize import ja_to_en
    t = re.sub(r"【[^】]*】", " ", title.replace("　", " "))
    t = t.replace("ズミルクス", "ズミルックス").replace("パリオ", "バリオ").replace("ファット", "Fat ")
    t = re.sub(r"\s+", " ", ja_to_en(t)).strip()
    t = re.sub(r"^(?:leica|ライカ)\s*", "", t, flags=re.I)
    t = re.sub(r"\bSumicron\b", "Summicron", t, flags=re.I)
    t = re.sub(r"^0型\s*復刻(?:版)?", "0-Series Reissue ", t)
    t = re.sub(r"^([1-3])([a-gA-G])\b", lambda m: "I" * int(m.group(1)) + m.group(2).lower(), t)
    t = re.sub(r"^A型", "I (Model A)", t)
    t = re.sub(r"\bM6TTL\b", "M6 TTL", t, flags=re.I)
    t = re.sub(r"([A-Za-z])(\d{2,3}(?:\.\d)?\s?(?:mm|cm))", r"\1 \2", t)  # 'Elmar90mm' → 'Elmar 90mm'
    t = re.sub(r"(\d)\s?mm\s?f\s?(\d)", r"\1mm f\2", t, flags=re.I)
    t = re.sub(r"\bElmarc\s?(\d)", r"Elmar-C \1", t)
    return t if re.match(r"(?:leica|leitz)\b", t, re.I) else "Leica " + t


KENMORE_SECTIONS = ["used-lenses-for-mirrorless/used-leica-m-mount-lenses", "used-film-era-lenses/used-leica-ltm-m39-lenses",
                    "used-film-era-lenses/used-leica-r-lenses", "used-mirrorless-digital-cameras/used-leica-mirrorless-cameras",
                    "used-compact-digital-cameras/used-leica-compact-digital-cameras", "used-camera-lens-accessories/used-accessories-for-leica"]


def crawl_kenmore():
    """Kenmore Camera (미국 시애틀) - BigCommerce 중고 라이카 분류 6곳을 정적 HTML로 (목록에 있으면 판매 중). 가격 USD.
    제목 'USED LEICA (M) 50MM F1.4 SUMMILUX' → 'Leica Summilux-M 50mm f1.4' 꼴. 분류에 섞인 다른 회사(7Artisans·보이그랜더·Orion) 제외.
    등급 표기 없음"""
    import html as _html
    import requests
    import crawl_engine as _ce
    base = "https://kenmorecamera.com/used-equipment"
    sess = requests.Session()
    sess.headers["User-Agent"] = _ce.BROWSER_UA
    results, seen = [], set()
    print(f"\n  📂 Kenmore Camera 크롤링 시작")
    for section in KENMORE_SECTIONS:
        for page_num in range(1, 10):
            try:
                resp = sess.get(f"{base}/{section}/?page={page_num}", timeout=30)
                resp.raise_for_status()
            except Exception as e:
                raise RuntimeError(f"Kenmore {section} {page_num}페이지 못 읽음: {e}")  # 빠진 쪽이 판매완료로 바뀌지 않게
            new = 0
            for card in re.split(r"<article\s", resp.text)[1:]:
                link = re.search(r'class="image-link desktop" href="([^"]+)"', card)
                title = re.search(r'title="([^"]+)"', card)
                if not link or not title or link.group(1) in seen:
                    continue
                seen.add(link.group(1))
                new += 1
                raw = _html.unescape(title.group(1)).strip()
                if not re.search(r"\bLEICA\b", raw) or re.search(r"7ARTISANS|VOIGTL|ORION|TTARTISAN|ZEISS|\(LEICA[- ]M\)", raw, re.I):
                    continue
                name = re.sub(r"^USED\s+", "", raw, flags=re.I)
                name = re.sub(r"^LEICA \((M|R|LTM)\)\s+", r"Leica \1 ", name)  # 'LEICA (R) 19MM …' → 'Leica R 19MM …'
                name = re.sub(r"(\d)MM\b", r"\1mm", name)
                name = re.sub(r"\bF(\d)", r"f\1", name)
                name = re.sub(r"^LEICA\b", "Leica", name)
                pr = re.search(r"price price--withoutTax[^>]*>\s*\$([\d,.]+)", card)
                price = f"${pr.group(1)}" if pr else "문의요망"
                img = re.search(r'data-src="([^"]+)"', card)
                cat = "Accessory" if "accessories" in section else detect_category(name, price)
                mount = 'Accessory' if cat == 'Accessory' else detect_mount(name)
                results.append({
                    "site": "Kenmore Camera (미국)",
                    "label": auto_label(name),
                    "상품명": name,
                    "세대": detect_generation(name),
                    "컨디션": "정보없음",
                    "가격": price,
                    "통화": "USD",
                    "이미지": img.group(1) if img else "",
                    "링크": link.group(1),
                    "품절": False,
                    "예약중": False,
                    "mount": mount,
                    "category": cat,
                    "brand": detect_brand(name),
                })
            if not new or f"?page={page_num + 1}" not in resp.text:
                break
            time.sleep(random.uniform(1.0, 2.0))
    print(f"  ✅ Kenmore Camera 완료: {len(results)}개")
    return results


def crawl_usedcl():
    """Used.cl (칠레 산티아고) - Horizontal Foto의 중고 전문몰(Jumpseller). '/leica' 분류를 정적 HTML로 (쪽마다 30개쯤).
    라이카·라이츠 제목만 (분류에 시그마·보이그랜더 M 마운트 렌즈도 섞임). 'No disponible'은 품절. 가격 CLP, 가격 없는 매물은 문의.
    등급 표기 없음"""
    import html as _html
    import requests
    import crawl_engine as _ce
    base = "https://www.used.cl"
    sess = requests.Session()
    sess.headers["User-Agent"] = _ce.BROWSER_UA
    results, seen = [], set()
    print(f"\n  📂 Used.cl 크롤링 시작")
    for page_num in range(1, 20):
        try:
            resp = sess.get(f"{base}/leica?page={page_num}", timeout=30)
            resp.raise_for_status()
        except Exception as e:
            raise RuntimeError(f"Used.cl {page_num}페이지 못 읽음: {e}")  # 빠진 쪽이 판매완료로 바뀌지 않게
        new = 0
        for block in resp.text.split("product-block__wrapper")[1:]:
            a = re.search(r'href="(/[^"]+)" class="product-block__anchor" title="Ir a ([^"]+)"', block)
            if not a or a.group(1) in seen:
                continue
            seen.add(a.group(1))
            new += 1
            title = _html.unescape(a.group(2)).strip()
            if (not re.search(r"\b(?:leica|leitz)\b", title, re.I)
                    or re.search(r"\b(?:for|para|montura)\b|\(leica|minolta|sigma|voigtl", title, re.I)):
                continue
            name = re.sub(r"\s*-\s*usad[oa]\.?\s*$", "", title, flags=re.I).strip()
            # 'APO-ELMARIT-R 1:2,8/180' → '180mm f2.8', 'Visor 24mm'(파인더) → 'Viewfinder 24mm'
            name = re.sub(r"\b1\s?:\s?(\d+)(?:[,.](\d))?\s*/\s*(\d{2,3})\b",
                          lambda m: f"{m.group(3)}mm f{m.group(1)}" + (f".{m.group(2)}" if m.group(2) else ""), name)
            name = re.sub(r"\bVisor\b", "Viewfinder", name, flags=re.I)
            name = re.sub(r"^Leica Leitz\b", "Leitz", name, flags=re.I)
            pr = re.search(r'product-block__price[^>]*>\s*\$\s*([\d.]+)', block)
            price = f"CLP {int(pr.group(1).replace('.', '')):,}" if pr else "문의요망"
            img = re.search(r'<img src="(https://cdnx\.jumpseller\.com/[^"]+)"', block)
            img = re.sub(r"/resize/\d+/\d+", "/resize/640/640", img.group(1)) if img else ""
            cat = detect_category(name, price)
            mount = 'Accessory' if cat == 'Accessory' else detect_mount(name)
            results.append({
                "site": "Used.cl (칠레)",
                "label": auto_label(name),
                "상품명": name,
                "세대": detect_generation(name),
                "컨디션": "정보없음",
                "가격": price,
                "통화": "CLP",
                "이미지": img,
                "링크": base + a.group(1),
                "품절": "No disponible" in block,
                "예약중": False,
                "mount": mount,
                "category": cat,
                "brand": detect_brand(name),
            })
        print(f"    └─ {page_num}페이지 새 상품 {new}개")
        if not new:
            break
        time.sleep(random.uniform(1.0, 2.0))
    print(f"  ✅ Used.cl 완료: {len(results)}개")
    return results


_FOTODOTTI_OTHER = re.compile(r"minolta|voigtl|zeiss|schneider|shneider|closter|kipon|fotodiox|fotga|k&f|peipro|quenox|crumpler|"
                              r"\beos\b|nikon|canon|sony|copy", re.I)


_FOTODOTTI_WORDS = [(r"\bparaluce\b", "Hood"), (r"\bmirino\b", "Viewfinder"), (r"\bfiltro\b", "Filter"),
                    (r"\bcustodia\b|\bborsa\b", "Case"), (r"\banello\b", "Ring"), (r"\btappo\b|\bfondello\b", "Cap"),
                    (r"\btubo\b", "Tube"), (r"\bsoffietto\b", "Bellows"), (r"\bcampana\b", "Hood"), (r"\bscatto flessibile\b", "Release")]


def _fotodotti_name(raw):
    """Foto Dotti 제목 다듬기: 'Obiettivo'·'Accessorio per …'·끝의 'Bello'·'Completo' 빼기, 이탈리아어 액세서리 말을 영어로,
    'Leica M39 Elmar 9cm' → 'Leica Elmar 9cm LTM', 'Leica R Summilux 80mm' → 'Leica Summilux-R 80mm'"""
    name = re.sub(r"^(?:Obiettivo(?: manuale)?|Accessorio(?: analogico)? per (?:fotocamera|obiettivo|macro)|Accessorio(?: analogico)?)\s+",
                  "", raw, flags=re.I)
    name = re.sub(r"\s+(?:bellissim[oa]|bell[oa]|rar[oa]|come nuov[oa]|ottim[oa]|perfett[oa]|completo)\b.*$", "", name, flags=re.I)
    name = re.sub(r"\s+(?:\+|con)\s+(?:filtro|filter|paraluce|hood|custodia|case)\b.*$", "", name, flags=re.I)  # 딸린 필터·후드
    name = re.sub(r"\b1\s?:\s?(\d+)(?:[,.](\d))?\s*/\s*(\d{2,3})\s?mm\b",
                  lambda m: f"{m.group(3)}mm f{m.group(1)}" + (f".{m.group(2)}" if m.group(2) else ""), name)
    name = re.sub(r"\b(\d{1,2}),(\d)\s?cm\b", lambda m: f"{int(m.group(1)) * 10 + int(m.group(2))}mm", name)
    for pattern, word in _FOTODOTTI_WORDS:
        name = re.sub(pattern, word, name, flags=re.I)
    name = re.sub(r"^(Leica)\s+M39\s+(.+)$", r"\1 \2 LTM", name, flags=re.I)
    name = re.sub(r"^(Leica)\s+R\s+(Summilux|Summicron|Elmarit|Elmar|Macro[ -]Elmarit|Super[ -]Angulon|Telyt)\b", r"\1 \2-R", name, flags=re.I)
    name = re.sub(r"\b(Summilux|Summicron|Elmarit|Elmar|Telyt)\s+R\b", r"\1-R", name, flags=re.I)
    name = re.sub(r"\s+", " ", name).strip(" -.")
    return name if re.search(r"\b(?:leica|leitz)\b", name, re.I) else "Leica " + name


def crawl_fotodotti():
    """Foto Dotti (이탈리아 모데나) - Magento 라이카 중고 분류 3곳(렌즈·바디·액세서리)을 정적 HTML로 (쪽마다 12개).
    목록에 있는 것은 판매 중, 가격 EUR. 목록에 등급 표기가 없어 상세 화면 설명 글 말투로 (처음 본 매물만, IT: …).
    robots.txt는 일반 수집을 막지 않음 (AI 봇만 막음, 2026-11-02 사장님 확인)"""
    import html as _html
    import requests
    import crawl_engine as _ce
    base = "https://www.fotodotti.it/prodotti/leica"
    sess = requests.Session()
    sess.headers["User-Agent"] = _ce.BROWSER_UA
    results, seen = [], set()
    print(f"\n  📂 Foto Dotti 크롤링 시작")
    for section in ("obiettivi", "fotocamere", "accessori"):
        for page_num in range(1, 30):
            try:
                resp = sess.get(f"{base}/{section}/usato.html?p={page_num}", timeout=30)
                resp.raise_for_status()
            except Exception as e:
                raise RuntimeError(f"Foto Dotti {section} {page_num}페이지 못 읽음: {e}")  # 빠진 쪽이 판매완료로 바뀌지 않게
            new = 0
            for card in re.split(r'<li\s+class="item\s+product-item', resp.text)[1:]:
                link = re.search(r'<h2\s+class="product-name"><a\s+href="([^"]+)"[^>]*>([^<]+)</a>', card)
                if not link or link.group(1) in seen:
                    continue
                seen.add(link.group(1))
                new += 1
                raw = re.sub(r"\s+", " ", _html.unescape(link.group(2))).strip()
                if _FOTODOTTI_OTHER.search(raw):
                    continue  # 라이카 분류에 섞인 다른 회사 렌즈·어댑터
                name = _fotodotti_name(raw)
                pr = re.search(r'<span\s+class="price">([\d.]+,\d{2})\s*€', card)
                # 이탈리아식 '4.800,00 €' (점이 천 단위) → '€4,800'
                price = f"€{int(pr.group(1).split(',')[0].replace('.', '')):,}" if pr else "문의요망"
                img = re.search(r'<img\s+src="([^"]+)"', card)
                cat = "Accessory" if section == "accessori" else detect_category(name, price)
                mount = 'Accessory' if cat == 'Accessory' else detect_mount(name)
                results.append({
                    "site": "Foto Dotti (이탈리아)",
                    "label": auto_label(name),
                    "상품명": name,
                    "세대": detect_generation(name),
                    "컨디션": "정보없음",
                    "가격": price,
                    "통화": "EUR",
                    "이미지": img.group(1) if img else "",
                    "링크": link.group(1),
                    "품절": False,
                    "예약중": False,
                    "mount": mount,
                    "category": cat,
                    "brand": detect_brand(name),
                })
            print(f"    └─ {section} {page_num}페이지 새 상품 {new}개")
            if not new:
                break
            time.sleep(random.uniform(1.0, 2.0))
    from condition_grade import it_condition

    def read_detail(url):  # 'Dettagli' 칸의 설명 글 ('IN OTTIME CONDIZIONI ESTETICHE E FUNZIONALI …')
        page = sess.get(url, timeout=30)
        page.raise_for_status()
        m = re.search(r'Dettagli([\s\S]{0,4000}?)Specifiche', re.sub(r"<[^>]+>", " ", page.text))
        return it_condition(_html.unescape(m.group(1))) if m else None
    _fill_detail_conditions("Foto Dotti (이탈리아)", results, read_detail)
    print(f"  ✅ Foto Dotti 완료: {len(results)}개")
    return results


def crawl_therangefinder():
    """The Rangefinder (캐나다 몬트리올) - WooCommerce 상품 API(Store API)에서 'leica' 검색, 판매 중만, 가격 CAD.
    다른 회사의 라이카 마운트 렌즈·어댑터(캐논 LTM·보이그랜더·Light Lens Lab·파나소닉 등)는 뺀다.
    robots.txt Crawl-delay 10초 지킴. 등급 표기 없음"""
    import html as _html
    import requests
    import crawl_engine as _ce
    base = "https://therangefinder.com"
    other = re.compile(r"canon|voigtl|panasonic|lumix|7artisans|ttartisan|light lens|meyer|artralab|rayqual|match technical|sigma|"
                       r"\bfor (?:the )?leica|leica[- ](?:m|l|r)[- ]mount|leica thread|lpl mount|cine kit", re.I)
    results = []
    print(f"\n  📂 The Rangefinder 크롤링 시작")
    for page_num in range(1, 10):
        if page_num > 1:
            time.sleep(10)
        try:
            resp = requests.get(f"{base}/wp-json/wc/store/v1/products?search=leica&per_page=100&page={page_num}",
                                headers={"User-Agent": _ce.BROWSER_UA}, timeout=30)
            resp.raise_for_status()
            products = resp.json()
        except Exception as e:
            raise RuntimeError(f"The Rangefinder {page_num}페이지 못 읽음: {e}")  # 빠진 쪽이 판매완료로 바뀌지 않게
        if not products:
            break
        for p in products:
            title = re.sub(r"\s+", " ", _html.unescape(p.get("name") or "")).strip()
            if not p.get("is_in_stock") or not re.search(r"\b(?:leica|leitz)\b", title, re.I) or other.search(title):
                continue
            name = re.sub(r"\s+Lens\b", "", title)
            prices = p.get("prices") or {}
            try:
                price = f"C${int(prices.get('price')) / 10 ** int(prices.get('currency_minor_unit', 2)):,.0f}"
            except (TypeError, ValueError):
                price = "문의요망"
            img = p["images"][0].get("src", "") if p.get("images") else ""
            cat = detect_category(name, price)
            mount = 'Accessory' if cat == 'Accessory' else detect_mount(name)
            results.append({
                "site": "The Rangefinder (캐나다)",
                "label": auto_label(name),
                "상품명": name,
                "세대": detect_generation(name),
                "컨디션": "정보없음",
                "가격": price,
                "통화": "CAD",
                "이미지": img,
                "링크": p.get("permalink") or "",
                "품절": False,
                "예약중": False,
                "mount": mount,
                "category": cat,
                "brand": detect_brand(name),
            })
        if len(products) < 100:
            break
    print(f"  ✅ The Rangefinder 완료: {len(results)}개")
    return results


def crawl_leicastoreau(page):
    """Leica Store Australia (멜버른·시드니 공식 매장, Pronto Avenue 몰) - 중고 분류 3곳(바디·렌즈·액세서리)을 브라우저로 열어
    카드의 이름·가격(AUD, GST 포함)·사진을 읽는다 (목록을 스크립트로 그려서 브라우저 필요). robots.txt Crawl-delay 30초 지킴 →
    한 번에 1분 30초쯤, 하루 한 번. 목록에 있는 것은 판매 중. 등급 표기 없음 (상세에만 글로 있음)"""
    import html as _html
    base = "https://www.leica-store.com.au"
    results, seen = [], set()
    print(f"\n  📂 Leica Store Australia 크롤링 시작")
    for n, section in enumerate(("camerasbodies", "Lenses", "accessories")):
        if n:
            time.sleep(30)
        page.goto(f"{base}/categories/photography/preowned/{section}", wait_until="domcontentloaded", timeout=60_000)
        try:
            page.wait_for_selector("div.product-title a", timeout=30_000)
        except Exception:
            print(f"    └─ {section}: 상품 없음")
            continue
        time.sleep(2)
        html = page.content()
        cards = re.split(r'<li class="col-xs-12', html)[1:]
        for card in cards:
            link = re.search(r'<div class="product-title">\s*<a href="(/products/[^"]+)">\s*([^<]+?)\s*</a>', card)
            if not link or link.group(1) in seen:
                continue
            seen.add(link.group(1))
            name = re.sub(r"\s*\(pre-owned\)\s*", " ", _html.unescape(link.group(2)), flags=re.I).strip()
            if not re.search(r"\b(?:leica|leitz)\b", name, re.I):
                name = "Leica " + name
            pr = re.search(r'<div class="price">\$([\d,]+)(?:\.\d{2})?</div>', card)
            price = f"A${pr.group(1)}" if pr else "문의요망"
            img = re.search(r'<img data-src="(https://[^"]+)"[^>]*class="primary-image', card)
            cat = "Accessory" if section == "accessories" else detect_category(name, price)
            mount = 'Accessory' if cat == 'Accessory' else detect_mount(name)
            results.append({
                "site": "Leica Store Australia (호주)",
                "label": auto_label(name),
                "상품명": name,
                "세대": detect_generation(name),
                "컨디션": "정보없음",
                "가격": price,
                "통화": "AUD",
                "이미지": img.group(1) if img else "",
                "링크": base + link.group(1),
                "품절": False,
                "예약중": False,
                "mount": mount,
                "category": cat,
                "brand": detect_brand(name),
            })
        print(f"    └─ {section}: {len(cards)}개")
    print(f"  ✅ Leica Store Australia 완료: {len(results)}개")
    return results


def crawl_leicastoremy():
    """Leica Store Malaysia (쿠알라룸푸르 공식 매장) - Shopify 'pre-owned' 컬렉션 JSON (20개 안팎), 판매 중만. 가격 MYR.
    등급은 설명의 'Condition : A ( LIKE NEW )'·'B (fully functional…)' — 라이카 공식 등급이라 Leica Classic 대응을 그대로 씀.
    Leica Classic 몰의 말레이시아 매물(6개 안팎)과 겹칠 수 있음"""
    import html as _html
    import requests
    import crawl_engine as _ce
    from condition_grade import LEICA_CLASSIC_PREFIX
    results = []
    sess = requests.Session()
    sess.headers["User-Agent"] = _ce.BROWSER_UA
    base = "https://leica-store.my"
    print(f"\n  📂 Leica Store Malaysia 크롤링 시작")
    for p in _shopify_all(sess, f"{base}/collections/pre-owned/products.json", "Leica Store Malaysia"):
        variants = p.get("variants") or [{}]
        if not any(v.get("available") for v in variants):
            continue
        title = re.sub(r"\s+", " ", _html.unescape(p.get("title") or "")).strip()
        name = re.sub(r"^\(pre-owned\)\s*", "", title, flags=re.I)
        name = re.sub(r"^(\d{5})\s+(.+)$", r"\2 \1", name)  # 앞의 품번은 뒤로
        name = re.sub(r"\s*\(\d{7}\)", "", name)  # 일련번호
        name = re.sub(r"\s+with accessories\b", "", name, flags=re.I)
        if not re.search(r"\b(?:leica|leitz)\b", name, re.I):
            name = "Leica " + name
        text = _html.unescape(re.sub(r"<[^>]+>", " ", p.get("body_html") or ""))
        m = re.search(r"Condition\s*:\s*(A\+|A-|A|B\+|B-|B|C)\b", text)
        pct = re.search(r"\b(\d{2})%\s*like new", text, re.I)
        cond = LEICA_CLASSIC_PREFIX + m.group(1) if m else (f"{pct.group(1)}%" if pct else "정보없음")
        try:
            price = f"MYR {float(variants[0].get('price')):,.0f}"
        except (TypeError, ValueError):
            price = "문의요망"
        cat = detect_category(name, price)
        mount = 'Accessory' if cat == 'Accessory' else detect_mount(name)
        img = p["images"][0].get("src", "") if p.get("images") else ""
        results.append({
            "게시일": _shopify_listed(p),
            "site": "Leica Store Malaysia (말레이시아)",
            "label": auto_label(name),
            "상품명": name,
            "세대": detect_generation(name),
            "컨디션": cond,
            "가격": price,
            "통화": "MYR",
            "이미지": img,
            "링크": f"{base}/products/{p['handle']}",
            "품절": False,
            "예약중": False,
            "mount": mount,
            "category": cat,
            "brand": detect_brand(name),
        })
    print(f"  ✅ Leica Store Malaysia 완료: {len(results)}개")
    return results


def crawl_fotomeyer():
    """Foto Meyer (독일 베를린) - Magento 사이트 검색 'leica gebraucht'(robots.txt 막는 것 없음)에서 제목이 '… - gebraucht'인 라이카만.
    상태는 상품 화면 속성 'Zustand'(neuwertig·sehr leichte Gebrauchsspuren·leichte·deutliche·starke Gebrauchsspuren)라
    처음 본 매물만 읽고 전에 읽은 것은 다시 씀(_fill_detail_conditions). Panasonic Leica DG 등 다른 회사는 뺌"""
    import html as _html
    import requests
    import crawl_engine as _ce
    from condition_grade import FOTOMEYER_PREFIX
    results, seen = [], set()
    sess = requests.Session()
    sess.headers["User-Agent"] = _ce.BROWSER_UA
    base = "https://www.fotomeyer.de"
    print(f"\n  📂 Foto Meyer 크롤링 시작")
    for page in range(1, 15):
        resp = sess.get(f"{base}/catalogsearch/result/", params={"q": "leica gebraucht", "p": page}, timeout=30)
        resp.raise_for_status()
        blocks = re.findall(r'<li class="item product product-item">(.*?)</li>\s*(?=<li class="item product|</ol>)', resp.text, re.S)
        new = 0
        for b in blocks:
            link = re.search(r'class="product-item-link"[^>]*href="([^"]+)"[^>]*>\s*([^<]+)<', b)
            if not link or link.group(1) in seen:
                continue
            seen.add(link.group(1))
            new += 1
            title = re.sub(r"\s+", " ", _html.unescape(link.group(2))).strip()
            if not re.search(r"(?i)gebraucht\s*$", title) or not re.search(r"(?i)\b(?:leica|leitz)\b", title) or re.search(r"(?i)^panasonic|lumix|sigma|tamron|voigt|walimex", title):
                continue
            name = re.sub(r"(?i)\s*-\s*gebraucht\s*$", "", title).strip()
            # 독일식 조리개 '180mm 2,8'·'65mm/3,5'·'5cm 3,5' → 'f2.8' (렌즈로 알아보게)
            name = re.sub(r"\b(\d),(\d)cm\b", r"\1\g<2>mm", name)  # 'Summarex 8,5cm' → 85mm
            name = re.sub(r"(\d+(?:mm|cm))\s*/?\s*(\d{1,2}),(\d)\b", r"\1 f\2.\3", name)
            if re.search(r"\b65mm\b", name):  # 비조플렉스 'M 65mm/3,5 Macro Elmar' = Elmar 65mm
                name = re.sub(r"(?i)\bmacro[ -]?elmar\b", "Elmar", name)
            amount = re.search(r'data-price-amount="([\d.]+)"', b)
            price = f"€{float(amount.group(1)):,.0f}" if amount else "문의요망"
            img = re.search(r'class="product-image-photo"[^>]*src="([^"]+)"', b)
            cat = detect_category(name, price)
            results.append({
                "site": "Foto Meyer (독일)",
                "label": auto_label(name),
                "상품명": name,
                "세대": detect_generation(name),
                "컨디션": "정보없음",
                "가격": price,
                "통화": "EUR",
                "이미지": img.group(1) if img else "",
                "링크": link.group(1),
                "품절": False,
                "예약중": False,
                "mount": 'Accessory' if cat == 'Accessory' else detect_mount(name),
                "category": cat,
                "brand": detect_brand(name),
            })
        print(f"    └─ {page}페이지 {len(blocks)}개 (새 {new})")
        if not blocks or not new:
            break
        time.sleep(3)

    def read_detail(url):
        text = _html.unescape(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", sess.get(url, timeout=30).text)))
        m = re.search(r"Zustand\s+(neuwertig|sehr leichte Gebrauchsspuren|leichte Gebrauchsspuren|deutliche Gebrauchsspuren|starke Gebrauchsspuren|Gebrauchsspuren|[A-Za-zäöüÄÖÜß ]{3,40}?)\s+funktionsgeprüft", text)
        return FOTOMEYER_PREFIX + m.group(1).strip().lower() if m else None

    _fill_detail_conditions("Foto Meyer (독일)", results, read_detail)
    print(f"  ✅ Foto Meyer 완료: {len(results)}개")
    return results


def crawl_photo19():
    """Photo19 (이탈리아 브레시아) - PrestaShop 중고 분류 화면(카메라 191·렌즈 192·액세서리 194, 15개씩)에서 라이카·라이츠만.
    robots.txt가 사이트 검색(controller=search)을 막아 분류 화면만 읽음. 이름은 사진 alt, 가격 'price' 칸. 등급 표기 없음(사진 등급 대기열).
    다른 회사의 라이카 마운트 렌즈(7artisans 등)·Panasonic Leica DG는 뺌"""
    import html as _html
    import requests
    import crawl_engine as _ce
    results, seen = [], set()
    sess = requests.Session()
    sess.headers["User-Agent"] = _ce.BROWSER_UA
    base = "https://www.photo19.it"
    print(f"\n  📂 Photo19 크롤링 시작")
    for cat in ("191-fotocamere-usate", "192-obiettivi-usati", "194-accessori-usati-flash-varie"):
        for page in range(1, 20):
            resp = sess.get(f"{base}/{cat}", params={"page": page}, timeout=30)
            resp.raise_for_status()
            arts = re.findall(r'<article[^>]*product-miniature[^>]*>(.*?)</article>', resp.text, re.S)
            for a in arts:
                link = re.search(r'href="(https://www\.photo19\.it/[^"]+\.html)"', a)
                alt = re.search(r'alt="([^"]{4,200})"', a)
                if not link or not alt or link.group(1) in seen:
                    continue
                seen.add(link.group(1))
                name = re.sub(r"\s+", " ", _html.unescape(alt.group(1))).strip()
                if not re.search(r"(?i)\b(?:leica|leitz)\b", name) or re.search(r"(?i)panasonic|lumix|7 ?artisans|sigma|voigt|adatt|per leica|x leica", name):
                    continue
                price_m = re.findall(r'class="price[^"]*"[^>]*>([^<]+)<', a)
                num = re.sub(r"[^\d,]", "", _html.unescape(price_m[-1]).replace(".", "")) if price_m else ""
                price = f"€{float(num.replace(',', '.')):,.0f}" if num else "문의요망"
                img = re.search(r'(?:data-src|src)="(https://[^"]+\.(?:jpg|jpeg|webp|png))"', a)
                cat_name = detect_category(name, price)
                results.append({
                    "site": "Photo19 (이탈리아)",
                    "label": auto_label(name),
                    "상품명": name,
                    "세대": detect_generation(name),
                    "컨디션": "정보없음",
                    "가격": price,
                    "통화": "EUR",
                    "이미지": img.group(1) if img else "",
                    "링크": link.group(1),
                    "품절": False,
                    "예약중": False,
                    "mount": 'Accessory' if cat_name == 'Accessory' else detect_mount(name),
                    "category": cat_name,
                    "brand": detect_brand(name),
                })
            if len(arts) < 15:
                break
            time.sleep(2)
    print(f"  ✅ Photo19 완료: {len(results)}개")
    return results


def crawl_panajou():
    """Panajou (프랑스, 보르도 등 4개 매장) - PrestaShop 사이트 검색 'leica occasion' 결과 화면(25개씩)에서 제목이 Leica로 시작하는 중고만.
    전체 제목은 사진 alt('Leica Summicron-M 50mm f/2 Safari Occasion Garantie 12 Mois'), 가격은 'price' 칸(할인가면 할인가).
    상태는 제목 속 'Comme Neuf'·'Très bon état'·'Bon état' (condition_grade PANAJOU_PREFIX), 없으면 정보없음.
    robots.txt는 '?search_query='만 막음 — 이 수집기는 '?controller=search&s='를 씀. 배송은 프랑스·벨기에만"""
    import html as _html
    import requests
    import crawl_engine as _ce
    from condition_grade import PANAJOU_PREFIX
    results, seen = [], set()
    sess = requests.Session()
    sess.headers["User-Agent"] = _ce.BROWSER_UA
    base = "https://www.panajou.fr"
    print(f"\n  📂 Panajou 크롤링 시작")
    for page in range(1, 11):
        resp = sess.get(f"{base}/recherche", params={"controller": "search", "s": "leica occasion", "page": page}, timeout=30)
        resp.raise_for_status()
        arts = re.findall(r'<article[^>]*product-miniature[^>]*>(.*?)</article>', resp.text, re.S)
        new = 0
        for a in arts:
            link = re.search(r'href="(https://www\.panajou\.fr/[^"]+_p\d+)"', a)
            alt = re.search(r'alt="([^"]{10,200})"', a)
            if not link or not alt or link.group(1) in seen:
                continue
            seen.add(link.group(1))
            new += 1
            title = re.sub(r"\s+", " ", _html.unescape(alt.group(1))).strip()
            used = "occasion" in title.lower() or "occasion" in link.group(1).lower()  # 중고는 주소에도 '-occasion_p…'
            if title.endswith("...") and re.match(r"(?i)leica\b", title):  # 긴 제목은 alt에서 잘림 → 상품 화면 제목
                try:
                    time.sleep(2)
                    page_html = sess.get(link.group(1), timeout=30).text
                    h1 = re.search(r"<h1[^>]*>(.*?)</h1>", page_html, re.S)
                    if h1:
                        title = re.sub(r"\s+", " ", _html.unescape(re.sub(r"<[^>]+>", "", h1.group(1)))).strip() or title
                        title = re.sub(r"(?i)^(?:appareils photo|objectifs photo|accessoires)(?: d['’]occasion)?\s+", "", title)  # h1 앞의 분류 이름
                    # 화면 제목엔 'Occasion'이 없을 수 있음 → 중고 분류(occasions_c35 등) 안에 있으면 중고
                    used = used or "occasion" in title.lower() or bool(re.search(r"occasions?_c3[5-7]", page_html))
                    if not re.search(r"(?i)\b(comme neuf|tr[eè]s bon [ée]tat|bon [ée]tat)\b", title):
                        state = re.search(r"(?i)occasion\s+(comme neuf|tr[eè]s bon [ée]tat|bon [ée]tat)\b", _html.unescape(re.sub(r"<[^>]+>", " ", page_html)))
                        if state:
                            title += " " + state.group(1)
                except Exception:
                    pass
            if not re.match(r"(?i)leica\b", title) or not used:
                continue  # 새 상품·다른 회사(Voigtländer·Panasonic Leica DG 등)
            m = re.search(r"(?i)\b(comme neuf|tr[eè]s bon [ée]tat|bon [ée]tat)\b", title)
            cond = PANAJOU_PREFIX + m.group(1).lower() if m else "정보없음"
            name = re.sub(r"(?i)\s*[-–]?\s*(?:d['’])?occasion\b.*$", "", title)
            name = re.sub(r"(?i)\s+appareil photo$", "", name).strip(" -–")
            price_m = re.findall(r'class="price[^"]*"[^>]*>([^<]+)<', a)
            raw = _html.unescape(price_m[-1]).replace("\u202f", "").replace("\xa0", "").replace(" ", "") if price_m else ""
            num = re.sub(r"[^\d,]", "", raw).replace(",", ".")
            price = f"€{float(num):,.0f}" if num else "문의요망"
            img = re.search(r'(?:data-src|src)="(https://[^"]+\.(?:jpg|jpeg|webp|png))"', a)
            cat = detect_category(name, price)
            results.append({
                "site": "Panajou (프랑스)",
                "label": auto_label(name),
                "상품명": name,
                "세대": detect_generation(name),
                "컨디션": cond,
                "가격": price,
                "통화": "EUR",
                "이미지": img.group(1) if img else "",
                "링크": link.group(1),
                "품절": "en stock" not in a.lower(),
                "예약중": False,
                "mount": 'Accessory' if cat == 'Accessory' else detect_mount(name),
                "category": cat,
                "brand": detect_brand(name),
            })
        print(f"    └─ {page}페이지 {len(arts)}개 (새 {new})")
        if not arts or not new or len(arts) < 25:
            break
        time.sleep(3)
    print(f"  ✅ Panajou 완료: {len(results)}개")
    return results


def crawl_imagefoto():
    """Image Foto (덴마크, 라이카 공인 딜러) - Shopify '브루트'(brugt, 중고) 컬렉션 JSON에서 판매자 Leica만, 판매 중만. 가격 DKK.
    제목 'Brugt Leica M2 Chrome m. Selvudløser' → 'Leica M2 Chrome', 'Udstillingsmodel'(진열품)은 그대로 둠. 등급 표기 없음"""
    import html as _html
    import requests
    import crawl_engine as _ce
    results = []
    sess = requests.Session()
    sess.headers["User-Agent"] = _ce.BROWSER_UA
    base = "https://imagefoto.dk"
    print(f"\n  📂 Image Foto 크롤링 시작")
    for p in _shopify_all(sess, f"{base}/collections/brugt/products.json", "Image Foto"):
        if (p.get("vendor") or "").strip().lower() not in ("leica", "leitz"):
            continue
        variants = p.get("variants") or [{}]
        if not any(v.get("available") for v in variants):
            continue
        title = re.sub(r"\s+", " ", _html.unescape(p.get("title") or "")).strip()
        name = re.sub(r"^Brugt\s+", "", title, flags=re.I)
        name = re.sub(r"\s+m\.\s+Selvudløser\b", " self-timer", name, flags=re.I)
        name = re.sub(r"\s*\+\s*Lysmåler\b", "", name, flags=re.I)
        name = re.sub(r"\bSølv\b", "Silver", name)
        name = re.sub(r"\bSort\b", "Black", name)
        name = re.sub(r"\b1:(\d+)\s*/\s*(\d{2,3})mm\b", r"\2mm f\1", name)
        name = re.sub(r"(\d),(\d)\s?cm\b", lambda m: f"{int(m.group(1)) * 10 + int(m.group(2))}mm", name)
        name = re.sub(r"\bf/(\d),(\d)", r"f\1.\2", name)
        name = re.sub(r"^Ernst-Leitz Wetzlar\b", "Leitz", name)
        name = re.sub(r"\s+", " ", name).strip(" –-")
        if not re.search(r"\b(?:leica|leitz)\b", name, re.I):
            name = "Leica " + name
        try:
            price = f"DKK {float(variants[0].get('price')):,.0f}"
        except (TypeError, ValueError):
            price = "문의요망"
        cat = detect_category(name, price)
        mount = 'Accessory' if cat == 'Accessory' else detect_mount(name)
        img = p["images"][0].get("src", "") if p.get("images") else ""
        results.append({
            "게시일": _shopify_listed(p),
            "site": "Image Foto (덴마크)",
            "label": auto_label(name),
            "상품명": name,
            "세대": detect_generation(name),
            "컨디션": "정보없음",
            "가격": price,
            "통화": "DKK",
            "이미지": img,
            "링크": f"{base}/products/{p['handle']}",
            "품절": False,
            "예약중": False,
            "mount": mount,
            "category": cat,
            "brand": detect_brand(name),
        })
    print(f"  ✅ Image Foto 완료: {len(results)}개")
    return results


GEBRAUCHTKAMERAS_SLUG = re.compile(r"leica|leitz|summicron|summilux|summarit|summaron|noctilux|elmar|telyt|hektor|visoflex", re.I)


def crawl_gebrauchtkameras():
    """gebrauchtkameras.de (독일) - ePages 상점. 사이트맵(sitemap-products-N.xml)의 상품 주소 중 라이카 이름이 든 것만 상세를 읽음 (100개쯤, 1~2초 간격).
    'Auf Lager'만, 가격 EUR. 상태는 설명의 'Zustand: A-' (매장 등급표 A·A-·A/B·B/A·B+·B·B-·B/C·C/B·C+·C·C-, /c/zustandsbeschreibung)"""
    import html as _html
    import requests
    import crawl_engine as _ce
    from condition_grade import GBK_PREFIX
    base = "https://www.gebrauchtkameras.de"
    site = "gebrauchtkameras.de (독일)"
    sess = requests.Session()
    sess.headers["User-Agent"] = _ce.BROWSER_UA
    print(f"\n  📂 gebrauchtkameras.de 크롤링 시작")
    try:
        index = sess.get(f"{base}/sitemap.xml", timeout=30)
        index.raise_for_status()
        maps = [u for u in re.findall(r"<loc>([^<]+)</loc>", index.text) if "sitemap-products" in u]
        urls = []
        for m in maps:
            r = sess.get(m, timeout=30)
            r.raise_for_status()
            urls += re.findall(r"<loc>([^<]+/p/[^<]+)</loc>", r.text)
    except Exception as e:
        raise RuntimeError(f"gebrauchtkameras.de 사이트맵 못 읽음: {e}")  # 빠진 목록이 판매완료로 바뀌지 않게
    urls = [u for u in dict.fromkeys(urls) if GEBRAUCHTKAMERAS_SLUG.search(u.rsplit("/p/", 1)[-1])]
    print(f"    └─ 사이트맵 상품 중 라이카 주소 {len(urls)}개")
    results = []
    for url in urls:
        try:
            page = sess.get(url, timeout=30)
            if page.status_code == 404:
                continue
            page.raise_for_status()
        except Exception as e:
            print(f"    ⚠️ 상세 못 읽음: {url[-50:]} ({e})")
            continue
        h = page.text
        text = re.sub(r"\s+", " ", _html.unescape(re.sub(r"<script.*?</script>|<style.*?</style>|<[^>]+>", " ", h, flags=re.S)))
        time.sleep(random.uniform(1.0, 2.0))
        if "Auf Lager" not in text:
            continue
        title = _html.unescape((re.search(r'<meta property="og:title" content="([^"]+)"', h) or re.search(r"<h1[^>]*>([^<]+)</h1>", h) or [None, ""])[1]).strip()
        title = re.sub(r"\s*[-|]\s*Gebrauchtkameras\.de\s*$", "", title)
        if any(b in title.lower() for b in THIRD_PARTY_BRANDS) or re.search(r"\bf(?:ü|ue)r\s+(?:das\s+|die\s+)?leica\b|panasonic|lumix|\bmetz\b", title, re.I):
            continue  # 'Zeiss … für Leica M'·'Handgriff für Leica D-Lux' 같은 다른 회사 물건
        pr = re.search(r"Verkaufspreis:\s*([\d.]+,\d{2})\s*€", text)
        price = f"€{float(pr.group(1).replace('.', '').replace(',', '.')):,.0f}" if pr else "문의요망"
        z = re.search(r"Zustand\s*:\s*(A\+|AB|BA|BC|CB|[ABCD][+-]?(?:/[ABCD])?)(?![A-Za-z])", text)
        img = re.search(r'<meta property="og:image" content="([^"]+)"', h)
        name = _gebrauchtkameras_name(title)
        results.append({
            "site": site,
            "label": auto_label(name),
            "상품명": name,
            "세대": detect_generation(name),
            "컨디션": GBK_PREFIX + {"AB": "A/B", "BA": "B/A", "BC": "B/C", "CB": "C/B"}.get(z.group(1), z.group(1)) if z else "정보없음",
            "가격": price,
            "통화": "EUR",
            "이미지": _html.unescape(img.group(1)) if img else "",
            "링크": url,
            "품절": False,
            "예약중": False,
            "mount": detect_mount(name),
            "category": detect_category(name, price),
            "brand": detect_brand(name),
        })
    print(f"  ✅ gebrauchtkameras.de 완료: {len(results)}개")
    return results


def _gebrauchtkameras_name(title):
    """'Leica APO-Summicron-M 1:2/90mm ASPH. 6-Bit' → 'Leica APO-Summicron-M 90mm f2 ASPH. 6-Bit'"""
    t = re.sub(r"\b1:(\d+(?:[.,]\d+)?(?:-\d+(?:[.,]\d+)?)?)\s*[/ ]\s*(\d{2,3}(?:-\d{2,3})?)(?:\s*mm)?\b", lambda m: f"{m.group(2)}mm f{m.group(1).replace(',', '.')}", title)
    t = re.sub(r"(\d(?:[.,]\d)?)\s*/\s*(\d{2,3})\s*mm", lambda m: f"{m.group(2)}mm f{m.group(1).replace(',', '.')}", t)
    for de, en in (("schwarz", "black"), ("verchromt", "chrome"), ("silber", "silver"), ("chrom", "chrome"), ("Gehäuse", "body"), ("mit", "with"), ("Handgriff", "grip")):
        t = re.sub(rf"\b{de}\b", en, t, flags=re.I)
    t = re.sub(r"\b(Summicron|Summilux|Elmarit|Elmar|Summaron|Super-Angulon)\s+([RM])\b", r"\1-\2", t)
    t = re.sub(r"\bApo\b", "APO", t)
    t = re.sub(r"\bVario-APO-Elmarit\b", "APO-Vario-Elmarit", t)
    t = re.sub(r"\bMacro-Elmarit-R 100mm f4\b", "Macro-Elmar-R 100mm f4", t)  # 1:4/100은 Macro-Elmar (Elmarit은 2.8)
    t = re.sub(r"\bTrageriemen\b", "strap", t)
    t = re.sub(r"\bWeitwinkelsucher\b", "wide-angle finder", t)
    t = re.sub(r"\s+", " ", t).strip(" ,-")
    return t if re.match(r"(?:leica|leitz)\b", t, re.I) else "Leica " + t


def crawl_mitsubado():
    """三葉堂寫眞機店 (일본 닛포리) - colorme 온라인몰 'leica' 검색 목록 (EUC-JP 정적 HTML, 한 쪽 15개, 70개쯤). SOLD OUT 빼고 판매 중만, 가격 JPY(세금 포함).
    상태는 설명 글(【コンディション】)뿐이라 등급 없이 둠 — 사진 등급 대기열에서 매김"""
    import html as _html
    import requests
    import crawl_engine as _ce
    from ja_normalize import ja_to_en
    base = "https://mitsubado-online.com"
    site = "三葉堂寫眞機店 (일본)"
    sess = requests.Session()
    sess.headers["User-Agent"] = _ce.BROWSER_UA
    results, seen = [], set()
    print(f"\n  📂 三葉堂 크롤링 시작")
    for page_num in range(1, 20):
        try:
            resp = sess.get(f"{base}/", params={"mode": "srh", "keyword": "leica", "page": page_num}, timeout=30)
            resp.raise_for_status()
        except Exception as e:
            raise RuntimeError(f"三葉堂 {page_num}페이지 못 읽음: {e}")  # 빠진 쪽이 판매완료로 바뀌지 않게
        text = resp.content.decode("euc-jp", "ignore")
        cards = re.findall(r'<li class="col col-sm-4 col-lg-4 productlist_list">(.*?)</li>', text, re.S)
        new = 0
        for card in cards:
            pid = re.search(r"\?pid=(\d+)", card)
            if not pid or pid.group(1) in seen:
                continue
            seen.add(pid.group(1))
            new += 1
            if re.search(r"(?i)sold ?out", card):
                continue
            raw = _html.unescape((re.search(r'item_name show">([^<]+)', card) or [None, ""])[1]).strip()
            if not re.search(r"(?i)leica|leitz|ライカ", raw):
                continue
            pr = re.search(r'item_price show">([\d,]+)円', card)
            price = f"¥{int(pr.group(1).replace(',', '')):,}" if pr else "문의요망"
            img = re.search(r'<img src="([^"]+)"', card)
            name = re.sub(r"\s+", " ", ja_to_en(raw)).strip()
            name = re.sub(r"\b(\d(?:\.\d)?)cm\s*f\s?(\d(?:\.\d)?)\b", r"\1cm f\2", name)
            name = name if re.match(r"(?:leica|leitz)\b", name, re.I) else "Leica " + name
            results.append({
                "site": site,
                "label": auto_label(name),
                "상품명": name,
                "세대": detect_generation(name),
                "컨디션": "정보없음",
                "가격": price,
                "통화": "JPY",
                "이미지": _html.unescape(img.group(1)) if img else "",
                "링크": f"{base}/?pid={pid.group(1)}",
                "품절": False,
                "예약중": False,
                "mount": detect_mount(name),
                "category": detect_category(name, price),
                "brand": detect_brand(name),
            })
        print(f"    └─ {page_num}페이지 새 상품 {new}개")
        if not new:
            break
        time.sleep(random.uniform(1.0, 2.0))
    print(f"  ✅ 三葉堂 완료: {len(results)}개")
    return results


AUVIEUXFORMAT_CATEGORIES = ["appareil-photo-argentique-leica", "objectif-argentique-leica"]


def crawl_auvieuxformat():
    """Au Vieux Format (프랑스 생투앙) - WooCommerce 라이카 카메라·렌즈 분류 정적 HTML (각 20개쯤). 'instock'만, 가격 EUR.
    분류에 섞인 Konica Hexar·Hexanon 등은 뺌. 등급 표기 없음 (설명 'état esthétique'는 글뿐)"""
    import html as _html
    import requests
    import crawl_engine as _ce
    base = "https://www.auvieuxformat.com"
    site = "Au Vieux Format (프랑스)"
    sess = requests.Session()
    sess.headers["User-Agent"] = _ce.BROWSER_UA
    results, seen = [], set()
    print(f"\n  📂 Au Vieux Format 크롤링 시작")
    for cat in AUVIEUXFORMAT_CATEGORIES:
        for page_num in range(1, 10):
            url = f"{base}/{cat}/" + (f"page/{page_num}/" if page_num > 1 else "")
            try:
                resp = sess.get(url, timeout=30)
                if resp.status_code == 404 and page_num > 1:
                    break
                resp.raise_for_status()
            except Exception as e:
                raise RuntimeError(f"Au Vieux Format {cat} {page_num}페이지 못 읽음: {e}")  # 빠진 쪽이 판매완료로 바뀌지 않게
            cards = re.findall(r'<li class="(product [^"]+)">(.*?)</li>', resp.text, re.S)
            new = 0
            for cls, card in cards:
                link = re.search(r'href="([^"]+)"', card)
                if not link or link.group(1) in seen:
                    continue
                seen.add(link.group(1))
                new += 1
                if " instock" not in cls:
                    continue
                raw = _html.unescape((re.search(r'loop-product__title">([^<]+)', card) or [None, ""])[1]).strip()
                if any(b in raw.lower() for b in THIRD_PARTY_BRANDS) or re.search(r"(?i)hexar|hexanon|konica|voigtl|zeiss|minolta|canon|nikon", raw):
                    continue
                pr = re.search(r'amount">([\d\s.,]+)', card)
                price = f"€{float(pr.group(1).replace(' ', '').replace('.', '').replace(',', '.')):,.0f}" if pr else "문의요망"
                img = re.search(r'<img[^>]+src="([^"]+)"', card)
                name = _auvieuxformat_name(raw)
                results.append({
                    "site": site,
                    "label": auto_label(name),
                    "상품명": name,
                    "세대": detect_generation(name),
                    "컨디션": "정보없음",
                    "가격": price,
                    "통화": "EUR",
                    "이미지": re.sub(r"-\d+x\d+(\.\w+)$", r"\1", img.group(1)) if img else "",
                    "링크": link.group(1),
                    "품절": False,
                    "예약중": False,
                    "mount": detect_mount(name),
                    "category": detect_category(name, price),
                    "brand": detect_brand(name),
                })
            print(f"    └─ {cat} {page_num}페이지 새 상품 {new}개")
            if not new or "next page-numbers" not in resp.text:
                break
            time.sleep(random.uniform(1.0, 2.0))
    print(f"  ✅ Au Vieux Format 완료: {len(results)}개")
    return results


def _auvieuxformat_name(title):
    """'APO SUMMICRON 2/75 MM ASPH' → 'Leica APO-Summicron 75mm f2 ASPH', 'TELYT R 4/250' → 'Leica Telyt-R 250mm f4', 'LEICA IIIG' → 'Leica IIIg'"""
    t = re.sub(r"(\d(?:[.,]\d)?)\s*/\s*(\d{2,3})\s*(?:MM)?\b", lambda m: f"{m.group(2)}mm f{m.group(1).replace(',', '.')}", title, flags=re.I)
    t = re.sub(r"\b(APO|SUMMICRON|SUMMILUX|SUMMARIT|SUMMARON|ELMARIT|ELMAR|TELYT|NOCTILUX|HEKTOR|ASPH)\b", lambda m: m.group(1) if m.group(1) in ("APO", "ASPH") else m.group(1).capitalize(), t)
    t = re.sub(r"\bAPO (Summicron|Summilux|Telyt|Elmarit)", r"APO-\1", t)
    t = re.sub(r"\b(Summicron|Summilux|Elmarit|Elmar|Telyt|Summaron)\s+([RM])\b", r"\1-\2", t)
    t = re.sub(r"\bLEICA\b", "Leica", t)
    t = re.sub(r"\bLeica (I{1,3})([A-G])\b", lambda m: f"Leica {m.group(1)}{m.group(2).lower()}", t)
    t = re.sub(r"\s+", " ", t).strip(" ,-")
    return t if re.match(r"(?:leica|leitz)\b", t, re.I) else "Leica " + t


FOTOCURATOLO_CATEGORIES = ["catalogo-395-229-Usato-garantito-Fotocamere-usate-Usato-leica.html",
                           "catalogo-463-229-Usato-garantito-Obiettivi-fotografici-usati-Usato-attacco-leica.html"]


def crawl_fotocuratolo():
    """Foto Curatolo (이탈리아) - '보증 중고(Usato garantito)' 라이카 카메라·렌즈 분류에서 'Usato…Leica' 상품 주소를 모아 상세의 JSON-LD로
    이름·재고(InStock)·가격 EUR을 읽음 (몇 개뿐). 상태는 설명 글의 이탈리아어 말투 (IT: …)"""
    import html as _html
    import json as _json
    import requests
    import crawl_engine as _ce
    from condition_grade import it_condition
    base = "https://www.fotocuratolo.it"
    site = "Foto Curatolo (이탈리아)"
    sess = requests.Session()
    sess.headers["User-Agent"] = _ce.BROWSER_UA
    print(f"\n  📂 Foto Curatolo 크롤링 시작")
    links = []
    for cat in FOTOCURATOLO_CATEGORIES:
        try:
            resp = sess.get(f"{base}/{cat}", timeout=30)
            resp.raise_for_status()
        except Exception as e:
            raise RuntimeError(f"Foto Curatolo 분류 못 읽음: {e}")  # 빠진 목록이 판매완료로 바뀌지 않게
        for pid, card in re.findall(r"<article class='default_height Singlearticle[^']*' id=\"article(\d+)\">(.*?)</article>", resp.text, re.S):
            href = re.search(r'href="(\d+-Usato[^"]*\.html)"', card)
            if href and re.search(r"(?i)leica|leitz", href.group(1)):
                links.append(f"{base}/{href.group(1)}")
        time.sleep(random.uniform(1.0, 2.0))
    results = []
    for link in dict.fromkeys(links):
        try:
            page = sess.get(link, timeout=30)
            page.raise_for_status()
        except Exception as e:
            print(f"    ⚠️ 상세 못 읽음: {link[-50:]} ({e})")
            continue
        block = re.search(r'<script type="application/ld\+json">(.*?)</script>', page.text, re.S)
        try:
            data = _json.loads(block.group(1)) if block else {}
        except ValueError:
            data = {}
        offer = data.get("offers") or {}
        time.sleep(random.uniform(1.0, 2.0))
        if "InStock" not in str(offer.get("availability") or ""):
            continue
        raw = _html.unescape(str(data.get("name") or "")).strip()
        name = re.sub(r"^Usato\s+", "", raw, flags=re.I)
        name = re.sub(r"\+?\s*\bOTTICA\b", " with", name)
        name = re.sub(r"\+?\s*CUSTODIA IN PELLE ORIGINALE", " leather case", name, flags=re.I)
        name = re.sub(r"(\d{2,3})MM\b", r"\1mm", name)
        name = re.sub(r"\bF\.?\s?(\d+(?:[.,]\d+)?)\b", lambda m: "f" + m.group(1).replace(",", "."), name)
        name = re.sub(r"\((\d{2}) (\d{3})\)", r"\1\2", name)
        name = re.sub(r"\s+", " ", name).strip(" .")
        try:
            price = f"€{float(offer.get('price')):,.0f}"
        except (TypeError, ValueError):
            price = "문의요망"
        cond = it_condition(_html.unescape(str(data.get("description") or "")))
        results.append({
            "site": site,
            "label": auto_label(name),
            "상품명": name,
            "세대": detect_generation(name),
            "컨디션": cond or "정보없음",
            "가격": price,
            "통화": "EUR",
            "이미지": str(data.get("image") or ""),
            "링크": link,
            "품절": False,
            "예약중": False,
            "mount": detect_mount(name),
            "category": detect_category(name, price),
            "brand": detect_brand(name),
        })
    print(f"  ✅ Foto Curatolo 완료: {len(results)}개")
    return results


def crawl_mpex():
    """Midwest Photo (미국 콜럼버스, mpex.com) - Magento. robots.txt가 검색·'?' 주소를 막아 사이트맵(sitemap-1-1·1-2.xml, 1만 개)에서
    'used-…leica/summicron…' 상품 주소만 골라 상세를 읽음 (몇 개뿐). 'In stock'만, 가격 USD. 상태는 설명 첫 단어 (LIKE NEW·EXCELLENT·GOOD·FAIR)"""
    import html as _html
    import requests
    import crawl_engine as _ce
    from condition_grade import MPEX_PREFIX
    base = "https://mpex.com"
    site = "Midwest Photo (미국)"
    sess = requests.Session()
    sess.headers["User-Agent"] = _ce.BROWSER_UA
    print(f"\n  📂 Midwest Photo 크롤링 시작")
    urls = []
    try:
        index = sess.get(f"{base}/sitemap/sitemap.xml", timeout=60)
        index.raise_for_status()
        for m in re.findall(r"<loc>([^<]+)</loc>", index.text):
            r = sess.get(m, timeout=90)
            r.raise_for_status()
            urls += re.findall(r"<loc>([^<]+)</loc>", r.text)
            time.sleep(2)
    except Exception as e:
        raise RuntimeError(f"Midwest Photo 사이트맵 못 읽음: {e}")  # 빠진 목록이 판매완료로 바뀌지 않게
    urls = [u for u in dict.fromkeys(urls) if re.search(r"^https://mpex\.com/used-[^/]*(?:leica|leitz|summicron|summilux|summaron|summarit|elmarit|elmar|noctilux)[^/]*\.html$", u, re.I)
            and not re.search(r"(?i)blackmagic|sigma|panasonic|lumix|l-mount|voigtl|zeiss|7artisans|ttartisan", u)]
    print(f"    └─ 사이트맵 중고 라이카 주소 {len(urls)}개")
    results = []
    for url in urls:
        try:
            page = sess.get(url, timeout=30)
            if page.status_code == 404:
                continue
            page.raise_for_status()
        except Exception as e:
            print(f"    ⚠️ 상세 못 읽음: {url[-50:]} ({e})")
            continue
        time.sleep(random.uniform(1.0, 2.0))
        h = page.text
        text = re.sub(r"\s+", " ", _html.unescape(re.sub(r"<script.*?</script>|<style.*?</style>|<[^>]+>", " ", h, flags=re.S)))
        if not re.search(r"\bIn stock\b", text, re.I) or re.search(r"\bOut of stock\b", text, re.I):
            continue
        title = _html.unescape((re.search(r"<title>([^<]+)</title>", h) or [None, ""])[1]).strip()
        name = re.sub(r"^Used\s+", "", title, flags=re.I)
        name = re.sub(r"\bf/(\d+(?:\.\d+)?)", r"f\1", name)
        name = re.sub(r"\bM Mount\b", "M", name)
        pr = re.search(r"\$([\d,]+\.\d{2})", text)
        price = f"${float(pr.group(1).replace(',', '')):,.0f}" if pr else "문의요망"
        g = re.search(r"Description\s+(LIKE NEW|EXCELLENT\s?\+?|EXCELLENT|GOOD|FAIR|POOR)\b", text)
        img = re.search(r'og:image" content="([^"]+)"', h)
        results.append({
            "site": site,
            "label": auto_label(name),
            "상품명": name,
            "세대": detect_generation(name),
            "컨디션": MPEX_PREFIX + g.group(1).strip().lower() if g else "정보없음",
            "가격": price,
            "통화": "USD",
            "이미지": img.group(1) if img else "",
            "링크": url,
            "품절": False,
            "예약중": False,
            "mount": detect_mount(name),
            "category": detect_category(name, price),
            "brand": detect_brand(name),
        })
    print(f"  ✅ Midwest Photo 완료: {len(results)}개")
    return results


def crawl_2ndbase():
    """2nd BASE (일본, 三宝カメラ 계열) - MakeShop '[LEICA M]' 분류 /shopbrand/ct46/ (EUC-JP 정적 HTML, 10개 안팎). SOLD OUT 빼고 판매 중만, 가격 JPY(세금 포함).
    등급은 제목 앞 '【AB】' (일본 매장 공통 대응 _JP)"""
    import html as _html
    import requests
    import crawl_engine as _ce
    base = "https://www.2ndbase.jp"
    site = "2nd BASE (일본)"
    sess = requests.Session()
    sess.headers["User-Agent"] = _ce.BROWSER_UA
    results, seen = [], set()
    print(f"\n  📂 2nd BASE 크롤링 시작")
    for page_num in range(1, 20):
        try:
            resp = sess.get(f"{base}/shopbrand/ct46/page{page_num}/order/", timeout=30)
            resp.raise_for_status()
        except Exception as e:
            raise RuntimeError(f"2nd BASE {page_num}페이지 못 읽음: {e}")  # 빠진 쪽이 판매완료로 바뀌지 않게
        text = resp.content.decode("euc-jp", "ignore")
        new = 0
        for card in re.findall(r'<div class="innerBox">(.*?)</li>', text, re.S):
            m = re.search(r'<p class="name"><a href="(/shopdetail/(\d+)/[^"]*)">([^<]+)</a>', card)
            if not m or m.group(2) in seen:
                continue
            seen.add(m.group(2))
            new += 1
            if re.search(r"(?i)sold ?out|売切|品切", card):
                continue
            raw = _html.unescape(m.group(3)).strip()
            g = re.match(r"【([A-Z+\-]{1,3})】\s*", raw)
            name = re.sub(r"\s+", " ", raw[g.end():] if g else raw).strip()
            name = re.sub(r"\bF(\d+(?:\.\d+)?)\b", r"f\1", name)
            name = name if re.match(r"(?:leica|leitz)\b", name, re.I) else "Leica " + name
            pr = re.search(r"([\d,]+)円", card)
            price = f"¥{int(pr.group(1).replace(',', '')):,}" if pr else "문의요망"
            img = re.search(r'<img[^>]+src="([^"]+)"', card)
            results.append({
                "site": site,
                "label": auto_label(name),
                "상품명": name,
                "세대": detect_generation(name),
                "컨디션": g.group(1) if g else "정보없음",
                "가격": price,
                "통화": "JPY",
                "이미지": img.group(1) if img else "",
                "링크": base + m.group(1).split("/ct46/")[0] + "/",
                "품절": False,
                "예약중": False,
                "mount": detect_mount(name),
                "category": detect_category(name, price),
                "brand": detect_brand(name),
            })
        print(f"    └─ {page_num}페이지 새 상품 {new}개")
        if not new or f"page{page_num + 1}/" not in text:
            break
        time.sleep(random.uniform(1.0, 2.0))
    print(f"  ✅ 2nd BASE 완료: {len(results)}개")
    return results


def crawl_scandinavianphoto():
    """Scandinavian Photo (스웨덴) - 중고 목록 /begagnat?p_brand_name=Leica 화면에 실린 상품 JSON(window.CURRENT_PAGE).
    중고(begagnad)·전시품(demo)·개봉품(uppackad) 모두 Leica만, 가격 SEK(부가세 포함). robots.txt Crawl-delay 10이라 쪽마다 10초 쉼.
    등급은 카드 문구 'A-skick'·'B-skick'·'C-skick'·'Tidigare demoprodukt' (사진은 모두 새 상품 사진이라 사진 평가 없음)"""
    import requests
    import crawl_engine as _ce
    from condition_grade import SCANPHOTO_PREFIX
    base = "https://www.scandinavianphoto.se"
    site = "Scandinavian Photo (스웨덴)"
    sess = requests.Session()
    sess.headers["User-Agent"] = _ce.BROWSER_UA
    results, seen = [], set()
    print(f"\n  📂 Scandinavian Photo 크롤링 시작")
    page_num, pages = 1, 1
    while page_num <= min(pages, 10):
        try:
            resp = sess.get(f"{base}/begagnat", params={"p_brand_name": "Leica", "page": page_num}, timeout=30)
            resp.raise_for_status()
            text = resp.text
            start = text.index("window.CURRENT_PAGE") 
            start = text.index("{", start)
            data, _ = json.JSONDecoder().raw_decode(text[start:])
            block = data["products"]
        except Exception as e:
            raise RuntimeError(f"Scandinavian Photo {page_num}페이지 못 읽음: {e}")  # 빠진 쪽이 판매완료로 바뀌지 않게
        pages = int(block.get("pagesCount") or 1)
        for p in block.get("products") or []:
            url = p.get("url") or ""
            if not url or url in seen or str(p.get("brand") or p.get("brandName") or "").lower() != "leica":
                continue
            seen.add(url)
            raw = re.sub(r"\s+", " ", p.get("displayName") or "").strip()
            name = re.sub(r"\s*\((?:begagna[dt]|demo|uppackad|använd)\)\s*", " ", raw, flags=re.I)
            name = re.sub(r"(\d),(\d)", r"\1.\2", name).strip()  # 'f/1,4' → 'f/1.4'
            name = name if re.match(r"(?:leica|leitz)\b", name, re.I) else "Leica " + name
            usps = [str(u) for u in (p.get("uspList") or [])]
            level = next((u.strip() for u in usps if re.match(r"\s*[A-D]-skick", u, re.I)), None)
            if not level and (p.get("isDemo") or re.search(r"(?i)demo", raw + " ".join(usps))):
                level = "demo"
            if not level and re.search(r"(?i)uppackad", raw):
                level = "uppackad"
            price_v = (p.get("price") or {}).get("currentInclVat")
            price = f"SEK {float(price_v):,.0f}" if price_v else "문의요망"
            imgs = p.get("imageUrls") or []
            img = imgs[0].get("url", "") if imgs else ""
            sold = bool(p.get("isNotBuyable")) or str(p.get("stockLevel") or "").lower() in ("none", "outofstock", "soldout")
            results.append({
                "site": site,
                "label": auto_label(name),
                "상품명": name,
                "세대": detect_generation(name),
                "컨디션": SCANPHOTO_PREFIX + level if level else "정보없음",
                "가격": price,
                "통화": "SEK",
                "이미지": (base + img) if img.startswith("/") else img,
                "링크": base + url,
                "품절": sold,
                "예약중": False,
                "mount": detect_mount(name),
                "category": detect_category(name, price),
                "brand": detect_brand(name),
            })
        print(f"    └─ {page_num}/{pages}페이지 누적 {len(results)}개")
        page_num += 1
        if page_num <= min(pages, 10):
            time.sleep(10)
    print(f"  ✅ Scandinavian Photo 완료: {len(results)}개")
    return results


def _itscamera_name(title):
    """잇츠카메라 제목 '[중고]Leica 라이카 M10-R(m10r) Black 블랙 AAA급 중고카메라매입 잇츠카메라' → 'Leica M10-R Black'
    (머리말·가게 이름·'중고카메라매입' 같은 검색용 말·한글 중복 이름·등급 빼기). 라이카가 아니면 빈 이름"""
    t = re.sub(r"\[[^\]]*\]\s*", " ", title)
    t = re.sub(r"\([^)]*(?:라이카|정품|m10r|q2리포터|렌즈미포함|바디단품)[^)]*\)", " ", t, flags=re.I)
    t = re.sub(r"\S*(?:잇츠카메라|매입)\S*", " ", t)
    t = re.sub(r"\b(?:S|A{1,3}|B)급", " ", t)
    t = re.sub(r"라이카\s*(?:중고)?\s*(?:카메라|렌즈)?", " ", t)
    t = re.sub(r"\s(?:블랙|실버|디룩스\s*\d*|미러리스카메라|렌즈교환식|고성능카메라|방수 가능 아웃도어|바디만|본체)(?=\s|$)", " ", t)
    t = re.sub(r"\(\s*\)", " ", t)
    t = re.sub(r"\s+", " ", t).strip()
    if not re.search(r"(?i)\b(?:leica|leitz)\b", t):
        return ""
    t = re.sub(r"(?i)^.*?\b(leica|leitz)\b", r"\1", t)
    t = re.sub(r"(?i)\bnew\s+x\b", "X", t)  # 'NEW X (TYP113)'은 모델 이름 (신품 아님)
    return t


def crawl_itscamera():
    """잇츠카메라 (한국) - MakeShop 중고 분류 4곳의 '라이카' 하위 분류 (미러리스·컴팩트·렌즈·기타, 30여 개). 정적 HTML(UTF-8).
    가격은 판매가(price02, 할인가), 품절은 가격 대신 '품절' 표시. 등급은 제목의 'AAA급' 같은 말뿐이라 거의 없음"""
    import html as _html
    import requests
    import crawl_engine as _ce
    from condition_grade import ITSCAMERA_PREFIX
    base = "http://www.itscamera.com"
    site = "잇츠카메라"
    sess = requests.Session()
    sess.headers["User-Agent"] = _ce.BROWSER_UA
    results, seen = [], set()
    print(f"\n  📂 잇츠카메라 크롤링 시작")
    for xcode, mcode in [("003", "009"), ("004", "010"), ("002", "014"), ("012", "008")]:
        for page_num in range(1, 15):
            try:
                resp = sess.get(f"{base}/shop/shopbrand.html", params={"type": "M", "xcode": xcode, "mcode": mcode,
                                                                       "sort": "order", "page": page_num}, timeout=30)
                resp.raise_for_status()
            except Exception as e:
                raise RuntimeError(f"잇츠카메라 {xcode}-{mcode} {page_num}페이지 못 읽음: {e}")  # 빠진 쪽이 판매완료로 바뀌지 않게
            text = resp.content.decode("utf-8", "ignore")
            new = 0
            for box in re.findall(r'<div class="item_box">(.*?)<!-- //item_box -->', text, re.S):
                u = re.search(r'href="/shop/shopdetail\.html\?branduid=(\d+)', box)
                nm = re.search(r'<li class="name">(.*?)</li>', box, re.S)
                if not u or not nm or u.group(1) in seen:
                    continue
                seen.add(u.group(1))
                new += 1
                raw = _html.unescape(re.sub(r"<[^>]+>|\s+", " ", nm.group(1))).strip()
                name = _itscamera_name(raw)
                if not name:
                    continue
                if "새상품" in raw:
                    name += " 신품"  # 등급(N)은 제목의 '신품'으로 매김
                body = re.sub(r"<!--.*?-->", "", box, flags=re.S)
                sold = bool(re.search(r"품절|soldout", body, re.I))
                pr = re.search(r'class="price02">([\d,]+)원', box) or re.search(r'class="price01">([\d,]+)원', box)
                price = f"{int(pr.group(1).replace(',', '')):,}원" if pr else "문의요망"
                g = re.search(r"\b(S|A{1,3}|B)급", raw)
                img = re.search(r'<img class="MS_prod_img_m" src="([^"]+)"', box)
                img = img.group(1) if img else ""
                results.append({
                    "site": site,
                    "label": auto_label(name),
                    "상품명": name,
                    "세대": detect_generation(name),
                    "컨디션": ITSCAMERA_PREFIX + g.group(1) if g else "정보없음",
                    "가격": price,
                    "통화": "KRW",
                    "이미지": (base + img) if img.startswith("/") else img,
                    "링크": f"{base}/shop/shopdetail.html?branduid={u.group(1)}",
                    "품절": sold,
                    "예약중": False,
                    "mount": detect_mount(name),
                    "category": detect_category(name, price),
                    "brand": detect_brand(name),
                })
            if not new or f"page={page_num + 1}" not in text:
                break
            time.sleep(random.uniform(1.0, 2.0))
    print(f"  ✅ 잇츠카메라 완료: {len(results)}개")
    return results


def _listed_est(item):
    """매장이 준 게시일(Shopify) 또는 사진 주소에 남은 올린 날짜 → 게시 추정일 ('2024-12'·'2026-10-15'), 모르면 빈 문자열"""
    from listing_date import listed_of
    return listed_of(item) or ""


def _shopify_listed(p):
    """Shopify 상품의 등록일 (created_at '2025-03-04T10:00:00-05:00' → '2025-03-04'), 없으면 빈 문자열"""
    return str(p.get("created_at") or p.get("published_at") or "")[:10]


DETAIL_SEEN = "정보없음 (상세 봄)"  # 상세 화면을 봤는데 상태 표기가 없던 매물 — 다시 열지 않음


def _fill_detail_conditions(site, results, read_detail, limit=80):
    """목록에 상태 표기가 없는 매장: 상세 화면의 상태를 처음 본 매물만 읽고(한 번에 limit개, 1~2초 간격),
    전에 읽은 것은 이전 결과(data/raw/results.json)에서 다시 씀. 액세서리는 읽지 않음. read_detail(url) → 컨디션 문자열 또는 None"""
    known = {}
    try:
        with open("data/raw/results.json", encoding="utf-8") as f:
            known = {r["링크"]: r.get("컨디션") for r in json.load(f) if r.get("site") == site}
    except (OSError, ValueError):
        pass
    fetched = found = 0
    for r in results:
        if r.get("category") == "Accessory" or r.get("컨디션") not in (None, "", "정보없음"):
            continue
        prev = known.get(r["링크"])
        if prev and prev != "정보없음":
            r["컨디션"] = prev
            continue
        if fetched >= limit:
            continue
        fetched += 1
        try:
            cond = read_detail(r["링크"])
        except Exception as e:
            print(f"    ⚠️ 상세 못 읽음: {r['링크'][-50:]} ({e})")
            continue
        r["컨디션"] = cond or DETAIL_SEEN
        found += bool(cond)
        time.sleep(random.uniform(1.0, 2.0))
    print(f"    └─ 상세 상태: 새로 {fetched}개 열어 {found}개 찾음")


def crawl_fujikoshi():
    """富士越カメラ (일본) - 라이카 정규 판매점 MakeShop 중고 라이카 분류(/shopbrand/006/X/, EUC-JP 정적 HTML, 50개씩 6쪽쯤 260개).
    목록에 있는 것은 판매 중, 가격 JPY(세금 포함). 등급은 상세 화면 '■程度 極上品'(新品＞新同品＞極上品＞美品＞上程度＞中程度＞ジャンク)뿐이라
    처음 본 매물만 상세를 읽고 전에 읽은 등급은 이전 결과에서 다시 씀 (액세서리는 안 읽음). robots.txt 없음(404)"""
    import html as _html
    import requests
    import crawl_engine as _ce
    from condition_grade import FUJIKOSHI_PREFIX
    base = "https://www.fujikoshi-camera.com"
    sess = requests.Session()
    sess.headers["User-Agent"] = _ce.BROWSER_UA
    site = "富士越カメラ (일본)"
    known = {}
    try:
        with open("data/raw/results.json", encoding="utf-8") as f:
            known = {r["링크"]: (r.get("컨디션"), r.get("이미지")) for r in json.load(f) if r.get("site") == site}
    except (OSError, ValueError):
        pass
    results, seen = [], set()
    print(f"\n  📂 富士越カメラ 크롤링 시작 (이전 등급 {len(known)}개)")
    for page_num in range(1, 30):
        try:
            resp = sess.get(f"{base}/shopbrand/006/X/page{page_num}/order/", timeout=30)
            resp.raise_for_status()
        except Exception as e:
            raise RuntimeError(f"富士越カメラ {page_num}페이지 못 읽음: {e}")  # 빠진 쪽이 판매완료로 바뀌지 않게
        text = resp.content.decode("euc-jp", "ignore")
        new = 0
        for m in re.finditer(r'<a href="(/shopdetail/(\d+)/006/X/page\d+/order/)">\s*([^<]+)</a>([\s\S]{0,700}?)([\d,]+)円', text):
            link = base + m.group(1)
            if link in seen:
                continue
            seen.add(link)
            new += 1
            raw = re.sub(r"\s+", " ", _html.unescape(m.group(3)).replace("　", " ")).strip()
            if any(b2 in raw.lower() for b2 in THIRD_PARTY_BRANDS) or re.search(
                    r"Konica|コニカ|Voigtl|フォクトレンダー|Rayqual|レイクォール|Zeiss|ツァイス|Minolta|ミノルタ|TTArtisan|銘匠|腕時計", raw, re.I):
                continue  # 라이카 분류에 섞인 다른 회사 렌즈·어댑터
            name = _fujikoshi_name(raw)
            price = f"¥{int(m.group(5).replace(',', '')):,}"
            img_url = re.search(r'(https://[^"\s]+itemimages/[^"\s]*' + m.group(2) + r'[^"\s]*\.jpg)', text)
            results.append({
                "site": site,
                "label": auto_label(name),
                "상품명": name,
                "세대": detect_generation(name),
                "컨디션": "정보없음",
                "가격": price,
                "통화": "JPY",
                "이미지": img_url.group(1) if img_url else "",
                "링크": link,
                "품절": False,
                "예약중": False,
                "mount": detect_mount(name),
                "category": detect_category(name, price),
                "brand": detect_brand(name),
            })
        print(f"    └─ {page_num}페이지 새 상품 {new}개")
        if not new:
            break
        time.sleep(random.uniform(1.0, 2.0))
    read = 0
    for r in results:
        prev_cond, prev_img = known.get(r["링크"]) or (None, None)
        if prev_cond and prev_cond != "정보없음":
            r["컨디션"] = prev_cond
            r["이미지"] = prev_img or r["이미지"]
            continue
        if r["category"] == "Accessory" or read >= 150:
            continue
        read += 1
        try:
            page = sess.get(r["링크"], timeout=30).content.decode("euc-jp", "ignore")
            g = re.search(r"■程度\s*(?:<[^>]+>\s*)*(新品|新同品|極上品|美品|上程度|中程度|ジャンク)", page)
            if g:
                r["컨디션"] = FUJIKOSHI_PREFIX + g.group(1)
            # 목록 사진은 100px 썸네일 → 상세의 큰 사진(800px, 'itemimages/<상품번호>_xxxx.jpg')
            big = re.search(r'(https://[^"\s]+/itemimages/' + r["링크"].split("/shopdetail/")[1][:12] + r'_\w+\.jpg)', page)
            if big:
                r["이미지"] = big.group(1)
        except Exception as e:
            print(f"    ⚠️ 상세 못 읽음: {r['링크'][-40:]} ({e})")
        time.sleep(random.uniform(1.0, 2.0))
    print(f"  ✅ 富士越カメラ 완료: {len(results)}개 (상세 새로 {read}개)")
    return results


def _fujikoshi_name(title):
    """富士越カメラ 제목 다듬기: 'Leica(ライカ)　SUMMILUX-M　35mm　F1.4　ASPH.　シルバー　481万台　(NL-5446)'
    → 'Leica Summilux-M 35mm f1.4 ASPH. silver' ('481万台' 일련번호 대·관리 번호·【委託】 빼기)"""
    from ja_normalize import ja_to_en
    t = re.sub(r"【[^】]*】|\((?:N[A-Z]{1,2}|0NAC|NAC)-?\d+\)|\s\d{2,4}万台|\(ライカ\)|\(Leica\)", " ", title)
    t = re.sub(r"\s+", " ", ja_to_en(t)).strip()
    t = re.sub(r"^(?:leica|ライカ)\s*", "", t, flags=re.I)
    t = re.sub(r"\bF(\d+(?:\.\d+)?)\b", r"f\1", t)
    t = re.sub(r"\bM6TTL\b", "M6 TTL", t, flags=re.I)
    t = re.sub(r"\bVARIO-ELMARIT-T\b", "Vario-Elmar-T", t, flags=re.I)  # 매장 오기 (T 마운트 18-56은 Vario-Elmar-T)
    return t if re.match(r"(?:leica|leitz)\b", t, re.I) else "Leica " + t


OHBAYASHI_CATEGORIES = ["ct1021", "ct1056", "ct1008", "ct1044", "ct921"]  # 중고 라이카: 렌즈·필름·디지털·콤팩트·액세서리


def crawl_ohbayashi():
    """カメラの大林 (일본) - MakeShop 새 화면 중고 라이카 분류 5곳(/view/category/ct…, 정적 HTML, 한 쪽에 다 나옴 — 70개쯤).
    목록에 있으면 판매 중, 가격 JPY(세금 포함). 등급은 상세 화면 '商品の詳細' 표의 程度(A·AB·B·C)뿐이라 처음 본 매물만 상세를 읽고
    전에 읽은 등급은 이전 결과에서 다시 씀. robots.txt 없음(404)"""
    import html as _html
    import requests
    import crawl_engine as _ce
    from condition_grade import OHBAYASHI_PREFIX
    base = "https://www.camera-no-ohbayashi.co.jp"
    site = "カメラの大林 (일본)"
    sess = requests.Session()
    sess.headers["User-Agent"] = _ce.BROWSER_UA
    known = {}
    try:
        with open("data/raw/results.json", encoding="utf-8") as f:
            known = {r["링크"]: r.get("컨디션") for r in json.load(f) if r.get("site") == site}
    except (OSError, ValueError):
        pass
    results, seen = [], set()
    print(f"\n  📂 カメラの大林 크롤링 시작 (이전 등급 {len(known)}개)")
    for cat in OHBAYASHI_CATEGORIES:
        for page_num in range(1, 20):
            try:
                resp = sess.get(f"{base}/view/category/{cat}", params={"page": page_num} if page_num > 1 else None, timeout=30)
                resp.raise_for_status()
            except Exception as e:
                raise RuntimeError(f"カメラの大林 {cat} {page_num}페이지 못 읽음: {e}")  # 빠진 쪽이 판매완료로 바뀌지 않게
            new = 0
            for card in resp.text.split('<div class="item-list-image">')[1:]:
                m = re.search(r'<p class="item-name"><a href="(/view/item/(\d+))[^"]*">([^<]+)</a>', card)
                if not m or base + m.group(1) in seen:
                    continue
                link = base + m.group(1)
                seen.add(link)
                new += 1
                raw = _html.unescape(m.group(3)).replace("　", " ").strip()
                if re.search(r"Konica|コニカ|Voigtl|フォクトレンダー|Zeiss|ツァイス|ミノルタ|シグマ|Sigma|Panasonic|パナソニック", raw, re.I):
                    continue  # 라이카 분류에 섞인 다른 회사 렌즈·어댑터 (L 마운트 공용 렌즈 등)
                name = _ohbayashi_name(raw)
                pr = re.search(r'class="price">￥([\d,]+)', card)
                price = f"¥{int(pr.group(1).replace(',', '')):,}" if pr else "문의요망"
                img = re.search(r'<img src="([^"]+itemimages/[^"]+)"', card)
                results.append({
                    "site": site,
                    "label": auto_label(name),
                    "상품명": name,
                    "세대": detect_generation(name),
                    "컨디션": "정보없음",
                    "가격": price,
                    "통화": "JPY",
                    "이미지": img.group(1) if img else "",
                    "링크": link,
                    "품절": False,
                    "예약중": False,
                    "mount": detect_mount(name),
                    "category": "Accessory" if cat == "ct921" else detect_category(name, price),
                    "brand": detect_brand(name),
                })
            print(f"    └─ {cat} {page_num}페이지 새 상품 {new}개")
            if not new:
                break
            time.sleep(random.uniform(1.0, 2.0))
    read = 0
    for r in results:
        prev = known.get(r["링크"])
        if prev and prev != "정보없음":
            r["컨디션"] = prev
            continue
        if r["category"] == "Accessory" or read >= 120:
            continue
        read += 1
        try:
            page = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", sess.get(r["링크"], timeout=30).text))
            g = re.search(r"程度 保証 ケース フード 取説 元箱 備考 (AB|A|B|C) ", page)
            r["컨디션"] = OHBAYASHI_PREFIX + g.group(1) if g else "정보없음 (상세 봄)"  # 표가 깨진('#REF!') 상품은 다시 안 엶
        except Exception as e:
            print(f"    ⚠️ 상세 못 읽음: {r['링크'][-30:]} ({e})")
        time.sleep(random.uniform(1.0, 2.0))
    print(f"  ✅ カメラの大林 완료: {len(results)}개 (상세 새로 {read}개)")
    return results


def _ohbayashi_name(title):
    """カメラの大林 제목 다듬기: 'ライカ APO ズミクロンM 90mm F2 ASPH【中古管理番号：SW0198】' → 'Leica APO Summicron-M 90mm f2 ASPH'"""
    import unicodedata
    from ja_normalize import ja_to_en
    t = unicodedata.normalize("NFKC", re.sub(r"【[^】]*】", " ", title))  # 반각 가타카나 'ｽﾞﾐｸﾛﾝ'·전각 숫자 '９０mm'
    t = re.sub(r"\s+", " ", ja_to_en(t)).strip()
    t = re.sub(r"^(?:leica|ライカ)\s*", "", t, flags=re.I)
    t = re.sub(r"\bF(\d+(?:\.\d+)?)\b", r"f\1", t)
    t = re.sub(r"(\d{2,3})mm(\d(?:\.\d)?)\b|(\d(?:\.\d)?cm)(\d(?:\.\d)?)\b",
               lambda m: f"{m.group(1)}mm f{m.group(2)}" if m.group(1) else f"{m.group(3)} f{m.group(4)}", t)  # '90mm2.8'·'3.5cm3.5'
    t = re.sub(r"-\s+(?=[A-Z])", "-", t)  # 'Vario- Elmarit'
    t = re.sub(r"\b(I{1,3}[a-g]?)Body\b", r"\1 Body", t).replace("ゾフォート", "Sofort ")
    t = re.sub(r"\b(Summicron|Summaron|Elmar|Summitar|Hektor)\s+L\b", r"\1-L", t)  # 'Summicron L 50mm' (L 마운트)
    return t if re.match(r"(?:leica|leitz)\b", t, re.I) else "Leica " + t


USEDPHOTO_SKIP_CATEGORIES = {"Werbeartikel", "Ferngläser", "Aufsteckblitz / Blitz"}  # 판촉물·쌍안경·플래시


def crawl_usedphoto():
    """used-photo.de (독일 말스펠트) - WooCommerce 상품 API(Store API)에서 'leica'·'leitz' 검색 (100개씩, 합쳐 120개쯤).
    재고 있는 것만, 가격 EUR. 등급 표기가 없어 설명 글의 독일어 말투로 ('near mint'·'leichte Gebrauchsspuren' → DE: …).
    robots.txt는 장바구니·로그만 막음"""
    import html as _html
    import requests
    import crawl_engine as _ce
    from condition_grade import de_condition
    base = "https://www.used-photo.de"
    sess = requests.Session()
    sess.headers["User-Agent"] = _ce.BROWSER_UA
    results, seen = [], set()
    print(f"\n  📂 used-photo.de 크롤링 시작")
    for term in ("leica", "leitz"):
        for page_num in range(1, 10):
            try:
                resp = sess.get(f"{base}/wp-json/wc/store/v1/products", params={"search": term, "per_page": 100, "page": page_num}, timeout=30)
                resp.raise_for_status()
                products = resp.json()
            except Exception as e:
                raise RuntimeError(f"used-photo.de {term} {page_num}페이지 못 읽음: {e}")  # 빠진 쪽이 판매완료로 바뀌지 않게
            for p in products:
                link = p.get("permalink") or ""
                title = re.sub(r"\s+", " ", _html.unescape(p.get("name") or "")).strip()
                cats = {_html.unescape(c.get("name") or "") for c in p.get("categories") or []}
                if not link or link in seen or not p.get("is_in_stock") or cats & USEDPHOTO_SKIP_CATEGORIES:
                    continue
                if not re.search(r"\b(?:leica|leitz)", title, re.I) or any(b2 in title.lower() for b2 in THIRD_PARTY_BRANDS) or re.search(
                        r"Voigtl|Zeiss|Sigma|Panasonic|Lumix|Tamron|Hasselblad|Minolta|Rokkor", title, re.I):
                    continue
                seen.add(link)
                name = _usedphoto_name(title)
                prices = p.get("prices") or {}
                price = f"€{int(prices['price']) / 10 ** int(prices.get('currency_minor_unit', 2)):,.0f}" if prices.get("price") else "문의요망"
                desc = _html.unescape((p.get("short_description") or "") + " " + (p.get("description") or ""))
                results.append({
                    "site": "used-photo.de (독일)",
                    "label": auto_label(name),
                    "상품명": name,
                    "세대": detect_generation(name),
                    "컨디션": de_condition(desc) or "정보없음",
                    "가격": price,
                    "통화": "EUR",
                    "이미지": p["images"][0].get("src", "") if p.get("images") else "",
                    "링크": link,
                    "품절": False,
                    "예약중": False,
                    "mount": detect_mount(name),
                    "category": detect_category(name, price),
                    "brand": detect_brand(name),
                })
            print(f"    └─ {term} {page_num}페이지 {len(products)}개")
            if len(products) < 100:
                break
            time.sleep(random.uniform(1.0, 2.0))
    print(f"  ✅ used-photo.de 완료: {len(results)}개")
    return results


def _usedphoto_name(title):
    """used-photo.de 제목 다듬기: 'Leica Prime – Leica APO-Summicron-M 35mm f2 ASPH. | 11699' → 'Leica APO-Summicron-M 35mm f2 ASPH. 11699',
    'LEICA 20002 – Leica M10-R' → 'Leica M10-R 20002', 'f/1,7' → 'f1.7', 광고 꼬리('– Vom Erstbesitzer') 빼기"""
    t = title.replace("|", " ")
    parts = [x.strip() for x in re.split(r"\s+[\u2013\u2014-]\s+", t)]
    main = next((x for x in parts if re.search(r"\b(?:M\d|Q\d?|SL\d?|CL|TL|X\d?|R\d|summi|elmar|nocti|elmarit|leicaflex|minilux|D-?Lux|Sofort)", x, re.I)
                 and not re.match(r"^(?:leica|LEICA)\s+\d{5}$", x)), parts[0])
    code = re.search(r"\b(1\d{4}|2\d{4})\b", t)
    name = main + (f" {code.group(1)}" if code and code.group(1) not in main else "")
    name = re.sub(r"f/?\s?(\d),(\d)", r"f\1.\2", name)
    name = re.sub(r"\bf/(\d)", r"f\1", name)
    name = re.sub(r"^LEICA\b", "Leica", re.sub(r"\s+", " ", name)).strip()
    if re.search(r"Tasche|Werbeaufsteller|Display|Gurt|Case\b", name, re.I):
        name += " accessory"  # 가방·매장 진열대·스트랩 (렌즈 이름이 섞여 분류기가 렌즈로 봄)
    return name if re.match(r"(?:leica|leitz)\b", name, re.I) else "Leica " + name


def _rangefinder_name(title):
    """Rangefinder 제목 다듬기: 'Leica Summilux-M 35mm F1.4 ASPH FLE &#8211; Silver (Used)' → 'Leica Summilux-M 35mm f1.4 ASPH FLE Silver'"""
    import html as _html
    name = re.sub(r"\s+", " ", _html.unescape(title)).strip()
    name = re.sub(r"\s*\((?:Used|Open Box)\)\s*$", "", name, flags=re.I)
    name = re.sub(r"\s*[\u2013\u2014]\s*|\s+-\s+", " ", name)
    name = re.sub(r"[\u201c\u201d\u2018\u2019\"]", "", name)
    name = re.sub(r"\s+(?:Mirrorless |Compact |Film )?Camera\b(?! Body Cap)|\s+Lens\b", "", name)
    name = re.sub(r"\bF(\d+(?:\.\d+)?)\b", lambda m: "f" + m.group(1) + ("" if "." in m.group(1) else ".0"), name)
    return re.sub(r"\s+", " ", name).strip(" /")


def crawl_rangefinder():
    """Rangefinder (홍콩) - 라이카 전문점 WooCommerce 'Pre-owned Items' 분류(40개쯤)를 상품 API(Store API) JSON으로.
    판매 중만, 라이카·라이츠만. 등급은 설명의 'Cosmetic Condition: ~92-93% new' (낮은 쪽 숫자), 개봉품은 'New condition'"""
    import html as _html
    import requests
    from condition_grade import RANGEFINDER_PREFIX
    results = []
    base = "https://www.rangefinder.com.hk"
    print(f"\n  📂 Rangefinder 크롤링 시작")
    for page_num in range(1, 10):
        url = f"{base}/wp-json/wc/store/v1/products?category=23&per_page=100&page={page_num}"
        try:
            # 서버가 Chrome 120 표기(목록 0·4번)는 403으로 막음 (2026-10-19) → Safari 표기로 고정
            resp = requests.get(url, headers={"User-Agent": USER_AGENTS[1]}, timeout=30)
            resp.raise_for_status()
            products = resp.json()
        except Exception as e:
            raise RuntimeError(f"Rangefinder {page_num}페이지 못 읽음: {e}")  # 빠진 쪽이 판매완료로 바뀌지 않게
        if not products:
            break
        print(f"    └─ {page_num}페이지 {len(products)}개 상품 발견")
        for p in products:
            title = _html.unescape(p.get("name") or "")
            if not re.match(r"(?:leica|leitz)\b", title, re.I) or not p.get("is_in_stock"):
                continue
            name = _rangefinder_name(title)
            prices = p.get("prices") or {}
            try:
                price = f"HK${int(prices.get('price')) / 10 ** int(prices.get('currency_minor_unit', 2)):,.0f}"
            except (TypeError, ValueError):
                price = "문의요망"
            text = _html.unescape(re.sub(r"<[^>]+>", " ", p.get("description") or ""))
            m = re.search(r"Cosmetic Condition:\s*~?\s*(\d{2,3})(?:\s*-\s*\d{2,3})?\s*%", text, re.I)
            if m:
                cond = RANGEFINDER_PREFIX + m.group(1)
            elif re.search(r"Cosmetic Condition:\s*(?:Brand )?New\b", text, re.I):
                cond = RANGEFINDER_PREFIX + "New"
            else:
                cond = "정보없음"
            img = p["images"][0].get("src", "") if p.get("images") else ""
            cat = detect_category(name, price)
            mount = 'Accessory' if cat == 'Accessory' else detect_mount(name)
            results.append({
                "site": "Rangefinder (홍콩)",
                "label": auto_label(name),
                "상품명": name,
                "세대": detect_generation(name),
                "컨디션": cond,
                "가격": price,
                "통화": "HKD",
                "이미지": img,
                "링크": p.get("permalink") or "",
                "품절": False,
                "예약중": False,
                "mount": mount,
                "category": cat,
                "brand": detect_brand(name),
            })
        if len(products) < 100:
            break
        time.sleep(random.uniform(1.0, 2.0))
    print(f"  ✅ Rangefinder 완료: {len(results)}개")
    return results


def _roterpunkt_name(title):
    """Roter Punkt 제목 다듬기: 'LEICA Objektiv Summilux-M 1.4/35 mm ASPH. FLE 6bit #11663 m. OVP' → 'Leica Summilux-M 35mm f1.4 ASPH.
    FLE 6bit #11663', 'LEICA IIIf Kit Summaron 1:3,5/3,5cm mit OVP' → 'Leica IIIf Kit Summaron 35mm f3.5'. 상자('m. OVP'·'u. Box')·
    정비·자랑 말('Top Sammlerstück'·'RARE sehr selten')은 떼고, 조리개/초점거리는 '35mm f1.4' 꼴로, 독일어 색은 영어로"""
    import html as _html
    name = re.sub(r"\s+", " ", _html.unescape(title).replace("\u0192", "f")).strip()
    name = re.sub(r"[„“\"*]", "", name)
    name = re.sub(r"\s+[–-]\s+(?:Top Sammlerstück|TOP Zustand|v\.\s.*|\(Service.*|MINT.*)$", "", name, flags=re.I)
    name = re.sub(r"\b(?:m\.|mit|in|u\.)\s+OVP\b|\bOVP\b|\bu\.\s*Box\b|\bund Box\b|\bRARE\b|\bsehr selten\b|\bRAR\b\s*!?|"
                  r"\b(?:frischer|neuer) Service\b(?:\s+\d+/\d+)?|\bwerkstatt\s?geprüft\b|\(Werkstatt geprüft\)|\bProduktion \d{4}\b|"
                  r"\bfrühe Seriennummer\b|\b1A\b|\bKamera\b|\bObjektiv\b|\bvom \d+\.\d+\.\d{4}\b", " ", name, flags=re.I)
    name = re.sub(r"^\s*(?:LEITZ\s*/\s*)?(?:LEICA\s+LEITZ|LEICA|Leica\s+LEITZ|Leica)\b\s*", "Leica ", name)
    name = re.sub(r"(\d),(\d)", r"\1.\2", name)
    name = re.sub(r"\s*\+\s*Hood(?:\s+(?:Geli|und Gegenlichtblende))?", "", name)
    name = re.sub(r"\s+(?:&|mit)\s+(?:Freilaufknopf\s+)?neuer .*$|\s+(?:neuer )?Sensor (?:neu|CCD).*$|\s+und Sondernummer.*$", "", name)
    name = re.sub(r"\b(\d(?:\.\d)?)\s?cm\b", lambda m: f"{round(float(m.group(1)) * 10)}mm", name)  # '3.5 cm' → '35mm'
    name = re.sub(r"(?<![\d.])(?:1:|f)?(\d+(?:\.\d+)?)\s?/\s?(\d{2,3}(?:-\d{2,3})?)\s?mm\b",
                  lambda m: f"{m.group(2)}mm f{m.group(1)}" + ("" if "." in m.group(1) else ".0"), name)  # '1.4/35 mm'·'f1.4/28mm' → '35mm f1.4'
    name = re.sub(r"^\s*Leica M39 (.+)$", r"Leica \1 M39", name)  # 나사 마운트 렌즈 ('M39 Summitar')
    name = re.sub(r"\b(\d{2,3}(?:[-–]\d{2,3})?)\s+mm\b", lambda m: m.group(1).replace("–", "-") + "mm", name)  # '50 mm' → '50mm'
    name = re.sub(r"\bF\s?/\s?(\d)", r"f\1", name)
    name = re.sub(r"\bf\s?/\s?(\d)", r"f\1", name)
    name = re.sub(r"\bf(\d)(?![\d.])", r"f\1.0", name)
    name = re.sub(r"\b(\d{2,3}mm)\s+(?=(?:f\d|ASPH))", r"\1 ", name)
    name = re.sub(r"\bTyp (\d{3})\b", r"(Typ \1)", name)
    name = re.sub(r"\bM246 Monochrom\b", "M Monochrom (Typ 246)", name)
    name = re.sub(r"\bM240\b", "M (Typ 240)", name)
    name = re.sub(r"\bstahlgrau lackiert\b", "steel grey", name, flags=re.I)
    name = re.sub(r"\bschwarz\s+chrom\b", "black chrome", name, flags=re.I)
    name = re.sub(r"\bschwarz\s+lackiert\b|\bblack paint\b", "black paint", name, flags=re.I)
    name = re.sub(r"\bschwarz\b|\(Schwarz\)", "black", name, flags=re.I)
    name = re.sub(r"\bsilber\b", "silver", name, flags=re.I)
    name = re.sub(r"\bchrom\b|\bcrom\b", "chrome", name, flags=re.I)
    name = re.sub(r"\bGegenlichtblende\b|\bGeli\b", "Lens Hood", name, flags=re.I)
    name = re.sub(r"\bBereitschaftstasche\b", "Ever-Ready Case", name)
    name = re.sub(r"\bEntfernungsmesser\b", "Rangefinder", name)
    name = re.sub(r"\bDaumenstütze\b", "Thumb Rest", name)
    name = re.sub(r"\bBlitzschuh-?\s?Abdeckung\b", "Hot Shoe Cover", name, flags=re.I)
    name = re.sub(r"(#11817\b)", r"\1 3rd", name)  # 주미크론 50 3세대 번호 (번호만으론 이름이 이겨 현행으로 감)
    name = re.sub(r"\bAufstecksucher\b|\bFinder\b", "Viewfinder", name)
    name = re.sub(r"\bFreilaufknopf\b", "", name)
    name = re.sub(r"\bmit\b|&", "with", name)
    name = re.sub(r"\bund\b", "and", name)
    name = re.sub(r"\bSondermodell\b", "Special Edition", name)
    name = re.sub(r"\bNeuware\b|\bneuwertig\b", "", name, flags=re.I)
    name = re.sub(r"\s+\.\s+|\s+[–-]\s+", " ", name)
    name = re.sub(r"\s+", " ", name).strip(" ,-+.!")
    name = re.sub(r"\s+(?:with|and)$", "", name)
    if not re.match(r"(?:leica|leitz)\b", name, re.I):
        name = "Leica " + name
    if re.match(r"Leica (?:M\d{1,2}(?:-[PRD])?|MP|M-[AP]|M \(Typ|M Monochrom|SL\d?|Q\d?)\b", name) and not re.search(
            r"\d+mm|Hood|Thumb|Case|Viewfinder|Filter|Release|Body", name, re.I):
        name += " Body"  # 바디 이름만 있으면 렌즈로 갈리지 않게
    return name


def crawl_roterpunkt():
    """Roter Punkt (독일) - 베를린 라이카 중고 전문점 WooCommerce 상품 API(Store API) JSON 전체(90개쯤). 제목에 Leica·Leitz가
    있는 것만 (Keks 노출계·가죽끈 같은 다른 회사 액세서리 제외), 설명에 'VERKAUFT'가 있으면 재고 표시가 남아도 뺌.
    등급은 설명의 'Qualität: A++ (private Einschätzung)' (A+++·A++·A+·A·A-B, 새 액세서리는 Neuware·Demoware)"""
    import html as _html
    import requests
    from condition_grade import ROTERPUNKT_PREFIX
    results = []
    base = "https://www.roter-punkt-kamera.de"
    print(f"\n  📂 Roter Punkt 크롤링 시작")
    for page_num in range(1, 10):
        url = f"{base}/wp-json/wc/store/v1/products?per_page=100&page={page_num}"
        try:
            resp = requests.get(url, headers={"User-Agent": USER_AGENTS[1]}, timeout=60)
            resp.raise_for_status()
            products = resp.json()
        except Exception as e:
            raise RuntimeError(f"Roter Punkt {page_num}페이지 못 읽음: {e}")  # 빠진 쪽이 판매완료로 바뀌지 않게
        if not products:
            break
        print(f"    └─ {page_num}페이지 {len(products)}개 상품 발견")
        for p in products:
            title = _html.unescape(p.get("name") or "")
            text = re.sub(r"\s+", " ", _html.unescape(re.sub(r"<[^>]+>", " ", (p.get("short_description") or "") + " " +
                                                             (p.get("description") or ""))))
            if (not re.search(r"\b(?:leica|leitz)\b", title, re.I) or not p.get("is_in_stock") or "VERKAUFT" in text
                    or re.search(r"schild\b", title, re.I)):
                continue
            name = _roterpunkt_name(title)
            prices = p.get("prices") or {}
            try:
                price = f"€{int(prices.get('price')) / 10 ** int(prices.get('currency_minor_unit', 2)):,.0f}"
            except (TypeError, ValueError):
                price = "문의요망"
            m = (re.search(r"Qualität:\s*(Neuware|Demoware|[A-D](?:\s?-\s?[A-D]\b|\+{0,3}))", text) or
                 re.search(r"Zustand:\s*(Neuware|Demoware|[A-D](?:\s?-\s?[A-D]\b|\+{0,3}))", text))
            cond = ROTERPUNKT_PREFIX + m.group(1).replace(" ", "") if m else "정보없음"
            img = p["images"][0].get("src", "") if p.get("images") else ""
            cat = detect_category(name, price)
            mount = 'Accessory' if cat == 'Accessory' else detect_mount(name)
            results.append({
                "site": "Roter Punkt (독일)",
                "label": auto_label(name),
                "상품명": name,
                "세대": detect_generation(name),
                "컨디션": cond,
                "가격": price,
                "통화": "EUR",
                "이미지": img,
                "링크": p.get("permalink") or "",
                "품절": False,
                "예약중": False,
                "mount": mount,
                "category": cat,
                "brand": detect_brand(name),
            })
        if len(products) < 100:
            break
        time.sleep(random.uniform(1.0, 2.0))
    print(f"  ✅ Roter Punkt 완료: {len(results)}개")
    return results


_PG_FAMILY = (r"(?:APO[\s-])?(?:SUPER[\s-])?(?:TELE[\s-]|MACRO[\s-]|VARIO[\s-]|TRI[\s-])?(?:SUMMILUX|SUMMICRON|ELMARIT|ELMAR|NOCTILUX|SUMMARON|"
              r"SUMMARIT|SUPER[\s-]ANGULON|HEKTOR|TELYT|THAMBAR|SUMMAR|SUMMITAR|XENON)")


def _photografica_name(title):
    """Photografica 제목 다듬기: 'LEICA M 50/1,4 SUMMILUX ASPH BLACK' → 'Leica Summilux-M 50mm f1.4 ASPH black',
    'LEICA SM 35/3,5 SUMMARON' → 'Leica Summaron 35mm f3.5 LTM', 'BRUGT LEICA M SØGER 24MM' → 'Leica M Viewfinder 24mm'.
    'BRUGT'(중고)·'MINT BOXED'·'(Haze)' 같은 꼬리는 떼고 덴마크어 색·부속 이름은 영어로"""
    import html as _html
    name = re.sub(r"\s+", " ", _html.unescape(title)).strip()
    name = re.sub(r"^BRUGT[\s-]+", "", name, flags=re.I)
    name = re.sub(r"\bSUPER-V\b", "SUPER VARIO ELMAR", name)
    name = re.sub(rf"(?i)^(LEICA|LEITZ)\s+({_PG_FAMILY})[\s-](M|R)\s+(\d{{2,3}}/\d[\d,]*)", r"\1 \3 \4 \2", name)  # 'ELMARIT M 28/2,8' → 'M 28/2,8 ELMARIT'
    name = re.sub(r"\s*[-–]?\s*\b(?:MINT BOXED|Mint Boxed|Mint boxed)\b|\s*\((?:Mild )?Haze\)|\s*\(Som ny\)|\s*\+\s*(?:MODLYSBLÆNDE|ÆSKE|BOX)\b",
                  "", name, flags=re.I)
    name = re.sub(r"(\d),(\d)", r"\1.\2", name)
    m = re.match(r"(?i)(LEICA|LEITZ)\s+(M|R|SM|L|SL|TL|S)\s+(\d{2,3}(?:-\d{2,3})?)\s?/\s?(\d+(?:\.\d+)?(?:-\d+(?:\.\d+)?)?)\s*(.*)$", name)
    if m:
        brand, mount, fl, ap, rest = m.groups()
        fam = re.search(_PG_FAMILY, rest, re.I)
        ap = ap + ("" if "." in ap else ".0")
        mount = mount.upper()
        if fam:
            rest = (rest[:fam.start()] + " " + rest[fam.end():]).strip()
            family = "-".join(w.capitalize() if w.upper() != "APO" else "APO" for w in re.split(r"[\s-]", fam.group(0)))
            suffix = {"M": "-M", "R": "-R", "SL": "-SL", "TL": "-TL", "S": "-S"}.get(mount, "")
            name = f"Leica {family}{suffix} {fl}mm f{ap} {rest}" + (" LTM" if mount == "SM" else "")
        else:
            name = f"Leica {mount if mount != 'SM' else 'LTM'} {fl}mm f{ap} {rest}"
    name = re.sub(r"\b(\d{2,3}(?:-\d{2,3})?)\s?/\s?(\d(?:\.\d+)?)\b", lambda m: f"{m.group(1)}mm f{m.group(2)}", name)
    name = re.sub(r"\b(\d{2,3})MM\b", r"\1mm", name)
    name = re.sub(r"\b11817\b", "11817 3rd", name)  # 주미크론 50 3세대 번호 (번호만으론 이름이 이겨 현행으로 감)
    for da, en in (("SØGERLUP", "Viewfinder Magnifier"), ("SØGER", "Viewfinder"), ("MODLYSBLÆNDE", "Lens Hood"),
                   ("HÅNDLEDSREM", "Wrist Strap"), ("HÅNDGREB", "Handgrip"), ("LÆDERTASKE", "Leather Case"), ("TASKE", "Case"),
                   ("DÆKSEL", "Cover"), ("AKKU", "Battery"), ("REM", "Strap"), ("UDLØSER", "Release"), ("LÆDER", "Leather"),
                   ("SORT", "black"), ("SØLV", "silver"), ("KROM", "chrome"), ("RØD", "red"), ("BRAUN", "brown"), ("TIL", "for"),
                   ("COLL\\.", "Collapsible"), ("FAT", "Fat"), ("GRIB", "Grip"), ("BÆLG", "Bellows"),
                   ("SOOKY", "SOOKY Close-up Adapter"), ("LADER", "Charger"), ("KABEL", "Cable")):
        name = re.sub(rf"\b{da}(?=\W|$)", en, name, flags=re.I)
    name = re.sub(r"^(?:LEICA|LEITZ|Leica|Leitz)\b", "Leica", name)
    name = re.sub(r"\bLEICA\b", "Leica", name)
    name = re.sub(r"\s*\(\s*\)|\s+-\s*$", "", name)
    name = re.sub(r"\s+", " ", name).strip(" ,-+")
    if not re.match(r"(?:leica|leitz)\b", name, re.I):
        name = "Leica " + name
    if re.match(r"Leica (?:M\d{1,2}(?:-[PRD])?|MP|M-[AP]|CL|SL\d?|Q\d?|CM|M3|M2|M4(?:-P)?|M6|M7|M5)\b", name) and not re.search(
            r"\d+mm|Hood|Case|Viewfinder|Filter|Release|Strap|Battery|Handgrip|Cover|Body|Cap|Adapter|Winder|Grip|\+", name, re.I):
        name += " Body"
    return name


def crawl_photografica():
    """Photografica (덴마크) - 코펜하겐 클래식·중고 카메라 딜러(Shopify)의 'Photografica Vintage' 라이카 컬렉션 3곳
    (카메라·렌즈·액세서리, 판매 중 120개쯤) JSON. 제목이 Leica·Leitz인 것만 ('UORIGINAL' 호환 배터리 등은 뺌), 가격은 DKK.
    등급은 설명 첫 문장 'The lens is in very good condition' (mint~fair), 새 상품은 'This is a new item'·'Nyt i original indpakning'"""
    import html as _html
    import requests
    from condition_grade import PHOTOGRAFICA_PREFIX
    results, seen = [], set()
    base = "https://www.photografica.com"
    print(f"\n  📂 Photografica 크롤링 시작")
    for coll in ("photografica-vintage-leica-kamera", "photografica-vintage-leica-objektiver", "photografica-vintage-leica-tilbehor"):
        for page_num in range(1, 10):
            url = f"{base}/collections/{coll}/products.json?limit=250&page={page_num}"
            try:
                resp = requests.get(url, headers={"User-Agent": random.choice(USER_AGENTS)}, timeout=30)
                resp.raise_for_status()
                products = resp.json().get("products", [])
            except Exception as e:
                raise RuntimeError(f"Photografica {coll} {page_num}페이지 못 읽음: {e}")  # 빠진 쪽이 판매완료로 바뀌지 않게
            if not products:
                break
            print(f"    └─ {coll} {page_num}페이지 {len(products)}개 상품 발견")
            for p in products:
                title = (p.get("title") or "").strip()
                if p.get("id") in seen or not re.search(r"\b(?:leica|leitz)\b", title, re.I) or re.search(r"\bUORIGINAL\b", title, re.I):
                    continue
                variants = p.get("variants") or [{}]
                if not any(v.get("available") for v in variants):
                    continue
                seen.add(p.get("id"))
                name = _photografica_name(title)
                if re.match(r"Leica CL\b", name) and any("analog" in t.lower() for t in p.get("tags") or []):
                    name = name.replace("Leica CL", "Leica CL film", 1)  # 1973년 필름 CL (디지털 CL로 붙지 않게)
                try:
                    price = f"DKK {float(variants[0].get('price')):,.0f}"
                except (TypeError, ValueError):
                    price = "문의요망"
                text = re.sub(r"\s+", " ", _html.unescape(re.sub(r"<[^>]+>", " ", p.get("body_html") or "")))
                m = re.search(r"\b(?:is|are both) in (mint|near mint|excellent|very good|good|decent|fair)\b", text, re.I)
                if m:
                    cond = PHOTOGRAFICA_PREFIX + m.group(1).lower()
                elif re.search(r"\bnew (?:unused )?(?:item|camera)\b|\bunused item\b|\bny(?:t)? (?:vare|produkt)\b|"
                               r"\bnyt? i original indpakning\b|\bubrugt\b", text, re.I):
                    cond = PHOTOGRAFICA_PREFIX + "new"
                else:
                    cond = "정보없음"
                img = p["images"][0].get("src", "") if p.get("images") else ""
                cat = detect_category(name, price)
                mount = 'Accessory' if cat == 'Accessory' else detect_mount(name)
                results.append({
                    "게시일": _shopify_listed(p),
                    "site": "Photografica (덴마크)",
                    "label": auto_label(name),
                    "상품명": name,
                    "세대": detect_generation(name),
                    "컨디션": cond,
                    "가격": price,
                    "통화": "DKK",
                    "이미지": img,
                    "링크": f"{base}/products/{p['handle']}",
                    "품절": False,
                    "예약중": False,
                    "mount": mount,
                    "category": cat,
                    "brand": detect_brand(name),
                })
            if len(products) < 250:
                break
            time.sleep(random.uniform(1.0, 2.0))
        time.sleep(random.uniform(1.0, 2.0))
    print(f"  ✅ Photografica 완료: {len(results)}개")
    return results


def _shphoto_name(title):
    """SHphoto 제목 다듬기: 'Leitz Leica Elmar M39 3,5/5cm Red Scale' → 'Leica Elmar M39 50mm f3.5 Red Scale',
    'LEICA Summicron M 1:2/35 mm 6 Elements' → 'Leica Summicron-M 35mm f2.0 6 Elements', 'Leitz Leica II f body' → 'Leica IIf Body'.
    앞의 'Leitz Leica'·'Ernst Leitz Wetzlar' 같은 이름 겹침을 'Leica' 하나로, 독일어 부속 이름은 영어로"""
    import html as _html
    name = re.sub(r"\s+", " ", _html.unescape(title)).strip()
    name = re.sub(r"(?i)^(?:(?:Ernst|E\.)\s?Leitz(?: GmbH)?(?: Wetzlar| Wetzler| New York)?(?: Germany)?|Leitz(?: Wetzlar)?(?: Germany)?|"
                  r"Leica|LEICA|Original Leica|Leizt|Letz)(?:\s+(?:Leica|Leitz|LEICA|LEITZ)(?: Wetzlar(?: Germany)?)?)*\b\s*", "Leica ", name)
    name = re.sub(r"\b(?:nottested|notteated|not tested)\b", "", name, flags=re.I)
    name = re.sub(r"(\d),(\d)", r"\1.\2", name)
    name = re.sub(r"\b(\d+(?:\.\d+)?)\s?cm\b", lambda m: f"{round(float(m.group(1)) * (10 if float(m.group(1)) < 100 else 1))}mm",
                  name)  # '13.5cm' → '135mm' ('135cm'는 매장 오기라 135mm)
    fmt = lambda fl, ap: f"{fl}mm f{ap}" + ("" if "." in ap else ".0")
    name = re.sub(r"(?<![\d.])(\d(?:\.\d+)?)\s?/\s?(\d{2,3}-\d{2,3})\s?mm\b", lambda m: fmt(m.group(2), m.group(1)), name)  # 줌 '4.5/80-200 mm'
    name = re.sub(r"(?<![\d.])(?:1:)?(\d(?:\.\d+)?)\s?/\s?(\d{2,3})\s?mm\b", lambda m: fmt(m.group(2), m.group(1)), name)  # '1:2/35 mm'·'3.5/50mm'
    name = re.sub(r"\b(\d{2,3})mm\s?/\s?(?:1:)?(\d(?:\.\d+)?)\b", lambda m: fmt(m.group(1), m.group(2)), name)  # '50mm/3.5'
    name = re.sub(r"\b(\d{2,3})mm\s+f\s?/?(\d(?:\.\d+)?)\b", lambda m: fmt(m.group(1), m.group(2)), name)  # '135mm f4.5'
    name = re.sub(r"(?<![\d.])(\d(?:\.\d+)?)\s?/\s?(\d{2,3})\b(?!\s?mm)", lambda m: fmt(m.group(2), m.group(1)), name)  # '2.8/90'
    name = re.sub(r"\b(\d{2,3})\s?/\s?(\d(?:\.\d+)?)\b(?!\s?mm)", lambda m: fmt(m.group(1), m.group(2)), name)  # '135/4.5'
    name = re.sub(r"\s+(?:analoge\s+)?Messsucherkamera\b.*$|\bWe[tz]{1,2}lar\b", "", name)
    name = re.sub(r"\b(Summicron|Summilux|Elmarit|Elmar|Summaron|Summarit|Noctilux|Tele-Elmarit)\s(M|R)\b", r"\1-\2", name)
    name = re.sub(r"\b(I{1,3}|1|2|3)\s?([a-gA-G])\b(?!-)", lambda m: {"1": "I", "2": "II", "3": "III"}.get(m.group(1), m.group(1)) + m.group(2).lower(), name)
    name = re.sub(r"\b(?:body|Gehäuse)\b", "Body", name, flags=re.I)
    name = re.sub(r"(?<=\S)\s+Leica\s+(?:Screw\s+)?(?=M39|L39)", " ", name)  # 'Hektor 135mm Leica M39' ('Leica M3'로 바디가 되지 않게)
    name = re.sub(r"\bStandart\b", "Standard", name)
    name = re.sub(r"\bmini Elmar\b", "Elmar", name, flags=re.I)
    for de, en in (("Bodendeckel", "Bottom Cover"), ("Objektivfrontdeckel", "Lens Cap"), ("Objektiv Front Deckel", "Lens Cap"),
                   ("Objektivdeckel", "Lens Cap"), ("Deckel", "Lens Cap"), ("Tischstativ", "Tabletop Tripod"),
                   ("Kugelgelenkkopf", "Ball Head"), ("Universaltasche", "Universal Case"), ("Aufklappsucher", "Folding Viewfinder"),
                   ("Wasserwaage", "Spirit Level"), ("Gegenlichtblende", "Lens Hood"), ("Sonnenblende", "Lens Hood"), ("Sucher", "Viewfinder"), ("Spiegelsucher", "Mirror Viewfinder"),
                   ("Selbstauslöser", "Self Timer"), ("Balgengerät", "Bellows"), ("Gelbfilter", "Yellow Filter"), ("Blaufilter", "Blue Filter"),
                   ("Polfilter", "Polarizing Filter"), ("Zwischenring", "Extension Ring"), ("Nahvorsatz", "Close-up Lens"), ("Nahlinse", "Close-up Lens"),
                   ("Vorsatzlinse", "Close-up Lens"), ("Handgriff", "Handgrip"), ("Tragriemen", "Strap"), ("Kameragurt", "Strap"),
                   ("Gehäusedeckel", "Body Cap"), ("Bereitschaftstasche", "Ever-Ready Case"), ("Beiretschaftstasche", "Ever-Ready Case"),
                   ("Filmdose", "Film Canister"), ("Belichtungsmesser", "Light Meter"), ("schwarz", "black"), ("silber", "silver"),
                   ("chrom", "chrome"), ("grau", "grey"), ("rot", "red"), ("gelb", "yellow"), ("für", "for"), ("mit", "with")):
        name = re.sub(rf"\b{de}\b", en, name, flags=re.I)
    name = re.sub(r"\s+", " ", name).strip(" ,-")
    if not re.match(r"(?:leica|leitz)\b", name, re.I):
        name = "Leica " + name
    if re.fullmatch(r"Leica (?:M\d(?:-\d|-P)?|MP|CL|I{1,3}[a-g]?|I[a-g]|250|M[1-7])(?: (?:black|silver|chrome|black paint|Body|\d{4}))*", name):
        name = re.sub(r"(?: Body)?$", " Body", name, count=1)  # 바디 이름만 있으면 렌즈로 갈리지 않게
    return name


_SH_LENS_FAMILY = (r"Summicron|Summilux|Elmarit|Elmar|Summaron|Summarit|Summitar|Summar|Noctilux|Hektor|Telyt|Angulon|Xenon|"
                   r"Thambar|Tri-Elmar|Apo-|Macro-Elmar")
_SH_ACCESSORY = (r"Close-up|Extension Ring|Macro Ring|Bellows|projekt|Projektor|Focusing Mount|Fokus|Adapter|Blende|Deckel|SDPOO|"
                 r"Viewfinder|Lens Hood|Filter|Prado|Pradovit|Mikro|Focotar|Diamask|Stereo|Nahaufnahme|MIKAS|Micro Attachment|SOOKY|Near Focusing")


def crawl_shphoto():
    """SHphoto (독일) - 뉘른베르크 매장(Fotomax, Shopware) '/gebrauchtware/leica/' 분류 정적 HTML (24개씩 17쪽쯤, 390개 —
    빈티지 필터·후드 같은 액세서리가 절반 넘음). 제목이 Leica·Leitz로 시작하는 것만 (FED·Jupiter·Novoflex 같은 다른 회사 M39
    렌즈 제외). 'Für Sie bestellt'(LimitedAvailability)는 예약중으로. 등급은 상세 화면 'Zustand: AB'(있는 상품만, 처음 본 매물만 읽음)"""
    import html as _html
    import requests
    results, seen = [], set()
    base = "https://shphoto.de/gebrauchtware/leica/"
    print(f"\n  📂 SHphoto 크롤링 시작")
    for page_num in range(1, 60):
        try:
            resp = requests.get(f"{base}?p={page_num}", headers={"User-Agent": USER_AGENTS[1]}, timeout=30)
            resp.raise_for_status()
        except Exception as e:
            raise RuntimeError(f"SHphoto {page_num}페이지 못 읽음: {e}")  # 빠진 쪽이 판매완료로 바뀌지 않게
        new = 0
        for card in resp.text.split('class="card product-box')[1:]:
            m = re.search(r'href="([^"]+)"\s+class="product-name"\s+title="([^"]+)"', card)
            if not m or m.group(1) in seen:
                continue
            seen.add(m.group(1))
            new += 1
            title = re.sub(r"\s+", " ", _html.unescape(m.group(2))).strip()
            if not re.match(r"(?:(?:Ernst|E\.)\s?Leitz|Leitz|Leica|Original Leica|Leizt|Letz)\b", title, re.I):
                continue
            name = _shphoto_name(title)
            if any(b2 in name.lower() for b2 in THIRD_PARTY_BRANDS) or re.search(
                    r"Schneider|Novoflex|Tamron|Kenko|KMZ|Jupiter|\bFED\b|Industar|Russar|Meopta", name, re.I):
                continue
            pm = re.search(r'unit-price">\s*([\d.]+),(\d\d)\s*€', card) or re.search(r"([\d.]+),(\d\d)\s*€", card)
            price = f"€{int(pm.group(1).replace('.', '')):,}" if pm else "문의요망"
            img = re.search(r'<img src="([^"]+)"', card)
            if re.search(r"projekt|Filmkamera|Leicina|Mikroskop|Nachtsicht|Stereo|Diamask|Schild", name, re.I):
                continue  # 영사기·무비 카메라·현미경 부품 같은 사진기 아닌 물건
            # 독일어 액세서리(접사링·초점 헬리코이드·렌즈캡 등)는 렌즈 이름이 섞여 있어 분류기가 렌즈로 보므로 'accessory'를 붙임
            has_family = re.search(_SH_LENS_FAMILY, name, re.I) and re.search(r"\d{2,3}(?:-\d{2,3})?mm", name)
            is_body = re.match(r"Leica (?:I{1,3}[a-g]?|I[a-g]|M\d|MP|CL|Standard|Leicaflex|R\d|X\d|X-|Q\d?|D-Lux|C-Lux|V-Lux|"
                               r"Digilux|Minilux|Mini\b|CM|C\d|Z2X|AF-C|Sofort)\b", name, re.I)
            has_focal = re.search(r"\d{2,3}(?:-\d{2,3})?mm\s+f\d", name)
            if not re.search(r"\bBody\b", name) and (re.search(_SH_ACCESSORY, name, re.I) or not (has_family or has_focal or is_body)):
                name += " accessory"
            cat = detect_category(name, price)
            mount = 'Accessory' if cat == 'Accessory' else detect_mount(name)
            results.append({
                "site": "SHphoto (독일)",
                "label": auto_label(name),
                "상품명": name,
                "세대": detect_generation(name),
                "컨디션": "정보없음",
                "가격": price,
                "통화": "EUR",
                "이미지": img.group(1) if img else "",
                "링크": m.group(1),
                "품절": False,
                "예약중": "schema.org/LimitedAvailability" in card,
                "mount": mount,
                "category": cat,
                "brand": detect_brand(name),
            })
        if not new:
            break
        print(f"    └─ {page_num}페이지 {new}개 상품 발견")
        time.sleep(random.uniform(1.0, 2.0))
    from condition_grade import SH_PREFIX

    def read_detail(url):  # 상세 화면 'Zustand: AB, voll funktionsfähiger guter Zustand …' (없는 상품도 있음)
        page = requests.get(url, headers={"User-Agent": USER_AGENTS[1]}, timeout=30)
        page.raise_for_status()
        m = re.search(r"Zustand:\s*(A-|AB|A|BC|B|C|D)\b", re.sub(r"<[^>]+>", " ", page.text))
        return SH_PREFIX + m.group(1) if m else None
    _fill_detail_conditions("SHphoto (독일)", results, read_detail)
    print(f"  ✅ SHphoto 완료: {len(results)}개")
    return results


def crawl_delfshaven():
    """Fotohandel Delfshaven (네덜란드) - 로테르담 중고·빈티지점(WooCommerce)의 'leica' 분류 정적 HTML (22개씩 22쪽쯤, 470개).
    상품 API(/wp-json/wc/store)는 500이라 목록 화면으로. 묶음(grouped) 상품은 같은 목록에 낱개(simple)로도 나와 낱개만 담고,
    다른 브랜드(Voigtländer Bessa·MOM 등)는 뺌. 가격은 EUR. 등급(별 1~5개)은 상품 화면에만 있어 목록 설명 말투로 (describe_text)"""
    import html as _html
    import requests
    from condition_grade import describe_text
    results, seen = [], set()
    base = "https://fotohandeldelfshaven.nl"
    headers = {"User-Agent": random.choice(USER_AGENTS)}
    print(f"\n  📂 Fotohandel Delfshaven 크롤링 시작")
    pages = 1
    page_num = 1
    while page_num <= pages and page_num < 60:
        url = f"{base}/product-categorie/leica/" + (f"page/{page_num}/" if page_num > 1 else "")
        try:
            resp = requests.get(url, headers=headers, timeout=30)
            resp.raise_for_status()
        except Exception as e:
            raise RuntimeError(f"Fotohandel Delfshaven {page_num}페이지 못 읽음: {e}")  # 빠진 쪽이 판매완료로 바뀌지 않게
        html_text = resp.text
        m_total = re.search(r"of\s+(\d+)\s+results", html_text)
        items = re.findall(r'<li[^>]*class="([^"]*\bproduct\b[^"]*)"[^>]*>(.*?)</li>', html_text, re.S)
        if m_total and items:
            pages = -(-int(m_total.group(1)) // len(items)) if page_num == 1 else pages
        print(f"    └─ {page_num}/{pages}페이지 {len(items)}개 상품 발견")
        for cls, body in items:
            if "product-type-simple" not in cls or "outofstock" in cls:
                continue
            m_link = re.search(r'href="(https://fotohandeldelfshaven\.nl/product/[^"]+)"', body)
            m_name = re.search(r'loop-product__title">([^<]+)', body)
            if not m_link or not m_name or m_link.group(1) in seen:
                continue
            name = re.sub(r"\s+", " ", _html.unescape(m_name.group(1))).strip()
            if not re.match(r"(?:leica|leitz|ernst leitz)\b", name, re.I) or any(b2 in name.lower() for b2 in THIRD_PARTY_BRANDS):
                continue
            seen.add(m_link.group(1))
            m_price = re.search(r'amount"><bdi>.*?</span>([\d.,]+)</bdi>', body)
            if m_price:
                amount = float(m_price.group(1).replace(".", "").replace(",", "."))
                price = f"€{amount:,.0f}"
            else:
                price = "문의요망"
            name = re.sub(r"\bF/(\d)", r"f\1", name)
            name = re.sub(r"\b(\d{1,2}(?:[.,]\d)?)\s?cm\b", lambda m: f"{round(float(m.group(1).replace(',', '.')) * 10):d}mm", name)
            name = re.sub(r"\s*\+\s*(?=(?:metal\s+)?(?:lens\s?)?hood\b)", " with ", name, flags=re.I)  # '+ Hood'가 후드 매물로 빠지지 않게
            m_img = re.search(r'<img[^>]+src="([^"]+)"', body)
            img = re.sub(r"-\d+x\d+(\.\w+)$", r"\1", m_img.group(1)) if m_img else ""
            short = re.search(r'hongo-short-description">(.*?)</div>', body, re.S)
            cond = describe_text(short.group(1) if short else "") or "정보없음"
            cat = detect_category(name, price)
            mount = 'Accessory' if cat == 'Accessory' else detect_mount(name)
            results.append({
                "site": "Fotohandel Delfshaven (네덜란드)",
                "label": auto_label(name),
                "상품명": name,
                "세대": detect_generation(name),
                "컨디션": cond,
                "가격": price,
                "통화": "EUR",
                "이미지": img,
                "링크": m_link.group(1),
                "품절": False,
                "예약중": False,
                "mount": mount,
                "category": cat,
                "brand": detect_brand(name),
            })
        page_num += 1
        time.sleep(random.uniform(1.5, 2.5))
    print(f"  ✅ Fotohandel Delfshaven 완료: {len(results)}개")
    return results


def crawl_cameratweedehands():
    """Camera Tweedehands (네덜란드) - 중고 전문점(Lightspeed)의 브랜드 Leica 목록 JSON('/brands/leica/pageN.html?format=json',
    24개씩 5쪽쯤, 110개쯤). 가게 전체가 중고라 새 상품 거르기는 없음. 가격은 EUR. 등급 표기 없음.
    robots.txt의 Crawl-delay 2초를 지킨다"""
    import requests
    results, seen = [], set()
    base = "https://www.camera-tweedehands.nl"
    headers = {"User-Agent": random.choice(USER_AGENTS), "Accept": "application/json"}
    print(f"\n  📂 Camera Tweedehands 크롤링 시작")
    pages = 1
    page_num = 1
    while page_num <= pages and page_num < 40:
        url = f"{base}/brands/leica/" + (f"page{page_num}.html" if page_num > 1 else "") + "?format=json"
        try:
            resp = requests.get(url, headers=headers, timeout=30)
            resp.raise_for_status()
            coll = resp.json().get("collection") or {}
        except Exception as e:
            raise RuntimeError(f"Camera Tweedehands {page_num}페이지 못 읽음: {e}")  # 빠진 쪽이 판매완료로 바뀌지 않게
        pages = int(coll.get("pages") or 1)
        shop_id = (resp.json().get("shop") or {}).get("id")
        products = coll.get("products") or {}
        products = list(products.values()) if isinstance(products, dict) else products
        print(f"    └─ {page_num}/{pages}페이지 {len(products)}개 상품 발견")
        for p in products:
            if p.get("id") in seen or not p.get("available"):
                continue
            seen.add(p.get("id"))
            name = re.sub(r"\s+", " ", p.get("title") or "").strip()
            name = re.sub(r"\[(\d{5})\]", r"(\1)", name)
            name = re.sub(r"\bf/(\d)", r"f\1", name)
            if not re.match(r"(?:leica|leitz)\b", name, re.I):
                name = "Leica " + name
            amount = (p.get("price") or {}).get("price_incl") or (p.get("price") or {}).get("price")
            price = f"€{float(amount):,.0f}" if amount else "문의요망"
            img = f"https://cdn.webshopapp.com/shops/{shop_id}/files/{p['image']}/600x600x2/image.jpg" if p.get("image") and shop_id else ""
            cat = detect_category(name, price)
            mount = 'Accessory' if cat == 'Accessory' else detect_mount(name)
            results.append({
                "site": "Camera Tweedehands (네덜란드)",
                "label": auto_label(name),
                "상품명": name,
                "세대": detect_generation(name),
                "컨디션": "정보없음",
                "가격": price,
                "통화": "EUR",
                "이미지": img,
                "링크": f"{base}/{p.get('url')}",
                "품절": False,
                "예약중": False,
                "mount": mount,
                "category": cat,
                "brand": detect_brand(name),
            })
        page_num += 1
        time.sleep(random.uniform(2.0, 3.0))
    print(f"  ✅ Camera Tweedehands 완료: {len(results)}개")
    return results


def crawl_cardinal():
    """Cardinal Camera Used (미국) - 펜실베이니아 중고 전용 몰 Shopify products.json 전체(3,500개쯤, 14쪽)에서 브랜드 칸이 Leica인 것만.
    상품 종류(Rangefinder·Rangefinder camera lens·35mm lens·Filter·Caps…)로 액세서리를 거르고(종류 칸이 섞여 있어 바디·렌즈는 이름으로),
    설명서·상자·책·인화 장비는 뺌.
    등급 표기는 없고 설명 첫 문장 말투('Lens is in very good condition', 고장은 'sold as is')"""
    import html as _html
    import requests
    from condition_grade import cardinal_condition
    results = []
    sess = requests.Session()
    sess.headers["User-Agent"] = random.choice(USER_AGENTS)
    base = "https://cardinalcameraused.com"
    lens_body_types = ("rangefinder camera lens", "35mm lens", "digital lens", "rangefinder", "digital camera", "point and shoot", "asis")
    print(f"\n  📂 Cardinal Camera Used 크롤링 시작")
    for p in _shopify_all(sess, f"{base}/products.json", "Cardinal Camera Used"):
        ptype = (p.get("product_type") or "").strip().lower()
        if (p.get("vendor") or "").strip().lower() != "leica" or ptype in ("manual", "boxes", "book", "enlarging equipment", "parts"):
            continue
        variants = p.get("variants") or [{}]
        if not any(v.get("available") for v in variants):
            continue
        title = re.sub(r"\s+", " ", _html.unescape(p.get("title") or "")).strip()
        if re.search(r"convert|cine(ma)?\b|nikon f\b|canon ef|\bbox (and|&) case\b|^box\b", title, re.I):
            continue  # 다른 마운트·영화용으로 개조한 렌즈, 상자만
        name = re.sub(r"\b(?:35mm )?(?:rangefinder )?(?:film )?camera(?: body)?\b|\brangefinder\b|\b(?:telephoto |camera )?lens\b|\bRARE\b", " ", title, flags=re.I)
        name = re.sub(r"\bSN\s?:?\s?[0-9X]+\b|\bMFR\s?#\s?\d+|\bw/\s*$|\btelephoto\b|\(copy\)", " ", name, flags=re.I)  # '(Copy)'는 몰의 복제 상품 표시
        name = re.sub(r"\bLeica 1 Model\b", "Leica I Model", name, flags=re.I)
        name = re.sub(r"\bf/(\d)", r"f\1", name)
        name = re.sub(r"\s+", " ", name).strip(" ,-/")
        if not re.match(r"(?:leica|leitz)\b", name, re.I):
            name = "Leica " + name
        try:
            price = f"${float(variants[0].get('price')):,.0f}"
        except (TypeError, ValueError):
            price = "문의요망"
        cat = detect_category(name, price) if ptype in lens_body_types else "Accessory"
        if re.search(r"view ?finder|\bhood\b|\bshade\b|\bcap\b|filter|loupe|extension tube|nooky|crank|\bbarrel\b", name, re.I):
            cat = "Accessory"  # 렌즈·바디 종류 칸에 필터·캡·후드·파인더가 섞여 있음
        mount = 'Accessory' if cat == 'Accessory' else detect_mount(name)
        img = p["images"][0].get("src", "") if p.get("images") else ""
        results.append({
            "게시일": _shopify_listed(p),
            "site": "Cardinal Camera Used (미국)",
            "label": auto_label(name),
            "상품명": name,
            "세대": detect_generation(name),
            "컨디션": cardinal_condition(p.get("body_html") or "") or "정보없음",
            "가격": price,
            "통화": "USD",
            "이미지": img,
            "링크": f"{base}/products/{p['handle']}",
            "품절": False,
            "예약중": False,
            "mount": mount,
            "category": cat,
            "brand": detect_brand(name),
        })
    print(f"  ✅ Cardinal Camera Used 완료: {len(results)}개")
    return results


def crawl_fivestar():
    """Five Star Camera (일본) - 신주쿠 수출 중고점 Shopify. 전체가 15,000점(61쪽)이라 'leica' 컬렉션 products.json(400점, 2쪽)만 받고
    브랜드 칸이 Leica이고 판매 중인 것만 (컬렉션에 라이카 마운트용 다른 회사 렌즈가 섞여 있음). 가격은 USD.
    등급 표기는 없고 설명 【Appearance】 문장 말투('relatively good condition compared to other used products')"""
    import html as _html
    import requests
    from condition_grade import fivestar_condition
    results = []
    sess = requests.Session()
    sess.headers["User-Agent"] = random.choice(USER_AGENTS)
    base = "https://five-star-camera.com"
    print(f"\n  📂 Five Star Camera 크롤링 시작")
    for p in _shopify_all(sess, f"{base}/collections/leica/products.json", "Five Star Camera"):
        if (p.get("vendor") or "").strip().lower() != "leica":
            continue
        variants = p.get("variants") or [{}]
        if not any(v.get("available") for v in variants):
            continue
        title = re.sub(r"\s+", " ", _html.unescape(p.get("title") or "")).strip()
        if not re.search(r"[A-Za-z]{3}", re.sub(r"from Japan", "", title, flags=re.I)):
            continue  # 제목이 '- from Japan'뿐인 상품
        # 'Very Rare!! …', '… 2026.09 Overhauled!!', '… w/ Box from Japan', '※Read!' 같은 꼬리말 떼기
        name = re.sub(r"^(?:Very\s+)?(?:Rare|Good|Mint)!+\s*|\s*※.*$|\s+from Japan\b.*$", "", title, flags=re.I)
        name = re.sub(r"\b20\d\d\.\d{1,2}\s+Overhauled!*|\bw/\s*Box\b|\s*!+$", " ", name, flags=re.I)
        name = re.sub(r"\bf/(\d)", r"f\1", name)
        name = re.sub(r"\s+", " ", name).strip(" ,-")
        if not re.match(r"(?:leica|leitz)\b", name, re.I):
            name = "Leica " + name
        try:
            price = f"${float(variants[0].get('price')):,.0f}"
        except (TypeError, ValueError):
            price = "문의요망"
        cat = "Accessory" if (p.get("product_type") or "").lower() == "accessories" else detect_category(name, price)
        mount = 'Accessory' if cat == 'Accessory' else detect_mount(name)
        img = p["images"][0].get("src", "") if p.get("images") else ""
        results.append({
            "게시일": _shopify_listed(p),
            "site": "Five Star Camera (일본)",
            "label": auto_label(name),
            "상품명": name,
            "세대": detect_generation(name),
            "컨디션": fivestar_condition(p.get("body_html") or "") or "정보없음",
            "가격": price,
            "통화": "USD",
            "이미지": img,
            "링크": f"{base}/products/{p['handle']}",
            "품절": False,
            "예약중": False,
            "mount": mount,
            "category": cat,
            "brand": detect_brand(name),
        })
    print(f"  ✅ Five Star Camera 완료: {len(results)}개")
    return results


def _konstanz_name(title, cat_slug):
    """Leica Store Konstanz 제목 다듬기: 'Summilux-M35/1,4   #4947321    (11727)' → 'Leica Summilux-M 35mm f1.4'.
    일련번호('#…')·주문번호('(11727)'·'14402')·소수점 쉼표·'cm' 초점거리를 고치고, 독일어 색·액세서리 말은 영어로.
    M39 분류 렌즈는 'L39', R 분류의 'SL Mot'은 Leicaflex SL"""
    t = re.sub(r"#\s?[A-Z]{0,2}\d{4,}|\(\s*#?\d{4,}\s*\)|\(\s*\d{5}\s*(?:[+/]\s*\d{5}\s*)?\)|(?<![\d/.-])\b\d{5}\b(?:\s*[+/]\s*\d{5})*", " ", title)
    t = re.sub(r"\((?:letzte Generation|canada|SOONC-MW|Leica-Store-Konstanz-edition)\)", " ", t, flags=re.I)
    t = re.sub(r"(\d),(\d)", r"\1.\2", t)
    t = re.sub(r"(\d+(?:\.\d)?)\s?cm\b", lambda m: f"{round(float(m.group(1)) * 10)}mm", t)
    t = re.sub(r"(?<=[A-Za-z])-?\s?(?=\d{2,3}(?:-\d{2,3})?(?:mm)?\s?/)", " ", t)  # 'Summilux-M35/' → 'Summilux-M 35/'
    t = re.sub(r"\b(\d{2,3}(?:-\d{2,3})?)\s?(?:mm)?\s?/\s?(\d+(?:\.\d+)?(?:-\d+(?:\.\d+)?)?)", r"\1mm f\2", t)
    t = re.sub(r"\b(\d{2,3}(?:-\d{2,3})?mm)\s+(\d(?:\.\d)?)\b", r"\1 f\2", t)  # 'Summar 50mm 2.0' → 'f2.0'
    t = re.sub(r"(?<=-[MRS])(?=\d)|(?<=-SL)(?=\d)|(?<=-TL)(?=\d)", " ", t)
    for de, en in (("schwarz lackiert", "black paint"), ("schwarz", "black"), ("silber", "silver"), ("grau", "grey"),
                   ("anthrazit", "anthracite"), ("\\bChrom\\b", "chrome"), ("Doppelzug", "double stroke"), ("mit Brille", "goggles"),
                   ("mit ROM", "ROM"), ("Spiegelsucher", "mirror finder"), ("Sucher", "finder"), ("Geli\\b", "hood"),
                   ("Gegenlichtblende", "hood"), ("Multifunktions-Handgriff|Multifunktionshandgriff", "multifunction handgrip"),
                   ("Handgriff", "handgrip"), ("Bereitschaftstasche|Bereichtsschaftstasche|Every ready case", "ever ready case"),
                   ("Ledertasche|Leidertasche", "leather case"), ("Protektor", "protector"), ("Daumenstütze", "thumb support"),
                   ("Kugelgelenkkopf", "ball head"), ("Bodenplatte", "base plate"), ("Stativschelle", "tripod collar"),
                   ("Tasche", "bag"), ("für", "for"), ("Handschlaufe", "hand strap")):
        t = re.sub(de, en, t, flags=re.I)
    t = re.sub(r"\b(\d{2,3}-\d{2,3})\b(?!mm)", r"\1mm", t)  # 'SL 16-35' → '16-35mm'
    t = re.sub(r"\bM \((\d{3})\)", r"M Typ \1", t)
    t = re.sub(r"\bS \((\d{3})\)", r"S Typ \1", t)
    t = re.sub(r"\bM9\s*[–-]\s*Monochrom\b", "M9 Monochrom", t)
    t = re.sub(r"Macro-Elmar-R(?= ?60)", "Macro-Elmarit-R", t)  # 매장 오타 (R 60은 Macro-Elmarit)
    t = re.sub(r"Vario-Apo-Elmarit-R", "APO-Vario-Elmarit-R", t, flags=re.I)
    t = re.sub(r"Super-Vario-Elmarit-SL(?= ?16-35)", "Super-Vario-Elmar-SL", t)
    t = re.sub(r"\bPA-Curtagon(?!-R)", "PA-Curtagon-R", t)
    if re.match(r"(?:Leica\s+)?hood\b", t, re.I):
        t = re.sub(r"(\d{2,3})mm f(\d)", r"\1/\2", t)  # 후드에 붙은 '28mm f2.8'이 렌즈로 읽히지 않게
    if cat_slug == "leica-r-gehaeuse":
        t = re.sub(r"^(?:Leica\s+)?SL[\s-]?Mot\b", "Leicaflex SL MOT", t, flags=re.I)
    if cat_slug == "leica-m39" and re.search(r"\d{2,3}mm", t) and not re.search(r"M39|L39|LTM", t):
        t += " L39"
    t = re.sub(r"\s+", " ", t).strip(" -–,")
    if not re.match(r"(?:leica|leitz|ernst)", t, re.I):
        t = "Leica " + t
    return t


def crawl_konstanz():
    """Leica Store Konstanz (독일) - 라이카 매장의 'Gelegenheiten'(중고·진열품) 분류 11곳. 워드프레스 정적 HTML, 분류마다 한 쪽에 다 나옴
    (합쳐 300점 안팎). 카드에 이름·한 줄 설명('gebraucht – sehr guter Zustand')·가격('EURO 5.390.-')·사진(없으면 회색 그림).
    'Restposten'(남은 새 액세서리)·쌍안경·다른 회사(Voigtländer 등) 분류는 뺌. 가격 없는 카드는 '문의요망'.
    robots.txt는 /wp-admin/만 막음"""
    import html as _html
    import requests
    from condition_grade import konstanz_condition
    base = "https://www.leica-store-konstanz.de"
    site = "Leica Store Konstanz (독일)"
    cats = ("leica-m-kameras-analog", "leica-m-kameras-digital", "leica-m-objektive", "leica-m39", "leica-q",
            "leica-r-gehaeuse", "leica-r-objektive", "leica-s-system", "leica-sl", "leica-kompakt-kameras", "leica-aps-c-system")
    sess = requests.Session()
    sess.headers["User-Agent"] = random.choice(USER_AGENTS)
    print("\n  📂 Leica Store Konstanz 크롤링 시작")
    results, seen = [], set()
    for slug in cats:
        try:
            resp = sess.get(f"{base}/gelegenheiten/{slug}/", timeout=30)
            resp.raise_for_status()
        except Exception as e:
            raise RuntimeError(f"Leica Store Konstanz {slug} 못 읽음: {e}")  # 빠진 분류가 판매완료로 바뀌지 않게
        cards = resp.text.split('<div class="product">')[1:]
        print(f"    └─ {slug} {len(cards)}개")
        for card in cards:
            m = re.search(r'<div class="producttext">\s*<a href="([^"]+)">([^<]+)</a>', card)
            if not m or m.group(1) in seen:
                continue
            seen.add(m.group(1))
            title = _html.unescape(m.group(2)).strip()
            if re.search(r"sigma|novoflex|voigtl|oberwerth|artisan|leicatime|crescenza|insta360", title, re.I) or any(b2 in title.lower() for b2 in THIRD_PARTY_BRANDS):
                continue
            desc = re.search(r'class="producttexttext">(.*?)</span>', card, re.S)
            desc = desc.group(1) if desc else ""
            pm = re.search(r'class="lagerstatus">\s*EURO\s*([\d.]+)', card)
            price = f"€{int(pm.group(1).replace('.', '')):,}" if pm and pm.group(1).strip(".") else "문의요망"
            img = re.search(r'<img src="(https?://[^"]+\.(?:jpe?g|png|webp))"', card, re.I)
            name = _konstanz_name(title, slug)
            accessory = re.search(r"handgrip|protector|case|bag|hood|finder|thumb|winder|adapter|extender|base plate|ball head|tripod collar|strap|Visoflex|SF ?\d{2}|Elpro|T-Snap|Display|Holster|Sofort", name, re.I)
            if not accessory and not re.search(r"\d{2,3}mm", name) and slug not in ("leica-m-objektive", "leica-r-objektive"):
                name += " Body"  # 바디 분류의 'Leica R4'·'Leica M-EV1'이 값이 싸거나 이름이 짧아 액세서리·렌즈로 갈리지 않게
            cat = "Accessory" if accessory else detect_category(name, price)
            mount = 'Accessory' if cat == 'Accessory' else detect_mount(name)
            results.append({
                "site": site,
                "label": auto_label(name),
                "상품명": name,
                "세대": detect_generation(name),
                "컨디션": konstanz_condition(desc) or "정보없음",
                "가격": price,
                "통화": "EUR",
                "이미지": img.group(1) if img else "",
                "링크": m.group(1),
                "품절": False,
                "예약중": False,
                "mount": mount,
                "category": cat,
                "brand": detect_brand(name),
            })
        time.sleep(1.5)
    if not results:
        raise RuntimeError("Leica Store Konstanz 목록이 비어 있음")
    print(f"  ✅ Leica Store Konstanz 완료: {len(results)}개")
    return results


def _topcamera_name(title, ja_to_en):
    """トップカメラ 제목 다듬기: '【中古】 ライカ(leica) M3 1ストローク' → 'Leica M3 single stroke'.
    ja_to_en이 모르는 말(セルフ付き·ストローク·後塗り·第3世代·イマレクト·ゾフォート)은 먼저 영어로"""
    t = re.sub(r"【中古】|ライカ\(leica\)\s*(?:ライカ\s+)?", " ", title)
    for ja, en in (("1ストローク", "single stroke"), ("2ストローク", "double stroke"), ("セルフ付き", "self-timer"),
                   ("セルフ無し|セルフ無", "no self-timer"), ("ボタンリワインド", "button rewind"), ("後塗り", "repaint"),
                   (r"第(\d)世代", r"\1th"), ("イマレクト", "Imarect "), ("ゾフォート", "Sofort "), ("レッドシンクロ", "red synchro"),
                   ("プラスチック", "plastic"), ("最短1m", ""), ("フード組込|組込", ""), ("沈胴式", "collapsible"), ("付", "")):
        t = re.sub(ja, en, t)
    t = re.sub(r"\b1th\b", "1st", t)
    t = re.sub(r"\b2th\b", "2nd", t)
    t = re.sub(r"\b3th\b", "3rd", t)
    name = ja_to_en(t)
    name = re.sub(r"\b(I{1,3}) ([a-g])\b", r"\1\2", name)  # 'III f' → 'IIIf'
    name = re.sub(r"\bF/(\d)", r"F\1", name)
    name = re.sub(r"(?<=[A-Za-z])(?=\d{2,3}(?:mm|/))", " ", name)  # 'Summaron35mm' → 'Summaron 35mm'
    name = re.sub(r"[\[\]()（）]", " ", name)
    name = re.sub(r"\s+", " ", name).strip(" -")
    if not re.match(r"(?:leica|leitz)\b", name, re.I):
        name = "Leica " + name
    return name


def crawl_topcamera():
    """トップカメラ (일본) - 중고 카메라점 온라인몰(EC-CUBE). 사이트 검색 '라이카'(name=ライカ, 60개씩 pageno=N, 정적 HTML, 110점 안팎)에서
    제목에 'ライカ(leica)'가 붙은 라이카 상품만 (Sigma·TTArtisan 등 L·M 마운트용 다른 회사 렌즈는 브랜드 표기가 달라 빠짐).
    카드에 이름·등급(AB+·AB·AB-·A)·가격·사진. 중고 대부분이 '실매장에서만 구매' 표시지만 가격·상태 정보로 담음. robots.txt 없음"""
    import html as _html
    import requests
    from ja_normalize import ja_to_en
    base = "https://shop.topcamera.co.jp"
    site = "トップカメラ (일본)"
    sess = requests.Session()
    sess.headers["User-Agent"] = random.choice(USER_AGENTS)
    print("\n  📂 トップカメラ 크롤링 시작")
    results, seen = [], set()
    for page_num in range(1, 15):
        try:
            resp = sess.get(f"{base}/site/products/list", params={"name": "ライカ", "disp_number": 2, "pageno": page_num}, timeout=30)
            resp.raise_for_status()
        except Exception as e:
            raise RuntimeError(f"トップカメラ {page_num}쪽 못 읽음: {e}")  # 빠진 쪽이 판매완료로 바뀌지 않게
        items = re.findall(r'<li class="ec-shelfGrid__item">\s*<a href="([^"]+)">.*?<img src="([^"]+)">.*?<p>([^<]+)</p>\s*<p>([^<]*)</p>\s*'
                           r'<p class="price02-default">\s*([^<]+)</p>', resp.text, re.S)
        print(f"    └─ {page_num}페이지 {len(items)}개")
        for link, img, title, grade, ptxt in items:
            title = _html.unescape(title).strip()
            if link in seen or "ライカ(leica)" not in title:
                continue
            seen.add(link)
            name = _topcamera_name(title, ja_to_en)
            digits = re.sub(r"[^\d]", "", ptxt)
            price = f"¥{int(digits):,}" if digits else "문의요망"
            cat = detect_category(name, price)
            if re.search(r"\bhood\b|finder|adapter|Sofort", name, re.I):
                cat = "Accessory"
            mount = 'Accessory' if cat == 'Accessory' else detect_mount(name)
            results.append({
                "site": site,
                "label": auto_label(name),
                "상품명": name,
                "세대": detect_generation(name),
                "컨디션": grade.strip() or "정보없음",
                "가격": price,
                "통화": "JPY",
                "이미지": base + img if img.startswith("/") else img,
                "링크": link,
                "품절": False,
                "예약중": False,
                "mount": mount,
                "category": cat,
                "brand": detect_brand(name),
            })
        if len(items) < 60:
            break
        time.sleep(2)
    if not results:
        raise RuntimeError("トップカメラ 목록이 비어 있음")
    print(f"  ✅ トップカメラ 완료: {len(results)}개")
    return results


def _komehyo_name(title, ja_to_en):
    """KOMEHYO 제목 다듬기: 전각 글자를 반각으로(NFKC), 줄임말 'S.VARIO-EL-T'·'V-ELMAR-TL'을 풀고,
    'SUMMICRON-M50mm' → 'SUMMICRON-M 50mm', 'F2ASPH' → 'F2 ASPH', '【WEB限定・現状お渡し品】' 떼기"""
    import unicodedata
    t = unicodedata.normalize("NFKC", title)
    t = re.sub(r"【[^】]*】", " ", t)
    t = re.sub(r"\bS\.VARIO-EL-T\s?", "Super-Vario-Elmar-TL ", t, flags=re.I)
    t = re.sub(r"\bV-ELMAR-TL\s?", "Vario-Elmar-TL ", t, flags=re.I)
    for ja, en in (("1回巻き", "single stroke"), ("2回巻き", "double stroke"), ("セルフ付き", "self-timer"), ("0型復刻", "0-Series reissue"),
                   ("シルバー・クローム", "silver chrome"), ("ブラックペイント", "black paint"), ("レッドシンクロ", " red synchro"),
                   ("沈胴式", "collapsible"), ("卓上三脚", "table tripod"), ("ハンドグリップ用フインガーループ", "finger loop for handgrip ")):
        t = t.replace(ja, en)
    t = re.sub(r"BODY(?=\S)", "BODY ", t)
    t = ja_to_en(t)
    t = re.sub(r"(-(?:SL|TL|M|R|S|T))(?=\d)", r"\1 ", t)  # 'SUMMICRON-M50mm' → 'SUMMICRON-M 50mm'
    t = re.sub(r"(F\d(?:\.\d)?)(?=ASPH)", r"\1 ", t)
    t = re.sub(r"(?<=\d)(?=VER\.)|(?<=\d)(?=Ver\.)", " ", t)
    if not re.search(r"\d{2,3}mm|body", t, re.I) and re.search(r"\b(?:T|TL2?|CL|SL[23]?(?:-S)?)\b", t):
        t += " Body"  # 'LEICA T TYP701'·'LEICA TL'이 렌즈·액세서리로 갈리지 않게
    t = re.sub(r"\s+", " ", t).strip(" ,")
    if not re.match(r"(?:leica|leitz)\b", t, re.I):
        t = "Leica " + t
    return t


def crawl_komehyo():
    """KOMEHYO (일본) - 중고 명품·카메라 체인 KOMEHYO ONLINE. 사이트 검색 'LEICA'(정적 HTML, 쪽당 50개, page=N, 60점 안팎)에서
    브랜드 칸이 LEICA인 카메라·렌즈만 (같은 검색에 걸리는 Sigma 'ライカL' 렌즈와 라이카 손목시계 ZM은 뺌).
    카드에 이름(전각)·등급('ランク：中古品B')·매장·가격(할인가 있으면 할인가)·사진. robots.txt 막는 줄 없음. 해외 배송은 대행 주문만"""
    import html as _html
    import requests
    from ja_normalize import ja_to_en
    from condition_grade import KOMEHYO_PREFIX
    import unicodedata
    base = "https://komehyo.jp"
    site = "KOMEHYO (일본)"
    sess = requests.Session()
    sess.headers["User-Agent"] = random.choice(USER_AGENTS)
    print("\n  📂 KOMEHYO 크롤링 시작")
    results, seen = [], set()
    for page_num in range(1, 10):
        try:
            resp = sess.get(f"{base}/search/", params={"q": "LEICA", "page": page_num}, timeout=30)
            resp.raise_for_status()
        except Exception as e:
            raise RuntimeError(f"KOMEHYO {page_num}쪽 못 읽음: {e}")  # 빠진 쪽이 판매완료로 바뀌지 않게
        cards = resp.text.split('<a class="p-link p-link--card"')[1:]
        new = 0
        for card in cards:
            link = re.search(r'href="(/product/[^"]+)"', card)
            nm = re.search(r'productsname">([^<]+)', card)
            brand = re.search(r'txt--brand">([^<]+)', card)
            if not link or not nm or link.group(1) in seen:
                continue
            seen.add(link.group(1))
            new += 1
            title = _html.unescape(nm.group(1)).strip()
            if (brand.group(1).strip().upper() if brand else "") != "LEICA" or re.search(r"ZM\s?\d|自動巻|クォーツ|腕時計", unicodedata.normalize("NFKC", title)):
                continue
            rank = re.search(r'txt--rank">ランク：<span class="p-link__txt--rating">([^<]+)', card)
            prices = re.findall(r'txt--price[^"]*">￥([\d,]+)', card)
            price = f"¥{int(prices[0].replace(',', '')):,}" if prices else "문의요망"
            img = re.search(r'data-src="([^"]+)"', card)
            name = _komehyo_name(title, ja_to_en)
            cat = detect_category(name, price)
            if re.search(r"tripod|三脚|finger ?loop|フインガー|grip|adapter|meter|hood", name, re.I):
                cat = "Accessory"
            mount = 'Accessory' if cat == 'Accessory' else detect_mount(name)
            results.append({
                "site": site,
                "label": auto_label(name),
                "상품명": name,
                "세대": detect_generation(name),
                "컨디션": KOMEHYO_PREFIX + unicodedata.normalize("NFKC", rank.group(1)).strip() if rank else "정보없음",
                "가격": price,
                "통화": "JPY",
                "이미지": img.group(1) if img else "",
                "링크": base + link.group(1),
                "품절": False,
                "예약중": False,
                "mount": mount,
                "category": cat,
                "brand": detect_brand(name),
            })
        print(f"    └─ {page_num}페이지 {len(cards)}개")
        if new == 0:
            break
        time.sleep(2)
    if not results:
        raise RuntimeError("KOMEHYO 목록이 비어 있음")
    print(f"  ✅ KOMEHYO 완료: {len(results)}개")
    return results


def _sabatini_name(title):
    """Sabatini 제목 다듬기: 'USATO Leica Hektor 13,5 cm f/4' → 'Leica Hektor 135mm f4'. 앞의 'USATO'·'KIT', 딸린 것('+ accessori'·
    '+ Visoflex 2'·'con Brightin Star …'), 이탈리아어 액세서리 말(mirino·paraluce·tracolla …)을 영어로"""
    t = re.sub(r"^\s*(?:usato|kit)\s+(?:kit\s+)?", "", title.strip(), flags=re.I)
    t = re.sub(r"\s*\+\s*(?:accessori|visoflex.*)$|\s+con\s+.*$|\s*\(\d{4}\)", "", t, flags=re.I)
    t = re.sub(r"(\d)\s?,\s?(\d)", r"\1.\2", t)
    t = re.sub(r"(\d+(?:\.\d)?)\s?cm\b", lambda m: f"{round(float(m.group(1)) * 10)}mm", t)
    t = re.sub(r"\bf\s?/\s?(\d)|\bf (\d)", lambda m: "f" + (m.group(1) or m.group(2)), t, flags=re.I)
    t = re.sub(r"(\d)m (?=f\d)", r"\1mm ", t)  # '90m f2' 오타
    t = re.sub(r"\bAPO-\s+MACRO-\s+", "APO-Macro-", t, flags=re.I)
    t = re.sub(r"\s1:\d(?:\.\d)?$", "", t)
    t = re.sub(r"(\d)MM\b", r"\1mm", t)
    for it, en in (("mirino", "finder"), ("paraluce", "hood"), ("tracolla", "strap"), ("impugnatura", "handgrip"), ("custodia", "case"),
                   ("fondina in pelle", "leather holster"), ("borsa", "bag"), ("lentina di correzione", "correction lens"),
                   ("soffietto", "bellows"), ("caricabatteria", "charger"), ("tubo", "tube"), ("poggia pollice", "thumb support"),
                   ("laccetto da polso", "wrist strap"), ("per ", "for ")):
        t = re.sub(rf"\b{it}\b", en, t, flags=re.I)
    t = re.sub(r"\s+", " ", t).strip(" -–")
    if not re.match(r"(?:leica|leitz)\b", t, re.I):
        t = "Leica " + re.sub(r"^leica\s+", "", t, flags=re.I)
    return t


def crawl_msmateriale():
    """M&S Materiale Fotografico (이탈리아, 로마) - 라이카 중고 분류 6곳(정적 HTML, 쪽 넘김 없이 한 화면에 전부, 약 220개)의 카드에
    이름·가격·사진·등급('Condizioni: B+'). 팔린 것은 'Venduto' 띠를 달고 목록에 남아 품절로 담음. 가격 EUR.
    매장의 액세서리 분류에도 렌즈·바디가 섞여 있어 분류는 이름으로 (crawl_all 끝에서 어차피 다시 정함)"""
    import html as _html
    import requests
    from condition_grade import MS_PREFIX
    base = "https://www.msmaterialefotografico.it/product-category/"
    cats = ["fotocamere-leica-m", "obiettivi-leica-m-usati", "fotocamere-leica-r", "obiettivi-leica-r", "Leica-tl",
            "accessori-leica-usati"]
    site = "M&S Materiale Fotografico (이탈리아)"
    sess = requests.Session()
    sess.headers["User-Agent"] = random.choice(USER_AGENTS)
    print("\n  📂 M&S Materiale Fotografico 크롤링 시작")
    results, seen = [], set()
    for cat_slug in cats:
        try:
            resp = sess.get(base + cat_slug + "/", timeout=60)
            resp.raise_for_status()
        except Exception as e:
            raise RuntimeError(f"M&S {cat_slug} 못 읽음: {e}")  # 빠진 분류가 판매완료로 바뀌지 않게
        cards = re.findall(r'<div class="al_archive product-(\d+)[^"]*">(.*?)</a>\s*</div>', resp.text, re.S)
        print(f"    └─ {cat_slug} {len(cards)}개")
        for pid, card in cards:
            if pid in seen:
                continue
            seen.add(pid)
            link = re.search(r'<a href="([^"]+)"', card)
            title = re.search(r'<h3 class="product-name[^"]*">(.*?)</h3>', card, re.S)
            if not link or not title:
                continue
            title = _html.unescape(re.sub(r"<[^>]+>", "", title.group(1))).strip()
            if re.search(r"panasonic|voigtl|zeiss|minolta|sigma|tamron|canon|nikon|angenieux|schneider|xenogon", title, re.I):
                continue
            name = re.sub(r"\b(?:obiettivo|fotocamera|corpo macchina|macchina fotografica)\s+", "", title, flags=re.I)
            name = re.sub(r"\s*\((?:leggere|leggi|vedi)(?: bene)? (?:la )?descrizione\)|\s+leggere descrizione$|\s*\(come nuov[ao]\)",
                          "", name, flags=re.I)
            name = re.sub(r"\s+[–-]\s+(SL|TL|[MRSPC])\b", r"-\1", name)  # 'Summilux – M' → 'Summilux-M'
            name = re.sub(r"\b(APO|Super)\s*[–-]\s*", r"\1-", name)       # 'APO – Summicron' · 'Super- Angulon'
            name = re.sub(r"^(Leica|Leitz)[- ](SL|TL|R|M)\s+((?:APO-|Vario-|Super-|Tele-)?(?:Summilux|Summicron|Summarit|Elmarit|Elmar|"
                          r"Telyt|Noctilux|Summaron|Angulon))\b(?!-)", r"\1 \3-\2", name, flags=re.I)  # 'Leica R Summilux' → 'Leica Summilux-R'
            name = re.sub(r"\b(Angulon|Summilux|Summicron|Elmarit|Elmar|Telyt)\s+(R|M)\b", r"\1-\2", name)  # 'Super-Angulon R'
            for it, en in (("titanio", "Titanium"), ("visore", "viewer"), ("adattatore", "adapter"), ("anello", "ring"),
                           ("lente di correzione diottrica", "diopter correction lens"), ("nero", "black"), ("cromato", "chrome")):
                name = re.sub(rf"\b{it}\b", en, name, flags=re.I)
            name = _sabatini_name(name)
            if any(b2 in name.lower() for b2 in THIRD_PARTY_BRANDS):
                continue
            grade = re.search(r'Condizioni:</span>\s*<span class="attribute-value-listing">([^<]*)</span>', card)
            grade = re.sub(r"\s+", "", grade.group(1)) if grade else ""
            sold = "mes-ribbon-sold" in card or grade.lower() == "venduto"
            pm = re.search(r'product-price[^"]*">([\d.]+)(?:,\d+)?\s*€', card)
            price = f"€{int(pm.group(1).replace('.', '')):,}" if pm else "문의요망"
            img = re.search(r'<img[^>]+src="([^"]+)"', card)
            cat = detect_category(name, price)
            mount = 'Accessory' if cat == 'Accessory' else detect_mount(name)
            results.append({
                "site": site,
                "label": auto_label(name),
                "상품명": name,
                "세대": detect_generation(name),
                "컨디션": MS_PREFIX + grade if grade and not sold else "정보없음",
                "가격": price,
                "통화": "EUR",
                "이미지": img.group(1) if img else "",
                "링크": link.group(1),
                "품절": sold,
                "예약중": False,
                "mount": mount,
                "category": cat,
                "brand": detect_brand(name),
            })
        time.sleep(1)
    if not results:
        raise RuntimeError("M&S 목록이 비어 있음")
    print(f"  ✅ M&S Materiale Fotografico 완료: {len(results)}개")
    return results


def _leicastorepl_name(title):
    """Leica Store Poland 제목 다듬기: 'Leica 28 f/5.6 SUMMARON-M Matt Black' → 'Leica Summaron-M 28mm f5.6 Matt Black',
    'Leica Summilux-M 1:1.4/35 ASPH. LE11663 + zestaw filtrów' → 'Leica Summilux-M 35mm f1.4 ASPH. 11663'. 폴란드어 꼬리말(상태·구성품) 뺌"""
    t = re.sub(r"\s+-\s+(?:stan|pełen|komplet).*$|\s*\+\s*(?:zestaw|akcesoria|filtr).*$|\s*/\s*F\.\s*VAT$", "", title.strip(), flags=re.I)
    t = re.sub(r"\bLE(\d{5})\b", r"\1", t)
    t = re.sub(r"(\d)\s?,\s?(\d)", r"\1.\2", t)
    t = re.sub(r"\b(\d+(?:\.\d)?)\s?cm\b", lambda m: f"{round(float(m.group(1)) * 10)}mm", t)
    t = re.sub(r"\b1:(\d(?:\.\d+)?)\s*/\s*(\d{2,3})\b", r"\2mm f\1", t)          # '1:1.4/35' → '35mm f1.4'
    t = re.sub(r"\b(\d{2,3})\s*/\s*(\d\.\d+|\d)\b(?!\s*mm)", r"\1mm f\2", t)       # '35/1.4' → '35mm f1.4'
    t = re.sub(r"\bf\s?/\s?(\d)", r"f\1", t, flags=re.I)
    t = re.sub(r"^(Leica|Leitz)\s+(\d{2,3})(?:mm)?\s+(f\d(?:\.\d+)?)\s+([A-Z][A-Z-]+(?:-[A-Z]+)?)", r"\1 \4 \2mm \3", t)  # 숫자 먼저 → 이름 먼저
    t = re.sub(r"\b(APO|SUMMICRON|SUMMILUX|SUMMARON|ELMARIT|ELMAR|NOCTILUX|SUMMARIT|TELE|SUPER|ELMAR|HEKTOR|ASPH)\b",
               lambda m: m.group(1).capitalize() if m.group(1) not in ("APO", "ASPH") else m.group(1), t)
    t = re.sub(r"\b(Summicron|Summilux|Summaron|Elmarit|Elmar|Noctilux|Summarit)-m\b", r"\1-M", t, flags=re.I)
    t = re.sub(r"\s+", " ", t).strip(" -")
    return t


def crawl_leicastorepl():
    """Leica Store Poland (폴란드, 바르샤바 공식 매장) - 중고(komis) 목록 정적 HTML 쪽마다 16개(5쪽 안팎, 이름순)에서 Leica·Leitz만 골라
    상세 화면을 읽음 (가격은 목록에 없고 스크립트로 채움). 상세의 itemprop price·availability, 설명 첫 문장의 상태 말
    ('w stanie dobrym'·'stan idealny'). robots.txt Crawl-delay 2초를 지킴 → 약 2분, 6시간마다. 가격 PLN"""
    import html as _html
    import requests
    from condition_grade import leicastorepl_condition
    base = "https://leicastore.pl"
    site = "Leica Store Poland (폴란드)"
    sess = requests.Session()
    sess.headers["User-Agent"] = random.choice(USER_AGENTS)
    print("\n  📂 Leica Store Poland 크롤링 시작")
    cards, seen = [], set()
    for page_num in range(1, 21):
        url = f"{base}/komis" + (f"/page:{page_num}" if page_num > 1 else "")
        try:
            resp = sess.get(url, timeout=60)
            resp.raise_for_status()
        except Exception as e:
            raise RuntimeError(f"Leica Store Poland {page_num}쪽 못 읽음: {e}")  # 빠진 쪽이 판매완료로 바뀌지 않게
        found = re.findall(r'<h2 class="product-name">\s*<a data-type="product-url" href="([^"]+)" title="([^"]*)"', resp.text)
        print(f"    └─ {page_num}페이지 {len(found)}개")
        for href, title in found:
            title = _html.unescape(_html.unescape(title)).strip()
            if href not in seen and re.match(r"(?:leica|leitz)\b", title, re.I):
                seen.add(href)
                cards.append((base + href, title))
        time.sleep(2)
        if f"/komis/page:{page_num + 1}" not in resp.text:
            break
    results = []
    for link, title in cards:
        try:
            h = sess.get(link, timeout=60).text
        except Exception as e:
            print(f"    ⚠️ 상세 오류 {link[-40:]}: {e}")
            continue
        finally:
            time.sleep(2)
        pm = re.search(r'data-type="product-price">\s*([\d\s]+)(?:,\d+)?\s*Z[ŁL]', h, re.I)
        amount = int(re.sub(r"\s", "", pm.group(1))) if pm else 0
        price = f"{amount:,} zł" if amount else "문의요망"
        stock = re.search(r'itemprop="availability" content="([^"]+)"', h)
        desc = re.search(r'itemprop="description">(.*?)</div>', h, re.S)
        img = re.search(r'itemprop="image" content="([^"]+)"', h)
        name = _leicastorepl_name(title)
        if any(b2 in name.lower() for b2 in THIRD_PARTY_BRANDS):
            continue
        cat = detect_category(name, price)
        mount = 'Accessory' if cat == 'Accessory' else detect_mount(name)
        results.append({
            "site": site,
            "label": auto_label(name),
            "상품명": name,
            "세대": detect_generation(name),
            "컨디션": leicastorepl_condition(title + " " + (desc.group(1) if desc else "")) or "정보없음",
            "가격": price,
            "통화": "PLN",
            "이미지": img.group(1) if img else "",
            "링크": link,
            "품절": bool(stock) and "InStock" not in stock.group(1),
            "예약중": False,
            "mount": mount,
            "category": cat,
            "brand": detect_brand(name),
        })
    if not results:
        raise RuntimeError("Leica Store Poland 목록이 비어 있음")
    print(f"  ✅ Leica Store Poland 완료: {len(results)}개")
    return results


def _photowarehouse_name(title):
    """Photo Warehouse 제목 다듬기: 'Leica MF 13.5cm F4.5 Hektor M Mount Lens' → 'Leica 135mm f4.5 Hektor', 'in LTM Mount' → '(M39)'"""
    name = re.sub(r"\b(?:MF|AF)\s+", "", title)
    name = re.sub(r"\s*-?\s*\(see description\)", "", name, flags=re.I)
    name = re.sub(r"\bModel (\d{2}) ?(\d{3})\b", r"\1\2", name)  # 'Model 10 760' → '10760' (제품 코드)
    name = re.sub(r"^Leica Monochrom\b", "Leica M Monochrom", name)
    name = re.sub(r"^Ernst Leitz Wetzlar\b", "Leitz", name)
    name = re.sub(r"(\d+),(\d)cm\b", r"\1.\2cm", name)
    name = re.sub(r"\b(\d+(?:\.\d)?)cm\b", lambda m: f"{round(float(m.group(1)) * 10)}mm", name)
    name = re.sub(r"\bF/?(\d)", r"f\1", name)
    name = re.sub(r"\s+(?:lens\s+)?(?:in\s+)?LTM\s+mount\b|\s+L39\b", " (M39)", name, flags=re.I)
    name = re.sub(r"\s+-?\s*(?:lens\s+)?(?:in\s+)?(?:Leica\s+)?M\s+mount\b(?:\s+lens)?|\s+lens\s*$", "", name, flags=re.I)
    return re.sub(r"\s+", " ", name).strip(" -")


def crawl_photowarehouse():
    """Photo Warehouse (뉴질랜드, 오클랜드 등 6개 매장) - 중고 'rangefinders' 분류(사이트에서 'Leica cameras and lenses' 묶음)를
    ?display=all 한 화면(80여 개 카드)으로 읽고, Leica·Leitz만 골라 상세의 구조화 데이터(Product)에서 설명·사진·가격(NZD)·재고.
    상태는 짧은 설명 글('Excellent condition')로 (설명이 '1954 red dial'처럼 상태 말이 없으면 등급 없음). 1초씩 쉼 → 약 1분, 6시간마다"""
    import html as _html
    import requests
    from condition_grade import describe_text
    base = "https://www.photowarehouse.co.nz"
    site = "Photo Warehouse (뉴질랜드)"
    sess = requests.Session()
    sess.headers["User-Agent"] = random.choice(USER_AGENTS)
    print("\n  📂 Photo Warehouse 크롤링 시작")
    try:
        resp = sess.get(base + "/shop/second-hand-products/rangefinders", params={"display": "all"}, timeout=90)
        resp.raise_for_status()
    except Exception as e:
        raise RuntimeError(f"Photo Warehouse 목록 못 읽음: {e}")  # 빈 목록이 판매완료로 바뀌지 않게
    cards = re.findall(r'<a href="(/shop/second-hand-products/rangefinders/[a-z0-9-]+)"[^>]*class="simple-product__link">.*?'
                       r'<span class="simple-product__title">([^<]*)</span>', resp.text, re.S)
    print(f"    └─ 목록 {len(cards)}개")
    results, seen = [], set()
    for href, title in cards:
        title = _html.unescape(title).strip()
        if href in seen or not re.search(r"\b(?:leica|leitz)\b", title, re.I) or re.search(
                r"voigtl|canon|nikon|zeiss|kmz|\bfed\b|zorki|jupiter", title, re.I):
            continue
        seen.add(href)
        try:
            h = sess.get(base + href, timeout=60).text
        except Exception as e:
            print(f"    ⚠️ 상세 오류 {href[-40:]}: {e}")
            continue
        finally:
            time.sleep(1)
        prod = {}
        for block in re.findall(r'<script type="application/ld\+json">(.*?)</script>', h, re.S):
            try:
                data = json.loads(block)
            except ValueError:
                continue
            if isinstance(data, dict) and data.get("@type") == "Product":
                prod = data
        name = _photowarehouse_name(title)
        if any(b2 in name.lower() for b2 in THIRD_PARTY_BRANDS):
            continue
        offer = prod.get("offers") or {}
        try:
            price = f"NZ${float(offer.get('price')):,.0f}"
        except (TypeError, ValueError):
            price = "문의요망"
        imgs = prod.get("image") or []
        cat = detect_category(name, price)
        mount = 'Accessory' if cat == 'Accessory' else detect_mount(name)
        results.append({
            "site": site,
            "label": auto_label(name),
            "상품명": name,
            "세대": detect_generation(name),
            "컨디션": describe_text(prod.get("description") or "") or "정보없음",
            "가격": price,
            "통화": "NZD",
            "이미지": imgs[0] if isinstance(imgs, list) and imgs else "",
            "링크": base + href,
            "품절": bool(offer) and "InStock" not in str(offer.get("availability") or ""),
            "예약중": False,
            "mount": mount,
            "category": cat,
            "brand": detect_brand(name),
        })
    if not results:
        raise RuntimeError("Photo Warehouse 목록이 비어 있음")
    print(f"  ✅ Photo Warehouse 완료: {len(results)}개")
    return results


def crawl_sabatini():
    """Sabatini Fotografia (이탈리아, 로마) - 중고 카메라·렌즈 WooCommerce 상품 API(Store API). 중고 분류 3곳(obiettivi-usati 240·
    macchine-fotografiche-usate 371·accessori-usati 184)에서 'leica' 검색, 100개씩. Panasonic Leica DG·Voigtländer·Techart 등
    다른 회사 것과 쌍안경·현미경은 뺌. 판매 끝난 것도 목록에 남아(is_in_stock false) 품절로 담음. 가격 EUR.
    등급은 상품 속성 'Condizioni' (AB·BA·B+·B+/B·B)"""
    import html as _html
    import requests
    from condition_grade import SABATINI_PREFIX
    base = "https://sabatinifotografia.it"
    site = "Sabatini Fotografia (이탈리아)"
    sess = requests.Session()
    sess.headers["User-Agent"] = random.choice(USER_AGENTS)
    print("\n  📂 Sabatini Fotografia 크롤링 시작")
    results, seen = [], set()
    for cat_id in (240, 371, 184):
        for page_num in range(1, 10):
            try:
                resp = sess.get(f"{base}/wp-json/wc/store/v1/products",
                                params={"category": cat_id, "search": "leica", "per_page": 100, "page": page_num}, timeout=60)
                resp.raise_for_status()
                products = resp.json()
            except Exception as e:
                raise RuntimeError(f"Sabatini 분류 {cat_id} {page_num}쪽 못 읽음: {e}")  # 빠진 쪽이 판매완료로 바뀌지 않게
            print(f"    └─ 분류 {cat_id} {page_num}페이지 {len(products)}개")
            for p in products:
                if p.get("id") in seen:
                    continue
                seen.add(p.get("id"))
                title = _html.unescape(p.get("name") or "").strip()
                if not re.search(r"\b(?:leica|leitz)\b", title, re.I) or re.search(
                        r"panasonic|voigtl|techart|brightin|lumix|noctivid|microscope|binocol|\d+\s?[x×]\s?\d{2}\b", title, re.I):
                    continue
                name = _sabatini_name(title)
                if any(b2 in name.lower() for b2 in THIRD_PARTY_BRANDS):
                    continue
                fm = re.fullmatch(r"(?i)(?:leica|leitz)(?: leitz)?(?: (R|M))? (\d{2,3})mm f(\d(?:\.\d+)?)", name)
                if fm:  # 'Leica 21mm F2.8'처럼 렌즈 이름이 없으면 설명의 'BAIONETTA: Leica-R'로 마운트를 보고 하나로 정해질 때만 채움
                    desc = _html.unescape(re.sub(r"<[^>]+>", " ", p.get("description") or "") + " " + (p.get("short_description") or ""))
                    bm = fm.group(1) or (re.search(r"baionetta\s*:?\s*leica[\s-]*([RM])\b", desc, re.I) or [None, None])[1]
                    fam = _KOOKMIN_FAMILY.get((bm or "").upper(), {}).get((int(fm.group(2)), float(fm.group(3))))
                    if fam:
                        name = f"Leica {fam} {fm.group(2)}mm f{fm.group(3)}"
                prices = p.get("prices") or {}
                try:
                    price = f"€{int(prices.get('price')) / 10 ** int(prices.get('currency_minor_unit', 2)):,.0f}"
                except (TypeError, ValueError):
                    price = "문의요망"
                grade = next((t.get("name") for a in p.get("attributes") or [] if a.get("name") == "Condizioni"
                              for t in a.get("terms") or []), None)
                img = p["images"][0].get("src", "") if p.get("images") else ""
                cat = "Accessory" if cat_id == 184 else detect_category(name, price)
                mount = 'Accessory' if cat == 'Accessory' else detect_mount(name)
                results.append({
                    "site": site,
                    "label": auto_label(name),
                    "상품명": name,
                    "세대": detect_generation(name),
                    "컨디션": SABATINI_PREFIX + grade.strip() if grade else "정보없음",
                    "가격": price,
                    "통화": "EUR",
                    "이미지": img,
                    "링크": p.get("permalink") or "",
                    "품절": not p.get("is_in_stock"),
                    "예약중": False,
                    "mount": mount,
                    "category": cat,
                    "brand": detect_brand(name),
                })
            if len(products) < 100:
                break
            time.sleep(2)
    if not results:
        raise RuntimeError("Sabatini 목록이 비어 있음")
    print(f"  ✅ Sabatini Fotografia 완료: {len(results)}개")
    return results


def crawl_leicastoreamsterdam():
    """Leica Store Amsterdam (네덜란드) - 라이카 매장의 공인 중고(CPO). Lightspeed 쇼핑몰이라 분류 목록에 ?format=json.
    Used Cameras·Used Lenses·Used Accessories를 100개씩 (판매 중만 목록에 나옴, 합쳐 60점 안팎).
    등급 표기는 없고 상품 화면 설명 문장('shows minimal traces of use')이라 상품마다 ?format=json을 한 번씩 더 받음.
    robots.txt Crawl-delay 2초 지킴"""
    import requests
    from condition_grade import lsa_condition
    results, seen = [], set()
    base = "https://www.leicastoreamsterdam.nl"
    print(f"\n  📂 Leica Store Amsterdam 크롤링 시작")
    s = requests.Session()
    s.headers["User-Agent"] = random.choice(USER_AGENTS)
    for cat_slug in ("used-cameras", "used-lenses", "used-accessories"):
        for page_num in range(1, 10):
            resp = s.get(f"{base}/used-leica/{cat_slug}/page{page_num}.html", params={"format": "json", "limit": 100}, timeout=30)
            resp.raise_for_status()  # 빠진 분류가 판매완료로 바뀌지 않게 실패로
            col = resp.json().get("collection") or {}
            prods = col.get("products") or {}
            items = list(prods.values()) if isinstance(prods, dict) else list(prods)
            print(f"    └─ {cat_slug} {page_num}페이지 {len(items)}개 상품 발견")
            time.sleep(2)
            for p in items:
                link = f"{base}/{p.get('url', '')}"
                if not p.get("url") or link in seen or not p.get("available", True):
                    continue
                seen.add(link)
                # 'Leica Q2, Used.' · 'Leica M10 monochrom, Used s/n 5617164' · 'M10 Black Paint Finish, Used.'
                name = re.sub(r"[,.\s]*\b(?:used|demo)\b.*$|\s*s/n\.?\s*\d+.*$", "", p.get("title") or "", flags=re.I)
                name = re.sub(r"^Leica,\s*", "Leica ", name.strip(" ,."))
                name = re.sub(r"\bVari0\b", "Vario", name)
                name = re.sub(r"(?<=[A-Za-z])\s*-\s+(?=[A-Z])", "-", name)  # 'APO-SUMMICRON- SL'
                name = re.sub(r"\bVario-Elmarit 2\.8 24-70\b", "Vario-Elmarit-SL 24-70mm f2.8", name)  # SL 렌즈인데 SL이 빠짐
                name = re.sub(r"\bSL-2\b", "SL2", name)
                name = re.sub(r"\bf/(\d)", r"f\1", name)
                name = re.sub(r"\s+", " ", name).strip(" ,.")
                if not re.match(r"(?:leica|leitz)\b", name, re.I):
                    name = "Leica " + name
                cond = "정보없음"
                try:
                    detail = s.get(f"{link}?format=json", timeout=30).json().get("product") or {}
                    cond = lsa_condition(detail.get("content") or "") or "정보없음"
                except Exception as e:
                    print(f"    ⚠️ 상세 못 읽음 {link}: {e}")
                time.sleep(2)
                amount = ((p.get("price") or {}).get("price_incl")) or 0
                price = f"€{float(amount):,.0f}" if amount else "문의요망"
                img = f"https://cdn.webshopapp.com/shops/241792/files/{p['image']}/file.jpg" if p.get("image") else ""
                cat = detect_category(name, price)
                mount = 'Accessory' if cat == 'Accessory' else detect_mount(name)
                results.append({
                    "site": "Leica Store Amsterdam (네덜란드)",
                    "label": auto_label(name),
                    "상품명": name,
                    "세대": detect_generation(name),
                    "컨디션": cond,
                    "가격": price,
                    "통화": "EUR",
                    "이미지": img,
                    "링크": link,
                    "품절": False,
                    "예약중": False,
                    "mount": mount,
                    "category": cat,
                    "brand": detect_brand(name),
                })
            if not col.get("page_next"):
                break
    print(f"  ✅ Leica Store Amsterdam 완료: {len(results)}개")
    return results


def crawl_oneofmany():
    """One Of Many Cameras (덴마크) - 코펜하겐 중고·렌탈점 Shopify products.json 전체(3,900개쯤, 16쪽)에서 브랜드 칸이 Leica이고
    상품 종류가 'Used …'·'Brugt'(중고)인 것만 (Rental·New는 뺌). 가격은 DKK. 등급 표기는 없고 설명 말투('Mint condition')"""
    import html as _html
    import requests
    from condition_grade import describe_text
    results = []
    sess = requests.Session()
    sess.headers["User-Agent"] = random.choice(USER_AGENTS)
    base = "https://oneofmanycameras.com"
    print(f"\n  📂 One Of Many Cameras 크롤링 시작")
    for p in _shopify_all(sess, f"{base}/products.json", "One Of Many Cameras"):
        ptype = (p.get("product_type") or "").strip().lower()
        if (p.get("vendor") or "").strip().lower() != "leica" or not re.match(r"used|brugt", ptype):
            continue
        variants = p.get("variants") or [{}]
        if not any(v.get("available") for v in variants):
            continue
        title = re.sub(r"\s+", " ", _html.unescape(p.get("title") or "")).strip()
        if any(b2 in title.lower() for b2 in THIRD_PARTY_BRANDS) or re.search(r"cine ?mod|canon ef|sony e\b", title, re.I):
            continue  # 다른 마운트로 개조한 렌즈
        name = re.sub(r"\s+-\s+cl'?a\b.*$|\s*-\s*$", "", title, flags=re.I)  # '- cl'a October 2024' (정비 날짜)
        name = re.sub(r"^Original\s+", "", name, flags=re.I)
        name = re.sub(r"\b(\d{1,2}(?:\.\d)?)\s?cm\b", lambda m: f"{round(float(m.group(1)) * 10):d}mm", name)  # '5cm f2 Summicron III 11818'
        if not re.match(r"(?:leica|leitz)\b", name, re.I):
            name = "Leica " + name
        try:
            price = f"DKK {float(variants[0].get('price')):,.0f}"
        except (TypeError, ValueError):
            price = "문의요망"
        cat = "Lens" if "lens" in ptype else "Body" if "camera" in ptype else "Accessory" if "accessor" in ptype else detect_category(name, price)
        if re.search(r"hektor-?p|elmaron|colorplan|projector|spool|\bcap\b", name, re.I):
            cat = "Accessory"  # 영사기 렌즈(Hektor-P2·Elmaron)·필름 스풀·캡이 'Used lenses'에 섞여 있음
        mount = 'Accessory' if cat == 'Accessory' else detect_mount(name)
        img = p["images"][0].get("src", "") if p.get("images") else ""
        results.append({
            "게시일": _shopify_listed(p),
            "site": "One Of Many Cameras (덴마크)",
            "label": auto_label(name),
            "상품명": name,
            "세대": detect_generation(name),
            "컨디션": describe_text(p.get("body_html") or "") or "정보없음",
            "가격": price,
            "통화": "DKK",
            "이미지": img,
            "링크": f"{base}/products/{p['handle']}",
            "품절": False,
            "예약중": False,
            "mount": mount,
            "category": cat,
            "brand": detect_brand(name),
        })
    print(f"  ✅ One Of Many Cameras 완료: {len(results)}개")
    return results


def _cavour_name(title):
    """Foto Ottica Cavour 제목 다듬기: 'Leica SUMMICRON-M 35mm f/2 ASPH. [I], black anodized' → 'Leica SUMMICRON-M 35mm f2 ASPH. v1 black anodized',
    'Leica Mirino 28mm' → 'Leica Viewfinder 28mm'. 대괄호 세대 [I]~[V]는 v1~v5로, 이탈리아어 부속 이름은 영어로"""
    import html as _html
    name = re.sub(r"\s+", " ", _html.unescape(title)).strip()
    roman = {"I": "1", "II": "2", "III": "3", "IV": "4", "V": "5", "VI": "6"}
    name = re.sub(r"\[(VI|IV|V|I{1,3})\]", lambda m: "v" + roman[m.group(1)], name)
    name = re.sub(r"\bf/\s?(\d)", r"f\1", name)
    for it, en in (("Mirino elettronico", "Electronic Viewfinder"), ("Mirino", "Viewfinder"), ("Custodia in pelle", "Leather Case"),
                   ("Custodia", "Case"), ("Borsa", "Bag"), ("Cinghia", "Strap"), ("Paraluce", "Lens Hood"), ("Filtro", "Filter"),
                   ("Impugnatura", "Handgrip"), ("Batteria", "Battery"), ("Caricabatterie", "Charger"), ("Tappo", "Cap"),
                   ("Anello adattatore", "Adapter"), ("Adattatore", "Adapter"), ("nero", "black"), ("cromato", "chrome"),
                   ("argento", "silver"), ("per", "for")):
        name = re.sub(rf"(?<![\w-]){it}(?![\w-])", en, name, flags=re.I)
    name = re.sub(r"\s*,\s*", " ", name)
    name = re.sub(r"\s+", " ", name).strip(" ,-")
    if not re.match(r"(?:leica|leitz)\b", name, re.I):
        name = "Leica " + name
    return name


def crawl_cavour():
    """Foto Ottica Cavour (이탈리아) - 밀라노 라이카 중고점 Shopify products.json 전체(1,200개쯤, 5쪽)에서 브랜드 칸이 Leica Camera AG·
    Ernst Leitz Wetzlar·Leica Group이고 'Usato'(중고) 태그가 있는 것만 ('Nuovo' 새 상품은 뺌). 가격은 EUR.
    등급 표기가 없어 설명 글 말투로 ('In ottime condizioni' → IT: …, 없으면 정보없음)"""
    import requests
    from condition_grade import it_condition
    results = []
    sess = requests.Session()
    sess.headers["User-Agent"] = random.choice(USER_AGENTS)
    base = "https://www.fotootticacavour.com"
    print(f"\n  📂 Foto Ottica Cavour 크롤링 시작")
    for p in _shopify_all(sess, f"{base}/products.json", "Foto Ottica Cavour"):
        if not re.match(r"(?:leica|ernst leitz)", (p.get("vendor") or "").strip(), re.I) or "Usato" not in (p.get("tags") or []):
            continue
        variants = p.get("variants") or [{}]
        if not any(v.get("available") for v in variants):
            continue
        title = re.sub(r"\s+", " ", (p.get("title") or "")).strip()
        if any(b2 in title.lower() for b2 in THIRD_PARTY_BRANDS):
            continue
        name = _cavour_name(title)
        try:
            price = f"€{float(variants[0].get('price')):,.0f}"
        except (TypeError, ValueError):
            price = "문의요망"
        ptype = (p.get("product_type") or "").strip().lower()
        cat = "Lens" if ptype == "obiettivi" else "Body" if ptype.startswith("fotocamere") else "Accessory" if ptype else detect_category(name, price)
        mount = 'Accessory' if cat == 'Accessory' else detect_mount(name)
        img = p["images"][0].get("src", "") if p.get("images") else ""
        results.append({
            "게시일": _shopify_listed(p),
            "site": "Foto Ottica Cavour (이탈리아)",
            "label": auto_label(name),
            "상품명": name,
            "세대": detect_generation(name),
            "컨디션": it_condition(p.get("body_html") or "") or "정보없음",
            "가격": price,
            "통화": "EUR",
            "이미지": img,
            "링크": f"{base}/products/{p['handle']}",
            "품절": False,
            "예약중": False,
            "mount": mount,
            "category": cat,
            "brand": detect_brand(name),
        })
    print(f"  ✅ Foto Ottica Cavour 완료: {len(results)}개")
    return results


def _suffren_name(title):
    """Photo Suffren 제목 다듬기: 'Leica Summicron-M 2/35 Asph. v.I révisée' → 'Leica Summicron-M 35mm f2 Asph. v1',
    'Leica Elmarit-R 2,8/19 v.II à ROM + parasoleil' → 'Leica Elmarit-R 19mm f2.8 v2 ROM with hood'. 조리개/초점거리 순서를 바꾸고
    프랑스어 색·부속 이름은 영어로, 'révisé'·'en boîte'·'(26700 clics)' 같은 꼬리는 뗀다"""
    import html as _html
    name = re.sub(r"\s+", " ", _html.unescape(title)).strip()
    name = re.sub(r"^(Leitz|Leica)-", r"\1 ", name)
    name = re.sub(r"-(R|M)-(?=\d)", r"-\1 ", name)
    name = re.sub(r"\((?:\d[\d\s.]*)\s*clics?\)|\b(?:entièrement\s+)?révisée?s?\b|\b(?:neuf\s+)?en\s+bo[iî]te(?:\s+complète)?\b|"
                  r"\bgarantie?\b.*$", "", name, flags=re.I)
    name = re.sub(r"\b(\d(?:,\d{1,2})?)\s?/\s?(\d{2,3}(?:-\d{2,3})?)(?:\s?mm)?\b",
                  lambda m: f"{m.group(2)}mm f{m.group(1).replace(',', '.')}", name)
    roman = {"I": "1", "II": "2", "III": "3", "IV": "4", "V": "5"}
    name = re.sub(r"\bv\.?\s?(IV|V|I{1,3})\b", lambda m: "v" + roman[m.group(1)], name)
    for fr, en in (("laqué noir", "black paint"), ("laquée noire", "black paint"), ("chromée?", "chrome"), ("noire?", "black"),
                   ("argent(?:ée?)?", "silver"), ("gris métal", "grey"), ("à ROM", "ROM"), ("3 cames", "3-cam"), ("2 cames", "2-cam"),
                   ("R ONLY|ONLY R", "R-only"), (r"\+\s*parasoleil", "with hood"), ("parasoleil", "hood"),
                   (r"\+\s*étui(?: cuir)?", "with case"), ("étui(?: cuir)?", "case"), ("lunettes", "eyes"), ("viseur", "Viewfinder"),
                   ("boîtier", "Body"), ("bouchon", "cap"), ("filtre", "Filter"), ("codée?", "coded"), ("modifiée?", "modified"),
                   ("avec", "with"), ("pour", "for"), ("plastique", "plastic")):
        name = re.sub(rf"(?<![\w-]){fr}(?![\w-])", en, name, flags=re.I)
    name = re.sub(r"\s*\+\s*$|\s*\(\s*\)", "", name)
    name = re.sub(r"\s+", " ", name).strip(" ,-+")
    if not re.match(r"(?:leica|leitz)\b", name, re.I):
        name = "Leica " + name
    return name


def crawl_suffren():
    """Photo Suffren (프랑스) - 파리 라이카 중고 전문점 Shopify products.json 전체(300개쯤, 2쪽)에서 브랜드 칸이 Leica이고
    설명에 'Etat 8/10' 등급이 있는 중고만 (등급 없는 것은 새 상품·데모라 뺌). 가격은 EUR"""
    import html as _html
    import requests
    from condition_grade import SUFFREN_PREFIX
    results = []
    sess = requests.Session()
    sess.headers["User-Agent"] = random.choice(USER_AGENTS)
    base = "https://www.photosuffren.com"
    print(f"\n  📂 Photo Suffren 크롤링 시작")
    for p in _shopify_all(sess, f"{base}/products.json", "Photo Suffren"):
        if (p.get("vendor") or "").strip().lower() != "leica":
            continue
        variants = p.get("variants") or [{}]
        if not any(v.get("available") for v in variants):
            continue
        text = re.sub(r"\s+", " ", _html.unescape(re.sub(r"<[^>]+>", " ", p.get("body_html") or "")))
        m = re.search(r"[EÉ]tat\s*:?\s*(\d{1,2}(?:[.,]5)?)\s*/\s*10", text, re.I)
        if not m:
            continue
        title = re.sub(r"\s+", " ", (p.get("title") or "")).strip()
        if any(b2 in title.lower() for b2 in THIRD_PARTY_BRANDS):
            continue
        name = _suffren_name(title)
        try:
            price = f"€{float(variants[0].get('price')):,.0f}"
        except (TypeError, ValueError):
            price = "문의요망"
        img = p["images"][0].get("src", "") if p.get("images") else ""
        # 매장 분류(Optique·Boitier·Accessoire)를 먼저 믿는다 ('Macro-Elmar-M … + lunettes'가 바디로, 'Motor M'이 렌즈로 가던 것)
        cat = {"optique": "Lens", "boitier": "Body", "boîtier": "Body"}.get((p.get("product_type") or "").strip().lower()) \
            or ("Accessory" if (p.get("product_type") or "").strip() else detect_category(name, price))
        if re.search(r"viewfinder|filter\b|\bhood\b(?!.*\d+mm)", name, re.I) and not re.search(r"\d{2,3}mm f\d", name):
            cat = "Accessory"  # 'Viseur Leica 24 mm'은 매장이 Optique로 둠
        mount = 'Accessory' if cat == 'Accessory' else detect_mount(name)
        results.append({
            "게시일": _shopify_listed(p),
            "site": "Photo Suffren (프랑스)",
            "label": auto_label(name),
            "상품명": name,
            "세대": detect_generation(name),
            "컨디션": SUFFREN_PREFIX + m.group(1).replace(",", "."),
            "가격": price,
            "통화": "EUR",
            "이미지": img,
            "링크": f"{base}/products/{p['handle']}",
            "품절": False,
            "예약중": False,
            "mount": mount,
            "category": cat,
            "brand": detect_brand(name),
        })
    print(f"  ✅ Photo Suffren 완료: {len(results)}개")
    return results


def crawl_cameraelectronic():
    """Camera Electronic (호주, 퍼스) - Shopify JSON. 라이카·핫셀 중고 컬렉션(second-hand-leica-and-hasselblad, 120개쯤 한 쪽)에서
    브랜드 칸이 Leica인 것만
    (Panasonic Leica DG·Voigtlander 등은 브랜드가 달라 빠짐). 등급 표기가 없어 제목·설명 글의 말투('Mint'·'excellent condition'·
    'minimal signs of wear')로 (ce_condition). 전체 중고(second-hand)는 쪽이 많아 429(Retry-After 60)가 나서 이 컬렉션만"""
    import requests
    from condition_grade import ce_condition
    results, seen = [], set()
    base = "https://www.cameraelectronic.com.au"
    print(f"\n  📂 Camera Electronic 크롤링 시작")
    s = requests.Session()
    s.headers["User-Agent"] = random.choice(USER_AGENTS)
    s.headers["Accept"] = "application/json"
    for page_num in range(1, 30):
        products = None
        for attempt in range(4):
            try:
                resp = s.get(f"{base}/collections/second-hand-leica-and-hasselblad/products.json",
                             params={"limit": 250, "page": page_num}, timeout=30)
                if resp.status_code == 429:
                    time.sleep(int(resp.headers.get("Retry-After") or 0) or 20 * (attempt + 1))
                    continue
                resp.raise_for_status()
                products = resp.json().get("products", [])
                break
            except Exception as e:
                print(f"    ⚠️ {page_num}페이지 오류: {e}")
                time.sleep(5)
        if products is None:
            raise RuntimeError(f"Camera Electronic {page_num}페이지 못 읽음")  # 빠진 쪽이 판매완료로 바뀌지 않게
        if not products:
            break
        print(f"    └─ {page_num}페이지 {len(products)}개 상품 발견")
        for p in products:
            if (p.get("vendor") or "").strip().lower() != "leica":
                continue
            name = _cameraelectronic_name(p.get("title") or "")
            if not re.match(r"leica|leitz", name, re.I) or any(b2 in name.lower() for b2 in THIRD_PARTY_BRANDS):
                continue
            link = f"{base}/products/{p['handle']}" if p.get("handle") else ""
            if not link or link in seen or link in globals().get('SOLD_LINKS', ()):
                continue
            seen.add(link)
            variant = p["variants"][0] if p.get("variants") else {}
            try:
                price = f"A${float(variant.get('price')):,.0f}"
            except (TypeError, ValueError):
                price = "문의요망"
            img = p["images"][0].get("src", "") if p.get("images") else ""
            cat = detect_category(name, price)
            mount = 'Accessory' if cat == 'Accessory' else detect_mount(name)
            results.append({
                "게시일": _shopify_listed(p),
                "site": "Camera Electronic (호주)",
                "label": auto_label(name),
                "상품명": name,
                "세대": detect_generation(name),
                "컨디션": ce_condition((p.get("title") or "") + " " + (p.get("body_html") or "")) or "정보없음",
                "가격": price,
                "통화": "AUD",
                "이미지": img,
                "링크": link,
                "품절": not any(v.get("available") for v in p.get("variants") or [{}]),
                "예약중": False,
                "mount": mount,
                "category": cat,
                "brand": detect_brand(name),
            })
        if len(products) < 250:  # 마지막 쪽 — 빈 다음 쪽을 또 부르면 429가 나기 쉬움
            break
        time.sleep(4)
    print(f"  ✅ Camera Electronic 완료: {len(results)}개")
    return results


# Leica Classic (classic.leica-camera.com): 라이카 매장 수십 곳의 중고·빈티지가 한 몰에. 매장 나라마다 다른 사이트로 나눈다.
# 프랑스 매장(파리·마르세유·릴)은 Leica Store France, 싱가포르는 Leica Store Singapore와 같은 재고라 뺀다.
LEICA_CLASSIC_COUNTRIES = [  # (매장 이름에 든 말, 나라 코드, 사이트 이름)
    ("Vienna", "AT", "Leica Classic (오스트리아)"),
    ("London", "GB", "Leica Classic (영국)"),
    ("Munich|Stuttgart|Berlin|Nürnberg|Nuernberg|Wetzlar|Hamburg|Frankfurt|Düsseldorf|Dusseldorf", "DE", "Leica Classic (독일)"),
    ("Geneva|Basel|Zurich|Zürich", "CH", "Leica Classic (스위스)"),
    ("Madrid", "ES", "Leica Classic (스페인)"),
    ("Porto|Lisbo", "PT", "Leica Classic (포르투갈)"),
    ("Bologna|Milano|Firenze|Torino|Roma", "IT", "Leica Classic (이탈리아)"),
    ("Copenhagen", "DK", "Leica Classic (덴마크)"),
    (r"Los Angeles|Boston|Washington|U\.S\.|Bellevue|New York|Miami|San Francisco|Chicago", "US", "Leica Classic (미국)"),
    ("Dubai", "AE", "Leica Classic (아랍에미리트)"),
    ("Kuala Lumpur", "MY", "Leica Classic (말레이시아)"),
]
LEICA_CLASSIC_SKIP_STORES = re.compile(r"Paris|Marseille|Lille|Lyon|Singapore")
# 분류 경로에 이 말이 있으면 카메라 장비가 아니라 뺀다 (시계·현미경·사진 작품·책·쌍안경·영사기·확대기·시네 카메라)
LEICA_CLASSIC_SKIP_PATH = re.compile(r"Watches|ZM1|ZM2|Microscop|Photograph|Literature|Sport Optics|Binocular|Monocular|"
                                     r"Projector|Enlarger|Leicina|Other Brands|Gallery|Picture of the Year|Photo Books")
LEICA_CLASSIC_SLUG = re.compile(r"leica|leitz|summi|elmar|noctilux|hektor|telyt|angulon|summar|thambar|visoflex|leicina|ultravid|"
                                r"trinovid|noctivid|leicaflex|hologon|xenon|geovid|d-lux|c-lux|v-lux|sofort", re.I)
LEICA_CLASSIC_PRICE = {"EUR": "€{:,.0f}", "GBP": "£{:,.0f}", "USD": "${:,.0f}", "CHF": "CHF {:,.0f}", "DKK": "DKK {:,.0f}",
                       "MYR": "MYR {:,.0f}", "SGD": "S${:,.0f}"}
_LEICA_CLASSIC_CACHE = {}
_LEICA_CLASSIC_LOCK = threading.Lock()


def _leica_classic_name(name):
    """Leica Classic 제목 다듬기: 독일식 '조리개/초점거리' 순서('Summicron-M 2.0/50mm'·'Elmar 3,5/5cm'·'1:1.4/35')를
    '50mm f2.0'·'5cm f3.5'·'35mm f1.4'로, 긴 줄표 '–'는 '-'로 (그대로면 'R 3.5'가 R3 바디로 읽히는 등 연결이 안 됨)"""
    name = re.sub(r"\s+", " ", name.replace("–", "-").replace("—", "-")).strip()
    name = re.sub(r"\bf[:/](\d)", r"f\1", name).replace("Elamarit", "Elmarit")
    name = re.sub(r"\b(APO)[ -](Summicron|Summilux|Elmarit|Telyt)[ -](SL|M|R|TL)\b", r"\1-\2-\3", name, flags=re.I)
    name = re.sub(r"(?<![-\w])(Summicron|Summilux|Elmarit|Noctilux)[ ](SL|TL)\b", r"\1-\2", name, flags=re.I)

    def flip(m):
        ap, focal, unit = m.group(1).replace(",", "."), m.group(2).replace(",", "."), (m.group(3) or "mm").lower()
        if "-" not in ap and "-" not in focal and float(ap) > 12 >= float(focal):  # '35/2'처럼 초점거리가 앞이면 그대로 뒤집기
            ap, focal = focal, ap
        if "." not in ap.split("-")[0]:
            ap = ap.split("-")[0] + ".0" + ("-" + ap.split("-")[1] if "-" in ap else "")  # 정수 조리개는 'f2.0' (_has_aperture가 소수점만 읽음)
        return f"{focal}{unit} f{ap}"
    name = re.sub(r"(?<![\w.,/])(?:1\s?:\s?)?(\d{1,2}(?:[.,]\d{1,2})?(?:-\d{1,2}(?:[.,]\d{1,2})?)?)\s*/\s*"
                  r"(\d{1,3}(?:[.,]\d)?(?:-\d{2,3})?)\s*(mm|cm)?(?![\w/\"])",
                  flip, name, flags=re.I)
    if not re.match(r"leica|leitz", name, re.I):
        name = "Leica " + name
    return name


def _leica_classic_all():
    """사이트맵(robots.txt 허용) → 상품 주소, 슬러그로 라이카만 → 처음 보는 상품만 상세 화면을 읽고(메타 태그의 매장·가격·통화·사진,
    'Condition' 칸 등급) 전에 읽은 것은 이전 결과를 다시 쓴다. 목록 쪽 넘김(?p=)은 robots.txt가 막아(Disallow: */?) 안 씀.
    사이트맵에서 빠진 상품 = 판매 완료. 상세는 한 번에 최대 1,500개(첫 실행 약 3분) + 이전 것 80개 다시 확인 (가격·매진 변화).
    나라별 사이트 여럿이 같이 부르므로 한 실행에 한 번만 읽고 나라 코드 → 행 목록으로 돌려준다"""
    with _LEICA_CLASSIC_LOCK:
        if "rows" in _LEICA_CLASSIC_CACHE:
            return _LEICA_CLASSIC_CACHE["rows"]
        import gzip
        import html as _html
        import requests
        from concurrent.futures import ThreadPoolExecutor
        from condition_grade import LEICA_CLASSIC_PREFIX
        base = "https://classic.leica-camera.com"
        sess = requests.Session()
        sess.headers["User-Agent"] = random.choice(USER_AGENTS)
        print("\n  📂 Leica Classic 크롤링 시작")
        index = sess.get(f"{base}/en/sitemap.xml", timeout=30)
        index.raise_for_status()
        links = []
        for gz in re.findall(r"<loc>([^<]+\.xml\.gz)</loc>", index.text):
            resp = sess.get(gz, timeout=60)
            resp.raise_for_status()
            links += re.findall(r"<loc>(https://classic\.leica-camera\.com/en/[^/<]+/[^/<]+)</loc>", gzip.decompress(resp.content).decode("utf-8"))
        links = [u for u in dict.fromkeys(links) if LEICA_CLASSIC_SLUG.search(u.split("/en/")[1].split("/")[0])]
        if len(links) < 300:
            raise RuntimeError(f"Leica Classic 사이트맵 상품 {len(links)}개뿐")  # 사이트맵이 덜 나오면 판매완료로 바뀌지 않게
        known, skip = {}, {}
        try:
            with open("data/raw/results.json", encoding="utf-8") as f:
                known = {r["링크"]: r for r in json.load(f) if str(r.get("site", "")).startswith("Leica Classic (")}
        except (OSError, ValueError):
            pass
        try:
            with open("data/raw/leica_classic_skip.json", encoding="utf-8") as f:
                skip = json.load(f)
        except (OSError, ValueError):
            pass
        todo = [u for u in links if u not in known and u not in skip][:1500]
        seen_before = [u for u in links if u in known]
        recheck = random.sample(seen_before, min(80, len(seen_before)))
        print(f"    └─ 사이트맵 라이카 {len(links)}개 · 이전 {len(known)}개 · 새로 읽기 {len(todo)}개 · 다시 확인 {len(recheck)}개")

        def meta(h, prop):
            m = re.search(r'<meta\s+property="' + prop + r'"\s+content="([^"]*)"', h)
            return _html.unescape(m.group(1)).strip() if m else ""

        def detail(link):
            try:
                h = sess.get(link, timeout=40).text
            except Exception as e:
                print(f"    ⚠️ 상세 오류 {link[-40:]}: {e}")
                return link, None
            m_name = re.search(r'<h1[^>]*product-detail-name[^>]*>(.*?)</h1>', h, re.S)
            path = " > ".join(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", li)).strip()
                              for li in re.findall(r'<li[^>]*breadcrumb-item[^>]*>(.*?)</li>', h, re.S))
            m_cond = re.search(r"<strong>Condition\s*</strong>.*?</a>\s*</div>\s*<div[^>]*>\s*([^<]+?)\s*<", h, re.S)
            try:
                amount = float(meta(h, "product:price:amount") or 0)
            except ValueError:
                amount = 0
            return link, {"name": _html.unescape(re.sub(r"<[^>]+>", "", m_name.group(1))).strip() if m_name else "",
                          "store": meta(h, "product:brand"), "amount": amount, "currency": meta(h, "product:price:currency"),
                          "image": meta(h, "og:image"), "cond": m_cond.group(1).strip() if m_cond else "",
                          "cart": "Add to shopping cart" in h, "path": _html.unescape(path)}

        with ThreadPoolExecutor(6) as ex:
            fetched = dict(ex.map(detail, todo + recheck))
        rows_by_cc = {cc: [] for _, cc, _ in LEICA_CLASSIC_COUNTRIES}
        for link in links:
            info = fetched.get(link)
            if info is None:
                prev = known.get(link)
                if prev:  # 이전에 읽은 것 그대로 (가격 바뀜은 다시 확인 차례에)
                    cc = next((c for _, c, site in LEICA_CLASSIC_COUNTRIES if site == prev["site"]), None)
                    if cc:
                        row = dict(prev)
                        row["상품명"] = _leica_classic_name(row["상품명"])
                        rows_by_cc[cc].append(row)
                continue
            store = info["store"]
            cc_site = next(((cc, site) for pat, cc, site in LEICA_CLASSIC_COUNTRIES if re.search(pat, store)), None)
            if (not info["name"] or LEICA_CLASSIC_SKIP_STORES.search(store) or not cc_site
                    or LEICA_CLASSIC_SKIP_PATH.search(info["path"])):
                skip[link] = store or "?"
                continue
            if not info["cart"]:  # 장바구니 버튼이 없으면 판매 끝 (사이트맵엔 아직 남은 것)
                continue
            name = _leica_classic_name(info["name"])
            # 'Leica Systems > M-System > Cameras'인데 이름에 Body가 없으면 붙인다 ('Leica SL (Typ 601)'·'Leica M EV1'이 렌즈로 갈리지 않게)
            if re.search(r"> Cameras\b", info["path"]) and not re.search(r"\bbody\b|\bkit\b|\d\s?mm\b|\d\s?cm\b|dummy|not working", name, re.I):
                name += " Body"
            # 액세서리 분류인데 렌즈 표기('50mm f/2')가 없으면 'Accessory'를 붙인다 ('FLOTH plumb line'·'SCNOO'가 렌즈로 갈리지 않게)
            elif re.search(r"Accessor|Copy Equipment|Focussing Stages|Close Up|Lens Hoods|Finder|Light-Meter|Filter|Caps|Bags",
                           info["path"]) and not re.search(r"\d\s?(?:mm|cm) f\d|\baccessory\b", name, re.I):
                name += " Accessory"
            fmt = LEICA_CLASSIC_PRICE.get(info["currency"])
            price = fmt.format(info["amount"]) if fmt and info["amount"] else "문의요망"
            cat = detect_category(name, price)
            mount = 'Accessory' if cat == 'Accessory' else detect_mount(name)
            rows_by_cc[cc_site[0]].append({
                "site": cc_site[1],
                "label": auto_label(name),
                "상품명": name,
                "세대": detect_generation(name),
                "컨디션": LEICA_CLASSIC_PREFIX + info["cond"] if info["cond"] else "정보없음",
                "가격": price,
                "통화": info["currency"] or "EUR",
                "이미지": info["image"],
                "링크": link,
                "품절": False,
                "예약중": False,
                "mount": mount,
                "category": cat,
                "brand": detect_brand(name),
            })
        try:
            live = set(links)
            with open("data/raw/leica_classic_skip.json", "w", encoding="utf-8") as f:
                json.dump({u: v for u, v in skip.items() if u in live}, f, ensure_ascii=False, indent=0)
        except OSError:
            pass
        print("  ✅ Leica Classic 완료: " + " · ".join(f"{cc} {len(v)}" for cc, v in rows_by_cc.items()))
        _LEICA_CLASSIC_CACHE["rows"] = rows_by_cc
        return rows_by_cc


def crawl_leica_classic(cc):
    return _leica_classic_all().get(cc, [])


def crawl_kitamura():
    """기타무라 크롤러 - 라이카 중고 전체

    2026-09 사이트 개편으로 중고 재고가 shop.kitamura.jp 로 옮겨감.
    목록 페이지가 부르는 used_sell_search JSON을 그대로 받아 100개씩 끝까지 넘긴다.
    """
    import re as _re
    results = []
    base = "https://shop.kitamura.jp"
    base_url = f"{base}/ec/list?type=u&narrow1=%E3%83%A9%E3%82%A4%E3%82%AB(LEICA)"
    page_size = 100
    # used_sell_search rank → 상태 등급 (사이트 집계값으로 확인)
    RANK_TO_COND = {5: 'AA', 4: 'A', 3: 'AB', 2: 'B', 1: 'C'}

    from ja_normalize import ja_to_en  # 일본 사이트 공용 (app/ja_normalize.py)

    print(f"\n  📂 기타무라 크롤링 시작")

    # 목록 페이지가 부르는 검색 API를 바로 부름 (브라우저 불필요).
    # 기타무라는 미국 서버 접속을 막아서 GitHub에선 Vercel 도쿄 중계 서버(relay/)를 거침.
    # x-kitamura-api-key는 사이트 화면 코드에 들어 있는 공개 값 — 바뀌면 브라우저 개발자도구에서 새 값 확인.
    import crawl_engine as _ce
    search_url = (f"{base}/ec/api/cache/s/v1/used_sell_search?maker=%E3%83%A9%E3%82%A4%E3%82%AB&sort=default"
                  f"&size={page_size}&offset=1&ref_id=used_sell_search&func=srch"
                  "&extra_fields=sales_status,is_maintenance,sale_start_at,sale_end_at&site=ns&is_logged_in=0&aggs=default")
    headers = {"x-kitamura-api-key": "AA4n2cEkYz", "x-kitamura-app-id": "1",
               "accept": "application/json, text/plain, */*", "referer": base_url}

    offset = 1  # 1부터 시작하는 상품 순번
    total = None
    while True:
        url = _re.sub(r'offset=\d+', f'offset={offset}', search_url)
        print(f"    └─ {offset}번째부터 수집 중...")
        try:
            resp = _ce.http_get(url, headers, via_relay=True)
            resp.raise_for_status()
            data = resp.json()["search"]
        except Exception as e:
            print(f"    ❌ 목록 오류: {e}")
            if offset == 1:
                raise  # 첫 페이지부터 못 받으면 실패로 (병합 단계에서 이전 데이터 유지)
            break

        hits = data.get("hits") or []
        if total is None:
            total = data.get("total_hits", 0)
            print(f"    └─ 전체 {total}개")
        if not hits:
            break

        for item in hits:
            try:
                if item.get("sales_status") not in (None, 1):
                    continue  # 판매중이 아님
                name_ja = (item.get("title") or "").strip()
                if not name_ja:
                    continue

                # 일본어 → 영어 변환
                name_en = ja_to_en(name_ja)

                href = f"{base}/ec/used/{item['id']}"
                if href in globals().get('SOLD_LINKS', ()):
                    continue

                price_num = item.get("price")
                price = f"¥{int(price_num):,}" if price_num else "문의요망"

                img = item.get("image_link") or ""
                cond = RANK_TO_COND.get(item.get("rank"), "정보없음")

                label = auto_label(name_en)
                mount = detect_mount(name_en)
                gen = detect_generation(name_en)
                brand = detect_brand(name_en)
                cat = detect_category(name_en, price)

                if cat == 'Accessory':
                    mount = 'Accessory'

                results.append({
                    "site": "기타무라 (일본)",
                    "label": label,
                    "상품명": name_en,
                    "세대": gen,
                    "컨디션": cond,
                    "가격": price,
                    "통화": "JPY",
                    "이미지": img,
                    "링크": href,
                    "품절": False,
                    "예약중": False,
                    "mount": mount,
                    "category": cat,
                    "brand": brand,
                })

            except Exception as e:
                print(f"    ⚠️  파싱 오류: {e}")
                continue

        offset += len(hits)
        if offset > total:
            break
        time.sleep(random.uniform(0.3, 0.8))

    print(f"  ✅ 기타무라 완료: {len(results)}개")
    return results


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
            page.goto(cat_url, wait_until="networkidle", timeout=20_000)
            page.wait_for_selector('#sscProductArray article', timeout=10_000)
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
                    page.goto(next_url, wait_until="networkidle", timeout=15_000)
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
                    const grade = (a.querySelector('.sortkey2')?.getAttribute('rel') || '').trim();  // Mint-, E++, E+ …
                    const isSold = a.querySelector('.soldout, .out-of-stock') !== null ||
                                   a.innerText.toLowerCase().includes('sold out');
                    results.push({name, href, img, price, isUsed, isSold, grade});
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
                cond = item.get('grade') or ("Used" if is_used else "New")  # Ffordes 등급 (E++ 등)
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


# 목록엔 컨디션이 없고 상세 페이지에만 있는 사이트 → 상세 페이지에서 찾을 글귀 (숫자 하나 = %)
DETAIL_CONDITION = {
    "장씨카메라": r"상태\s*:?\s*(\d{2,3})\s*%",
}

# 사이트별 최소 수집 간격(시간). 없는 사이트는 매 실행마다. Ffordes는 서버가 느리고 매물이 130개 안팎이라 6시간.
SOURCE_MIN_INTERVAL_HOURS = {
    "gebrauchtkameras.de (독일)": 12,  # 라이카 상품 상세 100개쯤 (3분)
    "Midwest Photo (미국)": 12,  # 사이트맵 1만 개 받아 거름
    "Ffordes (영국)": 6,
    "Lucky Camera (일본)": 12,  # 목록 30쪽 + 새 매물 상세
    "Tamarkin Camera (미국)": 6,  # 카드마다 상세 (약 170개)
    "Leica Store Poland (폴란드)": 6,  # 매물마다 상세, Crawl-delay 2초 (약 40개 · 2분)
    "Photo Warehouse (뉴질랜드)": 6,  # 매물마다 상세 (약 70개 · 1분)
    "富士越カメラ (일본)": 6,  # 목록 6쪽 + 새 매물 상세
    "カメラの大林 (일본)": 6,  # 분류 5곳 + 새 매물 상세
    "Howard Parker (영국)": 6,  # 매물마다 상세 (약 50개)
    "Foto Köster (독일)": 6,  # 매물마다 상세 (약 40개)
    "Lecuit (룩셈부르크)": 6,  # 목록 2쪽 + 새 매물 상세 (약 110개)
    "Calumet (독일)": 6,  # 상품 화면 120개쯤 (4~5분)
    "Fotohandel Delfshaven (네덜란드)": 6,  # 목록 22쪽 (1분쯤)
    "One Of Many Cameras (덴마크)": 6,  # 전체 16쪽 (중고 라이카는 200개쯤)
    "Leica Store Amsterdam (네덜란드)": 6,  # 매물마다 상세 (약 55개, 2초 간격이라 2분쯤)
    "PhotoCo (호주)": 24,  # robots.txt Crawl-delay 600초, 목록 2쪽 (약 10분)
    "J-カメラ (일본)": 6,  # Crawl-delay 10초, 7쪽 안팎
    "Leica Store Australia (호주)": 24,  # 브라우저, Crawl-delay 30초 (1분 30초쯤)
    **{site: 6 for _, _, site in LEICA_CLASSIC_COUNTRIES},  # 사이트맵 + 새 매물 상세 (나라별 사이트가 한 번에 같이)
}


def _with_browser(fn, headers=None):
    """Playwright 페이지 하나로 기존 수집 함수 실행"""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        try:
            page = browser.new_page()
            if headers:
                page.set_extra_http_headers(headers)
            return fn(page)
        finally:
            browser.close()



def _fotogoerlitz_name(title):
    """Foto Görlitz 제목 다듬기: 'Demo'·'DEMO' 떼고 독일어 색(schwarz·silber·glänzend) → 영어, '50mm 1.2' → '50mm f1.2'"""
    name = re.sub(r"\s*\b(?:demo|demoartikel)\b", "", title, flags=re.I)
    name = re.sub(r"\bschwarz\b", "black", name, flags=re.I)
    name = re.sub(r"\bsilber\b", "silver", name, flags=re.I)
    name = re.sub(r"\bglänzend\b", "glossy", name, flags=re.I)
    name = re.sub(r"\b(\d{2,3})mm\s+(\d\.\d)\b", r"\1mm f\2", name)
    return re.sub(r"\s+", " ", name).strip(" -")


def crawl_fotogoerlitz():
    """Foto Görlitz (독일 뷘데) - 라이카 매장 WooCommerce 상품 API(Store API)의 'Demoartikel' 분류(id 479, 18점 안팎)만, 판매 중만. 가격 EUR.
    신품 분류는 빼고 데모품만 (2026-11-05 사장님). 데모품이라 등급은 전부 S (condition_grade FOTOGOERLITZ_PREFIX)"""
    import html as _html
    import requests
    import crawl_engine as _ce
    from condition_grade import FOTOGOERLITZ_PREFIX
    results = []
    sess = requests.Session()
    sess.headers["User-Agent"] = _ce.BROWSER_UA
    base = "https://fotogoerlitz.de"
    print(f"\n  📂 Foto Görlitz 크롤링 시작")
    for page_num in range(1, 10):
        resp = sess.get(f"{base}/wp-json/wc/store/v1/products",
                        params={"category": 479, "per_page": 100, "page": page_num}, timeout=30)
        resp.raise_for_status()
        items = resp.json()
        if not items:
            break
        print(f"    └─ Foto Görlitz {page_num}페이지 {len(items)}개")
        for p in items:
            if not p.get("is_in_stock", True):
                continue
            title = re.sub(r"\s+", " ", _html.unescape(p.get("name") or "")).strip()
            if not re.search(r"\b(?:leica|leitz)\b", title, re.I):
                continue
            name = _fotogoerlitz_name(title)
            pr = p.get("prices") or {}
            try:
                price = f"€{int(pr.get('price')) / 10 ** int(pr.get('currency_minor_unit') or 2):,.0f}"
            except (TypeError, ValueError):
                price = "문의요망"
            cat = detect_category(name, price)
            mount = 'Accessory' if cat == 'Accessory' else detect_mount(name)
            imgs = p.get("images") or []
            results.append({
                "게시일": "",
                "site": "Foto Görlitz (독일)",
                "label": auto_label(name),
                "상품명": name,
                "세대": detect_generation(name),
                "컨디션": FOTOGOERLITZ_PREFIX + "Demo",
                "가격": price,
                "통화": "EUR",
                "이미지": imgs[0].get("src", "") if imgs else "",
                "링크": p.get("permalink") or "",
                "품절": False,
                "예약중": False,
                "mount": mount,
                "category": cat,
                "brand": detect_brand(name),
            })
        if len(items) < 100:
            break
        time.sleep(2)
    print(f"  ✅ Foto Görlitz 완료: {len(results)}개")
    return results


COE_SLUG = re.compile(r"leica|leitz|summi|elmar|noctilux|summaron|hektor|visoflex|telyt|angulon|elmarit", re.I)
COE_STATE = "data/raw/cameraobscura_state.json"


def crawl_cameraobscura():
    """Camera Obscura Elburg (네덜란드 엘뷔르흐) - 중고점 WooCommerce. 상품 API·쪽 넘김은 robots.txt가 막아(Disallow: /wp-json, /*page/)
    사이트맵(product-sitemap.xml, lastmod 있음)의 라이카 주소(340개쯤)만 상품 화면을 1~2초 간격으로 읽음.
    처음 한 번은 전부, 다음부터는 lastmod가 바뀐 상품 + 무작위 40개만 다시 읽고 나머지는 상태 파일(COE_STATE)의 이전 결과를 씀.
    사이트맵에서 빠진 상품 = 판매 완료. 판매 중('InStock')만 담음. 가격 EUR.
    등급 표기가 없고 설명이 자유 문장이라('clearly seen plenty of use … glass in excellent shape') describe_text가 엉뚱하게 잡혀 등급 없이 둠 (2026-11-05)"""
    import html as _html
    import requests
    import crawl_engine as _ce
    base = "https://www.cameraobscuraelburg.nl"
    sess = requests.Session()
    sess.headers["User-Agent"] = _ce.BROWSER_UA
    print(f"\n  📂 Camera Obscura Elburg 크롤링 시작")
    resp = sess.get(f"{base}/product-sitemap.xml", timeout=30)
    resp.raise_for_status()
    urls = re.findall(r"<url>\s*<loc>([^<]+)</loc>\s*(?:<lastmod>([^<]+)</lastmod>)?", resp.text)
    if len(urls) < 200:
        raise RuntimeError(f"Camera Obscura 사이트맵 상품 {len(urls)}개뿐")  # 덜 나오면 판매 완료로 바뀌지 않게
    links = {u: (m or "") for u, m in urls if COE_SLUG.search(u.rstrip("/").rsplit("/", 1)[-1])}
    try:
        with open(COE_STATE, encoding="utf-8") as f:
            state = json.load(f)
    except (OSError, ValueError):
        state = {}
    changed = [u for u, m in links.items() if u not in state or state[u].get("lastmod") != m]
    same = [u for u in links if u not in changed]
    todo = changed + random.sample(same, min(40, len(same)))
    print(f"    └─ 사이트맵 라이카 {len(links)}개 · 새로·바뀜 {len(changed)}개 · 다시 확인 {len(todo) - len(changed)}개")

    def detail(link):
        h = sess.get(link, timeout=40).text
        m_name = re.search(r"<h1[^>]*>(.*?)</h1>", h, re.S)
        m_av = re.search(r'"availability":"([^"]+)"', h)
        m_pr = re.search(r'"price":"?([\d.]+)', h)
        m_img = re.search(r'og:image" content="([^"]+)"', h)
        return {"name": _html.unescape(re.sub(r"<[^>]+>", "", m_name.group(1))).strip() if m_name else "",
                "in_stock": bool(m_av and "InStock" in m_av.group(1)),
                "amount": float(m_pr.group(1)) if m_pr else 0.0,
                "image": m_img.group(1) if m_img else ""}

    fails = 0
    for i, link in enumerate(todo):
        try:
            info = detail(link)
        except Exception as e:
            fails += 1
            print(f"    ⚠️ 상세 오류 {link[-50:]}: {e}")
            if fails > 20:
                raise RuntimeError("Camera Obscura 상세 오류가 너무 많음")
            continue
        info["lastmod"] = links[link]
        state[link] = info
        if (i + 1) % 50 == 0:
            print(f"    └─ 상세 {i + 1}/{len(todo)}")
        time.sleep(random.uniform(1, 2))
    state = {u: v for u, v in state.items() if u in links}
    with open(COE_STATE, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=0)
    results = []
    for link, info in state.items():
        name = re.sub(r"\s+", " ", info.get("name") or "").strip()
        if not info.get("in_stock") or not re.search(r"\b(?:leica|leitz)\b", name, re.I):
            continue
        price = f"€{info['amount']:,.0f}" if info.get("amount") else "문의요망"
        cat = detect_category(name, price)
        mount = 'Accessory' if cat == 'Accessory' else detect_mount(name)
        results.append({
            "게시일": "",
            "site": "Camera Obscura Elburg (네덜란드)",
            "label": auto_label(name),
            "상품명": name,
            "세대": detect_generation(name),
            "컨디션": "정보없음",
            "가격": price,
            "통화": "EUR",
            "이미지": info.get("image") or "",
            "링크": link,
            "품절": False,
            "예약중": False,
            "mount": mount,
            "category": cat,
            "brand": detect_brand(name),
        })
    print(f"  ✅ Camera Obscura Elburg 완료: {len(results)}개")
    return results


def crawl_chiswick():
    """Chiswick Camera Centre (영국 런던) - WooCommerce. 상품 API는 쪽 넘김을 무시해 같은 10개만 돌려줘서(2026-11-05)
    중고 분류 화면의 'Used brand: Leica' 필터(?filter_used-brand=leica, ?paged=N)를 읽음. 판매 중(instock)만. 가격 GBP.
    등급 표기 없음. 영국 안에만 배송"""
    import html as _html
    import requests
    import crawl_engine as _ce
    results, seen = [], set()
    sess = requests.Session()
    sess.headers["User-Agent"] = _ce.BROWSER_UA
    base = "https://chiswickcameras.co.uk"
    print(f"\n  📂 Chiswick Camera Centre 크롤링 시작")
    for page_num in range(1, 20):
        resp = sess.get(f"{base}/products/category/used/", params={"filter_used-brand": "leica", "paged": page_num}, timeout=30)
        if resp.status_code == 404 and page_num > 1:
            break
        resp.raise_for_status()
        items = re.findall(r'<li class="product [^"]*">(.*?)</li>', resp.text, re.S)
        classes = re.findall(r'<li class="(product [^"]*)">', resp.text)
        new = 0
        for cls, li in zip(classes, items):
            m_link = re.search(r'<a href="([^"]+)"', li)
            if not m_link or m_link.group(1) in seen:
                continue
            seen.add(m_link.group(1))
            new += 1
            if "instock" not in cls.split():
                continue
            m_name = re.search(r'woocommerce-loop-product__title">(.*?)</h2>', li, re.S)
            name = re.sub(r"\s+", " ", _html.unescape(re.sub(r"<[^>]+>", "", m_name.group(1)))).strip() if m_name else ""
            name = re.sub(r"\s*[–-]\s*", " ", name).strip()
            name = re.sub(r"\bGoogles\b", "Goggles", name)
            if not name:
                continue
            if not re.search(r"\b(?:leica|leitz)\b", name, re.I):
                name = "Leica " + name
            m_price = re.search(r'</span>([\d,]+\.\d\d)</bdi>', li)
            price = f"£{float(m_price.group(1).replace(',', '')):,.0f}" if m_price else "문의요망"
            m_img = re.search(r'<img[^>]+src="([^"]+)"', li)
            cat = detect_category(name, price)
            mount = 'Accessory' if cat == 'Accessory' else detect_mount(name)
            results.append({
                "게시일": "",
                "site": "Chiswick Camera Centre (영국)",
                "label": auto_label(name),
                "상품명": name,
                "세대": detect_generation(name),
                "컨디션": "정보없음",
                "가격": price,
                "통화": "GBP",
                "이미지": m_img.group(1) if m_img else "",
                "링크": m_link.group(1),
                "품절": False,
                "예약중": False,
                "mount": mount,
                "category": cat,
                "brand": detect_brand(name),
            })
        print(f"    └─ Chiswick {page_num}페이지 {len(items)}개")
        if not new or 'class="next page-numbers"' not in resp.text:
            break
        time.sleep(2)
    print(f"  ✅ Chiswick Camera Centre 완료: {len(results)}개")
    return results



def crawl_fotono():
    """Foto.no (노르웨이 대형 사진점) - 라이카 중고('Brukt'). 브랜드 화면은 100개까지만 보이고 쪽 넘김이 자바스크립트라
    사이트맵(sitemap-default.xml)에서 라이카 주소(/leica/…) 중 'tilstand'(중고 상태)가 든 것만 상품 화면을 2초 간격으로 읽음 (10개 안팎).
    상품 화면의 lipscore 속성(이름·사진·재고)과 가격 칸을 씀. 판매 중(ls-availability=1)만. 가격 NOK.
    등급은 제목의 'Tilstand: 2' (condition_grade FOTONO_PREFIX). '/search'는 robots.txt 금지라 안 씀"""
    import html as _html
    import requests
    import crawl_engine as _ce
    from condition_grade import FOTONO_PREFIX
    base = "https://www.foto.no"
    sess = requests.Session()
    sess.headers["User-Agent"] = _ce.BROWSER_UA
    print(f"\n  📂 Foto.no 크롤링 시작")
    resp = sess.get(f"{base}/sitemap-default.xml", timeout=60)
    resp.raise_for_status()
    urls = re.findall(r"<loc>([^<]+)</loc>", resp.text)
    if len(urls) < 5000:
        raise RuntimeError(f"Foto.no 사이트맵 {len(urls)}개뿐")  # 덜 나오면 판매 완료로 바뀌지 않게
    links = [u for u in dict.fromkeys(urls) if "/leica/" in u.lower() and "tilstand" in u.lower()]
    print(f"    └─ 사이트맵 라이카 중고 {len(links)}개")
    results = []
    for link in links:
        time.sleep(2)
        try:
            h = sess.get(link, timeout=30).text
        except Exception as e:
            print(f"    ⚠️ 상세 오류 {link[-50:]}: {e}")
            continue
        m_av = re.search(r'ls-availability="(\d)"', h)
        if not m_av or m_av.group(1) != "1":
            continue
        m_name = re.search(r"<h1[^>]*>(.*?)</h1>", h, re.S)
        m_title = re.search(r"<title>(.*?)</title>", h, re.S)
        title = _html.unescape(re.sub(r"\s+", " ", m_title.group(1))).split(" - Foto.no")[0].strip() if m_title else ""
        m_cond = re.search(r"Tilstand:\s*([1-5])", title)
        name = _html.unescape(re.sub(r"<[^>]+>", "", m_name.group(1))).strip() if m_name else re.sub(r"\s*Tilstand:.*$", "", title)
        name = re.sub(r"\s+", " ", name)
        name = re.sub(r"(?<!APO-)\bSummicron-M ASPH 75mm", "APO-Summicron-M 75mm ASPH", name)  # 75/2는 APO뿐
        if not re.search(r"\b(?:leica|leitz)\b", name, re.I):
            name = "Leica " + name
        if "Leica M" in title.split("|")[-1] and not re.search(r"\bM\b|-M\b", name):
            name += " M"
        elif "skrufatning" in title.lower():
            name += " LTM"
        m_price = re.search(r'class="[^"]*(?:price|Price)[^"]*"[^>]*>\s*([\d\s.,]+)\s*(?:kr|,-)', h)
        try:
            price = f"NOK {int(re.sub(r'[^0-9]', '', m_price.group(1))):,}" if m_price else "문의요망"
        except ValueError:
            price = "문의요망"
        m_img = re.search(r'ls-image-url="([^"]+)"', h)
        cat = detect_category(name)  # 'NOK'가 붙은 가격을 주면 바디도 액세서리로 갈림 (2026-11-05)
        mount = 'Accessory' if cat == 'Accessory' else detect_mount(name)
        results.append({
            "게시일": "",
            "site": "Foto.no (노르웨이)",
            "label": auto_label(name),
            "상품명": name,
            "세대": detect_generation(name),
            "컨디션": FOTONO_PREFIX + m_cond.group(1) if m_cond else "정보없음",
            "가격": price,
            "통화": "NOK",
            "이미지": m_img.group(1).replace(":443", "") if m_img else "",
            "링크": link,
            "품절": False,
            "예약중": False,
            "mount": mount,
            "category": cat,
            "brand": detect_brand(name),
        })
    print(f"  ✅ Foto.no 완료: {len(results)}개")
    return results


SIPKES_CATEGORIES = ["occasion-objectieven/leica", "occasion-compact-camera-s-digitaal/leica", "occasion-accessoires/leica"]


def crawl_fotosipkes():
    """Foto Sipkes (네덜란드 흐로닝언) - Magento 'occasion'(중고) 분류의 라이카 하위 분류 3개(렌즈·디지털 콤팩트·액세서리) 정적 HTML (?p=N).
    robots.txt Crawl-delay 2 → 2.5초 간격. 주문 버튼(btn-cart)이 있는 것만 판매 중. 가격 EUR. 등급 표기 없음"""
    import html as _html
    import requests
    import crawl_engine as _ce
    base = "https://www.fotosipkes.nl"
    sess = requests.Session()
    sess.headers["User-Agent"] = _ce.BROWSER_UA
    results, seen = [], set()
    print(f"\n  📂 Foto Sipkes 크롤링 시작")
    for cat in SIPKES_CATEGORIES:
        for page_num in range(1, 20):
            time.sleep(2.5)
            resp = sess.get(f"{base}/occasion-s/{cat}.html", params={"p": page_num} if page_num > 1 else None, timeout=30)
            resp.raise_for_status()
            new = 0
            for li in re.findall(r'<li class="item">(.*?)<!-- End div class product-block-inner --> </li>', re.sub(r"\s+", " ", resp.text)):
                m = re.search(r'<h2 class="product-name"><a href="([^"]+)" title="([^"]*)"', li)
                if not m or m.group(1) in seen:
                    continue
                seen.add(m.group(1))
                new += 1
                if "btn-cart" not in li:
                    continue
                name = re.sub(r"\s*\boccasion\b.*$", "", _html.unescape(m.group(2)), flags=re.I).strip()
                name = re.sub(r"\s+", " ", name)
                if not re.search(r"\b(?:leica|leitz)\b", name, re.I):
                    continue
                pr = re.search(r'class="price">€\s*([\d.]+,\d\d)<', li)
                amount = float(pr.group(1).replace(".", "").replace(",", ".")) if pr else 0
                price = f"€{amount:,.0f}" if amount else "문의요망"
                img = re.search(r'<img class="remover-image"[^>]+src="([^"]+)"', li)
                cat_ = detect_category(name, price)
                mount = 'Accessory' if cat_ == 'Accessory' else detect_mount(name)
                results.append({
                    "게시일": "",
                    "site": "Foto Sipkes (네덜란드)",
                    "label": auto_label(name),
                    "상품명": name,
                    "세대": detect_generation(name),
                    "컨디션": "정보없음",
                    "가격": price,
                    "통화": "EUR",
                    "이미지": img.group(1) if img else "",
                    "링크": m.group(1),
                    "품절": False,
                    "예약중": False,
                    "mount": mount,
                    "category": cat_,
                    "brand": detect_brand(name),
                })
            print(f"    └─ {cat} {page_num}페이지 새 상품 {new}개")
            if not new or f"?p={page_num + 1}" not in resp.text:
                break
    print(f"  ✅ Foto Sipkes 완료: {len(results)}개")
    return results


def _fct_name(title):
    """Film Camera Tokyo 제목 다듬기: 'SN. 4230670'·'Year 1970' 떼고, '(L)'은 L39, '(M)'은 뗌, 오타 'Jagur'"""
    name = re.sub(r"\s*SN\.?\s*[\d*]+\s*$", "", title, flags=re.I)
    name = re.sub(r"\s*\b(?:year|yr)\.?\s*(19|20)\d\d\b", "", name, flags=re.I)
    name = re.sub(r"\s*\(L\)", " L39", name)
    name = re.sub(r"\s*\(M\)", "", name)
    name = re.sub(r"\bJagur\b", "Jaguar", name, flags=re.I)
    name = re.sub(r"\b(\d{1,2})cm\b", lambda m: f"{int(m.group(1)) * 10}mm", name)  # '5cm' → '50mm' (모델 규칙이 mm로 봄)
    name = re.sub(r"^MINOLTA LEITZ minolta CL\b", "Leitz Minolta CL", name, flags=re.I)
    name = re.sub(r"\s+", " ", name).strip(" -")
    if not re.search(r"\b(?:leica|leitz)\b", name, re.I):
        name = "Leica " + name
    return name


def crawl_filmcameratokyo():
    """Film Camera Tokyo (일본 도쿄) - 필름 카메라점 Shopify products.json 전체(500개쯤)에서 라이카·라이츠만, 판매 중만. 가격 JPY.
    쪽 사이를 천천히(빠르면 429 'local_rate_limited'). 등급은 설명의 'Product status: A/Beautiful'
    (S/Brand New·A/Beautiful·B/Good·C/Normal·D) — 사진 평가로 글자 그대로 씀 (condition_grade FCT_PREFIX)"""
    import html as _html
    import requests
    import crawl_engine as _ce
    from condition_grade import FCT_PREFIX
    results = []
    sess = requests.Session()
    sess.headers["User-Agent"] = _ce.BROWSER_UA
    base = "https://filmcameratokyo.com"
    print(f"\n  📂 Film Camera Tokyo 크롤링 시작")
    for p in _shopify_all(sess, f"{base}/products.json", "Film Camera Tokyo"):
        title = re.sub(r"\s+", " ", _html.unescape(p.get("title") or "")).strip()
        if not re.search(r"\b(?:leica|leitz)\b", title, re.I):
            continue
        variants = p.get("variants") or [{}]
        if not any(v.get("available") for v in variants):
            continue
        name = _fct_name(title)
        text = _html.unescape(re.sub(r"<[^>]+>", " ", p.get("body_html") or ""))
        m = re.search(r"Product status\s*[:：]?\s*([SABCD])\b", text)
        cond = FCT_PREFIX + m.group(1) if m else "정보없음"
        try:
            price = f"¥{float(variants[0].get('price')):,.0f}"
        except (TypeError, ValueError):
            price = "문의요망"
        cat = detect_category(name, price)
        mount = 'Accessory' if cat == 'Accessory' else detect_mount(name)
        img = p["images"][0].get("src", "") if p.get("images") else ""
        results.append({
            "게시일": _shopify_listed(p),
            "site": "Film Camera Tokyo (일본)",
            "label": auto_label(name),
            "상품명": name,
            "세대": detect_generation(name),
            "컨디션": cond,
            "가격": price,
            "통화": "JPY",
            "이미지": img,
            "링크": f"{base}/products/{p['handle']}",
            "품절": False,
            "예약중": False,
            "mount": mount,
            "category": cat,
            "brand": detect_brand(name),
        })
    print(f"  ✅ Film Camera Tokyo 완료: {len(results)}개")
    return results

MEDIAJOY_CATEGORIES = [66002, 66014]  # 35mm 소형 카메라 › ライカ, 35mm 소형 렌즈 › ライカ


def crawl_mediajoy():
    """メディアジョイカメラ (일본 교토 통신판매 전문 중고점) - 楽ウル 몰 'ライカ' 카메라·렌즈 분류 정적 HTML (10여 개).
    목록에는 이름·가격·사진만 있어 상품 화면을 1.5초 간격으로 읽어 '在庫 ○'(재고 있음)와 'グレード：★★ 並品'을 봄.
    가격 JPY(세금 포함). 등급은 별 개수 (condition_grade MEDIAJOY_PREFIX)"""
    import html as _html
    import unicodedata
    import requests
    import crawl_engine as _ce
    from ja_normalize import ja_to_en
    from condition_grade import MEDIAJOY_PREFIX
    base = "https://mediajoycamera.com"
    site = "メディアジョイカメラ (일본)"
    sess = requests.Session()
    sess.headers["User-Agent"] = _ce.BROWSER_UA
    print(f"\n  📂 メディアジョイ 크롤링 시작")
    cards, seen = [], set()
    for cat in MEDIAJOY_CATEGORIES:
        for page_idx in range(0, 10):
            try:
                resp = sess.get(f"{base}/item-list", params={"categoryId": cat, "pageIndex": page_idx, "sortKind": 3}, timeout=30)
                resp.raise_for_status()
            except Exception as e:
                raise RuntimeError(f"メディアジョイ 분류 {cat} 못 읽음: {e}")  # 빠진 쪽이 판매완료로 바뀌지 않게
            new = 0
            for pid, img, name, price in re.findall(
                    r'<a href="/item-detail/(\d+)">\s*<img src="([^"]+)"[^>]*>.*?<p class="item-name"><a[^>]*>(.*?)</a></p>\s*'
                    r'<p class="item-price">([\d,]+)円', resp.text, re.S):
                if pid in seen:
                    continue
                seen.add(pid)
                new += 1
                cards.append((pid, img, name, price))
            if not new:
                break
            time.sleep(1.5)
    if not cards:
        raise RuntimeError("メディアジョイ 라이카 분류가 비어 있음")
    results = []
    for pid, img, raw_name, price_txt in cards:
        try:
            det = sess.get(f"{base}/item-detail/{pid}", timeout=30)
            det.raise_for_status()
        except Exception as e:
            raise RuntimeError(f"メディアジョイ 상품 {pid} 못 읽음: {e}")
        text = re.sub(r"\s+", " ", _html.unescape(re.sub(r"<[^>]+>", " ", re.sub(r"(?s)<script.*?</script>|<style.*?</style>", "", det.text))))
        time.sleep(1.5)
        if not re.search(r"在庫\s*○", text):
            continue
        m_grade = re.search(r"グレード\s*[:：]\s*(★+)", text)
        raw = unicodedata.normalize("NFKC", _html.unescape(raw_name)).strip()
        name = re.sub(r"^ライカ\s*", "", raw)
        name = re.sub(r"\bD\s?III\b", "III (DIII) Body", name)
        name = name.replace("レッドダイヤル", " Red Dial").replace("-Red Dial", " Red Dial")
        name = re.sub(r"\((M|L|R|L39)\)", lambda m: " " + {"L": "L39"}.get(m.group(1), m.group(1)), name)
        name = re.sub(r"(\d{2,3})\s?(?:mm|㎜)?\s?/\s?F\s?(\d(?:\.\d)?)", r" \1mm f\2", name)
        name = re.sub(r"\s+", " ", ja_to_en(name)).strip().replace("-Redダイヤル", " Red Dial").replace("Redダイヤル", "Red Dial")
        name = re.sub(r"(?i)^(?:leica\s+)?", "Leica ", name)
        price = f"¥{int(price_txt.replace(',', '')):,}"
        results.append({
            "site": site,
            "label": auto_label(name),
            "상품명": name,
            "세대": detect_generation(name),
            "컨디션": MEDIAJOY_PREFIX + str(len(m_grade.group(1))) if m_grade else "정보없음",
            "가격": price,
            "통화": "JPY",
            "이미지": img.replace("_400.", "_800.") if "_400." in img else img,
            "링크": f"{base}/item-detail/{pid}",
            "품절": False,
            "예약중": False,
            "mount": detect_mount(name),
            "category": detect_category(name, price),
            "brand": detect_brand(name),
        })
    print(f"  ✅ メディアジョイ 완료: {len(results)}개 (목록 {len(cards)}개)")
    return results


def crawl_katsumido():
    """銀座カツミ堂写真機店 (일본 도쿄 긴자 라이카·롤라이 중고점) - colorme 몰 'Leica(ライカ)' 분류(cbid=1788926, 하위 M·R·바르낙·
    렌즈·비조·액세서리 전부) 정적 HTML(EUC-JP), 한 쪽 60개. 팔린 상품은 몰에서 내려가 목록에는 판매 중만 남음. 가격 JPY(세금 포함).
    등급은 목록 설명 '商品状態:AB' (A·AB·B…, condition_grade KATSUMIDO_PREFIX). 새 상품('新品')은 다른 분류라 안 들어옴"""
    import html as _html
    import unicodedata
    import requests
    import crawl_engine as _ce
    from ja_normalize import ja_to_en
    from condition_grade import KATSUMIDO_PREFIX
    base = "https://www.katsumido-camera.com"
    site = "銀座カツミ堂 (일본)"
    sess = requests.Session()
    sess.headers["User-Agent"] = _ce.BROWSER_UA
    print(f"\n  📂 カツミ堂 크롤링 시작")
    results, seen, total = [], set(), None
    for page_num in range(1, 10):
        try:
            resp = sess.get(f"{base}/", params={"mode": "cate", "cbid": 1788926, "csid": 0, "sort": "n", "page": page_num}, timeout=30)
            resp.raise_for_status()
        except Exception as e:
            raise RuntimeError(f"カツミ堂 {page_num}페이지 못 읽음: {e}")  # 빠진 쪽이 판매완료로 바뀌지 않게
        text = resp.content.decode("euc-jp", "ignore")
        if total is None:
            m_total = re.search(r"全\s*\[(\d+)\]\s*商品中", text)
            if not m_total:
                raise RuntimeError("カツミ堂 목록 틀이 바뀜 (상품 수 없음)")
            total = int(m_total.group(1))
        new = 0
        for blk in re.findall(r'<div class="item_box[^"]*">(.*?)</div>\s*</div>', text, re.S):
            m_pid = re.search(r"\?pid=(\d+)", blk)
            m_name = re.search(r'<p class="item_name">\s*<a[^>]*>(.*?)</a>', blk, re.S)
            m_price = re.search(r"([\d,]+)円", blk)
            if not (m_pid and m_name and m_price) or m_pid.group(1) in seen:
                continue
            seen.add(m_pid.group(1))
            new += 1
            if re.search(r"SOLD ?OUT|売り切れ|在庫なし", blk, re.I):
                continue
            raw = unicodedata.normalize("NFKC", re.sub(r"\s+", " ", _html.unescape(re.sub(r"<[^>]+>", "", m_name.group(1))))).strip()
            if "新品" in raw:
                continue
            name = re.sub(r"\([A-Z]\d{4}\)\*?|\*$", "", raw).strip()  # 매장 관리번호 '(A4218)*'
            viso = "(V)" in name
            name = re.sub(r"\((M|R|L39|V|M3)\)", lambda m: {"V": "", "M3": "M (M3)"}.get(m.group(1), m.group(1)), name)
            name = re.sub(r"\b(\d{1,3}(?:\.\d)?)(cm|mm)?\s?/\s?(\d(?:\.\d)?)\b",
                          lambda m: f"{round(float(m.group(1)) * (10 if m.group(2) == 'cm' else 1))}mm f{m.group(3)}", name)
            name = re.sub(r"\s+", " ", ja_to_en(name)).strip()
            name = re.sub(r"(?i)^leica\s+(summilux|summicron|summaron|summarit|elmarit|elmar|hektor|noctilux)\s+(M|R)\b",
                          lambda m: f"Leica {m.group(1)}-{m.group(2)}", name)
            name = name if re.match(r"(?i)leica|leitz", name) else "Leica " + name
            if viso:
                name += " (Visoflex)"  # 'エルマー (V) 65/3.5' → 'Leica Elmar 65mm f3.5 (Visoflex)'
            if re.search(r"(?i)filter|フィルター|finder|ファインダー|hood|フード|cap\b|キャップ", name):
                name += " accessory"
            m_cond = re.search(r"商品状態\s*[:：]\s*([A-D][A-D]?[+-]?)", blk)
            img = re.search(r'<img src="([^"]+)"', blk)
            price = f"¥{int(m_price.group(1).replace(',', '')):,}"
            results.append({
                "site": site,
                "label": auto_label(name),
                "상품명": name,
                "세대": detect_generation(name),
                "컨디션": KATSUMIDO_PREFIX + m_cond.group(1) if m_cond else "정보없음",
                "가격": price,
                "통화": "JPY",
                "이미지": img.group(1).split("?")[0].replace("_th.jpg", ".jpg") if img else "",
                "링크": f"{base}/?pid={m_pid.group(1)}",
                "품절": False,
                "예약중": False,
                "mount": detect_mount(name),
                "category": detect_category(name, price),
                "brand": detect_brand(name),
            })
        print(f"    └─ {page_num}페이지 새 상품 {new}개")
        if not new or len(seen) >= total:
            break
        time.sleep(random.uniform(1.0, 2.0))
    print(f"  ✅ カツミ堂 완료: {len(results)}개 (분류 {total}개)")
    return results


MATSUBARA_NOT_LEICA = (r"(?i)7artisans|七工匠|voigtl|nokton|ultron|jupit|zeiss|biogon|sonnar|biotar|canon|angenieux|cooke|ross|taylor|"
                       r"dallmeyer|dalrac|nikkor|wollensak|velostigmat|meyer|plasmat|torioplan|kinoptik|apochromat|fulgior|astoro|konica|"
                       r"hexar|light lens lab|mr\.?ding|noxlux|alpa|zork|olympia|fernobjektiv|old delft|minor\b|u\.s\.s\.r|made in china|社外品|"
                       r"hassel|ハッセル|nikon z|n\.z\.|sony ?e|sony nex|nex/e")  # 소니 E로 개조한 렌즈도 뺌 (원래 렌즈 시세와 다름)
MATSUBARA_LEICA = r"(?i)leica|leitz|ライカ|summi|summa|elmar|hektor|noctilux|xenon|telyt|angulon|thambar|focotar|ビゾ|visoflex|summarex|tele-elmar"
MATSUBARA_ACC = (r"フード|キャップ|キヤップ|ファインダー|finder|ヘリコイド|リング|ring|雲台|三脚|ルーペ|magnifier|フィルター|filter|ベロース|アダプタ|"
                 r"adapter|wender|距離計 （|接写|ビゾフレックス3|visoflex3|extender|エクステンダー|中間")


def crawl_matsubara():
    """カメラのマツバラ光機 (일본 오사카 우메다 클래식 카메라점) - easy-myshop 몰 'Leica' 분류(category_id=9, 하위 M·L39·R·비조·액세서리
    전부) 정적 HTML, 한 쪽 100개 7쪽쯤 (620여 개 중 판매 중 230여 개). robots.txt Crawl-delay 5라 쪽마다 5초 쉼.
    'soldout_item'은 판매 완료로 뺌. 분류에 섞인 타사 렌즈(7Artisans·보이그랜더·캐논·안제니외 등)는 뺌. 가격 JPY(세금 포함).
    이름 '50/2 Summicron SN.… ライカＭ用 …'은 일련번호 앞까지 → '50mm f2 Summicron' + 마운트(M·L39·R). 등급 표기 없음 → 사진 등급 대기열"""
    import html as _html
    import unicodedata
    import requests
    import crawl_engine as _ce
    from ja_normalize import ja_to_en
    base = "https://m-camera.com"
    site = "マツバラ光機 (일본)"
    sess = requests.Session()
    sess.headers["User-Agent"] = _ce.BROWSER_UA
    print(f"\n  📂 マツバラ光機 크롤링 시작")
    results, seen = [], set()
    for page_num in range(0, 15):
        try:
            resp = sess.get(f"{base}/c-item-list", params={
                "keyword": "", "category_id": 9, "parent_category_id": 9, "page_category_id": 9, "category_search_type": 1,
                "scnt": 100, "sort": 4, "p": page_num}, timeout=40)
            resp.raise_for_status()
        except Exception as e:
            raise RuntimeError(f"マツバラ {page_num}페이지 못 읽음: {e}")  # 빠진 쪽이 판매완료로 바뀌지 않게
        cards = re.findall(r'<div class="item ([^"]*)" id="item_\d+">(.*?)<div class="item_price_block"(.*?)</a>', resp.text, re.S)
        for cls, blk, price_blk in cards:
            m_link = re.search(r'href="(https://m-camera\.com/c-item-detail\?ic=[^"]+)"', blk)
            if not m_link or m_link.group(1) in seen:
                continue
            seen.add(m_link.group(1))
            if "soldout" in cls:
                continue
            m_name = re.search(r'<div class="item_name">\s*(.*?)</div>', blk, re.S)
            m_price = re.search(r'item_price_val">([\d,]+)<', price_blk)
            if not (m_name and m_price):
                continue
            raw = unicodedata.normalize("NFKC", re.sub(r"\s+", " ", _html.unescape(m_name.group(1)))).strip()
            if not re.search(MATSUBARA_LEICA, raw) or re.search(MATSUBARA_NOT_LEICA, raw):
                continue
            mount = ("L39" if re.search(r"スクリ[ュユ]ー|L39|L-39|スクリュー", raw) else
                     "R" if re.search(r"ライカ ?R|R用|-R\b|R型|\bR\b", raw) else
                     "M" if re.search(r"M用|ライカM|Leica M\b|Mマウント", raw) else "")
            head = raw[:1] + re.split(r"\s(?:SN|S/N|Sn|L#|L ?#|B#|N\.)\s?[.:,]?\s?\d|\s?\((?:made|Made) in|\(Germany|\(Canada|ライカ|距離計|前後|専用|純正|元箱|\s{2,}", raw[1:])[0]
            lens_like = re.match(r"\d{2,3}(?:\s?/\s?|mm\s?F)\d", raw)
            acc = (bool(re.search(MATSUBARA_ACC + r"|フ-ド|フ−ド", head[:45] if len(head) > 10 else raw[:45], re.I))
                   and not lens_like) or bool(re.search(r"\b1\d{4}[A-Z]\b", raw) or re.match(r"(?i)leica \d{2}mm uv", raw))  # 'Summicron 17672U'(부품 번호)·필터
            if len(head) <= 10:
                head = re.split(r"\s{2,}", raw)[0][:60]
            name = head if not acc else re.split(r"\s{2,}", raw)[0][:70]
            name = re.sub(r"^(\d{2,3})\s?/\s?(\d(?:\.\d)?)\s+", r"\1mm f\2 ", name)
            name = re.sub(r"^(\d{2,3})mm F(\d(?:\.\d)?)\s+", r"\1mm f\2 ", name)
            name = re.sub(r"\b1([FG])\b", lambda m: "I" + m.group(1).lower(), name)
            name = re.sub(r"\bIII?([CFG])\b", lambda m: m.group(0)[:-1] + m.group(1).lower(), name)
            name = re.sub(r"ライカフレックス\s?1型", "Leicaflex", name)
            name = re.sub(r"(?i)SUPER ANGULON\s+L-Rマウント", "Super-Angulon-R", name)
            name = re.sub(r"IIIc & IIIf combination", "IIIf (converted)", name)  # IIIc 몸체에 IIIf 부품 — 두 모델 겹침으로 잡히지 않게
            m_body = re.match(r"(?i)Leica\s+(I+[cfg]|D?III|IIIc & IIIf|Ig)\b(.*)$", name)
            if m_body and re.search(r"\d{2}\s?/\s?\d", m_body.group(2)) and "Body" not in name:
                name = f"Leica {m_body.group(1)} Body + {m_body.group(2).strip()}"  # 'Leica Ig 50/3.5 Elmar …' 바디 세트가 렌즈로 붙지 않게
            name = re.sub(r"ボデー(のみ)?", " Body ", name)
            name = re.sub(r"\s+", " ", ja_to_en(name)).strip(" ,、")
            if acc:
                name = " ".join(t for t in name.split() if not re.search(r"[぀-ヿ一-鿿]", t)) or name
            name = name if re.match(r"(?i)leica|leitz", name) else "Leica " + name
            if mount and not acc and not re.search(rf"\b{mount}\b", name):
                name += f" {mount}"
            if acc:
                name += " accessory"
            price = f"¥{int(m_price.group(1).replace(',', '')):,}"
            img = re.search(r'data-src="([^"]+)"', blk)
            results.append({
                "site": site,
                "label": auto_label(name),
                "상품명": name,
                "세대": detect_generation(name),
                "컨디션": "정보없음",
                "가격": price,
                "통화": "JPY",
                "이미지": img.group(1) if img else "",
                "링크": m_link.group(1),
                "품절": False,
                "예약중": False,
                "mount": detect_mount(name),
                "category": detect_category(name, price),
                "brand": detect_brand(name),
            })
        print(f"    └─ {page_num + 1}페이지 상품 {len(cards)}개")
        if len(cards) < 100:
            break
        time.sleep(5)
    if len(seen) < 100:
        raise RuntimeError(f"マツバラ 라이카 분류 {len(seen)}개뿐")
    print(f"  ✅ マツバラ光機 완료: {len(results)}개 (분류 {len(seen)}개 중)")
    return results


def crawl_pazdera():
    """Foto Optika Jan Pazdera (체코 프라하 바츨라프 광장 옆 중고점, '체코 최대 사진 바자') - Sun-shop 몰.
    검색 화면이 상품을 다 보여 주지 않아 사이트맵(sitemap.xml)에서 중고(bazar) 주소 중 라이카 낱말(leica·leitz·laica·leicaflex)이
    든 것만 골라(20여 개) 상품 화면을 1.5초 간격으로 읽음. 상품 화면의 itemprop price·availability(InStock)·og:image를 씀.
    판매 중(InStock)만. 가격 CZK(세금 포함). 등급 표기 없음('stav plně funkční' 작동 여부뿐) → 사진 등급 대기열"""
    import html as _html
    import requests
    import crawl_engine as _ce
    base = "https://www.fotopazdera.cz"
    site = "Foto Pazdera (체코)"
    sess = requests.Session()
    sess.headers["User-Agent"] = _ce.BROWSER_UA
    print(f"\n  📂 Foto Pazdera 크롤링 시작")
    sm = sess.get(f"{base}/sitemap.xml", timeout=60)
    sm.raise_for_status()
    urls = [u for u in re.findall(r"<loc>([^<]+)</loc>", sm.text)
            if "/katalog/bazar/" in u and re.search(r"leica|leitz|laica|leicaflex", u, re.I)
            and not re.search(r"vogtl|voigtl|zeiss|distagon|panasonic|dicomar|diaprojektor", u, re.I)]
    if len(urls) < 5:
        raise RuntimeError(f"Foto Pazdera 사이트맵 라이카 {len(urls)}개뿐")  # 덜 나오면 판매 완료로 바뀌지 않게
    results = []
    for url in urls:
        try:
            resp = sess.get(url, timeout=30)
            if resp.status_code == 404:
                continue  # 사이트맵에 남은 지운 상품
            resp.raise_for_status()
        except requests.HTTPError:
            raise
        except Exception as e:
            raise RuntimeError(f"Foto Pazdera 상품 화면 못 읽음: {e}")
        text = resp.text
        m_name = re.search(r'<h1 itemprop="name">(.*?)</h1>', text, re.S)
        m_price = re.search(r'itemprop="price"[^>]*content="([\d.]+)"', text)
        in_stock = 'itemprop="availability" href="http://schema.org/InStock"' in text
        if not (m_name and m_price and in_stock):
            time.sleep(1.5)
            continue
        raw = re.sub(r"\s+", " ", _html.unescape(m_name.group(1))).strip()
        name = re.sub(r"(?i)\blaica\b", "Leica", raw)
        name = re.sub(r"(?i)\b(?:objektiv|obj)\b:?|\bfotoapar[aá]t\b", " ", name)
        name = re.sub(r"(?i)\btělo\b", "Body", name)
        name = re.sub(r"(?i)\bbajonet\s+(m|r)\b", lambda m: m.group(1).upper() + "-mount", name)
        name = re.sub(r"(?i)\brok\s+(\d{4})\b", r"(\1)", name)
        name = re.sub(r"(?i)\bkrabice\b", "box", name)
        name = re.sub(r"\b3A\b|\bIII A\b", "IIIa", name)
        name = re.sub(r"\bIII F\b", "IIIf", name)
        name = re.sub(r"(?i)^Leica Compur\b", "Leica I Compur Body", name)  # 1920년대 콤푸어 셔터 바디(+Elmar) — Elmar 렌즈로 붙지 않게
        f = lambda x: x.replace(",", ".")
        name = re.sub(r"\b(\d)[,.](\d)\s?/\s?(\d{2,3})\s?mm\b", lambda m: f"{m.group(3)}mm f{m.group(1)}.{m.group(2)}", name)  # '3,5/50mm'
        name = re.sub(r"\b(\d(?:[,.]\d)?)\s?F\s+(\d{2,3})\s?mm\b", lambda m: f"{m.group(2)}mm f{f(m.group(1))}", name)  # '3,5F 50mm'
        name = re.sub(r"\b(\d{2,3})\s?mm\s?(?:/|1\s?:\s?|1\s?-\s?)(\d(?:[,.]\d)?)\s?F?\b", lambda m: f"{m.group(1)}mm f{f(m.group(2))}", name)  # '50mm/2'·'90mm 1:4F'
        name = re.sub(r"\b(\d{2,3})\s?mm\s+(\d(?:[,.]\d)?)\s?F\b", lambda m: f"{m.group(1)}mm f{f(m.group(2))}", name)  # '135mm 4,5F'
        name = re.sub(r"\b1\s?:\s?(\d(?:[.,]\d)?)\s?/?\s?(\d{2,3})\s?mm\b", lambda m: f"{m.group(2)}mm f{f(m.group(1))}", name)
        name = re.sub(r"\s+", " ", name).strip(" -")
        name = name if re.match(r"(?i)leica|leitz|e\. ?leitz", name) else "Leica " + name
        if re.match(r"(?i)(?:e\.?\s?leitz wetzlar\s+)?(?:hledáček|blesk)|leica motor", raw) and "accessory" not in name:
            name += " accessory"  # 파인더·모터·플래시 단품이 바디·렌즈 시세에 섞이지 않게
        img = re.search(r'<meta property="og:image" content="([^"]+)"', text)
        price = f"Kč {float(m_price.group(1)):,.0f}"
        results.append({
            "site": site,
            "label": auto_label(name),
            "상품명": name,
            "세대": detect_generation(name),
            "컨디션": "정보없음",
            "가격": price,
            "통화": "CZK",
            "이미지": (img.group(1).replace("/tn_", "/") if img else ""),
            "링크": url,
            "품절": False,
            "예약중": False,
            "mount": detect_mount(name),
            "category": detect_category(name, price),
            "brand": detect_brand(name),
        })
        time.sleep(1.5)
    print(f"  ✅ Foto Pazdera 완료: {len(results)}개 (사이트맵 라이카 {len(urls)}개 중)")
    return results


def crawl_adophoto():
    """AdoPhoto (그리스 아테네 사진점) - 중고(Μεταχειρισμένα) 하위 분류 화면 10여 곳 정적 HTML (한 화면에 분류 상품 전부, 쪽 넘김은
    화면 안에서만). 상품 칸의 'filter_brand_id_7'(Leica)이거나 제목이 Leica·Leitz로 시작하는 것만.
    재고는 'filter_availability_id_1'(Άμεσα Διαθέσιμο, 바로 발송)만 판매 중 — '_5'(1~2달 뒤 입고)는 사실상 없는 물건이라 뺌.
    가격 EUR(세금 포함). 등급 표기 없음 → 사진 등급 대기열, 'Δείγμα'(시연품)만 S"""
    import html as _html
    import requests
    import crawl_engine as _ce
    from condition_grade import ADOPHOTO_PREFIX
    base = "https://www.adophoto.gr/used/metaxeirismena-eidi"
    site = "AdoPhoto (그리스)"
    sess = requests.Session()
    sess.headers["User-Agent"] = _ce.BROWSER_UA
    print(f"\n  📂 AdoPhoto 크롤링 시작")
    top = sess.get(base, timeout=30)
    top.raise_for_status()
    cats = sorted(set(re.findall(r'href="https://www\.adophoto\.gr/used/metaxeirismena-eidi/([a-z0-9-]+)"', top.text)))
    if len(cats) < 5:
        raise RuntimeError(f"AdoPhoto 중고 분류 {len(cats)}곳뿐")  # 화면이 바뀌면 판매 완료로 잘못 바뀌지 않게
    results, seen = [], set()
    for cat in cats:
        try:
            resp = sess.get(f"{base}/{cat}", timeout=30)
            resp.raise_for_status()
        except Exception as e:
            raise RuntimeError(f"AdoPhoto {cat} 못 읽음: {e}")
        for cls, price_num, blk in re.findall(
                r'class="col-md-4 active product-item-holder([^"]*)" data-price="([\d.]+)">(.*?)</ul>\s*</div>\s*</div>\s*</div>',
                resp.text, re.S):
            m_link = re.search(r'class="product-link" href="([^"]+)">(.*?)</a>', blk, re.S)
            if not m_link or m_link.group(1) in seen:
                continue
            seen.add(m_link.group(1))
            raw = re.sub(r"\s+", " ", _html.unescape(m_link.group(2))).strip()
            if not ("filter_brand_id_7 " in cls + " " or re.match(r"(?i)leica|leitz", raw)) or re.search(r"(?i)\bleica dg\b|panasonic|lumix", raw):
                continue
            if "filter_availability_id_1 " not in cls + " ":
                continue
            demo = re.search(r"Δείγμα|Δειγμα|\bsample\b|\bdemo\b", raw, re.I)
            name = re.sub(r"\((?:used|Used|USED|Δείγμα|Δειγμα|Μεταχειρισμένος)\)", "", raw)
            name = re.sub(r"\bLeica Camera\b", "Leica", name)
            if re.search(r"\b\d{2,3}-\d{2,3}mm\b", name) and re.search(r"(?i)\bR Mount\b", name) and not re.search(r"(?i)elmar|angenieux", name):
                name = name.replace("Leica ", "Leica Vario-Elmar-R ", 1)  # 'Leica 35-70mm f/3.5 Leica R Mount Lens'
            name = re.sub(r"\bf/\s+(\d)", r"f/\1", name)
            name = re.sub(r"\s+", " ", name).strip()
            img = re.search(r"background-image: url\('([^']+)'\)", blk)
            price = f"€{float(price_num):,.0f}"
            results.append({
                "site": site,
                "label": auto_label(name),
                "상품명": name,
                "세대": detect_generation(name),
                "컨디션": ADOPHOTO_PREFIX + "DEMO" if demo else "정보없음",
                "가격": price,
                "통화": "EUR",
                "이미지": img.group(1) if img else "",
                "링크": m_link.group(1),
                "품절": False,
                "예약중": False,
                "mount": detect_mount(name),
                "category": detect_category(name, price),
                "brand": detect_brand(name),
            })
        time.sleep(random.uniform(1.0, 2.0))
    print(f"  ✅ AdoPhoto 완료: {len(results)}개 (중고 분류 {len(cats)}곳)")
    return results


def crawl_pch():
    """PCH Pro Shop (벨기에 브뤼셀 사진점) - Magento 중고(Occasions) 'Leica' 분류 정적 HTML (`/fr/occasions/leica.html?p=1~`,
    한 쪽 18개, 70여 개). 중고 분류라 모두 'Occasion - pièce unique'(한 점뿐), 품절 표시가 붙은 것은 뺌. 가격 EUR(세금 포함).
    등급 표기가 없어 등급 없이 둠 (사진 등급 대기열에서 매김). 'DEMO'(시연품)는 S"""
    import html as _html
    import requests
    import crawl_engine as _ce
    from condition_grade import PCH_PREFIX
    base = "https://pch.be/fr/occasions/leica.html"
    site = "PCH Pro Shop (벨기에)"
    sess = requests.Session()
    sess.headers["User-Agent"] = _ce.BROWSER_UA
    print(f"\n  📂 PCH Pro Shop 크롤링 시작")
    results, seen, total = [], set(), None
    for page_num in range(1, 15):
        try:
            resp = sess.get(base, params={"p": page_num} if page_num > 1 else None, timeout=30)
            resp.raise_for_status()
        except Exception as e:
            raise RuntimeError(f"PCH {page_num}페이지 못 읽음: {e}")  # 빠진 쪽이 판매완료로 바뀌지 않게
        text = resp.text
        if total is None:
            nums = re.findall(r'toolbar-number">(\d+)<', text)
            total = int(nums[-1]) if nums else 0
        new = 0
        for blk in text.split('product-item-info"')[1:]:
            m_link = re.search(r'class="product-item-link"\s+href="([^"]+)"[^>]*>\s*(.*?)\s*</a>', blk, re.S)
            if not m_link or m_link.group(1) in seen:
                continue
            seen.add(m_link.group(1))
            new += 1
            if re.search(r'stock unavailable|out-of-stock|Rupture', blk, re.I):
                continue
            raw = re.sub(r"\s+", " ", _html.unescape(m_link.group(2))).strip()
            if not re.search(r"(?i)\bleica|\bleitz|\blecia", raw) or re.match(r"(?i)voigtl|kamerakraft|rapid grip", raw):
                continue
            m_price = re.search(r'data-price-amount="([\d.]+)"', blk)
            if not m_price:
                continue
            price = f"€{float(m_price.group(1)):,.0f}"
            name = re.sub(r"(?i)\s*\boccasion\b", "", raw).replace("Lecia", "Leica").strip()
            name = re.sub(r"(?i)^bo[iî]te\s+(.*)$", r"\1 box only accessory", name)  # 'Boîte Leica …' 빈 상자
            name = name.replace("–", "-")
            name = re.sub(r"(?i)\bAPO[ -]Telyt M\b", "APO-Telyt-M", name)
            name = re.sub(r"(?i)\bAPO[ -]Summicron SL\b", "APO-Summicron-SL", name)
            name = re.sub(r"\b1:(\d(?:[.,]\d)?)\s?/\s?(\d{2,3})(?:\s?mm)?\b", lambda m: f"{m.group(2)}mm f{m.group(1).replace(',', '.')}", name)  # '1:2/35' → '35mm f2'
            name = re.sub(r"\b(\d{1,2}),(\d)\s?cm\b", lambda m: f"{int(m.group(1)) * 10 + int(m.group(2))}mm", name)  # '7,3cm' → '73mm'
            name = re.sub(r"\b(\d{1,2})\s?cm\b", lambda m: f"{int(m.group(1)) * 10}mm", name)  # '5cm' → '50mm'
            name = re.sub(r"\bM-(\d{2,3}mm)", r"M \1", name)  # 'M-50mm APO-Summicron' → 'M 50mm …'
            name = re.sub(r"(?i)\bF\s?1:(\d(?:[.,]\d)?)", lambda m: f"f{m.group(1).replace(',', '.')}", name)
            name = re.sub(r"(?i)\b(\d{2,3})\s?mm\s+f/?\s?(\d(?:[.,]\d)?)\b", lambda m: f"{m.group(1)}mm f{m.group(2).replace(',', '.')}", name)
            name = re.sub(r"(?i)\b(SL|M|S)\s+(\d{2,3})\s+f/?\s?(\d(?:\.\d)?)\b", r"\1 \2mm f\3", name)  # 'Summicron-SL 50 f/2' → '50mm f2'
            if re.search(r"(?i)\b(housse|sac|poign[ée]e|filtres?|thumb|soufflet|adaptateur|adapter|grip|case|dos dmr|flash|tripod|winder|booster|sfc1|sf-?\d\d)\b", name) \
                    and "accessory" not in name:
                name += " accessory"  # 'Housse en cuir C-Lux'(가죽 케이스)가 C-Lux 바디로 붙지 않게
            img = re.search(r'class="product-image-photo"\s+src="([^"]+)"', blk)
            demo = re.search(r"(?i)\bdemo\b|comme neuf", raw)
            results.append({
                "site": site,
                "label": auto_label(name),
                "상품명": name,
                "세대": detect_generation(name),
                "컨디션": PCH_PREFIX + "DEMO" if demo else "정보없음",
                "가격": price,
                "통화": "EUR",
                "이미지": img.group(1) if img else "",
                "링크": m_link.group(1),
                "품절": False,
                "예약중": False,
                "mount": detect_mount(name),
                "category": detect_category(name, price),
                "brand": detect_brand(name),
            })
        print(f"    └─ {page_num}페이지 새 상품 {new}개")
        if not new or (total and len(seen) >= total):
            break
        time.sleep(random.uniform(1.5, 2.5))
    if total and len(seen) < total * 0.8:
        raise RuntimeError(f"PCH 상품 {len(seen)}/{total}개만 읽음")
    print(f"  ✅ PCH Pro Shop 완료: {len(results)}개")
    return results


# Pacific Rim Camera 라이카 카탈로그 화면 (책·안내지·카탈로그·잡지 화면은 뺌)
PACIFICRIM_PAGES = ["th_bm12", "th_bm21", "th_bm31", "th_bm39", "th_bk14", "th_bk31", "th_bh11", "th_bl31", "th_bl35", "th_bl33", "th_bl38"]


def crawl_pacificrim():
    """Pacific Rim Camera (미국 오리건 빈티지 딜러) - 정적 HTML 카탈로그 'Leica Hub'의 카메라·렌즈·액세서리 화면 11곳.
    상품마다 '<h3>제목/재고번호 $가격</h3>설명 …, LOOKS EX+' 꼴. 상세 화면이 없어 링크는 화면 주소 + '#재고번호'.
    제목에 LEITZ가 있거나 LEICA로 시작하는 것만 (캐논 'IN LEICA THREAD' 같은 타사 물건은 뺌). 가격 USD.
    등급은 설명 끝 Shutterbug 등급 MINT·MINT-·EX++·EX+·EX·EX-·VG+·VG·G (condition_grade PACIFICRIM_PREFIX).
    목록에 있는 것은 모두 판매 중 (팔리면 화면에서 빠짐)"""
    import html as _html
    import requests
    import crawl_engine as _ce
    from condition_grade import PACIFICRIM_PREFIX
    base = "https://www.pacificrimcamera.com/catalog"
    site = "Pacific Rim Camera (미국)"
    sess = requests.Session()
    sess.headers["User-Agent"] = _ce.BROWSER_UA
    print(f"\n  📂 Pacific Rim Camera 크롤링 시작")
    results, seen = [], set()
    for page in PACIFICRIM_PAGES:
        url = f"{base}/{page}.htm"
        try:
            resp = sess.get(url, timeout=30)
            resp.raise_for_status()
        except Exception as e:
            raise RuntimeError(f"Pacific Rim {page} 못 읽음: {e}")  # 빠진 화면이 판매완료로 바뀌지 않게
        text = resp.content.decode("latin-1", "ignore")
        if "Pacific Rim Camera" not in text:
            raise RuntimeError(f"Pacific Rim {page} 화면 틀이 바뀜")
        for m in re.finditer(r"<h3>(.*?)</H3></b>(.*?)<p>", text, re.S | re.I):
            head = re.split(r"(?i)<h3>|<hr>|</h2>", m.group(1))[-1]  # 화면 머리말이 첫 상품 제목에 붙지 않게
            title = re.sub(r"\s+", " ", _html.unescape(re.sub(r"<[^>]+>", " ", head))).strip()
            m_t = re.match(r"(.*)/(\d{4,7})\s*\$([\d,]+(?:\.\d\d)?)$", title)
            if not m_t or m_t.group(2) in seen:
                continue
            seen.add(m_t.group(2))
            raw, pid = m_t.group(1).strip(), m_t.group(2)
            if not (re.search(r"\bLEITZ\b", raw) or re.match(r"(?:\d+MM\s+)?LEICA\b", raw)):
                continue
            raw = re.sub(r"^\d+MM\s+", "", raw)  # '135MM 135/4.5 LEITZ HEKTOR' 앞의 분류용 초점거리
            desc = re.sub(r"\s+", " ", _html.unescape(re.sub(r"<[^>]+>", " ", m.group(2)))).strip()
            grades = re.findall(r"\b(MINT-?|EX\+\+|EX\+|EX-|EX|VG\+|VG|G)(?=[\s,./)]|$)", desc)
            def _word(w):
                core = w.strip(",.()")
                if re.fullmatch(r"I{1,3}[A-Ga-g]?|IV|D?II", core):  # 'IIIF' → 'IIIf'
                    return w.replace(core, core[:len(core.rstrip("ABCDEFGabcdefg"))] + core[len(core.rstrip("ABCDEFGabcdefg")):].lower())
                if re.search(r"\d", w) or core in ("ASPH", "SLR", "TTL", "MP", "SL", "R", "M", "II", "RD", "CL", "MDA", "MD"):
                    return w
                return w.capitalize()
            name = " ".join(_word(w) for w in raw.split())
            head_part = re.split(r",|\bWITH\b", raw)[0]
            if page not in ("th_bm12", "th_bm21", "th_bk14", "th_bh11") or re.search(
                    r"\bFOR\b|\b(?:BOX|BOXES|CASE|BUBBLE|CAN|CAP|BASEPLATE|BASE|FILTER|ADAPTER|ADATER|HOOD|SHADE|EXTENSION|TUBE|"
                    r"CLOSE-UP|FINDER|STAND|REPRINT|COUPLER|RING|ELPRO|EXTENDER|STRAP|GRIP|WINDER|MOTOR|FLASH|CABLE|SCREEN)\b", head_part):
                name += " accessory"  # 'Bubble for 90mm Elmar' 같은 것이 렌즈·바디 시세에 섞이지 않게
            name = re.sub(r"\b(\d{2,3})/(\d(?:\.\d)?)\b", r"\1mm f\2", name)
            name = re.sub(r"(?i)\bin leica (?:thread|screw)(?: mount)?\b", "L39", name)
            name = re.sub(r"(?i)\bin leica m mount\b", "M-mount", name)
            name = re.sub(r"(?i),?\s*with (?:rear |front )?caps?\b", "", name)  # 'With Rear Cap'이 렌즈를 액세서리로 보이게 함
            name = re.sub(r"^(?:Leica )?(\d{2,3}mm f[\d.]+) Leitz (\w+)", r"Leitz \2 \1", name)  # 'Leica 135mm f4.5 Leitz Hektor' → 'Leitz Hektor 135mm f4.5'
            name = name if re.match(r"(?:leica|leitz)\b", name, re.I) else "Leica " + name
            price = f"${float(m_t.group(3).replace(',', '')):,.0f}"
            results.append({
                "site": site,
                "label": auto_label(name),
                "상품명": name,
                "세대": detect_generation(name),
                "컨디션": PACIFICRIM_PREFIX + grades[-1] if grades else "정보없음",
                "가격": price,
                "통화": "USD",
                "이미지": f"https://www.pacificrimcamera.com/images/{pid}.jpg",
                "링크": f"{url}#{pid}",
                "품절": False,
                "예약중": False,
                "mount": detect_mount(name),
                "category": detect_category(name, price),
                "brand": detect_brand(name),
            })
        time.sleep(random.uniform(1.0, 2.0))
    print(f"  ✅ Pacific Rim Camera 완료: {len(results)}개")
    return results


CAMERACOLLECTION_JA = [("ズミルクス", "Summilux "), ("ライカフレックス", "Leicaflex "), ("A型 新エルマー", "Leica I Model A Body "), ("A型", "Leica I Model A "), ("DⅢ", "Leica III Body "),
                       ("フード・ファインダー付", " "), ("グランドグラススクリーン", "Focusing Screen "), ("後期型", "Late "),
                       ("前期型", "Early "), ("後期", "Late "), ("前期", "Early "), ("50周年", "50 Jahre "),
                       ("ハンドグリップ", "Handgrip "), ("ブラッククローム", "Black Chrome "), ("ブラックペイント", "Black Paint "),
                       ("グロッシー", "Glossy "), ("シルバー", "Silver "), ("ブラック", "Black "), ("セルフ付", "Self-timer "),
                       ("固定鏡胴", "Rigid "), ("沈胴", "Collapsible "), ("メガネ付", "with Goggles "), ("用", " for "), ("元箱付", " "),
                       ("フィッシュアイ", "Fisheye "), ("フラッシュブラケット", "Flash Bracket "), ("エクステンダー", "Extender "),
                       ("逆像ビドム", "Vidom Finder "), ("ファインダー", " Finder "), ("ゴン", "gon")]


def crawl_cameracollection():
    """カメラコレクション (일본 삿포로 중고 카메라점) - 워드프레스 재고 목록. 공개 REST API
    `/wp-json/wp/v2/itemlist?maker=30`(메이커 '라이카', 70개쯤 한 번에)에서 본문 표의 価格(세금 포함)·在庫状況·程度를 읽음.
    在庫あり만 담음 ('販売済'는 판매 완료). '店頭販売のみ発送できません'(매장 판매만)도 판매 중이라 담음.
    등급은 표의 '程度' 'AA'·'A～AA'·'AB'·'C' (condition_grade CAMERACOLLECTION_PREFIX)"""
    import html as _html
    import unicodedata
    import requests
    import crawl_engine as _ce
    from ja_normalize import ja_to_en
    from condition_grade import CAMERACOLLECTION_PREFIX
    base = "https://camera-collection.jp"
    site = "カメラコレクション (일본)"
    sess = requests.Session()
    sess.headers["User-Agent"] = _ce.BROWSER_UA
    print(f"\n  📂 カメラコレクション 크롤링 시작")
    items, page_num = [], 1
    while page_num <= 10:
        resp = sess.get(f"{base}/wp-json/wp/v2/itemlist", params={"maker": 30, "per_page": 100, "page": page_num}, timeout=30)
        resp.raise_for_status()
        items += resp.json()
        if page_num >= int(resp.headers.get("X-WP-TotalPages", "1")):
            break
        page_num += 1
        time.sleep(random.uniform(1.0, 2.0))
    if len(items) < 10:
        raise RuntimeError(f"カメラコレクション 라이카 {len(items)}개뿐")  # 덜 나오면 판매 완료로 바뀌지 않게
    results = []
    for it in items:
        body = it.get("content", {}).get("rendered", "")
        cells = {}
        for k, v in re.findall(r"<tr><td>(.*?)</td><td>(.*?)</td></tr>", body, re.S):
            key = re.sub(r"<[^>]+>|\s", "", _html.unescape(k))
            cells[key] = re.sub(r"\s+", " ", _html.unescape(re.sub(r"<[^>]+>", " ", v))).strip()
        if "在庫あり" not in cells.get("在庫状況", ""):
            continue
        m_price = re.search(r"([\d,]+)\s*円", cells.get("価格(税込）", "") or cells.get("価格(税込)", ""))
        if not m_price:
            continue
        price = f"¥{int(m_price.group(1).replace(',', '')):,}"
        title = unicodedata.normalize("NFKC", _html.unescape(it.get("title", {}).get("rendered", "")))
        raw = re.split(r"[※]", title)[0]
        raw = re.sub(r"\([^)]*#[^)]*\)", " ", raw)  # '(1st、L#1759…、1,960年)' 같은 일련번호·연도 괄호
        raw = re.sub(r"(美品|極上品|良品|現状特価品|値下しました|元箱一式.*|店頭販売のみ.*)", " ", raw)
        for ja, en in CAMERACOLLECTION_JA:
            raw = raw.replace(unicodedata.normalize("NFKC", ja), en)
        name = re.sub(r"[、,]", " ", ja_to_en(raw))
        # 남은 일본어 설명('プラCase'·'撮影に影響のない…')은 모델 연결을 흐려 뺌 — 영문·숫자 조각만 남김
        name = " ".join(t for t in name.split() if not re.search(r"[\u3040-\u30ff\u4e00-\u9fff]", t))
        name = re.sub(r"\(\s*\)|\[\s*\]|\bfor\s*$", " ", name)
        if name.count(")") > name.count("("):
            name = name.replace(")", " ")
        name = re.sub(r"\s+", " ", name).strip()
        name = re.sub(r"\b(\d{2,3})/(\d(?:\.\d)?)\b", r"\1mm f\2", name)
        name = re.sub(r"\b([RLM])(\d{2,3})mm\b", r"\1 \2mm", name)
        name = name if re.match(r"(?:leica|leitz)\b", name, re.I) else "Leica " + name
        m_grade = re.match(r"(AA\s*[~～]\s*AAA|A\s*[~～]\s*AA|AAA|AA|AB|A|B|C)", unicodedata.normalize("NFKC", cells.get("程度", "")))
        img = re.search(r'<img[^>]+src="([^"]+)"', body)
        results.append({
            "site": site,
            "label": auto_label(name),
            "상품명": name,
            "세대": detect_generation(name),
            "컨디션": CAMERACOLLECTION_PREFIX + re.sub(r"\s", "", m_grade.group(1)).replace("～", "~") if m_grade else "정보없음",
            "가격": price,
            "통화": "JPY",
            "이미지": img.group(1) if img else "",
            "링크": f"{base}/?p={it['id']}",
            "품절": False,
            "예약중": False,
            "mount": detect_mount(name),
            "category": detect_category(name, price),
            "brand": detect_brand(name),
        })
    print(f"  ✅ カメラコレクション 완료: {len(results)}개 (라이카 {len(items)}개 중 재고 있음)")
    return results


def crawl_sunrise():
    """サンライズカメラ (일본 필름카메라·올드렌즈점) - BASE 몰 'Leica（ライカ）' 분류 정적 HTML (?page=1~, 한 쪽 24개, 90여 개).
    판매 중이 앞쪽에 오고 뒤는 SOLD OUT으로 남은 것. 쪽 수는 화면의 data-last-page. SOLD OUT 빼고 판매 중만, 가격 JPY.
    등급은 목록 설명의 '【コンディションランク】 A 美品' (S·A+·A·B+·B·C·D, condition_grade SUNRISE_PREFIX)"""
    import html as _html
    import requests
    import crawl_engine as _ce
    from ja_normalize import ja_to_en
    from condition_grade import SUNRISE_PREFIX
    base = "https://www.sunrise-camera.net"
    site = "サンライズカメラ (일본)"
    sess = requests.Session()
    sess.headers["User-Agent"] = _ce.BROWSER_UA
    results, seen = [], set()
    print(f"\n  📂 サンライズカメラ 크롤링 시작")
    last_page = 1
    page_num = 1
    while page_num <= min(last_page, 15):
        try:
            resp = sess.get(f"{base}/categories/4296284", params={"page": page_num}, timeout=30)
            resp.raise_for_status()
        except Exception as e:
            raise RuntimeError(f"サンライズカメラ {page_num}페이지 못 읽음: {e}")  # 빠진 쪽이 판매완료로 바뀌지 않게
        text = resp.text
        m_last = re.search(r'id="itemList"[^>]*data-last-page="(\d+)"', text)
        if page_num == 1:
            if not m_last:
                raise RuntimeError("サンライズカメラ 목록 틀이 바뀜 (itemList 없음)")
            last_page = int(m_last.group(1))
        cards = re.findall(r'<li class="items-grid_itemListLI_\w+">(.*?)</li>', text, re.S)
        for card in cards:
            m_id = re.search(r'href="https://www\.sunrise-camera\.net/items/(\d+)"', card)
            if not m_id or m_id.group(1) in seen:
                continue
            seen.add(m_id.group(1))
            if re.search(r"items-grid_soldOut_", card):
                continue
            m_title = re.search(r'itemTitleText_\w+">(.*?)</p>', card, re.S)
            raw = _html.unescape(m_title.group(1)).strip() if m_title else ""
            if not re.search(r"(?i)leica|leitz|ライカ", raw):
                continue
            m_price = re.search(r'items-grid_price_\w+">\s*JPY\s*([\d,]+)', card)
            if not m_price:
                continue
            price = f"¥{int(m_price.group(1).replace(',', '')):,}"
            desc = _html.unescape(card)
            m_rank = re.search(r"【コンディションランク】\s*([SABCD][+＋]?)\s*", desc)
            img = re.search(r'<img class="items-grid_image_\w+" src="([^"]+)"', card)
            name = re.sub(r"[（(]\s*\d{4,6}\s*[)）]\s*$", "", raw)
            for ja, en in (("レンジファインダーフィルムカメラ", " "), ("フィルムカメラ", " "), ("ライカビット", " "), ("8枚玉", " 8 Element "),
                           ("初代", " 1st "), ("ビッグネーム", " Big Name "), ("Lマウント", " L39 "), ("Mマウント", " M "),
                           ("ドイツ", " Germany "), ("外付けフラッシュ", " Flash "), ("スピードライト", " "), ("被せ", " ")):
                name = name.replace(ja, en)
            name = re.sub(r"\s*ライカ\s*", " ", name)
            name = re.sub(r"\s+", " ", ja_to_en(name)).strip()
            name = name if re.match(r"(?:leica|leitz)\b", name, re.I) else "Leica " + name
            results.append({
                "site": site,
                "label": auto_label(name),
                "상품명": name,
                "세대": detect_generation(name),
                "컨디션": SUNRISE_PREFIX + m_rank.group(1).replace("＋", "+") if m_rank else "정보없음",
                "가격": price,
                "통화": "JPY",
                "이미지": _html.unescape(img.group(1)).split("?")[0] if img else "",
                "링크": f"{base}/items/{m_id.group(1)}",
                "품절": False,
                "예약중": False,
                "mount": detect_mount(name),
                "category": detect_category(name, price),
                "brand": detect_brand(name),
            })
        print(f"    └─ {page_num}/{last_page}페이지 상품 {len(cards)}개")
        page_num += 1
        time.sleep(random.uniform(1.5, 2.5))
    print(f"  ✅ サンライズカメラ 완료: {len(results)}개")
    return results


MORITZ_EXTRA_JA = [("レッドダイヤル", "Red Dial "), ("ブラックダイヤル", "Black Dial "), ("ダイヤル", "Dial "), ("セルフ付", "Self-timer "),
                   ("ブラックボディ", "Black Body"), ("ブラック", "Black "), ("ボディ", "Body "), ("ミニルックス", "Minilux "),
                   ("ベローズ", "Visoflex Bellows "), ("カナダ", "Canada "), ("ライツカナダ", "Leitz Canada "), ("沈胴", "Collapsible "),
                   ("固定鏡胴", "Rigid "), ("後期型", "Late "), ("初期型", "Early "), ("前期型", "Early "), ("後期", "Late "),
                   ("Ｍマウント", "M mount"), ("Ｌマウント", "L39"), ("マウント", " mount"), ("ダブルストローク", "Double Stroke "),
                   ("シングルストローク", "Single Stroke "), ("ファインダー", "Finder "), ("製造", "")]
MORITZ_NOT_LEICA = r"キャノン|キヤノン|ジュピター|ニッコール|シュタンハイル|ソリゴール|コムラー|インダスタール|ロッコール|クルト|フレクサメーター|ローライ|ツァイス|ツアイス|フォクトレンダー|ペンタックス|ミノルタ|オリンパス"


def crawl_moritz():
    """クラシックカメラ モリッツ (일본 신주쿠) - 'ドイツカメラ(ライカ・ローライ)' 한 화면(doitu.html, Shift_JIS 정적 HTML 표).
    상품마다 사진 번호(./image/jpeg/3026.jpg)가 있어 그것을 링크 꼬리표(#3026)로 씀. 가격 칸이 '売り切れ'이면 판매 완료.
    가격은 세금 별도(税別)라 10%를 더해 JPY(세금 포함)로. 다른 회사 L39 렌즈(캐논·주피터 등)는 뺌.
    등급은 설명 끝 '外観良上品'·'外観極上' 꼴 (condition_grade MORITZ_PREFIX)"""
    import html as _html
    import unicodedata
    import requests
    import crawl_engine as _ce
    from ja_normalize import ja_to_en
    from condition_grade import MORITZ_PREFIX
    base = "https://www.moritz.co.jp"
    site = "モリッツ (일본)"
    sess = requests.Session()
    sess.headers["User-Agent"] = _ce.BROWSER_UA
    print(f"\n  📂 モリッツ 크롤링 시작")
    resp = sess.get(f"{base}/doitu.html", timeout=30)
    resp.raise_for_status()
    text = resp.content.decode("cp932", "ignore")
    blocks = re.findall(r'<A HREF="\./image/jpeg/\s*(\d+)\.jpg\s*"(.*?)</TABLE></CENTER>', text, re.S | re.I)
    if len(blocks) < 10:
        raise RuntimeError(f"モリッツ 상품 칸 {len(blocks)}개뿐")  # 화면이 바뀌면 판매 완료로 잘못 바뀌지 않게
    results, seen = [], set()
    for pid, block in blocks:
        if pid in seen:  # 위쪽 '새로 들어온 상품' 칸과 아래 목록에 같은 상품이 두 번 나옴
            continue
        seen.add(pid)
        m_name = re.search(r'<FONT SIZE="\+1"><B>(.*?)</B>', block, re.S | re.I)
        if not m_name:
            continue
        parts = [unicodedata.normalize("NFKC", _html.unescape(re.sub(r"<[^>]+>", " ", p))).strip()
                 for p in re.split(r"<BR>", m_name.group(1), flags=re.I)]
        first = re.sub(r"\s+", " ", parts[0])
        second = re.sub(r"\s+", " ", " ".join(parts[1:]))
        if not re.search(r"ライカ|ライツ|ズミ|ズマ|エルマ|ノクチ|テリート|ヘクトール|Leica|Leitz", first, re.I):
            continue
        if re.search(MORITZ_NOT_LEICA, first):
            continue
        m_price = re.search(r'<FONT SIZE="\+2"><B>(.*?)</B>', block, re.S | re.I)
        price_cell = re.sub(r"\s+", "", m_price.group(1)) if m_price else ""
        sold = "売り切れ" in price_cell
        m_yen = re.search(r"\\(\d[\d,]*)", price_cell)
        if sold or not m_yen:
            continue
        price = f"¥{round(int(m_yen.group(1).replace(',', '')) * 1.1):,}"
        desc = unicodedata.normalize("NFKC", _html.unescape(re.sub(r"<[^>]+>", " ", block.split("</B></FONT><BR><BR>", 1)[-1])))
        m_grade = re.search(r"外観\s*(極上|美品|良上品|良上|良品|並上|並品|並)", desc)
        lens_extra = second if re.search(r"\d+/\d|cm|mm|ミリ|マウント|カム", second) and not second.startswith("#") else ""
        raw = f"{first} {lens_extra}".strip()
        if second.startswith("#") and not re.search(r"\d+/\d|ボディ|ズミ|ズマ|エルマ|ファインダー|ベローズ", first):
            raw += " ボディ"  # 'ライカ IIf ブラックダイヤル' + 일련번호뿐인 줄 → 바디
        raw = re.sub(r"#\S+", " ", raw)
        for ja, en in MORITZ_EXTRA_JA:
            raw = raw.replace(unicodedata.normalize("NFKC", ja), en)
        name = re.sub(r"\s+", " ", ja_to_en(raw)).strip()
        name = re.sub(r"\b(\d{2,3})/(\d(?:\.\d)?)\b", r"\1mm f\2", name)
        name = name if re.match(r"(?:leica|leitz)\b", name, re.I) else "Leica " + name
        results.append({
            "site": site,
            "label": auto_label(name),
            "상품명": name,
            "세대": detect_generation(name),
            "컨디션": MORITZ_PREFIX + m_grade.group(1) if m_grade else "정보없음",
            "가격": price,
            "통화": "JPY",
            "이미지": f"{base}/image/jpeg/{pid}.jpg",
            "링크": f"{base}/doitu.html#{pid}",
            "품절": False,
            "예약중": False,
            "mount": detect_mount(name),
            "category": detect_category(name, price),
            "brand": detect_brand(name),
        })
    print(f"  ✅ モリッツ 완료: {len(results)}개 (상품 칸 {len(seen)}개)")
    return results


def crawl_all():
    from concurrent.futures import ThreadPoolExecutor, as_completed
    import crawl_engine as ce

    start_time = time.time()
    write_status(0, "Starting...", 0, 0)
    crawl_time = ce.now_kst()
    force_full = os.environ.get("CRAWL_FULL") == "1"

    # 이전 결과 → 사이트별 병합 기준
    try:
        with open("data/raw/results.json", "r", encoding="utf-8") as f:
            prev_all = json.load(f)
    except (OSError, ValueError):
        prev_all = []
    prev_by_site = {}
    for r in prev_all:
        prev_by_site.setdefault(r.get("site"), []).append(r)
    print(f"📋 기존 매물 {len(prev_all)}개 로드")

    # 이미 판매 완료로 기록된 링크 (Kamerastore 등에서 건너뜀)
    try:
        with open("data/sold_items.json", "r", encoding="utf-8") as f:
            globals()['SOLD_LINKS'] = {r["링크"] for r in json.load(f)}
    except (OSError, ValueError):
        globals()['SOLD_LINKS'] = set()

    freshness = ce.load_freshness()

    def keep_name(name):
        if re.search(r'^\d+[-\s]*판매완료|^\d+[-\s]*보류', name):
            return False
        return not any(b in name.lower() for b in NON_LEICA_BRANDS)

    def run_cafe24(site):
        full = ce.needs_full_sweep(site["name"], freshness, crawl_time, force_full)
        known = {r["링크"] for r in prev_by_site.get(site["name"], [])}
        run = ce.crawl_cafe24_http(site, known, full, keep_name, fix_img_url, normalize_price)
        if not run["ok"] and not run["rows"]:
            # HTML 구조가 바뀌어 HTTP로 못 읽으면 예전 브라우저 방식으로 전체 수집
            print(f"  ↪ {site['name']}: HTTP 수집 실패({run.get('error')}) → 브라우저로 전체 수집")
            run = ce.wrap_full_run(site["name"], lambda: crawl_site(site))
        return run

    # 예전 크롤에서 남은 '1234 - 판매완료/보류' 자리표시 행은 매물이 아님 → 병합 전에 정리
    for _name in [s["name"] for s in SITES]:
        if _name in prev_by_site:
            prev_by_site[_name] = [r for r in prev_by_site[_name] if keep_name(r.get("상품명", ""))]

    sources = [(s["name"], (lambda s=s: run_cafe24(s))) for s in SITES]
    sources += [
        ("Ffordes (영국)", lambda: ce.wrap_full_run("Ffordes (영국)", lambda: _with_browser(crawl_ffordes, {"Accept-Language": "en-GB,en;q=0.9"}))),
        ("Leica Store Miami", lambda: ce.wrap_full_run("Leica Store Miami", crawl_leicamiami)),
        ("Kamerastore (핀란드)", lambda: ce.wrap_full_run("Kamerastore (핀란드)", crawl_kamerastore)),
        ("M & K Kamera (홍콩)", lambda: ce.wrap_full_run("M & K Kamera (홍콩)", crawl_mkkamera)),
        ("Leica Store France (프랑스)", lambda: ce.wrap_full_run("Leica Store France (프랑스)", crawl_leicafrance)),
        ("Leica Store Singapore (싱가포르)", lambda: ce.wrap_full_run("Leica Store Singapore (싱가포르)", crawl_leicasg)),
        ("Newoldcamera (이탈리아)", lambda: ce.wrap_full_run("Newoldcamera (이탈리아)", crawl_newoldcamera)),
        ("Camtec Photo (캐나다)", lambda: ce.wrap_full_run("Camtec Photo (캐나다)", crawl_camtec)),
        ("Aperture (영국)", lambda: ce.wrap_full_run("Aperture (영국)", crawl_aperture)),
        ("Harrison Cameras (영국)", lambda: ce.wrap_full_run("Harrison Cameras (영국)", crawl_harrison)),
        ("Wex Photo Video (영국)", lambda: ce.wrap_full_run("Wex Photo Video (영국)", crawl_wex)),
        ("기타무라 (일본)", lambda: ce.wrap_full_run("기타무라 (일본)", crawl_kitamura)),
        ("Camera West (미국)", lambda: ce.wrap_full_run("Camera West (미국)", crawl_camerawest)),
        ("Peter Loy (영국)", lambda: ce.wrap_full_run("Peter Loy (영국)", crawl_peterloy)),
        ("Lucky Camera (일본)", lambda: ce.wrap_full_run("Lucky Camera (일본)", crawl_lucky)),
        ("Akasaka Camera (일본)", lambda: ce.wrap_full_run("Akasaka Camera (일본)", crawl_akasaka)),
        ("Glazers Camera (미국)", lambda: ce.wrap_full_run("Glazers Camera (미국)", crawl_glazers)),
        ("Tamarkin Camera (미국)", lambda: ce.wrap_full_run("Tamarkin Camera (미국)", crawl_tamarkin)),
        ("카메라노나니와 (일본)", lambda: ce.wrap_full_run("카메라노나니와 (일본)", crawl_naniwa)),
        ("Calumet (독일)", lambda: ce.wrap_full_run("Calumet (독일)", crawl_calumet)),
        ("Camera Electronic (호주)", lambda: ce.wrap_full_run("Camera Electronic (호주)", crawl_cameraelectronic)),
        ("Nivo Schweitzer (네덜란드)", lambda: ce.wrap_full_run("Nivo Schweitzer (네덜란드)", crawl_nivo)),
        ("fotohandel.de (독일)", lambda: ce.wrap_full_run("fotohandel.de (독일)", crawl_fotohandel)),
        ("三宝カメラ (일본)", lambda: ce.wrap_full_run("三宝カメラ (일본)", crawl_sanpou)),
        ("Leica Store Heidelberg (독일)", lambda: ce.wrap_full_run("Leica Store Heidelberg (독일)", crawl_heidelberg)),
        # Vibe.pl (폴란드) 보류: 미국(GitHub)·도쿄 중계 서버 모두 상품 API 403 (데이터센터 IP 차단, 2026-10-19). 수집기는 남겨 둠
        ("Foto Köster (독일)", lambda: ce.wrap_full_run("Foto Köster (독일)", crawl_koester)),
        ("Lecuit (룩셈부르크)", lambda: ce.wrap_full_run("Lecuit (룩셈부르크)", crawl_lecuit)),
        ("カメラの大貫 (일본)", lambda: ce.wrap_full_run("カメラの大貫 (일본)", crawl_ohnuki)),
        ("喜久屋カメラ (일본)", lambda: ce.wrap_full_run("喜久屋カメラ (일본)", crawl_kikuya)),
        ("가산카메라", lambda: ce.wrap_full_run("가산카메라", crawl_kasan)),
        ("K-Camera", lambda: ce.wrap_full_run("K-Camera", crawl_kcamera)),
        ("MF Camera (미국)", lambda: ce.wrap_full_run("MF Camera (미국)", crawl_mfcamera)),
        ("Classic Connection (미국)", lambda: ce.wrap_full_run("Classic Connection (미국)", crawl_classicconnection)),
        ("The Classic Camera (영국)", lambda: ce.wrap_full_run("The Classic Camera (영국)", crawl_classiccamera)),
        ("Japan Camera Hunter (일본)", lambda: ce.wrap_full_run("Japan Camera Hunter (일본)", crawl_jch)),
        ("Rangefinder (홍콩)", lambda: ce.wrap_full_run("Rangefinder (홍콩)", crawl_rangefinder)),
        ("Roter Punkt (독일)", lambda: ce.wrap_full_run("Roter Punkt (독일)", crawl_roterpunkt)),
        ("Photografica (덴마크)", lambda: ce.wrap_full_run("Photografica (덴마크)", crawl_photografica)),
        ("SHphoto (독일)", lambda: ce.wrap_full_run("SHphoto (독일)", crawl_shphoto)),
        ("Fotohandel Delfshaven (네덜란드)", lambda: ce.wrap_full_run("Fotohandel Delfshaven (네덜란드)", crawl_delfshaven)),
        ("Camera Tweedehands (네덜란드)", lambda: ce.wrap_full_run("Camera Tweedehands (네덜란드)", crawl_cameratweedehands)),
        ("One Of Many Cameras (덴마크)", lambda: ce.wrap_full_run("One Of Many Cameras (덴마크)", crawl_oneofmany)),
        ("Foto Ottica Cavour (이탈리아)", lambda: ce.wrap_full_run("Foto Ottica Cavour (이탈리아)", crawl_cavour)),
        ("Photo Suffren (프랑스)", lambda: ce.wrap_full_run("Photo Suffren (프랑스)", crawl_suffren)),
        ("Cardinal Camera Used (미국)", lambda: ce.wrap_full_run("Cardinal Camera Used (미국)", crawl_cardinal)),
        ("Five Star Camera (일본)", lambda: ce.wrap_full_run("Five Star Camera (일본)", crawl_fivestar)),
        ("Leica Store Amsterdam (네덜란드)", lambda: ce.wrap_full_run("Leica Store Amsterdam (네덜란드)", crawl_leicastoreamsterdam)),
        ("Sabatini Fotografia (이탈리아)", lambda: ce.wrap_full_run("Sabatini Fotografia (이탈리아)", crawl_sabatini)),
        ("KOMEHYO (일본)", lambda: ce.wrap_full_run("KOMEHYO (일본)", crawl_komehyo)),
        ("トップカメラ (일본)", lambda: ce.wrap_full_run("トップカメラ (일본)", crawl_topcamera)),
        ("Leica Store Konstanz (독일)", lambda: ce.wrap_full_run("Leica Store Konstanz (독일)", crawl_konstanz)),
        ("M&S Materiale Fotografico (이탈리아)", lambda: ce.wrap_full_run("M&S Materiale Fotografico (이탈리아)", crawl_msmateriale)),
        ("Leica Store Poland (폴란드)", lambda: ce.wrap_full_run("Leica Store Poland (폴란드)", crawl_leicastorepl)),
        ("Photo Warehouse (뉴질랜드)", lambda: ce.wrap_full_run("Photo Warehouse (뉴질랜드)", crawl_photowarehouse)),
        ("富士越カメラ (일본)", lambda: ce.wrap_full_run("富士越カメラ (일본)", crawl_fujikoshi)),
        ("カメラの大林 (일본)", lambda: ce.wrap_full_run("カメラの大林 (일본)", crawl_ohbayashi)),
        ("used-photo.de (독일)", lambda: ce.wrap_full_run("used-photo.de (독일)", crawl_usedphoto)),
        ("Howard Parker (영국)", lambda: ce.wrap_full_run("Howard Parker (영국)", crawl_howardparker)),
        # PhotoCo (호주): GitHub 서버에서 매번 403이라 보류 (2026-11-02, 수집기는 남겨 둠)
        ("J-カメラ (일본)", lambda: ce.wrap_full_run("J-カメラ (일본)", crawl_jcamera)),
        ("Kenmore Camera (미국)", lambda: ce.wrap_full_run("Kenmore Camera (미국)", crawl_kenmore)),
        ("Used.cl (칠레)", lambda: ce.wrap_full_run("Used.cl (칠레)", crawl_usedcl)),
        ("Foto Dotti (이탈리아)", lambda: ce.wrap_full_run("Foto Dotti (이탈리아)", crawl_fotodotti)),
        ("The Rangefinder (캐나다)", lambda: ce.wrap_full_run("The Rangefinder (캐나다)", crawl_therangefinder)),
        ("Leica Store Australia (호주)", lambda: ce.wrap_full_run("Leica Store Australia (호주)", lambda: _with_browser(crawl_leicastoreau))),
        ("Leica Store Malaysia (말레이시아)", lambda: ce.wrap_full_run("Leica Store Malaysia (말레이시아)", crawl_leicastoremy)),
        ("Image Foto (덴마크)", lambda: ce.wrap_full_run("Image Foto (덴마크)", crawl_imagefoto)),
        ("Foto Meyer (독일)", lambda: ce.wrap_full_run("Foto Meyer (독일)", crawl_fotomeyer)),
        ("Photo19 (이탈리아)", lambda: ce.wrap_full_run("Photo19 (이탈리아)", crawl_photo19)),
        ("Panajou (프랑스)", lambda: ce.wrap_full_run("Panajou (프랑스)", crawl_panajou)),
        ("gebrauchtkameras.de (독일)", lambda: ce.wrap_full_run("gebrauchtkameras.de (독일)", crawl_gebrauchtkameras)),
        ("三葉堂寫眞機店 (일본)", lambda: ce.wrap_full_run("三葉堂寫眞機店 (일본)", crawl_mitsubado)),
        ("Au Vieux Format (프랑스)", lambda: ce.wrap_full_run("Au Vieux Format (프랑스)", crawl_auvieuxformat)),
        ("Foto Curatolo (이탈리아)", lambda: ce.wrap_full_run("Foto Curatolo (이탈리아)", crawl_fotocuratolo)),
        ("Midwest Photo (미국)", lambda: ce.wrap_full_run("Midwest Photo (미국)", crawl_mpex)),
        ("2nd BASE (일본)", lambda: ce.wrap_full_run("2nd BASE (일본)", crawl_2ndbase)),
        ("Scandinavian Photo (스웨덴)", lambda: ce.wrap_full_run("Scandinavian Photo (스웨덴)", crawl_scandinavianphoto)),
        ("잇츠카메라", lambda: ce.wrap_full_run("잇츠카메라", crawl_itscamera)),
        ("Film Camera Tokyo (일본)", lambda: ce.wrap_full_run("Film Camera Tokyo (일본)", crawl_filmcameratokyo)),
        ("Foto Sipkes (네덜란드)", lambda: ce.wrap_full_run("Foto Sipkes (네덜란드)", crawl_fotosipkes)),
        ("Foto.no (노르웨이)", lambda: ce.wrap_full_run("Foto.no (노르웨이)", crawl_fotono)),
        ("Chiswick Camera Centre (영국)", lambda: ce.wrap_full_run("Chiswick Camera Centre (영국)", crawl_chiswick)),
        ("Foto Görlitz (독일)", lambda: ce.wrap_full_run("Foto Görlitz (독일)", crawl_fotogoerlitz)),
        ("Camera Obscura Elburg (네덜란드)", lambda: ce.wrap_full_run("Camera Obscura Elburg (네덜란드)", crawl_cameraobscura)),
        ("メディアジョイカメラ (일본)", lambda: ce.wrap_full_run("メディアジョイカメラ (일본)", crawl_mediajoy)),
        ("銀座カツミ堂 (일본)", lambda: ce.wrap_full_run("銀座カツミ堂 (일본)", crawl_katsumido)),
        ("マツバラ光機 (일본)", lambda: ce.wrap_full_run("マツバラ光機 (일본)", crawl_matsubara)),
        ("Foto Pazdera (체코)", lambda: ce.wrap_full_run("Foto Pazdera (체코)", crawl_pazdera)),
        ("AdoPhoto (그리스)", lambda: ce.wrap_full_run("AdoPhoto (그리스)", crawl_adophoto)),
        ("PCH Pro Shop (벨기에)", lambda: ce.wrap_full_run("PCH Pro Shop (벨기에)", crawl_pch)),
        ("Pacific Rim Camera (미국)", lambda: ce.wrap_full_run("Pacific Rim Camera (미국)", crawl_pacificrim)),
        ("カメラコレクション (일본)", lambda: ce.wrap_full_run("カメラコレクション (일본)", crawl_cameracollection)),
        ("サンライズカメラ (일본)", lambda: ce.wrap_full_run("サンライズカメラ (일본)", crawl_sunrise)),
        ("モリッツ (일본)", lambda: ce.wrap_full_run("モリッツ (일본)", crawl_moritz)),
    ]
    sources += [(site, (lambda site=site, cc=cc: ce.wrap_full_run(site, lambda: crawl_leica_classic(cc))))
                for _, cc, site in LEICA_CLASSIC_COUNTRIES]
    # 느리거나 자주 안 바뀌는 사이트는 최소 간격마다만 (그 사이엔 이전 데이터 유지)
    if not force_full and not SITE_FILTER:
        skipped = []
        for _name, _hours in SOURCE_MIN_INTERVAL_HOURS.items():
            _since = ce.hours_between((freshness.get(_name) or {}).get("last_attempt"), crawl_time)
            if _since is not None and _since < _hours:
                skipped.append(_name)
        if skipped:
            sources = [x for x in sources if x[0] not in skipped]
            print(f"⏭️ 간격 전이라 건너뜀: {', '.join(skipped)}")
    if SITE_FILTER:
        sources = [x for x in sources if SITE_FILTER.lower() in x[0].lower()]
        print(f"🎯 사이트 필터: {SITE_FILTER} ({len(sources)}개, 나머지 사이트는 이전 데이터 유지)")

    print(f"🚀 수집 시작 ({len(sources)}개 사이트, 동시 4개)")
    runs = {}
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = {executor.submit(fn): name for name, fn in sources}
        for future in as_completed(futures):
            name = futures[future]
            try:
                runs[name] = future.result()
            except Exception as e:
                runs[name] = {"site": name, "ok": False, "rows": [], "coverage": "full", "error": str(e)[:200]}
            run = runs[name]
            print(f"  {'✅' if run['ok'] else '❌'} {name}: {len(run['rows'])}개 ({run.get('coverage')}, "
                  f"{run.get('pages') or '-'}페이지, {run.get('seconds') or 0}초){' ' + run['error'] if run.get('error') else ''}")
            write_status(int(len(runs) / len(sources) * 100) - 1, name, sum(len(x["rows"]) for x in runs.values()), len(runs))

    # 사이트별 병합: 바뀐 것만 이벤트로, 실패·의심 사이트는 이전 데이터 유지
    unique_results, all_events, site_stats = [], [], []
    site_order = list(dict.fromkeys([r.get("site") for r in prev_all] + [name for name, _ in sources]))
    for name in site_order:
        prev_rows = prev_by_site.get(name, [])
        if name not in runs:
            unique_results.extend(prev_rows)
            continue
        merged, events, stat = ce.merge_source(prev_rows, runs[name], crawl_time)
        unique_results.extend(merged)
        all_events.extend(events)
        site_stats.append(stat)
        ce.update_freshness(freshness, stat, crawl_time)
        if stat["status"] == "ok":
            print(f"  🔀 {name}: {stat['rows']}개 (판매 중 {stat['active']}) · 신규 {stat['new']} · 변경 {stat['changed']} · 유지 {stat['carried']}")
        else:
            print(f"  ⚠️ {name}: {stat['status']} ({stat['reason']}) → 이전 데이터 {stat['kept']}개 유지")
    for e in all_events:
        if e["type"] == "new":
            print(f"  🆕 신규: {str(e.get('title'))[:40]}")
    # 목록엔 컨디션이 없고 상세 페이지에만 있는 사이트 (장씨카메라: '상태 95%')
    for _site, _pattern in DETAIL_CONDITION.items():
        if SITE_FILTER and SITE_FILTER.lower() not in _site.lower():
            continue
        _n = ce.enrich_detail_condition(unique_results, _site, _pattern, crawl_time)
        if _n:
            print(f"  🔎 {_site}: 상세 페이지에서 컨디션 {_n}건 채움")
    elapsed = time.time() - start_time

    # label 자동 보정 + 상품명 정리 + system/category 분류
    import datetime
    _KST = datetime.timezone(datetime.timedelta(hours=9))
    crawl_time = datetime.datetime.now(_KST).strftime("%Y-%m-%d %H:%M:%S")
    for r in unique_results:
        name = r['상품명']
        # 상품명에서 "상품명 :" 제거
        if name.startswith('상품명') and ':' in name:
            name = name.split(':', 1)[-1].strip()
            r['상품명'] = name
        name_lower = name.lower()
        # system/category 분류
        r['category'] = detect_category(r['상품명'], r.get('가격', ''))
        # label 항상 재계산 (코드 업데이트 반영)
        r['label'] = auto_label(r['상품명'])
        r['mount'] = detect_mount(r['상품명'])
        r['brand'] = detect_brand(r['상품명'])
        if r['category'] == 'Accessory':
            r['label'] = ''  # Accessory는 label 제거 (평균가 왜곡 방지)
        r['mount'] = detect_mount(r['상품명'])
        # Accessory는 mount=Accessory로 강제
        if r['category'] == 'Accessory':
            r['mount'] = 'Accessory'
        # brand 필드: 없으면 상품명에서 자동 감지
        if not r.get('brand'):
            r['brand'] = detect_brand(r['상품명'])
        # 세대·system: HTTP 수집 행에도 같은 값 (first_seen은 병합 단계에서, 수집 시각은 사이트별 source_freshness.json)
        r['세대'] = detect_generation(r['상품명'])
        if 'system' not in r:
            r['system'] = detect_system(r['상품명'])
        r.pop('crawl_time', None)
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
                    # 500~1,500만원 → 라이카 공식 복각 (ASPH)
                    r['label'] = '50mm Noctilux f1.2 ASPH'
                    r['brand'] = 'Leica'
                elif 1_000_000 <= price_num < 5_000_000:
                    # 100~500만원 → 써드파티 복각
                    r['label'] = '50mm Noctilux f1.2 복각'
                    if r.get('brand') not in ['Leica']:
                        r['brand'] = '3rd Party'
        except Exception:
            pass

    # ── 판매 완료 추적 (sold_items.json): 병합 단계의 sold/gone 이벤트만 ──
    try:
        with open("data/sold_items.json", "r", encoding="utf-8") as f:
            sold_items = json.load(f)
    except (OSError, ValueError):
        sold_items = []
    sold_links = {r["링크"] for r in sold_items}
    by_link = {r["링크"]: r for r in unique_results}
    prev_by_link = {r["링크"]: r for r in prev_all}
    newly_sold = []
    for e in all_events:
        if e["type"] not in ("sold", "gone") or e["link"] in sold_links:
            continue
        sold_r = dict(by_link.get(e["link"]) or prev_by_link.get(e["link"]) or {})
        sold_r.pop("missing_runs", None)
        sold_r.pop("crawl_time", None)
        sold_r.update({"is_sold": True, "sold_at": e["t"], "hours_to_sell": e.get("hours_to_sell"), "sold_reason": e["type"]})
        if sold_r.get("sold_fx_krw") is None:  # 판매 순간 환율 (나중에 그날 시세를 다시 계산할 때)
            _fx = ce.fx_krw_now(sold_r.get("통화") or e.get("currency"))
            if _fx is not None:
                sold_r["sold_fx_krw"] = _fx
        newly_sold.append(sold_r)
        sold_links.add(e["link"])
        print(f"  💸 판매 완료: {str(e.get('title'))[:40]} ({e.get('hours_to_sell')}시간)")
    if newly_sold:
        sold_items = (sold_items + newly_sold)[-3000:]
        with open("data/sold_items.json", "w", encoding="utf-8") as f:
            json.dump(sold_items, f, ensure_ascii=False, indent=2)
        print(f"  💸 총 {len(newly_sold)}개 판매 완료 추가 → sold_items.json")

    # ── 변경 기록 · 사이트 확인 시각 (저장소에는 바뀐 것만 남김) ──
    _events_path = ce.append_events(all_events, crawl_time)
    if _events_path:
        print(f"  🧾 변경 {len(all_events)}건 → {_events_path}")
    ce.save_freshness(freshness)

    # ── 스냅샷: 저장소 대신 data/snapshots/ (gitignore, 워크플로가 Actions 보관함에 올림) ──
    import os as _os
    _os.makedirs("data/snapshots", exist_ok=True)
    _snap_path = f"data/snapshots/raw_{crawl_time.replace('-', '').replace(':', '').replace(' ', '_')}.json"
    with open(_snap_path, "w", encoding="utf-8") as f:
        json.dump(unique_results, f, ensure_ascii=False)
    for _old_f in sorted(x for x in _os.listdir("data/snapshots") if x.startswith("raw_"))[:-30]:
        _os.remove(f"data/snapshots/{_old_f}")
    # 키 순서를 고정해 바뀐 매물만 diff에 나오게
    with open("data/raw/results.json", "w", encoding="utf-8") as f:
        json.dump(unique_results, f, ensure_ascii=False, indent=2, sort_keys=True)
    # ── normalized 저장 ──
    _normalized = []
    for r in unique_results:
        _normalized.append({
            "listing_id": r.get("링크",""),
            "source": r.get("site",""),
            "source_url": r.get("링크",""),
            "title_raw": r.get("상품명",""),
            "price": r.get("가격",""),
            "currency": r.get("통화",""),
            "label": r.get("label",""),
            "mount": r.get("mount",""),
            "brand": r.get("brand",""),
            "category": r.get("category",""),
            "condition_raw": r.get("컨디션",""),
            "is_sold": r.get("품절", False),
            "image": r.get("이미지",""),
            "first_seen": r.get("first_seen",""),
        })
    _os.makedirs("data/normalized", exist_ok=True)
    with open("data/normalized/normalized_latest.json", "w", encoding="utf-8") as f:
        json.dump(_normalized, f, ensure_ascii=False, indent=2)
    print(f"  📋 normalized 저장 → data/normalized/normalized_latest.json ({len(_normalized)}개)")
    # ── 상태 플래그 추출 ──
    import os as _os_flags
    _os_flags.makedirs("data/derived", exist_ok=True)
    _FLAG_RULES = {
        "fungus":      ["fungus","곰팡이","fungi"],
        "haze":        ["haze 후드","haze filter","헤이즈 후드"],
        "separation":  ["separation","코팅분리","코팅 분리","balsam"],
        "repair":      ["repair","수리","수리이력","수리 이력","repaired"],
        "cla":         [" cla ","(cla)","cla'd","정비완료","정비 완료","overhaul"],
        "serviced":    ["serviced","서비스완료"],
        "repaint":     ["repaint","리페인트","re-paint","black repaint","페인트"],
        "no_serial":   ["no serial","시리얼없음","시리얼 없음","s/n unknown"],
        "not_working": ["not working","작동불량","불량","broken","as-is","asis"],
        "oil_blades":  ["oil on blades","조리개 오일","oily blades"],
        "modified":    ["modified","개조","모디파이"],
    }
    _flagged = []
    for r in unique_results:
        _n = (r.get('상품명','') + ' ' + r.get('컨디션','')).lower()
        _flags = []
        for _flag, _kws in _FLAG_RULES.items():
            if any(_kw in _n for _kw in _kws):
                _flags.append(_flag)
        if _flags:
            _flagged.append({
                "listing_id": r.get("링크",""),
                "source": r.get("site",""),
                "title": r.get("상품명",""),
                "flags": _flags,
                "first_seen": r.get("first_seen",""),
            })
    import json as _json_flags
    with open("data/derived/flags_latest.json", "w", encoding="utf-8") as f:
        _json_flags.dump(_flagged, f, ensure_ascii=False, indent=2)
    print(f"  🚩 플래그 추출 → data/derived/flags_latest.json ({len(_flagged)}개 리스크 매물)")
    # ── sold 품질 분류 ──
    import json as _json_sold
    _sold_quality = []
    try:
        with open("data/sold_items.json", "r", encoding="utf-8") as _f_base:
            _sold_base = _json_sold.load(_f_base)
        _sold_base_links = {s.get("링크","") for s in _sold_base}
        _inline_sold = [
            {**r, "hours_to_sell": 1, "sold_at": r.get("sold_at") or r.get("first_seen","")}
            for r in unique_results
            if r.get("품절") and r.get("가격") and r.get("가격")!="문의요망" and r.get("label")
            and r.get("링크","") not in _sold_base_links
        ]
        _sold_raw = _sold_base + _inline_sold
        for _s in _sold_raw:
            _price = _s.get("가격","")
            _hrs = _s.get("hours_to_sell", None)
            _label = _s.get("label","")
            _category = _s.get("category","")
            if _price and _hrs is not None and _hrs > 0:
                _quality = "sold_confirmed"
                _confidence = "high"
            elif _price and _hrs is not None and _hrs < 0:
                _quality = "sold_likely"
                _confidence = "medium"
            elif _price and _hrs is None:
                _quality = "sold_likely"
                _confidence = "low"
            else:
                _quality = "expired_unknown"
                _confidence = "low"
            _include_in_market = (
                _quality in ["sold_confirmed", "sold_likely"] and
                _category not in ["Accessory"] and
                bool(_label)
            )
            _sold_quality.append({
                "listing_id": _s.get("링크",""),
                "source": _s.get("site",""),
                "title": _s.get("상품명",""),
                "label": _label,
                "mount": _s.get("mount",""),
                "price": _price,
                "currency": _s.get("통화",""),
                "sold_quality": _quality,
                "confidence": _confidence,
                "hours_to_sell": _hrs,
                "include_in_market": _include_in_market,
                "sold_at": _s.get("sold_at",""),
                "sold_fx_krw": _s.get("sold_fx_krw"),
                "sold_at_unknown": bool(_s.get("sold_at_unknown")),
                "listed_est": _listed_est(_s),
            })
        with open("data/derived/sold_quality_latest.json", "w", encoding="utf-8") as f:
            _json_sold.dump(_sold_quality, f, ensure_ascii=False, indent=2)
        _confirmed = sum(1 for s in _sold_quality if s["sold_quality"]=="sold_confirmed")
        _likely = sum(1 for s in _sold_quality if s["sold_quality"]=="sold_likely")
        _unknown = sum(1 for s in _sold_quality if s["sold_quality"]=="expired_unknown")
        print(f"  💰 sold 품질 분류 → confirmed:{_confirmed} likely:{_likely} unknown:{_unknown} (총 {len(_sold_quality)}개)")
    except Exception as _e:
        print(f"  ⚠️ sold 품질 분류 실패: {_e}")
    # ── QA 리포트 생성 ──
    try:
        import json as _json_qa
        import datetime as _dt_qa
        _KST_qa = _dt_qa.timezone(_dt_qa.timedelta(hours=9))
        _qa_time = _dt_qa.datetime.now(_KST_qa).strftime("%Y-%m-%d %H:%M:%S")
        # 기본 통계
        _total = len(unique_results)
        # label 정확도 계산 시 Accessory 제외 (Accessory는 label 없어도 정상)
        _non_acc = [r for r in unique_results if r.get("category") != "Accessory"]
        _no_label = sum(1 for r in _non_acc if not r.get("label"))
        _total_for_accuracy = len(_non_acc)
        _no_mount = sum(1 for r in unique_results if not r.get("mount") or r.get("mount")=="Unknown")
        _no_price = sum(1 for r in unique_results if not r.get("가격"))
        _for_sale = sum(1 for r in unique_results if not r.get("품절"))
        _sold_out = sum(1 for r in unique_results if r.get("품절"))
        # 사이트별
        from collections import Counter as _Counter
        _site_counts = dict(_Counter(r.get("site","") for r in unique_results).most_common())
        _label_counts = dict(_Counter(r.get("label","") for r in unique_results if r.get("label")).most_common(20))
        # 플래그
        try:
            _flags_data = _json_qa.load(open("data/derived/flags_latest.json"))
            _flag_count = len(_flags_data)
            _flag_types = dict(_Counter(f for r in _flags_data for f in r.get("flags",[])).most_common())
        except:
            _flag_count = 0
            _flag_types = {}
        # sold 품질
        try:
            _sq_data = _json_qa.load(open("data/derived/sold_quality_latest.json"))
            _sq_confirmed = sum(1 for s in _sq_data if s["sold_quality"]=="sold_confirmed")
            _sq_likely = sum(1 for s in _sq_data if s["sold_quality"]=="sold_likely")
            _sq_unknown = sum(1 for s in _sq_data if s["sold_quality"]=="expired_unknown")
            _sq_market = sum(1 for s in _sq_data if s.get("include_in_market"))
        except:
            _sq_confirmed = _sq_likely = _sq_unknown = _sq_market = 0
        _qa_report = {
            "generated_at": _qa_time,
            "total_listings": _total,
            "for_sale": _for_sale,
            "sold_out": _sold_out,
            "no_label": _no_label,
            "no_mount": _no_mount,
            "no_price": _no_price,
            "label_accuracy": round((_total_for_accuracy - _no_label) / _total_for_accuracy * 100, 1) if _total_for_accuracy else 0,
            "mount_accuracy": round((_total - _no_mount) / _total * 100, 1) if _total else 0,
            "site_counts": _site_counts,
            "top_labels": _label_counts,
            "flags": {
                "total_flagged": _flag_count,
                "by_type": _flag_types,
            },
            "sold_quality": {
                "confirmed": _sq_confirmed,
                "likely": _sq_likely,
                "unknown": _sq_unknown,
                "market_eligible": _sq_market,
            },
        }
        with open("data/derived/qa_report_latest.json", "w", encoding="utf-8") as f:
            _json_qa.dump(_qa_report, f, ensure_ascii=False, indent=2)
        print(f"  📊 QA 리포트 → label정확도:{_qa_report['label_accuracy']}% mount정확도:{_qa_report['mount_accuracy']}%")
    except Exception as _e:
        print(f"  ⚠️ QA 리포트 실패: {_e}")
    # ── 시세 엔진 실행 ──
    # python3 app/test.py 로 실행하면 app/ 가 sys.path 첫 칸이라 'import app'이 app/app.py(flask)로 잡힌다 → 파일 경로로 불러옴
    try:
        import importlib.util as _ilu
        _spec = _ilu.spec_from_file_location("price_engine", os.path.join(os.path.dirname(os.path.abspath(__file__)), "services", "price_engine.py"))
        _pe = _ilu.module_from_spec(_spec)
        _spec.loader.exec_module(_pe)
        _pe.save_market_prices("data/derived/market_prices.json")
    except Exception as _e_pe:
        print(f"  ⚠️ 시세 엔진 실패: {_e_pe}")
    # ── crawl_sessions.json 누적 저장 ──
    end_time = ce.now_kst()
    new_listings = [
        {"상품명": e.get("title"), "site": e.get("site"), "가격": e.get("price"), "통화": e.get("currency", ""), "링크": e.get("link")}
        for e in all_events if e["type"] == "new"
    ]
    from collections import Counter as _Counter2
    session_entry = {
        "start_time": crawl_time,
        "end_time": end_time,
        "seconds": round(elapsed, 1),
        "new_items": len(new_listings),
        "total_items": len(unique_results),
        "site_counts": dict(_Counter2(r['site'] for r in unique_results)),
        "events": dict(_Counter2(e["type"] for e in all_events)),
        "sources": site_stats,
        "new_listings": new_listings,
    }
    try:
        with open("crawler/sessions/crawl_sessions.json", "r", encoding="utf-8") as f:
            sessions_log = json.load(f)
    except (OSError, ValueError):
        sessions_log = []
    sessions_log = [x for x in sessions_log if x.get("start_time") != crawl_time]
    sessions_log.append(session_entry)
    sessions_log = sessions_log[-100:]
    with open("crawler/sessions/crawl_sessions.json", "w", encoding="utf-8") as f:
        json.dump(sessions_log, f, ensure_ascii=False, indent=2)

    write_status(100, "완료", len(unique_results), len(sources), 0)
    print(f"\n{'='*50}")
    print(f"✅ 최종 {len(unique_results)}개 → results.json 저장 완료")
    print(f"🆕 신규 {len(new_listings)} · 변경 {len(all_events)}건 · 수집 {elapsed:.1f}초")
    for st in site_stats:
        print(f"   {st['site']}: {st['status']} · {st.get('coverage')} · {st.get('pages') or '-'}페이지 · {st.get('seconds') or 0}초")
    print(f"{'='*50}")

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
        ["git", "add", "--ignore-errors", "data/raw/results.json", "index.html", "admin.html", "data/sold_items.json"],
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
