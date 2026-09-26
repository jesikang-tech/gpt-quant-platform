"""Explicitly invoked OHLCV-only backfill; no default database or provider."""

import sqlite3
from contextlib import closing
from math import isfinite
from pathlib import Path

import pandas as pd


class OHLCVBackfill:
    """The caller supplies an existing, initialized DB and a get_price provider.

    No schema initialization or provider request occurs on construction/import.
    A ticker is atomic; failures roll back that ticker and can be retried.
    """

    def __init__(self, db_path, provider):
        self.db_path = Path(db_path).resolve()
        self.provider = provider

    def _connection(self):
        conn = sqlite3.connect(self.db_path.as_uri() + "?mode=rw", uri=True, timeout=30)

        def authorize(action, table, column, database, source):
            if action in (sqlite3.SQLITE_SELECT, sqlite3.SQLITE_READ,
                          sqlite3.SQLITE_FUNCTION, sqlite3.SQLITE_TRANSACTION):
                return sqlite3.SQLITE_OK
            if (action in (sqlite3.SQLITE_INSERT, sqlite3.SQLITE_UPDATE)
                    and database == "main" and table == "etf_ohlcv_prices"
                    and source is None):
                return sqlite3.SQLITE_OK
            return sqlite3.SQLITE_DENY

        conn.set_authorizer(authorize)
        return conn

    def get_targets(self):
        """Return ticker-specific inclusive legacy date ranges, ordered by ticker."""
        with closing(self._connection()) as conn:
            return conn.execute(
                "SELECT ticker, MIN(date), MAX(date) FROM etf_prices "
                "GROUP BY ticker ORDER BY ticker"
            ).fetchall()

    def backfill_ticker(self, ticker):
        result = {"ticker": ticker, "status": "SKIPPED", "rows_written": 0,
                  "rows_skipped": 0, "error": None}
        try:
            with closing(self._connection()) as conn:
                start, end = conn.execute(
                    "SELECT MIN(date), MAX(date) FROM etf_prices WHERE ticker = ?",
                    (ticker,),
                ).fetchone()
                if start is None:
                    return result
                result.update(start_date=start, end_date=end)
                # Fail before fetching if the separate table has not been initialized.
                conn.execute("SELECT ticker FROM etf_ohlcv_prices LIMIT 0")
                frame = self.provider.get_price(ticker, start, end)
                # MIN/MAX bounds the request; only exact legacy dates may persist.
                legacy_dates = {
                    row[0] for row in conn.execute(
                        "SELECT date FROM etf_prices WHERE ticker = ?", (ticker,)
                    ).fetchall()
                }
                rows = []
                for index, row in frame.iterrows():
                    observation_date = pd.Timestamp(index)
                    if pd.isna(observation_date):
                        raise ValueError("Invalid source date")
                    observation_date = observation_date.date().isoformat()
                    if not start <= observation_date <= end or observation_date not in legacy_dates:
                        result["rows_skipped"] += 1
                        continue
                    values = []
                    for field in ("Open", "High", "Low", "Close", "Volume"):
                        value = row.get(field)
                        value = None if pd.isna(value) else float(value)
                        if value is not None and not isfinite(value):
                            raise ValueError(f"Non-finite {field} at {observation_date}")
                        values.append(value)
                    rows.append((ticker, observation_date, *values))
                with conn:
                    conn.executemany(
                        """
                        INSERT INTO etf_ohlcv_prices
                            (ticker, date, open_price, high_price, low_price, close_price, volume)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                        ON CONFLICT(ticker, date) DO UPDATE SET
                            open_price = COALESCE(excluded.open_price, etf_ohlcv_prices.open_price),
                            high_price = COALESCE(excluded.high_price, etf_ohlcv_prices.high_price),
                            low_price = COALESCE(excluded.low_price, etf_ohlcv_prices.low_price),
                            close_price = COALESCE(excluded.close_price, etf_ohlcv_prices.close_price),
                            volume = COALESCE(excluded.volume, etf_ohlcv_prices.volume)
                        """,
                        rows,
                    )
                result.update(status="SUCCEEDED" if rows else "SKIPPED", rows_written=len(rows))
        except Exception as exc:
            result.update(status="FAILED", error=f"{type(exc).__name__}: {exc}")
        return result

    def backfill(self, tickers=None):
        """Process all legacy targets or explicit tickers; report failures individually.

        rows_written counts source rows successfully upserted (including updates).
        """
        if tickers is None:
            tickers = [ticker for ticker, _, _ in self.get_targets()]
        results = [self.backfill_ticker(ticker) for ticker in dict.fromkeys(tickers)]
        return {
            "attempted": len(results),
            "succeeded": sum(r["status"] == "SUCCEEDED" for r in results),
            "failed": sum(r["status"] == "FAILED" for r in results),
            "skipped": sum(r["status"] == "SKIPPED" for r in results),
            "results": results,
        }
