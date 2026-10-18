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
PRICE_SYMBOL_TO_KRW = {'¥': 9, '£': 1800, '€': 1500, 'A$': 880, '$': 1350, 'CHF': 1650, 'DKK': 200, 'MYR': 300}

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
                "site": "Leica Store Heidelberg (독일)",
                "label": auto_label(name),
                "상품명": name,
                "세대": detect_generation(name),
                "컨디션": cond,
                "가격": price,
                "통화": "EUR",
                "이미지": img,
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
        try:
            resp = sess.get(f"{base}/wp-json/wc/store/v1/products",
                            params={"search": "leica", "per_page": 100, "page": page_num}, timeout=60)
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
                "category": cat_,
                "brand": detect_brand(name),
            })
        time.sleep(2)
    print(f"  ✅ fotohandel.de 완료: {len(results)}개")
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
                "category": cat,
                "brand": detect_brand(name),
            })
        time.sleep(random.uniform(1.0, 2.0))
    print(f"  ✅ Leica Store Heidelberg 완료: {len(results)}개")
                "category": cat,
                "brand": detect_brand(name),
            })
        if len(products) < 100:
            break
        time.sleep(2)
    print(f"  ✅ Vibe.pl 완료: {len(results)}개")
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
    "Ffordes (영국)": 6,
    "Lucky Camera (일본)": 12,  # 목록 30쪽 + 새 매물 상세
    "Tamarkin Camera (미국)": 6,  # 카드마다 상세 (약 170개)
    "Foto Köster (독일)": 6,  # 매물마다 상세 (약 40개)
    "Calumet (독일)": 6,  # 상품 화면 120개쯤 (4~5분)
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
        ("Vibe.pl (폴란드)", lambda: ce.wrap_full_run("Vibe.pl (폴란드)", crawl_vibe)),
        ("Foto Köster (독일)", lambda: ce.wrap_full_run("Foto Köster (독일)", crawl_koester)),
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
