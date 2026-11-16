"""모델 사양표 v1 (2026-11-16 시작) — 대화창·모델 페이지·비교 페이지가 함께 쓰는 사양.

2026-11-16 사장님: "SL과 SL2 차이", "M6와 M6 TTL 차이", "M 50mm 1.4 최단거리" 같은 질문에
떠 있는 대화창이 답하게 하려면 사양표가 먼저. 사이트는 질문 때마다 찾아보지 않고 이 표에서만 답한다.

규칙
- 키는 엔티티 ID (data/config/entity_catalog_v1.json). 부모에 적으면 아래 버전이 물려받고,
  버전에 적은 값이 부모 값을 덮는다 (spec_for). 사양이 다른 버전(M6 TTL, Summilux 50 ASPH II 등)만 따로 적는다.
- 부모가 없거나 부모가 다른데 바탕이 같은 모델(M10-R ← M10, ASPH 한정판 ← ASPH)은 BASED_ON으로 이어 준다.
- 물려받으면 안 되는 값은 None으로 지운다 (예: M6 TTL은 M6 무게가 아님).
- 확실하지 않은 숫자는 적지 않는다(빈칸이 틀린 값보다 낫다). 라이카 사용자는 틀린 사양에 민감하다.
- checked: 출처(라이카 공식 사양서·제품 페이지 등)로 확인했으면 출처를 적는다. 비어 있으면 "확인 전"이라
  화면에 내보내지 않는다 (CHECKED_ONLY). v1은 모두 Claude 지식으로 채운 확인 전 값.

항목 (없는 항목은 빼고 적는다)
  공통: years "1954–1967" / "2023–", mount M·LTM·L·R·고정, note 한 줄
  바디: kind(필름 RF, 디지털 RF, 미러리스, 컴팩트, 필름 SLR), sensor_mp, sensor(풀프레임·APS-H·APS-C·포서드),
        mono(흑백 전용), finder(배율·EVF 화소), framelines, meter, shutter, top_speed, flash_ttl, ibis, video, weight_g
  렌즈: focal, aperture, min_focus_m, elements("8/5" = 8매 5군), filter, weight_g
"""
from __future__ import annotations

B = "leica:body:"
L = "leica:lens:"
CHECKED_ONLY = True  # 화면에는 checked(출처) 있는 값만

