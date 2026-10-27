"""Provider-neutral, untrusted price observation contract.

No API, database, filesystem, or broker operations.
"""
from dataclasses import dataclass


SUPPORTED_PROVIDERS = frozenset({"KIS", "KIWOOM"})


class ProviderObservationRejected(ValueError):
    pass


@dataclass(frozen=True)
class RawPriceObservation:
    provider: str
    ticker: str
    observation_date: str
    raw_fields: tuple
    adjustment: str = "UNKNOWN"


def prepare_raw_observation(provider, ticker, observation_date, raw_fields):
    if provider not in SUPPORTED_PROVIDERS:
        raise ProviderObservationRejected("Unsupported provider")

    if type(ticker) is not str or not ticker.strip():
        raise ProviderObservationRejected("Invalid ticker")

    if type(observation_date) is not str or not observation_date.strip():
        raise ProviderObservationRejected("Invalid observation date")

    if type(raw_fields) is not tuple:
        raise ProviderObservationRejected("Raw fields must be a tuple")

    return RawPriceObservation(
        provider=provider,
        ticker=ticker,
        observation_date=observation_date,
        raw_fields=raw_fields,
    )
