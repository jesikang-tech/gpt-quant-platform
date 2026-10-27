"""Offline synthetic tests for documented KIS daily-response fields."""

import pytest

from price_provider_validation.kis_daily_response import (
    kis_daily_array_field,
    prepare_kis_daily_observation,
)
from price_provider_validation.kis_adapter import map_kis_ohlcv
from price_provider_validation.ohlcv_mapping import OhlcvFieldMapping
from price_provider_validation.decimal_bridge import (
    prepare_provider_decimal_record,
)
from price_provider_validation.provider_contract import (
    ProviderObservationRejected,
)


def _row(date="20261028", **overrides):
    row = {
        "stck_bsop_date": date,
        "stck_oprc": "100",
        "stck_hgpr": "110",
        "stck_lwpr": "90",
        "stck_clpr": "105",
        "acml_vol": "1000",
    }
    row.update(overrides)
    return row


def test_documented_kis_fields_preserved_and_unverified():
    observation = prepare_kis_daily_observation(
        "005930",
        _row(),
    )

    assert observation.provider == "KIS"
    assert observation.ticker == "005930"
    assert observation.observation_date == "2026-10-28"
    assert observation.adjustment == "UNKNOWN"
    assert observation.raw_fields == (
        "100", "110", "90", "105", "1000"
    )
    assert kis_daily_array_field() == "output2"

    mapping = OhlcvFieldMapping(0, 1, 2, 3, 4)

    assert map_kis_ohlcv(observation, mapping) == {
        "Open": "100",
        "High": "110",
        "Low": "90",
        "Close": "105",
        "Volume": "1000",
    }

    with pytest.raises(ProviderObservationRejected):
        prepare_provider_decimal_record(observation)


@pytest.mark.parametrize(
    "bad_date",
    [
        "20260230",
        "20261301",
        "2026-10-28",
        "",
        20261028,
        None,
        True,
    ],
)
def test_invalid_dates_rejected(bad_date):
    with pytest.raises(ProviderObservationRejected):
        prepare_kis_daily_observation(
            "005930",
            _row(date=bad_date),
        )


@pytest.mark.parametrize(
    "missing_field",
    [
        "stck_bsop_date",
        "stck_oprc",
        "stck_hgpr",
        "stck_lwpr",
        "stck_clpr",
        "acml_vol",
    ],
)
def test_missing_fields_rejected(missing_field):
    row = _row()
    del row[missing_field]

    with pytest.raises(ProviderObservationRejected):
        prepare_kis_daily_observation("005930", row)


@pytest.mark.parametrize(
    "bad_value",
    [None, 100, "", True, [], {}],
)
def test_invalid_price_types_rejected(bad_value):
    with pytest.raises(ProviderObservationRejected):
        prepare_kis_daily_observation(
            "005930",
            _row(stck_clpr=bad_value),
        )


@pytest.mark.parametrize(
    "bad_row",
    [None, [], (), "invalid", 123],
)
def test_invalid_row_types_rejected(bad_row):
    with pytest.raises(ProviderObservationRejected):
        prepare_kis_daily_observation(
            "005930",
            bad_row,
        )


def test_original_price_strings_preserved_without_certification():
    observation = prepare_kis_daily_observation(
        "005930",
        _row(
            stck_oprc="-100",
            stck_hgpr="+110",
            stck_lwpr="090",
            stck_clpr="+105",
        ),
    )

    assert observation.raw_fields == (
        "-100", "+110", "090", "+105", "1000"
    )
    assert observation.adjustment == "UNKNOWN"

    with pytest.raises(ProviderObservationRejected):
        prepare_provider_decimal_record(observation)
