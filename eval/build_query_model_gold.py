"""구매자 검색어 → 정답 모델 세트 (query_model_gold_v1.json) 생성.

모델마다 '맞는 매물' 판정 규칙(종류·마운트·제목에 꼭 있어야 할 말·있으면 안 되는 말)을 둔다.
매물에 아직 모델 ID가 없어서 제목 규칙으로 채점한다. 모델 ID가 생기면 model_key로 바꿔 채점한다.

intent:
  exact      한 모델로 정해져야 함 → 상위 결과가 그 모델이어야 함
  parent     세대·버전이 여럿인 모델 → 자식 모델 중 무엇이든 맞음 (되묻기도 맞음)
  ambiguous  여러 모델이 가능 → 되묻거나(needs_disambiguation) 후보 모델만 보여야 함
  nonexistent 없는 모델 → 비슷한 걸로 채우지 말고 되묻거나 결과 없음이어야 함
"""
from __future__ import annotations

import json
from pathlib import Path

OUT = Path(__file__).resolve().parent / "query_model_gold_v1.json"


def f(n: str) -> str:
    """초점거리: 35mm, 35/1.4, 'M 35 ' 등. 135의 35 같은 오인 방지."""
    return rf"(?<![\d.]){n}(?:\s?mm|/|\b)"


MODELS: dict[str, dict] = {}


def model(key, name, category, mount=None, must=(), must_not=()):
    MODELS[key] = {"model_key": key, "display_name": name, "category": category, "mount": mount,
                   "title_must": list(must), "title_must_not": list(must_not)}


ACC_NOT = [r"\bhood\b", r"후드", r"\bcap\b", r"캡", r"case", r"케이스", r"strap", r"스트랩", r"holster", r"홀스터",
           r"grip", r"그립", r"battery", r"배터리", r"charger", r"충전기", r"protector", r"cover\b", r"부속품"]

# ── M 필름 바디 ──
model("leica:body:m3", "Leica M3", "Body", "M", [r"\bM ?3\b"], [r"M3J", r"MP3"])
model("leica:body:m2", "Leica M2", "Body", "M", [r"\bM ?2\b"], [r"M2-?R", r"\bM ?24\d"])
model("leica:body:m4", "Leica M4", "Body", "M", [r"\bM ?4\b"], [r"M4-?P", r"M4-?2"])
model("leica:body:m4-p", "Leica M4-P", "Body", "M", [r"\bM ?4-?P\b"])
model("leica:body:m4-2", "Leica M4-2", "Body", "M", [r"\bM ?4-2\b"])
model("leica:body:m5", "Leica M5", "Body", "M", [r"\bM ?5\b"])
model("leica:body:m6:classic", "Leica M6 (Classic)", "Body", "M", [r"\bM ?6\b"],
      [r"TTL", r"re-?issue", r"리이슈", r"2022", r"M6 ?J\b"])
