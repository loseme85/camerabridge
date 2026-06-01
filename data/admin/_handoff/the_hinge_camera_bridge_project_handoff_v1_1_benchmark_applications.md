# The Hinge / Camera Bridge Project Handoff v1.1

_Last updated: 2026-05-29 KST_

_Update note: v1.1 adds benchmark-derived product applications and market-positioning guidance from the strategic review conversation._

## 0. Purpose of this handoff

This document exists so the project does **not** depend only on ChatGPT memory.

Use this file as the single project handoff when starting a new ChatGPT/Codex session.  
It should prevent:

- repeating already completed contract rounds
- skipping important backlog items
- losing the overall The Hinge → Camera Bridge architecture
- mixing Camera-specific rules into The Hinge Core
- generating command prompts that conflict with previous artifacts

---

## 1. Company and product framing

### Company

**The Hinge**

The Hinge is a market intelligence company connecting fragmented supply with high-intent demand.

The company should not be framed as only a camera search service.  
The long-term system is a reusable market monitoring, normalization, alerting, and intelligence layer for fragmented inventory markets.

### First vertical product

**Camera Bridge by The Hinge**

Camera Bridge is the first vertical domain pack built on The Hinge Core.

Initial focus:

- Leica and rare camera/lens used-market monitoring
- global dealer-site surveillance
- rare listing alerts
- source-gap alerts
- conditional rare / smart deal alerts
- price guide and market intelligence over time

---

## 2. Core product thesis

The service does not compete by showing “many results.”

It competes by replacing the user’s manual dealer-site refresh behavior.

Core user behavior being replaced:

```text
User bookmarks dealer sites
→ repeatedly checks Map Camera / Fujiya / Leica Store / Ffordes / etc.
→ hopes a rare listing appears before others see it
```

The service promise:

```text
We watch the market before you refresh it.
```

Korean framing:

```text
전세계 딜러사이트를 직접 새로고침하지 않아도,
찾던 매물이 나오면 정확하게 알려주는 서비스.
```

---

## 3. Non-negotiable product principles

### 3.1 Accuracy over volume

```text
많이 보여주는 검색엔진이 아니라,
틀린 것을 안 보여주는 검색엔진.
```

### 3.2 No fake fill

If a user asks for Sigma 14-24 L and there is no exact candidate:

- do not substitute Leica SL 14-24
- do not substitute Sigma 24-70
- do not invent an adjacent result
- route to source-gap / exact monitoring instead

### 3.3 Broad query refinement

Broad queries must not create direct fast alerts.

Examples:

- summicron
- summilux
- leica m
- leica sl
- cron
- lux
- leica lens

These should route to:

- refinement UI
- family selector
- full normalization queue
- no direct urgent alert

### 3.4 Manual-review targets do not fast-path

Examples currently treated as manual-review / not launch-safe:

- Leica M-A
- M10 Monochrom
- M10-R
- M11 Monochrom

### 3.5 Source-gap means source-gap

A source-gap query should stay honest:

```text
현재 정확한 매물은 없지만, 감시하고 있다.
```

It should not become:

```text
비슷한 매물을 대체로 보여준다.
```

### 3.6 The Hinge Core must be domain-neutral

The Core must not hard-code:

- Summicron
- Summilux
- Noctilux
- 35 lux aa
- Rolex 14060M
- PLC module revision
- domain-specific aliases or source rules

Those belong inside vertical domain packs.

---

## 4. Architecture

```text
The Hinge Core
├─ Source Monitoring
├─ Source Change Detection
├─ Normalization Interface
├─ Demand-Based Freshness Scheduler
├─ Fast Alert Path
├─ Alert Lifecycle
├─ Preference Center
├─ Delivery Queue
├─ Provider Adapter
├─ No-Result / Refinement Framework
└─ Market Intelligence Layer

Vertical Domain Packs
├─ Camera Bridge
├─ Watch Bridge
├─ Parts Bridge
├─ Audio Bridge
├─ Moto Bridge
└─ Collectibles Bridge
```

### The Hinge Core owns

