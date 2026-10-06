"""사양으로 찾기: 프레임라인·노출계·TTL 플래시·기계식 셔터 → 그 사양을 가진 M 바디 묶음.

(2026-10-04 레딧 r/Leica 피드백: "28mm 프레임라인, TTL 같은 사양으로 찾고 싶다")

묶음 하나 = 검색창 후보 하나. 고르면 members 바디들의 매물을 한꺼번에 보여 준다.
  - members: 엔티티 ID (부모를 넣으면 그 아래 모든 버전 포함). 사양이 버전마다 다르면 부모 대신 버전만 넣는다
  - exclude: 제목에 이 말이 있으면 빼기 (예: 0.85 파인더는 28mm 프레임라인이 없음)
  - 시세는 모델이 섞이므로 계산하지 않는다

사양 기준 (라이카 공식 사양):
  - 28mm 프레임라인: M4-P부터. 0.72·0.58 파인더는 있음, 0.85 파인더(M6J·0.85 버전)는 없음. 디지털 M은 모두 있음
  - TTL 플래시 측광: M6 TTL, M7 (MP·M6 2022 복각은 없음)
  - 노출계 내장: M5, CL, M6 전부, M7, MP / 없음: M1·M2·M3·M4·M4-2·M4-P·M-A·MD
  - 배터리 없이 셔터 작동(기계식): M7만 전자식 셔터라 빠짐
"""
from __future__ import annotations

B = "leica:body:"

_M6_WITH_28 = [B + s for s in ("m6:classic", "m6:ttl", "m6:reissue", "m6:titan", "m6:platinum", "m6:lhsa", "m6:royal",
                               "m6:jaguar", "m6:ttl-millennium", "m6:ttl-titan", "m6:ttl-black-paint")]
_DIGITAL_M = [B + s for s in ("m8", "m8-2", "m9", "m9-p", "m-e", "m240", "m-p240", "m-e240", "m-monochrom-ccd",
                              "m-monochrom-246", "m262", "m-d262", "m10", "m10-p", "m10-r", "m10-monochrom", "m10-d",
                              "m10-e", "m11", "m11-p", "m11-monochrom", "m11-d")]
_NO_METER = [B + s for s in ("m3", "m2", "m2-r", "m1", "md", "m4", "m4-2", "m4-p", "m-a")]

# id: (영어 이름, 한국어 이름, members, 검색 별칭, exclude)
FEATURES: dict[str, tuple[str, str, list[str], list[str], list[str]]] = {
    "leica:feature:frameline-28": (
        "Leica M bodies with 28mm framelines", "28mm 프레임라인 있는 M 바디",
        [B + "m4-p", B + "m7", B + "mp-film", B + "m-a"] + _M6_WITH_28 + _DIGITAL_M,
        ["frameline 28", "framelines 28", "frame line 28", "프레임라인 28", "프레임 28"],  # 숫자로 시작하면 "28" 검색이 렌즈보다 이 묶음을 먼저 띄움
        [r"0\.85", r"\bM6 ?J\b"],
    ),
    "leica:feature:ttl-flash": (
        "Film M bodies with TTL flash metering (M6 TTL, M7)", "TTL 플래시 측광 필름 M 바디 (M6 TTL·M7)",
        [B + "m6:ttl", B + "m6:ttl-millennium", B + "m6:ttl-titan", B + "m6:ttl-black-paint", B + "m7"],
        ["ttl", "ttl flash", "ttl metering", "ttl 플래시", "ttl 측광", "티티엘"],
        [],
    ),
    "leica:feature:meter": (
        "Film M bodies with a built-in light meter", "노출계 내장 필름 M 바디",
        [B + "m5", B + "cl-film", B + "cl-film-50-jahre", B + "m6", B + "m7", B + "mp-film", B + "mp3"],
        ["meter", "light meter", "built in meter", "with meter", "metered", "노출계", "노출계 내장", "노출계 있는"],
        [],
    ),
    "leica:feature:no-meter": (
        "Film M bodies without a light meter", "노출계 없는 필름 M 바디",
        _NO_METER,
        ["no meter", "meterless", "without meter", "non metered", "노출계 없는", "노출계 없음", "무노출계"],
        [],
    ),
    "leica:feature:mechanical": (
        "Film M bodies that work without a battery (mechanical shutter)", "배터리 없이 찍히는 필름 M 바디 (기계식 셔터)",
        _NO_METER + [B + "m5", B + "cl-film", B + "cl-film-50-jahre", B + "m6", B + "mp-film", B + "mp3"],
        ["mechanical", "mechanical shutter", "fully mechanical", "battery free", "no battery", "기계식", "기계식 셔터",
         "완전 기계식", "배터리 없이"],
        [],
    ),
}
