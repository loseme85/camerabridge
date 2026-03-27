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
parser.add_argument('--site', type=str, help='특정 사이트만 크롤링 (예: 사진집)')
args, _ = parser.parse_known_args()
MOCK_MODE = args.mock
SITE_FILTER = args.site

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
    {"label": "21mm Summilux ASPH",      "keywords": ["Summilux 21", "21mm Summilux", "Summilux-M 21", "21/1.4"],   "must_contain": ["summilux", "21"]},
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
    {"label": "Leica C2",           "keywords": ["Leica C2", "C2 Zoom", "C2-Zoom", "c2 zoom black"], "must_contain": ["c2"]},
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
# 유틸 함수
# ══════════════════════════════════════════════════════
def detect_mount(name):
    """마운트 타입 자동 분류 - 이중 마운트(LTM) 지원"""
    n = name.upper()

    # R-mount (가장 먼저 - -R 표기가 명확)
    if any(x in n for x in ['-R ','-R/','SUMMILUX-R','SUMMICRON-R','ELMARIT-R',
                              'ELMAR-R','TELYT-R','LEICA R3','LEICA R4','LEICA R5',
                              'LEICA R6','LEICA R7','LEICA R8','LEICA R9']):
        return "R"

    # L-mount (SL/Q/S)
    if any(x in n for x in ['SL2',' SL ','VARIO-ELMARIT-SL','L-MOUNT','LEICA Q',
                              'LEICA SL','Q2 ','Q3 ',' Q2',' Q3']):
        return "L"

    # LTM/M39 - 이중 마운트 (M과 LTM 양쪽)
    # Summar/Summarit (구형, f1.5/f2.0) → LTM
    # SUMMARIT-M → M-mount (별도 처리)
    ltm_kw = ['LTM','L39','M39','SCREW','나사',
               'LEICA I ','LEICA IIF','LEICA IF',
               'LEICA IIA','LEICA IIB','LEICA IIC',
               'LEICA IIIA','LEICA IIIB','LEICA IIIC','LEICA IIIF','LEICA IIIG',
               '3.5CM','7.3CM','9CM ','13.5CM',
               'LEITZ WETZLAR','ERNST LEITZ']
    # Summar/Summarit (구형 나사마운트) - SUMMARIT-M 제외
    if 'SUMMAR' in n and 'SUMMARIT-M' not in n and 'SUMMARON' not in n:
        return "LTM"
    if any(x in n for x in ltm_kw):
        return "LTM"

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

    return "Unknown"

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
        ' R7', ' R8', ' R9', 'LEICA R3', 'LEICA R4', 'LEICA R5', 'LEICA R6', 'LEICA R7', 'LEICA R8', 'LEICA R9', '-R SN', '-R ('
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

# 비라이카 브랜드 키워드 (바디 검색 시 제외)
NON_LEICA = ['nikon', 'canon', 'sony', 'fuji', 'olympus', 'panasonic', 'hasselblad',
             'pentax', 'minolta', 'contax', '니콘', '소니', '캐논', '후지']

def passes_filter(name, must_contain, item_meta=None):
    """향상된 필터 - 카테고리별 상호 배타적 필터링"""
    name_lower = " ".join(name.lower().split())

    # 바디 검색 시 비라이카 브랜드 제외
    item_cat = item_meta.get("category", "") if item_meta else ""
    if item_cat == "Body":
        if any(kw in name_lower for kw in NON_LEICA):
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

]

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
            if "[중고]" not in name and "[위탁]" not in name:
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
            if route.request.resource_type in ["stylesheet", "font", "image", "media"]:
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

        for search_item in SEARCH_ITEMS:
            label = search_item["label"]
            must_contain = search_item["must_contain"]
            keywords = search_item["keywords"]
            item_meta = search_item  # category, barnack 등 메타 전달
            print(f"\n  🔍 필터: '{label}'")

            seen_in_item = set()
            for keyword in keywords:
                try:
                    if site["type"] == "cafe24":
                        res = crawl_cafe24(page, site, keyword, label, must_contain, item_meta)
                    elif site["type"] == "cafe24_all":
                        res = crawl_cafe24_all(page, site, keyword, label, must_contain, item_meta)
                    elif site["type"] == "godo":
                        res = crawl_godo(page, site, keyword, label, must_contain, item_meta)
                    elif site["type"] == "ffordes_search":
                        res = crawl_ffordes_search(page, site, keyword, label, must_contain, item_meta)
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
                time.sleep(0.3)

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

    # 억불카메라(godo)는 별도 순차 처리 (headless=False 필요)
    # 특정 사이트만 크롤링 (--site 옵션)
    active_sites = SITES
    if SITE_FILTER:
        active_sites = [s for s in SITES if SITE_FILTER in s["name"]]
        print(f"🎯 사이트 필터: {SITE_FILTER} ({len(active_sites)}개)")
    parallel_sites = [s for s in active_sites if s["type"] != "godo"]
    godo_sites = [s for s in active_sites if s["type"] == "godo"]

    print(f"🚀 병렬 크롤링 시작 ({len(parallel_sites)}개 사이트 동시 처리)")
    print(f"⏳ 억불카메라 ({len(godo_sites)}개)는 별도 처리")

    total_sites = len(parallel_sites) + len(godo_sites)
    done_sites = 0

    # 병렬 처리
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
            eta = int(elapsed / done_sites * (total_sites - done_sites))
            write_status(int(done_sites/total_sites*100), site['name'], len(all_results), done_sites, eta)

    # 억불카메라 순차 처리
    for site in godo_sites:
        results = crawl_site(site)
        all_results.extend(results)
        done_sites += 1
        write_status(int(done_sites/total_sites*100), site['name'], len(all_results), done_sites, 0)

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
    crawl_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    for r in unique_results:
        name = r['상품명']
        # 상품명에서 "상품명 :" 제거
        if name.startswith('상품명') and ':' in name:
            name = name.split(':', 1)[-1].strip()
            r['상품명'] = name
        name_lower = name.lower()
        # system/category 분류
        r['system'] = detect_system(r['상품명'])
        r['category'] = detect_category(r['상품명'], r.get('가격', ''))
        if r['category'] == 'Accessory':
            r['system'] = 'Accessory'
            r['label'] = ''  # Accessory는 label 제거 (평균가 왜곡 방지)
        r['mount'] = detect_mount(r['상품명'])
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

    # 신규 매물 통계
    new_count = sum(1 for r in unique_results if r.get('first_seen') == crawl_time)
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
    push_to_github()
