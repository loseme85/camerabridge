# P3-BROAD-QUERY-AMBIGUITY-UI-IMPLEMENTATION

## 1. 작업 목적
- broad / ambiguous query에 대해 search ranking을 바꾸지 않고 top-level `ui_hints` metadata를 API response에 추가
- 프론트가 refinement chip / selector / no-result alert UI를 바로 구성할 수 있는 계약을 구현

## 2. 구현 요약
- 새 순수 모듈 `search_ui_hints.py` 추가
- `api.search.search_from_params()` 성공 response에 additive field `ui_hints`를 부착
- ranking, filtering, pagination, result ordering은 변경하지 않음

## 3. 추가된 response metadata contract
```json
{
  "ui_hints": {
    "needs_disambiguation": true,
    "ambiguity_type": "focal_short_alias",
    "recommended_ui_pattern": "mount_selector",
    "recommended_chips": [
      "M 50 Summicron",
      "R 50 Summicron",
      "SL 50 Summicron",
      "Show all 50mm"
    ],
    "suggested_filters": {
      "category": [
        "Lens"
      ],
      "mount": [
        "M",
        "R",
        "SL"
      ],
      "focal_length": [
        "50mm"
      ],
      "family": [
        "Summicron",
        "Summicron-M",
        "Summicron-R",
        "Summicron-SL",
        "APO-Summicron-SL"
      ]
    },
    "hard_pin_allowed": false,
    "recommended_message": "50 cron can refer to M, R, or SL 50mm Summicron families. Choose a mount to refine.",
    "policy_version": "p3_broad_query_ambiguity_ui_v0"
  }
}
```

## 4. metadata field 정의
- `needs_disambiguation`: UI refinement가 필요한지 여부
- `ambiguity_type`: broad/short/source-gap 타입 분류
- `recommended_ui_pattern`: refinement_chips / mount_selector / family_selector / accessory_subtype_selector / no_result_alert_signup / no_disambiguation_needed
- `recommended_chips`: 프론트가 바로 그릴 수 있는 chip 후보 목록
- `suggested_filters`: 카테고리/마운트/focal/family/accessory subtype 등 추천 필터
- `hard_pin_allowed`: query를 특정 family로 강하게 고정해도 되는지 여부
- `recommended_message`: 프론트에 노출 가능한 helper message
- `policy_version`: 현재 policy spec 버전

## 5. query group별 metadata 예시
- `broad_family_alias`: `summicron` -> `broad_family_alias` / `refinement_chips`
- `bare_short_alias`: `cron` -> `short_alias_bare` / `family_selector`
- `focal_short_alias`: `50 cron` -> `focal_short_alias` / `mount_selector`
- `broad_r_query`: `leica r` -> `broad_mount_alias` / `family_selector`
- `broad_accessory_query`: `leica cap` -> `broad_accessory_alias` / `accessory_subtype_selector`
- `source_coverage_gap`: `sigma 14-24 l` -> `source_coverage_gap` / `no_result_alert_signup`
- `specific_guardrail`: `m 50 cron` -> `none` / `no_disambiguation_needed`

## 6. 수정 파일 목록
- `search_ui_hints.py`
- `api/search.py`
- `tests/test_broad_query_ambiguity_ui_implementation.py`
- `data/admin/p3_broad_query_ambiguity_ui_implementation_v0.md`
- `data/admin/p3_broad_query_ambiguity_ui_implementation_v0.jsonl`

## 7. 수정하지 않은 파일/영역
- `classifier_v2.py`
- `model_detector.py`
- `query_parser.py`
- `query_resolver.py`
- `search_service.py`
- `taxonomy seed / canonical index`
- `results.json`
- `data/normalized/normalized_latest.json`
- `data/sold_items.json`

## 8. ranking / result order 미변경 여부
- result order changed rows: `0`
- `ui_hints`는 endpoint top-level additive field만 추가했고, results ordering은 유지됨

## 9. output JSON / taxonomy seed / canonical index 미수정 여부
- output JSON 미수정
- taxonomy seed / canonical index 미수정
- search index write 없음

## 10. broad family alias metadata 결과
- `summicron` -> `broad_family_alias` / `refinement_chips` / chips=['M Lens', 'R Lens', 'SL Lens', 'LTM / L Lens']
- `summilux` -> `broad_family_alias` / `refinement_chips` / chips=['M Lens', 'R Lens', 'SL Lens', 'LTM / L Lens']
- `leica summicron` -> `broad_family_alias` / `refinement_chips` / chips=['M Lens', 'R Lens', 'SL Lens', 'LTM / L Lens']
- `leica summilux` -> `broad_family_alias` / `refinement_chips` / chips=['M Lens', 'R Lens', 'SL Lens', 'LTM / L Lens']

## 11. bare short alias metadata 결과
- `cron` -> `short_alias_bare` / `family_selector` / hard_pin_allowed=False
- `lux` -> `short_alias_bare` / `family_selector` / hard_pin_allowed=False

