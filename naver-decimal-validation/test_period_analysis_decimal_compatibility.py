"""Intentional red regressions for pure period-analysis Decimal compatibility.

No operational analysis, dashboard, provider, or database entry is invoked.
The real source is loaded only after replacing its configuration/repository
imports with test-local dependencies. These tests do not authorize NAVER use.
"""

from decimal import Context, Decimal, localcontext
from datetime import date, timedelta
import importlib.util
from pathlib import Path
import sys
from types import ModuleType

import pytest


@pytest.fixture
def period_analysis(monkeypatch):
    directory = Path(__file__).resolve().parent
    source = next((root / "core" / "period_analysis.py"
                   for root in (directory, directory.parent)
                   if (root / "core" / "period_analysis.py").is_file()), None)
    assert source is not None, "Stage the real core/period_analysis.py source"
    repository_calls = []

    def forbidden_prices(*args, **kwargs):
        repository_calls.append((args, kwargs))
        raise AssertionError("Operational price reads are forbidden")

    with monkeypatch.context() as patch:
        config = ModuleType("config")
        config.MIN_RETURN_3M = Decimal("0.15")
        repository = ModuleType("repository")
        repository.get_etf_prices = forbidden_prices
        patch.setitem(sys.modules, "config", config)
        patch.setitem(sys.modules, "repository", repository)
        spec = importlib.util.spec_from_file_location("period_decimal_subject", source)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        assert repository_calls == []
        yield module
        assert repository_calls == []


def test_decimal_sub_float_increment_counts_as_up_day(period_analysis):
    prices = [Decimal("1"), Decimal("1.00000000000000000001")]
    assert prices[1] > prices[0]
    assert float(prices[1]) == float(prices[0])
    assert period_analysis.calculate_period_uptrend_ratio(prices) == Decimal("100")


def test_decimal_sub_float_increment_preserves_positive_return(period_analysis):
    prices = [Decimal("1"), Decimal("1.00000000000000000001")]
    with localcontext(Context(prec=50)):
        expected = ((prices[-1] / prices[0]) - Decimal("1")) * Decimal("100")
        result = period_analysis.calculate_period_return(prices)
    assert expected == Decimal("0.000000000000000001")
    assert result == expected


@pytest.mark.parametrize(
    "closing,passes",
    [("105", True), ("104.999999999999999999", False)],
    ids=["exact_threshold", "strictly_below_threshold"],
)
def test_decimal_threshold_uses_exact_pass_fail_boundary(period_analysis, closing, passes):
    prices = [Decimal("100"), Decimal(closing)]
    threshold = Decimal("0.05")
    with localcontext(Context(prec=50)):
        expected_return = ((prices[-1] / prices[0]) - Decimal("1")) * Decimal("100")
        assert (expected_return >= threshold * Decimal("100")) is passes
        result = period_analysis.analyze_period(prices, 2, threshold)
    assert result["status"] == "ANALYZED"
    assert result["return_rate"] == expected_return
    assert result["threshold"] == Decimal("5")
    assert result["threshold_pass"] is passes


def test_legacy_float_threshold_does_not_round_decimal_shortfall_into_pass(period_analysis):
    # Even the existing float-threshold interface must not turn a strictly
    # sub-threshold Decimal observation into a pass via float/10-digit rounding.
    prices = [Decimal("100"), Decimal("104.999999999999999999")]
    with localcontext(Context(prec=50)):
        exact_return = ((prices[-1] / prices[0]) - Decimal("1")) * Decimal("100")
        assert exact_return < Decimal("5")
        result = period_analysis.analyze_period(prices, 2, 0.05)
    assert result["threshold_pass"] is False


def test_integer_price_inputs_preserve_existing_results(period_analysis):
    # Explicit compatibility control for the legacy integer-price interface.
    prices = [100, 100, 125]
    assert period_analysis.calculate_period_return(prices) == 25.0
    assert period_analysis.calculate_period_uptrend_ratio(prices) == 50.0
    assert period_analysis.analyze_period(prices, 3, 0.20) == {
        "period_days": 3,
        "status": "ANALYZED",
        "required_data": 3,
        "available_data": 3,
        "return_rate": 25.0,
        "uptrend_ratio": 50.0,
        "threshold": 20.0,
        "threshold_pass": True,
    }


def _query_synthetic_prices(period_analysis, monkeypatch, prices, thresholds):
    # Explicit synthetic calendar labels, not an inferred exchange schedule.
    rows = [((date(2026, 1, 1) + timedelta(days=index)).isoformat(), price)
            for index, price in enumerate(prices)]
    calls = []

    def fake_get_etf_prices(ticker, end_date=None):
        calls.append((ticker, end_date))
        return rows

    with monkeypatch.context() as patch:
        patch.setattr(period_analysis, "get_etf_prices", fake_get_etf_prices)
        result = period_analysis.get_period_analysis(
            "SYNTHETIC", rows[-1][0], thresholds=thresholds,
        )
    assert calls == [("SYNTHETIC", rows[-1][0])]
    assert [row[1] for row in rows] == prices
    assert result["ticker"] == "SYNTHETIC"
    assert result["analysis_date"] == rows[-1][0]
    return result


