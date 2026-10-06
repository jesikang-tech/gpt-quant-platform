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
from contextlib import closing
from decimal import Decimal

import config
from datetime import date
from pathlib import Path
from typing import Optional

from config import (
    MIN_UPTREND_RATIO,
)
from factor_engine import (
    calculate_return,
    calculate_return_score,
    calculate_trend_score,
    calculate_slope_score,
    calculate_uptrend_ratio,
)

def _get_replay_connection():
    """Open the configured database read-only; never create a missing database."""
    uri = Path(config.DATABASE_PATH).resolve().as_uri() + "?mode=ro"
    return sqlite3.connect(uri, uri=True, timeout=30)


def get_all_etf_tickers():
    with closing(_get_replay_connection()) as conn:
        rows = conn.execute(
            "SELECT ticker FROM etf_info ORDER BY ticker"
        ).fetchall()
    return [row[0] for row in rows]


def get_etf_prices(ticker, end_date=None):
    with closing(_get_replay_connection()) as conn:
        return conn.execute(
            """
            SELECT date, close_price
            FROM etf_prices
            WHERE ticker = ? AND (? IS NULL OR date <= ?) AND strftime('%w', date) NOT IN ('0', '6')
            ORDER BY date
            """,
            (ticker, end_date, end_date),
        ).fetchall()


def _get_latest_market_date() -> Optional[str]:
    """Return the latest available price date without modifying the DB."""
    with closing(_get_replay_connection()) as conn:
        row = conn.execute(
            "SELECT MAX(date) FROM etf_prices"
        ).fetchone()

    return row[0] if row and row[0] else None


def _get_etf_name_map() -> dict:
    """Return ETF ticker/name mapping using a read-only DB connection."""
    with closing(_get_replay_connection()) as conn:
        rows = conn.execute(
            "SELECT ticker, name FROM etf_info"
        ).fetchall()

    return {
        ticker: name
        for ticker, name in rows
    }


