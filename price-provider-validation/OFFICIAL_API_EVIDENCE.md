# Official API Contract Evidence

Status: PARTIALLY_VERIFIED / NO_OPERATIONAL_AUTHORITY
Review date: 2026-10-30

## KIS: inquire_daily_itemchartprice

Official provider example:
https://github.com/koreainvestment/open-trading-api/blob/main/examples_llm/domestic_stock/inquire_daily_itemchartprice/inquire_daily_itemchartprice.py

Confirmed from the provider-maintained example:
- Endpoint: /uapi/domestic-stock/v1/quotations/inquire-daily-itemchartprice
- Request parameter: FID_ORG_ADJ_PRC
- Value 0: adjusted price
- Value 1: original price
- Response collections: output1 and output2
- output2 is the historical price row collection

Still requiring independent confirmation:
- Complete response field schema and types
- Historical adjustment consistency
- Trading calendar and observation timestamps
- Licensing and provenance of actual data

## KIS: inquire_daily_price

Official provider example:
https://github.com/koreainvestment/open-trading-api/blob/main/examples_llm/domestic_stock/inquire_daily_price/inquire_daily_price.py

The provider example describes different adjustment-selector
semantics for this separate API:
- Value 0: adjustment not applied
- Value 1: adjustment applied

Do not transfer this selector mapping to
inquire_daily_itemchartprice or vice versa.

## KIWOOM: ka10081 and ka10086

Current local field mappings are synthetic contracts only.

Official primary-source verification remains pending for:
- API response collection names
- Date and OHLCV field names
- ka10081 adjustment selector upd_stkpc_tp
- ka10086 adjustment policy
- Price signs, units, and observation timing

No Kiwoom response adjustment status is certified.

## Operational boundary

This document records API contract evidence only.
It does not authenticate actual market data or grant permission
to access provider APIs.

Analysis, portfolio, dashboard, snapshot, persistence,
database rebuild, automatic provider fallback, broker access,
and live API execution remain DENIED.

No source code, operating database, or main branch
modification is authorized by this document.

## Kiwoom secondary-reference cross-check

Status: SECONDARY_SOURCES_ONLY / NOT_OFFICIALLY_VERIFIED

Reference materials:
- https://github.com/SungmanHan/kiwoom-rest-api-java/blob/main/chart/README.md
- https://algolab.co.kr/blog/kiwoom-rest-api-chart-daily-minute-tick-2026
- https://github.com/unohee/pykiwoom-rest/blob/master/docs/API.md

The external references describe:
- ka10081: POST /api/dostk/chart
- Response list: stk_dt_pole_chart_qry
- Date field: dt
- Close field: cur_prc
- OHLCV: open_pric, high_pric, low_pric, cur_prc, trde_qty
- Request selector: upd_stkpc_tp
- Selector 0: unadjusted; selector 1: adjusted

These statements are not a substitute for an independently
verified official Kiwoom API specification.

ka10086 response fields and adjustment policy remain pending
official primary-source verification.

No external data, adjustment state, provenance, licensing,
trading calendar, analysis, persistence, or operational
authorization is certified by these references.


## Kiwoom official primary-source verification

Review date: 2026-10-30
Status: OFFICIAL_FIELD_CONTRACT_REVIEWED / NO_DATA_CERTIFICATION

Official primary sources:
- https://openapi.kiwoom.com/m/guide/apiguide/08/ka10081
- https://openapi.kiwoom.com/m/guide/apiguide/08/ka10086

ka10081:
- Request: base_dt (YYYYMMDD), upd_stkpc_tp (required).
- Request upd_stkpc_tp 0: original price.
- Request upd_stkpc_tp 1: adjusted price.
- Adjusted historical retrieval depends on base_dt relative
  to the corporate-action effective date and continuation.
- Response array: stk_dt_pole_chart_qry.
- Response date: dt (YYYYMMDD).
- OHLCV: open_pric, high_pric, low_pric, cur_prc, trde_qty.
- Response upd_stkpc_tp describes corporate-action event
  codes and must not be interpreted as the request selector.

ka10086:
- Request: qry_dt (YYYYMMDD), indc_tp (0 quantity, 1 amount).
- Response array: daly_stkpc.
- Response date: date (YYYYMMDD).
- OHLCV: open_pric, high_pric, low_pric,
  close_pric, trde_qty.
