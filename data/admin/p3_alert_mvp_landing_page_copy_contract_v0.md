# P3-ALERT-MVP-LANDING-PAGE-COPY-CONTRACT

## 1. 작업명
- P3-ALERT-MVP-LANDING-PAGE-COPY-CONTRACT

## 2. 작업 목적
- Camera Bridge by The Hinge의 초기 랜딩페이지 메시지, CTA, 신뢰 문구, no-fake-result 원칙을 copy contract로 정의한다.

## 3. 구현 요약
- hero, problem, value proposition, how it works, rare alert, conditional rare, source-gap, trust, CTA, FAQ를 bilingual copy artifact로 만들었다.
- 금지 claim을 별도로 검증해서 과장/오해 가능성을 막았다.

## 4. landing page positioning 요약
- Camera Bridge는 단순 검색엔진이 아니라, 사용자의 수동 새로고침 습관을 대체하는 감시/알림 제품으로 설명한다.

## 5. hero copy variants
- hero variants: 4
- refresh replacement / rare Leica alert / no fake result / Camera Bridge by The Hinge framing을 포함

## 6. problem section
- 반복적인 딜러 확인, 빠르게 사라지는 매물, source 분산, 이름 불일치, noisy substitution 문제를 설명

## 7. value proposition section
- manual checking replacement, honest no-result, rare item vs rare opportunity, user-controlled alerts를 분리

## 8. how it works
- 검색 -> refinement -> 이메일 인증 -> 감지 시 알림의 4단계로 설명

## 9. rare alert section
- 35 lux aa, Noctilux 50 0.95, M6/MP, APO-Telyt-R 180 예시를 availability guarantee 없이 설명

## 10. conditional rare / smart deal section
- rare item과 rare opportunity를 구분하고, 가격/상태/지역/구성 조건이 맞을 때 smart deal로 설명

## 11. source-gap section
- exact-only policy, no fake fill, no adjacent substitution을 사용자 친화적으로 설명

## 12. no fake result / trust section
- no fake results, user control, email verification, no affiliation disclaimer, beta limitation 포함

## 13. CTA flow
- exact alert / source-gap / source expansion / refine / manual review unavailable / manage alerts CTA 포함

## 14. FAQ
- faq items: 10
- marketplace 여부, 속도, no listing, broad query, source-gap, pause/unsubscribe, privacy, affiliation 포함

## 15. claim safety validation
- prohibited absolute claims, affiliation overclaim, privacy overclaim을 별도 row로 점검

## 16. The Hinge / Camera Bridge positioning
- user-facing hero에서는 Camera Bridge by The Hinge 정도로만 노출하고, admin artifact에는 더 큰 company framing을 남긴다.

## 17. output JSON / production code 미수정 여부
- production frontend/search/crawler/classifier/parser/resolver/auth/db/provider 코드는 수정하지 않았다.

## 18. 테스트 결과
- script, tests, jsonl validation, py_compile, golden_set 기준으로 검증

## 19. 남은 위험
- 실제 landing implementation 단계에서 디자인 톤과 copy 밀도를 다시 조정할 필요가 있다.

## 20. 다음 backlog 후보
- P3-ALERT-MVP-LANDING-PAGE-COPY-IMPLEMENTATION
- P3-SOURCE-CHANGE-DETECTION-IMPLEMENTATION
- P3-FAST-ALERT-PATH-IMPLEMENTATION
- P3-CRAWL-FRESHNESS-SCHEDULER-IMPLEMENTATION
- P3-WATCH-BRIDGE-MARKET-SCOUT-CONTRACT
