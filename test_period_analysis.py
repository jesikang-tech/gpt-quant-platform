import pytest

from core.period_analysis import (
    analyze_period,
    analyze_periods,
    calculate_period_return,
    calculate_period_uptrend_ratio,
    calculate_trend_state,
)


def make_prices(count, start=100.0, end=None):
    if end is None:
        end = start + count - 1

    step = (end - start) / (count - 1)
    return [start + i * step for i in range(count)]


def test_period_return():
    prices = [100, 105]
    assert calculate_period_return(prices) == pytest.approx(5.0)


def test_period_uptrend_ratio():
    prices = [100, 101, 100, 102]
    assert calculate_period_uptrend_ratio(prices) == pytest.approx(2 / 3 * 100)


def test_20_day_threshold_boundary():
    prices = make_prices(20, 100, 105)
    result = analyze_period(prices, 20, 0.05)

    assert result["status"] == "ANALYZED"
    assert result["required_data"] == 20
    assert result["available_data"] == 20
    assert result["threshold_pass"] is True


def test_insufficient_data():
    prices = make_prices(19)

    results = analyze_periods(prices)

    assert results["20"]["status"] == "INSUFFICIENT_DATA"
    assert results["40"]["status"] == "INSUFFICIENT_DATA"
    assert results["60"]["status"] == "INSUFFICIENT_DATA"


def test_partial_period_data():
    prices = make_prices(40)

    results = analyze_periods(prices)

    assert results["20"]["status"] == "ANALYZED"
    assert results["40"]["status"] == "ANALYZED"
    assert results["60"]["status"] == "INSUFFICIENT_DATA"


def test_all_periods_with_60_prices():
    prices = make_prices(60)

    results = analyze_periods(prices)

    assert results["20"]["status"] == "ANALYZED"
    assert results["40"]["status"] == "ANALYZED"
    assert results["60"]["status"] == "ANALYZED"


def test_trend_state():
    periods = {
        "20": {"return_rate": 6.0},
        "40": {"return_rate": 12.0},
        "60": {"return_rate": 20.0},
    }
    assert calculate_trend_state(periods) == "UPTREND"

    periods["20"]["return_rate"] = 3.0
    assert calculate_trend_state(periods) == "SLOWING"

    periods["20"]["return_rate"] = -2.0
    assert calculate_trend_state(periods) == "CORRECTION"

    periods["60"]["return_rate"] = 10.0
    assert calculate_trend_state(periods) == "DOWNTREND"