- The official guide describes signed numeric price fields.
- An adjusted-price request selector was not identified
  in the reviewed request body.

Endpoint discrepancy:
- The reviewed official detail pages display
  URL /api/dostk/acnt for both APIs.
- Earlier secondary references describe /api/dostk/chart.
- The discrepancy is UNRESOLVED.
- Do not execute either endpoint based on this evidence.

Unverified:
- Actual data provenance, accuracy and completeness.
- Adjustment results for real historical observations.
- Price sign normalization and corporate-action handling.
- Trading-day calendar and source timestamps.
- Licensing, API entitlement and permitted downstream use.

No live API call, provider activation, analysis,
dashboard, persistence, database rebuild, automatic
fallback or broker operation is authorized.


## Official route documentation reconciliation

Review date: 2026-10-30
Status: OFFICIAL_DOCUMENT_ROUTE_IDENTIFIED / RUNTIME_UNVERIFIED

Official Kiwoom API detail pages:
- https://openapi.kiwoom.com/m/guide/apiguide/08/ka10081
- https://openapi.kiwoom.com/m/guide/apiguide/08/ka10086

Read-only inspection of both official pages confirmed:
- Displayed URL: /api/dostk/acnt
- Request API identifier header: api-id
- Neither page contained /api/dostk/chart.

The earlier /api/dostk/chart claim came from
secondary reference material, not these official pages.

Documentation-level route comparison: RESOLVED.
Actual endpoint execution and server acceptance: UNVERIFIED.

The existing local provider validation modules do not
implement a live HTTP transport or authorize API dispatch.

This record does not authorize real API calls, broker
access, source certification, adjustment certification,
analysis, dashboard use, persistence, database rebuild,
or automatic provider fallback.

## KIWOOM official Q&A 7961 reply evidence (2026-11-04)

Status: OFFICIAL_SITE_REPLY_OBSERVED / PDF_CAPTURE_REVIEWED / INDEPENDENT_AUTHENTICITY_UNVERIFIED

### Evidence identity

- Provider: KIWOOM Securities REST API
- Q&A inquiry number: 7961 (user-reported inquiry identifier)
- Reply timestamp displayed: 2026-11-02 15:05
- Reply author displayed: KIWOOM Securities operator
- Source: official REST API Q&A website
- Source page: https://openapi.kiwoom.com/board/Board0201View?dummyVal=0
- Evidence artifact: user-supplied two-page PDF print of the Q&A page
- PDF was visually reviewed; no independent cryptographic or server-side authenticity verification was performed.
- The PDF is not committed to the repository by this change.

### Provider reply: permitted-use scope

The reply states that individual customers may use REST API data
for their own investment purposes.

The reply indicates:
- No data-category differentiation or storage-period restriction.
- Third-party provision and redistribution are prohibited.
- Commercial use requires a separate information-use agreement.
- Additional usage terms and notices may apply.

These statements are recorded as provider guidance for personal use.
They do not independently establish a blanket operational entitlement
for every account, endpoint, or deployment.

### Provider reply: technical limitations

- REST API data is described as corresponding to HTS data.
- The provider recommends checking the official API guide
  and comparing REST API TR results with the matching HTS screens.
- The reply does not certify actual historical observations.
- No complete corporate-action adjustment methodology is provided.
- Adjusted/unadjusted historical price results remain unverified.
- Actual endpoint responses, provenance, calendar, completeness,
  and price normalization remain unverified.
- Rate limits and connection guidance are referred to other
  official notices and FAQ entries.

### Platform decision

- PERSONAL_USE_GUIDANCE: OFFICIAL_REPLY_OBSERVED
- SOURCE_AUTHENTICITY: INDEPENDENTLY_UNVERIFIED
- REAL_PRICE_PROVENANCE: UNVERIFIED
- ADJUSTMENT_CERTIFICATION: PENDING
- KIS_LICENSE_SCOPE: SEPARATELY_UNVERIFIED
- LIVE_API_EXECUTION: DENIED
- PRICE_ANALYSIS: DENIED
- PRICE_PERSISTENCE: DENIED
- OPERATING_DB_ACCESS: PROHIBITED
- HOST_PYTHON_EXECUTION: DENIED
- BROKER_CALLS: DENIED
- MAIN_MERGE: NOT_AUTHORIZED

