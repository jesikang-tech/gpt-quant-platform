"""Synthetic tests for the NAVER rebuild adapter."""

from dataclasses import FrozenInstanceError
from decimal import Decimal

import pytest

from price_rebuild_adapter import (
    prepare_synthetic_rebuild_rows,
    reject_unverified_rebuild,
)
from price_rebuild_preflight import RebuildPreflight


VALUES = {
    "Open": "100.125",
    "High": "110.500",
    "Low": "90.000",
    "Close": "105.375",
    "Volume": "1000",
}


def _prepare(**overrides):
    kwargs = {
        "adjustment": "UNADJUSTED",
        "synthetic_fixture": True,
    }
    kwargs.update(overrides)
    return prepare_synthetic_rebuild_rows(
        "005930",
        "2026-01-02",
        VALUES,
        **kwargs,
    )


def test_price_ohlcv_identity_and_decimal_precision():
    result = _prepare()

    assert result.ticker == "005930"
    assert result.price_row[0:2] == result.ohlcv_row[0:2]
    assert result.price_row[2] == result.ohlcv_row[5]
    assert result.price_row[2] == Decimal("105.375")
    assert result.ohlcv_row[2] == Decimal("110.500")
    assert result.verification_status == "SYNTHETIC_ONLY"
    assert result.persistence_authorized is False


@pytest.mark.parametrize("adjustment", ["ADJUSTED", "UNADJUSTED"])
def test_explicit_synthetic_adjustment(adjustment):
    result = _prepare(adjustment=adjustment)
    assert result.persistence_authorized is False


@pytest.mark.parametrize("declaration", [False, None, "true", 1])
def test_missing_or_invalid_synthetic_declaration_rejected(declaration):
    with pytest.raises(ValueError, match="synthetic fixture"):
        _prepare(synthetic_fixture=declaration)


@pytest.mark.parametrize("adjustment", ["UNKNOWN", "", None])
def test_unknown_adjustment_rejected(adjustment):
    with pytest.raises(ValueError, match="synthetic adjustment"):
        _prepare(adjustment=adjustment)


def test_unverified_preflight_always_denied():
    preflight = RebuildPreflight(
        ticker="005930",
        total_rows=6,
        normal_rows=4,
        zero_ohlc_rows=1,
        high_below_close_rows=1,
        price_candidates=4,
        ohlcv_candidates=4,
    )

    with pytest.raises(ValueError, match="UNVERIFIED_NAVER_REBUILD_DENIED"):
        reject_unverified_rebuild(preflight)


def test_invalid_preflight_type_rejected():
    with pytest.raises(ValueError, match="RebuildPreflight required"):
        reject_unverified_rebuild(object())


def test_preflight_authority_escalation_rejected():
    preflight = RebuildPreflight(
        ticker="005930",
        total_rows=1,
        normal_rows=1,
        zero_ohlc_rows=0,
        high_below_close_rows=0,
        price_candidates=1,
        ohlcv_candidates=1,
        persistence_authorized=True,
    )

    with pytest.raises(ValueError, match="Invalid preflight authority"):
        reject_unverified_rebuild(preflight)


def test_result_is_immutable():
    result = _prepare()

    with pytest.raises(FrozenInstanceError):
        result.persistence_authorized = True