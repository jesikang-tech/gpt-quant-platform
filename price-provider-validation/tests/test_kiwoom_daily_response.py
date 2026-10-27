"""Offline synthetic tests for documented Kiwoom daily-response fields."""

import pytest

from price_provider_validation.provider_contract import (
    ProviderObservationRejected,
)
from price_provider_validation.kiwoom_daily_response import (
    prepare_kiwoom_daily_observation,
    kiwoom_daily_array_field,
)
from price_provider_validation.kiwoom_adapter import map_kiwoom_ohlcv
from price_provider_validation.ohlcv_mapping import OhlcvFieldMapping
from price_provider_validation.decimal_bridge import (
    prepare_provider_decimal_record,
)


@pytest.mark.parametrize(
    "api_id,date_field,close_field,array_field",
    [
        ("ka10081", "dt", "cur_prc", "stk_dt_pole_chart_qry"),
        ("ka10086", "date", "close_pric", "daly_stkpc"),
    ],
)
def test_documented_fields_preserved(
    api_id, date_field, close_field, array_field
):
    row = {
        date_field: "20261028",
        "open_pric": "100",
        "high_pric": "110",
        "low_pric": "90",
        close_field: "105",
        "trde_qty": "1000",
    }

    observation = prepare_kiwoom_daily_observation(
        api_id, "005930", row
    )

    assert observation.provider == "KIWOOM"
    assert observation.observation_date == "2026-10-28"
    assert observation.adjustment == "UNKNOWN"
    assert observation.raw_fields == (
        "100", "110", "90", "105", "1000"
    )
    assert kiwoom_daily_array_field(api_id) == array_field

    mapping = OhlcvFieldMapping(0, 1, 2, 3, 4)

    assert map_kiwoom_ohlcv(observation, mapping) == {
        "Open": "100",
        "High": "110",
        "Low": "90",
        "Close": "105",
        "Volume": "1000",
    }

    with pytest.raises(ProviderObservationRejected):
        prepare_provider_decimal_record(observation)


@pytest.mark.parametrize(
    "api_id,date_field,close_field",
    [
        ("ka10081", "dt", "cur_prc"),
        ("ka10086", "date", "close_pric"),
    ],
)
@pytest.mark.parametrize(
    "bad_date",
    ["20260230", "2026-10-28", "20261301", "", 20261028],
)
def test_invalid_dates_rejected(
    api_id, date_field, close_field, bad_date
):
    row = {
        date_field: bad_date,
        "open_pric": "100",
        "high_pric": "110",
        "low_pric": "90",
        close_field: "105",
        "trde_qty": "1000",
    }

    with pytest.raises(ProviderObservationRejected):
        prepare_kiwoom_daily_observation(api_id, "005930", row)


@pytest.mark.parametrize(
    "api_id,date_field,close_field",
    [
        ("ka10081", "dt", "cur_prc"),
        ("ka10086", "date", "close_pric"),
    ],
)
def test_missing_price_field_rejected(
    api_id, date_field, close_field
):
    row = {
        date_field: "20261028",
        "open_pric": "100",
        "high_pric": "110",
        "low_pric": "90",
        "trde_qty": "1000",
    }

    with pytest.raises(ProviderObservationRejected):
        prepare_kiwoom_daily_observation(api_id, "005930", row)


@pytest.mark.parametrize(
    "bad_value",
    [None, 100, "", True, [], {}],
)
def test_invalid_price_types_rejected(bad_value):
    row = {
        "date": "20261028",
        "open_pric": bad_value,
        "high_pric": "110",
        "low_pric": "90",
        "close_pric": "105",
        "trde_qty": "1000",
    }

    with pytest.raises(ProviderObservationRejected):
        prepare_kiwoom_daily_observation("ka10086", "005930", row)


def test_unsupported_api_rejected():
    with pytest.raises(ProviderObservationRejected):
        prepare_kiwoom_daily_observation(
            "ka99999", "005930", {}
        )

    with pytest.raises(ProviderObservationRejected):
        kiwoom_daily_array_field("ka99999")


def test_raw_sign_preserved_without_certification():
    row = {
        "date": "20261028",
        "open_pric": "+100",
        "high_pric": "+110",
        "low_pric": "-90",
        "close_pric": "+105",
        "trde_qty": "1000",
    }

    observation = prepare_kiwoom_daily_observation(
        "ka10086", "005930", row
    )

    assert observation.raw_fields == (
        "+100", "+110", "-90", "+105", "1000"
    )
    assert observation.adjustment == "UNKNOWN"

    with pytest.raises(ProviderObservationRejected):
        prepare_provider_decimal_record(observation)
