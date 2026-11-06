"""Synthetic-only tests for explicit KIWOOM Ver1.1 scoring."""

from datetime import date, timedelta
from decimal import Decimal

import pytest

from factor_engine import (
    calculate_final_score,
    calculate_return,
    calculate_return_score,
    calculate_slope_score,
    calculate_trend_score,
    calculate_uptrend_ratio,
)
from kiwoom_ver11_analysis import score_kiwoom_ver11_close_prices


def _rows(count=65):
    start = date(2026, 8, 1)
    return tuple(
        (
            (start + timedelta(days=i)).isoformat(),
            Decimal("100") + Decimal(i),
        )
        for i in range(count)
    )


def test_reuses_existing_factor_calculations():
    rows = _rows()
    result = score_kiwoom_ver11_close_prices(
        "005930", rows, analysis_date="2026-11-06"
    )
    prices = [close for _, close in rows[-60:]]
    return_rate = calculate_return(prices[0], prices[-1])
    return_score = calculate_return_score(return_rate)
    trend_score = calculate_trend_score(prices)
    slope_score = calculate_slope_score(prices)
    assert result["available"] is True
    assert result["return"] == round(float(return_rate), 2)
    assert result["return_score"] == return_score
    assert result["trend_score"] == trend_score
    assert result["slope_score"] == slope_score
    assert result["uptrend_ratio"] == calculate_uptrend_ratio(prices)
    assert result["final_score"] == calculate_final_score(
        return_score, trend_score, slope_score
    )
    assert result["source"] == "KIWOOM"
    assert result["db_write"] is False


def test_future_prices_do_not_affect_historical_score():
    rows = _rows()
    cutoff = rows[59][0]
    expected = score_kiwoom_ver11_close_prices(
        "005930", rows[:60], analysis_date=cutoff
    )
    actual = score_kiwoom_ver11_close_prices(
        "005930", rows, analysis_date=cutoff
    )
    assert actual == expected


def test_insufficient_history_returns_unavailable():
    result = score_kiwoom_ver11_close_prices(
        "005930", _rows(19), analysis_date="2026-11-06", period="1m"
    )
    assert result["available"] is False
    assert result["observed_days"] == 19
    assert result["required_days"] == 20


@pytest.mark.parametrize("invalid", [
    Decimal("0"),
    Decimal("-1"),
    Decimal("NaN"),
    Decimal("Infinity"),
    "100",
])
def test_invalid_close_rejected(invalid):
    rows = (("2026-11-05", invalid),)
    with pytest.raises(ValueError):
        score_kiwoom_ver11_close_prices(
            "005930", rows, analysis_date="2026-11-06"
        )


def test_duplicate_dates_rejected():
    with pytest.raises(ValueError):
        score_kiwoom_ver11_close_prices(
            "005930",
            (("2026-11-05", Decimal("100")),
             ("2026-11-05", Decimal("101"))),
            analysis_date="2026-11-06",
        )


def test_invalid_period_rejected():
    with pytest.raises(ValueError):
        score_kiwoom_ver11_close_prices(
            "005930", _rows(), analysis_date="2026-11-06", period="4m"
        )