model("leica:body:m6:ttl", "Leica M6 TTL", "Body", "M", [r"\bM ?6\b", r"TTL"])
model("leica:body:m6:reissue", "Leica M6 (2022 Reissue)", "Body", "M", [r"\bM ?6\b", r"(re-?issue|리이슈|2022|복각)"], [r"TTL"])
model("leica:body:m7", "Leica M7", "Body", "M", [r"\bM ?7\b"])
model("leica:body:mp-film", "Leica MP (film)", "Body", "M", [r"\bMP\b"], [r"M-?P\b ?(240|typ)", r"M10-?P", r"M11-?P", r"MP3", r"MP6"])
model("leica:body:m-a", "Leica M-A (Typ 127)", "Body", "M", [r"\bM-?A\b"])
# ── M 디지털 바디 ──
model("leica:body:m8", "Leica M8", "Body", "M", [r"\bM ?8\b"], [r"M8\.2"])
model("leica:body:m9", "Leica M9", "Body", "M", [r"\bM ?9\b"], [r"M9-?P", r"monochrom"])
model("leica:body:m240", "Leica M (Typ 240)", "Body", "M", [r"(\bM ?240\b|typ ?240)"], [r"M-?P"])
model("leica:body:m10", "Leica M10", "Body", "M", [r"\bM ?10\b"], [r"M10-?(P|R|D|E)\b", r"monochrom"] + ACC_NOT)
model("leica:body:m10-p", "Leica M10-P", "Body", "M", [r"\bM ?10-?P\b"], ACC_NOT)
model("leica:body:m10-r", "Leica M10-R", "Body", "M", [r"\bM ?10-?R\b"], ACC_NOT)
model("leica:body:m10-monochrom", "Leica M10 Monochrom", "Body", "M", [r"\bM ?10\b", r"monochrom"], [r"M10-?P"] + ACC_NOT)
model("leica:body:m11", "Leica M11", "Body", "M", [r"\bM ?11\b"], [r"M11-?(P|D|V)\b", r"monochrom"] + ACC_NOT)
model("leica:body:m11-p", "Leica M11-P", "Body", "M", [r"\bM ?11-?P\b"], ACC_NOT)
model("leica:body:m11-monochrom", "Leica M11 Monochrom", "Body", "M", [r"\bM ?11\b", r"monochrom"], ACC_NOT)
# ── Q · SL · 기타 바디 ──
model("leica:body:q", "Leica Q (Typ 116)", "Body", None, [r"\bQ\b"], [r"\bQ ?[23]\b"] + ACC_NOT)
model("leica:body:q2", "Leica Q2", "Body", None, [r"\bQ ?2\b"], [r"monochrom"] + ACC_NOT)
model("leica:body:q2-monochrom", "Leica Q2 Monochrom", "Body", None, [r"\bQ ?2\b", r"monochrom"], ACC_NOT)
model("leica:body:q3", "Leica Q3", "Body", None, [r"\bQ ?3\b"], [r"\b43\b"] + ACC_NOT)
model("leica:body:sl2", "Leica SL2", "Body", "SL", [r"\bSL ?2\b"], [r"SL2-?S"] + ACC_NOT)
model("leica:body:sl2-s", "Leica SL2-S", "Body", "SL", [r"\bSL ?2-?S\b"], ACC_NOT)
model("leica:body:sl3", "Leica SL3", "Body", "SL", [r"\bSL ?3\b"], ACC_NOT)
model("leica:body:iiif", "Leica IIIf", "Body", None, [r"\bIII ?f\b"])
model("leica:body:iiig", "Leica IIIg", "Body", None, [r"\bIII ?g\b"])
# ── M 렌즈 ──
model("leica:lens:summilux-m:35:asph-fle", "Summilux-M 35mm f/1.4 ASPH FLE", "Lens", "M",
      [r"(summilux|lux)", f("35"), r"FLE"], [r"FLE ?(II|2)\b", r"steel"] + ACC_NOT)
model("leica:lens:summilux-m:35:asph-fle2", "Summilux-M 35mm f/1.4 ASPH FLE II", "Lens", "M",
      [r"(summilux|lux)", f("35"), r"FLE ?(II|2)\b"], ACC_NOT)
model("leica:lens:summilux-m:35:steel-rim-reissue", "Summilux-M 35mm f/1.4 Steel Rim (2021 reissue)", "Lens", "M",
      [r"(summilux|lux)", f("35"), r"(steel ?rim|스틸 ?림)", r"(re-?issue|복각|2021)"], ACC_NOT)
model("leica:lens:summicron-m:35:asph", "Summicron-M 35mm f/2 ASPH", "Lens", "M",
      [r"summicron|cron", f("35"), r"ASPH"], [r"\bAPO\b"] + ACC_NOT)
model("leica:lens:summicron-m:35:v1-8element", "Summicron 35mm f/2 1st (8 elements)", "Lens", "M",
      [r"summicron|cron", f("35"), r"(8 ?el|8매|eight|1st|1세대)"], [r"ASPH"] + ACC_NOT)
model("leica:lens:summicron-m:35:v4", "Summicron 35mm f/2 4th (pre-ASPH)", "Lens", "M",
      [r"summicron|cron", f("35"), r"(4th|v4|4세대|6매|6 ?el|IV\b)"], [r"ASPH"] + ACC_NOT)
model("leica:lens:apo-summicron-m:35", "APO-Summicron-M 35mm f/2 ASPH", "Lens", "M",
      [r"APO", r"summicron|cron", f("35")], ACC_NOT)
model("leica:lens:summilux-m:50:asph", "Summilux-M 50mm f/1.4 ASPH", "Lens", "M",
      [r"(summilux|lux)", f("50"), r"ASPH"], ACC_NOT)