SPECS: dict[str, dict] = {
    # ───────────── M 필름 바디 ─────────────
    B + "m3": dict(years="1954–1967", kind="필름 RF", mount="M", finder="0.91x", framelines="50·90·135",
                   meter="없음", shutter="기계식 천 셔터", top_speed="1/1000", weight_g=580),
    B + "m3:double-stroke": dict(note="필름을 두 번 나눠 감는 초기형 (1954–1958)"),
    B + "m3:single-stroke": dict(note="필름을 한 번에 감는 후기형 (1958–)"),
    B + "m2": dict(years="1957–1968", kind="필름 RF", mount="M", finder="0.72x", framelines="35·50·90",
                   meter="없음", shutter="기계식 천 셔터", top_speed="1/1000"),
    B + "m4": dict(years="1967–1975", kind="필름 RF", mount="M", finder="0.72x", framelines="35·50·90·135",
                   meter="없음", shutter="기계식 천 셔터", top_speed="1/1000", note="빠른 필름 장전, 크랭크 되감기"),
    B + "m5": dict(years="1971–1975", kind="필름 RF", mount="M", finder="0.72x", framelines="35·50·90·135",
                   meter="TTL (스윙 암)", shutter="기계식 천 셔터", top_speed="1/1000"),
    B + "m6": dict(years="1984–1998", kind="필름 RF", mount="M", finder="0.72x", framelines="28·35·50·75·90·135",
                   meter="TTL (LED)", shutter="기계식 천 셔터", top_speed="1/1000", flash_ttl=False, weight_g=560),
    B + "m6:ttl": dict(years="1998–2002", finder="0.58x·0.72x·0.85x", flash_ttl=True,
                       weight_g=None, note="TTL 플래시 측광, 셔터 다이얼이 크고 노출계 표시와 같은 방향, 윗판 2mm 높음"),
    B + "m6:reissue": dict(years="2022–", finder="0.72x", flash_ttl=False, note="2022년 복각판, 노출계 표시·배터리 표시 개선"),
    B + "m7": dict(years="2002–2018", kind="필름 RF", mount="M", finder="0.58x·0.72x·0.85x", framelines="28·35·50·75·90·135",
                   meter="TTL (LED)", shutter="전자식 (조리개 우선 자동)", top_speed="1/1000", flash_ttl=True, weight_g=610,
                   note="배터리가 없으면 1/60·1/125만 기계식으로 작동"),
    B + "mp-film": dict(years="2003–", kind="필름 RF", mount="M", finder="0.72x (0.58x·0.85x 주문)",
                        framelines="28·35·50·75·90·135", meter="TTL (LED)", shutter="기계식 천 셔터", top_speed="1/1000",
                        flash_ttl=False, weight_g=585),

    # ───────────── M 디지털 바디 ─────────────
    B + "m8": dict(years="2006–2009", kind="디지털 RF", mount="M", sensor_mp=10.3, sensor="APS-H (1.33배 크롭)",
                   finder="0.68x", framelines="24·35 / 28·90 / 50·75", top_speed="1/8000", video="없음", weight_g=591),
    B + "m9": dict(years="2009–", kind="디지털 RF", mount="M", sensor_mp=18, sensor="풀프레임 CCD", finder="0.68x",
                   framelines="28·90 / 35·135 / 50·75", top_speed="1/4000", video="없음", weight_g=585),
    B + "m240": dict(years="2013–", kind="디지털 RF", mount="M", sensor_mp=24, sensor="풀프레임 CMOS", finder="0.68x",
                     framelines="28·90 / 35·135 / 50·75", top_speed="1/4000", video="1080p", weight_g=680,
                     note="M 디지털 첫 라이브 뷰·동영상"),
    B + "m-p240": dict(note="M 240에 버퍼 2GB·사파이어 액정, 빨간 로고 없음"),
    B + "m10": dict(years="2017–", kind="디지털 RF", mount="M", sensor_mp=24, sensor="풀프레임 CMOS", finder="0.73x",
                    framelines="28·90 / 35·135 / 50·75", top_speed="1/4000", video="없음", weight_g=660,
                    note="필름 M만큼 얇아진 첫 디지털 M"),
    B + "m10-p": dict(years="2018–", weight_g=675, note="M10에 조용한 셔터·터치 액정, 빨간 로고 없음"),
    B + "m10-r": dict(years="2020–", sensor_mp=40),
    B + "m10-monochrom": dict(years="2020–", sensor_mp=40, mono=True),
    B + "m11": dict(years="2022–", kind="디지털 RF", mount="M", sensor_mp=60, sensor="풀프레임 BSI CMOS (60·36·18MP 선택)",
                    finder="0.73x", framelines="28·90 / 35·135 / 50·75", top_speed="1/4000 (전자 1/16000)", video="없음",
                    weight_g="530 (블랙) · 640 (실버)", note="밑판 없이 아래에서 배터리 교체"),
    B + "m11-p": dict(years="2023–", note="M11에 콘텐츠 인증(CAI)·내장 256GB·사파이어 액정, 빨간 로고 없음"),

    # ───────────── SL · CL · Q · 컴팩트 ─────────────
    B + "sl601": dict(years="2015–2019", kind="미러리스", mount="L", sensor_mp=24, sensor="풀프레임 CMOS",
                      finder="EVF 440만 화소", ibis=False, video="4K", weight_g=847),
    B + "sl2": dict(years="2019–", kind="미러리스", mount="L", sensor_mp=47, sensor="풀프레임 CMOS",
                    finder="EVF 576만 화소", ibis=True, video="5K"),
    B + "sl2-s": dict(years="2020–", kind="미러리스", mount="L", sensor_mp=24, sensor="풀프레임 BSI CMOS",
                      finder="EVF 576만 화소", ibis=True, video="4K 10bit", note="SL2 몸체에 동영상·고감도 쪽 24MP 센서"),
    B + "sl3": dict(years="2024–", kind="미러리스", mount="L", sensor_mp=60, sensor="풀프레임 BSI CMOS",
                    finder="EVF 576만 화소", ibis=True, video="8K", note="틸트 액정"),
    B + "sl3-s": dict(years="2025–", kind="미러리스", mount="L", sensor_mp=24, sensor="풀프레임 BSI CMOS", ibis=True),
    B + "cl-digital": dict(years="2017–", kind="미러리스", mount="L (TL 렌즈)", sensor_mp=24, sensor="APS-C",
                           finder="EVF 236만 화소", video="4K", weight_g=403),
    B + "q": dict(years="2015–2019", kind="컴팩트", mount="고정 Summilux 28mm f/1.7", sensor_mp=24, sensor="풀프레임 CMOS",
                  finder="EVF 368만 화소", video="1080p", weight_g=640, note="렌즈 광학식 손떨림 보정"),
    B + "q2": dict(years="2019–2023", kind="컴팩트", mount="고정 Summilux 28mm f/1.7", sensor_mp=47, sensor="풀프레임 CMOS",
                   finder="EVF 368만 화소", video="4K", weight_g=734, note="방진·방적 IP52"),
    B + "q2-monochrom": dict(years="2020–", sensor_mp=47, mono=True),
    B + "q3": dict(years="2023–", kind="컴팩트", mount="고정 Summilux 28mm f/1.7", sensor_mp=60, sensor="풀프레임 BSI CMOS",
                   finder="EVF 576만 화소", video="8K", weight_g=743, note="틸트 액정"),
    B + "q3-43": dict(years="2024–", kind="컴팩트", mount="고정 APO-Summicron 43mm f/2", sensor_mp=60,
                      sensor="풀프레임 BSI CMOS", finder="EVF 576만 화소", note="틸트 액정"),
    B + "d-lux-7": dict(years="2018–", kind="컴팩트", mount="고정 24–75mm 환산 f/1.7–2.8", sensor_mp=17, sensor="포서드"),
    B + "d-lux-8": dict(years="2024–", kind="컴팩트", mount="고정 24–75mm 환산 f/1.7–2.8", sensor_mp=17, sensor="포서드"),

    # ───────────── 바르낙 (스크루 마운트) · R ─────────────
    B + "i": dict(years="1925–", kind="필름 RF", mount="LTM", finder="거리계 없음", top_speed="1/500"),
    B + "ii": dict(years="1932–", kind="필름 RF", mount="LTM", finder="연동 거리계", top_speed="1/500"),
    B + "iii": dict(years="1933–", kind="필름 RF", mount="LTM", finder="연동 거리계", top_speed="1/500", note="저속 셔터 추가"),
    B + "iiia": dict(years="1935–", kind="필름 RF", mount="LTM", finder="연동 거리계", top_speed="1/1000"),
    B + "iiic": dict(years="1940–1951", kind="필름 RF", mount="LTM", finder="연동 거리계", top_speed="1/1000",
                     note="다이캐스트 몸체로 길이가 늘어남"),
    B + "iiif": dict(years="1950–1957", kind="필름 RF", mount="LTM", finder="연동 거리계", top_speed="1/1000",
                     note="플래시 싱크 다이얼"),
    B + "iiig": dict(years="1957–1960", kind="필름 RF", mount="LTM", finder="밝은 프레임 50·90", top_speed="1/1000",
                     note="마지막 바르낙"),
    B + "r4": dict(years="1980–1987", kind="필름 SLR", mount="R", shutter="전자식", note="P·A·S·M 노출 모드"),

    # ───────────── M 렌즈 ─────────────
    L + "summicron-m:50:current": dict(years="1979–", focal=50, aperture="f/2", mount="M", min_focus_m=0.7,
                                       elements="6/4", filter="E39"),
    L + "apo-summicron-m:50": dict(years="2012–", focal=50, aperture="f/2", mount="M", min_focus_m=0.7,
                                   elements="8/5", filter="E39"),
    L + "summilux-m:50": dict(focal=50, aperture="f/1.4", mount="M"),
    L + "summilux-m:50:v1": dict(min_focus_m=1.0),
    L + "summilux-m:50:v2": dict(min_focus_m=1.0),
    L + "summilux-m:50:v3": dict(min_focus_m=1.0),
    L + "summilux-m:50:v4": dict(min_focus_m=1.0),
    L + "summilux-m:50:asph": dict(years="2004–2023", min_focus_m=0.7, elements="8/5", filter="E46"),
    L + "summilux-m:50:asph:asph-ii": dict(years="2023–", min_focus_m=0.45, note="최단 45cm 근접"),
    L + "summicron-m:35:asph": dict(years="1997–", focal=35, aperture="f/2", mount="M", min_focus_m=0.7,
                                    elements="7/5", filter="E39"),
    L + "summilux-m:35": dict(focal=35, aperture="f/1.4", mount="M"),
    L + "summilux-m:35:asph-1994": dict(years="1994–2010", min_focus_m=0.7, filter="E46"),
    L + "summilux-m:35:asph-fle": dict(years="2010–2022", min_focus_m=0.7, elements="9/5", filter="E46",
                                       note="FLE = 초점 거리에 따라 움직이는 뒷 렌즈 묶음"),
    L + "summilux-m:35:asph-fle2": dict(years="2022–", min_focus_m=0.4, note="최단 40cm 근접"),
    L + "noctilux-m:50": dict(focal=50, mount="M"),
    L + "noctilux-m:50:f0.95": dict(years="2008–", aperture="f/0.95", min_focus_m=1.0, elements="8/5", filter="E60"),
    L + "noctilux-m:50:f1.2-asph": dict(years="2021–", aperture="f/1.2", min_focus_m=1.0, note="1966년 Noctilux 복각"),
    L + "apo-summicron-m:90": dict(years="1998–", focal=90, aperture="f/2", mount="M", min_focus_m=1.0,
                                   elements="5/5", filter="E55"),
    L + "summicron-m:90": dict(focal=90, aperture="f/2", mount="M", min_focus_m=1.0),
    L + "apo-summicron-m:75": dict(years="2005–", focal=75, aperture="f/2", mount="M", min_focus_m=0.7, filter="E49"),
    L + "summilux-m:75": dict(years="1980–2007", focal=75, aperture="f/1.4", mount="M", min_focus_m=0.75,
                              elements="7/5", filter="E60"),
    L + "elmarit-m:28:asph": dict(years="2006–", focal=28, aperture="f/2.8", mount="M", min_focus_m=0.7,
                                  elements="8/6", filter="E46"),
    L + "elmarit-m:90": dict(focal=90, aperture="f/2.8", mount="M", min_focus_m=1.0),
    L + "tele-elmarit-m:90": dict(focal=90, aperture="f/2.8", mount="M", min_focus_m=1.0),
    L + "elmarit-m:135": dict(focal=135, aperture="f/2.8", mount="M", min_focus_m=1.5, note="거리계용 안경(고글) 달림"),
    L + "summaron:35:f3.5": dict(focal=35, aperture="f/3.5", min_focus_m=1.0),
    L + "summaron:35:f2.8": dict(focal=35, aperture="f/2.8"),
    L + "hektor:135": dict(focal=135, aperture="f/4.5", min_focus_m=1.5),

    # ───────────── SL 렌즈 ─────────────
    L + "vario-elmarit-sl:24-90": dict(years="2015–", focal="24–90", aperture="f/2.8–4", mount="L"),
    L + "vario-elmarit-sl:24-70": dict(years="2020–", focal="24–70", aperture="f/2.8", mount="L"),
}

