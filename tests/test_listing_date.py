

def test_store_posted_date_wins_over_photo_address():
    import datetime as dt
    from listing_date import listed_of, posted_of
    today = dt.date(2026, 11, 2)
    item = {"게시일": "2025-03-04", "이미지": "https://cdn.shopify.com/a.jpg?v=1783637860"}
    assert posted_of(item, today) == "2025-03-04"
    assert listed_of(item, today) == "2025-03-04"
    assert posted_of({"게시일": "2027-01-01"}, today) is None  # 오늘보다 뒤
    assert posted_of({"게시일": ""}, today) is None
    assert listed_of({"이미지": "https://x.com/web/product/big/202412/a.jpg"}, today) == "2024-12"


def test_sold_history_adds_gone_listings_once():
    from final_resolution_pipeline import _with_sold_history
    import json, tempfile, os
    sold = [{"링크": "a", "가격": "$100", "is_sold": True, "sold_reason": "gone", "품절": False},
            {"링크": "b", "가격": "$200", "is_sold": True},
            {"링크": "c", "가격": "문의요망", "is_sold": True}]
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
        json.dump(sold, f)
    try:
        out = _with_sold_history([{"링크": "b", "가격": "$200"}], f.name)
    finally:
        os.unlink(f.name)
    assert [x["링크"] for x in out] == ["b", "a"]
    assert out[1]["품절"] is True
    assert _with_sold_history([{"링크": "x"}], None) == [{"링크": "x"}]
