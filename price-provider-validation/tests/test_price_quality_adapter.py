"""Synthetic, offline tests for the fail-closed provider quality input."""

from dataclasses import replace

import pytest

from price_provider_validation.provider_contract import (
    ProviderObservationRejected,
    prepare_raw_observation,
)
from price_provider_validation.ohlcv_mapping import OhlcvFieldMapping
from price_provider_validation.price_quality_adapter import (
    ProviderPriceQualityInput,
    existing_trading_session_contract,
    prepare_provider_price_quality_input,
)


@pytest.mark.parametrize("provider", ["KIS", "KIWOOM"])
def test_provider_quality_input_preserves_identity_and_denies_authority(provider):
    observation = prepare_raw_observation(
        provider,
        "005930",
        "2026-10-28",
        ("100.125", "110.500", "90.000", "105.375", "1000"),
    )
    mapping = OhlcvFieldMapping(0, 1, 2, 3, 4)

    result = prepare_provider_price_quality_input(observation, mapping)

    assert type(result) is ProviderPriceQualityInput
    assert result.provider == provider
    assert result.ticker == "005930"
    assert result.observation_date == "2026-10-28"
    assert result.ohlcv == (
        "100.125", "110.500", "90.000", "105.375", "1000"
    )
    assert result.adjustment == "UNKNOWN"
    assert result.analysis_authorized is False
    assert result.persistence_authorized is False


def test_quality_input_uses_explicit_field_mapping():
    observation = prepare_raw_observation(
        "KIS", "005930", "2026-10-28",
        ("105", "100", "1000", "90", "110"),
    )
    mapping = OhlcvFieldMapping(1, 4, 3, 0, 2)

    result = prepare_provider_price_quality_input(observation, mapping)

    assert result.ohlcv == ("100", "110", "90", "105", "1000")
    assert result.analysis_authorized is False


def test_quality_input_rejects_adjustment_escalation():
    observation = prepare_raw_observation(
        "KIS", "005930", "2026-10-28",
        ("100", "110", "90", "105", "1000"),
    )
    observation = replace(observation, adjustment="ADJUSTED")

    with pytest.raises(ProviderObservationRejected, match="UNKNOWN"):
        prepare_provider_price_quality_input(
            observation, OhlcvFieldMapping(0, 1, 2, 3, 4)
        )


def test_quality_input_rejects_wrong_observation_type():
    with pytest.raises(ProviderObservationRejected):
        prepare_provider_price_quality_input(
            object(), OhlcvFieldMapping(0, 1, 2, 3, 4)
        )


def test_quality_input_rejects_invalid_mapping():
    observation = prepare_raw_observation(
        "KIWOOM", "005930", "2026-10-28",
        ("100", "110", "90", "105", "1000"),
    )

    with pytest.raises(ProviderObservationRejected):
        prepare_provider_price_quality_input(
            observation, OhlcvFieldMapping(0, 0, 2, 3, 4)
        )


def test_existing_classifier_is_reference_only():
    path, function = existing_trading_session_contract()

    assert path == (
        "naver-decimal-validation/core/trading_session_eligibility.py"
    )
    assert function == "assess_trading_session"

from price_provider_validation.price_quality_adapter import assess_provider_price_quality


def _quality_input(ohlcv):
    return ProviderPriceQualityInput(
        provider="KIS",
        ticker="005930",
        observation_date="2026-10-28",
        ohlcv=ohlcv,
    )


@pytest.mark.parametrize("provider", ["KIS", "KIWOOM"])
def test_shared_quality_classifier_candidate(provider):
    quality = replace(
        _quality_input(("100", "110", "90", "105", "1000")),
        provider=provider,
    )
    decision = assess_provider_price_quality(quality)
    assert decision.status == "CANDIDATE"
    assert decision.reason == "STRUCTURALLY_VALID_UNVERIFIED"
    assert decision.trading_day_eligible is True
    assert decision.analysis_authorized is False
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
def test_shared_quality_classifier_blocks_invalid_ohlcv(ohlcv):
    decision = assess_provider_price_quality(_quality_input(ohlcv))
    assert decision.status == "BLOCKED"
    assert decision.trading_day_eligible is False
    assert decision.analysis_authorized is False
    assert decision.persistence_authorized is False


def test_shared_quality_classifier_non_trading_zero_ohlc():
    decision = assess_provider_price_quality(
        _quality_input(("0", "0", "0", "105", "0"))
    )
    assert decision.status == "NON_TRADING"
    assert decision.trading_day_eligible is False
    assert decision.analysis_authorized is False
    assert decision.persistence_authorized is False


@pytest.mark.parametrize(
    "changes",
    [
        {"adjustment": "ADJUSTED"},
        {"adjustment": "UNADJUSTED"},
        {"analysis_authorized": True},
        {"persistence_authorized": True},
        {"ohlcv": ("100", "110", "90", "105")},
    ],
)
def test_shared_quality_classifier_rejects_invalid_contract(changes):
    quality = replace(
        _quality_input(("100", "110", "90", "105", "1000")),
        **changes,
    )
    with pytest.raises(ProviderObservationRejected):
        assess_provider_price_quality(quality)


def test_shared_quality_classifier_rejects_wrong_input_type():
    with pytest.raises(ProviderObservationRejected):
        assess_provider_price_quality(object())


@pytest.mark.parametrize("invalid", ["NaN", "Infinity", None, True])
def test_shared_quality_classifier_rejects_invalid_numeric(invalid):
    quality = _quality_input(("100", "110", "90", invalid, "1000"))
    with pytest.raises(ValueError):
        assess_provider_price_quality(quality)
