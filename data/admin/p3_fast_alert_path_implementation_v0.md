# P3-FAST-ALERT-PATH-IMPLEMENTATION

## 작업 목적
- source change candidate를 fast alert queue candidate 또는 blocked candidate preview로 분기

## 구현 요약
- `fast_alert_path.py`는 lightweight normalization, watchlist match, condition evaluation, subscription guard, confidence guard를 거쳐 queue/blocked 결과를 만듭니다.
- 실제 queue worker나 provider send 없이 downstream-compatible preview만 생성합니다.

## fast_alert_path.py public API
- `normalize_candidate_lightweight`
- `match_watch_target`
- `evaluate_condition_match`
- `evaluate_confidence_guard`
- `evaluate_subscription_guard`
- `create_fast_alert_queue_candidate`
- `create_blocked_fast_alert_candidate`
- `process_fast_alert_candidate`
- `process_fast_alert_batch`

## 결과 요약
- queue events: `{'rare_new_listing': 2, 'price_drop': 1, 'source_gap_resolved': 1, 'source_expansion_available': 1, 'conditional_rare_match': 1, 'smart_deal_match': 1}`
- blocked reasons: `{'condition_not_met': 1, 'common_watch_digest_only': 2, 'fake_fill_detected': 2, 'broad_query_refinement_required': 3, 'manual_review_required': 1, 'sold_or_removed': 2, 'duplicate_listing': 2, 'anti_bot_guard': 1, 'missing_verified_subscription': 1, 'email_suppressed': 1}`
- scenario pass: `22/22`
