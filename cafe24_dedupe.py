"""Cafe24 매장의 같은 상품이 분류 두 곳에 걸려 링크만 다르게 두 번 잡히는 것을 합친다.

라이카스토어 충무로(leica-storebando.co.kr): 충무로(cate_no=442)에 전체 상품이, 대치(436)에 그중 일부가 같이 걸려 있어
'/22524/category/442/'와 '/22524/category/436/'가 따로 잡혔다 (2026-11-22: 3,055개 상품 중 461개가 두 번, 460개는 이름·가격 동일).
상품 번호(링크의 /숫자/category/)가 같으면 하나로 합친다. 충무로(442) 링크를 두고, 한쪽이라도 판매 중이면 판매 중으로 둔다.
병합 단계(crawl_engine.merge_source)에서 이전 기록과 이번 수집 양쪽에 같은 방식으로 적용해, 예전 436 링크 기록이
'팔림' 알림 없이 조용히 정리되게 한다.
"""
import re

_PRODUCT_NO = re.compile(r"/(\d+)/category/(\d+)")
PRIMARY_CATEGORY = "442"  # 충무로


def product_no(link: str):
    m = _PRODUCT_NO.search(link or "")
    return m.group(1) if m else None


def _is_primary(link: str) -> bool:
    m = _PRODUCT_NO.search(link or "")
    return bool(m and m.group(2) == PRIMARY_CATEGORY)


def dedupe_by_product_no(rows):
    """같은 상품 번호는 한 줄로. 자리는 처음 나온 줄 자리, 내용은 충무로 링크 줄 (없으면 처음 줄)."""
    out, index = [], {}
    for r in rows:
        no = product_no(r.get("링크"))
        if no is None:
            out.append(r)
            continue
        if no not in index:
            index[no] = len(out)
            out.append(r)
            continue
        pos = index[no]
        cur = out[pos]
        keep, other = (r, cur) if (_is_primary(r.get("링크")) and not _is_primary(cur.get("링크"))) else (cur, r)
        if keep.get("품절") and not other.get("품절"):  # 한쪽 분류에서라도 판매 중이면 판매 중
            keep = {k: v for k, v in keep.items() if k not in ("sold_at", "sold_fx_krw", "sold_at_unknown")}
            keep["품절"] = False
            keep["예약중"] = other.get("예약중", False)
        out[pos] = keep
    return out
