"""Synthetic tests for KIWOOM Ver1.1 close-price input."""

from decimal import Decimal

import pytest

from price_provider_validation.kiwoom_ver11_price_input import (
    prepare_kiwoom_ver11_close_prices,
)
from price_provider_validation.provider_contract import ProviderObservationRejected


def _row(day, close):
    return {
        "date": day,
        "open_pric": "100",
        "high_pric": "120",
        "low_pric": "90",
        "close_pric": close,
        "trde_qty": "1000",
    }


def _convert(rows, *, api_id="ka10086"):
    return prepare_kiwoom_ver11_close_prices(
        api_id,
        "005930",
        {"daly_stkpc": rows},
        requested_base_date="2026-11-06",
    )


def test_ascending_dates_and_exact_decimal_close():
    result = _convert([
        _row("20261106", "103.25"),
        _row("20261104", "101.10"),
    ])
    assert result == (
        ("2026-11-04", Decimal("101.10")),
        ("2026-11-06", Decimal("103.25")),
    )


@pytest.mark.parametrize("close", [
    "0", "-1", "NaN", "Infinity", "not-a-price",
])
def test_invalid_close_rejected(close):
    with pytest.raises(ProviderObservationRejected):
        _convert([_row("20261106", close)])


def test_duplicate_dates_rejected():
    with pytest.raises(ProviderObservationRejected):
        _convert([
            _row("20261106", "101"),
            _row("20261106", "102"),
        ])


def test_future_date_rejected():
    with pytest.raises(ProviderObservationRejected):
        _convert([_row("20261107", "101")])


def test_unsupported_api_rejected():
    with pytest.raises(ProviderObservationRejected):
        _convert([_row("20261106", "101")], api_id="unknown")
