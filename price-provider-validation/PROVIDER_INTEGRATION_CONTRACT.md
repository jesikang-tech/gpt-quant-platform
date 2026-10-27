# Parallel Price Provider Integration Contract

Status: DESIGN_ONLY / UNVERIFIED / FAIL_CLOSED

## Provider boundaries

- KIS and KIWOOM are separate price observation providers.
- Raw observations are untrusted input, not verified price evidence.
- No automatic fallback or source substitution is permitted.
- Provider identity must remain attached to each observation.

## Existing contract reuse

Reuse the existing contracts where applicable:

- decimal_price_conflict.py
- decimal_source_integration.py
- price_provenance_gate.py

Do not duplicate their Decimal OHLCV validation logic.

The existing Decimal source contract accepts only:
- ADJUSTED
- UNADJUSTED

UNKNOWN adjustment must never be relabeled to pass validation.

## Provenance

- Provider name alone does not establish provenance.
- Caller-supplied flags cannot authorize analysis.
- Each provider requires independent evidence of data origin,
  licensing, adjustment policy, and observation timing.
- A NAVER-specific trust decision cannot certify KIS or KIWOOM.

## Authorization

Until independently verified:

- analysis: DENIED
- portfolio: DENIED
- dashboard: DENIED
- snapshot: DENIED
- persistence: DENIED
- database rebuild: DENIED

## Execution scope

No API requests, credentials, account access, broker orders,
network access, operating database access, or host Python
execution are part of this scaffold.

## Future integration

1. Establish provider-specific raw response contracts.
2. Validate source identity and adjustment policy.
3. Verify provenance independently.
4. Reuse existing Decimal OHLCV normalization.
5. Integrate only through explicitly verified authorization gates.

No completion or authorization is implied by this document.

## Existing platform integration boundary

The existing `providers/base_provider.py` defines ETF-list and
price-DataFrame retrieval methods. It does not establish provenance,
licensing, adjustment semantics, or observation-time evidence.

The current `FDRProvider` in `providers/fdr_provider.py` invokes the root
`core.price_provenance_gate` before calling FinanceDataReader.
The gate currently denies unverified persistence authorization.

KIS and KIWOOM observation adapters must remain independent from:
- `providers/fdr_provider.py`
- `collector/etf_collector.py`
- `collector/price_collector.py`
- `collector/ohlcv_backfill.py`

Do not register KIS or KIWOOM as operational `BaseProvider`
implementations until separately approved and verified.

The root provenance gate is a denial boundary, not a source
certification mechanism. The NAVER-specific gate must not be used
to certify KIS or KIWOOM.

A synthetic Decimal record does not authorize analysis, dashboard
display, snapshots, persistence, or database rebuild.

Provider-specific API response fields, licensing, adjustment policy,
observation timestamps, and independently authenticated provenance
remain unresolved. No real API request is authorized by this document.
