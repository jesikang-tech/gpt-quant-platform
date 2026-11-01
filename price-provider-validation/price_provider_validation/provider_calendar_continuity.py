"""Offline calendar-continuity comparison; never official certification.

Both calendar dates and observation dates are caller-supplied.
A complete match cannot establish exchange-calendar authenticity,
historical completeness, or authorization.
"""
from dataclasses import dataclass, field
from datetime import date

from .provider_contract import (
    RawPriceObservation,
    SUPPORTED_PROVIDERS,
)


class CalendarContinuityRejected(ValueError):
    pass


MAX_CALENDAR_DAYS = 10000


@dataclass(frozen=True)
class CalendarContinuityAssessment:
    provider: str
    ticker: str
    observed_count: int
    calendar_count: int
    missing_dates: tuple
    reason: str = field(
        default="OFFICIAL_CALENDAR_NOT_INDEPENDENTLY_VERIFIED",
        init=False,
    )
    status: str = field(default="DENIED", init=False)
    official_calendar_verified: bool = field(default=False, init=False)
    historical_completeness_verified: bool = field(default=False, init=False)
    independently_verified: bool = field(default=False, init=False)
    analysis_authorized: bool = field(default=False, init=False)
    dashboard_authorized: bool = field(default=False, init=False)
    persistence_authorized: bool = field(default=False, init=False)
    database_rebuild_authorized: bool = field(default=False, init=False)
    broker_execution_authorized: bool = field(default=False, init=False)


def _canonical_date(value):
    if type(value) is not str:
        raise CalendarContinuityRejected("Invalid date type")
    try:
        parsed = date.fromisoformat(value)
    except ValueError as exc:
        raise CalendarContinuityRejected("Invalid date") from exc
    if parsed.isoformat() != value:
        raise CalendarContinuityRejected("Noncanonical date")
    return value


def assess_calendar_continuity(
    provider, ticker, observations, calendar_dates
):
    """Compare descending observations with untrusted calendar dates."""
    if type(provider) is not str or provider not in SUPPORTED_PROVIDERS:
        raise CalendarContinuityRejected("Unsupported provider")

    if type(ticker) is not str or not ticker or ticker != ticker.strip():
        raise CalendarContinuityRejected("Invalid ticker")

    if type(observations) is not tuple or not observations:
        raise CalendarContinuityRejected("Invalid observation collection")

    if (
        type(calendar_dates) is not tuple
        or not 1 <= len(calendar_dates) <= MAX_CALENDAR_DAYS
    ):
        raise CalendarContinuityRejected("Invalid calendar collection")

    checked_calendar = tuple(_canonical_date(day) for day in calendar_dates)

    if any(
        checked_calendar[i] <= checked_calendar[i + 1]
        for i in range(len(checked_calendar) - 1)
    ):
        raise CalendarContinuityRejected(
            "Duplicate or out-of-order calendar date"
        )

    observed_dates = []
    for observation in observations:
        if type(observation) is not RawPriceObservation:
            raise CalendarContinuityRejected("Invalid observation type")

        if observation.provider != provider or observation.ticker != ticker:
            raise CalendarContinuityRejected("Observation identity mismatch")

        if observation.adjustment != "UNKNOWN":
            raise CalendarContinuityRejected(
                "Unverified adjustment escalation"
            )

        observed_dates.append(_canonical_date(observation.observation_date))

    if any(
        observed_dates[i] <= observed_dates[i + 1]
        for i in range(len(observed_dates) - 1)
    ):
        raise CalendarContinuityRejected(
            "Duplicate or out-of-order observation date"
        )

    calendar_set = set(checked_calendar)
    if any(day not in calendar_set for day in observed_dates):
        raise CalendarContinuityRejected(
            "Observation outside declared calendar"
        )

    first_day = observed_dates[0]
    last_day = observed_dates[-1]

    expected_in_span = tuple(
        day for day in checked_calendar
        if last_day <= day <= first_day
    )

    observed_set = set(observed_dates)
    missing = tuple(
        day for day in expected_in_span
        if day not in observed_set
    )

    return CalendarContinuityAssessment(
        provider=provider,
        ticker=ticker,
        observed_count=len(observed_dates),
        calendar_count=len(expected_in_span),
        missing_dates=missing,
    )
