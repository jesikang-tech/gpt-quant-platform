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
