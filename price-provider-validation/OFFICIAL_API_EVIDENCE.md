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