This evidence updates the earlier reply-pending history without
retroactively modifying historical records or granting operational
authority.

## KIWOOM official Q&A 8123 preserved evidence

Evidence record date: 2026-11-04
Status: PDF_PRESERVED / SHA256_VERIFIED / CONTENT_REVIEW_PENDING

- Provider: KIWOOM Securities REST API
- Official Q&A inquiry number: 8123
- Reply: user-confirmed received
- Preserved PDF filename:
  KIWOOM_REST_API_QA_8123_Official_Reply_20261104.pdf
- Preserved PDF location (office PC, outside Git):
  D:\Projects\official-api-evidence\kiwoom
- PDF size: 93940 bytes
- SHA256:
  BBE8A08D5E5959D7DA66CA29B421E2D696FCD8AAD4809A5A63C265A72E6A057A
- Original PDF remains on the user's desktop.
- Preserved copy hash matched the original.
- PDF header check: PASS.
- Independent provider authenticity: NOT_VERIFIED.
- Full PDF transcription: PENDING; screenshot-based scope assessment recorded below.

This record establishes a reproducible file-integrity baseline.
It does not independently authenticate the provider response.

Data-use permission, adjustment policy, actual market-data
provenance, analysis, persistence, and operational authorization
must be assessed separately before any execution.

- HOST_PYTHON_EXECUTION: DENIED
- OPERATING_DB_ACCESS: PROHIBITED
- BROKER_CALLS: DENIED
- LIVE_API_EXECUTION: DENIED
- MAIN_MERGE: NOT_AUTHORIZED

### Q&A 8123 screenshot-based permitted-use assessment

Assessment date: 2026-11-04
Status: USER_SUPPLIED_SCREENSHOT_REVIEWED / PDF_FULL_TEXT_NOT_VERIFIED

The user-supplied official Q&A reply screenshot was reviewed.
The following is a paraphrase of the visible reply, not an
independently authenticated provider transcript:

- Individual customers may use REST API data for investment
  of their own assets.
- The visible reply indicates no separate restrictions on
  automated collection by data category or retention period.
- Provision or redistribution to third parties is prohibited.
- Commercial information provision and separate service
  agreements are not authorized by this personal-use guidance.
- REST API data is described as corresponding to HTS data.
- The provider recommends consulting API and HTS guides
  and comparing matching TR results with HTS screens.

Interpretation boundaries:

- PERSONAL_INVESTMENT_USE_GUIDANCE: OBSERVED
- AUTOMATED_COLLECTION_GUIDANCE: OBSERVED
- STORAGE_PERIOD_GUIDANCE: OBSERVED
- THIRD_PARTY_REDISTRIBUTION: PROHIBITED
- FULL_PDF_TEXT_REVIEW: PENDING
- INDEPENDENT_PROVIDER_AUTHENTICITY: UNVERIFIED
- SPECIFIC_ANALYSIS_AND_BACKTEST_SCOPE: NOT_INDEPENDENTLY_CERTIFIED
- ACTUAL_PRICE_PROVENANCE: UNVERIFIED
- CORPORATE_ACTION_ADJUSTMENT: PENDING
- HISTORICAL_CALENDAR_AND_COMPLETENESS: PENDING
- KIS_PERMISSION_SCOPE: SEPARATELY_UNVERIFIED
- LIVE_API_EXECUTION: DENIED
- REAL_PRICE_COLLECTION: DENIED
- PRICE_ANALYSIS_AND_PERSISTENCE: DENIED
- OPERATING_DB_ACCESS: PROHIBITED
- BROKER_CALLS: DENIED
- MAIN_MERGE: NOT_AUTHORIZED

This assessment updates the current evidence state without
retroactively rewriting historical reply-pending records.
It does not authorize execution, database construction,
external distribution, or deployment.

## KIWOOM HTS TR Mapping Evidence - 2026-11-04

Status: OFFICIAL_DOCUMENT_OBSERVED / REAL_PRICE_UNVERIFIED

Official material:
- Title: 영웅문4(HTS) - 키움 REST API, 키움 OPEN API + TR 매칭
- Published update date: 2025-11-06
- Source: https://openapi.kiwoom.com/
- Evidence: user-provided official notice attachments, PDF and XLSX

