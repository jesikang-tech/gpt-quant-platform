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

def summarize_price_quality_overall(database_path):
    """Summarize all stored ETF prices without modifying the database."""

    from datetime import date

    path = Path(database_path).resolve()

    counts = {
        "total": 0,
        "MATCH": 0,
        "MISMATCH": 0,
        "MISSING_SOURCE": 0,
        "INVALID_PRICE": 0,
        "weekend_rows": 0,
        "price_source_verified": False,
    }

    with closing(
        sqlite3.connect(path.as_uri() + "?mode=ro", uri=True)
    ) as conn:
        rows = conn.execute(
            """
            SELECT
                p.date,
                p.close_price,
                o.close_price,
                p.ticker,
                o.ticker
            FROM etf_prices AS p
            LEFT JOIN etf_ohlcv_prices AS o
              ON p.ticker = o.ticker
             AND p.date = o.date

            UNION ALL

            SELECT
                o.date,
                p.close_price,
                o.close_price,
                p.ticker,
                o.ticker
            FROM etf_ohlcv_prices AS o
            LEFT JOIN etf_prices AS p
              ON p.ticker = o.ticker
             AND p.date = o.date
            WHERE p.ticker IS NULL
            """
        )

        for day, legacy, ohlcv, legacy_ticker, ohlcv_ticker in rows:
            counts["total"] += 1

            try:
                if date.fromisoformat(day).weekday() >= 5:
                    counts["weekend_rows"] += 1
            except (ValueError, TypeError):
                pass

            if legacy_ticker is None or ohlcv_ticker is None:
                status = "MISSING_SOURCE"
            elif not _valid_price(legacy) or not _valid_price(ohlcv):
                status = "INVALID_PRICE"
            elif Decimal(str(legacy)) == Decimal(str(ohlcv)):
                status = "MATCH"
            else:
                status = "MISMATCH"

            counts[status] += 1

    return counts


def rank_price_quality_dates(database_path, limit=10):
    """Rank dates by cross-table close-price mismatch rate."""

    if not isinstance(limit, int) or isinstance(limit, bool) or limit < 1:
        raise ValueError("limit must be a positive integer")

    path = Path(database_path).resolve()

    with closing(
        sqlite3.connect(path.as_uri() + "?mode=ro", uri=True)
    ) as conn:
        dates = [
            row[0]
            for row in conn.execute(
                """
                SELECT date FROM etf_prices
                UNION
                SELECT date FROM etf_ohlcv_prices
                ORDER BY date
                """
            )
        ]

    results = []

    for day in dates:
        summary = summarize_price_quality_by_date(
            database_path,
            day,
        )

        total = summary["total"]
        summary["mismatch_rate"] = (
            summary["MISMATCH"] / total
            if total else 0.0
        )

        results.append(summary)

    results.sort(
        key=lambda item: (
            -item["mismatch_rate"],
            -item["MISMATCH"],
            -item["MISSING_SOURCE"],
            item["date"],
        )
    )

    return results[:limit]
