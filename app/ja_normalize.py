"""일본 중고 사이트 상품명(일본어 섞인 표기) → 영어 표기.

기타무라에서 시작했고, 맵카메라·후지야 등 일본 사이트가 늘어나면 같이 쓴다.
목표: 엔티티 매칭 규칙(카탈로그)이 읽을 수 있는 'Summicron-M 50mm f2.0' 같은 꼴.
"""
import re as _re

# 일본어 → 영어 변환 매핑
JA_TO_EN = {
    # 렌즈명
    'ズミルックス': 'Summilux', 'ズミクロン': 'Summicron', 'ノクティルックス': 'Noctilux',
    'ズマリット': 'Summarit', 'エルマー': 'Elmar', 'エルマリート': 'Elmarit',
    'スーパーアンギュロン': 'Super-Angulon', 'テレエルマー': 'Tele-Elmar',
    'アポズミクロン': 'APO-Summicron', 'ズマロン': 'Summaron',
    'ヘクトール': 'Hektor', 'ズマール': 'Summar', 'エルカン': 'Elcan',
    'トリエルマー': 'Tri-Elmar', 'バリオエルマー': 'Vario-Elmar',
    'バリオエルマリート': 'Vario-Elmarit', 'アポテリート': 'APO-Telyt',
    'スーパーエルマー': 'Super-Elmar', 'テリート': 'Telyt',
    'ズミター': 'Summitar', 'ヘクター': 'Hektor',
    # 브랜드/기기명
    'ライカ': 'Leica', 'ライカビット': 'Leicavit', 'ライカフード': 'Leica Hood',
    'ライカファインダー': 'Leica Finder', 'レンズフード': 'Lens Hood',
    # 카테고리 (제거)
    'ミラーレス一眼': '', '交換レンズ': '', 'カメラ用品': '',
    'フィルムカメラ': '', '中古': '', '新品': 'New',
    # 색상
    'ブラック': 'Black', 'シルバー': 'Silver', 'クローム': 'Chrome',
    'ゴールド': 'Gold', 'チタン': 'Titan', 'グリーン': 'Green',
    'レッド': 'Red', 'ホワイト': 'White', 'ブルー': 'Blue',
    # 상태/소재
    'ブラックペイント': 'Black Paint', 'ペイント': 'Paint',
    'アルミ': 'Aluminium', '状態': '', 'ボディ': 'Body',
    # 특수 에디션
    'エルメスエディション': 'Hermes Edition', 'エルメス': 'Hermes',
    'グロッシー': 'Glossy', 'ノクチ': 'Nocti', 'ビット': 'Vit',
    'メーター': 'Meter', 'アポ': 'APO', 'アポ·': 'APO-',
    'ファインダー': 'Finder', 'フード': 'Hood',
    'レンズフード': 'Lens Hood', 'ライカフード': 'Leica Hood',
    'ライカファインダー': 'Leica Finder', 'ライカビット': 'Leicavit',
    'ライカMRメーター': 'Leica MR Meter',
    'オリジナル': 'Original', 'プロトタイプ': 'Prototype',
    'オリジナル': 'Original', 'スペシャルエディション': 'Special Edition',
    # 시기
    '初期': 'Early', '後期': 'Late', '前期': 'Early',
    # 악세사리
    'フード': 'Hood', 'アダプター': 'Adapter', 'ファインダー': 'Finder',
    'ケース': 'Case', 'ストラップ': 'Strap', 'キャップ': 'Cap',
    'フィルター': 'Filter', 'グリップ': 'Grip', 'バッテリー': 'Battery',
    # 기타
    'アポ': 'APO', 'セット': 'Set', 'プロトタイプ': 'Prototype',
    'ミリ': 'mm', 'レンズ': 'Lens',
}

# 사전보다 먼저 바꿔야 하는 표기 (긴 말이 짧은 말에 먹히지 않게)
JA_PRE = {
    'モノクローム': 'Monochrom', 'ノクチルックス': 'Noctilux',
    'アンギュロン': 'Angulon', '沈胴': 'Collapsible', '固定': 'Rigid',
    'アポ-': 'APO-', 'バリオ-': 'Vario-', 'スーパー-': 'Super-',
    'トリ-': 'Tri-', 'テレ-': 'Tele-',
    'ライカビット': 'Leicavit', 'ワインダー': 'Winder',
    'ヘクトール': 'Hektor', 'ヘクト': 'Hektor',
}
LENS_NAMES = ('APO-Summicron|Vario-Elmarit|Vario-Elmar|Super-Elmar|Tri-Elmar|Tele-Elmarit|'
              'Tele-Elmar|Super-Angulon|Summicron|Summilux|Summarit|Summaron|Elmarit|Elmar|'
              'Noctilux|Hektor|Thambar')