Documented HTS mappings:
- ka10081: 6600, 0613, 0615, 0617
- ka10086: 0124
- ka40003: 0277, 0279 (ETF comparison candidate only)

Suggested comparison targets:
- ka10081: HTS 0613, with 6600 as secondary reference
- ka10086: HTS 0124
- ETF-specific supplemental reference: HTS 0277

The mapping document identifies corresponding HTS screens.
It does not independently certify:
- Actual REST API response authenticity
- Historical OHLCV numerical equivalence
- Adjusted-price methodology or adjustment factors
- Corporate-action effective dates and retroactive adjustments
- Official exchange trading-calendar alignment
- ETF distribution adjustment policy

Existing offline contracts remain fail-closed.

INDEPENDENT_SOURCE_VERIFICATION: PENDING
ORIGINAL_RESPONSE_VERIFICATION: PENDING
ADJUSTMENT_CERTIFICATION: PENDING
CORPORATE_ACTION_CERTIFICATION: PENDING
OFFICIAL_TRADING_DAY_CERTIFICATION: PENDING
ANALYSIS_AUTHORIZED: FALSE
PERSISTENCE_AUTHORIZED: FALSE
DATABASE_REBUILD_AUTHORIZED: FALSE
LIVE_API_EXECUTION_AUTHORIZED: FALSE
BROKER_EXECUTION_AUTHORIZED: FALSE

## KIWOOM official Q&A 8180 registration

Evidence date: 2026-11-05
Status: OFFICIAL_QA_LISTING_SCREENSHOT_OBSERVED / REPLY_PENDING

- Provider: KIWOOM Securities REST API
- Inquiry number: 8180
- Registration timestamp displayed: 2026-11-05 10:33
- Inquiry category displayed: API specification (TR-related)
- Evidence: user-supplied official Q&A listing screenshot
- Previous related inquiries: 7961, 8123
- Scope: historical price provenance, adjustment and corporate
  actions, trading calendar, ETF handling, and personal-use
  analysis/backtesting permissions.
- Full submitted inquiry text: NOT_INDEPENDENTLY_VERIFIED
- Provider reply: NOT_YET_OBSERVED
- Independent provider authenticity: UNVERIFIED
- Real market-data provenance: UNVERIFIED
- Adjustment certification: PENDING
- Corporate-action certification: PENDING
- Official trading-day certification: PENDING
- License scope certification: PENDING
- Real API execution: DENIED
- Price analysis and persistence: DENIED
- Operating database access: PROHIBITED
- Broker calls: DENIED
- Main merge: NOT_AUTHORIZED

This registration records the observed inquiry listing only.
It does not authenticate a provider reply, establish market-data
provenance, or grant operational authority.

## KIWOOM Q&A 8180 reply and Q&A 8245 registration

Evidence review date: 2026-11-06
Status: USER_CONFIRMED / INDEPENDENT_AUTHENTICITY_UNVERIFIED

### Q&A 8180 reply

- Inquiry number: 8180
- Reply timestamp displayed: 2026-11-05 15:24
- Reply evidence: user-supplied three-page PDF
- User confirmed the reply belongs to Q&A 8180.
- Provider stated that KIWOOM REST API provides HTS data.
- Detailed technical clarification was not provided.
- Original market-data provenance: UNVERIFIED
- Adjustment and corporate-action certification: PENDING
- Official trading-calendar certification: PENDING
- Specific analysis and backtest authorization: UNVERIFIED
- Independent provider authenticity: UNVERIFIED

### Q&A 8245 registration

- Inquiry number: 8245
- Registration: USER_CONFIRMED
- Question category: OTHER
- Subject: personal-use automated historical-price collection,
  local storage, analysis, and strategy backtesting permissions.
- Official reply: PENDING
- Additional separate questions on adjustment, trading days,
  and REST/HTS consistency: NOT_YET_REGISTERED

### Safety boundary

- REAL_PRICE_COLLECTION: DENIED
- PRICE_ANALYSIS_AND_PERSISTENCE: DENIED
- OPERATING_DB_ACCESS: PROHIBITED
- HOST_PYTHON_EXECUTION: DENIED
- BROKER_CALLS: DENIED
- MAIN_MERGE: NOT_AUTHORIZED

This record preserves earlier historical evidence states.
It does not establish independent certification or authorize execution.
