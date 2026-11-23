"""액세서리 모델 (후드·필터·Visoflex·접사·삼각대·플래시·파인더 등) — 주문 번호 하나가 모델 하나.

2026-11-14 사장님: "액세서리도 모델이 있어야 엉뚱하게 분류되지 않음"(camera-bridge/할일.md '액세서리 모델 만들기' 1차).
그때 카탈로그 JSON에 바로 들어갔던 43개를 2026-11-23 코드로 옮김 — 원본은 코드 하나, JSON은 build_entity_catalog.py 결과
(camera-bridge/분류설계.md ⑤, tests/test_catalog_matches_source.py).

새 액세서리 모델은 아래 표에 한 줄 더하고 `python3 catalog/build_entity_catalog.py`.
  (id 꼬리, 영어 이름, 한국어 이름, 주문 번호 5자리, 라이트 코드 이름(없으면 None), 검색 별칭)
"""
from __future__ import annotations

# 렌즈 이름이 먼저 나오는 제목(렌즈 매물)은 액세서리 모델에 붙이지 않음. 후드·필터 등 액세서리 단어가 먼저 나오면 통과
LENS_FIRST = (r"^(?:(?!hood|filter|adapter|adattat|mount|ring|cap\b|tube|フード|후드|필터|bague|griff|grip|finder|sucher|tripod|三脚|strap|flash|carrier).)*"
              r"(summicron|summilux|elmarit|\belmar\b|telyt|hektor|angulon|noctilux|summaron|summarit|\bapo\b)")