- source monitoring interface
- source change detection
- freshness scheduling
- generic watch target classes
- alert lifecycle
- preference center logic
- delivery queue
- provider adapter
- no-result/refinement framework
- market intelligence metrics

### Vertical Domain Pack owns

- canonical entities
- aliases
- shorthand rules
- source profiles and selectors
- condition overlays
- rarity / conditional rarity rules
- price normalization
- source-gap policy
- no-result copy
- watchlist seed
- alert eligibility rules
- risk policy
- market metrics

---

## 5. Domain pack status

### Camera Bridge

Status: `active_first_vertical`

Preview strengths:

- canonical entity taxonomy exists
- aliases exist
- source profiles exist
- watchlist seed exists
- condition overlays exist
- rarity rules exist
- source-gap policy supported
- conditional rare supported
- no-result policy supported
- price guide supported

Camera Bridge is the first proof that The Hinge Core can work.

### Watch Bridge

Status: `planned`

Needs:

- reference taxonomy
- dial / bracelet / box / papers overlays
- source list
- authenticity risk policy

### Parts Bridge

Status: `exploratory`

Needs:

- part number taxonomy
- compatibility / revision mapping
- substitute part rules
- high safety / regulatory risk policy

### Audio Bridge

Status: `exploratory`

Needs:

- model/year/serial taxonomy
- modification / provenance overlays
- vintage condition rules

### Moto Bridge

Status: `exploratory`

Needs:

- frame / engine / year compatibility
- domestic/export spec rules
- OEM / aftermarket / reproduction status

### Collectibles Bridge

Status: `exploratory`

Needs:

- grading rules
- sealed/opened status
- edition / print run rules
- authenticity risk policy

---

## 6. Alert MVP completed contract rounds

The following rounds should be treated as completed. Do not ask Codex to redo these unless explicitly revising or implementing them.

### 6.1 Alert watchlist

Artifact family:

- `alert_watchlist_contract.py`
- `data/admin/alert_mvp_watchlist_v0.json`
- `data/admin/p3_alert_mvp_query_watchlist_v0.md`

Purpose:

- defines initial MVP watchlist
- includes rare Leica, Leica body, R lens, SL, source-gap, and third-party L-mount targets
- separates include, source-gap, source-expansion, manual-review, and broad/refinement exclusions

### 6.2 Signup flow

Artifact family:

- `alert_signup_contract.py`
- `data/admin/alert_mvp_signup_flow_v0.json`

Purpose:

- maps user query/watchlist status to CTA
- alert signup
- source-gap alert signup
- source expansion waitlist
- manual review unavailable
- refinement required
- too broad / unavailable

### 6.3 Storage schema

Artifact family:

- `alert_storage_contract.py`
- `data/admin/alert_mvp_storage_schema_v0.json`

Purpose:

- defines signup, verification, subscription, event, notification log, suppression previews
- raw email absent
- token hash only
- dedupe policies

### 6.4 Email verification

Artifact family:

- `alert_verification_contract.py`
- `data/admin/alert_mvp_email_verification_contract_v0.json`

Purpose:

- pending → verified → active lifecycle
- token TTL / attempts / resend cooldown
- source-gap and waitlist activation
- blocked signups are not verifiable

### 6.5 Delivery simulation

Artifact family:

- `alert_delivery_contract.py`
- `data/admin/alert_mvp_delivery_simulation_v0.json`

Purpose:

- active subscriptions matched with mock events
- queue vs skip decisions
- duplicate / inactive / suppressed / no-match / trigger disabled behavior

### 6.6 Email template

Artifact family:

- `alert_email_template_contract.py`
- `data/admin/alert_mvp_email_template_contract_v0.json`

Purpose:

- renders preview templates for queueable events
- no provider send
- fake-fill templates blocked
- includes manage/unsubscribe/privacy/source disclaimer placeholders

### 6.7 Unsubscribe contract

Artifact family:

- `alert_unsubscribe_contract.py`
- `data/admin/alert_mvp_unsubscribe_contract_v0.json`

Purpose:

- single unsubscribe
- unsubscribe all
- pause/resume/delete
- privacy delete request
- suppression preview
- post-unsubscribe delivery behavior

### 6.8 No-result UI contract

Artifact family:

- `alert_no_result_ui_contract.py`
- `data/admin/alert_mvp_no_result_ui_contract_v0.json`

Purpose:

- source_gap_alertable
- source_expansion_needed
- broad_query_refinement_required
- broad_query_excluded
- manual_review_required
- true_no_result
- fake result / adjacent substitution prohibited

### 6.9 Delivery queue schema

Artifact family:

- `alert_delivery_queue_contract.py`
- `data/admin/alert_mvp_delivery_queue_schema_v0.json`

Purpose:

- queue job schema before provider dispatch
- retry / max attempts / expiry
- pre-dispatch suppression
- duplicate prevention
- raw email and provider payload absent

### 6.10 Email provider adapter contract

Artifact family:

- `alert_email_provider_adapter_contract.py`
- `data/admin/alert_mvp_email_provider_adapter_contract_v0.json`

Purpose:

- provider-neutral send request/result/webhook preview
- mapping preview for provider_neutral / Resend / SendGrid / AWS SES
- provider_send_enabled=false
- failure/bounce/complaint mapping
- no actual provider call

### 6.11 Crawl freshness scheduler contract

Artifact family:

- `crawl_freshness_scheduler_contract.py`
- `data/admin/crawl_freshness_scheduler_contract_v0.json`

Purpose:

- source profile + watch target profile + demand signal + source×watch matrix
- determines interval bands: very_fast / fast / normal / slow / paused
- includes anti-bot guard and crawl budget preview
- true rare / conditional rare / common watch / source-gap / source-expansion separated

### 6.12 Vertical domain pack contract

Artifact family:

- `vertical_domain_pack_contract.py`
- `data/admin/vertical_domain_pack_contract_v0.json`

Purpose:

- separates The Hinge Core from vertical domain packs
- Camera Bridge is active_first_vertical
- Watch / Parts / Audio / Moto / Collectibles future pack previews
- anti-hardcode policy

### 6.13 Source change detection contract

Artifact family:

- `source_change_detection_contract.py`
- `data/admin/source_change_detection_contract_v0.json`

Purpose:

- compares source snapshots / listing fingerprints
- detects unchanged, new, price changed, availability changed, sold/removed, duplicate, source-gap exact, fake-fill, source expansion, manual-review
- routes to fast alert / full normalization / price guide / manual review / ignore

### 6.14 Fast alert path contract

Artifact family:

- `fast_alert_path_contract.py`
- `data/admin/fast_alert_path_contract_v0.json`

Purpose:

- receives source change candidates
- lightweight normalization
- watchlist match
- condition match
- confidence guard
- creates queue-compatible candidate preview or blocked candidate preview
- only true rare, price drop opt-in, source-gap exact, conditional rare high-confidence pass

### 6.15 Preference center contract

Artifact family:

- `alert_preference_center_contract.py`
- `data/admin/alert_mvp_preference_center_contract_v0.json`

Purpose:

- user alert preferences
- active/pause/resume
- digest conversion
- price-drop opt-in
- source allowlist
- source-gap/source-expansion management
- global unsubscribe
- suppressed/unverified blocks
- downstream fast_alert_effect and delivery_queue_effect

---

## 7. Current system flow

```text
Domain Pack
→ Watchlist / Alert Eligibility
→ Signup CTA
→ Storage
→ Email Verification
→ Preference Center
→ Freshness Scheduler
→ Source Change Detection
→ Fast Alert Path
→ Delivery Queue
→ Provider Adapter
→ Email Template / Delivery Preview
→ Unsubscribe / Suppression
```

For discovery and alert speed:

```text
Freshness Scheduler
→ decides when to look

Source Change Detection
→ decides what changed

Fast Alert Path
→ decides whether it can alert quickly

Delivery Queue
→ holds send-ready job preview

Provider Adapter
→ maps job to provider-neutral request preview
```

---

## 8. Current recommended next backlog

Current recommended next step:

```text
P3-ALERT-MVP-LANDING-PAGE-COPY-CONTRACT
```

Why:

