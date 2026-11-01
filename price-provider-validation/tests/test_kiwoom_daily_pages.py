"""Synthetic tests for offline Kiwoom daily multipage validation."""
import pytest

from price_provider_validation.kiwoom_daily_pages import (
    MAX_DAILY_PAGES,
    prepare_kiwoom_daily_pages,
)
from price_provider_validation.provider_contract import (
    ProviderObservationRejected,
)


def _row(api_id, day):
    row = {
        "open_pric": "+100",
        "high_pric": "+110",
        "low_pric": "+90",
        "trde_qty": "1000",
    }
    if api_id == "ka10081":
        row["dt"] = day
        row["cur_prc"] = "+105"
    else:
        row["date"] = day
        row["close_pric"] = "+105"
    return row


def _page(api_id, *days):
    field = (
        "stk_dt_pole_chart_qry"
        if api_id == "ka10081"
        else "daly_stkpc"
    )
    return {field: [_row(api_id, day) for day in days]}


@pytest.mark.parametrize("api_id", ["ka10081", "ka10086"])
def test_ordered_pages_preserve_raw_observations(api_id):
    result = prepare_kiwoom_daily_pages(
        api_id,
        "005930",
        [
            _page(api_id, "20261030", "20261029"),
            _page(api_id, "20261028"),
        ],
        requested_base_date="2026-10-30",
    )
    assert [row.observation_date for row in result] == [
        "2026-10-30", "2026-10-29", "2026-10-28"
    ]
    assert all(row.adjustment == "UNKNOWN" for row in result)


@pytest.mark.parametrize("api_id", ["ka10081", "ka10086"])
@pytest.mark.parametrize(
    "pages",
    [
        [("20261030",), ("20261030",)],
        [("20261029",), ("20261030",)],
        [("20261029", "20261030")],
        [("20261030",), ("20261029", "20261029")],
    ],
)
def test_duplicate_or_out_of_order_dates_rejected(api_id, pages):
    responses = [_page(api_id, *days) for days in pages]
    with pytest.raises(ProviderObservationRejected):
        prepare_kiwoom_daily_pages(
            api_id, "005930", responses,
            requested_base_date="2026-10-30",
        )


@pytest.mark.parametrize(
    "responses",
    [[], None, {}, "invalid", [None]],
)
def test_invalid_page_collections_rejected(responses):
    with pytest.raises(ProviderObservationRejected):
        prepare_kiwoom_daily_pages(
            "ka10081", "005930", responses,
            requested_base_date="2026-10-30",
        )


def test_page_limit_rejected():
    pages = [_page("ka10081", "20261030")] * (MAX_DAILY_PAGES + 1)
    with pytest.raises(ProviderObservationRejected):
        prepare_kiwoom_daily_pages(
            "ka10081", "005930", pages,
            requested_base_date="2026-10-30",
        )


def test_future_date_rejected_through_existing_batch_contract():
    with pytest.raises(ProviderObservationRejected):
        prepare_kiwoom_daily_pages(
            "ka10081", "005930",
            [_page("ka10081", "20261031")],
            requested_base_date="2026-10-30",
        )
