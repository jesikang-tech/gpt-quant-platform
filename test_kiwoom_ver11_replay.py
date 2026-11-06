"""Offline KIWOOM historical ranking replay contracts."""

from datetime import date, timedelta
from decimal import Decimal

import pytest

from kiwoom_ver11_replay import replay_kiwoom_ver11_prices


def _rows(start_value=100, count=65):
    start = date(2026, 8, 1)
    return [
        (
            (start + timedelta(days=i)).isoformat(),
            Decimal(start_value + i),
        )
        for i in range(count)
    ]


def test_replay_ranks_selected_tickers():
    rows = {
        "069500": _rows(100),
        "102110": _rows(200),
    }
    result = replay_kiwoom_ver11_prices(
        rows, analysis_date="2026-10-04", period="3m"
    )
    assert result["success"] is True
    assert result["source"] == "KIWOOM"
    assert result["input_origin"] == "CALLER_SUPPLIED_UNVERIFIED"
    assert result["persistence"] is False
    assert result["db_write"] is False
    assert result["total_selected"] >= 1
    assert all(item["selection_pass"] for item in result["results"])
    assert result["results"] == sorted(
        result["results"],
        key=lambda item: (-item["final_score"], item["ticker"]),
    )


def test_future_rows_do_not_change_historical_replay():
    rows = _rows(100)
    cutoff = rows[59][0]
    baseline = replay_kiwoom_ver11_prices(
        {"069500": rows[:60]}, analysis_date=cutoff
    )
    extended = replay_kiwoom_ver11_prices(
        {"069500": rows}, analysis_date=cutoff
    )
    assert baseline == extended


def test_insufficient_history_reported():
    result = replay_kiwoom_ver11_prices(
        {"069500": _rows(count=19)},
        analysis_date="2026-10-04",
        period="1m",
    )
    assert result["results"] == []
    assert result["unavailable_tickers"] == ["069500"]


@pytest.mark.parametrize("bad_limit", [0, -1, 101, True, "10"])
def test_invalid_limit_rejected(bad_limit):
    with pytest.raises(ValueError, match="Invalid replay limit"):
        replay_kiwoom_ver11_prices(
            {"069500": _rows()},
            analysis_date="2026-10-04",
            limit=bad_limit,
        )


def test_invalid_price_row_rejected():
    rows = _rows()
    rows[5] = (rows[5][0], Decimal("NaN"))
    with pytest.raises(ValueError, match="Invalid close price"):
        replay_kiwoom_ver11_prices(
            {"069500": rows},
            analysis_date="2026-10-04",
        )


def test_non_mapping_rejected():
    with pytest.raises(ValueError, match="Invalid ticker price mapping"):
        replay_kiwoom_ver11_prices(
            [],
            analysis_date="2026-10-04",
        )