- The internal alert engine is now mostly designed.
- Users need to understand why the service matters.
- Landing copy should explain:
  - refresh replacement
  - rare alert
  - source-gap honesty
  - conditional rare / smart deal
  - no fake results
  - user control / preference center
  - The Hinge / Camera Bridge positioning

Secondary next candidates:

```text
P3-ALERT-MVP-PREFERENCE-CENTER-IMPLEMENTATION
P3-FAST-ALERT-PATH-IMPLEMENTATION
P3-SOURCE-CHANGE-DETECTION-IMPLEMENTATION
P3-CRAWL-FRESHNESS-SCHEDULER-IMPLEMENTATION
P3-WATCH-BRIDGE-MARKET-SCOUT-CONTRACT
```

---

## 9. Implementation sequence suggestion

After landing-page copy contract, the implementation order should probably be:

```text
1. Source Change Detection Implementation
2. Fast Alert Path Implementation
3. Crawl Freshness Scheduler Implementation
4. Preference Center Implementation
5. Delivery Queue / Provider Adapter Implementation
6. Landing page / signup UI
7. Limited beta with email verification and no-result source-gap signup
```

Reason:

- implementation should start where real data enters the pipeline
- source change detection must produce stable candidates
- fast alert path must filter candidates safely
- scheduler controls crawl frequency
- preference center controls user settings
- queue/provider comes after candidates are safe

---

## 10. Command-prompt generation rules

When generating future Codex prompts, always include:

1. project context
2. previous completed round
3. exact goal of this round
4. what this round is **not**
5. files allowed to modify
6. files forbidden to modify
7. schema/contracts to define
8. scenario validations
9. output artifacts
10. tests and golden set
11. completion report format
12. next backlog candidates

Also preserve the user’s preference:

```text
Every 5 command prompts, include a progress check:
- completed rounds
- current phase
- remaining major milestones
- recommended next 1–2 steps
```

---

## 11. Anti-duplication checklist before creating a new prompt

Before writing a new command prompt, check this list:

```text
1. Is this already completed as a contract?
2. Is this asking for implementation of an existing contract?
3. Does it modify production files that should remain untouched?
4. Does it duplicate an existing artifact?
5. Does it accidentally put domain-specific knowledge into The Hinge Core?
6. Does it break fake-fill / broad-query / manual-review guardrails?
7. Does it bypass preference/suppression/unverified checks?
8. Does it require web/current market research?
9. Does it need a progress checkpoint?
```

If already completed, do not redo.  
Instead choose implementation, extension, or next backlog.

---

## 12. File naming conventions

Use P3 names consistently:

```text
p3_<task_name>_v0.md
p3_<task_name>_v0.jsonl
<task_name>_v0.json
```

Scripts:

```text
scripts/run_p3_<task_name>.py
```

Tests:

```text
tests/test_<task_name>.py
```

Root-level contract module unless a stable package exists:

```text
<task_name>_contract.py
```

---

## 13. Golden validation habit

Most completed rounds require:

```text
python3 -m py_compile ...
python3 scripts/run_p3_*.py
python3 tests/test_*.py
JSONL validation
contract JSON validation
python3 golden_set.py
```

`golden_set.py` should remain:

```text
132/132
```

If a future round changes this unexpectedly, stop and inspect.

---

## 14. Safe continuation prompt for a new ChatGPT/Codex session

Use this at the start of a new session:

```text
You are continuing The Hinge / Camera Bridge project.

Read this handoff first and do not duplicate completed P3 contract rounds.

The Hinge Core is domain-neutral. Camera Bridge is the first vertical domain pack.

Preserve these guardrails:
- no fake fill
- no adjacent-family substitution
- broad query refinement only
- manual-review targets do not fast-path
- source-gap stays exact
- preference/suppression/unverified states block queue creation
- production crawler/search/parser/resolver/classifier files must not be modified unless explicitly requested

Current recommended next backlog:
P3-ALERT-MVP-LANDING-PAGE-COPY-CONTRACT.
```

---

## 15. Short Korean explanation for project owner

```text
이 문서는 ChatGPT 메모리가 사라져도 프로젝트 흐름을 잃지 않기 위한 기준표다.

앞으로 새 명령문을 만들 때는 이 문서를 먼저 보고,
이미 끝난 contract를 반복하지 않고,
남은 backlog 중 다음 단계만 선택하면 된다.

즉, 기억은 보조이고
이 핸드오프 문서가 프로젝트의 기준점이다.
```

