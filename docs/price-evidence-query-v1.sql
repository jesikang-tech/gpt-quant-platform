-- DESIGN ONLY: EXECUTION DENIED
-- Source database access requires separate explicit approval.
-- Required parameters:
--   :ticker = 0008S0
--   :date   = 2026-09-16
-- This SQL text does not grant database access.

SELECT
    'PRICE' AS source,
    ticker,
    date,
    close_price
FROM etf_prices
WHERE ticker = :ticker
  AND date = :date

UNION ALL

SELECT
    'OHLCV' AS source,
    ticker,
    date,
    close_price
FROM etf_ohlcv_prices
WHERE ticker = :ticker
  AND date = :date;
