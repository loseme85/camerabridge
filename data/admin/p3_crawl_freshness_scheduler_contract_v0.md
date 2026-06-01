# P3-CRAWL-FRESHNESS-SCHEDULER-CONTRACT

## 작업 목적
- 사용자 수요, 희귀도, source health, anti-ban risk를 함께 반영하는 freshness scheduler contract를 정의한다.

## 구현 요약
- source profile / watch target profile / demand signal / source×watch priority matrix를 생성했다.
- true rare, source-gap, source-expansion, broad/manual-review를 서로 다른 crawl intent로 분리했다.
- anti-bot risk와 failure rate가 높으면 aggressive interval을 자동으로 제한한다.

## Interval Decision 분포
- fast: 2
- normal: 5
- paused: 4
- slow: 4
- very_fast: 2

## 수정 파일 목록
- crawl_freshness_scheduler_contract.py
- scripts/run_p3_crawl_freshness_scheduler_contract.py
- tests/test_crawl_freshness_scheduler_contract.py
- data/admin/p3_crawl_freshness_scheduler_contract_v0.md
- data/admin/p3_crawl_freshness_scheduler_contract_v0.jsonl
- data/admin/crawl_freshness_scheduler_contract_v0.json

## 수정하지 않은 파일/영역
- crawler production code / actual cron / GitHub Actions
- production search/parser/resolver code
- raw data / search index / output JSON / canonical index / taxonomy seed