---

## 16. Benchmark-derived product applications

This section records strategic learnings from adjacent market-intelligence, alert, marketplace, and price-guide products.  
The goal is **not** to copy these companies directly.  
The goal is to extract reusable product patterns that fit The Hinge / Camera Bridge principles:

- accuracy over volume
- no fake fill
- source-gap honesty
- dealer-site refresh replacement
- domain-neutral The Hinge Core
- vertical-specific domain packs

### 16.1 Strategic conclusion from benchmark review

The Hinge should not enter a market just because the market is large.

The best target market is where:

```text
high-intent demand exists
+ premium / scarce goods exist
+ supply is fragmented
+ search terms, model names, variants, or part numbers are hard to normalize
+ existing services do not fully solve exact matching and alerting
+ users repeatedly refresh dealer / marketplace / forum sources manually
```

Current conclusion:

```text
Camera Bridge remains the best first vertical.
```

Reason:

- direct substitutes for Camera Bridge are weak compared with watch and audio markets
- Leica / rare camera gear has strong alias, family, generation, condition, and accessory ambiguity
- existing camera businesses are mostly inventory holders, marketplaces, price guides, or regional comparison tools
- Camera Bridge can differentiate with exact rare alerts, source-gap alerts, no fake fill, and model-level market intelligence
- the project already has taxonomy, watchlist, alert, source-gap, scheduler, source-change, and fast-alert contract foundations

### 16.2 Competitive-positioning rule

Do not compete as:

```text
another used-camera marketplace
another broad camera search engine
another lowest-price comparison site
another generic saved-search alert tool
```

Compete as:

```text
precision market-watching infrastructure for rare premium camera gear.
```

User-facing promise:

```text
We watch the market before you refresh it.
```

More explicit landing-page framing:

```text
Rare Leica listings disappear fast.
Camera Bridge watches global dealer sources and alerts you only when the exact match appears.
No substitutes. No fake fills. If it is not there, we keep watching.
```

---

## 17. Benchmark patterns to adapt

### 17.1 CLASSIC.COM pattern: model-level market pages

What to adapt:

- market pages by exact model / family
- active listings
- sold / past listings
- market alerts
- price trend and historical market data
- dealer exposure and lead routing
- demand aggregation around specific models

Camera Bridge application:

```text
Leica Summilux-M 35mm f/1.4 ASPH AA Market Page
Leica Noctilux-M 50mm f/1.0 E60 Market Page
Leica Tri-Elmar-M 16-18-21 WATE Market Page
Leica APO-Telyt-M 135mm f/3.4 Market Page
```

Each market page should eventually include:

- canonical family identity
- aliases and unsafe broad aliases
- current exact-match listings
- recently removed / sold / expired listings
- source distribution
- observed price range
- days-on-market estimate
- condition / packaging overlays
- source-gap state if no exact listing exists
- alert signup CTA
- price-drop CTA when enabled
- number of users watching, if safe to disclose

Important difference from CLASSIC.COM:

```text
CLASSIC.COM is market-view first.
Camera Bridge should be exact-watch first.
```

### 17.2 WatchCharts pattern: data subscription and professional tiers

What to adapt:

- price history by exact model
- sales volume / observed listing volume
- days-on-market
- CSV export for professional users
- API / data access later
- paid market data tier

Camera Bridge application:

- free tier: exact search, limited source-gap signup, limited alert watch
- paid collector tier: rare alerts, price-drop alerts, saved watches, model pages, historical listing views
- pro / dealer tier: CSV export, source-level data, demand indicators, pricing support, priority alerts
- future API: normalized model / listing / price / demand data

Do not lead with price charts alone.  
Lead with rare alert and refresh replacement; price data becomes the second monetization layer after enough observations accumulate.

### 17.3 HiFi Shark pattern: multi-source search agent + expired listings

What to adapt:

- multi-source used-market search
- search agents
- expired / removed listing archive
- active vs expired comparison
- simple email alert habit

