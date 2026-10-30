# Parallel Price Provider Validation

Status: SCAFFOLD_ONLY

Providers:
- KIS (Korea Investment & Securities)
- KIWOOM

Purpose:
- Independent raw observation adapters
- Reuse existing Decimal OHLCV validation
- Provider-specific provenance and adjustment evidence
- Fail-closed integration boundaries

Not authorized:
- Network or API requests
- Broker or account access
- Price analysis or dashboard publication
- Persistence or database rebuilding
- Automatic provider fallback

This directory is not a trusted price source.

## Synthetic CI verification record

The original SCAFFOLD_ONLY status above describes operational authority,
not the absence of implemented offline contracts.

As of 2026-10-30, the isolated feature branch has implemented and
synthetically tested the following independent improvements:

- I1: CI registration and execution safeguards.
- I2: Provider error and exception boundaries.
- I3: Shared daily observation interface for KIS and KIWOOM.
- I4: Synthetic price quality and numeric edge cases.
- I5: Fail-closed missing, mismatched, and equal-but-unverified provider pairs.
- I6: Shared raw observation validation reused at the provider pair boundary.

I7 final evidence documentation and release verification remain separate
from these six completed improvements.

### Verified GitHub Actions evidence

Workflow: `.github/workflows/parallel-price-provider-contract.yml`

- I1: run `40993889539`, success.
- I2: run `40994975729`, success.
- I3: run `41000403040`, success.
- I4: run `41000714517`, success.
- I5: run `41001171293`, success.
- I6: run `41001742572`, success.
- I6 verified commit:
  `39500c43b35eb97f8d0ada1cea1f926079fcbfb8`.
- I6 required jobs: `synthetic-contract` and
  `ci-registration-guard`, both successful.
- Provider validation test files registered in the workflow: 13.

Initial synthetic CI baseline tag:
`price-providers-synthetic-ci-baseline-20261030`

Initial baseline commit:
`476deaa08e0fd6a6767c38f5dede9f16e9f72714`

The baseline tag is retained as historical evidence and does not
represent the latest I6 verification commit.

### Unresolved external verification

Synthetic test success does not authenticate real KIS or KIWOOM data.
Provider API field contracts, licensing, adjustment policy,
trading-calendar authority, observation timestamps, and independently
verified provenance require separate confirmation.

NAVER permission and data-source questions also remain separate and
unresolved pending an official response.

The following remain DENIED: analysis, portfolio, dashboard, snapshot,
persistence, database rebuild, automatic provider fallback, broker
execution, and real API access.

No operational provider registration or trusted-price certification
is implied by this verification record.
