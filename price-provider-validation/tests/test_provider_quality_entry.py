"""Offline synthetic tests for the provider quality entry boundary."""

from dataclasses import replace

import pytest

from price_provider_validation.provider_contract import (
    ProviderObservationRejected,
    prepare_raw_observation,
)
from price_provider_validation.provider_quality_entry import (
    assess_provider_observation_quality,
)


def _observation(provider="KIS", ohlcv=None):
    return prepare_raw_observation(
        provider,
        "005930",
        "2026-10-28",
        ("100", "110", "90", "105", "1000")
        if ohlcv is None else ohlcv,
    )


@pytest.mark.parametrize("provider", ["KIS", "KIWOOM"])
def test_valid_observation_remains_denied(provider):
    decision = assess_provider_observation_quality(
        _observation(provider)
    )

    assert decision.provider == provider
    assert decision.ticker == "005930"
    assert decision.observation_date == "2026-10-28"
    assert decision.structural_status == "CANDIDATE"
    assert decision.structural_trading_day_eligible is True
    assert decision.official_trading_day_verified is False
    assert decision.status == "DENIED"
    assert decision.analysis_authorized is False
    assert decision.dashboard_authorized is False
    assert decision.snapshot_authorized is False
    assert decision.persistence_authorized is False


@pytest.mark.parametrize(
    "ohlcv",
    [
        ("100", "104", "90", "105", "1000"),
        ("100", "110", "106", "105", "1000"),
        ("100", "110", "90", "105", "0"),
        ("100", "110", "90", "105", "-1"),
    ],
)
def test_invalid_price_structure_remains_blocked(ohlcv):
    decision = assess_provider_observation_quality(
        _observation(ohlcv=ohlcv)
    )

    assert decision.structural_status == "BLOCKED"
    assert decision.structural_trading_day_eligible is False
    assert decision.official_trading_day_verified is False
    assert decision.status == "DENIED"
    assert decision.analysis_authorized is False
    assert decision.persistence_authorized is False


def test_zero_ohlc_does_not_certify_market_calendar():
    decision = assess_provider_observation_quality(
        _observation(ohlcv=("0", "0", "0", "105", "0"))
    )

    assert decision.structural_status == "NON_TRADING"
    assert decision.official_trading_day_verified is False
    assert decision.status == "DENIED"


@pytest.mark.parametrize(
    "adjustment",
    ["ADJUSTED", "UNADJUSTED"],
)
def test_unverified_adjustment_escalation_rejected(adjustment):
    observation = replace(
        _observation(),
        adjustment=adjustment,
    )

    with pytest.raises(ProviderObservationRejected):
        assess_provider_observation_quality(observation)


@pytest.mark.parametrize(
    "invalid",
    [None, object(), {}, (), "KIS"],
)
def test_invalid_observation_type_rejected(invalid):
    with pytest.raises(ProviderObservationRejected):
        assess_provider_observation_quality(invalid)


def test_forged_provider_identity_rejected():
    observation = replace(
        _observation(),
        provider="NAVER",
    )

    with pytest.raises(ProviderObservationRejected):
        assess_provider_observation_quality(observation)


def test_invalid_raw_field_count_rejected():
    observation = replace(
        _observation(),
        raw_fields=("100", "110", "90", "105"),
    )

    with pytest.raises(ProviderObservationRejected):
        assess_provider_observation_quality(observation)
