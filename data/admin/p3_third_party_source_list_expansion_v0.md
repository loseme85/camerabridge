# P3-THIRD-PARTY-SOURCE-LIST-EXPANSION

## 1. 작업명
- P3-THIRD-PARTY-SOURCE-LIST-EXPANSION

## 2. 작업 목적
- live crawl 없이 current source matrix와 public candidate list를 바탕으로 source expansion priority matrix를 planning artifact로 정리

## 3. 입력 파일/참조 파일
- `/Users/changdaepark/Desktop/LEICA SEARCH/data/admin/source_capability_matrix_v0.json`
- `/Users/changdaepark/Desktop/LEICA SEARCH/data/admin/p3_third_party_source_selector_implementation_v0.md`
- `/Users/changdaepark/Desktop/LEICA SEARCH/data/admin/p3_third_party_source_selector_implementation_v0.jsonl`
- `source_coverage_contract.py`
- `data/raw/results.json`
- `data/normalized/normalized_latest.json`
- `data/derived/results_search_index_v1.json`
- `crawler/logs/crawl_log.txt`

## 4. 현재 source capability matrix 요약
- current source count: `6`
- suspected_gap distribution: `{'selector_miss_possible': 4, 'source_list_gap_possible': 1, 'insufficient_evidence': 1}`
- `장씨카메라` -> third_party_l_mount_hits=1, sigma_hits=1, panasonic_lumix_hits=0, has_sigma_24_70=False, has_sigma_30mm=False, has_panasonic_24_105=False, has_sigma_14_24=False, suspected_gap=selector_miss_possible
- `라이카스토어 충무로` -> third_party_l_mount_hits=21, sigma_hits=24, panasonic_lumix_hits=3, has_sigma_24_70=True, has_sigma_30mm=False, has_panasonic_24_105=True, has_sigma_14_24=False, suspected_gap=selector_miss_possible
- `사진집` -> third_party_l_mount_hits=3, sigma_hits=3, panasonic_lumix_hits=1, has_sigma_24_70=False, has_sigma_30mm=True, has_panasonic_24_105=False, has_sigma_14_24=False, suspected_gap=selector_miss_possible
- `Ffordes (영국)` -> third_party_l_mount_hits=11, sigma_hits=10, panasonic_lumix_hits=6, has_sigma_24_70=False, has_sigma_30mm=False, has_panasonic_24_105=False, has_sigma_14_24=False, suspected_gap=selector_miss_possible
- `Leica Store Miami` -> third_party_l_mount_hits=0, sigma_hits=0, panasonic_lumix_hits=0, has_sigma_24_70=False, has_sigma_30mm=False, has_panasonic_24_105=False, has_sigma_14_24=False, suspected_gap=source_list_gap_possible
- `기타무라 (일본)` -> third_party_l_mount_hits=0, sigma_hits=0, panasonic_lumix_hits=0, has_sigma_24_70=False, has_sigma_30mm=False, has_panasonic_24_105=False, has_sigma_14_24=False, suspected_gap=insufficient_evidence

## 5. source expansion 필요성
- current active source mix는 Leica-specialized dealer 비중이 크고, Sigma 14-24 direct inventory는 아직 0이다.
- 이미 third-party L-mount positives는 들어오므로 next bottleneck은 search logic보다 source breadth와 source selector scope에 가깝다.

