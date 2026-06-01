# Local-only Output Regeneration Entrypoint v0

## 1. 목적

- live crawl 없이 local raw data 기반으로 output regeneration path를 분리한다.
- stale output 문제를 hot patch 없이 해결할 수 있는 **official local-only entrypoint**를 만든다.
- 이번 라운드에서는 entrypoint와 dry-run 검증까지만 수행하고, target output 파일은 직접 덮어쓰지 않는다.

## 2. 확인한 기존 pipeline

- `app/test.py`의 `crawl_all()`
  - `data/raw/results.json`
  - `data/normalized/normalized_latest.json`
  - `data/sold_items.json`
  을 갱신하는 메인 경로다.
  - 하지만 live crawl, raw snapshot, derived outputs, session log 갱신까지 함께 묶여 있다.
- `final_resolution_pipeline.py`
  - `data/raw/results.json`을 입력으로 받아 `data/derived/results_classified_v2.json`, `data/derived/results_resolved_v2.json`, search index를 생성한다.
  - 이번 라운드의 target output set을 직접 쓰지는 않는다.
- root `results.json`
  - 현재 앱 템플릿은 주로 `data/raw/results.json`을 읽는다.
  - root `results.json`의 공식 writer는 crawl-bound 경로 바깥에서는 명확하지 않다.
  - 따라서 새 entrypoint에서는 **legacy mirror / opt-in overwrite**로 취급한다.

## 3. 새 entrypoint

- 생성한 파일:
  - `scripts/regenerate_outputs_from_raw.py`
- dry-run 명령:

```bash
python3 scripts/regenerate_outputs_from_raw.py --dry-run
```

- preview output 명령:

```bash
python3 scripts/regenerate_outputs_from_raw.py   --input data/raw/results.json   --output-dir data/regen_preview   --dry-run
```

- write 명령:

```bash
python3 scripts/regenerate_outputs_from_raw.py --write
```

- root `results.json`까지 명시적으로 쓰는 명령:

```bash
python3 scripts/regenerate_outputs_from_raw.py --write --write-root-results
```

- 입력/출력 옵션:
  - `--input`
  - `--results-path`
  - `--normalized-path`
  - `--sold-items-path`
  - `--output-dir`
  - `--dry-run`
  - `--write`
  - `--write-root-results`

## 4. schema 처리

### `results.json`

- 현재 `data/raw/results.json`과 거의 같은 row schema를 사용한다.
- 새 entrypoint는 raw row를 base로 삼고 current classifier 결과를 덮어써서 재생성한다.
- unknown field는 existing row가 있으면 보존한다.
- 다만 앱의 primary source가 아니고 공식 writer도 crawl-bound라서, root overwrite는 기본 비활성화다.

### `data/normalized/normalized_latest.json`

- 기존 normalized schema(`listing_id`, `source`, `source_url`, `title_raw`, `price`, `currency`, `label`, `mount`, `brand`, `category`, `condition_raw`, `is_sold`, `image`, `first_seen`, `crawl_time`)를 유지한다.
- current classifier 결과에서 `model_raw`, `model_canonical`, `variant`, `focal_length`, reason/confidence fields 등을 함께 넣는다.
- existing normalized row에만 있던 unknown field는 `listing_id/source_url` 기준으로 보존한다.

### `data/sold_items.json`

- sold 여부는 새로 판단하지 않는다.
- 기존 sold row의 `sold_at`, `hours_to_sell`, `is_sold` 같은 sold metadata는 그대로 보존한다.
- 분류 관련 field만 current classifier 기준으로 다시 계산한다.
- sold row 재분류 시 `is_sold` 또는 `sold_at`가 있으면 classifier 입력의 `품절=True`로 넘겨 sold lane 의미를 유지한다.

## 5. dry-run 결과

- 입력 raw row 수: `7869`
- existing `results.json` row 수: `7923`
- existing `normalized_latest.json` row 수: `7869`
- existing `sold_items.json` row 수: `500`

변경 예상량:

- `results.json`: `7869` / `7869` rows
- `data/normalized/normalized_latest.json`: `7869` / `7869` rows
- `data/sold_items.json`: `500` / `500` rows

