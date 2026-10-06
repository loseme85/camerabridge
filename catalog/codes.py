"""라이카 제품 번호(주문 번호, 5자리) → 엔티티.

구매자가 "11873"처럼 제품 번호로 검색하면 그 모델이 나오게 하고, 제목에 모델명 없이 번호만 적힌 매물도 모델에 연결한다.
(2026-10-04 레딧 r/Leica 피드백: "11873으로 검색하면 아무것도 안 나온다")

넣는 기준: 틀린 번호를 넣느니 안 넣는다.
  - 딜러 매물 제목에 모델명과 함께 적힌 번호(Ffordes·Kamerastore 등) 중 모델이 분명한 것
  - 라이카 공식 중고 매장(classic.leica-camera.com)·딜러 상품명으로 확인한 현행 바디 번호
  - 세대가 여럿인데 같은 번호를 쓴 것(예: 11870 주미룩스 35 1·2세대)은 부모 엔티티에 붙인다
  - 같은 번호가 서로 다른 렌즈에 쓰인 것(예: 11063 Telyt 200/4·20cm/4.5)은 넣지 않는다
"""
from __future__ import annotations

L = "leica:lens:"
B = "leica:body:"

CODES: dict[str, list[str]] = {
    # ── M 렌즈: 주미룩스 ──
    L + "summilux-m:35:aa": ["11873"],
    L + "summilux-m:35:asph-1994": ["11874"],
    L + "summilux-m:35:asph-fle": ["11663"],
    L + "summilux-m:35:titan": ["11859"],
    L + "summilux-m:35:v1-steel-rim": ["11869"],
    L + "summilux-m:35:leitz-wetzlar": ["11700"],
    L + "summilux-m:35": ["11870", "11871"],  # pre-ASPH 1·2세대가 같은 번호
    L + "summilux-m:50": ["11114"],  # 1·2세대가 같은 번호
    L + "summilux-m:50:asph": ["11891", "11728"],
    L + "summilux-m:50:asph-safari": ["11736"],
    L + "summilux-m:28": ["11668"],
    # ── 주미크론 ──
    L + "summicron-m:35:asph": ["11879"],
    L + "summicron-m:35:v1-eyes": ["11108"],
    L + "summicron-m:35:v1-8element": ["11308"],
    L + "summicron-m:35": ["11309"],  # 2·3세대가 같은 번호
    L + "summicron-m:35:v4": ["11310", "11311"],
    L + "summicron:50:v3": ["11817"],
    L + "summicron-m:50:current": ["11819", "11816", "11826"],
    L + "summicron:50:50-jahre": ["11615"],
    L + "summicron-m:28:asph": ["11672"],
    L + "summicron-m:90": ["11122", "11136"],
    L + "apo-summicron-m:90": ["11884"],
    L + "apo-summicron-m:75": ["11637"],
    L + "summicron-c:40": ["11542"],
    # ── 녹티룩스 ──
    L + "noctilux-m:50:f0.95": ["11602"],
    L + "noctilux-m:50:f1.0": ["11821"],  # 여러 세대가 같은 번호
    # ── 엘마리트·엘마·기타 M ──
    L + "elmarit-m:28:v2": ["11802"],
    L + "elmarit-m:28:v3": ["11804"],
    L + "elmarit-m:28:v4": ["11809"],
    L + "elmarit-m:28:asph": ["11606"],
    L + "elmarit-m:24:asph": ["11878"],
    L + "elmarit-m:21": ["11134"],
    L + "elmarit-m:90": ["11807", "11808"],
    L + "elmarit-m:90:v1": ["11129"],
    L + "tele-elmarit-m:90": ["11800"],  # 굵은·얇은 버전이 같은 번호
    L + "elmarit-m:135": ["11827", "11829"],
    L + "elmar-m:50:f2.8": ["11831"],
    L + "elmar:50:f3.5": ["11110", "11610"],
    L + "elmar:90": ["11830", "11130"],
    L + "elmar:90:collapsible": ["11131", "11631"],
    L + "elmar:135": ["11850"],
    L + "elmar-c:90": ["11540"],
    L + "summaron:35:f2.8": ["11306"],
    L + "summaron-m:28:f5.6:reissue": ["11695"],
    L + "summarit-m:35:f2.5": ["11643"],
    L + "summarit-m:50:f2.5": ["11644"],
    L + "summarit-m:75:f2.5": ["11645"],
    L + "summarit-m:90:f2.5": ["11646"],
    L + "summarit-m:90:f2.4": ["11685"],
    L + "super-elmar-m:21": ["11145"],
    L + "super-angulon:21:f3.4": ["11103"],
    L + "tri-elmar-m:16-18-21": ["11626", "11642"],
    L + "hektor:125": ["11032", "11532"],
    L + "hektor:135": ["11135"],
    L + "telyt:visoflex": ["11912", "11914"],
    # ── SL·TL ──
    L + "apo-summicron-sl:21": ["11181"],
    L + "apo-summicron-sl:35": ["11184"],
    L + "apo-summicron-sl:75": ["11178"],
    L + "summicron-sl:50": ["11193"],
    L + "vario-elmarit-sl:24-70": ["11189"],
    L + "vario-elmarit-sl:28-70": ["11196"],
    L + "vario-elmarit-sl:70-200": ["11096"],
    L + "vario-elmar-tl:18-56": ["11080"],
    L + "apo-vario-elmar-tl:55-135": ["11083"],
    # ── R ──
    L + "elmarit-r:19": ["11258"],
    L + "elmarit-r:24": ["11221", "11331"],
    L + "elmarit-r:28": ["11204", "11333"],
    L + "elmarit-r:35": ["11101", "11231"],
    L + "elmarit-r:90": ["11239", "11806"],
    L + "elmarit-r:135": ["11111", "11211"],
    L + "elmarit-r:180": ["11919"],
    L + "summicron-r:35": ["11115"],
    L + "summicron-r:50": ["11215", "11216", "11228"],
    L + "summicron-r:90": ["11219", "11254"],
    L + "summilux-r:50": ["11776", "11777"],
    L + "summilux-r:80": ["11881"],
    L + "macro-elmarit-r:60": ["11205"],
    L + "apo-macro-elmarit-r:100": ["11210"],
    L + "apo-telyt-r:180": ["11240", "11242"],
    L + "apo-elmarit-r:180": ["11273"],
    L + "apo-summicron-r:180": ["11354"],
    L + "fisheye-elmarit-r:16": ["11222"],
    L + "super-angulon-r:21": ["11813"],
    L + "vario-elmar-r:28-70": ["11265", "11364"],
    L + "vario-elmar-r:35-70": ["11244"],
    L + "vario-elmar-r:70-210": ["11246"],
    L + "vario-elmar-r:80-200": ["11281"],
    L + "telyt-r:long": ["11915", "11920", "11960"],
    # ── 필름 바디 ──
    B + "m3": ["10150"],
    B + "m2": ["10300", "10308"],
    B + "m4:standard": ["10400"],
    B + "m4:black-paint": ["10402"],
    B + "m4-2:standard": ["10410"],
    B + "m5:standard": ["10502"],
    B + "m6:classic": ["10404", "10414"],
    B + "m6:ttl": ["10433"],
    B + "m6:reissue": ["10557"],
    B + "m7:standard": ["10505"],
    B + "mp-film": ["10302"],
    B + "m-a": ["10370"],
    B + "leicaflex": ["10001"],
    B + "leicaflex-sl": ["10011"],
    B + "r4": ["10043"],
    B + "r7": ["10067"],
    # ── 디지털 바디 ──
    B + "m8:standard": ["10701", "10702"],
    B + "m9:standard": ["10704"],
    B + "m-e": ["10759"],
    B + "m-monochrom-ccd": ["10760"],
    B + "m240:standard": ["10770"],
    B + "m10:standard": ["20000", "20001"],
    B + "m10-p:standard": ["20021"],
    B + "m10-r:standard": ["20002"],
    B + "m11:standard": ["20200"],
    B + "m11-p:standard": ["20211", "20214"],
    B + "q2:standard": ["19050"],
    B + "q3": ["19080"],
    B + "sl2-s:standard": ["10880"],
    B + "sl3:standard": ["10607", "10608"],
    B + "sl3-s": ["10644"],
    B + "sl3:reporter": ["10662"],
}
