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


# 모델 정의는 엔티티 카탈로그 원본 하나만 쓴다 (catalog/build_entity_catalog.py)
import sys as _sys  # noqa: E402

_sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "catalog"))
from build_entity_catalog import MODELS  # noqa: E402

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
