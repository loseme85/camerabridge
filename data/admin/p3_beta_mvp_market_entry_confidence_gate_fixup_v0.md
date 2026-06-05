# P3-BETA-MVP-MARKET-ENTRY-CONFIDENCE-GATE-FIXUP

- decision_status: `beta_mvp_market_entry_confidence_gate_fixup_passed_ready_for_owner_approved_push`
- production_alias_connect_allowed: `false`

## Previous Audit Summary
- decision_status: `beta_mvp_lens_family_boundary_market_entry_anchor_audit_completed_fixup_required`
- production_alias_connect_allowed: `False`
- problem_summary: `query parser unknown token + weak-only fallback + first-result market entry anchoring`

## Implemented Gate Fields
- `market_entry_allowed`
- `market_entry_block_reason`
- `price_summary_allowed`
- `price_summary_block_reason`
- `model_entry_confidence_state`
- `boundary_conflict_detected`
- `dangerous_unknown_family_token_detected`
- `weak_only_fallback_detected`

## Market Entry Allowed Rules
- strong_result_count > 0
- not weak-only fallback
- no dangerous unknown family token
- not broad query refinement state
- query intent confidence >= 0.60
- no family/mount/category/variant boundary conflict
- top result must be strong
- exact-model-like match must exist

## Price Summary Allowed Rules
- market_entry_allowed = true
- exact-model-like match exists
- query-compatible results exist
- query-compatible priced results exist
- weak-only fallback prices are excluded

## Query Regression Results
- `Summicron-M 35 ASPH`: market_entry_allowed=`False`, price_summary_allowed=`False`, state=`locked_dangerous_unknown_family_token`, top=`APO-Summicron`
- `Leica M 35mm f2 Summicron ASPH`: market_entry_allowed=`False`, price_summary_allowed=`False`, state=`locked_boundary_conflict`, top=`APO-Summicron`
- `35 Summicron-M ASPH`: market_entry_allowed=`False`, price_summary_allowed=`False`, state=`locked_dangerous_unknown_family_token`, top=`APO-Summicron`
- `APO-Summicron-M 35 ASPH`: market_entry_allowed=`False`, price_summary_allowed=`False`, state=`locked_dangerous_unknown_family_token`, top=`APO-Summicron`
- `apo 35 summicron`: market_entry_allowed=`False`, price_summary_allowed=`False`, state=`locked_dangerous_unknown_family_token`, top=`Summicron`
- `APO-Summicron-SL 50`: market_entry_allowed=`False`, price_summary_allowed=`False`, state=`locked_dangerous_unknown_family_token`, top=`Elmar`
- `APO-Summicron-SL 90`: market_entry_allowed=`False`, price_summary_allowed=`False`, state=`locked_dangerous_unknown_family_token`, top=`Summarit-M`
- `Summicron-M 50`: market_entry_allowed=`False`, price_summary_allowed=`False`, state=`locked_dangerous_unknown_family_token`, top=`Elmar`
- `summicron`: market_entry_allowed=`False`, price_summary_allowed=`False`, state=`locked_weak_only_fallback`, top=`Summicron`
- `leica lens`: market_entry_allowed=`False`, price_summary_allowed=`False`, state=`locked_weak_only_fallback`, top=`Elmar`
- `ltm summaron 35`: market_entry_allowed=`True`, price_summary_allowed=`True`, state=`exact_model_confident`, top=`Summaron`
- `35 lux aa`: market_entry_allowed=`True`, price_summary_allowed=`False`, state=`exact_model_confident`, top=`Summilux-M`
- `q3 28`: market_entry_allowed=`True`, price_summary_allowed=`True`, state=`exact_model_confident`, top=`Q3`
- `ricoh gr iiix`: market_entry_allowed=`False`, price_summary_allowed=`False`, state=`locked_low_query_intent_confidence`, top=`None`
- `hasselblad xpan`: market_entry_allowed=`False`, price_summary_allowed=`False`, state=`locked_low_query_intent_confidence`, top=`None`

## UI Copy Changes
- `locked_market_entry_copy`: `Exact model summary is locked until confidence is high enough.`
- `locked_price_summary_copy`: `Not enough exact confidence for price summary`
- `refine_cta_copy`: `Refine this search`
- `confidence_gate_badge`: `Confidence gate active`

## Git Diff Summary
```text
api/search.py            | 358 +++++++++++++++++++++++++++++++++++++++++++++++
 app/templates/index.html |  80 ++++++++++-
 index.html               |  80 ++++++++++-
 search_ui_hints.py       |  19 +++
 4 files changed, 525 insertions(+), 12 deletions(-)
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
- head_commit: `9481b8906935a3765e1e442be9045a2035734c29`
- head_subject: `fix: include search UI hints module in beta preview runtime`

## Preview Deployment
- url: `None`
- deployment_id: `None`
- state: `None`
- branch: `None`
- commit: `None`

## Guards
- production_launch_go: `False`
- production_alias_connect_allowed: `False`
- public_unrestricted_access_enabled: `False`
- external_tester_access_enabled: `False`
- invite_sent_count: `0`
- provider_send_count: `0`
- webhook_call_count: `0`
- production_DB_write_count: `0`
- access_activation_performed: `False`
- main_direct_push_executed: `False`
- production_promote_executed: `False`
- tester_link_send_allowed: `False`
- raw_identity_recorded: `False`
- raw_contact_recorded: `False`
- external_link_sent: `False`
- fake_fill_added: `False`

## Next Backlog Candidates
- `P3-BETA-MVP-MARKET-ENTRY-CONFIDENCE-GATE-OWNER-RECHECK`
- `P3-BETA-MVP-QUERY-PARSER-UNKNOWN-TOKEN-COVERAGE-FIXUP`
- `P3-BETA-MVP-MARKET-ENTRY-CONFIDENCE-GATE-PUSH-FOLLOWUP`
