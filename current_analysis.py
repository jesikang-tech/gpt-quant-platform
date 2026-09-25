"""
Current ETF Analysis
--------------------
Read-only current market analysis.

This module does NOT write to:
- etf_scores
- etf_score_history
- etf_ranking_history
- any production database table

It reads the latest available ETF price date and calculates
current scores in memory.
"""

import sqlite3
from datetime import date
from pathlib import Path
from typing import Optional

from config import (
    DATABASE_DIR,
    MIN_UPTREND_RATIO,
)
from factor_engine import (
    calculate_return,
    calculate_return_score,
    calculate_trend_score,
    calculate_slope_score,
    calculate_uptrend_ratio,
)
from repository import get_all_etf_tickers, get_etf_prices


def _get_latest_market_date() -> Optional[str]:
    """Return the latest available price date without modifying the DB."""
    db_path = Path(DATABASE_DIR) / "etf.db"

    uri = f"file:{db_path.as_posix()}?mode=ro"

    with sqlite3.connect(uri, uri=True) as conn:
        row = conn.execute(
            "SELECT MAX(date) FROM etf_prices"
        ).fetchone()

    return row[0] if row and row[0] else None


def _get_etf_name_map() -> dict:
    """Return ETF ticker/name mapping using a read-only DB connection."""
    db_path = Path(DATABASE_DIR) / "etf.db"

    uri = f"file:{db_path.as_posix()}?mode=ro"

    with sqlite3.connect(uri, uri=True) as conn:
        rows = conn.execute(
            "SELECT ticker, name FROM etf_info"
        ).fetchall()

    return {
        ticker: name
        for ticker, name in rows
    }


def _is_trading_day(analysis_date: str) -> bool:
    """Return whether the requested date exists in the ETF market-price data."""
    db_path = Path(DATABASE_DIR) / "etf.db"
    uri = f"file:{db_path.as_posix()}?mode=ro"

    with sqlite3.connect(uri, uri=True) as conn:
        row = conn.execute(
            """
            SELECT 1
            FROM etf_prices
            WHERE date = ?
            LIMIT 1
            """,
            (analysis_date,),
        ).fetchone()

    return row is not None


def _normalize_analysis_date(
    analysis_date: Optional[str],
) -> Optional[str]:
    """
    Resolve the analysis date.

    - None -> latest available market date
    - invalid date -> rejected
    - future date -> rejected
    - non-trading date -> rejected
    - trading date -> used as requested
    """
    latest_date = _get_latest_market_date()

    if latest_date is None:
        return None

    if analysis_date is None:
        return latest_date

    try:
        date.fromisoformat(analysis_date)
    except (TypeError, ValueError):
        raise ValueError(
            f"Invalid analysis date: {analysis_date}."
        )

    if analysis_date > latest_date:
        raise ValueError(
            f"Analysis date {analysis_date} is later than "
            f"latest market data date {latest_date}."
        )

    if not _is_trading_day(analysis_date):
        raise ValueError(
            f"Analysis date {analysis_date} is not a trading day."
        )

    return analysis_date


def _get_future_performance(ticker: str, analysis_date: str):
    """
    Historical Replay display-only future performance.

    The scoring calculation remains strictly historical as of analysis_date.
    This helper is used only after the historical Top 10 has been calculated.
    It reads the analysis-date close and up to the next 40 available trading days.
    No database writes are performed.
    """
    conn = sqlite3.connect(
        "file:database/etf.db?mode=ro",
        uri=True,
    )

    try:
        rows = conn.execute(
            """
            SELECT date, close_price
            FROM etf_prices
            WHERE ticker = ?
              AND date >= ?
            ORDER BY date
            LIMIT 41
            """,
            (ticker, analysis_date),
        ).fetchall()
    finally:
        conn.close()

    if not rows:
        return None, None, 0

    base_price = float(rows[0][1])
    future_rows = rows[1:41]

    if not future_rows:
        return base_price, None, 0

    highest_price = max(
        float(row[1])
        for row in future_rows
    )

    future_performance = (
        (highest_price / base_price) - 1.0
    ) * 100.0

    return (
        base_price,
        round(future_performance, 2),
        len(future_rows),
    )


