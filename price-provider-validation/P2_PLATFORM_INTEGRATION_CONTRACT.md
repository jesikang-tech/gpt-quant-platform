# P2 Platform Price Provider Integration Contract

Status: DESIGN_ONLY / UNVERIFIED / DENY_ONLY

## 1. Scope

Connect existing K1-K22 synthetic price provider contracts to
the existing GPT Quant Platform through a reusable, isolated
integration boundary.

No real API, broker, database, dashboard, analysis or
persistence execution is authorized.

## 2. Reuse existing modules

- provider_daily_interface
- provider_quality_entry
- provider_analysis_boundary
- provider_collection_entry
- provider_persistence_entry
- provider_certification_acceptance
- provider_license_purpose
- provider_execution_authorization
- core.price_provenance_gate

Existing validation logic must not be duplicated.

## 3. Proposed integration module

Canonical module path:
price-provider-validation/price_provider_validation/provider_platform_integration.py

Responsibilities:

- Preserve provider identity and observation identity.
- Reuse existing certification and licensing decisions.
- Reject provider identity mismatches.
- Reject forged or elevated authorization fields.
- Preserve UNKNOWN adjustment status.
- Return a deny-only integration assessment.
- Never invoke analysis, persistence, API or broker callbacks.

## 4. Protected platform boundaries

- /api/historical-replay
- /api/ver11-analysis
- /api/ver11-analysis/snapshots
- current_analysis.py
- historical_replay.py
- repository.py price persistence
- repository.py Ver1.1 snapshot persistence
- collector price collection and incremental updates

Existing legacy behavior must be preserved unless
a separately reviewed safety change is required.

## 5. Safety invariants

HOST_PYTHON_EXECUTION: DENIED
OPERATING_DB_ACCESS: PROHIBITED
LIVE_API_EXECUTION: DENIED
BROKER_CALLS: DENIED
MAIN_MERGE: NOT_AUTHORIZED

Unverified provider data must never gain:

- API execution authority
- analysis authority
- dashboard authority
- snapshot authority
- persistence authority
- database rebuild authority
- redistribution authority
- broker execution authority

## 6. Implementation stages

P3: Synthetic integration adapter.
P4: Provenance, integrity and adjustment-policy boundary.
P5: Analysis, dashboard and persistence entrypoint protection.
P6: Synthetic integration regression tests.
P7: GitHub CI verification and independent handoff.

## 7. Acceptance criteria

- Reuse existing K1-K22 contracts.
- No duplicated authorization engine.
- Synthetic inputs only.
- Forged approvals rejected.
- Provider mismatch rejected.
- No external callback invoked.
- No operational DB or network access.
- Existing NAVER isolation preserved.
- New tests registered in GitHub CI.
- GitHub CI success required before completion.

## 8. External dependency

KIWOOM official inquiry: 7961
Official reply: PENDING

No actual price collection, persistence or analysis
is authorized by this design document.

## KIWOOM Q&A 7961 follow-up (2026-11-04)

- Historical baseline: official reply PENDING at P2/P7 handoff.
- Reported reply timestamp: 2026-11-02 15:05 KST (conversation summary; original capture not repository-verified).
- Reported scope: personal investment use, personal storage, own analysis and backtesting.
- Reported restriction: third-party redistribution is not permitted.
- Evidence state: OFFICIAL_REPLY_REPORTED / SOURCE_AUTHENTICITY_UNVERIFIED.
- No automatic permission for commercial services, broker execution, or production integration.
- No certification of provider provenance, adjustment policy, data accuracy, or API runtime behavior.
- All operational gates remain DENIED; operating DB access and host Python execution remain prohibited.
