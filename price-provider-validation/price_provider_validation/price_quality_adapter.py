"""Fail-closed reference to existing synthetic price quality contracts.

No provider certification, database access, or operational authorization.
"""

from dataclasses import dataclass

from .provider_contract import RawPriceObservation, ProviderObservationRejected
from .ohlcv_mapping import OhlcvFieldMapping, map_raw_ohlcv


@dataclass(frozen=True)
class ProviderPriceQualityInput:
    provider: str
    ticker: str
    observation_date: str
    ohlcv: tuple
    adjustment: str = "UNKNOWN"
    analysis_authorized: bool = False
    persistence_authorized: bool = False


def prepare_provider_price_quality_input(observation, mapping):
    """Prepare mapped values without certifying prices or trading dates."""
    if type(observation) is not RawPriceObservation:
        raise ProviderObservationRejected("Invalid observation type")
    if observation.adjustment != "UNKNOWN":
        raise ProviderObservationRejected("Unverified adjustment must remain UNKNOWN")

    values = map_raw_ohlcv(observation, mapping)
    return ProviderPriceQualityInput(
        provider=observation.provider,
        ticker=observation.ticker,
        observation_date=observation.observation_date,
        ohlcv=tuple(values[name] for name in ("Open", "High", "Low", "Close", "Volume")),
    )


def existing_trading_session_contract():
    """Identify the existing pure classifier without importing or executing it."""
    return (
        "naver-decimal-validation/core/trading_session_eligibility.py",
        "assess_trading_session",
    )

def assess_provider_price_quality(quality_input):
    """Reuse the existing structural classifier without granting authority."""
    from core.trading_session_eligibility import assess_trading_session

    if type(quality_input) is not ProviderPriceQualityInput:
        raise ProviderObservationRejected("Invalid quality input type")

    if quality_input.adjustment != "UNKNOWN":
        raise ProviderObservationRejected("Unverified adjustment must remain UNKNOWN")

    if (
        quality_input.analysis_authorized is not False
        or quality_input.persistence_authorized is not False
    ):
        raise ProviderObservationRejected("Quality input authority escalation")

    if type(quality_input.ohlcv) is not tuple or len(quality_input.ohlcv) != 5:
        raise ProviderObservationRejected("Five OHLCV fields required")

    return assess_trading_session(
        quality_input.ohlcv[3],
        quality_input.ohlcv,
    )
