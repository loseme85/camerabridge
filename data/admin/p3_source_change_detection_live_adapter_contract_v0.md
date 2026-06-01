# P3-SOURCE-CHANGE-DETECTION-LIVE-ADAPTER-CONTRACT

## 1. 작업명
P3-SOURCE-CHANGE-DETECTION-LIVE-ADAPTER-CONTRACT

## 2. 작업 목적
raw crawler output과 source_change_detection.py 사이의 안전한 adapter contract를 정의한다.

## 3. 구현 요약
- raw fetch / raw listing 최소 스키마를 정의했다.
- adapted snapshot / listing row mapping 규칙과 failure policy를 정의했다.
- source adapter readiness matrix와 scenario validation을 함께 생성했다.

## 4. Live Adapter Contract Scope
- this round is contract only
- no live crawl
- no production crawler edits
- no cron or source selector integration

## 5. Raw Fetch Schema
- fetch status, anti-bot, parser status, parse confidence, raw-html-presence flag, source-url fingerprint를 포함한다.
- raw HTML/source URL string은 저장하지 않는다.

## 6. Raw Listing Schema
- listing identity, title preview, price preview, availability preview, source_published_at preview, seller preview, image fingerprint preview를 포함한다.
- raw listing URL/image URL string은 저장하지 않는다.

## 7. Source Change Detection Input Mapping
- adapted snapshot fields align to compare_source_snapshots/create_change_set input expectations.
- adapted listing rows keep raw_url_present=false and deterministic fingerprints.

## 8. Fingerprint / Page Hash Rules
- title normalization is limited to whitespace/case/basic punctuation cleanup.
- page hash uses sorted listing fingerprints to reduce order-only false positives.

## 9. Availability / Price / Date Mapping Rules
- availability covers available/reserved/sold/unavailable/unknown.
- POA/call-for-price maps to price_unknown without hard failure.
- source_published_at may be null; first_seen_at stays separate.

## 10. Source Adapter Profiles
- Map Camera: readiness=ready_for_fixture_mapping | anti_bot=low
- Fujiya Camera: readiness=ready_for_fixture_mapping | anti_bot=low
- Leica Store Miami: readiness=ready_for_fixture_mapping | anti_bot=low
- Ffordes: readiness=ready_for_fixture_mapping | anti_bot=low
- MPB US: readiness=ready_for_fixture_mapping | anti_bot=low
- MPB UK/EU: readiness=needs_selector_audit | anti_bot=low
- KEH: readiness=needs_selector_audit | anti_bot=low
- 라이카스토어 충무로: readiness=needs_sample_html | anti_bot=medium
- 사진집: readiness=needs_sample_html | anti_bot=medium
- 장씨카메라: readiness=source_list_followup_needed | anti_bot=medium
- Mercari Japan: readiness=blocked_by_anti_bot | anti_bot=high

## 11. Source Adapter Readiness Matrix
- Map Camera: ready_for_fixture_mapping | live=candidate_after_sample_validation | next=P3-SOURCE-CHANGE-DETECTION-LIVE-ADAPTER-IMPLEMENTATION
- Fujiya Camera: ready_for_fixture_mapping | live=candidate_after_sample_validation | next=P3-SOURCE-CHANGE-DETECTION-LIVE-ADAPTER-IMPLEMENTATION
- Leica Store Miami: ready_for_fixture_mapping | live=candidate_after_sample_validation | next=P3-SOURCE-CHANGE-DETECTION-LIVE-ADAPTER-IMPLEMENTATION
- Ffordes: ready_for_fixture_mapping | live=candidate_after_sample_validation | next=P3-SOURCE-CHANGE-DETECTION-LIVE-ADAPTER-IMPLEMENTATION
- MPB US: ready_for_fixture_mapping | live=candidate_after_sample_validation | next=P3-SOURCE-CHANGE-DETECTION-LIVE-ADAPTER-IMPLEMENTATION
- MPB UK/EU: needs_selector_audit | live=needs_followup | next=selector_audit_read_only
- KEH: needs_selector_audit | live=needs_followup | next=selector_audit_read_only
- 라이카스토어 충무로: needs_sample_html | live=needs_followup | next=collect_sample_html_read_only
- 사진집: needs_sample_html | live=needs_followup | next=collect_sample_html_read_only
- 장씨카메라: source_list_followup_needed | live=needs_followup | next=source_profile_followup
- Mercari Japan: blocked_by_anti_bot | live=blocked | next=defer_or_drop_from_mvp

