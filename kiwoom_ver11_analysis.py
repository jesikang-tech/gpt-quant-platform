"""Explicit KIWOOM Ver1.1 offline scoring adapter.

Accepts caller-supplied, validated close-price tuples only.
No HTTP, database, persistence, broker, or implicit source substitution.
This is a scoring component, not the complete Ver1.1 dashboard.
"""

from decimal import Decimal

from factor_engine import (
    calculate_return,
    calculate_return_score,
    calculate_trend_score,
    calculate_slope_score,
    calculate_uptrend_ratio,
    calculate_final_score,
)


_PERIODS = {
    "1m": (20, 5.0),
    "2m": (40, 10.0),
    "3m": (60, 15.0),
}


def score_kiwoom_ver11_close_prices(
    ticker, dated_closes, *, analysis_date, period="3m"
):
    """Score one ticker using explicit ascending (ISO date, Decimal) rows."""
    if type(ticker) is not str or not ticker:
        raise ValueError("Invalid ticker")
    if period not in _PERIODS:
        raise ValueError("Unsupported period")
    if type(analysis_date) is not str:
        raise ValueError("Invalid analysis date")

    from datetime import date

    try:
        parsed_date = date.fromisoformat(analysis_date)
    except ValueError as exc:
        raise ValueError("Invalid analysis date") from exc
    if parsed_date.isoformat() != analysis_date:
        raise ValueError("Noncanonical analysis date")

    if type(dated_closes) not in (tuple, list):
        raise ValueError("Invalid price collection")

    previous_date = None
    accepted = []
    for row in dated_closes:
        if type(row) not in (tuple, list) or len(row) != 2:
            raise ValueError("Invalid price row")
        observation_date, close = row
        if type(observation_date) is not str:
            raise ValueError("Invalid observation date")
        try:
            parsed_observation = date.fromisoformat(observation_date)
        except ValueError as exc:
            raise ValueError("Invalid observation date") from exc
        if parsed_observation.isoformat() != observation_date:
            raise ValueError("Noncanonical observation date")
        if previous_date is not None and observation_date <= previous_date:
            raise ValueError("Prices must have unique ascending dates")
        previous_date = observation_date
        if type(close) is not Decimal or not close.is_finite() or close <= 0:
            raise ValueError("Invalid close price")
        if observation_date <= analysis_date:
            accepted.append(close)

    window, threshold = _PERIODS[period]
    if len(accepted) < window:
        return {
            "ticker": ticker,
            "analysis_date": analysis_date,
            "period": period,
            "available": False,
            "observed_days": len(accepted),
            "required_days": window,
        }

    prices = accepted[-window:]
    return_rate = calculate_return(prices[0], prices[-1])
    return_score = calculate_return_score(return_rate)
    trend_score = calculate_trend_score(prices)
    slope_score = calculate_slope_score(prices)
    uptrend_ratio = calculate_uptrend_ratio(prices)
    final_score = calculate_final_score(
        return_score, trend_score, slope_score
    )
    return {
        "ticker": ticker,
        "analysis_date": analysis_date,
        "period": period,
        "available": True,
        "observed_days": len(prices),
        "required_days": window,
        "return": round(float(return_rate), 2),
        "return_score": return_score,
        "trend_score": trend_score,
        "slope_score": slope_score,
        "uptrend_ratio": uptrend_ratio,
        "final_score": final_score,
        "selection_pass": (
            return_rate >= threshold and uptrend_ratio >= 70.0
        ),
        "source": "KIWOOM",
        "db_write": False,
    }
