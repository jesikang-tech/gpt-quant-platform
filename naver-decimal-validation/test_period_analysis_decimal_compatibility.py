"""Intentional red regressions for pure period-analysis Decimal compatibility.

No operational analysis, dashboard, provider, or database entry is invoked.
The real source is loaded only after replacing its configuration/repository
imports with test-local dependencies. These tests do not authorize NAVER use.
"""

from decimal import Context, Decimal, localcontext
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
