"""Fail-closed external price persistence entry.

This module performs no broker, network, database or filesystem I/O.
Unverified provider data never reaches the supplied persistence callback.
"""

from core.price_provenance_gate import (
    assess_price_provenance,
    require_persistence_authorization,
)

from .provider_contract import (
    RawPriceObservation,
    ProviderObservationRejected,
)
from .provider_evidence import ProviderEvidenceDecision
from .provider_usage_policy import UsageAssessment
from .trading_day_certification import TradingDayCertificationDecision


def invoke_provider_persistence(
    observation,
    usage_decision,
    evidence_decision,
    trading_day_decision,
    persist_callback,
):
    """Reject unverified persistence before executing a callback."""
    if type(observation) is not RawPriceObservation:
        raise ProviderObservationRejected("Invalid observation type")

    if observation.provider != "KIWOOM":
        raise ProviderObservationRejected("Unsupported persistence provider")

    if observation.adjustment != "UNKNOWN":
        raise ProviderObservationRejected("Unverified adjustment must remain UNKNOWN")

    if type(usage_decision) is not UsageAssessment:
        raise ProviderObservationRejected("Invalid usage decision type")

    if (
        usage_decision.provider != observation.provider
        or usage_decision.independently_verified is not False
        or usage_decision.api_execution_authorized is not False
        or usage_decision.analysis_authorized is not False
        or usage_decision.persistence_authorized is not False
        or usage_decision.redistribution_authorized is not False
        or usage_decision.database_rebuild_authorized is not False
    ):
        raise ProviderObservationRejected("Usage authority escalation")

    if type(evidence_decision) is not ProviderEvidenceDecision:
        raise ProviderObservationRejected("Invalid evidence decision type")

    if (
        evidence_decision.status != "DENIED"
        or evidence_decision.independently_verified is not False
        or evidence_decision.analysis_authorized is not False
        or evidence_decision.persistence_authorized is not False
    ):
        raise ProviderObservationRejected("Evidence authority escalation")

    if type(trading_day_decision) is not TradingDayCertificationDecision:
        raise ProviderObservationRejected("Invalid trading day decision type")

    if (
        trading_day_decision.status != "DENIED"
        or trading_day_decision.official_trading_day_verified is not False
        or trading_day_decision.analysis_authorized is not False
        or trading_day_decision.persistence_authorized is not False
    ):
        raise ProviderObservationRejected("Trading day authority escalation")

    if not callable(persist_callback):
        raise ProviderObservationRejected("Invalid persistence callback")

    provenance = assess_price_provenance(
        provider=observation.provider,
        adjustment=observation.adjustment,
    )

    require_persistence_authorization(provenance)

    raise ProviderObservationRejected(
        "Unreachable unverified persistence boundary"
    )
