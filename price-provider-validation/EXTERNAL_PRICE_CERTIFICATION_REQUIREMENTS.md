# External Price Certification Requirements

Status: REQUIREMENTS_ONLY / UNVERIFIED / FAIL_CLOSED

This document defines evidence required before real KIS or KIWOOM
daily prices may be certified. It does not authorize API execution,
analysis, persistence, database rebuilding, or broker operations.

## 1. Provider and API identity

Record provider, API identifier, documented endpoint, ticker,
observation date, request parameters, and response field mapping.

KIS inquire_daily_itemchartprice:
- FID_ORG_ADJ_PRC 0 requests adjusted prices.
- FID_ORG_ADJ_PRC 1 requests original prices.

KIS inquire_daily_price:
- Official examples describe a different selector convention.
- Do not reuse the itemchartprice mapping without separate validation.

KIWOOM ka10081:
- upd_stkpc_tp 0 requests original prices.
- upd_stkpc_tp 1 requests adjusted prices.
- Response adjustment-related fields must not be interpreted as
  certified adjustment state without independent verification.

KIWOOM ka10086:
- No adjusted-price request selector has been certified.
- Response adjustment state remains UNKNOWN.

## 2. Original response and acquisition evidence

Require independently attributable source evidence, original response
bytes, SHA-256 digest, acquisition timestamp with timezone, documented
API identity, and an independently verifiable acquisition record.

Digest equality alone does not establish provider authenticity or
prove that an observation was parsed from the supplied bytes.

The observation-to-original-response derivation must be separately
verified before any certification claim.

## 3. Observation and trading calendar

Require canonical observation dates, provider field mapping,
documented market timezone, official exchange trading-calendar
evidence, and independently checked date-to-session alignment.

Structural trading-day eligibility is not official trading-day
certification.

## 4. Adjustment and corporate actions

Record requested adjustment selector separately from verified
response adjustment state.

Require provider adjustment policy, historical corporate-action
treatment, effective dates, and independent verification of adjusted
versus original OHLCV values.

Until verified, response adjustment remains UNKNOWN.

## 5. Price quality and cross-provider comparison

Validate numeric OHLCV, nonnegative volume, price relationships,
missing records, duplicates, chronological consistency, and
applicable trading-day continuity using existing reusable contracts.

A match between KIS and KIWOOM raw prices is MATCHED_UNVERIFIED,
not independent certification. Disagreement must not trigger
automatic fallback or source prioritization.

## 6. Licensing and permitted use

Independently confirm applicable provider terms, acquisition rights,
storage rights, redistribution restrictions, historical-data use,
and operational permissions before enabling any new use.

Public API documentation alone does not grant data-use rights.

## 7. Fail-closed release boundary

Until independent source, adjustment, calendar, quality, and
licensing evidence is verified and explicitly approved:

- independently_verified = False
- analysis_authorized = False
- persistence_authorized = False
- database_rebuild_authorized = False
- live_api_execution_authorized = False
- broker_execution_authorized = False

No implicit authorization, fallback, or production integration.

## 8. Existing modules to reuse

- provider_evidence.py
- adjustment_request.py
- trading_day_certification.py
- price_quality_adapter.py
- provider_pair_boundary.py
- kis_daily_response.py
- kiwoom_daily_response.py

Any future certification implementation requires separate approval,
isolated tests, and successful GitHub CI verification.
