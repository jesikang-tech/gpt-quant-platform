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