def _is_trading_day(analysis_date: str) -> bool:
    """Return whether the requested date exists in the ETF market-price data."""
    with closing(_get_replay_connection()) as conn:
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
    Missing or non-positive exact-date baselines return (None, None, 0).
    No database writes are performed.
    """
    conn = _get_replay_connection()

    try:
        rows = conn.execute(
            """
            SELECT date, close_price
            FROM etf_prices
            WHERE ticker = ?
              AND date >= ?
              AND strftime('%w', date) NOT IN ('0', '6')
            ORDER BY date
            LIMIT 41
            """,
            (ticker, analysis_date),
        ).fetchall()
    finally:
        conn.close()

    if not rows or rows[0][0] != analysis_date:
        return None, None, 0

    base_price = float(rows[0][1])
    if base_price <= 0:
        return None, None, 0

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


def _get_reality_test(ticker: str, analysis_date: str, period: str) -> dict:
    """Evaluate an exact OHLCV Close baseline and future OHLCV observations.

    Percent returns are exposed in percentage points. Missing baselines leave
    statuses null; missing High never supplies a hit. A completed window with
    no observed High hit is FAIL only with complete High coverage; otherwise
    High is indeterminate, independently of the Close result.
    """
    settings = _get_period_config(period)
    window = settings["lookback_trading_days"]
    result = {
        "available": False,
        "unavailable_reason": None,
        "window_days": window,
        "target_return_pct": settings["return_threshold"],
        "observed_days": 0,
        "high_observed_days": 0,
        "max_close_return_pct": None,
        "endpoint_close_return_pct": None,
        "high_status": None,
        "high_unavailable_reason": None,
        "high_first_hit_day": None,
        "close_status": None,
        "close_unavailable_reason": None,
        "close_first_hit_day": None,
    }
    with closing(_get_replay_connection()) as conn:
        has_ohlcv = conn.execute(
            "SELECT 1 FROM sqlite_master WHERE type = 'table' AND name = 'etf_ohlcv_prices'"
        ).fetchone()
        if not has_ohlcv:
            result["unavailable_reason"] = "MISSING_BASELINE"
            return result
        baseline = conn.execute(
            "SELECT close_price FROM etf_ohlcv_prices WHERE ticker = ? AND date = ?",
            (ticker, analysis_date),
        ).fetchone()
        if baseline is None:
            result["unavailable_reason"] = "MISSING_BASELINE"
            return result
        if baseline[0] is None:
            result["unavailable_reason"] = "INVALID_BASELINE"
            return result
        base = Decimal(str(baseline[0]))
        if not base.is_finite() or base <= 0:
            result["unavailable_reason"] = "INVALID_BASELINE"
            return result
        rows = conn.execute(
            "SELECT date, close_price, high_price FROM etf_ohlcv_prices "
            "WHERE ticker = ? AND date > ? AND strftime('%w', date) NOT IN ('0', '6') ORDER BY date LIMIT ?",
            (ticker, analysis_date, window),
        ).fetchall()

    target = Decimal(str(settings["return_threshold"])) / 100
    close_returns = []
    for day, (observation_date, close, high) in enumerate(rows, start=1):
        close_value = Decimal(str(close)) if close is not None else None
        close_return = (
            close_value / base - 1
            if close_value is not None and close_value.is_finite() else None
        )
        close_returns.append(close_return)
        if close_return is not None and close_return >= target and result["close_first_hit_day"] is None:
            result["close_first_hit_day"] = day
        if high is not None:
            result["high_observed_days"] += 1
            if Decimal(str(high)) / base - 1 >= target and result["high_first_hit_day"] is None:
                result["high_first_hit_day"] = day

    result["available"] = True
    result["observed_days"] = len(rows)
    complete = len(rows) == window
    for kind in ("high", "close"):
        result[f"{kind}_status"] = (
            "PASS" if result[f"{kind}_first_hit_day"] is not None
            else "FAIL" if complete else "PENDING"
        )
    if (complete and result["high_first_hit_day"] is None
            and result["high_observed_days"] < window):
        result["high_status"] = None
        result["high_unavailable_reason"] = "INCOMPLETE_HIGH_COVERAGE"
    if complete and result["close_first_hit_day"] is None and None in close_returns:
        result["close_status"] = None
        result["close_unavailable_reason"] = "INCOMPLETE_CLOSE_COVERAGE"
    valid_close_returns = [value for value in close_returns if value is not None]
    if valid_close_returns:
        result["max_close_return_pct"] = float(max(valid_close_returns) * 100)
    if complete and close_returns[-1] is not None:
        result["endpoint_close_return_pct"] = float(close_returns[-1] * 100)
    return result


def get_current_analysis_data(
    limit: int = 10,
    analysis_date: Optional[str] = None,
    period: str = "3m",
    sort_by: str = "final_score",
) -> dict:
    """
    Calculate current ETF scores entirely in memory.

    No production database writes are performed.
    """

    if limit < 1:
        raise ValueError("limit must be >= 1")

    allowed_sort_fields = {
        "final_score",
        "return",
        "trend_score",
        "slope_score",
    }

    if sort_by not in allowed_sort_fields:
        raise ValueError("Invalid sort_by.")

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
        }

        all_scores.append(row)

        if selection_pass:
            selection_count += 1
            selection_scores.append(row)

    if sort_by == "final_score":
        sort_fields = [
            "final_score",
            "return_score",
            "trend_score",
            "slope_score",
        ]
    else:
        sort_fields = [
            sort_by,
            *[
                field
                for field in (
                    "final_score",
                    "return_score",
                    "trend_score",
                    "slope_score",
                )
                if field != sort_by
            ],
        ]

    def score_sort_key(row):
        return tuple(row[field] for field in sort_fields)

    all_scores.sort(
        key=score_sort_key,
        reverse=True,
    )

    selection_scores.sort(
        key=score_sort_key,
        reverse=True,
    )

    current_score_top = all_scores[:limit]

    market_regime_scores = sorted(
        all_scores,
        key=lambda row: (
            row["final_score"],
            row["return_score"],
            row["trend_score"],
            row["slope_score"],
        ),
        reverse=True,
    )[:10]

    for row in current_score_top:
        price, future_performance, future_performance_days = (
            _get_future_performance(
                row["ticker"],
                resolved_date,
            )
        )
        row["price"] = price
        row["future_performance"] = future_performance
        row["future_performance_days"] = future_performance_days
        row["reality_test"] = _get_reality_test(row["ticker"], resolved_date, period)

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
        "current_score_top": current_score_top,
        "market_regime_scores": market_regime_scores,
        "db_write": False,
    }