## 12. Adapter Failure Policy
- failed_fetch: allow_source_change=False | next=no_source_change_detection_call
- blocked_by_anti_bot: allow_source_change=False | next=no_source_change_detection_call
- parse_failed: allow_source_change=False | next=manual_review_queue
- partial_parse: allow_source_change=True | next=source_change_detection_low_confidence_only
- missing_required_fields: allow_source_change=True | next=reject_listing_row
- price_parse_failed: allow_source_change=True | next=source_change_detection_with_price_unknown
- availability_unknown: allow_source_change=True | next=source_change_detection_with_unknown_availability
- duplicate_raw_listing: allow_source_change=True | next=dedupe_before_source_change_detection
- unsupported_source: allow_source_change=False | next=drop_source_from_mvp

## 13. Scenario Validation 결과
- map_camera_success / Map Camera: status=pass | adapter=success | listing_rows=2
- fujiya_success / Fujiya Camera: status=pass | adapter=success | listing_rows=1
- leica_store_miami_missing_published / Leica Store Miami: status=pass | adapter=success | listing_rows=1
- ffordes_poa / Ffordes: status=pass | adapter=success | listing_rows=1
- mpb_sold / MPB US: status=pass | adapter=success | listing_rows=1
- kr_source_parse / 사진집: status=pass | adapter=success | listing_rows=1
- missing_url_but_source_listing_id / Map Camera: status=pass | adapter=success | listing_rows=1
- missing_identity / Map Camera: status=pass | adapter=partial_success | listing_rows=0
- mercari_anti_bot / Mercari Japan: status=pass | adapter=blocked_by_anti_bot | listing_rows=0
- parse_failed_source / KEH: status=pass | adapter=parse_failed | listing_rows=0
- raw_url_policy_violation / Fujiya Camera: status=pass | adapter=partial_success | listing_rows=0
- duplicate_raw_rows / MPB US: status=pass | adapter=partial_success | listing_rows=1
- page_hash_unchanged / Map Camera: status=pass | adapter=success | listing_rows=2

## 14. source_change_detection.py Compatibility
- adapted snapshots and listing rows were checked against source_change_detection.py-compatible shape assumptions.

## 15. Raw URL / HTML / Privacy Guard
- raw URL strings are never stored.
- raw HTML is tracked only as a presence flag.
- raw image URL strings are never stored.

## 16. Output JSON / Production Code 미수정 여부
- contract artifact only; no production crawler/search/frontend/auth/provider code was modified.

## 17. 테스트 결과
- schema, mapping, fingerprint, page hash, availability, price, readiness, anti-bot, duplicate, privacy guard checks included.

## 18. 남은 위험
- real selector stability, source-specific HTML variance, anti-bot exposure, and persistence remain outside this contract round.

## 19. 다음 Backlog 후보
- P3-CRAWL-FRESHNESS-SCHEDULER-CRON-CONTRACT
- P3-PERSISTENT-ALERT-STORAGE-IMPLEMENTATION-CONTRACT
- P3-SOURCE-CHANGE-DETECTION-LIVE-ADAPTER-IMPLEMENTATION
- P3-ALERT-MVP-LANDING-PAGE-COPY-IMPLEMENTATION
- P3-PRIVATE-BETA-RUNBOOK
