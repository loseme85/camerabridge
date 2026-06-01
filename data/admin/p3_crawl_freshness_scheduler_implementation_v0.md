# P3-CRAWL-FRESHNESS-SCHEDULER-IMPLEMENTATION

## 작업 목적
- source/watch/demand 입력만으로 crawl interval decision preview를 계산

## 구현 요약
- `crawl_freshness_scheduler.py`는 demand aggregation, rarity/health/anti-bot weighting, priority scoring, interval band assignment를 수행합니다.
- 실제 crawl이나 cron 변경 없이 source change detection이 다음 단계에서 사용할 schedule decision shape만 생성합니다.

## 결과 요약
- interval bands: `{'very_fast': 2, 'fast': 5, 'normal': 4, 'slow': 2, 'paused': 5}`
- intents: `{'alert_fast_path': 8, 'digest_refresh': 2, 'source_gap_monitor': 2, 'source_expansion_monitor': 2, 'paused_no_crawl': 3, 'manual_review_observation': 1}`
- scenario pass: `18/18`
