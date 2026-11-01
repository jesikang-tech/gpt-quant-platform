"""Synthetic offline tests for provider quality integration."""

from dataclasses import replace

import pytest

from price_provider_validation.provider_contract import (
    ProviderObservationRejected,
)
from price_provider_validation.price_quality_adapter import (
    ProviderPriceQualityInput,
)
from price_provider_validation.provider_quality_integration import (
    ProviderQualityIntegrationDecision,
    assess_provider_quality_integration,
)


def _quality(provider="KIS", ohlcv=None):
    return ProviderPriceQualityInput(
        provider=provider,
        ticker="005930",
        observation_date="2026-10-28",
        ohlcv=(
            ("100", "110", "90", "105", "1000")
            if ohlcv is None else ohlcv
        ),
    )


@pytest.mark.parametrize("provider", ["KIS", "KIWOOM"])
def test_valid_provider_quality_remains_unauthorized(provider):
    decision = assess_provider_quality_integration(_quality(provider))

    assert type(decision) is ProviderQualityIntegrationDecision
    assert decision.provider == provider
    assert decision.ticker == "005930"
    assert decision.observation_date == "2026-10-28"
    assert decision.structural_status == "CANDIDATE"
    assert decision.structural_reason == "STRUCTURALLY_VALID_UNVERIFIED"
    assert decision.structural_trading_day_eligible is True
    assert decision.official_trading_day_verified is False
    assert decision.status == "DENIED"
    assert decision.reason == "OFFICIAL_TRADING_CALENDAR_EVIDENCE_MISSING"
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
def test_invalid_ohlcv_remains_blocked(ohlcv):
    decision = assess_provider_quality_integration(
        _quality(ohlcv=ohlcv)
    )

    assert decision.structural_status == "BLOCKED"
    assert decision.structural_trading_day_eligible is False
    assert decision.official_trading_day_verified is False
    assert decision.analysis_authorized is False
    assert decision.persistence_authorized is False


def test_zero_ohlc_is_not_certified_as_official_non_trading_day():
    decision = assess_provider_quality_integration(
        _quality(ohlcv=("0", "0", "0", "105", "0"))
    )

    assert decision.structural_status == "NON_TRADING"
    assert decision.structural_trading_day_eligible is False
    assert decision.official_trading_day_verified is False
    assert decision.status == "DENIED"


@pytest.mark.parametrize(
    "changes",
    [
        {"adjustment": "ADJUSTED"},
        {"adjustment": "UNADJUSTED"},
        {"analysis_authorized": True},
        {"persistence_authorized": True},
    ],
)
def test_authority_or_adjustment_escalation_rejected(changes):
    quality = replace(_quality(), **changes)

    with pytest.raises(ProviderObservationRejected):
        assess_provider_quality_integration(quality)


@pytest.mark.parametrize(
    "changes",
    [
        {"provider": "NAVER"},
        {"provider": "kis"},
        {"ticker": ""},
        {"observation_date": "20261028"},
        {"ohlcv": ("100", "110", "90", "105")},
    ],
)
def test_invalid_quality_input_rejected(changes):
    quality = replace(_quality(), **changes)

    with pytest.raises(ProviderObservationRejected):
        assess_provider_quality_integration(quality)


def test_wrong_input_type_rejected():
    with pytest.raises(ProviderObservationRejected):
        assess_provider_quality_integration(object())


def test_direct_decision_construction_remains_denied():
    decision = ProviderQualityIntegrationDecision(
        provider="KIS",
        ticker="005930",
        observation_date="2026-10-28",
        structural_status="CANDIDATE",
        structural_reason="STRUCTURALLY_VALID_UNVERIFIED",
        structural_trading_day_eligible=True,
    )

    assert decision.official_trading_day_verified is False
    assert decision.status == "DENIED"
    assert decision.analysis_authorized is False
    assert decision.dashboard_authorized is False
    assert decision.snapshot_authorized is False
    assert decision.persistence_authorized is False