# 사전보다 먼저: 붙어 쓴 접두어·수식어 (긴 말이 짧은 말에 먹히지 않게)
JA_PRE.update({
    'スーパー': 'Super-', 'トリ': 'Tri-', 'バリオ': 'Vario-', 'テレ': 'Tele-', 'マクロ': 'Macro-',
    'ホロゴン': 'Hologon', 'ヘクトール': 'Hektor', 'タンバール': 'Thambar', 'ズマレックス': 'Summarex',
    'ニッケル': 'Nickel ', '赤': 'Red ', '新': 'New ', '旧': 'Old ', '限定': ' Limited', '連番': ' Serial ',
    'マウンテン': 'Mountain', 'モーターなし': '', 'モーター付': ' Motor', 'ハンマートーン': ' Hammertone',
    'レザープロテクター': ' Leather Protector', 'プロテクター': ' Protector', '接写装置': ' Close-up Device',
    'フォーカスリング': ' Focus Ring', 'バヨネット': ' Bayonet', 'リング': ' Ring',
    '用': ' for ',  # 'D-LUX7用' = D-LUX7용 (액세서리)
})
LENS_NAMES = ('APO-Summicron|Vario-Elmarit|Vario-Elmar|Super-Elmar|Tri-Elmar|Tele-Elmarit|'
              'Tele-Elmar|Super-Angulon|Summicron|Summilux|Summarit|Summaron|Elmarit|Elmar|'
              'Noctilux|Hektor|Thambar|Hologon|Angulon')


def ja_to_en(text: str) -> str:
    text = text.replace('・', '-').replace('（', '(').replace('）', ')')
    for ja, en in JA_PRE.items():
        text = text.replace(ja, en)
    for ja, en in JA_TO_EN.items():
        text = text.replace(ja, en)
    text = text.replace('Super--', 'Super-').replace('Tri--', 'Tri-').replace('Vario--', 'Vario-')
    # 3代目 → 3rd
    text = _re.sub(r'(\d)代目', lambda m: m.group(1) + {'1': 'st', '2': 'nd', '3': 'rd'}.get(m.group(1), 'th'), text)
    # SummicronT / AngulonR / ElmarM28-35-50 → Summicron-T, Angulon-R, Elmar-M 28-35-50
    text = _re.sub(rf'({LENS_NAMES})(SL|TL|M|R|L|S|T)(?=\b|\d)', r'\1-\2 ', text)
    # T 시스템 렌즈는 2016년에 TL로 이름이 바뀜 (Summicron-T 23 = Summicron-TL 23)
    text = _re.sub(rf'({LENS_NAMES})-T\b', r'\1-TL', text)
    # 'f2.0/50mm', '1.4/35mm', 'f3.5-5.6/18-56mm' → '50mm f2.0' (초점거리가 '/' 뒤에 오면 매칭 규칙이 못 읽음)
    text = _re.sub(r'\b[fF]?(\d+(?:\.\d+)?(?:-\d+(?:\.\d+)?)?)\s*/\s*(\d+(?:-\d+)*)\s*mm\b', r'\2mm f\1', text)
    # 'M28-35-50mm' 처럼 마운트 글자와 초점거리가 붙은 것
    text = _re.sub(r'\b(SL|TL|M|R|L|S|T)(\d{2,3}(?:-\d{2,3})*mm)', r'\1 \2', text)
    # 'M-ATyp127' → 'M-A Typ 127'
    text = _re.sub(r'(?<=[A-Za-z0-9])Typ\s?(\d{3})', r' Typ \1', text)
    # F2 → F2.0 (조리개 인식용)
    text = _re.sub(r'\bF(\d+)(?![\d.])', r'F\1.0', text)
    # LeicaDII → Leica DII, 'Leica Leica' 중복 제거
    text = _re.sub(r'Leica(?=[A-Z0-9])', 'Leica ', text)
    text = _re.sub(r'\bLeica\s+Leica', 'Leica', text)
    text = text.replace('Leica Vit', 'Leicavit')
    # 일본식 바르낙 이름: DII = II(D형), DIII = III(F형), A = I(A형)
    text = _re.sub(r'\bLeica DIII\b', 'Leica III', text)
    text = _re.sub(r'\bLeica DII\b', 'Leica II (D)', text)
    text = _re.sub(r'\bLeica A (?=\d{2}mm)', 'Leica I (A) ', text)
    return _re.sub(r'\s+', ' ', text).strip()