def test_query_boundary_preserves_decimal_prices_and_period_results(period_analysis, monkeypatch):
    prices = [Decimal("1")] * 59 + [Decimal("1.00000000000000000001")]
    thresholds = {days: Decimal("1E-21") for days in (20, 40, 60)}
    assert float(prices[0]) == float(prices[-1])
    with localcontext(Context(prec=50)):
        expected = period_analysis.analyze_periods(prices, thresholds)
        result = _query_synthetic_prices(period_analysis, monkeypatch, prices, thresholds)
    for days in (20, 40, 60):
        period = result["periods"][str(days)]
        assert type(period["return_rate"]) is Decimal
        assert period["return_rate"] == Decimal("1E-18")
        assert period["uptrend_ratio"] == (1 / (days - 1)) * 100.0
        assert period["threshold_pass"] is True
    assert result["periods"] == expected
    assert result["trend_state"] == period_analysis.calculate_trend_state(expected) == "DOWNTREND"


@pytest.mark.parametrize("numeric_type", [int, float], ids=["integer_rows", "float_rows"])
def test_query_boundary_preserves_legacy_numeric_results(period_analysis, monkeypatch, numeric_type):
    prices = [numeric_type(100)] * 59 + [numeric_type(125)]
    thresholds = {20: 0.05, 40: 0.10, 60: 0.15}
    expected = period_analysis.analyze_periods(prices, thresholds)
    result = _query_synthetic_prices(period_analysis, monkeypatch, prices, thresholds)
    assert result["periods"] == expected
    assert result["trend_state"] == period_analysis.calculate_trend_state(expected) == "UPTREND"
    for days in (20, 40, 60):
        period = result["periods"][str(days)]
        assert type(period["return_rate"]) is float
        assert period["return_rate"] == 25.0
        assert period["uptrend_ratio"] == (1 / (days - 1)) * 100.0
        assert period["threshold_pass"] is True


@pytest.fixture
def flask_json_app():
    # Import only Flask, never the operational application or its dependencies.
    from importlib.metadata import version
    from flask import Flask

    assert version("Flask") == "3.1.3", "This contract requires Flask 3.1.3"
    return Flask("synthetic_period_json_contract")


def test_jsonify_decimal_analysis_preserves_strings_and_source(
    period_analysis, monkeypatch, flask_json_app,
):
    from copy import deepcopy
    from flask import jsonify

    prices = [Decimal("1")] * 59 + [Decimal("1.00000000000000000001")]
    thresholds = {days: Decimal("1E-21") for days in (20, 40, 60)}
    with localcontext(Context(prec=50)):
        result = _query_synthetic_prices(period_analysis, monkeypatch, prices, thresholds)
    payload = {"analyses": [result], "metadata": {"optional": None, "flags": [True, False]}}
    original = deepcopy(payload)
    original_returns = {days: result["periods"][str(days)]["return_rate"]
                        for days in (20, 40, 60)}
    with flask_json_app.app_context():
        response = jsonify(payload)
        decoded = response.get_json()

    assert response.status_code == 200
    assert response.mimetype == "application/json"
    assert decoded["metadata"]["optional"] is None
    assert decoded["metadata"]["flags"][0] is True
    assert decoded["metadata"]["flags"][1] is False
    for days in (20, 40, 60):
        source = result["periods"][str(days)]
        encoded = decoded["analyses"][0]["periods"][str(days)]
        for field in ("return_rate", "threshold"):
            assert type(source[field]) is Decimal
            assert type(encoded[field]) is str
            assert encoded[field] == str(source[field])
            assert Decimal(encoded[field]) == source[field]
        assert Decimal(encoded["return_rate"]) == Decimal("1E-18")
        assert encoded["threshold_pass"] is True
        assert type(encoded["uptrend_ratio"]) is float
        assert encoded["uptrend_ratio"] == source["uptrend_ratio"]
        assert source["return_rate"] is original_returns[days]
    assert payload == original


@pytest.mark.parametrize("numeric_type", [int, float], ids=["integer_rows", "float_rows"])
def test_jsonify_legacy_analysis_preserves_json_numbers(
    period_analysis, monkeypatch, flask_json_app, numeric_type,
):
    from flask import jsonify

    prices = [numeric_type(100)] * 59 + [numeric_type(125)]
    thresholds = {20: 0.05, 40: 0.10, 60: 0.15}
    result = _query_synthetic_prices(period_analysis, monkeypatch, prices, thresholds)
    with flask_json_app.app_context():
        decoded = jsonify(result).get_json()

    assert decoded == result
    for days in (20, 40, 60):
        period = decoded["periods"][str(days)]
        assert type(period["return_rate"]) is float
        assert period["return_rate"] == 25.0
        assert type(period["threshold"]) is float
        assert period["threshold"] == thresholds[days] * 100.0
        assert type(period["period_days"]) is int
        assert period["period_days"] == days
        assert period["threshold_pass"] is True


def test_jsonify_distinguishes_close_decimal_strings(flask_json_app):
    from flask import jsonify

    values = [Decimal("1.00000000000000000001"), Decimal("1.00000000000000000002")]
    assert values[0] != values[1]
    assert float(values[0]) == float(values[1])
    with flask_json_app.app_context():
        decoded = jsonify({"nested": {"values": values}}).get_json()

    encoded = decoded["nested"]["values"]
    assert all(type(value) is str for value in encoded)
    assert encoded == ["1.00000000000000000001", "1.00000000000000000002"]
    assert encoded[0] != encoded[1]
    assert [Decimal(value) for value in encoded] == values
