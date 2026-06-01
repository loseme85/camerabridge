# P3-VERTICAL-DOMAIN-PACK-CONTRACT

## 작업 목적
- The Hinge Core와 vertical domain pack의 경계를 분리해 Camera Bridge를 첫 번째 reusable pack으로 정의한다.

## 구현 요약
- Core는 source monitoring, normalization interface, scheduler, alert lifecycle, queue, provider adapter 같은 domain-neutral 엔진만 갖는다.
- Camera-specific taxonomy, aliases, rarity, source rules, no-result copy는 Camera Bridge pack에만 남긴다.
- Watch / Parts / Audio / Moto / Collectibles future pack을 preview로 추가했다.

## Domain Pack Status 분포
- active_first_vertical: 1
- exploratory: 4
- planned: 1

## 수정 파일 목록
- vertical_domain_pack_contract.py
- scripts/run_p3_vertical_domain_pack_contract.py
- tests/test_vertical_domain_pack_contract.py
- data/admin/p3_vertical_domain_pack_contract_v0.md
- data/admin/p3_vertical_domain_pack_contract_v0.jsonl
- data/admin/vertical_domain_pack_contract_v0.json

## 수정하지 않은 파일/영역
- production search/crawler/classifier/parser/resolver code
- taxonomy seed / canonical index actual data
- raw data / search index / output JSON / frontend production code
