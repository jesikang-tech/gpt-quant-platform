"""Offline provider-to-analysis denial boundary.

Reuses the existing provenance gate. No analysis, broker, database,
network, dashboard, or persistence execution is performed here.
"""

from dataclasses import dataclass

from core.price_provenance_gate import assess_price_provenance

from .provider_contract import RawPriceObservation, ProviderObservationRejected
from .provider_evidence import ProviderEvidenceDecision
from .trading_day_certification import TradingDayCertificationDecision


@dataclass(frozen=True)
class ProviderAnalysisBoundaryDecision:
    provider: str
    ticker: str
    observation_date: str
    status: str
    reason: str
    analysis_authorized: bool = False
    dashboard_authorized: bool = False
    snapshot_authorized: bool = False
    persistence_authorized: bool = False


def assess_provider_analysis_boundary(
    observation, evidence_decision, trading_day_decision
):
    """Preserve identity while denying all unverified operational use."""
    if type(observation) is not RawPriceObservation:
        raise ProviderObservationRejected("Invalid observation type")

    if observation.adjustment != "UNKNOWN":
        raise ProviderObservationRejected("Unverified adjustment must remain UNKNOWN")

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

    provenance = assess_price_provenance(
        provider=observation.provider,
        adjustment=observation.adjustment,
    )

    if (
        provenance.status != "BLOCKED"
        or provenance.analysis_authorized is not False
        or provenance.dashboard_authorized is not False
        or provenance.snapshot_authorized is not False
        or provenance.persistence_authorized is not False
    ):
        raise ProviderObservationRejected("Provenance authority escalation")

    return ProviderAnalysisBoundaryDecision(
        provider=observation.provider,
        ticker=observation.ticker,
        observation_date=observation.observation_date,
        status=provenance.status,
        reason="UNVERIFIED_PROVIDER_PROVENANCE_ADJUSTMENT_AND_TRADING_DAY",
    )
