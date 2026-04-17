import json
import math
from datetime import datetime, timezone

LAMBDA = 0.1  # 감쇠 상수 (1년 전 = 가중치 ~30%)
MIN_SAMPLES = 3  # 최소 샘플 수

def calc_weight(sold_at: str, now: datetime, lambda_: float = LAMBDA) -> float:
    """지수 감쇠 가중치 계산 w = e^(-λ * Δt) Δt 단위: 개월"""
    if not sold_at:
        return 0.05  # 날짜 없으면 최저 가중치
    try:
        dt = datetime.fromisoformat(sold_at.replace("Z",""))
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        delta_months = (now - dt).days / 30
        return math.exp(-lambda_ * delta_months)
    except:
        return 0.05

def weighted_median(prices: list, weights: list) -> float:
    """가중치 적용 중앙값 계산"""
    if not prices:
        return 0
    pairs = sorted(zip(prices, weights), key=lambda x: x[0])
    total_w = sum(w for _, w in pairs)
    cumulative = 0
    for price, weight in pairs:
        cumulative += weight
        if cumulative >= total_w / 2:
            return price
    return pairs[-1][0]

def parse_price_krw(price_str: str, currency: str = "KRW") -> float:
    """가격 문자열 → KRW 변환"""
    if not price_str or price_str in ["문의요망", ""]:
        return 0
    try:
        nums = price_str.replace(",", "").replace("원", "").replace("£", "").replace("¥", "").strip()
        val = float(''.join(c for c in nums if c.isdigit() or c == '.'))
        if currency == "GBP":
            val *= 1750  # 대략적인 환율
        elif currency == "JPY":
            val *= 9.5
        return val
    except:
        return 0

def compute_market_prices(sold_quality_path: str = "data/derived/sold_quality_latest.json") -> dict:
    """label별 시세 계산"""
    with open(sold_quality_path, "r", encoding="utf-8") as f:
        sold_data = json.load(f)

    # results.json의 label을 최신 코드로 재계산해서 매핑
    try:
        import sys, os
        sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        with open("data/raw/results.json", "r", encoding="utf-8") as f:
            results = json.load(f)
        # 링크 → 최신 label 매핑
        link_to_label = {r["링크"]: r.get("label","") for r in results if r.get("label")}
        # sold_data의 label 업데이트
        for s in sold_data:
            link = s.get("listing_id", "")
            if link in link_to_label and link_to_label[link]:
                s["label"] = link_to_label[link]
    except Exception as e:
        pass

    now = datetime.now(timezone.utc)

    # label별 그룹핑
    groups = {}
    for r in sold_data:
        if not r.get("include_in_market"):
            continue
        label = r.get("label", "")
        if not label:
            continue
        if label not in groups:
            groups[label] = []
        groups[label].append(r)

    results = {}
    for label, items in groups.items():
        prices, weights = [], []
        for item in items:
            price = parse_price_krw(item.get("price",""), item.get("currency","KRW"))
            if price <= 0:
                continue
            w = calc_weight(item.get("sold_at",""), now)
            prices.append(price)
            weights.append(w)

        if len(prices) < MIN_SAMPLES:
            continue

        wmed = weighted_median(prices, weights)
        results[label] = {
            "weighted_median": int(wmed),
            "sample_count": len(prices),
            "min": int(min(prices)),
            "max": int(max(prices)),
            "avg": int(sum(prices) / len(prices)),
        }

    return results

# 시세 계산에서 제외할 generic label
EXCLUDED_LABELS = {
    "3rd Party", "Set", "Accessory", "Visoflex", "Leicavit",
    "50mm Lens", "35mm Lens", "28mm Lens", "21mm Lens", "90mm Lens",
    "75mm Lens", "135mm Lens", "TL Lens", "SL Lens", "R Lens", "S Lens",
    "LTM Lens", "Hektor", "Leica C Lens",
}

def save_market_prices(output_path: str = "data/derived/market_prices.json"):
    """시세 계산 결과 저장"""
    import json as _json
    results = compute_market_prices()
    # Generic/Bucket 라벨 제외
    results = {k: v for k, v in results.items() if k not in EXCLUDED_LABELS}
    with open(output_path, "w", encoding="utf-8") as f:
        _json.dump(results, f, ensure_ascii=False, indent=2)
    print(f"  💰 시세 저장 → {output_path} ({len(results)}개 label)")
    return results

if __name__ == "__main__":
    results = save_market_prices()
    print(f"시세 산출 완료: {len(results)}개 label")
    for label, data in sorted(results.items(), key=lambda x: -x[1]["sample_count"])[:20]:
        wmed = f"{data['weighted_median']:,}"
        cnt = data['sample_count']
        print(f"  {label:40s} {wmed:>12s}원  ({cnt}개)")