## 12. focal short alias metadata 결과
- `50 cron` -> `focal_short_alias` / `mount_selector` / needs_disambiguation=True
- `leica 50 cron` -> `focal_short_alias` / `mount_selector` / needs_disambiguation=True
- `35 lux` -> `focal_short_alias` / `no_disambiguation_needed` / needs_disambiguation=False
- `50 lux` -> `focal_short_alias` / `no_disambiguation_needed` / needs_disambiguation=False
- `leica 35 lux` -> `focal_short_alias` / `refinement_chips` / needs_disambiguation=True
- `leica 50 lux` -> `focal_short_alias` / `refinement_chips` / needs_disambiguation=True

## 13. broad R metadata 결과
- `leica r` -> `broad_mount_alias` / `family_selector`
- `r lens` -> `broad_mount_alias` / `family_selector`
- `r apo` -> `broad_mount_alias` / `family_selector`
- `r telyt` -> `broad_mount_alias` / `family_selector`
- `r vario` -> `broad_mount_alias` / `family_selector`

## 14. broad accessory metadata 결과
- `leica cap` -> `broad_accessory_alias` / `accessory_subtype_selector`
- `leica battery` -> `broad_accessory_alias` / `accessory_subtype_selector`
- `leica strap` -> `broad_accessory_alias` / `accessory_subtype_selector`
- `leica hood` -> `broad_accessory_alias` / `accessory_subtype_selector`
- `leica adapter` -> `broad_accessory_alias` / `accessory_subtype_selector`

## 15. source coverage gap metadata 결과
- `sigma 14-24 l` -> `source_coverage_gap` / `no_result_alert_signup` / chips=['Sigma L mount', 'Sigma 14-24', 'L mount wide zoom', 'Alert me']
- `sigma 14-24 l mount` -> `source_coverage_gap` / `no_result_alert_signup` / chips=['Sigma L mount', 'Sigma 14-24', 'L mount wide zoom', 'Alert me']
- `sigma 14-24 dg dn` -> `source_coverage_gap` / `no_result_alert_signup` / chips=['Sigma L mount', 'Sigma 14-24', 'L mount wide zoom', 'Alert me']
- `sigma 14-24 dg dn art` -> `source_coverage_gap` / `no_result_alert_signup` / chips=['Sigma L mount', 'Sigma 14-24', 'L mount wide zoom', 'Alert me']

## 16. specific guardrail metadata 결과
- `m 50 cron` -> `none` / `no_disambiguation_needed` / status=guardrail_pass
- `r 50 cron` -> `none` / `no_disambiguation_needed` / status=guardrail_pass
- `sl 50 cron` -> `none` / `no_disambiguation_needed` / status=guardrail_pass
- `m 35 lux` -> `none` / `no_disambiguation_needed` / status=guardrail_pass
- `m 50 lux` -> `none` / `no_disambiguation_needed` / status=guardrail_pass
- `leica sl2` -> `none` / `no_disambiguation_needed` / status=guardrail_pass
- `leica sl3` -> `none` / `no_disambiguation_needed` / status=guardrail_pass
- `sl3 battery` -> `none` / `no_disambiguation_needed` / status=guardrail_pass
- `leica handgrip` -> `none` / `no_disambiguation_needed` / status=guardrail_pass
- `panasonic 24-105 l` -> `none` / `no_disambiguation_needed` / status=guardrail_pass
- `lumix 24-105` -> `none` / `no_disambiguation_needed` / status=guardrail_pass

## 17. fallback behavior
- `random unrelated query` -> `none` / `no_disambiguation_needed` / needs_disambiguation=False`
- unknown query도 `ui_hints` object는 항상 존재하고, 안전한 no-op contract를 반환함

## 18. 테스트 결과
- total contract rows: `43`
- status counts: `{'pass': 32, 'guardrail_pass': 11}`
- actual ambiguity counts: `{'broad_family_alias': 4, 'short_alias_bare': 2, 'focal_short_alias': 6, 'broad_mount_alias': 5, 'broad_accessory_alias': 11, 'source_coverage_gap': 4, 'none': 11}`

## 19. 남은 위험
- 현재 `ui_hints`는 query-policy 중심이다. top3 diversity를 반영한 동적 hint 개선은 후속 구현이 더 적합하다.
- source coverage gap은 metadata로 안내만 가능하며, inventory/source 자체를 보강하지는 않는다.
- broad accessory subtype precision은 여전히 UI filter와 taxonomy follow-up이 필요하다.

## 20. 다음 backlog 후보
- `P3-DIVERSITY-AWARE-RANKING`
- `P3-THIRD-PARTY-SOURCE-COVERAGE`
- `P3-ACCESSORY-SUBTYPE-PRECISION`
- `P3-R-LENS-TAXONOMY-AUDIT`
- `P3-SL-ZOOM-FAMILY-TAXONOMY-AUDIT`
