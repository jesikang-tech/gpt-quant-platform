"""Synthetic K17 calendar-continuity tests; no external authority."""
from dataclasses import FrozenInstanceError, replace

import pytest

from price_provider_validation.provider_calendar_continuity import (
    CalendarContinuityRejected,
    assess_calendar_continuity,
)
from price_provider_validation.provider_contract import (
    prepare_raw_observation,
)


def _observation(provider, day, ticker="005930"):
    return prepare_raw_observation(
        provider, ticker, day, ("100", "110", "90", "105", "1000")
    )


@pytest.mark.parametrize("provider", ("KIS", "KIWOOM"))
def test_matching_calendar_still_denied(provider):
    result = assess_calendar_continuity(
        provider,
        "005930",
        (
            _observation(provider, "2026-10-28"),
            _observation(provider, "2026-10-27"),
        ),
        ("2026-10-28", "2026-10-27"),
    )
    assert result.missing_dates == ()
    assert result.observed_count == 2
    assert result.calendar_count == 2
    assert result.status == "DENIED"
    assert result.reason == "OFFICIAL_CALENDAR_NOT_INDEPENDENTLY_VERIFIED"
    for name in (
        "official_calendar_verified",
        "historical_completeness_verified",
        "independently_verified",
        "analysis_authorized",
        "dashboard_authorized",
        "persistence_authorized",
        "database_rebuild_authorized",
        "broker_execution_authorized",
    ):
        assert getattr(result, name) is False


def test_missing_middle_date_reported_without_certification():
    result = assess_calendar_continuity(
        "KIS",
        "005930",
        (
            _observation("KIS", "2026-10-28"),
            _observation("KIS", "2026-10-26"),
        ),
        ("2026-10-28", "2026-10-27", "2026-10-26"),
    )
    assert result.missing_dates == ("2026-10-27",)
    assert result.status == "DENIED"
    assert result.historical_completeness_verified is False


@pytest.mark.parametrize("dates", (
    ("2026-10-27", "2026-10-28"),
    ("2026-10-28", "2026-10-28"),
    ("2026-02-30",),
    ("20261028",),
    (None,),
    (),
))
def test_invalid_calendar_rejected(dates):
    with pytest.raises(CalendarContinuityRejected):
        assess_calendar_continuity(
            "KIS", "005930",
            (_observation("KIS", "2026-10-28"),),
            dates,
        )


@pytest.mark.parametrize("days", (
    ("2026-10-27", "2026-10-28"),
    ("2026-10-28", "2026-10-28"),
))
def test_duplicate_or_out_of_order_observations_rejected(days):
    with pytest.raises(CalendarContinuityRejected):
        assess_calendar_continuity(
            "KIWOOM",
            "005930",
            tuple(_observation("KIWOOM", day) for day in days),
            ("2026-10-28", "2026-10-27"),
        )


def test_observation_outside_calendar_rejected():
    with pytest.raises(CalendarContinuityRejected):
        assess_calendar_continuity(
            "KIS", "005930",
            (_observation("KIS", "2026-10-28"),),
            ("2026-10-27",),
        )


def test_provider_or_ticker_mismatch_rejected():
    with pytest.raises(CalendarContinuityRejected):
        assess_calendar_continuity(
            "KIS", "005930",
            (_observation("KIWOOM", "2026-10-28"),),
            ("2026-10-28",),
        )


def test_unverified_adjustment_escalation_rejected():
    observation = replace(
        _observation("KIS", "2026-10-28"),
        adjustment="ADJUSTED",
    )
    with pytest.raises(CalendarContinuityRejected):
        assess_calendar_continuity(
            "KIS", "005930",
            (observation,),
            ("2026-10-28",),
        )


def test_direct_result_is_immutable():
    result = assess_calendar_continuity(
        "KIS", "005930",
        (_observation("KIS", "2026-10-28"),),
        ("2026-10-28",),
    )
    with pytest.raises(FrozenInstanceError):
        result.official_calendar_verified = True
