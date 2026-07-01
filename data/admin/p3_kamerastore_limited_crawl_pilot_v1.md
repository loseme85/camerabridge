# P3 Kamerastore Limited Crawl Pilot v1

## Executive Summary

이번 라운드는 **Kamerastore만** 대상으로 한 scoped limited crawl pilot이다.

핵심 결과:

- Kamerastore 3페이지 제한 크롤 성공
- raw -> normalized -> resolved -> search index 반영 성공
- Kamerastore source는 검색 노출은 되지만 **price evidence에는 사용되지 않음**
- 기존 6개 active source count는 유지됨
- 기존 smoke query도 큰 회귀 없이 응답 유지

이번 라운드는 local pilot만 수행했고, **preview/prod 배포는 하지 않았다**.

최종 판단: **PASS**

## 수정 파일 목록

코드/설정:

- [app/test.py](/Users/changdaepark/Desktop/LEICA%20SEARCH/app/test.py)
- [api/search.py](/Users/changdaepark/Desktop/LEICA%20SEARCH/api/search.py)
- [data/config/source_registry_v1.json](/Users/changdaepark/Desktop/LEICA%20SEARCH/data/config/source_registry_v1.json)

보고서:

- [p3_kamerastore_limited_crawl_pilot_v1.md](/Users/changdaepark/Desktop/LEICA%20SEARCH/data/admin/p3_kamerastore_limited_crawl_pilot_v1.md)

이번 pilot 실행으로 갱신된 산출물:

- `data/raw/results.json`
- `data/normalized/normalized_latest.json`
- `data/derived/results_classified_v2.json`
- `data/derived/results_resolved_v2.json`
- `data/derived/results_search_index_v1.json`
- `data/derived/override_report.json`

## source_registry 변경 여부

Kamerastore 항목을 pilot 상태에 맞춰 갱신했다.

- `status`: `audited` -> `limited_crawl`
- `seed_url`: Kamerastore 실제 search route로 조정
  - `https://kamerastore.com/en-int/search?q=leica&options%5Bprefix%5D=last`
- `price_evidence_policy`: **`blocked_initially` 유지**

## Kamerastore pagination 방식

이번 pilot은 registry 기준 `page_param` 방식으로 연결했다.

- page 1:
  - `https://kamerastore.com/en-int/search?q=leica&options%5Bprefix%5D=last`
- page 2+:
  - `&page=2`
  - `&page=3`

실제 HTML 확인 결과:

- `product-card` 기반 product grid 확인
- `a.pagination__link[aria-label="Next"]` 존재
- page 2 URL 예시:
  - `/en-int/search?options%5Bprefix%5D=last&page=2&q=leica`

즉, Kamerastore는 현재 구조에서 **기존 page_param 패턴을 재사용 가능한 source**로 확인됐다.

## max_pages 설정

- pilot 실행값: **3**
- 상한 정책: **5 이하**
- 이번 실제 실행: **3페이지**

## 수집된 Kamerastore item count

### Before

- raw total: `7961`
- resolved total: `7919`
- search index total: `7919`
- Kamerastore rows:
  - raw: `0`
  - resolved: `0`
  - index: `0`

### After

- raw total: `8067`
- normalized total: `8067`
- resolved total: `8067`
- search index total: `8067`
- Kamerastore rows:
  - raw: `106`
  - normalized: `106`
  - resolved: `106`
  - index: `106`

## raw / normalized / resolved / index 반영 여부

| stage | total | Kamerastore count | result |
|---|---:|---:|---|
| raw | 8067 | 106 | PASS |
| normalized | 8067 | 106 | PASS |
| resolved | 8067 | 106 | PASS |
| search index | 8067 | 106 | PASS |

## 기존 6개 source regression 결과

기존 active source count는 비정상 감소 없이 유지됐다.

### Before

- 장씨카메라: `3976`
- 라이카스토어 충무로: `3291`
- 사진집: `480`
- Ffordes (영국): `129`
- Leica Store Miami: `45`
- 기타무라 (일본): `40`

### After

- 장씨카메라: `3976`
- 라이카스토어 충무로: `3291`
- 사진집: `480`
- Ffordes (영국): `129`
- Leica Store Miami: `45`
- 기타무라 (일본): `40`
- Kamerastore: `106`

즉, 이번 구현은 기존 source를 줄이지 않고 Kamerastore만 추가했다.

또한 `--site Kamerastore` 실행 시 기존 `results.json`을 전부 덮어쓰지 않도록, **site-filter merge**를 넣어 다른 source rows를 보존했다.

