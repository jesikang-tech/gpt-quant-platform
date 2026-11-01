"""Offline tests for Kiwoom daily response batch validation."""
import pytest

from price_provider_validation.kiwoom_daily_batch import (
    MAX_DAILY_ROWS,
    prepare_kiwoom_daily_batch,
)
from price_provider_validation.provider_contract import (
    ProviderObservationRejected,
)


def _row(api_id, day="20261028"):
    date_field = "dt" if api_id == "ka10081" else "date"
    close_field = "cur_prc" if api_id == "ka10081" else "close_pric"
    return {
        date_field: day,
        "open_pric": "100",
        "high_pric": "110",
        "low_pric": "90",
        close_field: "105",
        "trde_qty": "1000",
    }


def _batch(api_id, rows):
    field = (
        "stk_dt_pole_chart_qry"
        if api_id == "ka10081"
        else "daly_stkpc"
    )
    return {field: rows}


@pytest.mark.parametrize("api_id", ["ka10081", "ka10086"])
def test_valid_batch_preserves_unverified_observations(api_id):
    response = _batch(
        api_id,
        [_row(api_id, "20261028"), _row(api_id, "20261027")],
    )
    result = prepare_kiwoom_daily_batch(
        api_id, "005930", response,
        requested_base_date="2026-10-28",
    )
    assert len(result) == 2
    assert [r.observation_date for r in result] == [
        "2026-10-28", "2026-10-27"
    ]
    assert all(r.provider == "KIWOOM" for r in result)
    assert all(r.adjustment == "UNKNOWN" for r in result)


@pytest.mark.parametrize("api_id", ["ka10081", "ka10086"])
@pytest.mark.parametrize("rows", [[], None, {}, "invalid"])
def test_invalid_array_rejected(api_id, rows):
    with pytest.raises(ProviderObservationRejected):
        prepare_kiwoom_daily_batch(
            api_id, "005930", _batch(api_id, rows),
            requested_base_date="2026-10-28",
        )


@pytest.mark.parametrize("api_id", ["ka10081", "ka10086"])
def test_duplicate_dates_rejected(api_id):
    row = _row(api_id)
    with pytest.raises(ProviderObservationRejected):
        prepare_kiwoom_daily_batch(
            api_id, "005930", _batch(api_id, [row, dict(row)]),
            requested_base_date="2026-10-28",
        )


@pytest.mark.parametrize("api_id", ["ka10081", "ka10086"])
def test_future_relative_to_request_rejected(api_id):
    with pytest.raises(ProviderObservationRejected):
        prepare_kiwoom_daily_batch(
            api_id, "005930",
            _batch(api_id, [_row(api_id, "20261029")]),
            requested_base_date="2026-10-28",
        )


def test_missing_array_rejected():
    with pytest.raises(ProviderObservationRejected):
        prepare_kiwoom_daily_batch(
            "ka10081", "005930", {},
            requested_base_date="2026-10-28",
        )


def test_excessive_batch_rejected():
    rows = [_row("ka10081", "20261028")] * (MAX_DAILY_ROWS + 1)
    with pytest.raises(ProviderObservationRejected):
        prepare_kiwoom_daily_batch(
            "ka10081", "005930",
            _batch("ka10081", rows),
            requested_base_date="2026-10-28",
        )


@pytest.mark.parametrize("invalid", ["20261028", "2026-02-30", None, True])
def test_invalid_base_date_rejected(invalid):
    with pytest.raises(ProviderObservationRejected):
        prepare_kiwoom_daily_batch(
            "ka10081", "005930",
            _batch("ka10081", [_row("ka10081")]),
            requested_base_date=invalid,
        )


def test_malformed_row_rejected():
    with pytest.raises(ProviderObservationRejected):
        prepare_kiwoom_daily_batch(
            "ka10081", "005930",
            _batch("ka10081", [{"dt": "20261028"}]),
            requested_base_date="2026-10-28",
        )