대표 P1 title before/after:

| title | source file | before category | before label | before mount | after category | after label | after mount | after model_canonical | status | note |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `Used Leica Summicron-SL 35mm f/2 ASPH` | `data/normalized/normalized_latest.json` | `Accessory` | `-` | `Accessory` | `Lens` | `SL Lens` | `SL` | `Summicron-SL` | `would_change_on_regeneration` | normalized_latest/results remain stale Accessory; sold_items is already Lens. |
| `Used Leica APO-Summicron-SL 50mm f/2 ASPH` | `data/sold_items.json` | `Accessory` | `-` | `SL` | `Lens` | `SL Lens` | `SL` | `APO-Summicron` | `would_change_on_regeneration` | Current classifier keeps the title in Lens lane; stale sold output still marks it as Accessory. |
| `Leica 35mm F2 AsphSummicron SL` | `data/normalized/normalized_latest.json` | `Accessory` | `-` | `Accessory` | `Lens` | `M Lens` | `M` | `Summicron-M` | `needs_followup_after_regeneration` | Accessory drift is gone, but current classifier still leaves SL title on M mount/model. |
| `[중고] SL 14-24/2.8 Vario Elmarit ASPH (Black)` | `data/normalized/normalized_latest.json` | `Lens` | `24mm Elmarit ASPH` | `M` | `Lens` | `SL Lens` | `SL` | `Super-Vario-Elmarit-SL` | `would_change_on_regeneration` | Stored output still shows M-prime collapse; current classifier restores SL zoom family recall. |
| `[중고] SL 16-35/3.5-4.5 Super Vario Elmar ASPH (Black)` | `data/normalized/normalized_latest.json` | `Lens` | `Vario-SL` | `M` | `Lens` | `SL Lens` | `SL` | `Super-Vario-Elmar-SL` | `would_change_on_regeneration` | results.json still contains a stronger M-prime collapse variant; current classifier is correct. |
| `[위탁] SL 24-90/2.8-4 Vario Elmar ASPH (Black)` | `data/normalized/normalized_latest.json` | `Lens` | `24mm Elmar-M` | `SL` | `Lens` | `SL Lens` | `SL` | `Vario-Elmarit-SL` | `would_change_on_regeneration` | Current classifier preserves SL standard zoom recall; stored labels remain stale. |
| `[중고] SL APO Vario Elmarit 90-280 f/2.8-4` | `data/normalized/normalized_latest.json` | `Lens` | `Elmarit` | `M` | `Lens` | `SL Lens` | `SL` | `APO-Vario-Elmarit-SL` | `would_change_on_regeneration` | Stored rows still show generic label and M drift; current classifier is already correct. |
| `Leica SL2 Black` | `data/normalized/normalized_latest.json` | `Lens` | `Leica SL2` | `SL` | `Body` | `SL Body` | `SL` | `SL2` | `would_change_on_regeneration` | normalized_latest, results, and sold_items still show stale Lens rows; current classifier now returns Body. |
| `Leica SL3 Black` | `data/normalized/normalized_latest.json` | `Lens` | `Leica SL3` | `SL` | `Body` | `SL Body` | `SL` | `SL3` | `would_change_on_regeneration` | normalized_latest and results remain stale Lens rows; current classifier now returns Body. |
| `Leica Barnack IIIF Silver` | `data/normalized/normalized_latest.json` | `Lens` | `Leica Barnack` | `L` | `Body` | `L Body` | `L` | `IIIf` | `would_change_on_regeneration` | Current classifier already classifies Barnack IIIF as Body; stored rows are stale. |
| `Leica Barnack IIIg Silver` | `data/normalized/normalized_latest.json` | `Lens` | `Leica Barnack` | `L` | `Body` | `L Body` | `L` | `IIIg` | `would_change_on_regeneration` | Current classifier already classifies Barnack IIIg as Body; stored rows are stale. |
| `Leica R 180mm f3.4 APO-Telyt Black` | `data/normalized/normalized_latest.json` | `Lens` | `180mm APO-Telyt` | `M` | `Lens` | `R Lens` | `R` | `APO-Telyt-R` | `would_change_on_regeneration` | results.json still has blank label + M drift; current classifier returns R Lens. |
| `LEICA 180mm F3.4 APO-TELYT-R` | `current_classifier_only` | `-` | `-` | `-` | `Lens` | `R Lens` | `R` | `APO-Telyt-R` | `not_found_in_source_file` | Representative R tele title was not found in stored datasets but current classifier output is correct. |
| `[위탁] R 180/3.4 APO-Telyt (Black)` | `current_classifier_only` | `-` | `-` | `-` | `Lens` | `R Lens` | `R` | `APO-Telyt-R` | `not_found_in_source_file` | Representative Chungmuro-style R tele title was not found in stored datasets but current classifier output is correct. |
| `Leica 12549 Hood Silver [for M 50mm f2.8 Elmar]` | `data/normalized/normalized_latest.json` | `Lens` | `50mm Elmar f2.8` | `M` | `Accessory` | `Accessory` | `M` | `Elmar` | `would_change_on_regeneration` | Current classifier is already correct; stored output still promotes the hood as a lens. |
| `Leica 12475 Hood Black for M 50mm F1.2 Noctilux ASPH` | `data/normalized/normalized_latest.json` | `Lens` | `75mm Noctilux f1.25` | `M` | `Accessory` | `Accessory` | `M` | `Noctilux` | `would_change_on_regeneration` | Current classifier is already correct; stored output still collapses the hood into a lens family. |
| `Used Leica SL3 - Extra Battery` | `data/sold_items.json` | `Lens` | `-` | `SL` | `Accessory` | `Accessory` | `SL` | `SL3` | `would_change_on_regeneration` | Current classifier is already correct; sold output still leaves the battery in Lens lane. |
| `Used Leica Multifunctional Handgrip HG-SCL7 for SL3` | `data/sold_items.json` | `Lens` | `-` | `SL` | `Accessory` | `Accessory` | `SL` | `If` | `would_change_on_regeneration` | results.json is already Accessory but sold output is stale Lens; current classifier is correct. |

