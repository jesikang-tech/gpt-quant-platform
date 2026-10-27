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
