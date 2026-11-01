"""Fail-closed platform integration of existing provider evidence contracts.

Synthetic and offline only. No API, database, broker or filesystem I/O.
"""
from dataclasses import dataclass, field

from .provider_contract import RawPriceObservation
from .provider_evidence import (
    ProviderEvidence,
    ProviderEvidenceDecision,
    assess_observation_evidence_binding,
)
from .trading_day_certification import TradingDayCertificationDecision


class ProviderPlatformIntegrationRejected(ValueError):
    pass


@dataclass(frozen=True)
class ProviderPlatformIntegrationDecision:
    provider: str
    ticker: str
    observation_date: str
    evidence_status: str
    trading_day_status: str
    reason: str = "PROVIDER_PLATFORM_AUTHORITY_NOT_VERIFIED"
    status: str = field(default="DENIED", init=False)
    independently_verified: bool = field(default=False, init=False)
    api_execution_authorized: bool = field(default=False, init=False)
    analysis_authorized: bool = field(default=False, init=False)
    dashboard_authorized: bool = field(default=False, init=False)
    snapshot_authorized: bool = field(default=False, init=False)
    persistence_authorized: bool = field(default=False, init=False)
    redistribution_authorized: bool = field(default=False, init=False)
    database_rebuild_authorized: bool = field(default=False, init=False)
    live_api_execution_authorized: bool = field(default=False, init=False)
    broker_execution_authorized: bool = field(default=False, init=False)


def assess_provider_platform_integration(
    observation, evidence, trading_day_decision
):
    """Bind untrusted evidence to an observation without granting authority."""
    if type(observation) is not RawPriceObservation:
        raise ProviderPlatformIntegrationRejected("Invalid observation type")

    if type(evidence) is not ProviderEvidence:
        raise ProviderPlatformIntegrationRejected("Invalid evidence type")

    if type(trading_day_decision) is not TradingDayCertificationDecision:
        raise ProviderPlatformIntegrationRejected("Invalid trading-day decision type")

    if observation.adjustment != "UNKNOWN" or evidence.adjustment != "UNKNOWN":
        raise ProviderPlatformIntegrationRejected("Adjustment policy not verified")

    if (
        trading_day_decision.status != "DENIED"
        or trading_day_decision.official_trading_day_verified is not False
        or trading_day_decision.analysis_authorized is not False
        or trading_day_decision.persistence_authorized is not False
    ):
        raise ProviderPlatformIntegrationRejected("Trading-day authority escalation")

    if (
        type(trading_day_decision.structural_status) is not str
        or trading_day_decision.structural_status not in (
            "CANDIDATE", "BLOCKED", "NON_TRADING"
        )
        or type(trading_day_decision.structural_reason) is not str
        or not trading_day_decision.structural_reason
        or type(trading_day_decision.structural_trading_day_eligible) is not bool
        or (
            trading_day_decision.structural_status == "CANDIDATE"
        ) is not trading_day_decision.structural_trading_day_eligible
    ):
        raise ProviderPlatformIntegrationRejected(
            "Inconsistent structural trading-day decision"
        )

    try:
        evidence_decision = assess_observation_evidence_binding(
            observation, evidence
        )
    except ValueError as exc:
        raise ProviderPlatformIntegrationRejected(
            "Observation evidence binding rejected"
        ) from exc

    if type(evidence_decision) is not ProviderEvidenceDecision:
        raise ProviderPlatformIntegrationRejected("Invalid evidence decision")

    if (
        evidence_decision.status != "DENIED"
        or evidence_decision.independently_verified is not False
        or evidence_decision.analysis_authorized is not False
        or evidence_decision.persistence_authorized is not False
    ):
        raise ProviderPlatformIntegrationRejected("Evidence authority escalation")

    return ProviderPlatformIntegrationDecision(
        provider=observation.provider,
        ticker=observation.ticker,
        observation_date=observation.observation_date,
        evidence_status=evidence_decision.status,
        trading_day_status=trading_day_decision.status,
    )
