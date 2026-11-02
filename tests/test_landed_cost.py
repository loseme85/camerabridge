"""landed_cost.py(서버)가 화면(beta.html)의 도착 총액 계산과 같은지: 화면 함수를 꺼내 node로 돌려 비교"""
from __future__ import annotations

import json
import re
import shutil
import subprocess
from pathlib import Path

import pytest

from landed_cost import landed_total, load_rates, load_rules

ROOT = Path(__file__).resolve().parents[1]
FUNCS = ["finalField", "fxRate", "convertAmount", "roundEstimate", "resultCategory", "resultOriginCountry", "landedSourceRule",
         "landedRegionOf", "landedTaxUsd", "computeLandedCost", "parseNumericPrice"]

CASES = [
    {"source": "Five Star Camera (일본)", "currency": "USD", "price": "$2,848", "category": "Lens", "title": "Leica Summicron-M 35mm f2 ASPH"},
    {"source": "Leica Classic (독일)", "currency": "EUR", "price": "€4,800", "category": "Lens", "title": "Leica Summilux-M 50mm f1.4 ASPH"},
    {"source": "기타무라 (일본)", "currency": "JPY", "price": "¥398,000", "category": "Body", "title": "Leica M6 TTL 0.72"},
    {"source": "Camera West (미국)", "currency": "USD", "price": "$7,995", "category": "Body", "title": "Leica M11 Black"},
    {"source": "국민카메라", "currency": "KRW", "price": "2,450,000원", "category": "Lens", "title": "Leica Summicron 50mm f2"},
    {"source": "Harrison Cameras (영국)", "currency": "GBP", "price": "£1,250", "category": "Lens", "title": "Leica Elmarit-M 28mm f2.8"},
    {"source": "Used.cl (칠레)", "currency": "CLP", "price": "CLP 2,080,000", "category": "Lens", "title": "Leica Summicron-M 35mm f2 ASPH"},
    {"source": "Five Star Camera (일본)", "currency": "USD", "price": "$95", "category": "Accessory", "title": "Leica 12526 hood"},
]
TARGETS = [("KRW", "KR"), ("USD", "US"), ("JPY", "JP"), ("EUR", "DE"), ("GBP", "GB"), ("TWD", "TW"), ("CNY", "CN"), ("BRL", "BR")]


def _js_functions() -> str:
    src = (ROOT / "app/templates/beta.html").read_text(encoding="utf-8")
    out = []
    for name in FUNCS:
        m = re.search(rf"\n    function {name}\(.*?\n    }}\n", src, re.S)
        assert m, name
        out.append(m.group(0))
    return "\n".join(out)


@pytest.mark.skipif(not shutil.which("node"), reason="node 없음")
def test_server_landed_total_matches_page():
    rules, rates = load_rules(), load_rates()
    script = _js_functions() + """
const input = JSON.parse(require('fs').readFileSync(0, 'utf8'));
const landedState = { rules: input.rules, fx: { rates: input.rates } };
const out = [];
for (const [target, dest] of input.targets) {
  const uiState = { currency: target, destination: dest };
  globalThis.uiState = uiState;
  for (const c of input.cases) {
    const r = computeLandedCost({ source: c.source, currency: c.currency, price: c.price, category: c.category, title: c.title, final_output: {} });
    out.push(r && r.landed ? r.landed.total : null);
  }
}
console.log(JSON.stringify(out));
"""
    script = script.replace("const landedState", "globalThis.landedState").replace("globalThis.uiState = uiState;", "globalThis.uiState = uiState;")
    js = subprocess.run(["node", "-e", "var landedState, uiState;\n" + script.replace("globalThis.landedState = ", "landedState = ").replace("const uiState = ", "uiState = ")],
                        input=json.dumps({"rules": rules, "rates": rates, "cases": CASES, "targets": TARGETS}), capture_output=True, text=True)
    assert js.returncode == 0, js.stderr
    page = json.loads(js.stdout)
    server = []
    for target, dest in TARGETS:
        for c in CASES:
            price = float(re.sub(r"[^0-9.]", "", c["price"]))
            r = landed_total({"source": c["source"], "currency": c["currency"], "parsed_price_numeric": price,
                              "category": c["category"], "title_raw": c["title"]}, target, dest, rules, rates)
            server.append(r["total"] if r else None)
    assert server == page
