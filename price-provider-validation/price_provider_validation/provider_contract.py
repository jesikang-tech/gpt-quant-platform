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
    from datetime import date

    if type(provider) is not str or provider not in SUPPORTED_PROVIDERS:
        raise ProviderObservationRejected("Unsupported provider")

    if (
        type(ticker) is not str
        or not ticker
        or ticker != ticker.strip()
    ):
        raise ProviderObservationRejected("Invalid ticker")

    if type(observation_date) is not str:
        raise ProviderObservationRejected("Invalid observation date")

    try:
        parsed_date = date.fromisoformat(observation_date)
    except ValueError as exc:
        raise ProviderObservationRejected("Invalid observation date") from exc

    if parsed_date.isoformat() != observation_date:
        raise ProviderObservationRejected("Noncanonical observation date")

    if type(raw_fields) is not tuple or len(raw_fields) != 5:
        raise ProviderObservationRejected("Exactly five raw fields required")

    return RawPriceObservation(
        provider=provider,
        ticker=ticker,
        observation_date=observation_date,
        raw_fields=raw_fields,
    )