## 6. candidate source matrix 요약
- candidate source count: `31`
- priority distribution: `{'P1': 15, 'P2': 4, 'P3': 6, 'reject_or_later': 1, 'P0': 5}`
- `라이카스토어 충무로` (KR, leica_specialized_dealer) -> priority=P1, third_party_l_mount=medium, rare_leica=high, sigma14_24=medium, complexity=medium, risk=low
- `사진집` (KR, used_camera_dealer) -> priority=P1, third_party_l_mount=medium, rare_leica=medium, sigma14_24=medium, complexity=medium, risk=low
- `장씨카메라` (KR, used_camera_dealer) -> priority=P1, third_party_l_mount=low, rare_leica=medium, sigma14_24=low, complexity=medium, risk=low
- `Map Camera` (JP, used_camera_dealer) -> priority=P0, third_party_l_mount=high, rare_leica=high, sigma14_24=high, complexity=medium, risk=medium
- `Kitamura` (JP, used_camera_dealer) -> priority=P1, third_party_l_mount=medium, rare_leica=medium, sigma14_24=medium, complexity=medium, risk=medium
- `Fujiya Camera` (JP, used_camera_dealer) -> priority=P0, third_party_l_mount=high, rare_leica=high, sigma14_24=high, complexity=medium, risk=medium
- `Lemonsha` (JP, used_camera_dealer) -> priority=P1, third_party_l_mount=low, rare_leica=high, sigma14_24=low, complexity=medium, risk=medium
- `Camera no Naniwa` (JP, used_camera_dealer) -> priority=P1, third_party_l_mount=medium, rare_leica=medium, sigma14_24=medium, complexity=medium, risk=medium
- `Leica Store Miami` (US, leica_specialized_dealer) -> priority=P1, third_party_l_mount=low, rare_leica=high, sigma14_24=low, complexity=medium, risk=low
- `KEH` (US, used_camera_dealer) -> priority=P0, third_party_l_mount=high, rare_leica=medium, sigma14_24=high, complexity=medium, risk=medium
- `MPB US` (US, used_camera_dealer) -> priority=P0, third_party_l_mount=high, rare_leica=medium, sigma14_24=high, complexity=medium, risk=medium
- `B&H Used` (US, used_camera_dealer) -> priority=P1, third_party_l_mount=medium, rare_leica=low, sigma14_24=medium, complexity=medium, risk=medium
- `Adorama Used` (US, used_camera_dealer) -> priority=P1, third_party_l_mount=medium, rare_leica=low, sigma14_24=medium, complexity=medium, risk=medium
- `UsedPhotoPro / Roberts Camera` (US, used_camera_dealer) -> priority=P1, third_party_l_mount=medium, rare_leica=medium, sigma14_24=medium, complexity=medium, risk=medium
- `Ffordes` (UK, used_camera_dealer) -> priority=P1, third_party_l_mount=medium, rare_leica=high, sigma14_24=medium, complexity=medium, risk=low
- `MPB UK/EU` (EU, used_camera_dealer) -> priority=P0, third_party_l_mount=high, rare_leica=medium, sigma14_24=high, complexity=medium, risk=medium
- `Red Dot Cameras` (UK, leica_specialized_dealer) -> priority=P1, third_party_l_mount=low, rare_leica=high, sigma14_24=low, complexity=medium, risk=low
- `Meister Camera` (EU, leica_specialized_dealer) -> priority=P1, third_party_l_mount=low, rare_leica=high, sigma14_24=low, complexity=medium, risk=medium
- `Leica Store Austria used pages` (EU, leica_specialized_dealer) -> priority=P1, third_party_l_mount=low, rare_leica=high, sigma14_24=low, complexity=medium, risk=medium
- `Kamerastore` (EU, used_camera_dealer) -> priority=P1, third_party_l_mount=medium, rare_leica=medium, sigma14_24=medium, complexity=medium, risk=low

## 7. region별 후보 요약
- `EU` -> candidates=5, P0=1, P1=3, high_third_party=1, high_rare_leica=3, high_risk=0, shortlist=['MPB UK/EU', 'Meister Camera', 'Leica Store Austria used pages', 'Kamerastore']
- `Global` -> candidates=3, P0=0, P1=0, high_third_party=2, high_rare_leica=2, high_risk=2, shortlist=[]
- `JP` -> candidates=7, P0=2, P1=3, high_third_party=4, high_rare_leica=4, high_risk=2, shortlist=['Map Camera', 'Kitamura', 'Fujiya Camera', 'Lemonsha', 'Camera no Naniwa']
- `KR` -> candidates=8, P0=0, P1=3, high_third_party=2, high_rare_leica=1, high_risk=3, shortlist=['라이카스토어 충무로', '사진집', '장씨카메라']
- `UK` -> candidates=2, P0=0, P1=2, high_third_party=0, high_rare_leica=2, high_risk=0, shortlist=['Ffordes', 'Red Dot Cameras']
- `US` -> candidates=6, P0=2, P1=4, high_third_party=2, high_rare_leica=1, high_risk=0, shortlist=['Leica Store Miami', 'KEH', 'MPB US', 'B&H Used', 'Adorama Used', 'UsedPhotoPro / Roberts Camera']

## 8. P0/P1 추천 source
- `라이카스토어 충무로` -> P1 / already active in the current source mix; prioritize selector/scope follow-up over net-new source expansion / follow-up: treat as current-source optimization work rather than first-wave source-list expansion
- `사진집` -> P1 / already active in the current source mix; prioritize selector/scope follow-up over net-new source expansion / follow-up: treat as current-source optimization work rather than first-wave source-list expansion
- `장씨카메라` -> P1 / already active in the current source mix; prioritize selector/scope follow-up over net-new source expansion / follow-up: treat as current-source optimization work rather than first-wave source-list expansion
- `Map Camera` -> P0 / strong net-new dealer-style source for third-party L-mount coverage with manageable implementation risk / follow-up: prepare a source-specific adapter feasibility spike without changing runtime ranking
- `Kitamura` -> P1 / good coverage value with some implementation or policy uncertainty / follow-up: keep in the first expansion wave after P0 sources
- `Fujiya Camera` -> P0 / strong net-new dealer-style source for third-party L-mount coverage with manageable implementation risk / follow-up: prepare a source-specific adapter feasibility spike without changing runtime ranking
- `Lemonsha` -> P1 / good coverage value with some implementation or policy uncertainty / follow-up: keep in the first expansion wave after P0 sources
- `Camera no Naniwa` -> P1 / good coverage value with some implementation or policy uncertainty / follow-up: keep in the first expansion wave after P0 sources
- `Leica Store Miami` -> P1 / already active in the current source mix; prioritize selector/scope follow-up over net-new source expansion / follow-up: treat as current-source optimization work rather than first-wave source-list expansion
- `KEH` -> P0 / strong net-new dealer-style source for third-party L-mount coverage with manageable implementation risk / follow-up: prepare a source-specific adapter feasibility spike without changing runtime ranking
- `MPB US` -> P0 / strong net-new dealer-style source for third-party L-mount coverage with manageable implementation risk / follow-up: prepare a source-specific adapter feasibility spike without changing runtime ranking
- `B&H Used` -> P1 / good coverage value with some implementation or policy uncertainty / follow-up: keep in the first expansion wave after P0 sources
- `Adorama Used` -> P1 / good coverage value with some implementation or policy uncertainty / follow-up: keep in the first expansion wave after P0 sources
- `UsedPhotoPro / Roberts Camera` -> P1 / good coverage value with some implementation or policy uncertainty / follow-up: keep in the first expansion wave after P0 sources
- `Ffordes` -> P1 / good coverage value with some implementation or policy uncertainty / follow-up: keep in the first expansion wave after P0 sources
- `MPB UK/EU` -> P0 / strong net-new dealer-style source for third-party L-mount coverage with manageable implementation risk / follow-up: prepare a source-specific adapter feasibility spike without changing runtime ranking
- `Red Dot Cameras` -> P1 / good coverage value with some implementation or policy uncertainty / follow-up: keep in the first expansion wave after P0 sources
- `Meister Camera` -> P1 / good coverage value with some implementation or policy uncertainty / follow-up: keep in the first expansion wave after P0 sources
- `Leica Store Austria used pages` -> P1 / good coverage value with some implementation or policy uncertainty / follow-up: keep in the first expansion wave after P0 sources
- `Kamerastore` -> P1 / good coverage value with some implementation or policy uncertainty / follow-up: keep in the first expansion wave after P0 sources