## 6. write safety

- 기본값은 dry-run이다.
- `--write` 없이는 target output 파일을 수정하지 않는다.
- `--output-dir`를 주면 target overwrite 없이 preview JSON들을 별도 위치에 쓸 수 있다.
- root `results.json`은 기본적으로 쓰지 않는다.
  - 이유: 앱의 primary source가 아니고, crawl-bound writer 외 공식 overwrite semantics가 불명확하기 때문이다.
  - root overwrite는 `--write-root-results`를 따로 줬을 때만 가능하다.

## 7. 남은 제한

- `sold_items.json`
  - 분류 필드 재생성은 안전하게 가능하다.
  - 하지만 sold inclusion 자체를 다시 판단하는 pipeline은 아니다.
- root `results.json`
  - legacy mirror 성격이 강하고 primary app source가 아니다.
  - overwrite는 opt-in으로만 열어둔다.
- raw input 부족 문제
  - `data/raw/results.json`에 없는 row는 재생성 대상에 포함되지 않는다.
  - 대표적으로 `LEICA 180mm F3.4 APO-TELYT-R`, `[위탁] R 180/3.4 APO-Telyt (Black)`는 current classifier smoke title로는 유효하지만 저장 산출물에 직접 대응 row가 없다.
- P1.1 후보
  - `Leica 35mm F2 AsphSummicron SL`은 regeneration 이후에도 `Lens / M Lens / Summicron-M / mount=M`이라서 별도 follow-up이 남는다.

## 8. 다음 추천 작업

현재 기준으로는 아래 순서가 가장 자연스럽다.

1. `python3 scripts/regenerate_outputs_from_raw.py --dry-run` 결과를 검수
2. preview가 괜찮으면 `--write`로 `normalized_latest.json`, `sold_items.json` 갱신
3. root `results.json`은 필요 시에만 `--write-root-results`로 별도 opt-in
4. 그 다음 `P1.1-SL-STRING-DRIFT`와 `P2 accessory-token guardrail` 중 하나로 이동