Camera Bridge application:

- global dealer source monitoring
- exact model search agents
- source-gap watch when no exact listing exists
- removed / sold / expired listing archive
- price guide built from observed active and expired listings

Important difference from HiFi Shark:

```text
HiFi Shark already covers audio broadly.
Camera Bridge should not merely copy broad metasearch.
It should add Leica-grade normalization, no fake fill, and condition-aware market intelligence.
```

### 17.4 Keepa pattern: price / availability tracking UX

What to adapt:

- price history chart
- availability history
- price-drop alert
- item-level tracking
- clear visual timeline

Camera Bridge application:

- model-level price trend
- listing-level price change timeline
- source availability tracking
- sold / removed / relisted state changes
- smart deal / conditional rare alert

Important difference from Keepa:

```text
Camera Bridge should not behave like a lowest-price tracker.
For rare Leica gear, exact identity and condition matter more than raw lowest price.
```

### 17.5 Reverb / PriceCharting / WorthPoint pattern: historical sold-data value

What to adapt:

- sold / historical listing archive
- condition-aware price guide
- collector value tracking
- pricing support for sellers

Camera Bridge application:

- sold / expired Leica price guide
- condition overlays: boxed, hood included, cap included, 6bit, haze, fungus, cleaning marks, finish, country marking
- seller pricing assistant later
- collection value tracking later

Priority:

```text
Build sold / expired archive before claiming precise valuation.
```

### 17.6 PCPartPicker pattern: compatibility warnings

What to adapt:

- compatibility checks
- warning UI
- parts fitment logic
- structured relation graph

Camera Bridge application:

- Leica hood / finder / cap / filter / battery / grip compatibility
- accessory-only listing protection
- lens vs accessory classification guardrails
- future Camera Parts Bridge pack

Examples:

```text
Leica 12585 hood → compatible lens families
E39 filter → compatible lens families
Leica finder → focal-length compatibility
SL battery / Q battery / M battery → body compatibility
```

Important guardrail:

```text
Compatibility suggestion is allowed only when clearly labeled as compatibility.
It must not become adjacent-family substitution in search results or fast alerts.
```

### 17.7 ILS / Automa / Radwell pattern: RFQ, supplier visibility, hard-to-find parts

What to adapt later:

- RFQ / WTB flow
- supplier stock visibility
- demand aggregation
- lead-time and availability monitoring
- source / supplier reliability
- hard-to-find part workflow

Camera Bridge application later:

- WTB / wanted flow for rare Leica gear
- dealer demand dashboard
- “users waiting for this exact family” indicator
- dealer lead routing
- private seller listing flow
- future Premium Parts / Aviation / Industrial packs

Do not implement full RFQ early.  
First validate alert signup and exact market watching.

### 17.8 StockX pattern: buyer intent and bid-like demand signal

What to adapt later:

- user-declared target price
- buy-intent signal
- market demand curve
- seller-facing demand proof

Camera Bridge application later:

```text
Notify me if Leica M6 classic under $X appears.
Notify me if Summilux 35 AA appears below $Y.
I would buy Noctilux E60 at or below $Z.
```

Do not start as a transaction marketplace.  
Avoid authentication, escrow, dispute, return, cross-border tax, and condition-liability burden in MVP.

---

## 18. Fields to add to future product contracts

Future contracts should consider these fields when appropriate.

### 18.1 Market page contract fields

```json
{
  "canonical_family_id": "string",
  "display_name": "string",
  "vertical_pack": "camera_bridge",
  "safe_aliases": ["string"],
  "unsafe_broad_aliases": ["string"],
  "current_exact_listing_count": 0,
  "recent_removed_listing_count": 0,
  "observed_price_low": null,
  "observed_price_high": null,
  "days_on_market_estimate": null,
  "source_distribution": [],
  "condition_overlay_summary": [],
  "source_gap_state": "exact_available | exact_absent_watchable | broad_refinement_required | manual_review_required",
  "primary_cta": "alert_signup | source_gap_signup | refinement | unavailable",
  "no_fake_fill_enforced": true
}
```

### 18.2 Expired / sold listing archive fields