model("leica:lens:summicron-m:50:current", "Summicron-M 50mm f/2 (4th/5th)", "Lens", "M",
      [r"summicron|cron", f("50")], [r"\bAPO\b", r"rigid|리짓", r"\bDR\b|dual ?range", r"collaps|침동", r"\bR\b ?50|-R\b", r"\bSL\b", r"\bL ?50|LTM|M39"] + ACC_NOT)
model("leica:lens:summicron:50:rigid", "Summicron 50mm f/2 Rigid", "Lens", None, [r"summicron|cron", f("50"), r"rigid|리짓|고정"], [r"\bDR\b|dual ?range"] + ACC_NOT)
model("leica:lens:summicron:50:dr", "Summicron 50mm f/2 Dual Range", "Lens", "M", [r"summicron|cron", f("50"), r"\bDR\b|dual ?range"], ACC_NOT)
model("leica:lens:apo-summicron-m:50", "APO-Summicron-M 50mm f/2 ASPH", "Lens", "M", [r"APO", r"summicron|cron", f("50")], [r"\bSL\b"] + ACC_NOT)
model("leica:lens:noctilux-m:50:f0.95", "Noctilux-M 50mm f/0.95 ASPH", "Lens", "M", [r"nocti", r"0\.95"], ACC_NOT)
model("leica:lens:noctilux-m:50:f1.0", "Noctilux-M 50mm f/1.0", "Lens", "M", [r"nocti", r"(\b1\.0\b|/1\b|f1\b|E60|E58)"], [r"0\.95", r"1\.2"] + ACC_NOT)
model("leica:lens:elmarit-m:28:asph", "Elmarit-M 28mm f/2.8 ASPH", "Lens", "M", [r"elmarit", f("28"), r"ASPH"], ACC_NOT)
model("leica:lens:summicron-m:28:asph", "Summicron-M 28mm f/2 ASPH", "Lens", "M", [r"summicron|cron", f("28")], [r"\bAPO\b"] + ACC_NOT)
model("leica:lens:summaron:35", "Summaron 35mm (f/3.5 · f/2.8)", "Lens", None, [r"summaron", f("35")], ACC_NOT)
model("leica:lens:summaron-m:28:f5.6", "Summaron-M 28mm f/5.6", "Lens", None, [r"summaron", f("28")], ACC_NOT)
model("leica:lens:elmar-m:50:f2.8", "Elmar-M 50mm f/2.8", "Lens", None, [r"elmar\b|elmar-m", f("50"), r"2\.8"], [r"elmarit"] + ACC_NOT)
model("leica:lens:summicron-m:90", "Summicron-M 90mm f/2", "Lens", "M", [r"summicron|cron", f("90")], [r"\bAPO\b", r"-R\b|\bR ?90", r"\bSL\b"] + ACC_NOT)
model("leica:lens:summilux-m:75", "Summilux-M 75mm f/1.4", "Lens", "M", [r"(summilux|lux)", f("75")], [r"\bSL\b"] + ACC_NOT)
model("leica:lens:tri-elmar-m:16-18-21", "Tri-Elmar-M 16-18-21mm f/4 (WATE)", "Lens", "M", [r"(tri-?elmar|WATE)", r"16"], ACC_NOT)
model("leica:lens:super-elmar-m:21", "Super-Elmar-M 21mm f/3.4 ASPH", "Lens", "M", [r"super-? ?elmar", f("21")], ACC_NOT)
# ── SL · R 렌즈 ──
model("leica:lens:vario-elmarit-sl:24-90", "Vario-Elmarit-SL 24-90mm f/2.8-4 ASPH", "Lens", "SL", [r"24-90"], ACC_NOT)
model("leica:lens:apo-summicron-sl:35", "APO-Summicron-SL 35mm f/2 ASPH", "Lens", "SL", [r"APO", r"summicron", f("35")], ACC_NOT)
model("leica:lens:summicron-r:50", "Summicron-R 50mm f/2", "Lens", "R", [r"summicron", f("50")], ACC_NOT)
model("leica:lens:apo-telyt-r:180", "APO-Telyt-R 180mm f/3.4", "Lens", "R", [r"telyt", f("180")], ACC_NOT)
model("leica:lens:summilux-r:80", "Summilux-R 80mm f/1.4", "Lens", "R", [r"summilux", f("80")], ACC_NOT)

CASES: list[dict] = []


def case(query, intent, models, lang="en", note=""):
    for key in models:
        assert key in MODELS, key
    CASES.append({"id": f"QMG-{len(CASES) + 1:03d}", "query": query, "lang": lang, "intent": intent,
                  "expected_models": list(models), "note": note})