# 바탕 모델 → 이 키의 사양을 물려받고 자기 값으로 덮음 (부모보다 먼저 따라감)
BASED_ON: dict[str, str] = {
    B + "m-p240": B + "m240",
    B + "m10-p": B + "m10",
    B + "m10-r": B + "m10",
    B + "m10-monochrom": B + "m10",
    B + "m11-p": B + "m11",
    B + "q2-monochrom": B + "q2",
    L + "summilux-m:50:asph:asph-ii": L + "summilux-m:50:asph",
    B + "m6:ttl-millennium": B + "m6:ttl",
    B + "m6:ttl-titan": B + "m6:ttl",
    B + "m6:ttl-black-paint": B + "m6:ttl",
    L + "summilux-m:50:asph-lhsa": L + "summilux-m:50:asph",
    L + "summilux-m:50:asph-kravitz": L + "summilux-m:50:asph",
    L + "summilux-m:50:asph-safari": L + "summilux-m:50:asph",
    L + "summilux-m:50:asph-black-paint": L + "summilux-m:50:asph",
}

CHECKED: dict[str, str] = {}  # 엔티티 ID → 출처 (확인한 것만)


def spec_for(entity_id: str, parents: dict[str, str | None]) -> dict:
    """부모 → 자기 순서로 겹쳐 쓴 사양. parents: 엔티티 ID → 부모 ID."""
    chain, cur = [], entity_id
    while cur and cur not in chain:
        chain.append(cur)
        cur = BASED_ON.get(cur) or parents.get(cur)
    out: dict = {}
    for key in reversed(chain):
        out.update(SPECS.get(key, {}))
    return {k: v for k, v in out.items() if v is not None}
