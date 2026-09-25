import pytest

import current_analysis


def test_normalize_analysis_date_defaults_to_latest_market_date(monkeypatch):
    monkeypatch.setattr(
        current_analysis,
        "_get_latest_market_date",
        lambda: "2026-09-22",
    )

    assert (
        current_analysis._normalize_analysis_date(None)
        == "2026-09-22"
    )


def test_normalize_analysis_date_rejects_future_date(monkeypatch):
    monkeypatch.setattr(
        current_analysis,
        "_get_latest_market_date",
        lambda: "2026-09-22",
    )

    with pytest.raises(ValueError, match="later than latest market data date"):
        current_analysis._normalize_analysis_date("2026-09-23")


def test_normalize_analysis_date_accepts_trading_day(monkeypatch):
    monkeypatch.setattr(
        current_analysis,
        "_get_latest_market_date",
        lambda: "2026-09-22",
    )

    monkeypatch.setattr(
        current_analysis,
        "_is_trading_day",
        lambda analysis_date: True,
    )

    assert (
        current_analysis._normalize_analysis_date("2026-09-04")
        == "2026-09-04"
    )


def test_normalize_analysis_date_rejects_non_trading_day(monkeypatch):
    monkeypatch.setattr(
        current_analysis,
        "_get_latest_market_date",
        lambda: "2026-09-22",
    )

    monkeypatch.setattr(
        current_analysis,
        "_is_trading_day",
        lambda analysis_date: False,
    )

    with pytest.raises(ValueError, match="not a trading day"):
        current_analysis._normalize_analysis_date("2026-09-05")


@pytest.mark.parametrize(
    "analysis_date",
    ["2026-02-30", "2026-13-01", "not-a-date"],
)
def test_normalize_analysis_date_rejects_invalid_date(
    monkeypatch,
    analysis_date,
):
    monkeypatch.setattr(
        current_analysis,
        "_get_latest_market_date",
        lambda: "2026-09-22",
    )

    with pytest.raises(ValueError, match="Invalid analysis date"):
        current_analysis._normalize_analysis_date(analysis_date)
