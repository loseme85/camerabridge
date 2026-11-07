import json
from pathlib import Path

BANK = Path(__file__).resolve().parent.parent / "data" / "derived" / "quiz_bank.json"


def test_quiz_bank_answers_are_valid():
    questions = json.loads(BANK.read_text(encoding="utf-8"))["questions"]
    kinds = {q["kind"] for q in questions}
    assert {"code_word", "order_no", "feature", "compare", "price"} <= kinds
    for q in questions:
        options = q.get("options") or q.get("options_krw")
        assert 2 <= len(options) <= 4 and 0 <= q["answer"] < len(options)
        assert len(set(map(str, options))) == len(options), q


def test_feature_answers_match_official_specs():
    from catalog import features
    questions = json.loads(BANK.read_text(encoding="utf-8"))["questions"]
    no_meter = set(features.FEATURES["leica:feature:no-meter"][2])
    for q in questions:
        if q["kind"] == "feature" and q["vars"]["f"] == "no_meter":
            assert q["entity"] in no_meter