E, P, A, N = "exact", "parent", "ambiguous", "nonexistent"
M6_ALL = ["leica:body:m6:classic", "leica:body:m6:ttl", "leica:body:m6:reissue"]
# 바디
case("Leica M3", E, ["leica:body:m3"]); case("라이카 M3", E, ["leica:body:m3"], "ko")
case("Leica M2", E, ["leica:body:m2"])
case("Leica M4", E, ["leica:body:m4"]); case("M4-P", E, ["leica:body:m4-p"]); case("M4-2", E, ["leica:body:m4-2"])
case("Leica M5", E, ["leica:body:m5"])
case("Leica M6", P, M6_ALL, note="클래식·TTL·리이슈 중 무엇이든 맞음. 어느 것인지 되묻는 것도 맞음")
case("라이카 M6", P, M6_ALL, "ko")
case("M6 classic", E, ["leica:body:m6:classic"]); case("M6 TTL", E, ["leica:body:m6:ttl"])
case("M6 TTL 0.72", E, ["leica:body:m6:ttl"]); case("M6 reissue", E, ["leica:body:m6:reissue"])
case("M6 리이슈", E, ["leica:body:m6:reissue"], "ko")
case("Leica M7", E, ["leica:body:m7"]); case("Leica MP", E, ["leica:body:mp-film"]); case("Leica M-A", E, ["leica:body:m-a"])
case("Leica M8", E, ["leica:body:m8"]); case("Leica M9", E, ["leica:body:m9"]); case("Leica M240", E, ["leica:body:m240"])
case("Leica M10", E, ["leica:body:m10"]); case("M10 body", E, ["leica:body:m10"]); case("라이카 M10", E, ["leica:body:m10"], "ko")
case("M10-P", E, ["leica:body:m10-p"]); case("M10-R", E, ["leica:body:m10-r"]); case("M10 Monochrom", E, ["leica:body:m10-monochrom"])
case("Leica M11", E, ["leica:body:m11"]); case("M11-P", E, ["leica:body:m11-p"]); case("M11 Monochrom", E, ["leica:body:m11-monochrom"])
case("Leica Q", E, ["leica:body:q"]); case("Leica Q2", E, ["leica:body:q2"]); case("라이카 Q2", E, ["leica:body:q2"], "ko")
case("Q2 Monochrom", E, ["leica:body:q2-monochrom"]); case("Leica Q3", E, ["leica:body:q3"])
case("Leica SL2", E, ["leica:body:sl2"]); case("SL2-S", E, ["leica:body:sl2-s"]); case("Leica SL3", E, ["leica:body:sl3"])
case("Leica IIIf", E, ["leica:body:iiif"]); case("Leica IIIg", E, ["leica:body:iiig"])
# M 렌즈
case("Summilux 35 FLE", E, ["leica:lens:summilux-m:35:asph-fle"]); case("35 lux FLE", E, ["leica:lens:summilux-m:35:asph-fle"])
case("Summilux 35 FLE II", E, ["leica:lens:summilux-m:35:asph-fle2"]); case("35 lux fle2", E, ["leica:lens:summilux-m:35:asph-fle2"])
case("주미룩스 35 FLE", E, ["leica:lens:summilux-m:35:asph-fle"], "ko")
case("Summilux 35 steel rim reissue", E, ["leica:lens:summilux-m:35:steel-rim-reissue"])
case("스틸림 복각", E, ["leica:lens:summilux-m:35:steel-rim-reissue"], "ko")
case("35 lux", A, ["leica:lens:summilux-m:35:asph-fle", "leica:lens:summilux-m:35:asph-fle2", "leica:lens:summilux-m:35:steel-rim-reissue"],
     note="35mm Summilux는 세대가 많음 → 되묻거나 35 Summilux만 보여야 함")
