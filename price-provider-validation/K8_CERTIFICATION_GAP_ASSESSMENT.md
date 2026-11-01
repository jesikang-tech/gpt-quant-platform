# K8 External Price Certification Gap Assessment

Status: REVIEW_COMPLETE / CI_NOT_YET_VERIFIED / OPERATIONAL_USE_DENIED

## Baseline

- Repository: jesikang-tech/gpt-quant-platform
- Branch: feature/parallel-price-providers
- Reviewed baseline: c2fc301f2f398c67951a167e9e9941db1ccdbeb8
- Review evidence: COMMAND 118-P, 119-P, 120-P
- Scope: offline KIS/KIWOOM price certification contracts

## Existing modules to reuse

- provider_evidence.py: provider identity, dates, SHA-256 format and supplied-byte digest binding
- kiwoom_raw_json_binding.py: strict JSON reparse and selected observation binding
- adjustment_request.py: documented request selector classification without response certification
- trading_day_certification.py: structural eligibility separate from official exchange evidence
- price_quality_adapter.py: existing OHLCV structural classification
- provider_pair_boundary.py: comparison without independent certification
- provider_analysis_boundary.py: deny unverified analysis
- provider_persistence_entry.py: deny unverified persistence
- kis_daily_response.py: KIS output2 row field/date validation
- kis_adapter.py: provider-neutral raw observation preparation

## KIS confirmed gap

The current KIS daily adapter accepts a caller-supplied dictionary
representing one output2 row.

No KIS-specific raw JSON byte reparse, duplicate-key rejection,
unique selected-row derivation, and raw-response digest/evidence
binding was found in the reviewed provider modules.

This is a gap in offline consistency checking, not evidence that
a real KIS response is trustworthy.

## K9 minimum implementation scope

1. Accept only caller-supplied raw JSON bytes.
2. Restrict the parser to the documented KIS daily response shape.
3. Enforce strict UTF-8, bounded size and duplicate-key rejection.
4. Require a valid output2 array and a uniquely selected date.
5. Reuse prepare_kis_daily_observation for selected row conversion.
6. Reuse assess_raw_bytes_evidence_binding for digest consistency.
7. Preserve UNKNOWN adjustment and DENIED authorization.
8. Add isolated synthetic rejection and positive-structure tests.
9. Register tests in the existing provider GitHub CI workflow.

## Not authorized by K8 or K9

- Live KIS or KIWOOM API requests
- Provider authentication or account access
- Independent provenance certification
- Response adjustment certification
- Official trading-calendar certification
- Analysis, dashboard, snapshots or persistence
- Operating database access or rebuilding
- Broker orders or live execution
- Main branch merge

## Remaining work

- K9: KIS raw JSON binding
- K10: adjustment and corporate-action evidence
- K11: trading calendar, continuity and ETF scope
- K12: integrated fail-closed execution boundaries
- K13: CI and handoff
- K14-K22: separately approved real-data and operational phases

## Release rule

K8 may be marked complete only after this assessment is committed,
pushed, and its required checks are verified.
