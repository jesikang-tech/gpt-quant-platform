"""Read-only cross-table ETF close-price quality diagnostics."""

import sqlite3
from contextlib import closing
from decimal import Decimal, InvalidOperation
from pathlib import Path


def _valid_price(value):
    if value is None:
        return False
    try:
        number = Decimal(str(value))
    except (InvalidOperation, ValueError, TypeError):
        return False
    return number.is_finite() and number > 0


def check_price_quality(database_path, ticker, analysis_date):
    """Compare stored Close values without modifying either source."""

    path = Path(database_path).resolve()

    result = {
        "ticker": ticker,
        "date": analysis_date,
        "status": None,
        "price_source_verified": False,
    }

    with closing(
        sqlite3.connect(path.as_uri() + "?mode=ro", uri=True)
    ) as conn:
        legacy = conn.execute(
            "SELECT close_price FROM etf_prices "
            "WHERE ticker = ? AND date = ?",
            (ticker, analysis_date),
        ).fetchone()

        ohlcv = conn.execute(
            "SELECT close_price FROM etf_ohlcv_prices "
            "WHERE ticker = ? AND date = ?",
            (ticker, analysis_date),
        ).fetchone()

    if legacy is None or ohlcv is None:
        result["status"] = "MISSING_SOURCE"
        return result

    if not _valid_price(legacy[0]) or not _valid_price(ohlcv[0]):
        result["status"] = "INVALID_PRICE"
        return result

    legacy_price = Decimal(str(legacy[0]))
    ohlcv_price = Decimal(str(ohlcv[0]))

    result["status"] = (
        "MATCH" if legacy_price == ohlcv_price else "MISMATCH"
    )

    return result


def summarize_price_quality_by_date(database_path, analysis_date):
    """Summarize cross-table close-price consistency for one date."""

    path = Path(database_path).resolve()

    counts = {
        "date": analysis_date,
        "total": 0,
        "MATCH": 0,
        "MISMATCH": 0,
        "MISSING_SOURCE": 0,
        "INVALID_PRICE": 0,
        "price_source_verified": False,
    }

    with closing(
        sqlite3.connect(path.as_uri() + "?mode=ro", uri=True)
    ) as conn:
        rows = conn.execute(
            """
            SELECT
                p.close_price,
                o.close_price,
                p.ticker,
                o.ticker
            FROM etf_prices AS p
            LEFT JOIN etf_ohlcv_prices AS o
              ON p.ticker = o.ticker AND p.date = o.date
            WHERE p.date = ?

            UNION ALL

            SELECT
                p.close_price,
                o.close_price,
                p.ticker,
                o.ticker
            FROM etf_ohlcv_prices AS o
            LEFT JOIN etf_prices AS p
              ON p.ticker = o.ticker AND p.date = o.date
            WHERE o.date = ?
              AND p.ticker IS NULL
            """,
            (analysis_date, analysis_date),
        )

        for legacy_price, ohlcv_price, legacy_ticker, ohlcv_ticker in rows:
            counts["total"] += 1

            if legacy_ticker is None or ohlcv_ticker is None:
                status = "MISSING_SOURCE"
            elif not _valid_price(legacy_price) or not _valid_price(ohlcv_price):
                status = "INVALID_PRICE"
            elif Decimal(str(legacy_price)) == Decimal(str(ohlcv_price)):
                status = "MATCH"
            else:
                status = "MISMATCH"

            counts[status] += 1

    return counts
