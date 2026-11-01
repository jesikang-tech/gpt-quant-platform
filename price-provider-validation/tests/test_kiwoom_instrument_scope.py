"""Offline synthetic tests for Kiwoom instrument-scope assessment."""
import pytest

from price_provider_validation.kiwoom_instrument_scope import (
    InstrumentKind,
    assess_kiwoom_instrument_scope,
)
from price_provider_validation.provider_contract import (
    ProviderObservationRejected,
)


@pytest.mark.parametrize("api_id", ["ka10081", "ka10086"])
@pytest.mark.parametrize("kind", list(InstrumentKind))
def test_all_instrument_kinds_remain_unverified(api_id, kind):
    result = assess_kiwoom_instrument_scope(
        api_id, "005930", kind
    )
    assert result.provider == "KIWOOM"
    assert result.instrument_kind is kind
    assert result.support_status == "UNVERIFIED"
    assert result.api_execution_authorized is False
    assert result.analysis_authorized is False
    assert result.persistence_authorized is False
    assert result.database_rebuild_authorized is False


@pytest.mark.parametrize(
    "bad_api", ["ka99999", "", None, True]
)
def test_unsupported_api_rejected(bad_api):
    with pytest.raises(ProviderObservationRejected):
        assess_kiwoom_instrument_scope(
            bad_api, "005930", InstrumentKind.ETF
        )


@pytest.mark.parametrize(
    "bad_ticker", ["", " 005930", "005930 ", None, True]
)
def test_invalid_ticker_rejected(bad_ticker):
    with pytest.raises(ProviderObservationRejected):
        assess_kiwoom_instrument_scope(
            "ka10081", bad_ticker, InstrumentKind.ETF
        )


@pytest.mark.parametrize(
    "bad_kind", ["ETF", "STOCK", "ETN", None, True]
)
def test_unverified_kind_declarations_rejected(bad_kind):
    with pytest.raises(ProviderObservationRejected):
        assess_kiwoom_instrument_scope(
            "ka10081", "005930", bad_kind
        )
