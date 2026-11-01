"""Fail-closed provider instrument and price-quality integration.

Instrument kinds are declarations, not exchange classifications.
No API-support certification, market-data certification, or authority.
"""
from dataclasses import dataclass, field

from .kiwoom_instrument_scope import (
    InstrumentKind,
    assess_kiwoom_instrument_scope,
)
from .provider_contract import (
    ProviderObservationRejected,
    RawPriceObservation,
    SUPPORTED_PROVIDERS,
)
from .provider_quality_entry import assess_provider_observation_quality


@dataclass(frozen=True)
class ProviderInstrumentQualityDecision:
    provider: str
    ticker: str
    observation_date: str
    instrument_kind: InstrumentKind
    structural_status: str
    structural_reason: str
    structural_trading_day_eligible: bool
    instrument_support_status: str = field(
        default="UNVERIFIED", init=False
    )
    instrument_classification_verified: bool = field(
        default=False, init=False
    )
    official_trading_day_verified: bool = field(
        default=False, init=False
    )
    independently_verified: bool = field(default=False, init=False)
    status: str = field(default="DENIED", init=False)
    reason: str = field(
        default="INSTRUMENT_AND_PRICE_NOT_INDEPENDENTLY_VERIFIED",
        init=False,
    )
    api_execution_authorized: bool = field(default=False, init=False)
    analysis_authorized: bool = field(default=False, init=False)
    dashboard_authorized: bool = field(default=False, init=False)
    snapshot_authorized: bool = field(default=False, init=False)
    persistence_authorized: bool = field(default=False, init=False)
    database_rebuild_authorized: bool = field(default=False, init=False)
    broker_execution_authorized: bool = field(default=False, init=False)


def assess_provider_instrument_quality(
    observation, instrument_kind, *, kiwoom_api_id=None
):
    """Reuse quality and Kiwoom scope contracts without certification."""
    if type(observation) is not RawPriceObservation:
        raise ProviderObservationRejected("Invalid observation type")

    if observation.provider not in SUPPORTED_PROVIDERS:
        raise ProviderObservationRejected("Unsupported provider")

    if type(instrument_kind) is not InstrumentKind:
        raise ProviderObservationRejected("Invalid instrument kind")

    if observation.adjustment != "UNKNOWN":
        raise ProviderObservationRejected("Unverified adjustment escalation")

    if observation.provider == "KIWOOM":
        scope = assess_kiwoom_instrument_scope(
            kiwoom_api_id, observation.ticker, instrument_kind
        )
        if (
            scope.provider != observation.provider
            or scope.ticker != observation.ticker
            or scope.instrument_kind is not instrument_kind
            or scope.support_status != "UNVERIFIED"
            or scope.api_execution_authorized is not False
            or scope.analysis_authorized is not False
            or scope.persistence_authorized is not False
            or scope.database_rebuild_authorized is not False
        ):
            raise ProviderObservationRejected(
                "Instrument scope authority escalation"
            )
    elif kiwoom_api_id is not None:
        raise ProviderObservationRejected(
            "Kiwoom API identifier on non-Kiwoom observation"
        )

    quality = assess_provider_observation_quality(observation)

    if (
        quality.provider != observation.provider
        or quality.ticker != observation.ticker
        or quality.observation_date != observation.observation_date
        or quality.status != "DENIED"
        or quality.official_trading_day_verified is not False
        or quality.analysis_authorized is not False
        or quality.dashboard_authorized is not False
        or quality.snapshot_authorized is not False
        or quality.persistence_authorized is not False
    ):
        raise ProviderObservationRejected(
            "Price quality authority escalation"
        )

    return ProviderInstrumentQualityDecision(
        provider=observation.provider,
        ticker=observation.ticker,
        observation_date=observation.observation_date,
        instrument_kind=instrument_kind,
        structural_status=quality.structural_status,
        structural_reason=quality.structural_reason,
        structural_trading_day_eligible=(
            quality.structural_trading_day_eligible
        ),
    )