## 9. reject/later source와 이유
- `당근마켓` -> policy/anti-bot risk is too high for near-term MVP expansion

## 10. source risk summary
- `anti_bot_or_policy` -> distribution={'low': 7, 'unknown': 1, 'medium': 16, 'high': 6, 'very_high': 1}, highest_risk_sources=['중고나라', '번개장터', '당근마켓', 'Yahoo Auctions Japan', 'Mercari Japan', 'eBay', 'Buyee proxy-visible listings']
- `adapter_complexity` -> distribution={'medium': 20, 'high': 4, 'very_high': 7}, highest_risk_sources=['충무로/남대문 중고카메라 딜러 후보', 'SLR클럽 장터', '중고나라', '번개장터', '당근마켓', 'Yahoo Auctions Japan', 'Mercari Japan', 'Wetzlar Camera Auctions', 'eBay', 'Buyee proxy-visible listings', 'Catawiki']
- `sold_status_quality` -> distribution={'good': 11, 'partial': 15, 'unknown': 1, 'poor': 4}, highest_risk_sources=[]

## 11. Sigma 14-24 / third-party L-mount coverage 관점 요약
- Sigma 14-24는 단일 제품 문제라기보다 broader used-camera dealer / MPB/KEH/JP used dealer 계열 source를 추가해야 줄어들 가능성이 높다.
- Leica-only / Leica-heavy boutique source는 rare Leica alert에는 좋지만, Sigma DG DN Art wide zoom 공백을 메우는 힘은 제한적이다.

## 12. rare Leica alert MVP 관점 요약
- rare Leica alert MVP에는 Leica-heavy source가 여전히 중요하다.
- 다만 price guide와 third-party L-mount alert까지 함께 보려면 `KEH`, `MPB`, `Map Camera`, `Fujiya Camera` 같은 broader used-camera dealer를 먼저 보는 편이 효율적이다.

## 13. implementation backlog proposal
- `P3-THIRD-PARTY-SOURCE-LIST-EXPANSION-IMPLEMENTATION`: P0/P1 shortlist에 대해 adapter feasibility spike만 진행
- `P3-THIRD-PARTY-SOURCE-CAPABILITY-DASHBOARD`: current source vs candidate source를 region/type/risk로 보는 admin artifact
- `P3-ALERT-MVP-QUERY-WATCHLIST`: Sigma/Panasonic/Lumix L-mount + rare Leica watchlist를 source expansion priority와 연결

## 14. 수정 파일 목록
- `scripts/run_p3_third_party_source_list_expansion.py`
- `data/admin/p3_third_party_source_list_expansion_v0.md`
- `data/admin/p3_third_party_source_list_expansion_v0.jsonl`
- `data/admin/source_candidate_matrix_v0.json`

## 15. 수정하지 않은 파일/영역
- production code 전반
- crawler selector production code
- output JSON / taxonomy seed / canonical index / raw data / search index

## 16. 테스트/검증 결과
- script run / JSON validation / py_compile / selector implementation test / golden set recorded separately

## 17. 다음 backlog 후보
- `P3-THIRD-PARTY-SOURCE-LIST-EXPANSION-IMPLEMENTATION`
- `P3-THIRD-PARTY-SOURCE-CAPABILITY-DASHBOARD`
- `P3-ALERT-MVP-QUERY-WATCHLIST`
- `P3-DIVERSITY-AWARE-RANKING`
- `P3-ACCESSORY-SUBTYPE-PRECISION`