case("Summicron 35 ASPH", E, ["leica:lens:summicron-m:35:asph"]); case("35 cron asph", E, ["leica:lens:summicron-m:35:asph"])
case("주미크론 35 ASPH", E, ["leica:lens:summicron-m:35:asph"], "ko")
case("Summicron 35 8 element", E, ["leica:lens:summicron-m:35:v1-8element"]); case("8매", E, ["leica:lens:summicron-m:35:v1-8element"], "ko")
case("Summicron 35 4th", E, ["leica:lens:summicron-m:35:v4"]); case("6매", E, ["leica:lens:summicron-m:35:v4"], "ko")
case("APO Summicron 35", A, ["leica:lens:apo-summicron-m:35", "leica:lens:apo-summicron-sl:35"], note="M과 SL에 둘 다 있음")
case("Summilux 50 ASPH", E, ["leica:lens:summilux-m:50:asph"]); case("50 lux asph", E, ["leica:lens:summilux-m:50:asph"])
case("주미룩스 50 ASPH", E, ["leica:lens:summilux-m:50:asph"], "ko")
case("50 cron", A, ["leica:lens:summicron-m:50:current", "leica:lens:summicron-r:50", "leica:lens:summicron:50:rigid", "leica:lens:summicron:50:dr"],
     note="M·R·SL, 세대(리짓·DR) 여럿 → 되묻거나 50 Summicron만")
case("Summicron M 50", E, ["leica:lens:summicron-m:50:current"]); case("주미크론 50", A, ["leica:lens:summicron-m:50:current", "leica:lens:summicron-r:50", "leica:lens:summicron:50:rigid", "leica:lens:summicron:50:dr"], "ko")
case("50 cron rigid", E, ["leica:lens:summicron:50:rigid"]); case("리짓", E, ["leica:lens:summicron:50:rigid"], "ko")
case("50 cron DR", E, ["leica:lens:summicron:50:dr"])
case("APO Summicron M 50", E, ["leica:lens:apo-summicron-m:50"]); case("APO 50 cron", E, ["leica:lens:apo-summicron-m:50"])
case("Noctilux 0.95", E, ["leica:lens:noctilux-m:50:f0.95"]); case("녹티룩스 0.95", E, ["leica:lens:noctilux-m:50:f0.95"], "ko")
case("Noctilux 1.0", E, ["leica:lens:noctilux-m:50:f1.0"]); case("nocti e60", E, ["leica:lens:noctilux-m:50:f1.0"])
case("Noctilux", A, ["leica:lens:noctilux-m:50:f0.95", "leica:lens:noctilux-m:50:f1.0"], note="f/0.95·f/1.0·f/1.2 → 되묻거나 Noctilux만")
case("녹티룩스", A, ["leica:lens:noctilux-m:50:f0.95", "leica:lens:noctilux-m:50:f1.0"], "ko")
case("Elmarit 28 ASPH", E, ["leica:lens:elmarit-m:28:asph"]); case("엘마리트 28", E, ["leica:lens:elmarit-m:28:asph"], "ko")
case("Summicron 28 ASPH", E, ["leica:lens:summicron-m:28:asph"])
case("Summaron 35", E, ["leica:lens:summaron:35"]); case("즈마론 35", E, ["leica:lens:summaron:35"], "ko")
case("Summaron 28 5.6", E, ["leica:lens:summaron-m:28:f5.6"])
case("Elmar 50 2.8", E, ["leica:lens:elmar-m:50:f2.8"])
case("Summicron 90", E, ["leica:lens:summicron-m:90"]); case("Summilux 75", E, ["leica:lens:summilux-m:75"])
case("WATE", E, ["leica:lens:tri-elmar-m:16-18-21"]); case("Tri-Elmar 16-18-21", E, ["leica:lens:tri-elmar-m:16-18-21"])
case("Super Elmar 21", E, ["leica:lens:super-elmar-m:21"])
# SL · R
case("SL 24-90", E, ["leica:lens:vario-elmarit-sl:24-90"]); case("24-90 vario elmarit", E, ["leica:lens:vario-elmarit-sl:24-90"])
case("APO Summicron SL 35", E, ["leica:lens:apo-summicron-sl:35"])
case("Summicron R 50", E, ["leica:lens:summicron-r:50"]); case("APO Telyt R 180", E, ["leica:lens:apo-telyt-r:180"])
case("Summilux R 80", E, ["leica:lens:summilux-r:80"])
# 없는 모델: 비슷한 걸로 채우면 안 됨
case("Summicron SL 24", N, [], note="SL 24mm Summicron은 없음")
case("24 cron", N, [], note="Leica 24mm Summicron은 없음")
case("Summilux 135", N, [], note="135mm Summilux는 없음")
case("M8 Monochrom", N, [], note="M8 Monochrom은 없음")

OUT.write_text(json.dumps({"schema_version": "query_model_gold_v1", "updated_at": "2026-10-03",
                           "models": MODELS, "cases": CASES}, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print(f"models {len(MODELS)}, cases {len(CASES)}")
