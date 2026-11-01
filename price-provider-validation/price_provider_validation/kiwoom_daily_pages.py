"""Offline validation of ordered Kiwoom daily response pages.

Page order is synthetic input, not authenticated broker pagination.
No HTTP, authentication, database, or execution authority.
"""
from .kiwoom_daily_batch import prepare_kiwoom_daily_batch
from .provider_contract import ProviderObservationRejected


MAX_DAILY_PAGES = 100


def prepare_kiwoom_daily_pages(
    api_id, ticker, responses, *, requested_base_date
):
    """Validate ordered pages without certifying historical completeness."""
    if type(responses) is not list or not 1 <= len(responses) <= MAX_DAILY_PAGES:
        raise ProviderObservationRejected("Invalid page count")

    observations = []
    previous_date = None

    for response in responses:
        batch = prepare_kiwoom_daily_batch(
            api_id,
            ticker,
            response,
            requested_base_date=requested_base_date,
        )

        for observation in batch:
            current_date = observation.observation_date
            if previous_date is not None and current_date >= previous_date:
                raise ProviderObservationRejected(
                    "Duplicate or out-of-order observation date"
                )
            observations.append(observation)
            previous_date = current_date

    return tuple(observations)
