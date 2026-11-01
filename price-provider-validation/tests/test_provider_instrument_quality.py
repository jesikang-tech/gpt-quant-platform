"""Synthetic K18 instrument-quality integration tests."""
from dataclasses import FrozenInstanceError, replace

import pytest

from price_provider_validation.kiwoom_instrument_scope import (
    InstrumentKind,
)
from price_provider_validation.provider_contract import (
    ProviderObservationRejected,
    prepare_raw_observation,
)
from price_provider_validation.provider_instrument_quality import (
    assess_provider_instrument_quality,
)


def _observation(provider, ticker="005930"):
    return prepare_raw_observation(
        provider,
        ticker,
        "2026-10-28",
        ("100", "110", "90", "105", "1000"),
    )


@pytest.mark.parametrize("kind", list(InstrumentKind))
@pytest.mark.parametrize(
    ("provider", "api_id"),
    [
        ("KIS", None),
        ("KIWOOM", "ka10081"),
        ("KIWOOM", "ka10086"),
    ],
)
def test_all_declared_instruments_remain_unverified(
    provider, api_id, kind
):
    result = assess_provider_instrument_quality(
        _observation(provider),
        kind,
        kiwoom_api_id=api_id,
    )
    assert result.provider == provider
    assert result.instrument_kind is kind
    assert result.instrument_support_status == "UNVERIFIED"
    assert result.status == "DENIED"
    assert result.reason == (
        "INSTRUMENT_AND_PRICE_NOT_INDEPENDENTLY_VERIFIED"
    )
    for name in (
        "instrument_classification_verified",
        "official_trading_day_verified",
        "independently_verified",
        "api_execution_authorized",
        "analysis_authorized",
        "dashboard_authorized",
        "snapshot_authorized",
        "persistence_authorized",
        "database_rebuild_authorized",
        "broker_execution_authorized",
    ):
        assert getattr(result, name) is False


@pytest.mark.parametrize("invalid", ("ETF", "STOCK", None, True))
def test_untrusted_instrument_kind_rejected(invalid):
    with pytest.raises(ProviderObservationRejected):
        assess_provider_instrument_quality(
            _observation("KIS"), invalid
        )


@pytest.mark.parametrize("api_id", (None, "ka99999", "", True))
def test_invalid_kiwoom_api_rejected(api_id):
    with pytest.raises(ProviderObservationRejected):
        assess_provider_instrument_quality(
            _observation("KIWOOM"),
            InstrumentKind.ETF,
            kiwoom_api_id=api_id,
        )


def test_kiwoom_api_on_kis_observation_rejected():
    with pytest.raises(ProviderObservationRejected):
        assess_provider_instrument_quality(
            _observation("KIS"),
            InstrumentKind.ETF,
            kiwoom_api_id="ka10081",
        )


def test_unverified_adjustment_claim_rejected():
    observation = replace(
        _observation("KIS"),
        adjustment="ADJUSTED",
    )
    with pytest.raises(ProviderObservationRejected):
        assess_provider_instrument_quality(
            observation, InstrumentKind.STOCK
        )


def test_invalid_price_observation_rejected():
    observation = replace(
        _observation("KIS"),
        raw_fields=("bad", "110", "90", "105", "1000"),
    )
    with pytest.raises(ProviderObservationRejected):
        assess_provider_instrument_quality(
            observation, InstrumentKind.ETF
        )


def test_result_is_immutable():
    result = assess_provider_instrument_quality(
        _observation("KIS"), InstrumentKind.ETF
    )
    with pytest.raises(FrozenInstanceError):
        result.analysis_authorized = True
