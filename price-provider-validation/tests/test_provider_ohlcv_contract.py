"""Synthetic, offline tests for isolated provider observation contracts."""

import pytest

from price_provider_validation.provider_contract import (
    ProviderObservationRejected,
    prepare_raw_observation,
)
from price_provider_validation.ohlcv_mapping import (
    OhlcvFieldMapping,
    map_raw_ohlcv,
)
from price_provider_validation.kis_adapter import map_kis_ohlcv
from price_provider_validation.kiwoom_adapter import map_kiwoom_ohlcv
from price_provider_validation.decimal_bridge import (
    prepare_provider_decimal_record,
)


def _observation(provider="KIS"):
    return prepare_raw_observation(
        provider,
        "005930",
        "2026-10-28",
        ("100", "110", "90", "105", "1000"),
    )


def _mapping():
    return OhlcvFieldMapping(0, 1, 2, 3, 4)


@pytest.mark.parametrize(
    "ticker,date_value,fields",
    [
        (" 005930", "2026-10-28", ("1",) * 5),
        ("005930", "2026-02-30", ("1",) * 5),
        ("005930", "2026-10-28", ("1",) * 4),
    ],
)
def test_invalid_raw_observation_rejected(ticker, date_value, fields):
    with pytest.raises(ProviderObservationRejected):
        prepare_raw_observation("KIS", ticker, date_value, fields)


def test_explicit_mapping_preserves_raw_values():
    result = map_raw_ohlcv(_observation(), _mapping())
    assert result == {
        "Open": "100",
        "High": "110",
        "Low": "90",
        "Close": "105",
        "Volume": "1000",
    }


def test_duplicate_mapping_index_rejected():
    with pytest.raises(ProviderObservationRejected):
        map_raw_ohlcv(
            _observation(),
            OhlcvFieldMapping(0, 0, 2, 3, 4),
        )


def test_cross_provider_mapping_rejected():
    with pytest.raises(ProviderObservationRejected):
        map_kiwoom_ohlcv(_observation("KIS"), _mapping())

    with pytest.raises(ProviderObservationRejected):
        map_kis_ohlcv(_observation("KIWOOM"), _mapping())


def test_invalid_adapter_observation_type_rejected():
    with pytest.raises(ProviderObservationRejected):
        map_kis_ohlcv(object(), _mapping())

    with pytest.raises(ProviderObservationRejected):
        map_kiwoom_ohlcv(object(), _mapping())


def test_unverified_decimal_normalization_rejected():
    with pytest.raises(ProviderObservationRejected):
        prepare_provider_decimal_record(_observation())