ROWS = [
    ('hood:12575', 'Lens hood 12575 IUFOO (90mm f/2.8–4 · 135mm f/4)', '렌즈 후드 12575 (90·135mm)', '12575', 'IUFOO', ['12575 hood', 'iufoo']),
    ('hood:12585', 'Lens hood 12585 (35/50mm)', '렌즈 후드 12585 (35·50mm)', '12585', None, ['12585 hood', '12585h']),
    ('hood:12504', 'Lens hood 12504 (35mm f/1.4–2)', '렌즈 후드 12504 (35mm)', '12504', None, ['12504 hood']),
    ('hood:12538', 'Lens hood 12538 (Summicron-M 50mm f/2)', '렌즈 후드 12538 (주미크론 50)', '12538', None, ['12538 hood']),
    ('hood:12571', 'Lens hood 12571', '렌즈 후드 12571', '12571', None, ['12571 hood', '12571j']),
    ('hood:12586', 'Lens hood 12586 (Summilux-M 50mm f/1.4)', '렌즈 후드 12586 (주미룩스 50)', '12586', None, ['12586 hood']),
    ('hood:12564', 'Lens hood 12564 (R 35mm f/2.8 · 50mm f/2)', '렌즈 후드 12564 (R 35·50mm)', '12564', None, ['12564 hood']),
    ('hood:12501', 'Lens hood 12501 (21mm f/3.4 · 28mm f/2.8)', '렌즈 후드 12501 (21·28mm)', '12501', None, ['12501 hood']),
    ('hood:12521', 'Lens hood 12521 XOOIM', '렌즈 후드 12521 (XOOIM)', '12521', 'XOOIM', ['12521 hood', 'xooim']),
    ('hood:12524', 'Lens hood 12524 (35mm f/2)', '렌즈 후드 12524 (35mm)', '12524', None, ['12524 hood']),
    ('hood:12529', 'Lens hood 12529 (Elmarit-R 19mm 1st)', '렌즈 후드 12529 (엘마릿 R 19)', '12529', None, ['12529 hood']),
    ('hood:12523', 'Lens hood 12523 (Elmarit-R 24mm)', '렌즈 후드 12523 (엘마릿 R 24)', '12523', None, ['12523 hood']),
    ('hood:12509', 'Lens hood 12509 (R 28/35mm)', '렌즈 후드 12509 (R 28·35mm)', '12509', None, ['12509 hood']),
    ('hood-cap:14033', 'Hood cap 14033 (42mm)', '후드 캡 14033 (42mm)', '14033', None, ['14033 cap']),
    ('filter:13373', 'Filter E55 UVa 13373', '필터 E55 UVa 13373', '13373', None, ['e55 uva', '13373 filter']),
    ('filter:13131', 'Filter E39 UVa 13131', '필터 E39 UVa 13131', '13131', None, ['e39 uva', '13131 filter']),
    ('filter:13004', 'Filter E46 UVa 13004', '필터 E46 UVa 13004', '13004', None, ['e46 uva', '13004 filter']),
    ('filter:13381', 'Filter E60 UVa 13381', '필터 E60 UVa 13381', '13381', None, ['e60 uva', '13381 filter']),
    ('filter:13386', 'Filter E67 UVa 13386', '필터 E67 UVa 13386', '13386', None, ['e67 uva', '13386 filter']),
    ('filter:13411', 'Filter E46 UV/IR 13411', '필터 E46 UV/IR 13411', '13411', None, ['e46 uv/ir', '13411 filter']),
    ('filter:13413', 'Filter E55 UV/IR 13413', '필터 E55 UV/IR 13413', '13413', None, ['e55 uv/ir', '13413 filter']),
    ('filter:13035', 'Filter E49 UVa II 13035', '필터 E49 UVa II 13035', '13035', None, ['e49 uva', '13035 filter']),
    ('filter:13352', 'Polarizing filter 13352', '편광 필터 13352', '13352', None, ['13352 polarizer']),
    ('filter-ring:14161', 'Series VII filter ring 14161', '시리즈 VII 필터 링 14161', '14161', None, ['series 7 ring', '14161 ring']),
    ('filter-ring:14160', 'Series VI filter ring 14160', '시리즈 VI 필터 링 14160', '14160', None, ['series 6 ring', '14160 ring']),
    ('visoflex:typ-020', 'Visoflex (Typ 020) electronic viewfinder 18767', '비조플렉스 (Typ 020) 18767', '18767', None, ['visoflex typ 020', 'visoflex 020', '18767 visoflex']),
    ('adapter:m-adapter-t', 'M-Adapter T/L 18771', 'M 어댑터 T/L 18771', '18771', None, ['m-adapter t', 'm-adapter l', '18771 adapter']),
    ('visoflex-adapter:16466', 'Visoflex adapter 16466 OUBIO', '비조플렉스 어댑터 16466 (OUBIO)', '16466', 'OUBIO', ['oubio', '16466 adapter']),
    ('visoflex-mount:16464', 'Universal focusing mount 16464 OTZFO', '유니버설 초점 마운트 16464 (OTZFO)', '16464', 'OTZFO', ['otzfo', '16464 mount']),
    ('visoflex-tube:16471', 'Visoflex extension tube 16471', '비조플렉스 접사 링 16471', '16471', 'OTRPO', ['16471 tube']),
    ('visoflex-mount:16462', 'Focusing mount 16462 (90mm f/2 · 135mm f/2.8 heads)', '초점 마운트 16462 (90·135mm 헤드)', '16462', None, ['16462 mount']),
    ('adapter:14127', 'Adapter 14127 (Visoflex / R)', '어댑터 14127', '14127', None, ['14127 adapter']),
    ('macro:14198', 'Macro-Adapter-R 14198', '매크로 어댑터 R 14198', '14198', None, ['macro-adapter-r 14198']),
    ('macro:14256', 'Macro-Adapter-R 14256', '매크로 어댑터 R 14256', '14256', None, ['macro-adapter-r 14256']),
    ('macro:14135', 'Extension tube R 14135', '접사 링 R 14135', '14135', None, ['14135 tube']),
    ('macro:14158', 'Extension tubes R 14158', '접사 링 R 14158', '14158', None, ['14158 tube']),
    ('macro:16531', 'ELPRO VIa close-up lens 16531', '엘프로 VIa 16531', '16531', None, ['elpro via', '16531 elpro']),
    ('tripod:14100', 'Table tripod 14100', '탁상 삼각대 14100', '14100', None, ['table tripod', '14100 tripod']),
    ('ball-head:14110', 'Ball head 14110', '볼 헤드 14110', '14110', None, ['ball head 14110']),
    ('lens-carrier:14404', 'M lens carrier 14404', 'M 렌즈 캐리어 14404', '14404', None, ['lens carrier 14404']),
    ('strap:14253', 'Neck strap 14253', '넥 스트랩 14253', '14253', None, ['14253 strap']),
    ('flash:sf20', 'SF 20 flash 14414', 'SF 20 플래시 14414', '14414', None, ['sf 20', 'sf20']),
    ('finder:12019', '24mm viewfinder 12019', '24mm 파인더 12019', '12019', None, ['24mm finder 12019']),
]

MODELS: dict[str, dict] = {}
ALIASES: dict[str, list[str]] = {}
NAME_KO: dict[str, str] = {}
PARENTS: dict[str, tuple] = {}
CODES: dict[str, list[str]] = {}
CODE_WORDS: dict[str, list[str]] = {}

for _tail, _name, _ko, _code, _word, _aliases in ROWS:
    _key = f"leica:acc:{_tail}"
    _must = rf"(?<![\d.,/]){_code}[A-Z]?(?!\d)" + (rf"|\b{_word.lower()}\b" if _word else "")
    MODELS[_key] = {"model_key": _key, "display_name": _name, "category": "Accessory", "mount": None,
                    "title_must": [_must], "title_must_not": [LENS_FIRST]}
    ALIASES[_key] = list(_aliases)
    NAME_KO[_key] = _ko
    CODES[_key] = [_code]
    if _word:
        CODE_WORDS[_key] = [_word]
