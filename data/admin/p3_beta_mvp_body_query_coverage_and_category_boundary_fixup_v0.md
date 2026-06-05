# P3-BETA-MVP-BODY-QUERY-COVERAGE-AND-CATEGORY-BOUNDARY-FIXUP

- decision_status: `beta_mvp_body_query_coverage_category_boundary_fixup_passed_ready_for_owner_approved_push`
- production_alias_connect_allowed: `false`

## Previous Audit Summary
- decision_status: `None`
- top_priority_fixup: `P3-BETA-MVP-BODY-QUERY-COVERAGE-AND-CATEGORY-BOUNDARY-FIXUP`
- production_alias_connect_allowed: `None`

## Body Parser Alias Changes
- new_aliases: `['m9', 'm9-p', 'm10', 'm10-r', 'm11', 'sl2']`
- variant_carry_over: `{'m9-p': ['P'], 'm10-r': ['R']}`
- token_consumption_rule: `parsed body tokens are not left behind as unknown tokens`
- body_alias_skip_rule: `body alias does not fire for accessory-intent or lens-family queries`

## Body Query Safe Handling
- `Leica M9`: body_intent=`M9`, top=`Body:M9`, state=`exact_or_strong_body_results`, weak_brand_suppressed=`True`
- `leica m9`: body_intent=`M9`, top=`Body:M9`, state=`exact_or_strong_body_results`, weak_brand_suppressed=`True`
- `m9`: body_intent=`M9`, top=`Body:M9`, state=`exact_or_strong_body_results`, weak_brand_suppressed=`True`
- `Leica M9-P`: body_intent=`M9-P`, top=`Body:M9-P`, state=`exact_or_strong_body_results`, weak_brand_suppressed=`True`
- `Leica M10`: body_intent=`M10`, top=`Body:M10`, state=`exact_or_strong_body_results`, weak_brand_suppressed=`True`
- `Leica M10-R`: body_intent=`M10-R`, top=`Body:M10-R`, state=`exact_or_strong_body_results`, weak_brand_suppressed=`True`
- `Leica M11`: body_intent=`M11`, top=`Body:M11`, state=`exact_or_strong_body_results`, weak_brand_suppressed=`True`
- `Leica Q3 28`: body_intent=`Q3`, top=`Body:Q3`, state=`exact_or_strong_body_results`, weak_brand_suppressed=`True`
- `q3 28`: body_intent=`Q3`, top=`Body:Q3`, state=`exact_or_strong_body_results`, weak_brand_suppressed=`True`
- `Leica SL2`: body_intent=`SL2`, top=`Body:SL2`, state=`exact_or_strong_body_results`, weak_brand_suppressed=`True`
- `Leica MP silver`: body_intent=`MP`, top=`Body:MP`, state=`exact_or_strong_body_results`, weak_brand_suppressed=`True`

## Lens Accessory No-Result Regressions
- `summicron`: top_category=`Lens`, market_entry_allowed=`False`, total_ranked=`1232`
- `ltm summaron 35`: top_category=`Lens`, market_entry_allowed=`True`, total_ranked=`197`
- `35 lux aa`: top_category=`Lens`, market_entry_allowed=`True`, total_ranked=`447`
- `leica hood 12585`: top_category=`Accessory`, market_entry_allowed=`False`, total_ranked=`108`
- `m adapter l`: top_category=`Accessory`, market_entry_allowed=`False`, total_ranked=`165`
- `ricoh gr iiix`: top_category=`None`, market_entry_allowed=`False`, total_ranked=`0`
- `hasselblad xpan`: top_category=`None`, market_entry_allowed=`False`, total_ranked=`0`

## Git Diff Summary
```text
(no working diff in scoped files)
```

## Commit Push Status
- commit_executed: `False`
- push_executed: `False`
- push_succeeded: `False`
- preview_deployment_url: `None`
- preview_deployment_id: `None`
- preview_deployment_state: `None`
- preview_branch: `None`
- preview_commit: `None`
- head_commit: `d0d14905657a96c977d8b4a1119813fa07711748`
- head_subject: `fix: prioritize body intent and category boundaries for Leica body queries`