```json
{
  "listing_fingerprint": "string",
  "canonical_family_id": "string",
  "source_id": "string",
  "first_seen_at": "datetime",
  "last_seen_at": "datetime",
  "removed_at": "datetime | null",
  "availability_state": "active | sold | removed | unknown",
  "last_observed_price": "number | null",
  "currency": "string | null",
  "condition_overlays": [],
  "included_accessories": [],
  "confidence": "high | medium | low",
  "valuation_eligible": false
}
```

### 18.3 Demand / watch signal fields

```json
{
  "watch_target_id": "string",
  "canonical_family_id": "string",
  "watch_type": "rare_exact | source_gap | price_drop | conditional_rare | smart_deal | wtb_future",
  "verified_subscriber_count": 0,
  "target_price": null,
  "condition_constraints": [],
  "source_allowlist": [],
  "digest_or_immediate": "immediate | digest",
  "dealer_visible_aggregate_allowed": false
}
```

### 18.4 Compatibility graph fields

```json
{
  "accessory_or_part_id": "string",
  "compatible_family_ids": [],
  "incompatible_family_ids": [],
  "compatibility_confidence": "high | medium | low",
  "relation_type": "hood | finder | filter | battery | cap | grip | adapter",
  "warning_copy": "string",
  "must_not_substitute_listing_results": true
}
```

---

## 19. Product roadmap adjustments from benchmark review

### 19.1 Keep current next backlog

Keep the current recommended next backlog:

```text
P3-ALERT-MVP-LANDING-PAGE-COPY-CONTRACT
```

But the landing-page copy should now explicitly include:

- dealer-site refresh replacement
- exact rare alert
- source-gap honesty
- no fake fill
- not a marketplace
- not a generic price comparison site
- model-level market intelligence coming later
- user control through alert preferences

### 19.2 Add new near-term backlog candidates

Add these after landing-page copy:

```text
P3-MODEL-MARKET-PAGE-CONTRACT
P3-EXPIRED-SOLD-LISTING-ARCHIVE-CONTRACT
P3-PRICE-GUIDE-MARKET-INTELLIGENCE-CONTRACT
P3-DEMAND-SIGNAL-AGGREGATION-CONTRACT
P3-CAMERA-ACCESSORY-COMPATIBILITY-CONTRACT
```

Recommended order:

```text
1. P3-ALERT-MVP-LANDING-PAGE-COPY-CONTRACT
2. P3-MODEL-MARKET-PAGE-CONTRACT
3. P3-EXPIRED-SOLD-LISTING-ARCHIVE-CONTRACT
4. P3-PRICE-GUIDE-MARKET-INTELLIGENCE-CONTRACT
5. P3-DEMAND-SIGNAL-AGGREGATION-CONTRACT
6. P3-CAMERA-ACCESSORY-COMPATIBILITY-CONTRACT
```

Reason:

- landing page explains why the alert product matters
- market page becomes the main product surface
- expired / sold archive creates pricing data foundation
- price guide monetizes the archive after enough evidence exists
- demand signal aggregation supports dealer lead and future B2B
- accessory compatibility supports future Camera Parts Bridge

### 19.3 Deprioritize these for now

Do not prioritize:

```text
Audio Bridge implementation
Watch Bridge implementation
StockX-style marketplace
full RFQ marketplace
Aviation / Industrial implementation
```

Reasons:

- Audio has a strong existing analog in HiFi Shark
- Watch has strong incumbents such as WatchCharts / Chrono-style services
- marketplace liability is too high for MVP
- RFQ and B2B supplier flows require more demand proof
- aviation / industrial require domain experts, compliance, and supplier access

---

## 20. Updated strategic north star

The Hinge should be remembered as:

```text
A precision market-watching company for premium scarce goods.
```

Camera Bridge should be remembered as:

```text
The first vertical proof: rare Leica and premium camera gear watched before users refresh dealer sites.
```

The product should not ask:

```text
How do we show more listings?
```

It should ask:

```text
How do we know the exact thing appeared before the user had to check manually?
```

And if the exact thing did not appear:

```text
How do we honestly preserve that demand and keep watching without fake-filling the result?
```

