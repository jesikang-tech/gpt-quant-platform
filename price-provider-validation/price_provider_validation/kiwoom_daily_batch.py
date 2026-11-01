"""Offline validation of one Kiwoom daily response batch.

No HTTP, authentication, database, broker, or operational authority.
"""
from datetime import date

from .kiwoom_daily_response import (
    kiwoom_daily_array_field,
    prepare_kiwoom_daily_observation,
)
from .provider_contract import ProviderObservationRejected


MAX_DAILY_ROWS = 1000


def prepare_kiwoom_daily_batch(
    api_id, ticker, response, *, requested_base_date
):
    """Validate one response batch without certifying market data."""
    array_field = kiwoom_daily_array_field(api_id)

    if type(response) is not dict:
        raise ProviderObservationRejected("Invalid response envelope")

    if type(requested_base_date) is not str:
        raise ProviderObservationRejected("Invalid requested base date")

    try:
        base_date = date.fromisoformat(requested_base_date)
    except ValueError as exc:
        raise ProviderObservationRejected("Invalid requested base date") from exc

    if base_date.isoformat() != requested_base_date:
        raise ProviderObservationRejected("Noncanonical base date")

    if array_field not in response:
        raise ProviderObservationRejected("Missing daily response array")

    rows = response[array_field]

    if type(rows) is not list or not 1 <= len(rows) <= MAX_DAILY_ROWS:
        raise ProviderObservationRejected("Invalid daily response size")

    observations = []
    seen_dates = set()

    for row in rows:
        observation = prepare_kiwoom_daily_observation(
            api_id, ticker, row
        )

        if observation.observation_date in seen_dates:
            raise ProviderObservationRejected("Duplicate observation date")

        if observation.observation_date > requested_base_date:
            raise ProviderObservationRejected("Observation after base date")

        seen_dates.add(observation.observation_date)
        observations.append(observation)

    return tuple(observations)
