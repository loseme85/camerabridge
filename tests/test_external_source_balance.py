from __future__ import annotations

from search_service import balance_external_sources


def _row(source: str, name: str) -> dict:
    return {"source": source, "title": name}


def _sources(rows: list[dict]) -> str:
    return "".join("E" if row["source"] == "eBay" else "L" for row in rows)


def test_external_rows_capped_to_one_per_three_slots() -> None:
    rows = [_row("eBay", f"e{i}") for i in range(6)] + [_row("사진집", f"l{i}") for i in range(6)]
    assert _sources(balance_external_sources(rows)) == "ELLELLELLEEE"


def test_external_rows_never_move_ahead_of_better_local_rows() -> None:
    rows = [_row("사진집", "l0"), _row("사진집", "l1"), _row("eBay", "e0"), _row("사진집", "l2")]
    assert [row["title"] for row in balance_external_sources(rows)] == ["l0", "l1", "e0", "l2"]


def test_external_rows_fill_when_local_runs_out() -> None:
    rows = [_row("eBay", "e0"), _row("eBay", "e1"), _row("사진집", "l0")]
    assert _sources(balance_external_sources(rows)) == "ELE"


def test_source_from_final_output_is_recognized() -> None:
    rows = [{"final_output": {"source": "eBay"}}, {"final_output": {"source": "eBay"}}, _row("사진집", "l0")]
    assert [bool(row.get("final_output")) for row in balance_external_sources(rows)] == [True, False, True]


def test_local_only_results_unchanged() -> None:
    rows = [_row("사진집", "l0"), _row("장씨카메라", "l1")]
    assert balance_external_sources(rows) == rows


def test_active_listings_stay_balanced_after_sold_listings_drop_out() -> None:
    # 엔티티 모드에서 판매 완료가 뒤로 빠져도, 판매 중 매물 맨 앞에 eBay가 몰리지 않아야 함
    def rec(source, sold):
        return {"source": source, "final_output": {"source": source, "sold_quality": "sold_confirmed" if sold else "asking"}}
    results = [rec("장씨카메라", True), rec("eBay", False), rec("장씨카메라", True), rec("eBay", False),
               rec("장씨카메라", True), rec("eBay", False), rec("사진집", False), rec("사진집", False), rec("사진집", False)]
    active_first = sorted(results, key=lambda r: r["final_output"]["sold_quality"] != "asking")
    balanced = balance_external_sources(active_first)
    first_three = [r["source"] for r in balanced[:3]]
    assert first_three.count("eBay") <= 1