def _get_period_config(period: str) -> dict:
    """Return the current analysis configuration for a supported period."""
    period_config = {
        "1m": {
            "lookback_trading_days": 20,
            "return_threshold": 5.0,
        },
        "2m": {
            "lookback_trading_days": 40,
            "return_threshold": 10.0,
        },
        "3m": {
            "lookback_trading_days": 60,
            "return_threshold": 15.0,
        },
    }

    if period not in period_config:
        raise ValueError("Invalid period. Use 1m, 2m, or 3m.")

    return period_config[period]


def get_current_analysis_data(
    limit: int = 10,
    analysis_date: Optional[str] = None,
    period: str = "3m",
) -> dict:
    """
    Calculate current ETF scores entirely in memory.

    No production database writes are performed.
    """

    if limit < 1:
        raise ValueError("limit must be >= 1")

    resolved_date = _normalize_analysis_date(analysis_date)

    if resolved_date is None:
        return {
            "success": False,
            "message": "No ETF market data is available.",
        }

    selected_period = _get_period_config(period)
    lookback_trading_days = selected_period["lookback_trading_days"]
    return_threshold = selected_period["return_threshold"]
    uptrend_threshold = MIN_UPTREND_RATIO * 100

    tickers = get_all_etf_tickers()
    name_map = _get_etf_name_map()

    total_etf = len(tickers)
    enough_data = 0

    all_scores = []
    selection_count = 0
    selection_scores = []

    for ticker in tickers:
        prices = get_etf_prices(ticker, resolved_date)

        if len(prices) < lookback_trading_days:
            continue

        enough_data += 1

        close_prices = [
            float(price[1])
            for price in prices[-lookback_trading_days:]
        ]

        if len(close_prices) < lookback_trading_days:
            continue

        return_rate = calculate_return(
            close_prices[0],
            close_prices[-1],
        )

        return_score = calculate_return_score(return_rate)
        trend_score = calculate_trend_score(close_prices)
        slope_score = calculate_slope_score(close_prices)
        uptrend_ratio = calculate_uptrend_ratio(close_prices)

        final_score = (
            return_score * 0.4
            + trend_score * 0.3
            + slope_score * 0.3
        )

        return_pct = return_rate
        uptrend_pct = uptrend_ratio

        selection_pass = (
            return_pct >= return_threshold
            and uptrend_pct >= uptrend_threshold
        )

        price, future_performance, future_performance_days = (
            _get_future_performance(
                ticker,
                resolved_date,
            )
        )

        row = {
            "ticker": ticker,
            "name": name_map.get(ticker, ticker),
            "return": round(return_pct, 2),
            "return_score": round(return_score, 2),
            "trend_score": round(trend_score, 2),
            "slope_score": round(slope_score, 2),
            "uptrend_ratio": round(uptrend_pct, 2),
            "final_score": round(final_score, 2),
            "selection_pass": selection_pass,
            "price": price,
            "future_performance": future_performance,
            "future_performance_days": future_performance_days,
        }

        all_scores.append(row)

        if selection_pass:
            selection_count += 1
            selection_scores.append(row)

    all_scores.sort(
        key=lambda x: (
            x["final_score"],
            x["return_score"],
            x["trend_score"],
            x["slope_score"],
        ),
        reverse=True,
    )

    selection_scores.sort(
        key=lambda x: (
            x["final_score"],
            x["return_score"],
            x["trend_score"],
            x["slope_score"],
        ),
        reverse=True,
    )

    return {
        "success": True,
        "analysis_date": resolved_date,
        "market_data_date": resolved_date,
        "period": period,
        "lookback_trading_days": lookback_trading_days,
        "return_threshold": return_threshold,
        "uptrend_threshold": uptrend_threshold,
        "total_etf": total_etf,
        "enough_data": enough_data,
        "selection": {
            "return_threshold": return_threshold,
            "uptrend_threshold": uptrend_threshold,
            "count": selection_count,
            "top": selection_scores[:limit],
        },
        "current_score_top": all_scores[:limit],
        "db_write": False,
    }
