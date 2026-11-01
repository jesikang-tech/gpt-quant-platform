"""Offline provider observation to quality decision entry.

Reuses existing OHLCV mapping and quality integration contracts.
No provenance certification, API, broker, database or execution authority.
"""

from .ohlcv_mapping import OhlcvFieldMapping
from .price_quality_adapter import prepare_provider_price_quality_input
from .provider_contract import (
    ProviderObservationRejected,
    RawPriceObservation,
)
from .provider_quality_integration import (
    ProviderQualityIntegrationDecision,
    assess_provider_quality_integration,
)


def assess_provider_observation_quality(observation):
    """Assess an unverified observation; never grant operational authority."""
    if type(observation) is not RawPriceObservation:
        raise ProviderObservationRejected("Invalid observation type")

    if observation.provider not in ("KIS", "KIWOOM"):
        raise ProviderObservationRejected("Unsupported provider")

    if observation.adjustment != "UNKNOWN":
        raise ProviderObservationRejected("Unverified adjustment claim")

    mapping = OhlcvFieldMapping(0, 1, 2, 3, 4)
    quality_input = prepare_provider_price_quality_input(
        observation, mapping
    )
    decision = assess_provider_quality_integration(quality_input)

    if type(decision) is not ProviderQualityIntegrationDecision:
        raise ProviderObservationRejected("Invalid integration decision")

    if (
        decision.provider != observation.provider
        or decision.ticker != observation.ticker
        or decision.observation_date != observation.observation_date
        or decision.status != "DENIED"
        or decision.official_trading_day_verified is not False
        or decision.analysis_authorized is not False
        or decision.dashboard_authorized is not False
        or decision.snapshot_authorized is not False
        or decision.persistence_authorized is not False
    ):
        raise ProviderObservationRejected("Quality authority escalation")

    return decision
