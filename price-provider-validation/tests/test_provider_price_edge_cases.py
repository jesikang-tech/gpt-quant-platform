"""Offline synthetic edge cases for both price providers.

Structural eligibility is never price provenance or trading-day certification.
"""

import pytest

from price_provider_validation.provider_contract import (
    ProviderObservationRejected,
)
from price_provider_validation.price_quality_adapter import (
    ProviderPriceQualityInput,
    assess_provider_price_quality,
)
from price_provider_validation.trading_day_certification import (
    assess_trading_day_certification,
)


def _quality(provider, ohlcv):
    return ProviderPriceQualityInput(
        provider=provider,
        ticker="005930",
        observation_date="2026-10-28",
        ohlcv=ohlcv,
    )


@pytest.mark.parametrize("provider", ["KIS", "KIWOOM"])
@pytest.mark.parametrize(
    "ohlcv,expected_status",
    [
        (("100.125", "110.500", "90.000", "105.375", "1000"), "CANDIDATE"),
        (("100", "99", "90", "105", "1000"), "BLOCKED"),
        (("100", "110", "106", "105", "1000"), "BLOCKED"),
        (("100", "110", "90", "105", "0"), "BLOCKED"),
        (("100", "110", "90", "105", "-1"), "BLOCKED"),
        (("0", "0", "0", "105", "0"), "NON_TRADING"),
        (("-100", "110", "90", "105", "1000"), "BLOCKED"),
        (("100", "110", "-90", "105", "1000"), "BLOCKED"),
        (("100", "110", "90", "105", "0.000"), "BLOCKED"),
    ],
)
def test_provider_edge_status_and_authority_denial(
    provider, ohlcv, expected_status
):
    decision = assess_provider_price_quality(_quality(provider, ohlcv))

    assert decision.status == expected_status
    assert decision.analysis_authorized is False
    assert decision.persistence_authorized is False

    certification = assess_trading_day_certification(decision)

    assert certification.official_trading_day_verified is False
    assert certification.status == "DENIED"
    assert certification.analysis_authorized is False
    assert certification.persistence_authorized is False


@pytest.mark.parametrize("provider", ["KIS", "KIWOOM"])
@pytest.mark.parametrize("field_index", range(5))
@pytest.mark.parametrize(
    "invalid",
    [None, True, "NaN", "Infinity", "-Infinity", "not-a-number"],
)
def test_invalid_numeric_in_every_field_rejected(
    provider, field_index, invalid
):
    fields = ["100", "110", "90", "105", "1000"]
    fields[field_index] = invalid

    with pytest.raises(ProviderObservationRejected):
        assess_provider_price_quality(
            _quality(provider, tuple(fields))
        )


@pytest.mark.parametrize("provider", ["KIS", "KIWOOM"])
def test_extreme_but_structurally_valid_values_remain_unverified(provider):
    quality = _quality(
        provider,
        (
            "0.00000000000000000001",
            "99999999999999999999",
            "0.00000000000000000001",
            "100.00000000000000000001",
            "99999999999999999999",
        ),
    )

    decision = assess_provider_price_quality(quality)

    assert decision.status == "CANDIDATE"
    assert decision.reason == "STRUCTURALLY_VALID_UNVERIFIED"
    assert decision.analysis_authorized is False
    assert decision.persistence_authorized is False

    certification = assess_trading_day_certification(decision)

    assert certification.status == "DENIED"
    assert certification.official_trading_day_verified is False