## price_evidence_policy가 blocked_initially로 유지되는지

유지됨.

registry:

- Kamerastore `price_evidence_policy = blocked_initially`

runtime:

- `api/search.py` price evidence pool에서 source registry를 읽어
  - `blocked_initially`
  - `sold_reference_only`
  source는 price evidence pool에서 제외하도록 처리했다.

## Kamerastore가 price evidence에 사용되지 않았는지

대표 query:

- `Leica 50mm f2 Summicron-M Type IV`

결과:

- Kamerastore row가 상단 visible cluster에 노출됨
- 하지만 `used_for_price = False`
- 표시 문구:
  - `Not used — Current source is not price-eligible yet`
- `price_scope = broader_model_family`
- `price_summary_allowed = False`

즉, **검색 노출/discovery는 가능하지만 exact/base price evidence에는 사용되지 않았다.**

## API 검증 예시

local meta:

- `meta.index_record_count = 8067`
- `meta.index_generated_at = 2026-06-30T14:52:36.264206+00:00`
- `meta.index_source_path = /Users/changdaepark/Desktop/LEICA SEARCH/data/derived/results_resolved_v2.json`

Kamerastore visibility example:

- query: `Leica 50mm f2 Summicron-M Type IV`
- top visible rows:
  - Kamerastore / Leica 50mm f2 Summicron-M (Type IV) (Black, 11819)
  - Kamerastore / Leica 50mm f2 Summicron-M (Type V) (Black, 11826 / 11719)
  - Kamerastore / Leica 50mm f2 Summicron (Type II, Dual Range) ...
- all visible Kamerastore rows:
  - `used_for_price = False`
  - `price_usage_label = Not used — Current source is not price-eligible yet`

## 기존 query smoke

| query | result |
|---|---|
| `Leica M10` | PASS - `price_scope = exact_base_model`, 기존 source 결과 유지 |
| `Leica M11-P` | PASS - `price_scope = exact_base_model`, body query 유지 |
| `Leica 50 Summicron Rigid` | PASS - `price_scope = insufficient_exact_data`, 기존 locked behavior 유지 |
| `Leica Noctilux 0.95` | PASS - `price_scope = insufficient_exact_data`, 기존 conservative behavior 유지 |

## 링크 생존성 샘플 결과

Kamerastore source URL 표본 10개를 read-only로 확인했다.

결과:

- sample size: `10`
- alive: `0`
- redirected: `0`
- timeout: `10`

해석:

- 이번 환경에서는 Kamerastore detail URL sample이 모두 timeout으로 떨어졌다.
- crawler/listing 수집 자체는 정상 동작했지만, direct detail URL health는 이번 샘플 기준 **추가 확인 필요**다.
- 링크 삭제로 단정하지는 않고, **network/timeout pending**으로 유지한다.

## 구현 메모

### app/test.py

- Kamerastore 전용 최소 wrapper 추가
- registry seed URL 사용
- page_param pagination 사용
- max_pages=3 pilot 실행
- `--site Kamerastore` 시 기존 source rows를 유지하도록 site-filter merge 추가
- Kamerastore condition badge를 `Certified / Restored / Not Passed` 같은 짧은 값으로 정리

### api/search.py

- source registry 로더 추가
- price evidence pool에서 source policy 확인
- `blocked_initially` source는 exact/base/broader price evidence pool에서 제외

## 다음 단계 제안

1. Kamerastore limited crawl을 1~2회 더 반복해서 selector 안정성 재확인
2. 링크 생존성은 timeout 원인만 별도 audit
3. price evidence는 계속 `blocked_initially`
4. 다음 승급 전 확인 항목:
   - product URL 안정성
   - sold/available 상태 품질
   - currency/localization 일관성
   - duplicate profile

그 다음에만:

- `limited_crawl -> active_source` 검토
- 그 이후에야 `price_eligible` 검토

## Final Judgment

판정 기준 대비:

- Kamerastore 3페이지 제한 크롤 성공: PASS
- raw/normalized/resolved/index 반영 성공: PASS
- price evidence에는 사용되지 않음: PASS
- 기존 source regression 없음: PASS

최종 판단: **PASS**

### Remaining Notes

- Kamerastore detail URL sample 10개는 모두 timeout이라 link survival은 별도 pending
- preview/prod 배포는 이번 라운드에서 하지 않았으므로, preview latest index meta는 기존 배포 상태를 유지한다
- commit/push는 이번 라운드에서 수행하지 않았다
